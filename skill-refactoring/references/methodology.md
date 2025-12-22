# Skill Refactoring Methodology

> Part of the skill-refactoring skill
> Read skill.md for overview and when to use this reference

## Overview

This document provides the step-by-step process for refactoring bloated skill.md files into well-structured skills that use progressive disclosure.

---

## Step 1: Analyze Current Skill

### 1.1 Read the Entire skill.md

```bash
# Check line count
wc -l ~/.claude/skills/SKILL_NAME/skill.md

# Read the file
cat ~/.claude/skills/SKILL_NAME/skill.md
```

### 1.2 Identify Major Sections

Look for logical groupings:
- Core concepts/principles
- Implementation details
- API/function references
- Examples and patterns
- Error handling
- Troubleshooting
- Configuration
- Best practices

### 1.3 Categorize Content

For each section, ask:

**Essential (stays in skill.md):**
- [ ] Explains the skill's purpose?
- [ ] Describes when to use it?
- [ ] Provides navigation to details?
- [ ] Includes minimal quick start?

**Reference (moves to references/):**
- [ ] Deep implementation details?
- [ ] Multiple code examples?
- [ ] API/endpoint documentation?
- [ ] Step-by-step guides?
- [ ] Troubleshooting procedures?
- [ ] Advanced/edge case content?

---

## Step 2: Plan Reference File Structure

### 2.1 Common Reference File Patterns

Choose files based on content type:

**For API/Integration Skills:**
```
references/
├── authentication.md      # Auth patterns, tokens, credentials
├── endpoints.md           # API reference, parameters
├── examples.md            # Working code samples
└── error-handling.md      # Common errors, retries
```

**For Tool/Library Skills:**
```
references/
├── core-concepts.md       # Main functionality, how it works
├── usage-patterns.md      # Common use cases, patterns
├── examples.md            # Complete working examples
├── configuration.md       # Setup, options, customization
└── troubleshooting.md     # Common issues, solutions
```

**For Framework Skills:**
```
references/
├── architecture.md        # System design, components
├── implementation.md      # How to implement features
├── examples.md            # Real-world implementations
├── best-practices.md      # Recommended patterns
└── advanced.md            # Edge cases, optimization
```

**For Meta/Process Skills:**
```
references/
├── methodology.md         # Step-by-step process
├── templates.md           # Reusable templates
├── best-practices.md      # Guidelines and principles
└── examples.md            # Sample applications
```

### 2.2 Reference File Naming Guidelines

**Good names:**
- `authentication.md` (specific, clear)
- `common-endpoints.md` (describes content)
- `error-handling.md` (action-oriented)
- `usage-patterns.md` (clear purpose)

