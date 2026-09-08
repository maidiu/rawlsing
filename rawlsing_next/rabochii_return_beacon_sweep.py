"""Reliable immediate and fallback branch selection for the Rawlsing Return Beacon.

Operational infrastructure only. Certification remains owned by
``rabochii_return_beacon.py``; this module only selects which worker branches
should be presented to that proven certification core.
"""
from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Mapping, Sequence

try:  # package import under pytest / module use
    from .rabochii_return_beacon import (
        DEFAULT_INBOX_ISSUE,
        GitHubClient,
        notify_if_certified,
    )
except ImportError:  # direct script execution from rawlsing_next/
    from rabochii_return_beacon import (
        DEFAULT_INBOX_ISSUE,
        GitHubClient,
        notify_if_certified,
    )


def _branch_from_node(node: Mapping[str, Any], *, cutoff: datetime) -> str | None:
    """Return one recent return-shaped agent branch from a GraphQL Ref node."""
    branch = node.get("name")
    target = node.get("target")
    if not isinstance(branch, str) or not branch.startswith("agent/"):
        return None
    if not isinstance(target, Mapping):
        return None
    committed = target.get("committedDate")
    headline = target.get("messageHeadline")
    if not isinstance(committed, str) or not isinstance(headline, str):
        return None
    if "return" not in headline.lower():
        return None
    try:
        instant = datetime.fromisoformat(committed.replace("Z", "+00:00"))
    except ValueError:
        return None
    return branch if instant >= cutoff else None


def discover_recent_return_branches(
    client: GitHubClient,
    *,
    hours: int = 72,
    max_pages: int = 100,
) -> list[str]:
    """Discover recent ``agent/*`` return tips from the full heads namespace.

    GitHub GraphQL ``Ref.name`` is interpreted relative to ``refs/heads/``.
    The original beacon queried ``refs/heads/agent/`` and then required the
    returned name to start with ``agent/``; the live smoke court demonstrated
    that combination could discard all worker branches. Querying the full heads
    namespace makes the returned names unambiguous and leaves the ``agent/``
    filter local and testable.
    """
    owner, name = client.repo.split("/", 1)
    query = """
    query($owner: String!, $name: String!, $after: String) {
      repository(owner: $owner, name: $name) {
        refs(refPrefix: "refs/heads/", first: 100, after: $after) {
          nodes {
            name
            target {
              ... on Commit { oid committedDate messageHeadline }
            }
          }
          pageInfo { hasNextPage endCursor }
        }
      }
    }
    """
    cutoff = datetime.now(timezone.utc) - timedelta(hours=hours)
    branches: set[str] = set()
    after: str | None = None

    for _ in range(max_pages):
        payload = client._request(
            "POST",
            "/graphql",
            body={
                "query": query,
                "variables": {"owner": owner, "name": name, "after": after},
            },
        )
        repo = payload.get("data", {}).get("repository") if isinstance(payload, Mapping) else None
        refs = repo.get("refs") if isinstance(repo, Mapping) else None
        if not isinstance(refs, Mapping):
            break

        for node in refs.get("nodes") or []:
            if not isinstance(node, Mapping):
                continue
            branch = _branch_from_node(node, cutoff=cutoff)
            if branch is not None:
                branches.add(branch)

        page_info = refs.get("pageInfo")
        if not isinstance(page_info, Mapping) or page_info.get("hasNextPage") is not True:
            break
        after = page_info.get("endCursor")
        if not isinstance(after, str) or not after:
            break

    return sorted(branches)


def run(
    client: GitHubClient,
    *,
    issue_number: int,
    branch: str | None = None,
) -> int:
    """Check one moved branch immediately, or perform the periodic fallback sweep."""
    branches = [branch] if branch is not None else discover_recent_return_branches(client)
    certified_or_known = 0
    for candidate in branches:
        if not isinstance(candidate, str) or not candidate.startswith("agent/"):
            continue
        try:
            if notify_if_certified(
                client,
                branch=candidate,
                issue_number=issue_number,
                allow_legacy=True,
            ):
                certified_or_known += 1
        except Exception as exc:
            print(f"warning: {candidate}: {exc}", file=sys.stderr)
    mode = "direct" if branch is not None else "fallback-sweep"
    print(
        f"return-beacon {mode} complete; "
        f"candidates={len(branches)} certified/known={certified_or_known}"
    )
    return 0


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--issue", type=int, default=DEFAULT_INBOX_ISSUE)
    parser.add_argument("--branch", help="exact moved agent branch for immediate checking")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if not args.repo:
        raise SystemExit("--repo or GITHUB_REPOSITORY is required")
    if not args.token:
        raise SystemExit("--token or GITHUB_TOKEN is required")
    if args.branch is not None and not args.branch.startswith("agent/"):
        raise SystemExit("--branch must be an agent/* branch")
    client = GitHubClient(args.repo, args.token)
    return run(client, issue_number=args.issue, branch=args.branch)


if __name__ == "__main__":
    raise SystemExit(main())
