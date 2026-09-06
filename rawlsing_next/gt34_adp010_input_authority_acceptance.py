"""OBL056 candidate: exact ADP-010 input-authority acceptance binding only."""
from __future__ import annotations
from dataclasses import asdict, dataclass, replace
from hashlib import sha256
import json, unicodedata
from typing import Any

ACCEPTANCE_AUTHORITY_ID="GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_REGISTRY"
ACCEPTANCE_AUTHORITY_VERSION="1.0.0"
REGISTRY_ID=ACCEPTANCE_AUTHORITY_ID
REGISTRY_VERSION="1.0.0"
RECEIPT_SCHEMA_ID="GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_RECEIPT@1.0.0"
ENTRY_SCHEMA_ID="GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_ENTRY@1.0.0"
CONSUMER="V3_OPPORTUNITY_ENCOUNTER_EXPOSURE_REALIZATION_RULE@1.0.0"
CAUSAL_USE_PERMISSION="CAUSAL_USE_PERMISSION"
POSITIVE_APPLICABILITY="POSITIVE_APPLICABILITY"
CONTACT_OCCURRENCE_WITNESS="CONTACT_OCCURRENCE_WITNESS"
CONTACT_WITNESS_INDEPENDENCE="CONTACT_WITNESS_INDEPENDENCE"
SUPPORTED_ROLES=(CAUSAL_USE_PERMISSION,POSITIVE_APPLICABILITY,CONTACT_OCCURRENCE_WITNESS,CONTACT_WITNESS_INDEPENDENCE)
CURRENT_ACCEPTED="CURRENT_ACCEPTED"
NONCURRENT_SYNTHETIC_TEST_ONLY="NONCURRENT_SYNTHETIC_TEST_ONLY"
CANDIDATE_NOT_ADOPTED="CANDIDATE_NOT_ADOPTED"
ACCEPT="ACCEPT"
AUTHORITY_CEILING=("NO_SUBJECT_IDENTITY_OR_CLASSIFICATION","NO_CAUSAL_USE_SEMANTIC_TRUTH","NO_APPLICABILITY_SEMANTIC_TRUTH","NO_CONTACT_OCCURRENCE","NO_CONTACT_INDEPENDENCE_FACT","NO_ENCOUNTER","NO_EXPOSURE","NO_EXTERNAL_EVENT_ADMISSION","NO_COMPARATOR","NO_PSEPF","NO_METABOLISM","NO_CAN_008","NO_V2","NO_POSITIVE_V3_ACTOR_MUTATION","NO_GENERIC_PROJECT_WIDE_AUTHORITY_ADMISSION")
_DOMAIN="RAWLSING\0GT34\0OBL056\0ADP010_INPUT_AUTHORITY_ACCEPTANCE_V1\0"

class AcceptanceAuthorityError(ValueError): pass
class AcceptanceIntegrityError(AcceptanceAuthorityError): pass
class AcceptanceMissingAuthority(AcceptanceAuthorityError): pass
class AcceptanceOutOfScope(AcceptanceAuthorityError): pass

def _norm(v:Any)->Any:
    if isinstance(v,str): return unicodedata.normalize("NFC",v)
    if isinstance(v,dict): return {str(k):_norm(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)): return [_norm(x) for x in v]
    return v
def _canonical_json(v:Any)->str:
    return json.dumps(_norm(v),sort_keys=True,separators=(",",":"),ensure_ascii=False)
def _digest(label:str,v:Any)->str:
    return sha256((_DOMAIN+label+"\0"+_canonical_json(v)).encode()).hexdigest()

@dataclass(frozen=True,order=True,slots=True)
class ContentAddressedRef:
    id:str; version:str; content_hash:str
@dataclass(frozen=True,order=True,slots=True)
class EvidenceRef:
    ref:str; content_hash:str
@dataclass(frozen=True,slots=True)
class AcceptanceScope:
    transition_use_scope:str
    family_scope:tuple[str,...]=()
    subject_scope:tuple[str,...]=()
    object_scope:tuple[str,...]=()
@dataclass(frozen=True,slots=True)
class AcceptanceEntry:
    schema_id:str; role:str; accepted_authority_ref:ContentAddressedRef
    accepted_authority_owner_jurisdiction_ref:EvidenceRef
    source_acceptance_evidence_ref:EvidenceRef; decision_state:str; consumer:str
    scope:AcceptanceScope; negative_limit_refs:tuple[EvidenceRef,...]
    currentness_state:str; immutable_provenance:tuple[EvidenceRef,...]
    entry_id:str; entry_hash:str
