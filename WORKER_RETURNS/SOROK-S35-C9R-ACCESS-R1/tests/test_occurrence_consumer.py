from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

RETURN = Path(__file__).resolve().parents[1]


def test_occurrence_consumer_intact_severed_restored_cold(tmp_path):
    evidence = tmp_path / "occurrence_consumer.json"
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(RETURN / "tools" / "occurrence_consumer_proof.py"),
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
    assert summary["reader_ok_all"] is True
    assert summary["intact_outcomes"] == {
        "PERFORMED": "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
        "OMITTED": "A_LOCAL_PERCEPTION_HOLD",
        "REFUSED": "OBSERVED_CURRENT_REFUSAL",
    }
    assert summary["intact_controlled_outcomes"] == {
        "PERFORMED": "OBSERVED_IMMEDIATE_OBJECT_ORIENTATION",
        "OMITTED": "A_OWNED_ACTION_HOLD",
        "REFUSED": "OBSERVED_CURRENT_REFUSAL",
    }
    assert set(summary["perception_severed_outcomes"].values()) == {
        "UNKNOWN_RECEIVABILITY"
    }
    assert set(summary["action_severed_outcomes"].values()) == {
        "A_OWNED_ACTION_HOLD"
    }
    assert summary["restored_outcomes"] == summary["intact_outcomes"]
    assert summary["clock_substitution_refused_all"] is True
    assert summary["cold_outcomes_match"] is True
    assert summary["cold_verify_all"] is True
    assert summary["performed_help_accept"] is True
    assert summary["omitted_help_accept"] is False
    assert summary["refused_help_accept"] is False
    assert summary["omitted_material_access"] is False
    assert summary["store_unmutated_by_s35"] is True
    assert summary["duplicate_admission"] is False
    assert summary["new_store_created"] is False
    assert summary["actual_a_producer"] == "NONE_VERIFIED"
    assert summary["missing_source_owner_contract_present"] is True
    assert summary["targetless_all"] is True
    assert summary["first_consumer"].endswith(
        "read_occurrence->evaluate_occurrence"
    )
    for world in document["worlds"].values():
        occurrence = world["occurrence"]
        assert occurrence["event_clock"] == 242
        assert occurrence["branch_clock"] == 10
        assert occurrence["clock_binding"]["distinct_sources"] is True
        assert occurrence["clock_binding"]["substitution"] is False
        assert occurrence["clock_binding"]["equality_claimed"] is False
        assert occurrence["duplicate_admission"] is False
        assert occurrence["new_store_created"] is False
        assert occurrence["c9_read_only"] is True
        assert all(occurrence["checks"].values())
        assert world["clock_substitution_fault"]["refused"] is True
        assert world["store_mutation"]["s35_mutated_store"] is False
        contract = world["missing_source_owner_contract"]
        assert contract["schema"] == "S35_MISSING_SOURCE_OWNER_CONTRACT@1"
        assert contract["actual_a_producer"] == "NONE_VERIFIED"
