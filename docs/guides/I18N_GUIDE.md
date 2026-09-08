# I18N GUIDE

**Status**: Active | **Domain**: Feature  
**Related Modules**: TRANSLATION_GUIDE, FRONTEND_STANDARDS, API_DESIGN

## Purpose

This module provides technical guidance for implementing internationalization (i18n) in applications, covering locale management, text externalization, date/number formatting, RTL support, and pluralization.

## When to Use This Module

- Building multi-language applications
- Implementing locale switching
- Formatting dates, numbers, and currencies
- Supporting right-to-left languages
- Managing translation files
- Implementing pluralization rules

---

## 1. Core Concepts

### 1.1 i18n vs L10n

**Internationalization (i18n)**: Prepare code for multiple languages
**Localization (L10n)**: Adapt for specific locale

```typescript
// i18n: Externalize strings
t('greeting.hello', { name })

// L10n: Provide translations
en: "Hello, {name}"
fr: "Bonjour, {name}"
ja: "こんにちは、{name}"
```

### 1.2 Locale Codes

**Format**: `language-REGION` (BCP 47)

```
en-US  (English - United States)
en-GB  (English - United Kingdom)
es-ES  (Spanish - Spain)
es-MX  (Spanish - Mexico)
zh-CN  (Chinese - Simplified, China)
zh-TW  (Chinese - Traditional, Taiwan)
pt-BR  (Portuguese - Brazil)
pt-PT  (Portuguese - Portugal)
```

---

## 2. Text Externalization

### 2.1 Never Hardcode Strings

```typescript
// ❌ BAD: Hardcoded
function Greeting({ name }) {
  return <h1>Welcome, {name}!</h1>;
}

// ✅ GOOD: Externalized
function Greeting({ name }) {
  const { t } = useTranslation();
  return <h1>{t('greeting.welcome', { name })}</h1>;
}
```

### 2.2 Translation File Structure

```json
// locales/en/common.json
{
  "greeting": {
    "welcome": "Welcome, {{name}}!",
    "goodbye": "Goodbye, {{name}}!"
  },
  "nav": {
    "home": "Home",
    "about": "About",
    "contact": "Contact"
  },
  "form": {
    "submit": "Submit",
    "cancel": "Cancel",
    "required": "This field is required"
  }
}

// locales/es/common.json
{
  "greeting": {
    "welcome": "¡Bienvenido, {{name}}!",
    "goodbye": "¡Adiós, {{name}}!"
  },
  "nav": {
    "home": "Inicio",
    "about": "Acerca de",
    "contact": "Contacto"
  },
  "form": {
    "submit": "Enviar",
    "cancel": "Cancelar",
    "required": "Este campo es obligatorio"
  }
}
```

### 2.3 Namespaces

```typescript
// Organize by feature/page
i18n.loadNamespaces(['common', 'dashboard', 'settings']);

// Use specific namespace
const { t } = useTranslation('dashboard');
t('metrics.users');  // dashboard:metrics.users
```

---

## 3. React i18next Implementation

### 3.1 Setup

```bash
npm install react-i18next i18next i18next-http-backend
```

```typescript
// i18n.ts
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';

i18n
  .use(Backend)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    debug: process.env.NODE_ENV === 'development',
    interpolation: {
      escapeValue: false,  // React already escapes
    },
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },
  });

export default i18n;
```

```typescript
// App.tsx
import './i18n';

function App() {
  return <Router>...</Router>;
}
```

### 3.2 Usage in Components

```typescript
import { useTranslation } from 'react-i18next';

function WelcomeMessage() {
  const { t, i18n } = useTranslation();

  const changeLanguage = (lng: string) => {
    i18n.changeLanguage(lng);
  };

  return (
    <div>
      <h1>{t('greeting.welcome', { name: 'John' })}</h1>
      <select value={i18n.language} onChange={(e) => changeLanguage(e.target.value)}>
        <option value="en">English</option>
        <option value="es">Español</option>
        <option value="fr">Français</option>
      </select>
    </div>
  );
}
```

### 3.3 Pluralization

```json
// en/common.json
{
  "items": "{{count}} item",
  "items_plural": "{{count}} items"
}

// fr/common.json (French has different plural rules)
{
  "items": "{{count}} élément",
  "items_plural": "{{count}} éléments"
}

// ar/common.json (Arabic has 6 plural forms!)
{
  "items_zero": "لا عناصر",
  "items_one": "عنصر واحد",
  "items_two": "عنصران",
  "items_few": "{{count}} عناصر",
  "items_many": "{{count}} عنصراً",
  "items_other": "{{count}} عنصر"
}
```

