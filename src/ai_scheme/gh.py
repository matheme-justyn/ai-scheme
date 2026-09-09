"""A thin, injectable wrapper around the `gh` CLI.

Everything that talks to GitHub goes through `Client.api`, so tests can hand
the commands a recorded response instead of a network, and so that one place
decides what happens when `gh` is missing or not authenticated.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from collections.abc import Callable, Sequence
from typing import Any


class GhError(Exception):
    """gh is unavailable, unauthenticated, or returned a failure."""


Runner = Callable[[Sequence[str]], str]


def _subprocess_runner(args: Sequence[str]) -> str:
    if shutil.which("gh") is None:
        raise GhError("gh is not installed; see https://cli.github.com")
    result = subprocess.run(["gh", *args], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise GhError((result.stderr or result.stdout).strip() or "gh failed")
    return result.stdout


class Client:
    def __init__(self, runner: Runner | None = None) -> None:
        self._run = runner or _subprocess_runner

    def api(self, path: str, *, method: str = "GET", fields: dict[str, Any] | None = None) -> Any:
        args = ["api", path, "--method", method]
        for key, value in (fields or {}).items():
            args += ["-f", f"{key}={value}"]
        output = self._run(args)
        if not output.strip():
            return None
        try:
            return json.loads(output)
        except json.JSONDecodeError as exc:
            raise GhError(f"gh returned output that is not JSON: {exc}") from exc

    def current_repo(self) -> str:
        """`owner/name` for the repository the working directory belongs to."""
        output = self._run(["repo", "view", "--json", "nameWithOwner", "-q", ".nameWithOwner"])
        name = output.strip()
        if not name:
            raise GhError("gh could not name the current repository")
        return name

    def issue(self, repo: str, number: int) -> dict[str, Any]:
        return self.api(f"repos/{repo}/issues/{number}")

    def closed_by_merged_pull_request(self, repo: str, number: int) -> bool:
        """Whether a merged pull request closed this issue.

        The REST timeline does not say so -- a squash merge that closes an
        issue through a `Closes #N` keyword leaves a `closed` event with no
        commit. The linked-pull-request field does say so, and then the pull
        request itself is asked whether it was merged rather than assumed.
        """
        output = self._run(
            [
                "issue",
                "view",
                str(number),
                "--repo",
                repo,
                "--json",
                "closedByPullRequestsReferences",
            ]
        )
        try:
            references = (json.loads(output) or {}).get("closedByPullRequestsReferences") or []
        except json.JSONDecodeError as exc:
            raise GhError(f"gh returned output that is not JSON: {exc}") from exc
        for reference in references:
            pull = self.api(f"repos/{repo}/pulls/{reference['number']}")
            if pull and pull.get("merged_at"):
                return True
        return False

    def pull_request(self, repo: str, number: int) -> dict[str, Any]:
        """The fields the policy needs, in gh's own JSON shape."""
        output = self._run(
            [
                "pr",
                "view",
                str(number),
                "--repo",
                repo,
                "--json",
                "number,title,body,isDraft,headRefName,labels,milestone,reviewRequests,author",
            ]
        )
        try:
            return json.loads(output)
        except json.JSONDecodeError as exc:
            raise GhError(f"gh returned output that is not JSON: {exc}") from exc

    def open_milestones(self, repo: str) -> list[dict[str, Any]]:
        return self.api(f"repos/{repo}/milestones?state=open") or []

    def milestone(self, repo: str, number: int) -> dict[str, Any]:
        return self.api(f"repos/{repo}/milestones/{number}")

    def issues_in_milestone(self, repo: str, number: int) -> list[dict[str, Any]]:
        path = f"repos/{repo}/issues?milestone={number}&state=all&per_page=100"
        return self.api(path) or []

    def create_milestone(self, repo: str, title: str, due_on: str, description: str) -> dict:
        return self.api(
            f"repos/{repo}/milestones",
            method="POST",
            fields={"title": title, "due_on": due_on, "description": description},
        )

    def create_issue(self, repo: str, title: str, body: str, labels: Sequence[str]) -> dict:
        fields: dict[str, Any] = {"title": title, "body": body}
        args = ["api", f"repos/{repo}/issues", "--method", "POST"]
        for key, value in fields.items():
            args += ["-f", f"{key}={value}"]
        for label in labels:
            args += ["-f", f"labels[]={label}"]
        output = self._run(args)
        return json.loads(output) if output.strip() else {}