@dataclass(frozen=True,slots=True)
class AcceptanceReceipt:
    schema_id:str; acceptance_authority_ref:ContentAddressedRef
    registry_ref:ContentAddressedRef; registry_entry_ref:EvidenceRef; role:str
    accepted_authority_ref:ContentAddressedRef
    accepted_authority_owner_jurisdiction_ref:EvidenceRef
    source_acceptance_evidence_ref:EvidenceRef; decision_state:str; consumer:str
    scope:AcceptanceScope; negative_limit_refs:tuple[EvidenceRef,...]
    currentness_state:str; immutable_provenance:tuple[EvidenceRef,...]
    receipt_id:str; receipt_hash:str

_TRANSITION_USE_BY_ROLE={
CAUSAL_USE_PERMISSION:"BASIS_TO_AVAILABLE:ADP010_CAUSAL_USE",
POSITIVE_APPLICABILITY:"AVAILABLE_TO_OPPORTUNITY:POSITIVE_APPLICABILITY",
CONTACT_OCCURRENCE_WITNESS:"OPPORTUNITY_TO_ENCOUNTER:CONTACT_OCCURRENCE_WITNESS",
CONTACT_WITNESS_INDEPENDENCE:"OPPORTUNITY_TO_ENCOUNTER:CONTACT_WITNESS_INDEPENDENCE",
}
_AUTHORITY_MATERIAL={"authority_id":ACCEPTANCE_AUTHORITY_ID,"authority_version":ACCEPTANCE_AUTHORITY_VERSION,"grain":"EXACT_ALREADY_EXISTING_AUTHORITY_ACCEPTANCE_FOR_ONE_ADP010_INPUT_ROLE_AND_SCOPE_ONLY","consumer":CONSUMER,"supported_roles":SUPPORTED_ROLES,"status":CANDIDATE_NOT_ADOPTED,"authority_ceiling":AUTHORITY_CEILING}
ACCEPTANCE_AUTHORITY_CONTENT_HASH=_digest("AUTHORITY",_AUTHORITY_MATERIAL)
ACCEPTANCE_AUTHORITY_REF=ContentAddressedRef(ACCEPTANCE_AUTHORITY_ID,ACCEPTANCE_AUTHORITY_VERSION,ACCEPTANCE_AUTHORITY_CONTENT_HASH)
_CURRENT_ENTRIES:tuple[AcceptanceEntry,...]=()
_REGISTRY_MATERIAL={"registry_id":REGISTRY_ID,"registry_version":REGISTRY_VERSION,"acceptance_authority_ref":asdict(ACCEPTANCE_AUTHORITY_REF),"receipt_schema_id":RECEIPT_SCHEMA_ID,"consumer":CONSUMER,"supported_roles":SUPPORTED_ROLES,"currentness_state":CANDIDATE_NOT_ADOPTED,"current_positive_entries":[]}
REGISTRY_CONTENT_HASH=_digest("REGISTRY",_REGISTRY_MATERIAL)
REGISTRY_REF=ContentAddressedRef(REGISTRY_ID,REGISTRY_VERSION,REGISTRY_CONTENT_HASH)

def _ev(label:str,v:Any)->EvidenceRef:
    h=_digest("EVIDENCE:"+label,v)
    return EvidenceRef("urn:rawlsing:gt34:obl056:evidence:"+label+":sha256:"+h,h)
def _entry_body(e:AcceptanceEntry)->dict[str,Any]:
    return {"schema_id":e.schema_id,"role":e.role,"accepted_authority_ref":asdict(e.accepted_authority_ref),"accepted_authority_owner_jurisdiction_ref":asdict(e.accepted_authority_owner_jurisdiction_ref),"source_acceptance_evidence_ref":asdict(e.source_acceptance_evidence_ref),"decision_state":e.decision_state,"consumer":e.consumer,"scope":asdict(e.scope),"negative_limit_refs":[asdict(x) for x in e.negative_limit_refs],"currentness_state":e.currentness_state,"immutable_provenance":[asdict(x) for x in e.immutable_provenance]}
