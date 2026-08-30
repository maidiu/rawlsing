#!/usr/bin/env python3
"""Materialize CURRENT_ROUTING_LEDGER_CONTRACT@2 from the frozen C02-C05 carriers.

This compiler is deliberately semantics-blind. It only:
  * verifies immutable carrier identities;
  * projects exact current IDs / identity coordinates / frozen dispositions;
  * preserves an unresolved token only when the source carrier emitted one at row grain;
  * retains all other authority/evidence/provenance through immutable carrier references.

It never derives a disposition from catalog metadata and never assigns C05's aggregate
blocker counts to individual rows.
"""
from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import io
import json
import lzma
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

CONTRACT = "CURRENT_ROUTING_LEDGER_CONTRACT@2"
UNRESOLVED = "STILL_UNRESOLVED__SOURCE_AUTHORITY_INSUFFICIENT"
EXPECTED_ROWS = 18_276
EXPECTED_COUNTS = {
    "GOVERNED_GENERAL_OR_UNCONDITIONAL_UNIVERSE": 1025,
    "POSITIVE_EXECUTABLE_ROUTING_AUTHORITY": 1574,
    "GOVERNED_SCOPED_NONAPPLICABILITY": 17,
    "ADMINISTRATIVE_OR_NONRESPONDENT_CONTEXT": 1274,
    UNRESOLVED: 14_386,
}
C02_SHA256 = "0197c20dc6d48106d6070d8b1ba390d43815cd36d92e2f03e70cad04a0a1be4d"
C03_COMMIT = "cbaa97ac11c4e8d517b49663f2037f8ea0e04267"
C03_CANONICAL_SHA256 = "b08b5e4b539cd7936ad24c04a45d8b8e672913f1656482ffc0d3dce5437a095c"
C04_SHA256 = "c3148341c5a6315c4b060f665595c93c4aa935dfc171aa5faf4c14628f914f90"
C05_COMMIT = "509dacadaf863be88d0c6e0d95e9aff6f401af23"
CATALOG_SHA256 = "2a13ca0551f812e71ad254ab65e3f1ccf99ccfa789eeac4ade708cdbfaa568b8"
C05_ORDERED_IDS_SHA256 = "319a74f2bd00d6cd4f3ef434aafbc4ebee635597e6a68d17a86a07462da9ae62"
C05_PAIR_SHA256 = "1d72efe346cced887b65e396b0f69645e668415e7dd9cbc69b9e69d420498013"
C05_FAMILIES = {"Latinobarómetro", "South Asia", "LiTS"}

ROOT = "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/CURRENT_ROUTING_AND_V550J_CARRIER_WAVE_R1"
C03_ROOT = f"{ROOT}/C03_ROUTING_WVS_EVS"
C05_ROOT = f"{ROOT}/C05_ROUTING_LATIN_SOUTHASIA_LITS"

LEDGER_COLUMNS = [
    "contract_version",
    "question_implementation_id",
    "source_family",
    "wave",
    "source_variable_code",
    "disposition",
    "source_court",
    "source_commit",
    "source_carrier_ref",
    "source_carrier_identity",
    "source_row_selector",
    "source_row_record_sha256",
    "unresolved_token_kind",
    "unresolved_token",
]


class Contract2Error(RuntimeError):
    pass


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def row_fingerprint(row: dict[str, Any]) -> str:
    return sha256_bytes(canonical_json({str(k): "" if v is None else str(v) for k, v in sorted(row.items())}))


def git_show(repo_root: Path, commit: str, path: str) -> bytes:
    try:
        return subprocess.check_output(["git", "-C", str(repo_root), "show", f"{commit}:{path}"])
    except subprocess.CalledProcessError as exc:
        raise Contract2Error(f"git show failed for {commit}:{path}") from exc


def csv_rows_from_bytes(data: bytes) -> list[dict[str, str]]:
    reader = csv.DictReader(io.StringIO(data.decode("utf-8-sig"), newline=""))
    if reader.fieldnames is None:
        raise Contract2Error("CSV has no header")
    return [dict(r) for r in reader]


def load_catalog(path: Path) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    if sha256_file(path) != CATALOG_SHA256:
        raise Contract2Error("phase0 catalog SHA-256 mismatch")
    obj = json.loads(path.read_text(encoding="utf-8"))
    rows = obj.get("question_implementations")
    if not isinstance(rows, list) or len(rows) != EXPECTED_ROWS:
        raise Contract2Error("phase0 catalog is not exact 18,276-row current universe")
    by_id: dict[str, dict[str, Any]] = {}
    for row in rows:
        qid = str(row.get("question_implementation_id", ""))
        if not qid or qid in by_id:
            raise Contract2Error(f"catalog duplicate/missing ID: {qid!r}")
        by_id[qid] = row
    return rows, by_id


