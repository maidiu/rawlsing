"""Executed I01 glue for pinned P04/S00E -> P01 B01E -> native M2/B5.

SOURCE_FREE / LOCAL_UNAUTHENTICATED only. No scientific/use issuer or E_pre.
P01's generic durable owner executes a caller-bound real query callback; its
frozen Field Forge workload adapter is separately regression-tested, not
misrepresented as a consumer of this unary progressive result.
"""
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path

from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize, canonical_json, semantic_hash
from rawlsing_next import pre553_n9_n10w_progressive_candidate as progressive
from rawlsing_next import pre553_selected_world_progressive_contract as selected
from rawlsing_next import r3_s02_seam_witness as seam
from rawlsing_next import pre553_governed_batch_checkpoint_integration_candidate as durable
from rawlsing_next.pre553_batch_durable_checkpoint_candidate import _atomic_write_bytes, ledger_lock
from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec, ExecutorBinding, ExecutionOutcome
from rawlsing_next.pre553_learned_product_lifecycle import LearnedProductLifecycleExecutor as B5, LearnedProductLifecycleSubject
from rawlsing_next import pre553_learned_product_release as m2

SCHEMA='I01_SOURCEFREE_SAVED_WORLD@1'
SCENARIO='I01_SOURCEFREE_PROGRESSIVE'
MODE='LOCAL_UNAUTHENTICATED'

class I01Error(ValueError):pass


def local_ref(kind, material):
    """Local content identity, never issuer authentication or a capability."""
    h=semantic_hash(material)
    return ExactRef(kind,f'urn:rawlsing:i01:local:{kind}:sha256:{h}',h)

PRODUCER=local_ref('ProducerContract',{'consumer':seam.ContractOnlySeamConsumer.CONSUMER_REF,'scope':'SOURCE_FREE_ONLY'})
EXECUTOR=local_ref('ExecutorContract',{'operation':SCENARIO,'scope':'SOURCE_FREE_ONLY'})
FAMILY=local_ref('ProductFamily',SCHEMA)
PURPOSE=local_ref('SelectionPurpose','source-free-inspection')
CEILING=local_ref('SourceFreeCeiling',{'source_permission':'SOURCE_FREE_ONLY','external_rights':False})


def save_json(path,payload):
    raw=canonical_json(payload).encode()
    _atomic_write_bytes(Path(path),raw)
    return hashlib.sha256(raw).hexdigest()


def contract_payload(c):
    return dict(contract_id=c.contract_id,world_tag=c.world_tag,source_universe_ref=c.source_universe_ref.as_dict(),release_ref=c.release_ref.as_dict(),risk_set_ref=c.risk_set_ref.as_dict(),selection_metadata=dict(c.selection_metadata),real_current=c.real_current)


def bundle_from_payload(payload):
    c=payload['selected_contract']
    contract=selected.SelectedWorldContract(contract_id=c['contract_id'],world_tag=c['world_tag'],source_universe_ref=ExactRef(**c['source_universe_ref']),release_ref=ExactRef(**c['release_ref']),risk_set_ref=ExactRef(**c['risk_set_ref']),selection_metadata=c['selection_metadata'],real_current=c['real_current'])
    b=payload['bundle']
    return seam.SociologicalWorldBundle(bundle_id=b['bundle_id'],contract_version=b['contract_version'],content_hash=b['content_hash'],world_scope=b['world_scope'],channels=tuple(seam.ChannelValue(**v) for v in b['channels']),evidence_graph=tuple(b['evidence_graph']),conditions=tuple(b['conditions']),steps=tuple(b['steps']),replay=b['replay'],selected_world_contract=contract)


def artifact_path(root,ref):
    if ref.kind!='I01SourceFreeSavedWorld' or ref!=local_ref(ref.kind,load_artifact_unchecked(root,ref)):
        raise I01Error('SAVED_WORLD_EXACT_IDENTITY_MISMATCH')
    return Path(root)/'artifacts'/(ref.content_hash+'.json')


def load_artifact_unchecked(root,ref):
    path=Path(root)/'artifacts'/(ref.content_hash+'.json')
    if not path.is_file():raise I01Error('SAVED_WORLD_UNAVAILABLE')
    raw=path.read_bytes()
    if hashlib.sha256(raw).hexdigest()!=ref.content_hash:raise I01Error('SAVED_WORLD_BYTES_MISMATCH')
    payload=json.loads(raw)
    if payload.get('schema')!=SCHEMA or payload.get('security_mode')!=MODE:raise I01Error('SOURCE_FREE_SCOPE_MISMATCH')
    return payload


