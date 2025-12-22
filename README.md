# Claude Code Skills

Skills I've built for my own Claude Code workflows. Will update with more once I de-personalize them!

## Skills

| Skill | Description |
|-------|-------------|
| [branch-session](branch-session/) | Branch current session into a new tmux session using `--resume` with session ID. Explore alternative approaches without losing context. |
| [agent-comms](agent-comms/) | Send messages between Claude Code sessions via tmux. Hand off debugging context, get second opinions. |
| [ai-transcript-analyzer](ai-transcript-analyzer/) | Analyze transcripts using OpenAI API. Extract summaries, key insights, action items. |
| [skill-refactoring](skill-refactoring/) | Refactor bloated skill.md files using progressive disclosure. Move detailed content to references/ while keeping skill.md focused. |

## Installation

Copy a skill to your Claude Code skills directory:

```bash
git clone https://github.com/buddyh/claude-code-skills.git
cp -r claude-code-skills/branch-session ~/.claude/skills/
```

Make scripts executable:
```bash
chmod +x ~/.claude/skills/branch-session/scripts/*.sh
chmod +x ~/.claude/skills/agent-comms/scripts/*
```

## Requirements

- tmux (for branch-session, agent-comms)
- Python 3 + `openai` package (for ai-transcript-analyzer)

## License

MIT
