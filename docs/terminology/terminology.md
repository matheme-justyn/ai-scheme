# Common Terminology (跨領域常用術語)

**Purpose**: Universal tech terms used across all project types (software, academic, documentation).

**Loading**: Always loaded regardless of `project.type` in config.toml.

**Priority**: Lowest (project > domain > common)

---

## Universal Tech Terms

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Context |
|---------|--------------|--------------|------------|---------|
| Project | 專案 | 项目 | プロジェクト | |
| File | 檔案 | 文件 | ファイル | |
| Folder | 資料夾 | 文件夹 | フォルダー | |
| Directory | 目錄 | 目录 | ディレクトリ | |
| Configuration | 配置 | 配置 | 設定 | |
| Template | 模板 | 模板 | テンプレート | |
| Version | 版本 | 版本 | バージョン | |
| Document | 文件 | 文档 | ドキュメント | |
| Module | 模組 | 模块 | モジュール | |
| Package | 套件 | 包 | パッケージ | |
| Library | 函式庫 | 库 | ライブラリ | |
| Framework | 框架 | 框架 | フレームワーク | |

## Git & Version Control

| English | 繁體中文 | 簡體中文 | 日本語 | Notes |
|---------|---------|---------|--------|-------|
| Commit | Commit (不翻) | 提交 | コミット | Git 操作 |
| Pull Request | Pull Request (不翻) | 拉取请求 | プルリクエスト | 縮寫：PR |
| Branch | Branch (不翻) | 分支 | ブランチ | |
| Merge | Merge (不翻) | 合并 | マージ | |
| Repository | Repository (不翻) | 仓库 | リポジトリ | 縮寫：Repo |
| Fork | Fork (不翻) | 复刻 | フォーク | |
| Clone | Clone (不翻) | 克隆 | クローン | |
| Push | Push (不翻) | 推送 | プッシュ | |
| Pull | Pull (不翻) | 拉取 | プル | |
| Tag | Tag (不翻) | 标签 | タグ | |
| Release | Release (不翻) | 发布 | リリース | |

## Development Process

| English | 繁體中文 | 簡體中文 | 日本語 | Notes |
|---------|---------|---------|--------|-------|
| Development | 開發 | 开发 | 開発 | |
| Implementation | 實作 | 实现 | 実装 | |
| Testing | 測試 | 测试 | テスト | |
| Debugging | 除錯 / Debug | 调试 | デバッグ | |
| Deployment | 部署 | 部署 | デプロイ | |
| Maintenance | 維護 | 维护 | メンテナンス | |
| Refactoring | 重構 | 重构 | リファクタリング | |
| Optimization | 優化 | 优化 | 最適化 | |
| Migration | 遷移 | 迁移 | マイグレーション | |
| Upgrade | 升級 | 升级 | アップグレード | |
| Downgrade | 降級 | 降级 | ダウングレード | |
| Rollback | 回滾 | 回滚 | ロールバック | |

## Documentation

| English | 繁體中文 | 簡體中文 | 日本語 | Notes |
|---------|---------|---------|--------|-------|
| Documentation | 文件 | 文档 | ドキュメント | |
| Guide | 指南 | 指南 | ガイド | |
| Tutorial | 教學 | 教程 | チュートリアル | |
| Reference | 參考 | 参考 | リファレンス | |
| Example | 範例 | 示例 | 例 | |
| Specification | 規格 | 规格 | 仕様 | 縮寫：Spec |
| Manual | 手冊 | 手册 | マニュアル | |
| README | README (不翻) | README | README | |
| Changelog | Changelog (不翻) | 更新日志 | 変更履歴 | |

## General Naming Conventions

### Variables & Functions

**General Rules**:
- **English names preferred** for code (variables, functions, files)
- **Local language OK** for documentation, comments, UI text

**Naming Styles**:
- `camelCase` - JavaScript/TypeScript variables, functions
- `PascalCase` - Classes, React components
- `snake_case` - Python, database columns
- `kebab-case` - File names, URLs, CSS classes
- `SCREAMING_SNAKE_CASE` - Constants, environment variables

**Function Naming**:
- Use verbs: `getUserData()`, `calculateTotal()`, `fetchData()`
- Boolean returns: `isValid()`, `hasPermission()`, `canEdit()`
- Event handlers: `onClick()`, `handleSubmit()`, `onDataLoad()`

