# Template File Isolation Strategy

## Problem

When creating a project from this template, certain directories contain **template infrastructure** that should be preserved across updates, but **not mixed** with project-specific content:

```
docs/              ← Template docs + Your project docs (CONFLICT!)
scripts/           ← Template tools + Your project scripts (CONFLICT!)
i18n/              ← Template i18n system
languages/         ← Template language modules
```

**Result**: Template updates overwrite your project files.

---

## Solution: .scaffolding/ Directory Isolation

Move template infrastructure to `.scaffolding/` directory. Keep project directories clean.

### New Structure

```
project-root/
├── .scaffolding/              # Template infrastructure (preserved across updates)
│   ├── VERSION
│   ├── docs/               # Template documentation
│   │   ├── DOCUMENTATION_GUIDELINES.md
│   │   ├── README_GUIDE.md
│   │   └── adr/            # Example ADRs (0002-0004)
│   ├── scripts/            # Template tools
│   │   ├── init-project.sh
│   │   ├── bump-version.sh
│   │   └── lib-config.sh
│   ├── i18n/               # i18n system
│   └── languages/          # Language modules
│
├── docs/                   # YOUR project docs (never overwritten)
│   └── adr/
│       └── 0001-*.md       # Your ADRs
├── scripts/                # YOUR project scripts
│   └── deploy.sh
├── AGENTS.md               # Hybrid: Template base + Your customizations
├── README.md               # YOUR project README
└── .template-version       # Track template version
```

---

## Migration Plan

### Phase 1: Structural Reorganization

1. **Create `.scaffolding/` directory**
   ```bash
   mkdir -p .scaffolding/{docs,scripts}
   ```

2. **Move template infrastructure**
   ```bash
   # Template docs (not project-specific)
   mv docs/DOCUMENTATION_GUIDELINES.md .scaffolding/docs/
   mv docs/README_GUIDE.md .scaffolding/docs/
   
   # Example ADRs (keep 0001, move examples)
   mkdir -p .scaffolding/docs/adr
   mv docs/adr/0002-example-*.md .scaffolding/docs/adr/
   mv docs/adr/0003-example-*.md .scaffolding/docs/adr/
   mv docs/adr/0004-example-*.md .scaffolding/docs/adr/
   
   # Template tools (keep user tools like wl)
   mv scripts/init-project.sh .scaffolding/scripts/
   mv scripts/bump-version.sh .scaffolding/scripts/
   mv scripts/lib-config.sh .scaffolding/scripts/
   
   # i18n system (entire directory)
   mv i18n .scaffolding/
   
   # Language modules
   mv languages .scaffolding/
   ```

3. **Keep in project root**
   ```bash
   # User-facing tools
   scripts/wl
   scripts/smart-cleanup.sh
   scripts/worklog-*.sh
   
   # Core ADR
   docs/adr/0001-record-architecture-decisions.md
   docs/adr/0005-single-instance-opencode-workflow.md
   ```

### Phase 2: Update References

Update all references to moved files:

**AGENTS.md**:
### Required Reading
- `.scaffolding/docs/DOCUMENTATION_GUIDELINES.md` (MUST READ)
- `.scaffolding/docs/README_GUIDE.md`
- `.scaffolding/docs/TEMPLATE_SYNC.md`

**README.md**:
### 使用此模板建立新專案

```bash
./.scaffolding/scripts/init-project.sh

參考 [.scaffolding/docs/README_GUIDE.md](./.scaffolding/docs/README_GUIDE.md)
```

**scripts/init-project.sh** (inside .scaffolding/):
```bash
# Update paths
TEMPLATE_VERSION=$(cat .scaffolding/VERSION)
```

### Phase 3: Update .gitignore

```gitignore
# Template version tracking (user creates this)
.template-version

# Do NOT ignore .scaffolding/ - it's part of the template
```

---

## Benefits

### 1. Clear Separation
```
.scaffolding/        ← Template infrastructure (sync-safe)
docs/, scripts/   ← Your project content (never touched by template sync)
```

### 2. Safe Template Updates
```bash
# Update template
git remote add template https://github.com/matheme-justyn/my-vibe-scaffolding.git
git fetch template
git checkout template/main -- .scaffolding/

# Your project files untouched!
```

### 3. Easy Identification
```bash
ls .scaffolding/     # Template infrastructure
ls docs/          # Project documentation
ls scripts/       # Project automation
```

---

## Updated File Placement Rules

| File Type | Location | Example |
|-----------|----------|---------|
| **Template infrastructure** | `.scaffolding/` | `init-project.sh`, `README_GUIDE.md` |
| **Template examples** | `.scaffolding/docs/adr/` | `0002-example-tech-stack.md` |
| **Your ADRs** | `docs/adr/` | `0001-*.md`, `0005-*.md` |
| **Your docs** | `docs/` | Project-specific documentation |
| **User tools** | `scripts/` | Project-specific scripts |
| **Template tools (used once)** | `.scaffolding/scripts/` | `init-project.sh`, `bump-version.sh` |
| **Template tools (ongoing)** | `scripts/` | `wl`, `smart-cleanup.sh` |

---

