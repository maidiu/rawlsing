from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry, Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    RoutingEligibilityFact,
    WeightMeasureFact,
)
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
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
    build_source_backed_c11_repository,
    build_validated_source_backed_c11_release_from_stream,
    execute_source_backed_empirical_query,
    physical_value_binding_key,
)
from rawlsing_next.tests.test_pre553_empirical_query import (
    _auth,
    _branch_predicate,
    _h,
    _query,
    _query_authority,
    _ref,
)


R2_SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
R2_SOURCE_BYTES = 185_163_494
R2_SELECTED_DECODE_SHA256 = "7e69d799e37d26c2e6ae749674d4994a276f93aaf89e43085bed34a5fd122ec9"
R2_RESPONDENTS = 97_220
R2_SOURCE_LOCAL_SCOPES = 66
R2_LOGICAL_SLOTS = 613
R2_PROJECTED_SLOTS = 612
R2_SOLE_EXCLUSION = "PWGHT"
R2_ROUTING_DOCUMENTARY = 222
R2_ROUTING_D03 = 9

ACCEPTED_WVS7_DUAL_ROLE_42 = (
    "Q138", "Q173", "Q260", "Q261", "Q262", "Q263", "Q264", "Q265", "Q266", "Q267", "Q268",
    "Q269", "Q270", "Q271", "Q272", "Q273", "Q274", "Q275", "Q275A", "Q276", "Q276A", "Q277",
    "Q277A", "Q278", "Q278A", "Q279", "Q280", "Q284", "Q287", "Q288", "Q47", "Q51", "Q52", "Q53",
    "Q54", "Q55", "Q56", "V001", "V001A_01", "V002", "V002A_01", "X002_02B",
)

EXPECTED_D03 = ("Q276", "Q276A", "Q277", "Q277A", "Q278", "Q278A", "Q280", "Q282", "Q283")


def _objects(release, cls):
    return tuple(obj for obj in release.public_objects if isinstance(obj, cls))


