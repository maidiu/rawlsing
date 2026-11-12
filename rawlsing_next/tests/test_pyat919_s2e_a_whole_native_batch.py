"""S2-E: one real native C11 first-reader Batch containing F1/F2/F3/F4/I05.

Unlike four isolated unit checks, these prove that the existing I03 and I05
executor, one sealed source scope, and Batch preserve the entire actual
output graph with compatible grouped reuse and with the ungrouped oracle.
"""
from __future__ import annotations

import json
import resource
import time

import pytest

from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec,
    ExecutionOutcome, ExecutorBinding,
)
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor, RuntimeObjectCatalog,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope
from rawlsing_next.pre553_s2e_exact_conservation import (
    S2EOutputConservationError, census_native_batch, require_same_native_output_graph,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _branch_predicate, _build_source, _predicate, _query, _query_authority,
    _response_leaf, _coordinate_leaf,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom, _d_auth, _discovery_authority, _grammar, _qt, _rule,
)


def _native_case():
    # 8/8 full binary-domain cells are enumerated even though the selected
    # synthetic 10+2 source only visits a strict subset. Group C is a minority.
    rows = [
        {"id": f"A{i}", "responses": {"X": i % 2, "Y": 0, "Z": i % 2},
         "coords": {"G": "A"}}
        for i in range(10)
    ]
    rows.extend([
        {"id": "C1", "responses": {"X": 1, "Y": 1, "Z": 0}, "coords": {"G": "C"}},
        {"id": "C2", "responses": {"X": 0, "Y": 1, "Z": 1}, "coords": {"G": "C"}},
    ])
    source = _build_source("pyat919-s2e-all-families", rows)
    qa = _query_authority("pyat919-s2e-queries")
    da = _d_auth("pyat919-s2e-discovery")
    allp = _branch_predicate(source, qa, tag="all")
    px = _predicate(source, qa, _response_leaf(source, qa, "X", 1), tag="x1")
    py = _predicate(source, qa, _response_leaf(source, qa, "Y", 1), tag="y1")
    pc = _predicate(source, qa, _coordinate_leaf(source, "G", "C"), tag="minority-c")
    f1 = _query(source, qa, allp, ("Y",), tag="F1-MARGINAL")
    f2yx = _query(source, qa, px, ("Y",), tag="F2-Y-GIVEN-X")
    f2xy = _query(source, qa, py, ("X",), tag="F2-X-GIVEN-Y")
    f4 = _query(source, qa, allp, ("X", "Y", "Z"), tag="F4-JOINT")
    grammar = _grammar(
        operation="I03-OP-pyat919-s2e-discovery",
        atoms=(_atom("ALL", allp, "BRANCH"), _atom("MIN", pc, "COORDINATE")),
        templates=(_qt("F1", f1),),
        rules=(_rule(
            "minority", "MINORITY_OR_NONMODAL_DEPARTURE", "SINGLE_ATOM",
            atom_ids=("MIN",), baseline_atom_id="ALL", query_template_id="F1",
            validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
        ),),
    )
    discovery = _discovery_authority(source, grammar, da, tag="s2e-all")
    catalog = RuntimeObjectCatalog(
        authorities=(*source["authorities"], qa, da),
        predicates=(allp, px, py, pc),
        queries=(f1, f2yx, f2xy, f4),
        discovery_authorities=(discovery,),
    )
    return source, catalog, ((f1,allp), (f2yx,px), (f2xy,py), (f4,allp)), discovery


