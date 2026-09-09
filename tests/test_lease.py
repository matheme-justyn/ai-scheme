"""The lease carrier: four primitives, and what they refuse (#19)."""

from __future__ import annotations

import json
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from ai_scheme import lease


def repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.email", "t@example.com"], cwd=root, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=root, check=True)
    subprocess.run(["git", "commit", "-q", "--allow-empty", "-m", "seed"], cwd=root, check=True)
    return root


def head_of(root: Path) -> str:
    return subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()


def test_the_namespace_is_the_contract() -> None:
    assert lease.ref_for(pr=12) == "refs/leases/pr/12"
    assert lease.ref_for(lane="main") == "refs/leases/lane/main"
    with pytest.raises(lease.LeaseError):
        lease.ref_for(pr=12, lane="main")


def test_acquire_then_inspect(tmp_path: Path) -> None:
    root = repo(tmp_path)
    carrier = lease.Carrier(root=root)

    taken = lease.acquire(
        carrier, pr=12, lane=None, base="main", head=head_of(root), ttl=60, holder="a"
    )
    held = lease.inspect(carrier, pr=12, lane=None)

    assert held is not None
    assert held["holder"] == "a"
    assert held["expired"] is False
    assert "capability" not in held
    assert taken.capability


def test_a_held_lease_cannot_be_taken_again(tmp_path: Path) -> None:
    root = repo(tmp_path)
    carrier = lease.Carrier(root=root)
    lease.acquire(carrier, pr=12, lane=None, base="main", head=head_of(root), ttl=60)

    with pytest.raises(lease.LeaseUnavailable, match="is held"):
        lease.acquire(carrier, pr=12, lane=None, base="main", head=head_of(root), ttl=60)


def test_an_expired_lease_can_be_reclaimed(tmp_path: Path) -> None:
    root = repo(tmp_path)
    carrier = lease.Carrier(root=root)
    lease.acquire(
        carrier, pr=12, lane=None, base="main", head=head_of(root), ttl=1, now=time.time() - 10
    )

    reclaimed = lease.acquire(
        carrier, pr=12, lane=None, base="main", head=head_of(root), ttl=60, holder="b"
    )

    assert reclaimed.holder == "b"


def test_exactly_one_of_two_racing_acquisitions_wins(tmp_path: Path) -> None:
    """Two processes, one ref. git's compare-and-swap decides, not this code."""
    root = repo(tmp_path)
    head = head_of(root)

    def take(holder: str) -> bool:
        try:
            lease.acquire(
                lease.Carrier(root=root),
                pr=12,
                lane=None,
                base="main",
                head=head,
                ttl=60,
                holder=holder,
            )
        except lease.LeaseError:
            return False
        return True

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(take, ["a", "b"]))

    assert results.count(True) == 1


def test_renew_needs_the_capability(tmp_path: Path) -> None:
    root = repo(tmp_path)
    carrier = lease.Carrier(root=root)
    lease.acquire(carrier, pr=12, lane=None, base="main", head=head_of(root), ttl=60)

    with pytest.raises(lease.LeaseUnavailable, match="somebody else"):
        lease.renew(carrier, pr=12, lane=None, capability="not-it", head=head_of(root), ttl=60)


def test_renew_refuses_when_the_head_moved(tmp_path: Path) -> None:
    """A lease covers the work it was taken against, not whatever is there now."""
    root = repo(tmp_path)
    carrier = lease.Carrier(root=root)
    taken = lease.acquire(carrier, pr=12, lane=None, base="main", head="a" * 40, ttl=60)

    with pytest.raises(lease.LeaseUnavailable, match="not the work that is there now"):
        lease.renew(carrier, pr=12, lane=None, capability=taken.capability, head="b" * 40, ttl=60)


def test_renew_extends_the_deadline(tmp_path: Path) -> None:
    root = repo(tmp_path)
    carrier = lease.Carrier(root=root)
    head = head_of(root)
    taken = lease.acquire(carrier, pr=12, lane=None, base="main", head=head, ttl=10)

    renewed = lease.renew(
        carrier, pr=12, lane=None, capability=taken.capability, head=head, ttl=120
    )

    assert renewed.expires_at > taken.expires_at
    assert renewed.capability == taken.capability


def test_release_needs_the_capability_and_then_frees_it(tmp_path: Path) -> None:
    root = repo(tmp_path)
    carrier = lease.Carrier(root=root)
    head = head_of(root)
    taken = lease.acquire(carrier, pr=12, lane=None, base="main", head=head, ttl=60)

    with pytest.raises(lease.LeaseUnavailable):
        lease.release(carrier, pr=12, lane=None, capability="not-it")

    lease.release(carrier, pr=12, lane=None, capability=taken.capability)

    assert lease.inspect(carrier, pr=12, lane=None) is None
    assert lease.acquire(carrier, pr=12, lane=None, base="main", head=head, ttl=60)


def test_a_lane_lease_is_a_separate_ref(tmp_path: Path) -> None:
    root = repo(tmp_path)
    carrier = lease.Carrier(root=root)
    head = head_of(root)

    lease.acquire(carrier, pr=None, lane="main", base="main", head=head, ttl=60)

    assert lease.inspect(carrier, pr=None, lane="main") is not None
    assert lease.inspect(carrier, pr=12, lane=None) is None


def test_the_stored_lease_is_json(tmp_path: Path) -> None:
    root = repo(tmp_path)
    carrier = lease.Carrier(root=root)
    lease.acquire(carrier, pr=12, lane=None, base="main", head=head_of(root), ttl=60)

    sha = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "refs/leases/pr/12"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    payload = subprocess.run(
        ["git", "-C", str(root), "cat-file", "blob", sha],
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    assert set(json.loads(payload)) == {
        "pr",
        "lane",
        "base",
        "head",
        "expires_at",
        "capability",
        "holder",
    }


def test_a_remote_lease_uses_push_with_lease(tmp_path: Path) -> None:
    """Local refs only serialise one machine; the shared ref is the real one."""
    shared = tmp_path / "shared.git"
    subprocess.run(["git", "init", "-q", "--bare", str(shared)], check=True)

    first = repo(tmp_path)
    subprocess.run(["git", "-C", str(first), "remote", "add", "origin", str(shared)], check=True)
    second = tmp_path / "second"
    subprocess.run(["git", "clone", "-q", str(shared), str(second)], check=True)
    subprocess.run(["git", "-C", str(second), "fetch", "-q", str(first), "HEAD"], check=True)

    head = head_of(first)
    lease.acquire(
        lease.Carrier(root=first, remote="origin"),
        pr=12,
        lane=None,
        base="main",
        head=head,
        ttl=60,
        holder="a",
    )

    from_elsewhere = lease.inspect(lease.Carrier(root=second, remote="origin"), pr=12, lane=None)
    assert from_elsewhere is not None
    assert from_elsewhere["holder"] == "a"

    with pytest.raises(lease.LeaseUnavailable):
        lease.acquire(
            lease.Carrier(root=second, remote="origin"),
            pr=12,
            lane=None,
            base="main",
            head=head,
            ttl=60,
            holder="b",
        )
