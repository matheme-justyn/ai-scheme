# README Language Strategies & Formatting Rules

This document defines how AI agents should generate bilingual content in README.md based on `config.toml` locale settings.

This document defines **language strategies** and **formatting rules** for README generation based on `config.toml` settings.

---

## README Language Strategies

**CRITICAL: Check `config.toml` first to determine which strategy to use.**

```toml
# config.toml
[i18n.readme]
strategy = "separate"  # or "bilingual" or "primary_only"
```

### Strategy 1: Separate Files (Recommended)

**Use when:**
- Professional projects
- 3+ languages needed
- Clean, maintainable structure preferred
- Each language has independent readers

**Structure:**
```
README.md              # Primary language (based on primary_locale)
README.en-US.md        # English version
README.zh-TW.md        # Traditional Chinese version
README.ja-JP.md        # Japanese version (if needed)
```

**Language Switcher** (at top of each README):
# Project Name

English | [繁體中文](./README.zh-TW.md) | [日本語](./README.ja-JP.md)

**Advantages:**
- ✅ Cleaner: Each file is single-language, easier to read
- ✅ Scalable: Add new languages without bloating existing files
- ✅ Maintainable: Update one language without touching others
- ✅ Git-friendly: Separate commits for each language

**Disadvantages:**
- ❌ Duplication: Same structure repeated across files
- ❌ Sync risk: Easy to forget updating all language versions

---

### Strategy 2: Bilingual (Single File)

**Use when:**
- Small projects
- 2 languages max
- Guaranteed synchronization needed (content changes together)

**Structure:**
```
README.md              # Contains both primary_locale + English
```

**Format:** Mixed language in same file (see "Bilingual Formatting Rules" below)

**Advantages:**
- ✅ Synchronized: Both languages always in sync
- ✅ Single file: Easier to maintain consistency
- ✅ Side-by-side: Readers can compare translations

**Disadvantages:**
- ❌ Cluttered: File becomes long and hard to read
- ❌ Limited: Hard to scale beyond 2 languages
- ❌ Complex: Formatting rules are strict

---

### Strategy 3: Primary Only

**Use when:**
- Internal projects (single team)
- No internationalization needed
- Team uses only one language

**Structure:**
```
README.md              # Only primary_locale, no translations
```

**Advantages:**
- ✅ Simplest: No translation overhead
- ✅ Fastest: No duplication work

**Disadvantages:**
- ❌ Limited audience: Only speakers of primary_locale can read

---

## Choosing the Right Strategy

| Scenario | Recommended Strategy | Reason |
|----------|----------------------|--------|
| Open-source project with global audience | **Separate** | Professional, scalable |
| Small personal project (zh-TW + en-US) | **Bilingual** | Guaranteed sync |
| Internal company project (single language) | **Primary Only** | No translation needed |
| Project with 3+ languages | **Separate** | Bilingual becomes unmanageable |
| Documentation-heavy project | **Separate** | Easier to maintain long files |

---

## Bilingual Formatting Rules

**CRITICAL: These rules apply ONLY when `strategy = "bilingual"` in config.toml.**

If using `strategy = "separate"`, each README file is single-language and follows standard Markdown without bilingual formatting.

### Core Principles (for Bilingual Strategy)

**When `strategy = "bilingual"`:**
2. **English (`en-US`) is always included** (unless primary locale IS English)
3. **Format: Primary language first, then English**

### Language Pairing Rules (for Bilingual Strategy)

```toml
# config.toml
[i18n]
primary_locale = "zh-TW"  # Traditional Chinese (Taiwan)
fallback_locale = "en-US"
```

**Result**: README is **Traditional Chinese + English**

### Bilingual Pairing Table

| primary_locale | README Languages | Order |
|----------------|------------------|-------|
| `zh-TW` | 繁體中文 + English | Chinese first, then English |
| `zh-CN` | 简体中文 + English | Chinese first, then English |
| `ja-JP` | 日本語 + English | Japanese first, then English |
| `ko-KR` | 한국어 + English | Korean first, then English |
| `en-US` | English only | No bilingual needed |
| `en-GB` | English only | No bilingual needed |

## Bilingual Formatting Syntax

### 1. Headers (Headings) - Bilingual

**Format**: `## 中文 | English` (same line, separated by `|`)

**Example**:
## 🏛️ 什麼是 My Vibe Scaffolding？ | What is My Vibe Scaffolding?
## ⚡ 核心功能 | Core Features
## 🎯 Vibe 技術選型 | Vibe Tech Stack

**❌ WRONG**:
## 🏛️ 什麼是 My Vibe Scaffolding？

## What is My Vibe Scaffolding?

### 2. Paragraphs - Bilingual

**Format**: Chinese paragraph, blank line, English paragraph

**Example**:
**AI 驅動的專案鷹架模板** — 基於心理學家 Lev Vygotsky 的鷹架理論，透過 AI 輔助快速建立專案結構、遵循最佳實踐，並在成長後自由拆除或客製化。

