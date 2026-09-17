"""Replay ASTRA-D11 M10-M01 rule current-selection evidence."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT = ROOT / "WORKER_RETURNS" / "ASTRA-D11" / "01_M10_M01_RULE_CURRENT_SELECTION.json"


def canonical(value):
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def test_astra_d11_m10_m01_current_selection_replay_r1():
    a = json.loads(ARTIFACT.read_text(encoding="utf-8"))

    assert a["schema"] == "ASTRA_D11_M10_M01_RULE_CURRENT_SELECTION_R1"
    assert a["commission"]["commission_tip"] == "fa3b419637ae2738dce1647e9dc8f4a93616f8eb"
    assert a["consumed_exact"]["d10_pass_commit"] == "c108691752137e858d1fcac7eceeff12ddc39f12"
    assert a["consumed_exact"]["d10q_pass_commit"] == "4b85b6c574105aebb0ce7e4047a454db55eaab5c"

    assert digest(a["selection_evidence_material"]) == a["selection_evidence_ref"]["content_hash"]
    assert digest(a["current_selection_disposition_material"]) == a["current_selection_disposition_ref"]["content_hash"]

    gate = a["selection_evidence_material"]["gate_facts"]
    assert gate["d10_rule_currentness"] == "CANDIDATE_NOT_CURRENT"
    assert gate["d10_rule_current_selection_evidence_refs"] == []
    assert gate["d10_rule_noncurrent_disposition_refs"] == []
    assert gate["d10_adapter_current_selection_state"] == "ELIGIBLE_FOR_SEPARATE_SELECTION"
    assert gate["d10q_independent_qualification"] == "PASS"
    assert gate["d10q_repair_authority_exercised"] == "NONE"
    assert gate["packages_a_through_e_closed_before_selection"] is True
    assert gate["exact_projection_qualified"] is True
    assert gate["conflicting_current_selection_evidence_present"] is False
    assert gate["noncurrent_disposition_present"] is False

    fields = a["inherited_r4_fields"]
    assert fields["GBE-R4-026"] == "CURRENT_ACCEPTED"
    assert fields["GBE-R4-027"] == [a["selection_evidence_ref"]]
    assert fields["GBE-R4-028"] == []
    assert fields["determinant_states_changed"] is False
    assert fields["package_states_changed"] is False

    assert a["authority_adjudication"]["state"] == "POSITIVE"
    assert a["authority_adjudication"]["conflict_state"] == "NONE"
    assert a["authority_adjudication"]["missing_authority_state"] is False

    assert all(value is False for value in a["boundaries"].values())
    assert all(value is False for value in a["preserved"].values())

    assert a["selection_evidence_ref"]["content_hash"] == "79e93764946dedf0fe5e7e700fa7dc876fc50a8cbbe1e630dbf5b5fab0ed2d71"
    assert a["current_selection_disposition_ref"]["content_hash"] == "c34924fd14d927189607e0a7c734058a7fbf37ccb2d7bc437c07cd064343aaf1"
