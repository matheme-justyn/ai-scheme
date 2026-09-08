"""Reading and validating the answers file.

`.scheme/config.yml` is the only source of skeleton-layer settings. Shell
scripts call `ai-scheme config get <key>` rather than parsing YAML themselves,
which is why `get` prints scalars bare and never quotes them.

This module never reads ai-zpd's config.toml. Same-named keys in the two files
are independent and there is no fallback between them -- see ADR 0008.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ai_scheme.paths import (
    ANSWERS_RELPATH,
    SCHEMA_RELPATH,
    package_root,
)


class ConfigError(Exception):
    """Raised when the answers file is missing, unreadable or invalid."""


@dataclass(frozen=True)
class ValidationProblem:
    location: str
    message: str

    def __str__(self) -> str:
        where = self.location or "(root)"
        return f"{where}: {self.message}"


def load_schema(root: Path | None = None) -> dict[str, Any]:
    schema_path = (root or package_root()) / SCHEMA_RELPATH
    if not schema_path.is_file():
        raise ConfigError(f"schema not found: {schema_path}")
    return json.loads(schema_path.read_text(encoding="utf-8"))


def load_answers(project_root: Path) -> dict[str, Any]:
    answers_path = project_root / ANSWERS_RELPATH
    if not answers_path.is_file():
        raise ConfigError(
            f"no answers file at {answers_path}. "
            "This project has not been created from or adopted into ai-scheme yet."
        )
    try:
        loaded = yaml.safe_load(answers_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"{answers_path} is not valid YAML: {exc}") from exc
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        raise ConfigError(f"{answers_path} must contain a mapping, got {type(loaded).__name__}")
    return loaded


def validate(answers: dict[str, Any], schema: dict[str, Any]) -> list[ValidationProblem]:
    """Return every problem found, rather than stopping at the first.

    A caller fixing a generated project wants the whole list in one run.
    """
    import jsonschema

    validator_cls = jsonschema.validators.validator_for(schema)
    validator_cls.check_schema(schema)
    validator = validator_cls(schema)

    problems = [
        ValidationProblem(
            location="/".join(str(part) for part in error.absolute_path),
            message=error.message,
        )
        for error in sorted(validator.iter_errors(answers), key=lambda e: list(e.absolute_path))
    ]
    problems.extend(_cross_field_problems(answers))
    return problems


def _cross_field_problems(answers: dict[str, Any]) -> list[ValidationProblem]:
    """Rules JSON Schema cannot express, because they compare two properties.

    Draft 2020-12 has no way to say "this array must contain the value of that
    other property", so the locale consistency rules live here instead of being
    contorted into the schema.
    """
    problems: list[ValidationProblem] = []

    primary = answers.get("readme_primary_language")
    locales = answers.get("commit_locales")
    if primary is not None and isinstance(locales, list) and primary not in locales:
        problems.append(
            ValidationProblem(
                location="commit_locales",
                message=(
                    f"must include readme_primary_language ({primary!r}); "
                    "the primary language's sources cannot be uncommitted"
                ),
            )
        )

    if answers.get("enable_academic_docs") is False:
        for key in ("citation_style", "academic_field"):
            if key in answers:
                problems.append(
                    ValidationProblem(
                        location=key,
                        message="set while enable_academic_docs is false; remove it or enable",
                    )
                )

    if answers.get("enable_terminology") is False and answers.get("terminology_domains"):
        problems.append(
            ValidationProblem(
                location="terminology_domains",
                message="set while enable_terminology is false; remove it or enable terminology",
            )
        )

    return problems


def get(answers: dict[str, Any], key: str) -> Any:
    """Look up a dotted key. Raises ConfigError when absent.

    Absent and null are deliberately different: a key that is not in the file
    is a caller error, a key that is explicitly null is a value.
    """
    node: Any = answers
    walked: list[str] = []
    for part in key.split("."):
        walked.append(part)
        if not isinstance(node, dict) or part not in node:
            raise ConfigError(f"no such key: {'.'.join(walked)}")
        node = node[part]
    return node


def format_value(value: Any) -> str:
    """Render a value for shell consumption.

    Lists print one item per line so that `for x in $(ai-scheme config get
    languages)` works; booleans print lowercase so they compare against
    `true`/`false` the way YAML and JSON write them.
    """
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, list):
        return "\n".join(format_value(item) for item in value)
    if value is None:
        return ""
    return str(value)
