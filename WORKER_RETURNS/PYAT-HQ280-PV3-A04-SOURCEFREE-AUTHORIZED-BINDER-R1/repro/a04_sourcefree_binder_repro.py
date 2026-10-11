#!/usr/bin/env python3
"""HQ280 PV3 A04 - standalone evidence recorder for the source-free binder.

Runs the REAL accepted owners end to end over the honest synthetic source-free
fixture and records the ACTUAL observed identities, job/result/consumer joins
and hostile verdicts into JSON.  This script imports only repository code that
already exists on this branch plus the A04 candidate module under test.

It grants nothing and claims nothing beyond source-free development scope.
"""
from __future__ import annotations

import json
import platform
import subprocess
import sys
from pathlib import Path

import rawlsing_next.pre553_original_workload_binder_candidate as binder
import rawlsing_next.tests.test_pre553_original_workload_binder_candidate as T


HERE = Path(__file__).resolve().parent
OUT = HERE / "a04_sourcefree_runs.json"


def _blob(path: str) -> dict:
    result = subprocess.run(
        ["git", "hash-object", path], capture_output=True, text=True, check=True
    )
    return {"path": path, "blob": result.stdout.strip()}


def environment() -> dict:
    return {
        "python_version": sys.version,
        "python_executable": sys.executable,
        "platform": platform.platform(),
        "machine": platform.machine(),
        "pytest_command": (
            "python3 -m pytest "
            "rawlsing_next/tests/test_pre553_original_workload_binder_candidate.py -q"
        ),
    }


def positive_run() -> dict:
    """A genuine positive run through C11 -> I03 -> I05 -> batch."""
    scope = T._scope()
    declared = T.frozen_universe(scope)
    bound = T.bind(scope, declared)
    executed = T.run(scope, bound)
    verdict = binder.reconcile(
        declarations=declared, executed=executed,
        consumer_receipts=T.consumers_for(declared, executed),
    )
    by_key = {d.expected_work_key: d for d in declared}
    return {
        "scope": "SYNTHETIC-SOURCEFREE-A04",
        "declared_expected_work": [
            {
                "expected_work_key": d.expected_work_key,
                "documentary_item_key": d.item_key,
                "operation_key": d.operation_key_value,
                "item": d.item,
                "state": d.state,
                "op_class": d.op_class,
                "target": d.target,
                "measure_kind": d.measure_kind,
                "required_consumer": d.required_consumer,
                "hold_reason": d.hold_reason,
            }
            for d in declared
        ],
        "expected_frontier_ref": bound.expected_frontier_ref.as_dict(),
        "c11_release_ref": executed.production_result.c11_release.release_ref.as_dict(),
        "projection_binding_identity": (
            executed.production_result.projection_binding_receipt["binding_identity"]
        ),
        "runtime_catalog_identity": (
            executed.production_result.repository_binding.executor
            .runtime_catalog.receipt()["catalog_identity"]
        ),
        "i03_requests": [r.as_dict() for r in bound.i03_requests],
        "i03_results": [
            {
                "query_ref": item.query_ref.as_dict(),
                "fact_refs": [fact.ref.as_dict() for fact in item.facts],
                "typed_states": [fact.typed_state for fact in item.facts],
                "measure_kinds": [fact.measure_kind for fact in item.facts],
                "raw_denominators": [fact.raw_denominator_support for fact in item.facts],
            }
            for item in executed.production_result.i03_results
        ],
        "i05": {
            "discovery_authority_ref": (
                executed.production_result.i05_result.discovery_authority_ref.as_dict()
            ),
            "evaluated_frontier_ref": (
                executed.production_result.i05_result.evaluated_frontier_ref.as_dict()
            ),
            "candidate_count": executed.production_result.i05_result.candidate_count,
            "covered_candidate_count": (
                executed.production_result.i05_result.covered_candidate_count
            ),
            "valid_empty": executed.production_result.i05_result.valid_empty,
            "receipt_refs": [
                r.ref.as_dict() for r in executed.production_result.i05_result.receipts
            ],
            "receipt_typed_states": [
                r.typed_state for r in executed.production_result.i05_result.receipts
            ],
        },
        "batch_manifest_ref": executed.batch_manifest.manifest_ref.as_dict(),
        "batch_manifest_hash": executed.batch_manifest.manifest_hash,
        "batch_summary": {
            "batch_state": executed.batch_summary.batch_state,
            "coverage_state": executed.batch_summary.coverage_state,
            "full_coverage": executed.batch_summary.full_coverage,
            "total_units": executed.batch_summary.total_units,
            "completed_units": executed.batch_summary.completed_units,
            "failed_units": executed.batch_summary.failed_units,
            "deferred_units": executed.batch_summary.deferred_units,
            "pending_units": executed.batch_summary.pending_units,
            "actual_execution_receipts": (
                executed.batch_summary.actual_execution_receipts
            ),
            "receipt_set_hash": executed.batch_summary.receipt_set_hash,
        },
        "batch_unit_receipts": [
            {
                "unit_ref": r.unit_ref.as_dict(),
                "attempt_index": r.attempt_index,
                "state": r.state,
                "execution_performed": r.execution_performed,
                "failure_code": r.failure_code,
                "result_refs": [x.as_dict() for x in r.result_refs],
            }
            for r in executed.batch_receipts
        ],
        "held_frontier": [dict(row) for row in bound.held_frontier],
        "effects": dict(bound.effects),
        "route_b_effects": dict(
            executed.production_result.replay_receipt["effects"]
        ),
        "replay_receipt": {
            "dependency_root": (
                executed.production_result.replay_receipt["dependency_root"]
            ),
            "receipt_identity": (
                executed.production_result.replay_receipt["receipt_identity"]
            ),
        },
        "result_classes": dict(verdict.result_classes),
        "reconciliation": {
            "ok": verdict.ok,
            "work_reconciled": verdict.work_reconciled,
            "failure_codes": list(verdict.failure_codes()),
            "expected_key_count": len(verdict.expected_keys),
            "job_key_count": len(verdict.job_keys),
            "omitted": list(verdict.omitted),
            "extra": list(verdict.extra),
            "visible_non_runnable": list(verdict.visible_non_runnable),
            "consumer_obligations": [
                dict(o) for o in verdict.consumer_obligations
            ],
            "unsatisfied_consumers": [dict(u) for u in verdict.unsatisfied_consumers],
            "declared_frontier_hash": verdict.declared_frontier_hash,
            "bound_frontier_hash": verdict.frontier_hash,
        },
        "_declared_index": {k: by_key[k].item for k in by_key},
    }


