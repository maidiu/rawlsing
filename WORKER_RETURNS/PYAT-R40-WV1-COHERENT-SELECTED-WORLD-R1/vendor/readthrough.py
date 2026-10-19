"""Permission-bounded E04 TEST_ONLY service adapter; accepted owners unchanged."""
from copy import deepcopy
from fractions import Fraction
import bootstrap
from product.service import GenericSelectedWorldService
from product.nonparent import consume
from rawlsing_next import pre553_learned_product_release as m2
from rawlsing_next import pre553_learned_empirical_adjudication as m1
from rawlsing_next import pre553_learned_world_composition as i4
from rawlsing_next.pre553_empirical_objects import ExactRef,EmpiricalFact,EmpiricalQuerySpec,EmpiricalPredicate,canonicalize,semantic_hash
from fixture import ref

class ReadThroughError(ValueError):pass
def require(ok,reason):
    if not ok:raise ReadThroughError(reason)

class ExactProducerCatalog:
    """Exact producer objects stay producer-owned. No fuzzy/source fallback."""
    def __init__(self,objects):self.objects=dict(objects)
    def get(self,reference):
        require(isinstance(reference,ExactRef),'EXACT_CATALOG_REF_REQUIRED')
        obj=self.objects.get(reference.key);require(obj is not None,'PRODUCER_OBJECT_UNAVAILABLE')
        require(isinstance(obj,(EmpiricalFact,EmpiricalQuerySpec,EmpiricalPredicate,m1.LearnedEmpiricalDisposition)),'PRODUCER_OBJECT_TYPE_MISMATCH')
        require(obj.ref==reference,'PRODUCER_OBJECT_REF_MISMATCH')
        require(semantic_hash(obj.semantic_projection())==reference.content_hash,'PRODUCER_PREIMAGE_MISMATCH')
        return obj

