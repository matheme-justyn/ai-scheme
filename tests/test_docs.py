"""Specs and decision records: the layers a machine can still check (#10)."""

from __future__ import annotations

from pathlib import Path

from ai_scheme import docs
from ai_scheme.paths import package_root

GOOD_SPEC = """---
id: SPEC-001
title: A real spec
status: draft
tracking: none
---

# SPEC-001

""" + "\n".join(f"## {section}\n\nsomething\n" for section in docs.SPEC_SECTIONS)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_this_repository_passes() -> None:
    assert docs.validate(package_root()) == []


def test_a_complete_spec_passes() -> None:
    assert docs.validate_spec("docs/specs/SPEC-001-a-real-spec.md", GOOD_SPEC) == []


def test_a_spec_without_frontmatter_is_rejected() -> None:
    problems = docs.validate_spec("docs/specs/SPEC-001-x.md", "# no frontmatter\n")
    assert "no YAML frontmatter" in str(problems[0])


def test_a_missing_section_is_named() -> None:
    without = GOOD_SPEC.replace("## Verification\n\nsomething\n", "")
    problems = docs.validate_spec("docs/specs/SPEC-001-x.md", without)
    assert any("Verification" in str(problem) for problem in problems)


def test_an_unknown_status_is_rejected() -> None:
    odd = GOOD_SPEC.replace("status: draft", "status: probably")
    problems = docs.validate_spec("docs/specs/SPEC-001-x.md", odd)
    assert any("not one of" in str(problem) for problem in problems)


def test_the_id_must_match_the_filename() -> None:
    problems = docs.validate_spec("docs/specs/SPEC-002-x.md", GOOD_SPEC)
    assert any("does not match the filename" in str(problem) for problem in problems)


def test_duplicate_ids_are_caught(tmp_path: Path) -> None:
    write(tmp_path / "docs/specs/SPEC-001-one.md", GOOD_SPEC)
    write(tmp_path / "docs/specs/SPEC-001-two.md", GOOD_SPEC)

    problems = docs.validate(tmp_path)

    assert any("already used by" in str(problem) for problem in problems)


def test_an_adr_needs_a_status_and_a_date() -> None:
    assert docs.validate_adr("docs/adr/0001-x.md", "# 0001\n\nno metadata\n")


def test_both_adr_layouts_are_accepted() -> None:
    modern = "# ADR 0007\n\n**Status**: Accepted\n**Date**: 2026-09-08\n"
    migrated = "# 1. Record decisions\n\nDate: 2026-02-25\n\n## Status\n\nAccepted\n"

    assert docs.validate_adr("docs/adr/0007-x.md", modern) == []
    assert docs.validate_adr("docs/adr/0001-x.md", migrated) == []


def test_an_unknown_adr_status_is_rejected() -> None:
    problems = docs.validate_adr(
        "docs/adr/0007-x.md", "# ADR 0007\n\n**Status**: Probably\n**Date**: 2026-09-08\n"
    )
    assert any("not one of" in str(problem) for problem in problems)
