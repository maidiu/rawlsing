"""Additional G5 hostile variation: additive producer closure promotion.

A3's published test removes dependency/authority refs. This independently
tests the symmetric falsification risk: append a legitimate but non-native
dependency/authority ref, rehash the receipt, outer frontier and Batch graph,
and require exact refusal + restoration.
"""
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_objects import DiscoveryResultReceipt
from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope
from rawlsing_next.pre553_s2e_exact_conservation import (
    S2EOutputConservationError,
    census_native_batch,
    require_same_native_output_graph,
)
from rawlsing_next.tests.test_pyat919_s2e_a_counterattack import _outer_consistent
from rawlsing_next.tests.test_pyat919_s2e_a_whole_native_batch import _batch, _native_case


def _five_unit():
    case = _native_case()
    with I03GroupedExecutionScope() as scope:
        manifest, receipts, outputs, baseline, _, _ = _batch(case, scope=scope)
    unit = next(u for u in manifest.units if u.job_kind == "DISCOVERY")
    return case, manifest, receipts, outputs, baseline, unit, outputs[unit.unit_hash].receipts[0]


def test_additive_dependency_and_authority_closure_refused():
    case, manifest, receipts, outputs, baseline, unit, receipt = _five_unit()
    extra_query_ref = case[2][3][0].ref  # legitimate F4 query, not an I05 dependency
    assert extra_query_ref.key not in {r.key for r in receipt.dependency_refs}
    forged_dep = DiscoveryResultReceipt(
        typed_state=receipt.typed_state,
        authority_snapshot_refs=receipt.authority_snapshot_refs,
        dependency_refs=(*receipt.dependency_refs, extra_query_ref),
        producer_replay_locator_or_reference_root=receipt.producer_replay_locator_or_reference_root,
        **receipt.semantic_fields,
    )
    history, forged_outputs = _outer_consistent(
        manifest, receipts, outputs, unit, forged_dep,
    )
    with pytest.raises(S2EOutputConservationError, match="S2E_I05_DEPENDENCY_CLOSURE_MISMATCH"):
        census_native_batch(
            manifest, history, forged_outputs,
            require_complete=True, runtime_catalog=case[1],
        )
    extra_auth_ref = case[0]["authorities"][3].authority_ref  # replay authority
    assert extra_auth_ref.key not in {a.key for a in receipt.authority_snapshot_refs}
    forged_auth = DiscoveryResultReceipt(
        typed_state=receipt.typed_state,
        authority_snapshot_refs=(*receipt.authority_snapshot_refs, extra_auth_ref),
        dependency_refs=receipt.dependency_refs,
        producer_replay_locator_or_reference_root=receipt.producer_replay_locator_or_reference_root,
        **receipt.semantic_fields,
    )
    history, forged_outputs = _outer_consistent(
        manifest, receipts, outputs, unit, forged_auth,
    )
    with pytest.raises(S2EOutputConservationError, match="S2E_I05_AUTHORITY_SNAPSHOT_CLOSURE_MISMATCH"):
        census_native_batch(
            manifest, history, forged_outputs,
            require_complete=True, runtime_catalog=case[1],
        )
    restored = census_native_batch(
        manifest, receipts, outputs, require_complete=True, runtime_catalog=case[1],
    )
    require_same_native_output_graph(baseline, restored)
