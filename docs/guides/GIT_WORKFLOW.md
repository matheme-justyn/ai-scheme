# Git Workflow (Git 工作流程)

## 分支與 Issue 的關係 | Branches and issues

`main` 是唯一的永久分支。工作分支從 Issue 開出來，用原生的 Development 連結：

    gh issue develop <issue> --name <type>/<issue>-slug

`<type>` 是 `feat`、`fix`、`docs`、`refactor`、`test`、`chore` 其中之一，與 commit
與 PR 標題用同一組字。`branch_strategy = delivery` 的專案，一個 milestone 用一條
短命的 `dev/m<N>-slug` 收斂，結束就刪；其餘情況直接進 `main`。

## Pull request 契約 | The pull request contract

一份 PR 說清楚三件事：關掉哪張 Issue（`Closes #N`）、完成清單、補充。

- 清單沒勾完就維持 draft。draft 只驗標題與分支名；標成 ready 等於宣告「現在該
  過了」，此時才做完整檢查。這條規則來自先前 POC 的教訓：一張 PR 反覆推了幾十次，
  每推一次就重跑一輪 gate。
- `scripts/validate-pr-policy <pr>` 在本機與 CI 跑同一套規則：closing keyword 對應
  的 Issue 存在、雙方 checklist 全勾、label 與 milestone 一致、分支名格式、標題符合
  conventional 格式（`!` 表示 breaking）。
- `collaboration_mode = team` 另外要求有非作者的 review request；`solo` 不要求。

## 版本 | Versions

推送前不需要（也不應該）手動 bump 版本。版本由 release 流程依 PR 標題的 SemVer
意圖決定。`hooks/pre-push` 現在跑的是 `scripts/verify`，不是版本檢查。

**Version**: 2.0.0  
**Module**: GIT_WORKFLOW  
**Loading**: Always (Core module)  
**Purpose**: Git conventions, commit messages, branching strategies, and PR guidelines.

---

## Overview

This guide defines **Git workflow conventions** for consistent version control across all projects. It covers commit messages, branching strategies, pull requests, and release processes.

**Scope**:
- ✅ Commit message format
- ✅ Branching strategies
- ✅ Pull request guidelines
- ✅ Version management
- ✅ Git hooks

**Loading Trigger**: Always loaded (Core module), keywords: "git", "commit", "branch", "merge"

---

## Core Principles

### 1. Commits Tell a Story

**Every commit should be atomic and meaningful.**

✅ **Good** (atomic commits):
```bash
git commit -m "feat: add user authentication endpoint"
git commit -m "test: add authentication integration tests"
git commit -m "docs: update API documentation for auth"
```

❌ **Bad** (bundled changes):
```bash
git commit -m "add auth, fix bugs, update docs"
```

### 2. Main Branch is Sacred

**`main` branch must always be deployable.**

- ✅ All commits pass tests
- ✅ No broken features
- ✅ Version bumped before push
- ❌ Never force push to `main`

### 3. Version Comes From the Release, Not From You

A push does not need a version bump. The release flow reads the SemVer intent
from the pull request title and produces the version, so there is one place
that decides and no hook blocking a push for the wrong reason.

## Commit Message Format

### Standard Format

**Rule**: Use Conventional Commits format.

```
type: brief description

[optional body]

[optional footer]
```

**Example**:
```
feat: add user login with JWT authentication

Implements JWT token-based authentication with refresh tokens.
Session expires after 30 minutes of inactivity.

Closes #42
```

### Commit Types

| Type | Purpose | Examples |
|------|---------|----------|
| `feat` | New feature | `feat: add password reset functionality` |
| `fix` | Bug fix | `fix: resolve memory leak in WebSocket connection` |
| `docs` | Documentation only | `docs: update README with setup instructions` |
| `style` | Code style (formatting, missing semicolons) | `style: format code with Prettier` |
| `refactor` | Code refactoring (no behavior change) | `refactor: extract validation into separate module` |
| `test` | Adding/updating tests | `test: add unit tests for user service` |
| `chore` | Maintenance (dependencies, scripts) | `chore: update dependencies` |
| `perf` | Performance improvement | `perf: optimize database query` |
| `ci` | CI/CD changes | `ci: add GitHub Actions workflow` |
| `build` | Build system changes | `build: update webpack config` |
| `revert` | Revert previous commit | `revert: revert "feat: add feature X"` |

