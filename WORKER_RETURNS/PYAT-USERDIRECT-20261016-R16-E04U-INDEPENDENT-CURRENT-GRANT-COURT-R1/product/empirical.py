"""Versioned generic facade over native N10E/C1/F8; no parallel estimator."""
from copy import deepcopy
from dataclasses import dataclass,fields
import json
from rawlsing_next.pre553_empirical_objects import canonical_json
from rawlsing_next.pre553_empirical_objects import ExactRef,canonicalize,semantic_hash
from rawlsing_next.pre553_empirical_possibility_provider import provide_empirical_possibility_slice
from rawlsing_next.pre553_analytical_composition import compose_positioned_subject_possibility
from rawlsing_next.source_backed_positioned_subject_possibility import evaluate_positioned_subject_possibility
from rawlsing_next import pre553_n9_n10w_progressive_candidate as e03
from rawlsing_next import pre553_empirical_query as i03
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry,require_positive_authority
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
from rawlsing_next.tests import test_pre553_empirical_query as fx
from rawlsing_next.tests import c1_at08_at13_fixture as c1
CONTRACT='E04_GENERIC_PROGRESSIVE_PROVIDER_CANDIDATE@1'

def build_source(*,changed=False,support_loss=False,same_marginals=False):
    rows=e03.synthetic_world_rows()
    if changed or same_marginals:
        next(r for r in rows if all(r['responses'][q]==1 for q in ('A','B','C')) and r['responses']['Y']==0)['responses']['Y']=1
    # New source/release identity for an actual changed producer input. Every
    # step inside one run retains exactly the same release/risk/permission root.
    if same_marginals:
        next(r for r in rows if all(r['responses'][q]==0 for q in ('A','B','C')) and r['responses']['Y']==1)['responses']['Y']=0
    if support_loss:rows=[r for r in rows if not all(r['responses'][q]==1 for q in ('A','B','C'))]
    tag='e04-same-marginals-r4' if same_marginals else 'e04-support-loss-r3' if support_loss else 'e04-counterfactual-r2' if changed else 'e04-base-r1'
    source=fx._build_source(tag,rows,question_namespace='E04_NATIVE_BINARY',risk_sets={'R_ALL':{q:{r['id'] for r in rows} for q in ('A','B','C','Y')}},risk_namespace=tag)
    source['risk_refs']['R']=source['risk_refs']['R_ALL']
    qauth=fx._query_authority(tag+'-query')
    world=dict(tag=tag,source=source,qauth=qauth,registry=fx._registry(source,qauth),pairing=c1.make_pairing_authority(tag),model_rule=c1.make_model_rule(source['universe'].ref,tag),rows_hash=semantic_hash(rows),permission_root='TEST_ONLY_E04_SOURCE_ROOT',publication='2026-04-01' if changed or support_loss or same_marginals else '2026-03-01')
    world['query_permits']={name:dict(target_ref=source['qrefs'][name].as_dict(),conditioner_refs={q:source['qrefs'][q].as_dict() for q in allowed},allowed_values=[0,1],max_conditioners=len(allowed),scope='TEST_ONLY_EXACT_QUERY_ROLES') for name,allowed in [('Y',('A','B','C')),('A',('Y',))]}
    return world

@dataclass(frozen=True)
class _AcceptedOwnerEntry:
    """Private process-local trust record. Contains no mutable descendants.

    Created only after actual native production and F8 consumption; never
    hydrated from the public projection cache or a caller's digest.
    """
    binding: str
    request: tuple
    projection: bytes
    native_owner_material: bytes


def _sealed(value):
    return canonical_json(value).encode('utf-8')


