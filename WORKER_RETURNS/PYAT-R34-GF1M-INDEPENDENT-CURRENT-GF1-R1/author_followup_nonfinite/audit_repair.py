import json,hashlib,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parent;P=R.parent;O=R/'evidence'
def ids(raw):return dict(sha256=hashlib.sha256(raw).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest(),bytes=len(raw))
raw=(R/'gf1_pair_support_consumer.py').read_bytes();candidate=ids(raw)
records=[]
for file in sorted(O.rglob('*.xml')):
 root=ET.parse(file).getroot();cases=list(root.iter('testcase'))
 actual=dict(tests=len(cases),failures=sum(c.find('failure') is not None for c in cases),errors=sum(c.find('error') is not None for c in cases),skipped=sum(c.find('skipped') is not None for c in cases))
 declared={k:sum(int(s.attrib.get(k,0)) for s in root.iter('testsuite')) for k in actual};assert actual==declared
 records.append(dict(path=str(file.relative_to(R)),**actual,**ids(file.read_bytes())))
def rec(path):return next(x for x in records if x['path']=='evidence/'+path)
assert rec('before_author22.xml')['tests']==22 and rec('before_author22.xml')['failures']==8
for path,n in [('original_phase_a26.xml',26),('author_nonfinite22.xml',22),('qualification/gf1i_nested_original44.xml',44)]:
 got=rec(path);assert got['tests']==n and got['failures']==got['errors']==got['skipped']==0
names=['original44','gf1g26','gf1h26','gf1j_native_two_plus_positive','gf1l_frozen14','gf1k_author12','supplemental10','repair_storage_guard26']
active=[rec('retained/'+name+'.xml') for name in names]+[rec('qualification/'+name+'.xml') for name in ('current_gf1f102','current_gf1i19')]
assert sum(x['tests'] for x in active)==282 and all(x['failures']==x['errors']==x['skipped']==0 for x in active)
for rel,sha in json.loads((P/'artifact_sha256.json').read_text()).items():assert hashlib.sha256((P/rel).read_bytes()).hexdigest()==sha,rel
for rel in ('01_PHASE_A_FROZEN_INDEPENDENT_ORACLES_AND_COMMIT.json','03_REAL_JUNIT_282_NESTED44_COLD_AND_NEW_ADVERSARIALS/test_independent_domains.py'):
 path=P/rel;repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=R,text=True).strip())
 assert path.read_bytes()==subprocess.check_output(['git','show','3a5fdc8f49c8dbd8df434b6407f7a8f760321513:'+str(path.relative_to(repo))],cwd=repo)
source=json.loads((O/'native_source_provenance.json').read_text());assert source['native_file_count']==74 and source['python_files']==45 and source['candidate']['sha256']==candidate['sha256']
cold82=[json.loads((O/f'cold82_{i}.json').read_text()) for i in (0,1)]
assert cold82[0]['pid']!=cold82[1]['pid'] and cold82[0]['results']==cold82[1]['results'] and len(cold82[0]['results'])==82
assert all(x['consumer_sha256']==candidate['sha256'] for x in cold82)
cold=[json.loads((O/f'cold_refusal_{i}.json').read_text()) for i in (0,1)]
a,b=[dict(x) for x in cold];assert a.pop('pid')!=b.pop('pid') and a==b
assert all(len(x['cases'])==12 and x['consumer_sha256']==candidate['sha256'] for x in cold)
summary=dict(role='USER_AUTHORIZED_AUTHOR_FOLLOWUP_NOT_INDEPENDENT_ACCEPTANCE',status='AUTHOR_VALIDATION_PASS__FRESH_INDEPENDENT_REVIEW_REQUIRED',candidate=candidate,base_candidate_commit='d97a5df8c03d02ca3c7433937550cdb6774537b5',original_review_commit='d5714ce5360d9b0f2319f4cb36e409af8e1e948e',original_review_and_all_frozen_tests_unchanged=True,current282=dict(tests=282,failures=0,errors=0,skipped=0),nested44=dict(tests=44,failures=0,errors=0,skipped=0),original_independent26=dict(tests=26,failures=0,errors=0,skipped=0),new_author22=dict(tests=22,failures=0,errors=0,skipped=0),cold82_pids=[x['pid'] for x in cold82],cold_refusal12_pids=[x['pid'] for x in cold],source_native_files=74,source_python_files=45,xml=records)
(O/'AUTHOR_VALIDATION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
for file in R.rglob('*.py'):
 if 'stage' not in file.relative_to(R).parts:compile(file.read_bytes(),str(file),'exec')
print('Actual JUnit/source/cold/frozen-artifact audits pass; author validation only')
