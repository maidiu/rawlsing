"""HQ280 B1: independent source-free original-workload no-drop integration.

This is a TEST-LOCAL frozen expectation, not a source-science grant, planner,
production adapter or all-35-wave coverage assertion.  Expected work never
depends on selected C11 slots, runtime catalogs, produced facts or batch units.
"""
from __future__ import annotations

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalQuerySpec, EmpiricalUniverse, ExactRef, RoutingEligibilityFact, exact_ref, semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateSlotRule, ExactPhysicalCellStream, GovernedC11Projection,
    OccurrenceRule, PhysicalSlot, ResponseSlotRule, ResponseValueRule,
    RowRespondentBinding, physical_value_binding_key,
)
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_route_b_production import (
    I03ExecutionRequest, execute_route_b_production, verify_route_b_replay_receipt,
)
from rawlsing_next.pre553_batch_runner import (
    BatchExecutionRunner, BatchManifest, BatchUnitSpec, ExecutionOutcome, ExecutorBinding,
)
from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
from rawlsing_next.tests import c1_at08_at13_fixture as c1fx
from rawlsing_next.tests.test_pre553_route_b_production import _scalar_occurrence
from rawlsing_next.tests.test_pre553_empirical_query import (
    _auth, _branch_predicate, _h, _predicate, _query_authority,
    _ref, _response_leaf,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom, _d_auth, _discovery_authority, _grammar, _qt, _rule,
)
from rawlsing_next.tests.test_pre553_analytical_composition_higher_order import _subject_fact_ref

# Before any physical row or producer exists.  Codes are not inferred meanings.
INSTRUMENT = (
    ("A", (("0", "synthetic A category zero"), ("1", "synthetic A category one"),
           ("2", "synthetic A nonmodal category two"))),
    ("B", (("0", "synthetic B category zero"), ("1", "synthetic B category one"))),
)
ORIGINAL_SCOPE = ("B1_SYNTHETIC_RELEASE_1", "B1_SYNTHETIC_SELECTED_ADULT",
                  "EIGHT_EXACT_SAME_RESPONDENTS", "RAW", "B1_TEST_ONLY_AUTHORITY")
WORK = (
    ("W01", "RAW_MARGINAL", "A", "ALL", "I03", "NONE"),
    ("W02", "RAW_MARGINAL", "B", "ALL", "I03", "NONE"),
    ("W03", "RAW_CONDITIONAL", "B", "A=1", "I03", "C1_POSITIONED_SUBJECT"),
    ("W04", "RAW_CONDITIONAL", "A", "B=1", "I03", "NONE"),
    ("W05", "RAW_CONDITIONAL", "B", "A=2", "I03", "NONE"),
    ("W06", "EXACT_DISCOVERY", "B", "A=1|A=2", "I05", "NONE"),
)
BASE_A = (0, 0, 0, 1, 1, 1, 2, 2)
BASE_B = (0, 0, 1, 1, 1, 1, 0, 0)


def _work_key(row):
    return semantic_hash({"schema": "B1_INDEPENDENT_ORIGINAL_WORK@1",
                          "scope": ORIGINAL_SCOPE, "item_domains": INSTRUMENT,
                          "work": row})


