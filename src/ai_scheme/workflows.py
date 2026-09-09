"""Auditing the workflows themselves (#15).

Three separate questions, three tools, on purpose. actionlint asks whether the
workflow is valid; zizmor asks whether it is dangerous; the pinning check asks
whether it will still be the same code tomorrow.

A floating tag is a credential handed to whoever can move it. `actions/checkout@v4`
is a promise by GitHub about a name, not about a commit -- and the supply-chain
attacks worth worrying about are exactly the ones that move a name.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

WORKFLOW_GLOBS = (".github/workflows/*.yml", ".github/workflows/*.yaml")

USES = re.compile(r"^\s*(?:-\s*)?uses:\s*(?P<ref>[^\s#]+)\s*(?P<comment>#.*)?$")
SHA = re.compile(r"^[0-9a-f]{40}$")

# A local action (`./.github/actions/x`) and a container action are not
# fetched from a moving ref, so they have nothing to pin.
LOCAL = ("./", "docker://")


@dataclass(frozen=True)
class Unpinned:
    path: str
    line: int
    ref: str
    detail: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.ref} -- {self.detail}"


def check_pinning(relative: str, text: str) -> list[Unpinned]:
    findings: list[Unpinned] = []
    for number, line in enumerate(text.splitlines(), start=1):
        match = USES.match(line)
        if not match:
            continue
        ref = match.group("ref").strip("\"'")
        if ref.startswith(LOCAL):
            continue
        _, separator, version = ref.partition("@")
        if not separator:
            findings.append(Unpinned(relative, number, ref, "no ref at all"))
            continue
        if not SHA.match(version):
            findings.append(Unpinned(relative, number, ref, "pin to a 40-character commit SHA"))
            continue
        if not (match.group("comment") or "").strip():
            findings.append(Unpinned(relative, number, ref, "add a comment naming the version"))
    return findings


def check_pinning_in(root: Path) -> list[Unpinned]:
    findings: list[Unpinned] = []
    for glob in WORKFLOW_GLOBS:
        for path in sorted(root.glob(glob)):
            findings.extend(
                check_pinning(path.relative_to(root).as_posix(), path.read_text(encoding="utf-8"))
            )
    return findings


def workflow_files(root: Path) -> list[Path]:
    found: list[Path] = []
    for glob in WORKFLOW_GLOBS:
        found.extend(sorted(root.glob(glob)))
    return found
