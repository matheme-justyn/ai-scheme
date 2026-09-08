"""Answers file loading, validation and shell-facing formatting."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from ai_scheme import config
from ai_scheme.paths import package_root

VALID = {
    "project_name": "Example Project",
    "project_slug": "example-project",
    "project_description": "An example.",
    "languages": ["python"],
    "branch_strategy": "main",
    "readme_primary_language": "en-US",
    "readme_strategy": "separate",
    "commit_locales": ["en-US"],
    "release_phase": "alpha",
    "collaboration_mode": "solo",
    "project_visibility": "public",
    "enable_pages": True,
}


@pytest.fixture
def schema() -> dict:
    return config.load_schema(package_root())


def write_answers(root: Path, answers: dict) -> Path:
    path = root / ".scheme" / "config.yml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(answers, sort_keys=True), encoding="utf-8")
    return path


def test_shipped_schema_is_itself_valid(schema: dict) -> None:
    import jsonschema

    jsonschema.validators.validator_for(schema).check_schema(schema)


def test_valid_answers_produce_no_problems(schema: dict) -> None:
    assert config.validate(VALID, schema) == []


def test_missing_required_key_is_reported(schema: dict) -> None:
    answers = {k: v for k, v in VALID.items() if k != "project_slug"}
    problems = config.validate(answers, schema)
    assert any("project_slug" in problem.message for problem in problems)


@pytest.mark.parametrize(
    "slug",
    ["Example", "example_project", "-example", "example-", "e", "a" * 65],
)
def test_bad_slugs_are_rejected(schema: dict, slug: str) -> None:
    problems = config.validate({**VALID, "project_slug": slug}, schema)
    assert any(problem.location == "project_slug" for problem in problems)


def test_unknown_key_is_rejected(schema: dict) -> None:
    """A typo must fail rather than sit in the file doing nothing."""
    problems = config.validate({**VALID, "colaboration_mode": "solo"}, schema)
    assert problems


def test_empty_language_list_is_allowed(schema: dict) -> None:
    assert config.validate({**VALID, "languages": []}, schema) == []


def test_unknown_language_is_rejected(schema: dict) -> None:
    problems = config.validate({**VALID, "languages": ["cobol"]}, schema)
    assert any(problem.location.startswith("languages") for problem in problems)


def test_primary_language_must_be_committed(schema: dict) -> None:
    """JSON Schema cannot compare two properties, so this rule lives in code."""
    answers = {**VALID, "readme_primary_language": "zh-TW", "commit_locales": ["en-US"]}
    problems = config.validate(answers, schema)
    assert [p.location for p in problems] == ["commit_locales"]


def test_bilingual_strategy_needs_two_locales(schema: dict) -> None:
    answers = {**VALID, "readme_strategy": "bilingual", "commit_locales": ["en-US"]}
    assert config.validate(answers, schema)


def test_academic_settings_without_the_toggle_are_rejected(schema: dict) -> None:
    """A setting that silently does nothing is worse than an error."""
    problems = config.validate(
        {**VALID, "enable_academic_docs": False, "citation_style": "APA"}, schema
    )
    assert [p.location for p in problems] == ["citation_style"]


def test_every_problem_is_reported_not_just_the_first(schema: dict) -> None:
    answers = {**VALID, "project_slug": "Bad Slug", "release_phase": "stable"}
    locations = {p.location for p in config.validate(answers, schema)}
    assert {"project_slug", "release_phase"} <= locations


def test_load_answers_missing_file(tmp_path: Path) -> None:
    with pytest.raises(config.ConfigError, match="no answers file"):
        config.load_answers(tmp_path)


def test_load_answers_rejects_non_mapping(tmp_path: Path) -> None:
    path = tmp_path / ".scheme" / "config.yml"
    path.parent.mkdir(parents=True)
    path.write_text("- a\n- b\n", encoding="utf-8")
    with pytest.raises(config.ConfigError, match="must contain a mapping"):
        config.load_answers(tmp_path)


def test_load_answers_roundtrip(tmp_path: Path) -> None:
    write_answers(tmp_path, VALID)
    assert config.load_answers(tmp_path) == VALID


def test_get_missing_key_names_the_path() -> None:
    with pytest.raises(config.ConfigError, match="no such key: nope"):
        config.get(VALID, "nope")


def test_get_distinguishes_absent_from_null() -> None:
    answers = {**VALID, "project_description": None}
    assert config.get(answers, "project_description") is None
    with pytest.raises(config.ConfigError):
        config.get(answers, "project_summary")


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (True, "true"),
        (False, "false"),
        (None, ""),
        ("main", "main"),
        (3, "3"),
        (["python", "rust"], "python\nrust"),
        ([], ""),
    ],
)
def test_format_value_for_shell(value: object, expected: str) -> None:
    assert config.format_value(value) == expected


def test_schema_file_is_valid_json() -> None:
    raw = (package_root() / "schemas" / "scheme-config.schema.json").read_text(encoding="utf-8")
    json.loads(raw)
