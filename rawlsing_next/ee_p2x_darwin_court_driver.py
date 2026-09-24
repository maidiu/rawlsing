"""Deterministic Darwin orchestration for the resumed EE-P2X court.

Preparation/orchestration only: this module owns continuation-map law, exact
host/repository/source gates, P2R1 composition, accepted-owner deployment,
resumability, failure scoping, and supervisor tokens. Measured work is delegated
to one fixed backend contract; no performance values are invented here.
"""
from __future__ import annotations

import argparse
import contextlib
import dataclasses
import fcntl
import hashlib
import importlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import platform
import resource
import subprocess
import sys
import tempfile
import time
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence

CONTINUATION_MAP_SCHEMA = "RAWLSING_EE_P2X_CONTINUATION_STATE_MACHINE@1.0.0"
CONTINUATION_MAP_SHA256 = "ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422"
CONTINUATION_MAP_GIT_BLOB_SHA1 = "e06e95dd370a4fd44235932088308c3372522ed4"
CURRENT_EXECUTION_MANIFEST_SCHEMA = "RAWLSING_FIABC_CURRENT_SIX_CELL_EXECUTION_MANIFEST@1.0.0"
HISTORICAL_CONTINUATION_MAP_SHA256 = CONTINUATION_MAP_SHA256
HISTORICAL_CONTINUATION_MAP_GIT_BLOB_SHA1 = CONTINUATION_MAP_GIT_BLOB_SHA1
LITS_I_CANONICAL_SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
WVS7_CANONICAL_SOURCE_SHA256 = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
CANDIDATE_C_POLICY = "SOURCE_BACKED_HYBRID_WITH_REGENERABLE_ACCELERATORS"
P2X_BRANCH = "agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"
P2X_RESUME_HEAD = "a954e2d6676843da8427ef2439b5d1ef33478359"
P2R1_PASS = "9511f44728a8469d685463ec0fc880864c9187de"
P2R1_SEAM_PATH = "rawlsing_next/pre553_carrier_execution.py"
P2R1_SEAM_BLOB = "e7cda773e6a2426bfa12b22790fd8e005fe75153"
OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
EXPECTED_SOURCE_ORDER = ("LITS_I", "WVS7")
EXPECTED_CANDIDATE_ORDER = ("A", "B", "C")
EXPECTED_RUNTIME = {
    "implementation": "CPython", "python": "3.11.3", "pyreadstat": "1.3.6",
    "pyarrow": "25.0.1", "system": "Darwin", "machine": "x86_64",
}
LITS_A_ABSENT_ROOT_CURRENT_LAW = {
    "schema": "FIABC_LITS_A_ABSENT_ROOT_CURRENT_LAW@1.0.0",
    "local_verification_tip": "002e424294221f5edb73366286ffe6c8fb850a30",
    "local_verification_terminal": "FIABC_LITS_A_LOCAL_PARENTAGE_VERIFY__HISTORICAL_ROOT_NOT_PRESENT__NO_REBUILD_PERFORMED",
    "historical_root": "e8f37557493b816e4562f5f47df110cf49b429e9ead54e5b624d6638ee07aa3d",
    "historical_root_current_host_state": "ABSENT",
    "historical_semantic_build_evidence": "RETAINED_AS_HISTORY",
    "current_physical_realization": "ABSENT_BEFORE_S01",
    "preserved_s01_physical_work_credit": "ZERO__NOT_AVAILABLE",
    "historical_r35_parentage": "NOT_APPLICABLE_TO_CURRENT_EXECUTION_BECAUSE_ROOT_ABSENT",
    "prebuild_required": False,
    "current_s01_action": "ONE_GOVERNED_MEASURED_CANDIDATE_A_BUILD_FROM_ABSENT_TARGET",
    "separate_r35_prebuild_allowed": False,
    "current_s01_parentage": "MINT_FROM_SAME_BUILD",
    "current_s01_physical_realization": "SEED_FROM_SAME_BUILD__R35_I03_PASS_NOT_PRECLAIMED",
}
R8B_RU_MAXRSS_LAW = "DARWIN_RU_MAXRSS_ALREADY_BYTES"
LEDGER_SCHEMA = "RAWLSING_EE_P2X_DARWIN_STAGE_LEDGER@1.0.0"
BACKEND_CONTRACT = "RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0"
SUPERVISOR_TOKEN_SCHEMA = "RAWLSING_EE_P2X_LOCAL_SUPERVISOR_ACTION@1.0.0"
PROGRESS_SCHEMA = "RAWLSING_FIABC_DRIVER_PROGRESS@1.0.0"
ISOLATED_BACKEND_MODULE = "rawlsing_next.ee_p2x_process_isolated_backend"
FROZEN_UPSTREAM_ENV = "RAWLSING_EE_P2X_FROZEN_UPSTREAM_RECEIPT"
OWNER_SPECS = {
    "A": {"path": "rawlsing_next/pre553_r5_source_backed_adapter.py", "blob": "d4915e7e6755ba1850756aebff72f982f73a332b", "builder": "build_r5_source_backed_c11_repository"},
    "B": {"path": "rawlsing_next/pre553_source_backed_c11_facade.py", "blob": "7c509c2098d0030f253344eb3f682471378812a8", "builder": "build_source_backed_c11_repository"},
    "C": {"path": "rawlsing_next/pre553_route_c_accelerators.py", "blob": "abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889", "builder": "build_route_c_repository"},
}
COMPLETE_LEDGER_DISPOSITIONS = frozenset({
    "PASS", "PRESERVED", "SKIPPED_BY_FROZEN_LAW", "CANDIDATE_LOCAL_FAILURE",
    "BLOCKED_BY_COMMON_SOURCE_AUTHORITY", "BLOCKED_BY_COMMON_COURT_AUTHORITY",
})

class CourtDriverError(RuntimeError): pass
class RuntimeGateError(CourtDriverError): pass
class ContinuationMapError(CourtDriverError): pass
class StageStateError(CourtDriverError): pass
class OwnerDeploymentError(CourtDriverError): pass
class StageExecutionError(CourtDriverError): pass

class CandidateLocalFailure(StageExecutionError):
    def __init__(self, message: str, *, receipt: Mapping[str, Any] | None = None):
        super().__init__(message); self.receipt = dict(receipt or {})

class CommonAuthorityBlocker(StageExecutionError):
    def __init__(self, message: str, *, scope: str, receipt: Mapping[str, Any] | None = None):
        if scope not in {"SOURCE", "COURT"}: raise ValueError("scope must be SOURCE or COURT")
        super().__init__(message); self.scope = scope; self.receipt = dict(receipt or {})

@dataclasses.dataclass(frozen=True)
class MapIdentity: schema: str; sha256: str; git_blob_sha1: str
@dataclasses.dataclass(frozen=True)
class HostFingerprint:
    implementation: str; python: str; system: str; machine: str
    dependency_versions: Mapping[str, str]; ru_maxrss_value: int
    ru_maxrss_unit_law: str = R8B_RU_MAXRSS_LAW
@dataclasses.dataclass(frozen=True)
class RepoFingerprint:
    branch: str; head: str; resume_head_is_ancestor: bool; p2r1_seam_blob: str
@dataclasses.dataclass(frozen=True)
class StageSpec:
    source: str; candidate: str; stage_id: str; disposition: str
    evidence_or_stop_law_ref: str | None; empirical_source_access_required: bool
    physical_host_measurement_required: bool; next_stage_on_pass: str
    executable_prerequisite: str; expected_output_receipt: str
    next_stage_on_candidate_local_failure: str
    @property
    def address(self) -> str:
        return f"COURT/{self.stage_id}" if self.source == "COURT" else f"{self.source}/{self.candidate}/{self.stage_id}"
@dataclasses.dataclass(frozen=True)
class CandidateRoots: root: Path; scratch: Path; durable: Path; logs: Path; receipts: Path
@dataclasses.dataclass(frozen=True)
class StageContext:
    contract: str; stage: StageSpec; work_root: Path; roots: CandidateRoots
    source_path: Path | None; source_sha256: str; map_identity: MapIdentity
    p2x_branch: str; observed_p2x_head: str; input_identity_hash: str
@dataclasses.dataclass(frozen=True)
class BackendResult:
    terminal_disposition: str; receipt: Mapping[str, Any]
    output_artifacts: Mapping[str, Path] = dataclasses.field(default_factory=dict)
    verifier_complete: bool = True
class StageBackend(Protocol):
    def run_stage(self, context: StageContext, services: "DriverServices") -> BackendResult: ...
@dataclasses.dataclass(frozen=True)
class StateMachine:
    document: Mapping[str, Any]; identity: MapIdentity; stages: Mapping[str, StageSpec]
    first_unfinished: str; final_stage_id: str
    def get(self, address: str) -> StageSpec:
        try: return self.stages[address]
        except KeyError as exc: raise ContinuationMapError(f"unknown continuation stage {address!r}") from exc


def _manifest_ordered_stage_ids(document: Mapping[str, Any], cell: Mapping[str, Any]) -> tuple[str, ...]:
    stages = cell.get("stages", {})
    if not isinstance(stages, Mapping):
        raise StageStateError("manifest progress cell stages must be a mapping")
    catalog = tuple(x for x in document.get("stage_catalog", ()) if isinstance(x, str))
    return tuple([sid for sid in catalog if sid in stages] + [sid for sid in stages if sid not in catalog])


@dataclasses.dataclass(frozen=True)
class ProgressPosition:
    address: str
    overall_index: int
    overall_total: int
    executable_index: int | None
    executable_total: int
    cell_index: int | None
    cell_total: int
    source: str
    candidate: str
    source_name: str
    candidate_name: str
    stage_id: str
    stage_index: int | None
    stage_total: int | None
    is_court_final: bool


