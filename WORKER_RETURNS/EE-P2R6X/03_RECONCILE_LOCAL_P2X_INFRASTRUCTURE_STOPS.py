#!/usr/bin/env python3
"""Fail-closed local reconciliation for the stopped EE-P2X Darwin court.

This tool is preparation for post-fan-in LOCAL use.  It never opens a source
carrier and never performs empirical work.  It accepts exactly the stopped
ledger adopted by HQ, proves the four infrastructure-misclassified candidate
stops plus the orphan S17 RUNNING state, removes only those ledger entries and
their mechanical stop propagation, and clears only failed-attempt-local backend
state/scratch.

Git-tracked EE-P2X evidence is validation input and is never modified here.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
from typing import Any, Mapping

EXPECTED_LEDGER_SHA256 = "7de7c91d539dd267e31098fd47285b3f4a7873e1c9ec7b542c45cac3908b8671"
LEDGER_SCHEMA = "RAWLSING_EE_P2X_DARWIN_STAGE_LEDGER@1.0.0"
CONTINUATION_MAP_SCHEMA = "RAWLSING_EE_P2X_CONTINUATION_STATE_MACHINE@1.0.0"
CONTINUATION_MAP_SHA256 = "ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422"
CONTINUATION_MAP_GIT_BLOB_SHA1 = "e06e95dd370a4fd44235932088308c3372522ed4"
BACKEND_STATE_SCHEMA = "RAWLSING_EE_P2X_PRODUCTION_BACKEND_STATE@1.0.0"
RECONCILIATION_RECEIPT_SCHEMA = "RAWLSING_EE_P2R6X_P2X_STOP_RECONCILIATION_RECEIPT@1.0.0"
RECONCILIATION_RECEIPT_NAME = "ee_p2r6x_reconciliation_receipt.json"
P2X_RETURN = "WORKER_RETURNS/EE-P2X/00_RETURN.md"
FINAL_VERIFY_RECEIPT = "WORKER_RETURNS/EE-P2X/LOCAL_COURT/91_DRIVER_BOUND_FINAL_VERIFICATION_RECEIPT.json"
S17 = "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"
FIRST_REOPENED_STAGE = "LITS_I/A/S02_C11_REACHABILITY"

STAGE_CATALOG = (
    "S00_SOURCE_PREFLIGHT_IDENTITY",
    "S01_CANDIDATE_PREPARATION_BUILD",
    "S02_C11_REACHABILITY",
    "S03_PARITY_ORACLE_GATE",
    "S04_I03_EXECUTION",
    "S05_I05_LEARNED_PRODUCTION",
    "S06_PROVENANCE_AUDIT",
    "S07_COLD_RESEARCH",
    "S08_WARM_REPEATED_RESEARCH",
    "S09_DELETION_REGEN_OR_A_PERSISTENCE",
    "S10_SOURCE_RELEASE_INVALIDATION",
    "S11_SEMANTIC_AUTHORITY_INVALIDATION",
    "S12_STALE_CACHE_OR_PERSISTENT_STATE",
    "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE",
    "S14_INTERRUPTION_RECOVERY",
    "S15_FRESH_PROCESS_REPLAY",
    "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS",
)

BLOCKERS: tuple[dict[str, str], ...] = (
    {
        "address": "LITS_I/A/S02_C11_REACHABILITY",
        "source": "LITS_I",
        "candidate": "A",
        "stage_id": "S02_C11_REACHABILITY",
        "failure_path": "WORKER_RETURNS/EE-P2X/LOCAL_COURT/failures/LITS_I__A__CANDIDATE_LOCAL_CORRECTNESS_FAILURE.json",
        "exception_type": "ModuleNotFoundError",
        "exception": "No module named 'rawlsing_next.pre553_runtime_authority'",
        "next_stage": "LITS_I/B/S00_SOURCE_PREFLIGHT_IDENTITY",
    },
    {
        "address": "LITS_I/B/S03_PARITY_ORACLE_GATE",
        "source": "LITS_I",
        "candidate": "B",
        "stage_id": "S03_PARITY_ORACLE_GATE",
        "failure_path": "WORKER_RETURNS/EE-P2X/LOCAL_COURT/failures/LITS_I__B__CANDIDATE_LOCAL_CORRECTNESS_FAILURE.json",
        "exception_type": "ModuleNotFoundError",
        "exception": "No module named 'rawlsing_next.pre553_runtime_authority'",
        "next_stage": "LITS_I/C/S00_SOURCE_PREFLIGHT_IDENTITY",
    },
    {
        "address": "WVS7/A/S01_CANDIDATE_PREPARATION_BUILD",
        "source": "WVS7",
        "candidate": "A",
        "stage_id": "S01_CANDIDATE_PREPARATION_BUILD",
        "failure_path": "WORKER_RETURNS/EE-P2X/LOCAL_COURT/failures/WVS7__A__CANDIDATE_LOCAL_CORRECTNESS_FAILURE.json",
        "exception_type": "RecursionError",
        "exception": "maximum recursion depth exceeded in comparison",
        "next_stage": "WVS7/B/S00_SOURCE_PREFLIGHT_IDENTITY",
    },
    {
        "address": "WVS7/B/S01_CANDIDATE_PREPARATION_BUILD",
        "source": "WVS7",
        "candidate": "B",
        "stage_id": "S01_CANDIDATE_PREPARATION_BUILD",
        "failure_path": "WORKER_RETURNS/EE-P2X/LOCAL_COURT/failures/WVS7__B__CANDIDATE_LOCAL_CORRECTNESS_FAILURE.json",
        "exception_type": "RecursionError",
        "exception": "maximum recursion depth exceeded in comparison",
        "next_stage": "WVS7/C/S01_CANDIDATE_PREPARATION_BUILD",
    },
)


class ReconciliationError(RuntimeError):
    pass


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _canonical(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def _render_json(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=False).encode("utf-8") + b"\n"


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ReconciliationError(f"required file absent: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ReconciliationError(f"required JSON malformed: {path}") from exc


def _atomic_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as fh:
            fh.write(data)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def _inside(root: Path, path: Path) -> bool:
    root = root.resolve()
    path = path.resolve()
    return path == root or root in path.parents


def _require_inside(root: Path, path: Path, label: str) -> Path:
    if not _inside(root, path):
        raise ReconciliationError(f"{label} escapes bound root: {path}")
    return path.resolve()


def _ledger_path(work_root: Path) -> Path:
    return work_root / "ee_p2x_stage_ledger.json"


def _receipt_path(work_root: Path) -> Path:
    return work_root / RECONCILIATION_RECEIPT_NAME


def _candidate_root(work_root: Path, source: str, candidate: str) -> Path:
    return work_root / "cells" / source / candidate


def _assert_authority_header(ledger: Mapping[str, Any]) -> None:
    if ledger.get("schema") != LEDGER_SCHEMA:
        raise ReconciliationError("ledger schema drift")
    continuation = ledger.get("continuation_map")
    expected = {
        "schema": CONTINUATION_MAP_SCHEMA,
        "sha256": CONTINUATION_MAP_SHA256,
        "git_blob_sha1": CONTINUATION_MAP_GIT_BLOB_SHA1,
    }
    if continuation != expected:
        raise ReconciliationError("continuation-map identity drift")
    if ledger.get("source_order") != ["LITS_I", "WVS7"]:
        raise ReconciliationError("source order drift")
    if ledger.get("candidate_order") != ["A", "B", "C"]:
        raise ReconciliationError("candidate order drift")
    if not isinstance(ledger.get("source_identities"), Mapping):
        raise ReconciliationError("source identity map missing")
    if not isinstance(ledger.get("stages"), Mapping):
        raise ReconciliationError("stage map missing")


def _entry_receipt(work_root: Path, entry: Mapping[str, Any], address: str) -> tuple[Path, Mapping[str, Any]]:
    rel = entry.get("receipt_path")
    if not isinstance(rel, str) or not rel:
        raise ReconciliationError(f"{address}: terminal receipt path missing")
    path = _require_inside(work_root, work_root / rel, f"{address} receipt")
    if not path.is_file():
        raise ReconciliationError(f"{address}: terminal receipt absent: {path}")
    if _sha256_file(path) != entry.get("receipt_hash"):
        raise ReconciliationError(f"{address}: terminal receipt hash drift")
    doc = _read_json(path)
    if not isinstance(doc, Mapping):
        raise ReconciliationError(f"{address}: terminal receipt is not an object")
    return path, doc


def _validate_repo_failure(repo_root: Path, spec: Mapping[str, str]) -> Mapping[str, Any]:
    path = _require_inside(repo_root, repo_root / spec["failure_path"], "governed failure receipt")
    doc = _read_json(path)
    expected_disposition = (
        f"EE_P2X_{spec['source']}_{spec['candidate']}_{spec['stage_id']}"
        "__CANDIDATE_LOCAL_CORRECTNESS_FAILURE"
    )
    expected = {
        "schema": "RAWLSING_EE_P2X_FAILURE_STOP_RECEIPT@1.0.0",
        "source": spec["source"],
        "candidate": spec["candidate"],
        "kind": "CANDIDATE_LOCAL_CORRECTNESS_FAILURE",
        "blocking_scope": "CANDIDATE_ONLY",
        "disposition": expected_disposition,
    }
    for key, value in expected.items():
        if doc.get(key) != value:
            raise ReconciliationError(f"{spec['address']}: governed failure identity drift at {key}")
    detail = doc.get("backend_detail")
    if not isinstance(detail, Mapping):
        raise ReconciliationError(f"{spec['address']}: governed backend detail missing")
    if detail.get("exception_type") != spec["exception_type"] or detail.get("exception") != spec["exception"]:
        raise ReconciliationError(f"{spec['address']}: governed exception identity drift")
    if doc.get("synthetic_fallback_used") is not False:
        raise ReconciliationError(f"{spec['address']}: governed stop unexpectedly used fallback")
    return doc


def _validate_blocker_entry(
    work_root: Path,
    ledger: Mapping[str, Any],
    spec: Mapping[str, str],
) -> list[str]:
    stages = ledger["stages"]
    address = spec["address"]
    entry = stages.get(address)
    if not isinstance(entry, Mapping):
        raise ReconciliationError(f"{address}: expected blocker entry missing")
    expected_fields = {
        "stage_id": spec["stage_id"],
        "source": spec["source"],
        "candidate": spec["candidate"],
        "state": "TERMINAL",
        "terminal_disposition": "CANDIDATE_LOCAL_FAILURE",
        "verifier_completion": True,
        "next_stage": spec["next_stage"],
    }
    for key, value in expected_fields.items():
        if entry.get(key) != value:
            raise ReconciliationError(f"{address}: blocker ledger identity drift at {key}")
    _, receipt = _entry_receipt(work_root, entry, address)
    if receipt.get("schema") != "RAWLSING_EE_P2X_DARWIN_STAGE_RECEIPT_ENVELOPE@1.0.0":
        raise ReconciliationError(f"{address}: blocker receipt schema drift")
    if receipt.get("stage") != address or receipt.get("terminal_disposition") != "CANDIDATE_LOCAL_FAILURE":
        raise ReconciliationError(f"{address}: blocker receipt identity drift")
    payload = receipt.get("measured_payload")
    detail = payload.get("detail") if isinstance(payload, Mapping) else None
    if not isinstance(detail, Mapping):
        raise ReconciliationError(f"{address}: blocker receipt detail missing")
    if detail.get("exception_type") != spec["exception_type"] or detail.get("exception") != spec["exception"]:
        raise ReconciliationError(f"{address}: blocker local exception identity drift")

    start = STAGE_CATALOG.index(spec["stage_id"]) + 1
    propagated: list[str] = []
    for stage_id in STAGE_CATALOG[start:]:
        later = f"{spec['source']}/{spec['candidate']}/{stage_id}"
        prop = stages.get(later)
        if not isinstance(prop, Mapping):
            raise ReconciliationError(f"{later}: expected candidate-stop propagation missing")
        for key, value in {
            "stage_id": stage_id,
            "source": spec["source"],
            "candidate": spec["candidate"],
            "state": "TERMINAL",
            "terminal_disposition": "CANDIDATE_LOCAL_FAILURE",
            "verifier_completion": True,
            "next_stage": spec["next_stage"],
        }.items():
            if prop.get(key) != value:
                raise ReconciliationError(f"{later}: propagated stop drift at {key}")
        _, prop_receipt = _entry_receipt(work_root, prop, later)
        if prop_receipt.get("schema") != "RAWLSING_EE_P2X_CANDIDATE_LOCAL_STOP_PROPAGATION@1.0.0":
            raise ReconciliationError(f"{later}: propagated stop receipt schema drift")
        if prop_receipt.get("stage") != later or prop_receipt.get("blocker_stage") != address:
            raise ReconciliationError(f"{later}: propagated stop does not link to exact blocker")
        if prop_receipt.get("execution_performed") is not False or prop_receipt.get("measurement_performed") is not False:
            raise ReconciliationError(f"{later}: propagated stop falsely records execution")
        propagated.append(later)
    return propagated


def _validate_s17(work_root: Path, repo_root: Path, ledger: Mapping[str, Any]) -> None:
    entry = ledger["stages"].get(S17)
    if not isinstance(entry, Mapping):
        raise ReconciliationError("orphan S17 RUNNING entry missing")
    expected = {
        "stage_id": "S17_FINAL_COMPLETENESS_AND_VERIFICATION",
        "source": "COURT",
        "candidate": "ALL",
        "state": "RUNNING",
        "terminal_disposition": None,
        "verifier_completion": False,
        "receipt_path": None,
        "receipt_hash": None,
        "next_stage": None,
    }
    for key, value in expected.items():
        if entry.get(key) != value:
            raise ReconciliationError(f"S17 orphan identity drift at {key}")

    final = _read_json(_require_inside(repo_root, repo_root / FINAL_VERIFY_RECEIPT, "final verifier receipt"))
    if final.get("schema") != "RAWLSING_EE_P2X_DRIVER_BOUND_FINAL_VERIFICATION@1.0.0":
        raise ReconciliationError("final verifier receipt schema drift")
    if final.get("driver_ledger_sha256") != EXPECTED_LEDGER_SHA256:
        raise ReconciliationError("final verifier receipt ledger identity drift")
    if final.get("terminal") != "BLOCKER__DRIVER_STAGE_RUNNING__COURT__S17_FINAL_COMPLETENESS_AND_VERIFICATION":
        raise ReconciliationError("final verifier receipt terminal drift")

    return_text = _require_inside(repo_root, repo_root / P2X_RETURN, "governed P2X return").read_text(encoding="utf-8")
    required_text = (
        "driver-bound final verification failed",
        "ValueError: 'COURT/ALL' is not in list",
        "BLOCKER__DRIVER_STAGE_RUNNING__COURT__S17_FINAL_COMPLETENESS_AND_VERIFICATION",
    )
    for fragment in required_text:
        if fragment not in return_text:
            raise ReconciliationError(f"governed P2X return no longer binds S17 defect fragment: {fragment}")


def _validate_backend_state(path: Path, source: str, candidate: str) -> None:
    if not path.exists():
        return
    if path.is_symlink() or not path.is_file():
        raise ReconciliationError(f"backend state path is not a regular file: {path}")
    state = _read_json(path)
    if state.get("schema") != BACKEND_STATE_SCHEMA:
        raise ReconciliationError(f"backend state schema drift: {path}")
    if state.get("source") != source or state.get("candidate") != candidate:
        raise ReconciliationError(f"backend state identity drift: {path}")


def _cleanup_plan(work_root: Path) -> list[dict[str, Any]]:
    cells = [(x["source"], x["candidate"]) for x in BLOCKERS] + [("COURT", "ALL")]
    plan: list[dict[str, Any]] = []
    for source, candidate in cells:
        root = _require_inside(work_root, _candidate_root(work_root, source, candidate), "candidate root")
        if root.exists() and root.is_symlink():
            raise ReconciliationError(f"candidate root may not be symlink: {root}")
        durable = _require_inside(work_root, root / "durable", "durable root")
        scratch = _require_inside(work_root, root / "scratch", "scratch root")
        for p in (durable, scratch):
            if p.exists() and p.is_symlink():
                raise ReconciliationError(f"candidate sub-root may not be symlink: {p}")
        state_path = durable / "ee_p2x_backend_state.json"
        _validate_backend_state(state_path, source, candidate)
        plan.append(
            {
                "source": source,
                "candidate": candidate,
                "state_path": state_path,
                "state_present": state_path.is_file(),
                "scratch_path": scratch,
                "scratch_present": scratch.exists(),
            }
        )
    return plan


def _validate_post_reconciliation_audit(work_root: Path, ledger_bytes: bytes) -> Mapping[str, Any]:
    receipt_path = _receipt_path(work_root)
    receipt = _read_json(receipt_path)
    if receipt.get("schema") != RECONCILIATION_RECEIPT_SCHEMA:
        raise ReconciliationError("audit-only reconciliation receipt schema drift")
    got = _sha256_bytes(ledger_bytes)
    if receipt.get("before_ledger_sha256") != EXPECTED_LEDGER_SHA256:
        raise ReconciliationError("audit-only receipt before-ledger identity drift")
    if receipt.get("after_ledger_sha256") != got:
        raise ReconciliationError("audit-only receipt does not bind current ledger")
    ledger = json.loads(ledger_bytes.decode("utf-8"))
    _assert_authority_header(ledger)
    for address in receipt.get("removed_stage_addresses", ()):
        if address in ledger["stages"]:
            raise ReconciliationError(f"audit-only removed stage reappeared: {address}")
    if receipt.get("next_stage_after_reconciliation") != FIRST_REOPENED_STAGE:
        raise ReconciliationError("audit-only receipt next-stage drift")
    return receipt


def reconcile(work_root: Path, repo_root: Path, *, audit_only: bool = False) -> Mapping[str, Any]:
    work_root = work_root.resolve()
    repo_root = repo_root.resolve()
    ledger_path = _ledger_path(work_root)
    if not ledger_path.is_file():
        raise ReconciliationError(f"ledger absent: {ledger_path}")
    ledger_bytes = ledger_path.read_bytes()
    before_hash = _sha256_bytes(ledger_bytes)

    if before_hash != EXPECTED_LEDGER_SHA256:
        if audit_only and _receipt_path(work_root).is_file():
            receipt = _validate_post_reconciliation_audit(work_root, ledger_bytes)
            return {
                "status": "AUDIT_ONLY__ALREADY_RECONCILED",
                "ledger_sha256": before_hash,
                "receipt": str(_receipt_path(work_root)),
                "removed_stage_count": len(receipt.get("removed_stage_addresses", ())),
            }
        raise ReconciliationError(
            f"pre-reconciliation ledger SHA-256 mismatch: expected {EXPECTED_LEDGER_SHA256}, got {before_hash}"
        )

    ledger = json.loads(ledger_bytes.decode("utf-8"))
    if not isinstance(ledger, Mapping):
        raise ReconciliationError("ledger top level must be object")
    _assert_authority_header(ledger)

    for spec in BLOCKERS:
        _validate_repo_failure(repo_root, spec)

    removed: list[str] = []
    for spec in BLOCKERS:
        propagated = _validate_blocker_entry(work_root, ledger, spec)
        removed.append(spec["address"])
        removed.extend(propagated)

    _validate_s17(work_root, repo_root, ledger)
    removed.append(S17)
    if len(removed) != len(set(removed)):
        raise ReconciliationError("reconciliation removal set contains duplicate addresses")

    c_before = {
        a: copy.deepcopy(e)
        for a, e in ledger["stages"].items()
        if a.startswith("LITS_I/C/") or a.startswith("WVS7/C/")
    }
    source_identities_before = copy.deepcopy(ledger["source_identities"])
    continuation_before = copy.deepcopy(ledger["continuation_map"])
    preserved_before = {
        a: _sha256_bytes(_canonical(e))
        for a, e in ledger["stages"].items()
        if a not in set(removed)
    }

    cleanup = _cleanup_plan(work_root)
    after = copy.deepcopy(ledger)
    for address in removed:
        if address not in after["stages"]:
            raise ReconciliationError(f"planned removed stage vanished during validation: {address}")
        del after["stages"][address]

    if after["source_identities"] != source_identities_before:
        raise ReconciliationError("source identities changed in reconciliation plan")
    if after["continuation_map"] != continuation_before:
        raise ReconciliationError("continuation map changed in reconciliation plan")
    c_after = {
        a: e
        for a, e in after["stages"].items()
        if a.startswith("LITS_I/C/") or a.startswith("WVS7/C/")
    }
    if c_after != c_before:
        raise ReconciliationError("LiTS-C or WVS-C changed in reconciliation plan")
    for address, before_identity in preserved_before.items():
        if address not in after["stages"]:
            raise ReconciliationError(f"unrelated stage removed: {address}")
        if _sha256_bytes(_canonical(after["stages"][address])) != before_identity:
            raise ReconciliationError(f"unrelated stage mutated: {address}")

    after_bytes = _render_json(after)
    after_hash = _sha256_bytes(after_bytes)
    preserved_addresses = sorted(after["stages"])
    planned_artifacts: list[str] = []
    for item in cleanup:
        if item["state_present"]:
            planned_artifacts.append(str(item["state_path"].relative_to(work_root)))
        if item["scratch_present"]:
            planned_artifacts.append(str(item["scratch_path"].relative_to(work_root)))

    result = {
        "schema": RECONCILIATION_RECEIPT_SCHEMA,
        "status": "AUDIT_ONLY__READY" if audit_only else "RECONCILED",
        "before_ledger_sha256": before_hash,
        "after_ledger_sha256": after_hash,
        "next_stage_after_reconciliation": FIRST_REOPENED_STAGE,
        "removed_stage_addresses": removed,
        "preserved_stage_addresses": preserved_addresses,
        "preserved_lits_c_addresses": sorted(a for a in preserved_addresses if a.startswith("LITS_I/C/")),
        "preserved_wvs_c_addresses": sorted(a for a in preserved_addresses if a.startswith("WVS7/C/")),
        "source_identities_preserved": source_identities_before,
        "continuation_map_preserved": continuation_before,
        "local_artifacts_removed": planned_artifacts,
        "git_evidence_preserved": [x["failure_path"] for x in BLOCKERS] + [FINAL_VERIFY_RECEIPT, P2X_RETURN],
        "source_carrier_access_performed": False,
        "empirical_measurement_performed": False,
        "candidate_roots_deleted": False,
    }

    if audit_only:
        return result

    # Clear only failed-attempt-local mutable state before changing the ledger.
    # Durable transformed carriers and Git evidence are deliberately untouched.
    for item in cleanup:
        state_path: Path = item["state_path"]
        scratch_path: Path = item["scratch_path"]
        if state_path.exists():
            state_path.unlink()
        if scratch_path.exists():
            shutil.rmtree(scratch_path)

    _atomic_bytes(ledger_path, after_bytes)
    if _sha256_file(ledger_path) != after_hash:
        raise ReconciliationError("post-write ledger hash mismatch")
    _atomic_bytes(_receipt_path(work_root), _render_json(result))
    return result


def _parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--work-root", type=Path, required=True)
    p.add_argument("--repo-root", type=Path, default=Path.cwd())
    p.add_argument("--audit-only", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        result = reconcile(args.work_root, args.repo_root, audit_only=args.audit_only)
    except ReconciliationError as exc:
        raise SystemExit(f"EE_P2R6X_BLOCK__{exc}") from exc
    print(json.dumps(result, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
