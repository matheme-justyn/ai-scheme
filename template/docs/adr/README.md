# Architecture decision records

One file per decision, `NNNN-slug.md`, numbered in the order they were made.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| `Proposed` | Written, not yet decided. |
| `Accepted` | In force. |
| `Superseded by ADR <n>` | Replaced by a later decision. |
| `Rejected` | Evaluated and decided against. |

## Flow forward, never delete

A superseded or rejected record keeps its full text. The value of the archive
is not the conclusion -- it is the reasoning that produced it, and the
alternatives that were already weighed. Delete the reasoning and the next
person evaluates the same options again, usually badly, usually under time
pressure.

When a decision changes, write a new record and mark the old one
`Superseded by ADR <n>`, saying in its header which part was replaced. Often it
is the implementation and not the problem statement.

## Every record carries

| Field | Why |
| --- | --- |
| **Status** | See above. |
| **Date** | When it was decided, not when the file was last touched. |
| **Issue / PR** | At least one of each. A decision with no pull request has not landed. |
| **Context** | The constraints in force at the time. |
| **Decision** | What was chosen. |
| **Alternatives considered** | With the reason each was rejected. |
| **Reconsider when** | The condition that should reopen this. |
| **Consequences** | What this costs, not only what it buys. |

## Cross-repository references

Always `<repo> ADR <n>` -- each repository numbers its own records, and the
same number means different things in different repositories.
