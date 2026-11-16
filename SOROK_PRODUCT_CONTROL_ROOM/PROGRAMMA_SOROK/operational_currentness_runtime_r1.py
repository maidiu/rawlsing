#!/usr/bin/env python3
"""SOROK automatic operational currentness runtime R1.

Existing-owner-compatible intake and reconciliation over the paired
SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json + .md.  The paired JSON is the
only currentness truth; the Markdown block is derived; the journal is recovery
custody only.  The frozen #1095 operational_currentness_r1 projection is
preserved byte-for-byte and is never rewritten as if it had live intake.

No provider, account, credential, native/science, human/actor or protected
authority is created here.
"""
from __future__ import annotations

import argparse
import copy
import datetime
import fcntl
import hashlib
import hmac
import json
import os
import re
import secrets
import shutil
import ssl
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "SOROK_OPERATIONAL_CURRENTNESS_RUNTIME_R1"
EVENT_SCHEMA = "SOROK_CURRENTNESS_EVENT_R1"
REVIEW_RECEIPT_SCHEMA = "SOROK_CURRENTNESS_REVIEW_RECEIPT@1"
REJECTION_SCHEMA = "SOROK_CURRENTNESS_REJECTION@1"
PROTECTED_INTEGRATION_SCHEMA = "SOROK_CURRENTNESS_PROTECTED_INTEGRATION@1"
RETURN_SCHEMA = "SOROK_CURRENTNESS_WORKER_RETURN@1"
CONFIG_SCHEMA = "SOROK_CURRENTNESS_RUNTIME_CONFIG_R1"
RUNTIME_KEY = "operational_currentness_runtime_r1"
FROZEN_KEY = "operational_currentness_r1"
START = "<!-- SOROK_RUNTIME_CURRENT_START -->"
END = "<!-- SOROK_RUNTIME_CURRENT_END -->"
FROZEN_START = "<!-- SOROK_OPERATIONAL_CURRENT_START -->"
FROZEN_END = "<!-- SOROK_OPERATIONAL_CURRENT_END -->"
HASH_RE = re.compile(r"^[0-9a-f]{40}(?:[0-9a-f]{24})?$")
UUID_RE = re.compile(r"^[0-9a-f-]{36}$")
PACKET_BLOB = "17cfae53f9ca16640d5d3d500aa7dcb3b31cc89c"
GMT_BLOB = "474befcb4d9f6e3842b4d256d00d9c0ac0bf1a4d"
VERIFIER_BLOB = "d971b6ea4af9c45904944c7eaa97f3dfef65f6b9"
GMT_ATLAS_COMMIT = "67698cfd32f838b7a5fdc381b0168d9225f5352f"
GMT_ATLAS_PATH = "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/32_OPERATIONAL_GMT_WORK_DEPENDENCY_AND_RECEIVING_20261115_R1.md"
WORKFLOW_BLOB = "f76c0d90d32e54d26d019b7f77c563b33fd5e97b"
MECHANISM_ID = "AUTOMATIC_CURRENTNESS_R1"
LIVE_GITHUB_SCHEMA = "SOROK_LIVE_GITHUB_OBSERVATION@1"
CAPABILITY_SCHEMA = "SOROK_CURRENTNESS_LOCAL_CAPABILITY@1"
TRUSTED_LAUNCH_SCHEMA = "SOROK_CURRENTNESS_TRUSTED_LAUNCH_REGISTRY@1"
OPERATOR_AUTH_SCHEMA = "SOROK_CURRENTNESS_OPERATOR_AUTHORIZATION@1"
EXPECTED_IDS = [f"{family}{n:02d}" for family, count in (
    ("B", 5), ("C", 5), ("D", 5), ("E", 4), ("F", 4), ("G", 4))
    for n in range(1, count + 1)]
PHASE_ORDER = {phase: index for index, phase in enumerate(
    ("CG-B", "CG-C", "CG-D", "CG-E", "CG-F", "CG-G"))}
ALLOWED_VERDICTS = {
    "ACCEPT_SCOPED_SOURCEFREE", "ACCEPT_SCOPED_SOURCEFREE_C05_ACTOR_PROJECTION",
    "REVISE_EXACT_DEFECT", "REJECTED", "HOLD_SOURCE_AUTHORITY",
    "ACCEPT_SCOPED",
}


class CurrentnessError(Exception):
    def __init__(self, code: str, detail: Any = None) -> None:
        super().__init__(code if detail is None else f"{code}: {detail}")
        self.code = code
        self.detail = detail


