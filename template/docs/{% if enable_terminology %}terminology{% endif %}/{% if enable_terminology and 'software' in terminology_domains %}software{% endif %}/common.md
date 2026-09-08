# Software Development - Common Terminology

**Applies to:** All software development projects (frontend, backend, fullstack, CLI, library)

**Auto-load when:** `config.toml` → `[project].type` contains "frontend", "backend", "fullstack", "cli", or "library"

**Priority:** Loaded after `terminology.md`, before domain-specific files (frontend.md, backend.md, etc.)

---

## Software Development Lifecycle (SDLC)

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Requirements | 需求 | 需求 | 要件 | 功能需求、非功能需求 |
| Specification | 規格 | 规格 | 仕様 | 技術規格書 |
| Design | 設計 | 设计 | 設計 | 架構設計、介面設計 |
| Implementation | 實作 | 实现 | 実装 | 編碼階段 |
| Testing | 測試 | 测试 | テスト | 單元測試、整合測試、端對端測試 |
| Deployment | 部署 | 部署 | デプロイ | 發佈到生產環境 |
| Maintenance | 維護 | 维护 | メンテナンス | 修復、更新、改進 |
| Deprecation | 棄用 | 弃用 | 非推奨 | 逐步淘汰舊功能 |
| End-of-Life (EOL) | 終止支援 | 终止支持 | サポート終了 | 完全停止維護 |

---

## Code Quality & Best Practices

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Clean Code | 乾淨程式碼 | 整洁代码 | クリーンコード | 可讀性高、易維護的程式碼 |
| Code Smell | 程式碼異味 | 代码坏味道 | コードの臭い | 潛在問題的徵兆 |
| Technical Debt | 技術債 | 技术债 | 技術的負債 | 為了快速交付而犧牲品質 |
| Refactoring | 重構 | 重构 | リファクタリング | 改善程式碼結構，不改變行為 |
| Code Review | 程式碼審查 | 代码审查 | コードレビュー | 同儕審查程式碼品質 |
| Pair Programming | 結對編程 | 结对编程 | ペアプログラミング | 兩人共同編寫程式碼 |
| Linter | 語法檢查器 | 代码检查器 | リンター | 自動檢查程式碼風格 |
| Formatter | 格式化工具 | 格式化工具 | フォーマッター | 自動排版程式碼 |
| Static Analysis | 靜態分析 | 静态分析 | 静的解析 | 不執行程式碼的分析 |
| Code Coverage | 程式碼覆蓋率 | 代码覆盖率 | コードカバレッジ | 測試覆蓋的程式碼比例 |

---

## Testing Terminology

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Unit Test | 單元測試 | 单元测试 | 単体テスト | 測試單一函數或類別 |
| Integration Test | 整合測試 | 集成测试 | 統合テスト | 測試模組間的互動 |
| End-to-End (E2E) Test | 端對端測試 | 端到端测试 | E2Eテスト | 模擬完整使用者流程 |
| Smoke Test | 冒煙測試 | 冒烟测试 | スモークテスト | 基本功能快速驗證 |
| Regression Test | 回歸測試 | 回归测试 | リグレッションテスト | 確保新變更不破壞既有功能 |
| Test-Driven Development (TDD) | 測試驅動開發 | 测试驱动开发 | テスト駆動開発 | 先寫測試，再寫程式碼 |
| Behavior-Driven Development (BDD) | 行為驅動開發 | 行为驱动开发 | 振る舞い駆動開発 | 以使用者行為描述測試 |
| Mock | 模擬物件 | 模拟对象 | モック | 替代真實物件進行測試 |
| Stub | 樁物件 | 桩对象 | スタブ | 提供預設回應的假物件 |
| Spy | 間諜物件 | 间谍对象 | スパイ | 記錄呼叫歷史的測試物件 |
| Test Fixture | 測試固件 | 测试固件 | テストフィクスチャ | 測試的前置條件資料 |
| Assertion | 斷言 | 断言 | アサーション | 驗證預期結果 |
| Test Suite | 測試套件 | 测试套件 | テストスイート | 一組相關測試 |
| Test Runner | 測試執行器 | 测试运行器 | テストランナー | 執行測試的工具 |

---

