# Build Agents & Azure Artifacts

> **Expert framing:** Choosing hosted vs self-hosted agents is a cost/control/security trade-off, not just a checkbox — an expert can articulate exactly *why* a workload needs self-hosted (network access to on-prem, licensing, pre-warmed caches, specific hardware) rather than defaulting to it out of habit. Artifacts feed management (upstream sources) is also a frequently-tested, easy-to-get-wrong area around supply-chain security.

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

**Expert insight — the real trade-offs behind hosted vs self-hosted:**
- **Microsoft-hosted**: zero maintenance, fresh/clean VM every run (no state leakage between builds — good for security/reproducibility), but capped build minutes on free tiers, no access to private/on-prem networks, and slower cold-start since a fresh VM boots each time.
- **Self-hosted**: full control (custom tools, pre-warmed dependency caches for much faster builds), can sit inside a private VNet to reach internal resources (on-prem DBs, internal APIs) — but *you* own patching, security hardening, and capacity planning, and because the same machine may be reused across runs, state can leak between builds unless you clean up deliberately (a security/reproducibility risk if not managed).
- A common enterprise pattern: Microsoft-hosted for public/open-source-style builds, self-hosted (often in a VNet with private endpoints) for anything needing internal network access or heavy caching.

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

## Common Pitfalls & Expert Tips

- **Self-hosted agents that never get patched.** Since you own the OS, they're your responsibility for security updates — a stale, unpatched agent VM is a real attack surface, especially since it often has broad credentials (service connections) configured on it.
- **State leakage between builds on self-hosted agents.** Unlike the always-fresh Microsoft-hosted VMs, a self-hosted agent can carry over files/env vars from a previous job unless the pipeline explicitly cleans the workspace — this can cause "works sometimes, fails other times" flakiness that's hard to diagnose.
- **Upstream sources in Azure Artifacts feeding directly from the public npm/NuGet registry without any vetting.** This is a supply-chain risk — a compromised public package gets pulled straight into your internal feed and consumed by every project pointing at it. Many orgs configure upstream sources with additional scanning/approval steps for exactly this reason.
- **Granting the pipeline's default identity ("Project Collection Build Service") more Artifacts feed permissions than needed** (e.g., Owner instead of Contributor) — violates least privilege for a non-human identity that's a common pivot point if a pipeline is compromised.

---

## Practical Exercise ✅
1. Set up a self-hosted agent on a local VM or Azure VM. Verify it appears in your agent pool.
2. Modify the pipeline from the previous exercise to run on your self-hosted agent.
3. Create an Azure Artifacts feed.
4. Publish a sample npm package (version `1.0.0`) to your feed.
5. In another pipeline (or another step), consume that package via a `.npmrc` file.

---

## Expert Interview Q&A

**Q: When would you choose a self-hosted agent over a Microsoft-hosted one, specifically?**
When the build needs access to resources not reachable from the public internet (an on-prem database, an internal API behind a VPN/private endpoint), when you need pre-warmed dependency caches for significantly faster builds at high volume, when you need specific hardware (GPU builds) or licensed software not on the hosted images, or when you've exhausted free-tier hosted build minutes and want predictable cost via owned infrastructure.

**Q: What security risk does an Azure Artifacts "upstream source" pointing directly at the public npm registry introduce, and how is it mitigated?**
It creates a direct supply-chain path from any public package straight into your organization's builds — a compromised or typosquatted public package becomes available to every internal consumer immediately. Mitigation: use upstream sources with review/approval gates, pin exact versions (avoid open version ranges like `^1.0.0` in production dependencies), and consider a scanning step (e.g., `npm audit`, dependency vulnerability scanning) before packages are trusted for consumption.

**Q: Why might state leak between builds on a self-hosted agent, and why doesn't this happen on Microsoft-hosted agents?**
Self-hosted agents reuse the same OS/filesystem across multiple pipeline runs unless the pipeline explicitly does a clean checkout/workspace reset — leftover files, cached dependencies, or environment state from a previous job can silently affect the next one. Microsoft-hosted agents provision a brand-new VM for every single job and destroy it afterward, so there's no possibility of cross-run contamination by design.
