"""Command line entry point.

Exit codes are fixed so that shell callers can branch on them:

    0  the command answered the question
    1  the answer is "no" -- invalid config, or generated files are stale
    2  the question could not be answered -- missing file, unreadable input

`status` (#4) will reuse this split: 0 for a successful judgement whatever the
state turns out to be, 2 for being unable to judge.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ai_scheme import __version__, config, issues, ownership, selfhost
from ai_scheme import verify as verify_module
from ai_scheme.paths import (
    OWNERSHIP_RELPATH,
    UNINSTALL_RELPATH,
    package_root,
    repo_root,
)
from ai_scheme.tiers import Tier, changed_paths, classify

EXIT_OK = 0
EXIT_NO = 1
EXIT_UNDETERMINED = 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ai-scheme",
        description="Repository skeleton lifecycle commands.",
    )
    parser.add_argument("--version", action="version", version=f"ai-scheme {__version__}")
    parser.add_argument(
        "-C",
        "--directory",
        type=Path,
        default=None,
        metavar="PATH",
        help="Act on this project instead of the current directory.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    cfg = sub.add_parser("config", help="Read and check the answers file.")
    cfg_sub = cfg.add_subparsers(dest="config_command", required=True)

    cfg_get = cfg_sub.add_parser(
        "get",
        help="Print one value. Lists print one item per line, booleans as true/false.",
    )
    cfg_get.add_argument("key", help="Key name, dotted for nested values.")

    cfg_sub.add_parser("validate", help="Check the answers file against the schema.")

    own = sub.add_parser("ownership", help="Work with the file ownership manifest.")
    own_sub = own.add_subparsers(dest="ownership_command", required=True)

    own_sync = own_sub.add_parser(
        "sync",
        help="Regenerate copier.yml's derived region and docs/uninstall.md.",
    )
    own_sync.add_argument(
        "--check",
        action="store_true",
        help="Do not write; exit 1 if the generated files are out of date.",
    )

    own_sub.add_parser("list", help="Print each declared path and its kind.")

    host = sub.add_parser(
        "selfhost",
        help="Render template/ over this repository's own tree (ADR 0014).",
    )
    host_sub = host.add_subparsers(dest="selfhost_command", required=True)
    host_sub.add_parser("check", help="Exit 1 if the tree differs from the rendering.")
    host_sub.add_parser("apply", help="Write the rendering into the working tree.")

    issue = sub.add_parser("issue", help="The issue contract: titles and forms (#7).")
    issue_sub = issue.add_subparsers(dest="issue_command", required=True)
    issue_title = issue_sub.add_parser("validate-title", help="Check one title against the rules.")
    issue_title.add_argument("title", help="The title, quoted.")
    issue_sub.add_parser("check-forms", help="Check the issue forms against the contract.")

    check = sub.add_parser("verify", help="Run the checks for a change (#11).")
    check.add_argument(
        "--tier",
        choices=[tier.value for tier in Tier],
        default=None,
        help="Force a tier instead of deriving it from the changed paths.",
    )
    check.add_argument(
        "--stage",
        choices=[stage.name for stage in verify_module.STAGES],
        default=None,
        help="Run one stage only.",
    )
    check.add_argument(
        "--base",
        default="origin/main",
        help="Ref to compare against when deriving the tier.",
    )

    return parser


def _resolve_root(directory: Path | None) -> Path:
    return repo_root(directory) if directory is None else directory.resolve()


def cmd_config_get(root: Path, key: str) -> int:
    answers = config.load_answers(root)
    print(config.format_value(config.get(answers, key)))
    return EXIT_OK


def cmd_config_validate(root: Path) -> int:
    answers = config.load_answers(root)
    schema = config.load_schema(package_root())
    problems = config.validate(answers, schema)
    if not problems:
        print(f"{root / '.scheme/config.yml'}: valid")
        return EXIT_OK
    print(f"{root / '.scheme/config.yml'}: {len(problems)} problem(s)", file=sys.stderr)
    for problem in problems:
        print(f"  {problem}", file=sys.stderr)
    return EXIT_NO


def cmd_ownership_sync(root: Path, check: bool) -> int:
    manifest = ownership.load(root)
    copier_path = root / "copier.yml"
    uninstall_path = root / UNINSTALL_RELPATH

    if not copier_path.is_file():
        raise ownership.OwnershipError(f"copier.yml not found: {copier_path}")

    current_copier = copier_path.read_text(encoding="utf-8")
    wanted_copier = ownership.sync_copier(current_copier, manifest)
    wanted_uninstall = ownership.uninstall_doc(manifest)
    current_uninstall = (
        uninstall_path.read_text(encoding="utf-8") if uninstall_path.is_file() else None
    )

    stale = []
    if wanted_copier != current_copier:
        stale.append("copier.yml")
    if wanted_uninstall != current_uninstall:
        stale.append(UNINSTALL_RELPATH.as_posix())

    if check:
        if stale:
            print(
                "out of date with " + str(OWNERSHIP_RELPATH) + ": " + ", ".join(stale),
                file=sys.stderr,
            )
            print("run `ai-scheme ownership sync`", file=sys.stderr)
            return EXIT_NO
        print("generated files are up to date")
        return EXIT_OK

    if not stale:
        print("generated files are already up to date")
        return EXIT_OK

    copier_path.write_text(wanted_copier, encoding="utf-8")
    uninstall_path.parent.mkdir(parents=True, exist_ok=True)
    uninstall_path.write_text(wanted_uninstall, encoding="utf-8")
    print("regenerated: " + ", ".join(stale))
    return EXIT_OK


def cmd_selfhost(root: Path, apply_changes: bool) -> int:
    with selfhost.render_to_temp(root) as rendered:
        rendered_root = Path(rendered) / "rendered"
        if apply_changes:
            written = selfhost.apply(root, rendered_root)
            print(f"rendered {len(written)} path(s) from template/")
            return EXIT_OK
        differences = selfhost.compare(root, rendered_root)

    if not differences:
        print("the working tree matches template/")
        return EXIT_OK
    print(f"{len(differences)} path(s) differ from template/:", file=sys.stderr)
    for difference in differences:
        print(f"  {difference}", file=sys.stderr)
    print("run `ai-scheme selfhost apply`", file=sys.stderr)
    return EXIT_NO


def cmd_issue_validate_title(title: str) -> int:
    problems = issues.validate_title(title)
    if not problems:
        print("title: ok")
        return EXIT_OK
    print(f"title: {len(problems)} problem(s)", file=sys.stderr)
    for problem in problems:
        print(f"  {problem}", file=sys.stderr)
    return EXIT_NO


def cmd_issue_check_forms(root: Path) -> int:
    problems = issues.validate_forms(root)
    if not problems:
        print("issue forms: ok")
        return EXIT_OK
    print(f"issue forms: {len(problems)} problem(s)", file=sys.stderr)
    for problem in problems:
        print(f"  {problem}", file=sys.stderr)
    return EXIT_NO


def cmd_verify(root: Path, tier_name: str | None, stage: str | None, base: str) -> int:
    if tier_name is not None:
        tier = Tier(tier_name)
    elif stage is not None:
        # An explicit stage says what to run; the tier only has to be wide
        # enough to contain it.
        tier = Tier.FULL
    else:
        tier = classify(changed_paths(base, cwd=str(root)))

    report = verify_module.run(root, tier, only=stage)
    stream = sys.stdout if report.ok else sys.stderr
    for line in report.lines():
        print(line, file=stream)
    return EXIT_OK if report.ok else EXIT_NO


def cmd_ownership_list(root: Path) -> int:
    manifest = ownership.load(root)
    width = max(len(entry.path) for entry in manifest.entries)
    for entry in sorted(manifest.entries, key=lambda e: e.path):
        print(f"{entry.path.ljust(width)}  {entry.kind}")
    return EXIT_OK


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = _resolve_root(args.directory)

    try:
        if args.command == "config":
            if args.config_command == "get":
                return cmd_config_get(root, args.key)
            return cmd_config_validate(root)
        if args.command == "ownership":
            if args.ownership_command == "sync":
                return cmd_ownership_sync(root, args.check)
            return cmd_ownership_list(root)
        if args.command == "issue":
            if args.issue_command == "validate-title":
                return cmd_issue_validate_title(args.title)
            return cmd_issue_check_forms(root)
        if args.command == "verify":
            return cmd_verify(root, args.tier, args.stage, args.base)
        if args.command == "selfhost":
            return cmd_selfhost(root, apply_changes=args.selfhost_command == "apply")
    except (config.ConfigError, ownership.OwnershipError, selfhost.SelfHostError) as exc:
        print(f"ai-scheme: {exc}", file=sys.stderr)
        return EXIT_UNDETERMINED

    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
