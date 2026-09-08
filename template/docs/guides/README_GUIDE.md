# README 撰寫指南

> 本文件提供使用此模板建立新專案時的 README 撰寫建議

---

## 快速開始

使用此模板建立新專案後，請：

1. **記錄模板版本**
   ```bash
   echo "1.2.0" > .template-version
   git add .template-version
   ```

2. **替換 README.md**
   - 刪除或大幅改寫當前的 README.md
   - 參考下方的「專案 README 模板」

3. **更新必要資訊**
   - 專案名稱、描述
   - 技術棧
   - 安裝和使用說明

---

## 專案 README 模板

以下是建議的結構（根據專案需求調整）：

# 專案名稱

> 簡短描述（1-2 句話說明專案目的）

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](./VERSION)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

---

## 功能特色

- 特色 1
- 特色 2
- 特色 3

## 技術棧

- **語言**: TypeScript / Python / Go / Rust
- **框架**: （如 React, FastAPI, Gin）
- **資料庫**: （如 PostgreSQL, MongoDB）
- **其他**: （工具、服務）

## 快速開始

### 環境需求

- Node.js 18+ / Python 3.11+ / Go 1.21+
- （其他依賴）

### 安裝

\`\`\`bash
# Clone repository
git clone https://github.com/your-org/your-project.git
cd your-project

# 安裝依賴
npm install  # 或 pip install -r requirements.txt
\`\`\`

### 設定

\`\`\`bash
# 複製環境變數範例
cp .env.example .env

# 編輯 .env 填入必要資訊
vim .env
\`\`\`

### 執行

\`\`\`bash
# 開發模式
npm run dev  # 或 python main.py

# 執行測試
npm test
\`\`\`

## 專案結構

\`\`\`
project/
├── src/           # 原始碼
├── tests/         # 測試
├── docs/          # 文件
├── config/        # 配置
└── scripts/       # 腳本
\`\`\`

## API 文件

（如果有 API）

- **Base URL**: `http://localhost:3000/api`
- **完整文件**: [API.md](./docs/API.md) 或 Swagger UI

## 開發指南

### 編碼規範

參考 [AGENTS.md](./AGENTS.md) 中的規範。

### 提交 Commit

\`\`\`bash
# 格式
type: brief description

# 範例
feat: add user authentication
fix: resolve database connection error
\`\`\`

### 執行測試

\`\`\`bash
npm test              # 所有測試
npm test -- --watch   # 監視模式
\`\`\`

## 部署

\`\`\`bash
# 建置
npm run build

# 部署到 production
（部署指令）
\`\`\`

## 貢獻

參考 [CONTRIBUTING.md](./CONTRIBUTING.md)

## 授權

MIT License - 詳見 [LICENSE](./LICENSE)

## 致謝

- 基於 [my-vibe-scaffolding](https://github.com/matheme-justyn/my-vibe-scaffolding) 模板建立

---

**模板版本**: 1.2.0 (記錄在 `.template-version`)

---

## 關鍵差異：框架 README vs 專案 README

| 內容 | 框架 README (此檔案) | 專案 README (你的專案) |
|------|---------------------|----------------------|
| **目的** | 介紹框架理念、結構 | 介紹專案功能、使用方式 |
| **受眾** | 想使用此模板的人 | 想使用你專案的人 |
| **內容** | 模板特色、i18n、ADR | 功能、API、部署 |
| **技術棧** | 通用說明 | 具體技術 |
| **快速開始** | 如何用模板建專案 | 如何跑起來你的專案 |

---

## 建議的專案初始化腳本

可以建立 `scripts/init-project.sh` 自動化：

```bash
#!/bin/bash
# 初始化新專案

read -p "專案名稱: " PROJECT_NAME
read -p "專案描述: " PROJECT_DESC

# 記錄模板版本
TEMPLATE_VERSION=$(cat VERSION)
echo "$TEMPLATE_VERSION" > .template-version

# 建立基礎 README
cat > README.md << EOF
# $PROJECT_NAME

> $PROJECT_DESC

（參考 docs/README_GUIDE.md 完成此文件）

---

**基於**: [my-vibe-scaffolding](https://github.com/matheme-justyn/my-vibe-scaffolding) v$TEMPLATE_VERSION
EOF

echo "✅ 已初始化專案"
echo "   .template-version: $TEMPLATE_VERSION"
echo "   README.md: 基礎版本已建立"
echo ""
echo "下一步："
echo "  1. 編輯 README.md（參考 docs/README_GUIDE.md）"
echo "  2. 更新 AGENTS.md 中的專案特定規範"
echo "  3. 刪除不需要的範例檔案"
```

---

## 版本追蹤

### .template-version 檔案

建立專案時，記錄使用的模板版本：

```bash
# 手動建立
echo "1.2.0" > .template-version

# 或使用初始化腳本
./scripts/init-project.sh
```

### 同步模板更新

當模板有新版本時，參考 [TEMPLATE_SYNC.md](../TEMPLATE_SYNC.md)。

---

## 常見問題

### Q: 要保留模板的 README 嗎？
**A**: 不用。可以移到 `docs/TEMPLATE_README.md` 作為參考，或直接刪除。

### Q: AGENTS.md 要改嗎？
**A**: 要。更新專案特定的編碼規範、commit 格式、技術棧。

### Q: 哪些檔案應該保留？
**A**: 
- ✅ 保留：AGENTS.md, CHANGELOG.md, CONTRIBUTING.md, LICENSE
- ✅ 修改：README.md（改成你的專案說明）
- ⚠️ 可選：docs/adr/（刪除範例 ADR，建立自己的）

### Q: 如何知道模板有更新？
**A**: 
```bash
# 查看你的模板版本
cat .template-version

# 查看最新版本
curl -s https://api.github.com/repos/matheme-justyn/my-vibe-scaffolding/releases/latest | grep tag_name
```

---

**更新**: 2026-02-26
