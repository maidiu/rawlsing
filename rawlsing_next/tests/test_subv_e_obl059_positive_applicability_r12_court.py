"""Governed-court wrapper for frozen OBL059 R12 semantic-view redesign."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R12/governed_bounded_court_r12.py"

spec = importlib.util.spec_from_file_location("_obl059_r12_semantic_view_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL059 R12 court: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL059R12SemanticViewRedesign(module.CourtR12):
    def test_131_unrelated_error_after_successful_preparation_remains_visible(self):
        """Route inherited R10 visibility check to R12's actual evaluator delegate."""
        original = module.r12._r11._r10._r9._evaluate_prepared
        packet = module.fixture()
        packet["opportunity"] = module.r11_court.r10_wrapper.module.MutableCarrier(
            copy.deepcopy(packet["opportunity"])
        )
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r10-post-preparation-programmer-error")
                module.r12._r11._r10._r9._evaluate_prepared = deliberate
                with self.assertRaisesRegex(exc_type, "r10-post-preparation-programmer-error"):
                    module.r12.evaluate_direct_positive_applicability(packet)
        finally:
            module.r12._r11._r10._r9._evaluate_prepared = original

    def test_140_parent_slot_change_from_composed_validation_is_child_local_and_negative(self):
        """R12 semantic authority ignores child-local private-state change itself."""
        packet = module.fixture()
        original_actor = packet["evidence"]["actor_activation"]
        composed = module.r11_court.CallbackLayered(
            copy.deepcopy(packet["opportunity"]),
            {},
            callback=lambda: packet["evidence"].__setitem__("actor_activation", None),
        )
        packet["opportunity"] = composed
        result = module.r12.evaluate_direct_positive_applicability(packet)
        self.assertEqual(result["decision"], module.r12.POSITIVE_DECISION, result)
        self.assertIs(packet["evidence"]["actor_activation"], original_actor)
        self.assert_no_effect_r12(result)

    def test_145_unrelated_errors_after_composed_view_established_remain_visible(self):
        """Route inherited R11 visibility check to R12's actual evaluator delegate."""
        original = module.r12._r11._r10._r9._evaluate_prepared
        packet = module.fixture()
        packet["opportunity"] = module.ChainMap(copy.deepcopy(packet["opportunity"]), {})
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r11-post-view-programmer-error")
                module.r12._r11._r10._r9._evaluate_prepared = deliberate
                with self.assertRaisesRegex(exc_type, "r11-post-view-programmer-error"):
                    module.r12.evaluate_direct_positive_applicability(packet)
        finally:
            module.r12._r11._r10._r9._evaluate_prepared = original
