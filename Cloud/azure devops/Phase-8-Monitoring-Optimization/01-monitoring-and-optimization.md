# Monitoring, Observability & Pipeline Optimization

> **Expert framing:** Instrumenting an app with Application Insights is basic. Expert-level observability is knowing which of the three pillars (logs/metrics/traces) actually answers the question you're asking, writing KQL that scales (not scanning huge time ranges unnecessarily), and treating pipeline speed as a first-class engineering concern (caching, parallelism, templates) rather than an afterthought once builds get painfully slow.

## The Three Pillars of Observability
1. **Logs** – What happened? (Text records of events)
2. **Metrics** – How is it performing? (CPU, memory, request rate, error %)
3. **Traces** – Why is it slow? (End-to-end request flow across microservices)

Azure handles all three via **Application Insights** and **Azure Monitor**.

---

## Application Insights

### Instrumenting a Node.js App
```bash
# Install the SDK
npm install applicationinsights
```

```javascript
// server.js - MUST be the VERY FIRST import
import appInsights from "applicationinsights";

appInsights.setup(process.env.APPLICATIONINSIGHTS_CONNECTION_STRING)
  .setAutoDependencyCorrelation(true)
  .setAutoCollectRequests(true)
  .setAutoCollectPerformance(true, true)
  .setAutoCollectExceptions(true)
  .setAutoCollectDependencies(true)   // Track calls to SQL, Redis, HTTP, etc.
  .setSendLiveMetrics(true)
  .start();

// Now your normal app code:
import express from "express";
const app = express();

// Manually track a custom event
const client = appInsights.defaultClient;
client.trackEvent({ name: "UserLoggedIn", properties: { userId: "user123" } });

// Manually track a custom metric
client.trackMetric({ name: "OrderProcessingTime", value: 142 });

// Manually track an exception
try {
  throw new Error("Something failed");
} catch (err) {
  client.trackException({ exception: err });
}
```

### Setting up Application Insights in Azure
```bash
# Create a Log Analytics Workspace
az monitor log-analytics workspace create \
  --resource-group rg-monitoring \
  --workspace-name law-myapp-prod

# Create Application Insights
az monitor app-insights component create \
  --app insights-myapp-prod \
  --location eastus \
  --resource-group rg-monitoring \
  --workspace /subscriptions/<SUB>/resourceGroups/rg-monitoring/providers/Microsoft.OperationalInsights/workspaces/law-myapp-prod

# Get the Connection String
az monitor app-insights component show \
  --app insights-myapp-prod \
  --resource-group rg-monitoring \
  --query connectionString --output tsv
```

---

## Azure Monitor & KQL (Kusto Query Language)

KQL is the query language for Log Analytics. In the Azure Portal, go to: **Log Analytics Workspace → Logs**.

### KQL Query Examples

```kusto
// View all application traces in the last hour
AppTraces
| where TimeGenerated > ago(1h)
| where SeverityLevel >= 2  // Warning and above
| order by TimeGenerated desc
| take 100

// Request rate and average duration per endpoint
AppRequests
| where TimeGenerated > ago(24h)
| summarize 
    RequestCount = count(), 
    AvgDuration = avg(DurationMs), 
    FailedCount = countif(Success == false)
  by Name  // Name = URL path
| order by RequestCount desc

// Top exceptions in the last 7 days
AppExceptions
| where TimeGenerated > ago(7d)
| summarize Count = count() by ExceptionType, OuterMessage
| order by Count desc
| take 20

// Slow dependencies (e.g., slow SQL queries)
AppDependencies
| where TimeGenerated > ago(1h) and DurationMs > 500
| project TimeGenerated, Target, Name, DurationMs, Success
| order by DurationMs desc

// Pipeline failure rate (from Azure DevOps to Log Analytics)
AzureDevOpsAuditEvents
| where TimeGenerated > ago(30d)
| where OperationName == "Build.RequestedForUser"
| summarize Success = countif(Data contains "Succeeded"), 
            Failed = countif(Data contains "Failed")
| extend SuccessRate = round(100.0 * Success / (Success + Failed), 2)
```

