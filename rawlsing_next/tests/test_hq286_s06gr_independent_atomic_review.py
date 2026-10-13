"""Independent S06GR positive court. Local synthetic objects, no custody grant."""
import json
import os
import subprocess
import sys
from copy import deepcopy
from dataclasses import replace, FrozenInstanceError
from threading import Barrier, Event, Thread

import pytest
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor as B5, LearnedProductLifecycleError
from rawlsing_next.pre553_learned_product_release import M2Repository, M2ReleaseError, RepresentationRecord, PublicationBinding, M2_PUBLICATION_CONTRACT_REF, publish_binding, resolve_release_exact
from rawlsing_next.tests.test_pre553_s06f_native_owner_security import ref, subject, register, m2_fixture

A = dict(event_authority_ref=ref('Authority', 'gr'), event_rule_ref=ref('Rule', 'gr'))

def key(x, s, label='gr'):
    return x.selection_key(product_family_ref=s.product_family_ref, selection_scope_ref=s.selection_scope_ref, selection_purpose_ref=ref('Purpose', label))

def select(x, k, s, previous=None):
    return x.select_current(k.ref, s.release_ref, expected_previous_receipt_ref=previous, selection_attestation_ref=ref('Attestation', 'gr'), **A)

def roundtrip(x):
    cp = x.export_checkpoint()
    assert B5.from_checkpoint(cp).export_checkpoint() == cp
    return cp

def fixture():
    x = B5()
    a = register(x, replace(subject('gr-a'), materialization_class='RECOMPUTABLE_PRODUCT_PAYLOAD'), publish=True)
    b = register(x, subject('gr-b'), publish=True)
    c = register(x, replace(subject('gr-cache'), materialization_class='OPTIONAL_CACHE_ACCELERATOR'))
    u = register(x, subject('gr-unpublished'))
    staged = subject('gr-staged'); x.stage_release(staged)
    k = key(x, a); chosen = select(x, k, a)
    x.record_rebuild_eligibility(a.release_ref, execution_mechanism_ref=ref('Mechanism', 'gr'), source_or_upstream_refs=(ref('Input','gr'),), **A)
    proofs = {name:ref('Proof', name) for name in ('reconstruction_proof_ref','historical_retention_proof_ref','serving_reconstruction_proof_ref','downstream_byte_dependency_absence_proof_ref','source_carrier_retention_proof_ref')}
    gc = x.attest_gc_eligibility(a.release_ref, **proofs, **A)
    operations = {
        'stage_release': lambda:x.stage_release(subject('gr-new')),
        'stage_protocol': lambda:x.stage_protocol(subject('gr-new')),
        'selection_key': lambda:key(x, a, 'new'),
        'register_product': lambda:x.register_product(staged.release_ref, **A),
        'publish_product': lambda:x.publish_product(u.release_ref, **A),
        'record_recertification': lambda:x.record_recertification(a.release_ref, attestation_ref=ref('Attestation','recert'), **A),
        'select_current': lambda:select(x,k,b,chosen.ref),
        'declare_no_current': lambda:x.declare_no_current(k.ref, expected_previous_receipt_ref=chosen.ref, selection_attestation_ref=ref('Attestation','clear'), reason_ref=ref('Reason','clear'), **A),
        'supersede_current': lambda:x.supersede_current(k.ref, predecessor_release_ref=a.release_ref, successor_release_ref=b.release_ref, expected_previous_receipt_ref=chosen.ref, selection_attestation_ref=ref('Attestation','super'), supersession_basis_ref=ref('Basis','super'), **A),
        'withdraw_product': lambda:x.withdraw_product(a.release_ref, withdrawal_reason_ref=ref('Reason','withdraw'), withdrawal_scope_ref=ref('Scope','withdraw'), selection_attestation_ref=ref('Attestation','withdraw'), current_transitions={k.ref.key:None}, **A),
        'declare_invalidation': lambda:x.declare_invalidation(a.determinant_refs, dependency_closure_receipt_ref=ref('Closure','inv'), selection_attestation_ref=ref('Attestation','inv'), current_transitions={k.ref.key:None}, **A),
        'record_rebuild_eligibility': lambda:x.record_rebuild_eligibility(b.release_ref, execution_mechanism_ref=None, **A),
        'link_rebuild': lambda:x.link_rebuild(a.release_ref,new_release_ref=b.release_ref,rebuild_state='REBUILT',rebuild_determinant_set_hash=b.determinant_set_hash,replay_or_execution_receipt_ref=ref('Receipt','rebuild'), **A),
        'record_cache_materialized': lambda:x.record_cache_materialized(c.release_ref,cache_ref=ref('Cache','gr'), **A),
        'record_cache_dropped': lambda:x.record_cache_dropped(c.release_ref,cache_ref=ref('Cache','gr'), **A),
        'attest_gc_eligibility': lambda:x.attest_gc_eligibility(a.release_ref, **proofs, **A),
        'record_payload_gc': lambda:x.record_payload_gc(gc.ref, **A),
    }
    return x,a,b,k,operations

