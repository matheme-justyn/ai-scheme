# ADR 0001: Record architecture decisions

**Status**: Accepted
**Date**: 2026-02-25
**Issue**: seeded by the ai-scheme template
**PR**: seeded by the ai-scheme template
**Tags**: process, documentation

## Context

Decisions that shape a codebase get made in conversations, pull request
comments and chat threads. Those are not searchable six months later, and the
reasoning is what future readers need -- not the conclusion, which they can
read off the code.

Without a record, a decision gets re-litigated whenever somebody new arrives,
and reversed by accident whenever nobody remembers why it was made.

## Decision

Record architecture decisions here, one file per decision, `NNNN-slug.md`,
following the format in [README.md](./README.md).

## Alternatives considered

| Option | Why not |
| --- | --- |
| A wiki page | Drifts from the code it describes, and is not reviewed with it. |
| Commit messages only | Real, but not findable: nobody greps history for "why". |
| Nothing | The default, and the reason this record exists. |

## Reconsider when

Records stop being written, which usually means they are being written
somewhere else -- find where, and move this there.

## Consequences

- A decision has one place to live, reviewed in the same pull request as the
  change it justifies.
- Superseded records stay, so the reasoning survives the decision.
- Somebody has to write them. A record nobody writes protects nothing.
