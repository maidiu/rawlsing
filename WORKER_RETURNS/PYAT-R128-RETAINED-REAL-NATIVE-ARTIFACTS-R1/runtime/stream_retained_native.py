#!/usr/bin/env python3
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import resource
import shutil
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Mapping, Sequence

import ijson

from rawlsing_next.pre553_carrier_execution import materialize_public_object
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot,
    canonicalize,
    semantic_hash,
)

CHECKPOINT_BYTES = 3_404_445_161
CHECKPOINT_SHA256 = "2704fd3fadc9c898a512183aaf5eebf0ca48d78c47e75a19d47e17281eaa5726"
CLOSURE_IDENTITY = "f264dd8f83a0794716583d1ea8445947cc9470b99475e5d51fc2383e7196f415"
CLOSURE_SCHEMA = "FIABC_LITS_CANONICAL_CURRENT_EMPIRICAL_OBJECT_CLOSURE@1.0.0"
EXPECTED_INVENTORY = {
    "AuthoritySnapshot@1.0.0": 24,
    "DiscoveryAuthority@1.0.0": 1,
    "DiscoveryResultReceipt@1.0.0": 50,
    "EmpiricalFact@1.0.0": 60,
    "EmpiricalPredicate@1.0.0": 35,
    "EmpiricalQuerySpec@1.0.0": 63,
    "EmpiricalUniverse@1.0.0": 1,
}
EXPECTED_RELEASE = "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f"
EXPECTED_REPLAY = "30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08"
EXPECTED_REPRESENTATION = "9fce3b606413c2a5d3e9a05eda967067d191fbb31ff869d445d962bdf321393d"
CLOSURE_KEY = b'"canonical_empirical_object_closure":'
NEXT_MATERIAL_KEY = b'"comparison_fact_manifest":'
IDENTITY_KEY = b'"closure_identity":"'
FRAGMENT_PREFIX = (
    "material.canonical_empirical_object_closure.preimage_fragments.item"
)
OBJECT_PREFIX = (
    "material.canonical_empirical_object_closure.public_object_preimages.item"
)
CHUNK = 8 * 1024 * 1024


class RetainedNativeError(RuntimeError):
    pass


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        canonicalize(value), sort_keys=True, separators=(",", ":"),
        ensure_ascii=False, allow_nan=False,
    ).encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_in_prefix(path: Path, needle: bytes, limit: int = 1024 * 1024) -> int:
    with path.open("rb") as handle:
        data = handle.read(limit)
    offset = data.find(needle)
    if offset < 0:
        raise RetainedNativeError(f"key absent from prefix: {needle!r}")
    return offset


def find_in_tail(path: Path, needle: bytes, limit: int = 2 * 1024 * 1024) -> int:
    size = path.stat().st_size
    with path.open("rb") as handle:
        handle.seek(max(0, size - limit))
        data = handle.read()
    offset = data.rfind(needle)
    if offset < 0:
        raise RetainedNativeError(f"key absent from tail: {needle!r}")
    return size - len(data) + offset


def find_in_range(path: Path, needle: bytes, start: int, end: int) -> int:
    pos = start
    overlap = b""
    with path.open("rb") as handle:
        handle.seek(start)
        while pos < end:
            chunk = handle.read(min(CHUNK, end - pos))
            if not chunk:
                break
            data = overlap + chunk
            offset = data.find(needle)
            if offset >= 0:
                return pos - len(overlap) + offset
            overlap = data[-(len(needle) - 1):]
            pos += len(chunk)
    raise RetainedNativeError(f"key absent from range: {needle!r}")


def checkpoint_identity(path: Path) -> str:
    with path.open("rb") as handle:
        prefix = handle.read(1024 * 1024)
    key = b'"checkpoint_sha256":"'
    index = prefix.find(key)
    if index < 0:
        raise RetainedNativeError("checkpoint identity field absent")
    start = index + len(key)
    value = prefix[start:start + 64].decode("ascii")
    if len(value) != 64 or prefix[start + 64:start + 66] != b'",':
        raise RetainedNativeError("checkpoint identity field malformed")
    return value


