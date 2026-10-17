from __future__ import annotations

import copy
import hashlib

from rawlsing_next.fiabc_p2_terminal_verifier import (
    INPUT_SCHEMA,
    I05_COVERAGE_CLAIM,
    verify_final_p2_terminal,
)


def _hash(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(source: str) -> dict[str, str]:
    return {
        "kind": "EmpiricalFact",
        "object_id": f"urn:test:{source}:fact",
        "content_hash": _hash(f"{source}:fact"),
    }


def _fact_manifest(source: str) -> list[dict[str, object]]:
    return [{"ref": _ref(source), "typed_state": "EVALUATED_SUPPORTED"}]


def _c11(source: str) -> dict[str, object]:
    return {
        "status": "PASS",
        "logical_release_identity": _hash(f"{source}:c11"),
        "replay_identity": _hash(f"{source}:c11:replay"),
    }


def _i03(source: str) -> dict[str, object]:
    return {
        "status": "PASS",
        "replay_identity": _hash(f"{source}:i03:replay"),
        "fact_manifest": _fact_manifest(source),
    }


def _terminal(source: str) -> dict[str, object]:
    return {
        "source_identity": _hash(f"{source}:source"),
        "workload_identity": _hash(f"{source}:workload"),
        "authority_closure_identity": _hash(f"{source}:authority"),
        "frontier_identity": _hash(f"{source}:frontier"),
        "coverage_receipt_identity": _hash(f"{source}:coverage"),
        "learned_product_identity": _hash(f"{source}:product"),
        "semantic_identity": _hash(f"{source}:semantic"),
        "replay_identity": _hash(f"{source}:terminal:replay"),
        "output_identity": _hash(f"{source}:output"),
        "coverage_claim": I05_COVERAGE_CLAIM,
        "candidate_count": 3,
        "covered_candidate_count": 3,
        "constituent_fact_manifest": _fact_manifest(source),
    }


def _cell(source: str, candidate: str) -> dict[str, object]:
    i05 = dict(_terminal(source))
    i05.pop("constituent_fact_manifest")
    i05.update(
        {
            "status": "PASS",
            "constituent_fact_refs": [_ref(source)],
        }
    )
    return {
        "source_id": source,
        "candidate_id": candidate,
        "terminal_disposition": "PASS",
        "c11": _c11(source),
        "i03": _i03(source),
        "i05": i05,
        "required_lifecycle_phases": [],
        "lifecycle_reproductions": [],
    }


def _document() -> dict[str, object]:
    sources = ("LITS_I", "WVS7")
    candidates = ("A", "B", "C")
    admitted = [
        {"source_id": source, "candidate_id": candidate}
        for source in sources
        for candidate in candidates
    ]
    source_oracles = []
    for source in sources:
        source_oracles.append(
            {
                "source_id": source,
                "oracle_identity": _hash(f"{source}:oracle"),
                "expected_c11_identity": {
                    "logical_release_identity": _hash(f"{source}:c11"),
                    "replay_identity": _hash(f"{source}:c11:replay"),
                },
                "expected_i03_identity": {
                    "replay_identity": _hash(f"{source}:i03:replay"),
                    "fact_manifest": _fact_manifest(source),
                },
                "expected_terminal_identity": _terminal(source),
                "candidate_matches": [
                    {"candidate_id": candidate, "status": "PASS"}
                    for candidate in candidates
                ],
            }
        )
    return {
        "schema": INPUT_SCHEMA,
        "court_id": "test-court",
        "admitted_cells": admitted,
        "succession_preflight": {
            "status": "PASS",
            "receipt_identity": _hash("preflight:receipt"),
            "manifest_identity": _hash("preflight:manifest"),
        },
        "independent_parity_oracle": {
            "status": "PASS",
            "receipt_identity": _hash("oracle:receipt"),
            "candidate_neutral": True,
            "frozen_before_candidate_output": True,
            "candidate_outputs_seen_at_freeze": 0,
            "candidate_owned_roots_consulted": [],
            "source_oracles": source_oracles,
        },
        "cells": [
            _cell(source, candidate)
            for source in sources
            for candidate in candidates
        ],
    }


def _codes(result: dict[str, object]) -> set[str]:
    return set(result["failure_codes"])


def _cell_at(document: dict[str, object], source: str, candidate: str) -> dict[str, object]:
    return next(
        cell
        for cell in document["cells"]
        if cell["source_id"] == source and cell["candidate_id"] == candidate
    )


def _oracle_at(document: dict[str, object], source: str) -> dict[str, object]:
    return next(
        oracle
        for oracle in document["independent_parity_oracle"]["source_oracles"]
        if oracle["source_id"] == source
    )


def test_full_two_source_six_cell_i05_terminal_passes():
    result = verify_final_p2_terminal(_document())
    assert result["status"] == "PASS"
    assert result["failure_codes"] == []
    assert result["verified_cell_count"] == 6
    assert result["semantic_authority_created"] is False
    assert result["empirical_fact_created_or_mutated"] is False


def test_c11_only_cannot_be_misreported_as_final_terminal():
    document = _document()
    cell = _cell_at(document, "LITS_I", "A")
    cell.pop("i03")
    cell.pop("i05")
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert {"TV_I03_NOT_PASS", "TV_I05_NOT_PASS"}.issubset(_codes(result))


def test_i03_only_cannot_be_misreported_as_final_terminal():
    document = _document()
    _cell_at(document, "LITS_I", "A").pop("i05")
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert "TV_I05_NOT_PASS" in _codes(result)


def test_partial_i05_frontier_coverage_blocks():
    document = _document()
    _cell_at(document, "LITS_I", "A")["i05"]["covered_candidate_count"] = 2
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert "TV_I05_COVERAGE_INCOMPLETE" in _codes(result)


def test_missing_admitted_cell_cannot_disappear_from_court():
    document = _document()
    document["cells"] = [
        cell
        for cell in document["cells"]
        if not (cell["source_id"] == "WVS7" and cell["candidate_id"] == "C")
    ]
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert "TV_CELL_SET_MISMATCH" in _codes(result)


def test_succession_preflight_pass_is_explicit_and_mandatory():
    document = _document()
    document["succession_preflight"]["status"] = "BLOCK"
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert "TV_PREFLIGHT_NOT_PASS" in _codes(result)


def test_oracle_independence_receipt_is_explicit_and_mandatory():
    document = _document()
    document["independent_parity_oracle"]["candidate_neutral"] = False
    document["independent_parity_oracle"]["candidate_outputs_seen_at_freeze"] = 1
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert "TV_ORACLE_NOT_INDEPENDENT" in _codes(result)


def test_pairwise_agreement_cannot_replace_independent_oracle_match():
    document = _document()
    oracle = _oracle_at(document, "LITS_I")
    oracle["candidate_matches"] = oracle["candidate_matches"][:2]
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert "TV_ORACLE_CANDIDATE_MATCH_MISMATCH" in _codes(result)


def test_constituent_i03_fact_closure_must_be_exact():
    document = _document()
    wrong = {
        "kind": "EmpiricalFact",
        "object_id": "urn:test:wrong:fact",
        "content_hash": _hash("wrong:fact"),
    }
    _cell_at(document, "LITS_I", "A")["i05"]["constituent_fact_refs"] = [wrong]
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert "TV_CONSTITUENT_FACT_CLOSURE_MISMATCH" in _codes(result)


def test_semantic_replay_output_identity_drift_from_oracle_blocks():
    document = _document()
    cell = _cell_at(document, "LITS_I", "A")
    cell["i05"]["semantic_identity"] = _hash("drifted-semantic")
    cell["i05"]["replay_identity"] = _hash("drifted-replay")
    cell["i05"]["output_identity"] = _hash("drifted-output")
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert "TV_ORACLE_TERMINAL_IDENTITY_MISMATCH" in _codes(result)


def test_typed_negative_state_cannot_collapse_to_none():
    document = _document()
    _cell_at(document, "LITS_I", "A")["i03"]["fact_manifest"][0]["typed_state"] = None
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert "TV_TYPED_STATE_COLLAPSE" in _codes(result)


def test_lifecycle_reproduction_must_return_to_same_terminal_identity():
    document = _document()
    cell = _cell_at(document, "LITS_I", "A")
    cell["required_lifecycle_phases"] = ["DELETE_REGENERATE"]
    reproduced = copy.deepcopy(_terminal("LITS_I"))
    reproduced["replay_identity"] = _hash("changed-after-regeneration")
    cell["lifecycle_reproductions"] = [
        {
            "phase": "DELETE_REGENERATE",
            "status": "PASS",
            "terminal_identity": reproduced,
        }
    ]
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert "TV_LIFECYCLE_TERMINAL_IDENTITY_MISMATCH" in _codes(result)


def test_typed_nonqualification_is_preserved_but_cannot_yield_full_pass():
    document = _document()
    _cell_at(document, "WVS7", "C")["terminal_disposition"] = "NONQUALIFIED_SOURCE_CAPABILITY"
    result = verify_final_p2_terminal(document)
    assert result["status"] == "BLOCK"
    assert "TV_FINAL_CELL_NOT_PASS" in _codes(result)
    failure = next(row for row in result["failures"] if row["code"] == "TV_FINAL_CELL_NOT_PASS")
    assert failure["observed"] == "NONQUALIFIED_SOURCE_CAPABILITY"
