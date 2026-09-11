from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError, require_positive_authority
from rawlsing_next.pre553_empirical_objects import (
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    RoutingEligibilityFact,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
    COORDINATE_OWNER_FAMILY,
    RESPONSE_OWNER_FAMILY,
    WEIGHT_OWNER_FAMILY,
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
    SourceBackedC11FacadeError,
    WeightSlotRule,
    build_validated_source_backed_c11_release_from_stream,
    physical_value_binding_key,
)
from rawlsing_next.tests.test_pre553_empirical_query import _auth, _h, _ref


def _build_dual_owner_release(response_owner_snapshot, coordinate_owner_snapshot=None):
    source_auth = _auth(
        "qual-source",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", RESPONSE_OWNER_FAMILY),
    )
    coordinate_auth = _auth(
        "qual-coordinate",
        "COORDINATE_SEMANTICS",
        families=(COORDINATE_OWNER_FAMILY,),
    )
    routing_auth = _auth(
        "qual-routing",
        "ROUTING_RISK_SET",
        families=("RoutingEligibilityFact@1.0.0",),
    )
    replay_auth = _auth(
        "qual-replay",
        "REPLAY_PROTOCOL",
        families=("ReplayReceipt@1.0.0",),
    )
    projection_auth = _auth(
        "qual-projection",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=(RESPONSE_OWNER_FAMILY, COORDINATE_OWNER_FAMILY),
    )
    coordinate_owner = coordinate_owner_snapshot or _auth(
        "qual-coordinate-owner",
        "COORDINATE_SEMANTICS",
        families=(COORDINATE_OWNER_FAMILY,),
    )

    source_sha = _h("qualification-multi-owner-authority-substitution-source")
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "qual-universe"),
        raw_source_identity="RAW-QUALIFICATION",
        source_family="SURVEY",
        study_product_release="QUALIFICATION/REL-1",
        instrument_release="QUAL-INSTRUMENT",
        country_geography="SOURCE_LOCAL",
        sampling_geography="SOURCE_LOCAL",
        raw_wave="W1",
        canonical_wave_if_governed=None,
        field_or_reference_time="2026-09-11",
        target_population_and_sample_frame="SOURCE_LOCAL_ONLY__NO_POPULATION_GENERALIZATION",
        sampling_design_regime="DESIGN_AUTHORITY_NOT_PROMOTED",
        respondent_namespace="QUAL-NS",
        source_artifact_import_lineage="QUALIFICATION-SYNTHETIC-WITNESS",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    respondent = RespondentIdentity(
        empirical_universe_ref=universe.ref,
        respondent_key="R1",
        source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", "qual-r1"),
        identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
    )
    question = QuestionVariableBinding(
        empirical_universe_ref=universe.ref,
        native_question_ref=_ref("QUESTION_NATIVE", "qual-X"),
        instrument_question_version="1",
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
        component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=source_auth.authority_ref,
        topology_authority_ref=source_auth.authority_ref,
    )
    routing = RoutingEligibilityFact(
        typed_state="ROUTING_UNKNOWN",
        authority_snapshot_refs=(routing_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "qual-routing-r1-X"),
        empirical_universe_ref=universe.ref,
        scoped_respondent_ref=respondent.ref,
        question_or_target_ref=question.native_question_ref,
        risk_set_ref=_ref("RISK_SET", "qual-risk"),
        routing_rule_ref=_ref("ROUTING_RULE", "qual-rule"),
        applicability_state="ROUTING_UNKNOWN",
        routing_state="ROUTING_UNKNOWN",
        parent_predicate_refs=(),
        member_set_replay_ref=_ref("MEMBER_SET", "qual-unknown"),
    )

    slot = PhysicalSlot(1, "X")
    physical_key = physical_value_binding_key("1", PhysicalMissingState.OBSERVED_STORAGE_VALUE)
    response_rule = ResponseSlotRule(
        slot,
        question,
        (
            ResponseValueRule(
                physical_key,
                "SUBSTANTIVE_RESPONSE",
                (
                    OccurrenceRule(
                        "0",
                        _ref("TOPOLOGY", "qual-X-scalar"),
                        {"kind": "SCALAR_SINGULAR", "index": 0},
                    ),
                ),
            ),
        ),
    )
    coordinate_rule = CoordinateSlotRule(
        slot,
        _ref("COORDINATE_NATIVE", "qual-X-coordinate"),
        _ref("UNIT_TAXONOMY", "qual-X-unit"),
        "2026-09-11",
        coordinate_auth.authority_ref,
        copy_observed_raw=True,
    )
    owner_set = PhysicalSlotOwnerSet(
        slot,
        (
            PhysicalSlotOwnerAuthorization(
                RESPONSE_OWNER_FAMILY,
                (response_owner_snapshot.authority_ref,),
            ),
            PhysicalSlotOwnerAuthorization(
                COORDINATE_OWNER_FAMILY,
                (coordinate_owner.authority_ref,),
            ),
        ),
    )

    authorities = (
        source_auth,
        coordinate_auth,
        routing_auth,
        replay_auth,
        projection_auth,
        coordinate_owner,
        response_owner_snapshot,
    )
    projection = GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", "qualification-owner-substitution"),
        source_artifact_id="QUAL-SOURCE",
        expected_source_sha256=source_sha,
        source_family_id="SURVEY",
        study_product_id="QUAL-STUDY",
        release_id="QUAL-REL-1",
        instrument_release_id="QUAL-INST-1",
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT",
            "urn:test:qualification:source-snapshot",
            source_sha,
        ),
        universes=(universe,),
        respondents=(respondent,),
        row_bindings=(RowRespondentBinding(1, respondent.ref),),
        questions=(question,),
        response_slots=(response_rule,),
        coordinate_slots=(coordinate_rule,),
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
        tie_order_ref=_ref("ORDER_RULE", "qual-canonical-ref-sort"),
        replay_protocol_version="1.0.0",
        slot_owner_sets=(owner_set,),
    )
    cell = PhysicalCell(
        1,
        1,
        "X",
        "1",
        PhysicalMissingState.OBSERVED_STORAGE_VALUE,
        None,
    )
    stream = ExactPhysicalCellStream(source_sha, 1, lambda: iter((cell,)))
    release = build_validated_source_backed_c11_release_from_stream(stream, projection)
    return release, projection, routing


