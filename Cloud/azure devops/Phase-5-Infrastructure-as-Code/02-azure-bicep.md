# Azure Bicep - Microsoft's Native IaC Language

> **Expert framing:** The AZ-400 exam and real interviews love to ask "why would you use Bicep over Terraform (or vice versa)" — an expert answer isn't "Bicep is simpler," it's about state management model (ARM as the implicit state store vs Terraform's explicit `.tfstate`), multi-cloud need, and organizational tooling maturity. Also know `what-if` cold — it's Bicep/ARM's answer to `terraform plan`, and interviewers check whether you actually use it before deploying.

## What is Bicep?
Bicep is a domain-specific language (DSL) that compiles into ARM (Azure Resource Manager) JSON templates. It's simpler, more readable, and 100% Azure-native.

```
Bicep code (.bicep)  →  ARM Template (JSON)  →  Azure Resources
```

---

## Bicep vs Terraform
| Feature | Bicep | Terraform |
|---------|-------|-----------|
| Cloud Support | Azure only | Multi-cloud (Azure, AWS, GCP) |
| Maintained by | Microsoft | HashiCorp |
| State Management | None (ARM handles state) | Requires `.tfstate` file |
| Learning Curve | Easier for Azure-first teams | More complex but more powerful |
| Best For | Azure-only shops | Multi-cloud or complex IaC |

---

## Bicep Core Syntax

### Hello World - Resource Group Level Deployment
```bicep
// main.bicep

// Parameters (like Terraform variables)
param environment string = 'dev'
param location string = resourceGroup().location
param appName string

// Variables (computed values)
var resourcePrefix = '${appName}-${environment}'

// Resource: Storage Account
resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: 'st${appName}${environment}001'  // Must be globally unique, lowercase
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
  }
}

// Resource: App Service Plan
resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'plan-${resourcePrefix}'
  location: location
  sku: {
    name: 'B1'
    tier: 'Basic'
  }
  properties: {
    reserved: true  // Required for Linux
  }
  kind: 'linux'
}

// Resource: Web App (depends on App Service Plan)
resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: 'app-${resourcePrefix}'
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    serverFarmId: appServicePlan.id   // Reference to another resource
    httpsOnly: true
    siteConfig: {
      linuxFxVersion: 'NODE|20-lts'
      appSettings: [
        {
          name: 'ENVIRONMENT'
          value: environment
        }
        {
          name: 'STORAGE_ACCOUNT'
          value: storageAccount.name
        }
      ]
    }
  }
}

// Outputs
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output webAppPrincipalId string = webApp.identity.principalId
```

---

## Deploying Bicep

```bash
# Compile Bicep to ARM JSON (to inspect)
az bicep build --file main.bicep

# Deploy to a Resource Group
az deployment group create \
  --resource-group rg-myapp-dev \
  --template-file main.bicep \
  --parameters environment=dev appName=myapp

# Preview before deploying (like terraform plan)
az deployment group what-if \
  --resource-group rg-myapp-dev \
  --template-file main.bicep \
  --parameters environment=dev appName=myapp
```

**Expert insight — Bicep/ARM has no separate state file, and that changes your mental model:**
Terraform tracks "what it deployed" in an explicit `.tfstate` file that it compares against on every plan. Bicep/ARM has no equivalent file — ARM re-derives the current state by querying Azure directly at deployment time and diffing against the template. This means there's no "state drift from a stale state file" class of bug that Terraform has, but it also means `what-if` is your *only* pre-deployment safety check — always run it before `create`, especially with `--mode Complete` (which deletes any resource in the resource group not defined in the template — a common and dangerous surprise for people used to Terraform's more surgical per-resource tracking).

---

## Bicep Modules (Reusability)

```bicep
// modules/webApp.bicep
param appName string
param location string
param appServicePlanId string

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: appName
  location: location
  properties: {
    serverFarmId: appServicePlanId
    httpsOnly: true
  }
}

output webAppUrl string = webApp.properties.defaultHostName
```

```bicep
// main.bicep - Consuming the module
module webAppModule './modules/webApp.bicep' = {
  name: 'deployWebApp'
  params: {
    appName: 'app-myapp-dev'
    location: location
    appServicePlanId: appServicePlan.id
  }
}

// Access module output
output siteUrl string = webAppModule.outputs.webAppUrl
```

---

## Bicep Loops & Conditions

