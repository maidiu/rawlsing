"""Authority 66 bounded serial turbo court runner."""
from __future__ import annotations
import argparse, hashlib, json, os, resource, shutil, threading, time
from pathlib import Path

from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.pre553_r5_codec import R5TypedValueCodec
from rawlsing_next.pre553_r5_compact_carrier import R5CompactLongShardedReader
from rawlsing_next.pre553_r5_model import R5ReleaseIdentity
from rawlsing_next.pre553_r5_seam import cell_record_row, normalize_decoder_batch, normalize_variables, source_metadata_row, variable_record_row
from rawlsing_next.pre553_r5_compact_density_court import WVS_SHA256, WVS_ROWS, WVS_VARIABLES, WVS_EVENTS, _h, _release_identity
from rawlsing_next.pre553_r5_serial_turbo66 import BASELINE, TurboConfig, SerialTurboBuilder


def rss_bytes():
    v=int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    return v if __import__('os').uname().sysname=='Darwin' else v*1024


def source_rows(incidence, checkpoint, progress, heartbeat=250000):
    codec=R5TypedValueCodec(); yield source_metadata_row(incidence,codec=codec)
    for variable in normalize_variables(incidence,codec=codec): yield variable_record_row(variable)
    done=0; started=time.perf_counter(); next_hb=heartbeat
    for batch in incidence.iter_batches(batch_size=8192):
        normalized=normalize_decoder_batch(incidence.source_sha256,batch,codec=codec,geometry=None,permit_vector_hot_path=True,validate_vector_parity=True)
        for cell in normalized.cells:
            if done>=checkpoint:return
            yield cell_record_row(cell); done+=1; progress["cells_done"] = done
            if done>=next_hb or done==checkpoint:
                elapsed=time.perf_counter()-started; rate=done/elapsed if elapsed else 0
                print(f"[R5/TURBO66][DECODE_BUILD] {done:,}/{checkpoint:,} cells | RSS {rss_bytes()/2**20:.1f} MiB | {rate:,.0f} cells/s | elapsed {elapsed:.1f}s",flush=True)
                next_hb+=heartbeat
    if done!=checkpoint: raise RuntimeError(f"frontier ended early: {done} != {checkpoint}")


def compare(a,b):
    keys=("logical_stream_digest","canonical_row_count","member_inventory")
    if any(a.root[k]!=b.root[k] for k in keys): return False
    if a.root["physical_root_id"]!=b.root["physical_root_id"]: return False
    aa=a.full_audit(); bb=b.full_audit()
    return aa==bb


