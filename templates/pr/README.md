# PR Template System

**Version**: 2.0.0  
**Purpose**: Multi-language Pull Request templates for GitHub

## Overview

This directory contains Pull Request templates in multiple languages. The system automatically selects the appropriate template based on the user's language preference in `config.toml`.

## Directory Structure

```
.scaffolding/templates/pr/
├── README.md                           # This file
├── PULL_REQUEST_TEMPLATE.zh-TW.md     # Traditional Chinese (Taiwan)
├── PULL_REQUEST_TEMPLATE.en-US.md     # English (United States)
├── PULL_REQUEST_TEMPLATE.zh-CN.md     # Simplified Chinese (China)
└── PULL_REQUEST_TEMPLATE.ja-JP.md     # Japanese (Japan)
```

## Usage

### Automatic Selection

When initializing a project, the script reads `config.toml` to determine the primary language:

```toml
[locale]
primary = "zh-TW"  # or "en-US", "zh-CN", "ja-JP"
```

The corresponding template is copied to `.github/PULL_REQUEST_TEMPLATE.md`.

### Manual Installation

```bash
# Generate PR template based on config.toml
./.scaffolding/scripts/generate-pr-template.sh

# Or specify language explicitly
./.scaffolding/scripts/generate-pr-template.sh zh-TW
./.scaffolding/scripts/generate-pr-template.sh en-US
```

## Template Features

All templates include:

1. **Summary** - Brief description of changes
2. **Changes** - Detailed list of modifications
3. **Testing** - How to verify the changes
4. **Checklist** - Quality assurance items
5. **Related Issues** - Link to issues (optional)
6. **Screenshots** - Visual changes (optional, for UI)

## Customization

### Project-Specific Templates

To customize templates for your project:

1. Copy template to project root:
   ```bash
   cp .scaffolding/templates/pr/PULL_REQUEST_TEMPLATE.zh-TW.md \
      .github/PULL_REQUEST_TEMPLATE.md
   ```

2. Edit `.github/PULL_REQUEST_TEMPLATE.md` as needed

3. Your custom template takes precedence over scaffolding templates

### Adding New Languages

To add a new language (e.g., `ko-KR` for Korean):

1. Create `PULL_REQUEST_TEMPLATE.ko-KR.md` in this directory
2. Follow the structure of existing templates
3. Update `generate-pr-template.sh` to recognize `ko-KR`
4. Update this README

## Configuration Options

Control PR template behavior in `config.toml`:

```toml
[github]
use_pr_template = true           # Enable/disable PR templates
pr_template_style = "simple"     # "simple" | "detailed" | "custom"
```

**Styles**:
- `simple` - Minimal fields (Summary, Changes, Testing)
- `detailed` - All fields including screenshots, related issues
- `custom` - Use project-specific template in `.github/`

## GitHub Integration

GitHub automatically uses the template in `.github/PULL_REQUEST_TEMPLATE.md` when creating PRs.

**Priority**:
1. `.github/PULL_REQUEST_TEMPLATE.md` (project-specific)
2. `.github/PULL_REQUEST_TEMPLATE/default.md` (multiple templates)
3. `docs/PULL_REQUEST_TEMPLATE.md` (alternative location)

This scaffolding uses **option 1** (single template in `.github/`).

## Design Principles

### Language-Specific Considerations

**Traditional Chinese (Taiwan)**:
- Use "繁體中文" terminology
- Professional but approachable tone
- Examples: "請簡述", "變更內容", "測試方式"

**Simplified Chinese (China)**:
- Use "简体中文" terminology
- Formal technical language
- Examples: "简述", "变更内容", "测试方法"

**English (United States)**:
- Clear, concise language
- International English conventions
- Examples: "Summary", "Changes", "Testing"

**Japanese (Japan)**:
- Polite form (です/ます調)
- Technical Japanese terminology
- Examples: "概要", "変更内容", "テスト方法"

### Consistency

All templates follow the same structure to ensure:
- **Consistency** across languages
- **Easy translation** when switching languages
- **Familiar workflow** for multilingual teams

## Maintenance

### Updating Templates

When updating templates:

1. Update all language versions simultaneously
2. Maintain structural consistency
3. Test with `generate-pr-template.sh`
4. Verify GitHub displays correctly

### Version Tracking

Template versions align with scaffolding versions:
- **2.0.0** - Initial multi-language PR template system
- Future updates documented in `.scaffolding/CHANGELOG.md`

## Related Documentation

- [ADR 0012 - Module System & Conditional Loading](../../docs/adr/0012-module-system-and-conditional-loading.md)
- [AGENTS.md - PR Template Protocol](../../../AGENTS.md#pull-request)
- [Internationalization Guide](../../i18n/README.md)

## Support

For issues or suggestions:
1. Check `AGENTS.md` for AI agent guidance
2. Review ADR 0012 for design decisions
3. Consult `config.toml.example` for configuration options
