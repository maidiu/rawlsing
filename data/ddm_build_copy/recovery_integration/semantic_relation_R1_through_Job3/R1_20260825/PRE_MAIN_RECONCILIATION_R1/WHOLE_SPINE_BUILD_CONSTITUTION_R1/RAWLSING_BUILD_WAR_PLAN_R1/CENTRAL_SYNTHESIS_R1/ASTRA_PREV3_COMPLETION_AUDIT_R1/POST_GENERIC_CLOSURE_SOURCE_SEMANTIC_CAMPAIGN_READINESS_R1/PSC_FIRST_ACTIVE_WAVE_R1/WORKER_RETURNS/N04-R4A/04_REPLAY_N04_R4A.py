#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import pathlib
import zlib
from collections import Counter, defaultdict

from rawlsing_next import n04_r2_whole_corpus_t03_release as n04r2

THIS = pathlib.Path(__file__).resolve()
RETURN_ROOT = THIS.parent

PREDECESSOR_COMMIT = "8e0266703bbf3b060abcd6fbe53c7ef6c49062c5"
PREDECESSOR_VECTOR_PATH = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/"
    "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/PSC_FIRST_ACTIVE_WAVE_R1/"
    "WORKER_RETURNS/N04-R3/03_CURRENT_18276_BINDING_STATUS_VECTOR.zlib.b64"
)
N03_REGISTRY_COMMIT = "497b8dfc6106e2761c61d07d8ba9ea472062892c"
N03_REGISTRY_PATH = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/ASTRA_PREV3_COMPLETION_AUDIT_R1/"
    "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/PSC_FIRST_ACTIVE_WAVE_R1/"
    "WORKER_RETURNS/N03/01_CURRENT_SEMANTIC_AUTHORITY_OBJECT_REGISTRY_R1.json"
)

EXPECTED_LEDGER_SHA256 = "0ac4cd90c19c859438ec12ddfa69c37e9b9c85607884e0f4ea93bc6b52493723"
EXPECTED_VECTOR_RAW_SHA256 = "f3bb9f06508f7eb26d1ee01e6bc865377637da34f5a60b4118006cc5d8a8d283"
EXPECTED_VECTOR_B64_SHA256 = "8241edb2bf043105e0eae12dfa8dd312ff14ca09d37141467834529404c161d7"
EXPECTED_VECTOR_COUNTS = {1: 41, 2: 22, 3: 18012, 4: 159, 5: 42}
EXPECTED_MASK_RAW_SHA256 = "58f5fc1288588874235288e046c1797968263303135af8ceb58cc37da48c112e"
EXPECTED_MASK_B64_SHA256 = "2b22305dda73bcf27d5d5de3c2adbd674e544ab09d7fbb35aa7a7138dc7674db"
EXPECTED_ORDINAL_STREAM_SHA256 = "c6092adb1a55233b8b372222639dcac0c7de8bb4ceff06a07d9e7d1ffe40db6c"
EXPECTED_ORDINAL_STREAM_BYTES = 98754
EXPECTED_SELECTED = 18012

RESPONSE_BINDING_OBJECT = "V550_V551_RESPONSE_SEMANTICS_BINDING"
RESPONSE_REGISTRY_OBJECT = "RESPONSE_SCALE_ENCODING_REGISTRY_35WAVE"
EXPECTED_BINDING_BLOB = "ef77bcbe61385a10fe28b67c15a13f4f794e58e0"
EXPECTED_REGISTRY_BLOB = "2a45215854d1feb4ba0a779edcb29479143ab613"
RESIDUAL = "NO_ACCEPTED_EXACT_RESPONSE_CATEGORY_SEMANTICS_IDENTITY_JOIN"


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git_blob(ref: str, path: str) -> str:
    n04r2._ensure_commit(ref)
    return n04r2._run("git", "rev-parse", f"{ref}:{path}").stdout.decode().strip()


def csv_rows(ref: str, path: str) -> list[dict[str, str]]:
    raw = n04r2._git_bytes(ref, path)
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))


