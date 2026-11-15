from __future__ import annotations

import argparse
from collections import Counter
import dataclasses
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import subprocess
import types
from typing import Any, Mapping, Sequence

import rawlsing_next.pre553_independent_parity_oracle as oracle_mod
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.pre553_independent_parity_oracle import (
    FreezeContext,
    LITS_ASTRA_D04_R2_COMMIT,
    LITS_CANDIDATE_COUNT,
    LITS_FRONTIER_SEAL,
    LITS_QUERY_ROLE_COUNT,
    LITS_LEARNED_PRODUCT_IDENTITY,
    LITS_PROJECTION_IDENTITY,
    LITS_SEMANTIC_REPLAY_IDENTITY,
    LITS_SOURCE_SHA256,
    ORACLE_SCHEMA,
    WVS7_SOURCE_SHA256,
    WVS_MATERIALIZER_CONTRACT,
    build_lits_i_oracle,
    freeze_wvs7_oracle_from_common_material,
    verify_frozen_oracle,
)
from rawlsing_next.ee_p2x_candidate_process_envelope import (
    FREEZE_RECEIPT_SCHEMA,
    load_frozen_upstream_receipt,
)
from rawlsing_next.fiabc_lits_astra_substantive_parity import (
    assert_substantive_parity as assert_lits_astra_substantive_parity,
    normalize_accepted_astra_summary,
    normalize_current_lits_summary,
)
from rawlsing_next.fiabc_lits_i_representation_authority import (
    LEGACY_FACADE_BLOB as LITS_LEGACY_FACADE_BLOB,
    LEGACY_FACADE_COMMIT as LITS_LEGACY_FACADE_COMMIT,
    LEGACY_FACADE_PATH as LITS_LEGACY_FACADE_PATH,
    REPRESENTATION_AUTHORITY_MATERIAL as LITS_REPRESENTATION_AUTHORITY_MATERIAL,
    REPRESENTATION_AUTHORITY_REF as LITS_REPRESENTATION_AUTHORITY_REF,
    TARGET_VARIABLES as LITS_TARGET_VARIABLES,
    authorized_replay_cell as authorized_lits_replay_cell,
    representation_authority_snapshot as lits_representation_authority_snapshot,
)
from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
from rawlsing_next.pre553_source_backed_c11_facade import (
    physical_value_binding_key as current_typed_physical_value_binding_key,
)

PRODUCER_SCHEMA = "RAWLSING_FIABC_FINAL_ORACLE_FREEZE_PRODUCERS@1.0.0"
R1M_SCHEMA = "FIABC_LM2_R1M_FRESH_WVS_ORACLE@1.0.0"
R1M_TRUTH_SCHEMA = "FIABC_LM2_R1M_WVS_TRUTH_PAYLOAD@1.0.0"
R1M_ORACLE_IDENTITY = "3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800"
R1M_TRUTH_IDENTITY = "eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405"
SUCCESSOR_DISCOVERY_AUTHORITY = "3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873"
SUCCESSOR_LOCK2 = "5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139"
SUCCESSOR_LOCK2_REPLAY = "9b5ac1726a03798d07e965396192d1bfefbee6d2188bad5a3acfb467ef063d4a"

LITS_RUNTIME_CATALOG = "5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02"
LITS_ACTIVE_BINDING = "a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308"
LITS_RUNTIME_RELEASE = "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f"
LITS_RUNTIME_REPLAY = "30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08"
LITS_RUNTIME_PROJECTION = "23912633a23318d22bad0da08027867031320331d8d436d944e9c0b21eb086eb"
LITS_BASE_C11_RELEASE = "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
LITS_BASE_C11_REPLAY = "6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd"
LITS_BASE_CANDIDATE_PROJECTION = "7f81a222ea2611638d7ce7ac55c695120b57323832e6dc17ff65c1992201659c"
LITS_R5B_COMMIT = "648a39ad5bed42f66e066410af5869604d29c12d"
LITS_R5B_DRIVER = "WORKER_RETURNS/EE-P2R5B/03_LOCAL_I02_SUCCESSOR_RELEASE_DRIVER.py"
LITS_R5B_BLOBS = {
    LITS_R5B_DRIVER: "b819fdff50470a71f1c570aa8021e28b361fa986",
    "WORKER_RETURNS/EE-P2R5B/SUPPORT/FROZEN_BASE/AS2A_LITS1_SHARED_CERTIFICATION_20260827/01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv": "c24e0d6acc6f2b823f0fc3fa5fb8a52b7c1cab0c",
    "WORKER_RETURNS/EE-P2R5B/SUPPORT/FROZEN_BASE/AS2A_LITS1_SHARED_CERTIFICATION_20260827/04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json": "174b931e8aa89111086e3d46159b47154bed7f16",
    "WORKER_RETURNS/EE-P2R5B/SUPPORT/FROZEN_BASE/AS2B_LITS1_MECHANICAL_SOURCE_CERTIFICATION_20260827/run_as2b_lits1_mechanical_certification.py": "c51b56779ab9d79126619b7733d41f5253c8150f",
    "WORKER_RETURNS/EE-P2R5B/SUPPORT/FROZEN_F02/prev3_lits1_selector_closure.py": "7b45b277164fa90c3da739aab26b516f7a8cb8dc",
}
LITS_ROWS = 29002
LITS_VARIABLES = 1198
WVS_ROWS = 97220
WVS_VARIABLES = 613
LITS_ACCEPTED_TERMINAL_COUNTS = {
    "EVALUATED_SUPPORTED": 49,
    "EVALUATED_VALID_EMPTY": 1,
}
LITS_ACCEPTED_TYPED_TERMINAL_COUNTS = {
    "DISCOVERED_RESULT_SUPPORTED": 49,
    "VALID_EMPTY": 1,
}
LITS_MATERIALIZATION_CHECKPOINT_SCHEMA = (
    "FIABC_LITS_CURRENT_NEUTRAL_I05_MATERIALIZATION_CHECKPOINT@3.0.0"
)
LITS_PARTIAL_MATERIALIZATION_CHECKPOINT_SCHEMA = (
    "FIABC_LITS_CURRENT_NEUTRAL_I05_MATERIALIZATION_CHECKPOINT@2.0.0"
)
LITS_LEGACY_MATERIALIZATION_CHECKPOINT_SCHEMA = (
    "FIABC_LITS_CURRENT_NEUTRAL_I05_MATERIALIZATION_CHECKPOINT@1.0.0"
)
LITS_CANONICAL_EMPIRICAL_CLOSURE_SCHEMA = (
    "FIABC_LITS_CANONICAL_CURRENT_EMPIRICAL_OBJECT_CLOSURE@1.0.0"
)
LITS_C11_RELEASE_RETENTION_SCHEMA = "FIABC_LITS_C11_RELEASE_RETENTION@1.0.0"
LITS_MATERIALIZATION_CHECKPOINT_NAME = "current_i05_materialization_checkpoint_v3.json"

ASTRA_PRODUCT_PATH = "WORKER_RETURNS/ASTRA-D04-R2/01_TYPED_LEARNED_EMPIRICAL_PRODUCT.json"
ASTRA_ROLE_PATH = "WORKER_RETURNS/ASTRA-D04-R2/02_77_ROLE_EXECUTION_RECEIPT.json"
ASTRA_REPLAY_PATH = "WORKER_RETURNS/ASTRA-D04-R2/03_SOURCE_AND_REPLAY_RECEIPT.json"
ASTRA_INPUT_GIT_BLOBS = {
    ASTRA_PRODUCT_PATH: "26fa18d10d242f3db212f6ee3e6f28abee3327ac",
    ASTRA_ROLE_PATH: "211e19bb17cd8e3c63418b686ac20508072cb7d7",
    ASTRA_REPLAY_PATH: "b2c70e992955853b540e498214c296ccc0e25b83",
}
CURRENT_SOURCE_MANIFEST_REF = "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json#source_root_law.canonical_source_sha256"


class FinalOracleProducerError(RuntimeError):
    pass


def _bind_current_lits_execution_to_astra(
    *,
    execution_receipt: Mapping[str, Any],
    semantic_replay_identity: str,
    terminal_counts: Mapping[str, int],
    candidate_count: int,
    query_role_count: int,
) -> Mapping[str, Any]:
    """Bind current neutral identities beside the immutable ASTRA anchor.

    The current carrier-neutral execution receipt and the historical ASTRA
    typed product are different schemas, so their object hashes are not
    interchangeable. The current identities remain current; the historical
    ASTRA product/replay are validated separately as immutable provenance by
    ``build_lits_i_oracle``.
    """
    if candidate_count != LITS_CANDIDATE_COUNT or query_role_count != LITS_QUERY_ROLE_COUNT:
        raise FinalOracleProducerError("LiTS current neutral runtime is not exact 50/77")
    observed_counts = dict(sorted(terminal_counts.items()))
    if observed_counts != LITS_ACCEPTED_TERMINAL_COUNTS:
        raise FinalOracleProducerError(
            "current neutral LiTS typed terminal counts do not equal accepted "
            f"ASTRA counts: observed={observed_counts!r}"
        )
    if not isinstance(semantic_replay_identity, str) or len(semantic_replay_identity) != 64:
        raise FinalOracleProducerError("current neutral LiTS semantic replay identity is malformed")
    execution_identity = execution_receipt.get("execution_identity")
    if not isinstance(execution_identity, str) or len(execution_identity) != 64:
        raise FinalOracleProducerError("current neutral LiTS execution identity is malformed")
    return {
        "product_identity": semantic_hash(execution_receipt),
        "semantic_identity": semantic_replay_identity,
        "replay_identity": execution_identity,
        "exact_output_identity": execution_identity,
        "coverage": {
            "candidate_count": candidate_count,
            "query_role_count": query_role_count,
            "typed_terminal_counts": observed_counts,
        },
    }


def _canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def _write_json(path: Path, value: Any) -> str:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = _canonical_bytes(value)
    tmp = path.with_name(path.name + ".tmp")
    tmp.write_bytes(payload)
    os.replace(tmp, path)
    return hashlib.sha256(payload).hexdigest()


def _load_json(path: Path) -> Mapping[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise FinalOracleProducerError(f"invalid JSON: {path}") from exc
    if not isinstance(value, Mapping):
        raise FinalOracleProducerError(f"JSON object required: {path}")
    return value


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_json(repo_root: Path, commit: str, path: str) -> Mapping[str, Any]:
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(Path(repo_root).resolve()), "show", f"{commit}:{path}"],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as exc:
        raise FinalOracleProducerError(
            f"required immutable historical input unavailable at {commit}:{path}"
        ) from exc
    value = json.loads(raw)
    if not isinstance(value, Mapping):
        raise FinalOracleProducerError("historical JSON input is not an object")
    return value


def _git_blob_sha(repo_root: Path, commit: str, path: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(Path(repo_root).resolve()), "rev-parse", f"{commit}:{path}"],
            stderr=subprocess.STDOUT,
            text=True,
        ).strip()
    except subprocess.CalledProcessError as exc:
        raise FinalOracleProducerError(
            f"required immutable historical blob unavailable at {commit}:{path}"
        ) from exc


def _verified_astra_input_manifest(repo_root: Path) -> list[Mapping[str, Any]]:
    inputs = []
    for path, expected_blob in ASTRA_INPUT_GIT_BLOBS.items():
        observed_blob = _git_blob_sha(repo_root, LITS_ASTRA_D04_R2_COMMIT, path)
        if observed_blob != expected_blob:
            raise FinalOracleProducerError(
                f"immutable ASTRA-D04-R2 input blob drift: {path}: "
                f"expected={expected_blob} observed={observed_blob}"
            )
        inputs.append({
            "commit": LITS_ASTRA_D04_R2_COMMIT,
            "path": path,
            "git_blob_sha": observed_blob,
        })
    return canonicalize(inputs)


def _candidate_cells_root(work_root: Path) -> Path:
    return (Path(work_root).resolve() / "cells").resolve()


def _reject_candidate_owned_path(path: Path, work_root: Path, label: str) -> None:
    p = Path(path).resolve()
    cells = _candidate_cells_root(work_root)
    if p == cells or cells in p.parents:
        raise FinalOracleProducerError(f"{label} may not reside in candidate-owned cells root")


