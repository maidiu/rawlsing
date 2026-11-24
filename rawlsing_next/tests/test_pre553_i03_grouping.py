"""Focused sourcefree tests for finite execution-local I03 grouped reuse."""
from __future__ import annotations

from dataclasses import replace
from types import MappingProxyType

import pytest

from rawlsing_next._pre553_query_common import _parse_target_plan, _profile
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_carrier_execution import (
    CarrierNeutralResearchExecutor,
    RuntimeObjectCatalog,
)
from rawlsing_next.pre553_c11_integrity import TYPED_ABSENCE_STATES
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalQuerySpec,
    ExactRef,
    semantic_hash,
)
from rawlsing_next import pre553_empirical_query as empirical_query
from rawlsing_next.pre553_empirical_query import I03GroupedExecutionScope, execute_empirical_query
from rawlsing_next._pre553_query_eval import _group_core_fingerprint
from rawlsing_next.pre553_runtime_authority import Pre553RuntimeAuthoritySet
from rawlsing_next.pre553_runtime_context import bind_runtime
from rawlsing_next.tests.pre553_query_frontier_fixtures import (
    _custom_query,
    special_state_fixture,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _astra_query_authority,
    _auth,
    _branch_predicate,
    _build_source,
    _predicate,
    _query,
    _query_authority,
    _ref,
    _response_leaf,
)
from rawlsing_next.tests.test_pre553_route_b_production import _fixture as route_b_fixture
from rawlsing_next.pre553_issued_workload import (
    DESCRIPTOR_FIELDS,
    IssuedWorkloadRecord,
    NativeWorkload,
    canonical as issued_canonical,
    execute_issued_workload,
)
from rawlsing_next.pre553_native_workload_binding import TestOnlyDecisionResolver


def _main_data(tag: str, n: int = 24):
    rows = []
    weights = {}
    ids = []
    questions = ("A", "B", "C", "K", "X", "Y", "Z", "U")
    for i in range(n):
        a = i & 1
        b = (i >> 1) & 1
        c = (i >> 2) & 1
        x = a
        y = b
        z = x ^ y
        u = c
        k = a ^ b ^ c
        rid = f"R{i:06d}"
        ids.append(rid)
        rows.append({
            "id": rid,
            "responses": {"A": a, "B": b, "C": c, "K": k, "X": x, "Y": y, "Z": z, "U": u},
            "coords": {"G": "A" if i % 3 == 0 else "B"},
        })
        weights[rid] = ("WEIGHT_VALID_AUTHORIZED", str(1 + (i % 4)))
    risk_sets = {
        "R": {q: set(ids) for q in questions},
        "S": {q: {rid for index, rid in enumerate(ids) if index % 2 == 0} for q in questions},
    }
    source = _build_source(tag, rows, risk_sets=risk_sets, weights=weights)
    qa = _query_authority(tag)
    all_p = _branch_predicate(source, qa, tag=f"{tag}-all")
    minority_p = _branch_predicate(
        source, qa, members=tuple(list(source["respondents"].values())[: max(1, n // 100)]),
        tag=f"{tag}-minority",
    )
    x1 = _predicate(source, qa, _response_leaf(source, qa, "X", 1), tag=f"{tag}-x1")
    y1 = _predicate(source, qa, _response_leaf(source, qa, "Y", 1), tag=f"{tag}-y1")
    x_leaf = _response_leaf(source, qa, "X", 1)
    y_leaf = _response_leaf(source, qa, "Y", 1)
    xor_p = _predicate(
        source, qa,
        {"op": "AND", "children": [
            {"op": "OR", "children": [x_leaf, y_leaf]},
            {"op": "NOT", "children": [{"op": "AND", "children": [x_leaf, y_leaf]}]},
        ]},
        tag=f"{tag}-xor",
    )
    specs = [
        ("all_K_raw", all_p, ("K",), "R", "RAW", f"{tag}-allKr"),
        ("all_K_weighted", all_p, ("K",), "R", "GOVERNED_WEIGHTED", f"{tag}-allKw"),
        ("all_K_raw_sibling", all_p, ("K",), "R", "RAW", f"{tag}-allKr2"),
        ("all_X_raw", all_p, ("X",), "R", "RAW", f"{tag}-allXr"),
        ("all_Z_raw", all_p, ("Z",), "R", "RAW", f"{tag}-allZr"),
        ("all_XY_raw", all_p, ("X", "Y"), "R", "RAW", f"{tag}-allXYr"),
        ("all_XYZ_raw", all_p, ("X", "Y", "Z"), "R", "RAW", f"{tag}-allXYZr"),
        ("all_ABCK_raw", all_p, ("A", "B", "C", "K"), "R", "RAW", f"{tag}-allABCKr"),
        ("cond_X1_target_Y", x1, ("Y",), "R", "RAW", f"{tag}-x1Y"),
        ("cond_Y1_target_X", y1, ("X",), "R", "RAW", f"{tag}-y1X"),
        ("xor_condition_target_Z", xor_p, ("Z",), "R", "RAW", f"{tag}-xorZ"),
        ("minority_branch_target_K", minority_p, ("K",), "R", "RAW", f"{tag}-minK"),
        ("risk_S_target_K", all_p, ("K",), "S", "RAW", f"{tag}-riskSK"),
    ]
    ops = []
    for op_id, predicate, targets, risk, measure, query_tag in specs:
        ops.append({
            "op_id": op_id,
            "predicate": predicate,
            "query": _query(source, qa, predicate, targets, risk=risk, measure=measure, tag=query_tag),
        })
    predicates = []
    for predicate in (all_p, minority_p, x1, y1, xor_p):
        if all(predicate.ref != existing.ref for existing in predicates):
            predicates.append(predicate)
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qa)),
        predicates=tuple(predicates),
        queries=tuple(op["query"] for op in ops),
        discovery_authorities=(),
    )
    return source, ops, catalog


