"""Governed-court wrapper for the frozen OBL059 R2 bounded repair."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL059_POSITIVE_APPLICABILITY_R2/governed_bounded_court_r2.py"

spec = importlib.util.spec_from_file_location("_obl059_r2_bounded_repair_court", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL059 R2 governed court: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL059R2BoundedRepair(module.CourtR2):
    """Expose the R2 court to the governed pytest runner."""

    pass
