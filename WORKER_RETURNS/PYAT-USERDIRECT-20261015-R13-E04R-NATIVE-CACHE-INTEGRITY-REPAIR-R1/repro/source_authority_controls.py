from common import *
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
s=GenericSelectedWorldService();snapshot=s.select();cases=[]
for key in ('source_universe_ref','release_ref','risk_set_ref'):
 payload=deepcopy(snapshot.material);old=payload['empirical'][key];payload['empirical'][key]={'kind':old['kind'],'object_id':'urn:e04n:coherent-foreign-'+key,'content_hash':semantic_hash(['foreign',key])}
 forged=SelectedSnapshot(payload,semantic_hash(payload))
 try:s.possibilities(forged)
 except ValueError as e:cases.append({'mutation':key,'coherent_exact_ref':payload['empirical'][key],'snapshot_hash_recomputed':True,'refused':str(e)})
 else:raise AssertionError('COHERENT_FOREIGN_SNAPSHOT_ACCEPTED:'+key)
old=s.provider.world['qauth'];fields=dict(old.semantic_fields);fields.update(authority_id='E04N_SELF_CREATED_ISSUER',authority_content_hash=semantic_hash('E04N_FAKE_ISSUER'))
forged=AuthoritySnapshot(typed_state=old.typed_state,authority_snapshot_refs=old.authority_snapshot_refs,dependency_refs=old.dependency_refs,producer_replay_locator_or_reference_root=old.producer_replay_locator_or_reference_root,**fields)
s.provider.world['qauth']=forged
try:s.possibilities(snapshot)
except ValueError as e:cases.append({'mutation':'self_created_query_issuer','new_authority_ref':forged.authority_ref.as_dict(),'refused':str(e)})
else:raise AssertionError('SELF_CREATED_QUERY_ISSUER_ACCEPTED')
dump('coherent_source_authority_controls.json',{'actual_fresh_native_service':True,'controls':cases,'result':'FOUR_TYPED_SOURCE_AUTHORITY_FORGERIES_REFUSED','note':'This does not issue original or operative authority; exact TEST_ONLY fixture bounds only.'});print('FOUR_COHERENT_TYPED_SOURCE_OR_ISSUER_FORGERIES_REFUSED')
