#!/usr/bin/env python3
"""The pull request control plane lease: acquire, renew, release, inspect.

    scripts/lease.py acquire --pr 12 --base main --head <sha> --ttl 900
    scripts/lease.py renew   --pr 12 --capability <token> --head <sha>
    scripts/lease.py release --pr 12 --capability <token>
    scripts/lease.py inspect --pr 12

The carrier is git: the lease is a blob behind `refs/leases/pr/<n>`, written
with compare-and-swap. See docs/lease-carrier.md for the contract.
"""

from __future__ import annotations

import subprocess
import sys


def main() -> int:
    arguments = ["lease", *sys.argv[1:]]
    try:
        from ai_scheme.cli import main as cli
    except ImportError:
        return subprocess.run(["uv", "run", "ai-scheme", *arguments], check=False).returncode
    return cli(arguments)


if __name__ == "__main__":
    raise SystemExit(main())
