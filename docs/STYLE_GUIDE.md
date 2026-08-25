# Style Guide (程式碼風格指南)

**Version**: 2.0.0  
**Module**: STYLE_GUIDE  
**Loading**: Always (Core module)  
**Purpose**: Universal code style conventions for AI agents and developers.

---

## Overview

This guide defines **consistent code style conventions** across all project types (frontend, backend, fullstack, academic, CLI, library). It ensures readable, maintainable, and professional code.

**Scope**:
- ✅ Universal principles (all languages, all projects)
- ✅ Naming conventions (variables, functions, files)
- ✅ Code structure (indentation, line length, comments)
- ✅ Documentation requirements
- ❌ Language-specific patterns (see FRONTEND_PATTERNS, BACKEND_PATTERNS)

**Loading Trigger**: Always loaded (Core module)

---

## Core Principles

### 1. Readability First

**Code is read 10x more than it's written.**

✅ **DO**:
```typescript
function calculateMonthlyPayment(principal: number, annualRate: number, months: number): number {
  const monthlyRate = annualRate / 12;
  return (principal * monthlyRate) / (1 - Math.pow(1 + monthlyRate, -months));
}
```

❌ **DON'T**:
```typescript
function calc(p: number, r: number, m: number): number {
  const mr = r / 12;
  return (p * mr) / (1 - Math.pow(1 + mr, -m));
}
```

**Why**: Clear names document intent, reducing cognitive load.

### 2. Consistency Over Perfection

**Follow existing patterns in the codebase.**

If existing code uses:
- `snake_case` for file names → continue using `snake_case`
- 2-space indentation → continue 2-space
- Single quotes → continue single quotes

**Exception**: Security vulnerabilities, performance issues, or anti-patterns.

### 3. Simplicity Over Cleverness

**Simple code beats clever code.**

✅ **DO**:
```typescript
if (user.isActive && user.hasPermission('admin')) {
  grantAccess();
}
```

❌ **DON'T**:
```typescript
user.isActive && user.hasPermission('admin') && grantAccess();
```

**Why**: Explicit `if` statements are clearer than boolean short-circuit tricks.

### 4. Fail Fast, Fail Loud

**Validate inputs early, throw meaningful errors.**

✅ **DO**:
```typescript
function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error('Division by zero: denominator cannot be zero');
  }
  return a / b;
}
```

❌ **DON'T**:
```typescript
function divide(a: number, b: number): number {
  return a / b;  // Returns Infinity, silently fails
}
```

### 5. No Magic Numbers

**Extract constants with meaningful names.**

✅ **DO**:
```typescript
const MAX_LOGIN_ATTEMPTS = 5;
const SESSION_TIMEOUT_MS = 30 * 60 * 1000;  // 30 minutes

if (loginAttempts > MAX_LOGIN_ATTEMPTS) {
  lockAccount();
}
```

❌ **DON'T**:
```typescript
if (loginAttempts > 5) {
  lockAccount();
}
```

---

## Naming Conventions

### Variables

**Rule**: Use descriptive, noun-based names.

| Type | Convention | Example | ❌ Avoid |
|------|-----------|---------|---------|
| Boolean | `is`, `has`, `should`, `can` prefix | `isActive`, `hasPermission`, `shouldValidate` | `active`, `permission` |
| Array/List | Plural nouns | `users`, `products`, `errors` | `userList`, `userArray` |
| Count/Total | `count`, `total`, `num` prefix | `userCount`, `totalPrice`, `numAttempts` | `users` (ambiguous) |
| Temporary | Meaningful context | `tempUser`, `cachedResult` | `tmp`, `x`, `data` |

**Examples**:

✅ **Good**:
```typescript
const isAuthenticated = true;
const activeUsers = fetchActiveUsers();
const userCount = activeUsers.length;
```

❌ **Bad**:
```typescript
const auth = true;
const users = fetchActiveUsers();  // Ambiguous: all users or active users?
const num = users.length;  // num of what?
```

### Functions

**Rule**: Use verb-based names describing action.

