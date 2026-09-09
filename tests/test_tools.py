"""Pinned external checks: version, hash, and what happens when they fail (#11)."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest

from ai_scheme import tools, verify
from ai_scheme.paths import package_root

REPO_ROOT = package_root()


def test_every_pinned_tool_declares_both_platforms() -> None:
    policy = json.loads((REPO_ROOT / tools.POLICY_RELPATH).read_text(encoding="utf-8"))
    for name, tool in policy["tools"].items():
        assert set(tool["platforms"]) >= {"darwin-arm64", "linux-x86_64"}, name
        for key, entry in tool["platforms"].items():
            assert len(entry["sha256"]) == 64, f"{name} {key}"


def test_a_pin_renders_its_url_and_member() -> None:
    pin = tools.load_pin(REPO_ROOT, "shellcheck", key="linux-x86_64")

    assert pin.url.endswith("shellcheck-v0.11.0.linux.x86_64.tar.xz")
    assert pin.member == "shellcheck-v0.11.0/shellcheck"


def test_an_unpinned_tool_is_an_error() -> None:
    with pytest.raises(tools.ToolError, match="not pinned"):
        tools.load_pin(REPO_ROOT, "nmap")


def test_an_unpinned_platform_is_an_error() -> None:
    with pytest.raises(tools.ToolError, match="not pinned for"):
        tools.load_pin(REPO_ROOT, "shellcheck", key="plan9-mips")


def test_a_download_that_does_not_match_its_pin_is_refused(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The whole point of pinning: a different binary is not a substitute."""
    policy = tmp_path / tools.POLICY_RELPATH
    policy.parent.mkdir(parents=True)
    policy.write_text(
        json.dumps(
            {
                "tools": {
                    "shellcheck": {
                        "version": "0.11.0",
                        "url": "https://example.invalid/{version}/{platform}",
                        "member": None,
                        "platforms": {tools.platform_key(): {"platform": "x", "sha256": "0" * 64}},
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv(tools.CACHE_ENV, str(tmp_path / "cache"))
    monkeypatch.setattr(tools, "_download", lambda url: b"not the pinned bytes")

    with pytest.raises(tools.ToolError, match="does not match its pin"):
        tools.ensure(tmp_path, "shellcheck")

    assert not (tmp_path / "cache" / "shellcheck").exists()


def test_an_unreachable_download_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv(tools.CACHE_ENV, str(tmp_path / "cache"))
    result = verify.stage_static(tmp_path)

    assert not result.ok
    assert "unavailable" in result.detail


@pytest.mark.slow
def test_gitleaks_fails_on_a_planted_secret(tmp_path: Path) -> None:
    """The deliberately broken fixture #11 asks for."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    (tmp_path / "policies").mkdir()
    (tmp_path / tools.POLICY_RELPATH).write_text(
        (REPO_ROOT / tools.POLICY_RELPATH).read_text(encoding="utf-8"), encoding="utf-8"
    )
    # A GitHub-shaped token, assembled at runtime so that this file does not
    # itself contain one -- gitleaks scans this repository too. The documented
    # AWS example key is on gitleaks' own allowlist, so it proves nothing.
    planted = "ghp_" + "A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8"
    (tmp_path / "leak.env").write_text(f'token = "{planted}"\n', encoding="utf-8")

    result = verify.stage_static(tmp_path)

    assert not result.ok
    assert "static analysis" in result.detail
