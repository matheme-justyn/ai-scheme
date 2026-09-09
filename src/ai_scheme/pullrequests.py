"""The pull request contract and its validator (#8).

A pull request says which issue it closes, carries a checklist that is
complete, and agrees with that issue about labels and milestone. The previous
POC learned the expensive half of this: a pull request pushed before its
checklist was done reran the whole gate on every push, dozens of times for one
change. So an incomplete pull request stays a draft, and a draft is only
checked for the things that are cheap to check.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

CLOSING_KEYWORD = re.compile(r"\b(?:close[sd]?|fixe?[sd]?|resolve[sd]?)\s+#(\d+)\b", re.IGNORECASE)
CHECKBOX = re.compile(r"^\s*[-*]\s+\[( |x|X)\]", re.MULTILINE)
BRANCH = re.compile(r"^(feat|fix|docs|refactor|test|chore)/(\d+)-[a-z0-9][a-z0-9-]*$")
TITLE = re.compile(r"^(feat|fix|docs|refactor|test|chore)(\([a-z0-9][a-z0-9-]*\))?!?: .+$")

TYPES = ("feat", "fix", "docs", "refactor", "test", "chore")


@dataclass(frozen=True)
class Problem:
    rule: str
    detail: str

    def __str__(self) -> str:
        return f"{self.rule}: {self.detail}"


def closes(body: str) -> list[int]:
    return [int(number) for number in CLOSING_KEYWORD.findall(body or "")]


def unchecked_boxes(body: str) -> int:
    return sum(1 for match in CHECKBOX.finditer(body or "") if match.group(1) == " ")


def total_boxes(body: str) -> int:
    return len(CHECKBOX.findall(body or ""))


def _names(items: list[Any]) -> set[str]:
    return {item["name"] if isinstance(item, dict) else item for item in items or []}


def validate_shape(pull: dict[str, Any]) -> list[Problem]:
    """The checks that are cheap and true even for a draft."""
    problems: list[Problem] = []

    title = pull.get("title", "")
    if not TITLE.match(title):
        problems.append(
            Problem(
                "title",
                f"must read `type(scope): description` with type in {', '.join(TYPES)}",
            )
        )

    branch = pull.get("headRefName", "")
    if not BRANCH.match(branch):
        problems.append(Problem("branch", "must read `type/<issue>-slug`, e.g. feat/9-milestone"))

    return problems


def validate_ready(
    pull: dict[str, Any],
    issue: dict[str, Any] | None,
    *,
    collaboration_mode: str = "solo",
) -> list[Problem]:
    """Everything else -- only asked of a pull request marked ready."""
    problems: list[Problem] = list(validate_shape(pull))

    body = pull.get("body", "")
    closed = closes(body)
    if not closed:
        problems.append(Problem("closes", "the body must close an issue: `Closes #N`"))
    elif issue is None:
        problems.append(Problem("closes", f"issue #{closed[0]} does not exist"))

    if total_boxes(body) == 0:
        problems.append(Problem("checklist", "the body has no completion checklist"))
    elif unchecked_boxes(body):
        problems.append(
            Problem(
                "checklist",
                f"{unchecked_boxes(body)} unticked item(s) -- keep the pull request a draft",
            )
        )

    branch = pull.get("headRefName", "")
    match = BRANCH.match(branch)
    if match and closed and int(match.group(2)) != closed[0]:
        problems.append(
            Problem("branch", f"names issue #{match.group(2)}, the body closes #{closed[0]}")
        )

    if issue is not None:
        if unchecked_boxes(issue.get("body", "")):
            problems.append(
                Problem(
                    "issue",
                    f"issue #{issue['number']} still has "
                    f"{unchecked_boxes(issue.get('body', ''))} unticked completion condition(s)",
                )
            )

        issue_labels = _names(issue.get("labels", []))
        pull_labels = _names(pull.get("labels", []))
        missing = issue_labels - pull_labels
        if missing:
            problems.append(Problem("labels", f"missing from the pull request: {sorted(missing)}"))

        issue_milestone = (issue.get("milestone") or {}).get("title")
        pull_milestone = (pull.get("milestone") or {}).get("title")
        if issue_milestone != pull_milestone:
            problems.append(
                Problem(
                    "milestone",
                    f"issue has {issue_milestone!r}, pull request has {pull_milestone!r}",
                )
            )

    if collaboration_mode == "team" and not pull.get("reviewRequests"):
        problems.append(Problem("review", "team mode needs a review request from another person"))

    return problems


def validate(
    pull: dict[str, Any],
    issue: dict[str, Any] | None,
    *,
    collaboration_mode: str = "solo",
) -> list[Problem]:
    if pull.get("isDraft"):
        return validate_shape(pull)
    return validate_ready(pull, issue, collaboration_mode=collaboration_mode)