| Pattern | Convention | Example | Use Case |
|---------|-----------|---------|----------|
| Action | `verb + noun` | `getUser`, `saveOrder`, `deleteComment` | General operations |
| Boolean Return | `is`, `has`, `should`, `can` prefix | `isValidEmail`, `hasPermission`, `canEdit` | Predicates |
| Event Handler | `handle` + event | `handleClick`, `handleSubmit`, `handleError` | UI events |
| Async | `async` suffix (optional) | `fetchUserAsync`, `saveOrderAsync` | Async operations |

**Examples**:

✅ **Good**:
```typescript
function getUserById(id: string): User { }
function isValidEmail(email: string): boolean { }
function handleFormSubmit(event: Event): void { }
```

❌ **Bad**:
```typescript
function user(id: string): User { }  // Not a verb
function email(email: string): boolean { }  // Ambiguous
function submit(event: Event): void { }  // Too generic
```

### Classes

**Rule**: Use PascalCase, noun-based names.

| Type | Convention | Example | Notes |
|------|-----------|---------|-------|
| Entity | Singular noun | `User`, `Product`, `Order` | Domain objects |
| Service | `Service` suffix | `UserService`, `PaymentService` | Business logic |
| Controller | `Controller` suffix | `UserController`, `ApiController` | Request handlers |
| Utility | Descriptive noun | `StringUtil`, `DateFormatter` | Helper classes |
| Abstract | `Abstract` prefix | `AbstractRepository`, `AbstractFactory` | Base classes |
| Interface (TS) | `I` prefix (optional) | `IUserService`, `UserService` | TypeScript interfaces |

**Examples**:

✅ **Good**:
```typescript
class UserService { }
class PaymentProcessor { }
class AuthenticationMiddleware { }
```

❌ **Bad**:
```typescript
class userService { }  // Not PascalCase
class Process { }  // Too generic
class DoStuff { }  // Not a noun
```

### Files

**Rule**: Match primary export, use consistent casing.

| Project Type | Convention | Example | Notes |
|--------------|-----------|---------|-------|
| React Component | PascalCase | `UserProfile.tsx` | Component name = file name |
| TypeScript Module | camelCase | `userService.ts` | Class/function name = file name |
| Python Module | snake_case | `user_service.py` | PEP 8 convention |
| Config Files | kebab-case | `jest.config.js`, `tsconfig.json` | Standard practice |
| Test Files | `*.test.*` or `*.spec.*` | `userService.test.ts`, `UserProfile.spec.tsx` | Framework convention |

**Examples**:

✅ **Good**:
```
src/
├── components/
│   ├── UserProfile.tsx       # React component
│   └── Button.tsx
├── services/
│   ├── userService.ts        # TypeScript class
│   └── authService.ts
├── utils/
│   ├── stringUtils.ts        # Utility functions
│   └── dateUtils.ts
└── __tests__/
    ├── userService.test.ts
    └── UserProfile.test.tsx
```

❌ **Bad**:
```
src/
├── UserProfile.tsx            # OK
├── userprofile.tsx            # Inconsistent casing
├── user-profile.tsx           # Wrong convention for React
├── UserService.ts             # Should be userService.ts
└── user_service.py            # Python style in TypeScript project
```

### Constants

**Rule**: SCREAMING_SNAKE_CASE for module-level constants.

✅ **Good**:
```typescript
const API_BASE_URL = 'https://api.example.com';
const MAX_RETRY_ATTEMPTS = 3;
const DEFAULT_TIMEOUT_MS = 5000;
```

❌ **Bad**:
```typescript
const apiBaseUrl = 'https://api.example.com';
const maxRetryAttempts = 3;
const DefaultTimeout = 5000;
```

**Exception**: Enum-like objects use PascalCase:
```typescript
const HttpStatus = {
  OK: 200,
  NOT_FOUND: 404,
  INTERNAL_ERROR: 500,
} as const;
```

---

## Code Structure

### Indentation

**Rule**: Use 2 spaces (never tabs), except where language/tooling dictates otherwise.

| Language | Convention | Notes |
|----------|-----------|-------|
| JavaScript/TypeScript | 2 spaces | Standard (Prettier, ESLint) |
| Python | 4 spaces | PEP 8 |
| Go | Tabs | `gofmt` standard |
| Ruby | 2 spaces | RuboCop default |
| Java | 4 spaces | Common practice |

**Why 2 spaces for JS/TS**: Reduces nesting depth, works well with React JSX.