```typescript
t('items', { count: 0 });  // "0 items"
t('items', { count: 1 });  // "1 item"
t('items', { count: 5 });  // "5 items"
```

---

## 4. Date and Time Formatting

### 4.1 Intl.DateTimeFormat

```typescript
const date = new Date('2026-03-16T14:30:00');

// English (US)
new Intl.DateTimeFormat('en-US').format(date);
// "3/16/2026"

// English (UK)
new Intl.DateTimeFormat('en-GB').format(date);
// "16/03/2026"

// Japanese
new Intl.DateTimeFormat('ja-JP').format(date);
// "2026/3/16"

// With time
new Intl.DateTimeFormat('en-US', {
  dateStyle: 'long',
  timeStyle: 'short'
}).format(date);
// "March 16, 2026 at 2:30 PM"
```

### 4.2 Relative Time

```typescript
const rtf = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });

rtf.format(-1, 'day');    // "yesterday"
rtf.format(0, 'day');     // "today"
rtf.format(1, 'day');     // "tomorrow"
rtf.format(-2, 'week');   // "2 weeks ago"
rtf.format(3, 'month');   // "in 3 months"
```

### 4.3 Using date-fns with Locales

```typescript
import { format } from 'date-fns';
import { enUS, es, ja } from 'date-fns/locale';

const date = new Date('2026-03-16');

format(date, 'PPP', { locale: enUS });  // "March 16th, 2026"
format(date, 'PPP', { locale: es });    // "16 de marzo de 2026"
format(date, 'PPP', { locale: ja });    // "2026年3月16日"
```

---

## 5. Number and Currency Formatting

### 5.1 Number Formatting

```typescript
const number = 1234567.89;

// US: Commas as thousand separators, period as decimal
new Intl.NumberFormat('en-US').format(number);
// "1,234,567.89"

// Germany: Periods as thousand separators, comma as decimal
new Intl.NumberFormat('de-DE').format(number);
// "1.234.567,89"

// India: Lakhs and crores system
new Intl.NumberFormat('en-IN').format(number);
// "12,34,567.89"
```

### 5.2 Currency Formatting

```typescript
const amount = 1234.56;

// US Dollars
new Intl.NumberFormat('en-US', {
  style: 'currency',
  currency: 'USD'
}).format(amount);
// "$1,234.56"

// Euros (Germany)
new Intl.NumberFormat('de-DE', {
  style: 'currency',
  currency: 'EUR'
}).format(amount);
// "1.234,56 €"

// Japanese Yen (no decimals)
new Intl.NumberFormat('ja-JP', {
  style: 'currency',
  currency: 'JPY'
}).format(amount);
// "¥1,235"
```

### 5.3 Percentages

```typescript
new Intl.NumberFormat('en-US', {
  style: 'percent',
  minimumFractionDigits: 1
}).format(0.1234);
// "12.3%"
```

---

## 6. Right-to-Left (RTL) Support

### 6.1 Detect RTL Languages

```typescript
const RTL_LANGUAGES = ['ar', 'he', 'fa', 'ur'];

function isRTL(language: string): boolean {
  return RTL_LANGUAGES.includes(language);
}
```

### 6.2 CSS for RTL

```css
/* Base styles */
.container {
  text-align: left;
  direction: ltr;
}

/* RTL override */
[dir="rtl"] .container {
  text-align: right;
  direction: rtl;
}

/* Logical properties (better approach) */
.container {
  text-align: start;  /* left in LTR, right in RTL */
  padding-inline-start: 16px;  /* padding-left in LTR, padding-right in RTL */
}
```

### 6.3 React RTL Support

```typescript
import { useEffect } from 'react';
import { useTranslation } from 'react-i18next';

function App() {
  const { i18n } = useTranslation();

  useEffect(() => {
    const dir = isRTL(i18n.language) ? 'rtl' : 'ltr';
    document.documentElement.setAttribute('dir', dir);
  }, [i18n.language]);

  return <div>...</div>;
}
```

---

## 7. Backend i18n

### 7.1 Express with i18next

```typescript
import i18next from 'i18next';
import Backend from 'i18next-fs-backend';
import middleware from 'i18next-http-middleware';

i18next
  .use(Backend)
  .use(middleware.LanguageDetector)
  .init({
    fallbackLng: 'en',
    preload: ['en', 'es', 'fr'],
    backend: {
      loadPath: './locales/{{lng}}/{{ns}}.json'
    }
  });

app.use(middleware.handle(i18next));

app.get('/api/welcome', (req, res) => {
  res.json({
    message: req.t('greeting.welcome', { name: 'John' })
  });
});
```

