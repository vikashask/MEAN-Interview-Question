# Cloud Computing Fundamentals (Azure Focus)

> **Expert framing:** You already know the basics (IaaS/PaaS/SaaS, resource groups). What separates a junior from an expert here isn't knowing the definitions — it's knowing *why* the resource hierarchy exists (blast-radius control, billing isolation, policy inheritance) and being able to design a subscription/resource-group layout that scales to a real organization instead of one flat dumping ground.

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

**Expert insight — why each layer exists, not just what it's called:**
- **Management Groups** exist so a Policy or RBAC assignment made *once* at the top cascades down to every subscription underneath — this is how large orgs enforce "no public IPs allowed" or "must tag with CostCenter" across hundreds of subscriptions without touching each one.
- **Subscriptions** are the hard billing + quota boundary (VM core quotas, for example, are per-subscription) — this is why orgs split Dev/Test/Prod into separate subscriptions, not just separate resource groups: it isolates both cost *and* blast radius (a runaway Dev workload can't eat Prod's quota).
- **Resource Groups** should be scoped around **lifecycle**, not just "type of thing" — the expert rule of thumb is "resources that get deployed and deleted together belong in the same RG." A common junior mistake is one giant RG for the whole subscription, which makes targeted teardown (and blast-radius containment) impossible.
- Deleting a Resource Group deletes *everything* inside it, non-recoverably (unless soft-delete is separately enabled per-resource-type) — always know what's living in an RG before you `az group delete`.

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

## Common Pitfalls & Expert Tips

- **Flat resource groups.** Dumping every resource for an entire org into one RG makes RBAC scoping, cost tracking, and safe teardown nearly impossible. Scope RGs by lifecycle + team ownership.
- **Ignoring Availability Zones vs Regions.** A Region can go down; an AZ failure inside a region is far more common. Production workloads should be **zone-redundant**, not just "deployed in East US" — this is a very common gap between people who've passed AZ-900 and people who've actually run production.
- **Confusing "high availability" with "disaster recovery."** HA = surviving a failure with no/minimal downtime (Multi-AZ, load balancing). DR = recovering after a full regional/catastrophic loss (backup + restore to another region, has an RTO/RPO). Interviewers frequently probe this distinction directly.
- **Not understanding the Shared Responsibility Model boundary shifts by service model.** In IaaS, you patch the OS. In PaaS, Microsoft does. Security incidents often trace back to a team assuming "Azure handles that" when the service model actually put it on them (e.g., OS patching on an IaaS VM).
- **CapEx vs OpEx isn't just a finance buzzword** — it explains *why* cloud exists commercially (no upfront hardware purchase, pay for what you use) and is a favorite AZ-900/interview trick question because people conflate it with "cloud is always cheaper" (it isn't, always — at steady massive scale, owned hardware can be cheaper; the value is agility, not guaranteed cost savings).

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

---

## Expert Interview Q&A

**Q: Why would an organization use multiple subscriptions instead of just multiple resource groups?**
Subscriptions are the hard boundary for billing, quotas (e.g. vCPU core limits), and Azure Policy/RBAC inheritance from Management Groups. Resource groups only organize resources *within* a subscription — they don't isolate quota or billing. Multi-subscription design (e.g. one per environment or business unit) contains blast radius and cost far more strongly than resource groups alone.

**Q: What's the actual difference between Fault Tolerance and Disaster Recovery?**
Fault tolerance is the system's ability to keep running *through* a failure with no perceptible downtime (e.g., a VM in an Availability Set/Zone dies, traffic just shifts to a healthy instance). Disaster recovery is the *planned process* to restore service after a major outage (region loss, major corruption) — it has defined RTO (how fast) and RPO (how much data loss is acceptable) targets and usually involves failing over to a secondary region.

**Q: How do Management Groups, Policies, and RBAC interact?**
Management Groups let you assign Azure Policy and RBAC roles at a level above subscriptions; both inherit downward through the hierarchy (Management Group → Subscription → Resource Group → Resource). A Policy denying public IP creation assigned at the Management Group level applies to every subscription beneath it automatically — this is how enterprises enforce guardrails at scale without per-subscription configuration.

**Q: When would you choose PaaS over IaaS for a new workload?**
When you don't need OS-level control and want to offload patching/scaling/HA to the platform — faster time to market, less operational burden. IaaS is chosen when you need custom OS configuration, licensing constraints, or software that assumes full machine control (e.g., certain legacy or specialized workloads).
