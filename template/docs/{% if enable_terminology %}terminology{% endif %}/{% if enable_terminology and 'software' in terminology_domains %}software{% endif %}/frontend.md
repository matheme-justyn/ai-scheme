# Software Development - Frontend Terminology

**Applies to:** Frontend and fullstack projects

**Auto-load when:** `config.toml` → `[project].type` contains "frontend" or "fullstack"

**Priority:** Loaded after `common.md`

---

## Core Web Technologies

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| HTML | HTML | HTML | HTML | HyperText Markup Language，超文本標記語言 |
| CSS | CSS | CSS | CSS | Cascading Style Sheets，階層式樣式表 |
| JavaScript | JavaScript | JavaScript | JavaScript | 瀏覽器腳本語言 |
| TypeScript | TypeScript | TypeScript | TypeScript | JavaScript 的超集，靜態型別 |
| DOM | DOM | DOM | DOM | Document Object Model，文件物件模型 |
| Virtual DOM | 虛擬 DOM | 虚拟DOM | 仮想DOM | 記憶體中的 DOM 表示 |
| Shadow DOM | Shadow DOM | Shadow DOM | Shadow DOM | 封裝 DOM 子樹 |
| Web Components | 網頁元件 | Web组件 | Webコンポーネント | 原生自訂元素 |
| Browser API | 瀏覽器 API | 浏览器API | ブラウザAPI | 瀏覽器提供的原生介面 |

---

## UI Frameworks & Libraries

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| React | React | React | React | Facebook 開源 UI 函式庫 |
| Vue | Vue | Vue | Vue | 漸進式框架 |
| Angular | Angular | Angular | Angular | Google 開源框架 |
| Svelte | Svelte | Svelte | Svelte | 編譯時框架 |
| Next.js | Next.js | Next.js | Next.js | React 伺服器端渲染框架 |
| Nuxt.js | Nuxt.js | Nuxt.js | Nuxt.js | Vue 伺服器端渲染框架 |
| Remix | Remix | Remix | Remix | 全端 React 框架 |
| Astro | Astro | Astro | Astro | 靜態網站生成器 |
| SolidJS | SolidJS | SolidJS | SolidJS | 反應式 UI 函式庫 |

---

## React Ecosystem

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Component | 元件 | 组件 | コンポーネント | 可重複使用的 UI 單元 |
| Props | 屬性 | 属性 | プロパティ | 父元件傳給子元件的資料 |
| State | 狀態 | 状态 | ステート | 元件內部資料 |
| Hook | Hook | Hook | フック | React 函數元件的狀態邏輯 |
| useState | useState | useState | useState | 狀態管理 Hook |
| useEffect | useEffect | useEffect | useEffect | 副作用處理 Hook |
| useContext | useContext | useContext | useContext | 存取 Context |
| useRef | useRef | useRef | useRef | 參照 DOM 或儲存可變值 |
| useMemo | useMemo | useMemo | useMemo | 記憶化計算結果 |
| useCallback | useCallback | useCallback | useCallback | 記憶化函數 |
| Custom Hook | 自訂 Hook | 自定义Hook | カスタムフック | 封裝可重複使用的邏輯 |
| Context | Context | Context | コンテキスト | 跨元件共享資料 |
| JSX | JSX | JSX | JSX | JavaScript XML，React 的語法擴充 |
| Fragment | Fragment | Fragment | フラグメント | 不產生額外 DOM 節點的容器 |
| Portal | Portal | Portal | ポータル | 渲染到其他 DOM 節點 |
| Error Boundary | 錯誤邊界 | 错误边界 | エラーバウンダリー | 捕捉子元件錯誤 |
| Higher-Order Component (HOC) | 高階元件 | 高阶组件 | 高階コンポーネント | 元件包裝器 |
| Render Props | 渲染屬性 | 渲染属性 | レンダープロップス | 透過函數共享邏輯 |
| Reconciliation | 協調 | 协调 | 再調整 | React 的 diff 演算法 |
| Fiber | Fiber | Fiber | Fiber | React 的協調引擎 |

---