def now_utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def command_digest(argv: list[str]) -> str:
    return hashlib.sha256(json.dumps(
        argv, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError) as exc:
        raise CurrentnessError("JSON_UNREADABLE", f"{path}: {exc}") from exc


def write_json_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def write_text_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=path.name + ".", dir=str(path.parent))
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp, path)
        directory = os.open(path.parent, os.O_RDONLY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def _absolute(base: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else (base / path)


def load_config(path: Path) -> dict:
    raw = read_json(path)
    if not isinstance(raw, dict):
        raise CurrentnessError("CONFIG_NOT_OBJECT")
    root = Path(raw.get("repo_root", Path.cwd())).resolve()
    config = dict(raw)
    config["_root"] = root
    config["_pair_json"] = _absolute(root, config["pair_json"]).resolve()
    config["_pair_md"] = _absolute(root, config["pair_md"]).resolve()
    config["_state_root"] = _absolute(root, config.get(
        "state_root", ".local-state/currentness")).resolve()
    frozen = config.get("frozen_source_dir",
                        "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1")
    config["_frozen_dir"] = _absolute(root, frozen).resolve()
    baseline = config.get("github_baseline")
    config["_baseline"] = _absolute(root, baseline).resolve() if baseline else None
    controller = config.get("controller_state_root")
    config["_controller_state_root"] = (
        _absolute(root, controller).resolve() if controller else None)
    operator_auth = config.get("trusted_operator_authorization")
    config["_operator_auth"] = (
        _absolute(root, operator_auth).resolve() if operator_auth else None)
    config["_capability_path"] = config["_state_root"] / "runtime_capability.json"
    config["_trusted_registry_path"] = config["_state_root"] / "trusted_launches.json"
    config["_github_live"] = dict(config.get("github_live") or {})
    config["_github_live"].setdefault(
        "remote", "https://github.com/maidiu/rawlsing.git")
    config["_github_live"].setdefault("api_repo", "maidiu/rawlsing")
    config["_github_live"].setdefault("ttl_seconds", 900)
    config["_github_live"].setdefault("cafile", "/etc/ssl/cert.pem")
    for key in ("_pair_json", "_pair_md"):
        if not config[key].is_file():
            raise CurrentnessError("PAIR_FILE_MISSING", str(config[key]))
    config["_state_root"].mkdir(parents=True, exist_ok=True)
    return config


def _lock(config: dict, exclusive: bool):
    lock_path = config["_state_root"] / "currentness.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open("a+")
    fcntl.flock(handle, fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
    return handle


def _unlock(handle) -> None:
    fcntl.flock(handle, fcntl.LOCK_UN)
    handle.close()


def frozen_contracts(config: dict) -> tuple[dict, dict, dict]:
    packet_path = config["_frozen_dir"] / "original_task_packets_20261112.json"
    gmt_path = config["_frozen_dir"] / "original_gmt_overlay_20261112.json"
    packet_raw = packet_path.read_bytes()
    gmt_raw = gmt_path.read_bytes()
    if git_blob_sha(packet_raw) != PACKET_BLOB:
        raise CurrentnessError("FROZEN_PACKET_BLOB_MISMATCH")
    if git_blob_sha(gmt_raw) != GMT_BLOB:
        raise CurrentnessError("FROZEN_GMT_BLOB_MISMATCH")
    packet = json.loads(packet_raw)
    gmt = json.loads(gmt_raw)
    tasks = packet.get("tasks")
    overlays = gmt.get("task_overlays")
    if not isinstance(tasks, list) or not isinstance(overlays, list):
        raise CurrentnessError("FROZEN_SOURCE_SCHEMA")
    if len(tasks) != 27 or len(overlays) != 27:
        raise CurrentnessError("FROZEN_DENOMINATOR")
    by_task = {row.get("task_id"): row for row in overlays if isinstance(row, dict)}
    if set(by_task) != set(EXPECTED_IDS):
        raise CurrentnessError("FROZEN_GMT_IDS")
    return packet, gmt, by_task


def _initial_execution_state(sourcefree_state: str) -> str:
    return {
        "SCOPED_RECEIVED_UNMERGED": "SCOPED_RECEIVED_UNMERGED",
        "PROTECTED_SOURCEFREE": "PROTECTED_SOURCEFREE",
        "HELD_NOT_LAUNCHED": "HELD_NOT_LAUNCHED",
        "PARTIAL_CANDIDATE": "PARTIAL_CANDIDATE",
        "CANDIDATE": "CANDIDATE_AUTHOR_TESTED",
    }.get(sourcefree_state, "NOT_LAUNCHED")


def build_tasks(frozen: dict, packet: dict, gmt_index: dict) -> list[dict]:
    packet_index = {row.get("id"): row for row in packet["tasks"]}
    tasks = []
    for row in frozen["tasks"]:
        task_id = row["id"]
        source = packet_index.get(task_id)
        if not isinstance(source, dict):
            raise CurrentnessError("TASK_SOURCE_MISSING", task_id)
        overlay = gmt_index.get(task_id, {})
        task = {
            "id": task_id,
            "phase": source.get("phase"),
            "title": source.get("title"),
            "class": row["class"],
            "depends_on": list(row["depends_on"]),
            "producer_owner": source.get("producer_owner"),
            "terminal_consumer": source.get("terminal_consumer"),
            "sourcefree_state": row["sourcefree_state"],
            "full_original_claim": row.get("full_original_claim", "NOT_ESTABLISHED"),
            "execution_state": _initial_execution_state(row["sourcefree_state"]),
            "protected_integration": (
                "PENDING_PROTECTED_CI_AND_ADOPTION"
                if row["sourcefree_state"] == "SCOPED_RECEIVED_UNMERGED" else "NONE"),
            "scientific_authority": "HELD",
            "source_refs": [
                "packet:" + str(source.get("id")),
                "gmt:" + str(gmt_index.get(task_id, {}).get("task_id", task_id)),
            ],
            "return_event_id": None,
            "review_event_id": None,
            "decision_prerequisites": list(overlay.get(
                "hard_prerequisites_to_expand_beyond_existing_fixture", [])),
            "decision_full_claim": list(overlay.get(
                "determinations_required_before_full_capability_claim", [])),
            "bounded_engineering_now": overlay.get("safe_bounded_engineering_now"),
            "claims_not_yet_warranted": overlay.get("claims_not_yet_warranted"),
            "decision_issue_ids": list(overlay.get("issue_ids", [])),
        }
        for key in ("code_sha", "review_sha", "review_pr", "limitation",
                    "evidence_note"):
            if key in row:
                task[key] = row[key]
        tasks.append(task)
    return tasks


def initial_state(config: dict, whole: dict) -> dict:
    frozen = whole.get(FROZEN_KEY)
    if not isinstance(frozen, dict):
        raise CurrentnessError("FROZEN_PROJECTION_MISSING")
    if frozen.get("schema") != "SOROK_OPERATIONAL_CURRENTNESS_R1":
        raise CurrentnessError("FROZEN_PROJECTION_SCHEMA")
    packet, gmt, gmt_index = frozen_contracts(config)
    tasks = build_tasks(frozen, packet, gmt_index)
    decision_nodes = []
    for node in gmt.get("decision_nodes", []):
        decision = copy.deepcopy(node)
        decision["full_original_claim"] = "NOT_ESTABLISHED"
        decision_nodes.append(decision)
    try:
        atlas_blob = subprocess.check_output(
            ["git", "-C", str(config["_root"]), "rev-parse",
             f"{GMT_ATLAS_COMMIT}:{GMT_ATLAS_PATH}"], text=True).strip()
    except (subprocess.CalledProcessError, OSError):
        atlas_blob = None
    baseline = None
    if config["_baseline"] and config["_baseline"].is_file():
        baseline = {
            "path": str(config["_baseline"]),
            "sha256": sha256_file(config["_baseline"]),
            "as_of": now_utc(),
        }
    verifier = config["_root"] / "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/verify_operational_currentness_r1.py"
    workflow = config["_root"] / ".github/workflows/sorok-operational-currentness-r1.yml"
    if verifier.is_file() and git_blob_sha(verifier.read_bytes()) != VERIFIER_BLOB:
        raise CurrentnessError("FROZEN_VERIFIER_BLOB_MISMATCH")
    if workflow.is_file() and git_blob_sha(workflow.read_bytes()) != WORKFLOW_BLOB:
        raise CurrentnessError("FROZEN_WORKFLOW_BLOB_MISMATCH")
    state = {
        "schema": SCHEMA,
        "generation": 1,
        "checkpoint_id": "",
        "created_utc": now_utc(),
        "updated_utc": now_utc(),
        "source_freeze": {
            "packet_blob": PACKET_BLOB,
            "gmt_blob": GMT_BLOB,
            "verifier_path": str(verifier),
            "verifier_blob": git_blob_sha(verifier.read_bytes()) if verifier.is_file() else None,
            "workflow_path": str(workflow),
            "workflow_blob": git_blob_sha(workflow.read_bytes()) if workflow.is_file() else None,
            "frozen_projection_sha256": digest(frozen),
            "frozen_md_block_sha256": None,
            "operational_gmt_atlas": {
                "commit": GMT_ATLAS_COMMIT,
                "path": GMT_ATLAS_PATH,
                "blob": atlas_blob,
                "status": "DRAFT_DOCUMENTARY_CANDIDATE_NOT_PROTECTED_LAW",
            },
            "oath_r2": {
                "commit": "1341c81dfe0e99da030e7dca356f55789a10c6f8",
                "status": "DRAFT_PR1098_NOT_PROTECTED_LAW",
            },
            "original_scope": {
                "functions": 144, "seams": 38, "gates": 83,
                "assets": 304, "inputs": 100,
            },
        },
        "pair": {
            "json_path": str(config["_pair_json"]),
            "md_path": str(config["_pair_md"]),
            "generation": 1,
            "checkpoint_id": "",
            "reader_boundary": "LOCKED_GENERATION_MATCH_REQUIRED",
        },
        "authenticated_checkpoint": {
            "baseline": baseline,
            "last_authenticated_at_utc": baseline["as_of"] if baseline else None,
            "github_observations": {},
            "local_receipts": {},
            "live_github": None,
            "legacy_baseline_not_live": bool(baseline),
        },
        "events": [],
        "tasks": tasks,
        "decision_nodes": decision_nodes,
        "controls": {"stops": [], "holds": [], "revocations": []},
        "browser": copy.deepcopy(frozen.get("browser", {})),
        "controllers": copy.deepcopy(frozen.get("controllers", {})),
        "outside_packets": copy.deepcopy(frozen.get("outside_packets", {})),
        "protected_foundations": copy.deepcopy(frozen.get("protected_foundations", {})),
        "readiness": {},
        "holds": [],
        "reconciliation_required": [],
        "baseline_replay": [],
        "infrastructure_qualification": [],
        "controller_integration": {
            "installed_controller": config.get("controller_state_root"),
            "hook": "completion_events.py optional COMPLETION_SOROK_CURRENTNESS",
            "hook_state": "CONFIGURED_NOT_YET_OBSERVED",
            "original_controller_hashes": config.get("controller_original_hashes", {}),
        },
        "no_authority_promotion": True,
        "adoption": "NO_PROTECTED_ADOPTION",
        "protected_ci": "PENDING_PROTECTED_CI_AND_ADOPTION",
        "frozen_projection_adoption": frozen.get("adoption"),
        "mechanism_review": {
            "id": MECHANISM_ID,
            "state": "PENDING_EXTERNAL_NONAUTHOR_REVIEW",
            "implementation_commit": config.get("implementation_commit"),
            "review_receipt": None,
            "review_run": None,
        },
        "mechanism_worker_return": None,
        "mechanism_review_history": [],
        "reconciliation_resolved": [],
        "source_authority_holds": [],
        "next_non_dispatch_action": None,
    }
    event = {
        "schema": EVENT_SCHEMA,
        "event_id": "runtime:init:" + digest(frozen),
        "sequence": 1,
        "kind": "INIT",
        "recorded_utc": now_utc(),
        "source": {
            "trust": "FROZEN_OPERATIONAL_PROJECTION_PRESENT",
            "frozen_projection_sha256": digest(frozen),
            "baseline_sha256": baseline["sha256"] if baseline else None,
        },
        "payload": {"adoption": frozen.get("adoption"),
                    "full_original_claim": "NOT_ESTABLISHED"},
    }
    event["event_hash"] = digest(event)
    event["previous_event_hash"] = None
    state["events"].append(event)
    recompute(state)
    return state


def _direct_scope(controls: list[dict], task_id: str) -> list[dict]:
    return [row for row in controls
            if row.get("scope") in (task_id, "ALL")]


def recompute(state: dict) -> None:
    tasks = state["tasks"]
    by_id = {row["id"]: row for row in tasks}
    controls = state.setdefault("controls", {"stops": [], "holds": [], "revocations": []})
    scoped_ok = {"CANDIDATE_AUTHOR_TESTED", "PARTIAL_CANDIDATE",
                 "SCOPED_RECEIVED_UNMERGED", "PROTECTED_SOURCEFREE"}
    blocked: dict[str, str] = {}
    for task in tasks:
        task_id = task["id"]
        if _direct_scope(controls.get("revocations", []), task_id):
            blocked[task_id] = "REVOKED"
        elif _direct_scope(controls.get("stops", []), task_id):
            blocked[task_id] = "STOPPED_BY_USER"
        elif _direct_scope(controls.get("holds", []), task_id):
            blocked[task_id] = "HELD_SOURCE_AUTHORITY"
        elif task.get("sourcefree_state") == "REJECTED":
            blocked[task_id] = "REJECTED"
        elif task.get("sourcefree_state") == "REVISE_REQUIRED":
            blocked[task_id] = "REVISE_REQUIRED"
        elif task.get("sourcefree_state") == "HELD_SOURCE_AUTHORITY":
            blocked[task_id] = "HELD_SOURCE_AUTHORITY"
    changed = True
    while changed:
        changed = False
        for task in tasks:
            task_id = task["id"]
            if task_id in blocked:
                continue
            for dependency in task["depends_on"]:
                if dependency in blocked:
                    blocked[task_id] = "BLOCKED_BY_DEPENDENCY"
                    changed = True
                    break
    ready_scoped, ready_receiving, awaiting_receiving, holds, full_ready = [], [], [], [], []
    for task in tasks:
        task_id = task["id"]
        unmet_scoped = [
            dependency for dependency in task["depends_on"]
            if by_id.get(dependency, {}).get("execution_state") not in scoped_ok
        ]
        unmet_full = [
            dependency for dependency in task["depends_on"]
            if by_id.get(dependency, {}).get("full_original_claim") != "ESTABLISHED"
        ]
        task["unmet_scoped_prereqs"] = unmet_scoped
        task["unmet_full_original_prereqs"] = unmet_full
        if task_id in blocked:
            readiness = blocked[task_id]
        elif task["sourcefree_state"] == "PROTECTED_SOURCEFREE":
            readiness = "PROTECTED_SOURCEFREE"
        elif task["sourcefree_state"] == "SCOPED_RECEIVED_UNMERGED":
            readiness = "SCOPED_RECEIVED_PENDING_PROTECTED_CI_AND_ADOPTION"
        elif task["execution_state"] == "RETURNED_REVIEW_PENDING":
            readiness = "READY_FOR_INDEPENDENT_RECEIVING"
        elif task["sourcefree_state"] in ("CANDIDATE", "PARTIAL_CANDIDATE"):
            readiness = "CANDIDATE_RETURNED_RECEIVING_NOT_RUN"
        elif unmet_scoped:
            readiness = "HOLD_DEPENDENCY"
        elif task["sourcefree_state"] == "HELD_NOT_LAUNCHED":
            readiness = "HELD_NOT_LAUNCHED"
        else:
            readiness = "READY_FOR_SCOPED_ENGINEERING"
        task["readiness"] = readiness
        task["ready_for_scoped_engineering"] = (
            readiness in {"READY_FOR_SCOPED_ENGINEERING",
                          "CANDIDATE_RETURNED_RECEIVING_NOT_RUN",
                          "READY_FOR_INDEPENDENT_RECEIVING"})
        task["ready_for_independent_receiving"] = readiness == "READY_FOR_INDEPENDENT_RECEIVING"
        task["full_original_ready"] = False
        task["owner"] = task.get("producer_owner")
        task["next_action"] = _next_action(task)
        task["claim_ready"] = readiness in {
            "READY_FOR_SCOPED_ENGINEERING", "CANDIDATE_RETURNED_RECEIVING_NOT_RUN",
            "READY_FOR_INDEPENDENT_RECEIVING", "SCOPED_RECEIVED_PENDING_PROTECTED_CI_AND_ADOPTION",
            "PROTECTED_SOURCEFREE"}
        task["bounded_repair_or_receiving_action"] = (
            "REVISE_OR_RECEIVE_BOUNDED_ENGINEERING_NOT_FULL_CLAIM"
            if readiness in ("REJECTED", "REVISE_REQUIRED", "BLOCKED_BY_DEPENDENCY")
            else task["next_action"])
        if readiness == "READY_FOR_SCOPED_ENGINEERING":
            ready_scoped.append(task_id)
        if readiness in ("CANDIDATE_RETURNED_RECEIVING_NOT_RUN",
                         "READY_FOR_INDEPENDENT_RECEIVING"):
            awaiting_receiving.append(task_id)
        if task["ready_for_independent_receiving"]:
            ready_receiving.append(task_id)
        if task_id in blocked:
            holds.append({
                "task": task_id, "state": blocked[task_id],
                "owner": task.get("producer_owner"),
                "reason": _block_reason(state, task_id, blocked[task_id]),
            })
        if task["full_original_claim"] != "ESTABLISHED":
            full_ready.append(task_id)
    state["readiness"] = {
        "ready_for_scoped_engineering": sorted(
            ready_scoped, key=lambda key: (PHASE_ORDER.get(by_id[key]["phase"], 99), key)),
        "ready_for_independent_receiving": sorted(
            ready_receiving, key=lambda key: (PHASE_ORDER.get(by_id[key]["phase"], 99), key)),
        "awaiting_independent_receiving": sorted(
            awaiting_receiving, key=lambda key: (PHASE_ORDER.get(by_id[key]["phase"], 99), key)),
        "task_readiness": [
            {"id": row["id"], "readiness": row["readiness"],
             "owner": row.get("producer_owner"),
             "unmet_scoped_prereqs": row["unmet_scoped_prereqs"],
             "unmet_full_original_prereqs": row["unmet_full_original_prereqs"],
             "sourcefree_state": row["sourcefree_state"],
             "execution_state": row["execution_state"],
             "code_sha": row.get("code_sha"),
             "review_sha": row.get("review_sha"),
             "review_pr": row.get("review_pr"),
             "protected_integration": row.get("protected_integration"),
             "protected_ci": row.get("protected_ci"),
             "decision_prerequisites": row.get("decision_prerequisites", []),
             "decision_full_claim": row.get("decision_full_claim", []),
             "decision_status": row.get("decision_status", {}),
             "full_original_decision_blockers": row.get(
                 "full_original_decision_blockers", []),
             "full_original_readiness": row.get("full_original_readiness"),
             "claim_ready": row.get("claim_ready"),
             "bounded_repair_or_receiving_action": row.get(
                 "bounded_repair_or_receiving_action"),
             "source_refs": row["source_refs"]}
            for row in tasks
        ],
        "holds": holds,
        "full_original_claim_not_established": sorted(full_ready),
        "browser": state.get("browser", {}),
        "controllers": state.get("controllers", {}),
        "protected_ci": state.get("protected_ci"),
    }
    node_by_id = {node.get("id"): node for node in state.get("decision_nodes", [])}
    for task in tasks:
        statuses = {node_id: node_by_id.get(node_id, {}).get("status", "UNKNOWN")
                    for node_id in task.get("decision_full_claim", [])}
        task["decision_status"] = statuses
        blockers = [node_id for node_id, status in statuses.items()
                    if not str(status).startswith(("ESTABLISHED", "SETTLED",
                                                    "GOVERNING_SOURCE_PRESENT"))]
        task["full_original_decision_blockers"] = blockers
        task["full_original_readiness"] = (
            "HOLD_DECISION_" + ",".join(blockers) if blockers else
            "FULL_ORIGINAL_NOT_ESTABLISHED")
    for node in state.get("decision_nodes", []):
        kind = node.get("decision_kind")
        status = str(node.get("status", ""))
        if kind == "EXTERNAL_AUTHORITY_HOLD":
            readiness = "HOLD_SOURCE_AUTHORITY"
        elif kind == "OPEN_SCIENTIFIC_MECHANISM":
            readiness = "OPEN_SCIENTIFIC_MECHANISM"
        elif status.startswith(("ESTABLISHED", "SETTLED",
                                "GOVERNING_SOURCE_PRESENT")):
            readiness = "SETTLED_LAW"
        else:
            readiness = "EXECUTIVE_OR_OWNER_DECISION_REQUIRED"
        node["readiness"] = readiness
        node["full_original_claim"] = "NOT_ESTABLISHED"
    state["decision_readiness"] = [
        {"id": node.get("id"), "kind": node.get("decision_kind"),
         "status": node.get("status"), "readiness": node.get("readiness"),
         "depends_on": node.get("depends_on", []),
         "blocks_full_claim": node.get("blocks_full_claim")}
        for node in state.get("decision_nodes", [])
    ]
    state["holds"] = _compose_holds(state)
    state["recommended_next"] = _recommended_next(state, by_id)
    state["checkpoint_id"] = _checkpoint_id(state)
    state["pair"]["generation"] = state["generation"]
    state["pair"]["checkpoint_id"] = state["checkpoint_id"]


def _block_reason(state: dict, task_id: str, state_name: str) -> str:
    controls = state.get("controls", {})
    rows = (_direct_scope(controls.get("holds", []), task_id)
            or _direct_scope(controls.get("stops", []), task_id)
            or _direct_scope(controls.get("revocations", []), task_id))
    if rows:
        return rows[-1].get("reason", state_name)
    return state_name


def _next_action(task: dict) -> str:
    if task["readiness"].startswith("READY_FOR"):
        return "Receive or execute the bounded next action; no automatic dispatch."
    if task["readiness"] == "SCOPED_RECEIVED_PENDING_PROTECTED_CI_AND_ADOPTION":
        return "Protected CI and separate adoption remain pending; do not claim protected integration."
    if task["unmet_scoped_prereqs"]:
        return "Unmet scoped prerequisites: " + ", ".join(task["unmet_scoped_prereqs"])
    return "Full original claim remains NOT_ESTABLISHED; preserve source/owner holds."


def _compose_holds(state: dict) -> list[dict]:
    rows = []
    for hold in state.get("controls", {}).get("holds", []):
        rows.append({"kind": "SOURCE_AUTHORITY_HOLD", "scope": hold.get("scope"),
                     "owner": hold.get("owner"), "reason": hold.get("reason")})
    for stop in state.get("controls", {}).get("stops", []):
        rows.append({"kind": "USER_STOP", "scope": stop.get("scope"),
                     "owner": stop.get("owner", "user"),
                     "reason": stop.get("reason")})
    for revoke in state.get("controls", {}).get("revocations", []):
        rows.append({"kind": "REVOCATION", "scope": revoke.get("scope"),
                     "owner": revoke.get("owner"), "reason": revoke.get("reason")})
    for hold in state.get("source_authority_holds", []):
        rows.append({"kind": "SOURCE_AUTHORITY_HOLD",
                     "scope": hold.get("what_changed"),
                     "owner": "competent source authority",
                     "reason": "held by authenticated source-authority evidence"})
    mechanism_return = state.get("mechanism_worker_return")
    if isinstance(mechanism_return, dict):
        rows.append({"kind": "REAL_MECHANISM_WORKER_RETURN",
                     "scope": MECHANISM_ID,
                     "owner": mechanism_return.get("session"),
                     "reason": mechanism_return.get("execution_state")})
    mechanism_review = state.get("mechanism_review") or {}
    if str(mechanism_review.get("state", "")).startswith("PENDING"):
        rows.append({"kind": "MECHANISM_REVIEW",
                     "scope": MECHANISM_ID,
                     "owner": "separate independent nonauthor",
                     "reason": mechanism_review.get("state")})
    for key, value in state.get("browser", {}).items():
        rows.append({"kind": "BROWSER_OWNERSHIP", "scope": key,
                     "owner": "user-operated Browser", "reason": value})
    for key, value in state.get("controllers", {}).items():
        rows.append({"kind": "CONTROLLER", "scope": key,
                     "owner": "existing SOROK owner", "reason": value})
    rows.append({"kind": "SCIENCE_AUTHORITY", "scope": "ALL",
                 "owner": "original CAN/ADP/Pyat/human issuers",
                 "reason": "native science, actor knowledge and human authority remain HELD"})
    return rows


def _recommended_next(state: dict, by_id: dict) -> dict:
    for task_id in state["readiness"].get("awaiting_independent_receiving", []):
        task = by_id[task_id]
        return {"action": "RECEIVE", "task": task_id, "owner": task.get("producer_owner"),
                "unmet_full_original_prereqs": task["unmet_full_original_prereqs"]}
    for task_id in state["readiness"]["ready_for_scoped_engineering"]:
        task = by_id[task_id]
        return {"action": "SCOPED_ENGINEERING", "task": task_id,
                "owner": task.get("producer_owner"),
                "unmet_full_original_prereqs": task["unmet_full_original_prereqs"]}
    return {"action": "NONE_READY", "task": None, "owner": None,
            "unmet_full_original_prereqs": []}


def _checkpoint_id(state: dict) -> str:
    payload = {
        "schema": state["schema"],
        "generation": state["generation"],
        "events": [{"event_id": row.get("event_id"), "event_hash": row.get("event_hash")}
                   for row in state.get("events", [])],
        "tasks": [{"id": row["id"], "sourcefree_state": row["sourcefree_state"],
                   "execution_state": row["execution_state"],
                   "review_sha": row.get("review_sha"),
                   "code_sha": row.get("code_sha"),
                   "readiness": row.get("readiness")}
                  for row in state.get("tasks", [])],
        "controls": state.get("controls", {}),
        "reconciliation_required": state.get("reconciliation_required", []),
        "reconciliation_resolved": state.get("reconciliation_resolved", []),
        "authenticated_checkpoint": state.get("authenticated_checkpoint", {}),
    }
    return digest(payload)


def _event_hash(event: dict) -> str:
    body = {key: value for key, value in event.items()
            if key not in ("event_hash", "previous_event_hash")}
    return digest(body)


def _last_event(state: dict) -> dict | None:
    return state["events"][-1] if state.get("events") else None


def _find_duplicate(state: dict, event_id: str, event_hash: str) -> dict | None:
    for row in state.get("events", []):
        if row.get("event_id") == event_id or row.get("event_hash") == event_hash:
            return row
    return None


def _task_by_id(state: dict, task_id: str) -> dict:
    for task in state["tasks"]:
        if task["id"] == task_id:
            return task
    raise CurrentnessError("TASK_UNKNOWN", task_id)


def validate_controller_run(run_dir: Path, source: dict) -> dict:
    run_dir = run_dir.resolve()
    required = ("job.json", "binding.json", "launch.json", "process.json",
                "completion.json")
    for name in required:
        if not (run_dir / name).is_file():
            raise CurrentnessError("CONTROLLER_RECEIPT_MISSING", name)
    job = read_json(run_dir / "job.json")
    binding = read_json(run_dir / "binding.json")
    launch = read_json(run_dir / "launch.json")
    process = read_json(run_dir / "process.json")
    completion = read_json(run_dir / "completion.json")
    hashes = {
        "job_sha256": sha256_file(run_dir / "job.json"),
        "binding_sha256": sha256_file(run_dir / "binding.json"),
        "launch_sha256": sha256_file(run_dir / "launch.json"),
        "process_sha256": sha256_file(run_dir / "process.json"),
        "completion_sha256": sha256_file(run_dir / "completion.json"),
    }
    for key, value in hashes.items():
        if source.get(key) and source[key] != value:
            raise CurrentnessError("CONTROLLER_RECEIPT_HASH_MISMATCH", key)
    if completion.get("exit_code") != 0:
        raise CurrentnessError("CONTROLLER_ZERO_EXIT_REQUIRED",
                               completion.get("exit_code"))
    if not (completion.get("pid") == process.get("pid") == launch.get("child_pid")):
        raise CurrentnessError("CONTROLLER_PID_MISMATCH")
    if not (job.get("job_id") == completion.get("job_id") == launch.get("job_id")):
        raise CurrentnessError("CONTROLLER_JOB_ID_MISMATCH")
    if not (job.get("session") == binding.get("session") == completion.get("session")):
        raise CurrentnessError("CONTROLLER_SESSION_MISMATCH")
    if job.get("grant_id") != binding.get("grant", {}).get("id"):
        raise CurrentnessError("CONTROLLER_GRANT_MISMATCH")
    if command_digest(job.get("argv", [])) != binding.get("grant", {}).get("argv_sha256"):
        raise CurrentnessError("CONTROLLER_ARGV_MISMATCH")
    worktree = Path(binding.get("worktree", "")).resolve()
    if not worktree.is_dir():
        raise CurrentnessError("CONTROLLER_WORKTREE_MISSING", str(worktree))
    if source.get("worktree") and Path(source["worktree"]).resolve() != worktree:
        raise CurrentnessError("CONTROLLER_WORKTREE_MISMATCH")
    if source.get("job_id") and source["job_id"] != job.get("job_id"):
        raise CurrentnessError("CONTROLLER_SOURCE_JOB_MISMATCH")
    if source.get("session") and source["session"] != job.get("session"):
        raise CurrentnessError("CONTROLLER_SOURCE_SESSION_MISMATCH")
    if source.get("pid") and int(source["pid"]) != int(process.get("pid")):
        raise CurrentnessError("CONTROLLER_SOURCE_PID_MISMATCH")
    if not UUID_RE.fullmatch(str(binding.get("recipient_thread", ""))):
        raise CurrentnessError("CONTROLLER_RECIPIENT_INVALID")
    completion_hash = hashes["completion_sha256"]
    event_id = source.get("event_id") or "completion:" + completion_hash
    return {
        "run_dir": str(run_dir), "job": job, "binding": binding, "launch": launch,
        "process": process, "completion": completion, "hashes": hashes,
        "event_id": event_id,
    }


def _verify_return_artifact(source: dict, binding: dict) -> dict:
    path_value = source.get("return_path")
    if not path_value:
        raise CurrentnessError("RETURN_ARTIFACT_REQUIRED")
    path = Path(path_value).resolve()
    worktree = Path(binding.get("worktree", "")).resolve()
    if worktree not in path.parents and path != worktree:
        raise CurrentnessError("RETURN_ARTIFACT_OUTSIDE_WORKTREE", str(path))
    if not path.is_file():
        raise CurrentnessError("RETURN_ARTIFACT_MISSING", str(path))
    actual = sha256_file(path)
    if source.get("return_sha256") and source["return_sha256"] != actual:
        raise CurrentnessError("RETURN_ARTIFACT_HASH_MISMATCH")
    payload = read_json(path)
    if (not isinstance(payload, dict)
            or payload.get("schema") not in (
                RETURN_SCHEMA, REVIEW_RECEIPT_SCHEMA, REJECTION_SCHEMA,
                PROTECTED_INTEGRATION_SCHEMA)):
        raise CurrentnessError("RETURN_ARTIFACT_SCHEMA")
    return {"path": str(path), "sha256": actual, "payload": payload}


def verify_git_documents(repo_root: Path, commit: str, documents: list[dict]) -> list[dict]:
    if not HASH_RE.fullmatch(str(commit)):
        raise CurrentnessError("REVIEW_COMMIT_INVALID")
    if subprocess.run(["git", "-C", str(repo_root), "cat-file", "-e", commit],
                      capture_output=True, text=True).returncode != 0:
        raise CurrentnessError("REVIEW_COMMIT_UNAVAILABLE", commit)
    verified = []
    for document in documents:
        path = document.get("path")
        expected = document.get("git_blob")
        if not path or not expected:
            raise CurrentnessError("REVIEW_DOCUMENT_PIN_INCOMPLETE")
        result = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", f"{commit}:{path}"],
            capture_output=True, text=True)
        if result.returncode != 0 or result.stdout.strip() != expected:
            raise CurrentnessError("REVIEW_DOCUMENT_BLOB_MISMATCH", path)
        verified.append({"path": path, "git_blob": expected})
    return verified


def _verify_verdict_artifact(config: dict, commit: str,
                             documents: list[dict], verdict: str) -> dict:
    candidates = [doc for doc in documents
                  if str(doc.get("path", "")).endswith("VERDICT.json")]
    if not candidates:
        raise CurrentnessError("REVIEWED_VERDICT_ARTIFACT_REQUIRED")
    document = candidates[0]
    path = document.get("path")
    expected_blob = document.get("git_blob")
    result = subprocess.run(
        ["git", "-C", str(config["_root"]), "rev-parse", f"{commit}:{path}"],
        capture_output=True, text=True)
    if result.returncode != 0 or result.stdout.strip() != expected_blob:
        raise CurrentnessError("REVIEWED_VERDICT_BLOB_MISMATCH", path)
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(config["_root"]), "show", f"{commit}:{path}"])
        artifact = json.loads(raw)
    except (subprocess.CalledProcessError, ValueError, TypeError) as exc:
        raise CurrentnessError("REVIEWED_VERDICT_UNREADABLE", path) from exc
    actual = artifact.get("engineering_verdict") or artifact.get("verdict")
    if not isinstance(actual, str) or actual != verdict:
        raise CurrentnessError("REVIEW_VERDICT_ARTIFACT_MISMATCH",
                               {"expected": verdict, "artifact": actual})
    return {"path": path, "git_blob": expected_blob, "verdict": actual}


