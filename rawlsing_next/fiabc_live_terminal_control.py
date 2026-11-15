"""FIABC-T5 live succession/oracle/terminal control.

Verification/composition seam only. Expected truth remains candidate-neutral and
pre-output frozen. Candidate execution emits governed observations; the neutral
court compares them to the frozen oracle and composes I07/I08 receipts.
"""
from __future__ import annotations

from collections import Counter
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from rawlsing_next.ee_p2x_candidate_process_envelope import load_frozen_upstream_receipt
from rawlsing_next.fiabc_terminal_completeness import (
    TerminalCompletenessError,
    validate_terminal_telemetry_completeness,
)
from rawlsing_next.fiabc_p2_terminal_verifier import (
    INPUT_SCHEMA as TERMINAL_INPUT_SCHEMA,
    TERMINAL_CONTRACT,
    verify_final_p2_terminal,
)
from rawlsing_next.fiabc_succession_preflight import (
    GitEvidenceResolver,
    evaluate_manifest,
    require_preflight_pass,
)
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next.pre553_independent_parity_oracle import (
    LITS_C11_RELEASE_IDENTITY,
    LITS_C11_REPLAY_IDENTITY,
    LITS_FRONTIER_SEAL,
    LITS_SOURCE_SHA256,
    NEGATIVE_STATE_LAW,
    WVS7_EMPIRICAL_UNIVERSE,
    WVS7_FAMILY_COUNTS,
    WVS7_MEASURE_BASIS,
    WVS7_ORDERED_CANDIDATE_HASHES,
    WVS7_RISK_SET,
    WVS7_SOURCE_SHA256,
    validate_candidate_observation,
    validate_three_way_parity,
    verify_frozen_oracle,
)

COURT_CONTRACT_SCHEMA = "RAWLSING_FIABC_T5_CURRENT_SIX_CELL_COURT_CONTRACT@1.0.0"
OBSERVATION_SCHEMA = "RAWLSING_FIABC_T5_LIVE_CANDIDATE_OBSERVATION@1.0.0"
MATCH_WRAPPER_SCHEMA = "RAWLSING_FIABC_T5_LIVE_ORACLE_MATCH@1.0.0"
THREE_WAY_WRAPPER_SCHEMA = "RAWLSING_FIABC_T5_LIVE_THREE_WAY_ORACLE_MATCH@1.0.0"
PREFLIGHT_RECEIPT_SCHEMA = "RAWLSING_FIABC_T5_LIVE_SUCCESSION_PREFLIGHT@1.0.0"
CELL_TERMINAL_SCHEMA = "RAWLSING_FIABC_T5_LIVE_CELL_TERMINAL@1.0.0"
FINAL_COMPOSITION_SCHEMA = "RAWLSING_FIABC_T5_LIVE_FINAL_COMPOSITION@1.0.0"
CLAIM_SCOPE = "P2X_LITS_I_WVS7_RAW_SOURCE_LOCAL_WORKLOAD__CLAIM_SCOPED_ONLY"

EXPECTED_SOURCES = ("LITS_I", "WVS7")
EXPECTED_CANDIDATES = ("A", "B", "C")
EXPECTED_CELLS = tuple((s, c) for s in EXPECTED_SOURCES for c in EXPECTED_CANDIDATES)
EXPECTED_SOURCE_SHA = {"LITS_I": LITS_SOURCE_SHA256, "WVS7": WVS7_SOURCE_SHA256}
EXPECTED_OWNER_BLOBS = {
    "A": "d4915e7e6755ba1850756aebff72f982f73a332b",
    "B": "7c509c2098d0030f253344eb3f682471378812a8",
    "C": "abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889",
}

EXPECTED_CURRENT_EXECUTION_MANIFEST = {
    "path": "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json",
    "schema": "RAWLSING_FIABC_CURRENT_SIX_CELL_EXECUTION_MANIFEST@1.0.0",
    "historical_continuation_is_current_law": False,
}
EXPECTED_REQUIRED_CONTRACTS = {
    "independent_oracle": "RAWLSING_FIABC_CANDIDATE_NEUTRAL_PARITY_ORACLE@1.0.0",
    "succession_preflight": "RAWLSING_FIABC_SUCCESSION_PREFLIGHT@1.0.0",
    "t4_accounting": "FIABC_T4_LIVE_ACCOUNTING_BINDING@1.0.0",
    "final_terminal": "RAWLSING_FIABC_P2_FINAL_TERMINAL_VERIFICATION@1.0.0",
}
EXPECTED_CLAIM_BOUNDARY = {
    "whole_source_physical_equivalence": False,
    "closed_35_universality": False,
    "source_certification": False,
    "whole_file_abc_identity": False,
    "capability_105_cells": False,
    "population_validity": False,
    "weighted_validity": False,
}
EXPECTED_T4_ACCOUNTING_SURFACES = {
    "process_isolation_provenance": True,
    "write_once_telemetry_semantics": True,
    "actual_lifecycle_actions": True,
    "typed_null_missing_telemetry": True,
    "preserved_work_classification": True,
    "source_candidate_process_action_identities": True,
}
EXPECTED_PRESERVATION_ANCHORS = {
    "hq_live_t4_checkpoint": {
        "branch": "agent/vozhd-premain-fiabc-live-t4-fanin-r1",
        "tip": "0478e95f59f1860626816d404baf51b85907e3ad",
    },
    "t1_runtime_packaging": {
        "lits_materializer": {
            "path": "rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py",
            "blob": "9406bacfd928393f6a159a46216aa1f7ec129f34",
        },
        "node4a_support": {
            "path": "WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py",
            "blob": "504944f9533b7385d201076e2e834b8a9446dee8",
        },
        "wvs_runtime_package": {
            "path": "rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json",
            "blob": "f016cdfdfd51e7973ab10b2196fe27ba5c90b3cd",
        },
        "wvs_projection_materializer": {
            "path": "rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py",
            "blob": "ec685803a7416032037ee415e8faf7bf60db8f1b",
        },
    },
    "t2_current_binding": {
        "candidate_c_module": {
            "path": "rawlsing_next/pre553_candidate_c_production_binding.py",
            "blob": "47893688ed455ced2c2f2311ad0aead6fb5bf2d2",
        },
        "candidate_c_policy": "SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS",
        "six_cell_manifest_path": "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json",
        "historical_continuation_is_current_law": False,
    },
    "t3_freeze_and_isolation": {
        "oracle_module": {
            "path": "rawlsing_next/pre553_independent_parity_oracle.py",
            "blob": "2b2b5fb869e8a1a47814dc8aaa7ff2e2ae20e757",
        },
        "process_envelope": {
            "path": "rawlsing_next/ee_p2x_candidate_process_envelope.py",
            "blob": "e8b653991887855ac7dee730bb19706219332422",
        },
        "isolated_backend": {
            "path": "rawlsing_next/ee_p2x_process_isolated_backend.py",
            "blob": "b36faf5af98b49a4b11c408402229cff02aad7bc",
        },
        "freeze_schema": "RAWLSING_FIABC_CANDIDATE_NEUTRAL_FREEZE@2.0.0",
        "fresh_process_per_source_candidate_cell": True,
        "generic_source_freeze": True,
    },
    "t4_accounting": {
        "telemetry": {
            "path": "rawlsing_next/fiabc_telemetry_semantics.py",
            "blob": "d061cd0f3c595c100ea728520fb0892404a2ca9b",
        },
        "lifecycle": {
            "path": "rawlsing_next/fiabc_lifecycle_accounting.py",
            "blob": "a2977ea22fe67858a2a811917bd7ac0f4b7350c7",
        },
        "bridge": {
            "path": "rawlsing_next/fiabc_live_accounting_binding.py",
            "blob": "3ca3a1ce90f18fbcb2d7b5c7e3a25d41dd4b0c4e",
        },
        "pre_t5_driver_blob": "9d9492f96d849a3f2e67e187507d443ed593aa72",
        "pre_t5_backend_blob": "f32fc0441efd649bcb7196a91354cc7311bc384b",
    },
}
WVS7_SUCCESSOR_DISCOVERY_AUTHORITY = "3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873"
WVS7_SUCCESSOR_LOCK2 = "5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139"
WVS7_SUCCESSOR_LOCK2_REPLAY = "9b5ac1726a03798d07e965396192d1bfefbee6d2188bad5a3acfb467ef063d4a"
WVS7_FRESH_ORACLE_IDENTITY = "3694b8bd0b5468433a1a83bd469337c7e36e552c3a9a5fef65fff88df8fce800"
WVS7_FRESH_ORACLE_TRUTH_PAYLOAD = "eb2f9224219385dbf21af70d317e0978383012ff057ce2ac857b59c130472405"

