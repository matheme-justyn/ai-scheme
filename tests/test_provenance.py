"""Where a project's skeleton came from (#6)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_scheme import gh, provenance


def client_for(responses: dict[str, object]) -> gh.Client:
    def runner(args):
        path = args[1]
        if path not in responses:
            raise gh.GhError(f"404 {path}")
        return json.dumps(responses[path])

    return gh.Client(runner)


TAG_REF = {"object": {"type": "commit", "sha": "a" * 40}}
ANNOTATED_REF = {"object": {"type": "tag", "sha": "b" * 40}}
RELEASE = {"tag_name": "v1.0.0", "draft": False, "prerelease": False}


def test_a_lightweight_tag_resolves_to_its_commit() -> None:
    client = client_for({"repos/o/r/git/ref/tags/v1.0.0": TAG_REF})

    assert provenance.resolve_tag(client, "o/r", "v1.0.0") == "a" * 40


def test_an_annotated_tag_is_dereferenced() -> None:
    client = client_for(
        {
            "repos/o/r/git/ref/tags/v1.0.0": ANNOTATED_REF,
            "repos/o/r/git/tags/" + "b" * 40: {"object": {"sha": "c" * 40}},
        }
    )

    assert provenance.resolve_tag(client, "o/r", "v1.0.0") == "c" * 40


def test_a_draft_release_is_refused() -> None:
    client = client_for({"repos/o/r/releases/tags/v1.0.0": {**RELEASE, "draft": True}})

    with pytest.raises(provenance.ProvenanceError, match="draft"):
        provenance.check_release(client, "o/r", "v1.0.0")


def test_a_prerelease_is_refused() -> None:
    client = client_for({"repos/o/r/releases/tags/v1.0.0": {**RELEASE, "prerelease": True}})

    with pytest.raises(provenance.ProvenanceError, match="pre-release"):
        provenance.check_release(client, "o/r", "v1.0.0")


def test_pinning_records_the_commit_not_the_tag() -> None:
    client = client_for(
        {
            "repos/o/r/git/ref/tags/v1.0.0": TAG_REF,
            "repos/o/r/releases/tags/v1.0.0": RELEASE,
        }
    )

    pinned = provenance.pin(
        client, "o/r", "git+https://example.com/o/r", "v1.0.0", cli_version="0.1.0"
    )

    assert pinned.sha == "a" * 40
    assert pinned.tag == "v1.0.0"
    assert pinned.mode == provenance.RELEASE
    assert pinned.attestation == provenance.UNVERIFIED


def test_an_unpinned_remote_source_is_refused() -> None:
    client = client_for({})

    with pytest.raises(provenance.ProvenanceError, match="not pinned"):
        provenance.pin(client, "o/r", "git+https://example.com/o/r", None, cli_version="0.1.0")


def test_an_unpinned_remote_source_may_be_declared_development() -> None:
    client = client_for({})

    pinned = provenance.pin(
        client,
        "o/r",
        "git+https://example.com/o/r",
        None,
        cli_version="0.1.0",
        allow_unreleased=True,
    )

    assert pinned.mode == provenance.DEVELOPMENT
    assert pinned.sha is None


def test_a_local_source_is_a_development_run_without_a_flag(tmp_path: Path) -> None:
    """Pointing at a working copy is not something a flag makes safer."""
    pinned = provenance.pin(client_for({}), "o/r", str(tmp_path), None, cli_version="0.1.0")

    assert pinned.mode == provenance.DEVELOPMENT


def test_provenance_round_trips(tmp_path: Path) -> None:
    pinned = provenance.Provenance(
        source="git+https://example.com/o/r",
        tag="v1.0.0",
        sha="a" * 40,
        applied_at="2026-09-09T00:00:00+00:00",
        cli_version="0.1.0",
    )

    provenance.write(tmp_path, pinned)

    assert provenance.read(tmp_path) == pinned


def test_update_check_reports_a_newer_release() -> None:
    client = client_for({"repos/o/r/releases/latest": {"tag_name": "v2.0.0"}})
    current = provenance.Provenance(
        source="s", tag="v1.0.0", sha="a" * 40, applied_at="", cli_version=""
    )

    answer = provenance.update_check(client, "o/r", current)

    assert answer["update_available"] is True
    assert answer["latest_tag"] == "v2.0.0"


def test_update_check_says_unknown_rather_than_yes_for_a_development_project() -> None:
    """A checkout with no released source is not "out of date" every week."""
    client = client_for({"repos/o/r/releases/latest": {"tag_name": "v2.0.0"}})

    answer = provenance.update_check(client, "o/r", None)

    assert answer["update_available"] is None
    assert "no released source" in answer["reason"]


def test_update_check_with_no_releases_at_all() -> None:
    answer = provenance.update_check(client_for({}), "o/r", None)

    assert answer["update_available"] is None
    assert "no published release" in answer["reason"]
