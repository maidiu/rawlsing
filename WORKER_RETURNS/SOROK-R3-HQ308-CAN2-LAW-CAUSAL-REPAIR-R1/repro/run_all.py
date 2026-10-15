"""Rehydrate and execute unchanged historical courts plus repair controls.

Use a fresh tag. A runner exit0 means dispositions were captured, never scientific
acceptance. Tests retain actual failures; no xfail, skip, or inverted assertions.
"""
from pathlib import Path
import subprocess,sys,re,json,xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
RET=Path(__file__).resolve().parents[1]
if len(sys.argv)<2 or not re.fullmatch('[A-Za-z0-9_-]+',sys.argv[1]):raise SystemExit('Usage: run_all.py fresh_tag [original|repaired]')
tag=sys.argv[1];labels=[sys.argv[2]] if len(sys.argv)==3 else ['original','repaired']
assert all(x in ('original','repaired') for x in labels)
subprocess.run([sys.executable,str(RET/'repro/prepare.py')],check=True)
(RET/'evidence').mkdir(exist_ok=True)
def job(pair):
 label,suite=pair;cmd=[sys.executable,str(RET/'runtime_root'/('court_'+label)/'repro/run_suite.py'),suite+'__'+tag]
 log=RET/'evidence'/(label+'_'+suite+'_'+tag+'.log')
 with log.open('x') as stream:code=subprocess.run(cmd,stdout=stream,stderr=subprocess.STDOUT).returncode
 source=RET/'runtime_root'/('court_'+label)/'repro/runs'/(suite+'__'+tag)
 dest=RET/'evidence'/(label+'_'+suite+'_'+tag);dest.mkdir(exist_ok=False)
 for n in ('junit.xml','execution.json'):(dest/n).write_bytes((source/n).read_bytes())
 ss=list(ET.parse(dest/'junit.xml').getroot().iter('testsuite'));counts={k:sum(int(s.get(k,0)) for s in ss) for k in ('tests','failures','errors','skipped')}
 print(label,suite,code,counts,flush=True);return dict(label=label,suite=suite,exit_code=code,counts=counts,receipt=str(dest.relative_to(RET)))
with ThreadPoolExecutor(max_workers=4) as pool:rows=list(pool.map(job,[(l,s) for l in labels for s in ('owners','rsm','candidate','candidate_unset','reviewer')]))
if 'repaired' in labels:
 with (RET/'evidence'/('repair_'+tag+'.log')).open('x') as stream:code=subprocess.run([sys.executable,str(RET/'repro/run_repair.py'),tag],stdout=stream,stderr=subprocess.STDOUT).returncode
 print('repair controls exit',code,flush=True)
 if code:raise SystemExit(code)
(RET/'evidence'/('run_summary_'+tag+'.json')).write_text(json.dumps(rows,indent=2)+'\n')
if any(x['counts']['errors'] for x in rows):raise SystemExit('Collection/runtime errors require diagnosis')
