from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
import inspect

import pytest

import rawlsing_next.pre553_route_b_production as route_b
from rawlsing_next.pre553_carrier_execution import (
    CarrierExecutionBindingError,
    CarrierNeutralResearchExecutor,
    RuntimeObjectCatalog,
    learned_empirical_execution_receipt,
)
from rawlsing_next.pre553_c11_integrity import (
    QuestionVariableBinding,
    RespondentIdentity,
    TypedAbsence,
)
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import (
    DiscoveryAuthority,
    EmpiricalUniverse,
    ExactRef,
    RoutingEligibilityFact,
    StructuralEmpiricalAdmission,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
    CoordinateSlotRule,
    ExactPhysicalCellStream,
    GovernedC11Projection,
    OccurrenceRule,
    PhysicalSlot,
    ResponseSlotRule,
    ResponseValueRule,
    RowRespondentBinding,
    SourceBackedC11SessionCache,
    WeightSlotRule,
    WeightValueRule,
    build_source_backed_c11_repository,
    physical_value_binding_key,
)
from rawlsing_next.tests.test_pre553_discovery_exact import (
    _atom,
    _d_auth,
    _discovery_authority,
    _grammar,
    _qt,
    _rule,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _auth,
    _branch_predicate,
    _h,
    _predicate,
    _query,
    _query_authority,
    _ref,
    _response_leaf,
)


def _scalar_occurrence(question: str) -> OccurrenceRule:
    return OccurrenceRule(
        "0",
        _ref("TOPOLOGY", f"m01-{question}-scalar"),
        {"kind": "SCALAR_SINGULAR", "index": 0},
    )


