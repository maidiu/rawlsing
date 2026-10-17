"""FIABC source×candidate process-isolation envelope.

This module is deliberately below semantic ownership. It does not derive source,
authority, workload, oracle, metric, or lifecycle truth. It enforces where a
candidate process may begin, what cell it belongs to, when it must die, and what
raw process-boundary observations sibling accounting workers may consume.
"""
from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import resource
import subprocess
import sys
import time
import types
from dataclasses import dataclass
from typing import Any, Mapping

BACKEND_CONTRACT = "RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0"
PROCESS_ENVELOPE_SCHEMA = "RAWLSING_FIABC_P2X_CANDIDATE_PROCESS_ENVELOPE@1.0.0"
FREEZE_RECEIPT_SCHEMA = "RAWLSING_FIABC_CANDIDATE_NEUTRAL_FREEZE@2.0.0"
PROTOCOL_SCHEMA = "RAWLSING_FIABC_P2X_CELL_PROCESS_PROTOCOL@1.0.0"
PROTOCOL_PREFIX = "RAWLSING_FIABC_CELL_PROCESS "
OWNER_MARKER = ".fiabc_process_envelope_owner.json"

CELL_SOURCE_ENV = "RAWLSING_EE_P2X_CELL_SOURCE"
CELL_CANDIDATE_ENV = "RAWLSING_EE_P2X_CELL_CANDIDATE"
CELL_KEY_ENV = "RAWLSING_EE_P2X_CELL_KEY"
FREEZE_SHA_ENV = "RAWLSING_EE_P2X_UPSTREAM_FREEZE_SHA256"

COLD_REQUIRED = "COLD_REQUIRED"
SAME_CELL_RESUME_EXPLICIT = "SAME_CELL_RESUME_EXPLICIT"


class ProcessIsolationError(RuntimeError):
    pass


class FrozenUpstreamError(ProcessIsolationError):
    pass


class RootIsolationError(ProcessIsolationError):
    pass


class ColdStateViolation(ProcessIsolationError):
    pass


class ForeignCandidateStateError(ProcessIsolationError):
    pass


class PreStartContaminationError(ProcessIsolationError):
    pass


class CrossCandidateReuseError(ProcessIsolationError):
    pass


class WarmStatePolicyError(ProcessIsolationError):
    pass


class CellProcessProtocolError(ProcessIsolationError):
    pass


@dataclass(frozen=True)
class IsolatedBackendResult:
    terminal_disposition: str
    receipt: Mapping[str, Any]
    output_artifacts: Mapping[str, Path]
    verifier_complete: bool


@dataclass
class _ActiveLab:
    source: str
    candidate: str
    cell_key: str
    root: Path
    process: subprocess.Popen
    parent_start_monotonic_ns: int
    start_mode: str
    cold_observation: Mapping[str, Any]
    handshake: Mapping[str, Any]


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _json_line(value: Mapping[str, Any]) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"


def _is_under(path: Path, root: Path) -> bool:
    p = path.resolve()
    r = root.resolve()
    return p == r or r in p.parents


def _relative_file_inventory(root: Path) -> tuple[str, ...]:
    if not root.exists():
        return ()
    out: list[str] = []
    for path in root.rglob("*"):
        if path.is_file():
            out.append(path.relative_to(root).as_posix())
    return tuple(sorted(out))


def _is_sha256(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(ch in "0123456789abcdef" for ch in value.lower())
    )


def _validate_source_freeze_entry(source_key: str, entry: Any) -> Mapping[str, Any]:
    if not isinstance(entry, Mapping):
        raise FrozenUpstreamError(f"source freeze entry must be an object: {source_key}")
    source_id = entry.get("source_id")
    if not isinstance(source_id, str) or not source_id or source_id != source_key:
        raise FrozenUpstreamError(f"source freeze source_id mismatch: {source_key}")
    canonical = entry.get("canonical_source_sha256")
    if not _is_sha256(canonical):
        raise FrozenUpstreamError(f"canonical source SHA-256 malformed: {source_key}")
    authority_ref = entry.get("source_identity_authority_ref")
    if authority_ref in (None, "", {}, []):
        raise FrozenUpstreamError(f"source identity authority ref missing: {source_key}")
    derivative_identity = entry.get("derivative_identity")
    derivative_ref = entry.get("derivative_to_source_provenance_ref")
    if (derivative_identity is None) != (derivative_ref is None):
        raise FrozenUpstreamError(
            f"derivative identity and derivative-to-source provenance must be paired: {source_key}"
        )
    if derivative_identity is not None and derivative_identity in ("", {}, []):
        raise FrozenUpstreamError(f"derivative identity malformed: {source_key}")
    if derivative_ref is not None and derivative_ref in ("", {}, []):
        raise FrozenUpstreamError(f"derivative-to-source provenance ref malformed: {source_key}")
    return entry


