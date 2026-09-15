from __future__ import annotations

import base64
import csv
import hashlib
import io
import json
import pathlib
import zlib
from collections import Counter, defaultdict

from rawlsing_next import n04_r2_whole_corpus_t03_release as n04r2
from rawlsing_next.prev3_governed_semantic_t03_compiler import compile_governed_semantic_batch

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
RETURN_ROOT = (
    REPO_ROOT
    / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3"
    / "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1"
    / "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1"
    / "ASTRA_PREV3_COMPLETION_AUDIT_R1"
    / "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1"
    / "PSC_FIRST_ACTIVE_WAVE_R1/WORKER_RETURNS/N04-R3"
)

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
N03_REGISTRY_BLOB = "f8220b07c541786f9798cc88d60420b53030d322"

STATUS_CODEBOOK = {
    0: "EMITTED_GOVERNED_T03_CANDIDATE",
    1: "BLOCKED_N03_REVIEW_REQUIRED",
    2: "BLOCKED_N03_TYPED_UNRESOLVED",
    3: "BLOCKED_CURRENT_POSITIVE__MISSING_RESPONSE_CATEGORY_SEMANTICS_REF",
    4: "BLOCKED_CURRENT_POSITIVE__MISSING_ROUTING_APPLICABILITY_REF",
    5: "BLOCKED_CURRENT_POSITIVE__MISSING_AUTHORITY_OWNED_CANDIDATE_KIND",
}

MISSING_RESPONSE_BASIS = (
    "NO_EXACT_CURRENT_RESPONSE_SEMANTICS_BINDING_FOR_IMPLEMENTATION_IN_ACCEPTED_"
    "V550_V551_RESPONSE_SEMANTICS_AUTHORITY"
)
MISSING_ROUTING_BASIS = (
    "N02_R2_EXACT_ID_ROUTING_SIDECAR_REMAINS_UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY"
)
MISSING_CANDIDATE_KIND_BASIS = (
    "EXACT_FQRA_ROW_OWNS_RELATION_OR_SUBJECTIVE_EVIDENCE_SEMANTICS_BUT_NOT_T03_"
    "STRUCTURAL_POSITION_OR_MECHANISM_RULE_CANDIDATE_KIND__BANKED_COMPILER_DEFAULT_"
    "STRUCTURAL_POSITION_IS_NOT_AUTHORITY_TO_MINT_STRUCTURAL_ADMISSION"
)

EXPECTED_EMPTY_STREAM_SHA256 = hashlib.sha256(b"").hexdigest()


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _git_blob(ref: str, path: str) -> str:
    n04r2._ensure_commit(ref)
    proc = n04r2._run("git", "rev-parse", f"{ref}:{path}")
    return proc.stdout.decode().strip()


def _csv_rows(ref: str, path: str):
    raw = n04r2._git_bytes(ref, path)
    return list(csv.DictReader(io.StringIO(raw.decode("utf-8-sig"), newline="")))


def _jurisdictions(row: dict) -> tuple[str, ...]:
    out = []
    if row["fqra_match_count"]:
        out.append("FQRA")
    if row["qsmv2_implementation_match_count"]:
        out.append("QSMV2")
    if row["response_binding_count"]:
        out.append("RESPONSE_SEMANTICS")
    if row["typed_positive_authority_ids"]:
        out.append("TYPED_RELATION")
    return tuple(out)


