"""EE-P2X production Darwin stage backend.

The qualified court driver owns orchestration, ledger/resume, preserved/skipped
historical stages and supervisor tokens. This module implements only
READY__RUN_LOCALLY stage bodies, including the current six-cell Candidate-C
binding selected by the successor execution manifest.

Import is source-inert. Real source bytes are opened only when the driver puts a
source_path in the StageContext. Missing exact authority is a typed blocker; no
hash inversion, semantic inference, synthetic timing or surrogate outcome is
permitted.
"""
from __future__ import annotations

import contextlib
import dataclasses
import hashlib
import importlib.util
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import resource
import shutil
import subprocess
import sys
import tempfile
import types
import time
from typing import Any, Mapping

BACKEND_CONTRACT = "RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0"
STATE_SCHEMA = "RAWLSING_EE_P2X_PRODUCTION_BACKEND_STATE@1.0.0"

OWNER_COMMIT = "0b96b8de9aac774566f872cf0630ebd4ddeb70e6"
P2R1_PASS = "9511f44728a8469d685463ec0fc880864c9187de"
P2F2_PASS = "R6S_PACKAGED_EXACT_P2F2"
LITS_BANKED_COMMIT = "3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f"
B12_RETURN = "R6O_CURRENT_RUNTIME_ONLY"
B12_PRODUCER_COMMIT = "cfc240aa3a64c59509eab97450a7d3603af813cc"
NODE4A_COMMIT = "4d66bc34c256f6bf3f9f707dda80d963881f3510"

LITS_SHA = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
WVS_SHA = "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d"
LITS_PROJECTION = "84361298ae702786a3fd1044bf619ffa4fe9ed2877040724386951e9c9d27872"
LITS_PRODUCT = "47d36b1459c2458c480b58631d2c78af68be4dde44015a9220b09177b1eeb28d"
LITS_REPLAY = "301735d4563314a0d7c133fa1afbb0ca57679b3fad887c66e77a909494779eb5"
WVS_LOCK2 = "5e2a53f0e5f3b6ddd8db53b724b352ca41fe1a49408483fbf83dfdaa96283139"
WVS_LOCK2_REPLAY = "9b5ac1726a03798d07e965396192d1bfefbee6d2188bad5a3acfb467ef063d4a"
WVS_DISCOVERY_AUTHORITY = "3aee36014e4c3b39dd36bfef46006d8e9058a93aa5eb53bd81aef627883c8873"
R6O_RUNTIME_CATALOG = "5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02"
R6O_ACTIVE_BINDING = "a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308"
R6O_RUNTIME_RELEASE = "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f"
R6S_WVS_PROJECTION = "f400c804fea9b526f25eac823138ecb30e10efaad3207c4578661f684adee665"
R6S_WVS_COORDINATE = "4a688332dca6462f357b092e7dfdba1216739139fd74e1c84395420827d153b6"
R6S_WVS_COORDINATE_AUTHORITY = "9e7f98a7ad723743771d6bea39077553d2a3920ac4c077e90720bb9e44da029d"
R6S_RUNTIME_PACKAGE = "rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json"
R6S_MATERIALIZER = "rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py"
R6S_LITS_SUPPORT = "rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py"
FROZEN_PYREADSTAT_VERSION = "1.3.6"
WVS_MATERIALIZER_BLOB = "ec685803a7416032037ee415e8faf7bf60db8f1b"
LITS_A_ADAPTER_BLOB = "d4915e7e6755ba1850756aebff72f982f73a332b"
LITS_B_FACADE_BLOB = "7c509c2098d0030f253344eb3f682471378812a8"
LITS_R5_BUILDER_BLOB = "92e364b31eaf27be1bca2081eff65f6ffb779c3d"
LITS_A_PARENTAGE_PATH_ENV = "RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT"
LITS_A_PARENTAGE_ID_ENV = "RAWLSING_EE_P2X_LITS_A_R5_PARENTAGE_RECEIPT_IDENTITY"
_SESSIONS: dict[tuple[str,str], tuple[Any,Any]] = {}
_T4_ACTIVE_CONTEXT = None
_T4_ACTIVE_STATE = None

EXPECTED_SOURCE = {"LITS_I": LITS_SHA, "WVS7": WVS_SHA}

READY = frozenset({
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
    "S17_FINAL_COMPLETENESS_AND_VERIFICATION",
})

METRICS = (
    "source_open_count", "source_decode_count", "source_reread_count",
    "bytes_read", "bytes_written", "bytes_rewritten",
    "candidate_total_wall_ns", "build_or_open_wall_ns",
    "cpu_user_ns", "cpu_system_ns", "peak_rss_bytes",
    "peak_scratch_bytes", "peak_scratch_file_count",
    "durable_authoritative_bytes", "durable_transformed_regenerable_bytes",
    "warm_retained_state_bytes",
    "cold_i03_latency_ns", "warm_i03_latency_ns",
    "i05_learned_production_wall_ns", "i05_learned_production_throughput_per_s",
    "repeated_research_source_open_count", "repeated_research_source_redecode_count",
    "repeated_research_source_reread_count",
    "delete_rebuild_wall_ns",
    "source_release_invalidation_recomputation_units",
    "source_release_invalidation_wall_ns",
    "source_release_invalidation_bytes_rewritten",
    "semantic_authority_invalidation_recomputation_units",
    "semantic_authority_invalidation_wall_ns",
    "semantic_authority_invalidation_bytes_rewritten",
    "fresh_process_replay_wall_ns", "fresh_process_replay_cpu_ns",
    "audit_wall_ns",
    "persistent_bytes_removable_with_zero_information_loss",
    "implementation_moving_parts_count",
)

LITS_BUILDER = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/"
    "banked_as2b/run_as2b_lits1_mechanical_certification.py"
)
LITS_AS2A = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/"
    "banked_as2a"
)
LITS_LEDGER = LITS_AS2A + "/01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv"
LITS_PACKAGE = LITS_AS2A + "/04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json"
NODE4A = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/AS3R3_NODE4A_PREDICATE_INPUT_FREEZE_20260827/PREDICATE_INPUTS.py"
)
B6_QUERIES = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/"
    "WORKERS/B6_AS3R3_NODE4B_QUERY_INPUT_FREEZE_R1/01_QUERY_INPUTS.json"
)
B13_DISCOVERY = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/PRE_MAIN_RECONCILIATION_R1/WHOLE_SPINE_BUILD_CONSTITUTION_R1/"
    "RAWLSING_BUILD_WAR_PLAN_R1/CENTRAL_SYNTHESIS_R1/"
    "SUB_VOZHD_CAMPAIGN_INTEGRATION_R1/B_ARCHITECTURE_COMPILER_DVA_CHETIRI_R1/"
    "WORKERS/B13_AS3R3_SUCCESSOR_DISCOVERY_FRONTIER_REPLAY_SEAL_R1/"
    "03_SUCCESSOR_DISCOVERY_AUTHORITY.json"
)
P2F2 = {
    "authority": "WORKER_RETURNS/EE-P2F2/01_WVS7_PRE553_ISSUED_AUTHORITY_SNAPSHOTS.json",
    "predicate": "WORKER_RETURNS/EE-P2F2/03_WVS7_RESPONSE_ATOM_AND_PREDICATE_BINDINGS.json",
    "query": "WORKER_RETURNS/EE-P2F2/04_WVS7_QUERY_TEMPLATE_BINDINGS.json",
    "discovery": "WORKER_RETURNS/EE-P2F2/05_WVS7_DISCOVERY_AUTHORITY_AND_FRONTIER_BINDING.json",
    "lock2": "WORKER_RETURNS/EE-P2F2/08_LOCK2_ISSUER_RECEIPT.json",
}
PUBLIC_KEYS = frozenset({
    "schema_id", "schema_version", "typed_state", "authority_snapshot_refs",
    "dependency_refs", "producer_replay_locator_or_reference_root",
    "semantic_fields", "object_id", "content_hash",
})


class BackendStop(RuntimeError):
    terminal = "CANDIDATE_LOCAL_FAILURE"
    kind = "CANDIDATE_LOCAL_CORRECTNESS_FAILURE"
    scope = "CANDIDATE_ONLY"
    def __init__(self, message: str, detail: Mapping[str, Any] | None = None):
        super().__init__(message)
        self.detail = dict(detail or {})


class SourceAuthorityStop(BackendStop):
    terminal = "COMMON_SOURCE_BLOCKER"
    kind = "COMMON_SOURCE_AUTHORITY_FAILURE"
    scope = "SOURCE_ONLY"


class CourtAuthorityStop(BackendStop):
    terminal = "COMMON_COURT_BLOCKER"
    kind = "COMMON_COURT_AUTHORITY_FAILURE"
    scope = "COURT_UNTIL_RESUME"


def _cj(v: Any) -> bytes:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()


def _h(v: Any) -> str:
    return hashlib.sha256(_cj(v)).hexdigest()


def _sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(8 * 1024 * 1024), b""):
            h.update(b)
    return h.hexdigest()


def _blob(data: bytes) -> str:
    return hashlib.sha1(("blob " + str(len(data)) + "\0").encode() + data).hexdigest()


def _git(repo: Path, *args: str, check: bool = True):
    return subprocess.run(["git", "-C", str(repo), *args], check=check,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def _git_bytes(repo: Path, commit: str, path: str) -> bytes:
    if _git(repo, "cat-file", "-e", commit + "^{commit}", check=False).returncode:
        if _git(repo, "fetch", "--no-tags", "origin", commit, check=False).returncode:
            raise CourtAuthorityStop("immutable commit unavailable", {"commit": commit})
    p = _git(repo, "show", commit + ":" + path, check=False)
    if p.returncode:
        raise CourtAuthorityStop("immutable path unavailable", {"commit": commit, "path": path})
    return p.stdout


def _git_json(repo: Path, commit: str, path: str) -> Any:
    try:
        return json.loads(_git_bytes(repo, commit, path).decode())
    except json.JSONDecodeError as exc:
        raise CourtAuthorityStop("immutable JSON malformed", {"commit": commit, "path": path}) from exc


def _deploy(repo: Path, work: Path, commit: str, path: str, expected_blob: str | None = None) -> Path:
    data = _git_bytes(repo, commit, path)
    if expected_blob and _blob(data) != expected_blob:
        raise CourtAuthorityStop("immutable blob drift", {"path": path, "expected": expected_blob, "got": _blob(data)})
    dest = work / "_be1_immutable" / commit / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.read_bytes() != data:
        raise CourtAuthorityStop("deployed immutable bytes drift", {"path": str(dest)})
    if not dest.exists():
        _write_bytes_tracked(dest, data, cost_class="C1")
    return dest


def _load(path: Path, name: str):
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, path)
    if not spec or not spec.loader:
        raise CourtAuthorityStop("cannot import immutable implementation", {"path": str(path)})
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return mod


def _atomic(path: Path, value: Mapping[str, Any]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False).encode() + b"\n"
    existed = path.exists()
    fd, tmp = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    tmp_path = Path(tmp)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        _tmp_oid="ATOMIC_TMP::"+_t4_object_id(tmp_path)
        _t4_note_scratch_size(tmp_path,len(data),object_id=_tmp_oid)
        os.replace(tmp, path)
        _t4_note_scratch_remove(tmp_path,object_id=_tmp_oid)
        _t4_note_file_write(path, len(data), rewrite=existed)
    finally:
        with contextlib.suppress(FileNotFoundError):
            tmp_path.unlink()
        _t4_note_scratch_remove(tmp_path,object_id="ATOMIC_TMP::"+_t4_object_id(tmp_path))
    return path


def _repo(services) -> Path:
    p = getattr(services, "repo_root", None)
    if not isinstance(p, Path):
        raise CourtAuthorityStop("DriverServices.repo_root unavailable")
    return p


def _state_path(ctx) -> Path:
    return ctx.roots.durable / "ee_p2x_backend_state.json"


def _new_state(ctx) -> dict[str, Any]:
    return {
        "schema": STATE_SCHEMA, "source": ctx.stage.source, "candidate": ctx.stage.candidate,
        "source_sha256": ctx.source_sha256, "event": 0, "metrics": {}, "behaviors": {},
        "outputs": {}, "bindings": {}, "parity": {}, "source_access": {"open": 0, "decode": 0, "reread": 0, "bytes": 0},
        "derivative_parentage": {},
        "oracle_frozen": None, "candidate_output_first": None, "parity_complete": None,
        "performance_first_admitted": None, "performance_admitted": False,
    }


def _state(ctx) -> dict[str, Any]:
    p = _state_path(ctx)
    if not p.exists():
        return _new_state(ctx)
    v = json.loads(p.read_text())
    if v.get("schema") != STATE_SCHEMA or v.get("source") != ctx.stage.source or v.get("candidate") != ctx.stage.candidate:
        raise BackendStop("durable backend state identity drift")
    return v


def _save(ctx, state) -> None:
    _atomic(_state_path(ctx), state)


def _ord(state) -> int:
    state["event"] += 1
    return state["event"]


def _dir_stats(p: Path) -> tuple[int, int]:
    total = count = 0
    if p.exists():
        for q in p.rglob("*"):
            if q.is_file():
                with contextlib.suppress(FileNotFoundError):
                    total += q.stat().st_size; count += 1
    return total, count


def _t4_active():
    return _T4_ACTIVE_CONTEXT, _T4_ACTIVE_STATE


def _t4_object_id(path: Path) -> str:
    ctx, _state = _t4_active()
    p = path.resolve()
    if ctx is not None:
        for label, root in (
            ("SCRATCH", getattr(ctx.roots, "scratch", None)),
            ("DURABLE", getattr(ctx.roots, "durable", None)),
            ("RECEIPTS", getattr(ctx.roots, "receipts", None)),
            ("CELL", getattr(ctx.roots, "root", None)),
        ):
            if root is None:
                continue
            r = Path(root).resolve()
            if p == r or r in p.parents:
                return label + "::" + p.relative_to(r).as_posix()
    return "PATH::" + str(p)


def _t4_current_lifecycle_action_id(state):
    return state.get("_t4_current_lifecycle_action_id")


def _t4_io_event(state, *, operation, byte_count, object_id, rewrite_of=None,
                 cost_class="C2", evidence_ref=None, lifecycle_action_id=None,
                 process_token=None):
    event = {
        "operation": operation,
        "byte_count": int(byte_count),
        "object_id": str(object_id),
        "rewrite_of": rewrite_of,
        "cost_class": cost_class,
        "evidence_ref": evidence_ref or "FIABC_T4_EXACT_IO_EVENT",
        "lifecycle_action_id": lifecycle_action_id,
    }
    if process_token is not None:
        event["process_token"] = process_token
    state.setdefault("_t4_io_events", []).append(event)
    return event


def _t4_note_scratch_size(path: Path, size: int, *, object_id=None, cost_class="C2",
                          lifecycle_action_id=None, process_token=None):
    ctx, state = _t4_active()
    if ctx is None or state is None:
        return
    p = path.resolve()
    scratch = Path(ctx.roots.scratch).resolve()
    if not (p == scratch or scratch in p.parents):
        return
    oid = object_id or _t4_object_id(path)
    tracker = state.setdefault("_t4_scratch_tracker", {})
    tracker[oid] = int(size)
    event = {
        "operation": "SIZE", "object_id": oid, "current_size_bytes": int(size),
        "cost_class": cost_class,
        "evidence_ref": "FIABC_T4_SCRATCH_MUTATION",
        "lifecycle_action_id": lifecycle_action_id,
    }
    if process_token is not None:
        event["process_token"] = process_token
    state.setdefault("_t4_scratch_events", []).append(event)


def _t4_note_scratch_temp(path: Path, size: int):
    _t4_note_scratch_size(path, size, object_id="ATOMIC_TMP::"+_t4_object_id(path))


def _t4_note_scratch_remove(path: Path, *, object_id=None, cost_class="C2",
                            lifecycle_action_id=None, process_token=None):
    ctx, state = _t4_active()
    if ctx is None or state is None:
        return
    p = path.resolve()
    scratch = Path(ctx.roots.scratch).resolve()
    if not (p == scratch or scratch in p.parents):
        return
    oid = object_id or _t4_object_id(path)
    tracker = state.setdefault("_t4_scratch_tracker", {})
    tracker.pop(oid, None)
    event = {
        "operation": "REMOVE", "object_id": oid, "cost_class": cost_class,
        "evidence_ref": "FIABC_T4_SCRATCH_MUTATION",
        "lifecycle_action_id": lifecycle_action_id,
    }
    if process_token is not None:
        event["process_token"] = process_token
    state.setdefault("_t4_scratch_events", []).append(event)


def _t4_note_file_write(path: Path, byte_count: int, *, rewrite=False, cost_class="C2",
                        lifecycle_action_id=None, process_token=None):
    ctx, state = _t4_active()
    if ctx is None or state is None:
        return
    oid = _t4_object_id(path)
    action_id = lifecycle_action_id
    if action_id is None:
        action_id = _t4_current_lifecycle_action_id(state)
    _t4_io_event(
        state, operation="WRITE", byte_count=byte_count, object_id=oid,
        rewrite_of=oid if rewrite else None, cost_class=cost_class,
        evidence_ref="FIABC_T4_EXACT_WRITE_EVENT",
        lifecycle_action_id=action_id, process_token=process_token,
    )
    _t4_note_scratch_size(
        path, byte_count, object_id=oid, cost_class=cost_class,
        lifecycle_action_id=action_id, process_token=process_token,
    )


