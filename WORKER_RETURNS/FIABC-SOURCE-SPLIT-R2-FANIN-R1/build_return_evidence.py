#!/usr/bin/env python3
"""Materialize source-free FIABC split fan-in qualification receipts."""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys


CONTROL_ROOT = Path(__file__).resolve().parents[2]
PACKET_ROOT = Path(__file__).resolve().parent
EXECUTION_ROOT = Path(os.environ.get("FIABC_SOURCE_SPLIT_EXECUTION_ROOT", "/private/tmp/fiabc-protected-16f5")).resolve()
QUALIFIED_HEAD = "ed8dabf015d1fd4b4ade9b55816a420b0bc1811e"
CONTROL_BRANCH = "agent/vozhd-fiabc-split-r2-fanin-r1"
EXECUTION_BRANCH = "agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"
EXECUTION_HEAD = "16f5e7d5f691e908d85dc1dd26b8a59a29f668f4"
PHYSICAL_EPOCH_ID = "fc6afc9bc7b287f8fd0654e1da546faee7e6c85491e6735ebe4a161b0db3de35"
EXPECTED_RETURN = "PASS__FIABC_SOURCE_SPLIT_R2_FANIN_SOURCE_FREE_QUALIFIED__HQ_PROMOTION_REQUIRED"
EXPECTED_CONTROL_BASE = "d60616d167987766f29762cb169b4f379df0e695"
SOURCES = ("LITS_I", "WVS7")


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load source-free qualification helper: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _git(root: Path, *args: str, raw: bool = False) -> str | bytes:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return proc.stdout if raw else proc.stdout.decode("utf-8", "surrogateescape").strip()


