"""Authority 67 independent trailing audit for frozen V4."""
from __future__ import annotations
import gzip, hashlib, json, multiprocessing as mp, os, queue, resource, shutil, time
from pathlib import Path

from rawlsing_next import pre553_r5_compact_carrier as frozen
from rawlsing_next.pre553_r5_codec import canonical_bytes


def _audit_member(path: Path, global_state=None):
    compressed=path.read_bytes(); sha=hashlib.sha256(compressed).hexdigest(); logical=hashlib.sha256(); rows=0; first=last=None; previous=None; relation_counts={}
    try:
        with gzip.GzipFile(fileobj=__import__('io').BytesIO(compressed), mode='rb') as stream:
            for raw in stream:
                row=frozen._decode_storage(raw); identity=row.identity_key
                if previous is not None and identity<=previous: raise RuntimeError("trailing audit duplicate/noncanonical identity")
                previous=identity; first=first or identity; last=identity; wire=frozen._logical_wire(row); logical.update(wire); rows+=1; relation_counts[row.relation]=relation_counts.get(row.relation,0)+1
                if global_state is not None:
                    global_state[0].update(wire); global_state[1] += 1; global_state[2][row.relation]=global_state[2].get(row.relation,0)+1
    except Exception as exc:
        raise RuntimeError(f"trailing audit member failure {path.name}: {exc}") from exc
    return {"inventory_schema_version": frozen.INVENTORY_SCHEMA_VERSION, "member":path.name,"member_encoding":frozen.MEMBER_ENCODING,"byte_length":len(compressed),"sha256":sha,"logical_digest":logical.hexdigest(),"row_count":rows,"first_identity":list(first) if first else None,"last_identity":list(last) if last else None,"relation_counts":dict(sorted(relation_counts.items()))}


def _auditor_main(target_text, ready, result):
    audit_started=time.perf_counter(); target=Path(target_text); members=target/"members"; derived=[]; global_digest=hashlib.sha256(); total=0; global_rel={}; global_state=[global_digest, total, global_rel]; previous=None; expected_ordinal=0; seen=set()
    try:
        while True:
            name=ready.get()
            if name is None: break
            try: ordinal=int(name.split("-")[1].split(".")[0])
            except Exception as exc: raise RuntimeError("invalid readiness ordinal") from exc
            if ordinal in seen or ordinal != expected_ordinal: raise RuntimeError("missing, duplicate, or out-of-order readiness ordinal")
            seen.add(ordinal); expected_ordinal += 1
            path=members/name
            if not path.exists(): raise RuntimeError("missing readiness member")
            item=_audit_member(path, global_state)
            if previous is not None and tuple(item["first_identity"]) <= previous: raise RuntimeError("global member order failure")
            previous=tuple(item["last_identity"]); derived.append(item)
        total=global_state[1]; global_rel=global_state[2]
        root_raw=(target/"root.json").read_bytes(); root=json.loads(root_raw.decode('ascii')); supplied=root.pop('physical_root_id',None)
        if supplied != hashlib.sha256(canonical_bytes(root)).hexdigest(): raise RuntimeError("root self-hash mismatch")
        inv_path=target/root["member_inventory"]["path"]; inv_raw=inv_path.read_bytes(); inv_sha=hashlib.sha256(inv_raw).hexdigest()
        if inv_sha != root["member_inventory"]["sha256"] or len(inv_raw)!=root["member_inventory"]["byte_length"]: raise RuntimeError("inventory binding mismatch")
        inventory=[json.loads(line) for line in inv_raw.splitlines() if line]
        if inventory != derived: raise RuntimeError("independent member facts disagree with inventory")
        if len(derived)!=root["member_inventory"]["member_count"] or total!=root["canonical_row_count"] or global_digest.hexdigest()!=root["logical_stream_digest"]: raise RuntimeError("global root reconciliation mismatch")
        result.put({"ok":True,"audit":{"canonical_rows":total,"logical_stream_digest":global_digest.hexdigest(),"physical_root_id":supplied,"relation_counts":dict(sorted(global_rel.items()))},"members":derived,"audit_seconds":time.perf_counter()-audit_started,"peak_rss_bytes":int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * (1 if os.uname().sysname == "Darwin" else 1024)})
    except Exception as exc:
        result.put({"ok":False,"error":repr(exc)})


def run_trailing(builder, rows, release_identity, target, *, queue_capacity=8):
    ctx=mp.get_context("spawn"); ready=ctx.Queue(maxsize=queue_capacity); result=ctx.Queue(maxsize=1); process=ctx.Process(target=_auditor_main,args=(str(target),ready,result)); process.start(); build_start=time.perf_counter(); auditor_start=build_start; queue_peak=0
    def notify(name):
        nonlocal queue_peak
        while True:
            if not process.is_alive(): raise RuntimeError("trailing auditor exited before readiness admission")
            try:
                ready.put(name, timeout=1.0); break
            except queue.Full:
                continue
        try: queue_peak=max(queue_peak,ready.qsize())
        except (NotImplementedError, AttributeError): queue_peak=max(queue_peak,1)
    try:
        telemetry=builder.__class__(builder.config, member_closed_callback=notify).build(rows,release_identity=release_identity,target_directory=target)
        builder_root_sealed=time.perf_counter()
        ready.put(None); process.join()
        if process.exitcode!=0: raise RuntimeError("trailing auditor process failure")
        outcome=result.get(timeout=10)
        if not outcome.get("ok"): raise RuntimeError(outcome.get("error","trailing audit failure"))
        finished=time.perf_counter()
        builder_rss=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss) * (1 if os.uname().sysname == "Darwin" else 1024)
        auditor_rss=outcome.get("peak_rss_bytes",0)
        return telemetry,outcome,{"overlap_total_seconds":finished-build_start,"auditor_seconds":outcome.get("audit_seconds"),"auditor_start_offset_seconds":auditor_start-build_start,"auditor_finish_lag_after_root_seal_seconds":finished-builder_root_sealed,"builder_blocked_seconds":telemetry.get("builder_blocked_seconds",0.0),"queue_peak":queue_peak,"aggregate_peak_rss_bytes":builder_rss+auditor_rss,"builder_rss_bytes":builder_rss,"auditor_rss_bytes":auditor_rss}
    except Exception:
        process.terminate(); process.join(timeout=5); raise
