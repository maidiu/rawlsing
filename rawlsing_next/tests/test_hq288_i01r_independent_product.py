"""Independent SOURCE_FREE_ONLY product court; frozen consumer expectations."""
from dataclasses import replace
import copy, hashlib, json, os, subprocess, sys
from pathlib import Path
import pytest
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I
from rawlsing_next.pre553_batch_durable_checkpoint_candidate import CheckpointTornError

ARTIFACT='a5d1146a5bc0182a0232b1f59dda9ea78a35b4c42096c2fc938fc0cd8ebd7606'
RELEASE='582317a6731c43d84959f7d0e74604f30bba4d49f3fe114f1afb07f63108d22a'
AUTHOR=Path(__file__).resolve().parents[2]/'WORKER_RETURNS/PYAT-R3-HQ287-I01-SOURCEFREE-INTEGRATED-WORLD-LIFECYCLE-R1/repro/product'

def test_frozen_retained_bytes_and_fresh_execution(tmp_path):
    raw=(AUTHOR/'artifacts'/f'{ARTIFACT}.json').read_bytes()
    assert hashlib.sha256(raw).hexdigest()==ARTIFACT
    p,report=I.build_product(tmp_path)
    assert p.subject_ref.content_hash==ARTIFACT and p.release.ref.content_hash==RELEASE
    assert I.artifact_path(tmp_path,p.subject_ref).read_bytes()==raw
    assert report['batch_state']=='COMPLETED'
    payload=I.load_artifact(tmp_path,p.subject_ref)
    assert payload['query_ref']==p.session.manifest.units[0].job_ref.as_dict()
    assert [r for r in payload['producer_invocations'] if 'inputs' in r][-1]['inputs']['empirical_query']==payload['query_ref']
    result=I.serve(p)
    trace=result['numeric_result']['progressive_trace']
    assert [(r['raw_denominator_support'],r['raw_numerators']['1'],r['exact_probabilities']['1']['$exact_fraction']) for r in trace]==[(32,18,[9,16]),(16,10,[5,8]),(8,6,[3,4])]
    reads=result['consumer_receipt']['values_read']
    assert len(reads)==6 and len({r['channel_id'] for r in reads})==6
    assert all(r['semantic_effect']=='VALUE_USED_IN_EXACT_CONDITIONAL' for r in reads)
    assert result['m2_resolution_receipt']['resolved_release_subject_ref']==p.subject_ref.as_dict()
    assert p.subject_ref!=p.release.ref

def test_serving_saved_bundle_with_all_producers_disabled(tmp_path,monkeypatch):
    p,_=I.build_product(tmp_path);expected=I.serve(p);payload=I.load_artifact(tmp_path,p.subject_ref)
    def forbidden(*a,**kw):raise AssertionError('producer reconstructed during serving')
    for obj,names in [(I.selected,['select_world','run_selected_world_progressive_chain']),(I.progressive,['build_synthetic_world','run_progressive_chain']),(I.seam,['build_sociological_bundle','build_synthetic_world','run_progressive_chain','select_world'])]:
        for name in names:monkeypatch.setattr(obj,name,forbidden)
    native=I.seam.ContractOnlySeamConsumer;observed=[]
    def spy(bundle):
        observed.append(bundle.as_dict());return native(bundle)
    monkeypatch.setattr(I.seam,'ContractOnlySeamConsumer',spy)
    assert I.serve(p)==expected and observed==[payload['bundle']]
    assert len(p.calls)==1

@pytest.mark.parametrize('field,value',[('schema','FOREIGN'),('security_mode','AUTHENTICATED'),('producer_contract_ref',{}),('query_ref',{}),('source_release_ref',{})])
def test_rehashed_artifact_does_not_bypass_durable_binding(tmp_path,field,value):
    p,_=I.build_product(tmp_path);payload=I.load_artifact(tmp_path,p.subject_ref)
    payload[field]=value
    # A new local hash is not the committed durable result identity.
    ref=I.local_ref('I01SourceFreeSavedWorld',payload)
    I.save_json(tmp_path/'artifacts'/f'{ref.content_hash}.json',payload)
    p.subject_ref=ref
    with pytest.raises(I.I01Error):I.serve(p)

@pytest.mark.parametrize('attack', ['scope','origin','permission','gt2','protected','risk','duplicate','no_channels','fraction','denominator','step_numerator','condition'])
def test_native_consumer_rejects_rehashed_hostile_saved_bundle(attack):
    payload=json.loads((AUTHOR/'artifacts'/f'{ARTIFACT}.json').read_text())
    b=I.bundle_from_payload(payload)
    if attack=='scope': b=replace(b,world_scope={**b.world_scope,'qualified_real_source_value_read':True})
    if attack=='origin': b=replace(b,replay={**b.replay,'test_origin':False})
    if attack=='permission': b=replace(b,replay={**b.replay,'source_permission':'ORIGINAL_SURVEY'})
    if attack=='gt2': b=replace(b,replay={**b.replay,'qualified_gt2_numeric_cells':True})
    if attack=='protected': b=replace(b,selected_world_contract=replace(b.selected_world_contract,real_current=True))
    if attack=='risk': b=replace(b,conditions=({**b.conditions[0],'risk_set_ref':{}},*b.conditions[1:]))
    if attack=='duplicate': b=replace(b,channels=(*b.channels,b.channels[0]))
    if attack=='no_channels': b=replace(b,channels=())
    if attack=='fraction': b=replace(b,channels=(replace(b.channels[0],value={**b.channels[0].value,'raw_probability_exact_fraction':{'$exact_fraction':[0,1]}}),*b.channels[1:]))
    if attack=='denominator': b=replace(b,conditions=({**b.conditions[0],'denominator':999},*b.conditions[1:]))
    if attack=='step_numerator':
        steps=copy.deepcopy(list(b.steps));steps[0]['cells']['0']['numerator']+=1;b=replace(b,steps=tuple(steps))
    if attack=='condition':b=replace(b,conditions=b.conditions[1:])
    b=replace(b,content_hash=I.seam._content_hash(replace(b,content_hash='').as_dict()))
    consumer=I.seam.ContractOnlySeamConsumer(b)
    result=consumer.compute_scenario(I.SCENARIO,list(I.seam.P04_STEPS))
    assert result['status']!='COMPUTED'
    assert consumer.get_receipt().values_read==[]

