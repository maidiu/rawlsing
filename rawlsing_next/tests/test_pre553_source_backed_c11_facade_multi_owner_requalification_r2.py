from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from rawlsing_next.pre553_c11_integrity import QuestionVariableBinding, RespondentIdentity, TypedAbsence
from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalCoordinateFact,
    EmpiricalUniverse,
    ExactRef,
    RespondentEvent,
    RoutingEligibilityFact,
    WeightMeasureFact,
    semantic_hash,
)
from rawlsing_next.pre553_physical_decoder import PhysicalCell, PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
    CONTRACT_ID,
    COORDINATE_OWNER_FAMILY,
    RESPONSE_OWNER_FAMILY,
    SLOT_OWNER_SET_CONTRACT_ID,
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


ACCEPTED_WVS7_DUAL_ROLE_42 = (
    "Q138", "Q173", "Q260", "Q261", "Q262", "Q263", "Q264", "Q265", "Q266", "Q267", "Q268",
    "Q269", "Q270", "Q271", "Q272", "Q273", "Q274", "Q275", "Q275A", "Q276", "Q276A", "Q277",
    "Q277A", "Q278", "Q278A", "Q279", "Q280", "Q284", "Q287", "Q288", "Q47", "Q51", "Q52", "Q53",
    "Q54", "Q55", "Q56", "V001", "V001A_01", "V002", "V002A_01", "X002_02B",
)


def _objects(release, cls):
    return tuple(obj for obj in release.public_objects if isinstance(obj, cls))


