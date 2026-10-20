from pathlib import Path
import json,hashlib,shutil
R=Path(__file__).resolve().parent
P='WORKER_RETURNS/SOROK-20261019-C9P-NATIVE-ACTOR-TRANSITION-TERMINAL-TRANCHE-R1/candidate/'
cases=[
('C9PI_NATIVE_GUARD_DIAGNOSTIC_ONLY','test_native_guard_result_is_consumed_as_diagnostic','rawlsing_next/v3_psepf_zero_positive_guard.py','outcome=GuardOutcome.DENY_ZERO_EFFECT,','outcome=GuardOutcome.DELEGATE_TO_ACCEPTED_OWNER,','candidate.conditioning.bind_conditioning -> _guard_decision','native denial outcome -> ConditioningView.guard_outcome ONLY; not enforcement'),
('C9PI_CAN011_PERMISSION_TECHNICAL','test_permission_conditions_full_create',P+'target_rules.py','if not _valid(permission):','if True:','candidate.target_rules.evaluate_target via run_candidate_path','TEST_ONLY sealed permission -> CREATE -> committed row'),
('C9PI_COMMITTED_TARGET_COLD_READ','test_committed_target_conditions_cold_later_read',P+'later_action.py','record, state_hash = consumer.read_target(store, middle_state_id, as_of)','record, state_hash = None, ""','candidate.later_action.read_target_for_later_action','cold committed row -> named consumer read -> readset'),
('C9PI_ACTOR_PRESENTED_SOURCE_READSET','test_actor_original_presented_source_controls_readset',P+'identity.py','readset_refs=(source_ref,),','readset_refs=("SEVERED_SOURCE",),','candidate.identity.ingress_actor','presented source_ref -> ingress readset; authentication NOT proved'),
('C9PI_EVENT_PRESENTED_SOURCE_READSET','test_event_original_presented_source_controls_readset',P+'events.py','readset = [owner_ref]','readset = ["SEVERED_OWNER"]','candidate.events.ingress_event','presented owner_ref -> event readset; authentication NOT proved')]
claims=[dict(claim_id=i,actual_consumer=c,claimed_dependency=d,positive_node='review/test_edges.py::'+n,fault=dict(path=p,old=o,new=v)) for i,n,p,o,v,c,d in cases]
p=R/'review/test_edges.py.proof.json';p.write_text(json.dumps(dict(schema='RAWLSING_PROOF_INTEGRITY_R1',claims=claims),indent=2)+'\n')
rows=[dict(path=str(f.relative_to(R)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()) for f in sorted((R/'review').iterdir()) if f.is_file()]
(R/'custody/edge_test_preimages.json').write_text(json.dumps(rows,indent=2)+'\n')
shutil.copytree(R/'review',R/'runs/runtime/review',dirs_exist_ok=True)
