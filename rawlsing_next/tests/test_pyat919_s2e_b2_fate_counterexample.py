"""S2-E B2: source-derived native-I05 scientific fate counterexample.

A2 validates candidate identity, role/fact refs, provenance and exact replay,
but not whether retained empirical facts actually substantiate the claimed
SUPPORTED versus VALID_EMPTY scientific discovery decision. The negative below
keeps the original I03 facts, valid source/authority/frontier and authentic
query roles; it changes only the discovery *interpretation*, then rehashes
the legitimate nested and Batch envelopes exactly as the native producer.
"""
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import DiscoveryResultReceipt, semantic_hash
from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope
from rawlsing_next.pre553_s2e_exact_conservation import (
    S2EOutputConservationError,
    census_native_batch,
    require_same_native_output_graph,
)
from rawlsing_next.tests.test_pyat919_s2e_a_whole_native_batch import (
    _native_case, _batch,
)
from rawlsing_next.tests.test_pyat919_s2e_a_counterattack import _replay_ref


def test_b2_rehashed_false_valid_empty_from_actually_supported_minority_is_red():
    case = _native_case()
    with I03GroupedExecutionScope() as scope:
        manifest, receipts, outputs, baseline, _, _ = _batch(case, scope=scope)
    unit = next(u for u in manifest.units if u.job_kind == "DISCOVERY")
    original = outputs[unit.unit_hash]
    assert original.candidate_count == len(original.receipts) == 1
    assert not original.valid_empty
    candidate = original.receipts[0]
    assert candidate.typed_state == "DISCOVERED_RESULT_SUPPORTED"
    assert candidate.coverage_state == "EVALUATED_SUPPORTED"
    assert candidate.empirical_fact_refs

    # The true CONDITION/BASLINE empirical facts and every source, authority,
    # candidate identity, query role, winner and fact reference remain untouched.
    # Forge ONLY the interpretation, then recompute both authentic replay roots.
    candidate_replay = _replay_ref("candidate-replay", {
        "contract": original.contract_id,
        "authority_ref": original.discovery_authority_ref.as_dict(),
        "frontier_ref": original.evaluated_frontier_ref.as_dict(),
        "candidate_id": candidate.candidate_identity["candidate_id"],
        "candidate_hash": candidate.candidate_identity["candidate_hash"],
        "coverage_state": "EVALUATED_VALID_EMPTY",
        "fact_refs": [ref.as_dict() for ref in candidate.empirical_fact_refs],
        "release_refs": [ref.as_dict() for ref in unit.release_refs],
        "query_execution_contract": candidate.exact_query_contract_id,
    })
    fields = dict(candidate.semantic_fields)
    fields["coverage_state"] = "EVALUATED_VALID_EMPTY"
    fields["replay_ref"] = candidate_replay
    forged_candidate = DiscoveryResultReceipt(
        typed_state="VALID_EMPTY",
        authority_snapshot_refs=candidate.authority_snapshot_refs,
        dependency_refs=candidate.dependency_refs,
        producer_replay_locator_or_reference_root=candidate_replay,
        **fields,
    )
    forged_frontier_replay = _replay_ref("frontier-replay", {
        "contract": original.contract_id,
        "frontier_ref": original.evaluated_frontier_ref.as_dict(),
        "receipt_refs": [forged_candidate.ref.as_dict()],
        "fact_refs": [ref.as_dict() for ref in original.empirical_fact_refs],
        "valid_empty": True,
    })
    forged = replace(
        original, receipts=(forged_candidate,), valid_empty=True,
        replay_ref=forged_frontier_replay,
    )
    forged_batch_history = tuple(
        replace(receipt, result_refs=(forged_candidate.ref,))
        if receipt.unit_ref == unit.unit_ref else receipt for receipt in receipts
    )
    # The issued grammar and candidate roster, scoped facts, and all nested
    # object hashes and Batch result refs remain valid. Only the scientific
    # decision conflicts with the actual immutable I03 cell comparisons.
    with pytest.raises(
        S2EOutputConservationError,
        match="S2E_I05_CANDIDATE_SCIENTIFIC_FATE_MISMATCH",
    ):
        census_native_batch(
            manifest, forged_batch_history,
            {**outputs, unit.unit_hash: forged}, require_complete=True,
            runtime_catalog=case[1],
        )

    restored = census_native_batch(
        manifest, receipts, outputs, require_complete=True,
        runtime_catalog=case[1],
    )
    require_same_native_output_graph(baseline, restored)
