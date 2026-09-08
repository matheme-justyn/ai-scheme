# Software Development - Backend Terminology

**Applies to:** Backend and fullstack projects

**Auto-load when:** `config.toml` → `[project].type` contains "backend" or "fullstack"

**Priority:** Loaded after `common.md`

---

## Core Backend Concepts

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Server | 伺服器 | 服务器 | サーバー | 提供服務的程式或機器 |
| Client | 客戶端 | 客户端 | クライアント | 發送請求的程式或機器 |
| Endpoint | 端點 | 端点 | エンドポイント | API 路由 |
| Route | 路由 | 路由 | ルート | URL 路徑對應 |
| Handler | 處理器 | 处理器 | ハンドラー | 處理請求的函數 |
| Controller | 控制器 | 控制器 | コントローラー | 處理業務邏輯 |
| Service | 服務 | 服务 | サービス | 封裝業務邏輯 |
| Model | 模型 | 模型 | モデル | 資料結構定義 |
| Middleware | 中介軟體 | 中间件 | ミドルウェア | 請求處理鏈中的攔截器 |
| Request | 請求 | 请求 | リクエスト | 客戶端發送的訊息 |
| Response | 回應 | 响应 | レスポンス | 伺服器返回的訊息 |
| Payload | 載荷 | 载荷 | ペイロード | 請求或回應的資料內容 |
| Header | 標頭 | 标头 | ヘッダー | HTTP 請求/回應的元資料 |
| Body | 主體 | 主体 | ボディ | 請求/回應的內容 |
| Query Parameter | 查詢參數 | 查询参数 | クエリパラメータ | URL 中的 ?key=value |
| Path Parameter | 路徑參數 | 路径参数 | パスパラメータ | URL 路徑中的變數 |

---

## HTTP & RESTful API

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| HTTP | HTTP | HTTP | HTTP | HyperText Transfer Protocol |
| HTTPS | HTTPS | HTTPS | HTTPS | HTTP Secure |
| REST | REST | REST | REST | Representational State Transfer |
| RESTful API | RESTful API | RESTful API | RESTful API | 符合 REST 原則的 API |
| GET | GET | GET | GET | 讀取資源 |
| POST | POST | POST | POST | 建立資源 |
| PUT | PUT | PUT | PUT | 完整更新資源 |
| PATCH | PATCH | PATCH | PATCH | 部分更新資源 |
| DELETE | DELETE | DELETE | DELETE | 刪除資源 |
| Status Code | 狀態碼 | 状态码 | ステータスコード | HTTP 回應狀態 |
| 200 OK | 200 成功 | 200 成功 | 200 OK | 請求成功 |
| 201 Created | 201 已建立 | 201 已创建 | 201 Created | 資源已建立 |
| 400 Bad Request | 400 錯誤請求 | 400 错误请求 | 400 Bad Request | 客戶端錯誤 |
| 401 Unauthorized | 401 未授權 | 401 未授权 | 401 Unauthorized | 未驗證身分 |
| 403 Forbidden | 403 禁止存取 | 403 禁止访问 | 403 Forbidden | 無權限 |
| 404 Not Found | 404 找不到 | 404 未找到 | 404 Not Found | 資源不存在 |
| 500 Internal Server Error | 500 伺服器錯誤 | 500 服务器错误 | 500 Internal Server Error | 伺服器內部錯誤 |
| CRUD | CRUD | CRUD | CRUD | Create, Read, Update, Delete |
| Idempotent | 冪等 | 幂等 | 冪等 | 多次執行結果相同 |
| Stateless | 無狀態 | 无状态 | ステートレス | 不保存客戶端狀態 |

---

