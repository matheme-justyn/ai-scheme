# Terminology System (術語系統)

**Version**: 2.0.0  
**Purpose**: Hierarchical terminology loading for AI agents based on project type and domain.

---

## Overview

This system provides **consistent technical terminology** across multiple natural languages (English, 繁體中文, 簡體中文, 日本語) for AI agents working on different project types.

**Benefits**:
- 🌐 Multilingual consistency (4 languages)
- 🎯 Context-aware loading (only load relevant terms)
- 📊 Hierarchical priority (custom > domain > common > universal)
- 🤖 AI agent friendly (table format, easy parsing)

---

## File Structure

```
.scaffolding/docs/terminology/
├── README.md                    # This file
├── terminology.md                # Universal terms (always loaded)
├── software/
│   ├── common.md                 # Software development common terms
│   ├── frontend.md               # React, CSS, UI/UX terms
│   ├── backend.md                # Node.js, API, server terms
│   └── database.md               # SQL, ORM, optimization terms
├── academic/
│   ├── common.md                 # Research, writing, ethics terms
│   └── computer-science.md       # AI/ML, algorithms, HCI terms
└── project/
    └── custom.md.example         # User-defined overrides
```

**Total**: 7 files, ~2,358 lines

---

## Loading Logic (AI Agents MUST Follow)

### 1. Always Load

**File**: `terminology.md`  
**Content**: Universal tech terms (Git, file operations, naming conventions)  
**When**: Every session, all project types

### 2. Domain-Specific Loading

Based on `[project].type` in `config.toml`:

#### Software Projects

**Frontend** (`type = "frontend"` or `"fullstack"`):
```
terminology.md
→ software/common.md
→ software/frontend.md
```

**Backend** (`type = "backend"` or `"fullstack"`):
```
terminology.md
→ software/common.md
→ software/backend.md
```

**Database** (`features` contains `"database"`):
```
+ software/database.md
```

#### Academic Projects

**Academic** (`type = "academic"`):
```
terminology.md
→ academic/common.md
→ academic/{field}.md  # e.g., computer-science.md
```

**Available fields**:
- `computer_science` → `academic/computer-science.md`
- (Future: `biology`, `physics`, `social_science`, etc.)

### 3. Custom Overrides (Highest Priority)

**File**: `.agents/terminology/custom.md` (user creates)  
**Purpose**: Project-specific term overrides  
**When**: If file exists, load LAST (highest priority)

**Example**:
```markdown
# Custom Project Terminology

| English | 繁體中文 | Notes |
|---------|---------|-------|
| User | 使用者 | NOT "用戶" |
| Payment | 付款 | NOT "支付" |
```

---

## Priority Order

When the same term appears in multiple files:

```
Custom > Domain-Specific > Common > Universal
```

**Example**:
- `terminology.md` says: "User" = "用戶"
- `custom.md` says: "User" = "使用者"
- AI agent uses: **"使用者"** (custom wins)

---

## Configuration

**File**: `config.toml`

```toml
[project]
type = "fullstack"  # frontend | backend | fullstack | cli | library | academic | documentation
features = ["api", "database", "auth"]

[academic]
citation_style = "APA"  # Only for type = "academic"
field = "computer_science"
```

---

## AI Agent Protocol

### On Session Start

1. **Read config.toml** → Identify `project.type`, `features`, `academic.field`
2. **Load terminology.md** (always)
3. **Load domain files** (based on type):
   - Fullstack → software/common.md, frontend.md, backend.md
   - Academic → academic/common.md, academic/{field}.md
4. **Load custom.md** (if exists)

### During Task Execution

1. When encountering **technical terms**, use loaded terminology
2. **Multilingual projects**: Use appropriate language column
3. **Ambiguous terms**: Check priority order (custom > domain > common > universal)

---

## File Format

Each terminology file follows this structure:

```markdown
# {Category Name}

**Purpose**: {Brief description}  
**Loading**: {When this file is loaded}  
**Priority**: {Priority level}

---

## {Section Name}

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Context |
|---------|--------------|--------------|------------|---------|
| Term 1  | 術語1        | 术语1        | 用語1      | Notes   |
| Term 2  | 術語2        | 术语2        | 用語2      | Notes   |
```

**Columns**:
- **English**: Standard technical term
- **繁體中文 (TW)**: Traditional Chinese (Taiwan)
- **簡體中文 (CN)**: Simplified Chinese (China)
- **日本語 (JP)**: Japanese
- **Context**: Usage notes, abbreviations, special cases

---

## Adding New Terms

### For Project-Specific Terms

1. Create `.agents/terminology/custom.md` (if not exists)
2. Copy format from `.scaffolding/docs/terminology/terminology.md`
3. Add your terms with appropriate columns

### For Template-Wide Terms

1. Edit appropriate file in `.scaffolding/docs/terminology/`
2. Follow existing format
3. Add to relevant section
4. Update this README if adding new files

---

## Examples

### Example 1: Fullstack Web Project

**config.toml**:
```toml
[project]
type = "fullstack"
features = ["api", "database", "auth"]
```

**AI Agent loads**:
1. `terminology.md` (universal)
2. `software/common.md` (SDLC, testing)
3. `software/frontend.md` (React, CSS)
4. `software/backend.md` (Node.js, API)
5. `software/database.md` (SQL, ORM)
6. `.agents/terminology/custom.md` (if exists)

**Total**: ~1,800 terms loaded

### Example 2: Academic Research Project

**config.toml**:
```toml
[project]
type = "academic"

[academic]
field = "computer_science"
citation_style = "APA"
```

**AI Agent loads**:
1. `terminology.md` (universal)
2. `academic/common.md` (research, writing)
3. `academic/computer-science.md` (AI/ML, algorithms)
4. `.agents/terminology/custom.md` (if exists)

**Total**: ~900 terms loaded

---

## Maintenance

### Adding New Languages

To add a new language column (e.g., French):

1. Edit ALL terminology files
2. Add column: `| Français (FR) |`
3. Translate existing terms
4. Update this README
5. Update AGENTS.md (Module Loading Protocol section)

### Adding New Domains

To add a new domain (e.g., `mobile/`):

1. Create directory: `.scaffolding/docs/terminology/mobile/`
2. Create files: `common.md`, `ios.md`, `android.md`
3. Update loading logic in AGENTS.md
4. Update this README

---

## Related Documentation

- **[AGENTS.md - Module Loading Protocol](../../../AGENTS.md#module-loading-protocol)** - Complete loading rules
- **[config.toml.example](../../../config.toml.example)** - Configuration reference
- **[ADR 0012 - Module System](../../../docs/adr/0012-module-system-and-conditional-loading.md)** - Design decisions

---

## Version History

- **2.0.0** (2026-03-16): Complete terminology system with 7 files
- **1.15.0** (2025-03-12): Initial terminology structure
