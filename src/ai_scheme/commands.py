"""What each command does, kept out of the parser (#5).

`cli.py` decides what the user asked for; this module answers it. The split
exists because the argument parser was growing a second job, and the issue that
asked for these commands also asked for no single file to run much past five
hundred lines.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from ai_scheme import __version__, config, gh, issues, milestones, ownership, pullrequests, selfhost
from ai_scheme import apply as apply_module
from ai_scheme import plan as plan_module
from ai_scheme import status as status_module
from ai_scheme import verify as verify_module
from ai_scheme.paths import OWNERSHIP_RELPATH, UNINSTALL_RELPATH, package_root, repo_root
from ai_scheme.tiers import Tier, changed_paths, classify

EXIT_OK = 0
EXIT_NO = 1
EXIT_UNDETERMINED = 2


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


def _report(subject: str, problems: list[milestones.Problem]) -> int:
    if not problems:
        print(f"{subject}: ok")
        return EXIT_OK
    print(f"{subject}: {len(problems)} problem(s)", file=sys.stderr)
    for problem in problems:
        print(f"  {problem}", file=sys.stderr)
    return EXIT_NO


def cmd_milestone_create(client: gh.Client, repo: str, args: Any) -> int:
    description = args.description_file.read_text(encoding="utf-8")
    problems = milestones.validate_description(description)
    if problems:
        # Refusing before the milestone exists beats editing it afterwards.
        return _report(str(args.description_file), problems)

    due_on = args.due_on if "T" in args.due_on else f"{args.due_on}T00:00:00Z"
    milestone = client.create_milestone(repo, args.title, due_on, description)
    number = milestone["number"]
    parent = client.create_issue(
        repo,
        milestones.parent_title(number, args.title),
        f"Milestone {number} 的 Feature parent 兼追蹤 Issue。"
        f"\n\n完成證據與提前終止都寫在這裡。\n\n## 問題\n\n見 milestone 描述的 Problem 段。"
        f"\n\n## 完成條件\n\n見 milestone 描述的 Acceptance criteria 段。\n\n## 補充\n\n",
        ["type:feature"],
    )
    print(f"milestone {number}: {args.title}")
    print(f"parent issue #{parent.get('number')}: {parent.get('title')}")
    return _report(
        f"milestone {number}", milestones.preflight(client.milestone(repo, number), parent)
    )


def cmd_milestone_detect_open(client: gh.Client, repo: str) -> int:
    open_milestones = client.open_milestones(repo)
    if len(open_milestones) != 1:
        print(f"{len(open_milestones)} open milestone(s)", file=sys.stderr)
        return EXIT_NO
    print(open_milestones[0]["title"])
    return EXIT_OK


def cmd_milestone_preflight(client: gh.Client, repo: str, number: int, parent: int | None) -> int:
    milestone = client.milestone(repo, number)
    parent_issue = client.issue(repo, parent) if parent else None
    return _report(f"milestone {number}", milestones.preflight(milestone, parent_issue))


def cmd_milestone_reconcile(client: gh.Client, repo: str, number: int) -> int:
    raw = client.issues_in_milestone(repo, number)
    enriched = []
    for issue in raw:
        if "pull_request" in issue:
            continue
        merged = False
        if issue.get("state") == "closed":
            merged = client.closed_by_merged_pull_request(repo, issue["number"])
        enriched.append({**issue, "merged_pull_request": merged})

    rows = milestones.reconcile(enriched)
    width = max((len(row.state) for row in rows), default=0)
    for row in sorted(rows, key=lambda item: item.number):
        print(f"{row.state.ljust(width)}  #{row.number}  {row.title}")
    pending = [row for row in rows if row.state != milestones.State.DELIVERED]
    if pending:
        print(f"{len(pending)} issue(s) not delivered by a merged pull request", file=sys.stderr)
        return EXIT_NO
    return EXIT_OK


def _answers_for(root: Path, mode: plan_module.Mode, data: list[str]) -> dict[str, Any]:
    answers: dict[str, Any] = {}
    if mode is plan_module.Mode.UPDATE:
        answers.update(config.load_answers(root))
    for item in data:
        key, separator, value = item.partition("=")
        if not separator:
            raise config.ConfigError(f"--data expects KEY=VALUE, got {item!r}")
        answers[key] = value
    return answers


def cmd_lifecycle(root: Path, mode: plan_module.Mode, args: Any) -> int:
    manifest = ownership.load(package_root())

    if args.apply_plan:
        raw = json.loads(args.apply_plan.read_text(encoding="utf-8"))
        stored = plan_module.Plan.from_dict(raw)
        with tempfile.TemporaryDirectory(prefix="ai-scheme-apply-") as temporary:
            rendered = Path(temporary) / "rendered"
            selfhost.render_into(stored.source, stored.answers, rendered, ref=stored.source_ref)
            digest = plan_module.digest_of(stored.entries, rendered)
            if digest != stored.digest:
                print(
                    "the plan describes a different rendering: "
                    f"plan {stored.digest[:12]}, now {digest[:12]}",
                    file=sys.stderr,
                )
                print("produce a new plan", file=sys.stderr)
                return EXIT_NO
            blocks = selfhost.managed_blocks(package_root())
            try:
                applied = apply_module.apply_plan(stored, root, rendered, blocks=blocks)
            except apply_module.ApplyRefused as refused:
                print("refused to apply:", file=sys.stderr)
                for reason in refused.reasons:
                    print(f"  {reason}", file=sys.stderr)
                return EXIT_NO
        print(f"wrote {len(applied.written)} path(s), left {len(applied.skipped)} alone")
        print("now run scripts/verify")
        return EXIT_OK

    answers = _answers_for(root, mode, args.data)
    source = args.source or str(answers.get("_src_path") or package_root())
    out = args.out or Path(tempfile.mkdtemp(prefix="ai-scheme-plan-"))
    out.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="ai-scheme-candidate-") as temporary:
        rendered = Path(temporary) / "rendered"
        selfhost.render_into(source, answers, rendered, ref=args.ref)
        previous = None
        if mode is plan_module.Mode.UPDATE and answers.get("_commit"):
            previous_root = Path(temporary) / "previous"
            try:
                selfhost.render_into(source, answers, previous_root, ref=answers["_commit"])
                previous = previous_root
            except Exception:
                # Without the previous rendering there is no way to tell a
                # local edit from an upstream one, so every difference becomes
                # a manual merge. Fail closed, not open.
                previous = None
        built = plan_module.build(
            mode,
            root,
            source=source,
            source_ref=args.ref or answers.get("_commit"),
            answers={key: value for key, value in answers.items() if not key.startswith("_")},
            rendered_root=rendered,
            manifest=manifest,
            previous_root=previous,
        )

    plan_path = out / "plan.json"
    report_path = out / "plan.md"
    plan_path.write_text(built.to_json(), encoding="utf-8")
    report_path.write_text(built.report(), encoding="utf-8")

    for action in plan_module.Action:
        count = len(built.by_action(action))
        if count:
            print(f"{action.value}: {count}")
    print(f"plan:   {plan_path}")
    print(f"report: {report_path}")
    print(f"apply:  ai-scheme {mode.value} --apply-plan {plan_path}")
    return EXIT_OK


def cmd_status(root: Path, as_json: bool, allow_render: bool) -> int:
    facts = status_module.collect(root, target_version=__version__, allow_render=allow_render)
    answer = status_module.judge(facts)

    if as_json:
        print(json.dumps(answer.as_dict(), indent=2, ensure_ascii=False, sort_keys=True))
        return EXIT_OK

    print(f"state:   {answer.state}")
    print(f"reason:  {answer.reason}")
    print(f"version: {answer.current_version or '-'} -> {answer.target_version or '-'}")
    if answer.drift == status_module.UNKNOWN:
        print("drift:   unknown (the template could not be rendered)")
    elif answer.drift:
        print(f"drift:   {len(answer.drift)} path(s)")
        for path in answer.drift:
            print(f"           {path}")
    if answer.mechanism_config_detected:
        print("note:    a mechanism-layer config.toml is present; this layer does not read it")
    print(f"next:    {answer.next_command or 'nothing to do'}")
    return EXIT_OK


def cmd_pr_validate(client: gh.Client, repo: str, root: Path, number: int) -> int:
    pull = client.pull_request(repo, number)
    closed = pullrequests.closes(pull.get("body", ""))
    issue = None
    if closed:
        try:
            issue = client.issue(repo, closed[0])
        except gh.GhError:
            issue = None

    try:
        mode = config.get(config.load_answers(root), "collaboration_mode")
    except config.ConfigError:
        # A repository without an answers file is not a reason to skip the
        # check; solo is the weaker of the two, so it cannot pass something
        # team mode would fail.
        mode = "solo"

    problems = pullrequests.validate(pull, issue, collaboration_mode=str(mode))
    state = "draft" if pull.get("isDraft") else "ready"
    if not problems:
        print(f"pull request #{number} ({state}): ok")
        return EXIT_OK
    print(f"pull request #{number} ({state}): {len(problems)} problem(s)", file=sys.stderr)
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
