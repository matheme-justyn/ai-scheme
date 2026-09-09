# The pull request lease carrier

Worktrees isolate files. They do not isolate the pull request control plane:
ready/draft, labels, milestone and merge live on GitHub, shared by every
session working on the same pull request. Two sessions writing at once race,
and the loser's change disappears without an error.

This document is the carrier's contract. What must hold a lease, and what an
agent does when it cannot get one, is the protocol -- that belongs to the
mechanism layer, and this document is what it is written against.

## The namespace

    refs/leases/pr/<n>          one pull request
    refs/leases/lane/<branch>   one destination branch

The ref points at a blob holding the lease as JSON. These names are a contract:
changing them is a change to the other layer, announced first.

## What a lease holds

| Field | Meaning |
| --- | --- |
| `pr` / `lane` | What it binds. Exactly one is set |
| `base` | Destination branch |
| `head` | The full 40-character head SHA this work is against |
| `expires_at` | Unix seconds. After this the lease may be reclaimed |
| `capability` | A random token. Whoever holds it holds the lease |
| `holder` | A label for the report. Not a credential |

`inspect` prints everything except `capability`.

## The four primitives

    scripts/lease.py acquire --pr <n> --base <branch> --head <sha> --ttl <seconds>
    scripts/lease.py renew   --pr <n> --capability <token> --head <sha>
    scripts/lease.py release --pr <n> --capability <token>
    scripts/lease.py inspect --pr <n>

Four commands rather than one with flags, because they fail differently:
`acquire` fails when somebody else holds it, `renew` when the capability is
wrong or the head moved, `release` almost never, and `inspect` is read-only and
open to anyone.

Add `--remote origin` to operate on the shared ref rather than the local one.
Local refs only serialise sessions on the same machine.

## Atomicity

Every write is a compare-and-swap: `git update-ref <ref> <new> <old>` locally,
`git push --force-with-lease=<ref>:<old>` against a remote. Git decides who
wins, not this code. Two sessions taking the same free lease at the same time
produce exactly one winner and one refusal.

## Expiry and reclaiming

A lease may be reclaimed **only** when it is provably expired, and reclaiming
is itself a compare-and-swap against the expired value -- so two sessions
seeing the same expired lease still produce one winner. There is no `--force`.

## When the head moves

A lease is taken against a specific head SHA. `renew` requires the caller to
state the head it believes it is working on, and refuses when that disagrees
with the lease. The work the lease covers is not the work that is there now:
release it and take a new one.

The carrier never asks GitHub what the head is. The moment it did, it would
have pull request semantics, and this file would be the protocol instead of the
carrier. The caller supplies the head it is acting on.

## Exit codes

| Code | Meaning |
| --- | --- |
| 0 | Done |
| 1 | A definite no: held by somebody else, wrong capability, head moved |
| 2 | Could not answer: git failed, the ref holds something unreadable |

`1` is worth retrying after a wait. `2` is not.

## Writes that skip the lease

`scripts/lease.py scan` looks through `.github/workflows/` and `scripts/` for
writes to pull request state that do not go through a lease -- `gh pr merge`,
`gh pr ready`, a REST `PATCH` to `/pulls/`, a GraphQL mutation -- and fails
closed. It runs in the static verification stage.

Exceptions live in `policies/lease-exceptions.json` as exact paths, each with
the issue that tracks removing it. No globs: a glob stops being reviewable the
moment it matches something new.

The scanner ignores comments and text inside backticks. The previous POC's
version matched documentation describing the rule it enforced, and a check that
cries wolf gets switched off.
