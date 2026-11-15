#!/usr/bin/env python3
"""PRE-MAIN sourcefree control integrity. Fail closed on adoption. Not an authority issuer."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SHA = re.compile(r"^[a-f0-9]{40}$")
# Pin initial, historically unreviewed candidate seed to a precise Git blob.
# Owner approval is NOT inferred from this constant. A changed seed requires a
# new independent control review and protected owner CAS, not a silent rewrite.
FROZEN_SEED_BLOB = "4ffe5f95b84505431a928f7ef6d0e7b5931f63d8"
SEED_FILE = ROOT / "00_FROZEN_INITIAL_SEED.json"
EVENT_STATES = {
    "DISCOVERED", "COMMISSIONED_NOT_LAUNCHED", "ACTIVITY_UNKNOWN",
    "ACTIVE_VERIFIED", "RETURNED_PARTIAL_HOLD", "RETURNED_UNADOPTED",
    "UNDER_INDEPENDENT_REVIEW", "REVISE", "ACCEPT_SCOPED", "REJECT",
    "HOLD", "OWNER_ADOPTION_CANDIDATE", "PREMAIN_FANIN_STAGED",
    "ADOPTED_CAS_VERIFIED",
}
GRADES = {"ACCEPT_SCOPED", "RED", "HOLD", "NOT_RUN"}
REQ = ("event_id", "role", "subject_ref", "immutable_sha",
       "parent_source_sha", "receipt_path", "state", "finding",
       "interpretation", "action", "owner", "three_courts", "first_consumer",
       "known_reds", "adoption", "reviewer_of_sha", "verified_date",
       "intake_grade")
REVIEW_ROLES = {"INDEPENDENT_REVIEW", "INDEPENDENT_CONTROL_REVIEW"}
UNTRUSTED_MERGE_STATES = {"MERGED", "ADOPTED_CAS_VERIFIED"}

def load_seed() -> tuple[dict, list[str]]:
    failures = []
    try:
        raw = SEED_FILE.read_bytes()
        git_blob = hashlib.sha1(
            b"blob " + str(len(raw)).encode("ascii") + bytes([0]) + raw
        ).hexdigest()
        if git_blob != FROZEN_SEED_BLOB:
            failures.append("INITIAL_SEED_SOURCE_BLOB_CHANGED__NOT_REVIEWED")
        seed = json.loads(raw)
        if seed.get("owner_approval_status") != "PENDING":
            failures.append("INITIAL_SEED_OWNER_APPROVAL_FABRICATED")
        if seed.get("frozen_subject_sha") != "73f0b57da42e264617e51fe9c703c17aba15ff2a":
            failures.append("INITIAL_SEED_SOURCE_CUT_MISMATCH")
        if len(seed.get("events", [])) != 11 or len(seed.get("workers", [])) != 11:
            failures.append("INITIAL_SEED_DENOMINATOR_CHANGED")
        return seed, failures
    except (ValueError, OSError) as exc:
        return {}, ["INITIAL_SEED_UNREADABLE:" + type(exc).__name__]

def validate(log: dict, flight: dict, seed: dict | None = None) -> list[str]:
    if seed is None:
        seed, errs = load_seed()
    else:
        errs = []
    errors = list(errs)
    def bad(test: bool, issue: str) -> None:
        if test:
            errors.append(issue)

    bad(log.get("schema") != "PREMAIN_CROSS_HQ_BRANCH_RETURN_EVENT_LOG@1", "LOG_SCHEMA")
    bad(flight.get("schema") != "PREMAIN_CROSS_HQ_BRANCH_FLIGHT_AND_PR_REGISTER@1", "FLIGHT_SCHEMA")
    events, workers = log.get("events"), flight.get("workers")
    if not isinstance(events, list) or not isinstance(workers, list):
        return errors + ["EVENT_OR_FLIGHT_LIST_MISSING"]
    for key, rows in (("events", events), ("workers", workers), ("prs", flight.get("prs"))):
        fixed = seed.get(key, [])
        bad(not isinstance(rows, list) or rows[:len(fixed)] != fixed,
            "INITIAL_" + key.upper() + "_REWRITTEN_OR_DELETED")
    ids: dict[str, int] = {}
    for n, e in enumerate(events):
        mark = f"EVENT_{n}_"
        if not isinstance(e, dict):
            errors.append(mark + "NOT_OBJECT")
            continue
        for field in REQ:
            bad(field not in e, mark + "MISSING_" + field)
        ident = e.get("event_id")
        bad(not isinstance(ident, str) or not ident.strip(), mark + "INVALID_ID")
        bad(ident in ids, mark + "DUPLICATE_ID")
        if isinstance(ident, str):
            ids[ident] = n
        bad(e.get("state") not in EVENT_STATES, mark + "ILLEGAL_STATUS")
        for k in ("immutable_sha", "parent_source_sha"):
            bad(not isinstance(e.get(k), str) or not SHA.fullmatch(e.get(k, "")), mark + "BAD_SHA_" + k)
        for k in ("subject_ref", "receipt_path", "finding", "interpretation", "action", "owner", "first_consumer"):
            bad(not isinstance(e.get(k), str) or not e.get(k, "").strip(), mark + "MISSING_DETAIL_" + k)
        bad(not isinstance(e.get("known_reds"), list), mark + "NEGATIVES_NOT_LIST")
        courts = e.get("three_courts")
        if not isinstance(courts, dict):
            errors.append(mark + "COURTS_MISSING")
        else:
            for axis in ("engineering", "scientific", "authority"):
                bad(courts.get(axis) not in GRADES, mark + "COURT_INVALID_" + axis)
        # OFFLINE log cannot certify authority/protection/merged target or source grants.
        # Even completely filled made-up CAS fields cannot pass. A later separately
        # adopted owner-attestation verifier is needed to change this rule.
        bad(e.get("adoption") is not False or e.get("state") == "ADOPTED_CAS_VERIFIED",
            mark + "ADOPTION_REQUIRES_EXTERNAL_OWNER_CAS__FAIL_CLOSED")
        if e.get("role") in REVIEW_ROLES:
            tested = e.get("reviewer_of_sha")
            bad(not isinstance(tested, str) or not SHA.fullmatch(tested), mark + "REVIEW_TARGET_SHA_INVALID")
            bad(tested == e.get("immutable_sha"), mark + "SELF_REVIEW")
            prior = events[:n]
            bad(not any(isinstance(p, dict) and p.get("immutable_sha") == tested
                        and p.get("role") not in REVIEW_ROLES for p in prior),
                mark + "REVIEW_TARGET_NOT_BOUND_TO_PRIOR_SOURCE_EVENT")
        older = e.get("supersedes_event_id")
        if older is not None:
            bad(older not in ids or ids.get(older, n) >= n, mark + "INVALID_SUPERSESSION")
    flights: dict[str, dict] = {}
    for n, row in enumerate(workers):
        if not isinstance(row, dict):
            errors.append(f"FLIGHT_{n}_NOT_OBJECT")
            continue
        ident = row.get("id")
        bad(not isinstance(ident, str) or not ident.strip() or ident in flights,
            f"FLIGHT_{n}_DUPLICATE_OR_MISSING_ID")
        if isinstance(ident, str):
            flights[ident] = row
        bad(not isinstance(row.get("exact_return_sha"), str)
            or not SHA.fullmatch(row.get("exact_return_sha", "")), f"FLIGHT_{n}_BAD_SHA")
        bad(row.get("first_consumer_adopted") is not False,
            f"FLIGHT_{n}_ADOPTION_REQUIRES_EXTERNAL_OWNER_CAS")
        bad(row.get("status") in UNTRUSTED_MERGE_STATES,
            f"FLIGHT_{n}_FAKE_ADOPTED_STATUS")
    bad(set(flights) != set(ids), "FLIGHTS_AND_EVENTS_NOT_ONE_TO_ONE")
    for e in events:
        if not isinstance(e, dict):
            continue
        row = flights.get(e.get("event_id"))
        if row:
            bad(row.get("exact_return_sha") != e.get("immutable_sha"),
                "FLIGHT_LOG_EXACT_SOURCE_MISMATCH_" + str(e.get("event_id")))
            # Legacy exact original 11 rows are frozen (some had different owner labels
            # and HR1's known REVISE status); new rows must be in the same lifecycle.
            if ids[e.get("event_id")] >= len(seed.get("events", [])):
                bad(row.get("status") != e.get("state"),
                    "NEW_FLIGHT_LOG_STATUS_DIVERGENCE_" + str(e.get("event_id")))
                bad(row.get("owner") != e.get("owner"),
                    "NEW_FLIGHT_LOG_OWNER_DIVERGENCE_" + str(e.get("event_id")))
    prs = flight.get("prs", [])
    if not isinstance(prs, list):
        errors.append("PRS_NOT_LIST")
    else:
        for pr in prs:
            if not isinstance(pr, dict):
                errors.append("PR_NOT_OBJECT")
            else:
                bad(pr.get("adoption") is not False or pr.get("status") in UNTRUSTED_MERGE_STATES,
                    "PR_MERGE_OR_ADOPTION_REQUIRES_VERIFIED_REMOTE_PROOF_" + str(pr.get("number")))
    return errors

def load() -> tuple[dict, dict]:
    return (json.loads((ROOT/"01_RETURN_EVENT_LOG.json").read_text()),
            json.loads((ROOT/"02_FLIGHT_AND_PR_REGISTER.json").read_text()))

def selftest(log: dict, flight: dict) -> None:
    seed, problems = load_seed()
    assert not problems, problems
    assert not validate(log, flight, seed), validate(log, flight, seed)
    def reject(name, edit, expected):
        a, b = copy.deepcopy((log, flight))
        edit(a, b)
        failures = validate(a, b, seed)
        assert any(expected in x for x in failures), (name, expected, failures)
    reject("W1",lambda a,b: a["events"].append(copy.deepcopy(a["events"][0])), "DUPLICATE_ID")
    reject("W2",lambda a,b: a["events"][0].update(adoption=True,state="ADOPTED_CAS_VERIFIED"), "ADOPTION_REQUIRES_EXTERNAL")
    ridx = next(i for i, e in enumerate(log["events"]) if e.get("role") == "INDEPENDENT_REVIEW")
    reject("W3",lambda a,b: a["events"][ridx].update(reviewer_of_sha=a["events"][ridx]["immutable_sha"]), "SELF_REVIEW")
    reject("W4",lambda a,b: b["workers"][0].update(exact_return_sha="0"*40), "FLIGHT_LOG_EXACT_SOURCE_MISMATCH")
    reject("W5",lambda a,b: a["events"][-1]["three_courts"].update(scientific="PASS"), "COURT_INVALID")
    reject("B1",lambda a,b: b["workers"][0].update(status="ADOPTED_CAS_VERIFIED"), "FAKE_ADOPTED_STATUS")
    reject("B2",lambda a,b: b["workers"][0].update(owner="NOT_THE_OWNER"), "INITIAL_WORKERS_REWRITTEN")
    reject("B3",lambda a,b: a["events"][ridx].update(known_reds=[]), "INITIAL_EVENTS_REWRITTEN")
    reject("B4",lambda a,b: a["events"][0]["three_courts"].update(scientific="ACCEPT_SCOPED"), "INITIAL_EVENTS_REWRITTEN")
    reject("B5",lambda a,b: a["events"][ridx].update(reviewer_of_sha="f"*40), "REVIEW_TARGET_NOT_BOUND")
    def fake_adopt(a,b):
        e=copy.deepcopy(a["events"][0]);w=copy.deepcopy(b["workers"][0])
        e.update(event_id="FORGED_ADOPTION", immutable_sha="e"*40,
                 parent_source_sha="f"*40, state="ADOPTED_CAS_VERIFIED", adoption=True,
                 merged_premain_commit="c"*40,owner_cas_receipt="FAKE",
                 progress_json_revision=999,progress_md_revision=999,
                 reviewed_author_sha="b"*40, independent_reviewer_sha="d"*40,
                 exact_importing_consumer="FAKE",source_owner_grant="FAKE",
                 three_courts={x:"ACCEPT_SCOPED" for x in ("engineering","scientific","authority")})
        w.update(id=e["event_id"],exact_return_sha=e["immutable_sha"],
                 status="ADOPTED_CAS_VERIFIED",first_consumer_adopted=True)
        a["events"].append(e);b["workers"].append(w)
    reject("B6",fake_adopt,"ADOPTION_REQUIRES_EXTERNAL")
    reject("B7",lambda a,b: a["events"][0].update(finding="REWRITTEN"), "INITIAL_EVENTS_REWRITTEN")
    reject("B8",lambda a,b: b["prs"][0].update(status="MERGED"), "INITIAL_PRS_REWRITTEN")
    # Legal owner candidate must NOT be a synonym for adoption.
    a,b=copy.deepcopy((log,flight))
    e=copy.deepcopy(a["events"][-1]);w=copy.deepcopy(b["workers"][-1])
    e.update(event_id="FUTURE_OWNER_CANDIDATE_TEST",immutable_sha="1"*40,
             state="OWNER_ADOPTION_CANDIDATE",adoption=False,reviewer_of_sha=None,
             supersedes_event_id=None)
    w.update(id=e["event_id"],exact_return_sha=e["immutable_sha"],
             status=e["state"],owner=e["owner"],first_consumer_adopted=False)
    a["events"].append(e);b["workers"].append(w)
    assert not validate(a,b,seed), validate(a,b,seed)
    print("PASS: 13 mutation witnesses rejected + valid nonadopted owner-candidate stage")

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--selftest",action="store_true")
    ap.add_argument("--baseline-ref",default=None)
    args=ap.parse_args()
    log,flight=load()
    errs=validate(log,flight)
    if args.baseline_ref:
        if not SHA.fullmatch(args.baseline_ref):
            errs.append("BAD_BASELINE_SHA")
        elif subprocess.run(["git","cat-file","-e",args.baseline_ref+"^{commit}"],
                             cwd=ROOT,capture_output=True).returncode:
            errs.append("BASELINE_GIT_COMMIT_UNAVAILABLE")
        else:
            p=subprocess.run(["git","show",args.baseline_ref+
                ":CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/01_RETURN_EVENT_LOG.json"],
                cwd=ROOT,capture_output=True,text=True)
            q=subprocess.run(["git","show",args.baseline_ref+
                ":CROSS_HQ_CONTROL_ROOM/BRANCH_FANIN/02_FLIGHT_AND_PR_REGISTER.json"],
                cwd=ROOT,capture_output=True,text=True)
            for name,resp,current,key in (
                ("EVENT",p,log,"events"),("FLIGHT",q,flight,"workers")
            ):
                if resp.returncode == 0:
                    try:
                        prior=json.loads(resp.stdout).get(key,[])
                        if current.get(key,[])[:len(prior)] != prior:
                            errs.append("PREMAIN_"+name+"_HISTORY_REWRITTEN")
                    except ValueError:
                        errs.append("PREMAIN_"+name+"_UNPARSABLE")
                else:
                    print("First install: "+name+" baseline missing; candidate seed source is separately frozen, owner approval still PENDING")
    if errs:
        for x in errs:
            print("FAIL:",x)
        return 1
    print(f"PASS sourcefree record integrity: {len(log['events'])} events and {len(flight['workers'])} flights; NO ADOPTION ALLOWED")
    if args.selftest:
        selftest(log,flight)
    return 0

if __name__=="__main__":
    raise SystemExit(main())