def _fixture(
    names=("SLOT-A",),
    *,
    dual_owner: bool = True,
    explicit_owner_sets: bool = True,
    include_pweight_noise: bool = False,
):
    source_auth = _auth(
        "rq2-source",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=("EmpiricalUniverse@1.0.0", RESPONSE_OWNER_FAMILY),
    )
    coordinate_auth = _auth(
        "rq2-coordinate",
        "COORDINATE_SEMANTICS",
        families=(COORDINATE_OWNER_FAMILY,),
    )
    routing_auth = _auth(
        "rq2-routing",
        "ROUTING_RISK_SET",
        families=("RoutingEligibilityFact@1.0.0",),
    )
    replay_auth = _auth(
        "rq2-replay",
        "REPLAY_PROTOCOL",
        families=("ReplayReceipt@1.0.0",),
    )
    projection_auth = _auth(
        "rq2-projection",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=(RESPONSE_OWNER_FAMILY, COORDINATE_OWNER_FAMILY),
    )
    response_owner = _auth(
        "rq2-response-owner",
        "SOURCE_SEMANTICS_TOPOLOGY",
        families=(RESPONSE_OWNER_FAMILY,),
    )
    coordinate_owner = _auth(
        "rq2-coordinate-owner",
        "COORDINATE_SEMANTICS",
        families=(COORDINATE_OWNER_FAMILY,),
    )

    authorities = [source_auth, coordinate_auth, routing_auth, replay_auth, projection_auth]
    if explicit_owner_sets:
        authorities.extend((response_owner, coordinate_owner))

    source_sha = _h("rq2-independent-source")
    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(source_auth.authority_ref,),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", "rq2-universe"),
        raw_source_identity="RAW-RQ2-INDEPENDENT",
        source_family="SURVEY",
        study_product_release="RQ2-STUDY/REL-1",
        instrument_release="RQ2-INSTRUMENT",
        country_geography="US",
        sampling_geography="US-NATIONAL",
        raw_wave="W1",
        canonical_wave_if_governed=None,
        field_or_reference_time="2026-01",
        target_population_and_sample_frame="NO_POPULATION_GENERALIZATION",
        sampling_design_regime="DESIGN_AUTHORITY_NOT_PROMOTED",
        respondent_namespace="RQ2-NS",
        source_artifact_import_lineage="RQ2-SOURCE-LINEAGE",
        harmonization_authority_ref=None,
        source_relation_refs=(),
    )
    respondent = RespondentIdentity(
        empirical_universe_ref=universe.ref,
        respondent_key="R1",
        source_native_respondent_key_ref_or_typed_absence=_ref("SOURCE_RESPONDENT", "rq2-R1"),
        identity_map_authority_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
    )

    questions = []
    response_slots = []
    coordinate_slots = []
    routing = []
    owner_sets = []
    cells = []
    pkey = physical_value_binding_key("1", PhysicalMissingState.OBSERVED_STORAGE_VALUE)

    for ordinal, name in enumerate(names, 1):
        qref = _ref("QUESTION_NATIVE", f"rq2-{name}")
        question = QuestionVariableBinding(
            empirical_universe_ref=universe.ref,
            native_question_ref=qref,
            instrument_question_version="1",
            canonical_question_ref_or_typed_absence=TypedAbsence("NOT_AUTHORIZED"),
            component_subitem_ref_or_typed_absence=TypedAbsence("NOT_APPLICABLE"),
            semantic_authority_ref=source_auth.authority_ref,
            topology_authority_ref=source_auth.authority_ref,
        )
        questions.append(question)
        routing.append(
            RoutingEligibilityFact(
                typed_state="ROUTING_UNKNOWN",
                authority_snapshot_refs=(routing_auth.authority_ref,),
                dependency_refs=(),
                producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"rq2-routing-{name}"),
                empirical_universe_ref=universe.ref,
                scoped_respondent_ref=respondent.ref,
                question_or_target_ref=qref,
                risk_set_ref=_ref("RISK_SET", f"rq2-risk-{name}"),
                routing_rule_ref=_ref("ROUTING_RULE", f"rq2-rule-{name}"),
                applicability_state="ROUTING_UNKNOWN",
                routing_state="ROUTING_UNKNOWN",
                parent_predicate_refs=(),
                member_set_replay_ref=_ref("MEMBER_SET", f"rq2-members-{name}"),
            )
        )
        response_slot = PhysicalSlot(ordinal, name)
        response_slots.append(
            ResponseSlotRule(
                response_slot,
                question,
                (
                    ResponseValueRule(
                        pkey,
                        "SUBSTANTIVE_RESPONSE",
                        (
                            OccurrenceRule(
                                "0",
                                _ref("TOPOLOGY", f"rq2-topology-{name}"),
                                {"kind": "SCALAR_SINGULAR", "index": 0},
                            ),
                        ),
                    ),
                ),
            )
        )
        coordinate_slot = response_slot if dual_owner else PhysicalSlot(len(names) + ordinal, f"G-{ordinal}")
        coordinate_slots.append(
            CoordinateSlotRule(
                coordinate_slot,
                _ref("COORDINATE_NATIVE", f"rq2-coordinate-{name}"),
                _ref("UNIT_TAXONOMY", "rq2-position"),
                "2026-01",
                coordinate_auth.authority_ref,
                copy_observed_raw=True,
            )
        )
        if dual_owner and explicit_owner_sets:
            owner_sets.append(
                PhysicalSlotOwnerSet(
                    response_slot,
                    (
                        PhysicalSlotOwnerAuthorization(
                            RESPONSE_OWNER_FAMILY,
                            (response_owner.authority_ref,),
                        ),
                        PhysicalSlotOwnerAuthorization(
                            COORDINATE_OWNER_FAMILY,
                            (coordinate_owner.authority_ref,),
                        ),
                    ),
                )
            )
        cells.append(
            PhysicalCell(
                1,
                response_slot.ordinal,
                response_slot.name,
                "1",
                PhysicalMissingState.OBSERVED_STORAGE_VALUE,
                None,
            )
        )
        if not dual_owner:
            cells.append(
                PhysicalCell(
                    1,
                    coordinate_slot.ordinal,
                    coordinate_slot.name,
                    f"C-{ordinal}",
                    PhysicalMissingState.OBSERVED_STORAGE_VALUE,
                    None,
                )
            )

    if include_pweight_noise:
        cells.append(
            PhysicalCell(
                1,
                999,
                "PWGHT",
                "2.5",
                PhysicalMissingState.OBSERVED_STORAGE_VALUE,
                None,
            )
        )

    projection = GovernedC11Projection(
        projection_identity_ref=_ref("C11_SEMANTIC_PROJECTION", "rq2-independent"),
        source_artifact_id="SOURCE-RQ2-INDEPENDENT",
        expected_source_sha256=source_sha,
        source_family_id="SURVEY",
        study_product_id="STUDY-RQ2",
        release_id="REL-RQ2",
        instrument_release_id="INST-RQ2",
        source_snapshot_retention_ref=ExactRef("SOURCE_SNAPSHOT", "urn:test:rq2:snapshot", source_sha),
        universes=(universe,),
        respondents=(respondent,),
        row_bindings=(RowRespondentBinding(1, respondent.ref),),
        questions=tuple(questions),
        response_slots=tuple(response_slots),
        coordinate_slots=tuple(coordinate_slots),
        routing=tuple(routing),
        weight_slots=(),
        authority_snapshots=tuple(authorities),
        source_relations=TypedAbsence("DISTINCT_BY_DEFAULT"),
        predicate_replay=TypedAbsence("NOT_APPLICABLE"),
        comparator_replay=TypedAbsence("DEFERRED"),
        discovery_replay=TypedAbsence("DEFERRED"),
        structural_replay=TypedAbsence("NOT_APPLICABLE"),
        required_authority_refs=tuple(a.authority_ref for a in authorities),
        projection_authority_ref=projection_auth.authority_ref,
        replay_authority_ref=replay_auth.authority_ref,
        tie_order_ref=_ref("ORDER_RULE", "RQ2-CANONICAL-REF-SORT"),
        replay_protocol_version="1.0.0",
        slot_owner_sets=tuple(owner_sets),
    )
    stream = ExactPhysicalCellStream(source_sha, 1, lambda: iter(tuple(cells)))
    return {
        "projection": projection,
        "stream": stream,
        "respondent": respondent,
        "questions": tuple(questions),
        "pkey": pkey,
        "response_owner": response_owner,
        "coordinate_owner": coordinate_owner,
        "coordinate_auth": coordinate_auth,
        "routing_auth": routing_auth,
    }