def _write_bytes_tracked(path: Path, data: bytes, *, cost_class="C2",
                         lifecycle_action_id=None):
    path.parent.mkdir(parents=True, exist_ok=True)
    existed = path.exists()
    path.write_bytes(data)
    _t4_note_file_write(
        path, len(data), rewrite=existed, cost_class=cost_class,
        lifecycle_action_id=lifecycle_action_id,
    )
    return path


def _t4_note_file_read(path: Path, byte_count: int, *, cost_class="C2",
                       lifecycle_action_id=None, process_token=None, role="EXACT_READ"):
    _ctx, state = _t4_active()
    if state is None:
        return
    _t4_io_event(
        state, operation="READ", byte_count=byte_count, object_id=_t4_object_id(path),
        rewrite_of=None, cost_class=cost_class,
        evidence_ref="FIABC_T4_"+role, lifecycle_action_id=lifecycle_action_id,
        process_token=process_token,
    )


def _t4_remove_tree(path: Path, *, cost_class="C2", lifecycle_action_id=None):
    ctx, state = _t4_active()
    if ctx is not None and state is not None and path.exists():
        scratch = Path(ctx.roots.scratch).resolve()
        p = path.resolve()
        if p == scratch or scratch in p.parents:
            for q in sorted((x for x in path.rglob("*") if x.is_file()), reverse=True):
                _t4_note_scratch_size(
                    q, q.stat().st_size, cost_class=cost_class,
                    lifecycle_action_id=lifecycle_action_id,
                )
            for q in sorted((x for x in path.rglob("*") if x.is_file()), reverse=True):
                _t4_note_scratch_remove(
                    q, cost_class=cost_class, lifecycle_action_id=lifecycle_action_id,
                )
    shutil.rmtree(path, ignore_errors=True)


def _t4_metric_unavailable(state, *, name, reason,
                           metric_state="NOT_APPLICABLE_BY_FROZEN_COURT",
                           cost_class="C2", evidence_ref=None,
                           lifecycle_action_id=None):
    state.setdefault("_t4_metric_unavailable", []).append({
        "name": name, "state": metric_state, "reason": reason,
        "cost_class": cost_class,
        "evidence_ref": evidence_ref or "FIABC_T4_FROZEN_APPLICABILITY",
        "lifecycle_action_id": lifecycle_action_id,
    })


def _deep_size_bytes(value) -> int:
    seen=set()
    def walk(obj):
        oid=id(obj)
        if oid in seen:
            return 0
        seen.add(oid)
        size=sys.getsizeof(obj)
        if isinstance(obj, Mapping):
            return size + sum(walk(k)+walk(v) for k,v in obj.items())
        if isinstance(obj, (tuple,list,set,frozenset)):
            return size + sum(walk(v) for v in obj)
        if dataclasses.is_dataclass(obj) and not isinstance(obj,type):
            return size + sum(walk(getattr(obj,f.name)) for f in dataclasses.fields(obj))
        raw=getattr(obj,"__dict__",None)
        if isinstance(raw,dict):
            size += walk(raw)
        return size
    return int(walk(value))


def _durable_state_sizes(ctx):
    root=Path(ctx.roots.durable)
    authoritative=0
    transformed=0
    classified=[]
    ignored={
        "ee_p2x_backend_state.json",
        "fiabc_t4_candidate_state_guard.json",
    }
    if not root.exists():
        return 0,0,classified
    for q in sorted(x for x in root.rglob("*") if x.is_file()):
        rel=q.relative_to(root).as_posix()
        size=q.stat().st_size
        if rel in ignored:
            continue
        if (
            rel.endswith(".parentage.json")
            or rel.endswith(".physical_realization_seed.json")
        ):
            authoritative += size
            classified.append(("AUTHORITATIVE",rel,size))
        elif (
            rel.startswith("lits_a_r5/")
            or rel.startswith("wvs7_r5/")
            or rel=="wvs7_projection_structural_input.json"
            or rel.startswith("p4_optional_cache/")
            or rel.startswith("p5_transient_compiler_state/")
        ):
            transformed += size
            classified.append(("TRANSFORMED_REGENERABLE",rel,size))
        else:
            raise BackendStop(
                "durable candidate state lacks frozen telemetry classification",
                {"path":rel,"metric_scope":"DURABLE_STATE_SIZE"},
            )
    return authoritative,transformed,classified


def _moving_parts_manifest(ctx,state):
    key=(ctx.stage.source,ctx.stage.candidate)
    session=_SESSIONS.get(key)
    parts=[]
    if session is not None:
        parts.extend(["LIVE_BINDING","GOVERNED_PROJECTION"])
        if session[2] is not None:
            parts.append("RUNTIME_AUTHORITY_SET")
    if ctx.stage.candidate=="A":
        root=Path(ctx.roots.durable)/("lits_a_r5" if ctx.stage.source=="LITS_I" else "wvs7_r5")
        if root.is_dir():
            parts.append("PERSISTENT_R5_CARRIER")
    if ctx.stage.candidate=="C":
        receipt=state.get("candidate_c_binding_receipt") or {}
        inv=receipt.get("accelerator_inventory") or receipt.get("current_f02_accelerator_inventory") or ()
        for item in inv:
            parts.append("ACCELERATOR::"+str(item))
    if _candidate_state_guard_path(ctx).is_file():
        parts.append("CANDIDATE_STATE_GUARD")
    return tuple(sorted(set(parts)))


def _t4_seed_scratch_baseline(ctx,state):
    scratch=Path(ctx.roots.scratch)
    tracker=state.setdefault("_t4_scratch_tracker",{})
    if scratch.exists():
        for q in sorted(x for x in scratch.rglob("*") if x.is_file()):
            oid=_t4_object_id(q)
            size=q.stat().st_size
            tracker[oid]=size
            state.setdefault("_t4_scratch_events",[]).append({
                "operation":"SIZE","object_id":oid,"current_size_bytes":size,
                "cost_class":"C2",
                "evidence_ref":"FIABC_T4_STAGE_START_SCRATCH_BASELINE",
                "lifecycle_action_id":None,
            })


def _t4_assert_scratch_coverage(ctx,state):
    scratch=Path(ctx.roots.scratch)
    tracker=state.setdefault("_t4_scratch_tracker",{})
    actual={}
    if scratch.exists():
        for q in sorted(x for x in scratch.rglob("*") if x.is_file()):
            actual[_t4_object_id(q)] = q.stat().st_size
    if actual != tracker:
        raise BackendStop(
            "scratch mutation stream is incomplete",
            {"actual":actual,"tracked":dict(tracker)},
        )


def _t4_metric_event(state, *, name, start_ns=None, stop_ns=None, value=None, unit=None,
                     cost_class="C2", evidence_ref=None, lifecycle_action_id=None):
    event = {
        "name": name,
        "cost_class": cost_class,
        "evidence_ref": evidence_ref or "FIABC_T4_LIVE_BACKEND_OBSERVATION",
        "lifecycle_action_id": lifecycle_action_id,
    }
    if start_ns is not None or stop_ns is not None:
        if not isinstance(start_ns, int) or not isinstance(stop_ns, int) or stop_ns < start_ns:
            raise BackendStop("invalid T4 monotonic metric interval", {"metric": name})
        event.update({"kind": "DURATION", "start_ns": start_ns, "stop_ns": stop_ns})
    else:
        if value is None:
            raise BackendStop("T4 observed metric requires value or duration", {"metric": name})
        event.update({"kind": "OBSERVED_VALUE", "value": value, "unit": unit})
    state.setdefault("_t4_metric_events", []).append(event)
    return event


def _t4_lifecycle_event(state, event):
    if state.get("_t4_lifecycle_event") is not None:
        raise BackendStop("one stage attempted to emit multiple lifecycle actions")
    state["_t4_lifecycle_event"] = dict(event)


def _session_object_id(source, candidate, session):
    if session is None:
        return None
    binding = session[0]
    receipt = binding.receipt()
    return "SESSION::" + _h({
        "source": source,
        "candidate": candidate,
        "binding_identity": receipt.get("binding_identity"),
        "release_ref": receipt.get("release_ref"),
    })


def _candidate_state_guard_path(ctx):
    return ctx.roots.durable / "fiabc_t4_candidate_state_guard.json"


def _write_candidate_state_guard(ctx, state):
    guard = {
        "schema": "FIABC_T4_CANDIDATE_STATE_GUARD@1.0.0",
        "source": ctx.stage.source,
        "candidate": ctx.stage.candidate,
        "source_sha256": ctx.source_sha256,
        "binding_identity": state.get("bindings", {}).get("candidate_provider_identity"),
        "terminal_identity": state.get("outputs", {}).get("exact_output_identity"),
    }
    return _atomic(_candidate_state_guard_path(ctx), guard)


def _children_cpu_snapshot():
    usage=resource.getrusage(resource.RUSAGE_CHILDREN)
    return {
        "cpu_user_ns":max(0,int(usage.ru_utime*1_000_000_000)),
        "cpu_system_ns":max(0,int(usage.ru_stime*1_000_000_000)),
    }


def _child_process_event(*, stage, pid, before, after, wall_start_ns, wall_stop_ns,
                         peak_rss_bytes, label):
    user=max(0,int(after["cpu_user_ns"])-int(before["cpu_user_ns"]))
    system=max(0,int(after["cpu_system_ns"])-int(before["cpu_system_ns"]))
    if wall_stop_ns < wall_start_ns:
        raise BackendStop("child process wall clock moved backwards")
    return {
        "process_token":f"{label}::pid={pid}",
        "pid":int(pid),"phase_id":stage.stage_id,
        "cpu_user_start_ns":0,"cpu_user_stop_ns":user,
        "cpu_system_start_ns":0,"cpu_system_stop_ns":system,
        "wall_start_ns":int(wall_start_ns),"wall_stop_ns":int(wall_stop_ns),
        "peak_rss_bytes":max(0,int(peak_rss_bytes)),
        "evidence_ref":stage.address+"::"+label,
        "label":label,
    }


def _measure(ctx, state, fn, metric: str | None = None, *, cost_class="C2",
             lifecycle_action_id=None):
    start_ns = time.perf_counter_ns()
    out = fn()
    stop_ns = time.perf_counter_ns()
    if metric:
        _t4_metric_event(
            state,
            name=metric,
            start_ns=start_ns,
            stop_ns=stop_ns,
            cost_class=cost_class,
            evidence_ref=ctx.stage.address,
            lifecycle_action_id=lifecycle_action_id,
        )
    return out, stop_ns - start_ns


def _decode(ctx, state, reread: bool = False):
    if ctx.source_path is None:
        raise BackendStop("source-access stage lacks driver-supplied source_path")
    if _sha(ctx.source_path) != EXPECTED_SOURCE[ctx.stage.source]:
        raise SourceAuthorityStop("source SHA drift immediately before decode")
    from rawlsing_next.pre553_physical_decoder import decode_dta, decode_sav
    sa = state["source_access"]
    observed_bytes = ctx.source_path.stat().st_size
    sa["open"] += 1; sa["decode"] += 1; sa["reread"] += int(reread); sa["bytes"] += observed_bytes
    state.setdefault("_t4_source_events", []).extend(["open", "decode"] + (["reread"] if reread else []))
    _t4_io_event(
        state, operation="READ", byte_count=observed_bytes,
        object_id="CANONICAL_SOURCE::"+ctx.source_sha256, rewrite_of=None,
        cost_class="C1", evidence_ref=ctx.stage.address+"::FULL_SOURCE_DECODE",
        lifecycle_action_id=_t4_current_lifecycle_action_id(state),
    )
    inc = decode_dta(ctx.source_path, encoding="latin1") if ctx.stage.source == "LITS_I" else decode_sav(ctx.source_path)
    if inc.source_sha256 != ctx.source_sha256:
        raise SourceAuthorityStop("decoder source identity drift")
    return inc


def _public(obj) -> Mapping[str, Any]:
    raw = obj.as_dict() if hasattr(obj, "as_dict") else obj
    if not isinstance(raw, Mapping):
        raise SourceAuthorityStop("public object is not serializable")
    doc = {k: raw[k] for k in PUBLIC_KEYS if k in raw}
    if frozenset(doc) != PUBLIC_KEYS:
        raise SourceAuthorityStop("canonical public-object preimage incomplete")
    return doc


def _projection_fields(p) -> Mapping[str, Any]:
    return {f.name: getattr(p, f.name) for f in dataclasses.fields(p)}


def _lits_projection(ctx, services, state, incidence):
    repo = _repo(services)
    root = ctx.work_root / "_be1_lits_projection"
    builder = _deploy(repo, root, LITS_BANKED_COMMIT, LITS_BUILDER, "c51b56779ab9d79126619b7733d41f5253c8150f")
    mod = _load(builder, "_be1_lits_banked")
    accepted = builder.parent.parent / "AS2A_LITS1_SHARED_CERTIFICATION_20260827"
    accepted.mkdir(parents=True, exist_ok=True)
    ledger = accepted / Path(LITS_LEDGER).name
    package = accepted / Path(LITS_PACKAGE).name
    _write_bytes_tracked(ledger, _git_bytes(repo, LITS_BANKED_COMMIT, LITS_LEDGER), cost_class="C1")
    _write_bytes_tracked(package, _git_bytes(repo, LITS_BANKED_COMMIT, LITS_PACKAGE), cost_class="C1")
    old_l, old_p = mod.LEDGER, mod.PACKAGE
    mod.LEDGER, mod.PACKAGE = ledger, package
    try:
        pkg, rows, slots = mod.read_banked_authority()
        if incidence is None:
            incidence=types.SimpleNamespace(
                variables=tuple(types.SimpleNamespace(ordinal=int(row["slot"]),name=row["var"]) for row in rows)
            )
        projection, pctx = mod.build_projection(incidence, pkg, rows, slots)
    finally:
        mod.LEDGER, mod.PACKAGE = old_l, old_p
    if projection.cache_identity != LITS_PROJECTION:
        raise SourceAuthorityStop("accepted LiTS projection identity drift")
    return projection, pctx, mod



def _support_module(ctx, services):
    path=_repo(services)/R6S_LITS_SUPPORT
    if not path.is_file():
        raise CourtAuthorityStop("R6S LiTS runtime support absent",{"path":R6S_LITS_SUPPORT})
    return _load(path,"_ee_p2r6s_lits_current_runtime")

def _lits_runtime(ctx, services, projection):
    support=_support_module(ctx,services)
    package=support.materialize_runtime_package()
    if package["runtime_catalog_identity"]!=R6O_RUNTIME_CATALOG:
        raise SourceAuthorityStop("adopted R6O runtime catalog identity drift")
    if package["active_binding"]!=R6O_ACTIVE_BINDING or package["runtime_release"]!=R6O_RUNTIME_RELEASE:
        raise SourceAuthorityStop("adopted R6O binding/release drift")
    if package["candidate_count"]!=50 or package["query_role_executions"]!=77:
        raise SourceAuthorityStop("adopted LiTS 50/77 runtime workload drift")
    return {
        "authorities":package["authority_documents"],
        "predicates":package["predicate_documents"],
        "queries":package["query_documents"],
        "discoveries":package["discovery_authority_documents"],
        "cross_schema_logical_candidate_bindings":package["cross_schema_logical_candidate_bindings"],
        "runtime_authority_set":support.materialize_runtime_authority_set(),
    }

def _wvs_docs(ctx, services):
    path=_repo(services)/R6S_RUNTIME_PACKAGE
    if not path.is_file():
        raise CourtAuthorityStop("R6S packaged WVS runtime authority absent")
    package=json.loads(path.read_text(encoding="utf-8"))
    if (
        package.get("lock2")!=WVS_LOCK2
        or package.get("replay")!=WVS_LOCK2_REPLAY
        or package.get("discovery_authority_hash")!=WVS_DISCOVERY_AUTHORITY
    ):
        raise SourceAuthorityStop("R6S WVS Lock2/runtime package identity drift")
    if package.get("counts")!={"authorities":6,"predicates":11,"queries":3,"discovery_authorities":1,"candidates":46}:
        raise SourceAuthorityStop("R6S WVS runtime-catalog cardinality drift")
    return {
        "authorities":package["authority_documents"],
        "predicates":package["predicate_documents"],
        "queries":package["query_documents"],
        "discoveries":package["discovery_authority_documents"],
    }

def _wvs_materializer(ctx, services):
    path=_repo(services)/R6S_MATERIALIZER
    if not path.is_file():
        raise CourtAuthorityStop("R6S WVS projection materializer absent")
    return _load(path,"_ee_p2r6s_wvs_projection_materializer")

def _wvs_structural_path(ctx):
    return ctx.roots.durable/"wvs7_projection_structural_input.json"


def _wvs_parentage_path(ctx):
    return ctx.roots.durable/"wvs7_projection_structural_input.parentage.json"


def _root_lineage_identity(ctx):
    return _h({
        "backend_contract": BACKEND_CONTRACT,
        "source": ctx.stage.source,
        "candidate": ctx.stage.candidate,
        "durable_root": str(ctx.roots.durable.resolve()),
    })


def _wvs_reader_config():
    return {
        "reader": "pyreadstat",
        "reader_version": FROZEN_PYREADSTAT_VERSION,
        "apply_value_formats": False,
        "user_missing": True,
        "metadata_read": {"metadataonly": True},
        "country_read": {"usecols": ["B_COUNTRY"]},
        "compatibility_mode": None,
    }