WRITERS = ('stage_release','stage_protocol','selection_key','register_product','publish_product','record_recertification','select_current','declare_no_current','supersede_current','withdraw_product','declare_invalidation','record_rebuild_eligibility','link_rebuild','record_cache_materialized','record_cache_dropped','attest_gc_eligibility','record_payload_gc')

class Fault(BaseException): pass

@pytest.mark.parametrize('name', WRITERS)
def test_baseexception_rollback_then_success_and_recovery(name, monkeypatch):
    x,a,b,k,ops = fixture(); cp = roundtrip(x)
    if name in ('stage_release','stage_protocol','selection_key'):
        store = '_selection_keys' if name == 'selection_key' else '_repository_subjects'
        class FaultDict(dict):
            def __setitem__(self,k,v):
                super().__setitem__(k,v); raise Fault('post-write')
        original = getattr(x,store)
        monkeypatch.setattr(x,store,FaultDict(original))
    else:
        original = x._append_events
        def fail(events):
            original(events); raise Fault('post-append')
        monkeypatch.setattr(x,'_append_events',fail)
    with pytest.raises(Fault): ops[name]()
    assert roundtrip(x) == cp
    monkeypatch.undo()
    ops[name]()
    assert roundtrip(x) != cp


def test_recursive_snapshot_detachment():
    x,a,_,_,_ = fixture(); before = roundtrip(x)
    for e in x.events:
        with pytest.raises(TypeError): e.payload['injected'] = 1
    published = next(e for e in x.release_history(a.release_ref) if e.event_kind == 'PRODUCT_PUBLISHED')
    old = published.ref
    with pytest.raises(TypeError): published.payload['authority_snapshot_refs'][0]['authority_id']='bad'
    with pytest.raises(TypeError): published.payload['replay_root_ref']['object_id']='bad'
    with pytest.raises(FrozenInstanceError): x.lifecycle_state(a.release_ref).publication='UNPUBLISHED'
    public = published.as_dict(); public['payload']['replay_root_ref']['object_id']='bad'
    cp = x.export_checkpoint(); restored = B5.from_checkpoint(cp)
    cp['checkpoint_payload']['events'].clear()
    assert roundtrip(restored) == before == roundtrip(x)
    assert published.ref == old
    raw = {'nested':[{'v':1}]}; e = replace(published,payload=raw); raw['nested'][0]['v']=2
    assert e.payload['nested'][0]['v']==1

@pytest.mark.parametrize('event_kind,field', [('PRODUCT_REGISTERED','determinant_set_hash'),('PRODUCT_PUBLISHED','replay_root_ref'),('PRODUCT_PUBLISHED','producer_permission_ceiling'),('CURRENT_SELECTED','determinant_snapshot_ref')])
def test_rehashed_event_semantic_drift_refused(event_kind,field):
    x=B5(); a=register(x,subject('gr-drift'),publish=event_kind!='PRODUCT_REGISTERED')
    chosen=None
    if event_kind=='CURRENT_SELECTED': chosen=select(x,key(x,a),a)
    cp=roundtrip(x); e=x.events[-1]; assert e.event_kind==event_kind
    payload=e.as_dict()['payload']
    payload[field] = semantic_hash('alien') if field=='determinant_set_hash' else ref('Alien','gr').as_dict()
    forged=replace(e,payload=payload)
    cp['checkpoint_payload']['events'][-1]=forged.as_dict()
    if chosen:
        receipt=replace(chosen,current_select_event_ref=forged.ref,determinant_snapshot_ref=ref('Alien','gr'))
        cp['checkpoint_payload']['selection_receipts'][0]=receipt.as_dict()
        for row in cp['checkpoint_payload']['selection_index']:row['receipt_ref']=receipt.ref.as_dict()
    cp['checkpoint_hash']=semantic_hash(cp['checkpoint_payload'])
    with pytest.raises(LearnedProductLifecycleError,match='semantics|semantic replay|native operations'): B5.from_checkpoint(cp)

