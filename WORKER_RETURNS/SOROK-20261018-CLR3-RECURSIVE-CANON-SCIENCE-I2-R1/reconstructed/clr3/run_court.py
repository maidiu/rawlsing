"""Reproduce CLR3 research evidence without rewriting any earlier return."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import gzip,hashlib,json,os,platform,re,subprocess,sys
import xml.etree.ElementTree as ET
from recursive_court import ROOT,run_trajectory,digest

OUT=ROOT/'evidence'


def write(name,value):
    (OUT/name).write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


def check_source_custody():
    inv=json.loads((ROOT/'sources/legacy_source_inventory.json').read_text())
    for row in inv['files']:
        b=(ROOT/'sources/legacy'/row['path']).read_bytes()
        assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row['path']
    for row in json.loads((ROOT/'preserved/manifest.json').read_text()):
        assert hashlib.sha256((ROOT/row['local_path']).read_bytes()).hexdigest()==row['sha256']
    return len(inv['files'])


def run():
    OUT.mkdir(exist_ok=True);source_count=check_source_custody();receipts=[]
    for name,cwd,test in [('clr3',ROOT,'test_recursive_court.py'),('original_six_red',ROOT/'preserved/r1_court','test_falsifiers.py')]:
        xml=OUT/(name+'.xml')
        args=[sys.executable,'-m','pytest','-v','-p','no:cacheprovider',test,'--junitxml='+os.path.relpath(xml,cwd)]
        result=subprocess.run(args,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        stdout=result.stdout.replace(str(ROOT),'<CLR3_RETURN>').replace(sys.executable,'<PYTHON>')
        (OUT/(name+'.log')).write_text(stdout)
        contents=xml.read_text();contents=re.sub(r'hostname="[^"]*"','hostname="local-host"',contents)
        xml.write_text(contents)
        suite=ET.parse(xml).getroot().find('testsuite')
        receipts.append(dict(suite=name,cwd=str(cwd.relative_to(ROOT)),command=['python3',*args[1:]],exit_code=result.returncode,**{k:int(suite.attrib[k]) for k in ('tests','failures','errors','skipped')}))
    traces={w:run_trajectory(w) for w in ('HOURS_CUT','ROUTINE','RAISE_WITH_OVERTIME')}
    traces['alternate_canon']=run_trajectory('ROUTINE',location='garage_shelf',variant='alternate')
    raw=json.dumps(traces,sort_keys=True,separators=(',',':')).encode()
    assert b'/Users/' not in raw,'Personal path in generated state evidence'
    payload=gzip.compress(raw,mtime=0);(OUT/'full_trajectories.json.gz').write_bytes(payload)
    assert json.loads(gzip.decompress(payload))==json.loads(raw)
    summary=[]
    for label,r in traces.items():
        summary.append(dict(scenario=label,trace_hash=r['trace_hash'],native_grade=r['native_grade'],initial_hash=digest(r['initial']),pre_encounter_hash=digest(r['pre_encounter']),workplace=r['resolved']['workplace'],father_response=r['resolved']['father_response'],father_present=r['resolved']['father_present'],effect_after_hash=r['immediate']['after_hash'],effect_numeric_changes=r['immediate']['numeric_changes'],canon_text=r['canon'][0]['text'],canon_hash=r['canon'][0]['hash'],later=r['later'],delayed_changes=r['delayed_feedback']['numeric_changes'],final_hash=digest(r['final_state']),final_age=r['final_state']['age'],final_social_support=r['final_state']['capacity']['social_support'],ticks=[dict(clock=t['clock'],age=t['after']['age'],after_hash=t['after_hash'],changed_sections=t['changed_sections'],numeric_change_count=len(t['numeric_changes']),rng_operation_count=len(t['rng_outputs']),pressure_status=t['pressure_status']) for t in r['ticks']]))
    write('trajectory_summary.json',summary)
    write('execution_receipts.json',dict(observed_utc=datetime.now(timezone.utc).isoformat(),python=platform.python_version(),pytest=subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),source_files_verified=source_count,suites=receipts,full_traces=dict(path='evidence/full_trajectories.json.gz',sha256=hashlib.sha256(payload).hexdigest(),uncompressed_bytes=len(raw)),scope='Historical provisional engine executed; current/native owner contracts UNISSUED; no independent acceptance',dependencies={'PyYAML':'6.0.2'},stdout_redaction='absolute CLR3 checkout/interpreter paths; JUnit host alias only'))
    check_source_custody()
    print(json.dumps(receipts,indent=2))
    assert [(r['tests'],r['failures'],r['errors'],r['skipped'],r['exit_code']) for r in receipts]==[(38,0,0,0,0),(6,6,0,0,1)]
    # Exit 1 preserves the original six REDs; it does not mean CLR3 passed native owners.
    return 1


if __name__=='__main__':raise SystemExit(run())
