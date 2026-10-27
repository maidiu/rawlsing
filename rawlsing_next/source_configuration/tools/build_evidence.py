"""Build the portable R157 evidence/facts package from pinned inputs.

Inputs are read from immutable Git objects plus the exact P2 phase-0 CSV.  The
script never reads an original survey file and never copies respondent rows.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import sqlite3
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, Mapping

R154_COMMIT = "a02adc896264e1b46afd143cba9426182ec14802"
R154_DB_PATH = "WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/store/r154_all35.sqlite"
H48_COMMIT = "359ddabc89d78ceb4c8fa45561588ee4cad7dd11"
H48_PATH = "WORKER_RETURNS/PYAT-R48-H48-AUTHORITY-AND-CODE-ATLAS-R1/evidence/original_item_authority_candidates.json.gz"
H48_SHA = "35818e2cdd2b7e16e60788bef094eb117ef78fc63df3dc068ecb8b8948f728f5"
RELATION_COMMIT = "9561723cfe0932869e781f2be27e9c80b050ad7a"
RELATION_PATH = "data/ddm_build_copy/authority/full_question_relation_authority/R1_20260814/QSM_FULL_QUESTION_RELATION_AUTHORITY_FINAL_R1.csv"
RELATION_SHA = "0f7fa1c0f579fd44ad44a7ccfc576166b5e8b49895e2822dfc916dff8d00ad13"
P2_SHA = "d38301588fae27c66f6b8627c5007fb0d8ed4ac3d7eb25f32c74228c367b86b6"
P2_ROWS = 18_276
PLAN_SEAL = "4c0c619eac747afee1d8e65e1418bf2d472da4c3"


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def git_blob(repo: Path, commit: str, path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{commit}:{path}"], cwd=repo)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")


def write_jsonl_gz(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with gzip.open(path, "wt", encoding="utf-8", compresslevel=9) as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
            handle.write("\n")


def json_value(value: Any) -> Any:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float, bool, dict, list)):
        return value
    try:
        return json.loads(value)
    except (TypeError, json.JSONDecodeError):
        return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--out", type=Path, default=Path("rawlsing_next/source_configuration/evidence"))
    parser.add_argument("--p2", type=Path, default=None,
                        help="exact P2 phase-0 CSV; defaults to evidence/P2_PHASE0.csv.gz")
    args = parser.parse_args()
    repo = args.repo_root.resolve()
    out = (repo / args.out).resolve() if not args.out.is_absolute() else args.out
    out.mkdir(parents=True, exist_ok=True)

    # Pinned plan facts.
    readiness_rows = list(csv.DictReader(
        (repo / "SOURCE_PRE553_PLAN/evidence/PER_SOURCE_READINESS.csv").open(newline="", encoding="utf-8")))
    source_cards = json.loads((repo / "SOURCE_PRE553_PLAN/SOURCE_CARDS.json").read_text(encoding="utf-8"))
    lanes = json.loads((repo / "SOURCE_PRE553_PLAN/LANES.json").read_text(encoding="utf-8"))
    lane_by_source = {sid: lane["lane_id"] for lane in lanes["lanes"] for sid in lane["source_ids"]}
    card_by_source = {card["source_id"]: card for card in source_cards["sources"]}
    if len(readiness_rows) != 35 or set(lane_by_source) != {row["source_id"] for row in readiness_rows}:
        raise SystemExit("source roster/lane coverage is not exactly 35")

    # Exact prior evidence.
    h48_raw = git_blob(repo, H48_COMMIT, H48_PATH)
    if sha256_bytes(h48_raw) != H48_SHA:
        raise SystemExit("H48 input SHA mismatch")
    h48 = json.loads(gzip.decompress(h48_raw))
    relation_raw = git_blob(repo, RELATION_COMMIT, RELATION_PATH)
    if sha256_bytes(relation_raw) != RELATION_SHA:
        raise SystemExit("full-relation input SHA mismatch")
    relation_rows = list(csv.DictReader(io.StringIO(relation_raw.decode("utf-8-sig"))))
    if args.p2 is not None:
        p2_raw = args.p2.read_bytes()
    else:
        p2_candidate = out / "P2_PHASE0.csv.gz"
        if not p2_candidate.is_file():
            raise SystemExit("--p2 is required on the first build")
        p2_raw = gzip.decompress(p2_candidate.read_bytes())
    if sha256_bytes(p2_raw) != P2_SHA:
        raise SystemExit("P2 input SHA mismatch")
    p2_rows = list(csv.DictReader(io.StringIO(p2_raw.decode("utf-8-sig"))))
    if len(p2_rows) != P2_ROWS:
        raise SystemExit("P2 row count mismatch")
    # Vendor the exact P2 facts as a compressed portable copy.
    (out / "P2_PHASE0.csv.gz").write_bytes(gzip.compress(p2_raw, 9))

    # Current R154 metadata facts (metadata-only snapshot DB).
    db_raw = git_blob(repo, R154_COMMIT, R154_DB_PATH)
    with tempfile.NamedTemporaryFile(suffix=".sqlite") as handle:
        handle.write(db_raw)
        handle.flush()
        con = sqlite3.connect(handle.name)
        con.row_factory = sqlite3.Row
        sources = {row["source_id"]: dict(row)
                   for row in con.execute("select * from sources order by source_id")}
        physical = [dict(row) for row in con.execute("select * from physical_columns order by source_id, ordinal")]
        codebook = [dict(row) for row in con.execute("select * from codebook_rows order by source_id, row_index")]
        con.close()

    if len(sources) != 35 or len(physical) != 18_413 or len(codebook) != 18_276:
        raise SystemExit("R154 metadata counts do not match the frozen baseline")

    source_id_by_key = {(row["family"], row["wave"]): row["source_id"] for row in readiness_rows}
    h48_by_id = {item["question_implementation_id"]: item for item in h48}
    p2_by_id = {row["question_implementation_id"]: row for row in p2_rows}
    relation_by_id = {row["p2_question_implementation_id"]: row
                      for row in relation_rows if row["p2_question_implementation_id"]}
    if len(h48_by_id) != 18_276 or len(p2_by_id) != 18_276:
        raise SystemExit("prior item index is not unique/complete")
    if set(h48_by_id) != set(p2_by_id):
        raise SystemExit("H48/P2 implementation identity mismatch")
    if len(relation_by_id) != 18_250:
        raise SystemExit("exact relation join count mismatch")
    if not set(relation_by_id).issubset(p2_by_id):
        raise SystemExit("relation join contains an ID absent from P2")
    unmatched_ids = tuple(sorted(set(p2_by_id) - set(relation_by_id)))
    if len(unmatched_ids) != 26:
        raise SystemExit("explicit unmatched relation count mismatch")

    codebook_by_source_var = {(row["source_id"], row["var_name"]): row for row in codebook}
    physical_by_source = Counter(row["source_id"] for row in physical)
    codebook_by_source = Counter(row["source_id"] for row in codebook)

    # Portable physical slot facts.
    def physical_rows() -> Iterable[Mapping[str, Any]]:
        for row in physical:
            codebook_row = codebook_by_source_var.get((row["source_id"], row["name"]))
            yield {
                "source_id": row["source_id"],
                "ordinal": row["ordinal"],
                "name": row["name"],
                "label": row["label"],
                "readstat_type": row["readstat_type"],
                "original_type": row["original_type"],
                "storage_width": row["storage_width"],
                "measure": row["measure"],
                "value_labels": json_value(row["value_labels"]),
                "missing_ranges": json_value(row["missing_ranges"]),
                "missing_user_values": json_value(row["missing_user_values"]),
                "codebook_mapping": {
                    "var_name": codebook_row["var_name"] if codebook_row else None,
                    "row_hash": codebook_row["row_hash"] if codebook_row else None,
                    "status": "EXACT" if codebook_row else "PHYSICAL_ONLY",
                },
            }

    write_jsonl_gz(out / "PHYSICAL_SLOTS.jsonl.gz", physical_rows())

    def codebook_rows() -> Iterable[Mapping[str, Any]]:
        for row in codebook:
            yield {
                "source_id": row["source_id"],
                "row_index": row["row_index"],
                "var_name": row["var_name"],
                "module_guess": row["module_guess"],
                "question_text": row["question_text"],
                "response_options_all": row["response_options_all"],
                "storage_type": row["storage_type"],
                "measure": row["measure"],
                "row_hash": row["row_hash"],
            }

    write_jsonl_gz(out / "CODEBOOK_ROWS.jsonl.gz", codebook_rows())

    # Evidence-preserving item index.  Full H48/P2 rows are retained; the exact
    # relation row is retained only for the 18,250 exact implementation joins.
    def item_rows() -> Iterable[Mapping[str, Any]]:
        for implementation_id in sorted(h48_by_id):
            h48_item = h48_by_id[implementation_id]
            p2 = p2_by_id[implementation_id]
            source_id = source_id_by_key.get((h48_item["source_family"], h48_item["wave"]))
            if source_id is None:
                raise SystemExit(f"unmapped H48 source/wave {h48_item['source_family']}/{h48_item['wave']}")
            relation = relation_by_id.get(implementation_id)
            yield {
                "source_id": source_id,
                "family": h48_item["source_family"],
                "wave": h48_item["wave"],
                "implementation_id": implementation_id,
                "exact_identity_sha256": h48_item["exact_identity_sha256"],
                "source_variable_code": h48_item["source_variable_code"],
                "relation_join_status": "EXACT" if relation is not None else "UNMATCHED_EXPLICIT_ID",
                "h48": h48_item,
                "p2": p2,
                "relation": relation,
            }

    write_jsonl_gz(out / "ITEM_EVIDENCE.jsonl.gz", item_rows())

    unmatched = []
    for implementation_id in unmatched_ids:
        h48_item = h48_by_id[implementation_id]
        p2 = p2_by_id[implementation_id]
        unmatched.append({
            "implementation_id": implementation_id,
            "source_id": source_id_by_key[(h48_item["source_family"], h48_item["wave"])],
            "source_variable_code": h48_item["source_variable_code"],
            "exact_identity_sha256": h48_item["exact_identity_sha256"],
            "h48_binding_grade": h48_item["binding_grade"],
            "p2_row": p2,
            "relation_witness": h48_item.get("full_relation_explicit_id_bindings", []),
            "disposition": "HELD_EXACT_UNMATCHED_RELATION_ID",
        })
    write_json(out / "UNMATCHED_RELATIONS.json", {
        "schema": "PYAT_R157_EXACT_UNMATCHED_RELATIONS@1.0.0",
        "count": len(unmatched),
        "records": unmatched,
    })

    physical_name_set = {(row["source_id"], row["name"]) for row in physical}
    physical_only_count = sum(1 for row in physical
                              if (row["source_id"], row["name"]) not in codebook_by_source_var)
    codebook_only_count = sum(1 for row in codebook
                              if (row["source_id"], row["var_name"]) not in physical_name_set)

    # Source roster.
    roster = []
    for readiness in readiness_rows:
        sid = readiness["source_id"]
        source = sources[sid]
        card = card_by_source[sid]
        phys_count = physical_by_source[sid]
        cb_count = codebook_by_source[sid]
        if phys_count != int(readiness["physical_columns"]) or cb_count != int(readiness["codebook_rows"]):
            raise SystemExit(f"{sid}: R154 counts differ from readiness baseline")
        source_sha = source["current_sha256"]
        qualified = None
        if sid in {"SRC13", "SRC14"}:
            qualified = "latin1"
        metadata_path = f"WORKER_RETURNS/PYAT-R154-EXACT-ALL35-PIPELINE-INPUT-COMPILATION-R1/records/physical/{sid}_PHYSICAL_METADATA.json"
        metadata_raw = git_blob(repo, R154_COMMIT, metadata_path)
        roster.append({
            "source_id": sid,
            "lane": lane_by_source[sid],
            "family": readiness["family"],
            "wave": readiness["wave"],
            "format": readiness["format"],
            "source_artifact_id": Path(source["path"]).name,
            "source_sha256": source_sha,
            "bytes": int(source["bytes"]),
            "rows": int(source["physical_rows"]),
            "physical_columns": phys_count,
            "codebook_rows": cb_count,
            "physical_only": int(readiness["physical_only"]),
            "codebook_only": int(readiness["codebook_only"]),
            "original_items": int(readiness["prior_H48_items"]),
            "exact_relation_matches": int(readiness["prior_exact_relation_ids"]),
            "unmatched_relation_ids": [x for x in unmatched_ids
                                       if x in set(h48_by_id) and
                                       source_id_by_key[(h48_by_id[x]["source_family"], h48_by_id[x]["wave"])] == sid],
            "metadata_ready": readiness["metadata_ready"] == "True",
            "native_projection_preparer_ready": readiness["native_projection_preparer_ready"],
            "response_execution_permission": readiness["response_execution_permission"],
            "source_card_baseline": {
                "physical_columns": card["physical_columns_baseline"],
                "original_items": card["original_items_baseline"],
                "codebook_rows": card["codebook_rows_baseline"],
                "physical_only": card["physical_only_baseline"],
                "codebook_only": card["codebook_only_baseline"],
                "exact_relation_matches": card["exact_relation_matches_baseline"],
            },
            "metadata_witness": {
                "commit": R154_COMMIT,
                "path": metadata_path,
                "sha256": sha256_bytes(metadata_raw),
                "bytes": len(metadata_raw),
            },
            "codebook_sha256": source["codebook_sha256"],
            "reader": {
                "decoder_owner": (
                    "rawlsing_next.pre553_physical_decoder.decode_sav"
                    if readiness["format"].upper() == "SAV" else
                    "rawlsing_next.pre553_physical_decoder.decode_dta"
                ),
                "required_encoding": qualified,
                "decoder_allowlist_encoding": None,
                "encoding_authority_status": None,
            },
        })

    # Add exact decoder allowlist availability after importing the native map.
    import sys
    sys.path.insert(0, str(repo))
    from rawlsing_next.pre553_physical_decoder import COMPATIBILITY_ALLOWLIST, COMPATIBILITY_ONLY
    for entry in roster:
        allow = COMPATIBILITY_ALLOWLIST.get(entry["source_sha256"])
        entry["reader"]["decoder_allowlist_encoding"] = allow
        entry["reader"]["encoding_authority_status"] = COMPATIBILITY_ONLY if allow else None
        if entry["reader"]["required_encoding"] is not None and allow != entry["reader"]["required_encoding"]:
            raise SystemExit(f"{entry['source_id']}: required encoding is not allowlisted")

    write_json(out / "SOURCE_ROSTER.json", {
        "schema": "PYAT_R157_SOURCE_ROSTER@1.0.0",
        "plan_seal": PLAN_SEAL,
        "counts": {
            "sources": len(roster),
            "physical_columns": sum(x["physical_columns"] for x in roster),
            "codebook_rows": sum(x["codebook_rows"] for x in roster),
            "original_items": sum(x["original_items"] for x in roster),
            "exact_relation_matches": sum(x["exact_relation_matches"] for x in roster),
            "unmatched_relation_ids": len(unmatched_ids),
            "physical_only": sum(x["physical_only"] for x in roster),
            "codebook_only": sum(x["codebook_only"] for x in roster),
        },
        "sources": roster,
    })

    # File manifest.  P0_RETURN/config hashes are recorded by the caller after
    # the config is generated; this manifest remains the exact evidence boundary.
    files = {}
    for name in ("SOURCE_ROSTER.json", "PHYSICAL_SLOTS.jsonl.gz", "CODEBOOK_ROWS.jsonl.gz",
                 "ITEM_EVIDENCE.jsonl.gz", "P2_PHASE0.csv.gz", "UNMATCHED_RELATIONS.json"):
        path = out / name
        raw = path.read_bytes()
        files[name] = {"sha256": sha256_bytes(raw), "bytes": len(raw)}
    write_json(out / "EVIDENCE_MANIFEST.json", {
        "schema": "PYAT_R157_EVIDENCE_MANIFEST@1.0.0",
        "plan_seal": PLAN_SEAL,
        "portable": True,
        "pinned_inputs": [
            {"kind": "R157_PLAN_SEAL", "commit": PLAN_SEAL},
            {"kind": "R154_METADATA_SNAPSHOT", "commit": R154_COMMIT, "path": R154_DB_PATH,
             "sha256": sha256_bytes(db_raw), "bytes": len(db_raw)},
            {"kind": "H48_ITEM_INDEX", "commit": H48_COMMIT, "path": H48_PATH,
             "sha256": H48_SHA, "bytes": len(h48_raw)},
            {"kind": "P2_PHASE0", "sha256": P2_SHA, "bytes": len(p2_raw), "rows": len(p2_rows)},
            {"kind": "FULL_RELATION_AUTHORITY", "commit": RELATION_COMMIT, "path": RELATION_PATH,
             "sha256": RELATION_SHA, "bytes": len(relation_raw), "rows": len(relation_rows)},
        ],
        "counts": {
            "sources": 35,
            "physical_columns": len(physical),
            "codebook_rows": len(codebook),
            "original_items": len(h48_by_id),
            "exact_relation_joins": len(relation_by_id),
            "unmatched_explicit_ids": len(unmatched_ids),
            "relation_rows_total": len(relation_rows),
            "relation_rows_not_imported": len(relation_rows) - len(relation_by_id),
            "physical_only": physical_only_count,
            "codebook_only": codebook_only_count,
        },
        "files": files,
        "limits": [
            "Prior row authority is recovered evidence with original grades, not current execution permission.",
            "No respondent rows or original survey files were read.",
            "The 268 relation rows outside the 18,250 exact implementation joins are intentionally not imported.",
            "The 26 unmatched explicit implementation IDs are preserved in UNMATCHED_RELATIONS.json.",
        ],
    })
    print(json.dumps({"out": str(out), "files": files, "unmatched": len(unmatched)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
