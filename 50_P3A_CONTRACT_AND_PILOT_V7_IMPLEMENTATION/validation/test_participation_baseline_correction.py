from __future__ import annotations

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1].parents[0]
SEC49 = ROOT / "49_P3_PLAN_SIXTH_EXECUTABLE_CLOSURE_AUDIT_AND_LOCK"


def test_participation_baseline_agrees_with_signature_workset():
    baseline = pd.read_csv(
        SEC49 / "upstream/P3_LINEAGE_PARTICIPATION_BASELINE_v7.csv",
        keep_default_na=False,
    )
    workset = pd.read_csv(
        SEC49 / "upstream/P3_SIGNATURE_WORKSET_v7.csv",
        keep_default_na=False,
    )
    merged = baseline.merge(
        workset[["lineage_id", "participation_status", "signature_requirement"]],
        on="lineage_id",
        how="outer",
        suffixes=("_baseline", "_workset"),
        indicator=True,
    )

    assert len(baseline) == 13526
    assert len(workset) == 13526
    assert baseline["lineage_id"].nunique() == 13526
    assert workset["lineage_id"].nunique() == 13526
    assert (merged["_merge"] == "both").all()
    assert (
        merged["participation_status_baseline"]
        == merged["participation_status_workset"]
    ).all()
    assert (
        merged["signature_requirement_baseline"]
        == merged["signature_requirement_workset"]
    ).all()

    counts = baseline["signature_requirement"].value_counts().to_dict()
    assert counts == {
        "DEFER_UNTIL_PROMOTED_OR_NEW_AUTHORITY": 10230,
        "P2_CONSTRAINT_EVIDENCE_PRESERVED": 2897,
        "FULL_P3A_SIGNATURE": 399,
    }
