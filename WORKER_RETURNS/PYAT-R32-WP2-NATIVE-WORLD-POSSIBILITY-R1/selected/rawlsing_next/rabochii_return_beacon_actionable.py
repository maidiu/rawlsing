"""Actionable presentation layer for certified Rawlsing worker returns.

Certification remains owned by ``rabochii_return_beacon.py``. This module only
turns a certified completion into an unmistakable human action: the associated
ChatGPT worker turn is safe to cancel/close, regardless of PASS/FAIL/BLOCKED.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time
from typing import Sequence

try:
    from . import rabochii_return_beacon as rb
    from . import rabochii_return_beacon_sweep as sweep
except ImportError:
    import rabochii_return_beacon as rb
    import rabochii_return_beacon_sweep as sweep


_OBL_RE = re.compile(r"-(OBL\d+)-", re.IGNORECASE)
_REVIEW_RE = re.compile(r"-(R\d+)-INDEPENDENT-REVIEW(?:-R\d+)?$", re.IGNORECASE)
_REPAIR_RE = re.compile(r"-BOUNDED-REPAIR-(R\d+)$", re.IGNORECASE)


def worker_label(cert: rb.Certification) -> str:
    """Return a short human-identifiable label for GitHub/email alerts."""
    branch = cert.branch
    obl = _OBL_RE.search(branch)
    review = _REVIEW_RE.search(branch)
    repair = _REPAIR_RE.search(branch)
    if obl and review:
        return f"{obl.group(1).upper()} {review.group(1).upper()} INDEPENDENT REVIEW"
    if obl and repair:
        return f"{obl.group(1).upper()} {repair.group(1).upper()} BOUNDED REPAIR"
    if cert.task_id and cert.task_id != "LEGACY_RETURN":
        return cert.task_id.replace("_", " ")
    return branch


def actionable_comment_body(cert: rb.Certification) -> str:
    label = worker_label(cert)
    evidence = f"`{cert.evidence_run_id}`" if cert.evidence_run_id else "not required / not declared"
    return (
        f"{rb._marker(cert)}\n"
        f"## 🛑 SAFE TO CANCEL WORKER CHAT — {label} — {cert.result}\n\n"
        "**ACTION: Cancel/close the corresponding ChatGPT worker turn now.**\n\n"
        f"The commissioned repository work is **certifiably complete**. Its semantic disposition is **{cert.result}**. "
        "PASS, FAIL, and BLOCKED are all terminal completed outcomes; the action above is based on completion, not success.\n\n"
        f"- **Worker label:** `{label}`\n"
        f"- **Result:** `{cert.result}`\n"
        f"- **Branch:** `{cert.branch}`\n"
        f"- **Certified branch tip:** `{cert.tip_sha}`\n"
        f"- **Terminal:** `{cert.terminal}`\n"
        f"- **Return packet:** `{cert.return_packet_path}`\n"
        f"- **Evidence run:** {evidence}\n"
        f"- **Certification mode:** `{cert.mode}`\n\n"
        "No required or background work remains for this commissioned turn. The chat UI may still show Thinking; "
        "that UI state is no longer authoritative once this alert exists."
    )


def _install_actionable_format() -> None:
    # rb.notify_if_certified resolves this global at call time, so the existing
    # certification and exact branch-tip deduplication core stays unchanged.
    rb._comment_body = actionable_comment_body


def _timeout_label(branch: str) -> str:
    fake = rb.Certification(
        branch=branch,
        tip_sha="0" * 40,
        task_id="LEGACY_RETURN",
        result="BLOCKED",
        terminal="RABOCHII_TIMEOUT__RETURN_TO_INFRASTRUCTURE",
        return_packet_path="none",
        evidence_run_id=None,
        mode="NONE",
    )
    return worker_label(fake)


def watch_branch(
    client: rb.GitHubClient,
    *,
    branch: str,
    issue_number: int,
    timeout_seconds: int,
    interval_seconds: int,
) -> int:
    deadline = time.monotonic() + timeout_seconds
    while True:
        if rb.notify_if_certified(client, branch=branch, issue_number=issue_number):
            return 0
        if time.monotonic() >= deadline:
            tip = "unknown"
            try:
                tip = client.get_branch_tip(branch)
            except Exception:
                pass
            marker = f"<!-- rawlsing-return-beacon-timeout:{branch}:{tip} -->"
            if not any(marker in str(c.get("body", "")) for c in client.issue_comments(issue_number)):
                client.post_issue_comment(
                    issue_number,
                    (
                        f"{marker}\n"
                        f"## ⏳ NOT CERTIFIED — DO NOT CANCEL YET — {_timeout_label(branch)}\n\n"
                        "**ACTION: Keep the corresponding worker turn available for now.**\n\n"
                        f"- **Branch:** `{branch}`\n"
                        f"- **Observed tip:** `{tip}`\n\n"
                        "No certified durable return appeared before the watcher timeout. This is **not** a completion alert. "
                        "The fallback sweep will keep checking repository state."
                    ),
                )
            return 2
        time.sleep(interval_seconds)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=os.environ.get("GITHUB_REPOSITORY"))
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--issue", type=int, default=rb.DEFAULT_INBOX_ISSUE)
    sub = parser.add_subparsers(dest="command", required=True)

    watch = sub.add_parser("watch")
    watch.add_argument("--branch", required=True)
    watch.add_argument("--timeout-seconds", type=int, default=1500)
    watch.add_argument("--interval-seconds", type=int, default=15)

    check = sub.add_parser("check")
    check.add_argument("--branch", required=True)
    sub.add_parser("sweep")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if not args.repo or not args.token:
        print("GITHUB_REPOSITORY/--repo and GITHUB_TOKEN/--token are required", file=sys.stderr)
        return 2
    if getattr(args, "branch", None) is not None and not args.branch.startswith("agent/"):
        print("--branch must be an agent/* branch", file=sys.stderr)
        return 2

    _install_actionable_format()
    client = rb.GitHubClient(args.repo, args.token)
    if args.command == "watch":
        return watch_branch(
            client,
            branch=args.branch,
            issue_number=args.issue,
            timeout_seconds=args.timeout_seconds,
            interval_seconds=args.interval_seconds,
        )
    if args.command == "check":
        return sweep.run(client, issue_number=args.issue, branch=args.branch)
    if args.command == "sweep":
        return sweep.run(client, issue_number=args.issue)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
