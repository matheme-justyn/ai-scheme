"""Finding writes to the pull request control plane that skip the lease (#19)."""

from __future__ import annotations

from pathlib import Path

from ai_scheme import leasescan


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_this_repository_has_no_unleased_writes() -> None:
    from ai_scheme.paths import package_root

    assert leasescan.scan(package_root()) == []


def test_a_gh_pr_write_is_found(tmp_path: Path) -> None:
    write(tmp_path / "scripts" / "ship", "#!/usr/bin/env bash\ngh pr merge 12 --squash\n")

    findings = leasescan.scan(tmp_path)

    assert len(findings) == 1
    assert findings[0].line == 2
    assert "gh pr write" in str(findings[0])


def test_reads_are_not_writes(tmp_path: Path) -> None:
    write(
        tmp_path / "scripts" / "look",
        "#!/usr/bin/env bash\ngh pr view 12 --json title\ngh pr checks 12\n",
    )

    assert leasescan.scan(tmp_path) == []


def test_a_rest_write_to_pulls_is_found(tmp_path: Path) -> None:
    write(
        tmp_path / ".github" / "workflows" / "ship.yml",
        "jobs:\n  a:\n    steps:\n      - run: gh api --method PATCH repos/o/r/pulls/12\n",
    )

    assert len(leasescan.scan(tmp_path)) == 1


def test_a_graphql_mutation_is_found(tmp_path: Path) -> None:
    write(
        tmp_path / "scripts" / "ship", 'gh api graphql -f query="mutation { mergePullRequest }"\n'
    )

    assert len(leasescan.scan(tmp_path)) == 1


def test_a_rule_written_in_a_comment_is_not_a_call(tmp_path: Path) -> None:
    """The POC's scanner fired on prose describing the rule it enforced."""
    write(
        tmp_path / "scripts" / "notes",
        "#!/usr/bin/env bash\n# never call gh pr merge without a lease\n"
        "echo 'see the docs'  # gh pr ready is also a write\n",
    )

    assert leasescan.scan(tmp_path) == []


def test_text_inside_backticks_is_prose(tmp_path: Path) -> None:
    write(tmp_path / "scripts" / "help", 'echo "run `gh pr merge` yourself"\n')

    assert leasescan.scan(tmp_path) == []


def test_an_exception_needs_an_exact_path_and_an_issue(tmp_path: Path) -> None:
    write(tmp_path / "scripts" / "ship", "gh pr merge 12 --squash\n")
    write(
        tmp_path / leasescan.EXCEPTIONS_RELPATH,
        '{"exceptions": [{"path": "scripts/ship", "issue": "#99"}]}',
    )

    assert leasescan.scan(tmp_path) == []


def test_an_exception_without_an_issue_does_not_count(tmp_path: Path) -> None:
    write(tmp_path / "scripts" / "ship", "gh pr merge 12 --squash\n")
    write(tmp_path / leasescan.EXCEPTIONS_RELPATH, '{"exceptions": [{"path": "scripts/ship"}]}')

    assert len(leasescan.scan(tmp_path)) == 1
