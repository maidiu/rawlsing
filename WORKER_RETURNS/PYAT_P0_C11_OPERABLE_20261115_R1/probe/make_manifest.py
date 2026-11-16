"""Generate the return manifest with exact file hashes and source pins."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    files = []
    for path in sorted(BASE.rglob("*")):
        if not path.is_file():
            continue
        relative = path.relative_to(BASE).as_posix()
        if relative.startswith(".local-data/") or "__pycache__" in relative:
            continue
        if relative == "MANIFEST.json":
            continue
        files.append({
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": sha(path),
        })
    document = {
        "schema": "PYAT_COUNTRY_REUSE_COURT_MANIFEST@1",
        "status": "COURT_MEASURED__COLD_MANY_OPERATION_REUSE_NOT_QUALIFIED__HANDOFF_READY",
        "grade": "SOURCEFREE_TEST_ONLY",
        "g5": "PENDING_DISTINCT_REVIEW",
        "worktree": str(BASE.parents[1]),
        "branch": "agent/pyat-country-reuse-court-20261115",
        "frozen_head": "9d96a9cac7d10f59f2c30d8045dd1696fa3ab969",
        "accepted_writer": "b7b697b69f0acea12174937ee824c19ac34ac284",
        "accepted_1006_author": "2beb2b894076510cdedf8981aa73d15eafc7c816",
        "accepted_1006_code": "1ca1c735a577a7524a0a26c15df8879cd88704e3",
        "accepted_1006_g5": "3e0ed0794498506520ae62c997a5c852ac672061",
        "voskres_corrected_accounting": "7ebd363dedc36cdc34b3a6ef53e32603f291c84e",
        "runtime": {
            "python": "3.11.3",
            "pyarrow": "22.0.0",
            "duckdb": "1.5.2",
            "pyreadstat": "1.3.2",
            "numpy": "2.3.2",
            "pandas": "2.3.1",
        },
        "result": {
            "distinct_cold_operations": 100,
            "cold_wall_seconds": 51.92870779597433,
            "cold_ops_per_second": 1.9257170887613015,
            "row_group_reads": 43130,
            "compressed_row_bytes": 576774322,
            "uncompressed_row_bytes": 2363218327,
            "cold_vs_native_exact": True,
            "in_memory_grouped_core_builds": 80,
            "in_memory_grouped_core_hits": 20,
            "cold_grouped_guard": "REFUSED",
            "thousand_distinct_cold": "NOT_RUN__FORECAST_519.3s_OVER_300s_BUDGET",
        },
        "files": files,
    }
    (BASE / "MANIFEST.json").write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps({
        "files": len(files),
        "bytes": sum(item["bytes"] for item in files),
        "manifest": str(BASE / "MANIFEST.json"),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
