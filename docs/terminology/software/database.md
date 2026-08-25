# Software Development - Database Terminology

**Applies to:** Projects using databases (fullstack, backend)

**Auto-load when:** `config.toml` → `[project].features` contains "database"

**Priority:** Loaded after `backend.md`

---

## Core Database Concepts

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Database | 資料庫 | 数据库 | データベース | 資料儲存系統 |
| Table | 資料表 | 表 | テーブル | 關聯式資料庫的資料集合 |
| Row | 列 | 行 | 行 | 一筆資料 |
| Column | 欄位 | 列 | カラム | 資料屬性 |
| Field | 欄位 | 字段 | フィールド | 同 Column |
| Record | 記錄 | 记录 | レコード | 同 Row |
| Schema | 架構 | 模式 | スキーマ | 資料表結構定義 |
| Entity | 實體 | 实体 | エンティティ | 資料物件 |
| Attribute | 屬性 | 属性 | 属性 | 實體的特徵 |
| Relationship | 關聯 | 关系 | リレーション | 實體間的連結 |
| Constraint | 約束 | 约束 | 制約 | 資料規則限制 |

---

## SQL Fundamentals

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| SQL | SQL | SQL | SQL | Structured Query Language |
| Query | 查詢 | 查询 | クエリ | 資料庫請求 |
| SELECT | SELECT | SELECT | SELECT | 讀取資料 |
| INSERT | INSERT | INSERT | INSERT | 新增資料 |
| UPDATE | UPDATE | UPDATE | UPDATE | 更新資料 |
| DELETE | DELETE | DELETE | DELETE | 刪除資料 |
| WHERE | WHERE | WHERE | WHERE | 條件篩選 |
| JOIN | JOIN | JOIN | JOIN | 連接多張資料表 |
| INNER JOIN | INNER JOIN | INNER JOIN | INNER JOIN | 內連接（交集） |
| LEFT JOIN | LEFT JOIN | LEFT JOIN | LEFT JOIN | 左外連接 |
| RIGHT JOIN | RIGHT JOIN | RIGHT JOIN | RIGHT JOIN | 右外連接 |
| FULL OUTER JOIN | FULL OUTER JOIN | FULL OUTER JOIN | FULL OUTER JOIN | 全外連接 |
| GROUP BY | GROUP BY | GROUP BY | GROUP BY | 分組聚合 |
| ORDER BY | ORDER BY | ORDER BY | ORDER BY | 排序 |
| HAVING | HAVING | HAVING | HAVING | 分組後篩選 |
| LIMIT | LIMIT | LIMIT | LIMIT | 限制回傳筆數 |
| OFFSET | OFFSET | OFFSET | OFFSET | 跳過前 N 筆 |
| DISTINCT | DISTINCT | DISTINCT | DISTINCT | 去除重複 |
| UNION | UNION | UNION | UNION | 合併查詢結果 |
| Subquery | 子查詢 | 子查询 | サブクエリ | 巢狀查詢 |
| Aggregate Function | 聚合函數 | 聚合函数 | 集約関数 | COUNT, SUM, AVG, MAX, MIN |

---

## Keys & Constraints

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Primary Key | 主鍵 | 主键 | 主キー | 唯一識別欄位 |
| Foreign Key | 外鍵 | 外键 | 外部キー | 參照其他資料表 |
| Composite Key | 複合鍵 | 复合键 | 複合キー | 多欄位主鍵 |
| Unique Key | 唯一鍵 | 唯一键 | ユニークキー | 唯一值約束 |
| NOT NULL | NOT NULL | NOT NULL | NOT NULL | 不可為空 |
| DEFAULT | DEFAULT | DEFAULT | DEFAULT | 預設值 |
| CHECK | CHECK | CHECK | CHECK | 自訂驗證規則 |
| CASCADE | CASCADE | CASCADE | CASCADE | 連鎖操作 |
| RESTRICT | RESTRICT | RESTRICT | RESTRICT | 限制刪除/更新 |
| SET NULL | SET NULL | SET NULL | SET NULL | 設為 NULL |
| AUTO INCREMENT | AUTO INCREMENT | AUTO INCREMENT | AUTO INCREMENT | 自動遞增 |

---