def _check_zero_candidate_provenance(value: Mapping[str, Any], label: str) -> None:
    if value.get("candidate_outputs_seen") != 0:
        raise FinalOracleProducerError(f"{label} observed candidate output")
    if value.get("candidate_owned_roots_consulted") not in ([], ()):
        raise FinalOracleProducerError(f"{label} consulted candidate-owned roots")
    if value.get("candidate_owned_state_reused") is not False:
        raise FinalOracleProducerError(f"{label} reused candidate-owned state")
    processes = value.get("candidate_processes_started")
    if processes not in (None, 0):
        raise FinalOracleProducerError(f"{label} started candidate processes")



def _canonical_public_object_documents(objects: Sequence[Any]) -> list[Mapping[str, Any]]:
    """Serialize exact PRE553 public objects without projecting away identity material."""
    by_key: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    for obj in objects:
        ref = getattr(obj, "ref", None)
        as_dict = getattr(obj, "as_dict", None)
        if ref is None or not callable(as_dict):
            raise FinalOracleProducerError("canonical closure received a non-public semantic object")
        key = _ref_key(ref.as_dict())
        doc = canonicalize(as_dict())
        previous = by_key.setdefault(key, doc)
        if canonicalize(previous) != doc:
            raise FinalOracleProducerError("canonical closure contains conflicting public-object preimages")
    return [by_key[key] for key in sorted(by_key)]



_LITS_PREIMAGE_FRAGMENT_MARKER = "$canonical_preimage_fragment"


def _store_lits_preimage_fragment(
    value: Any,
    fragments: dict[str, Any],
) -> Mapping[str, str]:
    material = canonicalize(value)
    digest = semantic_hash(material)
    previous = fragments.setdefault(digest, material)
    if canonicalize(previous) != material:
        raise FinalOracleProducerError("LiTS canonical preimage fragment hash collision")
    return {_LITS_PREIMAGE_FRAGMENT_MARKER: digest}


def _pack_lits_canonical_preimage(
    document: Mapping[str, Any],
    fragments: dict[str, Any],
) -> Mapping[str, Any]:
    """Losslessly deduplicate large identity-bearing fact fragments."""
    packed = canonicalize(document)
    if packed.get("schema_id") != "EmpiricalFact":
        return packed
    fields = dict(packed["semantic_fields"])
    for name in ("risk_set_member_refs", "denominator_member_refs"):
        if name in fields:
            fields[name] = _store_lits_preimage_fragment(fields[name], fragments)
    topology = fields.get("target_topology")
    if isinstance(topology, Mapping) and "complete_cell_semantic_projection" in topology:
        topology = dict(topology)
        topology["complete_cell_semantic_projection"] = _store_lits_preimage_fragment(
            topology["complete_cell_semantic_projection"],
            fragments,
        )
        fields["target_topology"] = topology
    packed = dict(packed)
    packed["semantic_fields"] = fields
    return canonicalize(packed)


def _lits_preimage_fragment_map(
    closure: Mapping[str, Any],
) -> dict[str, Any]:
    raw = closure.get("preimage_fragments")
    if not isinstance(raw, Sequence) or isinstance(raw, (str, bytes)):
        raise FinalOracleProducerError("LiTS canonical preimage fragment store is absent")
    fragments: dict[str, Any] = {}
    for entry in raw:
        if not isinstance(entry, Mapping) or set(entry) != {"fragment_hash", "value"}:
            raise FinalOracleProducerError("LiTS canonical preimage fragment entry is malformed")
        digest = entry.get("fragment_hash")
        value = entry.get("value")
        if not isinstance(digest, str) or len(digest) != 64:
            raise FinalOracleProducerError("LiTS canonical preimage fragment hash is malformed")
        if semantic_hash(canonicalize(value)) != digest:
            raise FinalOracleProducerError("LiTS canonical preimage fragment content hash drift")
        previous = fragments.setdefault(digest, canonicalize(value))
        if previous != canonicalize(value):
            raise FinalOracleProducerError("LiTS canonical preimage fragment collision")
    return fragments


def _hydrate_lits_canonical_preimage(
    value: Any,
    fragments: Mapping[str, Any],
) -> Any:
    if isinstance(value, Mapping):
        if set(value) == {_LITS_PREIMAGE_FRAGMENT_MARKER}:
            digest = value.get(_LITS_PREIMAGE_FRAGMENT_MARKER)
            if not isinstance(digest, str) or digest not in fragments:
                raise FinalOracleProducerError("LiTS canonical preimage references missing fragment")
            return canonicalize(fragments[digest])
        return {
            key: _hydrate_lits_canonical_preimage(item, fragments)
            for key, item in value.items()
        }
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        return [_hydrate_lits_canonical_preimage(item, fragments) for item in value]
    return value


def _lits_c11_release_retention_document(release: Any) -> Mapping[str, Any]:
    replay = canonicalize(release.replay_manifest.as_dict())
    replay_projection = {
        key: replay[key]
        for key in ("record_family", "record_version", "semantic_fields")
    }
    if semantic_hash(replay_projection) != replay.get("content_hash"):
        raise FinalOracleProducerError("LiTS C11 replay-manifest preimage/hash mismatch")
    if release.replay_manifest.ref.content_hash != replay.get("content_hash"):
        raise FinalOracleProducerError("LiTS C11 replay-manifest ref/preimage mismatch")
    return canonicalize({
        "schema": LITS_C11_RELEASE_RETENTION_SCHEMA,
        "release_ref": release.release_ref.as_dict(),
        "source_artifact_ref": release.source_artifact_ref.as_dict(),
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "semantic_release_hash": release.semantic_release_hash,
        "replay_ref": release.replay_manifest.ref.as_dict(),
        "replay_manifest": replay,
        "m01_m18_coverage": release.m01_m18_coverage,
    })


def _retain_exact_runtime_authority_snapshots(
    objects: Sequence[Any], runtime_authority_set: Any
) -> list[Any]:
    """Close public-object authority refs over exact retained snapshot preimages."""
    full_objects = list(objects)
    retained_authority_keys = {
        (obj.authority_id, obj.authority_version, obj.authority_content_hash)
        for obj in full_objects
        if getattr(obj, "schema_id", None) == "AuthoritySnapshot"
    }
    requested_authorities = {}
    for obj in full_objects:
        if getattr(obj, "schema_id", None) == "AuthoritySnapshot":
            continue
        for authority_ref in getattr(obj, "authority_snapshot_refs", ()):
            key = (
                authority_ref.authority_id,
                authority_ref.authority_version,
                authority_ref.authority_content_hash,
            )
            if key not in retained_authority_keys:
                requested_authorities[key] = authority_ref
    for key in sorted(requested_authorities):
        snapshot = runtime_authority_set.resolve_exact_runtime_authority(
            requested_authorities[key]
        )
        if snapshot is None:
            raise FinalOracleProducerError(
                "LiTS canonical empirical closure cannot resolve exact adopted "
                f"authority snapshot preimage: {key!r}"
            )
        full_objects.append(snapshot)
        retained_authority_keys.add(key)
    return full_objects


def _build_lits_canonical_empirical_closure(
    *,
    catalog: Any,
    result: Any,
    release: Any,
    runtime_authority_set: Any,
) -> Mapping[str, Any]:
    """Retain the current PRE553 empirical object ontology, not an ASTRA-shaped projection."""
    support_objects = [
        obj
        for obj in release.public_objects
        if getattr(obj, "schema_id", None) in {
            "AuthoritySnapshot",
            "EmpiricalUniverse",
            "SourceUniverseRelation",
        }
    ]
    representation_snapshot = lits_representation_authority_snapshot()
    full_objects = _retain_exact_runtime_authority_snapshots([
        *catalog.authorities,
        *catalog.predicates,
        *catalog.queries,
        *catalog.discovery_authorities,
        *result.executed_predicates,
        *result.executed_queries,
        *result.empirical_facts,
        *result.receipts,
        *support_objects,
        representation_snapshot,
    ], runtime_authority_set)
    full_documents = _canonical_public_object_documents(full_objects)
    fragments: dict[str, Any] = {}
    documents = [
        _pack_lits_canonical_preimage(doc, fragments)
        for doc in full_documents
    ]
    inventory = Counter(
        f"{doc['schema_id']}@{doc['schema_version']}" for doc in documents
    )
    facts = [
        doc for doc in documents
        if doc["schema_id"] == "EmpiricalFact"
    ]
    queries = [
        doc for doc in documents
        if doc["schema_id"] == "EmpiricalQuerySpec"
    ]
    predicates = [
        doc for doc in documents
        if doc["schema_id"] == "EmpiricalPredicate"
    ]
    authorities = [
        doc for doc in documents
        if doc["schema_id"] == "AuthoritySnapshot"
    ]
    discovery_authorities = [
        doc for doc in documents
        if doc["schema_id"] == "DiscoveryAuthority"
    ]
    discovery_receipts = [
        doc for doc in documents
        if doc["schema_id"] == "DiscoveryResultReceipt"
    ]
    universes = [
        doc for doc in documents
        if doc["schema_id"] == "EmpiricalUniverse"
    ]
    release_doc = _lits_c11_release_retention_document(release)
    body = canonicalize({
        "schema": LITS_CANONICAL_EMPIRICAL_CLOSURE_SCHEMA,
        "public_object_preimages": documents,
        "preimage_fragments": [
            {"fragment_hash": digest, "value": fragments[digest]}
            for digest in sorted(fragments)
        ],
        "inventory": dict(sorted(inventory.items())),
        "fact_refs": [
            {
                "kind": f"{doc['schema_id']}@{doc['schema_version']}",
                "object_id": doc["object_id"],
                "content_hash": doc["content_hash"],
            }
            for doc in facts
        ],
        "query_refs": [
            {
                "kind": f"{doc['schema_id']}@{doc['schema_version']}",
                "object_id": doc["object_id"],
                "content_hash": doc["content_hash"],
            }
            for doc in queries
        ],
        "predicate_refs": [
            {
                "kind": f"{doc['schema_id']}@{doc['schema_version']}",
                "object_id": doc["object_id"],
                "content_hash": doc["content_hash"],
            }
            for doc in predicates
        ],
        "authority_refs": [
            {
                "authority_id": doc["semantic_fields"]["authority_id"],
                "authority_version": doc["semantic_fields"]["authority_version"],
                "authority_content_hash": doc["semantic_fields"]["authority_content_hash"],
            }
            for doc in authorities
        ],
        "discovery_authority_refs": [
            {
                "kind": f"{doc['schema_id']}@{doc['schema_version']}",
                "object_id": doc["object_id"],
                "content_hash": doc["content_hash"],
            }
            for doc in discovery_authorities
        ],
        "discovery_result_receipt_refs": [
            {
                "kind": f"{doc['schema_id']}@{doc['schema_version']}",
                "object_id": doc["object_id"],
                "content_hash": doc["content_hash"],
            }
            for doc in discovery_receipts
        ],
        "empirical_universe_refs": [
            {
                "kind": f"{doc['schema_id']}@{doc['schema_version']}",
                "object_id": doc["object_id"],
                "content_hash": doc["content_hash"],
            }
            for doc in universes
        ],
        "representation_authority_ref": LITS_REPRESENTATION_AUTHORITY_REF.as_dict(),
        "representation_authority_material": LITS_REPRESENTATION_AUTHORITY_MATERIAL,
        "c11_release": release_doc,
        "structural_admission_object_count": sum(
            1 for doc in documents if doc["schema_id"] == "StructuralEmpiricalAdmission"
        ),
    })
    return {**body, "closure_identity": semantic_hash(body)}


