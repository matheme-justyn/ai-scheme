"""Validating the durable half of a project's memory (#10).

Four layers: specs say what must be true, decision records say why, issues
carry the work, tests check the behaviour. Only the last one is checked by a
machine, which is why the other three drift. This module checks what can be
checked about the first two: that a spec declares what it is, that its
identifier is unique, that it carries the sections somebody else has to read,
and that a decision record has a status from the vocabulary and a date.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml

SPECS_RELDIR = Path("docs/specs")
ADR_RELDIR = Path("docs/adr")

SPEC_FILENAME = re.compile(r"^SPEC-(\d{3})-[a-z0-9][a-z0-9-]*\.md$")
FRONTMATTER = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HEADING = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)

SPEC_STATUSES = ("draft", "approved", "superseded")
SPEC_SECTIONS = (
    "Problem",
    "Outcome",
    "Acceptance criteria",
    "Plan",
    "Out of scope",
    "Verification",
    "References",
)

ADR_STATUSES = ("Proposed", "Accepted", "Superseded", "Rejected")
ADR_STATUS_LINE = re.compile(r"(?:^\*\*Status\*\*:\s*(.+)$)|(?:^##\s+Status\s*$)", re.MULTILINE)
ADR_DATE = re.compile(r"(?:\*\*Date\*\*:\s*|^Date:\s*)(\d{4}-\d{2}-\d{2})", re.MULTILINE)


@dataclass(frozen=True)
class Problem:
    path: str
    detail: str

    def __str__(self) -> str:
        return f"{self.path}: {self.detail}"


def frontmatter(text: str) -> dict[str, object] | None:
    match = FRONTMATTER.match(text)
    if not match:
        return None
    loaded = yaml.safe_load(match.group(1))
    return loaded if isinstance(loaded, dict) else None


def validate_spec(relative: str, text: str) -> list[Problem]:
    problems: list[Problem] = []
    meta = frontmatter(text)
    if meta is None:
        return [Problem(relative, "no YAML frontmatter")]

    for key in ("id", "title", "status", "tracking"):
        if not meta.get(key):
            problems.append(Problem(relative, f"frontmatter is missing `{key}`"))

    status = str(meta.get("status", ""))
    if status and status not in SPEC_STATUSES:
        problems.append(
            Problem(relative, f"status {status!r} is not one of {', '.join(SPEC_STATUSES)}")
        )

    identifier = str(meta.get("id", ""))
    name = Path(relative).name
    match = SPEC_FILENAME.match(name)
    if not match:
        problems.append(Problem(relative, "filename must read SPEC-NNN-slug.md"))
    elif identifier and identifier != f"SPEC-{match.group(1)}":
        problems.append(Problem(relative, f"id {identifier!r} does not match the filename"))

    found = set(HEADING.findall(text))
    missing = [section for section in SPEC_SECTIONS if section not in found]
    if missing:
        problems.append(Problem(relative, f"missing section(s): {', '.join(missing)}"))

    return problems


def validate_adr(relative: str, text: str) -> list[Problem]:
    problems: list[Problem] = []

    status_match = ADR_STATUS_LINE.search(text)
    if not status_match:
        problems.append(Problem(relative, "no Status"))
    else:
        declared = (status_match.group(1) or "").strip()
        if not declared:
            # `## Status` on its own line, with the value underneath.
            after = text[status_match.end() :].strip().splitlines()
            declared = after[0].strip() if after else ""
        if not declared.startswith(ADR_STATUSES):
            problems.append(
                Problem(relative, f"status {declared!r} is not one of {', '.join(ADR_STATUSES)}")
            )

    if not ADR_DATE.search(text):
        problems.append(Problem(relative, "no Date"))

    return problems


def validate(root: Path) -> list[Problem]:
    problems: list[Problem] = []
    seen: dict[str, str] = {}

    for path in sorted((root / SPECS_RELDIR).glob("*.md")):
        relative = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        problems.extend(validate_spec(relative, text))
        meta = frontmatter(text) or {}
        identifier = str(meta.get("id", ""))
        if identifier:
            if identifier in seen:
                problems.append(
                    Problem(relative, f"id {identifier} is already used by {seen[identifier]}")
                )
            seen[identifier] = relative

    for path in sorted((root / ADR_RELDIR).glob("*.md")):
        if path.name == "README.md":
            continue
        problems.extend(
            validate_adr(path.relative_to(root).as_posix(), path.read_text(encoding="utf-8"))
        )

    return problems
