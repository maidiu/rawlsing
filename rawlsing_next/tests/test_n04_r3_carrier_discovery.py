from __future__ import annotations

import csv
import io
import json
from collections import Counter, defaultdict

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

FIELDS = (
    "authority_status_final_or_current",
    "authority_status",
    "relation_use_status_final",
    "coordinate_governance_status",
    "mapping_status",
    "p2_authority_status",
    "p2_deep_review_status",
    "p2_response_binding_status",
    "p2_semantic_lane",
    "p2_semantic_role",
    "p2_semantic_subrole",
    "p2_response_topology",
    "p2_directional_certification_status",
    "p2_current_directional_atom_eligible",
    "manual_semantic_lane",
    "manual_semantic_role",
    "manual_semantic_subrole",
    "manual_response_topology",
    "manual_directional_certification_status",
    "manual_current_directional_atom_eligible",
    "structural_adjudication_required",
    "structural_domain_id",
    "relation_axis_id",
    "target_entity_id",
)


def _rows(path: str):
    raw = n04r2._git_bytes(N03_REGISTRY_COMMIT, path)
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))


def test_n04_r3_targeted_fqra_production_candidate_discovery():
    ledger, _vec, summary = n04r2._load_n03_r2_replay()
    reg = json.loads(n04r2._git_bytes(N03_REGISTRY_COMMIT, N03_REGISTRY_PATH))
    objs = {o["object_id"]: o for o in reg["objects"]}
    fqra = _rows(objs["FQRA_R1"]["path"])
    typed = _rows(objs["JOB3_R3_POSITIVE_1190"]["path"])
    typed_by_id = defaultdict(list)
    for tr in typed:
        for q in json.loads(tr["member_implementation_ids_json"]):
            typed_by_id[q].append({
                "authority_id": tr["authority_id"],
                "relation_type": tr["relation_type"],
                "rule_id": tr["rule_id"],
                "authority_origin": tr["authority_origin"],
            })

    candidates = []
    signatures = Counter()
    sig_ids = defaultdict(list)
    for row in ledger:
        if row["top_level_disposition"] != "CURRENT_GOVERNED_POSITIVE":
            continue
        if not row["fqra_match_count"] or not row["response_binding_count"]:
            continue
        if row["routing_disposition"] == "UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY":
            continue
        q = row["question_implementation_id"]
        selected = [fqra[int(n)-1] for n in row["fqra_row_numbers"]]
        assert all((r.get("p2_question_implementation_id") or "").strip() == q for r in selected)
        compact = []
        for r in selected:
            compact.append({k: (r.get(k) or "").strip() for k in FIELDS})
        sig = tuple(tuple((k, c[k]) for k in FIELDS) for c in compact)
        signatures[sig] += 1
        if len(sig_ids[sig]) < 12:
            sig_ids[sig].append(q)
        candidates.append({
            "id": q,
            "source_family": row["source_family"],
            "wave": row["wave"],
            "source_variable_code": row["source_variable_code"],
            "routing_disposition": row["routing_disposition"],
            "routing_authority_code": row["routing_authority_code"],
            "routing_scope": row["routing_scope"],
            "response_registry_key_indices": row["response_registry_key_indices"],
            "fqra_rows": row["fqra_row_numbers"],
            "fqra_compact": compact,
            "typed": typed_by_id.get(q, []),
        })

    sig_out = []
    for sig, count in signatures.most_common():
        sig_out.append({
            "count": count,
            "ids_sample": sig_ids[sig],
            "fqra_compact": [dict(x) for x in sig],
        })

    out = {
        "n03_summary_digest": summary["ledger_canonical_jsonl_sha256"],
        "candidate_count": len(candidates),
        "fqra_match_count_distribution": dict(sorted(Counter(len(c["fqra_rows"]) for c in candidates).items())),
        "routing_counts": dict(sorted(Counter(c["routing_disposition"] for c in candidates).items())),
        "typed_membership_count": sum(bool(c["typed"]) for c in candidates),
        "signature_count": len(sig_out),
        "signatures": sig_out,
        "candidates": candidates,
    }
    raise AssertionError("N04R3_TARGETED_JSON=" + json.dumps(out, sort_keys=True, separators=(",", ":")))
