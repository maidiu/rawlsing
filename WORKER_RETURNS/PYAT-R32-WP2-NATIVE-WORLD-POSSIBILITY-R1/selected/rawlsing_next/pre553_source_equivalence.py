"""Exact source-to-C11 equivalence certification for PRE553 Wave-03 I06.

This module implements the certification decision surface frozen by P05. It
does not ingest source data, alter C11, pool sources, retire source snapshots,
promote empirical facts to structure, authorize cutover, or create actor/V3
semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import hashlib
from types import MappingProxyType
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_c11_ingest import (
    FRONTIER_VERSION,
    SEMANTIC_PROJECTION_ID,
    SourceReleaseManifest,
)
from rawlsing_next.pre553_c11_integrity import authority_snapshot_set_hash
from rawlsing_next.pre553_c11_repository import C11LogicalRelease
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    EmpiricalUniverse,
    ExactRef,
    canonical_json,
    canonicalize,
    semantic_hash,
)


CERTIFICATION_PROTOCOL_ID = "PRE553_SOURCE_TO_C11_EQUIVALENCE_CERTIFICATION@1.1.0"
P05_PROTOCOL_ID = "PRE553_SOURCE_TO_C11_EQUIVALENCE_PROTOCOL@1.0.0"
BOUND_P05_HEAD = "07f38d1416a13feb2b10ec259bb65f0d1eba284c"
BOUND_P05_PROTOCOL_BLOB = "e2ca14ff73f74f8dfc6542c231f88ea28a15184d"
BOUND_I01_HEAD = "b949280901b48f2ac6d4c711cd31f39b54889767"
BOUND_I02_HEAD = "98c59e55831c9d900878b1027cac86c9738028fc"
BOUND_I03_HEAD = "53ebe82da36187c38aec305109a9482c433dd0e3"

REQUIRED_DIMENSION_IDS = tuple(f"P{i:02d}" for i in range(1, 21))
REQUIRED_FRONTIER_TEST_IDS = tuple(f"T{i:02d}" for i in range(1, 19))
REQUIRED_M01_M18 = tuple(f"M{i:02d}" for i in range(1, 19))
REQUIRED_EXECUTION_HASH_ROLES = frozenset({
    "CERTIFIER_RUNTIME",
    "I02_INGEST_RUNTIME",
    "I03_QUERY_RUNTIME",
    "P05_PROTOCOL",
})
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


def _require_sha256(value: Any, name: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or value.lower() != value
        or any(ch not in "0123456789abcdef" for ch in value)
    ):
        raise SourceEquivalenceIntegrityError(f"{name} must be lowercase sha256")
    return value


def _require_git_sha(value: Any, name: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) not in {40, 64}
        or value.lower() != value
        or any(ch not in "0123456789abcdef" for ch in value)
    ):
        raise SourceEquivalenceIntegrityError(f"{name} must be an exact lowercase git hash")
    return value


def _require_nonnegative_int(value: Any, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise SourceEquivalenceIntegrityError(f"{name} must be a nonnegative integer")
    return value


def _normalized_token(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SourceEquivalenceIntegrityError(f"{name} must be a non-empty string")
    return "_".join(value.strip().upper().replace("-", "_").split())


def sha256_bytes(payload: bytes) -> str:
    if not isinstance(payload, bytes):
        raise SourceEquivalenceIntegrityError("sha256_bytes requires bytes")
    return hashlib.sha256(payload).hexdigest()


def semantic_projection_hash(material: Any) -> str:
    """Canonical exact semantic-projection hash; never a schema/count substitute."""
    return semantic_hash(material)


@dataclass(frozen=True)
class SourceNativeIdentity:
    """Exact source-side identity and retained semantic projection identity."""

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
        if not isinstance(self.source_artifact_ref, ExactRef) or self.source_artifact_ref.kind != "SOURCE_ARTIFACT":
            raise SourceEquivalenceIntegrityError("source_artifact_ref must be exact SOURCE_ARTIFACT")
        if not isinstance(self.source_universe_ref, ExactRef):
            raise SourceEquivalenceIntegrityError("source_universe_ref must be ExactRef")
        if self.source_universe_ref.kind != "EmpiricalUniverse@1.0.0":
            raise SourceEquivalenceIntegrityError("source_universe_ref must bind EmpiricalUniverse@1.0.0")
        if not isinstance(self.source_snapshot_retention_ref, ExactRef):
            raise SourceEquivalenceIntegrityError("source_snapshot_retention_ref must be ExactRef")


@dataclass(frozen=True)
class DimensionEvidence:
    """One exact D13B P01-P20 comparison result."""

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
                    "PASS requires source/C11 canonical semantic projection equality"
                )


@dataclass(frozen=True)
class FrontierReplayEvidence:
    """One exact D12/D13 T01-T18 replay fixture result."""

    test_id: str
    state: DimensionState
    query_or_fixture_hash: str
    source_result_hash: str | None
    c11_result_hash: str | None
    authority_closure_hash: str | None
    evidence_hash: str | None
    reason: str

    def __post_init__(self) -> None:
        if self.test_id not in REQUIRED_FRONTIER_TEST_IDS:
            raise SourceEquivalenceIntegrityError(f"unknown frontier replay test {self.test_id!r}")
        if not isinstance(self.state, DimensionState):
            object.__setattr__(self, "state", DimensionState(self.state))
        if self.state is DimensionState.NOT_APPLICABLE:
            raise SourceEquivalenceIntegrityError(
                "T01-T18 are mandatory for full source-to-C11 certification"
            )
        _require_sha256(self.query_or_fixture_hash, "query_or_fixture_hash")
        if not isinstance(self.reason, str) or not self.reason.strip():
            raise SourceEquivalenceIntegrityError("frontier replay reason must be non-empty")
        for name in (
            "source_result_hash", "c11_result_hash", "authority_closure_hash", "evidence_hash",
        ):
            value = getattr(self, name)
            if value is not None:
                _require_sha256(value, name)
        if self.state is DimensionState.PASS:
            if not all((
                self.source_result_hash,
                self.c11_result_hash,
                self.authority_closure_hash,
                self.evidence_hash,
            )):
                raise SourceEquivalenceIntegrityError("frontier PASS requires complete exact evidence")
            if self.source_result_hash != self.c11_result_hash:
                raise SourceEquivalenceIntegrityError(
                    "frontier PASS requires source/C11 exact semantic result equality"
                )


@dataclass(frozen=True)
class ReplayEquivalenceEvidence:
    """Independent deterministic replay proof on source-native and C11 lanes."""

    source_replay_root_hash: str
    c11_replay_root_hash: str
    source_run_semantic_hashes: tuple[str, ...]
    c11_run_semantic_hashes: tuple[str, ...]
    replay_authority_hash: str
    deterministic: bool

    def __post_init__(self) -> None:
        _require_sha256(self.source_replay_root_hash, "source_replay_root_hash")
        _require_sha256(self.c11_replay_root_hash, "c11_replay_root_hash")
        _require_sha256(self.replay_authority_hash, "replay_authority_hash")
        if len(self.source_run_semantic_hashes) < 2 or len(self.c11_run_semantic_hashes) < 2:
            raise SourceEquivalenceIntegrityError("deterministic replay needs at least two runs per lane")
        for value in (*self.source_run_semantic_hashes, *self.c11_run_semantic_hashes):
            _require_sha256(value, "repeated_run_semantic_hash")
        if not isinstance(self.deterministic, bool):
            raise SourceEquivalenceIntegrityError("deterministic must be bool")
        if self.deterministic:
            if len(set(self.source_run_semantic_hashes)) != 1:
                raise SourceEquivalenceIntegrityError("source-native deterministic replay hashes differ")
            if len(set(self.c11_run_semantic_hashes)) != 1:
                raise SourceEquivalenceIntegrityError("C11 deterministic replay hashes differ")


@dataclass(frozen=True)
class CertificationExecutionReceipt:
    """Exact populated/local-runner evidence required by the frozen P05 protocol."""

    git_head: str
    source_artifact_ref: ExactRef
    c11_release_ref: ExactRef
    source_universe_ref: ExactRef
    source_snapshot_retention_ref: ExactRef
    ingest_authority_hash: str
    query_authority_hash: str
    code_config_hashes: Mapping[str, str]
    typed_state_counts: Mapping[str, int]
    validation_state: DimensionState
    validation_output_hash: str
    output_bundle_hash: str
    source_replay_root_hash: str
    c11_replay_root_hash: str
    clean_worktree_before: bool
    clean_worktree_after: bool
    unauthorized_default_count: int = 0
    unauthorized_coercion_count: int = 0
    fuzzy_mapping_count: int = 0
    unproved_source_pooling_count: int = 0
    source_snapshot_retained: bool = True

    def __post_init__(self) -> None:
        _require_git_sha(self.git_head, "git_head")
        for name in (
            "ingest_authority_hash", "query_authority_hash", "validation_output_hash",
            "output_bundle_hash", "source_replay_root_hash", "c11_replay_root_hash",
        ):
            _require_sha256(getattr(self, name), name)
        if not isinstance(self.validation_state, DimensionState):
            object.__setattr__(self, "validation_state", DimensionState(self.validation_state))
        if self.validation_state is DimensionState.NOT_APPLICABLE:
            raise SourceEquivalenceIntegrityError("execution validation cannot be NOT_APPLICABLE")
        hashes = dict(self.code_config_hashes)
        if not REQUIRED_EXECUTION_HASH_ROLES <= set(hashes):
            missing = sorted(REQUIRED_EXECUTION_HASH_ROLES - set(hashes))
            raise SourceEquivalenceIntegrityError(f"execution code/config hashes missing roles: {missing!r}")
        for role, value in hashes.items():
            if not isinstance(role, str) or not role.strip():
                raise SourceEquivalenceIntegrityError("code/config hash role must be non-empty")
            _require_sha256(value, f"code_config_hashes[{role!r}]")
        counts = dict(self.typed_state_counts)
        if not counts:
            raise SourceEquivalenceIntegrityError("typed_state_counts must be populated")
        for state, count in counts.items():
            if not isinstance(state, str) or not state.strip():
                raise SourceEquivalenceIntegrityError("typed-state count key must be non-empty")
            _require_nonnegative_int(count, f"typed_state_counts[{state!r}]")
        for name in (
            "unauthorized_default_count", "unauthorized_coercion_count",
            "fuzzy_mapping_count", "unproved_source_pooling_count",
        ):
            _require_nonnegative_int(getattr(self, name), name)
        for name in ("clean_worktree_before", "clean_worktree_after", "source_snapshot_retained"):
            if not isinstance(getattr(self, name), bool):
                raise SourceEquivalenceIntegrityError(f"{name} must be bool")
        for name in (
            "source_artifact_ref", "c11_release_ref", "source_universe_ref",
            "source_snapshot_retention_ref",
        ):
            if not isinstance(getattr(self, name), ExactRef):
                raise SourceEquivalenceIntegrityError(f"{name} must be ExactRef")
        object.__setattr__(self, "code_config_hashes", MappingProxyType(dict(sorted(hashes.items()))))
        object.__setattr__(self, "typed_state_counts", MappingProxyType(dict(sorted(counts.items()))))

    def semantic_projection(self) -> dict[str, Any]:
        return {
            "git_head": self.git_head,
            "source_artifact_ref": self.source_artifact_ref.as_dict(),
            "c11_release_ref": self.c11_release_ref.as_dict(),
            "source_universe_ref": self.source_universe_ref.as_dict(),
            "source_snapshot_retention_ref": self.source_snapshot_retention_ref.as_dict(),
            "ingest_authority_hash": self.ingest_authority_hash,
            "query_authority_hash": self.query_authority_hash,
            "code_config_hashes": dict(self.code_config_hashes),
            "typed_state_counts": dict(self.typed_state_counts),
            "validation_state": self.validation_state.value,
            "validation_output_hash": self.validation_output_hash,
            "output_bundle_hash": self.output_bundle_hash,
            "source_replay_root_hash": self.source_replay_root_hash,
            "c11_replay_root_hash": self.c11_replay_root_hash,
            "clean_worktree_before": self.clean_worktree_before,
            "clean_worktree_after": self.clean_worktree_after,
            "unauthorized_default_count": self.unauthorized_default_count,
            "unauthorized_coercion_count": self.unauthorized_coercion_count,
            "fuzzy_mapping_count": self.fuzzy_mapping_count,
            "unproved_source_pooling_count": self.unproved_source_pooling_count,
            "source_snapshot_retained": self.source_snapshot_retained,
        }

    @property
    def receipt_hash(self) -> str:
        return semantic_hash(self.semantic_projection())


@dataclass(frozen=True)
class CertificationRequest:
    source_bytes: bytes
    source_manifest: SourceReleaseManifest
    source_native_identity: SourceNativeIdentity
    source_semantic_projection: Mapping[str, Any]
    c11_release: C11LogicalRelease
    dimension_evidence: tuple[DimensionEvidence, ...]
    frontier_replay_evidence: tuple[FrontierReplayEvidence, ...]
    replay_evidence: ReplayEquivalenceEvidence
    execution_receipt: CertificationExecutionReceipt
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
        if not isinstance(self.source_semantic_projection, Mapping) or not self.source_semantic_projection:
            raise SourceEquivalenceIntegrityError("exact non-empty source_semantic_projection required")
        try:
            normalized_projection = canonicalize(self.source_semantic_projection)
        except Exception as exc:
            raise SourceEquivalenceIntegrityError("source semantic projection is not canonicalizable") from exc
        object.__setattr__(self, "source_semantic_projection", MappingProxyType(dict(normalized_projection)))
        if not isinstance(self.c11_release, C11LogicalRelease):
            raise SourceEquivalenceIntegrityError("sealed C11LogicalRelease required")
        if any(not isinstance(item, DimensionEvidence) for item in self.dimension_evidence):
            raise SourceEquivalenceIntegrityError("dimension_evidence must contain DimensionEvidence only")
        if any(not isinstance(item, FrontierReplayEvidence) for item in self.frontier_replay_evidence):
            raise SourceEquivalenceIntegrityError("frontier_replay_evidence must contain FrontierReplayEvidence only")
        if not isinstance(self.replay_evidence, ReplayEquivalenceEvidence):
            raise SourceEquivalenceIntegrityError("ReplayEquivalenceEvidence required")
        if not isinstance(self.execution_receipt, CertificationExecutionReceipt):
            raise SourceEquivalenceIntegrityError("CertificationExecutionReceipt required")
        _require_sha256(self.authority_snapshot_set_hash, "authority_snapshot_set_hash")
        _require_sha256(self.source_universe_identity_hash, "source_universe_identity_hash")
        shortcut_tokens = {_normalized_token(value, "requested_claim_basis") for value in self.requested_claim_basis}
        shortcuts = NON_CERTIFYING_SHORTCUTS.intersection(shortcut_tokens)
        if shortcuts:
            raise SourceEquivalenceIntegrityError(
                f"non-certifying shortcut basis forbidden: {sorted(shortcuts)!r}"
            )
        authorization_tokens = {
            _normalized_token(value, "requested_authorizations") for value in self.requested_authorizations
        }
        forbidden = FORBIDDEN_AUTHORIZATIONS.intersection(authorization_tokens)
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
    frontier_test_states: Mapping[str, str]
    failed_dimensions: tuple[str, ...]
    blocked_dimensions: tuple[str, ...]
    failed_frontier_tests: tuple[str, ...]
    blocked_frontier_tests: tuple[str, ...]
    certification_identity_hash: str
    execution_receipt_hash: str
    source_snapshot_retention_required: bool
    source_retirement_authorized: bool
    source_pooling_authorized: bool
    structural_promotion_authorized: bool
    cutover_authorized: bool
    actor_or_v3_semantics_authorized: bool
    reasons: tuple[str, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.disposition, CertificationDisposition):
            object.__setattr__(self, "disposition", CertificationDisposition(self.disposition))
        if self.certified != (self.disposition is CertificationDisposition.CERTIFIED):
            raise SourceEquivalenceIntegrityError("certified boolean must match disposition")
        _require_sha256(self.certification_identity_hash, "certification_identity_hash")
        _require_sha256(self.execution_receipt_hash, "execution_receipt_hash")
        if not self.source_snapshot_retention_required:
            raise SourceEquivalenceIntegrityError("source snapshot retention is mandatory in every disposition")
        if any((
            self.source_retirement_authorized,
            self.source_pooling_authorized,
            self.structural_promotion_authorized,
            self.cutover_authorized,
            self.actor_or_v3_semantics_authorized,
        )):
            raise SourceEquivalenceIntegrityError("source equivalence certification cannot grant downstream authority")
        object.__setattr__(self, "dimension_states", MappingProxyType(dict(self.dimension_states)))
        object.__setattr__(self, "frontier_test_states", MappingProxyType(dict(self.frontier_test_states)))

    @property
    def result_ref(self) -> ExactRef:
        return ExactRef(
            "SourceToC11EquivalenceCertification",
            f"{self.source_artifact_ref.object_id}->{self.c11_release_ref.object_id}",
            self.certification_identity_hash,
        )


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


def make_frontier_replay_evidence(
    *,
    test_id: str,
    state: DimensionState | str,
    query_or_fixture: Any,
    source_result: Any | None,
    c11_result: Any | None,
    authority_closure: Any | None,
    evidence_material: Any | None,
    reason: str,
) -> FrontierReplayEvidence:
    state = DimensionState(state)

    def digest(value: Any | None) -> str | None:
        return None if value is None else semantic_hash(value)

    return FrontierReplayEvidence(
        test_id=test_id,
        state=state,
        query_or_fixture_hash=semantic_hash(query_or_fixture),
        source_result_hash=digest(source_result),
        c11_result_hash=digest(c11_result),
        authority_closure_hash=digest(authority_closure),
        evidence_hash=digest(evidence_material),
        reason=reason,
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

    actual_source_projection_hash = semantic_hash(request.source_semantic_projection)
    if actual_source_projection_hash != native.semantic_projection_hash:
        errors.append("SOURCE_NATIVE_SEMANTIC_PROJECTION_HASH_MISMATCH")

    declared_universe_keys = {ref.key for ref in manifest.declared_universe_refs}
    if native.source_universe_ref.key not in declared_universe_keys:
        errors.append("SOURCE_UNIVERSE_NOT_DECLARED_BY_SOURCE_MANIFEST")
    release_universe_keys = {
        obj.ref.key for obj in release.public_objects if isinstance(obj, EmpiricalUniverse)
    }
    if native.source_universe_ref.key not in release_universe_keys:
        errors.append("SOURCE_UNIVERSE_NOT_PRESENT_IN_C11_RELEASE")

    if release.source_artifact_ref != manifest.source_artifact_ref:
        errors.append("C11_SOURCE_ARTIFACT_REF_MISMATCH")
    if release.source_release_manifest_hash != manifest.content_hash:
        errors.append("C11_SOURCE_RELEASE_MANIFEST_HASH_MISMATCH")
    if release.replay_manifest.source_substrate_content_refs != (manifest.source_artifact_ref,):
        errors.append("C11_REPLAY_SOURCE_SUBSTRATE_BINDING_MISMATCH")
    closure_keys = {ref.key for ref in release.replay_manifest.closure_refs}
    if manifest.source_snapshot_retention_ref.key not in closure_keys:
        errors.append("SOURCE_SNAPSHOT_RETENTION_REF_MISSING_FROM_REPLAY_CLOSURE")

    actual_authorities = tuple(
        obj for obj in release.public_objects if isinstance(obj, AuthoritySnapshot)
    )
    if not actual_authorities:
        errors.append("C11_AUTHORITY_SNAPSHOT_OBJECTS_MISSING")
    else:
        actual_authority_hash = authority_snapshot_set_hash(actual_authorities)
        if actual_authority_hash != request.authority_snapshot_set_hash:
            errors.append("AUTHORITY_SNAPSHOT_SET_HASH_MISMATCH")
        if actual_authority_hash != release.replay_manifest.authority_snapshot_set_hash:
            errors.append("C11_REPLAY_AUTHORITY_SNAPSHOT_SET_HASH_MISMATCH")
        actual_authority_keys = {snapshot.authority_ref.key for snapshot in actual_authorities}
        declared_authority_keys = {ref.key for ref in manifest.declared_authority_snapshot_refs}
        if actual_authority_keys != declared_authority_keys:
            errors.append("SOURCE_MANIFEST_C11_AUTHORITY_SET_MISMATCH")

    universe_hash = semantic_hash(native.source_universe_ref.as_dict())
    if universe_hash != request.source_universe_identity_hash:
        errors.append("SOURCE_UNIVERSE_IDENTITY_HASH_MISMATCH")

    if request.replay_evidence.c11_replay_root_hash != release.replay_manifest.content_hash:
        errors.append("C11_REPLAY_ROOT_NOT_BOUND_TO_SEALED_REPLAY_MANIFEST")
    if (
        request.replay_evidence.replay_authority_hash
        != release.replay_manifest.replay_protocol_authority_ref.authority_content_hash
    ):
        errors.append("REPLAY_AUTHORITY_HASH_MISMATCH")
    return tuple(errors)


def _validate_c11_information_closure(release: C11LogicalRelease) -> tuple[str, ...]:
    errors: list[str] = []
    coverage = release.m01_m18_coverage
    for atom in REQUIRED_M01_M18:
        if not coverage.get(atom):
            errors.append(f"C11_{atom}_INFORMATION_CLOSURE_MISSING")
    if release.replay_manifest.frontier_version != FRONTIER_VERSION:
        errors.append("C11_FRONTIER_VERSION_MISMATCH")
    if release.replay_manifest.semantic_projection_id != SEMANTIC_PROJECTION_ID:
        errors.append("C11_SEMANTIC_PROJECTION_ID_MISMATCH")
    return tuple(errors)


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


def _frontier_map(evidence: Sequence[FrontierReplayEvidence]) -> Mapping[str, FrontierReplayEvidence]:
    mapping: dict[str, FrontierReplayEvidence] = {}
    for item in evidence:
        if item.test_id in mapping:
            raise SourceEquivalenceIntegrityError(f"duplicate frontier replay evidence for {item.test_id}")
        mapping[item.test_id] = item
    missing = [test_id for test_id in REQUIRED_FRONTIER_TEST_IDS if test_id not in mapping]
    if missing:
        raise SourceEquivalenceIntegrityError(f"missing mandatory frontier replay tests: {missing!r}")
    return MappingProxyType(mapping)


def _validate_replay(evidence: ReplayEquivalenceEvidence) -> tuple[str, ...]:
    errors: list[str] = []
    if not evidence.deterministic:
        errors.append("REPLAY_NONDETERMINISTIC")
    if len(set(evidence.source_run_semantic_hashes)) != 1:
        errors.append("SOURCE_REPEATED_REPLAY_SEMANTIC_HASH_MISMATCH")
    if len(set(evidence.c11_run_semantic_hashes)) != 1:
        errors.append("C11_REPEATED_REPLAY_SEMANTIC_HASH_MISMATCH")
    if evidence.source_run_semantic_hashes[0] != evidence.c11_run_semantic_hashes[0]:
        errors.append("SOURCE_C11_REPLAY_SEMANTIC_RESULT_MISMATCH")
    return tuple(errors)


def _validate_execution(
    request: CertificationRequest,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    receipt = request.execution_receipt
    failed: list[str] = []
    blocked: list[str] = []
    if receipt.source_artifact_ref != request.source_manifest.source_artifact_ref:
        failed.append("EXECUTION_SOURCE_ARTIFACT_REF_MISMATCH")
    if receipt.c11_release_ref != request.c11_release.release_ref:
        failed.append("EXECUTION_C11_RELEASE_REF_MISMATCH")
    if receipt.source_universe_ref != request.source_native_identity.source_universe_ref:
        failed.append("EXECUTION_SOURCE_UNIVERSE_REF_MISMATCH")
    if receipt.source_snapshot_retention_ref != request.source_manifest.source_snapshot_retention_ref:
        failed.append("EXECUTION_SOURCE_SNAPSHOT_RETENTION_REF_MISMATCH")
    if receipt.source_replay_root_hash != request.replay_evidence.source_replay_root_hash:
        failed.append("EXECUTION_SOURCE_REPLAY_ROOT_MISMATCH")
    if receipt.c11_replay_root_hash != request.replay_evidence.c11_replay_root_hash:
        failed.append("EXECUTION_C11_REPLAY_ROOT_MISMATCH")
    if not receipt.clean_worktree_before:
        failed.append("EXECUTION_WORKTREE_NOT_CLEAN_BEFORE")
    if not receipt.clean_worktree_after:
        failed.append("EXECUTION_WORKTREE_NOT_CLEAN_AFTER")
    if receipt.unauthorized_default_count:
        failed.append("UNAUTHORIZED_DEFAULT_COUNT_NONZERO")
    if receipt.unauthorized_coercion_count:
        failed.append("UNAUTHORIZED_COERCION_COUNT_NONZERO")
    if receipt.fuzzy_mapping_count:
        failed.append("FUZZY_MAPPING_COUNT_NONZERO")
    if receipt.unproved_source_pooling_count:
        failed.append("UNPROVED_SOURCE_POOLING_COUNT_NONZERO")
    if not receipt.source_snapshot_retained:
        failed.append("SOURCE_SNAPSHOT_NOT_RETAINED")
    if receipt.validation_state is DimensionState.FAIL:
        failed.append("POPULATED_VALIDATION_FAILED")
    elif receipt.validation_state is DimensionState.BLOCKED:
        blocked.append("POPULATED_VALIDATION_BLOCKED")
    return tuple(failed), tuple(blocked)


def certify_source_to_c11(request: CertificationRequest) -> CertificationResult:
    """Issue one per-source CERTIFIED/FAILED/BLOCKED disposition.

    FAILED outranks BLOCKED when an observed mandatory mismatch exists.
    A full C11 source-equivalence certificate requires every P01-P20 dimension
    and every T01-T18 replay fixture to PASS. Explicit typed absence is proved
    as a PASS when source and C11 preserve the same governed absence; marking a
    mandatory dimension NOT_APPLICABLE cannot erase the burden.
    """
    dimensions = _dimension_map(request.dimension_evidence)
    frontier = _frontier_map(request.frontier_replay_evidence)
    binding_errors = _validate_source_binding(request)
    closure_errors = _validate_c11_information_closure(request.c11_release)
    replay_errors = _validate_replay(request.replay_evidence)
    execution_failed, execution_blocked = _validate_execution(request)

    failed_dimensions = sorted(
        proof_id for proof_id, item in dimensions.items()
        if item.state is DimensionState.FAIL
    )
    blocked_dimensions = sorted(
        proof_id for proof_id, item in dimensions.items()
        if item.state in {DimensionState.BLOCKED, DimensionState.NOT_APPLICABLE}
        or not item.applicable
    )
    failed_frontier = sorted(
        test_id for test_id, item in frontier.items()
        if item.state is DimensionState.FAIL
    )
    blocked_frontier = sorted(
        test_id for test_id, item in frontier.items()
        if item.state is DimensionState.BLOCKED
    )

    reasons = [
        *binding_errors,
        *closure_errors,
        *replay_errors,
        *execution_failed,
        *execution_blocked,
        *(f"{proof_id}:{dimensions[proof_id].reason}" for proof_id in failed_dimensions),
        *(
            f"{proof_id}:MANDATORY_FULL_C11_DIMENSION_UNRESOLVED:{dimensions[proof_id].reason}"
            for proof_id in blocked_dimensions
        ),
        *(f"{test_id}:{frontier[test_id].reason}" for test_id in failed_frontier),
        *(f"{test_id}:{frontier[test_id].reason}" for test_id in blocked_frontier),
    ]

    observed_failure = bool(
        binding_errors
        or closure_errors
        or replay_errors
        or execution_failed
        or failed_dimensions
        or failed_frontier
    )
    unresolved = bool(execution_blocked or blocked_dimensions or blocked_frontier)

    if observed_failure:
        disposition = CertificationDisposition.FAILED
    elif unresolved:
        disposition = CertificationDisposition.BLOCKED
    else:
        disposition = CertificationDisposition.CERTIFIED

    dimension_states = {
        proof_id: dimensions[proof_id].state.value for proof_id in REQUIRED_DIMENSION_IDS
    }
    frontier_states = {
        test_id: frontier[test_id].state.value for test_id in REQUIRED_FRONTIER_TEST_IDS
    }
    identity_material = {
        "protocol_id": CERTIFICATION_PROTOCOL_ID,
        "p05_protocol_id": P05_PROTOCOL_ID,
        "bound_authority_heads": {
            "P05": BOUND_P05_HEAD,
            "I01": BOUND_I01_HEAD,
            "I02": BOUND_I02_HEAD,
            "I03": BOUND_I03_HEAD,
        },
        "bound_p05_protocol_blob": BOUND_P05_PROTOCOL_BLOB,
        "disposition": disposition.value,
        "source_artifact_ref": request.source_manifest.source_artifact_ref.as_dict(),
        "source_native_identity": {
            "source_family_id": request.source_native_identity.source_family_id,
            "study_product_id": request.source_native_identity.study_product_id,
            "release_id": request.source_native_identity.release_id,
            "instrument_release_id": request.source_native_identity.instrument_release_id,
            "source_universe_ref": request.source_native_identity.source_universe_ref.as_dict(),
            "source_snapshot_retention_ref": request.source_native_identity.source_snapshot_retention_ref.as_dict(),
            "semantic_projection_id": request.source_native_identity.semantic_projection_id,
            "semantic_projection_hash": request.source_native_identity.semantic_projection_hash,
        },
        "c11_release_ref": request.c11_release.release_ref.as_dict(),
        "c11_replay_manifest_ref": request.c11_release.replay_manifest.ref.as_dict(),
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
        "frontier_replay_evidence": {
            test_id: {
                "state": frontier[test_id].state.value,
                "query_or_fixture_hash": frontier[test_id].query_or_fixture_hash,
                "source_result_hash": frontier[test_id].source_result_hash,
                "c11_result_hash": frontier[test_id].c11_result_hash,
                "authority_closure_hash": frontier[test_id].authority_closure_hash,
                "evidence_hash": frontier[test_id].evidence_hash,
            }
            for test_id in REQUIRED_FRONTIER_TEST_IDS
        },
        "replay": {
            "source_replay_root_hash": request.replay_evidence.source_replay_root_hash,
            "c11_replay_root_hash": request.replay_evidence.c11_replay_root_hash,
            "source_run_semantic_hashes": list(request.replay_evidence.source_run_semantic_hashes),
            "c11_run_semantic_hashes": list(request.replay_evidence.c11_run_semantic_hashes),
            "replay_authority_hash": request.replay_evidence.replay_authority_hash,
            "deterministic": request.replay_evidence.deterministic,
        },
        "execution_receipt_hash": request.execution_receipt.receipt_hash,
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
        dimension_states=dimension_states,
        frontier_test_states=frontier_states,
        failed_dimensions=tuple(failed_dimensions),
        blocked_dimensions=tuple(blocked_dimensions),
        failed_frontier_tests=tuple(failed_frontier),
        blocked_frontier_tests=tuple(blocked_frontier),
        certification_identity_hash=identity_hash,
        execution_receipt_hash=request.execution_receipt.receipt_hash,
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
        and first.execution_receipt_hash == second.execution_receipt_hash
        and canonical_json(first.dimension_states) == canonical_json(second.dimension_states)
        and canonical_json(first.frontier_test_states) == canonical_json(second.frontier_test_states)
    )


__all__ = [
    "CERTIFICATION_PROTOCOL_ID",
    "P05_PROTOCOL_ID",
    "BOUND_P05_HEAD",
    "BOUND_I01_HEAD",
    "BOUND_I02_HEAD",
    "BOUND_I03_HEAD",
    "CertificationDisposition",
    "DimensionState",
    "SourceEquivalenceIntegrityError",
    "SourceNativeIdentity",
    "DimensionEvidence",
    "FrontierReplayEvidence",
    "ReplayEquivalenceEvidence",
    "CertificationExecutionReceipt",
    "CertificationRequest",
    "CertificationResult",
    "sha256_bytes",
    "semantic_projection_hash",
    "make_dimension_evidence",
    "make_frontier_replay_evidence",
    "certify_source_to_c11",
    "certification_is_replay_stable",
]