#!/usr/bin/env python3
"""Build lossless, ordered, newline-aligned chunks of every large U53F file.

Reads original bytes from the pinned Git object, never from a mutable worktree.
Writes only under WORKER_RETURNS/PYAT-R53-P53E-LOSSLESS-ASTRA-EVIDENCE-CORPUS-R1/.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus_common as C


def main():
    manifest, manifest_blob = C.u53f_manifest()
    tree = C.tree_map()
    files = sorted(manifest["files"], key=lambda item: item["path"])
    sharded = []
    direct = []
    per_file = []
    anomalies = []

    seen_paths = set()
    for item in files:
        rel = item["path"]
        if rel in seen_paths:
            anomalies.append({"kind": "DUPLICATE_MANIFEST_PATH", "path": rel})
        seen_paths.add(rel)
        full = C.U53F_RETURN + "/" + rel
        if full not in tree:
            raise SystemExit(f"manifest path absent from pinned tree: {rel}")
        entry = tree[full]
        if entry["kind"] != "blob":
            raise SystemExit(f"manifest path is not a blob: {rel} ({entry['kind']})")
        data = C.read_blob(entry["blob"])
        actual_sha = C.sha256(data)
        metrics = C.line_metrics(data)
        matches = (
            len(data) == item["bytes"]
            and actual_sha == item["sha256"]
        )
        record = {
            "path": rel,
            "full_path": full,
            "git_blob": entry["blob"],
            "git_mode": entry["mode"],
            "manifest_bytes": item["bytes"],
            "manifest_sha256": item["sha256"],
            "actual_bytes": len(data),
            "actual_sha256": actual_sha,
            "manifest_match": matches,
            **metrics,
            "first_line": data.split(b"\n", 1)[0].decode("utf-8", "replace")[:300],
        }
        if not matches:
            anomalies.append(
                {
                    "kind": "MANIFEST_HASH_OR_SIZE_MISMATCH",
                    "path": rel,
                    "manifest_bytes": item["bytes"],
                    "actual_bytes": len(data),
                    "manifest_sha256": item["sha256"],
                    "actual_sha256": actual_sha,
                }
            )
        if len(data) > C.CHUNK_BOUND or rel in C.LARGE_SHARDS:
            record["storage"] = "sharded"
            sharded.append((record, data))
        else:
            record["storage"] = "direct"
            record["direct_path"] = full
            record["chunk_count"] = 0
            record["chunks"] = []
            record["reconstructed_bytes"] = len(data)
            record["reconstructed_sha256"] = actual_sha
            record["reconstruction_equal"] = True
            direct.append(record)
        per_file.append(record)

    if len(sharded) != len(C.LARGE_SHARDS):
        raise SystemExit(
            f"expected {len(C.LARGE_SHARDS)} large files, found {len(sharded)}"
        )

    total_chunks = 0
    total_sharded_bytes = 0
    chunk_rows = []
    for index, (record, data) in enumerate(sharded, start=1):
        shard_id = C.shard_id_for_path(record["path"], index)
        shard_dir = C.SHARDS_ROOT / shard_id
        shard_dir.mkdir(parents=True, exist_ok=True)
        for stale in shard_dir.glob(C.CHUNK_PREFIX + "*.txt"):
            stale.unlink()
        chunks = []
        for part, (start, end) in enumerate(C.split_bytes(data)):
            chunk_path = shard_dir / f"{C.CHUNK_PREFIX}{part:04d}.txt"
            chunk_data = data[start:end]
            chunk_path.write_bytes(chunk_data)
            cm = C.chunk_metrics(data, start, end)
            rec = {
                "part": part,
                "path": str(chunk_path.relative_to(C.P53E_ROOT)),
                "bytes": len(chunk_data),
                "sha256": C.sha256(chunk_data),
                "git_blob": C.hash_object(chunk_path),
                **cm,
            }
            chunks.append(rec)
            chunk_rows.append((record["path"], rec))
        reconstructed = b"".join(data[c["byte_start"] : c["byte_end"]] for c in chunks)
        record.update(
            {
                "shard_id": shard_id,
                "shard_dir": str(shard_dir.relative_to(C.P53E_ROOT)),
                "chunk_count": len(chunks),
                "chunks": chunks,
                "mid_row_split_count": sum(
                    1 for c in chunks if c["starts_mid_row"] or c["ends_mid_row"]
                ),
                "reconstructed_bytes": len(reconstructed),
                "reconstructed_sha256": C.sha256(reconstructed),
                "reconstructed_line_count": reconstructed.count(b"\n")
                + (0 if (not reconstructed or reconstructed.endswith(b"\n")) else 1),
                "reconstruction_equal": reconstructed == data,
                "aggregate_chunk_bytes": sum(c["bytes"] for c in chunks),
                "aggregate_newlines": sum(c["newline_count"] for c in chunks),
            }
        )
        if not record["reconstruction_equal"]:
            anomalies.append({"kind": "RECONSTRUCTION_MISMATCH", "path": record["path"]})
        if record["aggregate_chunk_bytes"] != len(data):
            anomalies.append({"kind": "CHUNK_BYTE_CONSERVATION_FAILURE", "path": record["path"]})
        total_chunks += len(chunks)
        total_sharded_bytes += len(data)
        print(
            f"{shard_id}: {len(data)} bytes -> {len(chunks)} chunks "
            f"({record['line_count']} lines)",
            file=sys.stderr,
        )

    # Manifest-level anomalies are recorded, not hidden.
    observed = manifest.get("observed_head")
    if observed != C.SOURCE_REF:
        anomalies.append(
            {
                "kind": "MANIFEST_OBSERVED_HEAD_PREDATES_FINAL_U53F_HEAD",
                "manifest_observed_head": observed,
                "pinned_source_ref": C.SOURCE_REF,
                "note": "The manifest inside fdc4d... still names 872aaee...; the final "
                        "U53F remote head and the manifest blob's own commit are fdc4d... . "
                        "This is an apparent self-reference defect, not a content-hash failure.",
            }
        )
    remote_path = C.U53F_RETURN + "/evidence/remote_verification.json"
    remote = json.loads(C.read_blob(tree[remote_path]["blob"]).decode("utf-8"))
    if remote.get("verified_remote_ref") != C.SOURCE_REF:
        anomalies.append(
            {
                "kind": "REMOTE_VERIFICATION_RECEIPT_PREDATES_FINAL_HEAD",
                "verified_remote_ref": remote.get("verified_remote_ref"),
                "pinned_source_ref": C.SOURCE_REF,
                "note": "remote_verification.json still verifies 872aaee..., not fdc4d... .",
            }
        )
    nested = [
        r for r in per_file
        if r["path"].startswith("WORKER_RETURNS/")
    ]
    for r in nested:
        anomalies.append(
            {
                "kind": "NESTED_RETURN_ARTIFACT",
                "path": r["path"],
                "bytes": r["actual_bytes"],
                "sha256": r["actual_sha256"],
                "note": "Recursive WORKER_RETURNS copy retained byte-exactly; not treated as "
                        "the authoritative copy where a top-level counterpart exists.",
            }
        )
    if manifest.get("quality_all_pass") is True:
        anomalies.append(
            {
                "kind": "ORIGINAL_DECLARED_ALL_PASS_WITH_SELF_REFERENCE_DEFECT",
                "note": "QUALITY_CHECKS.json all_pass=true is consistent with content hashes, "
                        "but does not cover the observed_head/receipt self-reference defect.",
            }
        )

    total_original_bytes = sum(r["actual_bytes"] for r in per_file)
    all_manifest_match = all(r["manifest_match"] for r in per_file)
    all_reconstruction = all(
        r["reconstruction_equal"] for r in per_file if r["storage"] == "sharded"
    )
    summary = {
        "original_files": len(per_file),
        "sharded_original_files": len(sharded),
        "direct_original_files": len(direct),
        "chunk_count": total_chunks,
        "total_original_bytes": total_original_bytes,
        "sharded_original_bytes": total_sharded_bytes,
        "direct_original_bytes": total_original_bytes - total_sharded_bytes,
        "all_manifest_hashes_match": all_manifest_match,
        "all_sharded_reconstructions_equal": all_reconstruction,
        "chunk_bound_bytes": C.CHUNK_BOUND,
        "max_chunk_bytes": max((c["bytes"] for _, c in chunk_rows), default=0),
        "mid_row_split_count": sum(
            1
            for r in per_file
            for c in r.get("chunks", [])
            if c["starts_mid_row"] or c["ends_mid_row"]
        ),
        "rows_conserved": all(
            r["aggregate_newlines"] == r["newline_count"]
            and r["aggregate_chunk_bytes"] == r["actual_bytes"]
            and r["reconstructed_line_count"] == r["line_count"]
            for r in per_file
            if r["storage"] == "sharded"
        ),
    }

    recheck = {
        "schema": "R53_P53E_ORIGINAL_MANIFEST_INDEPENDENT_RECHECK@1",
        "source_ref": C.SOURCE_REF,
        "source_commit_date": C.commit_date(),
        "source_return_root": C.U53F_RETURN,
        "manifest_path": C.U53F_RETURN + "/EVIDENCE_MANIFEST.json",
        "manifest_git_blob": manifest_blob,
        "manifest_sha256": C.sha256(
            C.read_blob(tree[C.U53F_RETURN + "/EVIDENCE_MANIFEST.json"]["blob"])
        ),
        "manifest_schema": manifest.get("schema"),
        "manifest_sealed_startup": manifest.get("sealed_startup"),
        "manifest_observed_head": manifest.get("observed_head"),
        "manifest_quality_all_pass": manifest.get("quality_all_pass"),
        "manifest_upstream_refs": manifest.get("upstream_refs"),
        "verification": {
            "files_declared": len(files),
            "files_matched": sum(1 for r in per_file if r["manifest_match"]),
            "files_mismatched": sum(1 for r in per_file if not r["manifest_match"]),
            "total_declared_bytes": sum(r["manifest_bytes"] for r in per_file),
            "total_actual_bytes": total_original_bytes,
            "all_hashes_and_sizes_match": all_manifest_match,
        },
        "files": per_file,
        "apparent_manifest_anomalies": anomalies,
        "limits": [
            "This recheck proves byte/size/SHA256 identity of every manifest-declared file at "
            "the pinned fdc4d... object. It does not claim that U53F's selection was exhaustive.",
            "No SAV/DTA respondent data, production code execution, or scientific authority is used.",
        ],
    }
    C.write_json(C.P53E_ROOT / "01_ORIGINAL_MANIFEST_INDEPENDENT_RECHECK.json", recheck)

    corpus = {
        "schema": "R53_P53E_LOSSLESS_ORDERED_SHARD_MANIFEST@1",
        "source_ref": C.SOURCE_REF,
        "source_commit_date": C.commit_date(),
        "source_return_root": C.U53F_RETURN,
        "p53e_return_root": C.P53E_RETURN,
        "generated_from": "git cat-file blob at the pinned source ref; never a mutable worktree",
        "chunk_policy": {
            "bound_bytes": C.CHUNK_BOUND,
            "bound_note": "192 KiB, stricter than the commission's <=200 KiB ceiling.",
            "split_rule": "Ordered byte ranges. A cut is moved back to the last LF within the "
                          "bound. Only a single physical row longer than the bound is split mid-row; "
                          "no row in this corpus needed that exception.",
            "reassembly": "Concatenate chunks in ascending part order; bytes are the original bytes.",
            "row_number_definition": "1-based physical line number including any header row; "
                                     "a final non-LF-terminated line counts as one row.",
        },
        "summary": summary,
        "originals": per_file,
        "anomalies": anomalies,
        "accounting": {
            "every_u53f_manifest_file_accounted": len(per_file) == len(files),
            "sharded_plus_direct_bytes": total_sharded_bytes
            + (total_original_bytes - total_sharded_bytes),
            "declared_total_bytes": total_original_bytes,
            "no_selected_exclusions": True,
        },
    }
    C.write_json(C.P53E_ROOT / "02_LOSSLESS_ORDERED_SHARD_MANIFEST.json", corpus)
    print(
        json.dumps(
            {
                "originals": len(per_file),
                "sharded": len(sharded),
                "direct": len(direct),
                "chunks": total_chunks,
                "bytes": total_original_bytes,
                "all_manifest_match": all_manifest_match,
                "all_reconstruction": all_reconstruction,
                "max_chunk_bytes": summary["max_chunk_bytes"],
            },
            indent=1,
        )
    )


if __name__ == "__main__":
    main()
