"""Generated projects, verified as projects (#12).

The previous POC kept a second copy of every workflow and script at the
repository root and synchronised it by hand. ADR 0014 replaced that with
rendering, and this file is the other half: what is rendered has to work.

These are marked `slow` -- they render the real template. The full tier runs
them; the fast tier does not.
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

from ai_scheme.cli import main

pytestmark = pytest.mark.slow


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


def create(target: Path, out: Path, *data: str) -> None:
    arguments = ["create", str(target), "--out", str(out)]
    for item in ("project_name=Demo", "project_slug=demo", *data):
        arguments += ["--data", item]
    assert main(arguments) == 0
    assert main(["create", str(target), "--apply-plan", str(out / "plan.json")]) == 0


@pytest.mark.parametrize("languages", ["[]", "[python]"])
def test_a_created_project_passes_its_own_checks(
    tmp_path: Path, languages: str, capsys: pytest.CaptureFixture[str]
) -> None:
    """Docs-only projects are a supported answer, so both are fixtures."""
    target = tmp_path / "project"
    git_init(target)

    create(target, tmp_path / "plan", f"languages={languages}")
    capsys.readouterr()

    # Run the shipped script, not the library: this is the fixture that would
    # have caught a broken `scripts/verify` shim. `ai-scheme` is put on PATH so
    # the script resolves this checkout instead of fetching from git -- pinning
    # that fetch to a release is #6.
    environment = {
        **os.environ,
        "PATH": f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}",
    }
    result = subprocess.run(
        ["scripts/verify", "--tier", "docs"],
        cwd=target,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr

    assert (target / ".scheme" / "config.yml").is_file()
    assert (target / "scripts" / "verify").is_file()
    assert (target / ".github" / "workflows" / "ci.yml").is_file()


def test_adopting_leaves_the_product_alone(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    target = tmp_path / "project"
    git_init(target)
    product = {
        "README.md": "# Our product\n",
        "CHANGELOG.md": "## 1.0.0\n",
        "pyproject.toml": '[project]\nname = "ours"\n',
        "src/product.py": "VALUE = 1\n",
        "tests/test_product.py": "def test_value():\n    assert True\n",
        "docs/adr/0001-record-architecture-decisions.md": "# our own 0001\n",
        "docs/specs/one.md": "# a spec\n",
    }
    for path, text in product.items():
        write(target / path, text)
    commit_all(target)

    out = tmp_path / "plan"
    assert main(["adopt", str(target), "--out", str(out), "--data", "project_name=Demo"]) == 0
    capsys.readouterr()

    for path, text in product.items():
        assert (target / path).read_text() == text, f"{path} was touched by planning"


def test_updating_keeps_a_local_edit_out_of_harm(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """The regression: a project file edited after creation is not overwritten."""
    target = tmp_path / "project"
    git_init(target)
    create(target, tmp_path / "plan")
    write(target / "docs" / "adr" / "0001-record-architecture-decisions.md", "# ours now\n")
    write(target / "AGENTS.md", (target / "AGENTS.md").read_text() + "\nproject-specific rule\n")
    commit_all(target, "adopted")
    capsys.readouterr()

    out = tmp_path / "update-plan"
    assert main(["update", str(target), "--out", str(out)]) == 0
    capsys.readouterr()

    assert main(["update", str(target), "--apply-plan", str(out / "plan.json")]) == 0
    capsys.readouterr()

    assert (target / "docs/adr/0001-record-architecture-decisions.md").read_text() == "# ours now\n"
    assert "project-specific rule" in (target / "AGENTS.md").read_text()


def test_status_walks_create_to_current(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    target = tmp_path / "project"
    git_init(target)

    assert main(["status", str(target), "--no-render"]) == 0
    assert "create" in capsys.readouterr().out

    create(target, tmp_path / "plan")
    capsys.readouterr()

    assert main(["status", str(target), "--no-render"]) == 0
    assert "current" in capsys.readouterr().out
