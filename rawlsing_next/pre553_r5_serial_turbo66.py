"""Additive Authority-66 serial Compact V2 execution variants."""
from __future__ import annotations

from dataclasses import dataclass, asdict
import gzip, hashlib, heapq, json, os, shutil, struct, time
import resource
from pathlib import Path
from typing import Iterable

from rawlsing_next import pre553_r5_compact_carrier as frozen
from rawlsing_next.pre553_r5_codec import CODEC_VERSION, canonical_bytes, canonical_json
from rawlsing_next.pre553_r5_model import (
    CARRIER_ID, INVENTORY_SCHEMA_VERSION, ROOT_SCHEMA_VERSION,
    R5BuildConfig, R5CanonicalRow, R5Error, R5IntegrityError, R5ReleaseIdentity,
)


@dataclass(frozen=True)
class TurboConfig:
    name: str
    run_max_rows: int
    run_max_bytes: int
    merge_fan_in: int
    temp_level: int | None
    temp_fsync: bool
    shard_max_rows: int
    shard_max_bytes: int
    final_level: int
    baseline_layout: bool = True


BASELINE = TurboConfig("V0", 4096, 4 * 1024 * 1024, 8, 6, True, 16384, 16 * 1024 * 1024, 6)

RSS_PREFERRED = 2 * 1024**3
RSS_STOP = 3 * 1024**3
RSS_HARD_ABORT = int(3.5 * 1024**3)
SCRATCH_WARNING = 4 * 1024**3
SCRATCH_HARD_ABORT = 8 * 1024**3
FREE_SPACE_HARD_ABORT = 5 * 1024**3


class TurboSafetyAbort(RuntimeError):
    pass


def actual_fan_in(requested: int, *, soft_limit: int | None = None, reserve: int = 64) -> int:
    if soft_limit is None:
        soft_limit = int(resource.getrlimit(resource.RLIMIT_NOFILE)[0])
    return min(requested, max(0, soft_limit - reserve))


def rss_action(value: int) -> str:
    if value >= RSS_HARD_ABORT: return "HARD_ABORT"
    if value >= RSS_STOP: return "STOP_DISPATCH"
    if value >= RSS_PREFERRED: return "ALLOWED_SLOW_BAND"
    return "NORMAL"


def scratch_action(value: int) -> str:
    if value >= SCRATCH_HARD_ABORT: return "HARD_ABORT"
    if value >= SCRATCH_WARNING: return "WARNING"
    return "NORMAL"


def filesystem_action(free_bytes: int) -> str:
    return "HARD_ABORT" if free_bytes < FREE_SPACE_HARD_ABORT else "NORMAL"


def _fsync(path: Path, enabled: bool) -> None:
    if enabled:
        with path.open("rb") as h:
            os.fsync(h.fileno())


def _writer(path: Path, level: int | None):
    raw = path.open("wb")
    if level is None:
        return raw, raw
    return raw, gzip.GzipFile(filename="", mode="wb", fileobj=raw, compresslevel=level, mtime=0)


def _write_record(handle, key: bytes, data: bytes) -> None:
    handle.write(struct.pack(">II", len(key), len(data)))
    handle.write(key); handle.write(data)


def _read_record(handle):
    h = handle.read(8)
    if not h: return None
    if len(h) != 8: raise R5IntegrityError("truncated turbo run header")
    kl, dl = struct.unpack(">II", h)
    k, d = handle.read(kl), handle.read(dl)
    if len(k) != kl or len(d) != dl: raise R5IntegrityError("truncated turbo run record")
    return k, d