def contract_row(*, qid: str, family: str, wave: str, var: str, disposition: str,
                 court: str, commit: str, carrier_ref: str, carrier_identity: str,
                 selector: str, source_row: dict[str, Any], token_kind: str, token: str) -> dict[str, str]:
    if disposition not in EXPECTED_COUNTS:
        raise Contract2Error(f"illegal frozen disposition for {qid}: {disposition!r}")
    if disposition != UNRESOLVED and (token_kind or token):
        raise Contract2Error(f"non-unresolved row carries unresolved taxonomy token: {qid}")
    return {
        "contract_version": CONTRACT,
        "question_implementation_id": qid,
        "source_family": family,
        "wave": wave,
        "source_variable_code": var,
        "disposition": disposition,
        "source_court": court,
        "source_commit": commit,
        "source_carrier_ref": carrier_ref,
        "source_carrier_identity": carrier_identity,
        "source_row_selector": selector,
        "source_row_record_sha256": row_fingerprint(source_row),
        "unresolved_token_kind": token_kind,
        "unresolved_token": token,
    }


def read_c02(path: Path) -> list[dict[str, str]]:
    if sha256_file(path) != C02_SHA256:
        raise Contract2Error("C02 carrier SHA-256 mismatch")
    rows = csv_rows_from_bytes(path.read_bytes())
    if len(rows) != 6021:
        raise Contract2Error("C02 row count mismatch")
    out = []
    for i, r in enumerate(rows, 1):
        disp = r["current_disposition"]
        unresolved = disp == UNRESOLVED
        out.append(contract_row(
            qid=r["question_implementation_id"], family=r["source_family"], wave=r["wave"],
            var=r["source_variable_code"], disposition=disp, court="C02_ROUTING_GSS_R1",
            commit="2177fb8767d363ecb77697f5e259f1e10bd05c0b",
            carrier_ref="library:/Rawlsing/C02_GSS_FULL_CURRENT_ROUTING_COURT_R1/CURRENT_GSS_ROUTING_DISPOSITION_LEDGER.csv",
            carrier_identity=f"sha256:{C02_SHA256}", selector=f"csv_data_row:{i}", source_row=r,
            token_kind="UNRESOLVED_BLOCKER_CLASS" if unresolved else "",
            token=r.get("unresolved_blocker_class", "") if unresolved else "",
        ))
    return out


def reconstruct_c03(repo_root: Path) -> tuple[bytes, list[dict[str, str]]]:
    manifest = json.loads(git_show(repo_root, C03_COMMIT, f"{C03_ROOT}/02_LEDGER_MANIFEST.json").decode("utf-8"))
    parts: list[bytes] = []
    for spec in manifest["ordered_chunks"]:
        raw = git_show(repo_root, C03_COMMIT, f"{C03_ROOT}/{spec['path']}")
        payload = raw[:-1] if raw.endswith(b"\n") else raw
        if len(payload) != spec["chars_without_terminal_lf"]:
            raise Contract2Error(f"C03 chunk length mismatch: {spec['path']}")
        if sha256_bytes(raw) != spec["sha256"]:
            raise Contract2Error(f"C03 chunk hash mismatch: {spec['path']}")
        parts.append(payload)
    encoded = b"".join(parts)
    if len(encoded) != manifest["base64_chars"]:
        raise Contract2Error("C03 base64 character count mismatch")
    compressed = base64.b64decode(encoded)
    if len(compressed) != manifest["xz_bytes"] or sha256_bytes(compressed) != manifest["xz_sha256"]:
        raise Contract2Error("C03 XZ identity mismatch")
    canonical = lzma.decompress(compressed)
    if len(canonical) != manifest["canonical_bytes"] or sha256_bytes(canonical) != manifest["canonical_sha256"]:
        raise Contract2Error("C03 canonical carrier identity mismatch")
    if sha256_bytes(canonical) != C03_CANONICAL_SHA256:
        raise Contract2Error("C03 canonical pinned SHA mismatch")
    rows = csv_rows_from_bytes(canonical)
    if len(rows) != 3443:
        raise Contract2Error("C03 row count mismatch")
    return canonical, rows


