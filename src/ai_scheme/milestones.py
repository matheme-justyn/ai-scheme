"""The milestone contract (#9).

A milestone is only worth creating when several issues share one outcome and a
real date. When one exists, its description says the same seven things every
time, and the Feature parent that tracks it carries the matching title.

The previous POC also required a separate tracking issue and an approval
comment from someone other than the proposer. On a repository with one
maintainer that deadlocks, so the parent is the tracker and approval follows
`collaboration_mode` (#20, #24).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

SECTIONS = (
    "Problem",
    "Outcome",
    "Acceptance criteria",
    "Plan",
    "Out of scope",
    "Verification",
    "References",
)

PARENT_TITLE = re.compile(r"^Milestone (\d+): (.+)$")

HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class Problem:
    subject: str
    detail: str

    def __str__(self) -> str:
        return f"{self.subject}: {self.detail}"


def sections(description: str) -> list[str]:
    return [match.group(1) for match in HEADING.finditer(description or "")]


def validate_description(description: str) -> list[Problem]:
    """The seven sections, in order, each with something under it."""
    found = sections(description)
    problems: list[Problem] = []

    missing = [name for name in SECTIONS if name not in found]
    if missing:
        problems.append(Problem("description", f"missing section(s): {', '.join(missing)}"))

    ordered = [name for name in found if name in SECTIONS]
    if ordered != [name for name in SECTIONS if name in ordered]:
        problems.append(Problem("description", "sections are out of order"))

    for name in SECTIONS:
        if name not in found:
            continue
        start = description.index(f"## {name}") + len(f"## {name}")
        rest = description[start:]
        next_heading = HEADING.search(rest)
        body = rest[: next_heading.start()] if next_heading else rest
        if not body.strip():
            problems.append(Problem("description", f"section `{name}` is empty"))

    return problems


def parent_title(number: int, milestone_title: str) -> str:
    return f"Milestone {number}: {milestone_title}"


def validate_parent_title(title: str, milestone_title: str) -> list[Problem]:
    match = PARENT_TITLE.match(title or "")
    if not match:
        return [Problem("parent", "title must read `Milestone <N>: <name>`")]
    if match.group(2) != milestone_title:
        return [
            Problem(
                "parent",
                f"title after the colon is {match.group(2)!r}, milestone is {milestone_title!r}",
            )
        ]
    return []


def preflight(milestone: dict[str, Any], parent: dict[str, Any] | None) -> list[Problem]:
    """Everything that has to be true right after a milestone is created."""
    problems: list[Problem] = []

    if not milestone.get("due_on"):
        problems.append(Problem("milestone", "no due date -- a milestone without one is a bucket"))

    problems.extend(validate_description(milestone.get("description") or ""))

    if parent is None:
        problems.append(Problem("parent", "no Feature parent issue"))
        return problems

    problems.extend(validate_parent_title(parent.get("title", ""), milestone.get("title", "")))

    labels = {
        label["name"] if isinstance(label, dict) else label for label in parent.get("labels", [])
    }
    if "type:feature" not in labels:
        problems.append(Problem("parent", "the parent must carry the type:feature label"))
    if parent.get("milestone"):
        problems.append(
            Problem("parent", "the parent must not carry the milestone -- only leaves do")
        )
    return problems


class State:
    DELIVERED = "Delivered"
    CLOSED_WITHOUT_PR = "Closed without merged PR"
    PENDING = "Pending"


@dataclass(frozen=True)
class Reconciliation:
    number: int
    title: str
    state: str


def reconcile(issues: list[dict[str, Any]]) -> list[Reconciliation]:
    """Sort a milestone's issues into the three states, for a human to check.

    Each issue needs `merged_pull_request` filled in by the caller -- the REST
    payload does not say whether a merged pull request closed an issue, and
    "closed" on its own is exactly the word this report refuses to trust.

    Nothing here closes anything.
    """
    rows: list[Reconciliation] = []
    for issue in issues:
        if "pull_request" in issue:
            continue
        if issue.get("state") != "closed":
            state = State.PENDING
        elif issue.get("merged_pull_request"):
            state = State.DELIVERED
        else:
            state = State.CLOSED_WITHOUT_PR
        rows.append(Reconciliation(issue["number"], issue.get("title", ""), state))
    return rows
