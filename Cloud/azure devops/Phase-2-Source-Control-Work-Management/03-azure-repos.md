# Azure Repos - Source Control Hub

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

## Practical Exercise ✅
1. Create a new repository in Azure DevOps.
2. Clone it locally and push a Node.js or Python app.
3. Protect the `main` branch: require 1 reviewer + linked work item + passing CI build.
4. Create a `feature/update-readme` branch, commit a change, and open a Pull Request.
5. Link the PR to a work item created in Phase 2's Boards exercise.
6. Complete the PR using the "Squash commit" merge strategy.
