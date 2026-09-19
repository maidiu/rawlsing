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
from typing import Any, Callable, Iterable, Mapping, Protocol, Sequence

CONTINUATION_MAP_SCHEMA = "RAWLSING_EE_P2X_CONTINUATION_STATE_MACHINE@1.0.0"
CONTINUATION_MAP_SHA256 = "ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422"
CONTINUATION_MAP_GIT_BLOB_SHA1 = "e06e95dd370a4fd44235932088308c3372522ed4"
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
R8B_RU_MAXRSS_LAW = "DARWIN_RU_MAXRSS_ALREADY_BYTES"
LEDGER_SCHEMA = "RAWLSING_EE_P2X_DARWIN_STAGE_LEDGER@1.0.0"
BACKEND_CONTRACT = "RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0"
SUPERVISOR_TOKEN_SCHEMA = "RAWLSING_EE_P2X_LOCAL_SUPERVISOR_ACTION@1.0.0"
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
        if self.path.exists(): self.data = json.loads(self.path.read_text())
        else:
            self.data = {"schema": LEDGER_SCHEMA, "continuation_map": dataclasses.asdict(machine.identity), "p2x_branch": P2X_BRANCH, "p2x_resume_head": P2X_RESUME_HEAD, "source_order": list(EXPECTED_SOURCE_ORDER), "candidate_order": list(EXPECTED_CANDIDATE_ORDER), "source_identities": {}, "stages": {}}; self.flush()
        if self.data.get("schema") != LEDGER_SCHEMA or self.data.get("continuation_map") != dataclasses.asdict(machine.identity) or self.data.get("source_order") != list(EXPECTED_SOURCE_ORDER) or self.data.get("candidate_order") != list(EXPECTED_CANDIDATE_ORDER): raise StageStateError("ledger authority drift")
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
    def compose_p2r1_binding(self, *, authority_documents: Iterable[Mapping[str,Any]], predicate_documents: Iterable[Mapping[str,Any]], query_documents: Iterable[Mapping[str,Any]], discovery_authority_documents: Iterable[Mapping[str,Any]], projection_fields: Mapping[str,Any], candidate: str, builder_kwargs: Mapping[str,Any], builder_identity: Mapping[str,Any]):
        from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, bind_governed_c11_projection, bind_repository_builder
        catalog = RuntimeObjectCatalog.from_documents(authority_documents=authority_documents, predicate_documents=predicate_documents, query_documents=query_documents, discovery_authority_documents=discovery_authority_documents)
        projection = bind_governed_c11_projection(projection_fields); kw = dict(builder_kwargs)
        if "projection" in kw and kw["projection"] is not projection: raise StageExecutionError("projection substitution forbidden")
        kw["projection"] = projection
        return bind_repository_builder(repository_builder=self.accepted_repository_builder(candidate), builder_kwargs=kw, builder_identity=builder_identity, runtime_catalog=catalog)

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
    return _mechanical_terminal(machine,ledger,stage,head,source_sha,"PRESERVED",{"schema":"RAWLSING_EE_P2X_PRESERVED_STAGE_BINDING@1.0.0","evidence_ref":stage.evidence_or_stop_law_ref,"evidence":dict(d),"evidence_sha256":_sha256_bytes(data),"evidence_git_blob_sha1":_git_blob_sha1(data),"source_access_performed":False},stage.next_stage_on_pass)
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
    for c in EXPECTED_CANDIDATE_ORDER:
        for sid in machine.document.get("stage_catalog",()):
            sp=machine.stages[f"{source}/{c}/{sid}"]
            if ledger.stage_entry(sp.address) is None: _mechanical_terminal(machine,ledger,sp,head,source_sha,"BLOCKED_BY_COMMON_SOURCE_AUTHORITY",{"schema":"RAWLSING_EE_P2X_COMMON_SOURCE_BLOCK_PROPAGATION@1.0.0","blocker_stage":blocker},"__SOURCE_BLOCKED__")
    i=EXPECTED_SOURCE_ORDER.index(source); return machine.final_stage_id if i+1==len(EXPECTED_SOURCE_ORDER) else f"{EXPECTED_SOURCE_ORDER[i+1]}/A/S00_SOURCE_PREFLIGHT_IDENTITY"
def _mark_source_blocked(machine, ledger, *, source: str, observed_head: str, source_sha256: str, blocker_stage: str):
    return _source_stop(machine, ledger, source=source, head=observed_head, source_sha=source_sha256, blocker=blocker_stage)