def _fixture():
    source_auth = _auth(
        "hb01-r2-source", "SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", RESPONSE_OWNER_FAMILY),
    )
    coordinate_auth = _auth(
        "hb01-r2-coordinate", "COORDINATE_SEMANTICS",
        families=(COORDINATE_OWNER_FAMILY,),
    )
    routing_auth = _auth(
        "hb01-r2-routing", "ROUTING_RISK_SET",
        families=("RoutingEligibilityFact@1.0.0",),
    )
    replay_auth = _auth(
        "hb01-r2-replay", "REPLAY_PROTOCOL",
        families=("ReplayReceipt@1.0.0",),
    )
    projection_auth = _auth(
        "hb01-r2-projection", "SOURCE_SEMANTICS_TOPOLOGY",
        families=(RESPONSE_OWNER_FAMILY, COORDINATE_OWNER_FAMILY),
    )
    response_owner = _auth(
        "hb01-r2-response-owner", "SOURCE_SEMANTICS_TOPOLOGY",
        families=(RESPONSE_OWNER_FAMILY,),
    )
    coordinate_owner = _auth(
        "hb01-r2-coordinate-owner", "COORDINATE_SEMANTICS",
        families=(COORDINATE_OWNER_FAMILY,),
    )
    authorities = (
        source_auth, coordinate_auth, routing_auth, replay_auth,
        projection_auth, response_owner, coordinate_owner,
    )
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "hb01-r2-universe"),
        raw_source_identity=R2_SOURCE_SHA256,
        source_family="WVS7",
        study_product_release="WVS7/R2-CERTIFICATION",
        instrument_release="WVS7-WAVE7",
        country_geography="SOURCE_LOCAL",
        sampling_geography="SOURCE_LOCAL",
        raw_wave="7",
        canonical_wave_if_governed=None,
        field_or_reference_time="WVS7",
        target_population_and_sample_frame="NO_POPULATION_GENERALIZATION",
        sampling_design_regime="DESIGN_AUTHORITY_NOT_PROMOTED",
        respondent_namespace="WVS7-SOURCE-ROW",
        source_artifact_import_lineage=R2_SOURCE_SHA256,
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    respondent = RespondentIdentity(
        empirical_universe_ref=universe.ref,
        respondent_key="SOURCE_ROW_1",
        source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", "hb01-r2-row-1"),
        identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
    )
    risk_ref = _ref("RISK_SET", "hb01-r2-routing-unknown")
    pkey = physical_value_binding_key("1", PhysicalMissingState.OBSERVED_STORAGE_VALUE)
    questions = []
    response_slots = []
    coordinate_slots = []
    routing = []
    owner_sets = []
    cells = []
    qrefs = {}
    for ordinal, name in enumerate(ACCEPTED_WVS7_DUAL_ROLE_42, 1):
        qref = _ref("QUESTION_NATIVE", f"hb01-r2-{name}")
        qrefs[name] = qref
        question = QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=qref,
            instrument_question_version="WVS7",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref,
        )
        questions.append(question)
        slot = PhysicalSlot(ordinal, name)
        response_slots.append(ResponseSlotRule(
            slot,
            question,
            (ResponseValueRule(
                pkey,
                "SUBSTANTIVE_RESPONSE",
                (OccurrenceRule(
                    "0", _ref("TOPOLOGY", f"hb01-r2-{name}"),
                    {"kind": "SCALAR_SINGULAR", "index": 0},
                ),),
            ),),
        ))
        coordinate_slots.append(CoordinateSlotRule(
            slot,
            _ref("COORDINATE_NATIVE", f"hb01-r2-{name}"),
            _ref("UNIT_TAXONOMY", "hb01-r2-source-coordinate"),
            "WVS7",
            coordinate_auth.authority_ref,
            copy_observed_raw=True,
        ))
        routing.append(RoutingEligibilityFact(
            typed_state="ROUTING_UNKNOWN",
            authority_snapshot_refs=(routing_auth.authority_ref,),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"hb01-r2-routing-{name}"),
            empirical_universe_ref=universe.ref,
            scoped_respondent_ref=respondent.ref,
            question_or_target_ref=qref,
            risk_set_ref=risk_ref,
            routing_rule_ref=_ref("ROUTING_RULE", f"hb01-r2-{name}"),
            applicability_state="ROUTING_UNKNOWN",
            routing_state="ROUTING_UNKNOWN",
            parent_predicate_refs=(),
            member_set_replay_ref=_ref("MEMBER_SET", f"hb01-r2-{name}"),
        ))
        owner_sets.append(PhysicalSlotOwnerSet(slot, (
            PhysicalSlotOwnerAuthorization(RESPONSE_OWNER_FAMILY, (response_owner.authority_ref,)),
            PhysicalSlotOwnerAuthorization(COORDINATE_OWNER_FAMILY, (coordinate_owner.authority_ref,)),
        )))
        cells.append(PhysicalCell(
            1, ordinal, name, "1", PhysicalMissingState.OBSERVED_STORAGE_VALUE, None,
        ))
    cells.append(PhysicalCell(
        1, 999, R2_SOLE_EXCLUSION, "2.5", PhysicalMissingState.OBSERVED_STORAGE_VALUE, None,
    ))
    projection = GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", "hb01-r2-full-gsr07"),
        source_artifact_id="WVS7-SOURCE-R2",
        expected_source_sha256=R2_SOURCE_SHA256,
        source_family_id="WVS7",
        study_product_id="WVS7",
        release_id="WAVE7-R2",
        instrument_release_id="WVS7-WAVE7",
        source_snapshot_retention_ref=ExactRef("SOURCE_SNAPSHOT", "urn:rawlsing:wvs7:r2:snapshot", R2_SOURCE_SHA256),
        universes=(universe,),
        respondents=(respondent,),
        row_bindings=(RowRespondentBinding(1, respondent.ref),),
        questions=tuple(questions),
        response_slots=tuple(response_slots),
        coordinate_slots=tuple(coordinate_slots),
        routing=tuple(routing),
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
        tie_order_ref=_ref("ORDER_RULE", "HB01-R2-CANONICAL-REF-SORT"),
        replay_protocol_version="1.0.0",
        slot_owner_sets=tuple(owner_sets),
    )
    stream = ExactPhysicalCellStream(R2_SOURCE_SHA256, 1, lambda: iter(tuple(cells)))
    return {
        "projection": projection,
        "stream": stream,
        "universe": universe,
        "respondent": respondent,
        "qrefs": qrefs,
        "risk_ref": risk_ref,
        "authorities": authorities,
        "source_auth": source_auth,
        "response_owner": response_owner,
        "coordinate_owner": coordinate_owner,
    }


