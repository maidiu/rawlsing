from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

RETURN = Path(__file__).resolve().parents[1]


def test_actual_a_producer_is_missing_and_controlled_path_preserved(tmp_path):
    evidence = tmp_path / "actual_a_evidence.json"
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(RETURN / "tools" / "actual_a_evidence.py"),
            "--evidence-out",
            str(evidence),
            "--base-dir",
            str(tmp_path / "runtime"),
        ],
        cwd=str(RETURN),
        env=env,
        capture_output=True,
        text=True,
        timeout=240,
    )
    assert completed.returncode == 0, completed.stderr[-4000:]
    document = json.loads(evidence.read_text(encoding="utf8"))
    summary = document["summary"]
    assert summary["actual_a_producer"] == "NONE_VERIFIED"
    assert summary["performed_e2_a_action_present"] is True
    assert summary["performed_omit_a_omission_present"] is True
    assert summary["a_action_bound_to_e1"] is False
    assert summary["a_local_observation_of_e1"] is False
    assert summary["action_clock_matches_e1"] is False
    assert summary["action_order_persisted"] is False
    assert summary["actual_a_wiring_outcomes"]["performed-e2"] == {
        "perception_only": "PERCEPTION_TIME_INVALID",
        "action_only_with_controlled_perception": "ACTION_TIME_INVALID",
        "both_candidate": "PERCEPTION_TIME_INVALID",
    }
    assert summary["controlled_integration_preserved"] is True
    assert summary["cold_verify_all"] is True
    assert summary["store_unmutated_by_s35"] is True
    assert summary["s39_actual_a"] is False
    assert summary["s39_join_e_root_compatible"] is False
    assert summary["s39_synthetic_premises"] is True
    assert summary["missing_source_owner_contract_present"] is True
    performed = document["worlds"]["performed-e2"]
    assert performed["live"]["a_analysis"]["a_action_event_clocks"] == [10]
    assert performed["live"]["a_analysis"]["event_clock"] == 242
    assert performed["live"]["a_analysis"]["a_action_performed_rows"] == 1
    assert performed["live"]["a_analysis"]["a_own_action_perceptions"]
    omitted = document["worlds"]["performed-omit"]
    assert omitted["live"]["a_analysis"]["a_omission_rows"] == 1
    assert omitted["live"]["a_analysis"]["a_action_performed_rows"] == 0
    for world in document["worlds"].values():
        contract = world["live"]["missing_source_owner_contract"]
        assert contract["schema"] == "S35_MISSING_SOURCE_OWNER_CONTRACT@1"
        assert "A_LOCAL_OBSERVATION_RECEIPT_OF_E1" in contract["missing_fields"]
        assert (
            "A_ACTION_OR_OMISSION_RECEIPT_BOUND_TO_E1_CLOCK_AND_ORDER"
            in contract["missing_fields"]
        )
        assert "QUALIFIED_A_SOURCE_OWNER_RECEIPT" in contract["missing_fields"]
        assert world["store_mutation"]["mutated_by_s35"] is False