def _rebind_first_owner(projection, family, authority_ref):
    current = projection.slot_owner_sets[0]
    owners = []
    for owner in current.owners:
        owners.append(
            PhysicalSlotOwnerAuthorization(
                owner.owner_family,
                (authority_ref,) if owner.owner_family == family else owner.authority_refs,
            )
        )
    return PhysicalSlotOwnerSet(current.slot, tuple(owners))


def _nonallow_snapshot(tag: str, *, family: str, state: str) -> AuthoritySnapshot:
    return AuthoritySnapshot(
        typed_state=state,
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"rq2-{tag}"),
        authority_id=f"RQ2-AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=_h(f"rq2-authority:{tag}:1.0.0"),
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        decision_state=state,
        governed_operations=(f"RQ2-OP-{tag}",),
        governed_object_families=(family,),
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"rq2-semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", f"rq2-{tag}"),
    )


def _with_weight_owner(projection, owner_snapshot):
    slot = projection.slot_owner_sets[0].slot
    weight_semantics = _auth(
        "rq2-weight-semantics",
        "WEIGHT_DESIGN_ESTIMAND",
        families=(WEIGHT_OWNER_FAMILY,),
    )
    weight_slot = WeightSlotRule(
        slot,
        "RQ2-WEIGHT-BASIS",
        _ref("WEIGHT_SOURCE", "rq2-weight-source"),
        weight_semantics.authority_ref,
        weight_semantics.authority_ref,
        _ref("SCOPE", "rq2-weight-scope"),
        copy_observed_numeric=True,
    )
    owner_set = PhysicalSlotOwnerSet(
        slot,
        (
            *projection.slot_owner_sets[0].owners,
            PhysicalSlotOwnerAuthorization(WEIGHT_OWNER_FAMILY, (owner_snapshot.authority_ref,)),
        ),
    )
    snapshots = projection.authority_snapshots + tuple(
        snapshot
        for snapshot in (weight_semantics, owner_snapshot)
        if snapshot.authority_ref not in {x.authority_ref for x in projection.authority_snapshots}
    )
    required = projection.required_authority_refs + tuple(
        ref
        for ref in (weight_semantics.authority_ref, owner_snapshot.authority_ref)
        if ref not in set(projection.required_authority_refs)
    )
    return replace(
        projection,
        weight_slots=(weight_slot,),
        authority_snapshots=snapshots,
        required_authority_refs=required,
        slot_owner_sets=(owner_set,),
    )


def test_owner_family_authority_closure_is_exact_and_reciprocal_substitution_fails_closed():
    fx = _fixture()
    p = fx["projection"]
    with pytest.raises(Pre553AuthorityError, match="object family not named"):
        replace(
            p,
            slot_owner_sets=(
                _rebind_first_owner(p, RESPONSE_OWNER_FAMILY, fx["coordinate_owner"].authority_ref),
            ),
        )
    with pytest.raises(Pre553AuthorityError, match="object family not named"):
        replace(
            p,
            slot_owner_sets=(
                _rebind_first_owner(p, COORDINATE_OWNER_FAMILY, fx["response_owner"].authority_ref),
            ),
        )


