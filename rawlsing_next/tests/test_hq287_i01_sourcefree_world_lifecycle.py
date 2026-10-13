"""I01 actual owner-chain hostiles. Source-free only; independent review pending."""
from dataclasses import replace
import json
import os
import subprocess
import sys
import pytest
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I
from rawlsing_next.pre553_batch_runner import ExecutorBinding
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleError
from rawlsing_next.pre553_learned_product_release import M2ReleaseError


def test_actual_chain_saved_refs_and_numerical_consumer(tmp_path):
    p,report=I.build_product(tmp_path);served=I.serve(p)
    assert report['batch_state']=='COMPLETED' and report['checkpoint_sequence']==2
    assert len(p.calls)==1
    result=served['numeric_result'];trace=result['progressive_trace']
    assert [r['raw_denominator_support'] for r in trace]==[32,16,8]
    assert [r['raw_numerators']['1'] for r in trace]==[18,10,6]
    assert [r['exact_probabilities']['1']['$exact_fraction'] for r in trace]==[[9,16],[5,8],[3,4]]
    assert result['source_value_dependency']['value_reads_used']==6
    assert all(v['semantic_effect']=='VALUE_USED_IN_EXACT_CONDITIONAL' for v in served['consumer_receipt']['values_read'])
    assert served['producer_subject_ref']==p.release.release_subject_ref.as_dict()
    assert p.release.ref!=p.release.release_subject_ref
    assert served['m2_resolution_receipt']['resolved_release_subject_ref']==served['producer_subject_ref']
    assert all(served['m2_resolution_receipt'][k] is False for k in ('selector_substitution','lifecycle_publication_effect','current_selection_effect','consumer_permission_effect'))
    assert p.lifecycle.native_security_mode==p.repository.native_security_mode==I.MODE
    payload=I.load_artifact(tmp_path,p.subject_ref)
    assert payload['producer_invocations'][2]['inputs']['empirical_query']==payload['query_ref']
    assert payload['producer_invocations'][2]['outputs']['evidence_ref']==payload['bundle']['evidence_graph'][2]['parent_refs'][0]


def test_resume_reuses_durable_result_without_reexecution(tmp_path):
    p,_=I.build_product(tmp_path);first=I.serve(p)
    again,report=I.build_product(tmp_path)
    assert report['executed']==[] and again.calls==[]
    assert I.serve(again)==first


def test_invalidation_clears_current_preserves_exact_historical_receipt(tmp_path):
    p,_=I.build_product(tmp_path);before=I.serve(p);cp=p.lifecycle.export_checkpoint();inv=I.invalidate(p)
    asof=p.lifecycle.resolve_current_as_of(p.selection_key.ref,as_of_checkpoint=cp)
    assert asof.selected_release_ref==p.release.ref
    assert inv['directly_affected_release_refs']==[p.release.ref.as_dict()]
    with pytest.raises(I.I01Error,match='NO_CURRENT'):I.serve(p)
    q,report=I.build_product(tmp_path)
    assert report['executed']==[] # resume may never revive invalidated CURRENT
    with pytest.raises(I.I01Error,match='NO_CURRENT'):I.serve(q)
    history=I.serve(q,historical=True)
    assert history['numeric_result']==before['numeric_result']
    assert history['consumer_receipt']==before['consumer_receipt']
    checkpoint=q.lifecycle.export_checkpoint()
    assert I.B5.from_checkpoint(checkpoint).export_checkpoint()==checkpoint


def test_fresh_process_reads_saved_world_and_durable_receipt(tmp_path):
    p,_=I.build_product(tmp_path);first=I.serve(p)
    script="import json,sys; from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I; p=I.restore_product(sys.argv[1]); report=I.durable.run_to_completion(p.session); assert not report.executed_units and not p.calls; print(json.dumps(I.serve(p),sort_keys=True))"
    proc=subprocess.run([sys.executable,'-c',script,str(tmp_path)],text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    assert proc.returncode==0,proc.stderr
    assert json.loads(proc.stdout)==first


def test_saved_byte_corruption_refused_before_value_use(tmp_path):
    p,_=I.build_product(tmp_path);path=I.artifact_path(tmp_path,p.subject_ref)
    raw=json.loads(path.read_text());raw['numeric_result']['raw_denominator_support']=99;path.write_text(json.dumps(raw))
    with pytest.raises(I.I01Error,match='BYTES_MISMATCH'):I.serve(p)


def test_foreign_m2_and_stale_current_selection_refused(tmp_path):
    p,_=I.build_product(tmp_path)
    wrong=I.local_ref('LearnedProductRelease','foreign')
    with pytest.raises(M2ReleaseError):p.repository.release_exact(wrong)
    with pytest.raises(LearnedProductLifecycleError):p.lifecycle.select_current(p.selection_key.ref,p.release.ref,expected_previous_receipt_ref=None,selection_attestation_ref=p.selected_receipt.ref,event_authority_ref=I.PRODUCER,event_rule_ref=I.EXECUTOR)
    p.repository=I.m2.M2Repository()
    with pytest.raises(M2ReleaseError):I.serve(p)


def test_rehashed_lifecycle_semantic_drift_refused(tmp_path):
    p,_=I.build_product(tmp_path);cp=p.lifecycle.export_checkpoint()
    cp['checkpoint_payload']['publication'][0]=(cp['checkpoint_payload']['publication'][0][0],'UNPUBLISHED')
    cp['checkpoint_hash']=semantic_hash(cp['checkpoint_payload'])
    I.save_json(tmp_path/'lifecycle.json',cp)
    with pytest.raises(LearnedProductLifecycleError):I.restore_product(tmp_path)


def test_real_saved_effect_before_commit_stays_held_without_retry(tmp_path):
    class Interrupt(BaseException):pass
    session,world,query,calls=I.open_world_session(tmp_path)
    saved=session.executors['QUERY'].execute
    def stop(unit):saved(unit);raise Interrupt('after actual numeric artifact, before owner receipt')
    session=replace(session,executors={'QUERY':ExecutorBinding(I.EXECUTOR,stop)})
    with pytest.raises(Interrupt):I.durable.run_to_completion(session)
    assert len(calls)==1 and len(list((tmp_path/'artifacts').glob('*.json')))==1
    restored,_,_,newcalls=I.open_world_session(tmp_path);report=I.durable.run_to_completion(restored)
    assert report.skipped_held_units and report.executed_units==() and newcalls==[]
    with pytest.raises(I.I01Error,match='NOT_COMPLETED'):I.admit_saved_world(restored)


def test_partial_lifecycle_publication_is_typed_hold(tmp_path):
    p,_=I.build_product(tmp_path);(tmp_path/'product_index.json').unlink()
    with pytest.raises(I.I01Error,match='PARTIAL_LIFECYCLE_PUBLICATION_HOLD'):I.build_product(tmp_path)


def test_external_modes_never_become_authenticated(tmp_path):
    p,_=I.build_product(tmp_path)
    for obj,err in ((p.lifecycle,LearnedProductLifecycleError),(p.repository,M2ReleaseError)):
        with pytest.raises(err,match='EXTERNAL_ISSUER_HOLD'):obj.require_external_issuer('PROTECTED_CURRENT')
    payload=I.load_artifact(tmp_path,p.subject_ref)
    assert payload['bundle']['replay']['source_permission']=='SOURCE_FREE_ONLY'
    assert payload['selected_contract']['real_current'] is False
