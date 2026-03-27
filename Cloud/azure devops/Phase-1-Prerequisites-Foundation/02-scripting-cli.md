# Scripting & CLI for Azure DevOps

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

## Practical Exercise ✅
Write a bash script that:
1. Takes `environment` (dev/prod) as an argument.
2. Creates a Resource Group named `rg-<environment>`.
3. Creates a Storage Account with a unique name.
4. Prints the connection string at the end.

> **Tip**: Use `az storage account show-connection-string --name <name> --resource-group <rg>` to get the connection string.
