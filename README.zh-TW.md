<div align="center">

# ai-scheme

[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

[English](./README.md) | 繁體中文

</div>

---

## 這是什麼？

**repo/CI 骨架層**——同一套治理結構,套用到多個生成出來的專案上,靠 [Copier](https://copier.readthedocs.io/) 讓它們隨時間持續保持同步。

這個 repo 是從 [my-vibe-scaffolding](https://github.com/matheme-justyn/my-vibe-scaffolding) 拆分出來的,那個 repo 本身則會改名為 [`ai-zpd`](https://github.com/matheme-justyn/ai-zpd)（能力機制層)。`ai-scheme` 接手原本裡面跟專案骨架、CI/CD 慣例、Copier 模板傳遞有關的部分。

## 為什麼叫 Scheme

命名自 Jean Piaget 的 **schème**——不是比較常見的英譯「schema」。

Piaget 在法文裡區分兩個字,英文翻譯把它們混在一起了：*schéma*(比較靜態、圖像式的表徵)跟 **schème**(動作導向的認知結構——「一套可套用到大量情境的技能骨架」,一種會在類似情境中重複、轉化、類推的行動模式)。這個 repo 取的是後者:模板是可重複使用的程序骨架,不是一張靜態的圖。

英文拼法拿掉了重音符號,純粹是實務考量——帶重音的 "schème" 不適合當 repo 名稱的 ASCII 字元。這代表這個名字唸起來會跟 *Scheme* 程式語言(一種 Lisp 方言)撞名,這個碰撞風險經過考慮後被接受,判斷為低風險。

## 現況

這個 repo 剛建立。內容正在從 `my-vibe-scaffolding`／`ai-zpd` 分階段搬遷過來——這段期間可以先看那個 repo 的 `.scaffolding/` 目錄了解哪些東西會搬過來。

## 授權

MIT 授權——參閱 [LICENSE](./LICENSE)
