# Infrastructure as Code - Terraform for Azure

## Why IaC?
Instead of clicking around in the Azure Portal (which is error-prone and unrepeatable), you write code that declaratively describes what resources you want. Terraform then creates, updates, or destroys resources to match that desired state.

## Terraform Core Concepts

```
Provider      --> Tells Terraform WHICH cloud to talk to (Azure, AWS, GCP)
Resource      --> A thing to CREATE (VM, VNet, App Service)
Data Source   --> READ existing resources you didn't create with Terraform
Variable      --> Input parameters
Output        --> Values to expose after apply
Module        --> A reusable group of resources
State File    --> Terraform's memory of what it has deployed (.tfstate)
```

---

## Core Workflow

```bash
terraform init    # Download providers, initialize backend
terraform fmt     # Auto-format .tf files
terraform validate # Check for syntax errors
terraform plan    # Preview changes (DRY RUN - shows what will change)
terraform apply   # Apply the changes
terraform destroy # Delete everything Terraform manages
```

---

## Full Working Example: Azure Web App + Database

### File Structure
```
terraform/
 ├── main.tf           (providers and resources)
 ├── variables.tf      (input variable declarations)
 ├── outputs.tf        (output values)
 ├── terraform.tfvars  (your variable values - gitignore this!)
 └── backend.tf        (remote state config)
```

### `backend.tf` - Remote State in Azure Blob Storage
```hcl
# Store .tfstate file in Azure Blob Storage (NOT locally)
terraform {
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "stterraformstate12345"
    container_name       = "tfstate"
    key                  = "myapp.prod.tfstate"
  }
}
```

### `variables.tf`
```hcl
variable "environment" {
  type        = string
  description = "Deployment environment: dev, staging, prod"
}

variable "location" {
  type    = string
  default = "East US"
}

variable "app_name" {
  type = string
}

variable "sql_admin_password" {
  type      = string
  sensitive = true  # Never shown in output or logs
}
```

### `main.tf`
```hcl
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Naming convention: lowercase, no spaces
locals {
  resource_prefix = "${var.app_name}-${var.environment}"
}

# Resource Group
resource "azurerm_resource_group" "main" {
  name     = "rg-${local.resource_prefix}"
  location = var.location
}

# App Service Plan (hosting plan for the web app)
resource "azurerm_service_plan" "main" {
  name                = "plan-${local.resource_prefix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  os_type             = "Linux"
  sku_name            = "B1"  # Basic tier
}

# Azure Web App (Linux)
resource "azurerm_linux_web_app" "main" {
  name                = "app-${local.resource_prefix}"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    application_stack {
      node_version = "20-lts"
    }
    always_on = false  # Set true for production
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE" = "false"
    "ENVIRONMENT"                          = var.environment
    "DATABASE_URL"                         = azurerm_mssql_server.main.fully_qualified_domain_name
  }

  identity {
    type = "SystemAssigned"  # Enable Managed Identity
  }
}

# SQL Server
resource "azurerm_mssql_server" "main" {
  name                         = "sql-${local.resource_prefix}"
  resource_group_name          = azurerm_resource_group.main.name
  location                     = azurerm_resource_group.main.location
  version                      = "12.0"
  administrator_login          = "sqladmin"
  administrator_login_password = var.sql_admin_password
}

# SQL Database
resource "azurerm_mssql_database" "main" {
  name      = "db-${local.resource_prefix}"
  server_id = azurerm_mssql_server.main.id
  sku_name  = "Basic"
}
```

### `outputs.tf`
```hcl
output "web_app_url" {
  value       = "https://${azurerm_linux_web_app.main.default_hostname}"
  description = "The URL of the deployed web application"
}

output "web_app_outbound_ips" {
  value = azurerm_linux_web_app.main.outbound_ip_addresses
}

output "sql_server_fqdn" {
  value = azurerm_mssql_server.main.fully_qualified_domain_name
}
```

### `terraform.tfvars` (DO NOT COMMIT - add to `.gitignore`)
```hcl
environment        = "dev"
location           = "East US"
app_name           = "myapp"
sql_admin_password = "SuperSecret123!"
```

---

## Running Terraform in an Azure Pipeline

```yaml
# azure-pipelines-terraform.yml
variables:
  TF_WORKING_DIR: '$(System.DefaultWorkingDirectory)/terraform'

stages:
  - stage: TerraformPlan
    displayName: 'Terraform Plan'
    jobs:
      - job: Plan
        pool:
          vmImage: 'ubuntu-latest'
        steps:
          - task: TerraformInstaller@1
            inputs:
              terraformVersion: 'latest'

          - task: TerraformTaskV4@4
            displayName: 'Terraform Init'
            inputs:
              provider: 'azurerm'
              command: 'init'
              workingDirectory: $(TF_WORKING_DIR)
              backendServiceArm: 'AzureServiceConnection'
              backendAzureRmResourceGroupName: 'rg-terraform-state'
              backendAzureRmStorageAccountName: 'stterraformstate12345'
              backendAzureRmContainerName: 'tfstate'
              backendAzureRmKey: 'myapp.prod.tfstate'

          - task: TerraformTaskV4@4
            displayName: 'Terraform Plan'
            inputs:
              provider: 'azurerm'
              command: 'plan'
              workingDirectory: $(TF_WORKING_DIR)
              environmentServiceNameAzureRM: 'AzureServiceConnection'
              commandOptions: '-var="environment=prod" -out=tfplan'

  - stage: TerraformApply
    dependsOn: TerraformPlan
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    jobs:
      - deployment: Apply
        environment: 'Production'  # Requires manual approval
        pool:
          vmImage: 'ubuntu-latest'
        strategy:
          runOnce:
            deploy:
              steps:
                - task: TerraformTaskV4@4
                  displayName: 'Terraform Apply'
                  inputs:
                    provider: 'azurerm'
                    command: 'apply'
                    workingDirectory: $(TF_WORKING_DIR)
                    environmentServiceNameAzureRM: 'AzureServiceConnection'
                    commandOptions: 'tfplan'
```

---

## Practical Exercise ✅
1. Set up a storage account in Azure to hold Terraform state (do this manually once).
2. Write Terraform to create a Resource Group and an App Service Plan.
3. Run `terraform plan` locally - examine the output.
4. Run `terraform apply` to create the resources. Verify them in the Azure Portal.
5. Run `terraform destroy` to clean up.
6. *Advanced:* Move the Terraform into an Azure Pipeline with a `Plan` + `Apply` stage.