@pytest.mark.parametrize('kind', ['selection_receipts','no_current_receipts','invalidations','rebuild_eligibility','rebuild_links','gc_eligibility'])
def test_missing_receipt_family_is_not_replayable(kind):
    x,a,b,k,ops=fixture()
    ops['link_rebuild'](); ops['declare_no_current'](); x.declare_invalidation(a.determinant_refs,dependency_closure_receipt_ref=ref('Closure','inv'),selection_attestation_ref=ref('Attestation','inv'),**A)
    cp=roundtrip(x); assert cp['checkpoint_payload'][kind]
    cp['checkpoint_payload'][kind].clear(); cp['checkpoint_hash']=semantic_hash(cp['checkpoint_payload'])
    with pytest.raises(LearnedProductLifecycleError): B5.from_checkpoint(cp)


def parallel(calls):
    start=Barrier(len(calls)); results=[]; errors=[]
    def run(call):
        try: start.wait(timeout=5); results.append(call())
        except BaseException as e: errors.append(e)
    threads=[Thread(target=run,args=(call,)) for call in calls]
    for t in threads:t.start()
    for t in threads:t.join(10)
    assert not any(t.is_alive() for t in threads)
    return results,errors

@pytest.mark.parametrize('distinct', [False,True])
def test_four_concurrent_public_selectors(distinct):
    for _ in range(8):
        x=B5(); a=register(x,subject('gr-race-a'),publish=True); b=register(x,subject('gr-race-b'),publish=True)
        k=key(x,a); other=key(x,a,'other') if distinct else k
        results,errors=parallel([lambda:select(x,k,a),lambda:select(x,k,b),lambda:select(x,other,a),lambda:select(x,other,b)])
        assert len(results)==(2 if distinct else 1)
        assert len(errors)==(2 if distinct else 3)
        assert all(isinstance(e,LearnedProductLifecycleError) for e in errors)
        roundtrip(x)


def representation(release, source, producer, label='gr'):
    return RepresentationRecord(release_ref=release.ref,resolved_subject_ref=source,producer_contract_ref=producer,resolution_mode='CONTENT_ADDRESSED_MATERIALIZATION',resolver_or_locator_ref=ref('Locator',label),representation_integrity_ref=ref('Integrity',label))

@pytest.mark.parametrize('route',['subject','representation'])
def test_public_m2_colliding_preimages(route):
    for _ in range(8):
        repo,r,s,p,_=m2_fixture()
        if route=='subject':
            one=replace(repo.subject_exact(s),ref=ref('Subject','gr-collision')); two=replace(one,typed_state='UNKNOWN'); call=repo.register_subject
        else:
            one=representation(r,s,p); two=replace(one,representation_integrity_ref=ref('Integrity','gr-other')); call=repo.register_representation
        results,errors=parallel([lambda:call(one),lambda:call(two)])
        assert len(results)==len(errors)==1 and isinstance(errors[0],M2ReleaseError)
        actual=repo.subject_exact(one.ref) if route=='subject' else repo.representation_exact(one.resolver_or_locator_ref)
        assert actual==results[0]
        assert call(actual)==actual

@pytest.mark.parametrize('name',['register_subject','register_closure','register_release','register_representation','register_binding'])
def test_m2_baseexception_rollback_and_retry(name,monkeypatch):
    repo,r,s,p,closures=m2_fixture(); record=representation(r,s,p); repo.register_representation(record)
    bind=PublicationBinding(release_ref=r.ref,publication_contract_ref=M2_PUBLICATION_CONTRACT_REF,resolution_mode=record.resolution_mode,resolver_or_locator_ref=record.resolver_or_locator_ref,representation_integrity_ref=record.representation_integrity_ref)
    if name=='register_release':
        target=M2Repository(); target.register_subject(repo.subject_exact(s))
        for c in closures.values():target.register_closure(c)
        repo=target
    values={'register_subject':replace(repo.subject_exact(s),ref=ref('Subject','gr-new')),'register_closure':replace(closures['DEPENDENCY'],member_refs=(ref('Member','gr-new'),)),'register_release':r,'register_representation':replace(record,resolver_or_locator_ref=ref('Locator','gr-new')),'register_binding':bind}
    before={n:dict(getattr(repo,n)) for n in ('_subjects','_closures','_releases','_representations','_bindings')}; saved=repo._insert
    def fail(*args):saved(*args); raise Fault('post-insert')
    monkeypatch.setattr(repo,'_insert',fail)
    with pytest.raises(Fault):getattr(repo,name)(values[name])
    assert {n:dict(getattr(repo,n)) for n in ('_subjects','_closures','_releases','_representations','_bindings')}==before
    monkeypatch.undo(); assert getattr(repo,name)(values[name])==values[name]


