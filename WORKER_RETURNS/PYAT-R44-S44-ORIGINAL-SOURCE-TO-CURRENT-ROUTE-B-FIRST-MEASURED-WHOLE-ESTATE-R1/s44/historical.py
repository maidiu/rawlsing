"""S44 historical original-source positive verification (historical scope only).

The AS2B LiTS-I certification is genuine historical measured original-source
science. It does NOT authorize a current host, purpose, fresh selected-B read,
or original-estate occupancy. WVS7 has authoritative method precedent but no
executed fact receipt in the inspected commit, so it is recorded as precedent
only, never as a positive.
"""
from __future__ import annotations

import csv
import io
import json
import sys
from pathlib import Path

RETURN_ROOT = Path(__file__).resolve().parent.parent
if str(RETURN_ROOT) not in sys.path:
    sys.path.insert(0, str(RETURN_ROOT))
from frozen_a42.frozen_a41.a41.gitpreimage import GitPreimage  # noqa: E402

AS2B_COMMIT = "923f2c00b6145182a5e2be5038f579845951da19"
AS2B_DIR = ("data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/"
            "SUBSTRATE_RECONSTRUCTION/AS2B_LITS1_MECHANICAL_SOURCE_CERTIFICATION_20260827")
AS2B_PATHS = {
    "final_return": AS2B_DIR + "/09_FINAL_AS2B_RETURN.md",
    "i03_csv": AS2B_DIR + "/06_I03_CERTIFICATION_RECEIPT.csv",
    "projection": AS2B_DIR + "/02_GOVERNED_C11_PROJECTION_RECEIPT.json",
    "candidate_release": AS2B_DIR + "/03_C11_CANDIDATE_RELEASE_REPOSITORY_RECEIPT.json",
    "replay_manifest": AS2B_DIR + "/04_REPLAY_MANIFEST_AND_DETERMINISM_RECEIPT.json",
    "residual_blocker": AS2B_DIR + "/08_RESIDUAL_BLOCKER_LEDGER.csv",
}
GRADE = "HISTORICAL_SCOPE_POSITIVE"
LITS_WAVE = "SRC27"


def verify_historical(gp: GitPreimage) -> dict:
    records = {}
    for key, path in AS2B_PATHS.items():
        records[key] = gp.verify(AS2B_COMMIT, path)
    raw_csv = gp.blob_at(AS2B_COMMIT, AS2B_PATHS["i03_csv"]).decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(raw_csv)))
    executed = [r for r in rows if r.get("execution") == "EXECUTED"]
    supported = [r for r in executed if r.get("result_state") == "SUPPORTED"]
    typed_nonpositive = [r for r in executed if r.get("result_state") != "SUPPORTED"]
    return {
        "schema": "S44_HISTORICAL_SOURCE_POSITIVES@1",
        "grade": GRADE,
        "current_grant": False,
        "occupies_original_measured_cells": False,
        "as2b": {
            "commit": AS2B_COMMIT,
            "wave": LITS_WAVE,
            "source": "LiTS-I",
            "source_sha256": "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09",
            "historical_host": "Trii live HEAD 04a0109aa170c6041b199e5c6130a39a8e0f6029",
            "respondent_count": 29002,
            "event_count": 58004,
            "routing_fact_count": 58004,
            "coordinate_fact_count": 145010,
            "weight_fact_count": 0,
            "i03_executed": len(executed),
            "i03_supported": len(supported),
            "i03_typed_nonpositive": len(typed_nonpositive),
            "supported_fact": {
                "operation": supported[0]["operation"],
                "empirical_fact_hash": supported[0]["empirical_fact_hash"],
                "raw_numerator_support": int(supported[0]["raw_numerator_support"]),
                "raw_denominator_support": int(supported[0]["raw_denominator_support"]),
            } if supported else None,
            "verified_artifacts": records,
            "reused_at": "HISTORICAL_SCOPE_ONLY",
            "does_not_authorize": ["current host", "current purpose", "fresh raw read",
                                   "current selected B", "original35 occupancy"],
        },
        "wvs7": {
            "state": "HISTORICAL_AUTHORITY_PRECEDENT_ONLY__NO_EXECUTED_FACT_RECEIPT_IN_INSPECTED_COMMIT",
            "counts_as_positive": False,
        },
        "raw_source_access_this_pass": "NOT_GRANTED__NO_RAW_SAV_DTA_OPENED",
    }


def a42_historical_receipt(historical: dict) -> dict:
    a = historical["as2b"]
    return {
        "receipt_id": "S44-AS2B-LITS-I-HISTORICAL",
        "origin_commit": AS2B_COMMIT,
        "claim_id": "S44_AS2B_LITS_I_HISTORICAL_ORIGINAL_SOURCE_POSITIVE",
        "grade": historical["grade"],
        "coverage": {
            "wave_ids": [LITS_WAVE],
            "axis_ids": ["S19", "S21"],
            "f_gate_ids": [],
            "functional_gates": [],
            "register_151_ids": [],
            "ledger_101_ids": [],
            "global_relations": [],
            "global_contributions": [],
            "occupancy_grain_note": ("historical AS2B LiTS-I measured source positive; "
                                     "NOT current selected B, NOT original measured occupancy"),
        },
        "unknown_bounds": {"current_grant": False, "respondent_count": a["respondent_count"],
                           "supported_fact": a["supported_fact"]},
        "currentness": {"archive_or_current": "ARCHIVE", "as_of": "2026-08-27T00:00:00+0000"},
    }
