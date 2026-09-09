# Releasing

Four separate things, each with one owner. Most of the confusion about
releases comes from treating them as one thing.

| | Question | Decided by |
| --- | --- | --- |
| Version intent | Is this a patch, a minor or a breaking change? | The pull request title: `fix:`, `feat:`, `!` |
| Version number | What is the next version? | release-please, from the intents merged since the last release |
| Release | Does this become a published version now? | A person, by merging the version pull request |
| Delivery | Where does it go? | Not this repository's business |

## Version intent

You declare it when you name the pull request. `fix:` moves the patch, `feat:`
the minor, and a `!` before the colon marks a breaking change. `docs:`,
`chore:`, `refactor:` and `test:` move nothing.

There is no version file to edit, no `bump-version` script, and no hook that
blocks a push because a number did not change. Those existed because the intent
lived in somebody's head; it lives in the title now.

## The version pull request

release-please watches `main` and keeps one pull request open that bumps
`.release-please-manifest.json` and writes the changelog entry. It rewrites
that pull request as more work merges. Nothing is published while it sits
there.

Merging it is the decision to release. That is the only manual step, and it is
manual on purpose.

## What a release contains

Merging the version pull request tags the commit and publishes a GitHub
release. `release.yml` then attaches:

- the source archive, built by `git archive` so it can be rebuilt;
- `SHA256SUMS` over everything attached;
- an SPDX SBOM from a pinned syft;
- a build provenance attestation.

Then it downloads what was published and re-hashes it. A release whose
artefacts nobody checked is a tag with a changelog attached.

## When the hosted run fails

`scripts/publish-release build --tag <tag> --out dist` produces the same
artefacts locally, and `scripts/publish-release verify --tag <tag>` runs the
same check against what is published. The fallback is the same command, not a
second procedure that drifts from the first.

## Drift

`scripts/check-release-drift` asks whether `main` has moved on without a
release for longer than a day. Commits without a release are normal. A release
workflow that has been failing quietly for a week is not, and this is the
question that surfaces it.

## Not here

Deployment, environments and rollout are not this repository's concern. It
publishes a version; what consumes it decides what to do with it.
