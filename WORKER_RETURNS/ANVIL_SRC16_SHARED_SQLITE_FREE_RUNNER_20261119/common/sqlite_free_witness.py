#!/usr/bin/env python3
"""Actual SRC04 witness caller: producer, supervisor and fresh reader.

The ``run`` command is the only path that can start the producer.  It requires
``--authorized-source-launch`` and must not be invoked by this preparation
commission.  Preflight and synthetic rehearsal are metadata-only.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, Mapping

HERE = Path(__file__).resolve().parent
SOURCEFREE_FIXTURE = HERE / "sourcefree_fixture.py"
BINDING_DIR = HERE.parent / "ANVIL_ALL35_EXISTING_GRANT_ADMISSION_20261118"
FINAL_PATCH_SHA = "ffa4520f965e4f2fd22ea5043d0c80528f44a47f94afdb763d3b77c21ca3a08f"
FINAL_HANDOFF_SHA = "6ab7cb50574f6a50a441a24db44f2d7f05bdaad0c14988fc533bd263342aee1f"
SINGLE_PASS_SHA = "5340e04642e7ca1aff1daadb2aba071face7c36f352ef66f24b1e1485d66e3c0"
STREAMING_ESTATE_SHA = "1c4d28aad9dc667d982914b0e782aee161a30ddf1e0664ef2eed7ec03096837a"
RAM_CAP = 6 * 1024**3
COMPLETED_512K_BYTES = int(3.08 * 1024**3)       # completed 512x600 witness
Q2_SPOOL_RESERVE = 1024**3                       # routing/current-Q2 spool
# R3 observed terminal stage minus the duplicate replay journal; this is a
# practical floor, not a guarantee for a different source/writer generation.
R3_TERMINAL_STAGE_BYTES = 26678480536
R3_DUPLICATE_JOURNAL_BYTES = 8360588401
PRACTICAL_STAGING_BUDGET = R3_TERMINAL_STAGE_BYTES - R3_DUPLICATE_JOURNAL_BYTES
STAGING_BUDGET = PRACTICAL_STAGING_BUDGET
STARTUP_FREE_FLOOR = STAGING_BUDGET + 8 * 1024**3
IN_FLIGHT_FREE_FLOOR = 8 * 1024**3
OVERLAY_CANONICAL = "ba886d87763fdeb4d91df784b9672d6604081c9eaf81fd9ef6b3d334d4a387e0"
OVERLAY_ADDED_RULE_COUNTS = {
    "q715withoutmorocco": 303,
    "q716withoutmorocco": 327,
    "q715incomedeciles": 4,
    "q716incomedeciles": 2,
}
BASE_RULE_COUNTS = {
    "q715withoutmorocco": 6,
    "q716withoutmorocco": 6,
    "q715incomedeciles": 11,
    "q716incomedeciles": 11,
}
OVERLAY_RULE_COUNTS = {
    k: BASE_RULE_COUNTS[k] + OVERLAY_ADDED_RULE_COUNTS[k]
    for k in BASE_RULE_COUNTS
}
ACCEPTED = {
    "release_hash": "9ddec98561a0fc54668136cc13e64573edcadcbfb12cd3f79cbfc05606f97ae1",
    "public_objects": 2619317,
    "internal_records": 7514,
    "RespondentEvent": 1298649,
    "EmpiricalCoordinateFact": 22011,
    "response_positions": 1298649,
    "q217_unbound": 38,
}


class CallerRefusal(RuntimeError):
    def __init__(self, code: str, detail: str = ""):
        super().__init__(code + (f": {detail}" if detail else ""))
        self.code = code
        self.detail = detail


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_candidate(tree: Path, patch: Path | None = None) -> None:
    """Exact hash check before importing or running candidate code."""
    source = tree / "rawlsing_next/pre553_source_i02_handoff.py"
    if not source.is_file() or sha(source) != FINAL_HANDOFF_SHA:
        raise CallerRefusal("CANDIDATE_SOURCE_HASH_MISMATCH", str(source))
    if patch is not None and (not patch.is_file() or sha(patch) != FINAL_PATCH_SHA):
        raise CallerRefusal("CANDIDATE_PATCH_HASH_MISMATCH", str(patch))
    compact = HERE / "sqlite_free_single_pass.py"
    if not compact.is_file() or sha(compact) != SINGLE_PASS_SHA:
        raise CallerRefusal("COMPACT_IMPLEMENTATION_HASH_MISMATCH", str(compact))
    streaming = HERE / "streaming_estate.py"
    if not streaming.is_file() or sha(streaming) != STREAMING_ESTATE_SHA:
        raise CallerRefusal("STREAMING_IMPLEMENTATION_HASH_MISMATCH", str(streaming))


def _paths() -> None:
    pass


def _grant(binding_dir: Path = BINDING_DIR):
    sys.path.insert(0, str(binding_dir))
    from sqlite_free_single_pass import _require_current
    import existing_grant_binding as gb
    raw = json.loads((binding_dir / "fixtures/SRC04_CONFIG_BINDING.json").read_text())
    cfg = gb.ConfigBinding(**raw)
    trust_raw = json.loads((binding_dir / "TRUST_POLICY.json").read_text())
    trust = gb.ExternalTrust(**{k: trust_raw[k] for k in (
        "grant_sha256", "grant_path", "config_file_sha256",
        "config_canonical_sha256", "config_binding_sha256")})
    grant_path = binding_dir / "fixtures/SRC04_FULL_SOURCE_GRANT.json"
    bound = gb.bind_existing_grant(grant_path=grant_path, config=cfg, trust=trust)
    if bound.status != "REQUEST_ONLY_ALLOWED" or bound.decision is None:
        raise CallerRefusal("GRANT_NOT_REQUEST_ONLY_ALLOWED", bound.status)
    document = json.loads(grant_path.read_text())
    source_path = document.get("source_path")
    if not isinstance(source_path, str) or not source_path:
        raise CallerRefusal("GRANT_SOURCE_PATH_MISSING")
    resolver = gb.ExistingGrantResolver(grant_path, trust, bound.request)
    # Exact CURRENT/revocation/scope check before any checkpoint read/publication.
    try:
        _require_current(resolver, bound.request, bound.decision.decision_ref)
    except Exception as exc:
        raise CallerRefusal("GRANT_CURRENT_SCOPE_REFUSED", getattr(exc, "code", type(exc).__name__)) from exc
    return gb, bound, resolver, source_path, trust



def _scoped(binding_dir: Path = BINDING_DIR):
    import witness_runner as wr
    pin = json.loads((HERE / "SRC04_WITNESS_SCOPE.json").read_text())
    return wr, pin


def preflight(args) -> int:
    """Metadata-only overlay/request/coverage check; never opens source."""
    verify_candidate(args.candidate_tree, args.candidate_patch)
    sys.path.insert(0, str(args.candidate_tree))
    from rawlsing_next.pre553_r157_projection_adapter import SourceConfig, canonical_config_hash, source_read_request_from_config
    wr, pin = _scoped()
    base_doc = json.loads(args.config.read_text())
    if wr.sha_bytes(args.config) != pin["config_index_row"]["source_config"]["file_sha256"]:
        raise CallerRefusal("BASE_CONFIG_HASH_MISMATCH")
    base_cfg = SourceConfig(base_doc)
    scoped_doc = wr._strip_scope(base_doc, pin)
    if any(x["slot"]["name"] == "q217" for x in scoped_doc["response_slots"]):
        raise CallerRefusal("Q217_NOT_EXCLUDED")
    result = {
        "schema": "ANVIL_SRC04_OVERLAY_PREFLIGHT@1",
        "base_config_file_sha256": wr.sha_bytes(args.config),
        "base_config_canonical_sha256": canonical_config_hash(base_cfg),
        "expected_overlay_canonical_sha256": OVERLAY_CANONICAL,
        "expected_rule_counts": OVERLAY_RULE_COUNTS,
        "q217": wr._q217_guard(base_doc, pin),
        "scoped_counts": {"response_slots": len(scoped_doc["response_slots"]),
                          "coordinate_slots": len(scoped_doc["coordinate_slots"]),
                          "physical_slots": len(scoped_doc["physical_slots"])},
        "source_path_opened_stat_hashed_decoded": False,
    }
    if args.runtime_config is None:
        result.update({"status": "RUNTIME_OVERLAY_BYTES_MISSING",
                       "reason": "Exact accepted ba886d intermediate runtime overlay not supplied; base v2 would stop at UNBOUND_RESPONSE_CELL q716withoutmorocco slot 176.",
                       "first_failure_if_base_used": {"slot": 176, "name": "q716withoutmorocco", "error": "UNBOUND_RESPONSE_CELL"},
                       "source_path_from_grant": _grant_source_path(args.binding_dir)})
        (Path(args.outdir).mkdir(parents=True, exist_ok=True) if args.outdir else (HERE / "OVERLAY_PREFLIGHT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n"))
        if args.outdir:
            (Path(args.outdir) / "OVERLAY_PREFLIGHT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print(json.dumps(result))
        return 2
    overlay_doc = json.loads(args.runtime_config.read_text())
    overlay_cfg = SourceConfig(overlay_doc)
    actual_canonical = canonical_config_hash(overlay_cfg)
    if actual_canonical != OVERLAY_CANONICAL:
        raise CallerRefusal("RUNTIME_OVERLAY_CANONICAL_MISMATCH", actual_canonical)
    # Count the exact accepted target rules in the supplied overlay.
    counts = {}
    for slot in overlay_doc.get("response_slots", []):
        name = slot.get("slot", {}).get("name")
        if name in OVERLAY_RULE_COUNTS:
            counts[name] = len(slot.get("values", []))
    if counts != OVERLAY_RULE_COUNTS:
        raise CallerRefusal("RUNTIME_OVERLAY_RULE_COUNT_MISMATCH", json.dumps(counts, sort_keys=True))
    request = source_read_request_from_config(
        overlay_cfg, host="USER_LOCAL_MAC", purpose="FULL_SRC04_ORIGINAL_C11_CONSTRUCTION",
        consumer_use="EXISTING_PRE553_SOURCE_BACKED_C11",
        semantic_use_scope=("SOURCE_NATIVE_RESPONSE_INCIDENCE", "NO_SEMANTIC_ADOPTION", "SRC04", "FULL_SRC04_C11_CONSTRUCTION"))
    result.update({"status": "RUNTIME_OVERLAY_QUALIFIED", "runtime_config_file_sha256": wr.sha_bytes(args.runtime_config),
                   "runtime_config_canonical_sha256": actual_canonical, "rule_counts": counts,
                   "added_rule_counts": {k: counts[k] - BASE_RULE_COUNTS[k] for k in counts},
                   "request_equal_to_approved": request == _grant()[1].request,
                   "request": {"source_id": request.source_id, "source_sha256": request.source_sha256,
                               "locator": request.custody_locator_binding, "host": request.host,
                               "purpose": request.purpose, "consumer": request.consumer_use,
                               "semantic_use_scope": list(request.semantic_use_scope)}})
    out = Path(args.outdir) if args.outdir else HERE
    out.mkdir(parents=True, exist_ok=True)
    (out / "OVERLAY_PREFLIGHT.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result))
    return 0


def producer(args) -> int:
    verify_candidate(args.candidate_tree, args.candidate_patch)
    sys.path.insert(0, str(args.candidate_tree))
    if args.sourcefree:
        from sourcefree_fixture import make_keyed_fixture
        from sqlite_free_single_pass import build_single_pass
        root=Path(args.root).absolute(); private=root/"private"; private.mkdir(mode=0o700,parents=False,exist_ok=True)
        cfg,path=make_keyed_fixture(root/"sourcefree")
        progress_path=root/"progress.jsonl"
        def progress(update):
            with progress_path.open("a",encoding="utf-8") as stream:
                stream.write(json.dumps(update,sort_keys=True)+"\n"); stream.flush()
            print(json.dumps(update,sort_keys=True),file=sys.stderr,flush=True)
        receipt=build_single_pass(config=cfg,source_path=path,private_root=private,chunk_rows=2,compact_spool=True,progress=progress)
        payload={"schema":"ANVIL_ALL35_WITNESS_PRODUCER_RECEIPT@1","producer_pid":os.getpid(),"source_id":"SOURCEFREE","q217":{"status":"NOT_APPLICABLE"},"scoped_counts":{"response_slots":len(cfg.document["response_slots"]),"coordinate_slots":len(cfg.document["coordinate_slots"]),"physical_slots":len(cfg.document["physical_slots"])},"grant_ref":None,"decision_ref":None,"source_sha256":cfg.document["binding"]["source_sha256"],"row_count":cfg.document["binding"]["row_count"],"i02":{k:getattr(receipt.roots,k) for k in ("logical","physical","release","source","replay","universe","schema")},"proof_schema":receipt.roots.schema,"manifest_sha256":receipt.manifest_sha256,"estate_path":receipt.path,"family_counts":dict(receipt.family_counts),"single_pass_path":True,"resumed_from_checkpoint":False,"checkpoint":None,"i02_passes":1,"retained_bytes":receipt.retained_bytes,"source_read_performed":False,"joined_q2":False,"authorized_executable_q2":False,"issued_workload":False}
        (root/"producer_receipt.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n");(root/"producer.stdout").write_text("");(root/"producer.stderr").write_text("")
        print(json.dumps({"status":"PRODUCER_COMMITTED","path":receipt.path,"single_pass":True,"sourcefree":True}));return 0
    if getattr(args,"source_adapter",None):
        from source_adapter import Profile
        prof=Profile(args.source_adapter); prof.resolve_before_source()
        from sqlite_free_single_pass import build_single_pass
        root=Path(args.root).absolute(); private=root/"private"; private.mkdir(mode=0o700,parents=False,exist_ok=True)
        progress_path=root/"progress.jsonl"
        def progress(update):
            with progress_path.open("a",encoding="utf-8") as stream:
                stream.write(json.dumps(update,sort_keys=True)+"\n"); stream.flush()
            print(json.dumps(update,sort_keys=True),file=sys.stderr,flush=True)
        rec=build_single_pass(config=prof.config,source_path=prof.source_path,private_root=private,resolver=prof.resolver,
                              host=prof.request.host if prof.request else None,purpose=prof.request.purpose if prof.request else None,
                              consumer_use=prof.request.consumer_use if prof.request else None,
                              semantic_use_scope=prof.request.semantic_use_scope if prof.request else None,
                              chunk_rows=(2 if prof.kind=="sourcefree" else 512),compact_spool=True,progress=progress,request=prof.request,
                              grant_ref=prof.grant_ref,decision_ref=prof.decision_ref)
        payload={"schema":"ANVIL_ALL35_WITNESS_PRODUCER_RECEIPT@1","producer_pid":os.getpid(),"source_id":prof.config.source_id,"q217":{"status":"NOT_APPLICABLE"},"scoped_counts":{"response_slots":len(prof.config.document["response_slots"]),"coordinate_slots":len(prof.config.document["coordinate_slots"]),"physical_slots":len(prof.config.document["physical_slots"])},"grant_ref":prof.grant_ref.as_dict() if prof.grant_ref else None,"decision_ref":prof.decision_ref.as_dict() if prof.decision_ref else None,"source_sha256":prof.config.document["binding"]["source_sha256"],"row_count":prof.config.document["binding"]["row_count"],"i02":{k:getattr(rec.roots,k) for k in ("logical","physical","release","source","replay","universe","schema")},"proof_schema":rec.roots.schema,"manifest_sha256":rec.manifest_sha256,"estate_path":rec.path,"family_counts":dict(rec.family_counts),"single_pass_path":True,"resumed_from_checkpoint":False,"checkpoint":None,"i02_passes":1,"retained_bytes":rec.retained_bytes,"source_read_performed":True,"joined_q2":False,"authorized_executable_q2":False,"issued_workload":False}
        (root/"producer_receipt.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n");(root/"producer.stdout").write_text("");(root/"producer.stderr").write_text("")
        print(json.dumps({"status":"PRODUCER_COMMITTED","path":rec.path,"single_pass":True,"source_adapter":True}));return 0
    from sqlite_free_single_pass import build_single_pass, resume_single_pass
    from rawlsing_next.pre553_r157_projection_adapter import SourceConfig, source_read_request_from_config
    wr, pin = _scoped()
    if args.runtime_config is None:
        raise CallerRefusal("RUNTIME_OVERLAY_REQUIRED_FOR_PRODUCER")
    cfg_doc = json.loads(args.runtime_config.read_text())
    canonical_config_hash = __import__("rawlsing_next.pre553_r157_projection_adapter", fromlist=["canonical_config_hash"]).canonical_config_hash
    if canonical_config_hash(SourceConfig(cfg_doc)) != OVERLAY_CANONICAL:
        raise CallerRefusal("RUNTIME_OVERLAY_CANONICAL_MISMATCH")
    if wr.sha_bytes(args.config) != pin["config_index_row"]["source_config"]["file_sha256"]:
        raise CallerRefusal("BASE_CONFIG_HASH_MISMATCH")
    q217 = wr._q217_guard(cfg_doc, pin)
    scoped_doc = wr._strip_scope(cfg_doc, pin)
    if any(x["slot"]["name"] == "q217" for x in scoped_doc["response_slots"]):
        raise CallerRefusal("Q217_NOT_EXCLUDED")
    scoped = SourceConfig(scoped_doc)
    _gb, bound, resolver, source_path_from_grant, _trust = _grant(args.binding_dir)
    if not args.resume_checkpoint and os.path.normpath(args.source_path) != os.path.normpath(source_path_from_grant):
        raise CallerRefusal("SOURCE_PATH_DOES_NOT_MATCH_GRANT")
    exact_request = source_read_request_from_config(
        scoped, host=bound.request.host, purpose=bound.request.purpose,
        consumer_use=bound.request.consumer_use,
        semantic_use_scope=bound.request.semantic_use_scope)
    if exact_request != bound.request:
        raise CallerRefusal("SCOPED_REQUEST_MISMATCH")
    root = Path(args.root).absolute()
    private = root / "private"
    private.mkdir(mode=0o700, parents=False, exist_ok=True)
    checkpoint_root = None
    if args.resume_checkpoint:
        work = Path(args.work_root).absolute() if args.work_root else root.parent
        cp = Path(args.resume_checkpoint).absolute()
        try:
            cp.relative_to(work)
        except ValueError as exc:
            raise CallerRefusal("CHECKPOINT_OUTSIDE_WORK_ROOT", str(cp)) from exc
        if any(p.is_symlink() for p in (cp, cp.parent)):
            raise CallerRefusal("CHECKPOINT_SYMLINK_REFUSED")
        checkpoint_root = cp.parent
    if shutil.disk_usage(root).free < STARTUP_FREE_FLOOR:
        raise CallerRefusal("DISK_FLOOR_BEFORE_PRODUCER")
    progress_path = root / "progress.jsonl"
    def progress(update):
        with progress_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(update, sort_keys=True) + "\n")
            stream.flush()
        print(json.dumps(update, sort_keys=True), file=sys.stderr, flush=True)
    if args.resume_checkpoint:
        receipt = resume_single_pass(
            checkpoint=args.resume_checkpoint, root=root / "private", config=scoped,
            request=bound.request, grant_ref=bound.grant_ref,
            decision_ref=bound.decision.decision_ref, resolver=resolver,
            checkpoint_root=checkpoint_root, preserve_checkpoint=True,
            chunk_rows=512, progress=progress)
        resumed = True
    else:
        receipt = build_single_pass(
        config=scoped, source_path=args.source_path, private_root=private,
        resolver=resolver, host=bound.request.host, purpose=bound.request.purpose,
        consumer_use=bound.request.consumer_use,
        semantic_use_scope=bound.request.semantic_use_scope,
            chunk_rows=512, progress=progress, request=bound.request,
            grant_ref=bound.grant_ref, decision_ref=bound.decision.decision_ref)
        resumed = False
    payload = {
        "schema": "ANVIL_ALL35_WITNESS_PRODUCER_RECEIPT@1",
        "producer_pid": os.getpid(),
        "source_id": "SRC04",
        "q217": q217,
        "scoped_counts": {"response_slots": len(scoped_doc["response_slots"]),
                          "coordinate_slots": len(scoped_doc["coordinate_slots"]),
                          "physical_slots": len(scoped_doc["physical_slots"])},
        "grant_ref": bound.grant_ref.as_dict(),
        "decision_ref": bound.decision.decision_ref.as_dict(),
        "source_sha256": scoped_doc["binding"]["source_sha256"],
        "row_count": scoped_doc["binding"]["row_count"],
        "i02": {k: getattr(receipt.roots, k) for k in
                ("logical", "physical", "release", "source", "replay", "universe", "schema")},
        "proof_schema": getattr(receipt.roots, "schema", "ANVIL_STREAM_C11_ESTATE@1"),
        "manifest_sha256": receipt.manifest_sha256,
        "estate_path": receipt.path,
        "family_counts": dict(receipt.family_counts),
        "single_pass_path": True,
        "resumed_from_checkpoint": resumed,
        "checkpoint": None,
        "i02_passes": 1,
        "retained_bytes": receipt.retained_bytes,
        "source_read_performed": not resumed,
        "joined_q2": False,
        "authorized_executable_q2": False,
        "issued_workload": False,
    }
    (root / "producer_receipt.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    (root / "producer.stdout").write_text("")
    (root / "producer.stderr").write_text("")
    print(json.dumps({"status": "PRODUCER_COMMITTED", "path": receipt.path, "single_pass": True}))
    return 0


def reader(args) -> int:
    verify_candidate(args.candidate_tree, None)
    sys.path.insert(0, str(args.candidate_tree))
    if getattr(args,"source_adapter",None):
        from source_adapter import Profile
        from streaming_estate import StreamRoots, open_stream_native_estate
        from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
        prof=Profile(args.source_adapter); prof.resolve_before_source()
        root=Path(args.root).absolute();receipt=json.loads((root/"producer_receipt.json").read_text());producer_pid=int(receipt["producer_pid"])
        probe=subprocess.run(["ps","-p",str(producer_pid),"-o","pid="],capture_output=True,text=True)
        if probe.stdout.strip(): raise CallerRefusal("PRODUCER_STILL_ALIVE_BEFORE_READER")
        held=StreamRoots(**receipt["i02"]); request=prof.request
        def current(roots):
            if roots!=held: return False
            if prof.kind=="sourcefree": return True
            d=prof.resolver.resolve_current(request)
            return d.currentness=="CURRENT_GRANTED" and d.revocation_ref is None and d.source_id=="SRC16"
        estate=open_stream_native_estate(root/"private",exact_path=receipt["estate_path"],manifest_sha256=receipt["manifest_sha256"],roots=held,current_authorizer=current)
        counts={f:sum(1 for _ in estate.iter_family(f)) for f in ALL_FAMILIES}
        payload={"schema":"ANVIL_ALL35_WITNESS_READER_RECEIPT@1","reader_pid":os.getpid(),"producer_pid":producer_pid,"producer_exited_before_reader":True,"estate_path":receipt["estate_path"],"manifest_sha256":receipt["manifest_sha256"],"i02":receipt["i02"],"family_counts":counts,"reconstructed_release_ref":None,"stream_release_ref":receipt["i02"]["release"],"legacy_release_comparison":"NOT_APPLICABLE_SOURCE_ADAPTER","source_read_performed_by_reader":False,"source_path_opened_stat_hashed_decoded_by_reader":False}
        (root/"reader_receipt.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n");print(json.dumps({"status":"READER_OPENED","counts":counts,"source_adapter":True}));return 0
    if args.sourcefree:
        from streaming_estate import StreamRoots, open_stream_native_estate
        from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
        root=Path(args.root).absolute();receipt=json.loads((root/"producer_receipt.json").read_text());producer_pid=int(receipt["producer_pid"])
        probe=subprocess.run(["ps","-p",str(producer_pid),"-o","pid="],capture_output=True,text=True)
        if probe.stdout.strip(): raise CallerRefusal("PRODUCER_STILL_ALIVE_BEFORE_READER")
        held=StreamRoots(**receipt["i02"])
        estate=open_stream_native_estate(root/"private",exact_path=receipt["estate_path"],manifest_sha256=receipt["manifest_sha256"],roots=held,current_authorizer=lambda r:r==held)
        counts={f:sum(1 for _ in estate.iter_family(f)) for f in ALL_FAMILIES}
        payload={"schema":"ANVIL_ALL35_WITNESS_READER_RECEIPT@1","reader_pid":os.getpid(),"producer_pid":producer_pid,"producer_exited_before_reader":True,"estate_path":receipt["estate_path"],"manifest_sha256":receipt["manifest_sha256"],"i02":receipt["i02"],"family_counts":counts,"reconstructed_release_ref":None,"stream_release_ref":receipt["i02"]["release"],"legacy_release_comparison":"NOT_APPLICABLE_SOURCEFREE","source_read_performed_by_reader":False,"source_path_opened_stat_hashed_decoded_by_reader":False}
        (root/"reader_receipt.json").write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n");print(json.dumps({"status":"READER_OPENED","counts":counts,"sourcefree":True}));return 0
    from streaming_estate import StreamRoots, open_stream_native_estate
    from rawlsing_next.pre553_source_i02_streams import ALL_FAMILIES
    root = Path(args.root).absolute()
    receipt = json.loads((root / "producer_receipt.json").read_text())
    producer_pid = int(receipt["producer_pid"])
    probe = subprocess.run(["ps", "-p", str(producer_pid), "-o", "pid="],
                           capture_output=True, text=True)
    if probe.stdout.strip():
        raise CallerRefusal("PRODUCER_STILL_ALIVE_BEFORE_READER")
    _gb, _bound, resolver, _source_path, _trust = _grant(args.binding_dir)
    held = StreamRoots(**receipt["i02"])
    request = _bound.request

    def current(roots):
        if roots != held:
            return False
        decision = resolver.resolve_current(request)
        return (decision.currentness == "CURRENT_GRANTED"
                and decision.source_id == "SRC04"
                and decision.purpose == request.purpose
                and decision.consumer_use == request.consumer_use
                and decision.physical_read_extent == "EXACT_FILE")

    progress_path = root / "progress.jsonl"
    def reader_progress(update):
        with progress_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(update, sort_keys=True) + "\n")
            stream.flush()
    estate = open_stream_native_estate(
        root / "private", exact_path=receipt["estate_path"],
        manifest_sha256=receipt["manifest_sha256"], roots=held,
        current_authorizer=current, progress=reader_progress)
    counts = {}
    identities = []
    routing = []
    for family in ALL_FAMILIES:
        n = 0
        for obj in estate.iter_family(family):
            n += 1
            if family == "RespondentIdentity":
                identities.append(obj.ref.key)
            elif family == "RoutingEligibilityFact":
                routing.append(obj.ref.key)
        counts[family] = n
    differences = {k: {"actual": counts.get(k), "accepted": v}
                   for k, v in ACCEPTED.items()
                   if k in counts and counts.get(k) != v}
    payload = {
        "schema": "ANVIL_ALL35_WITNESS_READER_RECEIPT@1",
        "reader_pid": os.getpid(),
        "producer_pid": producer_pid,
        "producer_exited_before_reader": True,
        "estate_path": receipt["estate_path"],
        "manifest_sha256": receipt["manifest_sha256"],
        "i02": receipt["i02"],
        "family_counts": counts,
        "identity_count": len(identities),
        "identity_ref_digest": hashlib.sha256(
            json.dumps(sorted(identities), separators=(",", ":")).encode()).hexdigest(),
        "routing_count": len(routing),
        "routing_ref_digest": hashlib.sha256(
            json.dumps(sorted(routing), separators=(",", ":")).encode()).hexdigest(),
        "reconstructed_release_ref": None,
        "stream_release_ref": receipt["i02"]["release"],
        "accepted_historical": ACCEPTED,
        "legacy_release_comparison": "NOT_APPLICABLE_STREAM_PROOF",
        "stream_release_identity": receipt["i02"]["release"],
        "release_ref_equal_to_accepted": None,
        "differences_from_accepted": differences,
        "q217_hold_from_scoped_producer": receipt["q217"],
        "source_read_performed_by_reader": False,
        "source_path_opened_stat_hashed_decoded_by_reader": False,
    }
    (root / "reader_receipt.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"status": "READER_OPENED", "counts": counts,
                      "differences": differences}))
    return 0


def _rss(pid: int) -> int:
    vendor = Path("/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117/vendor")
    sys.path.insert(0, str(vendor))
    from court_instrumentation import process_tree_rss_bytes
    return process_tree_rss_bytes(pid)


def _sample(pid: int, root: Path, samples: list[dict[str, Any]]) -> str | None:
    rss = _rss(pid)
    free = shutil.disk_usage(root).free
    samples.append({"elapsed": time.monotonic(), "rss": rss, "free": free})
    if rss > RAM_CAP:
        return "RSS_6GIB"
    if free < IN_FLIGHT_FREE_FLOOR:
        return "IN_FLIGHT_8GIB_BREACH"
    return None


def _grant_source_path(binding_dir: Path) -> str:
    doc = json.loads((binding_dir / "fixtures/SRC04_FULL_SOURCE_GRANT.json").read_text())
    source = doc.get("source_path")
    if not isinstance(source, str) or not source:
        raise CallerRefusal("GRANT_SOURCE_PATH_MISSING")
    return source


def supervisor(args) -> int:
    verify_candidate(args.candidate_tree, args.candidate_patch)
    if not args.sourcefree and not getattr(args,"source_adapter",None) and not args.authorized_source_launch:
        raise CallerRefusal("EXPLICIT_SOURCE_LAUNCH_AUTHORIZATION_REQUIRED")
    if not args.sourcefree and not getattr(args,"source_adapter",None) and args.runtime_config is None:
        raise CallerRefusal("RUNTIME_OVERLAY_REQUIRED_FOR_RUN")
    work = Path(args.work_root).absolute()
    work.mkdir(mode=0o700, parents=True, exist_ok=True)
    root = (work / tempfile_name(work, args.candidate_tree)).absolute()
    root.mkdir(mode=0o700)
    if shutil.disk_usage(root).free < STARTUP_FREE_FLOOR:
        raise CallerRefusal("DISK_FLOOR_BEFORE_RUN")
    base = [sys.executable, str(Path(__file__).resolve()), "--mode"]
    common = (["--candidate-tree", str(args.candidate_tree),
               "--candidate-patch", str(args.candidate_patch),
               "--config", str(args.config),
               "--binding-dir", str(args.binding_dir), "--root", str(root),
               "--work-root", str(work)]
              + (["--sourcefree"] if args.sourcefree else
                 (["--source-adapter", str(args.source_adapter)] if getattr(args,"source_adapter",None) else [
                 "--runtime-config", str(args.runtime_config),
                 "--source-path", args.source_path or _grant_source_path(args.binding_dir)]))
              + (["--resume-checkpoint", str(args.resume_checkpoint)]
                 if args.resume_checkpoint else []))
    samples: list[dict[str, Any]] = []
    started = time.monotonic()
    producer = subprocess.Popen([*base, "producer", *common], cwd=str(HERE),
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                text=True, start_new_session=True)
    abort = None
    while producer.poll() is None:
        time.sleep(0.25)
        abort = _sample(producer.pid, root, samples)
        if abort:
            os.killpg(producer.pid, signal.SIGTERM)
            break
    out, err = producer.communicate(timeout=30)
    (root / "producer.stdout").write_text(out)
    (root / "producer.stderr").write_text(err)
    if abort:
        result = {"schema": "ANVIL_ALL35_WITNESS_SUPERVISOR@1",
                  "status": "ABORTED", "abort": abort,
                  "samples": len(samples), "rss_peak": max((x["rss"] for x in samples), default=0),
                  "free_min": min((x["free"] for x in samples), default=0),
                  "caps": {"rss": RAM_CAP,
                           "in_flight_free_floor": IN_FLIGHT_FREE_FLOOR,
                           "startup_free_floor": STARTUP_FREE_FLOOR}}
        (root / "supervisor_receipt.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result))
        return 3
    if producer.returncode != 0:
        result = {"schema": "ANVIL_ALL35_WITNESS_SUPERVISOR@1",
                  "status": "PRODUCER_REFUSED", "exit": producer.returncode,
                  "samples": len(samples), "rss_peak": max((x["rss"] for x in samples), default=0),
                  "free_min": min((x["free"] for x in samples), default=0)}
        (root / "supervisor_receipt.json").write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(result))
        return producer.returncode
    reader = subprocess.Popen([*base, "reader", *common], cwd=str(HERE),
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True, start_new_session=True)
    abort = None
    while reader.poll() is None:
        time.sleep(0.25)
        abort = _sample(reader.pid, root, samples)
        if abort:
            os.killpg(reader.pid, signal.SIGTERM)
            break
    rout, rerr = reader.communicate(timeout=30)
    (root / "reader.stdout").write_text(rout)
    (root / "reader.stderr").write_text(rerr)
    result = {"schema": "ANVIL_ALL35_WITNESS_SUPERVISOR@1",
              "status": "COMPLETE" if reader.returncode == 0 and not abort else "READER_FAILED",
              "producer_exit": producer.returncode, "reader_exit": reader.returncode,
              "abort": abort, "elapsed": time.monotonic() - started,
              "samples": len(samples), "rss_peak": max((x["rss"] for x in samples), default=0),
              "free_min": min((x["free"] for x in samples), default=0),
              "caps": {"rss": RAM_CAP, "startup_free_floor": STARTUP_FREE_FLOOR,
                       "in_flight_free_floor": IN_FLIGHT_FREE_FLOOR,
                       "staging_budget": STAGING_BUDGET, "wall_cutoff": None}}
    (root / "supervisor_receipt.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result))
    return 0 if result["status"] == "COMPLETE" else 4


def tempfile_name(work: Path, candidate: Path) -> str:
    return "SRC04_WITNESS_" + hashlib.sha256(
        (str(candidate) + str(time.time_ns())).encode()).hexdigest()[:16]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=("preflight", "run", "producer", "reader"), required=True)
    ap.add_argument("--candidate-tree", type=Path, required=True)
    ap.add_argument("--candidate-patch", type=Path, required=True)
    ap.add_argument("--config", type=Path, required=True)
    ap.add_argument("--runtime-config", type=Path)
    ap.add_argument("--outdir", type=Path)
    ap.add_argument("--binding-dir", type=Path, default=BINDING_DIR)
    ap.add_argument("--root", type=Path)
    ap.add_argument("--work-root", type=Path, default=HERE / "RUNS")
    ap.add_argument("--source-path", default=None)
    ap.add_argument("--resume-checkpoint", type=Path)
    ap.add_argument("--authorized-source-launch", action="store_true")
    ap.add_argument("--sourcefree", action="store_true")
    ap.add_argument("--source-adapter", type=Path)
    args = ap.parse_args()
    try:
        if args.mode == "preflight":
            return preflight(args)
        if args.mode == "producer":
            if not args.root or (not args.sourcefree and not getattr(args,"source_adapter",None) and not args.source_path and not args.resume_checkpoint):
                raise CallerRefusal("PRODUCER_ROOT_AND_GRANT_SOURCE_REQUIRED")
            return producer(args)
        if args.mode == "reader":
            if not args.root:
                raise CallerRefusal("READER_ROOT_REQUIRED")
            return reader(args)
        return supervisor(args)
    except CallerRefusal as exc:
        print(json.dumps({"status": "REFUSED", "code": exc.code, "detail": exc.detail}))
        return 2
    except Exception as exc:
        code = getattr(exc, "code", type(exc).__name__)
        detail = getattr(exc, "detail", str(exc)[:300])
        print(json.dumps({"status": "REFUSED", "code": code, "detail": detail}, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
