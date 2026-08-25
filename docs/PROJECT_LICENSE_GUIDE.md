# Project License Guide

When using this scaffolding for your project, you need to choose your own license.

## Quick Decision Guide

### Open Source Projects

**Permissive Licenses** (允許商業使用、修改、分發)：
- **MIT License** - 最簡單、最常用、最寬鬆
- **Apache 2.0** - 類似 MIT，但提供專利授權保護
- **BSD 3-Clause** - 類似 MIT，但禁止使用專案名稱做推廣

**Copyleft Licenses** (要求衍生作品也開源)：
- **GPL v3** - 強 copyleft，衍生作品必須開源
- **LGPL v3** - 較弱 copyleft，適合函式庫
- **AGPL v3** - 最強 copyleft，連網路服務也要開源

### Proprietary/Commercial Projects

**Closed Source**：
- 不放 LICENSE 檔案
- 在 README.md 註明 "All Rights Reserved"
- 考慮加入 copyright notice

## Recommended Licenses by Project Type

| Project Type | Recommended License | Reason |
|--------------|---------------------|--------|
| Web application | MIT | 簡單、無負擔 |
| Library/Framework | MIT or Apache 2.0 | 鼓勵採用 |
| Company internal | Proprietary | 不對外開源 |
| Community project | GPL v3 | 確保衍生作品開源 |
| SaaS/API service | AGPL v3 | 防止服務端閉源 |

## How to Add License

### Step 1: Choose Your License

Visit [choosealicense.com](https://choosealicense.com/) for interactive guidance.

### Step 2: Create LICENSE File

```bash
# From your project root
nano LICENSE

# Or copy from template
cp .scaffolding/LICENSE ./LICENSE  # If you want MIT like the scaffolding
```

### Step 3: Update Copyright

Replace the copyright holder and year:
```
MIT License

Copyright (c) 2024 Your Name or Organization

Permission is hereby granted...
```

### Step 4: Add Badge to README

[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

## Common Combinations

### Dual Licensing
Some projects offer both:
- Free: GPL v3 (open source)
- Commercial: Proprietary license for fee

### Multiple Licenses
If using multiple components:
- Document each in `LICENSES/` directory
- Reference in main LICENSE or README

## License Compatibility

⚠️ **Important**: If your project depends on GPL libraries, your project must also be GPL.

Check compatibility:
- [SPDX License List](https://spdx.org/licenses/)
- [License Compatibility Matrix](https://www.gnu.org/licenses/gpl-faq.html)

## This Scaffolding's License

The scaffolding itself (`.scaffolding/` directory) is MIT licensed. You can:
- ✅ Use it for any project (commercial or open source)
- ✅ Modify it freely
- ✅ Choose a different license for your project
- ❌ Remove the LICENSE file from `.scaffolding/` (keep scaffolding attribution)

## Resources

- [Choose a License](https://choosealicense.com/)
- [SPDX License List](https://spdx.org/licenses/)
- [GitHub Licensing Guide](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
- [TL;DR Legal](https://www.tldrlegal.com/) - License summaries in plain English