def _weight_owner_projection(weight_owner_snapshot):
    source_auth = _auth(
        "qual-weight-source",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", RESPONSE_OWNER_FAMILY),
    )
    coordinate_auth = _auth(
        "qual-weight-coordinate",
        "COORDINATE_SEMANTICS",
        families=(COORDINATE_OWNER_FAMILY,),
    )
    weight_auth = _auth(
        "qual-weight-semantic",
        "WEIGHT_DESIGN_ESTIMAND",
        families=(WEIGHT_OWNER_FAMILY,),
    )
    routing_auth = _auth(
        "qual-weight-routing",
        "ROUTING_RISK_SET",
        families=("RoutingEligibilityFact@1.0.0",),
    )
    replay_auth = _auth(
        "qual-weight-replay",
        "REPLAY_PROTOCOL",
        families=("ReplayReceipt@1.0.0",),
    )
    projection_auth = _auth(
        "qual-weight-projection",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=(RESPONSE_OWNER_FAMILY, COORDINATE_OWNER_FAMILY, WEIGHT_OWNER_FAMILY),
    )
    source_sha = _h("qualification-weight-owner-family-source")
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "qual-weight-universe"),
        raw_source_identity="RAW-QUALIFICATION-WEIGHT",
        source_family="SURVEY",
        study_product_release="QUALIFICATION-WEIGHT/REL-1",
        instrument_release="QUAL-WEIGHT-INSTRUMENT",
        country_geography="SOURCE_LOCAL",
        sampling_geography="SOURCE_LOCAL",
        raw_wave="W1",
        canonical_wave_if_governed=None,
        field_or_reference_time="2026-09-11",
        target_population_and_sample_frame="SOURCE_LOCAL_ONLY__NO_POPULATION_GENERALIZATION",
        sampling_design_regime="DESIGN_AUTHORITY_NOT_PROMOTED",
        respondent_namespace="QUAL-WEIGHT-NS",
        source_artifact_import_lineage="QUALIFICATION-WEIGHT-SYNTHETIC-WITNESS",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    respondent = RespondentIdentity(
        empirical_universe_ref=universe.ref,
        respondent_key="R1",
        source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", "qual-weight-r1"),
        identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
    )
    question = QuestionVariableBinding(
        empirical_universe_ref=universe.ref,
        native_question_ref=_ref("QUESTION_NATIVE", "qual-weight-X"),
        instrument_question_version="1",
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
        component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=source_auth.authority_ref,
        topology_authority_ref=source_auth.authority_ref,
    )
    routing = RoutingEligibilityFact(
        typed_state="ROUTING_UNKNOWN",
        authority_snapshot_refs=(routing_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "qual-weight-routing-r1-X"),
        empirical_universe_ref=universe.ref,
        scoped_respondent_ref=respondent.ref,
        question_or_target_ref=question.native_question_ref,
        risk_set_ref=_ref("RISK_SET", "qual-weight-risk"),
        routing_rule_ref=_ref("ROUTING_RULE", "qual-weight-rule"),
        applicability_state="ROUTING_UNKNOWN",
        routing_state="ROUTING_UNKNOWN",
        parent_predicate_refs=(),
        member_set_replay_ref=_ref("MEMBER_SET", "qual-weight-unknown"),
    )
    response_slot = ResponseSlotRule(
        PhysicalSlot(1, "X"),
        question,
        (
            ResponseValueRule(
                physical_value_binding_key("1", PhysicalMissingState.OBSERVED_STORAGE_VALUE),
                "SUBSTANTIVE_RESPONSE",
                (
                    OccurrenceRule(
                        "0",
                        _ref("TOPOLOGY", "qual-weight-X-scalar"),
                        {"kind": "SCALAR_SINGULAR", "index": 0},
                    ),
                ),
            ),
        ),
    )
    coordinate_slot = CoordinateSlotRule(
        PhysicalSlot(2, "G"),
        _ref("COORDINATE_NATIVE", "qual-weight-G"),
        _ref("UNIT_TAXONOMY", "qual-weight-G-unit"),
        "2026-09-11",
        coordinate_auth.authority_ref,
        copy_observed_raw=True,
    )
    weight_slot = WeightSlotRule(
        PhysicalSlot(3, "W"),
        "W",
        _ref("WEIGHT_SOURCE", "qual-weight-W"),
        weight_auth.authority_ref,
        weight_auth.authority_ref,
        _ref("SCOPE", "qual-weight-W"),
        copy_observed_numeric=True,
    )
    owner_set = PhysicalSlotOwnerSet(
        weight_slot.slot,
        (
            PhysicalSlotOwnerAuthorization(
                WEIGHT_OWNER_FAMILY,
                (weight_owner_snapshot.authority_ref,),
            ),
        ),
    )
    authorities = (
        source_auth,
        coordinate_auth,
        weight_auth,
        routing_auth,
        replay_auth,
        projection_auth,
        weight_owner_snapshot,
    )
    return GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", "qualification-weight-owner"),
        source_artifact_id="QUAL-WEIGHT-SOURCE",
        expected_source_sha256=source_sha,
        source_family_id="SURVEY",
        study_product_id="QUAL-WEIGHT-STUDY",
        release_id="QUAL-WEIGHT-REL-1",
        instrument_release_id="QUAL-WEIGHT-INST-1",
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT",
            "urn:test:qualification:weight-source-snapshot",
            source_sha,
        ),
        universes=(universe,),
        respondents=(respondent,),
        row_bindings=(RowRespondentBinding(1, respondent.ref),),
        questions=(question,),
        response_slots=(response_slot,),
        coordinate_slots=(coordinate_slot,),
        routing=(routing,),
        weight_slots=(weight_slot,),
        authority_snapshots=authorities,
        source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(a.authority_ref for a in authorities),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=_ref("ORDER_RULE", "qual-weight-canonical-ref-sort"),
        replay_protocol_version="1.0.0",
        slot_owner_sets=(owner_set,),
    )