HISTORICAL_C_FAILURE_PATHS = frozenset({
    "WORKER_RETURNS/EE-P2X/05_LITS_I_C_TERMINAL_BINDING_BLOCKER.json",
    "WORKER_RETURNS/EE-P2X/13_WVS7_C_PRESERVED_PORTABILITY_FAILURE.json",
})


class LiveTerminalControlError(RuntimeError):
    pass


def _canon(value: Any) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, default=str
    ).encode("utf-8")


def _hash(value: Any) -> str:
    return hashlib.sha256(_canon(value)).hexdigest()


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _load(path: Path) -> Mapping[str, Any]:
    p = Path(path)
    if not p.is_file():
        raise LiveTerminalControlError(f"required receipt/document missing: {p}")
    try:
        value = json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        raise LiveTerminalControlError(f"malformed JSON: {p}") from exc
    if not isinstance(value, Mapping):
        raise LiveTerminalControlError(f"document must be a mapping: {p}")
    return value


def _atomic(path: Path, value: Mapping[str, Any]) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(
        value, sort_keys=True, indent=2, ensure_ascii=False, default=str
    ) + "\n"
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(data, encoding="utf-8")
    os.replace(tmp, p)
    return p


def _ref_key(ref: Mapping[str, Any]) -> tuple[str, str, str]:
    return (
        str(ref.get("kind", "")),
        str(ref.get("object_id", "")),
        str(ref.get("content_hash", "")),
    )