def load_artifact(root,ref):
    artifact_path(root,ref)
    payload=load_artifact_unchecked(root,ref)
    if payload['producer_contract_ref']!=PRODUCER.as_dict():raise I01Error('PRODUCER_SUBSTITUTION')
    return payload


def open_world_session(root):
    contract,world=selected.select_world()
    predicate=progressive._joint_predicate(world,(('A',1),('B',1),('C',1)))
    query=progressive._producer_query(world,predicate)
    source=world['source'];release=source['repo'].resolve_release_exact(contract.release_ref)
    unit=BatchUnitSpec(job_kind='QUERY',job_ref=query.ref,release_refs=(contract.release_ref,),semantic_input_refs=(predicate.ref,world['qauth'].ref,contract.risk_set_ref))
    calls=[]
    def execute(presented):
        if presented!=unit:raise I01Error('EXACT_QUERY_BINDING_MISMATCH')
        calls.append(presented.unit_ref.as_dict())
        chain=selected.run_selected_world_progressive_chain(contract,world=world)
        if chain.steps[-1].invocation_log[0]['inputs']['empirical_query']!=query.ref.as_dict():
            raise I01Error('ACTUALLY_EXECUTED_QUERY_MISMATCH')
        bundle=seam.build_sociological_bundle()
        if [r['parent_refs'][0] for r in bundle.evidence_graph]!=[s.produced_evidence.evidence_ref.as_dict() for s in chain.steps]:
            raise I01Error('PROGRESSIVE_BUNDLE_EVIDENCE_SUBSTITUTION')
        contract.verify_bindings(source_universe_ref=bundle.selected_world_contract.source_universe_ref,release_ref=bundle.selected_world_contract.release_ref,risk_set_ref=bundle.selected_world_contract.risk_set_ref)
        consumer=seam.ContractOnlySeamConsumer(bundle)
        result=consumer.compute_scenario(SCENARIO,list(seam.P04_STEPS))
        if result['status']!='COMPUTED':raise I01Error('NATIVE_NUMERIC_CONSUMER_REFUSED:'+str(result))
        receipt=consumer.get_receipt().as_dict()
        payload=canonicalize(dict(schema=SCHEMA,security_mode=MODE,producer_contract_ref=PRODUCER.as_dict(),selected_contract=contract_payload(contract),bundle=bundle.as_dict(),numeric_result=result,consumer_receipt=receipt,producer_invocations=chain.invocation_log,query_ref=query.ref.as_dict(),predicate_ref=predicate.ref.as_dict(),source_release_ref=contract.release_ref.as_dict()))
        result_ref=local_ref('I01SourceFreeSavedWorld',payload)
        path=Path(root)/'artifacts'/(result_ref.content_hash+'.json');path.parent.mkdir(parents=True,exist_ok=True)
        if save_json(path,payload)!=result_ref.content_hash:raise I01Error('ARTIFACT_WRITE_MISMATCH')
        return ExecutionOutcome(result_refs=(result_ref,),provenance_refs=(query.ref,predicate.ref,contract.release_ref,*unit.semantic_input_refs))
    session=durable.open_session(manifest=BatchManifest((unit,)),repository=source['repo'],executors={'QUERY':ExecutorBinding(EXECUTOR,execute)},root=root,source_sha256=release.source_artifact_ref.content_hash)
    return session,world,query,calls


def admit_saved_world(session):
    receipts=durable.admit_saved_receipts(session)
    if len(receipts)!=1 or receipts[0].state!='COMPLETED' or len(receipts[0].result_refs)!=1:raise I01Error('DURABLE_WORLD_RESULT_NOT_COMPLETED')
    ref=receipts[0].result_refs[0]
    payload=load_artifact(session.store.root,ref)
    if payload['query_ref']!=session.manifest.units[0].job_ref.as_dict() or payload['source_release_ref']!=session.identity.release_refs[0].as_dict():raise I01Error('DURABLE_ARTIFACT_SCOPE_MISMATCH')
    return ref,payload,receipts[0]