## State Management

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| State Management | 狀態管理 | 状态管理 | 状態管理 | 管理應用程式資料 |
| Global State | 全域狀態 | 全局状态 | グローバルステート | 跨元件共享的狀態 |
| Local State | 區域狀態 | 局部状态 | ローカルステート | 元件內部狀態 |
| Redux | Redux | Redux | Redux | 可預測的狀態容器 |
| Zustand | Zustand | Zustand | Zustand | 輕量級狀態管理 |
| Jotai | Jotai | Jotai | Jotai | 原子式狀態管理 |
| Recoil | Recoil | Recoil | Recoil | Facebook 原子式狀態管理 |
| MobX | MobX | MobX | MobX | 反應式狀態管理 |
| Pinia | Pinia | Pinia | Pinia | Vue 官方狀態管理 |
| Vuex | Vuex | Vuex | Vuex | Vue 舊版狀態管理 |
| Store | Store | Store | ストア | 狀態儲存庫 |
| Action | Action | Action | アクション | 觸發狀態變更的事件 |
| Reducer | Reducer | Reducer | リデューサー | 純函數，處理狀態變更 |
| Dispatcher | 分派器 | 分发器 | ディスパッチャー | 發送 Action |
| Selector | 選擇器 | 选择器 | セレクター | 從狀態中取值 |
| Middleware | 中介軟體 | 中间件 | ミドルウェア | 攔截 Action 的邏輯 |
| Thunk | Thunk | Thunk | サンク | 延遲執行的函數 |
| Saga | Saga | Saga | サーガ | 副作用管理模式 |

---

## Styling & CSS

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| CSS-in-JS | CSS-in-JS | CSS-in-JS | CSS-in-JS | JavaScript 中撰寫 CSS |
| Styled Components | Styled Components | Styled Components | Styled Components | 基於標籤的 CSS-in-JS |
| Emotion | Emotion | Emotion | Emotion | CSS-in-JS 函式庫 |
| Tailwind CSS | Tailwind CSS | Tailwind CSS | Tailwind CSS | Utility-first CSS 框架 |
| CSS Modules | CSS 模組 | CSS模块 | CSSモジュール | 區域作用域的 CSS |
| SCSS / Sass | SCSS / Sass | SCSS / Sass | SCSS / Sass | CSS 預處理器 |
| PostCSS | PostCSS | PostCSS | PostCSS | CSS 轉換工具 |
| CSS Variable | CSS 變數 | CSS变量 | CSS変数 | 原生自訂屬性 |
| Flexbox | Flexbox | Flexbox | Flexbox | 彈性盒子佈局 |
| Grid | Grid | Grid | Grid | 網格佈局 |
| Responsive Design | 響應式設計 | 响应式设计 | レスポンシブデザイン | 適應不同螢幕尺寸 |
| Mobile-First | 行動優先 | 移动优先 | モバイルファースト | 從小螢幕開始設計 |
| Breakpoint | 斷點 | 断点 | ブレークポイント | 響應式設計的臨界點 |
| Media Query | 媒體查詢 | 媒体查询 | メディアクエリ | 條件式 CSS |
| Dark Mode | 深色模式 | 暗色模式 | ダークモード | 深色主題 |

---

## Routing & Navigation

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Routing | 路由 | 路由 | ルーティング | URL 與元件對應 |
| Client-Side Routing | 客戶端路由 | 客户端路由 | クライアントサイドルーティング | 瀏覽器端路由控制 |
| React Router | React Router | React Router | React Router | React 路由函式庫 |
| Vue Router | Vue Router | Vue Router | Vue Router | Vue 路由函式庫 |
| Dynamic Route | 動態路由 | 动态路由 | 動的ルート | 參數化的路由 |
| Nested Route | 巢狀路由 | 嵌套路由 | ネストされたルート | 多層路由結構 |
| Route Guard | 路由守衛 | 路由守卫 | ルートガード | 路由攔截器 |
| History API | History API | History API | History API | 瀏覽器歷史記錄 API |
| Hash Routing | Hash 路由 | Hash路由 | ハッシュルーティング | 使用 URL fragment |
| Browser Routing | 瀏覽器路由 | 浏览器路由 | ブラウザルーティング | 使用 History API |
| Link | Link | Link | リンク | 導航連結元件 |
| Redirect | 重新導向 | 重定向 | リダイレクト | 強制跳轉 |
| Navigation | 導航 | 导航 | ナビゲーション | 頁面切換 |

---

