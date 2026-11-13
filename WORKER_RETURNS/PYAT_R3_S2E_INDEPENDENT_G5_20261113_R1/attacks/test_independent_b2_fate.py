"""Independent G5 reproduction of B2's SUPPORTED -> VALID_EMPTY scientific-fate control.

The frozen author test has a test-only .as_dict() call on frozen mapping refs.
This harness reuses the same native five-unit Batch and forges the identical
scientific-fate substitution with exact_ref normalization, then requires the
native fact-derived validator to refuse and exact restoration to pass.
"""
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import (
    DiscoveryResultReceipt,
    ExactRef,
    exact_ref,
    semantic_hash,
)
from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope
from rawlsing_next.pre553_s2e_exact_conservation import (
    S2EOutputConservationError,
    census_native_batch,
    require_same_native_output_graph,
)
from rawlsing_next.tests.test_pyat919_s2e_a_whole_native_batch import _batch, _native_case
from rawlsing_next.tests.test_pyat919_s2e_a_counterattack import _replay_ref


def test_independent_b2_false_valid_empty_refused_and_restore_exact():
    case = _native_case()
    with I03GroupedExecutionScope() as scope:
        manifest, receipts, outputs, baseline, _, _ = _batch(case, scope=scope)
    unit = next(u for u in manifest.units if u.job_kind == "DISCOVERY")
    original = outputs[unit.unit_hash]
    candidate = original.receipts[0]
    assert candidate.typed_state == "DISCOVERED_RESULT_SUPPORTED"
    assert candidate.coverage_state == "EVALUATED_SUPPORTED"
    assert original.valid_empty is False
    fact_refs = tuple(exact_ref(ref, "candidate fact") for ref in candidate.empirical_fact_refs)

    candidate_replay = _replay_ref("candidate-replay", {
        "contract": original.contract_id,
        "authority_ref": original.discovery_authority_ref.as_dict(),
        "frontier_ref": original.evaluated_frontier_ref.as_dict(),
        "candidate_id": candidate.candidate_identity["candidate_id"],
        "candidate_hash": candidate.candidate_identity["candidate_hash"],
        "coverage_state": "EVALUATED_VALID_EMPTY",
        "fact_refs": [ref.as_dict() for ref in fact_refs],
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
    forged_frontier = _replay_ref("frontier-replay", {
        "contract": original.contract_id,
        "frontier_ref": original.evaluated_frontier_ref.as_dict(),
        "receipt_refs": [forged_candidate.ref.as_dict()],
        "fact_refs": [ref.as_dict() for ref in original.empirical_fact_refs],
        "valid_empty": True,
    })
    forged = replace(
        original, receipts=(forged_candidate,), valid_empty=True,
        replay_ref=forged_frontier,
    )
    forged_history = tuple(
        replace(r, result_refs=(forged_candidate.ref,))
        if r.unit_ref == unit.unit_ref else r
        for r in receipts
    )
    with pytest.raises(
        S2EOutputConservationError,
        match="S2E_I05_CANDIDATE_SCIENTIFIC_FATE_MISMATCH",
    ):
        census_native_batch(
            manifest, forged_history,
            {**outputs, unit.unit_hash: forged},
            require_complete=True, runtime_catalog=case[1],
        )
    restored = census_native_batch(
        manifest, receipts, outputs,
        require_complete=True, runtime_catalog=case[1],
    )
    require_same_native_output_graph(baseline, restored)
