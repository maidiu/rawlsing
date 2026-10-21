#!/usr/bin/env python3
"""Write a deterministic-ish environment receipt (includes wall-clock time)."""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus_common as C


def run(args):
    return subprocess.run(args, cwd=str(C.ROOT), capture_output=True, text=True)


def main():
    payload = {
        "schema": "R53_P53E_ENVIRONMENT@1",
        "collected_at_utc": datetime.now(timezone.utc).isoformat(),
        "os": platform.platform(),
        "machine": platform.machine(),
        "python": sys.version,
        "git": run(["git", "--version"]).stdout.strip(),
        "repo_root": str(C.ROOT),
        "worktree_head": run(["git", "rev-parse", "HEAD"]).stdout.strip(),
        "branch": run(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip(),
        "status_porcelain": run(["git", "status", "--porcelain"]).stdout.splitlines(),
        "worktrees": run(["git", "worktree", "list", "--porcelain"]).stdout.splitlines(),
        "remotes": run(["git", "remote", "-v"]).stdout.splitlines(),
        "partial_clone_filter": run(["git", "config", "--get", "remote.origin.partialclonefilter"]).stdout.strip(),
        "source_ref": C.SOURCE_REF,
        "source_head_readable": run(["git", "cat-file", "-t", C.SOURCE_REF]).stdout.strip(),
        "sealed_startup": "f6fd6cdfebe8f0d76a3aa0e2de150065f261709d",
    }
    C.write_json(C.RECEIPTS / "environment.json", payload)
    lines = [
        "PYAT R53 P53E environment receipt",
        f"collected_at_utc={payload['collected_at_utc']}",
        f"os={payload['os']}",
        f"machine={payload['machine']}",
        f"python={payload['python'].splitlines()[0]}",
        f"git={payload['git']}",
        f"repo_root={payload['repo_root']}",
        f"worktree_head={payload['worktree_head']}",
        f"branch={payload['branch']}",
        f"source_ref={payload['source_ref']} ({payload['source_head_readable']})",
        f"partial_clone_filter={payload['partial_clone_filter']}",
        "status_porcelain:",
        *["  " + line for line in payload["status_porcelain"]],
        "remotes:",
        *["  " + line for line in payload["remotes"]],
    ]
    (C.RECEIPTS / "environment.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"head": payload["worktree_head"], "branch": payload["branch"], "status_count": len(payload["status_porcelain"])}, indent=1))


if __name__ == "__main__":
    main()
