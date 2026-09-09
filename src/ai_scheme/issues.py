"""The issue contract: title rules and the shape of the issue forms (#7).

The forms ask three questions -- what the problem is, what "done" looks like,
and anything else worth knowing. A longer form is not filled in: the twenty-odd
field templates this replaces were abandoned by people and by agents alike.

Titles are checked before an issue is created, because a bad title is only
cheap to fix before other issues start linking to it.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

MIN_LENGTH = 12
MAX_LENGTH = 80
MIN_WORDS = 3

# `[FEATURE]`, `feat:`, `WIP -` and friends. The type belongs in a label, and
# GitHub already shows it; in the title it costs width and sorts badly.
PREFIX = re.compile(r"^\s*(\[[^\]]*\]|\((?!\s)[^)]*\)|[A-Za-z]+\s*[:/-])\s+")

FORM_RELDIR = Path(".github/ISSUE_TEMPLATE")
REQUIRED_FIELD_LABELS = ("問題", "完成條件")
OPTIONAL_FIELD_LABEL = "補充"
LABELS_RELPATH = Path("policies/labels.json")


@dataclass(frozen=True)
class TitleProblem:
    rule: str
    detail: str

    def __str__(self) -> str:
        return f"{self.rule}: {self.detail}"


def validate_title(title: str) -> list[TitleProblem]:
    """Every rule the title breaks, so one run reports all of them."""
    problems: list[TitleProblem] = []
    stripped = title.strip()

    if stripped != title:
        problems.append(TitleProblem("whitespace", "leading or trailing whitespace"))

    if not stripped:
        return [TitleProblem("empty", "a title is required")]

    if len(stripped) < MIN_LENGTH:
        problems.append(
            TitleProblem("length", f"{len(stripped)} characters, at least {MIN_LENGTH} needed")
        )
    if len(stripped) > MAX_LENGTH:
        problems.append(
            TitleProblem("length", f"{len(stripped)} characters, at most {MAX_LENGTH} allowed")
        )

    non_ascii = sorted({char for char in stripped if ord(char) > 127})
    if non_ascii:
        names = ", ".join(f"{char!r} ({unicodedata.name(char, 'unnamed')})" for char in non_ascii)
        problems.append(TitleProblem("ascii", f"non-ASCII character(s): {names}"))

    if len(stripped.split()) < MIN_WORDS:
        problems.append(TitleProblem("words", f"at least {MIN_WORDS} words needed"))

    if PREFIX.match(stripped):
        problems.append(TitleProblem("prefix", "drop the bracketed or typed prefix"))

    if stripped.endswith("."):
        problems.append(TitleProblem("punctuation", "no full stop at the end"))

    return problems


@dataclass(frozen=True)
class FormProblem:
    form: str
    detail: str

    def __str__(self) -> str:
        return f"{self.form}: {self.detail}"


def _field_labels(form: dict[str, Any]) -> list[str]:
    return [
        (field.get("attributes") or {}).get("label", "")
        for field in form.get("body") or []
        if field.get("type") != "markdown"
    ]


def validate_form(name: str, form: Any) -> list[FormProblem]:
    problems: list[FormProblem] = []
    if not isinstance(form, dict):
        return [FormProblem(name, "the form is not a mapping")]

    for key in ("name", "description", "labels", "body"):
        if key not in form:
            problems.append(FormProblem(name, f"missing `{key}`"))

    labels = form.get("labels") or []
    if not any(str(label).startswith("type:") for label in labels):
        problems.append(FormProblem(name, "no `type:` label -- personal repos have no issue types"))

    field_labels = _field_labels(form)
    for required in REQUIRED_FIELD_LABELS:
        if required not in field_labels:
            problems.append(FormProblem(name, f"missing the `{required}` field"))
    if OPTIONAL_FIELD_LABEL not in field_labels:
        problems.append(FormProblem(name, f"missing the `{OPTIONAL_FIELD_LABEL}` field"))

    extra = [
        label
        for label in field_labels
        if label not in (*REQUIRED_FIELD_LABELS, OPTIONAL_FIELD_LABEL)
    ]
    if extra:
        problems.append(FormProblem(name, f"unexpected field(s): {', '.join(extra)}"))

    for field in form.get("body") or []:
        attributes = field.get("attributes") or {}
        label = attributes.get("label")
        required = (field.get("validations") or {}).get("required", False)
        if label in REQUIRED_FIELD_LABELS and not required:
            problems.append(FormProblem(name, f"`{label}` must be required"))
        if label == OPTIONAL_FIELD_LABEL and required:
            problems.append(FormProblem(name, f"`{label}` must not be required"))

    return problems


def load_forms(root: Path) -> dict[str, Any]:
    directory = root / FORM_RELDIR
    forms: dict[str, Any] = {}
    for path in sorted(directory.glob("*.yml")):
        if path.name == "config.yml":
            continue
        forms[path.name] = yaml.safe_load(path.read_text(encoding="utf-8"))
    return forms


def validate_forms(root: Path) -> list[FormProblem]:
    problems: list[FormProblem] = []
    forms = load_forms(root)
    if not forms:
        return [FormProblem(str(FORM_RELDIR), "no issue forms found")]

    config_path = root / FORM_RELDIR / "config.yml"
    if not config_path.is_file():
        problems.append(FormProblem("config.yml", "missing"))
    else:
        config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        if config.get("blank_issues_enabled", True):
            problems.append(FormProblem("config.yml", "blank_issues_enabled must be false"))

    declared = declared_labels(root)
    for name, form in forms.items():
        problems.extend(validate_form(name, form))
        if declared is not None and isinstance(form, dict):
            for label in form.get("labels") or []:
                if label not in declared:
                    problems.append(FormProblem(name, f"label `{label}` is not in policies"))
    return problems


def declared_labels(root: Path) -> set[str] | None:
    """Label names from the policy file, or None when there is no policy."""
    path = root / LABELS_RELPATH
    if not path.is_file():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {entry["name"] for entry in raw.get("labels", [])}
