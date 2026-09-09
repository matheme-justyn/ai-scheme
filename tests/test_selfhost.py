"""The repository renders its own skeleton from template/ -- ADR 0014."""

from __future__ import annotations

from pathlib import Path

import pytest

from ai_scheme import ownership, selfhost
from ai_scheme.paths import ANSWERS_RELPATH, package_root

REPO_ROOT = package_root()


@pytest.fixture(scope="module")
def rendered() -> Path:
    with selfhost.render_to_temp(REPO_ROOT) as handle:
        yield Path(handle) / "rendered"


def test_answers_for_rendering_drops_the_keys_copier_owns() -> None:
    answers = selfhost.answers_for_rendering(REPO_ROOT)
    assert not [key for key in answers if key.startswith("_")]
    assert answers["project_slug"] == "ai-scheme"


def test_the_working_tree_matches_the_template(rendered: Path) -> None:
    """The whole point of ADR 0014: no second copy to drift."""
    assert selfhost.compare(REPO_ROOT, rendered) == []


def test_the_answers_file_is_never_compared(rendered: Path) -> None:
    """Copier rewrites it on every run; a diff there could never be resolved."""
    assert ANSWERS_RELPATH.as_posix() in selfhost.UNCOMPARED


def test_answers_drive_which_optional_files_render(rendered: Path) -> None:
    answers = selfhost.answers_for_rendering(REPO_ROOT)
    assert answers["enable_academic_docs"] is False
    assert not (rendered / "docs/guides/ACADEMIC_WRITING.md").exists()
    assert (rendered / "docs/guides/STYLE_GUIDE.md").is_file()

    assert answers["terminology_domains"] == ["software"]
    assert (rendered / "docs/terminology/software").is_dir()
    assert not (rendered / "docs/terminology/academic").exists()


def test_every_rendered_path_is_declared_in_the_manifest(rendered: Path) -> None:
    """A file that ships without an owner cannot be updated or uninstalled."""
    manifest = ownership.load(REPO_ROOT)
    declared = [entry.path for entry in manifest.entries]
    undeclared = []
    for path in sorted(rendered.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(rendered).as_posix()
        owned = any(
            relative == entry or (entry.endswith("/") and relative.startswith(entry))
            for entry in declared
        )
        if not owned:
            undeclared.append(relative)
    assert undeclared == []


def test_compare_reports_missing_and_changed_files(tmp_path: Path) -> None:
    rendered_root = tmp_path / "rendered"
    tree = tmp_path / "tree"
    (rendered_root / "docs").mkdir(parents=True)
    tree.mkdir()
    (rendered_root / "same.md").write_text("same\n")
    (rendered_root / "docs" / "changed.md").write_text("template\n")
    (rendered_root / "docs" / "gone.md").write_text("template\n")
    (tree / "same.md").write_text("same\n")
    (tree / "docs").mkdir()
    (tree / "docs" / "changed.md").write_text("edited by hand\n")

    differences = selfhost.compare(tree, rendered_root)

    assert [str(difference) for difference in differences] == [
        "different: docs/changed.md",
        "missing: docs/gone.md",
    ]


def test_apply_writes_every_rendered_path(tmp_path: Path) -> None:
    rendered_root = tmp_path / "rendered"
    tree = tmp_path / "tree"
    (rendered_root / "docs").mkdir(parents=True)
    tree.mkdir()
    (rendered_root / "docs" / "new.md").write_text("from the template\n")

    written = selfhost.apply(tree, rendered_root)

    assert written == ["docs/new.md"]
    assert (tree / "docs" / "new.md").read_text() == "from the template\n"
    assert selfhost.compare(tree, rendered_root) == []


def test_managed_block_files_are_compared_block_for_block(tmp_path: Path) -> None:
    """A project's own instructions must survive an update -- ADR 0008."""
    rendered_root = tmp_path / "rendered"
    tree = tmp_path / "tree"
    rendered_root.mkdir()
    tree.mkdir()
    (tree / "ownership.yml").write_text(
        "version: 1\n"
        "kinds:\n"
        "  managed-block:\n"
        "    update: replace-block\n"
        "paths:\n"
        "  - path: AGENTS.md\n"
        "    kind: managed-block\n"
        "    block: ai-scheme:conventions\n",
        encoding="utf-8",
    )
    block = (
        "<!-- BEGIN ai-scheme:conventions -->\n"
        "run scripts/verify\n"
        "<!-- END ai-scheme:conventions -->"
    )
    (rendered_root / "AGENTS.md").write_text(f"# Title\n\n{block}\n", encoding="utf-8")
    (tree / "AGENTS.md").write_text(
        f"# This project\n\nour own rules\n\n{block}\n", encoding="utf-8"
    )

    blocks = selfhost.managed_blocks(tree)
    assert blocks == {"AGENTS.md": "ai-scheme:conventions"}
    # The prose differs, the block does not: nothing to report.
    assert selfhost.compare(tree, rendered_root) == []


def test_replace_block_keeps_the_project_prose(tmp_path: Path) -> None:
    current = (
        "# This project\n\nour own rules\n\n"
        "<!-- BEGIN ai-scheme:conventions -->\nold\n<!-- END ai-scheme:conventions -->\n"
    )
    rendered = (
        "# Anything\n\n"
        "<!-- BEGIN ai-scheme:conventions -->\nnew\n<!-- END ai-scheme:conventions -->\n"
    )

    merged = selfhost.replace_block(current, rendered, "ai-scheme:conventions")

    assert "our own rules" in merged
    assert "new" in merged
    assert "old" not in merged
