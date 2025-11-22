# Session Summary: Claude Agent SDK Lab Setup

**Date**: 2025-11-22
**File**: `/Users/hai/hub/big/anthropics/claude-agent-sdk/session_summaries/2025_11_22_claude_sdk_lab_setup_08_45.md`

---

## Overview

Set up a safe learning environment for experimenting with the Claude Agent SDK without modifying the original repository. Created a lab folder structure and simple learning examples.

---

## Activities

### 1. Repository Strategy Discussion

**Goal**: Learn and experiment with the Claude Agent SDK without affecting the original repo.

**Solution**: Fork + Feature Branch workflow with folder-based organization.

**Key decisions**:
- Use dual remotes (`origin` for fork, `upstream` for official Anthropic repo)
- Stay on single `lab/learn` branch (simpler than multiple branches)
- Organize experiments in folders rather than branches

### 2. Git Environment Setup

**Configured remotes**:
```
origin    → https://github.com/hw92/claude-agent-sdk-python.git (your fork)
upstream  → https://github.com/anthropics/claude-agent-sdk-python.git (official)
```

**Created branch**: `lab/learn`

### 3. Lab Folder Structure Created

```
lab/
├── README.md           # Lab usage guide
├── tools/              # Custom tool experiments
├── agents/             # Agent pattern experiments
└── streaming/          # Streaming response experiments
```

### 4. Learning Examples Created

| File | Purpose |
|------|---------|
| `lab/tools/01_simple_calculator.py` | MCP tools with `@tool` decorator |
| `lab/tools/02_basic_query.py` | Simplest `query()` function usage |
| `lab/agents/01_simple_agent.py` | Custom agent definitions |
| `lab/agents/02_multi_agent.py` | Multiple agents working together |
| `lab/streaming/01_basic_streaming.py` | `ClaudeSDKClient` streaming pattern |
| `lab/streaming/02_multi_turn.py` | Multi-turn conversations |

### 5. Updated .gitignore

Added optional rules for lab folder outputs (commented out by default).

---

## Key Outcomes

- Safe isolated environment on `lab/learn` branch
- Dual remote setup for syncing with upstream
- 6 simple learning examples covering core SDK patterns
- Clear documentation in `lab/README.md`

---

## Recommended Learning Path

1. `tools/02_basic_query.py` - Start with simplest query
2. `streaming/01_basic_streaming.py` - Learn streaming client
3. `streaming/02_multi_turn.py` - Multi-turn conversations
4. `agents/01_simple_agent.py` - Custom agents
5. `agents/02_multi_agent.py` - Multiple agents
6. `tools/01_simple_calculator.py` - Custom MCP tools

---

## Next Steps

- [ ] Install SDK: `pip install -e .`
- [ ] Run examples to verify setup
- [ ] Experiment with modifying examples
- [ ] Explore more patterns in `examples/` directory
- [ ] Commit work: `git add lab/ && git commit -m "lab: initial setup"`

---

## Commands Reference

```bash
# Run examples
python lab/tools/02_basic_query.py

# Save your work
git add lab/
git commit -m "lab: description of experiment"
git push origin lab/learn

# Sync with official repo
git fetch upstream
git checkout main
git merge upstream/main
git checkout lab/learn
git rebase main
```
