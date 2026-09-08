# Git Workflow (Git 工作流程)

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

### 3. Version Bump on Every Push

**This template enforces version bumps via pre-push hook.**

**Why**: Direct main branch workflow (no dev branch) means every push is a "release". Without version bumps, `v1.2.0` before and after your change are different → confusion.

**Enforcement**: Pre-push git hook blocks pushes without version change.

---

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

**Use `.scaffolding/templates/pr/PULL_REQUEST_TEMPLATE.{lang}.md`**

**Sections**:
1. **Summary** (What changed)
2. **Motivation** (Why changed)
3. **Changes** (Detailed list)
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

### Version Bump Script

**Command**: `./.scaffolding/scripts/bump-version.sh <patch|minor|major>`

**What it does**:
1. Updates `.scaffolding/VERSION` and `VERSION`
2. Updates CHANGELOG.md
3. Updates README.md version badge
4. Creates git commit
5. Creates git tag

**Usage**:
```bash
# Bug fix
./.scaffolding/scripts/bump-version.sh patch

# New feature
./.scaffolding/scripts/bump-version.sh minor

# Breaking change
./.scaffolding/scripts/bump-version.sh major
```

### Pre-Push Hook

**Location**: `.git/hooks/pre-push`

**Purpose**: Enforce version bump before pushing to `main`.

**Behavior**:
```bash
# If pushing to main...
# And VERSION hasn't changed since last tag...
# Block the push with error message
```

**Install**:
```bash
./.scaffolding/scripts/install-hooks.sh
```

---

## Git Hooks

### Available Hooks

| Hook | Purpose | Installed By |
|------|---------|--------------|
| **pre-commit** | Run linters, formatters | `.scaffolding/scripts/install-hooks.sh` |
| **pre-push** | Enforce version bump | `.scaffolding/scripts/install-hooks.sh` |
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

**Enforces**: Version bump on `main` pushes.

**Example** (`.git/hooks/pre-push`):
```bash
#!/bin/bash
# Check if pushing to main
if [ "$(git branch --show-current)" = "main" ]; then
  # Get last tag
  LAST_TAG=$(git describe --tags --abbrev=0 2>/dev/null)
  CURRENT_VERSION=$(cat VERSION)
  
  if [ "$LAST_TAG" = "v$CURRENT_VERSION" ]; then
    echo "❌ VERSION unchanged. Run bump-version.sh first."
    exit 1
  fi
fi
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

**Automated** (via bump-version.sh):
```bash
./.scaffolding/scripts/bump-version.sh minor
# Creates tag automatically
```

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
- **[TERMINOLOGY](./terminology/)** - Git-related terms
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

# 2. Bump version
./.scaffolding/scripts/bump-version.sh patch

# 3. Push (hook will verify version)
git push origin main && git push --tags
```

---

**Version**: 2.0.0  
**Last Updated**: 2026-03-16  
**Maintainer**: my-vibe-scaffolding template