**AI-driven project scaffolding template** — Based on psychologist Lev Vygotsky's scaffolding theory, quickly build project structures with AI assistance, follow best practices, and freely remove or customize as you grow.

### 3. Bullet Lists - Bilingual

**Format**: Each bullet has Chinese line, then English line (using `<br>` or two spaces)

**Example**:
- 🤖 **AI Agent 整合** — `AGENTS.md` 驅動的 OpenCode/Cursor 開發體驗  
  **AI Agent Integration** — OpenCode/Cursor development experience driven by `AGENTS.md`

- 🌐 **多語言支援** — BCP 47 i18n 系統，AI 自動適應使用者語言  
  **Multi-language Support** — BCP 47 i18n system, AI automatically adapts to user's language

### 4. Tables - Bilingual

**Format**: Each cell contains Chinese `<br>` English

**Example**:
| 技術決策<br>Technology | 選擇理由<br>Why | 解決的問題<br>Problem Solved |
|---------|---------|-----------|
| **OpenCode（開源 AI 助手）**<br>**OpenCode (Open-source AI assistant)** | 75+ 模型支援、CLI 優先、可腳本化<br>75+ models, CLI-first, scriptable | 不被單一供應商綁定<br>Avoid vendor lock-in |

**Key**: Use `<br>` (HTML line break) inside table cells for line breaks.

### 5. Code Blocks - Bilingual

**Format**: Code appears ONCE (no duplication). Comments can be bilingual if needed.

**Example**:
### 方式 1：AI 助手安裝（推薦） | Option 1: AI Assistant Install (Recommended)

在 OpenCode/Cursor/Claude 對話中貼上：  
Paste this in OpenCode/Cursor/Claude chat:

\```
my-vibe-scaffolding (scaffolding template)
Install and configure my-vibe-scaffolding by following the instructions here:
https://raw.githubusercontent.com/matheme-justyn/my-vibe-scaffolding/main/.opencode/INSTALL.md
\```

**Example with bilingual comments**:
\```bash
# 1. GitHub 點擊 "Use this template" → Clone 專案
# 1. Click "Use this template" on GitHub → Clone project
# 2. 初始化專案
# 2. Initialize project
./.scaffolding/scripts/init-project.sh
\```

**❌ WRONG**: Don't duplicate entire code blocks
\```bash
# 中文版
./.scaffolding/scripts/init-project.sh
\```

\```bash
# English version
./.scaffolding/scripts/init-project.sh
\```

### 6. Links - Bilingual

**Format**: Inline bilingual description separated by `|`

**Example**:
詳細說明 | For details: [INSTALL.md](./.opencode/INSTALL.md)

- [更新日誌](./CHANGELOG.md) - 版本變更記錄 | Version change log
- [模板同步](./.scaffolding/docs/TEMPLATE_SYNC.md) - 更新到新版本 | Update to new versions

## AI Agent Implementation (Bilingual Strategy Only)

### Session Start Checklist

1. **Read `config.toml`**
   ```bash
   cat config.toml
   ```

2. **Extract `primary_locale`**
   ```toml
   [i18n]
   primary_locale = "zh-TW"
   ```

3. **Determine bilingual pairing**
   - If `zh-TW` → Traditional Chinese + English
   - If `ja-JP` → Japanese + English
   - If `en-US` → English only

4. **Apply formatting rules** from this document

---

## AI Agent Implementation (All Strategies)

### Session Start Protocol

1. **Read `config.toml`**
   ```bash
   cat config.toml
   ```

2. **Extract strategy and locales**
   ```toml
   [i18n]
   primary_locale = "zh-TW"
   fallback_locale = "en-US"
   commit_locales = ["en-US", "zh-TW"]
   
   [i18n.readme]
   strategy = "separate"  # KEY: This determines generation method
   ```

3. **Generate README based on strategy**

   **If `strategy = "separate"`:**
   - Create `README.md` in `primary_locale`
   - For each language in `commit_locales` (except primary), create `README.{lang}.md`
   - Add language switcher at top of each file
   - Load content from `i18n/locales/{lang}/readme.toml`
   - Each file is **single-language** (standard Markdown, no bilingual formatting)

   **Example:**
   ```
   README.md          -> Chinese (primary_locale = zh-TW)
   README.en-US.md    -> English
   README.ja-JP.md    -> Japanese (if in commit_locales)
   ```

   **If `strategy = "bilingual"`:**
   - Create single `README.md` with bilingual content
   - Follow "Bilingual Formatting Rules" section above
   - Primary language first, then fallback language
   - Load content from both `i18n/locales/{primary_locale}/` and `i18n/locales/{fallback_locale}/`

   **If `strategy = "primary_only"`:**
   - Create `README.md` in `primary_locale` only
   - No additional language files
   - Load content from `i18n/locales/{primary_locale}/readme.toml`

4. **Apply formatting**
   - Separate strategy: Standard Markdown (single language per file)
   - Bilingual strategy: Apply bilingual syntax rules (headers with `|`, paragraphs separated, etc.)
   - Primary only: Standard Markdown

### Pseudocode Implementation

```python
# AI agent README generation logic
def generate_readme(config):
    strategy = config['i18n']['readme']['strategy']
    primary_locale = config['i18n']['primary_locale']
    commit_locales = config['i18n']['commit_locales']
    fallback_locale = config['i18n']['fallback_locale']
    
    if strategy == 'separate':
        # Create README.md in primary language
        primary_content = load_translations(f'i18n/locales/{primary_locale}/readme.toml')
        write_file('README.md', render_single_language(primary_content))
        
        # Create README.{lang}.md for other languages
        for locale in commit_locales:
            if locale != primary_locale:
                content = load_translations(f'i18n/locales/{locale}/readme.toml')
                write_file(f'README.{locale}.md', render_single_language(content))
        
        # Add language switcher to all README files
        add_language_switcher_to_all(commit_locales, primary_locale)
    
    elif strategy == 'bilingual':
        # Create single README.md with both languages
        primary_content = load_translations(f'i18n/locales/{primary_locale}/readme.toml')
        fallback_content = load_translations(f'i18n/locales/{fallback_locale}/readme.toml')
        write_file('README.md', render_bilingual(primary_content, fallback_content))
    
    elif strategy == 'primary_only':
        # Create single README.md in primary language only
        primary_content = load_translations(f'i18n/locales/{primary_locale}/readme.toml')
        write_file('README.md', render_single_language(primary_content))