def _validate_review_receipt(config: dict, receipt: dict, *, replay: bool,
                             source: dict | None = None) -> dict:
    if not isinstance(receipt, dict) or receipt.get("schema") != REVIEW_RECEIPT_SCHEMA:
        raise CurrentnessError("REVIEW_RECEIPT_SCHEMA")
    task_id = receipt.get("task_id")
    if task_id not in EXPECTED_IDS and task_id != MECHANISM_ID:
        raise CurrentnessError("REVIEW_TASK_UNKNOWN", task_id)
    verdict = receipt.get("verdict")
    if verdict not in ALLOWED_VERDICTS:
        raise CurrentnessError("REVIEW_VERDICT_UNKNOWN", verdict)
    if receipt.get("reviewer_session") == receipt.get("author_session"):
        raise CurrentnessError("SELF_REVIEW_REFUSED")
    if not receipt.get("reviewer_session") or not receipt.get("author_session"):
        raise CurrentnessError("REVIEW_SESSION_MISSING")
    if not receipt.get("scope"):
        raise CurrentnessError("REVIEW_SCOPE_MISSING")
    if receipt.get("full_original_claim") != "NOT_ESTABLISHED":
        raise CurrentnessError("SCOPE_INFLATION_REFUSED")
    if verdict.startswith("ACCEPT_SCOPED"):
        if receipt.get("protected_ci") not in ("UNAVAILABLE_BILLING", "NOT_RUN", "PASS"):
            raise CurrentnessError("PROTECTED_CI_STATE_INVALID")
        if receipt.get("adoption") not in (
                "PENDING_PROTECTED_CI_AND_ADOPTION", "NO_PROTECTED_ADOPTION"):
            raise CurrentnessError("ADOPTION_INFLATION_REFUSED")
    documents = receipt.get("source_documents") or []
    commit = receipt.get("review_commit")
    verified = verify_git_documents(config["_root"], commit, documents)
    if replay:
        if receipt.get("source_trust") != "IMMUTABLE_HISTORICAL_INDEPENDENT_REVIEW_REPLAY":
            raise CurrentnessError("REPLAY_TRUST_REQUIRED")
        return {
            "receipt": receipt, "verified_documents": verified,
            "receipt_sha256": digest(receipt), "replay": True,
            "review_run": None,
        }
    if not isinstance(source, dict):
        raise CurrentnessError("REVIEW_SUPERVISED_RUN_REQUIRED")
    if source.get("trust") != "REAL_LOCAL_SUPERVISED_REVIEW_RUN":
        raise CurrentnessError("REVIEW_SUPERVISED_RUN_REQUIRED")
    run_dir = source.get("review_run_dir")
    if not run_dir:
        raise CurrentnessError("REVIEW_SUPERVISED_RUN_REQUIRED")
    run = validate_controller_run(Path(run_dir), source)
    _require_trusted_launch(config, Path(run_dir), run, run["binding"])
    if run["completion"].get("exit_code") != 0:
        raise CurrentnessError("REVIEW_RUN_ZERO_EXIT_REQUIRED")
    binding = run["binding"].get("sorok_currentness") or {}
    if binding.get("role") != "REVIEWER":
        raise CurrentnessError("REVIEW_RUN_ROLE_MISMATCH")
    if binding.get("task_id") != task_id:
        raise CurrentnessError("REVIEW_RUN_TASK_MISMATCH")
    if binding.get("expected_session") and binding["expected_session"] != receipt.get(
            "reviewer_session"):
        raise CurrentnessError("REVIEW_RUN_SESSION_MISMATCH")
    if binding.get("expected_source_commit") and binding[
            "expected_source_commit"] != receipt.get("implementation_commit"):
        raise CurrentnessError("REVIEW_RUN_SOURCE_MISMATCH")
    artifact = _verify_return_artifact(source, run["binding"])
    if artifact["payload"].get("schema") != REVIEW_RECEIPT_SCHEMA:
        raise CurrentnessError("REVIEW_RUN_ARTIFACT_SCHEMA")
    if digest(artifact["payload"]) != digest(receipt):
        raise CurrentnessError("REVIEW_RUN_ARTIFACT_MISMATCH")
    verdict_artifact = _verify_verdict_artifact(
        config, commit, documents, verdict)
    return {
        "receipt": receipt, "verified_documents": verified,
        "verdict_artifact": verdict_artifact,
        "receipt_sha256": digest(receipt), "replay": False,
        "review_run": {
            "run_dir": run["run_dir"], "job_id": run["job"]["job_id"],
            "session": run["job"]["session"],
            "grant_id": run["job"]["grant_id"],
            "completion_sha256": run["hashes"]["completion_sha256"],
            "binding_sha256": run["hashes"]["binding_sha256"],
            "launch_sha256": run["hashes"]["launch_sha256"],
            "return_sha256": artifact["sha256"],
            "role": "REVIEWER",
        },
    }


def _capability(config: dict) -> dict:
    path = config["_capability_path"]
    if not path.is_file():
        capability = {
            "schema": CAPABILITY_SCHEMA,
            "capability_id": "cap-" + secrets.token_hex(16),
            "key": secrets.token_hex(32),
            "created_utc": now_utc(),
        }
        path.parent.mkdir(parents=True, exist_ok=True)
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(capability, indent=2) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
    else:
        capability = read_json(path)
    if capability.get("schema") != CAPABILITY_SCHEMA:
        raise CurrentnessError("LOCAL_CAPABILITY_SCHEMA")
    return capability


def _sign_capability(config: dict, payload: dict) -> dict:
    capability = _capability(config)
    signature = hmac.new(bytes.fromhex(capability["key"]),
                         canonical(payload).encode("utf-8"),
                         hashlib.sha256).hexdigest()
    return {"capability_id": capability["capability_id"],
            "signature": signature}


def _verify_capability(config: dict, source: dict, payload: dict) -> None:
    capability = _capability(config)
    if source.get("capability_id") != capability["capability_id"]:
        raise CurrentnessError("LOCAL_CAPABILITY_MISMATCH")
    expected = hmac.new(bytes.fromhex(capability["key"]),
                        canonical(payload).encode("utf-8"),
                        hashlib.sha256).hexdigest()
    if not hmac.compare_digest(str(source.get("signature", "")), expected):
        raise CurrentnessError("LOCAL_CAPABILITY_SIGNATURE_MISMATCH")


def _registry_path(config: dict) -> Path:
    return config["_trusted_registry_path"]


def _registry_load(config: dict) -> dict:
    path = _registry_path(config)
    if not path.is_file():
        return {"schema": TRUSTED_LAUNCH_SCHEMA, "entries": {}}
    registry = read_json(path)
    if registry.get("schema") != TRUSTED_LAUNCH_SCHEMA:
        raise CurrentnessError("TRUSTED_LAUNCH_REGISTRY_SCHEMA")
    if not isinstance(registry.get("entries"), dict):
        raise CurrentnessError("TRUSTED_LAUNCH_REGISTRY_ENTRIES")
    return registry


def _pid_alive(pid: int) -> bool:
    try:
        result = subprocess.run(
            ["ps", "-p", str(pid), "-o", "pid="],
            capture_output=True, text=True, timeout=5)
        return result.returncode == 0 and bool(result.stdout.strip())
    except (OSError, subprocess.TimeoutExpired):
        return False


def _pid_ppid(pid: int) -> int | None:
    try:
        result = subprocess.run(
            ["ps", "-p", str(pid), "-o", "ppid="],
            capture_output=True, text=True, timeout=5)
        text = result.stdout.strip()
        return int(text) if result.returncode == 0 and text else None
    except (OSError, subprocess.TimeoutExpired, ValueError):
        return None


def _pid_command(pid: int) -> str:
    try:
        result = subprocess.run(
            ["ps", "-p", str(pid), "-o", "command="],
            capture_output=True, text=True, timeout=5)
        return result.stdout.strip() if result.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def _require_launcher_process_tree(launch: dict, process: dict) -> None:
    parent = os.getppid()
    command = _pid_command(parent)
    if ("launch.py" not in command or "--binding" not in command
            or "--job" not in command):
        raise CurrentnessError("TRUSTED_LAUNCH_CALLER_INVALID", parent)
    supervisor_pid = int(launch.get("supervisor_pid") or 0)
    observer_pid = int(launch.get("observer_pid") or 0)
    child_pid = int(process.get("pid") or 0)
    if (_pid_ppid(supervisor_pid) != parent
            or _pid_ppid(observer_pid) != parent
            or _pid_ppid(child_pid) != supervisor_pid):
        raise CurrentnessError("TRUSTED_LAUNCH_PROCESS_TREE_INVALID")


def _registry_entry(config: dict, run_dir: Path, binding: dict,
                    job: dict, launch: dict, process: dict, *,
                    provenance: str, migration: bool) -> dict:
    currentness = binding.get("sorok_currentness") or {}
    entry = {
        "launch_id": "launch-" + secrets.token_hex(16),
        "provenance": provenance,
        "migration": migration,
        "attested_at_utc": now_utc(),
        "expires_at_utc": _utc_add(7 * 24 * 3600),
        "run_dir": str(run_dir.resolve()),
        "job_id": job.get("job_id"),
        "session": job.get("session"),
        "grant_id": job.get("grant_id"),
        "argv_sha256": command_digest(job.get("argv", [])),
        "worktree": str(Path(binding.get("worktree", "")).resolve()),
        "recipient_thread": binding.get("recipient_thread"),
        "role": currentness.get("role"),
        "task_id": currentness.get("task_id"),
        "expected_session": currentness.get("expected_session"),
        "expected_source_commit": currentness.get("expected_source_commit"),
        "return_filename": currentness.get("return_filename"),
        "child_pid": launch.get("child_pid"),
        "job_sha256": sha256_file(run_dir / "job.json"),
        "binding_sha256": sha256_file(run_dir / "binding.json"),
        "launch_sha256": sha256_file(run_dir / "launch.json"),
        "process_sha256": sha256_file(run_dir / "process.json"),
        "process_started_utc": process.get("started_utc"),
    }
    entry["attestation"] = _sign_capability(config, entry)
    return entry


def _registry_add(config: dict, entry: dict) -> None:
    with _lock(config, True):
        registry = _registry_load(config)
        if entry["run_dir"] in {row.get("run_dir") for row in registry["entries"].values()}:
            raise CurrentnessError("TRUSTED_LAUNCH_ALREADY_ENROLLED", entry["run_dir"])
        registry["entries"][entry["launch_id"]] = entry
        write_json_atomic(_registry_path(config), registry)


def _registry_find(config: dict, run_dir: Path) -> dict | None:
    registry = _registry_load(config)
    resolved = str(run_dir.resolve())
    for entry in registry["entries"].values():
        if entry.get("run_dir") == resolved:
            return entry
    return None


def _verify_registry_entry(config: dict, entry: dict) -> None:
    attestation = entry.get("attestation")
    if not isinstance(attestation, dict):
        raise CurrentnessError("TRUSTED_LAUNCH_ATTESTATION_MISSING")
    unsigned = {key: value for key, value in entry.items() if key != "attestation"}
    _verify_capability(config, attestation, unsigned)
    try:
        if _parse_utc(entry["expires_at_utc"]) <= datetime.datetime.now(
                datetime.timezone.utc):
            raise CurrentnessError("TRUSTED_LAUNCH_ATTESTATION_EXPIRED")
    except (KeyError, ValueError, TypeError) as exc:
        raise CurrentnessError("TRUSTED_LAUNCH_ATTESTATION_EXPIRED") from exc


def _require_trusted_launch(config: dict, run_dir: Path, run: dict,
                            binding: dict) -> dict:
    entry = _registry_find(config, run_dir)
    if entry is None:
        raise CurrentnessError("UNTRUSTED_CONTROLLER_RUN", str(run_dir))
    _verify_registry_entry(config, entry)
    currentness = binding.get("sorok_currentness") or {}
    checks = {
        "job_id": run["job"].get("job_id"),
        "session": run["job"].get("session"),
        "grant_id": run["job"].get("grant_id"),
        "child_pid": run["process"].get("pid"),
        "role": currentness.get("role"),
        "task_id": currentness.get("task_id"),
        "job_sha256": run["hashes"].get("job_sha256"),
        "binding_sha256": run["hashes"].get("binding_sha256"),
        "launch_sha256": run["hashes"].get("launch_sha256"),
        "process_sha256": run["hashes"].get("process_sha256"),
    }
    for key, value in checks.items():
        if entry.get(key) != value:
            raise CurrentnessError("TRUSTED_LAUNCH_MISMATCH", key)
    return entry


def _require_trusted_run_root(config: dict, run_dir: Path) -> None:
    controller = config.get("_controller_state_root")
    if not controller:
        raise CurrentnessError("TRUSTED_RUN_ROOT_UNAVAILABLE")
    allowed = {Path(controller).resolve(), Path(controller).resolve().parent}
    if run_dir.resolve().parent not in allowed:
        raise CurrentnessError("UNTRUSTED_RUN_PATH", str(run_dir))


def attest_launch(config: dict, run_dir: Path) -> dict:
    run_dir = run_dir.resolve()
    _require_trusted_run_root(config, run_dir)
    job = read_json(run_dir / "job.json")
    binding = read_json(run_dir / "binding.json")
    launch = read_json(run_dir / "launch.json")
    process = read_json(run_dir / "process.json")
    currentness = binding.get("sorok_currentness") or {}
    if currentness.get("role") not in ("IMPLEMENTER", "REVIEWER", "REJECTOR",
                                       "PROTECTED_INTEGRATOR"):
        raise CurrentnessError("TRUSTED_LAUNCH_ROLE_MISSING")
    if not currentness.get("task_id"):
        raise CurrentnessError("TRUSTED_LAUNCH_TASK_MISSING")
    if (launch.get("child_pid") != process.get("pid")
            or job.get("job_id") != launch.get("job_id")
            or job.get("job_id") != process.get("job_id")):
        raise CurrentnessError("TRUSTED_LAUNCH_IDENTITY_MISMATCH")
    if command_digest(job.get("argv", [])) != binding.get("grant", {}).get(
            "argv_sha256"):
        raise CurrentnessError("TRUSTED_LAUNCH_ARGV_MISMATCH")
    if not _pid_alive(int(process.get("pid") or 0)):
        raise CurrentnessError("TRUSTED_LAUNCH_PROCESS_NOT_LIVE",
                               process.get("pid"))
    _require_launcher_process_tree(launch, process)
    entry = _registry_entry(
        config, run_dir, binding, job, launch, process,
        provenance="TRUSTED_LAUNCHER_ATTESTATION", migration=False)
    _registry_add(config, entry)
    return {"state": "TRUSTED_LAUNCH_ATTESTED", "launch_id": entry["launch_id"],
            "run_dir": entry["run_dir"], "role": entry["role"],
            "task_id": entry["task_id"], "child_pid": entry["child_pid"]}