# Test-local competent source/operation authorities are fixed from declarations,
# never borrowed from a selected producer catalog.
PREOUTCOME_AUTHORITY_REFS = (
    _auth("b1-source", "SOURCE_SEMANTICS_TOPOLOGY",
          families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0")).authority_ref.as_dict(),
    _query_authority("b1-grammar").authority_ref.as_dict(),
    _d_auth("b1-discovery").authority_ref.as_dict(),
)
# No result values, data hashes, selected projection references or runtime objects.
FROZEN_WORK_KEYS = {row[0]: _work_key(row) for row in WORK}
FROZEN_ORACLE_REF = semantic_hash({
    "schema": "B1_PRE_OUTCOME_ORIGINAL_ORACLE@1",
    "source_scope": ORIGINAL_SCOPE, "original_items": INSTRUMENT,
    "respondents": tuple(f"R{i}" for i in range(1, 9)),
    "scientifically_permitted_work": WORK,
    "exact_synthetic_issuers": PREOUTCOME_AUTHORITY_REFS,
    "operation_limit": {"K": 1, "J": 1, "pruning": "NONE_EXACT_EVALUATE_ALL"},
})


def _source(*, selected=("A", "B"), changed_outcomes=False, reversed_cells=False):
    # Separate transport/content identity from the pre-outcome work-class identity.
    aa = BASE_A
    bb = (1, 0, 1, 1, 1, 1, 0, 0) if changed_outcomes else BASE_B
    source_sha = _h(f"b1-physical:{aa}:{bb}")
    src = _auth("b1-source", "SOURCE_SEMANTICS_TOPOLOGY",
                families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"))
    mapping = _auth("b1-mapping", "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
                    families=("RespondentEvent@1.0.0",))
    coordinate = _auth("b1-coordinate", "COORDINATE_SEMANTICS",
                       families=("EmpiricalCoordinateFact@1.0.0",))
    routing_auth = _auth("b1-routing", "ROUTING_RISK_SET",
                         families=("RoutingEligibilityFact@1.0.0",))
    replay = _auth("b1-replay", "REPLAY_PROTOCOL", families=("ReplayReceipt@1.0.0",))
    projection_auth = _auth(
        "b1-projection", "SOURCE_SEMANTICS_TOPOLOGY",
        families=("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0",
                  "WeightMeasureFact@1.0.0"),
    )
    authorities = (src, mapping, coordinate, routing_auth, replay, projection_auth)
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(src.authority_ref,), dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "b1-universe"),
        raw_source_identity="RAW-B1-SYNTHETIC", source_family="SURVEY",
        study_product_release="B1/REL-1", instrument_release="B1-INST-1",
        country_geography="SYNTHETIC", sampling_geography="SYNTHETIC",
        raw_wave="W1", canonical_wave_if_governed=None,
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="SYNTHETIC_ADULTS",
        sampling_design_regime="SOURCE_LOCAL_TEST_ONLY",
        respondent_namespace="B1-SAME-PERSON",
        source_artifact_import_lineage="B1-TEST-FIXTURE",
        harmonization_authority_ref=None, source_relation_refs=(),
    )
    qrefs = {name: _ref("QUESTION_NATIVE", f"b1-{name}") for name, _ in INSTRUMENT}
    all_questions = {
        name: QuestionVariableBinding(
            empirical_universe_ref=universe.ref, native_question_ref=qrefs[name],
            instrument_question_version="1",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=src.authority_ref,
            topology_authority_ref=src.authority_ref,
        )
        for name, _ in INSTRUMENT
    }
    respondents = tuple(RespondentIdentity(
        empirical_universe_ref=universe.ref, respondent_key=f"R{i}",
        source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", f"b1-R{i}"),
        identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
    ) for i in range(1, 9))
    risk = _ref("RISK_SET", "b1-all-eight")
    route = tuple(RoutingEligibilityFact(
        typed_state="ELIGIBLE_APPLICABLE",
        authority_snapshot_refs=(routing_auth.authority_ref,), dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"b1-route-R{i}-{name}"),
        empirical_universe_ref=universe.ref, scoped_respondent_ref=respondents[i - 1].ref,
        question_or_target_ref=qrefs[name], risk_set_ref=risk,
        routing_rule_ref=_ref("ROUTING_RULE", f"b1-{name}-all-eight"),
        applicability_state="ELIGIBLE_APPLICABLE", routing_state="ELIGIBLE_APPLICABLE",
        parent_predicate_refs=(), member_set_replay_ref=_ref("MEMBER_SET", f"b1-{name}-all-eight"),
    ) for name in selected for i in range(1, 9))
    slot_rules = []
    for ordinal, (name, options) in enumerate(INSTRUMENT, 1):
        if name not in selected:
            continue
        slot_rules.append(ResponseSlotRule(
            PhysicalSlot(ordinal, name), all_questions[name],
            tuple(ResponseValueRule(
                physical_value_binding_key(code, PhysicalMissingState.OBSERVED_STORAGE_VALUE),
                "SUBSTANTIVE_RESPONSE", (_scalar_occurrence(name),), code,
                mapping.authority_ref,
            ) for code, _meaning in options),
        ))
    cells = []
    for i, (a, b) in enumerate(zip(aa, bb), 1):
        for ordinal, name, raw in ((1, "A", a), (2, "B", b), (3, "G", "T")):
            cells.append(PhysicalCell(
                row_ordinal=i, variable_ordinal=ordinal, variable_name=name,
                raw_value=str(raw), missing_state=PhysicalMissingState.OBSERVED_STORAGE_VALUE,
                source_missing_declaration=None,
            ))
    if reversed_cells:
        cells.reverse()
    stream = ExactPhysicalCellStream(
        source_sha256=source_sha, row_count=8,
        cell_iter_factory=lambda: iter(tuple(cells)),
    )
    projection = GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", "b1-" + "-".join(selected)),
        source_artifact_id="B1-SYNTHETIC-SOURCE",
        expected_source_sha256=source_sha,
        source_family_id="SURVEY", study_product_id="B1", release_id="REL-1",
        instrument_release_id="B1-INST-1",
        source_snapshot_retention_ref=ExactRef("SOURCE_SNAPSHOT", "urn:test:b1:snapshot", source_sha),
        universes=(universe,), respondents=respondents,
        row_bindings=tuple(RowRespondentBinding(i, respondents[i-1].ref) for i in range(1, 9)),
        questions=tuple(all_questions[n] for n in selected),
        response_slots=tuple(slot_rules),
        coordinate_slots=(CoordinateSlotRule(
            PhysicalSlot(3, "G"), _ref("COORDINATE_NATIVE", "b1-inert-G"),
            _ref("UNIT_TAXONOMY", "b1-inert-G"), "2026-01",
            coordinate.authority_ref, copy_observed_raw=True,
        ),),
        routing=route, weight_slots=(), authority_snapshots=authorities,
        source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(auth.authority_ref for auth in authorities),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay.authority_ref,
        tie_order_ref=_ref("ORDER_RULE", "b1-canonical"),
        replay_protocol_version="1.0.0",
    )
    stub = {
        "universe": universe, "respondents": {f"R{i}": x for i, x in enumerate(respondents, 1)},
        "qrefs": {k: qrefs[k] for k in selected}, "risk_refs": {"R": risk},
        "source_auth": src, "authorities": authorities,
    }
    return stream, projection, stub