def _wvs_parentage_material(ctx):
    producer = {
        "identity": "WVS7_PROJECTION_STRUCTURAL_MATERIALIZER",
        "code_blob": WVS_MATERIALIZER_BLOB,
        "version": "EE_P2R6S_WVS7_PROJECTION_STRUCTURAL_INPUT@1.0.0",
    }
    scope = {
        "source": "WVS7",
        "derivative_scope": "PROJECTION_STRUCTURAL_PREIMAGE",
        "projection_identity": R6S_WVS_PROJECTION,
    }
    currentness = {
        "owner_commit": OWNER_COMMIT,
        "materializer_blob": WVS_MATERIALIZER_BLOB,
        "projection_identity": R6S_WVS_PROJECTION,
        "lock2": WVS_LOCK2,
    }
    ownership = {
        "source": "WVS7",
        "candidate": ctx.stage.candidate,
        "root_lineage_identity": _root_lineage_identity(ctx),
        "process_lineage": BACKEND_CONTRACT,
    }
    return producer, _wvs_reader_config(), scope, currentness, ownership


def _wvs_projection(ctx, services, state):
    from rawlsing_next.fiabc_derivative_parentage import (
        ParentageError,
        mint_source_verification_receipt,
        mint_derivative_parentage_receipt,
        mint_parentage_bundle,
        verify_parentage_bundle,
        wvs_structural_metadata,
    )

    m=_wvs_materializer(ctx,services)
    structural=_wvs_structural_path(ctx)
    parentage=_wvs_parentage_path(ctx)
    producer,reader_config,scope,currentness,ownership=_wvs_parentage_material(ctx)
    source_operation="VERIFY_CANONICAL_WVS7_RAW_SHA_AND_EXTRACT_STRUCTURAL_INPUT"
    derivation_operation="MATERIALIZE_WVS7_STRUCTURAL_PREIMAGE_FROM_CANONICAL_SAV"

    try:
        if ctx.source_path is not None:
            runtime_version=importlib.metadata.version("pyreadstat")
            if runtime_version!=FROZEN_PYREADSTAT_VERSION:
                raise SourceAuthorityStop(
                    "WVS7 parentage reader version drift",
                    {"expected":FROZEN_PYREADSTAT_VERSION,"got":runtime_version},
                )
            doc=m.projection_structural_input_from_wvs_sav(ctx.source_path)
            derivative_identity=doc.get("structural_input_identity")
            source_receipt=mint_source_verification_receipt(
                source_id="WVS7",
                canonical_source_sha256=WVS_SHA,
                observed_source_sha256=WVS_SHA,
                producer=producer,
                operation=source_operation,
                reader_config=reader_config,
                scope_determinants=scope,
                currentness_determinants=currentness,
                ownership=ownership,
            )
            derivative_receipt=mint_derivative_parentage_receipt(
                source_receipt=source_receipt,
                derivative_class="WVS7_STRUCTURAL_PREIMAGE",
                derivative_identity=derivative_identity,
                derivative_hash=derivative_identity,
                derivative_metadata=wvs_structural_metadata(doc),
                producer=producer,
                derivation_operation=derivation_operation,
                reader_config=reader_config,
                scope_determinants=scope,
                currentness_determinants=currentness,
                ownership=ownership,
            )
            bundle=mint_parentage_bundle(
                source_receipt=source_receipt,
                derivative_receipt=derivative_receipt,
            )
            _atomic(structural,doc)
            _atomic(parentage,bundle)
            state.setdefault("derivative_parentage",{})["WVS7_STRUCTURAL_PREIMAGE"]={
                "bundle_identity":bundle["bundle_identity"],
                "source_receipt_identity":source_receipt["receipt_identity"],
                "derivative_receipt_identity":derivative_receipt["receipt_identity"],
                "structural_input_identity":derivative_identity,
            }
        elif structural.is_file():
            if not parentage.is_file():
                raise SourceAuthorityStop(
                    "source-free WVS structural preimage lacks external parentage receipt",
                    {"required":str(parentage),"source_reopen":"FORBIDDEN"},
                )
            doc=json.loads(structural.read_text(encoding="utf-8"))
            bundle=json.loads(parentage.read_text(encoding="utf-8"))
            frozen=(state.get("derivative_parentage") or {}).get("WVS7_STRUCTURAL_PREIMAGE")
            if not isinstance(frozen,Mapping):
                raise SourceAuthorityStop(
                    "source-free WVS structural preimage lacks prior governed parentage freeze",
                    {"source_reopen":"FORBIDDEN"},
                )
            if (
                bundle.get("bundle_identity")!=frozen.get("bundle_identity")
                or doc.get("structural_input_identity")!=frozen.get("structural_input_identity")
            ):
                raise SourceAuthorityStop("WVS structural preimage/parentage freeze identity drift")
            verify_parentage_bundle(
                bundle,
                expected_source_id="WVS7",
                expected_source_sha256=WVS_SHA,
                expected_source_receipt_identity=frozen.get("source_receipt_identity"),
                expected_source_operation=source_operation,
                expected_derivative_class="WVS7_STRUCTURAL_PREIMAGE",
                expected_derivative_identity=doc.get("structural_input_identity"),
                expected_derivative_receipt_identity=frozen.get("derivative_receipt_identity"),
                expected_derivative_hash=doc.get("structural_input_identity"),
                expected_derivative_metadata=wvs_structural_metadata(doc),
                expected_producer=producer,
                expected_derivation_operation=derivation_operation,
                expected_reader_config=reader_config,
                expected_scope_determinants=scope,
                expected_currentness_determinants=currentness,
                expected_ownership=ownership,
                expected_source_producer=producer,
                expected_source_reader_config=reader_config,
                expected_source_scope_determinants=scope,
                expected_source_currentness_determinants=currentness,
                expected_source_ownership=ownership,
            )
        else:
            raise BackendStop("source-free WVS stage lacks deterministic projection structural preimage",
                              {"required":str(structural),"source_reopen":"FORBIDDEN"})
        projection=m.materialize_from_structural_input(doc)
    except ParentageError as exc:
        raise SourceAuthorityStop("WVS structural preimage parentage failure",{"error":str(exc)}) from exc

    if projection.projection_identity_ref.content_hash!=R6S_WVS_PROJECTION:
        raise SourceAuthorityStop("R6S WVS projection identity drift")
    if projection.coordinate_slots[0].source_semantic_authority_ref.authority_content_hash!=R6S_WVS_COORDINATE_AUTHORITY:
        raise SourceAuthorityStop("R6S WVS coordinate authority drift")
    return projection


def _assert_r5_canonical_source_root(reader, source_name, projection):
    if projection.expected_source_sha256 != EXPECTED_SOURCE[source_name]:
        raise SourceAuthorityStop("R5 projection source SHA differs from the canonical source contract")
    expected = {
        "kind": "SOURCE_ARTIFACT",
        "object_id": projection.source_artifact_id,
        "content_hash": projection.expected_source_sha256,
    }
    if not isinstance(expected["object_id"], str) or not expected["object_id"]:
        raise SourceAuthorityStop("R5 projection omits the governed source artifact object_id")
    release_identity = getattr(reader, "release_identity", {})
    observed = release_identity.get("source_artifact_ref")
    if observed != expected:
        raise SourceAuthorityStop(
            "preserved/prebuilt R5 derivative does not close to canonical source root",
            {"source": source_name, "expected_source_artifact_ref": expected, "observed_source_artifact_ref": observed},
        )


def _compose_current_candidate_c(ctx, services, state, runtime, projection, incidence, runtime_authority):
    if incidence is None:
        raise BackendStop(f"{ctx.stage.source}-C exact source incidence required by current six-cell contract")
    services.load_exact_owner_module("C")
    from rawlsing_next.pre553_candidate_c_production_binding import (
        candidate_c_builder_identity,
        candidate_c_repository_builder_for_source,
    )
    from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, bind_repository_builder

    source_name = ctx.stage.source
    catalog = RuntimeObjectCatalog.from_documents(
        authority_documents=runtime["authorities"],
        predicate_documents=runtime["predicates"],
        query_documents=runtime["queries"],
        discovery_authority_documents=runtime["discoveries"],
    )
    builder = candidate_c_repository_builder_for_source(source_name)
    identity = dict(candidate_c_builder_identity(source_name))
    if source_name == "LITS_I":
        identity.update({
            "runtime_catalog": R6O_RUNTIME_CATALOG,
            "active_binding": R6O_ACTIVE_BINDING,
            "runtime_release": R6O_RUNTIME_RELEASE,
            "current_f02_accelerator_inventory": [],
        })
        builder_kwargs = {"source": incidence, "projection": projection, "accelerator_inventory": ()}
    else:
        identity.update({"lock2": WVS_LOCK2, "current_wvs_accelerator_inventory": []})
        builder_kwargs = {"source": incidence, "projection": projection}

    receipt_box = {}
    def current_c_builder(**kwargs):
        built = builder(**kwargs)
        if not isinstance(built, tuple) or len(built) < 3 or not isinstance(built[2], Mapping):
            raise BackendStop("Candidate-C successor builder omitted physical/provenance receipt")
        receipt_box["candidate_c"] = dict(built[2])
        return built

    binding = bind_repository_builder(
        repository_builder=current_c_builder,
        builder_kwargs=builder_kwargs,
        builder_identity=identity,
        runtime_catalog=catalog,
    )
    state["candidate_c_binding_receipt"] = receipt_box["candidate_c"]
    return binding, projection, runtime_authority


def _assert_lits_common_c11_identity(projection, release):
    """Pin full current LiTS materialization to the accepted C11/replay pair."""
    if projection.cache_identity != LITS_PROJECTION:
        return {
            "schema": "FIABC_LITS_COMMON_C11_IDENTITY_GATE@1.0.0",
            "enforced": False,
            "reason": "SOURCE_FREE_BOUNDED_FIXTURE_PROJECTION",
            "projection_cache_identity": projection.cache_identity,
        }
    if projection.expected_source_sha256 != LITS_SHA:
        raise SourceAuthorityStop("accepted LiTS C11 identity gate received a different source SHA")
    from rawlsing_next.fiabc_lits_i_representation_authority import (
        ACCEPTED_C11_RELEASE_IDENTITY,
        ACCEPTED_C11_REPLAY_IDENTITY,
    )
    replay_manifest = getattr(release, "replay_manifest", None)
    replay_ref = getattr(replay_manifest, "ref", None)
    observed_release = getattr(release, "semantic_release_hash", None)
    observed_replay = getattr(replay_ref, "content_hash", None)
    if (
        observed_release != ACCEPTED_C11_RELEASE_IDENTITY
        or observed_replay != ACCEPTED_C11_REPLAY_IDENTITY
    ):
        raise SourceAuthorityStop(
            "LiTS accepted base C11/replay identity drift",
            {
                "expected_c11_release": ACCEPTED_C11_RELEASE_IDENTITY,
                "observed_c11_release": observed_release,
                "expected_c11_replay": ACCEPTED_C11_REPLAY_IDENTITY,
                "observed_c11_replay": observed_replay,
            },
        )
    return {
        "schema": "FIABC_LITS_COMMON_C11_IDENTITY_GATE@1.0.0",
        "enforced": True,
        "projection_cache_identity": projection.cache_identity,
        "source_sha256": projection.expected_source_sha256,
        "accepted_c11_release_identity": ACCEPTED_C11_RELEASE_IDENTITY,
        "observed_c11_release_identity": observed_release,
        "accepted_c11_replay_identity": ACCEPTED_C11_REPLAY_IDENTITY,
        "observed_c11_replay_identity": observed_replay,
        "candidate_semantic_branching": False,
    }


def _lits_a_current_paths(ctx):
    return (
        ctx.roots.durable/"lits_a_r5",
        ctx.roots.durable/"lits_a_r5.parentage.json",
        ctx.roots.durable/"lits_a_r5.physical_realization_seed.json",
    )


def _lits_a_parentage_material(ctx, physical_root_id=None):
    producer={
        "identity":"R5CompactLongShardedBuilder",
        "code_blob":LITS_R5_BUILDER_BLOB,
        "version":"R5_LONG_SHARDED_TYPED_INCIDENCE_V1",
        "owner_commit":OWNER_COMMIT,
        "consumer_adapter_blob":LITS_A_ADAPTER_BLOB,
    }
    reader_config={
        "reader":"pyreadstat",
        "reader_version":FROZEN_PYREADSTAT_VERSION,
        "user_missing":True,
        "apply_value_formats":False,
        "encoding":"latin1",
        "authority_status":"COMPATIBILITY_EXECUTION_ONLY__NOT_SOURCE_TEXT_ENCODING_AUTHORITY",
    }
    scope={
        "source":"LITS_I",
        "derivative_scope":"PRESERVED_R5_PHYSICAL_SOURCE_CARRIER",
        "projection_identity":LITS_PROJECTION,
        "runtime_catalog":R6O_RUNTIME_CATALOG,
    }
    currentness={
        "owner_commit":OWNER_COMMIT,
        "candidate_owner_blob":LITS_A_ADAPTER_BLOB,
        "runtime_catalog":R6O_RUNTIME_CATALOG,
        "active_binding":R6O_ACTIVE_BINDING,
        "runtime_release":R6O_RUNTIME_RELEASE,
    }
    source_ownership={
        "source":"LITS_I",
        "candidate":"A",
        "current_court_stage":"S01_CANDIDATE_PREPARATION_BUILD",
        "root_lineage_identity":_root_lineage_identity(ctx),
    }
    derivative_ownership=dict(source_ownership)
    if physical_root_id is not None:
        derivative_ownership["physical_root_id"]=physical_root_id
    return producer,reader_config,scope,currentness,source_ownership,derivative_ownership


def _lits_a_inventory(reader, root_path):
    from rawlsing_next.fiabc_derivative_parentage import ParentageError
    inventory=reader.root.get("member_inventory")
    if not isinstance(inventory,Mapping):
        raise ParentageError("LiTS R5 member inventory missing")
    inventory_path=root_path/str(inventory.get("path",""))
    if (
        not inventory_path.is_file()
        or inventory_path.stat().st_size!=inventory.get("byte_length")
        or _sha(inventory_path)!=inventory.get("sha256")
    ):
        raise ParentageError("LiTS R5 member inventory identity mismatch")
    return inventory


def _lits_a_verify_current_r5(ctx, services, state, projection):
    _ensure_r5(ctx, services)
    from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedReader
    from rawlsing_next.fiabc_derivative_parentage import (
        ParentageError, assert_r5_root_parent, r5_root_metadata, verify_parentage_bundle,
    )
    root_path,parentage_path,seed_path=_lits_a_current_paths(ctx)
    if not root_path.is_dir() or not parentage_path.is_file() or not seed_path.is_file():
        raise SourceAuthorityStop(
            "current LiTS-A S01 realization or contemporaneous parentage absent",
            {"root":str(root_path),"parentage":str(parentage_path),"physical_seed":str(seed_path)},
        )
    def _r5_fault(phase,detail):
        if phase=="after_verified_read":
            _t4_note_file_read(Path(detail["path"]),int(detail["length"]),cost_class="C2",role="R5_VERIFIED_READ")
    reader=R5CompactLongShardedReader(root_path,fault_hook=_r5_fault)
    _t4_note_file_read(root_path/"root.json",(root_path/"root.json").stat().st_size,cost_class="C2",role="R5_ROOT_READ")
    try:
        _assert_r5_canonical_source_root(reader, "LITS_I", projection)
        assert_r5_root_parent(reader.root,expected_source_sha256=LITS_SHA)
        inventory=_lits_a_inventory(reader,root_path)
        bundle=json.loads(parentage_path.read_text(encoding="utf-8"))
        seed=json.loads(seed_path.read_text(encoding="utf-8"))
        physical_root_id=reader.root.get("physical_root_id")
        producer,reader_config,scope,currentness,source_ownership,ownership = _lits_a_parentage_material(
            ctx,physical_root_id
        )
        derivative_receipt=(bundle.get("derivative_receipt") or {})
        source_receipt=(bundle.get("source_receipt") or {})
        verify_parentage_bundle(
            bundle,
            expected_source_id="LITS_I",
            expected_source_sha256=LITS_SHA,
            expected_source_receipt_identity=source_receipt.get("receipt_identity"),
            expected_source_operation="VERIFY_CANONICAL_LITS_I_RAW_SHA_FOR_CURRENT_S01_BUILD",
            expected_source_producer=producer,
            expected_source_reader_config=reader_config,
            expected_source_scope_determinants=scope,
            expected_source_currentness_determinants=currentness,
            expected_source_ownership=source_ownership,
            expected_derivative_class="LITS_A_PRESERVED_R5_CARRIER",
            expected_derivative_identity=physical_root_id,
            expected_derivative_receipt_identity=derivative_receipt.get("receipt_identity"),
            expected_derivative_hash=physical_root_id,
            expected_derivative_metadata=r5_root_metadata(reader.root),
            expected_producer=producer,
            expected_derivation_operation="BUILD_LITS_A_R5_FROM_CANONICAL_PHYSICAL_INCIDENCE",
            expected_reader_config=reader_config,
            expected_scope_determinants=scope,
            expected_currentness_determinants=currentness,
            expected_ownership=ownership,
        )
        unsigned_seed={k:v for k,v in seed.items() if k!="seed_identity"}
        if _h(unsigned_seed)!=seed.get("seed_identity"):
            raise ParentageError("LiTS-A physical realization seed identity mismatch")
        if (
            seed.get("source")!="LITS_I"
            or seed.get("candidate")!="A"
            or seed.get("physical_root_id")!=physical_root_id
            or seed.get("parentage_bundle_identity")!=bundle.get("bundle_identity")
            or seed.get("derivative_receipt_identity")!=derivative_receipt.get("receipt_identity")
            or seed.get("r35_i03_status")!="PENDING__MUST_USE_SAME_S01_STATE__NO_SECOND_BUILD"
        ):
            raise ParentageError("LiTS-A current S01 physical realization seed drift")
        state.setdefault("derivative_parentage",{})["LITS_A_R5"]={
            "bundle_identity":bundle.get("bundle_identity"),
            "source_receipt_identity":source_receipt.get("receipt_identity"),
            "derivative_receipt_identity":derivative_receipt.get("receipt_identity"),
            "physical_root_id":physical_root_id,
            "logical_stream_digest":reader.root.get("logical_stream_digest"),
            "member_inventory_sha256":inventory.get("sha256"),
        }
        state["lits_a_physical_realization_seed"]={
            "path":str(seed_path),
            "seed_identity":seed.get("seed_identity"),
            "r35_i03_status":seed.get("r35_i03_status"),
        }
    except (ParentageError,json.JSONDecodeError) as exc:
        raise SourceAuthorityStop("current LiTS-A R5 parentage/physical-state failure",{"error":str(exc)}) from exc
    return reader


