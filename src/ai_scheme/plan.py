"""Lifecycle plans: what would change, before anything changes (#5).

Three paths -- create, adopt, update -- all produce the same artefact: a plan
that classifies every path and records enough about the target to detect that
the world moved underneath it. Nothing writes to the target until the plan is
handed back to `apply`.

The classification comes from the ownership manifest (#3), not from guesswork
about file names, and the plan lives outside the target repository so that
producing it cannot dirty the thing it describes.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from ai_scheme import ownership, selfhost

PLAN_VERSION = 1


class Action(StrEnum):
    ADD = "add"
    OVERWRITE = "overwrite"
    PRESERVE = "preserve"
    AUTO_MERGE = "auto-merge"
    MANUAL_MERGE = "manual-merge"


class Mode(StrEnum):
    CREATE = "create"
    ADOPT = "adopt"
    UPDATE = "update"


@dataclass(frozen=True)
class Entry:
    path: str
    action: Action
    kind: str
    reason: str

    def as_dict(self) -> dict[str, str]:
        return {
            "path": self.path,
            "action": self.action.value,
            "kind": self.kind,
            "reason": self.reason,
        }


@dataclass
class Target:
    path: str
    head: str | None
    dirty: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {"path": self.path, "head": self.head, "dirty": self.dirty}


@dataclass
class Plan:
    mode: Mode
    target: Target
    source: str
    source_ref: str | None
    answers: dict[str, Any]
    entries: list[Entry]
    digest: str
    version: int = PLAN_VERSION
    legacy: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return {
            "version": self.version,
            "mode": self.mode.value,
            "target": self.target.as_dict(),
            "source": self.source,
            "source_ref": self.source_ref,
            "answers": self.answers,
            "entries": [entry.as_dict() for entry in self.entries],
            "digest": self.digest,
            "legacy": self.legacy,
        }

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), indent=2, ensure_ascii=False, sort_keys=True)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Plan:
        return cls(
            mode=Mode(raw["mode"]),
            target=Target(
                path=raw["target"]["path"],
                head=raw["target"]["head"],
                dirty=list(raw["target"]["dirty"]),
            ),
            source=raw["source"],
            source_ref=raw.get("source_ref"),
            answers=raw.get("answers") or {},
            entries=[
                Entry(
                    path=entry["path"],
                    action=Action(entry["action"]),
                    kind=entry["kind"],
                    reason=entry["reason"],
                )
                for entry in raw.get("entries") or []
            ],
            digest=raw["digest"],
            version=raw.get("version", PLAN_VERSION),
            legacy=list(raw.get("legacy") or []),
        )

    def by_action(self, action: Action) -> list[Entry]:
        return [entry for entry in self.entries if entry.action is action]

    def report(self) -> str:
        """The Markdown half, for a person rather than a machine."""
        lines = [
            f"# {self.mode.value} plan",
            "",
            f"- target: `{self.target.path}`",
            f"- target HEAD: `{self.target.head or 'not a git repository'}`",
            f"- source: `{self.source}`" + (f" @ `{self.source_ref}`" if self.source_ref else ""),
            f"- digest: `{self.digest}`",
            "",
        ]
        if self.legacy:
            lines += [
                "## The previous layout is still here",
                "",
                "These belong to the layout this template replaces. They are read, never",
                "written, and never used to compare versions. Delete them once this plan",
                "has been applied and `ai-scheme status` reports `current`.",
                "",
                *(f"- `{path}`" for path in self.legacy),
                "",
            ]
        if self.target.dirty:
            lines += [
                "## Uncommitted changes in the target",
                "",
                "Applying will not touch these, and it will not commit or stash anything.",
                "",
                *(f"- `{path}`" for path in self.target.dirty),
                "",
            ]
        for action in Action:
            entries = self.by_action(action)
            if not entries:
                continue
            lines += [f"## {action.value} ({len(entries)})", ""]
            lines += [f"- `{entry.path}` -- {entry.reason}" for entry in entries]
            lines.append("")
        manual = self.by_action(Action.MANUAL_MERGE)
        if manual:
            lines += [
                "## What to do about manual-merge",
                "",
                "Apply refuses while these exist. Resolve each one in the target, then",
                "produce a new plan -- a plan is only valid for the world it described.",
                "",
            ]
        return "\n".join(lines)


def digest_of(entries: list[Entry], rendered_root: Path) -> str:
    """A digest over both the decisions and the bytes they were made from.

    The answers file is left out: Copier writes it from the answers the plan
    already records, down to a `_commit` that changes with every commit to the
    template. Hashing it would invalidate plans for a reason that has nothing
    to do with what they describe.
    """
    hasher = hashlib.sha256()
    for entry in sorted(entries, key=lambda item: item.path):
        if entry.path in selfhost.UNCOMPARED:
            continue
        hasher.update(entry.path.encode())
        hasher.update(entry.action.value.encode())
        candidate = rendered_root / entry.path
        if candidate.is_file():
            hasher.update(candidate.read_bytes())
    return hasher.hexdigest()


def git_head(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() or None if result.returncode == 0 else None


def git_dirty(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "-C", str(root), "status", "--porcelain"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return []
    return sorted(line[3:].strip() for line in result.stdout.splitlines() if line.strip())


def observe_target(root: Path) -> Target:
    return Target(path=str(root), head=git_head(root), dirty=git_dirty(root))


def _kind_of(manifest: ownership.Manifest, relative: str) -> tuple[str, str | None]:
    """The declared kind for a path, and its block name when it has one."""
    for entry in sorted(manifest.entries, key=lambda item: -len(item.path)):
        if relative == entry.path or (entry.path.endswith("/") and relative.startswith(entry.path)):
            return entry.kind, entry.block
    return "template", None


def classify(
    mode: Mode,
    root: Path,
    rendered_root: Path,
    manifest: ownership.Manifest,
    *,
    previous_root: Path | None = None,
) -> list[Entry]:
    """One entry per rendered path. Nothing here reads or writes the target."""
    entries: list[Entry] = []
    for rendered in sorted(rendered_root.rglob("*")):
        if not rendered.is_file():
            continue
        relative = rendered.relative_to(rendered_root).as_posix()
        kind, block = _kind_of(manifest, relative)
        existing = root / relative

        if not existing.exists():
            entries.append(Entry(relative, Action.ADD, kind, "not in the target yet"))
            continue

        if relative in selfhost.UNCOMPARED:
            # The answers file is Copier's bookkeeping, rewritten from the
            # answers this plan already records. Merging it would mean merging
            # a derived file against itself.
            entries.append(Entry(relative, Action.OVERWRITE, kind, "Copier rewrites this file"))
            continue

        if kind == "project":
            entries.append(Entry(relative, Action.PRESERVE, kind, "the project owns this path"))
            continue

        if kind == "managed-block" and block:
            entries.append(
                Entry(relative, Action.AUTO_MERGE, kind, f"replace the `{block}` block only")
            )
            continue

        if kind == "merge":
            entries.append(
                Entry(relative, Action.AUTO_MERGE, kind, "ordered union, nothing removed")
            )
            continue

        same = existing.read_bytes() == rendered.read_bytes()
        if same:
            entries.append(Entry(relative, Action.PRESERVE, kind, "already identical"))
            continue

        if mode is Mode.ADOPT:
            entries.append(
                Entry(relative, Action.MANUAL_MERGE, kind, "the project already has this path")
            )
            continue

        if previous_root is None:
            entries.append(
                Entry(
                    relative,
                    Action.OVERWRITE if mode is Mode.CREATE else Action.MANUAL_MERGE,
                    kind,
                    "differs, and the previous rendering was not available to compare",
                )
            )
            continue

        previous = previous_root / relative
        was_modified = not previous.is_file() or previous.read_bytes() != existing.read_bytes()
        if not was_modified:
            entries.append(
                Entry(relative, Action.OVERWRITE, kind, "unmodified since the last update")
            )
        else:
            entries.append(
                Entry(relative, Action.MANUAL_MERGE, kind, "changed locally and changed upstream")
            )
    return entries


def legacy_sentinels(root: Path) -> list[str]:
    from ai_scheme.status import observe_legacy

    return list(observe_legacy(root))


def build(
    mode: Mode,
    root: Path,
    *,
    source: str,
    source_ref: str | None,
    answers: dict[str, Any],
    rendered_root: Path,
    manifest: ownership.Manifest,
    previous_root: Path | None = None,
) -> Plan:
    entries = classify(mode, root, rendered_root, manifest, previous_root=previous_root)
    return Plan(
        legacy=legacy_sentinels(root),
        mode=mode,
        target=observe_target(root),
        source=source,
        source_ref=source_ref,
        answers=answers,
        entries=entries,
        digest=digest_of(entries, rendered_root),
    )


def render_candidate(source: str, answers: dict[str, Any], destination: Path) -> None:
    """Render the template into a directory that is not the target."""
    selfhost.render_into(source, answers, destination)
