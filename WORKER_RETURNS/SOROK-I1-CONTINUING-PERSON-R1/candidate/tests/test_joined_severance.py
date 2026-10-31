"""Seven load-bearing joined source severances plus three deeper variations.

The named assertion is ``bp2p4.assertion.joined_downstream_a0_a2_assertion``.
Each trial proves baseline PASS -> named assertion RED at the cut edge ->
restored PASS.
"""
from __future__ import annotations

import pytest

from bp2p4.assertion import ASSERTION_NAME
from bp2p4.severance import (
    SEVERANCE_EDGES,
    SUPPLEMENTARY_EDGES,
    run_all_severances,
    severance_receipt,
)

EXPECTED_RED = {
    "BP2_C8_PROOF": "BP2_C8_PROOF_INVALID",
    "BP2_ACTOR_HISTORY": "BP1_ACTOR_SOURCE_NOT_MATCHING_BP2_C8",
    "BP2_RULE_A": "BP2_RULE_A_RESPONSE_ABSENT",
    "BP2_RULE_T": "BP2_RULE_T_AUTHORIZATION_ABSENT",
    "BP2_TARGET_HASH": "BP2_C9_CONSUMED_HASH_MISMATCH",
    "BP2_E2": "BP2_E2_SELF_PERFORMED",
    "BP4_C10_M6_ACCESS": "A0_CLAIM_SET",
    "BP2_OTHER_HISTORY_ALIASED": "BP1_OTHER_SNAPSHOT_NOT_MATCHING_BP2_C8",
    "BP2_E2_NOT_PERFORMED": "A0_E2_ADMITTED",
    "BP2_PRACTICE_NOT_MATERIALIZED": "A0_PRACTICE_NOT_ESTABLISHED",
}


@pytest.fixture(scope="module")
def trials(tmp_path_factory, intact):
    work = tmp_path_factory.mktemp("severance")
    return run_all_severances(work, intact)


def test_seven_load_bearing_edges_are_declared():
    assert len(SEVERANCE_EDGES) == 7
    assert SEVERANCE_EDGES == (
        "BP2_C8_PROOF",
        "BP2_ACTOR_HISTORY",
        "BP2_RULE_A",
        "BP2_RULE_T",
        "BP2_TARGET_HASH",
        "BP2_E2",
        "BP4_C10_M6_ACCESS",
    )


def test_every_trial_uses_the_same_named_assertion(trials):
    assert trials
    assert {trial.assertion for trial in trials} == {ASSERTION_NAME}


def test_every_primary_edge_reddens_then_restores(trials):
    primary = [trial for trial in trials if not trial.supplementary]
    assert len(primary) == 7
    for trial in primary:
        assert trial.baseline["red"] is False, trial.as_dict()
        assert trial.red["red"] is True, trial.as_dict()
        assert trial.restored["red"] is False, trial.as_dict()
        assert trial.proves is True


def test_red_messages_are_the_actual_edge_codes(trials):
    by_edge = {trial.edge: trial for trial in trials}
    for edge, code in EXPECTED_RED.items():
        assert code in by_edge[edge].red["message"], by_edge[edge].as_dict()


def test_restoration_basis_is_explicit(trials):
    by_edge = {trial.edge: trial for trial in trials}
    for edge in ("BP2_C8_PROOF", "BP2_RULE_A", "BP2_RULE_T", "BP2_TARGET_HASH"):
        assert by_edge[edge].restore_basis == "same_root_exact_bytes_restored"
    for edge in ("BP2_ACTOR_HISTORY", "BP2_E2", "BP2_E2_NOT_PERFORMED",
                 "BP2_PRACTICE_NOT_MATERIALIZED"):
        assert by_edge[edge].restore_basis == "same_root_original_source_restored"
    assert by_edge["BP4_C10_M6_ACCESS"].restore_basis == (
        "fresh_c12_root_same_bp2_artifacts")


def test_supplementary_variations_also_redden_then_restore(trials):
    supplementary = [trial for trial in trials if trial.supplementary]
    assert [trial.edge for trial in supplementary] == list(SUPPLEMENTARY_EDGES)
    for trial in supplementary:
        assert trial.baseline["red"] is False
        assert trial.red["red"] is True
        assert trial.restored["red"] is False


def test_severance_receipt_reports_ten_witnesses(trials):
    receipt = severance_receipt(trials)
    assert receipt["edge_count"] == 7
    assert receipt["supplementary_count"] == 3
    assert receipt["all_primary_proved"] is True
    assert receipt["all_supplementary_proved"] is True
    assert receipt["named_assertion"] == ASSERTION_NAME
    assert receipt["edges"] == list(SEVERANCE_EDGES)
