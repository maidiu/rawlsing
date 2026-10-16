"""Return-local accession receipt, wrapping exact accepted owner material.
No producer/Field Forge science or semantic projection is changed.
"""
import json,hashlib,copy
SCHEMA='ORIGINAL_GT2_SCOPE_METHOD_RECEIPT@1'
def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False)
def digest(value):return hashlib.sha256(canonical(value).encode()).hexdigest()
def build(owner,report,current,unit_receipts):
 expected=json.loads(owner.installation.expected_json);links={x['original_expected_work_key']:x for x in report['links']};held={x['expected_work_key']:x for x in report['nonrunnable']}
 assert len(expected['records'])==8 and len(links)==6 and len(held)==2
 entries=[]
 for rec in expected['records']:
  key=rec['expected_work_key'];entry=dict(expected_work_key=key,exact_original_operation=copy.deepcopy(rec),status=rec['legacy']['state'])
  if key in links:
   link=copy.deepcopy(links[key]);m=link['consumer_material'];assert m['producer_fact_ref']==link['producer_result_ref']
   entry.update(source_free_positive=True,link=link,consumer_readset={k:copy.deepcopy(m[k]) for k in ['producer_query_ref','producer_fact_ref','risk_set_ref','empirical_universe_refs','participant_role_order','roles','producer_authority_refs','producer_provenance_refs','producer_replay_ref','producer_permission_ceiling','relation_permission_ceiling'] if k in m})
  else:entry.update(source_free_positive=False,held_record=copy.deepcopy(held[key]),hold='ORDERED_OWNER_NOT_ISSUED')
  entries.append(entry)
 receipt=dict(schema=SCHEMA,claim='SOURCE_FREE_DEV_SPECIALIZED_GT2_HANDOFF',accepted_method=dict(commit='5c70c7d347998907c1c8a865f833dad581777a0e',independent_acceptance='816aaac865a184e572dde10ff0802969bc51eed5',verdict='ACCEPT_SOURCEFREE_GT2_ORIGINAL_SCOPE_METHOD_ONLY'),expected_root=owner.installation.expected_root,register_root=owner.installation.register_root,fixture_owner=owner.installation.identity,profile=owner.installation.profile,operations=sorted(entries,key=lambda x:x['expected_work_key']),counts=dict(total=8,runnable=6,held=2,distinct_original_consumers=len({x['original_expected_work_key'] for x in report['links']}),legacy_keys=len({x['legacy_expected_work_key'] for x in report['links']})),current_test_only_decisions=copy.deepcopy(current['current_decisions']),accepted_original_receipt_objects=copy.deepcopy(unit_receipts),owner_custody=copy.deepcopy(report['pv3_custody']),semantic_holds=['GENERIC_NATIVE_SEMANTICS_HOLD','ORDERED_OWNER_NOT_ISSUED'],authority_holds=['REAL_ORIGINAL_U_EPRE_SOURCE_RIGHTS_HOLD','REAL_ORIGINAL_SIGNED_MONOTONIC_ISSUER_HOLD','OFFLINE_FACT_RESTORATION_HOLD'],hq_adopted=False,real_source_authority_issued=False,generic_semantics_issued=False,V3=False)
 receipt=json.loads(canonical(receipt));receipt['method_receipt_hash']=digest(receipt);return receipt

def verify(receipt):
 r=copy.deepcopy(receipt);h=r.pop('method_receipt_hash');assert digest(r)==h
 assert r['schema']==SCHEMA
 assert all(r['counts'][k]==v for k,v in dict(total=8,runnable=6,held=2,distinct_original_consumers=6).items())
 assert r['counts']['legacy_keys']==(3 if r['profile']=='BASELINE' else 6)
 assert len(r['operations'])==8 and len({x['expected_work_key'] for x in r['operations']})==8
 assert sum(x['source_free_positive'] for x in r['operations'])==6
 for x in r['operations']:
  assert x['exact_original_operation']['expected_work_key']==x['expected_work_key']
  if x['source_free_positive']:
   m=x['link']['consumer_material'];assert m['roles']['CONDITIONER']['source_native_variable']=='Q86B';assert m['roles']['TARGET']['source_native_variable']=='Q86A'
  else:assert x['hold']=='ORDERED_OWNER_NOT_ISSUED'
 assert not any(r[k] for k in ['hq_adopted','real_source_authority_issued','generic_semantics_issued','V3'])
 return h