def _executor(source, catalog, release=None):
    release = release or source["repo"].resolve_release_exact(source["release_ref"])
    return CarrierNeutralResearchExecutor(
        C11Repository((release,)), (release.release_ref,), catalog,
    )


def _run(executor, ops, scope=None):
    return {
        op["op_id"]: executor.execute_i03(
            query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
            group_scope=scope,
        )
        for op in ops
    }


def _material(results):
    return {
        op_id: tuple(fact.as_dict() for fact in result.facts)
        for op_id, result in results.items()
    }


def _facts_equal(left, right):
    assert set(left) == set(right)
    for op_id in left:
        assert tuple(f.as_dict() for f in left[op_id].facts) == tuple(
            f.as_dict() for f in right[op_id].facts
        )
        assert tuple(f.ref for f in left[op_id].facts) == tuple(
            f.ref for f in right[op_id].facts
        )
        assert tuple(f.replay_ref for f in left[op_id].facts) == tuple(
            f.replay_ref for f in right[op_id].facts
        )
        assert left[op_id].query_ref == right[op_id].query_ref
        assert left[op_id].release_refs == right[op_id].release_refs


def test_grouped_scope_exact_parity_and_actual_core_sharing():
    source, ops, catalog = _main_data("grouped-main")
    baseline = _run(_executor(source, catalog), ops)
    scope = I03GroupedExecutionScope()
    candidate = _run(_executor(source, catalog), ops, scope)
    _facts_equal(baseline, candidate)
    receipt = scope.receipt()
    assert receipt["core_builds"] == 11
    assert receipt["core_hits"] == 2
    assert receipt["fallbacks"] == 0
    assert receipt["open_groups"] == 11
    assert receipt["raw_materializations"] == 12
    assert receipt["weighted_materializations"] == 1
    scope.close()
    assert scope.receipt()["closed"] is True
    assert scope.receipt()["open_groups"] == 0


def test_grouped_scope_shares_only_exact_compatible_keys():
    source, ops, catalog = _main_data("grouped-keys")
    by_id = {op["op_id"]: op for op in ops}

    def receipt_for(*op_ids):
        scope = I03GroupedExecutionScope()
        executor = _executor(source, catalog)
        for op_id in op_ids:
            op = by_id[op_id]
            executor.execute_i03(
                query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
                group_scope=scope,
            )
        return scope.receipt()

    assert receipt_for("all_K_raw", "all_K_weighted", "all_K_raw_sibling")["core_hits"] == 2
    for group in (
        ("all_K_raw", "all_X_raw"),
        ("all_K_raw", "risk_S_target_K"),
        ("all_K_raw", "xor_condition_target_Z"),
        ("cond_X1_target_Y", "cond_Y1_target_X"),
        ("all_XY_raw", "all_XYZ_raw"),
        ("all_K_raw", "all_ABCK_raw"),
    ):
        receipt = receipt_for(*group)
        assert receipt["core_builds"] == 2
        assert receipt["core_hits"] == 0
        assert receipt["fallbacks"] == 0


def test_grouped_scope_weighted_first_then_raw_still_exact():
    source, ops, catalog = _main_data("grouped-order")
    by_id = {op["op_id"]: op for op in ops}
    ordered = [by_id[name] for name in ("all_K_weighted", "all_K_raw", "all_K_raw_sibling")]
    baseline = _run(_executor(source, catalog), ordered)
    scope = I03GroupedExecutionScope()
    candidate = _run(_executor(source, catalog), ordered, scope)
    _facts_equal(baseline, candidate)
    receipt = scope.receipt()
    assert receipt["core_builds"] == 1
    assert receipt["core_hits"] == 2
    assert receipt["weighted_materializations"] == 1
    assert receipt["raw_materializations"] == 2


