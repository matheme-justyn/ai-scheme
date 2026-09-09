# Why your project has two config files

A project that uses both layers ends up with two configuration files. This is
deliberate, decided on 2026-09-08 and recorded in `ai-scheme` ADR 0008 and
`ai-zpd` ADR 0015.

| File | Layer | Format | What it configures |
| --- | --- | --- | --- |
| `.scheme/config.yml` | Skeleton (`ai-scheme`) | YAML | Repository shape and conventions: project identity, language profiles, branching, README strategy, governance phase, collaboration mode, visibility, optional features |
| `config.toml` | Mechanism (`ai-zpd`) | TOML | How capabilities are loaded and run: module selection, OpenCode settings, service capabilities and fallbacks |

## The rules

**Neither file reads the other.** `ai-scheme`'s CLI and scripts never parse
`config.toml`; `ai-zpd`'s never parse `.scheme/config.yml`.

**Same-named keys are independent.** There is no fallback from one to the
other. If a key exists in both, they mean different things and both values
stand.

This is why the two layers avoid names that look alike. The rule came from a
real collision: the mechanism layer used to have `[project].type`, meaning
"which domain modules to load" -- close enough to a skeleton-layer
`project_type` to be read as the same thing, and different enough to be wrong.
That layer has since moved the module selectors into `[modules]` and renamed
the key to `domain`, so the collision no longer exists on that side. The
constraint stays anyway: this layer expresses technology choice as `languages`
and never as `project_type`. A name that was confusing once is cheap to keep
avoiding, and the next near-collision will not announce itself.

**Detection is not reading.** `ai-scheme status` and `ai-scheme adopt` report
that a mechanism-layer config file is present, because a user should be told
what is in their project. They do not open it, and its contents never change a
state judgement.

**Uninstalling one does not touch the other.** See [uninstall.md](./uninstall.md).

## Which file do I edit?

Ask what you are changing.

- Changing what the *repository* is like -- its name, languages, branching,
  release phase, whether it publishes a decision site -- edit
  `.scheme/config.yml`, then run `ai-scheme config validate`.
- Changing what the *agent tooling* does -- which modules load, how OpenCode
  behaves, which services are available -- edit `config.toml`.

If you are unsure, `ai-scheme config get <key>` tells you whether this layer
owns a key: it exits 2 with `no such key` when it does not.

## Why not one file

Three options were on the table: unify the format and keep separate paths,
merge into a single file with per-layer sections, or keep two files and write
the boundary down. The third won because Copier writes its answers file as YAML
natively -- a single merged file would mean one of the two layers maintaining a
conversion layer, and both layers writing to the same file during `update`,
where conflict handling is already the hardest part. The cost is that you see
two files; this page is that cost being paid.

## Migration from `config.toml.example`

The old `config.toml.example` in this repository was a first-pass slice from
`my-vibe-scaffolding` and has been removed. Where each section went:

| Old section | Now |
| --- | --- |
| `[i18n].primary_locale` | Question `readme_primary_language` |
| `[i18n].fallback_locale` | Removed -- always `en-US`, not a choice |
| `[i18n].commit_locales` | Question `commit_locales` |
| `[i18n.translation]` | Removed -- a translation working mode, not project configuration. Revisit if a translation command ships |
| `[i18n.readme].strategy` | Question `readme_strategy` |
| `[languages].primary` | Question `languages` |
| `[languages].auto_merge_gitignore` | Removed -- superseded by the `merge` kind in `ownership.yml`, which makes it unconditional and non-destructive |
| `[academic].citation_style` | Question `citation_style`, asked only when `enable_academic_docs` |
| `[academic].field` | Question `academic_field`, same condition |
| `[academic].primary_language` / `.secondary_language` | Removed -- duplicated the README language settings |
| `[github].use_pr_template` | Question `enable_pr_template` |
| `[terminology].priority` | Removed -- a resolution rule, not a preference. Project terms beat domain terms beat common terms, and that ordering is not configurable |
| `[terminology]` sources | Derived from `enable_terminology` and `terminology_domains` |

Nothing in the old file turned out to belong to another repository, so no
sections were handed back to `ai-zpd` or `ai-skill-web`.
