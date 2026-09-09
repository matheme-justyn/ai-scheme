"""`status`: one deterministic answer about where a project stands (#4).

Everything that decides a state is a plain function over facts that have
already been collected, so the same inputs always produce the same output and
the tests do not need a repository on disk. `collect` does the I/O; `judge`
does the thinking.

The old entry point buried this in shell: `init-project.sh` looked for a
`.template-version` file and branched. An agent could only guess what to do
next by reading prose. Here the answer carries `next_command`, and the contract
in docs/status-interface-contract.md forbids the caller from inferring a state
of its own.

Exit codes are fixed (ADR 0008, #3): 0 means the question was answered whatever
the answer is, 2 means it could not be answered. "An update is available" is
not an error and never leaves through a non-zero code.
"""

from __future__ import annotations

import re
import shlex
from dataclasses import dataclass, field, replace
from pathlib import Path
from typing import Any

from ai_scheme.paths import ANSWERS_RELPATH, MECHANISM_CONFIG_RELPATH

# The mechanism layer's own artefacts. `.scaffolding/` is its delivery
# directory and `.template-version` records its version, both current and both
# somebody else's -- so this layer detects them, reports them, and never reads
# or compares them. There is no "previous layout" to migrate from: the skeleton
# layer had not shipped anything before this one. See #41 and ADR 0007.
MECHANISM_MARKERS = (Path(".template-version"), Path(".scaffolding"))

VERSION = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)")


class State:
    CREATE = "create"
    ADOPT = "adopt"
    UPDATE = "update"
    POLICY_ONLY_UPDATE = "policy-only-update"
    DRIFTED = "drifted"
    CURRENT = "current"


NEXT_COMMAND = {
    State.CREATE: "ai-scheme create --plan",
    State.ADOPT: "ai-scheme adopt --plan",
    State.UPDATE: "ai-scheme update --plan",
    State.POLICY_ONLY_UPDATE: "ai-scheme settings apply --plan",
    State.DRIFTED: "ai-scheme update --plan",
    State.CURRENT: None,
}

UNKNOWN = "unknown"


@dataclass(frozen=True)
class Facts:
    """What was observed. Anything unobservable is None, never guessed."""

    exists: bool = True
    empty: bool = True
    is_git_repo: bool = False
    has_answers: bool = False
    mechanism_markers: tuple[str, ...] = ()
    current_version: str | None = None
    target_version: str | None = None
    drift: tuple[str, ...] | None = None
    policy_drift: tuple[str, ...] | None = None
    mechanism_config: bool = False


@dataclass(frozen=True)
class Status:
    state: str
    reason: str
    next_command: str | None
    current_version: str | None = None
    target_version: str | None = None
    drift: list[str] | str = field(default_factory=list)
    policy_drift: list[str] | str = field(default_factory=list)
    mechanism_config_detected: bool = False
    mechanism_layer_detected: list[str] = field(default_factory=list)

    @property
    def next_command_argv(self) -> list[str]:
        """`next_command` as argv, for callers that would otherwise eval it."""
        return shlex.split(self.next_command) if self.next_command else []

    def as_dict(self) -> dict[str, Any]:
        return {
            "state": self.state,
            "reason": self.reason,
            "next_command": self.next_command,
            "next_command_argv": self.next_command_argv,
            "current_version": self.current_version,
            "target_version": self.target_version,
            "drift": self.drift,
            "policy_drift": self.policy_drift,
            "mechanism_config_detected": self.mechanism_config_detected,
            "mechanism_layer_detected": self.mechanism_layer_detected,
        }


def parse_version(value: str | None) -> tuple[int, int, int] | None:
    match = VERSION.match((value or "").strip())
    if not match:
        return None
    major, minor, patch = match.groups()
    return int(major), int(minor), int(patch)


def is_behind(current: str | None, target: str | None) -> bool | None:
    """True, False, or None when the two cannot be compared."""
    left, right = parse_version(current), parse_version(target)
    if left is None or right is None:
        return None
    return left < right


def _listed(items: list[str]) -> str:
    if len(items) < 3:
        return " and ".join(items)
    return ", ".join(items[:-1]) + f" and {items[-1]}"