def test_grouped_scope_special_states_zero_support_and_unsupported_topology():
    source, baseline_fact, event_states, routing_states = special_state_fixture()
    qa = _query_authority("r12-special")
    predicate = _branch_predicate(source, qa, tag="all")
    domain = [
        "1",
        {"typed_response_state": "MISSING"}, {"typed_response_state": "DK"},
        {"typed_response_state": "REFUSAL"}, {"typed_response_state": "IAP"},
        {"typed_response_state": "NOT_ASKED"},
    ]
    query = _custom_query(
        source, qa, predicate, "Q", topology="SCALAR_SINGULAR", domain=domain,
        included_states=("SUBSTANTIVE_RESPONSE", "MISSING", "DK", "REFUSAL", "IAP", "NOT_ASKED"),
        tag="group-special",
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qa)),
        predicates=(predicate,), queries=(query,), discovery_authorities=(),
    )
    release = source["repo"].resolve_release_exact(source["release_ref"])
    baseline = _executor(source, catalog, release).execute_i03(
        query_ref=query.ref, predicate_ref=predicate.ref,
    )
    scope = I03GroupedExecutionScope()
    candidate = _executor(source, catalog, release).execute_i03(
        query_ref=query.ref, predicate_ref=predicate.ref, group_scope=scope,
    )
    assert candidate.facts[0].as_dict() == baseline.facts[0].as_dict()
    assert (
        candidate.facts[0].target_topology["complete_cell_semantic_projection"]
        == baseline_fact.target_topology["complete_cell_semantic_projection"]
    )
    assert candidate.facts[0].raw_denominator_support == baseline_fact.raw_denominator_support
    assert candidate.facts[0].typed_state == baseline_fact.typed_state == "SUPPORTED"
    assert scope.receipt()["core_builds"] == 1

    zero_source, zero_ops, zero_catalog = _main_data("grouped-zero")
    zero_op = zero_ops[0]
    empty_predicate = _branch_predicate(
        zero_source, _query_authority("grouped-zero"), members=(),
        tag="grouped-zero-empty",
    )
    empty_query = _query(
        zero_source, _query_authority("grouped-zero"), empty_predicate, ("K",),
        tag="grouped-zero-empty-query",
    )
    zero_catalog = RuntimeObjectCatalog(
        authorities=tuple((*zero_source["authorities"], _query_authority("grouped-zero"))),
        predicates=(empty_predicate,), queries=(empty_query,), discovery_authorities=(),
    )
    baseline = _executor(zero_source, zero_catalog).execute_i03(
        query_ref=empty_query.ref, predicate_ref=empty_predicate.ref,
    )
    scope = I03GroupedExecutionScope()
    candidate = _executor(zero_source, zero_catalog).execute_i03(
        query_ref=empty_query.ref, predicate_ref=empty_predicate.ref, group_scope=scope,
    )
    assert candidate.facts[0].as_dict() == baseline.facts[0].as_dict()
    assert candidate.facts[0].typed_state == "ZERO_SUPPORT"
    assert scope.receipt()["core_builds"] == 1

    unsupported_source = _build_source("grouped-unsupported", [{"id": "R1", "responses": {"Y": 1}}])
    qa = _query_authority("grouped-unsupported")
    predicate = _branch_predicate(unsupported_source, qa, tag="grouped-unsupported")
    base = _query(unsupported_source, qa, predicate, ("Y",), tag="grouped-unsupported")
    fields = dict(base.semantic_fields)
    topology = dict(fields["target_arity_and_topology"])
    components = [dict(component) for component in topology["components"]]
    components[0]["topology"] = "LOSSY_UNKNOWN_TOPOLOGY"
    topology["components"] = components
    fields["target_arity_and_topology"] = topology
    unsupported = EmpiricalQuerySpec(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
        **fields,
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*unsupported_source["authorities"], qa)),
        predicates=(predicate,), queries=(unsupported,), discovery_authorities=(),
    )
    baseline = _executor(unsupported_source, catalog).execute_i03(
        query_ref=unsupported.ref, predicate_ref=predicate.ref,
    )
    scope = I03GroupedExecutionScope()
    candidate = _executor(unsupported_source, catalog).execute_i03(
        query_ref=unsupported.ref, predicate_ref=predicate.ref, group_scope=scope,
    )
    assert candidate.facts[0].as_dict() == baseline.facts[0].as_dict()
    assert candidate.facts[0].typed_state == "UNRESOLVED"
    assert candidate.facts[0].p02_failure_state == "UNSUPPORTED_RESPONSE_TOPOLOGY"
    assert scope.receipt()["core_builds"] == 0
    assert scope.receipt()["open_groups"] == 0
    assert "NOT_ADMINISTERED" not in TYPED_ABSENCE_STATES
    assert event_states == ("DK", "IAP", "MISSING", "NOT_ASKED", "REFUSAL", "SUBSTANTIVE_RESPONSE")
    assert routing_states == ("ELIGIBLE_APPLICABLE", "INAPPLICABLE", "NOT_ASKED")