def _fixture(*, missing_weight: bool = False, valid_empty: bool = False):
    tag = "m01-missing-weight" if missing_weight else "m01"
    if valid_empty:
        tag += "-valid-empty"

    source_auth = _auth(
        f"{tag}-source",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"),
    )
    mapping_auth = _auth(
        f"{tag}-mapping",
        "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
        families=("RespondentEvent@1.0.0",),
    )
    coord_auth = _auth(
        f"{tag}-coord",
        "COORDINATE_SEMANTICS",
        families=("EmpiricalCoordinateFact@1.0.0",),
    )
    routing_auth = _auth(
        f"{tag}-routing",
        "ROUTING_RISK_SET",
        families=("RoutingEligibilityFact@1.0.0",),
    )
    weight_auth = _auth(
        f"{tag}-weight",
        "WEIGHT_DESIGN_ESTIMAND",
        families=("WeightMeasureFact@1.0.0",),
    )
    replay_auth = _auth(
        f"{tag}-replay",
        "REPLAY_PROTOCOL",
        families=("ReplayReceipt@1.0.0",),
    )
    projection_auth = _auth(
        f"{tag}-projection",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=(
            "RespondentEvent@1.0.0",
            "EmpiricalCoordinateFact@1.0.0",
            "WeightMeasureFact@1.0.0",
        ),
    )
    projection_authorities = (
        source_auth,
        mapping_auth,
        coord_auth,
        routing_auth,
        weight_auth,
        replay_auth,
        projection_auth,
    )

    source_sha = _h(f"{tag}-physical-source")
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", f"{tag}-universe"
        ),
        raw_source_identity=f"RAW-{tag}",
        source_family="SURVEY",
        study_product_release=f"STUDY-{tag}/REL-1",
        instrument_release=f"INST-{tag}",
        country_geography="US",
        sampling_geography="US-NATIONAL",
        raw_wave="W1",
        canonical_wave_if_governed=None,
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="ADULTS",
        sampling_design_regime="DESIGN-M01",
        respondent_namespace=f"NS-{tag}",
        source_artifact_import_lineage=f"SOURCE-LINEAGE-{tag}",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )

    names = ("X", "Y", "O", "R")
    qrefs = {name: _ref("QUESTION_NATIVE", f"{tag}-{name}") for name in names}
    questions = tuple(
        QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=qrefs[name],
            instrument_question_version="1",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref,
        )
        for name in names
    )
    qbind = dict(zip(names, questions))

    respondents = tuple(
        RespondentIdentity(
            empirical_universe_ref=universe.ref,
            respondent_key=f"R{i}",
            source_native_respondent_key_ref_or_typed_absence=_ref(
                "SOURCE_RESPONDENT", f"{tag}-R{i}"
            ),
            identity_map_authority_ref_or_typed_absence=TypedAbsence(
                "NOT_APPLICABLE"
            ),
        )
        for i in range(1, 4)
    )
    respondents_by_id = {f"R{i}": respondents[i - 1] for i in range(1, 4)}

    risk = _ref("RISK_SET", f"{tag}-risk")
    routing = []
    for name in names:
        for rid, respondent in respondents_by_id.items():
            state = (
                "NOT_ELIGIBLE"
                if name == "Y" and rid == "R3"
                else "ELIGIBLE_APPLICABLE"
            )
            routing.append(
                RoutingEligibilityFact(
                    typed_state=state,
                    authority_snapshot_refs=(routing_auth.authority_ref,),
                    dependency_refs=(),
                    producer_replay_locator_or_reference_root=_ref(
                        "REPLAY_ROOT", f"{tag}-routing-{rid}-{name}"
                    ),
                    empirical_universe_ref=universe.ref,
                    scoped_respondent_ref=respondent.ref,
                    question_or_target_ref=qrefs[name],
                    risk_set_ref=risk,
                    routing_rule_ref=_ref("ROUTING_RULE", f"{tag}-{name}"),
                    applicability_state=state,
                    routing_state=state,
                    parent_predicate_refs=(),
                    member_set_replay_ref=_ref(
                        "MEMBER_SET", f"{tag}-{name}-{state}"
                    ),
                )
            )

    rows = (
        {"X": "1", "Y": "1", "O": "AB", "R": "XY", "G": "A", "W": 2},
        {
            "X": "0",
            "Y": "0",
            "O": "BA",
            "R": "XZ",
            "G": "B",
            "W": None if missing_weight else 1,
        },
        {"X": "1", "Y": "1", "O": "AB", "R": "XY", "G": "A", "W": 3},
    )
    variable_ordinals = {"X": 1, "Y": 2, "O": 3, "R": 4, "G": 5, "W": 6}
    cells = []
    for row_ordinal, row in enumerate(rows, 1):
        for name, variable_ordinal in variable_ordinals.items():
            raw = row[name]
            missing_state = (
                PhysicalMissingState.SYSTEM_MISSING
                if raw is None
                else PhysicalMissingState.OBSERVED_STORAGE_VALUE
            )
            cells.append(
                PhysicalCell(
                    row_ordinal=row_ordinal,
                    variable_ordinal=variable_ordinal,
                    variable_name=name,
                    raw_value=raw,
                    missing_state=missing_state,
                    source_missing_declaration=None,
                )
            )
    cells = tuple(cells)
    stream = ExactPhysicalCellStream(
        source_sha256=source_sha,
        row_count=3,
        cell_iter_factory=lambda: iter(cells),
    )

    pkey = lambda raw, state=PhysicalMissingState.OBSERVED_STORAGE_VALUE: (
        physical_value_binding_key(raw, state)
    )
    response_slots = (
        ResponseSlotRule(
            PhysicalSlot(1, "X"),
            qbind["X"],
            (
                ResponseValueRule(
                    pkey("1"),
                    "SUBSTANTIVE_RESPONSE",
                    (_scalar_occurrence("X"),),
                    "1",
                    mapping_auth.authority_ref,
                ),
                ResponseValueRule(
                    pkey("0"),
                    "SUBSTANTIVE_RESPONSE",
                    (_scalar_occurrence("X"),),
                    "0",
                    mapping_auth.authority_ref,
                ),
            ),
        ),
        ResponseSlotRule(
            PhysicalSlot(2, "Y"),
            qbind["Y"],
            (
                ResponseValueRule(
                    pkey("1"),
                    "SUBSTANTIVE_RESPONSE",
                    (_scalar_occurrence("Y"),),
                    "1",
                    mapping_auth.authority_ref,
                ),
                ResponseValueRule(
                    pkey("0"),
                    "SUBSTANTIVE_RESPONSE",
                    (_scalar_occurrence("Y"),),
                    "0",
                    mapping_auth.authority_ref,
                ),
            ),
        ),
        ResponseSlotRule(
            PhysicalSlot(3, "O"),
            qbind["O"],
            tuple(
                ResponseValueRule(
                    pkey(value),
                    "SUBSTANTIVE_RESPONSE",
                    (
                        OccurrenceRule(
                            "0",
                            _ref("TOPOLOGY", f"{tag}-ordered"),
                            {
                                "kind": "ORDERED_SEQUENCE",
                                "semantic_ordinal": 0,
                            },
                        ),
                        OccurrenceRule(
                            "1",
                            _ref("TOPOLOGY", f"{tag}-ordered"),
                            {
                                "kind": "ORDERED_SEQUENCE",
                                "semantic_ordinal": 1,
                            },
                        ),
                    ),
                    value,
                    mapping_auth.authority_ref,
                )
                for value in ("AB", "BA")
            ),
        ),
        ResponseSlotRule(
            PhysicalSlot(4, "R"),
            qbind["R"],
            tuple(
                ResponseValueRule(
                    pkey(value),
                    "SUBSTANTIVE_RESPONSE",
                    (
                        OccurrenceRule(
                            "0",
                            _ref("TOPOLOGY", f"{tag}-repeated"),
                            {
                                "kind": "REPEATED_EVENT",
                                "multiplicity_index": 0,
                            },
                        ),
                        OccurrenceRule(
                            "1",
                            _ref("TOPOLOGY", f"{tag}-repeated"),
                            {
                                "kind": "REPEATED_EVENT",
                                "multiplicity_index": 1,
                            },
                        ),
                    ),
                    value,
                    mapping_auth.authority_ref,
                )
                for value in ("XY", "XZ")
            ),
        ),
    )

    weight_values = [
        WeightValueRule(pkey(2), 2),
        WeightValueRule(pkey(3), 3),
    ]
    if missing_weight:
        weight_values.append(
            WeightValueRule(
                pkey(None, PhysicalMissingState.SYSTEM_MISSING),
                None,
                state="WEIGHT_MISSING",
            )
        )
    else:
        weight_values.append(WeightValueRule(pkey(1), 1))

    projection = GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", tag),
        source_artifact_id=f"SOURCE-{tag}",
        expected_source_sha256=source_sha,
        source_family_id="SURVEY",
        study_product_id=f"STUDY-{tag}",
        release_id=f"REL-{tag}",
        instrument_release_id=f"INST-{tag}",
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:test:m01:snapshot:{tag}", source_sha
        ),
        universes=(universe,),
        respondents=respondents,
        row_bindings=tuple(
            RowRespondentBinding(i, respondents[i - 1].ref) for i in range(1, 4)
        ),
        questions=questions,
        response_slots=response_slots,
        coordinate_slots=(
            CoordinateSlotRule(
                PhysicalSlot(5, "G"),
                _ref("COORDINATE_NATIVE", f"{tag}-G"),
                _ref("UNIT_TAXONOMY", f"{tag}-G"),
                "2026-01",
                coord_auth.authority_ref,
                copy_observed_raw=True,
            ),
        ),
        routing=tuple(routing),
        weight_slots=(
            WeightSlotRule(
                PhysicalSlot(6, "W"),
                "W",
                _ref("WEIGHT_SOURCE", f"{tag}-W"),
                weight_auth.authority_ref,
                weight_auth.authority_ref,
                _ref("SCOPE", f"{tag}-W"),
                values=tuple(weight_values),
            ),
        ),
        authority_snapshots=projection_authorities,
        source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(
            auth.authority_ref for auth in projection_authorities
        ),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=_ref("ORDER_RULE", f"{tag}-canonical-ref-sort"),
        replay_protocol_version="1.0.0",
    )

    source_stub = {
        "universe": universe,
        "respondents": respondents_by_id,
        "qrefs": qrefs,
        "risk_refs": {"R": risk},
        "source_auth": source_auth,
        "authorities": projection_authorities,
    }
    qauth = _query_authority(f"{tag}-query")
    dauth = _d_auth(f"{tag}-discovery")
    all_p = _branch_predicate(source_stub, qauth, tag=f"{tag}-all")
    x1 = _predicate(
        source_stub,
        qauth,
        _response_leaf(source_stub, qauth, "X", 1),
        tag=f"{tag}-x1",
    )
    empty = _branch_predicate(
        source_stub, qauth, members=(), tag=f"{tag}-empty"
    )
    raw_query = _query(
        source_stub,
        qauth,
        all_p,
        ("Y",),
        measure="RAW",
        tag=f"{tag}-raw-y",
    )
    weighted_query = _query(
        source_stub,
        qauth,
        all_p,
        ("Y",),
        measure="GOVERNED_WEIGHTED",
        tag=f"{tag}-weighted-y",
    )

    discovery_atom = empty if valid_empty else x1
    discovery_atom_id = "EMPTY" if valid_empty else "X1"
    grammar = _grammar(
        operation=f"I03-OP-{tag}-discovery",
        atoms=[
            _atom("ALL", all_p, "BRANCH"),
            _atom(
                discovery_atom_id,
                discovery_atom,
                "BRANCH" if valid_empty else "RESPONSE",
            ),
        ],
        templates=[_qt("Y", raw_query)],
        rules=[
            _rule(
                "m01-rule",
                (
                    "MINORITY_OR_NONMODAL_DEPARTURE"
                    if valid_empty
                    else "PAIR_RESPONSE_COTRAVEL"
                ),
                "SINGLE_ATOM",
                atom_ids=(discovery_atom_id,),
                baseline_atom_id="ALL",
                query_template_id="Y",
                validation={"kind": "DISTRIBUTION_DIFFERS_FROM_BASELINE"},
            )
        ],
    )
    discovery_authority = _discovery_authority(
        source_stub, grammar, dauth, tag=f"{tag}-discovery"
    )

    catalog = RuntimeObjectCatalog(
        authorities=tuple((*projection_authorities, qauth, dauth)),
        predicates=(all_p, x1, empty),
        queries=(raw_query, weighted_query),
        discovery_authorities=(discovery_authority,),
    )
    requests = (
        route_b.I03ExecutionRequest(raw_query.ref, all_p.ref),
        route_b.I03ExecutionRequest(weighted_query.ref, all_p.ref),
    )

    return {
        "stream": stream,
        "projection": projection,
        "catalog": catalog,
        "requests": requests,
        "discovery_authority": discovery_authority,
        "raw_query": raw_query,
        "weighted_query": weighted_query,
        "all_p": all_p,
        "x1": x1,
        "empty": empty,
        "projection_auth": projection_auth,
        "qauth": qauth,
        "dauth": dauth,
        "risk": risk,
        "qrefs": qrefs,
    }