## Rendering Strategies

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Client-Side Rendering (CSR) | 客戶端渲染 | 客户端渲染 | クライアントサイドレンダリング | 瀏覽器渲染 |
| Server-Side Rendering (SSR) | 伺服器端渲染 | 服务端渲染 | サーバーサイドレンダリング | 伺服器預渲染 HTML |
| Static Site Generation (SSG) | 靜態網站生成 | 静态网站生成 | 静的サイト生成 | 建置時預渲染 |
| Incremental Static Regeneration (ISR) | 增量靜態再生成 | 增量静态再生成 | インクリメンタル静的再生成 | 部分更新靜態頁面 |
| Hydration | 注水 | 注水 | ハイドレーション | SSR 後在客戶端啟用互動 |
| Rehydration | 再注水 | 再注水 | 再ハイドレーション | 重新啟用互動 |
| Partial Hydration | 部分注水 | 部分注水 | 部分ハイドレーション | 僅部分元件啟用互動 |
| Islands Architecture | 群島架構 | 岛屿架构 | アイランドアーキテクチャ | 靜態內容中的互動島嶼 |
| Streaming SSR | 串流 SSR | 流式SSR | ストリーミングSSR | 逐步傳送 HTML |

---

## Performance Optimization

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Code Splitting | 程式碼分割 | 代码分割 | コード分割 | 拆分打包檔案 |
| Lazy Loading | 延遲載入 | 延迟加载 | 遅延ロード | 需要時才載入 |
| Tree Shaking | Tree Shaking | Tree Shaking | Tree Shaking | 移除未使用的程式碼 |
| Bundle Size | 打包大小 | 打包大小 | バンドルサイズ | 最終檔案大小 |
| Minification | 壓縮 | 压缩 | ミニファイ | 移除空白與註解 |
| Compression | 壓縮 | 压缩 | 圧縮 | Gzip / Brotli 壓縮 |
| Image Optimization | 圖片最佳化 | 图片优化 | 画像最適化 | 壓縮、格式轉換 |
| Font Loading | 字型載入 | 字体加载 | フォント読み込み | 最佳化字型載入策略 |
| Critical CSS | 關鍵 CSS | 关键CSS | クリティカルCSS | 首屏必要的 CSS |
| Above the Fold | 首屏內容 | 首屏内容 | ファーストビュー | 不需捲動即可見的內容 |
| Time to First Byte (TTFB) | 首位元組時間 | 首字节时间 | TTFB | 伺服器回應時間 |
| First Contentful Paint (FCP) | 首次內容繪製 | 首次内容绘制 | FCP | 首次渲染內容的時間 |
| Largest Contentful Paint (LCP) | 最大內容繪製 | 最大内容绘制 | LCP | 最大元素渲染時間 |
| Cumulative Layout Shift (CLS) | 累積版面配置位移 | 累积布局偏移 | CLS | 視覺穩定性指標 |
| First Input Delay (FID) | 首次輸入延遲 | 首次输入延迟 | FID | 互動回應時間 |
| Interaction to Next Paint (INP) | 互動到下次繪製 | 交互到下次绘制 | INP | 互動回應性 |
| Prefetching | 預取 | 预取 | プリフェッチ | 預先載入可能需要的資源 |
| Preloading | 預載 | 预加载 | プリロード | 提前載入必要資源 |
| Service Worker | Service Worker | Service Worker | Service Worker | 離線快取、背景同步 |

---

## Forms & Validation

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Form | 表單 | 表单 | フォーム | 使用者輸入介面 |
| Input Field | 輸入欄位 | 输入字段 | 入力フィールド | 單一輸入元件 |
| Textarea | 文字區域 | 文本区域 | テキストエリア | 多行文字輸入 |
| Select | 下拉選單 | 下拉选择 | セレクト | 選擇清單 |
| Checkbox | 核取方塊 | 复选框 | チェックボックス | 多選 |
| Radio Button | 單選按鈕 | 单选按钮 | ラジオボタン | 單選 |
| Form Validation | 表單驗證 | 表单验证 | フォーム検証 | 檢查輸入正確性 |
| Client-Side Validation | 客戶端驗證 | 客户端验证 | クライアント側検証 | 瀏覽器端驗證 |
| Server-Side Validation | 伺服器端驗證 | 服务端验证 | サーバー側検証 | 後端驗證 |
| Form State | 表單狀態 | 表单状态 | フォーム状態 | 追蹤輸入值與錯誤 |
| Controlled Component | 受控元件 | 受控组件 | 制御されたコンポーネント | React 控制的表單元件 |
| Uncontrolled Component | 非受控元件 | 非受控组件 | 非制御コンポーネント | DOM 自行管理的元件 |
| Form Library | 表單函式庫 | 表单库 | フォームライブラリ | React Hook Form, Formik |
| Error Message | 錯誤訊息 | 错误消息 | エラーメッセージ | 驗證失敗的提示 |
| Placeholder | 佔位符 | 占位符 | プレースホルダー | 輸入提示文字 |
| Label | 標籤 | 标签 | ラベル | 欄位說明 |