def test_grouped_scope_poisoned_memo_and_index_rebuild_never_publish_wrong_fact():
    source, ops, catalog = _main_data("grouped-poison")
    op = ops[0]
    baseline = _executor(source, catalog).execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
    )
    executor = _executor(source, catalog)
    scope = I03GroupedExecutionScope()
    assert executor.execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
        group_scope=scope,
    ).facts[0].as_dict() == baseline.facts[0].as_dict()
    key, core = next(iter(scope._cache.items()))
    forged = replace(core, raw_cells=MappingProxyType({"0": 0, "1": 999}))
    scope._cache[key] = forged
    observed = executor.execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
        group_scope=scope,
    )
    assert observed.facts[0].as_dict() == baseline.facts[0].as_dict()
    assert scope.receipt()["fingerprint_failures"] >= 1

    rebuilt_scope = I03GroupedExecutionScope()
    executor = _executor(source, catalog)
    assert executor.execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
        group_scope=rebuilt_scope,
    ).facts[0].as_dict() == baseline.facts[0].as_dict()
    repository = executor.repository
    index_key = next(iter(repository._i03_release_indices))
    before = repository._i03_release_indices[index_key]
    dropped = min(before.respondents)
    repository._i03_release_indices[index_key] = replace(
        before,
        respondents=MappingProxyType({
            item: value for item, value in before.respondents.items() if item != dropped
        }),
    )
    observed = executor.execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
        group_scope=rebuilt_scope,
    )
    assert observed.facts[0].as_dict() == baseline.facts[0].as_dict()
    assert repository._i03_release_indices[index_key].respondents == before.respondents
    assert rebuilt_scope.receipt()["open_groups"] == 2


def test_grouped_scope_runtime_binding_falls_back_unshared():
    source, ops, catalog = _main_data("grouped-runtime")
    op = ops[0]
    runtime = Pre553RuntimeAuthoritySet()
    with bind_runtime(runtime):
        baseline = _executor(source, catalog).execute_i03(
            query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
        )
        scope = I03GroupedExecutionScope()
        candidate = _executor(source, catalog).execute_i03(
            query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
            group_scope=scope,
        )
    assert candidate.facts[0].as_dict() == baseline.facts[0].as_dict()
    assert scope.receipt()["core_builds"] == 0
    assert scope.receipt()["core_hits"] == 0
    assert scope.receipt()["fallbacks"] >= 1


def test_grouped_scope_authority_deny_matches_unshared():
    source = _build_source("grouped-deny", [{"id": "R1", "responses": {"Y": 1}}])
    qa = _astra_query_authority("grouped-deny", state="DENY")
    predicate = _branch_predicate(source, qa, tag="grouped-deny")
    query = _query(source, qa, predicate, ("Y",), tag="grouped-deny")
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], qa)),
        predicates=(predicate,), queries=(query,), discovery_authorities=(),
    )
    baseline = _executor(source, catalog).execute_i03(
        query_ref=query.ref, predicate_ref=predicate.ref,
    )
    scope = I03GroupedExecutionScope()
    candidate = _executor(source, catalog).execute_i03(
        query_ref=query.ref, predicate_ref=predicate.ref, group_scope=scope,
    )
    assert candidate.facts[0].as_dict() == baseline.facts[0].as_dict()
    assert candidate.facts[0].typed_state == "UNAVAILABLE"
    assert candidate.facts[0].p02_failure_state == "MISSING_REQUIRED_AUTHORITY"
    assert scope.receipt()["core_builds"] == 0


