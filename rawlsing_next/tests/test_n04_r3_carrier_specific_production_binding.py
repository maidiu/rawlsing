from __future__ import annotations

import base64
import json
import zlib

from rawlsing_next.n04_r3_carrier_specific_production_binding import (
    MISSING_CANDIDATE_KIND_BASIS,
    RETURN_ROOT,
    STATUS_CODEBOOK,
    build,
    sha256,
)
from rawlsing_next._prev3_structural_batch_base import CandidateKind
from rawlsing_next.prev3_governed_semantic_t03_compiler import GovernedSemanticCapitalRecord


FRONTIER_COMPACT_FIELDS = (
    "question_implementation_id",
    "fqra_row_number",
    "fqra_authority_status",
    "fqra_semantic_lane",
    "source_family",
    "wave",
    "source_variable_code",
)


def test_n04_r3_carrier_specific_production_binding_and_t03_rerelease():
    accounting, vector, vector_b64, frontier, summary = build()
    manifest = json.loads((RETURN_ROOT / "01_BINDING_AUTHORITY_MANIFEST.json").read_text())
    expected = manifest.get("expected_output")

    assert len(accounting) == 18276
    assert len({row["question_implementation_id"] for row in accounting}) == 18276
    assert summary["status_counts"] == {
        "BLOCKED_CURRENT_POSITIVE__MISSING_AUTHORITY_OWNED_CANDIDATE_KIND": 42,
        "BLOCKED_CURRENT_POSITIVE__MISSING_RESPONSE_CATEGORY_SEMANTICS_REF": 18012,
        "BLOCKED_CURRENT_POSITIVE__MISSING_ROUTING_APPLICABILITY_REF": 159,
        "BLOCKED_N03_REVIEW_REQUIRED": 41,
        "BLOCKED_N03_TYPED_UNRESOLVED": 22,
    }
    assert summary["smallest_missing_role_counts"] == {
        "candidate_kind": 42,
        "response_category_semantics_ref": 18012,
        "routing_applicability_ref": 159,
    }
    assert summary["positive_t03_candidates"] == 0
    assert summary["candidate_kind_frontier_count"] == 42
    assert set(summary["candidate_kind_frontier_lane_counts"]) <= {"relation", "subjective_evidence"}
    assert sum(summary["candidate_kind_frontier_lane_counts"].values()) == 42
    assert summary["candidate_kind_frontier_authority_status_counts"] == {
        "FROZEN_ACCEPTED_GSS": 7,
        "GOVERNED_MANUAL_RELATION_AUTHORITY": 35,
    }
    assert summary["positive_jurisdiction_combo_counts"] == {
        "FQRA": 12553,
        "FQRA+QSMV2": 1780,
        "FQRA+QSMV2+RESPONSE_SEMANTICS": 7,
        "FQRA+QSMV2+RESPONSE_SEMANTICS+TYPED_RELATION": 4,
        "FQRA+QSMV2+TYPED_RELATION": 2606,
        "FQRA+RESPONSE_SEMANTICS": 114,
        "FQRA+RESPONSE_SEMANTICS+TYPED_RELATION": 76,
        "FQRA+TYPED_RELATION": 1069,
        "TYPED_RELATION": 4,
    }
    assert summary["terminal"] == "PASS__ZERO_BINDABLE_RECORDS__EXACT_ROLE_LEVEL_RESIDUALS_PROVED"

    # The banked dataclass does have a STRUCTURAL_POSITION default. N04-R3 must
    # not launder that implementation default into authority for these FQRA rows.
    assert GovernedSemanticCapitalRecord.__dataclass_fields__["candidate_kind"].default is CandidateKind.STRUCTURAL_POSITION
    assert all(item["missing_role"] == "candidate_kind" for item in frontier)
    assert all(item["exact_basis"] == MISSING_CANDIDATE_KIND_BASIS for item in frontier)
    assert all(item["fqra_semantic_lane"] in {"relation", "subjective_evidence"} for item in frontier)

    if expected is None:
        discovery = {
            "summary": summary,
            "status_vector_zlib_b64": vector_b64.decode(),
            "frontier": frontier,
        }
        raise AssertionError(
            "N04R3_FINAL_DISCOVERY_JSON="
            + json.dumps(discovery, sort_keys=True, separators=(",", ":"))
        )

    assert summary == expected
    committed_vector_b64 = (RETURN_ROOT / "03_CURRENT_18276_BINDING_STATUS_VECTOR.zlib.b64").read_bytes().strip()
    assert committed_vector_b64 == vector_b64
    assert zlib.decompress(base64.b64decode(committed_vector_b64)) == vector

    codebook = json.loads((RETURN_ROOT / "02_BINDING_STATUS_CODEBOOK.json").read_text())
    assert {int(k): v for k, v in codebook["codes"].items()} == STATUS_CODEBOOK

    committed_frontier = json.loads((RETURN_ROOT / "04_CANDIDATE_KIND_FRONTIER_42.json").read_text())
    assert committed_frontier["count"] == 42
    assert committed_frontier["missing_role"] == "candidate_kind"
    assert committed_frontier["exact_basis"] == MISSING_CANDIDATE_KIND_BASIS
    expected_compact = [
        {field: item[field] for field in FRONTIER_COMPACT_FIELDS}
        for item in frontier
    ]
    assert committed_frontier["records"] == expected_compact
    ids = [item["question_implementation_id"] for item in frontier]
    stream = ("\n".join(ids) + "\n").encode()
    assert committed_frontier["sorted_id_stream_sha256"] == sha256(stream)

    # The complete 18,276-ID accounting is repo-bound as an exact deterministic
    # projection over the accepted N03-R2 ledger plus the committed status vector.
    # Reconstruct its canonical byte stream here and prove the sealed contract.
    accounting_contract = json.loads(
        (RETURN_ROOT / "06_CURRENT_18276_BINDING_ACCOUNTING_RECONSTRUCTION_CONTRACT.json").read_text()
    )
    canonical_accounting = b"".join(
        (json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n").encode()
        for row in accounting
    )
    assert accounting_contract["rows"] == 18276
    assert accounting_contract["unique_ids"] == 18276
    assert accounting_contract["canonical_jsonl_bytes"] == len(canonical_accounting)
    assert accounting_contract["canonical_jsonl_sha256"] == sha256(canonical_accounting)
    assert accounting_contract["canonical_jsonl_bytes"] == summary["accounting_canonical_jsonl_bytes"]
    assert accounting_contract["canonical_jsonl_sha256"] == summary["accounting_canonical_jsonl_sha256"]
    assert accounting_contract["status_vector"]["raw_sha256"] == summary["status_vector_raw_sha256"]
    assert accounting_contract["status_vector"]["encoded_sha256_without_trailing_newline"] == summary["status_vector_zlib_b64_sha256"]
    assert accounting_contract["ordered_authority_surface"]["ledger_canonical_jsonl_sha256"] == summary["n03_canonical_jsonl_sha256"]

    receipt = json.loads((RETURN_ROOT / "05_VALIDATION_RECEIPT.json").read_text())
    assert receipt["terminal"] == "PASS"
    assert receipt["terminal_code"] == "N04_R3_CARRIER_SPECIFIC_PRODUCTION_BINDING_AND_T03_RERELEASE_COMPLETE__RETURN_TO_HQ"
    assert receipt["accounting_canonical_jsonl_sha256"] == summary["accounting_canonical_jsonl_sha256"]
    assert receipt["candidate_kind_frontier_sorted_id_stream_sha256"] == summary["candidate_kind_frontier_sorted_id_stream_sha256"]
