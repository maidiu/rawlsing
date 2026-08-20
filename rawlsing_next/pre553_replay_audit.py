"""PRE553 Wave-03 R11 authority / replay inspectorate.

This module is intentionally non-semantic. It audits accepted I01-I03 objects,
authority registries, C11 releases and query replay surfaces for exact closure.
It never supplies missing authority, resolves latest/default/fuzzy identities,
or changes runtime semantics.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_authority import (
    AuthorityRegistry,
    Pre553AuthorityError,
    require_exact_authority_ref,
    require_positive_authority,
    validate_replay_authority_closure,
)
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef,
    AuthoritySnapshot,
    CanonicalSemanticObject,
    ExactRef,
    Pre553IntegrityError,
    semantic_hash,
)
from rawlsing_next.pre553_c11_integrity import (
    C11IntegrityError,
    ReplayManifest,
    verify_public_object_integrity,
)
from rawlsing_next.pre553_c11_repository import C11LogicalRelease, C11Repository


class ReplayAuditError(AssertionError):
    """An R11 hostile invariant failed closed."""


@dataclass(frozen=True)
class HostileFinding:
    hostile_class: str
    passed: bool
    detail: str


HOSTILE_CLASSES = (
    "HISTORICAL_AUTHORITY_VERSION_PINNING",
    "AUTHORITY_ID_VERSION_HASH_MISMATCH",
    "MISSING_AUTHORITY",
    "LATEST_DEFAULT_FUZZY_NEAREST_FALLBACK",
    "REPLAY_IDENTITY_TAMPER",
    "SOURCE_CONTENT_TAMPER",
    "SEMANTIC_PROJECTION_TAMPER",
    "SUPERSESSION_REINTERPRETATION",
    "REPOSITORY_PRESENCE_AS_PERMISSION",
    "PROVENANCE_AS_QUERY_DISCOVERY_STRUCTURAL_AUTHORITY",
    "FAILURE_STATE_TO_POSITIVE_AUTHORITY",
)

NONPOSITIVE_AUTHORITY_STATES = frozenset({
    "DENY", "DEFER", "MISSING_AUTHORITY", "UNKNOWN", "OUT_OF_SCOPE",
    "SUPERSEDED_NOT_REPLAYABLE", "AUTHORITY_HASH_MISMATCH", "AUTHORITY_SCOPE_MISMATCH",
})

FORBIDDEN_SELECTOR_PROBES = (
    "LATEST", "DEFAULT", "FUZZY", "NEAREST", "SEMVER", "SEMVER_FALLBACK", "*",
    "LATEST:1", "DEFAULT:any", "FUZZY:authority", "NEAREST:authority", "SEMVER:^1",
)


def _fail(message: str) -> None:
    raise ReplayAuditError(message)


def assert_exact_historical_authorities(
    *, registry: AuthorityRegistry,
    historical_refs: Iterable[AuthorityRef | Mapping[str, Any]],
) -> tuple[AuthoritySnapshot, ...]:
    """Historical replay must resolve the exact id/version/hash tuple only."""
    refs = tuple(require_exact_authority_ref(r) for r in historical_refs)
    try:
        resolved = validate_replay_authority_closure(historical_refs=refs, registry=registry)
    except Pre553AuthorityError as exc:
        _fail(f"historical authority closure failed closed: {exc}")
    if tuple(snapshot.authority_ref for snapshot in resolved) != refs:
        _fail("historical authority resolution changed the exact authority tuple/order")
    return resolved


def assert_authority_tuple_mismatch_rejected(
    *, registry: AuthorityRegistry,
    ref: AuthorityRef | Mapping[str, Any],
) -> None:
    exact = require_exact_authority_ref(ref)
    try:
        registry.resolve_exact(exact)
    except Pre553AuthorityError:
        return
    _fail("authority id/version/hash mismatch unexpectedly resolved")


def assert_missing_authority_rejected(
    *, registry: AuthorityRegistry,
    ref: AuthorityRef | Mapping[str, Any],
) -> None:
    assert_authority_tuple_mismatch_rejected(registry=registry, ref=ref)


def assert_selector_fallback_rejected(selector: str) -> None:
    probe = AuthorityRef(selector, "1.0.0", "0" * 64)
    try:
        require_exact_authority_ref(probe)
    except Pre553AuthorityError:
        return
    _fail(f"forbidden authority selector {selector!r} was accepted")


def assert_all_selector_fallbacks_rejected() -> None:
    for selector in FORBIDDEN_SELECTOR_PROBES:
        assert_selector_fallback_rejected(selector)


def assert_public_semantic_integrity(
    obj: CanonicalSemanticObject,
    *,
    expected_ref: ExactRef | None = None,
) -> CanonicalSemanticObject:
    """Recompute projection and optionally pin against a previously recorded exact ref."""
    try:
        verified = verify_public_object_integrity(obj)
    except (C11IntegrityError, Pre553IntegrityError) as exc:
        _fail(f"semantic projection tamper detected: {exc}")
    if semantic_hash(obj.semantic_projection()) != obj.content_hash:
        _fail("semantic projection hash mismatch")
    if obj.ref.object_id != obj.object_id or obj.ref.content_hash != obj.content_hash:
        _fail("public ExactRef no longer matches object identity")
    if expected_ref is not None and obj.ref != expected_ref:
        _fail("public object no longer matches previously pinned replay identity")
    return verified


def assert_replay_manifest_integrity(
    manifest: ReplayManifest,
    *,
    expected_ref: ExactRef | None = None,
) -> ReplayManifest:
    """Replay manifest must match its pinned historical identity, not merely self-rehash."""
    if not isinstance(manifest, ReplayManifest):
        _fail("expected accepted I02 ReplayManifest")
    if semantic_hash(manifest.semantic_projection()) != manifest.content_hash:
        _fail("ReplayManifest semantic identity tamper")
    if manifest.ref.content_hash != manifest.content_hash:
        _fail("ReplayManifest ExactRef hash mismatch")
    if expected_ref is not None and manifest.ref != expected_ref:
        _fail("ReplayManifest no longer matches the pinned historical replay identity")
    return manifest


def assert_exact_source_content(
    *, actual: Iterable[ExactRef], expected: Iterable[ExactRef]
) -> None:
    actual_refs = tuple(sorted(actual, key=lambda r: r.key))
    expected_refs = tuple(sorted(expected, key=lambda r: r.key))
    if actual_refs != expected_refs:
        _fail("source-content exact refs differ; no path/label/latest fallback is lawful")


def assert_release_replay_closure(
    release: C11LogicalRelease,
    *,
    expected_release_ref: ExactRef | None = None,
    expected_manifest_ref: ExactRef | None = None,
    expected_source_refs: Iterable[ExactRef] | None = None,
) -> C11LogicalRelease:
    """Audit a sealed I02 release without treating repository presence as permission."""
    if not isinstance(release, C11LogicalRelease):
        _fail("expected accepted I02 C11LogicalRelease")
    if expected_release_ref is not None and release.release_ref != expected_release_ref:
        _fail("C11 release identity differs from pinned historical release ref")
    assert_replay_manifest_integrity(release.replay_manifest, expected_ref=expected_manifest_ref)
    if expected_source_refs is not None:
        assert_exact_source_content(
            actual=release.replay_manifest.source_substrate_content_refs,
            expected=expected_source_refs,
        )
    for obj in release.public_objects:
        assert_public_semantic_integrity(obj)
    return release


def assert_repository_exact_only(
    *, repository: C11Repository, release_ref: ExactRef
) -> C11LogicalRelease:
    if not isinstance(repository, C11Repository):
        _fail("expected accepted I02 C11Repository")
    try:
        release = repository.resolve_release_exact(release_ref)
    except KeyError as exc:
        _fail(f"exact release unavailable and correctly cannot fallback: {exc}")
    if release.release_ref != release_ref:
        _fail("repository returned a non-exact release")
    return release


def assert_repository_presence_not_permission(
    *, repository: C11Repository, registry: AuthorityRegistry, required_ref: AuthorityRef
) -> None:
    if not isinstance(repository, C11Repository):
        _fail("expected accepted I02 C11Repository")
    try:
        registry.resolve_exact(required_ref)
    except Pre553AuthorityError:
        return
    _fail("test precondition invalid: required authority is actually present")


def assert_provenance_not_permission(
    *,
    provenance_refs: Iterable[ExactRef],
    registry: AuthorityRegistry,
    required_authority_ref: AuthorityRef,
    authority_kind: str,
    operation: str,
    object_family: str | None = None,
) -> None:
    tuple(provenance_refs)  # provenance is intentionally inert as permission
    try:
        snapshot = registry.resolve_exact(required_authority_ref).snapshot
        require_positive_authority(
            snapshot,
            authority_kind=authority_kind,
            operation=operation,
            object_family=object_family,
        )
    except Pre553AuthorityError:
        return
    _fail("provenance test unexpectedly had a valid explicit positive authority")


def assert_supersession_does_not_reinterpret(
    *, registry: AuthorityRegistry, historical_ref: AuthorityRef, superseding_ref: AuthorityRef
) -> None:
    historical = registry.resolve_exact(historical_ref).snapshot
    newer = registry.resolve_exact(superseding_ref).snapshot
    if historical.authority_ref == newer.authority_ref:
        _fail("supersession fixture must use two distinct exact authority tuples")
    resolved = validate_replay_authority_closure(
        historical_refs=(historical_ref,), registry=registry
    )
    if resolved != (historical,):
        _fail("historical replay was reinterpreted through superseding authority")


def assert_failure_state_never_positive(
    snapshot: AuthoritySnapshot,
    *, operation: str | None = None, object_family: str | None = None,
) -> None:
    if snapshot.decision_state not in NONPOSITIVE_AUTHORITY_STATES:
        _fail("fixture must carry a nonpositive/failure authority state")
    try:
        require_positive_authority(snapshot, operation=operation, object_family=object_family)
    except Pre553AuthorityError:
        return
    _fail(f"failure authority state {snapshot.decision_state!r} became positive")


def audit_hostile_class(hostile_class: str, thunk) -> HostileFinding:
    if hostile_class not in HOSTILE_CLASSES:
        raise ReplayAuditError(f"unknown R11 hostile class {hostile_class!r}")
    try:
        thunk()
    except Exception as exc:
        return HostileFinding(hostile_class, False, f"unexpected inspectorate failure: {exc}")
    return HostileFinding(hostile_class, True, "zero semantic fallback preserved")


__all__ = [
    "ReplayAuditError", "HostileFinding", "HOSTILE_CLASSES",
    "NONPOSITIVE_AUTHORITY_STATES", "FORBIDDEN_SELECTOR_PROBES",
    "assert_exact_historical_authorities", "assert_authority_tuple_mismatch_rejected",
    "assert_missing_authority_rejected", "assert_selector_fallback_rejected",
    "assert_all_selector_fallbacks_rejected", "assert_public_semantic_integrity",
    "assert_replay_manifest_integrity", "assert_exact_source_content",
    "assert_release_replay_closure", "assert_repository_exact_only",
    "assert_repository_presence_not_permission", "assert_provenance_not_permission",
    "assert_supersession_does_not_reinterpret", "assert_failure_state_never_positive",
    "audit_hostile_class",
]
