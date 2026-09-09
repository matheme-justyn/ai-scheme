# Milestones

## When to create one

Only when several issues share one outcome **and** a real date. A milestone is
not a release label, not a backlog bucket, and not a place to park work with no
deadline. If you cannot name the date, you do not have a milestone yet.

One open milestone at a time is the normal state. `scripts/detect-open-milestone`
answers "is there exactly one?", and the issue and pull request tooling uses
that as a hint -- never as a gate.

## The description has seven sections

Always these, always in this order:

| Section | What goes in it |
| --- | --- |
| Problem | What is wrong now, and why it cannot stay that way |
| Outcome | What a person can do once this is finished |
| Acceptance criteria | A checklist somebody else can verify |
| Plan | The issues, in dependency order |
| Out of scope | What this milestone deliberately does not do |
| Verification | How the outcome is proven, end to end |
| References | Decisions and interfaces this depends on |

`scripts/create-milestone` refuses a description that is missing a section, has
them out of order, or leaves one empty -- before the milestone exists, because
a milestone description is awkward to fix once issues point at it.

## The Feature parent is the tracker

Every milestone has one Feature parent issue, titled:

    Milestone <N>: <milestone name>

The part after the colon is the milestone's name, character for character. The
number is the milestone's own number, which is why `scripts/create-milestone`
builds the title from what GitHub returns rather than from what you typed.

The parent holds completion evidence and, if it comes to that, the reason for
stopping early. It does **not** carry the milestone: only leaf issues and pull
requests do, so that progress is counted once instead of three times.

The previous POC required a separate tracking issue and an approval comment
from somebody other than the proposer. With one maintainer that deadlocks, so
the parent doubles as the tracker and approval follows `collaboration_mode`.

## Before closing

Run `scripts/reconcile-milestone <N>`. It sorts every issue in the milestone
into three states:

- **Delivered** -- closed by a merged pull request.
- **Closed without merged PR** -- closed by hand. Legitimate sometimes, but it
  should be a decision, not a surprise.
- **Pending** -- still open. Move it to the next milestone or drop it, and say
  which in the parent.

The script reports. Closing the milestone is still yours to do.
