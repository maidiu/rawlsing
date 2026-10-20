from support import *
from candidate.target_rules import evaluate_target

def test_committed_semantic_record_survives_cold_reopen(tmp_path):
 p=tmp_path/'semantic.sqlite'
 with CandidateStore(p) as s:
  r=run(s);key=r.decision.proposal_hash
 with CandidateStore(p) as s:
  record=s.read_target_state(key)
  assert record.get('semantic_object_ref')=='c9p:coordinated_material_inspection'
  assert record.get('effective_from')==15
  assert event()['hash'] in record['causal_parent_refs']

def test_explicit_validated_target_identity_is_committed_identity(tmp_path):
 with CandidateStore(tmp_path/'identity.sqlite') as s:
  args,resp,_=decide(s);proposal=reseal(resp.target_proposals[0],target_middle_state_id='TEST_ONLY_EXPLICIT_TARGET')
  d=evaluate_target(registry=args['target_registry'],proposal=proposal,permission=args['target_permission'],actor_id=A,before_target_hash=s.target_state_hash(),existing_target_ids=frozenset(),prior_event_hash=event()['hash'],as_of=20,enacted_history_refs=('TEST_ONLY_H1','TEST_ONLY_H2'),permitted_issuer_refs=frozenset({ISSUER}))
  assert d.branch is TargetBranch.CREATE
  s.admit_occurrence(args['event_raw'])
  receipt=s.commit(event=args['event_raw'],response=seal({'event_ref':args['event_raw']['hash']}),decision=d,readset_refs=d.readset_refs)
  assert receipt.committed
  assert s.read_target_state('TEST_ONLY_EXPLICIT_TARGET') is not None

def test_fabricated_decision_cannot_bypass_target_owner(tmp_path):
 with CandidateStore(tmp_path/'forged.sqlite') as s:
  e=event();s.admit_occurrence(e)
  forged=TargetDecision(TargetBranch.CREATE,TargetReason.OK,A,'V3MS_PRACTICE','INVENTED_PROPOSAL','INVENTED_RECORD',s.target_state_hash(),'INVENTED_POST',(),'NO_SUCH_GRANT')
  receipt=s.commit(event=e,response=seal({'event_ref':e['hash']}),decision=forged,readset_refs=())
  assert not receipt.committed or not s.committed_target_ids()
