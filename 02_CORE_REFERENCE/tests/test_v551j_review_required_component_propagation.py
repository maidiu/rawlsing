from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_ROOT = ROOT / "outputs" / "v551j_review_required_component_repair_v1_20260730T071144Z"
REVIEW_SMOKE = OUTPUT_ROOT / "smoke_outputs_c" / "v551j_four_component_review_required_smoke_v1c"
NEUTRAL_SMOKE = OUTPUT_ROOT / "neutral_smoke_outputs" / "v551j_positive_negative_neutral_smoke_v1"


def _csv(run: Path, rel: str) -> pd.DataFrame:
    return pd.read_csv(run / rel, keep_default_na=False)


def _ready(run: Path) -> dict[str, object]:
    return json.loads((run / "manifest/v551j_readiness_report.json").read_text(encoding="utf-8"))


def test_review_required_component_stays_present_and_review_only() -> None:
    candidate = _csv(REVIEW_SMOKE, "packets/v551j_joint_packet_candidate_index.csv")
    component = _csv(REVIEW_SMOKE, "packets/v551j_joint_component_index.csv")
    review = _csv(REVIEW_SMOKE, "packets/v551j_review_surface.csv")
    certified = _csv(REVIEW_SMOKE, "packets/v551j_certified_joint_packet_index.csv")

    assert len(component) == 4
    assert len(review) == 1
    assert certified.empty
    assert candidate.loc[0, "certification_status"] == "REVIEW_REQUIRED_PRESSURE_COMPONENT"
    assert candidate.loc[0, "review_required"] is True or str(candidate.loc[0, "review_required"]).lower() == "true"
    assert candidate.loc[0, "ready_for_v552j_joint_evidence"] is False or str(candidate.loc[0, "ready_for_v552j_joint_evidence"]).lower() == "false"
    assert json.loads(candidate.loc[0, "review_reason_codes_json"]) == ["REVIEW_REQUIRED_LOW_SUPPORT_COMPONENT"]
    assert int(candidate.loc[0, "v552_pressure_review_required_component_count"]) == 1
    assert int(candidate.loc[0, "v552_pressure_linkable_component_count"]) == 2
    assert int(candidate.loc[0, "v552_pressure_neutral_coverage_component_count"]) == 1
    assert int(candidate.loc[0, "unmatched_unexplained_component_count"]) == 0
    assert "v552_pressure_review_required" in set(component["component_v552_linkage_class"])


def test_underpowered_v551_fields_propagate_without_support_score_override() -> None:
    component = _csv(REVIEW_SMOKE, "packets/v551j_joint_component_index.csv")
    row = component[component["component_v552_linkage_class"].eq("v552_pressure_review_required")].iloc[0]

    assert row["v551_support_status"] == "underpowered"
    assert row["v551_support_gate_status"] == "underpowered"
    assert str(row["v551_manual_review_flag"]).lower() == "true"
    assert row["v551_manual_review_reason"] == "REVIEW_REQUIRED_LOW_SUPPORT"
    assert row["v551_v552_pressure_component_status"] == "REVIEW_REQUIRED"
    assert row["v551_v552_pressure_component_ineligibility_reason"] == "low_support_review_required"


def test_neutral_coverage_component_does_not_force_packet_review() -> None:
    candidate = _csv(NEUTRAL_SMOKE, "packets/v551j_joint_packet_candidate_index.csv")
    component = _csv(NEUTRAL_SMOKE, "packets/v551j_joint_component_index.csv")
    review = _csv(NEUTRAL_SMOKE, "packets/v551j_review_surface.csv")

    assert len(component) == 3
    assert review.empty
    assert candidate.loc[0, "certification_status"] == "CERTIFIED_JOINT_RELATION_EVIDENCE"
    assert int(candidate.loc[0, "v552_pressure_review_required_component_count"]) == 0
    assert int(candidate.loc[0, "v552_pressure_neutral_coverage_component_count"]) == 1
    assert "v552_pressure_ineligible_known_neutral" in set(component["component_v552_linkage_class"])


def test_gss_totals_remain_accepted_after_repair() -> None:
    summary = pd.read_csv(OUTPUT_ROOT / "reports/gss_v551j_review_required_repair_summary.csv")
    assert int(summary["candidate_count"].sum()) == 782
    assert int(summary["certified_count"].sum()) == 154
    assert int(summary["review_count"].sum()) == 628
    assert set(summary["returncode"]) == {0}
    assert set(summary["final_status"]) == {"READY_V551J_JOINT_EVIDENCE_CONTRACT"}


def test_smoke_readiness_statuses_are_exact() -> None:
    assert _ready(REVIEW_SMOKE)["final_status"] == "PARTIAL_READY_V551J_REVIEW_ONLY"
    assert _ready(REVIEW_SMOKE)["ready_for_v552j_joint_evidence"] is False
    assert _ready(NEUTRAL_SMOKE)["final_status"] == "READY_V551J_JOINT_EVIDENCE_CONTRACT"
    assert _ready(NEUTRAL_SMOKE)["ready_for_v552j_joint_evidence"] is True
