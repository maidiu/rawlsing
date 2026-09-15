"""V01 regression coverage for the bounded T02 predecessor-lineage repair."""
from __future__ import annotations

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.sdtf_r4_generic_batch_adapter import (
    ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT,
    CANDIDATE_ROW_KIND,
    NOT_PROJECTABLE,
    PREDECESSOR_CHAIN_INVALID,
    adapt_generic_r4_batch,
)
from rawlsing_next.tests import test_sdtf_r4_generic_batch_adapter as fx


def _receipt(result, row):
    return {
        receipt.candidate_row_ref.object_id: receipt
        for receipt in result.candidate_receipts
    }[row["ref"]["object_id"]]


def _forged_predecessor(tag: str):
    g0 = fx._row(tag, generation=0)
    actual_ref = ExactRef(**g0["ref"])
    forged_hash = fx._h(f"v01-forged-predecessor:{tag}")
    assert forged_hash != actual_ref.content_hash
    forged = ExactRef(
        CANDIDATE_ROW_KIND,
        actual_ref.object_id,
        forged_hash,
    ).as_dict()
    return g0, forged


def test_forged_predecessor_hash_with_prior_absent_fails_closed():
    _, forged = _forged_predecessor("lineage-forged-absent")
    successor = fx._row(
        "lineage-forged-absent",
        generation=1,
        predecessor=forged,
    )
    result = adapt_generic_r4_batch(
        fx._batch([successor], tag="v01-forged-absent")
    )
    receipt = _receipt(result, successor)
    assert PREDECESSOR_CHAIN_INVALID in receipt.integrity_failures
    assert receipt.runtime_projection_state == NOT_PROJECTABLE
    assert receipt.runtime_binding is None


def test_exact_predecessor_copresent_is_lawfully_accepted():
    g0 = fx._row("lineage-exact", generation=0)
    g1 = fx._row("lineage-exact", generation=1, predecessor=g0["ref"])
    result = adapt_generic_r4_batch(
        fx._batch([g0, g1], tag="v01-exact-copresent")
    )
    receipt = _receipt(result, g1)
    assert PREDECESSOR_CHAIN_INVALID not in receipt.integrity_failures
    assert receipt.runtime_projection_state == ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT
    assert receipt.runtime_binding is not None


def test_wrong_predecessor_hash_with_prior_copresent_fails_closed():
    g0, forged = _forged_predecessor("lineage-forged-copresent")
    g1 = fx._row(
        "lineage-forged-copresent",
        generation=1,
        predecessor=forged,
    )
    result = adapt_generic_r4_batch(
        fx._batch([g0, g1], tag="v01-forged-copresent")
    )
    receipt = _receipt(result, g1)
    assert PREDECESSOR_CHAIN_INVALID in receipt.integrity_failures
    assert receipt.runtime_projection_state == NOT_PROJECTABLE
    assert receipt.runtime_binding is None


def test_generation_zero_with_nonnull_predecessor_fails_closed():
    predecessor = fx._ref("SDTF_R4_GENERIC_BATCH_CANDIDATE_ROW", "v01-g0-nonnull")
    row = fx._row("g0-nonnull", generation=0, predecessor=predecessor)
    result = adapt_generic_r4_batch(
        fx._batch([row], tag="v01-g0-nonnull")
    )
    receipt = _receipt(result, row)
    assert PREDECESSOR_CHAIN_INVALID in receipt.integrity_failures
    assert receipt.runtime_projection_state == NOT_PROJECTABLE


def test_generation_positive_with_null_predecessor_fails_closed():
    row = fx._row("g1-null", generation=1, predecessor=None)
    result = adapt_generic_r4_batch(
        fx._batch([row], tag="v01-g1-null")
    )
    receipt = _receipt(result, row)
    assert PREDECESSOR_CHAIN_INVALID in receipt.integrity_failures
    assert receipt.runtime_projection_state == NOT_PROJECTABLE


def test_lineage_failure_is_row_local_and_unrelated_valid_row_still_projects():
    _, forged = _forged_predecessor("lineage-isolated-bad")
    bad = fx._row(
        "lineage-isolated-bad",
        generation=1,
        predecessor=forged,
    )
    good = fx._row("lineage-isolated-good")
    result = adapt_generic_r4_batch(
        fx._batch([bad, good], tag="v01-lineage-isolation")
    )
    bad_receipt = _receipt(result, bad)
    good_receipt = _receipt(result, good)
    assert PREDECESSOR_CHAIN_INVALID in bad_receipt.integrity_failures
    assert bad_receipt.runtime_binding is None
    assert good_receipt.integrity_failures == ()
    assert good_receipt.runtime_projection_state == ADAPTER_VALIDATED_CANDIDATE_NOT_CURRENT
    assert good_receipt.runtime_binding is not None


def test_exact_lineage_repair_does_not_change_row_or_batch_identity_law():
    g0 = fx._row("lineage-identity", generation=0)
    g1 = fx._row("lineage-identity", generation=1, predecessor=g0["ref"])
    forward = adapt_generic_r4_batch(
        fx._batch([g0, g1], tag="v01-lineage-identity")
    )
    reverse = adapt_generic_r4_batch(
        fx._batch([g1, g0], tag="v01-lineage-identity")
    )
    assert forward.batch_ref == reverse.batch_ref
    assert forward.batch_receipt_ref == reverse.batch_receipt_ref
    assert [receipt.ref for receipt in forward.candidate_receipts] == [
        receipt.ref for receipt in reverse.candidate_receipts
    ]
    assert {receipt.candidate_row_ref.as_dict()["content_hash"] for receipt in forward.candidate_receipts} == {
        g0["ref"]["content_hash"],
        g1["ref"]["content_hash"],
    }


def test_repair_does_not_weaken_existing_non_lineage_boundaries():
    # Re-run the producer's exact boundary checks most likely to be affected by
    # a batch-level lineage edit.  The full unchanged producer suite remains a
    # separate required test artifact and is executed alongside this file.
    fx.test_exact_duplicate_row_refs_deduplicate_idempotently()
    fx.test_same_key_generation_different_hashes_are_both_quarantined_with_no_winner()
    fx.test_silent_not_applicable_on_required_determinant_is_rejected()
    fx.test_candidate_only_row_stays_governed_and_cannot_masquerade_as_current()
    fx.test_currentness_evidence_mismatch_is_rejected_by_existing_r4_path()
    fx.test_adapter_does_not_invent_authority_ref_rule_body_or_currentness()
