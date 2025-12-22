# Skill Refactoring Best Practices

> Part of the skill-refactoring skill
> Read skill.md for overview and when to use this reference

## Overview

This document compiles best practices from official Claude Code documentation and our analysis of well-structured skills.

---

## Official Claude Code Guidance

### Progressive Disclosure Principle

From the official docs:

> "Keep SKILL.md body to the essentials and under 500 lines to minimize context bloat."

**What this means:**
- skill.md should be under 500 lines (shorter is better for context efficiency)
- Detailed content lives in `references/*.md`
- Claude loads reference files "only when needed"
- Links from skill.md make content discoverable

### Core Documentation Points

1. **Skill Description** - Shows in skill picker, be specific about when to use
2. **Clear Purpose** - User knows immediately what skill does
3. **Reference Files** - Organize detailed content logically
4. **Progressive Loading** - Claude doesn't load everything upfront
5. **No Extraneous Files** - Don't create README.md, CHANGELOG.md, INSTALLATION_GUIDE.md, etc.

---

## Well-Structured Skill Pattern

### Effective skill.md Structure

```markdown
# Title & Description (5 lines)
## When to Use (5 lines)
## Reference Files (30-40 lines)
### Each ref file has:
  - What it contains
  - When to read it
## Loading Strategy (10 lines)
## Key Principles (10-15 lines)
```

**Why this works:**
1. **Immediately clear** - Purpose obvious in first 10 lines
2. **Well-organized** - Focused reference files, not one bloated file
3. **Guided navigation** - Tells Claude exactly when to read each file
4. **Self-documenting** - Loading strategy explains itself

### Key Patterns

**1. Reference File Descriptions:**
```markdown
### 1. Core Concepts (`references/core-concepts.md`)
**Read this for:**
- Main functionality explained
- Key patterns and approaches
- Foundational knowledge
```

Not just "Read `core-concepts.md`" - explain what's in it!

**2. Loading Strategy:**
```markdown
- **Always read** `core-concepts.md` when using this skill
- **Read when implementing** `examples.md` for code patterns
- **Read when debugging** `troubleshooting.md` for solutions
```

Active voice, specific triggers, clear purpose.

---

## Content Categorization

### What Goes in skill.md

✅ **Include:**
- **Purpose** (2-3 sentences) - Why this exists
- **When to use** (bullet points) - Trigger conditions
- **Quick start** (5-10 lines) - Minimal working example
- **Reference guide** (20-30 lines) - What's in each file + when to read
- **Loading strategy** (10-15 lines) - Which file for which task
- **Key principles** (5-8 bullets) - Most important things to remember

❌ **Don't include:**
- Complete API documentation
- Multiple detailed examples
- Step-by-step procedures
- Extensive troubleshooting
- Long code listings
- Historical context
- Implementation details

### What Goes in references/

✅ **Belongs in references:**
- **Implementation details** - How things actually work
- **Complete examples** - Full working code
- **API documentation** - Parameters, endpoints, responses
- **Error handling** - Specific error cases and fixes
- **Edge cases** - Unusual scenarios
- **Troubleshooting guides** - Systematic debugging
- **Best practices** - Detailed guidelines
- **Advanced topics** - Optimization, complex patterns

---

## Reference File Organization

### Number of Files: Sweet Spot

**Too few (1-2 files):**
- Each file becomes bloated
- Hard to find specific information
- Load unnecessary content

**Too many (10+ files):**
- Navigation becomes complex
- Overhead in file management
- Content too fragmented

**Just right (4-7 files):**
- Each file focused on one topic
- Easy to navigate
- Clear organization
- Manageable maintenance

### Common Reference File Sets

**For API/Integration Skills:**
1. `authentication.md` - Auth methods, tokens
2. `endpoints.md` or `api-reference.md` - API details
3. `examples.md` - Working code
4. `error-handling.md` - Errors and retries
5. `troubleshooting.md` - Common issues

**For Tool/Library Skills:**
1. `core-concepts.md` - Main functionality
2. `usage-patterns.md` - Common patterns
3. `examples.md` - Code samples
4. `configuration.md` - Setup and options
5. `troubleshooting.md` - Issues and fixes

