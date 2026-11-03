#!/usr/bin/env python3
"""Read-only structural gate for the cross-HQ branch-custody derived queue.

NOT a scientific/original source, real consumer, review, or live-process validator.
By default this script has no network access and makes no repository mutations.
Use --live with an existing qualified GH CLI login only for passive tip drift.
"""
import argparse
import collections
import datetime
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

HEX40 = re.compile(r"^[0-9a-f]{40}$")
ALLOWED_REPOS = {"maidiu/rawlsing", "maidiu/rawlsing-controller"}
ALLOWED_STATES = {
    "DISCOVERED", "TRIAGED", "RETURNED", "EVIDENCE_ASSESSED",
    "REVIEW_PENDING", "REVIEWED_SCOPED", "DISPOSITIONED",
    "CONSUMER_PROVED", "CLOSED",
}
FINAL = {
    "ADOPTED_WITH_CONSUMER", "REUSED_EQUIVALENT",
    "REJECTED_WITH_FINDING", "SUPERSEDED_WITH_PROOF",
    "ARCHIVED_NONMATERIAL",
}
ALL_DISPOSITIONS = FINAL | {"PENDING", "HELD_WITH_OWNER"}
OPEN_STATES = ALLOWED_STATES - {"CLOSED"}


def valid_sha(value):
    return isinstance(value, str) and HEX40.fullmatch(value) is not None


def audit(data):
    problems = []
    if data.get("schema") != "RAWLSING_CROSS_HQ_BRANCH_CUSTODY@1.0.0":
        problems.append("INVALID_SCHEMA")
    entries = data.get("entries")
    if not isinstance(entries, list):
        return ["ENTRIES_MUST_BE_LIST"]
    seen = set()
    for idx, e in enumerate(entries):
        pre = f"entries[{idx}]"
        if not isinstance(e, dict):
            problems.append(f"{pre}: NOT_AN_OBJECT")
            continue
        cid = e.get("custody_id")
        if not isinstance(cid, str) or not cid:
            problems.append(f"{pre}: MISSING_CUSTODY_ID")
        elif cid in seen:
            problems.append(f"{pre}: DUPLICATE_CUSTODY_ID:{cid}")
        seen.add(cid)
        if e.get("repository") not in ALLOWED_REPOS:
            problems.append(f"{pre}: UNKNOWN_REPOSITORY")
        if not isinstance(e.get("branch"), str) or not e["branch"].strip():
            problems.append(f"{pre}: MISSING_BRANCH")
        if not valid_sha(e.get("observed_head_sha")):
            problems.append(f"{pre}: INVALID_HEAD_SHA")
        state = e.get("state")
        disposition = e.get("disposition")
        if state not in ALLOWED_STATES:
            problems.append(f"{pre}: INVALID_STATE")
        if disposition not in ALL_DISPOSITIONS:
            problems.append(f"{pre}: INVALID_DISPOSITION")
        if not e.get("function_or_claim") or not e.get("next_qualified_action"):
            problems.append(f"{pre}: MISSING_CLAIM_OR_NEXT_ACTION")
        if not e.get("negative_falsifier") or not e.get("unproved"):
            problems.append(f"{pre}: MISSING_FALSIFIER_OR_UNPROVED_SCOPE")
        art = e.get("artifact") or {}
        if not isinstance(art, dict):
            problems.append(f"{pre}: INVALID_ARTIFACT")
            art = {}
        if art.get("blob_sha") is not None and not valid_sha(art["blob_sha"]):
            problems.append(f"{pre}: INVALID_BLOB_SHA")
        rev = e.get("review") or {}
        if not isinstance(rev, dict):
            problems.append(f"{pre}: INVALID_REVIEW")
            rev = {}
        if rev.get("commit_sha") is not None and not valid_sha(rev["commit_sha"]):
            problems.append(f"{pre}: INVALID_REVIEW_SHA")
        if state == "REVIEWED_SCOPED" and not rev.get("commit_sha"):
            problems.append(f"{pre}: REVIEWED_WITHOUT_REVIEW_SHA")
        consumer = e.get("first_consumer") or {}
        if not isinstance(consumer, dict):
            problems.append(f"{pre}: INVALID_CONSUMER")
            consumer = {}
        if not consumer.get("required"):
            problems.append(f"{pre}: FIRST_CONSUMER_UNSPECIFIED")
        if disposition == "HELD_WITH_OWNER":
            if not e.get("owner_intake_receipt") or not e.get("next_qualified_action"):
                problems.append(f"{pre}: HELD_BUT_NO_RESPONSIBLE_INTAKE")
        if state == "CLOSED":
            if disposition not in FINAL:
                problems.append(f"{pre}: CLOSED_WITHOUT_DISPOSITION")
            if not e.get("owner_intake_receipt"):
                problems.append(f"{pre}: CLOSED_WITHOUT_OWNER_DECISION")
            if disposition in ("ADOPTED_WITH_CONSUMER", "REUSED_EQUIVALENT"):
                if not consumer.get("qualified_execution_receipt") or not valid_sha(consumer.get("accepted_target_sha")):
                    problems.append(f"{pre}: ADOPTED_WITHOUT_REAL_CONSUMER_AND_EXACT_TARGET")
                if not art.get("path") or not valid_sha(art.get("blob_sha")) or not art.get("symbol"):
                    problems.append(f"{pre}: ADOPTED_WITHOUT_FUNCTION_BLOB")
                if not rev.get("commit_sha") or not rev.get("independently_accepted_for_requested_consumer"):
                    problems.append(f"{pre}: ADOPTED_WITHOUT_INDEPENDENT_SCOPE_ACCEPTANCE")
                if e.get("source_and_science_authority") in ("UNVERIFIED_OR_RETAIN_EXACT_HOLDS", None):
                    problems.append(f"{pre}: ADOPTED_WITH_UNKNOWN_AUTHORITY")
            if disposition in ("REJECTED_WITH_FINDING", "SUPERSEDED_WITH_PROOF", "ARCHIVED_NONMATERIAL"):
                if not e.get("disposition_evidence"):
                    problems.append(f"{pre}: CLOSED_WITHOUT_DISPOSITION_EVIDENCE")
        elif disposition in FINAL:
            problems.append(f"{pre}: FINAL_DISPOSITION_BUT_STATE_NOT_CLOSED")
    return problems


