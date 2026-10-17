from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError, require_positive_authority
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot, EmpiricalCoordinateFact, RespondentEvent
from rawlsing_next.pre553_source_backed_c11_facade import (
    COORDINATE_OWNER_FAMILY,
    RESPONSE_OWNER_FAMILY,
    WEIGHT_OWNER_FAMILY,
    GovernedC11Projection,
    PhysicalSlot,
    PhysicalSlotOwnerAuthorization,
    PhysicalSlotOwnerSet,
    SourceBackedC11FacadeError,
    WeightSlotRule,
    build_validated_source_backed_c11_release_from_stream,
)
from rawlsing_next.tests.test_pre553_empirical_query import _auth, _h, _ref
from rawlsing_next.tests.test_pre553_source_backed_c11_facade_multi_owner_r1 import _fixture as _multi_owner_fixture


def _objects(release, cls):
    return tuple(x for x in release.public_objects if isinstance(x, cls))


def _owner_set_with_refs(projection, *, response_ref=None, coordinate_ref=None):
    owner_set = projection.slot_owner_sets[0]
    current = {owner.owner_family: owner.authority_refs for owner in owner_set.owners}
    if response_ref is not None:
        current[RESPONSE_OWNER_FAMILY] = (response_ref,)
    if coordinate_ref is not None:
        current[COORDINATE_OWNER_FAMILY] = (coordinate_ref,)
    return PhysicalSlotOwnerSet(
        owner_set.slot,
        tuple(
            PhysicalSlotOwnerAuthorization(family, refs)
            for family, refs in current.items()
        ),
    )


def _deny_snapshot(tag: str, *, family: str) -> AuthoritySnapshot:
    return AuthoritySnapshot(
        typed_state="DENY",
        authority_snapshot_refs=(),
        dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref("REPLAY_ROOT", f"authority-{tag}"),
        authority_id=f"I03-AUTH-{tag}",
        authority_version="1.0.0",
        authority_content_hash=_h(f"i03-authority:{tag}:1.0.0"),
        authority_kind="SOURCE_SEMANTICS_TOPOLOGY",
        decision_state="DENY",
        governed_operations=(f"I03-OP-{tag}",),
        governed_object_families=(family,),
        scope_envelope={"source_universe_refs": "EXPLICIT_UNRESTRICTED"},
        effective_time_or_interval="ALL_TIME",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(f"i03-semantics:{tag}"),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", tag),
    )


def _projection_with_weight_owner(owner_ref, *, owner_snapshot):
    fx = _multi_owner_fixture(dual_owner=True, explicit_owner_set=True)
    projection = fx["projection"]
    slot = PhysicalSlot(1, "X")
    weight_auth = _auth(
        "qual-weight-semantic",
        "WEIGHT_DESIGN_ESTIMAND",
        families=(WEIGHT_OWNER_FAMILY,),
    )
    weight_slot = WeightSlotRule(
        slot,
        "W",
        _ref("WEIGHT_SOURCE", "qual-weight-W"),
        weight_auth.authority_ref,
        weight_auth.authority_ref,
        _ref("SCOPE", "qual-weight-W"),
        copy_observed_numeric=True,
    )
    base_owner = projection.slot_owner_sets[0]
    owner_set = PhysicalSlotOwnerSet(
        slot,
        (
            *base_owner.owners,
            PhysicalSlotOwnerAuthorization(WEIGHT_OWNER_FAMILY, (owner_ref,)),
        ),
    )
    snapshots = projection.authority_snapshots + tuple(
        snapshot
        for snapshot in (weight_auth, owner_snapshot)
        if snapshot.authority_ref not in {x.authority_ref for x in projection.authority_snapshots}
    )
    required = projection.required_authority_refs + tuple(
        ref
        for ref in (weight_auth.authority_ref, owner_snapshot.authority_ref)
        if ref not in set(projection.required_authority_refs)
    )
    return replace(
        projection,
        weight_slots=(weight_slot,),
        authority_snapshots=snapshots,
        required_authority_refs=required,
        slot_owner_sets=(owner_set,),
    )


def test_control_exact_dual_owner_with_family_scoped_authorities_closes_deterministically():
    fx = _multi_owner_fixture(dual_owner=True, explicit_owner_set=True)
    first = build_validated_source_backed_c11_release_from_stream(fx["stream"], fx["projection"])
    second = build_validated_source_backed_c11_release_from_stream(fx["stream"], fx["projection"])

    events = _objects(first, RespondentEvent)
    coordinates = _objects(first, EmpiricalCoordinateFact)
    assert len(events) == 1
    assert len(coordinates) == 1
    assert fx["response_owner_auth"].authority_ref in events[0].authority_snapshot_refs
    assert fx["coordinate_owner_auth"].authority_ref in coordinates[0].authority_snapshot_refs
    assert first.release_ref == second.release_ref
    assert first.replay_manifest.ref == second.replay_manifest.ref


