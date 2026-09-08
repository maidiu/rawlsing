"""Governed wrapper for the fresh OBL058 R6 independent review.

This wrapper exposes only the reviewer-authored R6 review court. It does not
modify or repair the frozen semantic candidate.
"""
from __future__ import annotations

import gc
import importlib.util
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET_DIR = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL058_CAUSAL_USE_PERMISSION_R1"
TARGET = TARGET_DIR / "test_independent_review_r6.py"
if str(TARGET_DIR) not in sys.path:
    sys.path.insert(0, str(TARGET_DIR))

spec = importlib.util.spec_from_file_location("_obl058_r6_independent_review_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL058 R6 independent review: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL058R6IndependentReview(module.OBL058R6IndependentReview):
    def test_b01_detached_finalizer_leaves_stale_record_for_later_exact_type_generation(self):
        """Prove stale authority deterministically; allocator reuse is not required."""
        original = module.issue_noncurrent_synthetic_receipt(
            scope=module.REGISTERED_POSITIVE_SCOPE,
            basis_id=module.REGISTERED_POSITIVE_BASIS_ID,
        )
        old_id = id(original)
        body_json = object.__getattribute__(original, "_body_json")
        fin = module._find_receipt_finalizer(original)
        detached = fin.detach()
        self.assertIsNotNone(detached)
        del detached
        del fin
        del original
        gc.collect()

        try:
            response = module.candidate._bound_broker_request({
                "op": "validate",
                "object_id": old_id,
                "body_json": body_json,
                "expected_scope": module.REGISTERED_POSITIVE_SCOPE.canonical(),
                "request_id": uuid.uuid4().hex,
            })
            self.assertEqual(module.DECISION_PERMIT, response.get("decision"))
        finally:
            module.candidate._bound_broker_request({
                "op": "close",
                "object_id": old_id,
                "request_id": uuid.uuid4().hex,
            })
