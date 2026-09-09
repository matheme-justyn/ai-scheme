"""Applying a lifecycle plan, and refusing to when the world moved (#5).

A plan describes one state of the target. `apply` re-observes that state and
stops if anything it recorded has changed -- a plan is not a wish, it is a
claim about what is there. It never stashes, never commits, and never resolves
a conflict on the user's behalf.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from ai_scheme import selfhost
from ai_scheme.plan import Action, Plan, git_dirty, git_head

CONFLICT_MARKER = re.compile(r"^(<{7}|={7}|>{7})(\s|$)", re.MULTILINE)

MERGE_BEGIN = "# BEGIN ai-scheme"
MERGE_END = "# END ai-scheme"


class ApplyRefused(Exception):
    """The plan does not describe the world as it is now."""

    def __init__(self, reasons: list[str]) -> None:
        super().__init__("; ".join(reasons))
        self.reasons = reasons


@dataclass
class Applied:
    written: list[str]
    skipped: list[str]


def check_target_unchanged(plan: Plan, root: Path) -> list[str]:
    reasons: list[str] = []
    head = git_head(root)
    if head != plan.target.head:
        reasons.append(f"HEAD moved: plan {plan.target.head}, now {head}")
    dirty = git_dirty(root)
    if dirty != plan.target.dirty:
        added = sorted(set(dirty) - set(plan.target.dirty))
        removed = sorted(set(plan.target.dirty) - set(dirty))
        if added:
            reasons.append(f"newly uncommitted: {', '.join(added)}")
        if removed:
            reasons.append(f"no longer uncommitted: {', '.join(removed)}")
    return reasons


SKIP_DIRECTORIES = {".git", ".venv", "node_modules"}


def check_no_conflicts(plan: Plan, root: Path) -> list[str]:
    """Fail closed on conflict markers and on any leftover .rej file.

    A `.rej` is checked across the whole target, not only where this plan would
    write: it means a previous merge was left unfinished, and that is not a
    state to write another rendering into.
    """
    reasons: list[str] = []
    for entry in plan.entries:
        if entry.action is Action.PRESERVE:
            continue
        target = root / entry.path
        if target.is_file():
            text = target.read_text(encoding="utf-8", errors="replace")
            if CONFLICT_MARKER.search(text):
                reasons.append(f"{entry.path} contains conflict markers")

    for rejected in sorted(root.rglob("*.rej")):
        if SKIP_DIRECTORIES & set(rejected.relative_to(root).parts):
            continue
        reasons.append(f"{rejected.relative_to(root)} is a leftover rejected hunk")
    return reasons


def union_lines(existing: str, rendered: str) -> str:
    """Ordered union: everything the project had, plus what it did not have.

    Nothing is ever removed. A line the project deleted on purpose comes back,
    which is the trade for never losing one it meant to keep.
    """
    have = {line.strip() for line in existing.splitlines() if line.strip()}
    additions = [
        line for line in rendered.splitlines() if line.strip() and line.strip() not in have
    ]
    if not additions:
        return existing
    body = "\n".join(additions)
    section = f"{MERGE_BEGIN}\n{body}\n{MERGE_END}\n"
    separator = "" if existing.endswith("\n") else "\n"
    return f"{existing}{separator}\n{section}"


def apply_plan(plan: Plan, root: Path, rendered_root: Path, *, blocks: dict[str, str]) -> Applied:
    written: list[str] = []
    skipped: list[str] = []

    manual = plan.by_action(Action.MANUAL_MERGE)
    if manual:
        raise ApplyRefused(
            [f"{len(manual)} path(s) need a manual merge first"]
            + [f"  {entry.path}: {entry.reason}" for entry in manual]
        )

    reasons = check_target_unchanged(plan, root) + check_no_conflicts(plan, root)
    if reasons:
        raise ApplyRefused(reasons)

    for entry in plan.entries:
        source = rendered_root / entry.path
        destination = root / entry.path
        if entry.action is Action.PRESERVE:
            skipped.append(entry.path)
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        if entry.action in (Action.ADD, Action.OVERWRITE):
            shutil.copy2(source, destination)
        elif entry.action is Action.AUTO_MERGE:
            block = blocks.get(entry.path)
            if block:
                destination.write_text(
                    selfhost.replace_block(
                        destination.read_text(encoding="utf-8"),
                        source.read_text(encoding="utf-8"),
                        block,
                    ),
                    encoding="utf-8",
                )
            else:
                destination.write_text(
                    union_lines(
                        destination.read_text(encoding="utf-8"),
                        source.read_text(encoding="utf-8"),
                    ),
                    encoding="utf-8",
                )
        written.append(entry.path)

    return Applied(written=written, skipped=skipped)
