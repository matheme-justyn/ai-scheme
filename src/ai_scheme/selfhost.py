"""Applying this template to the repository that ships it.

ADR 0014: the skeleton files in this repository's own tree are the rendered
output of `template/`, not a second hand-maintained copy. Nothing checks a
paired-file list, because there is no pair -- there is one source and one
rendering of it, and this module is what compares them.

`check` renders the template with this repository's answers and reports every
path that differs. `apply` writes the rendering into the working tree.
"""

from __future__ import annotations

import filecmp
import shutil
import tempfile
import warnings
from collections.abc import Iterator
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from ai_scheme import config
from ai_scheme.paths import ANSWERS_RELPATH

# Copier owns the answers file: it rewrites it on every run with its own header
# and a _commit line. Comparing it would report a difference that no edit can
# ever resolve.
UNCOMPARED = frozenset({ANSWERS_RELPATH.as_posix()})


class SelfHostError(Exception):
    """Raised when the rendering cannot be produced or compared."""


class Status(Enum):
    MISSING = "missing"
    DIFFERENT = "different"


@dataclass(frozen=True)
class Difference:
    path: str
    status: Status

    def __str__(self) -> str:
        return f"{self.status.value}: {self.path}"


def answers_for_rendering(root: Path) -> dict[str, Any]:
    """This repository's answers, minus the keys Copier maintains itself."""
    answers = config.load_answers(root)
    return {key: value for key, value in answers.items() if not key.startswith("_")}


def render(root: Path, destination: Path) -> None:
    """Render `template/` into `destination` using this repository's answers."""
    try:
        from copier import run_copy
        from copier._vcs import DirtyLocalWarning
    except ImportError as exc:  # pragma: no cover - copier is a hard dependency
        raise SelfHostError(f"copier is not installed: {exc}") from exc

    # Rendering the working tree rather than the last commit is the point of
    # this command: it answers "does what I am about to commit still produce
    # the tree I am committing?". Copier warns about it every time; the warning
    # would be the only thing a clean run printed.
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=DirtyLocalWarning)
        run_copy(
            str(root),
            str(destination),
            data=answers_for_rendering(root),
            defaults=True,
            overwrite=True,
            quiet=True,
            vcs_ref=None,
        )


def _rendered_files(rendered_root: Path) -> Iterator[Path]:
    for path in sorted(rendered_root.rglob("*")):
        if path.is_file():
            yield path


def compare(root: Path, rendered_root: Path) -> list[Difference]:
    """Every rendered path that the working tree does not already match."""
    differences: list[Difference] = []
    for rendered in _rendered_files(rendered_root):
        relative = rendered.relative_to(rendered_root).as_posix()
        if relative in UNCOMPARED:
            continue
        actual = root / relative
        if not actual.is_file():
            differences.append(Difference(relative, Status.MISSING))
        elif not filecmp.cmp(rendered, actual, shallow=False):
            differences.append(Difference(relative, Status.DIFFERENT))
    return differences


def apply(root: Path, rendered_root: Path) -> list[str]:
    """Copy the rendering over the working tree. Returns the paths written."""
    written: list[str] = []
    for rendered in _rendered_files(rendered_root):
        relative = rendered.relative_to(rendered_root).as_posix()
        if relative in UNCOMPARED:
            continue
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(rendered, destination)
        written.append(relative)
    return written


def render_to_temp(root: Path) -> tempfile.TemporaryDirectory[str]:
    """Render into a temporary directory the caller is responsible for closing."""
    handle = tempfile.TemporaryDirectory(prefix="ai-scheme-selfhost-")
    try:
        render(root, Path(handle.name) / "rendered")
    except Exception:
        handle.cleanup()
        raise
    return handle