def load_frozen_upstream_receipt(path: Path) -> tuple[Mapping[str, Any], str]:
    """Load the all-source candidate-neutral freeze receipt.

    The contract is source-family agnostic.  Each source entry binds the
    canonical physical root and its identity authority, plus paired derivative
    identity/provenance when a derivative is the admitted physical carrier.
    """
    p = path.resolve()
    if not p.is_file():
        raise FrozenUpstreamError(f"candidate-neutral freeze receipt missing: {p}")
    data = p.read_bytes()
    try:
        doc = json.loads(data.decode("utf-8"))
    except Exception as exc:
        raise FrozenUpstreamError("candidate-neutral freeze receipt is not valid JSON") from exc
    if not isinstance(doc, Mapping):
        raise FrozenUpstreamError("candidate-neutral freeze receipt must be an object")
    if doc.get("schema") != FREEZE_RECEIPT_SCHEMA:
        raise FrozenUpstreamError("candidate-neutral freeze receipt schema drift")
    if doc.get("candidate_neutral") is not True:
        raise FrozenUpstreamError("upstream freeze receipt is not candidate-neutral")
    if doc.get("frozen_before_candidate_execution") is not True:
        raise FrozenUpstreamError("upstream material was not frozen before candidate execution")
    for forbidden in ("candidate", "candidate_id", "candidate_owner", "selected_candidate"):
        if forbidden in doc:
            raise FrozenUpstreamError(
                f"candidate-specific field forbidden in upstream freeze receipt: {forbidden}"
            )

    if doc.get("candidate_outputs_seen") != 0:
        raise FrozenUpstreamError("oracle/source freeze occurred after candidate output")
    if doc.get("candidate_owned_roots_consulted") not in ([], ()):
        raise FrozenUpstreamError("candidate-owned roots were consulted while freezing upstream truth")
    if doc.get("candidate_owned_state_reused") is not False:
        raise FrozenUpstreamError("candidate-owned state was reused while freezing upstream truth")
    if doc.get("state") != "FROZEN_READ_ONLY":
        raise FrozenUpstreamError("upstream freeze receipt is not read-only frozen")

    source_freezes = doc.get("source_freezes")
    if not isinstance(source_freezes, Mapping) or not source_freezes:
        raise FrozenUpstreamError("source_freezes must be a non-empty source-keyed mapping")
    for source_key, entry in source_freezes.items():
        if not isinstance(source_key, str) or not source_key:
            raise FrozenUpstreamError("source_freezes contains an invalid source key")
        _validate_source_freeze_entry(source_key, entry)

    authority_identities = doc.get("authority_identities")
    workload_identities = doc.get("workload_identities")
    oracle_identities = doc.get("oracle_identities")
    if not isinstance(authority_identities, Mapping) or not authority_identities:
        raise FrozenUpstreamError("authority_identities must be a non-empty mapping")
    if not isinstance(workload_identities, Mapping) or not workload_identities:
        raise FrozenUpstreamError("workload_identities must be a non-empty mapping")
    if not isinstance(oracle_identities, Mapping):
        raise FrozenUpstreamError("oracle_identities must be a source-keyed mapping")
    if set(oracle_identities) != set(source_freezes):
        raise FrozenUpstreamError("oracle identities must cover exactly the frozen source set")
    for source_key, oracle in oracle_identities.items():
        if not isinstance(oracle, Mapping):
            raise FrozenUpstreamError(f"oracle identity entry must be an object: {source_key}")
        if not _is_sha256(oracle.get("oracle_identity_sha256")):
            raise FrozenUpstreamError(f"oracle identity malformed: {source_key}")
        if oracle.get("oracle_freeze_authority_ref") in (None, "", {}, []):
            raise FrozenUpstreamError(f"oracle freeze authority ref missing: {source_key}")

    order = doc.get("freeze_order")
    if not isinstance(order, Mapping):
        raise FrozenUpstreamError("freeze_order missing")
    keys = (
        "source_identity_freeze_sequence",
        "authority_workload_freeze_sequence",
        "oracle_materialize_freeze_sequence",
    )
    values = tuple(order.get(k) for k in keys)
    if not all(isinstance(v, int) and not isinstance(v, bool) and v >= 0 for v in values):
        raise FrozenUpstreamError("freeze_order sequences must be non-negative integers")
    if not (values[0] < values[1] < values[2]):
        raise FrozenUpstreamError(
            "freeze ordering must be source identity -> authority/workload -> oracle"
        )

    return doc, _sha256_bytes(data)

def _backend_loaded_in_parent(backend_spec: str) -> bool:
    if backend_spec.endswith(".py") or os.path.sep in backend_spec:
        target = Path(backend_spec).resolve()
        for module in tuple(sys.modules.values()):
            raw = getattr(module, "__file__", None)
            if raw:
                try:
                    if Path(raw).resolve() == target:
                        return True
                except Exception:
                    pass
        return False
    return backend_spec in sys.modules


