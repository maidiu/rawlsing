#!/usr/bin/env python3
"""Independent verifier for the P53E lossless corpus.

It does NOT trust the corpus summary.  It re-reads every original from the
pinned Git object, re-reads every chunk from disk, recomputes byte/row/hash
identities, and only then compares the recomputed totals to the manifest.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus_common as C


def fail(check, message, **extra):
    return {"check": check, "pass": False, "message": message, **extra}


def first_difference(a: bytes, b: bytes):
    limit = min(len(a), len(b))
    for index in range(limit):
        if a[index] != b[index]:
            return index
    if len(a) != len(b):
        return limit
    return None


def load_manifest(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", default=str(C.P53E_ROOT / "02_LOSSLESS_ORDERED_SHARD_MANIFEST.json"))
    parser.add_argument("--root", default=str(C.P53E_ROOT))
    parser.add_argument("--source-ref", default=C.SOURCE_REF)
    parser.add_argument("--candidate", default=None)
    parser.add_argument("--candidate-for", default=None)
    parser.add_argument("--json-out", default=None)
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    root = Path(args.root)
    manifest = load_manifest(manifest_path)
    tree = C.tree_map(args.source_ref)
    u53f, _ = C.u53f_manifest()
    u53f_by_path = {item["path"]: item for item in u53f["files"]}
    checks = []
    file_results = []
    manifest_paths = [item["path"] for item in manifest.get("originals", [])]

    if set(manifest_paths) != set(u53f_by_path):
        checks.append(
            fail(
                "manifest_path_set",
                "corpus manifest paths do not exactly match the U53F manifest",
                missing=sorted(set(u53f_by_path) - set(manifest_paths)),
                extra=sorted(set(manifest_paths) - set(u53f_by_path)),
            )
        )
    else:
        checks.append(
            {
                "check": "manifest_path_set",
                "pass": True,
                "message": f"exactly {len(manifest_paths)} U53F paths accounted for",
            }
        )

    total_chunks = 0
    total_bytes = 0
    sharded_bytes = 0
    sharded_count = 0
    direct_count = 0
    max_chunk = 0
    mid_row_splits = 0

    for item in manifest.get("originals", []):
        rel = item["path"]
        full = C.U53F_RETURN + "/" + rel
        result = {"path": rel, "pass": False, "errors": []}
        if full not in tree:
            result["errors"].append(f"path absent at source ref: {full}")
            file_results.append(result)
            continue
        entry = tree[full]
        try:
            actual = C.read_blob(entry["blob"])
        except Exception as exc:
            result["errors"].append(f"cannot read source blob {entry['blob']}: {exc}")
            file_results.append(result)
            continue
        actual_sha = C.sha256(actual)
        actual_metrics = C.line_metrics(actual)
        u53f_item = u53f_by_path.get(rel, {})
        expected = [
            ("bytes", item.get("actual_bytes"), len(actual)),
            ("sha256", item.get("actual_sha256"), actual_sha),
            ("manifest_bytes", item.get("manifest_bytes"), u53f_item.get("bytes")),
            ("manifest_sha256", item.get("manifest_sha256"), u53f_item.get("sha256")),
            ("u53f_bytes", u53f_item.get("bytes"), len(actual)),
            ("u53f_sha256", u53f_item.get("sha256"), actual_sha),
            ("git_blob", item.get("git_blob"), entry["blob"]),
            ("git_mode", item.get("git_mode"), entry["mode"]),
            ("line_count", item.get("line_count"), actual_metrics["line_count"]),
            ("newline_count", item.get("newline_count"), actual_metrics["newline_count"]),
            ("ends_with_newline", item.get("ends_with_newline"), actual_metrics["ends_with_newline"]),
            ("max_line_bytes", item.get("max_line_bytes"), actual_metrics["max_line_bytes"]),
        ]
        for name, got, want in expected:
            if got != want:
                result["errors"].append(f"{name}: manifest={got!r} independent={want!r}")
        total_bytes += len(actual)
        result.update(
            {
                "storage": item.get("storage"),
                "actual_bytes": len(actual),
                "actual_sha256": actual_sha,
                "git_blob": entry["blob"],
                "line_count": actual_metrics["line_count"],
                "newline_count": actual_metrics["newline_count"],
                "ends_with_newline": actual_metrics["ends_with_newline"],
            }
        )
        if item.get("storage") == "sharded":
            sharded_count += 1
            sharded_bytes += len(actual)
            chunks = item.get("chunks", [])
            if not chunks:
                result["errors"].append("sharded original has no chunks")
            cursor = 0
            rebuilt = bytearray()
            chunk_dir = root / item.get("shard_dir", "")
            expected_names = set()
            for index, chunk in enumerate(chunks):
                expected_names.add(Path(chunk["path"]).name)
                if chunk.get("part") != index:
                    result["errors"].append(f"chunk {index}: part field {chunk.get('part')!r}")
                chunk_path = root / chunk["path"]
                if not chunk_path.exists():
                    result["errors"].append(f"chunk missing: {chunk['path']}")
                    continue
                data = chunk_path.read_bytes()
                digest = C.sha256(data)
                if len(data) != chunk.get("bytes"):
                    result["errors"].append(
                        f"chunk {index}: bytes {len(data)} != manifest {chunk.get('bytes')}"
                    )
                if digest != chunk.get("sha256"):
                    result["errors"].append(f"chunk {index}: sha256 mismatch")
                if C.hash_object(chunk_path) != chunk.get("git_blob"):
                    result["errors"].append(f"chunk {index}: git blob id mismatch")
                if chunk.get("byte_start") != cursor:
                    result["errors"].append(
                        f"chunk {index}: byte_start {chunk.get('byte_start')} != cursor {cursor}"
                    )
                if chunk.get("byte_end") != cursor + len(data):
                    result["errors"].append(
                        f"chunk {index}: byte_end {chunk.get('byte_end')} != {cursor + len(data)}"
                    )
                cm = C.chunk_metrics(actual, cursor, cursor + len(data))
                for key in (
                    "bytes",
                    "row_start",
                    "row_end",
                    "starts_mid_row",
                    "ends_mid_row",
                    "newline_count",
                ):
                    if chunk.get(key) != cm[key]:
                        result["errors"].append(
                            f"chunk {index}: {key} manifest={chunk.get(key)!r} independent={cm[key]!r}"
                        )
                if chunk.get("starts_mid_row") or chunk.get("ends_mid_row"):
                    mid_row_splits += 1
                rebuilt.extend(data)
                cursor = cursor + len(data)
                total_chunks += 1
                max_chunk = max(max_chunk, len(data))
            if cursor != len(actual):
                result["errors"].append(
                    f"chunk bytes {cursor} != original bytes {len(actual)}"
                )
            if bytes(rebuilt) != actual:
                result["errors"].append("reassembled bytes differ from original")
            if C.sha256(bytes(rebuilt)) != actual_sha:
                result["errors"].append("reassembled sha256 differs from original")
            reconstructed_lines = rebuilt.count(b"\n") + (
                0 if (not rebuilt or rebuilt.endswith(b"\n")) else 1
            )
            if reconstructed_lines != actual_metrics["line_count"]:
                result["errors"].append(
                    f"reconstructed line count {reconstructed_lines} != {actual_metrics['line_count']}"
                )
            if chunk_dir.exists():
                actual_names = {p.name for p in chunk_dir.glob(C.CHUNK_PREFIX + "*.txt")}
                extras = sorted(actual_names - expected_names)
                if extras:
                    result["errors"].append(f"unexpected chunk files: {extras}")
            else:
                result["errors"].append(f"shard directory missing: {item.get('shard_dir')}")
            result["chunk_count"] = len(chunks)
            result["reconstructed_bytes"] = len(rebuilt)
            result["reconstructed_sha256"] = C.sha256(bytes(rebuilt))
        else:
            direct_count += 1
            if item.get("chunks"):
                result["errors"].append("direct original unexpectedly has chunks")
            if item.get("direct_path") != full:
                result["errors"].append(
                    f"direct path {item.get('direct_path')!r} != pinned source path {full!r}"
                )
            if full not in tree:
                result["errors"].append(f"direct source path missing at pinned ref: {full}")
            else:
                direct = C.read_blob(tree[full]["blob"])
                if direct != actual:
                    result["errors"].append("direct-path bytes differ from pinned source blob")
        result["pass"] = not result["errors"]
        file_results.append(result)

    recomputed = {
        "original_files": len(file_results),
        "sharded_original_files": sharded_count,
        "direct_original_files": direct_count,
        "chunk_count": total_chunks,
        "total_original_bytes": total_bytes,
        "sharded_original_bytes": sharded_bytes,
        "direct_original_bytes": total_bytes - sharded_bytes,
        "max_chunk_bytes": max_chunk,
        "mid_row_split_count": mid_row_splits,
    }
    declared = manifest.get("summary", {})
    summary_keys = [
        "original_files",
        "sharded_original_files",
        "direct_original_files",
        "chunk_count",
        "total_original_bytes",
        "sharded_original_bytes",
        "direct_original_bytes",
        "max_chunk_bytes",
        "mid_row_split_count",
    ]
    summary_errors = {
        key: {"manifest": declared.get(key), "recomputed": recomputed[key]}
        for key in summary_keys
        if declared.get(key) != recomputed[key]
    }
    checks.append(
        {
            "check": "manifest_summary_recomputation",
            "pass": not summary_errors,
            "message": "summary matches independently recomputed values"
            if not summary_errors
            else "manifest summary does not match recomputed values",
            "differences": summary_errors,
        }
    )
    checks.append(
        {
            "check": "all_files",
            "pass": all(r["pass"] for r in file_results),
            "message": f"{sum(1 for r in file_results if r['pass'])}/{len(file_results)} files pass",
            "failed": [r["path"] for r in file_results if not r["pass"]],
        }
    )
    checks.append(
        {
            "check": "chunk_bound",
            "pass": max_chunk <= C.CHUNK_BOUND,
            "message": f"max chunk {max_chunk} <= bound {C.CHUNK_BOUND}",
        }
    )

    candidate_result = None
    if args.candidate:
        if not args.candidate_for:
            raise SystemExit("--candidate requires --candidate-for")
        target = u53f_by_path.get(args.candidate_for)
        if not target:
            raise SystemExit(f"unknown --candidate-for path: {args.candidate_for}")
        full = C.U53F_RETURN + "/" + args.candidate_for
        original = C.read_blob(tree[full]["blob"])
        candidate = Path(args.candidate).read_bytes()
        diff = first_difference(candidate, original)
        same = candidate == original
        candidate_result = {
            "path": args.candidate_for,
            "candidate": str(args.candidate),
            "pass": same,
            "candidate_bytes": len(candidate),
            "original_bytes": len(original),
            "candidate_sha256": C.sha256(candidate),
            "original_sha256": C.sha256(original),
            "first_difference_byte": diff,
            "first_difference_line": (
                C.row_at_offset(original, diff) if diff is not None else None
            ),
            "message": "candidate bytes equal the pinned original"
            if same
            else "candidate bytes differ from the pinned original",
        }
        checks.append(
            {
                "check": "candidate_exact_bytes",
                "pass": same,
                "message": candidate_result["message"],
                "first_difference_byte": diff,
            }
        )

    passed = all(check["pass"] for check in checks)
    payload = {
        "schema": "R53_P53E_CORPUS_VERIFICATION@1",
        "pass": passed,
        "manifest": str(manifest_path),
        "root": str(root),
        "source_ref": args.source_ref,
        "checks": checks,
        "recomputed": recomputed,
        "files": file_results,
        "candidate": candidate_result,
    }
    if args.json_out:
        C.write_json(Path(args.json_out), payload)
    print(json.dumps(
        {
            "pass": passed,
            "checks": {c["check"]: c["pass"] for c in checks},
            "files": f"{sum(1 for r in file_results if r['pass'])}/{len(file_results)}",
            "chunks": total_chunks,
            "bytes": total_bytes,
            "max_chunk": max_chunk,
            "candidate": candidate_result["pass"] if candidate_result else None,
        },
        indent=1,
    ))
    raise SystemExit(0 if passed else 1)


if __name__ == "__main__":
    main()
