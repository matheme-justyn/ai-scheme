# ADR 0007: Three-repo boundary

**Status**: Accepted
**Date**: 2026-09-08
**Issue**: [#1](https://github.com/matheme-justyn/ai-scheme/issues/1), [#2](https://github.com/matheme-justyn/ai-scheme/issues/2)
**PR**: [#28](https://github.com/matheme-justyn/ai-scheme/pull/28)
**Tags**: architecture, repo-split, boundary

## Context

`my-vibe-scaffolding` 同時扛了三件事：repo 骨架與 CI 慣例、安裝與執行機制、agent 角色與技能。三者的變更頻率與使用者都不同，混在一個 repo 導致每次改動都要判斷「這會不會影響另外兩件事」。拆分決定記錄在 `ai-zpd` ADR 0014，本 ADR 只記錄拆分後**本 repo 這一側的邊界**，以及跨層呼叫的介面方向。

限制：三個 repo 都是公開 repo、同一個維護者、彼此沒有 CI 相依。拆分後仍有約 20 份文件未明確歸屬，暫留 `ai-zpd`。

## Decision

- `ai-scheme`（骨架層）提供：Copier 模板、生命週期 CLI（`create`／`adopt`／`update`／`status`）、驗證入口、policies-as-code、release 流程、文件與 ADR 慣例。
- `ai-zpd`（機制層）提供：安裝與執行機制、統一 prompt。
- `ai-skill-web`（能力層）提供：agent 角色、技能、SDD 內容，以路徑契約掛入生成的 repo。
- **依賴方向單向**：`ai-zpd` 呼叫 `ai-scheme` 的 CLI；`ai-scheme` 不知道 `ai-zpd` 的存在，不讀它的檔案、不依賴它的安裝結果。
- **唯一介面是 `ai-scheme status --json`**。`ai-zpd` 的統一 prompt 讀 `state` 與 `next_command` 行動，不自行推斷 repo 狀態、不自行比對版本（見 [#4](https://github.com/matheme-justyn/ai-scheme/issues/4)）。介面契約寫在 `docs/status-interface-contract.md`。**命名約束**：本層的契約文件名不使用 `install` 字樣——`ai-zpd` 已有 `.opencode/INSTALL.md`，講的是「能力如何被裝進使用者專案」，與本文件的「agent 如何呼叫骨架層的生命週期介面」不是同一件事，同名會重演 `project_type` 那類撞名。本文件明寫一句不涵蓋 `ai-zpd` 的 install/update 機制。
- 跨 repo 引用 ADR 一律寫成 `<repo> ADR <n>`。

## Alternatives considered

| 方案 | 否決理由 |
| --- | --- |
| 不拆，維持單一 repo | 已經證明失敗：每次改動都要跨領域判斷影響範圍，這正是拆分的起因。 |
| 拆成兩個（骨架＋其他） | agent 能力內容的變更頻率遠高於安裝機制，綁在一起等於讓機制層跟著高頻變動。 |
| 骨架層反向讀取 `ai-zpd` 的設定以自動調整行為 | 造成雙向依賴，`ai-scheme` 將無法獨立測試；且骨架層要為機制層的格式變動負責。 |

## Reconsider when

- `ai-zpd` 或 `ai-skill-web` 出現需要 `ai-scheme` 主動讀取的狀態（屆時應先考慮把該狀態納入 `status` 的輸出，而不是開反向依賴）。
- 三個 repo 的維護者不再是同一人，跨 repo 的協調成本實際超過拆分收益。

## Consequences

- 正面：本 repo 可以獨立測試與發版，不需要 `ai-zpd` 在場。
- 正面：介面收斂成單一指令，`ai-zpd` 端的改寫範圍可預期。
- 負面：跨 repo 的收尾工作需要人工協調，例如 `hooks/pre-push` 搬到本 repo 後，驅動它的三支腳本留在 `ai-zpd` 形成斷裂（見 [#14](https://github.com/matheme-justyn/ai-scheme/issues/14)）。
- 負面：約 20 份未歸屬文件暫留 `ai-zpd`，需要另一輪盤點。