def _candidate_owner_modules_in_parent() -> tuple[str, ...]:
    return tuple(sorted(name for name in sys.modules if name.startswith("_rawlsing_ee_p2x_owner_")))


def _resource_snapshot() -> Mapping[str, int]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "cpu_user_ns": max(0, int(usage.ru_utime * 1_000_000_000)),
        "cpu_system_ns": max(0, int(usage.ru_stime * 1_000_000_000)),
        "peak_rss_bytes": max(0, int(usage.ru_maxrss)),
    }


def _wire_context(context: Any, services: Any) -> Mapping[str, Any]:
    stage = context.stage
    roots = context.roots
    ident = context.map_identity
    return {
        "contract": context.contract,
        "stage": {
            "source": stage.source,
            "candidate": stage.candidate,
            "stage_id": stage.stage_id,
            "disposition": stage.disposition,
            "evidence_or_stop_law_ref": stage.evidence_or_stop_law_ref,
            "empirical_source_access_required": stage.empirical_source_access_required,
            "physical_host_measurement_required": stage.physical_host_measurement_required,
            "next_stage_on_pass": stage.next_stage_on_pass,
            "executable_prerequisite": stage.executable_prerequisite,
            "expected_output_receipt": stage.expected_output_receipt,
            "next_stage_on_candidate_local_failure": stage.next_stage_on_candidate_local_failure,
            "address": stage.address,
        },
        "work_root": str(Path(context.work_root).resolve()),
        "roots": {
            "root": str(Path(roots.root).resolve()),
            "scratch": str(Path(roots.scratch).resolve()),
            "durable": str(Path(roots.durable).resolve()),
            "logs": str(Path(roots.logs).resolve()),
            "receipts": str(Path(roots.receipts).resolve()),
        },
        "source_path": None if context.source_path is None else str(Path(context.source_path).resolve()),
        "source_sha256": context.source_sha256,
        "map_identity": {
            "schema": ident.schema,
            "sha256": ident.sha256,
            "git_blob_sha1": ident.git_blob_sha1,
        },
        "p2x_branch": context.p2x_branch,
        "observed_p2x_head": context.observed_p2x_head,
        "input_identity_hash": context.input_identity_hash,
        "services": {
            "repo_root": str(Path(services.repo_root).resolve()),
            "work_root": str(Path(services.work_root).resolve()),
        },
    }


def _simple_context_from_wire(wire: Mapping[str, Any]) -> tuple[Any, Any]:
    stage_doc = dict(wire["stage"])
    stage_doc.pop("address", None)
    stage = types.SimpleNamespace(**stage_doc)
    stage.address = wire["stage"]["address"]
    roots = types.SimpleNamespace(**{k: Path(v) for k, v in wire["roots"].items()})
    ident = types.SimpleNamespace(**wire["map_identity"])
    ctx = types.SimpleNamespace(
        contract=wire["contract"],
        stage=stage,
        work_root=Path(wire["work_root"]),
        roots=roots,
        source_path=None if wire["source_path"] is None else Path(wire["source_path"]),
        source_sha256=wire["source_sha256"],
        map_identity=ident,
        p2x_branch=wire["p2x_branch"],
        observed_p2x_head=wire["observed_p2x_head"],
        input_identity_hash=wire["input_identity_hash"],
    )
    services = types.SimpleNamespace(
        repo_root=Path(wire["services"]["repo_root"]),
        work_root=Path(wire["services"]["work_root"]),
    )
    return ctx, services


def _driver_context_from_wire(wire: Mapping[str, Any]) -> tuple[Any, Any]:
    from rawlsing_next import ee_p2x_darwin_court_driver as driver

    stage_doc = dict(wire["stage"])
    stage_doc.pop("address", None)
    stage = driver.StageSpec(**stage_doc)
    roots = driver.CandidateRoots(**{k: Path(v) for k, v in wire["roots"].items()})
    ident = driver.MapIdentity(**wire["map_identity"])
    ctx = driver.StageContext(
        wire["contract"],
        stage,
        Path(wire["work_root"]),
        roots,
        None if wire["source_path"] is None else Path(wire["source_path"]),
        wire["source_sha256"],
        ident,
        wire["p2x_branch"],
        wire["observed_p2x_head"],
        wire["input_identity_hash"],
    )
    services = driver.DriverServices(
        repo_root=Path(wire["services"]["repo_root"]),
        work_root=Path(wire["services"]["work_root"]),
    )
    return ctx, services