**For Framework Skills:**
1. `architecture.md` - System design
2. `implementation.md` - How to build features
3. `examples.md` - Real implementations
4. `best-practices.md` - Recommended patterns
5. `advanced.md` - Edge cases, optimization

### File Naming Conventions

**Good names:**
- Specific: `authentication.md` not `auth.md`
- Descriptive: `common-endpoints.md` not `endpoints.md`
- Action-oriented: `error-handling.md` not `errors.md`
- Clear purpose: `usage-patterns.md` not `patterns.md`

**Avoid:**
- Vague: `misc.md`, `other.md`, `stuff.md`
- Sequential: `part1.md`, `part2.md`
- Redundant: `reference.md` (they're all references)
- Abbreviations: `auth.md`, `cfg.md` (spell it out)

---

## Loading Strategy Patterns

### Active Voice + Specific Triggers

**Good:**
```markdown
- **Always read** `core.md` when using this skill
- **Read when implementing** `examples.md` for code patterns
- **Read when errors occur** `troubleshooting.md` for solutions
- **Read for specifics** `api-reference.md` for endpoint details
```

**Why it works:**
- Active voice ("Read when")
- Specific triggers ("when errors occur")
- Clear purpose ("for solutions")

**Avoid:**
```markdown
- `core.md` - Core concepts
- `examples.md` - Examples
- `troubleshooting.md` - Help with issues
```

**Why it's weak:**
- Passive listing
- No trigger conditions
- Vague purpose

### Common Trigger Patterns

**Frequency-based:**
- **Always read** - Essential for any use
- **Usually read** - Needed for most tasks
- **Sometimes read** - Specific scenarios
- **Rarely read** - Edge cases only

**Task-based:**
- **Read when implementing** - Building something
- **Read when debugging** - Fixing issues
- **Read when learning** - First time usage
- **Read for reference** - Looking up specifics

**Scenario-based:**
- **Read when errors occur** - Troubleshooting
- **Read for advanced cases** - Complex scenarios
- **Read for optimization** - Performance tuning
- **Read for integration** - Connecting to other systems

---

## Quick Start Examples

### What Makes a Good Quick Start

✅ **Good Quick Start:**
- **5-10 lines of code**
- **Actually runs** - Can copy-paste and execute
- **Shows the essence** - Core functionality
- **Has comments** - Explains what's happening
- **Includes output** - Shows expected result
- **Links to more** - Points to examples.md

Example:
```python
# Quick Start: Send a message

from module import Client

client = Client(api_key="your_key")
response = client.send("Hello world")
print(response.status)  # "sent"

# For complete examples, see references/examples.md
```

❌ **Bad Quick Start:**
```python
# See references/examples.md for usage
```

Empty! Not helpful!

❌ **Also Bad:**
```python
# Production-ready example with error handling,
# retry logic, logging, configuration management,
# connection pooling, and graceful degradation...
[50 lines of code]
```

Too complex! That belongs in references/examples.md

---

## Testing Refactored Skills

### Manual Testing Checklist

After refactoring:

- [ ] **Read skill.md** - Can you understand the skill?
- [ ] **Check line count** - Under 500 lines?
- [ ] **Verify links** - All reference file links work?
- [ ] **Test with Claude** - Give it a task using the skill
- [ ] **Check loading** - Does Claude load only needed files?
- [ ] **Find information** - Can Claude locate content in references?
- [ ] **Run quick start** - Does the example work?
- [ ] **Compare before/after** - All content preserved?

### Claude Testing Scenarios

**Test 1: Understanding**
```
Prompt: "Explain what the [skill-name] skill does"
Expected: Claude describes it from skill.md alone
```

**Test 2: Basic Usage**
```
Prompt: "Use [skill-name] to [common task]"
Expected: Claude completes task, loads appropriate references
```

**Test 3: Specific Information**
```
Prompt: "How do I [specific thing from reference file]?"
Expected: Claude finds and uses the right reference file
```

**Test 4: Troubleshooting**
```
Prompt: "I'm getting [error]. Help me debug."
Expected: Claude loads troubleshooting.md, finds solution
```

---

## Common Pitfalls & Solutions

### Pitfall 1: Moving Too Little Content

**Symptom:** skill.md still bloated after "refactoring"

**Cause:** Being too conservative about what to move

**Solution:**
- If it's implementation details → references/
- If it's a complete example → references/examples.md
- If it's troubleshooting → references/troubleshooting.md
- If it's API docs → references/api-reference.md

**Rule of thumb:** When in doubt, move it to references

### Pitfall 2: Creating Too Many Tiny Files

**Symptom:** 15 reference files with 20 lines each

**Cause:** Over-splitting content

**Solution:**
- Combine related topics
- Aim for 4-7 reference files
- Each file should be 100-300 lines
- Better to have substantial sections than many tiny files

### Pitfall 3: Vague File Names

**Symptom:** Files named `info.md`, `more.md`, `part2.md`

**Cause:** Not thinking about discoverability

**Solution:**
- Name files by topic: `authentication.md`
- Be specific: `common-endpoints.md` not `endpoints.md`
- Action-oriented: `error-handling.md` not `errors.md`

### Pitfall 4: No Loading Strategy

**Symptom:** Just listing reference files without guidance

**Cause:** Forgetting that Claude needs context

**Solution:**
- Add "Loading Strategy" section to skill.md
- Explain when to read each file
- Use active voice and specific triggers
- Make it clear what's in each file

### Pitfall 5: Deleting Content

**Symptom:** Original skill.md had 800 lines, new one + references total 600

**Cause:** Removing "outdated" or "irrelevant" content

**Solution:**
- Preserve ALL original content
- If unsure about relevance, move to references/archive.md
- Update outdated content rather than deleting
- Review with user before removing anything

### Pitfall 6: No Quick Start

**Symptom:** skill.md says "See examples.md for usage"

**Cause:** Moving ALL examples to references

**Solution:**
- Keep ONE minimal example in skill.md
- Make it 5-10 lines max
- Should be copy-pastable and runnable
- Link to references/examples.md for more

### Pitfall 7: Forgetting Cross-Links

**Symptom:** Reference files don't link to each other

**Cause:** Treating each file as isolated

**Solution:**
- Add "Related References" section to each file
- Link authentication.md ↔ examples.md
- Link error-handling.md ↔ troubleshooting.md
- Help users navigate between related content

---

## Maintenance After Refactoring

### When to Update skill.md

**Rarely.** Only when:
- Purpose changes
- New major reference file added
- Loading strategy changes
- Quick start example needs update

**Most updates go to reference files.**

### When to Update Reference Files

**Frequently.** This is where active development happens:
- New API endpoints → Update `api-reference.md`
- New examples → Update `examples.md`
- New error discovered → Update `troubleshooting.md`
- New best practice → Update `best-practices.md`

### Preventing Re-Bloat

**Monthly check:**
```bash
wc -l ~/.claude/skills/*/skill.md | sort -rn | head -10
```

If any skill.md is getting large, investigate:
- Has new content been added to skill.md?
- Should it be moved to references?
- Is a new reference file needed?

**Quarterly review:**
- Check each skill's structure
- Look for duplicate content
- Consolidate where appropriate
- Update loading strategies if needed

---

## Metrics for Success

### Individual Skill Metrics

After refactoring a skill:

✅ **Structure:**
- skill.md: Under 500 lines (shorter is better for context)
- References: As needed, keep one level deep
- Files over 100 lines: Include table of contents

✅ **Content:**
- Purpose clear in first 10 lines
- Quick start example present
- All original content preserved
- Clear "when to read" guidance

✅ **Functionality:**
- Claude can use the skill
- Claude loads only needed files
- Users can find information
- Examples work correctly

### Overall Skill Library Metrics

Track improvements after refactoring:
- Average skill.md line count (target: well under 500)
- Percentage of skills using references/
- Reduction in initial context load

---

## Key Takeaways

1. **Under 500 lines for skill.md** - Official limit; shorter is better
2. **Use references/ for detailed content** - Keep skill.md focused
3. **Always include loading strategy** - Claude needs guidance on when to read what
4. **Preserve all content** - Never delete, only reorganize
5. **No extraneous files** - No README.md, CHANGELOG.md, etc.
6. **Only name and description in frontmatter** - No tags or other fields
7. **Progressive disclosure** - Load only what's needed
8. **Make it discoverable** - Clear navigation and descriptions

---

## Related References

- See `methodology.md` for the step-by-step refactoring process
- See `templates.md` for copy-paste templates
- Official docs: https://code.claude.com/docs/en/skills.md