def enroll_existing_run(config: dict, run_dir: Path,
                        authorization_id: str) -> dict:
    run_dir = run_dir.resolve()
    _require_trusted_run_root(config, run_dir)
    job = read_json(run_dir / "job.json")
    binding = read_json(run_dir / "binding.json")
    launch = read_json(run_dir / "launch.json")
    process = read_json(run_dir / "process.json")
    currentness = binding.get("sorok_currentness") or {}
    item = {
        "what_changed": "TRUSTED_LAUNCH_ENROLLMENT " + str(job.get("job_id")),
        "source_digest": digest({
            "job_id": job.get("job_id"), "session": job.get("session"),
            "grant_id": job.get("grant_id"),
            "job_sha256": sha256_file(run_dir / "job.json"),
            "binding_sha256": sha256_file(run_dir / "binding.json"),
            "launch_sha256": sha256_file(run_dir / "launch.json"),
            "process_sha256": sha256_file(run_dir / "process.json"),
            "pid": process.get("pid"),
        }),
    }
    authorization, authorization_sha = _authorize_operator(
        config, purpose="TRUSTED_LAUNCH_ENROLLMENT", item=item,
        authorization_id=authorization_id,
        allowed_roles=("SOROK_HQ_OPERATOR",))
    if currentness.get("role") not in ("IMPLEMENTER", "REVIEWER", "REJECTOR",
                                       "PROTECTED_INTEGRATOR"):
        raise CurrentnessError("TRUSTED_LAUNCH_ROLE_MISSING")
    if (launch.get("child_pid") != process.get("pid")
            or job.get("job_id") != launch.get("job_id")
            or job.get("job_id") != process.get("job_id")):
        raise CurrentnessError("TRUSTED_LAUNCH_IDENTITY_MISMATCH")
    if not _pid_alive(int(process.get("pid") or 0)):
        raise CurrentnessError("TRUSTED_LAUNCH_PROCESS_NOT_LIVE",
                               process.get("pid"))
    entry = _registry_entry(
        config, run_dir, binding, job, launch, process,
        provenance="HQ_EXPLICIT_ACTIVE_RUN_ENROLLMENT", migration=True)
    entry["enrollment_authorization_id"] = authorization.get("authorization_id")
    entry["enrollment_authorization_sha256"] = authorization_sha
    entry["attestation"] = _sign_capability(
        config, {key: value for key, value in entry.items()
                 if key != "attestation"})
    _registry_add(config, entry)
    return {"state": "EXISTING_RUN_ENROLLED", "launch_id": entry["launch_id"],
            "run_dir": entry["run_dir"], "role": entry["role"],
            "task_id": entry["task_id"], "child_pid": entry["child_pid"],
            "migration": True}


def _operator_authorization(config: dict) -> tuple[dict, str]:
    path = config.get("_operator_auth")
    if not path or not Path(path).is_file():
        raise CurrentnessError("OPERATOR_AUTHORIZATION_UNAVAILABLE")
    authorization = read_json(Path(path))
    if not isinstance(authorization, dict):
        raise CurrentnessError("OPERATOR_AUTHORIZATION_SCHEMA")
    if authorization.get("schema") != OPERATOR_AUTH_SCHEMA:
        raise CurrentnessError("OPERATOR_AUTHORIZATION_SCHEMA")
    try:
        if _parse_utc(authorization["expires_at_utc"]) <= datetime.datetime.now(
                datetime.timezone.utc):
            raise CurrentnessError("OPERATOR_AUTHORIZATION_EXPIRED")
    except (KeyError, ValueError, TypeError) as exc:
        raise CurrentnessError("OPERATOR_AUTHORIZATION_EXPIRED") from exc
    return authorization, sha256_file(Path(path))


def _authorize_operator(config: dict, *, purpose: str, item: dict,
                        authorization_id: str | None,
                        allowed_roles: tuple[str, ...],
                        supersedes: str | None = None) -> tuple[dict, str]:
    authorization, authorization_sha = _operator_authorization(config)
    if not authorization_id or authorization.get("authorization_id") != authorization_id:
        raise CurrentnessError("OPERATOR_AUTHORIZATION_ID_MISMATCH")
    if purpose not in authorization.get("allowed_kinds", []):
        raise CurrentnessError("OPERATOR_AUTHORIZATION_KIND_DENIED", purpose)
    if authorization.get("role") not in allowed_roles:
        raise CurrentnessError("OPERATOR_AUTHORIZATION_ROLE_DENIED",
                               authorization.get("role"))
    scope = str(item.get("what_changed", ""))
    allowed_scopes = [str(value) for value in authorization.get("allowed_scopes", [])]
    if not any(scope.startswith(value) for value in allowed_scopes):
        raise CurrentnessError("OPERATOR_AUTHORIZATION_SCOPE_DENIED", scope)
    allowed_items = set(authorization.get("allowed_item_digests", []))
    allowed_sources = set(authorization.get("allowed_source_digests", []))
    if allowed_items or allowed_sources:
        source_digest = item.get("source_digest")
        if digest(item) not in allowed_items and source_digest not in allowed_sources:
            raise CurrentnessError("OPERATOR_AUTHORIZATION_EVIDENCE_DIGEST_DENIED")
    if supersedes is not None:
        if supersedes not in authorization.get("allowed_supersedes", []):
            raise CurrentnessError("OPERATOR_AUTHORIZATION_SUPERSEDES_DENIED")
    return authorization, authorization_sha


def _verify_mechanism_worker_return(config: dict, payload: dict,
                                      binding: dict) -> None:
    if payload.get("task_id") != MECHANISM_ID:
        raise CurrentnessError("MECHANISM_WORKER_TASK_MISMATCH")
    if payload.get("role") != "IMPLEMENTER":
        raise CurrentnessError("MECHANISM_WORKER_ROLE_MISMATCH")
    if not payload.get("session"):
        raise CurrentnessError("MECHANISM_WORKER_SESSION_MISSING")
    implementation = payload.get("implementation_commit")
    if not HASH_RE.fullmatch(str(implementation or "")):
        raise CurrentnessError("MECHANISM_WORKER_SOURCE_INVALID")
    runtime_path = "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py"
    test_path = "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py"
    result = subprocess.run(
        ["git", "-C", str(config["_root"]), "rev-parse",
         f"{implementation}:{runtime_path}"], capture_output=True, text=True)
    if result.returncode != 0 or result.stdout.strip() != payload.get("runtime_blob"):
        raise CurrentnessError("MECHANISM_WORKER_RUNTIME_BLOB_MISMATCH")
    result = subprocess.run(
        ["git", "-C", str(config["_root"]), "rev-parse",
         f"{implementation}:{test_path}"], capture_output=True, text=True)
    if result.returncode != 0 or result.stdout.strip() != payload.get("test_blob"):
        raise CurrentnessError("MECHANISM_WORKER_TEST_BLOB_MISMATCH")
    return_paths = payload.get("return_paths") or {}
    if not isinstance(return_paths, dict):
        raise CurrentnessError("MECHANISM_WORKER_RETURN_PATHS")
    worktree = Path(binding.get("worktree", "")).resolve()
    for rel, expected in return_paths.items():
        path = (worktree / rel).resolve()
        if worktree not in path.parents and path != worktree:
            raise CurrentnessError("MECHANISM_WORKER_RETURN_PATH_ESCAPE", rel)
        if not path.is_file() or sha256_file(path) != expected:
            raise CurrentnessError("MECHANISM_WORKER_RETURN_PATH_HASH", rel)


def _apply_review_verdict(state: dict, receipt: dict, validated: dict,
                          event_id: str, *, replay: bool) -> None:
    implementation = receipt.get("implementation_commit")
    if not HASH_RE.fullmatch(str(implementation or "")):
        raise CurrentnessError("REVIEW_IMPLEMENTATION_INVALID")
    if receipt["task_id"] == MECHANISM_ID:
        current = state["mechanism_review"].get("implementation_commit")
        if current and implementation != current:
            raise CurrentnessError("STALE_EVIDENCE", MECHANISM_ID)
        state["mechanism_review"].update({
            "state": ("ACCEPTED_SCOPED_PENDING_HQ_ADOPTION"
                      if receipt["verdict"].startswith("ACCEPT_SCOPED")
                      else "REVISE_EXACT_DEFECT"
                      if receipt["verdict"] == "REVISE_EXACT_DEFECT"
                      else "HOLD_SOURCE_AUTHORITY"),
            "implementation_commit": implementation,
            "verdict": receipt["verdict"],
            "reviewer_session": receipt.get("reviewer_session"),
            "review_commit": receipt.get("review_commit"),
            "review_scope": receipt.get("scope"),
            "review_receipt": validated["receipt"],
            "review_run": validated.get("review_run"),
            "verdict_artifact": validated.get("verdict_artifact"),
            "replay": replay,
        })
        state["mechanism_review_history"].append({
            "event_id": event_id, "implementation_commit": implementation,
            "verdict": receipt["verdict"],
            "reviewer_session": receipt.get("reviewer_session"),
            "review_commit": receipt.get("review_commit"),
            "review_run": validated.get("review_run"),
            "replay": replay,
        })
        if replay:
            state["baseline_replay"].append({
                "event_id": event_id, "task_id": MECHANISM_ID,
                "review_commit": receipt.get("review_commit"),
                "verdict": receipt["verdict"],
                "replay_is_not_new_review": True,
            })
        return
    task = _task_by_id(state, receipt["task_id"])
    if not replay and validated.get("review_run") is None:
        raise CurrentnessError("REVIEW_SUPERVISED_RUN_REQUIRED")
    if task.get("code_sha") and implementation != task["code_sha"]:
        raise CurrentnessError("STALE_EVIDENCE", receipt["task_id"])
    if receipt.get("review_commit") and not HASH_RE.fullmatch(receipt["review_commit"]):
        raise CurrentnessError("REVIEW_COMMIT_INVALID")
    verdict = receipt["verdict"]
    task["review_event_id"] = event_id
    task["review_receipt_sha256"] = validated["receipt_sha256"]
    task["review_commit"] = receipt.get("review_commit")
    task["review_scope"] = receipt.get("scope")
    task["review_trust"] = receipt.get("source_trust")
    task["review_run"] = validated.get("review_run")
    task["replay"] = replay
    if verdict.startswith("ACCEPT_SCOPED"):
        task["sourcefree_state"] = "SCOPED_RECEIVED_UNMERGED"
        task["execution_state"] = "SCOPED_RECEIVED_UNMERGED"
        task["review_sha"] = receipt.get("review_commit")
        task["review_pr"] = receipt.get("review_pr")
        task["code_sha"] = receipt.get("implementation_commit")
        task["protected_integration"] = "PENDING_PROTECTED_CI_AND_ADOPTION"
        task["adoption"] = "PENDING_PROTECTED_CI_AND_ADOPTION"
        task["protected_ci"] = receipt.get("protected_ci")
    elif verdict == "REVISE_EXACT_DEFECT":
        task["sourcefree_state"] = "REVISE_REQUIRED"
        task["execution_state"] = "REVISE_REQUIRED"
    else:
        task["sourcefree_state"] = "REJECTED" if verdict == "REJECTED" else "HELD_SOURCE_AUTHORITY"
        task["execution_state"] = task["sourcefree_state"]
    if replay:
        state["baseline_replay"].append({
            "event_id": event_id, "task_id": receipt["task_id"],
            "review_pr": receipt.get("review_pr"),
            "review_commit": receipt.get("review_commit"),
            "verdict": verdict,
            "replay_is_not_new_review": True,
        })


