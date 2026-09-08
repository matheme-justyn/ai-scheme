# ADR 0009: Release phase drives governance, not approval ceremony

**Status**: Accepted
**Date**: 2026-09-08
**Issue**: [#2](https://github.com/matheme-justyn/ai-scheme/issues/2), [#13](https://github.com/matheme-justyn/ai-scheme/issues/13), [#21](https://github.com/matheme-justyn/ai-scheme/issues/21)
**PR**: [#28](https://github.com/matheme-justyn/ai-scheme/pull/28)
**Tags**: governance, ruleset, release-phase

## Context

先前的 POC 為多人組織設計，治理規則預設「提案者以外的人來核准」。單人維護的公開 repo 套用同一套規則會產生死結：GitHub 不允許核准自己的 PR，開了 required review 就等於自己擋住自己。POC 為此累積了一批單人例外補丁，散落在各個腳本裡，每一支都要自己判斷「現在是不是單人情境」。

同時，早期專案就套上完整治理是另一種浪費：`alpha` 階段還在改介面，required status checks 不可繞過只會逼人繞路。

限制：GitHub 對公開 repo 提供完整 Ruleset 能力；免費方案的私有 repo 不提供，能力不足時必須誠實回報。

## Decision

- **治理強度由 `release_phase` 宣告，不由核准儀式決定**。`release_phase` 取值 `alpha`／`beta`／`release`，寫在 answers 檔，**只能單向前進**。
- 各階段對應的 Ruleset 內容由 `scripts/apply-repository-settings` 依宣告值組出，行為矩陣的唯一來源是 [`docs/collaboration-modes.md`](../collaboration-modes.md)。概要：`alpha` 允許 repository admin 的 `pull_request` bypass；`beta` 起 required status checks 不可繞過；`release` 的 `bypass_actors` 必為空。
- **不做「非提案者核准」作為預設**。是否需要第二人由 `collaboration_mode` 決定（見 [ADR 0010](./0010-collaboration-mode-declaration.md)），與本 ADR 的階段軸正交。
- 腳本不得自行推斷情境。任何需要分流的地方一律讀宣告值。
- 能力不足（例如免費方案私有 repo 無法套用 Ruleset）標記為 `DEGRADED`，不當作通過。

## Alternatives considered

| 方案 | 否決理由 |
| --- | --- |
| 沿用 POC 的多人治理，單人情境逐處加例外 | 已證明會散成一堆補丁，每支腳本各自判斷，行為不一致且無法測試。 |
| 完全不做治理，單人 repo 靠自律 | 專案進入 `release` 後沒有任何機制擋住誤推；且本 template 的產出物要給別人用，治理能力本身是交付內容。 |
| 用 repo 的 collaborator 人數自動推斷治理強度 | 人數會變動，行為會在使用者沒改任何設定的情況下改變；且 API 查詢在離線時無解。 |
| 讓 `release_phase` 可以雙向調整 | 從 `release` 退回 `alpha` 等於把已放寬的 bypass 重新打開，且沒有留痕，是治理漏洞。 |

## Reconsider when

- 出現需要在 `release` 階段臨時放寬的真實情境，且 [#21](https://github.com/matheme-justyn/ai-scheme/issues/21) 的 bypass 留痕不足以涵蓋。
- GitHub 改變免費方案的 Ruleset 能力，使 `DEGRADED` 這個狀態不再需要。

## Consequences

- 正面：治理強度是一個可讀的宣告值，`plan` 可以印出「目前是 `solo × beta`、據此組出這些 Ruleset」。
- 正面：單人例外從散落的腳本邏輯收斂成兩個宣告值。
- 負面：`release_phase` 單向前進意味著誤設會需要人工介入改 answers 檔並留下紀錄。
- 負面：階段與模式兩軸交叉出六種組合，每一種都要有 fixture 測試（見 [#12](https://github.com/matheme-justyn/ai-scheme/issues/12)）。
