"""Deterministic file-neutral logical C11 repository for PRE553 Wave-02 I02.

Repository presence is not semantic authority. Only a release produced by the
I02 atomic ingest validator may be committed here.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Iterable, Mapping

from rawlsing_next.pre553_empirical_objects import CanonicalSemanticObject, ExactRef, canonical_json
from rawlsing_next.pre553_c11_integrity import C11AtomicityError, C11InternalRecord, ReplayManifest

_C11_VALIDATION_SEAL = object()


@dataclass(frozen=True)
class C11LogicalRelease:
    """One sealed C11 logical source release.

    Section records are immutable semantic objects/records.  Their order here is
    canonical storage order only; semantic order/rank remains inside the
    identity-bearing event/topology fields.
    """

    release_id: str
    source_artifact_ref: ExactRef
    source_release_manifest_hash: str
    semantic_release_hash: str
    replay_manifest: ReplayManifest
    public_objects: tuple[CanonicalSemanticObject, ...]
    internal_records: tuple[C11InternalRecord, ...]
    m01_m18_coverage: Mapping[str, tuple[str, ...]]
    _validation_seal: object = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self._validation_seal is not _C11_VALIDATION_SEAL:
            raise C11AtomicityError("C11LogicalRelease may be created only by complete I02 validation")
        if not self.release_id:
            raise C11AtomicityError("sealed release requires release_id")
        if len(self.source_release_manifest_hash) != 64 or len(self.semantic_release_hash) != 64:
            raise C11AtomicityError("sealed release hashes must be sha256 identities")
        object.__setattr__(self, "m01_m18_coverage",
                           MappingProxyType(dict(self.m01_m18_coverage)))

    @property
    def release_ref(self) -> ExactRef:
        return ExactRef("C11LogicalRelease", self.release_id, self.semantic_release_hash)


class C11Repository:
    """Append-only exact-key C11 logical repository; no latest/fuzzy lookup exists."""

    def __init__(self, releases: Iterable[C11LogicalRelease] = ()) -> None:
        self._by_ref: dict[str, C11LogicalRelease] = {}
        self._by_release_id: dict[str, str] = {}
        self._objects: dict[str, CanonicalSemanticObject | C11InternalRecord] = {}
        for release in releases:
            self._commit_validated(release)

    def __len__(self) -> int:
        return len(self._by_ref)

    @property
    def release_refs(self) -> tuple[ExactRef, ...]:
        return tuple(sorted((r.release_ref for r in self._by_ref.values()), key=lambda x: x.key))

    def snapshot_identity(self) -> str:
        """Deterministic repository inventory identity; not semantic permission."""
        return canonical_json([ref.as_dict() for ref in self.release_refs])

    def resolve_release_exact(self, ref: ExactRef) -> C11LogicalRelease:
        if not isinstance(ref, ExactRef) or ref.kind != "C11LogicalRelease":
            raise KeyError("exact C11LogicalRelease ref required")
        release = self._by_ref.get(ref.key)
        if release is None:
            raise KeyError("exact C11 release unavailable; no fallback permitted")
        return release

    def resolve_object_exact(self, ref: ExactRef) -> CanonicalSemanticObject | C11InternalRecord:
        if not isinstance(ref, ExactRef):
            raise KeyError("exact object ref required")
        obj = self._objects.get(ref.key)
        if obj is None:
            raise KeyError("exact C11 object unavailable; no fallback permitted")
        return obj

    def _commit_validated(self, release: C11LogicalRelease) -> None:
        """Atomic commit primitive used only after complete ingest validation."""
        if not isinstance(release, C11LogicalRelease) or release._validation_seal is not _C11_VALIDATION_SEAL:
            raise C11AtomicityError("repository accepts only I02-validated sealed C11LogicalRelease")
        ref = release.release_ref
        prior_hash = self._by_release_id.get(release.release_id)
        if prior_hash is not None and prior_hash != release.semantic_release_hash:
            raise C11AtomicityError("same C11 release_id cannot acquire a different semantic hash")
        if ref.key in self._by_ref:
            return

        # Stage all exact object identities before mutating repository state.
        staged = dict(self._objects)
        for obj in (*release.public_objects, *release.internal_records, release.replay_manifest):
            obj_ref = obj.ref
            prior = staged.get(obj_ref.key)
            if prior is not None and getattr(prior, "content_hash", None) != obj_ref.content_hash:
                raise C11AtomicityError("exact object ref collision has conflicting content")
            staged[obj_ref.key] = obj

        self._objects = staged
        self._by_ref[ref.key] = release
        self._by_release_id[release.release_id] = release.semantic_release_hash


def _make_validated_release(**kwargs: Any) -> C11LogicalRelease:
    return C11LogicalRelease(_validation_seal=_C11_VALIDATION_SEAL, **kwargs)


__all__ = ["C11LogicalRelease", "C11Repository"]
