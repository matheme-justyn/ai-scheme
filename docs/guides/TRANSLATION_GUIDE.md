# TRANSLATION GUIDE

**Status**: Active | **Domain**: Academic  
**Related Modules**: I18N_GUIDE, ACADEMIC_WRITING, DOCUMENT_STRUCTURE

## Purpose

This module defines standards and best practices for translation work, including translation workflows, quality assurance, terminology management, and handling cultural adaptation. It covers both technical translation (documentation, UI) and academic/professional translation.

## When to Use This Module

- Translating documentation or user interfaces
- Managing translation projects
- Establishing translation workflows
- Creating translation memory databases
- Ensuring translation quality and consistency
- Handling cultural localization

---

## 1. Translation Principles

### 1.1 Accuracy vs. Fluency

**Accuracy**: Preserve original meaning exactly  
**Fluency**: Read naturally in target language

```
Source (EN): "Click the button to save your changes"
❌ BAD (Too literal): "点击按钮来保存你的变更" (awkward in Chinese)
✅ GOOD (Fluent): "点击按钮保存" (natural Chinese)

Source (EN): "The system will automatically retry"
❌ BAD (Too free): "会再试一次" (loses "automatically")
✅ GOOD (Accurate + Fluent): "系统将自动重试"
```

### 1.2 Target Audience

Adapt language register to audience:

```
Technical Documentation:
EN: "Initialize the database connection"
ZH: "初始化数据库连接" (technical term preserved)

User-Facing UI:
EN: "Sign in"
ZH: "登录" (simple, common term)

Marketing Copy:
EN: "Transform your workflow"
ZH: "让工作流程焕然一新" (more expressive)
```

---

## 2. Translation Workflow

### 2.1 Standard Process

```
1. Preparation
   - Analyze source text
   - Identify terminology
   - Research context
   - Create glossary

2. Translation
   - First draft (focus on accuracy)
   - Self-review (check fluency)
   - Terminology consistency check

3. Quality Assurance
   - Peer review
   - Back-translation (for critical content)
   - Native speaker review

4. Finalization
   - Incorporate feedback
   - Final proofreading
   - Delivery
```

### 2.2 CAT Tools (Computer-Assisted Translation)

```
Translation Memory (TM):
- Stores previously translated segments
- Suggests matches for similar content
- Ensures consistency

Example TM entry:
Source: "Save changes"
Target: "保存更改"
Context: Button label
Date: 2026-03-16
```

**Popular CAT Tools**:
- **SDL Trados Studio**: Industry standard
- **MemoQ**: User-friendly interface
- **OmegaT**: Free, open-source
- **Smartcat**: Cloud-based, free tier

---

## 3. Terminology Management

### 3.1 Glossary Creation

```markdown
# Project Glossary

| English | 中文 | Notes | Context |
|---------|------|-------|---------|
| Authentication | 身份验证 | Not 认证 | Technical |
| Authorization | 授权 | - | Technical |
| Repository | 仓库 | Git context | Technical |
| Commit | 提交 | Git action | Technical |
| Dashboard | 仪表板 | UI element | General |
| Settings | 设置 | UI element | General |
```

### 3.2 Consistency Rules

```
✅ GOOD: Consistent terminology
"Save" → "保存" (everywhere)
"Cancel" → "取消" (everywhere)

❌ BAD: Inconsistent
"Save" → "保存" (page 1)
"Save" → "储存" (page 2)
"Save" → "存档" (page 3)
```

### 3.3 Brand Names

```
✅ Keep brand names in original language
- GitHub → GitHub (not 吉特哈布)
- Docker → Docker (not 多克)

✅ Use official localized names when available
- Microsoft → 微软 (official Chinese name)
- Apple → 苹果 (official Chinese name)
```

---

## 4. Cultural Adaptation

### 4.1 Date and Time Formats

