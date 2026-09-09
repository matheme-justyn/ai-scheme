"""Fetching the external checks, pinned and hash-verified (#11).

Every tool this repository runs is pinned to a version and a SHA-256 in
`policies/tools.json`. A download that does not match its hash is not
installed: a check that silently ran a different binary than the one that was
reviewed is worse than a check that did not run.

Binaries are cached under `${XDG_CACHE_HOME:-~/.cache}/ai-scheme/`, so a laptop
downloads each one once and CI downloads it once per runner.
"""

from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import stat
import tarfile
import tempfile
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

POLICY_RELPATH = Path("policies/tools.json")
CACHE_ENV = "AI_SCHEME_CACHE"


class ToolError(Exception):
    """The tool could not be provided, and no substitute was used."""


@dataclass(frozen=True)
class Pin:
    name: str
    version: str
    url: str
    sha256: str
    member: str | None


def platform_key() -> str:
    system = platform.system().lower()
    machine = platform.machine().lower()
    architecture = {"arm64": "arm64", "aarch64": "arm64", "x86_64": "x86_64", "amd64": "x86_64"}
    if machine not in architecture:
        raise ToolError(f"unsupported architecture: {machine}")
    return f"{system}-{architecture[machine]}"


def load_pin(root: Path, name: str, *, key: str | None = None) -> Pin:
    path = root / POLICY_RELPATH
    if not path.is_file():
        raise ToolError(f"no tool policy at {path}")
    policy = json.loads(path.read_text(encoding="utf-8"))
    tool = (policy.get("tools") or {}).get(name)
    if tool is None:
        raise ToolError(f"{name} is not pinned in {POLICY_RELPATH}")

    key = key or platform_key()
    entry = (tool.get("platforms") or {}).get(key)
    if entry is None:
        raise ToolError(f"{name} is not pinned for {key}")

    substitutions = {"version": tool["version"], "platform": entry["platform"]}
    member = tool.get("member")
    return Pin(
        name=name,
        version=tool["version"],
        url=tool["url"].format(**substitutions),
        sha256=entry["sha256"],
        member=member.format(**substitutions) if member else None,
    )


def cache_root(root: Path) -> Path:
    """Where binaries live: the XDG cache, or the repository when it is not writable."""
    override = os.environ.get(CACHE_ENV)
    if override:
        return Path(override)
    base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "ai-scheme"
    try:
        base.mkdir(parents=True, exist_ok=True)
        probe = base / ".writable"
        probe.touch()
        probe.unlink()
    except OSError:
        return root / ".cache" / "ai-scheme"
    return base


def _download(url: str) -> bytes:
    try:
        with urllib.request.urlopen(url, timeout=60) as response:  # noqa: S310 - pinned https
            return response.read()
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        raise ToolError(f"could not download {url}: {exc}") from exc


def _extract(payload: bytes, pin: Pin, destination: Path) -> None:
    if pin.member is None:
        destination.write_bytes(payload)
    else:
        with tempfile.TemporaryDirectory() as temporary:
            archive = Path(temporary) / "archive"
            archive.write_bytes(payload)
            with tarfile.open(archive) as tar:
                extracted = tar.extractfile(pin.member)
                if extracted is None:
                    raise ToolError(f"{pin.name}: {pin.member} is not in the archive")
                destination.write_bytes(extracted.read())
    destination.chmod(destination.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP)


def ensure(root: Path, name: str) -> Path:
    """The path to the pinned binary, downloading and verifying it if needed."""
    pin = load_pin(root, name)
    binary = cache_root(root) / name / pin.version / name
    if binary.is_file() and os.access(binary, os.X_OK):
        return binary

    payload = _download(pin.url)
    digest = hashlib.sha256(payload).hexdigest()
    if digest != pin.sha256:
        raise ToolError(
            f"{name} {pin.version} does not match its pin: "
            f"expected {pin.sha256}, downloaded {digest}"
        )

    binary.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary:
        staged = Path(temporary) / name
        _extract(payload, pin, staged)
        shutil.move(str(staged), binary)
    return binary
