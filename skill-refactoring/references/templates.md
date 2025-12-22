# Refactoring Templates

> Part of the skill-refactoring skill
> Read skill.md for overview and when to use this reference

## Overview

This document provides copy-paste templates for creating well-structured skill files during refactoring.

---

## skill.md Template

```markdown
---
name: skill-name
description: Clear description including what the skill does AND when to use it (shows in skill picker)
---

# Skill Name

[2-3 sentences explaining what this skill does and why it exists. Be specific and concrete.]

## Purpose

[Expand slightly on the description if needed. What problem does this solve?]

## When to Use This Skill

Use this skill when:
- [Specific use case 1]
- [Specific use case 2]
- [Specific use case 3]
- [Specific use case 4]

## Quick Start

\`\`\`language
# [Description of what this minimal example does]
from module import thing

result = thing.do_something()
print(result)  # Expected output
\`\`\`

For complete examples, see `references/examples.md`.

## Reference Files

### 1. [Primary Topic] (`references/main-topic.md`)
**Read this for:**
- [Specific subtopic A]
- [Specific subtopic B]
- [Specific subtopic C]

### 2. [Secondary Topic] (`references/secondary-topic.md`)
**Read this for:**
- [Specific subtopic D]
- [Specific subtopic E]
- [Specific subtopic F]

### 3. Examples (`references/examples.md`)
**Read this for:**
- [Common pattern 1]
- [Common pattern 2]
- [Real-world use cases]

### 4. Troubleshooting (`references/troubleshooting.md`)
**Read this for:**
- [Common error 1]
- [Common error 2]
- [Debug strategies]

## Loading Strategy

- **Always read** `main-topic.md` when using this skill
- **Read when implementing** `examples.md` for code patterns
- **Read when errors occur** `troubleshooting.md` for solutions
- **Read for specific needs** `secondary-topic.md` for advanced cases

## Key Principles

- [Most important principle 1]
- [Most important principle 2]
- [Most important principle 3]
- [Most important principle 4]
- [Most important principle 5]

## Related Documentation

- See `path/to/related/file.md` for [related topic]
- Official docs: [URL to external documentation if applicable]
```

**Target length:** Under 500 lines (shorter is better for context)

---

## Reference File Template

```markdown
# [Topic Name]

> Part of the [skill-name] skill
> Read skill.md for overview and when to use this reference

## Overview

[Brief description of what this reference file covers. 2-3 sentences.]

---

## [Section 1: Core Concept]

[Explain the main concept or pattern]

### Key Points

- [Important point 1]
- [Important point 2]
- [Important point 3]

### Example

\`\`\`language
# [Description of what this example demonstrates]
code here
\`\`\`

**Explanation:** [Walk through the important parts]

---

## [Section 2: Variations]

[Explain different approaches or variations]

### Pattern A: [Pattern Name]

**When to use:** [Specific scenario]

\`\`\`language
# [Pattern A implementation]
code here
\`\`\`

### Pattern B: [Pattern Name]

**When to use:** [Different scenario]

\`\`\`language
# [Pattern B implementation]
code here
\`\`\`

---

## [Section 3: Advanced Topics]

[Cover edge cases, optimization, or advanced usage]

### [Advanced Topic 1]

[Explanation]

### [Advanced Topic 2]

[Explanation]

---

## Common Pitfalls

❌ **Pitfall 1:** [What not to do]
- Why it's wrong: [Explanation]
- Fix: [Correct approach]

❌ **Pitfall 2:** [Another mistake to avoid]
- Why it's wrong: [Explanation]
- Fix: [Correct approach]

---

## Related References

- See `another-reference.md` for [related topic]
- See `examples.md` for [working code]
- See `troubleshooting.md` for [debugging help]

---

## Quick Reference Card

[Optional: One-page summary of key information for quick lookup]

\`\`\`
Function: thing.do_something()
Parameters:
  - param1: Type - Description
  - param2: Type - Description
Returns: Type - Description
Example: thing.do_something(param1, param2)
\`\`\`
```

---

## Examples File Template

```markdown
# Examples

> Part of the [skill-name] skill
> Read skill.md for overview and when to use this reference

## Overview

This file contains working code examples demonstrating common patterns and use cases.

---

## Example 1: [Common Use Case Name]

**Scenario:** [Describe when you'd use this]

**Requirements:**
- [Requirement 1]
- [Requirement 2]

**Code:**

\`\`\`language
# [Full working example with comments]
from module import thing

# Step 1: [Setup]
setup_code()

# Step 2: [Main operation]
result = thing.do_something()

# Step 3: [Handle result]
print(result)
\`\`\`

**Output:**
\`\`\`
Expected output here
\`\`\`

**Explanation:**
- [Line/section 1]: [What it does]
- [Line/section 2]: [What it does]
- [Line/section 3]: [What it does]

---

## Example 2: [Another Common Pattern]

[Repeat structure from Example 1]

---

## Example 3: [Advanced Use Case]

[Repeat structure, but for more complex scenario]

---

## Complete Real-World Example

**Scenario:** [Full application or integration example]

\`\`\`language
# [Complete working application]
# [With all error handling, best practices, etc.]
complete code here
\`\`\`

**Key features demonstrated:**
- [Feature 1]
- [Feature 2]
- [Feature 3]

---

## Quick Reference: Common Patterns

### Pattern: [Pattern Name]
\`\`\`language
# Minimal version for quick reference
code
\`\`\`

### Pattern: [Another Pattern]
\`\`\`language
# Minimal version
code
\`\`\`
```

---

## Troubleshooting File Template

