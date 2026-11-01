#!/usr/bin/env python3
"""Build the 845-name branch location summary from the frozen PR #515 roster."""
from __future__ import annotations
import json, subprocess, sys
from collections import Counter
from pathlib import Path

PREMAIN = "8e44ca9c751049d65e6def47600b5c073ee04b29"
DATA = Path("/tmp/rrif_custody")
CODE_ROOTS = ("rawlsing_next/", "candidate/", "v3/", "server/", "phase_d/", "apps/", "python/")
EVIDENCE_ROOTS = ("WORKER_RETURNS/", "WORKER_COMMISSIONS/", "PYAT_CONTROL_ROOM/", "SOROK_PRODUCT_CONTROL_ROOM/", "CROSS_HQ_CONTROL_ROOM/", "HQ_HANDOFF/", "docs/", "docs/AGENTS.md")


def git(*args: str, check: bool = True) -> str:
    p = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and p.returncode:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.strip()}")
    return p.stdout.strip()


def current_tree() -> dict[str, str]:
    out = git("ls-tree", "-r", "--full-tree", PREMAIN)
    d = {}
    for line in out.splitlines():
        meta, path = line.split("\t", 1)
        d[path] = meta.split()[2]
    return d


def classify(path: str) -> str:
    if path.startswith(("rawlsing_next/tests/", "tests/")) or "/tests/" in path or Path(path).name.startswith("test_"):
        return "test"
    if path.endswith(".py") and (path.startswith(CODE_ROOTS) or path.startswith("scripts/")):
        return "code"
    if path.endswith((".yml", ".yaml", ".toml")):
        return "config"
    if path.startswith(EVIDENCE_ROOTS) or path.endswith(".md"):
        return "evidence_or_docs"
    return "other"