def _grouped_issued_workload():
    fx = route_b_fixture()
    descriptor = {
        "source_edition": fx["projection"].expected_source_sha256,
        "native_item_ids": ["X", "Y", "O", "R"],
        "release_tag": fx["projection"].instrument_release_id,
        "routing_and_risk": {
            "routing_facts": len(fx["projection"].routing), "risk_tag": "M01",
        },
        "carrier": {
            "source_format": "SYNTHETIC_NONRESPONDENT_FIXTURE",
            "source_artifact_id": fx["projection"].source_artifact_id,
        },
        "country_and_population": {"country": "US", "population": "ADULTS"},
        "weight_design_estimand": {"weight_basis": "W", "estimand": "TEST_ONLY"},
        "missing_and_occurrence_policy": {
            "missing": "EXPLICIT_TYPED_STATES", "occurrence": "SCALAR_SINGULAR",
        },
        "target_conditioner_roles": {
            "target": "Y", "conditioner": None, "measure_kind": "BOTH",
        },
    }
    assert set(descriptor) == DESCRIPTOR_FIELDS
    workload = NativeWorkload(
        decision_ref=ExactRef("TEST_ONLY_DECISION", "urn:test:grouped-issued", "a" * 64),
        source_factory_ref=ExactRef("SOURCE_FACTORY", "urn:test:grouped-issued-source", "b" * 64),
        descriptor=issued_canonical(descriptor),
        projection=fx["projection"], catalog=fx["catalog"], requests=fx["requests"],
        discoveries=(fx["discovery_authority"].ref,),
        original_u_root="c" * 64, expected_frontier_root="d" * 64,
    )
    record = IssuedWorkloadRecord(
        decision_ref=workload.decision_ref,
        source_permission_ref=ExactRef("TEST_ONLY_SOURCE_PERMISSION", "urn:test:sp", "e" * 64),
        scientific_permission_refs=(
            ExactRef("TEST_ONLY_SCIENTIFIC_PERMISSION", "urn:test:sc", "f" * 64),
        ),
        host="h", purpose="p", source_sha256=fx["projection"].expected_source_sha256,
        envelope_sha256=semantic_hash(workload.envelope()),
        original_u_root=workload.original_u_root,
        expected_frontier_root=workload.expected_frontier_root,
        expected_jobs=tuple(
            ("QUERY", request.query_ref.key, request.predicate_ref.key)
            for request in workload.requests
        ) + tuple(("DISCOVERY", ref.key, "") for ref in workload.discoveries),
        currentness="CURRENT_GRANTED", scope="TEST_ONLY_SOURCEFREE",
    )
    return fx, workload, TestOnlyDecisionResolver(record)


def _issued_material(result):
    return (
        tuple(ref.as_dict() for ref in result.output_refs),
        tuple(sorted(receipt.state for receipt in result.receipts)),
        tuple(
            (
                "I03",
                tuple(fact.as_dict() for fact in output.facts),
            ) if hasattr(output, "facts") else (
                "I05",
                tuple(receipt.as_dict() for receipt in output.receipts),
                output.coverage_claim,
            )
            for output in result.native_outputs
        ),
    )


def test_issued_batch_and_i05_actually_use_grouped_scope():
    fx, workload, resolver = _grouped_issued_workload()
    closed_scope = I03GroupedExecutionScope()
    closed_scope.close()
    baseline = execute_issued_workload(
        workload, resolver, source_factory=lambda _ref: fx["stream"],
        host="h", purpose="p", allow_test_only=True, group_scope=closed_scope,
    )
    scope = I03GroupedExecutionScope()
    candidate = execute_issued_workload(
        workload, resolver, source_factory=lambda _ref: fx["stream"],
        host="h", purpose="p", allow_test_only=True, group_scope=scope,
    )
    assert _issued_material(candidate) == _issued_material(baseline)
    receipt = scope.receipt()
    assert receipt["core_builds"] >= 2
    assert receipt["core_hits"] >= 2
    assert receipt["fallbacks"] == 0
    assert closed_scope.receipt()["core_builds"] == 0
    assert closed_scope.receipt()["fallbacks"] >= 3


def test_grouped_scope_release_separation_and_cleanup_on_error():
    source_a, ops_a, catalog_a = _main_data("grouped-release-a")
    source_b, ops_b, catalog_b = _main_data("grouped-release-b")
    release_a = source_a["repo"].resolve_release_exact(source_a["release_ref"])
    release_b = source_b["repo"].resolve_release_exact(source_b["release_ref"])
    repository = C11Repository((release_a, release_b))
    executor_a = CarrierNeutralResearchExecutor(repository, (release_a.release_ref,), catalog_a)
    executor_b = CarrierNeutralResearchExecutor(repository, (release_b.release_ref,), catalog_b)
    scope = I03GroupedExecutionScope()
    op_a, op_b = ops_a[0], ops_b[0]
    fact_a = executor_a.execute_i03(
        query_ref=op_a["query"].ref, predicate_ref=op_a["predicate"].ref, group_scope=scope,
    ).facts[0]
    fact_b = executor_b.execute_i03(
        query_ref=op_b["query"].ref, predicate_ref=op_b["predicate"].ref, group_scope=scope,
    ).facts[0]
    assert fact_a.ref != fact_b.ref
    assert scope.receipt()["core_builds"] == 2
    assert scope.receipt()["core_hits"] == 0
    try:
        with scope:
            executor_a.execute_i03(
                query_ref=op_a["query"].ref, predicate_ref=op_a["predicate"].ref,
                group_scope=scope,
            )
            raise RuntimeError("test-only scope error")
    except RuntimeError:
        pass
    assert scope.receipt()["closed"] is True
    assert scope.receipt()["open_groups"] == 0


