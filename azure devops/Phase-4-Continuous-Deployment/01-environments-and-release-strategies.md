# Continuous Deployment (CD) - Environments & Release Strategies

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

## Practical Exercise ✅
1. Extend your CI pipeline to add `Deploy_Dev` and `Deploy_Prod` stages.
2. Create Environments named "Development" and "Production" in Azure DevOps.
3. Add a **manual approval gate** on the Production environment (add yourself as approver).
4. Trigger the pipeline, watch it auto-deploy to Dev, then manually approve the Production gate.
