"""Carrier-neutral C11 reconstruction facade for PRE553 R5 shadow.

Accepted C11 constructors remain the semantic/integrity boundary.  This module
stores constructor material exactly and reconstructs through those accepted
classes; it does not define a second semantic object family.
"""
from __future__ import annotations

from dataclasses import fields, is_dataclass
from typing import Any, Callable, Iterable, Mapping

from rawlsing_next.pre553_r5_codec import R5TypedValueCodec
from rawlsing_next.pre553_r5_model import R5CanonicalRow, R5Error, R5IntegrityError


C11_ADAPTER_VERSION = "PRE553_R5_C11_FACADE@1.0.0"

PUBLIC_RELATIONS = {
    "EmpiricalUniverse": "empirical_universes",
    "RespondentEvent": "respondent_events",
    "RoutingEligibilityFact": "routing_eligibility",
    "EmpiricalCoordinateFact": "empirical_coordinates",
    "AuthoritySnapshot": "authority_snapshots",
    "SourceUniverseRelation": "source_universe_relations",
    "WeightMeasureFact": "weight_measure",
}
INTERNAL_RELATIONS = {
    "RespondentIdentity": "respondent_identities",
    "QuestionVariableBinding": "question_variable_bindings",
    "ReplayManifest": "replay_manifest",
}


def relation_for_object(obj: Any) -> str:
    family = getattr(obj, "FAMILY", None)
    if isinstance(family, str):
        name = family.split("@", 1)[0]
        relation = PUBLIC_RELATIONS.get(name)
        if relation is None:
            raise R5Error(f"unsupported public C11 family {family}")
        return relation
    family = getattr(obj, "RECORD_FAMILY", None)
    if isinstance(family, str):
        return INTERNAL_RELATIONS.get(family, "replay_bindings")
    raise R5Error(f"unsupported C11 object type {type(obj).__name__}")


def _special_pack(value: Any) -> Any:
    if hasattr(value, "kind") and hasattr(value, "object_id") and hasattr(value, "content_hash"):
        return {"__r5_c11_type__": "ExactRef", "kind": value.kind,
                "object_id": value.object_id, "content_hash": value.content_hash}
    if hasattr(value, "authority_id") and hasattr(value, "authority_version") and hasattr(value, "authority_content_hash"):
        return {"__r5_c11_type__": "AuthorityRef", "authority_id": value.authority_id,
                "authority_version": value.authority_version,
                "authority_content_hash": value.authority_content_hash}
    # TypedAbsence is an internal record-like value, not a semantic object.
    if type(value).__name__ == "TypedAbsence" and hasattr(value, "state"):
        return {"__r5_c11_type__": "TypedAbsence", "state": value.state,
                "detail": getattr(value, "detail", None)}
    if isinstance(value, Mapping):
        return {_special_pack(k): _special_pack(v) for k, v in value.items()}
    if isinstance(value, tuple):
        return tuple(_special_pack(v) for v in value)
    if isinstance(value, list):
        return [_special_pack(v) for v in value]
    return value


def _special_unpack(value: Any, resolver: Callable[[str], type]) -> Any:
    if isinstance(value, Mapping) and value.get("__r5_c11_type__") == "ExactRef":
        cls = resolver("ExactRef")
        return cls(value["kind"], value["object_id"], value["content_hash"])
    if isinstance(value, Mapping) and value.get("__r5_c11_type__") == "AuthorityRef":
        cls = resolver("AuthorityRef")
        return cls(value["authority_id"], value["authority_version"], value["authority_content_hash"])
    if isinstance(value, Mapping) and value.get("__r5_c11_type__") == "TypedAbsence":
        cls = resolver("TypedAbsence")
        return cls(value["state"], value.get("detail"))
    if isinstance(value, Mapping):
        return {_special_unpack(k, resolver): _special_unpack(v, resolver) for k, v in value.items()}
    if isinstance(value, tuple):
        return tuple(_special_unpack(v, resolver) for v in value)
    if isinstance(value, list):
        return [_special_unpack(v, resolver) for v in value]
    return value


def default_class_resolver(name: str) -> type:
    from rawlsing_next import pre553_empirical_objects as objects
    from rawlsing_next import pre553_c11_integrity as integrity
    cls = getattr(objects, name, None) or getattr(integrity, name, None)
    if cls is None:
        raise R5IntegrityError(f"unknown accepted C11 class {name}")
    return cls


def object_to_canonical_row(obj: Any, *, codec: R5TypedValueCodec | None = None) -> R5CanonicalRow:
    codec = codec or R5TypedValueCodec()
    public_family = getattr(obj, "FAMILY", None)
    internal_family = getattr(obj, "RECORD_FAMILY", None)
    if isinstance(public_family, str):
        family = public_family
        kwargs = {
            "typed_state": obj.typed_state,
            "authority_snapshot_refs": obj.authority_snapshot_refs,
            "dependency_refs": obj.dependency_refs,
            "producer_replay_locator_or_reference_root": obj.producer_replay_locator_or_reference_root,
            **dict(obj.semantic_fields),
        }
        kind = "public"
    elif isinstance(internal_family, str) and is_dataclass(obj):
        family = internal_family
        kwargs = {field.name: getattr(obj, field.name) for field in fields(obj)}
        kind = "internal"
    else:
        raise R5Error(f"unsupported C11 object {type(obj).__name__}")
    packed = _special_pack(kwargs)
    return R5CanonicalRow(
        relation=relation_for_object(obj), object_family=family,
        object_id=obj.object_id, content_hash=obj.content_hash,
        payload={"adapter_version": C11_ADAPTER_VERSION, "kind": kind, "kwargs": codec.encode(packed)},
    )