def _execute(fx, *, cache=None, catalog=None, requests=None, discovery_ref=None):
    return route_b.execute_route_b_production(
        source=fx["stream"],
        projection=fx["projection"],
        runtime_catalog=catalog or fx["catalog"],
        i03_requests=requests or fx["requests"],
        discovery_authority_ref=discovery_ref or fx["discovery_authority"].ref,
        cache=cache,
    )


def _fact_for(result, query_ref):
    execution = next(item for item in result.i03_results if item.query_ref == query_ref)
    assert len(execution.facts) == 1
    return execution.facts[0]


def test_direct_composition_parity_and_complete_object_graph():
    fx = _fixture()
    observed = _execute(fx)

    repo, release = build_source_backed_c11_repository(
        fx["stream"], fx["projection"]
    )
    direct = CarrierNeutralResearchExecutor(
        repository=repo,
        release_refs=(release.release_ref,),
        runtime_catalog=fx["catalog"],
    )
    direct_i03 = tuple(
        direct.execute_i03(query_ref=req.query_ref, predicate_ref=req.predicate_ref)
        for req in fx["requests"]
    )
    direct_i05 = direct.execute_i05(
        discovery_authority_ref=fx["discovery_authority"].ref
    )

    assert observed.c11_release.release_ref == release.release_ref
    assert observed.c11_release.replay_manifest.ref == release.replay_manifest.ref
    assert tuple(
        tuple(f.ref for f in item.facts) for item in observed.i03_results
    ) == tuple(tuple(f.ref for f in item.facts) for item in direct_i03)
    assert observed.i05_result.evaluated_frontier_ref == direct_i05.evaluated_frontier_ref
    assert tuple(r.ref for r in observed.i05_result.receipts) == tuple(
        r.ref for r in direct_i05.receipts
    )
    assert observed.learned_empirical_execution_receipt == (
        learned_empirical_execution_receipt(direct_i05)
    )
    assert route_b.verify_route_b_replay_receipt(observed.replay_receipt) == (
        observed.replay_receipt["dependency_root"]
    )
    assert observed.object_graph.empirical_facts
    assert observed.object_graph.discovery_receipts
    assert observed.object_graph.authority_snapshots