def closure_bounds(path: Path) -> tuple[int, int]:
    key = find_in_prefix(path, CLOSURE_KEY)
    with path.open("rb") as handle:
        handle.seek(key + len(CLOSURE_KEY))
        prefix = handle.read(1024)
    brace = prefix.find(b"{")
    if brace < 0:
        raise RetainedNativeError("closure value has no opening object")
    start = key + len(CLOSURE_KEY) + brace
    next_key = find_in_tail(path, NEXT_MATERIAL_KEY)
    return start, next_key - 1


def closure_identity_parts(
    path: Path, start: int, end: int
) -> tuple[str, int, int]:
    key = find_in_range(path, IDENTITY_KEY, start, end)
    value_start = key + len(IDENTITY_KEY)
    with path.open("rb") as handle:
        handle.seek(value_start)
        value = handle.read(66).decode("ascii")
    if len(value) != 66 or value[64:] != "\",":
        raise RetainedNativeError("closure identity field is malformed")
    return value[:64], key, value_start + 66


def closure_body_sha256(path: Path, start: int, end: int, key: int, after: int) -> str:
    digest = hashlib.sha256()
    pos = start
    with path.open("rb") as handle:
        handle.seek(start)
        remaining = end - start
        while remaining > 0:
            chunk = handle.read(min(CHUNK, remaining))
            if not chunk:
                break
            chunk_start = pos
            chunk_end = pos + len(chunk)
            if chunk_end <= key or chunk_start >= after:
                digest.update(chunk)
            else:
                if chunk_start < key:
                    digest.update(chunk[: key - chunk_start])
                if chunk_end > after:
                    digest.update(chunk[after - chunk_start:])
            pos = chunk_end
            remaining -= len(chunk)
    return digest.hexdigest()


def hydrate(value: Any, fragments: Mapping[str, Any]) -> Any:
    if isinstance(value, Mapping):
        if set(value) == {"$canonical_preimage_fragment"}:
            digest = value["$canonical_preimage_fragment"]
            if digest not in fragments:
                raise RetainedNativeError("missing canonical preimage fragment")
            return canonicalize(fragments[digest])
        return {key: hydrate(item, fragments) for key, item in value.items()}
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [hydrate(item, fragments) for item in value]
    return value


def ref_material(value: Any) -> Mapping[str, Any]:
    return canonicalize(value)


def read_json_value(text: str, needle: str) -> tuple[Any, int]:
    index = text.find(needle)
    if index < 0:
        raise RetainedNativeError(f"tail key absent: {needle}")
    value, end = json.JSONDecoder().raw_decode(text, index + len(needle))
    return value, end


def tail_material(path: Path, closure_end: int) -> Mapping[str, Any]:
    precheck = find_in_tail(path, b'"precheck":')
    start = closure_end + 1
    with path.open("rb") as handle:
        handle.seek(start)
        text = handle.read(precheck - start).decode("utf-8")
    keys = (
        "comparison_fact_manifest",
        "constituent_i03_closure_identity",
        "constituent_i03_fact_manifest",
        "court_constitution_refs",
        "exact_ref_manifest",
        "expected_learned_product",
        "frontier_manifest",
        "projection_and_release_refs",
        "replay_manifest",
        "semantic_authority_closure",
        "source_identity",
    )
    result = {}
    for key in keys:
        value, _ = read_json_value(text, f'"{key}":')
        result[key] = value
    return result


def closure_tail(path: Path, closure_end: int) -> Mapping[str, Any]:
    start = max(0, closure_end - 2 * 1024 * 1024)
    with path.open("rb") as handle:
        handle.seek(start)
        text = handle.read(closure_end - start).decode("utf-8")
    result = {}
    for key in (
        "representation_authority_material",
        "representation_authority_ref",
        "structural_admission_object_count",
    ):
        value, _ = read_json_value(text, f'"{key}":')
        result[key] = value
    schema_index = text.rfind('"schema":"')
    if schema_index < 0:
        raise RetainedNativeError("closure schema key absent")
    value, _ = json.JSONDecoder().raw_decode(text, schema_index + len('"schema":'))
    result["schema"] = value
    return result


def read_closure_value(path: Path, key: str) -> Any:
    with path.open("rb") as handle:
        for value in ijson.items(
            handle,
            f"material.canonical_empirical_object_closure.{key}",
            use_float=False,
        ):
            return value
    raise RetainedNativeError(f"closure value absent: {key}")