## Indexing & Performance

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Index | 索引 | 索引 | インデックス | 加速查詢 |
| Primary Index | 主索引 | 主索引 | 主インデックス | 主鍵自動建立 |
| Secondary Index | 次要索引 | 辅助索引 | セカンダリインデックス | 非主鍵索引 |
| Unique Index | 唯一索引 | 唯一索引 | ユニークインデックス | 唯一值索引 |
| Composite Index | 複合索引 | 复合索引 | 複合インデックス | 多欄位索引 |
| Full-Text Index | 全文索引 | 全文索引 | フルテキストインデックス | 文字搜尋索引 |
| B-Tree | B-Tree | B树 | B木 | 平衡樹索引 |
| Hash Index | 雜湊索引 | 哈希索引 | ハッシュインデックス | 等值查詢索引 |
| Query Optimization | 查詢最佳化 | 查询优化 | クエリ最適化 | 提升查詢效能 |
| Execution Plan | 執行計畫 | 执行计划 | 実行計画 | 查詢執行步驟 |
| Query Cache | 查詢快取 | 查询缓存 | クエリキャッシュ | 快取查詢結果 |
| Slow Query | 慢查詢 | 慢查询 | スロークエリ | 執行時間過長的查詢 |
| N+1 Problem | N+1 問題 | N+1问题 | N+1問題 | 過多關聯查詢 |
| Eager Loading | 預先載入 | 预加载 | 先行ロード | 一次載入關聯資料 |
| Lazy Loading | 延遲載入 | 延迟加载 | 遅延ロード | 需要時才載入 |

---

## Transactions & ACID

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Transaction | 交易 | 事务 | トランザクション | 原子性操作單元 |
| ACID | ACID | ACID | ACID | Atomicity, Consistency, Isolation, Durability |
| Atomicity | 原子性 | 原子性 | 原子性 | 全做或全不做 |
| Consistency | 一致性 | 一致性 | 一貫性 | 符合所有規則 |
| Isolation | 隔離性 | 隔离性 | 独立性 | 交易互不干擾 |
| Durability | 持久性 | 持久性 | 永続性 | 提交後永久保存 |
| COMMIT | COMMIT | COMMIT | COMMIT | 提交交易 |
| ROLLBACK | ROLLBACK | ROLLBACK | ROLLBACK | 回滾交易 |
| SAVEPOINT | SAVEPOINT | SAVEPOINT | SAVEPOINT | 交易中的儲存點 |
| BEGIN TRANSACTION | BEGIN TRANSACTION | BEGIN TRANSACTION | BEGIN TRANSACTION | 開始交易 |
| Deadlock | 死鎖 | 死锁 | デッドロック | 交易互相等待 |
| Lock | 鎖定 | 锁 | ロック | 防止同時存取 |
| Pessimistic Locking | 悲觀鎖定 | 悲观锁 | 悲観的ロック | 讀取時即鎖定 |
| Optimistic Locking | 樂觀鎖定 | 乐观锁 | 楽観的ロック | 更新時才檢查衝突 |
| Isolation Level | 隔離層級 | 隔离级别 | 分離レベル | 控制交易隔離程度 |
| Read Uncommitted | 讀取未提交 | 读未提交 | Read Uncommitted | 最低隔離層級 |
| Read Committed | 讀取已提交 | 读已提交 | Read Committed | 防止髒讀 |
| Repeatable Read | 可重複讀取 | 可重复读 | Repeatable Read | 防止不可重複讀 |
| Serializable | 可序列化 | 可串行化 | Serializable | 最高隔離層級 |

---

## Database Design

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Normalization | 正規化 | 规范化 | 正規化 | 消除資料冗餘 |
| Denormalization | 反正規化 | 反规范化 | 非正規化 | 提升效能犧牲正規化 |
| First Normal Form (1NF) | 第一正規化 | 第一范式 | 第一正規形 | 原子值 |
| Second Normal Form (2NF) | 第二正規化 | 第二范式 | 第二正規形 | 完全依賴主鍵 |
| Third Normal Form (3NF) | 第三正規化 | 第三范式 | 第三正規形 | 消除遞移依賴 |
| Entity-Relationship Diagram (ERD) | 實體關聯圖 | 实体关系图 | ER図 | 資料庫設計圖 |
| One-to-One | 一對一 | 一对一 | 1対1 | 關聯關係 |
| One-to-Many | 一對多 | 一对多 | 1対多 | 關聯關係 |
| Many-to-Many | 多對多 | 多对多 | 多対多 | 關聯關係 |
| Junction Table | 中介表 | 中间表 | 中間テーブル | 處理多對多關聯 |
| Cardinality | 基數 | 基数 | カーディナリティ | 關聯的數量關係 |
| Data Type | 資料型別 | 数据类型 | データ型 | VARCHAR, INT, DATE 等 |

---

