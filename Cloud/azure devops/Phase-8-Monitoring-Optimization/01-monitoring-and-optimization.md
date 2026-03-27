# Monitoring, Observability & Pipeline Optimization

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

## Practical Exercise ✅
1. Create an Application Insights instance and integrate it into a Node.js app.
2. Deploy the app and trigger a few requests + one intentional error.
3. Write a KQL query in Log Analytics to find all requests with `DurationMs > 200ms`.
4. Add a `Cache@2` step to your pipeline. Compare the build time before and after.
5. Extract 2+ repeated steps into a YAML template file and reference it across 2 pipeline stages.
