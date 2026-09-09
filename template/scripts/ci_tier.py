#!/usr/bin/env python3
"""Print the verification tier a change needs, and nothing else.

CI reads this to label a run and to decide what to put in the job summary.
`scripts/verify` makes the same call internally, so the two can never disagree.
"""

from __future__ import annotations

import argparse
import sys


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", default="origin/main", help="Compare against this ref.")
    args = parser.parse_args(argv)

    try:
        from ai_scheme.tiers import changed_paths, classify
    except ImportError:
        # Fail closed: an environment that cannot classify the change runs
        # everything rather than guessing that nothing important moved.
        print("full")
        return 0

    print(classify(changed_paths(args.base)).value)
    return 0


if __name__ == "__main__":
    sys.exit(main())