def apply_event(state: dict, event: dict, config: dict, contracts: tuple) -> dict:
    kind = event["kind"]
    source = event.get("source", {})
    payload = event.get("payload", {})
    if kind == "INIT":
        return state
    if kind in ("WORKER_RETURN", "INFRASTRUCTURE_RETURN"):
        task_id = payload.get("task_id")
        if source.get("controller_run_dir"):
            run = validate_controller_run(Path(source["controller_run_dir"]), source)
        else:
            raise CurrentnessError("CONTROLLER_RUN_REQUIRED")
        artifact = _verify_return_artifact(source, run["binding"])
        _require_trusted_launch(config, Path(source["controller_run_dir"]),
                                run, run["binding"])
        binding = run["binding"].get("sorok_currentness") or {}
        role = payload.get("role") or binding.get("role")
        expected_session = binding.get("expected_session")
        if expected_session and run["job"].get("session") != expected_session:
            raise CurrentnessError("CONTROLLER_EXPECTED_SESSION_MISMATCH")
        if role == "REJECTOR":
            if artifact["payload"].get("schema") != REJECTION_SCHEMA:
                raise CurrentnessError("REJECTION_ARTIFACT_SCHEMA")
            rejection = artifact["payload"]
            if rejection.get("task_id") != task_id:
                raise CurrentnessError("REJECTION_TASK_MISMATCH")
            expected_source = binding.get("expected_source_commit")
            if expected_source and rejection.get("implementation_commit") != expected_source:
                raise CurrentnessError("REJECTION_SOURCE_MISMATCH")
            rejection_event = {
                "schema": EVENT_SCHEMA,
                "event_id": "rejection-run:" + run["hashes"]["completion_sha256"],
                "kind": "REJECTION",
                "recorded_utc": now_utc(),
                "source": {"trust": "TRUSTED_CONTROLLER_REJECTION",
                           "controller_run_dir": run["run_dir"],
                           "completion_sha256": run["hashes"]["completion_sha256"]},
                "payload": {"task_id": task_id,
                            "implementation_commit": rejection.get(
                                "implementation_commit"),
                            "predecessor": rejection.get("predecessor"),
                            "reason": rejection.get("reason")},
            }
            apply_event(state, rejection_event, config, contracts)
        elif role == "PROTECTED_INTEGRATOR":
            if artifact["payload"].get("schema") != PROTECTED_INTEGRATION_SCHEMA:
                raise CurrentnessError("PROTECTED_INTEGRATION_ARTIFACT_SCHEMA")
            protected = artifact["payload"]
            if protected.get("task_id") != task_id:
                raise CurrentnessError("PROTECTED_INTEGRATION_TASK_MISMATCH")
            expected_source = binding.get("expected_source_commit")
            if expected_source and protected.get("source_commit") != expected_source:
                raise CurrentnessError("PROTECTED_INTEGRATION_SOURCE_MISMATCH")
            protected_event = {
                "schema": EVENT_SCHEMA,
                "event_id": "protected-run:" + run["hashes"]["completion_sha256"],
                "kind": "PROTECTED_INTEGRATION",
                "recorded_utc": now_utc(),
                "source": {"trust": "TRUSTED_CONTROLLER_PROTECTED_INTEGRATION",
                           "controller_run_dir": run["run_dir"],
                           "completion_sha256": run["hashes"]["completion_sha256"]},
                "payload": protected,
            }
            apply_event(state, protected_event, config, contracts)
        elif task_id == MECHANISM_ID:
            if role == "IMPLEMENTER":
                if artifact["payload"].get("schema") != RETURN_SCHEMA:
                    raise CurrentnessError("MECHANISM_WORKER_RETURN_SCHEMA")
                _verify_mechanism_worker_return(
                    config, artifact["payload"], run["binding"])
                implementation = artifact["payload"].get("implementation_commit")
                expected_source = binding.get("expected_source_commit")
                if expected_source and implementation != expected_source:
                    raise CurrentnessError("MECHANISM_WORKER_SOURCE_MISMATCH")
                state["mechanism_worker_return"] = {
                    "event_id": event["event_id"],
                    "controller_run_dir": run["run_dir"],
                    "job_id": run["job"]["job_id"],
                    "session": run["job"]["session"],
                    "grant_id": run["job"]["grant_id"],
                    "role": "IMPLEMENTER",
                    "exit_code": run["completion"]["exit_code"],
                    "return_path": artifact["path"],
                    "return_sha256": artifact["sha256"],
                    "implementation_commit": implementation,
                    "runtime_blob": artifact["payload"].get("runtime_blob"),
                    "test_blob": artifact["payload"].get("test_blob"),
                    "execution_state": "RETURNED_REVIEW_PENDING",
                    "review_required": True,
                    "completion_sha256": run["hashes"]["completion_sha256"],
                }
                review = state["mechanism_review"]
                if review.get("implementation_commit") != implementation:
                    review.update({
                        "state": "PENDING_EXTERNAL_NONAUTHOR_REVIEW",
                        "implementation_commit": implementation,
                        "verdict": None,
                        "reviewer_session": None,
                        "review_commit": None,
                        "review_scope": None,
                        "review_receipt": None,
                        "review_run": None,
                        "verdict_artifact": None,
                        "replay": False,
                    })
                else:
                    review["implementation_commit"] = implementation
                state["controller_integration"]["hook_state"] = (
                    "REAL_MECHANISM_WORKER_RETURN_INTAKEN")
            elif role == "REVIEWER":
                if artifact["payload"].get("schema") != REVIEW_RECEIPT_SCHEMA:
                    raise CurrentnessError("MECHANISM_REVIEW_RECEIPT_SCHEMA")
                review_source = dict(source)
                review_source["trust"] = "REAL_LOCAL_SUPERVISED_REVIEW_RUN"
                review_source["review_run_dir"] = run["run_dir"]
                validated = _validate_review_receipt(
                    config, artifact["payload"], replay=False,
                    source=review_source)
                _apply_review_verdict(
                    state, artifact["payload"], validated,
                    event["event_id"], replay=False)
                state["controller_integration"]["hook_state"] = (
                    "REAL_MECHANISM_REVIEW_INTAKEN")
            else:
                raise CurrentnessError("MECHANISM_ROLE_UNKNOWN", role)
        elif task_id in EXPECTED_IDS:
            if role not in (None, "IMPLEMENTER"):
                raise CurrentnessError("TASK_RETURN_ROLE_MISMATCH", role)
            task = _task_by_id(state, task_id)
            if task.get("code_sha") and payload.get("source_commit") != task["code_sha"]:
                raise CurrentnessError("STALE_EVIDENCE", task_id)
            task["execution_state"] = "RETURNED_REVIEW_PENDING"
            task["return_event_id"] = event["event_id"]
            task["return_source_commit"] = payload.get("source_commit")
            task["return_artifact_sha256"] = artifact["sha256"]
            task["return_controller_run"] = run["run_dir"]
        else:
            state["infrastructure_qualification"].append({
                "event_id": event["event_id"],
                "scope": payload.get("scope", "INFRASTRUCTURE_QUALIFICATION"),
                "controller_run_dir": run["run_dir"],
                "job_id": run["job"]["job_id"],
                "session": run["job"]["session"],
                "exit_code": run["completion"]["exit_code"],
                "return_path": artifact["path"],
                "return_sha256": artifact["sha256"],
                "execution_state": "RETURNED_REVIEW_PENDING",
                "review_required": True,
            })
        state["authenticated_checkpoint"]["local_receipts"][run["hashes"]["completion_sha256"]] = {
            "event_id": event["event_id"], "job_id": run["job"]["job_id"],
            "session": run["job"]["session"],
        }
        return state
    if kind == "REVIEW_VERDICT":
        receipt = event.get("receipt")
        if not isinstance(receipt, dict):
            raise CurrentnessError("REVIEW_RECEIPT_MISSING")
        replay = source.get("trust") == "IMMUTABLE_HISTORICAL_INDEPENDENT_REVIEW_REPLAY"
        validated = _validate_review_receipt(
            config, receipt, replay=replay, source=source)
        _apply_review_verdict(state, receipt, validated, event["event_id"],
                              replay=replay)
        return state
    if kind == "REJECTION":
        if source.get("trust") != "TRUSTED_CONTROLLER_REJECTION":
            raise CurrentnessError("UNTRUSTED_REJECTION_SOURCE")
        task = _task_by_id(state, payload["task_id"])
        implementation = payload.get("implementation_commit")
        if not HASH_RE.fullmatch(str(implementation or "")):
            raise CurrentnessError("REJECTION_SOURCE_INVALID")
        if task.get("code_sha") and implementation != task["code_sha"]:
            raise CurrentnessError("REJECTION_SOURCE_MISMATCH")
        if not payload.get("predecessor"):
            raise CurrentnessError("REJECTION_PREDECESSOR_REQUIRED")
        task["sourcefree_state"] = "REJECTED"
        task["execution_state"] = "REJECTED"
        task["rejection_event_id"] = event["event_id"]
        task["rejection_source_commit"] = implementation
        task["rejection_predecessor"] = payload.get("predecessor")
        task["claim_ready"] = False
        return state
    if kind == "PROTECTED_INTEGRATION":
        if source.get("trust") != "TRUSTED_CONTROLLER_PROTECTED_INTEGRATION":
            raise CurrentnessError("UNTRUSTED_PROTECTED_INTEGRATION_SOURCE")
        target = payload.get("task_id")
        source_commit = payload.get("source_commit")
        merge_sha = payload.get("merge_sha")
        if not HASH_RE.fullmatch(str(source_commit or "")):
            raise CurrentnessError("PROTECTED_SOURCE_INVALID")
        if not HASH_RE.fullmatch(str(merge_sha or "")):
            raise CurrentnessError("PROTECTED_MERGE_INVALID")
        lineage = subprocess.run(
            ["git", "-C", str(config["_root"]), "show", "-s", "--format=%P",
             merge_sha], capture_output=True, text=True)
        parents = lineage.stdout.split()
        if lineage.returncode != 0 or len(parents) != 2 or parents[1] != source_commit:
            raise CurrentnessError("PROTECTED_MERGE_LINEAGE_INVALID")
        live = state.get("authenticated_checkpoint", {}).get("live_github")
        ci_observed = False
        if payload.get("ci_state") == "PASS" and _live_fresh(state, live):
            checks = ((live.get("api") or {}).get("checks") or {})
            observed = checks.get(merge_sha) or {}
            ci_observed = (
                observed.get("conclusion") == "success"
                and payload.get("ci_observation_digest") == live.get("evidence_digest"))
        if target in EXPECTED_IDS:
            task = _task_by_id(state, target)
            if task.get("code_sha") and source_commit != task["code_sha"]:
                raise CurrentnessError("PROTECTED_SOURCE_MISMATCH")
            task["protected_merge_sha"] = merge_sha
            task["protected_source_commit"] = source_commit
            if ci_observed:
                task["protected_integration"] = "PROTECTED_SOURCEFREE"
                task["protected_ci"] = "PASS"
            else:
                task["protected_integration"] = "PENDING_PROTECTED_CI_AND_ADOPTION"
                task["protected_ci"] = "UNAVAILABLE_BILLING"
                state["controls"]["holds"].append({
                    "scope": task["id"],
                    "owner": payload.get("owner", "protected CI owner"),
                    "reason": "PROTECTED_CI_UNAVAILABLE_OR_UNVERIFIED",
                    "event_id": event["event_id"],
                })
        elif target in state.get("protected_foundations", {}):
            foundation = state["protected_foundations"][target]
            if merge_sha != foundation.get("merge_sha"):
                raise CurrentnessError("PROTECTED_FOUNDATION_MERGE_MISMATCH")
            state.setdefault("protected_integration_requests", []).append({
                "task_id": target, "merge_sha": merge_sha,
                "source_commit": source_commit,
                "state": ("PROTECTED_SOURCEFREE" if ci_observed
                          else "PENDING_PROTECTED_CI_AND_ADOPTION"),
                "protected_ci": "PASS" if ci_observed else "UNAVAILABLE_BILLING",
                "event_id": event["event_id"],
            })
        else:
            raise CurrentnessError("PROTECTED_TARGET_UNKNOWN", target)
        return state
    if kind == "RESTORATION":
        scope = payload.get("scope")
        if not scope:
            raise CurrentnessError("CONTROL_SCOPE_MISSING")
        target = payload.get("restores")
        if not target:
            raise CurrentnessError("RESTORATION_TARGET_REQUIRED")
        revocation = next((row for row in state["controls"].get("revocations", [])
                           if row.get("event_id") == target), None)
        if revocation is None:
            raise CurrentnessError("RESTORATION_TARGET_NOT_FOUND")
        if revocation.get("scope") != scope:
            raise CurrentnessError("RESTORATION_SCOPE_MISMATCH")
        item = {"what_changed": "RESTORATION " + str(scope),
                "scope": scope,
                "source_digest": digest({
                    "kind": kind, "scope": scope,
                    "event_id": event.get("event_id"),
                    "recorded_utc": event.get("recorded_utc"),
                    "payload": payload})}
        authorization, authorization_sha = _authorize_operator(
            config, purpose="RESTORATION", item=item,
            authorization_id=payload.get("authorization_id"),
            allowed_roles=("SOROK_HQ_OPERATOR", "SOURCE_AUTHORITY_ISSUER"))
        if _parse_utc(event["recorded_utc"]) <= _parse_utc(
                revocation.get("recorded_at", "1970-01-01T00:00:00+00:00")):
            raise CurrentnessError("RESTORATION_ORDER")
        state["controls"]["revocations"] = [
            row for row in state["controls"]["revocations"]
            if row.get("event_id") != target]
        state["controls"].setdefault("restorations", []).append({
            "scope": scope, "event_id": event["event_id"],
            "restores": target, "authorization_id": authorization.get(
                "authorization_id"), "authorization_sha256": authorization_sha,
            "recorded_at": event["recorded_utc"],
        })
        return state
    if kind in ("SOURCE_AUTHORITY_HOLD", "USER_STOP", "REVOCATION", "USER_RESUME"):
        scope = payload.get("scope")
        if not scope:
            raise CurrentnessError("CONTROL_SCOPE_MISSING")
        item = {"what_changed": kind + " " + str(scope), "scope": scope,
                "source_digest": digest({
                    "kind": kind, "scope": scope,
                    "event_id": event.get("event_id"),
                    "recorded_utc": event.get("recorded_utc"),
                    "payload": payload})}
        roles = {
            "SOURCE_AUTHORITY_HOLD": ("SOURCE_AUTHORITY_ISSUER",),
            "USER_STOP": ("SOROK_HQ_OPERATOR",),
            "USER_RESUME": ("SOROK_HQ_OPERATOR",),
            "REVOCATION": ("SOROK_HQ_OPERATOR", "SOURCE_AUTHORITY_ISSUER"),
        }[kind]
        authorization, authorization_sha = _authorize_operator(
            config, purpose=kind, item=item,
            authorization_id=payload.get("authorization_id"),
            allowed_roles=roles, supersedes=payload.get("supersedes"))
        if kind == "USER_RESUME":
            target = payload.get("supersedes")
            if not target:
                raise CurrentnessError("UNAUTHORIZED_RESUME_SUPERSEDES_REQUIRED")
            stop = next((row for row in state["controls"]["stops"]
                         if row.get("event_id") == target), None)
            if stop is None:
                raise CurrentnessError("UNAUTHORIZED_RESUME_TARGET_NOT_FOUND")
            if stop.get("scope") != scope:
                raise CurrentnessError("UNAUTHORIZED_RESUME_SCOPE_MISMATCH")
            if _parse_utc(event["recorded_utc"]) <= _parse_utc(stop["recorded_at"]):
                raise CurrentnessError("UNAUTHORIZED_RESUME_ORDER")
            state["controls"]["stops"] = [
                row for row in state["controls"]["stops"]
                if row.get("event_id") != target]
            state["controls"].setdefault("resumes", []).append({
                "scope": scope, "event_id": event["event_id"],
                "supersedes": target, "authorization_id": authorization.get(
                    "authorization_id"), "authorization_sha256": authorization_sha,
            })
            return state
        key = {"SOURCE_AUTHORITY_HOLD": "holds", "USER_STOP": "stops",
               "REVOCATION": "revocations"}[kind]
        state["controls"].setdefault(key, []).append({
            "scope": scope, "owner": authorization.get("owner", payload.get("owner")),
            "reason": payload.get("reason", kind), "event_id": event["event_id"],
            "recorded_at": event["recorded_utc"],
            "authorization_id": authorization.get("authorization_id"),
            "authorization_sha256": authorization_sha,
        })
        return state
    if kind == "HISTORICAL_REVIEW":
        receipt = payload.get("receipt")
        if not isinstance(receipt, dict):
            raise CurrentnessError("HISTORICAL_REVIEW_RECEIPT_MISSING")
        if source.get("trust") != "POSTHOC_REGISTERED_REAL_REVIEWER_RUN":
            raise CurrentnessError("HISTORICAL_REVIEW_TRUST_REQUIRED")
        run_dir = source.get("controller_run_dir")
        if not run_dir:
            raise CurrentnessError("HISTORICAL_REVIEW_RUN_REQUIRED")
        run = validate_controller_run(Path(run_dir), source)
        if run["completion"].get("exit_code") != 0:
            raise CurrentnessError("HISTORICAL_REVIEW_ZERO_EXIT_REQUIRED")
        if receipt.get("reviewer_session") == receipt.get("author_session"):
            raise CurrentnessError("SELF_REVIEW_REFUSED")
        if receipt.get("verdict") != payload.get("verdict"):
            raise CurrentnessError("HISTORICAL_REVIEW_VERDICT_MISMATCH")
        verified = verify_git_documents(
            config["_root"], receipt.get("review_commit"),
            receipt.get("source_documents") or [])
        record = {
            "event_id": event["event_id"], "historical": True,
            "automatic_intake": False,
            "posthoc_registration": True,
            "controller_run_dir": run["run_dir"],
            "job_id": run["job"]["job_id"],
            "session": run["job"]["session"],
            "completion_sha256": run["hashes"]["completion_sha256"],
            "implementation_commit": receipt.get("implementation_commit"),
            "reviewer_session": receipt.get("reviewer_session"),
            "review_commit": receipt.get("review_commit"),
            "verdict": receipt.get("verdict"),
            "verified_documents": verified,
        }
        state["mechanism_review_history"].append(record)
        state["mechanism_review_original"] = record
        return state
    if kind == "GITHUB_OBSERVATION":
        live = payload.get("live_observation")
        if not isinstance(live, dict) or live.get("schema") != LIVE_GITHUB_SCHEMA:
            raise CurrentnessError("LIVE_GITHUB_OBSERVATION_SCHEMA")
        if source.get("trust") != "RUNTIME_INTERNAL_LIVE_FETCH":
            raise CurrentnessError("LIVE_GITHUB_OBSERVATION_UNTRUSTED_SOURCE")
        if source.get("observation_digest") != live.get("evidence_digest"):
            raise CurrentnessError("LIVE_GITHUB_OBSERVATION_DIGEST_MISMATCH")
        if not _live_fresh(state, live):
            raise CurrentnessError("LIVE_GITHUB_OBSERVATION_STALE_OR_UNTRUSTED")
        state["authenticated_checkpoint"]["live_github"] = copy.deepcopy(live)
        state["authenticated_checkpoint"]["last_authenticated_at_utc"] = (
            live.get("fetched_at_utc"))
        state["authenticated_checkpoint"]["legacy_baseline_not_live"] = True
        state["authenticated_checkpoint"]["github_observations"] = {
            "live:" + str(live.get("evidence_digest")): {
                "source_trust": live.get("source_trust"),
                "fetched_at_utc": live.get("fetched_at_utc"),
                "expires_at_utc": live.get("expires_at_utc"),
                "status_coverage": live.get("status_coverage"),
            }}
        state["reconciliation_required"] = [
            item for item in state.get("reconciliation_required", [])
            if item.get("source_kind") != "LIVE_GITHUB"]
        return state
    if kind == "RECONCILIATION_RESOLVED":
        what = payload.get("what_changed")
        if not what:
            raise CurrentnessError("RECONCILIATION_RESOLUTION_INCOMPLETE")
        match = next((row for row in state.get("reconciliation_required", [])
                      if row.get("what_changed") == what), None)
        if match is None:
            raise CurrentnessError("RECONCILIATION_ITEM_NOT_FOUND", what)
        item_digest = digest(match)
        resolution_key = digest({
            "what_changed": what,
            "source_kind": match.get("source_kind"),
            "source_digest": match.get("source_digest"),
        })
        resolution = {
            "what_changed": what, "item_digest": item_digest,
            "resolution_key": resolution_key,
            "source_digest": match.get("source_digest"),
            "checkpoint_id": state.get("checkpoint_id"),
            "event_id": event["event_id"], "recorded_at": event["recorded_utc"],
        }
        if payload.get("fresh_observation_digest"):
            live = state.get("authenticated_checkpoint", {}).get("live_github")
            if (not _live_fresh(state, live)
                    or live.get("evidence_digest") != payload["fresh_observation_digest"]
                    or match.get("source_kind") != "LIVE_GITHUB"):
                raise CurrentnessError("RESOLUTION_FRESH_OBSERVATION_INVALID")
            resolution.update({
                "resolution_state": "RESOLVED_BY_FRESH_LIVE_OBSERVATION",
                "evidence_digest": live.get("evidence_digest"),
                "fetched_at_utc": live.get("fetched_at_utc"),
            })
            state["reconciliation_required"] = [
                row for row in state["reconciliation_required"]
                if row.get("what_changed") != what]
        elif payload.get("source_hold_authorization_id"):
            authorization, authorization_sha = _authorize_operator(
                config, purpose="SOURCE_AUTHORITY_HOLD", item=match,
                authorization_id=payload.get("source_hold_authorization_id"),
                allowed_roles=("SOURCE_AUTHORITY_ISSUER",))
            match["held_by_source_authority"] = True
            match["held_at_utc"] = event["recorded_utc"]
            match["source_hold_authorization_id"] = authorization.get(
                "authorization_id")
            state.setdefault("source_authority_holds", []).append({
                "what_changed": what, "authorization_id": authorization.get(
                    "authorization_id"), "authorization_sha256": authorization_sha,
                "held_at_utc": event["recorded_utc"],
            })
            resolution.update({
                "resolution_state": "HELD_BY_COMPETENT_SOURCE_AUTHORITY",
                "authorization_id": authorization.get("authorization_id"),
                "authorization_sha256": authorization_sha,
            })
        elif payload.get("operator_authorization_id"):
            authorization, authorization_sha = _authorize_operator(
                config, purpose="RECONCILIATION_RESOLUTION", item=match,
                authorization_id=payload.get("operator_authorization_id"),
                allowed_roles=("SOROK_HQ_OPERATOR",))
            resolution.update({
                "resolution_state": "RESOLVED_BY_COMPETENT_OPERATOR_EVIDENCE",
                "authorization_id": authorization.get("authorization_id"),
                "authorization_sha256": authorization_sha,
            })
            state["reconciliation_required"] = [
                row for row in state["reconciliation_required"]
                if row.get("what_changed") != what]
        else:
            raise CurrentnessError("RESOLUTION_AUTHENTICATION_REQUIRED")
        state.setdefault("reconciliation_resolved", []).append(resolution)
        return state
    if kind == "RECONCILIATION_REQUIRED":
        item = payload.get("item")
        if not isinstance(item, dict) or not item.get("what_changed"):
            raise CurrentnessError("RECONCILIATION_ITEM_INVALID")
        if item not in state["reconciliation_required"]:
            state["reconciliation_required"].append(item)
        return state
    if kind == "GITHUB_PUBLICATION":
        return state
    raise CurrentnessError("EVENT_KIND_UNKNOWN", kind)


CONTROL_EVENT_KINDS = frozenset({
    "USER_STOP", "USER_RESUME", "REVOCATION", "RESTORATION",
    "SOURCE_AUTHORITY_HOLD",
})


def intake_control_event(config: dict, event: dict) -> dict:
    if event.get("kind") not in CONTROL_EVENT_KINDS:
        raise CurrentnessError("PUBLIC_EVENT_INTAKE_DISABLED",
                               str(event.get("kind")))
    return intake_event(config, event, trusted=True)


