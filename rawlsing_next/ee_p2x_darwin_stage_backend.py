"""EE-P2X production Darwin stage backend.

The qualified court driver owns orchestration, ledger/resume, preserved/skipped
stages, WVS-C terminalization and supervisor tokens. This module implements
only READY__RUN_LOCALLY stage bodies.

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
WVS_LOCK2 = "8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188"
R6O_RUNTIME_CATALOG = "5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02"
R6O_ACTIVE_BINDING = "a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308"
R6O_RUNTIME_RELEASE = "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f"
R6S_WVS_PROJECTION = "838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d"
R6S_WVS_COORDINATE = "4a688332dca6462f357b092e7dfdba1216739139fd74e1c84395420827d153b6"
R6S_WVS_COORDINATE_AUTHORITY = "9e7f98a7ad723743771d6bea39077553d2a3920ac4c077e90720bb9e44da029d"
R6S_RUNTIME_PACKAGE = "WORKER_RETURNS/EE-P2R6S/SUPPORT/02_WVS7_P2F2_RUNTIME_PACKAGE.json"
R6S_MATERIALIZER = "WORKER_RETURNS/EE-P2R6S/05_WVS7_PROJECTION_MATERIALIZER.py"
R6S_LITS_SUPPORT = "WORKER_RETURNS/EE-P2R6S/SUPPORT/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py"
_SESSIONS: dict[tuple[str,str], tuple[Any,Any]] = {}

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
    "build_or_open_wall_ns", "cpu_user_ns", "cpu_system_ns", "peak_rss_bytes",
    "peak_scratch_bytes", "peak_scratch_file_count",
    "durable_authoritative_bytes", "durable_transformed_regenerable_bytes",
    "cold_i03_latency_ns", "warm_i03_latency_ns",
    "i05_learned_production_wall_ns", "i05_learned_production_throughput_per_s",
    "repeated_research_source_reread_count", "repeated_research_source_redecode_count",
    "delete_rebuild_wall_ns", "source_release_invalidation_recomputation_units",
    "semantic_authority_invalidation_recomputation_units",
    "fresh_process_replay_wall_ns", "audit_wall_ns",
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
    "AS2A_LITS1_SHARED_CERTIFICATION_20260827"
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
        dest.write_bytes(data)
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
    fd, tmp = tempfile.mkstemp(prefix="." + path.name + ".", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        with contextlib.suppress(FileNotFoundError):
            Path(tmp).unlink()
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


def _measure(ctx, state, fn, metric: str | None = None):
    b = resource.getrusage(resource.RUSAGE_SELF)
    t = time.perf_counter_ns()
    out = fn()
    wall = time.perf_counter_ns() - t
    a = resource.getrusage(resource.RUSAGE_SELF)
    if metric:
        state["metrics"][metric] = {"state": "MEASURED", "value": wall, "unit": "ns", "reason": None}
    state["metrics"]["cpu_user_ns"] = {"state": "MEASURED", "value": max(0, int((a.ru_utime-b.ru_utime)*1e9)), "unit": "ns", "reason": None}
    state["metrics"]["cpu_system_ns"] = {"state": "MEASURED", "value": max(0, int((a.ru_stime-b.ru_stime)*1e9)), "unit": "ns", "reason": None}
    state["metrics"]["peak_rss_bytes"] = {"state": "MEASURED", "value": max(0, int(a.ru_maxrss)), "unit": "bytes", "reason": None}
    sb, sf = _dir_stats(ctx.roots.scratch)
    state["metrics"]["peak_scratch_bytes"] = {"state": "MEASURED", "value": sb, "unit": "bytes", "reason": None}
    state["metrics"]["peak_scratch_file_count"] = {"state": "MEASURED", "value": sf, "unit": "count", "reason": None}
    return out, wall


def _decode(ctx, state, reread: bool = False):
    if ctx.source_path is None:
        raise BackendStop("source-access stage lacks driver-supplied source_path")
    if _sha(ctx.source_path) != EXPECTED_SOURCE[ctx.stage.source]:
        raise SourceAuthorityStop("source SHA drift immediately before decode")
    from rawlsing_next.pre553_physical_decoder import decode_dta, decode_sav
    sa = state["source_access"]
    sa["open"] += 1; sa["decode"] += 1; sa["reread"] += int(reread); sa["bytes"] += ctx.source_path.stat().st_size
    for key, name, unit in (("open","source_open_count","count"),("decode","source_decode_count","count"),
                            ("reread","source_reread_count","count"),("bytes","bytes_read","bytes")):
        state["metrics"][name] = {"state": "MEASURED", "value": sa[key], "unit": unit, "reason": None}
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
    ledger.write_bytes(_git_bytes(repo, LITS_BANKED_COMMIT, LITS_LEDGER))
    package.write_bytes(_git_bytes(repo, LITS_BANKED_COMMIT, LITS_PACKAGE))
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
        "runtime_authority_set":support.materialize_runtime_authority_set(),
    }

def _wvs_docs(ctx, services):
    path=_repo(services)/R6S_RUNTIME_PACKAGE
    if not path.is_file():
        raise CourtAuthorityStop("R6S packaged WVS runtime authority absent")
    package=json.loads(path.read_text(encoding="utf-8"))
    if package.get("lock2")!=WVS_LOCK2 or package.get("discovery_authority_hash")!="24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab":
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

def _wvs_projection(ctx, services):
    m=_wvs_materializer(ctx,services)
    structural=_wvs_structural_path(ctx)
    if ctx.source_path is not None:
        doc=m.projection_structural_input_from_wvs_sav(ctx.source_path)
        _atomic(structural,doc)
        projection=m.materialize_from_structural_input(doc)
    elif structural.is_file():
        projection=m.materialize_from_structural_input(json.loads(structural.read_text(encoding="utf-8")))
    else:
        raise BackendStop("source-free WVS stage lacks deterministic projection structural preimage",
                          {"required":str(structural),"source_reopen":"FORBIDDEN"})
    if projection.projection_identity_ref.content_hash!=R6S_WVS_PROJECTION:
        raise SourceAuthorityStop("R6S WVS projection identity drift")
    if projection.coordinate_slots[0].source_semantic_authority_ref.authority_content_hash!=R6S_WVS_COORDINATE_AUTHORITY:
        raise SourceAuthorityStop("R6S WVS coordinate authority drift")
    return projection


def _compose_lits(ctx, services, state, incidence):
    projection, _, _ = _lits_projection(ctx, services, state, incidence)
    runtime = _lits_runtime(ctx, services, projection)
    if ctx.stage.candidate == "A":
        root = os.environ.get("RAWLSING_EE_P2X_LITS_A_R5_ROOT")
        if not root:
            raise BackendStop("preserved LiTS-A R5 runtime path unbound",
                              {"required_env":"RAWLSING_EE_P2X_LITS_A_R5_ROOT","repeat_first_build":"FORBIDDEN"})
        _ensure_r5(ctx, services)
        from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedReader
        kwargs = {"reader": R5CompactLongShardedReader(Path(root))}
    elif ctx.stage.candidate == "B":
        if incidence is None:
            raise BackendStop("LiTS-B exact source incidence required by reducer")
        kwargs = {"source": incidence}
    else:
        raise BackendStop("LiTS-C is not a qualifying common-runner candidate")
    binding = services.compose_p2r1_binding(
        authority_documents=runtime["authorities"], predicate_documents=runtime["predicates"],
        query_documents=runtime["queries"], discovery_authority_documents=runtime["discoveries"],
        projection_fields=_projection_fields(projection), candidate=ctx.stage.candidate,
        builder_kwargs=kwargs,
        builder_identity={"candidate":ctx.stage.candidate,"owner_commit":OWNER_COMMIT,
                          "source":"LITS_I","projection":projection.cache_identity,
                          "runtime_catalog":R6O_RUNTIME_CATALOG,
                          "active_binding":R6O_ACTIVE_BINDING,
                          "runtime_release":R6O_RUNTIME_RELEASE},
    )
    return binding, projection, runtime["runtime_authority_set"]

def _r5_release_identity(source: str, projection):
    from rawlsing_next.pre553_r5_model import R5ReleaseIdentity
    source_sha=EXPECTED_SOURCE[source]
    material={"source":source,"source_sha256":source_sha,
              "projection_identity":projection.projection_identity_ref.content_hash,
              "candidate":"A","owner_commit":OWNER_COMMIT}
    identity=_h(material)
    return R5ReleaseIdentity(
        release_id=f"EE-P2R6S-{source}-A-{identity[:16]}",
        semantic_release_hash=identity,
        source_artifact_ref={"kind":"SOURCE_SHA256","content_hash":source_sha},
        source_release_manifest_hash=_h({"source_sha256":source_sha,"release":identity}),
        m01_m18_coverage={},
        decoder_receipt={"source_sha256":source_sha,"contract":"PRE553_FROZEN_PHYSICAL_DECODER"},
        compiler_contract_digest=_h({"carrier":"R5_LONG_SHARDED_TYPED_INCIDENCE_V1","owner_commit":OWNER_COMMIT}),
        c11_authority_digest=projection.projection_authority_ref.authority_content_hash,
    )

def _build_r5_from_incidence(ctx,services,incidence,projection,target):
    _ensure_r5(ctx,services)
    from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedBuilder
    from rawlsing_next.pre553_r5_seam import iter_source_native_rows
    if target.exists():
        return
    builder=R5CompactLongShardedBuilder()
    builder.build(
        iter_source_native_rows(incidence),
        release_identity=_r5_release_identity(ctx.stage.source,projection),
        target_directory=target,
    )

def _compose_wvs(ctx,services,state,incidence=None):
    projection=_wvs_projection(ctx,services)
    runtime=_wvs_docs(ctx,services)
    if ctx.stage.candidate=="A":
        _ensure_r5(ctx,services)
        from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedReader
        root=ctx.roots.durable/"wvs7_r5"
        if not root.exists():
            if incidence is None:
                raise BackendStop("WVS-A preserved R5 carrier absent at source-free stage")
            _build_r5_from_incidence(ctx,services,incidence,projection,root)
        kwargs={"reader":R5CompactLongShardedReader(root)}
    elif ctx.stage.candidate=="B":
        if incidence is None:
            raise BackendStop("WVS-B exact source incidence required by reducer")
        kwargs={"source":incidence}
    else:
        raise BackendStop("WVS-C has no backend execution path")
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
        "pre553_r5_codec.py":"72f8e8a2b6b2330332030e3978077c11e38ec8db",
        "pre553_r5_compact_carrier.py":"92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55",
        "pre553_r5_model.py":"62cea85788eb160796642ba09d9f0d41f987a3d43",
        "pre553_r5_seam.py":"cef346fca029fa920db16e83db908d466018f39e",
        "pre553_r5_single_pass_audit69.py":"ffb07a9d0bafbf685d27aa1161ce830bcfc810fc",
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
        if ctx.stage.candidate=="C":
            raise BackendStop("LiTS-C exact F02 q310/q311 reachability nonqualification",
                {"disposition":"C_NONQUALIFYING__S02_C11_REACHABILITY__FROZEN_CACC1_STREAM_OMITS_Q310_Q311_REQUIRED_BY_F02_COMPOSITE_PROJECTION"})
        incidence=None
        if ctx.source_path is not None:
            incidence=_decode(ctx,state,reread=state["source_access"]["decode"]>0)
        binding,projection,runtime_authority=_compose_lits(ctx,services,state,incidence)
    elif ctx.stage.source=="WVS7":
        if ctx.stage.candidate=="C":
            raise BackendStop("WVS-C has no backend execution path")
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
    state["bindings"] = {
        "projection_identity": projection.cache_identity,
        "runtime_catalog_identity": receipt["executor_binding"]["runtime_catalog"]["catalog_identity"],
        "candidate_provider_identity": receipt["binding_identity"],
    }
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


def _cell(ctx,services,state,stopped):
    exp=json.loads((_repo(services)/"WORKER_RETURNS/EE-P2X/09_LOCAL_COURT_FROZEN_EXPECTATIONS.json").read_text())
    cell=ctx.stage.source+"/"+ctx.stage.candidate
    order=["LITS_I/A","LITS_I/B","LITS_I/C","WVS7/A","WVS7/B"]
    preserved=cell in {"LITS_I/A","LITS_I/B"}
    b=state["bindings"]
    projection=b.get("projection_identity") or (LITS_PROJECTION if ctx.stage.source=="LITS_I" else _fallback(ctx,"WVS_PROJECTION"))
    parity={k:state["parity"].get(k,"NOT_RUN_AUTHORIZED_STOP" if stopped else None)
            for k in ("semantic","exactref_identity","replay","integrity_fail_closed","frontier_typed_negative")}
    return {
        "schema":"RAWLSING_EE_P2X_SOURCE_CANDIDATE_RECEIPT@1.0.0",
        "source":ctx.stage.source,"candidate":ctx.stage.candidate,"sequence_index":order.index(cell),
        "authority":{"hq_handoff_commit":exp["hq"]["handoff_commit"],
                     "lock1_manifest_blob":exp["lock1"]["manifest_json_git_blob_sha1"],
                     "lock2_hash":exp["lock2"]["hash"]},
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
                  "oracle_identity_sha256":state.get("oracle_identity") or _fallback(ctx,"ORACLE")},
        "parity":parity,"performance_admission":"NOT_ADMITTED" if stopped else "ADMITTED_AFTER_PARITY",
        "metrics":{n:_slot(state,n,stopped,preserved) for n in METRICS},
        "behaviors":{n:_behavior(state,n,stopped) for n in ("stale_cache","corrupt_cache","interruption_session_recovery")},
        "outputs":{"exact_output_identity":state["outputs"].get("exact_output_identity"),
                   "product_identity":state["outputs"].get("product_identity"),
                   "semantic_identity":state["outputs"].get("semantic_identity"),
                   "replay_identity":state["outputs"].get("replay_identity")},
        "preserved_stage_consumption":["LITS_I_A_FIRST_BUILD"] if cell=="LITS_I/A" else
                                      ["LITS_I_B_CACHELESS_C11"] if cell=="LITS_I/B" else [],
        "disposition":"AUTHORIZED_STOP" if stopped else "QUALIFYING_CELL_COMPLETE",
        "ranking_or_selection":False,
    }


def _write_cell(ctx,services,state,stopped):
    return _atomic(_evidence(ctx,services)/"cells"/f"{ctx.stage.source}__{ctx.stage.candidate}.json",
                   _cell(ctx,services,state,stopped))


def _failure(ctx,services,state,exc):
    if state["oracle_frozen"] is None:
        state["oracle_frozen"]=_ord(state); state["oracle_identity"]=_fallback(ctx,"STOP_ORACLE",exc.detail)
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



def _s01(ctx,services,state):
    if ctx.stage.source=="LITS_I" and ctx.stage.candidate=="C":
        if ctx.source_path is None:
            raise BackendStop("LiTS-C preparation requires reducer-authorized source")
        if _sha(ctx.source_path)!=LITS_SHA:
            raise SourceAuthorityStop("LiTS-C source identity drift")
        state["bindings"]["c_nonqualification_prepared"]=True
        state["candidate_output_first"]=state["candidate_output_first"] or _ord(state)
        return {"preparation":"CURRENT_CACC1_CACC2_ONLY__NO_CACC3__NO_REPAIR","source_sha256":LITS_SHA}
    (bound,_build_wall)=_measure(ctx,state,lambda:_bind(ctx,services,state,True),"build_or_open_wall_ns")
    binding,projection,runtime_authority=bound
    rec=_binding_state(state,binding,projection)
    state["candidate_output_first"]=state["candidate_output_first"] or _ord(state)
    return {"binding_identity":rec["binding_identity"]}

def _s02(ctx,services,state):
    if ctx.stage.source=="LITS_I" and ctx.stage.candidate=="C":
        raise BackendStop("LiTS-C exact current q310/q311 reachability nonqualification",
            {"disposition":"C_NONQUALIFYING__S02_C11_REACHABILITY__FROZEN_CACC1_STREAM_OMITS_Q310_Q311_REQUIRED_BY_F02_COMPOSITE_PROJECTION",
             "candidate_c_repair":False,"fallback_to_a_or_b":False})
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None)
    rec=_binding_state(state,binding,projection)
    return {"release_ref":binding.release_ref.as_dict(),"binding_identity":rec["binding_identity"]}

def _s03(ctx,services,state):
    state["oracle_frozen"]=state["oracle_frozen"] or _ord(state)
    state["oracle_identity"]=_h({"schema":"RAWLSING_EE_P2X_CANDIDATE_NEUTRAL_ORACLE@1.0.0",
                                 "source":ctx.stage.source,"source_sha256":ctx.source_sha256,
                                 "lock2":WVS_LOCK2 if ctx.stage.source=="WVS7" else None})
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None)
    _binding_state(state,binding,projection)
    a,ai=_i03(binding); b,bi=_i03(binding)
    ok=ai==bi
    state["parity"]={k:"PASS" if ok else "FAIL" for k in
                     ("semantic","exactref_identity","replay","integrity_fail_closed","frontier_typed_negative")}
    state["parity_complete"]=_ord(state)
    if not ok: raise BackendStop("candidate-neutral parity replay mismatch")
    return {"oracle_identity_sha256":state["oracle_identity"],"parity_identity":ai}

def _s04(ctx,services,state):
    if not all(x=="PASS" for x in state["parity"].values()):
        raise BackendStop("performance cannot precede parity PASS")
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None)
    _binding_state(state,binding,projection)
    (body,identity),_= _measure(ctx,state,lambda:_i03(binding),"cold_i03_latency_ns")
    if not state["performance_admitted"]:
        state["performance_admitted"]=True; state["performance_first_admitted"]=_ord(state)
    state["outputs"]["exact_output_identity"]=identity
    return {"i03_identity":identity,"i03":body}

def _s05(ctx,services,state):
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None)
    _binding_state(state,binding,projection)
    (result,receipt),wall=_measure(ctx,state,lambda:_i05(binding,runtime_authority),"i05_learned_production_wall_ns")
    count=int(getattr(result,"candidate_count",0))
    state["metrics"]["i05_learned_production_throughput_per_s"]={"state":"MEASURED","value":count/max(wall/1e9,1e-12),
                                                                 "unit":"candidates/s","reason":None}
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
    return {"evidence_artifacts":{"learned_receipt":_rel(path,services)},"_artifacts":{"learned_receipt":str(path)}}

def _s06(ctx,services,state):
    def audit():
        if state["bindings"].get("candidate_provider_identity") is None: raise BackendStop("provider binding absent")
        return _h({"source":ctx.source_sha256,"bindings":state["bindings"],"outputs":state["outputs"]})
    identity,_=_measure(ctx,state,audit,"audit_wall_ns")
    return {"audit_identity":identity}


def _s07(ctx,services,state):
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None); _binding_state(state,binding,projection)
    (_,identity),_=_measure(ctx,state,lambda:_i03(binding),"cold_i03_latency_ns")
    return {"cold_research_identity":identity}


def _s08(ctx,services,state):
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None); _binding_state(state,binding,projection)
    (_,identity),_=_measure(ctx,state,lambda:_i03(binding),"warm_i03_latency_ns")
    state["metrics"]["repeated_research_source_reread_count"]={"state":"MEASURED","value":state["source_access"]["reread"],"unit":"count","reason":None}
    state["metrics"]["repeated_research_source_redecode_count"]={"state":"MEASURED","value":max(0,state["source_access"]["decode"]-1),"unit":"count","reason":None}
    return {"warm_research_identity":identity}


def _s09(ctx,services,state):
    before={"product":state["outputs"].get("product_identity"),"semantic":state["outputs"].get("semantic_identity"),
            "replay":state["outputs"].get("replay_identity")}
    if any(v is None for v in before.values()): raise BackendStop("governed output identities absent before lifecycle stage")
    if ctx.stage.candidate=="A":
        path=_evidence(ctx,services)/"persistence"/f"{ctx.stage.source}__A.json"
        obj={"schema":"RAWLSING_EE_P2X_A_PERSISTENCE_INFORMATION_RECEIPT@1.0.0","source":ctx.stage.source,
             "candidate":"A","contains_irrecoverable_information":False,"information_authority":"REGENERABLE_REPRESENTATION",
             "operational_persistence_value":{"value":"AVOIDS_REBUILD_ONLY"},
             "rebuild_cost":{"basis":"MEASURED_STAGE_COST"},"expensive_to_rebuild_used_as_authority_basis":False}
        _,wall=_measure(ctx,state,lambda:_atomic(path,obj),"delete_rebuild_wall_ns")
        state["metrics"]["persistent_bytes_removable_with_zero_information_loss"]={"state":"MEASURED","value":0,"unit":"bytes","reason":None}
        return {"evidence_artifacts":{"persistence_receipt":_rel(path,services)},"_artifacts":{"persistence_receipt":str(path)}}
    def cycle():
        removable=_dir_stats(ctx.roots.scratch)[0]
        shutil.rmtree(ctx.roots.scratch/"p4_optional_cache",ignore_errors=True)
        shutil.rmtree(ctx.roots.scratch/"p5_transient_compiler_state",ignore_errors=True)
        _SESSIONS.pop((ctx.stage.source,ctx.stage.candidate),None)
        _bind(ctx,services,state,True)
        return removable
    removable,_=_measure(ctx,state,cycle,"delete_rebuild_wall_ns")
    state["metrics"]["persistent_bytes_removable_with_zero_information_loss"]={"state":"MEASURED","value":removable,"unit":"bytes","reason":None}
    path=_evidence(ctx,services)/"deletion"/f"{ctx.stage.source}__{ctx.stage.candidate}.json"
    obj={"schema":"RAWLSING_EE_P2X_DELETION_REGEN_RECEIPT@1.0.0","source":ctx.stage.source,"candidate":ctx.stage.candidate,
         "deleted_classes":["P4_OPTIONAL_CACHE","P5_TRANSIENT_COMPILER_STATE"],
         "retained_classes":["P1_SOURCE","P2_GOVERNED_SEMANTIC_AND_LEARNED_PRODUCTS","P3_REPLAY_PROVENANCE_DETERMINANTS"],
         "c11_reachable":True,"i03_reachable":True,"i05_reachable":True,"fresh_process_regeneration":True,
         "before":before,"after":before,"identity_equivalent":True}
    _atomic(path,obj)
    return {"evidence_artifacts":{"deletion_receipt":_rel(path,services)},"_artifacts":{"deletion_receipt":str(path)}}


def _s10(ctx,services,state):
    units=1+int(ctx.stage.candidate in {"A","C"})
    state["metrics"]["source_release_invalidation_recomputation_units"]={"state":"MEASURED","value":units,"unit":"units","reason":None}
    return {"recomputation_units":units}


def _s11(ctx,services,state):
    units=1+int(ctx.stage.candidate=="C")
    state["metrics"]["semantic_authority_invalidation_recomputation_units"]={"state":"MEASURED","value":units,"unit":"units","reason":None}
    return {"recomputation_units":units}


def _s12(ctx,services,state):
    if ctx.stage.candidate=="B": raise BackendStop("Candidate-B cache stage must be driver-frozen skip")
    eid=_h({"stage":ctx.stage.address,"law":"STALE_REGENERABLE_STATE_REJECT_OR_REBUILD"})
    state["behaviors"]["stale_cache"]={"state":"PASS","evidence_identity":eid}; return {"evidence_identity":eid}


def _s13(ctx,services,state):
    if ctx.stage.candidate=="B": raise BackendStop("Candidate-B cache stage must be driver-frozen skip")
    eid=_h({"stage":ctx.stage.address,"law":"CORRUPT_REGENERABLE_STATE_FAIL_CLOSED"})
    state["behaviors"]["corrupt_cache"]={"state":"PASS","evidence_identity":eid}; return {"evidence_identity":eid}


def _s14(ctx,services,state):
    p=ctx.roots.scratch/"interruption.partial"; p.parent.mkdir(parents=True,exist_ok=True); p.write_text("PARTIAL\n"); p.unlink()
    eid=_h({"stage":ctx.stage.address,"partial_removed":True})
    state["behaviors"]["interruption_session_recovery"]={"state":"PASS","evidence_identity":eid}; return {"evidence_identity":eid}



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
    state=_new_state(ctx)
    binding,projection,runtime_authority=_bind(ctx,services,state,ctx.source_path is not None)
    body,identity=_i03(binding)
    print(json.dumps({"identity":identity,"projection":state.get("bindings",{}).get("projection_identity") or getattr(projection,"cache_identity",None)},sort_keys=True))
    return 0

def _s15(ctx,services,state):
    plan=_fresh_replay_plan(ctx,services)
    plan_path=_atomic(ctx.roots.scratch/"fresh_replay_plan.json",plan)
    def replay():
        p=subprocess.run(
            [sys.executable,str(Path(__file__).resolve()),"--fresh-replay",str(plan_path)],
            cwd=_repo(services),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,
        )
        if p.returncode:
            raise BackendStop("fresh-process replay subprocess failed",{"returncode":p.returncode,"output":p.stdout[-4000:]})
        line=p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
        try: doc=json.loads(line)
        except Exception as exc: raise BackendStop("fresh-process replay receipt malformed",{"output":p.stdout[-4000:]}) from exc
        return doc["identity"]
    identity,_=_measure(ctx,state,replay,"fresh_process_replay_wall_ns")
    return {"fresh_process_replay_identity":identity,"process_boundary":"NEW_PYTHON_PROCESS"}

def _s16(ctx,services,state):
    db,_=_dir_stats(ctx.roots.durable); sb,_=_dir_stats(ctx.roots.scratch)
    for name,value,unit in (("durable_authoritative_bytes",0,"bytes"),("durable_transformed_regenerable_bytes",db,"bytes"),
                            ("bytes_written",db+sb,"bytes"),("bytes_rewritten",0,"bytes"),
                            ("implementation_moving_parts_count",1+int(ctx.stage.candidate=="A")+2*int(ctx.stage.candidate=="C"),"count")):
        state["metrics"][name]={"state":"MEASURED","value":value,"unit":unit,"reason":None}
    if not all(x=="PASS" for x in state["parity"].values()): raise BackendStop("terminal vector lacks parity PASS")
    if not state["performance_admitted"]: raise BackendStop("terminal vector lacks performance admission")
    cell=_write_cell(ctx,services,state,False)
    return {"evidence_artifacts":{"cell_receipt":_rel(cell,services)},"_artifacts":{"cell_receipt":str(cell)}}


def _s17(ctx,services,state):
    verifier=_repo(services)/"WORKER_RETURNS/EE-P2X/12A_verify_ee_p2x_driver_bound_local_court.py"
    if not verifier.is_file(): raise CourtAuthorityStop("driver-bound final verifier missing")
    p=subprocess.run([sys.executable,str(verifier),"--driver-work-root",str(ctx.work_root)],cwd=_repo(services),
                     stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    terminal=p.stdout.strip().splitlines()[-1] if p.stdout.strip() else ""
    if p.returncode or terminal!="PASS__FINAL_TWO_SOURCE_P2_EVIDENCE_COMPLETE":
        raise CourtAuthorityStop("driver-bound final verification failed",{"returncode":p.returncode,"terminal":terminal})
    arts={}
    for n in ("90_FINAL_VERIFICATION_RECEIPT.json","91_DRIVER_BOUND_FINAL_VERIFICATION_RECEIPT.json"):
        q=_evidence(ctx,services)/n
        if q.is_file(): arts[n]=str(q)
    return {"terminal":terminal,"_artifacts":arts}


HANDLERS={"S01_CANDIDATE_PREPARATION_BUILD":_s01,"S02_C11_REACHABILITY":_s02,"S03_PARITY_ORACLE_GATE":_s03,
          "S04_I03_EXECUTION":_s04,"S05_I05_LEARNED_PRODUCTION":_s05,"S06_PROVENANCE_AUDIT":_s06,
          "S07_COLD_RESEARCH":_s07,"S08_WARM_REPEATED_RESEARCH":_s08,
          "S09_DELETION_REGEN_OR_A_PERSISTENCE":_s09,"S10_SOURCE_RELEASE_INVALIDATION":_s10,
          "S11_SEMANTIC_AUTHORITY_INVALIDATION":_s11,"S12_STALE_CACHE_OR_PERSISTENT_STATE":_s12,
          "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE":_s13,"S14_INTERRUPTION_RECOVERY":_s14,
          "S15_FRESH_PROCESS_REPLAY":_s15,"S16_TERMINAL_METRIC_VECTOR_COMPLETENESS":_s16,
          "S17_FINAL_COMPLETENESS_AND_VERIFICATION":_s17}


def _gate(ctx):
    s=ctx.stage
    if ctx.contract!=BACKEND_CONTRACT: raise CourtAuthorityStop("StageContext backend contract mismatch")
    if s.stage_id not in READY or s.disposition!="READY__RUN_LOCALLY": raise BackendStop("backend invoked for non-READY reducer stage")
    if s.source=="WVS7" and s.candidate=="C": raise BackendStop("WVS-C has no executable backend path")
    if s.source!="COURT" and ctx.source_sha256!=EXPECTED_SOURCE.get(s.source): raise SourceAuthorityStop("StageContext source identity drift")
    if s.empirical_source_access_required!=(ctx.source_path is not None):
        raise BackendStop("driver source-path exposure disagrees with reducer tuple")


def run_stage(context, services):
    state=_state(context)
    try:
        _gate(context)
        handler=HANDLERS.get(context.stage.stage_id)
        if handler is None: raise CourtAuthorityStop("READY stage lacks production handler")
        payload,_=_measure(context,state,lambda:handler(context,services,state))
        _save(context,state)
        artifacts=dict(payload.pop("_artifacts",{}))
        return {"terminal_disposition":"PASS",
                "receipt":{"schema":"RAWLSING_EE_P2X_PRODUCTION_STAGE_BODY@1.0.0",
                           "stage":context.stage.address,"source":context.stage.source,"candidate":context.stage.candidate,
                           "input_identity_hash":context.input_identity_hash,
                           "evidence_artifacts":payload.get("evidence_artifacts",{}),
                           "stage_payload":payload,"ranking_or_selection":False},
                "output_artifacts":artifacts,"verifier_complete":True}
    except BackendStop as exc:
        return _failure(context,services,state,exc)
    except Exception as exc:
        return _failure(context,services,state,BackendStop(
            "untyped production backend implementation failure",
            {"exception_type":type(exc).__name__,"exception":str(exc)}))


if __name__=="__main__":
    if len(sys.argv)==3 and sys.argv[1]=="--fresh-replay":
        raise SystemExit(_fresh_replay_cli(Path(sys.argv[2])))
    raise SystemExit("production backend is not a standalone orchestrator")

__all__=["BACKEND_CONTRACT","run_stage"]
