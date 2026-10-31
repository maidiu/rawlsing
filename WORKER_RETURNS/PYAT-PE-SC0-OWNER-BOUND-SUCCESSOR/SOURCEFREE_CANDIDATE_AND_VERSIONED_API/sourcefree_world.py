"""Source-free fixture world provider and exact test-only issuer grants."""
from __future__ import annotations

import copy
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    ExactRef,
    semantic_hash,
)

from owner_bound_successor import (
    ISSUER_TEST_ONLY_SOURCEFREE,
    ROLE_DIRECTIONS,
    WORLD_GRADE,
    ScopedGrant,
    WorldSnapshot,
    selection_digest_for,
)


def fixture_world_values() -> dict[str, Any]:
    return {
        "absolute_horizon": "TEST_ONLY_SOURCEFREE_HORIZON_2021",
        "native_strata": ["TEST_ONLY_STRATUM_A", "TEST_ONLY_STRATUM_B"],
        "nary": {"TEST_ONLY_PROFILE": "A"},
        "f2": {"TEST_ONLY_F2": "FIXTURE"},
        "public_sanctions": ["TEST_ONLY_SANCTION_RECORDED"],
        "public_categories": ["TEST_ONLY_CATEGORY_A", "TEST_ONLY_CATEGORY_B"],
        "contradictory_alternatives": ["TEST_ONLY_ALTERNATIVE_A"],
    }


def _as_exact(value: Any, name: str) -> ExactRef:
    if isinstance(value, ExactRef):
        return value
    if isinstance(value, Mapping):
        return ExactRef(value["kind"], value["object_id"], value["content_hash"])
    raise TypeError(f"{name} must be ExactRef or mapping")


def fixture_negative_status_rows(risk_set_ref: ExactRef) -> tuple[dict[str, Any], ...]:
    risk_set_ref = _as_exact(risk_set_ref, "risk_set_ref")
    states = (
        "OBSERVED_ZERO",
        "VALID_EMPTY",
        "MISSING",
        "UNDERPOWERED",
        "NOT_ASKED",
        "NONCOMPARABLE",
        "HELD_AUTHORITY",
        "DENIED_USE",
    )
    return tuple(
        {
            "state": state,
            "scope": f"urn:test:sourcefree:status-scope:{state.lower()}",
            "risk_set_ref": risk_set_ref.as_dict(),
            "measure": "TEST_ONLY_FIXTURE_MEASURE",
            "observed_complete": False,
        }
        for state in states
    )


def fixture_values_read_receipt() -> dict[str, Any]:
    keys = [
        "urn:test:sourcefree:value:absolute_horizon",
        "urn:test:sourcefree:value:public_sanctions",
        "urn:test:sourcefree:value:native_strata",
    ]
    return {
        "provider_id": "urn:test:sourcefree:values-read-provider:r1",
        "provider_grade": WORLD_GRADE,
        "keys": keys,
        "digest": semantic_hash(keys),
    }


def fixture_generated_binding_echo() -> dict[str, Any]:
    return {
        "tag": "GENERATED_RUNTIME_FACT_REF",
        "upstream_authorship": False,
        "may_use_as_source_observation": False,
        "binding_ref": "urn:test:sourcefree:generated-binding:r1",
    }