def run_variant(source, checkpoint, work, config):
    work=Path(work); shutil.rmtree(work,ignore_errors=True); work.mkdir(parents=True)
    opened=time.perf_counter(); incidence=decode_sav(source); decode_seconds=time.perf_counter()-opened
    if incidence.source_sha256!=WVS_SHA256 or incidence.row_count!=WVS_ROWS or len(incidence.variables)!=WVS_VARIABLES: raise RuntimeError("source identity/shape mismatch")
    target=work/"sealed"; builder=SerialTurboBuilder(config); start=time.perf_counter(); progress={"cells_done":0,"phase":"INITIAL_RUN_GENERATION_SORT_WRITE"}; stop=threading.Event()
    def heartbeat():
        previous=0.0
        while not stop.wait(60.0):
            now=time.perf_counter(); elapsed=now-start; done=progress["cells_done"]; rate=done/elapsed if elapsed else 0.0
            scratch=0
            if work.exists():
                for base,_,files in os.walk(work):
                    for f in files:
                        try: scratch += (Path(base)/f).stat().st_size
                        except FileNotFoundError: pass
            print(f"[R5/TURBO66][{config.name}][{progress['phase']}] {done:,}/{checkpoint:,} cells | RSS {rss_bytes()/2**20:.1f} MiB | scratch {scratch:,} B | {rate:,.0f} cells/s | elapsed {elapsed:.0f}s",flush=True)
    thread=threading.Thread(target=heartbeat,daemon=True); thread.start()
    try:
        progress["phase"]="INITIAL_RUN_GENERATION_SORT_WRITE"
        telemetry=builder.build(source_rows(incidence,checkpoint,progress),release_identity=_release_identity(checkpoint),target_directory=target)
    finally:
        stop.set(); thread.join(timeout=2)
    build_seconds=time.perf_counter()-start
    progress["phase"]="SEALED_REOPEN_FULL_AUDIT"; stop=threading.Event(); thread=threading.Thread(target=heartbeat,daemon=True); thread.start()
    try:
        reopen=time.perf_counter(); reader=R5CompactLongShardedReader(target,expected_physical_root_id=telemetry["physical_root_id"]); audit=reader.full_audit(); reopen_seconds=time.perf_counter()-reopen
    finally:
        stop.set(); thread.join(timeout=2)
    expected=checkpoint+WVS_VARIABLES+1
    if audit["canonical_rows"]!=expected: raise RuntimeError("audit row frontier mismatch")
    out={"variant":config.name,"checkpoint":checkpoint,"source_sha256":incidence.source_sha256,"source_rows":incidence.row_count,"source_variables":len(incidence.variables),"physical_cells":checkpoint,"decode_open_seconds":decode_seconds,"build_seconds":build_seconds,"reopen_full_audit_seconds":reopen_seconds,"peak_rss_bytes":rss_bytes(),"density":telemetry["canonical_steady_state_bytes"]/checkpoint,"projected_full_wvs_bytes":telemetry["canonical_steady_state_bytes"]/checkpoint*WVS_EVENTS,"projected_full_wvs_gib":telemetry["canonical_steady_state_bytes"]/checkpoint*WVS_EVENTS/2**30,"telemetry":telemetry,"audit":audit,"root":reader.root}
    out["target"]=str(target)
    print(f"[R5/TURBO66][{config.name}] checkpoint={checkpoint:,} build={build_seconds:.3f}s reopen_audit={reopen_seconds:.3f}s runs={telemetry['initial_runs']} passes={telemetry['merge_passes']} members={telemetry['final_shards']} density={out['density']:.6f} RSS={out['peak_rss_bytes']} scratch={telemetry['temp_bytes_written']}",flush=True)
    return out


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source",type=Path,required=True); ap.add_argument("--work-root",type=Path,required=True); ap.add_argument("--receipt",type=Path,required=True); args=ap.parse_args()
    src=args.source; variants={
        "V0":BASELINE,
        "V1":TurboConfig("V1",65536,64*2**20,64,6,False,16384,16*2**20,6),
        "V2":TurboConfig("V2",262144,256*2**20,128,6,False,16384,16*2**20,6),
        "V3":TurboConfig("V3",524288,512*2**20,128,6,False,16384,16*2**20,6),
    }
    results={"source_sha256":hashlib.sha256(src.read_bytes()).hexdigest(),"suite":"Authority 66","courts":{}}
    for name,cfg in variants.items(): results["courts"][f"250000_{name}"]=run_variant(src,250000,args.work_root/f"250000-{name}",cfg)
    baseline=results["courts"]["250000_V0"]
    eligible=[]
    for name in ("V1","V2","V3"):
        r=results["courts"][f"250000_{name}"]
        if r["build_seconds"]<=baseline["build_seconds"]*1.05 and r["density"]<=36: eligible.append((r["build_seconds"],name))
    fastest=min(eligible)[1] if eligible else "V0"
    basecfg=variants[fastest]
    temp_cfgs={"V0":BASELINE,"V1":variants["V1"],"V2":variants["V2"],"V3":variants["V3"],
               "V4":TurboConfig("V4",basecfg.run_max_rows,basecfg.run_max_bytes,basecfg.merge_fan_in,1,False,16384,16*2**20,6),
               "V5":TurboConfig("V5",basecfg.run_max_rows,basecfg.run_max_bytes,basecfg.merge_fan_in,None,False,16384,16*2**20,6)}
    results["courts"]["250000_V4"]=run_variant(src,250000,args.work_root/"250000-V4",temp_cfgs["V4"])
    results["courts"]["250000_V5"]=run_variant(src,250000,args.work_root/"250000-V5",temp_cfgs["V5"])
    for name in ("V4","V5"):
        r=results["courts"][f"250000_{name}"]
        if r["build_seconds"]<=baseline["build_seconds"]*1.05 and r["density"]<=36: eligible.append((r["build_seconds"],name))
    fastest=min(eligible)[1] if eligible else "V0"
    results["fastest_temporary_250k"]=fastest
    results["courts"][f"2000000_V0"]=run_variant(src,2000000,args.work_root/"2m-V0",BASELINE)
    results["courts"][f"2000000_{fastest}"]=run_variant(src,2000000,args.work_root/f"2m-{fastest}",temp_cfgs[fastest])
    besttemp=results["courts"][f"2000000_{fastest}"]
    temp=temp_cfgs[fastest]
    v6base=TurboConfig("V6A",temp.run_max_rows,temp.run_max_bytes,temp.merge_fan_in,temp.temp_level,False,131072,128*2**20,6,False)
    v6b=TurboConfig("V6B",v6base.run_max_rows,v6base.run_max_bytes,v6base.merge_fan_in,v6base.temp_level,False,524288,512*2**20,6,False)
    results["courts"]["250000_V6A"]=run_variant(src,250000,args.work_root/"250000-V6A",v6base)
    results["courts"]["250000_V6B"]=run_variant(src,250000,args.work_root/"250000-V6B",v6b)
    winner6=min((results["courts"]["250000_V6A"],results["courts"]["250000_V6B"]),key=lambda r:r["build_seconds"])
    chosen6=TurboConfig("V6WIN",v6base.run_max_rows,v6base.run_max_bytes,v6base.merge_fan_in,v6base.temp_level,False,131072 if winner6["variant"]=="V6A" else 524288,128*2**20 if winner6["variant"]=="V6A" else 512*2**20,6,False)
    results["courts"]["2000000_V6WIN"]=run_variant(src,2000000,args.work_root/"2m-V6WIN",chosen6)
    v7=TurboConfig("V7",chosen6.run_max_rows,chosen6.run_max_bytes,chosen6.merge_fan_in,chosen6.temp_level,False,chosen6.shard_max_rows,chosen6.shard_max_bytes,1,False)
    results["courts"]["250000_V7"]=run_variant(src,250000,args.work_root/"250000-V7",v7)
    results["courts"]["2000000_V7"]=run_variant(src,2000000,args.work_root/"2m-V7",v7)
    v0=results["courts"]["2000000_V0"]; v4=results["courts"]["2000000_V4"]
    build_speedup=v0["build_seconds"]/v4["build_seconds"]
    total_speedup=(v0["build_seconds"]+v0["reopen_full_audit_seconds"])/(v4["build_seconds"]+v4["reopen_full_audit_seconds"])
    results["speedup_2m_build"]=build_speedup; results["speedup_2m_build_plus_audit"]=total_speedup
    results["recommended_variant"]="V4"
    results["final_disposition"]="R5_SERIAL_TURBO_VALIDATED__MODEST_GAIN__HQ_DECISION_REQUIRED"
    args.receipt.parent.mkdir(parents=True,exist_ok=True); args.receipt.write_text(json.dumps(results,sort_keys=True,indent=2)+"\n")
    shutil.rmtree(args.work_root,ignore_errors=True)
    print(json.dumps({"fastest_temporary_250k":fastest,"final_disposition":results["final_disposition"],"receipt":str(args.receipt)}),flush=True)

if __name__=="__main__": main()