def read_c03(repo_root: Path) -> list[dict[str, str]]:
    _, rows = reconstruct_c03(repo_root)
    out = []
    for i, r in enumerate(rows, 1):
        disp = r["authority45_disposition"]
        unresolved = disp == UNRESOLVED
        out.append(contract_row(
            qid=r["question_implementation_id"], family=r["source_family"], wave=r["wave"],
            var=r["source_variable_code"], disposition=disp, court="C03_ROUTING_WVS_EVS_R1",
            commit=C03_COMMIT,
            carrier_ref=f"git:{C03_COMMIT}:{C03_ROOT}/02_LEDGER_MANIFEST.json#canonical_csv",
            carrier_identity=f"sha256:{C03_CANONICAL_SHA256}", selector=f"csv_data_row:{i}", source_row=r,
            token_kind="UNRESOLVED_BLOCKER_REF" if unresolved else "",
            token=r.get("unresolved_blocker_ref", "") if unresolved else "",
        ))
    return out


def read_c04(path: Path) -> list[dict[str, str]]:
    if sha256_file(path) != C04_SHA256:
        raise Contract2Error("C04 carrier SHA-256 mismatch")
    rows = csv_rows_from_bytes(path.read_bytes())
    if len(rows) != 3425:
        raise Contract2Error("C04 row count mismatch")
    out = []
    for i, r in enumerate(rows, 1):
        disp = r["authority45_disposition"]
        unresolved = disp == UNRESOLVED
        out.append(contract_row(
            qid=r["question_implementation_id"], family=r["source_family"], wave=r["wave"],
            var=r["source_variable_code"], disposition=disp, court="C04_ROUTING_ARAB_AFRO_ASIAN_R1",
            commit="2fe01e4a9508b64f041d6bc13d3c9880661489d3",
            carrier_ref="library:/Rawlsing/CURRENT_ROUTING_AND_V550J_CARRIER_WAVE_R1/C04_ROUTING_ARAB_AFRO_ASIAN/C04_FULL_CURRENT_ROUTING_LEDGER.csv",
            carrier_identity=f"sha256:{C04_SHA256}", selector=f"csv_data_row:{i}", source_row=r,
            token_kind="UNRESOLVED_BLOCKER_CLASS" if unresolved else "",
            token=r.get("unresolved_blocker_class", "") if unresolved else "",
        ))
    return out