### Commit Message Rules

**1. Subject Line** (first line):
- ✅ Max 50 characters
- ✅ Start with lowercase
- ✅ No period at end
- ✅ Imperative mood ("add" not "added")

**2. Body** (optional):
- ✅ Wrap at 72 characters
- ✅ Explain WHAT and WHY
- ✅ Separate from subject with blank line

**3. Footer** (optional):
- ✅ Reference issues: `Closes #123`, `Fixes #456`
- ✅ Breaking changes: `BREAKING CHANGE: API endpoint renamed`

**Examples**:

✅ **Good**:
```
feat: add user authentication

Implements JWT-based authentication with the following features:
- Login/logout endpoints
- Refresh token rotation
- Session management with Redis

Closes #42
```

❌ **Bad**:
```
Added authentication.  # Wrong tense, capitalized, period
```

---

## Branching Strategy

### Strategy Selection

**Choose based on team size and project maturity:**

| Strategy | Team Size | Complexity | Use Case |
|----------|-----------|------------|----------|
| **Trunk-Based** | 1-3 | Low-Medium | Template development, small teams |
| **Feature Branch** | 3-10 | Medium | Most projects |
| **Git Flow** | 10+ | High | Enterprise, regulated environments |

### Trunk-Based Development (Recommended for Template)

**Structure**: Direct commits to `main` (or very short-lived branches).

```
main: ─●─●─●─●─●─●─●→
       │ │ │ │ │ │ │
       1 2 3 4 5 6 7
```

**Rules**:
- ✅ Commit directly to `main` (if confident)
- ✅ Short-lived feature branches (< 1 day)
- ✅ Small, frequent commits
- ✅ Version bump on EVERY push
- ✅ Tests run on EVERY commit

**When to Use**:
- Single developer (template maintainer)
- Rapid iteration
- CI/CD pipeline robust

**Pre-push Hook Enforcement**:
```bash
# .git/hooks/pre-push
# Blocks push if VERSION unchanged
```

### Feature Branch Workflow

**Structure**: One branch per feature/fix.

```
main:    ─●───────●───────●→
          │       │       │
feature: ─●─●─●─●─┘       │
                  └─●─●─●─┘
                   hotfix
```

**Branch Naming**:
```
feature/user-authentication
fix/memory-leak-websocket
docs/update-readme
chore/update-dependencies
```

**Rules**:
- ✅ Branch from `main`
- ✅ Descriptive branch names
- ✅ Merge via Pull Request
- ✅ Delete branch after merge
- ✅ Keep branches up-to-date with `main`

**Example Workflow**:
```bash
# Create feature branch
git checkout -b feature/user-auth

# Make commits
git commit -m "feat: add login endpoint"
git commit -m "test: add auth integration tests"

# Update from main
git checkout main
git pull origin main
git checkout feature/user-auth
git rebase main  # or git merge main

# Push and create PR
git push origin feature/user-auth
gh pr create --title "feat(auth): add user authentication"
```

### Git Flow (Advanced)

**Structure**: Multiple long-lived branches.

```
main:     ─●───────●───────●→ (production)
          │       │       │
develop: ─●─●─●─●─●─●─●─●─●→ (integration)
            │   │ │   │
feature:    ●─●─┘ │   │
                  ●─●─┘
```

**Branches**:
- `main`: Production-ready code
- `develop`: Integration branch
- `feature/*`: New features
- `hotfix/*`: Emergency fixes
- `release/*`: Release preparation

**When to Use**:
- Large teams (10+)
- Scheduled releases
- Strict QA process

**Not recommended for**:
- Template development (too complex)
- Small teams (overhead too high)

---

## Merge Strategies

