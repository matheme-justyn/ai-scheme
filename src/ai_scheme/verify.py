"""The one verification entry point, shared by a laptop and by CI (#11).

Every check is a stage: it has a name, the tier it starts running at, and a
callable that returns a `StageResult`. `run` picks the stages for a tier and
reports each one, so a failure names the stage to rerun rather than a line
number in a three-hundred-line shell script.
"""

from __future__ import annotations

import re
import subprocess
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from ai_scheme import issues, ownership, selfhost, tools
from ai_scheme.paths import TEMPLATE_RELPATH
from ai_scheme.tiers import Tier

MARKDOWN_LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE = re.compile(r"^\s*(```|~~~)")

LINK_POLICY_RELPATH = Path("policies/docs-links.yml")

# template/ holds the same documents with Jinja file names: a link to
# ../terminology/ is correct in the rendering and unresolvable in the source.
# The rendered copy at the repository root is what this stage checks.
LINK_CHECK_SKIP_PREFIXES = (TEMPLATE_RELPATH.as_posix() + "/",)


@dataclass(frozen=True)
class LinkPolicy:
    """Which dangling links are deliberate, from policies/docs-links.yml."""

    forward_references: frozenset[str] = frozenset()
    illustrative: frozenset[str] = frozenset()

    @classmethod
    def load(cls, root: Path) -> LinkPolicy:
        path = root / LINK_POLICY_RELPATH
        if not path.is_file():
            return cls()
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        return cls(
            forward_references=frozenset(
                entry["target"] for entry in raw.get("forward_references") or []
            ),
            illustrative=frozenset(entry["path"] for entry in raw.get("illustrative") or []),
        )


@dataclass(frozen=True)
class StageResult:
    ok: bool
    detail: str = ""
    findings: tuple[str, ...] = ()


@dataclass(frozen=True)
class Stage:
    name: str
    tier: Tier
    run: Callable[[Path], StageResult]
    summary: str = ""


def _run(command: list[str], root: Path) -> tuple[int, str]:
    result = subprocess.run(command, cwd=root, capture_output=True, text=True, check=False)
    return result.returncode, (result.stdout + result.stderr).strip()


SHELL_GLOBS = ("scripts/*", "hooks/*", "template/scripts/*", "template/hooks/*")

# `"$(dirname "$0")/other"` and `scripts/other` -- the two ways a script in this
# template reaches a sibling.
SIBLING_CALL = re.compile(r"""\$\(dirname\s+"?\$0"?\)/([A-Za-z0-9._-]+)""")
SCRIPTS_CALL = re.compile(r"(?<![\w/.-])scripts/([A-Za-z0-9._-]+)")


def sibling_calls(script: Path, root: Path) -> list[tuple[int, str, Path]]:
    """Every sibling script a shell script names, with where it should be.

    A syntax check proves a script parses, not that what it calls exists. The
    mechanism layer lost its main install path to exactly this: three call
    sites for a script that had been deleted, under `set -e`, with CI green.
    """
    calls: list[tuple[int, str, Path]] = []
    for number, line in enumerate(script.read_text(encoding="utf-8").splitlines(), start=1):
        code = line.split("#", 1)[0] if not line.lstrip().startswith("#") else ""
        for match in SIBLING_CALL.finditer(code):
            calls.append((number, match.group(1), script.parent / match.group(1)))
        for match in SCRIPTS_CALL.finditer(code):
            # `scripts/x` is written relative to the repository root -- and to
            # the template body's root, for a script that ships.
            base = root / "template" if "template" in script.relative_to(root).parts else root
            calls.append((number, f"scripts/{match.group(1)}", base / "scripts" / match.group(1)))
    return calls


def shell_files(root: Path) -> list[Path]:
    found: list[Path] = []
    for pattern in SHELL_GLOBS:
        for path in sorted(root.glob(pattern)):
            if path.is_file() and path.suffix != ".py":
                found.append(path)
    return found


