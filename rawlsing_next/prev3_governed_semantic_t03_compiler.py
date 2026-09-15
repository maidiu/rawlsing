"""PSC02 governed semantic capital -> HQ-adopted T03 intake compiler.

Compiler != semantic interpreter. Only explicit governed refs/states are accepted;
question text, labels, embeddings, statistics, model judgment and similarity are not.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, authority_ref, exact_ref, semantic_hash
from rawlsing_next._prev3_structural_batch_base import BlockerClass, CandidateKind, CandidateOutcome, CandidateStage, StructuralBatchControlPlaneError
from rawlsing_next._prev3_structural_batch_records import SemanticCandidateRecord, SourceLocalIntakeRecord
from rawlsing_next._prev3_structural_batch_status import CandidateBlockerRecord, CandidateStatusRecord, SemanticReductionResult
from rawlsing_next._prev3_structural_batch_runtime import reduce_semantic_candidates

PSC02_COMPILER_CONTRACT_ID="PREV3_GOVERNED_SEMANTIC_CAPITAL_TO_ADOPTED_T03_INTAKE_COMPILER_R1@1.0.0"
T03_SEMANTIC_CANDIDATE="5f90f5b94b76babe37c289840afd89005f67dbfe"
T03_QUALIFIED_EXECUTION_TREE="545e2827bfdbaf07ffb9e54b4f822ae7db53b510"
T03_G03_COURT="48 passed"
FINAL_RELEASE_HOLD="FINAL_RELEASE_AWAITS_HQ_ADOPTED_PSC01_DENOMINATOR"
PREV3_BOUNDARY="PRE_V3_OBJECTIVE_WORLD_ONLY"
OBL063_BOUNDARY="OBL063_PERSON_TERMINAL_DRIVER_TYPE_SEMANTICS_QUARANTINED"

class GovernedSemanticCompilerError(StructuralBatchControlPlaneError): pass
class CurrentnessBlockedError(GovernedSemanticCompilerError): pass
class FixtureSchemaError(GovernedSemanticCompilerError): pass
class CarrierKind(str,Enum): FQRA="FQRA"; QSMV2="QSMV2"; NEGATIVE_BLOCK="NEGATIVE_BLOCK"; RESPONSE_SEMANTICS="RESPONSE_SEMANTICS"; TYPED_RELATION="TYPED_RELATION"
class EpistemicClass(str,Enum): MANUAL_ADJUDICATED="MANUAL_ADJUDICATED"; DETERMINISTIC_DERIVATION="DETERMINISTIC_DERIVATION"
class SemanticJurisdiction(str,Enum): SOURCE_SEMANTIC="SOURCE_SEMANTIC"; RAWLSING_SEMANTIC="RAWLSING_SEMANTIC"
class SemanticAuthorityState(str,Enum): POSITIVE="POSITIVE"; NEGATIVE_FORBIDDEN="NEGATIVE_FORBIDDEN"; BLOCKED="BLOCKED"; REVIEW_REQUIRED="REVIEW_REQUIRED"; SUPERSEDED="SUPERSEDED"
class CurrentnessState(str,Enum): CURRENT="CURRENT"; HISTORICAL_NONCURRENT="HISTORICAL_NONCURRENT"; MISSING="MISSING"; AMBIGUOUS="AMBIGUOUS"
class EquivalenceDecision(str,Enum): AUTHORIZED="AUTHORIZED"; DENIED="DENIED"; NOT_APPLICABLE="NOT_APPLICABLE"; UNKNOWN_AUTHORITY="UNKNOWN_AUTHORITY"; CONFLICTING_AUTHORITY="CONFLICTING_AUTHORITY"; EXPIRED_OR_STALE="EXPIRED_OR_STALE"

def _enum(v:Any,t:type[Enum],n:str)->Enum:
    try: return v if isinstance(v,t) else t(v)
    except (TypeError,ValueError) as e: raise FixtureSchemaError(f"unknown {n}: {v!r}") from e
def _ref(k:str,o:str,m:Mapping[str,Any])->ExactRef: return ExactRef(k,o,semantic_hash(m))
def _uniq(refs:Iterable[ExactRef])->tuple[ExactRef,...]:
    d={r.key:r for r in refs}; return tuple(d[k] for k in sorted(d))
def _auth_ref(a:AuthorityRef)->ExactRef: return _ref("PSC02_GOVERNED_AUTHORITY_REF",f"{a.authority_id}@{a.authority_version}",{"contract":PSC02_COMPILER_CONTRACT_ID,"authority_ref":a.as_dict()})

@dataclass(frozen=True,slots=True)
class EquivalenceAuthority:
    relation_ref:ExactRef; decision:EquivalenceDecision; decision_ref:ExactRef; authority_ref:AuthorityRef
    def __post_init__(self):
        object.__setattr__(self,"relation_ref",exact_ref(self.relation_ref)); object.__setattr__(self,"decision",_enum(self.decision,EquivalenceDecision,"equivalence decision")); object.__setattr__(self,"decision_ref",exact_ref(self.decision_ref)); object.__setattr__(self,"authority_ref",authority_ref(self.authority_ref))
    @property
    def provenance_refs(self): return (self.relation_ref,self.decision_ref,_auth_ref(self.authority_ref))

@dataclass(frozen=True,slots=True)
class GovernedSemanticCapitalRecord:
    carrier_kind:CarrierKind; carrier_locator_ref:ExactRef; carrier_row_ref:ExactRef
    source_family_ref:ExactRef; source_release_ref:ExactRef; source_question_ref:ExactRef; implementation_ref_or_exact_na:ExactRef
    authority_ref:AuthorityRef; authority_snapshot_ref:ExactRef; epistemic_class:EpistemicClass; jurisdiction:SemanticJurisdiction; authority_state:SemanticAuthorityState
    currentness_state:CurrentnessState; currentness_ref:ExactRef|None; noncurrent_disposition_ref:ExactRef|None
    response_category_semantics_ref:ExactRef; routing_applicability_ref:ExactRef; structural_use_ceiling_ref:ExactRef
    semantic_core_ref:ExactRef; semantic_schema_ref:ExactRef; negative_ceiling_ref:ExactRef; type_class_ceiling_ref:ExactRef
    evidence_admission_refs:tuple[ExactRef,...]; provenance_refs:tuple[ExactRef,...]; equivalence_authorities:tuple[EquivalenceAuthority,...]
    candidate_kind:CandidateKind=CandidateKind.STRUCTURAL_POSITION
    def __post_init__(self):
        object.__setattr__(self,"carrier_kind",_enum(self.carrier_kind,CarrierKind,"carrier_kind")); object.__setattr__(self,"authority_ref",authority_ref(self.authority_ref)); object.__setattr__(self,"epistemic_class",_enum(self.epistemic_class,EpistemicClass,"epistemic_class")); object.__setattr__(self,"jurisdiction",_enum(self.jurisdiction,SemanticJurisdiction,"jurisdiction")); object.__setattr__(self,"authority_state",_enum(self.authority_state,SemanticAuthorityState,"authority_state")); object.__setattr__(self,"currentness_state",_enum(self.currentness_state,CurrentnessState,"currentness_state")); object.__setattr__(self,"candidate_kind",_enum(self.candidate_kind,CandidateKind,"candidate_kind"))
        names=("carrier_locator_ref","carrier_row_ref","source_family_ref","source_release_ref","source_question_ref","implementation_ref_or_exact_na","authority_snapshot_ref","response_category_semantics_ref","routing_applicability_ref","structural_use_ceiling_ref","semantic_core_ref","semantic_schema_ref","negative_ceiling_ref","type_class_ceiling_ref")
        for n in names: object.__setattr__(self,n,exact_ref(getattr(self,n),n))
        if self.currentness_ref is not None: object.__setattr__(self,"currentness_ref",exact_ref(self.currentness_ref))
        if self.noncurrent_disposition_ref is not None: object.__setattr__(self,"noncurrent_disposition_ref",exact_ref(self.noncurrent_disposition_ref))
        if not self.evidence_admission_refs or not self.provenance_refs: raise FixtureSchemaError("evidence_admission_refs and provenance_refs must be nonempty")
        object.__setattr__(self,"evidence_admission_refs",_uniq(exact_ref(r) for r in self.evidence_admission_refs)); object.__setattr__(self,"provenance_refs",_uniq(exact_ref(r) for r in self.provenance_refs)); object.__setattr__(self,"equivalence_authorities",tuple(sorted(self.equivalence_authorities,key=lambda x:x.relation_ref.key)))
    @property
    def positive_equivalence_refs(self): return tuple(x.relation_ref for x in self.equivalence_authorities if x.decision is EquivalenceDecision.AUTHORIZED)
    @property
    def equivalence_provenance_refs(self): return _uniq(r for x in self.equivalence_authorities for r in x.provenance_refs)

@dataclass(frozen=True,slots=True)
class CompiledT03SemanticIntake:
    carrier_kind:CarrierKind; authority_ref:AuthorityRef; epistemic_class:EpistemicClass; jurisdiction:SemanticJurisdiction; authority_state:SemanticAuthorityState; currentness_state:CurrentnessState
    response_category_semantics_ref:ExactRef; routing_applicability_ref:ExactRef; structural_use_ceiling_ref:ExactRef; positive_equivalence_refs:tuple[ExactRef,...]
    source_local_intake:SourceLocalIntakeRecord; semantic_candidate:SemanticCandidateRecord; status:CandidateStatusRecord; blocker:CandidateBlockerRecord|None=None
    @property
    def ref(self):
        m={"contract":PSC02_COMPILER_CONTRACT_ID,"carrier":self.carrier_kind.value,"authority":self.authority_ref.as_dict(),"epistemic":self.epistemic_class.value,"jurisdiction":self.jurisdiction.value,"state":self.authority_state.value,"currentness":self.currentness_state.value,"response":self.response_category_semantics_ref.as_dict(),"routing":self.routing_applicability_ref.as_dict(),"ceiling":self.structural_use_ceiling_ref.as_dict(),"positive_equivalence_refs":[r.as_dict() for r in self.positive_equivalence_refs],"source_local":self.source_local_intake.ref.as_dict(),"candidate":self.semantic_candidate.ref.as_dict(),"status":self.status.ref.as_dict(),"blocker":None if self.blocker is None else self.blocker.ref.as_dict(),"hold":FINAL_RELEASE_HOLD,"prev3":PREV3_BOUNDARY,"obl063":OBL063_BOUNDARY}
        return _ref("PSC02_COMPILED_T03_GOVERNED_SEMANTIC_INTAKE",self.semantic_candidate.logical_key,m)
@dataclass(frozen=True,slots=True)
class CompiledBatch:
    compiled:tuple[CompiledT03SemanticIntake,...]; reduction:SemanticReductionResult; final_release_hold:str=FINAL_RELEASE_HOLD

def _validate_currentness(x:GovernedSemanticCapitalRecord):
    if x.currentness_state in (CurrentnessState.MISSING,CurrentnessState.AMBIGUOUS) or x.currentness_ref is None: raise CurrentnessBlockedError("missing or ambiguous governed currentness")
    if x.currentness_state is CurrentnessState.CURRENT:
        if x.authority_state is SemanticAuthorityState.SUPERSEDED or x.noncurrent_disposition_ref is not None: raise CurrentnessBlockedError("contradictory CURRENT/SUPERSEDED currentness")
    elif x.noncurrent_disposition_ref is None: raise CurrentnessBlockedError("HISTORICAL_NONCURRENT requires exact noncurrent disposition")

def _source_universe(x): return _ref("PSC02_SOURCE_UNIVERSE_IDENTITY",f"{x.source_family_ref.object_id}:{x.source_release_ref.object_id}",{"family":x.source_family_ref.as_dict(),"release":x.source_release_ref.as_dict()})
def _source_item(x): return _ref("PSC02_SOURCE_QUESTION_IMPLEMENTATION_IDENTITY",f"{x.source_question_ref.object_id}:{x.implementation_ref_or_exact_na.object_id}",{"question":x.source_question_ref.as_dict(),"implementation":x.implementation_ref_or_exact_na.as_dict()})
def _state_ref(x): return _ref("PSC02_DECLARED_GOVERNED_SEMANTIC_STATE",x.carrier_row_ref.object_id,{"state":x.authority_state.value,"currentness":x.currentness_state.value,"currentness_ref":x.currentness_ref.as_dict() if x.currentness_ref else None,"epistemic":x.epistemic_class.value,"jurisdiction":x.jurisdiction.value,"authority":x.authority_ref.as_dict(),"snapshot":x.authority_snapshot_ref.as_dict()})
def _claim_ref(x): return _ref("PSC02_GOVERNED_SEMANTIC_CAPITAL_CLAIM",x.carrier_row_ref.object_id,{"snapshot":x.authority_snapshot_ref.as_dict(),"family":x.source_family_ref.as_dict(),"release":x.source_release_ref.as_dict(),"question":x.source_question_ref.as_dict(),"implementation":x.implementation_ref_or_exact_na.as_dict(),"core":x.semantic_core_ref.as_dict(),"schema":x.semantic_schema_ref.as_dict(),"response":x.response_category_semantics_ref.as_dict(),"routing":x.routing_applicability_ref.as_dict(),"ceiling":x.structural_use_ceiling_ref.as_dict(),"negative_ceiling":x.negative_ceiling_ref.as_dict(),"type_ceiling":x.type_class_ceiling_ref.as_dict(),"state":x.authority_state.value,"currentness":x.currentness_state.value,"jurisdiction":x.jurisdiction.value,"epistemic":x.epistemic_class.value})
def _replay_ref(x): return _ref("PSC02_COMPILER_REPLAY_BASIS",x.carrier_row_ref.object_id,{"contract":PSC02_COMPILER_CONTRACT_ID,"carrier":x.carrier_kind.value,"locator":x.carrier_locator_ref.as_dict(),"row":x.carrier_row_ref.as_dict(),"authority":x.authority_ref.as_dict(),"snapshot":x.authority_snapshot_ref.as_dict(),"currentness":x.currentness_ref.as_dict() if x.currentness_ref else None,"core":x.semantic_core_ref.as_dict(),"schema":x.semantic_schema_ref.as_dict(),"negative_ceiling":x.negative_ceiling_ref.as_dict(),"type_ceiling":x.type_class_ceiling_ref.as_dict()})
def _candidate_id(x): return semantic_hash({"family":x.source_family_ref.as_dict(),"release":x.source_release_ref.as_dict(),"question":x.source_question_ref.as_dict(),"implementation":x.implementation_ref_or_exact_na.as_dict(),"authority":x.authority_ref.as_dict(),"row":x.carrier_row_ref.as_dict()})

def compile_governed_semantic_capital(x:GovernedSemanticCapitalRecord)->CompiledT03SemanticIntake:
    if not isinstance(x,GovernedSemanticCapitalRecord): raise GovernedSemanticCompilerError("record must be GovernedSemanticCapitalRecord")
    _validate_currentness(x)
    direct=(x.carrier_locator_ref,x.carrier_row_ref,x.authority_snapshot_ref,_auth_ref(x.authority_ref),x.source_family_ref,x.source_release_ref,x.source_question_ref,x.implementation_ref_or_exact_na,x.response_category_semantics_ref,x.routing_applicability_ref,x.structural_use_ceiling_ref,x.semantic_core_ref,x.semantic_schema_ref,x.negative_ceiling_ref,x.type_class_ceiling_ref,x.currentness_ref,x.noncurrent_disposition_ref)
    provenance=_uniq(r for r in (*x.provenance_refs,*direct,*x.equivalence_provenance_refs) if r is not None)
    evidence=_uniq((*x.evidence_admission_refs,x.authority_snapshot_ref,*x.positive_equivalence_refs))
    state=_state_ref(x)
    source=SourceLocalIntakeRecord(_source_universe(x),_source_item(x),state,x.routing_applicability_ref,(_claim_ref(x),x.response_category_semantics_ref,x.structural_use_ceiling_ref),state,provenance,_replay_ref(x))
    candidate=SemanticCandidateRecord("PSC02_GOVERNED_SEMANTIC_CAPITAL",_candidate_id(x),0,None,x.candidate_kind,x.semantic_core_ref,x.semantic_schema_ref,evidence,x.negative_ceiling_ref,x.type_class_ceiling_ref,CandidateStage.CLAIM_NORMALIZED,_uniq((*provenance,source.ref)))
    basis=_uniq((x.authority_snapshot_ref,x.currentness_ref,state,source.ref))
    blocker=None
    if x.authority_state in (SemanticAuthorityState.BLOCKED,SemanticAuthorityState.REVIEW_REQUIRED):
        blocker=CandidateBlockerRecord(candidate.ref,BlockerClass.AUTHORITY,"governed_semantic_capital.authority_state",f"upstream state must be resolved before downstream routing: {x.authority_state.value}",basis,"EXACT_UPSTREAM_GOVERNED_AUTHORITY_RESOLUTION_REQUIRED")
        status=CandidateStatusRecord(candidate.ref,CandidateOutcome.BLOCKED,basis,blocker_refs=(blocker.ref,),current_selection_refs=(x.currentness_ref,))
    elif x.authority_state is SemanticAuthorityState.SUPERSEDED or x.currentness_state is CurrentnessState.HISTORICAL_NONCURRENT:
        status=CandidateStatusRecord(candidate.ref,CandidateOutcome.HISTORICAL_NONCURRENT,basis,current_selection_refs=(x.currentness_ref,),noncurrent_disposition_refs=(x.noncurrent_disposition_ref,))
    else: status=CandidateStatusRecord(candidate.ref,CandidateOutcome.CANDIDATE_ONLY,basis,current_selection_refs=(x.currentness_ref,))
    return CompiledT03SemanticIntake(x.carrier_kind,x.authority_ref,x.epistemic_class,x.jurisdiction,x.authority_state,x.currentness_state,x.response_category_semantics_ref,x.routing_applicability_ref,x.structural_use_ceiling_ref,x.positive_equivalence_refs,source,candidate,status,blocker)

def compile_governed_semantic_batch(records:Iterable[GovernedSemanticCapitalRecord])->CompiledBatch:
    c=tuple(compile_governed_semantic_capital(x) for x in records); return CompiledBatch(c,reduce_semantic_candidates(x.semantic_candidate for x in c))

_FIELDS=frozenset("carrier_locator_ref carrier_row_ref source_family_ref source_release_ref source_question_ref implementation_ref_or_exact_na authority_ref authority_snapshot_ref epistemic_class jurisdiction authority_state currentness_state currentness_ref noncurrent_disposition_ref response_category_semantics_ref routing_applicability_ref structural_use_ceiling_ref semantic_core_ref semantic_schema_ref negative_ceiling_ref type_class_ceiling_ref evidence_admission_refs provenance_refs equivalence_authorities candidate_kind".split())
def _peq(v):
    e={"relation_ref","decision","decision_ref","authority_ref"}
    if set(v)!=e: raise FixtureSchemaError(f"equivalence fixture fields mismatch; missing={sorted(e-set(v))}, extra={sorted(set(v)-e)}")
    return EquivalenceAuthority(exact_ref(v["relation_ref"]),_enum(v["decision"],EquivalenceDecision,"equivalence decision"),exact_ref(v["decision_ref"]),authority_ref(v["authority_ref"]))
def _adapt(m:Mapping[str,Any],k:CarrierKind):
    if not isinstance(m,Mapping) or set(m)!=_FIELDS: raise FixtureSchemaError(f"fixture fields mismatch; missing={sorted(_FIELDS-set(m) if isinstance(m,Mapping) else _FIELDS)}, extra={sorted(set(m)-_FIELDS) if isinstance(m,Mapping) else []}")
    er=lambda n: exact_ref(m[n],n)
    return GovernedSemanticCapitalRecord(k,er("carrier_locator_ref"),er("carrier_row_ref"),er("source_family_ref"),er("source_release_ref"),er("source_question_ref"),er("implementation_ref_or_exact_na"),authority_ref(m["authority_ref"]),er("authority_snapshot_ref"),_enum(m["epistemic_class"],EpistemicClass,"epistemic_class"),_enum(m["jurisdiction"],SemanticJurisdiction,"jurisdiction"),_enum(m["authority_state"],SemanticAuthorityState,"authority_state"),_enum(m["currentness_state"],CurrentnessState,"currentness_state"),None if m["currentness_ref"] is None else er("currentness_ref"),None if m["noncurrent_disposition_ref"] is None else er("noncurrent_disposition_ref"),er("response_category_semantics_ref"),er("routing_applicability_ref"),er("structural_use_ceiling_ref"),er("semantic_core_ref"),er("semantic_schema_ref"),er("negative_ceiling_ref"),er("type_class_ceiling_ref"),tuple(exact_ref(r) for r in m["evidence_admission_refs"]),tuple(exact_ref(r) for r in m["provenance_refs"]),tuple(_peq(v) for v in m["equivalence_authorities"]),_enum(m["candidate_kind"],CandidateKind,"candidate_kind"))
def adapt_fqra_fixture(m): return _adapt(m,CarrierKind.FQRA)
def adapt_qsmv2_fixture(m): return _adapt(m,CarrierKind.QSMV2)
def adapt_negative_block_fixture(m): return _adapt(m,CarrierKind.NEGATIVE_BLOCK)
def adapt_response_semantics_fixture(m): return _adapt(m,CarrierKind.RESPONSE_SEMANTICS)
def adapt_typed_relation_fixture(m): return _adapt(m,CarrierKind.TYPED_RELATION)
