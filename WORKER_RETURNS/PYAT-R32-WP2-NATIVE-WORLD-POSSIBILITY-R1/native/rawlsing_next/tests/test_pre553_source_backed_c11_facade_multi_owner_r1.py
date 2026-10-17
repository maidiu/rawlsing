from dataclasses import replace

import pytest

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_empirical_objects import EmpiricalCoordinateFact, EmpiricalUniverse, ExactRef, RespondentEvent, RoutingEligibilityFact, semantic_hash
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
    CONTRACT_ID,
    COORDINATE_OWNER_FAMILY,
    RESPONSE_OWNER_FAMILY,
    CoordinateSlotRule,
    ExactPhysicalCellStream,
    GovernedC11Projection,
    OccurrenceRule,
    PhysicalSlot,
    PhysicalSlotOwnerAuthorization,
    PhysicalSlotOwnerSet,
    ResponseSlotRule,
    ResponseValueRule,
    RowRespondentBinding,
    SLOT_OWNER_SET_CONTRACT_ID,
    SourceBackedC11FacadeError,
    build_validated_source_backed_c11_release_from_stream,
    physical_value_binding_key,
)
from rawlsing_next.tests.test_pre553_empirical_query import _auth, _h, _ref


WVS7_COORDINATE_DUAL_OWNER_42 = (
    "Q138", "Q173", "Q260", "Q261", "Q262", "Q263", "Q264", "Q265", "Q266", "Q267", "Q268",
    "Q269", "Q270", "Q271", "Q272", "Q273", "Q274", "Q275", "Q275A", "Q276", "Q276A", "Q277",
    "Q277A", "Q278", "Q278A", "Q279", "Q280", "Q284", "Q287", "Q288", "Q47", "Q51", "Q52", "Q53",
    "Q54", "Q55", "Q56", "V001", "V001A_01", "V002", "V002A_01", "X002_02B",
)