def _unique_refs(refs: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    by = {_ref_key(ref): canonicalize(ref) for ref in refs}
    return [by[key] for key in sorted(by)]


def validate_current_court_contract(
    document: Mapping[str, Any], current_manifest: Mapping[str, Any]
) -> str:
    if document.get("schema") != COURT_CONTRACT_SCHEMA:
        raise LiveTerminalControlError("T5 current court contract schema drift")
    if document.get("claim_scope") != CLAIM_SCOPE:
        raise LiveTerminalControlError("T5 court claim scope drift")
    if document.get("claim_boundary") != EXPECTED_CLAIM_BOUNDARY:
        raise LiveTerminalControlError("T5 claim boundary drift or overclaim")
    if document.get("current_execution_manifest") != EXPECTED_CURRENT_EXECUTION_MANIFEST:
        raise LiveTerminalControlError("T5 current execution manifest binding drift")
    if document.get("required_contracts") != EXPECTED_REQUIRED_CONTRACTS:
        raise LiveTerminalControlError("T5 required contract identity drift")
    if document.get("t4_accounting_required_surfaces") != EXPECTED_T4_ACCOUNTING_SURFACES:
        raise LiveTerminalControlError("T4 accounting surface closure drift")
    if document.get("preservation_anchors") != EXPECTED_PRESERVATION_ANCHORS:
        raise LiveTerminalControlError("T1-T4 preservation anchor drift")
    r35 = document.get("r35_post_t5_convergence")
    if not isinstance(r35, Mapping):
        raise LiveTerminalControlError("R35 post-T5 convergence boundary missing")
    if (
        r35.get("branch") != "agent/vozhd-premain-fiabc-r35-fanin-r1"
        or r35.get("hq_seal") != "c3c83908fb0083c575ab1b5ea2a3a6d84f14b5ff"
        or r35.get("merged_in_t5") is not False
        or r35.get("required_before_final_qualification") is not True
    ):
        raise LiveTerminalControlError("R35 bounded convergence boundary drift")
    if tuple(document.get("sources", ())) != EXPECTED_SOURCES:
        raise LiveTerminalControlError("T5 court source set drift")
    if tuple(document.get("candidates", ())) != EXPECTED_CANDIDATES:
        raise LiveTerminalControlError("T5 court candidate set drift")
    cells = document.get("cells")
    if not isinstance(cells, Sequence) or isinstance(cells, (str, bytes)):
        raise LiveTerminalControlError("T5 court cells missing")
    observed = {
        (item.get("source"), item.get("candidate"))
        for item in cells
        if isinstance(item, Mapping)
    }
    if observed != set(EXPECTED_CELLS) or len(cells) != 6:
        raise LiveTerminalControlError("T5 court must contain exactly six current cells")
    for source, sha in EXPECTED_SOURCE_SHA.items():
        if document.get("source_roots", {}).get(source) != sha:
            raise LiveTerminalControlError(f"T5 canonical source root drift: {source}")
        if current_manifest.get("sources", {}).get(source, {}).get("sha256") != sha:
            raise LiveTerminalControlError(f"T2 manifest source root drift: {source}")
    if document.get("candidate_owner_blobs") != EXPECTED_OWNER_BLOBS:
        raise LiveTerminalControlError("frozen candidate-owner set drift")
    if (
        document.get("current_execution_manifest", {}).get("schema")
        != current_manifest.get("schema")
    ):
        raise LiveTerminalControlError("T5 contract not bound to T2 current manifest schema")
    historical = document.get("historical_candidate_c_failures", [])
    if set(historical) != set(HISTORICAL_C_FAILURE_PATHS):
        raise LiveTerminalControlError("historical Candidate-C inventory drift")
    if document.get("historical_failures_are_current_capability_law") is not False:
        raise LiveTerminalControlError("historical Candidate-C failure reused as current law")
    for cell in cells:
        if not isinstance(cell, Mapping):
            raise LiveTerminalControlError("malformed current cell contract")
        if cell.get("state") != "CURRENT_ADMITTED":
            raise LiveTerminalControlError("one of six capabilities is not current-admitted")
        if str(cell.get("current_capability_ref", "")) in HISTORICAL_C_FAILURE_PATHS:
            raise LiveTerminalControlError(
                "historical Candidate-C failure cannot satisfy current capability"
            )
    return _hash(document)


def validate_current_court_contract_file(
    path: Path, current_manifest: Mapping[str, Any]
) -> Mapping[str, Any]:
    doc = _load(path)
    digest = validate_current_court_contract(doc, current_manifest)
    return {"document": doc, "sha256": digest, "path": str(Path(path).resolve())}


def run_live_succession_preflight(
    *,
    manifest_path: Path,
    lifecycle_context_path: Path,
    repo_root: Path,
    repo_head: str,
    court_contract_path: Path,
    current_manifest: Mapping[str, Any],
    output_path: Path,
) -> Mapping[str, Any]:
    court = validate_current_court_contract_file(court_contract_path, current_manifest)
    manifest = _load(manifest_path)
    lifecycle = _load(lifecycle_context_path)
    result = evaluate_manifest(
        manifest,
        resolver=GitEvidenceResolver(repo_root),
        lifecycle_context=lifecycle,
    )
    require_preflight_pass(result)
    ident = manifest.get("manifest_identity", {})
    if not isinstance(ident, Mapping):
        raise LiveTerminalControlError("succession manifest identity missing")
    if ident.get("frozen_before_candidate_execution") is not True:
        raise LiveTerminalControlError("succession manifest was not frozen pre-candidate")
    if ident.get("generated_from_commit_sha") != repo_head:
        raise LiveTerminalControlError(
            "succession manifest does not bind current execution commit"
        )
    body = {
        "schema": PREFLIGHT_RECEIPT_SCHEMA,
        "status": "PASS",
        "repo_head": repo_head,
        "manifest_path": str(Path(manifest_path).resolve()),
        "manifest_identity": ident.get("manifest_content_sha256"),
        "evaluated_manifest_sha256": result.evaluated_manifest_sha256,
        "lifecycle_context_sha256": _sha(Path(lifecycle_context_path)),
        "court_contract_sha256": court["sha256"],
        "i07_result": result.as_dict(),
        "candidate_execution_started": False,
    }
    body["receipt_identity"] = _hash(body)
    _atomic(output_path, body)
    return body


def validate_live_succession_preflight_receipt(
    path: Path,
    *,
    repo_head: str,
    court_contract_path: Path,
    current_manifest: Mapping[str, Any],
) -> Mapping[str, Any]:
    doc = _load(path)
    court = validate_current_court_contract_file(court_contract_path, current_manifest)
    if doc.get("schema") != PREFLIGHT_RECEIPT_SCHEMA or doc.get("status") != "PASS":
        raise LiveTerminalControlError("succession preflight receipt is not PASS")
    if doc.get("repo_head") != repo_head:
        raise LiveTerminalControlError("succession preflight receipt is stale")
    if doc.get("court_contract_sha256") != court["sha256"]:
        raise LiveTerminalControlError("succession preflight court-contract binding drift")
    i07 = doc.get("i07_result")
    if not isinstance(i07, Mapping) or i07.get("status") != "PASS":
        raise LiveTerminalControlError("embedded I07 result is not PASS")
    if doc.get("candidate_execution_started") is not False:
        raise LiveTerminalControlError("succession preflight was not pre-candidate")
    material = {key: value for key, value in doc.items() if key != "receipt_identity"}
    if doc.get("receipt_identity") != _hash(material):
        raise LiveTerminalControlError("succession preflight receipt identity drift")
    return doc


def _oracle_path(entry: Mapping[str, Any], freeze_path: Path) -> Path:
    raw = entry.get("oracle_document_path")
    if not isinstance(raw, str) or not raw:
        raise LiveTerminalControlError("frozen oracle entry lacks oracle_document_path")
    p = Path(raw)
    return p.resolve() if p.is_absolute() else (freeze_path.resolve().parent / p).resolve()


def load_frozen_source_oracle(
    *, freeze_path: Path, source: str, work_root: Path
) -> tuple[Mapping[str, Any], Mapping[str, Any], str]:
    freeze, freeze_sha = load_frozen_upstream_receipt(Path(freeze_path))
    entry = freeze.get("oracle_identities", {}).get(source)
    if not isinstance(entry, Mapping):
        raise LiveTerminalControlError(f"frozen upstream lacks oracle for {source}")
    p = _oracle_path(entry, Path(freeze_path))
    cells = Path(work_root).resolve() / "cells"
    if p == cells or cells in p.parents:
        raise LiveTerminalControlError("candidate-owned root cannot contain oracle")
    if not p.is_file():
        raise LiveTerminalControlError("frozen oracle document is absent")
    expected_file_sha = entry.get("oracle_document_sha256")
    if (
        not isinstance(expected_file_sha, str)
        or len(expected_file_sha) != 64
        or _sha(p) != expected_file_sha
    ):
        raise LiveTerminalControlError("frozen oracle document byte identity drift")
    oracle = _load(p)
    identity = verify_frozen_oracle(oracle)
    if identity != entry.get("oracle_identity_sha256"):
        raise LiveTerminalControlError("T3 oracle identity differs from oracle document")
    if oracle.get("source") != source:
        raise LiveTerminalControlError("frozen oracle source drift")
    if freeze.get("candidate_outputs_seen") != 0:
        raise LiveTerminalControlError("oracle frozen after candidate output")
    if freeze.get("candidate_owned_roots_consulted") not in ([], ()):
        raise LiveTerminalControlError("oracle consulted candidate-owned roots")
    return oracle, freeze, freeze_sha


def _source_identity(source: str, source_sha256: str) -> Mapping[str, Any]:
    shape = {"LITS_I": (29002, 1198), "WVS7": (97220, 613)}.get(source)
    if shape is None or EXPECTED_SOURCE_SHA.get(source) != source_sha256:
        raise LiveTerminalControlError("candidate observation source identity drift")
    return {
        "source": source,
        "sha256": source_sha256,
        "rows": shape[0],
        "variables": shape[1],
    }


def _court_constitution(
    source: str, freeze: Mapping[str, Any]
) -> Mapping[str, Any]:
    base = {
        "frozen_authority_identity": canonicalize(
            freeze["authority_identities"][source]
        ),
        "frozen_workload_identity": canonicalize(
            freeze["workload_identities"][source]
        ),
    }
    if source == "WVS7":
        base.update({
            "lock2_hash": WVS7_SUCCESSOR_LOCK2,
            "lock2_replay_hash": WVS7_SUCCESSOR_LOCK2_REPLAY,
            "discovery_authority": WVS7_SUCCESSOR_DISCOVERY_AUTHORITY,
            "empirical_universe": WVS7_EMPIRICAL_UNIVERSE,
            "risk_set": WVS7_RISK_SET,
            "measure_basis": WVS7_MEASURE_BASIS,
        })
    return base


def _projection_refs(
    source: str, binding: Any, state: Mapping[str, Any]
) -> Mapping[str, Any]:
    releases = list(binding.executor.release_refs)
    if not releases:
        raise LiveTerminalControlError("C11 release set is empty")
    replay_refs = []
    for ref in releases:
        release = binding.executor.repository.resolve_release_exact(ref)
        replay_refs.append(release.replay_manifest.ref.as_dict())
    material = {
        "projection_identity": state.get("bindings", {}).get("projection_identity"),
        "release_refs": [ref.as_dict() for ref in releases],
        "release_replay_refs": replay_refs,
    }
    if source == "LITS_I":
        if len(releases) != 1 or releases[0].content_hash != LITS_C11_RELEASE_IDENTITY:
            raise LiveTerminalControlError("LiTS C11 release identity drift")
        replay_hash = replay_refs[0]["content_hash"]
        if replay_hash != LITS_C11_REPLAY_IDENTITY:
            raise LiveTerminalControlError("LiTS C11 replay identity drift")
        material.update({
            "c11_release_identity": releases[0].content_hash,
            "c11_replay_identity": replay_hash,
        })
    return material


def _constituent_i03(
    binding: Any, result: Any
) -> tuple[list[Mapping[str, Any]], list[Mapping[str, Any]], str]:
    candidate_rows = []
    global_facts: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    fact_preimages = {
        _ref_key(fact.ref.as_dict()): fact
        for fact in getattr(result, "empirical_facts", ())
    }
    all_expected = {_ref_key(ref.as_dict()) for ref in result.empirical_fact_refs}
    if set(fact_preimages) != all_expected:
        raise LiveTerminalControlError(
            "retained I03 fact preimages do not close over I05 fact refs"
        )
    ordered = sorted(
        result.receipts, key=lambda receipt: receipt.candidate_identity["candidate_hash"]
    )
    for receipt in ordered:
        per_candidate: dict[tuple[str, str, str], Mapping[str, Any]] = {}
        query_roles = receipt.candidate_identity["query_roles"]
        expected = {
            _ref_key(ref if isinstance(ref, Mapping) else ref.as_dict())
            for ref in receipt.empirical_fact_refs
        }
        support = receipt.support_uncertainty_state
        states = support.get("fact_states") if isinstance(support, Mapping) else None
        if (
            not isinstance(states, Sequence)
            or isinstance(states, (str, bytes))
            or len(states) != len(receipt.empirical_fact_refs)
        ):
            raise LiveTerminalControlError("I05 receipt fact-state preimages are incomplete")
        for ref, retained_state in zip(receipt.empirical_fact_refs, states):
            ref_doc = ref if isinstance(ref, Mapping) else ref.as_dict()
            fact = fact_preimages.get(_ref_key(ref_doc))
            if fact is None or fact.typed_state != retained_state:
                raise LiveTerminalControlError("I05 retained fact preimage/state mismatch")
            row = {"ref": fact.ref.as_dict(), "typed_state": fact.typed_state}
            per_candidate[_ref_key(row["ref"])] = row
            global_facts[_ref_key(row["ref"])] = row

        role_fact_refs = support.get("query_role_fact_refs")
        role_names = {role.get("role") for role in query_roles if isinstance(role, Mapping)}
        if not isinstance(role_fact_refs, Mapping) or set(role_fact_refs) != role_names:
            raise LiveTerminalControlError("I05 query-role fact closure is incomplete")
        role_closure = set()
        for refs in role_fact_refs.values():
            if not isinstance(refs, Sequence) or isinstance(refs, (str, bytes)):
                raise LiveTerminalControlError("I05 query-role fact refs are malformed")
            role_closure.update(_ref_key(ref) for ref in refs)
        if set(per_candidate) != expected or role_closure != expected:
            raise LiveTerminalControlError(
                "constituent I03 preimages do not close over I05 candidate facts"
            )
        candidate_rows.append({
            "candidate_hash": receipt.candidate_identity["candidate_hash"],
            "typed_state": receipt.typed_state,
            "semantic_fields": {
                "candidate_identity": canonicalize(receipt.candidate_identity),
                "constituent_fact_manifest": [
                    per_candidate[key] for key in sorted(per_candidate)
                ],
                "coverage_state": receipt.coverage_state,
                "support_uncertainty_state": canonicalize(
                    receipt.support_uncertainty_state
                ),
                "replay_ref": canonicalize(receipt.replay_ref),
            },
        })
    if set(global_facts) != all_expected:
        raise LiveTerminalControlError(
            "constituent I03 fact closure differs from I05 fact set"
        )
    manifest = [global_facts[key] for key in sorted(global_facts)]
    closure_identity = semantic_hash({
        "candidate_fact_rows": candidate_rows,
        "constituent_fact_manifest": manifest,
    })
    return candidate_rows, manifest, closure_identity


def project_live_candidate_observation(
    *,
    source: str,
    candidate: str,
    source_sha256: str,
    binding: Any,
    result: Any,
    execution_receipt: Mapping[str, Any],
    state: Mapping[str, Any],
    freeze: Mapping[str, Any],
    oracle_identity_sha256: str,
) -> Mapping[str, Any]:
    if candidate not in EXPECTED_CANDIDATES:
        raise LiveTerminalControlError("unknown candidate")
    projection = _projection_refs(source, binding, state)
    candidate_rows, fact_manifest, i03_closure = _constituent_i03(binding, result)
    ordered = sorted(
        result.receipts, key=lambda receipt: receipt.candidate_identity["candidate_hash"]
    )
    hashes = [receipt.candidate_identity["candidate_hash"] for receipt in ordered]
    query_role_count = sum(
        len(receipt.candidate_identity["query_roles"]) for receipt in ordered
    )
    frontier: dict[str, Any] = {
        "candidate_count": result.candidate_count,
        "ordered_candidate_hashes": hashes,
    }
    if source == "LITS_I":
        frontier.update({
            "query_role_count": query_role_count,
            "frontier_seal": LITS_FRONTIER_SEAL,
        })
    else:
        families = Counter(
            receipt.candidate_identity["family"] for receipt in ordered
        )
        frontier["family_counts"] = dict(sorted(families.items()))
        if tuple(hashes) != tuple(WVS7_ORDERED_CANDIDATE_HASHES):
            raise LiveTerminalControlError("WVS7 live I05 frontier order drift")
        if dict(sorted(families.items())) != dict(sorted(WVS7_FAMILY_COUNTS.items())):
            raise LiveTerminalControlError("WVS7 live I05 family shape drift")
    terminal_counts = _typed_terminal_counts(source, ordered)
    learned = {
        "product_identity": semantic_hash(execution_receipt),
        "semantic_identity": result.replay_ref.content_hash,
        "replay_identity": execution_receipt["execution_identity"],
        "exact_output_identity": execution_receipt["execution_identity"],
        "coverage": {
            "candidate_count": result.candidate_count,
            "query_role_count": query_role_count,
            "typed_terminal_counts": terminal_counts,
        },
    }
    authorities = [
        authority.ref.as_dict()
        for authority in binding.executor.runtime_catalog.authorities
    ]
    exact_refs = _unique_refs([
        *authorities,
        *[
            predicate.ref.as_dict()
            for predicate in binding.executor.runtime_catalog.predicates
        ],
        *[query.ref.as_dict() for query in binding.executor.runtime_catalog.queries],
        *[
            authority.ref.as_dict()
            for authority in binding.executor.runtime_catalog.discovery_authorities
        ],
        *[ref.as_dict() for ref in binding.executor.release_refs],
        result.discovery_authority_ref.as_dict(),
        result.candidate_grammar_ref.as_dict(),
        result.evaluated_frontier_ref.as_dict(),
        result.replay_ref.as_dict(),
        *[ref.as_dict() for ref in result.empirical_fact_refs],
        *[receipt.ref.as_dict() for receipt in result.receipts],
    ])
    replay_manifest = {
        "i05_replay_ref": result.replay_ref.as_dict(),
        "constituent_i03_closure_identity": i03_closure,
        "dependency_root": semantic_hash(exact_refs),
    }
    observation = {
        "schema": OBSERVATION_SCHEMA,
        "candidate": candidate,
        "oracle_identity_sha256": oracle_identity_sha256,
        "source_identity": _source_identity(source, source_sha256),
        "court_constitution_refs": _court_constitution(source, freeze),
        "semantic_authority_closure": canonicalize(authorities),
        "projection_and_release_refs": canonicalize(projection),
        "frontier_manifest": canonicalize(frontier),
        "fact_manifest": canonicalize(candidate_rows),
        "learned_product": canonicalize(learned),
        "replay_manifest": canonicalize(replay_manifest),
        "exact_ref_manifest": canonicalize(exact_refs),
        "negative_state_manifest": canonicalize(NEGATIVE_STATE_LAW),
        "authority_closure_digest": semantic_hash(canonicalize(authorities)),
        "frontier_digest": semantic_hash(canonicalize(frontier)),
        "constituent_i03_fact_manifest": canonicalize(fact_manifest),
        "constituent_i03_closure_identity": i03_closure,
        "self_replay_ok": None,
        "self_replay_used_as_expected_truth": False,
    }
    observation["observation_identity"] = _hash(observation)
    return observation


def _typed_terminal_counts(
    source: str, receipts: Sequence[Any]
) -> Mapping[str, int]:
    """Project the frozen source-specific terminal-state domain exactly."""
    if source == "LITS_I":
        field = "coverage_state"
    elif source == "WVS7":
        field = "typed_state"
    else:
        raise LiveTerminalControlError(
            "unknown source terminal-count compatibility domain"
        )
    values = []
    for receipt in receipts:
        value = getattr(receipt, field, None)
        if not isinstance(value, str) or not value:
            raise LiveTerminalControlError(
                f"{source} receipt lacks exact {field} terminal state"
            )
        values.append(value)
    return dict(sorted(Counter(values).items()))


def _terminal_projection_from_material(
    *,
    source: str,
    source_identity: Mapping[str, Any],
    projection: Mapping[str, Any],
    fact_manifest: Sequence[Mapping[str, Any]],
    i03_closure_identity: str,
    learned: Mapping[str, Any],
    authority_digest: str,
    frontier_digest: str,
    freeze: Mapping[str, Any],
) -> Mapping[str, Any]:
    releases = projection.get("release_refs")
    replays = projection.get("release_replay_refs")
    if (
        not isinstance(releases, Sequence)
        or not releases
        or not isinstance(replays, Sequence)
        or not replays
    ):
        raise LiveTerminalControlError("terminal projection lacks C11 identities")
    c11 = {
        "status": "PASS",
        "logical_release_identity": semantic_hash(canonicalize(releases)),
        "replay_identity": semantic_hash(canonicalize(replays)),
    }
    if source == "LITS_I":
        c11 = {
            "status": "PASS",
            "logical_release_identity": projection.get("c11_release_identity"),
            "replay_identity": projection.get("c11_replay_identity"),
        }
    i03 = {
        "status": "PASS",
        "replay_identity": i03_closure_identity,
        "fact_manifest": list(fact_manifest),
    }
    coverage = learned.get("coverage", {})
    terminal = {
        "source_identity": semantic_hash(canonicalize(source_identity)),
        "workload_identity": semantic_hash(
            canonicalize(freeze["workload_identities"][source])
        ),
        "authority_closure_identity": authority_digest,
        "frontier_identity": frontier_digest,
        "coverage_receipt_identity": semantic_hash(canonicalize(coverage)),
        "learned_product_identity": learned.get("product_identity"),
        "semantic_identity": learned.get("semantic_identity"),
        "replay_identity": learned.get("replay_identity"),
        "output_identity": learned.get("exact_output_identity"),
        "coverage_claim": "COMPLETE_FOR_EXACT_DECLARED_FRONTIER",
        "candidate_count": coverage.get("candidate_count"),
        "covered_candidate_count": coverage.get("candidate_count"),
        "constituent_fact_manifest": list(fact_manifest),
    }
    i05 = {
        **terminal,
        "status": "PASS",
        "constituent_fact_refs": [row["ref"] for row in fact_manifest],
    }
    i05.pop("constituent_fact_manifest")
    return {
        "c11": c11,
        "i03": i03,
        "i05": i05,
        "terminal_identity": terminal,
    }


def terminal_projection_from_observation(
    observation: Mapping[str, Any], freeze: Mapping[str, Any]
) -> Mapping[str, Any]:
    return _terminal_projection_from_material(
        source=observation["source_identity"]["source"],
        source_identity=observation["source_identity"],
        projection=observation["projection_and_release_refs"],
        fact_manifest=observation["constituent_i03_fact_manifest"],
        i03_closure_identity=observation["constituent_i03_closure_identity"],
        learned=observation["learned_product"],
        authority_digest=observation["authority_closure_digest"],
        frontier_digest=observation["frontier_digest"],
        freeze=freeze,
    )


def _oracle_fact_manifest(oracle: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    out: dict[tuple[str, str, str], Mapping[str, Any]] = {}
    rows = oracle.get("expected_fact_manifest")
    if not isinstance(rows, Sequence):
        raise LiveTerminalControlError("oracle expected fact manifest missing")
    for row in rows:
        if not isinstance(row, Mapping):
            raise LiveTerminalControlError("oracle expected fact row malformed")
        semantic = row.get("semantic_fields")
        if not isinstance(semantic, Mapping):
            raise LiveTerminalControlError(
                "T5 oracle material lacks standardized semantic_fields"
            )
        facts = semantic.get("constituent_fact_manifest")
        if not isinstance(facts, Sequence):
            raise LiveTerminalControlError(
                "T5 oracle material lacks constituent I03 facts"
            )
        for fact in facts:
            if (
                not isinstance(fact, Mapping)
                or not isinstance(fact.get("ref"), Mapping)
                or not isinstance(fact.get("typed_state"), str)
            ):
                raise LiveTerminalControlError("oracle constituent fact row malformed")
            out[_ref_key(fact["ref"])] = canonicalize(fact)
    return [out[key] for key in sorted(out)]


def terminal_projection_from_oracle(
    oracle: Mapping[str, Any], freeze: Mapping[str, Any]
) -> Mapping[str, Any]:
    replay = oracle.get("replay_manifest")
    if not isinstance(replay, Mapping) or not isinstance(
        replay.get("constituent_i03_closure_identity"), str
    ):
        raise LiveTerminalControlError(
            "T5 oracle replay manifest lacks constituent I03 closure identity"
        )
    return _terminal_projection_from_material(
        source=oracle["source"],
        source_identity=oracle["source_identity"],
        projection=oracle["projection_and_release_refs"],
        fact_manifest=_oracle_fact_manifest(oracle),
        i03_closure_identity=replay["constituent_i03_closure_identity"],
        learned=oracle["expected_learned_product"],
        authority_digest=oracle["authority_closure_digest"],
        frontier_digest=oracle["frontier_digest"],
        freeze=freeze,
    )


def _cell_receipts_root(work_root: Path, source: str, candidate: str) -> Path:
    return Path(work_root) / "cells" / source / candidate / "receipts"


def admit_post_i05_oracle_match(
    *,
    stage: Any,
    roots: Any,
    work_root: Path,
    freeze_path: Path,
    backend_receipt: Mapping[str, Any],
) -> Mapping[str, Any]:
    if stage.stage_id != "S05_I05_LEARNED_PRODUCTION":
        raise LiveTerminalControlError("oracle match is only lawful after I05")
    payload = backend_receipt.get("stage_payload")
    if not isinstance(payload, Mapping):
        raise LiveTerminalControlError("S05 backend receipt lacks payload")
    observation = payload.get("t5_candidate_observation")
    if (
        not isinstance(observation, Mapping)
        or observation.get("schema") != OBSERVATION_SCHEMA
    ):
        raise LiveTerminalControlError("complete candidate observation absent after I05")
    if observation.get("candidate") != stage.candidate:
        raise LiveTerminalControlError("candidate observation identity drift")
    oracle, _freeze, _freeze_sha = load_frozen_source_oracle(
        freeze_path=freeze_path, source=stage.source, work_root=work_root
    )
    accepted = validate_candidate_observation(oracle, observation)
    wrapper = {
        "schema": MATCH_WRAPPER_SCHEMA,
        "status": "PASS",
        "source": stage.source,
        "candidate": stage.candidate,
        "oracle_identity_sha256": oracle["oracle_identity_sha256"],
        "accepted_match_receipt": accepted,
        "observation_identity": observation.get("observation_identity"),
        "self_replay_used_as_expected_truth": False,
        "performance_admission": "ADMITTED_ONLY_AFTER_INDEPENDENT_ORACLE_MATCH",
    }
    wrapper["receipt_identity"] = _hash(wrapper)
    obs_path = Path(roots.receipts) / "fiabc_t5_candidate_observation.json"
    match_path = Path(roots.receipts) / "fiabc_t5_oracle_match.json"
    _atomic(obs_path, observation)
    _atomic(match_path, wrapper)

    three_way = None
    if stage.candidate == "C":
        observations = {}
        for candidate in EXPECTED_CANDIDATES:
            p = (
                _cell_receipts_root(work_root, stage.source, candidate)
                / "fiabc_t5_candidate_observation.json"
            )
            row = _load(p)
            if row.get("candidate") != candidate:
                raise LiveTerminalControlError(
                    "three-way gate encountered candidate substitution"
                )
            observations[candidate] = row
        accepted_three = validate_three_way_parity(oracle, observations)
        three_way = {
            "schema": THREE_WAY_WRAPPER_SCHEMA,
            "status": "PASS",
            "source": stage.source,
            "oracle_identity_sha256": oracle["oracle_identity_sha256"],
            "accepted_three_way_receipt": accepted_three,
            "candidates": ["A", "B", "C"],
            "pairwise_agreement_used_as_truth": False,
            "self_replay_used_as_truth": False,
        }
        three_way["receipt_identity"] = _hash(three_way)
        _atomic(
            Path(work_root) / "court" / "t5_oracle" / f"{stage.source}.json",
            three_way,
        )
    return {
        "status": "PASS",
        "match_receipt_path": str(match_path),
        "match_receipt_identity": wrapper["receipt_identity"],
        "three_way_receipt_identity": (
            None if three_way is None else three_way["receipt_identity"]
        ),
    }


def _current_execution_manifest_for_terminal() -> Mapping[str, Any]:
    raw = os.environ.get("RAWLSING_FIABC_T5_CURRENT_EXECUTION_MANIFEST")
    if not raw:
        raise LiveTerminalControlError(
            "terminal telemetry completeness requires the current six-cell execution manifest"
        )
    return _load(Path(raw))


def _stage_receipts_for_completeness(
    *,
    work_root: Path,
    source: str,
    candidate: str,
    current_manifest: Mapping[str, Any],
) -> Mapping[str, Mapping[str, Any]]:
    root = _cell_receipts_root(work_root, source, candidate)
    out: dict[str, Mapping[str, Any]] = {}
    for stage_id in current_manifest.get("stage_catalog", ()):
        if not isinstance(stage_id, str):
            raise LiveTerminalControlError("current manifest stage catalog is malformed")
        path = root / f"{stage_id.lower()}.json"
        if path.is_file():
            out[stage_id] = _load(path)
    return out


def validate_terminal_telemetry_completeness_from_accounting(
    *,
    accounting: Mapping[str, Any],
    source: str,
    candidate: str,
    current_manifest: Mapping[str, Any],
    work_root: Path,
    completed_qualifying_cell: bool,
) -> Mapping[str, Any]:
    """Re-prove completeness from the canonical T4 receipt and current court law."""
    accounting = validate_t4_terminal_accounting_receipt(accounting)
    telemetry = _load(Path(accounting["telemetry_receipt_path"]))
    if accounting.get("metric_definition_hash") != telemetry.get("metric_definition_hash"):
        raise LiveTerminalControlError(
            "T4 accounting wrapper metric-definition hash differs from canonical telemetry"
        )
    stage_receipts = _stage_receipts_for_completeness(
        work_root=work_root,
        source=source,
        candidate=candidate,
        current_manifest=current_manifest,
    )
    try:
        return validate_terminal_telemetry_completeness(
            telemetry=telemetry,
            source=source,
            candidate=candidate,
            current_manifest=current_manifest,
            stage_receipts=stage_receipts,
            completed_qualifying_cell=completed_qualifying_cell,
        )
    except TerminalCompletenessError as exc:
        raise LiveTerminalControlError(
            f"terminal telemetry completeness BLOCK for {source}/{candidate}: {exc}"
        ) from exc


def validate_t4_terminal_accounting_receipt(value: Any) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise LiveTerminalControlError("T4 terminal accounting receipt is missing")
    if value.get("schema") != "FIABC_T4_LIVE_ACCOUNTING_BINDING@1.0.0":
        raise LiveTerminalControlError("T4 terminal accounting contract identity drift")
    if value.get("semantic_state_modified") is not False:
        raise LiveTerminalControlError("T4 accounting may not modify semantic state")
    if value.get("candidate_neutral_c0_excluded") is not True:
        raise LiveTerminalControlError("T4 candidate-neutral C0 exclusion drift")
    path_raw = value.get("telemetry_receipt_path")
    expected_sha = value.get("telemetry_receipt_sha256")
    if not isinstance(path_raw, str) or not path_raw:
        raise LiveTerminalControlError("T4 terminal telemetry receipt path missing")
    if not isinstance(expected_sha, str) or len(expected_sha) != 64:
        raise LiveTerminalControlError("T4 terminal telemetry receipt SHA missing")
    path = Path(path_raw)
    if not path.is_file():
        raise LiveTerminalControlError("T4 terminal telemetry receipt file missing")
    if _sha(path) != expected_sha:
        raise LiveTerminalControlError("T4 terminal telemetry receipt byte drift")
    return value


def seal_live_cell_terminal(
    *, stage: Any, roots: Any, work_root: Path, freeze_path: Path,
    backend_receipt: Mapping[str, Any],
) -> Mapping[str, Any]:
    if stage.stage_id != "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS":
        raise LiveTerminalControlError("cell terminal may only seal at S16")
    observation = _load(
        Path(roots.receipts) / "fiabc_t5_candidate_observation.json"
    )
    match = _load(Path(roots.receipts) / "fiabc_t5_oracle_match.json")
    if match.get("status") != "PASS" or match.get("candidate") != stage.candidate:
        raise LiveTerminalControlError("cell terminal lacks independent oracle PASS")
    _oracle, freeze, _ = load_frozen_source_oracle(
        freeze_path=freeze_path, source=stage.source, work_root=work_root
    )
    projection = terminal_projection_from_observation(observation, freeze)
    t4_accounting = validate_t4_terminal_accounting_receipt(
        backend_receipt.get("t4_accounting")
    )
    current_manifest = _current_execution_manifest_for_terminal()
    telemetry_completeness = validate_terminal_telemetry_completeness_from_accounting(
        accounting=t4_accounting,
        source=stage.source,
        candidate=stage.candidate,
        current_manifest=current_manifest,
        work_root=work_root,
        completed_qualifying_cell=True,
    )
    journal = _load(Path(roots.receipts) / "fiabc_t4_live_accounting_journal.json")
    s15 = journal.get("stages", {}).get(
        f"{stage.source}/{stage.candidate}/S15_FRESH_PROCESS_REPLAY"
    )
    if not isinstance(s15, Mapping):
        raise LiveTerminalControlError("T4 fresh-process replay receipt absent")
    life = s15.get("lifecycle_receipt")
    if (
        not isinstance(life, Mapping)
        or life.get("disposition") != "EXECUTED_NOW"
        or life.get("action") != "FRESH_PROCESS_REPLAY"
    ):
        raise LiveTerminalControlError("T4 fresh replay is not executed-now")
    terminal = projection["terminal_identity"]
    if life.get("terminal_identity") != terminal.get("output_identity"):
        raise LiveTerminalControlError("T4 lifecycle replay changed terminal output identity")
    payload=backend_receipt.get("stage_payload")
    if not isinstance(payload,Mapping):
        raise LiveTerminalControlError("S16 backend payload absent for lifecycle terminal closure")
    replay_projection=payload.get("fresh_process_terminal_projection")
    if not isinstance(replay_projection,Mapping):
        raise LiveTerminalControlError("fresh-process replay lacks full terminal projection")
    if canonicalize(replay_projection) != canonicalize(projection):
        raise LiveTerminalControlError(
            "T4 fresh-process replay changed the full C11/I03/I05 terminal projection"
        )
    bundle = {
        "schema": CELL_TERMINAL_SCHEMA,
        "source_id": stage.source,
        "candidate_id": stage.candidate,
        "terminal_disposition": "PASS",
        "oracle_match_receipt_identity": match.get("receipt_identity"),
        "t4_accounting_receipt": {
            "schema": t4_accounting.get("schema"),
            "journal_sha256": t4_accounting.get("journal_sha256"),
            "telemetry_receipt_path": t4_accounting.get("telemetry_receipt_path"),
            "telemetry_receipt_sha256": t4_accounting.get("telemetry_receipt_sha256"),
            "metric_definition_hash": t4_accounting.get("metric_definition_hash"),
            "semantic_state_modified": t4_accounting.get("semantic_state_modified"),
            "candidate_neutral_c0_excluded": t4_accounting.get("candidate_neutral_c0_excluded"),
        },
        "telemetry_completeness_receipt": telemetry_completeness,
        "c11": projection["c11"],
        "i03": projection["i03"],
        "i05": projection["i05"],
        "required_lifecycle_phases": ["FRESH_PROCESS_REPLAY"],
        "lifecycle_reproductions": [{
            "phase": "FRESH_PROCESS_REPLAY",
            "status": "PASS",
            "terminal_identity": terminal,
            "t4_lifecycle_receipt_identity": life.get("receipt_id"),
        }],
    }
    bundle["receipt_identity"] = _hash(bundle)
    path = Path(roots.receipts) / "fiabc_t5_cell_terminal.json"
    _atomic(path, bundle)
    return {
        "status": "PASS",
        "path": str(path),
        "receipt_identity": bundle["receipt_identity"],
    }


def _source_oracle_for_i08(
    *,
    source: str,
    oracle: Mapping[str, Any],
    freeze: Mapping[str, Any],
    work_root: Path,
) -> Mapping[str, Any]:
    three = _load(Path(work_root) / "court" / "t5_oracle" / f"{source}.json")
    if (
        three.get("status") != "PASS"
        or three.get("oracle_identity_sha256")
        != oracle.get("oracle_identity_sha256")
    ):
        raise LiveTerminalControlError("source A/B/C oracle gate absent or stale")
    projection = terminal_projection_from_oracle(oracle, freeze)
    matches = []
    for candidate in EXPECTED_CANDIDATES:
        match = _load(
            _cell_receipts_root(work_root, source, candidate)
            / "fiabc_t5_oracle_match.json"
        )
        if (
            match.get("status") != "PASS"
            or match.get("oracle_identity_sha256")
            != oracle.get("oracle_identity_sha256")
        ):
            raise LiveTerminalControlError("candidate oracle match absent")
        matches.append({
            "candidate_id": candidate,
            "status": "PASS",
            "receipt_identity": match.get("receipt_identity"),
        })
    return {
        "source_id": source,
        "oracle_identity": oracle["oracle_identity_sha256"],
        "expected_c11_identity": {
            key: value for key, value in projection["c11"].items()
            if key != "status"
        },
        "expected_i03_identity": {
            key: value for key, value in projection["i03"].items()
            if key != "status"
        },
        "expected_terminal_identity": projection["terminal_identity"],
        "candidate_matches": matches,
    }


def verify_live_final_terminal(
    *,
    work_root: Path,
    repo_root: Path,
    repo_head: str,
    freeze_path: Path,
    preflight_receipt_path: Path,
    court_contract_path: Path,
    current_manifest: Mapping[str, Any],
    output_root: Path,
) -> Mapping[str, Any]:
    del repo_root
    contract = validate_current_court_contract_file(
        court_contract_path, current_manifest
    )
    preflight = validate_live_succession_preflight_receipt(
        preflight_receipt_path,
        repo_head=repo_head,
        court_contract_path=court_contract_path,
        current_manifest=current_manifest,
    )
    source_oracles = []
    oracle_receipt_ids = []
    for source in EXPECTED_SOURCES:
        oracle, freeze, _ = load_frozen_source_oracle(
            freeze_path=freeze_path, source=source, work_root=work_root
        )
        source_oracles.append(
            _source_oracle_for_i08(
                source=source, oracle=oracle, freeze=freeze, work_root=work_root
            )
        )
        three = _load(
            Path(work_root) / "court" / "t5_oracle" / f"{source}.json"
        )
        oracle_receipt_ids.append(three["receipt_identity"])
    cells = []
    for source, candidate in EXPECTED_CELLS:
        cell = _load(
            _cell_receipts_root(work_root, source, candidate)
            / "fiabc_t5_cell_terminal.json"
        )
        if (
            cell.get("source_id") != source
            or cell.get("candidate_id") != candidate
        ):
            raise LiveTerminalControlError("one of six terminal bundles has wrong identity")
        revalidated_completeness = validate_terminal_telemetry_completeness_from_accounting(
            accounting=cell.get("t4_accounting_receipt"),
            source=source,
            candidate=candidate,
            current_manifest=current_manifest,
            work_root=work_root,
            completed_qualifying_cell=True,
        )
        sealed_completeness = cell.get("telemetry_completeness_receipt")
        if (
            not isinstance(sealed_completeness, Mapping)
            or sealed_completeness.get("status") != "PASS"
            or sealed_completeness.get("receipt_identity")
            != revalidated_completeness.get("receipt_identity")
        ):
            raise LiveTerminalControlError(
                "S17 terminal completeness receipt is absent, stale, or disagrees with revalidation"
            )
        cells.append({
            key: value for key, value in cell.items()
            if key not in {
                "schema", "receipt_identity", "oracle_match_receipt_identity"
            }
        })
    oracle_wrapper = {
        "status": "PASS",
        "receipt_identity": _hash({
            "source_three_way_receipts": oracle_receipt_ids
        }),
        "candidate_neutral": True,
        "frozen_before_candidate_output": True,
        "candidate_outputs_seen_at_freeze": 0,
        "candidate_owned_roots_consulted": [],
        "source_oracles": source_oracles,
    }
    document = {
        "schema": TERMINAL_INPUT_SCHEMA,
        "court_id": CLAIM_SCOPE,
        "admitted_cells": [
            {"source_id": source, "candidate_id": candidate}
            for source, candidate in EXPECTED_CELLS
        ],
        "succession_preflight": {
            "status": "PASS",
            "receipt_identity": preflight["receipt_identity"],
            "manifest_identity": preflight["manifest_identity"],
        },
        "independent_parity_oracle": oracle_wrapper,
        "cells": cells,
    }
    result = verify_final_p2_terminal(document)
    root = Path(output_root)
    root.mkdir(parents=True, exist_ok=True)
    input_path = _atomic(root / "fiabc_t5_final_terminal_input.json", document)
    verify_path = _atomic(
        root / "fiabc_t5_final_terminal_verification.json", result
    )
    if result.get("status") != "PASS":
        raise LiveTerminalControlError(
            "I08 final terminal BLOCK: "
            + ",".join(result.get("failure_codes", []))
        )
    body = {
        "schema": FINAL_COMPOSITION_SCHEMA,
        "status": "PASS",
        "claim_scope": CLAIM_SCOPE,
        "claim_boundary": dict(EXPECTED_CLAIM_BOUNDARY),
        "r35_post_t5_convergence": {
            "branch": "agent/vozhd-premain-fiabc-r35-fanin-r1",
            "hq_seal": "c3c83908fb0083c575ab1b5ea2a3a6d84f14b5ff",
            "merged_in_t5": False,
            "required_before_final_qualification": True,
        },
        "terminal_contract": TERMINAL_CONTRACT,
        "court_contract_sha256": contract["sha256"],
        "succession_preflight_receipt_identity": preflight["receipt_identity"],
        "independent_oracle_receipt_identity": oracle_wrapper["receipt_identity"],
        "i08_verification_identity": result["verification_identity"],
        "input_path": str(input_path),
        "verification_path": str(verify_path),
    }
    body["receipt_identity"] = _hash(body)
    final_path = _atomic(root / "fiabc_t5_final_composition.json", body)
    return {**body, "final_path": str(final_path)}


__all__ = [
    "COURT_CONTRACT_SCHEMA",
    "OBSERVATION_SCHEMA",
    "MATCH_WRAPPER_SCHEMA",
    "PREFLIGHT_RECEIPT_SCHEMA",
    "CELL_TERMINAL_SCHEMA",
    "CLAIM_SCOPE",
    "LiveTerminalControlError",
    "validate_current_court_contract",
    "validate_current_court_contract_file",
    "run_live_succession_preflight",
    "validate_live_succession_preflight_receipt",
    "load_frozen_source_oracle",
    "project_live_candidate_observation",
    "admit_post_i05_oracle_match",
    "seal_live_cell_terminal",
    "validate_t4_terminal_accounting_receipt",
    "validate_terminal_telemetry_completeness_from_accounting",
    "verify_live_final_terminal",
    "terminal_projection_from_observation",
    "terminal_projection_from_oracle",
]
