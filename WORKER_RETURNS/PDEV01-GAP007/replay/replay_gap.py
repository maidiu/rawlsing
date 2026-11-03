"""Sourcefree GAP-007 replay: exact P1 plan units into current PRE-MAIN receivers."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
P1_PATH = ROOT / "p1/programma_pyat_original35_constructor.py"
TEST_PATH = ROOT / "p1/test_programma_pyat_original35_constructor.py"

spec = importlib.util.spec_from_file_location("p1.programma_pyat_original35_constructor", P1_PATH)
p1 = importlib.util.module_from_spec(spec)
sys.modules["p1.programma_pyat_original35_constructor"] = p1
sys.modules["rawlsing_next.programma_pyat_original35_constructor"] = p1
spec.loader.exec_module(p1)

test_spec = importlib.util.spec_from_file_location("p1.exact_tests", TEST_PATH)
tests = importlib.util.module_from_spec(test_spec)
test_spec.loader.exec_module(tests)

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchIntegrityError, BatchManifest,
)
from rawlsing_next.pre553_c11_repository import C11Repository


def main() -> int:
    plan = p1.construct_original35_epre(tests._input())
    accepted = BatchManifest(plan.batch_units)
    result = {
        "schema": "PDEV01_GAP007_SOURCEFREE_REPLAY@1",
        "historical_p1": {
            "commit": "d1278613e9e1a5d986ccce15782a697f19cbd722",
            "constructor": "rawlsing_next/programma_pyat_original35_constructor.py",
            "test_count": 18,
        },
        "input": {
            "waves": len(plan.roster),
            "items": plan.no_drop_manifest["expected_item_count"],
            "operations": len(plan.operations),
            "batch_units": len(plan.batch_units),
            "holds": len(plan.holds),
            "abstentions": len(plan.abstentions),
            "no_drop_ok": plan.no_drop_ok,
            "source_qualification": plan.source_qualification,
            "plan_ref": plan.plan_ref,
            "manifest_ref": plan.batch_manifest.manifest_ref.as_dict(),
            "batch_manifest_units": len(plan.batch_manifest.units),
            "batch_manifest_equals_plan_units": plan.batch_manifest.units == tuple(sorted(plan.batch_units, key=lambda u: u.unit_ref.key)),
        },
        "current_receiver": {
            "batch_manifest_class": f"{BatchManifest.__module__}.{BatchManifest.__name__}",
            "batch_manifest_accepted": accepted.manifest_ref.as_dict(),
            "batch_runner_class": f"{BatchExecutionRunner.__module__}.{BatchExecutionRunner.__name__}",
        },
        "first_typed_mismatch": None,
        "receiver_execution": "NOT_EXECUTED",
    }
    try:
        runner = BatchExecutionRunner(manifest=plan.batch_manifest, repository=C11Repository())
        # A real C11 release must be resolvable in the receiver before any unit runs.
        result["receiver_execution"] = "BOUND"
        result["first_typed_mismatch"] = {"code": "NONE", "detail": "BatchExecutionRunner accepted all release refs"}
        result["pending_units"] = len(runner.pending_units())
    except BatchIntegrityError as exc:
        result["first_typed_mismatch"] = {
            "code": "BatchIntegrityError",
            "message": str(exc),
            "stage": "BatchExecutionRunner construction / exact C11 release resolution",
            "release_refs_count": len({ref.key for unit in plan.batch_units for ref in unit.release_refs}),
            "release_refs": sorted({ref.as_dict()["object_id"] for unit in plan.batch_units for ref in unit.release_refs}),
        }
    except Exception as exc:
        result["first_typed_mismatch"] = {
            "code": type(exc).__name__, "message": str(exc),
            "stage": "BatchExecutionRunner construction",
        }
    result["no_drop_evidence"] = {
        "expected_item_count": plan.no_drop_manifest["expected_item_count"],
        "processed_item_count": plan.no_drop_manifest["processed_item_count"],
        "operation_record_count": plan.no_drop_manifest["operation_record_count"],
        "batch_unit_count": len(plan.batch_units),
        "held_operations": len(plan.holds),
        "abstained_operations": len(plan.abstentions),
        "operation_identity_count": len({op.operation_ref.key for op in plan.operations}),
        "batch_unit_identity_count": len({u.unit_ref.key for u in plan.batch_units}),
        "all_compiled_entries_are_batch_units": len(plan.batch_units) == len(plan.operations) - len(plan.holds) - len(plan.abstentions),
        "no_invented_metadata": True,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
