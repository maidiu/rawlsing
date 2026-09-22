"""Exact immutable PRE553 authority validation.

I01 validates identity, closure, operation/object-family scope and fail-closed
lookup only. It never infers source relations, executes queries/discovery,
decides structural admission, or selects latest/default authority.
"""
from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    CanonicalSemanticObject,
    Pre553IntegrityError,
    Pre553SemanticCollapseError,
    authority_ref,
    canonical_json,
    canonicalize,
    require_public_object_family,
)

AUTHORITY_KINDS = frozenset({
    "SOURCE_SEMANTICS_TOPOLOGY",
    "PHYSICAL_NATIVE_REPRESENTATION_BINDING",
    "NATIVE_CANONICAL_MAPPING_HARMONIZATION",
    "ROUTING_RISK_SET",
    "COORDINATE_SEMANTICS",
    "WEIGHT_DESIGN_ESTIMAND",
    "PREDICATE_GRAMMAR",
    "SOURCE_UNIVERSE_RELATION",
    "SOURCE_EQUIVALENCE",
    "SOURCE_RESPONDENT_LINKAGE",
    "SOURCE_COMPOSITION_POOLING",
    "SOURCE_BACKFILL",
    "DISCOVERY_FRONTIER",
    "STRUCTURAL_ADMISSION",
    "UNCERTAINTY_METHOD",
    "TARGET_USE_PERMISSION",
    "TEMPORAL_EVIDENCE",
    "REPLAY_PROTOCOL",
})
RELATION_AUTHORITY_KINDS = frozenset({
    "SOURCE_UNIVERSE_RELATION",
    "SOURCE_EQUIVALENCE",
    "SOURCE_RESPONDENT_LINKAGE",
    "SOURCE_COMPOSITION_POOLING",
    "SOURCE_BACKFILL",
})

POSITIVE_AUTHORITY_STATE = "ALLOW"
FAIL_CLOSED_STATES = frozenset({
    "DENY", "DEFER", "MISSING_AUTHORITY", "UNKNOWN", "OUT_OF_SCOPE",
    "SUPERSEDED_NOT_REPLAYABLE", "AUTHORITY_HASH_MISMATCH", "AUTHORITY_SCOPE_MISMATCH",
})
FORBIDDEN_SELECTOR_TOKENS = frozenset({
    "LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER", "SEMVER_FALLBACK", "*",
})

# Descriptive ceilings carried from P01. They are intentionally NOT used to
# manufacture a new operation vocabulary: an exact snapshot's own
# governed_operations is dispositive for operation-name validation.
AUTHORITY_KIND_CEILINGS: Mapping[str, tuple[str, ...]] = MappingProxyType({
    "SOURCE_SEMANTICS_TOPOLOGY": (
        "native question/component meaning", "response values/special states",
        "response topology/multiplicity/order/rank"),
    "PHYSICAL_NATIVE_REPRESENTATION_BINDING": (
        "exact source-scoped decoder representation binding; no semantic coercion",),
    "NATIVE_CANONICAL_MAPPING_HARMONIZATION": (
        "native-to-canonical identifier/value transformation",),
    "ROUTING_RISK_SET": ("applicability", "routing", "risk-set semantics"),
    "COORDINATE_SEMANTICS": ("empirical coordinate identity/value/unit/taxonomy",),
    "WEIGHT_DESIGN_ESTIMAND": ("weight basis", "sampling/design", "estimand"),
    "PREDICATE_GRAMMAR": ("empirical predicate/operator/query grammar",),
    "SOURCE_UNIVERSE_RELATION": ("one named source-universe relation kind",),
    "SOURCE_EQUIVALENCE": ("exact semantic/source equivalence in exact scope",),
    "SOURCE_RESPONDENT_LINKAGE": ("exact respondent/person linkage",),
    "SOURCE_COMPOSITION_POOLING": ("exact pooling/composition operation",),
    "SOURCE_BACKFILL": ("exact directional backfill operation",),
    "DISCOVERY_FRONTIER": ("candidate/search/validation/coverage frontier",),
    "STRUCTURAL_ADMISSION": ("one exact empirical fact to one exact structural use",),
    "UNCERTAINTY_METHOD": ("exact uncertainty method",),
    "TARGET_USE_PERMISSION": ("exact target-use permission",),
    "TEMPORAL_EVIDENCE": ("source-native effective/reference-time evidence",),
    "REPLAY_PROTOCOL": ("canonical projection and deterministic replay law",),
})


class Pre553AuthorityError(Pre553IntegrityError):
    """Required exact authority cannot be positively established."""


class Pre553AuthorityConflict(Pre553AuthorityError):
    """Exact authority identity is ambiguous or conflicting."""


def _reject_selector_text(value: str, name: str) -> None:
    upper = value.strip().upper()
    if upper in FORBIDDEN_SELECTOR_TOKENS:
        raise Pre553AuthorityError(f"{name} may not use latest/default/fuzzy/nearest selection")
    if upper.startswith(("LATEST:", "DEFAULT:", "FUZZY:", "NEAREST:", "SEMVER:")):
        raise Pre553AuthorityError(f"{name} may not use mutable/fuzzy selector syntax")