def _validate_lits_canonical_empirical_closure(
    closure: Mapping[str, Any],
    *,
    candidate_rows: Sequence[Mapping[str, Any]],
    compact_facts: Sequence[Mapping[str, Any]],
    projection_and_release_refs: Mapping[str, Any],
) -> Mapping[str, int]:
    """Rehydrate every retained current object and prove 50/77 exact-ref closure."""
    from rawlsing_next.pre553_carrier_execution import materialize_public_object

    if not isinstance(closure, Mapping) or closure.get("schema") != LITS_CANONICAL_EMPIRICAL_CLOSURE_SCHEMA:
        raise FinalOracleProducerError("LiTS canonical empirical closure schema drift")
    body = {
        key: value for key, value in closure.items() if key != "closure_identity"
    }
    if closure.get("closure_identity") != semantic_hash(canonicalize(body)):
        raise FinalOracleProducerError("LiTS canonical empirical closure identity drift")
    docs = closure.get("public_object_preimages")
    if not isinstance(docs, Sequence) or isinstance(docs, (str, bytes)) or not docs:
        raise FinalOracleProducerError("LiTS canonical empirical object preimages are absent")

    fragments = _lits_preimage_fragment_map(closure)
    by_ref: dict[tuple[str, str, str], Any] = {}
    by_schema: Counter[str] = Counter()
    authority_refs: set[tuple[str, str, str]] = set()
    for packed_doc in docs:
        if not isinstance(packed_doc, Mapping):
            raise FinalOracleProducerError("LiTS canonical empirical object preimage is malformed")
        doc = _hydrate_lits_canonical_preimage(packed_doc, fragments)
        try:
            obj = materialize_public_object(doc)
        except Exception as exc:
            raise FinalOracleProducerError(
                f"LiTS canonical empirical object failed exact re-materialization: {exc}"
            ) from exc
        if canonicalize(obj.as_dict()) != canonicalize(doc):
            raise FinalOracleProducerError("LiTS canonical empirical object round-trip drift")
        key = _ref_key(obj.ref.as_dict())
        if key in by_ref:
            raise FinalOracleProducerError("LiTS canonical empirical closure contains duplicate exact ref")
        by_ref[key] = obj
        schema = f"{obj.schema_id}@{obj.schema_version}"
        by_schema[schema] += 1
        if obj.schema_id == "AuthoritySnapshot":
            authority_refs.add((
                obj.authority_ref.authority_id,
                obj.authority_ref.authority_version,
                obj.authority_ref.authority_content_hash,
            ))

    expected_inventory = dict(sorted(by_schema.items()))
    if canonicalize(closure.get("inventory")) != canonicalize(expected_inventory):
        raise FinalOracleProducerError("LiTS canonical empirical closure inventory drift")

    def exact_refs_for_schema(schema_id: str) -> list[Mapping[str, Any]]:
        return [
            {
                "kind": f"{obj.schema_id}@{obj.schema_version}",
                "object_id": obj.object_id,
                "content_hash": obj.content_hash,
            }
            for obj in by_ref.values()
            if obj.schema_id == schema_id
        ]

    for manifest_key, schema_id in (
        ("fact_refs", "EmpiricalFact"),
        ("query_refs", "EmpiricalQuerySpec"),
        ("predicate_refs", "EmpiricalPredicate"),
        ("discovery_authority_refs", "DiscoveryAuthority"),
        ("discovery_result_receipt_refs", "DiscoveryResultReceipt"),
        ("empirical_universe_refs", "EmpiricalUniverse"),
    ):
        if canonicalize(closure.get(manifest_key)) != canonicalize(exact_refs_for_schema(schema_id)):
            raise FinalOracleProducerError(
                f"LiTS canonical empirical {manifest_key} do not close over exact object preimages"
            )
    expected_authority_refs = [
        {
            "authority_id": obj.authority_id,
            "authority_version": obj.authority_version,
            "authority_content_hash": obj.authority_content_hash,
        }
        for obj in by_ref.values()
        if obj.schema_id == "AuthoritySnapshot"
    ]
    if canonicalize(closure.get("authority_refs")) != canonicalize(expected_authority_refs):
        raise FinalOracleProducerError(
            "LiTS canonical authority manifest does not close over exact snapshots"
        )
    if by_schema.get("EmpiricalFact@1.0.0") != 60:
        raise FinalOracleProducerError("LiTS canonical empirical closure must retain all 60 facts")
    if by_schema.get("DiscoveryResultReceipt@1.0.0") != LITS_CANDIDATE_COUNT:
        raise FinalOracleProducerError("LiTS canonical empirical closure must retain all 50 discovery receipts")
    if by_schema.get("StructuralEmpiricalAdmission@1.0.0", 0) != 0:
        raise FinalOracleProducerError("LiTS canonical empirical closure illegally contains structural admission")
    if closure.get("structural_admission_object_count") != 0:
        raise FinalOracleProducerError("LiTS canonical empirical closure structural-admission count drift")

    fact_keys = {
        key for key, obj in by_ref.items() if obj.schema_id == "EmpiricalFact"
    }
    compact_fact_keys = {_ref_key(row["ref"]) for row in compact_facts}
    if fact_keys != compact_fact_keys:
        raise FinalOracleProducerError("LiTS canonical fact preimages do not close over compact I03 manifest")

    query_keys = {
        key for key, obj in by_ref.items() if obj.schema_id == "EmpiricalQuerySpec"
    }
    predicate_keys = {
        key for key, obj in by_ref.items() if obj.schema_id == "EmpiricalPredicate"
    }
    receipt_identity_by_candidate: dict[str, Mapping[str, Any]] = {}
    receipt_fact_refs_by_candidate: dict[str, set[tuple[str, str, str]]] = {}
    for obj in by_ref.values():
        if obj.schema_id != "DiscoveryResultReceipt":
            continue
        identity = obj.candidate_identity
        candidate_hash = identity.get("candidate_hash") if isinstance(identity, Mapping) else None
        if not isinstance(candidate_hash, str) or len(candidate_hash) != 64:
            raise FinalOracleProducerError("LiTS retained discovery receipt candidate identity is malformed")
        if candidate_hash in receipt_identity_by_candidate:
            raise FinalOracleProducerError("LiTS retained discovery receipts duplicate candidate hash")
        receipt_identity_by_candidate[candidate_hash] = canonicalize(identity)
        receipt_fact_refs_by_candidate[candidate_hash] = {
            _ref_key(ref) for ref in obj.empirical_fact_refs
        }

    role_count = 0
    for row in candidate_rows:
        identity = row.get("semantic_fields", {}).get("candidate_identity")
        if not isinstance(identity, Mapping):
            raise FinalOracleProducerError("LiTS canonical closure candidate identity missing")
        candidate_hash = row.get("candidate_hash")
        if (
            not isinstance(candidate_hash, str)
            or canonicalize(receipt_identity_by_candidate.get(candidate_hash))
            != canonicalize(identity)
        ):
            raise FinalOracleProducerError("LiTS compact frontier identity differs from retained discovery receipt")
        compact_candidate_facts = {
            _ref_key(item.get("ref"))
            for item in row.get("semantic_fields", {}).get("constituent_fact_manifest", ())
            if isinstance(item, Mapping)
        }
        if compact_candidate_facts != receipt_fact_refs_by_candidate.get(candidate_hash):
            raise FinalOracleProducerError("LiTS compact candidate facts differ from retained discovery receipt")
        roles = identity.get("query_roles")
        if not isinstance(roles, Sequence) or isinstance(roles, (str, bytes)):
            raise FinalOracleProducerError("LiTS canonical closure query roles malformed")
        for role in roles:
            if not isinstance(role, Mapping):
                raise FinalOracleProducerError("LiTS canonical closure role binding malformed")
            qref = role.get("query_ref")
            pref = role.get("predicate_ref")
            qkey = _ref_key(qref)
            pkey = _ref_key(pref)
            if qkey not in query_keys or pkey not in predicate_keys:
                raise FinalOracleProducerError("LiTS role predicate/query preimage substitution or omission")
            query = by_ref[qkey]
            if _ref_key(query.condition_predicate_ref) != pkey:
                raise FinalOracleProducerError("LiTS role query/predicate binding mismatch")
            role_count += 1
    if len(candidate_rows) != LITS_CANDIDATE_COUNT or role_count != LITS_QUERY_ROLE_COUNT:
        raise FinalOracleProducerError("LiTS canonical empirical closure does not close over 50/77 frontier")

    for key in fact_keys:
        fact = by_ref[key]
        qkey = _ref_key(fact.empirical_query_spec_ref)
        pkey = _ref_key(fact.condition_predicate_ref)
        if qkey not in query_keys or pkey not in predicate_keys:
            raise FinalOracleProducerError("LiTS fact lost exact query/predicate preimage")
        query = by_ref[qkey]
        if _ref_key(query.condition_predicate_ref) != pkey:
            raise FinalOracleProducerError("LiTS fact/query/predicate closure mismatch")

    for obj in by_ref.values():
        if obj.schema_id == "AuthoritySnapshot":
            continue
        for auth in obj.authority_snapshot_refs:
            key = (
                auth.authority_id,
                auth.authority_version,
                auth.authority_content_hash,
            )
            if key not in authority_refs:
                raise FinalOracleProducerError("LiTS canonical empirical closure lost authority snapshot preimage")

    representation_material = closure.get("representation_authority_material")
    if (
        not isinstance(representation_material, Mapping)
        or semantic_hash(representation_material)
        != LITS_REPRESENTATION_AUTHORITY_REF.authority_content_hash
        or closure.get("representation_authority_ref")
        != LITS_REPRESENTATION_AUTHORITY_REF.as_dict()
    ):
        raise FinalOracleProducerError("LiTS representation authority retention drift")

    release_doc = closure.get("c11_release")
    if not isinstance(release_doc, Mapping) or release_doc.get("schema") != LITS_C11_RELEASE_RETENTION_SCHEMA:
        raise FinalOracleProducerError("LiTS retained C11 release identity document missing")
    replay = release_doc.get("replay_manifest")
    if not isinstance(replay, Mapping):
        raise FinalOracleProducerError("LiTS retained C11 replay manifest missing")
    replay_projection = {
        key: replay.get(key)
        for key in ("record_family", "record_version", "semantic_fields")
    }
    if semantic_hash(replay_projection) != replay.get("content_hash"):
        raise FinalOracleProducerError("LiTS retained C11 replay preimage/hash drift")
    if _ref_key(release_doc.get("replay_ref"))[2] != replay.get("content_hash"):
        raise FinalOracleProducerError("LiTS retained C11 replay ref drift")
    release_refs = projection_and_release_refs.get("release_refs")
    if (
        not isinstance(release_refs, Sequence)
        or isinstance(release_refs, (str, bytes))
        or len(release_refs) != 1
        or canonicalize(release_doc.get("release_ref")) != canonicalize(release_refs[0])
        or release_doc.get("semantic_release_hash") != release_refs[0].get("content_hash")
        or projection_and_release_refs.get("c11_release_identity")
        != release_doc.get("semantic_release_hash")
        or projection_and_release_refs.get("c11_replay_identity")
        != release_doc.get("replay_ref", {}).get("content_hash")
    ):
        raise FinalOracleProducerError("LiTS retained C11 release/replay identity drift")

    return expected_inventory


def _load_accepted_r1m(path: Path) -> Mapping[str, Any]:
    doc = _load_json(path)
    if doc.get("schema") != R1M_SCHEMA or doc.get("source") != "WVS7":
        raise FinalOracleProducerError("accepted R1M WVS wrapper schema/source drift")
    if doc.get("status") != "PASS__FROZEN_BEFORE_CANDIDATE_EXECUTION":
        raise FinalOracleProducerError("accepted R1M WVS wrapper is not frozen PASS")
    if doc.get("successor_discovery_authority") != SUCCESSOR_DISCOVERY_AUTHORITY:
        raise FinalOracleProducerError("R1M successor DiscoveryAuthority drift")
    if doc.get("successor_lock2") != SUCCESSOR_LOCK2:
        raise FinalOracleProducerError("R1M successor Lock2 drift")
    if doc.get("oracle_identity_sha256") != R1M_ORACLE_IDENTITY:
        raise FinalOracleProducerError("R1M accepted wrapper identity drift")
    if doc.get("truth_payload_identity") != R1M_TRUTH_IDENTITY:
        raise FinalOracleProducerError("R1M accepted truth identity drift")
    _check_zero_candidate_provenance(doc, "R1M wrapper")
    freeze = doc.get("freeze_receipt")
    if not isinstance(freeze, Mapping):
        raise FinalOracleProducerError("R1M freeze receipt missing")
    _check_zero_candidate_provenance(freeze, "R1M freeze receipt")

    body = {
        key: value
        for key, value in doc.items()
        if key not in {"oracle_identity_sha256", "freeze_receipt"}
    }
    if semantic_hash(canonicalize(body)) != R1M_ORACLE_IDENTITY:
        raise FinalOracleProducerError("R1M wrapper semantic identity mismatch")
    truth = doc.get("truth_payload")
    if not isinstance(truth, Mapping) or truth.get("schema") != R1M_TRUTH_SCHEMA:
        raise FinalOracleProducerError("R1M truth payload schema drift")
    if semantic_hash(canonicalize(truth)) != R1M_TRUTH_IDENTITY:
        raise FinalOracleProducerError("R1M truth payload semantic identity mismatch")
    source = truth.get("source_identity")
    if source != {
        "source": "WVS7",
        "sha256": WVS7_SOURCE_SHA256,
        "rows": WVS_ROWS,
        "variables": WVS_VARIABLES,
    }:
        raise FinalOracleProducerError("R1M WVS source identity drift")
    return doc


