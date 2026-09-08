# Architecture Decision Records

本目錄記錄 `ai-scheme` 的架構決策。ADR 的目的與使用時機見 [ADR 0001](./0001-record-architecture-decisions.md)；本頁只規定格式、狀態詞彙與編號政策。

## 必填欄位

0007 起的每份 ADR 至少要有下列欄位。缺任何一項，`scripts/verify` 的 docs tier 會失敗（[#10](https://github.com/matheme-justyn/ai-scheme/issues/10) 落地前先以 grep 檢查）。

| 欄位 | 說明 |
| --- | --- |
| **Status** | 見下方狀態詞彙。被取代時要指名取代者。 |
| **Date** | 決策日期，`YYYY-MM-DD`。 |
| **Issue / PR** | 至少一張 Issue 與一張 PR 的連結。沒有 PR 的決策不算落地。 |
| **Context** | 面臨的問題與限制。限制要寫實際存在的那些（配額、方案、人數、既有檔案），不寫假設。 |
| **Decision** | 決定本身。用可驗證的敘述，不用「盡量」「考慮」。 |
| **Alternatives considered** | 真的評估過的替代方案，各附一句否決理由。沒評估過的不要列。 |
| **Reconsider when** | 什麼條件成立時應重新評估這個決策。寫不出來，通常表示這不是一個決策。 |
| **Consequences** | 正面與負面後果，含已知會被犧牲的東西。 |

## 狀態詞彙

| 狀態 | 意義 |
| --- | --- |
| `Proposed` | 已寫下但尚未定案，不得被其他文件當成既定事實引用。 |
| `Accepted` | 現行有效。 |
| `Superseded by ADR <n>` | 已被後續決策取代。**原文保留不刪**，並在檔頭說明被取代的是哪一部分——通常是實作手段，而問題判斷仍然有效。 |
| `Rejected` | 評估後決定不做。保留的價值在於避免下一次重新討論同一件事。 |
| `Deprecated` | 不再適用，但沒有明確的取代者（例如它針對的東西已經不存在）。 |

`Superseded` 與 `Rejected` 的原文一律保留。這是從先前的 POC 帶過來的做法：只留結論不留理由，下一個 session 會把同樣的選項再評估一次。

## 編號政策

- 檔名格式 `NNNN-kebab-case-title.md`，四位數字，連續遞增。
- 標題第一行為 `# ADR NNNN: <English Title>`。內文以 zh-TW 撰寫，技術名詞保留英文。
- **跨 repo 引用一律寫成 `<repo> ADR <n>`**，例如 `ai-zpd ADR 0014`。三個 repo 的編號各自獨立，同一個號碼在不同 repo 是不同文件，不帶 repo 名的引用一律視為錯誤。
- 不要為了填補空號而重編。編號是識別碼，不是順序保證。

### 2026-09-08 的重新編號

`ai-scheme` 的 ADR 是從 `my-vibe-scaffolding` 依三 repo 拆分而來，拆完後本 repo 的編號有洞（缺 0005、0007），而且 0008 與 `ai-zpd` 的 0008 是兩份不同文件。依 [#2](https://github.com/matheme-justyn/ai-scheme/issues/2) 的決定重新編號為連續序列，對照表如下。

| 舊編號（`my-vibe-scaffolding`） | 新編號（`ai-scheme`） | 標題 |
| --- | --- | --- |
| 0001 | 0001 | Record architecture decisions |
| 0002 | 0002 | Example tech stack selection |
| 0003 | 0003 | Example API design principles |
| 0004 | 0004 | Example testing strategy |
| 0006 | **0005** | Template file isolation strategy |
| 0008 | **0006** | No markdown code fence in markdown files |

未進入本 repo 的舊編號，去向如下，引用時請改用帶 repo 名的形式：

| 舊編號 | 去向 |
| --- | --- |
| 0005 single-instance-opencode-workflow | `ai-zpd` |
| 0007 agent-skills-ecosystem-integration | 未歸屬，性質屬 `ai-skill-web` |
| 0008 opencode-config-claude-code-reference | `ai-zpd` |
| 0009 reference-claude-code-architecture | `ai-zpd` |
| 0010 everything-claude-code-integration | `ai-zpd` |
| 0011 scaffolding-directory-and-skill-priority | 未歸屬 |
| 0012 config-driven-modular-documentation-system | `ai-zpd` |
| 0012 module-system-and-conditional-loading | 未歸屬（上游即與前者同號） |
| 0013 skills-architecture | 未歸屬 |
| 0014 repo-split-ai-scheme-ai-zpd-ai-skill-web | `ai-zpd` |

## 目錄

| ADR | 狀態 | 主題 |
| --- | --- | --- |
| [0001](./0001-record-architecture-decisions.md) | Accepted | 採用 ADR 記錄架構決策 |
| [0002](./0002-example-tech-stack-selection.md) | Accepted | 範例：技術選型 |
| [0003](./0003-example-api-design-principles.md) | Accepted | 範例：API 設計原則 |
| [0004](./0004-example-testing-strategy.md) | Accepted | 範例：測試策略 |
| [0005](./0005-template-directory-isolation.md) | Superseded by 0008 | 以目錄名隔離 template 檔案 |
| [0006](./0006-no-markdown-code-fence-in-markdown-files.md) | Accepted | markdown 檔內不使用 markdown code fence |
| [0007](./0007-three-repo-boundary.md) | Accepted | 三 repo 的職責邊界 |
| [0008](./0008-single-config-file-and-ownership-manifest.md) | Accepted | 單一設定檔與 ownership manifest |
| [0009](./0009-release-phase-governance.md) | Accepted | 以 release_phase 取代單人核准儀式 |
| [0010](./0010-collaboration-mode-declaration.md) | Accepted | 以 collaboration_mode 宣告單人或多人 |
| [0011](./0011-verification-location-and-attestation.md) | Accepted | 驗證位置與本機證明的信任邊界 |
| [0012](./0012-implementation-language.md) | Accepted | 實作語言採 Python 與 uv |
| [0013](./0013-publishing-target.md) | Accepted | 發布目標只做 GitHub Pages |
| [0014](./0014-root-self-governance.md) | Accepted | 根目錄自我治理，不維護兩份同步檔案 |

0002 至 0004 是從上游帶過來的**範例** ADR，不是本 repo 的真實決策，保留作為格式示範。它們的內容不得被當成本 repo 的既定事實引用。
