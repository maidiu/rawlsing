#!/usr/bin/env python3
"""Resolve exact R157 SourceConfig revisions from the all-35 package bundles.

This is a consumer of the producer's one package format. It reads only the
immutable revision refs recorded in each bundle, materializes metadata through
the current parser, and verifies the config against the bundle's wave, source
SHA and shape. It never opens respondent/source body bytes.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
SRC04_REPAIR_COMMIT = "da23c65d1e211cb7e8ce416e98757f321b78d25e"
SRC04_REPAIR_PATH = "rawlsing_next/source_configuration/data/SRC04/source.config.repaired.v2.json"
SRC04_FILE_SHA = "5e107de4baf43f11a2a3e739e05481d8008de6f90951e86a170fb4d804ef3ff5"


class ResolveRefusal(ValueError):
    pass


def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_bytes(commit: str, path: str) -> bytes:
    try:
        return subprocess.check_output(
            ["git", "-C", str(REPO), "show", f"{commit}:{path}"],
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        raise ResolveRefusal(f"CONFIG_GIT_MATERIALIZATION_FAILED:{commit}:{path}") from exc


def shape(document):
    return {
        "rows": document["identity"]["source_row_count"],
        "columns": document["identity"]["source_column_count"],
        "original_items": document["identity"]["original_item_count"],
        "physical_slots": len(document["physical_slots"]),
        "questions": len(document["questions"]),
        "response_slots": len(document["response_slots"]),
        "coordinate_slots": len(document["coordinate_slots"]),
        "weight_slots": len(document["weight_slots"]),
        "routing_rules": len(document["routing"]),
    }


def expected_shape(bundle):
    c = bundle["counts"]
    return {
        "rows": bundle["declared_rows"],
        "columns": bundle["declared_columns"],
        "original_items": c["original_items"],
        "physical_slots": c["physical_slots"],
        "questions": c["questions"],
        "response_slots": c["response_slots"],
        "coordinate_slots": c["coordinate_slots"],
        "weight_slots": c["weight_slots"],
        "routing_rules": c["routing_rules"],
    }


def resolve_one(bundle_path: Path, out_dir: Path | None = None):
    bundle = json.loads(bundle_path.read_text())
    sid = bundle["source_id"]
    sc = bundle["source_config"]
    commit = sc["revision_commit"]
    path = sc.get("revision_path", sc["path"])
    if sid == "SRC04" and (commit, path, sc["file_sha256"]) != (
        SRC04_REPAIR_COMMIT, SRC04_REPAIR_PATH, SRC04_FILE_SHA,
    ):
        raise ResolveRefusal("STALE_SRC04_CONFIG_REFUSED")
    raw = git_bytes(commit, path)
    if sha_bytes(raw) != sc["file_sha256"]:
        raise ResolveRefusal(f"CONFIG_FILE_SHA_MISMATCH:{sid}")
    with tempfile.TemporaryDirectory(prefix="anvil-config-resolve-") as tmp:
        staged = Path(tmp) / f"{sid}.config.json"
        staged.write_bytes(raw)
        from rawlsing_next.pre553_r157_projection_adapter import (
            canonical_config_hash, load_source_config,
        )
        config = load_source_config(staged)
        canonical = canonical_config_hash(config)
        d = config.document
        checks = {
            "source_id": config.source_id == sid == bundle["source_id"],
            "identity_class": config.identity_class == "ORIGINAL_SOURCE",
            "source_sha": config.active_source_sha256 == bundle["source_sha256"],
            "expected_source_sha": d["identity"]["expected_source_sha256"] == bundle["source_sha256"],
            "row_count": d["binding"]["row_count"] == bundle["declared_rows"],
            "wave": d["identity"]["wave"] == bundle["wave"],
            "shape": shape(d) == expected_shape(bundle),
            "canonical_sha": canonical == sc["canonical_sha256"],
        }
        if not all(checks.values()):
            raise ResolveRefusal(f"CONFIG_BINDING_MISMATCH:{sid}:{json.dumps(checks, sort_keys=True)}")
        if out_dir is not None:
            out_dir.mkdir(parents=True, exist_ok=True)
            (out_dir / f"{sid}.config.json").write_bytes(raw)
        return {
            "source_id": sid,
            "wave": d["identity"]["wave"],
            "revision_ref": f"{commit}:{path}",
            "file_sha256": sc["file_sha256"],
            "canonical_sha256": canonical,
            "declared_shape": shape(d),
            "checks": checks,
            "config_materialized": True,
            "original_source_bodies_read": False,
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundles", default=str(HERE / "bundles"))
    ap.add_argument("--source-id")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out-dir")
    args = ap.parse_args()
    bundles = Path(args.bundles)
    if args.all:
        paths = [bundles / f"SRC{i:02d}.json" for i in range(1, 36)]
        rows = [resolve_one(p) for p in paths]
        refs = {r["revision_ref"] for r in rows}
        if len(rows) != 35 or len(refs) != 35:
            raise ResolveRefusal("CONFIG_REVISION_COVERAGE_DRIFT")
        print(json.dumps({"status": "PASS", "resolved": len(rows), "distinct_revisions": len(refs), "rows": rows}, sort_keys=True))
        return 0
    if not args.source_id:
        raise SystemExit("--source-id or --all required")
    row = resolve_one(bundles / f"{args.source_id}.json", Path(args.out_dir) if args.out_dir else None)
    print(json.dumps(row, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