**Avoid:**
- `misc.md` (too vague)
- `part2.md` (not descriptive)
- `stuff.md` (meaningless)
- `reference.md` (redundant - they're all references)

---

## Step 3: Create New skill.md Structure

### 3.1 Use the Standard Template

See `templates.md` for the complete skill.md template.

### 3.2 Essential Sections

Every skill.md should have:

1. **Frontmatter** (YAML) - Only name and description, no other fields
   ```yaml
   ---
   name: skill-name
   description: Clear description including when to use this skill
   ---
   ```

2. **Title and Purpose** (2-3 sentences)
   ```markdown
   # Skill Name

   Brief description of what this skill does and why it exists.
   ```

3. **When to Use** (bullet points)
   ```markdown
   ## When to Use This Skill

   - Use case 1
   - Use case 2
   - Use case 3
   ```

4. **Quick Start** (5-10 lines of code)
   ```markdown
   ## Quick Start

   \`\`\`language
   # Minimal working example
   code here
   \`\`\`
   ```

5. **Reference Files** (with when-to-read guidance)
   ```markdown
   ## Reference Files

   ### 1. File Name (`references/file.md`)
   **Read this for:**
   - Topic A
   - Topic B
   ```

6. **Loading Strategy**
   ```markdown
   ## Loading Strategy

   - **Always read** `file1.md` when doing X
   - **Read when** `file2.md` for Y scenarios
   ```

7. **Key Principles** (3-5 bullet points)
   ```markdown
   ## Key Principles

   - Most important thing 1
   - Most important thing 2
   ```

### 3.3 Target Length

- **Official limit:** 500 lines
- **Shorter is better** for context efficiency
- **If approaching limit:** Move more content to references

---

## Step 4: Extract Content to Reference Files

### 4.1 Create references/ Directory

```bash
mkdir -p ~/.claude/skills/SKILL_NAME/references
```

### 4.2 Move Content Systematically

For each planned reference file:

1. **Create the file**
   ```bash
   touch ~/.claude/skills/SKILL_NAME/references/topic.md
   ```

2. **Add header** (see templates.md)
   ```markdown
   # Topic Name

   > Part of the SKILL_NAME skill
   > Read skill.md for overview and when to use this reference
   ```

3. **Copy relevant content** from old skill.md
4. **Add structure** (headers, examples, sections)
5. **Add cross-links** to other reference files if needed

### 4.3 Organize Content Logically

Within each reference file:
- **Start with overview** - What this file covers
- **Use clear headers** - Make scanning easy
- **Include examples** - Show, don't just tell
- **Link related content** - Cross-reference other files
- **Keep focused** - One topic per file

### 4.4 Preserve All Information

**Critical:** No content should be deleted during refactoring.

If you find:
- Outdated information → Move to references/archive.md or update it
- Duplicate information → Consolidate in one place, link from others
- Unclear relevance → Create references/misc.md temporarily, review later

---

## Step 5: Test and Validate

### 5.1 Manual Checks

```bash
# Check new skill.md line count
wc -l ~/.claude/skills/SKILL_NAME/skill.md

# Verify all reference files exist
ls -la ~/.claude/skills/SKILL_NAME/references/

# Verify links in skill.md
grep "references/" ~/.claude/skills/SKILL_NAME/skill.md
```

### 5.2 Test with Claude

Ask Claude to:
1. **Explain the skill** - Can it understand from skill.md alone?
2. **Use the skill** - Give it a task requiring references
3. **Find specific info** - Ask about content in reference files
4. **Check loading** - Verify it loads only needed references

### 5.3 Validation Checklist

- [ ] skill.md is under 500 lines (shorter is better)
- [ ] All original content preserved somewhere
- [ ] Reference files have clear names
- [ ] Links in skill.md work correctly
- [ ] "When to read" guidance is clear
- [ ] Loading strategy section exists
- [ ] Quick start example is present
- [ ] No extraneous files (README.md, CHANGELOG.md, etc.)
- [ ] Only name and description in frontmatter
- [ ] Claude can successfully use the skill

---

## Step 6: Document Changes

### 6.1 Update REFACTORING-PROGRESS.md

Add entry:

```markdown
### Skill Name (YYYY-MM-DD)
**Before:** XXX lines
**After:** YY lines
**Reduction:** ZZ%

**Changes Made:**
- Created references/file1.md (moved X content)
- Created references/file2.md (moved Y content)
- Condensed skill.md to focus on navigation

**Files Created:**
- references/topic1.md (150 lines)
- references/topic2.md (200 lines)

**Issues Encountered:**
- Issue 1 and how it was resolved

**Testing Results:**
- Claude successfully used skill: ✓
- All references loaded correctly: ✓
- No content lost: ✓

**Lessons Learned:**
- Insight 1
- Insight 2
```

### 6.2 Backup Old Version (Optional)

```bash
# Create backup before refactoring
cp ~/.claude/skills/SKILL_NAME/skill.md \
   ~/.claude/skills/SKILL_NAME/skill.md.backup.$(date +%Y%m%d)
```

---

## Common Patterns & Solutions

### Pattern 1: Large API Reference

**Problem:** skill.md has 50+ endpoints documented

**Solution:**
```
references/
├── authentication.md     # Auth methods
├── common-endpoints.md   # Top 10 most-used endpoints
├── full-api-reference.md # Complete endpoint list
└── examples.md           # Working code samples
```

In skill.md: Link to common-endpoints.md in loading strategy, mention full reference exists.

### Pattern 2: Many Code Examples

**Problem:** skill.md has 20+ code examples

**Solution:**
```
references/
├── quick-examples.md     # 3-5 common patterns
├── complete-examples.md  # Full implementations
└── advanced-examples.md  # Edge cases, optimization
```

In skill.md: Include ONE minimal quick start example, link to others.

### Pattern 3: Step-by-Step Guides

**Problem:** skill.md has detailed procedural guides

**Solution:**
```
references/
├── getting-started.md    # First-time setup
├── common-tasks.md       # Frequent operations
└── advanced-workflows.md # Complex procedures
```

In skill.md: High-level overview, link to detailed guides.

### Pattern 4: Extensive Troubleshooting

**Problem:** skill.md has long error-handling sections

**Solution:**
```
references/
├── common-errors.md      # Top 10 errors and fixes
├── troubleshooting-guide.md # Systematic debugging
└── error-reference.md    # Complete error catalog
```

In skill.md: Mention troubleshooting exists, link in loading strategy.

---

## Tips for Success

1. **Start with the biggest sections** - Tackle the bulk first
2. **Keep quick start in skill.md** - Users need immediate working example
3. **Be specific in "when to read"** - "For authentication issues" not "For help"
4. **Test as you go** - Validate each reference file works
5. **Don't over-split** - Better 4 good files than 10 tiny ones
6. **Use consistent formatting** - Makes navigation easier
7. **Add cross-links** - Help users navigate between references
8. **Update loading strategy last** - You'll know the final structure

---

## Anti-Patterns to Avoid

❌ **Creating extraneous files**
- Bad: README.md, CHANGELOG.md, INSTALLATION_GUIDE.md
- Good: Only SKILL.md, scripts/, references/, assets/

❌ **Extra fields in frontmatter**
- Bad: `tags: [foo, bar]`, `version: 1.0`
- Good: Only `name` and `description`

❌ **Vague file names**
- Bad: `info.md`, `more.md`, `part2.md`
- Good: `authentication.md`, `examples.md`, `error-handling.md`

❌ **No loading strategy**
- Bad: Just listing files
- Good: Explaining when to read each file

❌ **Deleting content**
- Bad: "This seems outdated, I'll remove it"
- Good: "I'll move this to references/archive.md"

❌ **No quick start in skill.md**
- Bad: "See references/examples.md for usage"
- Good: Minimal example in skill.md + link to more

---

## Related References

- See `templates.md` for actual templates to use
- See `best-practices.md` for principles and guidelines
