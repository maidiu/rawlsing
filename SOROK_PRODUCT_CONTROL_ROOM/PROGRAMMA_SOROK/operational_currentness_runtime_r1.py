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
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "SOROK_OPERATIONAL_CURRENTNESS_RUNTIME_R1"
EVENT_SCHEMA = "SOROK_CURRENTNESS_EVENT_R1"
REVIEW_RECEIPT_SCHEMA = "SOROK_CURRENTNESS_REVIEW_RECEIPT@1"
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
WORKFLOW_BLOB = "f76c0d90d32e54d26d019b7f77c563b33fd5e97b"
MECHANISM_ID = "AUTOMATIC_CURRENTNESS_R1"
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
    packet, _gmt, gmt_index = frozen_contracts(config)
    tasks = build_tasks(frozen, packet, gmt_index)
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
        },
        "events": [],
        "tasks": tasks,
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
        },
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
             "source_refs": row["source_refs"]}
            for row in tasks
        ],
        "holds": holds,
        "full_original_claim_not_established": sorted(full_ready),
        "browser": state.get("browser", {}),
        "controllers": state.get("controllers", {}),
        "protected_ci": state.get("protected_ci"),
    }
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
    if not isinstance(payload, dict) or payload.get("schema") != RETURN_SCHEMA:
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


def _validate_review_receipt(config: dict, receipt: dict, *, replay: bool) -> dict:
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
    verified = []
    commit = receipt.get("review_commit")
    if replay:
        if receipt.get("source_trust") != "IMMUTABLE_HISTORICAL_INDEPENDENT_REVIEW_REPLAY":
            raise CurrentnessError("REPLAY_TRUST_REQUIRED")
        verified = verify_git_documents(config["_root"], commit, documents)
    else:
        if receipt.get("source_trust") != "REAL_LOCAL_NONAUTHOR_REVIEW":
            raise CurrentnessError("REVIEW_TRUST_REQUIRED")
        verified = verify_git_documents(config["_root"], commit, documents)
    return {
        "receipt": receipt,
        "verified_documents": verified,
        "receipt_sha256": digest(receipt),
        "replay": replay,
    }


