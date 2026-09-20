"""Fail-closed FIABC P2 final comparison-terminal verifier.

This verifier is a court gate, not a semantic producer.  It consumes explicit
succession-preflight, independent-oracle, C11, I03, I05 and lifecycle receipts
and checks the Wave-2 comparison-terminal contract.  It never creates or
modifies EmpiricalFact truth, semantic authority, discovery frontier membership,
or candidate physical state.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections.abc import Mapping, Sequence
from typing import Any

INPUT_SCHEMA = "RAWLSING_FIABC_P2_FINAL_TERMINAL_INPUT@1.0.0"
OUTPUT_SCHEMA = "RAWLSING_FIABC_P2_FINAL_TERMINAL_VERIFICATION@1.0.0"
TERMINAL_CONTRACT = (
    "GOVERNED_I05_LEARNED_EMPIRICAL_PRODUCT__"
    "EXACT_SEMANTIC_REPLAY_OUTPUT_IDENTITY__"
    "COMPLETE_COVERAGE__CONSTITUENT_I03_FACT_CLOSURE"
)
I05_COVERAGE_CLAIM = "COMPLETE_FOR_EXACT_DECLARED_FRONTIER"
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class TerminalVerifierInputError(ValueError):
    """The final-terminal verifier input cannot be interpreted safely."""


def _canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def _identity(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value)).hexdigest()


def _is_sequence(value: Any) -> bool:
    return isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray))


def _failure(
    failures: list[dict[str, Any]],
    code: str,
    path: str,
    detail: str,
    *,
    expected: Any | None = None,
    observed: Any | None = None,
) -> None:
    row: dict[str, Any] = {"code": code, "path": path, "detail": detail}
    if expected is not None:
        row["expected"] = expected
    if observed is not None:
        row["observed"] = observed
    failures.append(row)


def _text(
    value: Any,
    failures: list[dict[str, Any]],
    path: str,
    code: str,
) -> str | None:
    if not isinstance(value, str) or not value.strip():
        _failure(failures, code, path, "required non-empty identity/string is absent")
        return None
    return value.strip()


def _pass_status(
    value: Any,
    failures: list[dict[str, Any]],
    path: str,
    code: str,
) -> bool:
    if value != "PASS":
        _failure(failures, code, path, "required governed receipt is not PASS", expected="PASS", observed=value)
        return False
    return True


def _cell_key(
    value: Any,
    failures: list[dict[str, Any]],
    path: str,
) -> tuple[str, str] | None:
    if not isinstance(value, Mapping):
        _failure(failures, "TV_CELL_DESCRIPTOR_INVALID", path, "cell descriptor must be a mapping")
        return None
    source = _text(value.get("source_id"), failures, f"{path}.source_id", "TV_CELL_DESCRIPTOR_INVALID")
    candidate = _text(value.get("candidate_id"), failures, f"{path}.candidate_id", "TV_CELL_DESCRIPTOR_INVALID")
    if source is None or candidate is None:
        return None
    return source, candidate


def _normalize_exact_ref(
    value: Any,
    failures: list[dict[str, Any]],
    path: str,
) -> dict[str, str] | None:
    if not isinstance(value, Mapping):
        _failure(failures, "TV_EXACT_REF_INVALID", path, "ExactRef must be a mapping")
        return None
    kind = _text(value.get("kind"), failures, f"{path}.kind", "TV_EXACT_REF_INVALID")
    object_id = _text(value.get("object_id"), failures, f"{path}.object_id", "TV_EXACT_REF_INVALID")
    content_hash = value.get("content_hash")
    if not isinstance(content_hash, str) or _HEX64.fullmatch(content_hash) is None:
        _failure(
            failures,
            "TV_EXACT_REF_INVALID",
            f"{path}.content_hash",
            "ExactRef content_hash must be lowercase SHA-256 hex",
        )
        return None
    if kind is None or object_id is None:
        return None
    return {"kind": kind, "object_id": object_id, "content_hash": content_hash}


def _ref_key(ref: Mapping[str, str]) -> tuple[str, str, str]:
    return ref["kind"], ref["object_id"], ref["content_hash"]


def _normalize_fact_manifest(
    value: Any,
    failures: list[dict[str, Any]],
    path: str,
) -> tuple[list[dict[str, Any]], set[tuple[str, str, str]]] | None:
    if not _is_sequence(value) or not value:
        _failure(failures, "TV_I03_FACT_MANIFEST_INVALID", path, "fact manifest must be a non-empty sequence")
        return None
    rows: list[dict[str, Any]] = []
    keys: set[tuple[str, str, str]] = set()
    for index, raw in enumerate(value):
        row_path = f"{path}[{index}]"
        if not isinstance(raw, Mapping):
            _failure(failures, "TV_I03_FACT_MANIFEST_INVALID", row_path, "fact row must be a mapping")
            continue
        ref = _normalize_exact_ref(raw.get("ref"), failures, f"{row_path}.ref")
        state = _text(
            raw.get("typed_state"),
            failures,
            f"{row_path}.typed_state",
            "TV_TYPED_STATE_COLLAPSE",
        )
        if ref is None or state is None:
            continue
        key = _ref_key(ref)
        if key in keys:
            _failure(
                failures,
                "TV_I03_FACT_MANIFEST_INVALID",
                row_path,
                "duplicate constituent EmpiricalFact ExactRef",
                observed=ref,
            )
            continue
        keys.add(key)
        rows.append({"ref": ref, "typed_state": state})
    if not rows:
        return None
    rows.sort(key=lambda row: _ref_key(row["ref"]))
    return rows, keys


def _normalize_ref_sequence(
    value: Any,
    failures: list[dict[str, Any]],
    path: str,
) -> tuple[list[dict[str, str]], set[tuple[str, str, str]]] | None:
    if not _is_sequence(value) or not value:
        _failure(failures, "TV_CONSTITUENT_FACT_CLOSURE_MISMATCH", path, "constituent fact refs must be non-empty")
        return None
    rows: list[dict[str, str]] = []
    keys: set[tuple[str, str, str]] = set()
    for index, raw in enumerate(value):
        ref = _normalize_exact_ref(raw, failures, f"{path}[{index}]")
        if ref is None:
            continue
        key = _ref_key(ref)
        if key in keys:
            _failure(
                failures,
                "TV_CONSTITUENT_FACT_CLOSURE_MISMATCH",
                f"{path}[{index}]",
                "duplicate I05 constituent fact ref",
                observed=ref,
            )
            continue
        keys.add(key)
        rows.append(ref)
    if not rows:
        return None
    rows.sort(key=_ref_key)
    return rows, keys


def _normalize_c11_identity(
    value: Any,
    failures: list[dict[str, Any]],
    path: str,
) -> dict[str, str] | None:
    if not isinstance(value, Mapping):
        _failure(failures, "TV_C11_IDENTITY_INCOMPLETE", path, "C11 identity must be a mapping")
        return None
    release = _text(
        value.get("logical_release_identity"),
        failures,
        f"{path}.logical_release_identity",
        "TV_C11_IDENTITY_INCOMPLETE",
    )
    replay = _text(
        value.get("replay_identity"),
        failures,
        f"{path}.replay_identity",
        "TV_C11_IDENTITY_INCOMPLETE",
    )
    if release is None or replay is None:
        return None
    return {"logical_release_identity": release, "replay_identity": replay}


def _normalize_i03_identity(
    value: Any,
    failures: list[dict[str, Any]],
    path: str,
) -> tuple[dict[str, Any] | None, set[tuple[str, str, str]] | None]:
    if not isinstance(value, Mapping):
        _failure(failures, "TV_I03_IDENTITY_INCOMPLETE", path, "I03 identity must be a mapping")
        return None, None
    replay = _text(
        value.get("replay_identity"),
        failures,
        f"{path}.replay_identity",
        "TV_I03_IDENTITY_INCOMPLETE",
    )
    manifest = _normalize_fact_manifest(value.get("fact_manifest"), failures, f"{path}.fact_manifest")
    if replay is None or manifest is None:
        return None, manifest[1] if manifest else None
    rows, keys = manifest
    return {"replay_identity": replay, "fact_manifest": rows}, keys


def _positive_int(
    value: Any,
    failures: list[dict[str, Any]],
    path: str,
    code: str,
) -> int | None:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        _failure(failures, code, path, "required count must be a positive integer", observed=value)
        return None
    return value


def _normalize_terminal_identity(
    value: Any,
    failures: list[dict[str, Any]],
    path: str,
) -> dict[str, Any] | None:
    if not isinstance(value, Mapping):
        _failure(failures, "TV_I05_IDENTITY_INCOMPLETE", path, "I05 terminal identity must be a mapping")
        return None
    identity_fields = (
        "source_identity",
        "workload_identity",
        "authority_closure_identity",
        "frontier_identity",
        "coverage_receipt_identity",
        "learned_product_identity",
        "semantic_identity",
        "replay_identity",
        "output_identity",
    )
    normalized: dict[str, Any] = {}
    valid = True
    for field in identity_fields:
        item = _text(value.get(field), failures, f"{path}.{field}", "TV_I05_IDENTITY_INCOMPLETE")
        if item is None:
            valid = False
        else:
            normalized[field] = item
    coverage = value.get("coverage_claim")
    if coverage != I05_COVERAGE_CLAIM:
        _failure(
            failures,
            "TV_I05_COVERAGE_INCOMPLETE",
            f"{path}.coverage_claim",
            "I05 must close the complete exact declared frontier",
            expected=I05_COVERAGE_CLAIM,
            observed=coverage,
        )
        valid = False
    else:
        normalized["coverage_claim"] = coverage
    candidate_count = _positive_int(
        value.get("candidate_count"), failures, f"{path}.candidate_count", "TV_I05_COVERAGE_INCOMPLETE"
    )
    covered_count = _positive_int(
        value.get("covered_candidate_count"),
        failures,
        f"{path}.covered_candidate_count",
        "TV_I05_COVERAGE_INCOMPLETE",
    )
    if candidate_count is not None and covered_count is not None:
        normalized["candidate_count"] = candidate_count
        normalized["covered_candidate_count"] = covered_count
        if candidate_count != covered_count:
            _failure(
                failures,
                "TV_I05_COVERAGE_INCOMPLETE",
                path,
                "partial I05 frontier coverage cannot satisfy the comparison terminal",
                expected=candidate_count,
                observed=covered_count,
            )
            valid = False
    else:
        valid = False
    manifest = _normalize_fact_manifest(
        value.get("constituent_fact_manifest"), failures, f"{path}.constituent_fact_manifest"
    )
    if manifest is None:
        valid = False
    else:
        normalized["constituent_fact_manifest"] = manifest[0]
    return normalized if valid else None


def _terminal_from_cell(
    i05: Mapping[str, Any],
    i03_manifest: list[dict[str, Any]],
    failures: list[dict[str, Any]],
    path: str,
) -> tuple[dict[str, Any] | None, set[tuple[str, str, str]] | None]:
    material = dict(i05)
    material["constituent_fact_manifest"] = i03_manifest
    terminal = _normalize_terminal_identity(material, failures, path)
    refs = _normalize_ref_sequence(
        i05.get("constituent_fact_refs"), failures, f"{path}.constituent_fact_refs"
    )
    return terminal, refs[1] if refs else None


def _normalize_required_phases(
    value: Any,
    failures: list[dict[str, Any]],
    path: str,
) -> set[str] | None:
    if not _is_sequence(value):
        _failure(failures, "TV_LIFECYCLE_PHASE_SET_MISMATCH", path, "required_lifecycle_phases must be a sequence")
        return None
    phases: set[str] = set()
    for index, raw in enumerate(value):
        phase = _text(raw, failures, f"{path}[{index}]", "TV_LIFECYCLE_PHASE_SET_MISMATCH")
        if phase is None:
            continue
        if phase in phases:
            _failure(failures, "TV_LIFECYCLE_PHASE_SET_MISMATCH", f"{path}[{index}]", "duplicate required lifecycle phase")
        phases.add(phase)
    return phases


def _result(
    *,
    failures: list[dict[str, Any]],
    admitted_cells: set[tuple[str, str]],
    preflight_identity: str | None,
    oracle_identity: str | None,
) -> dict[str, Any]:
    ordered_failures = sorted(failures, key=lambda row: (row["code"], row["path"], row["detail"]))
    status = "PASS" if not ordered_failures else "BLOCK"
    core: dict[str, Any] = {
        "schema": OUTPUT_SCHEMA,
        "status": status,
        "terminal_contract": TERMINAL_CONTRACT,
        "admitted_cells": [
            {"source_id": source, "candidate_id": candidate}
            for source, candidate in sorted(admitted_cells)
        ],
        "verified_cell_count": len(admitted_cells) if status == "PASS" else 0,
        "succession_preflight_receipt_identity": preflight_identity,
        "independent_parity_oracle_receipt_identity": oracle_identity,
        "failure_codes": sorted({row["code"] for row in ordered_failures}),
        "failures": ordered_failures,
        "semantic_authority_created": False,
        "empirical_fact_created_or_mutated": False,
    }
    core["verification_identity"] = _identity(core)
    return core


def verify_final_p2_terminal(document: Mapping[str, Any]) -> dict[str, Any]:
    """Verify the full governed I05 comparison terminal and return PASS/BLOCK.

    Expected truth is supplied by explicit upstream receipts.  This function
    only validates their status, causal independence claims, cell completeness,
    intermediate invariants, terminal identity and lifecycle reproduction.
    """
    if not isinstance(document, Mapping):
        raise TerminalVerifierInputError("final-terminal input must be a mapping")

    failures: list[dict[str, Any]] = []
    if document.get("schema") != INPUT_SCHEMA:
        _failure(
            failures,
            "TV_INPUT_SCHEMA_INVALID",
            "schema",
            "final-terminal input schema mismatch",
            expected=INPUT_SCHEMA,
            observed=document.get("schema"),
        )

    admitted_cells: set[tuple[str, str]] = set()
    admitted_raw = document.get("admitted_cells")
    if not _is_sequence(admitted_raw) or not admitted_raw:
        _failure(failures, "TV_ADMITTED_CELL_SET_INVALID", "admitted_cells", "admitted cells must be a non-empty sequence")
    else:
        for index, raw in enumerate(admitted_raw):
            key = _cell_key(raw, failures, f"admitted_cells[{index}]")
            if key is None:
                continue
            if key in admitted_cells:
                _failure(
                    failures,
                    "TV_ADMITTED_CELL_DUPLICATE",
                    f"admitted_cells[{index}]",
                    "admitted source×candidate cell occurs more than once",
                    observed={"source_id": key[0], "candidate_id": key[1]},
                )
            admitted_cells.add(key)

    preflight_identity: str | None = None
    preflight = document.get("succession_preflight")
    if not isinstance(preflight, Mapping):
        _failure(failures, "TV_PREFLIGHT_NOT_PASS", "succession_preflight", "explicit succession-preflight receipt is required")
    else:
        _pass_status(preflight.get("status"), failures, "succession_preflight.status", "TV_PREFLIGHT_NOT_PASS")
        preflight_identity = _text(
            preflight.get("receipt_identity"),
            failures,
            "succession_preflight.receipt_identity",
            "TV_PREFLIGHT_RECEIPT_IDENTITY_MISSING",
        )
        _text(
            preflight.get("manifest_identity"),
            failures,
            "succession_preflight.manifest_identity",
            "TV_PREFLIGHT_RECEIPT_IDENTITY_MISSING",
        )

    oracle_identity: str | None = None
    oracle = document.get("independent_parity_oracle")
    source_oracles: dict[str, dict[str, Any]] = {}
    if not isinstance(oracle, Mapping):
        _failure(failures, "TV_ORACLE_NOT_PASS", "independent_parity_oracle", "explicit independent-parity-oracle receipt is required")
    else:
        _pass_status(oracle.get("status"), failures, "independent_parity_oracle.status", "TV_ORACLE_NOT_PASS")
        oracle_identity = _text(
            oracle.get("receipt_identity"),
            failures,
            "independent_parity_oracle.receipt_identity",
            "TV_ORACLE_RECEIPT_IDENTITY_MISSING",
        )
        if oracle.get("candidate_neutral") is not True:
            _failure(failures, "TV_ORACLE_NOT_INDEPENDENT", "independent_parity_oracle.candidate_neutral", "oracle must explicitly be candidate-neutral")
        if oracle.get("frozen_before_candidate_output") is not True:
            _failure(failures, "TV_ORACLE_NOT_INDEPENDENT", "independent_parity_oracle.frozen_before_candidate_output", "oracle must be frozen before candidate output")
        if oracle.get("candidate_outputs_seen_at_freeze") != 0:
            _failure(
                failures,
                "TV_ORACLE_NOT_INDEPENDENT",
                "independent_parity_oracle.candidate_outputs_seen_at_freeze",
                "oracle freeze must observe zero candidate outputs",
                expected=0,
                observed=oracle.get("candidate_outputs_seen_at_freeze"),
            )
        roots = oracle.get("candidate_owned_roots_consulted")
        if roots != []:
            _failure(
                failures,
                "TV_ORACLE_NOT_INDEPENDENT",
                "independent_parity_oracle.candidate_owned_roots_consulted",
                "oracle dependency closure may not consult candidate-owned roots",
                expected=[],
                observed=roots,
            )
        raw_source_oracles = oracle.get("source_oracles")
        if not _is_sequence(raw_source_oracles) or not raw_source_oracles:
            _failure(failures, "TV_ORACLE_SOURCE_SET_MISMATCH", "independent_parity_oracle.source_oracles", "source-local oracle receipts are required")
        else:
            for index, raw in enumerate(raw_source_oracles):
                path = f"independent_parity_oracle.source_oracles[{index}]"
                if not isinstance(raw, Mapping):
                    _failure(failures, "TV_ORACLE_SOURCE_SET_MISMATCH", path, "source oracle must be a mapping")
                    continue
                source = _text(raw.get("source_id"), failures, f"{path}.source_id", "TV_ORACLE_SOURCE_SET_MISMATCH")
                if source is None:
                    continue
                if source in source_oracles:
                    _failure(failures, "TV_ORACLE_SOURCE_SET_MISMATCH", path, "duplicate source oracle", observed=source)
                    continue
                _text(raw.get("oracle_identity"), failures, f"{path}.oracle_identity", "TV_ORACLE_RECEIPT_IDENTITY_MISSING")
                expected_c11 = _normalize_c11_identity(raw.get("expected_c11_identity"), failures, f"{path}.expected_c11_identity")
                expected_i03, _ = _normalize_i03_identity(raw.get("expected_i03_identity"), failures, f"{path}.expected_i03_identity")
                expected_terminal = _normalize_terminal_identity(
                    raw.get("expected_terminal_identity"), failures, f"{path}.expected_terminal_identity"
                )
                matches: dict[str, str] = {}
                raw_matches = raw.get("candidate_matches")
                if not _is_sequence(raw_matches):
                    _failure(failures, "TV_ORACLE_CANDIDATE_MATCH_MISMATCH", f"{path}.candidate_matches", "candidate oracle-match receipts must be a sequence")
                else:
                    for match_index, match in enumerate(raw_matches):
                        match_path = f"{path}.candidate_matches[{match_index}]"
                        if not isinstance(match, Mapping):
                            _failure(failures, "TV_ORACLE_CANDIDATE_MATCH_MISMATCH", match_path, "candidate match must be a mapping")
                            continue
                        candidate = _text(match.get("candidate_id"), failures, f"{match_path}.candidate_id", "TV_ORACLE_CANDIDATE_MATCH_MISMATCH")
                        if candidate is None:
                            continue
                        if candidate in matches:
                            _failure(failures, "TV_ORACLE_CANDIDATE_MATCH_MISMATCH", match_path, "duplicate candidate oracle-match receipt", observed=candidate)
                            continue
                        status = match.get("status")
                        matches[candidate] = status if isinstance(status, str) else ""
                        if status != "PASS":
                            _failure(
                                failures,
                                "TV_ORACLE_CANDIDATE_MATCH_MISMATCH",
                                f"{match_path}.status",
                                "each admitted candidate must independently PASS the same source-local oracle",
                                expected="PASS",
                                observed=status,
                            )
                source_oracles[source] = {
                    "expected_c11": expected_c11,
                    "expected_i03": expected_i03,
                    "expected_terminal": expected_terminal,
                    "matches": matches,
                }

    expected_sources = {source for source, _ in admitted_cells}
    if set(source_oracles) != expected_sources:
        _failure(
            failures,
            "TV_ORACLE_SOURCE_SET_MISMATCH",
            "independent_parity_oracle.source_oracles",
            "source-local oracle set must exactly equal admitted source set",
            expected=sorted(expected_sources),
            observed=sorted(source_oracles),
        )
    for source in sorted(expected_sources):
        expected_candidates = {candidate for src, candidate in admitted_cells if src == source}
        matches = source_oracles.get(source, {}).get("matches", {})
        if set(matches) != expected_candidates:
            _failure(
                failures,
                "TV_ORACLE_CANDIDATE_MATCH_MISMATCH",
                f"independent_parity_oracle.source_oracles[{source}].candidate_matches",
                "oracle-match receipts must exactly cover every admitted candidate for the source",
                expected=sorted(expected_candidates),
                observed=sorted(matches),
            )

    cells: dict[tuple[str, str], Mapping[str, Any]] = {}
    raw_cells = document.get("cells")
    if not _is_sequence(raw_cells):
        _failure(failures, "TV_CELL_SET_MISMATCH", "cells", "terminal cells must be a sequence")
    else:
        for index, raw in enumerate(raw_cells):
            key = _cell_key(raw, failures, f"cells[{index}]")
            if key is None or not isinstance(raw, Mapping):
                continue
            if key in cells:
                _failure(failures, "TV_CELL_SET_MISMATCH", f"cells[{index}]", "duplicate terminal cell", observed={"source_id": key[0], "candidate_id": key[1]})
                continue
            cells[key] = raw
    if set(cells) != admitted_cells:
        _failure(
            failures,
            "TV_CELL_SET_MISMATCH",
            "cells",
            "terminal cell set must exactly equal admitted source×candidate set; omission or extras are forbidden",
            expected=[list(key) for key in sorted(admitted_cells)],
            observed=[list(key) for key in sorted(cells)],
        )

    for source, candidate in sorted(admitted_cells):
        cell = cells.get((source, candidate))
        if cell is None:
            continue
        path = f"cells[{source}/{candidate}]"
        if cell.get("terminal_disposition") != "PASS":
            _failure(
                failures,
                "TV_FINAL_CELL_NOT_PASS",
                f"{path}.terminal_disposition",
                "an admitted cell may retain its typed nonqualification state, but full-court terminal PASS cannot silently omit or scalarize it",
                expected="PASS",
                observed=cell.get("terminal_disposition"),
            )

        c11 = cell.get("c11")
        observed_c11: dict[str, str] | None = None
        if not isinstance(c11, Mapping):
            _failure(failures, "TV_C11_NOT_PASS", f"{path}.c11", "validated C11 is a mandatory intermediate invariant")
        else:
            _pass_status(c11.get("status"), failures, f"{path}.c11.status", "TV_C11_NOT_PASS")
            observed_c11 = _normalize_c11_identity(c11, failures, f"{path}.c11")
        expected_c11 = source_oracles.get(source, {}).get("expected_c11")
        if observed_c11 is not None and expected_c11 is not None and observed_c11 != expected_c11:
            _failure(
                failures,
                "TV_C11_ORACLE_MISMATCH",
                f"{path}.c11",
                "C11 intermediate identity differs from candidate-neutral oracle",
                expected=expected_c11,
                observed=observed_c11,
            )

        i03 = cell.get("i03")
        observed_i03: dict[str, Any] | None = None
        i03_keys: set[tuple[str, str, str]] | None = None
        if not isinstance(i03, Mapping):
            _failure(failures, "TV_I03_NOT_PASS", f"{path}.i03", "I03 exact empirical facts are a mandatory intermediate invariant")
        else:
            _pass_status(i03.get("status"), failures, f"{path}.i03.status", "TV_I03_NOT_PASS")
            observed_i03, i03_keys = _normalize_i03_identity(i03, failures, f"{path}.i03")
        expected_i03 = source_oracles.get(source, {}).get("expected_i03")
        if observed_i03 is not None and expected_i03 is not None and observed_i03 != expected_i03:
            _failure(
                failures,
                "TV_I03_ORACLE_MISMATCH",
                f"{path}.i03",
                "I03 exact facts/states/replay differ from candidate-neutral oracle",
                expected=expected_i03,
                observed=observed_i03,
            )

        i05 = cell.get("i05")
        observed_terminal: dict[str, Any] | None = None
        i05_ref_keys: set[tuple[str, str, str]] | None = None
        if not isinstance(i05, Mapping):
            _failure(failures, "TV_I05_NOT_PASS", f"{path}.i05", "full I05 learned empirical product is required; C11/I03 alone cannot terminate the court")
        else:
            _pass_status(i05.get("status"), failures, f"{path}.i05.status", "TV_I05_NOT_PASS")
            if observed_i03 is not None:
                observed_terminal, i05_ref_keys = _terminal_from_cell(
                    i05,
                    observed_i03["fact_manifest"],
                    failures,
                    f"{path}.i05",
                )
            else:
                _failure(
                    failures,
                    "TV_CONSTITUENT_FACT_CLOSURE_MISMATCH",
                    f"{path}.i05.constituent_fact_refs",
                    "I05 constituent closure cannot be proved without a valid I03 fact manifest",
                )
        if i03_keys is not None and i05_ref_keys is not None and i03_keys != i05_ref_keys:
            _failure(
                failures,
                "TV_CONSTITUENT_FACT_CLOSURE_MISMATCH",
                f"{path}.i05.constituent_fact_refs",
                "I05 constituent refs must close exactly over the I03 fact set",
                expected=sorted(i03_keys),
                observed=sorted(i05_ref_keys),
            )
        expected_terminal = source_oracles.get(source, {}).get("expected_terminal")
        if observed_terminal is not None and expected_terminal is not None and observed_terminal != expected_terminal:
            _failure(
                failures,
                "TV_ORACLE_TERMINAL_IDENTITY_MISMATCH",
                f"{path}.i05",
                "full I05 source/workload/authority/frontier/product/semantic/replay/output/fact identity differs from candidate-neutral oracle",
                expected=expected_terminal,
                observed=observed_terminal,
            )

        required_phases = _normalize_required_phases(
            cell.get("required_lifecycle_phases", []), failures, f"{path}.required_lifecycle_phases"
        )
        lifecycle = cell.get("lifecycle_reproductions", [])
        observed_phases: dict[str, Mapping[str, Any]] = {}
        if not _is_sequence(lifecycle):
            _failure(failures, "TV_LIFECYCLE_PHASE_SET_MISMATCH", f"{path}.lifecycle_reproductions", "lifecycle reproductions must be a sequence")
        else:
            for index, raw in enumerate(lifecycle):
                life_path = f"{path}.lifecycle_reproductions[{index}]"
                if not isinstance(raw, Mapping):
                    _failure(failures, "TV_LIFECYCLE_PHASE_SET_MISMATCH", life_path, "lifecycle reproduction must be a mapping")
                    continue
                phase = _text(raw.get("phase"), failures, f"{life_path}.phase", "TV_LIFECYCLE_PHASE_SET_MISMATCH")
                if phase is None:
                    continue
                if phase in observed_phases:
                    _failure(failures, "TV_LIFECYCLE_PHASE_SET_MISMATCH", life_path, "duplicate lifecycle reproduction phase")
                    continue
                observed_phases[phase] = raw
                _pass_status(raw.get("status"), failures, f"{life_path}.status", "TV_LIFECYCLE_NOT_PASS")
                reproduced = _normalize_terminal_identity(
                    raw.get("terminal_identity"), failures, f"{life_path}.terminal_identity"
                )
                if observed_terminal is not None and reproduced is not None and reproduced != observed_terminal:
                    _failure(
                        failures,
                        "TV_LIFECYCLE_TERMINAL_IDENTITY_MISMATCH",
                        f"{life_path}.terminal_identity",
                        "post-terminal lifecycle operation must reproduce the same exact terminal identity",
                        expected=observed_terminal,
                        observed=reproduced,
                    )
        if required_phases is not None and set(observed_phases) != required_phases:
            _failure(
                failures,
                "TV_LIFECYCLE_PHASE_SET_MISMATCH",
                f"{path}.lifecycle_reproductions",
                "lifecycle reproduction receipts must exactly cover the phases required by the cell contract",
                expected=sorted(required_phases),
                observed=sorted(observed_phases),
            )

    return _result(
        failures=failures,
        admitted_cells=admitted_cells,
        preflight_identity=preflight_identity,
        oracle_identity=oracle_identity,
    )


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify the governed FIABC P2 final I05 comparison terminal")
    parser.add_argument("input_json", help="path to the explicit terminal-verifier input receipt bundle")
    args = parser.parse_args(argv)
    with open(args.input_json, "r", encoding="utf-8") as handle:
        document = json.load(handle)
    if not isinstance(document, Mapping):
        raise TerminalVerifierInputError("input JSON root must be an object")
    result = verify_final_p2_terminal(document)
    print(json.dumps(result, sort_keys=True, indent=2, ensure_ascii=False))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
