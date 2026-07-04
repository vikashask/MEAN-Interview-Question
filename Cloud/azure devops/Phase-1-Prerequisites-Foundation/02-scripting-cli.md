# Scripting & CLI for Azure DevOps

> **Expert framing:** Anyone can copy-paste `az` commands. What makes a DevOps engineer valuable is writing scripts that are **idempotent** (safe to re-run), **fail loudly** (`set -e`, proper exit codes) instead of silently continuing after an error, and **parameterized** so the same script runs unchanged across dev/staging/prod. Pipeline reliability lives or dies on these habits.

## Linux & Bash Essentials

### File System Navigation
```bash
# Essential commands
pwd           # print working directory
ls -la        # list all files with details
cd /etc       # change directory
mkdir -p ops/scripts  # create nested directories
cp -r src/ dest/      # copy recursively
mv old.txt new.txt    # move/rename
rm -rf dir/           # remove recursively (use carefully!)
cat file.txt          # view file contents
less file.txt         # page through file
grep -r "password" .  # search text in all files
find / -name "*.log"  # find files by name
```

### File Permissions
```bash
# Format: [owner][group][others]
# r=4, w=2, x=1
chmod 755 deploy.sh   # rwxr-xr-x (owner full, others read+exec)
chmod +x deploy.sh    # just make executable
chown azureuser:azureuser deploy.sh  # change owner

# SSH Key Generation (password-less auth)
ssh-keygen -t rsa -b 4096 -C "devops@mycompany.com"
# This creates ~/.ssh/id_rsa (private) and ~/.ssh/id_rsa.pub (public)

# Copy public key to remote server
ssh-copy-id azureuser@<VM_IP>
```

### Writing Bash Scripts
```bash
#!/bin/bash
# ============================================
# Azure Resource Setup Script
# Usage: ./setup-azure.sh <env> <region>
# ============================================

set -e  # Exit immediately if a command fails
set -o pipefail  # Fail on pipe errors

ENV=$1      # First argument: "dev", "prod"
REGION=$2   # Second argument: "eastus"

if [ -z "$ENV" ] || [ -z "$REGION" ]; then
  echo "Usage: $0 <environment> <region>"
  exit 1
fi

RG_NAME="rg-myapp-${ENV}"
STORAGE_NAME="stmyapp${ENV}$(date +%s)" # Unique name with timestamp

echo "----> Creating Resource Group: $RG_NAME"
az group create --name "$RG_NAME" --location "$REGION"
# Expert note: `az group create` is naturally idempotent (safe to re-run — it
# no-ops if the group already exists with the same properties). But most other
# `az ... create` commands are NOT idempotent by default; re-running them can
# error ("already exists") or silently create a duplicate. Always check the
# command's docs or add an explicit existence check before create in scripts
# meant to be re-run (e.g. `az group exists --name "$RG_NAME"`).

echo "----> Creating Storage Account: $STORAGE_NAME"
az storage account create \
  --name "$STORAGE_NAME" \
  --resource-group "$RG_NAME" \
  --location "$REGION" \
  --sku Standard_LRS

echo "✅ All resources created successfully!"
```

---

## Azure CLI (`az`) Deep Dive

### Installation & Auth
```bash
# Install Azure CLI on Linux/Mac
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash

# Authenticate
az login  # Opens browser for interactive login
az login --service-principal -u <appId> -p <password> --tenant <tenantId>  # For automation

# Show current logged-in account
az account show

# Query output using JMESPath
az vm list --query "[].{Name:name, OS:storageProfile.osDisk.osType}" --output table
```

### Useful CLI Patterns
```bash
# Use --query to filter JSON output
az resource list \
  --resource-group rg-devops \
  --query "[?type=='Microsoft.Compute/virtualMachines'].name" \
  --output tsv

# Exporting to a variable
RG_ID=$(az group show --name rg-devops --query id --output tsv)
echo "Resource Group ID: $RG_ID"
```

---

## PowerShell (Az Module) Basics

### Setup and Authentication
```powershell
# Install the Az module (run once)
Install-Module -Name Az -Repository PSGallery -Force

# Login
Connect-AzAccount

# Select a subscription
Set-AzContext -SubscriptionName "My-Dev-Subscription"
```

### Core Resource Management Commands
```powershell
# Create a Resource Group
New-AzResourceGroup -Name "rg-devops" -Location "EastUS"

# Get all resources in a group
Get-AzResource -ResourceGroupName "rg-devops"

# Create a Storage Account
New-AzStorageAccount `
  -ResourceGroupName "rg-devops" `
  -Name "stdevopsdata" `
  -Location "EastUS" `
  -SkuName "Standard_LRS" `
  -Kind "StorageV2"

