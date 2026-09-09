"""Governed-court wrapper for OBL058 R12 authority-client boundary.

Producer-side verification only. This wrapper does not perform or substitute for
the required fresh distinct independent review of the frozen R12 candidate.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
LANE = ROOT / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/E_V3_FIRST_POSITIVE_SOURCE_AUTHORITY_R1/OBL058_CAUSAL_USE_PERMISSION_R1"
if str(LANE) not in sys.path:
    sys.path.insert(0, str(LANE))

from test_authority_client_boundary_r12 import OBL058AuthorityClientBoundaryR12Court as _Court  # noqa: E402


class TestOBL058AuthorityClientBoundaryR12Court(_Court):
    pass
