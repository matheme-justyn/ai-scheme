"""Finding writes to the pull request control plane that skip the lease (#19).

The carrier only helps if everything that writes goes through it. This scans
the two places a write can hide -- workflows and scripts -- and fails closed:
an unrecognised write is a finding, and an exception is an exact path with an
issue number next to it.

It is deliberately fussy about what counts. The previous POC's version matched
inside documentation and comments, so it fired on prose describing the very
rule it was enforcing; a check that cries wolf gets switched off. Comments and
fenced examples do not count here, and the patterns are anchored so that a
word like `gh pr view` (a read) is not mistaken for a write.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

EXCEPTIONS_RELPATH = Path("policies/lease-exceptions.json")

SCAN_GLOBS = (".github/workflows/*.yml", ".github/workflows/*.yaml", "scripts/*")

# `gh pr` subcommands that change state. `view`, `list`, `checks` and `diff`
# read, and are not listed.
GH_PR_WRITE = re.compile(r"\bgh\s+pr\s+(ready|edit|merge|close|reopen|review)\b")
REST_WRITE = re.compile(
    r"""\bgh\s+api\b[^\n]*?(?:--method|-X)\s+(?:PATCH|POST|PUT|DELETE)[^\n]*?/pulls/""",
    re.IGNORECASE,
)
GRAPHQL_WRITE = re.compile(
    r"\b(mergePullRequest|markPullRequestReadyForReview|convertPullRequestToDraft"
    r"|addLabelsToLabelable|removeLabelsFromLabelable)\b"
)

PATTERNS = (
    ("gh pr write", GH_PR_WRITE),
    ("REST write to /pulls/", REST_WRITE),
    ("GraphQL pull request mutation", GRAPHQL_WRITE),
)


@dataclass(frozen=True)
class Write:
    path: str
    line: int
    kind: str
    text: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: {self.kind} without a lease -- {self.text.strip()}"


def load_exceptions(root: Path) -> dict[str, str]:
    """Exact path -> the issue that tracks it. No globs, on purpose."""
    path = root / EXCEPTIONS_RELPATH
    if not path.is_file():
        return {}
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {
        entry["path"]: entry["issue"]
        for entry in raw.get("exceptions", [])
        if entry.get("path") and entry.get("issue")
    }


def code_lines(text: str) -> list[tuple[int, str]]:
    """Lines with comments and fenced blocks removed.

    A rule written down in a comment is documentation, not a call.
    """
    kept: list[tuple[int, str]] = []
    fenced = False
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith(("```", "~~~")):
            fenced = not fenced
            continue
        if fenced or stripped.startswith("#"):
            continue
        code = line.split(" #", 1)[0]
        # Text inside backticks is prose about a command, not the command.
        code = re.sub(r"`[^`]*`", "", code)
        kept.append((number, code))
    return kept


def scan_file(relative: str, text: str) -> list[Write]:
    found: list[Write] = []
    for number, line in code_lines(text):
        for kind, pattern in PATTERNS:
            if pattern.search(line):
                found.append(Write(relative, number, kind, line))
                break
    return found


def scan(root: Path) -> list[Write]:
    exceptions = load_exceptions(root)
    findings: list[Write] = []
    for glob in SCAN_GLOBS:
        for path in sorted(root.glob(glob)):
            if not path.is_file():
                continue
            relative = path.relative_to(root).as_posix()
            if relative in exceptions:
                continue
            findings.extend(scan_file(relative, path.read_text(encoding="utf-8", errors="replace")))
    return findings