### Merge Commit (Default)

**Command**: `git merge --no-ff`

**Result**:
```
main:    ─●───────●→
          │       │
feature: ─●─●─●─●─┘
```

**Pros**:
- ✅ Preserves full history
- ✅ Easy to revert entire feature

**Cons**:
- ❌ Cluttered history

### Squash Merge

**Command**: `git merge --squash`

**Result**:
```
main:    ─●───────●→
          │       
feature: ─●─●─●─●
```

**Pros**:
- ✅ Clean linear history
- ✅ One commit per feature

**Cons**:
- ❌ Loses intermediate commits

### Rebase

**Command**: `git rebase main`

**Result**:
```
main:    ─●───────●─●─●─●─●→
          │           (rebased commits)
```

**Pros**:
- ✅ Linear history
- ✅ Preserves individual commits

**Cons**:
- ❌ Rewrites history (dangerous if shared)

**Recommendation**:
- **Template dev**: Squash merge (clean history)
- **Open-source**: Merge commit (preserve contributions)
- **Rebase**: Local branches only (before pushing)

---

## Pull Request (PR) Guidelines

### PR Title Format

**Rule**: Use Angular Conventional Commits style.

```
type(scope): brief description
```

**Examples**:
```
feat(auth): add JWT authentication
fix(api): resolve memory leak in user service
docs(readme): update installation guide
refactor(core): simplify error handling logic
```

**Types**: Same as commit types (feat, fix, docs, style, refactor, test, chore, perf, ci, build, revert)

### PR Description Template

**Use `.github/pull_request_template.md`** -- GitHub fills it in for you.

**Sections**:
1. `Closes #N`
2. 完成清單 / Checklist
3. 補充 / Notes
4. **Testing** (How tested)
5. **Screenshots** (If UI change)
6. **Breaking Changes** (If any)

**Example**:
```markdown
## Summary
Implement JWT-based user authentication

## Motivation
Replace session-based auth to support API-only clients

## Changes
- Add `/api/auth/login` endpoint
- Add `/api/auth/refresh` endpoint
- Implement JWT token generation
- Add Redis session store

## Testing
- ✅ Unit tests: 15 new tests
- ✅ Integration tests: 5 new scenarios
- ✅ Manual testing: Login flow verified

## Breaking Changes
⚠️  Old session cookies no longer supported. Clients must use Authorization header.
```

### PR Review Checklist

**Before requesting review**:
- [ ] All tests pass
- [ ] Code follows STYLE_GUIDE
- [ ] No debug logs (`console.log`, `print`)
- [ ] Documentation updated
- [ ] No security vulnerabilities

**Reviewer checks**:
- [ ] Code is readable and maintainable
- [ ] Tests cover edge cases
- [ ] No performance regressions
- [ ] API changes are backward-compatible (if not, flagged as breaking)

### PR Size Guidelines

**Rule**: Keep PRs small.

| Size | Lines Changed | Review Time | Recommendation |
|------|---------------|-------------|----------------|
| **XS** | < 50 | < 10 min | ✅ Ideal |
| **S** | 50-200 | 10-30 min | ✅ Good |
| **M** | 200-500 | 30-60 min | ⚠️  Consider splitting |
| **L** | 500-1000 | 1-2 hours | ❌ Split into multiple PRs |
| **XL** | > 1000 | > 2 hours | ❌ Must split |

**Exceptions**:
- Generated code (migrations, GraphQL schemas)
- Automated refactoring (rename tool)
- Documentation updates

---

## Version Management

### Semantic Versioning (SemVer)

**Format**: `MAJOR.MINOR.PATCH`

**Rules**:
- **PATCH** (1.0.0 → 1.0.1): Bug fixes, docs, no API change
- **MINOR** (1.0.0 → 1.1.0): New features, backward-compatible
- **MAJOR** (1.0.0 → 2.0.0): Breaking changes

**Examples**:

| Change | Old | New | Reason |
|--------|-----|-----|--------|
| Fix typo in docs | 1.5.0 | 1.5.1 | PATCH (no code change) |
| Add new optional parameter | 1.5.0 | 1.6.0 | MINOR (backward-compatible) |
| Remove deprecated function | 1.5.0 | 2.0.0 | MAJOR (breaking change) |

### Producing a Version

Versions are produced by the release flow from the pull request title:
`feat:` moves the minor, `fix:` the patch, a `!` marks a breaking change. There
is no `bump-version` script to run and no VERSION file to keep in step by hand.

### Pre-Push Hook

`hooks/pre-push` runs `scripts/verify` at the tier your change needs. Install
it with:

```bash
git config core.hooksPath hooks
```

It used to block pushes to `main` whose VERSION had not changed. That rule is
gone: it fired on changes that had no business bumping anything, and a hook
that is wrong often enough gets bypassed and then ignored.

## Git Hooks

### Available Hooks

| Hook | Purpose | Installed By |
|------|---------|--------------|
| **pre-commit** | Run linters, formatters | `git config core.hooksPath hooks` |
| **pre-push** | Run `scripts/verify` at the tier the change needs | `git config core.hooksPath hooks` |
| **commit-msg** | Validate commit message format | (Optional) |

### Pre-Commit Hook

**Runs**:
- Linters (ESLint, Pylint)
- Formatters (Prettier, Black)
- Type checks (TypeScript, mypy)

**Example** (`.git/hooks/pre-commit`):
```bash
#!/bin/bash
npm run lint || exit 1
npm run format || exit 1
npm run type-check || exit 1
```

### Pre-Push Hook

**Runs**: `scripts/verify`, which picks docs, fast or full from what changed.

**Shipped as** `hooks/pre-push`:
```bash
#!/usr/bin/env bash
set -euo pipefail
repo_root="$(git rev-parse --show-toplevel)"
[ -x "${repo_root}/scripts/verify" ] || exit 0
"${repo_root}/scripts/verify"
```

### Commit Message Hook (Optional)

**Validates**: Conventional Commits format.

**Example** (`.git/hooks/commit-msg`):
```bash
#!/bin/bash
COMMIT_MSG=$(cat "$1")
PATTERN="^(feat|fix|docs|style|refactor|test|chore|perf|ci|build|revert): .{1,50}$"

if ! echo "$COMMIT_MSG" | head -1 | grep -qE "$PATTERN"; then
  echo "❌ Invalid commit message format"
  echo "Expected: type: description"
  exit 1
fi
```

---

## Gitignore Best Practices

### Universal Patterns

**Always ignore**:
```gitignore
# Dependencies
node_modules/
venv/
__pycache__/

# Build outputs
dist/
build/
*.pyc
*.pyo

# Environment files
.env
.env.local
*.secret

# OS files
.DS_Store
Thumbs.db

# IDE files
.vscode/
.idea/
*.swp

# Logs
*.log
npm-debug.log*
```

### Project-Specific

**Add based on project type**:
```gitignore
# OpenCode (project-specific)
.opencode-data/

# Template tracking
.template-version

# User preferences
config.toml
```

**Commit to Git**:
```gitignore
# Template example
config.toml.example
```

---

## Tagging Strategy

### Tag Format

**Rule**: `vMAJOR.MINOR.PATCH`

**Examples**:
- `v1.0.0` - Initial release
- `v1.1.0` - Feature release
- `v2.0.0` - Major release

### Creating Tags

**Manual**:
```bash
git tag -a v1.2.0 -m "Release v1.2.0: Add user authentication"
git push origin v1.2.0
```

**Automated**: the release flow tags from the pull request's SemVer intent.
Nothing to run by hand.

### Tag Annotations

**Rule**: Include release notes in tag message.

**Example**:
```bash
git tag -a v1.2.0 -m "Release v1.2.0

Features:
- Add user authentication
- Add password reset

Bug fixes:
- Fix memory leak in WebSocket
"
```

---

## Conflict Resolution

### Prevention

**Rule**: Keep branches up-to-date.

```bash
# Update feature branch from main daily
git checkout main
git pull origin main
git checkout feature/my-feature
git rebase main  # or git merge main
```

