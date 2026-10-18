"""Independent expectation and source checks; never obtains expected labels from consumer."""
import ast,json,subprocess,hashlib,collections
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parent;REPO=R.parents[1]
V=R/'stage/WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1';Q=V/'repair/current_qualification';S=V/'stage'
F='WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1';I='WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1';E='WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1'
def git(sha,path):return subprocess.check_output(['git','show',sha+':'+path],cwd=REPO)
def ids(b):return dict(sha256=hashlib.sha256(b).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest(),bytes=len(b))
candidate=V/'repair/gf1_pair_support_consumer.py';b=candidate.read_bytes()
assert ids(b)['sha256']=='00a5cc6adc8b6a4074e9ae63d0a57384a8c227e9c88a719683cb0304691a4f9b'
assert ids(b)['git_blob']=='3761730d975f3281e69f8038b337da62824e0baf'
assert b==git('d97a5df8c03d02ca3c7433937550cdb6774537b5','WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1/repair/gf1_pair_support_consumer.py')
files=[]
for row in json.loads((S/E/'court/source_selector.json').read_text())['files']:
 path=S/E/'court/runtime_root'/row['staged_path'];raw=path.read_bytes()
 assert raw==git(row['commit'],row['source_path'])
 if path.suffix=='.py':compile(raw,str(path),'exec')
 files.append(dict(row,independent_exact_git_bytes=True,physical_file=str(path)))
assert len(files)==74 and sum(Path(x['physical_file']).suffix=='.py' for x in files)==45
old=json.loads(git('3dcc7d7dddfff4f1be8b4293cab92e5b4275007d',F+'/01_INDEPENDENT_FROZEN_PAIR_ORACLE.json'))
cur=json.loads((Q/'gf1f/01_CURRENT_PAIR_ORACLE.json').read_text())
def expected(cells,risk):
 n=[cells[k] for k in ('00','01','10','11')]
 assert risk>=sum(n)>=0
 if risk==0:return 'UNDETERMINED_NO_ELIGIBLE_RISK'
 if sum(n)==0:return 'UNDETERMINED_ZERO_SUPPORT_RISK'
 a,b,c,d=n
 if a+b==0 or c+d==0:return 'UNDETERMINED_NO_ELIGIBLE_RISK'
 if (a>0 and d>0 and b==c==0) or (b>0 and c>0 and a==d==0):return 'EXACT_PAIR_SEPARATION'
 return 'NO_PAIR_SEPARATION'
assert len(old['universe'])==len(cur['universe'])==81
changed=[]
for n,(a,b) in enumerate(zip(old['universe'],cur['universe'],strict=True)):
 assert {k:v for k,v in a.items() if k!='expected_class'}=={k:v for k,v in b.items() if k!='expected_class'}
 assert b['expected_class']==expected(b['cells'],b['eligible'])
 if a['expected_class']!=b['expected_class']:changed.append(dict(index=n,old=a,current=b))
assert len(changed)==1
for name,c in cur['named_cases'].items():assert c['expected_class']==expected({k:c[k] for k in ('00','01','10','11')},c['eligible'])
assert len(cur['cold_extra_cases'])==1 and cur['cold_extra_cases'][0]['eligible']==2
for c in cur['cold_extra_cases']:assert c['expected_class']==expected(c['cells'],c['eligible'])
def functions(b):return {n.name:ast.dump(n,include_attributes=False) for n in ast.parse(b).body if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef))}
fun=[]
for name,pin,original,current in [('GF1F','3dcc7d7dddfff4f1be8b4293cab92e5b4275007d',F+'/tests/test_gf1f_independent_consumer.py',Q/'gf1f/tests/test_current_gf1f.py'),('GF1I','c6a55f0dd5b327c40d64f96e0705ab5485559e90',I+'/court/test_gf1i_independent.py',Q/'gf1i/test_current_gf1i.py')]:
 raw=git(pin,original);assert (S/original).read_bytes()==raw
 a,b=functions(raw),functions(current.read_bytes())
 fun.append(dict(suite=name,unchanged_functions=[k for k in a.keys()&b.keys() if a[k]==b[k]],modified_functions=[k for k in a.keys()&b.keys() if a[k]!=b[k]],removed_functions=sorted(a.keys()-b.keys()),added_functions=sorted(b.keys()-a.keys()),original=ids(raw),current=ids(current.read_bytes())))
counts=collections.Counter(expected(r['cells'],r['eligible']) for r in cur['universe']+cur['cold_extra_cases'])
assert dict(counts)==cur['cold_class_counts']
report=dict(candidate=ids(candidate.read_bytes()),original74=files,python45_compiled=True,universe81_retained=True,oracle_changes=changed,function_preservation=fun,independent_cold82_class_counts=dict(counts),expectations_derived_without_candidate_execution=True)
(R/'02_ORIGINAL74_ACTUAL_IMPORTED_SOURCE_AND_GIT_SHA.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='original74'},indent=2))