def apply_event(state: dict, event: dict, config: dict, contracts: tuple) -> dict:
    kind = event["kind"]
    source = event.get("source", {})
    payload = event.get("payload", {})
    if kind == "INIT":
        return state
    if kind in ("WORKER_RETURN", "INFRASTRUCTURE_RETURN"):
        task_id = payload.get("task_id")
        run = None
        if source.get("controller_run_dir"):
            run = validate_controller_run(Path(source["controller_run_dir"]), source)
        else:
            raise CurrentnessError("CONTROLLER_RUN_REQUIRED")
        artifact = _verify_return_artifact(source, run["binding"])
        if task_id in EXPECTED_IDS:
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
        state["controller_integration"]["hook_state"] = "REAL_LOCAL_RETURN_INTAKEN"
        return state
    if kind == "REVIEW_VERDICT":
        receipt = event.get("receipt")
        if not isinstance(receipt, dict):
            raise CurrentnessError("REVIEW_RECEIPT_MISSING")
        replay = source.get("trust") == "IMMUTABLE_HISTORICAL_INDEPENDENT_REVIEW_REPLAY"
        validated = _validate_review_receipt(config, receipt, replay=replay)
        task = _task_by_id(state, receipt["task_id"])
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
                "reviewer_session": receipt.get("reviewer_session"),
                "review_commit": receipt.get("review_commit"),
                "review_scope": receipt.get("scope"),
                "review_receipt": validated["receipt"],
                "replay": replay,
            })
            if replay:
                state["baseline_replay"].append({
                    "event_id": event["event_id"], "task_id": MECHANISM_ID,
                    "review_commit": receipt.get("review_commit"),
                    "verdict": receipt["verdict"],
                    "replay_is_not_new_review": True,
                })
            return state
        if task.get("code_sha") and implementation != task["code_sha"]:
            raise CurrentnessError("STALE_EVIDENCE", receipt["task_id"])
        if receipt.get("review_commit") and not HASH_RE.fullmatch(receipt["review_commit"]):
            raise CurrentnessError("REVIEW_COMMIT_INVALID")
        verdict = receipt["verdict"]
        task["review_event_id"] = event["event_id"]
        task["review_receipt_sha256"] = validated["receipt_sha256"]
        task["review_commit"] = receipt.get("review_commit")
        task["review_scope"] = receipt.get("scope")
        task["review_trust"] = receipt.get("source_trust")
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
                "event_id": event["event_id"], "task_id": receipt["task_id"],
                "review_pr": receipt.get("review_pr"),
                "review_commit": receipt.get("review_commit"),
                "verdict": verdict,
                "replay_is_not_new_review": True,
            })
        return state
    if kind == "REJECTION":
        task = _task_by_id(state, payload["task_id"])
        task["sourcefree_state"] = "REJECTED"
        task["execution_state"] = "REJECTED"
        task["rejection_event_id"] = event["event_id"]
        return state
    if kind == "PROTECTED_INTEGRATION":
        task = _task_by_id(state, payload["task_id"])
        ci_state = payload.get("ci_state")
        merge_sha = payload.get("merge_sha")
        if ci_state != "PASS" or not merge_sha:
            task["protected_integration"] = "PENDING_PROTECTED_CI_AND_ADOPTION"
            task["protected_ci"] = ci_state or "NOT_RUN"
            state["controls"]["holds"].append({
                "scope": task["id"], "owner": payload.get("owner", "protected CI owner"),
                "reason": "PROTECTED_CI_UNAVAILABLE_OR_UNMET", "event_id": event["event_id"],
            })
        else:
            task["protected_integration"] = "PROTECTED_SOURCEFREE"
            task["protected_ci"] = "PASS"
            task["protected_merge_sha"] = merge_sha
        return state
    if kind in ("SOURCE_AUTHORITY_HOLD", "USER_STOP", "REVOCATION", "USER_RESUME"):
        scope = payload.get("scope")
        if not scope:
            raise CurrentnessError("CONTROL_SCOPE_MISSING")
        key = {"SOURCE_AUTHORITY_HOLD": "holds", "USER_STOP": "stops",
               "REVOCATION": "revocations"}.get(kind)
        if kind == "USER_RESUME":
            state["controls"]["stops"] = [
                row for row in state["controls"]["stops"]
                if row.get("scope") != scope]
            return state
        state["controls"].setdefault(key, []).append({
            "scope": scope, "owner": payload.get("owner"),
            "reason": payload.get("reason", kind), "event_id": event["event_id"],
        })
        return state
    if kind == "GITHUB_OBSERVATION":
        baseline_sha = payload.get("baseline_sha256")
        if not baseline_sha:
            raise CurrentnessError("GITHUB_BASELINE_SHA_MISSING")
        state["authenticated_checkpoint"]["baseline"] = {
            "path": payload.get("baseline_path"),
            "sha256": baseline_sha,
            "as_of": payload.get("as_of", now_utc()),
        }
        state["authenticated_checkpoint"]["last_authenticated_at_utc"] = (
            payload.get("as_of", now_utc()))
        state["authenticated_checkpoint"]["github_observations"] = copy.deepcopy(
            payload.get("observations", {}))
        state["reconciliation_required"] = [
            item for item in state.get("reconciliation_required", [])
            if not str(item.get("what_changed", "")).startswith(
                ("AUTHENTICATED_GITHUB_REF_NOT_YET_RECONCILED",
                 "AUTHENTICATED_GITHUB_INTAKE_UNAVAILABLE"))]
        return state
    if kind == "RECONCILIATION_RESOLVED":
        what = payload.get("what_changed")
        if not what or not payload.get("evidence"):
            raise CurrentnessError("RECONCILIATION_RESOLUTION_INCOMPLETE")
        before = len(state.get("reconciliation_required", []))
        state["reconciliation_required"] = [
            item for item in state.get("reconciliation_required", [])
            if item.get("what_changed") != what]
        state.setdefault("reconciliation_resolved", []).append({
            "what_changed": what, "evidence": payload.get("evidence"),
            "owner": payload.get("owner"), "reason": payload.get("reason"),
            "event_id": event["event_id"],
        })
        if len(state["reconciliation_required"]) == before:
            raise CurrentnessError("RECONCILIATION_ITEM_NOT_FOUND", what)
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