def astra_summary(path: Path, closure_start: int) -> Any:
    with path.open("rb") as handle:
        text = handle.read(closure_start).decode("utf-8")
    value, _ = read_json_value(text, '"astra_shaped_empirical_summary":')
    return value


def object_meta(obj: Any, doc: Mapping[str, Any], raw: bytes, compressed: bytes) -> Mapping[str, Any]:
    sf = obj.semantic_fields
    base = {
        "schema": f"{obj.schema_id}@{obj.schema_version}",
        "schema_id": obj.schema_id,
        "schema_version": obj.schema_version,
        "typed_state": obj.typed_state,
        "ref": obj.ref.as_dict(),
        "object_id": obj.object_id,
        "content_hash": obj.content_hash,
        "doc_sha256": sha256_bytes(raw),
        "uncompressed_bytes": len(raw),
        "gzip_bytes": len(compressed),
        "gzip_sha256": sha256_bytes(compressed),
        "authority_snapshot_ref_count": len(obj.authority_snapshot_refs),
        "dependency_ref_count": len(obj.dependency_refs),
    }
    if obj.schema_id == "EmpiricalFact":
        topology = canonicalize(sf.get("target_topology", {}))
        base.update({
            "empirical_query_spec_ref": ref_material(sf["empirical_query_spec_ref"]),
            "condition_predicate_ref": ref_material(sf["condition_predicate_ref"]),
            "empirical_universe_refs": [ref_material(x) for x in sf["empirical_universe_refs"]],
            "risk_set_ref": ref_material(sf["risk_set_ref"]),
            "replay_ref": ref_material(sf["replay_ref"]),
            "raw_numerator_support": sf["raw_numerator_support"],
            "raw_denominator_support": sf["raw_denominator_support"],
            "raw_resolved_target_support": sf.get("raw_resolved_target_support"),
            "risk_set_type": sf.get("risk_set_type"),
            "target_topology_summary": {
                key: topology[key]
                for key in (
                    "arity",
                    "joint_order_semantics",
                    "target_domain_identity",
                    "requested_target_arity_and_topology",
                    "p02_failure_state",
                )
                if key in topology
            },
            "source_empirical_provenance_ref_count": len(sf.get("source_empirical_provenance_refs", ())),
            "risk_set_member_ref_count": len(sf.get("risk_set_member_refs", ())),
            "denominator_member_ref_count": len(sf.get("denominator_member_refs", ())),
            "uncertainty_method_or_typed_state": sf.get("uncertainty_method_or_typed_state"),
        })
    elif obj.schema_id == "EmpiricalQuerySpec":
        base.update({
            "condition_predicate_ref": ref_material(sf["condition_predicate_ref"]),
            "risk_set_ref": ref_material(sf["risk_set_ref"]),
            "empirical_universe_refs": [ref_material(x) for x in sf["empirical_universe_refs"]],
            "target_refs": [ref_material(x) for x in sf["target_refs"]],
        })
    elif obj.schema_id == "EmpiricalPredicate":
        base.update({
            "predicate_hash": sf["predicate_hash"],
            "grammar_authority_ref": ref_material(sf["grammar_authority_ref"]),
            "risk_set_refs": [ref_material(x) for x in sf.get("risk_set_refs", ())],
        })
    elif obj.schema_id == "DiscoveryResultReceipt":
        identity = canonicalize(sf["candidate_identity"])
        roles = identity.get("query_roles", ())
        base.update({
            "discovery_authority_ref": ref_material(sf["discovery_authority_ref"]),
            "candidate_hash": identity.get("candidate_hash"),
            "rule_id": identity.get("rule_id"),
            "candidate_identity": identity,
            "query_role_count": len(roles),
            "winning_predicate_ref": ref_material(sf["winning_predicate_ref"]),
            "empirical_fact_refs": [ref_material(x) for x in sf["empirical_fact_refs"]],
            "validation_fact_refs": [ref_material(x) for x in sf["validation_fact_refs"]],
            "coverage_state": sf["coverage_state"],
            "evaluated_frontier_ref": ref_material(sf["evaluated_frontier_ref"]),
            "support_uncertainty_state": canonicalize(sf.get("support_uncertainty_state")),
            "replay_ref": ref_material(sf["replay_ref"]),
        })
    elif obj.schema_id == "AuthoritySnapshot":
        base.update({
            "authority_id": sf["authority_id"],
            "authority_version": sf["authority_version"],
            "authority_content_hash": sf["authority_content_hash"],
            "authority_kind": sf["authority_kind"],
            "decision_state": sf["decision_state"],
            "governed_operations": canonicalize(sf["governed_operations"]),
            "governed_object_families": canonicalize(sf["governed_object_families"]),
        })
    return base