def _lits_a_build_current_s01(ctx, services, state, incidence, projection):
    from rawlsing_next.fiabc_derivative_parentage import (
        ParentageError, assert_r5_root_parent, mint_derivative_parentage_receipt,
        mint_parentage_bundle, mint_source_verification_receipt, r5_root_metadata,
    )
    if incidence is None:
        raise BackendStop("LiTS-A current measured S01 requires canonical source incidence")
    observed=getattr(incidence,"source_sha256",None)
    if observed!=LITS_SHA:
        raise SourceAuthorityStop("LiTS-A S01 incidence source identity drift")
    root_path,parentage_path,seed_path=_lits_a_current_paths(ctx)
    if root_path.exists() or parentage_path.exists() or seed_path.exists():
        raise BackendStop(
            "LiTS-A current measured S01 requires absent candidate-owned target",
            {"no_historical_or_prebuilt_root_reuse":True,"root":str(root_path)},
        )
    _build_r5_from_incidence(ctx,services,state,incidence,projection,root_path)
    from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedReader
    reader=R5CompactLongShardedReader(root_path)
    try:
        assert_r5_root_parent(reader.root,expected_source_sha256=LITS_SHA)
        inventory=_lits_a_inventory(reader,root_path)
        physical_root_id=reader.root.get("physical_root_id")
        producer,reader_config,scope,currentness,source_ownership,ownership = _lits_a_parentage_material(
            ctx,physical_root_id
        )
        source_receipt=mint_source_verification_receipt(
            source_id="LITS_I",
            canonical_source_sha256=LITS_SHA,
            observed_source_sha256=observed,
            producer=producer,
            operation="VERIFY_CANONICAL_LITS_I_RAW_SHA_FOR_CURRENT_S01_BUILD",
            reader_config=reader_config,
            scope_determinants=scope,
            currentness_determinants=currentness,
            ownership=source_ownership,
        )
        derivative_receipt=mint_derivative_parentage_receipt(
            source_receipt=source_receipt,
            derivative_class="LITS_A_PRESERVED_R5_CARRIER",
            derivative_identity=physical_root_id,
            derivative_hash=physical_root_id,
            derivative_metadata=r5_root_metadata(reader.root),
            producer=producer,
            derivation_operation="BUILD_LITS_A_R5_FROM_CANONICAL_PHYSICAL_INCIDENCE",
            reader_config=reader_config,
            scope_determinants=scope,
            currentness_determinants=currentness,
            ownership=ownership,
        )
        bundle=mint_parentage_bundle(
            source_receipt=source_receipt,
            derivative_receipt=derivative_receipt,
        )
        _atomic(parentage_path,bundle)
        seed_body={
            "schema":"FIABC_LITS_A_CURRENT_S01_PHYSICAL_REALIZATION_SEED@1.0.0",
            "source":"LITS_I",
            "candidate":"A",
            "stage":"S01_CANDIDATE_PREPARATION_BUILD",
            "canonical_source_sha256":LITS_SHA,
            "physical_root_id":physical_root_id,
            "logical_stream_digest":reader.root.get("logical_stream_digest"),
            "member_inventory_sha256":inventory.get("sha256"),
            "source_receipt_identity":source_receipt.get("receipt_identity"),
            "derivative_receipt_identity":derivative_receipt.get("receipt_identity"),
            "parentage_bundle_identity":bundle.get("bundle_identity"),
            "r35_i03_status":"PENDING__MUST_USE_SAME_S01_STATE__NO_SECOND_BUILD",
            "physical_equivalence_claimed":False,
            "semantic_parity_claimed":False,
            "performance_admission":"BLOCKED_PENDING_R35_I03_AND_PARITY",
        }
        _atomic(seed_path,{**seed_body,"seed_identity":_h(seed_body)})
    except ParentageError as exc:
        raise SourceAuthorityStop("LiTS-A current S01 parentage mint failed",{"error":str(exc)}) from exc
    # Re-open only the just-built candidate-owned root to verify the exact
    # parentage/seed contract. This does not repeat the build.
    return _lits_a_verify_current_r5(ctx,services,state,projection)


def _compose_lits(ctx, services, state, incidence):
    projection, _, _ = _lits_projection(ctx, services, state, incidence)
    current_projection = projection
    runtime = _lits_runtime(ctx, services, projection)
    from rawlsing_next.fiabc_final_oracle_freeze_producers import _lits_accepted_legacy_projection
    from rawlsing_next.fiabc_lits_common_representation import (
        LiTSRepresentationBridgeError,
        authorized_lits_cell,
        reconstruct_exact_owner_projection,
        representation_authority_receipt,
        validate_lits_projection_scope,
    )
    from rawlsing_next.fiabc_lits_i_representation_authority import (
        ACCEPTED_C11_RELEASE_IDENTITY,
        ACCEPTED_C11_REPLAY_IDENTITY,
    )

    owner_b = services.load_exact_owner_module("B")
    try:
        legacy_owner, adapted_projection = _lits_accepted_legacy_projection(
            projection=projection,
            repo_root=_repo(services),
            neutral_root=ctx.work_root / "_lits_common_representation",
            backend=sys.modules[__name__],
            legacy_module=owner_b,
        )
        b_projection, owner_projection_receipt = reconstruct_exact_owner_projection(
            current_projection=projection,
            adapted_projection=adapted_projection,
            owner_module=legacy_owner,
        )
        validate_lits_projection_scope(projection)
    except Exception as exc:
        if isinstance(exc, (SourceAuthorityStop, BackendStop)):
            raise
        raise SourceAuthorityStop(
            "accepted LiTS representation/projection-owner adaptation failed",
            {"error": f"{type(exc).__name__}: {exc}"},
        ) from exc

    base_cell_iterator = None
    if ctx.stage.candidate == "A":
        # Current final-P2 law: the historical LiTS-A R5 is not a prerequisite.
        # S01 owns exactly one absent-target build; later stages consume that
        # same candidate-owned realization and its contemporaneous R35 parentage.
        if ctx.stage.stage_id == "S01_CANDIDATE_PREPARATION_BUILD":
            reader = _lits_a_build_current_s01(ctx, services, state, incidence, projection)
        else:
            reader = _lits_a_verify_current_r5(ctx, services, state, projection)
        _assert_r5_canonical_source_root(reader, "LITS_I", projection)
        owner_a = services.load_exact_owner_module("A")
        try:
            base_stream, descriptor = owner_a.prepare_r5_exact_physical_cell_stream(
                reader, expected_source_sha256=projection.expected_source_sha256
            )
        except Exception as exc:
            raise SourceAuthorityStop(
                "exact Candidate-A R5 adapter rejected the canonical current carrier",
                {"error": f"{type(exc).__name__}: {exc}"},
            ) from exc
        base_cell_iterator = base_stream.iter_cells
        physical_transport_identity = base_stream.transport_identity
        source_row_count = descriptor.row_count
        if base_stream.source_sha256 != projection.expected_source_sha256 or base_stream.row_count != source_row_count:
            raise SourceAuthorityStop("Candidate-A exact R5 stream geometry/source identity drift")
    elif ctx.stage.candidate == "B":
        if incidence is None:
            raise BackendStop("LiTS-B exact source incidence required by reducer")
        base_cell_iterator = lambda: incidence.iter_cells(batch_size=20_000)
        physical_transport_identity = "CURRENT_EXACT_LITS_PHYSICAL_INCIDENCE"
        source_row_count = incidence.row_count
    elif ctx.stage.candidate == "C":
        if incidence is None:
            raise BackendStop("LiTS-C exact source incidence required by current six-cell contract")
        base_cell_iterator = lambda: incidence.iter_cells(batch_size=20_000)
        physical_transport_identity = "CURRENT_EXACT_LITS_PHYSICAL_INCIDENCE"
        source_row_count = incidence.row_count
        services.load_exact_owner_module("C")
    else:
        raise BackendStop("unknown LiTS candidate")

    transformed_counts = {}

    def authorized_cells():
        for cell in base_cell_iterator():
            try:
                rebound = authorized_lits_cell(
                    source_sha256=projection.expected_source_sha256,
                    cell=cell,
                )
            except LiTSRepresentationBridgeError as exc:
                raise SourceAuthorityStop(
                    "LiTS bounded representation authority rejected a physical cell",
                    {"error": str(exc)},
                ) from exc
            if rebound is not cell:
                kind = "system_missing" if cell.missing_state.value == "SYSTEM_MISSING" else "observed"
                key = f"{cell.variable_ordinal}:{cell.variable_name}:{kind}"
                transformed_counts[key] = transformed_counts.get(key, 0) + 1
            yield rebound

    b_stream = legacy_owner.ExactPhysicalCellStream(
        source_sha256=projection.expected_source_sha256,
        row_count=source_row_count,
        cell_iter_factory=authorized_cells,
        transport_identity=(
            f"FIABC_LITS_AUTHORIZED_EXACT_B_OWNER_STREAM::{physical_transport_identity}::"
            f"{legacy_owner.__name__}"
        ),
    )

    representation_receipt_seed = representation_authority_receipt(
        projection=projection,
        transformed_counts={},
    )
    binding_identity = {
        "candidate": ctx.stage.candidate,
        "semantic_owner_candidate": "B",
        "owner_commit": OWNER_COMMIT,
        "semantic_owner_commit": OWNER_COMMIT,
        "source": "LITS_I",
        "projection": projection.cache_identity,
        "projection_owner_reconstruction": owner_projection_receipt,
        "representation_authority": {
            "authority_ref": representation_receipt_seed["authority_ref"],
            "authority_snapshot": representation_receipt_seed["authority_snapshot"],
            "authority_snapshot_identity": representation_receipt_seed["authority_snapshot_identity"],
        },
        "accepted_base_c11_identity_gate": {
            "projection_cache_identity": LITS_PROJECTION,
            "release_identity": ACCEPTED_C11_RELEASE_IDENTITY,
            "replay_identity": ACCEPTED_C11_REPLAY_IDENTITY,
        },
        "physical_transport_identity": physical_transport_identity,
        "runtime_catalog": R6O_RUNTIME_CATALOG,
        "active_binding": R6O_ACTIVE_BINDING,
        "runtime_release": R6O_RUNTIME_RELEASE,
        "semantic_inference": False,
    }

    common_truth_receipt_box = {}

    def exact_b_common_builder(*, source, projection):
        built = legacy_owner.build_source_backed_c11_repository(
            source, projection, cache=None
        )
        if not isinstance(built, tuple) or len(built) < 2:
            raise BackendStop("exact B owner did not return a C11 repository/release pair")
        common_truth_receipt_box["identity_gate"] = _assert_lits_common_c11_identity(
            current_projection, built[1]
        )
        return built

    repository_builder_override = exact_b_common_builder
    if ctx.stage.candidate == "C":
        from rawlsing_next.pre553_candidate_c_production_binding import (
            candidate_c_builder_identity,
            candidate_c_repository_builder_for_source,
        )

        current_c_builder = candidate_c_repository_builder_for_source("LITS_I")
        c_receipt_box = {}

        def current_candidate_c_common_builder(*, source, projection):
            common_repository, common_release = exact_b_common_builder(
                source=source, projection=projection
            )[:2]
            built = current_c_builder(
                source=incidence,
                projection=current_projection,
                accelerator_inventory=(),
                common_semantic_result=(common_repository, common_release),
            )
            if not isinstance(built, tuple) or len(built) != 3 or not isinstance(built[2], Mapping):
                raise BackendStop("current Candidate-C binding omitted its common-truth receipt")
            c_receipt_box["receipt"] = dict(built[2])
            return built

        repository_builder_override = current_candidate_c_common_builder
        binding_identity.update(candidate_c_builder_identity("LITS_I"))
        binding_identity.update({
            "candidate": "C",
            "semantic_owner_candidate": "B",
            "common_semantic_owner_blob": LITS_B_FACADE_BLOB,
            "candidate_c_policy_receipt": "EMBEDDED_IN_C11_BUILDER_RETURN",
        })
    elif ctx.stage.candidate == "A":
        binding_identity.update({
            "physical_owner": {
                "candidate": "A",
                "commit": OWNER_COMMIT,
                "path": "rawlsing_next/pre553_r5_source_backed_adapter.py",
                "blob": LITS_A_ADAPTER_BLOB,
            },
            "common_semantic_owner_blob": LITS_B_FACADE_BLOB,
        })
    else:
        binding_identity["common_semantic_owner_blob"] = LITS_B_FACADE_BLOB

    binding = services.compose_p2r1_binding(
        authority_documents=runtime["authorities"],
        predicate_documents=runtime["predicates"],
        query_documents=runtime["queries"],
        discovery_authority_documents=runtime["discoveries"],
        projection_fields=_projection_fields(projection),
        candidate=ctx.stage.candidate,
        semantic_owner_candidate="B",
        projection_override=b_projection,
        builder_kwargs={"source": b_stream},
        builder_identity=binding_identity,
        repository_builder_override=repository_builder_override,
    )
    representation_receipt = representation_authority_receipt(
        projection=projection,
        transformed_counts=transformed_counts,
    )
    representation_receipt["receipt_identity"] = _h(representation_receipt)
    state["lits_representation_binding_receipt"] = representation_receipt
    state["lits_common_c11_identity_gate"] = common_truth_receipt_box["identity_gate"]
    if ctx.stage.candidate == "C":
        state["candidate_c_binding_receipt"] = c_receipt_box["receipt"]
    return binding, projection, runtime["runtime_authority_set"]

def _r5_release_identity(source: str, projection):
    from rawlsing_next.pre553_r5_model import R5ReleaseIdentity
    source_sha=projection.expected_source_sha256
    if source_sha != EXPECTED_SOURCE[source]:
        raise SourceAuthorityStop("R5 projection source SHA differs from the canonical source contract")
    source_artifact_ref={
        "kind":"SOURCE_ARTIFACT",
        "object_id":projection.source_artifact_id,
        "content_hash":source_sha,
    }
    if not isinstance(source_artifact_ref["object_id"],str) or not source_artifact_ref["object_id"]:
        raise SourceAuthorityStop("R5 projection omits the governed source artifact object_id")
    material={"source":source,"source_sha256":source_sha,
              "source_artifact_ref":source_artifact_ref,
              "projection_identity":projection.projection_identity_ref.content_hash,
              "candidate":"A","owner_commit":OWNER_COMMIT}
    identity=_h(material)
    return R5ReleaseIdentity(
        release_id=f"EE-P2R6S-{source}-A-{identity[:16]}",
        semantic_release_hash=identity,
        source_artifact_ref=source_artifact_ref,
        source_release_manifest_hash=_h({"source_sha256":source_sha,"release":identity}),
        m01_m18_coverage={},
        decoder_receipt={"source_sha256":source_sha,"contract":"PRE553_FROZEN_PHYSICAL_DECODER"},
        compiler_contract_digest=_h({"carrier":"R5_LONG_SHARDED_TYPED_INCIDENCE_V1","owner_commit":OWNER_COMMIT}),
        c11_authority_digest=projection.projection_authority_ref.authority_content_hash,
    )

