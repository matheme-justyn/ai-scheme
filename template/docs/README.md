# Documentation map

Four layers, four questions. Each has one canonical place, and none of them is
a conversation.

| Layer | Question | Lives in | Changes when |
| --- | --- | --- | --- |
| Specification | What must be true now? | `docs/specs/SPEC-NNN-*.md` | The contract changes |
| Decision | Why this way and not another? | `docs/adr/NNNN-*.md` | A new decision supersedes an old one |
| Work | What are we doing, and when is it done? | Issues and pull requests | Continuously |
| Behaviour | Does it still hold? | Tests | Every commit |

## What belongs where

- A **spec** describes the contract as it stands. It is a living document:
  edit it in place, do not append a changelog to it. Its `tracking` field names
  the issue carrying the work, or `none` when the spec merely records what is
  already true.
- An **ADR** is written once and never edited except to change its status. It
  keeps the reasoning, including the options that were rejected.
- An **issue** carries work: a problem, completion conditions, and the notes
  needed to act. It closes; the spec and the ADR stay.
- A **test** is the only layer that is checked automatically. If a claim
  matters and cannot be tested, say so in the spec rather than hoping.

## What does not belong in the repository

Plans and conversations are not durable truth. Do not commit:

- transcripts of a conversation with an agent, or an agent's reasoning;
- inferences nobody has confirmed, written as though they were established;
- a plan that duplicates the issues, which will drift from them within a week.

If something from a conversation is worth keeping, it is worth rewriting as a
spec, an ADR, or an issue -- in the voice of the repository, not the chat.

## Guides

`docs/guides/` holds the conventions the skeleton ships: style, git workflow,
documentation standards, README structure. They are template-owned and updated
by `ai-scheme update`; edit them upstream, not here.
