#!/usr/bin/env python3
import json,os,signal,subprocess,sys,time,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[2]
sys.path.insert(0,str(REPO));sys.path.insert(0,str(REPO/'WORKER_RETURNS'/'ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117'/'vendor'))
from court_instrumentation import directory_bytes,process_tree_rss_bytes
def run(cmd,label,cap):
 start=time.monotonic();p=subprocess.Popen(cmd,cwd=str(REPO),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True);samples=[];abort=None
 while p.poll() is None:
  time.sleep(.25);e=time.monotonic()-start;r=process_tree_rss_bytes(p.pid);s=directory_bytes(HERE);samples.append({'elapsed':e,'rss':r,'scratch':s})
  if e>cap:abort='WALL_600S'
  elif r>6*1024**3:abort='RSS_6GIB'
  elif s>4*1024**3:abort='SCRATCH_4GIB'
  if abort:break
 if abort:
  try:os.killpg(p.pid,signal.SIGTERM)
  except ProcessLookupError:pass
  try:p.wait(timeout=3)
  except subprocess.TimeoutExpired:
   try:os.killpg(p.pid,signal.SIGKILL)
   except ProcessLookupError:pass
   p.wait(timeout=3)
 out,err=p.communicate(timeout=10);d={'label':label,'command':cmd,'exit':p.returncode,'abort':abort,'wall':time.monotonic()-start,'rss_peak':max((x['rss'] for x in samples),default=0),'scratch_peak':max((x['scratch'] for x in samples),default=0),'samples':len(samples),'stdout':out,'stderr':err};(HERE/f'{label}.json').write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');(HERE/f'{label}.samples.json').write_text(json.dumps(samples,indent=2,sort_keys=True)+'\n');print(json.dumps({'label':label,'exit':p.returncode,'abort':abort,'wall':d['wall'],'rss':d['rss_peak'],'scratch':d['scratch_peak']},sort_keys=True));return d
def main():
 if shutil.disk_usage(str(HERE)).free<8*1024**3:raise SystemExit('FREE_SPACE')
 snap=(HERE/'SNAPSHOT_PATH.txt').read_text().strip();b=run([sys.executable,str(HERE/'build_width128.py'),'--snapshot',snap,'--out',str(HERE/'.local-data-width128'),'--respondents','128','--questions','600'],'build',600.0)
 if b['exit'] or b['abort']:return 1
 q=run([sys.executable,str(HERE/'qualify_width128.py')],'query',600.0)
 return q['exit'] or (1 if q['abort'] else 0)
if __name__=='__main__':raise SystemExit(main())
