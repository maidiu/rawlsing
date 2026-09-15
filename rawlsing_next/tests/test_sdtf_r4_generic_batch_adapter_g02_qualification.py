"""Independent hostile qualification for the repaired T02 generic R4 batch adapter."""

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.sdtf_r4_generic_batch_adapter import (
    CANDIDATE_ROW_KIND,
    NOT_PROJECTABLE,
    PREDECESSOR_CHAIN_INVALID,
    adapt_generic_r4_batch,
)
from rawlsing_next.tests import test_sdtf_r4_generic_batch_adapter as fx


def _receipts(result):
    return {r.candidate_row_ref.object_id: r for r in result.candidate_receipts}


def _forged_predecessor(g0, label):
    actual = ExactRef(**g0["ref"])
    forged_hash = fx._h(label)
    assert forged_hash != actual.content_hash
    return ExactRef(CANDIDATE_ROW_KIND, actual.object_id, forged_hash).as_dict()


def test_g02_forged_predecessor_hash_with_absent_prior_fails_closed():
    g0 = fx._row("g02-absent", generation=0)
    forged = _forged_predecessor(g0, "g02-forged-absent")
    g1 = fx._row("g02-absent", generation=1, predecessor=forged)
    result = adapt_generic_r4_batch(fx._batch([g1], tag="g02-absent"))
    receipt = result.candidate_receipts[0]
    assert PREDECESSOR_CHAIN_INVALID in receipt.integrity_failures
    assert receipt.runtime_projection_state == NOT_PROJECTABLE
    assert receipt.runtime_binding is None


def test_g02_exact_copresent_predecessor_is_accepted():
    g0 = fx._row("g02-exact", generation=0)
    g1 = fx._row("g02-exact", generation=1, predecessor=g0["ref"])
    result = adapt_generic_r4_batch(fx._batch([g0, g1], tag="g02-exact"))
    receipts = _receipts(result)
    r0 = receipts[g0["ref"]["object_id"]]
    r1 = receipts[g1["ref"]["object_id"]]
    assert PREDECESSOR_CHAIN_INVALID not in r0.integrity_failures
    assert PREDECESSOR_CHAIN_INVALID not in r1.integrity_failures
    assert r0.runtime_binding is not None
    assert r1.runtime_binding is not None


def test_g02_wrong_hash_with_copresent_prior_fails_closed():
    g0 = fx._row("g02-wrong", generation=0)
    forged = _forged_predecessor(g0, "g02-forged-copresent")
    g1 = fx._row("g02-wrong", generation=1, predecessor=forged)
    result = adapt_generic_r4_batch(fx._batch([g0, g1], tag="g02-wrong"))
    receipt = _receipts(result)[g1["ref"]["object_id"]]
    assert PREDECESSOR_CHAIN_INVALID in receipt.integrity_failures
    assert receipt.runtime_projection_state == NOT_PROJECTABLE
    assert receipt.runtime_binding is None


def test_g02_identity_invalid_prior_cannot_prove_lineage():
    g0 = fx._row("g02-stale", generation=0)
    stale_ref = dict(g0["ref"])
    stale_ref["content_hash"] = fx._h("g02-stale-supplied-ref")
    g0["ref"] = stale_ref
    g1 = fx._row("g02-stale", generation=1, predecessor=stale_ref)
    result = adapt_generic_r4_batch(fx._batch([g0, g1], tag="g02-stale"))
    receipt = _receipts(result)[g1["ref"]["object_id"]]
    assert PREDECESSOR_CHAIN_INVALID in receipt.integrity_failures
    assert receipt.runtime_projection_state == NOT_PROJECTABLE
    assert receipt.runtime_binding is None


def test_g02_lineage_acceptance_is_order_independent_and_deterministic():
    g0 = fx._row("g02-order", generation=0)
    g1 = fx._row("g02-order", generation=1, predecessor=g0["ref"])
    forward = adapt_generic_r4_batch(fx._batch([g0, g1], tag="g02-order"))
    reverse = adapt_generic_r4_batch(
        fx._batch([g1, g0], tag="g02-order", row_refs=[g1["ref"], g0["ref"]])
    )
    f = _receipts(forward)[g1["ref"]["object_id"]]
    r = _receipts(reverse)[g1["ref"]["object_id"]]
    assert PREDECESSOR_CHAIN_INVALID not in f.integrity_failures
    assert PREDECESSOR_CHAIN_INVALID not in r.integrity_failures
    assert f.ref == r.ref
    assert f.runtime_binding_ref == r.runtime_binding_ref
    assert forward.batch_ref == reverse.batch_ref
    assert forward.batch_receipt_ref == reverse.batch_receipt_ref


def test_g02_lineage_failure_is_row_local():
    prior = fx._row("g02-local-bad", generation=0)
    forged = _forged_predecessor(prior, "g02-local-forged")
    bad = fx._row("g02-local-bad", generation=1, predecessor=forged)
    good = fx._row("g02-local-good", generation=0)
    result = adapt_generic_r4_batch(fx._batch([bad, good], tag="g02-local"))
    receipts = _receipts(result)
    bad_receipt = receipts[bad["ref"]["object_id"]]
    good_receipt = receipts[good["ref"]["object_id"]]
    assert PREDECESSOR_CHAIN_INVALID in bad_receipt.integrity_failures
    assert bad_receipt.runtime_binding is None
    assert good_receipt.integrity_failures == ()
    assert good_receipt.runtime_binding is not None
