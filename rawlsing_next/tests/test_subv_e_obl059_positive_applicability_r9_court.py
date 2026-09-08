"""Governed-court wrapper for frozen OBL059 R9 bounded repair."""
from __future__ import annotations

import importlib.util
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R9/governed_bounded_court_r9.py"

spec = importlib.util.spec_from_file_location("_obl059_r9_bounded_repair_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL059 R9 court: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL059R9BoundedRepair(module.CourtR9):
    def test_70_reproduced_zero_to_minimum_barrier_remains_total(self):
        """Keep the inherited R6 barrier bound to frozen R7 -> R6."""
        huge = 10 ** 5000
        packet = module.fixture()
        packet["actor_id"] = huge
        r7 = module.r9._r7
        original_requires = r7._r6._requires_total_projection_stable
        original_limit = sys.get_int_max_str_digits()
        entered = threading.Event()
        release = threading.Event()
        state = {}

        def gated_requires(candidate_packet, reason):
            decision = original_requires(candidate_packet, reason)
            state["classification_result"] = decision
            entered.set()
            if not release.wait(timeout=10):
                raise RuntimeError("r9 inherited barrier timeout")
            return decision

        def run_candidate():
            try:
                state["result"] = r7.evaluate_direct_positive_applicability(packet)
            except Exception as exc:
                state["exception"] = exc

        try:
            sys.set_int_max_str_digits(0)
            r7._r6._requires_total_projection_stable = gated_requires
            worker = threading.Thread(target=run_candidate, daemon=True)
            worker.start()
            self.assertTrue(entered.wait(timeout=10), "inherited barrier not reached")
            self.assertTrue(state.get("classification_result"))
            sys.set_int_max_str_digits(int(sys.int_info.str_digits_check_threshold))
            release.set()
            worker.join(timeout=10)
            self.assertFalse(worker.is_alive(), "inherited barrier worker did not finish")
            if "exception" in state:
                raise state["exception"]
            result = state["result"]
            self.assertEqual(result["decision"], module.r9.NEGATIVE_DECISION, result)
            self.assertEqual(result["reason"], "MALFORMED_BINDING:actor_id", result)
        finally:
            release.set()
            r7._r6._requires_total_projection_stable = original_requires
            sys.set_int_max_str_digits(original_limit)

    def test_90_r7_revision_identity_is_exact(self):
        """Keep the inherited R7 identity assertion bound to frozen R7."""
        self.assertEqual(
            module.r9._r7.R7_CANDIDATE_REVISION,
            "OBL059_POSITIVE_APPLICABILITY_BOUNDED_REPAIR_R7",
        )
