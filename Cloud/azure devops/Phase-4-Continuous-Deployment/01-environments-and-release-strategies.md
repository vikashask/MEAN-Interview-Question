# Continuous Deployment (CD) - Environments & Release Strategies

> **Expert framing:** The exam and interview favorite here is being able to explain, precisely, the *risk profile* of each deployment strategy (Blue-Green vs Canary vs Rolling) — not just "how to write the YAML." An expert also knows that approvals and automated gates solve different problems: approvals are a human judgment checkpoint, gates are an automated go/no-go based on system health, and production-grade pipelines usually need both.

## Azure DevOps Environments

An **Environment** is a logical grouping that represents a deployment target (Dev, QA, Staging, Prod). It provides:
- Deployment history for the environment.
- Approval gates before a deployment job runs.
- Resource tracking (Kubernetes namespaces, Virtual Machines).

### Creating an Environment via CLI
```bash
# Create an environment
az devops environment create \
  --name "Production" \
  --project "MyProject"
```

### Deployment Job in YAML
```yaml
# ================================================================
# MULTI-STAGE CD PIPELINE (Dev -> QA -> Prod)
# ================================================================
stages:
  # Stage 1: CI (Build)
  - stage: Build
    jobs:
      - job: BuildApp
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - script: npm ci && npm run build
          - task: PublishPipelineArtifact@1
            inputs:
              targetPath: './dist'
              artifact: 'dist-artifact'

  # Stage 2: Deploy to Dev (Auto - no approval needed)
  - stage: Deploy_Dev
    displayName: '🚀 Deploy to Dev'
    dependsOn: Build
    jobs:
      - deployment: DeployToDev
        environment: 'Development'       # Links to Azure DevOps Environment
        pool:
          vmImage: 'ubuntu-latest'
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: 'dist-artifact'
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: 'AzureServiceConnection'
                    appName: 'myapp-dev'
                    package: '$(Pipeline.Workspace)/dist-artifact'

  # Stage 3: Deploy to QA (Requires Manual Approval)
  - stage: Deploy_QA
    displayName: '🧪 Deploy to QA'
    dependsOn: Deploy_Dev
    jobs:
      - deployment: DeployToQA
        environment: 'QA'                # Configure approval in Azure DevOps portal
        pool:
          vmImage: 'ubuntu-latest'
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: 'dist-artifact'
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: 'AzureServiceConnection'
                    appName: 'myapp-qa'
                    package: '$(Pipeline.Workspace)/dist-artifact'

  # Stage 4: Deploy to Production (Requires Approval + Automated Gate)
  - stage: Deploy_Prod
    displayName: '🏭 Deploy to Production'
    dependsOn: Deploy_QA
    jobs:
      - deployment: DeployToProd
        environment: 'Production'
        pool:
          vmImage: 'ubuntu-latest'
        strategy:
          runOnce:
            deploy:
              steps:
                - download: current
                  artifact: 'dist-artifact'
                - task: AzureWebApp@1
                  inputs:
                    azureSubscription: 'AzureServiceConnection'
                    appName: 'myapp-prod'
                    package: '$(Pipeline.Workspace)/dist-artifact'
```

---

## Configuring Approvals on an Environment
1. Go to **Pipelines > Environments > Production**.
2. Click the three dots (**...**) > **Approvals and checks**.
3. Click **+** > **Approvals**.
4. Add approvers (e.g., `tech-lead@company.com`).
5. Set a timeout (e.g., 24 hours to approve or the pipeline fails).

**Expert insight — Approvals vs Checks/Gates, don't conflate them:**
- **Approvals** = a human must click "Approve" — a judgment-based checkpoint, good for compliance/change-management requirements (someone accountable signed off).
- **Checks/Gates** = automated conditions evaluated by the system — e.g., "Azure Monitor alert must be inactive," "no active incidents," "business hours only" (via the built-in "Business Hours" check). These catch things humans might miss or forget to check manually.
- Production-grade pipelines typically use **both**: an automated gate to block deployment during a known-bad system state, plus a human approval for accountability/change-control. Relying on only one is a common gap — pure-approval setups miss real-time system health; pure-gate setups miss judgment calls a human should make (e.g., "we're mid-incident on something unrelated, hold off anyway").

---

## Advanced Deployment Techniques

### Blue-Green Deployment (Zero Downtime)
```yaml
# Strategy: Deploy to a 'staging slot', smoke test, then swap slot to production
- stage: BlueGreen_Deploy
  jobs:
    - deployment: SwapSlots
      environment: 'Production'
      strategy:
        runOnce:
          deploy:
            steps:
              # Deploy to the STAGING slot (not live yet)
              - task: AzureWebApp@1
                displayName: 'Deploy to Staging Slot'
                inputs:
                  azureSubscription: 'AzureServiceConnection'
                  appName: 'myapp-prod'
                  deployToSlotOrASE: true
                  resourceGroupName: 'rg-production'
                  slotName: 'staging'
                  package: '$(Pipeline.Workspace)/dist-artifact'
              
              # Run smoke tests against the staging slot
              - script: |
                  curl -f https://myapp-prod-staging.azurewebsites.net/health || exit 1
                displayName: 'Smoke Test Staging Slot'

              # Swap staging to production
              - task: AzureAppServiceManage@0
                displayName: 'Swap Staging to Production'
                inputs:
                  azureSubscription: 'AzureServiceConnection'
                  action: 'Swap Slots'
                  webAppName: 'myapp-prod'
                  sourceSlot: 'staging'
                  swapWithProduction: true
```