def intake_event(config: dict, event: dict) -> dict:
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


def baseline_observations(rows: list[dict]) -> dict:
    observations = {}
    for row in rows:
        number = row.get("number")
        value = row.get("value") or {}
        if "pr" in row:
            key = "pr:" + str(number)
            observations[key] = {
                "state": "MERGED" if row.get("merged") else value.get("state", "OPEN"),
                "head_sha": row.get("head"),
                "merge_sha": row.get("merge"),
                "observed": True,
            }
        elif isinstance(value, dict) and "head" in value and "base" in value:
            observations["pr:" + str(number)] = {
                "state": "MERGED" if value.get("merged") else value.get("state", "OPEN"),
                "head_sha": value.get("head"),
                "merge_sha": value.get("merge_commit_sha"),
                "draft": value.get("draft"),
                "observed": True,
            }
        elif "comments" in row:
            key = "comment:" + str(number)
            for comment in row.get("comments", []):
                if comment.get("id"):
                    observations[key + ":" + str(comment["id"])] = {
                        "state": "REPORTED_COMMENT",
                        "comment_id": comment.get("id"),
                        "body_sha256": hashlib.sha256(
                            comment.get("body", "").encode()).hexdigest(),
                        "observed": True,
                    }
        elif isinstance(value, dict) and "issue" in value:
            issue = value["issue"]
            key = "issue:" + str(number)
            observations[key] = {
                "state": issue.get("state", "OPEN"),
                "updated_at": issue.get("updated_at"),
                "comments": issue.get("comments"),
                "observed": True,
            }
        else:
            observations["row:" + str(number)] = {"state": "UNCLASSIFIED", "observed": True}
    return observations


def reconciliation_items(config: dict, state: dict) -> list[dict]:
    items = []
    try:
        rows = _baseline_rows(config)
        observations = baseline_observations(rows)
        known = state.get("authenticated_checkpoint", {}).get("github_observations", {})
        for key, value in observations.items():
            if known.get(key) != value:
                items.append({
                    "what_changed": "AUTHENTICATED_GITHUB_REF_NOT_YET_RECONCILED " + key,
                    "expected_evidence": "local return/review/protected receipt matching the GitHub ref",
                    "owner": "SOROK HQ",
                    "next_action": "run startup --reconcile and inspect the exact local return/review before any state change",
                })
    except CurrentnessError as exc:
        items.append({
            "what_changed": exc.code,
            "expected_evidence": "authenticated GitHub intake baseline file",
            "owner": "existing SOROK HQ/controller owner",
            "next_action": "restore the baseline or record explicit source gap",
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
                })
    return items


def startup(config: dict, *, reconcile: bool = False) -> dict:
    recover(config)
    whole, md, state = read_pair(config)
    items = reconciliation_items(config, state)
    resolved = {row.get("what_changed")
                for row in state.get("reconciliation_resolved", [])}
    items = [item for item in items if item.get("what_changed") not in resolved]
    if reconcile:
        existing = {item.get("what_changed"): item for item in state.get(
            "reconciliation_required", [])}
        new_items = [item for item in items if item["what_changed"] not in existing]
        for item in new_items:
            event = {
                "schema": EVENT_SCHEMA,
                "event_id": "reconciliation:" + digest(item),
                "kind": "RECONCILIATION_REQUIRED",
                "recorded_utc": now_utc(),
                "source": {"trust": "AUTHENTICATED_LOCAL_STARTUP"},
                "payload": {"item": item},
            }
            intake_event(config, event)
        try:
            rows = _baseline_rows(config)
            observations = baseline_observations(rows)
            event = {
                "schema": EVENT_SCHEMA,
                "event_id": "github-baseline:" + sha256_file(Path(config["_baseline"])),
                "kind": "GITHUB_OBSERVATION",
                "recorded_utc": now_utc(),
                "source": {"trust": "AUTHENTICATED_GITHUB_INTAKE_BASELINE"},
                "payload": {
                    "baseline_path": str(config["_baseline"]),
                    "baseline_sha256": sha256_file(Path(config["_baseline"])),
                    "as_of": now_utc(),
                    "observations": observations,
                },
            }
            intake_event(config, event)
        except CurrentnessError:
            pass
        whole, md, state = read_pair(config)
        items = state.get("reconciliation_required", [])
    return {"generation": state["generation"], "checkpoint_id": state["checkpoint_id"],
            "reconciliation_required": items,
            "readout": render_readout(state)}


