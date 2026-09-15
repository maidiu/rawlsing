from __future__ import annotations

import base64
import json
import zlib

from rawlsing_next.n04_r2_whole_corpus_t03_release import (
    EXPECTED_EMPTY_POSITIVE_ID_STREAM_SHA256,
    EXPECTED_STATUS_VECTOR_B64_SHA256,
    EXPECTED_STATUS_VECTOR_RAW_SHA256,
    PRODUCTION_BINDING_BLOCKER,
    PRODUCTION_BINDING_MISSING_PROOF,
    RETURN_ROOT,
    STATUS_CODEBOOK,
    build_whole_corpus_status,
)


def test_n04_r2_whole_current_corpus_t03_release_status_surface():
    rows, vector, vb64, summary = build_whole_corpus_status()

    assert len(rows) == 18276
    assert len({row["question_implementation_id"] for row in rows}) == 18276
    assert summary["rows"] == 18276
    assert summary["unique_ids"] == 18276
    assert summary["positive_t03_candidates"] == 0
    assert (
        summary["positive_candidate_sorted_id_stream_sha256"]
        == EXPECTED_EMPTY_POSITIVE_ID_STREAM_SHA256
    )
    assert summary["status_counts"] == {
        "BLOCKED_CURRENT_POSITIVE__MISSING_HQ_ADOPTED_PRODUCTION_PREMISE_BINDING": 18213,
        "BLOCKED_N03_REVIEW_REQUIRED": 41,
        "BLOCKED_N03_TYPED_UNRESOLVED": 22,
    }
    assert summary["status_vector_raw_sha256"] == EXPECTED_STATUS_VECTOR_RAW_SHA256
    assert summary["status_vector_zlib_b64_sha256"] == EXPECTED_STATUS_VECTOR_B64_SHA256
    assert summary["positive_status_residual"] == PRODUCTION_BINDING_BLOCKER
    assert summary["smallest_missing_proof"] == PRODUCTION_BINDING_MISSING_PROOF

    committed = (
        RETURN_ROOT / "03_CURRENT_18276_T03_RELEASE_STATUS_VECTOR.zlib.b64"
    ).read_bytes().strip()
    assert committed == vb64
    assert zlib.decompress(base64.b64decode(committed)) == vector

    codebook = json.loads((RETURN_ROOT / "02_RELEASE_STATUS_CODEBOOK.json").read_text())
    assert {int(k): v for k, v in codebook["codes"].items()} == STATUS_CODEBOOK

    manifest = json.loads((RETURN_ROOT / "01_RELEASE_AUTHORITY_MANIFEST.json").read_text())
    assert manifest["expected_output"]["status_vector_raw_sha256"] == EXPECTED_STATUS_VECTOR_RAW_SHA256
    assert manifest["expected_output"]["status_vector_zlib_b64_sha256"] == EXPECTED_STATUS_VECTOR_B64_SHA256
    assert manifest["expected_output"]["positive_t03_candidates"] == 0
    assert manifest["expected_output"]["status_counts"] == summary["status_counts"]

    assert all(
        not row["t03_positive_candidate_emitted"]
        for row in rows
    )
    assert all(
        row["residual_basis"] == PRODUCTION_BINDING_BLOCKER
        and row["smallest_missing_proof"] == PRODUCTION_BINDING_MISSING_PROOF
        for row in rows
        if row["n03_top_level_disposition"] == "CURRENT_GOVERNED_POSITIVE"
    )
