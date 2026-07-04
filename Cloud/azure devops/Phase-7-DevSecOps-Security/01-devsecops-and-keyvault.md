# DevSecOps - Security in the Pipeline

> **Expert framing:** "Shift left" is the buzzword; the expert skill is knowing exactly *which* identity type (Service Principal, System-Assigned Managed Identity, User-Assigned Managed Identity, Workload Identity Federation) is correct for a given scenario, and why. This is one of the most heavily tested AZ-400 areas and one of the most common real-world misconfiguration sources — get it wrong and you either have a security hole (over-broad access) or a brittle pipeline (expired secrets breaking deploys at 2am).

## The DevSecOps Mindset
Traditional security: Security checks at the END before release.
DevSecOps: Security is embedded at EVERY stage of the pipeline.

```
Code →  SCM  →  Build  →  Test  →  Deploy  →  Monitor
  ↑       ↑       ↑        ↑         ↑           ↑
Secret  Branch  SAST/  Integration  DAST    Runtime
 Scan  Policy   Scan    Sec Test     Scan    Alerts
```

---

## 1. Secrets & Azure Key Vault

### Why Key Vault?
Never store passwords, connection strings, or certificate private keys in:
- Code / `appsettings.json`
- Environment variables (in the portal)
- Azure DevOps pipeline variables (unencrypted)

Store them in **Azure Key Vault** and fetch them at runtime or pipeline time.

### Creating and Using Key Vault
```bash
# Create a Key Vault
az keyvault create \
  --name kv-myapp-prod \
  --resource-group rg-production \
  --location eastus \
  --enable-soft-delete true \  # Protect against accidental deletion
  --retention-days 90

# Add a secret
az keyvault secret set \
  --vault-name kv-myapp-prod \
  --name "DatabaseConnectionString" \
  --value "Server=mysql.database.azure.com;Database=appdb;User=sqladmin;Password=SuperSecret123!"

# Grant a Service Principal access to READ secrets
az keyvault set-policy \
  --name kv-myapp-prod \
  --spn <SERVICE_PRINCIPAL_APP_ID> \
  --secret-permissions get list

# Grant a Managed Identity access (preferred)
az keyvault set-policy \
  --name kv-myapp-prod \
  --object-id <MANAGED_IDENTITY_PRINCIPAL_ID> \
  --secret-permissions get list
```

### Reading Key Vault Secrets in a Pipeline (Variable Group)
1. In Azure DevOps: **Library → Variable Groups → + Variable Group**
2. Toggle "Link secrets from an Azure key vault".
3. Choose your Key Vault and map secrets as variables.
4. Reference in pipeline: `$(DatabaseConnectionString)`

```yaml
# In your pipeline YAML, link the variable group
variables:
  - group: kv-myapp-production-secrets  # Links to Key Vault-backed Variable Group

steps:
  - script: |
      echo "Connecting to DB..."  # The secret appears as a masked variable
      node app.js
    env:
      DATABASE_URL: $(DatabaseConnectionString)  # Injected from Key Vault
```

---

## 2. Identity & Access Management (IAM)

### Service Principals (for Pipelines)
A Service Principal (SP) is a non-human identity for an application to authenticate against Azure.

```bash
# Create a Service Principal with Contributor access to a Resource Group
az ad sp create-for-rbac \
  --name sp-azuredevops-pipeline \
  --role Contributor \
  --scopes /subscriptions/<SUB_ID>/resourceGroups/rg-production \
  --sdk-auth  # Outputs JSON suitable for a service connection

# Output:
# {
#   "clientId": "...",
#   "clientSecret": "...",    <-- Treat as a password! Store in Key Vault.
#   "subscriptionId": "...",
#   "tenantId": "...",
# }
```

Creating a Service Connection in Azure DevOps using the SP:
- **Project Settings → Service Connections → New (Azure Resource Manager)**
- Choose "Service Principal (manual)" and paste the credentials.

### Managed Identities (for App Code)
A Managed Identity removes the need for credentials entirely. Azure manages the identity for you.