def _batch(case, *, scope):
    source, catalog, queries, discovery = case
    executor = CarrierNeutralResearchExecutor(
        repository=source["repo"],
        release_refs=(source["release_ref"],),
        runtime_catalog=catalog,
    )
    release_ref = source["release_ref"]
    units = tuple(
        BatchUnitSpec("QUERY", query.ref, (release_ref,), (predicate.ref,))
        for query, predicate in queries
    ) + (BatchUnitSpec("DISCOVERY", discovery.ref, (release_ref,), ()),)
    manifest = BatchManifest(units)
    outputs = {}
    calls = {"query": 0, "discovery": 0}
    by_query = {query.ref.key: predicate.ref for query, predicate in queries}

    def execute(unit):
        if unit.job_kind == "QUERY":
            calls["query"] += 1
            value = executor.execute_i03(
                query_ref=unit.job_ref, predicate_ref=by_query[unit.job_ref.key],
                group_scope=scope,
            )
            result_refs = tuple(fact.ref for fact in value.facts)
        else:
            calls["discovery"] += 1
            value = executor.execute_i05(
                discovery_authority_ref=unit.job_ref, group_scope=scope,
            )
            result_refs = tuple(receipt.ref for receipt in value.receipts)
        outputs[unit.unit_hash] = value
        return ExecutionOutcome(result_refs, (release_ref,))

    digest = semantic_hash({"test": "PYAT_R3_S2E_A_BATCH", "source": release_ref.as_dict()})
    executor_ref = ExactRef(
        "PYAT_S2E_TEST_ONLY_EXECUTOR", "urn:test:s2e:batch:" + digest, digest,
    )
    runner = BatchExecutionRunner(repository=source["repo"], manifest=manifest)
    begin = time.perf_counter()
    runner.run(executors={
        "QUERY": ExecutorBinding(executor_ref, execute),
        "DISCOVERY": ExecutorBinding(executor_ref, execute),
    })
    elapsed = time.perf_counter() - begin
    census = census_native_batch(
        manifest, runner.receipts, outputs, require_complete=True,
        runtime_catalog=catalog,
    )
    assert calls == {"query": 4, "discovery": 1}
    return manifest, runner.receipts, outputs, census, elapsed, calls


def test_a_one_shared_native_batch_executes_all_f1_f4_and_i05_f3():
    case = _native_case()
    with I03GroupedExecutionScope() as grouped:
        manifest, receipts, outputs, shared, cold_s, counts = _batch(case, scope=grouped)
        group_stats = grouped.receipt()
    forced_native = I03GroupedExecutionScope()
    forced_native.close()
    _manifest, _receipts, _outputs, independent, repeat_s, _calls = _batch(
        case, scope=forced_native,
    )
    require_same_native_output_graph(shared, independent)
    assert shared.declared_domain_verified
    assert shared.complete and shared.unit_count == 5
    assert shared.completed_count == 5
    assert shared.i03_fact_count == 4
    assert shared.i05_fact_count >= 1
    assert shared.i05_receipt_count >= 1
    assert "DISCOVERY:DISCOVERED_RESULT_SUPPORTED" in shared.typed_state_counts
    assert group_stats["core_builds"] >= 1
    assert group_stats["core_hits"] >= 1
    by_ref = {unit.job_ref.key: outputs[unit.unit_hash] for unit in manifest.units}
    source, catalog, queries, discovery = case
    f1, f2yx, f2xy, f4 = [by_ref[q.ref.key].facts[0] for q, p in queries]
    assert f1.target_topology["arity"] == 1
    assert f4.target_topology["arity"] == 3
    assert len(f4.target_topology["complete_cell_semantic_projection"]) == 8
    assert sum(
        row["raw_numerator_support"] for row in f4.target_topology["complete_cell_semantic_projection"]
    ) == len(source["respondents"])
    def cell_counts(fact):
        return {
            tuple(row["cell"]) if isinstance(row["cell"], (list, tuple)) else row["cell"]:
                row["raw_numerator_support"]
            for row in fact.target_topology["complete_cell_semantic_projection"]
        }
    # Independent manually specified oracle: all eight possible X×Y×Z
    # configurations, not reconstructed via native marginal multiplication.
    assert cell_counts(f4) == {
        ("0", "0", "0"): 5, ("0", "0", "1"): 0,
        ("0", "1", "0"): 0, ("0", "1", "1"): 1,
        ("1", "0", "0"): 0, ("1", "0", "1"): 5,
        ("1", "1", "0"): 1, ("1", "1", "1"): 0,
    }
    assert cell_counts(f1) == {"0": 10, "1": 2}
    assert f2yx.raw_denominator_support == 6
    assert f2xy.raw_denominator_support == 2
    assert cell_counts(f2yx) == {"0": 5, "1": 1}
    assert cell_counts(f2xy) == {"0": 1, "1": 1}
    assert f2yx.denominator_member_refs != f2xy.denominator_member_refs
    assert len(by_ref[discovery.ref.key].receipts) == shared.i05_receipt_count
    # This is exact sourcefree case evidence, NOT a 100k process-tree cap test.
    print("S2E_NATIVE_RESOURCE_JSON=" + json.dumps({
        "schema": "PYAT_S2E_SOURCEFREE_NATIVE_RESOURCE@1",
        "universe_respondents": len(source["respondents"]),
        "full_domain_cell_count_f4": 8,
        "source_opens_during_batch": 0,
        "logical_source_release_reused": 1,
        "native_batch_units": 5,
        "query_calls": counts["query"],
        "discovery_calls": counts["discovery"],
        "shared_core_builds": group_stats["core_builds"],
        "shared_core_hits": group_stats["core_hits"],
        "grouped_seconds": round(cold_s, 6),
        "independent_seconds": round(repeat_s, 6),
        "process_maxrss_kib": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        "process_tree_maxrss_kib": None,
        "saved_store_bytes": None,
        "integrated_100k_cap": "NOT_RUN_S2_D_DEPENDENCY",
        "graph_sha256": shared.full_output_sha256,
    }, sort_keys=True))