## NoSQL Concepts

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| NoSQL | NoSQL | NoSQL | NoSQL | Not Only SQL |
| Document Database | 文件資料庫 | 文档数据库 | ドキュメントデータベース | MongoDB, Firestore |
| Key-Value Store | 鍵值儲存 | 键值存储 | キーバリューストア | Redis, DynamoDB |
| Column-Family Store | 列族儲存 | 列族存储 | カラムファミリーストア | Cassandra, HBase |
| Graph Database | 圖形資料庫 | 图数据库 | グラフデータベース | Neo4j |
| Collection | 集合 | 集合 | コレクション | MongoDB 的資料表 |
| Document | 文件 | 文档 | ドキュメント | MongoDB 的記錄 |
| Embedded Document | 嵌入式文件 | 嵌入式文档 | 埋め込みドキュメント | 巢狀資料 |
| Reference | 參照 | 引用 | 参照 | 關聯其他文件 |
| Shard | 分片 | 分片 | シャード | 水平分割 |
| Replica Set | 副本集 | 副本集 | レプリカセット | 資料備份 |
| CAP Theorem | CAP 定理 | CAP定理 | CAP定理 | Consistency, Availability, Partition Tolerance |
| Eventual Consistency | 最終一致性 | 最终一致性 | 結果整合性 | NoSQL 常見特性 |
| BASE | BASE | BASE | BASE | Basically Available, Soft state, Eventual consistency |

---

## ORM & Query Builders

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| ORM | ORM | ORM | ORM | Object-Relational Mapping |
| Query Builder | 查詢建構器 | 查询构建器 | クエリビルダー | 程式化建構 SQL |
| Model | 模型 | 模型 | モデル | 對應資料表的類別 |
| Migration | 遷移 | 迁移 | マイグレーション | 資料庫結構變更腳本 |
| Seed | 種子資料 | 种子数据 | シードデータ | 初始化測試資料 |
| Active Record | Active Record | Active Record | Active Record | ORM 模式 |
| Data Mapper | Data Mapper | Data Mapper | Data Mapper | ORM 模式 |
| Repository | 儲存庫 | 仓储 | リポジトリ | 封裝資料存取 |
| Unit of Work | 工作單元 | 工作单元 | Unit of Work | 追蹤物件變更 |
| Lazy Loading | 延遲載入 | 延迟加载 | 遅延ロード | 關聯資料按需載入 |
| Eager Loading | 預先載入 | 预加载 | 先行ロード | 一次載入關聯資料 |
| Hydration | 注水 | 注水 | ハイドレーション | 將資料轉為物件 |
| Raw Query | 原生查詢 | 原生查询 | ローSQLクエリ | 直接執行 SQL |

---

## Connection Management

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Connection | 連線 | 连接 | コネクション | 應用程式與資料庫的連結 |
| Connection String | 連線字串 | 连接字符串 | 接続文字列 | 資料庫連線配置 |
| Connection Pool | 連線池 | 连接池 | コネクションプール | 重複使用連線 |
| Pooling | 連線池化 | 连接池化 | プーリング | 管理多個連線 |
| Max Connections | 最大連線數 | 最大连接数 | 最大接続数 | 同時連線上限 |
| Idle Connection | 閒置連線 | 空闲连接 | アイドル接続 | 未使用的連線 |
| Connection Timeout | 連線逾時 | 连接超时 | 接続タイムアウト | 連線失敗的時限 |
| Keep-Alive | 保持連線 | 保持连接 | Keep-Alive | 維持連線活躍 |

---

## Backup & Recovery

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Backup | 備份 | 备份 | バックアップ | 資料複製保存 |
| Restore | 還原 | 恢复 | リストア | 恢復備份資料 |
| Full Backup | 完整備份 | 完整备份 | フルバックアップ | 全部資料 |
| Incremental Backup | 增量備份 | 增量备份 | 増分バックアップ | 僅備份變更 |
| Differential Backup | 差異備份 | 差异备份 | 差分バックアップ | 備份自上次完整備份後的變更 |
| Point-in-Time Recovery | 時間點還原 | 时间点恢复 | ポイントインタイムリカバリ | 恢復到特定時間 |
| Replication | 複製 | 复制 | レプリケーション | 資料同步到其他伺服器 |
| Master | 主節點 | 主节点 | マスター | 主要資料來源 |
| Slave / Replica | 從節點 | 从节点 | スレーブ / レプリカ | 備份節點 |
| Failover | 故障轉移 | 故障转移 | フェイルオーバー | 自動切換到備援 |
| High Availability | 高可用性 | 高可用性 | 高可用性 | 系統持續運作能力 |

---

## Notes

### Context-Specific Translations