```markdown
# Troubleshooting

> Part of the [skill-name] skill
> Read skill.md for overview and when to use this reference

## Overview

Common issues, error messages, and solutions when using [skill-name].

---

## Quick Diagnosis

**Symptoms → Solution:**
- ❌ Error: "[Error message]" → See [Section X]
- ❌ [Problem behavior] → See [Section Y]
- ❌ [Another symptom] → See [Section Z]

---

## Error: [Common Error Message]

**Full error:**
\`\`\`
[Complete error message as it appears]
\`\`\`

**Cause:** [What causes this error]

**Solution:**
1. [Step 1 to fix]
2. [Step 2 to fix]
3. [Step 3 to fix]

**Prevention:** [How to avoid in the future]

---

## Problem: [Common Issue Description]

**Symptoms:**
- [Symptom 1]
- [Symptom 2]

**Possible Causes:**
1. [Cause 1] - See [Solution A]
2. [Cause 2] - See [Solution B]
3. [Cause 3] - See [Solution C]

### Solution A: [Fix for Cause 1]
\`\`\`language
# Code or command to fix
fix here
\`\`\`

### Solution B: [Fix for Cause 2]
\`\`\`language
# Code or command to fix
fix here
\`\`\`

---

## Debugging Checklist

When something isn't working:

- [ ] [Check 1: Common issue]
  - How to check: [Command or test]
  - If failed: [What to do]

- [ ] [Check 2: Another common issue]
  - How to check: [Command or test]
  - If failed: [What to do]

- [ ] [Check 3: Less common but important]
  - How to check: [Command or test]
  - If failed: [What to do]

---

## Known Limitations

**Limitation 1:** [What doesn't work]
- **Workaround:** [How to work around it]
- **Status:** [Will be fixed / permanent limitation]

**Limitation 2:** [Another limitation]
- **Workaround:** [Alternative approach]
- **Status:** [Update on when/if it will be addressed]

---

## Getting More Help

If the above doesn't resolve your issue:

1. Check official documentation: [URL]
2. Review `references/examples.md` for working code
3. Verify your setup matches `references/prerequisites.md`
4. [Other resource or contact]
```

---

## API Reference Template

```markdown
# API Reference

> Part of the [skill-name] skill
> Read skill.md for overview and when to use this reference

## Overview

Complete reference for all functions, classes, and endpoints.

---

## Class: ClassName

**Description:** [What this class does]

**Import:**
\`\`\`language
from module import ClassName
\`\`\`

### Constructor

\`\`\`language
ClassName(param1, param2, param3=default)
\`\`\`

**Parameters:**
- `param1` (Type): [Description]
- `param2` (Type): [Description]
- `param3` (Type, optional): [Description]. Default: `default`

**Example:**
\`\`\`language
obj = ClassName(value1, value2)
\`\`\`

### Methods

#### method_name()

\`\`\`language
obj.method_name(arg1, arg2, kwarg1=default)
\`\`\`

**Description:** [What this method does]

**Parameters:**
- `arg1` (Type): [Description]
- `arg2` (Type): [Description]
- `kwarg1` (Type, optional): [Description]. Default: `default`

**Returns:**
- (ReturnType): [Description of return value]

**Raises:**
- `ExceptionType`: [When this is raised]

**Example:**
\`\`\`language
result = obj.method_name(val1, val2)
print(result)  # Expected: [output]
\`\`\`

---

## Function: function_name()

\`\`\`language
function_name(param1, param2, param3=default)
\`\`\`

[Repeat method structure]

---

## Endpoint: GET /api/path

**URL:** `https://api.example.com/api/path`

**Method:** `GET`

**Authentication:** [Required/Optional] - [Type]

**Parameters:**

*Query Parameters:*
- `param1` (string, required): [Description]
- `param2` (integer, optional): [Description]. Default: `0`

*Headers:*
- `Authorization`: Bearer token
- `Content-Type`: application/json

**Request Example:**
\`\`\`bash
curl -X GET "https://api.example.com/api/path?param1=value" \
  -H "Authorization: Bearer YOUR_TOKEN"
\`\`\`

**Response:**

*Success (200):*
\`\`\`json
{
  "status": "success",
  "data": {
    "field1": "value1",
    "field2": "value2"
  }
}
\`\`\`

*Error (400):*
\`\`\`json
{
  "status": "error",
  "message": "Error description"
}
\`\`\`

**Response Fields:**
- `status` (string): "success" or "error"
- `data` (object): Response data
  - `field1` (string): [Description]
  - `field2` (string): [Description]

**Rate Limits:** [X requests per minute]

---

## Quick Reference Table

| Function/Method | Purpose | Common Use |
|----------------|---------|------------|
| `function1()` | [Short description] | [When to use] |
| `function2()` | [Short description] | [When to use] |
| `function3()` | [Short description] | [When to use] |
```

---

## Loading Strategy Template

Use this pattern in skill.md:

```markdown
## Loading Strategy

- **Always read** `core-concepts.md` when [common task]
  - This covers [what's in there]
  - Essential for [why it's needed]

- **Read when implementing** `examples.md` for [specific need]
  - Contains [what's in there]
  - Useful when [scenario]

- **Read when errors occur** `troubleshooting.md` for [debugging]
  - Has solutions for [error types]
  - Includes [debugging tools/tips]

- **Read for advanced cases** `advanced.md` when [complex scenario]
  - Covers [advanced topics]
  - Needed for [edge cases]

- **Read for quick lookup** `api-reference.md` when [need specifics]
  - Complete reference for [what]
  - Use when [you know what you need]
```

---

## Related References

- See `methodology.md` for the refactoring process
- See `best-practices.md` for principles and guidelines