def canonical_row_to_object(row: R5CanonicalRow, *, codec: R5TypedValueCodec | None = None,
                            class_resolver: Callable[[str], type] = default_class_resolver) -> Any:
    codec = codec or R5TypedValueCodec()
    if row.payload.get("adapter_version") != C11_ADAPTER_VERSION:
        raise R5IntegrityError("C11 adapter version mismatch")
    family_name = row.object_family.split("@", 1)[0]
    cls = class_resolver(family_name)
    decoded = codec.decode(row.payload["kwargs"])
    kwargs = _special_unpack(decoded, class_resolver)
    try:
        obj = cls(**kwargs)
    except Exception as exc:
        raise R5IntegrityError(f"accepted C11 constructor rejected reconstructed {row.object_family}") from exc
    if getattr(obj, "object_id", None) != row.object_id or getattr(obj, "content_hash", None) != row.content_hash:
        raise R5IntegrityError(f"reconstructed C11 identity mismatch for {row.object_family}")
    return obj


def iter_release_rows(release: Any, *, codec: R5TypedValueCodec | None = None) -> Iterable[R5CanonicalRow]:
    """Bounded-court/reference convenience; full-source R5 need not materialize a release first."""
    codec = codec or R5TypedValueCodec()
    for obj in getattr(release, "public_objects", ()):
        yield object_to_canonical_row(obj, codec=codec)
    for obj in getattr(release, "internal_records", ()):
        yield object_to_canonical_row(obj, codec=codec)
    replay = getattr(release, "replay_manifest", None)
    if replay is not None:
        yield object_to_canonical_row(replay, codec=codec)


class R5C11Facade:
    """Lazy carrier-neutral logical facade over an R5 reader.

    Full-source correctness paths remain streaming.  Materializing a frozen
    C11Repository is explicitly bounded and exists only for bounded G7 courts
    because frozen I03 currently requires that accepted repository type.
    """

    def __init__(self, reader: Any, *, codec: R5TypedValueCodec | None = None,
                 class_resolver: Callable[[str], type] = default_class_resolver) -> None:
        self.reader = reader
        self.codec = codec or R5TypedValueCodec()
        self.class_resolver = class_resolver

    def iter_objects(self, *, relation: str | None = None) -> Iterable[Any]:
        c11_relations = set(PUBLIC_RELATIONS.values()) | set(INTERNAL_RELATIONS.values()) | {"replay_bindings"}
        for row in self.reader.iter_rows(relation=relation):
            if row.relation not in c11_relations:
                continue
            yield canonical_row_to_object(row, codec=self.codec, class_resolver=self.class_resolver)

    def resolve_exact(self, relation: str, object_id: str) -> Any:
        row = self.reader.resolve_exact(relation, object_id)
        if row is None:
            raise KeyError("exact C11 object unavailable; no fallback permitted")
        return canonical_row_to_object(row, codec=self.codec, class_resolver=self.class_resolver)

    def materialize_bounded_release(self, *, max_objects: int) -> Any:
        if not isinstance(max_objects, int) or isinstance(max_objects, bool) or max_objects < 1:
            raise R5Error("max_objects must be positive")
        public, internal, replay = [], [], []
        count = 0
        for obj in self.iter_objects():
            count += 1
            if count > max_objects:
                raise R5Error("bounded C11 materialization limit exceeded")
            if getattr(obj, "RECORD_FAMILY", None) == "ReplayManifest":
                replay.append(obj)
            elif getattr(obj, "FAMILY", None) is not None:
                public.append(obj)
            else:
                internal.append(obj)
        if len(replay) != 1:
            raise R5IntegrityError("R5 C11 reconstruction requires exactly one ReplayManifest")
        identity = self.reader.release_identity
        from rawlsing_next.pre553_c11_repository import _make_validated_release
        return _make_validated_release(
            release_id=identity["release_id"],
            source_artifact_ref=self.class_resolver("ExactRef")(
                identity["source_artifact_ref"]["kind"],
                identity["source_artifact_ref"]["object_id"],
                identity["source_artifact_ref"]["content_hash"],
            ),
            source_release_manifest_hash=identity["source_release_manifest_hash"],
            semantic_release_hash=identity["semantic_release_hash"],
            replay_manifest=replay[0],
            public_objects=tuple(sorted(public, key=lambda x: x.ref.key)),
            internal_records=tuple(sorted(internal, key=lambda x: x.ref.key)),
            m01_m18_coverage={k: tuple(v) for k, v in identity["m01_m18_coverage"].items()},
        )

    def materialize_bounded_repository(self, *, max_objects: int) -> Any:
        from rawlsing_next.pre553_c11_repository import C11Repository
        return C11Repository((self.materialize_bounded_release(max_objects=max_objects),))


__all__ = [
    "C11_ADAPTER_VERSION", "PUBLIC_RELATIONS", "INTERNAL_RELATIONS", "relation_for_object",
    "object_to_canonical_row", "canonical_row_to_object", "iter_release_rows", "R5C11Facade",
]
