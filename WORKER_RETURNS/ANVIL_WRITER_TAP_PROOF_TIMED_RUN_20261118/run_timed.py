#!/usr/bin/env python3
"""One supervised diagnostic run; retains caps, samples, progress, no retry."""
import json,os,signal,subprocess,sys,time,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE/'.local-data-width512-timed';SNAP=Path('/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/anvil-scale-06ulz7')
MP=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117')
sys.path.insert(0,str(MP/'vendor'))
from court_instrumentation import directory_bytes,process_tree_rss_bytes
CAP=600.0;RSS=6*1024**3;SCRATCH=4*1024**3;FREE=8*1024**3
def main():
 if ROOT.exists(): raise SystemExit(f'UNIQUE_OUTPUT_EXISTS:{ROOT}')
 if shutil.disk_usage(str(HERE)).free<FREE: raise SystemExit('FREE_SPACE_BELOW_8GIB')
 progress=HERE/'PROGRESS.json';cmd=[sys.executable,'-B',str(HERE/'timed_writer.py'),'--snapshot',str(SNAP),'--out',str(ROOT),'--respondents','512','--questions','600','--progress',str(progress)]
 env=dict(os.environ);env['PYTHONPATH']=f'{SNAP}:{MP}:{MP/"vendor"}';env['PYTHONDONTWRITEBYTECODE']='1';start=time.monotonic();p=subprocess.Popen(cmd,cwd=str(HERE),env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);samples=[];abort=None
 while p.poll() is None:
  time.sleep(.25);e=time.monotonic()-start;r=process_tree_rss_bytes(p.pid);s=directory_bytes(ROOT);samples.append({'elapsed':e,'rss':r,'scratch':s,'progress':str(progress) if progress.exists() else None})
  if e>CAP:abort='WALL_600S'
  elif r>RSS:abort='RSS_6GIB'
  elif s>SCRATCH:abort='SCRATCH_4GIB'
  if abort:break
 if abort:
  try:os.killpg(p.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  try:p.wait(timeout=3)
  except subprocess.TimeoutExpired:
   try:os.killpg(p.pid,signal.SIGKILL)
   except ProcessLookupError:pass
   p.wait(timeout=3)
 out,err=p.communicate(timeout=10);partial=directory_bytes(ROOT);res={'schema':'ANVIL_WIDTH512_TIMED_RUN@1','status':'CAPPED' if abort else ('EXITED' if p.returncode else 'PUBLISHED'),'command':cmd,'exit':p.returncode,'abort':abort,'wall':time.monotonic()-start,'rss_peak':max((x['rss'] for x in samples),default=0),'scratch_peak':max((x['scratch'] for x in samples),default=0),'partial_bytes':partial,'output_root':str(ROOT),'progress':str(progress),'samples':len(samples),'caps':{'wall':CAP,'rss':RSS,'scratch':SCRATCH,'free':FREE},'stdout':out,'stderr':err}
 (HERE/'RUN_RECEIPT.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n');(HERE/'SAMPLES.json').write_text(json.dumps(samples,indent=2,sort_keys=True)+'\n');(HERE/'STDOUT.txt').write_text(out);(HERE/'STDERR.txt').write_text(err);print(json.dumps({k:res[k] for k in ('status','exit','abort','wall','rss_peak','scratch_peak','partial_bytes')},sort_keys=True));return p.returncode or (1 if abort else 0)
if __name__=='__main__':raise SystemExit(main())