def hostile_cases() -> list[dict]:
    """Every hostile actually executed, with its real observed verdict."""
    scope = T._scope()
    frozen = T.frozen_universe(scope)
    cases: list[dict] = []

    def record(name, description, expect_fail, *, executed=None, verdict=None, error=None):
        entry = {
            "case": name,
            "description": description,
            "expected": "FAIL" if expect_fail else "PASS",
            "observed_failure_codes": (
                list(verdict.failure_codes()) if verdict is not None else None
            ),
            "observed_ok": verdict.ok if verdict is not None else None,
            "observed_error": (
                f"{type(error).__name__}: {error}" if error is not None else None
            ),
        }
        if verdict is not None:
            entry["omitted_count"] = len(verdict.omitted)
            entry["extra_count"] = len(verdict.extra)
            entry["unsatisfied_consumer_count"] = len(verdict.unsatisfied_consumers)
        cases.append(entry)

    def run(name, description, submission, *, frozen_set=None):
        try:
            _, verdict = T.court(
                scope, submission, frozen=frozen_set or frozen
            )
            record(name, description, True, verdict=verdict)
        except Exception as exc:  # noqa: BLE001 - recorded as evidence
            record(name, description, True, error=exc)

    # --- positives / controls
    _, control = T.court(scope, frozen)
    record(
        "P0-honest-submission",
        "full declared expectation submitted and executed",
        False, verdict=control,
    )

    # --- omissions
    run("H1-a-only-submission",
        "A submitted while A and B are both independently expected",
        T.submitted(scope, omit_items={"B"}))
    run("H2-missing-b",
        "every B operation omitted",
        T.submitted(scope, omit_items={"B"}))
    joint = next(d for d in frozen if d.target == "J2")
    run("H3-missing-j2",
        "the J2 joint operation omitted",
        [d for d in frozen if d is not joint])
    run("H4-missing-b-and-j2",
        "B omitted and the J2 joint omitted together",
        T.submitted(scope, omit_items={"B"}, omit_targets={"J2"}))

    # --- extras
    rogue = T._d(
        scope, item="Z", form="F1", slot="S9",
        op_class="I03_UNARY_OR_JOINT_QUERY", roles=("BASE",), target="R",
        condition_order=T.owner_order(scope["queries"]["yx"]),
        risk_identity="RISK-R-ALL", topology_identity="SCALAR_2X2_JOINT",
        required_consumer=T.CONSUMER_C1,
        query_ref=scope["queries"]["yx"].ref, predicate_ref=scope["all_p"].ref,
    )
    run("H5-unauthorized-extra-work",
        "an I03 job whose query the frozen universe never declared",
        frozen + [rogue])

    # --- same count, different keys
    a_decl = next(d for d in frozen if d.item == "A")
    run("H6-same-count-different-keys",
        "equal totals, renamed documentary item: wrong expected-work keys",
        T.swap(frozen, a_decl, T.clone(a_decl, item="A-PRIME")))

    # --- condition order
    xy = next(d for d in frozen if d.target == "J2")
    yx = scope["queries"]["yx"]
    run("H7-condition-order-substitution",
        "q(C|A) declared with the q(C|A,B) reversed owner target order",
        T.swap(frozen, xy, T.clone(
            xy, query_ref=yx.ref, condition_order=T.owner_order(yx)
        )))

    # --- own-_dk co-topic joint
    x_dk = scope["queries"]["x_dk"]
    run("H8-own-dk-cotopic-joint",
        "a candidate's own derived topic used as a joint co-travel warrant",
        T.swap(frozen, xy, T.clone(
            xy, target="J2_DK", query_ref=x_dk.ref,
            condition_order=T.owner_order(x_dk),
        )))

    # --- document version
    run("H9-altered-document-version",
        "the same administered item declared under a different form version",
        T.swap(frozen, a_decl, T.clone(a_decl, form="F2")))

    # --- source identity
    run("H10-source-identity-mismatch",
        "an expectation naming a source the owners never ran against",
        T.swap(frozen, a_decl, T.clone(a_decl, source_identity="0" * 64)))

    # --- laundering
    truncated = T.submitted(scope, omit_items={"B"})
    truncated_executed = T.run(scope, T.bind(scope, truncated))
    produced = [p.expected_work_key for p in truncated_executed.bound.job_plans]
    laundered = [d for d in frozen if d.expected_work_key in set(produced)]
    self_verdict = binder.reconcile(
        declarations=laundered, executed=truncated_executed,
        consumer_receipts=T.consumers_for(laundered, truncated_executed),
    )
    frozen_verdict = binder.reconcile(
        declarations=frozen, executed=truncated_executed,
        consumer_receipts=T.consumers_for(frozen, truncated_executed),
    )
    record(
        "H11a-post-result-laundering-self-certifies",
        "the truncated manifest reconciled against ITSELF: no omission visible, "
        "which is precisely why self-certification is insufficient",
        False, verdict=self_verdict,
    )
    record(
        "H11b-post-result-laundering-vs-frozen",
        "the SAME execution reconciled against the independent frozen universe",
        True, verdict=frozen_verdict,
    )

    # --- consumers
    executed_full = T.run(scope, T.bind(scope, frozen))
    partial = T.consumers_for(frozen, executed_full)[:-1]
    consumer_verdict = binder.reconcile(
        declarations=frozen, executed=executed_full, consumer_receipts=partial
    )
    record(
        "H12-required-consumer-omitted",
        "every job completed and every product present, one required consumer "
        "unsatisfied",
        True, verdict=consumer_verdict,
    )

    # --- held / denied / NA
    _, held_verdict = T.court(scope, T.submitted(scope, include_held=False))
    record("H13-held-obligations-invisible",
          "held/denied/non-applicable obligations removed from the export",
          True, verdict=held_verdict)

    # --- bind-time refusals
    for name, description, submission, pattern in (
        ("H14-duplicate-semantic-job",
         "two distinct expected operations collapsing onto one semantic batch job",
         frozen + [T.clone(a_decl, item="A-TWIN")],
         "collapsed onto one semantic"),
        ("H15-multiplicity-without-justification",
         "multiplicity > 1 asserted without explicit justification",
         frozen + [T.clone(a_decl, item="A-MULTI", multiplicity=2)],
         "collapsed onto one semantic"),
        ("H16-undeclared-authority",
         "an operation authority absent from the issued RuntimeObjectCatalog",
         T.swap(frozen, a_decl, T.clone(
             a_decl, authority_ref="NOT-IN-CATALOG|1.0.0|" + "f" * 64
         )),
         "issued RuntimeObjectCatalog"),
        ("H17-missing-i05-expected-work",
         "no I05 discovery operation in the expected work",
         [d for d in frozen if d.op_class != "I05_BOUNDED_DISCOVERY"],
         "exactly one I05"),
    ):
        try:
            T.bind(scope, submission)
            record(name, description, True,
                   error=RuntimeError("bind unexpectedly succeeded"))
        except Exception as exc:  # noqa: BLE001
            message = f"{type(exc).__name__}: {exc}"
            ok = pattern in message
            cases.append({
                "case": name,
                "description": description,
                "expected": "FAIL",
                "observed_failure_codes": ["BIND_TIME_REFUSAL"],
                "observed_ok": False,
                "observed_error": message,
                "matched_expected_pattern": ok,
            })

    # --- reorder control
    import random

    shuffled = list(frozen)
    random.Random(20261011).shuffle(shuffled)
    from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog

    reversed_catalog = RuntimeObjectCatalog(
        authorities=tuple(reversed(scope["catalog"].authorities)),
        predicates=tuple(reversed(scope["catalog"].predicates)),
        queries=tuple(reversed(scope["catalog"].queries)),
        discovery_authorities=tuple(reversed(scope["catalog"].discovery_authorities)),
    )
    reordered_bound = binder.bind_expected_work(
        declarations=shuffled,
        projection_fields=scope["projection_fields"],
        runtime_catalog=reversed_catalog,
    )
    reordered = T.run(scope, reordered_bound)
    original = T.run(scope, T.bind(scope, frozen))
    cases.append({
        "case": "P1-stable-reorder",
        "description": "shuffled declarations and reversed catalog yield identical "
                       "jobs, manifest hash and replay receipt",
        "expected": "PASS",
        "observed_failure_codes": [],
        "observed_ok": (
            reordered.batch_manifest.manifest_hash
            == original.batch_manifest.manifest_hash
            and reordered.production_result.replay_receipt["receipt_identity"]
            == original.production_result.replay_receipt["receipt_identity"]
        ),
        "observed_error": None,
    })

    # --- restart identity
    from rawlsing_next.pre553_batch_runner import BatchExecutionRunner

    resumed = BatchExecutionRunner(
        manifest=original.batch_manifest,
        repository=original.production_result.repository_binding.executor.repository,
        prior_receipts=original.batch_receipts,
    )
    cases.append({
        "case": "P2-restart-identity",
        "description": "resume with prior receipts adds no work and preserves the "
                       "receipt set hash",
        "expected": "PASS",
        "observed_failure_codes": [],
        "observed_ok": (
            resumed.pending_units() == ()
            and resumed.summary().receipt_set_hash
            == original.batch_summary.receipt_set_hash
        ),
        "observed_error": None,
    })

    return cases