def gh_branches(repo):
    """Passive list only; a page-stream is not an atomic remote snapshot."""
    if not shutil.which("gh"):
        raise RuntimeError("gh CLI absent; no live branch claim possible")
    rows = {}
    for page in range(1, 60):
        cmd = ["gh", "api", "-H", "Accept: application/vnd.github+json",
               f"repos/{repo}/branches?per_page=100&page={page}"]
        raw = subprocess.check_output(cmd, text=True)
        payload = json.loads(raw)
        if not isinstance(payload, list):
            raise ValueError("GH API branches response not list")
        if not payload:
            return rows
        for v in payload:
            rows[v["name"]] = v["commit"]["sha"]
    raise RuntimeError("Pagination guard exceeded, no complete live census")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("queue", type=Path)
    p.add_argument("--live", action="store_true",
                   help="Passive GH remote name/SHA drift only; requires qualified gh login")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    try:
        data = json.loads(args.queue.read_text(encoding="utf-8"))
        errors = audit(data)
        counts = dict(collections.Counter(e.get("state") for e in data.get("entries", []) if isinstance(e, dict)))
        result = {
            "schema": "RAWLSING_CUSTODY_STRUCTURAL_GATE_RESULT@1.0.0",
            "structural_pass": not errors,
            "entries": len(data.get("entries", [])),
            "states": counts, "errors": errors,
            "scientific_validation": "NOT_RUN",
            "actual_consumer_execution": "NOT_RUN",
            "original_source_validation": "NOT_RUN",
            "independent_review": "NOT_PERFORMED_BY_THIS_SCRIPT",
        }
        if args.live:
            drift = []
            live_census = {}
            for repo in sorted({e.get("repository") for e in data.get("entries", []) if e.get("repository") in ALLOWED_REPOS}):
                live_census[repo] = gh_branches(repo)
            for e in data.get("entries", []):
                repo = e.get("repository")
                if repo in live_census:
                    current = live_census[repo].get(e.get("branch"))
                    if current is None or current != e.get("observed_head_sha"):
                        drift.append({
                            "custody_id": e.get("custody_id"),
                            "old": e.get("observed_head_sha"),
                            "now": current, "kind": "MISSING_REF" if current is None else "MOVED_HEAD",
                        })
            result["live_observed_utc"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
            result["live_branch_counts"] = {k: len(v) for k, v in live_census.items()}
            result["observed_head_drift"] = drift
            result["live_caveat"] = "PAGINATED_NONATOMIC_NAME_AND_SHA_ONLY_NOT_A_PROCESS_OR_CODE_AUDIT"
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as e:
        print(json.dumps({"structural_pass": False, "errors": [str(e)]}, indent=2))
        return 2
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print(f"CUSTODY_STRUCTURAL_GATE={'PASS' if result['structural_pass'] else 'FAIL'}; entries={result['entries']}; states={result['states']}")
        for err in errors:
            print("ERROR:", err)
        if args.live:
            print(f"LIVE_REMOTE_NAME_SHA_DRIFT={len(result['observed_head_drift'])}")
    return 0 if result["structural_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