**Expert insight — System-Assigned vs User-Assigned Managed Identity, and when it matters:**
- **System-Assigned**: tied 1:1 to the lifecycle of the resource it's attached to (e.g., the Web App) — created when the resource is created, destroyed when the resource is destroyed. Simple, but if you delete/recreate the Web App, the identity (and everything granted to it) is gone and must be reconfigured.
- **User-Assigned**: an independent Azure resource of its own, which can be attached to multiple resources (e.g., the same identity shared by an App Service and a Function App that both need the same Key Vault access), and it survives the deletion of any single resource it's attached to.
- Choose User-Assigned when multiple resources need identical access (avoids reconfiguring RBAC/Key Vault policies N times) or when the identity's lifecycle should outlive any single resource; System-Assigned is simpler when it's genuinely a 1:1, tightly-coupled relationship.
- **Managed Identities only work for Azure resources talking to Azure services** — they can't be used for Azure DevOps pipelines authenticating *to* Azure (the pipeline runs on Microsoft's infrastructure, not yours). For that, use a Service Principal or, better, Workload Identity Federation.

```bash
# Assign System-Managed Identity to a Web App
az webapp identity assign \
  --name app-myapp-prod \
  --resource-group rg-production

# Get the Principal ID of the identity
APP_IDENTITY=$(az webapp identity show --name app-myapp-prod \
  --resource-group rg-production --query principalId --output tsv)

# Grant that identity access to Key Vault
az keyvault set-policy \
  --name kv-myapp-prod \
  --object-id $APP_IDENTITY \
  --secret-permissions get list
```

```javascript
// Node.js - Access Key Vault using Managed Identity (NO credentials in code!)
import { SecretClient } from "@azure/keyvault-secrets";
import { DefaultAzureCredential } from "@azure/identity";

const credential = new DefaultAzureCredential();  // Uses Managed Identity automatically
const client = new SecretClient("https://kv-myapp-prod.vault.azure.net", credential);

const secret = await client.getSecret("DatabaseConnectionString");
const dbConnectionString = secret.value;
```

### Role-Based Access Control (RBAC)
```bash
# Assign the 'Reader' role to a user on a Resource Group
az role assignment create \
  --assignee "user@company.com" \
  --role "Reader" \
  --scope /subscriptions/<SUB_ID>/resourceGroups/rg-devops

# List role assignments on a resource group
az role assignment list \
  --resource-group rg-production \
  --output table

# Custom RBAC Role (if built-in roles are too permissive)
az role definition create --role-definition '{
  "Name": "Custom Pipeline Role",
  "Description": "Allows deploy to App Service but not modify infrastructure",
  "Actions": [
    "Microsoft.Web/sites/write",
    "Microsoft.Web/sites/read",
    "Microsoft.Web/sites/restart/action"
  ],
  "NotActions": [],
  "AssignableScopes": ["/subscriptions/<SUB_ID>"]
}'
```

---

## 3. Pipeline Security

### Secret Scanning (Detecting Leaked Credentials)
```yaml
# Use Gitleaks to scan for secrets in EVERY PR
- stage: SecurityScan
  jobs:
    - job: SecretScan
      pool:
        vmImage: 'ubuntu-latest'
      steps:
        - script: |
            # Install Gitleaks
            wget https://github.com/gitleaks/gitleaks/releases/download/v8.18.0/gitleaks_8.18.0_linux_x64.tar.gz
            tar -xzf gitleaks_8.18.0_linux_x64.tar.gz
            chmod +x gitleaks
            
            # Run the scan on changed files
            ./gitleaks detect --source . --verbose --exit-code 1
          displayName: 'Scan for hardcoded secrets'
```

### Dependency Vulnerability Scanning
```yaml
# Scan npm dependencies for known CVEs
- script: |
    npm audit --audit-level=high  # Fail build if any HIGH vulnerabilities found
  displayName: 'npm Audit - Dependency Scan'

# OR use OWASP Dependency Check
- task: dependency-check-build-task@6
  displayName: 'OWASP Dependency Check'
  inputs:
    projectName: 'MyApp'
    scanPath: '$(System.DefaultWorkingDirectory)'
    format: 'HTML,JUNIT'
    failOnCVSS: '7'  # Fail on Critical/High CVEs (score >= 7)
```

