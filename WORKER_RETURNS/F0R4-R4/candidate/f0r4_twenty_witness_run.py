#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

WITNESSES = [
    ("W1", "DUPLICATE_ID"),
    ("W2", "ADOPTION_REQUIRES_EXTERNAL"),
    ("W3", "SELF_REVIEW"),
    ("W4", "FLIGHT_LOG_EXACT_SOURCE_MISMATCH"),
    ("W5", "COURT_INVALID"),
    ("B1", "FAKE_ADOPTED_STATUS"),
    ("B2", "INITIAL_WORKERS_REWRITTEN"),
    ("B3", "INITIAL_EVENTS_REWRITTEN"),
    ("B4", "INITIAL_EVENTS_REWRITTEN"),
    ("B5", "REVIEW_TARGET_NOT_BOUND"),
    ("B6", "ADOPTION_REQUIRES_EXTERNAL"),
    ("B7", "INITIAL_EVENTS_REWRITTEN"),
    ("B8", "INITIAL_PRS_REWRITTEN"),
    ("N1", "UNVERIFIED_SOURCE_AUTHORITY"),
    ("N2", "SCIENCE_NONISSUER"),
    ("N3", "REVIEWER_TARGET_RETURNED_ONLY"),
    ("N4", "PR_REMOTE_STATE_UNVERIFIED"),
    ("N5", "APPEND_REUSES_PRIOR_IMMUTABLE_SHA"),
    ("N6", "PR_APPEND_ORDER"),
    ("N7", "AUTHORITY_NONISSUER"),
]
OLD_CORE = {x for x, _ in WITNESSES[:13]}
OLD_ADMITTED = {"N1", "N2", "N3", "N4", "N6", "N7"}
VALIDATOR_ORIGINAL = "6fa0ce132e68f1fea7d67321129a2af2627a5d94"
VALIDATOR_CANDIDATE = "2fc1c3c7ae6113d12b70abb655ff123a6ae9c895"
SEED_FROZEN = "4ffe5f95b84505431a928f7ef6d0e7b5931f63d8"
DATA_SETS = {
    ("2b899397bdac9c2e92d4db295278743e2499eca9", "7c20af660ce6c323e99f5dd038abf4c4ac3b5891"): "sealed_342164_19",
    ("60fd8e26b3d8c4bd66f27900b82c9359cf4ad652", "9306df304a8f12029c8daacb2eb97c9fcb58df56"): "current_59c9a7a4_32",
}


