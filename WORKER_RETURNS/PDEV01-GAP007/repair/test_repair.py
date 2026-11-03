"""Focused tests for GAP-007 repaired C11/I03/I05/Batch binding."""
from __future__ import annotations
import json
from pathlib import Path
HERE = Path(__file__).resolve().parent
TRACE = json.loads((HERE / "actual_trace.json").read_text())


def test_01_exact_c11_release_and_p1_operation_identity():
    assert TRACE["source"]["release_ref"]["kind"] == "C11LogicalRelease"
    assert TRACE["source"]["release_object_count"] > 0
    assert TRACE["p1"]["operation_identity_preserved"] is True
    assert TRACE["p1"]["original_plan_ref"] == TRACE["p1"]["bound_plan_ref"]


def test_02_all_840_p1_operations_accounted_with_no_invention():
    assert TRACE["p1"]["operation_count"] == 840
    assert TRACE["no_drop"]["all_840_accounted"] is True
    assert TRACE["no_drop"]["bound_210"] is True
    assert TRACE["no_drop"]["unsupported_630"] is True
    assert TRACE["no_drop"]["no_invented_operations"] is True


def test_03_bound_i03_batch_actual_output():
    assert TRACE["p1"]["manifest_unit_count"] == 210
    assert TRACE["batch"]["receipt_count"] == 210
    assert TRACE["batch"]["completed"] == 210
    assert TRACE["batch"]["states"] == {"COMPLETED": 210}
    assert TRACE["batch"]["fact_state_counts"] == {"SUPPORTED": 210}


def test_04_actual_i05_receiver_and_wrong_release_authority_refusals():
    assert TRACE["i05"]["status"] == "EXECUTED"
    assert TRACE["i05"]["native_result_type"] == "ExactBoundedDiscoveryResult"
    assert TRACE["i05"]["receipt_count"] > 0
    assert TRACE["i05"]["fact_count"] > 0
    assert TRACE["wrong_release_refusal"]["status"] == "TYPED_REFUSAL"
    assert "exact C11 release unavailable" in TRACE["wrong_release_refusal"]["detail"]
    assert TRACE["wrong_authority_refusal"]["status"] == "TYPED_REFUSAL"
    assert "query_ref exact preimage unavailable" in TRACE["wrong_authority_refusal"]["detail"]


def test_05_unsupported_p1_kinds_are_typed_refusals_not_invented_queries():
    counts = TRACE["p1"]["unsupported_typed_refusals"]
    assert counts == {"CONDITIONAL": 210, "HETEROGENEITY": 105, "JOINT": 210, "RECURSIVE_BRANCH": 105}
    assert len([x for x in TRACE["p1"]["accounting"] if x["status"] == "TYPED_REFUSAL"]) == 630
    assert all(x.get("reason") == "P1_OPERATION_KIND_HAS_NO_EXACT_CURRENT_I03_BINDING" for x in TRACE["p1"]["accounting"] if x["status"] == "TYPED_REFUSAL")


def test_06_frozen_source_has_exact_committed_sha():
    import hashlib
    frozen = HERE / "frozen/source.sav"
    assert hashlib.sha256(frozen.read_bytes()).hexdigest() == (
        "5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f"
    )
    assert TRACE["source"]["source_sha256"] == (
        "5009f3c9272dcbfb15a48b17cfff51f9afa67e60d6a2c1364c9aa07bc6732e4f"
    )


def test_07_two_fresh_processes_match_source_release_queries_manifest_i05():
    import os
    import subprocess
    import sys
    script = HERE / "replay_repair.py"
    env = dict(os.environ, PYTHONHASHSEED="0", PYTHONDONTWRITEBYTECODE="1")
    outputs = []
    for index in (1, 2):
        proc = subprocess.run(
            [sys.executable, str(script)], cwd=str(HERE.parents[2]),
            env={**env, "PYTHONPATH": str(HERE.parents[2])},
            capture_output=True, text=True, timeout=300,
        )
        assert proc.returncode == 0, proc.stdout[-2000:] + proc.stderr[-2000:]
        outputs.append(json.loads(proc.stdout))
    first, second = outputs
    assert first["source"]["source_sha256"] == second["source"]["source_sha256"]
    assert first["source"]["release_ref"] == second["source"]["release_ref"]
    assert first["p1"]["manifest_ref"] == second["p1"]["manifest_ref"]
    assert first["i05"]["compilation_ref"] == second["i05"]["compilation_ref"]
    first_refs = [row["bound_job_ref"] for row in first["p1"]["accounting"] if row["status"] == "BOUND_I03_QUERY"]
    second_refs = [row["bound_job_ref"] for row in second["p1"]["accounting"] if row["status"] == "BOUND_I03_QUERY"]
    assert len(first_refs) == len(second_refs) == 210
    assert first_refs == second_refs
    assert first["batch"]["receipt_count"] == second["batch"]["receipt_count"] == 210
    assert first["i05"]["receipt_count"] == second["i05"]["receipt_count"] == 16
    assert first["i05"]["compilation_ref"] == "78568e5e47b086d9f537a6359b8e729ab2d8e42305981075d21aa613e0b31dc9"
