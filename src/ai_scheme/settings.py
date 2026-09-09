"""Repository settings declared as files, and compared against reality (#13).

Neither a GitHub template nor Copier copies repository settings, so every new
project gets its merge strategy, its branch rules and its scanning switches set
by hand -- and nothing ever notices when one drifts back.

Three modes, and the asymmetry between them is deliberate. `plan` and `check`
are read-only and anything may run them. `apply` writes, and writing branch
rules or security switches is a change a person makes.

Capability is reported, never assumed: a plan that cannot be enforced on this
repository's plan or with this token is `degraded`, which is neither a pass nor
a failure. Reporting "enforced" for something GitHub is not enforcing is the
one outcome worse than no check at all.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from ai_scheme import gh

POLICY_RELDIR = Path("policies")


class Capability(StrEnum):
    ALLOWED = "allowed"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class Verdict(StrEnum):
    MATCHES = "matches"
    DRIFTED = "drifted"
    DEGRADED = "degraded"


@dataclass
class Finding:
    area: str
    verdict: Verdict
    capability: Capability
    differences: list[str] = field(default_factory=list)
    detail: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "area": self.area,
            "verdict": self.verdict.value,
            "capability": self.capability.value,
            "differences": self.differences,
            "detail": self.detail,
        }

    def __str__(self) -> str:
        head = f"{self.area}: {self.verdict.value} ({self.capability.value})"
        if self.detail:
            head += f" -- {self.detail}"
        return head


def load_policy(root: Path, name: str) -> dict[str, Any] | None:
    path = root / POLICY_RELDIR / f"{name}.json"
    if not path.is_file():
        return None
    raw = json.loads(path.read_text(encoding="utf-8"))
    return {key: value for key, value in raw.items() if not key.startswith("$")}


def compare(desired: dict[str, Any], actual: dict[str, Any]) -> list[str]:
    """Only the keys the policy declares. Everything else is the repo's business."""
    return [
        f"{key}: want {value!r}, have {actual.get(key)!r}"
        for key, value in desired.items()
        if actual.get(key) != value
    ]


def check_repository(client: gh.Client, repo: str, desired: dict[str, Any]) -> Finding:
    try:
        actual = client.api(f"repos/{repo}") or {}
    except gh.GhError as exc:
        return Finding("repository", Verdict.DEGRADED, Capability.UNKNOWN, detail=str(exc))
    differences = compare(desired, actual)
    verdict = Verdict.DRIFTED if differences else Verdict.MATCHES
    return Finding("repository", verdict, Capability.ALLOWED, differences)


def check_actions(client: gh.Client, repo: str, desired: dict[str, Any]) -> Finding:
    try:
        actual = client.api(f"repos/{repo}/actions/permissions/workflow") or {}
    except gh.GhError as exc:
        return Finding("actions", Verdict.DEGRADED, Capability.UNKNOWN, detail=str(exc))
    differences = compare(desired, actual)
    return Finding(
        "actions",
        Verdict.DRIFTED if differences else Verdict.MATCHES,
        Capability.ALLOWED,
        differences,
    )


def check_security(client: gh.Client, repo: str, desired: dict[str, Any]) -> Finding:
    try:
        repository = client.api(f"repos/{repo}") or {}
    except gh.GhError as exc:
        return Finding("security", Verdict.DEGRADED, Capability.UNKNOWN, detail=str(exc))

    analysis = repository.get("security_and_analysis") or {}
    actual = {
        "secret_scanning": (analysis.get("secret_scanning") or {}).get("status"),
        "secret_scanning_push_protection": (
            analysis.get("secret_scanning_push_protection") or {}
        ).get("status"),
    }
    wanted = {key: value for key, value in desired.items() if key in actual}
    differences = compare(wanted, actual)

    if repository.get("private") and not analysis:
        # Advanced Security is a paid add-on for private repositories. The
        # setting is not wrong here, it is unavailable.
        return Finding(
            "security",
            Verdict.DEGRADED,
            Capability.BLOCKED,
            differences,
            "a private repository on this plan does not expose secret scanning",
        )

    return Finding(
        "security",
        Verdict.DRIFTED if differences else Verdict.MATCHES,
        Capability.ALLOWED,
        differences,
    )


def check_labels(client: gh.Client, repo: str, desired: dict[str, Any]) -> Finding:
    try:
        actual = client.api(f"repos/{repo}/labels?per_page=100") or []
    except gh.GhError as exc:
        return Finding("labels", Verdict.DEGRADED, Capability.UNKNOWN, detail=str(exc))

    present = {label["name"] for label in actual}
    missing = sorted(
        label["name"] for label in desired.get("labels", []) if label["name"] not in present
    )
    return Finding(
        "labels",
        Verdict.DRIFTED if missing else Verdict.MATCHES,
        Capability.ALLOWED,
        [f"missing label: {name}" for name in missing],
    )