def _build_r5_from_incidence(ctx,services,state,incidence,projection,target):
    _ensure_r5(ctx,services)
    from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedBuilder
    from rawlsing_next.pre553_r5_seam import iter_source_native_rows
    if target.exists():
        return

    class InstrumentedR5Builder(R5CompactLongShardedBuilder):
        def _record_write(self,path,role):
            p=Path(path)
            _t4_note_file_write(p,p.stat().st_size,rewrite=False,cost_class="C2")
            if ".work" in p.parts:
                oid="R5_WORK::"+p.relative_to(target).as_posix()
                state.setdefault("_t4_scratch_tracker",{})[oid]=p.stat().st_size
                state.setdefault("_t4_scratch_events",[]).append({
                    "operation":"SIZE","object_id":oid,
                    "current_size_bytes":p.stat().st_size,"cost_class":"C2",
                    "evidence_ref":"FIABC_T4_R5_TRANSIENT_WORK_OBJECT",
                    "lifecycle_action_id":_t4_current_lifecycle_action_id(state),
                })
        def _record_read(self,path,role):
            p=Path(path)
            _t4_note_file_read(p,p.stat().st_size,cost_class="C2",role=role)
        def _flush_run(self,directory,index,records):
            path=super()._flush_run(directory,index,records)
            self._record_write(path,"R5_TEMP_RUN")
            return path
        def _merge_group(self,source_dir,names,target_path):
            for name in names:
                self._record_read(source_dir/name,"R5_TEMP_MERGE_READ")
            super()._merge_group(source_dir,names,target_path)
            self._record_write(target_path,"R5_TEMP_MERGE_WRITE")
        def _make_runs(self,rows,work):
            manifest,telemetry=super()._make_runs(rows,work)
            self._record_write(manifest,"R5_TEMP_MANIFEST")
            return manifest,telemetry
        def _reduce(self,manifest,work):
            source_dir=work/"runs-0000"
            pass_index=0
            max_open=1
            while True:
                self._record_read(manifest,"R5_TEMP_MANIFEST_READ")
                with manifest.open("r",encoding="utf-8") as handle:
                    count=sum(1 for line in handle if line.strip())
                if count <= self.config.merge_fan_in:
                    return manifest,source_dir,pass_index,max_open
                pass_index += 1
                target_dir=work/f"runs-{pass_index:04d}"
                target_dir.mkdir()
                next_manifest=work/f"runs-{pass_index:04d}.txt"
                next_count=0
                with next_manifest.open("w",encoding="utf-8",newline="\n") as out:
                    for group in self._groups(manifest,self.config.merge_fan_in):
                        max_open=max(max_open,len(group))
                        target_path=target_dir/f"run-{next_count:08d}.tmp.gz"
                        self._merge_group(source_dir,group,target_path)
                        out.write(target_path.name+"\n")
                        next_count += 1
                    out.flush(); os.fsync(out.fileno())
                self._record_write(next_manifest,"R5_TEMP_MANIFEST")
                for q in sorted(x for x in source_dir.rglob("*") if x.is_file()):
                    oid="R5_WORK::"+q.relative_to(target).as_posix()
                    state.setdefault("_t4_scratch_tracker",{}).pop(oid,None)
                    state.setdefault("_t4_scratch_events",[]).append({
                        "operation":"REMOVE","object_id":oid,"cost_class":"C2",
                        "evidence_ref":"FIABC_T4_R5_TRANSIENT_WORK_REMOVE",
                        "lifecycle_action_id":_t4_current_lifecycle_action_id(state),
                    })
                shutil.rmtree(source_dir)
                oid="R5_WORK::"+manifest.relative_to(target).as_posix()
                state.setdefault("_t4_scratch_tracker",{}).pop(oid,None)
                state.setdefault("_t4_scratch_events",[]).append({
                    "operation":"REMOVE","object_id":oid,"cost_class":"C2",
                    "evidence_ref":"FIABC_T4_R5_TRANSIENT_WORK_REMOVE",
                    "lifecycle_action_id":_t4_current_lifecycle_action_id(state),
                })
                manifest.unlink()
                source_dir,manifest=target_dir,next_manifest
        def _iter_final(self,manifest,source_dir):
            self._record_read(manifest,"R5_FINAL_MANIFEST_READ")
            names=[line.strip() for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()]
            for name in names:
                self._record_read(source_dir/name,"R5_FINAL_RUN_READ")
            yield from super()._iter_final(manifest,source_dir)

    builder=InstrumentedR5Builder()
    telemetry=builder.build(
        iter_source_native_rows(incidence),
        release_identity=_r5_release_identity(ctx.stage.source,projection),
        target_directory=target,
    )
    for q in sorted(x for x in target.rglob("*") if x.is_file() and ".work" not in x.parts):
        _t4_note_file_write(q,q.stat().st_size,rewrite=False,cost_class="C2")
    tracker=state.setdefault("_t4_scratch_tracker",{})
    for oid in [k for k in tracker if k.startswith("R5_WORK::")]:
        tracker.pop(oid,None)
        state.setdefault("_t4_scratch_events",[]).append({
            "operation":"REMOVE","object_id":oid,"cost_class":"C2",
            "evidence_ref":"FIABC_T4_R5_TRANSIENT_WORK_REMOVE",
            "lifecycle_action_id":_t4_current_lifecycle_action_id(state),
        })
    state["r5_build_telemetry"]=dict(telemetry)

def _compose_wvs(ctx,services,state,incidence=None):
    projection=_wvs_projection(ctx,services,state)
    runtime=_wvs_docs(ctx,services)
    if ctx.stage.candidate=="A":
        _ensure_r5(ctx,services)
        from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedReader
        root=ctx.roots.durable/"wvs7_r5"
        if not root.exists():
            if incidence is None:
                raise BackendStop("WVS-A preserved R5 carrier absent at source-free stage")
            _build_r5_from_incidence(ctx,services,state,incidence,projection,root)
        def _r5_fault(phase,detail):
            if phase=="after_verified_read":
                _t4_note_file_read(Path(detail["path"]),int(detail["length"]),cost_class="C2",role="R5_VERIFIED_READ")
        reader=R5CompactLongShardedReader(root,fault_hook=_r5_fault)
        _t4_note_file_read(root/"root.json",(root/"root.json").stat().st_size,cost_class="C2",role="R5_ROOT_READ")
        _assert_r5_canonical_source_root(reader, "WVS7", projection)
        kwargs={"reader":reader}
    elif ctx.stage.candidate=="B":
        if incidence is None:
            raise BackendStop("WVS-B exact source incidence required by reducer")
        kwargs={"source":incidence}
    elif ctx.stage.candidate=="C":
        return _compose_current_candidate_c(ctx,services,state,runtime,projection,incidence,None)
    else:
        raise BackendStop("unknown WVS7 candidate")
    binding=services.compose_p2r1_binding(
        authority_documents=runtime["authorities"],
        predicate_documents=runtime["predicates"],
        query_documents=runtime["queries"],
        discovery_authority_documents=runtime["discoveries"],
        projection_fields=_projection_fields(projection),
        candidate=ctx.stage.candidate,
        builder_kwargs=kwargs,
        builder_identity={"candidate":ctx.stage.candidate,"owner_commit":OWNER_COMMIT,
                          "source":"WVS7","projection":R6S_WVS_PROJECTION,"lock2":WVS_LOCK2},
    )
    return binding,projection,None

def _ensure_r5(ctx, services):
    import rawlsing_next
    repo = _repo(services)
    blobs = {
        "pre553_r5_codec.py":"72f8f3c03ed065e86fea4e76bb17f8e06c2bf540",
        "pre553_r5_compact_carrier.py":"92e364b31eaf27be1bca2081eff65f6ffb779c3d",
        "pre553_r5_model.py":"62ce608829c3d9c2fb7c999aefe40188637edf80",
        "pre553_r5_seam.py":"cef326ebbc40468428378f7fdbe76e4756179f39",
        "pre553_r5_single_pass_audit69.py":"ffb063b93c86e215604eecb29a9545c7efdff399",
    }
    for name, blob in blobs.items():
        if importlib.util.find_spec("rawlsing_next." + name[:-3]) is not None:
            continue
        p = _deploy(repo, ctx.work_root, OWNER_COMMIT, "rawlsing_next/" + name, blob)
        if str(p.parent) not in rawlsing_next.__path__:
            rawlsing_next.__path__.append(str(p.parent))



def _bind(ctx, services, state, source_allowed: bool):
    key=(ctx.stage.source,ctx.stage.candidate)
    if key in _SESSIONS:
        return _SESSIONS[key]
    if ctx.stage.source=="LITS_I":
        incidence=None
        if ctx.source_path is not None:
            incidence=_decode(ctx,state,reread=state["source_access"]["decode"]>0)
        binding,projection,runtime_authority=_compose_lits(ctx,services,state,incidence)
    elif ctx.stage.source=="WVS7":
        incidence=None
        if ctx.source_path is not None:
            incidence=_decode(ctx,state,reread=state["source_access"]["decode"]>0)
        binding,projection,runtime_authority=_compose_wvs(ctx,services,state,incidence)
    else:
        raise CourtAuthorityStop("unsupported source in production backend")
    session=(binding,projection,runtime_authority)
    _SESSIONS[key]=session
    return session

def _binding_state(state, binding, projection):
    receipt = binding.receipt()
    candidate_c_receipt = state.get("candidate_c_binding_receipt")
    state["bindings"] = {
        "projection_identity": projection.cache_identity,
        "runtime_catalog_identity": receipt["executor_binding"]["runtime_catalog"]["catalog_identity"],
        "candidate_provider_identity": receipt["binding_identity"],
    }
    if candidate_c_receipt is not None:
        state["bindings"]["candidate_c_production_binding"] = candidate_c_receipt
    return receipt


def _i03(binding):
    catalog = binding.executor.runtime_catalog
    q = sorted(catalog.queries,key=lambda x:x.ref.key)[0]
    p = catalog.resolve_predicate_exact(q.condition_predicate_ref)
    result = binding.executor.execute_i03(query_ref=q.ref,predicate_ref=p.ref)
    body = {"query_ref":result.query_ref.as_dict(),"release_refs":[x.as_dict() for x in result.release_refs],
            "facts":[{"ref":x.ref.as_dict(),"state":x.typed_state} for x in result.facts]}
    return body, _h(body)



def _i05(binding, runtime_authority=None):
    refs = binding.executor.runtime_catalog.discovery_authority_refs
    if len(refs) != 1:
        raise SourceAuthorityStop("runtime catalog must expose exactly one DiscoveryAuthority")
    if runtime_authority is None:
        result = binding.executor.execute_i05(discovery_authority_ref=refs[0])
    else:
        from rawlsing_next.pre553_runtime_context import bind_runtime
        with bind_runtime(runtime_authority):
            result = binding.executor.execute_i05(discovery_authority_ref=refs[0])
    from rawlsing_next.pre553_carrier_execution import learned_empirical_execution_receipt
    return result, learned_empirical_execution_receipt(result)

def _evidence(ctx, services) -> Path:
    return _repo(services) / "WORKER_RETURNS/EE-P2X/LOCAL_COURT"


def _rel(path: Path, services) -> str:
    return path.resolve().relative_to(_repo(services).resolve()).as_posix()


def _version(name):
    try:
        import importlib.metadata
        return importlib.metadata.version(name)
    except Exception:
        return "MISSING"


def _host_id():
    return _h({"python":platform.python_version(),"system":platform.system(),"machine":platform.machine(),
               "pyreadstat":_version("pyreadstat"),"pyarrow":_version("pyarrow")})


def _unit(name):
    if name.endswith("_ns") or "wall_ns" in name or "latency_ns" in name: return "ns"
    if "bytes" in name: return "bytes"
    if "throughput" in name: return "candidates/s"
    if "units" in name: return "units"
    return "count"


def _slot(state,name,stopped=False,preserved=False):
    if name in state["metrics"]:
        return state["metrics"][name]
    if stopped:
        return {"state":"NOT_REACHED_AUTHORIZED_STOP","value":None,"unit":_unit(name),
                "reason":"Lawful typed stop occurred before this metric was reached."}
    if preserved:
        return {"state":"NOT_CAPTURED_PRESERVED_STAGE","value":None,"unit":_unit(name),
                "reason":"Repetition-forbidden preserved stage did not capture this metric."}
    raise BackendStop("terminal metric vector incomplete; metric was not actually measured",
                      {"missing_metric":name,"prepopulated_default_forbidden":True})


def _behavior(state,name,stopped):
    if name in state["behaviors"]: return state["behaviors"][name]
    if stopped: return {"state":"NOT_REACHED_AUTHORIZED_STOP","evidence_identity":None}
    if state["candidate"] == "B" and name in {"stale_cache","corrupt_cache"}:
        return {"state":"NOT_APPLICABLE_BY_FROZEN_COURT",
                "evidence_identity":_h({"candidate":"B","behavior":name,"law":"PURE_B_NO_CACHE"})}
    raise BackendStop("terminal behavior vector incomplete", {"behavior":name})


def _fallback(ctx,label,detail=None):
    return _h({"kind":"TYPED_PREOUTCOME_ABSENCE","source":ctx.stage.source,
               "candidate":ctx.stage.candidate,"label":label,"detail":detail})


def _current_failure_authority(ctx, services) -> Mapping[str, Any]:
    """Bind failure metadata to the adopted successor WVS court object.

    The historical EE-P2X expectations file remains an exact Lock1/owner/seam
    source, but its predecessor WVS Lock2 is never consulted here.
    """
    path=_repo(services)/R6S_RUNTIME_PACKAGE
    if not path.is_file():
        raise CourtAuthorityStop(
            "current WVS successor runtime package absent for failure serialization",
            {"path":R6S_RUNTIME_PACKAGE},
        )
    try:
        package=json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise CourtAuthorityStop(
            "current WVS successor runtime package malformed for failure serialization",
            {"path":R6S_RUNTIME_PACKAGE},
        ) from exc
    observed={
        "lock2_hash":package.get("lock2"),
        "lock2_replay_hash":package.get("replay"),
        "discovery_authority":package.get("discovery_authority_hash"),
    }
    expected={
        "lock2_hash":WVS_LOCK2,
        "lock2_replay_hash":WVS_LOCK2_REPLAY,
        "discovery_authority":WVS_DISCOVERY_AUTHORITY,
    }
    if observed!=expected:
        raise CourtAuthorityStop(
            "current WVS successor authority drift during failure serialization",
            {"expected":expected,"observed":observed},
        )
    authority={
        "lock2_hash":observed["lock2_hash"],
        "lock2_replay_hash":observed["lock2_replay_hash"],
    }
    if ctx.stage.source=="WVS7":
        authority["discovery_authority"]=observed["discovery_authority"]
    return authority


def _current_manifest_cell_order() -> tuple[tuple[str, str], ...]:
    raw=os.environ.get("RAWLSING_FIABC_T5_CURRENT_EXECUTION_MANIFEST")
    if not raw:
        raise CourtAuthorityStop("current execution manifest is not bound for cell serialization")
    from rawlsing_next.ee_p2x_darwin_court_driver import load_current_execution_manifest
    machine=load_current_execution_manifest(Path(raw))
    cells=machine.document.get("cells",())
    order=tuple((cell.get("source"),cell.get("candidate")) for cell in cells)
    if not order or any(not isinstance(source,str) or not isinstance(candidate,str) for source,candidate in order):
        raise CourtAuthorityStop("current execution manifest cell order malformed")
    if len(set(order))!=len(order):
        raise CourtAuthorityStop("current execution manifest cell order contains duplicates")
    return order


def _cell(ctx,services,state,stopped):
    exp=json.loads((_repo(services)/"WORKER_RETURNS/EE-P2X/09_LOCAL_COURT_FROZEN_EXPECTATIONS.json").read_text())
    current_authority=_current_failure_authority(ctx,services)
    cell=ctx.stage.source+"/"+ctx.stage.candidate
    order=_current_manifest_cell_order()
    cell_key=(ctx.stage.source,ctx.stage.candidate)
    if cell_key not in order:
        raise CourtAuthorityStop("failure serialization cell absent from current execution manifest",
                                 {"source":ctx.stage.source,"candidate":ctx.stage.candidate})
    preserved=cell in {"LITS_I/A","LITS_I/B"}
    b=state["bindings"]
    projection=b.get("projection_identity") or (LITS_PROJECTION if ctx.stage.source=="LITS_I" else _fallback(ctx,"WVS_PROJECTION"))
    parity={k:state["parity"].get(k,"NOT_RUN_AUTHORIZED_STOP" if stopped else None)
            for k in ("semantic","exactref_identity","replay","integrity_fail_closed","frontier_typed_negative")}
    return {
        "schema":"RAWLSING_EE_P2X_SOURCE_CANDIDATE_RECEIPT@1.0.0",
        "source":ctx.stage.source,"candidate":ctx.stage.candidate,"sequence_index":order.index(cell_key),
        "authority":{"hq_handoff_commit":exp["hq"]["handoff_commit"],
                     "lock1_manifest_blob":exp["lock1"]["manifest_json_git_blob_sha1"],
                     **current_authority},
        "host":{"identity_sha256":_host_id(),"same_physical_host_token":_host_id()},
        "runtime":{"platform":f"{platform.system()} {platform.machine()}","python":platform.python_version(),
                   "pyreadstat":_version("pyreadstat"),"pyarrow":_version("pyarrow"),
                   "darwin_ru_maxrss_unit":"BYTES","same_physical_host_required":True},
        "bindings":{"source_sha256":ctx.source_sha256,"candidate_owner_blob":exp["candidates"][ctx.stage.candidate]["owner_blob"],
                    "execution_seam_blob":exp["execution_seam"]["git_blob_sha1"],
                    "projection_identity":projection,
                    "runtime_catalog_identity":b.get("runtime_catalog_identity") or _fallback(ctx,"RUNTIME_CATALOG"),
                    "candidate_provider_identity":b.get("candidate_provider_identity") or _fallback(ctx,"PROVIDER")},
        "event_ordinals":{"oracle_frozen":state["oracle_frozen"] if state["oracle_frozen"] is not None else 0,
                          "candidate_output_first":state["candidate_output_first"],
                          "parity_complete":state["parity_complete"],
                          "performance_first_admitted":state["performance_first_admitted"]},
        "oracle":{"candidate_neutral":True,"candidate_defined":False,
                  "oracle_identity_sha256":state.get("oracle_identity"),
                  "freeze_receipt_sha256":state.get("upstream_freeze_receipt_sha256")},
        "parity":parity,"performance_admission":("NOT_ADMITTED" if stopped else
            ("ADMITTED_AFTER_INDEPENDENT_ORACLE_MATCH" if state["performance_admitted"] else
             "PENDING__INDEPENDENT_ORACLE_MATCH")),
        "metrics":{n:_slot(state,n,stopped,preserved) for n in METRICS},
        "behaviors":{n:_behavior(state,n,stopped) for n in ("stale_cache","corrupt_cache","interruption_session_recovery")},
        "outputs":{"exact_output_identity":state["outputs"].get("exact_output_identity"),
                   "product_identity":state["outputs"].get("product_identity"),
                   "semantic_identity":state["outputs"].get("semantic_identity"),
                   "replay_identity":state["outputs"].get("replay_identity")},
        "preserved_stage_consumption":[] if cell=="LITS_I/A" else
                                      ["LITS_I_B_CACHELESS_C11"] if cell=="LITS_I/B" else [],
        "disposition":"AUTHORIZED_STOP" if stopped else "QUALIFYING_CELL_COMPLETE",
        "ranking_or_selection":False,
    }