```
EN-US: 03/16/2026 (MM/DD/YYYY)
ZH-CN: 2026年3月16日 or 2026-03-16
JA-JP: 2026年3月16日
DE-DE: 16.03.2026 (DD.MM.YYYY)

Time:
EN-US: 2:30 PM
ZH-CN: 下午2:30 or 14:30
JA-JP: 午後2時30分
DE-DE: 14:30 Uhr
```

### 4.2 Numbers and Currency

```
Numbers:
EN-US: 1,234,567.89
ZH-CN: 1,234,567.89 or 1234567.89
FR-FR: 1 234 567,89
DE-DE: 1.234.567,89

Currency:
EN-US: $1,234.56
ZH-CN: ¥1,234.56 or 1234.56元
JA-JP: ¥1,234
EUR: 1.234,56€
```

### 4.3 Cultural References

```
❌ BAD: Direct translation loses meaning
EN: "Comparing apples to oranges"
ZH: "比较苹果和橙子" (meaningless in Chinese)

✅ GOOD: Equivalent idiom
ZH: "风马牛不相及" (unrelated things)

❌ BAD: Culture-specific reference
EN: "Thanksgiving sale"
ZH: "感恩节促销" (not celebrated in China)

✅ GOOD: Localized equivalent
ZH: "年末大促" (end-of-year sale)
```

---

## 5. Technical Translation

### 5.1 UI String Translation

```json
// en.json
{
  "button.save": "Save",
  "button.cancel": "Cancel",
  "message.success": "Changes saved successfully",
  "error.required": "{field} is required",
  "label.email": "Email Address"
}

// zh-CN.json
{
  "button.save": "保存",
  "button.cancel": "取消",
  "message.success": "保存成功",
  "error.required": "请填写{field}",
  "label.email": "电子邮箱"
}
```

**Guidelines**:
- Keep keys in English
- Use placeholders `{variable}` for dynamic content
- Maintain consistent tone across strings

### 5.2 Documentation Translation

```markdown
<!-- en/README.md -->
# Getting Started

Install the package:

\`\`\`bash
npm install my-package
\`\`\`

## Usage

Import and initialize:

\`\`\`javascript
const MyPackage = require('my-package');
const instance = new MyPackage();
\`\`\`

<!-- zh-CN/README.md -->
# 快速开始

安装包：

\`\`\`bash
npm install my-package
\`\`\`

## 使用方法

导入并初始化：

\`\`\`javascript
const MyPackage = require('my-package');
const instance = new MyPackage();
\`\`\`
```

**Guidelines**:
- Translate prose, keep code examples unchanged
- Keep technical terms (variable names, function names) in English
- Adapt examples to local conventions when relevant

---

## 6. Quality Assurance

### 6.1 QA Checklist

- [ ] **Completeness**: All source text translated?
- [ ] **Accuracy**: Meaning preserved?
- [ ] **Fluency**: Reads naturally?
- [ ] **Terminology**: Consistent with glossary?
- [ ] **Formatting**: Preserved (bold, italics, links)?
- [ ] **Placeholders**: `{variables}` intact?
- [ ] **Context**: Makes sense in target culture?
- [ ] **Grammar**: No errors?
- [ ] **Typos**: Spell-checked?

### 6.2 Back-Translation

```
Original (EN): "Delete this item permanently"
Translation (ZH): "永久删除此项目"
Back-translation (EN): "Permanently delete this item"
✅ Meaning preserved

Original (EN): "Save draft"
Translation (ZH): "保存草稿"
Back-translation (EN): "Save draft"
✅ Accurate

Original (EN): "Verify email"
Translation (ZH): "邮件验证"
Back-translation (EN): "Email verification" (noun instead of verb)
⚠️ Check if context requires verb form
```

---

## 7. Translation Memory (TM)

### 7.1 TM Entry Structure

```xml
<tu>
  <tuv xml:lang="en-US">
    <seg>Click here to learn more</seg>
  </tuv>
  <tuv xml:lang="zh-CN">
    <seg>点击此处了解更多</seg>
  </tuv>
  <prop type="x-context">Button label</prop>
  <prop type="x-project">Website</prop>
</tu>
```

### 7.2 Leveraging TM