def test_grouped_scope_weight_negatives_and_regime_isolation():
    bad_source = _build_source(
        "grouped-bad-weight",
        [{"id": "R1", "responses": {"Y": 1}}, {"id": "R2", "responses": {"Y": 0}}],
        weights={"R1": ("WEIGHT_VALID_AUTHORIZED", "1"), "R2": ("WEIGHT_MISSING", "0")},
    )
    qa = _query_authority("grouped-bad-weight")
    predicate = _branch_predicate(bad_source, qa, tag="grouped-bad-weight")
    query = _query(
        bad_source, qa, predicate, ("Y",), measure="GOVERNED_WEIGHTED",
        tag="grouped-bad-weight",
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*bad_source["authorities"], qa)),
        predicates=(predicate,), queries=(query,), discovery_authorities=(),
    )
    baseline = _executor(bad_source, catalog).execute_i03(
        query_ref=query.ref, predicate_ref=predicate.ref,
    )
    scope = I03GroupedExecutionScope()
    candidate = _executor(bad_source, catalog).execute_i03(
        query_ref=query.ref, predicate_ref=predicate.ref, group_scope=scope,
    )
    assert candidate.facts[0].as_dict() == baseline.facts[0].as_dict()
    assert candidate.facts[0].typed_state == "UNAVAILABLE"
    assert candidate.facts[0].p02_failure_state == "MEASURE_UNAVAILABLE"
    assert scope.receipt()["core_builds"] == 1
    assert scope.receipt()["fallbacks"] >= 1

    source, ops, catalog = _main_data("grouped-weight-basis")
    op = ops[0]
    weighted = _query(
        source, _query_authority("grouped-weight-basis"), op["predicate"],
        ("K",), measure="GOVERNED_WEIGHTED", tag="grouped-weight-basis-w2",
    )
    fields = dict(weighted.semantic_fields)
    grain = dict(fields["requested_output_grain"])
    grain["weight_basis_id"] = "W2"
    fields["requested_output_grain"] = grain
    weighted_w2 = EmpiricalQuerySpec(
        typed_state=weighted.typed_state,
        authority_snapshot_refs=weighted.authority_snapshot_refs,
        dependency_refs=weighted.dependency_refs,
        producer_replay_locator_or_reference_root=weighted.producer_replay_locator_or_reference_root,
        **fields,
    )
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], _query_authority("grouped-weight-basis"))),
        predicates=(op["predicate"],), queries=(weighted_w2,), discovery_authorities=(),
    )
    baseline = _executor(source, catalog).execute_i03(
        query_ref=weighted_w2.ref, predicate_ref=op["predicate"].ref,
    )
    scope = I03GroupedExecutionScope()
    candidate = _executor(source, catalog).execute_i03(
        query_ref=weighted_w2.ref, predicate_ref=op["predicate"].ref, group_scope=scope,
    )
    assert candidate.facts[0].as_dict() == baseline.facts[0].as_dict()
    assert candidate.facts[0].typed_state == "UNAVAILABLE"
    assert candidate.facts[0].p02_failure_state == "MEASURE_UNAVAILABLE"


def test_grouped_scope_universe_and_authority_registry_separation():
    from rawlsing_next.tests.pre553_query_frontier_fixtures import _multi_source_predicate

    left = _build_source(
        "grouped-univ-left",
        [{"id": "L1", "responses": {"X": 0, "Y": 0}},
         {"id": "L2", "responses": {"X": 0, "Y": 0}}],
        question_namespace="grouped-univ-shared", risk_namespace="grouped-univ-shared",
    )
    right = _build_source(
        "grouped-univ-right",
        [{"id": "R1", "responses": {"X": 1, "Y": 1}},
         {"id": "R2", "responses": {"X": 1, "Y": 1}}],
        question_namespace="grouped-univ-shared", risk_namespace="grouped-univ-shared",
    )
    qa = _query_authority("grouped-univ")
    predicate = _multi_source_predicate(left, right, qa, tag="grouped-univ")
    query = _query(
        left, qa, predicate, ("X", "Y"),
        source_mode="SOURCE_INDEXED_MULTI_UNIVERSE",
        universe_refs=(left["universe"].ref, right["universe"].ref),
        tag="grouped-univ",
        target_authority_refs=(
            left["source_auth"].authority_ref, right["source_auth"].authority_ref,
        ),
    )
    release_left = left["repo"].resolve_release_exact(left["release_ref"])
    release_right = right["repo"].resolve_release_exact(right["release_ref"])
    repository = C11Repository((release_left, release_right))
    registry = AuthorityRegistry((*left["authorities"], *right["authorities"], qa))
    release_refs = (release_left.release_ref, release_right.release_ref)
    baseline = execute_empirical_query(
        repository=repository, query=query, predicate=predicate,
        authority_registry=registry, release_refs=release_refs,
    )
    scope = I03GroupedExecutionScope()
    candidate = execute_empirical_query(
        repository=repository, query=query, predicate=predicate,
        authority_registry=registry, release_refs=release_refs, group_scope=scope,
    )
    assert [fact.as_dict() for fact in candidate.facts] == [
        fact.as_dict() for fact in baseline.facts
    ]
    assert scope.receipt()["core_builds"] == 2
    assert scope.receipt()["core_hits"] == 0

    source, ops, catalog = _main_data("grouped-registry")
    op = ops[0]
    extra = _auth("grouped-extra", "REPLAY_PROTOCOL", families=("ReplayReceipt@1.0.0",))
    catalog_extra = RuntimeObjectCatalog(
        authorities=tuple((*source["authorities"], _query_authority("grouped-registry"), extra)),
        predicates=(op["predicate"],), queries=(op["query"],), discovery_authorities=(),
    )
    first = _executor(source, catalog).execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref, group_scope=scope,
    )
    second = _executor(source, catalog_extra).execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref, group_scope=scope,
    )
    assert second.facts[0].as_dict() == first.facts[0].as_dict()
    assert scope.receipt()["core_builds"] == 4
    assert scope.receipt()["core_hits"] == 0