def test_source_projection_mismatch_fails_closed_before_execution():
    fx = _fixture()
    hostile = ExactPhysicalCellStream(
        source_sha256=_h("hostile-different-source"),
        row_count=fx["stream"].row_count,
        cell_iter_factory=fx["stream"].cell_iter_factory,
    )
    with pytest.raises(route_b.RouteBProductionError, match="source/projection"):
        route_b.execute_route_b_production(
            source=hostile,
            projection=fx["projection"],
            runtime_catalog=fx["catalog"],
            i03_requests=fx["requests"],
            discovery_authority_ref=fx["discovery_authority"].ref,
        )


def test_missing_or_substituted_projection_authority_fails_closed():
    fx = _fixture()
    substitute = _auth(
        "m01-substitute-projection",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=(
            "RespondentEvent@1.0.0",
            "EmpiricalCoordinateFact@1.0.0",
            "WeightMeasureFact@1.0.0",
        ),
    )
    authorities = tuple(
        auth
        for auth in fx["catalog"].authorities
        if auth.authority_ref != fx["projection_auth"].authority_ref
    ) + (substitute,)
    hostile = RuntimeObjectCatalog(
        authorities=authorities,
        predicates=fx["catalog"].predicates,
        queries=fx["catalog"].queries,
        discovery_authorities=fx["catalog"].discovery_authorities,
    )
    with pytest.raises(route_b.RouteBProductionError, match="projection authority"):
        _execute(fx, catalog=hostile)


