# ADR 0015: "Cannot answer" is not "nothing to report"

**Status**: Accepted
**Date**: 2026-09-09
**Issue**: [#55](https://github.com/matheme-justyn/ai-scheme/issues/55)
**PR**: [#56](https://github.com/matheme-justyn/ai-scheme/pull/56)
**Tags**: contracts, exit-codes, status, lease, settings

## Context

本層的每個查詢介面都會遇到同一種情況：**它無法回答**。模板抓不到所以算不出 drift；GitHub 連不上所以讀不到 repository settings；沒有任何 release 所以沒得比較版本。

這種情況與「查過了，沒有問題」在結構上很像——兩者都沒有東西可報——所以在型別層次上很容易被合併成同一個值：空陣列、`false`、exit `0`。合併之後，呼叫端無法區分「驗過沒事」與「沒人驗過」。

這個形狀在 2026-09-08 到 09 之間出現了三次，其中兩次是 `ai-zpd` 側在消費本層介面時指出的：

1. **版本同步檢查**：檢查確實執行（covered），但它所在的 workflow 常態紅燈，所以真的漂移時 job 狀態從紅變紅，產生不出可觀察的訊號（not signalled）。「已確認 CI 覆蓋」被讀成「已確認 CI 會擋」。
2. **`status` 的消費端**：`drift` 與 `policy_drift` 的 `"unknown"` 若被當成 `[]`，呼叫端就會宣稱一件沒人驗過的事。
3. **lease 協定的合併條件**：空的 review decision、完全沒有 checks 回報、`mergeStateStatus UNKNOWN`——都不是「通過」。

三次都是同一句話的不同形狀。

## Decision

**「答不出來」必須有自己的值，而且永遠不得降級成「沒事」。**

具體到本層既有的介面：

- `status --json` 的 `drift` 與 `policy_drift` 在檢查跑不起來時是字串 `"unknown"`，不是 `[]`（見 [ADR 0014](./0014-root-self-governance.md) 之後的 `status` 實作與 `docs/status-interface-contract.md`）。
- `update --check` 對沒有記錄 release 來源的專案回 `update_available: null`，不是 `true`——否則每個開發中的 checkout 每週都會被通知它過期了。
- `settings check` 的每個領域帶 `capability`（`allowed`／`blocked`／`unknown`）與 `verdict`（`matches`／`drifted`／`degraded`）。`degraded` 既不算通過也不算失敗。對 GitHub 根本沒在強制的事情回報「已強制」，比完全沒檢查更糟。
- lease 載體的 exit code：`1` 是明確的否定（別人持有、capability 不符、head 前進），`2` 是答不出來（git 失敗、ref 內容讀不懂）。`1` 值得等一下重試，`2` 不值得。
- `verify` 的任何 stage：工具抓不到就讓該 stage 失敗，不跳過。跑不起來的檢查不是通過的檢查。

契約文件必須明寫這件事，因為型別本身無法表達「這個值不可以被正規化掉」。

## Alternatives considered

| 方案 | 否決理由 |
| --- | --- |
| `unknown` 正規化成空集合，讓型別乾淨 | 這正是要防的那一步。它把「沒人驗過」變成型別上的「驗過了，沒問題」，而且看起來像是無害的簡化。 |
| 無法回答時直接失敗（非零 exit） | 對 `status` 不成立：它必須離線可用，且「無法判斷 drift」不該擋住呼叫端得知其他狀態。改以欄位表達，exit code 只區分「答出來了」與「答不出來」。 |
| 額外欄位 `drift_checked: bool` | 兩個欄位可以各自為政，第三個 session 只讀其中一個。單一欄位帶三種值，讀的人無法只讀一半。 |
| 只寫在各自的契約文件裡 | 已經是現況，而且不夠：規則寫在三份程式碼與三份文件裡，理由沒有寫在任何地方，下一個人看不到它是一個決定。 |

## Reconsider when

- 出現一個呼叫端**必須**把三態壓成二態的場景，且壓縮的方向有安全預設（例如「未知一律視為有漂移」）。屆時那個壓縮應該發生在呼叫端，並在它自己的文件裡寫明方向，而不是由本層先壓好。
- 某個介面的 `unknown` 在實務上從未出現過，表示那個檢查其實不會失敗——那時要確認的是「真的不會失敗」，而不是「失敗時我們沒看到」。

## Consequences

- 正面：呼叫端在型別層次上無法把「不知道」誤讀成「沒事」。`ai-zpd` 的三個消費點沿用同一組語意（它們的 ADR 0016、0020、0021 各記一次，依 ADR 0007 的規則，那是另一側的記錄）。
- 正面：新增介面時有一個現成的答案可以照抄，不必每次重新爭論。
- 負面：每個呼叫端都要處理三種值，比兩種麻煩。這是刻意付的代價。
- 負面：`"unknown"` 是字串而其他值是陣列，型別不整齊。整齊會讓它消失。
