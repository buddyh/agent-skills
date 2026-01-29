---
name: project-spawn
description: Spawn a new Claude Code or Codex session in a project directory with context handoff. This skill should be used when discussion shifts to a different project/repo and the user wants to work on it in a dedicated session. Creates a handoff document with relevant context from the current conversation, then launches a new tmux session ready to continue.
---

# Project Spawn

## Overview

Transfer context from the current conversation to a new session in a different project directory. This enables seamless context handoff when pivoting from a general session to focused project work.

## Platform Support

- **Claude Code**: Uses `~/.claude/projects/` for session storage, `claude` CLI
- **Codex**: Uses `~/.codex/sessions/` for session storage, `codex` CLI

The handoff workflow is similar on both platforms.

## Workflow

### Step 1: Resolve Target Project

Determine the target project directory:

1. **If explicit path provided**: Use directly (e.g., `~/repos/my-project`)
2. **If relative path provided**: Resolve from current working directory
3. **If no target specified**: Ask the user which project they want to work on

### Step 1b: Handle Non-Existent Directory

If target directory doesn't exist, ask user:

> "Directory `<path>` doesn't exist. Want me to create it?"
> - Create folder only
> - Create folder + init git repo
> - Create folder + init git + create GitHub repo (public)
> - Create folder + init git + create GitHub repo (private)
> - Cancel

Create as requested before proceeding to Step 2.

### Step 2: Extract Relevant Context

Analyze the last 5-10 messages for content relevant to the target project:

- Tasks or work items discussed
- Specific files, scripts, or features mentioned
- Decisions made or questions raised
- Any errors or issues identified
- Uncommitted changes noted

Focus only on information relevant to the target project, not the entire conversation.

### Step 3: Create Handoff Document

Write `PROJECT_HANDOFF.md` to the target project directory:

```markdown
# Project Handoff - [DATE] [TIME]

## Context
[Why this handoff is happening - what triggered the pivot]

## Discussion Summary
[Relevant context extracted from conversation]

## Specific Tasks/Questions
- [Actionable items identified]

## Files/Areas Mentioned
- [Specific files or code areas referenced]

## Suggested Starting Point
[What to do first in this session]
```

### Step 4: Launch Session

**Claude Code:**
```bash
~/.claude/skills/project-spawn/scripts/spawn_session.sh "<project-path>" "<session-name>"
```

**Codex:**
```bash
codex --cd "<project-path>" "Read PROJECT_HANDOFF.md and continue with the tasks described there."
```

### Step 5: Confirm to User

Report:
```
Spawned: <session-name>
Directory: <project-path>
Handoff: PROJECT_HANDOFF.md created

To attach: tmux attach -t <session-name>
```

## Quick Reference

**Invocation**: `/spawn <project-path>` or mention wanting to work on a different project

**Session naming**: Uses repo folder name (e.g., `my-project`)

**Handoff location**: `<project-dir>/PROJECT_HANDOFF.md`

## Setup

```bash
chmod +x ~/.claude/skills/project-spawn/scripts/*.sh
```

## Resources

### scripts/
- `spawn_session.sh` - Creates tmux session and launches Claude Code with handoff context
