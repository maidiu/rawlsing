"""Governed-court wrapper for superseding OBL058 R12 authority-client candidate.

Producer-side verification only. This wrapper uses the corrected producer-court
surface after the first execution exposed only an exception-type expectation
mismatch. It performs no self-review and no independent review.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
LANE = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL058_CAUSAL_USE_PERMISSION_R1"
if str(LANE) not in sys.path:
    sys.path.insert(0, str(LANE))

from test_authority_client_boundary_r12_corrected import OBL058AuthorityClientBoundaryR12Court as _Court  # noqa: E402


class TestOBL058AuthorityClientBoundaryR12Court(_Court):
    pass