def test_catalog_query_predicate_and_discovery_substitution_fail_closed():
    fx = _fixture()

    wrong_request = (
        route_b.I03ExecutionRequest(fx["raw_query"].ref, fx["x1"].ref),
    )
    with pytest.raises(CarrierExecutionBindingError):
        _execute(fx, requests=wrong_request)

    absent_query_catalog = RuntimeObjectCatalog(
        authorities=fx["catalog"].authorities,
        predicates=fx["catalog"].predicates,
        queries=(fx["weighted_query"],),
        discovery_authorities=fx["catalog"].discovery_authorities,
    )
    with pytest.raises(CarrierExecutionBindingError, match="query_ref"):
        _execute(
            fx,
            catalog=absent_query_catalog,
            requests=(fx["requests"][0],),
        )

    with pytest.raises(CarrierExecutionBindingError, match="discovery_authority_ref"):
        _execute(
            fx,
            discovery_ref=ExactRef(
                "DiscoveryAuthority@1.0.0",
                "urn:test:m01:absent-discovery",
                _h("absent-discovery"),
            ),
        )


def test_catalog_order_invariance():
    fx = _fixture()
    a = _execute(fx)
    reversed_catalog = RuntimeObjectCatalog(
        authorities=tuple(reversed(fx["catalog"].authorities)),
        predicates=tuple(reversed(fx["catalog"].predicates)),
        queries=tuple(reversed(fx["catalog"].queries)),
        discovery_authorities=tuple(reversed(fx["catalog"].discovery_authorities)),
    )
    b = _execute(fx, catalog=reversed_catalog)
    assert a.replay_receipt["dependency_root"] == b.replay_receipt["dependency_root"]
    assert a.replay_receipt["receipt_identity"] == b.replay_receipt["receipt_identity"]
    assert a.c11_release.release_ref == b.c11_release.release_ref
    assert tuple(r.ref for r in a.i05_result.receipts) == tuple(
        r.ref for r in b.i05_result.receipts
    )