def _make_entry(role:str)->AcceptanceEntry:
    ar=ContentAddressedRef("SYNTHETIC_EXISTING_"+role+"_AUTHORITY","1.0.0",_digest("SYNTH_ACCEPTED:"+role,{"role":role}))
    owner=_ev("synthetic-owner-"+role.lower(),{"role":role})
    source=_ev("synthetic-source-"+role.lower(),{"role":role,"accepted":True})
    prov=(_ev("synthetic-provenance",{"mode":NONCURRENT_SYNTHETIC_TEST_ONLY}),)
    scope=AcceptanceScope(_TRANSITION_USE_BY_ROLE[role],("SYNTHETIC_TEST_FAMILY",),("SYNTHETIC_TEST_SUBJECT",),("SYNTHETIC_TEST_OBJECT",))
    p=AcceptanceEntry(ENTRY_SCHEMA_ID,role,ar,owner,source,ACCEPT,CONSUMER,scope,(),NONCURRENT_SYNTHETIC_TEST_ONLY,prov,"PENDING","0"*64)
    h=_digest("ENTRY",_entry_body(p))
    return replace(p,entry_id="urn:rawlsing:gt34:obl056:acceptance-entry:sha256:"+h,entry_hash=h)

_SYNTH_ENTRIES=tuple(_make_entry(r) for r in SUPPORTED_ROLES)
_SYNTH_AUTHORITY_REF=ContentAddressedRef(ACCEPTANCE_AUTHORITY_ID+"_SYNTHETIC_TEST","1.0.0",_digest("SYNTH_AUTHORITY",{"roles":SUPPORTED_ROLES,"currentness":NONCURRENT_SYNTHETIC_TEST_ONLY}))
_SYNTH_REGISTRY_REF=ContentAddressedRef(REGISTRY_ID+"_SYNTHETIC_TEST","1.0.0",_digest("SYNTH_REGISTRY",[e.entry_hash for e in _SYNTH_ENTRIES]))

def _receipt_body(r:AcceptanceReceipt)->dict[str,Any]:
    return {"schema_id":r.schema_id,"acceptance_authority_ref":asdict(r.acceptance_authority_ref),"registry_ref":asdict(r.registry_ref),"registry_entry_ref":asdict(r.registry_entry_ref),"role":r.role,"accepted_authority_ref":asdict(r.accepted_authority_ref),"accepted_authority_owner_jurisdiction_ref":asdict(r.accepted_authority_owner_jurisdiction_ref),"source_acceptance_evidence_ref":asdict(r.source_acceptance_evidence_ref),"decision_state":r.decision_state,"consumer":r.consumer,"scope":asdict(r.scope),"negative_limit_refs":[asdict(x) for x in r.negative_limit_refs],"currentness_state":r.currentness_state,"immutable_provenance":[asdict(x) for x in r.immutable_provenance]}
def _issue(e:AcceptanceEntry)->AcceptanceReceipt:
    p=AcceptanceReceipt(RECEIPT_SCHEMA_ID,_SYNTH_AUTHORITY_REF,_SYNTH_REGISTRY_REF,EvidenceRef(e.entry_id,e.entry_hash),e.role,e.accepted_authority_ref,e.accepted_authority_owner_jurisdiction_ref,e.source_acceptance_evidence_ref,e.decision_state,e.consumer,e.scope,e.negative_limit_refs,e.currentness_state,e.immutable_provenance,"PENDING","0"*64)
    h=_digest("RECEIPT",_receipt_body(p))
    return replace(p,receipt_id="urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:"+h,receipt_hash=h)
def issue_noncurrent_synthetic_test_receipt(role:str)->AcceptanceReceipt:
    if role not in SUPPORTED_ROLES: raise AcceptanceOutOfScope("unsupported role")
    return _issue(next(e for e in _SYNTH_ENTRIES if e.role==role))

def _check_integrity(r:AcceptanceReceipt)->None:
    h=_digest("RECEIPT",_receipt_body(r))
    if r.receipt_hash!=h or r.receipt_id!="urn:rawlsing:gt34:obl056:acceptance-receipt:sha256:"+h:
        raise AcceptanceIntegrityError("acceptance receipt content/hash mismatch")
