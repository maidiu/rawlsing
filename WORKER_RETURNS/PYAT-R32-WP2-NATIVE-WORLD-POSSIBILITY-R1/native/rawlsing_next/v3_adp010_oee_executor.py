"""Bounded ADP-010 OEE executor for the synthetic governed S3 court.

Consumes an already-owned exact subject ref. Implements only deterministic
BASIS->AVAILABLE->OPPORTUNITY->ENCOUNTER. It never creates/classifies subjects,
infers contact from co-location, creates exposure, mutates actor state, or
invokes comparator/PSEPF/metabolism/CAN-008 semantics.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import datetime, timezone
from hashlib import sha256
import json
import re
import unicodedata
from typing import Any, Iterable, Mapping, Sequence

ADP010_AUTHORITY_ID = "V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE"
ADP010_AUTHORITY_VERSION = "1.0.0"
ADP010_REGISTRY_ID = "V3_OEE_REALIZATION_RULE_REGISTRY"
ADP010_REGISTRY_VERSION = "1.0.0"
ADP010_AUTHORITY_ARTIFACT_PATH = "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W1_CRITICAL_AUTHORITY_EXPANSION/ADP_010_V3_ENCOUNTER_EXPOSURE/AUTHORITY.json"
ADP010_AUTHORITY_ARTIFACT_BLOB_SHA = "0eac41d081b112255dcfc6dd42a6afab15a2928b"
ADP008_AUTHORITY_ID = "V3_DEVELOPMENTAL_PHASE_RULE"
ADP008_AUTHORITY_VERSION = "1.1.0"
ADP008_AUTHORITY_ARTIFACT_PATH = "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W0_AUTHORITY_FOUNDATION/ADP_008_V3_DEVELOPMENTAL_PHASE/AUTHORITY.json"
ADP008_AUTHORITY_ARTIFACT_BLOB_SHA = "c6564c5c2793e9ed86ec0c5cecbcf84ff6f427d6"
ADP020_AUTHORITY_ID = "ADP-020"
ADP020_AUTHORITY_VERSION = "1.0.0"
ADP020_AUTHORITY_ARTIFACT_PATH = "data/ddm_build_copy/vozhd_dva/20260817_downstream_completion/schematics/release/W0_AUTHORITY_FOUNDATION/ADP_020_V3_CAUSAL_RNG/AUTHORITY.json"
ADP020_AUTHORITY_ARTIFACT_BLOB_SHA = "1f13dc7ccc69bda562613d6215acc996a9c092e4"
DEVELOPMENT_ACTIVE_PHASE = "V3DP_DEVELOPMENT_ACTIVE"
STATE_AVAILABLE, STATE_OPPORTUNITY, STATE_ENCOUNTER = "AVAILABLE", "OPPORTUNITY", "ENCOUNTER"
RULE_AVAILABLE = "OEE_CORE_AVAILABLE_BASIS_V1"
RULE_OPPORTUNITY = "OEE_CORE_OPPORTUNITY_FROM_EXPLICIT_BASIS_V1"
RULE_ENCOUNTER = "OEE_CORE_ENCOUNTER_FROM_EXPLICIT_CONTACT_WITNESS_V1"
RULE_VERSION = "V1"  # accepted core-v1 identity is embedded in each exact rule id
EFFECT_OPPORTUNITY, EFFECT_ENCOUNTER = "OEE_OPPORTUNITY_ESTABLISHED", "OEE_ENCOUNTER_OCCURRED"
CONTACT_WITNESS_KIND = "CONTACT_OCCURRENCE_WITNESS"
CONTACT_INDEPENDENCE_KIND = "CONTACT_WITNESS_INDEPENDENCE"
CONTACT_OCCURRENCE_SEMANTIC = "CONTACT_OCCURRENCE"
EP_GENERATED_RUNTIME_FACT = "GENERATED_RUNTIME_FACT"
EP_RESOLVER_CONTEXT = "RESOLVER_DERIVED_CONTEXT"
EP_ADMITTED_CAUSAL_EVENT = "ADMITTED_CAUSAL_EVENT"
_ADMISSIBLE_EP = {EP_GENERATED_RUNTIME_FACT, EP_RESOLVER_CONTEXT, EP_ADMITTED_CAUSAL_EVENT}
_INSUFFICIENT_CONTACT = {"COLOCATION","CO_LOCATION","COPRESENCE","CO_PRESENCE","SAME_GEOGRAPHY_TIME","SHARED_V555_ENDPOINT","SAME_STRUCTURAL_TARGET","SAME_INSTITUTION_CATEGORY","SIMULTANEOUS_RESOLVER_SELECTION","NARRATIVE_PLAUSIBILITY"}
_HASH64 = re.compile(r"^[0-9a-f]{64}$")
_BLOB40 = re.compile(r"^[0-9a-f]{40}$")
_RECORD_DOMAIN = "RAWLSING\0ADP-010\0V3_OEE_REALIZATION_RECORD_V1\0"
_CANDIDATE_DOMAIN = "RAWLSING\0ADP-010\0OEE_CANDIDATE_V1\0"
_EVENT_DOMAIN = "RAWLSING\0ADP-010\0OEE_EVENT_V1\0"

class OEEAdmissionError(ValueError): pass
class OEEIntegrityError(OEEAdmissionError): pass

@dataclass(frozen=True, slots=True)
class ExactRef:
    kind: str
    ref: str
    content_hash: str

@dataclass(frozen=True, slots=True)
class SubjectIngressEvidence:
    subject_ref: str
    semantic_owner_authority_id: str
    semantic_owner_authority_version: str
    semantic_owner_authority_content_hash: str
    semantic_object_hash: str
    materialization_receipt: ExactRef
    epistemic_class: str
    causal_use_permission: ExactRef
    provenance_refs: tuple[ExactRef, ...]

@dataclass(frozen=True, slots=True)
class ActorPhaseEvidence:
    actor_id: str
    phase_state_ref: ExactRef
    phase_authority_id: str = ADP008_AUTHORITY_ID
    phase_authority_version: str = ADP008_AUTHORITY_VERSION
    phase_authority_artifact_blob_sha: str = ADP008_AUTHORITY_ARTIFACT_BLOB_SHA
    base_phase_id: str = DEVELOPMENT_ACTIVE_PHASE
    provenance_refs: tuple[ExactRef, ...] = ()

@dataclass(frozen=True, slots=True)
class PositiveApplicabilityReceipt:
    receipt: ExactRef
    authority_id: str
    authority_version: str
    authority_content_hash: str
    result: str
    provenance_refs: tuple[ExactRef, ...]

@dataclass(frozen=True, slots=True)
class OpportunityBasisEvidence:
    basis_ref: ExactRef
    actor_id: str
    subject_ref: str
    applicability_receipts: tuple[PositiveApplicabilityReceipt, ...]
    context_or_world_receipt_refs: tuple[ExactRef, ...]
    position_or_other_constraint_refs: tuple[ExactRef, ...] = ()
    provenance_refs: tuple[ExactRef, ...] = ()

@dataclass(frozen=True, slots=True)
class ContactOccurrenceWitness:
    witness_ref: ExactRef
    witness_authority_id: str
    witness_authority_version: str
    witness_authority_content_hash: str
    actor_id: str
    subject_ref: str
    occurrence_time: str
    semantic: str
    independence_ref: ExactRef
    provenance_refs: tuple[ExactRef, ...]

@dataclass(frozen=True, slots=True)
class V3OEERealizationRecord:
    record_id: str; actor_id: str; authority_id: str; authority_version: str
    registry_id: str; registry_version: str; rule_id: str; rule_version: str
    realization_state: str; subject_ref: str; parent_record_id: str | None
    effective_from: str; effective_until: str; time_granularity: str
    source_candidate_id: str; source_candidate_replay_hash: str
    context_or_world_receipt_refs: tuple[ExactRef, ...]
    applicability_receipt_refs: tuple[ExactRef, ...]
    phase_state_ref: ExactRef
    position_or_other_constraint_refs: tuple[ExactRef, ...]
    causal_witness_refs: tuple[ExactRef, ...]
    rng_decision_receipt_ref: ExactRef | None
    event_id: str | None; event_effect_kind: str | None
    prior_ledger_anchor_ref: ExactRef
    provenance_refs: tuple[ExactRef, ...]
    record_hash: str

@dataclass(frozen=True, slots=True)
class OEEExecutionResult:
    record: V3OEERealizationRecord

_RULES = {
    STATE_AVAILABLE: (RULE_AVAILABLE, "BASIS_TO_AVAILABLE", None, None),
    STATE_OPPORTUNITY: (RULE_OPPORTUNITY, "AVAILABLE_TO_OPPORTUNITY", STATE_AVAILABLE, EFFECT_OPPORTUNITY),
    STATE_ENCOUNTER: (RULE_ENCOUNTER, "OPPORTUNITY_TO_ENCOUNTER", STATE_OPPORTUNITY, EFFECT_ENCOUNTER),
}

def _s(v: Any, n: str) -> str:
    if not isinstance(v, str) or not unicodedata.normalize("NFC", v.strip()): raise OEEIntegrityError(f"{n} must be non-empty string")
    return unicodedata.normalize("NFC", v.strip())
def _h(v: Any, n: str) -> str:
    v=_s(v,n)
    if not _HASH64.fullmatch(v): raise OEEIntegrityError(f"{n} must be lowercase SHA-256 hex")
    return v
def _ref(v: Any, n: str) -> ExactRef:
    if not isinstance(v, ExactRef): raise OEEIntegrityError(f"{n} must be ExactRef")
    _s(v.kind,n+".kind"); _s(v.ref,n+".ref"); _h(v.content_hash,n+".content_hash"); return v
def _refs(xs: Iterable[ExactRef], n: str, required=False) -> tuple[ExactRef,...]:
    xs=tuple(xs)
    if required and not xs: raise OEEIntegrityError(f"{n} must be non-empty")
    d={(_ref(x,n).kind,_ref(x,n).ref,_ref(x,n).content_hash):x for x in xs}
    return tuple(d[k] for k in sorted(d))
def _merge(*groups: Iterable[ExactRef]) -> tuple[ExactRef,...]: return _refs((x for g in groups for x in g),"refs",True)
def _time(v: Any, n: str) -> str:
    raw=_s(v,n); p=raw[:-1]+"+00:00" if raw.endswith("Z") else raw
    try: dt=datetime.fromisoformat(p)
    except ValueError as e: raise OEEIntegrityError(f"{n} must be ISO-8601") from e
    if dt.tzinfo is None or dt.utcoffset() is None: raise OEEIntegrityError(f"{n} must be timezone-aware")
    return dt.astimezone(timezone.utc).isoformat(timespec="microseconds").replace("+00:00","Z")
def _norm(v: Any) -> Any:
    if isinstance(v,ExactRef): return {"kind":v.kind,"ref":v.ref,"content_hash":_h(v.content_hash,"content_hash")}
    if isinstance(v,Mapping): return {str(k):_norm(x) for k,x in v.items()}
    if isinstance(v,(tuple,list)): return [_norm(x) for x in v]
    return unicodedata.normalize("NFC",v) if isinstance(v,str) else v
def _digest(domain: str, v: Any) -> str: return sha256((domain+json.dumps(_norm(v),sort_keys=True,separators=(",",":"),ensure_ascii=False)).encode()).hexdigest()
def _dt(v: str): return datetime.fromisoformat(v[:-1]+"+00:00")
def _interval(a,b):
    a,b=_time(a,"effective_from"),_time(b,"effective_until")
    if _dt(b)<_dt(a): raise OEEIntegrityError("effective_until precedes effective_from")
    return a,b

def _subject(s: Any) -> SubjectIngressEvidence:
    if not isinstance(s,SubjectIngressEvidence): raise OEEIntegrityError("subject must be SubjectIngressEvidence")
    _s(s.subject_ref,"subject_ref"); _s(s.semantic_owner_authority_id,"semantic_owner_authority_id"); _s(s.semantic_owner_authority_version,"semantic_owner_authority_version")
    _h(s.semantic_owner_authority_content_hash,"semantic_owner_authority_content_hash"); _h(s.semantic_object_hash,"semantic_object_hash")
    _ref(s.materialization_receipt,"materialization_receipt"); _ref(s.causal_use_permission,"causal_use_permission"); _refs(s.provenance_refs,"subject.provenance_refs",True)
    if s.epistemic_class not in _ADMISSIBLE_EP: raise OEEAdmissionError("subject basis epistemic class is not ADP-010-admissible")
    return s

def _actor(a: Any) -> ActorPhaseEvidence:
    if not isinstance(a,ActorPhaseEvidence): raise OEEIntegrityError("actor must be ActorPhaseEvidence")
    _s(a.actor_id,"actor_id"); r=_ref(a.phase_state_ref,"phase_state_ref")
    if r.kind!="V3DevelopmentalPhaseState": raise OEEAdmissionError("phase_state_ref must be V3DevelopmentalPhaseState")
    if (a.phase_authority_id,a.phase_authority_version,a.phase_authority_artifact_blob_sha)!=(ADP008_AUTHORITY_ID,ADP008_AUTHORITY_VERSION,ADP008_AUTHORITY_ARTIFACT_BLOB_SHA): raise OEEAdmissionError("wrong ADP-008 authority binding")
    if not _BLOB40.fullmatch(a.phase_authority_artifact_blob_sha): raise OEEIntegrityError("phase authority blob malformed")
    if a.base_phase_id!=DEVELOPMENT_ACTIVE_PHASE: raise OEEAdmissionError("V3DP_DEVELOPMENT_ACTIVE is required")
    _refs(a.provenance_refs,"actor.provenance_refs",True); return a

def _parent(r: Any, state: str, actor: str, subject: str) -> V3OEERealizationRecord:
    r=validate_record(r)
    if r.realization_state!=state: raise OEEAdmissionError(f"expected {state} parent")
    if r.actor_id!=actor: raise OEEAdmissionError("parent actor continuity failure")
    if r.subject_ref!=subject: raise OEEAdmissionError("parent subject continuity failure")
    return r

def _within(a,b,p):
    if _dt(a)<_dt(p.effective_from) or _dt(b)>_dt(p.effective_until): raise OEEAdmissionError("child effective scope must remain within active parent scope")

def _candidate(state, actor, subject, parent, a,b,g,w,c,app,ctx):
    rid,transition,_,_=_RULES[state]
    material={"transition":transition,"actor":actor.actor_id,"subject":subject.subject_ref,"subject_owner":[subject.semantic_owner_authority_id,subject.semantic_owner_authority_version,subject.semantic_owner_authority_content_hash],"subject_object_hash":subject.semantic_object_hash,"materialization_receipt":subject.materialization_receipt,"causal_use_permission":subject.causal_use_permission,"parent":parent,"effective_scope":[a,b,g],"rule":[rid,RULE_VERSION,ADP010_REGISTRY_VERSION],"canonical_witnesses":w,"constraints":c,"applicability":app,"context":ctx}
    h=_digest(_CANDIDATE_DOMAIN,material); return f"urn:rawlsing:v3:oee:candidate:sha256:{h}",h

def _identity(r):
    return {"actor":r.actor_id,"authority":[r.authority_id,r.authority_version],"registry":[r.registry_id,r.registry_version],"rule":[r.rule_id,r.rule_version],"state":r.realization_state,"subject":r.subject_ref,"parent":r.parent_record_id,"effective_scope":[r.effective_from,r.effective_until,r.time_granularity],"canonical_witnesses":r.causal_witness_refs,"candidate_replay_hash":r.source_candidate_replay_hash,"rng_decision_receipt_ref":r.rng_decision_receipt_ref}

def _build(state, actor, subject, parent, a,b,g,cid,ch,ctx,app,constraints,w,prior,prov):
    rid,_,_,effect=_RULES[state]
    r=V3OEERealizationRecord("",actor.actor_id,ADP010_AUTHORITY_ID,ADP010_AUTHORITY_VERSION,ADP010_REGISTRY_ID,ADP010_REGISTRY_VERSION,rid,RULE_VERSION,state,subject.subject_ref,parent,a,b,g,cid,ch,ctx,app,actor.phase_state_ref,constraints,w,None,None,effect,prior,prov,"")
    rh=_digest(_RECORD_DOMAIN,_identity(r)); event=None if effect is None else f"urn:rawlsing:v3:oee:event:sha256:{_digest(_EVENT_DOMAIN,{'record_hash':rh,'effect':effect})}"
    return replace(r,record_id=f"urn:rawlsing:v3:oee:record:sha256:{rh}",event_id=event,record_hash=rh)

def validate_record(r: Any) -> V3OEERealizationRecord:
    if not isinstance(r,V3OEERealizationRecord): raise OEEIntegrityError("record must be V3OEERealizationRecord")
    if (r.authority_id,r.authority_version,r.registry_id,r.registry_version)!=(ADP010_AUTHORITY_ID,ADP010_AUTHORITY_VERSION,ADP010_REGISTRY_ID,ADP010_REGISTRY_VERSION): raise OEEIntegrityError("ADP-010 authority/registry mismatch")
    if r.realization_state not in _RULES: raise OEEIntegrityError("unsupported realization state")
    rid,_,_,effect=_RULES[r.realization_state]
    if (r.rule_id,r.rule_version)!=(rid,RULE_VERSION): raise OEEIntegrityError("rule identity mismatch")
    _h(r.source_candidate_replay_hash,"source_candidate_replay_hash"); _ref(r.phase_state_ref,"phase_state_ref"); _ref(r.prior_ledger_anchor_ref,"prior_ledger_anchor_ref")
    for n,xs in [("context",r.context_or_world_receipt_refs),("applicability",r.applicability_receipt_refs),("constraints",r.position_or_other_constraint_refs),("witnesses",r.causal_witness_refs),("provenance",r.provenance_refs)]: _refs(xs,n,n=="provenance")
    _interval(r.effective_from,r.effective_until); _s(r.time_granularity,"time_granularity")
    if r.rng_decision_receipt_ref is not None: raise OEEIntegrityError("ADP-010 core-v1 is ZERO_DRAW")
    rh=_digest(_RECORD_DOMAIN,_identity(r))
    if r.record_hash!=rh or r.record_id!=f"urn:rawlsing:v3:oee:record:sha256:{rh}": raise OEEIntegrityError("record identity/hash mismatch")
    event=None if effect is None else f"urn:rawlsing:v3:oee:event:sha256:{_digest(_EVENT_DOMAIN,{'record_hash':rh,'effect':effect})}"
    if (r.event_id,r.event_effect_kind)!=(event,effect): raise OEEIntegrityError("event identity/effect mismatch")
    return r

def admit_available(*,subject,actor,effective_from,effective_until,time_granularity,context_or_world_receipt_refs,prior_ledger_anchor_ref,provenance_refs):
    s,a=_subject(subject),_actor(actor); start,end=_interval(effective_from,effective_until); g=_s(time_granularity,"time_granularity"); ctx=_refs(context_or_world_receipt_refs,"context",True); prior=_ref(prior_ledger_anchor_ref,"prior_ledger_anchor_ref")
    w=_refs((s.materialization_receipt,s.causal_use_permission),"basis witnesses",True); prov=_merge(s.provenance_refs,a.provenance_refs,ctx,provenance_refs,(s.materialization_receipt,s.causal_use_permission,a.phase_state_ref,prior)); cid,ch=_candidate(STATE_AVAILABLE,a,s,None,start,end,g,w,(),(),ctx)
    return OEEExecutionResult(_build(STATE_AVAILABLE,a,s,None,start,end,g,cid,ch,ctx,(),(),w,prior,prov))

def admit_opportunity(*,parent_available,subject,actor,opportunity_basis,effective_from,effective_until,time_granularity,prior_ledger_anchor_ref,provenance_refs):
    s,a=_subject(subject),_actor(actor); p=_parent(parent_available,STATE_AVAILABLE,a.actor_id,s.subject_ref)
    b=opportunity_basis
    if not isinstance(b,OpportunityBasisEvidence): raise OEEIntegrityError("opportunity_basis must be OpportunityBasisEvidence")
    if b.actor_id!=a.actor_id or b.subject_ref!=s.subject_ref: raise OEEAdmissionError("opportunity basis actor/subject mismatch")
    _ref(b.basis_ref,"basis_ref"); ctx=_refs(b.context_or_world_receipt_refs,"context",True); cons=_refs(b.position_or_other_constraint_refs,"constraints"); _refs(b.provenance_refs,"basis.provenance",True)
    if not b.applicability_receipts: raise OEEAdmissionError("opportunity requires positive applicability")
    apps=[]
    for x in b.applicability_receipts:
        if not isinstance(x,PositiveApplicabilityReceipt) or x.result!="POSITIVE": raise OEEAdmissionError("opportunity requires positive applicability")
        _s(x.authority_id,"applicability authority"); _s(x.authority_version,"applicability version"); _h(x.authority_content_hash,"applicability authority hash"); _refs(x.provenance_refs,"applicability provenance",True); apps.append(_ref(x.receipt,"applicability receipt"))
    apps=_refs(apps,"applicability",True); start,end=_interval(effective_from,effective_until); _within(start,end,p); g=_s(time_granularity,"time_granularity"); prior=_ref(prior_ledger_anchor_ref,"prior_ledger_anchor_ref"); w=(b.basis_ref,)
    prov=_merge(p.provenance_refs,s.provenance_refs,a.provenance_refs,b.provenance_refs,*(x.provenance_refs for x in b.applicability_receipts),ctx,cons,provenance_refs,(b.basis_ref,a.phase_state_ref,prior)); cid,ch=_candidate(STATE_OPPORTUNITY,a,s,p.record_id,start,end,g,w,cons,apps,ctx)
    return OEEExecutionResult(_build(STATE_OPPORTUNITY,a,s,p.record_id,start,end,g,cid,ch,ctx,apps,cons,w,prior,prov))

def admit_encounter(*,parent_opportunity,subject,actor,contact_witness,effective_time,time_granularity,prior_ledger_anchor_ref,declared_precondition_refs,provenance_refs):
    s,a=_subject(subject),_actor(actor); p=_parent(parent_opportunity,STATE_OPPORTUNITY,a.actor_id,s.subject_ref); t=_time(effective_time,"effective_time"); _within(t,t,p); g=_s(time_granularity,"time_granularity")
    w=contact_witness
    if not isinstance(w,ContactOccurrenceWitness): raise OEEAdmissionError("ENCOUNTER requires exact ContactOccurrenceWitness")
    wr=_ref(w.witness_ref,"contact witness")
    if wr.kind in _INSUFFICIENT_CONTACT: raise OEEAdmissionError("co-location/co-presence or structural proximity is insufficient for ENCOUNTER")
    if wr.kind!=CONTACT_WITNESS_KIND: raise OEEAdmissionError("contact witness must be independently supplied contact-occurrence witness")
    if w.actor_id!=a.actor_id or w.subject_ref!=s.subject_ref: raise OEEAdmissionError("contact witness actor/subject mismatch")
    _s(w.witness_authority_id,"witness authority"); _s(w.witness_authority_version,"witness authority version"); _h(w.witness_authority_content_hash,"witness authority hash")
    if w.semantic!=CONTACT_OCCURRENCE_SEMANTIC: raise OEEAdmissionError("contact witness does not assert CONTACT_OCCURRENCE")
    if _time(w.occurrence_time,"contact occurrence time")!=t: raise OEEAdmissionError("encounter time must equal contact occurrence time")
    ir=_ref(w.independence_ref,"independence ref")
    if ir.kind!=CONTACT_INDEPENDENCE_KIND: raise OEEAdmissionError("contact witness lacks independence proof")
    _refs(w.provenance_refs,"witness provenance",True); pre=_refs(declared_precondition_refs,"preconditions",True); prior=_ref(prior_ledger_anchor_ref,"prior_ledger_anchor_ref"); witnesses=_merge((wr,ir),pre); ctx=_refs(p.context_or_world_receipt_refs,"context",True); apps=_refs(p.applicability_receipt_refs,"applicability",True); cons=_refs(p.position_or_other_constraint_refs,"constraints")
    prov=_merge(p.provenance_refs,s.provenance_refs,a.provenance_refs,w.provenance_refs,provenance_refs,witnesses,(a.phase_state_ref,prior)); cid,ch=_candidate(STATE_ENCOUNTER,a,s,p.record_id,t,t,g,witnesses,cons,apps,ctx)
    return OEEExecutionResult(_build(STATE_ENCOUNTER,a,s,p.record_id,t,t,g,cid,ch,ctx,apps,cons,witnesses,prior,prov))

def validate_basis_available_opportunity_encounter_chain(records: Sequence[V3OEERealizationRecord]):
    if len(records)!=3: raise OEEAdmissionError("bounded chain must contain exactly AVAILABLE, OPPORTUNITY, ENCOUNTER")
    a,o,e=(validate_record(x) for x in records)
    if [x.realization_state for x in (a,o,e)]!=[STATE_AVAILABLE,STATE_OPPORTUNITY,STATE_ENCOUNTER]: raise OEEAdmissionError("bounded chain state order invalid")
    if o.parent_record_id!=a.record_id or e.parent_record_id!=o.record_id: raise OEEAdmissionError("bounded chain parentage invalid")
    if len({x.actor_id for x in (a,o,e)})!=1 or len({x.subject_ref for x in (a,o,e)})!=1: raise OEEAdmissionError("bounded chain actor/subject continuity failure")
    return a,o,e

def authority_identity_manifest():
    return {"ADP-010":{"authority_id":ADP010_AUTHORITY_ID,"authority_version":ADP010_AUTHORITY_VERSION,"registry_id":ADP010_REGISTRY_ID,"registry_version":ADP010_REGISTRY_VERSION,"artifact_path":ADP010_AUTHORITY_ARTIFACT_PATH,"artifact_blob_sha":ADP010_AUTHORITY_ARTIFACT_BLOB_SHA},"ADP-008":{"authority_id":ADP008_AUTHORITY_ID,"authority_version":ADP008_AUTHORITY_VERSION,"artifact_path":ADP008_AUTHORITY_ARTIFACT_PATH,"artifact_blob_sha":ADP008_AUTHORITY_ARTIFACT_BLOB_SHA,"required_phase":DEVELOPMENT_ACTIVE_PHASE},"ADP-020":{"authority_id":ADP020_AUTHORITY_ID,"authority_version":ADP020_AUTHORITY_VERSION,"artifact_path":ADP020_AUTHORITY_ARTIFACT_PATH,"artifact_blob_sha":ADP020_AUTHORITY_ARTIFACT_BLOB_SHA,"core_rule_rng":"ZERO_DRAW"}}