### Canary Release (Rolling Deployment to AKS)
```yaml
# Deploy to 20% of pods first, validate, then roll out 100%
- deployment: CanaryDeploy
  environment: 'Production.kubernetes-namespace'
  strategy:
    canary:
      increments: [20, 100]  # First deploy to 20%, then 100%
      preDeploy:
        steps:
          - script: echo "Pre-deploy checks..."
      deploy:
        steps:
          - task: KubernetesManifest@0
            inputs:
              action: 'deploy'
              manifests: 'k8s/deployment.yaml'
              containers: 'myacr.azurecr.io/myapp:$(Build.BuildId)'
      postRouteTraffic:
        steps:
          - script: |
              echo "Running canary validation..."
              sleep 60  # Wait and check metrics
      on:
        failure:
          steps:
            - script: echo "Canary failed! Rolling back..."
        success:
          steps:
            - script: echo "Canary succeeded!"
```

---

## Feature Flags with Azure App Configuration
```javascript
// Node.js - Using Azure App Configuration feature flags
import { AppConfigurationClient } from "@azure/app-configuration";
import { DefaultAzureCredential } from "@azure/identity";

const client = new AppConfigurationClient(
  process.env.AZURE_APP_CONFIG_ENDPOINT,
  new DefaultAzureCredential()
);

async function isFeatureEnabled(flagName) {
  const setting = await client.getConfigurationSetting({
    key: `.appconfig.featureflag/${flagName}`,
  });
  const flag = JSON.parse(setting.value);
  return flag.enabled;
}

// Usage
if (await isFeatureEnabled("newCheckoutFlow")) {
  // Show new feature
} else {
  // Show old feature
}
```

---

## Common Pitfalls & Expert Tips

- **Skipping smoke tests before a slot swap in Blue-Green.** Swapping slots without validating the staging slot first defeats the entire point of the strategy — you're supposed to catch problems *before* they're live, not after.
- **Canary "increments" without real automated validation between steps.** If `postRouteTraffic` just `sleep`s instead of actually checking error rates/latency metrics, you're not really doing canary analysis — you're just delaying a blind full rollout by a minute.
- **No automatic rollback wired to canary/gate failure.** A canary strategy's entire value proposition is catching bad releases *before* 100% rollout and reverting — if `on: failure:` just logs a message instead of triggering an actual rollback action, the safety net is cosmetic.
- **Feature flags left in code indefinitely.** Feature flags used for progressive rollout should be temporary — permanent flags accumulate into "flag debt" that makes the codebase harder to reason about (effectively an if/else branch nobody ever cleans up).
- **Treating "manual approval" as sufficient governance for production.** Approval alone doesn't catch a system already in a bad state (e.g., ongoing high error rate) — pair it with an automated gate reading real telemetry.

---

## Practical Exercise ✅
1. Extend your CI pipeline to add `Deploy_Dev` and `Deploy_Prod` stages.
2. Create Environments named "Development" and "Production" in Azure DevOps.
3. Add a **manual approval gate** on the Production environment (add yourself as approver).
4. Trigger the pipeline, watch it auto-deploy to Dev, then manually approve the Production gate.

---

## Expert Interview Q&A

**Q: Blue-Green vs Canary — walk through the risk/rollback trade-off of each.**
Blue-Green deploys the full new version to an idle environment (staging slot), validates it, then does an instant, complete cutover — rollback is just swapping back, so it's fast and simple, but a bug that only shows up under real production traffic/load affects 100% of users the instant it's live. Canary shifts a small percentage of real production traffic to the new version first, observes real metrics, and only increases exposure if healthy — it catches production-only issues with a much smaller blast radius, but is more complex to implement correctly (needs real traffic-splitting infrastructure and automated health analysis, not just a sleep timer).

**Q: What's the difference between an "Approval" and a "Gate/Check" in Azure DevOps Environments, and why would you use both?**
An Approval requires a specific human to explicitly click approve/reject — it's a judgment and accountability checkpoint (good for change management/compliance). A Gate/Check is an automated, system-evaluated condition (e.g., no active Azure Monitor alert, work item state, business hours) that blocks deployment without human involvement. Using both means you get real-time automated safety (a gate blocking deploys during a detected bad state) plus deliberate human sign-off for accountability — either alone leaves a gap the other covers.

**Q: Why are feature flags often paired with progressive deployment strategies like canary?**
Feature flags decouple *code deployment* from *feature exposure* — you can deploy the new code to 100% of servers safely (it's inert/off) and then progressively turn the feature on for a percentage of *users* independently of infrastructure rollout. This means you can instantly disable a problematic feature via a flag flip (seconds) without needing a full redeploy/rollback (minutes), which is strictly faster for feature-level issues that aren't infrastructure-related.