def _query(stub, qauth, predicate, target, label):
    """Existing I03 object constructor with explicit 3-option A domain."""
    domain = [code for name, options in INSTRUMENT if name == target for code, _ in options]
    return EmpiricalQuerySpec(
        typed_state="QUERY_AUTHORIZED_RESOLVABLE",
        authority_snapshot_refs=(qauth.authority_ref,),
        dependency_refs=(predicate.ref,),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"b1-query-{label}"),
        target_refs=(stub["qrefs"][target],),
        target_arity_and_topology={
            "arity": 1, "joint_order_semantics": "SEMANTIC_ORDERED",
            "components": [{
                "target_ref": stub["qrefs"][target],
                "topology": "SCALAR_SINGULAR", "domain": domain,
                "target_domain_replay_ref": _ref("TARGET_DOMAIN", f"b1-{target}-" + "".join(domain)),
                "topology_authority_refs": [stub["source_auth"].authority_ref],
                "response_semantic_authority_refs": [stub["source_auth"].authority_ref],
                "included_states": ["SUBSTANTIVE_RESPONSE"],
            }],
        },
        condition_predicate_ref=predicate.ref, risk_set_ref=stub["risk_refs"]["R"],
        empirical_universe_refs=(stub["universe"].ref,), scope_refs=(stub["universe"].ref,),
        measure_basis_ref=_ref("MEASURE_BASIS", "RAW"),
        requested_output_grain={
            "source_scope_mode": "SINGLE_UNIVERSE", "measure_kind": "RAW",
            "risk_set_type": "WHOLE_QUESTION_RISK_SET",
            "response_state_semantics_ref": _ref("RESPONSE_STATE_SEMANTICS", "SUBSTANTIVE"),
            "uncertainty_method_or_typed_state": "UNCERTAINTY_UNQUANTIFIED",
        },
        query_authority_refs=(qauth.authority_ref,),
    )


