import hashlib
from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    RespondentEvent,
    RoutingEligibilityFact,
    require_public_object_family,
)
from rawlsing_next.pre553_c11_integrity import (
    M01_M18,
    QuestionVariableBinding,
    RespondentIdentity,
    TypedAbsence,
)
from rawlsing_next.pre553_c11_ingest import (
    INGEST_CONTRACT_VERSION,
    C11SourceReleaseCandidate,
    IngestDisposition,
    SourceReleaseManifest,
    build_candidate_replay_manifest,
    ingest_c11_source_release,
)
from rawlsing_next.pre553_c11_repository import C11Repository


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _root(tag: str) -> ExactRef:
    return _ref("REPLAY_ROOT", tag)


def _authority(
    tag: str,
    kind: str,
    *,
    families=("EmpiricalUniverse@1.0.0", "RespondentEvent@1.0.0",
              "EmpiricalCoordinateFact@1.0.0", "RoutingEligibilityFact@1.0.0"),
) -> AuthoritySnapshot:
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


def _base_parts(tag: str = "A", *, event_order=("e1", "e2"), event_kind="UNORDERED_MULTISELECT_SET"):
    source_auth = _authority("source", "SOURCE_SEMANTICS_TOPOLOGY")
    coord_auth = _authority("coord", "COORDINATE_SEMANTICS", families=("EmpiricalCoordinateFact@1.0.0",))
    replay_auth = _authority("replay", "REPLAY_PROTOCOL", families=("ReplayReceipt@1.0.0",))
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
        source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", f"{tag}-R1"),
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
            producer_replay_locator_or_reference_root=_root(f"event-{tag}-{event_id}"),
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
            response_topology_ref=_ref("TOPOLOGY", event_kind),
            multiplicity_order_rank_fields={"kind": event_kind, "multiplicity_index": i},
            response_state="SUBSTANTIVE_RESPONSE",
        )
        for i, event_id in enumerate(event_order)
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
    return authorities, universe, respondent, question, events, routing, coordinate, replay_auth


def _candidate(tag: str = "A", *, event_order=("e1", "e2"), event_kind="UNORDERED_MULTISELECT_SET"):
    authorities, universe, respondent, question, events, routing, coordinate, replay_auth = _base_parts(
        tag, event_order=event_order, event_kind=event_kind)
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
        declared_authority_snapshot_refs=tuple(a.authority_ref for a in authorities),
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
        source_universe_relations_or_explicit_distinct_default=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay_bindings_when_retained_objects_require_them=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"),
        discovery_branch_replay_bindings_or_typed_deferred_state=TypedAbsence("DEFERRED"),
        structural_admission_replay_bindings_or_typed_not_applicable_state=TypedAbsence("NOT_APPLICABLE"),
        candidate_replay_manifest=None,
    )
    replay = build_candidate_replay_manifest(
        candidate,
        replay_protocol_authority_ref=replay_auth.authority_ref,
        deterministic_tie_order_rules_ref=_ref("ORDER_RULE", "CANONICAL-REF-SORT"),
        replay_protocol_version="1.0.0",
    )
    return replace(candidate, candidate_replay_manifest=replay)


def test_event_multiplicity_preserved_without_value_deduplication():
    candidate = _candidate("multi")
    repo = C11Repository()
    result = ingest_c11_source_release(candidate, repo)
    assert result.accepted
    release = repo.resolve_release_exact(result.release_ref)
    events = [o for o in release.public_objects if isinstance(o, RespondentEvent)]
    assert len(events) == 2
    assert events[0].raw_response_value == events[1].raw_response_value
    assert events[0].ref != events[1].ref


def test_storage_order_invariance_does_not_change_release_identity():
    left = _candidate("order", event_order=("e1", "e2"))
    right0 = replace(left, respondent_events=tuple(reversed(left.respondent_events)), candidate_replay_manifest=None)
    right = replace(
        right0,
        candidate_replay_manifest=build_candidate_replay_manifest(
            right0,
            replay_protocol_authority_ref=left.candidate_replay_manifest.replay_protocol_authority_ref,
            deterministic_tie_order_rules_ref=left.candidate_replay_manifest.deterministic_tie_order_rules_ref,
            replay_protocol_version=left.candidate_replay_manifest.replay_protocol_version,
        ),
    )
    lres = ingest_c11_source_release(left, C11Repository())
    rres = ingest_c11_source_release(right, C11Repository())
    assert lres.accepted and rres.accepted
    assert lres.semantic_release_hash == rres.semantic_release_hash


def test_same_respondent_key_in_different_universes_has_distinct_internal_identity():
    _, u1, _, _, _, _, _, _ = _base_parts("U1", event_order=("e1",))
    _, u2, _, _, _, _, _, _ = _base_parts("U2", event_order=("e1",))
    r1 = RespondentIdentity(u1.ref, "SAME", _ref("SOURCE_RESPONDENT", "u1"), TypedAbsence("NOT_APPLICABLE"))
    r2 = RespondentIdentity(u2.ref, "SAME", _ref("SOURCE_RESPONDENT", "u2"), TypedAbsence("NOT_APPLICABLE"))
    assert r1.ref != r2.ref


