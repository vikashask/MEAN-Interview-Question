# DevSecOps - Security in the Pipeline

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

## Practical Exercise ✅
1. Create an Azure Key Vault and add 3 secrets (DB password, API key, JWT secret).
2. Link the Key Vault to an Azure DevOps Variable Group.
3. Use a secret in a pipeline step via the Variable Group (verify it appears masked in logs).
4. Add the `npm audit` step to your CI pipeline. Fix any HIGH vulnerabilities it finds.
5. Create a Service Principal and use it to set up a Service Connection in Azure DevOps.
