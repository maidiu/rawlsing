from pathlib import Path
import subprocess,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def get(s,p):return subprocess.check_output(['git','-c','gc.auto=0','show',s+':'+p],cwd=ROOT)
def put(s,p,local,rows):
 b=get(s,p);oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();d=ROOT/local;d.parent.mkdir(parents=True,exist_ok=True)
 if d.exists():assert d.read_bytes()==b,'REFUSE_CHANGED_SOURCE '+local
 else:d.write_bytes(b)
 rows.append(dict(commit=s,path=p,local=local,git_blob=oid,sha256=hashlib.sha256(b).hexdigest()))
S='f524f60781e2e7e72278d04d6377fb1da877698a';SP='WORKER_RETURNS/PYAT-USERDIRECT-20261016-R14-E05S-INDEPENDENT-SELECTED-WORLD-R1/'
manifest=json.loads(get(S,SP+'source_manifest.json'));assert len(manifest)==401
rows=[]
for x in manifest:
 put(x['commit'],x['path'],'runtime/'+x['local'],rows);assert rows[-1]['git_blob']==x['git_blob'] and rows[-1]['sha256']==x['sha256']
T='79cb8244a5291218bde17142b93fc2419eade396';TP='WORKER_RETURNS/PYAT-USERDIRECT-20261016-R15-E04T-NATIVE-CURRENT-GRANT-REPAIR-R1/'
put(T,TP+'product/empirical.py','runtime/owners/e04t_empirical.py',rows)
(ROOT/'source_manifest.json').write_text(json.dumps(rows,indent=2)+'\n')
evidence=[]
for s,p in [(S,SP+x) for x in ['source_manifest.json','00_INDEPENDENT_VERDICT.md','execution_receipt.json']]+[('f1ca9c530f6f03053ca981b49eefc91b85be47b8','WORKER_RETURNS/PYAT-USERDIRECT-20261016-R16-E04U-INDEPENDENT-CURRENT-GRANT-COURT-R1/'+x) for x in ['source_manifest.json','00_INDEPENDENT_VERDICT.md','03_POSITIVE_BOTH_CLIENTS_CURRENT_COLD_AND_REVOCATION.md','04_SOURCE_RIGHTS_AND_ADOPTION_CEILING.md','preimage_and_frozen_test_proof.json']]:
 alias='e05s' if s==S else 'e04u';put(s,p,'evidence/'+alias+'/'+Path(p).name,evidence)
for name in ['__init__.py','service.py','world.py','nonparent.py','scenario.py']:
 b=get(T,TP+'product/'+name);original=(ROOT/'runtime/product'/name).read_bytes();assert b==original,'NONEMPIRICAL_E04T_MODULE_DIFFERS '+name
put('a71d19ec527502d797036241d9199205c5b0e78d','PYAT_CONTROL_ROOM/USERDIRECT_20261016_R17_THREE_METHOD_FANIN/00_INTAKE_AND_COMPETENT_HQ_DECISION_REQUEST.md','evidence/R17_FANIN.md',evidence)
(ROOT/'evidence_manifest.json').write_text(json.dumps(evidence,indent=2)+'\n')
print('Verified 401 unchanged E05S closure + separate E04T owner; five other E04T modules byte-identical')
