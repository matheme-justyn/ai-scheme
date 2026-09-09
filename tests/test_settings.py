"""Repository settings as policy files, and honest capability reporting (#13)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from ai_scheme import gh, settings
from ai_scheme.paths import package_root


def client_for(responses: dict[str, object]) -> gh.Client:
    def runner(args):
        path = args[1]
        if path not in responses:
            raise gh.GhError(f"404 Not Found: {path}")
        value = responses[path]
        if isinstance(value, Exception):
            raise value
        return json.dumps(value)

    return gh.Client(runner)


def test_the_shipped_policies_parse() -> None:
    for name in ("repository", "actions", "security", "labels", "rulesets"):
        assert settings.load_policy(package_root(), name) is not None


def test_comparison_only_covers_declared_keys() -> None:
    differences = settings.compare(
        {"has_wiki": False}, {"has_wiki": True, "description": "anything"}
    )

    assert differences == ["has_wiki: want False, have True"]


def test_repository_drift_is_named() -> None:
    client = client_for({"repos/o/r": {"has_wiki": True}})

    finding = settings.check_repository(client, "o/r", {"has_wiki": False})

    assert finding.verdict is settings.Verdict.DRIFTED
    assert finding.differences == ["has_wiki: want False, have True"]


def test_a_private_repository_without_scanning_is_degraded_not_failed() -> None:
    """Unavailable is not the same as wrong, and neither is it a pass."""
    client = client_for({"repos/o/r": {"private": True}})

    finding = settings.check_security(client, "o/r", {"secret_scanning": "enabled"})

    assert finding.verdict is settings.Verdict.DEGRADED
    assert finding.capability is settings.Capability.BLOCKED
    assert "does not expose secret scanning" in finding.detail


def test_rulesets_unavailable_on_the_plan_are_degraded() -> None:
    client = client_for({})  # every call raises 404

    finding = settings.check_rulesets(
        client, "o/r", {"rulesets": [{"name": "protected-branch", "bypass_when": {}}]}, "alpha"
    )

    assert finding.verdict is settings.Verdict.DEGRADED
    assert finding.capability is settings.Capability.BLOCKED
    assert finding.differences == ["expected ruleset: protected-branch"]


def test_release_phase_decides_who_may_bypass() -> None:
    policy = settings.load_policy(package_root(), "rulesets")
    assert policy is not None

    alpha = {entry["name"]: entry["bypass"] for entry in settings.desired_rulesets(policy, "alpha")}
    release = {
        entry["name"]: entry["bypass"] for entry in settings.desired_rulesets(policy, "release")
    }

    assert alpha["protected-branch"] == "repository_admin"
    assert alpha["required-checks"] == "none"
    assert release["protected-branch"] == "none"


def test_a_bypass_actor_in_the_release_phase_is_drift() -> None:
    client = client_for(
        {
            "repos/o/r/rulesets": [
                {"name": "protected-branch", "bypass_actors": [{"actor_id": 5}]},
                {"name": "required-checks"},
            ]
        }
    )
    policy = {
        "rulesets": [
            {"name": "protected-branch", "bypass_when": {"release": "none"}},
            {"name": "required-checks", "bypass_when": {"release": "none"}},
        ]
    }

    finding = settings.check_rulesets(client, "o/r", policy, "release")

    assert any("bypass actors present" in difference for difference in finding.differences)


def test_missing_labels_are_reported() -> None:
    client = client_for({"repos/o/r/labels?per_page=100": [{"name": "type:task"}]})

    finding = settings.check_labels(
        client, "o/r", {"labels": [{"name": "type:task"}, {"name": "hotfix"}]}
    )

    assert finding.differences == ["missing label: hotfix"]


def test_apply_refuses_the_areas_a_person_should_set() -> None:
    for area in settings.APPLY_BY_HAND:
        with pytest.raises(gh.GhError, match="applied by a person"):
            settings.apply_area(client_for({}), "o/r", area, {})


def test_check_walks_every_policy_that_exists(tmp_path: Path) -> None:
    (tmp_path / "policies").mkdir()
    (tmp_path / "policies" / "repository.json").write_text('{"has_wiki": false}', encoding="utf-8")
    client = client_for({"repos/o/r": {"has_wiki": False}})

    findings = settings.check(client, "o/r", tmp_path, release_phase="alpha")

    assert [finding.area for finding in findings] == ["repository"]
    assert findings[0].verdict is settings.Verdict.MATCHES
