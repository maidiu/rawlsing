"""Production constructor for the adopted PRE-V3 objective world release root.

The root is an immutable, content-addressed binding over already-authorized
objective PRE-V3 publication/repository material and independently supplied
objective scope / valid-time authority. It does not resolve V558, infer
currentness, inspect V3 state, or read a wall clock.
"""
from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from rawlsing_next.m1_temporal_v554_admission_dedup import semantic_hash
from rawlsing_next.m4_v557_v558_publication_repository import (
    AuthorityRef,
    ExactRef,
    M4IntegrityError,
    V558RepositoryBundle,
    _validate_repository_checksum,
)

WORLD_ROOT_SCHEMA = "PREV3_OBJECTIVE_WORLD_RELEASE_ROOT_R1"
WORLD_ROOT_REF_KIND = WORLD_ROOT_SCHEMA
OBJECTIVE_WORLD_SCOPE_REF_KIND = "PREV3_OBJECTIVE_WORLD_SCOPE"
OBJECTIVE_WORLD_VALIDITY_REF_KIND = "PREV3_OBJECTIVE_WORLD_VALIDITY"

_FORBIDDEN_AUTHORITY_SOURCE_TOKENS = (
    "actor", "person", "persona", "cursor", "wall_clock", "wall-clock",
)
_V3_TOKEN = re.compile(r"(^|[:/_-])v3([:/_-]|$)")
_FORBIDDEN_SELECTOR_TOKENS = ("latest", "default", "fuzzy")


class ObjectiveWorldRootError(ValueError):
    """The objective world root tuple is malformed or jurisdictionally invalid."""


def _authority_dict(value: AuthorityRef) -> dict[str, str]:
    if not isinstance(value, AuthorityRef):
        raise ObjectiveWorldRootError("world-root authority inputs must be exact M4 AuthorityRef values")
    return value.as_dict()


def _exact_ref(value: Any, *, expected_kind: str, field: str) -> ExactRef:
    if not isinstance(value, ExactRef):
        raise ObjectiveWorldRootError(f"{field} must be an exact M4 ExactRef")
    if value.kind != expected_kind:
        raise ObjectiveWorldRootError(
            f"{field} must have exact kind {expected_kind!r}, got {value.kind!r}"
        )
    lower = value.object_id.lower()
    if any(token in lower for token in _FORBIDDEN_SELECTOR_TOKENS):
        raise ObjectiveWorldRootError(f"{field} may not use latest/default/fuzzy selection")
    if any(token in lower for token in _FORBIDDEN_AUTHORITY_SOURCE_TOKENS) or _V3_TOKEN.search(lower):
        raise ObjectiveWorldRootError(
            f"{field} may not derive objective world validity from V3/actor/person/runtime cursor"
        )
    return value


def _predecessor_ref(value: ExactRef | None) -> ExactRef | None:
    if value is None:
        return None
    if not isinstance(value, ExactRef) or value.kind != WORLD_ROOT_REF_KIND:
        raise ObjectiveWorldRootError(
            f"predecessor_world_root_ref must be {WORLD_ROOT_REF_KIND} or null"
        )
    return value


@dataclass(frozen=True)
class ObjectiveWorldReleaseRoot:
    schema: str
    release_authority_ref: AuthorityRef
    repository_ref: ExactRef
    publication_bundle_ref: ExactRef
    index_manifest_ref: ExactRef
    objective_world_scope_ref: ExactRef
    valid_time_authority_ref: AuthorityRef
    world_validity_ref: ExactRef
    predecessor_world_root_ref: ExactRef | None
    root_id: str
    root_hash: str

    @property
    def ref(self) -> ExactRef:
        return ExactRef(WORLD_ROOT_REF_KIND, self.root_id, self.root_hash)

    def canonical_material(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "release_authority_ref": self.release_authority_ref.as_dict(),
            "repository_ref": self.repository_ref.as_dict(),
            "publication_bundle_ref": self.publication_bundle_ref.as_dict(),
            "index_manifest_ref": self.index_manifest_ref.as_dict(),
            "objective_world_scope_ref": self.objective_world_scope_ref.as_dict(),
            "valid_time_authority_ref": self.valid_time_authority_ref.as_dict(),
            "world_validity_ref": self.world_validity_ref.as_dict(),
            "predecessor_world_root_ref": (
                self.predecessor_world_root_ref.as_dict()
                if self.predecessor_world_root_ref is not None
                else None
            ),
        }


def _constructor_material(
    *,
    release_authority_ref: AuthorityRef,
    repository_ref: ExactRef,
    publication_bundle_ref: ExactRef,
    index_manifest_ref: ExactRef,
    objective_world_scope_ref: ExactRef,
    valid_time_authority_ref: AuthorityRef,
    world_validity_ref: ExactRef,
    predecessor_world_root_ref: ExactRef | None,
) -> dict[str, Any]:
    return {
        "schema": WORLD_ROOT_SCHEMA,
        "release_authority_ref": _authority_dict(release_authority_ref),
        "repository_ref": repository_ref.as_dict(),
        "publication_bundle_ref": publication_bundle_ref.as_dict(),
        "index_manifest_ref": index_manifest_ref.as_dict(),
        "objective_world_scope_ref": objective_world_scope_ref.as_dict(),
        "valid_time_authority_ref": _authority_dict(valid_time_authority_ref),
        "world_validity_ref": world_validity_ref.as_dict(),
        "predecessor_world_root_ref": (
            predecessor_world_root_ref.as_dict()
            if predecessor_world_root_ref is not None
            else None
        ),
    }