**Variable Naming**:
- Use descriptive names (avoid `a`, `b`, `temp`, `data`)
- Boolean variables: `isLoading`, `hasError`, `shouldRender`
- Arrays: Plural nouns `users`, `items`, `products`
- Objects: Singular nouns `user`, `item`, `product`

### Files & Directories

**File Naming**:
- Use kebab-case: `user-service.ts`, `api-client.py`, `data-utils.js`
- React components: PascalCase `UserProfile.tsx`, `HeaderNav.tsx`
- Config files: lowercase `package.json`, `tsconfig.json`, `.gitignore`
- Documentation: UPPERCASE or kebab-case `README.md`, `api-reference.md`

**Directory Naming**:
- Use kebab-case or snake_case
- Singular for utilities: `util/`, `helper/`, `service/`
- Plural for collections: `components/`, `models/`, `controllers/`

## Translation Notes

### When NOT to Translate

**Keep in English** (do not translate):
- Programming language keywords (`if`, `for`, `function`, `class`)
- Variable/function names in code examples
- File names and paths
- Technical terms with no established translation (e.g., `scaffolding`)
- Brand names (GitHub, VSCode, React)
- Acronyms when widely used (API, JSON, HTML, CSS)

### Domain-Specific Terms

**If a term has different meanings across domains**, see domain-specific terminology files:
- Software development: `.scaffolding/terminology/software/common.md`
- Academic: `.scaffolding/terminology/academic/common.md`
- Documentation: `.scaffolding/terminology/documentation/technical-writing.md`

**Example**:
| Term | Software Dev | Academic | Documentation |
|------|--------------|----------|---------------|
| "Framework" | 框架 (kuàngjià) | 理論框架 (lǐlùn kuàngjià) | 架構 (jiàgòu) |
| "Method" | 方法 (fāngfǎ) | 研究方法 (yánjiū fāngfǎ) | 操作方式 (cāozuò fāngshì) |

**When in doubt**: Check domain-specific file based on your `project.type` in config.toml.

## Abbreviations & Acronyms

| Abbreviation | Full Form | 中文 | 日本語 | Notes |
|--------------|-----------|------|--------|-------|
| API | Application Programming Interface | 應用程式介面 | API | 通常不翻譯 |
| CI/CD | Continuous Integration/Continuous Deployment | 持續整合/持續部署 | CI/CD | |
| CRUD | Create, Read, Update, Delete | 增查改刪 | CRUD | |
| CLI | Command-Line Interface | 命令列介面 | CLI | |
| GUI | Graphical User Interface | 圖形化介面 | GUI | |
| IDE | Integrated Development Environment | 整合開發環境 | IDE | |
| JSON | JavaScript Object Notation | JSON | JSON | 不翻譯 |
| REST | Representational State Transfer | REST | REST | 不翻譯 |
| SQL | Structured Query Language | 結構化查詢語言 | SQL | |
| UI | User Interface | 使用者介面 | UI | |
| UX | User Experience | 使用者體驗 | UX | |
| URL | Uniform Resource Locator | 統一資源定位符 | URL | |

## Usage Guidelines

### For AI Agents

1. **Check project type** in config.toml first
2. **Load domain-specific** terminology if relevant
3. **Use this file** as fallback for general terms
4. **Respect priority**: project custom > domain > common

### For Human Contributors

1. **Prefer English** for code (variables, functions, classes)
2. **Use local language** for:
   - Comments (when team prefers)
   - Documentation
   - User-facing text (UI, error messages)
   - Commit messages (follow project convention)
3. **Be consistent** within each file
4. **When translating**:
   - Check domain-specific files first
   - Use this file for general terms
   - Add new terms to appropriate domain file

### Adding New Terms

**To this file** (common terms):
- Universal tech terms (not domain-specific)
- Used across multiple project types
- No variation in meaning across domains

**To domain files** (domain terms):
- Software-specific → `software/`
- Academic-specific → `academic/`
- Documentation-specific → `documentation/`
- Project-specific → `.agents/terminology/custom.md`

## References

- **BCP 47 Language Tags**: https://www.rfc-editor.org/rfc/rfc5646.html
- **Unicode CLDR**: https://cldr.unicode.org/
- **Naming Conventions**: See `.scaffolding/docs/STYLE_GUIDE.md`