def _ref_key(ref: Mapping[str, Any]) -> tuple[str, str, str]:
    if not isinstance(ref, Mapping):
        raise FinalOracleProducerError("exact ref must be a mapping")
    key = (ref.get("kind"), ref.get("object_id"), ref.get("content_hash"))
    if any(not isinstance(value, str) or not value for value in key):
        raise FinalOracleProducerError("exact ref is malformed")
    return key


def _standardize_r1m_candidate_rows(truth: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    """Map R1M I05 rows into the exact live T5 observation row shape."""
    raw_rows = truth.get("expected_fact_manifest")
    frontier = truth.get("frontier_manifest")
    constituent = truth.get("constituent_i03_fact_manifest")
    if not isinstance(raw_rows, Sequence) or isinstance(raw_rows, (str, bytes)):
        raise FinalOracleProducerError("R1M expected fact manifest missing")
    if not isinstance(frontier, Mapping):
        raise FinalOracleProducerError("R1M frontier manifest missing")
    if not isinstance(constituent, Sequence) or isinstance(constituent, (str, bytes)):
        raise FinalOracleProducerError("R1M constituent I03 fact manifest missing")

    rows = []
    observed_global = {}
    for index, raw in enumerate(raw_rows):
        if not isinstance(raw, Mapping):
            raise FinalOracleProducerError(f"R1M candidate row {index} malformed")
        identity = raw.get("candidate_identity")
        support = raw.get("support_uncertainty_state")
        refs = raw.get("empirical_fact_refs")
        if not isinstance(identity, Mapping) or not isinstance(support, Mapping):
            raise FinalOracleProducerError("R1M candidate identity/support state missing")
        if not isinstance(refs, Sequence) or isinstance(refs, (str, bytes)):
            raise FinalOracleProducerError("R1M candidate empirical fact refs missing")
        states = support.get("fact_states")
        if not isinstance(states, Sequence) or isinstance(states, (str, bytes)):
            raise FinalOracleProducerError("R1M candidate fact states missing")
        if len(refs) != len(states):
            raise FinalOracleProducerError("R1M fact refs/states cardinality mismatch")
        facts = []
        for ref, state in zip(refs, states):
            if not isinstance(state, str) or not state:
                raise FinalOracleProducerError("R1M constituent I03 typed state missing")
            key = _ref_key(ref)
            item = {"ref": canonicalize(ref), "typed_state": state}
            prior = observed_global.get(key)
            if prior is not None and canonicalize(prior) != canonicalize(item):
                raise FinalOracleProducerError("R1M constituent I03 fact state contradiction")
            observed_global[key] = item
            facts.append((key, item))
        facts = [item for _key, item in sorted(facts, key=lambda pair: pair[0])]
        candidate_hash = identity.get("candidate_hash")
        if not isinstance(candidate_hash, str) or len(candidate_hash) != 64:
            raise FinalOracleProducerError("R1M candidate hash missing")
        if not isinstance(raw.get("typed_state"), str):
            raise FinalOracleProducerError("R1M candidate typed state missing")
        replay_ref = raw.get("replay_ref")
        _ref_key(replay_ref)
        rows.append({
            "candidate_hash": candidate_hash,
            "typed_state": raw["typed_state"],
            "semantic_fields": {
                "candidate_identity": canonicalize(identity),
                "constituent_fact_manifest": facts,
                "coverage_state": raw.get("coverage_state"),
                "support_uncertainty_state": canonicalize(support),
                "replay_ref": canonicalize(replay_ref),
            },
        })

    frontier_hashes = frontier.get("ordered_candidate_hashes")
    if [row["candidate_hash"] for row in rows] != list(frontier_hashes or ()):
        raise FinalOracleProducerError("R1M candidate rows do not align with exact frontier order")
    expected_global = {_ref_key(ref) for ref in constituent}
    if set(observed_global) != expected_global:
        raise FinalOracleProducerError("R1M candidate rows do not close over constituent I03 facts")
    return canonicalize(rows)


def _assert_live_successor_oracle_law() -> None:
    expected = {
        "WVS7_DISCOVERY_AUTHORITY": SUCCESSOR_DISCOVERY_AUTHORITY,
        "WVS7_LOCK2_IDENTITY": SUCCESSOR_LOCK2,
        "WVS7_LOCK2_REPLAY_IDENTITY": SUCCESSOR_LOCK2_REPLAY,
    }
    for name, value in expected.items():
        if getattr(oracle_mod, name) != value:
            raise FinalOracleProducerError(
                f"live standard oracle law has not been rebound to accepted successor: {name}"
            )


def standardize_wvs_r1m_oracle(
    *, r1m_path: Path, output_path: Path, freeze_sequence: int = 30
) -> Mapping[str, Any]:
    """Source-free R1M successor oracle -> standard live T3/T5 oracle."""
    doc = _load_accepted_r1m(Path(r1m_path))
    truth = doc["truth_payload"]
    court = truth["court_constitution_refs"]
    if court.get("successor_discovery_authority") != SUCCESSOR_DISCOVERY_AUTHORITY:
        raise FinalOracleProducerError("R1M truth successor DiscoveryAuthority drift")
    if court.get("successor_lock2_hash") != SUCCESSOR_LOCK2:
        raise FinalOracleProducerError("R1M truth successor Lock2 drift")
    if court.get("successor_lock2_replay_hash") != SUCCESSOR_LOCK2_REPLAY:
        raise FinalOracleProducerError("R1M truth successor Lock2 replay drift")

    authority_identity = canonicalize(court)
    workload_identity = canonicalize(truth["frontier_manifest"])
    standard_court = {
        "frozen_authority_identity": authority_identity,
        "frozen_workload_identity": workload_identity,
        "lock2_hash": court["successor_lock2_hash"],
        "lock2_replay_hash": court["successor_lock2_replay_hash"],
        "discovery_authority": court["successor_discovery_authority"],
        "empirical_universe": court["empirical_universe"],
        "risk_set": court["risk_set"],
        "measure_basis": court["measure_basis"],
    }
    material = {
        "contract": WVS_MATERIALIZER_CONTRACT,
        "source_identity": canonicalize(truth["source_identity"]),
        "court_constitution_refs": canonicalize(standard_court),
        "semantic_authority_closure": canonicalize(truth["semantic_authority_closure"]),
        "projection_and_release_refs": canonicalize(truth["projection_and_release_refs"]),
        "frontier_manifest": canonicalize(truth["frontier_manifest"]),
        "expected_fact_manifest": _standardize_r1m_candidate_rows(truth),
        "expected_learned_product": canonicalize(truth["expected_learned_product"]),
        "replay_manifest": canonicalize(truth["replay_manifest"]),
        "exact_ref_manifest": canonicalize(truth["exact_ref_manifest"]),
        "oracle_build_provenance": canonicalize(truth["oracle_build_provenance"]),
    }
    _assert_live_successor_oracle_law()
    frozen = freeze_wvs7_oracle_from_common_material(
        material=material,
        freeze=FreezeContext(freeze_sequence=freeze_sequence),
    )
    identity = verify_frozen_oracle(frozen)
    if frozen.get("schema") != ORACLE_SCHEMA or frozen.get("source") != "WVS7":
        raise FinalOracleProducerError("standardized WVS oracle schema/source drift")
    output_sha = _write_json(Path(output_path), frozen)
    return {
        "schema": PRODUCER_SCHEMA,
        "operation": "STANDARDIZE_WVS_R1M_SUCCESSOR_ORACLE",
        "status": "PASS",
        "source": "WVS7",
        "source_free": True,
        "r1m_oracle_identity": R1M_ORACLE_IDENTITY,
        "r1m_truth_payload_identity": R1M_TRUTH_IDENTITY,
        "standard_oracle_identity_sha256": identity,
        "standard_oracle_document_sha256": output_sha,
        "output_path": str(Path(output_path)),
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
    }


def _neutral_lits_authority_identity() -> Mapping[str, Any]:
    return {
        "runtime_catalog_identity": LITS_RUNTIME_CATALOG,
        "active_binding": LITS_ACTIVE_BINDING,
        "runtime_release": LITS_RUNTIME_RELEASE,
        "representation_authority": LITS_REPRESENTATION_AUTHORITY_REF.authority_content_hash,
    }


def _lits_accepted_legacy_projection(
    *, projection: Any, repo_root: Path, neutral_root: Path, backend: Any,
    legacy_module: Any | None = None,
):
    """Load the pinned owner and rebind only its exact historical physical keys."""
    if legacy_module is None:
        legacy_path = backend._deploy(
            repo_root,
            neutral_root / "legacy_facade",
            LITS_LEGACY_FACADE_COMMIT,
            LITS_LEGACY_FACADE_PATH,
            LITS_LEGACY_FACADE_BLOB,
        )
        legacy = backend._load(legacy_path, "_fiabc_lits_i_accepted_legacy_facade")
    else:
        legacy = legacy_module
        if not callable(getattr(legacy, "physical_value_binding_key", None)) or not callable(
            getattr(legacy, "build_source_backed_c11_repository", None)
        ):
            raise FinalOracleProducerError("exact legacy owner module lacks its frozen C11 surface")
        owner_path = getattr(legacy, "__file__", None)
        if not isinstance(owner_path, str) or not Path(owner_path).is_file():
            raise FinalOracleProducerError("exact legacy owner module has no deployed source file")
        owner_bytes = Path(owner_path).read_bytes()
        owner_blob = hashlib.sha1(
            b"blob " + str(len(owner_bytes)).encode("ascii") + b"\0" + owner_bytes
        ).hexdigest()
        if owner_blob != LITS_LEGACY_FACADE_BLOB:
            raise FinalOracleProducerError("supplied legacy owner module blob differs from the frozen owner")
    observed = PhysicalMissingState.OBSERVED_STORAGE_VALUE
    system_missing = PhysicalMissingState.SYSTEM_MISSING
    exact_current_to_legacy = {
        current_typed_physical_value_binding_key(Decimal(code), observed):
            legacy.physical_value_binding_key(Decimal(code), observed)
        for code in range(1, 8)
    }
    current_missing = current_typed_physical_value_binding_key(None, system_missing)
    legacy_missing = legacy.physical_value_binding_key(None, system_missing)

    response_slots = []
    observed_response_keys = set()
    observed_response_slots = set()
    for slot in projection.response_slots:
        slot_key = slot.slot.key
        if LITS_TARGET_VARIABLES.get(slot_key[1]) != slot_key[0]:
            raise FinalOracleProducerError("LiTS legacy response slot outside exact authority")
        observed_response_slots.add(slot_key)
        values = []
        for rule in slot.values:
            if rule.physical_key == current_missing:
                rebound = legacy_missing
            else:
                rebound = exact_current_to_legacy.get(rule.physical_key)
                if rebound is None:
                    raise FinalOracleProducerError(
                        "LiTS legacy response rule outside exact representation authority"
                    )
                observed_response_keys.add(rule.physical_key)
            values.append(dataclasses.replace(rule, physical_key=rebound))
        response_slots.append(dataclasses.replace(slot, values=tuple(values)))
    expected_slots = {(ordinal, name) for name, ordinal in LITS_TARGET_VARIABLES.items()}
    if observed_response_slots != expected_slots:
        raise FinalOracleProducerError("LiTS exact legacy response slot closure drift")
    if observed_response_keys != set(exact_current_to_legacy):
        raise FinalOracleProducerError("LiTS exact legacy response key closure drift")

    coordinate_slots = []
    for slot in projection.coordinate_slots:
        values = []
        for rule in slot.values:
            if rule.physical_key != current_missing:
                raise FinalOracleProducerError(
                    "LiTS legacy coordinate rule outside exact system-missing binding"
                )
            values.append(dataclasses.replace(rule, physical_key=legacy_missing))
        coordinate_slots.append(dataclasses.replace(slot, values=tuple(values)))
    if projection.weight_slots:
        raise FinalOracleProducerError("LiTS accepted projection unexpectedly contains weights")

    rebound_projection = dataclasses.replace(
        projection,
        response_slots=tuple(response_slots),
        coordinate_slots=tuple(coordinate_slots),
    )
    legacy_fields = {field.name for field in dataclasses.fields(legacy.GovernedC11Projection)}
    legacy_projection = legacy.GovernedC11Projection(**{
        field.name: getattr(rebound_projection, field.name)
        for field in dataclasses.fields(rebound_projection)
        if field.name in legacy_fields
    })
    if legacy_projection.cache_identity != LITS_PROJECTION_IDENTITY:
        raise FinalOracleProducerError("LiTS accepted legacy projection identity drift")
    return legacy, legacy_projection


def _lits_accepted_legacy_base_candidate(
    *,
    incidence: Any,
    projection: Any,
    repo_root: Path,
    neutral_root: Path,
    backend: Any,
    banked: Any,
):
    """Replay and verify the exact accepted base candidate from one incidence."""
    legacy, legacy_projection = _lits_accepted_legacy_projection(
        projection=projection,
        repo_root=repo_root,
        neutral_root=neutral_root,
        backend=backend,
    )
    stream = legacy.ExactPhysicalCellStream(
        source_sha256=incidence.source_sha256,
        row_count=incidence.row_count,
        cell_iter_factory=lambda: (
            banked.exact_cell(
                authorized_lits_replay_cell(
                    source_sha256=incidence.source_sha256,
                    cell=cell,
                )
            )
            for cell in incidence.iter_cells(batch_size=20_000)
        ),
        transport_identity=(
            "FIABC_LITS_I_AUTHORIZED_ACCEPTED_REPLAY__"
            + LITS_REPRESENTATION_AUTHORITY_REF.authority_content_hash
        ),
    )
    base_candidate = legacy.project_c11_candidate_from_physical_cells(
        source_sha256=incidence.source_sha256,
        row_count=incidence.row_count,
        cells=stream.iter_cells(),
        projection=legacy_projection,
    )
    if (
        base_candidate.candidate_replay_manifest.semantic_projection_hash
        != LITS_BASE_CANDIDATE_PROJECTION
    ):
        raise FinalOracleProducerError("LiTS accepted base candidate projection identity drift")
    base_release = legacy.validate_c11_source_release(base_candidate)
    if base_release.release_ref.content_hash != LITS_BASE_C11_RELEASE:
        raise FinalOracleProducerError("LiTS accepted base C11 release identity drift")
    if base_release.replay_manifest.ref.content_hash != LITS_BASE_C11_REPLAY:
        raise FinalOracleProducerError("LiTS accepted base C11 replay identity drift")
    return legacy, legacy_projection, base_candidate


def _lits_accepted_legacy_repository(
    *,
    incidence: Any,
    projection: Any,
    repo_root: Path,
    neutral_root: Path,
    backend: Any,
    banked: Any,
):
    """Replay the exact adopted R5B successor release from one decoded incidence."""
    legacy, legacy_projection, base_candidate = _lits_accepted_legacy_base_candidate(
        incidence=incidence,
        projection=projection,
        repo_root=repo_root,
        neutral_root=neutral_root,
        backend=backend,
        banked=banked,
    )

    r5b_root = neutral_root / "accepted_r5b_successor"
    deployed = {
        path: backend._deploy(
            repo_root, r5b_root, LITS_R5B_COMMIT, path, expected_blob
        )
        for path, expected_blob in LITS_R5B_BLOBS.items()
    }
    r5b = backend._load(deployed[LITS_R5B_DRIVER], "_fiabc_lits_i_exact_r5b_successor")
    r5b.verify_frozen_support()
    f02 = r5b.load_module(r5b.F02, "_fiabc_lits_i_exact_r5b_f02")
    closure = f02.build_selector_closure()
    if closure["new_release_ref"]["content_hash"] != r5b.FROZEN_F02_SCOPE_HASH:
        raise FinalOracleProducerError("LiTS frozen F02 successor scope drift")
    selector_scan = r5b.f02_source_scan(incidence, f02)

    # R5B was adopted against the pinned legacy physical-key representation.
    # Rebind only its facade constructors/functions to those exact deployed bytes.
    for name in (
        "OccurrenceRule", "PhysicalSlot", "ResponseSlotRule", "ResponseValueRule",
        "physical_value_binding_key", "project_c11_candidate_from_physical_cells",
    ):
        setattr(r5b, name, getattr(legacy, name))

    _package, _ledger, slots = banked.read_banked_authority()
    (
        extension_projection,
        extension_questions,
        extension_routing,
        all_authorities,
        extension_auth_refs,
        _extension_projection_material,
    ) = r5b.build_extension_projection(
        base_projection=legacy_projection,
        base_context={},
        slots=slots,
        closure=closure,
        f02_module=f02,
    )
    selected = r5b.selected_incidence(incidence, ("country", "q310", "q311"))
    extension_candidate = legacy.project_c11_candidate_from_physical_cells(
        source_sha256=incidence.source_sha256,
        row_count=incidence.row_count,
        cells=r5b.exact_cells(selected, banked),
        projection=extension_projection,
    )
    successor = r5b.build_successor_candidate(
        base_candidate=base_candidate,
        base_projection=legacy_projection,
        extension_candidate=extension_candidate,
        extension_questions=extension_questions,
        extension_routing=extension_routing,
        all_authorities=all_authorities,
        f02_replay_authority_ref=extension_auth_refs["replay"],
        f02_module=f02,
    )
    release = r5b.validate_c11_source_release(successor)
    repository = r5b.C11Repository((release,))
    if release.release_ref.content_hash != LITS_RUNTIME_RELEASE:
        raise FinalOracleProducerError("LiTS accepted successor C11 release identity drift")
    if release.replay_manifest.ref.content_hash != LITS_RUNTIME_REPLAY:
        raise FinalOracleProducerError("LiTS accepted successor replay identity drift")
    if successor.candidate_replay_manifest.semantic_projection_hash != LITS_RUNTIME_PROJECTION:
        raise FinalOracleProducerError("LiTS accepted successor projection identity drift")
    if repository.resolve_release_exact(release.release_ref).release_ref != release.release_ref:
        raise FinalOracleProducerError("LiTS successor release exact repository resolution failed")
    return repository, release, selector_scan


def _neutral_lits_material(
    *,
    source_path: Path,
    repo_root: Path,
    work_root: Path,
) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    """Execute the common LiTS semantic path without composing A/B/C."""
    from rawlsing_next.pre553_physical_decoder import decode_dta
    from rawlsing_next.pre553_carrier_execution import (
        CarrierNeutralResearchExecutor,
        RuntimeObjectCatalog,
        learned_empirical_execution_receipt,
    )
    from rawlsing_next.pre553_runtime_context import bind_runtime
    import rawlsing_next.ee_p2x_darwin_stage_backend as backend
    import rawlsing_next.fiabc_live_terminal_control as terminal

    source_path = Path(source_path).resolve()
    repo_root = Path(repo_root).resolve()
    work_root = Path(work_root).resolve()
    if not source_path.is_file():
        raise FinalOracleProducerError("LiTS exact source file is required")
    _reject_candidate_owned_path(source_path, work_root, "LiTS source")
    neutral_root = work_root / "court" / "oracle_producers" / "LITS_I"
    _reject_candidate_owned_path(neutral_root, work_root, "LiTS neutral producer root")
    neutral_root.mkdir(parents=True, exist_ok=True)

    incidence = decode_dta(
        source_path,
        encoding="latin1",
        expected_source_sha256=LITS_SOURCE_SHA256,
    )
    if incidence.source_sha256 != LITS_SOURCE_SHA256:
        raise FinalOracleProducerError("LiTS decoder source identity drift")
    if incidence.row_count != LITS_ROWS or len(incidence.variables) != LITS_VARIABLES:
        raise FinalOracleProducerError("LiTS decoder source shape drift")

    ctx = types.SimpleNamespace(work_root=neutral_root)
    services = types.SimpleNamespace(repo_root=repo_root)
    projection, _pctx, banked = backend._lits_projection(ctx, services, {}, incidence)
    runtime = backend._lits_runtime(ctx, services, projection)
    if (
        backend.R6O_RUNTIME_CATALOG != LITS_RUNTIME_CATALOG
        or backend.R6O_ACTIVE_BINDING != LITS_ACTIVE_BINDING
        or backend.R6O_RUNTIME_RELEASE != LITS_RUNTIME_RELEASE
    ):
        raise FinalOracleProducerError("LiTS accepted runtime identity constants drift")

    repository, release, selector_scan = _lits_accepted_legacy_repository(
        incidence=incidence,
        projection=projection,
        repo_root=repo_root,
        neutral_root=neutral_root,
        backend=backend,
        banked=banked,
    )
    catalog = RuntimeObjectCatalog.from_documents(
        authority_documents=runtime["authorities"],
        predicate_documents=runtime["predicates"],
        query_documents=runtime["queries"],
        discovery_authority_documents=runtime["discoveries"],
    )
    if catalog.receipt()["catalog_identity"] != LITS_RUNTIME_CATALOG:
        raise FinalOracleProducerError("LiTS current runtime catalog identity drift")
    executor = CarrierNeutralResearchExecutor(
        repository=repository,
        release_refs=(release.release_ref,),
        runtime_catalog=catalog,
    )
    discovery_refs = catalog.discovery_authority_refs
    if len(discovery_refs) != 1:
        raise FinalOracleProducerError("LiTS runtime must expose exactly one DiscoveryAuthority")
    with bind_runtime(
        runtime["runtime_authority_set"],
        repository=repository,
        runtime_catalog_identity=catalog.receipt()["catalog_identity"],
    ):
        result = executor.execute_i05(discovery_authority_ref=discovery_refs[0])
    execution_receipt = learned_empirical_execution_receipt(result)
    astra_empirical_summary = normalize_current_lits_summary(
        result=result,
        frontier_seal=LITS_FRONTIER_SEAL,
        selector_scan=selector_scan,
        logical_candidate_bindings=runtime["cross_schema_logical_candidate_bindings"],
    )

    ordered = sorted(
        result.receipts, key=lambda receipt: receipt.candidate_identity["candidate_hash"]
    )
    query_role_count = sum(
        len(receipt.candidate_identity["query_roles"]) for receipt in ordered
    )
    terminal_counts = dict(
        sorted(Counter(receipt.coverage_state for receipt in ordered).items())
    )
    facts = tuple(sorted(result.empirical_facts, key=lambda fact: fact.ref.key))
    precheck = {
        "schema": "FIABC_LITS_CURRENT_NEUTRAL_I05_PRECHECK@1.0.0",
        "candidate_count": result.candidate_count,
        "query_role_count": query_role_count,
        "coverage_state_counts": terminal_counts,
        "typed_state_counts": dict(
            sorted(Counter(receipt.typed_state for receipt in ordered).items())
        ),
        "empirical_fact_state_counts": dict(
            sorted(Counter(fact.typed_state for fact in facts).items())
        ),
        "empirical_facts": [
            {
                "fact_ref": fact.ref.as_dict(),
                "typed_state": fact.typed_state,
                "empirical_query_spec_ref": canonicalize(fact.empirical_query_spec_ref),
                "condition_predicate_ref": canonicalize(fact.condition_predicate_ref),
                "raw_denominator_support": fact.raw_denominator_support,
                "raw_resolved_target_support": fact.semantic_fields.get(
                    "raw_resolved_target_support"
                ),
                "execution_detail": fact.semantic_fields.get("execution_detail"),
                "p02_failure_state": fact.semantic_fields.get("p02_failure_state"),
                "target_topology": canonicalize({
                    key: fact.target_topology[key]
                    for key in (
                        "arity",
                        "joint_order_semantics",
                        "target_domain_identity",
                        "requested_target_arity_and_topology",
                        "p02_failure_state",
                    )
                    if key in fact.target_topology
                }),
            }
            for fact in facts
        ],
        "by_rule": [
            {
                "candidate_hash": receipt.candidate_identity["candidate_hash"],
                "rule_id": receipt.candidate_identity["rule_id"],
                "validation": canonicalize(receipt.candidate_identity["validation"]),
                "coverage_state": receipt.coverage_state,
                "typed_state": receipt.typed_state,
            }
            for receipt in ordered
        ],
        "current_semantic_replay_identity": result.replay_ref.content_hash,
        "current_execution_identity": execution_receipt["execution_identity"],
        "candidate_processes_started": 0,
    }
    _write_json(neutral_root / "current_i05_precheck.json", precheck)
    learned = _bind_current_lits_execution_to_astra(
        execution_receipt=execution_receipt,
        semantic_replay_identity=result.replay_ref.content_hash,
        terminal_counts=terminal_counts,
        candidate_count=result.candidate_count,
        query_role_count=query_role_count,
    )

    binding = types.SimpleNamespace(executor=executor)
    state = {"bindings": {"projection_identity": projection.cache_identity}}
    projection_refs = terminal._projection_refs("LITS_I", binding, state)
    candidate_rows, constituent_facts, i03_closure = terminal._constituent_i03(binding, result)
    canonical_empirical_closure = _build_lits_canonical_empirical_closure(
        catalog=catalog,
        result=result,
        release=release,
        runtime_authority_set=runtime["runtime_authority_set"],
    )

    hashes = [receipt.candidate_identity["candidate_hash"] for receipt in ordered]
    frontier = {
        "candidate_count": result.candidate_count,
        "query_role_count": query_role_count,
        "frontier_seal": LITS_FRONTIER_SEAL,
        "ordered_candidate_hashes": hashes,
    }
    authorities = [authority.ref.as_dict() for authority in catalog.authorities]
    exact_refs = terminal._unique_refs([
        *authorities,
        *[predicate.ref.as_dict() for predicate in catalog.predicates],
        *[query.ref.as_dict() for query in catalog.queries],
        *[predicate.ref.as_dict() for predicate in result.executed_predicates],
        *[query.ref.as_dict() for query in result.executed_queries],
        *[authority.ref.as_dict() for authority in catalog.discovery_authorities],
        *[ref.as_dict() for ref in executor.release_refs],
        result.discovery_authority_ref.as_dict(),
        result.candidate_grammar_ref.as_dict(),
        result.evaluated_frontier_ref.as_dict(),
        result.replay_ref.as_dict(),
        *[ref.as_dict() for ref in result.empirical_fact_refs],
        *[receipt.ref.as_dict() for receipt in result.receipts],
    ])
    replay_manifest = {
        "i05_replay_ref": result.replay_ref.as_dict(),
        "constituent_i03_closure_identity": i03_closure,
        "dependency_root": semantic_hash(exact_refs),
    }
    authority_identity = _neutral_lits_authority_identity()
    workload_identity = canonicalize(frontier)
    material = {
        "source_identity": {
            "source": "LITS_I",
            "sha256": LITS_SOURCE_SHA256,
            "rows": LITS_ROWS,
            "variables": LITS_VARIABLES,
        },
        "court_constitution_refs": {
            "frozen_authority_identity": canonicalize(authority_identity),
            "frozen_workload_identity": workload_identity,
        },
        "semantic_authority_closure": canonicalize(authorities),
        "projection_and_release_refs": canonicalize(projection_refs),
        "frontier_manifest": workload_identity,
        "comparison_fact_manifest": canonicalize(candidate_rows),
        "expected_learned_product": canonicalize(learned),
        "replay_manifest": canonicalize(replay_manifest),
        "exact_ref_manifest": canonicalize(exact_refs),
        "constituent_i03_fact_manifest": canonicalize(constituent_facts),
        "constituent_i03_closure_identity": i03_closure,
        "canonical_empirical_object_closure": canonical_empirical_closure,
        # Historical ASTRA is retained only as an audit/regression projection.
        # It is not the canonical current empirical storage ontology.
        "astra_shaped_empirical_summary": astra_empirical_summary,
    }
    audit = {
        "runtime_catalog_identity": catalog.receipt()["catalog_identity"],
        "common_execution_binding": executor.binding_receipt(),
        "current_i05_execution_identity": execution_receipt["execution_identity"],
        "current_i05_replay_identity": result.replay_ref.content_hash,
        "astra_shaped_empirical_summary_identity": semantic_hash(astra_empirical_summary),
        "astra_projection_role": "OPTIONAL_HISTORICAL_REGRESSION__NOT_CANONICAL_CURRENT_STORAGE",
        "canonical_empirical_closure_identity": canonical_empirical_closure["closure_identity"],
        "canonical_empirical_object_inventory": canonical_empirical_closure["inventory"],
        "constituent_i03_fact_count": len(constituent_facts),
        "constituent_i03_closure_identity": i03_closure,
        "exact_ref_count": len(exact_refs),
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
        "representation_authority": LITS_REPRESENTATION_AUTHORITY_REF.as_dict(),
        "accepted_legacy_facade_blob": LITS_LEGACY_FACADE_BLOB,
    }
    return material, audit, execution_receipt, precheck



def _validate_lits_materialization_checkpoint_body(
    body: Mapping[str, Any],
) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any], Mapping[str, Any]]:
    if body.get("schema") in {
        LITS_LEGACY_MATERIALIZATION_CHECKPOINT_SCHEMA,
        LITS_PARTIAL_MATERIALIZATION_CHECKPOINT_SCHEMA,
    }:
        raise FinalOracleProducerError(
            "legacy LiTS checkpoint lacks complete canonical current empirical object preimages; fresh source-backed I05 required"
        )
    if body.get("schema") != LITS_MATERIALIZATION_CHECKPOINT_SCHEMA:
        raise FinalOracleProducerError("LiTS materialization checkpoint schema drift")
    material = body.get("material")
    audit = body.get("audit")
    execution = body.get("execution_receipt")
    precheck = body.get("precheck")
    if not all(isinstance(value, Mapping) for value in (material, audit, execution, precheck)):
        raise FinalOracleProducerError("LiTS materialization checkpoint body is incomplete")

    expected_source = {
        "source": "LITS_I",
        "sha256": LITS_SOURCE_SHA256,
        "rows": LITS_ROWS,
        "variables": LITS_VARIABLES,
    }
    if body.get("source_identity") != expected_source or material.get("source_identity") != expected_source:
        raise FinalOracleProducerError("LiTS checkpoint source identity drift")

    frontier = material.get("frontier_manifest")
    rows = material.get("comparison_fact_manifest")
    if not isinstance(frontier, Mapping) or not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
        raise FinalOracleProducerError("LiTS checkpoint frontier material is incomplete")
    hashes = frontier.get("ordered_candidate_hashes")
    if (
        frontier.get("candidate_count") != LITS_CANDIDATE_COUNT
        or frontier.get("query_role_count") != LITS_QUERY_ROLE_COUNT
        or frontier.get("frontier_seal") != LITS_FRONTIER_SEAL
        or not isinstance(hashes, Sequence)
        or isinstance(hashes, (str, bytes))
        or len(hashes) != LITS_CANDIDATE_COUNT
        or len(rows) != LITS_CANDIDATE_COUNT
    ):
        raise FinalOracleProducerError("LiTS checkpoint frontier cardinality or seal drift")

    observed_hashes = []
    role_count = 0
    coverage_counts: Counter[str] = Counter()
    typed_counts: Counter[str] = Counter()
    for row in rows:
        if not isinstance(row, Mapping):
            raise FinalOracleProducerError("LiTS checkpoint candidate row is malformed")
        candidate_hash = row.get("candidate_hash")
        if not isinstance(candidate_hash, str) or len(candidate_hash) != 64:
            raise FinalOracleProducerError("LiTS checkpoint candidate hash is malformed")
        semantic_fields = row.get("semantic_fields")
        if not isinstance(semantic_fields, Mapping):
            raise FinalOracleProducerError("LiTS checkpoint candidate semantic fields are malformed")
        identity = semantic_fields.get("candidate_identity")
        if not isinstance(identity, Mapping) or identity.get("candidate_hash") != candidate_hash:
            raise FinalOracleProducerError("LiTS checkpoint candidate identity/hash mismatch")
        roles = identity.get("query_roles")
        if not isinstance(roles, Sequence) or isinstance(roles, (str, bytes)):
            raise FinalOracleProducerError("LiTS checkpoint candidate query roles are malformed")
        role_count += len(roles)
        coverage = semantic_fields.get("coverage_state")
        typed = row.get("typed_state")
        if not isinstance(coverage, str) or not isinstance(typed, str):
            raise FinalOracleProducerError("LiTS checkpoint candidate terminal is malformed")
        observed_hashes.append(candidate_hash)
        coverage_counts[coverage] += 1
        typed_counts[typed] += 1

    if observed_hashes != list(hashes) or role_count != LITS_QUERY_ROLE_COUNT:
        raise FinalOracleProducerError("LiTS checkpoint candidates do not close over frontier")
    if dict(sorted(coverage_counts.items())) != LITS_ACCEPTED_TERMINAL_COUNTS:
        raise FinalOracleProducerError("LiTS checkpoint coverage terminal drift")
    if dict(sorted(typed_counts.items())) != LITS_ACCEPTED_TYPED_TERMINAL_COUNTS:
        raise FinalOracleProducerError("LiTS checkpoint typed terminal drift")

    facts = material.get("constituent_i03_fact_manifest")
    if not isinstance(facts, Sequence) or isinstance(facts, (str, bytes)) or len(facts) != 60:
        raise FinalOracleProducerError("LiTS checkpoint retained I03 fact closure is incomplete")
    fact_counts = Counter(
        fact.get("typed_state") for fact in facts if isinstance(fact, Mapping)
    )
    if dict(sorted(fact_counts.items())) != {"SUPPORTED": 60}:
        raise FinalOracleProducerError("LiTS checkpoint retained I03 fact state drift")

    canonical_closure = material.get("canonical_empirical_object_closure")
    canonical_inventory = _validate_lits_canonical_empirical_closure(
        canonical_closure,
        candidate_rows=rows,
        compact_facts=facts,
        projection_and_release_refs=material.get("projection_and_release_refs", {}),
    )
    if audit.get("canonical_empirical_closure_identity") != canonical_closure.get("closure_identity"):
        raise FinalOracleProducerError("LiTS checkpoint canonical empirical closure audit identity drift")
    if canonicalize(audit.get("canonical_empirical_object_inventory")) != canonicalize(canonical_inventory):
        raise FinalOracleProducerError("LiTS checkpoint canonical empirical inventory audit drift")

    closure_facts: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    expected_by_rule = []
    for row in rows:
        fields = row["semantic_fields"]
        for fact in fields.get("constituent_fact_manifest", ()):
            if not isinstance(fact, Mapping):
                raise FinalOracleProducerError("LiTS checkpoint candidate fact preimage is malformed")
            key = _ref_key(fact.get("ref"))
            previous = closure_facts.setdefault(key, fact)
            if canonicalize(previous) != canonicalize(fact):
                raise FinalOracleProducerError("LiTS checkpoint fact preimages conflict")
        identity = fields["candidate_identity"]
        expected_by_rule.append({
            "candidate_hash": row["candidate_hash"],
            "rule_id": identity.get("rule_id"),
            "validation": canonicalize(identity.get("validation")),
            "coverage_state": fields["coverage_state"],
            "typed_state": row["typed_state"],
        })
    ordered_closure = [closure_facts[key] for key in sorted(closure_facts)]
    if canonicalize(ordered_closure) != canonicalize(facts):
        raise FinalOracleProducerError("LiTS checkpoint facts do not close over candidate preimages")
    closure_identity = semantic_hash({
        "candidate_fact_rows": rows,
        "constituent_fact_manifest": facts,
    })
    if (
        material.get("constituent_i03_closure_identity") != closure_identity
        or audit.get("constituent_i03_closure_identity") != closure_identity
    ):
        raise FinalOracleProducerError("LiTS checkpoint constituent-I03 closure identity drift")

    expected_precheck = {
        "schema": "FIABC_LITS_CURRENT_NEUTRAL_I05_PRECHECK@1.0.0",
        "candidate_count": LITS_CANDIDATE_COUNT,
        "query_role_count": LITS_QUERY_ROLE_COUNT,
        "coverage_state_counts": LITS_ACCEPTED_TERMINAL_COUNTS,
        "typed_state_counts": LITS_ACCEPTED_TYPED_TERMINAL_COUNTS,
        "empirical_fact_state_counts": {"SUPPORTED": 60},
        "candidate_processes_started": 0,
    }
    for key, value in expected_precheck.items():
        if canonicalize(precheck.get(key)) != canonicalize(value):
            raise FinalOracleProducerError(f"LiTS checkpoint precheck {key} drift")
    if canonicalize(precheck.get("by_rule")) != canonicalize(expected_by_rule):
        raise FinalOracleProducerError("LiTS checkpoint precheck candidate rows drift")
    precheck_facts = precheck.get("empirical_facts")
    if not isinstance(precheck_facts, Sequence) or isinstance(precheck_facts, (str, bytes)):
        raise FinalOracleProducerError("LiTS checkpoint precheck fact preimages are absent")
    expected_precheck_fact_refs = [
        {"fact_ref": fact["ref"], "typed_state": fact["typed_state"]}
        for fact in facts
    ]
    observed_precheck_fact_refs = [
        {"fact_ref": fact.get("fact_ref"), "typed_state": fact.get("typed_state")}
        for fact in precheck_facts
        if isinstance(fact, Mapping)
    ]
    if canonicalize(observed_precheck_fact_refs) != canonicalize(expected_precheck_fact_refs):
        raise FinalOracleProducerError("LiTS checkpoint precheck fact closure drift")
    if precheck.get("current_execution_identity") != execution.get("execution_identity"):
        raise FinalOracleProducerError("LiTS checkpoint precheck execution identity drift")
    if precheck.get("current_semantic_replay_identity") != material.get(
        "expected_learned_product", {}
    ).get("semantic_identity"):
        raise FinalOracleProducerError("LiTS checkpoint precheck semantic identity drift")

    execution_body = dict(execution)
    execution_identity = execution_body.pop("execution_identity", None)
    if (
        not isinstance(execution_identity, str)
        or len(execution_identity) != 64
        or semantic_hash(execution_body) != execution_identity
    ):
        raise FinalOracleProducerError("LiTS checkpoint I05 execution receipt identity drift")
    _check_zero_candidate_provenance(audit, "LiTS materialization checkpoint")
    if (
        audit.get("runtime_catalog_identity") != LITS_RUNTIME_CATALOG
        or audit.get("current_i05_execution_identity") != execution_identity
        or audit.get("constituent_i03_fact_count") != 60
        or audit.get("exact_ref_count") != len(material.get("exact_ref_manifest", ()))
        or audit.get("representation_authority")
        != LITS_REPRESENTATION_AUTHORITY_REF.as_dict()
        or audit.get("accepted_legacy_facade_blob") != LITS_LEGACY_FACADE_BLOB
    ):
        raise FinalOracleProducerError("LiTS checkpoint authority/audit identity drift")

    learned = material.get("expected_learned_product")
    if not isinstance(learned, Mapping):
        raise FinalOracleProducerError("LiTS checkpoint learned product is absent")
    rebuilt_learned = _bind_current_lits_execution_to_astra(
        execution_receipt=execution,
        semantic_replay_identity=learned.get("semantic_identity"),
        terminal_counts=LITS_ACCEPTED_TERMINAL_COUNTS,
        candidate_count=LITS_CANDIDATE_COUNT,
        query_role_count=LITS_QUERY_ROLE_COUNT,
    )
    if canonicalize(rebuilt_learned) != canonicalize(learned):
        raise FinalOracleProducerError("LiTS checkpoint learned product does not bind its I05 receipt")

    projection = material.get("projection_and_release_refs")
    if not isinstance(projection, Mapping) or projection.get("projection_identity") != LITS_PROJECTION_IDENTITY:
        raise FinalOracleProducerError("LiTS checkpoint projection identity drift")
    if (
        projection.get("c11_release_identity") != LITS_RUNTIME_RELEASE
        or projection.get("c11_replay_identity") != LITS_RUNTIME_REPLAY
    ):
        raise FinalOracleProducerError("LiTS checkpoint successor release/replay identity drift")

    # ASTRA is a bounded historical regression projection, not checkpoint ontology.
    summary = material.get("astra_shaped_empirical_summary")
    if summary is not None:
        if not isinstance(summary, Mapping):
            raise FinalOracleProducerError("LiTS ASTRA regression projection is malformed")
        if summary.get("schema") != "FIABC_LITS_ASTRA_SHAPED_EMPIRICAL_SUMMARY@1.0.0":
            raise FinalOracleProducerError("LiTS ASTRA regression projection schema drift")
        summary_identity = semantic_hash(summary)
        if audit.get("astra_shaped_empirical_summary_identity") != summary_identity:
            raise FinalOracleProducerError("LiTS ASTRA regression projection identity drift")

    return material, audit, execution, precheck


