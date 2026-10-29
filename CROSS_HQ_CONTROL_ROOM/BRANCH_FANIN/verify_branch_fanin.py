#!/usr/bin/env python3
"""Offline intake-contract gate. Data integrity only; NEVER science or remote lease authority."""
from __future__ import annotations
import argparse
import copy
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHA = re.compile(r"^[a-f0-9]{40}$")
EVENT_STATES = {
    "DISCOVERED", "COMMISSIONED_NOT_LAUNCHED", "ACTIVITY_UNKNOWN",
    "ACTIVE_VERIFIED", "RETURNED_PARTIAL_HOLD", "RETURNED_UNADOPTED",
    "UNDER_INDEPENDENT_REVIEW", "REVISE", "ACCEPT_SCOPED", "REJECT",
    "HOLD", "PREMAIN_FANIN_STAGED", "ADOPTED_CAS_VERIFIED",
}
COURT_GRADES = {"ACCEPT_SCOPED", "RED", "HOLD", "NOT_RUN"}
REQ_EVENT = ("event_id", "role", "subject_ref", "immutable_sha",
    "parent_source_sha", "receipt_path", "state", "finding",
    "interpretation", "action", "owner", "three_courts",
    "first_consumer", "known_reds", "adoption", "reviewer_of_sha",
    "verified_date", "intake_grade")
REQ_ADOPTED = ("merged_premain_commit", "owner_cas_receipt",
    "progress_json_revision", "progress_md_revision",
    "exact_importing_consumer", "reviewed_author_sha",
    "independent_reviewer_sha", "source_owner_grant")

def validate(log: dict, flight: dict) -> list[str]:
    errors: list[str] = []
    def bad(condition: bool, msg: str):
        if condition:
            errors.append(msg)

    bad(log.get("schema") != "PREMAIN_CROSS_HQ_BRANCH_RETURN_EVENT_LOG@1", "LOG_SCHEMA")
    bad(flight.get("schema") != "PREMAIN_CROSS_HQ_BRANCH_FLIGHT_AND_PR_REGISTER@1", "FLIGHT_SCHEMA")
    events = log.get("events")
    workers = flight.get("workers")
    if not isinstance(events, list) or not isinstance(workers, list):
        return errors + ["EVENT_OR_WORKER_LIST_MISSING"]
    known = {}
    for index, e in enumerate(events):
        pre = f"EVENT_{index}_"
        for field in REQ_EVENT:
            bad(field not in e, pre+"MISSING_"+field)
        ident = e.get("event_id")
        bad(not isinstance(ident, str) or not ident.strip(), pre+"INVALID_EVENT_ID")
        bad(ident in known, pre+"DUPLICATE_ID")
        if isinstance(ident, str):
            known[ident] = index
        bad(e.get("state") not in EVENT_STATES, pre+"ILLEGAL_STATUS")
        for f in ("immutable_sha", "parent_source_sha"):
            bad(not isinstance(e.get(f), str) or not SHA.fullmatch(e[f]), pre+"NOT_EXACT_SHA_"+f)
        for f in ("subject_ref", "receipt_path", "finding", "interpretation", "action", "owner", "first_consumer"):
            bad(not isinstance(e.get(f), str) or not e[f].strip(), pre+"MISSING_DETAIL_"+f)
        bad(not isinstance(e.get("known_reds"), list), pre+"NO_NEGATIVE_LIST")
        courts = e.get("three_courts")
        if not isinstance(courts, dict):
            errors.append(pre+"COURTS_MISSING")
        else:
            for name in ("engineering", "scientific", "authority"):
                bad(courts.get(name) not in COURT_GRADES, pre+"INVALID_COURT_"+name)
        if e.get("role") == "INDEPENDENT_REVIEW":
            tested = e.get("reviewer_of_sha")
            bad(not isinstance(tested, str) or not SHA.fullmatch(tested), pre+"REVIEWED_SHA_MISSING")
            bad(tested == e.get("immutable_sha"), pre+"SELF_REVIEW")
        if e.get("adoption") is True or e.get("state") == "ADOPTED_CAS_VERIFIED":
            bad(e.get("adoption") is not True or e.get("state") != "ADOPTED_CAS_VERIFIED", pre+"ADOPTION_STATE_MISMATCH")
            for f in REQ_ADOPTED:
                bad(not e.get(f), pre+"UNPROVED_ADOPTION_"+f)
            if e.get("progress_json_revision") != e.get("progress_md_revision"):
                errors.append(pre+"PROGRESS_REVISION_DIVERGENCE")
            for f in ("merged_premain_commit", "reviewed_author_sha", "independent_reviewer_sha"):
                bad(not isinstance(e.get(f), str) or not SHA.fullmatch(e[f]), pre+"ADOPTION_SHA_"+f)
            if isinstance(courts, dict):
                bad(any(courts.get(k) != "ACCEPT_SCOPED" for k in ("engineering","scientific","authority")), pre+"UNQUALIFIED_COURT_AS_ADOPTED")
        else:
            bad(e.get("adoption") not in (False, None), pre+"FALSE_ADOPTION_FLAG")
        older = e.get("supersedes_event_id")
        if older is not None:
            bad(older not in known or known.get(older, index)>=index, pre+"BAD_SUPERSESSION")
        # A historical event cannot be changed in-place by this script. Git history must be reviewed by owner.
    registered = {}
    for i, w in enumerate(workers):
        wid = w.get("id")
        bad(not wid or wid in registered, f"FLIGHT_{i}_DUPLICATE_ID")
        if wid:
            registered[wid] = w
        bad(not isinstance(w.get("exact_return_sha"), str) or not SHA.fullmatch(w["exact_return_sha"]), f"FLIGHT_{i}_SHA")
        bad(w.get("first_consumer_adopted") is True and w.get("status") != "ADOPTED_CAS_VERIFIED", f"FLIGHT_{i}_UNAUTHORIZED_ADOPTION")
    bad(set(registered) != {e.get("event_id") for e in events}, "FLIGHTS_AND_LOG_EVENTS_DO_NOT_MATCH")
    for e in events:
        key = e.get("event_id")
        if key in registered:
            bad(registered[key].get("exact_return_sha") != e.get("immutable_sha"), "FLIGHT_LOG_REF_MISMATCH_"+str(key))
    for pr in flight.get("prs", []):
        bad(pr.get("adoption") is True and not pr.get("merged_commit"), "PR_FALSE_ADOPTION_"+str(pr.get("number")))
    return errors