def render_readout(state: dict) -> dict:
    baseline = state.get("authenticated_checkpoint", {}).get("baseline")
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
        "mechanism_review": state.get("mechanism_review"),
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
    if return_path is None:
        filename = binding.get("sorok_currentness", {}).get(
            "return_filename", "return.json")
        return_path = str(worktree / filename)
    source = {
        "trust": "REAL_LOCAL_CONTROLLER_COMPLETION",
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
                          or binding.get("sorok_currentness", {}).get("source_commit")),
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
    sub.add_parser("reconcile")
    completion = sub.add_parser("intake-completion")
    completion.add_argument("--run-dir", required=True, type=Path)
    completion.add_argument("--task-id")
    completion.add_argument("--return-path")
    completion.add_argument("--scope")
    review = sub.add_parser("intake-review")
    review.add_argument("--receipt", required=True, type=Path)
    review.add_argument("--replay", action="store_true")
    event_parser = sub.add_parser("intake-event")
    event_parser.add_argument("--event", required=True, type=Path)
    resolve = sub.add_parser("resolve-reconciliation")
    resolve.add_argument("--what-changed", required=True)
    resolve.add_argument("--evidence", required=True)
    resolve.add_argument("--owner", default="SOROK HQ")
    resolve.add_argument("--reason", default="explicit operator reconciliation")
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
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
            print(json.dumps(render_readout(state), indent=2, sort_keys=True))
            return 2 if state.get("reconciliation_required") else 0
        if args.command == "what-next":
            whole, md, state = read_pair(config)
            print(json.dumps(render_readout(state)["recommended_next"], indent=2,
                             sort_keys=True))
            return 2 if state.get("reconciliation_required") else 0
        if args.command == "recover":
            print(json.dumps(recover(config), indent=2))
            return 0
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
            print(json.dumps(intake_event(config, event), indent=2, sort_keys=True))
            return 0
        if args.command == "intake-review":
            receipt = _load_review_receipt(args.receipt)
            event = {
                "schema": EVENT_SCHEMA,
                "event_id": "review:" + digest(receipt),
                "kind": "REVIEW_VERDICT",
                "recorded_utc": now_utc(),
                "source": {
                    "trust": ("IMMUTABLE_HISTORICAL_INDEPENDENT_REVIEW_REPLAY"
                              if args.replay else "REAL_LOCAL_NONAUTHOR_REVIEW"),
                    "receipt_path": str(args.receipt),
                    "receipt_sha256": sha256_file(args.receipt),
                },
                "receipt": receipt,
                "payload": {"task_id": receipt.get("task_id"),
                            "verdict": receipt.get("verdict")},
            }
            print(json.dumps(intake_event(config, event), indent=2, sort_keys=True))
            return 0
        if args.command == "intake-event":
            event = read_json(args.event)
            print(json.dumps(intake_event(config, event), indent=2, sort_keys=True))
            return 0
        if args.command == "resolve-reconciliation":
            event = {
                "schema": EVENT_SCHEMA,
                "event_id": "resolve:" + digest({
                    "what": args.what_changed, "evidence": args.evidence}),
                "kind": "RECONCILIATION_RESOLVED",
                "recorded_utc": now_utc(),
                "source": {"trust": "EXPLICIT_LOCAL_OPERATOR_RESOLUTION"},
                "payload": {"what_changed": args.what_changed,
                            "evidence": args.evidence, "owner": args.owner,
                            "reason": args.reason},
            }
            print(json.dumps(intake_event(config, event), indent=2, sort_keys=True))
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
