"""Independent receipt arithmetic, complete source/import custody, original RED anti-join."""
from pathlib import Path
from collections import Counter
import json,hashlib,subprocess,xml.etree.ElementTree as ET,shutil,platform,datetime,uuid,sys
R=Path(__file__).resolve().parents[1];C=R/'runtime/court';RT=C/'runtime_root';E=R/'evidence'
def read(p):return json.loads(Path(p).read_text())
def h(v):return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()
def bh(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def write(p,v):(R/p).write_text(json.dumps(v,indent=2)+'\n')
# Preserve complete fresh execution outputs; no author archived outputs substituted.
shutil.copytree(C/'observations',E/'original_runs',dirs_exist_ok=True)
if (C/'historical').exists():shutil.copytree(C/'historical',E/'historical',dirs_exist_ok=True)
manifest=read(R/'native_74_source_manifest.json')['files'];assert len(manifest)==74
for row in manifest:
 b=(RT/row['staged_path']).read_bytes();assert bh(b)==row['git_blob_sha1'] and hashlib.sha256(b).hexdigest()==row['sha256']
packet=read(R/'source_packet_receipts.json');known={row['git_blob_sha1']:row for row in manifest};known.update({row['blob_sha1']:row for row in packet})
# All exact reviewed module/test/installer sources are unchanged, including original oracle.
for name in ['repro','tests','authority']:
 for p in (R/'runtime/pv3'/name).rglob('*'):
  if p.is_file():assert p.read_bytes()==(C/p.relative_to(R/'runtime/pv3')).read_bytes()
assert hashlib.sha256((C/'frozen_pv2i/01_FROZEN_ORIGINAL_EXPECTED_SET.json').read_bytes()).hexdigest()=='321681bb0918e4119e3053aef8f0a6cb0d9db434eadc0a3225f897a686a55f79'
assert (C/'frozen_pv2i/tests/test_independent.py').read_bytes()==(R/'runtime/pv2i/tests/test_independent.py').read_bytes()
base=read(E/'independent/actual_six_native_calls.json');trace=base['trace'];rows=[]
for c in trace['C11']:
 people={h(p):p['semantic_fields']['respondent_key'] for p in c['respondents']}
 universe=next(x['semantic_fields'] for x in c['public'] if x['schema_id']=='EmpiricalUniverse');namespace=universe['respondent_namespace'];features=[x['semantic_fields'] for x in c['public'] if x['schema_id']=='RespondentEvent'];routing=[x['semantic_fields'] for x in c['public'] if x['schema_id']=='RoutingEligibilityFact'];answers={};eligible={}
 for q in ['X','Y']:
  answers[q]={people[x['scoped_respondent_ref']['content_hash']]:x['raw_response_value']['$raw_physical_value']['token']['v'] for x in features if x['native_question_ref']['object_id'].endswith('-'+q)}
  eligible[q]={people[x['scoped_respondent_ref']['content_hash']] for x in routing if x['question_or_target_ref']['object_id'].endswith('-'+q) and x['routing_state']=='ELIGIBLE_APPLICABLE'}
 assert answers=={'X':{'R1':'1','R2':'0','R3':'1'},'Y':{'R1':'1','R2':'0','R3':'1'}}
 joint=eligible['X']&eligible['Y'];assert joint=={'R1','R2'};counts=Counter((answers['X'][k],answers['Y'][k]) for k in joint);assert counts=={('0','0'):1,('1','1'):1}
 rows.append(dict(namespace=namespace,raw_answers=answers,eligibility={q:sorted(v) for q,v in eligible.items()},same_person_joint=sorted(joint),joint_counts=[dict(X=k[0],Y=k[1],n=v) for k,v in sorted(counts.items())],source_artifact_ref=c['source_artifact_ref'],C11_release=c['release_ref']))
facts={f['ref']['content_hash']:f for f in trace['I03']};actual_relations={f['ref']['content_hash']:f for f in trace['Field_Forge']}
links=[]
for l in base['report']['links']:
 f=facts[l['producer_result_ref']['content_hash']];m=l['consumer_material'];assert h(f['projection'])==f['ref']['content_hash'];assert h(f['query'])==f['query_ref']['content_hash']
 assert f['ref']==m['producer_fact_ref']==l['producer_result_ref'];assert f['query_ref']==m['producer_query_ref']
 assert m==actual_relations[l['consumer_ref']['content_hash']]['material']
 fields=f['projection']['semantic_fields'];assert fields['risk_set_ref']==m['risk_set_ref'] and fields['empirical_universe_refs']==m['empirical_universe_refs']
 if l['original_identity']['operation']['slot']=='DISCOVERY':
  candidates=[r['semantic_fields'] for d in trace['I05'] for r in d['receipts'] if l['producer_result_ref'] in r['semantic_fields']['empirical_fact_refs']]
  assert candidates and any(r['winning_predicate_ref']==fields['condition_predicate_ref'] for r in candidates)
 links.append(dict(original_work_key=l['original_expected_work_key'],legacy_key=l['legacy_expected_work_key'],native=l['original_identity'],source_release_refs=l['c11_release_refs'],producer_fact_ref=f['ref'],producer_query_ref=f['query_ref'],risk=m['risk_set_ref'],universe=m['empirical_universe_refs'],raw_denominator=fields['raw_denominator_support'],actual_consumer_ref=l['consumer_ref'],actual_material=m))
# Direct process imports with physical source and exact Git identities.
imports=[]
def verify_import(row,pkey,hkey):
 p=Path(row[pkey].replace('<RETURN>',str(R)));p=p if p.is_absolute() else R/p
 b=p.read_bytes();assert bh(b)==row[hkey];assert row[hkey] in known,(str(p),row[hkey])
 rel=str(p.relative_to(RT)) if p.is_relative_to(RT) else None
 source=next((x for x in manifest if x['staged_path']==rel),known[row[hkey]])
 assert source.get('git_blob_sha1',source.get('blob_sha1'))==row[hkey]
 imports.append(dict(module=row['module'],physical_file=str(p.relative_to(R)),blob_sha1=row[hkey],source_commit=source['commit'],source_path=source.get('source_path',source.get('path'))))
for row in trace['imports']:verify_import(row,'file','blob_sha1')
audits=list((C/'observations/owners_111_child_audits').glob('process_*.json'));assert len(audits)==53
for p in audits:
 for row in read(p)['imports']:verify_import(row,'physical_file','git_blob_sha1')
for name in ['first','replay','offline']:
 for row in read(E/'abrupt'/(name+'.json'))['trace']['imports'] if name!='offline' else read(E/'abrupt'/(name+'.json'))['imports']:verify_import(row,'file','blob_sha1')
inherited=read(R/'inherited_results.json');historic=next(x for x in inherited if x['mode']=='pv2i_historical');target=next(x for x in inherited if x['mode']=='pv2i_adapter')
a={x['name']:x for x in historic['cases']};b={x['name']:x for x in target['cases']};assert set(a)==set(b) and len(a)==48
red=[k for k,v in a.items() if v['status']=='FAIL'];closed=[k for k in red if b[k]['status']=='PASS'];left=[k for k in b if b[k]['status']=='FAIL'];assert len(closed)==21 and left==['test_generic_native_labels_not_specialized_Q86']
for mode,n in [('pv2_33',33),('v2k_24',24),('pv_21',21),('owners_111',111),('pv3',28)]:
 d=next(x for x in inherited if x['mode']==mode);assert d['counts']==dict(tests=n,failures=0,errors=0,skipped=0)
assert historic['counts']==dict(tests=48,failures=22,errors=0,skipped=0)
assert target['counts']==dict(tests=48,failures=1,errors=0,skipped=0)
for folder,n in [('independent',28),('extra',8)]:
 root=ET.parse(E/folder/'junit.xml').getroot();ts=list(root.iter('testsuite'));assert sum(int(t.get('tests')) for t in ts)==n and all(int(t.get(k,0))==0 for t in ts for k in ['failures','errors','skipped'])
write('02_REAL_C11_I03_I05_P01_FIELD_FORGE_CALLS_AND_48_CASES.json',dict(grade='ACCEPT_SOURCEFREE_GT2_ORIGINAL_SCOPE_METHOD_ONLY',full_native_tree_verified=74,owner_suite_process_audits=53,import_observations=len(imports),imports=imports,actual_independent_call_counts=trace['call_counts'],independently_reconstructed_C11_rows=rows,six_complete_producer_consumer_values=links,exact_original_48_cases=[dict(name=k,PV2=a[k]['status'],PV3=b[k]['status'],disposition='CLOSED' if k in closed else 'GENERIC_NATIVE_SEMANTICS_HOLD_RAW_FAIL' if k in left else 'RETAINED_PASS') for k in a],original_21_RED_closed=closed,remaining_raw_failure=left,suite_counts=dict(historical=historic['counts'],target=target['counts'],unchanged_baseline=189,PV3_additional=28,independent_review=28,supplemental=8),source_and_test_bytes_unchanged=True,accepted_Field_Forge_semantics_changed=False))
write('05_IMPORT_AND_SOURCE_CUSTODY.json',dict(native_manifest='native_74_source_manifest.json',actual_imports=imports,original_48_test_blob=bh((C/'frozen_pv2i/tests/test_independent.py').read_bytes()),original_independent_oracle_sha256=hashlib.sha256((C/'frozen_pv2i/01_FROZEN_ORIGINAL_EXPECTED_SET.json').read_bytes()).hexdigest(),native_74_byte_unchanged=True,reviewed_PV3_code_byte_unchanged=True,original_PV3I_and_PV2I_packet_refs='source_packet_receipts.json',compatibility_alias=[x for x in manifest if 'compatibility_alias' in x]))
print('INDEPENDENT ADJUDICATION PASS: native74, actual53 processes, all6 current products, original21 RED closure; generic remains RAW FAIL/HOLD')
