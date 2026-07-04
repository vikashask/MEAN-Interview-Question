# Infrastructure as Code - Terraform for Azure

> **Expert framing:** Anyone can write `resource` blocks. The expert-level skill is state management discipline — understanding *why* state locking exists, what happens when two people `apply` at once without it, how to safely handle drift, and when to reach for `import`/`moved` blocks instead of destroying and recreating a resource that shouldn't go down.

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

**Expert insight — why remote state + locking is non-negotiable in a team:**
- Local `.tfstate` means only one person's laptop has "the truth" about what's deployed — the moment a second person runs `terraform apply`, you get divergent, corrupted understandings of reality. Remote state (Azure Blob here) gives everyone the same source of truth.
- The `azurerm` backend uses **blob leases** for state locking automatically — if someone else is mid-`apply`, your `apply` will block/fail with a lock error instead of racing and corrupting the state file. Never manually delete a lock unless you're certain the other operation truly died (e.g., a crashed CI agent) — force-unlocking during a live apply can corrupt state.
- `terraform.tfstate` contains **all resource attributes in plain text, including secrets** passed as resource arguments (e.g., a DB admin password set via a resource property) — treat the state file itself as sensitive, enable encryption at rest on the storage account, and restrict access via RBAC, not just "it's in a private container."

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

## Common Pitfalls & Expert Tips

- **Manually changing a resource in the Azure Portal that Terraform manages.** This is "drift" — Terraform's state no longer matches reality. The next `plan` will show Terraform wanting to "fix" it back (potentially undoing an emergency manual fix) or, worse, wanting to recreate a resource that can't be updated in place. Always run `terraform plan` after any manual out-of-band change to see and reconcile drift deliberately.
- **Destroying and recreating a resource that has real data/uptime requirements** because a property changed that Terraform can't update in place (many properties force `ForceNew`/replacement). Know which resource attributes are mutable vs force-replace *before* changing them on a production database or similar.
- **Never running `terraform apply` in CI with the exact same plan reviewed by a human.** Best practice: `plan` produces a saved plan file (`-out=tfplan`), a human/approval reviews the *plan output*, then `apply` consumes that exact saved plan file — not a fresh plan — so what gets applied is guaranteed to be what was reviewed.
- **Not using `terraform import` for resources created outside Terraform.** Instead of deleting a manually-created resource and letting Terraform recreate it (causing downtime), `terraform import` brings an existing resource under Terraform management without touching it.
- **Committing `terraform.tfvars` with real secrets to git.** Sensitive variables should come from a secure source (Key Vault-backed pipeline variable group, environment variables) at apply time, never committed — even in a "private" repo.
- **Ignoring the `sensitive = true` flag's actual limits.** It hides a value from CLI *output*, but the value is still stored in plain text in the state file — `sensitive` is not encryption, it's just output redaction.

---

## Practical Exercise ✅
1. Set up a storage account in Azure to hold Terraform state (do this manually once).
2. Write Terraform to create a Resource Group and an App Service Plan.
3. Run `terraform plan` locally - examine the output.
4. Run `terraform apply` to create the resources. Verify them in the Azure Portal.
5. Run `terraform destroy` to clean up.
6. *Advanced:* Move the Terraform into an Azure Pipeline with a `Plan` + `Apply` stage.

---

## Expert Interview Q&A

**Q: Two engineers run `terraform apply` on the same state at the same time without remote state locking. What happens, and how does remote state prevent it?**
Without locking, both processes read the state, compute a plan, and write back independently — the second write can overwrite the first's changes or corrupt the state file, leading to Terraform's understanding of infrastructure diverging from reality (and potentially double-creating or losing track of resources). The `azurerm` remote backend uses blob leases to acquire an exclusive lock during any state-modifying operation; the second `apply` blocks or errors immediately instead of racing.

**Q: What is "drift" in Terraform, and how do you detect and reconcile it?**
Drift is when real infrastructure no longer matches what's recorded in Terraform's state — usually from manual changes made outside Terraform (Portal, CLI, another tool). Run `terraform plan` to detect it: it shows what Terraform would change to bring reality back in line with the `.tf` code. You then decide deliberately — either let Terraform revert the manual change, or update the `.tf` code to match the new desired reality and re-`apply`, or `terraform import`/`terraform state` commands to reconcile without destructive changes.

**Q: Why should CI pipelines `apply` a saved plan file rather than re-running `plan` right before `apply`?**
Time passes between plan review/approval and the actual apply — if you re-run `plan` at apply time, the underlying infrastructure or variables could have changed in between, so what actually gets applied might differ from what a human approved. Saving the plan (`-out=tfplan`) and applying that exact file (`terraform apply tfplan`) guarantees the approved plan is exactly what executes — critical for change control in regulated environments.

**Q: Why is `sensitive = true` on a Terraform variable/output not sufficient to protect a secret?**
It only suppresses the value from being printed in CLI output/logs — the actual value is still stored in plaintext inside the `.tfstate` file. True protection requires securing the state file itself (encryption at rest, strict RBAC on the storage account/container) and, where possible, avoiding storing genuinely sensitive long-lived secrets in Terraform state at all (e.g., generate them via Key Vault and reference by ID rather than passing raw secret values as resource arguments).