def test_a_one_batch_lost_i05_receipt_ref_is_red_even_at_same_count():
    case = _native_case()
    with I03GroupedExecutionScope() as grouped:
        manifest, receipts, outputs, census, _cold, _calls = _batch(case, scope=grouped)
    discovery_unit = next(unit for unit in manifest.units if unit.job_kind == "DISCOVERY")
    original = outputs[discovery_unit.unit_hash]
    assert original.receipts
    # Remove one receipt preimage; the unchanged Batch receipt/result_refs and
    # candidate count must prevent loss from being called complete.
    from dataclasses import replace
    broken = replace(original, receipts=original.receipts[1:])
    with pytest.raises(S2EOutputConservationError):
        census_native_batch(
            manifest, receipts,
            {**outputs, discovery_unit.unit_hash: broken}, require_complete=True,
            runtime_catalog=case[1],
        )
    good = census_native_batch(
        manifest, receipts, outputs, require_complete=True,
        runtime_catalog=case[1],
    )
    require_same_native_output_graph(census, good)


def test_a_rehashed_f4_domain_hole_with_rehashed_completed_receipt_is_red():
    """A zero cell can be deleted without changing totals; published query says no."""
    from dataclasses import replace
    from rawlsing_next.pre553_empirical_objects import EmpiricalFact

    case = _native_case()
    with I03GroupedExecutionScope() as scope:
        manifest, receipts, outputs, original, _elapsed, _calls = _batch(case, scope=scope)
    query_unit = next(
        unit for unit in manifest.units
        if unit.job_kind == "QUERY"
        and len(next(q for q, p in case[2] if q.ref == unit.job_ref).target_refs) == 3
    )
    original_result = outputs[query_unit.unit_hash]
    fact = original_result.facts[0]
    fields = dict(fact.semantic_fields)
    topology = dict(fields["target_topology"])
    cells = list(topology["complete_cell_semantic_projection"])
    assert len(cells) == 8 and any(row["raw_numerator_support"] == 0 for row in cells)
    missing_zero_cell = next(i for i, row in enumerate(cells) if row["raw_numerator_support"] == 0)
    cells.pop(missing_zero_cell)
    topology["complete_cell_semantic_projection"] = cells
    fields["target_topology"] = topology
    # A self-consistent replacement object, not merely field corruption.
    tampered_fact = EmpiricalFact(
        typed_state=fact.typed_state,
        authority_snapshot_refs=fact.authority_snapshot_refs,
        dependency_refs=fact.dependency_refs,
        producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
        **fields,
    )
    assert tampered_fact.ref != fact.ref
    altered_result = replace(original_result, facts=(tampered_fact,))
    altered_receipts = tuple(
        replace(r, result_refs=(tampered_fact.ref,))
        if r.unit_ref == query_unit.unit_ref else r
        for r in receipts
    )
    # All other counts and Batch references remain self-consistent. The source
    # query's exact declared 8-cell domain still falsifies the manufactured 7.
    with pytest.raises(S2EOutputConservationError, match="S2E_INCOMPLETE_OR_FOREIGN_DECLARED_DOMAIN"):
        census_native_batch(
            manifest, altered_receipts,
            {**outputs, query_unit.unit_hash: altered_result},
            require_complete=True, runtime_catalog=case[1],
        )
    good = census_native_batch(
        manifest, receipts, outputs,
        require_complete=True, runtime_catalog=case[1],
    )
    require_same_native_output_graph(original, good)