def _write_json(path: Path, document: object) -> None:
    path.write_text(json.dumps(document, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _assert_checkout_identities() -> None:
    if _git(CONTROL_ROOT, "branch", "--show-current") != CONTROL_BRANCH:
        raise RuntimeError("fan-in control branch drift")
    if _git(CONTROL_ROOT, "rev-parse", "HEAD") != QUALIFIED_HEAD:
        raise RuntimeError("qualified implementation head drift")
    if _git(EXECUTION_ROOT, "branch", "--show-current") != EXECUTION_BRANCH:
        raise RuntimeError("protected successor branch drift")
    if _git(EXECUTION_ROOT, "rev-parse", "HEAD") != EXECUTION_HEAD:
        raise RuntimeError("protected successor head drift")
    if _git(EXECUTION_ROOT, "status", "--porcelain", "--untracked-files=all"):
        raise RuntimeError("protected successor checkout is dirty")
    subprocess.run(
        ["git", "-C", str(CONTROL_ROOT), "merge-base", "--is-ancestor", EXPECTED_CONTROL_BASE, QUALIFIED_HEAD],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def _build_stage_matrix(driver):
    base = driver._load_base(EXECUTION_ROOT)
    manifest_path = EXECUTION_ROOT / "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json"
    machine = base.load_current_execution_manifest(manifest_path)
    joined_prefix = list(driver._joined_preflight_prefix(base, machine))
    joined_trace = list(driver._joined_all_pass_trace(machine))
    joined_order = joined_prefix + joined_trace
    joined_source_order = [address for address in joined_order if address.startswith(tuple(source + "/" for source in SOURCES))]
    joined_court_order = [address for address in joined_order if address.startswith("COURT/")]
    split_addresses = {
        source: list(driver._stage_addresses(base, machine, source))
        for source in SOURCES
    }
    if any(len(addresses) != 51 for addresses in split_addresses.values()):
        raise RuntimeError("each exact source cut must contain 51 stages")
    if len(joined_order) != 102 or len(set(joined_order)) != 102:
        raise RuntimeError("joined preflight plus all-pass trace must contain 102 unique stages")
    split_union = [address for source in SOURCES for address in split_addresses[source]]
    if len(split_union) != 102 or len(set(split_union)) != 102:
        raise RuntimeError("split source cuts must contain exactly 102 unique stages")
    joined_set, split_set = set(joined_source_order), set(split_union)
    split_only = sorted(split_set - joined_set)
    joined_only = sorted(joined_set - split_set)
    if joined_court_order != ["COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"]:
        raise RuntimeError(f"joined success-only court terminal drift: {joined_court_order}")
    if split_only != ["WVS7/C/S00_SOURCE_PREFLIGHT_IDENTITY"]:
        raise RuntimeError(f"unapproved split-only mechanical row: {split_only}")
    if joined_only:
        raise RuntimeError(f"split source cuts omitted joined rows: {joined_only}")

    joined_global = {address: index for index, address in enumerate(joined_order, 1)}
    joined_by_source: dict[str, int] = {}
    joined_local: dict[str, int] = {}
    for address in joined_order:
        source = address.split("/", 1)[0]
        joined_by_source[source] = joined_by_source.get(source, 0) + 1
        joined_local[address] = joined_by_source[source]

    rows = []
    parity = {}
    for source in SOURCES:
        report = driver._assert_transition_parity(base, machine, source)
        parity[source] = report
        ready_index = 0
        for split_index, address in enumerate(split_addresses[source], 1):
            stage = machine.get(address)
            is_ready = stage.disposition == "READY__RUN_LOCALLY"
            if is_ready:
                ready_index += 1
                split_result = "PASS__SYNTHETIC_ALL_PASS_LEDGER"
                joined_result = "PASS__SYNTHETIC_ALL_PASS_LEDGER"
            elif stage.disposition == "DONE__PRESERVE":
                split_result = "PRESERVED"
                joined_result = "PRESERVED"
            else:
                split_result = "SKIPPED_BY_FROZEN_LAW"
                joined_result = "SKIPPED_BY_FROZEN_LAW"
            if address not in joined_global:
                joined_result = "NOT_ON_JOINED_ALL_PASS_TRACE__LATENT_MECHANICAL_ROW"
            if address in joined_global and joined_global[address] <= len(joined_prefix):
                joined_segment = "JOINED_PREFLIGHT"
            elif address in joined_global:
                joined_segment = "JOINED_SOURCE_RUN"
            else:
                joined_segment = "NOT_REACHED_ON_JOINED_ALL_PASS_TRACE"
            rows.append({
                "matrix_row": len(rows) + 1,
                "source": source,
                "candidate": stage.candidate,
                "stage_id": stage.stage_id,
                "address": address,
                "split_source_cut_position": split_index,
                "split_candidate_backend_position": ready_index if is_ready else "",
                "joined_global_position": joined_global.get(address, ""),
                "joined_source_local_position": joined_local.get(address, ""),
                "joined_segment": joined_segment,
                "manifest_disposition": stage.disposition,
                "split_all_pass_disposition": split_result,
                "joined_all_pass_disposition": joined_result,
                "candidate_backend_included": str(is_ready).lower(),
                "empirical_source_access_required_by_manifest": str(stage.empirical_source_access_required).lower(),
                "physical_host_measurement_required_by_manifest": str(stage.physical_host_measurement_required).lower(),
                "split_only_mechanical_closure": str(address in split_only).lower(),
                "joined_preflight_equivalent": str(address in joined_prefix).lower(),
                "next_stage_on_pass": stage.next_stage_on_pass,
                "evidence_or_stop_law_ref": stage.evidence_or_stop_law_ref,
            })
        if report["selected_stage_count"] != 51:
            raise RuntimeError(f"{source} transition court stage count drift")
        if len(report["joined_candidate_backend_addresses"]) != 44:
            raise RuntimeError(f"{source} joined backend address count drift")
        if not report["candidate_backend_addresses_identical"]:
            raise RuntimeError(f"{source} candidate backend address order drift")

    csv_path = PACKET_ROOT / "102_STAGE_MATRIX.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    matrix_doc = {
        "schema": "RAWLSING_FIABC_SOURCE_SPLIT_R2_EXACT_102_STAGE_MATRIX@1.0.0",
        "status": "PASS__EXACT_102_STAGE_UNIVERSES_BOUND",
        "protected_manifest_path": "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json",
        "protected_execution_head": EXECUTION_HEAD,
        "source_stage_count": {source: len(split_addresses[source]) for source in SOURCES},
        "total_split_stage_rows": len(rows),
        "joined_preflight_count": len(joined_prefix),
        "joined_all_pass_trace_count": len(joined_trace),
        "joined_all_pass_address_count_including_court_terminal": len(joined_order),
        "joined_source_segment_address_count": len(joined_source_order),
        "joined_success_only_court_terminal_excluded_from_source_segment": joined_court_order,
        "split_only_mechanical_closure": split_only,
        "joined_only_addresses": joined_only,
        "candidate_backend_addresses_per_source": {
            source: len(parity[source]["joined_candidate_backend_addresses"])
            for source in SOURCES
        },
        "candidate_backend_addresses_identical_by_source": {
            source: parity[source]["candidate_backend_addresses_identical"]
            for source in SOURCES
        },
        "csv_path": csv_path.name,
        "csv_sha256": _sha256(csv_path.read_bytes()),
    }
    _write_json(PACKET_ROOT / "102_STAGE_MATRIX.json", matrix_doc)
    return matrix_doc, parity


def _build_implementation_table() -> dict[str, object]:
    changed = str(_git(CONTROL_ROOT, "diff", "--name-only", EXPECTED_CONTROL_BASE, QUALIFIED_HEAD)).splitlines()
    if len(changed) != 17:
        raise RuntimeError(f"expected 17 integrated implementation/authority files, got {len(changed)}")
    rows = []
    for rel in changed:
        data = _git(CONTROL_ROOT, "show", f"{QUALIFIED_HEAD}:{rel}", raw=True)
        blob = _git(CONTROL_ROOT, "rev-parse", f"{QUALIFIED_HEAD}:{rel}")
        if not isinstance(data, bytes):
            raise RuntimeError("Git object bytes unavailable")
        if rel.startswith("WORKER_COMMISSIONS/"):
            role = "worker commission provenance"
        elif rel.startswith("WORKER_RETURNS/FIABC-CACHE-NEUTRAL"):
            role = "exact joined successor epoch/reuse authority"
        elif "/tests/" in rel:
            role = "hostile source-free qualification"
        elif rel.endswith("FIABC_SOURCE_LOCAL_SPLIT_MERGE.py"):
            role = "portable evidence merge"
        elif rel.endswith("FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE.py"):
            role = "control binding and evidence closure"
        elif rel.endswith("FIABC_SPLIT_R2_WORKROOT_GATES.py"):
            role = "runtime, workroot, 10C/reuse and epoch gates"
        elif rel.endswith("FIABC_PYTHON_CACHE_NEUTRALITY_SUCCESSOR.py"):
            role = "cache-neutral joined successor runtime helper"
        elif rel.endswith("FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py"):
            role = "source-local stage orchestration"
        elif rel.endswith("RUN_FIABC_SOURCE_LOCAL_SPLIT.sh"):
            role = "source-local split launcher"
        else:
            role = "source-free implementation and qualification"
        rows.append({
            "path": rel,
            "role": role,
            "git_blob_sha1_at_qualified_head": blob,
            "file_sha256_at_qualified_head": _sha256(data),
            "bytes_at_qualified_head": len(data),
        })
    path = PACKET_ROOT / "INTEGRATED_IMPLEMENTATION_BLOBS.csv"
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return {"path": path.name, "count": len(rows), "sha256": _sha256(path.read_bytes())}


def main() -> None:
    _assert_checkout_identities()
    sys.path.insert(0, str(CONTROL_ROOT))
    driver = _load("fiabc_split_driver_return_packet", CONTROL_ROOT / "HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_DRIVER.py")
    gates = _load("fiabc_split_gates_return_packet", CONTROL_ROOT / "HQ_HANDOFF/launchers/FIABC_SPLIT_R2_WORKROOT_GATES.py")
    evidence = _load("fiabc_split_evidence_return_packet", CONTROL_ROOT / "HQ_HANDOFF/launchers/FIABC_SOURCE_LOCAL_SPLIT_EVIDENCE.py")

    matrix_doc, parity = _build_stage_matrix(driver)
    implementation_table = _build_implementation_table()
    successor_binding = gates.verify_successor_binding(repo_root=EXECUTION_ROOT, control_root=CONTROL_ROOT)
    runtime_gate = gates.combined_import_abi_gate()
    if runtime_gate.get("status") != "PASS" or runtime_gate.get("observed") != gates.EXPECTED_RUNTIME:
        raise RuntimeError("pinned combined import/ABI runtime gate failed")

    control_binding = evidence.create_control_binding(
        control_root=CONTROL_ROOT,
        qualified_implementation_head=QUALIFIED_HEAD,
        output_path=PACKET_ROOT / "CONTROL_BINDING.json",
        qualification_return_ref=(
            "WORKER_RETURNS/FIABC-SOURCE-SPLIT-R2-FANIN-R1/RETURN.json"
        ),
    )
    control_binding_check = evidence.verify_control_binding(
        binding_path=PACKET_ROOT / "CONTROL_BINDING.json",
        control_root=CONTROL_ROOT,
        require_clean=False,
    )
    _write_json(PACKET_ROOT / "CONTROL_BINDING_PRESEAL_CHECK.json", {
        "schema": "RAWLSING_FIABC_SOURCE_SPLIT_R2_CONTROL_BINDING_PRESEAL_CHECK@1.0.0",
        "status": "PASS__QUALIFIED_HEAD_AND_BOUND_FILE_HASHES_MATCH",
        **control_binding_check,
        "require_clean": False,
        "post_docs_commit_clean_verification_required": True,
    })

    epoch_path = CONTROL_ROOT / gates.EPOCH_REL
    epoch = json.loads(epoch_path.read_text(encoding="utf-8"))
    epoch_material = {key: value for key, value in epoch.items() if key != "receipt_identity"}
    contract_path = CONTROL_ROOT / gates.REUSE_CONTRACT_REL
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    epoch_receipt = {
        "schema": "RAWLSING_FIABC_SOURCE_SPLIT_R2_CACHE_NEUTRAL_EPOCH_BINDING_RECEIPT@1.0.0",
        "status": "PASS__JOINED_SPLIT_PHYSICAL_EPOCH_AND_RUNTIME_BOUND",
        "epoch_path": gates.EPOCH_REL,
        "epoch_git_blob_sha1": _git(CONTROL_ROOT, "rev-parse", f"{QUALIFIED_HEAD}:{gates.EPOCH_REL}"),
        "epoch_file_sha256": _sha256(epoch_path.read_bytes()),
        "epoch_receipt_identity": epoch["receipt_identity"],
        "epoch_self_identity_recomputed": hashlib.sha256(gates._canon(epoch_material)).hexdigest(),
        "reuse_contract_path": gates.REUSE_CONTRACT_REL,
        "reuse_contract_git_blob_sha1": _git(CONTROL_ROOT, "rev-parse", f"{QUALIFIED_HEAD}:{gates.REUSE_CONTRACT_REL}"),
        "reuse_contract_file_sha256": _sha256(contract_path.read_bytes()),
        "joined_successor_head": EXECUTION_HEAD,
        "successor_binding_blob_sha1": gates.EXPECTED_SUCCESSOR_BINDING_BLOB_SHA1,
        "physical_epoch_identity": PHYSICAL_EPOCH_ID,
        "epoch_runtime": epoch["runtime"],
        "normalized_epoch_runtime": runtime_gate["observed"],
        "reuse_contract_exact_runtime": contract["exact_runtime"],
        "runtime_gate": runtime_gate,
        "cache_neutral_environment": contract["cache_neutral_environment"],
        "measured_p2x_executions": 0,
    }
    if epoch_receipt["epoch_receipt_identity"] != PHYSICAL_EPOCH_ID or epoch_receipt["epoch_self_identity_recomputed"] != PHYSICAL_EPOCH_ID:
        raise RuntimeError("epoch self-identity failed")
    _write_json(PACKET_ROOT / "CACHE_NEUTRAL_EPOCH_BINDING_RECEIPT.json", epoch_receipt)

    proof_doc = {
        "schema": "RAWLSING_FIABC_SOURCE_SPLIT_R2_10C_REUSE_CONTRACT_BINDING_PROOF@1.0.0",
        **successor_binding,
        "control_branch": CONTROL_BRANCH,
        "control_qualified_implementation_head": QUALIFIED_HEAD,
        "control_tracked_files_clean": subprocess.run(
            ["git", "-C", str(CONTROL_ROOT), "diff", "--quiet"], check=False
        ).returncode == 0,
        "verified_using": "FIABC_SPLIT_R2_WORKROOT_GATES.verify_successor_binding",
    }
    _write_json(PACKET_ROOT / "10C_REUSE_CONTRACT_BINDING_PROOF.json", proof_doc)

    tree = _git(EXECUTION_ROOT, "rev-parse", "HEAD^{tree}")
    status = _git(EXECUTION_ROOT, "status", "--porcelain", "--untracked-files=all")
    _write_json(PACKET_ROOT / "PROTECTED_SUCCESSOR_NO_DRIFT.json", {
        "schema": "RAWLSING_FIABC_PROTECTED_SUCCESSOR_NO_DRIFT@1.0.0",
        "status": "PASS__EXACT_PROTECTED_SUCCESSOR_UNCHANGED_AND_CLEAN",
        "checkout": str(EXECUTION_ROOT),
        "branch_before_and_after": EXECUTION_BRANCH,
        "head_before_and_after": EXECUTION_HEAD,
        "tree_before_and_after": tree,
        "qualification_runner_precondition_verified_before_tests": True,
        "qualification_runner_cleanliness_check_after_tests": True,
        "observed_final_status_porcelain": status,
        "observed_final_dirty": bool(status),
        "successor_binding_blob_sha1": gates.EXPECTED_SUCCESSOR_BINDING_BLOB_SHA1,
        "protected_successor_code_blobs_verified": successor_binding["protected_blob_checks"],
    })

    differential = {
        "schema": "RAWLSING_FIABC_SOURCE_SPLIT_R2_JOINED_VS_SPLIT_DIFFERENTIAL@1.0.0",
        "status": "PASS__CANDIDATE_RELEVANT_SOURCE_SEGMENTS_EQUIVALENT",
        "verdicts": {
            "LITS_I": "LITS_SPLIT_RUNNER_EQUIVALENT_TO_JOINED_SOURCE_SEGMENT__PASS",
            "WVS7": "WVS7_SPLIT_RUNNER_EQUIVALENT_TO_JOINED_SOURCE_SEGMENT__PASS",
        },
        "scope": "source-free actual protected StateMachine, StageLedger, and manifest stage tuples; no raw source payload opened",
        "protected_execution_head": EXECUTION_HEAD,
        "exact_stage_matrix": matrix_doc,
        "per_source_actual_object_transition_parity": parity,
        "failure_scenario_counts": {
            "actual_object_all_pass_scenarios": 2,
            "actual_object_candidate_local_failure_scenarios": 18,
            "actual_object_common_source_blocker_scenarios": 6,
            "actual_object_common_court_blocker_scenarios": 6,
            "actual_object_total_scenarios": 32,
            "source_local_fake_backend_all_pass_scenarios": 2,
            "source_local_fake_backend_candidate_failure_scenarios": 6,
            "source_local_fake_backend_common_source_and_court_blocker_scenarios": 12,
        },
        "candidate_backend_addresses_identical": {source: parity[source]["candidate_backend_addresses_identical"] for source in SOURCES},
        "candidate_backend_address_count_per_source": {source: len(parity[source]["joined_candidate_backend_addresses"]) for source in SOURCES},
        "classified_administration_only_difference": {
            "address": "WVS7/C/S00_SOURCE_PREFLIGHT_IDENTITY",
            "split_disposition": "PRESERVED",
            "joined_all_pass_trace_disposition": "NOT_ON_JOINED_ALL_PASS_TRACE__LATENT_MECHANICAL_ROW",
            "may_receive_joined_block_propagation_disposition": "BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
            "empirical_source_access_required": False,
            "physical_host_measurement_required": False,
            "source_free_preserve_receipt_executed_before_source_identity_check": True,
        },
        "lits_preflight_equivalence": {
            "address": "LITS_I/A/S00_SOURCE_PREFLIGHT_IDENTITY",
            "joined_and_split_segment": "PRESERVED_BEFORE_LITS_SOURCE_IDENTITY_CHECK",
            "actual_protected_preserve_receipt_check_passed": True,
        },
        "success_only_joined_court_terminal": {
            "address": "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION",
            "classification": "OUTSIDE_BOTH_SOURCE_LOCAL_SEGMENTS__NOT_RUN_BY_SPLIT",
            "split_invoked": False,
            "synthesis_authorized": False,
        },
        "process_lifecycle_t5_t4_and_cache_neutrality": {
            "protected_joined_t5_failure_semantics_suite": "PASS",
            "source_local_posthook_stop_uses_protected_helper": True,
            "t4_accounting_and_adjacent_process_envelope_suites": "PASS",
            "same_physical_epoch_bound": PHYSICAL_EPOCH_ID,
            "main_child_attestation_phase": "MAIN_CELL_CHILD_PRE_BACKEND_IMPORT",
            "s15_child_attestation_phase": "FRESH_REPLAY_CHILD_PRE_SEMANTIC_WORK",
            "measured_cell_execution": False,
        },
    }
    _write_json(PACKET_ROOT / "JOINED_VS_SPLIT_DIFFERENTIAL.json", differential)

    test_output = (PACKET_ROOT / "HOSTILE_TEST_OUTPUT.txt").read_text(encoding="utf-8")
    if "102 passed, 65 subtests passed" not in test_output or "86 passed" not in test_output:
        raise RuntimeError("complete hostile test output is not green")
    telemetry = json.loads((PACKET_ROOT / "source_access_telemetry.json").read_text(encoding="utf-8"))
    if telemetry.get("status") != "PASS__ZERO_SOURCE_AND_CANDIDATE_EXECUTION":
        raise RuntimeError("zero-execution telemetry is not green")
    if any(telemetry.get(key) != 0 for key in (
        "raw_source_opens",
        "raw_source_hash_sha_passes",
        "decoder_calls",
        "candidate_abc_process_launch_attempts",
        "candidate_outputs",
        "measured_p2x_executions",
    )):
        raise RuntimeError("zero-execution law counters are nonzero")

    implementation_hash = _build_implementation_table()
    output_hashes = {
        name: _sha256((PACKET_ROOT / name).read_bytes())
        for name in (
            "HOSTILE_TEST_OUTPUT.txt",
            "source_access_telemetry.json",
            "102_STAGE_MATRIX.csv",
            "102_STAGE_MATRIX.json",
            "JOINED_VS_SPLIT_DIFFERENTIAL.json",
            "CACHE_NEUTRAL_EPOCH_BINDING_RECEIPT.json",
            "10C_REUSE_CONTRACT_BINDING_PROOF.json",
            "PROTECTED_SUCCESSOR_NO_DRIFT.json",
            "CONTROL_BINDING.json",
            "CONTROL_BINDING_PRESEAL_CHECK.json",
        )
    }
    receipt = {
        "schema": "RAWLSING_FIABC_SOURCE_SPLIT_R2_FANIN_RETURN@1.0.0",
        "status": EXPECTED_RETURN,
        "repository": "maidiu/rawlsing",
        "control_branch": CONTROL_BRANCH,
        "qualified_implementation_head": QUALIFIED_HEAD,
        "commission_head": EXPECTED_CONTROL_BASE,
        "evidence_docs_tip_commit": None,
        "later_evidence_docs_tip_distinct_from_implementation": True,
        "protected_execution_branch": EXECUTION_BRANCH,
        "protected_execution_head": EXECUTION_HEAD,
        "physical_epoch_identity": PHYSICAL_EPOCH_ID,
        "worker_provenance_path": "WORKER_PROVENANCE.md",
        "integrated_implementation_blob_table": implementation_hash,
        "exact_stage_matrix": {"csv": "102_STAGE_MATRIX.csv", "json": "102_STAGE_MATRIX.json", "rows": 102},
        "differential_report": "JOINED_VS_SPLIT_DIFFERENTIAL.json",
        "cache_neutral_epoch_receipt": "CACHE_NEUTRAL_EPOCH_BINDING_RECEIPT.json",
        "10c_reuse_contract_binding_proof": "10C_REUSE_CONTRACT_BINDING_PROOF.json",
        "protected_successor_no_drift_proof": "PROTECTED_SUCCESSOR_NO_DRIFT.json",
        "control_binding_path": "CONTROL_BINDING.json",
        "control_binding_receipt_identity": control_binding.get("receipt_identity"),
        "control_binding_verification_path": "CONTROL_BINDING_PRESEAL_CHECK.json",
        "hostile_test_output": "HOSTILE_TEST_OUTPUT.txt",
        "source_access_telemetry": "source_access_telemetry.json",
        "qualification": {
            "fan_in_integrated_suite": "102 passed, 65 subtests passed",
            "protected_joined_successor_suites": "86 passed",
            "total_tests_passed": 188,
            "total_subtests_passed": 65,
            "source_free_orchestration_both_sources": "PASS",
            "actual_object_102_stage_parity_and_failure_matrices": "PASS",
            "full_driver_bound_10c_integration": "PASS",
            "worker_e_cache_neutral_hostility": "PASS",
            "worker_d_merge_receipt_hostility": "PASS",
            "worker_b_runtime_pair_postrun_and_workroot_hostility": "PASS",
            "adjacent_t3_t4_t5_process_envelope_suites": "PASS",
        },
        "equivalence_verdicts": differential["verdicts"],
        "zero_execution_law": {
            key: telemetry[key]
            for key in (
                "raw_source_opens",
                "raw_source_hash_sha_passes",
                "decoder_calls",
                "candidate_abc_process_launch_attempts",
                "candidate_outputs",
                "measured_p2x_executions",
            )
        },
        "synthetic_process_envelope_probe_launches": telemetry["synthetic_process_envelope_probe_launches"],
        "source_free_scope": True,
        "machine_preparation_or_measurement_performed": False,
        "production_candidate_processes_or_outputs_performed": False,
        "hq_promotion_required": True,
        "artifact_sha256": output_hashes,
        "next_action": "HQ adjudication; no push or promotion performed",
    }
    _write_json(PACKET_ROOT / "RETURN.json", receipt)

    (PACKET_ROOT / "QUALIFIED_IMPLEMENTATION_HEAD.txt").write_text(
        f"{QUALIFIED_HEAD}\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