class ManifestProgressPlan:
    """Manifest-derived court-administration ordinals; never evidentiary metrics."""

    def __init__(self, machine: StateMachine):
        self.machine = machine
        doc = machine.document
        cells = doc.get("cells", ())
        if not isinstance(cells, list) or not cells:
            raise StageStateError("progress plan requires manifest cells")
        self.cells = tuple(cells)
        self.cell_addresses: dict[tuple[str, str], tuple[str, ...]] = {}
        self.cell_meta: dict[tuple[str, str], Mapping[str, Any]] = {}
        flattened: list[str] = []
        sources = doc.get("sources", {}) if isinstance(doc.get("sources", {}), Mapping) else {}
        for cell_index, cell in enumerate(cells, 1):
            source, candidate = cell.get("source"), cell.get("candidate")
            if not isinstance(source, str) or not isinstance(candidate, str):
                raise StageStateError("progress plan cell source/candidate malformed")
            key = (source, candidate)
            if key in self.cell_addresses:
                raise StageStateError(f"progress plan duplicate cell {source}/{candidate}")
            stage_ids = _manifest_ordered_stage_ids(doc, cell)
            addresses = tuple(f"{source}/{candidate}/{sid}" for sid in stage_ids)
            for address in addresses:
                machine.get(address)
            self.cell_addresses[key] = addresses
            src_doc = sources.get(source, {}) if isinstance(sources.get(source, {}), Mapping) else {}
            self.cell_meta[key] = {
                "cell_index": cell_index,
                "source_name": str(
                    cell.get("source_name")
                    or src_doc.get("display_name")
                    or src_doc.get("name")
                    or src_doc.get("label")
                    or source
                ),
                "candidate_name": str(cell.get("candidate_name") or candidate),
                "stage_ids": stage_ids,
            }
            flattened.extend(addresses)
        if machine.final_stage_id not in flattened:
            machine.get(machine.final_stage_id)
            flattened.append(machine.final_stage_id)
        try:
            entry_index = flattened.index(machine.first_unfinished)
        except ValueError as exc:
            raise StageStateError("progress entry stage is absent from manifest ordering") from exc
        governed = tuple(flattened[entry_index:])
        executable = tuple(
            address for address in governed
            if machine.get(address).disposition == "READY__RUN_LOCALLY"
        )
        self.governed_addresses = governed
        self.executable_addresses = executable
        self._overall = {address: i for i, address in enumerate(governed, 1)}
        self._executable = {address: i for i, address in enumerate(executable, 1)}

    @property
    def overall_total(self) -> int:
        return len(self.governed_addresses)

    @property
    def executable_total(self) -> int:
        return len(self.executable_addresses)

    @property
    def cell_total(self) -> int:
        return len(self.cells)

    def position(self, address: str) -> ProgressPosition:
        if address not in self._overall:
            raise StageStateError(f"progress address precedes current manifest entry or is unknown: {address}")
        stage = self.machine.get(address)
        if stage.source == "COURT":
            return ProgressPosition(
                address=address,
                overall_index=self._overall[address],
                overall_total=self.overall_total,
                executable_index=self._executable.get(address),
                executable_total=self.executable_total,
                cell_index=None,
                cell_total=self.cell_total,
                source=stage.source,
                candidate=stage.candidate,
                source_name="COURT",
                candidate_name=stage.candidate,
                stage_id=stage.stage_id,
                stage_index=None,
                stage_total=None,
                is_court_final=True,
            )
        key = (stage.source, stage.candidate)
        meta = self.cell_meta[key]
        stage_ids = meta["stage_ids"]
        return ProgressPosition(
            address=address,
            overall_index=self._overall[address],
            overall_total=self.overall_total,
            executable_index=self._executable.get(address),
            executable_total=self.executable_total,
            cell_index=int(meta["cell_index"]),
            cell_total=self.cell_total,
            source=stage.source,
            candidate=stage.candidate,
            source_name=str(meta["source_name"]),
            candidate_name=str(meta["candidate_name"]),
            stage_id=stage.stage_id,
            stage_index=stage_ids.index(stage.stage_id) + 1,
            stage_total=len(stage_ids),
            is_court_final=False,
        )


class ProgressReporter:
    """Append-only C4 progress telemetry, intentionally separate from candidate metrics."""

    def __init__(
        self,
        machine: StateMachine,
        ledger: "StageLedger",
        *,
        stream=None,
        clock: Callable[[], int] = time.perf_counter_ns,
    ):
        self.machine = machine
        self.ledger = ledger
        self.plan = ManifestProgressPlan(machine)
        self.stream = sys.stderr if stream is None else stream
        self.clock = clock
        self.path = ledger.work_root / "fiabc_driver_progress.jsonl"
        self._seen: set[str] = set()
        if self.path.exists():
            for line_no, raw in enumerate(self.path.read_text(encoding="utf-8").splitlines(), 1):
                if not raw.strip():
                    continue
                try:
                    doc = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise StageStateError(f"progress JSONL malformed at line {line_no}") from exc
                event_id = doc.get("event_identity")
                if isinstance(event_id, str):
                    self._seen.add(event_id)

    def now_ns(self) -> int:
        return int(self.clock())

    def _resource_snapshot(self) -> Mapping[str, Any] | None:
        try:
            usage = resource.getrusage(resource.RUSAGE_SELF)
            return {
                "platform": platform.system(),
                "ru_maxrss_raw": int(usage.ru_maxrss),
                "ru_maxrss_unit": (
                    "bytes" if platform.system() == "Darwin"
                    else "platform_native_uninterpreted"
                ),
                "cpu_user_seconds": float(usage.ru_utime),
                "cpu_system_seconds": float(usage.ru_stime),
            }
        except Exception:
            return None

    def _append(self, event: Mapping[str, Any], identity_basis: Mapping[str, Any]) -> bool:
        event_id = _semantic_hash({
            "schema": PROGRESS_SCHEMA,
            "manifest_sha256": self.machine.identity.sha256,
            **identity_basis,
        })
        if event_id in self._seen:
            return False
        payload = {
            "schema": PROGRESS_SCHEMA,
            "event_identity": event_id,
            "manifest": dataclasses.asdict(self.machine.identity),
            "court_administration_only": True,
            "evidentiary_measurement": False,
            **event,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        self._seen.add(event_id)
        return True

    @staticmethod
    def _stage_name(stage_id: str) -> str:
        return stage_id.split("_", 1)[1] if "_" in stage_id else stage_id

    def emit_stage(
        self,
        stage: StageSpec,
        state: str,
        *,
        next_stage: str | None,
        elapsed_stage_ns: int | None,
        terminal_disposition: str | None = None,
    ) -> None:
        pos = self.plan.position(stage.address)
        event = {
            "event_type": "STAGE",
            "state": state,
            "address": stage.address,
            "overall": {"index": pos.overall_index, "total": pos.overall_total},
            "executable": {
                "index": pos.executable_index,
                "total": pos.executable_total,
                "is_executable": stage.disposition == "READY__RUN_LOCALLY",
            },
            "cell": (
                None if pos.cell_index is None else
                {"index": pos.cell_index, "total": pos.cell_total}
            ),
            "source": pos.source,
            "candidate": pos.candidate,
            "source_name": pos.source_name,
            "candidate_name": pos.candidate_name,
            "stage": {
                "id": pos.stage_id,
                "name": self._stage_name(pos.stage_id),
                "index": pos.stage_index,
                "total": pos.stage_total,
                "is_court_final": pos.is_court_final,
            },
            "manifest_disposition": stage.disposition,
            "terminal_disposition": terminal_disposition,
            "next_stage": next_stage,
            "elapsed_stage_ns": elapsed_stage_ns,
            "elapsed_clock": "time.perf_counter_ns",
            "resource_snapshot": self._resource_snapshot(),
        }
        appended = self._append(
            event,
            {"event_type": "STAGE", "address": stage.address, "state": state},
        )
        if not appended:
            return
        width = max(3, len(str(pos.overall_total)))
        overall = f"[{pos.overall_index:0{width}d}/{pos.overall_total}]"
        if pos.is_court_final:
            lead = f"FIABC P2 {overall} COURT STAGE {pos.stage_id}"
        else:
            exec_part = (
                f" EXEC {pos.executable_index}/{pos.executable_total}"
                if pos.executable_index is not None else ""
            )
            lead = (
                f"FIABC P2 {overall}{exec_part} CELL {pos.cell_index}/{pos.cell_total} "
                f"{pos.source_name}/{pos.candidate_name} STAGE {pos.stage_id} "
                f"[{pos.stage_index}/{pos.stage_total}] {self._stage_name(pos.stage_id)}"
            )
        elapsed = "" if elapsed_stage_ns is None else f" elapsed_stage={elapsed_stage_ns / 1_000_000_000:.3f}s"
        nxt = "" if next_stage is None else f" next={next_stage}"
        print(f"{lead} {state}{elapsed}{nxt}", file=self.stream, flush=True)

    def emit_completed_cells(self) -> None:
        for key, addresses in self.plan.cell_addresses.items():
            entries = [self.ledger.stage_entry(a) for a in addresses]
            if not addresses or any(
                not e or e.get("terminal_disposition") not in COMPLETE_LEDGER_DISPOSITIONS
                for e in entries
            ):
                continue
            terminal_dispositions = [e["terminal_disposition"] for e in entries]
            if any(x.startswith("BLOCKED_BY_COMMON_") for x in terminal_dispositions):
                state = "BLOCKED"
            elif "CANDIDATE_LOCAL_FAILURE" in terminal_dispositions:
                state = "CANDIDATE_LOCAL_FAILURE"
            else:
                state = "PASS"
            meta = self.plan.cell_meta[key]
            event = {
                "event_type": "CELL_TERMINAL",
                "state": state,
                "cell": {"index": meta["cell_index"], "total": self.plan.cell_total},
                "source": key[0],
                "candidate": key[1],
                "source_name": meta["source_name"],
                "candidate_name": meta["candidate_name"],
                "terminal_dispositions": terminal_dispositions,
                "cell_terminal_status": "COMPLETE",
                "resource_snapshot": self._resource_snapshot(),
            }
            if self._append(
                event,
                {"event_type": "CELL_TERMINAL", "source": key[0], "candidate": key[1], "state": state},
            ):
                print(
                    f"FIABC P2 CELL {meta['cell_index']}/{self.plan.cell_total} "
                    f"{meta['source_name']}/{meta['candidate_name']} COMPLETE status={state}",
                    file=self.stream,
                    flush=True,
                )

    def emit_court_terminal(self, *, status: str, next_stage: str, ledger_sha256: str) -> None:
        state = (
            "PASS" if status == "COURT_SEQUENCE_COMPLETE__S17_VERIFIED"
            else "CANDIDATE_LOCAL_FAILURE" if "CANDIDATE_LOCAL_FAILURE" in status
            else "BLOCKED"
        )
        event = {
            "event_type": "COURT_TERMINAL",
            "state": state,
            "terminal": status,
            "next_stage": next_stage,
            "ledger_sha256": ledger_sha256,
            "overall_total": self.plan.overall_total,
            "executable_total": self.plan.executable_total,
            "cell_total": self.plan.cell_total,
            "resource_snapshot": self._resource_snapshot(),
        }
        if self._append(
            event,
            {"event_type": "COURT_TERMINAL", "terminal": status, "next_stage": next_stage},
        ):
            print(
                f"FIABC P2 COURT TERMINAL {status} ledger={ledger_sha256} next={next_stage}",
                file=self.stream,
                flush=True,
            )

# ---- byte, git, host and map authority -------------------------------------------------
def _canonical_bytes(v: Any) -> bytes: return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
def _semantic_hash(v: Any) -> str: return hashlib.sha256(_canonical_bytes(v)).hexdigest()
def _sha256_bytes(v: bytes) -> str: return hashlib.sha256(v).hexdigest()
def _git_blob_sha1(v: bytes) -> str: return hashlib.sha1(f"blob {len(v)}\0".encode() + v).hexdigest()
def _sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(8 * 1024 * 1024), b""): h.update(chunk)
    return h.hexdigest()
