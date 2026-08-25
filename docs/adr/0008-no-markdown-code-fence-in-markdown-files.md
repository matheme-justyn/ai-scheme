# ADR 0008: No Markdown Code Fence in Markdown Files

**Status**: Accepted  
**Date**: 2026-03-10  
**Deciders**: Template Maintainers  
**Tags**: documentation, markdown, standards

## Context

We discovered a widespread anti-pattern in our documentation: wrapping markdown content with ` ```markdown ` code fences inside `.md` files.

**Example of the problem:**

```markdown
<!-- In a README.md file -->
## Example Section

```markdown
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
```
```

This creates several issues:

1. **Redundancy** - `.md` files are already markdown; wrapping markdown in markdown is redundant
2. **Rendering Issues** - GitHub and other markdown renderers may display the content as a code block instead of rendering it
3. **Cognitive Overhead** - Adds unnecessary visual noise, making files harder to read
4. **Inconsistency** - Some files have fences, others don't, leading to inconsistent style
5. **AI Confusion** - AI agents may think they need to preserve/add these fences when editing

### Where This Occurs

Common locations where this anti-pattern appears:
- Documentation files (`.scaffolding/docs/*.md`)
- Root README files
- ADR documents
- Guide/tutorial files
- Template documentation

### Root Cause

This anti-pattern likely originated from:
1. **AI Generation** - AI models sometimes over-apply code fence syntax when generating markdown
2. **Copy-Paste** - Copying markdown examples from documentation that shows "how to write markdown"
3. **Habit Transfer** - Coming from contexts where markdown needs to be escaped (e.g., in Slack, Discord)

## Decision

**We will enforce a strict rule: NEVER use ` ```markdown ` code fences inside `.md` files.**

### When to Use Code Fences

Code fences are ONLY appropriate for:

| Use Case | Example | Reason |
|----------|---------|--------|
| **Programming languages** | ` ```python`, ` ```bash`, ` ```javascript` | Syntax highlighting for code |
| **Configuration files** | ` ```toml`, ` ```yaml`, ` ```json` | Distinguishing config from prose |
| **Plain text** | ` ```text`, ` ``` ` (no language) | Literal text that shouldn't render |

### When NOT to Use Code Fences

❌ **NEVER use ` ```markdown ` in `.md` files for:**

- Tables
- Headers
- Lists
- Links
- Emphasis (bold, italic)
- Blockquotes
- Any standard markdown syntax

**Correct approach:**

```markdown
<!-- ✅ CORRECT - Direct markdown -->
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |

## This is a header

- List item 1
- List item 2
```

```markdown
<!-- ❌ WRONG - Unnecessary wrapping -->
```markdown
| Column 1 | Column 2 |
|----------|----------|
| Value 1  | Value 2  |
```
```

## Consequences

### Positive

✅ **Cleaner files** - Markdown files are easier to read and edit  
✅ **Consistent rendering** - Content renders correctly on all platforms  
✅ **AI-friendly** - AI agents generate cleaner markdown without unnecessary fences  
✅ **Reduced file size** - Removes redundant wrapper syntax  
✅ **Standard compliance** - Follows markdown best practices  

### Negative

⚠️ **Migration effort** - Need to clean up existing files (one-time cost)  
⚠️ **Re-education** - Team and AI agents need to learn this rule  

### Neutral

🔄 **Enforcement** - Need linting or review process to catch violations  

## Implementation

### Phase 1: Cleanup (Immediate)

1. ✅ Create this ADR documenting the rule
2. ✅ Scan all `.md` files for ` ```markdown ` usage
3. ✅ Batch-fix all occurrences
4. ✅ Update AGENTS.md to warn AI agents about this anti-pattern

### Phase 2: Prevention (Future)

1. Add markdown linter rule (markdownlint, remark)
2. Create pre-commit hook to detect violations
3. Add to CI/CD validation
4. Document in contribution guidelines

### Detection Pattern

Find all violations:
```bash
# Search for markdown code fences in .md files
grep -r '```markdown' --include="*.md" .
```

### Automated Fix

```bash
# Remove markdown code fences (careful with edge cases)
find . -name "*.md" -exec sed -i '' '/^```markdown$/d' {} \;
```

## Validation

### Success Criteria

- [ ] No ` ```markdown ` found in any `.md` file
- [ ] All tables, lists, headers render correctly
- [ ] AI agents warned in AGENTS.md
- [ ] Linting rule added (future)

### Testing

```bash
# Verify no markdown fences remain
grep -r '```markdown' --include="*.md" . && echo "❌ Found violations" || echo "✅ Clean"

# Check files still render correctly on GitHub
# (Manual visual inspection)
```

## References

- [GitHub Flavored Markdown Spec](https://github.github.com/gfm/)
- [CommonMark Spec](https://spec.commonmark.org/)
- [Markdown Guide - Basic Syntax](https://www.markdownguide.org/basic-syntax/)

## Related Decisions

- ADR 0007: Agent Skills Ecosystem Integration - AI agent behavior standards
- AGENTS.md § README Generation Protocol - Automated markdown generation rules

## Notes

This ADR was created after discovering the anti-pattern in:
- README.md (fixed in commit f3c582a)
- Multiple documentation files in `.scaffolding/docs/`
- Example files and templates

**Lesson learned**: When generating markdown programmatically (scripts, AI), always output raw markdown without unnecessary code fence wrappers.
