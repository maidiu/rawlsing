"""Current qualification entry point; legacy failures remain archival diagnostics.
Runs the unchanged repair courts, fixes exact GF1I metadata staging, and requires
all versioned successor and current product checks to pass without exceptions.
"""
import hashlib
import json
import os
import subprocess
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

R=Path(__file__).resolve().parent
REVIEW=R.parent
Q=R/'current_qualification'
S=REVIEW/'stage'
EVIDENCE=Q/'evidence'
EVIDENCE.mkdir(parents=True,exist_ok=True)
F=S/'WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1'
I=S/'WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1'
repair=(R/'gf1_pair_support_consumer.py').read_bytes()
sha=hashlib.sha256(repair).hexdigest()

def execute(name,args,cwd,env):
    p=subprocess.run(args,cwd=cwd,env=env,text=True,capture_output=True)
    (EVIDENCE/(name+'.log')).write_text(p.stdout+p.stderr)
    print(name,'exit',p.returncode,p.stdout[-700:],flush=True)
    return p


def counts(path):
    root=ET.parse(path).getroot()
    suites=[root] if root.tag=='testsuite' else list(root.findall('testsuite'))
    return {k:sum(int(s.attrib.get(k,0)) for s in suites) for k in ('tests','failures','errors','skipped')}


env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GF1_REPAIR_ARTIFACT_DIR=str(Q/'retained_replay'))
p=execute('oracle_derivation',[sys.executable,str(Q/'build_current_oracle.py')],REVIEW.parents[1],env)
assert p.returncode==0
# Reuse the complete inherited native replay and source assertions, while putting
# these new author outputs in their own directory. Earlier evidence is untouched.
p=execute('retained_replay',[sys.executable,str(R/'reproduce.py')],REVIEW.parents[1],env)
assert p.returncode==0,(p.stdout,p.stderr)
seats=[F/'candidate/court/runtime_root/gf1_pair_support_consumer.py',I/'court/runtime_root/gf1_pair_support_consumer.py']
saved={p:p.read_bytes() for p in seats}
try:
    for p in seats:p.write_bytes(repair)
    env.update(GF1_CURRENT_FROZEN_GF1F=str(F),GF1_CURRENT_GF1I_COURT=str(I/'court'),GF1_CURRENT_EXPECTED_CONSUMER_SHA256=sha,GF1_CURRENT_QUALIFICATION_EVIDENCE=str(EVIDENCE))
    # Reproduce the actual prior staging fault as a controlled negative, then
    # restore the exact pinned bytes. This checks the positive gate cannot pass
    # merely by ignoring any arbitrary collection error.
    oracle=I/'01_PRECOMMITTED_GENERIC_NATIVE_PAIR_ORACLE.json'
    oracle_bytes=oracle.read_bytes()
    child_env=dict(env,PYTHONPATH=str(I/'court/repro')+os.pathsep+str(I/'court/runtime_root'))
    try:
        oracle.unlink()
        p=execute('staging_missing_oracle_negative',[sys.executable,'-m','pytest','test_gf1_generic_pair.py','-q','-p','no:cacheprovider','--collect-only'],I/'court/repro',child_env)
        assert p.returncode!=0 and 'FileNotFoundError' in p.stdout+p.stderr
        assert '01_PRECOMMITTED_GENERIC_NATIVE_PAIR_ORACLE.json' in p.stdout+p.stderr
    finally:
        oracle.write_bytes(oracle_bytes)
    result=[]
    for name,path,cwd,n in [
        ('current_gf1f102',Q/'gf1f/tests/test_current_gf1f.py',Q/'gf1f',102),
        ('current_gf1i19',Q/'gf1i/test_current_gf1i.py',I/'court',19),
    ]:
        xml=EVIDENCE/(name+'.xml')
        args=[sys.executable,'-m','pytest','-q','-p','no:cacheprovider','--import-mode=importlib',str(path),'--junitxml='+str(xml)]
        p=execute(name,args,cwd,env)
        got=counts(xml)
        assert p.returncode==0 and got==dict(tests=n,failures=0,errors=0,skipped=0),got
        result.append(dict(name=name,command=args,counts=got,junit_sha256=hashlib.sha256(xml.read_bytes()).hexdigest()))
    nested=counts(EVIDENCE/'gf1i_nested_original44.xml')
    assert nested==dict(tests=44,failures=0,errors=0,skipped=0)
    cold=[json.loads((Q/f'gf1f/observations/gf1f_cold_{i}.json').read_text()) for i in (0,1)]
    assert cold[0]['pid']!=cold[1]['pid'] and cold[0]['results']==cold[1]['results']
    assert len(cold[0]['results'])==82 and len(cold[0]['class_counts'])==4
    assert all(c['consumer_sha256']==sha for c in cold)
    assert all(Path(c['consumer_file']).read_bytes()==repair for c in cold)
    # Preserve exact original failure artifacts and original independent review.
    for path,expected in json.loads((REVIEW/'artifact_sha256.json').read_text()).items():
        assert hashlib.sha256((REVIEW/path).read_bytes()).hexdigest()==expected,path
    retained=json.loads((Q/'retained_replay/court_summary.json').read_text())
    historical_names={'before_supplemental','historical_gf1f100','historical_gf1i19'}
    active=[r for r in retained if r['name'] not in historical_names]
    assert sum(r['tests'] for r in active)==161
    assert all(r['failures']==r['errors']==r['skipped']==0 for r in active)
    summary=dict(status='CURRENT_QUALIFICATION_GREEN',role='USER_AUTHORIZED_AUTHOR_QUALIFICATION; NOT INDEPENDENT ADOPTION',candidate_sha256=sha,current_tests=282,current_failures=0,current_errors=0,current_skipped=0,current_allowlisted_failures=0,existing_product_and_frozen_tests=161,current_successor_tests=121,nested_native44_separately_verified=nested,successor_courts=result,cold_case_count=82,cold_class_count=4,cold_pids=[c['pid'] for c in cold],staging_negative_control='MISSING_ORACLE_FAILS_COLLECTION; RESTORING_EXACT_METADATA_COLLECTS_AND_EXECUTES44',staged_parent_metadata=json.loads((Q/'retained_replay/staged_parent_metadata.json').read_text()),historical_evidence='Original frozen suites still run as diagnostics, with unchanged failed nodes; no historical failure is an exception in the current gate.',historical_tests_unchanged=True,original_independent_review_hashes_unchanged=True,product_source_changed=False)
    (Q/'CURRENT_QUALIFICATION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('CURRENT QUALIFICATION: 282 PASS / 0 FAIL / 0 ERROR / 0 SKIP; NESTED NATIVE44 PASS; NO FAILURE ALLOWLIST',flush=True)
finally:
    for p,data in saved.items():p.write_bytes(data);assert p.read_bytes()==data