def build() -> tuple[list[dict], dict]:
    ledger, _n03_vector, n03_summary = n04r2._load_n03_r2_replay()
    assert len(ledger) == 18276
    assert n03_summary["rows"] == 18276
    assert n03_summary["unique_ids"] == 18276
    assert n03_summary["ledger_canonical_jsonl_sha256"] == EXPECTED_LEDGER_SHA256

    predecessor_b64 = n04r2._git_bytes(PREDECESSOR_COMMIT, PREDECESSOR_VECTOR_PATH).strip()
    assert sha256(predecessor_b64) == EXPECTED_VECTOR_B64_SHA256
    predecessor_vector = zlib.decompress(base64.b64decode(predecessor_b64))
    assert len(predecessor_vector) == 18276
    assert sha256(predecessor_vector) == EXPECTED_VECTOR_RAW_SHA256
    assert dict(sorted(Counter(predecessor_vector).items())) == EXPECTED_VECTOR_COUNTS

    mask_b64 = (RETURN_ROOT / "02_SELECTED_18012_MASK.zlib.b64").read_bytes().strip()
    assert sha256(mask_b64) == EXPECTED_MASK_B64_SHA256
    mask = zlib.decompress(base64.b64decode(mask_b64))
    assert len(mask) == 18276
    assert set(mask) <= {0, 1}
    assert sha256(mask) == EXPECTED_MASK_RAW_SHA256
    assert mask == bytes(1 if code == 3 else 0 for code in predecessor_vector)
    assert sum(mask) == EXPECTED_SELECTED

    selected_ordinals = [i + 1 for i, bit in enumerate(mask) if bit]
    ordinal_stream = "".join(f"{i}\n" for i in selected_ordinals).encode()
    assert len(ordinal_stream) == EXPECTED_ORDINAL_STREAM_BYTES
    assert sha256(ordinal_stream) == EXPECTED_ORDINAL_STREAM_SHA256

    registry = json.loads(n04r2._git_bytes(N03_REGISTRY_COMMIT, N03_REGISTRY_PATH))
    objects = {obj["object_id"]: obj for obj in registry["objects"]}
    binding_obj = objects[RESPONSE_BINDING_OBJECT]
    response_registry_obj = objects[RESPONSE_REGISTRY_OBJECT]

    assert binding_obj["blob_sha"] == EXPECTED_BINDING_BLOB
    assert response_registry_obj["blob_sha"] == EXPECTED_REGISTRY_BLOB
    assert git_blob(N03_REGISTRY_COMMIT, binding_obj["path"]) == EXPECTED_BINDING_BLOB
    assert git_blob(N03_REGISTRY_COMMIT, response_registry_obj["path"]) == EXPECTED_REGISTRY_BLOB
    assert binding_obj["grain"] == "SOURCE_FAMILY_WAVE_VARIABLE_BINDING"
    assert binding_obj["implementation_binding_status"] == "EXACT_SOURCE_FAMILY_WAVE_VAR_CODE_TO_V551_REGISTRY_KEY_INDEX"
    assert response_registry_obj["grain"] == "RESPONSE_SEMANTICS_CONTRACT_ROW"
    assert response_registry_obj["implementation_binding_status"] == "BOUND_BY_RESPONSE_SEMANTICS_CONTRACT_HASH_AND_V551_REGISTRY_KEY_INDEX_WHERE_DECLARED"

    binding_rows = csv_rows(N03_REGISTRY_COMMIT, binding_obj["path"])
    response_registry_rows = csv_rows(N03_REGISTRY_COMMIT, response_registry_obj["path"])
    assert len(binding_rows) == 236 == binding_obj["state_counts"]["binding_rows"]
    assert len(response_registry_rows) == 145 == response_registry_obj["state_counts"]["registry_rows"]

    exact_binding_index: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in binding_rows:
        exact_binding_index[(row["source_family"], row["canonical_wave"], row["var_code"])].append(row)

    accounting = []
    for row, bit in zip(ledger, mask):
        if not bit:
            continue
        assert row["top_level_disposition"] == "CURRENT_GOVERNED_POSITIVE"
        assert row["response_binding_count"] == 0
        assert row["response_registry_key_indices"] == []
        key = (row["source_family"], row["wave"], row["source_variable_code"])
        assert key not in exact_binding_index
        accounting.append({
            "question_implementation_id": row["question_implementation_id"],
            "source_family": row["source_family"],
            "wave": row["wave"],
            "source_variable_code": row["source_variable_code"],
            "response_category_semantics_ref": None,
            "r4a_disposition": "TYPED_RESIDUAL",
            "typed_residual": RESIDUAL,
            "exact_authority_checks": [
                f"{RESPONSE_BINDING_OBJECT}@{EXPECTED_BINDING_BLOB}:key={key[0]}|{key[1]}|{key[2]}:NO_ROW",
                f"{RESPONSE_REGISTRY_OBJECT}@{EXPECTED_REGISTRY_BLOB}:NO_DECLARED_REGISTRY_KEY_WITHOUT_EXACT_BINDING"
            ]
        })

    assert len(accounting) == EXPECTED_SELECTED
    assert len({row["question_implementation_id"] for row in accounting}) == EXPECTED_SELECTED
    canonical_accounting = b"".join(
        (json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n").encode()
        for row in accounting
    )
    selected_id_stream = "".join(row["question_implementation_id"] + "\n" for row in accounting).encode()

    summary = {
        "schema": "RAWLSING_N04_R4A_REPLAY_SUMMARY@1.0.0",
        "status": "PASS__ZERO_EXACT_BINDS__18012_TYPED_RESIDUALS_PROVED",
        "selected_count": len(accounting),
        "exact_bound_count": 0,
        "typed_residual_count": len(accounting),
        "typed_residual_code": RESIDUAL,
        "newly_production_bindable_after_r4a_count": 0,
        "selected_id_stream_sha256": sha256(selected_id_stream),
        "selected_id_stream_bytes": len(selected_id_stream),
        "canonical_accounting_jsonl_sha256": sha256(canonical_accounting),
        "canonical_accounting_jsonl_bytes": len(canonical_accounting),
        "selector_mask_raw_sha256": sha256(mask),
        "selected_ordinal_stream_sha256": sha256(ordinal_stream),
        "accepted_binding_rows_checked": len(binding_rows),
        "accepted_registry_rows_checked": len(response_registry_rows),
        "forbidden_inference_count": 0,
        "new_semantic_authority_count": 0
    }
    return accounting, summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-accounting", type=pathlib.Path)
    args = parser.parse_args()
    accounting, summary = build()
    if args.emit_accounting:
        payload = "".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in accounting)
        args.emit_accounting.write_text(payload, encoding="utf-8")
    print(json.dumps(summary, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
