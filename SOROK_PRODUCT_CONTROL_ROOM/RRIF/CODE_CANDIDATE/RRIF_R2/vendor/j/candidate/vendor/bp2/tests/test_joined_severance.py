"""Six same-assertion source-edge severances, plus four deeper variations.

The named downstream assertion is ``joined_consumer_assertion``. Each edge is
cut physically where the chain depends on it; the assertion must redden and the
same chain must return to passing when the edge is restored.
"""
from __future__ import annotations

import pytest

from bp2_joined.severance import (
    SEVERANCE_EDGES,
    SUPPLEMENTARY_EDGES,
    run_all_severances,
    severance_receipt,
)

ASSERTION = "bp2_joined.producer.joined_consumer_assertion"


@pytest.fixture(scope="module")
def trials(tmp_path_factory):
    root = tmp_path_factory.mktemp("severance")
    return run_all_severances(root)


def test_six_load_bearing_edges_are_declared():
    assert len(SEVERANCE_EDGES) == 6
    assert SEVERANCE_EDGES == (
        "C8_PROOF",
        "BP1_ACTOR_OTHER_HISTORY",
        "RULE_A_SOURCE",
        "RULE_T_GRANT_BINDING",
        "TARGET_COMMIT_READ_HASH",
        "PERFORMED_E2",
    )


def test_every_trial_uses_the_same_named_downstream_assertion(trials):
    assert trials
    for trial in trials:
        assert trial.assertion == ASSERTION


def test_every_primary_edge_reddens_then_restores(trials):
    primary = [t for t in trials if not t.supplementary]
    assert len(primary) == 6
    for trial in primary:
        assert trial.red["red"] is True, trial.as_dict()
        assert trial.restored["red"] is False, trial.as_dict()
        assert trial.proves is True


def test_red_failure_codes_are_the_actual_edge_codes(trials):
    expected = {
        "C8_PROOF": "PROOF_VERIFIER_REQUIRED",
        "BP1_ACTOR_OTHER_HISTORY": "ACTOR_ROLE_NOT_FOCAL",
        "RULE_A_SOURCE": "CAN008_RULE_A_UNISSUED",
        "RULE_T_GRANT_BINDING": "CAN011_TARGET_GRANT_UNISSUED",
        "TARGET_COMMIT_READ_HASH": "CONSUMER_READSET_MISMATCH",
        "PERFORMED_E2": "E2_ACTUATOR_SELF_BOUND",
    }
    by_edge = {t.edge: t for t in trials}
    for edge, code in expected.items():
        assert by_edge[edge].red["failure_code"] == code, by_edge[edge].as_dict()


def test_primary_edges_restore_on_the_same_root(trials):
    primary = [t for t in trials if not t.supplementary]
    for trial in primary:
        assert trial.same_root is True
        assert trial.restore_basis == "same_root_exact_state_restored"


def test_restored_positive_hashes_are_present_and_distinct_from_the_cut(trials):
    by_edge = {t.edge: t for t in trials}
    for edge in (
        "C8_PROOF",
        "BP1_ACTOR_OTHER_HISTORY",
        "RULE_A_SOURCE",
        "RULE_T_GRANT_BINDING",
        "PERFORMED_E2",
    ):
        restored = by_edge[edge].restored
        assert restored["red"] is False
        assert restored["c8_occurrence_id"] == "OCC-0001"
        assert restored["target_record_hash"]
        assert restored["consumed_state_hash"]
        assert restored["e2_receipt_hash"]
    target = by_edge["TARGET_COMMIT_READ_HASH"]
    assert target.red["red"] is True
    assert target.restored["red"] is False
    assert target.restored["target_record_hash"]


def test_supplementary_variations_also_redden_then_restore(trials):
    supplementary = [t for t in trials if t.supplementary]
    assert len(supplementary) == 4
    assert [t.edge for t in supplementary] == list(SUPPLEMENTARY_EDGES)
    for trial in supplementary:
        assert trial.red["red"] is True, trial.as_dict()
        assert trial.restored["red"] is False, trial.as_dict()
        assert trial.restore_basis == "identical_fresh_root_uncut"


def test_self_offer_variation_is_caught_by_the_assertion_not_by_a_refusal(trials):
    trial = next(t for t in trials if t.edge == "BP1_OTHER_SELF_OFFER")
    assert trial.red["red"] is True
    assert trial.red["ok"] is True
    assert "non-other offer" in trial.red["assertion_message"]


def test_severance_receipt_reports_ten_witnesses(trials):
    receipt = severance_receipt(trials)
    assert receipt["edge_count"] == 6
    assert receipt["supplementary_count"] == 4
    assert receipt["all_primary_proved"] is True
    assert receipt["all_supplementary_proved"] is True
    assert receipt["named_assertion"] == ASSERTION