def reconstruct_m2(payload,subject_ref,checkpoint_ref):
    bundle=bundle_from_payload(payload);c=bundle.selected_world_contract
    dependencies=(c.release_ref,ExactRef(**payload['query_ref']),ExactRef(**payload['predicate_ref']),c.risk_set_ref)
    determinant=local_ref('SelectedWorldDeterminant',contract_payload(c))
    evidence=tuple(ExactRef(**p) for row in bundle.evidence_graph for p in row['parent_refs'])
    repo=m2.M2Repository()
    m2.register_producer_subject(repo,subject_ref=subject_ref,subject_kind='IMMUTABLE_LEARNED_PRODUCT',producer_contract_ref=PRODUCER,typed_state='SUPPORTED',required_dependency_refs=dependencies,required_determinant_refs=(determinant,),required_replay_refs=(checkpoint_ref,subject_ref),required_explanation_refs=evidence)
    members={'AUTHORITY':(PRODUCER,),'DEPENDENCY':dependencies,'DETERMINANT':(determinant,),'REPLAY_RECONSTRUCTION':(checkpoint_ref,subject_ref),'EXPLANATION_LINEAGE':(subject_ref,PRODUCER,*evidence)}
    closures={kind:m2.constitute_closure(repo,closure_kind=kind,member_refs=refs,metadata={'replay_grade':'EXACT_MATERIALIZED_DEREFERENCE'} if kind=='REPLAY_RECONSTRUCTION' else None) for kind,refs in members.items()}
    release=m2.constitute_release(repo,release_subject_ref=subject_ref,release_subject_kind='IMMUTABLE_LEARNED_PRODUCT',semantic_producer_contract_ref=PRODUCER,authority_closure_ref=closures['AUTHORITY'].ref,dependency_closure_ref=closures['DEPENDENCY'].ref,determinant_closure_ref=closures['DETERMINANT'].ref,replay_reconstruction_ref=closures['REPLAY_RECONSTRUCTION'].ref,explanation_lineage_ref=closures['EXPLANATION_LINEAGE'].ref)
    locator=local_ref('ArtifactLocator',subject_ref.as_dict());integrity=local_ref('ArtifactIntegrity',subject_ref.as_dict())
    m2.register_representation(repo,release_ref=release.ref,resolution_mode='CONTENT_ADDRESSED_MATERIALIZATION',resolver_or_locator_ref=locator,representation_integrity_ref=integrity,resolved_subject_ref=subject_ref,producer_contract_ref=PRODUCER)
    binding=m2.publish_binding(repo,release_ref=release.ref,resolution_mode='CONTENT_ADDRESSED_MATERIALIZATION',resolver_or_locator_ref=locator,representation_integrity_ref=integrity)
    return repo,release,binding,determinant,dependencies


@dataclass
class Product:
    root:Path
    session:object
    lifecycle:B5
    repository:object
    release:object
    binding:object
    selection_key:object
    subject_ref:ExactRef
    selected_receipt:object
    determinant:ExactRef
    calls:list


def build_product(root):
    root=Path(root);root.mkdir(parents=True,exist_ok=True)
    with ledger_lock(root/'.i01.integration.lock'):
        return _build_product_locked(root)


def _build_product_locked(root):
    if (root/'product_index.json').exists() or (root/'lifecycle.json').exists():
        if not (root/'product_index.json').exists() or not (root/'lifecycle.json').exists():
            raise I01Error('PARTIAL_LIFECYCLE_PUBLICATION_HOLD')
        product=restore_product(root)
        with ledger_lock(root/'.p01.integration.lock'):
            report=durable.run_to_completion(product.session)
        return product,report.summary()
    session,world,query,calls=open_world_session(root)
    with ledger_lock(root/'.p01.integration.lock'):
        report=durable.run_to_completion(session)
    subject_ref,payload,saved=admit_saved_world(session)
    cp=session.checkpoint()
    repo,release,binding,determinant,dependencies=reconstruct_m2(payload,subject_ref,cp.checkpoint_ref)
    life=B5();c=bundle_from_payload(payload).selected_world_contract
    dets=tuple(sorted((determinant,c.release_ref),key=lambda r:r.key))
    subject=LearnedProductLifecycleSubject(release_ref=release.ref,product_ref=subject_ref,product_family_ref=FAMILY,producer_owner_ref=PRODUCER,producer_contract_ref=PRODUCER,semantic_projection_hash=subject_ref.content_hash,authority_snapshot_refs=tuple(query.authority_snapshot_refs),direct_dependency_refs=dependencies,determinant_refs=dets,determinant_set_hash=semantic_hash([r.as_dict() for r in dets]),replay_root_ref=cp.checkpoint_ref,selection_scope_ref=c.risk_set_ref,build_or_release_receipt_refs=(saved.receipt_ref,),producer_permission_ceiling_ref=CEILING)
    life.stage_release(subject);life.verify_m2_release_subject_exact(repo,release.ref)
    authority=dict(event_authority_ref=PRODUCER,event_rule_ref=EXECUTOR)
    life.register_product(release.ref,**authority);life.publish_product(release.ref,**authority)
    key=life.selection_key(product_family_ref=FAMILY,selection_scope_ref=c.risk_set_ref,selection_purpose_ref=PURPOSE)
    chosen=life.select_current(key.ref,release.ref,expected_previous_receipt_ref=None,selection_attestation_ref=saved.receipt_ref,**authority)
    product=Product(root,session,life,repo,release,binding,key,subject_ref,chosen,determinant,calls)
    save_json(root/'lifecycle.json',life.export_checkpoint())
    save_json(root/'product_index.json',dict(subject_ref=subject_ref.as_dict(),release_ref=release.ref.as_dict(),binding_ref=binding.ref.as_dict(),selection_key_ref=key.ref.as_dict(),selected_receipt=chosen.as_dict(),determinant_ref=determinant.as_dict(),checkpoint_ref=cp.checkpoint_ref.as_dict()))
    return product,report.summary()


