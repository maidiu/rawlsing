"""R03 independent early-miss capacity gate checks; reviewer-authored."""
from __future__ import annotations

import json
import sys
from dataclasses import replace
from pathlib import Path

ROOT = Path(__file__).resolve()
while not (ROOT / "rawlsing_next").is_dir():
    if ROOT.parent == ROOT:
        raise RuntimeError("repo root not found")
    ROOT = ROOT.parent
sys.path.insert(0, str(ROOT))

from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_empirical_objects import EmpiricalQuerySpec
from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope
from rawlsing_next.tests.test_pre553_i03_grouping import _executor, _main_data
from rawlsing_next.tests.test_pre553_empirical_query import (
    _astra_query_authority,
    _branch_predicate,
    _build_source,
    _query,
)
import rawlsing_next.pre553_empirical_query as empirical_query


def _run_scope(executor, op, scope):
    return executor.execute_i03(
        query_ref=op["query"].ref,
        predicate_ref=op["predicate"].ref,
        group_scope=scope,
    ).facts[0]


def _run_no_scope(source, catalog, op):
    return _executor(source, catalog).execute_i03(
        query_ref=op["query"].ref,
        predicate_ref=op["predicate"].ref,
    ).facts[0]


def main():
    source, ops, catalog = _main_data("r03-early-gate")
    by_id = {op["op_id"]: op for op in ops}
    op_a = by_id["all_K_raw"]
    op_b = by_id["all_X_raw"]
    baseline_a = _run_no_scope(source, catalog, op_a)
    baseline_b = _run_no_scope(source, catalog, op_b)

    scope = I03GroupedExecutionScope(max_groups=1)
    executor = _executor(source, catalog)
    fill = _run_scope(executor, op_a, scope)
    hit = _run_scope(executor, op_a, scope)
    assert fill.as_dict() == baseline_a.as_dict()
    assert hit.as_dict() == baseline_a.as_dict()
    receipt_fill_hit = dict(scope.receipt())
    assert receipt_fill_hit["core_builds"] == 1
    assert receipt_fill_hit["core_hits"] == 1
    assert receipt_fill_hit["core_build_attempts"] == 1
    assert receipt_fill_hit["early_capacity_fallbacks"] == 0
    assert receipt_fill_hit["capacity_fallbacks"] == 0

    calls = {"count": 0}
    original = empirical_query._evaluate_index_group_core

    def counted(*args, **kwargs):
        calls["count"] += 1
        return original(*args, **kwargs)

    empirical_query._evaluate_index_group_core = counted
    try:
        early_miss = _run_scope(executor, op_b, scope)
    finally:
        empirical_query._evaluate_index_group_core = original
    assert calls["count"] == 0
    assert early_miss.as_dict() == baseline_b.as_dict()
    receipt_early_miss = dict(scope.receipt())
    assert receipt_early_miss["core_build_attempts"] == 1
    assert receipt_early_miss["core_builds"] == 1
    assert receipt_early_miss["core_hits"] == 1
    assert receipt_early_miss["early_capacity_fallbacks"] == 1
    assert receipt_early_miss["capacity_fallbacks"] == 1

    restored_hit = _run_scope(executor, op_a, scope)
    assert restored_hit.as_dict() == baseline_a.as_dict()
    receipt_restored = dict(scope.receipt())
    assert receipt_restored["core_hits"] == 2
    assert receipt_restored["early_capacity_fallbacks"] == 1
    assert receipt_restored["capacity_fallbacks"] == 1

    # Authority refusal with the scope already at group capacity: the normal
    # pre-check/negative path must still run and the scope must not be touched.
    denied_source = _build_source(
        "r03-early-deny", [{"id": "R1", "responses": {"Y": 1}}],
    )
    denied_qa = _astra_query_authority("r03-early-deny", state="DENY")
    denied_predicate = _branch_predicate(denied_source, denied_qa, tag="r03-early-deny")
    denied_query = _query(denied_source, denied_qa, denied_predicate, ("Y",), tag="r03-early-deny")
    denied_catalog = RuntimeObjectCatalog(
        authorities=tuple((*denied_source["authorities"], denied_qa)),
        predicates=(denied_predicate,), queries=(denied_query,),
        discovery_authorities=(),
    )
    denied_baseline = _executor(denied_source, denied_catalog).execute_i03(
        query_ref=denied_query.ref, predicate_ref=denied_predicate.ref,
    ).facts[0]
    denied_scope_before = dict(scope.receipt())
    denied_with_scope = _executor(denied_source, denied_catalog).execute_i03(
        query_ref=denied_query.ref, predicate_ref=denied_predicate.ref,
        group_scope=scope,
    ).facts[0]
    assert denied_with_scope.as_dict() == denied_baseline.as_dict()
    assert denied_with_scope.typed_state == "UNAVAILABLE"
    assert denied_with_scope.p02_failure_state == "MISSING_REQUIRED_AUTHORITY"
    assert dict(scope.receipt()) == denied_scope_before

    # Unsupported topology refusal with the same full scope.
    unsupported_base = op_a["query"]
    fields = dict(unsupported_base.semantic_fields)
    topology = dict(fields["target_arity_and_topology"])
    components = [dict(component) for component in topology["components"]]
    components[0]["topology"] = "LOSSY_UNKNOWN_TOPOLOGY"
    topology["components"] = components
    fields["target_arity_and_topology"] = topology
    unsupported_query = EmpiricalQuerySpec(
        typed_state=unsupported_base.typed_state,
        authority_snapshot_refs=unsupported_base.authority_snapshot_refs,
        dependency_refs=unsupported_base.dependency_refs,
        producer_replay_locator_or_reference_root=(
            unsupported_base.producer_replay_locator_or_reference_root
        ),
        **fields,
    )
    unsupported_catalog = RuntimeObjectCatalog(
        authorities=catalog.authorities,
        predicates=(op_a["predicate"],), queries=(unsupported_query,),
        discovery_authorities=(),
    )
    unsupported_baseline = _executor(source, unsupported_catalog).execute_i03(
        query_ref=unsupported_query.ref, predicate_ref=op_a["predicate"].ref,
    ).facts[0]
    unsupported_scope_before = dict(scope.receipt())
    unsupported_with_scope = _executor(source, unsupported_catalog).execute_i03(
        query_ref=unsupported_query.ref, predicate_ref=op_a["predicate"].ref,
        group_scope=scope,
    ).facts[0]
    assert unsupported_with_scope.as_dict() == unsupported_baseline.as_dict()
    assert unsupported_with_scope.typed_state == "UNRESOLVED"
    assert unsupported_with_scope.p02_failure_state == "UNSUPPORTED_RESPONSE_TOPOLOGY"
    assert dict(scope.receipt()) == unsupported_scope_before

    # Measure/refusal after an actual early miss: a different target plan with
    # W2 weighted measure and no W2 weights must take the early fallback and
    # still run the unshared weight validation/negative path.
    w2_base = op_b["query"]
    w2_fields = dict(w2_base.semantic_fields)
    w2_grain = dict(w2_fields["requested_output_grain"])
    w2_grain["measure_kind"] = "GOVERNED_WEIGHTED"
    w2_grain["weight_basis_id"] = "W2"
    w2_fields["requested_output_grain"] = w2_grain
    w2_query = EmpiricalQuerySpec(
        typed_state=w2_base.typed_state,
        authority_snapshot_refs=w2_base.authority_snapshot_refs,
        dependency_refs=w2_base.dependency_refs,
        producer_replay_locator_or_reference_root=(
            w2_base.producer_replay_locator_or_reference_root
        ),
        **w2_fields,
    )
    w2_catalog = RuntimeObjectCatalog(
        authorities=catalog.authorities,
        predicates=(op_b["predicate"],), queries=(w2_query,),
        discovery_authorities=(),
    )
    w2_baseline = _executor(source, w2_catalog).execute_i03(
        query_ref=w2_query.ref, predicate_ref=op_b["predicate"].ref,
    ).facts[0]
    w2_scope_before = dict(scope.receipt())
    w2_with_scope = _executor(source, w2_catalog).execute_i03(
        query_ref=w2_query.ref, predicate_ref=op_b["predicate"].ref,
        group_scope=scope,
    ).facts[0]
    assert w2_with_scope.as_dict() == w2_baseline.as_dict()
    assert w2_with_scope.typed_state == "UNAVAILABLE"
    assert w2_with_scope.p02_failure_state == "MEASURE_UNAVAILABLE"
    w2_scope_after = dict(scope.receipt())
    assert w2_scope_after["early_capacity_fallbacks"] == (
        w2_scope_before["early_capacity_fallbacks"] + 1
    )
    assert w2_scope_after["capacity_fallbacks"] == (
        w2_scope_before["capacity_fallbacks"] + 1
    )
    assert w2_scope_after["core_build_attempts"] == w2_scope_before["core_build_attempts"]

    # Member cap already exhausted: no new core builder.
    member_scope = I03GroupedExecutionScope(max_cached_members=1, max_groups=4)
    minority = by_id["minority_branch_target_K"]
    minority_baseline = _run_no_scope(source, catalog, minority)
    minority_fill = _run_scope(executor, minority, member_scope)
    assert minority_fill.as_dict() == minority_baseline.as_dict()
    member_before = dict(member_scope.receipt())
    assert member_before["core_builds"] == 1
    assert member_before["early_capacity_fallbacks"] == 0
    calls["count"] = 0
    empirical_query._evaluate_index_group_core = counted
    try:
        member_miss = _run_scope(executor, op_b, member_scope)
    finally:
        empirical_query._evaluate_index_group_core = original
    assert calls["count"] == 0
    assert member_miss.as_dict() == baseline_b.as_dict()
    member_after = dict(member_scope.receipt())
    assert member_after["core_builds"] == 1
    assert member_after["early_capacity_fallbacks"] == 1
    assert member_after["capacity_fallbacks"] == 1

    # Unknown prospective member size: early guard must not trigger; the
    # existing post-build member fallback remains and is honest.
    unknown_scope = I03GroupedExecutionScope(max_cached_members=1)
    unknown_first = _run_scope(executor, op_a, unknown_scope)
    assert unknown_first.as_dict() == baseline_a.as_dict()
    unknown_first_receipt = dict(unknown_scope.receipt())
    assert unknown_first_receipt["core_build_attempts"] == 1
    assert unknown_first_receipt["core_builds"] == 0
    assert unknown_first_receipt["early_capacity_fallbacks"] == 0
    assert unknown_first_receipt["capacity_fallbacks"] == 1
    unknown_second = _run_scope(executor, op_a, unknown_scope)
    assert unknown_second.as_dict() == baseline_a.as_dict()
    unknown_second_receipt = dict(unknown_scope.receipt())
    assert unknown_second_receipt["core_build_attempts"] == 2
    assert unknown_second_receipt["core_builds"] == 0
    assert unknown_second_receipt["early_capacity_fallbacks"] == 0
    assert unknown_second_receipt["capacity_fallbacks"] == 2

    scope.close()
    closed_receipt = dict(scope.receipt())
    assert closed_receipt["closed"] is True
    assert closed_receipt["open_groups"] == 0

    payload = {
        "schema": "R03_EARLY_MISS_GATE@1",
        "implementation_sha": "9a5cfd2aba62b3e320aa4fd4a85c689eb4649bd3",
        "fill_hit_receipt": receipt_fill_hit,
        "early_miss_receipt": receipt_early_miss,
        "restored_hit_receipt": receipt_restored,
        "early_miss_core_builder_calls": 0,
        "early_miss_fact_equal": True,
        "restored_hit_fact_equal": True,
        "authority_deny_fact_equal": True,
        "authority_deny_typed_state": denied_with_scope.typed_state,
        "authority_deny_p02": denied_with_scope.p02_failure_state,
        "unsupported_topology_fact_equal": True,
        "unsupported_topology_typed_state": unsupported_with_scope.typed_state,
        "unsupported_topology_p02": unsupported_with_scope.p02_failure_state,
        "w2_early_miss_fact_equal": True,
        "w2_early_miss_typed_state": w2_with_scope.typed_state,
        "w2_early_miss_p02": w2_with_scope.p02_failure_state,
        "w2_early_miss_scope_before": w2_scope_before,
        "w2_early_miss_scope_after": w2_scope_after,
        "member_exhausted_before": member_before,
        "member_exhausted_after": member_after,
        "unknown_prospective_first": unknown_first_receipt,
        "unknown_prospective_second": unknown_second_receipt,
        "scope_close": closed_receipt,
        "all_pass": True,
    }
    out = ROOT / ".local-logs/pyat-l03-r03/early_miss_gate.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=1, sort_keys=True))
    print(json.dumps({
        "all_pass": True,
        "early_miss_receipt": receipt_early_miss,
        "member_after": member_after,
        "unknown_first": unknown_first_receipt,
    }, indent=1, sort_keys=True))


if __name__ == "__main__":
    main()
