"""The issue contract: titles and the three-field forms (#7)."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ai_scheme import issues
from ai_scheme.paths import package_root

VALID = [
    "Add a deterministic status command",
    "Replace issue templates with lean typed issue forms",
    "Record every ruleset bypass with a traceable comment",
    "Fix the nested go profile path",
    "Publish the decision site to GitHub Pages",
]

INVALID = [
    ("[FEATURE] add a status command", "prefix"),
    ("feat: add a status command", "prefix"),
    ("Add status", "length"),
    ("Add a deterministic status command.", "punctuation"),
    ("加入狀態指令的實作與測試", "ascii"),
]


@pytest.mark.parametrize("title", VALID)
def test_accepted_titles(title: str) -> None:
    assert issues.validate_title(title) == []


@pytest.mark.parametrize(("title", "rule"), INVALID)
def test_rejected_titles(title: str, rule: str) -> None:
    problems = issues.validate_title(title)
    assert rule in [problem.rule for problem in problems]


def test_a_title_reports_every_broken_rule_at_once() -> None:
    problems = issues.validate_title("[BUG] broken.")
    assert {problem.rule for problem in problems} == {"words", "prefix", "punctuation"}


def test_the_shipped_forms_satisfy_the_contract() -> None:
    assert issues.validate_forms(package_root()) == []


def test_a_fifth_field_is_rejected() -> None:
    form = yaml.safe_load(
        (package_root() / issues.FORM_RELDIR / "task.yml").read_text(encoding="utf-8")
    )
    form["body"].append({"type": "input", "id": "extra", "attributes": {"label": "Environment"}})

    problems = issues.validate_form("task.yml", form)

    assert any("unexpected field" in str(problem) for problem in problems)


def test_an_optional_acceptance_field_is_rejected() -> None:
    form = yaml.safe_load(
        (package_root() / issues.FORM_RELDIR / "task.yml").read_text(encoding="utf-8")
    )
    for field in form["body"]:
        if (field.get("attributes") or {}).get("label") == "完成條件":
            field["validations"]["required"] = False

    problems = issues.validate_form("task.yml", form)

    assert any("must be required" in str(problem) for problem in problems)


def test_forms_may_only_use_declared_labels(tmp_path: Path) -> None:
    forms = tmp_path / issues.FORM_RELDIR
    forms.mkdir(parents=True)
    (forms / "config.yml").write_text("blank_issues_enabled: false\n", encoding="utf-8")
    source = (package_root() / issues.FORM_RELDIR / "task.yml").read_text(encoding="utf-8")
    (forms / "task.yml").write_text(source.replace("type:task", "type:invented"), encoding="utf-8")
    (tmp_path / issues.LABELS_RELPATH).parent.mkdir(parents=True)
    (tmp_path / issues.LABELS_RELPATH).write_text(
        '{"labels": [{"name": "type:task"}]}', encoding="utf-8"
    )

    problems = issues.validate_forms(tmp_path)

    assert any("not in policies" in str(problem) for problem in problems)


def test_blank_issues_must_be_off(tmp_path: Path) -> None:
    forms = tmp_path / issues.FORM_RELDIR
    forms.mkdir(parents=True)
    (forms / "config.yml").write_text("blank_issues_enabled: true\n", encoding="utf-8")
    source = (package_root() / issues.FORM_RELDIR / "task.yml").read_text(encoding="utf-8")
    (forms / "task.yml").write_text(source, encoding="utf-8")

    problems = issues.validate_forms(tmp_path)

    assert any("blank_issues_enabled" in str(problem) for problem in problems)
