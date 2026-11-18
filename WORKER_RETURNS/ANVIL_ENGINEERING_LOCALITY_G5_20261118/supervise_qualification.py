#!/usr/bin/env python3
"""Bounded external supervisor for the frozen-snapshot actual F4 qualification."""
from __future__ import annotations
import json, os, signal, subprocess, sys, time
from pathlib import Path
SELF=Path(__file__).resolve().parent
OWNER=SELF.parents[1]
MP=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117')
sys.path.insert(0,str(MP)); sys.path.insert(0,str(MP/'vendor'))
from court_instrumentation import directory_bytes, process_tree_rss_bytes
CAP=120.0; RSS=2*1024**3; SCRATCH=2*1024**3
cmd=[sys.executable,'-B',str(SELF/'qualify_snapshot.py')]
started=time.monotonic(); p=subprocess.Popen(cmd,cwd=str(OWNER),text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
samples=[]; aborted=None
while p.poll() is None:
    time.sleep(0.25); elapsed=time.monotonic()-started
    rss=process_tree_rss_bytes(p.pid); scratch=directory_bytes(MP/'.local-data-pilot')
    samples.append({'elapsed_seconds':elapsed,'process_tree_rss_bytes':rss,'scratch_bytes':scratch})
    if elapsed>CAP: aborted=f'WALL_LIMIT:{CAP}'
    elif rss>RSS: aborted=f'RSS_LIMIT:{rss}>{RSS}'
    elif scratch>SCRATCH: aborted=f'SCRATCH_LIMIT:{scratch}>{SCRATCH}'
    if aborted: break
if aborted:
    try: os.killpg(p.pid,signal.SIGTERM)
    except ProcessLookupError: pass
    try: p.wait(timeout=3)
    except subprocess.TimeoutExpired:
        try: os.killpg(p.pid,signal.SIGKILL)
        except ProcessLookupError: pass
        p.wait(timeout=3)
out,err=p.communicate(timeout=10)
child=json.loads((SELF/'qualification.json').read_text()) if (SELF/'qualification.json').exists() else None
sup={'schema':'ANVIL_ENGINEERING_LOCALITY_G5_SUPERVISION@1','command':cmd,'exit':p.returncode,'aborted':aborted,
 'external_wall_seconds':time.monotonic()-started,'sample_count':len(samples),
 'process_tree_rss_peak_sampled_bytes':max((s['process_tree_rss_bytes'] for s in samples),default=0),
 'scratch_peak_sampled_bytes':max((s['scratch_bytes'] for s in samples),default=0),
 'caps':{'wall_seconds':CAP,'rss_bytes':RSS,'scratch_bytes':SCRATCH,'sampling_seconds':0.25},
 'stdout':out,'stderr':err,'child':child}
(SELF/'supervision.json').write_text(json.dumps(sup,indent=2,sort_keys=True)+'\n')
(SELF/'samples.json').write_text(json.dumps(samples,indent=2,sort_keys=True)+'\n')
print(json.dumps({'exit':p.returncode,'aborted':aborted,'wall':sup['external_wall_seconds'],'rss':sup['process_tree_rss_peak_sampled_bytes'],'scratch':sup['scratch_peak_sampled_bytes'],'child':(child or {}).get('parity')},sort_keys=True))
raise SystemExit(p.returncode or (1 if aborted else 0))