def _backend_terminal(machine,ledger,stage,head,source_sha,result):
    if result.terminal_disposition not in {"PASS","CANDIDATE_LOCAL_FAILURE","COMMON_SOURCE_BLOCKER","COMMON_COURT_BLOCKER"}: raise StageStateError("backend terminal disposition invalid")
    if not result.verifier_complete: raise StageStateError("backend result incomplete: verifier did not complete")
    ih=_input_identity(machine,stage,source_sha,head); roots=_candidate_roots(ledger.work_root,stage.source,stage.candidate)
    receipt=_write_receipt(roots,stage,{"schema":"RAWLSING_EE_P2X_DARWIN_STAGE_RECEIPT_ENVELOPE@1.0.0","stage":stage.address,"backend_contract":BACKEND_CONTRACT,"terminal_disposition":result.terminal_disposition,"input_identity_hash":ih,"measured_payload":dict(result.receipt)})
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
    if ledger.stage_entry("WVS7/C/S01_CANDIDATE_PREPARATION_BUILD").get("terminal_disposition") != "CANDIDATE_LOCAL_FAILURE": raise StageStateError("WVS-C portability failure not bound")
def _token(stage,receipt_hash,ledger_hash,head): return {"schema":SUPERVISOR_TOKEN_SCHEMA,"action":"COMMIT_AND_PUSH_EXISTING_P2X_BRANCH_BOUNDED_STAGE_EVIDENCE","stage_id":stage.address,"terminal_receipt_sha256":receipt_hash,"ledger_sha256":ledger_hash,"p2x_branch":P2X_BRANCH,"observed_branch_head":head}

# ---- driver ---------------------------------------------------------------------------
class DarwinCourtDriver:
    def __init__(self, *, machine, work_root, repo_root, source_paths, host, repo, backend):
        self.machine,self.work_root,self.repo_root,self.source_paths,self.host,self.repo,self.backend=machine,work_root,repo_root,dict(source_paths),host,repo,backend
        self._verified_sources_this_process={}; self.ledger=StageLedger(work_root,machine,repo_root); self.services=DriverServices(repo_root=repo_root,work_root=work_root)
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
    def bind_initial_preserved_prefix(self):
        sha=self.frozen_source_sha("LITS_I")
        for a in ("LITS_I/A/S00_SOURCE_PREFLIGHT_IDENTITY","LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD"):
            if self.ledger.stage_entry(a) is None: _preserve(self.machine,self.ledger,self.machine.get(a),self.repo_root,self.repo.head,sha)
    def preflight(self):
        self.verify_static_gates(); verified={s:self.ensure_source_verified(s) for s in EXPECTED_SOURCE_ORDER}; owners={}
        for c,sp in OWNER_SPECS.items():
            data=_git_show_bytes(self.repo_root,OWNER_COMMIT,sp["path"]); blob=_git_blob_sha1(data)
            if blob != sp["blob"]: raise OwnerDeploymentError(f"Candidate-{c} owner blob drift")
            owners[c]=blob
        self.bind_initial_preserved_prefix()
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
        self.verify_static_gates(); self.bind_initial_preserved_prefix()
        if self.backend is None: raise StageExecutionError("--run/--resume requires backend")
        a=self.machine.first_unfinished; seen=set()
        while a != "__COURT_COMPLETE__":
            if a in seen: raise StageStateError(f"continuation loop at {a}")
            seen.add(a); stage=self.machine.get(a); old=self.ledger.stage_entry(a)
            if old and old.get("terminal_disposition") in COMPLETE_LEDGER_DISPOSITIONS:
                if not resume: raise StageStateError(f"terminal stage {a} already exists; use --resume")
                old=self.ledger.revalidate_terminal(a); n=old["next_stage"]
                if n=="__COMMON_SOURCE_BLOCKER__": a=_source_stop(self.machine,self.ledger,source=stage.source,head=self.repo.head,source_sha=self.frozen_source_sha(stage.source),blocker=a); continue
                if n=="__COMMON_COURT_BLOCKER__": return self._summary("BLOCKED__COMMON_COURT_AUTHORITY",a)
                a=n; continue
            if old and old.get("state")=="RUNNING" and not resume: raise StageStateError(f"partial stage {a}; use --resume")
            is_final = stage.address==self.machine.final_stage_id
            if is_final:
                if old and old.get("state")=="RUNNING":
                    self.ledger.discard_empty_running_preterminal(stage)
                    old=None
                try: _final_ready(self.machine,self.ledger)
                except CommonAuthorityBlocker: return self._summary("BLOCKED__UNRESOLVED_COMMON_AUTHORITY_AT_S17",stage.address)
            sha=self.source_sha_for_stage(stage); roots=_candidate_roots(self.work_root,stage.source,stage.candidate); ih=_input_identity(self.machine,stage,sha,self.repo.head)
            if stage.disposition=="DONE__PRESERVE": a,_=_preserve(self.machine,self.ledger,stage,self.repo_root,self.repo.head,sha); continue
            if stage.disposition=="SKIP__NOT_APPLICABLE_BY_FROZEN_LAW": a,_=_skip(self.machine,self.ledger,stage,self.repo.head,sha); continue
            if stage.disposition=="TERMINAL_CANDIDATE_LOCAL_FAILURE__PRESERVE": a,_=self._preserved_wvs_c(stage,sha); continue
            if stage.disposition!="READY__RUN_LOCALLY": raise StageStateError(f"unexpected disposition {stage.disposition}")
            if not is_final: self.ledger.begin(stage,ih)
            elif self.ledger.stage_entry(stage.address) is not None: raise StageStateError("S17 must be absent before backend verification")
            ctx=StageContext(BACKEND_CONTRACT,stage,self.work_root,roots,self.source_paths.get(stage.source) if stage.empirical_source_access_required else None,sha,self.machine.identity,P2X_BRANCH,self.repo.head,ih)
            try: result=self.backend.run_stage(ctx,self.services)
            except CandidateLocalFailure as exc: result=BackendResult("CANDIDATE_LOCAL_FAILURE",{"error":str(exc),**exc.receipt},verifier_complete=True)
            except CommonAuthorityBlocker as exc: result=BackendResult("COMMON_SOURCE_BLOCKER" if exc.scope=="SOURCE" else "COMMON_COURT_BLOCKER",{"error":str(exc),"scope":exc.scope,**exc.receipt},verifier_complete=True)
            except Exception as exc: raise StageExecutionError(f"untyped backend failure at {a}: {exc}") from exc
            n,rh,disp=_backend_terminal(self.machine,self.ledger,stage,self.repo.head,sha,result)
            if stage.physical_host_measurement_required: print("RAWLSING_LOCAL_SUPERVISOR_ACTION "+json.dumps(_token(stage,rh,self.ledger.hash(),self.repo.head),sort_keys=True,separators=(",",":")))
            if disp=="CANDIDATE_LOCAL_FAILURE" and stage.address!=self.machine.final_stage_id: _candidate_stop(self.machine,self.ledger,source=stage.source,candidate=stage.candidate,head=self.repo.head,source_sha=sha,blocker=stage.address)
            if stage.address==self.machine.final_stage_id and disp=="CANDIDATE_LOCAL_FAILURE": raise StageStateError("candidate-local failure forbidden at S17")
            if disp=="BLOCKED_BY_COMMON_SOURCE_AUTHORITY": a=_source_stop(self.machine,self.ledger,source=stage.source,head=self.repo.head,source_sha=sha,blocker=stage.address)
            elif disp=="BLOCKED_BY_COMMON_COURT_AUTHORITY": return self._summary("BLOCKED__COMMON_COURT_AUTHORITY",stage.address)
            else: a=n
        return self._summary("COURT_SEQUENCE_COMPLETE__S17_VERIFIED",a)
    def _summary(self,status,address): return {"schema":"RAWLSING_EE_P2X_DARWIN_DRIVER_RUN@1.0.0","status":status,"next_stage":address,"ledger_sha256":self.ledger.hash(),"observed_p2x_head":self.repo.head,"measured_synthesis_performed":False}