### 7.2 Email Templates

```typescript
// Localized email templates
const templates = {
  en: {
    subject: 'Welcome to Our Service!',
    body: 'Hello {{name}}, thank you for signing up...'
  },
  es: {
    subject: '¡Bienvenido a Nuestro Servicio!',
    body: 'Hola {{name}}, gracias por registrarte...'
  }
};

function sendWelcomeEmail(user: User, locale: string) {
  const template = templates[locale] || templates.en;
  const subject = template.subject;
  const body = template.body.replace('{{name}}', user.name);
  
  sendEmail(user.email, subject, body);
}
```

---

## 8. Best Practices

### 8.1 Context for Translators

```json
// ❌ BAD: No context
{
  "save": "Save"
}

// ✅ GOOD: With context
{
  "button": {
    "save": "Save",
    "_comment": "Button label for saving changes"
  }
}

// ✅ BETTER: Structured keys
{
  "form": {
    "button": {
      "save": "Save Changes",
      "cancel": "Cancel"
    }
  },
  "file": {
    "menu": {
      "save": "Save File"
    }
  }
}
```

### 8.2 Variables in Translations

```json
{
  "greeting": "Hello, {{name}}!",
  "itemCount": "You have {{count}} items in your cart",
  "dateFormat": "Last updated on {{date}}"
}
```

```typescript
t('greeting', { name: 'John' });
t('itemCount', { count: 5 });
t('dateFormat', { date: new Date().toLocaleDateString() });
```

### 8.3 Handle Missing Translations

```typescript
i18n.init({
  fallbackLng: 'en',
  saveMissing: true,  // Save missing keys
  missingKeyHandler: (lng, ns, key, fallbackValue) => {
    console.warn(`Missing translation: ${lng}:${ns}:${key}`);
    // Report to monitoring service
  }
});
```

---

## 9. Testing

### 9.1 Test with Different Locales

```typescript
import { render } from '@testing-library/react';
import { I18nextProvider } from 'react-i18next';
import i18n from './test-i18n';

test('renders welcome message in Spanish', () => {
  i18n.changeLanguage('es');
  
  const { getByText } = render(
    <I18nextProvider i18n={i18n}>
      <WelcomeMessage name="Juan" />
    </I18nextProvider>
  );
  
  expect(getByText(/Bienvenido, Juan/)).toBeInTheDocument();
});
```

### 8.2 Test Pluralization

```typescript
test('handles plural forms correctly', () => {
  expect(t('items', { count: 0 })).toBe('0 items');
  expect(t('items', { count: 1 })).toBe('1 item');
  expect(t('items', { count: 5 })).toBe('5 items');
});
```

---

## 10. Performance

### 10.1 Lazy Load Namespaces

```typescript
// Load only needed namespaces
const { t } = useTranslation(['common', 'dashboard']);

// Load on demand
i18n.loadNamespaces('settings').then(() => {
  // Translations available
});
```

### 10.2 Bundle Optimization

```javascript
// webpack.config.js
module.exports = {
  plugins: [
    new webpack.IgnorePlugin({
      resourceRegExp: /^\.\/locale$/,
      contextRegExp: /moment$/
    })
  ]
};
```

---

## Anti-Patterns

### ❌ String Concatenation
Building sentences from parts doesn't work in all languages.

```typescript
// ❌ BAD
t('you.have') + ' ' + count + ' ' + t('items')
// Doesn't work in languages with different word order

// ✅ GOOD
t('itemCount', { count })
```

### ❌ Splitting Sentences
Some languages require different structure.

```json
// ❌ BAD
{
  "click": "Click",
  "here": "here",
  "to": "to",
  "continue": "continue"
}

// ✅ GOOD
{
  "clickToContinue": "Click here to continue"
}
```

### ❌ Hardcoded Formats
Don't assume formats work everywhere.

```typescript
// ❌ BAD: US date format hardcoded
`${month}/${day}/${year}`

// ✅ GOOD: Locale-aware
new Intl.DateTimeFormat(locale).format(date)
```

---

## Related Modules

- **TRANSLATION_GUIDE** - Translation workflow and quality
- **FRONTEND_STANDARDS** - React component patterns
- **API_DESIGN** - API internationalization

---

## Resources

**Libraries**:
- react-i18next: https://react.i18next.com/
- i18next: https://www.i18next.com/
- Format.JS: https://formatjs.io/

**Standards**:
- BCP 47: https://tools.ietf.org/html/bcp47
- Unicode CLDR: http://cldr.unicode.org/
