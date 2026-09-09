"""Tier routing: what a change touches decides how much is run (#11)."""

from __future__ import annotations

import pytest

from ai_scheme.tiers import Tier, classify

CASES = [
    (["docs/guides/STYLE_GUIDE.md"], Tier.DOCS),
    (["README.md", "docs/adr/0001-record-architecture-decisions.md"], Tier.DOCS),
    (["LICENSE"], Tier.FAST),
    (["languages/python/pyproject.toml"], Tier.FAST),
    (["src/ai_scheme/cli.py"], Tier.FULL),
    (["template/docs/guides/STYLE_GUIDE.md"], Tier.FULL),
    (["copier.yml"], Tier.FULL),
    ([".github/workflows/ci.yml"], Tier.FULL),
    (["policies/docs-links.yml"], Tier.FULL),
    (["scripts/verify"], Tier.FULL),
    (["docs/guides/STYLE_GUIDE.md", "src/ai_scheme/verify.py"], Tier.FULL),
]


@pytest.mark.parametrize(("paths", "expected"), CASES)
def test_classify(paths: list[str], expected: Tier) -> None:
    assert classify(paths) is expected


def test_no_paths_fails_closed() -> None:
    """A change nobody can describe is not a change nobody has to check."""
    assert classify([]) is Tier.FULL


def test_hotfix_label_forces_the_full_tier() -> None:
    assert classify(["docs/guides/STYLE_GUIDE.md"], labels=["hotfix"]) is Tier.FULL


def test_tiers_are_ordered() -> None:
    assert Tier.FULL.includes(Tier.DOCS)
    assert Tier.FAST.includes(Tier.DOCS)
    assert not Tier.DOCS.includes(Tier.FAST)
