# Git Mastery for Azure DevOps

> **Expert framing:** Knowing `add`/`commit`/`push` is table stakes. Expert-level Git means understanding *why* rebase rewrites history and when that's dangerous, being able to recover from a bad `reset --hard` before it's too late, and picking a branching strategy that matches your team's release cadence rather than cargo-culting GitFlow because a tutorial said so.

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

**Expert insight — the "golden rule of rebase":** never rebase a branch that other people have already pulled/based work on. Rebase rewrites commit hashes; if someone else already has the old commits, their next `pull` produces duplicated/conflicting history. This is the single most common Git incident in teams — someone force-pushes a rebased shared branch and everyone else's local history diverges. Rule of thumb: rebase freely on branches only you use; merge on anything shared.

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

## Common Pitfalls & Expert Tips

- **Force-pushing a rebased shared branch.** Use `git push --force-with-lease` instead of `--force` — it refuses to overwrite the remote if someone else has pushed since your last fetch, preventing you from silently destroying a teammate's work.
- **`git reset --hard` without checking `git reflog` first.** Every commit you've ever had HEAD point to is recoverable via `git reflog` for a while (default ~90 days) even after a hard reset — this is the "oh no" escape hatch every expert knows before they need it.
- **Confusing `git fetch` with `git pull`.** `fetch` only downloads; it never touches your working directory or current branch — always safe to run. `pull` = `fetch` + `merge` (or `rebase`), which *does* modify your branch. When debugging "why does my branch look wrong," a plain `fetch` + `git log origin/main` is the safe way to inspect without side effects.
- **Trunk-based development requires small, short-lived branches** (hours to 1-2 days) merged frequently, plus feature flags for incomplete work — teams that adopt "trunk-based" in name but keep branches alive for weeks get the worst of both worlds (merge conflicts *and* no real CI benefit).
- **Squash-merging by default in Azure Repos** keeps `main` history readable (one commit per PR) but loses the individual commit granularity for `git bisect` — know this trade-off before setting it as a blanket policy.

---

## Practical Exercise ✅
1. Create a new local repo and make 3 commits on `main`.
2. Create a `feature/add-readme` branch, make 2 commits.
3. Simulate a merge conflict: edit the same line in `main` and `feature/add-readme`. Resolve it.
4. Squash your 2 feature commits into 1 using `git rebase -i`.
5. Merge the feature into `main` with a merge commit.

---

## Expert Interview Q&A

**Q: You accidentally ran `git reset --hard HEAD~3` and lost 3 commits. How do you recover them?**
Run `git reflog` — it records every position HEAD has been at, including the commits before the reset. Find the commit hash from before the reset and run `git reset --hard <hash>` (or `git cherry-pick` the individual commits) to restore them. The reflog is local-only and expires eventually, so this isn't a permanent safety net, but it covers the vast majority of "oops" scenarios.

**Q: Why is `git push --force-with-lease` preferred over `git push --force` after a rebase?**
`--force` unconditionally overwrites the remote branch, even if someone else pushed commits you don't have locally — silently destroying their work. `--force-with-lease` checks that the remote branch is still at the commit you last saw before pushing; if someone else pushed in the meantime, it refuses and fails safely, forcing you to fetch and reconcile first.

**Q: GitFlow vs Trunk-Based Development — when would you pick one over the other?**
GitFlow suits products with scheduled/versioned releases (e.g., installed software, mobile apps with app-store review cycles) where you need a dedicated `release/*` branch to stabilize before shipping and `hotfix/*` for emergency patches to production. Trunk-based development suits continuous-delivery web services deploying multiple times a day — it minimizes merge conflicts and long-lived divergence, but requires strong CI, small PRs, and feature flags to hide incomplete work on `main`.

**Q: What's the practical difference between `git merge` and `git rebase` in terms of the resulting commit graph, and why does it matter for `git bisect`?**
Merge preserves the true chronological/branching history, including a merge commit — you can see exactly when and how branches diverged and reconverged. Rebase rewrites the feature commits to appear as if they were made sequentially after the latest main commit, producing a linear history. `git bisect` (binary-searching for the commit that introduced a bug) works cleanly on linear history; a history full of merge commits can make bisect land on a merge commit rather than the actual offending change, complicating root-cause analysis.