---

## Animation & Transitions

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Animation | 動畫 | 动画 | アニメーション | 視覺效果變化 |
| Transition | 轉場 | 过渡 | トランジション | 狀態切換動畫 |
| CSS Animation | CSS 動畫 | CSS动画 | CSSアニメーション | 原生 CSS 動畫 |
| JavaScript Animation | JavaScript 動畫 | JavaScript动画 | JavaScriptアニメーション | 程式控制動畫 |
| Keyframe | 關鍵影格 | 关键帧 | キーフレーム | 動畫的關鍵狀態 |
| Easing Function | 緩動函數 | 缓动函数 | イージング関数 | 動畫速度曲線 |
| Framer Motion | Framer Motion | Framer Motion | Framer Motion | React 動畫函式庫 |
| GSAP | GSAP | GSAP | GSAP | 高效能動畫函式庫 |
| React Spring | React Spring | React Spring | React Spring | 基於物理的動畫 |
| Lottie | Lottie | Lottie | Lottie | After Effects 動畫播放 |
| SVG Animation | SVG 動畫 | SVG动画 | SVGアニメーション | 向量圖形動畫 |
| Parallax | 視差 | 视差 | パララックス | 不同速度的滾動效果 |

---

## Accessibility (A11y)

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Accessibility | 無障礙性 | 无障碍 | アクセシビリティ | 殘障人士可用性 |
| WCAG | WCAG | WCAG | WCAG | Web Content Accessibility Guidelines |
| ARIA | ARIA | ARIA | ARIA | Accessible Rich Internet Applications |
| Semantic HTML | 語義化 HTML | 语义化HTML | セマンティックHTML | 使用正確的 HTML 標籤 |
| Alt Text | 替代文字 | 替代文本 | 代替テキスト | 圖片的文字描述 |
| Screen Reader | 螢幕閱讀器 | 屏幕阅读器 | スクリーンリーダー | 視障輔助工具 |
| Keyboard Navigation | 鍵盤導航 | 键盘导航 | キーボードナビゲーション | 僅用鍵盤操作 |
| Focus Management | 焦點管理 | 焦点管理 | フォーカス管理 | 控制鍵盤焦點 |
| Skip Link | 跳過連結 | 跳过链接 | スキップリンク | 快速跳到主內容 |
| Color Contrast | 色彩對比 | 颜色对比 | カラーコントラスト | 文字與背景的對比度 |
| Tab Index | Tab 索引 | Tab索引 | Tab Index | 控制 Tab 鍵順序 |
| Live Region | 即時區域 | 实时区域 | ライブリージョン | 動態內容通知 |

---

## Testing

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Unit Test | 單元測試 | 单元测试 | 単体テスト | 測試單一元件 |
| Integration Test | 整合測試 | 集成测试 | 統合テスト | 測試元件互動 |
| E2E Test | 端對端測試 | 端到端测试 | E2Eテスト | 完整使用者流程 |
| Component Test | 元件測試 | 组件测试 | コンポーネントテスト | 測試 UI 元件 |
| Visual Regression Test | 視覺回歸測試 | 视觉回归测试 | ビジュアルリグレッションテスト | 檢查 UI 變化 |
| Snapshot Test | 快照測試 | 快照测试 | スナップショットテスト | 比對元件輸出 |
| Jest | Jest | Jest | Jest | JavaScript 測試框架 |
| Vitest | Vitest | Vitest | Vitest | Vite 原生測試框架 |
| React Testing Library | React Testing Library | React Testing Library | React Testing Library | React 元件測試 |
| Cypress | Cypress | Cypress | Cypress | E2E 測試框架 |
| Playwright | Playwright | Playwright | Playwright | 跨瀏覽器測試 |
| Storybook | Storybook | Storybook | Storybook | UI 元件開發環境 |
| Test Coverage | 測試覆蓋率 | 测试覆盖率 | テストカバレッジ | 測試涵蓋的程式碼比例 |

