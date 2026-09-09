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

## 職業對應:字模雕刻師 Punchcutter

這個專案家族裡每個名字都是「心理學家的術語」配上「體現這個術語的消失職業」,這一個是**字模雕刻師**。

活字印刷要能鑄出一顆活字之前,得先有人把每個字母手工雕進一小塊鋼胚裡——這叫「衝壓」(punch)。這個衝壓再打進較軟的金屬做出「字模」(matrix),字模才是真正用來鑄造出無數個一模一樣活字的工具。刻一個衝壓,熟練的工匠常常要花上一整天,普遍被認為是整條活字生產鏈裡最困難的工作。這門技藝現在幾乎絕跡,全世界只剩少數幾位還在做。

它是一個母版打出另一個母版,那個母版才鑄出無窮多的忠實副本——是模板的模板,不是單一物件被重複生產。這種分層結構比「一位工匠、重複產出相同物件」的職業更貼近 `ai-scheme` 實際在做的事:repo 模板本身不是生成出來的那些 repo,它是打出字模、讓那些 repo 得以存在的那個衝壓。

## 怎麼用

每一個生命週期指令預設都是 dry run:先產出 plan,只有 `--apply-plan` 會動到你的專案。

```bash
# 這個專案現在是什麼狀態?下一步該跑什麼?
uvx --from git+https://github.com/matheme-justyn/ai-scheme@v0.1.0 ai-scheme status --json

# 把既有專案納入骨架
uvx --from git+https://github.com/matheme-justyn/ai-scheme@v0.1.0 ai-scheme adopt --tag v0.1.0
```

一律釘 tag。tag 會被解析成它所指的完整 commit 並寫進 `.scheme/provenance.json`,
之後更新時才能說出到底變了什麼,而不是相信一個隨時可以被移動的名字。
`--allow-unreleased` 是給開發模板本身用的,會把那次執行標記為 `development`。

第一個 release 還沒發布,所以上面的指令指向一個還不存在的 tag;在那之前請從 checkout 執行。

## 現況

骨架、生命週期指令(`status`、`create`、`adopt`、`update`)、驗證入口,
以及 Issue、PR、milestone 三份契約都已就位。release 自動化、
repository settings as code、語言 profile 與決策簡報站尚未完成——見 open issues。

## 授權

MIT 授權——參閱 [LICENSE](./LICENSE)
