# Agent Skills

Skills I've built for Claude Code and OpenAI Codex CLI workflows. Supports both platforms — some skills detect your environment and adapt accordingly.

## Skills

| Skill | Description | Platform |
|-------|-------------|----------|
| [branch-session](branch-session/) | Branch current session into a new tmux session using `--fork-session` (Claude Code) or equivalent (Codex). Creates a true fork with a new session ID while preserving conversation state. | Both |
| [agent-comms](agent-comms/) | Send messages between Claude Code/Codex sessions via tmux. Hand off debugging context, get second opinions. | Both |
| [ai-transcript-analyzer](ai-transcript-analyzer/) | Analyze transcripts using OpenAI API. Extract summaries, key insights, action items. | Both |
| [skill-refactoring](skill-refactoring/) | Refactor bloated skill.md files using progressive disclosure. Move detailed content to references/ while keeping skill.md focused. | Both |
| [todoist-cli](todoist-cli/) | Manage Todoist tasks via the `todoist` CLI. | Agnostic |
| [transcribe-and-analyze](transcribe-and-analyze/) | Local transcription with WhisperKit + AI analysis. | Agnostic |
| [alexa-cli](alexa-cli/) | Control Amazon Echo/Alexa devices via the `alexacli` CLI. | Agnostic |

## Installation

Copy a skill to your Claude Code skills directory:

```bash
git clone https://github.com/buddyh/agent-skills.git
cp -r agent-skills/branch-session ~/.claude/skills/
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