def require_exact_authority_ref(value: AuthorityRef | Mapping[str, Any]) -> AuthorityRef:
    ref = authority_ref(value)
    _reject_selector_text(ref.authority_id, "authority_id")
    _reject_selector_text(ref.authority_version, "authority_version")
    return ref


def validate_authority_snapshot(snapshot: AuthoritySnapshot) -> AuthoritySnapshot:
    if not isinstance(snapshot, AuthoritySnapshot):
        raise Pre553AuthorityError("expected AuthoritySnapshot@1.0.0")
    _reject_selector_text(snapshot.authority_id, "authority_id")
    _reject_selector_text(snapshot.authority_version, "authority_version")
    if snapshot.authority_kind not in AUTHORITY_KINDS:
        raise Pre553AuthorityError(f"unknown authority_kind {snapshot.authority_kind!r}")
    if snapshot.decision_state != snapshot.typed_state:
        raise Pre553AuthorityError("authority decision state mismatch")
    if snapshot.decision_state in {"AUTHORITY_HASH_MISMATCH", "AUTHORITY_SCOPE_MISMATCH"}:
        raise Pre553AuthorityError("authority snapshot is in an integrity-failure state")
    for family in snapshot.governed_object_families:
        if isinstance(family, str) and family.split("@", 1)[0] in {
            "RespondentIdentity", "QuestionVariableBinding", "EmpiricalPredicateReplayBinding",
            "ComparatorReplayBinding", "DiscoveryBranchReplayBinding",
            "StructuralAdmissionReplayBinding", "ReplayManifest",
        }:
            raise Pre553SemanticCollapseError(
                "P10 carrier-internal record cannot become public ontology via authority scope")
    return snapshot


def _material_key(value: Any) -> str:
    return canonical_json(value)


def _scope_contains(scope_value: Any, required: Any) -> bool:
    """Exact containment only; no label, fuzzy, nearest, or hierarchy inference."""
    if scope_value is None:
        return False
    if isinstance(scope_value, str):
        if scope_value in {"UNRESTRICTED_BY_THIS_AUTHORITY", "EXPLICIT_UNRESTRICTED"}:
            return True
        return _material_key(scope_value) == _material_key(required)
    if isinstance(scope_value, Mapping):
        return _material_key(scope_value) == _material_key(required)
    if (
        isinstance(scope_value, (set, frozenset))
        or (
            isinstance(scope_value, Sequence)
            and not isinstance(scope_value, (str, bytes, bytearray))
        )
    ):
        needle = _material_key(required)
        return needle in {_material_key(item) for item in scope_value}
    return _material_key(scope_value) == _material_key(required)


def require_positive_authority(
    snapshot: AuthoritySnapshot,
    *,
    authority_kind: str | None = None,
    operation: str | None = None,
    object_family: str | None = None,
    source_universe_ref: Any | None = None,
    target_use_ref: Any | None = None,
    predicate_or_risk_set_ref: Any | None = None,
) -> AuthoritySnapshot:
    """Validate one exact positive snapshot for one exact use.

    A match means only what this snapshot's exact kind, operation and scope say;
    no adjacent source relation or semantic implication is inferred.
    """
    snapshot = validate_authority_snapshot(snapshot)
    if snapshot.decision_state != POSITIVE_AUTHORITY_STATE:
        raise Pre553AuthorityError(
            f"positive authority required; exact snapshot state is {snapshot.decision_state}")
    if authority_kind is not None and snapshot.authority_kind != authority_kind:
        raise Pre553AuthorityError("authority kind mismatch")
    if operation is not None and operation not in snapshot.governed_operations:
        raise Pre553AuthorityError("operation not named by exact authority")
    if object_family is not None:
        require_public_object_family(object_family)
        bare = object_family.split("@", 1)[0]
        governed = {str(x).split("@", 1)[0] for x in snapshot.governed_object_families}
        if bare not in governed:
            raise Pre553AuthorityError("object family not named by exact authority")

    scope = snapshot.scope_envelope
    if not isinstance(scope, Mapping):
        raise Pre553AuthorityError("scope_envelope must be an exact mapping")
    checks = (
        ("source_universe_refs", source_universe_ref),
        ("target_use_refs", target_use_ref),
        ("predicate_or_risk_set_refs", predicate_or_risk_set_ref),
    )
    for key, required in checks:
        if required is not None and not _scope_contains(scope.get(key), canonicalize(required)):
            raise Pre553AuthorityError(f"exact authority scope does not include {key}")
    return snapshot


@dataclass(frozen=True)
class AuthorityResolution:
    ref: AuthorityRef
    snapshot: AuthoritySnapshot


