# Azure DevOps Learning Repository

A phase-by-phase, hands-on guide to mastering the full Azure DevOps ecosystem.
Each phase folder contains detailed, code-first markdown documents to study and practice.

---

## 🗂️ Folder Structure

```
azure devops/
 ├── Azure-DevOps-Roadmap-Detailed.md          ← High-level checklist (start here)
 │
 ├── Phase-1-Prerequisites-Foundation/
 │   ├── 01-cloud-fundamentals.md              ← IaaS/PaaS/SaaS, ARM, CLI basics
 │   └── 02-scripting-cli.md                   ← Bash, PowerShell, Azure CLI
 │
 ├── Phase-2-Source-Control-Work-Management/
 │   ├── 01-git-mastery.md                     ← Git commands, branching, merge vs rebase
 │   ├── 02-azure-boards.md                    ← Agile, Scrum, WIQL, Dashboards
 │   └── 03-azure-repos.md                     ← Branch policies, PR workflows
 │
 ├── Phase-3-Continuous-Integration/
 │   ├── 01-yaml-pipelines.md                  ← Full YAML anatomy, variables, conditions
 │   └── 02-agents-and-artifacts.md            ← Hosted vs self-hosted, Azure Artifacts
 │
 ├── Phase-4-Continuous-Deployment/
 │   └── 01-environments-and-release-strategies.md  ← Multi-stage CD, approvals, Blue-Green, Canary
 │
 ├── Phase-5-Infrastructure-as-Code/
 │   ├── 01-terraform.md                       ← Full Terraform workflow, Azure + pipeline
 │   └── 02-azure-bicep.md                     ← Bicep syntax, modules, loops
 │
 ├── Phase-6-Containerization-Orchestration/
 │   ├── 01-docker-and-acr.md                  ← Dockerfile, Docker Compose, ACR
 │   └── 02-azure-kubernetes-service.md        ← K8s concepts, YAML manifests, AKS, Helm
 │
 ├── Phase-7-DevSecOps-Security/
 │   └── 01-devsecops-and-keyvault.md          ← Key Vault, Managed Identities, RBAC, secret scanning
 │
 └── Phase-8-Monitoring-Optimization/
     └── 01-monitoring-and-optimization.md     ← Application Insights, KQL, Alerts, caching, templates
```

---

## 📋 Learning Path & Status

| Phase | Topic | Status |
|-------|-------|--------|
| 1 | Prerequisites & Foundation | [ ] |
| 2 | Source Control & Work Management | [ ] |
| 3 | Continuous Integration (CI) | [ ] |
| 4 | Continuous Deployment (CD) | [ ] |
| 5 | Infrastructure as Code (IaC) | [ ] |
| 6 | Containerization & Orchestration | [ ] |
| 7 | DevSecOps & Security | [ ] |
| 8 | Monitoring & Optimization | [ ] |
| 🏆 | AZ-400 Certification | [ ] |

---

## 🔗 Quick Links

### Phase 1: Prerequisites
- [Cloud Fundamentals](./Phase-1-Prerequisites-Foundation/01-cloud-fundamentals.md)
- [Scripting & CLI](./Phase-1-Prerequisites-Foundation/02-scripting-cli.md)

### Phase 2: Source Control
- [Git Mastery](./Phase-2-Source-Control-Work-Management/01-git-mastery.md)
- [Azure Boards](./Phase-2-Source-Control-Work-Management/02-azure-boards.md)
- [Azure Repos](./Phase-2-Source-Control-Work-Management/03-azure-repos.md)

### Phase 3: CI Pipelines
- [YAML Pipelines](./Phase-3-Continuous-Integration/01-yaml-pipelines.md)
- [Agents & Artifacts](./Phase-3-Continuous-Integration/02-agents-and-artifacts.md)

### Phase 4: CD / Release Management
- [Environments & Release Strategies](./Phase-4-Continuous-Deployment/01-environments-and-release-strategies.md)

### Phase 5: Infrastructure as Code
- [Terraform](./Phase-5-Infrastructure-as-Code/01-terraform.md)
- [Azure Bicep](./Phase-5-Infrastructure-as-Code/02-azure-bicep.md)

### Phase 6: Containers & Kubernetes
- [Docker & ACR](./Phase-6-Containerization-Orchestration/01-docker-and-acr.md)
- [Azure Kubernetes Service](./Phase-6-Containerization-Orchestration/02-azure-kubernetes-service.md)

### Phase 7: DevSecOps
- [DevSecOps & Key Vault](./Phase-7-DevSecOps-Security/01-devsecops-and-keyvault.md)

### Phase 8: Monitoring
- [Monitoring & Optimization](./Phase-8-Monitoring-Optimization/01-monitoring-and-optimization.md)

---

## 💡 Study Tips
- **Practice beats theory**: Every document has a "Practical Exercise". Do every one.
- **Use free tiers**: Azure gives $200 credit for new accounts. Use it fearlessly (just delete resources after).
- **Use Azure DevOps free tier**: Up to 5 users free with 1 parallel job.
- **Build a portfolio project**: The ultimate goal is an end-to-end repo on public GitHub showing all 8 phases working together.