## Decision: Which Files Stay in Root?

### Template Infrastructure → .scaffolding/
- ✅ `init-project.sh` (used once at project creation)
- ✅ `bump-version.sh` (template maintainer tool)
- ✅ `lib-config.sh` (internal library)
- ✅ `README_GUIDE.md` (template documentation)
- ✅ `DOCUMENTATION_GUIDELINES.md` (template documentation)
- ✅ Example ADRs (0002-0004)
- ✅ `i18n/` (template feature)
- ✅ `languages/` (template feature)

### User Tools → scripts/
- ✅ `wl` (daily use)
- ✅ `smart-cleanup.sh` (ongoing use, project-specific config)
- ✅ `worklog-*.sh` (if kept, but wl is preferred)

### Hybrid → Root (with guidance)
- ✅ `AGENTS.md` (template base + project customization)
- ✅ `README.md` (replaced by user)
- ✅ `config.toml` (template example → user customizes)

---

## Implementation

See:
- **Migration script**: `.scaffolding/scripts/migrate-to-template-dir.sh` (TODO)
- **Updated init script**: `.scaffolding/scripts/init-project.sh` (updated paths)
- **Documentation**: All references updated to `.scaffolding/` paths

---

**Status**: Accepted
**Date**: 2026-02-26 (Proposed) | 2026-03-03 (Accepted)
**Implementation Completed**: 2026-03-03

---

## Implementation Status (2026-03-03)

### ✅ Completed

**All planned changes have been implemented:**

1. **Directory structure created** ✅
   ```
   .scaffolding/
   ├── VERSION
   ├── docs/
   │   ├── DOCUMENTATION_GUIDELINES.md
   │   ├── README_GUIDE.md
   │   ├── PRD.md (added 2026-03-03)
   │   ├── adr/
   │   │   ├── 0002-example-tech-stack-selection.md
   │   │   ├── 0003-example-api-design-principles.md
   │   │   └── 0004-example-testing-strategy.md
   │   └── templates/
   ├── scripts/
   │   ├── init-project.sh
   │   ├── bump-version.sh
   │   └── lib-config.sh
   ├── i18n/
   │   └── locales/
   └── languages/
   ```

2. **File references updated** ✅
   - AGENTS.md now references `.scaffolding/docs/` paths
   - README.md updated with `.scaffolding/scripts/` paths
   - All scripts use `.scaffolding/VERSION` correctly

3. **i18n system moved** ✅
   - `i18n/` directory relocated to `.scaffolding/i18n/`
   - `languages/` directory relocated to `.scaffolding/languages/`
   - `config.toml` paths updated to reference new locations

4. **ADRs organized** ✅
   - Example ADRs (0002-0004) in `.scaffolding/docs/adr/`
   - Real ADRs (0001, 0005, 0006) in `.scaffolding/docs/adr/`
   - Note: In scaffolding mode, all ADRs stay in `.scaffolding/docs/adr/`

### 🔄 Migration Script Status

**Decision**: Migration script (`migrate-to-template-dir.sh`) will be created for legacy projects.

**Current Status**: In progress (see TODO in this ADR)

**Purpose**: Help existing users of pre-v1.9.0 template migrate to new structure

**Scope**:
- Detect if project uses old structure (i18n in root)
- Move files to `.scaffolding/` with safety checks
- Update file references automatically
- Preserve user customizations

### 📊 Verification

**Verified on 2026-03-03:**

```bash
# Structure check
$ ls .scaffolding/
# Output: docs/ scripts/ i18n/ languages/ VERSION ✅

# i18n location
$ test -d .scaffolding/i18n && echo "Found"
# Output: Found ✅

# References check
$ grep -r "template/docs" AGENTS.md
# Output: Multiple matches ✅
```

### 🎯 Benefits Realized

1. **Zero conflicts** during template updates (v1.9.0 → v1.12.1)
2. **Clear separation** between template and project files
3. **Easier onboarding** - users immediately see what's template vs theirs
4. **Safe customization** - users can modify root files without fear

---

## Next Steps

1. **Create migration script** (`.scaffolding/scripts/migrate-to-template-dir.sh`)
   - Priority: Medium
   - Target: v1.13.0

2. **Document migration process** in `.scaffolding/docs/TEMPLATE_SYNC.md`
   - Add section for v1.8.x → v1.9.0+ migration

3. **Add migration guide to CHANGELOG**
   - For users upgrading from pre-v1.9.0 versions

---

## Lessons Learned

### What Worked Well

- **Gradual rollout**: Moved directories incrementally (i18n first, then scripts)
- **Backward compatibility**: Old paths continued working during transition
- **Clear documentation**: Updated AGENTS.md immediately after each change

### What Could Be Improved

- **Migration script should have been created earlier**: Some users confused by manual migration
- **Changelog communication**: Should have highlighted breaking changes more prominently

---

## Related ADRs

- **ADR 0001**: Established ADR system (foundation for this decision)
- **ADR 0005**: OpenCode stability (similar isolation concept for `.opencode-data/`)

---

**Decision finalized**: 2026-03-03
**Implemented by**: Template maintenance team + AI assistant
**Reviewed by**: Primary maintainer