def _fixture(*, dual_owner: bool, explicit_owner_set: bool = False):
    source_auth = _auth("multi-owner-source", "SOURCE_SEMANTICS_TOPOLOGY",
                        families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0"))
    coord_auth = _auth("multi-owner-coordinate", "COORDINATE_SEMANTICS",
                       families=("EmpiricalCoordinateFact@1.0.0",))
    routing_auth = _auth("multi-owner-routing", "ROUTING_RISK_SET",
                         families=("RoutingEligibilityFact@1.0.0",))
    replay_auth = _auth("multi-owner-replay", "REPLAY_PROTOCOL", families=("ReplayReceipt@1.0.0",))
    projection_auth = _auth("multi-owner-projection", "SOURCE_SEMANTICS_TOPOLOGY",
                            families=("RespondentEvent@1.0.0", "EmpiricalCoordinateFact@1.0.0"))
    response_owner_auth = _auth("multi-owner-response-owner", "SOURCE_SEMANTICS_TOPOLOGY",
                                families=(RESPONSE_OWNER_FAMILY,))
    coordinate_owner_auth = _auth("multi-owner-coordinate-owner", "COORDINATE_SEMANTICS",
                                  families=(COORDINATE_OWNER_FAMILY,))

    authorities = [source_auth, coord_auth, routing_auth, replay_auth, projection_auth]
    if explicit_owner_set:
        authorities.extend((response_owner_auth, coordinate_owner_auth))
    authorities = tuple(authorities)

    source_sha = _h("c05-r2a-multi-owner-focused-source")
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "multi-owner-universe"),
        raw_source_identity="RAW-C05-R2A-MULTI-OWNER",
        source_family="SURVEY",
        study_product_release="STUDY-C05-R2A/REL-1",
        instrument_release="INST-C05-R2A",
        country_geography="US",
        sampling_geography="US-NATIONAL",
        raw_wave="W1",
        canonical_wave_if_governed=None,
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="ADULTS",
        sampling_design_regime="DESIGN-C05-R2A",
        respondent_namespace="NS-C05-R2A",
        source_artifact_import_lineage="SOURCE-LINEAGE-C05-R2A",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    respondent = RespondentIdentity(
        empirical_universe_ref=universe.ref,
        respondent_key="R1",
        source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", "multi-owner-R1"),
        identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
    )
    qref = _ref("QUESTION_NATIVE", "multi-owner-X")
    question = QuestionVariableBinding(
        empirical_universe_ref=universe.ref,
        native_question_ref=qref,
        instrument_question_version="1",
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
        component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=source_auth.authority_ref,
        topology_authority_ref=source_auth.authority_ref,
    )
    routing = RoutingEligibilityFact(
        typed_state="ELIGIBLE_APPLICABLE",
        authority_snapshot_refs=(routing_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "multi-owner-routing-R1-X"),
        empirical_universe_ref=universe.ref,
        scoped_respondent_ref=respondent.ref,
        question_or_target_ref=qref,
        risk_set_ref=_ref("RISK_SET", "multi-owner-R"),
        routing_rule_ref=_ref("ROUTING_RULE", "multi-owner-X"),
        applicability_state="ELIGIBLE_APPLICABLE",
        routing_state="ELIGIBLE_APPLICABLE",
        parent_predicate_refs=(),
        member_set_replay_ref=_ref("MEMBER_SET", "multi-owner-X-R1"),
    )

    pkey = physical_value_binding_key("1", PhysicalMissingState.OBSERVED_STORAGE_VALUE)
    slot_x = PhysicalSlot(1, "X")
    response_slot = ResponseSlotRule(
        slot_x,
        question,
        (ResponseValueRule(
            pkey,
            "SUBSTANTIVE_RESPONSE",
            (OccurrenceRule("0", _ref("TOPOLOGY", "multi-owner-X-SCALAR"),
                            {"kind": "SCALAR_SINGULAR", "index": 0}),),
        ),),
    )
    coordinate_slot = CoordinateSlotRule(
        slot_x if dual_owner else PhysicalSlot(2, "G"),
        _ref("COORDINATE_NATIVE", "multi-owner-X" if dual_owner else "multi-owner-G"),
        _ref("UNIT_TAXONOMY", "multi-owner-position"),
        "2026-01",
        coord_auth.authority_ref,
        copy_observed_raw=True,
    )

    owner_sets = ()
    if explicit_owner_set:
        owner_sets = (
            PhysicalSlotOwnerSet(
                slot_x,
                (
                    PhysicalSlotOwnerAuthorization(RESPONSE_OWNER_FAMILY, (response_owner_auth.authority_ref,)),
                    PhysicalSlotOwnerAuthorization(COORDINATE_OWNER_FAMILY, (coordinate_owner_auth.authority_ref,)),
                ),
            ),
        )

    projection = GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", "multi-owner-focused"),
        source_artifact_id="SOURCE-C05-R2A-MULTI-OWNER",
        expected_source_sha256=source_sha,
        source_family_id="SURVEY",
        study_product_id="STUDY-C05-R2A",
        release_id="REL-C05-R2A",
        instrument_release_id="INST-C05-R2A",
        source_snapshot_retention_ref=ExactRef("SOURCE_SNAPSHOT", "urn:test:c05r2a:multi-owner-snapshot", source_sha),
        universes=(universe,),
        respondents=(respondent,),
        row_bindings=(RowRespondentBinding(1, respondent.ref),),
        questions=(question,),
        response_slots=(response_slot,),
        coordinate_slots=(coordinate_slot,),
        routing=(routing,),
        weight_slots=(),
        authority_snapshots=authorities,
        source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(a.authority_ref for a in authorities),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=_ref("ORDER_RULE", "CANONICAL-REF-SORT"),
        replay_protocol_version="1.0.0",
        slot_owner_sets=owner_sets,
    )

    cells = [PhysicalCell(1, 1, "X", "1", PhysicalMissingState.OBSERVED_STORAGE_VALUE, None)]
    if not dual_owner:
        cells.append(PhysicalCell(1, 2, "G", "US", PhysicalMissingState.OBSERVED_STORAGE_VALUE, None))
    stream = ExactPhysicalCellStream(source_sha, 1, lambda: iter(tuple(cells)))
    return {
        "projection": projection,
        "stream": stream,
        "respondent": respondent,
        "question": question,
        "pkey": pkey,
        "response_owner_auth": response_owner_auth,
        "coordinate_owner_auth": coordinate_owner_auth,
        "coord_auth": coord_auth,
    }


def _objects(release, cls):
    return tuple(x for x in release.public_objects if isinstance(x, cls))


def test_generic_single_owner_identity_parity_preserves_v1_contract_material():
    fx = _fixture(dual_owner=False)
    p = fx["projection"]
    release = build_validated_source_backed_c11_release_from_stream(fx["stream"], p)
    events = _objects(release, RespondentEvent)
    coords = _objects(release, EmpiricalCoordinateFact)
    assert len(events) == 1
    assert len(coords) == 1

    legacy_cache_material = {
        "contract": CONTRACT_ID,
        "projection_identity_ref": p.projection_identity_ref.as_dict(),
        "source_sha256": p.expected_source_sha256,
        "required_authority_refs": [x.as_dict() for x in sorted(p.required_authority_refs, key=lambda r: r.key)],
    }
    assert p.cache_identity == semantic_hash(legacy_cache_material)

    event_material = {
        "contract": CONTRACT_ID,
        "projection": p.projection_identity_ref.as_dict(),
        "source_sha": p.expected_source_sha256,
        "row": 1,
        "respondent": fx["respondent"].ref.as_dict(),
        "question": fx["question"].ref.as_dict(),
        "slot": (1, "X"),
        "physical_value_key": fx["pkey"],
        "occurrence": "0",
    }
    assert events[0].producer_replay_locator_or_reference_root.content_hash == semantic_hash(event_material)


