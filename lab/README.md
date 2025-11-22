# Lab Experiments

This directory contains learning experiments and explorations with the Claude Agent SDK.

## Structure

```
lab/
├── tools/       # Custom tool experiments and examples
├── agents/      # Agent pattern experiments
├── streaming/   # Streaming response experiments
└── README.md    # This file
```

## Guidelines

- **Branch**: All experiments live on the `lab/learn` branch
- **Safety**: This is a safe space to break things and learn
- **Tracking**: Document interesting findings in dated markdown files
- **Cleanup**: Feel free to delete failed experiments

## Workflow

```bash
# You're already on lab/learn branch
git branch --show-current  # Should show: lab/learn

# Work in any folder
cd lab/tools/
# ... create experiments ...

# Commit your work
git add lab/
git commit -m "lab: experiment with custom calculator tool"

# Push to your fork (optional)
git push origin lab/learn
```

## Sync with Upstream

```bash
# Get latest from official Anthropic repo
git checkout main
git fetch upstream
git merge upstream/main

# Rebase your lab work
git checkout lab/learn
git rebase main
```

## Notes

- Keep `main` branch clean (never commit directly to it)
- All Python cache files are already gitignored
- Add `.env` files to `.gitignore` if using secrets