## API Design & Standards

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| API Gateway | API 閘道 | API网关 | APIゲートウェイ | 統一入口 |
| GraphQL | GraphQL | GraphQL | GraphQL | 查詢語言 |
| gRPC | gRPC | gRPC | gRPC | 高效能 RPC 框架 |
| WebSocket | WebSocket | WebSocket | WebSocket | 全雙工通訊 |
| Server-Sent Events (SSE) | 伺服器推送事件 | 服务器推送事件 | Server-Sent Events | 單向即時推送 |
| Webhook | Webhook | Webhook | Webhook | HTTP 回調 |
| API Versioning | API 版本控制 | API版本控制 | APIバージョン管理 | /v1/, /v2/ |
| Rate Limiting | 速率限制 | 速率限制 | レート制限 | 限制請求頻率 |
| Throttling | 節流 | 节流 | スロットリング | 限制處理速度 |
| Pagination | 分頁 | 分页 | ページネーション | 分批回傳資料 |
| Filtering | 篩選 | 筛选 | フィルタリング | 條件查詢 |
| Sorting | 排序 | 排序 | ソート | 資料排列 |
| HATEOAS | HATEOAS | HATEOAS | HATEOAS | 超媒體驅動的 API |
| OpenAPI / Swagger | OpenAPI / Swagger | OpenAPI / Swagger | OpenAPI / Swagger | API 規格文件 |
| JSON Schema | JSON Schema | JSON Schema | JSON Schema | JSON 資料結構驗證 |

---

## Authentication & Authorization

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Authentication | 驗證 | 认证 | 認証 | 確認使用者身分 |
| Authorization | 授權 | 授权 | 認可 | 控制存取權限 |
| Session | 會話 | 会话 | セッション | 使用者狀態追蹤 |
| Cookie | Cookie | Cookie | クッキー | 瀏覽器儲存的小資料 |
| Token | 令牌 | 令牌 | トークン | 身分憑證 |
| JWT | JWT | JWT | JWT | JSON Web Token |
| Access Token | 存取令牌 | 访问令牌 | アクセストークン | 短期憑證 |
| Refresh Token | 更新令牌 | 刷新令牌 | リフレッシュトークン | 長期憑證 |
| OAuth 2.0 | OAuth 2.0 | OAuth 2.0 | OAuth 2.0 | 授權框架 |
| OpenID Connect | OpenID Connect | OpenID Connect | OpenID Connect | 身分認證層 |
| Single Sign-On (SSO) | 單一登入 | 单点登录 | シングルサインオン | 一次登入多服務 |
| Two-Factor Authentication (2FA) | 雙因素驗證 | 双因素认证 | 二要素認証 | 多重驗證 |
| Multi-Factor Authentication (MFA) | 多因素驗證 | 多因素认证 | 多要素認証 | 多重驗證 |
| Role-Based Access Control (RBAC) | 角色基礎存取控制 | 基于角色的访问控制 | ロールベースアクセス制御 | 依角色控制權限 |
| Attribute-Based Access Control (ABAC) | 屬性基礎存取控制 | 基于属性的访问控制 | 属性ベースアクセス制御 | 依屬性控制權限 |
| API Key | API 金鑰 | API密钥 | APIキー | 應用程式識別 |
| Bearer Token | Bearer Token | Bearer令牌 | Bearer Token | HTTP Authorization 標頭 |
| Basic Authentication | 基本驗證 | 基本认证 | Basic認証 | Base64 編碼的使用者名稱與密碼 |

---

## Node.js & JavaScript Runtime

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Node.js | Node.js | Node.js | Node.js | JavaScript 執行環境 |
| Deno | Deno | Deno | Deno | 安全的 JavaScript/TypeScript 執行環境 |
| Bun | Bun | Bun | Bun | 快速的 JavaScript 執行環境 |
| Express | Express | Express | Express | Node.js 網頁框架 |
| Koa | Koa | Koa | Koa | 輕量級 Node.js 框架 |
| Fastify | Fastify | Fastify | Fastify | 高效能 Node.js 框架 |
| NestJS | NestJS | NestJS | NestJS | TypeScript 企業級框架 |
| Event Loop | 事件迴圈 | 事件循环 | イベントループ | 非阻塞 I/O 機制 |
| Callback | 回呼 | 回调 | コールバック | 非同步處理函數 |
| Promise | Promise | Promise | Promise | 非同步操作物件 |
| Async/Await | Async/Await | Async/Await | Async/Await | 非同步語法糖 |
| Stream | 串流 | 流 | ストリーム | 連續資料處理 |
| Buffer | 緩衝區 | 缓冲区 | バッファ | 二進位資料處理 |
| Process | 程序 | 进程 | プロセス | 執行中的應用程式 |
| Thread | 執行緒 | 线程 | スレッド | 程序內的執行單元 |
| Worker Thread | 工作執行緒 | 工作线程 | ワーカースレッド | Node.js 多執行緒 |
| Cluster | 叢集 | 集群 | クラスター | 多程序負載平衡 |

