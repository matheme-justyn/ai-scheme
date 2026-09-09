"""Lifecycle plans: create, adopt, update, and what apply refuses (#5)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from ai_scheme import apply as apply_module
from ai_scheme import ownership, plan
from ai_scheme.cli import main
from ai_scheme.paths import package_root

MANIFEST = ownership.load(package_root())


def git_init(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)


def commit_all(root: Path, message: str = "seed") -> None:
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", message], cwd=root, check=True)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


@pytest.fixture
def rendered(tmp_path: Path) -> Path:
    """A tiny stand-in for a rendering, so the tests stay about classification."""
    root = tmp_path / "rendered"
    write(
        root / "AGENTS.md",
        "# A\n\n<!-- BEGIN ai-scheme:conventions -->\nnew\n<!-- END ai-scheme:conventions -->\n",
    )
    write(root / ".gitignore", "*.log\n.venv/\n")
    write(root / "scripts" / "verify", "#!/usr/bin/env bash\necho new\n")
    write(root / "docs" / "adr" / "0001-record-architecture-decisions.md", "# ADR 0001\n")
    write(root / "src" / "placeholder.py", "PLACEHOLDER = 1\n")
    return root


def test_create_classifies_everything_as_add(tmp_path: Path, rendered: Path) -> None:
    target = tmp_path / "project"
    git_init(target)

    entries = plan.classify(plan.Mode.CREATE, target, rendered, MANIFEST)

    assert {entry.action for entry in entries} == {plan.Action.ADD}


def test_adopt_preserves_the_project_and_flags_the_rest(tmp_path: Path, rendered: Path) -> None:
    """The regression #5 asks for: product files survive adoption."""
    target = tmp_path / "project"
    git_init(target)
    write(target / "src" / "placeholder.py", "REAL_CODE = True\n")
    write(target / "docs" / "adr" / "0001-record-architecture-decisions.md", "# our own 0001\n")
    write(target / "scripts" / "verify", "#!/usr/bin/env bash\necho ours\n")
    write(target / ".gitignore", "node_modules/\n")

    entries = {
        entry.path: entry for entry in plan.classify(plan.Mode.ADOPT, target, rendered, MANIFEST)
    }

    assert entries["src/placeholder.py"].action is plan.Action.PRESERVE
    assert entries["docs/adr/0001-record-architecture-decisions.md"].action is plan.Action.PRESERVE
    assert entries["scripts/verify"].action is plan.Action.MANUAL_MERGE
    assert entries[".gitignore"].action is plan.Action.AUTO_MERGE
    assert entries["AGENTS.md"].action is plan.Action.ADD


def test_update_overwrites_what_was_not_touched_locally(tmp_path: Path, rendered: Path) -> None:
    target = tmp_path / "project"
    git_init(target)
    previous = tmp_path / "previous"
    write(previous / "scripts" / "verify", "#!/usr/bin/env bash\necho old\n")
    write(target / "scripts" / "verify", "#!/usr/bin/env bash\necho old\n")

    entries = {
        entry.path: entry
        for entry in plan.classify(
            plan.Mode.UPDATE, target, rendered, MANIFEST, previous_root=previous
        )
    }

    assert entries["scripts/verify"].action is plan.Action.OVERWRITE


def test_update_will_not_silently_overwrite_a_local_edit(tmp_path: Path, rendered: Path) -> None:
    target = tmp_path / "project"
    git_init(target)
    previous = tmp_path / "previous"
    write(previous / "scripts" / "verify", "#!/usr/bin/env bash\necho old\n")
    write(target / "scripts" / "verify", "#!/usr/bin/env bash\necho mine\n")

    entries = {
        entry.path: entry
        for entry in plan.classify(
            plan.Mode.UPDATE, target, rendered, MANIFEST, previous_root=previous
        )
    }

    assert entries["scripts/verify"].action is plan.Action.MANUAL_MERGE


def test_without_the_previous_rendering_an_update_fails_closed(
    tmp_path: Path, rendered: Path
) -> None:
    target = tmp_path / "project"
    git_init(target)
    write(target / "scripts" / "verify", "#!/usr/bin/env bash\necho mine\n")

    entries = {
        entry.path: entry for entry in plan.classify(plan.Mode.UPDATE, target, rendered, MANIFEST)
    }

    assert entries["scripts/verify"].action is plan.Action.MANUAL_MERGE


def build_plan(target: Path, rendered: Path, mode: plan.Mode = plan.Mode.CREATE) -> plan.Plan:
    return plan.build(
        mode,
        target,
        source=".",
        source_ref=None,
        answers={"project_name": "Demo"},
        rendered_root=rendered,
        manifest=MANIFEST,
    )


def test_apply_writes_adds_and_merges(tmp_path: Path, rendered: Path) -> None:
    target = tmp_path / "project"
    git_init(target)
    write(target / ".gitignore", "node_modules/\n")
    write(
        target / "AGENTS.md",
        "# ours\n\nour rules\n\n"
        "<!-- BEGIN ai-scheme:conventions -->\nold\n<!-- END ai-scheme:conventions -->\n",
    )
    commit_all(target)

    built = build_plan(target, rendered)
    applied = apply_module.apply_plan(
        built, target, rendered, blocks={"AGENTS.md": "ai-scheme:conventions"}
    )

    assert "scripts/verify" in applied.written
    assert "node_modules/" in (target / ".gitignore").read_text()
    assert "*.log" in (target / ".gitignore").read_text()
    agents = (target / "AGENTS.md").read_text()
    assert "our rules" in agents and "new" in agents and "old" not in agents