def judge(facts: Facts) -> Status:
    """The state machine. One state, one reason, one next command."""
    unknowns: list[str] | str = UNKNOWN if facts.drift is None else list(facts.drift)
    policy: list[str] | str = UNKNOWN if facts.policy_drift is None else list(facts.policy_drift)

    def answer(state: str, reason: str) -> Status:
        return Status(
            state=state,
            reason=reason,
            next_command=NEXT_COMMAND[state],
            current_version=facts.current_version,
            target_version=facts.target_version,
            drift=unknowns,
            policy_drift=policy,
            mechanism_config_detected=facts.mechanism_config,
            mechanism_layer_detected=list(facts.mechanism_markers),
        )

    if not facts.exists or facts.empty:
        return answer(State.CREATE, "the target is missing or empty")

    if not facts.has_answers:
        if facts.mechanism_markers:
            return answer(
                State.ADOPT,
                f"no {ANSWERS_RELPATH}; the mechanism layer is installed here ("
                + ", ".join(facts.mechanism_markers)
                + "), which this layer reports but never reads",
            )
        return answer(State.ADOPT, f"an existing project with no {ANSWERS_RELPATH}")

    behind = is_behind(facts.current_version, facts.target_version)
    if behind:
        return answer(
            State.UPDATE,
            f"the answers file records {facts.current_version}, "
            f"the template is at {facts.target_version}",
        )

    # Drift is reported before policy drift: a locally modified template file
    # is what makes the next update conflict, and the caller should see it
    # first. `drift` stays in the payload either way.
    if facts.drift:
        return answer(
            State.DRIFTED,
            f"{len(facts.drift)} template-owned path(s) differ from the template",
        )

    if facts.policy_drift:
        return answer(
            State.POLICY_ONLY_UPDATE,
            f"the version matches, {len(facts.policy_drift)} repository setting(s) do not",
        )

    # Nothing is wrong with what was checked. Say what was checked, because
    # "current" plus an unchecked drift is not the same claim as "current".
    checked = []
    unchecked = []
    (checked if behind is not None else unchecked).append("the version")
    (checked if facts.drift is not None else unchecked).append("template-owned files")
    (checked if facts.policy_drift is not None else unchecked).append("repository settings")
    reason = f"{_listed(checked)} match the template" if checked else "nothing was checked"
    if unchecked:
        reason += f"; {_listed(unchecked)} not checked"
    return answer(State.CURRENT, reason)


def observe_mechanism(root: Path) -> tuple[str, ...]:
    return tuple(marker.as_posix() for marker in MECHANISM_MARKERS if (root / marker).exists())


def is_empty(root: Path) -> bool:
    if not root.is_dir():
        return True
    return not any(child.name != ".git" for child in root.iterdir())


def observe(root: Path) -> Facts:
    """The observable half: filesystem only, no network, no guesses."""
    return Facts(
        exists=root.exists(),
        empty=is_empty(root),
        is_git_repo=(root / ".git").exists(),
        has_answers=(root / ANSWERS_RELPATH).is_file(),
        mechanism_markers=observe_mechanism(root),
        mechanism_config=(root / MECHANISM_CONFIG_RELPATH).is_file(),
    )


def collect(root: Path, *, target_version: str, allow_render: bool = True) -> Facts:
    """Everything `judge` needs, with anything unobtainable left as None.

    Rendering the template to detect drift needs the template itself, which for
    a generated project means a network fetch. When that is not possible the
    answer is `unknown`, never a guess -- an unknown drift must not read as
    "no drift".
    """
    from ai_scheme import config, selfhost

    facts = replace(observe(root), target_version=target_version)
    if not facts.has_answers:
        return facts

    try:
        answers = config.load_answers(root)
    except config.ConfigError:
        return facts

    current_version = answers.get("_commit")
    drift: tuple[str, ...] | None = None
    if allow_render:
        try:
            with selfhost.render_to_temp(root, source=answers.get("_src_path")) as handle:
                differences = selfhost.compare(root, Path(handle) / "rendered")
            drift = tuple(difference.path for difference in differences)
        except Exception:
            # A template that cannot be fetched or rendered is a fact about
            # this run, not about the project.
            drift = None

    return replace(facts, current_version=current_version, drift=drift)