def build_objective_world_release_root(
    *,
    release_authority_ref: AuthorityRef,
    repository: V558RepositoryBundle,
    publication_bundle_ref: ExactRef,
    index_manifest_ref: ExactRef,
    objective_world_scope_ref: ExactRef,
    valid_time_authority_ref: AuthorityRef,
    world_validity_ref: ExactRef,
    predecessor_world_root_ref: ExactRef | None = None,
) -> ObjectiveWorldReleaseRoot:
    """Build the adopted objective-world root from exact existing authorities.

    This function deliberately has no actor, V3, cursor, timestamp, "latest",
    resolver, or wall-clock input. A caller must already possess the exact
    objective scope and objective world-validity instance.
    """
    if not isinstance(repository, V558RepositoryBundle):
        raise ObjectiveWorldRootError("repository must be exact V558RepositoryBundle")
    try:
        _validate_repository_checksum(repository)
    except M4IntegrityError as exc:
        raise ObjectiveWorldRootError("repository checksum/integrity validation failed") from exc

    if not isinstance(publication_bundle_ref, ExactRef):
        raise ObjectiveWorldRootError("publication_bundle_ref must be exact M4 ExactRef")
    if publication_bundle_ref != repository.publication_bundle_ref:
        raise ObjectiveWorldRootError(
            "publication_bundle_ref must equal repository.publication_bundle_ref"
        )

    if not isinstance(index_manifest_ref, ExactRef):
        raise ObjectiveWorldRootError("index_manifest_ref must be exact M4 ExactRef")
    if index_manifest_ref != repository.index_manifest.ref:
        raise ObjectiveWorldRootError(
            "index_manifest_ref must equal repository.index_manifest.ref"
        )

    scope = _exact_ref(
        objective_world_scope_ref,
        expected_kind=OBJECTIVE_WORLD_SCOPE_REF_KIND,
        field="objective_world_scope_ref",
    )
    validity = _exact_ref(
        world_validity_ref,
        expected_kind=OBJECTIVE_WORLD_VALIDITY_REF_KIND,
        field="world_validity_ref",
    )
    predecessor = _predecessor_ref(predecessor_world_root_ref)
    _authority_dict(release_authority_ref)
    _authority_dict(valid_time_authority_ref)

    material = _constructor_material(
        release_authority_ref=release_authority_ref,
        repository_ref=repository.ref,
        publication_bundle_ref=publication_bundle_ref,
        index_manifest_ref=index_manifest_ref,
        objective_world_scope_ref=scope,
        valid_time_authority_ref=valid_time_authority_ref,
        world_validity_ref=validity,
        predecessor_world_root_ref=predecessor,
    )
    root_hash = semantic_hash(material)
    root = ObjectiveWorldReleaseRoot(
        schema=WORLD_ROOT_SCHEMA,
        release_authority_ref=release_authority_ref,
        repository_ref=repository.ref,
        publication_bundle_ref=publication_bundle_ref,
        index_manifest_ref=index_manifest_ref,
        objective_world_scope_ref=scope,
        valid_time_authority_ref=valid_time_authority_ref,
        world_validity_ref=validity,
        predecessor_world_root_ref=predecessor,
        root_id=f"PREV3WORLD:{root_hash}",
        root_hash=root_hash,
    )
    if semantic_hash(root.canonical_material()) != root.root_hash:
        raise ObjectiveWorldRootError("world-root canonical identity replay mismatch")
    return root


def replay_objective_world_release_root(
    root: ObjectiveWorldReleaseRoot,
    *,
    repository: V558RepositoryBundle,
) -> ObjectiveWorldReleaseRoot:
    """Rebuild an immutable root and require exact same-tuple identity."""
    if not isinstance(root, ObjectiveWorldReleaseRoot):
        raise ObjectiveWorldRootError("replay requires ObjectiveWorldReleaseRoot")
    replayed = build_objective_world_release_root(
        release_authority_ref=root.release_authority_ref,
        repository=repository,
        publication_bundle_ref=root.publication_bundle_ref,
        index_manifest_ref=root.index_manifest_ref,
        objective_world_scope_ref=root.objective_world_scope_ref,
        valid_time_authority_ref=root.valid_time_authority_ref,
        world_validity_ref=root.world_validity_ref,
        predecessor_world_root_ref=root.predecessor_world_root_ref,
    )
    if replayed.ref != root.ref:
        raise ObjectiveWorldRootError("same-tuple world-root replay identity mismatch")
    return replayed


__all__ = [
    "WORLD_ROOT_SCHEMA",
    "WORLD_ROOT_REF_KIND",
    "OBJECTIVE_WORLD_SCOPE_REF_KIND",
    "OBJECTIVE_WORLD_VALIDITY_REF_KIND",
    "ObjectiveWorldRootError",
    "ObjectiveWorldReleaseRoot",
    "build_objective_world_release_root",
    "replay_objective_world_release_root",
]
