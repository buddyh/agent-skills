# Agent Skills

Skills for Claude Code and OpenAI Codex CLI workflows. Supports both platforms -- most skills detect your environment and adapt accordingly.

## Skills

| Skill | Description | Platform |
|-------|-------------|----------|
| [deep-dive](deep-dive/) | Comprehensive research reports via parallel subtopic decomposition. Scales depth dynamically (4,000-10,000+ words, 40-100+ sources). | Agnostic |
| [project-spawn](project-spawn/) | Spawn a new session in a project directory with context handoff. Creates handoff document and launches a new tmux session. | Claude & Codex |
| [branch-session](branch-session/) | Branch current session into a new tmux session using `--continue` (Claude Code) or `resume` (Codex). Creates a parallel conversation that can diverge independently. | Claude & Codex |
| [agent-comms](agent-comms/) | Send messages between Claude Code/Codex sessions via tmux. Hand off debugging context, get second opinions. | Claude & Codex |
| [skill-refactoring](skill-refactoring/) | Refactor bloated skill.md files using progressive disclosure. Move detailed content to references/ while keeping skill.md focused. | Claude & Codex |
| [todoist-cli](todoist-cli/) | Manage Todoist tasks via the `todoist` CLI. | Agnostic |
| [transcribe-and-analyze](transcribe-and-analyze/) | Local transcription with WhisperKit + AI analysis. | Agnostic |
| [alexa-cli](alexa-cli/) | Control Amazon Echo/Alexa devices via the `alexacli` CLI. | Agnostic |

## Installation

Copy a skill to your skills directory:

```bash
git clone https://github.com/buddyh/agent-skills.git

# Claude Code
cp -r agent-skills/deep-dive ~/.claude/skills/

# Codex
cp -r agent-skills/deep-dive ~/.codex/skills/
```

Make scripts executable (for skills that include them):
```bash
chmod +x ~/.claude/skills/branch-session/scripts/*.sh
chmod +x ~/.claude/skills/agent-comms/scripts/*
chmod +x ~/.claude/skills/project-spawn/scripts/*.sh
```

## Requirements

- tmux (for branch-session, agent-comms, project-spawn)
- Python 3 + `openai` package (for ai-transcript-analyzer)

## License

MIT
