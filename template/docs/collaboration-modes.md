# Collaboration modes（單人／多人模式）

- **狀態**：Draft，隨 [#24](https://github.com/matheme-justyn/ai-scheme/issues/24) 實作時更新
- **來源 Issue**：#24；相關實作 #8、#13、#19、#20、#21
- **定位**：本頁是 `collaboration_mode` 行為矩陣的**唯一來源**。各腳本以 `ai-scheme config get collaboration_mode` 讀值後依本頁分流；不得在腳本內自行推斷 repo 有幾個人。

## 兩個正交的軸

| 軸 | 鍵 | 值 | 意義 | 誰決定 |
| --- | --- | --- | --- | --- |
| 人數 | `collaboration_mode` | `solo`／`team` | repo 是否有第二位真人可以審查、核可 | repo owner 宣告，寫在 answers 檔 |
| 成熟度 | `release_phase` | `alpha`／`beta`／`release` | 專案發布階段，只能單向前進 | 維護者以 PR 修改 |

兩軸互不推導：`release` 階段的單人專案仍是 `solo`；`alpha` 階段的多人專案仍是 `team`。

## 行為矩陣

| 機制 | `solo` | `team` | 實作 |
| --- | --- | --- | --- |
| required review（Ruleset `pull_request` 規則） | 不開；GitHub 不允許核准自己的 PR，開了就是死結 | `required_approving_review_count: 1`、`require_last_push_approval`、`require_code_owner_review`（依 `release_phase` 漸進，見下表） | #13、#21 |
| required status checks | 開 | 開 | #13、#21 |
| Ruleset `bypass_actors` | 依 `release_phase` 允許 repository admin 的 `pull_request` bypass；`release` 時必為空 | 一律為空 | #21 |
| bypass 留痕（`bypass-trace:` 留言、`check-bypass-trace`） | 每次使用 bypass 必留痕 | 不適用（沒有 bypass 可用） | #21 |
| milestone 開工核可 | 只有提案者自己 `/milestone admin-approve: <理由>`；理由必填，紀錄標示 **Admin self-approved** | 必須由非提案者 `/milestone approve`；`admin-approve` 一律拒絕 | #20 |
| scope 變更核可（`Tracker scope: expanded`） | 同上 | 同上 | #20 |
| `/milestone object:`／`resolve:` 反駁流程 | 可用（自己對自己留紀錄） | 可用，且必須全部 resolve 才能開工 | #20 |
| reviewer 輪派、`.github/REVIEWERS` | 不產生 | 產生；PR 轉 ready 時指派一位非作者 reviewer | #8 |
| `CODEOWNERS` | 不產生 | 產生；Ruleset 要求 code owner review | #13 |
| PR policy（ready 時） | `Closes #N`、雙向 checklist、label／milestone 一致、分支名 | 同左，另要求存在非作者 review request | #8 |
| PR remote lease（`pr_lifecycle.py`、`scan_writers`） | 開 | 開 | #19 |
| `scripts/verify`、CI tier | 相同 | 相同 | #11 |
| release、Dependabot、供應鏈掃描 | 相同 | 相同 | #14、#15 |

Lease 兩種模式都開：它解決的是**多個 agent session** 同時寫同一張 PR 控制面，與人數無關。

## `collaboration_mode` × `release_phase` 的 Ruleset 內容

| | `alpha` | `beta` | `release` |
| --- | --- | --- | --- |
| **`solo`** | 一條 Ruleset：`non_fast_forward` ＋ `required_status_checks`；`bypass_actors` 含 admin `pull_request` bypass（required checks 可被一併繞過，每次留痕） | 兩條 Ruleset：protected branches（`non_fast_forward`，admin bypass）＋ required checks（`bypass_actors: []`）；required checks 不可繞過 | 兩條 Ruleset，`bypass_actors` 皆為空；`check-bypass-lifecycle` 在任何非空時讓 `verify` 失敗 |
| **`team`** | 兩條 Ruleset；`pull_request` 規則：1 位核准；`bypass_actors: []` | 同左，加 `require_last_push_approval`、`require_code_owner_review` | 同左，加 `required_review_thread_resolution`、`dismiss_stale_reviews_on_push` |

`scripts/apply-repository-settings plan` 必須印出目前的組合（例如 `solo × beta`）與據此組出的 Ruleset。

## 一致性檢查

| 情況 | 行為 |
| --- | --- |
| `team` 但 repo 的 write 以上 collaborator 少於 2 人 | `apply-repository-settings check` 標 `DEGRADED`，說明 required review 會變成死結；不自動改回 `solo` |
| `solo` 但偵測到第二位 write 以上 collaborator | 只印提示建議改 `team`，不失敗 |
| 私有 repo 在免費方案無法套用 Ruleset | 既有 `DEGRADED required governance` 語意，與模式無關 |
| `team` 模式收到 `/milestone admin-approve:` | 拒絕，並在 summary 標明原因 |

## 切換模式

1. 修改 answers 檔的 `collaboration_mode`（或 `ai-scheme config set collaboration_mode=team`）。
2. `ai-scheme status --json` 回報 `policy-only-update`。
3. `scripts/apply-repository-settings plan` 檢視差異，人工執行 `apply`（依 GitHub 跨專案協作規則，改 settings 與 branch protection 屬高風險，agent 只跑 `plan`／`check`）。
4. 不需要重跑 `adopt`／`update`；`update` 時模式值保持不變。

## 測試矩陣

- `apply-repository-settings plan` 對六種組合各一組 fixture，輸出與本頁 Ruleset 表逐格比對。
- #20 的核可解析、#8 的 PR validator、#21 的 bypass 檢查各對兩種模式跑一次。
- 一致性檢查四種情況各一測試。

## 決策紀錄

本頁的取捨（以宣告值取代散落的單人例外、兩軸正交、lease 不依模式）在 #2 的 ADR 記錄；本頁只描述行為，不重述理由。