class GenericProgressiveProvider:
    """Only source-backed exact target/condition requests, ordered by caller.

    This finite synthetic source permits forward Y|A,B,C and independently
    authorized reverse A|Y. It does not authorize arbitrary coordinate refs.
    """
    def __init__(self,world):
        self.world=world;self.cache={};self.trace=[];self._binding=self._identity()
        self._accepted={}
        # Native C11 releases and their records are immutable. Pin the actual
        # accepted release object as well as its exact ref, not inventory alone.
        self._source_release=world['source']['repo'].resolve_release_exact(world['source']['release_ref'])
    def _identity(self):
        w=self.world;s=w['source']
        return semantic_hash(dict(universe=s['universe'].ref.as_dict(),release=s['release_ref'].as_dict(),risk=canonicalize(s['risk_refs']['R']),model=w['model_rule'].rule_hash,query_authority=w['qauth'].authority_ref.as_dict(),pairing=w['pairing'].as_dict(),permission_root=w['permission_root'],rows_hash=w.get('rows_hash'),publication=w.get('publication'),query_permits=w['query_permits'],coordinates={k:v.as_dict() for k,v in s['qrefs'].items()}))
    def _validate(self,target,conditions):
        if not isinstance(target,str):raise ValueError('EXACT_NATIVE_TARGET_REQUIRED')
        if not isinstance(conditions,(tuple,list)) or any(not isinstance(c,(tuple,list)) or len(c)!=2 or not isinstance(c[0],str) or type(c[1]) is not int for c in conditions):raise ValueError('ORDERED_EXACT_NATIVE_VALUE_BINDINGS_REQUIRED')
        conditions=tuple(tuple(c) for c in conditions)
        if not conditions or len(set(q for q,v in conditions))!=len(conditions):raise ValueError('EXACT_NONEMPTY_UNIQUE_ORDERED_CONDITIONERS_REQUIRED')
        if self._identity()!=self._binding:raise ValueError('SOURCE_QUERY_PERMISSION_BINDING_CHANGED')
        try:release=self.world['source']['repo'].resolve_release_exact(self.world['source']['release_ref'])
        except (KeyError,TypeError):raise ValueError('ACCEPTED_NATIVE_SOURCE_UNAVAILABLE') from None
        if release is not self._source_release:raise ValueError('ACCEPTED_NATIVE_SOURCE_REPLACED')
        permit=self.world['query_permits'].get(target)
        coordinates=self.world['source']['qrefs']
        if permit is None or permit['target_ref']!=coordinates[target].as_dict() or len(conditions)>permit['max_conditioners'] or any(q not in permit['conditioner_refs'] or permit['conditioner_refs'][q]!=coordinates[q].as_dict() or v not in permit['allowed_values'] for q,v in conditions):raise ValueError('TARGET_CONDITION_ROLE_AUTHORITY_UNAVAILABLE')
        return conditions
    def _authorize_cached_use(self,target,conditions,accepted):
        """Historical production does not authorize a new use of its projection.

        Rebuild the exact native request and run pinned I03 authority validators
        against the currently attached registry, never a retained registry. Source
        authorities come from the immutable accepted C11 release, not a mutable
        source inventory. No evidence, cells or historical receipts are rewritten.
        """
        w=self.world;s=w['source'];registry=w['registry']
        if not isinstance(registry,AuthorityRegistry):
            raise ValueError('CURRENT_NATIVE_AUTHORITY_REGISTRY_REQUIRED')
        predicate=e03._joint_predicate(w,conditions)
        query=e03._producer_query(w,predicate,target)
        original=json.loads(accepted.native_owner_material)
        if _sealed(query.as_dict())!=_sealed(original['query']):
            raise ValueError('CURRENT_NATIVE_QUERY_OWNER_BINDING_MISMATCH')
        # Current availability of every exact authority sealed into this source
        # release is required. A same-label successor cannot substitute for it.
        source_refs=[]
        for obj in self._source_release.public_objects:
            if isinstance(obj,AuthoritySnapshot):
                current=registry.resolve_exact(obj.authority_ref).snapshot
                require_positive_authority(current)
                if _sealed(current.as_dict())!=_sealed(obj.as_dict()):
                    raise ValueError('CURRENT_NATIVE_SOURCE_GRANT_CONTENT_MISMATCH')
                source_refs.append(obj.authority_ref.as_dict())
        i03._validate_public_object_authorities(query,registry)
        i03._validate_public_object_authorities(predicate,registry)
        i03._require_exact_i03_authority_fitness(
            query=query,predicate=predicate,authority_registry=registry,
            universe_refs=(s['universe'].ref,))
        i03._parse_target_plan(query,registry)
        current=registry.resolve_exact(w['qauth'].authority_ref).snapshot
        if _sealed(current.as_dict())!=_sealed(original['query_authority_snapshot']):
            raise ValueError('CURRENT_NATIVE_QUERY_GRANT_CONTENT_MISMATCH')
        self.trace.append(dict(call='CURRENT_NATIVE_QUERY_GRANT_VALIDATED',
            query_ref=query.ref.as_dict(),source_universe_ref=s['universe'].ref.as_dict(),
            release_ref=s['release_ref'].as_dict(),risk_set_ref=canonicalize(query.risk_set_ref),
            query_authority_refs=canonicalize(query.query_authority_refs),
            source_authority_refs=source_refs,permission_root=w['permission_root']))

    def step(self,target,conditions):
        conditions=self._validate(target,conditions)
        key=(target,conditions)
        if key in self.cache:
            accepted=self._accepted.get(key)
            if accepted is None or accepted.binding!=self._binding or accepted.request!=key:
                raise ValueError('UNATTESTED_NATIVE_CACHE_ENTRY')
            try:projection=_sealed(self.cache[key])
            except (ValueError,TypeError,RecursionError):raise ValueError('INVALID_NATIVE_CACHE_PROJECTION') from None
            if projection!=accepted.projection:
                raise ValueError('NATIVE_OWNER_CACHE_PROJECTION_MISMATCH')
            # Serve fresh descendants of the trusted bytes, never aliases of
            # the untrusted mapping just compared. Full byte equality covers
            # counts, minority cells, geometry, source/risk/ordered request,
            # witnesses, fact/evidence refs, authority and F8 result state.
            self._authorize_cached_use(target,conditions,accepted)
            result=json.loads(accepted.projection)
            self.trace.append(dict(call='PROVIDER_CACHE_READ',query=repr(key),evidence_ref=result['evidence_ref'],verified_native_owner=True))
            return result
        w=self.world;s=w['source'];step=semantic_hash([target,conditions])[:16]
        pred=e03._joint_predicate(w,conditions);query=e03._producer_query(w,pred,target)
        bindings=[c1.make_conditioner_binding(binding_id=q.lower(),subject_fact_ref=ExactRef(**c1.subject_fact_ref(s,q,v)),empirical_coordinate_ref=s['qrefs'][q],comparability_authority_ref=w['pairing'],source_universe_ref=s['universe'].ref,release_ref=s['release_ref']) for q,v in conditions]
        subject_material=dict(schema='E04_OPAQUE_SYNTHETIC_SUBJECT@1',subject='GENERIC_POSITION',real_subject=False)
        consumer=c1.make_multi_conditioner_consumer_query(query_id='E04-'+step,subject_ref=ExactRef('E04_SYNTHETIC_SUBJECT','urn:test:e04:generic-subject',semantic_hash(subject_material)),target_ref=s['qrefs'][target],source_universe_ref=s['universe'].ref,release_ref=s['release_ref'],bindings=bindings,projection_kind='E04_GENERIC_EMPIRICAL_POSSIBILITY',projection_payload={'ordered_conditions':[list(c) for c in conditions]})
        witness=e03._witness(w,step,consumer,query,pred,conditions)
        args=dict(repository=s['repo'],empirical_query=query,predicate=pred,authority_registry=w['registry'],release_refs=(s['release_ref'],),consumer_query=consumer,model_rule=w['model_rule'],condition_binding_witness=witness)
        if len(conditions)==1:
            produced=provide_empirical_possibility_slice(**args);composition=produced.composition_result;route='N10E_PUBLIC_SINGLE'
        else:composition=compose_positioned_subject_possibility(**args);route='C1_PUBLIC_MULTI_BINDING'
        evidence=composition.possibility_slice_evidence_or_null
        self.trace.append(dict(call='provide_empirical_possibility_slice' if len(conditions)==1 else 'compose_positioned_subject_possibility',query_ref=query.ref.as_dict(),predicate_ref=pred.ref.as_dict(),consumer_query_ref=consumer.ref.as_dict(),witness_ref=witness.witness_ref.as_dict(),target=target,ordered_conditions=[list(c) for c in conditions],fact_state=composition.producer_fact_state,composition_hash=composition.composed_result_identity_hash))
        if evidence is None:
            return dict(state=composition.producer_fact_state,cells=[],denominator=composition.raw_denominator_support,geometry=None,uncertainty='NO_SUPPORTED_EVIDENCE',dependencies=['empirical'],conditioners=[list(c) for c in conditions],target=target,target_ref=s['qrefs'][target].as_dict(),source_universe_ref=s['universe'].ref.as_dict(),release_ref=s['release_ref'].as_dict(),risk_set_ref=canonicalize(query.risk_set_ref),permission_root=w['permission_root'],producer_query_ref=query.ref.as_dict(),producer_fact_ref=composition.producer_fact_ref.as_dict(),condition_witness_ref=witness.witness_ref.as_dict(),model_rule_hash=w['model_rule'].rule_hash)
        # Actual same evidence object, not a manually reconstructed twin.
        consumed=evaluate_positioned_subject_possibility(query=consumer,rule=w['model_rule'],evidence=(evidence,))
        self.trace.append(dict(call='evaluate_positioned_subject_possibility',produced_evidence_ref=evidence.evidence_ref.as_dict(),consumed_evidence_ref=consumed.exact_evidence_ref.as_dict() if consumed.exact_evidence_ref else None,result_state=consumed.result_state,same_evidence_object=True,consumer_result_hash=consumed.result_hash))
        result=dict(schema=CONTRACT,state=consumed.result_state,route=route,target=target,target_ref=s['qrefs'][target].as_dict(),conditioners=[list(c) for c in conditions],binding_order=[b.binding_id for b in bindings],source_universe_ref=s['universe'].ref.as_dict(),release_ref=s['release_ref'].as_dict(),risk_set_ref=canonicalize(query.risk_set_ref),permission_root=w['permission_root'],denominator=composition.raw_denominator_support,cells=canonicalize(composition.complete_cell_geometry),geometry=canonicalize(evidence.geometry),evidence_ref=evidence.evidence_ref.as_dict(),uncertainty=evidence.uncertainty_state,model_rule_hash=w['model_rule'].rule_hash,condition_witness_ref=witness.witness_ref.as_dict(),producer_query_ref=query.ref.as_dict(),producer_fact_ref=composition.producer_fact_ref.as_dict(),authority_refs=[a.as_dict() for a in evidence.authority_refs],provenance_refs=[r.as_dict() for r in evidence.provenance_refs],measure='RAW; unweighted; no causal inference',dependencies=['empirical'])
        result['content_hash']=semantic_hash(result)
        owner_material=dict(composition=composition.identity_material(),
            facts=[f.as_dict() for f in composition.producer_result.facts],
            evidence={f.name:getattr(evidence,f.name) for f in fields(evidence)},
            F8=consumed.material(),query=query.as_dict(),
            query_authority_snapshot=w['qauth'].as_dict(),
            condition_witness_ref=witness.witness_ref.as_dict(),
            request=[target,conditions],source_binding=self._binding)
        self._accepted[key]=_AcceptedOwnerEntry(self._binding,key,_sealed(result),_sealed(owner_material))
        self.cache[key]=deepcopy(result)
        return deepcopy(result)
    def progressive(self,target,conditions):
        conditions=self._validate(target,conditions)
        return [self.step(target,tuple(conditions[:depth])) for depth in range(1,len(conditions)+1)]