def test_grouped_scope_warm_hit_at_group_capacity_still_reuses():
    source, ops, catalog = _main_data("grouped-cap-hit")
    op = ops[0]
    baseline = _executor(source, catalog).execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
    )
    scope = I03GroupedExecutionScope(max_groups=1)
    executor = _executor(source, catalog)
    first = executor.execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref, group_scope=scope,
    )
    second = executor.execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref, group_scope=scope,
    )
    assert first.facts[0].as_dict() == baseline.facts[0].as_dict()
    assert second.facts[0].as_dict() == baseline.facts[0].as_dict()
    receipt = scope.receipt()
    assert receipt["core_builds"] == 1
    assert receipt["core_hits"] == 1
    assert receipt["capacity_fallbacks"] == 0
    assert receipt["early_capacity_fallbacks"] == 0
    assert receipt["open_groups"] == 1


def test_grouped_scope_capacity_miss_does_not_invoke_core_builder(monkeypatch):
    source, ops, catalog = _main_data("grouped-cap-miss")
    op_a, op_b = ops[0], ops[3]
    baseline_b = _executor(source, catalog).execute_i03(
        query_ref=op_b["query"].ref, predicate_ref=op_b["predicate"].ref,
    ).facts[0]
    scope = I03GroupedExecutionScope(max_groups=1)
    executor = _executor(source, catalog)
    executor.execute_i03(
        query_ref=op_a["query"].ref, predicate_ref=op_a["predicate"].ref,
        group_scope=scope,
    )
    calls = {"count": 0}
    original = empirical_query._evaluate_index_group_core

    def counted(*args, **kwargs):
        calls["count"] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(empirical_query, "_evaluate_index_group_core", counted)
    observed = executor.execute_i03(
        query_ref=op_b["query"].ref, predicate_ref=op_b["predicate"].ref,
        group_scope=scope,
    ).facts[0]
    monkeypatch.setattr(empirical_query, "_evaluate_index_group_core", original)
    assert calls["count"] == 0
    assert observed.as_dict() == baseline_b.as_dict()
    receipt = scope.receipt()
    assert receipt["core_build_attempts"] == 1
    assert receipt["core_builds"] == 1
    assert receipt["early_capacity_fallbacks"] == 1
    assert receipt["capacity_fallbacks"] == 1
    assert receipt["open_groups"] == 1
    baseline_a = _executor(source, catalog).execute_i03(
        query_ref=op_a["query"].ref, predicate_ref=op_a["predicate"].ref,
    ).facts[0]
    replay = executor.execute_i03(
        query_ref=op_a["query"].ref, predicate_ref=op_a["predicate"].ref,
        group_scope=scope,
    ).facts[0]
    assert replay.as_dict() == baseline_a.as_dict()
    assert scope.receipt()["core_hits"] >= 1


def test_grouped_scope_member_bound_unknown_prospective_keeps_honest_fallback():
    source, ops, catalog = _main_data("grouped-member-bound")
    op = ops[0]
    baseline = _executor(source, catalog).execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref,
    ).facts[0]
    scope = I03GroupedExecutionScope(max_cached_members=1)
    executor = _executor(source, catalog)
    first = executor.execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref, group_scope=scope,
    ).facts[0]
    second = executor.execute_i03(
        query_ref=op["query"].ref, predicate_ref=op["predicate"].ref, group_scope=scope,
    ).facts[0]
    assert first.as_dict() == baseline.as_dict()
    assert second.as_dict() == baseline.as_dict()
    receipt = scope.receipt()
    assert receipt["core_build_attempts"] == 2
    assert receipt["core_builds"] == 0
    assert receipt["early_capacity_fallbacks"] == 0
    assert receipt["capacity_fallbacks"] == 2
    assert receipt["open_groups"] == 0


