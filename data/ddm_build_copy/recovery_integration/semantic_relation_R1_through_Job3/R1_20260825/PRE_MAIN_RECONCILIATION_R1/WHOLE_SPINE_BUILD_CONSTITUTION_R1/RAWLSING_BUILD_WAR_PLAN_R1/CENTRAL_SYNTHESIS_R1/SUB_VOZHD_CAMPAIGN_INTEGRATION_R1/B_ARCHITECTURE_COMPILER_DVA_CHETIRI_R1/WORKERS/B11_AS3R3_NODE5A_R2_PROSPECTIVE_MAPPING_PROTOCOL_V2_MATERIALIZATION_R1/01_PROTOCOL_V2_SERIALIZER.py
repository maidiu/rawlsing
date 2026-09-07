#!/usr/bin/env python3
"""Prospective Node5A-R2 mapping replay protocol-v2 materializer.

This implementation is prospective only. It validates the immutable HQ protocol
spec and frozen 19-row carrier by Git blob identity, then materializes exactly
AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL@2.0.0.

It intentionally contains no historical mapping-payload digest and performs no
serialization search or target comparison.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any

EXPECTED_PROTOCOL_SPEC_GIT_BLOB = "befee68ee14f6e80e88cb3142947a37a7619fc5b"
EXPECTED_CARRIER_GIT_BLOB = "26a7c35df2e6454c5e270a03b3571599bdf152fd"
PROTOCOL_VALUE = "AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL@2.0.0"
EXPECTED_FIELDS = [
    "as3_id",
    "source_object_id",
    "source_content_hash",
    "node4a_input_sha256",
    "successor_kind",
    "successor_object_id",
    "successor_content_hash",
    "alias_class",
    "role_key_lookup_preserved",
]
EXPECTED_ROW_ORDER = [
    "A000",
    "A1V1",
    "A1V2",
    "A1V3",
    "A1V4",
    "A1V5",
    "A1SSUB",
    "A1SSPS",
    "A1SMIS",
    "A1RAPP",
    "A2V1",
    "A2V2",
    "A2V3",
    "A2V4",
    "A2V5",
    "A2SSUB",
    "A2SSPS",
    "A2SMIS",
    "A2RAPP",
]
ALIAS_MEMBERS = {"A000", "A1RAPP"}
ALIAS_VALUE = "{A000,A1RAPP}"


class ProtocolViolation(RuntimeError):
    pass


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ProtocolViolation(message)


def normalize_nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def validate_protocol_spec(spec_bytes: bytes) -> None:
    require(
        git_blob_sha1(spec_bytes) == EXPECTED_PROTOCOL_SPEC_GIT_BLOB,
        "protocol spec Git blob mismatch",
    )
    spec = json.loads(spec_bytes.decode("utf-8"))
    require(
        spec.get("schema") == "AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL_SPEC@2.0.0",
        "protocol spec schema mismatch",
    )
    require(
        spec.get("protocol_id") == "AS3R3_NODE5A_R2_MAPPING_REPLAY_PROTOCOL",
        "protocol id mismatch",
    )
    require(spec.get("protocol_version") == "2.0.0", "protocol version mismatch")
    frozen = spec.get("frozen_semantic_input", {})
    require(frozen.get("carrier_git_blob") == EXPECTED_CARRIER_GIT_BLOB, "carrier blob law mismatch")
    require(frozen.get("row_count") == 19, "row-count law mismatch")
    require(frozen.get("fields") == EXPECTED_FIELDS, "field law mismatch")
    require(frozen.get("row_order") == EXPECTED_ROW_ORDER, "row-order law mismatch")
    canonical = spec.get("canonical_payload_object", {})
    require(canonical.get("protocol_value") == PROTOCOL_VALUE, "payload protocol value mismatch")
    serialization = spec.get("serialization", {})
    require(serialization.get("format") == "RFC8259 JSON", "format law mismatch")
    require(serialization.get("encoding") == "UTF-8", "encoding law mismatch")
    require(serialization.get("bom") is False, "BOM law mismatch")
    require(serialization.get("ensure_ascii") is False, "ensure_ascii law mismatch")
    require(
        serialization.get("key_order") == "lexicographically sorted recursively",
        "key-order law mismatch",
    )
    require(serialization.get("separators") == {"item": ",", "key_value": ":"}, "separator law mismatch")
    require(serialization.get("insignificant_whitespace") is False, "whitespace law mismatch")
    require(
        serialization.get("trailing_bytes") == "exactly one LF byte 0x0A",
        "trailing-byte law mismatch",
    )


def parse_and_validate_carrier(carrier_bytes: bytes) -> list[dict[str, Any]]:
    require(
        git_blob_sha1(carrier_bytes) == EXPECTED_CARRIER_GIT_BLOB,
        "mapping carrier Git blob mismatch",
    )
    text = carrier_bytes.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text, newline=""))
    require(reader.fieldnames == EXPECTED_FIELDS, "CSV header mismatch")
    source_rows = list(reader)
    require(len(source_rows) == 19, "expected exactly 19 data rows")
    require([r["as3_id"] for r in source_rows] == EXPECTED_ROW_ORDER, "row order mismatch")

    rows: list[dict[str, Any]] = []
    for source in source_rows:
        require(list(source.keys()) == EXPECTED_FIELDS, "row field set/order mismatch")
        as3_id = source["as3_id"]
        expected_alias = ALIAS_VALUE if as3_id in ALIAS_MEMBERS else ""
        require(source["alias_class"] == expected_alias, f"alias mismatch for {as3_id}")
        require(
            source["role_key_lookup_preserved"] == "true",
            f"role_key_lookup_preserved must be literal true for {as3_id}",
        )

        row: dict[str, Any] = {}
        for field in EXPECTED_FIELDS:
            if field == "role_key_lookup_preserved":
                row[field] = True
            else:
                row[field] = normalize_nfc(source[field])
        require(set(row.keys()) == set(EXPECTED_FIELDS), "normalized row key mismatch")
        rows.append(row)

    successor_hash_to_roles: dict[str, list[str]] = {}
    for row in rows:
        successor_hash_to_roles.setdefault(row["successor_content_hash"], []).append(row["as3_id"])
    require(len(successor_hash_to_roles) == 18, "distinct successor predicate count must be 18")
    duplicate_roles = sorted(
        sorted(role_ids)
        for role_ids in successor_hash_to_roles.values()
        if len(role_ids) > 1
    )
    require(duplicate_roles == [["A000", "A1RAPP"]], "sole duplicate successor target must be A000/A1RAPP")
    return rows


def materialize(protocol_spec: Path, carrier: Path) -> bytes:
    spec_bytes = protocol_spec.read_bytes()
    carrier_bytes = carrier.read_bytes()
    validate_protocol_spec(spec_bytes)
    rows = parse_and_validate_carrier(carrier_bytes)
    payload = {"protocol": PROTOCOL_VALUE, "rows": rows}
    encoded = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8") + b"\n"
    require(not encoded.startswith(b"\xef\xbb\xbf"), "UTF-8 BOM forbidden")
    require(encoded.endswith(b"\n") and not encoded.endswith(b"\n\n"), "exactly one terminal LF required")
    return encoded


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--protocol-spec", required=True, type=Path)
    parser.add_argument("--carrier", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()

    payload_bytes = materialize(args.protocol_spec, args.carrier)
    args.output.write_bytes(payload_bytes)
    receipt = {
        "schema": "AS3R3_NODE5A_R2_PROTOCOL_V2_SERIALIZER_RUN_RECEIPT@1.0.0",
        "status": "PASS",
        "protocol": PROTOCOL_VALUE,
        "protocol_spec_git_blob": EXPECTED_PROTOCOL_SPEC_GIT_BLOB,
        "carrier_git_blob": EXPECTED_CARRIER_GIT_BLOB,
        "row_count": 19,
        "payload_byte_length": len(payload_bytes),
        "payload_sha256": hashlib.sha256(payload_bytes).hexdigest(),
    }
    if args.receipt is not None:
        args.receipt.write_text(
            json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    sys.stdout.write(json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ProtocolViolation, UnicodeDecodeError, json.JSONDecodeError, csv.Error, OSError) as exc:
        sys.stderr.write(f"FAIL_CLOSED: {exc}\n")
        raise SystemExit(2)