def test_explicit_legal_response_coordinate_multi_owner_emits_both_and_replays_deterministically():
    fx = _fixture(dual_owner=True, explicit_owner_set=True)
    p = fx["projection"]
    first = build_validated_source_backed_c11_release_from_stream(fx["stream"], p)
    second = build_validated_source_backed_c11_release_from_stream(fx["stream"], p)

    events = _objects(first, RespondentEvent)
    coords = _objects(first, EmpiricalCoordinateFact)
    assert len(events) == 1
    assert len(coords) == 1
    assert fx["response_owner_auth"].authority_ref in events[0].authority_snapshot_refs
    assert fx["coordinate_owner_auth"].authority_ref in coords[0].authority_snapshot_refs
    assert first.release_ref == second.release_ref
    assert first.replay_manifest.ref == second.replay_manifest.ref
    assert tuple(x.ref for x in first.public_objects) == tuple(x.ref for x in second.public_objects)

    owner_set = p.slot_owner_sets[0]
    reversed_owner_set = PhysicalSlotOwnerSet(owner_set.slot, tuple(reversed(owner_set.owners)))
    p_reordered = replace(p, slot_owner_sets=(reversed_owner_set,))
    reordered = build_validated_source_backed_c11_release_from_stream(fx["stream"], p_reordered)
    assert reordered.release_ref == first.release_ref
    assert reordered.replay_manifest.ref == first.replay_manifest.ref


def test_implicit_or_malformed_multi_owner_fails_closed():
    with pytest.raises(SourceBackedC11FacadeError, match="implicit/unapproved second"):
        _fixture(dual_owner=True, explicit_owner_set=False)

    fx = _fixture(dual_owner=True, explicit_owner_set=True)
    owner = fx["projection"].slot_owner_sets[0].owners[0]
    with pytest.raises(SourceBackedC11FacadeError, match="conflicting duplicate"):
        PhysicalSlotOwnerSet(PhysicalSlot(1, "X"), (owner, owner))
    with pytest.raises(SourceBackedC11FacadeError, match="unsupported physical-slot semantic owner family"):
        PhysicalSlotOwnerAuthorization("UnsupportedFamily@1.0.0", (fx["response_owner_auth"].authority_ref,))


def test_accepted_wvs7_42_slot_authority_shape_is_representable_without_source_special_case():
    assert len(WVS7_COORDINATE_DUAL_OWNER_42) == 42
    assert len(set(WVS7_COORDINATE_DUAL_OWNER_42)) == 42
    assert tuple(sorted(WVS7_COORDINATE_DUAL_OWNER_42)) == tuple(sorted(set(WVS7_COORDINATE_DUAL_OWNER_42)))

    response_owner = _auth("wvs7-shape-response-owner", "SOURCE_SEMANTICS_TOPOLOGY",
                           families=(RESPONSE_OWNER_FAMILY,)).authority_ref
    coordinate_owner = _auth("wvs7-shape-coordinate-owner", "COORDINATE_SEMANTICS",
                             families=(COORDINATE_OWNER_FAMILY,)).authority_ref
    owner_sets = tuple(
        PhysicalSlotOwnerSet(
            PhysicalSlot(i, name),
            (
                PhysicalSlotOwnerAuthorization(COORDINATE_OWNER_FAMILY, (coordinate_owner,)),
                PhysicalSlotOwnerAuthorization(RESPONSE_OWNER_FAMILY, (response_owner,)),
            ),
        )
        for i, name in enumerate(WVS7_COORDINATE_DUAL_OWNER_42, 1)
    )
    assert len(owner_sets) == 42
    assert all(x.contract_id == SLOT_OWNER_SET_CONTRACT_ID for x in owner_sets)
    assert all(x.owner_families == tuple(sorted((RESPONSE_OWNER_FAMILY, COORDINATE_OWNER_FAMILY))) for x in owner_sets)
    assert tuple(x.slot.name for x in owner_sets) == WVS7_COORDINATE_DUAL_OWNER_42
