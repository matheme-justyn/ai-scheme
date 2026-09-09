"""The lease carrier: four primitives over a git ref (#19).

Worktrees isolate files. They do not isolate the pull request control plane --
ready/draft, labels, milestone, merge all live on GitHub, shared by every
session working on the same pull request. Two sessions writing at once race.

This module is the carrier only, and it deliberately knows nothing about pull
requests beyond a number. It offers acquire, renew, release and inspect, and
the atomicity comes from git's own compare-and-swap (`git update-ref` with an
expected old value), not from anything written here. The protocol -- which
operations must hold a lease, what the agent does when it cannot get one --
belongs to the mechanism layer (ai-zpd #4) and is not in this file.

The lease records the head SHA it was taken against, and renew refuses when the
caller states a different one. The carrier does not ask GitHub what the head
is: the moment it did, it would have pull request semantics.
"""

from __future__ import annotations

import json
import secrets
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

ZERO = "0" * 40


class LeaseError(Exception):
    """The carrier itself failed: git refused, or the ref holds nonsense."""


class LeaseUnavailable(LeaseError):
    """A definite no: somebody holds it, the capability is wrong, head moved.

    Separated because the two mean different things to a caller. "Somebody
    else has it" is an answer worth retrying; "git is broken" is not.
    """


@dataclass(frozen=True)
class Lease:
    pr: int | None
    lane: str | None
    base: str
    head: str
    expires_at: float
    capability: str
    holder: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "pr": self.pr,
            "lane": self.lane,
            "base": self.base,
            "head": self.head,
            "expires_at": self.expires_at,
            "capability": self.capability,
            "holder": self.holder,
        }

    def public(self, *, now: float | None = None) -> dict[str, Any]:
        """What `inspect` prints: everything except the capability."""
        moment = time.time() if now is None else now
        payload = {key: value for key, value in self.as_dict().items() if key != "capability"}
        payload["expired"] = self.is_expired(now=moment)
        payload["seconds_remaining"] = round(max(0.0, self.expires_at - moment), 3)
        return payload

    def is_expired(self, *, now: float | None = None) -> bool:
        return (time.time() if now is None else now) >= self.expires_at

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Lease:
        return cls(
            pr=raw.get("pr"),
            lane=raw.get("lane"),
            base=raw["base"],
            head=raw["head"],
            expires_at=float(raw["expires_at"]),
            capability=raw["capability"],
            holder=raw.get("holder", ""),
        )


