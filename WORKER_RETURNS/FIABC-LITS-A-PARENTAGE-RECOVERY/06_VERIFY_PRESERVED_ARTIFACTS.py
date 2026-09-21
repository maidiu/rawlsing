#!/usr/bin/env python3
"""Read-only LiTS-A preserved first-build artifact verifier.

This tool never opens LiTS source bytes and never reads R5 member payloads.
It validates only:
- the preserved R5 root manifest identity,
- the member-inventory file identity/cardinality,
- the independently pinned historical raw first-build receipt SHA,
and emits a mechanical inspection receipt.

It deliberately does NOT mint or approve FIABC generic parentage.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

EXPECTED_ROOT = "e8f37557493b816e4562f5f47df110cf49b429e9ead54e5b624d6638ee07aa3d"
EXPECTED_LOGICAL = "de8f060aa72eff7e45f8355ed683cb8ee4b6aca7ff255167cb41bcf8e5a7e3d6"
EXPECTED_ROWS = 34_745_595
EXPECTED_SHARDS = 2_121
EXPECTED_SOURCE = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
EXPECTED_RAW_RECEIPT = "89bd0719f0c546bc3e6e0d3ef7678c01c3fb3ab51cf0c82c84f9a343e08d5337"


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("ascii")


def sha256_file(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    size = 0
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
            size += len(block)
    return h.hexdigest(), size


def find_values(value: Any, key: str) -> list[Any]:
    out: list[Any] = []
    if isinstance(value, dict):
        for k, v in value.items():
            if k == key:
                out.append(v)
            out.extend(find_values(v, key))
    elif isinstance(value, list):
        for item in value:
            out.extend(find_values(item, key))
    return out


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--r5-root", required=True)
    p.add_argument("--raw-first-build-receipt", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args()

    root_dir = Path(args.r5_root)
    root_path = root_dir / "root.json"
    inv_path_expected = root_dir / "member_inventory.jsonl"
    raw_receipt_path = Path(args.raw_first_build_receipt)

    raw_root = root_path.read_bytes()
    root = json.loads(raw_root.decode("ascii"))
    supplied = root.get("physical_root_id")
    unsigned = {k: v for k, v in root.items() if k != "physical_root_id"}
    derived = hashlib.sha256(canonical_bytes(unsigned)).hexdigest()
    if supplied != EXPECTED_ROOT or derived != EXPECTED_ROOT:
        raise SystemExit("BLOCKED__PRESERVED_R5_ROOT_IDENTITY_MISMATCH")
    if root.get("logical_stream_digest") != EXPECTED_LOGICAL:
        raise SystemExit("BLOCKED__PRESERVED_R5_LOGICAL_STREAM_MISMATCH")
    if root.get("canonical_row_count") != EXPECTED_ROWS:
        raise SystemExit("BLOCKED__PRESERVED_R5_ROW_COUNT_MISMATCH")

    inv = root.get("member_inventory")
    if not isinstance(inv, dict) or inv.get("path") != "member_inventory.jsonl":
        raise SystemExit("BLOCKED__PRESERVED_R5_INVENTORY_DESCRIPTOR_MISSING")
    if inv.get("member_count") != EXPECTED_SHARDS:
        raise SystemExit("BLOCKED__PRESERVED_R5_INVENTORY_COUNT_MISMATCH")
    inv_path = root_dir / inv["path"]
    if inv_path != inv_path_expected:
        raise SystemExit("BLOCKED__PRESERVED_R5_INVENTORY_PATH_DRIFT")
    inv_sha, inv_bytes = sha256_file(inv_path)
    if inv_sha != inv.get("sha256") or inv_bytes != inv.get("byte_length"):
        raise SystemExit("BLOCKED__PRESERVED_R5_INVENTORY_IDENTITY_MISMATCH")
    with inv_path.open("rb") as f:
        line_count = sum(1 for line in f if line.strip())
    if line_count != EXPECTED_SHARDS:
        raise SystemExit("BLOCKED__PRESERVED_R5_INVENTORY_CARDINALITY_MISMATCH")

    release = root.get("release_identity")
    if not isinstance(release, dict):
        raise SystemExit("BLOCKED__PRESERVED_R5_RELEASE_IDENTITY_MISSING")
    source_ref = release.get("source_artifact_ref")
    if not isinstance(source_ref, dict) or source_ref.get("content_hash") != EXPECTED_SOURCE:
        raise SystemExit("BLOCKED__PRESERVED_R5_EMBEDDED_SOURCE_SHA_MISMATCH")

    raw_sha, raw_bytes = sha256_file(raw_receipt_path)
    if raw_sha != EXPECTED_RAW_RECEIPT:
        raise SystemExit("BLOCKED__ORIGINAL_RAW_FIRST_BUILD_RECEIPT_SHA_MISMATCH")
    raw_doc = json.loads(raw_receipt_path.read_text(encoding="utf-8"))

    receipt = {
        "schema": "FIABC_LITS_A_MINIMAL_LOCAL_PRESERVED_ARTIFACT_INSPECTION@1.0.0",
        "terminal": "MECHANICAL_PRESERVED_ARTIFACT_IDENTITY_PASS__GENERIC_R35_PARENTAGE_NOT_GRANTED",
        "r5": {
            "physical_root_id": supplied,
            "logical_stream_digest": root["logical_stream_digest"],
            "canonical_row_count": root["canonical_row_count"],
            "root_sha256": hashlib.sha256(raw_root).hexdigest(),
            "member_inventory_sha256": inv_sha,
            "member_inventory_byte_length": inv_bytes,
            "member_inventory_count": line_count,
            "build_config": root.get("build_config"),
            "release_identity": release,
        },
        "historical_raw_receipt": {
            "sha256": raw_sha,
            "byte_length": raw_bytes,
            "schema": raw_doc.get("schema") if isinstance(raw_doc, dict) else None,
            "top_level_keys": sorted(raw_doc) if isinstance(raw_doc, dict) else None,
            "observed_source_sha_occurrences": find_values(raw_doc, "sha256").count(EXPECTED_SOURCE),
            "physical_root_id_occurrences": find_values(raw_doc, "physical_root_id").count(EXPECTED_ROOT),
            "code_blob_values": find_values(raw_doc, "code_blob"),
            "build_config_values": find_values(raw_doc, "build_config"),
            "producer_values": find_values(raw_doc, "producer"),
            "operation_values": find_values(raw_doc, "operation") + find_values(raw_doc, "derivation_operation"),
            "reader_config_values": find_values(raw_doc, "reader_config"),
        },
        "prohibitions": {
            "raw_lits_source_opened": False,
            "r5_member_payloads_opened": False,
            "candidate_executed": False,
            "r5_rebuilt": False,
            "parentage_receipt_minted": False,
        },
    }
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(receipt["terminal"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
