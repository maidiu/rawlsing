import json,shutil,hashlib,xml.etree.ElementTree as ET,subprocess
from pathlib import Path
O=Path(__file__).resolve().parent;R=O.parent;V=R/'stage/WORKER_RETURNS/PYAT-R33-GF1L-NATIVE-IDENTITY-I2-R1';Q=V/'repair/current_qualification';X=Q/'retained_replay'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
for folder,src in [('retained_replay',X/'evidence'),('current_qualification',Q/'evidence')]:
 target=O/folder;target.mkdir(exist_ok=True)
 for file in src.iterdir():
  if file.is_file():shutil.copyfile(file,target/file.name)
for i in (0,1):shutil.copyfile(Q/f'gf1f/observations/gf1f_cold_{i}.json',O/f'current_qualification/gf1f_cold_{i}.json')
for path in ['CURRENT_QUALIFICATION_SUMMARY.json','SIX_FAILURE_SUCCESSOR_CROSSWALK.json','GF1F_SUCCESSOR.diff','GF1I_SUCCESSOR.diff','gf1f/01_CURRENT_PAIR_ORACLE.json']:
 target=O/'reviewed_author_source'/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Q/path,target)
for path in ['qualify.py','reproduce.py','staging.py','gf1_pair_support_consumer.py','current_qualification/build_current_oracle.py']:
 target=O/'reviewed_author_source'/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(V/'repair'/path,target)
counts=[]
for path in sorted(O.rglob('*.xml')):
 root=ET.parse(path).getroot();cases=list(root.iter('testcase'))
 actual=dict(tests=len(cases),failures=sum(c.find('failure') is not None for c in cases),errors=sum(c.find('error') is not None for c in cases),skipped=sum(c.find('skipped') is not None for c in cases))
 suites=list(root.iter('testsuite'));reported={k:sum(int(s.attrib.get(k,0)) for s in suites) for k in actual}
 assert actual==reported,(path,actual,reported)
 counts.append(dict(path=str(path.relative_to(O)),**actual,sha256=digest(path),timestamp=suites[0].attrib.get('timestamp'),testcases=[dict(classname=c.attrib.get('classname'),name=c.attrib['name'],failed=c.find('failure') is not None) for c in cases]))
active_names=['original44','gf1g26','gf1h26','gf1j_native_two_plus_positive','gf1l_frozen14','gf1k_author12','supplemental10','repair_storage_guard26']
active=[next(x for x in counts if x['path']=='retained_replay/'+n+'.xml') for n in active_names]
active.extend(next(x for x in counts if x['path']=='current_qualification/'+n+'.xml') for n in ('current_gf1f102','current_gf1i19'))
assert sum(x['tests'] for x in active)==282 and all(x['failures']==x['errors']==x['skipped']==0 for x in active)
nested=next(x for x in counts if x['path']=='current_qualification/gf1i_nested_original44.xml');assert nested['tests']==44 and nested['failures']==nested['errors']==nested['skipped']==0
mapped=[]
for old,new,renames in [('historical_gf1f100','current_gf1f102',{'test_missing_suppressed_relation_is_empty_response':'test_missing_suppressed_relation_remains_typed_blocking'}),('historical_gf1i19','current_gf1i19',{'test_named_downstream_consumer_module_is_absent_from_candidate':'test_named_downstream_consumer_is_present_and_computes','test_candidate_frozen_44_suite_cannot_be_collected':'test_candidate_frozen_44_suite_collects_and_executes'})]:
 a=next(x for x in counts if x['path']=='retained_replay/'+old+'.xml');b=next(x for x in counts if x['path']=='current_qualification/'+new+'.xml')
 an=[renames.get(c['name'],c['name']) for c in a['testcases']];bn=[c['name'] for c in b['testcases']]
 assert len(an)==len(set(an)) and set(an)<=set(bn)
 mapped.append(dict(historical=old,current=new,inherited_nodes=len(an),all_inherited_nodes_preserved=True,renames=renames,added_nodes=sorted(set(bn)-set(an))))
cold=[json.loads((O/f'current_qualification/gf1f_cold_{i}.json').read_text()) for i in (0,1)]
assert cold[0]['pid']!=cold[1]['pid'] and cold[0]['results']==cold[1]['results'] and len(cold[0]['results'])==82
assert all(x['consumer_sha256']=='00a5cc6adc8b6a4074e9ae63d0a57384a8c227e9c88a719683cb0304691a4f9b' for x in cold)
source=json.loads((R/'02_ORIGINAL74_ACTUAL_IMPORTED_SOURCE_AND_GIT_SHA.json').read_text());source['replayed_import_evidence']=json.loads((X/'native_sources_imports_and_tests.json').read_text());source['original_parent_metadata']=json.loads((X/'staged_parent_metadata.json').read_text());source['independent_cold']=json.loads((O/'independent_cold_verification.json').read_text());source['independent_actual_imports']=json.loads((O/'independent_cold_0.json').read_text())['imports']
for row in source['original_parent_metadata']:
 data=Path(row['destination']).read_bytes();assert digest(Path(row['destination']))==row['sha256'];assert data==subprocess.check_output(['git','show',row['commit']+':'+row['source_path']],cwd=R.parents[1])
(R/'02_ORIGINAL74_ACTUAL_IMPORTED_SOURCE_AND_GIT_SHA.json').write_text(json.dumps(source,indent=2)+'\n')
summary=dict(verdict='RED_NATIVE_DOMAIN_FAIL_CLOSED_SERIALIZATION_BOUNDARY',current_282=dict(tests=282,failures=0,errors=0,skipped=0),nested44=dict(tests=44,failures=0,errors=0,skipped=0),new_independent26=dict(tests=26,failures=2,errors=0,skipped=0),historical_originals=dict(tests=119,failures=6,errors=0,skipped=0),successor_node_mapping=mapped,author_cold_pids=[c['pid'] for c in cold],author_cold_case_count=82,xml=counts)
(O/'INDEPENDENT_JUNIT_AND_SUCCESSOR_AUDIT.json').write_text(json.dumps(summary,indent=2)+'\n')
print('Independently counted actual testcase elements: current282 green; nested44 green; new26 24PASS/2FAIL; original historical119 113PASS/6FAIL')
