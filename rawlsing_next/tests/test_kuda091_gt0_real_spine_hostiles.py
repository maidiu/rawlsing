"""KUDA-091's nontrivial historical hostile GT0 checks, recast on REAL stages.

The old sibling-blind fake-stage harness is not substituted for the selected
current DVA→FF→PREV3→V3→V2 pipeline.
"""
from dataclasses import replace

import pytest

import rawlsing_next.wsc_gt0_end_to_end as gt0


def test_original_kuda091_v3_rng_state_mutation_detected_in_actual_spine(monkeypatch):
    genuine = gt0.run_gt0_prev3_v3

    def forged(prev3):
        real = genuine(prev3)
        altered = replace(real.after, rng_state_hash="a" * 64)
        assert altered != real.before
        return replace(real, after=altered)

    monkeypatch.setattr(gt0, "run_gt0_prev3_v3", forged)
    with pytest.raises(AssertionError, match="V3 state mutated"):
        gt0.run_gt0_end_to_end()


@pytest.mark.parametrize("field,forgery", [
    ("actor_claim_created", True),
    ("rendered_text", "UNAUTHORIZED_GT0_RENDER"),
    ("v3_mutated", True),
])
def test_original_kuda091_v2_actor_expression_and_v3_side_effects_blocked(
    monkeypatch, field, forgery
):
    genuine = gt0.run_gt0_v3_v2

    def forged(v3):
        real = genuine(v3)
        return replace(real, **{field: forgery})

    monkeypatch.setattr(gt0, "run_gt0_v3_v2", forged)
    with pytest.raises(AssertionError, match="V2 fabricated actor claim"):
        gt0.run_gt0_end_to_end()


def test_original_kuda091_exact_receipt_hash_changes_on_actual_stage_detail_drift():
    left = gt0.run_gt0_end_to_end()
    from rawlsing_next.wsc_gt0_protocol import gt0_content_hash
    prior = left.receipts[2]
    forged = replace(prior, detail_code=prior.detail_code + "__UNAUTHORIZED_CHANGE")
    forged_receipts = left.receipts[:2] + (forged,) + left.receipts[3:]
    altered_thread_hash = gt0_content_hash({
        "terminal": gt0.TERMINAL,
        "receipt_hashes": [r.content_hash for r in forged_receipts],
    })
    assert forged.content_hash != prior.content_hash
    assert altered_thread_hash != left.full_thread_hash
