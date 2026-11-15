"""Exact FIABC-style canonical preimage fragment factoring.

This module adapts the sourcefree canonical-preimage fragment map implemented in
``rawlsing_next.fiabc_final_oracle_freeze_producers`` at
``8e35e9b0d41c6a404a84ea511761d5123323af35``.  It deliberately copies only the
three sourcefree primitives:

* ``_store_lits_preimage_fragment``
* ``_pack_lits_canonical_preimage``
* ``_hydrate_lits_canonical_preimage``

No LiTS artifact, respondent row, original source byte, authority snapshot
issuance, or scientific product is loaded here.  A fragment is identified by
``semantic_hash(canonicalize(value))`` and verified again on every read.

The fragment map is a pure lossless compression seam: hydration reconstructs the
exact canonical preimage, and the caller re-materializes the public object under
its own constructor identity law.  A missing, substituted, or hash-drifted
fragment must fail closed.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.pre553_empirical_objects import (
    canonicalize,
    semantic_hash,
)

FRAGMENT_SCHEMA = "PYAT_S2F_CANONICAL_PREIMAGE_FRAGMENT@1.0.0"
FRAGMENT_MARKER = "$canonical_preimage_fragment"

# The only document paths this adapter factors.  They are the exact FIABC LiTS
# paths: complete risk/denominator member refs and the complete target-cell
# semantic projection.  Adding arbitrary paths would change the accepted
# fragment contract and is intentionally not done here.
TRANSFORMED_SCHEMA_ID = "EmpiricalFact"


class DurableFragmentError(ValueError):
    """A canonical preimage fragment is absent, malformed, or hash-drifted."""


def fragment_identity(value: Any) -> str:
    """Return the exact content identity of one canonical fragment."""

    return semantic_hash(canonicalize(value))


def store_fragment(value: Any, fragments: dict[str, Any]) -> Mapping[str, str]:
    """Store one fragment exactly once and return its reference marker.

    Mirrors FIABC's ``_store_lits_preimage_fragment`` including the conflicting
    preimage check for one hash.
    """

    material = canonicalize(value)
    digest = semantic_hash(material)
    previous = fragments.setdefault(digest, material)
    if canonicalize(previous) != material:
        raise DurableFragmentError("canonical preimage fragment hash collision")
    return {FRAGMENT_MARKER: digest}


def pack_canonical_preimage(
    document: Mapping[str, Any],
    fragments: dict[str, Any],
) -> Mapping[str, Any]:
    """Losslessly deduplicate large identity-bearing fact fragments.

    Mirrors FIABC's ``_pack_lits_canonical_preimage`` exactly: only
    ``EmpiricalFact`` documents are transformed, and only the three declared
    fields are replaced by content-addressed fragment references.
    """

    packed = canonicalize(document)
    if packed.get("schema_id") != TRANSFORMED_SCHEMA_ID:
        return packed
    fields = dict(packed["semantic_fields"])
    for name in ("risk_set_member_refs", "denominator_member_refs"):
        if name in fields:
            fields[name] = store_fragment(fields[name], fragments)
    topology = fields.get("target_topology")
    if (
        isinstance(topology, Mapping)
        and "complete_cell_semantic_projection" in topology
    ):
        topology = dict(topology)
        topology["complete_cell_semantic_projection"] = store_fragment(
            topology["complete_cell_semantic_projection"],
            fragments,
        )
        fields["target_topology"] = topology
    packed = dict(packed)
    packed["semantic_fields"] = fields
    return canonicalize(packed)


def hydrate_canonical_preimage(
    value: Any,
    fragments: Mapping[str, Any],
) -> Any:
    """Reconstruct one exact preimage from the fragment map.

    Mirrors FIABC's ``_hydrate_lits_canonical_preimage`` and fails closed on a
    missing fragment reference.
    """

    if isinstance(value, Mapping):
        if set(value) == {FRAGMENT_MARKER}:
            digest = value.get(FRAGMENT_MARKER)
            if not isinstance(digest, str) or digest not in fragments:
                raise DurableFragmentError(
                    "canonical preimage references a missing fragment"
                )
            return canonicalize(fragments[digest])
        return {
            key: hydrate_canonical_preimage(item, fragments)
            for key, item in value.items()
        }
    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        return [hydrate_canonical_preimage(item, fragments) for item in value]
    return value


def fragment_entries(
    fragments: Mapping[str, Any],
    *,
    compressed_bytes: Mapping[str, int] | None = None,
    blob_names: Mapping[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Return canonical, hash-sorted fragment entries with exact byte counts."""

    compressed_bytes = compressed_bytes or {}
    blob_names = blob_names or {}
    entries: list[dict[str, Any]] = []
    for digest in sorted(fragments):
        material = canonicalize(fragments[digest])
        if semantic_hash(material) != digest:
            raise DurableFragmentError("fragment map contains hash-drifted content")
        entry: dict[str, Any] = {
            "schema": FRAGMENT_SCHEMA,
            "fragment_hash": digest,
            "uncompressed_bytes": len(_canonical_bytes(material)),
            "value": material,
        }
        if digest in compressed_bytes:
            entry["compressed_bytes"] = int(compressed_bytes[digest])
        if digest in blob_names:
            entry["blob"] = blob_names[digest]
        entries.append(entry)
    return entries


def fragment_map_from_entries(
    entries: Iterable[Mapping[str, Any]],
) -> dict[str, Any]:
    """Validate and rebuild a fragment map from persisted entries.

    Accepts both inline values (the FIABC-compatible form) and blob-backed
    entries whose value is loaded by the caller into ``value``.
    """

    fragments: dict[str, Any] = {}
    if isinstance(entries, (str, bytes, bytearray)) or not isinstance(
        entries, Iterable
    ):
        raise DurableFragmentError("fragment entries must be an iterable")
    for entry in entries:
        if not isinstance(entry, Mapping):
            raise DurableFragmentError("fragment entry must be a mapping")
        digest = entry.get("fragment_hash")
        if not isinstance(digest, str) or len(digest) != 64:
            raise DurableFragmentError("fragment entry hash is malformed")
        if "value" not in entry:
            raise DurableFragmentError("fragment entry value is unavailable")
        material = canonicalize(entry["value"])
        if semantic_hash(material) != digest:
            raise DurableFragmentError("fragment entry content hash drift")
        previous = fragments.setdefault(digest, material)
        if canonicalize(previous) != material:
            raise DurableFragmentError("fragment entry hash collision")
    return fragments


def _canonical_bytes(value: Any) -> bytes:
    from rawlsing_next.pre553_empirical_objects import canonical_json

    return canonical_json(value).encode("utf-8")


__all__ = [
    "FRAGMENT_SCHEMA",
    "FRAGMENT_MARKER",
    "TRANSFORMED_SCHEMA_ID",
    "DurableFragmentError",
    "fragment_identity",
    "store_fragment",
    "pack_canonical_preimage",
    "hydrate_canonical_preimage",
    "fragment_entries",
    "fragment_map_from_entries",
]
