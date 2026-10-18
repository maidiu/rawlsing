"""Run frozen tests and hostile courts, preserving genuine REDs and stdout/JUnit.

Exit 1 means scientific falsifiers are RED. It is not a packaging failure.
"""
from pathlib import Path
from dataclasses import asdict, replace
from datetime import datetime, timezone
import hashlib
import json
import platform
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from court import model as m, intervene, behavior, threshold_variant

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'evidence'

def write(name,value):
    (OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')

def run():
    OUT.mkdir(exist_ok=True)
    manifest=json.loads((ROOT/'inherited/manifest.json').read_text())
    for name,spec in manifest['files'].items():
        p=ROOT/'inherited'/name
        if p.exists():
            assert len(p.read_bytes())==spec['bytes']
            assert hashlib.sha256(p.read_bytes()).hexdigest()==spec['sha256']
    results=[]
    for name,cwd,test,junit in [
        ('inherited',ROOT/'inherited/causal_experiment','test_world_intersection.py','../../evidence/inherited.xml'),
        ('controls',ROOT,'test_controls.py','evidence/controls.xml'),
        ('falsifiers',ROOT,'test_falsifiers.py','evidence/falsifiers.xml')]:
        args=[sys.executable,'-m','pytest','-v',test,'--junitxml='+junit]
        p=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
        # Only host checkout/interpreter prefixes are redacted; test values and
        # failures remain verbatim. JUnit is actual pytest output.
        output=p.stdout.replace(str(ROOT),'<RETURN_ROOT>').replace(sys.executable,'<PYTHON>')
        (OUT/(name+'.log')).write_text(output)
        xml_path=OUT/(name+'.xml')
        xml_path.write_text(re.sub(r'hostname="[^"]*"', 'hostname="local-host"', xml_path.read_text()))
        tree=ET.parse(xml_path); suite=tree.getroot().find('testsuite')
        results.append(dict(suite=name,command=['python3',*args[1:]],cwd=str(cwd.relative_to(ROOT)),exit_code=p.returncode,tests=int(suite.attrib['tests']),failures=int(suite.attrib['failures']),errors=int(suite.attrib['errors']),skipped=int(suite.attrib['skipped'])))
    write('execution_receipts.json',dict(observed_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),pytest=subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),suites=results,redaction='stdout host checkout/interpreter prefixes and JUnit hostname alias only; test values unchanged'))
    traces=m.paired_counterfactual()
    write('baseline.json',m.output_table())
    write('baseline_traces.json',{label:asdict(t) for label,t in traces.items()})
    cases={
        'baseline':m.WorldParameters(),
        'cash_reserve_220':m.WorldParameters(father=m.FatherHistory(cash_buffer=220)),
        'protected_care_24':m.WorldParameters(father=m.FatherHistory(protected_care_min=24)),
        'no_prior_joint_repair':m.WorldParameters(father=m.FatherHistory(joint_repair_episodes=0)),
        'large_reserve_protected_care':m.WorldParameters(father=m.FatherHistory(cash_buffer=400,protected_care_min=35)),
        'child_no_practice_slots':m.WorldParameters(child=m.ChildHistory(weekday_practice_slots=0)),
        'child_prior_episodes_3':m.WorldParameters(child=m.ChildHistory(practical_bicycle_episodes=3)),
        'neighbor_unrelated_garden':m.WorldParameters(neighbor=m.NeighborHistory(independent_project='garden',independently_scheduled_shift_day4=False))}
    write('sensitivity.json',{name:dict(parameters=asdict(p),rows=m.output_table(params=p)) for name,p in cases.items()})
    write('threshold_sensitivity.json',{str(k):[dict(workplace=w,behavior=behavior(threshold_variant(k).simulate(w))) for w in m.WORK_OUTCOMES] for k in (2,3,4)})
    write('dag.json',{label:dict(nodes=[e.id for e in t.events],edges=[[p,e.id] for e in t.events for p in e.parents]) for label,t in traces.items()})
    (ROOT/'CAUSAL_DAG.mmd').write_text('flowchart TD\n'+''.join(f'  {p} --> {e.id}\n' for e in traces['ROUTINE'].events for p in e.parents))
    print(json.dumps(results,indent=2))
    return 1 if any(r['exit_code'] for r in results) else 0

if __name__=='__main__':
    raise SystemExit(run())
