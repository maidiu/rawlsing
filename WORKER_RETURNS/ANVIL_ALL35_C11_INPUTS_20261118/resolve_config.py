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
SRC04_CANONICAL = "28630f26b491dcbce411667e3ad285ea42b40abf2d0176056a8a15d1ecad768d"
SRC04_PINS = {
    "v2-historical": {
        "id": "v2-historical",
        "commit": SRC04_REPAIR_COMMIT,
        "path": SRC04_REPAIR_PATH,
        "file_sha256": SRC04_FILE_SHA,
        "canonical_sha256": SRC04_CANONICAL,
        "status": "HISTORICAL_DEFAULT",
        "default_for_frozen_run": True,
    },
    "v3-accepted": {
        "id": "v3-accepted",
        "commit": "35bb18f8e347efa432ffd7d19af9cb419c1f529f",
        "path": "WORKER_RETURNS/ANVIL_SRC04_Q217_MAPPING_20261118/source.config.repaired.v3.json",
        "file_sha256": "f007afdc0cbcd58a3f856121e265a5069f2145cce6c9ce0c112aff1f9c7d7855",
        "canonical_sha256": "a3d3267cc37f7f6d2f6267d777c414f285be58ff5e7ea88b8bc9ac0d74c1269f",
        "status": "SELECTABLE_ACCEPTED",
        "default_for_frozen_run": False,
    },
}


def selected_pin(name):
    pin = SRC04_PINS.get(name)
    if pin is None:
        raise ResolveRefusal(f"UNKNOWN_SRC04_PIN:{name}")
    return pin


def bundle_src04_pin(sc):
    """Accept only v2 historical or v3 accepted bundle config pins."""
    for pin in SRC04_PINS.values():
        if (sc.get("revision_commit"), sc.get("revision_path", sc.get("path")),
                sc.get("file_sha256"), sc.get("canonical_sha256")) == (
                pin["commit"], pin["path"], pin["file_sha256"], pin["canonical_sha256"]):
            return pin
    raise ResolveRefusal("STALE_SRC04_CONFIG_REFUSED")


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


def resolve_one(bundle_path: Path, out_dir: Path | None = None, *, src04_pin: str = "v2-historical"):
    bundle = json.loads(bundle_path.read_text())
    sid = bundle["source_id"]
    sc = bundle["source_config"]
    selected = None
    if sid == "SRC04":
        bundle_pin = bundle_src04_pin(sc)
        selected = selected_pin(src04_pin)
        commit = selected["commit"]
        path = selected["path"]
        expected_file_sha = selected["file_sha256"]
        expected_canonical = selected["canonical_sha256"]
    else:
        commit = sc["revision_commit"]
        path = sc.get("revision_path", sc["path"])
        expected_file_sha = sc["file_sha256"]
        expected_canonical = sc["canonical_sha256"]
    raw = git_bytes(commit, path)
    if sha_bytes(raw) != expected_file_sha:
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
            "canonical_sha": canonical == expected_canonical,
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
            "file_sha256": expected_file_sha,
            "canonical_sha256": canonical,
            "declared_shape": shape(d),
            "checks": checks,
            "selected_pin": selected["id"] if selected else None,
            "selected_pin_status": selected["status"] if selected else None,
            "bundle_pin_accepted": bundle_pin["id"] if selected else None,
            "historical_default": bool(selected and selected["default_for_frozen_run"]),
            "config_materialized": True,
            "original_source_bodies_read": False,
        }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bundles", default=str(HERE / "bundles"))
    ap.add_argument("--source-id")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--out-dir")
    ap.add_argument("--src04-pin", choices=tuple(SRC04_PINS), default="v2-historical")
    args = ap.parse_args()
    bundles = Path(args.bundles)
    if args.all:
        paths = [bundles / f"SRC{i:02d}.json" for i in range(1, 36)]
        rows = [resolve_one(p, src04_pin=args.src04_pin) for p in paths]
        refs = {r["revision_ref"] for r in rows}
        if len(rows) != 35 or len(refs) != 35:
            raise ResolveRefusal("CONFIG_REVISION_COVERAGE_DRIFT")
        print(json.dumps({"status": "PASS", "resolved": len(rows), "distinct_revisions": len(refs), "rows": rows}, sort_keys=True))
        return 0
    if not args.source_id:
        raise SystemExit("--source-id or --all required")
    row = resolve_one(bundles / f"{args.source_id}.json", Path(args.out_dir) if args.out_dir else None, src04_pin=args.src04_pin)
    print(json.dumps(row, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
