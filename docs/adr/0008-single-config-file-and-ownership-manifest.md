# ADR 0008: Single config file and ownership manifest

**Status**: Accepted
**Date**: 2026-09-08
**Issue**: [#2](https://github.com/matheme-justyn/ai-scheme/issues/2), [#3](https://github.com/matheme-justyn/ai-scheme/issues/3)
**PR**: [#28](https://github.com/matheme-justyn/ai-scheme/pull/28)
**Tags**: config, copier, ownership, update
**Supersedes**: [ADR 0005](./0005-template-directory-isolation.md)  
**Cross-repo**: 對應的決策記錄由 `ai-zpd` 側自行保存（`ai-zpd` ADR 0015，撰寫完成待 commit）。本 ADR 只約束本層行為，不代表另一側。

## Context

現況有兩個問題。第一，`config.toml.example` 是從上游一刀切下來的段落（i18n、academic、github、terminology），沒有任何地方記錄「這個 repo 由哪個 template 版本產生、選了哪些語言與功能」。第二，「哪些檔案屬於 template、哪些屬於專案」只靠 `.scaffolding/` 這個目錄名隔離（ADR 0005），更新時只能整包覆蓋或整包不動。

先前的 POC 用單一 answers 檔當唯一設定來源是對的，但它把 ownership 規則散落在 `copier.yml` 的 `_exclude`／`_skip_if_exists` Jinja 條件裡，人讀不出來，`adopt` 報告與 uninstall 文件只能各自手抄一份清單。POC 也因為不想裝 PyYAML 而手寫了 YAML 子集解析器，導致設定只能是平面鍵。

另一個限制來自 `ai-zpd`：它已經有一個根目錄 `config.toml`（TOML，160 行，section 為 `[project]`／`[opencode]`／`[services]`／`[modules]`）。

## Decision

- Copier 為模板引擎。**單一 answers 檔 `.scheme/config.yml`（YAML，Copier 原生）是骨架層設定的唯一來源**，附 JSON Schema 驗證。
- CLI 提供 `config get <key>` 與 `config validate`，shell 腳本不自行解析 YAML。CLI 以 uv 管理依賴，直接用 PyYAML，不重蹈手寫解析器。
- **Ownership 是資料不是 Jinja**：以一份可讀的 manifest 宣告哪些路徑由 template 擁有，`uninstall`、`adopt` 報告、`update` 衝突判斷共用同一份清單。這取代 ADR 0005 的目錄名隔離。
- **與 `ai-zpd` 的設定檔採兩檔兩格式，邊界寫明**：`ai-zpd` 保留根目錄 `config.toml`（機制層），本層用 `.scheme/config.yml`（骨架層）。兩者**不互相讀寫**，同名鍵各自獨立、不做 fallback。`status` 與 `adopt` 偵測到根目錄有 `config.toml` 時只回報「偵測到機制層設定檔」，不讀內容、不因此改變狀態判斷。
- 骨架層擁有的鍵：`languages`、`branch_strategy`、`readme_primary_language`、`release_phase`、`collaboration_mode`、`project_visibility`、`enable_*`、以及專案識別（名稱、slug、描述）。
- 機制層（`ai-zpd` 的 `config.toml`）擁有的鍵，列此僅為邊界對照，本層不得讀取：`[project].type`、`[project].features`、`[project].quality`（決定載入哪些模組）、`[opencode]` 整棵、`[services]` 整棵、`[modules]` 整棵。
- **命名約束**：兩層都不得使用會被誤認為對方的鍵名。具體地，本層**不使用 `project_type`** 這個字面——語言與技術棧一律以 `languages` 表達。理由：`ai-zpd` 的 `[project].type` 指的是「載入哪些領域模組」（fullstack／backend／cli／academic…），與本層的語言 profile 語意不同；在「不互讀、同名鍵各自獨立」的前提下，名字相近而行為不同是最糟的組合。
- **template 版本**：概念上歸骨架層，唯一來源是 `.scheme/config.yml` 與 `ai-scheme status --json` 的 `current_version`／`target_version`。`ai-zpd` 既有的 `.scaffolding/VERSION` 與使用者專案根目錄的 `.template-version` 為**過渡期相容路徑**，本層僅在 `migrate` 狀態下唯讀，不寫入、不作為判斷依據（見 [#4](https://github.com/matheme-justyn/ai-scheme/issues/4)）。

## Alternatives considered

| 方案 | 否決理由 |
| --- | --- |
| 統一成 YAML，兩層各自一個檔 | 技術上較乾淨，但要求 `ai-zpd` 改寫 160 行範本與所有讀取點，換來的只是格式一致；兩檔的邊界問題並沒有因此消失。 |
| 統一成 TOML | Copier 的 answers 檔原生是 YAML，改用 TOML 等於自己維護一層轉換。 |
| 合併成單一設定檔，用 section 標明擁有層 | 使用者只看到一個檔案是優點，但兩個 repo 的 update 流程都要寫進同一個檔，`update` 的衝突處理會明顯變複雜。 |
| 維持 ADR 0005 的目錄名隔離 | 目錄名無法表達「這個檔案由 template 產生但允許使用者改」這類狀態，也無法讓 `update` 做逐檔判斷。 |
| ownership 繼續寫在 `copier.yml` 的 Jinja 條件 | 人讀不出來，且無法被 `uninstall`／`adopt` 報告重用，POC 已證明會導致多份手抄清單。 |

## Reconsider when

- 使用者實際回報「兩個設定檔」造成誤改或困惑，且文件說明無法解決。
- `ai-zpd` 的 config 重新設計（`ai-zpd` ADR 0014 的 consequences 已註明需要）走到定案，屆時可重新評估統一格式的成本。
- ownership manifest 的規則複雜到需要條件邏輯（表示它正在變回 Jinja，該重新設計）。

## Consequences

- 正面：`update` 能逐檔判斷，不再是整包覆蓋或整包不動。
- 正面：`uninstall`、`adopt` 報告、衝突判斷共用同一份清單，不會再各自手抄。
- 負面：使用者的專案裡會同時出現 `.scheme/config.yml` 與 `config.toml` 兩個設定檔、兩種格式。這是明知的代價，靠檔頭註解與文件說明處理。
- 負面：`.template-version` 這個約定散落在 `ai-zpd` 的 **15 個檔案**——雙語 README、`AGENTS.md`、`.gitignore`、`.opencode/INSTALL.md`、`.scaffolding/` 下兩份 README、PRD、`test-init-project.sh`，再加六支腳本（`init-project.sh`、`smart-install.sh`、`sync-template.sh`、`analyze-conflicts.sh`、`generate-readme.sh`、`migrate-to-template-dir.sh`）。這是一次遷移，不是順手改幾行，過渡期不會短。
- 負面：ADR 0005 的目錄隔離仍存在於既有的生成 repo，需要 `migrate` 路徑處理（見 [#4](https://github.com/matheme-justyn/ai-scheme/issues/4)、[#5](https://github.com/matheme-justyn/ai-scheme/issues/5)）。
