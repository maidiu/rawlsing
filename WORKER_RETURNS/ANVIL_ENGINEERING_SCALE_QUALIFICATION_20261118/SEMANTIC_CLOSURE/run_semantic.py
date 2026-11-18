#!/usr/bin/env python3
import json,os,signal,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
sys.path.insert(0,str(REPO));sys.path.insert(0,str(REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'/'vendor'))
from court_instrumentation import directory_bytes,process_tree_rss_bytes
CAP=600.0;RSS=6*1024**3;SCRATCH=4*1024**3
def main():
 cmd=[sys.executable,str(HERE/'semantic_closure.py')];start=time.monotonic();p=subprocess.Popen(cmd,cwd=str(REPO),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);samples=[];abort=None
 while p.poll() is None:
  time.sleep(.25);elapsed=time.monotonic()-start;rss=process_tree_rss_bytes(p.pid);scratch=directory_bytes(HERE);samples.append({'elapsed_seconds':elapsed,'rss':rss,'scratch':scratch})
  if elapsed>CAP:abort='WALL_600S'
  elif rss>RSS:abort='RSS_6GIB'
  elif scratch>SCRATCH:abort='SCRATCH_4GIB'
  if abort:break
 if abort:
  try:os.killpg(p.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  try:p.wait(timeout=3)
  except subprocess.TimeoutExpired:
   try:os.killpg(p.pid,signal.SIGKILL)
   except ProcessLookupError:pass
   p.wait(timeout=3)
 out,err=p.communicate(timeout=10);s={'schema':'ANVIL_SEMANTIC_SUPERVISION@1','exit':p.returncode,'abort':abort,'wall':time.monotonic()-start,'rss_peak':max((x['rss'] for x in samples),default=0),'scratch_peak':max((x['scratch'] for x in samples),default=0),'samples':len(samples),'caps':{'wall_seconds':CAP,'rss_bytes':RSS,'scratch_bytes':SCRATCH},'stdout':out,'stderr':err}
 (HERE/'SUPERVISION.json').write_text(json.dumps(s,indent=2,sort_keys=True)+'\n');(HERE/'samples.json').write_text(json.dumps(samples,indent=2,sort_keys=True)+'\n');(HERE/'stdout.txt').write_text(out);(HERE/'stderr.txt').write_text(err);print(json.dumps({'exit':p.returncode,'abort':abort,'wall':s['wall'],'rss':s['rss_peak'],'scratch':s['scratch_peak']},sort_keys=True));return p.returncode or (1 if abort else 0)
if __name__=='__main__':raise SystemExit(main())
