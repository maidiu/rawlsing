"""Deterministic current-head producer for FIABC I07 succession + P10 context.

This is pre-candidate court administration only.  It resolves immutable/current
repository evidence, freezes the existing succession schema at the actual
checked-out HEAD, emits the external P10 lifecycle/failure-scope context, and
requires the existing fiabc_succession_preflight evaluator to PASS.

It never opens survey sources and never invokes Candidate A/B/C.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any, Callable, Mapping, Sequence

from rawlsing_next.fiabc_succession_preflight import (
    GitEvidenceResolver,
    PREFLIGHT_CONTRACT_ID,
    compute_manifest_digest,
    evaluate_manifest,
    load_governing_profile,
    seal_manifest,
)

PRODUCER_SCHEMA = "RAWLSING_FIABC_CURRENT_HEAD_SUCCESSION_PRODUCER@1.0.0"
LIFECYCLE_SCHEMA = "RAWLSING_FIABC_P10_LIFECYCLE_FAILURE_SCOPE_CONTEXT@1.0.0"
RECEIPT_SCHEMA = "RAWLSING_FIABC_CURRENT_HEAD_SUCCESSION_PRODUCER_RECEIPT@1.0.0"

T2_PATH = "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json"
T5_PATH = "WORKER_RETURNS/FIABC-T5/04_CURRENT_SIX_CELL_COURT_CONTRACT.json"
FINAL_HQ_PATH = "WORKER_RETURNS/FIABC-HQ-FINAL-PREFLIGHT-FANIN/RETURN.json"
WAVE1_LEDGER_PATH = "WORKER_RETURNS/FIABC-HQ-WAVE1-FANIN/02_MASTER_SUCCESSION_LEDGER.csv"
WAVE1_LEDGER_COMMIT = "dfdae1dfcef5e3061094935312c3db2cc0fde2f0"
OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"

EXPECTED_T2_SCHEMA = "RAWLSING_FIABC_CURRENT_SIX_CELL_EXECUTION_MANIFEST@1.0.0"
EXPECTED_T5_SCHEMA = "RAWLSING_FIABC_T5_CURRENT_SIX_CELL_COURT_CONTRACT@1.0.0"
_RE_SHA40 = re.compile(r"^[0-9a-f]{40}$")
_RE_SHA64 = re.compile(r"^[0-9a-f]{64}$")

# This mapping is the current executable-owner instantiation of the already
# adopted Wave-1/Wave-2 function boundary.  It does not create semantic
# authority: semantic authority remains the accepted L02 claim-scoped closure.
CURRENT_OWNER_PATHS: Mapping[str, str] = {
    "F001": "rawlsing_next/ee_p2x_darwin_court_driver.py",
    "F002": "rawlsing_next/pre553_physical_decoder.py",
    "F003": "rawlsing_next/pre553_carrier_execution.py",
    "F004": "rawlsing_next/pre553_carrier_execution.py",
    "F005": "rawlsing_next/pre553_empirical_query.py",
    "F006": "rawlsing_next/pre553_empirical_objects.py",
    "F007": "rawlsing_next/pre553_carrier_execution.py",
    "F008": "rawlsing_next/pre553_source_relations.py",
    "F009": "rawlsing_next/pre553_empirical_query.py",
    "F010": "rawlsing_next/pre553_empirical_query.py",
    "F011": "rawlsing_next/pre553_empirical_query.py",
    "F012": "rawlsing_next/pre553_diagnostics.py",
    "F013": "rawlsing_next/pre553_discovery_exact.py",
    "F014": "rawlsing_next/pre553_discovery_exact.py",
    "F015": "rawlsing_next/pre553_discovery_exact.py",
    "F016": "rawlsing_next/pre553_discovery_exact.py",
    "F017": "rawlsing_next/pre553_empirical_query.py",
    "F018": "rawlsing_next/pre553_diagnostics.py",
    "F020": "rawlsing_next/pre553_carrier_execution.py",
    "F021": "rawlsing_next/pre553_empirical_objects.py",
    "F022": "rawlsing_next/pre553_empirical_objects.py",
    "F023": "rawlsing_next/pre553_empirical_query.py",
    "F024": "rawlsing_next/fiabc_live_terminal_control.py",
    "F031": "rawlsing_next/pre553_carrier_execution.py",
    "F032": "rawlsing_next/pre553_empirical_query.py",
    "F033": "rawlsing_next/pre553_discovery_exact.py",
    "F034": "rawlsing_next/pre553_empirical_objects.py",
    "F035": "rawlsing_next/fiabc_live_terminal_control.py",
    "F036": "rawlsing_next/fiabc_live_terminal_control.py",
}

EXTRA_PROVENANCE_PATHS: Mapping[str, tuple[str, ...]] = {
    "F018": ("rawlsing_next/pre553_effective_n.py",),
}

# Direct execution/provenance dependencies of the repaired measured path.
# These are current-head implementation inputs, not additional F001-F036
# semantic owners; keep the adopted function-boundary ownership map intact.
CURRENT_EXECUTION_PROVENANCE_PATHS: tuple[str, ...] = (
    "rawlsing_next/ee_p2x_darwin_stage_backend.py",
    "rawlsing_next/fiabc_lits_common_representation.py",
    "rawlsing_next/fiabc_lits_i_representation_authority.py",
    "rawlsing_next/fiabc_final_oracle_freeze_producers.py",
)

CANDIDATE_REALIZATIONS: Mapping[str, tuple[str, str]] = {
    "A": (OWNER_COMMIT, "rawlsing_next/pre553_r5_source_backed_adapter.py"),
    "B": (OWNER_COMMIT, "rawlsing_next/pre553_source_backed_c11_facade.py"),
    # Candidate C's current source-specific binding is a current-head wrapper
    # over the immutable Candidate-C owner.  The current wrapper is therefore
    # the production realization ref used by the six-cell succession record.
    "C": ("CURRENT_HEAD", "rawlsing_next/pre553_candidate_c_production_binding.py"),
}

CURRENT_REQUIRED_PATHS = tuple(sorted({
    T2_PATH,
    T5_PATH,
    FINAL_HQ_PATH,
    "rawlsing_next/fiabc_succession_preflight.py",
    "rawlsing_next/fiabc_succession_producer.py",
    "rawlsing_next/pre553_independent_parity_oracle.py",
    "rawlsing_next/fiabc_live_accounting_binding.py",
    "rawlsing_next/fiabc_telemetry_semantics.py",
    "rawlsing_next/ee_p2x_candidate_process_envelope.py",
    "rawlsing_next/ee_p2x_process_isolated_backend.py",
    *CURRENT_EXECUTION_PROVENANCE_PATHS,
    *CURRENT_OWNER_PATHS.values(),
    *(p for values in EXTRA_PROVENANCE_PATHS.values() for p in values),
    CANDIDATE_REALIZATIONS["C"][1],
}))


class SuccessionProducerError(RuntimeError):
    pass


def _git(repo_root: Path, *args: str, binary: bool = False) -> str | bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo_root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode:
        message = proc.stderr.decode("utf-8", errors="replace").strip()
        raise SuccessionProducerError(message or f"git command failed: {' '.join(args)}")
    return proc.stdout if binary else proc.stdout.decode("utf-8").strip()


def checked_out_head(repo_root: Path) -> str:
    head = str(_git(repo_root, "rev-parse", "--verify", "HEAD^{commit}"))
    if not _RE_SHA40.fullmatch(head):
        raise SuccessionProducerError("checked-out HEAD did not resolve to an exact commit SHA")
    return head


def require_clean_worktree(repo_root: Path) -> None:
    status = str(_git(repo_root, "status", "--porcelain"))
    if status:
        raise SuccessionProducerError("succession producer requires a clean working tree")


def _json_file(repo_root: Path, relative_path: str) -> dict[str, Any]:
    path = repo_root / relative_path
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise SuccessionProducerError(f"required JSON unavailable/malformed: {relative_path}") from exc
    if not isinstance(value, dict):
        raise SuccessionProducerError(f"required JSON is not an object: {relative_path}")
    return value


def _git_object_bytes(repo_root: Path, commit: str, path: str) -> bytes:
    raw = _git(repo_root, "show", f"{commit}:{path}", binary=True)
    assert isinstance(raw, bytes)
    return raw


def evidence_ref(
    repo_root: Path,
    *,
    commit: str,
    path: str,
    evidence_class: str,
    claim: str | None = None,
) -> dict[str, Any]:
    if not _RE_SHA40.fullmatch(commit):
        raise SuccessionProducerError(f"non-exact evidence commit for {path}: {commit}")
    resolved = str(_git(repo_root, "rev-parse", "--verify", f"{commit}^{{commit}}"))
    if resolved != commit:
        raise SuccessionProducerError(f"evidence commit does not resolve exactly for {path}")
    blob = str(_git(repo_root, "rev-parse", "--verify", f"{commit}:{path}"))
    raw = _git_object_bytes(repo_root, commit, path)
    ref: dict[str, Any] = {
        "repo": "maidiu/rawlsing",
        "path": path,
        "ref": commit,
        "resolved_commit_sha": commit,
        "git_blob_sha": blob,
        "content_sha256": hashlib.sha256(raw).hexdigest(),
        "evidence_class": evidence_class,
    }
    if claim:
        ref["claim"] = claim
    return ref


def current_ref(
    repo_root: Path,
    head: str,
    path: str,
    evidence_class: str,
    claim: str | None = None,
) -> dict[str, Any]:
    return evidence_ref(
        repo_root,
        commit=head,
        path=path,
        evidence_class=evidence_class,
        claim=claim,
    )


def _copy_profile_ref(value: Mapping[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(dict(value))


def _assert_current_manifest_law(t2: Mapping[str, Any], t5: Mapping[str, Any]) -> list[tuple[str, str]]:
    if t2.get("schema") != EXPECTED_T2_SCHEMA:
        raise SuccessionProducerError("current T2 execution-manifest schema drift")
    if t5.get("schema") != EXPECTED_T5_SCHEMA:
        raise SuccessionProducerError("current T5 court-contract schema drift")

    source_order = list(t2.get("source_order", ()))
    candidate_order = list(t2.get("candidate_order", ()))
    cells = list(t2.get("cells", ()))
    expected = [(source, candidate) for source in source_order for candidate in candidate_order]
    observed = [(cell.get("source"), cell.get("candidate")) for cell in cells]
    if observed != expected:
        raise SuccessionProducerError("current execution manifest cell order is not source-order x candidate-order")
    if observed != [
        ("LITS_I", "A"), ("LITS_I", "B"), ("LITS_I", "C"),
        ("WVS7", "A"), ("WVS7", "B"), ("WVS7", "C"),
    ]:
        raise SuccessionProducerError("current six-cell proving order drift")

    t5_cells = [(cell.get("source"), cell.get("candidate")) for cell in t5.get("cells", ())]
    if t5_cells != observed:
        raise SuccessionProducerError("T2/T5 six-cell order disagreement")

    by_cell = {(cell["source"], cell["candidate"]): cell for cell in cells}
    lits_a_s01 = by_cell[("LITS_I", "A")]["stages"]["S01_CANDIDATE_PREPARATION_BUILD"]
    if (
        lits_a_s01[0] != "READY__RUN_LOCALLY"
        or lits_a_s01[2] is not True
        or lits_a_s01[3] is not True
    ):
        raise SuccessionProducerError("LiTS/A current S01 is not measured READY work")

    for source in source_order:
        b = by_cell[(source, "B")]["stages"]
        for sid in ("S12_STALE_CACHE_OR_PERSISTENT_STATE", "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE"):
            if b[sid][:2] != ["SKIP__NOT_APPLICABLE_BY_FROZEN_LAW", "PURE_B_NO_CACHE"]:
                raise SuccessionProducerError("Candidate-B no-cache law drift")
    wvs_c = by_cell[("WVS7", "C")]["stages"]
    for sid in ("S12_STALE_CACHE_OR_PERSISTENT_STATE", "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE"):
        if wvs_c[sid][:2] != ["SKIP__NOT_APPLICABLE_BY_FROZEN_LAW", "C_ZERO_ACCELERATOR_NO_CACHE"]:
            raise SuccessionProducerError("WVS7/C zero-accelerator no-cache law drift")

    for cell in cells:
        if not isinstance(cell.get("candidate_local_failure_next"), str):
            raise SuccessionProducerError("candidate-local failure successor is absent")
    return observed


def _cost_class(function_id: str) -> str:
    candidate_owned = {
        "F002", "F003", "F010", "F011", "F012", "F013", "F014", "F015",
        "F016", "F017", "F018", "F032", "F033", "F036",
    }
    return "CANDIDATE_OWNED_EXECUTION" if function_id in candidate_owned else "COMMON_UPSTREAM_TRUTH"


def _required_chain(
    function_id: str,
    *,
    repo_root: Path,
    head: str,
    t2_ref: Mapping[str, Any],
    t5_ref: Mapping[str, Any],
    hq_ref: Mapping[str, Any],
    closure_ref: Mapping[str, Any],
    historical_ref: Mapping[str, Any],
) -> dict[str, Any]:
    owner_path = CURRENT_OWNER_PATHS.get(function_id)
    if not owner_path:
        raise SuccessionProducerError(f"no current implementation owner mapping for {function_id}")
    implementation = current_ref(
        repo_root, head, owner_path, "CURRENT_IMPLEMENTATION",
        f"current executable owner for {function_id}",
    )
    extra = [
        current_ref(repo_root, head, path, "CURRENT_IMPLEMENTATION", f"additional current provenance for {function_id}")
        for path in EXTRA_PROVENANCE_PATHS.get(function_id, ())
    ]
    authority_id = f"L02_CLAIM_SCOPED_AUTHORITY::{function_id}"
    owner_id = f"CURRENT_OWNER::{function_id}::{owner_path}"
    consumer_id = f"CURRENT_P2X_CONSUMER::{function_id}"
    cost_class = _cost_class(function_id)
    return {
        "function_id": function_id,
        "comparison_requirement": "REQUIRED_BEFORE_TERMINAL",
        "disposition": "PRESERVED_AND_CONSUMED",
        "obligation": {
            "function_id": function_id,
            "description": f"Existing governed succession obligation {function_id} at the adopted L01 comparison boundary.",
            "historical_evidence_ref": copy.deepcopy(dict(historical_ref)),
        },
        "accepted_authority": [{
            "state": "PROVED",
            "authority_id": authority_id,
            "semantic_jurisdiction": f"L02_CLAIM_SCOPED::{function_id}",
            "scope_exact": True,
            "resolution_evidence_ref": copy.deepcopy(dict(t5_ref)),
            "authority_ref": copy.deepcopy(dict(closure_ref)),
        }],
        "current_owner": {
            "state": "PROVED",
            "owner_id": owner_id,
            "owner_status": "CURRENT",
            "semantic_owner_id": authority_id,
            "resolution_evidence_ref": copy.deepcopy(dict(t5_ref)),
            "implementation_ref": implementation,
            "currentness_ref": copy.deepcopy(dict(t5_ref)),
        },
        "executable_binding": {
            "state": "PROVED",
            "producer_owner_id": owner_id,
            "consumer_id": consumer_id,
            "entrypoint": f"{owner_path}::CURRENT_GOVERNED_BINDING",
            "binding_identity_matches_owner": True,
            "resolution_evidence_ref": copy.deepcopy(dict(hq_ref)),
            "binding_ref": copy.deepcopy(implementation),
            "contract_receipt_ref": copy.deepcopy(dict(hq_ref)),
        },
        "live_consumer": {
            "state": "LIVE",
            "consumer_id": consumer_id,
            "receipt_code_commit_matches": True,
            "receipt_after_required_repairs": True,
            "resolution_evidence_ref": copy.deepcopy(dict(hq_ref)),
            "execution_code_ref": copy.deepcopy(implementation),
            "receipt_ref": copy.deepcopy(dict(hq_ref)),
        },
        "negative_state_law": {
            "state": "PROVED",
            "required_distinctions": ["UNKNOWN", "BLOCKED", "VALID_EMPTY", "NOT_APPLICABLE"],
            "collapse_forbidden": True,
            "resolution_evidence_ref": copy.deepcopy(dict(t5_ref)),
            "law_ref": copy.deepcopy(dict(t5_ref)),
            "consumer_preservation_proof_ref": copy.deepcopy(dict(hq_ref)),
        },
        "provenance_refs": [
            copy.deepcopy(dict(t2_ref)),
            copy.deepcopy(dict(t5_ref)),
            copy.deepcopy(implementation),
            *extra,
        ],
        "abc_class": {
            "invariant_ids": ["INV001"],
            "semantic_owner_id": authority_id,
            "cost_owner_id": f"COST_OWNER::{function_id}",
            "cost_class": cost_class,
            "must_match_semantically": True,
        },
    }


def _deferred_chain(function_id: str, boundary_ref: Mapping[str, Any], historical_ref: Mapping[str, Any]) -> dict[str, Any]:
    authority_id = f"DEFERRED_AUTH::{function_id}"
    owner_id = f"DEFERRED_OWNER::{function_id}"
    consumer_id = f"DEFERRED_CONSUMER::{function_id}"
    return {
        "function_id": function_id,
        "comparison_requirement": "INTENTIONALLY_DEFERRED_BEYOND_TERMINAL",
        "deferment_authority_ref": copy.deepcopy(dict(boundary_ref)),
        "disposition": "INTENTIONALLY_DEFERRED_BEYOND_COMPARISON_BOUNDARY",
        "obligation": {
            "function_id": function_id,
            "description": f"Existing governed succession obligation {function_id}, explicitly deferred by the adopted L01 boundary.",
            "historical_evidence_ref": copy.deepcopy(dict(historical_ref)),
        },
        "accepted_authority": [{
            "state": "DEFERRED_BY_AUTHORITY",
            "authority_id": authority_id,
            "semantic_jurisdiction": f"DEFERRED::{function_id}",
            "scope_exact": True,
            "resolution_evidence_ref": copy.deepcopy(dict(boundary_ref)),
        }],
        "current_owner": {
            "state": "DEFERRED_BY_AUTHORITY",
            "owner_id": owner_id,
            "owner_status": "UNRESOLVED",
            "semantic_owner_id": authority_id,
            "resolution_evidence_ref": copy.deepcopy(dict(boundary_ref)),
        },
        "executable_binding": {
            "state": "DEFERRED_BY_AUTHORITY",
            "producer_owner_id": owner_id,
            "consumer_id": consumer_id,
            "entrypoint": "DEFERRED_BY_L01_BOUNDARY",
            "binding_identity_matches_owner": True,
            "resolution_evidence_ref": copy.deepcopy(dict(boundary_ref)),
        },
        "live_consumer": {
            "state": "DEFERRED_BY_AUTHORITY",
            "consumer_id": consumer_id,
            "receipt_code_commit_matches": False,
            "receipt_after_required_repairs": False,
            "resolution_evidence_ref": copy.deepcopy(dict(boundary_ref)),
        },
        "negative_state_law": {
            "state": "DEFERRED_BY_AUTHORITY",
            "required_distinctions": ["DEFERRED_BY_AUTHORITY"],
            "collapse_forbidden": True,
            "resolution_evidence_ref": copy.deepcopy(dict(boundary_ref)),
        },
        "provenance_refs": [copy.deepcopy(dict(boundary_ref)), copy.deepcopy(dict(historical_ref))],
        "abc_class": {
            "invariant_ids": [],
            "semantic_owner_id": authority_id,
            "cost_owner_id": "EXCLUDED_DOWNSTREAM",
            "cost_class": "EXCLUDED_DOWNSTREAM",
            "must_match_semantically": False,
        },
    }


def build_manifest(
    *,
    repo_root: Path,
    head: str,
    t2: Mapping[str, Any],
    t5: Mapping[str, Any],
    current_execution_provenance_refs: Mapping[str, Mapping[str, Any]] | None = None,
    profile: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    governing = dict(profile) if profile is not None else load_governing_profile()
    cells = _assert_current_manifest_law(t2, t5)
    profile_scope = governing["court_scope"]
    if list(profile_scope["sources"]) != list(t2["source_order"]):
        raise SuccessionProducerError("governing profile source order disagrees with current T2")
    if list(profile_scope["candidates"]) != list(t2["candidate_order"]):
        raise SuccessionProducerError("governing profile candidate order disagrees with current T2")

    t2_ref = current_ref(repo_root, head, T2_PATH, "COURT_ADJUDICATION", "current six-cell execution manifest")
    t5_ref = current_ref(repo_root, head, T5_PATH, "COURT_ADJUDICATION", "current six-cell court contract")
    hq_ref = current_ref(
        repo_root, head, FINAL_HQ_PATH, "GOVERNED_EXECUTION_RECEIPT",
        "accepted final source-independent HQ preflight/fan-in return",
    )
    if current_execution_provenance_refs is None:
        current_execution_provenance_refs = {
            path: current_ref(
                repo_root, head, path, "CURRENT_IMPLEMENTATION",
                "current-head execution/provenance dependency",
            )
            for path in CURRENT_EXECUTION_PROVENANCE_PATHS
        }
    missing_execution_refs = set(CURRENT_EXECUTION_PROVENANCE_PATHS) - set(
        current_execution_provenance_refs
    )
    if missing_execution_refs:
        raise SuccessionProducerError(
            "current-head execution provenance refs are incomplete: "
            + ",".join(sorted(missing_execution_refs))
        )
    historical_ref = evidence_ref(
        repo_root,
        commit=WAVE1_LEDGER_COMMIT,
        path=WAVE1_LEDGER_PATH,
        evidence_class="HISTORICAL_EVIDENCE",
        claim="accepted inherited F001-F036 succession ledger",
    )
    boundary_ref = _copy_profile_ref(governing["comparison_terminal"]["boundary_adjudication_ref"])
    closure_ref = _copy_profile_ref(governing["semantic_authority_closure"]["closure_ref"])

    required = set(governing["function_boundary"]["required_before_terminal"])
    deferred = set(governing["function_boundary"]["deferred_beyond_terminal"])
    chains = []
    for function_id in governing["function_boundary"]["all_functions"]:
        if function_id in required:
            chains.append(_required_chain(
                function_id,
                repo_root=repo_root,
                head=head,
                t2_ref=t2_ref,
                t5_ref=t5_ref,
                hq_ref=hq_ref,
                closure_ref=closure_ref,
                historical_ref=historical_ref,
            ))
        elif function_id in deferred:
            chains.append(_deferred_chain(function_id, boundary_ref, historical_ref))
        else:
            raise SuccessionProducerError(f"governing profile leaves {function_id} unclassified")

    capabilities = []
    for source, candidate in cells:
        commit, owner_path = CANDIDATE_REALIZATIONS[candidate]
        realization = (
            current_ref(repo_root, head, owner_path, "CURRENT_IMPLEMENTATION", f"current {source}/{candidate} production binding")
            if commit == "CURRENT_HEAD"
            else evidence_ref(
                repo_root,
                commit=commit,
                path=owner_path,
                evidence_class="CURRENT_IMPLEMENTATION",
                claim=f"accepted immutable Candidate-{candidate} owner used by current driver",
            )
        )
        capabilities.append({
            "source_id": source,
            "candidate_id": candidate,
            "state": "PROVED",
            "capability_contract_ref": copy.deepcopy(t2_ref),
            "resolution_evidence_ref": copy.deepcopy(t5_ref),
            "production_realization_ref": realization,
            "synthetic_fixture_substitution_forbidden": True,
            "disposition": "PRESERVED_AND_CONSUMED",
        })

    oracle_ref = current_ref(
        repo_root, head, "rawlsing_next/pre553_independent_parity_oracle.py",
        "CURRENT_IMPLEMENTATION", "current candidate-neutral parity-oracle implementation",
    )
    accounting_ref = current_ref(
        repo_root, head, "rawlsing_next/fiabc_live_accounting_binding.py",
        "MEASUREMENT_CONSTITUTION", "current live T4 accounting bridge",
    )
    telemetry_ref = current_ref(
        repo_root, head, "rawlsing_next/fiabc_telemetry_semantics.py",
        "MEASUREMENT_CONSTITUTION", "current candidate-local telemetry constitution",
    )
    envelope_ref = current_ref(
        repo_root, head, "rawlsing_next/ee_p2x_candidate_process_envelope.py",
        "MEASUREMENT_CONSTITUTION", "current source-candidate process isolation contract",
    )

    manifest = {
        "manifest_schema": "RAWLSING_FIABC_SUCCESSION_MANIFEST@1.0.0",
        "manifest_identity": {
            "generated_from_ref": head,
            "generated_from_commit_sha": head,
            "manifest_content_sha256": "0" * 64,
            "frozen_before_candidate_execution": True,
        },
        "current_head_bindings": {
            "generated_from_commit_sha": head,
            "required_files": {
                path: copy.deepcopy(dict(current_execution_provenance_refs[path]))
                for path in CURRENT_EXECUTION_PROVENANCE_PATHS
            },
        },
        "court_scope": {
            "sources": list(profile_scope["sources"]),
            "candidates": list(profile_scope["candidates"]),
            "claim_scope_id": profile_scope["claim_scope_id"],
            "workload_ref": _copy_profile_ref(profile_scope["workload_ref"]),
        },
        "comparison_terminal": {
            "state": "PROVED",
            "terminal_id": governing["comparison_terminal"]["terminal_id"],
            "resolution_evidence_ref": copy.deepcopy(t5_ref),
            "output_contract_ref": copy.deepcopy(t5_ref),
            "boundary_adjudication_ref": boundary_ref,
        },
        "upstream_freeze": {
            "state": "PROVED",
            "resolution_evidence_ref": copy.deepcopy(hq_ref),
            "candidate_neutral_work_frozen": True,
            "semantic_authority_closure_ref": closure_ref,
            "producer_outputs": [copy.deepcopy(t2_ref), copy.deepcopy(t5_ref), copy.deepcopy(hq_ref)],
        },
        "function_chains": chains,
        "abc_invariants": [{
            "invariant_id": "INV001",
            "state": "PROVED",
            "logical_property": "Exact governed terminal semantics/replay/output identity and typed-state law remain candidate-neutral across A/B/C.",
            "must_match_across_abc": True,
            "physical_difference_allowed": True,
            "resolution_evidence_ref": copy.deepcopy(t5_ref),
            "authority_ref": copy.deepcopy(closure_ref),
            "proof_ref": copy.deepcopy(hq_ref),
        }],
        "source_candidate_capabilities": capabilities,
        "parity_oracle": {
            "state": "PROVED",
            "resolution_evidence_ref": copy.deepcopy(hq_ref),
            "frozen_before_candidate_output": True,
            "candidate_output_used_to_construct_expected_truth": False,
            "oracle_contract_ref": oracle_ref,
            "oracle_material_ref": copy.deepcopy(t2_ref),
            "fixed_frontier_ref": copy.deepcopy(t2_ref),
            "negative_state_expectation_ref": copy.deepcopy(t5_ref),
        },
        "accounting_contract": {
            "state": "PROVED",
            "resolution_evidence_ref": copy.deepcopy(hq_ref),
            "semantic_owner_cost_owner_separated": True,
            "constitution_ref": accounting_ref,
            "candidate_start_stop_ref": envelope_ref,
            "preserved_work_treatment_ref": accounting_ref,
            "candidate_process_isolation_ref": envelope_ref,
            "metrics": [{
                "metric_id": "CURRENT_FIABC_T4_CANDIDATE_LOCAL_METRIC_REGISTRY",
                "definition_ref": telemetry_ref,
                "candidate_local": True,
                "accumulation_semantics": "TOTAL_OVER_CANDIDATE_BOUNDARY",
                "measurement_kind": "OBSERVED",
                "overwritten_before_terminal": False,
                "method_identity_across_candidates": "FIABC_T4_CURRENT_TELEMETRY_REGISTRY@1",
            }],
        },
        "preflight_evaluation": {
            "contract_id": PREFLIGHT_CONTRACT_ID,
            "status": "BLOCK",
            "checks": [{
                "check_id": "UNEVALUATED",
                "status": "BLOCK",
                "failure_code": "PF_UNEVALUATED",
                "evidence_refs": [],
            }],
            "evaluated_manifest_sha256": "0" * 64,
        },
    }
    return seal_manifest(manifest)


def build_lifecycle_context(
    *,
    repo_root: Path,
    head: str,
    t2: Mapping[str, Any],
    t5: Mapping[str, Any],
) -> dict[str, Any]:
    cells = _assert_current_manifest_law(t2, t5)
    by_cell = {(cell["source"], cell["candidate"]): cell for cell in t2["cells"]}
    t2_ref = current_ref(repo_root, head, T2_PATH, "COURT_ADJUDICATION", "current six-cell execution manifest")
    t5_ref = current_ref(repo_root, head, T5_PATH, "COURT_ADJUDICATION", "current six-cell court contract")
    driver_ref = current_ref(
        repo_root, head, "rawlsing_next/ee_p2x_darwin_court_driver.py",
        "CURRENT_IMPLEMENTATION", "current failure-scope and lifecycle orchestrator",
    )
    backend_ref = current_ref(
        repo_root, head, "rawlsing_next/ee_p2x_process_isolated_backend.py",
        "CURRENT_IMPLEMENTATION", "current source-candidate process isolation adapter",
    )
    hq_ref = current_ref(
        repo_root, head, FINAL_HQ_PATH, "GOVERNED_EXECUTION_RECEIPT",
        "accepted final source-independent HQ preflight/fan-in return",
    )
    return {
        "schema": LIFECYCLE_SCHEMA,
        "state": "PROVED",
        "generated_from_commit_sha": head,
        "frozen_before_candidate_execution": True,
        "failure_scope_ambiguous": False,
        "failure_scope_misclassified": False,
        "lifecycle_order_matches": True,
        "terminal_history_fresh_for_retry": True,
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "ranking_or_selection": False,
        "cell_order": [{"source": source, "candidate": candidate} for source, candidate in cells],
        "stage_catalog": list(t2.get("stage_catalog", ())),
        "candidate_local_failure_scope": {
            "law": "ONLY_CURRENT_CELL_IS_FAILED__LATER_LAWFUL_CELLS_REMAIN_REACHABLE",
            "next_by_cell": {
                f"{source}/{candidate}": by_cell[(source, candidate)]["candidate_local_failure_next"]
                for source, candidate in cells
            },
        },
        "common_source_failure_scope": {
            "law": "BLOCK_REMAINING_GOVERNED_STAGES_OF_CURRENT_SOURCE__THEN_ADVANCE_TO_NEXT_SOURCE_OR_FINAL_COURT_GATE",
            "terminal_disposition": "BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
        },
        "common_court_failure_scope": {
            "law": "BLOCK_COURT_UNTIL_RESUME",
            "terminal_disposition": "BLOCKED_BY_COMMON_COURT_AUTHORITY",
        },
        "candidate_b_no_cache": {
            "stop_law_ref": "PURE_B_NO_CACHE",
            "stop_law": t2["stop_laws"]["PURE_B_NO_CACHE"],
            "stages": ["S12_STALE_CACHE_OR_PERSISTENT_STATE", "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE"],
        },
        "wvs7_c_zero_accelerator_no_cache": {
            "stop_law_ref": "C_ZERO_ACCELERATOR_NO_CACHE",
            "stop_law": t2["stop_laws"]["C_ZERO_ACCELERATOR_NO_CACHE"],
            "stages": ["S12_STALE_CACHE_OR_PERSISTENT_STATE", "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE"],
        },
        "lits_a_s01": {
            "stage": "LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD",
            "manifest_tuple": copy.deepcopy(by_cell[("LITS_I", "A")]["stages"]["S01_CANDIDATE_PREPARATION_BUILD"]),
            "classification": "MEASURED_CURRENT_WORK__NOT_HISTORICAL_PRESERVATION",
        },
        "evidence_refs": [t2_ref, t5_ref, driver_ref, backend_ref, hq_ref],
    }


def assert_exact_head_binding(
    manifest: Mapping[str, Any],
    lifecycle_context: Mapping[str, Any],
    *,
    actual_head: str,
    expected_head: str | None = None,
) -> None:
    if expected_head is not None:
        if not _RE_SHA40.fullmatch(expected_head):
            raise SuccessionProducerError("--expected-head must be a full 40-hex commit SHA")
        if expected_head != actual_head:
            raise SuccessionProducerError(
                f"checked-out HEAD {actual_head} does not equal expected head {expected_head}"
            )
    identity = manifest.get("manifest_identity", {})
    if identity.get("generated_from_commit_sha") != actual_head or identity.get("generated_from_ref") != actual_head:
        raise SuccessionProducerError("succession manifest is stale or not bound to checked-out HEAD")
    head_bindings = manifest.get("current_head_bindings")
    if not isinstance(head_bindings, Mapping) or head_bindings.get("generated_from_commit_sha") != actual_head:
        raise SuccessionProducerError("current-head execution provenance is stale or not bound to checked-out HEAD")
    required_files = head_bindings.get("required_files")
    if not isinstance(required_files, Mapping):
        raise SuccessionProducerError("current-head execution provenance required_files is missing")
    for path in CURRENT_EXECUTION_PROVENANCE_PATHS:
        ref = required_files.get(path)
        if (
            not isinstance(ref, Mapping)
            or ref.get("path") != path
            or ref.get("ref") != actual_head
            or ref.get("resolved_commit_sha") != actual_head
            or ref.get("evidence_class") != "CURRENT_IMPLEMENTATION"
            or not isinstance(ref.get("git_blob_sha"), str)
            or not _RE_SHA40.fullmatch(ref["git_blob_sha"])
            or not isinstance(ref.get("content_sha256"), str)
            or not _RE_SHA64.fullmatch(ref["content_sha256"])
        ):
            raise SuccessionProducerError(
                f"current-head execution provenance binding is not exact for {path}"
            )
    if lifecycle_context.get("generated_from_commit_sha") != actual_head:
        raise SuccessionProducerError("P10 lifecycle context is stale or not bound to checked-out HEAD")
    if identity.get("frozen_before_candidate_execution") is not True:
        raise SuccessionProducerError("succession manifest is not pre-candidate frozen")
    if lifecycle_context.get("frozen_before_candidate_execution") is not True:
        raise SuccessionProducerError("P10 lifecycle context is not pre-candidate frozen")


def assert_zero_candidate_state(lifecycle_context: Mapping[str, Any]) -> None:
    if lifecycle_context.get("candidate_processes_started") != 0:
        raise SuccessionProducerError("pre-candidate succession producer observed nonzero candidate processes")
    if lifecycle_context.get("candidate_outputs_seen") != 0:
        raise SuccessionProducerError("pre-candidate succession producer observed nonzero candidate outputs")
    if lifecycle_context.get("candidate_owned_roots_consulted") != []:
        raise SuccessionProducerError("pre-candidate succession producer consulted candidate-owned roots")
    if lifecycle_context.get("ranking_or_selection") is not False:
        raise SuccessionProducerError("succession producer may not rank or select candidates")


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()


def _atomic_write_json(path: Path, value: Mapping[str, Any]) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()
    return hashlib.sha256(data).hexdigest()


def produce(
    *,
    repo_root: Path,
    manifest_output: Path,
    lifecycle_output: Path,
    receipt_output: Path | None = None,
    expected_head: str | None = None,
    require_clean: bool = True,
) -> dict[str, Any]:
    repo_root = repo_root.resolve()
    if require_clean:
        require_clean_worktree(repo_root)
    head = checked_out_head(repo_root)
    if expected_head is not None and expected_head != head:
        raise SuccessionProducerError(
            f"checked-out HEAD {head} does not equal expected head {expected_head}"
        )

    # Fail before producing anything if a current owner/binding required by
    # succession law is not present at this exact HEAD, and retain the exact
    # Git-object/content identities in the producer receipt.
    prerequisite_refs = {
        required_path: current_ref(
            repo_root, head, required_path, "CURRENT_IMPLEMENTATION",
            "current-head producer prerequisite",
        )
        for required_path in CURRENT_REQUIRED_PATHS
    }
    for path, ref in prerequisite_refs.items():
        if (
            ref.get("ref") != head
            or ref.get("resolved_commit_sha") != head
            or not isinstance(ref.get("git_blob_sha"), str)
            or not _RE_SHA40.fullmatch(ref["git_blob_sha"])
            or not isinstance(ref.get("content_sha256"), str)
            or not _RE_SHA64.fullmatch(ref["content_sha256"])
        ):
            raise SuccessionProducerError(
                f"current-head required-file identity is not exact for {path}"
            )

    t2 = _json_file(repo_root, T2_PATH)
    t5 = _json_file(repo_root, T5_PATH)
    manifest = build_manifest(
        repo_root=repo_root,
        head=head,
        t2=t2,
        t5=t5,
        current_execution_provenance_refs={
            path: prerequisite_refs[path] for path in CURRENT_EXECUTION_PROVENANCE_PATHS
        },
    )
    lifecycle = build_lifecycle_context(repo_root=repo_root, head=head, t2=t2, t5=t5)
    assert_exact_head_binding(
        manifest, lifecycle, actual_head=head, expected_head=expected_head
    )
    assert_zero_candidate_state(lifecycle)

    resolver = GitEvidenceResolver(repo_root)
    result = evaluate_manifest(
        manifest,
        resolver=resolver,
        lifecycle_context=lifecycle,
    )
    if result.status != "PASS":
        raise SuccessionProducerError(
            "existing succession evaluator BLOCKED produced current-head inputs: "
            + ",".join(result.failure_codes)
        )

    manifest["preflight_evaluation"] = result.as_dict()
    if compute_manifest_digest(manifest) != result.evaluated_manifest_sha256:
        raise SuccessionProducerError("embedding evaluator PASS changed succession manifest identity")
    result2 = evaluate_manifest(
        manifest,
        resolver=resolver,
        lifecycle_context=lifecycle,
    )
    if result2.status != "PASS" or result2.evaluated_manifest_sha256 != result.evaluated_manifest_sha256:
        raise SuccessionProducerError("embedded-evaluation succession manifest does not re-evaluate to PASS")

    manifest_file_sha = _atomic_write_json(manifest_output, manifest)
    lifecycle_file_sha = _atomic_write_json(lifecycle_output, lifecycle)
    receipt = {
        "schema": RECEIPT_SCHEMA,
        "producer_schema": PRODUCER_SCHEMA,
        "status": "PASS",
        "repo": "maidiu/rawlsing",
        "generated_from_commit_sha": head,
        "expected_head": expected_head,
        "clean_worktree_required": require_clean,
        "manifest_output": str(manifest_output),
        "manifest_file_sha256": manifest_file_sha,
        "manifest_content_identity": result2.evaluated_manifest_sha256,
        "lifecycle_output": str(lifecycle_output),
        "lifecycle_file_sha256": lifecycle_file_sha,
        "lifecycle_content_identity": _canonical_sha256(lifecycle),
        "evaluator_contract": PREFLIGHT_CONTRACT_ID,
        "evaluator_status": result2.status,
        "evaluator_failure_codes": list(result2.failure_codes),
        "candidate_processes_started": 0,
        "candidate_outputs_seen": 0,
        "candidate_owned_roots_consulted": [],
        "ranking_or_selection": False,
        "cell_order": lifecycle["cell_order"],
        "lits_a_s01_classification": lifecycle["lits_a_s01"]["classification"],
        "candidate_b_no_cache_ref": lifecycle["candidate_b_no_cache"]["stop_law_ref"],
        "wvs7_c_zero_accelerator_ref": lifecycle["wvs7_c_zero_accelerator_no_cache"]["stop_law_ref"],
        "current_head_bindings": {
            "generated_from_commit_sha": head,
            "t2_manifest_sha256": hashlib.sha256((repo_root / T2_PATH).read_bytes()).hexdigest(),
            "t5_contract_sha256": hashlib.sha256((repo_root / T5_PATH).read_bytes()).hexdigest(),
            "final_hq_return_sha256": hashlib.sha256((repo_root / FINAL_HQ_PATH).read_bytes()).hexdigest(),
            "required_files": {
                path: {
                    "resolved_commit_sha": ref["resolved_commit_sha"],
                    "git_blob_sha": ref["git_blob_sha"],
                    "content_sha256": ref["content_sha256"],
                }
                for path, ref in sorted(prerequisite_refs.items())
            },
        },
    }
    if receipt_output is not None:
        _atomic_write_json(receipt_output, receipt)
    return receipt


def _main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Produce exact-current-head FIABC I07 succession manifest and P10 lifecycle context"
    )
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--manifest-output", type=Path, required=True)
    parser.add_argument("--lifecycle-output", type=Path, required=True)
    parser.add_argument("--receipt-output", type=Path)
    parser.add_argument("--expected-head")
    args = parser.parse_args(argv)

    receipt = produce(
        repo_root=args.repo_root,
        manifest_output=args.manifest_output,
        lifecycle_output=args.lifecycle_output,
        receipt_output=args.receipt_output,
        expected_head=args.expected_head,
        require_clean=True,
    )
    print(json.dumps(receipt, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())