def _objects(release, cls):
    return tuple(x for x in release.public_objects if isinstance(x, cls))


def test_control_exact_dual_owner_with_family_scoped_authority_closes():
    response_owner = _auth(
        "qual-response-owner-control",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=(RESPONSE_OWNER_FAMILY,),
    )
    release, projection, routing = _build_dual_owner_release(response_owner)
    events = _objects(release, RespondentEvent)
    coordinates = _objects(release, EmpiricalCoordinateFact)
    assert len(events) == 1
    assert len(coordinates) == 1
    assert response_owner.authority_ref in events[0].authority_snapshot_refs
    assert routing.typed_state == "ROUTING_UNKNOWN"
    assert routing in release.public_objects
    assert projection.universes[0] in release.public_objects
    assert projection.universes[0].target_population_and_sample_frame == "SOURCE_LOCAL_ONLY__NO_POPULATION_GENERALIZATION"
    assert projection.universes[0].sampling_design_regime == "DESIGN_AUTHORITY_NOT_PROMOTED"


def test_exact_hostile_coordinate_only_authority_is_rejected_as_response_owner():
    wrong_owner = _auth(
        "qual-wrong-response-owner",
        "COORDINATE_SEMANTICS",
        families=(COORDINATE_OWNER_FAMILY,),
    )

    with pytest.raises(Pre553AuthorityError, match="object family not named"):
        require_positive_authority(
            wrong_owner,
            object_family=RESPONSE_OWNER_FAMILY,
        )

    with pytest.raises(Pre553AuthorityError, match="object family not named"):
        _build_dual_owner_release(wrong_owner)


