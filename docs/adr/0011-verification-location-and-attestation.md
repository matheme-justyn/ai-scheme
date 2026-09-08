# ADR 0011: Verification location and the trust boundary of local attestation

**Status**: Accepted
**Date**: 2026-09-08
**Issue**: [#2](https://github.com/matheme-justyn/ai-scheme/issues/2), [#11](https://github.com/matheme-justyn/ai-scheme/issues/11), [#27](https://github.com/matheme-justyn/ai-scheme/issues/27)
**PR**: [#28](https://github.com/matheme-justyn/ai-scheme/pull/28)
**Tags**: ci, verification, attestation, trust-boundary

## Context

`scripts/verify` 是本機與 CI 的共同入口（[#11](https://github.com/matheme-justyn/ai-scheme/issues/11)）。本機跑過一次、樹沒變的情況下，hosted CI 再跑一次同一組 stage 是重工：等待時間長，而且本機與 CI 的結果之間沒有任何可稽核的連結。

先前的 POC 做過這件事，但動機是私有方案的 Actions 配額耗盡。本 repo 與生成的 repo 都是公開 repo，Actions 免費，**那個動機在這裡不成立**。原本因此把 trailer 列為 Out of scope；2026-09-08 由 repo owner 決定納入，理由改為回饋時間，並要求補上 POC 沒有的信任邊界。

限制：trailer 是未簽章的宣告，任何能寫 commit 的人都能偽造。squash-merge 會產生新的 tree，被驗過的 tree hash 對不上。

## Decision

- CI 與本機跑同一支 `scripts/verify`，分級與 stage 拆分見 [#11](https://github.com/matheme-justyn/ai-scheme/issues/11)。
- 本機驗證通過後寫入 trailer `Verified-locally: sha256=<tree> tier=<t> at=<ts>`，`<tree>` 取 `git rev-parse HEAD^{tree}`。
- **不靜默改寫歷史**：只在明確指定 `--attest`、且 HEAD 尚未被 push 時 amend；否則印出 trailer 讓使用者自行處理並以非零退出。
- **信任邊界**：
  - 只在 `collaboration_mode=solo` 時可據此跳過重跑。`team` 模式下 trailer **只記錄不跳過**——PR 作者以外的人無法驗證它。
  - 只作用於 PR head 的 CI run。squash-merge 後合併 commit 的 tree 與被驗過的 tree 不同，`main` 上一律全跑，`check-attestation` 在 `main` 回報 not-applicable，不算失敗。
  - 比對 tree hash、比對 tier 是否 ≥ 本次變更所需級別、比對時窗。任一不符即**退回全跑**。
- 失敗方向固定為 fail open 到「重跑」，不是 fail open 到「跳過」。

## Alternatives considered

| 方案 | 否決理由 |
| --- | --- |
| 不做 trailer，CI 一律重跑（2026-09-08 前的決定） | 公開 repo 沒有配額壓力，但回饋時間仍是實際成本；owner 判定值得換。 |
| 做 trailer 但不分 `solo`／`team` | `team` 模式下等於讓 PR 作者自己宣告「我驗過了」而審查者無從查證，是治理漏洞。 |
| 用簽章（GPG／sigstore）讓 trailer 可驗證 | 可解決偽造問題，但要求每個使用者設定簽章金鑰，對單人公開 repo 的成本遠高於收益。若之後真的需要跨人信任，這是第一順位方案。 |
| 改用 CI 快取而非跳過 stage | 快取只省下載與建置，不省實際執行；且快取失效判斷本身就是一個要維護的東西。 |
| 在 `main` 上也讀 trailer | squash-merge 後 tree hash 必然對不上，讀了只會製造假失敗。 |

## Reconsider when

- 專案轉為 `team` 且確實需要跨人信任本機驗證結果——屆時改用簽章方案，而不是放寬現在的邊界。
- Actions 的等待時間不再是瓶頸（例如 stage 全部縮短到分鐘以內），trailer 的複雜度就不值得。
- GitHub 提供原生的「這棵 tree 已通過某某檢查」機制。

## Consequences

- 正面：PR 上的回饋時間縮短，且「這棵樹在本機被驗過哪一級」成為可查的事實。
- 正面：失敗方向固定為重跑，最壞情況只是沒省到時間。
- 負面：多一支 `check-attestation` 與三個 fixture 要維護。
- 負面：`solo` 與 `team` 的 CI 行為不同，除錯時要先確認模式。