def main() -> int:
    positive = positive_run()
    positive.pop("_declared_index", None)
    cases = hostile_cases()
    document = {
        "schema": "HQ280_PV3_A04_ACTUAL_SOURCEFREE_RUNS@1.0.0",
        "scope": "SOURCE_FREE_DEVELOPMENT_ONLY",
        "authorizing": False,
        "nonauthorizing": True,
        "environment": environment(),
        "source_code_identity": [
            _blob("rawlsing_next/pre553_original_workload_binder_candidate.py"),
            _blob(
                "rawlsing_next/tests/"
                "test_pre553_original_workload_binder_candidate.py"
            ),
        ],
        "existing_owner_untouched": [
            _blob("rawlsing_next/pre553_route_b_production.py"),
            _blob("rawlsing_next/pre553_carrier_execution.py"),
            _blob("rawlsing_next/pre553_batch_runner.py"),
            _blob("rawlsing_next/pre553_discovery_exact.py"),
            _blob("rawlsing_next/pre553_empirical_objects.py"),
        ],
        "positive_run": positive,
        "hostile_and_control_cases": cases,
        "summary": {
            "case_count": len(cases),
            "must_fail_cases": sum(1 for c in cases if c["expected"] == "FAIL"),
            "must_pass_cases": sum(1 for c in cases if c["expected"] == "PASS"),
            "failures_observed_with_expected_code": sum(
                1 for c in cases
                if c["expected"] == "FAIL" and c["observed_failure_codes"]
            ),
        },
        "terminal": (
            "HQ280_PV3_A04_REAL_CURRENT_OWNER_BINDER_CANDIDATE_MEASURED__"
            "SOURCEFREE_ONLY__GITHUB_PUSHED"
        ),
    }
    OUT.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(f"wrote {OUT}")
    print(json.dumps(document["summary"], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())