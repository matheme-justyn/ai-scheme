"""Where a project's skeleton came from, recorded and checked (#6).

A tag is a label somebody can move. What goes into `.scheme/provenance.json` is
the 40-character commit the tag pointed at when the template was applied, so a
later `update` can say "this is the same source" or "this is not" rather than
trusting the name.

The previous POC also required immutable releases and signed commits before it
would run. On a public repository with one maintainer neither is a check --
there is no second party for them to protect against -- so this keeps the parts
that carry information: full SHA resolution, a recorded source, and a refusal
to run from a draft or pre-release.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ai_scheme import gh

PROVENANCE_RELPATH = Path(".scheme/provenance.json")

RELEASE = "release"
DEVELOPMENT = "development"
UNVERIFIED = "unverified"
VERIFIED = "verified"


class ProvenanceError(Exception):
    """The source could not be pinned, so nothing should be applied from it."""


@dataclass
class Provenance:
    source: str
    tag: str | None
    sha: str | None
    applied_at: str
    cli_version: str
    mode: str = RELEASE
    attestation: str = UNVERIFIED

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.as_dict(), indent=2, sort_keys=True) + "\n"

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Provenance:
        return cls(
            source=raw["source"],
            tag=raw.get("tag"),
            sha=raw.get("sha"),
            applied_at=raw.get("applied_at", ""),
            cli_version=raw.get("cli_version", ""),
            mode=raw.get("mode", RELEASE),
            attestation=raw.get("attestation", UNVERIFIED),
        )


def read(root: Path) -> Provenance | None:
    path = root / PROVENANCE_RELPATH
    if not path.is_file():
        return None
    try:
        return Provenance.from_dict(json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, KeyError) as exc:
        raise ProvenanceError(f"{path} is not readable: {exc}") from exc


def write(root: Path, provenance: Provenance) -> Path:
    path = root / PROVENANCE_RELPATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(provenance.to_json(), encoding="utf-8")
    return path


def is_local(source: str) -> bool:
    """A working copy on disk, as opposed to something fetched by tag."""
    return not source.startswith(("http://", "https://", "git+", "git@"))


def resolve_tag(client: gh.Client, repo: str, tag: str) -> str:
    """The full commit SHA a tag points at, dereferencing an annotated tag."""
    reference = client.api(f"repos/{repo}/git/ref/tags/{tag}")
    if not reference:
        raise ProvenanceError(f"{repo} has no tag {tag}")
    obj = reference.get("object") or {}
    sha = obj.get("sha")
    if obj.get("type") == "tag":
        tag_object = client.api(f"repos/{repo}/git/tags/{sha}")
        sha = ((tag_object or {}).get("object") or {}).get("sha")
    if not sha or len(sha) != 40:
        raise ProvenanceError(f"{repo} tag {tag} did not resolve to a full commit SHA")
    return sha


def check_release(client: gh.Client, repo: str, tag: str) -> dict[str, Any]:
    """The release for a tag, refusing drafts and pre-releases."""
    release = client.api(f"repos/{repo}/releases/tags/{tag}")
    if not release:
        raise ProvenanceError(f"{repo} has no release for {tag}")
    if release.get("draft"):
        raise ProvenanceError(f"{repo} release {tag} is a draft")
    if release.get("prerelease"):
        raise ProvenanceError(f"{repo} release {tag} is a pre-release")
    return release


def pin(
    client: gh.Client,
    repo: str,
    source: str,
    tag: str | None,
    *,
    cli_version: str,
    allow_unreleased: bool = False,
) -> Provenance:
    """What to record for this run, refusing an unpinned remote source."""
    now = datetime.now(UTC).isoformat(timespec="seconds")

    if tag is None:
        if not is_local(source) and not allow_unreleased:
            raise ProvenanceError(
                f"{source} is not pinned to a tag. Pass --tag <tag>, or "
                "--allow-unreleased to record this as a development run."
            )
        return Provenance(
            source=source,
            tag=None,
            sha=None,
            applied_at=now,
            cli_version=cli_version,
            mode=DEVELOPMENT,
            attestation=UNVERIFIED,
        )

    sha = resolve_tag(client, repo, tag)
    check_release(client, repo, tag)
    return Provenance(
        source=source,
        tag=tag,
        sha=sha,
        applied_at=now,
        cli_version=cli_version,
        mode=RELEASE,
        attestation=UNVERIFIED,
    )


def latest_release(client: gh.Client, repo: str) -> dict[str, Any] | None:
    """The newest published release, or None when there is not one yet."""
    try:
        return client.api(f"repos/{repo}/releases/latest")
    except gh.GhError:
        return None


def update_check(client: gh.Client, repo: str, current: Provenance | None) -> dict[str, Any]:
    """Whether a newer release exists. The answer is a field, never an exit code."""
    latest = latest_release(client, repo)
    if latest is None:
        return {
            "update_available": None,
            "reason": f"{repo} has no published release to compare against",
            "current_tag": current.tag if current else None,
            "latest_tag": None,
        }

    latest_tag = latest.get("tag_name")
    if current is None or current.tag is None:
        # Not "yes": there is nothing to compare. A development checkout would
        # otherwise be told every week that it is out of date.
        return {
            "update_available": None,
            "reason": "this project records no released source to compare against",
            "current_tag": current.tag if current else None,
            "latest_tag": latest_tag,
        }

    same = current.tag == latest_tag
    return {
        "update_available": not same,
        "reason": ("already on the latest release" if same else "a newer release is published"),
        "current_tag": current.tag,
        "latest_tag": latest_tag,
    }
