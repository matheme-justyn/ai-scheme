# Repository instructions -- ai-scheme

Repository skeleton and CI conventions, applied and kept in sync across
generated projects.

This repository applies its own template: the block below is rendered from
`template/AGENTS.md.jinja`, and everything above it is ai-scheme's own. Split
out of the upstream scaffolding repository -- see ai-zpd for the install and
runtime mechanism, ai-skill-web for agent roles, skills and SDD.

<!-- BEGIN ai-scheme:conventions -->
<!-- Owned by ai-scheme. Edits inside this block are overwritten on update. -->

## Working loop

Before opening an issue, search open **and** closed issues with two to four
concrete words. If an existing decision applies, say in 補充 whether you are
following it, replacing it, or rejecting it, and why.

- Issues use the four forms in `.github/ISSUE_TEMPLATE/`: three fields, 問題 and
  完成條件 required. Titles: 12-80 ASCII characters, at least three words, no
  `[PREFIX]`, no full stop. `scripts/validate-issue-title "<title>"` checks one
  before it exists; `scripts/gh-issue-create` checks it and then creates it.
- A Feature is a shared outcome that is not finished yet; Tasks and Bugs hang
  under it as sub-issues. Use blocked-by only for a real ordering constraint.
- Branch from the issue: `gh issue develop <issue> --name type/<issue>-slug`.
- Before pushing, run `scripts/verify`. It picks docs, fast or full from what
  you changed; `scripts/verify --tier full` runs everything.

## Coding conventions

- **先寫測試** (test first): a new behaviour or a fixed bug arrives with the
  test that would have caught it.
- **型別標注** (typed): every function signature carries types.
- **簡單優先** (simplest thing): implement what is needed now.
- **可讀性** (readable): clear names, comments that say *why*.

Never: delete or skip a failing test; silence a type error with `as any`,
`@ts-ignore` or an unexplained `type: ignore`; commit secrets; refactor code
you were not asked to touch.

## Commit messages

English, `type: brief description`, where type is one of `feat`, `fix`, `docs`,
`refactor`, `test`, `chore`. The body explains why, when why is not obvious.

## Pull requests

Title in the same conventional form with a scope: `feat(auth): add JWT`. Body:
`Closes #N`, the completion checklist, and 補充. Keep the pull request a draft
until the checklist is complete -- a ready pull request means "the gate should
pass now".

## Documentation

Read `docs/guides/DOCUMENTATION_GUIDELINES.md` before creating a document, and
`docs/README.md` for which of the four layers a thing belongs in: specs say
what must be true, decision records say why, issues carry the work, tests check
the behaviour.

Decisions go to `docs/adr/`, specs to `docs/specs/`, guides to `docs/guides/`,
nothing to the root.

**Never commit a conversation.** No transcripts, no agent reasoning, no
inference that nobody has confirmed written as though it were established, and
no plan file that duplicates the issues. If something from a conversation is
worth keeping, rewrite it as a spec, a decision record or an issue, in the
repository's voice. `scripts/validate-docs` checks the shape of the first two.

Configuration lives in `.scheme/config.yml`; read it with
`ai-scheme config get <key>` rather than parsing it. If this project also uses
the mechanism layer, `config.toml` at the root belongs to that layer and this
one never reads it -- see `docs/config-boundary.md`.

<!-- END ai-scheme:conventions -->