def _write_cell(ctx,services,state,stopped):
    return _atomic(_evidence(ctx,services)/"cells"/f"{ctx.stage.source}__{ctx.stage.candidate}.json",
                   _cell(ctx,services,state,stopped))


def _failure(ctx,services,state,exc):
    if ctx.stage.source=="COURT" and exc.scope=="COURT_UNTIL_RESUME":
        court=_evidence(ctx,services)/"court"/f"{ctx.stage.stage_id}__COMMON_COURT_SCOPE.json"
        failure=_evidence(ctx,services)/"failures"/f"COURT__COMMON__{exc.kind}.json"
        court_obj={"schema":"RAWLSING_EE_P2X_COMMON_COURT_SCOPE_RECEIPT@1.0.0",
                   "source":"COURT","candidate":None,"stage":ctx.stage.address,
                   "kind":exc.kind,"blocking_scope":exc.scope,"candidate_neutral":True,
                   "binding_role":"cell_receipt",
                   "binding_role_law":"FROZEN_VERIFIER_ROLE_NAME__CONTENT_IS_COURT_SCOPE_NOT_CANDIDATE_CELL",
                   "input_identity_hash":ctx.input_identity_hash,
                   "backend_detail":exc.detail,"ranking_or_selection":False}
        _atomic(court,court_obj)
        obj={"schema":"RAWLSING_EE_P2X_FAILURE_STOP_RECEIPT@1.0.0","source":"COURT",
             "candidate":None,"kind":exc.kind,"blocking_scope":exc.scope,
             "disposition":f"EE_P2X_COURT_{ctx.stage.stage_id}__{exc.kind}",
             "evidence_paths":[_rel(court,services),_rel(failure,services)],
             "later_lawful_cells_suppressed":False,"synthetic_fallback_used":False,
             "backend_detail":exc.detail,"ranking_or_selection":False}
        _atomic(failure,obj)
        return {"terminal_disposition":exc.terminal,
                "receipt":{"error":str(exc),"detail":exc.detail,"evidence_artifacts":
                           {"cell_receipt":_rel(court,services),"failure_receipt":_rel(failure,services)}},
                "output_artifacts":{"cell_receipt":str(court),"failure_receipt":str(failure)},
                "verifier_complete":True}
    _save(ctx,state)
    cell=_write_cell(ctx,services,state,True)
    candidate=None if exc.scope in {"SOURCE_ONLY","COURT_UNTIL_RESUME"} else ctx.stage.candidate
    path=_evidence(ctx,services)/"failures"/f"{ctx.stage.source}__{candidate or 'COMMON'}__{exc.kind}.json"
    obj={"schema":"RAWLSING_EE_P2X_FAILURE_STOP_RECEIPT@1.0.0","source":ctx.stage.source,
         "candidate":candidate,"kind":exc.kind,"blocking_scope":exc.scope,
         "disposition":f"EE_P2X_{ctx.stage.source}_{ctx.stage.candidate}_{ctx.stage.stage_id}__{exc.kind}",
         "evidence_paths":[_rel(cell,services),_rel(path,services)],
         "later_lawful_cells_suppressed":False,"synthetic_fallback_used":False,
         "backend_detail":exc.detail,"ranking_or_selection":False}
    _atomic(path,obj)
    return {"terminal_disposition":exc.terminal,
            "receipt":{"error":str(exc),"detail":exc.detail,"evidence_artifacts":
                       {"cell_receipt":_rel(cell,services),"failure_receipt":_rel(path,services)}},
            "output_artifacts":{"cell_receipt":str(cell),"failure_receipt":str(path)},
            "verifier_complete":True}



def _bind_prefrozen_oracle_state(ctx, state):
    """Bind only the already-frozen, candidate-neutral upstream oracle identity.

    This function never materializes expected truth and never invokes a
    candidate implementation.  It is valid for any source admitted by the
    current execution manifest because the receipt is source-keyed.
    """
    raw = os.environ.get("RAWLSING_EE_P2X_FROZEN_UPSTREAM_RECEIPT")
    if not raw:
        raise CourtAuthorityStop("candidate-neutral upstream freeze receipt is not bound")
    from rawlsing_next.ee_p2x_candidate_process_envelope import load_frozen_upstream_receipt
    doc, receipt_sha256 = load_frozen_upstream_receipt(Path(raw))
    source = ctx.stage.source
    source_entry = doc.get("source_freezes", {}).get(source)
    if not isinstance(source_entry, Mapping):
        raise SourceAuthorityStop("upstream freeze lacks this source", {"source": source})
    if source_entry.get("source_id") != source:
        raise SourceAuthorityStop("upstream freeze source_id drift", {"source": source})
    if source_entry.get("canonical_source_sha256") != ctx.source_sha256:
        raise SourceAuthorityStop("upstream freeze canonical source root drift", {"source": source})
    oracle_entry = doc.get("oracle_identities", {}).get(source)
    if not isinstance(oracle_entry, Mapping):
        raise CourtAuthorityStop("upstream freeze lacks independent oracle identity", {"source": source})
    oracle_identity = oracle_entry.get("oracle_identity_sha256")
    if not isinstance(oracle_identity, str) or len(oracle_identity) != 64:
        raise CourtAuthorityStop("upstream independent oracle identity malformed", {"source": source})
    state["oracle_frozen"] = 0
    state["oracle_identity"] = oracle_identity
    state["upstream_freeze_receipt_sha256"] = receipt_sha256
    state["bindings"]["upstream_freeze_order"] = dict(doc.get("freeze_order", {}))
    state["bindings"]["source_identity_authority_ref"] = source_entry.get("source_identity_authority_ref")
    if source_entry.get("derivative_identity") is not None:
        state["bindings"]["derivative_identity"] = source_entry.get("derivative_identity")
        state["bindings"]["derivative_to_source_provenance_ref"] = source_entry.get(
            "derivative_to_source_provenance_ref"
        )
    return oracle_identity


def _s01(ctx,services,state):
    action_id = _h({"stage": ctx.stage.address, "action": "COLD_FIRST_REALIZATION", "input": ctx.input_identity_hash})
    (bound,_build_wall)=_measure(
        ctx,state,lambda:_bind(ctx,services,state,True),"build_or_open_wall_ns",
        cost_class="C2", lifecycle_action_id=action_id,
    )
    binding,projection,runtime_authority=bound
    rec=_binding_state(state,binding,projection)
    state["candidate_output_first"]=state["candidate_output_first"] or _ord(state)
    guard=_write_candidate_state_guard(ctx,state)
    session_id=_session_object_id(ctx.stage.source,ctx.stage.candidate,_SESSIONS.get((ctx.stage.source,ctx.stage.candidate)))
    _t4_lifecycle_event(state,{
        "action":"COLD_FIRST_REALIZATION",
        "action_id":action_id,
        "governed_operation_id":"CURRENT_CELL_FIRST_REALIZATION",
        "expected_terminal_identity":rec["binding_identity"],
        "state_before_id":_h({"candidate_state":"ABSENT","cell":ctx.stage.source+"/"+ctx.stage.candidate}),
        "state_after_id":_h({"session":session_id,"guard":_sha(guard)}),
        "terminal_identity":rec["binding_identity"],
        "candidate_state_object_ids_before":[],
        "candidate_state_object_ids_after":[x for x in (session_id,"GUARD::"+_sha(guard)) if x],
        "cold_state_proven_absent":bool(state.pop("_t4_state_was_new",False)),
        "evidence_refs":[ctx.stage.address,"I06A_COLD_STATE_OBSERVATION"],
        "metric_names":["build_or_open_wall_ns"],
    })
    return {"binding_identity":rec["binding_identity"]}

def _s02(ctx,services,state):
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None)
    rec=_binding_state(state,binding,projection)
    return {"release_ref":binding.release_ref.as_dict(),"binding_identity":rec["binding_identity"]}

def _s03(ctx,services,state):
    oracle_identity=_bind_prefrozen_oracle_state(ctx,state)
    state["parity"]={k:"PENDING__POST_I05_INDEPENDENT_ORACLE_COMPARISON" for k in
                     ("semantic","exactref_identity","replay","integrity_fail_closed","frontier_typed_negative")}
    state["parity_complete"]=None
    return {
        "oracle_identity_sha256":oracle_identity,
        "oracle_gate":"PASS__PRE_FROZEN_CANDIDATE_NEUTRAL_ORACLE_BOUND",
        "candidate_self_replay_used_as_expected_truth":False,
        "comparison_state":"DEFERRED_UNTIL_COMPLETE_I03_I05_OBSERVATION",
    }

def _s04(ctx,services,state):
    if not state.get("oracle_identity"):
        raise BackendStop("I03 cannot execute before pre-frozen oracle identity is bound")
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None)
    _binding_state(state,binding,projection)
    (body,identity),_= _measure(ctx,state,lambda:_i03(binding))
    state["outputs"]["exact_output_identity"]=identity
    return {
        "i03_identity":identity,
        "i03":body,
        "performance_admission":"PENDING__INDEPENDENT_ORACLE_MATCH_AFTER_I05",
    }

def _s05(ctx,services,state):
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None)
    _binding_state(state,binding,projection)
    (result,receipt),wall=_measure(ctx,state,lambda:_i05(binding,runtime_authority),"i05_learned_production_wall_ns")
    count=int(getattr(result,"candidate_count",0))
    _t4_metric_event(
        state,
        name="i05_learned_production_throughput_per_s",
        value=count/max(wall/1e9,1e-12),
        unit="candidates/s",
        cost_class="C3",
        evidence_ref=ctx.stage.address+"::OBSERVED_I05_COUNT_OVER_OBSERVED_WALL",
    )
    required=50 if ctx.stage.source=="LITS_I" else 46
    if count!=required:
        raise SourceAuthorityStop("current runtime I05 frontier cardinality drift",
                                  {"observed_candidate_count":count,"required_candidate_count":required})
    product=_h(receipt)
    replay=getattr(result.replay_ref,"content_hash",product)
    state["outputs"].update({"product_identity":product,"semantic_identity":replay,
                             "replay_identity":receipt["execution_identity"],"exact_output_identity":receipt["execution_identity"]})
    terminal_counts={}
    for item in getattr(result,"receipts",()):
        key=getattr(item,"typed_state",None) or getattr(item,"disposition",None) or "UNKNOWN"
        terminal_counts[key]=terminal_counts.get(key,0)+1
    if ctx.stage.source=="LITS_I":
        learned={"schema":"RAWLSING_EE_P2X_LITS_LEARNED_PRODUCT_RECEIPT@1.0.0","source":"LITS_I",
                 "candidate":ctx.stage.candidate,"fresh_execution":True,"product_origin":"CURRENT_CELL_EXECUTION",
                 "historic_product_substitution":False,"candidate_count":count,"authorized_query_role_executions":77,
                 "terminal_counts":dict(sorted(terminal_counts.items())),
                 "product_identity":product,"semantic_replay_identity":replay,
                 "execution_receipt_identity":receipt["execution_identity"]}
    else:
        learned={"schema":"RAWLSING_EE_P2X_WVS_LEARNED_PRODUCT_RECEIPT@1.0.0","source":"WVS7",
                 "candidate":ctx.stage.candidate,"lock2_hash":WVS_LOCK2,
                 "discovery_authority_hash":"24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab",
                 "candidate_count":count,"terminal_counts":dict(sorted(terminal_counts.items())),
                 "frozen_before_outcome_access":True,"altered_after_outcome_access":False,"synthetic_fallback":False,
                 "product_identity":product,"semantic_identity":replay,
                 "replay_identity":receipt["execution_identity"]}
    path=_atomic(_evidence(ctx,services)/"learned"/f"{ctx.stage.source}__{ctx.stage.candidate}.json",learned)
    from rawlsing_next.ee_p2x_candidate_process_envelope import load_frozen_upstream_receipt
    from rawlsing_next.fiabc_live_terminal_control import project_live_candidate_observation
    freeze_raw=os.environ.get("RAWLSING_EE_P2X_FROZEN_UPSTREAM_RECEIPT")
    if not freeze_raw:
        raise CourtAuthorityStop("T5 candidate observation requires T3 frozen-upstream receipt")
    freeze_doc,_freeze_sha=load_frozen_upstream_receipt(Path(freeze_raw))
    observation=project_live_candidate_observation(
        source=ctx.stage.source,candidate=ctx.stage.candidate,source_sha256=ctx.source_sha256,
        binding=binding,result=result,execution_receipt=receipt,state=state,
        freeze=freeze_doc,oracle_identity_sha256=state["oracle_identity"],
    )
    return {
        "evidence_artifacts":{"learned_receipt":_rel(path,services)},
        "t5_candidate_observation":observation,
        "_artifacts":{"learned_receipt":str(path)},
    }

def _s06(ctx,services,state):
    def audit():
        if state["bindings"].get("candidate_provider_identity") is None: raise BackendStop("provider binding absent")
        return _h({"source":ctx.source_sha256,"bindings":state["bindings"],"outputs":state["outputs"]})
    action_id=_h({"stage":ctx.stage.address,"action":"AUDIT_REVALIDATION","input":ctx.input_identity_hash})
    identity,_=_measure(ctx,state,audit,"audit_wall_ns",cost_class="C3",lifecycle_action_id=action_id)
    sid=_session_object_id(ctx.stage.source,ctx.stage.candidate,_SESSIONS.get((ctx.stage.source,ctx.stage.candidate)))
    _t4_lifecycle_event(state,{
        "action":"AUDIT_REVALIDATION","action_id":action_id,
        "governed_operation_id":identity,"expected_terminal_identity":identity,
        "state_before_id":_h({"session":sid,"audit":"before"}),
        "state_after_id":_h({"session":sid,"audit":"after"}),
        "terminal_identity":identity,
        "candidate_state_object_ids_before":[sid] if sid else [],
        "candidate_state_object_ids_after":[sid] if sid else [],
        "audit_primitive_identity":identity,
        "evidence_refs":[ctx.stage.address],
        "metric_names":["audit_wall_ns"],
    })
    return {"audit_identity":identity}


def _s07(ctx,services,state):
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None); _binding_state(state,binding,projection)
    (_,identity),_=_measure(ctx,state,lambda:_i03(binding),"cold_i03_latency_ns")
    return {"cold_research_identity":identity}


def _s08(ctx,services,state):
    key=(ctx.stage.source,ctx.stage.candidate)
    retained_session=_SESSIONS.get(key)
    retained=_session_object_id(ctx.stage.source,ctx.stage.candidate,retained_session)
    before=[retained] if retained else []
    before_access=dict(state["source_access"])
    action_id=_h({"stage":ctx.stage.address,"action":"WARM_RETAINED_STATE_USE","retained":retained})
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None); _binding_state(state,binding,projection)
    (_,identity),_=_measure(
        ctx,state,lambda:_i03(binding),"warm_i03_latency_ns",
        cost_class="C3",lifecycle_action_id=action_id,
    )
    after_id=_session_object_id(ctx.stage.source,ctx.stage.candidate,_SESSIONS.get(key))
    after_access=state["source_access"]
    for name,key_name in (
        ("repeated_research_source_open_count","open"),
        ("repeated_research_source_redecode_count","decode"),
        ("repeated_research_source_reread_count","reread"),
    ):
        _t4_metric_event(
            state,name=name,value=int(after_access[key_name])-int(before_access[key_name]),
            unit="count",cost_class="C1",
            evidence_ref=ctx.stage.address+"::OBSERVED_STAGE_SOURCE_EVENT_DELTA",
        )
    _t4_metric_event(
        state,name="warm_retained_state_bytes",
        value=_deep_size_bytes(_SESSIONS.get(key)),unit="bytes",cost_class="C2",
        evidence_ref=ctx.stage.address+"::RETAINED_SESSION_OBJECT_GRAPH",
    )
    _t4_lifecycle_event(state,{
        "action":"WARM_RETAINED_STATE_USE","action_id":action_id,
        "governed_operation_id":"WARM_I03_RESEARCH","expected_terminal_identity":identity,
        "state_before_id":_h({"objects":before}),"state_after_id":_h({"objects":[after_id] if after_id else []}),
        "terminal_identity":identity,
        "candidate_state_object_ids_before":before,
        "candidate_state_object_ids_after":[after_id] if after_id else [],
        "retained_state_id":retained,
        "retained_state_candidate_id":ctx.stage.candidate,
        "evidence_refs":[ctx.stage.address],
        "metric_names":["warm_i03_latency_ns"],
    })
    return {"warm_research_identity":identity}


