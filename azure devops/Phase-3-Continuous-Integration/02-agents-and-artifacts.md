# Build Agents & Azure Artifacts

## Build Agents

### Microsoft-Hosted Agents
These are fully managed VMs spun up fresh for each job and discarded after.

| Image Name | OS | Pre-installed Tools |
|---|---|---|
| `ubuntu-latest` | Ubuntu 22.04 | Docker, Node, Python, Java, Git, Azure CLI |
| `windows-latest` | Windows Server 2022 | .NET, Azure CLI, PowerShell, Node |
| `macos-latest` | macOS 13 (Ventura) | Xcode, Node, Homebrew |

```yaml
# Using a Microsoft-hosted agent
pool:
  vmImage: 'ubuntu-latest'
```

### Self-Hosted Agents
Install on your own VM (Azure VM, on-prem server, Docker container). Best for:
- Accessing internal resources (private databases, on-prem APIs).
- Pre-caching large build dependencies.
- Needing specific hardware or software not on hosted images.

```bash
# ---- Self-Hosted Agent Setup on Linux VM ----

# 1. Create an Agent Pool in Azure DevOps:
#    Project Settings -> Agent Pools -> Add pool

# 2. Download and configure the agent (run on your VM):
mkdir ~/myagent && cd ~/myagent
curl -O https://vstsagentpackage.azureedge.net/agent/3.238.0/vsts-agent-linux-x64-3.238.0.tar.gz
tar zxvf ./vsts-agent-linux-x64-3.238.0.tar.gz

# 3. Configure (PAT token required with 'Agent Pools (Read & manage)' scope)
./config.sh --url https://dev.azure.com/YOUR_ORG \
            --auth pat \
            --token YOUR_PAT_TOKEN \
            --pool MyLinuxAgentPool \
            --agent MyAgent-01

# 4. Run as a service (auto-start on boot)
sudo ./svc.sh install
sudo ./svc.sh start
```

```yaml
# Using a self-hosted agent pool in a pipeline
pool:
  name: 'MyLinuxAgentPool'
  demands:
    - node  # Only use agents that have Node.js installed
```

---

## Agent Capabilities & Demands

```yaml
# In the pipeline, DEMAND specific capabilities from agents
pool:
  name: 'MyPool'
  demands:
    - java           # Agent must have Java installed
    - maven          # Agent must have Maven installed
    - agent.os -equals Windows_NT  # Windows agents only
```

You register capabilities on a self-hosted agent via:
**Agent Pool → Agents → Select Agent → Capabilities → Add user capability**.

---

## Azure Artifacts (Package Management)

Azure Artifacts is a private package registry for your team. It hosts npm, NuGet, Maven, Python, and Universal packages.

### Creating and Publishing an npm Package

```yaml
# azure-pipelines.yml - Publish npm package to Azure Artifacts

steps:
  - task: NodeTool@0
    inputs:
      versionSpec: '20.x'

  # Authenticate with the Azure Artifacts npm feed
  - task: npmAuthenticate@0
    inputs:
      workingFile: .npmrc  # Points to your Azure Artifacts feed

  - script: npm install
    displayName: 'Install dependencies'

  - script: npm run build
    displayName: 'Build package'

  - task: npm@1
    displayName: 'Publish to Azure Artifacts'
    inputs:
      command: 'publish'
      publishRegistry: 'useFeed'
      publishFeed: 'MyOrg/MyFeedName'
```

```ini
# .npmrc file (tells npm where your private registry is)
registry=https://pkgs.dev.azure.com/MyOrg/MyProject/_packaging/MyFeedName/npm/registry/
always-auth=true
```

### Consuming a Package from Azure Artifacts

```bash
# Configure npm to use your private feed
npm config set registry https://pkgs.dev.azure.com/MyOrg/_packaging/MyFeedName/npm/registry/

# Install the private package
npm install @myorg/my-private-lib
```

### Universal Packages (for non-typed binaries/files)

```yaml
# Upload any file/folder as a Universal Package
- task: UniversalPackages@0
  displayName: 'Publish Universal Package'
  inputs:
    command: 'publish'
    publishDirectory: '$(Build.ArtifactStagingDirectory)'
    feedsToUsePublish: 'internal'
    vstsFeedPublish: 'MyFeedName'
    vstesFeedPackagePublish: 'my-binary-tools'
    versionPublish: '1.0.$(Build.BuildId)'

# Download a Universal Package
- task: UniversalPackages@0
  displayName: 'Download Universal Package'
  inputs:
    command: 'download'
    feedsToUse: 'internal'
    vstsFeed: 'MyFeedName'
    vstsFeedPackage: 'my-binary-tools'
    vstsPackageVersion: '1.0.42'
    downloadDirectory: '$(System.DefaultWorkingDirectory)/tools'
```

---

## Practical Exercise ✅
1. Set up a self-hosted agent on a local VM or Azure VM. Verify it appears in your agent pool.
2. Modify the pipeline from the previous exercise to run on your self-hosted agent.
3. Create an Azure Artifacts feed.
4. Publish a sample npm package (version `1.0.0`) to your feed.
5. In another pipeline (or another step), consume that package via a `.npmrc` file.