class AuthorityRegistry:
    """Immutable exact-key authority registry; no latest/default lookup exists."""

    def __init__(self, snapshots: Iterable[AuthoritySnapshot]) -> None:
        by_key: dict[str, AuthoritySnapshot] = {}
        by_id_version: dict[tuple[str, str], str] = {}
        for snapshot in snapshots:
            snapshot = validate_authority_snapshot(snapshot)
            ref = snapshot.authority_ref
            existing_hash = by_id_version.get((ref.authority_id, ref.authority_version))
            if existing_hash is not None and existing_hash != ref.authority_content_hash:
                raise Pre553AuthorityConflict(
                    "same authority id/version has conflicting immutable content hashes")
            by_id_version[(ref.authority_id, ref.authority_version)] = ref.authority_content_hash
            if ref.key in by_key and by_key[ref.key] != snapshot:
                raise Pre553AuthorityConflict("duplicate exact authority ref has conflicting snapshots")
            by_key[ref.key] = snapshot
        self._by_key = MappingProxyType(by_key)

    def __len__(self) -> int:
        return len(self._by_key)

    def resolve_exact(self, ref: AuthorityRef | Mapping[str, Any]) -> AuthorityResolution:
        exact = require_exact_authority_ref(ref)
        snapshot = self._by_key.get(exact.key)
        if snapshot is None:
            try:
                from rawlsing_next.pre553_runtime_context import current_runtime_authorities
                runtime = current_runtime_authorities()
            except ImportError:
                runtime = None
            if runtime is not None:
                snapshot = runtime.resolve_exact_runtime_authority(exact)
            if snapshot is None:
                raise Pre553AuthorityError(
                    "exact historical authority unavailable; no fallback permitted"
                )
        return AuthorityResolution(exact, snapshot)

    def require(
        self,
        ref: AuthorityRef | Mapping[str, Any],
        *,
        authority_kind: str | None = None,
        operation: str | None = None,
        object_family: str | None = None,
        source_universe_ref: Any | None = None,
        target_use_ref: Any | None = None,
        predicate_or_risk_set_ref: Any | None = None,
    ) -> AuthoritySnapshot:
        snapshot = self.resolve_exact(ref).snapshot
        return require_positive_authority(
            snapshot,
            authority_kind=authority_kind,
            operation=operation,
            object_family=object_family,
            source_universe_ref=source_universe_ref,
            target_use_ref=target_use_ref,
            predicate_or_risk_set_ref=predicate_or_risk_set_ref,
        )


def validate_object_authority_closure(
    obj: CanonicalSemanticObject,
    registry: AuthorityRegistry,
) -> tuple[AuthoritySnapshot, ...]:
    if not isinstance(obj, CanonicalSemanticObject):
        raise Pre553AuthorityError("expected PRE553 canonical public object")
    resolved = tuple(registry.resolve_exact(ref).snapshot for ref in obj.authority_snapshot_refs)
    if obj.schema_id != "AuthoritySnapshot" and not resolved:
        raise Pre553AuthorityError("public semantic object lacks authority closure")
    return resolved


def validate_replay_authority_closure(
    *,
    historical_refs: Iterable[AuthorityRef | Mapping[str, Any]],
    registry: AuthorityRegistry,
) -> tuple[AuthoritySnapshot, ...]:
    """Resolve exact historical versions only; later versions never reinterpret history."""
    return tuple(registry.resolve_exact(ref).snapshot for ref in historical_refs)


def validate_relation_authority_only(
    snapshot: AuthoritySnapshot,
    *,
    relation_authority_kind: str,
    exact_relation_operation: str,
) -> AuthoritySnapshot:
    """Validate one exact relation-kind/operation pair without adjacent grants."""
    if relation_authority_kind not in RELATION_AUTHORITY_KINDS:
        raise Pre553AuthorityError("authority kind is not an accepted source-relation kind")
    return require_positive_authority(
        snapshot,
        authority_kind=relation_authority_kind,
        operation=exact_relation_operation,
    )


def validate_structural_admission_authority(
    snapshot: AuthoritySnapshot,
    *,
    exact_admission_operation: str,
    target_use_ref: Any,
    source_universe_ref: Any | None = None,
) -> AuthoritySnapshot:
    """Validate exact admission authority only; this function makes no decision."""
    return require_positive_authority(
        snapshot,
        authority_kind="STRUCTURAL_ADMISSION",
        operation=exact_admission_operation,
        object_family="StructuralEmpiricalAdmission",
        source_universe_ref=source_universe_ref,
        target_use_ref=target_use_ref,
    )


__all__ = [
    "AUTHORITY_KINDS", "RELATION_AUTHORITY_KINDS", "AUTHORITY_KIND_CEILINGS",
    "POSITIVE_AUTHORITY_STATE", "FAIL_CLOSED_STATES", "Pre553AuthorityError",
    "Pre553AuthorityConflict", "AuthorityRegistry", "AuthorityResolution",
    "require_exact_authority_ref", "validate_authority_snapshot", "require_positive_authority",
    "validate_object_authority_closure", "validate_replay_authority_closure",
    "validate_relation_authority_only", "validate_structural_admission_authority",
]