class SerialTurboBuilder:
    def __init__(self, config: TurboConfig, *, member_closed_callback=None):
        self.config = config
        self.member_closed_callback = member_closed_callback
        self.builder_blocked_seconds = 0.0
        self.actual_merge_fan_in = actual_fan_in(config.merge_fan_in)
        if self.actual_merge_fan_in < 2:
            raise TurboSafetyAbort("RLIMIT_NOFILE leaves insufficient merge fan-in")
        self.phase = {}
        self.max_open = 0
        self.temp_bytes_written = 0

    def _timed(self, name, fn):
        start = time.perf_counter(); value = fn(); self.phase[name] = time.perf_counter() - start
        return value

    def _flush(self, directory: Path, index: int, records):
        records.sort(key=lambda x: x[0])
        path = directory / f"run-{index:08d}.tmp"
        raw, out = _writer(path, self.config.temp_level)
        try:
            for k, d in records: _write_record(out, k, d)
            if out is not raw: out.close()
            raw.flush(); _fsync(path, self.config.temp_fsync)
        finally:
            raw.close()
        self.temp_bytes_written += path.stat().st_size
        return path

    def _make_runs(self, rows, work):
        directory = work / "runs-0000"; directory.mkdir()
        manifest = work / "runs-0000.txt"
        buffered=[]; buffered_bytes=0; index=count=max_rows=max_bytes=0
        with manifest.open("w", encoding="utf-8", newline="\n") as out:
            for row in rows:
                key=frozen._sort_key(row); data=frozen._storage_wire(row)
                size=len(key)+len(data)+8
                if buffered and (len(buffered)>=self.config.run_max_rows or buffered_bytes+size>self.config.run_max_bytes):
                    p=self._flush(directory,index,buffered); out.write(p.name+"\n"); index+=1
                    max_rows=max(max_rows,len(buffered)); max_bytes=max(max_bytes,buffered_bytes)
                    buffered=[]; buffered_bytes=0
                buffered.append((key,data)); buffered_bytes+=size; count+=1
                if len(buffered)>=self.config.run_max_rows or buffered_bytes>=self.config.run_max_bytes:
                    p=self._flush(directory,index,buffered); out.write(p.name+"\n"); index+=1
                    max_rows=max(max_rows,len(buffered)); max_bytes=max(max_bytes,buffered_bytes)
                    buffered=[]; buffered_bytes=0
            if buffered:
                p=self._flush(directory,index,buffered); out.write(p.name+"\n"); index+=1
                max_rows=max(max_rows,len(buffered)); max_bytes=max(max_bytes,buffered_bytes)
            out.flush(); _fsync(manifest,self.config.temp_fsync)
        if not count: raise R5Error("R5 canonical release cannot be empty")
        return manifest,directory,{"input_rows":count,"initial_runs":index,"max_buffered_run_rows":max_rows,"max_buffered_run_bytes":max_bytes}

    def _groups(self, manifest):
        group=[]
        for line in manifest.read_text(encoding="utf-8").splitlines():
            if line.strip():
                group.append(line.strip())
                if len(group)>=self.actual_merge_fan_in: yield group; group=[]
        if group: yield group

    def _merge_group(self, source, names, target):
        raws=[(source/n).open("rb") for n in names]
        handles=[gzip.GzipFile(mode="rb",fileobj=r) if self.config.temp_level is not None else r for r in raws]
        try:
            heap=[]
            for i,h in enumerate(handles):
                rec=_read_record(h)
                if rec: heapq.heappush(heap,(rec[0],i,rec[1]))
            raw,out=_writer(target,self.config.temp_level)
            try:
                while heap:
                    k,i,d=heapq.heappop(heap); _write_record(out,k,d)
                    nxt=_read_record(handles[i])
                    if nxt: heapq.heappush(heap,(nxt[0],i,nxt[1]))
                if out is not raw: out.close()
                raw.flush(); _fsync(target,self.config.temp_fsync)
            finally: raw.close()
        finally:
            for h in handles:
                if h not in raws: h.close()
            for r in raws: r.close()
        self.temp_bytes_written += target.stat().st_size

    def _reduce(self, manifest, directory, work):
        passes=0; max_open=0
        while True:
            count=sum(bool(x.strip()) for x in manifest.read_text(encoding="utf-8").splitlines())
            if count<=self.actual_merge_fan_in: return manifest,directory,passes,max_open
            passes+=1; target_dir=work/f"runs-{passes:04d}"; target_dir.mkdir(); nxt=work/f"runs-{passes:04d}.txt"; n=0
            with nxt.open("w",encoding="utf-8",newline="\n") as out:
                for group in self._groups(manifest):
                    max_open=max(max_open,len(group)); target=target_dir/f"run-{n:08d}.tmp"; self._merge_group(directory,group,target); out.write(target.name+"\n"); n+=1
                out.flush(); _fsync(nxt,self.config.temp_fsync)
            shutil.rmtree(directory); manifest.unlink(); directory,manifest=target_dir,nxt

    def _iter_final(self, manifest, directory):
        names=[x.strip() for x in manifest.read_text(encoding="utf-8").splitlines() if x.strip()]
        raws=[(directory/n).open("rb") for n in names]
        handles=[gzip.GzipFile(mode="rb",fileobj=r) if self.config.temp_level is not None else r for r in raws]
        try:
            heap=[]
            for i,h in enumerate(handles):
                rec=_read_record(h)
                if rec: heapq.heappush(heap,(rec[0],i,rec[1]))
            while heap:
                k,i,d=heapq.heappop(heap); yield k,d
                nxt=_read_record(handles[i])
                if nxt: heapq.heappush(heap,(nxt[0],i,nxt[1]))
        finally:
            for h in handles:
                if h not in raws: h.close()
            for r in raws: r.close()

    def build(self, rows: Iterable[R5CanonicalRow], *, release_identity: R5ReleaseIdentity, target_directory):
        target=Path(target_directory); target.mkdir(parents=True); members=target/"members"; members.mkdir(); work=target/".work"; work.mkdir()
        manifest,directory,telemetry=self._timed("initial_run_generation_sort_write",lambda:self._make_runs(rows,work))
        manifest,directory,passes,max_open=self._timed("merge_reduction",lambda:self._reduce(manifest,directory,work))
        telemetry.update(merge_passes=passes,max_merge_open_runs=max_open)
        inventory=target/"member_inventory.jsonl"; total=members_count=shard=0; global_digest=hashlib.sha256(); prev=None; actual_member=0
        current_raw=current_out=current_path=None; current_rows=current_bytes=0; first=last=None; current_digest=None; relcounts={}
        final_start=time.perf_counter()
        member_hash_seconds=0.0
        with inventory.open("w",encoding="ascii",newline="\n") as inv:
            def close_member():
                nonlocal current_raw,current_out,current_path,current_rows,current_bytes,first,last,current_digest,relcounts,members_count,actual_member,member_hash_seconds
                if current_out is None:return
                if current_out is not current_raw: current_out.close()
                current_raw.flush(); _fsync(current_path,True); current_raw.close()
                hash_start=time.perf_counter(); sha,size=frozen._sha256_file(current_path); member_hash_seconds += time.perf_counter()-hash_start; actual_member+=size
                inv.write(canonical_json({"inventory_schema_version":INVENTORY_SCHEMA_VERSION,"member":current_path.name,"member_encoding":frozen.MEMBER_ENCODING,"byte_length":size,"sha256":sha,"logical_digest":current_digest.hexdigest(),"row_count":current_rows,"first_identity":list(first),"last_identity":list(last),"relation_counts":dict(sorted(relcounts.items()))})+"\n")
                if self.member_closed_callback is not None:
                    blocked_start=time.perf_counter()
                    self.member_closed_callback(current_path.name)
                    self.builder_blocked_seconds += time.perf_counter()-blocked_start
                members_count+=1; current_raw=current_out=current_path=None; current_rows=current_bytes=0; first=last=None; current_digest=None; relcounts={}
            for key,data in self._iter_final(manifest,directory):
                row=frozen._decode_storage(data)
                if key!=frozen._sort_key(row): raise R5IntegrityError("temporary run identity mismatch")
                identity=row.identity_key
                if prev is not None and identity<=prev: raise R5IntegrityError("duplicate/noncanonical exact identity")
                prev=identity
                if current_out is not None and (current_rows>=self.config.shard_max_rows or current_bytes+len(data)>self.config.shard_max_bytes): close_member(); shard+=1
                if current_out is None:
                    current_path=members/f"member-{shard:08d}.r5z"; current_raw,current_out=_writer(current_path,self.config.final_level); first=identity; current_digest=hashlib.sha256()
                current_out.write(data); lw=frozen._logical_wire(row); current_digest.update(lw); global_digest.update(lw); current_rows+=1; current_bytes+=len(data); total+=1; last=identity; relcounts[row.relation]=relcounts.get(row.relation,0)+1
            close_member(); inv.flush(); _fsync(inventory,True)
        self.phase["final_merge_member_sealing"]=time.perf_counter()-final_start
        self.phase["member_hashing_inventory_write"]=member_hash_seconds
        if total!=telemetry["input_rows"]: raise R5IntegrityError("row count changed during merge")
        inv_sha,inv_bytes=frozen._sha256_file(inventory)
        root_config=R5BuildConfig() if self.config.baseline_layout else R5BuildConfig(run_max_rows=self.config.run_max_rows,run_max_bytes=self.config.run_max_bytes,shard_max_rows=self.config.shard_max_rows,shard_max_bytes=self.config.shard_max_bytes,merge_fan_in=self.config.merge_fan_in,verified_spool_memory_bytes=1024*1024)
        release={"release_id":release_identity.release_id,"semantic_release_hash":release_identity.semantic_release_hash,"source_artifact_ref":dict(release_identity.source_artifact_ref),"source_release_manifest_hash":release_identity.source_release_manifest_hash,"m01_m18_coverage":{k:list(v) for k,v in sorted(release_identity.m01_m18_coverage.items())},"decoder_receipt":release_identity.decoder_receipt,"compiler_contract_digest":release_identity.compiler_contract_digest,"c11_authority_digest":release_identity.c11_authority_digest}
        unsigned={"root_schema_version":ROOT_SCHEMA_VERSION,"carrier_schema_version":frozen.CARRIER_SCHEMA_VERSION,"carrier_id":CARRIER_ID,"member_encoding":frozen.MEMBER_ENCODING,"typed_codec_version":CODEC_VERSION,"release_identity":release,"logical_stream_digest":global_digest.hexdigest(),"canonical_row_count":total,"member_inventory":{"path":inventory.name,"sha256":inv_sha,"byte_length":inv_bytes,"member_count":members_count},"build_config":asdict(root_config)}
        closure_start=time.perf_counter(); root_id=hashlib.sha256(canonical_bytes(unsigned)).hexdigest(); root={**unsigned,"physical_root_id":root_id}; root_path=target/"root.json"; root_path.write_text(canonical_json(root)+"\n",encoding="ascii"); frozen._fsync_file(root_path); frozen._fsync_file(inventory); frozen._fsync_dir(members); frozen._fsync_dir(target)
        self.phase["hash_inventory_root_closure"]=time.perf_counter()-closure_start
        shutil.rmtree(work)
        telemetry.update({"merge_passes":passes,"max_merge_open_runs":max_open,"actual_merge_fan_in":self.actual_merge_fan_in,"requested_merge_fan_in":self.config.merge_fan_in,"execution_config":asdict(self.config),"final_shards":members_count,"member_bytes":actual_member,"inventory_bytes":inv_bytes,"root_bytes":root_path.stat().st_size,"canonical_steady_state_bytes":actual_member+inv_bytes+root_path.stat().st_size,"logical_stream_digest":global_digest.hexdigest(),"physical_root_id":root_id,"temp_bytes_written":self.temp_bytes_written,"builder_blocked_seconds":self.builder_blocked_seconds,"phases":dict(self.phase)})
        return telemetry


def baseline_config(name="V0"):
    return BASELINE if name=="V0" else TurboConfig(name,4096,4*1024*1024,8,6,True,16384,16*1024*1024,6)
