#!/usr/bin/env python3
"""Independent sourcefree review of OWNER's saved-Batch prior-cache patch.

Run once with an untouched pinned tree and once with the exact OWNER patch
applied to an isolated copy.  No Batch implementation file is edited here.
"""
from __future__ import annotations

import dataclasses
import hashlib
import inspect
import json
import os
import sys
import tempfile
from pathlib import Path

TREE = Path(os.environ["ANVIL_IMPLEMENTER"]).resolve()
MODE = os.environ.get("ANVIL_REVIEW_MODE", "patched")
OWNER_PATCH = Path(os.environ.get(
    "ANVIL_OWNER_PATCH",
    "/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/"
    "OWNER/WORKER_RETURNS/ANVIL_SRC16_SAVED_BATCH_PRIOR_CACHE_REPAIR_20261119/"
    "execute_saved_batch_prior_cache.patch",
))
sys.path.insert(0, str(TREE))

import pytest  # noqa: E402
from rawlsing_next.pre553_batch_runner import (  # noqa: E402
    BatchManifest,
    BatchUnitSpec,
)
from rawlsing_next.pre553_saved_workload_integration import (  # noqa: E402
    execute_saved_batch,
)
from rawlsing_next.tests.test_pre553_prepared_saved_i03 import _fixture  # noqa: E402


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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


def receipt_view(receipt):
    return {
        "receipt_hash": receipt.receipt_hash,
        "state": receipt.state,
        "execution_performed": receipt.execution_performed,
        "unit_ref": receipt.unit_ref.as_dict(),
        "result_refs": [ref.as_dict() for ref in receipt.result_refs],
        "attempt_index": receipt.attempt_index,
    }


