---
name: branch-session
description: Branch the current Claude Code or Codex session into a new tmux session. Creates a parallel conversation that can diverge independently. Use when you want to explore an alternative approach without losing your current context.
---

# Branch Session

## Overview

Create a "branch" of the current conversation by spawning a new tmux session that continues from the same session. Both sessions can then diverge independently. The original session remains untouched.

## Platform Support

- **Claude Code**: Uses `claude --continue <session-id>` to resume from the same session
- **Codex**: Uses `codex resume <session-id>` to resume from the same session

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
```bash
# Find recent session files
ls -t ~/.codex/sessions/$(date +%Y/%m/%d)/*.jsonl 2>/dev/null | head -5
```

### Step 2: Generate Branch Name

Create a unique session name:
```bash
SHORT_ID=$(echo "$SESSION_ID" | cut -c1-5)
TIMESTAMP=$(date +%H%M)
BRANCH_NAME="branch-${SHORT_ID}-${TIMESTAMP}"
```

### Step 3: Execute Branch

Run the branch script:
```bash
~/.claude/skills/branch-session/scripts/branch_session.sh "$PWD" "$SESSION_ID" "$BRANCH_NAME"
```

The script creates a new tmux session and launches the agent with session context:

- **Claude Code**: `claude --continue $SESSION_ID`
- **Codex**: `codex resume $SESSION_ID`

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

Make the script executable (one-time):
```bash
chmod +x ~/.claude/skills/branch-session/scripts/*.sh
```

## Requirements

- tmux installed and running
- Claude Code CLI (`claude`) or Codex CLI (`codex`)
- Active session to branch from

## Resources

### scripts/
- `branch_session.sh` - Creates tmux session and continues from current session
