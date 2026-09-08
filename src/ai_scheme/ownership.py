"""The ownership manifest, and the artefacts derived from it.

ownership.yml says who owns each path in a generated project. Three things are
generated from it rather than restated by hand:

- copier.yml's _exclude and _skip_if_exists
- docs/uninstall.md
- the adopt report and the update conflict rules (both still to come)

ADR 0008 is the reason this is data instead of Jinja conditions: a human has to
be able to read the list, and three consumers have to share one copy of it.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from ai_scheme.paths import OWNERSHIP_RELPATH

BEGIN_MARKER = "# BEGIN ai-scheme:ownership-derived"
END_MARKER = "# END ai-scheme:ownership-derived"

# copier can express "seed once, never touch again" and nothing else. The other
# kinds need the update logic in this package, so they are deliberately absent
# from _skip_if_exists -- listing them there would make copier skip paths the
# CLI still has to reconcile.
COPIER_SKIP_KINDS = frozenset({"project"})


class OwnershipError(Exception):
    """Raised when the manifest is missing, unreadable or inconsistent."""


@dataclass(frozen=True)
class Entry:
    path: str
    kind: str
    note: str | None = None
    block: str | None = None
    source: str | None = None

    @property
    def is_directory(self) -> bool:
        return self.path.endswith("/")


@dataclass(frozen=True)
class Manifest:
    version: int
    kinds: dict[str, dict[str, Any]]
    template_repo_only: tuple[str, ...]
    entries: tuple[Entry, ...]

    def by_kind(self, kind: str) -> tuple[Entry, ...]:
        return tuple(entry for entry in self.entries if entry.kind == kind)


def load(project_root: Path) -> Manifest:
    manifest_path = project_root / OWNERSHIP_RELPATH
    if not manifest_path.is_file():
        raise OwnershipError(f"ownership manifest not found: {manifest_path}")
    try:
        raw = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise OwnershipError(f"{manifest_path} is not valid YAML: {exc}") from exc
    return parse(raw, source=str(manifest_path))


def parse(raw: Any, source: str = "ownership.yml") -> Manifest:
    if not isinstance(raw, dict):
        raise OwnershipError(f"{source}: top level must be a mapping")

    kinds = raw.get("kinds")
    if not isinstance(kinds, dict) or not kinds:
        raise OwnershipError(f"{source}: `kinds` must be a non-empty mapping")

    raw_paths = raw.get("paths")
    if not isinstance(raw_paths, list) or not raw_paths:
        raise OwnershipError(f"{source}: `paths` must be a non-empty list")

    entries: list[Entry] = []
    seen: set[str] = set()
    for index, item in enumerate(raw_paths):
        if not isinstance(item, dict):
            raise OwnershipError(f"{source}: paths[{index}] must be a mapping")
        path = item.get("path")
        kind = item.get("kind")
        if not isinstance(path, str) or not path:
            raise OwnershipError(f"{source}: paths[{index}] is missing `path`")
        if kind not in kinds:
            raise OwnershipError(
                f"{source}: paths[{index}] ({path}) has unknown kind {kind!r}; "
                f"known kinds are {', '.join(sorted(kinds))}"
            )
        if path in seen:
            raise OwnershipError(f"{source}: {path} is declared more than once")
        seen.add(path)
        if kind == "managed-block" and not item.get("block"):
            raise OwnershipError(f"{source}: {path} is managed-block but declares no `block`")
        if kind == "generated" and not item.get("source"):
            raise OwnershipError(f"{source}: {path} is generated but declares no `source`")
        entries.append(
            Entry(
                path=path,
                kind=kind,
                note=item.get("note"),
                block=item.get("block"),
                source=item.get("source"),
            )
        )

    repo_only = raw.get("template_repo_only") or []
    if not isinstance(repo_only, list) or not all(isinstance(p, str) for p in repo_only):
        raise OwnershipError(f"{source}: `template_repo_only` must be a list of strings")

    return Manifest(
        version=int(raw.get("version", 1)),
        kinds=kinds,
        template_repo_only=tuple(repo_only),
        entries=tuple(entries),
    )


def copier_block(manifest: Manifest) -> str:
    """Render the generated region of copier.yml.

    Sorted so that regenerating after an unrelated manifest edit produces no
    spurious diff.
    """
    lines = [BEGIN_MARKER, "_exclude:"]
    lines.extend(f"  - {path}" for path in sorted(manifest.template_repo_only))
    lines.append("_skip_if_exists:")
    skip = sorted(entry.path for entry in manifest.entries if entry.kind in COPIER_SKIP_KINDS)
    lines.extend(f"  - {path}" for path in skip)
    lines.append(END_MARKER)
    return "\n".join(lines) + "\n"


def sync_copier(copier_text: str, manifest: Manifest) -> str:
    """Replace the generated region of copier.yml, leaving the rest alone."""
    pattern = re.compile(
        rf"^{re.escape(BEGIN_MARKER)}$.*?^{re.escape(END_MARKER)}$\n?",
        re.DOTALL | re.MULTILINE,
    )
    if not pattern.search(copier_text):
        raise OwnershipError(
            "copier.yml has no ownership-derived region; "
            f"expected a block delimited by {BEGIN_MARKER!r} and {END_MARKER!r}"
        )
    return pattern.sub(copier_block(manifest), copier_text)


_UNINSTALL_GROUPS = (
    (
        "Safe to delete outright",
        ("template", "generated"),
        "The template put these here and nothing else did. Removing them removes the skeleton.",
    ),
    (
        "Remove only the template's part",
        ("managed-block", "merge"),
        "These files are shared. Delete the delimited block or the contributed "
        "lines, not the file.",
    ),
    (
        "Leave alone -- yours",
        ("project",),
        "Seeded once at creation and never touched again. Uninstalling the "
        "template does not reclaim them.",
    ),
)


def uninstall_doc(manifest: Manifest) -> str:
    """Render docs/uninstall.md.

    Written as a generated file so that the three-way categorisation can never
    drift from the manifest the update logic actually uses.
    """
    out = [
        "# Uninstalling the skeleton",
        "",
        "<!-- Generated from ownership.yml by `ai-scheme ownership sync`. Do not edit. -->",
        "",
        "Removing `ai-scheme` from a project is a manual operation on purpose: some of",
        "the paths below are shared with your own content, and no script should guess",
        "which lines in them are yours. Work through the three groups in order.",
        "",
    ]
    for title, kinds, blurb in _UNINSTALL_GROUPS:
        entries = [entry for entry in manifest.entries if entry.kind in kinds]
        out += [f"## {title}", "", blurb, ""]
        if not entries:
            out += ["Nothing in this category.", ""]
            continue
        out += ["| Path | Kind | Detail |", "| --- | --- | --- |"]
        for entry in sorted(entries, key=lambda e: e.path):
            detail = entry.note or ""
            if entry.block:
                detail = f"Block `{entry.block}`. {detail}".strip()
            if entry.source:
                detail = f"Rebuilt from `{entry.source}`. {detail}".strip()
            detail = " ".join(detail.split())
            out.append(f"| `{entry.path}` | {entry.kind} | {detail} |")
        out.append("")

    out += [
        "## After removing the files",
        "",
        "Delete `.scheme/config.yml` last. While it exists, `ai-scheme status` still",
        "reports the project as adopted and will offer to update it.",
        "",
        "`config.toml` at the repository root belongs to `ai-zpd`, not to this layer.",
        "Uninstalling the skeleton does not touch it -- see ADR 0008.",
        "",
    ]
    return "\n".join(out)
