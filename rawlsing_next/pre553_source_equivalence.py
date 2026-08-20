"""Exact source-to-C11 equivalence certification for PRE553 Wave-03 I06.

This module implements the certification decision surface frozen by P05. It
does not ingest source data, alter C11, pool sources, retire source snapshots,
promote empirical facts to structure, or create actor/V3 semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_c11_ingest import SourceReleaseManifest
from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_empirical_objects import ExactRef, canonical_json, semantic_hash


CERTIFICATION_PROTOCOL_ID = "PRE553_SOURCE_TO_C11_EQUIVALENCE_CERTIFICATION@1.0.0"
P05_PROTOCOL_ID = "PRE553_SOURCE_TO_C11_EQUIVALENCE_PROTOCOL@1.0.0"
BOUND_P05_HEAD = "07f38d1416a13feb2b10ec259bb65f0d1eba284c"
BOUND_I01_HEAD = "b949280901b48f2ac6d4c711cd31f39b54889767"
BOUND_I02_HEAD = "98c59e55831c9d900878b1027cac86c9738028fc"
BOUND_I03_HEAD = "53ebe82da36187c38aec305109a9482c433dd0e3"

REQUIRED_DIMENSION_IDS = tuple(f"P{i:02d}" for i in range(1, 21))
REQUIRED_M01_M18 = tuple(f"M{i:02d}" for i in range(1, 19))
NON_CERTIFYING_SHORTCUTS = frozenset({
    "SCHEMA_PARITY_ONLY",
    "ROW_COUNT_PARITY_ONLY",
    "RESPONDENT_COUNT_PARITY_ONLY",
    "AGGREGATE_PARITY_ONLY",
    "SELECTED_QUERY_PARITY_ONLY",
    "SPOT_CHECK_ONLY",
    "MARGINAL_SUMMARY_PARITY_ONLY",
    "SERIALIZED_FILE_HASH_ONLY",
    "SCHEMA_HASH_ONLY",
    "CANONICAL_LABEL_EQUALITY_ONLY",
})
FORBIDDEN_AUTHORIZATIONS = frozenset({
    "SOURCE_RETIREMENT",
    "SOURCE_POOLING",
    "STRUCTURAL_PROMOTION",
    "CUTOVER",
    "ACTOR_SEMANTICS",
    "V3_SEMANTICS",
})


class CertificationDisposition(str, Enum):
    CERTIFIED = "CERTIFIED"
    FAILED = "FAILED"
    BLOCKED = "BLOCKED"


class DimensionState(str, Enum):
    PASS = "PASS"
    FAIL = "FAIL"
    BLOCKED = "BLOCKED"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class SourceEquivalenceIntegrityError(ValueError):
    """Certification input violates the frozen exact-identity contract."""


@dataclass(frozen=True)
class SourceNativeIdentity:
    """Exact source-side identity and retained semantic projection."""

    source_artifact_ref: ExactRef
    source_family_id: str
    study_product_id: str
    release_id: str
    instrument_release_id: str
    source_universe_ref: ExactRef
    source_snapshot_retention_ref: ExactRef
    semantic_projection_id: str
    semantic_projection_hash: str

    def __post_init__(self) -> None:
        for field in (
            "source_family_id", "study_product_id", "release_id",
            "instrument_release_id", "semantic_projection_id",
        ):
            value = getattr(self, field)
            if not isinstance(value, str) or not value.strip():
                raise SourceEquivalenceIntegrityError(f"{field} must be non-empty")
            if value.strip().lower() in {"latest", "default", "nearest", "fuzzy", "*"}:
                raise SourceEquivalenceIntegrityError(f"{field} may not use fallback selection")
        _require_sha256(self.semantic_projection_hash, "semantic_projection_hash")
        if self.source_artifact_ref.kind != "SOURCE_ARTIFACT":
            raise SourceEquivalenceIntegrityError("source_artifact_ref must be SOURCE_ARTIFACT")


@dataclass(frozen=True)
class DimensionEvidence:
    """One exact P01-P20 comparison result."""

    proof_id: str
    state: DimensionState
    source_projection_hash: str | None
    c11_projection_hash: str | None
    authority_closure_hash: str | None
    evidence_hash: str | None
    reason: str
    applicable: bool = True

    def __post_init__(self) -> None:
        if self.proof_id not in REQUIRED_DIMENSION_IDS:
            raise SourceEquivalenceIntegrityError(f"unknown proof dimension {self.proof_id!r}")
        if not isinstance(self.state, DimensionState):
            object.__setattr__(self, "state", DimensionState(self.state))
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise SourceEquivalenceIntegrityError("dimension reason must be non-empty")
        for name in (
            "source_projection_hash", "c11_projection_hash",
            "authority_closure_hash", "evidence_hash",
        ):
            value = getattr(self, name)
            if value is not None:
                _require_sha256(value, name)
        if not self.applicable and self.state is not DimensionState.NOT_APPLICABLE:
            raise SourceEquivalenceIntegrityError("inapplicable dimension must be NOT_APPLICABLE")
        if self.applicable and self.state is DimensionState.NOT_APPLICABLE:
            raise SourceEquivalenceIntegrityError("applicable dimension may not be NOT_APPLICABLE")
        if self.state is DimensionState.PASS:
            if not all((
                self.source_projection_hash,
                self.c11_projection_hash,
                self.authority_closure_hash,
                self.evidence_hash,
            )):
                raise SourceEquivalenceIntegrityError("PASS requires complete exact evidence hashes")
            if self.source_projection_hash != self.c11_projection_hash:
                raise SourceEquivalenceIntegrityError(
                    "PASS requires source/C11 semantic projection equality"
                )


@dataclass(frozen=True)
class ReplayEquivalenceEvidence:
    source_replay_root_hash: str
    c11_replay_root_hash: str
    repeated_run_semantic_hashes: tuple[str, ...]
    replay_authority_hash: str
    deterministic: bool

    def __post_init__(self) -> None:
        _require_sha256(self.source_replay_root_hash, "source_replay_root_hash")
        _require_sha256(self.c11_replay_root_hash, "c11_replay_root_hash")
        _require_sha256(self.replay_authority_hash, "replay_authority_hash")
        if len(self.repeated_run_semantic_hashes) < 2:
            raise SourceEquivalenceIntegrityError("deterministic replay needs at least two runs")
        for value in self.repeated_run_semantic_hashes:
            _require_sha256(value, "repeated_run_semantic_hash")
        if self.deterministic:
            if len(set(self.repeated_run_semantic_hashes)) != 1:
                raise SourceEquivalenceIntegrityError("deterministic replay run hashes differ")
            if self.source_replay_root_hash != self.c11_replay_root_hash:
                raise SourceEquivalenceIntegrityError("deterministic replay roots differ")


@dataclass(frozen=True)
class CertificationRequest:
    source_bytes: bytes
    source_manifest: SourceReleaseManifest
    source_native_identity: SourceNativeIdentity
    c11_release: C11LogicalRelease
    dimension_evidence: tuple[DimensionEvidence, ...]
    replay_evidence: ReplayEquivalenceEvidence
    authority_snapshot_set_hash: str
    source_universe_identity_hash: str
    requested_claim_basis: tuple[str, ...] = ()
    requested_authorizations: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.source_bytes, bytes):
            raise SourceEquivalenceIntegrityError("source_bytes must be exact bytes")
        if not isinstance(self.source_manifest, SourceReleaseManifest):
            raise SourceEquivalenceIntegrityError("exact SourceReleaseManifest required")
        if not isinstance(self.source_native_identity, SourceNativeIdentity):
            raise SourceEquivalenceIntegrityError("SourceNativeIdentity required")
        if not isinstance(self.c11_release, C11LogicalRelease):
            raise SourceEquivalenceIntegrityError("sealed C11LogicalRelease required")
        if not isinstance(self.replay_evidence, ReplayEquivalenceEvidence):
            raise SourceEquivalenceIntegrityError("ReplayEquivalenceEvidence required")
        _require_sha256(self.authority_snapshot_set_hash, "authority_snapshot_set_hash")
        _require_sha256(self.source_universe_identity_hash, "source_universe_identity_hash")
        shortcuts = NON_CERTIFYING_SHORTCUTS.intersection(self.requested_claim_basis)
        if shortcuts:
            raise SourceEquivalenceIntegrityError(
                f"non-certifying shortcut basis forbidden: {sorted(shortcuts)!r}"
            )
        forbidden = FORBIDDEN_AUTHORIZATIONS.intersection(self.requested_authorizations)
        if forbidden:
            raise SourceEquivalenceIntegrityError(
                f"certification cannot grant authorization: {sorted(forbidden)!r}"
            )


@dataclass(frozen=True)
class CertificationResult:
    disposition: CertificationDisposition
    certified: bool
    source_artifact_ref: ExactRef
    c11_release_ref: ExactRef
    source_universe_ref: ExactRef
    protocol_id: str
    dimension_states: Mapping[str, str]
    failed_dimensions: tuple[str, ...]
    blocked_dimensions: tuple[str, ...]
    certification_identity_hash: str
    source_snapshot_retention_required: bool
    source_retirement_authorized: bool
    source_pooling_authorized: bool
    structural_promotion_authorized: bool
    cutover_authorized: bool
    actor_or_v3_semantics_authorized: bool
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        object.__setattr__(self, "dimension_states", MappingProxyType(dict(self.dimension_states)))

    @property
    def result_ref(self) -> ExactRef:
        return ExactRef(
            "SourceToC11EquivalenceCertification",
            f"{self.source_artifact_ref.object_id}->{self.c11_release_ref.object_id}",
            self.certification_identity_hash,
        )


def _require_sha256(value: Any, name: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or value.lower() != value
        or any(ch not in "0123456789abcdef" for ch in value)
    ):
        raise SourceEquivalenceIntegrityError(f"{name} must be lowercase sha256")
    return value


def sha256_bytes(payload: bytes) -> str:
    if not isinstance(payload, bytes):
        raise SourceEquivalenceIntegrityError("sha256_bytes requires bytes")
    return hashlib.sha256(payload).hexdigest()


def semantic_projection_hash(material: Any) -> str:
    """Canonical exact semantic-projection hash; never a schema/count substitute."""
    return semantic_hash(material)


def make_dimension_evidence(
    *,
    proof_id: str,
    state: DimensionState | str,
    source_projection: Any | None,
    c11_projection: Any | None,
    authority_closure: Any | None,
    evidence_material: Any | None,
    reason: str,
    applicable: bool = True,
) -> DimensionEvidence:
    state = DimensionState(state)

    def digest(value: Any | None) -> str | None:
        return None if value is None else semantic_hash(value)

    return DimensionEvidence(
        proof_id=proof_id,
        state=state,
        source_projection_hash=digest(source_projection),
        c11_projection_hash=digest(c11_projection),
        authority_closure_hash=digest(authority_closure),
        evidence_hash=digest(evidence_material),
        reason=reason,
        applicable=applicable,
    )


def _validate_source_binding(request: CertificationRequest) -> tuple[str, ...]:
    errors: list[str] = []
    manifest = request.source_manifest
    native = request.source_native_identity
    release = request.c11_release

    actual_bytes_hash = sha256_bytes(request.source_bytes)
    if actual_bytes_hash != manifest.source_artifact_content_hash:
        errors.append("SOURCE_ARTIFACT_BYTES_HASH_MISMATCH")
    if native.source_artifact_ref != manifest.source_artifact_ref:
        errors.append("SOURCE_ARTIFACT_REF_MISMATCH")
    for field in ("source_family_id", "study_product_id", "release_id", "instrument_release_id"):
        if getattr(native, field) != getattr(manifest, field):
            errors.append(f"SOURCE_IDENTITY_{field.upper()}_MISMATCH")
    if native.source_snapshot_retention_ref != manifest.source_snapshot_retention_ref:
        errors.append("SOURCE_SNAPSHOT_RETENTION_REF_MISMATCH")
    if release.source_artifact_ref != manifest.source_artifact_ref:
        errors.append("C11_SOURCE_ARTIFACT_REF_MISMATCH")
    if release.source_release_manifest_hash != manifest.content_hash:
        errors.append("C11_SOURCE_RELEASE_MANIFEST_HASH_MISMATCH")
    if release.replay_manifest.source_substrate_content_refs != (manifest.source_artifact_ref,):
        errors.append("C11_REPLAY_SOURCE_SUBSTRATE_BINDING_MISMATCH")
    if release.replay_manifest.authority_snapshot_set_hash != request.authority_snapshot_set_hash:
        errors.append("AUTHORITY_SNAPSHOT_SET_HASH_MISMATCH")
    universe_hash = semantic_hash(native.source_universe_ref.as_dict())
    if universe_hash != request.source_universe_identity_hash:
        errors.append("SOURCE_UNIVERSE_IDENTITY_HASH_MISMATCH")
    return tuple(errors)


def _validate_c11_information_closure(release: C11LogicalRelease) -> tuple[str, ...]:
    coverage = release.m01_m18_coverage
    missing = tuple(atom for atom in REQUIRED_M01_M18 if not coverage.get(atom))
    return tuple(f"C11_{atom}_INFORMATION_CLOSURE_MISSING" for atom in missing)


def _dimension_map(evidence: Sequence[DimensionEvidence]) -> Mapping[str, DimensionEvidence]:
    mapping: dict[str, DimensionEvidence] = {}
    for item in evidence:
        if item.proof_id in mapping:
            raise SourceEquivalenceIntegrityError(f"duplicate evidence for {item.proof_id}")
        mapping[item.proof_id] = item
    missing = [proof_id for proof_id in REQUIRED_DIMENSION_IDS if proof_id not in mapping]
    if missing:
        raise SourceEquivalenceIntegrityError(f"missing mandatory proof dimensions: {missing!r}")
    return MappingProxyType(mapping)


def _validate_replay(evidence: ReplayEquivalenceEvidence) -> tuple[str, ...]:
    errors: list[str] = []
    if evidence.source_replay_root_hash != evidence.c11_replay_root_hash:
        errors.append("REPLAY_ROOT_MISMATCH")
    if not evidence.deterministic:
        errors.append("REPLAY_NONDETERMINISTIC")
    if len(set(evidence.repeated_run_semantic_hashes)) != 1:
        errors.append("REPEATED_REPLAY_SEMANTIC_HASH_MISMATCH")
    return tuple(errors)


def certify_source_to_c11(request: CertificationRequest) -> CertificationResult:
    """Issue one per-source CERTIFIED/FAILED/BLOCKED disposition.

    FAILED outranks BLOCKED when an observed mandatory mismatch exists.
    Certification never creates source-retirement, pooling, structural, cutover,
    actor, or V3 authority.
    """
    dimensions = _dimension_map(request.dimension_evidence)
    binding_errors = _validate_source_binding(request)
    closure_errors = _validate_c11_information_closure(request.c11_release)
    replay_errors = _validate_replay(request.replay_evidence)

    failed = sorted(
        proof_id for proof_id, item in dimensions.items()
        if item.applicable and item.state is DimensionState.FAIL
    )
    blocked = sorted(
        proof_id for proof_id, item in dimensions.items()
        if item.applicable and item.state is DimensionState.BLOCKED
    )

    reasons = [
        *binding_errors,
        *closure_errors,
        *replay_errors,
        *(f"{proof_id}:{dimensions[proof_id].reason}" for proof_id in failed),
        *(f"{proof_id}:{dimensions[proof_id].reason}" for proof_id in blocked),
    ]

    observed_failure = bool(binding_errors or closure_errors or replay_errors or failed)
    unresolved = bool(blocked)

    if observed_failure:
        disposition = CertificationDisposition.FAILED
    elif unresolved:
        disposition = CertificationDisposition.BLOCKED
    else:
        disposition = CertificationDisposition.CERTIFIED

    states = {proof_id: dimensions[proof_id].state.value for proof_id in REQUIRED_DIMENSION_IDS}
    identity_material = {
        "protocol_id": CERTIFICATION_PROTOCOL_ID,
        "p05_protocol_id": P05_PROTOCOL_ID,
        "bound_authority_heads": {
            "P05": BOUND_P05_HEAD,
            "I01": BOUND_I01_HEAD,
            "I02": BOUND_I02_HEAD,
            "I03": BOUND_I03_HEAD,
        },
        "disposition": disposition.value,
        "source_artifact_ref": request.source_manifest.source_artifact_ref.as_dict(),
        "source_native_identity": {
            "source_family_id": request.source_native_identity.source_family_id,
            "study_product_id": request.source_native_identity.study_product_id,
            "release_id": request.source_native_identity.release_id,
            "instrument_release_id": request.source_native_identity.instrument_release_id,
            "source_universe_ref": request.source_native_identity.source_universe_ref.as_dict(),
            "semantic_projection_id": request.source_native_identity.semantic_projection_id,
            "semantic_projection_hash": request.source_native_identity.semantic_projection_hash,
        },
        "c11_release_ref": request.c11_release.release_ref.as_dict(),
        "authority_snapshot_set_hash": request.authority_snapshot_set_hash,
        "source_universe_identity_hash": request.source_universe_identity_hash,
        "dimension_evidence": {
            proof_id: {
                "state": dimensions[proof_id].state.value,
                "source_projection_hash": dimensions[proof_id].source_projection_hash,
                "c11_projection_hash": dimensions[proof_id].c11_projection_hash,
                "authority_closure_hash": dimensions[proof_id].authority_closure_hash,
                "evidence_hash": dimensions[proof_id].evidence_hash,
                "applicable": dimensions[proof_id].applicable,
            }
            for proof_id in REQUIRED_DIMENSION_IDS
        },
        "replay": {
            "source_replay_root_hash": request.replay_evidence.source_replay_root_hash,
            "c11_replay_root_hash": request.replay_evidence.c11_replay_root_hash,
            "repeated_run_semantic_hashes": list(request.replay_evidence.repeated_run_semantic_hashes),
            "replay_authority_hash": request.replay_evidence.replay_authority_hash,
            "deterministic": request.replay_evidence.deterministic,
        },
        "source_snapshot_retention_required": True,
        "forbidden_authorizations": sorted(FORBIDDEN_AUTHORIZATIONS),
        "reasons": reasons,
    }
    identity_hash = semantic_hash(identity_material)

    return CertificationResult(
        disposition=disposition,
        certified=disposition is CertificationDisposition.CERTIFIED,
        source_artifact_ref=request.source_manifest.source_artifact_ref,
        c11_release_ref=request.c11_release.release_ref,
        source_universe_ref=request.source_native_identity.source_universe_ref,
        protocol_id=CERTIFICATION_PROTOCOL_ID,
        dimension_states=states,
        failed_dimensions=tuple(failed),
        blocked_dimensions=tuple(blocked),
        certification_identity_hash=identity_hash,
        source_snapshot_retention_required=True,
        source_retirement_authorized=False,
        source_pooling_authorized=False,
        structural_promotion_authorized=False,
        cutover_authorized=False,
        actor_or_v3_semantics_authorized=False,
        reasons=tuple(reasons),
    )


def certification_is_replay_stable(
    first: CertificationResult, second: CertificationResult
) -> bool:
    return (
        first.disposition == second.disposition
        and first.certification_identity_hash == second.certification_identity_hash
        and canonical_json(first.dimension_states) == canonical_json(second.dimension_states)
    )


__all__ = [
    "CERTIFICATION_PROTOCOL_ID",
    "CertificationDisposition",
    "DimensionState",
    "SourceEquivalenceIntegrityError",
    "SourceNativeIdentity",
    "DimensionEvidence",
    "ReplayEquivalenceEvidence",
    "CertificationRequest",
    "CertificationResult",
    "sha256_bytes",
    "semantic_projection_hash",
    "make_dimension_evidence",
    "certify_source_to_c11",
    "certification_is_replay_stable",
]