### SAST (Static Application Security Testing)
```yaml
# Run SonarQube Analysis
- task: SonarQubePrepare@5
  inputs:
    SonarQube: 'MySonarQubeServiceConnection'
    scannerMode: 'CLI'
    configMode: 'manual'
    cliProjectKey: 'myapp'
    cliSources: 'src'

- script: npm run build
  displayName: 'Build'

- task: SonarQubeAnalyze@5
  displayName: 'SonarQube Analysis'

- task: SonarQubePublish@5
  displayName: 'Publish Quality Gate Result'
  inputs:
    pollingTimeoutSec: '300'
```

---

## Common Pitfalls & Expert Tips

- **Service Principal client secrets with no expiry, or long expiry, never rotated.** A forgotten SP secret from 2 years ago with Contributor rights on production is a classic finding in security audits — set short expiries and track rotation, or move to Workload Identity Federation (no secret at all).
- **Granting `Contributor` (or worse, `Owner`) at the subscription level to a pipeline's Service Connection "to keep things simple."** Violates least privilege badly — scope service connections to the specific resource group(s) a given pipeline actually needs to touch.
- **Treating `npm audit`/dependency scanning as a one-time setup instead of a continuously enforced gate.** New CVEs are discovered in already-shipped dependencies constantly — a scan only run once at pipeline creation misses everything discovered afterward. It needs to run on every build.
- **Masking secrets in logs (`$(SecretVar)`) but then echoing them indirectly** (e.g., writing them to a file and `cat`-ing the file, or interpolating them into a shell command that gets logged) — Azure Pipelines' log masking is string-match based and easy to accidentally bypass.
- **SAST-only security strategy with no DAST or dependency scanning.** SAST (static analysis of your own code) misses vulnerabilities in third-party dependencies and runtime-only issues (like misconfigured headers) — a mature pipeline layers SAST + dependency scanning + secret scanning + (for critical apps) DAST.

---

## Practical Exercise ✅
1. Create an Azure Key Vault and add 3 secrets (DB password, API key, JWT secret).
2. Link the Key Vault to an Azure DevOps Variable Group.
3. Use a secret in a pipeline step via the Variable Group (verify it appears masked in logs).
4. Add the `npm audit` step to your CI pipeline. Fix any HIGH vulnerabilities it finds.
5. Create a Service Principal and use it to set up a Service Connection in Azure DevOps.

---

## Expert Interview Q&A

**Q: Service Principal vs Managed Identity vs Workload Identity Federation — when do you use each, precisely?**
Service Principal: a non-human Azure AD identity authenticated with a client secret or certificate — used when a system *outside* Azure (like an on-prem app, or historically, Azure DevOps) needs to authenticate to Azure APIs; requires managing secret rotation. Managed Identity: for an Azure *resource* (VM, App Service, Function) to authenticate to other Azure services with zero stored credentials — Azure handles the credential lifecycle entirely, but it only works from within Azure resources. Workload Identity Federation: lets an external system (like Azure DevOps or GitHub Actions) exchange its own short-lived OIDC token for Azure access *without* any stored secret at all — the current best-practice replacement for Service Principal client secrets in CI/CD pipelines.

**Q: Why is a Managed Identity not usable for Azure DevOps pipeline authentication to Azure?**
Managed Identity is bound to the lifecycle and identity of a specific Azure *resource* — the pipeline agent itself isn't an Azure resource you control in that way (Microsoft-hosted agents are ephemeral, shared infrastructure). Pipelines need either a Service Principal (with a stored secret/cert) or Workload Identity Federation (token exchange, no stored secret) to authenticate outward to Azure.

**Q: Your organization wants to eliminate long-lived secrets from CI/CD entirely. What's the modern approach?**
Workload Identity Federation (OIDC-based). Instead of storing a Service Principal's client secret in Azure DevOps, you configure a federated credential on the Azure AD App Registration that trusts tokens issued by Azure DevOps for a specific pipeline/service connection. At runtime, Azure DevOps presents a short-lived, cryptographically verifiable OIDC token; Azure AD exchanges it for a short-lived access token. No secret is ever stored, so there's nothing to leak or rotate.

**Q: What's the risk of granting a pipeline's service connection `Contributor` access at the subscription level instead of a specific resource group?**
It violates least privilege — if that pipeline (or its stored credentials) is ever compromised, the blast radius is the entire subscription rather than one resource group. It also makes it harder to reason about "what can this pipeline actually touch" during a security review. Scope service connections as narrowly as the pipeline's actual deployment target requires.
