---
name: skill-refactoring
description: Refactor bloated skill.md files using progressive disclosure pattern. Moves detailed content to references/ while keeping skill.md focused and discoverable. Use when a skill is approaching 500 lines or needs better organization.
---

# Skill Refactoring

Refactor bloated skill.md files to follow best practices using the progressive disclosure pattern.

## Platform Support

This skill works for both Claude Code and Codex skills:

- **Claude Code**: Skills located in `~/.claude/skills/`
- **Codex**: Skills located in `~/.codex/skills/`

Both platforms use the same `skill.md` format and 500-line limit.

## Purpose

This skill helps refactor large skill.md files into focused, maintainable skills that use reference files for detailed content. Official limit is 500 lines, but targeting shorter is better for context efficiency.

## When to Use This Skill

Use this skill when:
- **skill.md approaching 500 lines** - Official limit, consider splitting
- **Creating a new complex skill** - Start with good structure
- **Skill is hard to navigate** - Too much content in one file
- **Adding major new content** - Might push skill over limit
- **Reviewing existing skills** - Periodic maintenance

## Quick Start

```bash
# Check skill size
wc -l ~/.claude/skills/my-skill/skill.md

# If large or hard to navigate, invoke this skill:
# "Refactor the my-skill using progressive disclosure pattern"
```

## Reference Files

### 1. Methodology (`references/methodology.md`)
**Read this for:**
- Step-by-step refactoring process
- How to analyze and categorize content
- Creating reference file structure
- Testing and validation steps

### 2. Templates (`references/templates.md`)
**Read this for:**
- skill.md template
- Reference file template
- Quick start code block template
- Loading strategy examples

### 3. Best Practices (`references/best-practices.md`)
**Read this for:**
- Official guidance
- Progressive disclosure principles
- What goes in skill.md vs references/
- Well-structured skill patterns

## Loading Strategy

- **Always read** `methodology.md` when refactoring a skill
- **Read for templates** `templates.md` when creating new files
- **Read for guidance** `best-practices.md` when making decisions

## Key Principles

1. **Keep skill.md under 500 lines** - Official limit; shorter is better for context
2. **Move details to references/** - Implementation, examples, troubleshooting
3. **Include loading strategy** - Tell Claude when to read each reference
4. **Preserve all content** - Nothing gets deleted, just reorganized
5. **Don't create extraneous files** - No README.md, CHANGELOG.md, etc.

## Process Overview

1. **Analyze** - Read skill.md, identify sections
2. **Plan** - Design reference file structure
3. **Extract** - Move content to reference files
4. **Condense** - Create new focused skill.md
5. **Test** - Verify Claude can still find everything
6. **Document** - Update progress tracking

## Success Criteria

- [ ] skill.md is under 500 lines (shorter is better)
- [ ] All content preserved in references/
- [ ] Clear "when to read" guidance
- [ ] Loading strategy documented
- [ ] Quick start example included
- [ ] No extraneous files (README.md, etc.)

## Platform Support

Works for both Claude Code and Codex skills:
- **Claude Code**: Skills in `~/.claude/skills/`
- **Codex**: Skills in `~/.codex/skills/`

Both platforms use the same SKILL.md format and progressive disclosure pattern.