def intake_event(config: dict, event: dict, *, trusted: bool = False) -> dict:
    if not trusted:
        kind = event.get("kind")
        if kind in ("USER_STOP", "USER_RESUME", "REVOCATION", "RESTORATION",
                    "SOURCE_AUTHORITY_HOLD"):
            raise CurrentnessError("OPERATOR_AUTHORIZATION_UNAVAILABLE")
        if kind == "REJECTION":
            raise CurrentnessError("UNTRUSTED_REJECTION_SOURCE")
        if kind == "PROTECTED_INTEGRATION":
            raise CurrentnessError("UNTRUSTED_PROTECTED_INTEGRATION_SOURCE")
        if kind == "GITHUB_OBSERVATION":
            raise CurrentnessError("LIVE_GITHUB_OBSERVATION_UNTRUSTED_SOURCE")
        if kind in ("REVIEW_VERDICT", "WORKER_RETURN", "INFRASTRUCTURE_RETURN"):
            raise CurrentnessError("TRUSTED_CONTROLLER_RUN_REQUIRED")
        raise CurrentnessError("PUBLIC_EVENT_INTAKE_DISABLED")
    with _lock(config, True):
        whole = read_json(config["_pair_json"])
        md = config["_pair_md"].read_text(encoding="utf-8")
        state = whole.get(RUNTIME_KEY)
        if not isinstance(state, dict):
            raise CurrentnessError("RUNTIME_NOT_INITIALIZED")
        errors = validate_pair(whole, md)
        if errors:
            raise CurrentnessError("PAIRED_MD_JSON_MIXED_GENERATION", errors)
        if event.get("schema") != EVENT_SCHEMA:
            raise CurrentnessError("EVENT_SCHEMA")
        if not event.get("event_id") or not event.get("kind"):
            raise CurrentnessError("EVENT_ID_OR_KIND_MISSING")
        event = copy.deepcopy(event)
        event.pop("event_hash", None)
        event.pop("previous_event_hash", None)
        event_hash = _event_hash(event)
        duplicate = _find_duplicate(state, event["event_id"], event_hash)
        if duplicate is not None:
            return {"state": "DUPLICATE_EVENT", "event_id": duplicate["event_id"],
                    "event_hash": duplicate["event_hash"], "generation": state["generation"]}
        expected = (state["events"][-1]["sequence"] + 1) if state.get("events") else 1
        if event.get("sequence") is not None and event["sequence"] != expected:
            raise CurrentnessError("OUT_OF_ORDER_EVENT",
                                   {"expected": expected, "got": event["sequence"]})
        event["sequence"] = expected
        last = _last_event(state)
        event["event_hash"] = event_hash
        event["previous_event_hash"] = last["event_hash"] if last else None
        apply_event(state, event, config, frozen_contracts(config))
        state["events"].append(event)
        state["generation"] += 1
        state["updated_utc"] = now_utc()
        recompute(state)
        commit_state(config, whole, md, state)
        return {"state": "EVENT_RECORDED", "event_id": event["event_id"],
                "event_hash": event_hash, "generation": state["generation"],
                "checkpoint_id": state["checkpoint_id"]}


def migrate_state(config: dict, state: dict) -> None:
    packet, gmt, gmt_index = frozen_contracts(config)
    state.setdefault("authenticated_checkpoint", {}).setdefault("live_github", None)
    state["authenticated_checkpoint"].setdefault("legacy_baseline_not_live", True)
    state.setdefault("mechanism_worker_return", None)
    state.setdefault("mechanism_review_history", [])
    state.setdefault("mechanism_review_original", None)
    state.setdefault("reconciliation_resolved", [])
    state.setdefault("source_authority_holds", [])
    state.setdefault("decision_nodes", [])
    state.setdefault("decision_readiness", [])
    state.setdefault("frozen_projection_adoption",
                     (state.get("frozen_projection") or {}).get(
                         "adoption", "PENDING_INDEPENDENT_RECEIVING"))
    review = state.setdefault("mechanism_review", {})
    review.setdefault("review_run", None)
    review.setdefault("verdict_artifact", None)
    review.setdefault("verdict", None)
    source_freeze = state.setdefault("source_freeze", {})
    source_freeze.setdefault("operational_gmt_atlas", {
        "commit": GMT_ATLAS_COMMIT, "path": GMT_ATLAS_PATH,
        "blob": None,
        "status": "DRAFT_DOCUMENTARY_CANDIDATE_NOT_PROTECTED_LAW"})
    source_freeze.setdefault("oath_r2", {
        "commit": "1341c81dfe0e99da030e7dca356f55789a10c6f8",
        "status": "DRAFT_PR1098_NOT_PROTECTED_LAW"})
    if not state["decision_nodes"]:
        for node in gmt.get("decision_nodes", []):
            decision = copy.deepcopy(node)
            decision["full_original_claim"] = "NOT_ESTABLISHED"
            state["decision_nodes"].append(decision)
    for task in state.get("tasks", []):
        overlay = gmt_index.get(task.get("id"), {})
        task.setdefault("decision_prerequisites", list(overlay.get(
            "hard_prerequisites_to_expand_beyond_existing_fixture", [])))
        task.setdefault("decision_full_claim", list(overlay.get(
            "determinations_required_before_full_capability_claim", [])))
        task.setdefault("bounded_engineering_now",
                        overlay.get("safe_bounded_engineering_now"))
        task.setdefault("claims_not_yet_warranted",
                        overlay.get("claims_not_yet_warranted"))
        task.setdefault("decision_issue_ids", list(overlay.get("issue_ids", [])))
    recompute(state)


def _render_runtime_block(state: dict) -> str:
    lines = [
        START,
        "## SOROK automatic currentness — runtime reconciled",
        f"<!-- SOROK_RUNTIME_GENERATION: {state['generation']} -->",
        f"**Generation:** {state['generation']} | **Checkpoint:** `{state['checkpoint_id']}`"
        f" | **Updated:** {state['updated_utc']}",
        "**Frozen #1095 projection:** preserved as historical candidate; it is not rewritten as live intake.",
        f"**Runtime adoption:** {state.get('adoption')} | **Protected CI:** {state.get('protected_ci')}",
    ]
    baseline = state.get("authenticated_checkpoint", {}).get("baseline")
    if baseline:
        lines.append(f"**Authenticated GitHub checkpoint:** `{baseline.get('sha256')}`"
                     f" ({baseline.get('as_of')})")
    else:
        lines.append("**Authenticated GitHub checkpoint:** UNAVAILABLE — RECONCILIATION_REQUIRED")
    ready = state["readiness"].get("ready_for_independent_receiving", [])
    scoped = state["readiness"].get("ready_for_scoped_engineering", [])
    lines.append("**Ready for independent receiving:** " +
                 (", ".join(ready) if ready else "NONE"))
    lines.append("**Ready for scoped engineering:** " +
                 (", ".join(scoped) if scoped else "NONE"))
    awaiting = state["readiness"].get("awaiting_independent_receiving", [])
    lines.append("**Awaiting independent receiving:** " +
                 (", ".join(awaiting) if awaiting else "NONE"))
    lines.append("**Holds and source-authority boundaries:**")
    for hold in state.get("holds", []):
        lines.append(f"- {hold.get('kind')} | {hold.get('scope')} | owner: "
                     f"{hold.get('owner')} | {hold.get('reason')}")
    lines.append("**Reconciliation required:**")
    if state.get("reconciliation_required"):
        for item in state["reconciliation_required"]:
            lines.append(f"- {item.get('what_changed')} | expected: "
                         f"{item.get('expected_evidence')} | owner: {item.get('owner')}"
                         f" | next: {item.get('next_action')}")
    else:
        lines.append("- NONE at this authenticated checkpoint.")
    infra = state.get("infrastructure_qualification") or []
    lines.append(f"**Real controller infrastructure returns:** {len(infra)}"
                 " (review pending, not task acceptance)")
    replay = state.get("baseline_replay") or []
    lines.append(f"**Immutable historical review replays:** {len(replay)}"
                 " (explicit replay, not new review)")
    lines.append(f"**Next non-dispatch action:** {json.dumps(state.get('recommended_next'), sort_keys=True)}")
    lines.append("**No automatic job dispatch.** Engineering, original-task completion, "
                 "protected integration, scientific authority and execution state remain separate.")
    lines.append(END)
    return "\n".join(lines)


def _extract_block(md: str, start: str, end: str) -> str | None:
    if md.count(start) != 1 or md.count(end) != 1:
        return None
    left = md.index(start)
    right = md.index(end) + len(end)
    return md[left:right]


def _replace_runtime_block(md: str, block: str) -> str:
    existing = _extract_block(md, START, END)
    if existing is not None:
        return md.replace(existing, block, 1)
    frozen = _extract_block(md, FROZEN_START, FROZEN_END)
    if frozen is None:
        raise CurrentnessError("FROZEN_MD_BLOCK_MISSING")
    index = md.index(frozen) + len(frozen)
    return md[:index] + "\n\n" + block + md[index:]


def _verify_frozen_md(whole: dict, md: str) -> list[str]:
    errors = []
    frozen = whole.get(FROZEN_KEY)
    block = _extract_block(md, FROZEN_START, FROZEN_END)
    if block is None:
        errors.append("FROZEN_MD_BLOCK_MISSING")
    state = whole.get(RUNTIME_KEY)
    if isinstance(state, dict):
        expected = state.get("source_freeze", {}).get("frozen_md_block_sha256")
        if expected and block and sha256_bytes(block.encode()) != expected:
            errors.append("FROZEN_MD_BLOCK_MUTATED")
    if isinstance(frozen, dict):
        state_digest = (state or {}).get("source_freeze", {}).get(
            "frozen_projection_sha256")
        if state_digest and digest(frozen) != state_digest:
            errors.append("FROZEN_JSON_PROJECTION_MUTATED")
    return errors


def validate_pair(whole: dict, md: str) -> list[str]:
    errors = _verify_frozen_md(whole, md)
    state = whole.get(RUNTIME_KEY)
    if not isinstance(state, dict):
        return errors + ["RUNTIME_STATE_MISSING"]
    if state.get("schema") != SCHEMA:
        errors.append("RUNTIME_SCHEMA")
    if state.get("pair", {}).get("generation") != state.get("generation"):
        errors.append("PAIR_GENERATION_MISMATCH")
    if state.get("pair", {}).get("checkpoint_id") != state.get("checkpoint_id"):
        errors.append("PAIR_CHECKPOINT_MISMATCH")
    block = _extract_block(md, START, END)
    if block is None:
        errors.append("RUNTIME_MD_BLOCK_MISSING")
        return errors
    marker = f"<!-- SOROK_RUNTIME_GENERATION: {state.get('generation')} -->"
    if marker not in block:
        errors.append("RUNTIME_MD_GENERATION_MISMATCH")
    try:
        if block.strip() != _render_runtime_block(state).strip():
            errors.append("PAIRED_MD_JSON_DRIFT")
    except (KeyError, TypeError) as exc:
        errors.append("RUNTIME_RENDER_ERROR " + str(exc))
    return errors