def _workload(stub, *, only_a):
    qa = _query_authority("b1-grammar")
    da = _d_auth("b1-discovery")
    all_p = _branch_predicate(stub, qa, tag="b1-all")
    a1 = _predicate(stub, qa, _response_leaf(stub, qa, "A", 1), tag="b1-a1")
    a2 = _predicate(stub, qa, _response_leaf(stub, qa, "A", 2), tag="b1-a2")
    by_id = {
        "W01": (_query(stub, qa, all_p, "A", "w01"), all_p),
    }
    if only_a:
        empty = _branch_predicate(stub, qa, members=(), tag="b1-empty")
        grammar = _grammar(
            operation="I03-OP-b1-discovery",
            atoms=[_atom("ALL", all_p, "BRANCH"), _atom("EMPTY", empty, "BRANCH")],
            templates=[_qt("A", by_id["W01"][0])],
            rules=[_rule(
                "a-only-valid-empty", "MINORITY_OR_NONMODAL_DEPARTURE",
                "SINGLE_ATOM", atom_ids=("EMPTY",), baseline_atom_id="ALL",
                query_template_id="A",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )], k=1, j=1,
        )
        predicates = (all_p, a1, a2, empty)
    else:
        b1 = _predicate(stub, qa, _response_leaf(stub, qa, "B", 1), tag="b1-b1")
        by_id.update({
            "W02": (_query(stub, qa, all_p, "B", "w02"), all_p),
            "W03": (_query(stub, qa, a1, "B", "w03"), a1),
            "W04": (_query(stub, qa, b1, "A", "w04"), b1),
            "W05": (_query(stub, qa, a2, "B", "w05"), a2),
        })
        grammar = _grammar(
            operation="I03-OP-b1-discovery",
            atoms=[_atom("ALL", all_p, "BRANCH"),
                   _atom("A1", a1, "RESPONSE"), _atom("A2", a2, "RESPONSE")],
            templates=[_qt("B", by_id["W02"][0])],
            rules=[_rule(
                "b1-two-conditions", "PAIR_RESPONSE_COTRAVEL",
                "SINGLE_ATOM", atom_ids=("A1", "A2"), baseline_atom_id="ALL",
                query_template_id="B",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )], k=1, j=1,
        )
        predicates = (all_p, a1, a2, b1)
    discovery = _discovery_authority(stub, grammar, da, tag="b1-discovery")
    catalog = RuntimeObjectCatalog(
        authorities=tuple((*stub["authorities"], qa, da)),
        predicates=predicates,
        queries=tuple(query for query, _ in by_id.values()),
        discovery_authorities=(discovery,),
    )
    requests = tuple(I03ExecutionRequest(q.ref, p.ref) for q, p in by_id.values())
    return catalog, by_id, discovery, requests, qa


def _batch(route, by_id, discovery):
    """Independent operational view; genuine existing QUERY/DISCOVERY executors."""
    executor = route.repository_binding.executor
    release = route.c11_release.release_ref
    query_units = {
        name: BatchUnitSpec(
            job_kind="QUERY", job_ref=query.ref, release_refs=(release,),
            semantic_input_refs=(predicate.ref,),
        )
        for name, (query, predicate) in by_id.items()
    }
    discovery_unit = BatchUnitSpec(
        job_kind="DISCOVERY", job_ref=discovery.ref, release_refs=(release,),
    )
    units = tuple((*query_units.values(), discovery_unit))
    manifest = BatchManifest(units)
    query_by_ref = {q.ref.key: (q, p) for q, p in by_id.values()}

    def execute(unit):
        if unit.job_kind == "QUERY":
            query, predicate = query_by_ref[unit.job_ref.key]
            result = executor.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
            return ExecutionOutcome(
                result_refs=tuple(fact.ref for fact in result.facts),
                provenance_refs=(query.ref, predicate.ref, release),
            )
        result = executor.execute_i05(discovery_authority_ref=discovery.ref)
        return ExecutionOutcome(
            result_refs=tuple(receipt.ref for receipt in result.receipts),
            provenance_refs=(discovery.ref, release, result.evaluated_frontier_ref),
        )

    runner = BatchExecutionRunner(manifest=manifest, repository=executor.repository)
    receipts = runner.run(executors={
        "QUERY": ExecutorBinding(_ref("EXECUTOR", "b1-query"), execute),
        "DISCOVERY": ExecutorBinding(_ref("EXECUTOR", "b1-discovery"), execute),
    })
    assert len(receipts) == len(manifest.units)
    assert all(r.state == "COMPLETED" and r.execution_performed for r in receipts)
    assert runner.summary().full_coverage
    return query_units, discovery_unit, runner, receipts


