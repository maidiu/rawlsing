"""Governed-court wrapper for frozen OBL059 R11 bounded repair."""
from __future__ import annotations

import copy
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R11/governed_bounded_court_r11.py"

spec = importlib.util.spec_from_file_location("_obl059_r11_bounded_repair_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL059 R11 court: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL059R11BoundedRepair(module.CourtR11):
    def test_131_unrelated_error_after_successful_preparation_remains_visible(self):
        """Route inherited preservation check to R11's actual frozen delegate."""
        original = module.r11._r10._r9._evaluate_prepared
        packet = module.fixture()
        packet["opportunity"] = module.r10_wrapper.module.MutableCarrier(
            copy.deepcopy(packet["opportunity"])
        )
        try:
            for exc_type in (TypeError, ValueError, RuntimeError):
                def deliberate(_packet, exc_type=exc_type):
                    raise exc_type("r10-post-preparation-programmer-error")
                module.r11._r10._r9._evaluate_prepared = deliberate
                with self.assertRaisesRegex(exc_type, "r10-post-preparation-programmer-error"):
                    module.r11.evaluate_direct_positive_applicability(packet)
        finally:
            module.r11._r10._r9._evaluate_prepared = original