@dataclass
class Carrier:
    """Git ref operations, with the repository and remote fixed."""

    root: Path
    remote: str | None = None
    _env: dict[str, str] = field(default_factory=dict)

    def _git(self, *args: str, check: bool = True) -> str:
        result = subprocess.run(
            ["git", "-C", str(self.root), *args],
            capture_output=True,
            text=True,
            check=False,
        )
        if check and result.returncode != 0:
            raise LeaseError((result.stderr or result.stdout).strip())
        return result.stdout.strip()

    # -- ref plumbing ----------------------------------------------------

    def read_ref(self, ref: str) -> tuple[str | None, Lease | None]:
        """The object the ref points at, and the lease stored in it."""
        if self.remote:
            listing = self._git("ls-remote", self.remote, ref)
            sha = listing.split("\t")[0] if listing else None
            if sha:
                self._git("fetch", "--quiet", self.remote, f"+{ref}:{ref}", check=False)
        else:
            sha = self._git("rev-parse", "--verify", "--quiet", ref, check=False) or None
        if not sha:
            return None, None
        try:
            payload = self._git("cat-file", "blob", sha)
        except LeaseError:
            return sha, None
        try:
            return sha, Lease.from_dict(json.loads(payload))
        except (json.JSONDecodeError, KeyError) as exc:
            raise LeaseError(f"{ref} does not hold a readable lease: {exc}") from exc

    def write_ref(self, ref: str, lease: Lease, old: str | None) -> str:
        """Compare-and-swap `ref` from `old` to a blob holding `lease`."""
        blob = subprocess.run(
            ["git", "-C", str(self.root), "hash-object", "-w", "--stdin"],
            input=json.dumps(lease.as_dict(), sort_keys=True),
            capture_output=True,
            text=True,
            check=False,
        )
        if blob.returncode != 0:
            raise LeaseError(blob.stderr.strip())
        new = blob.stdout.strip()

        if self.remote:
            expected = old or ZERO
            pushed = subprocess.run(
                [
                    "git",
                    "-C",
                    str(self.root),
                    "push",
                    f"--force-with-lease={ref}:{expected}",
                    self.remote,
                    f"{new}:{ref}",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if pushed.returncode != 0:
                raise LeaseUnavailable("the lease changed while this one was being written")
            return new

        result = subprocess.run(
            ["git", "-C", str(self.root), "update-ref", ref, new, old or ZERO],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise LeaseUnavailable("the lease changed while this one was being written")
        return new

    def delete_ref(self, ref: str, old: str) -> None:
        if self.remote:
            pushed = subprocess.run(
                [
                    "git",
                    "-C",
                    str(self.root),
                    "push",
                    f"--force-with-lease={ref}:{old}",
                    self.remote,
                    f":{ref}",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            if pushed.returncode != 0:
                raise LeaseUnavailable("the lease changed while it was being released")
            return
        result = subprocess.run(
            ["git", "-C", str(self.root), "update-ref", "-d", ref, old],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            raise LeaseUnavailable("the lease changed while it was being released")


def ref_for(*, pr: int | None = None, lane: str | None = None) -> str:
    """The namespace. Once shipped this is a contract with the other layer."""
    if pr is not None and lane is not None:
        raise LeaseError("a lease binds a pull request or a lane, not both")
    if pr is not None:
        return f"refs/leases/pr/{pr}"
    if lane:
        return f"refs/leases/lane/{lane}"
    raise LeaseError("a lease needs --pr or --lane")


def acquire(
    carrier: Carrier,
    *,
    pr: int | None,
    lane: str | None,
    base: str,
    head: str,
    ttl: float,
    holder: str = "",
    now: float | None = None,
) -> Lease:
    """Take the lease, or reclaim one that is provably expired. Never force."""
    moment = time.time() if now is None else now
    ref = ref_for(pr=pr, lane=lane)
    old, existing = carrier.read_ref(ref)

    if existing is not None and not existing.is_expired(now=moment):
        raise LeaseUnavailable(
            f"{ref} is held for another {round(existing.expires_at - moment)}s "
            f"by {existing.holder or 'an unnamed holder'}"
        )

    lease = Lease(
        pr=pr,
        lane=lane,
        base=base,
        head=head,
        expires_at=moment + ttl,
        capability=secrets.token_urlsafe(24),
        holder=holder,
    )
    # Reclaiming is itself a compare-and-swap against the expired value, so two
    # sessions seeing the same expired lease cannot both win.
    carrier.write_ref(ref, lease, old)
    return lease


def renew(
    carrier: Carrier,
    *,
    pr: int | None,
    lane: str | None,
    capability: str,
    head: str,
    ttl: float,
    now: float | None = None,
) -> Lease:
    moment = time.time() if now is None else now
    ref = ref_for(pr=pr, lane=lane)
    old, existing = carrier.read_ref(ref)
    if existing is None:
        raise LeaseUnavailable(f"{ref} is not held")
    if not secrets.compare_digest(existing.capability, capability):
        raise LeaseUnavailable(f"{ref} is held by somebody else")
    if existing.head != head:
        raise LeaseUnavailable(
            f"{ref} was taken against {existing.head[:12]}, the caller states "
            f"{head[:12]}: the work this lease covers is not the work that is there now. "
            "Release it and take a new one."
        )

    renewed = Lease(
        pr=existing.pr,
        lane=existing.lane,
        base=existing.base,
        head=existing.head,
        expires_at=moment + ttl,
        capability=existing.capability,
        holder=existing.holder,
    )
    carrier.write_ref(ref, renewed, old)
    return renewed


def release(carrier: Carrier, *, pr: int | None, lane: str | None, capability: str) -> None:
    ref = ref_for(pr=pr, lane=lane)
    old, existing = carrier.read_ref(ref)
    if existing is None or old is None:
        raise LeaseUnavailable(f"{ref} is not held")
    if not secrets.compare_digest(existing.capability, capability):
        raise LeaseUnavailable(f"{ref} is held by somebody else")
    carrier.delete_ref(ref, old)


def inspect(
    carrier: Carrier, *, pr: int | None, lane: str | None, now: float | None = None
) -> dict[str, Any] | None:
    _, existing = carrier.read_ref(ref_for(pr=pr, lane=lane))
    return None if existing is None else existing.public(now=now)
