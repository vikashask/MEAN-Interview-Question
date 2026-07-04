# Azure DevOps — Continuous Delivery Quick Reference

> **Expert framing:** This file is your fast-recall cheat sheet for what each Azure DevOps service is *for*, not just its feature list. In interviews, being able to instantly map "which service handles this concern" (traceability → Boards, versioning → Repos, automation → Pipelines, testing → Test Plans, packages → Artifacts) signals real fluency with the platform, not memorized trivia.

## Core Definitions

**Continuous Delivery**: a repeatable, reliable process for shipping software so that new value reaches customers fast and safely, every time — the "repeatable and reliable" part matters as much as the "fast" part; a fast process that breaks unpredictably isn't continuous delivery, it's just risky automation.

**DevOps**: the union of people, process, and tooling that enables continuous delivery of value to the end user. Note what this definition deliberately includes: DevOps isn't a tool (Azure DevOps the *product* is named after the *practice*, not the other way around) — it's an operating model. Buying Azure DevOps licenses does not make an organization "doing DevOps" if the culture/process side isn't there.

## The Five Azure DevOps Services, at a Glance

| Service | Core Job | Key Concepts |
|---|---|---|
| **Boards** | Work tracking & traceability | Work Items, Kanban, Backlogs, Sprints |
| **Repos** | Source control | Files, Commits, Branches, Tags, Pull Requests |
| **Pipelines** | Build & release automation | Pipelines, Environments, Releases, Library, Deployment Groups |
| **Test Plans** | Manual & exploratory testing | Test Plans, Test Runs, Progress Reports, Load Testing |
| **Artifacts** | Package management | NuGet, npm, Maven, Universal Packages |

### Boards — Work Item, Traceability, Planning
Everything starts here: an Epic breaks into Features, breaks into User Stories, breaks into Tasks. The value isn't the hierarchy itself — it's that every downstream artifact (a commit, a PR, a build, a release) can link back to *why* the change was made. This link is what "traceability" means in an audit or incident-review context.

### Repos — Files, Commits, Pushes, Branches, Tags, Pull Requests
Git-based source control with branch policies enforcing quality gates (required reviewers, linked work items, passing builds) before code reaches protected branches like `main`.

### Pipelines — Build Automation, CI, Deployment Automation, CD
The automation engine. Its responsibilities break into two halves people often conflate:
- **Continuous Integration (CI)**: automatically build + test every change, catching problems immediately.
- **Continuous Delivery/Deployment (CD)**: automatically ship a validated build to an environment, with Delivery requiring a human "go" and Deployment being fully automatic.

Also covers: Environments (deployment targets with approval/gates), the Library (shared variable groups, often Key Vault-backed), Task Groups (reusable step bundles), and Deployment Groups (for classic, non-containerized VM-target deployments).

### Test Plans — Planned & Exploratory Testing
Structured manual test case management plus exploratory testing session capture, across web and desktop apps, with end-to-end traceability back to the requirement/work item being verified. Distinct from automated tests run inside Pipelines — Test Plans is for the *human*-driven testing layer.

### Artifacts — Package Management
A private package registry (NuGet, npm, Maven, Python, Universal Packages) for your org — lets teams publish and consume internal libraries the same way they'd consume public ones, with usage tracking and full traceability of what version is used where.

## Expert Interview Q&A

**Q: Is buying Azure DevOps licenses the same as "doing DevOps"? Why does this distinction matter in an interview answer?**
No — DevOps is defined as the union of *people, process, and products*. Tooling alone (Pipelines, Repos) automates mechanics but doesn't create the collaborative culture, shared ownership, or feedback loops that make continuous delivery actually reliable. Interviewers ask variations of this question specifically to filter candidates who understand DevOps as a practice versus those who only know a product's feature list.

**Q: What's the practical difference between what Pipelines' CI half does versus its CD half?**
CI's job is fast feedback on *code correctness* — build and test every change quickly so problems are caught within minutes, not weeks. CD's job is *safe delivery* of an already-validated build to real environments — sequencing through Dev/QA/Prod with appropriate approvals/gates. Conflating them (e.g., deploying straight to production as part of the same job that runs unit tests) removes the safety checkpoints CD strategies (approvals, canary, blue-green) are built to provide.

**Q: Why does Azure DevOps separate Test Plans from the testing that happens inside Pipelines?**
Pipelines runs *automated* tests (unit/integration) as part of the build — fast, deterministic, no human needed. Test Plans manages *manual and exploratory* testing — scenarios that need human judgment, UI/UX verification, or ad-hoc exploration that hasn't been automated yet. Mature teams use both: automation for regression coverage, Test Plans for exploratory/manual verification and for tracking formal test sign-off in regulated environments.