def stage_static(root: Path) -> StageResult:
    """Whitespace, shell, workflows and secrets -- with pinned tools (#11)."""
    findings: list[str] = []
    code, output = _run(["git", "diff", "--check", "HEAD"], root)
    if code not in (0, 128) and output:
        findings.extend(output.splitlines())

    scripts = shell_files(root)
    if scripts:
        try:
            shellcheck = tools.ensure(root, "shellcheck")
        except tools.ToolError as exc:
            # Fail closed: a check that could not run is not a check that passed.
            return StageResult(False, "shellcheck unavailable", (str(exc),))
        code, output = _run([str(shellcheck), *(str(path) for path in scripts)], root)
        if code != 0:
            findings.append(output)

    for script in scripts:
        for number, name, expected in sibling_calls(script, root):
            if not expected.exists():
                findings.append(
                    f"{script.relative_to(root)}:{number}: calls {name}, which does not exist"
                )

    workflows = sorted(root.glob(".github/workflows/*.yml"))
    if workflows:
        try:
            actionlint = tools.ensure(root, "actionlint")
        except tools.ToolError as exc:
            return StageResult(False, "actionlint unavailable", (str(exc),))
        code, output = _run([str(actionlint), *(str(path) for path in workflows)], root)
        if code != 0:
            findings.append(output)

    try:
        gitleaks = tools.ensure(root, "gitleaks")
    except tools.ToolError as exc:
        return StageResult(False, "gitleaks unavailable", (str(exc),))
    gitleaks_command = [str(gitleaks), "dir", ".", "--no-banner", "--redact"]
    if (root / ".gitleaks.toml").is_file():
        gitleaks_command += ["--config", ".gitleaks.toml"]
    code, output = _run(gitleaks_command, root)
    if code != 0:
        findings.append(output)

    if findings:
        return StageResult(False, "static analysis found problems", tuple(findings))
    return StageResult(True, "shellcheck, actionlint and gitleaks are clean")


def prose_only(text: str) -> str:
    """The document with fenced code blocks blanked out.

    A link inside a fence is an illustration of markdown, not a link this
    repository has to honour -- ADR 0006 already forbids fencing markdown as
    markdown, and what remains inside fences is sample output.
    """
    lines = text.splitlines()
    kept: list[str] = []
    fence: str | None = None
    for line in lines:
        match = FENCE.match(line)
        if fence is None and match:
            fence = match.group(1)
            kept.append("")
            continue
        if fence is not None:
            if match and match.group(1) == fence:
                fence = None
            kept.append("")
            continue
        kept.append(line)
    return "\n".join(kept)


def _markdown_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*.md")):
        parts = set(path.relative_to(root).parts)
        if parts & {".git", ".venv", "node_modules", ".cache"}:
            continue
        yield path


def stage_docs(root: Path) -> StageResult:
    """Every relative markdown link resolves to a file that exists.

    The three-repository split left more than a dozen links pointing at paths
    that had moved. They were fixed by hand once; this stage is why they do not
    grow back.
    """
    policy = LinkPolicy.load(root)
    findings: list[str] = []
    checked = 0
    for document in _markdown_files(root):
        relative_document = document.relative_to(root).as_posix()
        if relative_document.startswith(LINK_CHECK_SKIP_PREFIXES):
            continue
        if relative_document in policy.illustrative:
            continue
        text = prose_only(document.read_text(encoding="utf-8", errors="replace"))
        for target in MARKDOWN_LINK.findall(text):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            relative = target.split("#", 1)[0]
            if not relative or Path(relative).name in policy.forward_references:
                continue
            checked += 1
            resolved = (document.parent / relative).resolve()
            if not resolved.exists():
                findings.append(f"{relative_document} -> {target}")
    if findings:
        return StageResult(False, f"{len(findings)} dangling link(s)", tuple(findings))
    return StageResult(True, f"{checked} relative link(s) resolve")


def stage_python(root: Path) -> StageResult:
    findings: list[str] = []
    for command in (
        ["uv", "run", "ruff", "check", "."],
        ["uv", "run", "ruff", "format", "--check", "."],
        # Types are checked over src only: the test helpers build dataclasses
        # from dictionaries on purpose, which is exactly what a type checker
        # cannot see through.
        ["uv", "run", "ty", "check", "src"],
        # The fixtures that render the real template are the full tier's job,
        # in the template stage. This one stays quick enough to run on every
        # commit.
        ["uv", "run", "pytest", "-q", "-m", "not slow"],
    ):
        code, output = _run(command, root)
        if code != 0:
            findings.append(f"$ {' '.join(command)}\n{output}")
    if findings:
        return StageResult(False, "lint or tests failed", tuple(findings))
    return StageResult(True, "ruff, ty and pytest pass")