def render_single_language(content):
    """Render standard Markdown from translation content"""
    return f"""
# {content['meta']['project_name']}

{content['description']}

## Features

{render_features(content['features'])}
"""

def render_bilingual(primary, fallback):
    """Render bilingual Markdown following formatting rules"""
    return f"""
## {primary['title']} | {fallback['title']}

{primary['description']}

{fallback['description']}
"""

def add_language_switcher_to_all(locales, primary):
    """Add language switcher links at top of each README"""
    switcher_links = []
    for locale in locales:
        if locale == primary:
            switcher_links.append(get_language_name(locale))  # No link for current file
        else:
            switcher_links.append(f"[{get_language_name(locale)}](./README.{locale}.md)")
    
    switcher = " | ".join(switcher_links)
    
    # Prepend to README.md
    prepend_to_file('README.md', switcher)
    
    # Prepend to README.{lang}.md files
    for locale in locales:
        if locale != primary:
            prepend_to_file(f'README.{locale}.md', switcher)
```

### Code Example

```python
# Pseudocode for AI agents
def generate_readme_header(title_zh, title_en, primary_locale):
    if primary_locale == "en-US":
        return f"## {title_en}"
    else:
        return f"## {title_zh} | {title_en}"

def generate_readme_paragraph(content_zh, content_en, primary_locale):
    if primary_locale == "en-US":
        return content_en
    else:
        return f"{content_zh}\n\n{content_en}"
```

## Validation Examples

### Correct Bilingual README Structure

## 🏛️ 什麼是 My Vibe Scaffolding？ | What is My Vibe Scaffolding?

**AI 驅動的專案鷹架模板** — 基於...

**AI-driven project scaffolding template** — Based on...

---

## ⚡ 核心功能 | Core Features

- 🤖 **AI Agent 整合** — `AGENTS.md` 驅動...  
  **AI Agent Integration** — OpenCode/Cursor experience...

### Common Mistakes (Bilingual Strategy)

❌ **Headers on separate lines**
## 什麼是 My Vibe Scaffolding？

## What is My Vibe Scaffolding?

❌ **Duplicated code blocks**
\```bash
./.scaffolding/scripts/init-project.sh
\```

\```bash
./.scaffolding/scripts/init-project.sh
\```

❌ **Table cells without `<br>`**
| Technology | Why |
|------------|-----|
| **OpenCode** (Open-source) | 75+ models |

---

### Correct Separate Files Structure

**README.md (Chinese):**
# My Vibe Scaffolding

English | [繁體中文](./README.zh-TW.md)

## 什麼是 My Vibe Scaffolding？

**AI 驅動的專案鷹架模板** — 基於心理學家 Lev Vygotsky 的鷹架理論...

**README.en-US.md (English):**
# My Vibe Scaffolding

English | [繁體中文](./README.zh-TW.md)

## What is My Vibe Scaffolding?

**AI-driven project scaffolding template** — Based on psychologist Lev Vygotsky's scaffolding theory...

## Version History

- **1.6.0** - Added language strategy system (separate/bilingual/primary_only) (2026-03-02)
- **1.5.3** - Initial bilingual documentation (2026-02-26)