def desired_rulesets(policy: dict[str, Any], release_phase: str) -> list[dict[str, Any]]:
    """The rulesets for this phase, with bypass resolved from `release_phase`."""
    resolved: list[dict[str, Any]] = []
    for ruleset in policy.get("rulesets", []):
        entry = {key: value for key, value in ruleset.items() if key != "bypass_when"}
        entry["bypass"] = (ruleset.get("bypass_when") or {}).get(release_phase, "none")
        resolved.append(entry)
    return resolved


def check_rulesets(
    client: gh.Client, repo: str, desired: dict[str, Any], release_phase: str
) -> Finding:
    wanted = desired_rulesets(desired, release_phase)
    try:
        actual = client.api(f"repos/{repo}/rulesets") or []
    except gh.GhError as exc:
        message = str(exc).lower()
        if "upgrade" in message or "not available" in message or "404" in message:
            return Finding(
                "rulesets",
                Verdict.DEGRADED,
                Capability.BLOCKED,
                [f"expected ruleset: {entry['name']}" for entry in wanted],
                "rulesets are not available on this repository's plan",
            )
        return Finding("rulesets", Verdict.DEGRADED, Capability.UNKNOWN, detail=str(exc))

    present = {ruleset.get("name") for ruleset in actual}
    differences = [
        f"missing ruleset: {entry['name']}" for entry in wanted if entry["name"] not in present
    ]
    if release_phase == "release":
        bypassing = [ruleset.get("name") for ruleset in actual if ruleset.get("bypass_actors")]
        differences += [f"bypass actors present in release phase: {name}" for name in bypassing]

    return Finding(
        "rulesets",
        Verdict.DRIFTED if differences else Verdict.MATCHES,
        Capability.ALLOWED,
        differences,
    )


def check_pages(client: gh.Client, repo: str, desired: dict[str, Any]) -> Finding:
    try:
        actual = client.api(f"repos/{repo}/pages") or {}
    except gh.GhError as exc:
        message = str(exc).lower()
        if "404" in message or "not found" in message:
            return Finding(
                "pages",
                Verdict.DRIFTED,
                Capability.ALLOWED,
                ["Pages is not enabled"],
            )
        return Finding("pages", Verdict.DEGRADED, Capability.UNKNOWN, detail=str(exc))

    differences = []
    if desired.get("build_type") and actual.get("build_type") != desired["build_type"]:
        differences.append(
            f"build_type: want {desired['build_type']!r}, have {actual.get('build_type')!r}"
        )
    return Finding(
        "pages",
        Verdict.DRIFTED if differences else Verdict.MATCHES,
        Capability.ALLOWED,
        differences,
    )


AREAS: dict[str, Callable[..., Finding]] = {
    "repository": check_repository,
    "actions": check_actions,
    "security": check_security,
    "labels": check_labels,
    "pages": check_pages,
}


def check(client: gh.Client, repo: str, root: Path, *, release_phase: str) -> list[Finding]:
    findings: list[Finding] = []
    for name, checker in AREAS.items():
        policy = load_policy(root, name)
        if policy is None:
            continue
        findings.append(checker(client, repo, policy))

    rulesets = load_policy(root, "rulesets")
    if rulesets is not None:
        findings.append(check_rulesets(client, repo, rulesets, release_phase))
    return findings


def drifted(findings: list[Finding]) -> list[Finding]:
    return [finding for finding in findings if finding.verdict is Verdict.DRIFTED]


APPLY_BY_HAND = (
    "rulesets",
    "security",
)


def apply_area(client: gh.Client, repo: str, name: str, policy: dict[str, Any]) -> str:
    """Write one area's policy. Refuses the areas a person should set."""
    if name in APPLY_BY_HAND:
        raise gh.GhError(
            f"{name} is applied by a person, not by this command: "
            "branch rules and security switches are not an agent's to change"
        )
    if name == "repository":
        client.api(f"repos/{repo}", method="PATCH", fields=policy)
        return f"repository: applied {len(policy)} setting(s)"
    if name == "actions":
        client.api(f"repos/{repo}/actions/permissions/workflow", method="PUT", fields=policy)
        return "actions: applied workflow permissions"
    if name == "labels":
        created = 0
        for label in policy.get("labels", []):
            try:
                client.api(f"repos/{repo}/labels", method="POST", fields=label)
                created += 1
            except gh.GhError:
                continue
        return f"labels: created {created}"
    raise gh.GhError(f"no apply step for {name}")
