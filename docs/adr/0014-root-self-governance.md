# ADR 0014: The template repo governs itself from rendered output

**Status**: Accepted
**Date**: 2026-09-08
**Issue**: [#2](https://github.com/matheme-justyn/ai-scheme/issues/2), [#12](https://github.com/matheme-justyn/ai-scheme/issues/12)
**PR**: PR_PLACEHOLDER
**Tags**: self-governance, template, testing

## Context

本 repo 自己也是一個用同一套規則管理的 repo：它有 CI、有 PR 契約、有 release 流程。問題是這些檔案同時扮演兩個角色——「本 repo 實際使用的設定」與「要交付給生成 repo 的模板」。

先前的 POC 維護了 root 與 template 兩份幾乎相同的檔案，靠腳本或人工同步。實務上兩份必定漂移，而且漂移通常是在「只改了其中一份」的 PR 裡悄悄發生，沒有任何檢查會抓到。

## Decision

- 本 template repo 自己也套用同一套規則，但**不維護 root 與 template 兩份手動同步的檔案**。
- 根目錄實際使用的檔案由 template 渲染產生，模板是唯一來源。
- 驗證方式是**生成 fixture**：對每一條生命週期路徑渲染出真實的專案，對它跑 `scripts/verify`（見 [#12](https://github.com/matheme-justyn/ai-scheme/issues/12)）。不做 paired-file sync 檢查。
- 例外必須明確列出並說明理由（例如本 repo 專屬、不應出現在生成專案的檔案）。

## Alternatives considered

| 方案 | 否決理由 |
| --- | --- |
| root 與 template 兩份，用腳本同步 | POC 已證明會漂移，且漂移發生在單邊修改時，沒有檢查抓得到。 |
| root 與 template 兩份，用 CI 比對是否一致 | 比對規則本身要維護；且「應該一致」與「刻意不同」的界線需要另一份清單，等於把問題往後推一層。 |
| 本 repo 不套用自己的規則 | template 的規則沒有被實際使用過就交付出去，等於沒測過。 |

## Reconsider when

- 出現大量「本 repo 需要但生成專案不需要」的檔案，使渲染產生的根目錄檔案反而變成例外清單的主體。
- Copier 的渲染能力不足以表達本 repo 自身的需求。

## Consequences

- 正面：模板是唯一來源，不可能出現「改了模板忘了改 root」。
- 正面：fixture 測的是真實渲染結果，比比對檔案內容更接近使用者實際拿到的東西。
- 負面：改本 repo 根目錄的檔案要透過模板，回饋迴圈比直接改檔案長。
- 負面：例外清單需要人工維護與 review。
