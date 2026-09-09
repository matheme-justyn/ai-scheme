<div align="center">

# ai-scheme

[![License](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

English | [繁體中文](./README.zh-TW.md)

</div>

---

## What is This?

**The repo/CI skeleton layer** — one governed structure, applied consistently across many generated projects, using [Copier](https://copier.readthedocs.io/) to keep them in sync over time.

This repo is being split out of [my-vibe-scaffolding](https://github.com/matheme-justyn/my-vibe-scaffolding), which is itself becoming [`ai-zpd`](https://github.com/matheme-justyn/ai-zpd) (the capability-mechanism layer). `ai-scheme` takes over the parts of the old repo concerned with project skeleton, CI/CD conventions, and Copier-based template propagation.

## Why "Scheme"

Named after Jean Piaget's **schème** — not the more commonly translated "schema."

Piaget distinguished two French words that English collapses into one: *schéma* (a static, figurative representation) and **schème** (an action-based cognitive structure — "a nucleus or skeleton of know-how," a repeatable pattern of action that generalizes across many situations). It's the second one this repo is named for: a template is a reusable procedural skeleton, not a static picture.

The English spelling drops the accent for practical reasons — the properly-accented "schème" isn't ASCII-friendly for a repo slug. This does mean the name reads the same as the *Scheme* programming language (a Lisp dialect); that collision was considered and accepted as low-risk.

## The Occupation: Punchcutter

Every name in this project family pairs a psychologist's term with a vanished occupation that embodies it. This one is the **punchcutter**.

Before a single piece of movable type could be cast, someone had to hand-carve every letterform into a small steel billet — the *punch*. That punch was then struck into softer metal to make a *matrix*, and the matrix is what actually cast the unlimited, identical pieces of type a printer used. Cutting a single punch could take a skilled craftsman an entire day; it was, by most accounts, the hardest job in the whole production chain. The trade is effectively extinct today — a handful of practitioners remain worldwide.

It's a master pattern that strikes another master pattern, which then casts endless faithful copies — a template of templates, not a single reproduced object. That layered structure is closer to what `ai-scheme` actually is than a simpler "one craftsman, many identical outputs" trade would be: a repo template isn't the generated repos themselves, it's the punch that makes the matrix that makes them possible.

## Using it

Every lifecycle command is a dry run first: it writes a plan, and only
`--apply-plan` touches your project.

```bash
# Where does this project stand, and what should run next?
uvx --from git+https://github.com/matheme-justyn/ai-scheme@v0.1.0 ai-scheme status --json

# Bring an existing project under the skeleton
uvx --from git+https://github.com/matheme-justyn/ai-scheme@v0.1.0 ai-scheme adopt --tag v0.1.0
```

Always pin the tag. The tag is resolved to the full commit it points at and
recorded in `.scheme/provenance.json`, so a later update can tell you what
changed instead of trusting a name that somebody can move. `--allow-unreleased`
exists for working on the template itself and marks the run as `development`.

The first release has not been published yet, so the commands above name a tag
that does not exist. Until it does, run the CLI from a checkout.

## Status

The skeleton, the lifecycle commands (`status`, `create`, `adopt`, `update`),
the verification entry point and the issue, pull request and milestone
contracts are in place. Release automation, repository settings as code, the
language profiles and the decision site are not — see the open issues.

## License

MIT License — see [LICENSE](./LICENSE)
