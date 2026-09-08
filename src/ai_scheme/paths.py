"""Locating the answers file, the schema and the ownership manifest.

Kept separate so that tests can point the loaders at a fixture directory
without monkeypatching module globals.
"""

from __future__ import annotations

from pathlib import Path

ANSWERS_RELPATH = Path(".scheme/config.yml")
# The template body. This repository renders it over its own tree (ADR 0014),
# so generated artefacts are written here, not into the rendered copy.
TEMPLATE_RELPATH = Path("template")
UNINSTALL_RELPATH = TEMPLATE_RELPATH / "docs" / "uninstall.md"
OWNERSHIP_RELPATH = Path("ownership.yml")
SCHEMA_RELPATH = Path("schemas/scheme-config.schema.json")

# The config.toml a project gets from ai-zpd. This layer detects it so that
# `status` and `adopt` can report it, and never reads its contents -- see
# ADR 0008.
MECHANISM_CONFIG_RELPATH = Path("config.toml")


def repo_root(start: Path | None = None) -> Path:
    """Walk up from `start` to the nearest directory containing a .git entry.

    Falls back to `start` itself so that callers working in an unpacked
    archive still get a usable answer rather than an exception.
    """
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return current


def package_root() -> Path:
    """The installed template's own root, used to find the bundled schema."""
    return Path(__file__).resolve().parent.parent.parent