---

## Database & ORM

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Database | 資料庫 | 数据库 | データベース | 資料儲存系統 |
| Relational Database | 關聯式資料庫 | 关系型数据库 | リレーショナルデータベース | SQL 資料庫 |
| NoSQL | NoSQL | NoSQL | NoSQL | 非關聯式資料庫 |
| ORM | ORM | ORM | ORM | Object-Relational Mapping |
| Query | 查詢 | 查询 | クエリ | 資料庫請求 |
| Transaction | 交易 | 事务 | トランザクション | 原子性操作 |
| ACID | ACID | ACID | ACID | Atomicity, Consistency, Isolation, Durability |
| Schema | 架構 | 模式 | スキーマ | 資料表結構定義 |
| Migration | 遷移 | 迁移 | マイグレーション | 資料庫結構變更 |
| Seed | 種子資料 | 种子数据 | シードデータ | 初始化資料 |
| Connection Pool | 連線池 | 连接池 | コネクションプール | 重複使用資料庫連線 |
| Prepared Statement | 預編譯語句 | 预编译语句 | プリペアドステートメント | 防止 SQL 注入 |
| Stored Procedure | 預存程序 | 存储过程 | ストアドプロシージャ | 資料庫中的函數 |
| Trigger | 觸發器 | 触发器 | トリガー | 自動執行的資料庫邏輯 |
| View | 視圖 | 视图 | ビュー | 虛擬資料表 |
| Index | 索引 | 索引 | インデックス | 加速查詢 |
| Foreign Key | 外鍵 | 外键 | 外部キー | 關聯其他資料表 |
| Primary Key | 主鍵 | 主键 | 主キー | 唯一識別 |
| Composite Key | 複合鍵 | 复合键 | 複合キー | 多欄位主鍵 |

---

## Popular Databases

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| PostgreSQL | PostgreSQL | PostgreSQL | PostgreSQL | 開源關聯式資料庫 |
| MySQL | MySQL | MySQL | MySQL | 流行關聯式資料庫 |
| SQLite | SQLite | SQLite | SQLite | 輕量級嵌入式資料庫 |
| MongoDB | MongoDB | MongoDB | MongoDB | 文件導向 NoSQL |
| Redis | Redis | Redis | Redis | 記憶體鍵值資料庫 |
| Elasticsearch | Elasticsearch | Elasticsearch | Elasticsearch | 搜尋引擎 |
| Cassandra | Cassandra | Cassandra | Cassandra | 分散式 NoSQL |
| DynamoDB | DynamoDB | DynamoDB | DynamoDB | AWS 託管 NoSQL |
| Firestore | Firestore | Firestore | Firestore | Google 雲端 NoSQL |
| Supabase | Supabase | Supabase | Supabase | 開源 Firebase 替代品 |
| Prisma | Prisma | Prisma | Prisma | 現代 TypeScript ORM |
| Drizzle ORM | Drizzle ORM | Drizzle ORM | Drizzle ORM | 輕量型 TypeScript ORM |
| Sequelize | Sequelize | Sequelize | Sequelize | Node.js ORM |
| TypeORM | TypeORM | TypeORM | TypeORM | TypeScript ORM |
| Mongoose | Mongoose | Mongoose | Mongoose | MongoDB ORM |

---

