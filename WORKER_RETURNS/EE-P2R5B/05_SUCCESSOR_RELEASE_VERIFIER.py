#!/usr/bin/env python3
"""Verify an EE-P2R5B successor-release execution receipt without source access."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any

SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
SOURCE_ROWS = 29002
SOURCE_VARIABLES = 1198
BASE_RELEASE_HASH = "e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
BASE_CANDIDATE_HASH = "7f81a222ea2611638d7ce7ac55c695120b57323832e6dc17ff65c1992201659c"
BASE_REPLAY_HASH = "6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd"
BASE_PROJECTION_HASH = "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872"
F02_SCOPE_HASH = "bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297"
PASS_TERMINAL = (
    "EE_P2R5B_PASS__I02_SUCCESSOR_RELEASE_LOCAL_EXECUTION_FULLY_MECHANIZED__"
    "EXACT_SOURCE_ACCESS_ONLY_REMAINS__NO_REALIZATION_AUTHORITY_CLAIMED"
)
SHA256 = re.compile(r"^[0-9a-f]{64}$")

EXPECTED_SELECTORS = {
    "urn:rawlsing:prev3:d02:lits2006:q310:eq:1": "c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a",
    "urn:rawlsing:prev3:d02:lits2006:q310:eq:2": "78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df",
    "urn:rawlsing:prev3:d02:lits2006:q310:eq:3": "c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca",
    "urn:rawlsing:prev3:d02:lits2006:q311:eq:1": "69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8",
    "urn:rawlsing:prev3:d02:lits2006:q311:eq:2": "f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849",
    "urn:rawlsing:prev3:d02:lits2006:q311:eq:3": "a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d",
}
EXPECTED_SCAN = {
    "q310": {
        "counts": {"1": 12340, "2": 7511, "3": 9085, "MISSING": 66},
        "row_semantic_root_sha256": "a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455",
    },
    "q311": {
        "counts": {"1": 16582, "2": 4548, "3": 7826, "MISSING": 46},
        "row_semantic_root_sha256": "af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa",
    },
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def fail(message: str) -> None:
    raise SystemExit(f"FAIL: {message}")


def require_sha(value: Any, name: str) -> str:
    if not isinstance(value, str) or not SHA256.fullmatch(value):
        fail(f"{name} is not lowercase sha256")
    return value


def walk_keys(value: Any):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from walk_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_keys(child)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--receipt", required=True, type=Path)
    args = parser.parse_args()
    receipt = load(args.receipt)
    outdir = args.receipt.parent

    if receipt.get("schema") != "EE_P2R5B_SUCCESSOR_RELEASE_RECEIPT@1.0.0":
        fail("receipt schema mismatch")
    if receipt.get("status") != "PASS" or receipt.get("terminal") != PASS_TERMINAL:
        fail("receipt is not terminal PASS")

    source = receipt.get("source", {})
    if source.get("sha256") != SOURCE_SHA256:
        fail("source SHA mismatch")
    if source.get("rows") != SOURCE_ROWS or source.get("variables") != SOURCE_VARIABLES:
        fail("source shape mismatch")
    if source.get("decoder_call") != 'decode_dta(source_path, encoding="latin1")':
        fail("decoder call mismatch")
    if source.get("decoder_compatibility_status") != "COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY":
        fail("decoder compatibility status mismatch")

    base = receipt.get("accepted_base_replay", {})
    if not base.get("reproduced_exactly"):
        fail("base replay not proved exact")
    if base.get("projection_hash") != BASE_PROJECTION_HASH:
        fail("base projection identity mismatch")
    if base.get("candidate_projection_hash") != BASE_CANDIDATE_HASH:
        fail("base candidate identity mismatch")
    if base.get("semantic_release_hash") != BASE_RELEASE_HASH:
        fail("base release identity mismatch")
    if base.get("replay_manifest_hash") != BASE_REPLAY_HASH:
        fail("base replay identity mismatch")

    anchor = receipt.get("frozen_f02_scope_anchor", {})
    if anchor.get("content_hash") != F02_SCOPE_HASH:
        fail("F02 frozen anchor mismatch")
    if anchor.get("accepted_i02_release_claimed") is not False:
        fail("receipt falsely claims frozen F02 anchor is accepted I02")

    extension = receipt.get("extension", {})
    selectors = extension.get("selector_refs", {})
    if set(selectors) != set(EXPECTED_SELECTORS):
        fail("selector identity set mismatch")
    for selector_id, expected_hash in EXPECTED_SELECTORS.items():
        ref = selectors[selector_id]
        if ref.get("content_hash") != expected_hash:
            fail(f"selector hash mismatch: {selector_id}")

    scan_file = outdir / extension.get("source_scan_receipt_file", "")
    if not scan_file.is_file() or sha256_file(scan_file) != extension.get("source_scan_receipt_sha256"):
        fail("extension scan sidecar missing or hash mismatch")
    scan = load(scan_file)
    if scan.get("source_scan") != EXPECTED_SCAN:
        fail("F02 source scan roots/counts mismatch")
    relation = scan.get("row_coordinate_relation", {})
    if relation.get("exact_relation") != "f02_row = i02_physical_row - 1":
        fail("row-coordinate relation mismatch")
    require_sha(relation.get("row_alignment_root_sha256"), "row_alignment_root_sha256")

    successor = receipt.get("accepted_i02_successor", {})
    if successor.get("accepted") is not True:
        fail("I02 successor not accepted")
    if successor.get("ingest_contract") != "PRE553_C11_INGEST@1.0.0":
        fail("ingest contract mismatch")
    if successor.get("ingest_disposition") != "ACCEPTED_C11_LOGICAL_RELEASE":
        fail("ingest disposition mismatch")
    release_ref = successor.get("release_ref", {})
    if release_ref.get("kind") != "C11LogicalRelease":
        fail("successor release ref kind mismatch")
    release_hash = require_sha(release_ref.get("content_hash"), "successor release hash")
    if successor.get("semantic_release_hash") != release_hash:
        fail("successor semantic hash differs from accepted release ref")
    require_sha(successor.get("candidate_projection_hash"), "candidate_projection_hash")
    if successor.get("resolve_release_exact") != "PASS":
        fail("exact repository resolution was not proved")
    if successor.get("repository_release_count") != 1:
        fail("successor repository cardinality mismatch")

    replay_file = outdir / successor.get("replay_manifest_file", "")
    coverage_file = outdir / successor.get("m01_m18_file", "")
    if not replay_file.is_file() or sha256_file(replay_file) != successor.get("replay_manifest_file_sha256"):
        fail("ReplayManifest sidecar missing/hash mismatch")
    if not coverage_file.is_file() or sha256_file(coverage_file) != successor.get("m01_m18_file_sha256"):
        fail("M01-M18 sidecar missing/hash mismatch")
    coverage = load(coverage_file)
    expected_m = {f"M{i:02d}" for i in range(1, 19)}
    if set(coverage) != expected_m or any(not coverage[k] for k in expected_m):
        fail("M01-M18 closure incomplete")
    if coverage != successor.get("m01_m18_coverage"):
        fail("M01-M18 receipt/sidecar mismatch")

    boundary = receipt.get("r5a_boundary", {})
    for key in (
        "realization_authority_claimed",
        "scope_anchor_runtime_release_equality_claimed",
        "release_alias_claimed",
        "realization_binding_emitted",
    ):
        if boundary.get(key) is not False:
            fail(f"R5A boundary violated: {key}")
    if boundary.get("facts_emitted_for_future_binding_only") is not True:
        fail("future-binding-facts boundary missing")
    if boundary.get("frozen_scope_anchor", {}).get("content_hash") != F02_SCOPE_HASH:
        fail("R5A boundary anchor mismatch")
    if boundary.get("actual_accepted_i02_runtime_release_ref") != release_ref:
        fail("R5A boundary runtime ref mismatch")

    forbidden_key_names = {
        "expected_successor_semantic_release_hash",
        "authorized_release_realization_binding",
        "scope_anchor_equals_runtime_release",
    }
    if forbidden_key_names.intersection(set(walk_keys(receipt))):
        fail("receipt contains a forbidden predeclared/equality/authority field")

    print(json.dumps({
        "status": "PASS",
        "receipt": str(args.receipt),
        "accepted_i02_runtime_release_ref": release_ref,
        "r5a_realization_authority_claimed": False,
        "future_release_hash_was_not_predeclared": True,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
