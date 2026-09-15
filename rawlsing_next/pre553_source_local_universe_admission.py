"""PRE553 source-local EmpiricalUniverse admission (R1).

This contract permits exact source-local respondent evidence to have a lawful
EmpiricalUniverse source-scope identity without asserting population
representativeness.  Population, weighted-estimand, pooling, backfill and
harmonization authority remain separately governed.

The contract does not infer source authority.  It validates a caller-supplied
positive exact AuthoritySnapshot and materializes only at that authority's
source-local ceiling.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    EmpiricalUniverse,
    ExactRef,
    Pre553IntegrityError,
    canonicalize,
    exact_ref,
    semantic_hash,
)

CONTRACT_ID = "SOURCE_LOCAL_EMPIRICAL_UNIVERSE_ADMISSION_R1@1.0.0"
ADMISSION_OPERATION = "SOURCE_LOCAL_EMPIRICAL_UNIVERSE_ADMISSION_R1"
AUTHORITY_KIND = "SOURCE_SEMANTICS_TOPOLOGY"
GOVERNED_FAMILY = "EmpiricalUniverse@1.0.0"
CLAIM_CEILING = "SOURCE_LOCAL_ONLY"

REQUIRED_NEGATIVE_LIMIT_NAMES = (
    "NO_POPULATION_GENERALIZATION",
    "NO_WEIGHTED_POPULATION_ESTIMAND_UNLESS_SEPARATELY_AUTHORIZED",
    "NO_CROSS_UNIVERSE_POOLING_WITHOUT_RELATION_AUTHORITY",
    "NO_NEAREST_COUNTRY_OR_WAVE_BACKFILL",
)

DOCUMENTARY_STATES = frozenset({
    "NOT_POPULATION_CERTIFIED",
    "DOCUMENTARY_CONTENT_PRESENT__POPULATION_USE_NOT_GRANTED",
})


class SourceLocalUniverseAdmissionError(Pre553IntegrityError):
    """Source-local universe admission or use exceeds the exact R1 ceiling."""


class SourceLocalUse(str, Enum):
    RAW_SINGLE_UNIVERSE = "RAW_SINGLE_UNIVERSE"
    RAW_SOURCE_INDEXED_MULTI_UNIVERSE = "RAW_SOURCE_INDEXED_MULTI_UNIVERSE"
    POPULATION_GENERALIZATION = "POPULATION_GENERALIZATION"
    GOVERNED_WEIGHTED_POPULATION_ESTIMAND = "GOVERNED_WEIGHTED_POPULATION_ESTIMAND"
    AUTHORIZED_COMPOSITE_POOLING = "AUTHORIZED_COMPOSITE_POOLING"
    SOURCE_BACKFILL = "SOURCE_BACKFILL"
    HARMONIZATION = "HARMONIZATION"


ALLOWED_SOURCE_LOCAL_USES = frozenset({
    SourceLocalUse.RAW_SINGLE_UNIVERSE,
    SourceLocalUse.RAW_SOURCE_INDEXED_MULTI_UNIVERSE,
})


def _text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceLocalUniverseAdmissionError(f"{name} must be non-empty text")
    return value.strip()


def _ref(value: ExactRef | Mapping[str, Any], name: str) -> ExactRef:
    try:
        return exact_ref(value, name)
    except Pre553IntegrityError as exc:
        raise SourceLocalUniverseAdmissionError(str(exc)) from exc


def _canonical_ref_set(values: Iterable[ExactRef]) -> tuple[ExactRef, ...]:
    refs = tuple(values)
    if any(not isinstance(ref, ExactRef) for ref in refs):
        raise SourceLocalUniverseAdmissionError("exact refs required")
    return tuple(sorted(set(refs), key=lambda ref: ref.key))


def negative_limit_ref(name: str) -> ExactRef:
    name = _text(name, "negative_limit_name")
    if name not in REQUIRED_NEGATIVE_LIMIT_NAMES:
        raise SourceLocalUniverseAdmissionError(
            f"unknown source-local negative limit {name!r}"
        )
    material = {
        "contract_id": CONTRACT_ID,
        "negative_limit": name,
        "claim_ceiling": CLAIM_CEILING,
    }
    digest = semantic_hash(material)
    return ExactRef(
        "PRE553_SOURCE_LOCAL_NEGATIVE_LIMIT",
        f"urn:rawlsing:pre553:source-local-negative-limit:{name}:sha256:{digest}",
        digest,
    )


REQUIRED_NEGATIVE_LIMIT_REFS = _canonical_ref_set(
    negative_limit_ref(name) for name in REQUIRED_NEGATIVE_LIMIT_NAMES
)


@dataclass(frozen=True)
class DocumentaryField:
    """Documentary material preserved without granting population use."""

    state: str
    content: Any | None = None
    provenance_refs: tuple[ExactRef, ...] = ()
    reason_code: str = "POPULATION_CERTIFICATION_NOT_GRANTED_BY_SOURCE_LOCAL_ADMISSION"

    def __post_init__(self) -> None:
        state = _text(self.state, "documentary.state")
        if state not in DOCUMENTARY_STATES:
            raise SourceLocalUniverseAdmissionError(
                f"unsupported documentary state {state!r}"
            )
        object.__setattr__(self, "state", state)
        reason = _text(self.reason_code, "documentary.reason_code")
        object.__setattr__(self, "reason_code", reason)
        refs = _canonical_ref_set(self.provenance_refs)
        object.__setattr__(self, "provenance_refs", refs)

        if state == "NOT_POPULATION_CERTIFIED":
            if self.content is not None:
                raise SourceLocalUniverseAdmissionError(
                    "NOT_POPULATION_CERTIFIED may not carry asserted documentary content"
                )
        else:
            if self.content is None:
                raise SourceLocalUniverseAdmissionError(
                    "documentary-content-present state requires exact preserved content"
                )
            if not refs:
                raise SourceLocalUniverseAdmissionError(
                    "preserved documentary content requires exact provenance refs"
                )
            canonicalize(self.content)

    @classmethod
    def not_population_certified(cls, reason_code: str) -> "DocumentaryField":
        return cls(
            "NOT_POPULATION_CERTIFIED",
            None,
            (),
            reason_code,
        )

    @classmethod
    def preserve(
        cls,
        content: Any,
        provenance_refs: Iterable[ExactRef],
        *,
        reason_code: str = "DOCUMENTARY_CONTENT_PRESERVED__POPULATION_USE_NOT_GRANTED",
    ) -> "DocumentaryField":
        return cls(
            "DOCUMENTARY_CONTENT_PRESENT__POPULATION_USE_NOT_GRANTED",
            content,
            tuple(provenance_refs),
            reason_code,
        )

    def semantic_material(self) -> Mapping[str, Any]:
        return MappingProxyType({
            "state": self.state,
            "claim_ceiling": CLAIM_CEILING,
            "content": canonicalize(self.content),
            "provenance_refs": tuple(ref.as_dict() for ref in self.provenance_refs),
            "reason_code": self.reason_code,
        })


@dataclass(frozen=True)
class SourceLocalUniverseSpec:
    raw_source_identity: str
    source_family: str
    study_product_release: str
    instrument_release: str
    country_geography: Any
    sampling_geography: Any
    raw_wave: Any
    canonical_wave_if_governed: Any
    field_or_reference_time: Any
    respondent_namespace: str
    source_artifact_import_lineage: Any
    source_artifact_ref: ExactRef
    respondent_scope_ref: ExactRef
    replay_scope_ref: ExactRef
    target_population_and_sample_frame: DocumentaryField
    sampling_design_regime: DocumentaryField
    additional_dependency_refs: tuple[ExactRef, ...] = ()

    def __post_init__(self) -> None:
        for name in (
            "raw_source_identity",
            "source_family",
            "study_product_release",
            "instrument_release",
            "respondent_namespace",
        ):
            object.__setattr__(self, name, _text(getattr(self, name), name))

        for name in (
            "country_geography",
            "sampling_geography",
            "raw_wave",
            "canonical_wave_if_governed",
            "field_or_reference_time",
            "source_artifact_import_lineage",
        ):
            canonicalize(getattr(self, name))

        for name in ("source_artifact_ref", "respondent_scope_ref", "replay_scope_ref"):
            object.__setattr__(self, name, _ref(getattr(self, name), name))

        if not isinstance(self.target_population_and_sample_frame, DocumentaryField):
            raise SourceLocalUniverseAdmissionError(
                "target_population_and_sample_frame must be DocumentaryField"
            )
        if not isinstance(self.sampling_design_regime, DocumentaryField):
            raise SourceLocalUniverseAdmissionError(
                "sampling_design_regime must be DocumentaryField"
            )

        object.__setattr__(
            self,
            "additional_dependency_refs",
            _canonical_ref_set(self.additional_dependency_refs),
        )

    @property
    def exact_scope_refs(self) -> tuple[ExactRef, ...]:
        return _canonical_ref_set((
            self.source_artifact_ref,
            self.respondent_scope_ref,
            self.replay_scope_ref,
        ))

    @property
    def documentary_provenance_refs(self) -> tuple[ExactRef, ...]:
        return _canonical_ref_set((
            *self.target_population_and_sample_frame.provenance_refs,
            *self.sampling_design_regime.provenance_refs,
        ))


def _scope_exact_ref(scope: Mapping[str, Any], key: str) -> ExactRef:
    if key not in scope:
        raise SourceLocalUniverseAdmissionError(
            f"source-local admission authority scope omits {key}"
        )
    return _ref(scope[key], f"authority.scope_envelope.{key}")


def validate_source_local_admission_authority(
    spec: SourceLocalUniverseSpec,
    snapshot: AuthoritySnapshot,
    registry: AuthorityRegistry,
) -> AuthoritySnapshot:
    """Require exact positive source-local universe admission authority."""
    if not isinstance(spec, SourceLocalUniverseSpec):
        raise SourceLocalUniverseAdmissionError("SourceLocalUniverseSpec required")
    if not isinstance(snapshot, AuthoritySnapshot):
        raise SourceLocalUniverseAdmissionError("AuthoritySnapshot required")
    if not isinstance(registry, AuthorityRegistry):
        raise SourceLocalUniverseAdmissionError("AuthorityRegistry required")

    try:
        resolved = registry.resolve_exact(snapshot.authority_ref).snapshot
    except Pre553AuthorityError as exc:
        raise SourceLocalUniverseAdmissionError(
            "exact source-local admission authority unavailable"
        ) from exc
    if resolved != snapshot:
        raise SourceLocalUniverseAdmissionError(
            "supplied admission authority differs from registry-resolved exact snapshot"
        )
    if snapshot.typed_state != "ALLOW" or snapshot.decision_state != "ALLOW":
        raise SourceLocalUniverseAdmissionError(
            "source-local admission authority must be exact positive ALLOW"
        )
    if snapshot.authority_kind != AUTHORITY_KIND:
        raise SourceLocalUniverseAdmissionError(
            f"source-local admission authority kind must be {AUTHORITY_KIND}"
        )
    if ADMISSION_OPERATION not in set(snapshot.governed_operations):
        raise SourceLocalUniverseAdmissionError(
            "source-local admission operation is not governed by authority"
        )
    governed = {str(family).split("@", 1)[0] for family in snapshot.governed_object_families}
    if "EmpiricalUniverse" not in governed:
        raise SourceLocalUniverseAdmissionError(
            "source-local admission authority does not govern EmpiricalUniverse"
        )

    scope = snapshot.scope_envelope
    if not isinstance(scope, Mapping):
        raise SourceLocalUniverseAdmissionError(
            "source-local admission authority scope must be exact mapping"
        )
    if scope.get("claim_ceiling") != CLAIM_CEILING:
        raise SourceLocalUniverseAdmissionError(
            "source-local admission authority must bind SOURCE_LOCAL_ONLY ceiling"
        )
    if scope.get("population_generalization") != "DENIED_UNLESS_SEPARATELY_AUTHORIZED":
        raise SourceLocalUniverseAdmissionError(
            "source-local admission scope must explicitly deny population generalization"
        )
    if scope.get("default_measure_ceiling") != "RAW_ONLY":
        raise SourceLocalUniverseAdmissionError(
            "source-local admission scope must bind RAW_ONLY default measure ceiling"
        )

    required_scope = {
        "source_artifact_ref": spec.source_artifact_ref,
        "respondent_scope_ref": spec.respondent_scope_ref,
        "replay_scope_ref": spec.replay_scope_ref,
    }
    for key, expected in required_scope.items():
        if _scope_exact_ref(scope, key) != expected:
            raise SourceLocalUniverseAdmissionError(
                f"source-local admission authority {key} mismatch"
            )

    dependencies = _canonical_ref_set(snapshot.dependency_refs)
    for required in spec.exact_scope_refs:
        if required not in dependencies:
            raise SourceLocalUniverseAdmissionError(
                f"source-local admission authority dependency closure omits {required.kind}"
            )

    negatives = _canonical_ref_set(
        _ref(value, "authority.negative_limit_refs")
        for value in snapshot.negative_limit_refs
    )
    missing = [ref for ref in REQUIRED_NEGATIVE_LIMIT_REFS if ref not in negatives]
    if missing:
        raise SourceLocalUniverseAdmissionError(
            "source-local admission authority omits required negative limits"
        )
    return snapshot


def materialize_source_local_universe(
    *,
    spec: SourceLocalUniverseSpec,
    admission_authority: AuthoritySnapshot,
    authority_registry: AuthorityRegistry,
) -> EmpiricalUniverse:
    """Materialize one exact source-local EmpiricalUniverse.

    The resulting public object is an exact source-scope identity.  Its
    target/frame/design fields preserve known documentary material but grant no
    population use.
    """
    authority = validate_source_local_admission_authority(
        spec, admission_authority, authority_registry
    )
    dependencies = _canonical_ref_set((
        *spec.exact_scope_refs,
        *spec.documentary_provenance_refs,
        *spec.additional_dependency_refs,
    ))

    universe = EmpiricalUniverse(
        typed_state="UNIVERSE_IDENTIFIED",
        authority_snapshot_refs=(authority.authority_ref,),
        dependency_refs=dependencies,
        producer_replay_locator_or_reference_root=spec.replay_scope_ref,
        raw_source_identity=spec.raw_source_identity,
        source_family=spec.source_family,
        study_product_release=spec.study_product_release,
        instrument_release=spec.instrument_release,
        country_geography=canonicalize(spec.country_geography),
        sampling_geography=canonicalize(spec.sampling_geography),
        raw_wave=canonicalize(spec.raw_wave),
        canonical_wave_if_governed=canonicalize(spec.canonical_wave_if_governed),
        field_or_reference_time=canonicalize(spec.field_or_reference_time),
        target_population_and_sample_frame=spec.target_population_and_sample_frame.semantic_material(),
        sampling_design_regime=spec.sampling_design_regime.semantic_material(),
        respondent_namespace=spec.respondent_namespace,
        source_artifact_import_lineage=canonicalize(spec.source_artifact_import_lineage),
        harmonization_authority_ref=None,
        source_relation_refs=(),
        source_local_admission_contract_id=CONTRACT_ID,
        source_local_claim_ceiling=CLAIM_CEILING,
        source_local_negative_limit_refs=tuple(
            ref.as_dict() for ref in REQUIRED_NEGATIVE_LIMIT_REFS
        ),
    )
    return universe


def validate_source_local_universe(
    universe: EmpiricalUniverse,
    registry: AuthorityRegistry,
) -> AuthoritySnapshot:
    """Validate an already materialized source-local universe and its limits."""
    if not isinstance(universe, EmpiricalUniverse):
        raise SourceLocalUniverseAdmissionError("EmpiricalUniverse required")
    if universe.typed_state != "UNIVERSE_IDENTIFIED":
        raise SourceLocalUniverseAdmissionError(
            "source-local universe must be UNIVERSE_IDENTIFIED"
        )
    if universe.semantic_fields.get("source_local_admission_contract_id") != CONTRACT_ID:
        raise SourceLocalUniverseAdmissionError(
            "universe is not bound to source-local admission contract"
        )
    if universe.semantic_fields.get("source_local_claim_ceiling") != CLAIM_CEILING:
        raise SourceLocalUniverseAdmissionError(
            "source-local universe claim ceiling drift"
        )
    if universe.harmonization_authority_ref is not None:
        raise SourceLocalUniverseAdmissionError(
            "source-local R1 universe may not carry harmonization authority"
        )
    if tuple(universe.source_relation_refs):
        raise SourceLocalUniverseAdmissionError(
            "source-local R1 universe may not carry source relation refs"
        )

    declared_negatives = _canonical_ref_set(
        _ref(value, "universe.source_local_negative_limit_refs")
        for value in universe.semantic_fields.get("source_local_negative_limit_refs", ())
    )
    if declared_negatives != REQUIRED_NEGATIVE_LIMIT_REFS:
        raise SourceLocalUniverseAdmissionError(
            "source-local universe negative-limit set drift"
        )

    matches: list[AuthoritySnapshot] = []
    for ref in universe.authority_snapshot_refs:
        try:
            snapshot = registry.resolve_exact(ref).snapshot
        except Pre553AuthorityError as exc:
            raise SourceLocalUniverseAdmissionError(
                "universe authority closure unavailable"
            ) from exc
        if (
            snapshot.authority_kind == AUTHORITY_KIND
            and ADMISSION_OPERATION in set(snapshot.governed_operations)
        ):
            matches.append(snapshot)
    if len(matches) != 1:
        raise SourceLocalUniverseAdmissionError(
            "source-local universe must resolve exactly one admission authority"
        )
    snapshot = matches[0]
    scope = snapshot.scope_envelope
    if not isinstance(scope, Mapping):
        raise SourceLocalUniverseAdmissionError(
            "source-local universe admission authority scope must remain exact mapping"
        )
    if scope.get("claim_ceiling") != CLAIM_CEILING:
        raise SourceLocalUniverseAdmissionError(
            "source-local universe authority claim ceiling drift"
        )
    if scope.get("population_generalization") != "DENIED_UNLESS_SEPARATELY_AUTHORIZED":
        raise SourceLocalUniverseAdmissionError(
            "source-local universe authority lost population-generalization denial"
        )
    if scope.get("default_measure_ceiling") != "RAW_ONLY":
        raise SourceLocalUniverseAdmissionError(
            "source-local universe authority lost RAW_ONLY default measure ceiling"
        )

    dependencies = _canonical_ref_set(universe.dependency_refs)
    scoped_source = _scope_exact_ref(scope, "source_artifact_ref")
    scoped_respondents = _scope_exact_ref(scope, "respondent_scope_ref")
    scoped_replay = _scope_exact_ref(scope, "replay_scope_ref")
    for required in (scoped_source, scoped_respondents, scoped_replay):
        if required not in dependencies:
            raise SourceLocalUniverseAdmissionError(
                "source-local universe dependency closure no longer matches admission authority scope"
            )
    replay_root = _ref(
        universe.producer_replay_locator_or_reference_root,
        "universe.producer_replay_locator_or_reference_root",
    )
    if replay_root != scoped_replay:
        raise SourceLocalUniverseAdmissionError(
            "source-local universe replay root differs from admission-authority replay scope"
        )

    for field_name in ("target_population_and_sample_frame", "sampling_design_regime"):
        material = getattr(universe, field_name)
        if not isinstance(material, Mapping):
            raise SourceLocalUniverseAdmissionError(
                f"{field_name} must remain typed documentary material"
            )
        state = material.get("state")
        if state not in DOCUMENTARY_STATES:
            raise SourceLocalUniverseAdmissionError(
                f"{field_name} documentary state drift"
            )
        if material.get("claim_ceiling") != CLAIM_CEILING:
            raise SourceLocalUniverseAdmissionError(
                f"{field_name} exceeds source-local claim ceiling"
            )
        content = material.get("content")
        provenance = material.get("provenance_refs")
        if state == "NOT_POPULATION_CERTIFIED" and content is not None:
            raise SourceLocalUniverseAdmissionError(
                f"{field_name} smuggles content into NOT_POPULATION_CERTIFIED"
            )
        if state == "DOCUMENTARY_CONTENT_PRESENT__POPULATION_USE_NOT_GRANTED":
            if content is None or not provenance:
                raise SourceLocalUniverseAdmissionError(
                    f"{field_name} preserved documentary content lost provenance"
                )

    negatives = _canonical_ref_set(
        _ref(value, "authority.negative_limit_refs")
        for value in snapshot.negative_limit_refs
    )
    if any(ref not in negatives for ref in REQUIRED_NEGATIVE_LIMIT_REFS):
        raise SourceLocalUniverseAdmissionError(
            "source-local universe admission authority lost required negative limit"
        )
    return snapshot


def require_source_local_use(
    universe: EmpiricalUniverse,
    registry: AuthorityRegistry,
    requested_use: SourceLocalUse | str,
) -> None:
    """Fail closed when source-local authority is asked to bear a stronger claim."""
    validate_source_local_universe(universe, registry)
    try:
        use = requested_use if isinstance(requested_use, SourceLocalUse) else SourceLocalUse(requested_use)
    except ValueError as exc:
        raise SourceLocalUniverseAdmissionError(
            f"unknown requested source-local use {requested_use!r}"
        ) from exc
    if use not in ALLOWED_SOURCE_LOCAL_USES:
        raise SourceLocalUniverseAdmissionError(
            f"{use.value} exceeds {CLAIM_CEILING}; separate positive authority required"
        )


def population_overlay_basis(universe: EmpiricalUniverse) -> Mapping[str, Any]:
    """Return deterministic documentary/source basis for a later population court.

    No population permission is created.  The overlay court can bind this exact
    universe and its preserved documentary material without replaying raw source
    bytes merely to recover the source-local identity.
    """
    if not isinstance(universe, EmpiricalUniverse):
        raise SourceLocalUniverseAdmissionError("EmpiricalUniverse required")
    material = {
        "source_local_universe_ref": universe.ref.as_dict(),
        "target_population_and_sample_frame": canonicalize(
            universe.target_population_and_sample_frame
        ),
        "sampling_design_regime": canonicalize(universe.sampling_design_regime),
        "source_empirical_dependency_refs": [
            ref.as_dict() for ref in _canonical_ref_set(universe.dependency_refs)
        ],
        "population_permission_granted": False,
    }
    digest = semantic_hash(material)
    return MappingProxyType({
        **material,
        "overlay_basis_hash": digest,
    })


__all__ = [
    "CONTRACT_ID",
    "ADMISSION_OPERATION",
    "AUTHORITY_KIND",
    "GOVERNED_FAMILY",
    "CLAIM_CEILING",
    "REQUIRED_NEGATIVE_LIMIT_NAMES",
    "REQUIRED_NEGATIVE_LIMIT_REFS",
    "DOCUMENTARY_STATES",
    "SourceLocalUniverseAdmissionError",
    "SourceLocalUse",
    "DocumentaryField",
    "SourceLocalUniverseSpec",
    "negative_limit_ref",
    "validate_source_local_admission_authority",
    "materialize_source_local_universe",
    "validate_source_local_universe",
    "require_source_local_use",
    "population_overlay_basis",
]
