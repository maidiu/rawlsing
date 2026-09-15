"""Constructor-complete repo-native transport for ordinary PRE553 query/fact objects.

Transport only: no empirical execution, source/Library/filesystem reads, authority
minting, or PRE553 semantic/hash-law changes.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from typing import Any, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, EmpiricalFact, EmpiricalQuerySpec, ExactRef, Pre553IntegrityError,
    authority_ref, canonical_json, exact_ref, semantic_hash,
)

SEAL_FORMAT = "PRE553_REPO_NATIVE_QUERY_FACT_SEAL"
SEAL_VERSION = "1.0.0"
DOCUMENT_SCHEMA = "PRE553_QUERY_FACT_CONSTRUCTOR_DOCUMENT@1.0.0"
DEFAULT_SHARD_CHAR_LIMIT = 16_384
_OBJECT_KEYS = frozenset({
    "schema_id", "schema_version", "typed_state", "authority_snapshot_refs",
    "dependency_refs", "producer_replay_locator_or_reference_root", "semantic_fields",
    "object_id", "content_hash",
})


class RepoNativeSealError(Pre553IntegrityError):
    pass


class RealGT2PayloadPendingError(RepoNativeSealError):
    pass


@dataclass(frozen=True)
class RepoNativeSealPayload:
    manifest_json: str
    shards: tuple[str, ...]
    manifest_sha256: str

    def __post_init__(self) -> None:
        if not isinstance(self.manifest_json, str) or not self.manifest_json:
            raise RepoNativeSealError("manifest_json must be non-empty text")
        if not isinstance(self.shards, tuple) or any(not isinstance(x, str) for x in self.shards):
            raise RepoNativeSealError("shards must be an exact tuple of text shards")
        _sha(self.manifest_sha256, "manifest_sha256")


def _sha(value: Any, name: str) -> str:
    if (not isinstance(value, str) or len(value) != 64 or value.lower() != value
            or any(ch not in "0123456789abcdef" for ch in value)):
        raise RepoNativeSealError(f"{name} must be a lowercase sha256")
    return value


def _text_hash(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _mapping(value: Any, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise RepoNativeSealError(f"{name} must be a mapping")
    return value


def _list(value: Any, name: str) -> list[Any]:
    if not isinstance(value, list):
        raise RepoNativeSealError(f"{name} must be a canonical JSON array")
    return value


def _exact_refs(value: Any, name: str, *, canonical_order: bool = True) -> tuple[ExactRef, ...]:
    refs = tuple(exact_ref(x, name) for x in _list(value, name))
    if len(refs) != len(set(refs)):
        raise RepoNativeSealError(f"{name} contains duplicate exact refs")
    if canonical_order and refs != tuple(sorted(refs, key=lambda r: r.key)):
        raise RepoNativeSealError(f"{name} order drift")
    return refs


def _authority_refs(value: Any, name: str) -> tuple[AuthorityRef, ...]:
    refs = tuple(authority_ref(x, name) for x in _list(value, name))
    if len(refs) != len(set(refs)):
        raise RepoNativeSealError(f"{name} contains duplicate authority refs")
    if refs != tuple(sorted(refs, key=lambda r: r.key)):
        raise RepoNativeSealError(f"{name} order drift")
    return refs


def _set_like(value: Any, name: str) -> None:
    keys = [canonical_json(x) for x in _list(value, name)]
    if len(keys) != len(set(keys)):
        raise RepoNativeSealError(f"{name} contains duplicate canonical members")
    if keys != sorted(keys):
        raise RepoNativeSealError(f"{name} order drift")


def _strict_object(raw: Any, role: str, cls: type[EmpiricalQuerySpec] | type[EmpiricalFact]) -> Mapping[str, Any]:
    obj = _mapping(raw, role)
    if set(obj) != _OBJECT_KEYS:
        raise RepoNativeSealError(f"{role} constructor material key-set drift")
    family, version = cls.FAMILY.split("@", 1)
    if obj["schema_id"] != family or obj["schema_version"] != version:
        raise RepoNativeSealError(f"{role} schema family/version drift")
    _sha(obj["content_hash"], f"{role}.content_hash")
    if not isinstance(obj["object_id"], str) or not obj["object_id"]:
        raise RepoNativeSealError(f"{role}.object_id must be non-empty text")
    _authority_refs(obj["authority_snapshot_refs"], f"{role}.authority_snapshot_refs")
    _exact_refs(obj["dependency_refs"], f"{role}.dependency_refs")
    fields = _mapping(obj["semantic_fields"], f"{role}.semantic_fields")
    for field in cls.SET_LIKE_FIELDS:
        if field in fields:
            _set_like(fields[field], f"{role}.semantic_fields.{field}")
    if role == "fact":
        risk, denom = fields.get("risk_set_member_refs"), fields.get("denominator_member_refs")
        if (risk is None) != (denom is None):
            raise RepoNativeSealError("fact risk and denominator member refs must travel together")
        if risk is not None:
            _exact_refs(risk, "fact.risk_set_member_refs")
            _exact_refs(denom, "fact.denominator_member_refs")
    return obj


def _construct(raw: Mapping[str, Any], role: str, cls):
    try:
        return cls(
            typed_state=raw["typed_state"],
            authority_snapshot_refs=raw["authority_snapshot_refs"],
            dependency_refs=raw["dependency_refs"],
            producer_replay_locator_or_reference_root=raw["producer_replay_locator_or_reference_root"],
            object_id=raw["object_id"], content_hash=raw["content_hash"],
            schema_id=raw["schema_id"], schema_version=raw["schema_version"],
            **dict(_mapping(raw["semantic_fields"], f"{role}.semantic_fields")),
        )
    except (Pre553IntegrityError, TypeError, ValueError) as exc:
        raise RepoNativeSealError(f"{role} existing constructor rejected sealed material: {exc}") from exc


def _refs(value: Any, name: str) -> tuple[ExactRef, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise RepoNativeSealError(f"{name} must be an exact ref sequence")
    return tuple(exact_ref(x, name) for x in value)


def _auths(value: Any, name: str) -> tuple[AuthorityRef, ...]:
    if isinstance(value, (str, bytes, bytearray)) or not isinstance(value, Sequence):
        raise RepoNativeSealError(f"{name} must be an authority ref sequence")
    return tuple(authority_ref(x, name) for x in value)


def _cross_check(query: EmpiricalQuerySpec, fact: EmpiricalFact) -> None:
    if not isinstance(query, EmpiricalQuerySpec) or not isinstance(fact, EmpiricalFact):
        raise RepoNativeSealError("rehydration must yield ordinary PRE553 query/fact objects")
    pairs = (
        (fact.condition_predicate_ref, query.condition_predicate_ref, "condition predicate"),
        (fact.risk_set_ref, query.risk_set_ref, "risk set"),
        (fact.measure_basis_ref, query.measure_basis_ref, "measure basis"),
    )
    if exact_ref(fact.empirical_query_spec_ref, "fact.query") != query.ref:
        raise RepoNativeSealError("fact query identity drift")
    for left, right, label in pairs:
        if exact_ref(left, f"fact.{label}") != exact_ref(right, f"query.{label}"):
            raise RepoNativeSealError(f"query/fact {label} drift")
    qu = set(_refs(query.empirical_universe_refs, "query.universes"))
    fu = set(_refs(fact.empirical_universe_refs, "fact.universes"))
    if not fu or not fu.issubset(qu):
        raise RepoNativeSealError("fact empirical-universe provenance escapes query source scope")
    fact_auth = set(fact.authority_snapshot_refs)
    if not set(query.authority_snapshot_refs).issubset(fact_auth):
        raise RepoNativeSealError("fact authority closure dropped query snapshot authority")
    if not set(_auths(query.query_authority_refs, "query.query_authority_refs")).issubset(fact_auth):
        raise RepoNativeSealError("fact authority closure dropped query semantic authority")
    replay = exact_ref(fact.replay_ref, "fact.replay_ref")
    if fact.producer_replay_locator_or_reference_root != replay:
        raise RepoNativeSealError("fact replay root drift")
    provenance = set(_refs(fact.source_empirical_provenance_refs, "fact.provenance"))
    predicate = exact_ref(fact.condition_predicate_ref, "fact.condition_predicate_ref")
    if not {query.ref, replay, predicate, *provenance}.issubset(set(fact.dependency_refs)):
        raise RepoNativeSealError("fact dependency closure dropped query/replay/predicate/provenance")
    risk = fact.semantic_fields.get("risk_set_member_refs")
    denom = fact.semantic_fields.get("denominator_member_refs")
    if risk is not None or denom is not None:
        if risk is None or denom is None:
            raise RepoNativeSealError("risk/denominator member transport is incomplete")
        rrefs, drefs = _refs(risk, "fact.risk_members"), _refs(denom, "fact.denominator_members")
        if len(rrefs) != len(set(rrefs)) or len(drefs) != len(set(drefs)):
            raise RepoNativeSealError("risk/denominator members must be unique")
        if not set(drefs).issubset(set(rrefs)):
            raise RepoNativeSealError("denominator members are not an exact subset of risk-set members")
        if fact.raw_denominator_support != len(drefs):
            raise RepoNativeSealError("raw denominator count does not equal denominator member count")


def _sequences(document: Mapping[str, Any]) -> dict[str, list[Any]]:
    q, f = _mapping(document["query"], "query"), _mapping(document["fact"], "fact")
    qf, ff = _mapping(q["semantic_fields"], "query.fields"), _mapping(f["semantic_fields"], "fact.fields")
    out = {
        "query.authority_snapshot_refs": _list(q["authority_snapshot_refs"], "query.authority_snapshot_refs"),
        "query.dependency_refs": _list(q["dependency_refs"], "query.dependency_refs"),
        "query.empirical_universe_refs": _list(qf["empirical_universe_refs"], "query.empirical_universe_refs"),
        "query.scope_refs": _list(qf["scope_refs"], "query.scope_refs"),
        "query.query_authority_refs": _list(qf["query_authority_refs"], "query.query_authority_refs"),
        "fact.authority_snapshot_refs": _list(f["authority_snapshot_refs"], "fact.authority_snapshot_refs"),
        "fact.dependency_refs": _list(f["dependency_refs"], "fact.dependency_refs"),
        "fact.empirical_universe_refs": _list(ff["empirical_universe_refs"], "fact.empirical_universe_refs"),
        "fact.source_empirical_provenance_refs": _list(ff["source_empirical_provenance_refs"], "fact.provenance"),
    }
    if "risk_set_member_refs" in ff or "denominator_member_refs" in ff:
        out["fact.risk_set_member_refs"] = _list(ff.get("risk_set_member_refs"), "fact.risk_members")
        out["fact.denominator_member_refs"] = _list(ff.get("denominator_member_refs"), "fact.denominator_members")
    return out


def _commitments(document: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    return {role: {"count": len(items), "sha256": semantic_hash({"role": role, "items": items})}
            for role, items in sorted(_sequences(document).items())}


def _identities(document: Mapping[str, Any]) -> dict[str, Any]:
    q, f = _mapping(document["query"], "query"), _mapping(document["fact"], "fact")
    ff = _mapping(f["semantic_fields"], "fact.fields")
    return {
        "query_ref": ExactRef(EmpiricalQuerySpec.FAMILY, q["object_id"], q["content_hash"]).as_dict(),
        "fact_ref": ExactRef(EmpiricalFact.FAMILY, f["object_id"], f["content_hash"]).as_dict(),
        "replay_ref": exact_ref(ff["replay_ref"], "fact.replay_ref").as_dict(),
    }


def _seal_document(document: Mapping[str, Any], *, shard_char_limit: int) -> RepoNativeSealPayload:
    if not isinstance(shard_char_limit, int) or isinstance(shard_char_limit, bool) or shard_char_limit < 1:
        raise RepoNativeSealError("shard_char_limit must be a positive integer")
    text = canonical_json(document)
    document = json.loads(text)
    if set(document) != {"document_schema", "query", "fact"} or document["document_schema"] != DOCUMENT_SCHEMA:
        raise RepoNativeSealError("constructor document schema drift")
    shards = tuple(text[i:i + shard_char_limit] for i in range(0, len(text), shard_char_limit))
    descriptors = [{"index": i, "char_count": len(s), "byte_count": len(s.encode("utf-8")), "sha256": _text_hash(s)}
                   for i, s in enumerate(shards)]
    manifest = {
        "format": SEAL_FORMAT, "version": SEAL_VERSION, "document_schema": DOCUMENT_SCHEMA,
        "encoding": "utf-8", "object_roles": ["query", "fact"], "object_count": 2,
        "shard_count": len(shards), "document_char_count": len(text),
        "document_byte_count": len(text.encode("utf-8")), "document_sha256": _text_hash(text),
        "identities": _identities(document), "sequence_commitments": _commitments(document),
        "shards": descriptors,
    }
    manifest_json = canonical_json(manifest)
    return RepoNativeSealPayload(manifest_json, shards, _text_hash(manifest_json))


def seal_query_fact(query: EmpiricalQuerySpec, fact: EmpiricalFact, *, shard_char_limit: int = DEFAULT_SHARD_CHAR_LIMIT) -> RepoNativeSealPayload:
    """Generic build helper; accepts no authority/path/identity overrides."""
    _cross_check(query, fact)
    return _seal_document({"document_schema": DOCUMENT_SCHEMA, "query": query.as_dict(), "fact": fact.as_dict()},
                          shard_char_limit=shard_char_limit)


def rehydrate_repo_native_query_fact(payload: RepoNativeSealPayload) -> tuple[EmpiricalQuerySpec, EmpiricalFact]:
    """Verify the full seal and return ordinary existing PRE553 objects."""
    if not isinstance(payload, RepoNativeSealPayload):
        raise RepoNativeSealError("transport carrier required; it is not an EmpiricalFact substitute")
    if _text_hash(payload.manifest_json) != payload.manifest_sha256:
        raise RepoNativeSealError("manifest content hash mismatch")
    try:
        manifest = json.loads(payload.manifest_json)
    except json.JSONDecodeError as exc:
        raise RepoNativeSealError("manifest is not JSON") from exc
    if canonical_json(manifest) != payload.manifest_json:
        raise RepoNativeSealError("manifest is not canonical JSON")
    keys = {"format", "version", "document_schema", "encoding", "object_roles", "object_count",
            "shard_count", "document_char_count", "document_byte_count", "document_sha256",
            "identities", "sequence_commitments", "shards"}
    if set(manifest) != keys or manifest["format"] != SEAL_FORMAT or manifest["version"] != SEAL_VERSION:
        raise RepoNativeSealError("manifest format/version/key-set drift")
    if manifest["document_schema"] != DOCUMENT_SCHEMA or manifest["encoding"] != "utf-8":
        raise RepoNativeSealError("manifest document schema/encoding drift")
    if manifest["object_roles"] != ["query", "fact"] or manifest["object_count"] != 2:
        raise RepoNativeSealError("manifest object role/count drift")
    descriptors = _list(manifest["shards"], "manifest.shards")
    if manifest["shard_count"] != len(descriptors) or len(payload.shards) != len(descriptors):
        raise RepoNativeSealError("missing or extra shard")
    for i, (raw, shard) in enumerate(zip(descriptors, payload.shards)):
        desc = _mapping(raw, f"manifest.shards[{i}]")
        if set(desc) != {"index", "char_count", "byte_count", "sha256"} or desc["index"] != i:
            raise RepoNativeSealError("shard descriptor/order drift")
        if desc["char_count"] != len(shard) or desc["byte_count"] != len(shard.encode("utf-8")):
            raise RepoNativeSealError("shard character count mismatch")
        if desc["sha256"] != _text_hash(shard):
            raise RepoNativeSealError("shard content hash mismatch")
    text = "".join(payload.shards)
    if (manifest["document_char_count"] != len(text)
            or manifest["document_byte_count"] != len(text.encode("utf-8"))
            or manifest["document_sha256"] != _text_hash(text)):
        raise RepoNativeSealError("constructor document count/hash mismatch")
    try:
        document = json.loads(text)
    except json.JSONDecodeError as exc:
        raise RepoNativeSealError("constructor document is not JSON") from exc
    if canonical_json(document) != text or set(document) != {"document_schema", "query", "fact"}:
        raise RepoNativeSealError("constructor document shape/canonicalization drift")
    if document["document_schema"] != DOCUMENT_SCHEMA:
        raise RepoNativeSealError("constructor document schema drift")
    qraw = _strict_object(document["query"], "query", EmpiricalQuerySpec)
    fraw = _strict_object(document["fact"], "fact", EmpiricalFact)
    if _identities(document) != manifest["identities"] or _commitments(document) != manifest["sequence_commitments"]:
        raise RepoNativeSealError("sequence count/order commitment drift")
    query = _construct(qraw, "query", EmpiricalQuerySpec)
    fact = _construct(fraw, "fact", EmpiricalFact)
    ids = _mapping(manifest["identities"], "manifest.identities")
    if query.ref != exact_ref(ids["query_ref"], "manifest.query_ref"):
        raise RepoNativeSealError("rehydrated query identity mismatch")
    if fact.ref != exact_ref(ids["fact_ref"], "manifest.fact_ref"):
        raise RepoNativeSealError("rehydrated fact identity mismatch")
    if exact_ref(fact.replay_ref, "fact.replay_ref") != exact_ref(ids["replay_ref"], "manifest.replay_ref"):
        raise RepoNativeSealError("rehydrated replay identity mismatch")
    _cross_check(query, fact)
    return query, fact


def load_current_gt2_query_fact() -> tuple[EmpiricalQuerySpec, EmpiricalFact]:
    """No-argument frozen current entrypoint over the committed Worker-A repo transport."""
    from rawlsing_next.pre553_repo_native_current_payload import (
        load_current_gt2_query_fact_from_committed_transport,
    )
    return load_current_gt2_query_fact_from_committed_transport()


__all__ = [
    "SEAL_FORMAT", "SEAL_VERSION", "DOCUMENT_SCHEMA", "DEFAULT_SHARD_CHAR_LIMIT",
    "RepoNativeSealError", "RealGT2PayloadPendingError", "RepoNativeSealPayload",
    "seal_query_fact", "rehydrate_repo_native_query_fact", "load_current_gt2_query_fact",
]