def _load_backend(backend_spec: str):
    if backend_spec.endswith(".py") or os.path.sep in backend_spec:
        path = Path(backend_spec).resolve()
        name = "_fiabc_cell_backend_" + hashlib.sha256(str(path).encode()).hexdigest()[:16]
        spec = importlib.util.spec_from_file_location(name, path)
        if not spec or not spec.loader:
            raise CellProcessProtocolError(f"unable to import backend path: {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            sys.modules.pop(name, None)
            raise
        return module
    return importlib.import_module(backend_spec)


def _normalize_backend_result(raw: Any) -> Mapping[str, Any]:
    if isinstance(raw, Mapping):
        terminal = raw.get("terminal_disposition", "PASS")
        receipt = raw.get("receipt", {})
        artifacts = raw.get("output_artifacts", {})
        complete = bool(raw.get("verifier_complete", False))
    else:
        terminal = getattr(raw, "terminal_disposition")
        receipt = getattr(raw, "receipt")
        artifacts = getattr(raw, "output_artifacts")
        complete = bool(getattr(raw, "verifier_complete"))
    return {
        "terminal_disposition": terminal,
        "receipt": dict(receipt),
        "output_artifacts": {str(k): str(v) for k, v in dict(artifacts).items()},
        "verifier_complete": complete,
    }


def _emit_protocol(value: Mapping[str, Any]) -> None:
    sys.stdout.write(PROTOCOL_PREFIX + json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n")
    sys.stdout.flush()


def _child_main(backend_spec: str, context_mode: str) -> int:
    first = sys.stdin.readline()
    if not first:
        return 70
    try:
        start = json.loads(first)
        if start.get("schema") != PROTOCOL_SCHEMA or start.get("op") != "START":
            raise CellProcessProtocolError("first child command must be START")
        source = start["source"]
        candidate = start["candidate"]
        cell_key = start["cell_key"]
        if os.environ.get(CELL_SOURCE_ENV) != source or os.environ.get(CELL_CANDIDATE_ENV) != candidate:
            raise CellProcessProtocolError("cell environment attribution mismatch")
        if os.environ.get(CELL_KEY_ENV) != cell_key:
            raise CellProcessProtocolError("cell key environment attribution mismatch")
        if os.environ.get(FREEZE_SHA_ENV) != start["freeze_receipt_sha256"]:
            raise CellProcessProtocolError("upstream freeze environment attribution mismatch")

        pre_import_ns = time.perf_counter_ns()
        pre_import_resource = _resource_snapshot()
        owner_modules_before = tuple(sorted(name for name in sys.modules if name.startswith("_rawlsing_ee_p2x_owner_")))
        if owner_modules_before:
            raise PreStartContaminationError(f"candidate owner module exists before backend import: {owner_modules_before}")

        backend = _load_backend(backend_spec)
        if getattr(backend, "BACKEND_CONTRACT", None) != BACKEND_CONTRACT:
            raise CellProcessProtocolError("inner backend contract mismatch")
        run_stage = getattr(backend, "run_stage", None)
        if not callable(run_stage):
            raise CellProcessProtocolError("inner backend run_stage is not callable")
        sessions = getattr(backend, "_SESSIONS", None)
        if sessions is not None and (not isinstance(sessions, Mapping) or len(sessions) != 0):
            raise PreStartContaminationError("inner backend session registry is non-empty at candidate process start")

        _emit_protocol({
            "schema": PROTOCOL_SCHEMA,
            "op": "HANDSHAKE",
            "source": source,
            "candidate": candidate,
            "cell_key": cell_key,
            "pid": os.getpid(),
            "ppid": os.getppid(),
            "parent_envelope_start_monotonic_ns": start["parent_envelope_start_monotonic_ns"],
            "child_pre_backend_import_monotonic_ns": pre_import_ns,
            "child_backend_import_complete_monotonic_ns": time.perf_counter_ns(),
            "pre_backend_import_resource": pre_import_resource,
            "post_backend_import_resource": _resource_snapshot(),
            "session_registry_empty_at_start": True,
            "candidate_owner_modules_before_backend_import": list(owner_modules_before),
            "rss_scope": "RUSAGE_SELF__THIS_CELL_PROCESS_ONLY",
            "environment_attribution": {
                CELL_SOURCE_ENV: source,
                CELL_CANDIDATE_ENV: candidate,
                CELL_KEY_ENV: cell_key,
                FREEZE_SHA_ENV: start["freeze_receipt_sha256"],
            },
        })

        while True:
            line = sys.stdin.readline()
            if not line:
                return 71
            command = json.loads(line)
            if command.get("schema") != PROTOCOL_SCHEMA:
                raise CellProcessProtocolError("protocol schema drift")
            if command.get("cell_key") != cell_key:
                raise CrossCandidateReuseError("command attempted to reuse a cell process for another cell")
            if command.get("op") == "RUN_STAGE":
                wire = command["context"]
                stage = wire["stage"]
                if stage["source"] != source or stage["candidate"] != candidate:
                    raise CrossCandidateReuseError("stage identity does not match sealed process cell")
                if context_mode == "DRIVER":
                    context, services = _driver_context_from_wire(wire)
                elif context_mode == "SIMPLE_TEST_ONLY":
                    context, services = _simple_context_from_wire(wire)
                else:
                    raise CellProcessProtocolError("unknown context reconstruction mode")
                raw = run_stage(context, services)
                _emit_protocol({
                    "schema": PROTOCOL_SCHEMA,
                    "op": "STAGE_RESULT",
                    "cell_key": cell_key,
                    "pid": os.getpid(),
                    "stage": stage["address"],
                    "result": _normalize_backend_result(raw),
                    "resource_after_stage": _resource_snapshot(),
                })
            elif command.get("op") == "STOP":
                sessions = getattr(backend, "_SESSIONS", None)
                session_keys = []
                if isinstance(sessions, Mapping):
                    session_keys = [list(k) if isinstance(k, tuple) else k for k in sessions.keys()]
                    for key in sessions.keys():
                        normalized = "/".join(key) if isinstance(key, tuple) else str(key)
                        if normalized != cell_key:
                            raise CrossCandidateReuseError(
                                f"foreign candidate session survived inside sealed process: {normalized}"
                            )
                stop_ns = time.perf_counter_ns()
                _emit_protocol({
                    "schema": PROTOCOL_SCHEMA,
                    "op": "STOPPED",
                    "source": source,
                    "candidate": candidate,
                    "cell_key": cell_key,
                    "pid": os.getpid(),
                    "child_process_stop_monotonic_ns": stop_ns,
                    "resource_at_stop": _resource_snapshot(),
                    "session_keys_at_stop": session_keys,
                    "reason": command.get("reason"),
                    "rss_scope": "RUSAGE_SELF__THIS_CELL_PROCESS_ONLY",
                })
                return 0
            else:
                raise CellProcessProtocolError("unknown child process operation")
    except Exception as exc:
        _emit_protocol({
            "schema": PROTOCOL_SCHEMA,
            "op": "ERROR",
            "error_type": type(exc).__name__,
            "error": str(exc),
            "pid": os.getpid(),
        })
        return 72


class ProcessIsolationController:
    """One active child at most; never a semantic/session registry in the parent."""

    def __init__(
        self,
        *,
        backend_spec: str,
        freeze_receipt_path: Path,
        resume_cells: tuple[str, ...] | list[str] | set[str] = (),
        warm_state_transitions: tuple[str, ...] | list[str] | set[str] = (),
        context_mode: str = "DRIVER",
    ):
        self.backend_spec = backend_spec
        self.freeze_receipt_path = Path(freeze_receipt_path).resolve()
        self.freeze_document, self.freeze_receipt_sha256 = load_frozen_upstream_receipt(self.freeze_receipt_path)
        self.resume_cells = frozenset(resume_cells)
        self.warm_state_transitions = frozenset(warm_state_transitions)
        self.context_mode = context_mode
        self._active: _ActiveLab | None = None

    @property
    def active_cell(self) -> str | None:
        return None if self._active is None else self._active.cell_key

    def _validate_freeze_for_context(self, context: Any) -> None:
        source = context.stage.source
        if source == "COURT":
            return
        source_freezes = self.freeze_document.get("source_freezes", {})
        if source not in source_freezes:
            raise FrozenUpstreamError(f"freeze receipt has no source freeze for {source}")
        entry = _validate_source_freeze_entry(source, source_freezes[source])
        if entry.get("canonical_source_sha256") != context.source_sha256:
            raise FrozenUpstreamError(f"freeze receipt canonical source identity drift for {source}")
        oracle = self.freeze_document.get("oracle_identities", {}).get(source)
        if not isinstance(oracle, Mapping) or not _is_sha256(oracle.get("oracle_identity_sha256")):
            raise FrozenUpstreamError(f"freeze receipt has no valid frozen oracle for {source}")

    def _validate_roots(self, context: Any) -> tuple[Path, Mapping[str, Any]]:
        source = context.stage.source
        candidate = context.stage.candidate
        work_root = Path(context.work_root).resolve()
        raw_paths = {
            "root": Path(context.roots.root),
            "scratch": Path(context.roots.scratch),
            "durable": Path(context.roots.durable),
            "logs": Path(context.roots.logs),
            "receipts": Path(context.roots.receipts),
        }
        for name, raw in raw_paths.items():
            if raw.is_symlink():
                raise RootIsolationError(f"candidate {name} root may not be a symlink")
        paths = {name: raw.resolve() for name, raw in raw_paths.items()}
        root = paths["root"]
        expected = (work_root / "cells" / source / candidate).resolve()
        if root != expected:
            raise RootIsolationError(f"candidate root drift: expected {expected}, got {root}")
        for name, path in paths.items():
            if not path.exists() or not path.is_dir():
                raise RootIsolationError(f"pre-provisioned candidate {name} root missing: {path}")
            if name != "root" and not _is_under(path, root):
                raise RootIsolationError(f"candidate {name} root escapes sealed cell root")
        if _is_under(self.freeze_receipt_path, work_root / "cells"):
            raise FrozenUpstreamError("candidate-neutral freeze receipt may not live inside a candidate cell root")

        marker = root / OWNER_MARKER
        if marker.exists():
            try:
                marker_doc = json.loads(marker.read_text(encoding="utf-8"))
            except Exception as exc:
                raise ForeignCandidateStateError("candidate process owner marker malformed") from exc
            if marker_doc.get("cell_key") != f"{source}/{candidate}":
                raise ForeignCandidateStateError("foreign candidate owner marker found in cell root")
            if marker_doc.get("state") == "ACTIVE":
                raise ForeignCandidateStateError("interrupted ACTIVE cell requires explicit lifecycle recovery before reuse")

        scratch_files = _relative_file_inventory(paths["scratch"])
        durable_files = _relative_file_inventory(paths["durable"])
        cell_key = f"{source}/{candidate}"
        start_mode = SAME_CELL_RESUME_EXPLICIT if cell_key in self.resume_cells else COLD_REQUIRED
        if source != "COURT" and start_mode == COLD_REQUIRED and (scratch_files or durable_files):
            raise ColdStateViolation(
                f"cold cell {cell_key} already has candidate-owned state: "
                f"scratch={scratch_files!r}, durable={durable_files!r}"
            )
        if source != "COURT" and start_mode == SAME_CELL_RESUME_EXPLICIT and marker.exists() is False:
            raise ColdStateViolation("same-cell resume requires an existing matching process-envelope owner marker")

        observation = {
            "start_mode": start_mode,
            "scratch_files_before_start": list(scratch_files),
            "durable_files_before_start": list(durable_files),
            "candidate_owned_warm_state_present": bool(scratch_files or durable_files),
            "cold_definition": "NO_CANDIDATE_OWNED_ACCELERATING_STATE__HOST_OS_CACHE_NOT_CLAIMED_COLD",
        }
        return root, observation

    def _read_protocol(self, process: subprocess.Popen, expected_op: str) -> Mapping[str, Any]:
        diagnostics: list[str] = []
        assert process.stdout is not None
        while True:
            line = process.stdout.readline()
            if line == "":
                rc = process.poll()
                raise CellProcessProtocolError(
                    f"cell process ended before {expected_op}; returncode={rc}; diagnostics={diagnostics[-20:]}"
                )
            line = line.rstrip("\n")
            if not line.startswith(PROTOCOL_PREFIX):
                diagnostics.append(line)
                continue
            try:
                doc = json.loads(line[len(PROTOCOL_PREFIX):])
            except Exception as exc:
                raise CellProcessProtocolError("malformed process protocol line") from exc
            if doc.get("op") == "ERROR":
                raise CellProcessProtocolError(
                    f"cell process error {doc.get('error_type')}: {doc.get('error')}"
                )
            if doc.get("op") != expected_op:
                raise CellProcessProtocolError(
                    f"expected child protocol op {expected_op}, got {doc.get('op')}"
                )
            return doc

    def _send(self, active: _ActiveLab, value: Mapping[str, Any]) -> None:
        if active.process.stdin is None:
            raise CellProcessProtocolError("cell process stdin unavailable")
        active.process.stdin.write(_json_line(value))
        active.process.stdin.flush()

    def _start(self, context: Any, services: Any) -> _ActiveLab:
        if self._active is not None:
            raise CellProcessProtocolError("internal error: attempted second active cell process")
        self._validate_freeze_for_context(context)
        root, cold = self._validate_roots(context)

        if _backend_loaded_in_parent(self.backend_spec):
            raise PreStartContaminationError("inner candidate backend was imported in parent before lawful cell start")
        owner_modules = _candidate_owner_modules_in_parent()
        if owner_modules:
            raise PreStartContaminationError(
                f"candidate owner modules initialized in parent before lawful cell start: {owner_modules}"
            )

        source = context.stage.source
        candidate = context.stage.candidate
        cell_key = f"{source}/{candidate}"
        start_mode = cold["start_mode"]
        parent_start_ns = time.perf_counter_ns()

        marker = root / OWNER_MARKER
        marker.write_text(
            json.dumps({
                "schema": PROCESS_ENVELOPE_SCHEMA,
                "cell_key": cell_key,
                "source": source,
                "candidate": candidate,
                "state": "ACTIVE",
                "parent_envelope_start_monotonic_ns": parent_start_ns,
                "freeze_receipt_sha256": self.freeze_receipt_sha256,
                "start_mode": start_mode,
            }, sort_keys=True, indent=2) + "\n",
            encoding="utf-8",
        )

        env = dict(os.environ)
        for key in (CELL_SOURCE_ENV, CELL_CANDIDATE_ENV, CELL_KEY_ENV, FREEZE_SHA_ENV):
            env.pop(key, None)
        if candidate != "A":
            env.pop("RAWLSING_EE_P2X_LITS_A_R5_ROOT", None)
        env[CELL_SOURCE_ENV] = source
        env[CELL_CANDIDATE_ENV] = candidate
        env[CELL_KEY_ENV] = cell_key
        env[FREEZE_SHA_ENV] = self.freeze_receipt_sha256
        env["PYTHONUNBUFFERED"] = "1"

        command = [
            sys.executable,
            "-m",
            "rawlsing_next.ee_p2x_candidate_process_envelope",
            "--child",
            "--backend-spec",
            self.backend_spec,
            "--context-mode",
            self.context_mode,
        ]
        process = subprocess.Popen(
            command,
            cwd=Path(services.repo_root).resolve(),
            env=env,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        provisional = _ActiveLab(
            source=source,
            candidate=candidate,
            cell_key=cell_key,
            root=root,
            process=process,
            parent_start_monotonic_ns=parent_start_ns,
            start_mode=start_mode,
            cold_observation=cold,
            handshake={},
        )
        try:
            self._send(provisional, {
                "schema": PROTOCOL_SCHEMA,
                "op": "START",
                "source": source,
                "candidate": candidate,
                "cell_key": cell_key,
                "parent_envelope_start_monotonic_ns": parent_start_ns,
                "freeze_receipt_sha256": self.freeze_receipt_sha256,
            })
            handshake = self._read_protocol(process, "HANDSHAKE")
        except Exception:
            process.kill()
            process.wait()
            marker.write_text(
                json.dumps({
                    "schema": PROCESS_ENVELOPE_SCHEMA,
                    "cell_key": cell_key,
                    "state": "ABORTED_DURING_START",
                    "parent_envelope_start_monotonic_ns": parent_start_ns,
                }, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )
            raise
        active = _ActiveLab(
            source=source,
            candidate=candidate,
            cell_key=cell_key,
            root=root,
            process=process,
            parent_start_monotonic_ns=parent_start_ns,
            start_mode=start_mode,
            cold_observation=cold,
            handshake=handshake,
        )
        self._active = active
        return active

    def _stop(self, reason: str) -> Mapping[str, Any]:
        active = self._active
        if active is None:
            raise CellProcessProtocolError("no active cell process to stop")
        try:
            self._send(active, {
                "schema": PROTOCOL_SCHEMA,
                "op": "STOP",
                "cell_key": active.cell_key,
                "reason": reason,
            })
            stop = self._read_protocol(active.process, "STOPPED")
            if active.process.stdin is not None:
                active.process.stdin.close()
            rc = active.process.wait(timeout=20)
            if rc != 0:
                raise CellProcessProtocolError(f"cell process stop returned nonzero: {rc}")
            marker = active.root / OWNER_MARKER
            marker.write_text(
                json.dumps({
                    "schema": PROCESS_ENVELOPE_SCHEMA,
                    "cell_key": active.cell_key,
                    "source": active.source,
                    "candidate": active.candidate,
                    "state": "STOPPED",
                    "parent_envelope_start_monotonic_ns": active.parent_start_monotonic_ns,
                    "child_process_stop_monotonic_ns": stop["child_process_stop_monotonic_ns"],
                    "freeze_receipt_sha256": self.freeze_receipt_sha256,
                    "start_mode": active.start_mode,
                    "process_pid": stop["pid"],
                }, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )
            parent_stop_ns = time.perf_counter_ns()
            return {
                **stop,
                "parent_envelope_stop_monotonic_ns": parent_stop_ns,
                "process_returncode": rc,
            }
        finally:
            self._active = None

    def _abort_active(self, reason: str) -> None:
        active = self._active
        if active is None:
            return
        try:
            if active.process.poll() is None:
                active.process.kill()
            active.process.wait()
        finally:
            marker = active.root / OWNER_MARKER
            marker.write_text(
                json.dumps({
                    "schema": PROCESS_ENVELOPE_SCHEMA,
                    "cell_key": active.cell_key,
                    "state": "ABORTED",
                    "reason": reason,
                    "parent_envelope_start_monotonic_ns": active.parent_start_monotonic_ns,
                }, sort_keys=True, indent=2) + "\n",
                encoding="utf-8",
            )
            self._active = None

    def close(self) -> None:
        if self._active is not None:
            self._abort_active("controller closed before lawful cell terminal")

    def run_stage(self, context: Any, services: Any) -> IsolatedBackendResult:
        source = context.stage.source
        candidate = context.stage.candidate
        cell_key = f"{source}/{candidate}"

        active = self._active
        if active is not None and active.cell_key != cell_key:
            raise CrossCandidateReuseError(
                f"active process belongs to {active.cell_key}; refusing stage for {cell_key}"
            )
        if active is None:
            active = self._start(context, services)

        if Path(context.roots.root).resolve() != active.root:
            raise RootIsolationError("same cell attempted to change roots during one process lifecycle")

        try:
            self._send(active, {
                "schema": PROTOCOL_SCHEMA,
                "op": "RUN_STAGE",
                "cell_key": cell_key,
                "context": _wire_context(context, services),
            })
            response = self._read_protocol(active.process, "STAGE_RESULT")
            raw_result = response["result"]
            terminal = raw_result["terminal_disposition"]
            next_stage = (
                context.stage.next_stage_on_pass
                if terminal == "PASS"
                else context.stage.next_stage_on_candidate_local_failure
            )
            same_cell_next = isinstance(next_stage, str) and next_stage.startswith(cell_key + "/")
            next_stage_id = next_stage.rsplit("/", 1)[-1] if same_cell_next else None
            warm_transition_token = (
                f"{context.stage.stage_id}>{next_stage_id}" if same_cell_next else None
            )
            warm_transition_authorized = (
                warm_transition_token in self.warm_state_transitions
                if warm_transition_token is not None
                else False
            )
            if same_cell_next and not warm_transition_authorized:
                raise WarmStatePolicyError(
                    "same-cell process retention would preserve possible candidate warm state "
                    f"without explicit lifecycle authorization: {warm_transition_token}"
                )
            must_stop = source == "COURT" or terminal != "PASS" or not same_cell_next
            stop = self._stop(
                "LAWFUL_CELL_TERMINAL_OR_TRANSITION"
            ) if must_stop else None

            process_envelope = {
                "schema": PROCESS_ENVELOPE_SCHEMA,
                "source": source,
                "candidate": candidate,
                "cell_key": cell_key,
                "candidate_neutral_freeze": {
                    "classification": "C0_SHARED_UPSTREAM__NOT_CANDIDATE_PRODUCTION_COST",
                    "receipt_path": str(self.freeze_receipt_path),
                    "receipt_sha256": self.freeze_receipt_sha256,
                },
                "candidate_local_boundary": {
                    "parent_envelope_start_monotonic_ns": active.parent_start_monotonic_ns,
                    "start_mode": active.start_mode,
                    "candidate_specific_backend_import_before_boundary": False,
                    "parent_backend_preimport_check": "PASS",
                    "parent_candidate_owner_module_preinit_check": "PASS",
                },
                "cold_state_observation": dict(active.cold_observation),
                "process": dict(active.handshake),
                "stage_process_pid": response["pid"],
                "resource_after_stage": response["resource_after_stage"],
                "child_process_attribution_environment_inherited_by_descendants": True,
                "lifecycle_process_retention": {
                    "next_stage": next_stage,
                    "same_cell_next": same_cell_next,
                    "authorization_token": warm_transition_token,
                    "authorized": warm_transition_authorized,
                    "policy_owner": "I06C_LIFECYCLE_INTEGRATION",
                },
                "stop": stop,
            }
            receipt = dict(raw_result["receipt"])
            if "process_envelope" in receipt:
                raise CellProcessProtocolError("inner backend may not overwrite process_envelope")
            receipt["process_envelope"] = process_envelope
            return IsolatedBackendResult(
                terminal_disposition=terminal,
                receipt=receipt,
                output_artifacts={str(k): Path(v) for k, v in raw_result["output_artifacts"].items()},
                verifier_complete=bool(raw_result["verifier_complete"]),
            )
        except Exception:
            if self._active is not None:
                self._abort_active("stage protocol or backend failure")
            raise


def _parser():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--child", action="store_true")
    parser.add_argument("--backend-spec")
    parser.add_argument("--context-mode", default="DRIVER")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if not args.child or not args.backend_spec:
        raise SystemExit("candidate process envelope is child-only when invoked as a module")
    return _child_main(args.backend_spec, args.context_mode)


if __name__ == "__main__":
    raise SystemExit(main())


__all__ = [
    "BACKEND_CONTRACT",
    "PROCESS_ENVELOPE_SCHEMA",
    "FREEZE_RECEIPT_SCHEMA",
    "COLD_REQUIRED",
    "SAME_CELL_RESUME_EXPLICIT",
    "ProcessIsolationController",
    "IsolatedBackendResult",
    "ProcessIsolationError",
    "FrozenUpstreamError",
    "RootIsolationError",
    "ColdStateViolation",
    "ForeignCandidateStateError",
    "PreStartContaminationError",
    "CrossCandidateReuseError",
    "WarmStatePolicyError",
    "CellProcessProtocolError",
    "load_frozen_upstream_receipt",
]
