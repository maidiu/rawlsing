"""Grade observed executions and verify physical sources; never regenerate oracle."""
from pathlib import Path
from collections import Counter
import hashlib,json,sys,platform,subprocess,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];RT=R/'runtime_root'
def read(p):return json.loads((R/p).read_text())
def save(p,obj):(R/p).write_text(json.dumps(obj,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def suite(mode):
 result=[]
 for t in ET.parse(R/f'observations/{mode}.xml').getroot().iter('testcase'):
  node=next((t.find(x) for x in ('failure','error','skipped') if t.find(x) is not None),None)
  state='PASS' if node is None else node.tag.upper()
  result.append({'name':t.attrib['name'],'state':state,'message':None if node is None else node.attrib.get('message')})
 return {'counts':dict(Counter(t['state'] for t in result)),'cases':result,'terminal':read(f'observations/{mode}.terminal.json')}
suites={m:suite(m) for m in ('pv2_33','v2k_24','pv_21','owners_111','pv2i_historical','pv2i_adapter','pv3')}
for mode,n in [('pv2_33',33),('v2k_24',24),('pv_21',21),('owners_111',111),('pv3',28)]:assert suites[mode]['counts']=={'PASS':n}
assert suites['pv2i_historical']['counts']=={'PASS':26,'FAILURE':22}
assert suites['pv2i_adapter']['counts']=={'PASS':47,'FAILURE':1}
raw={t['name']:t for t in suites['pv2i_adapter']['cases']};events={r['name']:r for r in read('observations/pv2i_case_execution.json')}
assert len(events)==48
closure=[]
for old in suites['pv2i_historical']['cases']:
 if old['state']=='PASS':continue
 name=old['name'];generic=name=='test_generic_native_labels_not_specialized_Q86'
 assert raw[name]['state']==('FAILURE' if generic else 'PASS')
 closure.append({'case':name,'predecessor_observed':old,'pv3_raw_observed':raw[name],'disposition':'MANDATED_SEMANTIC_HOLD__GENERIC_READ_DENIED' if generic else 'REPAIRED_OBSERVED_PASS','strict_frozen_assertion_passes':not generic,'observed_execution':events[name],'additional_guard_evidence':'observations/generic_semantics_hold.json' if generic else None})
assert len(closure)==22
save('01_PV2I_TWENTYTWO_RED_CLOSURE.json',{'schema':'PV3_PV2I_RED_CLOSURE@1','scope':'TEST_ONLY sourcefree implementation, not independent acceptance/adoption','independent_oracle_sha256':sha(R/'authority/independent_oracle.json'),'summary':{'original_red':22,'repaired_raw_guards':21,'mandated_semantic_hold':1,'raw_pv2i_pass':47,'raw_pv2i_fail':1,'all_22_original_assertions_green':False,'all_22_edges_have_explicit_disposition':True},'cases':closure,'suites':suites,'adapter_contract':'repro/pv2i_adapter.py; repro/adapter_plugin.py. Legacy revocation test input is explicitly translated into a trusted fixture-owner control event; direct PV3 treats supplied registers as untrusted and never mutates owner state from them. No original assertion is replaced, skipped, xfailed or reauthored.'})
selector=read('source_selector.json');mapped={r['staged_path']:r for r in selector['files']}
for rel,row in mapped.items():
 data=(RT/rel).read_bytes();assert blob(data)==row['git_blob_sha1'] and sha(RT/rel)==row['sha256'],rel
verified=[];own_observers=[]
for p in sorted((R/'observations/owners_111_child_audits').glob('*.json')):
 d=json.loads(p.read_text())
 for row in d['imports']:
  path=Path(row['physical_file']);rel=str(path.relative_to(RT))
  if rel=='sitecustomize.py':
   assert path.read_bytes()==(R/'repro/sitecustomize.py').read_bytes();own_observers.append(row)
  else:
   assert rel in mapped,(rel,p)
   assert row['git_blob_sha1']==mapped[rel]['git_blob_sha1'],row
   verified.append(row)
physical=read('observations/physical_baseline.json')
for row in physical['imports']:
 p=Path(row['physical_file']);rel=str(p.relative_to(RT));assert row['git_blob_sha1']==mapped[rel]['git_blob_sha1']
for tag in ('cold_first','cold_replay'):
 audit=read(f'observations/{tag}.audit.json')
 for row in audit['imports']:
  p=Path(row['file']);rel=str(p.relative_to(RT))
  if rel=='sitecustomize.py':assert p.read_bytes()==(R/'repro/sitecustomize.py').read_bytes()
  else:assert row['git_blob_sha1']==mapped[rel]['git_blob_sha1'],(tag,rel)
assert sha(R/'authority/independent_oracle.json')=='321681bb0918e4119e3053aef8f0a6cb0d9db434eadc0a3225f897a686a55f79'
assert physical['report']['links']==read('authority/original_six_consumers.json')
assert len(physical['report']['links'])==6 and len(physical['report']['nonrunnable'])==2
save('observations/source_integrity_verification.json',{'staged_original_files':len(mapped),'all_original_blob_and_SHA256_bytes_unchanged':True,'actual_NUL_blob_preimages_verified':True,'physical_baseline_imports':physical['imports'],'owner_suite_processes':len(list((R/'observations/owners_111_child_audits').glob('*.json'))),'owner_suite_original_import_observations_verified':len(verified),'own_observer_imports_verified':len(own_observers),'all_six_original_links_exact':True,'V2K_original_blob':subprocess.check_output(['git','rev-parse','d1283fb53b543471fe825e78d64bf5bd19efbf11:rawlsing_next/pre553_original_identity_v2k_successor_candidate.py'],text=True).strip(),'PV21_original_test_blob':subprocess.check_output(['git','rev-parse','694fb45085cd5e4891949921a44edb77c3f603f2:rawlsing_next/tests/test_postastra_pv_v2k_independent.py'],text=True).strip()})
import pytest
save('environment_passport_delta.json',{'schema':'PV3_IMPLEMENTER_PASSPORT@1','platform':'Codex local authorized private repository','requested_model':'GPT-6.1 Sol High','python':sys.version,'python_executable':sys.executable,'pytest':pytest.__version__,'host_platform':platform.platform(),'timezone_for_user_dates':'America/New_York','sealed_startup':'4e3b5760a8c62c79272088a15f517e1590cdea6c','assigned_branch':subprocess.check_output(['git','branch','--show-current'],text=True).strip(),'predecessor_commits':{'PV2I':'1de1c9c57bffa8bb663edd44af744379b028f698','PV2':'c6ff1c3ec68d62fda478df8ceb2986b268b72dbf','V2K':'d1283fb53b543471fe825e78d64bf5bd19efbf11','PV':'694fb45085cd5e4891949921a44edb77c3f603f2'},'physical_source_selector':'source_selector.json','physical_import_verification':'observations/source_integrity_verification.json','original_frozen_oracle_sha256':sha(R/'authority/independent_oracle.json'),'original_R2_erratum':'frozen_pv2i/observations/PRE_EXECUTION_ORACLE_ERRATUM.json (exact Git bytes staged; manifest retained)','own_source_sha256':{str(p.relative_to(R)):sha(p) for p in sorted((R/'repro').glob('*.py'))},'compatibility_alias':'Exact HQ282 worker blob 84926e049d1879e48e9dcda7b1283de9d6cfc34d staged at the unchanged historic owner test HQ280 pathname; no worker/test rewrite','runtime_dependencies':'Python standard library + existing pytest; Black only used as isolated formatting tool, not needed to run candidate','authority_boundary':'Trusted local fixture installation/control capability outside ordinary request work/register arguments; no arbitrary Python/OS adversary isolation and no real source or institutionally independent U/E issuer','offline_fact_restoration':'HOLD; fresh process must source-bootstrap to attest live consumer material','canonical_or_V3_modified':False})
print('OBSERVED_CLOSURE_21_REPAIRED_1_MANDATED_HOLD; PHYSICAL_SOURCES_VERIFIED')

# Preserve the actually recovered byte artifacts, not just reconstructed hashes.
import shutil
cold=RT/'pv3_final_cold';copies=[]
for source in sorted((cold/'ledger').rglob('*')):
 if source.is_file() and source.suffix in ('.json','.jsonl'):
  dest=R/'observations/cold_ledger'/source.relative_to(cold/'ledger');dest.parent.mkdir(parents=True,exist_ok=True)
  dest.write_bytes(source.read_bytes());copies.append({'source':str(source),'copy':str(dest),'sha256':sha(source)})
for name in ('first.json','replay.json'):
 shutil.copyfile(cold/'observations'/name,R/'observations'/('cold_full_'+name))
save('observations/cold_ledger_byte_copies.json',copies)