**「資料庫」vs「數據庫」(Database)**:
- 🇹🇼 TW: 使用「資料庫」（data）
- 🇨🇳 CN: 使用「数据库」（數據）
- 一致性：整份文件保持統一

**「欄位」vs「列」vs「字段」(Column/Field)**:
- 🇹🇼 TW: 「欄位」通用
- 🇨🇳 CN: 「列」(Column) vs「字段」(Field)
- Context: Column = 資料表結構，Field = ORM 物件屬性

**「列」vs「行」(Row)**:
- 🇹🇼 TW: 使用「列」（橫向）
- 🇨🇳 CN: 使用「行」（橫向）
- 🇯🇵 JP: 使用「行」（ぎょう）
- 注意：中文的「列」、「行」容易混淆

**「架構」vs「模式」(Schema)**:
- 🇹🇼 TW: 「架構」更常用（結構之意）
- 🇨🇳 CN: 「模式」更常用（Pattern 之意）
- Context: 資料表結構定義

**「交易」(Transaction)**:
- 資料庫術語：原子性操作單元
- 不是商業交易或金融交易
- Context: BEGIN TRANSACTION, COMMIT, ROLLBACK

**「鎖定」vs「鎖」(Lock)**:
- 🇹🇼 TW: 使用「鎖定」（動詞）、「鎖」（名詞）
- 🇨🇳 CN: 使用「锁」（通用）
- Context: 悲觀鎖定、樂觀鎖定

### SQL Keyword Conventions

SQL 關鍵字保持大寫英文：

```sql
-- ✅ Good - 大寫關鍵字
SELECT name, age FROM users WHERE age > 18;

-- ❌ Bad - 小寫關鍵字
select name, age from users where age > 18;

-- ❌ Bad - 中文化
選擇 姓名, 年齡 從 使用者 哪裡 年齡 > 18;
```

### Database Naming Conventions

**資料表命名** (依專案慣例)：
```sql
-- Snake case (推薦)
CREATE TABLE user_profiles;

-- Camel case (較少見)
CREATE TABLE userProfiles;
```

**欄位命名** (英文優先)：
```sql
-- ✅ Good - 英文欄位名
CREATE TABLE users (
  id INT PRIMARY KEY,
  email VARCHAR(255),
  created_at TIMESTAMP
);

-- ❌ Bad - 中文欄位名
CREATE TABLE users (
  編號 INT PRIMARY KEY,
  電子郵件 VARCHAR(255),
  建立時間 TIMESTAMP
);
```

### ORM Model Naming

當使用 ORM 時，Model 名稱使用英文：

```typescript
// ✅ Good - 英文 Model
class User extends Model {
  email: string;
  createdAt: Date;
}

// ❌ Bad - 中文 Model
class 使用者 extends Model {
  電子郵件: string;
  建立時間: Date;
}
```

### Index Naming Conventions

索引命名慣例：

```sql
-- Primary Key: pk_{table}
ALTER TABLE users ADD PRIMARY KEY pk_users (id);

-- Foreign Key: fk_{table}_{column}
ALTER TABLE orders ADD FOREIGN KEY fk_orders_user_id (user_id) REFERENCES users(id);

-- Index: idx_{table}_{column}
CREATE INDEX idx_users_email ON users(email);

-- Unique Index: uq_{table}_{column}
CREATE UNIQUE INDEX uq_users_email ON users(email);
```

### Isolation Level Usage

當設定隔離層級時，使用英文關鍵字：

```sql
-- ✅ Good - 英文隔離層級
SET TRANSACTION ISOLATION LEVEL READ COMMITTED;
SET TRANSACTION ISOLATION LEVEL SERIALIZABLE;

-- ❌ Bad - 中文化
設定交易隔離層級為讀取已提交;
```

### Abbreviation Guidelines

資料庫常用縮寫：

- DB = Database（資料庫）
- DBMS = Database Management System（資料庫管理系統）
- RDBMS = Relational DBMS（關聯式資料庫管理系統）
- SQL = Structured Query Language（結構化查詢語言）
- DDL = Data Definition Language（資料定義語言）
- DML = Data Manipulation Language（資料操縱語言）
- DCL = Data Control Language（資料控制語言）
- TCL = Transaction Control Language（交易控制語言）
- ERD = Entity-Relationship Diagram（實體關聯圖）
- CRUD = Create, Read, Update, Delete
- ACID = Atomicity, Consistency, Isolation, Durability
- CAP = Consistency, Availability, Partition Tolerance
- ORM = Object-Relational Mapping（物件關聯對映）
