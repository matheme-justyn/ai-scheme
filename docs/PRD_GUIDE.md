# PRD (Product Requirements Document) Writing Guide

> **For AI-assisted development with OpenCode/Cursor**  
> **Last Updated**: 2026-03-03

---

## 📋 Table of Contents

- [What is a PRD?](#what-is-a-prd)
- [Why PRD for AI Coding?](#why-prd-for-ai-coding)
- [Where to Place PRD](#where-to-place-prd)
- [PRD Template](#prd-template)
- [Writing Guidelines](#writing-guidelines)
- [Converting from Word/Google Docs](#converting-from-wordgoogle-docs)
- [Integration with AGENTS.md](#integration-with-agentsmd)
- [Best Practices](#best-practices)

---

## What is a PRD?

**Product Requirements Document (PRD)** - A comprehensive document that describes:
- **What** the product should do (features, functionality)
- **Why** we're building it (goals, user needs)
- **How** it should work (user flows, technical requirements)
- **When** features should be delivered (milestones)

**Purpose**: Bridge between product vision and technical implementation.

---

## Why PRD for AI Coding?

### Traditional Development
- PRD → PMs write, devs read → ask questions → implement
- Context scattered across: meetings, Slack, emails, brain

### AI-Assisted Development
- PRD → **Single source of truth** for AI
- AI reads PRD → generates code directly
- No context loss, no ambiguity

### Benefits with OpenCode/Cursor

| Without PRD | With PRD |
|-------------|----------|
| "Build a login feature" (vague) | Complete auth flow spec with edge cases |
| AI asks clarifying questions | AI has all context upfront |
| Inconsistent implementation | Follows documented standards |
| Lost context between sessions | PRD persists across sessions |

---

## Where to Place PRD

### Option 1: `docs/PRD.md` (Recommended ✅)

```
project-root/
├── README.md              # Project overview (user-facing)
├── AGENTS.md              # AI coding conventions
├── docs/
│   ├── PRD.md            # ← Product requirements (this is it!)
│   ├── architecture.md    # System architecture details
│   └── adr/              # Architecture decision records
```

**Pros**:
- ✅ Industry standard location
- ✅ Version controlled (team visibility)
- ✅ Accessible to both AI and humans
- ✅ Fits existing docs/ structure

**When to use**: Default choice for most projects.

---

### Option 2: `docs/specs/PRD.md` (Large Projects)

```
docs/
├── specs/
│   ├── PRD.md            # Product requirements
│   ├── system-design.md   # Technical design
│   └── data-model.md      # Database schema
└── adr/                  # Decisions
```

**When to use**: Multiple spec documents, need clear separation.

---

### Option 3: `.opencode/PRD.md` (AI-Exclusive)

```
.opencode/
├── INSTALL.md
├── PRD.md                # OpenCode-specific PRD
└── sessions/             # (gitignored)
```

**Pros**:
- ✅ Clear signal "this is for AI"
- ✅ Separate from user-facing docs

**Cons**:
- ❌ Human developers might miss it
- ❌ Not discoverable on GitHub

**When to use**: PRD contains AI-specific instructions, not general product spec.

---

## PRD Template

**Location**: `.scaffolding/docs/templates/PRD_TEMPLATE.md`

See full template with examples: [PRD_TEMPLATE.md](./templates/PRD_TEMPLATE.md)

**Quick structure**:
# [Project Name] - Product Requirements Document

## 1. Overview
- Problem statement
- Goals & objectives
- Target users

## 2. Features & Requirements
- Feature list with priorities
- User stories
- Edge cases

## 3. Technical Requirements
- Technology stack
- Performance requirements
- Security requirements

## 4. User Flows
- Flow diagrams (Mermaid)
- Screenshots/wireframes

## 5. Implementation Phases
- MVP scope
- Phase 1, 2, 3...
- Success metrics

---

## Writing Guidelines

### 1. Be Specific & Unambiguous

**❌ Bad**:
```
User should be able to log in.
```

**✅ Good**:
## Login Feature

**Requirements**:
- User logs in with email + password
- Max 5 failed attempts → lock account for 15 minutes
- Show error message: "Invalid credentials" (don't reveal if email exists)
- Remember me: 30-day session, else 24 hours
- Support OAuth: Google, GitHub

**Edge Cases**:
- Locked account → show unlock time remaining
- First-time user → redirect to onboarding
- Already logged in → redirect to dashboard

### 2. Use Structured Format

**Sections AI loves**:
- ✅ Numbered lists (priorities)
- ✅ Tables (comparisons, requirements matrix)
- ✅ Code blocks (API contracts, data schemas)
- ✅ Mermaid diagrams (flows, architecture)

**Example - API Spec in PRD**:
## API Requirements

### POST /api/auth/login

**Request**:
\`\`\`json
{
  "email": "user@example.com",
  "password": "hashed_value",
  "remember_me": true
}
\`\`\`

**Response (Success)**:
\`\`\`json
{
  "token": "jwt_token_here",
  "user": { "id": 1, "name": "John" },
  "expires_at": "2026-04-03T00:00:00Z"
}
\`\`\`

**Response (Error)**:
\`\`\`json
{
  "error": "Invalid credentials",
  "locked_until": "2026-03-03T14:30:00Z"  // if account locked
}
\`\`\`

### 3. Include Visual Context

**Use Mermaid for flows**:
## User Authentication Flow

\`\`\`mermaid
sequenceDiagram
    User->>Frontend: Enter credentials
    Frontend->>API: POST /login
    API->>DB: Verify credentials
    DB-->>API: User found
    API->>API: Generate JWT
    API-->>Frontend: Return token
    Frontend->>Frontend: Store token
    Frontend-->>User: Redirect to dashboard
\`\`\`

### 4. Prioritize Features

**Use MoSCoW method**:
- **Must Have** - MVP, can't launch without
- **Should Have** - Important but not critical
- **Could Have** - Nice to have
- **Won't Have** - Out of scope

**Example**:
## Feature Priority

| Feature | Priority | Reason |
|---------|----------|--------|
| Email/password login | Must Have | Core functionality |
| OAuth (Google) | Should Have | Reduces friction |
| 2FA | Could Have | Security enhancement |
| Biometric login | Won't Have | V1 scope |

### 5. Define Success Metrics

**Measurable criteria**:
## Success Metrics

**Performance**:
- Page load < 2s (p95)
- API response < 500ms (p95)
- 99.9% uptime

**User Experience**:
- Login success rate > 95%
- Account lockout rate < 1%
- Password reset completion > 80%

---

## Converting from Word/Google Docs

### Step 1: Export to Markdown

**Tools**:
- **Pandoc** (Recommended): `pandoc PRD.docx -o PRD.md`
- **Word Online**: Save as → Plain Text → manual cleanup
- **Google Docs**: Add-on "Docs to Markdown"

### Step 2: Clean Up Formatting

**Common fixes**:
```bash
# Remove extra blank lines
sed -i '' '/^$/N;/^\n$/D' PRD.md

# Fix heading levels (Word often uses wrong levels)
# Manually adjust # levels in editor

# Convert tables to Markdown
# Use online tool: https://www.tablesgenerator.com/markdown_tables
```

### Step 3: Add AI-Friendly Enhancements

**Enhance converted PRD**:
1. Add code blocks for technical specs
2. Convert flow diagrams to Mermaid
3. Add explicit edge cases section
4. Structure into numbered sections

**Before (Word)**:
```
Login Feature: User logs in with credentials. Handle errors properly.
```

**After (Markdown)**:
## 2.1 Login Feature

**User Story**: As a user, I want to log in securely so I can access my account.

**Requirements**:
1. Support email + password authentication
2. Validate input format before submission
3. Show specific error messages (see table below)
4. Lock account after 5 failed attempts

**Error Handling**:
| Scenario | Error Message | HTTP Code |
|----------|---------------|-----------|
| Invalid email format | "Please enter a valid email" | 400 |
| Wrong password | "Invalid credentials" | 401 |
| Account locked | "Too many attempts. Try again in 15 minutes" | 429 |

---

## Integration with AGENTS.md

**Reference PRD in AGENTS.md**:

## Project Overview

[Your project description]

**📋 Product Requirements**: See [docs/PRD.md](./docs/PRD.md) for complete specification.

**Key Features** (from PRD):
- Authentication system with OAuth support
- Real-time collaboration features
- Advanced search with filters

**Current Phase**: Phase 1 - MVP (see PRD Section 5)

**This ensures AI reads PRD at session start.**

---

## Best Practices

### ✅ Do's

1. **Keep PRD updated** - Treat as living document
2. **Version in git** - Track changes, reviewable
3. **Link from AGENTS.md** - Make discoverable
4. **Use examples** - Show, don't just tell
5. **Include edge cases** - AI needs to handle errors
6. **Add diagrams** - Visual > text for flows
7. **Define data schemas** - Explicit structure
8. **Set priorities** - Must/Should/Could/Won't

### ❌ Don'ts

1. **Don't be vague** - "User-friendly UI" means nothing to AI
2. **Don't skip edge cases** - AI won't infer them
3. **Don't mix concerns** - PRD = requirements, not implementation
4. **Don't leave TODOs** - Complete sections or mark "TBD with rationale"
5. **Don't copy-paste without context** - Standalone document
6. **Don't use proprietary formats** - Markdown only
7. **Don't forget to link** - PRD is useless if AI doesn't know it exists

---

## Real-World Example

See example PRD for a task management app:
- [Example PRD](./../examples/PRD_EXAMPLE.md) (if available)

---

## Checklist: PRD Quality

Before committing your PRD:

- [ ] All features have priorities (Must/Should/Could/Won't)
- [ ] Edge cases explicitly documented
- [ ] API contracts defined (request/response)
- [ ] User flows visualized (Mermaid diagrams)
- [ ] Success metrics specified
- [ ] Referenced from AGENTS.md
- [ ] No Word/PDF artifacts (pure Markdown)
- [ ] Code blocks use proper syntax highlighting
- [ ] Tables formatted correctly
- [ ] Linked from project README (optional)

---

## Additional Resources

- [PRD Template](./templates/PRD_TEMPLATE.md) - Copy and customize
- [AGENTS.md Guide](./../../AGENTS.md) - How AI reads your docs
- [Documentation Guidelines](./DOCUMENTATION_GUIDELINES.md) - File organization
- [Mermaid Documentation](https://mermaid.js.org/) - For diagrams

---

**Questions?** Open an issue or see [CONTRIBUTING.md](./../../CONTRIBUTING.md)
