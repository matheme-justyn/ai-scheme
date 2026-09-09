"""Release artefacts, their checksums, and the drift question (#14)."""

from __future__ import annotations

import json
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from ai_scheme import gh, pullrequests, release


def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)
    (root / "README.md").write_text("a project\n", encoding="utf-8")
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-qm", "seed"], cwd=root, check=True)
    return root


def test_the_source_archive_holds_the_tracked_tree(tmp_path: Path) -> None:
    root = repo(tmp_path)

    archive = release.source_archive(root, tmp_path / "dist", name="demo-1.0.0")

    assert archive.name == "demo-1.0.0.tar.gz"
    assert "demo-1.0.0/README.md" in release.read_archive_names(archive)


def test_checksums_round_trip(tmp_path: Path) -> None:
    destination = tmp_path / "dist"
    destination.mkdir()
    artefact = destination / "thing.tar.gz"
    artefact.write_bytes(b"contents")

    checksums = release.write_checksums(
        [release.Artifact(artefact, release.sha256_of(artefact))], destination
    )

    assert release.verify_checksums(checksums) == []


def test_a_changed_artefact_is_caught(tmp_path: Path) -> None:
    """The point of re-hashing what was published."""
    destination = tmp_path / "dist"
    destination.mkdir()
    artefact = destination / "thing.tar.gz"
    artefact.write_bytes(b"contents")
    checksums = release.write_checksums(
        [release.Artifact(artefact, release.sha256_of(artefact))], destination
    )

    artefact.write_bytes(b"something else")

    problems = release.verify_checksums(checksums)
    assert len(problems) == 1
    assert "expected" in problems[0]


def test_a_missing_artefact_is_caught(tmp_path: Path) -> None:
    destination = tmp_path / "dist"
    destination.mkdir()
    artefact = destination / "thing.tar.gz"
    artefact.write_bytes(b"contents")
    checksums = release.write_checksums(
        [release.Artifact(artefact, release.sha256_of(artefact))], destination
    )
    artefact.unlink()

    assert "not present" in release.verify_checksums(checksums)[0]


def client_for(responses: dict[str, object]) -> gh.Client:
    def runner(args):
        path = args[1]
        if path not in responses:
            raise gh.GhError(f"404 {path}")
        return json.dumps(responses[path])

    return gh.Client(runner)


def commit_at(when: datetime) -> dict[str, object]:
    return {"commit": {"committer": {"date": when.isoformat().replace("+00:00", "Z")}}}


def test_drift_is_false_when_the_release_is_current() -> None:
    now = datetime(2026, 9, 9, tzinfo=UTC)
    client = client_for(
        {
            "repos/o/r/releases/latest": {
                "tag_name": "v1.0.0",
                "published_at": now.isoformat().replace("+00:00", "Z"),
            },
            "repos/o/r/commits?per_page=100": [commit_at(now - timedelta(hours=1))],
        }
    )

    drift = release.check_drift(client, "o/r", now=now)

    assert drift.drifted is False
    assert drift.commits_since == 0


def test_drift_is_true_when_commits_sat_unreleased_for_a_day() -> None:
    now = datetime(2026, 9, 9, tzinfo=UTC)
    client = client_for(
        {
            "repos/o/r/releases/latest": {
                "tag_name": "v1.0.0",
                "published_at": (now - timedelta(days=3)).isoformat().replace("+00:00", "Z"),
            },
            "repos/o/r/commits?per_page=100": [commit_at(now - timedelta(days=1))],
        }
    )

    drift = release.check_drift(client, "o/r", now=now)

    assert drift.drifted is True
    assert drift.commits_since == 1
    assert "since v1.0.0" in drift.reason


def test_no_release_yet_is_reported_as_such() -> None:
    now = datetime(2026, 9, 9, tzinfo=UTC)
    client = client_for({"repos/o/r/commits?per_page=100": [commit_at(now)]})

    drift = release.check_drift(client, "o/r", now=now)

    assert drift.latest_tag is None
    assert "no release exists yet" in drift.reason


@pytest.mark.parametrize(
    ("branch", "checked"),
    [("release-please--branches--main", False), ("feat/14-release", True)],
)
def test_the_generated_version_pull_request_is_exempt(branch: str, checked: bool) -> None:
    """It is machine-made from intent already reviewed elsewhere."""
    pull = {
        "title": "chore: release 1.2.0",
        "body": "changelog, no closing keyword",
        "isDraft": False,
        "headRefName": branch,
        "labels": [],
        "milestone": None,
    }

    problems = pullrequests.validate(pull, None)

    assert bool(problems) is checked
