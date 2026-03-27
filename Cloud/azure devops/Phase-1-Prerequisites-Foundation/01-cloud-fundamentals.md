# Cloud Computing Fundamentals (Azure Focus)

## What is Cloud Computing?
Cloud computing is the delivery of computing services (servers, storage, databases, networking, software) over the internet ("the cloud") to offer faster innovation, flexible resources, and economies of scale.

---

## Service Models

| Model | Who Manages | Example |
|-------|-------------|---------|
| **IaaS** (Infrastructure as a Service) | You manage OS, runtime, data | Azure VMs, Azure VNet |
| **PaaS** (Platform as a Service) | Provider manages OS & runtime; you manage app & data | Azure App Service, Azure SQL |
| **SaaS** (Software as a Service) | Provider manages everything | Azure DevOps, Microsoft 365 |

---

## Azure Resource Hierarchy

```
Tenant (Azure AD / Entra ID)
 └── Management Groups (optional, for multi-subscription governance)
      └── Subscriptions (billing boundary: e.g. "Dev", "Prod")
           └── Resource Groups (logical container for related resources)
                └── Resources (VM, Storage Account, App Service, etc.)
```

### Resource Groups via Azure CLI
```bash
# Login to Azure
az login

# List all subscriptions
az account list --output table

# Set active subscription
az account set --subscription "Your-Subscription-Name"

# Create a Resource Group
az group create \
  --name rg-devops-learning \
  --location eastus

# List Resource Groups
az group list --output table

# Delete a Resource Group (and ALL resources inside it)
az group delete --name rg-devops-learning --yes --no-wait
```

---

## Core Azure Services to Know

### Compute
```bash
# Create a Linux VM
az vm create \
  --resource-group rg-devops-learning \
  --name vm-myserver \
  --image Ubuntu2204 \
  --admin-username azureuser \
  --generate-ssh-keys \
  --size Standard_B1s

# Open port 22 (SSH) for access
az vm open-port --port 22 --resource-group rg-devops-learning --name vm-myserver

# SSH into the VM
ssh azureuser@<VM_PUBLIC_IP>

# Deallocate (stop billing for compute but keep disk)
az vm deallocate --resource-group rg-devops-learning --name vm-myserver

# Delete the VM
az vm delete --resource-group rg-devops-learning --name vm-myserver --yes
```

### Storage (Blob)
```bash
# Create a Storage Account
az storage account create \
  --name mystoragedevopslearn \
  --resource-group rg-devops-learning \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2

# Create a Blob Container
az storage container create \
  --name pipeline-artifacts \
  --account-name mystoragedevopslearn \
  --public-access off

# Upload a file to Blob Storage
az storage blob upload \
  --account-name mystoragedevopslearn \
  --container-name pipeline-artifacts \
  --name my-build.zip \
  --file /path/to/local/file.zip

# List blobs in a container
az storage blob list \
  --account-name mystoragedevopslearn \
  --container-name pipeline-artifacts \
  --output table
```

### Networking (VNet Basics)
```bash
# Create a Virtual Network (VNet) with a subnet
az network vnet create \
  --resource-group rg-devops-learning \
  --name vnet-main \
  --address-prefix 10.0.0.0/16 \
  --subnet-name subnet-default \
  --subnet-prefix 10.0.1.0/24

# Create a Network Security Group (NSG)
az network nsg create \
  --resource-group rg-devops-learning \
  --name nsg-devops

# Add a rule to allow SSH inbound
az network nsg rule create \
  --resource-group rg-devops-learning \
  --nsg-name nsg-devops \
  --name allow-ssh \
  --priority 1000 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --destination-port-range 22
```

---

## Practical Exercise ✅
1. Create a Resource Group `rg-devops-lab`.
2. Create a VNet and a Subnet inside it.
3. Deploy an Ubuntu VM into that VNet/Subnet.
4. SSH into the VM and run `echo "Hello from Azure!"`.
5. Delete the Resource Group to clean up everything in one command.

---

## AZ-900 Key Topics to Review
- Shared Responsibility Model
- CapEx vs OpEx (cloud financial model)
- High Availability, Fault Tolerance, Disaster Recovery
- Azure Availability Zones and Regions