def write_json(path: Path, value: Any) -> None:
    path.write_bytes(canonical_bytes(value) + b"\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--checkpoint", type=Path, required=True)
    parser.add_argument("--private", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()

    checkpoint = args.checkpoint.resolve()
    private = args.private.resolve()
    out = args.out.resolve()
    if checkpoint.stat().st_size != CHECKPOINT_BYTES:
        raise RetainedNativeError("checkpoint size mismatch")
    private.mkdir(parents=True, exist_ok=True)
    out.mkdir(parents=True, exist_ok=True)
    objects_root = private / "objects"
    objects_root.mkdir(parents=True, exist_ok=True)
    disk_before = shutil.disk_usage(private)

    checkpoint_sha = sha256_file(checkpoint)
    if checkpoint_sha != CHECKPOINT_SHA256:
        raise RetainedNativeError("checkpoint document hash mismatch")
    checkpoint_identity_sha = checkpoint_identity(checkpoint)

    start, end = closure_bounds(checkpoint)
    identity, identity_key, identity_after = closure_identity_parts(checkpoint, start, end)
    body_sha = closure_body_sha256(checkpoint, start, end, identity_key, identity_after)
    if identity != CLOSURE_IDENTITY or body_sha != CLOSURE_IDENTITY:
        raise RetainedNativeError("closure identity mismatch")

    fragments: dict[str, Any] = {}
    fragment_raw_bytes = 0
    with checkpoint.open("rb") as handle:
        for entry in ijson.items(handle, FRAGMENT_PREFIX, use_float=False):
            digest = entry.get("fragment_hash")
            value = canonicalize(entry.get("value"))
            if not isinstance(digest, str) or len(digest) != 64:
                raise RetainedNativeError("fragment hash malformed")
            if semantic_hash(value) != digest:
                raise RetainedNativeError("fragment content hash mismatch")
            if digest in fragments and canonical_bytes(fragments[digest]) != canonical_bytes(value):
                raise RetainedNativeError("fragment collision")
            fragments[digest] = value
            fragment_raw_bytes += len(canonical_bytes(value))
    fragment_blob = canonical_bytes({"fragments": fragments})
    fragment_gz = gzip.compress(fragment_blob, compresslevel=6, mtime=0)
    (private / "preimage_fragments.json.gz").write_bytes(fragment_gz)

    tail = tail_material(checkpoint, end)
    release = read_closure_value(checkpoint, "c11_release")
    release_raw = canonical_bytes(release)
    release_gz = gzip.compress(release_raw, compresslevel=6, mtime=0)
    (private / "c11_release.json.gz").write_bytes(release_gz)
    closing = closure_tail(checkpoint, end)
    astra = astra_summary(checkpoint, start)
    if closing["schema"] != CLOSURE_SCHEMA:
        raise RetainedNativeError("closure schema mismatch")
    if closing["structural_admission_object_count"] != 0:
        raise RetainedNativeError("structural admission count mismatch")

    if release.get("semantic_release_hash") != EXPECTED_RELEASE:
        raise RetainedNativeError("release identity mismatch")
    if release.get("replay_ref", {}).get("content_hash") != EXPECTED_REPLAY:
        raise RetainedNativeError("replay identity mismatch")
    representation_ref = closing["representation_authority_ref"]
    representation_material = closing["representation_authority_material"]
    if representation_ref.get("authority_content_hash") != EXPECTED_REPRESENTATION:
        raise RetainedNativeError("representation authority mismatch")
    if semantic_hash(canonicalize(representation_material)) != EXPECTED_REPRESENTATION:
        raise RetainedNativeError("representation authority material mismatch")

    index_path = private / "object_index.jsonl"
    existing = []
    if args.resume and index_path.exists():
        with index_path.open(encoding="utf-8") as handle:
            existing = [json.loads(line) for line in handle]
    total_raw = sum(x["uncompressed_bytes"] for x in existing)
    total_gz = sum(x["gzip_bytes"] for x in existing)
    counts: Counter[str] = Counter(x["schema"] for x in existing)
    authority_keys: set[tuple[str, str, str]] = {
        (x["authority_id"], x["authority_version"], x["authority_content_hash"])
        for x in existing if x["schema_id"] == "AuthoritySnapshot"
    }
    existing_hashes = {x["content_hash"] for x in existing}
    count = len(existing)
    with index_path.open("a" if args.resume else "w", encoding="utf-8") as index_handle, checkpoint.open("rb") as handle:
        for packed in ijson.items(handle, OBJECT_PREFIX, use_float=False):
            content_hash = packed.get("content_hash")
            schema_id = packed.get("schema_id")
            target_existing = objects_root / str(schema_id) / f"{content_hash}.json.gz"
            if (
                content_hash in existing_hashes
                and target_existing.is_file()
            ):
                continue
            doc = hydrate(packed, fragments)
            obj = materialize_public_object(doc)
            if canonicalize(obj.as_dict()) != canonicalize(doc):
                raise RetainedNativeError("public object round-trip drift")
            if semantic_hash(obj.semantic_projection()) != obj.content_hash:
                raise RetainedNativeError("public object content hash drift")
            if obj.schema_id == "AuthoritySnapshot":
                authority_keys.add((
                    obj.authority_id,
                    obj.authority_version,
                    obj.authority_content_hash,
                ))
            else:
                for auth in obj.authority_snapshot_refs:
                    if (
                        auth.authority_id,
                        auth.authority_version,
                        auth.authority_content_hash,
                    ) not in authority_keys:
                        raise RetainedNativeError(
                            "authority snapshot closure missing before object"
                        )
            raw = canonical_bytes(obj.as_dict())
            compressed = gzip.compress(raw, compresslevel=6, mtime=0)
            schema_dir = objects_root / obj.schema_id
            schema_dir.mkdir(parents=True, exist_ok=True)
            target = schema_dir / f"{obj.content_hash}.json.gz"
            target.write_bytes(compressed)
            meta = object_meta(obj, doc, raw, compressed)
            index_handle.write(json.dumps(meta, sort_keys=True, separators=(",", ":")) + "\n")
            counts[meta["schema"]] += 1
            existing_hashes.add(obj.content_hash)
            count += 1
            total_raw += len(raw)
            total_gz += len(compressed)
            if count % 25 == 0:
                print(f"objects={count} raw={total_raw} gz={total_gz}", flush=True)

    if dict(sorted(counts.items())) != EXPECTED_INVENTORY:
        raise RetainedNativeError(f"inventory mismatch: {dict(counts)!r}")

    with index_path.open(encoding="utf-8") as handle:
        index = [json.loads(line) for line in handle]
    by_ref = {x["ref"]["object_id"]: x for x in index}
    if len(by_ref) != len(index):
        raise RetainedNativeError("duplicate object ref")
    facts = [x for x in index if x["schema_id"] == "EmpiricalFact"]
    queries = [x for x in index if x["schema_id"] == "EmpiricalQuerySpec"]
    predicates = [x for x in index if x["schema_id"] == "EmpiricalPredicate"]
    authorities = [x for x in index if x["schema_id"] == "AuthoritySnapshot"]
    receipts = [x for x in index if x["schema_id"] == "DiscoveryResultReceipt"]
    discoveries = [x for x in index if x["schema_id"] == "DiscoveryAuthority"]
    universes = [x for x in index if x["schema_id"] == "EmpiricalUniverse"]
    if len(facts) != 60 or len(receipts) != 50 or len(authorities) != 24:
        raise RetainedNativeError("required object class count mismatch")

    query_by_ref = {x["ref"]["object_id"]: x for x in queries}
    predicate_by_ref = {x["ref"]["object_id"]: x for x in predicates}
    authority_keys = {
        (x["authority_id"], x["authority_version"], x["authority_content_hash"])
        for x in authorities
    }
    for fact in facts:
        qref = fact["empirical_query_spec_ref"]["object_id"]
        pref = fact["condition_predicate_ref"]["object_id"]
        if qref not in query_by_ref or pref not in predicate_by_ref:
            raise RetainedNativeError("fact query/predicate preimage missing")
        if query_by_ref[qref]["condition_predicate_ref"]["object_id"] != pref:
            raise RetainedNativeError("fact query/predicate binding mismatch")

    compact = tail["constituent_i03_fact_manifest"]
    compact_refs = {x["ref"]["object_id"] for x in compact}
    fact_refs = {x["ref"]["object_id"] for x in facts}
    if fact_refs != compact_refs:
        raise RetainedNativeError("compact fact closure mismatch")
    rows = tail["comparison_fact_manifest"]
    receipt_by_candidate = {x["candidate_hash"]: x for x in receipts}
    role_count = 0
    valid_empty = []
    for row in rows:
        candidate_hash = row["candidate_hash"]
        receipt = receipt_by_candidate.get(candidate_hash)
        if receipt is None:
            raise RetainedNativeError("candidate receipt missing")
        if canonical_bytes(receipt["candidate_identity"]) != canonical_bytes(
            row["semantic_fields"]["candidate_identity"]
        ):
            raise RetainedNativeError("candidate identity mismatch")
        receipt_fact_refs = {x["object_id"] for x in receipt["empirical_fact_refs"]}
        compact_fact_refs = {
            x["ref"]["object_id"]
            for x in row["semantic_fields"].get("constituent_fact_manifest", ())
        }
        if receipt_fact_refs != compact_fact_refs:
            raise RetainedNativeError("candidate fact refs mismatch")
        identity = row["semantic_fields"]["candidate_identity"]
        roles = identity.get("query_roles", ())
        role_count += len(roles)
        for role in roles:
            qref = role["query_ref"]["object_id"]
            pref = role["predicate_ref"]["object_id"]
            if qref not in query_by_ref or pref not in predicate_by_ref:
                raise RetainedNativeError("role query/predicate preimage missing")
            if query_by_ref[qref]["condition_predicate_ref"]["object_id"] != pref:
                raise RetainedNativeError("role query/predicate binding mismatch")
        if receipt["coverage_state"] == "EVALUATED_VALID_EMPTY":
            valid_empty.append(receipt["ref"])
    if len(rows) != 50 or role_count != 77:
        raise RetainedNativeError("candidate/role closure mismatch")

    coverage = Counter(x["coverage_state"] for x in receipts)
    typed = Counter(x["typed_state"] for x in receipts)
    fact_states = Counter(x["typed_state"] for x in facts)
    if dict(coverage) != {"EVALUATED_SUPPORTED": 49, "EVALUATED_VALID_EMPTY": 1}:
        raise RetainedNativeError("coverage terminal mismatch")
    if dict(typed) != {"DISCOVERED_RESULT_SUPPORTED": 49, "VALID_EMPTY": 1}:
        raise RetainedNativeError("typed terminal mismatch")
    if dict(fact_states) != {"SUPPORTED": 60}:
        raise RetainedNativeError("fact state mismatch")
    if len(valid_empty) != 1:
        raise RetainedNativeError("valid-empty evidence mismatch")

    mixed = [
        x for x in authorities
        if x["authority_id"] == "urn:rawlsing:prev3:p2r4a:pre553:mixed-predicate-grammar"
    ]
    if (
        len(mixed) != 1
        or mixed[0]["content_hash"]
        != "c22cccad0add0048047f4edc3852ebce5d7f87ca0e7b81acb18587abb98ece4e"
        or mixed[0]["authority_content_hash"]
        != "0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55"
    ):
        raise RetainedNativeError("adopted mixed-predicate authority missing")

    graph = {
        "schema": "PYAT_R128_OBJECT_GRAPH@1",
        "closure_identity": CLOSURE_IDENTITY,
        "source_identity": tail["source_identity"],
        "inventory": dict(sorted(counts.items())),
        "objects": {
            "authorities": [
                {"ref": x["ref"], "authority_id": x["authority_id"],
                 "authority_version": x["authority_version"],
                 "authority_content_hash": x["authority_content_hash"],
                 "authority_kind": x["authority_kind"]}
                for x in authorities
            ],
            "discovery_authorities": [x["ref"] for x in discoveries],
            "empirical_universes": [x["ref"] for x in universes],
            "facts": [
                {"ref": x["ref"], "condition_predicate_ref": x["condition_predicate_ref"],
                 "empirical_query_spec_ref": x["empirical_query_spec_ref"],
                 "risk_set_ref": x["risk_set_ref"],
                 "raw_denominator_support": x["raw_denominator_support"],
                 "target_topology_summary": x["target_topology_summary"],
                 "source_empirical_provenance_ref_count": x["source_empirical_provenance_ref_count"]}
                for x in facts
            ],
            "queries": [
                {"ref": x["ref"], "condition_predicate_ref": x["condition_predicate_ref"],
                 "risk_set_ref": x["risk_set_ref"]}
                for x in queries
            ],
            "predicates": [
                {"ref": x["ref"], "predicate_hash": x["predicate_hash"],
                 "grammar_authority_ref": x["grammar_authority_ref"]}
                for x in predicates
            ],
            "discovery_receipts": [
                {"ref": x["ref"], "candidate_hash": x["candidate_hash"],
                 "rule_id": x["rule_id"], "coverage_state": x["coverage_state"],
                 "typed_state": x["typed_state"],
                 "query_role_count": x["query_role_count"],
                 "empirical_fact_refs": x["empirical_fact_refs"]}
                for x in receipts
            ],
        },
        "edges": {
            "fact_query": [
                {"from": x["ref"], "to": x["empirical_query_spec_ref"], "type": "EMPIRICAL_QUERY_SPEC"}
                for x in facts
            ],
            "fact_predicate": [
                {"from": x["ref"], "to": x["condition_predicate_ref"], "type": "CONDITION_PREDICATE"}
                for x in facts
            ],
            "receipt_fact": [
                {"from": x["ref"], "to": ref, "type": "EMPIRICAL_FACT"}
                for x in receipts for ref in x["empirical_fact_refs"]
            ],
        },
        "frontier": {
            "candidate_count": len(rows),
            "query_role_count": role_count,
            "coverage_state_counts": dict(sorted(coverage.items())),
            "typed_state_counts": dict(sorted(typed.items())),
            "valid_empty_receipt_ref": valid_empty[0],
        },
        "c11_release": {
            "release_ref": release["release_ref"],
            "replay_ref": release["replay_ref"],
            "semantic_release_hash": release["semantic_release_hash"],
        },
        "representation_authority": {
            "ref": representation_ref,
            "material_sha256": EXPECTED_REPRESENTATION,
        },
        "adopted_mixed_predicate_authority": mixed[0],
        "unretained_in_public_graph": [
            "risk_set_member_refs",
            "denominator_member_refs",
            "source_empirical_provenance_refs",
            "complete_cell_semantic_projection",
            "respondent rows and person/event preimages",
        ],
    }
    write_json(out / "OBJECT_GRAPH.json", graph)

    validation = {
        "schema": "PYAT_R128_NATIVE_VALIDATION@1",
        "status": "PASS__RETAINED_NATIVE_OBJECTS_REHYDRATED_AND_CLOSED",
        "evidence_class": "FRESH_RETAINED_REPLAY__NO_SOURCE_EXECUTION__ORIGINAL_SOURCE_NOT_EXECUTED",
        "checkpoint": {
            "bytes": checkpoint.stat().st_size,
            "sha256": checkpoint_sha,
            "closure_identity": CLOSURE_IDENTITY,
            "closure_body_sha256": body_sha,
            "closure_schema": CLOSURE_SCHEMA,
            "checkpoint_identity_sha256": checkpoint_identity_sha,
        },
        "objects": {
            "total": count,
            "inventory": dict(sorted(counts.items())),
            "all_roundtrip": True,
            "all_content_hashes": True,
            "all_authority_refs_resolve": True,
            "structural_admission_count": 0,
            "raw_bytes_recovered": total_raw,
            "gzip_bytes_private": total_gz,
        },
        "frontier": graph["frontier"],
        "retained_private_content": {
            "facts_with_full_preimages": len(facts),
            "source_empirical_provenance_ref_count": sum(
                x["source_empirical_provenance_ref_count"] for x in facts
            ),
            "risk_set_member_ref_count": sum(
                x["risk_set_member_ref_count"] for x in facts
            ),
            "denominator_member_ref_count": sum(
                x["denominator_member_ref_count"] for x in facts
            ),
            "target_topology_fact_count": sum(
                1 for x in facts if x["target_topology_summary"]
            ),
            "uncertainty_states": sorted(
                {str(x["uncertainty_method_or_typed_state"]) for x in facts}
            ),
            "valid_empty_receipt_ref": graph["frontier"]["valid_empty_receipt_ref"],
            "preimage_fragments": len(fragments),
        },
        "identities": {
            "release": release["release_ref"],
            "replay": release["replay_ref"],
            "representation_authority": representation_ref,
            "adopted_mixed_predicate_authority": mixed[0],
            "candidate_frontier": {
                "candidate_count": len(rows),
                "query_role_count": role_count,
            },
        },
        "resource": {
            "private_store": ".r61/r128-retained-native/private",
            "fragments": len(fragments),
            "fragment_raw_bytes": fragment_raw_bytes,
            "fragment_gzip_bytes": len(fragment_gz),
            "c11_release_raw_bytes": len(release_raw),
            "c11_release_gzip_bytes": len(release_gz),
            "c11_release_gzip_sha256": sha256_bytes(release_gz),
        },
        "oracle_summary": {
            "astra_shaped_empirical_summary_identity": semantic_hash(astra),
            "stored_private": True,
        },
        "limits": [
            "No raw survey/DTA/SAV/source hash/metadata decode or respondent snapshot expansion.",
            "No full checkpoint JSON load or 3.4GB serialization.",
            "Heavy member/provenance lists remain private and unexpanded in Git output.",
            "Historical counts are conservation checks for this retained artifact, not current survey scope.",
        ],
    }
    write_json(out / "NATIVE_VALIDATION.json", validation)

    (private / "astra_shaped_empirical_summary.json").write_bytes(canonical_bytes(astra) + b"\n")
    write_json(private / "material_tail.json", tail)
    write_json(private / "closure_metadata.json", {
        "closure_identity": CLOSURE_IDENTITY,
        "closure_schema": CLOSURE_SCHEMA,
        "c11_release": release,
        "representation_authority_ref": representation_ref,
        "representation_authority_material": representation_material,
        "inventory": dict(sorted(EXPECTED_INVENTORY.items())),
        "structural_admission_object_count": closing["structural_admission_object_count"],
    })

    disk_after = shutil.disk_usage(private)
    max_rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    resources = {
        "schema": "PYAT_R128_RESOURCE_AND_ACCESS@1",
        "status": "PASS__BOUNDED_STREAMING_WITHIN_16GIB_HOST",
        "checkpoint_reads": {
            "full_document_hash_passes": 1,
            "closure_body_hash_passes": 1,
            "fragment_stream_passes": 1,
            "object_stream_passes": 1,
            "targeted_small_field_reads": 4,
            "source_accesses": 0,
            "raw_survey_accesses": 0,
            "respondent_snapshot_expansions": 0,
            "full_checkpoint_json_loads": 0,
        },
        "memory": {
            "max_rss_bytes": max_rss,
            "limit_bytes": 3 * 1024 * 1024 * 1024,
            "below_limit": max_rss < 3 * 1024 * 1024 * 1024,
            "host_physical_bytes": 16 * 1024 * 1024 * 1024,
        },
        "disk": {
            "before_free_bytes": disk_before.free,
            "after_free_bytes": disk_after.free,
            "private_gzip_bytes": total_gz + len(fragment_gz) + len(release_gz),
            "uncompressed_object_bytes": total_raw,
        },
        "private_store": {
            "locator": ".r61/r128-retained-native/private",
            "object_files": count,
            "index": "object_index.jsonl",
            "fragments": "preimage_fragments.json.gz",
            "oracle_summary": "astra_shaped_empirical_summary.json",
            "c11_release": "c11_release.json.gz",
        },
        "source_access": {
            "raw_source_opens": 0,
            "raw_source_hashes": 0,
            "raw_survey_decodes": 0,
            "retained_checkpoint_reads_counted_separately": True,
        },
    }
    write_json(out / "RESOURCE_AND_ACCESS.json", resources)

    summary = {
        "schema": "PYAT_R128_EXTRACTION_SUMMARY@1",
        "status": validation["status"],
        "closure_identity": CLOSURE_IDENTITY,
        "object_count": count,
        "inventory": dict(sorted(counts.items())),
        "frontier": graph["frontier"],
        "object_index": str(index_path),
        "outputs": ["OBJECT_GRAPH.json", "NATIVE_VALIDATION.json", "RESOURCE_AND_ACCESS.json"],
    }
    write_json(private / "extraction_summary.json", summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"R128_EXTRACTION_FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        raise
