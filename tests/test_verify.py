"""The verification stages (#11)."""

from __future__ import annotations

from pathlib import Path

from ai_scheme import verify
from ai_scheme.tiers import Tier


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_stages_grow_with_the_tier() -> None:
    docs = [stage.name for stage in verify.stages_for(Tier.DOCS)]
    full = [stage.name for stage in verify.stages_for(Tier.FULL)]
    assert docs == ["static", "docs", "issues"]
    assert full == ["static", "docs", "issues", "python", "template", "dependencies"]


def test_prose_only_blanks_fenced_blocks() -> None:
    text = "\n".join(
        [
            "real [link](./there.md)",
            "```markdown",
            "sample [link](./nowhere.md)",
            "```",
            "another [link](./here.md)",
        ]
    )
    stripped = verify.prose_only(text)
    assert "./there.md" in stripped
    assert "./here.md" in stripped
    assert "./nowhere.md" not in stripped


def test_docs_stage_finds_a_dangling_link(tmp_path: Path) -> None:
    """The deliberately broken fixture #11 asks for."""
    write(tmp_path / "docs" / "a.md", "see [the guide](./missing.md)\n")

    result = verify.stage_docs(tmp_path)

    assert not result.ok
    assert result.findings == ("docs/a.md -> ./missing.md",)


def test_docs_stage_accepts_a_link_that_resolves(tmp_path: Path) -> None:
    write(tmp_path / "docs" / "a.md", "see [the guide](./b.md)\n")
    write(tmp_path / "docs" / "b.md", "here\n")

    assert verify.stage_docs(tmp_path).ok


def test_docs_stage_honours_the_policy_file(tmp_path: Path) -> None:
    write(tmp_path / "docs" / "a.md", "see [later](./RELEASE_PROCESS.md) and [example](./x.md)\n")
    write(
        tmp_path / "policies" / "docs-links.yml",
        "forward_references:\n"
        "  - target: RELEASE_PROCESS.md\n"
        "    reason: not written yet\n"
        "illustrative:\n"
        "  - path: docs/b.md\n"
        "    reason: describes the reader's project\n",
    )
    write(tmp_path / "docs" / "b.md", "see [nothing](./nowhere.md)\n")

    result = verify.stage_docs(tmp_path)

    assert result.findings == ("docs/a.md -> ./x.md",)


def test_template_stage_is_not_applicable_to_a_generated_project(tmp_path: Path) -> None:
    result = verify.stage_template(tmp_path)

    assert result.ok
    assert "not a template repository" in result.detail


def test_report_lines_name_the_failing_stage() -> None:
    report = verify.Report(tier=Tier.DOCS)
    stage = verify.STAGES[0]
    report.results.append((stage, verify.StageResult(False, "broke", ("one finding",))))

    lines = report.lines()

    assert not report.ok
    assert lines[0] == "tier: docs"
    assert lines[1].startswith("FAIL static: broke")
    assert "one finding" in lines[2]