```bicep
param environments array = ['dev', 'qa', 'prod']

// Loop: Create one storage account per environment
resource storageAccounts 'Microsoft.Storage/storageAccounts@2022-09-01' = [for env in environments: {
  name: 'stmyapp${env}001'
  location: resourceGroup().location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}]

// Condition: Only create VPN gateway in production
param isProd bool = false

resource vpnGateway 'Microsoft.Network/virtualNetworkGateways@2022-07-01' = if (isProd) {
  name: 'vpn-myapp-prod'
  location: resourceGroup().location
  // ... properties
}
```

---

## Bicep in an Azure Pipeline

```yaml
# Deploy infrastructure with Bicep in Azure Pipelines
- stage: DeployInfra
  jobs:
    - job: BicepDeploy
      pool:
        vmImage: 'ubuntu-latest'
      steps:
        - task: AzureCLI@2
          displayName: 'Deploy Bicep Template'
          inputs:
            azureSubscription: 'AzureServiceConnection'
            scriptType: 'bash'
            scriptLocation: 'inlineScript'
            inlineScript: |
              az deployment group create \
                --resource-group rg-myapp-$(environment) \
                --template-file $(System.DefaultWorkingDirectory)/infra/main.bicep \
                --parameters environment=$(environment) appName=myapp \
                --mode Incremental
```

---

## Common Pitfalls & Expert Tips

- **Using `--mode Complete` without fully understanding it.** Complete mode deletes any resource in the target resource group that isn't defined in the template — a huge, often-unintended blast radius if the RG contains anything not managed by this particular Bicep file. Incremental mode (the default) only adds/updates what's in the template and leaves everything else alone — know which one you're using before every deploy.
- **Skipping `what-if` "because it's just a small change."** Small changes are exactly where `what-if` catches unexpected replacements (e.g., changing a property that forces resource recreation, causing unplanned downtime) before they happen live.
- **Hardcoding resource API versions that go stale.** Bicep resource declarations pin an API version (`@2022-09-01`); an outdated pinned version can miss newer properties/features. Periodically check for and update to current stable API versions.
- **Not using modules for anything reused more than once.** Copy-pasted resource blocks across multiple Bicep files drift out of sync over time — modules keep a single source of truth, same as Terraform modules.
- **Confusing Bicep's lack of a state file with "no risk of drift."** ARM re-derives state at deploy time, but manual out-of-band changes to a resource are still overwritten on the next `deploy` (or left alone, depending on what properties changed) — the absence of a state *file* doesn't mean drift-related surprises can't happen, just that they manifest differently than in Terraform.

---

## Practical Exercise ✅
1. Install the Bicep VS Code extension.
2. Write a Bicep file that creates a Resource Group, VNet, and an Azure App Service.
3. Use `az deployment group what-if` to preview the changes.
4. Deploy the Bicep file with `az deployment group create`.
5. Add a second environment by using a **loop** (create the same app service for both `dev` and `qa`).

---

## Expert Interview Q&A

**Q: Bicep vs Terraform — how would you actually decide between them for a new Azure-only project?**
Bicep is a strong default for Azure-only shops: no separate state file/backend to manage, first-party Microsoft support with day-one support for new Azure resource types/API versions, and a gentler learning curve tied directly to ARM concepts most Azure admins already know. Terraform wins when the organization is multi-cloud (or might become so), needs its large third-party provider ecosystem (beyond just Azure), or already has significant Terraform tooling/expertise investment (state backends, CI patterns, team knowledge) that would be costly to duplicate for a second IaC tool.

**Q: What does `--mode Complete` do differently from the default `Incremental` mode, and why is it risky?**
Incremental mode only creates/updates resources defined in the template, leaving unrelated resources in the resource group untouched. Complete mode makes the resource group's actual contents match the template *exactly* — meaning any resource present in the RG but not defined in the template gets deleted. It's risky because a resource group commonly contains things created by other automation, another team, or manually — Complete mode will delete them without further warning if they're not in your template.

**Q: How does ARM/Bicep know what's currently deployed, if there's no `.tfstate`-equivalent file?**
ARM queries the live Azure Resource Manager API for the resource group's current resource state at deployment time and computes the diff against the template on the fly — deployment history in the Portal is a record of past deployments, not a state cache used for diffing. This means there's no local/remote state file to lock, corrupt, or go stale, but it also means `what-if` (which performs this same live diff) is your only pre-flight check — there's no separate "always available" plan artifact to review offline the way a saved Terraform plan file works.