**Expert insight — writing KQL that doesn't fall over at scale:**
- **Always filter on `TimeGenerated` first**, before other `where` clauses — KQL is optimized to prune by time range early; filtering time last (or omitting it) forces a scan across the entire retention window, which gets slow and expensive as data volume grows.
- **`summarize` before `project`** when you only need aggregated results — projecting first and summarizing after processes unnecessary row-level data through the pipeline.
- **Prefer `has`/`contains` only when necessary** — `has` is faster than `contains` because it matches on indexed whole-term tokens rather than doing a full substring scan; use `contains` only when you genuinely need substring matching (e.g., partial words).
- These aren't just performance trivia — a KQL query scanning a huge un-time-filtered range against a busy Log Analytics workspace is a common real-world cause of slow, expensive dashboards and alert queries that time out.

---

## Setting Up Alerts

```bash
# Alert when HTTP error rate exceeds 5%
az monitor metrics alert create \
  --name "High-Error-Rate-Alert" \
  --resource-group rg-monitoring \
  --scopes /subscriptions/<SUB>/resourceGroups/rg-production/providers/Microsoft.Web/sites/app-myapp-prod \
  --condition "avg Http5xx > 5" \
  --window-size 5m \
  --evaluation-frequency 1m \
  --action /subscriptions/<SUB>/resourceGroups/rg-monitoring/providers/Microsoft.Insights/actionGroups/DevOps-Team-ActionGroup \
  --severity 2

# Create an Action Group (who to notify and how)
az monitor action-group create \
  --name "DevOps-Team-ActionGroup" \
  --resource-group rg-monitoring \
  --short-name "DevOpsTeam" \
  --email-receiver name="OnCallEngineer" email-address="oncall@company.com"
```

---

## Pipeline Optimization

### Pipeline Caching
Caching prevents re-downloading `node_modules`, Maven dependencies, etc. on every run.

```yaml
variables:
  npm_cache_dir: $(Pipeline.Workspace)/.npm

steps:
  # Restore cache
  - task: Cache@2
    displayName: 'Cache npm dependencies'
    inputs:
      key: 'npm | "$(Agent.OS)" | package-lock.json'
      restoreKeys: |
        npm | "$(Agent.OS)"
      path: $(npm_cache_dir)

  # Use cached node_modules
  - script: npm ci --cache $(npm_cache_dir)
    displayName: 'npm install (with cache)'
```

### YAML Templates (DRY Pipelines)
```yaml
# templates/install-and-test.yml (reusable template)
parameters:
  - name: nodeVersion
    type: string
    default: '20.x'

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: ${{ parameters.nodeVersion }}

  - script: npm ci
    displayName: 'Install dependencies'

  - script: npm test
    displayName: 'Run tests'

  - task: PublishTestResults@2
    inputs:
      testResultsFormat: 'JUnit'
      testResultsFiles: '**/test-results.xml'
```

```yaml
# azure-pipelines.yml - Using the template
stages:
  - stage: Test
    jobs:
      - job: TestNode20
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - template: templates/install-and-test.yml
            parameters:
              nodeVersion: '20.x'

      - job: TestNode18
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - template: templates/install-and-test.yml
            parameters:
              nodeVersion: '18.x'
```

### Parallel Jobs Strategy
```yaml
# Run tests in parallel across multiple agents
strategy:
  matrix:
    Node_20_Ubuntu:
      imageToUse: 'ubuntu-latest'
      nodeVersion: '20.x'
    Node_20_Windows:
      imageToUse: 'windows-latest'
      nodeVersion: '20.x'
    Node_18_Ubuntu:
      imageToUse: 'ubuntu-latest'
      nodeVersion: '18.x'
  maxParallel: 3  # Run all 3 at the same time

pool:
  vmImage: $(imageToUse)

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: $(nodeVersion)
  - script: npm test
```

---

## Common Pitfalls & Expert Tips

