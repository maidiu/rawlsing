#!/usr/bin/env python3
"""External supervision for ONE 10k build."""
from __future__ import annotations
import json,os,shutil,signal,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent; REPO=HERE.parents[2]
sys.path.insert(0,str(REPO));sys.path.insert(0,str(REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'/'vendor'))
from court_instrumentation import directory_bytes,process_tree_rss_bytes
CAP=600.0;RSS=6*1024**3;SCRATCH=4*1024**3;FREE=8*1024**3
def main():
 if shutil.disk_usage(str(HERE)).free<FREE: raise SystemExit('ABORT_FREE_SPACE_BELOW_8GIB')
 cmd=[sys.executable,str(HERE/'build_10k_estate.py')]+sys.argv[1:];start=time.monotonic();p=subprocess.Popen(cmd,cwd=str(REPO),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);samples=[];abort=None
 while p.poll() is None:
  time.sleep(.25);elapsed=time.monotonic()-start;rss=process_tree_rss_bytes(p.pid);scratch=directory_bytes(HERE);samples.append({'elapsed_seconds':elapsed,'rss':rss,'scratch':scratch})
  if elapsed>CAP:abort='BUILD_WALL_600S'
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
 out,err=p.communicate(timeout=10);summary={'schema':'ANVIL_SCALE_BUILD_SUPERVISION@1','command':cmd,'exit':p.returncode,'abort':abort,'external_wall_seconds':time.monotonic()-start,'rss_peak_sampled':max((s['rss'] for s in samples),default=0),'scratch_peak_sampled':max((s['scratch'] for s in samples),default=0),'samples':len(samples),'caps':{'wall_seconds':CAP,'rss_bytes':RSS,'scratch_bytes':SCRATCH,'free_bytes_required':FREE},'stdout':out,'stderr':err}
 (HERE/'BUILD_SUPERVISION.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n');(HERE/'BUILD_SAMPLES.json').write_text(json.dumps(samples,indent=2,sort_keys=True)+'\n');(HERE/'BUILD_STDOUT.txt').write_text(out);(HERE/'BUILD_STDERR.txt').write_text(err)
 print(json.dumps({k:summary[k] for k in ('exit','abort','external_wall_seconds','rss_peak_sampled','scratch_peak_sampled')},sort_keys=True));return p.returncode or (1 if abort else 0)
if __name__=='__main__':raise SystemExit(main())
