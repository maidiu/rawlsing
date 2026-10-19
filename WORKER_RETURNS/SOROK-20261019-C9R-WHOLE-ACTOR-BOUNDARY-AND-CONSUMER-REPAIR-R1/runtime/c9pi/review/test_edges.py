"""Only TEST_ONLY technical edge positives; no claim of native actor enactment."""
from support import *
from candidate.events import ingress_event

def test_native_guard_result_is_consumed_as_diagnostic():
 v=bind_conditioning(subject=A,sources=sources(),as_of=20)
 assert 'DENY_ZERO_EFFECT' in v.guard_outcome

def test_permission_conditions_full_create(tmp_path):
 with CandidateStore(tmp_path/'positive.sqlite') as s:
  r=run(s)
  assert r.receipt.committed
  assert r.decision.branch is TargetBranch.CREATE
  assert r.decision.permission_ref=='TEST_ONLY_REVIEW_GRANT'
  assert r.decision.permission_ref in r.receipt.readset_refs

def test_committed_target_conditions_cold_later_read(tmp_path):
 p=tmp_path/'positive.sqlite'
 with CandidateStore(p) as s:
  r=run(s);key=r.decision.proposal_hash;expected=r.decision.record_hash
 with CandidateStore(p) as s:
  from candidate.later_action import read_target_for_later_action
  read=read_target_for_later_action(s,consumer=LaterActionConsumer('TEST_ONLY_COLD_READER','target'),middle_state_id=key,as_of=30,commit_time=15)
  assert read.status is LaterActionStatus.ACTION_ADMISSION_HELD
  assert read.committed_record['record_hash']==expected
  assert read.state_hash==digest(read.committed_record)
  assert key in read.readset_refs

def test_actor_original_presented_source_controls_readset():
 a=actor();r=ingress_actor(a,as_of=20)
 assert r.admitted
 assert r.readset_refs==(a['source_ref'],)
 assert r.record_hash==a['hash']

def test_event_original_presented_source_controls_readset():
 e=event();r=ingress_event(e,as_of=20,last_time=0,prior_event_hashes=frozenset())
 assert r.admitted
 assert r.event_hash==e['hash']
 assert r.readset_refs==(e['owner_ref'],)

def test_test_only_create_does_not_depend_on_guard_diagnostic(tmp_path):
 # Used under a native denial-result fault, without altering registry or issuing authority.
 with CandidateStore(tmp_path/'invariance.sqlite') as s:
  r=run(s)
  assert r.decision.branch is TargetBranch.CREATE
  assert r.receipt.committed
  assert evaluate_release_gate().held
