"""S2-E A sourcefree adversarial controls over actual native first readers.

Uses the existing governed synthetic SAV source→C11→I03/I05/Batch routines,
not a hand-written statistical emulator. Frozen original packet: #919 S2-E.
"""
from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_query import (
    I03GroupedExecutionScope,
    execute_empirical_query,
)
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_issued_workload import execute_issued_workload
from rawlsing_next.pre553_s2e_exact_conservation import (
    S2EOutputConservationError,
    census_native_batch,
    require_same_native_output_graph,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _build_source, _query, _query_authority,
)
from rawlsing_next.tests.test_universal_workload_custody import (
    HOST, PURPOSE, _issued_workloads, _resolver,
)
from rawlsing_next.tests.test_universal_workload import (
    AS_OF, _frontier_bundle, _frontier_fixture,
)
from rawlsing_next.pre553_universal_workload import (
    compile_governed_frontier, execute_governed_frontier,
)


def _full_query_run(tmp_path, *, scope=None, shared=None):
    if shared is None:
        tmp_path.mkdir(parents=True, exist_ok=True)
        bundle, issued = _issued_workloads(tmp_path)
    else:
        bundle, issued = shared
    item = issued[0]
    result = execute_issued_workload(
        item.workload,
        _resolver((item,)),
        source_factory=lambda _ref: bundle.physical_stream,
        host=HOST, purpose=PURPOSE, allow_test_only=True,
        group_scope=scope,
    )
    return result


def _query_census(result):
    # The normal issued native result (not a stand-alone model record) exposes
    # its first-reader full-output conservation contract.
    return result.exact_s2e_output_census(require_complete=True)


def _discovery_run(tmp_path):
    bundle, _rows = _frontier_bundle(tmp_path / "s2e_frontier.sav")
    inventory, policy, frontier = _frontier_fixture(bundle)
    compilation = compile_governed_frontier(
        bundle=bundle, inventory=inventory, policy=policy, frontier=frontier,
        as_of=AS_OF, host=HOST, purpose=PURPOSE,
    )
    actual = execute_governed_frontier(
        compilation=compilation, source_factory=lambda _ref: bundle.physical_stream,
    )
    native = actual.native_execution
    return actual, native, census_native_batch(
        native.manifest, native.receipts,
        {native.manifest.units[0].unit_hash: native.native_result},
        require_complete=True,
    )


def test_a_real_issued_i03_batch_complete_and_identity_parity(tmp_path):
    # Same immutable source edition, issuer and full input universe; changing
    # the test SAV path would change the upstream SHA and invalidate parity.
    source = _issued_workloads(tmp_path)
    shared = _full_query_run(tmp_path, shared=source)
    # A closed scope forces the original exact per-operation evaluator. It is
    # not an alternative scientific model or an untrusted cache.
    disabled = I03GroupedExecutionScope()
    disabled.close()
    independent = _full_query_run(tmp_path, scope=disabled, shared=source)
    first = _query_census(shared)
    second = _query_census(independent)
    require_same_native_output_graph(first, second)
    assert first.i03_fact_count >= 1
    assert first.complete and not first.unresolved_unit_count
    assert first.full_output_sha256 == second.full_output_sha256


def test_a_full_output_receipt_severance_is_not_a_count_pass(tmp_path):
    result = _full_query_run(tmp_path)
    receipt = result.receipts[0]
    assert receipt.result_refs
    # A successful Batch execution receipt can be internally well-formed
    # while falsely omitting an actual result ref. The consumer audit rejects.
    forged = replace(receipt, result_refs=())
    with pytest.raises(S2EOutputConservationError, match="S2E_BATCH_RECEIPT_RESULT_GRAPH_LOSS"):
        census_native_batch(
            result.manifest, (forged,), result.outputs_by_unit, require_complete=True,
        )
    # Removing output while retaining a legitimate completed receipt is
    # different from an explicitly pending/DEFERRED unit.
    with pytest.raises(S2EOutputConservationError, match="S2E_COMPLETED_WITHOUT_ACTUAL_OUTPUT"):
        census_native_batch(result.manifest, result.receipts, {}, require_complete=True)


def test_a_real_i05_batch_full_frontier_negative_and_replay(tmp_path):
    actual, native, census = _discovery_run(tmp_path)
    result = native.native_result
    assert actual.anti_join["no_drop_ok"]
    assert census.complete and census.i05_receipt_count == result.candidate_count
    assert census.i05_fact_count == len(result.empirical_facts)
    assert census.i05_receipt_count >= 1
    assert "DISCOVERY:VALID_EMPTY" in census.typed_state_counts
    assert "DISCOVERY:DISCOVERED_RESULT_SUPPORTED" in census.typed_state_counts
    again = census_native_batch(
        native.manifest, native.receipts,
        {native.manifest.units[0].unit_hash: result}, require_complete=True,
    )
    require_same_native_output_graph(census, again)


