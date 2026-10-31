"""Source-free fixture assembly for the owner-bound successor tests."""
from __future__ import annotations

from dataclasses import replace
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import ExactRef, exact_ref, semantic_hash
from rawlsing_next.tests.n10e_empirical_slice_fixture import build_provider_case

from first_consumer import SourceFreeWorldRouteConsumer
from n10e_adapter import N10EProducer
from owner_bound_successor import (
    ExactIssuerRegistry,
    N9_SELECTED_IMMUTABLE,
    OwnerBoundRequest,
    ROLE_FORWARD,
    ROLE_REVERSE,
)
from sourcefree_world import SourceFreeWorldProvider, make_test_grant

REQUEST_TIME = "2026-10-14"
ASOF_TIME = "2021-06-30"
WORLD_OWNER = "urn:test:sourcefree:owner-bound-world:r1"
WORLD_REVISION = 7


def _routing_ref() -> ExactRef:
    return ExactRef(
        "TEST_ONLY_SOURCEFREE_ROUTING@1",
        "urn:test:sourcefree:routing:r1",
        semantic_hash({"tag": "sourcefree-routing", "revision": WORLD_REVISION}),
    )


def build_success_fixture(
    *,
    role_direction: str = ROLE_REVERSE,
    world_owner: str = WORLD_OWNER,
    revision: int = WORLD_REVISION,
    request_time: str = REQUEST_TIME,
    asof_time: str = ASOF_TIME,
    world_overrides: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if role_direction == ROLE_FORWARD:
        case = build_provider_case("forward")
        target_value = "yes"
        condition_value = "P1"
    elif role_direction == ROLE_REVERSE:
        case = build_provider_case("reverse")
        target_value = "P1"
        condition_value = "yes"
    else:
        raise ValueError(f"unsupported role_direction: {role_direction!r}")
    producer = N10EProducer(case=case)
    consumer_query = case["consumer_query"]
    binding = consumer_query.conditioner_bindings[0]
    target_ref = exact_ref(consumer_query.target_ref, "target_ref")
    conditioner_coordinate_ref = exact_ref(
        binding.empirical_coordinate_ref, "conditioner_coordinate_ref"
    )
    risk_set_ref = exact_ref(case["empirical_query"].risk_set_ref, "risk_set_ref")
    world_kwargs: dict[str, Any] = dict(world_overrides or {})
    clocks = dict(
        world_kwargs.pop(
            "clocks",
            {
                "observation_effective": "2008",
                "publication_knowledge": "2010",
                "actor_event": None,
                "request_currentness": request_time,
            },
        )
    )
    provider = SourceFreeWorldProvider(
        world_owner=world_owner,
        revision=revision,
        risk_set_ref=risk_set_ref,
        routing_ref=_routing_ref(),
        clocks=clocks,
        **world_kwargs,
    )
    grant = make_test_grant(
        target_ref=target_ref,
        risk_set_ref=risk_set_ref,
        world_owner=world_owner,
        operations={role_direction},
        valid_from="2020-01-01",
        valid_until=None,
    )
    request = OwnerBoundRequest(
        request_id=f"urn:test:sourcefree:request:{role_direction.lower()}:r1",
        role_direction=role_direction,
        target_ref=target_ref,
        risk_set_ref=risk_set_ref,
        conditioner_coordinate_ref=conditioner_coordinate_ref,
        declared_target_value=target_value,
        declared_condition_value=condition_value,
        selected_world_owner=world_owner,
        selected_world_digest=provider.selection_digest,
        world_revision=revision,
        n9_snapshot_state=N9_SELECTED_IMMUTABLE,
        n9_asof_time=asof_time,
        request_time=request_time,
        issuer_ref=grant.authority_ref,
    )
    return {
        "case": case,
        "producer": producer,
        "world_provider": provider,
        "issuer_registry": ExactIssuerRegistry([grant]),
        "consumer": SourceFreeWorldRouteConsumer(),
        "request": request,
        "grant": grant,
        "role_direction": role_direction,
    }


def with_request(fixture: Mapping[str, Any], **changes: Any) -> dict[str, Any]:
    out = dict(fixture)
    out["request"] = replace(fixture["request"], **changes)
    return out


__all__ = [
    "REQUEST_TIME",
    "ASOF_TIME",
    "WORLD_OWNER",
    "WORLD_REVISION",
    "build_success_fixture",
    "with_request",
]