def test_exact_hostile_coordinate_authority_as_response_owner_fails_closed():
    fx = _multi_owner_fixture(dual_owner=True, explicit_owner_set=True)
    wrong = fx["coordinate_owner_auth"]
    with pytest.raises(Pre553AuthorityError, match="object family not named"):
        require_positive_authority(wrong, object_family=RESPONSE_OWNER_FAMILY)

    bad_owner_set = _owner_set_with_refs(
        fx["projection"], response_ref=wrong.authority_ref
    )
    with pytest.raises(Pre553AuthorityError, match="object family not named"):
        replace(fx["projection"], slot_owner_sets=(bad_owner_set,))


def test_reciprocal_response_authority_as_coordinate_owner_fails_closed():
    fx = _multi_owner_fixture(dual_owner=True, explicit_owner_set=True)
    bad_owner_set = _owner_set_with_refs(
        fx["projection"], coordinate_ref=fx["response_owner_auth"].authority_ref
    )
    with pytest.raises(Pre553AuthorityError, match="object family not named"):
        replace(fx["projection"], slot_owner_sets=(bad_owner_set,))


def test_weight_owner_family_is_independently_validated_without_weight_policy_expansion():
    lawful_owner = _auth(
        "qual-weight-owner-control",
        "WEIGHT_DESIGN_ESTIMAND",
        families=(WEIGHT_OWNER_FAMILY,),
    )
    lawful = _projection_with_weight_owner(
        lawful_owner.authority_ref, owner_snapshot=lawful_owner
    )
    assert lawful.slot_owner_sets[0].authority_refs_for(WEIGHT_OWNER_FAMILY) == (
        lawful_owner.authority_ref,
    )

    wrong_owner = _auth(
        "qual-wrong-weight-owner",
        "COORDINATE_SEMANTICS",
        families=(COORDINATE_OWNER_FAMILY,),
    )
    with pytest.raises(Pre553AuthorityError, match="object family not named"):
        _projection_with_weight_owner(
            wrong_owner.authority_ref, owner_snapshot=wrong_owner
        )


@pytest.mark.parametrize(
    "family",
    (RESPONSE_OWNER_FAMILY, COORDINATE_OWNER_FAMILY, WEIGHT_OWNER_FAMILY),
)
def test_owner_authority_omission_fails_closed_for_every_supported_family(family):
    with pytest.raises(SourceBackedC11FacadeError, match="lacks explicit authority"):
        PhysicalSlotOwnerAuthorization(family, ())


def test_revoked_response_owner_authority_fails_closed_by_canonical_authority_law():
    fx = _multi_owner_fixture(dual_owner=True, explicit_owner_set=True)
    revoked = _deny_snapshot("qual-response-owner-revoked", family=RESPONSE_OWNER_FAMILY)
    owner_set = _owner_set_with_refs(
        fx["projection"], response_ref=revoked.authority_ref
    )
    snapshots = tuple(
        snapshot
        for snapshot in fx["projection"].authority_snapshots
        if snapshot.authority_ref != fx["response_owner_auth"].authority_ref
    ) + (revoked,)
    required = tuple(
        ref
        for ref in fx["projection"].required_authority_refs
        if ref != fx["response_owner_auth"].authority_ref
    ) + (revoked.authority_ref,)

    with pytest.raises(Pre553AuthorityError, match="positive authority required"):
        replace(
            fx["projection"],
            authority_snapshots=snapshots,
            required_authority_refs=required,
            slot_owner_sets=(owner_set,),
        )


def test_owner_family_repair_does_not_mutate_routing_population_design_or_owner_contract():
    fx = _multi_owner_fixture(dual_owner=True, explicit_owner_set=True)
    projection: GovernedC11Projection = fx["projection"]
    release = build_validated_source_backed_c11_release_from_stream(
        fx["stream"], projection
    )

    routing = tuple(
        obj for obj in release.public_objects if obj.schema_id == "RoutingEligibilityFact"
    )
    assert routing
    assert tuple(x.routing_state for x in routing) == tuple(
        x.routing_state for x in projection.routing
    )
    assert projection.universes[0].target_population_and_sample_frame == "ADULTS"
    assert projection.universes[0].sampling_design_regime == "DESIGN-C05-R2A"
    assert projection.slot_owner_sets[0].contract_id == "PRE553_C11_PHYSICAL_SLOT_OWNER_SET@1.0.0"
