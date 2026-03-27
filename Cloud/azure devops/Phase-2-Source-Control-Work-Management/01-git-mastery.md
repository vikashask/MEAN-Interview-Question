# Git Mastery for Azure DevOps

## Core Git Workflow

### Initial Setup
```bash
git config --global user.name "Your Name"
git config --global user.email "you@company.com"
git config --global core.editor "code --wait"  # Use VS Code as editor
git config --list  # View all config
```

### The Staging Area (Understanding the Three States)
```
Working Directory  -->  Staging Area (Index)  -->  Repository (.git)
   git add file            git commit
```

```bash
git init                  # Initialize a new repo
git status                # See what's changed
git add file.txt          # Stage a specific file
git add .                 # Stage ALL changes
git add -p                # Interactively stage chunks of changes
git commit -m "message"   # Commit what's staged
git commit -am "message"  # Stage & commit tracked files in one go
git log --oneline --graph --decorate  # Pretty log view
```

---

## Branching Deep Dive

### Branch Operations
```bash
git branch                   # List local branches
git branch -a                # List all branches (local + remote)
git branch feature/login     # Create a new branch
git checkout feature/login   # Switch to a branch
git switch feature/login     # Modern alternative to checkout
git checkout -b feature/login # Create AND switch in one command
git branch -d feature/login  # Delete a merged branch
git branch -D feature/login  # Force delete (even if not merged)
```

### Merge vs Rebase
```bash
# ---- MERGE ----
# Creates a merge commit. Preserves history exactly.
git checkout main
git merge feature/login
# Result: creates a "Merge commit" node in history

# ---- REBASE ----
# Rewrites your branch's commits on top of main. Linear history.
git checkout feature/login
git rebase main
# Result: your feature commits appear AFTER the latest main commits

# Interactive Rebase (clean up commits before merging)
git rebase -i HEAD~3  # Reword/squash/drop last 3 commits
```

**When to use which?**
| Scenario | Use |
|----------|-----|
| Public shared branches | `merge` (don't rewrite shared history) |
| Cleaning up local feature branch | `rebase -i` |
| Keeping feature branch up-to-date | `rebase main` |

---

## Remote Operations

```bash
git remote add origin https://dev.azure.com/yourorg/project/_git/repo-name
git remote -v                 # View configured remotes
git push -u origin main       # Push and set upstream tracking
git push                      # Subsequent pushes
git fetch                     # Download changes but DON'T merge
git pull                      # fetch + merge (or fetch + rebase if configured)
git pull --rebase             # fetch + rebase (cleaner history)
```

---

## Troubleshooting & Recovery

```bash
# Stash uncommitted changes temporarily
git stash
git stash pop                 # Apply most recent stash and remove it
git stash list                # See all stashes
git stash apply stash@{2}     # Apply a specific stash

# Undoing Changes
git restore file.txt          # Discard working dir changes (UNSTAGED)
git restore --staged file.txt # Unstage a file (keep working dir changes)
git reset --soft HEAD~1       # Undo last commit, keep changes STAGED
git reset --mixed HEAD~1      # Undo last commit, keep changes UNSTAGED (default)
git reset --hard HEAD~1       # Undo last commit, DESTROY changes (dangerous!)
git revert <commit-hash>      # Create a new commit that undoes changes (safe for shared branches)

# Resolving Merge Conflicts
# After a conflict, files will have markers:
# <<<<<<< HEAD
# your changes
# =======
# their changes
# >>>>>>> feature/other-branch
# Edit the file, then:
git add file.txt
git commit  # Complete the merge
```

---

## Branching Strategies

### GitFlow
```
main         (production-ready code)
develop      (integration branch - feature branches merge here)
feature/*    (new features)
release/*    (preparing for a release: bug fixes only)
hotfix/*     (emergency production fix - branches from main)
```

### Trunk-Based Development (Preferred for CI/CD)
```
main         (the ONE trunk - always deployable)
  └── feature/short-lived (merged within 1-2 days)
```
> This is the recommended approach for Azure DevOps pipelines as it supports continuous integration naturally.

---

## Practical Exercise ✅
1. Create a new local repo and make 3 commits on `main`.
2. Create a `feature/add-readme` branch, make 2 commits.
3. Simulate a merge conflict: edit the same line in `main` and `feature/add-readme`. Resolve it.
4. Squash your 2 feature commits into 1 using `git rebase -i`.
5. Merge the feature into `main` with a merge commit.