def _write_lits_materialization_checkpoint(
    *,
    path: Path,
    material: Mapping[str, Any],
    audit: Mapping[str, Any],
    execution_receipt: Mapping[str, Any],
    precheck: Mapping[str, Any],
) -> tuple[str, str]:
    path = Path(path).resolve()
    if path.exists():
        raise FinalOracleProducerError("LiTS materialization checkpoint path already exists")
    body = canonicalize({
        "schema": LITS_MATERIALIZATION_CHECKPOINT_SCHEMA,
        "source_identity": material.get("source_identity"),
        "material": material,
        "audit": audit,
        "execution_receipt": execution_receipt,
        "precheck": precheck,
    })
    _validate_lits_materialization_checkpoint_body(body)
    checkpoint_identity = hashlib.sha256(_canonical_bytes(body)).hexdigest()
    document = {**body, "checkpoint_sha256": checkpoint_identity}
    document_sha = _write_json(path, document)
    return checkpoint_identity, document_sha


def _load_lits_materialization_checkpoint(
    path: Path,
) -> tuple[Mapping[str, Any], Mapping[str, Any], Mapping[str, Any], Mapping[str, Any], str, str]:
    path = Path(path).resolve()
    raw = path.read_bytes()
    document = _load_json(path)
    if raw != _canonical_bytes(document):
        raise FinalOracleProducerError("LiTS materialization checkpoint is not canonical JSON")
    checkpoint_identity = document.get("checkpoint_sha256")
    body = {key: value for key, value in document.items() if key != "checkpoint_sha256"}
    observed_identity = hashlib.sha256(_canonical_bytes(body)).hexdigest()
    if checkpoint_identity != observed_identity:
        raise FinalOracleProducerError("LiTS materialization checkpoint digest mismatch")
    material, audit, execution, precheck = _validate_lits_materialization_checkpoint_body(body)
    document_sha = hashlib.sha256(raw).hexdigest()
    return material, audit, execution, precheck, checkpoint_identity, document_sha