## Design Patterns

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Design Pattern | 設計模式 | 设计模式 | デザインパターン | 可重複使用的解決方案 |
| Singleton | 單例模式 | 单例模式 | シングルトン | 確保類別只有一個實例 |
| Factory | 工廠模式 | 工厂模式 | ファクトリ | 封裝物件創建邏輯 |
| Observer | 觀察者模式 | 观察者模式 | オブザーバー | 一對多的訂閱通知機制 |
| Strategy | 策略模式 | 策略模式 | ストラテジー | 封裝可替換的演算法 |
| Decorator | 裝飾器模式 | 装饰器模式 | デコレーター | 動態新增物件功能 |
| Adapter | 轉接器模式 | 适配器模式 | アダプター | 介面轉換 |
| Facade | 外觀模式 | 外观模式 | ファサード | 提供統一的簡化介面 |
| Proxy | 代理模式 | 代理模式 | プロキシ | 控制對物件的存取 |
| Repository | 儲存庫模式 | 仓储模式 | リポジトリ | 封裝資料存取邏輯 |
| Dependency Injection (DI) | 依賴注入 | 依赖注入 | 依存性注入 | 從外部注入依賴物件 |
| Inversion of Control (IoC) | 控制反轉 | 控制反转 | 制御の反転 | 框架控制應用程式流程 |

---

## Architecture Patterns

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Monolithic Architecture | 單體式架構 | 单体架构 | モノリシックアーキテクチャ | 所有功能在一個應用程式中 |
| Microservices | 微服務 | 微服务 | マイクロサービス | 獨立部署的小型服務 |
| Serverless | 無伺服器 | 无服务器 | サーバーレス | 雲端函數即服務 (FaaS) |
| Event-Driven Architecture | 事件驅動架構 | 事件驱动架构 | イベント駆動アーキテクチャ | 透過事件觸發行為 |
| Service-Oriented Architecture (SOA) | 服務導向架構 | 面向服务架构 | サービス指向アーキテクチャ | 基於服務的分散式系統 |
| Layered Architecture | 分層架構 | 分层架构 | レイヤードアーキテクチャ | 垂直分層（UI、Business、Data） |
| Clean Architecture | 整潔架構 | 整洁架构 | クリーンアーキテクチャ | 依賴規則、領域為核心 |
| Hexagonal Architecture | 六角形架構 | 六边形架构 | ヘキサゴナルアーキテクチャ | 也稱 Ports and Adapters |
| Model-View-Controller (MVC) | 模型-視圖-控制器 | 模型-视图-控制器 | MVC | 分離資料、介面、邏輯 |
| Model-View-ViewModel (MVVM) | 模型-視圖-視圖模型 | 模型-视图-视图模型 | MVVM | 資料繫結驅動的架構 |

---

## Development Methodologies

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Agile | 敏捷開發 | 敏捷开发 | アジャイル | 迭代式、漸進式開發 |
| Scrum | Scrum | Scrum | スクラム | 敏捷框架，固定時間衝刺 |
| Kanban | 看板 | 看板 | カンバン | 視覺化工作流程 |
| Sprint | 衝刺 | 冲刺 | スプリント | Scrum 的固定迭代週期 |
| Stand-up Meeting | 每日站會 | 每日站会 | 朝会 | 簡短的日常同步會議 |
| Retrospective | 回顧會議 | 回顾会议 | ふりかえり | 反思改進的會議 |
| User Story | 使用者故事 | 用户故事 | ユーザーストーリー | 從使用者角度描述需求 |
| Epic | 史詩 | 史诗 | エピック | 大型功能集合 |
| Backlog | 待辦清單 | 待办事项 | バックログ | 待開發的功能列表 |
| Definition of Done (DoD) | 完成定義 | 完成定义 | 完了の定義 | 任務完成的標準 |
| Velocity | 速率 | 速率 | ベロシティ | 團隊單位時間完成工作量 |
| Burndown Chart | 燃盡圖 | 燃尽图 | バーンダウンチャート | 剩餘工作量趨勢圖 |

---

