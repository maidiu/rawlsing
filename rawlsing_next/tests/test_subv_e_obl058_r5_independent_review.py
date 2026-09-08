"""Governed wrapper for the fresh OBL058 R5 independent review.

This wrapper exposes the independently authored lane-local review court to the
bounded-court protocol. It does not modify the frozen semantic candidate.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL058_CAUSAL_USE_PERMISSION_R1/test_independent_review_r5.py"

spec = importlib.util.spec_from_file_location("_obl058_r5_independent_review_lane", TARGET)
if spec is None or spec.loader is None:
    raise RuntimeError(f"cannot load OBL058 R5 independent review: {TARGET}")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class TestOBL058R5IndependentReview(module.OBL058R5IndependentReview):
    """Expose the lane-local independent review TestCase to governed pytest."""

    pass