def _journal_append(config: dict, record: dict) -> None:
    path = config["_state_root"] / "journal.jsonl"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(canonical(record) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def commit_state(config: dict, whole: dict, md: str, state: dict) -> None:
    block = _render_runtime_block(state)
    frozen_block = _extract_block(md, FROZEN_START, FROZEN_END)
    if state["source_freeze"].get("frozen_md_block_sha256") is None and frozen_block:
        state["source_freeze"]["frozen_md_block_sha256"] = sha256_bytes(
            frozen_block.encode())
    new_md = _replace_runtime_block(md, block)
    whole[RUNTIME_KEY] = state
    new_json = json.dumps(whole, indent=2, ensure_ascii=False) + "\n"
    transaction = "txn-" + digest({"generation": state["generation"],
                                   "checkpoint": state["checkpoint_id"],
                                   "json": sha256_bytes(new_json.encode()),
                                   "md": sha256_bytes(new_md.encode())})[:24]
    pending = config["_state_root"] / "pending"
    pending.mkdir(parents=True, exist_ok=True)
    pending_json = pending / (transaction + ".json")
    pending_md = pending / (transaction + ".md")
    pending_json.write_text(new_json, encoding="utf-8")
    pending_md.write_text(new_md, encoding="utf-8")
    for path in (pending_json, pending_md):
        with path.open("rb") as handle:
            os.fsync(handle.fileno())
    record = {
        "transaction": transaction, "generation": state["generation"],
        "checkpoint_id": state["checkpoint_id"],
        "json_path": str(config["_pair_json"]), "md_path": str(config["_pair_md"]),
        "pending_json": str(pending_json), "pending_md": str(pending_md),
        "json_sha256": sha256_bytes(new_json.encode()),
        "md_sha256": sha256_bytes(new_md.encode()),
        "state": "PREPARED", "at_utc": now_utc(),
    }
    _journal_append(config, record)
    write_text_atomic(config["_pair_json"], new_json)
    write_text_atomic(config["_pair_md"], new_md)
    check = json.loads(config["_pair_json"].read_text(encoding="utf-8"))
    check_md = config["_pair_md"].read_text(encoding="utf-8")
    errors = validate_pair(check, check_md)
    if errors:
        raise CurrentnessError("COMMIT_PAIR_VALIDATION_FAILED", errors)
    _journal_append(config, {**record, "state": "COMMITTED", "committed_at_utc": now_utc()})


def recover(config: dict) -> dict:
    with _lock(config, True):
        return _recover_locked(config)


def _recover_locked(config: dict) -> dict:
    journal = config["_state_root"] / "journal.jsonl"
    if not journal.is_file():
        return {"state": "NO_JOURNAL"}
    rows = []
    for line in journal.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    committed = {row["transaction"] for row in rows if row.get("state") == "COMMITTED"}
    pending = [row for row in rows if row.get("state") == "PREPARED"
               and row["transaction"] not in committed]
    if not pending:
        return {"state": "NO_PENDING_TRANSACTION"}
    transaction = pending[-1]
    pending_json = Path(transaction["pending_json"])
    pending_md = Path(transaction["pending_md"])
    if not pending_json.is_file() or not pending_md.is_file():
        return {"state": "RECONCILIATION_REQUIRED",
                "reason": "PENDING_TRANSACTION_PAYLOAD_MISSING"}
    json_text = pending_json.read_text(encoding="utf-8")
    md_text = pending_md.read_text(encoding="utf-8")
    if sha256_bytes(json_text.encode()) != transaction["json_sha256"]:
        return {"state": "RECONCILIATION_REQUIRED",
                "reason": "PENDING_JSON_HASH_MISMATCH"}
    if sha256_bytes(md_text.encode()) != transaction["md_sha256"]:
        return {"state": "RECONCILIATION_REQUIRED",
                "reason": "PENDING_MD_HASH_MISMATCH"}
    write_text_atomic(Path(transaction["json_path"]), json_text)
    write_text_atomic(Path(transaction["md_path"]), md_text)
    _journal_append(config, {**transaction, "state": "COMMITTED",
                             "recovered_at_utc": now_utc()})
    return {"state": "RECOVERED", "transaction": transaction["transaction"],
            "generation": transaction["generation"]}


def read_pair(config: dict) -> tuple[dict, str, dict]:
    recover(config)
    with _lock(config, False):
        whole = read_json(config["_pair_json"])
        md = config["_pair_md"].read_text(encoding="utf-8")
        errors = validate_pair(whole, md)
        if errors:
            raise CurrentnessError("PAIRED_MD_JSON_MIXED_GENERATION", errors)
        return whole, md, whole[RUNTIME_KEY]


def _baseline_rows(config: dict) -> list[dict]:
    baseline = config.get("_baseline")
    if not baseline or not Path(baseline).is_file():
        raise CurrentnessError("AUTHENTICATED_GITHUB_INTAKE_UNAVAILABLE")
    data = read_json(Path(baseline))
    if not isinstance(data, list):
        raise CurrentnessError("GITHUB_BASELINE_SCHEMA")
    return data


def _parse_utc(value: str):
    return datetime.datetime.fromisoformat(str(value).replace("Z", "+00:00"))


def _utc_add(seconds: int) -> str:
    return (datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(seconds=seconds)).isoformat()


def _git_credential_token() -> tuple[str | None, str | None]:
    """Use the existing git credential helper in memory; never log the secret."""
    try:
        completed = subprocess.run(
            ["git", "credential", "fill"],
            input="protocol=https\nhost=github.com\n\n",
            capture_output=True, text=True, timeout=15)
    except (OSError, subprocess.TimeoutExpired):
        return None, "GIT_CREDENTIAL_HELPER_UNAVAILABLE"
    if completed.returncode != 0:
        return None, "GIT_CREDENTIAL_HELPER_REFUSED"
    values = {}
    for line in completed.stdout.splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            values[key] = value
    token = values.get("password")
    return (token, None) if token else (None, "GIT_CREDENTIAL_TOKEN_MISSING")


def _live_ref_patterns(config: dict) -> list[str]:
    patterns = set()
    try:
        rows = _baseline_rows(config)
    except CurrentnessError:
        rows = []
    for row in rows:
        number = row.get("number")
        value = row.get("value") or {}
        if isinstance(value, dict) and "head" in value:
            patterns.add(f"refs/pull/{number}/head")
            patterns.add(f"refs/pull/{number}/merge")
            head = value.get("head")
            if isinstance(head, str) and head:
                patterns.add("refs/heads/" + head.removeprefix("refs/heads/"))
        elif isinstance(value, dict) and "issue" in value:
            continue
        else:
            patterns.add(f"refs/pull/{number}/head")
    live_cfg = config.get("_github_live", {})
    for number in live_cfg.get("watch_prs", []):
        patterns.add(f"refs/pull/{number}/head")
        patterns.add(f"refs/pull/{number}/merge")
    for branch in live_cfg.get("watch_branches", []):
        patterns.add("refs/heads/" + str(branch).removeprefix("refs/heads/"))
    return sorted(patterns)


def _git_ls_remote(config: dict, patterns: list[str]) -> tuple[dict, str, str]:
    remote = config.get("_github_live", {}).get(
        "remote", "https://github.com/maidiu/rawlsing.git")
    try:
        completed = subprocess.run(
            ["git", "ls-remote", "--refs", remote, *patterns],
            capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise CurrentnessError("LIVE_GITHUB_REF_FETCH_UNAVAILABLE",
                               {"error": type(exc).__name__}) from exc
    if completed.returncode != 0:
        raise CurrentnessError("LIVE_GITHUB_REF_FETCH_UNAVAILABLE", {
            "exit": completed.returncode,
            "stderr_sha256": sha256_bytes(completed.stderr.encode()),
        })
    refs = {}
    for line in completed.stdout.splitlines():
        if "\t" in line:
            sha, ref = line.split("\t", 1)
            refs[ref] = sha
    return refs, sha256_bytes(completed.stdout.encode()), remote


def _api_get(config: dict, path: str, token: str | None) -> dict:
    base = config.get("_github_live", {}).get(
        "api_base", "https://api.github.com")
    headers = {"Accept": "application/vnd.github+json",
               "User-Agent": "sorok-currentness-runtime-r2"}
    if token:
        headers["Authorization"] = "Bearer " + token
    request = urllib.request.Request(base + path, headers=headers)
    cafile = config.get("_github_live", {}).get("cafile", "/etc/ssl/cert.pem")
    context = ssl.create_default_context(cafile=cafile)
    try:
        with urllib.request.urlopen(request, timeout=25, context=context) as response:
            body = response.read()
            try:
                parsed = json.loads(body)
            except ValueError:
                parsed = None
            return {"http_status": response.status, "body_sha256": sha256_bytes(body),
                    "body": parsed, "error": None}
    except urllib.error.HTTPError as exc:
        body = exc.read()
        return {"http_status": exc.code, "body_sha256": sha256_bytes(body),
                "body": None, "error": "HTTP_" + str(exc.code)}
    except Exception as exc:  # noqa: BLE001
        return {"http_status": None, "body_sha256": None, "body": None,
                "error": type(exc).__name__}


def fetch_live_github(config: dict) -> dict:
    """Authenticated live ref/SHA fetch via git credentials; API as available."""
    patterns = _live_ref_patterns(config)
    refs, refs_digest, remote = _git_ls_remote(config, patterns)
    token, token_error = _git_credential_token()
    api_repo = config.get("_github_live", {}).get("api_repo", "maidiu/rawlsing")
    api = {"repo": None, "pulls": {}, "issues": {}, "commits": {},
           "token_available": bool(token), "token_error": token_error}
    if token:
        api["repo"] = _api_get(config, "/repos/" + api_repo, token)
    status_checks = 0
    status_success = 0
    try:
        rows = _baseline_rows(config)
    except CurrentnessError:
        rows = []
    for row in rows:
        number = row.get("number")
        value = row.get("value") or {}
        if isinstance(value, dict) and "head" in value:
            status_checks += 1
            result = _api_get(config, f"/repos/{api_repo}/pulls/{number}", token)
            if result.get("http_status") == 200 and isinstance(result.get("body"), dict):
                body = result["body"]
                api["pulls"][str(number)] = {
                    "state": body.get("state"),
                    "merged": body.get("merged"),
                    "draft": body.get("draft"),
                    "updated_at": body.get("updated_at"),
                    "head_sha": (body.get("head") or {}).get("sha"),
                    "merge_commit_sha": body.get("merge_commit_sha"),
                    "http_status": 200,
                    "body_sha256": result.get("body_sha256"),
                }
                status_success += 1
            else:
                api["pulls"][str(number)] = {
                    "http_status": result.get("http_status"),
                    "error": result.get("error"),
                    "body_sha256": result.get("body_sha256"),
                }
        elif isinstance(value, dict) and "issue" in value:
            status_checks += 1
            result = _api_get(config, f"/repos/{api_repo}/issues/{number}", token)
            if result.get("http_status") == 200 and isinstance(result.get("body"), dict):
                body = result["body"]
                api["issues"][str(number)] = {
                    "state": body.get("state"),
                    "updated_at": body.get("updated_at"),
                    "comments": body.get("comments"),
                    "http_status": 200,
                    "body_sha256": result.get("body_sha256"),
                }
                status_success += 1
            else:
                api["issues"][str(number)] = {
                    "http_status": result.get("http_status"),
                    "error": result.get("error"),
                    "body_sha256": result.get("body_sha256"),
                }
        else:
            for comment in row.get("comments", []):
                if comment.get("id"):
                    status_checks += 1
                    result = _api_get(
                        config, f"/repos/{api_repo}/issues/{number}/comments", token)
                    if result.get("http_status") == 200 and isinstance(result.get("body"), list):
                        match = next((c for c in result["body"]
                                      if c.get("id") == comment.get("id")), None)
                        if match:
                            api.setdefault("comments", {})[str(comment["id"])] = {
                                "body_sha256": hashlib.sha256(
                                    match.get("body", "").encode()).hexdigest(),
                                "updated_at": match.get("updated_at"),
                                "http_status": 200,
                            }
                            status_success += 1
                        else:
                            api.setdefault("comments", {})[str(comment["id"])] = {
                                "http_status": 200, "error": "COMMENT_NOT_FOUND"}
                    else:
                        api.setdefault("comments", {})[str(comment["id"])] = {
                            "http_status": result.get("http_status"),
                            "error": result.get("error")}
    for sha in sorted(set(refs.values())):
        if token:
            result = _api_get(config, f"/repos/{api_repo}/commits/{sha}", token)
            api["commits"][sha] = {
                "http_status": result.get("http_status"),
                "error": result.get("error"),
                "body_sha256": result.get("body_sha256"),
            }
    status_coverage = ("FULL" if status_checks and status_success == status_checks
                       else "REF_SHA_ONLY")
    fetched_at = now_utc()
    ttl = int(config.get("_github_live", {}).get("ttl_seconds", 900))
    live = {
        "schema": LIVE_GITHUB_SCHEMA,
        "source_trust": "AUTHENTICATED_LIVE_GITHUB",
        "source_identity": remote + " + " + api_repo,
        "transport": "git_ls_remote+github_api_credential_helper",
        "fetched_at_utc": fetched_at,
        "expires_at_utc": _utc_add(ttl),
        "ttl_seconds": ttl,
        "ref_patterns": patterns,
        "refs": refs,
        "refs_digest": refs_digest,
        "api": api,
        "status_coverage": status_coverage,
        "status_checks": status_checks,
        "status_success": status_success,
        "credential_helper_used": bool(token),
        "credential_error": token_error,
    }
    live["evidence_digest"] = digest({key: live[key] for key in (
        "source_identity", "fetched_at_utc", "refs", "refs_digest", "api",
        "status_coverage")})
    return live


def _live_fresh(state: dict, live: dict | None) -> bool:
    if not isinstance(live, dict):
        return False
    if not str(live.get("source_trust", "")).startswith("AUTHENTICATED_LIVE_GITHUB"):
        return False
    try:
        return _parse_utc(live["expires_at_utc"]) > datetime.datetime.now(
            datetime.timezone.utc)
    except (KeyError, ValueError, TypeError):
        return False


def fresh_live_github(config: dict, state: dict) -> dict:
    live = state.get("authenticated_checkpoint", {}).get("live_github")
    if _live_fresh(state, live):
        return live
    return fetch_live_github(config)


def _live_item(what: str, expected: str, next_action: str, live: dict,
               state: dict) -> dict:
    return {
        "what_changed": what,
        "expected_evidence": expected,
        "owner": "SOROK HQ + authenticated GitHub connector",
        "next_action": next_action,
        "source_kind": "LIVE_GITHUB",
        "source_digest": live.get("evidence_digest"),
        "fetched_at_utc": live.get("fetched_at_utc"),
        "expires_at_utc": live.get("expires_at_utc"),
        "status_coverage": live.get("status_coverage"),
        "checkpoint_id": state.get("checkpoint_id"),
    }


def compare_live_github(config: dict, state: dict, live: dict) -> list[dict]:
    items = []
    refs = live.get("refs", {})
    api = live.get("api", {})
    try:
        rows = _baseline_rows(config)
    except CurrentnessError:
        rows = []
        items.append(_live_item(
            "LOCAL_GITHUB_BASELINE_MISSING",
            "operator-owned expected-ref baseline file",
            "restore the expected-ref baseline; live observations are preserved separately",
            live, state))
    for row in rows:
        number = row.get("number")
        value = row.get("value") or {}
        if isinstance(value, dict) and "head" in value:
            head_ref = f"refs/pull/{number}/head"
            merge_ref = f"refs/pull/{number}/merge"
            actual_head = refs.get(head_ref)
            actual_merge = refs.get(merge_ref)
            expected_head = value.get("head_sha") or value.get("head")
            expected_merge = value.get("merge_commit_sha")
            branch = value.get("head")
            branch_ref = ("refs/heads/" + str(branch).removeprefix("refs/heads/")
                          if branch else None)
            if branch_ref and branch_ref not in refs:
                items.append(_live_item(
                    f"LOCAL_GITHUB_BASELINE_BRANCH_UNAVAILABLE pr:{number}",
                    "expected live branch ref " + branch_ref,
                    "reconcile the local expected-ref baseline against live GitHub",
                    live, state))
            elif branch_ref and expected_head and refs.get(branch_ref) != expected_head:
                items.append(_live_item(
                    f"LOCAL_GITHUB_BASELINE_BRANCH_MISMATCH pr:{number}",
                    f"expected {expected_head}; live {refs.get(branch_ref)}",
                    "do not accept a locally edited baseline; reconcile the actual live branch",
                    live, state))
            if actual_head is None:
                items.append(_live_item(
                    f"GITHUB_REF_DELETED pr:{number}",
                    "live PR head ref or competent connector status",
                    "inspect whether the PR was closed/deleted; keep dependent readiness on HOLD",
                    live, state))
            elif expected_head and actual_head != expected_head:
                items.append(_live_item(
                    f"GITHUB_HEAD_ADVANCED pr:{number}",
                    f"expected {expected_head}; live {actual_head}",
                    "reconcile the actual PR head and re-run the relevant receiving",
                    live, state))
            if expected_merge and actual_merge != expected_merge:
                items.append(_live_item(
                    f"GITHUB_MERGE_ADVANCED pr:{number}",
                    f"expected {expected_merge}; live {actual_merge}",
                    "reconcile the merge ref; do not treat old status as current",
                    live, state))
            actual_pull = (api.get("pulls") or {}).get(str(number))
            if not isinstance(actual_pull, dict) or actual_pull.get("http_status") != 200:
                items.append(_live_item(
                    f"GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE pr:{number}",
                    "authenticated issue/pull status and updated_at",
                    "wire an authenticated connector with pull/issues read scope; keep status HOLD",
                    live, state))
            else:
                if (value.get("state") != actual_pull.get("state")
                        or value.get("merged") != actual_pull.get("merged")
                        or value.get("updated_at") != actual_pull.get("updated_at")
                        or expected_head != actual_pull.get("head_sha")):
                    items.append(_live_item(
                        f"GITHUB_PR_STATUS_ADVANCED pr:{number}",
                        "live state/merged/updated_at/head matching the expected baseline",
                        "reconcile the changed PR status and re-run the relevant receiving",
                        live, state))
        elif isinstance(value, dict) and "issue" in value:
            actual_issue = (api.get("issues") or {}).get(str(number))
            if not isinstance(actual_issue, dict) or actual_issue.get("http_status") != 200:
                items.append(_live_item(
                    f"GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE issue:{number}",
                    "authenticated issue status and updated_at",
                    "wire an authenticated connector with issues read scope; keep status HOLD",
                    live, state))
            elif (value.get("state") != actual_issue.get("state")
                  or value.get("updated_at") != actual_issue.get("updated_at")):
                items.append(_live_item(
                    f"GITHUB_ISSUE_ADVANCED issue:{number}",
                    "live state/updated_at matching the expected baseline",
                    "reconcile the changed issue state and dependent ownership",
                    live, state))
        else:
            for comment in row.get("comments", []):
                if not comment.get("id"):
                    continue
                cid = str(comment["id"])
                actual = (api.get("comments") or {}).get(cid)
                if not isinstance(actual, dict) or actual.get("http_status") != 200:
                    items.append(_live_item(
                        f"GITHUB_COMMENT_SOURCE_UNAVAILABLE comment:{number}:{cid}",
                        "authenticated live comment body and updated_at",
                        "wire an authenticated connector with issue-comment read scope; keep HOLD",
                        live, state))
                elif actual.get("body_sha256") != hashlib.sha256(
                        comment.get("body", "").encode()).hexdigest():
                    items.append(_live_item(
                        f"GITHUB_COMMENT_ADVANCED comment:{number}:{cid}",
                        "live comment body matching the expected baseline",
                        "reconcile the changed comment and dependent currentness",
                        live, state))
    return items


def reconciliation_items(config: dict, state: dict) -> tuple[list[dict], dict | None]:
    items = []
    live = None
    try:
        live = fresh_live_github(config, state)
        items.extend(compare_live_github(config, state, live))
    except CurrentnessError as exc:
        items.append({
            "what_changed": exc.code,
            "expected_evidence": "authenticated live GitHub refs/status/SHA or a competent expiring connector feed",
            "owner": "SOROK HQ + authenticated GitHub connector",
            "next_action": "restore network/credential access or record exact source HOLD; do not use the local snapshot as live truth",
            "source_kind": "LIVE_GITHUB",
            "source_digest": None,
            "checkpoint_id": state.get("checkpoint_id"),
        })
    if config.get("_controller_state_root") and config["_controller_state_root"].is_dir():
        seen = state.get("authenticated_checkpoint", {}).get("local_receipts", {})
        for completion in sorted(config["_controller_state_root"].rglob("completion.json")):
            sha = sha256_file(completion)
            if sha not in seen:
                items.append({
                    "what_changed": "UNSEEN_LOCAL_CONTROLLER_RECEIPT " + str(completion.parent.name),
                    "expected_evidence": "WORKER_RETURN event bound to this completion.json",
                    "owner": "SOROK HQ/controller owner",
                    "next_action": "run intake-completion for this run before treating it as current",
                    "source_kind": "LOCAL_CONTROLLER",
                    "source_digest": sha,
                    "checkpoint_id": state.get("checkpoint_id"),
                })
    accepted_resolution_keys = {
        row.get("what_changed") for row in state.get("reconciliation_resolved", [])
        if row.get("resolution_state") in (
            "RESOLVED_BY_FRESH_LIVE_OBSERVATION",
            "RESOLVED_BY_COMPETENT_OPERATOR_EVIDENCE")
    }
    for resolution in state.get("reconciliation_resolved", []):
        if resolution.get("resolution_state") in (
                "RESOLVED_BY_FRESH_LIVE_OBSERVATION",
                "RESOLVED_BY_COMPETENT_OPERATOR_EVIDENCE"):
            continue
        legacy_name = "LEGACY_UNVERIFIED_RESOLUTION " + str(resolution.get("what_changed"))
        if legacy_name in accepted_resolution_keys:
            continue
        item = {
            "what_changed": legacy_name,
            "expected_evidence": "fresh live observation or competent operator/source authorization tied to the exact item",
            "owner": "SOROK HQ/competent source owner",
            "next_action": "treat the legacy arbitrary resolution as unverified history and resolve only with authenticated evidence",
            "source_kind": "LEGACY",
            "source_digest": digest(resolution),
            "checkpoint_id": state.get("checkpoint_id"),
        }
        items.append(item)
    resolved_keys = {
        row.get("resolution_key") for row in state.get("reconciliation_resolved", [])
        if row.get("resolution_key") and row.get("resolution_state") in (
            "RESOLVED_BY_FRESH_LIVE_OBSERVATION",
            "RESOLVED_BY_COMPETENT_OPERATOR_EVIDENCE")
    }
    filtered = []
    for item in items:
        key = digest({
            "what_changed": item.get("what_changed"),
            "source_kind": item.get("source_kind"),
            "source_digest": item.get("source_digest"),
        })
        if key in resolved_keys:
            continue
        filtered.append(item)
    return filtered, live


def startup(config: dict, *, reconcile: bool = False) -> dict:
    recover(config)
    whole, md, state = read_pair(config)
    items, live = reconciliation_items(config, state)
    resolved = {
        row.get("resolution_key"): row
        for row in state.get("reconciliation_resolved", [])
        if row.get("resolution_key") and row.get("resolution_state") in (
            "RESOLVED_BY_FRESH_LIVE_OBSERVATION",
            "RESOLVED_BY_COMPETENT_OPERATOR_EVIDENCE")
    }
    filtered = []
    for item in items:
        key = digest({
            "what_changed": item.get("what_changed"),
            "source_kind": item.get("source_kind"),
            "source_digest": item.get("source_digest"),
        })
        if key in resolved:
            continue
        filtered.append(item)
    items = filtered
    if reconcile:
        if live is not None:
            event = {
                "schema": EVENT_SCHEMA,
                "event_id": "github-live:" + str(live.get("evidence_digest")),
                "kind": "GITHUB_OBSERVATION",
                "recorded_utc": now_utc(),
                "source": {"trust": "RUNTIME_INTERNAL_LIVE_FETCH",
                           "observation_digest": live.get("evidence_digest")},
                "payload": {"live_observation": live},
            }
            intake_event(config, event, trusted=True)
        existing = {item.get("what_changed"): item for item in state.get(
            "reconciliation_required", [])}
        for item in items:
            if item["what_changed"] in existing:
                continue
            event = {
                "schema": EVENT_SCHEMA,
                "event_id": "reconciliation:" + digest(item),
                "kind": "RECONCILIATION_REQUIRED",
                "recorded_utc": now_utc(),
                "source": {"trust": "AUTHENTICATED_LIVE_GITHUB"
                           if item.get("source_kind") == "LIVE_GITHUB"
                           else "AUTHENTICATED_LOCAL_STARTUP"},
                "payload": {"item": item},
            }
            intake_event(config, event, trusted=True)
        whole, md, state = read_pair(config)
        state = copy.deepcopy(state)
        state["reconciliation_required"] = items
        state["generation"] += 1
        state["updated_utc"] = now_utc()
        recompute(state)
        commit_state(config, whole, md, state)
    return {"generation": state["generation"], "checkpoint_id": state["checkpoint_id"],
            "reconciliation_required": items,
            "readout": render_readout(state)}


def render_readout(state: dict) -> dict:
    baseline = state.get("authenticated_checkpoint", {}).get("baseline")
    live = state.get("authenticated_checkpoint", {}).get("live_github")
    live_summary = None
    if isinstance(live, dict):
        live_summary = {
            "source_trust": live.get("source_trust"),
            "source_identity": live.get("source_identity"),
            "fetched_at_utc": live.get("fetched_at_utc"),
            "expires_at_utc": live.get("expires_at_utc"),
            "status_coverage": live.get("status_coverage"),
            "evidence_digest": live.get("evidence_digest"),
            "refs_digest": live.get("refs_digest"),
            "fresh": _live_fresh(state, live),
        }
    return {
        "schema": "SOROK_CURRENTNESS_READOUT_R1",
        "generation": state["generation"],
        "checkpoint_id": state["checkpoint_id"],
        "updated_utc": state["updated_utc"],
        "frozen_projection": {
            "adoption": state.get("frozen_projection_adoption",
                                  "PENDING_INDEPENDENT_RECEIVING"),
            "preserved": True,
        },
        "runtime_adoption": state.get("adoption"),
        "protected_ci": state.get("protected_ci"),
        "authenticated_github_baseline": baseline,
        "authenticated_github_live": live_summary,
        "ready_for_independent_receiving": state["readiness"].get(
            "ready_for_independent_receiving", []),
        "ready_for_scoped_engineering": state["readiness"].get(
            "ready_for_scoped_engineering", []),
        "ready": {
            "receiving": state["readiness"].get(
                "awaiting_independent_receiving", []),
            "scoped_engineering": state["readiness"].get(
                "ready_for_scoped_engineering", []),
            "next": state.get("recommended_next"),
        },
        "awaiting_independent_receiving": state["readiness"].get(
            "awaiting_independent_receiving", []),
        "task_readiness": state["readiness"].get("task_readiness", []),
        "decision_readiness": state.get("decision_readiness", []),
        "mechanism_review": state.get("mechanism_review"),
        "mechanism_review_history": state.get("mechanism_review_history", []),
        "mechanism_review_original": state.get("mechanism_review_original"),
        "mechanism_worker_return": state.get("mechanism_worker_return"),
        "holds": state.get("holds", []),
        "reconciliation_required": state.get("reconciliation_required", []),
        "reconciliation_resolved": state.get("reconciliation_resolved", []),
        "protected_foundations": state.get("protected_foundations", {}),
        "browser": state.get("browser", {}),
        "controllers": state.get("controllers", {}),
        "infrastructure_qualification": state.get("infrastructure_qualification", []),
        "baseline_replay": state.get("baseline_replay", []),
        "recommended_next": state.get("recommended_next"),
        "no_automatic_dispatch": True,
        "source_trust": "SOURCEFREE_ENGINEERING_ONLY__NATIVE_SCIENCE_AND_HUMAN_HELD",
    }


def _make_return_event(config: dict, run_dir: Path, *, task_id: str | None = None,
                       return_path: str | None = None, scope: str | None = None) -> dict:
    run_dir = run_dir.resolve()
    job = read_json(run_dir / "job.json")
    binding = read_json(run_dir / "binding.json")
    launch = read_json(run_dir / "launch.json")
    process = read_json(run_dir / "process.json")
    completion = read_json(run_dir / "completion.json")
    worktree = Path(binding["worktree"]).resolve()
    currentness = binding.get("sorok_currentness") or {}
    task_id = task_id or currentness.get("task_id")
    role = currentness.get("role")
    if return_path is None:
        filename = currentness.get("return_filename", "return.json")
        return_path = str(worktree / filename)
    source = {
        "trust": "REAL_LOCAL_CONTROLLER_COMPLETION",
        "role": role,
        "expected_session": currentness.get("expected_session"),
        "expected_source_commit": currentness.get("expected_source_commit"),
        "controller_run_dir": str(run_dir),
        "job_id": job["job_id"],
        "session": job["session"],
        "pid": process["pid"],
        "grant_id": job["grant_id"],
        "argv_sha256": command_digest(job["argv"]),
        "worktree": str(worktree),
        "recipient_thread": binding.get("recipient_thread"),
        "job_sha256": sha256_file(run_dir / "job.json"),
        "binding_sha256": sha256_file(run_dir / "binding.json"),
        "launch_sha256": sha256_file(run_dir / "launch.json"),
        "process_sha256": sha256_file(run_dir / "process.json"),
        "completion_sha256": sha256_file(run_dir / "completion.json"),
        "source_commit": (completion.get("source_commit")
                          or launch.get("source_commit")
                          or job.get("source_commit")
                          or binding.get("source_commit")
                          or currentness.get("expected_source_commit")),
        "return_path": return_path,
    }
    event = {
        "schema": EVENT_SCHEMA,
        "event_id": "completion:" + source["completion_sha256"],
        "kind": "WORKER_RETURN" if task_id else "INFRASTRUCTURE_RETURN",
        "recorded_utc": now_utc(),
        "source": source,
        "payload": {
            "task_id": task_id,
            "role": role,
            "scope": scope or "INFRASTRUCTURE_QUALIFICATION_NOT_ORIGINAL_SCIENCE",
            "exit_code": completion.get("exit_code"),
            "author_session": job.get("session"),
            "source_commit": source.get("source_commit"),
        },
    }
    return event


def _load_review_receipt(path: Path) -> dict:
    receipt = read_json(path)
    if not isinstance(receipt, dict):
        raise CurrentnessError("REVIEW_RECEIPT_NOT_OBJECT")
    return receipt


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SOROK automatic currentness runtime")
    parser.add_argument("--config", required=True, type=Path)
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init")
    sub.add_parser("status")
    sub.add_parser("what-next")
    startup_parser = sub.add_parser("startup")
    startup_parser.add_argument("--reconcile", action="store_true")
    sub.add_parser("recover")
    reconcile_parser = sub.add_parser("reconcile")
    reconcile_parser.add_argument("--operator-authorization-id")
    migrate_parser = sub.add_parser("migrate")
    migrate_parser.add_argument("--operator-authorization-id")
    attest = sub.add_parser("attest-launch")
    attest.add_argument("--run-dir", required=True, type=Path)
    enroll = sub.add_parser("enroll-existing-run")
    enroll.add_argument("--run-dir", required=True, type=Path)
    enroll.add_argument("--authorization-id", required=True)
    sub.add_parser("show-trusted-launches")
    completion = sub.add_parser("intake-completion")
    completion.add_argument("--run-dir", required=True, type=Path)
    completion.add_argument("--task-id")
    completion.add_argument("--return-path")
    completion.add_argument("--scope")
    review = sub.add_parser("intake-review")
    review.add_argument("--receipt", type=Path)
    review.add_argument("--review-run-dir", type=Path)
    review.add_argument("--replay", action="store_true")
    historical = sub.add_parser("intake-historical-review")
    historical.add_argument("--run-dir", required=True, type=Path)
    historical.add_argument("--receipt", required=True, type=Path)
    historical.add_argument("--verdict", required=True)
    event_parser = sub.add_parser("intake-event")
    event_parser.add_argument("--event", required=True, type=Path)
    control = sub.add_parser("control-event")
    control.add_argument("--event", required=True, type=Path)
    resolve = sub.add_parser("resolve-reconciliation")
    resolve.add_argument("--what-changed", required=True)
    resolve.add_argument("--fresh-observation-digest")
    resolve.add_argument("--operator-authorization-id")
    resolve.add_argument("--source-hold-authorization-id")
    resolve.add_argument("--reason", default="explicit authenticated reconciliation")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        if args.command == "attest-launch":
            print(json.dumps(attest_launch(config, args.run_dir), indent=2,
                             sort_keys=True))
            return 0
        if args.command == "enroll-existing-run":
            print(json.dumps(enroll_existing_run(
                config, args.run_dir, args.authorization_id), indent=2,
                sort_keys=True))
            return 0
        if args.command == "show-trusted-launches":
            registry = _registry_load(config)
            safe = {
                "schema": registry.get("schema"),
                "entries": [
                    {key: value for key, value in entry.items()
                     if key not in ("attestation",)}
                    for entry in registry.get("entries", {}).values()],
            }
            print(json.dumps(safe, indent=2, sort_keys=True))
            return 0
        if args.command == "init":
            with _lock(config, True):
                whole = read_json(config["_pair_json"])
                md = config["_pair_md"].read_text(encoding="utf-8")
                if RUNTIME_KEY in whole:
                    raise CurrentnessError("RUNTIME_ALREADY_INITIALIZED")
                state = initial_state(config, whole)
                state["source_freeze"]["frozen_md_block_sha256"] = sha256_bytes(
                    _extract_block(md, FROZEN_START, FROZEN_END).encode())
                commit_state(config, whole, md, state)
            print(json.dumps({"state": "INITIALIZED", "generation": state["generation"],
                              "checkpoint_id": state["checkpoint_id"]}, indent=2))
            return 0
        if args.command == "status":
            whole, md, state = read_pair(config)
            items, live = reconciliation_items(config, state)
            readout = render_readout(state)
            readout["reconciliation_required"] = items
            readout["status_source_check"] = (
                "LIVE_GITHUB_FETCH_PERFORMED" if live else
                "LIVE_GITHUB_UNAVAILABLE_KEEP_HOLD")
            if live:
                readout["authenticated_github_live"] = {
                    "source_trust": live.get("source_trust"),
                    "source_identity": live.get("source_identity"),
                    "fetched_at_utc": live.get("fetched_at_utc"),
                    "expires_at_utc": live.get("expires_at_utc"),
                    "status_coverage": live.get("status_coverage"),
                    "evidence_digest": live.get("evidence_digest"),
                    "refs_digest": live.get("refs_digest"),
                    "fresh": True,
                }
            print(json.dumps(readout, indent=2, sort_keys=True))
            return 2 if items else 0
        if args.command == "what-next":
            whole, md, state = read_pair(config)
            items, live = reconciliation_items(config, state)
            readout = render_readout(state)
            readout["reconciliation_required"] = items
            print(json.dumps(readout["recommended_next"], indent=2,
                             sort_keys=True))
            print(json.dumps({"reconciliation_required": items}, indent=2,
                             sort_keys=True))
            return 2 if items else 0
        if args.command == "recover":
            print(json.dumps(recover(config), indent=2))
            return 0
        if args.command == "migrate":
            item = {"what_changed": "STATE_MAINTENANCE migrate",
                    "source_digest": digest({
                        "command": "migrate",
                        "pair_json": str(config["_pair_json"]),
                    })}
            _authorize_operator(
                config, purpose="STATE_MAINTENANCE", item=item,
                authorization_id=args.operator_authorization_id,
                allowed_roles=("SOROK_HQ_OPERATOR",))
            with _lock(config, True):
                whole = read_json(config["_pair_json"])
                md = config["_pair_md"].read_text(encoding="utf-8")
                state = whole.get(RUNTIME_KEY)
                if not isinstance(state, dict):
                    raise CurrentnessError("RUNTIME_NOT_INITIALIZED")
                state = copy.deepcopy(state)
                state["generation"] += 1
                state["updated_utc"] = now_utc()
                migrate_state(config, state)
                commit_state(config, whole, md, state)
            print(json.dumps({"state": "MIGRATED",
                              "generation": state["generation"],
                              "checkpoint_id": state["checkpoint_id"]}, indent=2))
            return 0
        if args.command in ("reconcile", "migrate"):
            item = {"what_changed": "STATE_MAINTENANCE " + args.command,
                    "source_digest": digest({
                        "command": args.command,
                        "pair_json": str(config["_pair_json"]),
                    })}
            _authorize_operator(
                config, purpose="STATE_MAINTENANCE", item=item,
                authorization_id=getattr(args, "operator_authorization_id", None),
                allowed_roles=("SOROK_HQ_OPERATOR",))
        if args.command == "reconcile":
            with _lock(config, True):
                whole = read_json(config["_pair_json"])
                md = config["_pair_md"].read_text(encoding="utf-8")
                state = whole.get(RUNTIME_KEY)
                if not isinstance(state, dict):
                    raise CurrentnessError("RUNTIME_NOT_INITIALIZED")
                state = copy.deepcopy(state)
                state["generation"] += 1
                state["updated_utc"] = now_utc()
                recompute(state)
                commit_state(config, whole, md, state)
            print(json.dumps({"state": "RECONCILED",
                              "generation": state["generation"],
                              "checkpoint_id": state["checkpoint_id"]}, indent=2))
            return 0
        if args.command == "startup":
            result = startup(config, reconcile=args.reconcile)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 2 if result["reconciliation_required"] else 0
        if args.command == "intake-completion":
            event = _make_return_event(
                config, args.run_dir, task_id=args.task_id,
                return_path=args.return_path, scope=args.scope)
            print(json.dumps(intake_event(config, event, trusted=True), indent=2, sort_keys=True))
            return 0
        if args.command == "intake-review":
            if args.replay:
                if not args.receipt:
                    raise CurrentnessError("REPLAY_RECEIPT_REQUIRED")
                receipt = _load_review_receipt(args.receipt)
                event = {
                    "schema": EVENT_SCHEMA,
                    "event_id": "review:" + digest(receipt),
                    "kind": "REVIEW_VERDICT",
                    "recorded_utc": now_utc(),
                    "source": {
                        "trust": "IMMUTABLE_HISTORICAL_INDEPENDENT_REVIEW_REPLAY",
                        "receipt_path": str(args.receipt),
                        "receipt_sha256": sha256_file(args.receipt),
                    },
                    "receipt": receipt,
                    "payload": {"task_id": receipt.get("task_id"),
                                "verdict": receipt.get("verdict")},
                }
                print(json.dumps(intake_event(config, event, trusted=True), indent=2, sort_keys=True))
                return 0
            if not args.review_run_dir:
                raise CurrentnessError("REVIEW_SUPERVISED_RUN_REQUIRED")
            run_dir = args.review_run_dir.resolve()
            event = _make_return_event(config, run_dir)
            artifact_path = Path(event["source"]["return_path"])
            artifact = read_json(artifact_path)
            if not isinstance(artifact, dict) or artifact.get("schema") != REVIEW_RECEIPT_SCHEMA:
                raise CurrentnessError("REVIEW_RUN_ARTIFACT_SCHEMA")
            if args.receipt and digest(_load_review_receipt(args.receipt)) != digest(artifact):
                raise CurrentnessError("REVIEW_RECEIPT_DOES_NOT_MATCH_RUN_ARTIFACT")
            source = dict(event["source"])
            source["trust"] = "REAL_LOCAL_SUPERVISED_REVIEW_RUN"
            source["review_run_dir"] = str(run_dir)
            review_event = {
                "schema": EVENT_SCHEMA,
                "event_id": "review-run:" + source["completion_sha256"],
                "kind": "REVIEW_VERDICT",
                "recorded_utc": now_utc(),
                "source": source,
                "receipt": artifact,
                "payload": {"task_id": artifact.get("task_id"),
                            "verdict": artifact.get("verdict")},
            }
            print(json.dumps(intake_event(config, review_event, trusted=True),
                             indent=2, sort_keys=True))
            return 0
        if args.command == "intake-historical-review":
            receipt = _load_review_receipt(args.receipt)
            run_dir = args.run_dir.resolve()
            source = {
                "trust": "POSTHOC_REGISTERED_REAL_REVIEWER_RUN",
                "controller_run_dir": str(run_dir),
                "job_id": read_json(run_dir / "job.json")["job_id"],
                "session": read_json(run_dir / "job.json")["session"],
                "pid": read_json(run_dir / "process.json")["pid"],
                "worktree": read_json(run_dir / "binding.json")["worktree"],
                "recipient_thread": read_json(run_dir / "binding.json").get(
                    "recipient_thread"),
                "job_sha256": sha256_file(run_dir / "job.json"),
                "binding_sha256": sha256_file(run_dir / "binding.json"),
                "launch_sha256": sha256_file(run_dir / "launch.json"),
                "process_sha256": sha256_file(run_dir / "process.json"),
                "completion_sha256": sha256_file(run_dir / "completion.json"),
            }
            run = validate_controller_run(run_dir, source)
            _require_trusted_launch(config, run_dir, run, run["binding"])
            event = {
                "schema": EVENT_SCHEMA,
                "event_id": "historical-review:" + source["completion_sha256"],
                "kind": "HISTORICAL_REVIEW",
                "recorded_utc": now_utc(),
                "source": source,
                "payload": {"receipt": receipt, "verdict": args.verdict,
                            "posthoc_registration": True,
                            "automatic_intake": False},
            }
            print(json.dumps(intake_event(config, event, trusted=True), indent=2, sort_keys=True))
            return 0
        if args.command == "intake-event":
            event = read_json(args.event)
            print(json.dumps(intake_event(config, event), indent=2, sort_keys=True))
            return 0
        if args.command == "control-event":
            event = read_json(args.event)
            print(json.dumps(intake_control_event(config, event), indent=2,
                             sort_keys=True))
            return 0
        if args.command == "resolve-reconciliation":
            if not (args.fresh_observation_digest
                    or args.operator_authorization_id
                    or args.source_hold_authorization_id):
                raise CurrentnessError("RESOLUTION_AUTHENTICATION_REQUIRED")
            payload = {"what_changed": args.what_changed,
                       "reason": args.reason}
            if args.fresh_observation_digest:
                payload["fresh_observation_digest"] = args.fresh_observation_digest
            if args.operator_authorization_id:
                payload["operator_authorization_id"] = args.operator_authorization_id
            if args.source_hold_authorization_id:
                payload["source_hold_authorization_id"] = (
                    args.source_hold_authorization_id)
            event = {
                "schema": EVENT_SCHEMA,
                "event_id": "resolve:" + digest(payload),
                "kind": "RECONCILIATION_RESOLVED",
                "recorded_utc": now_utc(),
                "source": {"trust": "AUTHENTICATED_RESOLUTION_EVIDENCE"},
                "payload": payload,
            }
            print(json.dumps(intake_event(config, event, trusted=True), indent=2, sort_keys=True))
            return 0
        raise CurrentnessError("COMMAND_UNKNOWN", args.command)
    except CurrentnessError as exc:
        print("SOROK_CURRENTNESS_RUNTIME_RED: " + str(exc), file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001 - fail visibly, never silently promote
        print("SOROK_CURRENTNESS_RUNTIME_RED: UNEXPECTED " +
              type(exc).__name__ + ": " + str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