def stage_template(root: Path) -> StageResult:
    """The template body, and the tree this repository renders from it."""
    if not (root / TEMPLATE_RELPATH).is_dir():
        # A generated project has no template body to check. Saying so beats
        # both a spurious pass and a failure the project cannot act on.
        return StageResult(True, "not a template repository, nothing to render")

    findings: list[str] = []

    manifest = ownership.load(root)
    copier_text = (root / "copier.yml").read_text(encoding="utf-8")
    if ownership.sync_copier(copier_text, manifest) != copier_text:
        findings.append("copier.yml is out of date with ownership.yml")
    uninstall_path = root / TEMPLATE_RELPATH / "docs" / "uninstall.md"
    wanted = ownership.uninstall_doc(manifest)
    if not uninstall_path.is_file() or uninstall_path.read_text(encoding="utf-8") != wanted:
        findings.append(f"{uninstall_path.relative_to(root)} is out of date with ownership.yml")
    if findings:
        findings.append("run `ai-scheme ownership sync`")

    code, output = _run(["uv", "run", "pytest", "-q", "-m", "slow"], root)
    if code != 0:
        findings.append(f"generated-project fixtures failed\n{output}")

    with selfhost.render_to_temp(root) as handle:
        differences = selfhost.compare(root, Path(handle) / "rendered")
    if differences:
        findings.extend(str(difference) for difference in differences)
        findings.append("run `ai-scheme selfhost apply`")

    if findings:
        return StageResult(False, "the tree and the template disagree", tuple(findings))
    return StageResult(
        True, "generated files, the rendered tree and the generated-project fixtures are current"
    )


def stage_issues(root: Path) -> StageResult:
    """The issue forms still ask three questions, with declared labels."""
    if not (root / issues.FORM_RELDIR).is_dir():
        return StageResult(True, "no issue forms in this project")
    problems = issues.validate_forms(root)
    if problems:
        return StageResult(
            False, "the forms drifted from the contract", tuple(str(p) for p in problems)
        )
    return StageResult(True, "issue forms match the three-field contract")


def stage_dependencies(root: Path) -> StageResult:
    """Known vulnerabilities in what this project depends on."""
    lockfiles = [
        name for name in ("uv.lock", "package-lock.json", "Cargo.lock") if (root / name).is_file()
    ]
    if not lockfiles:
        return StageResult(True, "no lockfile to scan")

    try:
        scanner = tools.ensure(root, "osv-scanner")
    except tools.ToolError as exc:
        return StageResult(False, "osv-scanner unavailable", (str(exc),))

    arguments = [str(scanner), "scan", "source"]
    for name in lockfiles:
        arguments += ["--lockfile", name]
    code, output = _run(arguments, root)
    # 0 clean, 1 vulnerabilities found; anything else is the scanner itself
    # failing, which is not a pass either.
    if code != 0:
        return StageResult(False, f"osv-scanner exited {code}", (output,))
    return StageResult(True, f"no known vulnerabilities in {', '.join(lockfiles)}")


STAGES: tuple[Stage, ...] = (
    Stage("static", Tier.DOCS, stage_static, "whitespace and shell syntax"),
    Stage("docs", Tier.DOCS, stage_docs, "relative markdown links resolve"),
    Stage("issues", Tier.DOCS, stage_issues, "issue forms match the contract"),
    Stage("python", Tier.FAST, stage_python, "ruff and pytest"),
    Stage("template", Tier.FULL, stage_template, "ownership and rendered tree"),
    Stage("dependencies", Tier.FULL, stage_dependencies, "known vulnerabilities"),
)


def stages_for(tier: Tier) -> tuple[Stage, ...]:
    return tuple(stage for stage in STAGES if tier.includes(stage.tier))


@dataclass
class Report:
    tier: Tier
    results: list[tuple[Stage, StageResult]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(result.ok for _, result in self.results)

    def lines(self) -> list[str]:
        out = [f"tier: {self.tier.value}"]
        for stage, result in self.results:
            mark = "ok  " if result.ok else "FAIL"
            out.append(f"{mark} {stage.name}: {result.detail}")
            if not result.ok:
                out.extend(f"       {finding}" for finding in result.findings)
        return out


def run(root: Path, tier: Tier, only: str | None = None) -> Report:
    report = Report(tier=tier)
    for stage in stages_for(tier):
        if only and stage.name != only:
            continue
        report.results.append((stage, stage.run(root)))
    return report
