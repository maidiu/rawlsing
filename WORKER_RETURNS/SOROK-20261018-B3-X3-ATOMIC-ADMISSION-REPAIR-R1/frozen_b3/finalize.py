"""Audit exact evidence, sanitize portable copies and seal an artifact hash manifest."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,platform,re,sqlite3,subprocess,sys,uuid
import xml.etree.ElementTree as ET
from materialize import ROOT,RUNTIME,dump
from sources import identities
from integration import digest,GRADE

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def portable(s):
 s=s.replace(str(ROOT),'<B3_RETURN>').replace(str(Path.home()),'<HOME>')
 s=re.sub(r'/(?:private/)?var/folders/[^\s\'\"<>]*','<TEMP>',s)
 return s

def totals(path):
 root=ET.parse(path).getroot();suites=list(root.iter('testsuite'))
 return {k:sum(int(s.get(k,'0')) for s in suites) for k in ('tests','failures','errors','skipped')}

def main():
 # Only new portable evidence copies are transformed. Exact staged sources aren't.
 for path in (ROOT/'evidence').rglob('*'):
  if not path.is_file():continue
  if path.suffix=='.xml':
   tree=ET.parse(path)
   for node in tree.iter():
    node.attrib.pop('hostname',None)
    for k,v in list(node.attrib.items()):node.set(k,portable(v))
    if node.text:node.text=portable(node.text)
    if node.tail:node.tail=portable(node.tail)
   tree.write(path,encoding='utf-8',xml_declaration=True)
  elif path.suffix in ('.json','.log','.txt'):path.write_text(portable(path.read_text()))
 for r in json.loads((ROOT/'source_manifest.json').read_text()):
  assert sha(ROOT/r['local'])==r['sha256'],r['local']
 result={}
 for label,n,fail in [('b3_final',71,0),('inherited/r1_45',45,0),('inherited/repair_5',5,0),('inherited/e2_strict',2,0),('inherited/e2_full',44,2),('inherited/x2',17,1),('inherited/m2_41',41,0),('inherited/m1_37_on_m2',37,19),('inherited/i2_23_on_m2',23,10),('inherited/m3_source_preimage_3_red',3,3)]:
  actual=totals(ROOT/'evidence'/(label+'.xml'));assert actual==dict(tests=n,failures=fail,errors=0,skipped=0),(label,actual);result[label]=actual
 inherited=json.loads((ROOT/'evidence/inherited/b2_execution_receipt.json').read_text())
 assert inherited['f1']['raw_native_exit']==1 and inherited['f1']['raw_native_failures']==17
 native=json.loads((ROOT/'evidence/inherited/b2/f1_native_gate.log').read_text())
 assert native['status']=='RED' and len(native['failures'])==17
 for label,n in [('b1',39),('p1',74),('f1',97),('integration',81)]:
  assert totals(ROOT/'evidence/inherited/b2'/(label+'.xml'))==dict(tests=n,failures=0,errors=0,skipped=0)
 assert '22 / 22' in (ROOT/'evidence/inherited/b2/d1_original.log').read_text()
 assert '17 / 17' in (ROOT/'evidence/inherited/b2/d1_corrected.log').read_text()
 f2=json.loads((ROOT/'F2_CASE_MATRIX.json').read_text());assert f2['totals']==dict(PASS=42,RED=0,NOT_APPLICABLE=0)
 assert sum(x['actual_status']=='ELIGIBLE_NONCAUSAL' for x in f2['cases'])==20
 assert len(f2['cases'])==42 and len({x['case_id'] for x in f2['cases']})==42
 mutation=json.loads((ROOT/'evidence/b3_mutation_receipt.json').read_text());assert all(x['killed'] for x in mutation['mutants'].values())
 sql={}
 for label,expected_middle in [('positive',1),('permission_absent',0)]:
  live=json.loads((ROOT/'evidence/loop'/(label+'.json')).read_text());cold=json.loads((ROOT/'evidence'/(label+'_cold.log')).read_text())
  assert cold['receipts']==[ep['receipt'] for ep in live['episodes']]
  assert cold['snapshot_hash']==live['snapshot_hash'] and len(live['final_middle'])==expected_middle
  early=live['episodes'][0]['receipt']['M2_temporal_traces'][0]
  assert early['clock']==3 and early['actual_speech_ids']==[]
  assert live['episodes'][-1]['actor_actions'][-1]['action']=='DECLINE_CONTACT'
  for suffix in ('','_cold'):
   db=sqlite3.connect(ROOT/'evidence/loop'/(label+suffix+'.sqlite'))
   assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok'
   snapshot={n:db.execute('SELECT * FROM '+n+' ORDER BY 1').fetchall() for (n,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")}
   assert digest(snapshot)==live['snapshot_hash']
   source=json.loads(db.execute("SELECT body FROM b3_source WHERE id='loss:t3'").fetchone()[0]);assert source['content']['fact']=='stolen'
   sql[label+suffix]=dict(integrity='ok',snapshot_hash=digest(snapshot),table_rows={k:len(v) for k,v in snapshot.items()},sha256=sha(ROOT/'evidence/loop'/(label+suffix+'.sqlite')))
   db.close()
 # Audit exact frozen failure names as well as counts.
 failed={}
 for label in ('e2_full','x2','m1_37_on_m2','i2_23_on_m2','m3_source_preimage_3_red'):
  failed[label]=[n.get('name') for n in ET.parse(ROOT/'evidence/inherited'/(label+'.xml')).iter('testcase') if n.find('failure') is not None]
 assert failed['e2_full']==['test_direct_b1_after_wrapper_limit_is_measured[False]','test_direct_b1_after_wrapper_limit_is_measured[True]']
 assert failed['x2']==['test_same_event_id_accepts_distinct_objective_payload_hashes']
 branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
 assert branch=='agent/rabochii-sorok-v2-hq329-b3-coupled-interpretation-prototype-r1'
 changed=subprocess.check_output(['git','diff','--name-only','63f07960eb04cc856d94ed85f4c3c597f2f6bc9e'],cwd=ROOT.parent.parent,text=True).splitlines()
 assert all(p.startswith('WORKER_RETURNS/SOROK-V2-HQ329-B3-COUPLED-INTERPRETATION-R1/') for p in changed),changed
 now=datetime.now(timezone.utc).isoformat();marker=RUNTIME/'runtime_marker.json'
 if not marker.exists():dump(marker,dict(environment_id=str(uuid.uuid4()),epoch_id=str(uuid.uuid4()),opaque_marker=str(uuid.uuid4())))
 identity=json.loads(marker.read_text())
 receipt=dict(grade=GRADE,passed=True,startup='63f07960eb04cc856d94ed85f4c3c597f2f6bc9e',branch=branch,
  required_suites=result,inherited=inherited['totals'],f1_native_status='RED',f1_native_failed_cases=native['failures'],
  preserved_failed_assertions=failed,f2=f2['totals'],sql_cold_replay=sql,loaded_modules=identities(),
  E3=dict(commit='a16ba353f3bc471776d60ce198f267be4e9e5773',verdict='SOURCEFREE_BFIRST_EVENT_CUSTODY_ACCEPT_SCOPED'),
  M3=dict(commit='49dfcb30971310756a12f659961600d9f2eb4a11',verdict='REVISE_SOURCE_PREIMAGE',independence='NOT_MET',durable_m2_use='QUARANTINED'),
  no_original_sources=True,no_model_calls=True,no_semantic_adoption=True,portable_sanitation='PATHS_AND_XML_HOSTNAME_ONLY_SOURCE_BYTES_UNCHANGED')
 dump(ROOT/'verification_receipt.json',receipt)
 versions={'python':sys.version.split()[0],'pytest':__import__('pytest').__version__,'sqlite':sqlite3.sqlite_version,'git':subprocess.check_output(['git','--version'],text=True).strip(),'node':subprocess.check_output(['node','--version'],text=True).strip()}
 passport=dict(passport_schema='SOROK_WARM_ENVIRONMENT_PASSPORT_R1',environment_id=identity['environment_id'],epoch_id=identity['epoch_id'],owner_session_alias='B3_IMPLEMENTER',surface='LOCAL_SHARED_STORE',machine_alias='LOCAL_B3',conversation_or_account_affinity=None,status='LIVE_VERIFIED',last_live_probe_at=now,runtime_marker_digest=sha(marker),probe_command_and_result=versions,capabilities={k:'VERIFIED' for k in ('python','pytest','sqlite','git','node','filesystem','bash')},git_object_store_alias='EXISTING_CANONICAL_SHARED_STORE',worktree_alias='HQ329-B3-coupled-interpretation-wt',branch=branch,exact_checkout_base='63f07960eb04cc856d94ed85f4c3c597f2f6bc9e',head_at_return='REPORTED_EXTERNALLY_AFTER_PUSH',clean_dirty_state='ONLY_COMMISSIONED_RETURN_CHANGES_PLUS_UNRELATED_UNTRACKED_DESKTOP_METADATA',materialized_source_refs='source_manifest.json',verified_imports=identities(),dependency_closure_status='BOUNDED',fixture_query_source_permission='USER_AUTHORIZED_SYNTHETIC_ONLY',covered_test_suites='verification_receipt.json',actual_commands='evidence/run_commands.json and evidence/inherited/commands.json',science_grade=GRADE,model_provider='CODEX',model_effort='USER_REQUESTED_GPT6_MEDIUM_ACTUAL_RUNTIME_SELECTION_UNVERIFIED',pricing_class='UNKNOWN',observed_usage={'primary_used_percent':56,'secondary_used_percent':23,'cash_charges':None,'source':'LIVE_ACCOUNT_TOOL_AT_RETURN_PREPARATION'},independent_review_separation='B3_AUTHOR_NOT_ACCEPTANCE_REVIEWER; E3_SCOPED_INPUT; M3_INDEPENDENCE_NOT_MET; FRESH_I2_REQUIRED',privacy_source_grant='NO_ORIGINAL_SURVEY_NO_EXTERNAL_MODEL_DISCLOSURE',assignments_completed=['B3_INTEGRATED_RESEARCH_CANDIDATE'],next_good_affinity_tags=['B2','M2_QUARANTINE','SOURCE_PREIMAGE','CAN008','CAN011','SQLITE','F2'],staged_state_preservation='LIVE_LOCAL_RECHECK_REQUIRED_ON_RESUME',retire_or_rebuild_reason=None,attestation='00C_READ=YES;00D_WARM_PASSPORT_READ=YES;LIVE_RESOURCE_CHECK=YES;REAL_SESSION_CONTINUITY_VERIFIED_OR_NEW=YES;CHEAPEST_QUALIFIED_ROUTE_EVALUATED=YES;INDEPENDENCE_AND_AUTHORITY_PRESERVED=YES')
 dump(ROOT/'environment_passport_delta.json',passport)
 # Hash every delivered file except this self-referential manifest and ignored staging.
 files=[]
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file() or any(x in p.relative_to(ROOT).parts for x in ('.runtime','__pycache__','.pytest_cache')) or p.name=='artifact_manifest.json' or p.suffix=='.b3lock':continue
  files.append(dict(path=str(p.relative_to(ROOT)),bytes=p.stat().st_size,sha256=sha(p)))
 dump(ROOT/'artifact_manifest.json',dict(grade=GRADE,files=files))
 print(json.dumps(dict(grade=GRADE,b3_tests=71,f2=f2['totals'],f1_native_red=17,files=len(files)),sort_keys=True))
if __name__=='__main__':main()
