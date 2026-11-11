#!/usr/bin/env python3
"""One finite baseline/candidate pilot pair using the existing benchmark CLI."""
from __future__ import annotations
import hashlib, json, os, platform, shutil, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path

CANDIDATE = Path('/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-w03-w04-mcr-verifier-repair-r1')
BASELINE = Path('/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/pyat-w03-w04-baseline-4f3413')
BASELINE_HEAD = '4f3413fc5c37b589be3412f826bf8f68ee617d4a'
CAP = 6 * 1024 ** 3
MIN_FREE = 512 * 1024 ** 2
EXPECTED = {
 'rawlsing_next/_pre553_c11_execution_view.py':'0f86148f504c06bc694dd980ae1da8913db929b6',
 'rawlsing_next/_pre553_w03_cold_compact.py':'06eefd8fe8c1839854a783c78045b170627806f2',
 'rawlsing_next/_pre553_w04_cache.py':'4bb7e933f0a5c3f34366ee9e9013b3714a3e4341',
 'rawlsing_next/pre553_source_backed_c11_facade.py':'c5f78e1f7385b188eda18ace063557c26a19fd40',
 'rawlsing_next/pre553_parquet_carrier.py':'2c09deeb9b85051cb9d4c36fc12b0a193095e085',
 'rawlsing_next/pre553_carrier_execution.py':'ee9b3af02bfca9238eb72ea45d94073d47769a07',
 'rawlsing_next/bench_w03_w04_physical.py':'6c72f7d67c16fe79b9260032f6ace4085c6f1f3d',
 'rawlsing_next/tests/test_bench_w03_w04_physical.py':'c765799a1ed54d3f74283b1f493d8a3e5256d9e7',
 'rawlsing_next/tests/test_pre553_w03_w04_completion.py':'7cd62ffc36091f6e36847f1498d1dc428ebda157',
}
def now(): return datetime.now(timezone.utc).isoformat()
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
 return h.hexdigest()
def save(p,v):
 p.parent.mkdir(parents=True,exist_ok=True)
 t=p.with_suffix(p.suffix+'.tmp'); t.write_text(json.dumps(v,indent=2,sort_keys=True)+'\n'); t.replace(p)
def gb(root,rel): return subprocess.check_output(['git','-C',str(root),'rev-parse',f'HEAD:{rel}'],text=True).strip()
def gh(root): return subprocess.check_output(['git','-C',str(root),'rev-parse','HEAD'],text=True).strip()
def disk(label):
 u=shutil.disk_usage('/Users/matthewsmith/Desktop')
 return {'label':label,'free_bytes':u.free,'total_bytes':u.total,'used_bytes':u.used,'minimum_free_bytes':MIN_FREE,'pass':u.free>=MIN_FREE,'observed_utc':now()}
def run_child(name,argv,cwd,env,raw,marker):
 lp=raw/f'{name}.launch.json'; cp=raw/f'{name}.completion.json'; so=raw/f'{name}.stdout.log'; se=raw/f'{name}.stderr.log'
 launch={'name':name,'argv':argv,'cwd':str(cwd),'pid':None,'started_utc':now(),'launch_is_not_completion':True}
 with so.open('wb') as o, se.open('wb') as e:
  p=subprocess.Popen(argv,cwd=str(cwd),env=env,stdout=o,stderr=e)
  launch['pid']=p.pid; save(lp,launch); save(marker,launch)
  code=p.wait()
 comp={'name':name,'pid':launch['pid'],'exit_code':code,'started_utc':launch['started_utc'],'finished_utc':now(),'stdout_path':str(so),'stderr_path':str(se),'launch_path':str(lp)}
 save(cp,comp); return comp
