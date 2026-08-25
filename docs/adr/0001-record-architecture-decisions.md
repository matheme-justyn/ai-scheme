# 1. Record architecture decisions

Date: 2026-02-25

## Status

Accepted

## Context

在軟體開發過程中，我們會做出許多重要的架構決策。這些決策會影響專案的長期發展方向、技術選型、系統設計等關鍵面向。然而，隨著時間推移和團隊成員的變動，這些決策的背景脈絡、考量因素和權衡取捨往往會逐漸模糊或遺失。

當新成員加入團隊，或是需要重新審視某個設計決策時，我們常常面臨以下問題：

1. **決策脈絡消失**：不清楚當初為什麼做出某個決定
2. **重複討論**：相同的問題被反覆討論，浪費時間
3. **知識流失**：資深成員離開後，重要的決策背景也隨之消失
4. **缺乏追溯性**：難以理解系統演進的歷史軌跡
5. **決策品質下降**：因為缺乏歷史脈絡，新的決策可能與先前的設計衝突

我們需要一個輕量級且結構化的方式來記錄這些重要的架構決策。

## Decision

我們將採用 **Architecture Decision Records (ADR)** 來記錄所有重要的架構決策。

### 什麼是 ADR？

ADR 是一種輕量級的文件格式，用於記錄架構決策。每個 ADR 包含：

- **標題**：簡短描述決策內容，並賦予唯一編號
- **日期**：決策的制定日期
- **狀態**：決策的當前狀態（Proposed, Accepted, Deprecated, Superseded）
- **背景**（Context）：描述面臨的問題和決策背景
- **決策**（Decision）：描述我們的決定和解決方案
- **後果**（Consequences）：說明決策帶來的影響（正面和負面）

### ADR 的使用規則

1. **所有重要的架構決策都應該被記錄**，包括但不限於：
   - 技術選型（框架、函式庫、工具）
   - 架構模式（MVC, Microservices, Event-driven 等）
   - 資料庫設計決策
   - API 設計原則
   - 部署策略
   - 安全性相關決策

2. **ADR 應該在決策制定時立即撰寫**，不要事後補寫

3. **ADR 一旦 Accepted 就不應修改**（除了修正錯字）
   - 如果決策需要變更，應該建立新的 ADR 來取代舊的
   - 舊的 ADR 狀態改為 "Superseded by ADR-XXXX"

4. **ADR 檔案命名格式**：`NNNN-title-with-dashes.md`
   - NNNN：四位數編號，從 0001 開始遞增
   - title-with-dashes：用連字號分隔的標題

5. **ADR 存放位置**：`docs/adr/` 目錄

### ADR 範例

# N. 決策標題

Date: YYYY-MM-DD

## Status

Accepted | Proposed | Deprecated | Superseded by ADR-XXXX

## Context

描述問題背景、需求、約束條件等

## Decision

描述我們的決定和解決方案

## Consequences

描述決策的影響（正面和負面）

## Consequences

### 正面影響

- **知識保存**：架構決策的背景和理由被明確記錄，不會因人員流動而流失
- **提升溝通效率**：新成員可以快速了解專案的重要決策脈絡
- **避免重複討論**：已經討論過的議題有明確的結論可以參考
- **提升決策品質**：強迫我們在做決策時深思熟慮，並清楚說明理由
- **追溯性**：可以清楚追蹤系統設計的演進歷史
- **工具整合**：ADR 是純文字檔案，可以輕鬆整合到版本控制、code review 流程中

### 可能的挑戰

- **需要額外時間**：撰寫 ADR 需要花費時間
- **維護成本**：需要確保 ADR 的編號不重複、狀態正確更新
- **團隊紀律**：需要團隊成員養成記錄 ADR 的習慣
- **判斷標準**：需要明確定義什麼樣的決策需要記錄成 ADR

然而，考量到長期的知識管理和團隊協作效益，這些成本是值得的。

## References

- [Architecture Decision Records](https://adr.github.io/)
- [Documenting Architecture Decisions by Michael Nygard](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR GitHub Organization](https://github.com/joelparkerhenderson/architecture-decision-record)
