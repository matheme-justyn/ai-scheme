# ADR 0013: Publish the decision site to GitHub Pages only

**Status**: Accepted
**Date**: 2026-09-08
**Issue**: [#2](https://github.com/matheme-justyn/ai-scheme/issues/2), [#23](https://github.com/matheme-justyn/ai-scheme/issues/23), [#26](https://github.com/matheme-justyn/ai-scheme/issues/26)
**PR**: [#28](https://github.com/matheme-justyn/ai-scheme/pull/28)
**Tags**: publishing, github-pages, scope

## Context

[#23](https://github.com/matheme-justyn/ai-scheme/issues/23) 產出一份可攜的雙語決策站（單檔 `docs/index.html`）。接著的問題是發布到哪裡，以及私有內容怎麼辦。

調查過的限制（實測文件確認）：

- GitHub 私有 Pages 只有 Enterprise Cloud 有，且只開給對該 repo 有 read 權限的人；個人帳號完全沒有這個功能。把 Cloudflare 擋在 GitHub Pages 前面沒用，`*.github.io` 原站仍公開。
- Cloudflare Pages 的「Enable access policy」開關**預設只保護 preview deployments**，不保護正式站與 custom domain；要另外處理才涵蓋，這是最容易裸奔的地方。
- Cloudflare Access 的 Google IdP 拿不到 Workspace group，權限只能用 email 清單或 domain；每個登入過的 identity 佔一個 seat（免費 50 席）。

## Decision

- 本 template **只發布 GitHub Pages**，且安裝時可關閉（`enable_pages`）。預設值由 `project_visibility` 決定。
- **登入牆、Cloudflare Pages／Access、任何第三方託管都不在本 template 範圍**。
- 成品契約：`docs/index.html` 永遠存在於 `main`。需要私有站的人由**外部 repo 自行取用這個單檔成品**，本 template 不介入其存取控制。
- 私有 repo 情境下 Pages 方案不支援時，標記為 `DEGRADED` 並說明，不靜默跳過。
- 發布走 GitHub Actions，policy 檔的 `plan`／`apply`／`check` 流程沿用 [#13](https://github.com/matheme-justyn/ai-scheme/issues/13)。

## Alternatives considered

| 方案 | 否決理由 |
| --- | --- |
| Cloudflare Pages ＋ Cloudflare Access（Google 或 OTP 登入） | 技術上可行且免費額度夠，但把一整套 Zero Trust 設定面、seat 管理與「正式站是否真的被保護」的自動檢查帶進本 template；owner 決定這屬於另一個 repo 的職責。 |
| GitHub 私有 Pages | 個人帳號沒有這個功能，Enterprise Cloud 才有。 |
| 不發布，只留 markdown | 決策站的價值就在於可分享的單一頁面；不發布等於沒做。 |
| 發布但不提供關閉選項 | 有些生成的 repo 不需要站，強制發布會產生沒人看的 Pages 與多餘的 workflow。 |

## Reconsider when

- 使用者實際需要在本 template 內建的私有發布，且「外部 repo 取用單檔成品」被證明太麻煩。
- GitHub 對個人帳號開放私有 Pages。

## Consequences

- 正面：發布路徑單一，workflow 與 policy 檔都小。
- 正面：單檔成品契約讓外部 repo 可以自由選擇託管與存取控制。
- 負面：需要登入牆的人要自己維護另一個 repo。
- 負面：私有 repo 的使用者會看到 `DEGRADED`，需要文件說明這不是錯誤。