def build():
    imported = n04r2.verify_imported_implementation()
    ledger, _n03_vec, n03_summary = n04r2._load_n03_r2_replay()
    assert n03_summary["rows"] == 18276
    assert n03_summary["disposition_counts"] == {
        "CURRENT_GOVERNED_POSITIVE": 18213,
        "CURRENT_GOVERNED_REVIEW_REQUIRED": 41,
        "CURRENT_TYPED_UNRESOLVED__EXACT_BASIS": 22,
    }

    assert _git_blob(N03_REGISTRY_COMMIT, N03_REGISTRY_PATH) == N03_REGISTRY_BLOB
    registry = json.loads(n04r2._git_bytes(N03_REGISTRY_COMMIT, N03_REGISTRY_PATH))
    objects = {obj["object_id"]: obj for obj in registry["objects"]}
    fqra_object = objects["FQRA_R1"]
    assert fqra_object["blob_sha"] == "e4f79f47417077c840f985d37e9341f068e3cf8f"
    assert _git_blob(N03_REGISTRY_COMMIT, fqra_object["path"]) == fqra_object["blob_sha"]
    fqra_rows = _csv_rows(N03_REGISTRY_COMMIT, fqra_object["path"])

    accounting = []
    vector = []
    frontier = []
    status_counts = Counter()
    combo_counts = Counter()
    jurisdiction_counts = Counter()
    missing_role_counts = Counter()
    missing_role_by_jurisdiction = Counter()
    frontier_lane_counts = Counter()
    frontier_authority_status_counts = Counter()

    for row in ledger:
        qid = row["question_implementation_id"]
        top = row["top_level_disposition"]
        jurisdictions = _jurisdictions(row)
        combo = "+".join(jurisdictions) if jurisdictions else "NONE"
        missing_roles: tuple[str, ...] = ()
        exact_basis = ""
        frontier_detail = None

        if top == "CURRENT_GOVERNED_REVIEW_REQUIRED":
            code = 1
            exact_basis = "EXACT_QSMV2_BLOCKED_IMPLEMENTATION__PRESERVE_REVIEW_REQUIRED"
        elif top == "CURRENT_TYPED_UNRESOLVED__EXACT_BASIS":
            code = 2
            exact_basis = row["unresolved_basis"]
        elif top == "CURRENT_GOVERNED_POSITIVE":
            combo_counts[combo] += 1
            for jurisdiction in jurisdictions:
                jurisdiction_counts[jurisdiction] += 1
            if not row["response_binding_count"]:
                code = 3
                missing_roles = ("response_category_semantics_ref",)
                exact_basis = MISSING_RESPONSE_BASIS
            elif row["routing_disposition"] == "UNRESOLVED_ROUTING_APPLICABILITY_AUTHORITY":
                code = 4
                missing_roles = ("routing_applicability_ref",)
                exact_basis = MISSING_ROUTING_BASIS
            else:
                # Every current-positive implementation that survives response and routing
                # gates is exact FQRA-backed at this accepted authority state.  Preserve the
                # FQRA row as authority; do not reinterpret its lane into a T03 kind.
                assert row["fqra_match_count"] == 1
                assert len(row["fqra_row_numbers"]) == 1
                fqra_row_number = int(row["fqra_row_numbers"][0])
                fqra = fqra_rows[fqra_row_number - 1]
                assert (fqra.get("p2_question_implementation_id") or "").strip() == qid
                assert (fqra.get("p2_response_binding_status") or "").strip() == "bound"
                assert (fqra.get("p2_directional_certification_status") or "").strip() == "CERTIFIED"
                assert (fqra.get("structural_adjudication_required") or "").strip() == "NO"
                lane = (fqra.get("p2_semantic_lane") or "").strip()
                assert lane in {"relation", "subjective_evidence"}
                assert "candidate_kind" not in fqra
                authority_status = (fqra.get("authority_status_final_or_current") or "").strip()
                assert authority_status in {"GOVERNED_MANUAL_RELATION_AUTHORITY", "FROZEN_ACCEPTED_GSS"}
                code = 5
                missing_roles = ("candidate_kind",)
                exact_basis = MISSING_CANDIDATE_KIND_BASIS
                frontier_lane_counts[lane] += 1
                frontier_authority_status_counts[authority_status] += 1
                frontier_detail = {
                    "question_implementation_id": qid,
                    "source_family": row["source_family"],
                    "wave": row["wave"],
                    "source_variable_code": row["source_variable_code"],
                    "fqra_row_number": fqra_row_number,
                    "fqra_authority_status": authority_status,
                    "fqra_semantic_lane": lane,
                    "fqra_semantic_role": (fqra.get("p2_semantic_role") or "").strip(),
                    "fqra_semantic_subrole": (fqra.get("p2_semantic_subrole") or "").strip(),
                    "fqra_relation_axis_id": (fqra.get("relation_axis_id") or "").strip(),
                    "response_registry_key_indices": row["response_registry_key_indices"],
                    "routing_authority_code": row["routing_authority_code"],
                    "routing_disposition": row["routing_disposition"],
                    "routing_scope": row["routing_scope"],
                    "typed_positive_authority_ids": row["typed_positive_authority_ids"],
                    "missing_role": "candidate_kind",
                    "exact_basis": MISSING_CANDIDATE_KIND_BASIS,
                }
                frontier.append(frontier_detail)
        else:
            raise AssertionError(f"unexpected N03 disposition for {qid}: {top}")

        status = STATUS_CODEBOOK[code]
        status_counts[status] += 1
        for role in missing_roles:
            missing_role_counts[role] += 1
            for jurisdiction in jurisdictions:
                missing_role_by_jurisdiction[f"{role}|{jurisdiction}"] += 1
        vector.append(code)
        accounting.append({
            "question_implementation_id": qid,
            "n03_top_level_disposition": top,
            "governing_jurisdictions": list(jurisdictions),
            "binding_status": status,
            "smallest_exact_missing_roles": list(missing_roles),
            "smallest_exact_basis": exact_basis,
        })

    assert len(accounting) == 18276
    assert len({row["question_implementation_id"] for row in accounting}) == 18276
    assert sum(status_counts.values()) == 18276
    assert status_counts["EMITTED_GOVERNED_T03_CANDIDATE"] == 0

    compiled_empty = compile_governed_semantic_batch(())
    assert compiled_empty.compiled == ()
    assert compiled_empty.reduction_groups == ()
    assert compiled_empty.reduction.aggregates == ()
    assert compiled_empty.reduction.quarantines == ()

    canonical_accounting = b"".join(
        (json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n").encode()
        for row in accounting
    )
    raw_vector = bytes(vector)
    vector_b64 = base64.b64encode(zlib.compress(raw_vector, 9))
    frontier_sorted = sorted(frontier, key=lambda item: item["question_implementation_id"])
    frontier_ids = [item["question_implementation_id"] for item in frontier_sorted]
    frontier_stream = ("\n".join(frontier_ids) + ("\n" if frontier_ids else "")).encode()

    summary = {
        "rows": 18276,
        "unique_ids": 18276,
        "positive_t03_candidates": 0,
        "positive_candidate_sorted_id_stream_sha256": EXPECTED_EMPTY_STREAM_SHA256,
        "status_counts": dict(sorted(status_counts.items())),
        "smallest_missing_role_counts": dict(sorted(missing_role_counts.items())),
        "positive_jurisdiction_combo_counts": dict(sorted(combo_counts.items())),
        "positive_jurisdiction_membership_counts": dict(sorted(jurisdiction_counts.items())),
        "smallest_missing_role_by_jurisdiction_counts": dict(sorted(missing_role_by_jurisdiction.items())),
        "candidate_kind_frontier_count": len(frontier_sorted),
        "candidate_kind_frontier_sorted_id_stream_sha256": sha256(frontier_stream),
        "candidate_kind_frontier_lane_counts": dict(sorted(frontier_lane_counts.items())),
        "candidate_kind_frontier_authority_status_counts": dict(sorted(frontier_authority_status_counts.items())),
        "accounting_canonical_jsonl_bytes": len(canonical_accounting),
        "accounting_canonical_jsonl_sha256": sha256(canonical_accounting),
        "status_vector_raw_bytes": len(raw_vector),
        "status_vector_raw_sha256": sha256(raw_vector),
        "status_vector_zlib_b64_bytes": len(vector_b64),
        "status_vector_zlib_b64_sha256": sha256(vector_b64),
        "n03_canonical_jsonl_sha256": n03_summary["ledger_canonical_jsonl_sha256"],
        "n01_full_csv_sha256": n03_summary["n01_full_csv_sha256"],
        "n02_canonical_row_jsonl_sha256": n03_summary["n02_canonical_row_jsonl_sha256"],
        "banked_compiler_blob": imported["rawlsing_next/prev3_governed_semantic_t03_compiler.py"],
        "banked_compiler_replay_records": 0,
        "terminal": "PASS__ZERO_BINDABLE_RECORDS__EXACT_ROLE_LEVEL_RESIDUALS_PROVED",
    }
    return accounting, raw_vector, vector_b64, frontier_sorted, summary


if __name__ == "__main__":
    _accounting, _vector, _vector_b64, _frontier, summary = build()
    print(json.dumps(summary, sort_keys=True, indent=2))
