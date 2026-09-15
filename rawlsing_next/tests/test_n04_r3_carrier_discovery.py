from __future__ import annotations

import csv
import io
import json
from collections import Counter

from rawlsing_next import n04_r2_whole_corpus_t03_release as n04r2

N03_REGISTRY_COMMIT = "497b8dfc6106e2761c61d07d8ba9ea472062892c"
N03_REGISTRY_PATH = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "ASTRA_PREV3_COMPLETION_AUDIT_R1/"
    "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/"
    "PSC_FIRST_ACTIVE_WAVE_R1/WORKER_RETURNS/N03/"
    "01_CURRENT_SEMANTIC_AUTHORITY_OBJECT_REGISTRY_R1.json"
)
OBJECT_IDS = (
    "FQRA_R1",
    "QSMV2_IMPLEMENTATION_AUTHORITY_4438",
    "V550_V551_RESPONSE_SEMANTICS_BINDING",
    "JOB3_R3_POSITIVE_1190",
)
TOKENS = ("status", "class", "kind", "type", "schema", "ceiling", "semantic", "relation", "authority", "current", "eligible", "use")


def _csv_rows(path: str):
    raw = n04r2._git_bytes(N03_REGISTRY_COMMIT, path)
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))


def _compact_values(rows, headers):
    out = {}
    for h in headers:
        if not any(t in h.lower() for t in TOKENS):
            continue
        vals = sorted({(r.get(h) or "").strip() for r in rows})
        if len(vals) <= 16:
            out[h] = vals
    return out


def test_n04_r3_exact_carrier_discovery_only():
    ledger, _vec, summary = n04r2._load_n03_r2_replay()
    reg = json.loads(n04r2._git_bytes(N03_REGISTRY_COMMIT, N03_REGISTRY_PATH))
    objs = {o["object_id"]: o for o in reg["objects"]}

    combo_counts = Counter()
    route_counts = Counter()
    positive_rows = [r for r in ledger if r["top_level_disposition"] == "CURRENT_GOVERNED_POSITIVE"]
    for r in positive_rows:
        j = []
        if r["fqra_match_count"]:
            j.append("FQRA")
        if r["qsmv2_implementation_match_count"]:
            j.append("QSMV2")
        if r["response_binding_count"]:
            j.append("RESPONSE")
        if r["typed_positive_authority_ids"]:
            j.append("TYPED")
        combo = "+".join(j) if j else "NONE"
        combo_counts[combo] += 1
        route_counts[(combo, r["routing_disposition"])] += 1

    object_probe = {}
    for oid in OBJECT_IDS:
        o = objs[oid]
        rows = _csv_rows(o["path"])
        headers = list(rows[0].keys()) if rows else []
        object_probe[oid] = {
            "rows": len(rows),
            "registry_jurisdiction": o.get("jurisdiction"),
            "registry_epistemic_class": o.get("epistemic_class"),
            "registry_compile_disposition": o.get("compile_disposition"),
            "registry_negative_ceiling": o.get("negative_ceiling"),
            "registry_keys": sorted(o),
            "headers": headers,
            "compact_role_like_values": _compact_values(rows, headers),
            "first_row": {k: (v[:240] if isinstance(v, str) else v) for k, v in (rows[0] if rows else {}).items()},
        }

    discovery = {
        "n03_summary": summary,
        "positive_rows": len(positive_rows),
        "positive_jurisdiction_combo_counts": dict(sorted(combo_counts.items())),
        "positive_combo_routing_counts": {
            f"{combo}|{route}": n for (combo, route), n in sorted(route_counts.items())
        },
        "objects": object_probe,
    }
    raise AssertionError("N04R3_DISCOVERY_JSON=" + json.dumps(discovery, sort_keys=True, separators=(",", ":")))