## Performance & Optimization

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Performance | 效能 | 性能 | パフォーマンス | 系統執行速度與效率 |
| Optimization | 最佳化 | 优化 | 最適化 | 改善效能 |
| Bottleneck | 瓶頸 | 瓶颈 | ボトルネック | 限制效能的關鍵點 |
| Profiling | 效能分析 | 性能分析 | プロファイリング | 測量程式效能 |
| Benchmark | 基準測試 | 基准测试 | ベンチマーク | 標準化的效能測試 |
| Caching | 快取 | 缓存 | キャッシング | 儲存常用資料加速存取 |
| Lazy Loading | 延遲載入 | 延迟加载 | 遅延ロード | 需要時才載入資源 |
| Eager Loading | 預先載入 | 预加载 | 先行ロード | 提前載入所需資源 |
| Throttling | 節流 | 节流 | スロットリング | 限制執行頻率 |
| Debouncing | 防抖 | 防抖 | デバウンス | 延遲執行直到停止觸發 |
| Memoization | 記憶化 | 记忆化 | メモ化 | 快取函數運算結果 |
| Load Balancing | 負載平衡 | 负载均衡 | ロードバランシング | 分散流量到多個伺服器 |
| Scalability | 可擴展性 | 可扩展性 | スケーラビリティ | 系統應對增長的能力 |
| Horizontal Scaling | 水平擴展 | 水平扩展 | 水平スケーリング | 增加伺服器數量 |
| Vertical Scaling | 垂直擴展 | 垂直扩展 | 垂直スケーリング | 提升單一伺服器效能 |

---

## Security

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Authentication | 驗證 | 认证 | 認証 | 確認使用者身分 |
| Authorization | 授權 | 授权 | 認可 | 控制存取權限 |
| Encryption | 加密 | 加密 | 暗号化 | 資料保護 |
| Hashing | 雜湊 | 哈希 | ハッシュ化 | 單向加密 |
| Salt | 鹽值 | 盐值 | ソルト | 密碼加密的隨機值 |
| Token | 令牌 | 令牌 | トークン | 身分憑證 |
| JSON Web Token (JWT) | JSON 網頁令牌 | JSON网页令牌 | JSON Web Token | 無狀態身分驗證 |
| OAuth | OAuth | OAuth | OAuth | 第三方授權協定 |
| Cross-Site Scripting (XSS) | 跨站腳本攻擊 | 跨站脚本攻击 | クロスサイトスクリプティング | 注入惡意腳本 |
| Cross-Site Request Forgery (CSRF) | 跨站請求偽造 | 跨站请求伪造 | クロスサイトリクエストフォージェリ | 偽造使用者請求 |
| SQL Injection | SQL 注入 | SQL注入 | SQLインジェクション | 惡意 SQL 查詢攻擊 |
| Man-in-the-Middle (MITM) | 中間人攻擊 | 中间人攻击 | 中間者攻撃 | 攔截通訊 |
| Denial of Service (DoS) | 阻斷服務攻擊 | 拒绝服务攻击 | サービス拒否攻撃 | 癱瘓系統 |
| Penetration Testing | 滲透測試 | 渗透测试 | ペネトレーションテスト | 模擬攻擊找漏洞 |
| Security Audit | 安全稽核 | 安全审计 | セキュリティ監査 | 檢查安全性 |

---

## Error Handling

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Exception | 例外 | 异常 | 例外 | 執行時錯誤 |
| Error Handling | 錯誤處理 | 错误处理 | エラーハンドリング | 捕捉並處理錯誤 |
| Try-Catch | Try-Catch | Try-Catch | Try-Catch | 錯誤捕捉語法 |
| Throw | 拋出 | 抛出 | スロー | 觸發例外 |
| Stack Trace | 堆疊追蹤 | 堆栈跟踪 | スタックトレース | 錯誤呼叫鏈 |
| Logging | 日誌記錄 | 日志记录 | ロギング | 記錄系統事件 |
| Error Message | 錯誤訊息 | 错误消息 | エラーメッセージ | 描述錯誤的文字 |
| Fallback | 備案 | 回退 | フォールバック | 失敗時的替代方案 |
| Graceful Degradation | 優雅降級 | 优雅降级 | グレースフルデグラデーション | 功能失效時仍可運作 |
| Fail-fast | 快速失敗 | 快速失败 | フェイルファスト | 立即回報錯誤 |
| Retry Logic | 重試邏輯 | 重试逻辑 | リトライロジック | 失敗後自動重試 |
| Circuit Breaker | 斷路器 | 断路器 | サーキットブレーカー | 防止連鎖失效 |

---

