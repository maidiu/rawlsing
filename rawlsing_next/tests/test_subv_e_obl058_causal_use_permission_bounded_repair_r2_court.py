"""Governed-court wrapper for OBL058 R2 bounded repair verification.

This wrapper exposes the producer-side repair court only. It is not an
independent review of the frozen repaired candidate.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL058_CAUSAL_USE_PERMISSION_R1/test_bounded_repair_r2.py"

spec = importlib.util.spec_from_file_location("_obl058_bounded_repair_r2_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL058 R2 bounded repair court: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL058BoundedRepairR2Court(module.OBL058BoundedRepairR2Court):
    """Expose the lane-local producer repair TestCase to governed pytest."""

    pass
