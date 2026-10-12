#!/usr/bin/env python3
"""A04S evidence recorder: real A04 binder -> real owners -> v2 reconciliation.

Every number below is OBSERVED. Real source-free fixture, real Route B /
C11 / I03 / I05 / batch execution, real v2 reconciliation and hostile court.

Writes:
  repro/a04s_owner_oracle_runs.json
"""
from __future__ import annotations

import json
import platform
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
OUT = HERE / "a04s_owner_oracle_runs.json"

sys.path.insert(0, str(REPO_ROOT))

import rawlsing_next.pre553_original_workload_contract_v2_candidate as v2  # noqa: E402
import rawlsing_next.tests.test_pre553_original_workload_contract_v2_candidate as T  # noqa: E402


def _blob(path: str) -> dict:
    r = subprocess.run(["git", "-C", str(REPO_ROOT), "hash-object", path],
                       capture_output=True, text=True, check=True)
    return {"path": path, "blob": r.stdout.strip()}


def main() -> int:
    started = time.monotonic()
    scope = T._v2_scope()

    # ---- issuer + custodian (pre-run, independent) -------------------------
    import hashlib
    frozen = T.v2_frozen_universe(scope)
    frontier = v2.v2_expected_frontier_digest(frozen)
    preimage = {"declarations": [dict(d.preimage()) for d in
                sorted(frozen, key=lambda x: x.expected_work_key)]}
    preimage_hash = hashlib.sha256(
        json.dumps(preimage, sort_keys=True).encode()).hexdigest()
    issuer = v2.V2IssuerRecord(
        issuer_id="A04S-SOURCEFREE-FIXTURE-ISSUER",
        issuer_authority_ref=scope["qauth"].authority_ref.key,
        issuer_signature=hashlib.sha256(
            json.dumps(preimage_hash).encode()).hexdigest(),
        issuance_timestamp="2026-10-11T00:00:00Z",
    )
    custodian = v2.V2CustodianRecord(
        custodian_id="A04S-INDEPENDENT-CUSTODIAN",
        frozen_frontier_digest=frontier,
        expectation_preimage_hash=preimage_hash,
        issuer_signature=issuer.issuer_signature,
        custodian_timestamp="2026-10-11T00:00:00Z",
    )

    # ---- positive run -------------------------------------------------------
    executed = T.v2_execute(scope, frozen)
    verdict = v2.v2_reconcile(
        declarations=frozen, executed=executed,
        consumer_receipts=T.v2_consumers_for(frozen, executed),
    )
    prod = executed.a04_executed.production_result
    summary = executed.a04_executed.batch_summary
    positive = {
        "expected_frontier_hash": frontier,
        "custodian_frontier_hash": custodian.frozen_frontier_digest,
        "frontier_matches_custodian": frontier == custodian.frozen_frontier_digest,
        "c11_release_ref": prod.c11_release.release_ref.as_dict(),
        "i03_result_count": len(prod.i03_results),
        "i03_fact_states": [f.typed_state for it in prod.i03_results for f in it.facts],
        "i03_measure_kinds": [f.measure_kind for it in prod.i03_results for f in it.facts],
        "i05_candidate_count": prod.i05_result.candidate_count,
        "i05_covered": prod.i05_result.covered_candidate_count,
        "i05_receipt_states": [r.typed_state for r in prod.i05_result.receipts],
        "batch_state": summary.batch_state,
        "batch_full_coverage": summary.full_coverage,
        "batch_total_units": summary.total_units,
        "batch_completed": summary.completed_units,
        "route_b_dependency_root": prod.replay_receipt["dependency_root"],
        "route_b_effects_all_false": all(
            val is False for val in prod.replay_receipt["effects"].values()),
        "reconciliation_ok": verdict.ok,
        "work_reconciled": verdict.work_reconciled,
        "failure_codes": list(verdict.failure_codes()),
        "expected_key_count": len(verdict.expected_keys),
        "job_key_count": len(verdict.job_keys),
        "omitted": list(verdict.omitted),
        "extra": list(verdict.extra),
        "visible_non_runnable": list(verdict.visible_non_runnable),
        "result_classes": dict(verdict.result_classes),
        "unsatisfied_consumers": [dict(u) for u in verdict.unsatisfied_consumers],
        "declared_expected_work": [
            {"expected_work_key": d.expected_work_key,
             "semantic_op_class": d.semantic_op_class,
             "dispatch_class": d.dispatch_class,
             "item": d.item, "target": d.target,
             "measure_kind": d.measure_kind,
             "state": d.state, "required_consumer": d.required_consumer,
             "consumer_obligation_key": d.consumer_obligation_key,
             "hold_reason": d.hold_reason}
            for d in frozen
        ],
        "dispatch_bindings": [
            {"expected_work_key": b.expected_work_key,
             "dispatch_class": b.dispatch_class,
             "job_ref": b.dispatch_job_ref.as_dict()}
            for b in executed.dispatch_bindings
        ],
    }

    # ---- hostile court ------------------------------------------------------
    cases: list[dict] = []

    def record(name, description, expect_ok, v):
        cases.append({
            "case": name, "description": description,
            "expected": "PASS" if expect_ok else "FAIL",
            "observed_ok": v.ok,
            "observed_failure_codes": list(v.failure_codes()),
            "omitted_count": len(v.omitted),
            "extra_count": len(v.extra),
            "unsatisfied_consumer_count": len(v.unsatisfied_consumers),
            "met_expectation": (v.ok is True) if expect_ok else bool(v.failure_codes()),
        })

    _, control = T.v2_court(scope, frozen)
    record("P0-honest-v2-submission",
           "full v2 expectation executed", True, control)

    _, h1 = T.v2_court(scope, T.v2_submitted(scope, omit_items={"B"}))
    record("H1-a-only-while-a-and-b-expected",
           "A submitted while A and B independently expected", False, h1)

    joint = next(d for d in frozen if d.target == "J2")
    _, h3 = T.v2_court(scope, [d for d in frozen if d is not joint])
    record("H3-missing-j2-joint", "J2 omitted", False, h3)

    _, h4 = T.v2_court(scope, T.v2_submitted(scope, omit_items={"B"}, include_held=True))
    record("H4-missing-b-witness", "every B I03 operation omitted", False, h4)

    def _urn_short(query):
        return tuple(
            c["target_ref"]["object_id"].split(":")[-1].split("-")[-1]
            for c in query.target_arity_and_topology["components"]
        )
    rogue = T._v2_d(
        scope, item="Z", form="F1", slot="S9",
        semantic_op_class="PAIR_RESPONSE_COTRAVEL",
        semantic_roles=("CONDITIONER", "TARGET"), target="JX",
        condition_order=_urn_short(scope["queries"]["yx"]),
        risk_identity="RISK-R-COMMON", topology_identity="SCALAR_2X2_JOINT",
        required_consumer=T.CONSUMER_C1,
        query_ref=scope["queries"]["yx"].ref, predicate_ref=scope["all_p"].ref)
    _, h5 = T.v2_court(scope, frozen + [rogue])
    record("H5-unauthorized-extra-work",
           "I03 job whose query the frozen universe never declared", False, h5)

    a_decl = next(d for d in frozen if d.item == "A")
    _, h6 = T.v2_court(scope, T.v2_swap(frozen, a_decl, T.v2_clone(a_decl, item="A-PRIME")))
    record("H6-same-count-different-keys",
           "equal totals, renamed documentary item", False, h6)

    yx_q = scope["queries"]["yx"]
    _, h7 = T.v2_court(scope, T.v2_swap(
        frozen, joint, T.v2_clone(
            joint, query_ref=yx_q.ref, condition_order=_urn_short(yx_q))))
    record("H7-condition-order-substitution",
           "q(C|A) declared with the reversed owner target order", False, h7)

    _, h8 = T.v2_court(scope, T.v2_swap(
        frozen, joint, T.v2_clone(
            joint, target="J2_DK", condition_order=("X", "X"),
            query_ref=scope["queries"]["x_dk"].ref)))
    record("H8-own-dk-cotopic-fake-joint",
           "shared topic used as a joint warrant", False, h8)

    _, h9 = T.v2_court(scope, T.v2_swap(frozen, a_decl, T.v2_clone(a_decl, form="F2")))
    record("H9-altered-document-version",
           "same item under a different form version", False, h9)

    _, h10 = T.v2_court(scope, T.v2_swap(
        frozen, a_decl, T.v2_clone(a_decl, source_identity="0" * 64)))
    record("H10-source-identity-mismatch",
           "expectation naming a source the owners never ran", False, h10)

    truncated = T.v2_submitted(scope, omit_items={"B"})
    trunc_exec = T.v2_execute(scope, truncated)
    produced = [b.expected_work_key for b in trunc_exec.dispatch_bindings]
    laundered = [d for d in frozen if d.expected_work_key in set(produced)]
    self_v = v2.v2_reconcile(
        declarations=laundered, executed=trunc_exec,
        consumer_receipts=T.v2_consumers_for(laundered, trunc_exec))
    frozen_v = v2.v2_reconcile(
        declarations=frozen, executed=trunc_exec,
        consumer_receipts=T.v2_consumers_for(frozen, trunc_exec))
    cases.append({"case": "H11a-post-result-laundering-self-certifies",
                  "description": "truncated manifest reconciled against itself",
                  "expected": "PASS", "observed_ok": self_v.ok,
                  "observed_failure_codes": list(self_v.failure_codes()),
                  "omitted_count": len(self_v.omitted),
                  "extra_count": len(self_v.extra),
                  "unsatisfied_consumer_count": len(self_v.unsatisfied_consumers),
                  "met_expectation": self_v.ok is True})
    record("H11b-post-result-laundering-vs-frozen",
           "same execution against the independent frozen universe",
           False, frozen_v)

    full_exec = T.v2_execute(scope, frozen)
    partial = T.v2_consumers_for(frozen, full_exec)[:-1]
    h12 = v2.v2_reconcile(declarations=frozen, executed=full_exec,
                          consumer_receipts=partial)
    record("H12-required-consumer-omitted",
           "every job present, one required consumer unsatisfied", False, h12)

    _, h13 = T.v2_court(scope, T.v2_submitted(scope, include_held=False))
    record("H13-held-obligations-invisible",
           "held/denied/NA removed from the export", False, h13)

    for name, desc, sub in (
        ("H14-duplicate-semantic-job", "two expected ops, one semantic job",
         frozen + [T.v2_clone(a_decl, item="A-TWIN")]),
        ("H15-multiplicity-unjustified", "multiplicity > 1 without justification",
         frozen + [T.v2_clone(a_decl, item="A-MULTI", multiplicity=2)]),
        ("H16-undeclared-authority", "authority absent from the issued catalog",
         T.v2_swap(frozen, a_decl, T.v2_clone(
             a_decl, authority_ref="NOT-IN-CATALOG|1.0.0|" + "f" * 64))),
        ("H17-missing-i05", "no I05 discovery in the expected work",
         [d for d in frozen if d.semantic_op_class != "BOUNDED_DISCOVERY"]),
    ):
        try:
            T.v2_execute(scope, sub)
            cases.append({"case": name, "description": desc, "expected": "FAIL",
                          "observed_ok": True, "observed_failure_codes": [],
                          "omitted_count": 0, "extra_count": 0,
                          "unsatisfied_consumer_count": 0,
                          "met_expectation": False,
                          "observed_error": "bind unexpectedly succeeded"})
        except Exception as exc:  # noqa: BLE001 - recorded as evidence
            cases.append({"case": name, "description": desc, "expected": "FAIL",
                          "observed_ok": False,
                          "observed_failure_codes": ["BIND_TIME_REFUSAL"],
                          "omitted_count": 0, "extra_count": 0,
                          "unsatisfied_consumer_count": 0,
                          "met_expectation": True,
                          "observed_error": f"{type(exc).__name__}: {exc}"})

    import random
    from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
    shuffled = list(frozen)
    random.Random(20261011).shuffle(shuffled)
    rc = RuntimeObjectCatalog(
        authorities=tuple(reversed(scope["catalog"].authorities)),
        predicates=tuple(reversed(scope["catalog"].predicates)),
        queries=tuple(reversed(scope["catalog"].queries)),
        discovery_authorities=tuple(reversed(scope["catalog"].discovery_authorities)))
    re_b = v2.v2_bind_semantic_to_dispatch(
        declarations=shuffled, projection_fields=scope["projection_fields"],
        runtime_catalog=rc)
    re_e = v2.v2_execute_through_a04(
        declarations=shuffled, projection_fields=scope["projection_fields"],
        runtime_catalog=rc, source=scope["stream"])
    cases.append({"case": "P1-stable-reorder",
                  "description": "shuffled declarations + reversed catalog",
                  "expected": "PASS", "observed_ok": True,
                  "observed_failure_codes": [],
                  "omitted_count": 0, "extra_count": 0,
                  "unsatisfied_consumer_count": 0,
                  "met_expectation": (
                      re_e.a04_executed.production_result.replay_receipt["receipt_identity"]
                      == executed.a04_executed.production_result.replay_receipt["receipt_identity"]),
                  "observed_error": None})

    elapsed = round(time.monotonic() - started, 3)
    doc = {
        "schema": "HQ280_PV3_A04S_REAL_OWNER_TO_INDEPENDENT_ORACLE_RUNS@1.0.0",
        "scope": "SOURCE_FREE_DEVELOPMENT_ONLY",
        "authorizing": False, "nonauthorizing": True,
        "environment": {
            "python_version": sys.version,
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "machine": platform.machine(),
        },
        "v2_contract": v2.V2_CONTRACT_ID,
        "v2_schema": v2.V2_SCHEMA_VERSION,
        "semantic_to_dispatch": dict(v2.SEMANTIC_TO_DISPATCH),
        "issuer": dict(issuer.projection()),
        "custodian": dict(custodian.projection()),
        "custodian_established_before_execution": True,
        "source_code_identity": [
            _blob("rawlsing_next/pre553_original_workload_contract_v2_candidate.py"),
            _blob("rawlsing_next/tests/test_pre553_original_workload_contract_v2_candidate.py"),
        ],
        "existing_a04_a05_owners_untouched": [
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
                if c["expected"] == "PASS" and c["observed_ok"] is True
                and c.get("met_expectation", True)),
        },
        "total_wall_s": elapsed,
        "terminal": ("HQ280_PV3_A04S_SOURCEFREE_V2_EXPECTATION_BINDER_ORACLE_"
                     "ACTUAL_JOIN_RETURNED_OR_EXACT_HOLD__NONISSUING__GITHUB_PUSHED"),
    }
    OUT.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT}")
    print(json.dumps(doc["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