def restore_product(root):
    from rawlsing_next.pre553_learned_product_lifecycle import CurrentSelectionReceipt,SelectionKey
    root=Path(root);session,world,query,calls=open_world_session(root)
    index=json.loads((root/'product_index.json').read_text());subject_ref,payload,saved=admit_saved_world(session)
    if subject_ref.as_dict()!=index['subject_ref'] or session.checkpoint().checkpoint_ref.as_dict()!=index['checkpoint_ref']:raise I01Error('SAVED_INDEX_SCOPE_MISMATCH')
    repo,release,binding,determinant,_=reconstruct_m2(payload,subject_ref,session.checkpoint().checkpoint_ref)
    if release.ref.as_dict()!=index['release_ref'] or binding.ref.as_dict()!=index['binding_ref'] or determinant.as_dict()!=index['determinant_ref']:raise I01Error('SAVED_M2_IDENTITY_MISMATCH')
    life=B5.from_checkpoint(json.loads((root/'lifecycle.json').read_text()))
    chosen=CurrentSelectionReceipt.from_dict(index['selected_receipt'])
    life.verify_m2_release_subject_exact(repo,release.ref)
    key=next(k for k in life.export_checkpoint()['checkpoint_payload']['selection_keys'] if k['record_ref']==index['selection_key_ref'])
    return Product(root,session,life,repo,release,binding,SelectionKey.from_dict(key),subject_ref,chosen,determinant,calls)


def serve(product,*,historical=False):
    # Admit a durable COMPLETED reference before any numeric dereference.
    subject_ref,payload,saved=admit_saved_world(product.session)
    if subject_ref!=product.subject_ref:raise I01Error('DURABLE_SUBJECT_SUBSTITUTION')
    if historical:
        resolved=product.lifecycle.resolve_current_as_of(product.selection_key.ref,as_of_event_ref=product.selected_receipt.current_select_event_ref)
    else:
        receipt_ref=product.lifecycle.current_selection_receipt_ref(product.selection_key.ref)
        resolved=product.lifecycle.resolve_selection_exact(product.selection_key.ref,receipt_ref)
    if resolved.state!='CURRENT_SELECTED' or resolved.selected_release_ref!=product.release.ref:raise I01Error('NO_CURRENT_SOURCEFREE_WORLD')
    product.lifecycle.verify_m2_release_subject_exact(product.repository,resolved.selected_release_ref)
    resolution=m2.resolve_release_exact(product.repository,resolved.selected_release_ref,publication_binding_refs=(product.binding.ref,))
    if resolution.subject is None or resolution.subject.ref!=subject_ref:raise I01Error('M2_PRODUCER_SUBJECT_SUBSTITUTION')
    consumer=seam.ContractOnlySeamConsumer(bundle_from_payload(payload))
    numeric=consumer.compute_scenario(SCENARIO,list(seam.P04_STEPS));receipt=consumer.get_receipt().as_dict()
    if canonicalize(numeric)!=payload['numeric_result'] or canonicalize(receipt)!=payload['consumer_receipt']:raise I01Error('ACTUAL_CONSUMER_REPLAY_MISMATCH')
    return dict(security_mode=MODE,historical=historical,selected_release_ref=resolved.selected_release_ref.as_dict(),producer_subject_ref=subject_ref.as_dict(),durable_checkpoint_ref=product.session.checkpoint().checkpoint_ref.as_dict(),durable_receipt_ref=saved.receipt_ref.as_dict(),m2_resolution_receipt={**resolution.receipt.semantic_projection(),'receipt_ref':resolution.receipt.ref.as_dict()},numeric_result=numeric,consumer_receipt=receipt)


def invalidate(product):
    receipt=product.lifecycle.declare_invalidation((product.determinant,),event_authority_ref=PRODUCER,event_rule_ref=EXECUTOR,dependency_closure_receipt_ref=product.release.dependency_closure_ref,selection_attestation_ref=product.selected_receipt.ref,current_transitions={product.selection_key.ref.key:None})
    save_json(product.root/'lifecycle.json',product.lifecycle.export_checkpoint())
    return receipt.as_dict()