def test_a_false_complete_i05_count_and_unvisited_branch_refused(tmp_path):
    _actual, native, original = _discovery_run(tmp_path)
    result = native.native_result
    # ExactBoundedDiscoveryResult's old constructor checks two claimed totals
    # agree, but not that a receipt exists for *every* claimed candidate.
    tampered = replace(
        result, candidate_count=result.candidate_count + 1,
        covered_candidate_count=result.covered_candidate_count + 1,
    )
    with pytest.raises(S2EOutputConservationError,
                       match="S2E_MISSING_DISCOVERY_CANDIDATE_FATE"):
        census_native_batch(
            native.manifest, native.receipts,
            {native.manifest.units[0].unit_hash: tampered}, require_complete=True,
        )
    restored = census_native_batch(
        native.manifest, native.receipts,
        {native.manifest.units[0].unit_hash: result}, require_complete=True,
    )
    require_same_native_output_graph(original, restored)


def test_a_grouped_compatible_i03_reuses_core_without_changing_facts():
    rows = [
        {"id": "A", "responses": {"X": 0, "Y": 0, "Z": 1}},
        {"id": "B", "responses": {"X": 1, "Y": 0, "Z": 1}},
        {"id": "C", "responses": {"X": 1, "Y": 1, "Z": 0}},
        {"id": "D", "responses": {"X": 0, "Y": 1, "Z": 0}},
    ]
    source = _build_source("s2e-shared-keys", rows)
    qa = _query_authority("s2e-shared")
    p = _branch_predicate(source, qa, tag="all")
    query1 = _query(source, qa, p, ("X", "Y", "Z"), tag="joint-one")
    query2 = _query(source, qa, p, ("X", "Y", "Z"), tag="joint-two")
    registry = AuthorityRegistry((*source["authorities"], qa))
    kwargs = {
        "repository": source["repo"],
        "predicate": p,
        "authority_registry": registry,
        "release_refs": (source["release_ref"],),
    }
    with I03GroupedExecutionScope() as scope:
        first = execute_empirical_query(query=query1, group_scope=scope, **kwargs)
        second = execute_empirical_query(query=query2, group_scope=scope, **kwargs)
        proof = scope.receipt()
    first_native = execute_empirical_query(query=query1, **kwargs)
    second_native = execute_empirical_query(query=query2, **kwargs)
    assert [fact.as_dict() for fact in first.facts] == [
        fact.as_dict() for fact in first_native.facts
    ]
    assert [fact.as_dict() for fact in second.facts] == [
        fact.as_dict() for fact in second_native.facts
    ]
    assert proof["core_builds"] >= 1
    assert proof["core_hits"] >= 1
    assert len(first.facts[0].target_topology["complete_cell_semantic_projection"]) == 8


def test_a_incompatible_conditioner_and_upstream_changed_value_remain_distinct():
    from rawlsing_next.tests.test_pre553_empirical_query import (
        _predicate, _response_leaf, _cell_map,
    )
    baseline = [
        {"id": "A", "responses": {"X": 1, "Y": 0}},
        {"id": "B", "responses": {"X": 0, "Y": 1}},
        {"id": "C", "responses": {"X": 0, "Y": 0}},
    ]
    changed = [
        {"id": "A", "responses": {"X": 1, "Y": 1}},
        *baseline[1:],
    ]
    def run(rows):
        source = _build_source("s2e-f2-countervalue", rows)
        qa = _query_authority("s2e-f2")
        x = _predicate(source, qa, _response_leaf(source, qa, "X", 1), tag="x1")
        y = _predicate(source, qa, _response_leaf(source, qa, "Y", 1), tag="y1")
        qyx = _query(source, qa, x, ("Y",), tag="y-given-x")
        qxy = _query(source, qa, y, ("X",), tag="x-given-y")
        reg = AuthorityRegistry((*source["authorities"], qa))
        with I03GroupedExecutionScope() as scope:
            a = execute_empirical_query(repository=source["repo"], query=qyx,
                predicate=x, authority_registry=reg, release_refs=(source["release_ref"],),
                group_scope=scope)
            b = execute_empirical_query(repository=source["repo"], query=qxy,
                predicate=y, authority_registry=reg, release_refs=(source["release_ref"],),
                group_scope=scope)
            proof = scope.receipt()
        return a, b, proof
    first = run(baseline)
    changed_value = run(changed)
    restored = run(baseline)
    assert first[0].facts[0].ref != changed_value[0].facts[0].ref
    assert first[1].facts[0].ref != changed_value[1].facts[0].ref
    assert first[0].facts[0].ref == restored[0].facts[0].ref
    assert first[1].facts[0].ref == restored[1].facts[0].ref
    # Directional denominators must be independently computed:
    assert first[0].facts[0].raw_denominator_support == 1
    assert first[1].facts[0].raw_denominator_support == 1
    assert changed_value[1].facts[0].raw_denominator_support == 2
    assert first[2]["core_hits"] == 0
