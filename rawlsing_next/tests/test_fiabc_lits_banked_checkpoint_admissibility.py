from __future__ import annotations

import json
import subprocess
from pathlib import Path

from rawlsing_next import fiabc_lits_astra_substantive_parity as parity


ROOT = Path(__file__).resolve().parents[2]
SOURCE_BACKED_COMMIT = "ed9bc0c9fd8a25e43719650b5cd5b39caa4d613c"
CHECKPOINT_PATH = "WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/24_LITS_R5B_SUCCESSOR_I05_MATERIALIZATION_CHECKPOINT.json"
PARTIAL_PATH = "WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/22_LITS_R5B_SUCCESSOR_I05_PRECHECK_PARTIAL.json"
ORACLE_PATH = "WORKER_RETURNS/FIABC-CANONICAL-TERMINAL-READINESS-R1/25_LITS_R5B_SUCCESSOR_FROZEN_ORACLE.json"


def _git_json(path: str):
    subprocess.run(
        ["git", "fetch", "--no-tags", "origin", SOURCE_BACKED_COMMIT],
        cwd=ROOT,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    raw = subprocess.check_output(
        ["git", "show", f"{SOURCE_BACKED_COMMIT}:{path}"],
        cwd=ROOT,
    )
    return json.loads(raw)


def test_banked_checkpoint_identity_and_candidate_neutral_envelope_are_real():
    checkpoint = _git_json(CHECKPOINT_PATH)
    assert checkpoint["schema"] == "FIABC_LITS_CURRENT_NEUTRAL_I05_MATERIALIZATION_CHECKPOINT@1.0.0"
    assert checkpoint["checkpoint_sha256"] == "8593814c51456015e5167cbe6f05037de7dbeadcc36ab857c72192b9087f9062"
    assert checkpoint["source_identity"] == {
        "source": "LITS_I",
        "sha256": "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09",
        "rows": 29002,
        "variables": 1198,
    }
    assert checkpoint["material"]["frontier_manifest"]["candidate_count"] == 50
    assert checkpoint["material"]["frontier_manifest"]["query_role_count"] == 77
    assert len(checkpoint["material"]["comparison_fact_manifest"]) == 50
    assert len(checkpoint["material"]["constituent_i03_fact_manifest"]) == 60
    assert checkpoint["audit"]["candidate_processes_started"] == 0
    assert checkpoint["audit"]["candidate_outputs_seen"] == 0


def test_checkpoint_retains_exact_candidate_refs_but_not_complete_fact_cell_projections():
    checkpoint = _git_json(CHECKPOINT_PATH)
    rows = checkpoint["material"]["comparison_fact_manifest"]
    assert all("candidate_identity" in row["semantic_fields"] for row in rows)
    assert sum(len(row["semantic_fields"]["candidate_identity"]["query_roles"]) for row in rows) == 77
    facts = checkpoint["precheck"]["empirical_facts"]
    assert len(facts) == 60
    assert all("fact_ref" in fact and "typed_state" in fact for fact in facts)
    assert all("target_topology" in fact for fact in facts)
    assert all(
        set(fact["target_topology"]) <= {"arity", "joint_order_semantics", "target_domain_identity"}
        for fact in facts
    )
    assert not any("complete_cell_semantic_projection" in fact["target_topology"] for fact in facts)
    assert not any("raw_numerator_support" in fact for fact in facts)


def test_adjacent_banked_precheck_and_oracle_do_not_restore_missing_cell_preimages():
    partial = _git_json(PARTIAL_PATH)
    oracle = _git_json(ORACLE_PATH)
    partial_facts = partial["empirical_facts"]
    assert len(partial_facts) == 60
    assert not any(
        "complete_cell_semantic_projection" in fact.get("target_topology", {})
        for fact in partial_facts
    )
    expected = oracle["expected_fact_manifest"]
    assert len(expected) == 50
    # Oracle candidate manifests preserve refs/terminal state, not full I03 fact cell projections.
    serialized = json.dumps(expected, sort_keys=True)
    assert "complete_cell_semantic_projection" not in serialized
    assert "raw_numerator_support" not in serialized


def test_repaired_parity_law_requires_complete_cell_semantic_projection():
    source = Path(parity.__file__).read_text(encoding="utf-8")
    assert 'complete_cell_semantic_projection' in source
    assert "raw_numerator_support" in source
    assert "first_exact_difference_witness" in source
    assert "first_exact_dependence_witness" in source


def test_checkpoint_is_admissible_for_identity_and_zero_source_resume_but_not_new_substantive_parity():
    checkpoint = _git_json(CHECKPOINT_PATH)
    assert checkpoint["precheck"]["candidate_count"] == 50
    assert checkpoint["precheck"]["query_role_count"] == 77
    assert checkpoint["precheck"]["coverage_state_counts"] == {
        "EVALUATED_SUPPORTED": 49,
        "EVALUATED_VALID_EMPTY": 1,
    }
    assert checkpoint["precheck"]["typed_state_counts"] == {
        "DISCOVERED_RESULT_SUPPORTED": 49,
        "VALID_EMPTY": 1,
    }
    # The missing numerator/cell projection is not a cosmetic field: P0/P1/P2/P3/P4
    # parity depends on those exact empirical values.
    facts = checkpoint["precheck"]["empirical_facts"]
    assert all("raw_denominator_support" in fact for fact in facts)
    assert all("raw_numerator_support" not in fact for fact in facts)