def test_saved_helpers_and_unwrapped_bodies_refuse():
    x,a,b,k,_=fixture(); cp=roundtrip(x)
    for call in (lambda:x._append_events((x.events[-1],)),lambda:x._commit_selection_transition_receipts(()),lambda:B5.stage_release.__wrapped__(x,subject('outside'))):
        with pytest.raises(LearnedProductLifecycleError):call()
    assert roundtrip(x)==cp
    repo,r,s,p,_=m2_fixture()
    with pytest.raises(M2ReleaseError):repo._insert(repo._subjects,s,repo.subject_exact(s),'COLLISION')
    with pytest.raises(M2ReleaseError):M2Repository.register_subject.__wrapped__(repo,repo.subject_exact(s))
    for obj,err in ((x,LearnedProductLifecycleError),(repo,M2ReleaseError)):
        with pytest.raises(err,match='EXTERNAL_ISSUER_HOLD'):obj.require_external_issuer('EXTERNAL_CUSTODY')
        assert obj.native_security_mode=='LOCAL_UNAUTHENTICATED'


def test_m2_early_refusal_lawful_foreign_mismatch_and_same_release_failover():
    from rawlsing_next.tests.test_pre553_learned_product_release import build_fixture,bind_representation
    repo,r,s,p,_,_=build_fixture(subject_label='gr-main')
    foreign,other,osub,op,_,_=build_fixture(subject_label='gr-foreign')
    fb,loc,_=bind_representation(foreign,other,osub,op,label='gr-foreign',mode='CONTENT_ADDRESSED_MATERIALIZATION')
    for call in (lambda:repo.register_binding(fb),lambda:repo.register_representation(foreign.representation_exact(loc))):
        with pytest.raises(M2ReleaseError) as exc:call()
        assert exc.value.code=='RELEASE_UNAVAILABLE'
    repo.register_subject(foreign.subject_exact(other.release_subject_ref))
    for field in ('authority_closure_ref','dependency_closure_ref','determinant_closure_ref','replay_reconstruction_ref','explanation_lineage_ref'):repo.register_closure(foreign.closure_exact(getattr(other,field)))
    repo.register_release(other); repo.register_representation(foreign.representation_exact(loc)); repo.register_binding(fb)
    with pytest.raises(M2ReleaseError) as exc:publish_binding(repo,release_ref=r.ref,resolution_mode=fb.resolution_mode,resolver_or_locator_ref=fb.resolver_or_locator_ref,representation_integrity_ref=fb.representation_integrity_ref)
    assert exc.value.code=='PUBLICATION_BINDING_MISMATCH'
    first,_,_=bind_representation(repo,r,s,p,label='gr-first',mode='CONTENT_ADDRESSED_MATERIALIZATION')
    second,_,_=bind_representation(repo,r,s,p,label='gr-second',mode='CONTENT_ADDRESSED_MATERIALIZATION')
    with pytest.raises(M2ReleaseError) as exc:resolve_release_exact(repo,r.ref,publication_binding_refs=(first.ref,fb.ref),unavailable_binding_refs=(first.ref,))
    assert exc.value.code=='PUBLICATION_BINDING_MISMATCH'
    result=resolve_release_exact(repo,r.ref,publication_binding_refs=(first.ref,second.ref),unavailable_binding_refs=(first.ref,))
    assert result.receipt.used_publication_binding_ref==second.ref


