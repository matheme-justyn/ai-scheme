"""The milestone contract (#9)."""

from __future__ import annotations

import json

import pytest

from ai_scheme import gh, milestones

GOOD = "\n".join(f"## {name}\n\nsomething\n" for name in milestones.SECTIONS)


def test_a_seven_section_description_passes() -> None:
    assert milestones.validate_description(GOOD) == []


def test_a_missing_section_is_named() -> None:
    without_plan = GOOD.replace("## Plan\n\nsomething\n", "")
    problems = milestones.validate_description(without_plan)
    assert "Plan" in str(problems[0])


def test_an_empty_section_is_rejected() -> None:
    hollow = GOOD.replace("## Verification\n\nsomething\n", "## Verification\n\n")
    assert any(
        "`Verification` is empty" in str(problem)
        for problem in milestones.validate_description(hollow)
    )


def test_sections_out_of_order_are_rejected() -> None:
    shuffled = "## Outcome\n\nx\n\n## Problem\n\nx\n" + "\n".join(
        f"## {name}\n\nx\n" for name in milestones.SECTIONS[2:]
    )
    assert any(
        "out of order" in str(problem) for problem in milestones.validate_description(shuffled)
    )


def test_the_parent_title_is_built_from_the_number() -> None:
    assert milestones.parent_title(3, "Verified lifecycle") == "Milestone 3: Verified lifecycle"


@pytest.mark.parametrize(
    "title",
    ["Milestone 1 Verified lifecycle", "Verified lifecycle", "milestone 1: Verified lifecycle"],
)
def test_a_parent_title_off_contract_is_rejected(title: str) -> None:
    assert milestones.validate_parent_title(title, "Verified lifecycle")


def test_a_parent_title_that_disagrees_with_the_milestone_is_rejected() -> None:
    problems = milestones.validate_parent_title("Milestone 1: Something else", "Verified lifecycle")
    assert "milestone is 'Verified lifecycle'" in str(problems[0])


def test_preflight_wants_a_due_date_and_a_parent_without_the_milestone() -> None:
    milestone = {"title": "Verified lifecycle", "description": GOOD, "due_on": None}
    parent = {
        "title": "Milestone 1: Verified lifecycle",
        "labels": [{"name": "type:feature"}],
        "milestone": {"number": 1},
    }

    problems = [str(problem) for problem in milestones.preflight(milestone, parent)]

    assert any("no due date" in problem for problem in problems)
    assert any("must not carry the milestone" in problem for problem in problems)


def test_preflight_is_happy_with_a_compliant_milestone() -> None:
    milestone = {
        "title": "Verified lifecycle",
        "description": GOOD,
        "due_on": "2026-11-30T00:00:00Z",
    }
    parent = {
        "title": "Milestone 1: Verified lifecycle",
        "labels": [{"name": "type:feature"}],
        "milestone": None,
    }

    assert milestones.preflight(milestone, parent) == []


def test_reconcile_separates_closed_from_delivered() -> None:
    rows = milestones.reconcile(
        [
            {"number": 1, "title": "one", "state": "closed", "merged_pull_request": True},
            {"number": 2, "title": "two", "state": "closed", "merged_pull_request": False},
            {"number": 3, "title": "three", "state": "open"},
            {"number": 4, "title": "a pull request", "state": "closed", "pull_request": {}},
        ]
    )

    assert [(row.number, row.state) for row in rows] == [
        (1, milestones.State.DELIVERED),
        (2, milestones.State.CLOSED_WITHOUT_PR),
        (3, milestones.State.PENDING),
    ]


def test_gh_client_uses_the_injected_runner() -> None:
    calls: list[list[str]] = []

    def runner(args):
        calls.append(list(args))
        return json.dumps([{"title": "Verified lifecycle", "number": 1}])

    client = gh.Client(runner)

    assert client.open_milestones("owner/name")[0]["title"] == "Verified lifecycle"
    assert calls == [["api", "repos/owner/name/milestones?state=open", "--method", "GET"]]


def test_gh_client_reports_non_json_output() -> None:
    client = gh.Client(lambda args: "not json")
    with pytest.raises(gh.GhError):
        client.api("repos/owner/name/milestones")


def test_delivered_means_a_merged_pull_request_not_just_a_link() -> None:
    """A closed issue with an unmerged linked pull request is not delivered."""
    responses = {
        ("issue", "view"): json.dumps(
            {"closedByPullRequestsReferences": [{"number": 30}, {"number": 31}]}
        ),
        ("api", "repos/owner/name/pulls/30"): json.dumps({"merged_at": None}),
        ("api", "repos/owner/name/pulls/31"): json.dumps({"merged_at": None}),
    }

    def runner(args):
        return responses[(args[0], args[1])]

    assert gh.Client(runner).closed_by_merged_pull_request("owner/name", 3) is False

    responses[("api", "repos/owner/name/pulls/30")] = json.dumps(
        {"merged_at": "2026-09-08T00:00:00Z"}
    )
    assert gh.Client(runner).closed_by_merged_pull_request("owner/name", 3) is True
