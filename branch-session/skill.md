---
name: branch-session
description: Branch the current Claude Code or Codex session into a new tmux session. Creates a true fork with a new session ID while preserving conversation state. Use when you want to explore an alternative approach without losing your current context.
---

# Branch Session

## Overview

Create a "branch" of the current conversation by spawning a new tmux session with a forked session. Uses platform-specific fork commands to create a true fork with a new session ID while preserving conversation state. The original session remains untouched.

## Platform Detection

This skill automatically detects your environment:

- **Claude Code**: Uses `~/.claude/projects/` session files
- **Codex**: Uses `~/.codex/sessions/` and the `codex fork` command

## Workflow

### Step 1: Get Current Session ID

**Claude Code:**
1. Get current working directory
2. Convert to Claude project path format:
   ```bash
   # /home/user/projects/myapp -> -home-user-projects-myapp
   PROJECT_PATH=$(echo "$PWD" | sed 's|/|-|g' | sed 's|^-||')
   ```
3. Find most recently modified session file:
   ```bash
   SESSION_FILE=$(ls -t ~/.claude/projects/$PROJECT_PATH/*.jsonl 2>/dev/null | head -1)
   SESSION_ID=$(basename "$SESSION_FILE" .jsonl)
   ```

**Codex:**
1. Find session IDs from the sessions folder:
   ```bash
   ls -t ~/.codex/sessions/*.jsonl | head -5
   ```
2. Or use `codex fork --last` to fork the most recent session directly

### Step 2: Generate Branch Name

Create a unique session name:
```bash
SHORT_ID=$(echo "$SESSION_ID" | cut -c1-5)
TIMESTAMP=$(date +%H%M)
BRANCH_NAME="branch-${SHORT_ID}-${TIMESTAMP}"
```

### Step 3: Execute Branch

**Claude Code:**
```bash
~/.claude/skills/branch-session/scripts/branch_session.sh "$PWD" "$SESSION_ID" "$BRANCH_NAME"
```

**Codex:**
```bash
# Fork most recent session (simplest)
codex fork --last

# Or fork a specific session
codex fork <SESSION_ID>
```

### Step 4: Confirm

Report to user:
```
Branched session: branch-a1b2c-1508
Directory: /home/user/projects/myapp
Resuming: a1b2c3d4-da03-4ece-8625-582be89f6dff

To attach: tmux attach -t branch-a1b2c-1508
```

## Quick Reference

**Invocation**: `/branch`

**Session naming**: `branch-<first-5-chars-of-id>-<HHMM>`

**Use cases**:
- Explore alternative implementation approaches
- Test something risky without losing progress
- Split work into parallel tracks

## Setup

Make the scripts executable (one-time):
```bash
chmod +x ~/.claude/skills/branch-session/scripts/*.sh
```

## Requirements

- tmux installed and running
- **Claude Code**: `claude` CLI available
- **Codex**: `codex` CLI available
- Active session to branch from

## Resources

### scripts/
- `branch_session.sh` - Creates tmux session and resumes Claude Code
