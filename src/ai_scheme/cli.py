"""Command line entry point.

Exit codes are fixed so that shell callers can branch on them:

    0  the command answered the question
    1  the answer is "no" -- invalid config, or generated files are stale
    2  the question could not be answered -- missing file, unreadable input

`status` (#4) reuses this split: 0 for a successful judgement whatever the
state turns out to be, 2 for being unable to judge.

This module is the parser and the dispatch. What each command does lives in
`commands.py`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ai_scheme import __version__, commands, config, gh, lease, ownership, selfhost
from ai_scheme import plan as plan_module
from ai_scheme import verify as verify_module
from ai_scheme.commands import EXIT_NO, EXIT_OK, EXIT_UNDETERMINED
from ai_scheme.tiers import Tier

# Re-exported: callers branch on these, and they are part of the contract.
__all__ = ["EXIT_NO", "EXIT_OK", "EXIT_UNDETERMINED", "build_parser", "main"]


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

    for name, blurb in (
        ("create", "Render this template into a new project (#5)."),
        ("adopt", "Bring an existing project under this template (#5)."),
        ("update", "Bring a project up to the current template (#5)."),
    ):
        life = sub.add_parser(name, help=blurb)
        life.add_argument("path", nargs="?", type=Path, default=None, help="Defaults to -C or cwd.")
        life.add_argument(
            "--source",
            default=None,
            help="Template to render. Defaults to the answers file's _src_path, else this repo.",
        )
        life.add_argument("--ref", default=None, help="Template ref to render.")
        life.add_argument(
            "--data",
            action="append",
            default=[],
            metavar="KEY=VALUE",
            help="An answer, repeatable. Only for create and adopt.",
        )
        life.add_argument(
            "--out",
            type=Path,
            default=None,
            help="Where the plan is written. Defaults to a temporary directory.",
        )
        life.add_argument(
            "--tag",
            default=None,
            help="Template release to apply. Resolved to a full commit SHA and recorded.",
        )
        life.add_argument(
            "--repo",
            default=None,
            metavar="OWNER/NAME",
            help="Template repository the tag belongs to.",
        )
        life.add_argument(
            "--allow-unreleased",
            action="store_true",
            help="Run from an unpinned remote source, recorded as a development run.",
        )
        if name == "update":
            life.add_argument(
                "--check",
                action="store_true",
                help="Report whether a newer release exists, and change nothing.",
            )
        life.add_argument(
            "--apply-plan",
            type=Path,
            default=None,
            metavar="PLAN.JSON",
            help="Apply this plan instead of producing a new one.",
        )

    held = sub.add_parser("lease", help="The pull request control plane lease (#19).")
    held.add_argument("--remote", default=None, help="Operate on this remote instead of locally.")
    held_sub = held.add_subparsers(dest="lease_command", required=True)

    def add_target(parser: argparse.ArgumentParser) -> None:
        target = parser.add_mutually_exclusive_group(required=True)
        target.add_argument("--pr", type=int, help="Pull request number.")
        target.add_argument("--lane", help="Destination branch, for a lane lease.")

    held_acquire = held_sub.add_parser("acquire", help="Take the lease, or reclaim an expired one.")
    add_target(held_acquire)
    held_acquire.add_argument("--base", required=True, help="Destination branch.")
    held_acquire.add_argument("--head", required=True, help="Full head SHA this work is against.")
    held_acquire.add_argument("--ttl", type=float, default=900.0, help="Seconds. Default 900.")
    held_acquire.add_argument("--holder", default=None, help="Who is holding it, for the report.")

    held_renew = held_sub.add_parser("renew", help="Extend a lease you hold.")
    add_target(held_renew)
    held_renew.add_argument("--capability", required=True)
    held_renew.add_argument("--head", required=True, help="The head you believe you are on.")
    held_renew.add_argument("--ttl", type=float, default=900.0)

    held_release = held_sub.add_parser("release", help="Give the lease back.")
    add_target(held_release)
    held_release.add_argument("--capability", required=True)

    held_inspect = held_sub.add_parser("inspect", help="Who holds it, and for how much longer.")
    add_target(held_inspect)

    held_sub.add_parser("scan", help="Find writes to pull request state that skip the lease.")

    policy = sub.add_parser("settings", help="Repository settings as policy files (#13).")
    policy.add_argument("--repo", default=None, metavar="OWNER/NAME", help="Defaults to this one.")
    policy.add_argument("--area", default=None, help="One policy area instead of all of them.")
    policy_sub = policy.add_subparsers(dest="settings_command", required=True)
    policy_sub.add_parser("plan", help="Read-only: what differs from the policy files.")
    policy_sub.add_parser("check", help="Read-only: exit 1 when something drifted.")
    policy_sub.add_parser(
        "apply", help="Write one area. Branch rules and security switches are not included."
    )

    documents = sub.add_parser("docs", help="The durable documentation layers (#10).")
    documents_sub = documents.add_subparsers(dest="docs_command", required=True)
    documents_sub.add_parser("validate", help="Check specs and decision records.")

    tooling = sub.add_parser("tools", help="The pinned external checks (#11).")
    tooling_sub = tooling.add_subparsers(dest="tools_command", required=True)
    tooling_install = tooling_sub.add_parser(
        "install", help="Download one pinned tool and print its path."
    )
    tooling_install.add_argument("name", help="Tool name from policies/tools.json.")

    state = sub.add_parser("status", help="Where this project stands, and what to run next (#4).")
    state.add_argument("path", nargs="?", type=Path, default=None, help="Defaults to -C or cwd.")
    state.add_argument("--json", action="store_true", help="Machine-readable output.")
    state.add_argument(
        "--no-render",
        action="store_true",
        help="Skip drift detection; report drift as unknown instead of fetching the template.",
    )
    state.add_argument(
        "--policy",
        action="store_true",
        help="Also compare repository settings. Needs gh; without it policy_drift stays unknown.",
    )

    pull = sub.add_parser("pr", help="The pull request contract (#8).")
    pull.add_argument("--repo", default=None, metavar="OWNER/NAME", help="Defaults to this one.")
    pull_sub = pull.add_subparsers(dest="pr_command", required=True)
    pull_check = pull_sub.add_parser("validate", help="Check one pull request against the policy.")
    pull_check.add_argument("number", type=int)

    stone = sub.add_parser("milestone", help="The milestone contract (#9).")
    stone.add_argument("--repo", default=None, metavar="OWNER/NAME", help="Defaults to this one.")
    stone_sub = stone.add_subparsers(dest="milestone_command", required=True)

    stone_create = stone_sub.add_parser(
        "create", help="Create a milestone and its Feature parent, then preflight."
    )
    stone_create.add_argument("--title", required=True, help="Milestone name, without a number.")
    stone_create.add_argument("--due-on", required=True, help="ISO 8601 date, e.g. 2026-11-30.")
    stone_create.add_argument(
        "--description-file", required=True, type=Path, help="The seven-section description."
    )

    stone_sub.add_parser("detect-open", help="Print the single open milestone, if there is one.")

    stone_check = stone_sub.add_parser("preflight", help="Check a milestone against the contract.")
    stone_check.add_argument("number", type=int)
    stone_check.add_argument("--parent", type=int, default=None, help="Feature parent issue.")

    stone_done = stone_sub.add_parser(
        "reconcile", help="Delivered / closed without merged PR / pending, before closing."
    )
    stone_done.add_argument("number", type=int)

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


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    root = commands._resolve_root(args.directory)

    try:
        if args.command == "config":
            if args.config_command == "get":
                return commands.cmd_config_get(root, args.key)
            return commands.cmd_config_validate(root)
        if args.command == "ownership":
            if args.ownership_command == "sync":
                return commands.cmd_ownership_sync(root, args.check)
            return commands.cmd_ownership_list(root)
        if args.command == "issue":
            if args.issue_command == "validate-title":
                return commands.cmd_issue_validate_title(args.title)
            return commands.cmd_issue_check_forms(root)
        if args.command in ("create", "adopt", "update"):
            target = args.path.resolve() if args.path else root
            if getattr(args, "check", False):
                return commands.cmd_update_check(
                    target, args.repo or commands.TEMPLATE_REPO, as_json=True
                )
            return commands.cmd_lifecycle(target, plan_module.Mode(args.command), args)
        if args.command == "lease":
            return commands.cmd_lease(root, args)
        if args.command == "settings":
            client_repo = args.repo or gh.Client().current_repo()
            return commands.cmd_settings(root, client_repo, args.settings_command, args.area)
        if args.command == "docs":
            return commands.cmd_docs_validate(root)
        if args.command == "tools":
            return commands.cmd_tools_install(root, args.name)
        if args.command == "status":
            target = args.path.resolve() if args.path else root
            return commands.cmd_status(
                target,
                args.json,
                allow_render=not args.no_render,
                check_policy=args.policy,
            )
        if args.command == "pr":
            client = gh.Client()
            return commands.cmd_pr_validate(
                client, args.repo or client.current_repo(), root, args.number
            )
        if args.command == "milestone":
            client = gh.Client()
            repo = args.repo or client.current_repo()
            if args.milestone_command == "create":
                return commands.cmd_milestone_create(client, repo, args)
            if args.milestone_command == "detect-open":
                return commands.cmd_milestone_detect_open(client, repo)
            if args.milestone_command == "preflight":
                return commands.cmd_milestone_preflight(client, repo, args.number, args.parent)
            return commands.cmd_milestone_reconcile(client, repo, args.number)
        if args.command == "verify":
            return commands.cmd_verify(root, args.tier, args.stage, args.base)
        if args.command == "selfhost":
            return commands.cmd_selfhost(root, apply_changes=args.selfhost_command == "apply")
    except lease.LeaseUnavailable as exc:
        # A definite no, not a failure to answer -- see the exit code table in
        # docs/lease-carrier.md.
        print(f"ai-scheme: {exc}", file=sys.stderr)
        return EXIT_NO
    except (
        config.ConfigError,
        gh.GhError,
        lease.LeaseError,
        ownership.OwnershipError,
        selfhost.SelfHostError,
    ) as exc:
        print(f"ai-scheme: {exc}", file=sys.stderr)
        return EXIT_UNDETERMINED

    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
