# ADR 0010: Declare collaboration mode instead of inferring head count

**Status**: Accepted
**Date**: 2026-09-08
**Issue**: [#2](https://github.com/matheme-justyn/ai-scheme/issues/2), [#24](https://github.com/matheme-justyn/ai-scheme/issues/24)
**PR**: [#28](https://github.com/matheme-justyn/ai-scheme/pull/28)
**Tags**: governance, collaboration-mode, ruleset

## Context

[ADR 0009](./0009-release-phase-governance.md) 把治理強度交給 `release_phase`，但還有一件事它決定不了：這個 repo 有沒有第二個真人可以審查與核可。required review、milestone 核可、reviewer 指派、`CODEOWNERS` 這幾件事只有在有第二人時才有意義；沒有第二人時開啟它們會造成死結。

先前的 POC 把這件事藏在各腳本的條件判斷裡，導致同一個問題在不同腳本有不同答案。

## Decision

- 新增宣告值 `collaboration_mode`，取值 `solo`／`team`，由 repo owner 寫在 answers 檔。
- **與 `release_phase` 正交**：`release` 階段的單人專案仍是 `solo`；`alpha` 階段的多人專案仍是 `team`。兩軸互不推導。
- 完整行為矩陣（機制 × `solo`／`team` × 實作 Issue）的**唯一來源**是 [`docs/collaboration-modes.md`](../collaboration-modes.md)。腳本以 `ai-scheme config get collaboration_mode` 讀值後分流，**不得自行推斷 repo 有幾個人**。
- 一致性檢查只提示不強制：`team` 但 write 以上 collaborator 少於兩人時標 `DEGRADED` 並說明會死結，**不自動改回 `solo`**；`solo` 但偵測到第二人時只印建議，不失敗。
- 例外：PR remote lease（[#19](https://github.com/matheme-justyn/ai-scheme/issues/19)）兩種模式都開。它解決的是多個 agent session 同時寫同一張 PR 控制面，與人數無關。

## Alternatives considered

| 方案 | 否決理由 |
| --- | --- |
| 由 collaborator 人數自動推斷 | 人數變動會讓行為在使用者沒改設定時改變；離線無法查詢；且「有帳號」不等於「會來審查」。 |
| 併入 `release_phase`，用階段隱含人數 | 兩者實際正交，硬併會產生「`release` 就必須有第二人」這種不成立的規則。 |
| 只做 `solo`，多人情境不支援 | 本 template 的產出物要給別人用，多人是必要情境。 |
| 偵測到不一致時自動改回 `solo` | 靜默改變使用者的宣告值，比死結更難查。 |

## Reconsider when

- 出現第三種明顯不同的協作型態（例如「多人但不做 code review」），兩值不足以表達。
- GitHub 提供可靠且離線可得的「這個 repo 實際有幾個活躍審查者」訊號。

## Consequences

- 正面：所有治理分流讀同一個值，行為一致且可測試。
- 正面：切換模式只需改 answers 檔加跑 `apply-repository-settings plan`，不需要重跑 `adopt`／`update`。
- 負面：宣告值可能與現實不符，只能靠一致性檢查提示。
- 負面：六種 `collaboration_mode × release_phase` 組合各需 fixture。
