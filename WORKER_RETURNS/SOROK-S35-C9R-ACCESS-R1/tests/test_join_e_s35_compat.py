from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys

RETURN = Path(__file__).resolve().parents[1]


def test_join_e_s35_same_root_compatibility_and_incompatibility(tmp_path):
    evidence = tmp_path / "join_e_s35_compat.json"
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [
            sys.executable,
            "-B",
            str(RETURN / "tools" / "join_e_s35_compat.py"),
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
    assert summary["worlds"] == 3
    assert summary["performed_help_accept"] is True
    assert summary["omitted_help_accept"] is False
    assert summary["refused_help_accept"] is False
    assert summary["omitted_operation_only_grant_observed"] is False
    assert summary["omitted_performed_aware_access"] is False
    assert summary["same_root_full_pipeline_incompatibility"] is True
    assert set(summary["controlled_same_root_outcomes"].values()) == {
        "PERCEPTION_TIME_INVALID"
    }
    assert set(summary["baseline_same_root_outcomes"].values()) == {
        "A_LOCAL_PERCEPTION_HOLD"
    }
    assert summary["targetless_all"] is True
    assert summary["store_unmutated_by_s35"] is True
    assert summary["cold_verify_all"] is True
    assert summary["s35_store_created"] is False
    for world in document["worlds"].values():
        assert world["join_e"]["event_time"] == 242
        assert world["join_e"]["c12_branch_clock"] == 10
        incompatibility = world["s35"]["full_pipeline_incompatibility"]
        assert incompatibility["event_time_gt_c12_clock"] is True
        assert incompatibility["ingress_status"] == "REFUSED"
        assert incompatibility["ingress_reason"] == "CLOCK_OUTSIDE_FRAME"
        assert incompatibility["same_root_c9_reexecution_lawful"] is False
        assert world["store_mutation"]["s35_mutated_store"] is False
