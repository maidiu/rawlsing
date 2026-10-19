"""Portable byte/receipt checks and optional three-world smoke, with no old Git refs.

Frozen scientific suites are not rerun. Fresh smoke != independent acceptance.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,sys
import xml.etree.ElementTree as ET

PUB=Path(__file__).resolve().parent
REPO=PUB.parents[2]
R2=PUB.parent
R1=R2.parent/'SOROK_CONTINGENT_LIVES_CAUSAL_COURT_R1'


def blob_sha(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()


def verify(smoke=False):
    manifest=json.loads((PUB/'source_blob_manifest.json').read_text())
    for row in manifest['files']:
        path=Path(row['path'])
        assert not path.is_absolute() and '..' not in path.parts
        data=(REPO/path).read_bytes()
        assert len(data)==row['bytes'] and blob_sha(data)==row['source_git_blob_sha1'],str(path)
        assert hashlib.sha256(data).hexdigest()==row['sha256'],str(path)
    inventories={}
    for root in (R1,R2):
        count=0
        for line in (root/'SHA256SUMS').read_text().splitlines():
            expected,name=line.split('  ',1)
            assert hashlib.sha256((root/name).read_bytes()).hexdigest()==expected,name
            count+=1
        inventories[root.name]=count
    suites=[]
    for name,expected in [('inherited',(24,0)),('controls',(23,0)),('original_falsifiers',(6,6)),('adjudication',(18,0))]:
        xml=R2/'evidence'/(name+'.xml')
        suite=ET.parse(xml).getroot().find('testsuite')
        tests,failures,errors,skips=(int(suite.attrib[k]) for k in ('tests','failures','errors','skipped'))
        assert (tests,failures)==expected and errors==skips==0
        suites.append(dict(name=name,claim='VERIFIED_PRIOR_RECEIPT',tests=tests,pass_count=tests-failures,failures=failures,errors=errors,skips=skips,sha256=hashlib.sha256(xml.read_bytes()).hexdigest()))
    compared=[]
    for name in ('baseline.json','baseline_traces.json','sensitivity.json','threshold_sensitivity.json','dag.json'):
        assert json.loads((R1/'evidence'/name).read_text())==json.loads((R2/'evidence'/name).read_text()),name
        compared.append(name)
    compiled=[]
    for row in manifest['files']:
        if row['path'].endswith('.py'):
            compile((REPO/row['path']).read_bytes(),row['path'],'exec')
            compiled.append(row['path'])
    smoke_result='NOT_REQUESTED'
    if smoke:
        source=R1/'inherited/causal_experiment'
        sys.path.insert(0,str(source))
        import world_intersection as candidate
        assert Path(candidate.__file__).resolve()==(source/'world_intersection.py').resolve()
        actual=candidate.output_table()
        assert actual==json.loads((R2/'evidence/baseline.json').read_text())
        smoke_result=dict(claim='EXECUTED_NOW_THREE_WORLD_SMOKE',scenarios=3,baseline_exact_match=True,imported_source=str((source/'world_intersection.py').relative_to(REPO)))
    return dict(checked_at_utc=datetime.now(timezone.utc).isoformat(),source_commit=manifest['source_local_commit'],sealed_startup=manifest['sealed_startup'],copied_source_blobs=len(manifest['files']),all_source_blobs_match=True,source_inventories=inventories,compiled_python_files=len(compiled),prior_suites=suites,prior_structured_outputs_match=compared,smoke=smoke_result,full_scientific_suites_rerun=False,independent_acceptance=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--smoke',action='store_true')
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    report=verify(args.smoke)
    rendered=json.dumps(report,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(rendered)
    print(rendered)
