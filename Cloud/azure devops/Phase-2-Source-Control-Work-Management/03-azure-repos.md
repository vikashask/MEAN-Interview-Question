# Azure Repos - Source Control Hub

> **Expert framing:** Branch policies are the actual security/quality control layer of your SDLC — an expert configures them defensively (assuming someone *will* try to push straight to `main`, or approve their own PR, eventually) rather than just enabling the defaults. PATs are also a common real-world security incident source — know their scope and expiry implications cold.

## Setting Up an Azure Repo

### Cloning a Repo
```bash
# Using HTTPS (recommended with a PAT token)
git clone https://dev.azure.com/{org}/{project}/_git/{repository}

# You'll be prompted for credentials.
# Username: anything (e.g., your email)
# Password: your Personal Access Token (PAT)

# To avoid typing credentials every time, use Git Credential Manager:
git config --global credential.helper manager
```

### Generating a Personal Access Token (PAT)
1. In Azure DevOps, click your profile picture (top right) → **Personal Access Tokens**.
2. Click **+ New Token**.
3. Select **Code (Read & Write)** scope.
4. Copy the token immediately (it won't be shown again).

---

## Branch Policies (The Heart of Code Quality)

Branch policies protect important branches (like `main`) from direct pushes and enforce quality gates on every Pull Request.

### Setting Up Policies on `main`
Go to **Project Settings > Repos > Branches → Click `...` next to `main` > Branch Policies**.

**Recommended policies for production branches:**

| Policy | Setting | Why |
|--------|---------|-----|
| Minimum number of reviewers | 1 or 2 | Enforces code review |
| Check for linked work items | Required | Traceability to Boards |
| Check for comment resolution | Required | Ensures all review comments are addressed |
| Limit merge types | Squash or Rebase | Keeps main history clean |
| Build validation | Required - link to CI pipeline | Ensures code builds before merge |

**Expert insight:** also enable **"Reset code reviewer votes when there are new changes"** — without it, a reviewer can approve a PR, then someone pushes an unreviewed change onto the same branch before merge, and it ships without a fresh review. This is a real, commonly-missed gap. For genuinely sensitive branches, also check **"The most recent push was not approved by the pusher"**, which stops someone from approving their own final change.

---

## Pull Request (PR) Workflow

### Creating a PR via CLI (using Azure DevOps CLI extension)
```bash
# Install the DevOps CLI extension
az extension add --name azure-devops

# Set your org and project defaults
az devops configure --defaults organization=https://dev.azure.com/myorg project=MyProject

# Create a PR
az repos pr create \
  --title "feat: Add user authentication endpoint" \
  --description "Implements JWT-based login. Closes #123" \
  --source-branch feature/auth \
  --target-branch main \
  --reviewers "teammate@company.com" \
  --work-items 123

# List open PRs
az repos pr list --status active --output table

# Approve a PR
az repos pr update --id <PR_ID> --vote approve

# Complete/Merge a PR
az repos pr update --id <PR_ID> --status completed --merge-commit-message "feat: Add auth endpoint (squash)"
```

---

## A Good PR Description Template
```markdown
## Summary
Briefly describe what this PR does.

## Changes Made
- Added `AuthController.cs` with `/login` and `/logout` endpoints.
- Implemented JWT token generation.
- Added unit tests for token validation.

## Testing Done
- [x] Unit tests pass (`dotnet test`)
- [x] Manually tested login flow with Postman.
- [ ] Integration tests (pending - see issue #456)

## Screenshots / Logs (if applicable)
[Paste relevant Postman output or screenshots here]

## Related Work Items
Closes AB#123
```

---

## Azure Repos with `.gitignore` & `.gitattributes`
```bash
# .gitignore for a Node.js project
node_modules/
dist/
.env
.env.local
*.log
coverage/
.DS_Store

# .gitattributes to normalize line endings across OS
* text=auto eol=lf
*.ps1 text eol=crlf
*.bat text eol=crlf
*.png binary
*.jpg binary
```

---

## Tagging and Releases
```bash
# Create an annotated tag (points to a specific commit)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tags to Azure Repos
git push origin --tags

# List all tags
git tag -l "v1.*"
```

---

## Common Pitfalls & Expert Tips

- **PATs with no expiry, and overly broad scope ("Full access").** Treat a PAT exactly like a password — scope it to the minimum needed (e.g., just "Code: Read & Write") and set a short expiry. A leaked full-access PAT with no expiry is a standing security incident waiting to happen.
- **Not rotating PATs used in automation/service hooks.** Any script or external tool holding a PAT should be tracked somewhere so it can be rotated before expiry without breaking silently in production.
- **Skipping "reset approvals on new changes."** Without it, a PR can be approved once and then quietly modified before merge — approvals become theater rather than an actual control.
- **Allowing all merge types on `main`.** Mixing merge commits, squash, and rebase on the same protected branch produces an inconsistent, hard-to-read history. Pick one (squash is most common for keeping `main` linear and readable) and enforce it via policy.
- **Using `.gitattributes` line-ending settings inconsistently across a team with mixed OSes** (Windows devs + Linux CI) causes noisy diffs where every line shows as changed due to CRLF/LF mismatches — `* text=auto eol=lf` at the repo root prevents this.

---

## Practical Exercise ✅
1. Create a new repository in Azure DevOps.
2. Clone it locally and push a Node.js or Python app.
3. Protect the `main` branch: require 1 reviewer + linked work item + passing CI build.
4. Create a `feature/update-readme` branch, commit a change, and open a Pull Request.
5. Link the PR to a work item created in Phase 2's Boards exercise.
6. Complete the PR using the "Squash commit" merge strategy.

---

## Expert Interview Q&A

**Q: What's wrong with a branch policy that only requires "1 reviewer," with no other settings?**
Without "reset votes on new changes," an approval can become stale — someone approves, then the branch gets more (unreviewed) commits pushed before merge, and it ships anyway. Without "most recent push not approved by the pusher," someone could push a change and then approve their own PR. A robust policy combines: minimum reviewers, reset-on-change, linked work items, comment resolution required, and build validation — not just reviewer count alone.

**Q: How do you securely automate PR creation/approval from a script without embedding a personal password?**
Use a Personal Access Token (PAT) scoped to only the permissions needed (e.g., Code Read & Write) with a defined expiry, stored in a secrets manager (Key Vault/pipeline secret variable) rather than hardcoded — or, in newer setups, use Azure DevOps' support for Azure AD / Workload Identity Federation-based auth where available to avoid a long-lived secret entirely.

**Q: Why would a team enforce "squash merge only" on `main` instead of allowing regular merge commits?**
Squash merging collapses a PR's often-messy intermediate commits ("fix typo," "wip," "actually fix it") into one clean commit on `main`, keeping history readable and making `git log`/`git bisect` easier to reason about. The trade-off is losing the individual commit-level granularity from the feature branch — acceptable for most teams since that detail is still visible in the PR itself if needed.
