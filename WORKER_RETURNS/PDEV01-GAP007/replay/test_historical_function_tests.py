"""Five historical-function jurisprudence tests for GAP-007, TEST_ONLY."""
from __future__ import annotations
import json
from pathlib import Path


def _replay():
    return json.loads((Path(__file__).resolve().parents[1] / "evidence/replay_gap.json").read_text())


def test_01_history_pinned_actual_p1_constructor_and_tests():
    r = _replay()["historical_p1"]
    assert r["commit"] == "d1278613e9e1a5d986ccce15782a697f19cbd722"
    assert "programma_pyat_original35_constructor.py" in r["constructor"]
    assert r["test_count"] == 18


def test_02_current_requirement_is_execution_receiver_not_reinvented_manifest():
    r = _replay()
    assert r["input"]["batch_manifest_units"] == 840
    assert r["input"]["batch_manifest_equals_plan_units"] is True
    assert r["current_receiver"]["batch_runner_class"].endswith("BatchExecutionRunner")


def test_03_first_consumer_is_current_batch_runner_and_its_exact_release_mismatch():
    r = _replay()
    assert r["receiver_execution"] == "NOT_EXECUTED"
    assert r["first_typed_mismatch"]["code"] == "BatchIntegrityError"
    assert "exact C11 release unavailable" in r["first_typed_mismatch"]["message"]
    assert r["first_typed_mismatch"]["release_refs_count"] == 35


def test_04_authority_and_unit_constraints_preserve_test_only_and_no_invention():
    r = _replay()
    assert r["input"]["source_qualification"] == "TEST_ONLY_SOURCEFREE"
    assert r["input"]["no_drop_ok"] is True
    assert r["input"]["waves"] == 35
    assert r["input"]["items"] == 70
    assert r["no_drop_evidence"]["no_invented_metadata"] is True
    assert r["first_typed_mismatch"]["release_refs_count"] == 35


def test_05_comparative_disposition_reuse_manifest_defer_new_compiler():
    r = _replay()
    # The current BatchManifest accepts exact P1 units; no repair is justified
    # merely to invent missing C11 releases or a replacement compiler.
    assert r["current_receiver"]["batch_manifest_accepted"]["content_hash"] == (
        "d9164f33d81ea2ec30681af98364e06983967a3a1f784f40d30ab2639553dca5"
    )
    assert r["no_drop_evidence"]["operation_identity_count"] == 840
    assert r["no_drop_evidence"]["batch_unit_identity_count"] == 840