# Delete a Resource Group
Remove-AzResourceGroup -Name "rg-devops" -Force
```

### PowerShell Scripting Patterns
```powershell
# Loop through resources and take action
$vms = Get-AzVM -ResourceGroupName "rg-devops"
foreach ($vm in $vms) {
    Write-Host "Found VM: $($vm.Name) in location $($vm.Location)"
    if ($vm.PowerState -eq "VM running") {
        Stop-AzVM -ResourceGroupName "rg-devops" -Name $vm.Name -Force
        Write-Host "  -> Stopped $($vm.Name)"
    }
}

# Using Param blocks for reusable scripts
param(
    [Parameter(Mandatory=$true)]
    [string]$Environment,

    [Parameter(Mandatory=$false)]
    [string]$Region = "eastus"
)

$resourceGroupName = "rg-myapp-$Environment"
Write-Host "Creating resources for: $resourceGroupName in $Region"
```

---

## Common Pitfalls & Expert Tips

- **Forgetting `set -e` / `set -o pipefail`.** Without them, a failed command mid-script is silently ignored and the script barrels on with bad state — one of the most common causes of "the pipeline said it passed but nothing actually deployed."
- **Not quoting variables** (`$VAR` instead of `"$VAR"`). Breaks on any value containing spaces or special characters — a classic source of flaky pipeline scripts that "worked on my machine."
- **Using `az` interactively-formatted output (`--output table`) inside scripts.** Table output is for humans; scripts should use `--output tsv` or `--output json` + `jq`/`--query` so parsing doesn't break if column widths change.
- **Storing secrets as plain arguments on the command line.** Command-line args are visible in shell history and process lists (`ps aux`). Prefer piping secrets via stdin, environment variables scoped to the process, or fetching them from Key Vault at runtime.
- **Service Principal auth in automation vs `az login` interactively.** Interactive login is for a human at a terminal; pipelines must use `az login --service-principal` (or, better, Workload Identity Federation / OIDC — no stored secret at all) — mixing these up is a common early mistake.
- **PowerShell `Az` module vs classic `AzureRM` module.** `AzureRM` is deprecated — if you see it in a script or exam question, know it's legacy; all new work uses the `Az` module.

---

## Practical Exercise ✅
Write a bash script that:
1. Takes `environment` (dev/prod) as an argument.
2. Creates a Resource Group named `rg-<environment>`.
3. Creates a Storage Account with a unique name.
4. Prints the connection string at the end.

> **Tip**: Use `az storage account show-connection-string --name <name> --resource-group <rg>` to get the connection string.

---

## Expert Interview Q&A

**Q: Why is idempotency important in infrastructure automation scripts?**
Pipelines re-run — due to retries, re-triggers, or manual re-runs after a partial failure. A non-idempotent script (e.g., blindly calling `create` without checking existence) will fail or duplicate resources on a second run, turning a simple retry into a manual cleanup job. Idempotent scripts can be safely re-executed to reach the same end state regardless of the starting state.

**Q: How should secrets be passed into a script running inside a pipeline — command-line args, env vars, or a secrets store?**
Never as raw command-line arguments (visible in shell history/process list). Prefer resolving secrets at runtime from Azure Key Vault (via Managed Identity or Workload Identity Federation) into short-lived environment variables scoped to that pipeline run — this avoids persisting the secret anywhere and keeps an audit trail of who/what accessed it.

**Q: Service Principal vs Managed Identity vs Workload Identity Federation for pipeline authentication — what's the expert's default choice today?**
Workload Identity Federation (OIDC) is the current best practice for Azure DevOps → Azure authentication — no stored secret/certificate at all; Azure DevOps presents a short-lived OIDC token that Azure AD trusts based on a federated credential configuration. Service Principals with client secrets are the older approach and still common, but they require secret rotation and are a bigger attack surface. Managed Identities are for *Azure resources* (VMs, App Services) to authenticate to other Azure services — not directly usable from Azure DevOps pipelines themselves.

**Q: What's the risk of not using `--query`/JMESPath and instead parsing `az` table output with `grep`/`awk`?**
Table output is meant for human readability and its formatting (column widths, header text) is not a stable contract — Azure CLI updates can silently break brittle text-parsing. `--query` with JMESPath (or `--output json` piped to `jq`) parses the actual structured data, which is stable across CLI versions.
