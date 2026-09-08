"""Governed-court wrapper for OBL058 R4 bounded repair verification.

Producer-side repair court only. This wrapper does not perform or substitute for
the required fresh distinct independent review of the frozen R4 candidate.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL058_CAUSAL_USE_PERMISSION_R1/test_bounded_repair_r4.py"

spec = importlib.util.spec_from_file_location("_obl058_bounded_repair_r4_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL058 R4 bounded repair court: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL058BoundedRepairR4Court(module.OBL058BoundedRepairR4Court):
    """Expose the lane-local producer repair TestCase to governed pytest."""

    pass
