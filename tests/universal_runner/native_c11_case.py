"""Committed sourcefree C11 fixture built through existing native constructors."""
from __future__ import annotations

from dataclasses import replace
import hashlib

from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    RoutingEligibilityFact,
)
from rawlsing_next.pre553_c11_integrity import (
    QuestionVariableBinding,
    RespondentIdentity,
    TypedAbsence,
)
from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION,
    C11SourceReleaseCandidate,
    SourceReleaseManifest,
    build_candidate_replay_manifest,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _root(tag: str) -> ExactRef:
    return _ref("REPLAY_ROOT", tag)


def _authority(tag: str, kind: str, *, families=(
        "EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0",
        "EmpiricalCoordinateFact@1.0.0", "RoutingEligibilityFact@1.0.0")):
    content_hash = _h(f"authority:{tag}:1.0.0")
    return AuthoritySnapshot(
        typed_state="ALLOW",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root(f"authority-{tag}"),
        authority_id=f"AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=content_hash,
        authority_kind=kind,
        decision_state="ALLOW",
        governed_operations=(f"OP-{tag}",),
        governed_object_families=families,
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", tag),
    )


def build_candidate(tag: str = "R09"):
    source_auth = _authority("source", "SOURCE_SEMANTICS_TOPOLOGY")
    coord_auth = _authority("coord", "COORDINATE_SEMANTICS",
                            families=("EmpiricalCoordinateFact@1.0.0",))
    replay_auth = _authority("replay", "REPLAY_PROTOCOL",
                             families=("ReplayReceipt@1.0.0",))
    authorities = (source_auth, coord_auth, replay_auth)
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root(f"universe-{tag}"),
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
        sampling_design_regime="DESIGN-A",
        respondent_namespace=f"NS-{tag}",
        source_artifact_import_lineage=f"SRC-{tag}",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    respondent = RespondentIdentity(
        empirical_universe_ref=universe.ref,
        respondent_key="R1",
        source_native_respondent_key_ref_or_typed_absence=_ref(
            "SOURCE_RESPONDENT", f"{tag}-R1"),
        identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
    )
    native_q = _ref("QUESTION_NATIVE", f"{tag}-Q1")
    question = QuestionVariableBinding(
        empirical_universe_ref=universe.ref,
        native_question_ref=native_q,
        instrument_question_version="1",
        canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
        component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        semantic_authority_ref=source_auth.authority_ref,
        topology_authority_ref=source_auth.authority_ref,
    )
    events = tuple(
        RespondentEvent(
            typed_state="SUBSTANTIVE_RESPONSE",
            authority_snapshot_refs=(source_auth.authority_ref,),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_root(
                f"event-{tag}-{event_id}"),
            empirical_universe_ref=universe.ref,
            scoped_respondent_ref=respondent.ref,
            native_question_ref=native_q,
            canonical_question_ref_if_authorized=None,
            component_or_subitem_ref=None,
            event_group_id=f"GROUP-{tag}",
            response_event_id_or_deterministic_index=event_id,
            raw_response_value="SAME-VALUE",
            canonical_response_value_if_authorized=None,
            value_transform_authority_ref=None,
            response_topology_ref=_ref("TOPOLOGY", "UNORDERED_MULTISELECT_SET"),
            multiplicity_order_rank_fields={
                "kind": "UNORDERED_MULTISELECT_SET", "multiplicity_index": index},
            response_state="SUBSTANTIVE_RESPONSE",
        )
        for index, event_id in enumerate(("e1", "e2"))
    )
    routing = RoutingEligibilityFact(
        typed_state="ELIGIBLE_APPLICABLE",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root(f"routing-{tag}"),
        empirical_universe_ref=universe.ref,
        scoped_respondent_ref=respondent.ref,
        question_or_target_ref=native_q,
        risk_set_ref=_ref("RISK_SET", f"{tag}-Q1"),
        routing_rule_ref=_ref("ROUTING_RULE", f"{tag}-Q1"),
        applicability_state="ELIGIBLE_APPLICABLE",
        routing_state="ELIGIBLE_APPLICABLE",
        parent_predicate_refs=(),
        member_set_replay_ref=_ref("MEMBER_SET", f"{tag}-eligible-R1"),
    )
    coordinate = EmpiricalCoordinateFact(
        typed_state="OBSERVED_COORDINATE",
        authority_snapshot_refs=(coord_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root(f"coordinate-{tag}"),
        empirical_universe_ref=universe.ref,
        scoped_respondent_ref=respondent.ref,
        native_coordinate_ref=_ref("COORDINATE_NATIVE", f"{tag}-AGE"),
        canonical_coordinate_ref_if_authorized=None,
        raw_coordinate_value="45",
        canonical_coordinate_value_if_authorized=None,
        unit_category_taxonomy_ref=_ref("UNIT_TAXONOMY", "YEARS"),
        effective_or_reference_time="2026-01",
        coordinate_state="OBSERVED_COORDINATE",
        normalization_crosswalk_authority_ref=None,
        source_semantic_authority_ref=coord_auth.authority_ref,
    )
    counts = {
        "EmpiricalUniverse": 1,
        "RespondentIdentity": 1,
        "QuestionVariableBinding": 1,
        "RespondentEvent": len(events),
        "RoutingEligibilityFact": 1,
        "EmpiricalCoordinateFact": 1,
        "WeightMeasureFact": 0,
        "AuthoritySnapshot": len(authorities),
        "SourceUniverseRelation": 0,
        "EmpiricalPredicateReplayBinding": 0,
        "ComparatorReplayBinding": 0,
        "DiscoveryBranchReplayBinding": 0,
        "StructuralAdmissionReplayBinding": 0,
        "ReplayManifest": 1,
    }
    source_hash = _h(f"source-artifact:{tag}")
    manifest = SourceReleaseManifest(
        source_artifact_id=f"SOURCE-{tag}",
        source_artifact_content_hash=source_hash,
        source_family_id="SURVEY",
        study_product_id=f"STUDY-{tag}",
        release_id=f"REL-{tag}",
        instrument_release_id=f"INST-{tag}",
        ingest_contract_version=INGEST_CONTRACT_VERSION,
        declared_universe_refs=(universe.ref,),
        declared_authority_snapshot_refs=tuple(
            authority.authority_ref for authority in authorities),
        declared_record_counts_by_logical_family=counts,
        source_snapshot_retention_ref=ExactRef(
            "SOURCE_SNAPSHOT", f"urn:test:source-snapshot:{tag}", source_hash),
    )
    candidate = C11SourceReleaseCandidate(
        source_release_manifest=manifest,
        empirical_universes=(universe,),
        respondent_identities=(respondent,),
        question_variable_bindings=(question,),
        respondent_events=events,
        routing_eligibility_facts_or_exact_rules=(routing,),
        empirical_coordinate_facts=(coordinate,),
        weight_measure_facts_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
        authority_snapshots=authorities,
        source_universe_relations_or_explicit_distinct_default=TypedAbsence(
            "DISTINCT_BY_DEFAULT"),
        predicate_replay_bindings_when_retained_objects_require_them=TypedAbsence(
            "NOT_APPLICABLE"),
        comparator_replay_bindings_or_typed_deferred_state=TypedAbsence(
            "DEFERRED"),
        discovery_branch_replay_bindings_or_typed_deferred_state=TypedAbsence(
            "DEFERRED"),
        structural_admission_replay_bindings_or_typed_not_applicable_state=TypedAbsence(
            "NOT_APPLICABLE"),
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=replay_auth.authority_ref,
        deterministic_tie_order_rules_ref=_ref("ORDER_RULE", "CANONICAL-REF-SORT"),
        replay_protocol_version="1.0.0",
    )
    return replace(candidate, candidate_replay_manifest=replay)