def produce_lits_local_oracle(
    *,
    source_path: Path | None = None,
    repo_root: Path,
    work_root: Path,
    output_path: Path,
    checkpoint_output: Path | None = None,
    resume_checkpoint: Path | None = None,
    freeze_sequence: int = 30,
) -> Mapping[str, Any]:
    repo_root = Path(repo_root).resolve()
    work_root = Path(work_root).resolve()
    output_path = Path(output_path).resolve()
    _reject_candidate_owned_path(output_path, work_root, "LiTS oracle output")

    if resume_checkpoint is not None:
        if source_path is not None or checkpoint_output is not None:
            raise FinalOracleProducerError(
                "LiTS checkpoint resume may not also specify source or checkpoint output"
            )
        if (work_root / "cells").exists():
            raise FinalOracleProducerError(
                "LiTS checkpoint resume requires a work root without candidate-owned cells"
            )
        resume_path = Path(resume_checkpoint).resolve()
        if resume_path == output_path:
            raise FinalOracleProducerError("LiTS checkpoint and oracle output paths must differ")
        _reject_candidate_owned_path(resume_path, work_root, "LiTS materialization checkpoint")
        (
            material,
            audit,
            execution_receipt,
            _precheck,
            checkpoint_identity,
            checkpoint_document_sha,
        ) = _load_lits_materialization_checkpoint(resume_path)
        source_access = {
            "mode": "RESUME_VERIFIED_PARITY_READY_I05_CHECKPOINT",
            "source_hash_passes": 0,
            "decoder_calls": 0,
        }
        checkpoint_path = resume_path
    else:
        if source_path is None:
            raise FinalOracleProducerError(
                "LiTS source path or parity-ready verified I05 checkpoint is required"
            )
        material, audit, execution_receipt, precheck = _neutral_lits_material(
            source_path=source_path,
            repo_root=repo_root,
            work_root=work_root,
        )
        checkpoint_path = (
            Path(checkpoint_output).resolve()
            if checkpoint_output is not None
            else work_root
            / "court"
            / "oracle_producers"
            / "LITS_I"
            / LITS_MATERIALIZATION_CHECKPOINT_NAME
        )
        if checkpoint_path == output_path:
            raise FinalOracleProducerError("LiTS checkpoint and oracle output paths must differ")
        _reject_candidate_owned_path(
            checkpoint_path, work_root, "LiTS materialization checkpoint"
        )
        checkpoint_identity, checkpoint_document_sha = _write_lits_materialization_checkpoint(
            path=checkpoint_path,
            material=material,
            audit=audit,
            execution_receipt=execution_receipt,
            precheck=precheck,
        )
        source_access = {
            "mode": "FRESH_SOURCE_BACKED_PARITY_READY_I05_MATERIALIZATION",
            "source_hash_passes": 1,
            "decoder_calls": 1,
        }
    prior_product = _git_json(repo_root, LITS_ASTRA_D04_R2_COMMIT, ASTRA_PRODUCT_PATH)
    prior_replay = _git_json(repo_root, LITS_ASTRA_D04_R2_COMMIT, ASTRA_REPLAY_PATH)
    astra_projection = material.get("astra_shaped_empirical_summary")
    parity_receipt = None
    parity_path = None
    parity_document_sha = None
    astra_regression_status = "NOT_REQUIRED_FOR_CANONICAL_CURRENT_RESUME"
    if astra_projection is not None:
        prior_roles = _git_json(repo_root, LITS_ASTRA_D04_R2_COMMIT, ASTRA_ROLE_PATH)
        accepted_inputs = _verified_astra_input_manifest(repo_root)
        expected_astra_summary = normalize_accepted_astra_summary(
            product=prior_product,
            role_receipt=prior_roles,
            replay_receipt=prior_replay,
        )
        parity_receipt = assert_lits_astra_substantive_parity(
            expected_summary=expected_astra_summary,
            observed_summary=astra_projection,
            accepted_inputs=accepted_inputs,
            current_execution_identity=execution_receipt["execution_identity"],
            current_replay_identity=material["replay_manifest"]["i05_replay_ref"]["content_hash"],
        )
        parity_path = (
            Path(work_root).resolve()
            / "court"
            / "oracle_producers"
            / "LITS_I"
            / "astra_substantive_parity_receipt.json"
        )
        parity_document_sha = _write_json(parity_path, parity_receipt)
        astra_regression_status = "PASS__CURRENT_FACTS_PROJECTED_TO_HISTORICAL_ASTRA_LOGICAL_DOMAIN"

    provenance = {
        "builder": "FIABC_FINAL_LITS_CANDIDATE_NEUTRAL_LOCAL_ORACLE_PRODUCER_R1",
        "dependencies": [
            {"owner_class": "EXACT_SOURCE", "identity": LITS_SOURCE_SHA256},
            {
                "owner_class": "ACCEPTED_AUTHORITY",
                "identity": LITS_RUNTIME_CATALOG,
            },
            {
                "owner_class": "BOUNDED_PHYSICAL_REPRESENTATION_AUTHORITY",
                "identity": LITS_REPRESENTATION_AUTHORITY_REF.authority_content_hash,
            },
            {
                "owner_class": "COMMON_SEMANTIC_PRODUCER",
                "identity": execution_receipt["execution_identity"],
            },
            {
                "owner_class": "ACCEPTED_IMMUTABLE_PRIOR_EMPIRICAL_PRODUCT",
                "identity": LITS_LEARNED_PRODUCT_IDENTITY,
            },
        ],
        "candidate_outputs_used": [],
        "pairwise_candidate_vote": False,
        "first_successful_candidate_as_golden": False,
        "candidate_a_b_c_processes_started": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
    }
    frozen = build_lits_i_oracle(
        prior_product=prior_product,
        prior_replay_receipt=prior_replay,
        source_identity=material["source_identity"],
        court_constitution_refs=material["court_constitution_refs"],
        semantic_authority_closure=material["semantic_authority_closure"],
        projection_and_release_refs=material["projection_and_release_refs"],
        frontier_manifest=material["frontier_manifest"],
        comparison_fact_manifest=material["comparison_fact_manifest"],
        expected_learned_product=material["expected_learned_product"],
        replay_manifest=material["replay_manifest"],
        exact_ref_manifest=material["exact_ref_manifest"],
        oracle_build_provenance=provenance,
        freeze=FreezeContext(freeze_sequence=freeze_sequence),
    )
    identity = verify_frozen_oracle(frozen)
    output_sha = _write_json(Path(output_path), frozen)
    return {
        "schema": PRODUCER_SCHEMA,
        "operation": "PRODUCE_LITS_LOCAL_CANDIDATE_NEUTRAL_ORACLE",
        "status": "PASS",
        "source": "LITS_I",
        "oracle_identity_sha256": identity,
        "oracle_document_sha256": output_sha,
        "output_path": str(Path(output_path)),
        "materialization_checkpoint_path": str(checkpoint_path),
        "materialization_checkpoint_schema": LITS_MATERIALIZATION_CHECKPOINT_SCHEMA,
        "materialization_checkpoint_sha256": checkpoint_identity,
        "materialization_checkpoint_document_sha256": checkpoint_document_sha,
        "source_access": source_access,
        "astra_regression_status": astra_regression_status,
        "astra_substantive_parity_receipt_path": (
            str(parity_path) if parity_path is not None else None
        ),
        "astra_substantive_parity_receipt_identity": (
            parity_receipt["parity_receipt_identity"] if parity_receipt is not None else None
        ),
        "astra_substantive_parity_document_sha256": parity_document_sha,
        "astra_expected_empirical_summary_identity": (
            parity_receipt["expected_empirical_summary_identity"]
            if parity_receipt is not None else None
        ),
        "astra_observed_empirical_summary_identity": (
            parity_receipt["observed_empirical_summary_identity"]
            if parity_receipt is not None else None
        ),
        "current_standardized_constituent_i03_fact_refs": [
            row["ref"] for row in material["constituent_i03_fact_manifest"]
        ],
        "current_constituent_i03_closure_identity": material[
            "constituent_i03_closure_identity"
        ],
        "current_observation_shaped_exact_ref_manifest": material["exact_ref_manifest"],
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
        "audit": audit,
    }