def validate_acceptance_receipt(r:AcceptanceReceipt,*,expected_role:str,expected_accepted_authority_ref:ContentAddressedRef,expected_owner_jurisdiction_ref:EvidenceRef,expected_source_acceptance_evidence_ref:EvidenceRef,expected_scope:AcceptanceScope,required_currentness:str)->AcceptanceReceipt:
    if not isinstance(r,AcceptanceReceipt): raise AcceptanceMissingAuthority("exact receipt required")
    _check_integrity(r)
    if r.role!=expected_role or expected_role not in SUPPORTED_ROLES: raise AcceptanceOutOfScope("role mismatch")
    if r.consumer!=CONSUMER: raise AcceptanceOutOfScope("consumer mismatch")
    if r.accepted_authority_ref!=expected_accepted_authority_ref: raise AcceptanceOutOfScope("authority identity/version/hash mismatch")
    if r.accepted_authority_owner_jurisdiction_ref!=expected_owner_jurisdiction_ref: raise AcceptanceOutOfScope("owner/jurisdiction mismatch")
    if r.source_acceptance_evidence_ref!=expected_source_acceptance_evidence_ref: raise AcceptanceOutOfScope("source evidence mismatch")
    if r.scope!=expected_scope: raise AcceptanceOutOfScope("transition/use/family/subject/object scope mismatch")
    if r.currentness_state!=required_currentness: raise AcceptanceOutOfScope("currentness mismatch")
    if r.decision_state!=ACCEPT: raise AcceptanceMissingAuthority("nonpositive")
    if required_currentness==CURRENT_ACCEPTED:
        raise AcceptanceMissingAuthority("candidate registry not adopted/current; current positive set empty")
    if required_currentness!=NONCURRENT_SYNTHETIC_TEST_ONLY: raise AcceptanceOutOfScope("unknown currentness")
    if r.acceptance_authority_ref!=_SYNTH_AUTHORITY_REF or r.registry_ref!=_SYNTH_REGISTRY_REF: raise AcceptanceIntegrityError("issuer/registry mismatch")
    matches=[e for e in _SYNTH_ENTRIES if e.role==r.role and e.accepted_authority_ref==r.accepted_authority_ref and e.accepted_authority_owner_jurisdiction_ref==r.accepted_authority_owner_jurisdiction_ref and e.source_acceptance_evidence_ref==r.source_acceptance_evidence_ref and e.scope==r.scope and e.currentness_state==r.currentness_state]
    if len(matches)!=1: raise AcceptanceMissingAuthority("no exact positive registry entry")
    e=matches[0]
    eh=_digest("ENTRY",_entry_body(e))
    if e.entry_hash!=eh or r.registry_entry_ref!=EvidenceRef(e.entry_id,e.entry_hash): raise AcceptanceIntegrityError("entry binding mismatch")
    if r.negative_limit_refs!=e.negative_limit_refs or r.immutable_provenance!=e.immutable_provenance: raise AcceptanceIntegrityError("limits/provenance mismatch")
    return r

def validate_contact_acceptance_pair(o:AcceptanceReceipt,i:AcceptanceReceipt)->tuple[AcceptanceReceipt,AcceptanceReceipt]:
    if o.receipt_id==i.receipt_id or o.receipt_hash==i.receipt_hash: raise AcceptanceOutOfScope("contact occurrence and independence require distinct acceptance receipts")
    if o.accepted_authority_ref==i.accepted_authority_ref: raise AcceptanceOutOfScope("contact occurrence and independence require distinct accepted authorities")
    if o.role!=CONTACT_OCCURRENCE_WITNESS or i.role!=CONTACT_WITNESS_INDEPENDENCE: raise AcceptanceOutOfScope("contact role mismatch")
    return o,i

def candidate_registry_artifact()->dict[str,Any]:
    return {"schema_id":"GT34_ADP010_INPUT_AUTHORITY_ACCEPTANCE_REGISTRY_ARTIFACT@1.0.0","status":CANDIDATE_NOT_ADOPTED,"acceptance_authority_ref":asdict(ACCEPTANCE_AUTHORITY_REF),"registry_ref":asdict(REGISTRY_REF),"receipt_schema_id":RECEIPT_SCHEMA_ID,"consumer":CONSUMER,"supported_roles":list(SUPPORTED_ROLES),"current_positive_entries":[],"authority_ceiling":list(AUTHORITY_CEILING),"positive_fallback":False,"generic_project_wide_authority":False}
def receipt_schema_artifact()->dict[str,Any]:
    return {"schema_id":RECEIPT_SCHEMA_ID,"required_fields":["acceptance_authority_ref","registry_ref","registry_entry_ref","role","accepted_authority_ref","accepted_authority_owner_jurisdiction_ref","source_acceptance_evidence_ref","decision_state","consumer","scope.transition_use_scope","scope.family_scope","scope.subject_scope","scope.object_scope","negative_limit_refs","currentness_state","immutable_provenance","receipt_id","receipt_hash"],"positive_decision_state":ACCEPT,"current_positive_requires_separate_adoption":True,"synthetic_currentness":NONCURRENT_SYNTHETIC_TEST_ONLY}
