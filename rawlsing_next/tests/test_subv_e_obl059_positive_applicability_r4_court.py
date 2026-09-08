"""Governed-court wrapper for frozen OBL059 R4 bounded repair."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R4/governed_bounded_court_r4.py"

spec = importlib.util.spec_from_file_location("_obl059_r4_bounded_repair_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL059 R4 court: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL059R4BoundedRepair(module.CourtR4):
    def test_43_unrelated_programmer_errors_are_not_masked(self):
        """Route the inherited R3 preservation check to R4's actual R3 module."""
        original = module.r4._r3.evaluate_direct_positive_applicability

        def raise_type_error(_packet):
            raise TypeError("deliberate-programmer-error")

        def raise_value_error(_packet):
            raise ValueError("deliberate-programmer-error")

        try:
            module.r4._r3.evaluate_direct_positive_applicability = raise_type_error
            with self.assertRaisesRegex(TypeError, "deliberate-programmer-error"):
                module.r4.evaluate_direct_positive_applicability(module.fixture())

            module.r4._r3.evaluate_direct_positive_applicability = raise_value_error
            with self.assertRaisesRegex(ValueError, "deliberate-programmer-error"):
                module.r4.evaluate_direct_positive_applicability(module.fixture())
        finally:
            module.r4._r3.evaluate_direct_positive_applicability = original