class SourceFreeWorldProvider:
    """A deterministic source-free fixture world with audited refresh calls."""

    def __init__(
        self,
        *,
        world_owner: str,
        revision: int,
        risk_set_ref: ExactRef,
        routing_ref: ExactRef,
        values: Mapping[str, Any] | None = None,
        clocks: Mapping[str, Any] | None = None,
        negative_status_rows: Sequence[Mapping[str, Any]] | None = None,
        generated_binding_echo: Mapping[str, Any] | None = None,
        native_sampling_unit: str = "RESPONDENT",
        values_read_receipt: Mapping[str, Any] | None = None,
        reported_selection_digest: str | None = None,
        grade: str = WORLD_GRADE,
    ) -> None:
        self.world_owner = world_owner
        self.revision = revision
        self.risk_set_ref = risk_set_ref
        self.routing_ref = routing_ref
        self.values = copy.deepcopy(dict(values or fixture_world_values()))
        self.clocks = copy.deepcopy(
            dict(
                clocks
                or {
                    "observation_effective": "2008",
                    "publication_knowledge": "2010",
                    "actor_event": None,
                    "request_currentness": "2026-10-14",
                }
            )
        )
        self.negative_status_rows = tuple(
            copy.deepcopy(dict(row))
            for row in (negative_status_rows or fixture_negative_status_rows(risk_set_ref))
        )
        self.generated_binding_echo = copy.deepcopy(
            dict(generated_binding_echo or fixture_generated_binding_echo())
        )
        self.native_sampling_unit = native_sampling_unit
        self.values_read_receipt = copy.deepcopy(
            dict(values_read_receipt or fixture_values_read_receipt())
        )
        self.grade = grade
        self._counts = {"publication": 0, "binding": 0}
        computed = selection_digest_for(
            world_owner=self.world_owner,
            revision=self.revision,
            values=self.values,
            clocks=self.clocks,
            negative_status_rows=self.negative_status_rows,
            generated_binding_echo=self.generated_binding_echo,
            native_sampling_unit=self.native_sampling_unit,
            risk_set_ref=self.risk_set_ref,
            routing_ref=self.routing_ref,
            values_read_receipt=self.values_read_receipt,
        )
        self.selection_digest = reported_selection_digest or computed

    def snapshot(self) -> WorldSnapshot:
        return WorldSnapshot(
            world_owner=self.world_owner,
            revision=self.revision,
            selection_digest=self.selection_digest,
            values=copy.deepcopy(self.values),
            clocks=copy.deepcopy(self.clocks),
            negative_status_rows=tuple(copy.deepcopy(row) for row in self.negative_status_rows),
            generated_binding_echo=copy.deepcopy(self.generated_binding_echo),
            native_sampling_unit=self.native_sampling_unit,
            risk_set_ref=self.risk_set_ref,
            routing_ref=self.routing_ref,
            values_read_receipt=copy.deepcopy(self.values_read_receipt),
            grade=self.grade,
        )

    def refresh_invocation_counts(self) -> Mapping[str, int]:
        return dict(self._counts)

    def _refresh(self, *, channel: str, invocation_token: str) -> dict[str, Any]:
        if channel == "H2_PUBLICATION_BOUNDARY_REFRESH":
            self._counts["publication"] += 1
        elif channel == "H2_GENERATED_BINDING_REFRESH":
            self._counts["binding"] += 1
        else:
            raise ValueError("unsupported refresh channel")
        generation = self.revision + 1
        successor = semantic_hash(
            {
                "channel": channel,
                "world_owner": self.world_owner,
                "base_revision": self.revision,
                "world_result_ref": self.selection_digest,
                "invocation_token": invocation_token,
            }
        )
        return {
            "channel": channel,
            "executed": True,
            "world_owner": self.world_owner,
            "base_revision": self.revision,
            "world_result_ref": self.selection_digest,
            "invocation_token": invocation_token,
            "generation": generation,
            "successor_digest": successor,
        }

    def refresh_publication(self, *, invocation_token: str) -> dict[str, Any]:
        return self._refresh(
            channel="H2_PUBLICATION_BOUNDARY_REFRESH",
            invocation_token=invocation_token,
        )

    def refresh_binding(self, *, invocation_token: str) -> dict[str, Any]:
        return self._refresh(
            channel="H2_GENERATED_BINDING_REFRESH",
            invocation_token=invocation_token,
        )


def make_test_grant(
    *,
    target_ref: ExactRef,
    risk_set_ref: ExactRef,
    world_owner: str,
    operations: Iterable[str] = ROLE_DIRECTIONS,
    authority_id: str = "urn:test:sourcefree:owner-bound-issuer",
    authority_version: str = "1.0.0",
    valid_from: str = "2020-01-01",
    valid_until: str | None = None,
    issuer_grade: str = ISSUER_TEST_ONLY_SOURCEFREE,
    source_promotion_authority: bool = False,
    target_refs: Iterable[str] | None = None,
    risk_set_refs: Iterable[str] | None = None,
    world_owners: Iterable[str] | None = None,
) -> ScopedGrant:
    target_keys = frozenset(target_refs or {target_ref.key})
    risk_keys = frozenset(risk_set_refs or {risk_set_ref.key})
    owners = frozenset(world_owners or {world_owner})
    op_set = frozenset(operations)
    content_hash = semantic_hash(
        {
            "authority_id": authority_id,
            "authority_version": authority_version,
            "issuer_grade": issuer_grade,
            "operations": sorted(op_set),
            "target_refs": sorted(target_keys),
            "risk_set_refs": sorted(risk_keys),
            "world_owners": sorted(owners),
            "valid_from": valid_from,
            "valid_until": valid_until,
            "source_promotion_authority": source_promotion_authority,
        }
    )
    return ScopedGrant(
        authority_ref=AuthorityRef(authority_id, authority_version, content_hash),
        issuer_id=authority_id,
        issuer_version=authority_version,
        issuer_grade=issuer_grade,
        state="ALLOW",
        operations=op_set,
        target_refs=target_keys,
        risk_set_refs=risk_keys,
        world_owners=owners,
        valid_from=valid_from,
        valid_until=valid_until,
        source_promotion_authority=source_promotion_authority,
    )


__all__ = [
    "fixture_world_values",
    "fixture_negative_status_rows",
    "fixture_values_read_receipt",
    "fixture_generated_binding_echo",
    "SourceFreeWorldProvider",
    "make_test_grant",
]