## Caching & Message Queues

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Cache | 快取 | 缓存 | キャッシュ | 暫存資料加速存取 |
| Cache Hit | 快取命中 | 缓存命中 | キャッシュヒット | 找到快取資料 |
| Cache Miss | 快取未中 | 缓存未命中 | キャッシュミス | 未找到快取資料 |
| Cache Invalidation | 快取失效 | 缓存失效 | キャッシュ無効化 | 清除舊快取 |
| TTL | TTL | TTL | TTL | Time To Live，存活時間 |
| In-Memory Cache | 記憶體快取 | 内存缓存 | インメモリキャッシュ | RAM 中的快取 |
| Distributed Cache | 分散式快取 | 分布式缓存 | 分散キャッシュ | 跨伺服器快取 |
| Message Queue | 訊息佇列 | 消息队列 | メッセージキュー | 非同步訊息傳遞 |
| Message Broker | 訊息代理 | 消息代理 | メッセージブローカー | 訊息中介 |
| Publisher | 發布者 | 发布者 | パブリッシャー | 發送訊息的角色 |
| Subscriber | 訂閱者 | 订阅者 | サブスクライバー | 接收訊息的角色 |
| Pub/Sub | 發布/訂閱 | 发布/订阅 | Pub/Sub | 訊息模式 |
| Queue | 佇列 | 队列 | キュー | 先進先出資料結構 |
| Topic | 主題 | 主题 | トピック | 訊息分類 |
| Dead Letter Queue | 死信佇列 | 死信队列 | デッドレターキュー | 失敗訊息儲存 |
| RabbitMQ | RabbitMQ | RabbitMQ | RabbitMQ | 訊息佇列中介軟體 |
| Apache Kafka | Apache Kafka | Apache Kafka | Apache Kafka | 分散式串流平台 |
| AWS SQS | AWS SQS | AWS SQS | AWS SQS | Amazon 訊息佇列服務 |
| BullMQ | BullMQ | BullMQ | BullMQ | Node.js 工作佇列 |

---

## Microservices & Distributed Systems

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Microservices | 微服務 | 微服务 | マイクロサービス | 獨立部署的小型服務 |
| Service Mesh | 服務網格 | 服务网格 | サービスメッシュ | 服務間通訊層 |
| API Gateway | API 閘道 | API网关 | APIゲートウェイ | 統一入口 |
| Service Discovery | 服務探索 | 服务发现 | サービスディスカバリー | 自動找到服務位址 |
| Load Balancer | 負載平衡器 | 负载均衡器 | ロードバランサー | 分散流量 |
| Circuit Breaker | 斷路器 | 断路器 | サーキットブレーカー | 防止連鎖失效 |
| Retry Logic | 重試邏輯 | 重试逻辑 | リトライロジック | 失敗後自動重試 |
| Timeout | 逾時 | 超时 | タイムアウト | 限制等待時間 |
| Backpressure | 背壓 | 背压 | バックプレッシャー | 流量控制 |
| Rate Limiting | 速率限制 | 速率限制 | レート制限 | 限制請求頻率 |
| Distributed Tracing | 分散式追蹤 | 分布式追踪 | 分散トレーシング | 跨服務追蹤請求 |
| Saga Pattern | Saga 模式 | Saga模式 | Sagaパターン | 分散式交易 |
| Event Sourcing | 事件溯源 | 事件溯源 | イベントソーシング | 儲存狀態變更事件 |
| CQRS | CQRS | CQRS | CQRS | Command Query Responsibility Segregation |
| Container | 容器 | 容器 | コンテナ | 應用程式封裝 |
| Docker | Docker | Docker | Docker | 容器化平台 |
| Kubernetes | Kubernetes | Kubernetes | Kubernetes | 容器編排系統 |
| Orchestration | 編排 | 编排 | オーケストレーション | 自動化管理 |

---