def _relative_oracle_path(oracle_path: Path, freeze_path: Path) -> str:
    return os.path.relpath(
        str(Path(oracle_path).resolve()), str(Path(freeze_path).resolve().parent)
    )


def _verified_standard_oracle(
    *, path: Path, source: str, work_root: Path
) -> tuple[Mapping[str, Any], str, str]:
    _reject_candidate_owned_path(path, work_root, f"{source} oracle")
    doc = _load_json(path)
    if doc.get("schema") != ORACLE_SCHEMA or doc.get("source") != source:
        raise FinalOracleProducerError(f"{source} oracle is not the standard live schema")
    identity = verify_frozen_oracle(doc)
    receipt = doc.get("freeze_receipt")
    if not isinstance(receipt, Mapping):
        raise FinalOracleProducerError(f"{source} oracle freeze receipt missing")
    _check_zero_candidate_provenance(receipt, f"{source} standard oracle")
    court = doc.get("court_constitution_refs")
    if not isinstance(court, Mapping):
        raise FinalOracleProducerError(f"{source} oracle court constitution missing")
    if not isinstance(court.get("frozen_authority_identity"), Mapping):
        raise FinalOracleProducerError(f"{source} oracle frozen authority identity missing")
    if not isinstance(court.get("frozen_workload_identity"), Mapping):
        raise FinalOracleProducerError(f"{source} oracle frozen workload identity missing")
    return doc, identity, _sha256_file(path)


