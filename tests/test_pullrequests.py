"""The pull request contract (#8)."""

from __future__ import annotations

import pytest

from ai_scheme import pullrequests as pr

READY = {
    "number": 34,
    "title": "feat(milestone): add the milestone description contract",
    "body": "Closes #9\n\n## 完成清單\n\n- [x] done\n- [x] also done\n",
    "isDraft": False,
    "headRefName": "feat/9-milestone-contract",
    "labels": [{"name": "enhancement"}],
    "milestone": {"title": "Verified lifecycle"},
    "reviewRequests": [],
}

ISSUE = {
    "number": 9,
    "body": "## 完成條件\n\n- [x] one\n- [x] two\n",
    "labels": [{"name": "enhancement"}],
    "milestone": {"title": "Verified lifecycle"},
}


def test_a_complete_pull_request_passes() -> None:
    assert pr.validate(READY, ISSUE) == []


@pytest.mark.parametrize(
    ("title", "ok"),
    [
        ("feat: add a thing", True),
        ("feat(scope): add a thing", True),
        ("feat(scope)!: remove a thing", True),
        ("Add a thing", False),
        ("feature: add a thing", False),
        ("feat add a thing", False),
    ],
)
def test_title_format(title: str, ok: bool) -> None:
    problems = pr.validate_shape({**READY, "title": title})
    assert (problems == []) is ok


@pytest.mark.parametrize(
    ("branch", "ok"),
    [
        ("feat/9-milestone-contract", True),
        ("fix/12-nested-go-path", True),
        ("milestone-contract", False),
        ("feat/milestone-contract", False),
        ("feat/9_milestone", False),
    ],
)
def test_branch_format(branch: str, ok: bool) -> None:
    problems = pr.validate_shape({**READY, "headRefName": branch})
    assert (problems == []) is ok


def test_a_draft_is_only_checked_for_shape() -> None:
    """The expensive lesson: an incomplete pull request must not rerun the gate."""
    draft = {**READY, "isDraft": True, "body": "no closing keyword\n\n- [ ] not done\n"}

    assert pr.validate(draft, None) == []


def test_a_ready_pull_request_with_unticked_boxes_is_rejected() -> None:
    problems = pr.validate({**READY, "body": "Closes #9\n\n- [x] one\n- [ ] two\n"}, ISSUE)
    assert any("keep the pull request a draft" in str(problem) for problem in problems)


def test_the_issue_checklist_is_checked_too() -> None:
    problems = pr.validate(READY, {**ISSUE, "body": "- [ ] not yet\n"})
    assert any("unticked completion condition" in str(problem) for problem in problems)


def test_missing_closing_keyword_is_rejected() -> None:
    problems = pr.validate({**READY, "body": "## 完成清單\n\n- [x] done\n"}, None)
    assert any(problem.rule == "closes" for problem in problems)


def test_branch_and_body_must_name_the_same_issue() -> None:
    problems = pr.validate({**READY, "headRefName": "feat/11-something"}, ISSUE)
    assert any("the body closes #9" in str(problem) for problem in problems)


def test_labels_and_milestone_must_match_the_issue() -> None:
    problems = pr.validate({**READY, "labels": [], "milestone": None}, ISSUE)
    rules = {problem.rule for problem in problems}
    assert rules == {"labels", "milestone"}


def test_team_mode_wants_a_reviewer_and_solo_does_not() -> None:
    assert pr.validate(READY, ISSUE, collaboration_mode="solo") == []
    problems = pr.validate(READY, ISSUE, collaboration_mode="team")
    assert any(problem.rule == "review" for problem in problems)


def test_closing_keywords_are_recognised_in_their_usual_spellings() -> None:
    assert pr.closes("Closes #1, fixes #2, resolved #3") == [1, 2, 3]