def test_apply_refuses_when_head_moved(tmp_path: Path, rendered: Path) -> None:
    target = tmp_path / "project"
    git_init(target)
    write(target / "README.md", "one\n")
    commit_all(target)
    built = build_plan(target, rendered)
    write(target / "README.md", "two\n")
    commit_all(target, "second")

    with pytest.raises(apply_module.ApplyRefused) as refused:
        apply_module.apply_plan(built, target, rendered, blocks={})

    assert any("HEAD moved" in reason for reason in refused.value.reasons)


def test_apply_refuses_when_the_target_became_dirty(tmp_path: Path, rendered: Path) -> None:
    target = tmp_path / "project"
    git_init(target)
    write(target / "README.md", "one\n")
    commit_all(target)
    built = build_plan(target, rendered)
    write(target / "README.md", "edited after planning\n")

    with pytest.raises(apply_module.ApplyRefused) as refused:
        apply_module.apply_plan(built, target, rendered, blocks={})

    assert any("newly uncommitted" in reason for reason in refused.value.reasons)


def test_apply_refuses_on_manual_merge(tmp_path: Path, rendered: Path) -> None:
    target = tmp_path / "project"
    git_init(target)
    write(target / "scripts" / "verify", "#!/usr/bin/env bash\necho mine\n")
    commit_all(target)

    built = build_plan(target, rendered, plan.Mode.ADOPT)

    with pytest.raises(apply_module.ApplyRefused) as refused:
        apply_module.apply_plan(built, target, rendered, blocks={})

    assert "manual merge" in refused.value.reasons[0]


def test_apply_refuses_on_conflict_markers(tmp_path: Path, rendered: Path) -> None:
    target = tmp_path / "project"
    git_init(target)
    write(target / "scripts" / "verify", "<<<<<<< HEAD\nours\n=======\ntheirs\n>>>>>>> them\n")
    commit_all(target)
    built = build_plan(target, rendered)
    built.entries = [
        entry
        if entry.path != "scripts/verify"
        else plan.Entry(entry.path, plan.Action.OVERWRITE, entry.kind, "forced for the test")
        for entry in built.entries
    ]

    with pytest.raises(apply_module.ApplyRefused) as refused:
        apply_module.apply_plan(built, target, rendered, blocks={})

    assert any("conflict markers" in reason for reason in refused.value.reasons)


def test_a_rej_file_stops_the_apply(tmp_path: Path, rendered: Path) -> None:
    target = tmp_path / "project"
    git_init(target)
    write(target / "scripts" / "verify.rej", "rejected hunk\n")
    write(target / "scripts" / "verify", "#!/usr/bin/env bash\necho new\n")
    commit_all(target)
    built = build_plan(target, rendered)

    with pytest.raises(apply_module.ApplyRefused) as refused:
        apply_module.apply_plan(built, target, rendered, blocks={})

    assert any(".rej" in reason for reason in refused.value.reasons)


def test_union_never_removes_a_line() -> None:
    merged = apply_module.union_lines("node_modules/\n", "*.log\nnode_modules/\n")

    assert "node_modules/" in merged
    assert "*.log" in merged
    assert merged.count("node_modules/") == 1


def test_plan_round_trips_through_json(tmp_path: Path, rendered: Path) -> None:
    target = tmp_path / "project"
    git_init(target)
    built = build_plan(target, rendered)

    restored = plan.Plan.from_dict(json.loads(built.to_json()))

    assert restored.as_dict() == built.as_dict()


def test_the_report_names_what_needs_a_human(tmp_path: Path, rendered: Path) -> None:
    target = tmp_path / "project"
    git_init(target)
    write(target / "scripts" / "verify", "#!/usr/bin/env bash\necho mine\n")
    built = build_plan(target, rendered, plan.Mode.ADOPT)

    report = built.report()

    assert "manual-merge (1)" in report
    assert "scripts/verify" in report


def test_create_then_status_reports_current(tmp_path: Path) -> None:
    """The fast tier's create smoke: one language, real template, end to end."""
    target = tmp_path / "project"
    git_init(target)
    out = tmp_path / "plan"

    assert (
        main(
            [
                "create",
                str(target),
                "--data",
                "project_name=Demo",
                "--data",
                "project_slug=demo",
                "--out",
                str(out),
            ]
        )
        == 0
    )
    assert main(["create", str(target), "--apply-plan", str(out / "plan.json")]) == 0

    assert (target / ".scheme" / "config.yml").is_file()
    assert (target / "scripts" / "verify").is_file()
    assert main(["status", str(target), "--no-render", "--json"]) == 0


def test_the_plan_reports_the_previous_layout(tmp_path: Path, rendered: Path) -> None:
    """`migrate` in #4's language: the sentinel is read, reported, never written."""
    target = tmp_path / "project"
    git_init(target)
    write(target / ".template-version", "4.0.2\n")

    built = build_plan(target, rendered, plan.Mode.ADOPT)

    assert built.legacy == [".template-version"]
    assert "previous layout" in built.report()
    assert (target / ".template-version").read_text() == "4.0.2\n"
