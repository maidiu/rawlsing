"""N04-R2 whole-current-corpus governed T03 release/status runner.

This runner is deliberately conservative.  It reconstructs the HQ-adopted
N03-R2 18,276-row semantic-currentness surface and projects only states that
are already authorized.  It does not turn CURRENT_GOVERNED_POSITIVE into a
T03 compiler record unless an HQ-adopted production binding to the banked
GovernedSemanticCapitalRecord contract exists.

At this commission grain no such production binding exists.  The banked N04
compiler is imported and requalified byte-exact, but its five carrier adapters
consume already-governed exact-schema premise bundles; they are not authority
to reinterpret FQRA/QSMv2/typed-relation/source-native rows into those roles.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import importlib.util
import json
import pathlib
import subprocess
import tempfile
import zlib
from collections import Counter
from typing import Any

from rawlsing_next.prev3_governed_semantic_t03_compiler import (
    PSC02_COMPILER_CONTRACT_ID,
    _FIELDS as BANKED_COMPILER_FIXTURE_FIELDS,
)

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]

N03_R2_COMMIT = "3eaf9918e66b9d4bbc3a1c12598baca20c9d594d"
N03_R2_ROOT = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "ASTRA_PREV3_COMPLETION_AUDIT_R1/"
    "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1/"
    "PSC_FIRST_ACTIVE_WAVE_R1/WORKER_RETURNS/N03-R2"
)
N03_EXPECTED_JSONL_SHA256 = (
    "0ac4cd90c19c859438ec12ddfa69c37e9b9c85607884e0f4ea93bc6b52493723"
)
N03_EXPECTED_VECTOR_SHA256 = (
    "0418de4150a807d655caeb5d9e452a6fb1dda9639c18cf82b7624e2cbce3d4b0"
)
N01_EXPECTED_CARRIER_SHA256 = (
    "df0df368ecd4b884e69894b32fb49102edb554c5ca69700d3d56b9dbe3b76cfc"
)

IMPORTED_BLOBS = {
    "rawlsing_next/prev3_governed_semantic_t03_compiler.py":
        "ad5806e3f500bdc63b40fde49f210ff45b282170",
    "tests/test_prev3_governed_semantic_t03_compiler.py":
        "e4d612f34f7ee5d8fb978a4b4299ed29b98f994a",
    "rawlsing_next/_prev3_structural_batch_base.py":
        "4e785a8eba66f092e95abea39ad3948ec1c3e019",
    "rawlsing_next/_prev3_structural_batch_records.py":
        "988b0c03359d9bdf89408b46acec90118ee422fa",
    "rawlsing_next/_prev3_structural_batch_status.py":
        "ed892763978110f4254d4c36fb130e3f9a058e50",
    "rawlsing_next/_prev3_structural_batch_runtime.py":
        "aec8167eaeceb229c932e162b1f922dea33a119c",
}

STATUS_CODEBOOK = {
    0: "EMITTED_GOVERNED_T03_CANDIDATE",
    1: "BLOCKED_N03_REVIEW_REQUIRED",
    2: "BLOCKED_N03_TYPED_UNRESOLVED",
    3: "BLOCKED_CURRENT_POSITIVE__MISSING_HQ_ADOPTED_PRODUCTION_PREMISE_BINDING",
}
STATUS_BY_N03 = {
    "CURRENT_GOVERNED_POSITIVE": 3,
    "CURRENT_GOVERNED_REVIEW_REQUIRED": 1,
    "CURRENT_TYPED_UNRESOLVED__EXACT_BASIS": 2,
}

PRODUCTION_BINDING_BLOCKER = (
    "NO_HQ_ADOPTED_CARRIER_SPECIFIC_BINDING_FROM_CURRENT_N03_AUTHORITY_"
    "JURISDICTIONS_TO_N04_GOVERNED_SEMANTIC_CAPITAL_RECORD_PREMISES"
)
PRODUCTION_BINDING_MISSING_PROOF = (
    "EXACT_ACCEPTED_PRODUCTION_ADAPTER_OR_BINDING_RECEIPT_ASSIGNING_"
    "SEMANTIC_CORE_SCHEMA_CEILINGS_EPISTEMIC_JURISDICTION_AND_ADMISSION_"
    "ROLES_WITHOUT_COLLAPSING_FQRA_QSMV2_TYPED_RELATION_OR_SOURCE_NATIVE_"
    "JURISDICTIONS"
)

EXPECTED_STATUS_VECTOR_RAW_SHA256 = (
    "ff8303f17c1707c61982e3518823e2c441d26f5bda5a0f962fe6a5903d7ab742"
)
EXPECTED_STATUS_VECTOR_B64_SHA256 = (
    "f01e07ecfaa8f5af3b83bd26da7373b7ae6bba8ace5377ca1277a0530c8970e6"
)
EXPECTED_STATUS_VECTOR_B64_BYTES = 188
EXPECTED_EMPTY_POSITIVE_ID_STREAM_SHA256 = hashlib.sha256(b"").hexdigest()

RETURN_ROOT = (
    REPO_ROOT
    / "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3"
    / "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1"
    / "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1"
    / "ASTRA_PREV3_COMPLETION_AUDIT_R1"
    / "POST_GENERIC_CLOSURE_SOURCE_SEMANTIC_CAMPAIGN_READINESS_R1"
    / "PSC_FIRST_ACTIVE_WAVE_R1/WORKER_RETURNS/N04-R2"
)


def _run(*args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        args,
        cwd=REPO_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=check,
    )


def _sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _ensure_commit(sha: str) -> None:
    if _run("git", "cat-file", "-e", sha + "^{commit}", check=False).returncode == 0:
        return
    fetched = _run("git", "fetch", "--no-tags", "--depth=1", "origin", sha, check=False)
    if fetched.returncode:
        raise AssertionError(
            f"cannot fetch accepted commit {sha}: "
            f"{fetched.stderr.decode(errors='replace')}"
        )
    assert _run("git", "cat-file", "-e", sha + "^{commit}", check=False).returncode == 0


def _git_bytes(ref: str, path: str) -> bytes:
    _ensure_commit(ref)
    proc = _run("git", "show", f"{ref}:{path}", check=False)
    if proc.returncode:
        raise AssertionError(
            f"missing accepted object {ref}:{path}: "
            f"{proc.stderr.decode(errors='replace')}"
        )
    return proc.stdout


def _git_blob_for_worktree_path(path: str) -> str:
    proc = _run("git", "hash-object", path)
    return proc.stdout.decode().strip()


def verify_imported_implementation() -> dict[str, str]:
    observed = {
        path: _git_blob_for_worktree_path(path)
        for path in sorted(IMPORTED_BLOBS)
    }
    assert observed == dict(sorted(IMPORTED_BLOBS.items()))
    assert (
        PSC02_COMPILER_CONTRACT_ID
        == "PREV3_GOVERNED_SEMANTIC_CAPITAL_TO_ADOPTED_T03_INTAKE_COMPILER_R1@1.0.0"
    )
    return observed


def _load_n03_r2_replay():
    names = (
        "01_AUTHORITY_JURISDICTION_MANIFEST.json",
        "02_DISPOSITION_CODEBOOK.json",
        "replay_n03_r2.py",
    )
    with tempfile.TemporaryDirectory(prefix="n04r2_n03r2_") as tmp:
        root = pathlib.Path(tmp)
        for name in names:
            (root / name).write_bytes(_git_bytes(N03_R2_COMMIT, f"{N03_R2_ROOT}/{name}"))
        spec = importlib.util.spec_from_file_location("accepted_n03_r2_replay", root / "replay_n03_r2.py")
        if spec is None or spec.loader is None:
            raise AssertionError("cannot load accepted N03-R2 replay")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        ledger, vector, _vb64, summary = module.build()
    return ledger, vector, summary


def _status_row(row: dict[str, Any], code: int) -> dict[str, Any]:
    disposition = STATUS_CODEBOOK[code]
    if code == 3:
        residual_basis = PRODUCTION_BINDING_BLOCKER
        missing_proof = PRODUCTION_BINDING_MISSING_PROOF
    elif code == 1:
        residual_basis = "N03_R2_CURRENT_GOVERNED_REVIEW_REQUIRED"
        missing_proof = "EXACT_UPSTREAM_GOVERNED_AUTHORITY_RESOLUTION_REQUIRED"
    elif code == 2:
        residual_basis = "N03_R2_CURRENT_TYPED_UNRESOLVED__EXACT_BASIS"
        missing_proof = row.get("unresolved_basis") or "EXACT_N03_R2_UNRESOLVED_BASIS"
    else:
        residual_basis = ""
        missing_proof = ""
    return {
        "question_implementation_id": row["question_implementation_id"],
        "source_family": row["source_family"],
        "wave": row["wave"],
        "source_variable_code": row["source_variable_code"],
        "n03_top_level_disposition": row["top_level_disposition"],
        "t03_release_status": disposition,
        "t03_positive_candidate_emitted": code == 0,
        "residual_basis": residual_basis,
        "smallest_missing_proof": missing_proof,
        "n03_top_level_authority_refs": row["top_level_authority_refs"],
        "routing_authority_code": row["routing_authority_code"],
        "routing_disposition": row["routing_disposition"],
        "routing_scope": row["routing_scope"],
        "psc03_companion_authority": (
            "PRESERVED_OUTSIDE_ROW_LEVEL_T03_PROMOTION_UNLESS_EXACT_BINDING_AND_"
            "COMPILER_PREMISES_ARE_SEPARATELY_GOVERNED"
        ),
    }


def build_whole_corpus_status():
    imported = verify_imported_implementation()
    ledger, n03_vector, n03_summary = _load_n03_r2_replay()
    assert n03_summary["rows"] == 18276
    assert n03_summary["unique_ids"] == 18276
    assert n03_summary["families"] == 9
    assert n03_summary["active_scopes"] == 35
    assert n03_summary["ledger_canonical_jsonl_sha256"] == N03_EXPECTED_JSONL_SHA256
    assert n03_summary["top_vector_raw_sha256"] == N03_EXPECTED_VECTOR_SHA256
    assert n03_summary["n01_full_csv_sha256"] == N01_EXPECTED_CARRIER_SHA256
    assert n03_summary["disposition_counts"] == {
        "CURRENT_GOVERNED_POSITIVE": 18213,
        "CURRENT_GOVERNED_REVIEW_REQUIRED": 41,
        "CURRENT_TYPED_UNRESOLVED__EXACT_BASIS": 22,
    }

    vector_codes = []
    rows = []
    for row in ledger:
        code = STATUS_BY_N03.get(row["top_level_disposition"])
        if code is None:
            raise AssertionError(
                "unexpected adopted N03-R2 disposition at N04-R2 production grain: "
                + row["top_level_disposition"]
            )
        vector_codes.append(code)
        rows.append(_status_row(row, code))

    vector = bytes(vector_codes)
    vb64 = base64.b64encode(zlib.compress(vector, 9))
    assert len(vector) == 18276
    assert _sha256(vector) == EXPECTED_STATUS_VECTOR_RAW_SHA256
    assert len(vb64) == EXPECTED_STATUS_VECTOR_B64_BYTES
    assert _sha256(vb64) == EXPECTED_STATUS_VECTOR_B64_SHA256

    counts = Counter(STATUS_CODEBOOK[code] for code in vector)
    expected_counts = {
        "BLOCKED_CURRENT_POSITIVE__MISSING_HQ_ADOPTED_PRODUCTION_PREMISE_BINDING": 18213,
        "BLOCKED_N03_REVIEW_REQUIRED": 41,
        "BLOCKED_N03_TYPED_UNRESOLVED": 22,
    }
    assert dict(sorted(counts.items())) == dict(sorted(expected_counts.items()))
    assert not any(row["t03_positive_candidate_emitted"] for row in rows)

    critical_roles = {
        "semantic_core_ref",
        "semantic_schema_ref",
        "negative_ceiling_ref",
        "type_class_ceiling_ref",
        "structural_use_ceiling_ref",
        "epistemic_class",
        "jurisdiction",
        "authority_ref",
        "currentness_ref",
        "evidence_admission_refs",
    }
    assert critical_roles.issubset(BANKED_COMPILER_FIXTURE_FIELDS)
    assert all(not critical_roles.issubset(set(row)) for row in ledger)

    summary = {
        "schema": "RAWLSING_N04_R2_WHOLE_CORPUS_T03_RELEASE_STATUS@1.0.0",
        "rows": 18276,
        "unique_ids": 18276,
        "families": 9,
        "active_scopes": 35,
        "positive_t03_candidates": 0,
        "positive_candidate_sorted_id_stream_sha256": EXPECTED_EMPTY_POSITIVE_ID_STREAM_SHA256,
        "status_counts": dict(sorted(expected_counts.items())),
        "status_vector_raw_sha256": EXPECTED_STATUS_VECTOR_RAW_SHA256,
        "status_vector_raw_bytes": len(vector),
        "status_vector_zlib_b64_sha256": EXPECTED_STATUS_VECTOR_B64_SHA256,
        "status_vector_zlib_b64_bytes": len(vb64),
        "n03_r2_canonical_jsonl_sha256": N03_EXPECTED_JSONL_SHA256,
        "n03_r2_raw_vector_sha256": N03_EXPECTED_VECTOR_SHA256,
        "n01_full_csv_sha256": N01_EXPECTED_CARRIER_SHA256,
        "compiler_contract": PSC02_COMPILER_CONTRACT_ID,
        "imported_blobs": imported,
        "positive_status_residual": PRODUCTION_BINDING_BLOCKER,
        "smallest_missing_proof": PRODUCTION_BINDING_MISSING_PROOF,
        "boundary": (
            "NO_SEMANTIC_INFERENCE__NO_AUTOMATIC_COMPILE_FROM_CURRENT_POSITIVE__"
            "NO_JURISDICTION_COLLAPSE__NO_STRUCTURAL_PROMOTION__NO_PERSON_STATE"
        ),
    }
    return rows, vector, vb64, summary


def _canonical_jsonl(rows: list[dict[str, Any]]) -> bytes:
    return b"".join(
        (
            json.dumps(row, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
            + "\n"
        ).encode("utf-8")
        for row in rows
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-status-jsonl")
    parser.add_argument("--emit-vector")
    parser.add_argument("--summary-out")
    args = parser.parse_args()
    rows, _vector, vb64, summary = build_whole_corpus_status()
    if args.emit_status_jsonl:
        pathlib.Path(args.emit_status_jsonl).write_bytes(_canonical_jsonl(rows))
    if args.emit_vector:
        pathlib.Path(args.emit_vector).write_bytes(vb64 + b"\n")
    if args.summary_out:
        pathlib.Path(args.summary_out).write_text(
            json.dumps(summary, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
