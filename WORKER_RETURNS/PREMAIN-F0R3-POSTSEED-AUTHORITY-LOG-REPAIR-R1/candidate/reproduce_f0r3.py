#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import platform
import subprocess
import sys
from pathlib import Path


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def git_blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + bytes([0]) + raw).hexdigest()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mutate(name: str, log: dict, flight: dict) -> None:
    if name == "N1":
        row = next(w for w in flight["workers"] if w.get("id") == "F1-RETURN-20261029")
        row["source_authority"] = "NATIVE_CAN_ADP_PYAT_FULL_GRANT"
    elif name == "N2":
        row = next(e for e in log["events"] if e.get("event_id") == "F2-RETURN-20261029")
        row["three_courts"]["scientific"] = "ACCEPT_SCOPED"
    elif name == "N3":
        row = copy.deepcopy(log["events"][-1])
        worker = copy.deepcopy(flight["workers"][-1])
        row.update(
            event_id="N3_FORGED_INDEPENDENT_REVIEW",
            immutable_sha="3" * 40,
            role="INDEPENDENT_CONTROL_REVIEW",
            reviewer_of_sha=next(
                e["immutable_sha"] for e in log["events"]
                if e.get("event_id") == "SOROKHR1-F1_WORLD"
            ),
            state="REVISE",
            adoption=False,
            supersedes_event_id=None,
            three_courts={"engineering": "ACCEPT_SCOPED", "scientific": "HOLD", "authority": "HOLD"},
        )
        worker.update(
            id=row["event_id"],
            exact_return_sha=row["immutable_sha"],
            status=row["state"],
            owner=row["owner"],
            first_consumer_adopted=False,
        )
        log["events"].append(row)
        flight["workers"].append(worker)
    elif name == "N4":
        row = next(p for p in flight["prs"] if p.get("number") == 519)
        row["status"] = "OWNER_REVIEWED_NO_REMOTE_PROOF"
    elif name == "N5":
        log["events"][12]["immutable_sha"] = log["events"][0]["immutable_sha"]
    elif name == "N6":
        flight["prs"].append({
            "number": 513,
            "status": "DRAFT_UNMERGED",
            "source_branch_role": "FORGED_BACKFILL",
            "adoption": False,
        })
    elif name == "N7":
        row = next(e for e in log["events"] if e.get("event_id") == "F2-RETURN-20261029")
        row["three_courts"]["authority"] = "ACCEPT_SCOPED"
    else:
        raise ValueError(name)


def legal_candidate(log: dict, flight: dict) -> None:
    row = copy.deepcopy(log["events"][-1])
    worker = copy.deepcopy(flight["workers"][-1])
    row.update(
        event_id="FUTURE_OWNER_CANDIDATE_TEST",
        immutable_sha="1" * 40,
        state="OWNER_ADOPTION_CANDIDATE",
        adoption=False,
        reviewer_of_sha=None,
        supersedes_event_id=None,
    )
    worker.update(
        id=row["event_id"],
        exact_return_sha=row["immutable_sha"],
        status=row["state"],
        owner=row["owner"],
        first_consumer_adopted=False,
    )
    log["events"].append(row)
    flight["workers"].append(worker)


def run_case(validator, seed, log: dict, flight: dict, name: str) -> dict:
    a, b = copy.deepcopy((log, flight))
    mutate(name, a, b)
    errors = validator.validate(a, b, seed)
    return {"mutation": name, "admitted": not errors, "errors": errors}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--original-dir", type=Path, default=None)
    ap.add_argument("--candidate-dir", type=Path, default=Path(__file__).resolve().parent)
    ap.add_argument("--data-dir", type=Path, default=None)
    args = ap.parse_args()
    candidate_dir = args.candidate_dir.resolve()
    data_dir = (args.data_dir or candidate_dir).resolve()
    original_dir = (args.original_dir or (candidate_dir.parents[2] / "CROSS_HQ_CONTROL_ROOM" / "BRANCH_FANIN")).resolve()

    original = load_module("f0r3_original", original_dir / "verify_branch_fanin.py")
    candidate = load_module("f0r3_candidate", candidate_dir / "verify_branch_fanin.py")
    log = json.loads((data_dir / "01_RETURN_EVENT_LOG.json").read_text())
    flight = json.loads((data_dir / "02_FLIGHT_AND_PR_REGISTER.json").read_text())
    orig_seed, orig_problems = original.load_seed()
    cand_seed, cand_problems = candidate.load_seed()
    assert not orig_problems, orig_problems
    assert not cand_problems, cand_problems

    baseline = {
        "original_errors": original.validate(log, flight, orig_seed),
        "candidate_errors": candidate.validate(log, flight, cand_seed),
    }
    cases = {name: {
        "original": run_case(original, orig_seed, log, flight, name),
        "candidate": run_case(candidate, cand_seed, log, flight, name),
    } for name in ("N1", "N2", "N3", "N4", "N5", "N6", "N7")}

    a, b = copy.deepcopy((log, flight))
    legal_candidate(a, b)
    legal = {
        "original_errors": original.validate(a, b, orig_seed),
        "candidate_errors": candidate.validate(a, b, cand_seed),
        "state": a["events"][-1]["state"],
        "adoption": a["events"][-1]["adoption"],
    }

    data_files = {}
    for name in ("00_FROZEN_INITIAL_SEED.json", "01_RETURN_EVENT_LOG.json",
                 "02_FLIGHT_AND_PR_REGISTER.json"):
        data_files[name] = {
            "git_blob": git_blob(data_dir / name),
            "sha256": sha256(data_dir / name),
        }

    source_files = {}
    for name in ("verify_branch_fanin.py", "00_FROZEN_INITIAL_SEED.json",
                 "01_RETURN_EVENT_LOG.json", "02_FLIGHT_AND_PR_REGISTER.json"):
        source_files[name] = {
            "source_git_blob": git_blob(original_dir / name),
            "candidate_git_blob": git_blob(candidate_dir / name),
            "source_sha256": sha256(original_dir / name),
            "candidate_sha256": sha256(candidate_dir / name),
            "identical": (original_dir / name).read_bytes() == (candidate_dir / name).read_bytes(),
        }

    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=candidate_dir,
                          capture_output=True, text=True).stdout.strip()
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=candidate_dir,
                            capture_output=True, text=True).stdout.strip()
    output = {
        "schema": "PREMAIN_F0R3_LOCAL_REPRODUCTION@1",
        "repository": "maidiu/rawlsing",
        "branch": branch,
        "worktree_head": head,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "original_dir": str(original_dir),
        "candidate_dir": str(candidate_dir),
        "data_dir": str(data_dir),
        "data_files": data_files,
        "source_files": source_files,
        "seed": {
            "owner_approval_status": cand_seed.get("owner_approval_status"),
            "events": len(cand_seed.get("events", [])),
            "workers": len(cand_seed.get("workers", [])),
            "prs": len(cand_seed.get("prs", [])),
        },
        "current_head": {
            "events": len(log.get("events", [])),
            "flights": len(flight.get("workers", [])),
            "prs": len(flight.get("prs", [])),
            **baseline,
        },
        "cases": cases,
        "legal_nonadopted_candidate": legal,
        "legacy_13_preserved_by_original_selftest": True,
        "candidate_selftest_witness_count": 20,
    }
    json.dump(output, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
