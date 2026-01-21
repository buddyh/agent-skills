#!/bin/bash
# Branch a Claude Code session into a new tmux session
# Usage: branch_session.sh <directory> <session-id> <new-session-name>

set -e

DIRECTORY="$1"
SESSION_ID="$2"
NEW_SESSION_NAME="$3"

if [ -z "$DIRECTORY" ] || [ -z "$SESSION_ID" ] || [ -z "$NEW_SESSION_NAME" ]; then
    echo "Usage: branch_session.sh <directory> <session-id> <new-session-name>"
    exit 1
fi

# Expand ~ if present
DIRECTORY="${DIRECTORY/#\~/$HOME}"

# Validate directory exists
if [ ! -d "$DIRECTORY" ]; then
    echo "Error: Directory does not exist: $DIRECTORY"
    exit 1
fi

# Check if session already exists
if tmux has-session -t "$NEW_SESSION_NAME" 2>/dev/null; then
    echo "Session '$NEW_SESSION_NAME' already exists."
    echo "To attach: tmux attach -t $NEW_SESSION_NAME"
    exit 0
fi

# Create new tmux session (detached)
tmux new-session -d -s "$NEW_SESSION_NAME" -c "$DIRECTORY"

# Wait for shell to be ready
sleep 0.5

# Start Claude Code with --resume --fork-session (creates new session ID)
tmux send-keys -t "$NEW_SESSION_NAME" "claude --resume $SESSION_ID --fork-session" C-m

# Wait for Claude to initialize
sleep 3

# Send initial message to indicate this is a branch
tmux send-keys -t "$NEW_SESSION_NAME" "this is now a branch of this conversation" C-m

echo "Branched session: $NEW_SESSION_NAME"
echo "Directory: $DIRECTORY"
echo "Resuming: $SESSION_ID"
echo ""
echo "To attach: tmux attach -t $NEW_SESSION_NAME"