def test_frozen_real_source_certification_constants_are_exact_and_noncollapsed():
    assert R2_SOURCE_SHA256 == "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
    assert R2_SOURCE_BYTES == 185_163_494
    assert R2_SELECTED_DECODE_SHA256 == "7e69d799e37d26c2e6ae749674d4994a276f93aaf89e43085bed34a5fd122ec9"
    assert R2_LOGICAL_SLOTS == 613 and R2_PROJECTED_SLOTS == 612
    assert R2_SOURCE_LOCAL_SCOPES == 66 and R2_RESPONDENTS == 97_220
    assert len(ACCEPTED_WVS7_DUAL_ROLE_42) == 42
    assert len(set(ACCEPTED_WVS7_DUAL_ROLE_42)) == 42
    assert R2_ROUTING_DOCUMENTARY == 222 and R2_ROUTING_D03 == len(EXPECTED_D03) == 9


def test_exact_42_dual_owner_slots_release_deterministically_without_weight_promotion():
    fx = _fixture()
    first = build_validated_source_backed_c11_release_from_stream(fx["stream"], fx["projection"])
    second = build_validated_source_backed_c11_release_from_stream(fx["stream"], fx["projection"])
    assert len(_objects(first, RespondentEvent)) == 42
    assert len(_objects(first, EmpiricalCoordinateFact)) == 42
    assert len(_objects(first, RoutingEligibilityFact)) == 42
    assert all(x.typed_state == "ROUTING_UNKNOWN" for x in _objects(first, RoutingEligibilityFact))
    assert not _objects(first, WeightMeasureFact)
    assert first.release_ref == second.release_ref
    assert first.replay_manifest.ref == second.replay_manifest.ref
    assert tuple(x.ref for x in first.public_objects) == tuple(x.ref for x in second.public_objects)
    assert all(R2_SOLE_EXCLUSION not in x.ref.object_id for x in first.public_objects)


def test_owner_family_authority_closure_is_exact_and_reciprocal_substitution_fails_closed():
    fx = _fixture()
    p = fx["projection"]
    current = p.slot_owner_sets[0]
    bad_response_owners = tuple(
        PhysicalSlotOwnerAuthorization(
            owner.owner_family,
            (fx["coordinate_owner"].authority_ref,) if owner.owner_family == RESPONSE_OWNER_FAMILY else owner.authority_refs,
        )
        for owner in current.owners
    )
    with pytest.raises(Pre553AuthorityError):
        replace(p, slot_owner_sets=(PhysicalSlotOwnerSet(current.slot, bad_response_owners), *p.slot_owner_sets[1:]))
    bad_coordinate_owners = tuple(
        PhysicalSlotOwnerAuthorization(
            owner.owner_family,
            (fx["response_owner"].authority_ref,) if owner.owner_family == COORDINATE_OWNER_FAMILY else owner.authority_refs,
        )
        for owner in current.owners
    )
    with pytest.raises(Pre553AuthorityError):
        replace(p, slot_owner_sets=(PhysicalSlotOwnerSet(current.slot, bad_coordinate_owners), *p.slot_owner_sets[1:]))


def test_source_backed_c11_release_is_frozen_i03_eligible_and_wrapper_matches_direct_executor():
    fx = _fixture()
    repo, release = build_source_backed_c11_repository(fx["stream"], fx["projection"])
    qa = _query_authority("hb01-r2-frozen-i03")
    source = {
        "repo": repo,
        "release_ref": release.release_ref,
        "universe": fx["universe"],
        "respondents": {"SOURCE_ROW_1": fx["respondent"]},
        "qrefs": fx["qrefs"],
        "risk_refs": {"R": fx["risk_ref"]},
        "authorities": fx["authorities"],
        "source_auth": fx["source_auth"],
    }
    predicate = _branch_predicate(source, qa, tag="hb01-r2")
    query = _query(source, qa, predicate, (ACCEPTED_WVS7_DUAL_ROLE_42[0],), tag="hb01-r2")
    registry = AuthorityRegistry((*fx["authorities"], qa))
    direct = execute_empirical_query(
        repository=repo,
        query=query,
        predicate=predicate,
        authority_registry=registry,
        release_refs=(release.release_ref,),
    )
    wrapped = execute_source_backed_empirical_query(
        source=fx["stream"],
        projection=fx["projection"],
        query=query,
        predicate=predicate,
        authority_registry=registry,
    )
    assert direct.query_ref == wrapped.query_ref
    assert direct.release_refs == wrapped.release_refs == (release.release_ref,)
    assert tuple(x.ref for x in direct.facts) == tuple(x.ref for x in wrapped.facts)
    assert direct.facts and all(x.typed_state in {"SUPPORTED", "ZERO_SUPPORT"} for x in direct.facts)