def test_response_only_authority_is_rejected_as_coordinate_owner():
    response_owner = _auth(
        "qual-response-owner-for-coordinate-hostile",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=(RESPONSE_OWNER_FAMILY,),
    )
    wrong_coordinate_owner = _auth(
        "qual-wrong-coordinate-owner",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=(RESPONSE_OWNER_FAMILY,),
    )
    with pytest.raises(Pre553AuthorityError, match="object family not named"):
        _build_dual_owner_release(response_owner, wrong_coordinate_owner)


def test_nonweight_authority_is_rejected_as_weight_owner():
    wrong_weight_owner = _auth(
        "qual-wrong-weight-owner",
        "COORDINATE_SEMANTICS",
        families=(COORDINATE_OWNER_FAMILY,),
    )
    with pytest.raises(Pre553AuthorityError, match="object family not named"):
        _weight_owner_projection(wrong_weight_owner)


def test_lawful_weight_family_owner_authority_closes_without_policy_expansion():
    weight_owner = _auth(
        "qual-weight-owner-control",
        "WEIGHT_DESIGN_ESTIMAND",
        families=(WEIGHT_OWNER_FAMILY,),
    )
    projection = _weight_owner_projection(weight_owner)
    assert projection.slot_owner_sets[0].authority_refs_for(WEIGHT_OWNER_FAMILY) == (
        weight_owner.authority_ref,
    )
    assert projection.universes[0].target_population_and_sample_frame == "SOURCE_LOCAL_ONLY__NO_POPULATION_GENERALIZATION"
    assert projection.universes[0].sampling_design_regime == "DESIGN_AUTHORITY_NOT_PROMOTED"


@pytest.mark.parametrize(
    "family",
    (RESPONSE_OWNER_FAMILY, COORDINATE_OWNER_FAMILY, WEIGHT_OWNER_FAMILY),
)
def test_owner_authority_omission_is_fail_closed_for_every_supported_family(family):
    with pytest.raises(SourceBackedC11FacadeError, match="lacks explicit authority"):
        PhysicalSlotOwnerAuthorization(family, ())


def test_revoked_family_authority_is_fail_closed_by_canonical_authority_law():
    response_owner = _auth(
        "qual-response-owner-revoked",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=(RESPONSE_OWNER_FAMILY,),
    )
    revoked = replace(response_owner, typed_state="DENY", decision_state="DENY")
    with pytest.raises(Pre553AuthorityError, match="positive authority required"):
        _build_dual_owner_release(revoked)
