# VSCode Configuration Templates

This directory contains recommended VSCode configuration files.

## 📁 Files

### `settings.json.template`

**Purpose**: OpenCode project-isolated database configuration

**Problem it solves**:
- ❌ Multiple projects sharing `~/.local/share/opencode/opencode.db`
- ❌ Database conflicts when opening multiple projects simultaneously
- ❌ Session loss and data corruption

**Configuration**:
```json
{
  "opencode.dataDir": "${workspaceFolder}/.opencode-data",
  "opencode.logLevel": "info"
}
```

**Benefits**:
- ✅ Each project uses isolated `.opencode-data/` directory
- ✅ Safe to open multiple projects simultaneously
- ✅ Session history bound to project
- ✅ Controlled database size (< 10MB per project)

## 🚀 Usage

### Method 1: Automated Script (Recommended)

```bash
# Run from project root
./.scaffolding/scripts/init-opencode.sh
```

This automatically:
1. Copies `settings.json.template` → `.vscode/settings.json`
2. Adds `.opencode-data/` to `.gitignore`
3. Creates necessary directory structure

### Method 2: Manual Setup

```bash
# 1. Create .vscode directory
mkdir -p .vscode

# 2. Copy template
cp .scaffolding/vscode/settings.json.template .vscode/settings.json

# 3. Update .gitignore
echo ".opencode-data/" >> .gitignore

# 4. Restart VSCode
```

## 📖 Documentation

- [ADR 0005 - OpenCode Workflow](./../docs/adr/0005-single-instance-opencode-workflow.md)
- [OpenCode Setup Guide](./../docs/OPENCODE_SETUP_GUIDE.md)

## ⚠️ Important Notes

1. **Restart VSCode**: Changes to `.vscode/settings.json` require VSCode restart
2. **Don't commit `.opencode-data/`**: This is local data, should not be version controlled
3. **Apply to all projects**: Every project using OpenCode needs this configuration
4. **Old database cleanup**: After configuring, optionally clean up `~/.local/share/opencode/`

## 🔍 Verify Configuration

```bash
# After VSCode restart, should see new directory
ls -la .opencode-data/

# Should see project-isolated database (initially small)
ls -lh .opencode-data/opencode.db
```

## 🆘 Troubleshooting

### Q: Still using old database after configuration?

**A**: Ensure:
1. VSCode fully restarted (close all windows)
2. `.vscode/settings.json` syntax is correct (valid JSON)
3. No typos in file path

### Q: Want to restore old session history?

**A**: Can copy from old database (manual operation):
```bash
# Backup old database
cp ~/.local/share/opencode/opencode.db .opencode-data/opencode.db
```

### Q: Want to clean old shared database?

**A**: After all projects configured:
```bash
# Backup (recommended)
mkdir -p ~/opencode-backups
cp -r ~/.local/share/opencode ~/opencode-backups/opencode-$(date +%Y%m%d_%H%M%S)

# Clean (optional)
rm -rf ~/.local/share/opencode/opencode.db*
```
