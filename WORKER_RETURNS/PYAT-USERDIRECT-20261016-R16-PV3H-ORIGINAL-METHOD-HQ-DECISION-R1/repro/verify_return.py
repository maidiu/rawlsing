"""Requirement audit of retained acceptance and current bounded handoff."""
import pathlib,json,hashlib,xml.etree.ElementTree as ET,sys
R=pathlib.Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'repro'))
from method_receipt import verify

def read(p):return json.loads((R/p).read_text())
def cases(p):return list(ET.parse(R/p).getroot().iter('testcase'))
def failing(cs):return {c.attrib['name'] for c in cs if c.find('failure') is not None}
cs=cases('evidence/handoff_junit.xml');assert len(cs)==16 and not any(c.find(k) is not None for c in cs for k in ['failure','error','skipped'])
raw=cases('evidence/raw_semantic_junit.xml');assert len(raw)==1 and failing(raw)=={'test_generic_native_labels_not_specialized_Q86'};assert raw[0].find('error') is None and raw[0].find('skipped') is None
prior=read('01_PINNED_PV3N_METHOD_ORIGINAL_EIGHT_AND_PROOF.json');oldfail=failing(cases('retained/pv2i_historical.xml'));newfail=failing(cases('retained/pv2i_adapter.xml'));assert oldfail-newfail==set(prior['retained_proof']['repaired_method_authority_assertions']) and len(oldfail-newfail)==21
receipt=read('method_receipts/BASELINE.json');h=verify(receipt);assert h==read('evidence/handoff/summary.json')['stable_method_receipt_hash']
assert receipt==read('evidence/handoff/first.json')['method_receipt']==read('evidence/handoff/replay.json')['method_receipt']
assert receipt['expected_root']==read('handoff_oracle.json')['original_expected_root'];assert receipt['counts']['total']==8 and receipt['counts']['held']==2
for name in ['R2_Y1','R1_Y0']:verify(read('method_receipts/'+name+'.json'));assert read('02_ACTUAL_SIX_CONSUMERS_AND_COLD_POSITIVE.json')['interventions'][name]['all_B_links_bitwise_stable']
for row in read('source_manifest.json'):
 b=(R/row['local']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob'];assert hashlib.sha256(b).hexdigest()==row['sha256']
assert len(read('native_74_source_manifest.json')['files'])==74
cold=read('evidence/handoff/summary.json');assert cold['first_pid']!=cold['replay_pid'];assert cold['processes'][0]['exit']==-9 and [p['exit'] for p in cold['processes'][1:]]==[0,0]
assert cold['first_new_durable']==[3,3] and cold['replay_new_durable']==[0,0] and cold['byte_identical_journals']
for k,v in read('handoff_oracle.json')['cold']['actual_replay_recomputation'].items():assert cold['recomputed_owner_calls'][k]==v
for name,digest in cold['journal_sha256'].items():assert hashlib.sha256((R/'evidence/handoff/native_journals'/name).read_bytes()).hexdigest()==digest
assert read('evidence/handoff/history_and_current.json')['original_history_verified'];assert read('evidence/handoff/offline.json')['claim']=='OFFLINE_FACT_RESTORATION_HOLD'
proposal=read('next_original_family_contract_proposal.json');assert proposal['implementation'] is None and proposal['semantic_signature'] is None and proposal['HQ_adoption'] is None
for name in ['00_ACCESSION_READY_NOT_ADOPTED.md','01_PINNED_PV3N_METHOD_ORIGINAL_EIGHT_AND_PROOF.json','02_ACTUAL_SIX_CONSUMERS_AND_COLD_POSITIVE.json','03_GENERIC_NATIVE_FIELD_FORGE_ISSUER_AND_EPRE_RIGHTS.md','04_NEXT_COMPETENT_HQ_POSITIVE_ADOPTION_GATE.md']:assert (R/name).is_file()
# Original48 source and observer support retain exact original bytes.
for a,b in [('retained/PV2I_original_48_cases.py','runtime/court/frozen_pv2i/tests/test_independent.py'),('repro/bootstrap.py','primary/pv3n/repro/bootstrap.py'),('repro/physical.py','primary/pv3n/repro/physical.py')]:assert (R/a).read_bytes()==(R/b).read_bytes()
excludes={'artifact_sha256.json','publication_receipt.json'}
files=[p for p in sorted(R.rglob('*')) if p.is_file() and not any(z in ('primary','runtime','__pycache__','.pytest_cache') for z in p.relative_to(R).parts) and p.name not in excludes and p.suffix!='.pyc']
manifest={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
if '--write' in sys.argv:(R/'artifact_sha256.json').write_text(json.dumps(manifest,indent=2)+'\n')
elif (R/'artifact_sha256.json').exists():assert manifest==read('artifact_sha256.json')
print('VERIFIED: 16 new handoff passes; one preserved raw semantic FAIL; all eight operations; six actual consumers; native74; cold/history/current/source effects; no adoption')