---

## Build Tools & Module Bundlers

| English | 繁體中文 (TW) | 簡體中文 (CN) | 日本語 (JP) | Notes |
|---------|--------------|--------------|------------|-------|
| Webpack | Webpack | Webpack | Webpack | 模組打包工具 |
| Vite | Vite | Vite | Vite | 快速建置工具 |
| Rollup | Rollup | Rollup | Rollup | ES Module 打包工具 |
| Parcel | Parcel | Parcel | Parcel | 零配置打包工具 |
| esbuild | esbuild | esbuild | esbuild | 極快的打包工具 |
| Babel | Babel | Babel | Babel | JavaScript 編譯器 |
| TypeScript Compiler | TypeScript 編譯器 | TypeScript编译器 | TypeScriptコンパイラ | tsc |
| Hot Module Replacement (HMR) | 模組熱替換 | 模块热替换 | HMR | 開發時即時更新 |
| Development Server | 開發伺服器 | 开发服务器 | 開発サーバー | 本地開發環境 |
| Production Build | 生產建置 | 生产构建 | プロダクションビルド | 最佳化後的打包 |

---

## Notes

### Context-Specific Translations

**「元件」vs「組件」(Component)**:
- 🇹🇼 TW: 使用「元件」（通用）
- 🇨🇳 CN: 使用「组件」（通用）
- 軟體工程通用術語，不同於硬體元件 (Hardware Component)

**「屬性」(Props)**:
- 完整名稱：Properties
- React 特有術語，不翻譯為「道具」（日文 Props）
- 與 HTML 屬性 (Attribute) 不同

**「狀態」(State)**:
- 指應用程式資料，非狀態碼 (Status Code)
- Context: State Management = 狀態管理

**「注水」(Hydration)**:
- 較新的術語，翻譯尚未統一
- 🇹🇼/🇨🇳: 使用「注水」（形象化）
- 🇯🇵: 使用「ハイドレーション」（外來語）

**「打包」vs「建置」**:
- Build = 建置（整個流程）
- Bundle = 打包（檔案合併）
- Bundler = 打包工具

### Abbreviation Guidelines

- CSR = 客戶端渲染 (Client-Side Rendering)
- SSR = 伺服器端渲染 (Server-Side Rendering)
- SSG = 靜態網站生成 (Static Site Generation)
- ISR = 增量靜態再生成 (Incremental Static Regeneration)
- HMR = 模組熱替換 (Hot Module Replacement)
- A11y = Accessibility (11 個字母簡寫)
- I18n = Internationalization (18 個字母簡寫)

### Framework-Specific Terms

當使用特定框架時，保持該框架的術語風格：

**React**:
- Component (元件), Props (屬性), State (狀態), Hook

**Vue**:
- Component (元件), Props (屬性), Reactive (響應式), Composition API

**Angular**:
- Component (元件), Service (服務), Directive (指令), Dependency Injection (依賴注入)

### Usage in Code

**變數命名** (英文優先):
```javascript
// ✅ Good - 使用英文
const userProfile = { ... }
const handleSubmit = () => { ... }

// ❌ Bad - 中文命名
const 使用者資料 = { ... }
const 處理提交 = () => { ... }
```

**註解** (使用在地化語言):
```javascript
// ✅ Good - 繁體中文註解
// 處理使用者登入，驗證後回傳 JWT token
function handleLogin() { ... }

// ✅ Good - 英文註解 (多國團隊)
// Handle user login, return JWT token after validation
function handleLogin() { ... }
```

**錯誤訊息** (使用在地化語言):
```javascript
// ✅ Good - 使用者看得懂的語言
throw new Error('無法載入使用者資料')
alert('表單驗證失敗，請檢查必填欄位')

// ❌ Bad - 英文錯誤訊息 (非英語使用者)
throw new Error('Failed to load user data')
```
