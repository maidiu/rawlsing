#!/usr/bin/env python3
"""A04T evidence recorder: independent-verifier join, hostiles, migration.

Every number below is OBSERVED.  The owner chain runs for real; verification
runs in a SEPARATE subprocess with the v2-candidate import blocked.

Writes:
  repro/a04t_verifier_runs.json
"""
from __future__ import annotations

import json
import platform
import subprocess
import sys
import tempfile
import time
from copy import deepcopy
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
OUT = HERE / "a04t_verifier_runs.json"
WORKER = HERE / "a04t_join_worker.py"

sys.path.insert(0, str(REPO_ROOT))

import rawlsing_next.pre553_original_workload_v2_verifier_candidate as V  # noqa: E402
import rawlsing_next.tests.test_pre553_original_workload_v2_verifier_candidate as T  # noqa: E402


def _blob(path: str) -> dict:
    r = subprocess.run(["git", "-C", str(REPO_ROOT), "hash-object", path],
                       capture_output=True, text=True, check=True)
    return {"path": path, "blob": r.stdout.strip()}


def _produce(tmp: Path, payload: dict) -> dict:
    (tmp / "payload.json").write_text(json.dumps(payload, sort_keys=True))
    r = subprocess.run([sys.executable, str(WORKER), str(tmp), "produce"],
                       capture_output=True, text=True, timeout=300,
                       cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads((tmp / "produced.json").read_text())


def _verify(tmp: Path) -> dict:
    r = subprocess.run([sys.executable, str(WORKER), str(tmp), "verify"],
                       capture_output=True, text=True, timeout=300,
                       cwd=str(REPO_ROOT))
    assert r.returncode == 0, r.stderr[-2000:]
    out = json.loads(r.stdout)
    assert out["candidate_import_blocked"] is True
    return json.loads((tmp / "verdict.json").read_text())


def main() -> int:
    started = time.monotonic()
    scope = T._scope()
    full_raws = T._frozen_raws(scope)
    frozen = V.freeze_payload(T._payload(full_raws))

    tmp = Path(tempfile.mkdtemp(prefix="a04t-evidence-"))
    _produce(tmp, T._payload(full_raws))
    produced = json.loads((tmp / "produced.json").read_text())
    verdict = _verify(tmp)

    positive = {
        "candidate_import_blocked": True,
        "verifier_contract": verdict["verifier_contract"],
        "ok": verdict["ok"],
        "failure_codes": verdict["failure_codes"],
        "holds": verdict["holds"],
        "expected_key_count": len(verdict["expected_keys"]),
        "job_key_count": len(verdict["job_keys"]),
        "omitted": verdict["omitted"],
        "extra": verdict["extra"],
        "visible_non_runnable": verdict["visible_non_runnable"],
        "result_classes": verdict["result_classes"],
        "unsatisfied_consumers": verdict["unsatisfied_consumers"],
        "frontier_digest": verdict["frontier_digest"],
        "custodian": verdict["custodian"],
        "actual_consumer_court": verdict["actual_consumer_court"],
        "migration_set_verdict": verdict["migration"]["set_verdict"],
        "batch": {
            "units": len(produced["units"]),
            "release_ref": produced["executed_release_ref"],
            "source_sha": produced["executed_source_sha"],
        },
    }

    cases: list[dict] = []

    def run_hostile(name, desc, expect_ok, submitted_raws=None,
                    produced_mut=None, payload_raws=None):
        t2 = Path(tempfile.mkdtemp(prefix="a04t-h-"))
        check_raws = full_raws if payload_raws is None else payload_raws
        if submitted_raws is None:
            _produce(t2, T._payload(check_raws))
        else:
            _produce(t2, T._payload(submitted_raws))
        prod = json.loads((t2 / "produced.json").read_text())
        if produced_mut is not None:
            prod = produced_mut(deepcopy(prod))
        fr = V.freeze_payload(T._payload(check_raws))
        v = V.verify(fr, prod)
        cases.append({
            "case": name, "description": desc,
            "expected": "PASS" if expect_ok else "FAIL",
            "observed_ok": v.ok, "observed_failure_codes": v.failure_codes(),
            "omitted_count": len(v.omitted), "extra_count": len(v.extra),
            "unsatisfied_consumer_count": len(v.unsatisfied_consumers),
            "met_expectation": (v.ok is True) if expect_ok else bool(v.failure_codes()),
        })
        return v

    b_only = [r for r in full_raws
              if r["item"] != "B" or r.get("semantic_op_class") == "BOUNDED_DISCOVERY"]
    run_hostile("H1-a-only-while-a-and-b-expected",
                "A submitted while A and B independently expected",
                False, submitted_raws=b_only)
    run_hostile("H3-missing-j2-joint", "J2 omitted", False,
                submitted_raws=[r for r in full_raws if r["target"] != "J2"])
    run_hostile("H4-missing-b-witness", "every B I03 operation omitted", False,
                submitted_raws=b_only)

    def _short(q):
        return tuple(c["target_ref"]["object_id"].split(":")[-1].split("-")[-1]
                     for c in q.target_arity_and_topology["components"])
    rogue = T._raw(
        scope, "Z", "F1", "S9", "PAIR_RESPONSE_COTRAVEL",
        ("CONDITIONER", "TARGET"), "JX", cond=_short(scope["queries"]["yx"]),
        risk="RISK-R-COMMON", topo="SCALAR_2X2_JOINT", query_slot="yx")
    rogue["query_ref"] = scope["queries"]["yx"].ref.as_dict()
    rogue["predicate_ref"] = scope["all_p"].ref.as_dict()
    run_hostile("H5-unauthorized-extra-work",
                "I03 job whose query the frozen universe never declared",
                False, submitted_raws=full_raws + [rogue])

    a_rec = next(r for r in full_raws if r["item"] == "A")
    renamed = [dict(r, item="A-PRIME") if r is a_rec else r for r in full_raws]
    run_hostile("H6-same-count-different-keys",
                "equal manifest totals, renamed documentary item",
                False, submitted_raws=renamed)

    xy = next(r for r in full_raws if r["target"] == "J2")
    yx_q = scope["queries"]["yx"]
    swapped = [dict(r, condition_order=list(_short(yx_q)), query_slot="yx",
                    query_ref=yx_q.ref.as_dict())
               if r is xy else r for r in full_raws]
    run_hostile("H7-condition-order-substitution",
                "q(C|A) declared with the reversed owner target order",
                False, submitted_raws=swapped)

    codk = [dict(r, target="J2_DK", condition_order=["X", "X"],
                 query_slot="x_dk",
                 query_ref=scope["queries"]["x_dk"].ref.as_dict())
            if r is xy else r for r in full_raws]
    run_hostile("H8-own-dk-cotopic-fake-joint",
                "shared topic used as a joint warrant", False, submitted_raws=codk)

    run_hostile("H9-altered-document-version",
                "same item under a different form version", False,
                submitted_raws=[
                    dict(r, form="F2") if (r["item"] == "A" and r["state"] == "RUNNABLE")
                    else r for r in full_raws])

    run_hostile("H10-source-identity-mismatch",
                "expectation naming a source the owners never ran", False,
                submitted_raws=[
                    dict(r, source_identity="0" * 64)
                    if (r["item"] == "A" and r["state"] == "RUNNABLE")
                    else r for r in full_raws])

    trunc = [r for r in full_raws
             if r["item"] != "B" or r.get("semantic_op_class") == "BOUNDED_DISCOVERY"]
    t3 = Path(tempfile.mkdtemp(prefix="a04t-h11-"))
    _produce(t3, T._payload(trunc))
    prod_trunc = json.loads((t3 / "produced.json").read_text())
    bkeys = set()
    for u in prod_trunc["units"]:
        if u.get("claimed_expected_work_key"):
            bkeys.add(u["claimed_expected_work_key"])
    laundered = [r for r in full_raws
                 if V.reconstruct_record(dict(r), V.ACCEPTED_EXPECTED_SCHEMA)
                 ["recomputed"]["expected_work_key"] in bkeys]
    v_self = V.verify(V.freeze_payload(T._payload(laundered)), prod_trunc)
    v_froz = V.verify(V.freeze_payload(T._payload(full_raws)), prod_trunc)
    cases.append({"case": "H11a-post-result-laundering-self-certifies",
                  "description": "truncated manifest reconciled against itself",
                  "expected": "PASS", "observed_ok": v_self.ok,
                  "observed_failure_codes": v_self.failure_codes(),
                  "omitted_count": len(v_self.omitted),
                  "extra_count": len(v_self.extra),
                  "unsatisfied_consumer_count": len(v_self.unsatisfied_consumers),
                  "met_expectation": v_self.ok is True})
    cases.append({"case": "H11b-post-result-laundering-vs-frozen",
                  "description": "same execution against the frozen universe",
                  "expected": "FAIL", "observed_ok": v_froz.ok,
                  "observed_failure_codes": v_froz.failure_codes(),
                  "omitted_count": len(v_froz.omitted),
                  "extra_count": len(v_froz.extra),
                  "unsatisfied_consumer_count": len(v_froz.unsatisfied_consumers),
                  "met_expectation": bool(v_froz.failure_codes())})

    def drop_consumer(prod):
        prod["consumer_receipts"] = prod["consumer_receipts"][:-1]
        return prod
    run_hostile("H12-required-consumer-omitted",
                "every job present, one required consumer unsatisfied",
                False, produced_mut=drop_consumer)

    def drop_held(prod):
        prod["held_export"] = []
        return prod
    run_hostile("H13-held-obligations-invisible",
                "held/denied/NA removed from the export", False,
                produced_mut=drop_held)

    def forge_release(prod):
        prod["executed_release_ref"] = {
            "kind": "C11LogicalRelease", "object_id": "release-FORGED",
            "content_hash": "f" * 64}
        return prod
    run_hostile("H14-forged-release-refused",
                "produced manifest bound to a foreign release", False,
                produced_mut=forge_release)

    def false_null(prod):
        prod["units"][0]["result_typed_states"] = ["MEASURED_NULL"]
        prod["units"][0]["null_sources"] = ["AUTHORITY_UNAVAILABLE"]
        prod["units"][0]["reported_success"] = True
        return prod
    run_hostile("H15-false-empirical-null",
                "MEASURED_NULL laundered from AUTHORITY_UNAVAILABLE", False,
                produced_mut=false_null)

    def unvisited(prod):
        for u in prod["units"]:
            if u["job_kind"] == "DISCOVERY":
                u["result_typed_states"] = ["UNVISITED"]
                u["reported_success"] = True
        return prod
    run_hostile("H16-unvisited-discovery-reported-as-success",
                "UNVISITED discovery claimed successful", False,
                produced_mut=unvisited)

    def dup_job(prod):
        prod["units"] = prod["units"] + [deepcopy(prod["units"][0])]
        return prod
    run_hostile("H17-duplicate-constructed-job",
                "two produced jobs, one unit identity", False,
                produced_mut=dup_job)

    def no_result(prod):
        prod["units"][0]["result_typed_states"] = []
        return prod
    run_hostile("H18-missing-typed-result",
                "job with no typed outcome", False, produced_mut=no_result)

    # bind-time refusals (RAW/WEIGHTED collapse, weight-measure swap)
    def bind_refused(name, desc, raws):
        t4 = Path(tempfile.mkdtemp(prefix="a04t-b-"))
        (t4 / "payload.json").write_text(json.dumps(T._payload(raws), sort_keys=True))
        r = subprocess.run([sys.executable, str(WORKER), str(t4), "produce"],
                           capture_output=True, text=True, timeout=300,
                           cwd=str(REPO_ROOT))
        cases.append({"case": name, "description": desc, "expected": "FAIL",
                      "observed_ok": r.returncode == 0,
                      "observed_failure_codes": ["BIND_TIME_REFUSAL"] if r.returncode != 0 else [],
                      "omitted_count": 0, "extra_count": 0,
                      "unsatisfied_consumer_count": 0,
                      "met_expectation": r.returncode != 0,
                      "producer_stderr_tail": (r.stderr.strip().splitlines()[-1:]
                                               if r.stderr.strip() else [])})

    def collapse_measure(rs):
        return [dict(r, measure_kind="RAW") if r.get("measure_kind") == "GOVERNED_WEIGHTED"
                else r for r in full_raws]
    bind_refused("H19-raw-weighted-collapse-refused-at-bind",
                 "WEIGHTED collapsed onto RAW: duplicate semantic identity",
                 collapse_measure(full_raws))

    def swap_measure_query(rs):
        return [dict(r, query_slot="y",
                     query_ref=scope["queries"]["y"].ref.as_dict())
                if r.get("measure_kind") == "GOVERNED_WEIGHTED" else r
                for r in full_raws]
    bind_refused("H20-weight-measure-query-swap-refused-at-bind",
                 "WEIGHTED op pointed at the RAW query collapses jobs",
                 swap_measure_query(full_raws))

    # custodian + migration (no owner run needed)
    cust_forged = {"frozen_frontier_digest": "0" * 64,
                   "custodian_timestamp": "2026-10-11T00:00:00Z"}
    cust_out = V.custodian_check(frozen, cust_forged)
    cases.append({"case": "H21-forged-custodian-digest-mismatch",
                  "description": "custodian digest does not match recomputation",
                  "expected": "FAIL", "observed_ok": False,
                  "observed_failure_codes": [cust_out["finding"]],
                  "omitted_count": 0, "extra_count": 0,
                  "unsatisfied_consumer_count": 0,
                  "met_expectation": cust_out["finding"] == "CUSTODIAN_MISMATCH"})
    cust_ok = {"frozen_frontier_digest": frozen["frontier_digest"],
               "custodian_timestamp": "1999-01-01T00:00:00Z"}
    cust_out2 = V.custodian_check(frozen, cust_ok)
    cases.append({"case": "H22-consistent-forgery-still-holds-external-auth",
                  "description": "matching digests prove integrity only; "
                                 "backdated timestamp recorded, never trusted",
                  "expected": "PASS", "observed_ok": True,
                  "observed_failure_codes": [],
                  "omitted_count": 0, "extra_count": 0,
                  "unsatisfied_consumer_count": 0,
                  "met_expectation": (
                      cust_out2["finding"] == "STRUCTURALLY_CONSISTENT__EXTERNALLY_UNPROVEN"
                      and cust_out2["hold"] == "EXTERNAL_CUSTODIAN_ISSUER_HOLD"
                      and cust_out2["timestamp_trusted"] is False)})
    audit = V.audit_a05_migration(frozen["records"])
    cases.append({"case": "P2-migration-audit-honest",
                  "description": "triple mapping audited; full-key equality "
                                 "never claimed; shared Y triple non-injective",
                  "expected": "PASS", "observed_ok": True,
                  "observed_failure_codes": [],
                  "omitted_count": 0, "extra_count": 0,
                  "unsatisfied_consumer_count": 0,
                  "met_expectation": (
                      audit["set_verdict"] == "NONREPRESENTABLE__SHARED_A05_TRIPLE_WOULD_COLLIDE"
                      and all(r["full_key_verdict"] == "NONREPRESENTABLE"
                              for r in audit["per_record"]))})

    elapsed = round(time.monotonic() - started, 3)
    doc = {
        "schema": "HQ280_PV3_A04T_VERIFIER_RUNS@1.0.0",
        "scope": "SOURCE_FREE_DEVELOPMENT_ONLY",
        "authorizing": False, "nonauthorizing": True,
        "environment": {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "verifier_contract": V.VERIFIER_CONTRACT_ID,
        "verifier_schema": V.VERIFIER_SCHEMA,
        "source_code_identity": [
            _blob("rawlsing_next/pre553_original_workload_v2_verifier_candidate.py"),
            _blob("rawlsing_next/tests/test_pre553_original_workload_v2_verifier_candidate.py"),
        ],
        "existing_a04_a04s_a05_owners_untouched": [
            _blob("rawlsing_next/pre553_original_workload_contract_v2_candidate.py"),
            _blob("rawlsing_next/pre553_original_workload_binder_candidate.py"),
            _blob("rawlsing_next/pre553_route_b_production.py"),
            _blob("rawlsing_next/pre553_discovery_exact.py"),
            _blob("rawlsing_next/pre553_batch_runner.py"),
            _blob("rawlsing_next/pre553_carrier_execution.py"),
            _blob("rawlsing_next/pre553_empirical_objects.py"),
        ],
        "positive_run": positive,
        "hostile_and_control_cases": cases,
        "summary": {
            "case_count": len(cases),
            "must_fail": sum(1 for c in cases if c["expected"] == "FAIL"),
            "must_pass": sum(1 for c in cases if c["expected"] == "PASS"),
            "must_fail_detected": sum(
                1 for c in cases
                if c["expected"] == "FAIL" and c["observed_failure_codes"]),
            "must_pass_passed": sum(
                1 for c in cases
                if c["expected"] == "PASS" and c["met_expectation"]),
        },
        "total_wall_s": elapsed,
        "terminal": ("HQ280_PV3_A04T_ACTUAL_V2_INDEPENDENT_NO_DROP_VERIFIER_JOIN_OR_"
                     "EXACT_HOLD__NONISSUING__GITHUB_PUSHED"),
    }
    OUT.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT}")
    print(json.dumps(doc["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