### Resolution Steps

**When conflict occurs**:

1. **Identify conflicting files**:
   ```bash
   git status
   ```

2. **Open conflict markers**:
   ```
   <<<<<<< HEAD
   current code
   =======
   incoming code
   >>>>>>> feature/my-feature
   ```

3. **Resolve conflicts**:
   - Keep both changes (if compatible)
   - Choose one version
   - Rewrite to integrate both

4. **Mark as resolved**:
   ```bash
   git add <resolved-files>
   git rebase --continue  # or git merge --continue
   ```

5. **Verify**:
   ```bash
   npm test  # or pytest, etc.
   ```

### Aborting

**If resolution too complex**:
```bash
git rebase --abort  # or git merge --abort
# Ask for help or use different strategy
```

---

## Cherry-Picking

### Use Cases

**When to cherry-pick**:
- Urgent hotfix to `main`
- Backport fix to older version
- Move commit to different branch

**Example**:
```bash
# Find commit hash
git log --oneline

# Cherry-pick to current branch
git cherry-pick <commit-hash>
```

### Best Practices

- ✅ Cherry-pick single commits
- ✅ Include original author in commit message
- ❌ Don't cherry-pick merge commits
- ❌ Don't cherry-pick without understanding context

---

## Git Aliases (Recommended)

**Add to `~/.gitconfig`**:

```ini
[alias]
  # Status shortcuts
  st = status -s
  
  # Log shortcuts
  lg = log --oneline --graph --decorate --all
  last = log -1 HEAD
  
  # Branch shortcuts
  br = branch
  co = checkout
  cob = checkout -b
  
  # Commit shortcuts
  cm = commit -m
  ca = commit --amend
  
  # Rebase shortcuts
  rb = rebase
  rbi = rebase -i
  rbc = rebase --continue
  rba = rebase --abort
  
  # Diff shortcuts
  df = diff
  dfc = diff --cached
  
  # Undo shortcuts
  undo = reset HEAD~1 --mixed
  unstage = reset HEAD --
```

**Usage**:
```bash
git st           # Instead of git status -s
git lg           # Instead of git log --oneline --graph
git cob my-feat  # Instead of git checkout -b my-feat
```

---

## Emergency Procedures

### Accidentally Committed to Wrong Branch

```bash
# Reset current branch (keep changes)
git reset HEAD~1 --soft

# Switch to correct branch
git checkout correct-branch

# Commit there
git commit -m "your message"
```

### Accidentally Pushed to Main

```bash
# If push was recent and no one pulled yet...
git revert <commit-hash>  # Safer than force push
git push origin main

# If absolutely must force push (DANGEROUS)
git reset HEAD~1
git push --force origin main  # ⚠️  BREAKS OTHER DEVELOPERS
```

### Accidentally Deleted Branch

```bash
# Find lost commit
git reflog

# Recover branch
git checkout -b recovered-branch <commit-hash>
```

---

## Related Documentation

- **[STYLE_GUIDE](./STYLE_GUIDE.md)** - Code style conventions
- **[TERMINOLOGY](../terminology/)** - Git-related terms
- **[RELEASE_PROCESS](./RELEASE_PROCESS.md)** - Release procedures (when available)
- **[ADR_TEMPLATE](./ADR_TEMPLATE.md)** - Architecture decision records (when available)

---

## Quick Reference

### Daily Workflow

```bash
# Morning: Update from main
git checkout main
git pull origin main
git checkout -b feature/my-feature

# Work: Commit frequently
git add .
git commit -m "feat: add feature X"

# Evening: Push to remote
git push origin feature/my-feature

# Create PR
gh pr create --title "feat(scope): description"
```

### Before Pushing to Main

```bash
# 1. Ensure tests pass
npm test

# 2. Run the checks the change needs
scripts/verify

# 3. Push
git push origin main
```

---

**Maintained by**: the `ai-scheme` skeleton. Edit it there, not here --
`ai-scheme update` overwrites this file.