def _atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent); tmp = Path(name)
    try:
        with os.fdopen(fd, "wb") as f: f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        with contextlib.suppress(FileNotFoundError): tmp.unlink()
def _atomic_write_json(path: Path, v: Mapping[str, Any]) -> str:
    data = json.dumps(v, sort_keys=True, indent=2, ensure_ascii=False).encode() + b"\n"; _atomic_write_bytes(path, data); return _sha256_bytes(data)
def _run_git(root: Path, *args: str, check: bool = True):
    return subprocess.run(["git", "-C", str(root), *args], check=check, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
def _git_show_bytes(root: Path, commit: str, path: str) -> bytes:
    if _run_git(root, "cat-file", "-e", f"{commit}^{{commit}}", check=False).returncode:
        if _run_git(root, "fetch", "--no-tags", "origin", commit, check=False).returncode:
            raise CourtDriverError(f"required immutable commit unavailable: {commit}")
    p = subprocess.run(["git", "-C", str(root), "show", f"{commit}:{path}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode: raise CourtDriverError(f"required immutable object unavailable: {commit}:{path}")
    return p.stdout

def observe_host() -> HostFingerprint:
    deps = {}
    for pkg in ("pyreadstat", "pyarrow"):
        try: deps[pkg] = importlib.metadata.version(pkg)
        except importlib.metadata.PackageNotFoundError: deps[pkg] = "MISSING"
    v = sys.version_info
    return HostFingerprint(platform.python_implementation(), f"{v.major}.{v.minor}.{v.micro}", platform.system(), platform.machine(), deps, int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
def verify_runtime_gate(h: HostFingerprint) -> None:
    got = {"implementation": h.implementation, "python": h.python, "system": h.system, "machine": h.machine, "pyreadstat": h.dependency_versions.get("pyreadstat", "MISSING"), "pyarrow": h.dependency_versions.get("pyarrow", "MISSING")}
    drift = {k: (got.get(k), v) for k, v in EXPECTED_RUNTIME.items() if got.get(k) != v}
    if drift: raise RuntimeGateError(f"Darwin runtime gate drift: {drift}")
    if h.ru_maxrss_unit_law != R8B_RU_MAXRSS_LAW or h.ru_maxrss_value < 0: raise RuntimeGateError("accepted R8B ru_maxrss law not bound")
def observe_repo(root: Path) -> RepoFingerprint:
    branch = _run_git(root, "branch", "--show-current").stdout.strip(); head = _run_git(root, "rev-parse", "HEAD").stdout.strip()
    anc = _run_git(root, "merge-base", "--is-ancestor", P2X_RESUME_HEAD, "HEAD", check=False).returncode == 0
    seam = _run_git(root, "rev-parse", f"HEAD:{P2R1_SEAM_PATH}", check=False); blob = seam.stdout.strip() if seam.returncode == 0 else "MISSING"
    return RepoFingerprint(branch, head, anc, blob)
def verify_repo_gate(r: RepoFingerprint) -> None:
    if r.branch != P2X_BRANCH: raise RuntimeGateError(f"driver must run on existing P2X branch {P2X_BRANCH}")
    if not r.resume_head_is_ancestor: raise RuntimeGateError("frozen P2X resume head is not an ancestor of HEAD")
    if r.p2r1_seam_blob != P2R1_SEAM_BLOB: raise RuntimeGateError("adopted P2R1 seam blob identity drift")

def _stage_tuple(v: Any, address: str):
    if not isinstance(v, list) or len(v) != 5: raise ContinuationMapError(f"{address}: stage tuple must have five fields")
    d, e, sa, m, n = v
    if d not in {"DONE__PRESERVE", "READY__RUN_LOCALLY", "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW", "TERMINAL_CANDIDATE_LOCAL_FAILURE__PRESERVE"}: raise ContinuationMapError(f"{address}: unknown disposition")
    if e is not None and not isinstance(e, str): raise ContinuationMapError(f"{address}: malformed evidence ref")
    if not isinstance(sa, bool) or not isinstance(m, bool) or not isinstance(n, str) or not n: raise ContinuationMapError(f"{address}: malformed tuple")
    if d != "READY__RUN_LOCALLY" and (sa or m): raise ContinuationMapError(f"{address}: executable {d} is forbidden")
    return d, e, sa, m, n

def _validate_stage_tuple(value: Any, *, address: str):
    return _stage_tuple(value, address)

def validate_state_machine(doc: Mapping[str, Any], ident: MapIdentity) -> StateMachine:
    if doc.get("schema") != CONTINUATION_MAP_SCHEMA: raise ContinuationMapError("continuation map schema drift")
    if tuple(doc.get("source_order", ())) != EXPECTED_SOURCE_ORDER: raise ContinuationMapError("source order drift")
    if tuple(doc.get("candidate_order", ())) != EXPECTED_CANDIDATE_ORDER: raise ContinuationMapError("candidate order drift")
    auth = doc.get("authority", {})
    for k, v in {"p2x_branch": P2X_BRANCH, "p2x_resume_head": P2X_RESUME_HEAD, "p2r1_pass": P2R1_PASS, "p2r1_seam_path": P2R1_SEAM_PATH, "p2r1_seam_blob": P2R1_SEAM_BLOB}.items():
        if auth.get(k) != v: raise ContinuationMapError(f"authority drift for {k}")
    if tuple(doc.get("stage_tuple_schema", ())) != ("disposition", "evidence_or_stop_law_ref", "empirical_source_access_required", "physical_host_measurement_required", "next_stage_on_pass"): raise ContinuationMapError("stage tuple schema drift")
    cells = doc.get("cells")
    if not isinstance(cells, list) or [(c.get("source"), c.get("candidate")) for c in cells] != [(s, c) for s in EXPECTED_SOURCE_ORDER for c in EXPECTED_CANDIDATE_ORDER]: raise ContinuationMapError("source×candidate cell order drift")
    evidence, laws = doc.get("evidence", {}), doc.get("stop_laws", {})
    stages: dict[str, StageSpec] = {}
    for cell in cells:
        source, candidate, sm = cell["source"], cell["candidate"], cell.get("stages")
        prereq, receipt, fail = cell.get("prerequisite_ref"), cell.get("expected_receipt"), cell.get("candidate_local_failure_next")
        if not isinstance(sm, Mapping) or not all(isinstance(x, str) and x for x in (prereq, receipt, fail)): raise ContinuationMapError(f"{source}/{candidate}: inherited fields incomplete")
        for sid, raw in sm.items():
            address = f"{source}/{candidate}/{sid}"; d, e, sa, m, n = _stage_tuple(raw, address)
            if e is not None and e not in evidence and e not in laws: raise ContinuationMapError(f"{address}: unknown evidence/stop-law")
            n = f"{source}/{candidate}/{n}" if n in sm else n
            stages[address] = StageSpec(source, candidate, sid, d, e, sa, m, n, prereq, f"{receipt}#{sid}", fail)
    first = doc.get("entry_guard", {}).get("first_unfinished_court_stage")
    if first != "LITS_I/A/S02_C11_REACHABILITY" or first not in stages: raise ContinuationMapError("first unfinished stage drift")
    wc = stages.get("WVS7/C/S01_CANDIDATE_PREPARATION_BUILD")
    if not wc or wc.disposition != "TERMINAL_CANDIDATE_LOCAL_FAILURE__PRESERVE" or wc.evidence_or_stop_law_ref != "WVS_C_FAILURE": raise ContinuationMapError("WVS-C portability failure drift")
    for sid in doc.get("stage_catalog", ()):
        if sid in {"S00_SOURCE_PREFLIGHT_IDENTITY", "S01_CANDIDATE_PREPARATION_BUILD"}: continue
        if stages[f"WVS7/C/{sid}"].disposition != "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW": raise ContinuationMapError("executable WVS-C fallback is forbidden")
    final = doc.get("final_stage", {})
    if final.get("stage_id") != "S17_FINAL_COMPLETENESS_AND_VERIFICATION" or final.get("wake_on_pass") != "HQ_MEASURED_SYNTHESIS" or not isinstance(final.get("expected_outputs"), list): raise ContinuationMapError("final court stage drift")
    fa = "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"
    stages[fa] = StageSpec("COURT", "ALL", "S17_FINAL_COMPLETENESS_AND_VERIFICATION", "READY__RUN_LOCALLY", None, False, False, "__COURT_COMPLETE__", "ALL_SIX_CELLS_LAWFULLY_TERMINAL__NO_UNRESOLVED_COMMON_BLOCKER", "|".join(final["expected_outputs"]), "__FORBIDDEN_FINAL_STAGE_CANDIDATE_LOCAL_FAILURE__")
    return StateMachine(doc, ident, stages, first, fa)
def load_continuation_map(path: Path) -> StateMachine:
    data = path.read_bytes(); ident = MapIdentity(CONTINUATION_MAP_SCHEMA, _sha256_bytes(data), _git_blob_sha1(data))
    if ident.sha256 != CONTINUATION_MAP_SHA256 or ident.git_blob_sha1 != CONTINUATION_MAP_GIT_BLOB_SHA1: raise ContinuationMapError("continuation map exact identity drift")
    doc = json.loads(data.decode());
    if not isinstance(doc, Mapping): raise ContinuationMapError("continuation map top level must be mapping")
    return validate_state_machine(doc, ident)


def validate_current_execution_manifest(doc: Mapping[str, Any], ident: MapIdentity) -> StateMachine:
    if doc.get("schema") != CURRENT_EXECUTION_MANIFEST_SCHEMA or ident.schema != CURRENT_EXECUTION_MANIFEST_SCHEMA:
        raise ContinuationMapError("current six-cell execution manifest schema drift")
    if tuple(doc.get("source_order", ())) != EXPECTED_SOURCE_ORDER or tuple(doc.get("candidate_order", ())) != EXPECTED_CANDIDATE_ORDER:
        raise ContinuationMapError("current six-cell source/candidate order drift")
    expected_pairs = tuple((s, c) for s in EXPECTED_SOURCE_ORDER for c in EXPECTED_CANDIDATE_ORDER)
    capabilities = doc.get("current_capabilities")
    if not isinstance(capabilities, list) or tuple((x.get("source"), x.get("candidate")) for x in capabilities) != expected_pairs:
        raise ContinuationMapError("current manifest must admit exactly the six LiTS-I/WVS7 x A/B/C cells")
    if any(x.get("status") != "CURRENT_EXECUTABLE" for x in capabilities):
        raise ContinuationMapError("all six current capabilities must be executable")
    sources = doc.get("sources", {})
    expected_roots = {"LITS_I": LITS_I_CANONICAL_SOURCE_SHA256, "WVS7": WVS7_CANONICAL_SOURCE_SHA256}
    if {k: sources.get(k, {}).get("sha256") for k in expected_roots} != expected_roots:
        raise ContinuationMapError("canonical source-root identity drift")
    root_law = doc.get("source_root_law", {})
    if root_law.get("same_canonical_root_required_across_candidates") is not True:
        raise ContinuationMapError("source-root equality law missing")
    if root_law.get("alternate_edition_export_cleaned_source_allowed") is not False:
        raise ContinuationMapError("alternate source artifact admitted")
    if root_law.get("canonical_source_sha256") != expected_roots:
        raise ContinuationMapError("source-root law does not close to canonical sources")
    derivative = root_law.get("preserved_or_prebuilt_derivative_substitution", {})
    if derivative.get("allowed_only_if_same_canonical_source_sha_proven") is not True or derivative.get("accounting_classification_required") is not True:
        raise ContinuationMapError("preserved derivative provenance/accounting gate missing")
    history = doc.get("historical_continuation", {})
    if history.get("schema") != CONTINUATION_MAP_SCHEMA or history.get("sha256") != HISTORICAL_CONTINUATION_MAP_SHA256 or history.get("git_blob_sha1") != HISTORICAL_CONTINUATION_MAP_GIT_BLOB_SHA1:
        raise ContinuationMapError("historical continuation identity drift")
    if history.get("role") != "IMMUTABLE_HISTORY_ONLY__NOT_CURRENT_CAPABILITY_LAW" or history.get("mutate_in_place") is not False:
        raise ContinuationMapError("historical continuation map promoted into current law")
    cbind = doc.get("candidate_c_binding", {})
    if cbind.get("candidate") != "C" or cbind.get("policy") != CANDIDATE_C_POLICY:
        raise ContinuationMapError("Candidate-C current policy identity drift")
    if cbind.get("candidate_b_identity_substitution_allowed") is not False or cbind.get("historical_failure_receipts_are_current_capability_law") is not False:
        raise ContinuationMapError("Candidate-C identity/history boundary drift")
    lits_c = cbind.get("LITS_I", {})
    if lits_c.get("source_sha256") != LITS_I_CANONICAL_SOURCE_SHA256 or tuple(lits_c.get("permitted_accelerators", ())) != ("CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE", "CACC2_FRONTIER_ATOMIC_PREDICATE_RISK_MASK_BANK") or tuple(lits_c.get("applicable_accelerators_current_f02", ())) != () or lits_c.get("q310_q311_required") is not True or lits_c.get("cacc3_allowed") is not False:
        raise ContinuationMapError("LiTS-I Candidate-C exact current scope drift")
    wvs_c = cbind.get("WVS7", {})
    if wvs_c.get("source_sha256") != WVS7_CANONICAL_SOURCE_SHA256 or tuple(wvs_c.get("permitted_accelerators", ())) != () or wvs_c.get("wvs_specific_cacc_allowed") is not False:
        raise ContinuationMapError("WVS7 Candidate-C zero-accelerator law drift")
    auth = doc.get("authority", {})
    for k, v in {"p2x_branch": P2X_BRANCH, "p2x_resume_head": P2X_RESUME_HEAD, "p2r1_pass": P2R1_PASS, "p2r1_seam_path": P2R1_SEAM_PATH, "p2r1_seam_blob": P2R1_SEAM_BLOB}.items():
        if auth.get(k) != v: raise ContinuationMapError(f"authority drift for {k}")
    if tuple(doc.get("stage_tuple_schema", ())) != ("disposition", "evidence_or_stop_law_ref", "empirical_source_access_required", "physical_host_measurement_required", "next_stage_on_pass"):
        raise ContinuationMapError("stage tuple schema drift")
    cells = doc.get("cells")
    if not isinstance(cells, list) or tuple((c.get("source"), c.get("candidate")) for c in cells) != expected_pairs:
        raise ContinuationMapError("current cell order drift")
    evidence, laws = doc.get("evidence", {}), doc.get("stop_laws", {})
    stages: dict[str, StageSpec] = {}
    for cell in cells:
        source, candidate, sm = cell["source"], cell["candidate"], cell.get("stages")
        prereq, receipt, fail = cell.get("prerequisite_ref"), cell.get("expected_receipt"), cell.get("candidate_local_failure_next")
        if not isinstance(sm, Mapping) or not all(isinstance(x, str) and x for x in (prereq, receipt, fail)):
            raise ContinuationMapError(f"{source}/{candidate}: current inherited fields incomplete")
        for sid, raw in sm.items():
            address = f"{source}/{candidate}/{sid}"; d, e, sa, m, n = _stage_tuple(raw, address)
            if d == "TERMINAL_CANDIDATE_LOCAL_FAILURE__PRESERVE":
                raise ContinuationMapError(f"{address}: historical Candidate-C failure may not be current capability law")
            if e is not None and e not in evidence and e not in laws:
                raise ContinuationMapError(f"{address}: unknown evidence/stop-law")
            n = f"{source}/{candidate}/{n}" if n in sm else n
            stages[address] = StageSpec(source, candidate, sid, d, e, sa, m, n, prereq, f"{receipt}#{sid}", fail)
    if doc.get("lits_a_absent_root_current_law") != LITS_A_ABSENT_ROOT_CURRENT_LAW:
        raise ContinuationMapError("LiTS-A absent-root current-law succession missing or drifted")
    first = doc.get("entry_guard", {}).get("first_unfinished_court_stage")
    if first != "LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD" or first not in stages:
        raise ContinuationMapError("first unfinished stage drift")
    lits_a_s01 = stages["LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD"]
    if (
        lits_a_s01.disposition != "READY__RUN_LOCALLY"
        or lits_a_s01.evidence_or_stop_law_ref is not None
        or lits_a_s01.empirical_source_access_required is not True
        or lits_a_s01.physical_host_measurement_required is not True
    ):
        raise ContinuationMapError("LiTS-A absent-root S01 must be current measured candidate work")
    prohibitions = set(doc.get("hard_prohibitions", ()))
    if "NO_REPEAT_COMPLETED_LITS_A_FIRST_BUILD" in prohibitions:
        raise ContinuationMapError("obsolete preserved-root no-repeat law suppresses required current LiTS-A S01")
    for required in (
        "NO_DUPLICATE_LITS_A_S01_PREBUILD_OR_R35_REBUILD",
        "NO_HISTORICAL_LITS_A_S01_NUMERIC_CREDIT_WHEN_ROOT_ABSENT",
    ):
        if required not in prohibitions:
            raise ContinuationMapError("LiTS-A absent-root nonduplication/accounting law missing")
    for source in EXPECTED_SOURCE_ORDER:
        for sid in ("S01_CANDIDATE_PREPARATION_BUILD", "S02_C11_REACHABILITY"):
            if stages[f"{source}/C/{sid}"].disposition != "READY__RUN_LOCALLY":
                raise ContinuationMapError(f"{source}/C current execution is not admitted at {sid}")
    for sid in ("S12_STALE_CACHE_OR_PERSISTENT_STATE", "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE"):
        sp = stages[f"WVS7/C/{sid}"]
        if sp.disposition != "SKIP__NOT_APPLICABLE_BY_FROZEN_LAW" or sp.evidence_or_stop_law_ref != "C_ZERO_ACCELERATOR_NO_CACHE":
            raise ContinuationMapError("WVS7/C zero-accelerator cache law drift")
    final = doc.get("final_stage", {})
    if final.get("stage_id") != "S17_FINAL_COMPLETENESS_AND_VERIFICATION" or final.get("wake_on_pass") != "HQ_MEASURED_SYNTHESIS" or not isinstance(final.get("expected_outputs"), list):
        raise ContinuationMapError("final court stage drift")
    fa = "COURT/S17_FINAL_COMPLETENESS_AND_VERIFICATION"
    stages[fa] = StageSpec("COURT", "ALL", "S17_FINAL_COMPLETENESS_AND_VERIFICATION", "READY__RUN_LOCALLY", None, False, False, "__COURT_COMPLETE__", "ALL_SIX_CELLS_LAWFULLY_TERMINAL__NO_UNRESOLVED_COMMON_BLOCKER", "|".join(final["expected_outputs"]), "__FORBIDDEN_FINAL_STAGE_CANDIDATE_LOCAL_FAILURE__")
    return StateMachine(doc, ident, stages, first, fa)

def load_current_execution_manifest(path: Path) -> StateMachine:
    data = path.read_bytes()
    try:
        doc = json.loads(data.decode())
    except Exception as exc:
        raise ContinuationMapError("current execution manifest is not valid JSON") from exc
    if not isinstance(doc, Mapping):
        raise ContinuationMapError("current execution manifest top level must be mapping")
    ident = MapIdentity(CURRENT_EXECUTION_MANIFEST_SCHEMA, _sha256_bytes(data), _git_blob_sha1(data))
    return validate_current_execution_manifest(doc, ident)


def validate_frozen_upstream_for_machine(machine: StateMachine, receipt_path: Path) -> Mapping[str, Any]:
    """Bind the pre-candidate freeze receipt to the current execution manifest.

    This deliberately reasons over the manifest's source set rather than a
    LiTS/WVS-specific switch, so the same contract can bind any admitted
    CLOSED_35 source when a later execution manifest exposes it.
    """
    from rawlsing_next.ee_p2x_candidate_process_envelope import load_frozen_upstream_receipt

    doc, receipt_sha256 = load_frozen_upstream_receipt(receipt_path)
    source_freezes = doc.get("source_freezes", {})
    oracle_identities = doc.get("oracle_identities", {})
    manifest_sources = machine.document.get("sources", {})
    if not isinstance(manifest_sources, Mapping) or not manifest_sources:
        raise RuntimeGateError("current execution manifest has no source registry")

    for source_id, source_doc in manifest_sources.items():
        if source_id not in source_freezes:
            raise RuntimeGateError(f"frozen upstream receipt lacks manifest source {source_id}")
        entry = source_freezes[source_id]
        if entry.get("source_id") != source_id:
            raise RuntimeGateError(f"frozen upstream source_id drift for {source_id}")
        canonical = source_doc.get("sha256")
        if entry.get("canonical_source_sha256") != canonical:
            raise RuntimeGateError(f"frozen upstream canonical source root drift for {source_id}")
        if entry.get("source_identity_authority_ref") in (None, "", {}, []):
            raise RuntimeGateError(f"frozen upstream source identity authority missing for {source_id}")
        if source_id not in oracle_identities:
            raise RuntimeGateError(f"frozen upstream independent oracle missing for {source_id}")

    return {
        "schema": doc.get("schema"),
        "receipt_sha256": receipt_sha256,
        "source_ids": tuple(manifest_sources),
        "freeze_order": dict(doc.get("freeze_order", {})),
    }

# ---- durable ledger --------------------------------------------------------------------
def _candidate_roots(root: Path, source: str, candidate: str) -> CandidateRoots:
    r = root / "cells" / source / candidate; obj = CandidateRoots(r, r/"scratch", r/"durable", r/"logs", r/"receipts")
    resolved = []
    for p in dataclasses.astuple(obj):
        if p.exists() and p.is_symlink(): raise StageStateError(f"candidate root may not be symlink: {p}")
        p.mkdir(parents=True, exist_ok=True); resolved.append(p.resolve())
    if len(set(resolved[1:])) != 4: raise StageStateError("candidate roots are not isolated")
    return obj

class StageLedger:
    def __init__(self, work_root: Path, machine: StateMachine, repo_root: Path | None = None):
        self.work_root, self.repo_root, self.machine = work_root, (repo_root or work_root).resolve(), machine
        self.path = work_root / "ee_p2x_stage_ledger.json"; work_root.mkdir(parents=True, exist_ok=True)
        source_order = list(machine.document.get("source_order", ()))
        candidate_order = list(machine.document.get("candidate_order", ()))
        if self.path.exists(): self.data = json.loads(self.path.read_text())
        else:
            self.data = {"schema": LEDGER_SCHEMA, "continuation_map": dataclasses.asdict(machine.identity), "p2x_branch": P2X_BRANCH, "p2x_resume_head": P2X_RESUME_HEAD, "source_order": source_order, "candidate_order": candidate_order, "source_identities": {}, "stages": {}}; self.flush()
        if self.data.get("schema") != LEDGER_SCHEMA or self.data.get("continuation_map") != dataclasses.asdict(machine.identity) or self.data.get("source_order") != source_order or self.data.get("candidate_order") != candidate_order: raise StageStateError("ledger authority drift")
    def flush(self): return _atomic_write_json(self.path, self.data)
    def hash(self): return _sha256_file(self.path)
    def source_identity(self, source): return self.data["source_identities"].get(source)
    def record_source_identity(self, source: str, *, sha256: str, size: int):
        if sha256 != self.machine.document["sources"][source]["sha256"]: raise RuntimeGateError(f"{source} source SHA-256 drift")
        v = {"sha256": sha256, "size": size}; old = self.source_identity(source)
        if old is not None and old != v: raise StageStateError(f"{source} source identity changed")
        self.data["source_identities"][source] = v; self.flush()
    def stage_entry(self, address): return self.data["stages"].get(address)
    def begin(self, stage: StageSpec, ih: str):
        old = self.stage_entry(stage.address)
        if old and old.get("terminal_disposition") in COMPLETE_LEDGER_DISPOSITIONS: raise StageStateError(f"cannot restart terminal stage {stage.address}")
        self.data["stages"][stage.address] = {"stage_id": stage.stage_id, "source": stage.source, "candidate": stage.candidate, "input_identity_hash": ih, "state": "RUNNING", "output_artifact_hashes": {}, "receipt_path": None, "receipt_hash": None, "verifier_completion": False, "terminal_disposition": None, "next_stage": None}; self.flush()
    def discard_empty_running_preterminal(self, stage: StageSpec):
        old = self.stage_entry(stage.address)
        if old is None: return
        if old.get("state") != "RUNNING" or old.get("terminal_disposition") is not None:
            raise StageStateError(f"cannot discard non-running preterminal stage {stage.address}")
        if old.get("receipt_path") is not None or old.get("receipt_hash") is not None or old.get("output_artifact_hashes"):
            raise StageStateError(f"cannot discard evidenced running stage {stage.address}")
        del self.data["stages"][stage.address]; self.flush()
    def complete(self, stage: StageSpec, *, input_identity_hash: str, terminal_disposition: str, receipt_path: Path, output_artifact_hashes: Mapping[str,str], verifier_complete: bool, next_stage: str):
        if terminal_disposition not in COMPLETE_LEDGER_DISPOSITIONS or not verifier_complete or not receipt_path.is_file(): raise StageStateError("stage cannot become terminal")
        self.data["stages"][stage.address] = {"stage_id": stage.stage_id, "source": stage.source, "candidate": stage.candidate, "input_identity_hash": input_identity_hash, "state": "TERMINAL", "output_artifact_hashes": dict(sorted(output_artifact_hashes.items())), "receipt_path": str(receipt_path.relative_to(self.work_root)), "receipt_hash": _sha256_file(receipt_path), "verifier_completion": True, "terminal_disposition": terminal_disposition, "next_stage": next_stage}; return self.flush()
    def revalidate_terminal(self, address: str):
        e = self.stage_entry(address)
        if not e or e.get("terminal_disposition") not in COMPLETE_LEDGER_DISPOSITIONS or e.get("state") != "TERMINAL" or e.get("verifier_completion") is not True: raise StageStateError(f"stage {address} is incomplete")
        rp = (self.work_root / e["receipt_path"]).resolve(); wr = self.work_root.resolve()
        if wr not in rp.parents or not rp.is_file() or _sha256_file(rp) != e.get("receipt_hash"): raise StageStateError(f"stage {address} terminal receipt hash drift")
        for loc, expected in e.get("output_artifact_hashes", {}).items():
            root, rel = (wr, loc[5:]) if loc.startswith("work:") else (self.repo_root, loc[5:]) if loc.startswith("repo:") else (None, None)
            if root is None: raise StageStateError(f"stage {address} artifact locator unbound")
            p = (root / rel).resolve()
            if (p != root and root not in p.parents) or not p.is_file() or _sha256_file(p) != expected: raise StageStateError(f"stage {address} output artifact hash drift: {loc}")
        return e

class DriverInstanceLock:
    def __init__(self, root: Path): self.path = root / ".ee_p2x_darwin_driver.lock"; self.fh = None
    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True); self.fh = self.path.open("a+")
        try: fcntl.flock(self.fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc: self.fh.close(); self.fh=None; raise RuntimeGateError("a second EE-P2X court-driver instance already owns this root") from exc
        return self
    def __exit__(self, *args):
        if self.fh: fcntl.flock(self.fh.fileno(), fcntl.LOCK_UN); self.fh.close()

# ---- accepted owner / P2R1 / backend services -----------------------------------------
class DriverServices:
    def __init__(self, *, repo_root: Path, work_root: Path): self.repo_root, self.work_root = repo_root, work_root
    def load_exact_owner_module(self, candidate: str): return load_exact_owner_module(candidate, repo_root=self.repo_root, work_root=self.work_root)
    def accepted_repository_builder(self, candidate: str) -> Callable[..., Any]:
        m = self.load_exact_owner_module(candidate); b = getattr(m, OWNER_SPECS[candidate]["builder"], None)
        if not callable(b): raise OwnerDeploymentError(f"accepted Candidate-{candidate} builder absent")
        return b
    def compose_p2r1_binding(self, *, authority_documents: Iterable[Mapping[str,Any]], predicate_documents: Iterable[Mapping[str,Any]], query_documents: Iterable[Mapping[str,Any]], discovery_authority_documents: Iterable[Mapping[str,Any]], projection_fields: Mapping[str,Any], candidate: str, builder_kwargs: Mapping[str,Any], builder_identity: Mapping[str,Any], semantic_owner_candidate: str | None = None, projection_override: Any | None = None, repository_builder_override: Callable[..., Any] | None = None):
        from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, bind_governed_c11_projection, bind_repository_builder
        catalog = RuntimeObjectCatalog.from_documents(authority_documents=authority_documents, predicate_documents=predicate_documents, query_documents=query_documents, discovery_authority_documents=discovery_authority_documents)
        owner_candidate = semantic_owner_candidate or candidate
        if owner_candidate not in OWNER_SPECS:
            raise StageExecutionError("semantic owner candidate is not admitted")
        owner_module = self.load_exact_owner_module(owner_candidate)
        if projection_override is None:
            projection = bind_governed_c11_projection(projection_fields)
        else:
            expected_projection_type = getattr(owner_module, "GovernedC11Projection", None)
            if expected_projection_type is None or not isinstance(projection_override, expected_projection_type):
                raise StageExecutionError("projection is outside the exact semantic-owner type universe")
            projection = projection_override
        kw = dict(builder_kwargs)
        if "projection" in kw and kw["projection"] is not projection: raise StageExecutionError("projection substitution forbidden")
        kw["projection"] = projection
        repository_builder = repository_builder_override or getattr(owner_module, OWNER_SPECS[owner_candidate]["builder"], None)
        if not callable(repository_builder):
            raise OwnerDeploymentError(f"exact Candidate-{owner_candidate} repository builder absent")
        return bind_repository_builder(repository_builder=repository_builder, builder_kwargs=kw, builder_identity=builder_identity, runtime_catalog=catalog)

def load_exact_owner_module(candidate: str, *, repo_root: Path, work_root: Path):
    if candidate not in OWNER_SPECS: raise OwnerDeploymentError(f"unknown candidate {candidate}")
    sp = OWNER_SPECS[candidate]; data = _git_show_bytes(repo_root, OWNER_COMMIT, sp["path"])
    if _git_blob_sha1(data) != sp["blob"]: raise OwnerDeploymentError(f"Candidate-{candidate} owner blob drift")
    dest = work_root / "_exact_owner_modules" / OWNER_COMMIT / candidate / Path(sp["path"]).name
    if dest.exists() and dest.read_bytes() != data: raise OwnerDeploymentError("deployed owner bytes drifted")
    if not dest.exists(): _atomic_write_bytes(dest, data)
    name = f"_rawlsing_ee_p2x_owner_{candidate.lower()}_{sp['blob'][:12]}"; old = sys.modules.get(name)
    if old is not None: return old
    spec = importlib.util.spec_from_file_location(name, dest)
    if not spec or not spec.loader: raise OwnerDeploymentError("exact owner import spec failed")
    mod = importlib.util.module_from_spec(spec); sys.modules[name] = mod
    try: spec.loader.exec_module(mod)
    except Exception: sys.modules.pop(name, None); raise
    return mod

def _load_backend(module_or_path: str) -> StageBackend:
    if module_or_path.endswith(".py") or os.path.sep in module_or_path:
        spec = importlib.util.spec_from_file_location("_rawlsing_ee_p2x_runtime_backend", Path(module_or_path).resolve())
        if not spec or not spec.loader: raise StageExecutionError("unable to load backend")
        mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    else: mod = importlib.import_module(module_or_path)
    if getattr(mod, "BACKEND_CONTRACT", None) != BACKEND_CONTRACT or not callable(getattr(mod, "run_stage", None)): raise StageExecutionError("backend contract mismatch")
    class B:
        def run_stage(self, context, services):
            r = mod.run_stage(context, services)
            if isinstance(r, BackendResult): return r
            if not isinstance(r, Mapping): raise StageExecutionError("backend result must be mapping")
            return BackendResult(r.get("terminal_disposition", "PASS"), r.get("receipt", {}), {str(k): Path(v) for k,v in r.get("output_artifacts", {}).items()}, bool(r.get("verifier_complete", False)))
    return B()

# ---- stage mechanics -------------------------------------------------------------------
def _evidence_bytes(machine: StateMachine, ref: str, repo_root: Path):
    d = machine.document.get("evidence", {}).get(ref)
    if not isinstance(d, Mapping) or not isinstance(d.get("commit"), str) or not isinstance(d.get("path"), str): raise StageStateError(f"banked evidence {ref} unavailable")
    return _git_show_bytes(repo_root, d["commit"], d["path"]), d
def _write_receipt(roots: CandidateRoots, stage: StageSpec, payload: Mapping[str,Any]):
    p = roots.receipts / f"{stage.stage_id.lower()}.json"; _atomic_write_json(p, payload); return p
def _artifact_hashes(work: Path, repo: Path, artifacts: Mapping[str,Path]):
    out={}; wr, rr = work.resolve(), repo.resolve()
    for label, raw in artifacts.items():
        p=raw.resolve()
        if not p.is_file(): raise StageStateError(f"backend artifact missing: {label}")
        loc = "work:"+str(p.relative_to(wr)) if p==wr or wr in p.parents else "repo:"+str(p.relative_to(rr)) if p==rr or rr in p.parents else None
        if loc is None: raise StageStateError(f"backend artifact {label} escapes bound roots")
        out[loc]=_sha256_file(p)
    return out
def _source_hash_and_size(path: Path):
    if not path.is_file(): raise RuntimeGateError(f"source path is not a file: {path}")
    return _sha256_file(path), path.stat().st_size
def _input_identity(machine: StateMachine, stage: StageSpec, source_sha: str, head: str):
    return _semantic_hash({"continuation_map":dataclasses.asdict(machine.identity),"stage":stage.address,"disposition":stage.disposition,"evidence_or_stop_law_ref":stage.evidence_or_stop_law_ref,"executable_prerequisite":stage.executable_prerequisite,"expected_output_receipt":stage.expected_output_receipt,"source_sha256":source_sha,"p2x_branch":P2X_BRANCH,"p2x_resume_head":P2X_RESUME_HEAD,"observed_p2x_head":head,"p2r1_pass":P2R1_PASS,"p2r1_seam_blob":P2R1_SEAM_BLOB})
def _mechanical_terminal(machine, ledger, stage, head, source_sha, kind, body, next_stage):
    roots=_candidate_roots(ledger.work_root,stage.source,stage.candidate); ih=_input_identity(machine,stage,source_sha,head); receipt=_write_receipt(roots,stage,{**body,"stage":stage.address,"input_identity_hash":ih,"execution_performed":False,"measurement_performed":False})
    ledger.complete(stage,input_identity_hash=ih,terminal_disposition=kind,receipt_path=receipt,output_artifact_hashes={},verifier_complete=True,next_stage=next_stage); return next_stage,_sha256_file(receipt)
def _preserve(machine, ledger, stage, repo, head, source_sha):
    data,d=_evidence_bytes(machine,stage.evidence_or_stop_law_ref,repo)
    from rawlsing_next.fiabc_live_accounting_binding import preserved_stage_adjudication
    accounting=preserved_stage_adjudication(
        stage=stage,source_sha256=source_sha,evidence_ref=stage.evidence_or_stop_law_ref
    )
    return _mechanical_terminal(machine,ledger,stage,head,source_sha,"PRESERVED",{
        "schema":"RAWLSING_EE_P2X_PRESERVED_STAGE_BINDING@1.0.0",
        "evidence_ref":stage.evidence_or_stop_law_ref,"evidence":dict(d),
        "evidence_sha256":_sha256_bytes(data),"evidence_git_blob_sha1":_git_blob_sha1(data),
        "source_access_performed":False,"t4_preserved_work_adjudication":accounting,
    },stage.next_stage_on_pass)
def _skip(machine, ledger, stage, head, source_sha):
    ref=stage.evidence_or_stop_law_ref; law=machine.document.get("stop_laws",{}).get(ref)
    if not isinstance(law,str): raise StageStateError(f"stop law unavailable: {ref}")
    return _mechanical_terminal(machine,ledger,stage,head,source_sha,"SKIPPED_BY_FROZEN_LAW",{"schema":"RAWLSING_EE_P2X_FROZEN_LAW_SKIP@1.0.0","stop_law_ref":ref,"stop_law":law},stage.next_stage_on_pass)
def _candidate_stop(machine, ledger, *, source, candidate, head, source_sha, blocker):
    cat=list(machine.document.get("stage_catalog",())); sid=blocker.rsplit("/",1)[-1]; start=cat.index(sid)+1
    for later in cat[start:]:
        sp=machine.stages[f"{source}/{candidate}/{later}"]
        if ledger.stage_entry(sp.address) is None: _mechanical_terminal(machine,ledger,sp,head,source_sha,"CANDIDATE_LOCAL_FAILURE",{"schema":"RAWLSING_EE_P2X_CANDIDATE_LOCAL_STOP_PROPAGATION@1.0.0","blocker_stage":blocker},sp.next_stage_on_candidate_local_failure)
def _source_stop(machine,ledger,*,source,head,source_sha,blocker):
    cells = list(machine.document.get("cells", ()))
    source_cells = [cell for cell in cells if cell.get("source") == source]
    if not source_cells:
        raise StageStateError(f"source blocker references manifest-absent source {source}")
    for cell in source_cells:
        for sid in _manifest_ordered_stage_ids(machine.document, cell):
            sp=machine.stages[f"{source}/{cell['candidate']}/{sid}"]
            if ledger.stage_entry(sp.address) is None:
                _mechanical_terminal(
                    machine,ledger,sp,head,source_sha,"BLOCKED_BY_COMMON_SOURCE_AUTHORITY",
                    {"schema":"RAWLSING_EE_P2X_COMMON_SOURCE_BLOCK_PROPAGATION@1.0.0","blocker_stage":blocker},
                    "__SOURCE_BLOCKED__",
                )
    source_order = list(dict.fromkeys(cell.get("source") for cell in cells))
    i = source_order.index(source)
    if i + 1 == len(source_order):
        return machine.final_stage_id
    next_source = source_order[i + 1]
    next_cell = next(cell for cell in cells if cell.get("source") == next_source)
    next_stage_ids = _manifest_ordered_stage_ids(machine.document, next_cell)
    if not next_stage_ids:
        raise StageStateError(f"next source {next_source} has no governed stages")
    return f"{next_source}/{next_cell['candidate']}/{next_stage_ids[0]}"
def _mark_source_blocked(machine, ledger, *, source: str, observed_head: str, source_sha256: str, blocker_stage: str):
    return _source_stop(machine, ledger, source=source, head=observed_head, source_sha=source_sha256, blocker=blocker_stage)
def _backend_terminal(machine,ledger,stage,head,source_sha,result):
    if result.terminal_disposition not in {"PASS","CANDIDATE_LOCAL_FAILURE","COMMON_SOURCE_BLOCKER","COMMON_COURT_BLOCKER"}: raise StageStateError("backend terminal disposition invalid")
    if not result.verifier_complete: raise StageStateError("backend result incomplete: verifier did not complete")
    ih=_input_identity(machine,stage,source_sha,head); roots=_candidate_roots(ledger.work_root,stage.source,stage.candidate)
    measured_payload=dict(result.receipt)
    from rawlsing_next.fiabc_live_accounting_binding import admit_live_stage_accounting
    owner_identity=OWNER_SPECS.get(stage.candidate,{}).get("blob","COURT_ADMINISTRATION")
    measured_payload["t4_accounting"]=admit_live_stage_accounting(
        stage=stage,roots=roots,source_sha256=source_sha,
        candidate_owner_identity=owner_identity,repo_head=head,
        backend_receipt=measured_payload,terminal_disposition=result.terminal_disposition,
    )
    if result.terminal_disposition=="PASS" and stage.stage_id=="S05_I05_LEARNED_PRODUCTION":
        from rawlsing_next.fiabc_live_terminal_control import admit_post_i05_oracle_match
        freeze=os.environ.get(FROZEN_UPSTREAM_ENV)
        if not freeze:
            raise StageStateError("T5 post-I05 oracle match lacks T3 freeze receipt")
        measured_payload["t5_oracle_match"]=admit_post_i05_oracle_match(
            stage=stage,roots=roots,work_root=ledger.work_root,
            freeze_path=Path(freeze),backend_receipt=measured_payload,
        )
    if result.terminal_disposition=="PASS" and stage.stage_id=="S16_TERMINAL_METRIC_VECTOR_COMPLETENESS":
        from rawlsing_next.fiabc_live_terminal_control import seal_live_cell_terminal
        freeze=os.environ.get(FROZEN_UPSTREAM_ENV)
        if not freeze:
            raise StageStateError("T5 cell terminal lacks T3 freeze receipt")
        measured_payload["t5_cell_terminal"]=seal_live_cell_terminal(
            stage=stage,roots=roots,work_root=ledger.work_root,freeze_path=Path(freeze),
            backend_receipt=measured_payload,
        )
    receipt=_write_receipt(roots,stage,{"schema":"RAWLSING_EE_P2X_DARWIN_STAGE_RECEIPT_ENVELOPE@1.0.0","stage":stage.address,"backend_contract":BACKEND_CONTRACT,"terminal_disposition":result.terminal_disposition,"input_identity_hash":ih,"measured_payload":measured_payload})
    arts=_artifact_hashes(ledger.work_root,ledger.repo_root,result.output_artifacts)
    disp,nxt={"PASS":("PASS",stage.next_stage_on_pass),"CANDIDATE_LOCAL_FAILURE":("CANDIDATE_LOCAL_FAILURE",stage.next_stage_on_candidate_local_failure),"COMMON_SOURCE_BLOCKER":("BLOCKED_BY_COMMON_SOURCE_AUTHORITY","__COMMON_SOURCE_BLOCKER__"),"COMMON_COURT_BLOCKER":("BLOCKED_BY_COMMON_COURT_AUTHORITY","__COMMON_COURT_BLOCKER__")}[result.terminal_disposition]
    ledger.complete(stage,input_identity_hash=ih,terminal_disposition=disp,receipt_path=receipt,output_artifact_hashes=arts,verifier_complete=True,next_stage=nxt); return nxt,_sha256_file(receipt),disp
def _final_ready(machine,ledger):
    common=[]
    for cell in machine.document["cells"]:
        for sid in machine.document["stage_catalog"]:
            a=f"{cell['source']}/{cell['candidate']}/{sid}"; e=ledger.stage_entry(a)
            if not e or e.get("terminal_disposition") not in COMPLETE_LEDGER_DISPOSITIONS: raise StageStateError(f"final S17 gate: nonterminal reducer stage {a}")
            e=ledger.revalidate_terminal(a)
            if e["terminal_disposition"] in {"BLOCKED_BY_COMMON_SOURCE_AUTHORITY","BLOCKED_BY_COMMON_COURT_AUTHORITY"}: common.append(a)
    if common: raise CommonAuthorityBlocker("unresolved common blockers at S17",scope="COURT",receipt={"blockers":common})
    if machine.identity.schema == CURRENT_EXECUTION_MANIFEST_SCHEMA:
        candidate_failures=[]
        for cell in machine.document.get("cells", ()):
            stage_ids = _manifest_ordered_stage_ids(machine.document, cell)
            if not stage_ids:
                raise StageStateError(f"current cell has no governed stages: {cell}")
            terminal_address = f"{cell['source']}/{cell['candidate']}/{stage_ids[-1]}"
            terminal = ledger.stage_entry(terminal_address)
            disposition = None if not terminal else terminal.get("terminal_disposition")
            if disposition == "CANDIDATE_LOCAL_FAILURE":
                candidate_failures.append(f"{cell['source']}/{cell['candidate']}")
            elif disposition != "PASS":
                raise StageStateError(f"current cell terminal PASS/failure absent for {cell['source']}/{cell['candidate']}")
        if candidate_failures:
            raise CandidateLocalFailure(
                "current six-cell court contains lawful candidate-local failures; success-only S17 is not applicable",
                receipt={"candidate_failure_cells":candidate_failures},
            )
    elif ledger.stage_entry("WVS7/C/S01_CANDIDATE_PREPARATION_BUILD").get("terminal_disposition") != "CANDIDATE_LOCAL_FAILURE":
        raise StageStateError("historical WVS-C portability failure not bound")
def _token(stage,receipt_hash,ledger_hash,head): return {"schema":SUPERVISOR_TOKEN_SCHEMA,"action":"COMMIT_AND_PUSH_EXISTING_P2X_BRANCH_BOUNDED_STAGE_EVIDENCE","stage_id":stage.address,"terminal_receipt_sha256":receipt_hash,"ledger_sha256":ledger_hash,"p2x_branch":P2X_BRANCH,"observed_branch_head":head}

# ---- driver ---------------------------------------------------------------------------
class DarwinCourtDriver:
    def __init__(self, *, machine, work_root, repo_root, source_paths, host, repo, backend):
        self.machine,self.work_root,self.repo_root,self.source_paths,self.host,self.repo,self.backend=machine,work_root,repo_root,dict(source_paths),host,repo,backend
        self._verified_sources_this_process={}; self.ledger=StageLedger(work_root,machine,repo_root); self.services=DriverServices(repo_root=repo_root,work_root=work_root)
        self.progress=ProgressReporter(machine,self.ledger)
    def verify_static_gates(self): verify_runtime_gate(self.host); verify_repo_gate(self.repo)
    def frozen_source_sha(self,source):
        expected=self.machine.document["sources"][source]["sha256"]; old=self.ledger.source_identity(source)
        if old and old.get("sha256") != expected: raise StageStateError(f"{source} ledger source hash drift")
        return expected
    def ensure_source_verified(self,source):
        if source in self._verified_sources_this_process: return self._verified_sources_this_process[source]
        expected=self.frozen_source_sha(source); path=self.source_paths.get(source)
        if path is None or not path.is_file(): raise RuntimeGateError(f"explicit runtime path required for {source}")
        got,size=_source_hash_and_size(path)
        if got != expected: raise RuntimeGateError(f"{source} source SHA drift before source use")
        self.ledger.record_source_identity(source,sha256=got,size=size); self._verified_sources_this_process[source]=got; return got
    def source_sha_for_stage(self,stage):
        if stage.source == "COURT": return _semantic_hash(self.machine.document.get("sources",{}))
        return self.ensure_source_verified(stage.source) if stage.empirical_source_access_required else self.frozen_source_sha(stage.source)
    def bind_initial_manifest_prefix(self):
        plan=ManifestProgressPlan(self.machine)
        first=plan.governed_addresses[0]
        cells=list(self.machine.document.get("cells",()))
        ordered=[]
        for cell in cells:
            ordered.extend(
                f"{cell['source']}/{cell['candidate']}/{sid}"
                for sid in _manifest_ordered_stage_ids(self.machine.document,cell)
            )
        if self.machine.final_stage_id not in ordered:
            ordered.append(self.machine.final_stage_id)
        prefix=ordered[:ordered.index(first)]
        for address in prefix:
            stage=self.machine.get(address)
            if self.ledger.stage_entry(address) is not None:
                self.ledger.revalidate_terminal(address)
                continue
            sha=self.frozen_source_sha(stage.source) if stage.source!="COURT" else _semantic_hash(self.machine.document.get("sources",{}))
            if stage.disposition=="DONE__PRESERVE":
                _preserve(self.machine,self.ledger,stage,self.repo_root,self.repo.head,sha)
            elif stage.disposition=="SKIP__NOT_APPLICABLE_BY_FROZEN_LAW":
                _skip(self.machine,self.ledger,stage,self.repo.head,sha)
            elif stage.disposition=="TERMINAL_CANDIDATE_LOCAL_FAILURE__PRESERVE":
                if stage.source=="WVS7" and stage.candidate=="C":
                    self._preserved_wvs_c(stage,sha)
                else:
                    raise StageStateError(f"unsupported pre-entry preserved candidate failure: {address}")
            else:
                raise StageStateError(f"pre-entry executable stage cannot be synthesized: {address}")
    def preflight(self):
        source_order=tuple(self.machine.document.get("source_order",()))
        self.verify_static_gates(); verified={s:self.ensure_source_verified(s) for s in source_order}; owners={}
        for c,sp in OWNER_SPECS.items():
            data=_git_show_bytes(self.repo_root,OWNER_COMMIT,sp["path"]); blob=_git_blob_sha1(data)
            if blob != sp["blob"]: raise OwnerDeploymentError(f"Candidate-{c} owner blob drift")
            owners[c]=blob
        self.bind_initial_manifest_prefix()
        return {"schema":"RAWLSING_EE_P2X_DARWIN_PREFLIGHT@1.0.0","status":"PASS","host":dataclasses.asdict(self.host),"repo":dataclasses.asdict(self.repo),"source_sha256":verified,"owner_blobs":owners,"continuation_map":dataclasses.asdict(self.machine.identity),"host_contention_claim":"SINGLE_DRIVER_LOCK_ONLY__NO_PROCESS_NAME_IDLE_HEURISTIC","next_stage":self.next_stage()}
    def next_stage(self):
        a=self.machine.first_unfinished; seen=set()
        while a != "__COURT_COMPLETE__":
            if a in seen: raise StageStateError("next-stage cycle")
            seen.add(a); e=self.ledger.stage_entry(a)
            if not e or e.get("terminal_disposition") not in COMPLETE_LEDGER_DISPOSITIONS: return a
            e=self.ledger.revalidate_terminal(a); n=e.get("next_stage")
            if n in {"__COMMON_COURT_BLOCKER__","__COMMON_SOURCE_BLOCKER__","__SOURCE_BLOCKED__"}: return a
            a=n
        return a
    def verify_only(self):
        count=0
        for a,e in self.ledger.data["stages"].items():
            if e.get("terminal_disposition") in COMPLETE_LEDGER_DISPOSITIONS: self.ledger.revalidate_terminal(a); count+=1
            elif e.get("state")=="RUNNING": raise StageStateError(f"partial RUNNING stage remains incomplete: {a}")
        return {"schema":"RAWLSING_EE_P2X_DARWIN_LEDGER_VERIFICATION@1.0.0","status":"PASS","terminal_stages_reverified":count,"ledger_sha256":self.ledger.hash(),"next_stage":self.next_stage()}
    def _preserved_wvs_c(self,stage,source_sha):
        prior=self.machine.get("WVS7/C/S00_SOURCE_PREFLIGHT_IDENTITY")
        if self.ledger.stage_entry(prior.address) is None: _preserve(self.machine,self.ledger,prior,self.repo_root,self.repo.head,source_sha)
        data,d=_evidence_bytes(self.machine,stage.evidence_or_stop_law_ref,self.repo_root)
        nxt,rh=_mechanical_terminal(self.machine,self.ledger,stage,self.repo.head,source_sha,"CANDIDATE_LOCAL_FAILURE",{"schema":"RAWLSING_EE_P2X_PRESERVED_CANDIDATE_LOCAL_FAILURE@1.0.0","preserved_failure":"WVS7_C__CURRENT_PORTABILITY_FAILURE","evidence":dict(d),"evidence_sha256":_sha256_bytes(data)},stage.next_stage_on_pass)
        for sid in self.machine.document["stage_catalog"]:
            if sid not in {"S00_SOURCE_PREFLIGHT_IDENTITY","S01_CANDIDATE_PREPARATION_BUILD"}:
                sp=self.machine.get(f"WVS7/C/{sid}")
                if self.ledger.stage_entry(sp.address) is None: _skip(self.machine,self.ledger,sp,self.repo.head,source_sha)
        return nxt,rh
    def run(self, *, resume: bool):
        self.verify_static_gates(); self.bind_initial_manifest_prefix()
        if self.backend is None: raise StageExecutionError("--run/--resume requires backend")
        a=self.machine.first_unfinished; seen=set()
        while a != "__COURT_COMPLETE__":
            if a in seen: raise StageStateError(f"continuation loop at {a}")
            seen.add(a); stage=self.machine.get(a); old=self.ledger.stage_entry(a)
            if old and old.get("terminal_disposition") in COMPLETE_LEDGER_DISPOSITIONS:
                if not resume: raise StageStateError(f"terminal stage {a} already exists; use --resume")
                old=self.ledger.revalidate_terminal(a); n=old["next_stage"]
                if n=="__COMMON_SOURCE_BLOCKER__":
                    a=_source_stop(self.machine,self.ledger,source=stage.source,head=self.repo.head,source_sha=self.frozen_source_sha(stage.source),blocker=a)
                    self.progress.emit_completed_cells()
                    continue
                if n=="__COMMON_COURT_BLOCKER__": return self._summary("BLOCKED__COMMON_COURT_AUTHORITY",a)
                a=n; continue
            if old and old.get("state")=="RUNNING" and not resume: raise StageStateError(f"partial stage {a}; use --resume")
            is_final = stage.address==self.machine.final_stage_id
            stage_start_ns=self.progress.now_ns()
            if is_final:
                if old and old.get("state")=="RUNNING":
                    self.ledger.discard_empty_running_preterminal(stage)
                    old=None
                try:
                    _final_ready(self.machine,self.ledger)
                except CandidateLocalFailure:
                    return self._summary(
                        "COURT_SEQUENCE_COMPLETE__CANDIDATE_LOCAL_FAILURES_RECORDED__S17_SUCCESS_VERIFIER_NOT_RUN",
                        "__COURT_COMPLETE__",
                    )
                except CommonAuthorityBlocker:
                    self.progress.emit_stage(
                        stage,"BLOCKED",next_stage=stage.address,
                        elapsed_stage_ns=self.progress.now_ns()-stage_start_ns,
                        terminal_disposition="BLOCKED_BY_COMMON_COURT_AUTHORITY",
                    )
                    return self._summary("BLOCKED__UNRESOLVED_COMMON_AUTHORITY_AT_S17",stage.address)
            sha=self.source_sha_for_stage(stage); roots=_candidate_roots(self.work_root,stage.source,stage.candidate); ih=_input_identity(self.machine,stage,sha,self.repo.head)
            if stage.disposition=="DONE__PRESERVE":
                a,_=_preserve(self.machine,self.ledger,stage,self.repo_root,self.repo.head,sha)
                self.progress.emit_stage(stage,"PRESERVE",next_stage=a,elapsed_stage_ns=self.progress.now_ns()-stage_start_ns,terminal_disposition="PRESERVED")
                self.progress.emit_completed_cells()
                continue
            if stage.disposition=="SKIP__NOT_APPLICABLE_BY_FROZEN_LAW":
                a,_=_skip(self.machine,self.ledger,stage,self.repo.head,sha)
                self.progress.emit_stage(stage,"SKIP",next_stage=a,elapsed_stage_ns=self.progress.now_ns()-stage_start_ns,terminal_disposition="SKIPPED_BY_FROZEN_LAW")
                self.progress.emit_completed_cells()
                continue
            if stage.disposition=="TERMINAL_CANDIDATE_LOCAL_FAILURE__PRESERVE":
                a,_=self._preserved_wvs_c(stage,sha)
                self.progress.emit_stage(stage,"CANDIDATE_LOCAL_FAILURE",next_stage=a,elapsed_stage_ns=self.progress.now_ns()-stage_start_ns,terminal_disposition="CANDIDATE_LOCAL_FAILURE")
                self.progress.emit_completed_cells()
                continue
            if stage.disposition!="READY__RUN_LOCALLY": raise StageStateError(f"unexpected disposition {stage.disposition}")
            self.progress.emit_stage(stage,"START",next_stage=None,elapsed_stage_ns=None)
            if not is_final: self.ledger.begin(stage,ih)
            elif self.ledger.stage_entry(stage.address) is not None: raise StageStateError("S17 must be absent before backend verification")
            ctx=StageContext(BACKEND_CONTRACT,stage,self.work_root,roots,self.source_paths.get(stage.source) if stage.empirical_source_access_required else None,sha,self.machine.identity,P2X_BRANCH,self.repo.head,ih)
            try: result=self.backend.run_stage(ctx,self.services)
            except CandidateLocalFailure as exc: result=BackendResult("CANDIDATE_LOCAL_FAILURE",{"error":str(exc),**exc.receipt},verifier_complete=True)
            except CommonAuthorityBlocker as exc: result=BackendResult("COMMON_SOURCE_BLOCKER" if exc.scope=="SOURCE" else "COMMON_COURT_BLOCKER",{"error":str(exc),"scope":exc.scope,**exc.receipt},verifier_complete=True)
            except Exception as exc: raise StageExecutionError(f"untyped backend failure at {a}: {exc}") from exc
            n,rh,disp=_backend_terminal(self.machine,self.ledger,stage,self.repo.head,sha,result)
            if stage.physical_host_measurement_required:
                print("RAWLSING_LOCAL_SUPERVISOR_ACTION "+json.dumps(_token(stage,rh,self.ledger.hash(),self.repo.head),sort_keys=True,separators=(",",":")),file=sys.stderr,flush=True)
            if disp=="CANDIDATE_LOCAL_FAILURE" and stage.address!=self.machine.final_stage_id:
                _candidate_stop(self.machine,self.ledger,source=stage.source,candidate=stage.candidate,head=self.repo.head,source_sha=sha,blocker=stage.address)
            if stage.address==self.machine.final_stage_id and disp=="CANDIDATE_LOCAL_FAILURE": raise StageStateError("candidate-local failure forbidden at S17")
            if disp=="BLOCKED_BY_COMMON_SOURCE_AUTHORITY":
                a=_source_stop(self.machine,self.ledger,source=stage.source,head=self.repo.head,source_sha=sha,blocker=stage.address)
                progress_state="BLOCKED"
            elif disp=="BLOCKED_BY_COMMON_COURT_AUTHORITY":
                a=stage.address
                progress_state="BLOCKED"
            elif disp=="CANDIDATE_LOCAL_FAILURE":
                a=n
                progress_state="CANDIDATE_LOCAL_FAILURE"
            else:
                a=n
                progress_state="PASS"
            self.progress.emit_stage(
                stage,progress_state,next_stage=a,
                elapsed_stage_ns=self.progress.now_ns()-stage_start_ns,
                terminal_disposition=disp,
            )
            self.progress.emit_completed_cells()
            if disp=="BLOCKED_BY_COMMON_COURT_AUTHORITY":
                return self._summary("BLOCKED__COMMON_COURT_AUTHORITY",stage.address)
        return self._summary("COURT_SEQUENCE_COMPLETE__S17_VERIFIED",a)
    def _summary(self,status,address):
        ledger_sha=self.ledger.hash()
        self.progress.emit_court_terminal(status=status,next_stage=address,ledger_sha256=ledger_sha)
        return {"schema":"RAWLSING_EE_P2X_DARWIN_DRIVER_RUN@1.0.0","status":status,"next_stage":address,"ledger_sha256":ledger_sha,"observed_p2x_head":self.repo.head,"measured_synthesis_performed":False,"progress_jsonl":str(self.progress.path)}

# ---- CLI ------------------------------------------------------------------------------
def _parser():
    p=argparse.ArgumentParser(); m=p.add_mutually_exclusive_group(required=True)
    for x in ("preflight","status","run","resume","verify-only"): m.add_argument(f"--{x}",action="store_true")
    p.add_argument("--continuation-map",type=Path,required=True)
    p.add_argument("--work-root",type=Path,required=True)
    p.add_argument("--repo-root",type=Path,default=Path.cwd())
    p.add_argument("--lits-path",type=Path)
    p.add_argument("--wvs-path",type=Path)
    p.add_argument("--backend-module")
    p.add_argument("--frozen-upstream-receipt",type=Path)
    p.add_argument("--current-court-contract",type=Path)
    p.add_argument("--succession-manifest",type=Path)
    p.add_argument("--succession-lifecycle-context",type=Path)
    p.add_argument("--succession-preflight-receipt",type=Path)
    return p

def main(argv: Sequence[str] | None=None):
    args=_parser().parse_args(argv)
    machine=load_current_execution_manifest(args.continuation_map)
    work=args.work_root.resolve()
    repo_root=args.repo_root.resolve()
    paths={}
    executing=bool(args.run or args.resume)
    t5_controlled=bool(args.preflight or executing)
    court_contract_path=None
    if t5_controlled:
        if args.current_court_contract is None:
            raise RuntimeGateError("--preflight/--run/--resume requires --current-court-contract")
        from rawlsing_next.fiabc_live_terminal_control import validate_current_court_contract_file
        court_contract_path=args.current_court_contract.resolve()
        validate_current_court_contract_file(court_contract_path,machine.document)
        os.environ["RAWLSING_FIABC_T5_CURRENT_COURT_CONTRACT"]=str(court_contract_path)
        os.environ["RAWLSING_FIABC_T5_CURRENT_EXECUTION_MANIFEST"]=str(args.continuation_map.resolve())
    if args.preflight or executing:
        if args.lits_path is None or args.wvs_path is None:
            raise RuntimeGateError("explicit --lits-path and --wvs-path required")
        paths={"LITS_I":args.lits_path.resolve(),"WVS7":args.wvs_path.resolve()}

    if executing:
        if args.frozen_upstream_receipt is None:
            raise RuntimeGateError(
                "--run/--resume requires --frozen-upstream-receipt; "
                "candidate execution may not begin before source/authority/workload/oracle freeze"
            )
        freeze_path=args.frozen_upstream_receipt.resolve()
        validate_frozen_upstream_for_machine(machine,freeze_path)
        os.environ[FROZEN_UPSTREAM_ENV]=str(freeze_path)
        from rawlsing_next.fiabc_live_terminal_control import load_frozen_source_oracle
        for source_id in machine.document.get("source_order",()):
            load_frozen_source_oracle(
                freeze_path=freeze_path,source=source_id,work_root=work
            )
        if args.succession_preflight_receipt is None:
            raise RuntimeGateError("--run/--resume requires --succession-preflight-receipt")
        from rawlsing_next.fiabc_live_terminal_control import validate_live_succession_preflight_receipt
        preflight_path=args.succession_preflight_receipt.resolve()
        validate_live_succession_preflight_receipt(
            preflight_path,repo_head=observe_repo(repo_root).head,
            court_contract_path=court_contract_path,current_manifest=machine.document,
        )
        os.environ["RAWLSING_FIABC_T5_SUCCESSION_PREFLIGHT_RECEIPT"]=str(preflight_path)
        from rawlsing_next.fiabc_live_accounting_binding import authorized_same_cell_transitions
        os.environ["RAWLSING_EE_P2X_WARM_STATE_TRANSITIONS"]=",".join(
            authorized_same_cell_transitions(machine.document.get("stage_catalog",()))
        )
        if args.backend_module != ISOLATED_BACKEND_MODULE:
            raise RuntimeGateError(
                "FIABC-T3 execution requires the process-isolated backend adapter; "
                "direct candidate-backend execution is forbidden"
            )
    elif args.frozen_upstream_receipt is not None:
        validate_frozen_upstream_for_machine(machine,args.frozen_upstream_receipt.resolve())

    backend=_load_backend(args.backend_module) if args.backend_module else None
    lock_root=repo_root/".git" if (repo_root/".git").is_dir() else work
    with DriverInstanceLock(lock_root):
        d=DarwinCourtDriver(
            machine=machine,work_root=work,repo_root=repo_root,source_paths=paths,
            host=observe_host(),repo=observe_repo(repo_root),backend=backend
        )
        if args.status:
            out={"schema":"RAWLSING_EE_P2X_DARWIN_DRIVER_STATUS@1.0.0","next_stage":d.next_stage(),"ledger_sha256":d.ledger.hash()}
        elif args.preflight:
            if args.succession_manifest is None or args.succession_lifecycle_context is None:
                raise RuntimeGateError(
                    "--preflight requires --succession-manifest and --succession-lifecycle-context"
                )
            base_out=d.preflight()
            from rawlsing_next.fiabc_live_terminal_control import run_live_succession_preflight
            t5_path=work/"court"/"fiabc_t5_succession_preflight.json"
            t5=run_live_succession_preflight(
                manifest_path=args.succession_manifest.resolve(),
                lifecycle_context_path=args.succession_lifecycle_context.resolve(),
                repo_root=repo_root,repo_head=d.repo.head,
                court_contract_path=court_contract_path,current_manifest=machine.document,
                output_path=t5_path,
            )
            out={**base_out,"t5_succession_preflight":t5,
                 "t5_succession_preflight_path":str(t5_path)}
        elif getattr(args,"verify_only"):
            out=d.verify_only()
        else:
            if backend is None:
                raise StageExecutionError("--run/--resume requires --backend-module")
            out=d.run(resume=bool(args.resume))
    print(json.dumps(out,sort_keys=True,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
