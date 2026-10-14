"""TEST_ONLY modeled N9-like selected world snapshot on the actual M4/M5 selected-service owners.

Reused read-only owners (no mutation):
  * rawlsing_next.m4_v557_v558_publication_repository
      make_structural_object, govern_v557, make_producer_locator,
      build_v557_publication_bundle, build_v558_repository_bundle,
      make_context_query, ContextQueryItem, exact_resolution_key, resolve_v558
  * rawlsing_next.m5_runtime_rsc_peer_prior
      make_structural_currentness_receipt, materialize_resolved_structural_context,
      validate_resolved_structural_context, refresh_structural_currentness

Every premise state below is a declared synthetic MODELED rule of the E05 vertical
experiment, never an observed measurement of any real population, country, house-
hold or person.  The snapshot is explicitly NOT an operative N9 current-world
token and carries no source/model issuer.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef,
    ContextQuery,
    ContextQueryItem,
    ExactRef,
    RepositoryEntry,
    V557DecisionState,
    V557PublicationEntry,
    build_v557_publication_bundle,
    build_v558_repository_bundle,
    exact_resolution_key,
    govern_v557,
    make_context_query,
    make_producer_locator,
    make_structural_object,
    resolve_v558,
    semantic_hash as m4_semantic_hash,
)
from rawlsing_next.m5_runtime_rsc_peer_prior import (
    ResolvedStructuralContext,
    StructuralCurrentnessReceipt,
    StructuralCurrentnessState,
    make_structural_currentness_receipt,
    materialize_resolved_structural_context,
    refresh_structural_currentness,
    validate_resolved_structural_context,
)
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash

WORLD_GRADE = (
    "TEST_ONLY_MODELED_SELECTED_WORLD__NOT_N9_OPERATIVE_CURRENT__NOT_OBSERVED"
)
WORLD_SCHEMA = "W10_TEST_ONLY_MODELED_WORLD_SNAPSHOT@1"
MODELED_FACT_SCHEMA = "W10_TEST_ONLY_MODELED_WORLD_FACT@1"
MODELED_FACT_CLASS = "W10_MODELED_ROUTE_FACT"
MODELED_PRODUCER_FAMILY = "V555"
MODELED_SOURCE_STAGE = "W10_TEST_ONLY_MODELED_WORLD_PROBE"

DECLARED_HISTORICAL_YEAR = 2008
DECLARED_UNIT_SCOPE = (
    "ANONYMOUS_SYNTHETIC_TEST_REGION__INDIVIDUAL_OPPORTUNITY_STRUCTURE"
)
TEST_ONLY_AUTHORITY_ID = (
    "urn:rawlsing:hq295-w10:test-only-modeled-world-authority:r1"
)

INSTITUTIONAL_KEYS = (
    "education_institution.public_school_seat",
    "education_institution.fee_barrier",
    "education_institution.administrative_access",
)
HOUSEHOLD_CARE_KEYS = (
    "household_care.daily_time_obligation",
    "household_care.support_network",
)
CARE_TIME_KEYS = (
    "labor.paid_apprenticeship",
    "labor.time_cost",
    "civil_routes.peer_nonformal_study",
)
CIVIL_INVARIANT_KEYS = ("civil_routes.mutual_aid",)
WORLD_FACT_KEYS = INSTITUTIONAL_KEYS + HOUSEHOLD_CARE_KEYS + CARE_TIME_KEYS + CIVIL_INVARIANT_KEYS

VARIANT_A = "A_BUFFERED_PUBLIC_ACCESS"
VARIANT_B = "B_INSTITUTIONAL_ACCESS_BARRIER_WITH_CARE_PRESSURE"

A_PREMISE_STATES: dict[str, str] = {
    "education_institution.public_school_seat": "AVAILABLE",
    "education_institution.fee_barrier": "NOT_PRESENT_IN_MODEL",
    "education_institution.administrative_access": "ELIGIBLE",
    "household_care.daily_time_obligation": "LOW_IN_MODEL",
    "household_care.support_network": "AVAILABLE",
    "labor.paid_apprenticeship": "CONDITIONAL",
    "labor.time_cost": "POSITIVE",
    "civil_routes.peer_nonformal_study": "AVAILABLE",
    "civil_routes.mutual_aid": "AVAILABLE",
}
B_PREMISE_STATES: dict[str, str] = {
    "education_institution.public_school_seat": "NOT_ACCESSIBLE_UNDER_TEST_RULE",
    "education_institution.fee_barrier": "PRESENT_IN_MODEL",
    "education_institution.administrative_access": "BLOCKED",
    "household_care.daily_time_obligation": "HIGH_IN_MODEL",
    "household_care.support_network": "LIMITED",
    "labor.paid_apprenticeship": "CONDITIONAL",
    "labor.time_cost": "HIGH",
    "civil_routes.peer_nonformal_study": "AVAILABLE_UNDER_CONSTRAINT",
    "civil_routes.mutual_aid": "AVAILABLE",
}


class ModeledWorldError(ValueError):
    """Typed TEST_ONLY modeled-world construction/resolution failure."""


@dataclass(frozen=True)
class WorldSpec:
    variant_id: str
    premise_states: Mapping[str, str]
    declared_historical_year: int = DECLARED_HISTORICAL_YEAR
    declared_unit_scope: str = DECLARED_UNIT_SCOPE

    def premises(self, keys: tuple[str, ...]) -> dict[str, str]:
        return {k: self.premise_states[k] for k in keys}

    def material(self) -> Mapping[str, Any]:
        return {
            "schema": WORLD_SCHEMA,
            "variant_id": self.variant_id,
            "world_grade": WORLD_GRADE,
            "declared_historical_year": self.declared_historical_year,
            "declared_unit_scope": self.declared_unit_scope,
            "premise_states": dict(sorted(self.premise_states.items())),
        }

    @property
    def spec_hash(self) -> str:
        return semantic_hash(self.material())


def world_spec_a() -> WorldSpec:
    return WorldSpec(VARIANT_A, dict(A_PREMISE_STATES))


def world_spec_b() -> WorldSpec:
    return WorldSpec(VARIANT_B, dict(B_PREMISE_STATES))


def with_premise_overrides(
    base: WorldSpec,
    *,
    variant_id: str,
    overrides: Mapping[str, str],
) -> WorldSpec:
    unknown = set(overrides) - set(WORLD_FACT_KEYS)
    if unknown:
        raise ModeledWorldError(f"unknown modeled premise keys: {sorted(unknown)!r}")
    states = dict(base.premise_states)
    states.update(overrides)
    return WorldSpec(
        variant_id,
        states,
        declared_historical_year=base.declared_historical_year,
        declared_unit_scope=base.declared_unit_scope,
    )


def _authority(label: str) -> AuthorityRef:
    return AuthorityRef(
        f"{TEST_ONLY_AUTHORITY_ID}:{label}",
        "TEST_ONLY@1.0.0",
        semantic_hash({"test_only_authority": label}),
    )


def _world_fact_payload(spec: WorldSpec, key: str) -> dict[str, Any]:
    return {
        "schema": MODELED_FACT_SCHEMA,
        "world_grade": WORLD_GRADE,
        "variant_id": spec.variant_id,
        "fact_key": key,
        "modeled_state": spec.premise_states[key],
        "declared_historical_year": spec.declared_historical_year,
        "declared_unit_scope": spec.declared_unit_scope,
        "epistemic_label": "MODELED__NOT_OBSERVED__NOT_MEASURED",
        "spec_hash": spec.spec_hash,
    }


@dataclass(frozen=True)
class ModeledSelectedWorld:
    spec: WorldSpec
    repository: Any
    query: ContextQuery
    resolution: Any
    currentness: StructuralCurrentnessReceipt
    rsc: ResolvedStructuralContext
    validation_receipt: Any
    fact_payloads: Mapping[str, Mapping[str, Any]]
    resolution_keys: Mapping[str, str]

    @property
    def world_grade(self) -> str:
        return WORLD_GRADE

    def identity(self) -> Mapping[str, Any]:
        return {
            "schema": WORLD_SCHEMA,
            "world_grade": WORLD_GRADE,
            "variant_id": self.spec.variant_id,
            "spec_hash": self.spec.spec_hash,
            "declared_historical_year": self.spec.declared_historical_year,
            "declared_unit_scope": self.spec.declared_unit_scope,
            "repository_ref": self.repository.ref.as_dict(),
            "context_query_id": self.query.query_id,
            "context_query_hash": self.query.query_hash,
            "resolution_receipt_ref": self.resolution.receipt.ref.as_dict(),
            "resolution_result_state": self.resolution.receipt.result_state,
            "currentness_receipt_ref": self.currentness.ref.as_dict(),
            "currentness_state": self.currentness.state.value,
            "rsc_ref": self.rsc.ref.as_dict(),
            "validation_receipt_ref": self.validation_receipt.ref.as_dict(),
            "selection_record_refs": [
                s.ref.as_dict() for s in self.resolution.selection_records
            ],
            "resolution_keys": dict(sorted(self.resolution_keys.items())),
        }

    @property
    def replay_hash(self) -> str:
        return semantic_hash(self.identity())


def _build_repository(spec: WorldSpec) -> tuple[Any, Any, dict[str, str], dict[str, Mapping[str, Any]]]:
    entries: list[RepositoryEntry] = []
    publication_entries: list[V557PublicationEntry] = []
    resolution_keys: dict[str, str] = {}
    payloads: dict[str, Mapping[str, Any]] = {}
    for key in WORLD_FACT_KEYS:
        payload = _world_fact_payload(spec, key)
        payloads[key] = payload
        obj = make_structural_object(
            producer_family=MODELED_PRODUCER_FAMILY,
            semantic_class=MODELED_FACT_CLASS,
            object_id=f"urn:test:w10:modeled-world-fact:{spec.variant_id}:{key}",
            schema_id=MODELED_FACT_SCHEMA,
            schema_version="1.0.0",
            typed_state="SUPPORTED",
            producer_allowed_uses=("CONTEXT",),
            payload=payload,
            source_stage=MODELED_SOURCE_STAGE,
        )
        governance = govern_v557(
            obj,
            decision_state=V557DecisionState.ALLOW_CONTEXT_ONLY,
            v557_allowed_uses=("CONTEXT",),
            authority_ref=_authority(f"gov:{spec.variant_id}:{key}"),
        )
        locator = make_producer_locator(
            obj,
            governance,
            logical_collection_kind="W10_TEST_ONLY_MODELED_WORLD",
            authoritative_build_id=f"W10-MODELED-WORLD:{spec.spec_hash}",
            authoritative_build_hash=spec.spec_hash,
            producer_contract_id="W10_TEST_ONLY_MODELED_WORLD_CONTRACT@1",
            producer_contract_version="1.0.0",
            producer_contract_hash=semantic_hash({"contract": "W10_TEST_ONLY_MODELED_WORLD_CONTRACT@1"}),
            producer_rule_bindings=(_authority(f"rule:{spec.variant_id}:{key}"),),
            provenance_locator=f"audit://W10_TEST_ONLY_MODELED_WORLD/{spec.variant_id}/{key}",
        )
        entries.append(RepositoryEntry(obj, governance, locator))
        publication_entries.append(V557PublicationEntry(obj, governance))
        resolution_keys[key] = exact_resolution_key(locator)
    publication = build_v557_publication_bundle(tuple(publication_entries))
    repository = build_v558_repository_bundle(publication, tuple(entries))
    return repository, publication, resolution_keys, payloads


def build_modeled_selected_world(
    spec: WorldSpec,
    *,
    currentness_state: StructuralCurrentnessState = StructuralCurrentnessState.CURRENT,
    requested_uses: tuple[str, ...] = ("CONTEXT",),
    extra_query_keys: tuple[str, ...] = (),
) -> ModeledSelectedWorld:
    """Resolve + materialize one TEST_ONLY modeled world through actual M4/M5."""

    if spec.declared_historical_year != DECLARED_HISTORICAL_YEAR:
        raise ModeledWorldError(
            "probe binds exactly the E05 declared historical year 2008; "
            "other years are refused rather than silently accepted"
        )
    repository, _publication, resolution_keys, payloads = _build_repository(spec)
    items = [
        ContextQueryItem(resolution_keys[key], requested_uses) for key in WORLD_FACT_KEYS
    ]
    for key in extra_query_keys:
        items.append(ContextQueryItem(key, requested_uses))
    query = make_context_query(tuple(items))
    resolution = resolve_v558(repository, query)
    currentness = make_structural_currentness_receipt(
        resolution,
        state=currentness_state,
        authority_ref=_authority(f"currentness:{spec.variant_id}"),
        structural_currentness_basis_ref=ExactRef(
            "W10_TEST_ONLY_CURRENTNESS_BASIS",
            f"urn:test:w10:currentness-basis:{spec.variant_id}",
            semantic_hash({"basis": spec.variant_id}),
        ),
        decision_effective_time_ref=ExactRef(
            "W10_TEST_ONLY_DECISION_EFFECTIVE_TIME",
            f"urn:test:w10:as-of:{spec.declared_historical_year}",
            semantic_hash({"as_of_year": spec.declared_historical_year}),
        ),
    )
    rsc = materialize_resolved_structural_context(repository, query, resolution, currentness)
    validation = validate_resolved_structural_context(
        rsc, repository, query, resolution, currentness
    )
    return ModeledSelectedWorld(
        spec=spec,
        repository=repository,
        query=query,
        resolution=resolution,
        currentness=currentness,
        rsc=rsc,
        validation_receipt=validation,
        fact_payloads=payloads,
        resolution_keys=resolution_keys,
    )


def refresh_world_currentness(
    world: ModeledSelectedWorld,
    *,
    state: StructuralCurrentnessState,
    reason_label: str,
) -> StructuralCurrentnessReceipt:
    """Prospective successor currentness receipt; prior history stays immutable."""

    return refresh_structural_currentness(
        world.currentness,
        world.resolution,
        state=state,
        authority_ref=_authority(f"currentness-refresh:{reason_label}"),
        structural_currentness_basis_ref=ExactRef(
            "W10_TEST_ONLY_CURRENTNESS_BASIS",
            f"urn:test:w10:currentness-basis:refresh:{reason_label}",
            semantic_hash({"basis": reason_label}),
        ),
        decision_effective_time_ref=ExactRef(
            "W10_TEST_ONLY_DECISION_EFFECTIVE_TIME",
            f"urn:test:w10:as-of:refresh:{reason_label}",
            semantic_hash({"as_of": reason_label}),
        ),
        refresh_reason_ref=ExactRef(
            "W10_TEST_ONLY_REFRESH_REASON",
            f"urn:test:w10:refresh-reason:{reason_label}",
            semantic_hash({"reason": reason_label}),
        ),
    )


def world_fact_digest(world: ModeledSelectedWorld) -> str:
    return semantic_hash(
        {key: canonicalize(world.fact_payloads[key]) for key in sorted(WORLD_FACT_KEYS)}
    )


__all__ = [
    "WORLD_GRADE",
    "WORLD_SCHEMA",
    "MODELED_FACT_SCHEMA",
    "DECLARED_HISTORICAL_YEAR",
    "DECLARED_UNIT_SCOPE",
    "INSTITUTIONAL_KEYS",
    "HOUSEHOLD_CARE_KEYS",
    "CARE_TIME_KEYS",
    "CIVIL_INVARIANT_KEYS",
    "WORLD_FACT_KEYS",
    "VARIANT_A",
    "VARIANT_B",
    "A_PREMISE_STATES",
    "B_PREMISE_STATES",
    "ModeledWorldError",
    "WorldSpec",
    "ModeledSelectedWorld",
    "world_spec_a",
    "world_spec_b",
    "with_premise_overrides",
    "build_modeled_selected_world",
    "refresh_world_currentness",
    "world_fact_digest",
    "m4_semantic_hash",
]
