"""Workflow pinning, and what the linters are asked (#15)."""

from __future__ import annotations

from pathlib import Path

from ai_scheme import workflows
from ai_scheme.paths import package_root

PINNED = """
jobs:
  a:
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262 # v4
"""

FLOATING = """
jobs:
  a:
    steps:
      - uses: actions/checkout@v4
"""

NO_COMMENT = """
jobs:
  a:
    steps:
      - uses: actions/checkout@11d5960a326750d5838078e36cf38b85af677262
"""

LOCAL = """
jobs:
  a:
    steps:
      - uses: ./.github/actions/setup
      - uses: docker://alpine:3.20
"""


def test_every_shipped_workflow_is_pinned() -> None:
    assert workflows.check_pinning_in(package_root()) == []


def test_a_pinned_use_with_a_version_comment_passes() -> None:
    assert workflows.check_pinning("ci.yml", PINNED) == []


def test_a_floating_tag_is_a_finding() -> None:
    """A tag is a credential handed to whoever can move it."""
    findings = workflows.check_pinning("ci.yml", FLOATING)

    assert len(findings) == 1
    assert "40-character commit SHA" in findings[0].detail
    assert findings[0].line == 5


def test_a_pin_without_a_version_comment_is_a_finding() -> None:
    findings = workflows.check_pinning("ci.yml", NO_COMMENT)

    assert "naming the version" in findings[0].detail


def test_local_and_container_actions_have_nothing_to_pin() -> None:
    assert workflows.check_pinning("ci.yml", LOCAL) == []


def test_workflow_files_finds_both_extensions(tmp_path: Path) -> None:
    directory = tmp_path / ".github" / "workflows"
    directory.mkdir(parents=True)
    (directory / "one.yml").write_text("", encoding="utf-8")
    (directory / "two.yaml").write_text("", encoding="utf-8")

    assert [path.name for path in workflows.workflow_files(tmp_path)] == ["one.yml", "two.yaml"]
