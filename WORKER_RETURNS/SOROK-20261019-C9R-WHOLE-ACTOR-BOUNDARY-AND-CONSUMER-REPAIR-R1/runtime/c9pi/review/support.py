"""Reviewer-built TEST_ONLY transport controls, no issued/native authority."""
from candidate import *
from candidate.pipeline import run_candidate_path
A='TEST_ONLY_REVIEW_A'
ISSUER='TEST_ONLY_REVIEW_TARGET_OWNER'
def reseal(x,**kw):
 return seal({**{k:v for k,v in x.items() if k!='hash'},**kw})
def actor():
 return ActorIdentityRecord(A,'ACTIVE','STANDING_CURRENT',10,'TEST_ONLY_REVIEW_ACTOR_SOURCE','test-only-source-digest').sealed()
def event(**kw):
 fields=dict(event_id='TEST_ONLY_REVIEW_E1',owner_ref='TEST_ONLY_REVIEW_EVENT_OWNER',time=15,content={'fact':'tool_offer','scene':'garage','participants':[A,'TEST_ONLY_P']},actor_role=A)
 fields.update(kw)
 return make_event_witness(**fields)
def sources():
 return [make_conditioning_source(source_ref='TEST_ONLY_REVIEW_GARAGE',source_class='ResolvedStructuralContext',subject=A,body={'tool':'wrench','access':'granted','as_of':15,'scene':'garage'})]
def rule():
 return ResponseRule('TEST_ONLY_REVIEW_A_RULE','1',digest({'test_only':'A_RULE'}),'TEST_ONLY_REVIEW_CAN008','1','TEST_ONLY_RESPONSE_OWNER',True,(A,),('ResolvedStructuralContext',),'TEST_ONLY_SOURCEFREE_TECHNICAL',('two distinct preceding actual enacted acts','independent P offer','material access'))
def target(r):
 return TargetRule('TEST_ONLY_REVIEW_T_RULE','1',r.rule_content_hash,'TEST_ONLY_REVIEW_CAN011','1',ISSUER,True,'V3MS_PRACTICE',('CREATE',),('c9p:coordinated_material_inspection',),'TEST_ONLY_SOURCEFREE_TECHNICAL')
def params(store,**kw):
 r=rule()
 p=make_target_permission(grant_id='TEST_ONLY_REVIEW_GRANT',issuer_ref=ISSUER,actor_id=A,rule_content_hash=r.rule_content_hash,before_target_hash=store.target_state_hash(),response_hash='',issued_at=10)
 args=dict(store=store,actor_raw=actor(),event_raw=event(),conditioning_sources=sources(),response_registry=ResponseRuleRegistry.test_only((r,)),target_registry=TargetRuleRegistry.test_only((target(r),)),authority_id=r.authority_id,rule_version=r.rule_version,rule_content_hash=r.rule_content_hash,as_of=20,permitted_issuer_refs=frozenset({ISSUER}),other_person_offer_ref='TEST_ONLY_P_OFFER',material_opportunity_ref='TEST_ONLY_MATERIAL_ACCESS',enacted_history_refs=('TEST_ONLY_H1','TEST_ONLY_H2'),later_consumer=LaterActionConsumer('TEST_ONLY_REVIEW_READER','committed_target_state'),later_as_of=30,target_permission=p,expected_act='inspect_with_tool')
 args.update(kw);return args
def run(store,**kw):return run_candidate_path(**params(store,**kw))
def decide(store,**kw):
 args=params(store,**kw);e=ingress_event(args['event_raw'],as_of=20,last_time=0,prior_event_hashes=frozenset())
 lookup=lookup_rule(args['response_registry'],authority_id=args['authority_id'],rule_version=args['rule_version'],rule_content_hash=args['rule_content_hash'],subject=A)
 resp=evaluate_response(rule_lookup=lookup,event_ref=e.event_hash,event_time=15,subject=A,conditioning_readset=('TEST_ONLY_REVIEW_GARAGE',),actor_history_refs=args['enacted_history_refs'],other_person_offer_ref=args['other_person_offer_ref'],material_opportunity_ref=args['material_opportunity_ref'],prior_response_count=0)
 d=evaluate_target(registry=args['target_registry'],proposal=resp.target_proposals[0] if resp.target_proposals else None,permission=args['target_permission'],actor_id=A,before_target_hash=store.target_state_hash(),existing_target_ids=store.committed_target_ids(),prior_event_hash=e.event_hash,as_of=20,enacted_history_refs=args['enacted_history_refs'],permitted_issuer_refs=args['permitted_issuer_refs'])
 return args,resp,d