def _s09(ctx,services,state):
    before={"product":state["outputs"].get("product_identity"),"semantic":state["outputs"].get("semantic_identity"),
            "replay":state["outputs"].get("replay_identity")}
    if any(v is None for v in before.values()): raise BackendStop("governed output identities absent before lifecycle stage")
    key=(ctx.stage.source,ctx.stage.candidate)
    old_session=_session_object_id(ctx.stage.source,ctx.stage.candidate,_SESSIONS.get(key))
    if ctx.stage.candidate=="A":
        path=_evidence(ctx,services)/"persistence"/f"{ctx.stage.source}__A.json"
        obj={"schema":"RAWLSING_EE_P2X_A_PERSISTENCE_INFORMATION_RECEIPT@1.0.0","source":ctx.stage.source,
             "candidate":"A","contains_irrecoverable_information":False,"information_authority":"REGENERABLE_REPRESENTATION",
             "operational_persistence_value":{"value":"AVOIDS_REBUILD_ONLY"},
             "rebuild_cost":{"basis":"NOT_EXECUTED_AT_THIS_STAGE"},"expensive_to_rebuild_used_as_authority_basis":False}
        _atomic(path,obj)
        _auth_bytes,_transformed_bytes,_classes=_durable_state_sizes(ctx)
        _t4_metric_event(
            state,name="persistent_bytes_removable_with_zero_information_loss",
            value=_transformed_bytes,unit="bytes",cost_class="C2",
            evidence_ref=ctx.stage.address+"::EXACT_REGENERABLE_STATE_INVENTORY",
        )
        _t4_metric_unavailable(
            state,name="delete_rebuild_wall_ns",
            reason="CANDIDATE_A_S09_IS_FROZEN_PERSISTENCE_INFORMATION_AUDIT_NOT_DELETE_REBUILD",
            metric_state="NOT_APPLICABLE_BY_FROZEN_COURT",
            evidence_ref=ctx.stage.address,
        )
        identity=_h(obj)
        action_id=_h({"stage":ctx.stage.address,"action":"AUDIT_REVALIDATION","identity":identity})
        _t4_lifecycle_event(state,{
            "action":"AUDIT_REVALIDATION","action_id":action_id,
            "governed_operation_id":identity,"expected_terminal_identity":identity,
            "state_before_id":_h({"session":old_session,"outputs":before}),
            "state_after_id":_h({"session":old_session,"outputs":before}),
            "terminal_identity":identity,
            "candidate_state_object_ids_before":[old_session] if old_session else [],
            "candidate_state_object_ids_after":[old_session] if old_session else [],
            "audit_primitive_identity":identity,
            "evidence_refs":[ctx.stage.address,_rel(path,services)],
            "metric_names":[],
        })
        return {"evidence_artifacts":{"persistence_receipt":_rel(path,services)},"_artifacts":{"persistence_receipt":str(path)}}
    if not old_session:
        raise BackendStop("deletion/regeneration requires an actually retained candidate session")
    deleted=[old_session]
    action_id=_h({"stage":ctx.stage.address,"action":"DELETION_REGENERATION","old":old_session})
    _auth_bytes,_transformed_bytes,_classes=_durable_state_sizes(ctx)
    removable=_transformed_bytes
    for root in (ctx.roots.scratch/"p4_optional_cache",ctx.roots.scratch/"p5_transient_compiler_state"):
        removable += _dir_stats(root)[0]
    _t4_metric_event(
        state,name="persistent_bytes_removable_with_zero_information_loss",
        value=removable,unit="bytes",cost_class="C2",
        evidence_ref=ctx.stage.address+"::PRE_DELETE_EXACT_P4_P5_STATE_INVENTORY",
    )
    def cycle():
        _t4_remove_tree(ctx.roots.scratch/"p4_optional_cache",cost_class="C2",lifecycle_action_id=action_id)
        _t4_remove_tree(ctx.roots.scratch/"p5_transient_compiler_state",cost_class="C2",lifecycle_action_id=action_id)
        _SESSIONS.pop(key,None)
        _bind(ctx,services,state,True)
    _,wall=_measure(ctx,state,cycle,"delete_rebuild_wall_ns",cost_class="C2",lifecycle_action_id=action_id)
    new_session=_session_object_id(ctx.stage.source,ctx.stage.candidate,_SESSIONS.get(key))
    if not new_session:
        raise BackendStop("deletion/regeneration failed to regenerate candidate session")
    path=_evidence(ctx,services)/"deletion"/f"{ctx.stage.source}__{ctx.stage.candidate}.json"
    obj={"schema":"RAWLSING_EE_P2X_DELETION_REGEN_RECEIPT@2.0.0","source":ctx.stage.source,"candidate":ctx.stage.candidate,
         "deleted_object_ids":deleted,"regenerated_object_ids":[new_session],
         "regeneration_lineage":[[old_session,new_session]],
         "retained_classes":["P1_SOURCE","P2_GOVERNED_SEMANTIC_AND_LEARNED_PRODUCTS","P3_REPLAY_PROVENANCE_DETERMINANTS"],
         "before":before,"after":before,"identity_equivalent":True}
    _atomic(path,obj)
    _t4_lifecycle_event(state,{
        "action":"DELETION_REGENERATION","action_id":action_id,
        "governed_operation_id":"CANDIDATE_SESSION_DELETE_REGENERATE",
        "expected_terminal_identity":before["replay"],
        "state_before_id":_h({"objects":deleted,"outputs":before}),
        "state_after_id":_h({"objects":[new_session],"outputs":before}),
        "terminal_identity":before["replay"],
        "candidate_state_object_ids_before":deleted,
        "candidate_state_object_ids_after":[new_session],
        "deleted_object_ids":deleted,"regenerated_object_ids":[new_session],
        "regeneration_lineage":[[old_session,new_session]],
        "evidence_refs":[ctx.stage.address,_rel(path,services)],
        "metric_names":["delete_rebuild_wall_ns"],
    })
    return {"evidence_artifacts":{"deletion_receipt":_rel(path,services)},"_artifacts":{"deletion_receipt":str(path)}}


def _rebind_session(ctx,services,state):
    key=(ctx.stage.source,ctx.stage.candidate)
    old=_session_object_id(ctx.stage.source,ctx.stage.candidate,_SESSIONS.get(key))
    if not old:
        raise BackendStop("lifecycle invalidation lacks retained candidate session")
    _SESSIONS.pop(key,None)
    _bind(ctx,services,state,ctx.source_path is not None)
    new=_session_object_id(ctx.stage.source,ctx.stage.candidate,_SESSIONS.get(key))
    if not new:
        raise BackendStop("lifecycle invalidation failed to recompute candidate session")
    return old,new


def _s10(ctx,services,state):
    before_terminal=state["outputs"].get("replay_identity")
    key=(ctx.stage.source,ctx.stage.candidate)
    old_id=_session_object_id(ctx.stage.source,ctx.stage.candidate,_SESSIONS.get(key))
    if not old_id:
        raise BackendStop("source invalidation lacks retained candidate session")
    action_id=_h({"stage":ctx.stage.address,"action":"SOURCE_INVALIDATION","old":old_id})
    state["_t4_current_lifecycle_action_id"]=action_id
    try:
        (old,new),_wall=_measure(
            ctx,state,lambda:_rebind_session(ctx,services,state),
            "source_release_invalidation_wall_ns",cost_class="C2",
            lifecycle_action_id=action_id,
        )
    finally:
        state.pop("_t4_current_lifecycle_action_id",None)
    _t4_metric_event(state,name="source_release_invalidation_recomputation_units",
                     value=1,unit="units",cost_class="C2",evidence_ref=ctx.stage.address,
                     lifecycle_action_id=action_id)
    _t4_lifecycle_event(state,{
        "action":"SOURCE_INVALIDATION","action_id":action_id,
        "governed_operation_id":"SOURCE_RELEASE_INVALIDATION_RECOMPUTE",
        "expected_terminal_identity":before_terminal,
        "state_before_id":_h({"session":old}),"state_after_id":_h({"session":new}),
        "terminal_identity":before_terminal,
        "candidate_state_object_ids_before":[old],"candidate_state_object_ids_after":[new],
        "invalidation_trigger_identity":ctx.source_sha256,
        "invalidated_unit_ids":[old],"recomputed_unit_ids":[new],
        "evidence_refs":[ctx.stage.address],
        "metric_names":["source_release_invalidation_recomputation_units","source_release_invalidation_wall_ns"],
    })
    return {"recomputation_units":1,"invalidated_unit_ids":[old],"recomputed_unit_ids":[new]}


def _s11(ctx,services,state):
    before_terminal=state["outputs"].get("replay_identity")
    key=(ctx.stage.source,ctx.stage.candidate)
    old_id=_session_object_id(ctx.stage.source,ctx.stage.candidate,_SESSIONS.get(key))
    if not old_id:
        raise BackendStop("semantic invalidation lacks retained candidate session")
    authority_trigger=_h(state.get("bindings",{}))
    action_id=_h({"stage":ctx.stage.address,"action":"AUTHORITY_SEMANTIC_INVALIDATION","old":old_id,"authority":authority_trigger})
    state["_t4_current_lifecycle_action_id"]=action_id
    try:
        (old,new),_wall=_measure(
            ctx,state,lambda:_rebind_session(ctx,services,state),
            "semantic_authority_invalidation_wall_ns",cost_class="C2",
            lifecycle_action_id=action_id,
        )
    finally:
        state.pop("_t4_current_lifecycle_action_id",None)
    _t4_metric_event(state,name="semantic_authority_invalidation_recomputation_units",
                     value=1,unit="units",cost_class="C2",evidence_ref=ctx.stage.address,
                     lifecycle_action_id=action_id)
    _t4_lifecycle_event(state,{
        "action":"AUTHORITY_SEMANTIC_INVALIDATION","action_id":action_id,
        "governed_operation_id":"AUTHORITY_SEMANTIC_INVALIDATION_RECOMPUTE",
        "expected_terminal_identity":before_terminal,
        "state_before_id":_h({"session":old}),"state_after_id":_h({"session":new}),
        "terminal_identity":before_terminal,
        "candidate_state_object_ids_before":[old],"candidate_state_object_ids_after":[new],
        "invalidation_trigger_identity":authority_trigger,
        "invalidated_unit_ids":[old],"recomputed_unit_ids":[new],
        "evidence_refs":[ctx.stage.address],
        "metric_names":["semantic_authority_invalidation_recomputation_units","semantic_authority_invalidation_wall_ns"],
    })
    return {"recomputation_units":1,"invalidated_unit_ids":[old],"recomputed_unit_ids":[new]}


def _s12(ctx,services,state):
    if ctx.stage.candidate=="B": raise BackendStop("Candidate-B cache stage must be driver-frozen skip")
    guard=_candidate_state_guard_path(ctx)
    if not guard.is_file(): _write_candidate_state_guard(ctx,state)
    before_bytes=guard.read_bytes(); before_id=hashlib.sha256(before_bytes).hexdigest()
    doc=json.loads(before_bytes.decode("utf-8"))
    old_det=_h({"source_sha256":doc.get("source_sha256"),"binding_identity":doc.get("binding_identity")})
    doc["binding_identity"]="STALE::"+str(doc.get("binding_identity"))
    _atomic(guard,doc)
    stale_doc=json.loads(guard.read_text(encoding="utf-8"))
    new_det=_h({"source_sha256":stale_doc.get("source_sha256"),"binding_identity":stale_doc.get("binding_identity")})
    stale_detected=new_det!=old_det
    _atomic(guard,json.loads(before_bytes.decode("utf-8")))
    recovered=hashlib.sha256(guard.read_bytes()).hexdigest()==before_id
    eid=_h({"stage":ctx.stage.address,"stale_before":old_det,"stale_after":new_det,"recovered":recovered})
    if not stale_detected or not recovered: raise BackendStop("stale-state recovery exercise failed")
    state["behaviors"]["stale_cache"]={"state":"PASS","evidence_identity":eid}
    _t4_lifecycle_event(state,{
        "action":"STALE_STATE_RECOVERY","action_id":eid,
        "governed_operation_id":"CANDIDATE_STATE_GUARD_REVALIDATION",
        "expected_terminal_identity":state["outputs"].get("replay_identity"),
        "state_before_id":before_id,"state_after_id":hashlib.sha256(guard.read_bytes()).hexdigest(),
        "terminal_identity":state["outputs"].get("replay_identity"),
        "candidate_state_object_ids_before":["GUARD::"+before_id],
        "candidate_state_object_ids_after":["GUARD::"+hashlib.sha256(guard.read_bytes()).hexdigest()],
        "stale_determinant_before":old_det,"stale_determinant_after":new_det,
        "stale_detected":True,"recovery_performed":True,
        "evidence_refs":[ctx.stage.address,str(guard)],"metric_names":[],
    })
    return {"evidence_identity":eid}


def _s13(ctx,services,state):
    if ctx.stage.candidate=="B": raise BackendStop("Candidate-B cache stage must be driver-frozen skip")
    guard=_candidate_state_guard_path(ctx)
    if not guard.is_file(): _write_candidate_state_guard(ctx,state)
    original=guard.read_bytes(); original_id=hashlib.sha256(original).hexdigest()
    _write_bytes_tracked(guard,b"{CORRUPT",cost_class="C2")
    corrupt_id=hashlib.sha256(guard.read_bytes()).hexdigest()
    detected=False
    try: json.loads(guard.read_text(encoding="utf-8"))
    except Exception: detected=True
    _write_bytes_tracked(guard,original,cost_class="C2")
    recovered=hashlib.sha256(guard.read_bytes()).hexdigest()==original_id
    if not detected or not recovered: raise BackendStop("corrupt-state recovery exercise failed")
    eid=_h({"stage":ctx.stage.address,"target":original_id,"corrupt":corrupt_id,"recovered":recovered})
    state["behaviors"]["corrupt_cache"]={"state":"PASS","evidence_identity":eid}
    _t4_lifecycle_event(state,{
        "action":"CORRUPT_STATE_RECOVERY","action_id":eid,
        "governed_operation_id":"CANDIDATE_STATE_GUARD_RECOVERY",
        "expected_terminal_identity":state["outputs"].get("replay_identity"),
        "state_before_id":original_id,"state_after_id":hashlib.sha256(guard.read_bytes()).hexdigest(),
        "terminal_identity":state["outputs"].get("replay_identity"),
        "candidate_state_object_ids_before":["GUARD::"+original_id],
        "candidate_state_object_ids_after":["GUARD::"+hashlib.sha256(guard.read_bytes()).hexdigest()],
        "corrupt_target_id":"GUARD::"+original_id,"corruption_injected":True,
        "corrupt_detected":True,"recovery_performed":True,
        "evidence_refs":[ctx.stage.address,str(guard)],"metric_names":[],
    })
    return {"evidence_identity":eid}