### Line Length

**Rule**: 80-120 characters max.

| Language | Limit | Enforcement |
|----------|-------|-------------|
| JavaScript/TypeScript | 100 chars | Prettier default |
| Python | 79 chars | PEP 8 (88 with Black) |
| Go | 120 chars | `gofmt` doesn't enforce |
| Markdown | 120 chars | Readability |

**Exception**: URLs, import statements, long strings can exceed limit.

### Line Breaks

**Rule**: One statement per line.

✅ **Good**:
```typescript
const user = getUser();
const isValid = validateUser(user);
const result = processUser(user);
```

❌ **Bad**:
```typescript
const user = getUser(); const isValid = validateUser(user); const result = processUser(user);
```

**Exception**: Short object properties, array items:
```typescript
const point = { x: 10, y: 20 };
const colors = ['red', 'green', 'blue'];
```

### Blank Lines

**Rule**: Use blank lines to separate logical sections.

✅ **Good**:
```typescript
function processOrder(order: Order): void {
  // Validate input
  if (!order.id) {
    throw new Error('Order ID required');
  }

  // Calculate total
  const total = order.items.reduce((sum, item) => sum + item.price, 0);

  // Save to database
  saveOrder({ ...order, total });

  // Send notification
  sendOrderConfirmation(order.customerEmail);
}
```

❌ **Bad** (no blank lines):
```typescript
function processOrder(order: Order): void {
  if (!order.id) {
    throw new Error('Order ID required');
  }
  const total = order.items.reduce((sum, item) => sum + item.price, 0);
  saveOrder({ ...order, total });
  sendOrderConfirmation(order.customerEmail);
}
```

### Function Length

**Rule**: Max 50 lines per function (soft limit).

**When exceeding**:
1. Extract helper functions
2. Split into smaller responsibilities
3. Document why complexity is necessary

**Example** (refactoring long function):

❌ **Before** (80 lines):
```typescript
function processUserRegistration(data: any): void {
  // 80 lines of validation, DB saves, email sending, logging...
}
```

✅ **After** (modular):
```typescript
function processUserRegistration(data: UserData): void {
  validateUserData(data);
  const user = createUser(data);
  sendWelcomeEmail(user.email);
  logRegistration(user.id);
}
```

### Nesting Depth

**Rule**: Max 3 levels of nesting.

✅ **Good** (early return):
```typescript
function getDiscount(user: User, order: Order): number {
  if (!user.isPremium) return 0;
  if (order.total < 100) return 0;
  return order.total * 0.1;
}
```

❌ **Bad** (deep nesting):
```typescript
function getDiscount(user: User, order: Order): number {
  if (user.isPremium) {
    if (order.total >= 100) {
      return order.total * 0.1;
    } else {
      return 0;
    }
  } else {
    return 0;
  }
}
```

---

## Comments

### When to Comment

**Rule**: Explain **WHY**, not **WHAT**.

✅ **Good** (explains reasoning):
```typescript
// Use exponential backoff to avoid overwhelming the API during outages
const retryDelay = Math.pow(2, attemptNumber) * 1000;
```

❌ **Bad** (states the obvious):
```typescript
// Calculate retry delay
const retryDelay = Math.pow(2, attemptNumber) * 1000;
```

### Comment Types

| Type | When to Use | Example |
|------|-------------|---------|
| **Inline** | Clarify complex logic | `// Edge case: handle empty array` |
| **Block** | Document function intent | `/** Calculate monthly loan payment */` |
| **TODO** | Mark incomplete work | `// TODO: Add rate limiting` |
| **FIXME** | Mark known bugs | `// FIXME: Race condition with async updates` |
| **NOTE** | Highlight important context | `// NOTE: This API is deprecated, migrate to v2` |

**Examples**:

✅ **Good**:
```typescript
/**
 * Calculate compound interest using the formula: A = P(1 + r/n)^(nt)
 * 
 * @param principal - Initial investment amount
 * @param rate - Annual interest rate (e.g., 0.05 for 5%)
 * @param years - Investment duration in years
 * @returns Final amount including interest
 */
function calculateCompoundInterest(principal: number, rate: number, years: number): number {
  const n = 12;  // Compound monthly
  return principal * Math.pow(1 + rate / n, n * years);
}
```