def main() -> int:
    roster = []
    for i in range(1, 6):
        roster += json.loads((DATA / f"pr515_s{i}.json").read_text())["branch_heads"]
    heads = {}
    for line in (DATA / "remote_heads.txt").read_text().splitlines():
        sha, ref = line.split("\t")
        heads[ref.removeprefix("refs/heads/")] = sha
    tree = current_tree()
    by_tip = {}
    for row in roster:
        by_tip.setdefault(row["tip_sha"], []).append(row)
    base_info = {}
    for n, (tip, names) in enumerate(sorted(by_tip.items()), 1):
        print(f"[{n}/{len(by_tip)}] {tip[:12]}", file=sys.stderr)
        ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", tip, PREMAIN]).returncode == 0
        mb = git("merge-base", PREMAIN, tip, check=False)
        ahead, behind = 0, 0
        if mb:
            counts = git("rev-list", "--left-right", "--count", f"{PREMAIN}...{tip}", check=False)
            if counts:
                behind, ahead = (int(x) for x in counts.split())
        changed = []
        if mb:
            out = git("diff", "--name-status", mb, tip, check=False)
            for line in out.splitlines():
                fields = line.split("\t")
                if len(fields) >= 2:
                    changed.append((fields[0][0], fields[-1]))
        counts = Counter(classify(p) for _, p in changed)
        code = [(status, p) for status, p in changed if classify(p) == "code"]
        exact = modified = absent = 0
        exact_paths, modified_paths, absent_paths = [], [], []
        for status, p in code:
            if status == "D":
                absent += 1; absent_paths.append(p); continue
            tip_blob = git("rev-parse", f"{tip}:{p}", check=False)
            cur = tree.get(p)
            if cur and cur == tip_blob:
                exact += 1; exact_paths.append(p)
            elif cur:
                modified += 1; modified_paths.append(p)
            else:
                absent += 1; absent_paths.append(p)
        if not changed:
            disposition = "NO_DELTA_VS_MERGE_BASE"
        elif code and absent == 0 and modified == 0:
            disposition = "CODE_EXACT_PRESENT_IN_PREMAIN__TRANSFER_METHOD_UNVERIFIED"
        elif code:
            disposition = "CODE_STRANDED_OR_DIVERGED"
        else:
            disposition = "EVIDENCE_OR_ADMIN_ONLY_DELTA"
        base_info[tip] = {
            "merge_base": mb or None,
            "premain_ancestor": ancestor,
            "premain_ahead": ahead,
            "premain_behind": behind,
            "changed_files": len(changed),
            "code_delta_count": counts["code"],
            "test_delta_count": counts["test"],
            "config_delta_count": counts["config"],
            "evidence_or_doc_delta_count": counts["evidence_or_docs"],
            "other_delta_count": counts["other"],
            "code_exact_in_premain": exact,
            "code_modified_in_premain": modified,
            "code_absent_from_premain": absent,
            "code_exact_paths_sample": sorted(exact_paths)[:8],
            "code_modified_paths_sample": sorted(modified_paths)[:8],
            "code_absent_paths_sample": sorted(absent_paths)[:8],
            "disposition": disposition,
        }
    rows = []
    for row in roster:
        info = base_info[row["tip_sha"]]
        current = heads.get(row["branch"])
        ref_status = "MISSING_CURRENT_REF" if current is None else ("SAME_AS_FROZEN_TIP" if current == row["tip_sha"] else "MOVED_AFTER_FROZEN_ROSTER")
        rows.append({
            "schema": "RRIF_CUSTODY_BRANCH_LOCATION@1",
            "branch": row["branch"],
            "frozen_tip": row["tip_sha"],
            "frozen_tree": row["tree_sha"],
            "frozen_parent_shas": row.get("parent_shas", []),
            "frozen_tip_author_time": row.get("author_time_utc"),
            "frozen_tip_committer_time": row.get("committer_time_utc"),
            "cohort": row.get("cohort_date_status"),
            "kind": row.get("kind"),
            "current_remote_tip": current,
            "current_ref_status": ref_status,
            **info,
            "location_status": (
                "PREMAIN_ANCESTOR" if info["premain_ancestor"] else
                "EXACT_CODE_PRESENT_IN_PREMAIN" if info["disposition"] == "CODE_EXACT_PRESENT_IN_PREMAIN__TRANSFER_METHOD_UNVERIFIED" else
                "CODE_STRANDED_OR_DIVERGED" if info["disposition"] == "CODE_STRANDED_OR_DIVERGED" else
                "EVIDENCE_ONLY" if info["disposition"] == "EVIDENCE_OR_ADMIN_ONLY_DELTA" else
                "NO_DELTA"
            ),
        })
    out = Path("WORKER_RETURNS/PYAT_RRIF_CUSTODY_A_SOURCE_LOCATION_R1")
    (out / "BRANCH_LOCATION_SUMMARY.jsonl").write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in rows))
    summary = {
        "schema": "RRIF_CUSTODY_BRANCH_SUMMARY_COUNTS@1",
        "frozen_names": len(rows), "distinct_tips": len(by_tip),
        "current_refs_present": sum(r["current_remote_tip"] is not None for r in rows),
        "current_refs_moved": sum(r["current_ref_status"] == "MOVED_AFTER_FROZEN_ROSTER" for r in rows),
        "disposition_counts": dict(Counter(r["disposition"] for r in rows)),
        "location_status_counts": dict(Counter(r["location_status"] for r in rows)),
        "code_delta_branches": sum(r["code_delta_count"] > 0 for r in rows),
        "stranded_code_branches": sum(r["disposition"] == "CODE_STRANDED_OR_DIVERGED" for r in rows),
        "evidence_only_branches": sum(r["disposition"] == "EVIDENCE_OR_ADMIN_ONLY_DELTA" for r in rows),
        "no_delta_branches": sum(r["disposition"] == "NO_DELTA_VS_MERGE_BASE" for r in rows),
    }
    (out / "BRANCH_LOCATION_COUNTS.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
