from pathlib import Path
import subprocess,json,hashlib,uuid,datetime
R=Path(__file__).resolve().parents[1];ROOT=R.parents[1];RT=R/'runtime_root';RT.mkdir(exist_ok=False)
C='9c96f201f3530d2dae321201e9a913bb7a61800f';CP='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R10-E04-GENERIC-WORLD-POSSIBILITY-SERVICE-R1';I='54013488a181f25db7b10ef5220afc48d320fa37';IP='WORKER_RETURNS/PYAT-USERDIRECT-20261015-R11-E04I-INDEPENDENT-WORLD-SERVICE-R1';rows=[]
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0','-C',str(ROOT),*a])
def put(c,p,d):
 data=git('show',c+':'+p);blob=git('rev-parse',c+':'+p).decode().strip();assert subprocess.check_output(['git','hash-object','--stdin'],input=data).decode().strip()==blob
 assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==blob
 dest=RT/d;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data);rows.append(dict(commit=c,source_path=p,staged_path=d,git_blob_sha1=blob,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)));return data
selected_outputs={'outputs/experiment_summary.json','outputs/tests_native_final/execution.json','outputs/tests_native_final/junit.xml','outputs/tests_product_sanction_final/execution.json','outputs/tests_product_sanction_final/junit.xml'}
for p in git('ls-tree','-r','--name-only',C,CP).decode().splitlines():
 rel=p.removeprefix(CP+'/')
 if not rel.startswith('outputs/') or rel in selected_outputs:put(C,p,'candidate/'+rel)
for p in git('ls-tree','-r','--name-only',I,IP).decode().splitlines():put(I,p,'prior_E04I/'+p.removeprefix(IP+'/'))
oracle=RT/'prior_E04I/01_PRECOMMITTED_WORLD_AND_QUERY_ORACLES.json';(R/'E04I_ORIGINAL_FROZEN_ORACLE.json').write_bytes(oracle.read_bytes())
manifest=json.loads((RT/'candidate/source_manifest.json').read_text());assert len(manifest)==51
for row in manifest:
 put(row['commit'],row['path'],'candidate/'+row['local']);assert rows[-1]['git_blob_sha1']==row['blob_sha1'],row
(R/'source_selector.json').write_text(json.dumps({'candidate':C,'prior_independent':I,'files':rows,'native_source_manifest_count':len(manifest),'genuine_git_hash_object_and_NUL_preimages':True},indent=2)+'\n')
(R/'observations/runtime_marker.json').write_text(json.dumps({'environment_id':str(uuid.uuid4()),'epoch_id':str(uuid.uuid4()),'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'permission':'Local full-native synthetic test execution; no survey data, issuer, adoption or actor rights'},indent=2)+'\n')
(R/'observations/original_oracle.sha256').write_text(hashlib.sha256(oracle.read_bytes()).hexdigest()+'  E04I_ORIGINAL_FROZEN_ORACLE.json\n');print('STAGED_ORIGINALS',len(rows),'NATIVE',len(manifest),'ORACLE',hashlib.sha256(oracle.read_bytes()).hexdigest())

# Read-only opt-in process observer, not an original owner.
(RT/"candidate/runtime_root/source/sitecustomize.py").write_bytes((R/"repro/sitecustomize.py").read_bytes())
