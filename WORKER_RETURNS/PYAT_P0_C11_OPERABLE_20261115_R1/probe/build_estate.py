"""Build the ONE deterministic 128-respondent sourcefree saved estate and battery.

TEST_ONLY.  Reuses the accepted #1006 fixture builder, S2-C direct writer and
S2-B/S2-C identity machinery.  No production file is modified.
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = BASE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from rawlsing_next.pre553_source_direct_parquet_estate import write_direct_estate

from fixture_1006 import ShapeSpec, build_context
from ops import Battery

RESPONDENTS = 128
CHUNK_ROWS = 16
TAG = "PYAT-COUNTRY-REUSE-20261115"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _jsonable(value):
    return json.loads(canonical_json(value))


def main() -> int:
    scratch_root = BASE / ".local-data"
    scratch_root.mkdir(mode=0o700, exist_ok=True)
    scratch_root.chmod(0o700)
    estate_root = scratch_root / f"estate-{RESPONDENTS}"
    if estate_root.exists():
        shutil.rmtree(estate_root)
    estate_root.mkdir(mode=0o700)
    estate_root.chmod(0o700)

    shape = ShapeSpec(
        "country-reuse", RESPONDENTS, include_weights=True, tag=TAG
    )
    ctx = build_context(shape)
    battery = Battery(ctx)
    ops = battery.build(core_count=80, weighted_count=20)
    catalog = battery.catalog()

    receipt = write_direct_estate(
        ctx.direct_sections(), ctx.universe.ref, estate_root,
        chunk_rows=CHUNK_ROWS,
    )
    release_name = Path(receipt.path).name
    release_dir = estate_root / "releases" / release_name
    checksums = {
        path.name: _sha256(path)
        for path in sorted(release_dir.iterdir())
    }
    snapshot = {
        "schema": "PYAT_COUNTRY_REUSE_ESTATE@1",
        "grade": "SOURCEFREE_TEST_ONLY",
        "fixture": {
            "respondents": RESPONDENTS,
            "events": shape.event_count,
            "routing": shape.routing_count,
            "weights": shape.weight_count,
            "family_counts": dict(receipt.family_counts),
            "chunk_rows": CHUNK_ROWS,
            "tag": TAG,
            "questions": ["A", "B", "C", "D", "MR"],
            "typed_missing": "B at index % 17 == 0",
            "routed_sparse": "D eligible at index % 11 == 0",
            "repeated": "MR two occurrences at index % 13 == 0",
        },
        "root": str(estate_root),
        "exact_path": f"releases/{release_name}",
        "manifest_sha256": receipt.manifest_sha256,
        "i02": {
            "logical": receipt.i02.logical,
            "physical": receipt.i02.physical,
            "release": receipt.i02.release,
            "source": receipt.i02.source,
            "replay": receipt.i02.replay,
            "universe": receipt.i02.universe,
            "schema": receipt.i02.schema,
        },
        "reconstructed_v1_release_ref": receipt.reconstructed_v1_release_ref.as_dict(),
        "family_counts": dict(receipt.family_counts),
        "retained_bytes": receipt.retained_bytes,
        "members_sha256": checksums,
        "release_name": release_name,
    }
    (BASE / "evidence").mkdir(exist_ok=True)
    (BASE / "evidence" / "estate_receipt.json").write_text(
        json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    ops_manifest = {
        "schema": "PYAT_COUNTRY_REUSE_OPS@1",
        "grade": "SOURCEFREE_TEST_ONLY",
        "distinct_operations": len(ops),
        "core_operations": len({op.core_id for op in ops}),
        "measure_variants": sum(1 for op in ops if op.measure == "GOVERNED_WEIGHTED"),
        "distinct_query_refs": len({op.query_ref.key for op in ops}),
        "operations": [
            {
                "op_id": op.op_id,
                "query_ref": _jsonable(op.query_ref),
                "predicate_ref": _jsonable(op.predicate_ref),
                "targets": list(op.targets),
                "measure": op.measure,
                "family": op.family,
                "core_id": op.core_id,
                "condition_ast": json.loads(canonical_json(op.condition_ast)),
            }
            for op in ops
        ],
    }
    (BASE / "evidence" / "ops_manifest.json").write_text(
        json.dumps(ops_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "estate_root": str(estate_root),
        "exact_path": snapshot["exact_path"],
        "manifest_sha256": receipt.manifest_sha256,
        "release": snapshot["reconstructed_v1_release_ref"],
        "retained_bytes": receipt.retained_bytes,
        "distinct_ops": len(ops),
        "core_ops": ops_manifest["core_operations"],
        "weighted_variants": ops_manifest["measure_variants"],
        "events": shape.event_count,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
