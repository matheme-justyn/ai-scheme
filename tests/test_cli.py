"""CLI behaviour, chiefly the exit codes shell callers branch on."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest
import yaml

from ai_scheme.cli import EXIT_NO, EXIT_OK, EXIT_UNDETERMINED, main
from ai_scheme.paths import package_root
from tests.test_config import VALID


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A project directory with a valid answers file and a copy of the manifest."""
    answers = tmp_path / ".scheme" / "config.yml"
    answers.parent.mkdir(parents=True)
    answers.write_text(yaml.safe_dump(VALID, sort_keys=True), encoding="utf-8")
    shutil.copy(package_root() / "ownership.yml", tmp_path / "ownership.yml")
    shutil.copy(package_root() / "copier.yml", tmp_path / "copier.yml")
    return tmp_path


def run(*args: str) -> int:
    return main(list(args))


def test_config_get_prints_a_bare_scalar(project: Path, capsys) -> None:
    assert run("-C", str(project), "config", "get", "project_slug") == EXIT_OK
    assert capsys.readouterr().out == "example-project\n"


def test_config_get_prints_one_list_item_per_line(project: Path, capsys) -> None:
    assert run("-C", str(project), "config", "get", "languages") == EXIT_OK
    assert capsys.readouterr().out == "python\n"


def test_config_get_prints_lowercase_booleans(project: Path, capsys) -> None:
    assert run("-C", str(project), "config", "get", "enable_pages") == EXIT_OK
    assert capsys.readouterr().out == "true\n"


def test_config_get_unknown_key_is_undetermined(project: Path, capsys) -> None:
    assert run("-C", str(project), "config", "get", "nope") == EXIT_UNDETERMINED
    assert "no such key" in capsys.readouterr().err


def test_config_get_without_answers_file_is_undetermined(tmp_path: Path, capsys) -> None:
    assert run("-C", str(tmp_path), "config", "get", "project_slug") == EXIT_UNDETERMINED
    assert "no answers file" in capsys.readouterr().err


def test_config_validate_accepts_a_good_file(project: Path) -> None:
    assert run("-C", str(project), "config", "validate") == EXIT_OK


def test_config_validate_rejects_a_bad_file(project: Path, capsys) -> None:
    answers = project / ".scheme" / "config.yml"
    bad = {**VALID, "release_phase": "stable"}
    answers.write_text(yaml.safe_dump(bad, sort_keys=True), encoding="utf-8")

    assert run("-C", str(project), "config", "validate") == EXIT_NO
    err = capsys.readouterr().err
    assert "release_phase" in err


def test_validate_exit_code_separates_invalid_from_unreadable(tmp_path: Path) -> None:
    """1 means "the answer is no", 2 means "I could not tell" -- shell callers rely on it."""
    assert run("-C", str(tmp_path), "config", "validate") == EXIT_UNDETERMINED


def test_ownership_sync_check_passes_on_the_repo(capsys) -> None:
    assert run("-C", str(package_root()), "ownership", "sync", "--check") == EXIT_OK
    assert "up to date" in capsys.readouterr().out


def test_ownership_sync_check_fails_when_generated_files_drift(project: Path, capsys) -> None:
    copier = project / "copier.yml"
    copier.write_text(
        copier.read_text(encoding="utf-8").replace("  - src/", "  - src/\n  - stale/"),
        encoding="utf-8",
    )
    assert run("-C", str(project), "ownership", "sync", "--check") == EXIT_NO
    assert "ownership sync" in capsys.readouterr().err


def test_ownership_sync_writes_and_then_is_clean(project: Path) -> None:
    assert run("-C", str(project), "ownership", "sync") == EXIT_OK
    assert (project / "docs" / "uninstall.md").is_file()
    assert run("-C", str(project), "ownership", "sync", "--check") == EXIT_OK


def test_ownership_list_reports_every_declared_path(capsys) -> None:
    assert run("-C", str(package_root()), "ownership", "list") == EXIT_OK
    out = capsys.readouterr().out
    assert "docs/adr/" in out
    assert "managed-block" in out


def test_ownership_without_manifest_is_undetermined(tmp_path: Path, capsys) -> None:
    assert run("-C", str(tmp_path), "ownership", "list") == EXIT_UNDETERMINED
    assert "not found" in capsys.readouterr().err