def test_cache_drop_rebuild_is_semantically_invariant():
    fx = _fixture()
    cache = SourceBackedC11SessionCache()
    a = _execute(fx, cache=cache)
    assert cache.entry_count == 1
    cache.clear()
    assert cache.entry_count == 0
    b = _execute(fx, cache=cache)
    assert a.c11_release.release_ref == b.c11_release.release_ref
    assert a.c11_release.replay_manifest.ref == b.c11_release.replay_manifest.ref
    assert a.replay_receipt["dependency_root"] == b.replay_receipt["dependency_root"]
    assert a.replay_receipt["receipt_identity"] == b.replay_receipt["receipt_identity"]


def test_valid_empty_and_typed_absences_survive_packaging():
    fx = _fixture(valid_empty=True)
    result = _execute(fx)
    assert result.i05_result.valid_empty is True
    assert result.i05_result.receipts[0].typed_state == "VALID_EMPTY"
    states = result.replay_receipt["typed_states"]
    assert "VALID_EMPTY" in states["conserved_terminal_or_negative_states"]
    assert states["projection_typed_absence_states"] == {
        "source_relations": "DISTINCT_BY_DEFAULT",
        "predicate_replay": "NOT_APPLICABLE",
        "comparator_replay": "DEFERRED",
        "discovery_replay": "DEFERRED",
        "structural_replay": "NOT_APPLICABLE",
    }
    assert "NOT_APPLICABLE" in states["conserved_terminal_or_negative_states"]


def test_raw_and_weighted_are_distinct_and_missing_weight_never_defaults_to_one():
    fx = _fixture()
    result = _execute(fx)
    raw = _fact_for(result, fx["raw_query"].ref)
    weighted = _fact_for(result, fx["weighted_query"].ref)
    assert raw.measure_kind == "RAW"
    assert weighted.measure_kind == "GOVERNED_WEIGHTED"
    assert raw.weighted_denominator_support_if_authorized is None
    assert weighted.weighted_denominator_support_if_authorized == {
        "$exact_fraction": [3, 1],
    }
    assert raw.raw_denominator_support == weighted.raw_denominator_support == 2

    missing = _fixture(missing_weight=True)
    missing_result = _execute(missing)
    missing_weighted = _fact_for(
        missing_result, missing["weighted_query"].ref
    )
    assert missing_weighted.typed_state == "UNAVAILABLE"
    assert missing_weighted.p02_failure_state == "MEASURE_UNAVAILABLE"
    assert missing_weighted.weighted_denominator_support_if_authorized is None
    assert "WEIGHT_MISSING" in missing_weighted.execution_detail


