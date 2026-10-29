#!/usr/bin/env python3
"""Passive Pyat/predecessor branch delta intake detector; no code/source grants."""
import argparse
import collections
import datetime
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
P = re.compile(r"pyat|vozhd-pyat|astra-pyat", re.I)
F = re.compile(r"vozhd-dva|vozhd-trii|vozhd-chetiri|vozhd-verkhovod|dva|trii|chetiri|premain|pre-main|prev3|pre553|fiabc|v54[6-9]|v55[0-8]|field[-_]forge|fracture|ddm|sdtf|source[-_]backed|joint[-_]pattern|phase-d", re.I)
S = re.compile(r"sorok", re.I)
SHA = re.compile(r"^[0-9a-f]{40}$")

def cohort(name):
    p, f, s = bool(P.search(name)), bool(F.search(name)), bool(S.search(name))
    if s:
        return "SHARED_BOUNDARY_REFERENCE_ONLY" if p or f else "SOROK_OUTSIDE_MISSION"
    return "PYAT_DIRECT" if p else ("PRE_PYAT_FOUNDATION_OR_SHARED" if f else "UNCLASSIFIED_SCREEN_NOT_CLOSED")

def baseline(directory=None):
    directory = directory or BASE / "DISCOVERY"
    files = sorted(directory.glob("NAME_HEAD_CANDIDATES_*.json")) + sorted(directory.glob("NAME_HEAD_REMAINDER_*.json"))
    if len(files) != 7:
        raise ValueError("BASELINE_SHARD_COUNT_NOT_7")
    heads, totals = {}, collections.Counter()
    for path in files:
        for row in json.loads(path.read_text(encoding="utf-8"))["records"]:
            name, head = row["branch"], row["head"]
            if name in heads or not SHA.fullmatch(head) or row["cohort"] != cohort(name):
                raise ValueError("DUPLICATE_OR_INVALID_BASELINE:" + name)
            heads[name] = head
            totals[row["cohort"]] += 1
    if len(heads) != 2831:
        raise ValueError("BASELINE_COUNT_NOT_2831")
    return heads, dict(totals)

def normalize(data):
    if isinstance(data, dict):
        data = data.get("entries", data.get("branches"))
    if not isinstance(data, list):
        raise ValueError("CENSUS_NOT_LIST")
    heads = {}
    for row in data:
        name = row.get("name", row.get("branch"))
        head = row.get("sha", row.get("head"))
        if not isinstance(name, str) or not SHA.fullmatch(str(head)) or name in heads:
            raise ValueError("DUPLICATE_OR_INVALID_CURRENT:" + str(name))
        heads[name] = head
    return heads

def live():
    if not shutil.which("gh"):
        raise RuntimeError("GH_CLI_UNAVAILABLE; LIVE_NOT_VERIFIED")
    result = []
    for page in range(1, 80):
        raw = subprocess.check_output(["gh", "api", "-H", "Accept: application/vnd.github+json",
            f"repos/maidiu/rawlsing/branches?per_page=100&page={page}"], text=True)
        rows = json.loads(raw)
        if not isinstance(rows, list):
            raise ValueError("GH_API_BAD_RESPONSE")
        if not rows:
            return normalize(result)
        result.extend({"name": e["name"], "sha": e["commit"]["sha"]} for e in rows)
    raise RuntimeError("GH_PAGINATION_LIMIT")

def scan(old, new, queue):
    claims = {e["branch"]: e["observed_head_sha"] for e in queue["entries"]}
    flagged, stats = [], collections.Counter()
    for name, head in sorted(new.items()):
        before = old.get(name)
        if head == before:
            stats["UNCHANGED"] += 1
            continue
        typ = "NEW_REF" if before is None else "MOVED_HEAD"
        stats[typ] += 1
        kind = cohort(name)
        if kind == "SOROK_OUTSIDE_MISSION":
            stats["SOROK_SEPARATE_NO_PYAT_INTAKE"] += 1
            continue
        if claims.get(name) == head:
            stats["REGISTERED_AT_THIS_SHA"] += 1
            continue
        flagged.append({"branch": name, "old_head": before, "current_head": head,
            "cohort": kind, "kind": typ,
            "disposition": "UNINTAKEN_OR_STALE_CUSTODY__HQ_DECISION_REQUIRED",
            "does_not_prove_live_worker": True})
    stats["MISSING_REF_NO_DELETE_INFERENCE"] = len(set(old) - set(new))
    return flagged, dict(stats)

def main():
    ap = argparse.ArgumentParser()
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--current", type=Path)
    group.add_argument("--live", action="store_true")
    ap.add_argument("--queue", type=Path, default=BASE / "01_PYAT_AND_PREDECESSOR_RECOVERY_QUEUE.json")
    ap.add_argument("--strict", action="store_true")
    args = ap.parse_args()
    try:
        old, groups = baseline()
        new = live() if args.live else normalize(json.loads(args.current.read_text(encoding="utf-8")))
        queue = json.loads(args.queue.read_text(encoding="utf-8"))
        findings, stats = scan(old, new, queue)
        result = {"schema": "PYAT_BRANCH_DELTA_INTAKE_AUDIT@1",
            "observed_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "baseline_size": len(old), "current_size": len(new),
            "baseline_cohorts": groups, "status": "INTAKE_REQUIRED" if findings else "NO_UNREGISTERED_DELTA_SEEN",
            "findings": findings, "stats": stats,
            "limitations": "Passive name/head comparison only; no actual process or science/code acceptance"}
        print(json.dumps(result, indent=2, sort_keys=True))
        return 1 if args.strict and findings else 0
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(json.dumps({"status": "AUDIT_ERROR", "error": str(exc)}))
        return 2

if __name__ == "__main__":
    sys.exit(main())
