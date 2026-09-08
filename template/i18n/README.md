# Internationalization (i18n) System

## 概述 | Overview

This template uses **BCP 47 (RFC 5646)** language tags for internationalization, allowing you to customize all documentation and templates in your preferred natural language while keeping the codebase language-agnostic.

本模板使用 **BCP 47 (RFC 5646)** 語言標籤進行國際化，讓你可以用偏好的自然語言自訂所有文件和模板，同時保持程式碼庫的語言中立性。

## 語言標籤標準 | Language Tag Standard

**BCP 47 (RFC 5646)** is the IETF standard for identifying languages:

- `zh-TW` - Traditional Chinese (Taiwan) | 台灣繁體中文
- `zh-HK` - Traditional Chinese (Hong Kong) | 香港繁體中文
- `zh-CN` - Simplified Chinese (China) | 簡體中文
- `en-US` - English (United States) | 美式英語
- `en-GB` - English (United Kingdom) | 英式英語
- `ja-JP` - Japanese (Japan) | 日文

This standard is used by:
- W3C WCAG (Web Content Accessibility Guidelines)
- HTML `lang` attribute
- EPUB (electronic publication)
- Unicode CLDR (Common Locale Data Repository)

**Reference:** [RFC 5646 - Tags for Identifying Languages](https://www.rfc-editor.org/rfc/rfc5646.html)

## 架構 | Architecture

```
i18n/
├── config.toml.example          # Configuration example (committed to Git)
├── config.toml                  # Your local config (gitignored)
├── locales/
│   ├── en-US/                   # English (US) - Base language
│   │   ├── agents.toml          # AGENTS.md translations
│   │   ├── readme.toml          # README.md translations
│   │   ├── templates.toml       # GitHub templates
│   │   └── adr.toml             # ADR templates
│   └── zh-TW/                   # Traditional Chinese (Taiwan)
│       ├── agents.toml
│       ├── readme.toml
│       ├── templates.toml
│       └── adr.toml
└── README.md                    # This file
```

## 使用方式 | Usage

### 1. 設定語言 | Set Your Language

```bash
# Copy example config
cp config.toml.example config.toml

# Edit config.toml and set your preferred language
# For example, for Traditional Chinese (Taiwan):
[locale]
primary = "zh-TW"
fallback = "en-US"
```

### 2. 語言切換效果 | What Gets Switched

When you switch languages, the following content adapts:

- **AGENTS.md** - Coding conventions, commit message format, PR guidelines
- **README.md** - Project description, usage instructions
- **GitHub Templates** - Issue templates, PR template
- **ADR Templates** - Architecture decision record templates

**Code stays in English** - Variable names, function names, and code comments remain in English for universal comprehension.

### 3. Git 策略 | Git Strategy

**Committed to Git:**
- `config.toml.example` - Configuration template
- `i18n/locales/en-US/` - English (base language)
- `i18n/locales/zh-TW/` - Traditional Chinese (Taiwan)

**NOT committed (`.gitignored`):**
- `config.toml` - Your personal language preference

This allows each team member to use their preferred language locally while maintaining a consistent codebase.

## 新增語言 | Adding New Languages

### For Personal Use

1. Create new locale directory: `i18n/locales/{lang-tag}/`
2. Copy files from `en-US/` or `zh-TW/`
3. Translate content
4. Update your local `config.toml`

### For Contributing Back

If you want to contribute a new language to the template:

1. Follow personal use steps above
2. Add the locale to `config.toml.example`
3. Update this README's "Available Locales" section
4. Commit the new locale directory
5. Update `.gitignore` if needed

## 可用語系 | Available Locales

| Language Tag | Language | Status |
|--------------|----------|--------|
| `en-US` | English (United States) | ✅ Base language |
| `zh-TW` | Traditional Chinese (Taiwan) | ✅ Available |
| `zh-HK` | Traditional Chinese (Hong Kong) | 🔜 Planned |
| `zh-CN` | Simplified Chinese (China) | 🔜 Planned |
| `ja-JP` | Japanese (Japan) | 🔜 Planned |
| `en-GB` | English (United Kingdom) | 🔜 Planned |

## 翻譯工作流程 | Translation Workflow

If you're doing translation work (e.g., Chinese → English, Chinese → Japanese):

1. Enable translation mode in `config.toml`:
   ```toml
   [translation]
   enabled = true
   source_lang = "zh-TW"
   target_langs = ["en-US", "ja-JP"]
   ```

2. Use translation tools or AI to assist

3. Validate completeness:
   ```bash
   # Check for missing keys (future feature)
   ./scripts/i18n-validate.sh
   ```

## 台灣特殊詞彙考量 | Taiwan-Specific Terminology

For Taiwan localization (`zh-TW`), certain terms require special attention:

- **政府相關** - Government-related terms must follow Taiwan official terminology
- **資訊科技** - IT terms may differ from mainland China usage
- **日常用語** - Colloquial expressions differ significantly

**Example:**
- `zh-TW`: "軟體" (software)
- `zh-CN`: "软件" (software)

The `zh-TW` locale respects these distinctions.

## 技術細節 | Technical Details

### TOML Format

Translation files use TOML for readability:

```toml
[coding_conventions]
title = "編碼規範"
test_first = "永遠先寫測試"
docstring = "所有函數要有 docstring 和型別標注"

[commit_message]
format = "使用繁體中文撰寫 commit message"
```

### Key Naming Convention

- Use `snake_case` for keys
- Organize by section/context
- Keep keys consistent across locales
- English keys preferred for maintainability

## 疑難排解 | Troubleshooting

### Language Not Switching

1. Check `config.toml` exists (copy from `.example` if missing)
2. Verify locale directory exists: `i18n/locales/{your-lang}/`
3. Ensure TOML files have required keys

### Missing Translations

If a translation key is missing:
1. Fallback to `en-US` (base language)
2. Check if key exists in base language
3. Add missing key to your locale

### Encoding Issues

- All TOML files must be UTF-8 encoded
- No BOM (Byte Order Mark)
- Use Unix line endings (LF, not CRLF)

## 參考資源 | Resources

- [BCP 47 / RFC 5646 - Language Tags](https://www.rfc-editor.org/rfc/rfc5646.html)
- [IANA Language Subtag Registry](https://www.iana.org/assignments/language-subtag-registry)
- [W3C Language Tags in HTML and XML](https://www.w3.org/International/articles/language-tags/)
- [Unicode CLDR](http://cldr.unicode.org/)