def test_wrong_family_weight_owner_fails_before_any_weight_policy_can_be_inferred():
    fx = _fixture()
    wrong = _auth(
        "rq2-wrong-weight-owner",
        "COORDINATE_SEMANTICS",
        families=(COORDINATE_OWNER_FAMILY,),
    )
    with pytest.raises(Pre553AuthorityError, match="object family not named"):
        _with_weight_owner(fx["projection"], wrong)


@pytest.mark.parametrize("state", ("DENY", "DEFER", "SUPERSEDED_NOT_REPLAYABLE"))
def test_nonallow_or_revoked_owner_authority_fails_closed(state):
    fx = _fixture()
    p = fx["projection"]
    bad = _nonallow_snapshot(f"response-{state.lower()}", family=RESPONSE_OWNER_FAMILY, state=state)
    owner_set = _rebind_first_owner(p, RESPONSE_OWNER_FAMILY, bad.authority_ref)
    snapshots = tuple(x for x in p.authority_snapshots if x.authority_ref != fx["response_owner"].authority_ref) + (bad,)
    required = tuple(x for x in p.required_authority_refs if x != fx["response_owner"].authority_ref) + (bad.authority_ref,)
    with pytest.raises(Pre553AuthorityError, match="positive authority required"):
        replace(p, authority_snapshots=snapshots, required_authority_refs=required, slot_owner_sets=(owner_set,))


def test_missing_unrequired_and_unpacked_owner_authority_all_fail_closed():
    fx = _fixture()
    p = fx["projection"]
    response_ref = fx["response_owner"].authority_ref

    with pytest.raises(SourceBackedC11FacadeError, match="explicitly required"):
        replace(
            p,
            required_authority_refs=tuple(x for x in p.required_authority_refs if x != response_ref),
        )

    with pytest.raises(SourceBackedC11FacadeError, match="required authority absent"):
        replace(
            p,
            authority_snapshots=tuple(x for x in p.authority_snapshots if x.authority_ref != response_ref),
        )

    alien = _auth("rq2-alien-owner", "SOURCE_SEMANTICS_TOPOLOGY", families=(RESPONSE_OWNER_FAMILY,))
    owner_set = _rebind_first_owner(p, RESPONSE_OWNER_FAMILY, alien.authority_ref)
    with pytest.raises(SourceBackedC11FacadeError, match="explicitly required"):
        replace(p, slot_owner_sets=(owner_set,))


def test_malformed_implicit_incomplete_duplicate_or_orphan_owner_sets_fail_closed():
    with pytest.raises(SourceBackedC11FacadeError, match="implicit/unapproved second"):
        _fixture(explicit_owner_sets=False)

    fx = _fixture()
    p = fx["projection"]
    response_owner = p.slot_owner_sets[0].owners[1] if p.slot_owner_sets[0].owners[1].owner_family == RESPONSE_OWNER_FAMILY else p.slot_owner_sets[0].owners[0]

    with pytest.raises(SourceBackedC11FacadeError, match="lacks explicit authority"):
        PhysicalSlotOwnerAuthorization(RESPONSE_OWNER_FAMILY, ())
    with pytest.raises(SourceBackedC11FacadeError, match="duplicate physical-slot owner authority"):
        PhysicalSlotOwnerAuthorization(RESPONSE_OWNER_FAMILY, (fx["response_owner"].authority_ref, fx["response_owner"].authority_ref))
    with pytest.raises(SourceBackedC11FacadeError, match="unsupported physical-slot semantic owner family"):
        PhysicalSlotOwnerAuthorization("NotARealSemanticFamily@1.0.0", (fx["response_owner"].authority_ref,))
    with pytest.raises(SourceBackedC11FacadeError, match="conflicting duplicate"):
        PhysicalSlotOwnerSet(p.slot_owner_sets[0].slot, (response_owner, response_owner))

    incomplete = PhysicalSlotOwnerSet(p.slot_owner_sets[0].slot, (response_owner,))
    with pytest.raises(SourceBackedC11FacadeError, match="does not exactly match"):
        replace(p, slot_owner_sets=(incomplete,))

    orphan = PhysicalSlotOwnerSet(
        PhysicalSlot(9999, "ORPHAN"),
        (PhysicalSlotOwnerAuthorization(RESPONSE_OWNER_FAMILY, (fx["response_owner"].authority_ref,)),),
    )
    with pytest.raises(SourceBackedC11FacadeError, match="slot with no emitted semantic owner"):
        replace(p, slot_owner_sets=(p.slot_owner_sets[0], orphan))