def load():
    return (json.loads((ROOT/"01_RETURN_EVENT_LOG.json").read_text()),
        json.loads((ROOT/"02_FLIGHT_AND_PR_REGISTER.json").read_text()))

def selftest(log: dict, flight: dict):
    assert not validate(log, flight), validate(log, flight)
    def must_fail(edit, token):
        a,b=copy.deepcopy((log,flight))
        edit(a,b)
        failures=validate(a,b)
        assert any(token in e for e in failures),(token,failures)
    must_fail(lambda a,b: a["events"].append(copy.deepcopy(a["events"][0])), "DUPLICATE_ID")
    must_fail(lambda a,b: a["events"][0].update(adoption=True,state="ADOPTED_CAS_VERIFIED"), "UNPROVED_ADOPTION")
    review_index = next(i for i, e in enumerate(log["events"]) if e.get("role") == "INDEPENDENT_REVIEW")
    must_fail(lambda a,b: a["events"][review_index].update(reviewer_of_sha=a["events"][review_index]["immutable_sha"]), "SELF_REVIEW")
    must_fail(lambda a,b: b["workers"][0].update(exact_return_sha="0"*40), "FLIGHT_LOG_REF_MISMATCH")
    must_fail(lambda a,b: a["events"][-1]["three_courts"].update(scientific="PASS"), "INVALID_COURT")
    print("PASS: 5 controlled mutation witnesses fail as intended")

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--selftest",action="store_true")
    ap.add_argument("--baseline-ref", default=None, help="Actual immutable PRE-MAIN PR base SHA; verify strict append-only event prefix")
    args=ap.parse_args()
    log,flight=load()
    failures=validate(log,flight)
    if args.baseline_ref:
        if not SHA.fullmatch(args.baseline_ref):
            failures.append("INVALID_BASELINE_SHA")
        else:
            p = subprocess.run(["git", "cat-file", "-e", args.baseline_ref + "^{commit}"], cwd=ROOT, capture_output=True)
            if p.returncode:
                failures.append("BASELINE_COMMIT_UNAVAILABLE__NO_APPEND_ONLY_PROOF")
            else:
                prior = subprocess.run(["git", "show", args.baseline_ref + ":CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/01_RETURN_EVENT_LOG.json"], cwd=ROOT, capture_output=True, text=True)
                if prior.returncode == 0:
                    try:
                        previous = json.loads(prior.stdout)
                        prefix = previous.get("events", [])
                        if log.get("events", [])[:len(prefix)] != prefix:
                            failures.append("HISTORICAL_EVENTS_REWRITTEN_OR_DELETED__APPEND_ONLY_BROKEN")
                        print(f"Append-only baseline checked: {len(prefix)} immutable prior event(s)")
                    except ValueError:
                        failures.append("BASELINE_EVENT_LOG_UNPARSABLE")
                else:
                    print("Baseline does not contain log (first installation); new log seeded as candidate")
    if failures:
        for e in failures:
            print("FAIL:",e)
        return 1
    print(f"PASS: structural event intake {len(log['events'])}, flight workers {len(flight['workers'])}; NOT scientific/authority certification")
    if args.selftest:
        selftest(log,flight)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