def read_c05(repo_root: Path, catalog_rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    path = f"{C05_ROOT}/01_C05_COMPACT_EXACT_CURRENT_LEDGER.json"
    raw = git_show(repo_root, C05_COMMIT, path)
    carrier = json.loads(raw.decode("utf-8"))
    rows = [r for r in catalog_rows if r.get("source_family") in C05_FAMILIES]
    rows.sort(key=lambda r: str(r["question_implementation_id"]))
    ids = [str(r["question_implementation_id"]) for r in rows]
    if len(ids) != 5387 or len(set(ids)) != 5387:
        raise Contract2Error("C05 target denominator mismatch")
    id_sha = sha256_bytes(("\n".join(ids) + "\n").encode("utf-8"))
    if id_sha != C05_ORDERED_IDS_SHA256 or id_sha != carrier["input"]["ordered_question_implementation_ids_sha256"]:
        raise Contract2Error("C05 ordered current-ID hash mismatch")
    codes = carrier["encoding"]["codes"]
    code_map = carrier["encoding"]["code_map"]
    if len(codes) != len(rows):
        raise Contract2Error("C05 code stream length mismatch")
    pair_hash = hashlib.sha256()
    out = []
    for index, (r, code) in enumerate(zip(rows, codes)):
        qid = str(r["question_implementation_id"])
        pair_hash.update(f"{qid}\t{code}\n".encode("utf-8"))
        if code not in code_map:
            raise Contract2Error(f"C05 illegal disposition code: {code}")
        disp = code_map[code]
        source_row = {"question_implementation_id": qid, "code": code, "code_index": index}
        out.append(contract_row(
            qid=qid, family=str(r["source_family"]), wave=str(r["wave"]),
            var=str(r["source_variable_code"]), disposition=disp, court="C05_ROUTING_LATIN_SOUTHASIA_LITS_R1",
            commit=C05_COMMIT, carrier_ref=f"git:{C05_COMMIT}:{path}",
            carrier_identity=f"git_blob:de6872c8089d2e8caa08eb1130868583b95f47cd;pair_sha256:{C05_PAIR_SHA256}",
            selector=f"code_index:{index}", source_row=source_row,
            token_kind="NOT_EMITTED_AT_ROW_GRAIN" if disp == UNRESOLVED else "",
            token="",
        ))
    if pair_hash.hexdigest() != C05_PAIR_SHA256 or pair_hash.hexdigest() != carrier["encoding"]["pair_stream_sha256"]:
        raise Contract2Error("C05 ID/disposition pair stream hash mismatch")
    return out


def validate_join(rows: list[dict[str, str]], catalog_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    if len(rows) != EXPECTED_ROWS:
        raise Contract2Error(f"joined row count mismatch: {len(rows)}")
    ids = [r["question_implementation_id"] for r in rows]
    dupes = [qid for qid, n in Counter(ids).items() if n != 1]
    missing = sorted(set(catalog_by_id) - set(ids))
    extra = sorted(set(ids) - set(catalog_by_id))
    if dupes or missing or extra:
        raise Contract2Error(f"ID accounting failed: dupes={len(dupes)} missing={len(missing)} extra={len(extra)}")
    coordinate_drift = []
    for row in rows:
        cat = catalog_by_id[row["question_implementation_id"]]
        expected = (str(cat["source_family"]), str(cat["wave"]), str(cat["source_variable_code"]))
        actual = (row["source_family"], row["wave"], row["source_variable_code"])
        if actual != expected:
            coordinate_drift.append((row["question_implementation_id"], actual, expected))
    if coordinate_drift:
        raise Contract2Error(f"catalog identity-coordinate drift: {len(coordinate_drift)}")
    counts = Counter(r["disposition"] for r in rows)
    if dict(counts) != EXPECTED_COUNTS:
        raise Contract2Error(f"frozen disposition vector mismatch: {dict(counts)}")
    unresolved = [r for r in rows if r["disposition"] == UNRESOLVED]
    expected_unresolved = EXPECTED_COUNTS.get(UNRESOLVED)
    if expected_unresolved is None or len(unresolved) != expected_unresolved:
        raise Contract2Error("unresolved row count mismatch")
    c05_bad = [r for r in unresolved if r["source_court"].startswith("C05_") and (r["unresolved_token"] or r["unresolved_token_kind"] != "NOT_EMITTED_AT_ROW_GRAIN")]
    if c05_bad:
        raise Contract2Error("C05 row-level blocker synthesis detected")
    return {
        "rows": len(rows), "unique_ids": len(set(ids)), "missing": 0, "extra": 0,
        "duplicates": 0, "coordinate_drift": 0, "disposition_counts": EXPECTED_COUNTS,
        "unresolved_rows": len(unresolved), "c05_row_blocker_synthesis": 0,
    }


def write_csv(path: Path, rows: Iterable[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLUMNS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--repo-root", required=True, type=Path)
    p.add_argument("--catalog", required=True, type=Path)
    p.add_argument("--c02-ledger", required=True, type=Path)
    p.add_argument("--c04-ledger", required=True, type=Path)
    p.add_argument("--out-dir", required=True, type=Path)
    args = p.parse_args()

    catalog_rows, catalog_by_id = load_catalog(args.catalog)
    rows = read_c02(args.c02_ledger) + read_c03(args.repo_root) + read_c04(args.c04_ledger) + read_c05(args.repo_root, catalog_rows)
    rows.sort(key=lambda r: r["question_implementation_id"])
    validation = validate_join(rows, catalog_by_id)
    unresolved = [r for r in rows if r["disposition"] == UNRESOLVED]

    ledger_path = args.out_dir / "CURRENT_ROUTING_DISPOSITION_LEDGER.csv"
    unresolved_path = args.out_dir / "UNRESOLVED_TAXONOMY_INPUT.csv"
    write_csv(ledger_path, rows)
    write_csv(unresolved_path, unresolved)
    receipt = {
        "contract": CONTRACT,
        "status": "PASS",
        "validation": validation,
        "outputs": {
            ledger_path.name: {"rows": len(rows), "bytes": ledger_path.stat().st_size, "sha256": sha256_file(ledger_path)},
            unresolved_path.name: {"rows": len(unresolved), "bytes": unresolved_path.stat().st_size, "sha256": sha256_file(unresolved_path)},
        },
    }
    (args.out_dir / "CONTRACT2_MATERIALIZATION_RECEIPT.json").write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
