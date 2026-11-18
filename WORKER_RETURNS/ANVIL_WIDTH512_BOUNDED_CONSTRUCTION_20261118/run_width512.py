#!/usr/bin/env python3
import json,os,signal,subprocess,sys,time,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1];MP=REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'
sys.path.insert(0,str(MP/'vendor'))
from court_instrumentation import directory_bytes,process_tree_rss_bytes
CAP=600.0;RSS=6*1024**3;SCRATCH=4*1024**3;FREE=8*1024**3;ROOT=HERE/'.local-data-width512'
def main():
 if shutil.disk_usage(str(HERE)).free<FREE: raise SystemExit('FREE_SPACE_BELOW_8GIB')
 snap=(HERE/'SNAPSHOT_PATH.txt').read_text().strip();cmd=[sys.executable,str(HERE/'build_width512.py'),'--snapshot',snap,'--out',str(ROOT),'--respondents','512','--questions','600'];start=time.monotonic();p=subprocess.Popen(cmd,cwd=str(REPO),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);samples=[];abort=None
 while p.poll() is None:
  time.sleep(.25);e=time.monotonic()-start;r=process_tree_rss_bytes(p.pid);s=directory_bytes(ROOT);samples.append({'elapsed':e,'rss':r,'scratch':s})
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
 out,err=p.communicate(timeout=10);stage=None
 try:stage=json.loads((HERE/'BUILD_STAGES.json').read_text())
 except Exception:pass
 partial=directory_bytes(ROOT);res={'schema':'ANVIL_WIDTH512_BUILD_SUPERVISION@1','status':'CAPPED' if abort else ('EXITED' if p.returncode else 'PUBLISHED'),'command':cmd,'exit':p.returncode,'abort':abort,'wall':time.monotonic()-start,'rss_peak':max((x['rss'] for x in samples),default=0),'scratch_peak':max((x['scratch'] for x in samples),default=0),'partial_bytes':partial,'stage':stage,'samples':len(samples),'caps':{'wall':CAP,'rss':RSS,'scratch':SCRATCH,'free':FREE},'stdout':out,'stderr':err}
 (HERE/'BUILD_SUPERVISION.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n');(HERE/'BUILD_SAMPLES.json').write_text(json.dumps(samples,indent=2,sort_keys=True)+'\n');(HERE/'BUILD_STDOUT.txt').write_text(out);(HERE/'BUILD_STDERR.txt').write_text(err);print(json.dumps({k:res[k] for k in ('status','exit','abort','wall','rss_peak','scratch_peak','partial_bytes')},sort_keys=True));return p.returncode or (1 if abort else 0)
if __name__=='__main__':raise SystemExit(main())
