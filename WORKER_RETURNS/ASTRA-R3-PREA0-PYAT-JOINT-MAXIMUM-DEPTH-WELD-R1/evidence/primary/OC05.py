"""W2-D07 finite objective-consumer bounded-evidence policy binding.

Only current OC01/OC02 seams are executable here. OC03/OC04/OC05 remain typed
NOT_YET_APPLICABLE until their competent owner paths materialize real consumers.
"""
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import hashlib, json, re
from typing import Any, Mapping, Sequence

CONTRACT_ID="PREV3_OBJECTIVE_CONSUMER_BOUNDED_EVIDENCE@1.0.0"
C08_POLICY_COMMIT="1d1faccd176ddc7b7c88edc05fc4dc374ffbf4dd"
C08_POLICY_BLOB="e3736b720fe8893c750443522f2aa61e36e5da3b"
HQ_ADOPTION_BLOB="8a5741e8f7d698f9f98e7b23df66751a7cbfab6a"
OC01="OC01_PRE553_SOURCE_LOCAL_EMPIRICAL_QUERY_R1"
OC02="OC02_LEARNED_STRUCTURAL_ADMISSION_R1"
OC03="OC03_SDTF_OBJECTIVE_CONSEQUENCE_R1"
OC04="OC04_OCCURRENCE_NONEVENT_WORLD_FACT_R1"
OC05="OC05_TERMINAL_OBJECTIVE_WORLD_RESOLUTION_R1"

class PolicyError(ValueError): pass
class NotYetApplicableConsumer(PolicyError): pass
class MissingAsValueError(PolicyError): pass
class RelationAuthorityRequired(PolicyError): pass
class NonEmpiricalAuthorityRequired(PolicyError): pass
class RenormalizationForbidden(PolicyError): pass

class ClaimCeiling(str,Enum):
    POPULATION_STATISTIC="POPULATION_STATISTIC"
    SOURCE_LOCAL_STATISTIC="SOURCE_LOCAL_STATISTIC"
    SUPPORTED_COMPONENT_ONLY="SUPPORTED_COMPONENT_ONLY"
    OBJECTIVE_FACT="OBJECTIVE_FACT"
    STRUCTURAL_RELATION="STRUCTURAL_RELATION"
class EvidenceKind(str,Enum):
    EMPIRICAL="EMPIRICAL"; NON_EMPIRICAL_MODEL="NON_EMPIRICAL_MODEL"
class EvidenceTier(str,Enum):
    POPULATION_CERTIFIED="POPULATION_CERTIFIED"
    SOURCE_LOCAL_CERTIFIED="SOURCE_LOCAL_CERTIFIED"
    PARTIAL_AUTHORITY="PARTIAL_AUTHORITY"
    UNAVAILABLE="UNAVAILABLE"
class DecisionState(str,Enum):
    SUPPORTED_OBJECTIVE_RESULT="SUPPORTED_OBJECTIVE_RESULT"
    PARTIAL_OBJECTIVE_RESULT="PARTIAL_OBJECTIVE_RESULT"
    REFUSED_REQUIRED_OBJECTIVE_EVIDENCE="REFUSED_REQUIRED_OBJECTIVE_EVIDENCE"
    ALL_UNAVAILABLE__NOT_POSITIVE_COMPLETION="ALL_UNAVAILABLE__NOT_POSITIVE_COMPLETION"

def _text(v,n):
    if not isinstance(v,str) or not v.strip(): raise PolicyError(f"{n} must be non-empty text")
    return v.strip()
