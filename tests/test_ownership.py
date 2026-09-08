"""The ownership manifest and everything generated from it."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from ai_scheme import ownership
from ai_scheme.paths import UNINSTALL_RELPATH, package_root

MINIMAL = {
    "version": 1,
    "kinds": {
        "template": {"update": "overwrite"},
        "project": {"update": "never-touch"},
        "managed-block": {"update": "replace-block"},
        "merge": {"update": "union"},
        "generated": {"update": "regenerate"},
    },
    "template_repo_only": ["copier.yml"],
    "paths": [
        {"path": "scripts/", "kind": "template"},
        {"path": "src/", "kind": "project"},
        {"path": "AGENTS.md", "kind": "managed-block", "block": "ai-scheme:conventions"},
        {"path": ".gitignore", "kind": "merge"},
        {"path": "README.md", "kind": "generated", "source": "i18n/"},
    ],
}


@pytest.fixture
def manifest() -> ownership.Manifest:
    return ownership.load(package_root())


def test_repo_manifest_parses(manifest: ownership.Manifest) -> None:
    assert manifest.entries
    assert manifest.template_repo_only


def test_every_kind_is_declared_before_use(manifest: ownership.Manifest) -> None:
    for entry in manifest.entries:
        assert entry.kind in manifest.kinds


def test_unknown_kind_is_rejected() -> None:
    raw = {**MINIMAL, "paths": [{"path": "x", "kind": "invented"}]}
    with pytest.raises(ownership.OwnershipError, match="unknown kind"):
        ownership.parse(raw)


def test_duplicate_path_is_rejected() -> None:
    raw = {
        **MINIMAL,
        "paths": [{"path": "x", "kind": "template"}, {"path": "x", "kind": "project"}],
    }
    with pytest.raises(ownership.OwnershipError, match="declared more than once"):
        ownership.parse(raw)


def test_managed_block_must_name_its_block() -> None:
    raw = {**MINIMAL, "paths": [{"path": "AGENTS.md", "kind": "managed-block"}]}
    with pytest.raises(ownership.OwnershipError, match="declares no `block`"):
        ownership.parse(raw)


def test_generated_must_name_its_source() -> None:
    raw = {**MINIMAL, "paths": [{"path": "README.md", "kind": "generated"}]}
    with pytest.raises(ownership.OwnershipError, match="declares no `source`"):
        ownership.parse(raw)


def test_skip_if_exists_covers_exactly_the_project_kind() -> None:
    """copier can express "seed once" and nothing else.

    managed-block, merge and generated paths are deliberately absent: copier
    would either clobber them or freeze them, and both are wrong. The CLI
    reconciles those kinds itself.
    """
    parsed = ownership.parse(MINIMAL)
    block = ownership.copier_block(parsed)
    skip = block.split("_skip_if_exists:")[1]
    assert "src/" in skip
    for path in ("AGENTS.md", ".gitignore", "README.md", "scripts/"):
        assert path not in skip


def test_copier_block_is_sorted_and_stable() -> None:
    parsed = ownership.parse(MINIMAL)
    assert ownership.copier_block(parsed) == ownership.copier_block(parsed)


def test_sync_copier_replaces_only_the_marked_region() -> None:
    text = (
        "questions: here\n"
        f"{ownership.BEGIN_MARKER}\n"
        "_exclude:\n  - stale\n"
        f"{ownership.END_MARKER}\n"
        "trailing: kept\n"
    )
    result = ownership.sync_copier(text, ownership.parse(MINIMAL))
    assert result.startswith("questions: here\n")
    assert result.endswith("trailing: kept\n")
    assert "stale" not in result
    assert "copier.yml" in result


def test_sync_copier_without_markers_is_an_error() -> None:
    with pytest.raises(ownership.OwnershipError, match="no ownership-derived region"):
        ownership.sync_copier("no markers here\n", ownership.parse(MINIMAL))


def test_generated_files_are_in_sync_with_the_manifest(manifest: ownership.Manifest) -> None:
    """The check `ai-scheme ownership sync --check` runs in CI; this is its unit form."""
    root = package_root()
    copier_text = (root / "copier.yml").read_text(encoding="utf-8")
    assert ownership.sync_copier(copier_text, manifest) == copier_text

    uninstall = (root / UNINSTALL_RELPATH).read_text(encoding="utf-8")
    assert ownership.uninstall_doc(manifest) == uninstall


def test_uninstall_doc_places_every_entry_in_exactly_one_group() -> None:
    parsed = ownership.parse(MINIMAL)
    doc = ownership.uninstall_doc(parsed)
    for entry in parsed.entries:
        assert doc.count(f"| `{entry.path}` |") == 1


def test_uninstall_doc_keeps_project_owned_paths_out_of_the_delete_group() -> None:
    doc = ownership.uninstall_doc(ownership.parse(MINIMAL))
    delete_section = doc.split("## Remove only the template's part")[0]
    assert "`src/`" not in delete_section


def test_uninstall_doc_says_the_mechanism_config_is_not_ours() -> None:
    """A user uninstalling the skeleton must not be told to delete ai-zpd's file."""
    doc = ownership.uninstall_doc(ownership.parse(MINIMAL))
    assert "config.toml" in doc
    assert "ADR 0008" in doc


def test_load_missing_manifest(tmp_path: Path) -> None:
    with pytest.raises(ownership.OwnershipError, match="not found"):
        ownership.load(tmp_path)


def test_load_rejects_bad_yaml(tmp_path: Path) -> None:
    (tmp_path / "ownership.yml").write_text("a: [\n", encoding="utf-8")
    with pytest.raises(ownership.OwnershipError, match="not valid YAML"):
        ownership.load(tmp_path)


def test_manifest_yaml_has_no_tabs() -> None:
    raw = (package_root() / "ownership.yml").read_text(encoding="utf-8")
    assert "\t" not in raw
    yaml.safe_load(raw)
