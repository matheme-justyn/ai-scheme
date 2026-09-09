# Uninstalling the skeleton

<!-- Generated from ownership.yml by `ai-scheme ownership sync`. Do not edit. -->

Removing `ai-scheme` from a project is a manual operation on purpose: some of
the paths below are shared with your own content, and no script should guess
which lines in them are yours. Work through the three groups in order.

## Safe to delete outright

The template put these here and nothing else did. Removing them removes the skeleton.

| Path | Kind | Detail |
| --- | --- | --- |
| `.github/ISSUE_TEMPLATE/` | template |  |
| `.github/PULL_REQUEST_TEMPLATE.md` | template |  |
| `.github/dependabot.yml` | template | Update groups per ecosystem, chosen from the languages answer. Minor and patch merge themselves once checks pass; a major waits for a person. |
| `.github/workflows/` | template |  |
| `.gitleaks.toml` | template | Secret scanning rules, so the same ones apply everywhere. |
| `.scheme/README.md` | template | Orientation for the answers file. Copier owns the header of config.yml itself, so the explanation of why a project can hold two configuration files lives beside it rather than inside it -- see ADR 0008. |
| `.scheme/config.yml` | template | Copier answers file. The single source of skeleton-layer settings. |
| `.scheme/provenance.json` | generated | Rebuilt from `the lifecycle command that applied the template`. Which release this project was applied from: tag, the full commit it resolved to, when, and by which CLI version. Rewritten on every apply. |
| `.vscode/` | template | Editor settings the skeleton keeps in step, plus their explanation. |
| `README.md` | generated | Rebuilt from `i18n/locales/<readme_primary_language>/readme.toml`. Regenerated from the i18n sources plus the answers file. Edit the sources, not the output. Additional language files follow readme_strategy. |
| `docs/README.md` | template | The documentation map: which of the four layers a thing belongs in, and what never belongs in the repository at all. |
| `docs/collaboration-modes.md` | template | What solo and team mode change, crossed with release_phase. |
| `docs/config-boundary.md` | template | Why a project sees both .scheme/config.yml and config.toml, and which layer owns which keys. |
| `docs/guides/` | template | Style, git workflow, documentation and writing guides. |
| `docs/lease-carrier.md` | template | The pull request lease contract the mechanism layer's protocol is written against: namespace, fields, atomicity, expiry, exit codes. |
| `docs/milestone-description.md` | template | When a milestone is worth creating, and what its description says. |
| `docs/status-interface-contract.md` | template | Defines how an agent calls this layer's lifecycle interface. Deliberately not named "install" -- see ADR 0007. |
| `docs/templates/` | template | Document templates a project fills in, such as the PRD skeleton. |
| `docs/terminology/` | template |  |
| `docs/uninstall.md` | generated | Rebuilt from `ownership.yml`. |
| `hooks/` | template |  |
| `i18n/` | template |  |
| `ownership.yml` | template | This file. |
| `policies/` | template | Declared policy the checks read -- link exceptions, and more to come. |
| `release-please-config.json` | template | How the version pull request is produced. Nobody edits a version by hand. |
| `schemas/` | template |  |
| `scripts/` | template | Lifecycle and verification entry points. |

## Remove only the template's part

These files are shared. Delete the delimited block or the contributed lines, not the file.

| Path | Kind | Detail |
| --- | --- | --- |
| `.gitignore` | merge | Language profile patterns are appended as a delimited section. Existing project entries are never removed. |
| `AGENTS.md` | managed-block | Block `ai-scheme:conventions`. The template owns the conventions block. Everything outside it is the project's, including any project-specific agent instructions. |

## Leave alone -- yours

Seeded once at creation and never touched again. Uninstalling the template does not reclaim them.

| Path | Kind | Detail |
| --- | --- | --- |
| `.release-please-manifest.json` | project | The current version. Owned by the project because release-please rewrites it on every release; the template seeds it and never touches it again. |
| `CHANGELOG.md` | project |  |
| `LICENSE` | project |  |
| `docs/adr/` | project | Decision records belong to the project. The template seeds ADR 0001 and the README, then never touches this directory again. |
| `docs/specs/` | project |  |
| `src/` | project |  |
| `tests/` | project |  |

## After removing the files

Delete `.scheme/config.yml` last. While it exists, `ai-scheme status` still
reports the project as adopted and will offer to update it.

`config.toml` at the repository root belongs to `ai-zpd`, not to this layer.
Uninstalling the skeleton does not touch it -- see ADR 0008.