# ---- CLI ------------------------------------------------------------------------------
def _parser():
    p=argparse.ArgumentParser(); m=p.add_mutually_exclusive_group(required=True)
    for x in ("preflight","status","run","resume","verify-only"): m.add_argument(f"--{x}",action="store_true")
    p.add_argument("--continuation-map",type=Path,required=True); p.add_argument("--work-root",type=Path,required=True); p.add_argument("--repo-root",type=Path,default=Path.cwd()); p.add_argument("--lits-path",type=Path); p.add_argument("--wvs-path",type=Path); p.add_argument("--backend-module"); return p
def main(argv: Sequence[str] | None=None):
    args=_parser().parse_args(argv); machine=load_continuation_map(args.continuation_map); work=args.work_root.resolve(); repo_root=args.repo_root.resolve(); paths={}
    if args.preflight or args.run or args.resume:
        if args.lits_path is None or args.wvs_path is None: raise RuntimeGateError("explicit --lits-path and --wvs-path required")
        paths={"LITS_I":args.lits_path.resolve(),"WVS7":args.wvs_path.resolve()}
    backend=_load_backend(args.backend_module) if args.backend_module else None; lock_root=repo_root/".git" if (repo_root/".git").is_dir() else work
    with DriverInstanceLock(lock_root):
        d=DarwinCourtDriver(machine=machine,work_root=work,repo_root=repo_root,source_paths=paths,host=observe_host(),repo=observe_repo(repo_root),backend=backend)
        if args.status: out={"schema":"RAWLSING_EE_P2X_DARWIN_DRIVER_STATUS@1.0.0","next_stage":d.next_stage(),"ledger_sha256":d.ledger.hash()}
        elif args.preflight: out=d.preflight()
        elif getattr(args,"verify_only"): out=d.verify_only()
        else:
            if backend is None: raise StageExecutionError("--run/--resume requires --backend-module")
            out=d.run(resume=bool(args.resume))
    print(json.dumps(out,sort_keys=True,indent=2)); return 0
if __name__=="__main__": raise SystemExit(main())
