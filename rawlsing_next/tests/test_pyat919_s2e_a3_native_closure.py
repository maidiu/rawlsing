"""Agent A3 — native I05 exact output closure falsifiers over B2's fact-fate repair.

All four controls use the actual S2-E five-unit native C11 sourcefree Batch.
B2's scientific decision and factual input values remain unchanged.
Every substituted receipt is reconstructed with a valid canonical public hash,
outer frontier replay is recomputed, and completed Batch result refs are updated.
The repair must reject false authority/provenance/effect/used-object claims.
"""
from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import DiscoveryResultReceipt
from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope
from rawlsing_next.pre553_s2e_exact_conservation import (
    S2EOutputConservationError,
    census_native_batch,
    require_same_native_output_graph,
)
from rawlsing_next.tests.test_pyat919_s2e_a_counterattack import (
    _outer_consistent,
    _forge_receipt,
)
from rawlsing_next.tests.test_pyat919_s2e_a_whole_native_batch import _batch, _native_case


def _five_unit():
    case = _native_case()
    with I03GroupedExecutionScope() as scope:
        manifest, receipts, outputs, baseline, _, _ = _batch(case, scope=scope)
    unit = next(u for u in manifest.units if u.job_kind == "DISCOVERY")
    original = outputs[unit.unit_hash]
    assert len(original.receipts) == 1
    return case, manifest, receipts, outputs, baseline, unit, original.receipts[0]


def _expect_red_and_exact_restoration(
    case, manifest, receipts, outputs, baseline, unit, tampered,
    code,
):
    altered_history, altered_outputs = _outer_consistent(
        manifest, receipts, outputs, unit, tampered,
    )
    with pytest.raises(S2EOutputConservationError, match=code):
        census_native_batch(
            manifest, altered_history, altered_outputs,
            require_complete=True, runtime_catalog=case[1],
        )
    restored = census_native_batch(
        manifest, receipts, outputs,
        require_complete=True, runtime_catalog=case[1],
    )
    require_same_native_output_graph(baseline, restored)


def test_a3_rehashed_structural_or_actor_promotion_is_not_native_discovery():
    case, manifest, history, outputs, baseline, unit, receipt = _five_unit()
    assert receipt.structural_truth_effect is False
    assert receipt.actor_v3_effect is False
    assert receipt.diagnostic_score_is_empirical_fact is False
    for field in (
        "structural_truth_effect",
        "actor_v3_effect",
        "diagnostic_score_is_empirical_fact",
    ):
        tampered = _forge_receipt(receipt, overrides={field: True})
        assert tampered.ref != receipt.ref
        _expect_red_and_exact_restoration(
            case, manifest, history, outputs, baseline, unit, tampered,
            "S2E_I05_NONPROMOTION_FLAGS_MISMATCH",
        )


def test_a3_rehashed_wrong_query_contract_is_not_native_i05():
    case, manifest, history, outputs, baseline, unit, receipt = _five_unit()
    wrong = "PRE553_I03_FAKE_QUERY_ABI@0.0.0"
    assert receipt.exact_query_contract_id != wrong
    forged = _forge_receipt(receipt, overrides={"exact_query_contract_id": wrong})
    _expect_red_and_exact_restoration(
        case, manifest, history, outputs, baseline, unit, forged,
        "S2E_I05_QUERY_EXECUTION_CONTRACT_MISMATCH",
    )


def test_a3_rehashed_native_dependency_and_authority_loss_is_refused():
    case, manifest, history, outputs, baseline, unit, receipt = _five_unit()
    assert receipt.dependency_refs
    # A self-consistent receipt may still omit source/issuer/fact references.
    # No arithmetic or fact preimage is changed by this forgery.
    forged_deps = DiscoveryResultReceipt(
        typed_state=receipt.typed_state,
        authority_snapshot_refs=receipt.authority_snapshot_refs,
        dependency_refs=(),
        producer_replay_locator_or_reference_root=receipt.producer_replay_locator_or_reference_root,
        **receipt.semantic_fields,
    )
    _expect_red_and_exact_restoration(
        case, manifest, history, outputs, baseline, unit, forged_deps,
        "S2E_I05_DEPENDENCY_CLOSURE_MISMATCH",
    )
    assert len(receipt.authority_snapshot_refs) > 1
    forged_auth = DiscoveryResultReceipt(
        typed_state=receipt.typed_state,
        authority_snapshot_refs=(receipt.authority_snapshot_refs[0],),
        dependency_refs=receipt.dependency_refs,
        producer_replay_locator_or_reference_root=receipt.producer_replay_locator_or_reference_root,
        **receipt.semantic_fields,
    )
    _expect_red_and_exact_restoration(
        case, manifest, history, outputs, baseline, unit, forged_auth,
        "S2E_I05_AUTHORITY_SNAPSHOT_CLOSURE_MISMATCH",
    )


def test_a3_extra_self_consistent_executed_query_outside_issued_frontier_refused():
    case, manifest, receipts, outputs, baseline, unit, receipt = _five_unit()
    original = outputs[unit.unit_hash]
    extra_query = case[2][1][0]  # Legitimate F2 query, but NOT a role of I05.
    assert extra_query.ref not in {q.ref for q in original.executed_queries}
    forged = replace(
        original,
        executed_queries=tuple(
            sorted((*original.executed_queries, extra_query), key=lambda q: q.ref.key)
        ),
    )
    # Outer I05 replay and Batch receipt already match; native producer would
    # never include an unused query in the I05 executed-object closure.
    with pytest.raises(
        S2EOutputConservationError,
        match="S2E_I05_EXECUTED_OBJECT_CLOSURE_MISMATCH",
    ):
        census_native_batch(
            manifest, receipts,
            {**outputs, unit.unit_hash: forged},
            require_complete=True, runtime_catalog=case[1],
        )
    require_same_native_output_graph(
        baseline, census_native_batch(
            manifest, receipts, outputs,
            require_complete=True, runtime_catalog=case[1],
        ),
    )