- **Alerting on raw thresholds without accounting for normal variance.** A static "CPU > 80%" alert fires constantly on a workload with legitimate periodic spikes (batch jobs, traffic bursts) — leading to alert fatigue where the team starts ignoring alerts entirely (the real danger, since it means a *genuine* incident gets ignored too). Use dynamic thresholds or aggregate over a sensible window (e.g., sustained for 5+ minutes) instead.
- **Logging everything at maximum verbosity in production.** Excessive logging increases Application Insights/Log Analytics ingestion cost significantly and makes genuinely important signals harder to find in the noise — sample or filter appropriately (Application Insights supports adaptive sampling for exactly this reason).
- **Not correlating traces across services.** Without distributed tracing (`setAutoDependencyCorrelation(true)`), a slow user-facing request in a microservices architecture is nearly impossible to root-cause — you see the symptom (slow request) but not which downstream dependency actually caused it.
- **Caching keyed only on `Agent.OS` without including the lockfile hash.** A cache key like `npm | "$(Agent.OS)"` alone never invalidates when dependencies change — the pipeline keeps using stale cached dependencies. Always include a hash of the lockfile (`package-lock.json`) in the key so the cache automatically invalidates when dependencies actually change.
- **Copy-pasting the same pipeline steps across many `azure-pipelines.yml` files instead of using templates.** This is a maintenance trap — a fix or improvement has to be manually applied to every copy, and they inevitably drift out of sync over time.
- **Running everything sequentially "because it's simpler."** Independent test suites, lint checks, and builds across different configurations (Node versions, OSes) should run in parallel via a `matrix` strategy — sequential execution wastes wall-clock time for no correctness benefit when the jobs don't actually depend on each other.

---

## Practical Exercise ✅
1. Create an Application Insights instance and integrate it into a Node.js app.
2. Deploy the app and trigger a few requests + one intentional error.
3. Write a KQL query in Log Analytics to find all requests with `DurationMs > 200ms`.
4. Add a `Cache@2` step to your pipeline. Compare the build time before and after.
5. Extract 2+ repeated steps into a YAML template file and reference it across 2 pipeline stages.

---

## Expert Interview Q&A

**Q: Logs, Metrics, and Traces — give a concrete scenario where you'd need each, and why one wouldn't be enough alone.**
Metrics tell you *something* is wrong fast (error rate spiked at 2:14pm) but not *why*. Traces show you the end-to-end path of a specific slow/failed request across multiple services, pinpointing *where* in the chain the time was lost or the failure occurred. Logs give you the detailed contextual message at that exact point (a stack trace, a specific input value that caused the failure) once traces have narrowed down *where* to look. In practice: metrics alert you, traces localize the problem, logs explain the root cause.

**Q: Why does alert fatigue actually make systems less reliable, and how do you design around it?**
If alerts fire too often for non-actionable reasons (normal variance, transient blips), the on-call team starts to reflexively dismiss or mute them — meaning a genuinely critical alert gets the same "probably nothing" treatment and is missed or delayed. Design around it with thresholds that require sustained breach (not single data points), dynamic/seasonal baselines instead of static numbers where traffic patterns vary, and routing only truly actionable alerts to paging channels (informational ones to a dashboard instead).

**Q: Your pipeline caching isn't actually speeding anything up even though you added a `Cache@2` step. What's the likely misconfiguration?**
The cache key is probably too broad or too narrow. Too broad (e.g., keyed only on OS) means it never invalidates and might serve stale dependencies, or the restore itself takes as long as a fresh install if the cache is enormous and unfocused. Too narrow/unstable (e.g., including a timestamp or build ID in the key) means it *never* gets a cache hit because the key is different every single run. The correct key includes something stable that changes exactly when the cache should invalidate — typically a hash of the lockfile.

**Q: When would you use a pipeline `matrix` strategy versus a single sequential job with multiple steps?**
Use a matrix when the work is genuinely independent and would benefit from running concurrently — e.g., testing against multiple Node versions or OSes, where a failure in one combination shouldn't block or be conflated with another. Sequential steps are appropriate when there's a real dependency between steps (build must complete before test can run against its output) — parallelizing dependent steps would either fail or produce incorrect results.
