"""B43 independently frozen all35 expected-vs-executed source frontier.

The frontier is frozen from the declared estate matrix and the WG0P4 fixture
frontier, BEFORE any execution result. It never derives expectations from an
observed output. U43's prospective per-wave operation frontier has not returned,
so every wave's expected operation count is null WITH CAUSE (not zero).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

RETURN_ROOT = Path(__file__).resolve().parent.parent
if str(RETURN_ROOT) not in sys.path:
    sys.path.insert(0, str(RETURN_ROOT))
from frozen_a42.frozen_a41.a41.gitpreimage import GitPreimage  # noqa: E402

STARTUP = "556dd7e2bf67e2bc0b1772d18880ef0dfaa819e3"
WG0P4_COMMIT = "20d781c8502662bf788b60b828e46df55898d687"
WG0P4_DIR = "WORKER_RETURNS/PYAT-USERDIRECT-20261015-R9-WG0P4-EXACT-FRONTIER-COLD-REPAIR-R1"
ESTATE_MATRIX = "PYAT_CONTROL_ROOM/WHOLE_MACHINE_COMPLETION_R1/ESTATE_35X_REQUIREMENTS_MATRIX.json"
ESTATE_BLOB = "2ad9a001aefef4889d8ac48a2a81cd806dec50d6"
FRONTIER_BLOB = "b974c1bf94f81fcafe7120b921e4ac19686eece5"  # blob at WG0P4 return
FIXTURE_FRONTIER_SCHEMA = "WG0P4_ORIGINAL_25_FIXTURE_FRONTIER@1"


def _load(gp: GitPreimage, commit: str, path: str, blob: str | None = None):
    rec = gp.verify(commit, path, expect_blob_sha1=blob)
    return json.loads(gp.blob_at(commit, path)), rec


def load_frontier(gp: GitPreimage) -> dict:
    estate, estate_rec = _load(gp, STARTUP, ESTATE_MATRIX, ESTATE_BLOB)
    orig, orig_rec = _load(gp, WG0P4_COMMIT, WG0P4_DIR + "/ORIGINAL_FRONTIER.json", FRONTIER_BLOB)
    cond, cond_rec = _load(gp, WG0P4_COMMIT, WG0P4_DIR + "/CONDITIONAL_FRONTIER.json")

    waves = []
    for s in estate["sources"]:
        waves.append({
            "source_id": s["id"],
            "source_name": s["name"],
            "execution_eligibility": "PENDING_COMPETENT_SOURCE_HOST_PURPOSE_AND_U_E_PRE",
            "raw_source_permitted": False,
            "grant_ref": None,
            "u43_prospective_operation_frontier": None,
            "u43_frontier_reason": "U43 has not returned a qualified prospective frontier",
            "expected_original_operations": None,
            "expected_original_operations_reason": ("null with cause: prospective original "
                                                    "operation issuer has not issued"),
            "executed_original_operations": 0,
            "measured_occupancy": 0,
        })
    counts = orig.get("expected_counts") or {}
    fixture = {
        "schema": FIXTURE_FRONTIER_SCHEMA,
        "grade": "SOURCEFREE_FIXTURE_METHOD_PROOF__NOT_ORIGINAL",
        "origin_commit": WG0P4_COMMIT,
        "origin_blob": orig_rec["blob_sha1"],
        "conditional_origin_blob": cond_rec["blob_sha1"],
        "native_item_count": len(orig.get("native_items") or []),
        "produced": counts.get("PRODUCED"),
        "held": counts.get("HELD"),
        "inadmissible": counts.get("INADMISSIBLE"),
        "rights_ceiling": orig.get("rights_ceiling"),
        "counts_toward_original_occupancy": False,
    }
    return {
        "schema": "B43_ALL35_SOURCE_EXECUTION_FRONTIER@1",
        "startup": STARTUP,
        "estate_matrix_blob": estate_rec["blob_sha1"],
        "wave_count": len(waves),
        "waves": waves,
        "fixture_frontier": fixture,
        "executed_original_operations_total": 0,
        "expected_original_operations_total": None,
        "expected_original_operations_total_reason": (
            "null with cause: U43 prospective frontier and competent U/E_pre issuance absent"),
        "original_source_grant_present": False,
        "frozen_before_execution": True,
    }


def decision_docket(frontier: dict) -> dict:
    rows = []
    for w in frontier["waves"]:
        rows.append({
            "source_id": w["source_id"], "source_name": w["source_name"],
            "required_competent_decisions": [
                "source-specific source+host+purpose permission",
                "current source edition / native item / release identity (issuer-bound)",
                "prospective U/E_pre operation eligibility for this wave",
                "risk/weight/denominator/estimand and population routing",
                "consumer purpose (original E04 NONPARENT_OPTIONS or lawful generic)",
            ],
            "state": "PENDING_COMPETENT_OWNER",
            "blocks": "RAW_SOURCE_READ_AND_ORIGINAL_MEASURED_OCCUPANCY",
        })
    return {
        "schema": "B43_SOURCE_OWNER_DECISION_DOCKET@1",
        "wave_count": len(rows),
        "global_prerequisites": [
            "LiTS C11 custodian preimages OR exact reconstruction warrant",
            "U43 qualified prospective frontier",
            "competent original35 source/operation/U/E_pre issuer grant",
        ],
        "rows": rows,
    }