class ReleaseReadThroughProvider:
    def __init__(self,prepared):
        self.prepared=prepared;self.world=prepared.native_provider.world
        self.catalog=ExactProducerCatalog(prepared.objects);self.records=deepcopy(prepared.records)
        self.trace=[];self.expected_release=prepared.composition.m2_artifacts.release.ref
        self.expected_subject=prepared.composition.m1_disposition.ref
        self.selection_key=prepared.composition.b5_selection_receipt.selection_key_ref
        self.selection_receipt=prepared.composition.b5_selection_receipt.ref
        self.last_bindings=[]
    def resolve(self,target,conditions):
        p=self.prepared
        selected=p.lifecycle.resolve_selection_exact(self.selection_key,self.selection_receipt)
        require(selected.state=='CURRENT_SELECTED' and selected.selected_release_ref==self.expected_release,'SELECTED_RELEASE_BINDING_MISMATCH')
        state=p.lifecycle.lifecycle_state(selected.selected_release_ref)
        require(state.validity=='VALID' and state.publication=='PUBLISHED','RELEASE_NOT_FRESH_USE_VALID')
        require(p.lifecycle.audit_replay().replay_state=='REPLAY_VERIFIED','LIFECYCLE_REPLAY_MISMATCH')
        resolution=m2.resolve_release_exact(p.repository,selected.selected_release_ref)
        require(resolution.receipt.representation_integrity_state=='VERIFIED','RELEASE_RESOLUTION_UNVERIFIED')
        require(resolution.subject.ref==self.expected_subject,'WRONG_RELEASE_SUBJECT')
        subject=self.catalog.get(resolution.subject.ref)
        m1.verify_m1_disposition_replay(subject)
        # Existing I4 validates the same source-owned disposition/closure binding,
        # with no lifecycle actions during the read.
        from dataclasses import replace
        checked=i4.compose_learned_world(replace(p.contract,lifecycle_actions=()),m2_repository=p.repository,lifecycle_executor=p.lifecycle,m1_disposition=subject)
        require(checked.receipt.terminal_state=='RULE_SATISFIED' and checked.m2_artifacts.release.ref==selected.selected_release_ref,'I4_SUBJECT_RELEASE_MISMATCH')
        record=self.records.get((target,conditions));require(record is not None,'RELEASE_QUERY_NOT_INCLUDED')
        fact=self.catalog.get(record['fact_ref']);query=self.catalog.get(record['query_ref']);predicate=self.catalog.get(record['predicate_ref'])
        require(fact.ref in subject.empirical_fact_refs and query.ref in subject.empirical_query_spec_refs and predicate.ref in subject.empirical_predicate_refs,'FACT_NOT_IN_SELECTED_SUBJECT')
        closure=p.repository.closure_exact(resolution.release_core.dependency_closure_ref)
        require(all(x.ref in closure.member_refs for x in (fact,query,predicate)),'RELEASE_DEPENDENCY_INCOMPLETE')
        require(fact.empirical_query_spec_ref==query.ref.as_dict() and fact.condition_predicate_ref==predicate.ref.as_dict(),'FACT_QUERY_PREDICATE_MISMATCH')
        require(fact.risk_set_ref==query.risk_set_ref and fact.measure_basis_ref==query.measure_basis_ref,'RISK_OR_MEASURE_MISMATCH')
        template=record['template'];require(semantic_hash(template)==record['template_hash'],'PROJECTION_RECORD_CHANGED')
        require(template['producer_fact_ref']==fact.ref.as_dict() and template['producer_query_ref']==query.ref.as_dict(),'PROJECTION_FACT_BINDING_MISMATCH')
        require(template['permission_root']=='TEST_ONLY_E04_SOURCE_ROOT' and template['source_universe_ref']==self.world['source']['universe'].ref.as_dict(),'SOURCE_PERMISSION_BINDING_MISMATCH')
        require(template['target']==target and template['conditioners']==[list(x) for x in conditions],'TARGET_CONDITION_ROLE_MISMATCH')
        require(canonicalize(fact.empirical_universe_refs)==[template['source_universe_ref']],'CROSS_SOURCE_PERSON_BINDING')
        require(template['risk_set_ref']==canonicalize(fact.risk_set_ref),'DENOMINATOR_BINDING_MISMATCH')
        binding=dict(learned_release_ref=selected.selected_release_ref.as_dict(),b5_selection_ref=selected.receipt_ref.as_dict(),m1_subject_ref=subject.ref.as_dict(),m2_resolution_ref=resolution.receipt.ref.as_dict(),i4_verification_ref=checked.receipt.ref.as_dict(),producer_fact_ref=fact.ref.as_dict(),producer_query_ref=query.ref.as_dict(),producer_predicate_ref=predicate.ref.as_dict(),consumer='NONPARENT_OPTIONS',permission='EXISTING_E04_TEST_ONLY_SOURCE_ROLE_SCOPE; NOT_B5_PERMISSION')
        return fact,template,binding
    def step(self,target,conditions):
        conditions=self.prepared.native_provider._validate(target,conditions)
        fact,template,binding=self.resolve(target,conditions)
        result=deepcopy(template);denominator=fact.raw_denominator_support
        result['denominator']=denominator
        cells=[]
        if fact.typed_state=='SUPPORTED':
            for cell in canonicalize(fact.target_topology)['complete_cell_semantic_projection']:
                cell=deepcopy(cell);fraction=Fraction(cell['raw_numerator_support'],denominator)
                cell['raw_probability_exact_fraction']={'$exact_fraction':[fraction.numerator,fraction.denominator]}
                cell['weighted_probability_exact_fraction_if_authorized']=None;cells.append(cell)
        require(result['cells']==cells and template['denominator']==denominator,'PRODUCER_PROJECTION_MISMATCH')
        result['cells']=cells
        result['learned_release_binding']=binding
        result['content_hash']=semantic_hash({k:v for k,v in result.items() if k!='content_hash'})
        self.trace.append(dict(call='SELECTED_RELEASE_FACT_VALUES_READ',**binding,denominator=denominator,cells=deepcopy(cells)))
        self.last_bindings.append(binding)
        return result
    def progressive(self,target,conditions):
        conditions=self.prepared.native_provider._validate(target,conditions)
        return [self.step(target,conditions[:n]) for n in range(1,len(conditions)+1)]

class ReadThroughService(GenericSelectedWorldService):
    def __init__(self,prepared):
        # Retain the actual original service's world/snapshot/structural permissions.
        self.__dict__.update(prepared.service.__dict__)
        self.provider=ReleaseReadThroughProvider(prepared)
    def possibilities(self,snapshot,*,target='Y',conditions=(('A',1),('B',1),('C',1)),consumer='GENERIC'):
        require(consumer=='NONPARENT_OPTIONS','TEST_ONLY_CONSUMER_PERMISSION_UNAVAILABLE')
        start=len(self.value_reads);self.provider.last_bindings=[]
        result=super().possibilities(snapshot,target=target,conditions=conditions,consumer=consumer)
        reads=[x for x in self.value_reads[start:] if x['channel']=='empirical']
        if result['steps']:
            require(len(reads)==len(self.provider.last_bindings),'CONSUMER_RELEASE_READSET_MISMATCH')
            for read,binding in zip(reads,self.provider.last_bindings):read['learned_release_binding']=deepcopy(binding)
        return result

def execute(prepared):
    service=ReadThroughService(prepared)
    return service,consume(service,prepared.snapshot)
