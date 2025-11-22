# Git Operations: Setting Up a Clean "learn" Branch

**Date**: 2025-11-22
**File**: `/Users/hai/hub/big/anthropics/claude-agent-sdk/session_summaries/2025_11_22_git_clean_learn_branch_09_15.md`

---

## Overview

Learned how to set up a clean branch workflow where `main` stays in sync with upstream (Anthropic) and all personal work lives on a separate `learn` branch.

---

## Git Operations Performed

### 1. Set Up Dual Remotes

```bash
git remote add upstream https://github.com/anthropics/claude-agent-sdk-python.git
```

**Result:**
```
origin    → https://github.com/hw92/claude-agent-sdk-python.git (your fork)
upstream  → https://github.com/anthropics/claude-agent-sdk-python.git (official)
```

### 2. Sync Main with Upstream

```bash
# Fetch all updates
git checkout main
git fetch upstream
git fetch origin

# Discard local changes and reset to upstream
git restore .gitignore
git reset --hard upstream/main
```

**Result:** `main` branch now exactly matches Anthropic's official repo.

### 3. Create Clean Learn Branch

```bash
git checkout -b learn
```

**Result:** New branch `learn` created from clean `main`.

### 4. Add and Commit Lab Files

```bash
git add lab/ session_summaries/
git commit -m "lab: initial learning environment setup"
```

**Files committed:**
- `lab/README.md`
- `lab/agents/01_simple_agent.py`
- `lab/agents/02_multi_agent.py`
- `lab/streaming/01_basic_streaming.py`
- `lab/streaming/02_multi_turn.py`
- `lab/tools/01_simple_calculator.py`
- `lab/tools/02_basic_query.py`
- `session_summaries/2025_11_22_claude_sdk_lab_setup_08_45.md`

### 5. Push to Fork

```bash
git push origin learn
```

**Result:** `learn` branch now on GitHub fork.

---

## Final Branch Structure

| Branch | Purpose | Tracks |
|--------|---------|--------|
| `main` | Clean, never commit here | `upstream/main` (Anthropic) |
| `learn` | All personal work/experiments | `origin/learn` (your fork) |

---

## Key Learnings

1. **`git reset --hard upstream/main`** - Resets local branch to match upstream exactly
2. **`git restore <file>`** - Discards uncommitted changes to a file
3. **Dual remotes** - `origin` for your fork, `upstream` for official repo
4. **Branch isolation** - Keep `main` clean, work on feature branches

---

## Workflow Reference

### Daily Work
```bash
git checkout learn
# ... make changes ...
git add .
git commit -m "lab: description"
git push origin learn
```

### Sync with Upstream
```bash
# Update main
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

# Rebase learn on latest
git checkout learn
git rebase main
git push origin learn --force-with-lease
```

---

## Commands Summary

| Command | Purpose |
|---------|---------|
| `git remote add upstream <url>` | Add official repo as upstream |
| `git fetch upstream` | Get latest from upstream |
| `git reset --hard upstream/main` | Reset branch to match upstream |
| `git checkout -b <branch>` | Create and switch to new branch |
| `git push origin <branch>` | Push branch to your fork |