def test_routing_member_set_identity_is_semantic_not_denominator_equivalence():
    candidate = _candidate("risk")
    original = candidate.routing_eligibility_facts_or_exact_rules[0]
    changed = RoutingEligibilityFact(
        typed_state=original.typed_state,
        authority_snapshot_refs=original.authority_snapshot_refs,
        dependency_refs=original.dependency_refs,
        producer_replay_locator_or_reference_root=original.producer_replay_locator_or_reference_root,
        **{**dict(original.semantic_fields), "member_set_replay_ref": _ref("MEMBER_SET", "different-members")},
    )
    assert original.ref != changed.ref


def test_typed_special_states_remain_distinct_from_substantive_zero_or_missing_row():
    candidate = _candidate("states", event_order=("e1",))
    base = candidate.respondent_events[0]
    dk = RespondentEvent(
        typed_state="DK",
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root("dk"),
        **{**dict(base.semantic_fields), "raw_response_value": None,
           "canonical_response_value_if_authorized": None, "response_state": "DK",
           "response_event_id_or_deterministic_index": "dk"},
    )
    refusal = RespondentEvent(
        typed_state="REFUSAL",
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_root("refusal"),
        **{**dict(base.semantic_fields), "raw_response_value": None,
           "canonical_response_value_if_authorized": None, "response_state": "REFUSAL",
           "response_event_id_or_deterministic_index": "refusal"},
    )
    assert dk.ref != refusal.ref != base.ref


def test_missing_weight_cannot_be_repaired_to_one_at_public_object_boundary():
    from rawlsing_next.pre553_empirical_objects import WeightMeasureFact
    candidate = _candidate("weight", event_order=("e1",))
    u = candidate.empirical_universes[0]
    r = candidate.respondent_identities[0]
    auth = candidate.authority_snapshots[0].authority_ref
    with pytest.raises(Pre553IntegrityError):
        WeightMeasureFact(
            typed_state="WEIGHT_MISSING",
            authority_snapshot_refs=(auth,),
            dependency_refs=(),
            producer_replay_locator_or_reference_root=_root("weight"),
            empirical_universe_ref=u.ref,
            scoped_respondent_ref=r.ref,
            weight_basis_id="W1",
            exact_weight_value_representation="1.0",
            weight_state="WEIGHT_MISSING",
            weight_source_ref=_ref("WEIGHT_SOURCE", "w"),
            design_authority_ref=auth,
            estimand_authority_ref=auth,
            normalization_or_recalibration_rule_ref=None,
            effective_scope_ref=_ref("SCOPE", "w"),
        )


def test_missing_exact_authority_blocks_and_repository_remains_empty():
    candidate = _candidate("missing-auth", event_order=("e1",))
    base = candidate.respondent_events[0]
    missing = AuthorityRef("AUTH-NOT-PACKAGED", "1.0.0", _h("missing-auth"))
    event = RespondentEvent(
        typed_state=base.typed_state,
        authority_snapshot_refs=(missing,),
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
        **dict(base.semantic_fields),
    )
    bad0 = replace(candidate, respondent_events=(event,), candidate_replay_manifest=None)
    bad = replace(
        bad0,
        candidate_replay_manifest=build_candidate_replay_manifest(
            bad0,
            replay_protocol_authority_ref=candidate.candidate_replay_manifest.replay_protocol_authority_ref,
            deterministic_tie_order_rules_ref=candidate.candidate_replay_manifest.deterministic_tie_order_rules_ref,
            replay_protocol_version="1.0.0",
        ),
    )
    repo = C11Repository()
    result = ingest_c11_source_release(bad, repo)
    assert not result.accepted
    assert result.disposition == IngestDisposition.BLOCKED_MISSING_REQUIRED_AUTHORITY
    assert len(repo) == 0


def test_partial_package_presence_is_not_authority_and_commit_is_atomic():
    candidate = _candidate("partial", event_order=("e1",))
    partial = replace(candidate, routing_eligibility_facts_or_exact_rules=(), candidate_replay_manifest=None)
    repo = C11Repository()
    result = ingest_c11_source_release(partial, repo)
    assert not result.accepted
    assert result.disposition == IngestDisposition.REJECTED_RISK_SET_LOSS
    assert len(repo) == 0


def test_accepted_release_returns_complete_m01_m18_coverage():
    result = ingest_c11_source_release(_candidate("coverage"), C11Repository())
    assert result.accepted
    assert tuple(result.m01_m18_coverage) == M01_M18
    assert all(result.m01_m18_coverage[atom] for atom in M01_M18)