def test_missing_artifact_cannot_reconstruct_fixture(tmp_path):
    p,_=I.build_product(tmp_path);I.artifact_path(tmp_path,p.subject_ref).unlink()
    with pytest.raises(I.I01Error,match='UNAVAILABLE'):I.serve(p)

def test_unscheduled_and_incomplete_work_cannot_admit(tmp_path):
    session,_,_,calls=I.open_world_session(tmp_path)
    with pytest.raises(CheckpointTornError,match="no durable checkpoint"):I.admit_saved_world(session)
    assert calls==[]
    unit=session.manifest.units[0]
    with pytest.raises(I.I01Error,match='QUERY_BINDING'):
        session.executors['QUERY'].execute(replace(unit,job_ref=I.local_ref('EmpiricalQuerySpec','unscheduled')))
    assert calls==[]

def test_release_index_substitution_refused(tmp_path):
    p,_=I.build_product(tmp_path);index=json.loads((tmp_path/'product_index.json').read_text())
    index['release_ref']=p.subject_ref.as_dict();I.save_json(tmp_path/'product_index.json',index)
    with pytest.raises(I.I01Error,match='M2_IDENTITY'):I.restore_product(tmp_path)

def test_cold_invalidated_resume_preserves_asof_without_execution(tmp_path):
    p,_=I.build_product(tmp_path);before=I.serve(p);I.invalidate(p)
    script='''import json,sys
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I
from rawlsing_next.pre553_batch_durable_checkpoint_candidate import CheckpointTornError
p,report=I.build_product(sys.argv[1])
assert p.calls==[] and report['executed']==[]
try:I.serve(p)
except I.I01Error as e:assert 'NO_CURRENT' in str(e)
else:raise AssertionError('resurrection')
print(json.dumps(I.serve(p,historical=True)))
'''
    proc=subprocess.run([sys.executable,'-c',script,str(tmp_path)],capture_output=True,text=True)
    assert proc.returncode==0,proc.stderr
    after=json.loads(proc.stdout)
    assert after['numeric_result']==before['numeric_result'] and after['consumer_receipt']==before['consumer_receipt']

def test_copied_module_or_dynamic_hash_is_not_frozen_owner():
    root=Path(__file__).resolve().parents[2]
    rel='rawlsing_next/pre553_i01_sourcefree_world_lifecycle_candidate.py'
    blob=subprocess.check_output(['git','show','5eb51c6868f4919c31758e0fa96c52f755564fa4:'+rel])
    assert (root/rel).read_bytes()==blob
    impostor=blob+b'\n# substituted owner\n'
    assert hashlib.sha256(impostor).digest()!=hashlib.sha256(blob).digest()
    # Freeze to the sealed Git blob, never a worker-calculated new expectation.
    assert subprocess.check_output(['git','hash-object',str(root/rel)]).strip()==subprocess.check_output(['git','rev-parse','5eb51c6868f4919c31758e0fa96c52f755564fa4:'+rel]).strip()


def test_independent_external_issuer_and_retained_gt2_refusals(tmp_path):
    from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleError
    from rawlsing_next.pre553_learned_product_release import M2ReleaseError
    p,_=I.build_product(tmp_path)
    for obj,error in ((p.lifecycle,LearnedProductLifecycleError),(p.repository,M2ReleaseError)):
        assert obj.native_security_mode=='LOCAL_UNAUTHENTICATED'
        with pytest.raises(error,match='EXTERNAL_ISSUER_HOLD'):obj.require_external_issuer('PROTECTED_CURRENT')
    with pytest.raises(I.seam.SeamContractError,match='SOURCE_VALUE_UNAVAILABLE'):
        I.seam.build_retained_gt2_bundle(issued_source_owned_values={'cells':[1,2]},issued_use_authority='caller-claimed')

def test_reconstructed_m2_dereferences_only_exact_saved_subject(tmp_path):
    from rawlsing_next.pre553_learned_product_release import M2ReleaseError
    p,_=I.build_product(tmp_path)
    p.repository=I.m2.M2Repository()
    with pytest.raises(M2ReleaseError):I.serve(p)
    restored=I.restore_product(tmp_path)
    result=I.serve(restored)
    assert result['producer_subject_ref']==restored.subject_ref.as_dict()
    assert result['selected_release_ref']==restored.release.ref.as_dict()
    assert restored.calls==[]
