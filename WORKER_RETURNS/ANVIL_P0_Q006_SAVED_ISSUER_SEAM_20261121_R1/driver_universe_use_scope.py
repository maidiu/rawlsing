#!/usr/bin/env python3
import dataclasses,json,sys
from types import SimpleNamespace
sys.path.insert(0,str(__import__('pathlib').Path.cwd()))
from rawlsing_next.pre553_empirical_objects import AuthorityRef,AuthoritySnapshot,ExactRef,semantic_hash
from rawlsing_next.pre553_anvil_stream_recorded import RecordedUniverseUse,RecordedResponseError
u=ExactRef('EmpiricalUniverse@1.0.0','urn:test:universe','1'*64)
q=ExactRef('EmpiricalQuerySpec@1.0.0','urn:test:q','2'*64)
predref=ExactRef('EmpiricalPredicate@1.0.0','urn:test:p','3'*64)
r=ExactRef('RISK_SET','urn:test:r','4'*64)
op='Q103-OP-RECORDED-RESPONSE-ONLY'; scope='Q103_RAW_UNWEIGHTED_RECORDED_RESPONSE_ONLY'; owner='a'*64; doc='b'*64
hist_ref=AuthorityRef('SOURCE_SEMANTICS_TOPOLOGY','HIST-DEFER','5'*64)
pos_ref=AuthorityRef('SOURCE_SEMANTICS_TOPOLOGY','POS-USE','6'*64)
def snap(ref,state,scope_env,kwargs=None):
 return AuthoritySnapshot(typed_state=state,authority_snapshot_refs=(),dependency_refs=(),producer_replay_locator_or_reference_root=ExactRef('REPLAY_ROOT','x',semantic_hash({'r':ref.key})),authority_id=ref.authority_id,authority_version=ref.authority_version,authority_content_hash=ref.authority_content_hash,authority_kind='SOURCE_SEMANTICS_TOPOLOGY',decision_state=state,governed_operations=(op,),governed_object_families=('EmpiricalUniverse@1.0.0',),scope_envelope=scope_env,effective_time_or_interval='CURRENT',parent_authority_refs=(),negative_limit_refs=(),supersession_refs=(),interpretation_semantics_fingerprint='c'*64,replay_protocol_ref=ExactRef('REPLAY_PROTOCOL','x',semantic_hash({'p':ref.key})))
def build(positive_scope,opv=op,current=lambda:True,posref=pos_ref):
 h=snap(hist_ref,'DEFER',{'semantic_scope':'EXACT_SOURCE_CODEBOOK_AND_H48_EVIDENCE_ONLY','source_universe_refs':[u.as_dict()]})
 possnap=snap(posref,'ALLOW',positive_scope)
 return RecordedUniverseUse(historical_snapshot=h,positive_snapshot=possnap,owner_decision_sha256=owner,operation_document_sha256=doc,source_id='SRC04',source_root='SOURCE_ARTIFACT|test|'+'7'*64,release_root='C11_STREAM_SOURCEFREE_RELEASE|test|'+'8'*64,universe_root=u.key,replay_root='9'*64,question_ref=ExactRef('NATIVE_QUESTION','urn:test:q103','a'*64),query_ref=q,predicate_ref=predref,operation=opv,risk_ref=r,interpretation=(('1','SUBSTANTIVE_RESPONSE'),),scope=scope,current_verifier=current)
def run(label,fn):
 try: fn(); print(json.dumps({'case':label,'accepted':True},sort_keys=True))
 except Exception as e: print(json.dumps({'case':label,'accepted':False,'type':type(e).__name__},sort_keys=True))
base={'source_universe_refs':[u.as_dict()],'scope':scope,'release':'C11_STREAM_SOURCEFREE_RELEASE|test|'+'8'*64,'source_sha256':'SOURCE_ARTIFACT|test|'+'7'*64,'recorded_raw_codes':['1']}
run('exact_positive',lambda: build(base).authorize(SimpleNamespace(ref=u,authority_snapshot_refs=(hist_ref,)),SimpleNamespace(ref=q,risk_set_ref=r),SimpleNamespace(ref=predref)))
run('absent_scope',lambda: build({}).authorize(SimpleNamespace(ref=u,authority_snapshot_refs=(hist_ref,)),SimpleNamespace(ref=q,risk_set_ref=r),SimpleNamespace(ref=predref)))
wrong=dict(base); wrong['source_universe_refs']=[{'kind':u.kind,'object_id':u.object_id,'content_hash':'0'*64}]
run('wrong_hash',lambda: build(wrong).authorize(SimpleNamespace(ref=u,authority_snapshot_refs=(hist_ref,)),SimpleNamespace(ref=q,risk_set_ref=r),SimpleNamespace(ref=predref)))
run('substituted_operation',lambda: build(base,opv='OTHER').authorize(SimpleNamespace(ref=u,authority_snapshot_refs=(hist_ref,)),SimpleNamespace(ref=q,risk_set_ref=r),SimpleNamespace(ref=predref)))
run('missing_current',lambda: build(base,current=lambda:None).authorize(SimpleNamespace(ref=u,authority_snapshot_refs=(hist_ref,)),SimpleNamespace(ref=q,risk_set_ref=r),SimpleNamespace(ref=predref)))
