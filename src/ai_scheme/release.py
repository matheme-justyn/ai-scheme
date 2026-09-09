"""Release artefacts and the evidence that goes with them (#14).

The version is not decided here and not by a person editing a file: it comes
from the intent already declared in pull request titles, which release-please
turns into a version pull request. What this module does is the part after
that -- build the artefacts, hash them, and answer whether a release that
should exist does.

A release with no artefacts, or with artefacts nobody re-checked, is a tag with
a changelog attached. The point of the checksum file and the SBOM is that
somebody downloading later can tell they got what was published.
"""

from __future__ import annotations

import hashlib
import subprocess
import tarfile
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from ai_scheme import gh


class ReleaseError(Exception):
    """The artefacts could not be built, or what was published does not match."""


CHECKSUM_FILE = "SHA256SUMS"
SBOM_FILE = "sbom.spdx.json"

# How long `main` may sit ahead of the newest release before that is worth
# saying out loud. Long enough that a normal working day does not trip it.
DRIFT_AFTER = timedelta(hours=24)


@dataclass(frozen=True)
class Artifact:
    path: Path
    sha256: str

    @property
    def line(self) -> str:
        return f"{self.sha256}  {self.path.name}"


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_archive(root: Path, destination: Path, *, name: str, ref: str = "HEAD") -> Path:
    """A tar.gz of the tracked tree at `ref`, built by git so it is reproducible."""
    destination.mkdir(parents=True, exist_ok=True)
    archive = destination / f"{name}.tar.gz"
    result = subprocess.run(
        ["git", "-C", str(root), "archive", "--format=tar.gz", f"--prefix={name}/", ref],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise ReleaseError(f"cannot archive {ref}: {result.stderr.decode().strip()}")
    archive.write_bytes(result.stdout)
    return archive


def write_checksums(artifacts: list[Artifact], destination: Path) -> Path:
    path = destination / CHECKSUM_FILE
    path.write_text("\n".join(artifact.line for artifact in artifacts) + "\n", encoding="utf-8")
    return path


def verify_checksums(checksums: Path) -> list[str]:
    """Re-hash what the checksum file names. Returns the mismatches."""
    problems: list[str] = []
    for line in checksums.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        expected, _, name = line.partition("  ")
        candidate = checksums.parent / name
        if not candidate.is_file():
            problems.append(f"{name}: named in {CHECKSUM_FILE} but not present")
            continue
        actual = sha256_of(candidate)
        if actual != expected:
            problems.append(f"{name}: expected {expected}, got {actual}")
    return problems


def read_archive_names(archive: Path) -> list[str]:
    with tarfile.open(archive) as tar:
        return tar.getnames()


@dataclass(frozen=True)
class Drift:
    drifted: bool
    reason: str
    latest_tag: str | None = None
    commits_since: int = 0

    def as_dict(self) -> dict[str, Any]:
        return {
            "drifted": self.drifted,
            "reason": self.reason,
            "latest_tag": self.latest_tag,
            "commits_since": self.commits_since,
        }


def check_drift(
    client: gh.Client, repo: str, *, now: datetime | None = None, after: timedelta = DRIFT_AFTER
) -> Drift:
    """Has `main` moved on without a release for longer than it should have?

    Not an error on its own -- plenty of commits do not deserve a release. It
    is a question worth asking out loud once a day, because the failure mode it
    catches is a release workflow that has been quietly failing.
    """
    moment = now or datetime.now(UTC)
    try:
        latest = client.api(f"repos/{repo}/releases/latest")
    except gh.GhError:
        latest = None

    commits = client.api(f"repos/{repo}/commits?per_page=100") or []
    if not commits:
        return Drift(False, "no commits to compare")

    head_date = datetime.fromisoformat(
        commits[0]["commit"]["committer"]["date"].replace("Z", "+00:00")
    )

    if latest is None:
        return Drift(
            moment - head_date > after,
            "no release exists yet",
            None,
            len(commits),
        )

    published = datetime.fromisoformat(latest["published_at"].replace("Z", "+00:00"))
    since = [
        commit
        for commit in commits
        if datetime.fromisoformat(commit["commit"]["committer"]["date"].replace("Z", "+00:00"))
        > published
    ]
    if not since:
        return Drift(False, "the newest release is current", latest.get("tag_name"), 0)

    age = moment - published
    return Drift(
        age > after,
        (
            f"{len(since)} commit(s) since {latest.get('tag_name')}, published "
            f"{round(age.total_seconds() / 3600)}h ago"
        ),
        latest.get("tag_name"),
        len(since),
    )