### TODOs and FIXMEs

**Rule**: Include assignee and date.

✅ **Good**:
```typescript
// TODO(@justyn, 2026-03-16): Implement OAuth 2.0 authentication
// FIXME(@team, 2026-03-10): Memory leak in WebSocket connection
```

❌ **Bad**:
```typescript
// TODO: Fix this later
// FIXME: Broken
```

---

## Documentation

### Function Documentation

**Rule**: Document all public functions with JSDoc/docstrings.

**Template** (TypeScript):
```typescript
/**
 * {Brief description of what function does}
 * 
 * {Optional: Extended description, edge cases, examples}
 * 
 * @param {type} paramName - Description
 * @param {type} paramName - Description
 * @returns {type} Description
 * @throws {ErrorType} When this error occurs
 * 
 * @example
 * const result = myFunction(arg1, arg2);
 */
```

**Example**:
```typescript
/**
 * Fetch user by ID from database with caching.
 * 
 * Uses Redis cache with 5-minute TTL. Falls back to database on cache miss.
 * 
 * @param userId - Unique user identifier
 * @returns User object if found
 * @throws {NotFoundError} If user doesn't exist
 * @throws {DatabaseError} If database connection fails
 * 
 * @example
 * const user = await getUserById('user_123');
 * console.log(user.email);
 */
async function getUserById(userId: string): Promise<User> {
  // Implementation...
}
```

### Class Documentation

**Rule**: Document class purpose and key methods.

```typescript
/**
 * Manages user authentication and session handling.
 * 
 * Supports JWT token-based auth with Redis session storage.
 * Implements refresh token rotation for security.
 * 
 * @example
 * const auth = new AuthService();
 * const token = await auth.login(email, password);
 */
class AuthService {
  /**
   * Authenticate user with email and password.
   * 
   * @param email - User email address
   * @param password - Plain text password (hashed internally)
   * @returns JWT access token
   * @throws {InvalidCredentialsError} If email/password incorrect
   */
  async login(email: string, password: string): Promise<string> {
    // Implementation...
  }
}
```

### README Requirements

**Every project must have**:
- 📌 Project description (1-2 sentences)
- 🚀 Installation instructions
- ⚙️ Configuration options
- 📖 Usage examples
- 🤝 Contributing guidelines (if open-source)
- 📄 License information

See [README_STRUCTURE module](./.scaffolding/docs/README_STRUCTURE.md) (when available).

---

## Type Safety

### TypeScript

**Rule**: No `any`, use specific types.

✅ **Good**:
```typescript
interface User {
  id: string;
  email: string;
  createdAt: Date;
}

function getUser(id: string): User | null {
  // Implementation...
}
```

❌ **Bad**:
```typescript
function getUser(id: any): any {
  // Implementation...
}
```

**Exception**: External library types unavailable → use `unknown` and type guard:
```typescript
function parseJSON(json: string): unknown {
  return JSON.parse(json);
}

const data = parseJSON(input);
if (typeof data === 'object' && data !== null && 'name' in data) {
  // TypeScript knows 'name' exists
  console.log(data.name);
}
```

### Python

**Rule**: Use type hints for function signatures.

✅ **Good**:
```python
from typing import List, Optional

def get_user_emails(user_ids: List[str]) -> List[str]:
    """Fetch emails for given user IDs."""
    # Implementation...

def find_user(email: str) -> Optional[User]:
    """Return user if found, None otherwise."""
    # Implementation...
```

❌ **Bad**:
```python
def get_user_emails(user_ids):
    # Implementation...

def find_user(email):
    # Implementation...
```

---

## Error Handling

### Rule: Explicit Error Handling

✅ **Good** (catch specific errors):
```typescript
try {
  const data = await fetchData();
  processData(data);
} catch (error) {
  if (error instanceof NetworkError) {
    logger.error('Network failure:', error);
    retryFetch();
  } else if (error instanceof ValidationError) {
    logger.warn('Invalid data:', error);
    notifyUser(error.message);
  } else {
    logger.error('Unexpected error:', error);
    throw error;  // Re-throw unknown errors
  }
}
```