def test_unauthorized_canonical_mapping_is_rejected_not_silently_inferred():
    candidate = _candidate("canonical", event_order=("e1",))
    base = candidate.respondent_events[0]
    event = RespondentEvent(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
        **{**dict(base.semantic_fields),
           "canonical_question_ref_if_authorized": _ref("QUESTION_CANONICAL", "Q1"),
           "value_transform_authority_ref": None},
    )
    bad0 = replace(candidate, respondent_events=(event,), candidate_replay_manifest=None)
    bad = replace(
        bad0,
        candidate_replay_manifest=build_candidate_replay_manifest(
            bad0,
            replay_protocol_authority_ref=candidate.candidate_replay_manifest.replay_protocol_authority_ref,
            deterministic_tie_order_rules_ref=candidate.candidate_replay_manifest.deterministic_tie_order_rules_ref,
            replay_protocol_version="1.0.0",
        ),
    )
    result = ingest_c11_source_release(bad, C11Repository())
    assert not result.accepted
    assert result.disposition == IngestDisposition.REJECTED_UNAUTHORIZED_SEMANTIC_PROMOTION


def test_no_cross_universe_relation_is_inferred_from_same_labels_or_keys():
    candidate = _candidate("distinct", event_order=("e1",))
    assert isinstance(candidate.source_universe_relations_or_explicit_distinct_default, TypedAbsence)
    assert candidate.source_universe_relations_or_explicit_distinct_default.state == "DISTINCT_BY_DEFAULT"
    result = ingest_c11_source_release(candidate, C11Repository())
    assert result.accepted


def test_replay_manifest_tamper_is_rejected_and_not_committed():
    candidate = _candidate("tamper", event_order=("e1",))
    base = candidate.respondent_events[0]
    changed = RespondentEvent(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=_root("tampered-event"),
        **{**dict(base.semantic_fields), "raw_response_value": "CHANGED"},
    )
    tampered = replace(candidate, respondent_events=(changed,))
    repo = C11Repository()
    result = ingest_c11_source_release(tampered, repo)
    assert not result.accepted
    assert result.disposition == IngestDisposition.REJECTED_REPLAY_NONDETERMINISM
    assert len(repo) == 0


def test_source_manifest_hash_tamper_is_rejected_by_replay_binding():
    candidate = _candidate("source-tamper", event_order=("e1",))
    manifest = replace(candidate.source_release_manifest,
                       source_artifact_content_hash=_h("different-source-bytes"))
    tampered = replace(candidate, source_release_manifest=manifest)
    result = ingest_c11_source_release(tampered, C11Repository())
    assert not result.accepted
    assert result.disposition == IngestDisposition.REJECTED_REPLAY_NONDETERMINISM


def test_ordered_topology_requires_explicit_semantic_rank_or_order():
    candidate = _candidate("ranked", event_order=("e1",), event_kind="RANKED_RESPONSE")
    base = candidate.respondent_events[0]
    bad_event = RespondentEvent(
        typed_state=base.typed_state,
        authority_snapshot_refs=base.authority_snapshot_refs,
        dependency_refs=base.dependency_refs,
        producer_replay_locator_or_reference_root=base.producer_replay_locator_or_reference_root,
        **{**dict(base.semantic_fields),
           "multiplicity_order_rank_fields": {"kind": "RANKED_RESPONSE", "multiplicity_index": 0}},
    )
    bad0 = replace(candidate, respondent_events=(bad_event,), candidate_replay_manifest=None)
    bad = replace(
        bad0,
        candidate_replay_manifest=build_candidate_replay_manifest(
            bad0,
            replay_protocol_authority_ref=candidate.candidate_replay_manifest.replay_protocol_authority_ref,
            deterministic_tie_order_rules_ref=candidate.candidate_replay_manifest.deterministic_tie_order_rules_ref,
            replay_protocol_version="1.0.0",
        ),
    )
    result = ingest_c11_source_release(bad, C11Repository())
    assert not result.accepted
    assert result.disposition == IngestDisposition.REJECTED_TOPOLOGY_LOSS


def test_carrier_internal_record_does_not_promote_public_ontology():
    with pytest.raises(Pre553SemanticCollapseError):
        require_public_object_family("RespondentIdentity")
    with pytest.raises(Pre553SemanticCollapseError):
        AuthorityRegistry([_authority("bad", "SOURCE_SEMANTICS_TOPOLOGY", families=("RespondentIdentity",))])


def test_repository_has_exact_lookup_only_no_latest_or_default_lane():
    repo = C11Repository()
    result = ingest_c11_source_release(_candidate("lookup"), repo)
    assert result.accepted
    assert repo.resolve_release_exact(result.release_ref).release_ref == result.release_ref
    with pytest.raises(KeyError):
        repo.resolve_release_exact(ExactRef("C11LogicalRelease", "latest", _h("latest")))