def produce_t3_two_source_freeze(
    *,
    lits_oracle_path: Path,
    wvs_oracle_path: Path,
    work_root: Path,
    output_path: Path,
) -> Mapping[str, Any]:
    work_root = Path(work_root).resolve()
    output_path = Path(output_path).resolve()
    _reject_candidate_owned_path(output_path, work_root, "T3 freeze receipt")
    lits, lits_id, lits_sha = _verified_standard_oracle(
        path=Path(lits_oracle_path), source="LITS_I", work_root=work_root
    )
    wvs, wvs_id, wvs_sha = _verified_standard_oracle(
        path=Path(wvs_oracle_path), source="WVS7", work_root=work_root
    )
    if lits["source_identity"] != {
        "source": "LITS_I",
        "sha256": LITS_SOURCE_SHA256,
        "rows": LITS_ROWS,
        "variables": LITS_VARIABLES,
    }:
        raise FinalOracleProducerError("LiTS standard oracle source identity drift")
    if wvs["source_identity"] != {
        "source": "WVS7",
        "sha256": WVS7_SOURCE_SHA256,
        "rows": WVS_ROWS,
        "variables": WVS_VARIABLES,
    }:
        raise FinalOracleProducerError("WVS standard oracle source identity drift")

    authority_identities = {
        "LITS_I": canonicalize(lits["court_constitution_refs"]["frozen_authority_identity"]),
        "WVS7": canonicalize(wvs["court_constitution_refs"]["frozen_authority_identity"]),
    }
    workload_identities = {
        "LITS_I": canonicalize(lits["court_constitution_refs"]["frozen_workload_identity"]),
        "WVS7": canonicalize(wvs["court_constitution_refs"]["frozen_workload_identity"]),
    }
    oracle_paths = {
        "LITS_I": Path(lits_oracle_path).resolve(),
        "WVS7": Path(wvs_oracle_path).resolve(),
    }
    identities = {"LITS_I": lits_id, "WVS7": wvs_id}
    shas = {"LITS_I": lits_sha, "WVS7": wvs_sha}
    source_shas = {"LITS_I": LITS_SOURCE_SHA256, "WVS7": WVS7_SOURCE_SHA256}

    source_freezes = {
        source: {
            "source_id": source,
            "canonical_source_sha256": source_shas[source],
            "source_identity_authority_ref": f"{CURRENT_SOURCE_MANIFEST_REF}.{source}",
            "derivative_identity": None,
            "derivative_to_source_provenance_ref": None,
        }
        for source in ("LITS_I", "WVS7")
    }
    oracle_identities = {}
    for source in ("LITS_I", "WVS7"):
        rel = _relative_oracle_path(oracle_paths[source], output_path)
        oracle_identities[source] = {
            "oracle_identity_sha256": identities[source],
            "oracle_freeze_authority_ref": rel + "#freeze_receipt",
            "oracle_document_path": rel,
            "oracle_document_sha256": shas[source],
        }

    doc = {
        "schema": FREEZE_RECEIPT_SCHEMA,
        "candidate_neutral": True,
        "frozen_before_candidate_execution": True,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
        "state": "FROZEN_READ_ONLY",
        "source_freezes": source_freezes,
        "authority_identities": authority_identities,
        "workload_identities": workload_identities,
        "oracle_identities": oracle_identities,
        "freeze_order": {
            "source_identity_freeze_sequence": 10,
            "authority_workload_freeze_sequence": 20,
            "oracle_materialize_freeze_sequence": 30,
        },
    }
    output_sha = _write_json(output_path, doc)
    loaded, loaded_sha = load_frozen_upstream_receipt(output_path)
    if loaded_sha != output_sha or canonicalize(loaded) != canonicalize(doc):
        raise FinalOracleProducerError("T3 self-validation identity mismatch")

    # Exercise the live T5 path resolver and standard oracle verifier, not only
    # the generic envelope validator.
    from rawlsing_next.fiabc_live_terminal_control import load_frozen_source_oracle

    for source in ("LITS_I", "WVS7"):
        live_oracle, _freeze, live_freeze_sha = load_frozen_source_oracle(
            freeze_path=output_path, source=source, work_root=work_root
        )
        if live_oracle.get("oracle_identity_sha256") != identities[source]:
            raise FinalOracleProducerError(f"{source} live T5 oracle binding mismatch")
        if live_freeze_sha != output_sha:
            raise FinalOracleProducerError(f"{source} live T5 freeze identity mismatch")

    return {
        "schema": PRODUCER_SCHEMA,
        "operation": "PRODUCE_FINAL_TWO_SOURCE_T3_FREEZE",
        "status": "PASS",
        "freeze_schema": FREEZE_RECEIPT_SCHEMA,
        "freeze_document_sha256": output_sha,
        "output_path": str(output_path),
        "oracle_identities": identities,
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "candidate_owned_state_reused": False,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m rawlsing_next.fiabc_final_oracle_freeze_producers"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    wvs = sub.add_parser(
        "standardize-wvs",
        help="Source-free accepted R1M WVS successor oracle -> standard live oracle",
    )
    wvs.add_argument("--r1m", required=True, type=Path)
    wvs.add_argument("--output", required=True, type=Path)
    wvs.add_argument("--freeze-sequence", type=int, default=30)

    lits = sub.add_parser(
        "produce-lits",
        help="Candidate-neutral local LiTS common-path oracle producer",
    )
    lits.add_argument("--repo-root", required=True, type=Path)
    source = lits.add_mutually_exclusive_group(required=True)
    source.add_argument("--source", type=Path)
    source.add_argument("--resume-checkpoint", type=Path)
    lits.add_argument("--work-root", required=True, type=Path)
    lits.add_argument("--output", required=True, type=Path)
    lits.add_argument("--checkpoint-output", type=Path)
    lits.add_argument("--freeze-sequence", type=int, default=30)

    t3 = sub.add_parser(
        "freeze-t3",
        help="Verify two standard source oracles and emit final T3 upstream freeze",
    )
    t3.add_argument("--lits-oracle", required=True, type=Path)
    t3.add_argument("--wvs-oracle", required=True, type=Path)
    t3.add_argument("--work-root", required=True, type=Path)
    t3.add_argument("--output", required=True, type=Path)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "standardize-wvs":
        receipt = standardize_wvs_r1m_oracle(
            r1m_path=args.r1m,
            output_path=args.output,
            freeze_sequence=args.freeze_sequence,
        )
    elif args.command == "produce-lits":
        receipt = produce_lits_local_oracle(
            source_path=args.source,
            repo_root=args.repo_root,
            work_root=args.work_root,
            output_path=args.output,
            checkpoint_output=args.checkpoint_output,
            resume_checkpoint=args.resume_checkpoint,
            freeze_sequence=args.freeze_sequence,
        )
    elif args.command == "freeze-t3":
        receipt = produce_t3_two_source_freeze(
            lits_oracle_path=args.lits_oracle,
            wvs_oracle_path=args.wvs_oracle,
            work_root=args.work_root,
            output_path=args.output,
        )
    else:  # pragma: no cover
        raise FinalOracleProducerError("unknown command")
    print(json.dumps(receipt, sort_keys=True, separators=(",", ":"), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "FinalOracleProducerError",
    "PRODUCER_SCHEMA",
    "R1M_ORACLE_IDENTITY",
    "R1M_TRUTH_IDENTITY",
    "SUCCESSOR_DISCOVERY_AUTHORITY",
    "SUCCESSOR_LOCK2",
    "SUCCESSOR_LOCK2_REPLAY",
    "produce_lits_local_oracle",
    "produce_t3_two_source_freeze",
    "standardize_wvs_r1m_oracle",
]