def main():
 if len(sys.argv)!=5: raise SystemExit('usage: run_pair.py RUN_DIR CANDIDATE BASELINE EVIDENCE_ROOT')
 run_dir=Path(sys.argv[1]).resolve(); candidate=Path(sys.argv[2]).resolve(); baseline=Path(sys.argv[3]).resolve(); evidence=Path(sys.argv[4]).resolve()
 raw=evidence/'raw'; raw.mkdir(parents=True,exist_ok=True); cache=run_dir/'cache'; cache.mkdir(parents=True,exist_ok=True)
 pre={'schema':'PYAT_W03_W04_ONE_PASS_PILOT_PREFLIGHT_R1','started_utc':now(),'candidate_head':gh(candidate),'candidate_root':str(candidate),'baseline_head':gh(baseline),'baseline_expected_head':BASELINE_HEAD,'candidate_blobs':{p:gb(candidate,p) for p in EXPECTED},'candidate_blobs_match':all(gb(candidate,p)==v for p,v in EXPECTED.items()),'baseline_diff_empty':subprocess.run(['git','-C',str(baseline),'diff','--quiet','--','rawlsing_next'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0,'host':{'node':platform.node(),'platform':platform.platform(),'python':sys.version,'memory_bytes':int(subprocess.check_output(['sysctl','-n','hw.memsize'],text=True).strip())},'cap_bytes':CAP,'disk_before':disk('before')}
 save(evidence/'preflight.json',pre)
 if not pre['candidate_blobs_match'] or pre['baseline_head']!=BASELINE_HEAD or not pre['baseline_diff_empty'] or not pre['disk_before']['pass']:
  save(evidence/'run_summary.json',{'schema':'PYAT_W03_W04_ONE_PASS_PILOT_RUN_R1','status':'BLOCKED_EXACT_DEPENDENCY','reason':'PREFLIGHT_IDENTITY_OR_DISK','preflight':pre}); return 2
 env=os.environ.copy(); env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONPATH']=str(candidate)+(os.pathsep+env['PYTHONPATH'] if env.get('PYTHONPATH') else '')
 def cmd(scenario,profiles,source,root,jsonpath,baseline_json=None,gate=False):
  a=[sys.executable,'-B','-m','rawlsing_next.bench_w03_w04_physical','--scenario',scenario,'--profiles',profiles,'--rows','100000','--repetitions','1','--source-root',str(source),'--root',str(root),'--jsonpath',str(jsonpath),'--cap-bytes',str(CAP)]
  if baseline_json: a+=['--baseline-json',str(baseline_json)]
  if gate: a+=['--acceptance-gate']
  return a
 base_raw=evidence/'raw'/'baseline_narrow_cold_n1.json'; cand_raw=evidence/'raw'/'candidate_narrow_cold_n1.json'
 base_root=cache/'baseline-narrow-cold'; cand_root=cache/'candidate-narrow-cold'; marker=evidence/'first_child_launch.json'
 stages=[]
 # 1 baseline narrow cold
 bcomp=run_child('baseline_narrow_cold_n1',cmd('cold','narrow',baseline,base_root,base_raw),candidate,env,raw,marker)
 b_ok=base_raw.is_file()
 stages.append({'stage':'baseline_narrow_cold_n1','command':cmd('cold','narrow',baseline,base_root,base_raw),'json':str(base_raw),'json_sha256':sha(base_raw) if b_ok else None,'completion':bcomp,'disk_after':disk('after_baseline')})
 if b_ok:
  br={'baseline_json':str(base_raw),'baseline_json_sha256':sha(base_raw),'saved_before_candidate_comparison':True,'saved_utc':now()}
  save(evidence/'baseline_external_receipt.json',br)
  if base_root.exists():
   save(evidence/'raw'/'baseline_narrow_cold_n1.cache_usage.json',{'path':str(base_root),'bytes':sum(p.stat().st_size for p in base_root.rglob('*') if p.is_file())}); shutil.rmtree(base_root)
  # 2 candidate narrow cold, exact baseline bytes; gate is expected final_shape false at n=1
  ccomp=run_child('candidate_narrow_cold_n1',cmd('cold','narrow',candidate,cand_root,cand_raw,base_raw,gate=True),candidate,env,raw,None)
  c_ok=cand_raw.is_file()
  stages.append({'stage':'candidate_narrow_cold_n1','command':cmd('cold','narrow',candidate,cand_root,cand_raw,base_raw,gate=True),'json':str(cand_raw),'json_sha256':sha(cand_raw) if c_ok else None,'completion':ccomp,'disk_after':disk('after_candidate')})
  if c_ok:
   b=json.loads(base_raw.read_text()); c=json.loads(cand_raw.read_text())
   ba=b.get('results',{}).get('cold',{}).get('narrow',{}); ca=c.get('results',{}).get('cold',{}).get('narrow',{})
   b_run=ba.get('cold',{}).get('runs',[None])[0]; c_run=ca.get('cold',{}).get('runs',[None])[0]
   def pick(run,key):
    if not isinstance(run,dict): return None
    if key in run: return run[key]
    return run.get('metrics',{}).get(key)
   parity={
    'consumer_fingerprint_equal': b_run.get('consumer_fingerprint')==c_run.get('consumer_fingerprint') if b_run and c_run else False,
    'consumer_fact_states_equal': b_run.get('consumer_fact_states')==c_run.get('consumer_fact_states') if b_run and c_run else False,
    'event_count_equal': b_run.get('event_count')==c_run.get('event_count') if b_run and c_run else False,
    'cell_count_equal': b_run.get('cell_count')==c_run.get('cell_count') if b_run and c_run else False,
    'i05_fact_count_equal': b_run.get('i05_fact_count')==c_run.get('i05_fact_count') if b_run and c_run else False,
    'consumer_fact_count_equal': b_run.get('consumer_fact_count')==c_run.get('consumer_fact_count') if b_run and c_run else False,
    'baseline_values': {'consumer_fingerprint':b_run.get('consumer_fingerprint'),'consumer_fact_states':b_run.get('consumer_fact_states'),'event_count':b_run.get('event_count'),'cell_count':b_run.get('cell_count'),'i05_fact_count':b_run.get('i05_fact_count'),'consumer_fact_count':b_run.get('consumer_fact_count')},
    'candidate_values': {'consumer_fingerprint':c_run.get('consumer_fingerprint'),'consumer_fact_states':c_run.get('consumer_fact_states'),'event_count':c_run.get('event_count'),'cell_count':c_run.get('cell_count'),'i05_fact_count':c_run.get('i05_fact_count'),'consumer_fact_count':c_run.get('consumer_fact_count')},
   }
   obs={'baseline':{'wall_seconds':pick(b_run,'cold_combined_wall_seconds'),'rss_peak_bytes':pick(b_run,'cold_combined_rss_peak_bytes'),'launch_to_firstconsumer_seconds':pick(b_run,'launch_to_firstconsumer_seconds'),'derived_write_wall_seconds':pick(b_run,'derived_write_wall_seconds'),'derived_read_validation_wall_seconds':pick(b_run,'derived_read_validation_wall_seconds'),'cap_enforced':pick(b_run,'cap_enforced'),'cap_peak_sampled_bytes':pick(b_run,'cap_peak_sampled_bytes'),'status':b_run.get('status')},'candidate':{'wall_seconds':pick(c_run,'cold_combined_wall_seconds'),'rss_peak_bytes':pick(c_run,'cold_combined_rss_peak_bytes'),'launch_to_firstconsumer_seconds':pick(c_run,'launch_to_firstconsumer_seconds'),'derived_write_wall_seconds':pick(c_run,'derived_write_wall_seconds'),'derived_read_validation_wall_seconds':pick(c_run,'derived_read_validation_wall_seconds'),'cap_enforced':pick(c_run,'cap_enforced'),'cap_peak_sampled_bytes':pick(c_run,'cap_peak_sampled_bytes'),'status':c_run.get('status')}}
   comparison={'schema':'PYAT_W03_W04_ONE_PASS_PILOT_COMPARISON_R1','case':'cold/narrow','n':1,'rows':100000,'actual_event_count':b_run.get('event_count') if b_run else None,'cap_bytes':CAP,'baseline_external_receipt':'baseline_external_receipt.json','baseline_raw':str(base_raw),'candidate_raw':str(cand_raw),'baseline_raw_sha256':sha(base_raw),'candidate_raw_sha256':sha(cand_raw),'baseline_aggregate':ba.get('cold',{}).get('aggregate'),'candidate_aggregate':ca.get('cold',{}).get('aggregate'),'cold_vs_baseline':ca.get('cold_vs_baseline'),'observed':obs,'parity':parity,'candidate_acceptance':c.get('acceptance'),'gate_exit_code':ccomp.get('exit_code'),'gate_expected_final_shape_false':not bool(c.get('acceptance',{}).get('final_shape')),'economic_final_pass':False,'confidence_claim':None,'limits':['n=1 pilot only; no 3-run confidence or economic final PASS','same host/source/cap only','no source/native/science/actor acceptance']}
   save(evidence/'comparison.json',comparison)
  if cand_root.exists():
   save(evidence/'raw'/'candidate_narrow_cold_n1.cache_usage.json',{'path':str(cand_root),'bytes':sum(p.stat().st_size for p in cand_root.rglob('*') if p.is_file())}); shutil.rmtree(cand_root)
 else:
  stages.append({'stage':'candidate_narrow_cold_n1','status':'SKIPPED_BASELINE_NOT_AVAILABLE'})
 summary={'schema':'PYAT_W03_W04_ONE_PASS_PILOT_RUN_R1','status':'PAIR_COMPLETE' if (base_raw.is_file() and cand_raw.is_file()) else 'INCOMPLETE_OR_BLOCKED','started_utc':pre['started_utc'],'finished_utc':now(),'candidate_head':pre['candidate_head'],'source_blobs':pre['candidate_blobs'],'baseline_head':pre['baseline_head'],'case':'cold/narrow','n':1,'cap_bytes':CAP,'stages':stages,'comparison':'comparison.json' if (evidence/'comparison.json').is_file() else None,'acceptance_claimed':False,'economic_final_pass':False,'receiving_required':True}
 save(evidence/'run_summary.json',summary)
 return 0 if summary['status']=='PAIR_COMPLETE' else 2
if __name__=='__main__': raise SystemExit(main())
