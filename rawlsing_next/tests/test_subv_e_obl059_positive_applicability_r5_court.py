"""Pytest wrapper for the governed OBL059 R5 bounded-repair court."""

import importlib.util
from pathlib import Path

COURT_PATH = (
    Path(__file__).resolve().parents[2]
    / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R5/governed_bounded_court_r5.py"
)

spec = importlib.util.spec_from_file_location("_obl059_r5_governed_court", COURT_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load governed R5 court: {COURT_PATH}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL059R5BoundedRepair(module.CourtR5):
    def test_43_unrelated_programmer_errors_are_not_masked(self):
        """Route inherited R3 preservation check to R5's actual delegate chain."""
        original = module.r5._r4._r3._r2.evaluate_direct_positive_applicability

        def raise_type_error(_packet):
            raise TypeError("deliberate-programmer-error")

        def raise_value_error(_packet):
            raise ValueError("deliberate-programmer-error")

        try:
            module.r5._r4._r3._r2.evaluate_direct_positive_applicability = raise_type_error
            with self.assertRaisesRegex(TypeError, "deliberate-programmer-error"):
                module.r5.evaluate_direct_positive_applicability(module.fixture())

            module.r5._r4._r3._r2.evaluate_direct_positive_applicability = raise_value_error
            with self.assertRaisesRegex(ValueError, "deliberate-programmer-error"):
                module.r5.evaluate_direct_positive_applicability(module.fixture())
        finally:
            module.r5._r4._r3._r2.evaluate_direct_positive_applicability = original
