"""`status`: one deterministic answer, and a fixture for every state (#4)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_scheme import status
from ai_scheme.cli import main

BASE = {
    "exists": True,
    "empty": False,
    "is_git_repo": True,
    "has_answers": True,
    "current_version": "1.0.0",
    "target_version": "1.0.0",
    "drift": (),
    "policy_drift": (),
}


def facts(**overrides: object) -> status.Facts:
    return status.Facts(**{**BASE, **overrides})


def test_create_when_the_target_is_empty() -> None:
    answer = status.judge(facts(empty=True, has_answers=False))
    assert answer.state == status.State.CREATE
    assert answer.next_command == "ai-scheme create --plan"


def test_adopt_when_a_project_has_no_answers_file() -> None:
    answer = status.judge(facts(has_answers=False))
    assert answer.state == status.State.ADOPT


def test_mechanism_artefacts_do_not_make_a_project_legacy() -> None:
    """`.scaffolding/` is the other layer's current delivery, not a leftover (#41)."""
    answer = status.judge(facts(has_answers=False, mechanism_markers=(".scaffolding",)))

    assert answer.state == status.State.ADOPT
    assert "mechanism layer is installed" in answer.reason
    assert answer.mechanism_layer_detected == [".scaffolding"]


def test_update_when_the_recorded_version_is_behind() -> None:
    answer = status.judge(facts(current_version="1.0.0", target_version="1.1.0"))
    assert answer.state == status.State.UPDATE


def test_drifted_when_template_owned_files_changed() -> None:
    answer = status.judge(facts(drift=("AGENTS.md", "scripts/verify")))
    assert answer.state == status.State.DRIFTED
    assert answer.drift == ["AGENTS.md", "scripts/verify"]


def test_update_outranks_drift() -> None:
    """The update is what has to merge the drift, so it is the next step."""
    answer = status.judge(facts(target_version="2.0.0", drift=("AGENTS.md",)))
    assert answer.state == status.State.UPDATE
    assert answer.drift == ["AGENTS.md"]


def test_policy_only_update_when_just_the_settings_differ() -> None:
    answer = status.judge(facts(policy_drift=("branch protection",)))
    assert answer.state == status.State.POLICY_ONLY_UPDATE
    assert answer.next_command == "ai-scheme settings apply --plan"


def test_current_when_everything_checked_matches() -> None:
    answer = status.judge(facts())
    assert answer.state == status.State.CURRENT
    assert answer.next_command is None


def test_next_command_is_also_offered_as_argv() -> None:
    """bash callers should not have to eval a string (#41)."""
    answer = status.judge(facts(target_version="2.0.0"))

    assert answer.next_command == "ai-scheme update --plan"
    assert answer.next_command_argv == ["ai-scheme", "update", "--plan"]
    assert status.judge(facts()).next_command_argv == []


def test_unknown_is_not_none() -> None:
    """A check that could not run must not read as a check that passed."""
    answer = status.judge(facts(drift=None, policy_drift=None))
    assert answer.state == status.State.CURRENT
    assert answer.drift == status.UNKNOWN
    assert answer.policy_drift == status.UNKNOWN
    assert "not checked" in answer.reason


@pytest.mark.parametrize(
    ("current", "target", "expected"),
    [
        ("1.0.0", "1.1.0", True),
        ("v1.0.0", "v1.0.0", False),
        ("2.0.0", "1.9.9", False),
        (None, "1.0.0", None),
        ("not-a-version", "1.0.0", None),
    ],
)
def test_version_comparison(current: str | None, target: str, expected: bool | None) -> None:
    assert status.is_behind(current, target) is expected


def test_observe_reads_the_filesystem_only(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / ".template-version").write_text("3.0.0\n")
    (tmp_path / "config.toml").write_text("[project]\n")

    observed = status.observe(tmp_path)

    assert observed.is_git_repo
    assert observed.has_answers is False
    assert observed.mechanism_markers == (".template-version",)
    assert observed.mechanism_config is True


def test_the_mechanism_config_is_reported_and_not_read(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / "config.toml").write_text("[project]\ntype = 'fullstack'\n")

    answer = status.judge(status.collect(tmp_path, target_version="1.0.0"))

    assert answer.mechanism_config_detected is True
    assert answer.state == status.State.ADOPT


def test_the_cli_answers_with_exit_zero_whatever_the_state(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """`update available` is not an error. ADR 0008, #3."""
    (tmp_path / ".git").mkdir()
    (tmp_path / "README.md").write_text("a project\n")

    assert main(["status", str(tmp_path), "--json", "--no-render"]) == 0

    payload = json.loads(capsys.readouterr().out)
    assert payload["state"] == status.State.ADOPT
    assert payload["next_command"] == "ai-scheme adopt --plan"


def test_two_runs_produce_identical_output(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / ".git").mkdir()
    (tmp_path / "README.md").write_text("a project\n")

    main(["status", str(tmp_path), "--json", "--no-render"])
    first = capsys.readouterr().out
    main(["status", str(tmp_path), "--json", "--no-render"])
    second = capsys.readouterr().out

    assert first == second