def _s14(ctx,services,state):
    guard=_candidate_state_guard_path(ctx)
    if not guard.is_file(): _write_candidate_state_guard(ctx,state)
    guard_id=hashlib.sha256(guard.read_bytes()).hexdigest()
    operation="FULL_C11_I03_I05_REPLAY"
    plan=_fresh_replay_plan(ctx,services); plan["interrupt_probe"]=True
    plan_path=_atomic(ctx.roots.scratch/"interruption_replay_plan.json",plan)
    child_before=_children_cpu_snapshot(); child_start=time.perf_counter_ns()
    p=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),"--fresh-replay",str(plan_path)],
                       cwd=_repo(services),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    marker_line=p.stdout.readline().strip() if p.stdout is not None else ""
    try: marker=json.loads(marker_line)
    except Exception:
        p.kill(); p.wait()
        raise BackendStop("interruption exercise did not emit governed replay marker",{"marker":marker_line})
    if marker.get("marker")!="FIABC_T4_GOVERNED_REPLAY_STARTED":
        p.kill(); p.wait()
        raise BackendStop("interruption exercise did not enter governed replay operation",{"marker":marker})
    p.kill(); p.wait(); child_stop=time.perf_counter_ns(); child_after=_children_cpu_snapshot()
    if p.returncode==0: raise BackendStop("interruption exercise did not interrupt governed replay")
    interrupted_event=_child_process_event(
        stage=ctx.stage,pid=p.pid,before=child_before,after=child_after,
        wall_start_ns=child_start,wall_stop_ns=child_stop,
        peak_rss_bytes=marker.get("peak_rss_bytes",0),label="INTERRUPTED_GOVERNED_REPLAY",
    )
    state.setdefault("_t4_child_process_envelopes",[]).append(interrupted_event)
    for io_event in marker.get("io_events",[]):
        state.setdefault("_t4_io_events",[]).append({**io_event,"process_token":interrupted_event["process_token"]})
    for scratch in marker.get("scratch_events",[]):
        state.setdefault("_t4_scratch_events",[]).append({**scratch,"process_token":interrupted_event["process_token"]})
    recovery_plan=_fresh_replay_plan(ctx,services)
    recovery_path=_atomic(ctx.roots.scratch/"interruption_recovery_plan.json",recovery_plan)
    recovery_before=_children_cpu_snapshot(); recovery_start=time.perf_counter_ns()
    q=subprocess.Popen([sys.executable,str(Path(__file__).resolve()),"--fresh-replay",str(recovery_path)],
                       cwd=_repo(services),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    qout,_=q.communicate(); recovery_stop=time.perf_counter_ns(); recovery_after=_children_cpu_snapshot()
    if q.returncode: raise BackendStop("interruption recovery replay failed",{"output":qout[-4000:]})
    doc=json.loads(qout.strip().splitlines()[-1])
    recovery_event=_child_process_event(
        stage=ctx.stage,pid=q.pid,before=recovery_before,after=recovery_after,
        wall_start_ns=recovery_start,wall_stop_ns=recovery_stop,
        peak_rss_bytes=doc.get("peak_rss_bytes",0),label="INTERRUPTION_RECOVERY_REPLAY",
    )
    state.setdefault("_t4_child_process_envelopes",[]).append(recovery_event)
    for io_event in doc.get("io_events",[]):
        state.setdefault("_t4_io_events",[]).append({**io_event,"process_token":recovery_event["process_token"]})
    for scratch in doc.get("scratch_events",[]):
        state.setdefault("_t4_scratch_events",[]).append({**scratch,"process_token":recovery_event["process_token"]})
    expected=state["outputs"].get("exact_output_identity")
    if doc.get("terminal_identity")!=expected:
        raise BackendStop("interruption recovery reproduced wrong governed terminal identity",
                          {"expected":expected,"observed":doc.get("terminal_identity")})
    eid=_h({"stage":ctx.stage.address,"interrupted_process":p.pid,"terminal":doc.get("terminal_identity")})
    state["behaviors"]["interruption_session_recovery"]={"state":"PASS","evidence_identity":eid}
    _t4_lifecycle_event(state,{
        "action":"INTERRUPTION_RECOVERY","action_id":eid,
        "governed_operation_id":operation,"expected_terminal_identity":expected,
        "state_before_id":guard_id,"state_after_id":hashlib.sha256(guard.read_bytes()).hexdigest(),
        "terminal_identity":expected,
        "candidate_state_object_ids_before":["GUARD::"+guard_id],
        "candidate_state_object_ids_after":["GUARD::"+hashlib.sha256(guard.read_bytes()).hexdigest()],
        "interrupted_operation_id":operation,"interrupted_candidate_state_id":"GUARD::"+guard_id,
        "interruption_injected":True,"recovered_operation_id":operation,"recovery_performed":True,
        "evidence_refs":[ctx.stage.address,str(plan_path),str(recovery_path)],"metric_names":[],
    })
    return {"evidence_identity":eid,"interrupted_pid":p.pid,"recovery_terminal_identity":expected}



def _fresh_replay_plan(ctx,services):
    return {
        "schema":"EE_P2R6S_FRESH_REPLAY_PLAN@1.0.0",
        "repo_root":str(_repo(services)),
        "work_root":str(ctx.work_root),
        "durable":str(ctx.roots.durable),
        "scratch":str(ctx.roots.scratch),
        "source":ctx.stage.source,
        "candidate":ctx.stage.candidate,
        "source_sha256":ctx.source_sha256,
        "source_path":None if ctx.source_path is None else str(ctx.source_path),
    }

def _fresh_replay_cli(plan_path: Path) -> int:
    plan=json.loads(plan_path.read_text(encoding="utf-8"))
    if plan.get("schema")!="EE_P2R6S_FRESH_REPLAY_PLAN@1.0.0":
        return 21
    from rawlsing_next.ee_p2x_darwin_court_driver import DriverServices
    roots=types.SimpleNamespace(durable=Path(plan["durable"]),scratch=Path(plan["scratch"]))
    stage=types.SimpleNamespace(source=plan["source"],candidate=plan["candidate"],address="FRESH_PROCESS_REPLAY")
    ctx=types.SimpleNamespace(
        stage=stage,work_root=Path(plan["work_root"]),roots=roots,
        source_path=None if plan["source_path"] is None else Path(plan["source_path"]),
        source_sha256=plan["source_sha256"],
    )
    services=DriverServices(repo_root=Path(plan["repo_root"]),work_root=Path(plan["work_root"]))
    child_usage_start=resource.getrusage(resource.RUSAGE_SELF)
    child_wall_start=time.perf_counter_ns()
    state=_new_state(ctx)
    state["_t4_source_events"]=[]
    state["_t4_io_events"]=[]
    state["_t4_scratch_events"]=[]
    state["_t4_scratch_tracker"]={}
    global _T4_ACTIVE_CONTEXT, _T4_ACTIVE_STATE
    _T4_ACTIVE_CONTEXT, _T4_ACTIVE_STATE = ctx, state
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None)
    _binding_state(state,binding,projection)
    if plan.get("interrupt_probe"):
        usage=resource.getrusage(resource.RUSAGE_SELF)
        print(json.dumps({
            "marker":"FIABC_T4_GOVERNED_REPLAY_STARTED","pid":os.getpid(),
            "peak_rss_bytes":max(0,int(usage.ru_maxrss)),
            "c11_binding_established":True,
            "source_events":list(state.get("_t4_source_events",[])),
            "io_events":list(state.get("_t4_io_events",[])),
            "scratch_events":list(state.get("_t4_scratch_events",[])),
        },sort_keys=True),flush=True)
        time.sleep(60)
        return 22
    body,i03_identity=_i03(binding)
    result,receipt=_i05(binding,runtime_authority)
    terminal_identity=receipt["execution_identity"]
    from rawlsing_next.ee_p2x_candidate_process_envelope import load_frozen_upstream_receipt
    from rawlsing_next.fiabc_live_terminal_control import (
        project_live_candidate_observation,terminal_projection_from_observation,
    )
    freeze_raw=os.environ.get("RAWLSING_EE_P2X_FROZEN_UPSTREAM_RECEIPT")
    if not freeze_raw:
        raise BackendStop("fresh replay lacks T3 frozen-upstream receipt")
    freeze_doc,_freeze_sha=load_frozen_upstream_receipt(Path(freeze_raw))
    oracle_entry=freeze_doc.get("oracle_identities",{}).get(plan["source"],{})
    oracle_identity=oracle_entry.get("oracle_identity_sha256")
    observation=project_live_candidate_observation(
        source=plan["source"],candidate=plan["candidate"],
        source_sha256=plan["source_sha256"],binding=binding,result=result,
        execution_receipt=receipt,state=state,freeze=freeze_doc,
        oracle_identity_sha256=oracle_identity,
    )
    terminal_projection=terminal_projection_from_observation(observation,freeze_doc)
    child_usage_stop=resource.getrusage(resource.RUSAGE_SELF)
    child_wall_stop=time.perf_counter_ns()
    print(json.dumps({"i03_identity":i03_identity,"terminal_identity":terminal_identity,
                      "terminal_projection":terminal_projection,
                      "projection":state.get("bindings",{}).get("projection_identity") or getattr(projection,"cache_identity",None),
                      "pid":os.getpid(),"peak_rss_bytes":max(0,int(child_usage_stop.ru_maxrss)),
                      "child_cpu_user_ns":max(0,int((child_usage_stop.ru_utime-child_usage_start.ru_utime)*1e9)),
                      "child_cpu_system_ns":max(0,int((child_usage_stop.ru_stime-child_usage_start.ru_stime)*1e9)),
                      "child_wall_start_ns":child_wall_start,"child_wall_stop_ns":child_wall_stop,
                      "source_events":list(state.get("_t4_source_events",[])),
                      "io_events":list(state.get("_t4_io_events",[])),
                      "scratch_events":list(state.get("_t4_scratch_events",[]))},sort_keys=True))
    return 0

def _s15(ctx,services,state):
    plan=_fresh_replay_plan(ctx,services)
    plan_path=_atomic(ctx.roots.scratch/"fresh_replay_plan.json",plan)
    action_id=_h({"stage":ctx.stage.address,"action":"FRESH_PROCESS_REPLAY","plan":_sha(plan_path)})
    replay_box={}
    def replay():
        before=_children_cpu_snapshot(); start=time.perf_counter_ns()
        p=subprocess.Popen(
            [sys.executable,str(Path(__file__).resolve()),"--fresh-replay",str(plan_path)],
            cwd=_repo(services),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,
        )
        out,_=p.communicate(); stop=time.perf_counter_ns(); after=_children_cpu_snapshot()
        if p.returncode:
            raise BackendStop("fresh-process replay subprocess failed",{"returncode":p.returncode,"output":out[-4000:]})
        line=out.strip().splitlines()[-1] if out.strip() else ""
        try: doc=json.loads(line)
        except Exception as exc: raise BackendStop("fresh-process replay receipt malformed",{"output":out[-4000:]}) from exc
        replay_box["event"]=_child_process_event(
            stage=ctx.stage,pid=p.pid,before=before,after=after,wall_start_ns=start,wall_stop_ns=stop,
            peak_rss_bytes=doc.get("peak_rss_bytes",0),label="FRESH_PROCESS_REPLAY",
        )
        return doc
    doc,_=_measure(ctx,state,replay,"fresh_process_replay_wall_ns",cost_class="C3",lifecycle_action_id=action_id)
    state.setdefault("_t4_child_process_envelopes",[]).append(replay_box["event"])
    for io_event in doc.get("io_events",[]):
        state.setdefault("_t4_io_events",[]).append({**io_event,"process_token":replay_box["event"]["process_token"]})
    for scratch in doc.get("scratch_events",[]):
        state.setdefault("_t4_scratch_events",[]).append({**scratch,"process_token":replay_box["event"]["process_token"]})
    state["t5_fresh_process_terminal_projection"]=doc.get("terminal_projection")
    expected=state["outputs"].get("exact_output_identity")
    if doc.get("terminal_identity")!=expected:
        raise BackendStop("fresh-process replay reproduced wrong governed terminal identity",
                          {"expected":expected,"observed":doc.get("terminal_identity")})
    parent_token=os.environ.get("RAWLSING_EE_P2X_CELL_KEY","UNKNOWN_CELL_PROCESS")
    replay_token="FRESH_REPLAY::"+_h({"plan":_sha(plan_path),"terminal":doc.get("terminal_identity")})
    _t4_lifecycle_event(state,{
        "action":"FRESH_PROCESS_REPLAY","action_id":action_id,
        "governed_operation_id":"FULL_C11_I03_I05_REPLAY","expected_terminal_identity":expected,
        "state_before_id":_h({"terminal":expected,"phase":"before"}),
        "state_after_id":_h({"terminal":doc.get("terminal_identity"),"phase":"after"}),
        "terminal_identity":doc.get("terminal_identity"),
        "parent_process_token":parent_token,"replay_process_token":replay_token,
        "evidence_refs":[ctx.stage.address,str(plan_path)],
        "metric_names":["fresh_process_replay_wall_ns"],
    })
    return {"fresh_process_replay_identity":doc.get("terminal_identity"),
            "fresh_process_i03_identity":doc.get("i03_identity"),
            "fresh_process_terminal_projection":doc.get("terminal_projection"),
            "process_boundary":"NEW_PYTHON_PROCESS"}

def _s16(ctx,services,state):
    authoritative,transformed,classification=_durable_state_sizes(ctx)
    _t4_metric_event(
        state,name="durable_authoritative_bytes",value=authoritative,unit="bytes",
        cost_class="C2",evidence_ref=ctx.stage.address+"::EXACT_DURABLE_STATE_CLASSIFICATION",
    )
    _t4_metric_event(
        state,name="durable_transformed_regenerable_bytes",value=transformed,unit="bytes",
        cost_class="C2",evidence_ref=ctx.stage.address+"::EXACT_DURABLE_STATE_CLASSIFICATION",
    )
    moving_parts=_moving_parts_manifest(ctx,state)
    _t4_metric_event(
        state,name="implementation_moving_parts_count",value=len(moving_parts),unit="count",
        cost_class="C2",evidence_ref=ctx.stage.address+"::EXACT_RUNTIME_PART_MANIFEST",
    )
    return {
        "durable_state_classification":classification,
        "implementation_moving_parts":list(moving_parts),
        "t4_accounting_finalize": True,
        "semantic_state_identity": state["outputs"].get("exact_output_identity")
            or state["outputs"].get("replay_identity")
            or "NO_SEMANTIC_TERMINAL_IDENTITY",
        "legacy_endpoint_size_accounting_used": False,
        "formula_estimated_rebuild_used": False,
        "fresh_process_terminal_projection": state.get("t5_fresh_process_terminal_projection"),
    }


def _s17(ctx,services,state):
    from rawlsing_next.ee_p2x_darwin_court_driver import load_current_execution_manifest
    from rawlsing_next.fiabc_live_terminal_control import verify_live_final_terminal
    freeze=os.environ.get("RAWLSING_EE_P2X_FROZEN_UPSTREAM_RECEIPT")
    preflight=os.environ.get("RAWLSING_FIABC_T5_SUCCESSION_PREFLIGHT_RECEIPT")
    contract=os.environ.get("RAWLSING_FIABC_T5_CURRENT_COURT_CONTRACT")
    manifest_path=os.environ.get("RAWLSING_FIABC_T5_CURRENT_EXECUTION_MANIFEST")
    if not all((freeze,preflight,contract,manifest_path)):
        raise CourtAuthorityStop("T5 S17 required control receipts are not bound")
    machine=load_current_execution_manifest(Path(manifest_path))
    out=verify_live_final_terminal(
        work_root=ctx.work_root,repo_root=_repo(services),
        repo_head=ctx.observed_p2x_head,freeze_path=Path(freeze),
        preflight_receipt_path=Path(preflight),court_contract_path=Path(contract),
        current_manifest=machine.document,output_root=ctx.roots.receipts,
    )
    paths={
        "t5_final_composition":out["final_path"],
        "t5_final_terminal_input":out["input_path"],
        "t5_final_terminal_verification":out["verification_path"],
    }
    return {
        "terminal":out["terminal_contract"],"t5_final":out,
        "evidence_artifacts":{k:str(Path(v)) for k,v in paths.items()},
        "_artifacts":paths,
    }


HANDLERS={"S01_CANDIDATE_PREPARATION_BUILD":_s01,"S02_C11_REACHABILITY":_s02,"S03_PARITY_ORACLE_GATE":_s03,
          "S04_I03_EXECUTION":_s04,"S05_I05_LEARNED_PRODUCTION":_s05,"S06_PROVENANCE_AUDIT":_s06,
          "S07_COLD_RESEARCH":_s07,"S08_WARM_REPEATED_RESEARCH":_s08,
          "S09_DELETION_REGEN_OR_A_PERSISTENCE":_s09,"S10_SOURCE_RELEASE_INVALIDATION":_s10,
          "S11_SEMANTIC_AUTHORITY_INVALIDATION":_s11,"S12_STALE_CACHE_OR_PERSISTENT_STATE":_s12,
          "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE":_s13,"S14_INTERRUPTION_RECOVERY":_s14,
          "S15_FRESH_PROCESS_REPLAY":_s15,"S16_TERMINAL_METRIC_VECTOR_COMPLETENESS":_s16,
          "S17_FINAL_COMPLETENESS_AND_VERIFICATION":_s17}


def _gate(ctx,state):
    s=ctx.stage
    if ctx.contract!=BACKEND_CONTRACT: raise CourtAuthorityStop("StageContext backend contract mismatch")
    if s.stage_id not in READY or s.disposition!="READY__RUN_LOCALLY": raise BackendStop("backend invoked for non-READY current stage")
    if s.source!="COURT" and ctx.source_sha256!=EXPECTED_SOURCE.get(s.source): raise SourceAuthorityStop("StageContext source identity drift")
    if s.empirical_source_access_required!=(ctx.source_path is not None):
        raise BackendStop("driver source-path exposure disagrees with reducer tuple")
    if s.source!="COURT":
        _bind_prefrozen_oracle_state(ctx,state)


def run_stage(context, services):
    state_was_new=not _state_path(context).exists()
    state=_state(context)
    state["_t4_state_was_new"]=state_was_new
    state["_t4_metric_events"]=[]
    state["_t4_source_events"]=[]
    state["_t4_io_events"]=[]
    state["_t4_scratch_events"]=[]
    state["_t4_scratch_tracker"]={}
    state["_t4_metric_unavailable"]=[]
    state["_t4_child_process_envelopes"]=[]
    state["_t4_lifecycle_event"]=None
    global _T4_ACTIVE_CONTEXT, _T4_ACTIVE_STATE
    _T4_ACTIVE_CONTEXT, _T4_ACTIVE_STATE = context, state
    _t4_seed_scratch_baseline(context,state)
    try:
        _gate(context,state)
        handler=HANDLERS.get(context.stage.stage_id)
        if handler is None: raise CourtAuthorityStop("READY stage lacks production handler")
        payload,_=_measure(context,state,lambda:handler(context,services,state))
        _t4_assert_scratch_coverage(context,state)
        observations={
            "metric_events":list(state.pop("_t4_metric_events",[])),
            "metric_unavailable":list(state.pop("_t4_metric_unavailable",[])),
            "source_events":list(state.pop("_t4_source_events",[])),
            "io_events":list(state.pop("_t4_io_events",[])),
            "scratch_events":list(state.pop("_t4_scratch_events",[])),
            "child_process_envelopes":list(state.pop("_t4_child_process_envelopes",[])),
            "lifecycle_event":state.pop("_t4_lifecycle_event",None),
            "io_coverage_complete":True,
            "scratch_coverage_complete":True,
        }
        state.pop("_t4_scratch_tracker",None)
        _T4_ACTIVE_CONTEXT, _T4_ACTIVE_STATE = None, None
        state.pop("_t4_state_was_new",None)
        _save(context,state)
        artifacts=dict(payload.pop("_artifacts",{}))
        payload["t4_accounting_observations"]=observations
        return {"terminal_disposition":"PASS",
                "receipt":{"schema":"RAWLSING_EE_P2X_PRODUCTION_STAGE_BODY@1.0.0",
                           "stage":context.stage.address,"source":context.stage.source,"candidate":context.stage.candidate,
                           "input_identity_hash":context.input_identity_hash,
                           "evidence_artifacts":payload.get("evidence_artifacts",{}),
                           "stage_payload":payload,"ranking_or_selection":False},
                "output_artifacts":artifacts,"verifier_complete":True}
    except BackendStop as exc:
        _T4_ACTIVE_CONTEXT, _T4_ACTIVE_STATE = None, None
        if context.stage.source=="COURT" and not isinstance(exc,CourtAuthorityStop):
            exc=CourtAuthorityStop(str(exc),exc.detail)
        return _failure(context,services,state,exc)
    except Exception as exc:
        _T4_ACTIVE_CONTEXT, _T4_ACTIVE_STATE = None, None
        stop_cls=CourtAuthorityStop if context.stage.source=="COURT" else BackendStop
        return _failure(context,services,state,stop_cls(
            "untyped production backend implementation failure",
            {"exception_type":type(exc).__name__,"exception":str(exc)}))


if __name__=="__main__":
    if len(sys.argv)==3 and sys.argv[1]=="--fresh-replay":
        raise SystemExit(_fresh_replay_cli(Path(sys.argv[2])))
    raise SystemExit("production backend is not a standalone orchestrator")

__all__=["BACKEND_CONTRACT","run_stage"]
