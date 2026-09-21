from __future__ import annotations

import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MATERIALIZER = ROOT / "rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py"

def load_module():
    spec = importlib.util.spec_from_file_location("_hq_lits_runtime_materializer", MATERIALIZER)
    if spec is None or spec.loader is None:
        raise RuntimeError("LiTS runtime materializer import failed")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    mod = load_module()
    catalog, candidates, primitives, queries, definition = mod.catalog_and_frontier()
    rows = []
    for index, candidate in enumerate(candidates):
        rows.append({
            "index": index,
            "candidate_hash": candidate.candidate_hash,
            "candidate_id": candidate.candidate_id,
            "family": candidate.family,
            "rule_id": candidate.rule_id,
            "validation": candidate.validation,
            "winning_predicate_ref": candidate.winning_predicate.ref.as_dict(),
            "query_roles": [
                {
                    "role": role.role,
                    "predicate_ref": role.predicate.ref.as_dict(),
                    "query_ref": role.query.ref.as_dict(),
                }
                for role in candidate.query_roles
            ],
        })
    out = {
        "schema": "FIABC_HQ_LITS_SOURCE_FREE_FRONTIER_PROBE@1.0.0",
        "candidate_count": len(rows),
        "query_role_count": sum(len(x["query_roles"]) for x in rows),
        "runtime_catalog_identity": catalog.receipt()["catalog_identity"],
        "candidates": rows,
        "source_read": False,
        "candidate_execution": False,
        "i03_executed": False,
        "i05_executed": False,
    }
    assert out["candidate_count"] == 50
    assert out["query_role_count"] == 77
    print("FIABC_LITS_SOURCE_FREE_FRONTIER_JSON=" + json.dumps(out, sort_keys=True, separators=(",", ":")))

if __name__ == "__main__":
    main()