def _run(*, only_a=False, changed_outcomes=False, reversed_cells=False):
    stream, projection, stub = _source(
        selected=("A",) if only_a else ("A", "B"),
        changed_outcomes=changed_outcomes, reversed_cells=reversed_cells,
    )
    catalog, by_id, discovery, requests, qauth = _workload(stub, only_a=only_a)
    route = execute_route_b_production(
        source=stream, projection=projection, runtime_catalog=catalog,
        i03_requests=requests, discovery_authority_ref=discovery.ref,
    )
    assert verify_route_b_replay_receipt(route.replay_receipt) == route.replay_receipt["dependency_root"]
    query_units, discovery_unit, runner, receipts = _batch(route, by_id, discovery)
    return {
        "route": route, "projection": projection, "stub": stub,
        "catalog": catalog, "by_id": by_id, "discovery": discovery,
        "query_units": query_units, "discovery_unit": discovery_unit,
        "runner": runner, "receipts": receipts, "qauth": qauth,
    }


def _cells(fact):
    return {
        str(c["cell"]): c for c in fact.target_topology["complete_cell_semantic_projection"]
    }


def _fact(case, work_id):
    query, _ = case["by_id"][work_id]
    found = [r for r in case["route"].i03_results if r.query_ref == query.ref]
    assert len(found) == 1 and len(found[0].facts) == 1
    return found[0].facts[0]


def _reconcile(case, *, consumed=()):
    # Oracle names and keys are independent of the actual submitted workload.
    qrefs = {name: _ref("QUESTION_NATIVE", f"b1-{name}") for name, _ in INSTRUMENT}
    present_native_refs = {q.native_question_ref for q in case["projection"].questions}
    missing_original = tuple(name for name in ("A", "B") if qrefs[name] not in present_native_refs)
    constructed = set(case["by_id"])
    discovery_rules = case["discovery"].candidate_universe_definition["rules"]
    has_exact_w06 = (
        not missing_original and len(discovery_rules) == 1
        and discovery_rules[0]["family"] == "PAIR_RESPONSE_COTRAVEL"
        and discovery_rules[0]["form"] == "SINGLE_ATOM"
        and set(discovery_rules[0]["atom_ids"]) == {"A1", "A2"}
        and discovery_rules[0]["validation"]["kind"] == "DISTRIBUTION_DIFFERS_FROM_BASELINE"
    )
    if has_exact_w06:
        constructed.add("W06")
    expected = set(FROZEN_WORK_KEYS)
    missing_work = tuple(sorted(expected - constructed))
    # Do not allow an A-query or a synthetic success receipt to impersonate B.
    # Reconcile exact target, source, risk, measure, job and produced fact refs.
    by_expected = {row[0]: row for row in WORK}
    executor = case["route"].repository_binding.executor
    release = case["route"].c11_release.release_ref
    for name, (query, predicate) in case["by_id"].items():
        role = by_expected[name]
        assert tuple(exact_ref(r, "target") for r in query.target_refs) == (qrefs[role[2]],)
        assert exact_ref(query.condition_predicate_ref, "condition") == predicate.ref
        assert exact_ref(query.risk_set_ref, "risk") == case["stub"]["risk_refs"]["R"]
        assert tuple(exact_ref(r, "universe") for r in query.empirical_universe_refs) == (case["stub"]["universe"].ref,)
        assert query.requested_output_grain["measure_kind"] == "RAW"
        unit = case["query_units"][name]
        assert unit.job_ref == query.ref and unit.release_refs == (release,)
        assert predicate.ref in unit.semantic_input_refs
        execution = executor.execute_i03(query_ref=query.ref, predicate_ref=predicate.ref)
        facts = tuple(f.ref for f in execution.facts)
        batch_receipts = tuple(r for r in case["receipts"] if r.unit_ref == unit.unit_ref)
        assert len(batch_receipts) == 1
        assert tuple(batch_receipts[0].result_refs) == facts
        assert all(exact_ref(fact.empirical_query_spec_ref, "fact query") == query.ref for fact in execution.facts)
    local_discovery = case["route"].i05_result
    discovery_receipts = tuple(
        r for r in case["receipts"] if r.unit_ref == case["discovery_unit"].unit_ref
    )
    assert len(discovery_receipts) == 1
    assert tuple(discovery_receipts[0].result_refs) == tuple(
        r.ref for r in local_discovery.receipts
    )
    completed = {name for name in case["by_id"] if any(
        receipt.unit_ref == case["query_units"][name].unit_ref and receipt.state == "COMPLETED"
        for receipt in case["receipts"]
    )}
    if "W06" in constructed and any(
        receipt.unit_ref == case["discovery_unit"].unit_ref and receipt.state == "COMPLETED"
        for receipt in case["receipts"]
    ):
        completed.add("W06")
    not_executed = tuple(sorted(expected - completed))
    missing_consumers = tuple(
        row[0] for row in WORK if row[-1] != "NONE"
        and (row[0] not in completed or row[0] not in consumed)
    )
    passed = not (missing_original or missing_work or not_executed or missing_consumers)
    return {
        "pass": passed, "original_omissions": missing_original,
        "work_omissions": missing_work, "not_executed": not_executed,
        "consumer_omissions": missing_consumers,
    }