def test_risk_set_identity_and_ordered_repeated_topology_are_preserved():
    fx = _fixture()
    result = _execute(fx)
    for execution in result.i03_results:
        query = fx["catalog"].resolve_query_exact(execution.query_ref)
        for fact in execution.facts:
            assert fact.risk_set_ref == query.risk_set_ref
            assert dict(fact.risk_set_ref) == fx["risk"].as_dict()

    events = [
        obj
        for obj in result.c11_release.public_objects
        if obj.schema_id == "RespondentEvent"
    ]
    ordered = [
        obj
        for obj in events
        if dict(obj.native_question_ref) == fx["qrefs"]["O"].as_dict()
    ]
    repeated = [
        obj
        for obj in events
        if dict(obj.native_question_ref) == fx["qrefs"]["R"].as_dict()
    ]
    assert len(ordered) == 6
    assert len(repeated) == 6
    assert {obj.multiplicity_order_rank_fields["semantic_ordinal"] for obj in ordered} == {
        0,
        1,
    }
    assert {obj.multiplicity_order_rank_fields["multiplicity_index"] for obj in repeated} == {
        0,
        1,
    }


def test_exact_replay_identity_and_tamper_fail_closed():
    fx = _fixture()
    a = _execute(fx)
    b = _execute(fx)
    assert a.replay_receipt["dependency_root"] == b.replay_receipt["dependency_root"]
    assert a.replay_receipt["receipt_identity"] == b.replay_receipt["receipt_identity"]

    tampered = deepcopy(a.replay_receipt)
    tampered["dependency_material"]["i05"]["candidate_count"] += 1
    with pytest.raises(route_b.RouteBProductionError, match="dependency root"):
        route_b.verify_route_b_replay_receipt(tampered)

    tampered_preimage = deepcopy(a.replay_receipt)
    tampered_preimage["object_preimages"]["empirical_facts"][0]["typed_state"] = (
        "NONCOMPARABLE"
    )
    # Re-hash the outer envelope to prove the exact public-object constructor,
    # not merely the envelope checksum, rejects semantic-preimage substitution.
    tampered_preimage["receipt_identity"] = route_b.semantic_hash(
        {
            key: value
            for key, value in tampered_preimage.items()
            if key != "receipt_identity"
        }
    )
    with pytest.raises((CarrierExecutionBindingError, route_b.RouteBProductionError)):
        route_b.verify_route_b_replay_receipt(tampered_preimage)


def test_no_currentness_structural_causal_v3_or_historical_stage_resurrection():
    fx = _fixture()
    result = _execute(fx)
    assert result.replay_receipt["effects"] == {
        "learned_empirical_adjudication_effect": False,
        "learned_product_publication_effect": False,
        "learned_product_current_selection_effect": False,
        "structural_truth_effect": False,
        "causal_truth_effect": False,
        "actor_v3_effect": False,
    }
    assert result.learned_empirical_execution_receipt["structural_truth_effect"] is False
    assert result.learned_empirical_execution_receipt["causal_truth_effect"] is False
    assert result.learned_empirical_execution_receipt["actor_v3_effect"] is False
    assert not any(
        isinstance(obj, StructuralEmpiricalAdmission)
        for obj in result.object_graph.public_objects()
    )

    source = inspect.getsource(route_b).lower()
    import_surface = "\n".join(
        line for line in source.splitlines()
        if line.startswith("from ") or line.startswith("import ")
    )
    forbidden_imports = (
        "fiabc",
        "astra",
        "candidate_a",
        "candidate_b",
        "candidate_c",
        "pre553_structural_admission",
        "field_forge",
        "wave1_ff_prev3",
        "v3_adp",
    )
    assert all(token not in import_surface for token in forbidden_imports)
