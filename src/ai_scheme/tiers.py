"""Choosing how much verification a change needs.

One entry point runs locally and in CI (#11). Which stages it runs is a
function of what the change touches, so that a typo fix is not gated on the
same evidence as a change to the template body.

The routing is deliberately conservative: anything this module cannot place
lands in `fast`, and anything that can change what other repositories receive
lands in `full`.
"""

from __future__ import annotations

import subprocess
from collections.abc import Iterable, Sequence
from enum import Enum


class Tier(Enum):
    DOCS = "docs"
    FAST = "fast"
    FULL = "full"

    def includes(self, other: Tier) -> bool:
        order = (Tier.DOCS, Tier.FAST, Tier.FULL)
        return order.index(self) >= order.index(other)


# A change to any of these can alter what a generated project receives, or how
# it is verified. Neither a reviewer nor a test can tell from the diff alone
# that the effect is local, so these always take the full tier.
FULL_TIER_PREFIXES = (
    "copier.yml",
    "ownership.yml",
    "template/",
    ".github/workflows/",
    "policies/",
    "schemas/",
    "scripts/verify",
    "src/",
    "tests/",
    "pyproject.toml",
    "uv.lock",
)

DOCS_SUFFIXES = (".md",)
DOCS_PREFIXES = ("docs/",)


def classify(paths: Iterable[str], *, labels: Sequence[str] = ()) -> Tier:
    """The tier a change touching `paths` needs.

    An empty change list means "something happened that produced no paths" --
    a shallow clone, a tag build, a caller that guessed wrong. That is not a
    licence to skip: it takes the full tier.
    """
    if "hotfix" in labels:
        return Tier.FULL

    paths = [path for path in paths if path]
    if not paths:
        return Tier.FULL

    if any(path.startswith(FULL_TIER_PREFIXES) for path in paths):
        return Tier.FULL

    if all(path.endswith(DOCS_SUFFIXES) or path.startswith(DOCS_PREFIXES) for path in paths):
        return Tier.DOCS

    return Tier.FAST


def changed_paths(base: str = "origin/main", *, cwd: str | None = None) -> list[str]:
    """Paths changed against `base`, or an empty list when git cannot say."""
    command = ["git", "diff", "--name-only", f"{base}...HEAD"]
    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=cwd, check=False)
    except OSError:
        return []
    if result.returncode != 0:
        return []
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]