## Logging & Monitoring

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Logging | 日誌記錄 | 日志记录 | ロギング | 記錄系統事件 |
| Log Level | 日誌等級 | 日志级别 | ログレベル | 訊息重要性 |
| Debug | 除錯 | 调试 | デバッグ | 開發階段訊息 |
| Info | 資訊 | 信息 | 情報 | 一般訊息 |
| Warning | 警告 | 警告 | 警告 | 潛在問題 |
| Error | 錯誤 | 错误 | エラー | 執行失敗 |
| Fatal | 致命錯誤 | 致命错误 | 致命的エラー | 系統崩潰 |
| Structured Logging | 結構化日誌 | 结构化日志 | 構造化ログ | JSON 格式日誌 |
| Log Aggregation | 日誌聚合 | 日志聚合 | ログ集約 | 集中收集日誌 |
| Monitoring | 監控 | 监控 | モニタリング | 追蹤系統狀態 |
| Metrics | 指標 | 指标 | メトリクス | 量化數據 |
| Alert | 警報 | 告警 | アラート | 異常通知 |
| Dashboard | 儀表板 | 仪表板 | ダッシュボード | 視覺化介面 |
| APM | APM | APM | APM | Application Performance Monitoring |
| Observability | 可觀測性 | 可观测性 | オブザーバビリティ | 系統內部狀態透明度 |
| Telemetry | 遙測 | 遥测 | テレメトリ | 自動收集資料 |
| Health Check | 健康檢查 | 健康检查 | ヘルスチェック | 服務狀態確認 |
| Uptime | 正常運作時間 | 正常运行时间 | 稼働時間 | 服務可用時間 |
| Downtime | 停機時間 | 停机时间 | ダウンタイム | 服務不可用時間 |

---

## Security

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Encryption | 加密 | 加密 | 暗号化 | 資料保護 |
| Hashing | 雜湊 | 哈希 | ハッシュ化 | 單向加密 |
| Salt | 鹽值 | 盐值 | ソルト | 密碼加密的隨機值 |
| bcrypt | bcrypt | bcrypt | bcrypt | 密碼雜湊演算法 |
| SSL/TLS | SSL/TLS | SSL/TLS | SSL/TLS | 傳輸層加密 |
| Certificate | 憑證 | 证书 | 証明書 | 數位證書 |
| SQL Injection | SQL 注入 | SQL注入 | SQLインジェクション | 惡意 SQL 查詢攻擊 |
| XSS | XSS | XSS | XSS | Cross-Site Scripting |
| CSRF | CSRF | CSRF | CSRF | Cross-Site Request Forgery |
| CORS | CORS | CORS | CORS | Cross-Origin Resource Sharing |
| Same-Origin Policy | 同源政策 | 同源策略 | 同一オリジンポリシー | 瀏覽器安全限制 |
| Content Security Policy (CSP) | 內容安全政策 | 内容安全策略 | コンテンツセキュリティポリシー | 防止 XSS |
| Input Validation | 輸入驗證 | 输入验证 | 入力検証 | 檢查使用者輸入 |
| Sanitization | 淨化 | 清理 | サニタイズ | 清除危險字元 |
| Rate Limiting | 速率限制 | 速率限制 | レート制限 | 防止濫用 |
| DDoS | DDoS | DDoS | DDoS | Distributed Denial of Service |
| Firewall | 防火牆 | 防火墙 | ファイアウォール | 網路安全屏障 |

---

## Deployment & DevOps

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Deployment | 部署 | 部署 | デプロイ | 發佈到生產環境 |
| CI/CD | CI/CD | CI/CD | CI/CD | 持續整合/持續部署 |
| Pipeline | 管線 | 流水线 | パイプライン | 自動化工作流程 |
| Build | 建置 | 构建 | ビルド | 編譯與打包 |
| Artifact | 建置產物 | 构建产物 | アーティファクト | 建置輸出檔案 |
| Environment | 環境 | 环境 | 環境 | Development, Staging, Production |
| Production | 生產環境 | 生产环境 | 本番環境 | 正式環境 |
| Staging | 預發布環境 | 预发布环境 | ステージング環境 | 測試環境 |
| Development | 開發環境 | 开发环境 | 開発環境 | 開發階段環境 |
| Rollback | 回滾 | 回滚 | ロールバック | 恢復到前一版本 |
| Blue-Green Deployment | 藍綠部署 | 蓝绿部署 | ブルーグリーンデプロイメント | 兩套環境切換 |
| Canary Release | 金絲雀發布 | 金丝雀发布 | カナリアリリース | 漸進式發布 |
| Zero-Downtime Deployment | 零停機部署 | 零停机部署 | ゼロダウンタイムデプロイ | 不中斷服務的部署 |
| Infrastructure as Code (IaC) | 基礎設施即程式碼 | 基础设施即代码 | Infrastructure as Code | 程式化管理基礎設施 |
| Terraform | Terraform | Terraform | Terraform | IaC 工具 |
| Ansible | Ansible | Ansible | Ansible | 自動化配置管理 |