def _consume_w03(case):
    stub, route = case["stub"], case["route"]
    query, predicate = case["by_id"]["W03"]
    release = route.c11_release.release_ref
    pairing = c1fx.make_pairing_authority("b1-w03")
    subject_ref = ExactRef(
        "C1_SYNTHETIC_POSITIONED_SUBJECT@1", "urn:test:b1:subject",
        semantic_hash({"fixture": "B1_W03"}),
    )
    binding = c1fx.make_conditioner_binding(
        binding_id="a1",
        subject_fact_ref=ExactRef(**_subject_fact_ref(stub, "A", 1)),
        empirical_coordinate_ref=stub["qrefs"]["A"],
        comparability_authority_ref=pairing,
        source_universe_ref=stub["universe"].ref, release_ref=release,
    )
    consumer_query = c1fx.make_multi_conditioner_consumer_query(
        query_id="B1-W03-C1", subject_ref=subject_ref,
        target_ref=stub["qrefs"]["B"], source_universe_ref=stub["universe"].ref,
        release_ref=release, bindings=[binding],
        projection_kind="B1_C1_CONDITIONAL_DISTRIBUTION",
    )
    witness = c1fx.build_witness_for_binding(
        witness_object_id="urn:test:b1:w03-witness", consumer_query=consumer_query,
        producer_query=query, producer_predicate=predicate,
        bindings=[binding], coordinate_value_pairs=[(stub["qrefs"]["A"], 1)],
        pairing_authority=pairing, source_universe_ref=stub["universe"].ref,
        release_ref=release,
    )
    result = compose_positioned_subject_possibility(
        repository=route.repository_binding.executor.repository,
        empirical_query=query, predicate=predicate,
        authority_registry=case["catalog"].authority_registry,
        release_refs=(release,), consumer_query=consumer_query,
        model_rule=c1fx.make_model_rule(stub["universe"].ref, "b1-w03"),
        condition_binding_witness=witness,
    )
    assert result.producer_route == "DIRECT_I03_TO_POSITIONED_SUBJECT"
    assert result.analytical_state == "SUPPORTED"
    assert result.raw_denominator_support == 3
    assert result.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    return result


def test_p01_frozen_original_ab_all_operations_batch_and_actual_c1_consumer():
    assert len(FROZEN_WORK_KEYS) == 6
    frozen = FROZEN_ORACLE_REF
    case = _run()
    assert FROZEN_ORACLE_REF == frozen
    assert {q.native_question_ref for q in case["projection"].questions} == {
        _ref("QUESTION_NATIVE", "b1-A"), _ref("QUESTION_NATIVE", "b1-B")
    }
    assert all(_fact(case, key).typed_state == "SUPPORTED" for key in ("W01", "W02", "W03", "W04", "W05"))
    assert {k: v["raw_numerator_support"] for k, v in _cells(_fact(case, "W01")).items()} == {
        "0": 3, "1": 3, "2": 2,
    }
    assert {k: v["raw_numerator_support"] for k, v in _cells(_fact(case, "W02")).items()} == {
        "0": 4, "1": 4,
    }
    assert _fact(case, "W03").raw_denominator_support == 3
    assert _cells(_fact(case, "W03"))["1"]["raw_numerator_support"] == 3
    assert _fact(case, "W04").raw_denominator_support == 4
    assert _cells(_fact(case, "W04"))["1"]["raw_numerator_support"] == 3
    assert _fact(case, "W05").raw_denominator_support == 2
    assert _cells(_fact(case, "W05"))["1"]["raw_numerator_support"] == 0
    assert _cells(_fact(case, "W05"))["1"]["cell_state"] == "OBSERVED_ZERO_IN_SUPPORTED_RISK_SET"
    discovery = case["route"].i05_result
    assert discovery.candidate_count == discovery.covered_candidate_count == 2
    assert len(discovery.receipts) == 2
    assert all(r.coverage_state.startswith("EVALUATED_") for r in discovery.receipts)
    consumer = _consume_w03(case)
    assert {cell["cell"]: cell["raw_numerator_support"] for cell in consumer.complete_cell_geometry} == {
        "0": 0, "1": 3,
    }
    assert _reconcile(case, consumed=("W03",)) == {
        "pass": True, "original_omissions": (), "work_omissions": (),
        "not_executed": (), "consumer_omissions": (),
    }


