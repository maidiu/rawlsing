#!/usr/bin/env python3
"""Reassemble one original or verify all originals from the lossless shards.

Default is check-only.  --out writes the reconstructed bytes to a caller-chosen
path (use a temporary path outside the repository unless you intend to inspect
the result).
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import corpus_common as C


def load_manifest():
    return json.loads((C.P53E_ROOT / "02_LOSSLESS_ORDERED_SHARD_MANIFEST.json").read_text(encoding="utf-8"))


def reassemble(record):
    if record["storage"] != "sharded":
        return C.read_blob(record["git_blob"]), []
    chunks = []
    for chunk in record["chunks"]:
        path = C.P53E_ROOT / chunk["path"]
        data = path.read_bytes()
        if len(data) != chunk["bytes"]:
            raise ValueError(f"{chunk['path']}: size {len(data)} != {chunk['bytes']}")
        if C.sha256(data) != chunk["sha256"]:
            raise ValueError(f"{chunk['path']}: sha256 mismatch")
        chunks.append(data)
    return b"".join(chunks), chunks


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="original path relative to the U53F return root")
    parser.add_argument("--shard-id", help="shard id such as S02_02_ALL_PINNED_TREE_FILES")
    parser.add_argument("--all", action="store_true", help="verify every original")
    parser.add_argument("--out", help="write reconstructed bytes to this path")
    parser.add_argument("--json-out", help="write a JSON receipt")
    args = parser.parse_args()
    manifest = load_manifest()
    by_path = {o["path"]: o for o in manifest["originals"]}
    by_shard = {o.get("shard_id"): o for o in manifest["originals"] if o.get("shard_id")}
    if args.all:
        targets = manifest["originals"]
    elif args.shard_id:
        if args.shard_id not in by_shard:
            raise SystemExit(f"unknown shard id: {args.shard_id}")
        targets = [by_shard[args.shard_id]]
    elif args.path:
        if args.path not in by_path:
            raise SystemExit(f"unknown original path: {args.path}")
        targets = [by_path[args.path]]
    else:
        raise SystemExit("choose --all, --shard-id, or --path")
    results = []
    for record in targets:
        data, chunks = reassemble(record)
        source = C.read_blob(record["git_blob"])
        result = {
            "path": record["path"],
            "storage": record["storage"],
            "shard_id": record.get("shard_id"),
            "chunks": len(chunks),
            "bytes": len(data),
            "sha256": C.sha256(data),
            "expected_bytes": record["actual_bytes"],
            "expected_sha256": record["actual_sha256"],
            "source_blob": record["git_blob"],
            "byte_equal_to_source": data == source,
            "pass": data == source and len(data) == record["actual_bytes"] and C.sha256(data) == record["actual_sha256"],
        }
        results.append(result)
    if args.out:
        if len(results) != 1:
            raise SystemExit("--out requires exactly one target")
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(reassemble(targets[0])[0])
    payload = {
        "schema": "R53_P53E_REASSEMBLY_RECEIPT@1",
        "targets": len(results),
        "passed": sum(1 for r in results if r["pass"]),
        "failed": sum(1 for r in results if not r["pass"]),
        "results": results,
    }
    if args.json_out:
        C.write_json(Path(args.json_out), payload)
    print(json.dumps({k: payload[k] for k in ("targets", "passed", "failed")}, indent=1))
    if len(results) == 1:
        print(json.dumps(results[0], indent=1))
    raise SystemExit(0 if payload["failed"] == 0 else 1)


if __name__ == "__main__":
    main()