def test_lawful_dual_owner_release_is_exact_deterministic_and_owner_order_invariant():
    fx = _fixture()
    p = fx["projection"]
    first = build_validated_source_backed_c11_release_from_stream(fx["stream"], p)
    second = build_validated_source_backed_c11_release_from_stream(fx["stream"], p)

    event = _objects(first, RespondentEvent)
    coordinate = _objects(first, EmpiricalCoordinateFact)
    assert len(event) == 1
    assert len(coordinate) == 1
    assert fx["response_owner"].authority_ref in event[0].authority_snapshot_refs
    assert fx["coordinate_owner"].authority_ref in coordinate[0].authority_snapshot_refs
    assert first.release_ref == second.release_ref
    assert first.replay_manifest.ref == second.replay_manifest.ref
    assert tuple(x.ref for x in first.public_objects) == tuple(x.ref for x in second.public_objects)

    current = p.slot_owner_sets[0]
    reordered = replace(
        p,
        slot_owner_sets=(PhysicalSlotOwnerSet(current.slot, tuple(reversed(current.owners))),),
        required_authority_refs=tuple(reversed(p.required_authority_refs)),
        authority_snapshots=tuple(reversed(p.authority_snapshots)),
    )
    replayed = build_validated_source_backed_c11_release_from_stream(fx["stream"], reordered)
    assert reordered.cache_identity == p.cache_identity
    assert replayed.release_ref == first.release_ref
    assert replayed.replay_manifest.ref == first.replay_manifest.ref
    assert tuple(x.ref for x in replayed.public_objects) == tuple(x.ref for x in first.public_objects)


def test_legacy_single_owner_v1_cache_and_event_replay_identity_remain_exact():
    fx = _fixture(("LEGACY",), dual_owner=False, explicit_owner_sets=False)
    p = fx["projection"]
    release = build_validated_source_backed_c11_release_from_stream(fx["stream"], p)
    events = _objects(release, RespondentEvent)
    assert len(events) == 1

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
        "question": fx["questions"][0].ref.as_dict(),
        "slot": (1, "LEGACY"),
        "physical_value_key": fx["pkey"],
        "occurrence": "0",
    }
    assert events[0].producer_replay_locator_or_reference_root.content_hash == semantic_hash(event_material)


def test_exact_accepted_42_slot_shape_executes_generically_and_preserves_negative_ceilings():
    assert len(ACCEPTED_WVS7_DUAL_ROLE_42) == 42
    assert len(set(ACCEPTED_WVS7_DUAL_ROLE_42)) == 42
    fx = _fixture(ACCEPTED_WVS7_DUAL_ROLE_42, include_pweight_noise=True)
    p = fx["projection"]
    first = build_validated_source_backed_c11_release_from_stream(fx["stream"], p)
    second = build_validated_source_backed_c11_release_from_stream(fx["stream"], p)

    assert len(p.slot_owner_sets) == 42
    assert tuple(owner.slot.name for owner in p.slot_owner_sets) == ACCEPTED_WVS7_DUAL_ROLE_42
    assert all(owner.contract_id == SLOT_OWNER_SET_CONTRACT_ID for owner in p.slot_owner_sets)
    assert len(_objects(first, RespondentEvent)) == 42
    assert len(_objects(first, EmpiricalCoordinateFact)) == 42
    assert len(_objects(first, WeightMeasureFact)) == 0
    assert first.release_ref == second.release_ref
    assert first.replay_manifest.ref == second.replay_manifest.ref

    release_routing = _objects(first, RoutingEligibilityFact)
    assert len(release_routing) == 42
    assert {x.routing_state for x in release_routing} == {"ROUTING_UNKNOWN"}
    assert {x.applicability_state for x in release_routing} == {"ROUTING_UNKNOWN"}
    assert p.universes[0].target_population_and_sample_frame == "NO_POPULATION_GENERALIZATION"
    assert p.universes[0].sampling_design_regime == "DESIGN_AUTHORITY_NOT_PROMOTED"

    production = Path("rawlsing_next/pre553_source_backed_c11_facade.py").read_text(encoding="utf-8")
    assert "WVS7" not in production
    assert "Q138" not in production
    assert "PWGHT" not in production


def test_pweight_named_physical_cell_never_becomes_an_implicit_weight_or_estimand():
    fx = _fixture(("SLOT-A",), include_pweight_noise=True)
    release = build_validated_source_backed_c11_release_from_stream(fx["stream"], fx["projection"])
    assert not _objects(release, WeightMeasureFact)
    assert fx["projection"].weight_slots == ()
    assert all("PWGHT" not in obj.ref.object_id for obj in release.public_objects)