❌ **Bad** (silent catch-all):
```typescript
try {
  const data = await fetchData();
  processData(data);
} catch (error) {
  // Silent failure
}
```

### Custom Error Classes

**Rule**: Create domain-specific error classes.

```typescript
class NotFoundError extends Error {
  constructor(resource: string, id: string) {
    super(`${resource} not found: ${id}`);
    this.name = 'NotFoundError';
  }
}

class ValidationError extends Error {
  constructor(field: string, value: any) {
    super(`Invalid ${field}: ${value}`);
    this.name = 'ValidationError';
  }
}
```

---

## Testing

### Test File Naming

**Rule**: Mirror source file structure.

```
src/
├── services/
│   └── userService.ts
└── components/
    └── UserProfile.tsx

tests/ or __tests__/
├── services/
│   └── userService.test.ts
└── components/
    └── UserProfile.test.tsx
```

### Test Function Naming

**Rule**: Descriptive sentences with "should".

✅ **Good**:
```typescript
describe('UserService', () => {
  describe('getUser', () => {
    it('should return user when ID exists', () => { });
    it('should throw NotFoundError when ID not found', () => { });
    it('should cache result for 5 minutes', () => { });
  });
});
```

❌ **Bad**:
```typescript
test('getUser works', () => { });
test('getUser error', () => { });
```

---

## Import Organization

### Rule: Group imports by source.

```typescript
// 1. External dependencies
import React from 'react';
import { useState } from 'react';
import axios from 'axios';

// 2. Internal absolute imports
import { UserService } from '@/services/userService';
import { Button } from '@/components/Button';

// 3. Relative imports
import { formatDate } from './utils';
import type { User } from './types';

// 4. Styles (if applicable)
import './UserProfile.css';
```

### Rule: Sort alphabetically within groups.

✅ **Good**:
```typescript
import axios from 'axios';
import React from 'react';
import { useEffect, useState } from 'react';
```

---

## Consistency Checklist

Before committing code, verify:

- [ ] Naming follows conventions (camelCase, PascalCase, SCREAMING_SNAKE_CASE)
- [ ] Functions < 50 lines
- [ ] Nesting depth ≤ 3 levels
- [ ] No magic numbers
- [ ] Comments explain WHY, not WHAT
- [ ] Type annotations present (TS/Python)
- [ ] Error handling explicit
- [ ] Tests mirror source structure
- [ ] Imports organized and sorted

---

## Language-Specific Guides

**This module covers universal conventions. For language-specific patterns, load:**

| Language/Framework | Module | When Loaded |
|--------------------|--------|-------------|
| React/Next.js | FRONTEND_PATTERNS | type=frontend or fullstack |
| Node.js/Express | BACKEND_PATTERNS | type=backend or fullstack |
| Database/SQL | DATABASE_CONVENTIONS | features contains "database" |
| Academic Writing | ACADEMIC_WRITING | type=academic |

---

## Enforcement

### Automated Tools

**Recommended linters/formatters**:

| Language | Linter | Formatter | Config |
|----------|--------|-----------|--------|
| JavaScript/TypeScript | ESLint | Prettier | `.eslintrc.js`, `.prettierrc` |
| Python | Pylint, Flake8 | Black | `pyproject.toml`, `setup.cfg` |
| Go | golint | gofmt | (built-in) |
| Ruby | RuboCop | RuboCop | `.rubocop.yml` |

**Pre-commit hooks**: `.scaffolding/scripts/install-hooks.sh`

### Manual Review

**Code review checklist**:
- [ ] Follows project conventions
- [ ] Names are clear and consistent
- [ ] No commented-out code
- [ ] No unused imports
- [ ] No debug logs (`console.log`, `print`)

---

## Related Documentation

- **[TERMINOLOGY](./terminology/)** - Multilingual tech terms
- **[GIT_WORKFLOW](./GIT_WORKFLOW.md)** - Git conventions and commit messages
- **[FRONTEND_PATTERNS](./FRONTEND_PATTERNS.md)** - React/Next.js patterns (when available)
- **[BACKEND_PATTERNS](./BACKEND_PATTERNS.md)** - Node.js/Express patterns (when available)

---

**Version**: 2.0.0  
**Last Updated**: 2026-03-16  
**Maintainer**: my-vibe-scaffolding template