def _hash(v): return hashlib.sha256(json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

@dataclass(frozen=True,order=True)
class ExactRef:
    kind:str; object_id:str; content_hash:str
    def __post_init__(self):
        object.__setattr__(self,"kind",_text(self.kind,"kind")); object.__setattr__(self,"object_id",_text(self.object_id,"object_id"))
        if not re.fullmatch(r"[0-9a-f]{64}",self.content_hash): raise PolicyError("content_hash must be sha256")
    def as_dict(self): return {"kind":self.kind,"object_id":self.object_id,"content_hash":self.content_hash}

@dataclass(frozen=True)
class ConsumerBinding:
    policy_id:str; state:str; seam:str|None; reason:str
    @property
    def applicable(self): return self.state=="APPLICABLE_CURRENT"

POLICY_BINDINGS:Mapping[str,ConsumerBinding]={
 OC01:ConsumerBinding(OC01,"APPLICABLE_CURRENT","rawlsing_next.pre553_empirical_query.execute_empirical_query","current exact source-local empirical query/statistic seam"),
 OC02:ConsumerBinding(OC02,"APPLICABLE_CURRENT","rawlsing_next.pre553_structural_admission","current P06/I04 structural-admission decision/refusal seam"),
 OC03:ConsumerBinding(OC03,"NOT_YET_APPLICABLE",None,"P1-P5 remain CANDIDATE_NOT_CURRENT pending W2-D04 and later admission"),
 OC04:ConsumerBinding(OC04,"NOT_YET_APPLICABLE",None,"generic non-event adapter is W2-D05; real world rooting is W2-D01"),
 OC05:ConsumerBinding(OC05,"NOT_YET_APPLICABLE",None,"terminal objective-world root/resolver is not current; no universal terminal may be invented"),
}

@dataclass(frozen=True)
class PolicyInput:
    input_id:str; required:bool; available:bool; evidence_kind:EvidenceKind; evidence_tier:EvidenceTier; claim_ceiling:ClaimCeiling
    producer_ref:ExactRef|None=None; authority_refs:tuple[ExactRef,...]=(); substitution:bool=False; relation_authority_ref:ExactRef|None=None
    model_prior_version:str|None=None; model_prior_authority_ref:ExactRef|None=None; omission_reason:str|None=None
    def __post_init__(self):
        object.__setattr__(self,"input_id",_text(self.input_id,"input_id")); object.__setattr__(self,"authority_refs",tuple(sorted(set(self.authority_refs))))
        if not self.available:
            if self.evidence_tier is not EvidenceTier.UNAVAILABLE or self.producer_ref is not None or self.authority_refs or not self.omission_reason:
                raise MissingAsValueError("unavailable evidence must be typed and carry no positive producer/authority value")
        elif self.evidence_tier is EvidenceTier.UNAVAILABLE or self.producer_ref is None or not self.authority_refs:
            raise PolicyError("available evidence requires non-UNAVAILABLE tier plus exact producer/authority refs")
        if self.substitution and self.relation_authority_ref is None: raise RelationAuthorityRequired("alternate/backfill requires exact relation authority")
        if self.evidence_kind is EvidenceKind.NON_EMPIRICAL_MODEL:
            if not self.model_prior_version or self.model_prior_authority_ref is None: raise NonEmpiricalAuthorityRequired("model prior requires explicit version and separate authority")
        elif self.model_prior_version is not None or self.model_prior_authority_ref is not None:
            raise NonEmpiricalAuthorityRequired("model-prior metadata requires NON_EMPIRICAL_MODEL typing")

@dataclass(frozen=True)
class Receipt:
    policy_id:str; consumer_seam:str; operation_id:str; state:DecisionState; requested_claim_ceiling:ClaimCeiling
    selected_input_ids:tuple[str,...]; selected_producer_refs:tuple[ExactRef,...]; missing_required_input_ids:tuple[str,...]
    omitted_optional_input_ids:tuple[str,...]; non_empirical_input_ids:tuple[str,...]; refusal_reasons:tuple[str,...]
    relation_authority_refs:tuple[ExactRef,...]; selected_input_authority_refs:tuple[tuple[str,tuple[ExactRef,...]],...]
    unavailable_input_omission_reasons:tuple[tuple[str,str],...]; coefficient_reallocated:bool; positive_completion:bool; receipt_hash:str
    def as_dict(self):
        def refs(xs): return [x.as_dict() for x in xs]
        return {"contract_id":CONTRACT_ID,"policy_id":self.policy_id,"consumer_seam":self.consumer_seam,"operation_id":self.operation_id,"state":self.state.value,
          "requested_claim_ceiling":self.requested_claim_ceiling.value,"selected_input_ids":list(self.selected_input_ids),"selected_producer_refs":refs(self.selected_producer_refs),
          "missing_required_input_ids":list(self.missing_required_input_ids),"omitted_optional_input_ids":list(self.omitted_optional_input_ids),"non_empirical_input_ids":list(self.non_empirical_input_ids),
          "refusal_reasons":list(self.refusal_reasons),"relation_authority_refs":refs(self.relation_authority_refs),
          "selected_input_authority_refs":[{"input_id":input_id,"authority_refs":refs(authority_refs)} for input_id,authority_refs in self.selected_input_authority_refs],
          "unavailable_input_omission_reasons":[{"input_id":input_id,"omission_reason":reason} for input_id,reason in self.unavailable_input_omission_reasons],
          "coefficient_reallocated":False,"positive_completion":self.positive_completion,"receipt_hash":self.receipt_hash}

def _satisfies(x:PolicyInput,c:ClaimCeiling)->bool:
    if x.evidence_kind is EvidenceKind.NON_EMPIRICAL_MODEL:return False
    if c is ClaimCeiling.POPULATION_STATISTIC:return x.evidence_tier is EvidenceTier.POPULATION_CERTIFIED and x.claim_ceiling is ClaimCeiling.POPULATION_STATISTIC
    if c is ClaimCeiling.SOURCE_LOCAL_STATISTIC:return x.evidence_tier in {EvidenceTier.POPULATION_CERTIFIED,EvidenceTier.SOURCE_LOCAL_CERTIFIED} and x.claim_ceiling in {ClaimCeiling.POPULATION_STATISTIC,ClaimCeiling.SOURCE_LOCAL_STATISTIC}
    if c is ClaimCeiling.STRUCTURAL_RELATION:return x.claim_ceiling is ClaimCeiling.STRUCTURAL_RELATION and x.evidence_tier is not EvidenceTier.UNAVAILABLE
    if c is ClaimCeiling.OBJECTIVE_FACT:return x.claim_ceiling is ClaimCeiling.OBJECTIVE_FACT and x.evidence_tier is not EvidenceTier.UNAVAILABLE
    return x.evidence_tier is not EvidenceTier.UNAVAILABLE

def evaluate_current_consumer(*,policy_id:str,operation_id:str,inputs:Sequence[PolicyInput],requested_claim_ceiling:ClaimCeiling,partial_allowed:bool,renormalization_requested:bool=False)->Receipt:
    b=POLICY_BINDINGS.get(policy_id)
    if b is None: raise PolicyError(f"unknown policy {policy_id}")
    if not b.applicable or b.seam is None: raise NotYetApplicableConsumer(f"{policy_id}: {b.state}: {b.reason}")
    if renormalization_requested: raise RenormalizationForbidden("no coefficient/confidence/semantic-scope renormalization")
    items=tuple(sorted(inputs,key=lambda x:x.input_id)); _text(operation_id,"operation_id")
    if not items or len({x.input_id for x in items})!=len(items): raise PolicyError("finite unique input manifest required")
    missing=tuple(x.input_id for x in items if x.required and not x.available); omitted=tuple(x.input_id for x in items if not x.required and not x.available)
    omission_reasons=tuple((x.input_id,x.omission_reason) for x in items if not x.available and x.omission_reason is not None)
    nonemp=tuple(x.input_id for x in items if x.available and x.evidence_kind is EvidenceKind.NON_EMPIRICAL_MODEL)
    empirical=tuple(x for x in items if x.available and x.evidence_kind is EvidenceKind.EMPIRICAL); selected=tuple(x for x in empirical if _satisfies(x,requested_claim_ceiling))
    refusal=[]
    if missing: refusal.append("MISSING_REQUIRED_OBJECTIVE_EVIDENCE:"+",".join(missing))
    under=tuple(x.input_id for x in items if x.required and x.available and x.evidence_kind is EvidenceKind.EMPIRICAL and not _satisfies(x,requested_claim_ceiling))
    if under: refusal.append("CLAIM_CEILING_NOT_AUTHORIZED:"+",".join(under))
    if not empirical: state=DecisionState.ALL_UNAVAILABLE__NOT_POSITIVE_COMPLETION; refusal.append("NO_EMPIRICAL_OBJECTIVE_EVIDENCE_AVAILABLE"); positive=False
    elif refusal: state=DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE; positive=False
    elif omitted and partial_allowed: state=DecisionState.PARTIAL_OBJECTIVE_RESULT; positive=True
    elif omitted: state=DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE; refusal.append("OPTIONAL_LOSS_NOT_ALLOWED_FOR_THIS_OPERATION"); positive=False
    else: state=DecisionState.SUPPORTED_OBJECTIVE_RESULT; positive=True
    if positive and not selected: state=DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE; refusal.append("NO_SELECTED_EMPIRICAL_INPUT_SATISFIES_REQUESTED_CLAIM"); positive=False
    selected_refs=tuple(sorted(x.producer_ref for x in selected if x.producer_ref)); relation_refs=tuple(sorted(x.relation_authority_ref for x in items if x.relation_authority_ref))
    selected_authority_refs=tuple((x.input_id,x.authority_refs) for x in selected)
    core={"contract_id":CONTRACT_ID,"policy_id":policy_id,"consumer_seam":b.seam,"operation_id":operation_id,"state":state.value,"requested_claim_ceiling":requested_claim_ceiling.value,
      "selected_input_ids":[x.input_id for x in selected],"selected_producer_refs":[x.as_dict() for x in selected_refs],"missing_required_input_ids":list(missing),"omitted_optional_input_ids":list(omitted),"non_empirical_input_ids":list(nonemp),
      "refusal_reasons":refusal,"relation_authority_refs":[x.as_dict() for x in relation_refs],
      "selected_input_authority_refs":[{"input_id":input_id,"authority_refs":[ref.as_dict() for ref in authority_refs]} for input_id,authority_refs in selected_authority_refs],
      "unavailable_input_omission_reasons":[{"input_id":input_id,"omission_reason":reason} for input_id,reason in omission_reasons],
      "coefficient_reallocated":False,"positive_completion":positive,
      "authority_basis":{"c08_policy_commit":C08_POLICY_COMMIT,"c08_policy_blob":C08_POLICY_BLOB,"hq_adoption_blob":HQ_ADOPTION_BLOB}}
    return Receipt(policy_id,b.seam,operation_id,state,requested_claim_ceiling,tuple(x.input_id for x in selected),selected_refs,missing,omitted,nonemp,tuple(refusal),relation_refs,selected_authority_refs,omission_reasons,False,positive,_hash(core))

def evaluate_oc01_pre553_source_local(*,operation_id,inputs,requested_claim_ceiling,partial_allowed=True,renormalization_requested=False):
    return evaluate_current_consumer(policy_id=OC01,operation_id=operation_id,inputs=inputs,requested_claim_ceiling=requested_claim_ceiling,partial_allowed=partial_allowed,renormalization_requested=renormalization_requested)
def evaluate_oc02_structural_admission(*,operation_id,inputs,partial_allowed=False,renormalization_requested=False):
    return evaluate_current_consumer(policy_id=OC02,operation_id=operation_id,inputs=inputs,requested_claim_ceiling=ClaimCeiling.STRUCTURAL_RELATION,partial_allowed=partial_allowed,renormalization_requested=renormalization_requested)
def installation_manifest():
    return tuple({"policy_id":b.policy_id,"current_applicability":b.state,"consumer_seam":b.seam,"reason":b.reason} for b in (POLICY_BINDINGS[k] for k in (OC01,OC02,OC03,OC04,OC05)))