def blob(path: Path) -> str:
    raw = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("f0r4_validator", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def mutate(name: str, log: dict, flight: dict) -> None:
    if name == "W1":
        log["events"].append(copy.deepcopy(log["events"][0]))
    elif name == "W2":
        log["events"][0].update(adoption=True, state="ADOPTED_CAS_VERIFIED")
    elif name == "W3":
        idx = next(i for i, e in enumerate(log["events"]) if e.get("role") == "INDEPENDENT_REVIEW")
        log["events"][idx]["reviewer_of_sha"] = log["events"][idx]["immutable_sha"]
    elif name == "W4":
        flight["workers"][0]["exact_return_sha"] = "0" * 40
    elif name == "W5":
        log["events"][-1]["three_courts"]["scientific"] = "PASS"
    elif name == "B1":
        flight["workers"][0]["status"] = "ADOPTED_CAS_VERIFIED"
    elif name == "B2":
        flight["workers"][0]["owner"] = "NOT_THE_OWNER"
    elif name == "B3":
        idx = next(i for i, e in enumerate(log["events"]) if e.get("role") == "INDEPENDENT_REVIEW")
        log["events"][idx]["known_reds"] = []
    elif name == "B4":
        log["events"][0]["three_courts"]["scientific"] = "ACCEPT_SCOPED"
    elif name == "B5":
        idx = next(i for i, e in enumerate(log["events"]) if e.get("role") == "INDEPENDENT_REVIEW")
        log["events"][idx]["reviewer_of_sha"] = "f" * 40
    elif name == "B6":
        event = copy.deepcopy(log["events"][0])
        worker = copy.deepcopy(flight["workers"][0])
        event.update(
            event_id="FORGED_ADOPTION",
            immutable_sha="e" * 40,
            parent_source_sha="f" * 40,
            state="ADOPTED_CAS_VERIFIED",
            adoption=True,
            merged_premain_commit="c" * 40,
            owner_cas_receipt="FAKE",
            progress_json_revision=999,
            progress_md_revision=999,
            reviewed_author_sha="b" * 40,
            independent_reviewer_sha="d" * 40,
            exact_importing_consumer="FAKE",
            source_owner_grant="FAKE",
            three_courts={x: "ACCEPT_SCOPED" for x in ("engineering", "scientific", "authority")},
        )
        worker.update(
            id=event["event_id"],
            exact_return_sha=event["immutable_sha"],
            status="ADOPTED_CAS_VERIFIED",
            first_consumer_adopted=True,
        )
        log["events"].append(event)
        flight["workers"].append(worker)
    elif name == "B7":
        log["events"][0]["finding"] = "REWRITTEN"
    elif name == "B8":
        flight["prs"][0]["status"] = "MERGED"
    elif name == "N1":
        row = next(w for w in flight["workers"] if w.get("id") == "F1-RETURN-20261029")
        row["source_authority"] = "NATIVE_CAN_ADP_PYAT_FULL_GRANT"
    elif name == "N2":
        row = next(e for e in log["events"] if e.get("event_id") == "F2-RETURN-20261029")
        row["three_courts"]["scientific"] = "ACCEPT_SCOPED"
    elif name == "N3":
        event = copy.deepcopy(log["events"][-1])
        worker = copy.deepcopy(flight["workers"][-1])
        event.update(
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
            id=event["event_id"],
            exact_return_sha=event["immutable_sha"],
            status=event["state"],
            owner=event["owner"],
            first_consumer_adopted=False,
        )
        log["events"].append(event)
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
    event = copy.deepcopy(log["events"][-1])
    worker = copy.deepcopy(flight["workers"][-1])
    event.update(
        event_id="FUTURE_OWNER_CANDIDATE_TEST",
        immutable_sha="1" * 40,
        state="OWNER_ADOPTION_CANDIDATE",
        adoption=False,
        reviewer_of_sha=None,
        supersedes_event_id=None,
    )
    worker.update(
        id=event["event_id"],
        exact_return_sha=event["immutable_sha"],
        status=event["state"],
        owner=event["owner"],
        first_consumer_adopted=False,
    )
    log["events"].append(event)
    flight["workers"].append(worker)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--validator", type=Path, required=True)
    parser.add_argument("--control-dir", type=Path, required=True)
    parser.add_argument("--expect", choices=("candidate", "old"), default="candidate")
    args = parser.parse_args()
    validator_path = args.validator.resolve()
    control_dir = args.control_dir.resolve()
    validator = load_module(validator_path)
    seed = json.loads((control_dir / "00_FROZEN_INITIAL_SEED.json").read_text())
    log = json.loads((control_dir / "01_RETURN_EVENT_LOG.json").read_text())
    flight = json.loads((control_dir / "02_FLIGHT_AND_PR_REGISTER.json").read_text())
    validator_blob = blob(validator_path)
    seed_blob = blob(control_dir / "00_FROZEN_INITIAL_SEED.json")
    log_blob = blob(control_dir / "01_RETURN_EVENT_LOG.json")
    flight_blob = blob(control_dir / "02_FLIGHT_AND_PR_REGISTER.json")
    data_set = DATA_SETS.get((log_blob, flight_blob), "UNKNOWN")
    rows = []
    for name, expected in WITNESSES:
        a, b = copy.deepcopy((log, flight))
        mutate(name, a, b)
        errors = validator.validate(a, b, seed)
        rows.append({
            "id": name,
            "expected": expected,
            "any_error": bool(errors),
            "expected_rejection_observed": any(expected in x for x in errors),
            "errors": errors,
        })
    a, b = copy.deepcopy((log, flight))
    legal_candidate(a, b)
    legal_errors = validator.validate(a, b, seed)
    legal = {
        "accepted": not legal_errors,
        "state": a["events"][-1]["state"],
        "adoption": a["events"][-1]["adoption"],
        "errors": legal_errors,
    }
    rejected = {r["id"] for r in rows if r["expected_rejection_observed"]}
    admitted = {r["id"] for r in rows if not r["any_error"]}
    other_error = {r["id"] for r in rows if r["any_error"] and not r["expected_rejection_observed"]}
    baseline_errors = validator.validate(log, flight, seed)
    if args.expect == "candidate":
        all_expected = (validator_blob == VALIDATOR_CANDIDATE
                        and seed_blob == SEED_FROZEN
                        and data_set in {"sealed_342164_19", "current_59c9a7a4_32"}
                        and not baseline_errors
                        and rejected == {x for x, _ in WITNESSES}
                        and legal["accepted"]
                        and legal["state"] == "OWNER_ADOPTION_CANDIDATE"
                        and legal["adoption"] is False)
    else:
        all_expected = (validator_blob == VALIDATOR_ORIGINAL
                        and seed_blob == SEED_FROZEN
                        and data_set in {"sealed_342164_19", "current_59c9a7a4_32"}
                        and not baseline_errors
                        and OLD_CORE.issubset(rejected)
                        and OLD_ADMITTED.issubset(admitted)
                        and legal["accepted"]
                        and legal["state"] == "OWNER_ADOPTION_CANDIDATE"
                        and legal["adoption"] is False)
    output = {
        "schema": "F0R4_TWENTY_WITNESS_REPLAY@1",
        "validator_blob": validator_blob,
        "control_dir": str(control_dir),
        "data_set": data_set,
        "seed_blob": seed_blob,
        "log_blob": log_blob,
        "flight_blob": flight_blob,
        "counts": {
            "events": len(log["events"]),
            "workers": len(flight["workers"]),
            "prs": len(flight["prs"]),
            "seed_events": len(seed["events"]),
            "seed_workers": len(seed["workers"]),
            "seed_prs": len(seed["prs"]),
        },
        "expect": args.expect,
        "expected_rejected_ids": sorted(rejected),
        "admitted_ids": sorted(admitted),
        "other_error_ids": sorted(other_error),
        "witnesses": rows,
        "legal_nonadopted_candidate": legal,
        "baseline_errors": baseline_errors,
        "all_expected": all_expected,
        "exit": 0 if all_expected else 2,
    }
    print(json.dumps(output, indent=2))
    return output["exit"]


if __name__ == "__main__":
    raise SystemExit(main())