---

## Notes

### Context-Specific Translations

**「驗證」vs「認證」(Authentication)**:
- 🇹🇼 TW: 使用「驗證」（確認身分）
- 🇨🇳 CN: 使用「认证」（認可身分）
- 🇯🇵 JP: 使用「認証」（確認）

**「授權」(Authorization)**:
- 所有語系同義，但與 Authentication 不同
- Authentication = 你是誰？
- Authorization = 你能做什麼？

**「快取」vs「緩存」(Cache)**:
- 🇹🇼 TW: 使用「快取」（加速存取）
- 🇨🇳 CN: 使用「缓存」（緩衝儲存）

**「伺服器」vs「服務器」(Server)**:
- 🇹🇼 TW: 使用「伺服器」（serve + er）
- 🇨🇳 CN: 使用「服务器」（服務機器）

**「資料庫」vs「數據庫」(Database)**:
- 🇹🇼 TW: 使用「資料庫」（data）
- 🇨🇳 CN: 使用「数据库」（數據）

### Database Translation Nuances

**「架構」vs「模式」(Schema)**:
- 🇹🇼 TW: 「架構」更常用（結構之意）
- 🇨🇳 CN: 「模式」更常用（Pattern 之意）
- Context: 資料表結構定義

**「遷移」(Migration)**:
- 資料庫結構變更管理
- 不翻譯為「移民」或「搬遷」

**「種子資料」(Seed)**:
- 初始化測試資料
- 不翻譯為「種子」（農業）

### HTTP Status Code Usage

當回報狀態碼時，保持數字 + 英文名稱：

```javascript
// ✅ Good - 保持國際慣例
return res.status(404).json({ error: '找不到資源' })
throw new Error('401 Unauthorized: 請先登入')

// ❌ Bad - 完全中文化
return res.status(404).json({ error: '404 找不到' })
throw new Error('401 未授權: 請先登入')
```

### Async Pattern Naming

**「回呼」vs「回調」(Callback)**:
- 🇹🇼 TW: 使用「回呼」（call back）
- 🇨🇳 CN: 使用「回调」（回頭調用）

**Promise 與 Async/Await**:
- 保持英文，不翻譯為「承諾」或「非同步/等待」
- 程式碼中直接使用 async/await 關鍵字

### Logging Level Conventions

當記錄日誌時，保持英文等級名稱：

```javascript
// ✅ Good - 英文等級
logger.debug('查詢參數:', params)
logger.info('使用者登入成功')
logger.warn('快取即將過期')
logger.error('資料庫連線失敗', error)

// ❌ Bad - 中文等級
logger.除錯('查詢參數:', params)
logger.資訊('使用者登入成功')
```

### Security Term Usage

安全相關術語保持嚴肅性，避免俚語：

- SQL Injection = SQL 注入（不說「SQL 隱碼攻擊」）
- XSS = 跨站腳本攻擊（不說「跨站指令碼」）
- CSRF = 跨站請求偽造（不說「跨站冒充」）

### Abbreviation Guidelines

後端常用縮寫：

- API = 應用程式介面 (Application Programming Interface)
- REST = Representational State Transfer
- CRUD = Create, Read, Update, Delete
- JWT = JSON Web Token
- ORM = Object-Relational Mapping
- ACID = Atomicity, Consistency, Isolation, Durability
- CORS = Cross-Origin Resource Sharing
- TTL = Time To Live
- APM = Application Performance Monitoring
- IaC = Infrastructure as Code