def test_full_world_consumer_n04_and_fresh_process(monkeypatch):
    from rawlsing_next.tests.test_pre553_learned_world_composition import _contract,_m1_authority,_binding,_registry,execute_m01,m01_fixture
    from rawlsing_next.pre553_learned_world_composition import compose_learned_world
    auth=_m1_authority('gr-world'); binding=_binding(auth); native=execute_m01(m01_fixture())
    x=B5(); repo=M2Repository()
    result=compose_learned_world(_contract(route='M01_M1_M2_B5',binding=binding,actions=('REGISTER','PUBLISH','SELECT_CURRENT'),tag='gr-world'),m2_repository=repo,lifecycle_executor=x,m01_result=native,selected_discovery_receipt_refs=tuple(r.ref for r in native.i05_result.receipts),requested_scope={'fixture':'GR_SYNTHETIC'},m1_family_rule_binding=binding,validator_registry=_registry(binding),m1_authority_snapshots=(auth,))
    assert result.receipt.terminal_state=='RULE_SATISFIED'
    release=result.m2_artifacts.release; calls=[]; saved=repo.subject_exact
    def spy(r):calls.append(r); assert r==release.release_subject_ref; return saved(r)
    monkeypatch.setattr(repo,'subject_exact',spy)
    assert x.verify_m2_release_subject_exact(repo,release.ref)==result.b5_subject
    assert calls and release.ref!=release.release_subject_ref
    cp=roundtrip(x)
    script="import json,sys; from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor as B; x=B.from_checkpoint(json.load(sys.stdin)); print(json.dumps(x.export_checkpoint()))"
    proc=subprocess.run([sys.executable,'-c',script],input=json.dumps(cp),text=True,capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    assert proc.returncode==0,proc.stderr
    assert json.loads(proc.stdout)==json.loads(json.dumps(cp))
    assert result.b5_selection_receipt.selected_release_ref==release.ref

@pytest.mark.parametrize('kind,field', [('selection_receipts','selection_authority_refs'),('no_current_receipts','selection_attestation_refs'),('invalidations','unaffected_product_refs'),('rebuild_eligibility','release_ref'),('rebuild_links','old_release_ref'),('gc_eligibility','release_ref')])
def test_rehashed_receipt_field_mismatch_refused(kind,field):
    from rawlsing_next import pre553_learned_product_lifecycle as mod
    classes=dict(selection_receipts=mod.CurrentSelectionReceipt,no_current_receipts=mod.NoCurrentReceipt,invalidations=mod.InvalidationReceipt,rebuild_eligibility=mod.RebuildEligibilityReceipt,rebuild_links=mod.RebuildLinkReceipt,gc_eligibility=mod.GCElegibilityReceipt)
    x,a,b,k,ops=fixture(); ops['link_rebuild']()
    if kind!='selection_receipts':
        ops['declare_no_current']()
        x.declare_invalidation(a.determinant_refs,dependency_closure_receipt_ref=ref('Closure','inv'),selection_attestation_ref=ref('Attestation','inv'),**A)
    cp=roundtrip(x); old=classes[kind].from_dict(cp['checkpoint_payload'][kind][0])
    value=(ref('Alien','gr'),) if field.endswith('_refs') else b.release_ref
    forged=replace(old,**{field:value}); cp['checkpoint_payload'][kind][0]=forged.as_dict()
    for row in cp['checkpoint_payload']['selection_index']:
        if row['receipt_ref']==old.ref.as_dict():row['receipt_ref']=forged.ref.as_dict()
    cp['checkpoint_hash']=semantic_hash(cp['checkpoint_payload'])
    with pytest.raises(LearnedProductLifecycleError,match='semantic replay|native operations'):B5.from_checkpoint(cp)


def test_public_reader_waits_until_rollback(monkeypatch):
    x=B5(); a=register(x,subject('gr-reader')); before=roundtrip(x)
    appended=Event(); unblock=Event(); attempted=Event(); finished=Event(); errors=[]; reads=[]; saved=x._append_events
    def pause(events):
        saved(events); appended.set(); assert unblock.wait(5); raise Fault('pending')
    monkeypatch.setattr(x,'_append_events',pause)
    def writer():
        try:x.publish_product(a.release_ref,**A)
        except Fault as e:errors.append(e)
    def reader():
        attempted.set(); reads.append(x.export_checkpoint()); finished.set()
    wt=Thread(target=writer);wt.start(); assert appended.wait(5)
    rt=Thread(target=reader);rt.start();assert attempted.wait(5)
    blocked=not finished.wait(.1);unblock.set();wt.join(5);rt.join(5)
    assert blocked and not wt.is_alive() and not rt.is_alive()
    assert len(errors)==1 and reads==[before]


def test_m2_nested_metadata_cannot_change_release_closure():
    from rawlsing_next.pre553_learned_product_release import ClosureObject
    repo=M2Repository(); raw={'nested':[{'v':'original'}]}
    obj=ClosureObject('DEPENDENCY',(ref('Member','gr'),),True,metadata=raw); repo.register_closure(obj)
    old=obj.ref; raw['nested'][0]['v']='external'
    with pytest.raises(TypeError):repo.closure_exact(old).metadata['nested'][0]['v']='internal'
    assert repo.closure_exact(old).ref==old and obj.metadata['nested'][0]['v']=='original'
