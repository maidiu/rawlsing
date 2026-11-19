#!/usr/bin/env python3
"""Trace the SRC16 native I03 unresolved fact through actual saved I05/Batch.

TEST_ONLY sourcefree fixture.  It reuses existing native owners and existing
test fixtures; it does not author a producer, issuer, evaluator, or Batch path.
No original source, configuration, grant, or private artifact is accessed.
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
import os
import sys
import tempfile
import traceback
from pathlib import Path

IMPLEMENTER = Path(os.environ.get(
    "ANVIL_IMPLEMENTER",
    "/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER",
)).resolve()
SRC16 = IMPLEMENTER / "WORKER_RETURNS" / "ANVIL_SRC16_SHARED_SQLITE_FREE_RUNNER_20261119"
sys.path.insert(0, str(IMPLEMENTER))

import pytest  # noqa: E402  (existing test-fixture harness only)

from rawlsing_next.pre553_batch_runner import (  # noqa: E402
    BatchManifest,
    BatchUnitSpec,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog  # noqa: E402
from rawlsing_next.pre553_prepared_saved_i03 import PreparedSavedC11Admission  # noqa: E402
from rawlsing_next.pre553_saved_workload_integration import (  # noqa: E402
    execute_saved_batch,
)
from rawlsing_next.pre553_source_direct_parquet_estate import (  # noqa: E402
    DirectEstateError,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (  # noqa: E402
    _atom,
    _d_auth,
    _discovery_authority,
    _grammar,
    _qt,
    _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import (  # noqa: E402
    _branch_predicate,
    _query,
)
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture  # noqa: E402
from rawlsing_next.tests.test_pyat940_s2f_b_negative_and_multisource import (  # noqa: E402
    _unsupported_topology_query,
)

HERE = Path(__file__).resolve().parent
OUT = HERE / "TRACE.json"
SCRATCH = Path(os.environ.get(
    "ANVIL_TRACE_SCRATCH",
    "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode",
))
FORBIDDEN_SOURCE_NAMES = ("source", "raw", "original", "wave1")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ref_kinds(refs):
    return [ref.kind for ref in refs]


def summary_dict(summary):
    return {
        "batch_state": summary.batch_state,
        "coverage_state": summary.coverage_state,
        "full_coverage": summary.full_coverage,
        "total_units": summary.total_units,
        "completed_units": summary.completed_units,
        "failed_units": summary.failed_units,
        "deferred_units": summary.deferred_units,
        "pending_units": summary.pending_units,
        "actual_execution_receipts": summary.actual_execution_receipts,
        "populated_data_execution_claim": summary.populated_data_execution_claim,
    }


def main() -> int:
    scratch = Path(tempfile.mkdtemp(prefix="src16-i03-i05-batch-", dir=SCRATCH))
    monkeypatch = pytest.MonkeyPatch()
    result = {
        "schema": "ANVIL_SRC16_I03_I05_BATCH_TRACE@1",
        "sourcefree": True,
        "original_source_accessed": False,
        "product_files_modified": False,
        "fixture": "existing rawlsing_next.tests.test_pre553_prepared_saved_i03._fixture",
        "batch_api": "rawlsing_next.pre553_saved_workload_integration.execute_saved_batch",
        "scratch": str(scratch),
        "pins": {
            "src16_handoff_sha256": sha256(SRC16 / "00_HANDOFF.md"),
            "src16_receipt_sha256": sha256(SRC16 / "receipt.json"),
            "discovery_exact_sha256": sha256(IMPLEMENTER / "rawlsing_next" / "pre553_discovery_exact.py"),
            "prepared_saved_i03_sha256": sha256(IMPLEMENTER / "rawlsing_next" / "pre553_prepared_saved_i03.py"),
            "saved_workload_integration_sha256": sha256(IMPLEMENTER / "rawlsing_next" / "pre553_saved_workload_integration.py"),
            "batch_runner_sha256": sha256(IMPLEMENTER / "rawlsing_next" / "pre553_batch_runner.py"),
            "saved_c11_admission_sha256": sha256(IMPLEMENTER / "rawlsing_next" / "pre553_saved_c11_admission.py"),
        },
    }
    try:
        source, qa, all_p, _other, queries, base_admission = _fixture(
            monkeypatch, scratch / "fixture", "TRACE-SRC16",
        )
        negative_query = _unsupported_topology_query(
            source, qa, all_p, tag="trace-negative",
        )
        dn = _d_auth("trace-negative")
        unresolved_grammar = _grammar(
            operation="I03-OP-trace-negative",
            atoms=[_atom("ALL", all_p, "BRANCH")],
            templates=[_qt("NEG", negative_query)],
            rules=[_rule(
                "negative",
                "MINORITY_OR_NONMODAL_DEPARTURE",
                "SINGLE_ATOM",
                atom_ids=("ALL",),
                baseline_atom_id="ALL",
                query_template_id="NEG",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )],
        )
        unresolved_authority = _discovery_authority(
            source, unresolved_grammar, dn, tag="trace-negative",
        )

        empty_predicate = _branch_predicate(source, qa, members=(), tag="trace-empty")
        empty_query = _query(source, qa, empty_predicate, ("Y",), tag="trace-empty")
        de = _d_auth("trace-empty")
        empty_grammar = _grammar(
            operation="I03-OP-trace-empty",
            atoms=[
                _atom("ALL", all_p, "BRANCH"),
                _atom("EMPTY", empty_predicate, "BRANCH"),
            ],
            templates=[_qt("EMPTY", empty_query)],
            rules=[_rule(
                "empty",
                "MINORITY_OR_NONMODAL_DEPARTURE",
                "SINGLE_ATOM",
                atom_ids=("EMPTY",),
                baseline_atom_id="ALL",
                query_template_id="EMPTY",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )],
        )
        empty_authority = _discovery_authority(
            source, empty_grammar, de, tag="trace-empty",
        )

        catalog = RuntimeObjectCatalog(
            authorities=tuple((*source["authorities"], qa, dn, de)),
            predicates=(all_p, empty_predicate),
            queries=(queries["selected"], negative_query, empty_query),
            discovery_authorities=(unresolved_authority, empty_authority),
        )
        admission = PreparedSavedC11Admission.open(
            root=Path(base_admission.estate_path).parents[1],
            exact_path=base_admission.estate_path,
            independently_held_manifest_sha256=base_admission.manifest_sha256,
            independently_held_i02=base_admission.i02,
            release_ref=base_admission.release_ref,
            runtime_catalog=catalog,
            current_authorizer=lambda _roots: True,
        )

        positive = admission.execute_i03(
            query_ref=queries["selected"].ref, predicate_ref=all_p.ref,
        )
        unresolved = admission.execute_i05(
            discovery_authority_ref=unresolved_authority.ref,
        )
        empty = admission.execute_i05(
            discovery_authority_ref=empty_authority.ref,
        )

        result["positive_i03"] = {
            "typed_state": positive.facts[0].typed_state,
            "raw_denominator_support": positive.facts[0].raw_denominator_support,
            "fact_count": len(positive.facts),
        }
        result["unresolved_i05"] = {
            "native_i03_fact_states": [
                fact.typed_state for fact in unresolved.empirical_facts
            ],
            "receipt_coverage_states": [
                receipt.coverage_state for receipt in unresolved.receipts
            ],
            "receipt_typed_states": [
                receipt.typed_state for receipt in unresolved.receipts
            ],
            "valid_empty": unresolved.valid_empty,
            "first_mapping": {
                "source_states": "UNRESOLVED",
                "mapped_fact_class": "UNAVAILABLE",
                "mapped_coverage": "EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY",
                "mapped_typed_state": "COVERAGE_LIMITED",
                "location": "rawlsing_next/pre553_discovery_exact.py:_terminal_fact_class / _evaluate_candidate",
            },
        }
        result["valid_empty_i05"] = {
            "native_i03_fact_states": [fact.typed_state for fact in empty.empirical_facts],
            "receipt_coverage_states": [r.coverage_state for r in empty.receipts],
            "receipt_typed_states": [r.typed_state for r in empty.receipts],
            "valid_empty": empty.valid_empty,
            "distinct_from_unresolved": (
                empty.receipts[0].coverage_state != unresolved.receipts[0].coverage_state
                and empty.valid_empty is not unresolved.valid_empty
            ),
        }

        manifest = BatchManifest((
            BatchUnitSpec(
                "QUERY", queries["selected"].ref,
                (admission.release_ref,), (all_p.ref,),
            ),
            BatchUnitSpec(
                "DISCOVERY", unresolved_authority.ref,
                (admission.release_ref,),
            ),
            BatchUnitSpec(
                "DISCOVERY", empty_authority.ref,
                (admission.release_ref,),
            ),
        ))
        batch = execute_saved_batch(
            admission,
            manifest=manifest,
            predicate_ref_by_query={queries["selected"].ref.key: all_p.ref},
        )
        result["batch"] = {
            "receipts": [
                {
                    "state": receipt.state,
                    "execution_performed": receipt.execution_performed,
                    "result_kinds": ref_kinds(receipt.result_refs),
                }
                for receipt in batch.receipts
            ],
            "summary": summary_dict(batch.summary()),
            "receipt_has_typed_fact_state": any(
                hasattr(receipt, "typed_state") for receipt in batch.receipts
            ),
            "result_refs_include_empirical_fact": any(
                any(ref.kind == "EmpiricalFact@1.0.0" for ref in receipt.result_refs)
                for receipt in batch.receipts
            ),
            "observation": (
                "Batch COMPLETED is operational execution, not an empirical-fact "
                "or VALID_EMPTY claim; result refs are DiscoveryResultReceipt refs."
            ),
        }

        # Prior completed receipts are reused by execute_saved_batch without an
        # exact native-output argument.  Prove whether a forged result ref is
        # accepted and can therefore become a stale completed interpretation.
        forged = tuple(
            dataclasses.replace(receipt, result_refs=(all_p.ref,))
            for receipt in batch.receipts
        )
        forged_run = execute_saved_batch(
            admission,
            manifest=manifest,
            predicate_ref_by_query={queries["selected"].ref.key: all_p.ref},
            prior_receipts=forged,
        )
        result["batch_prior_receipt_reuse"] = {
            "forged_result_kind": ref_kinds(forged[0].result_refs)[0],
            "forged_receipt_count": len(forged),
            "returned_receipt_count": len(forged_run.receipts),
            "all_forged_receipts_retained": all(
                any(
                    observed.receipt_ref == supplied.receipt_ref
                    and observed.result_refs == supplied.result_refs
                    for observed in forged_run.receipts
                )
                for supplied in forged
            ),
            "reused_states": [r.state for r in forged_run.receipts],
            "summary": summary_dict(forged_run.summary()),
            "native_execution_required": False,
            "observation": (
                "All COMPLETED prior receipts with non-result refs are accepted; "
                "execute_saved_batch has no prior-output consistency check."
            ),
        }

        # Existing current-authority denial remains fail-closed, including a
        # prior receipt that would otherwise be reused.
        state = {"now": True}
        denied = PreparedSavedC11Admission.open(
            root=Path(base_admission.estate_path).parents[1],
            exact_path=base_admission.estate_path,
            independently_held_manifest_sha256=base_admission.manifest_sha256,
            independently_held_i02=base_admission.i02,
            release_ref=base_admission.release_ref,
            runtime_catalog=catalog,
            current_authorizer=lambda _roots: state["now"],
        )
        state["now"] = False
        denial = {}
        try:
            denied.execute_i05(discovery_authority_ref=unresolved_authority.ref)
            denial["direct_i05"] = "NOT_REFUSED"
        except DirectEstateError as exc:
            denial["direct_i05"] = {
                "type": type(exc).__name__,
                "message": str(exc),
            }
        try:
            execute_saved_batch(
                denied,
                manifest=manifest,
                predicate_ref_by_query={queries["selected"].ref.key: all_p.ref},
                prior_receipts=forged,
            )
            denial["prior_receipt_batch"] = "NOT_REFUSED"
        except DirectEstateError as exc:
            denial["prior_receipt_batch"] = {
                "type": type(exc).__name__,
                "message": str(exc),
            }
        result["rights_denial"] = denial
        result["status"] = (
            "FIRST_DISCREPANCY__UNRESOLVED_MAPPED_TO_COVERAGE_LIMITED__"
            "BATCH_PRIOR_RECEIPT_REUSE_UNVALIDATED"
        )
        result["existing_src16_status"] = {
            "receipt_status": "SOURCE_NEUTRAL_RAW_LANE_PASS__I03_LEAF_GUARD_MIXED_RED_GREEN_PASS__I05_BATCH_PENDING",
            "handoff_statement": "I05/Batch was not exercised here.",
            "correct_as_pending": True,
        }
        result["first_discrepancy"] = {
            "where": "I05 terminal mapping after native I03 output",
            "source_fact_states": [f.typed_state for f in unresolved.empirical_facts],
            "emitted_coverage_state": unresolved.receipts[0].coverage_state,
            "emitted_typed_state": unresolved.receipts[0].typed_state,
            "why": (
                "UNRESOLVED is collapsed with UNAVAILABLE in "
                "_terminal_fact_class before _evaluate_candidate selects "
                "EVALUATED_MISSING_OR_CONFLICTING_AUTHORITY / COVERAGE_LIMITED."
            ),
        }
        result["one_narrow_fix"] = {
            "not_applied": True,
            "first_discrepancy": (
                "In pre553_discovery_exact._terminal_fact_class, test "
                "UNRESOLVED before UNAVAILABLE and return UNRESOLVED; in "
                "_evaluate_candidate return EVALUATED_UNRESOLVED / UNRESOLVED; "
                "add EVALUATED_UNRESOLVED to TERMINAL_COVERAGE_STATES."
            ),
            "batch_prior_cache": (
                "In execute_saved_batch, require exact prior native outputs and "
                "validate every completed prior receipt with the existing "
                "_validate_prior_cache; reject otherwise. Do not trust "
                "result_refs from a prior receipt alone."
            ),
        }
        return_code = 0
    except Exception:
        result["status"] = "TRACE_EXCEPTION"
        result["exception"] = traceback.format_exc()
        return_code = 1
    finally:
        monkeypatch.undo()
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps({
        "status": result.get("status"),
        "out": str(OUT),
        "first_discrepancy": result.get("first_discrepancy"),
        "batch_prior_receipt_reuse": result.get("batch_prior_receipt_reuse"),
    }, indent=2, sort_keys=True))
    return return_code


if __name__ == "__main__":
    raise SystemExit(main())
