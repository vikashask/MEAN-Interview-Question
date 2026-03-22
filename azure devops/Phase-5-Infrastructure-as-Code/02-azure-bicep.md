# Azure Bicep - Microsoft's Native IaC Language

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

## Practical Exercise ✅
1. Install the Bicep VS Code extension.
2. Write a Bicep file that creates a Resource Group, VNet, and an Azure App Service.
3. Use `az deployment group what-if` to preview the changes.
4. Deploy the Bicep file with `az deployment group create`.
5. Add a second environment by using a **loop** (create the same app service for both `dev` and `qa`).
