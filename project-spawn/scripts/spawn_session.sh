#!/bin/bash
# Spawn a new tmux session with Claude Code for project handoff
# Usage: spawn_session.sh <project-path> <session-name>

set -e

PROJECT_PATH="$1"
SESSION_NAME="$2"

if [ -z "$PROJECT_PATH" ] || [ -z "$SESSION_NAME" ]; then
    echo "Usage: spawn_session.sh <project-path> <session-name>"
    exit 1
fi

# Expand ~ if present
PROJECT_PATH="${PROJECT_PATH/#\~/$HOME}"

# Validate directory exists
if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Directory does not exist: $PROJECT_PATH"
    exit 1
fi

# Check if session already exists
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
    echo "Session '$SESSION_NAME' already exists. Attaching..."
    echo "To attach: tmux attach -t $SESSION_NAME"
    exit 0
fi

# Create new tmux session (detached)
tmux new-session -d -s "$SESSION_NAME" -c "$PROJECT_PATH"

# Wait for shell to be ready
sleep 0.5

# Start Claude Code
tmux send-keys -t "$SESSION_NAME" "claude" C-m

# Wait for Claude to initialize
sleep 3

# Send initial prompt to read handoff
tmux send-keys -t "$SESSION_NAME" "Read PROJECT_HANDOFF.md for context on what I'm working on. Summarize what you understand and then begin working through the implementation plan." C-m

echo "Spawned: $SESSION_NAME"
echo "Directory: $PROJECT_PATH"
echo ""
echo "To attach: tmux attach -t $SESSION_NAME"