def test_grouped_scope_member_capacity_hit_and_exhausted_miss():
    source, ops, catalog = _main_data("grouped-member-hit")
    by_id = {op["op_id"]: op for op in ops}
    op_small = by_id["minority_branch_target_K"]
    op_zero = by_id["all_X_raw"]
    baseline = _executor(source, catalog).execute_i03(
        query_ref=op_small["query"].ref, predicate_ref=op_small["predicate"].ref,
    ).facts[0]
    scope = I03GroupedExecutionScope(max_cached_members=1, max_groups=4)
    executor = _executor(source, catalog)
    first = executor.execute_i03(
        query_ref=op_small["query"].ref, predicate_ref=op_small["predicate"].ref,
        group_scope=scope,
    ).facts[0]
    second = executor.execute_i03(
        query_ref=op_small["query"].ref, predicate_ref=op_small["predicate"].ref,
        group_scope=scope,
    ).facts[0]
    assert first.as_dict() == baseline.as_dict()
    assert second.as_dict() == baseline.as_dict()
    assert scope.receipt()["core_builds"] == 1
    assert scope.receipt()["core_hits"] == 1
    assert scope.receipt()["capacity_fallbacks"] == 0
    zero_baseline = _executor(source, catalog).execute_i03(
        query_ref=op_zero["query"].ref, predicate_ref=op_zero["predicate"].ref,
    ).facts[0]
    zero = executor.execute_i03(
        query_ref=op_zero["query"].ref, predicate_ref=op_zero["predicate"].ref,
        group_scope=scope,
    ).facts[0]
    assert zero.as_dict() == zero_baseline.as_dict()
    assert scope.receipt()["early_capacity_fallbacks"] == 1
    assert scope.receipt()["capacity_fallbacks"] == 1


def test_cross_target_condition_reuse_preserves_exact_evidence_and_risk():
    source,ops,catalog=_main_data("condition-reuse",n=48)
    baseline=_run(_executor(source,catalog),ops)
    # A single full target core can fit, but all distinct targets may reuse
    # the small independently bounded condition memo on fallback.
    scope=I03GroupedExecutionScope(max_groups=1)
    candidate=_run(_executor(source,catalog),ops,scope)
    _facts_equal(baseline,candidate)
    receipt=scope.receipt()
    assert receipt["condition_cache_hits"]>48
    assert receipt["condition_cache_bytes_estimate"]>0
    assert receipt["condition_cache_bytes_estimate"]<=16*1024*1024
    assert receipt["core_builds"]==1
    scope.close()
    assert scope.receipt()["condition_cache_bytes_estimate"]==0
    tiny=I03GroupedExecutionScope(max_condition_bytes=1)
    _facts_equal(baseline,_run(_executor(source,catalog),ops,tiny))
    assert tiny.receipt()["condition_capacity_fallbacks"]>0
    assert tiny.receipt()["condition_cache_bytes_estimate"]==0


def test_indexed_country_postings_exact_selector_order_and_aliases():
    from array import array
    from rawlsing_next._pre553_c11_execution_view import _EventRead,_EventLane,_RespondentEvents,_ref_identity
    x,y,z=(_ref("QUESTION_NATIVE",name) for name in ("x","y","z"))
    auth=_query_authority("postings").authority_ref
    selectors=[]
    for i in range(80):
        native=(x,y,z)[i%3]
        canonical=x if i%5==0 else None
        component=y if i%7==0 else None
        selectors.append(_EventRead(_ref_identity(_ref("RespondentEvent",str(i))),
            "SUBSTANTIVE_RESPONSE" if i%2 else "MISSING",_ref_identity(native),
            _ref_identity(canonical) if canonical else None,
            _ref_identity(component) if component else None,
            ((auth.authority_id,auth.authority_version,auth.authority_content_hash),),
            i,None,{"kind":"SCALAR_SINGULAR"},str(i)))
    lane=_EventLane(None,tuple(selectors))
    rows=tuple(range(80))
    postings=[]
    for field in ("_native_question_identity","_canonical_question_identity","_component_identity"):
        ordered=sorted((i for i in rows if getattr(selectors[i],field) is not None),
                       key=lambda i:getattr(selectors[i],field))
        postings.append(memoryview(array("I",ordered).tobytes()).cast("I"))
    old=_RespondentEvents(lane,rows);new=_RespondentEvents(lane,rows,tuple(postings))
    for target in (x,y,z,_ref("QUESTION_NATIVE","absent")):
        for native_only in (False,True):
            for component in (False,True):
                for states in (None,frozenset(),frozenset({"MISSING"})):
                    kwargs=dict(native_only=native_only,include_component=component,states=states)
                    assert tuple(old.select(target,**kwargs))==tuple(new.select(target,**kwargs))
