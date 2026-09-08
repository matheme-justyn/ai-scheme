# ADR 0012: Implement the lifecycle CLI in Python with uv

**Status**: Accepted
**Date**: 2026-09-08
**Issue**: [#1](https://github.com/matheme-justyn/ai-scheme/issues/1), [#2](https://github.com/matheme-justyn/ai-scheme/issues/2)
**PR**: PR_PLACEHOLDER
**Tags**: language, tooling, copier, uv

## Context

整個 milestone 的實作語言要先定，否則每張 Issue 都會各自假設。實際被評估的問題是：改用 Rust 會不會更快？

限制：`update` 這條路徑的核心是 Copier 的三方合併——用舊版 template 重新渲染一次，再與新版做 git 三方合併。這是「可更新骨架」之所以成立的機制，不是可以繞過的細節。

## Decision

本 milestone 全部以 **Python 3.12+ ＋ uv** 實作，工具鏈為 ruff、ty、pytest。

## Alternatives considered

| 方案 | 否決理由 |
| --- | --- |
| Rust | 執行速度無感：所有工作都是 I/O（呼叫 `gh`、渲染模板、跑 shellcheck／gitleaks／pytest 子程序），沒有 CPU 熱點；唯一差別是啟動時間（`uvx` 冷啟動秒級、暖啟動不到一秒，Rust binary 毫秒級）。開發速度明顯較慢：Rust 生態沒有 Copier `update` 的對應物——`cargo-generate` 只有 create 沒有 update，minijinja 只解 Jinja 語法不解三方合併，自己重做等於再寫一個 Copier。Rust 唯一的實質優勢是單一靜態 binary、使用者不需要 uv；本生態已全面站在 uv 上，此優勢為零。 |
| Go | 同樣沒有 Copier update 的對應物，且模板渲染要自己接 Jinja 相容層。 |
| 純 shell | 現況已證明失敗：判斷邏輯埋在 shell 裡無法測試，YAML／JSON 解析需要外部工具或手寫解析器。 |

## Reconsider when

- 量測到 `status` 的冷啟動實際拖慢 prompt。屆時的做法是用 Rust 寫一支**只讀 answers 檔的 `status` 小 binary**，其餘不動——不是整包改寫。
- 目的是 dogfood 本 template 的 rust profile。那是另一個目標，不是效能問題，應另開 Issue 討論。

## Consequences

- 正面：Copier 的 `update` 直接可用，`update` 路徑不需要自己實作三方合併。
- 正面：測試用 pytest 跑子程序 fixture，與生成專案的驗證方式一致。
- 負面：使用者需要 uv。這是本生態的既有前提，不是新增成本。
- 負面：`status` 的啟動時間受 Python 冷啟動影響，若 prompt 高頻呼叫可能感覺得到（見上方重新評估條件）。