```
New source: "Click here to continue"
TM match: "Click here to learn more" (90% match)
Suggested translation: "点击此处了解更多"
Translator edits: "点击此处继续"
```

**Benefits**:
- Faster translation
- Consistent terminology
- Reduced cost (recycling translations)

---

## 8. Localization (L10n) vs Internationalization (i18n)

### 8.1 Internationalization (i18n)

**Prepare code for multiple languages**:

```javascript
// ❌ BAD: Hardcoded strings
function greet(name) {
  return "Hello, " + name;
}

// ✅ GOOD: Externalized strings
function greet(name) {
  return t('greeting.hello', { name });
}
```

### 8.2 Localization (L10n)

**Adapt to specific locale**:

```javascript
// Date formatting
const date = new Date('2026-03-16');

// EN-US
date.toLocaleDateString('en-US'); // "3/16/2026"

// ZH-CN
date.toLocaleDateString('zh-CN'); // "2026/3/16"

// Number formatting
const num = 1234567.89;

// EN-US
num.toLocaleString('en-US'); // "1,234,567.89"

// ZH-CN
num.toLocaleString('zh-CN'); // "1,234,567.89"

// DE-DE
num.toLocaleString('de-DE'); // "1.234.567,89"
```

---

## 9. Common Challenges

### 9.1 Untranslatable Terms

```
✅ Keep in English + add explanation
EN: "Repository"
ZH: "Repository（代码仓库）"

✅ Transliterate + explanation
EN: "WiFi"
ZH: "Wi-Fi（无线网络）"
```

### 9.2 Length Variation

```
EN: "OK" (2 chars)
DE: "OK" (2 chars)
FR: "OK" (2 chars)
✅ Similar length

EN: "Save" (4 chars)
DE: "Speichern" (10 chars)
⚠️ German text 2.5x longer

Solution: Design UI with flexible space
```

### 9.3 Right-to-Left (RTL) Languages

```css
/* LTR (English, Chinese) */
.container {
  text-align: left;
  direction: ltr;
}

/* RTL (Arabic, Hebrew) */
.container[dir="rtl"] {
  text-align: right;
  direction: rtl;
}
```

---

## 10. Tools and Resources

### 10.1 Machine Translation

**Use for**:
- First draft (post-editing)
- Gisting (understanding source)
- Terminology research

**Don't use for**:
- Final delivery (without review)
- Creative content
- Legal/medical documents

**Popular MT engines**:
- Google Translate
- DeepL (high quality for European languages)
- Microsoft Translator

### 10.2 Quality Estimation

```
BLEU Score (0-100):
- >60: Good quality
- 40-60: Acceptable with editing
- <40: Requires significant revision

Example:
Source: "Save your changes"
Translation: "保存您的更改"
BLEU: 85 (high quality)
```

---

## Anti-Patterns

### ❌ Word-for-Word Translation
Translating each word individually without considering sentence structure.

**Solution**: Translate meaning, not words.

### ❌ Ignoring Context
Translating without understanding how/where text is used.

**Solution**: Request context or screenshots.

### ❌ Inconsistent Terminology
Using different terms for the same concept.

**Solution**: Create and follow glossary.

### ❌ Over-Localization
Changing content unnecessarily for local market.

**Solution**: Preserve original intent, adapt only when culturally necessary.

### ❌ Ignoring Formatting
Breaking bold/italic/link markup during translation.

**Solution**: Preserve all formatting tags.

---

## Related Modules

- **I18N_GUIDE** - Technical internationalization implementation
- **ACADEMIC_WRITING** - Academic translation standards
- **DOCUMENT_STRUCTURE** - Document organization across languages

---

## Resources

**Translation Tools**:
- SDL Trados: https://www.trados.com/
- MemoQ: https://www.memoq.com/
- OmegaT: https://omegat.org/

**Quality Assurance**:
- Xbench: QA tool for translations
- ErrorSpy: QA for CAT tools

**Standards**:
- ISO 17100: Translation services standard
- ASTM F2575: Quality assurance in translation