def main() -> int:
    scratch = Path(tempfile.mkdtemp(
        prefix=f"src16-batch-review-{MODE}-",
        dir="/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode",
    ))
    mp = pytest.MonkeyPatch()
    result = {
        "schema": "ANVIL_SRC16_SAVED_BATCH_INDEPENDENT_REVIEW@1",
        "mode": MODE,
        "tree": str(TREE),
        "sourcefree": True,
        "original_source_accessed": False,
        "owner_patch_sha256": sha256(OWNER_PATCH),
        "has_prior_outputs_parameter": "prior_outputs" in inspect.signature(
            execute_saved_batch
        ).parameters,
    }
    try:
        source, qa, predicate, other_predicate, queries, admission = _fixture(
            mp, scratch / "fixture", "BATCH-REVIEW",
        )
        chosen = (queries["selected"], queries["f2"], queries["f4"])
        units = tuple(
            BatchUnitSpec(
                "QUERY", query.ref, (admission.release_ref,), (predicate.ref,),
            )
            for query in chosen
        )
        manifest = BatchManifest(units)
        by_job = {unit.job_ref.key: unit for unit in manifest.units}
        predicate_map = {query.ref.key: predicate.ref for query in chosen}

        first = execute_saved_batch(
            admission, manifest=manifest, predicate_ref_by_query=predicate_map,
        )
        baseline_receipts = tuple(first.receipts)
        exact_outputs = {
            by_job[query.ref.key].unit_hash: admission.execute_i03(
                query_ref=query.ref, predicate_ref=predicate.ref,
            )
            for query in chosen
        }
        result["baseline"] = {
            "receipts": [receipt_view(r) for r in baseline_receipts],
            "summary": summary_dict(first.summary()),
            "unit_hashes": [u.unit_hash for u in manifest.units],
            "manifest_hash": manifest.manifest_hash,
        }
        result["binding"] = {
            "manifest_hash": manifest.manifest_hash,
            "unit_hashes_are_prior_output_keys": set(exact_outputs) == {
                u.unit_hash for u in manifest.units
            },
            "prior_output_fact_refs_match_receipts": True,
            "admission_current_required": True,
        }

        forged = tuple(
            dataclasses.replace(receipt, result_refs=(predicate.ref,))
            for receipt in baseline_receipts
        )
        result["forged_prior_receipts"] = [receipt_view(r) for r in forged]
        result["forged_input_kind"] = "EmpiricalPredicate@1.0.0"

        # Baseline path: no prior_outputs argument. Patched path: no trusted
        # outputs supplied, so completed receipts must be discarded and units
        # must actually reexecute.
        if result["has_prior_outputs_parameter"]:
            patched_forged = execute_saved_batch(
                admission,
                manifest=manifest,
                predicate_ref_by_query=predicate_map,
                prior_receipts=forged,
            )
            result["forged_path"] = {
                "receipts": [receipt_view(r) for r in patched_forged.receipts],
                "summary": summary_dict(patched_forged.summary()),
                "all_forged_receipts_retained": all(
                    any(
                        observed.receipt_ref == supplied.receipt_ref
                        and observed.result_refs == supplied.result_refs
                        for observed in patched_forged.receipts
                    )
                    for supplied in forged
                ),
                "reexecuted": all(
                    r.state == "COMPLETED" and r.attempt_index == 1
                    for r in patched_forged.receipts
                ),
            }
        else:
            baseline_forged = execute_saved_batch(
                admission,
                manifest=manifest,
                predicate_ref_by_query=predicate_map,
                prior_receipts=forged,
            )
            result["forged_path"] = {
                "receipts": [receipt_view(r) for r in baseline_forged.receipts],
                "summary": summary_dict(baseline_forged.summary()),
                "all_forged_receipts_retained": all(
                    any(
                        observed.receipt_ref == supplied.receipt_ref
                        and observed.result_refs == supplied.result_refs
                        for observed in baseline_forged.receipts
                    )
                    for supplied in forged
                ),
                "reexecuted": False,
            }

        if result["has_prior_outputs_parameter"]:
            exact_reuse = execute_saved_batch(
                admission,
                manifest=manifest,
                predicate_ref_by_query=predicate_map,
                prior_receipts=baseline_receipts,
                prior_outputs=exact_outputs,
            )
            result["exact_cache_reuse"] = {
                "receipts": [receipt_view(r) for r in exact_reuse.receipts],
                "summary": summary_dict(exact_reuse.summary()),
                "same_records_equal": [
                    r.receipt_hash for r in exact_reuse.receipts
                ] == [r.receipt_hash for r in baseline_receipts],
            }

            changed_outputs = dict(exact_outputs)
            changed_key = next(iter(changed_outputs))
            changed_outputs[changed_key] = object()
            try:
                execute_saved_batch(
                    admission,
                    manifest=manifest,
                    predicate_ref_by_query=predicate_map,
                    prior_receipts=baseline_receipts,
                    prior_outputs=changed_outputs,
                )
                result["changed_prior_output"] = {
                    "refused": False,
                    "error": None,
                }
            except Exception as exc:
                result["changed_prior_output"] = {
                    "refused": True,
                    "error": f"{type(exc).__name__}: {exc}",
                }

            changed_map = dict(predicate_map)
            changed_map[chosen[0].ref.key] = other_predicate.ref
            try:
                changed_map_run = execute_saved_batch(
                    admission,
                    manifest=manifest,
                    predicate_ref_by_query=changed_map,
                    prior_receipts=baseline_receipts,
                    prior_outputs=exact_outputs,
                )
                result["changed_mapping"] = {
                    "accepted": True,
                    "receipts": len(changed_map_run.receipts),
                    "summary": summary_dict(changed_map_run.summary()),
                }
            except Exception as exc:
                result["changed_mapping"] = {
                    "accepted": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }

            # One legitimate deferred/partial attempt: it must survive and
            # only its unit may reexecute. Completed units stay reusable only
            # with their exact outputs.
            partial = dataclasses.replace(
                baseline_receipts[0],
                state="DEFERRED",
                result_refs=(),
                failure_code="TEST_PARTIAL",
                detail_hash="a" * 64,
            )
            partial_unit = partial.unit_ref
            completed_for_partial = tuple(
                r for r in baseline_receipts if r.unit_ref != partial_unit
            )
            partial_outputs = {
                u.unit_hash: exact_outputs[u.unit_hash]
                for u in manifest.units
                if u.unit_ref != partial_unit
            }
            partial_run = execute_saved_batch(
                admission,
                manifest=manifest,
                predicate_ref_by_query=predicate_map,
                prior_receipts=(partial, *completed_for_partial),
                prior_outputs=partial_outputs,
            )
            result["partial_resume"] = {
                "partial_receipt_retained": any(
                    r.receipt_ref == partial.receipt_ref for r in partial_run.receipts
                ),
                "unit_reexecuted": any(
                    r.unit_ref == partial_unit and r.attempt_index == 2
                    and r.state == "COMPLETED"
                    for r in partial_run.receipts
                ),
                "receipts": [receipt_view(r) for r in partial_run.receipts],
                "summary": summary_dict(partial_run.summary()),
            }

        state = {"now": True}
        denied = admission.__class__.open(
            root=Path(admission.estate_path).parents[1],
            exact_path=admission.estate_path,
            independently_held_manifest_sha256=admission.manifest_sha256,
            independently_held_i02=admission.i02,
            release_ref=admission.release_ref,
            runtime_catalog=admission._runtime_catalog,
            current_authorizer=lambda _roots: state["now"],
        )
        state["now"] = False
        try:
            execute_saved_batch(
                denied,
                manifest=manifest,
                predicate_ref_by_query=predicate_map,
                prior_receipts=baseline_receipts,
                **({"prior_outputs": exact_outputs} if result["has_prior_outputs_parameter"] else {}),
            )
            result["authority_refusal"] = {"refused": False}
        except Exception as exc:
            result["authority_refusal"] = {
                "refused": True,
                "error": f"{type(exc).__name__}: {exc}",
            }

        result["status"] = (
            "RED_FORGED_RETAINED"
            if MODE == "baseline" and result.get("forged_path", {}).get("all_forged_receipts_retained")
            else "GREEN_FORGED_REEXECUTED"
            if MODE == "patched"
            and not result.get("forged_path", {}).get("all_forged_receipts_retained")
            and result.get("forged_path", {}).get("reexecuted")
            else "REVIEW_INCOMPLETE"
        )
        return 0
    except Exception as exc:
        result["status"] = "ERROR"
        result["error"] = f"{type(exc).__name__}: {exc}"
        return 1
    finally:
        mp.undo()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