def test_n01_all_submitted_a_only_jobs_complete_but_frozen_original_b_fails():
    frozen = FROZEN_ORACLE_REF
    case = _run(only_a=True)
    assert case["runner"].summary().full_coverage is True
    assert case["runner"].summary().coverage_state == "FULL_MANIFEST_COVERAGE"
    assert _fact(case, "W01").typed_state == "SUPPORTED"
    assert case["route"].i05_result.valid_empty is True
    assert case["route"].i05_result.receipts[0].typed_state == "VALID_EMPTY"
    fail = _reconcile(case)
    assert not fail["pass"]
    assert fail["original_omissions"] == ("B",)
    assert fail["work_omissions"] == ("W02", "W03", "W04", "W05", "W06")
    assert "W02" in fail["not_executed"] and "W06" in fail["not_executed"]
    assert fail["consumer_omissions"] == ("W03",)
    assert FROZEN_ORACLE_REF == frozen


def test_n02_three_expected_batch_jobs_one_omitted_locally_complete_globally_fails():
    case = _run()
    release = case["route"].c11_release.release_ref
    expected = {
        name: BatchUnitSpec(
            job_kind="QUERY", job_ref=case["by_id"][name][0].ref,
            release_refs=(release,),
            semantic_input_refs=(case["by_id"][name][1].ref,),
        )
        for name in ("W01", "W02", "W03")
    }
    manifest = BatchManifest((expected["W01"], expected["W03"]))
    executor = case["route"].repository_binding.executor
    by_ref = {expected[name].job_ref.key: case["by_id"][name] for name in ("W01", "W03")}

    def execute(unit):
        query, pred = by_ref[unit.job_ref.key]
        result = executor.execute_i03(query_ref=query.ref, predicate_ref=pred.ref)
        return ExecutionOutcome(
            result_refs=tuple(f.ref for f in result.facts),
            provenance_refs=(query.ref, pred.ref, release),
        )

    runner = BatchExecutionRunner(manifest=manifest, repository=executor.repository)
    receipts = runner.run(executors={
        "QUERY": ExecutorBinding(_ref("EXECUTOR", "b1-n02-query"), execute),
    })
    assert len(receipts) == 2 and all(r.state == "COMPLETED" for r in receipts)
    assert runner.summary().full_coverage is True
    assert runner.summary().coverage_state == "FULL_MANIFEST_COVERAGE"
    expected_refs = {x.unit_ref.key for x in expected.values()}
    actual_refs = {x.unit_ref.key for x in manifest.units}
    assert expected_refs - actual_refs == {expected["W02"].unit_ref.key}


def test_n03_outcome_and_physical_order_do_not_select_the_original_frontier():
    frozen = FROZEN_ORACLE_REF
    left = _run()
    reversed_cells = _run(reversed_cells=True)
    changed = _run(changed_outcomes=True)
    assert FROZEN_ORACLE_REF == frozen
    assert left["discovery"].ref == reversed_cells["discovery"].ref == changed["discovery"].ref
    assert left["discovery"].candidate_grammar_ref == changed["discovery"].candidate_grammar_ref
    assert left["route"].i05_result.evaluated_frontier_ref == changed["route"].i05_result.evaluated_frontier_ref
    assert left["route"].c11_release.release_ref == reversed_cells["route"].c11_release.release_ref
    assert _cells(_fact(left, "W02"))["1"]["raw_numerator_support"] != (
        _cells(_fact(changed, "W02"))["1"]["raw_numerator_support"]
    )
    # An outcome change may alter source/release/fact identities; not authorized work.
    assert set(FROZEN_WORK_KEYS) == {"W01", "W02", "W03", "W04", "W05", "W06"}