## Documentation

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Documentation | 文件 | 文档 | ドキュメント | 說明文件 |
| Inline Comment | 行內註解 | 行内注释 | インラインコメント | 程式碼中的說明 |
| Docstring | 文件字串 | 文档字符串 | ドキュメント文字列 | 函數/類別的說明 |
| README | README | README | README | 專案說明文件 |
| Changelog | 變更日誌 | 变更日志 | 変更履歴 | 版本更新記錄 |
| API Documentation | API 文件 | API文档 | APIドキュメント | 介面使用說明 |
| User Guide | 使用者指南 | 用户指南 | ユーザーガイド | 最終使用者文件 |
| Developer Guide | 開發者指南 | 开发者指南 | 開発者ガイド | 開發人員文件 |
| Architecture Decision Record (ADR) | 架構決策記錄 | 架构决策记录 | アーキテクチャ決定記録 | 記錄重大技術決策 |
| Runbook | 維運手冊 | 运维手册 | ランブック | 故障排除指南 |

---

## Continuous Integration / Continuous Deployment (CI/CD)

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Continuous Integration (CI) | 持續整合 | 持续集成 | 継続的インテグレーション | 自動化測試與整合 |
| Continuous Deployment (CD) | 持續部署 | 持续部署 | 継続的デプロイ | 自動化發佈到生產環境 |
| Continuous Delivery | 持續交付 | 持续交付 | 継続的デリバリー | 隨時可部署的狀態 |
| Pipeline | 管線 | 流水线 | パイプライン | CI/CD 工作流程 |
| Build | 建置 | 构建 | ビルド | 編譯與打包 |
| Artifact | 建置產物 | 构建产物 | アーティファクト | 建置輸出檔案 |
| Blue-Green Deployment | 藍綠部署 | 蓝绿部署 | ブルーグリーンデプロイメント | 兩套環境切換 |
| Canary Release | 金絲雀發布 | 金丝雀发布 | カナリアリリース | 漸進式發布 |
| Rolling Update | 滾動更新 | 滚动更新 | ローリングアップデート | 逐步更新實例 |
| Rollback | 回滾 | 回滚 | ロールバック | 恢復到前一版本 |
| Smoke Test | 冒煙測試 | 冒烟测试 | スモークテスト | 部署後基本驗證 |

---

## Notes

### Context-Specific Translations

**「實作」vs「實現」(Implementation)**:
- 🇹🇼 TW: 優先使用「實作」（實際製作、編碼）
- 🇨🇳 CN: 優先使用「实现」（實現功能）

**「效能」vs「性能」(Performance)**:
- 🇹🇼 TW: 使用「效能」（功效與效率）
- 🇨🇳 CN: 使用「性能」（系統表現）
- 🇯🇵 JP: 使用「パフォーマンス」（外來語）

**「快取」vs「緩存」(Cache)**:
- 🇹🇼 TW: 使用「快取」（加速存取）
- 🇨🇳 CN: 使用「缓存」（緩衝儲存）

**「驗證」vs「認證」(Authentication)**:
- 🇹🇼 TW: 使用「驗證」（確認身分）
- 🇨🇳 CN: 使用「认证」（認可身分）
- 🇯🇵 JP: 使用「認証」（確認）

**「授權」(Authorization)**:
- 所有語系同義，但意義不同於 Authentication
- Authentication = 你是誰？
- Authorization = 你能做什麼？

### Abbreviation Guidelines

保持原文縮寫，但首次出現時提供完整翻譯：

- API = 應用程式介面 (Application Programming Interface)
- CI/CD = 持續整合/持續部署
- TDD = 測試驅動開發
- MVC = 模型-視圖-控制器
- JWT = JSON 網頁令牌
- XSS = 跨站腳本攻擊
- CSRF = 跨站請求偽造
- DoS = 阻斷服務攻擊

### Usage in Documentation

當撰寫技術文件時：

1. **首次提及**：使用「英文 (中文翻譯)」格式
   - 範例：Refactoring (重構) 是改善程式碼結構的過程...

2. **後續提及**：可直接使用英文或中文
   - 範例：重構時應保持測試通過...

3. **程式碼中**：優先使用英文
   - 變數名稱、函數名稱、註解關鍵詞使用英文

4. **使用者文件**：優先使用中文
   - README、操作手冊、錯誤訊息使用在地化語言
