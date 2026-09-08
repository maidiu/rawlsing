"""Governed-court wrapper for OBL058 R4 fresh independent review."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL058_CAUSAL_USE_PERMISSION_R1/test_independent_review_r4.py"

spec = importlib.util.spec_from_file_location("_obl058_r4_independent_review_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load independent review surface: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL058R4IndependentReview(module.OBL058R4IndependentReview):
    """Expose the reviewer matrix, correcting one discovery-only API assertion."""

    def test_s08_no_public_registration_or_current_effect_api(self):
        exported = set(dir(module.candidate))
        registration_callables = {
            name for name in exported
            if "register" in name.lower() and callable(getattr(module.candidate, name))
        }
        self.assertFalse(registration_callables)
        forbidden = {
            "execute_obl055", "create_encounter", "realize_oee",
            "install_current_positive_obl056", "unblock_obl061",
            "activate_current_actor", "create_current_actor",
        }
        self.assertTrue(forbidden.isdisjoint(exported))
