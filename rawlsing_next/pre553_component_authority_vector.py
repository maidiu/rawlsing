"""Common PRE-V3 component-authority vector closure/projection receipt."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Mapping, Sequence
from rawlsing_next.pre553_empirical_objects import (
    AuthorityRef, ExactRef, Pre553IntegrityError, authority_ref, canonicalize,
    exact_ref, semantic_hash,
)

FAMILY = "ComponentAuthorityVectorReceipt@1.0.0"
RULE_CONTRACT = "PRE553_COMPONENT_AUTHORITY_VECTOR_SCALARIZATION@1.0.0"
URN = "urn:rawlsing:pre553:ComponentAuthorityVectorReceipt:sha256"
STATES = frozenset({"VALUE","GOVERNED_EMPTY","UNRESOLVED","DENIED","NONCOMPARABLE"})
NEGATIVE_STATES = frozenset({"DENIED","NONCOMPARABLE"})

def _text(v: Any, n: str) -> str:
    if not isinstance(v,str) or not v.strip(): raise Pre553IntegrityError(f"{n} must be non-empty")
    return v.strip()
def _sha(v: Any, n: str) -> str:
    s=_text(v,n)
    if len(s)!=64 or any(c not in "0123456789abcdef" for c in s): raise Pre553IntegrityError(f"{n} must be lowercase sha256")
    return s
def _root(v: Any) -> ExactRef|str:
    if isinstance(v,ExactRef): return v
    if isinstance(v,Mapping): return exact_ref(v,"replay_root")
    s=_text(v,"replay_root")
    if s.lower() in {"latest","default","*"} or "latest" in s.lower(): raise Pre553IntegrityError("fuzzy/latest replay root forbidden")
    return s

@dataclass(frozen=True)
class ComponentAuthorityBinding:
    component_id: str
    component_ref: ExactRef
    producer_family: str
    role: str
    ordinal_or_null: int|None
    multiplicity_index: int
    authority_state: str
    authoritative_value_digest: str|None
    value_authority_ref: AuthorityRef
    negative_or_limit_refs: tuple[ExactRef,...]=()
    def __post_init__(self):
        object.__setattr__(self,"component_id",_text(self.component_id,"component_id"))
        object.__setattr__(self,"component_ref",exact_ref(self.component_ref))
        object.__setattr__(self,"producer_family",_text(self.producer_family,"producer_family"))
        object.__setattr__(self,"role",_text(self.role,"role"))
        if self.ordinal_or_null is not None and (not isinstance(self.ordinal_or_null,int) or isinstance(self.ordinal_or_null,bool) or self.ordinal_or_null<1):
            raise Pre553IntegrityError("ordinal must be positive integer or null")
        if not isinstance(self.multiplicity_index,int) or isinstance(self.multiplicity_index,bool) or self.multiplicity_index<0:
            raise Pre553IntegrityError("multiplicity_index must be nonnegative integer")
        state=_text(self.authority_state,"authority_state")
        if state not in STATES: raise Pre553IntegrityError("unknown authority state")
        object.__setattr__(self,"authority_state",state)
        object.__setattr__(self,"value_authority_ref",authority_ref(self.value_authority_ref))
        neg=tuple(sorted({exact_ref(x) for x in self.negative_or_limit_refs},key=lambda r:r.key))
        object.__setattr__(self,"negative_or_limit_refs",neg)
        if state=="VALUE":
            if self.authoritative_value_digest is None: raise Pre553IntegrityError("VALUE requires exact value digest")
            object.__setattr__(self,"authoritative_value_digest",_sha(self.authoritative_value_digest,"value_digest"))
        elif self.authoritative_value_digest is not None:
            raise Pre553IntegrityError("non-VALUE may not carry value digest")
        if state in NEGATIVE_STATES and not neg:
            raise Pre553IntegrityError(f"{state} requires exact negative/noncomparability ref")
    def as_dict(self):
        return {
            "component_id":self.component_id,"component_ref":self.component_ref.as_dict(),
            "producer_family":self.producer_family,"role":self.role,
            "ordinal_or_null":self.ordinal_or_null,"multiplicity_index":self.multiplicity_index,
            "authority_state":self.authority_state,"authoritative_value_digest":self.authoritative_value_digest,
            "value_authority_ref":self.value_authority_ref.as_dict(),
            "negative_or_limit_refs":[r.as_dict() for r in self.negative_or_limit_refs],
        }
    @classmethod
    def from_dict(cls,v:Mapping[str,Any]):
        return cls(v["component_id"],exact_ref(v["component_ref"]),v["producer_family"],v["role"],
                   v.get("ordinal_or_null"),v["multiplicity_index"],v["authority_state"],
                   v.get("authoritative_value_digest"),authority_ref(v["value_authority_ref"]),
                   tuple(exact_ref(x) for x in v.get("negative_or_limit_refs",())))

@dataclass(frozen=True)
class ComponentAuthorityVectorReceipt:
    vector_subject_ref: ExactRef
    authority_dimension_contract_ref: ExactRef
    vector_rule_authority_ref: AuthorityRef
    governed_component_ids: tuple[str,...]
    component_bindings: tuple[ComponentAuthorityBinding,...]
    producer_replay_locator_or_reference_root: ExactRef|str
    schema_id: str; schema_version: str; object_id: str; content_hash: str
    declared_component_count: int; bound_component_count: int
    missing_component_ids: tuple[str,...]; ambiguous_component_ids: tuple[str,...]
    unresolved_component_ids: tuple[str,...]; governed_empty_component_ids: tuple[str,...]
    denied_component_ids: tuple[str,...]; noncomparable_component_ids: tuple[str,...]
    complete_coverage: bool; all_governed_components_nonempty: bool
    unanimous_authoritative_value: bool
    distinct_authoritative_value_digests: tuple[str,...]
    coverage_proof_hash: str; nonempty_proof_hash: str; unanimity_proof_hash: str
    projection_disposition: str; scalar_value_digest: str|None
    negative_or_limit_refs: tuple[ExactRef,...]
    @property
    def family(self): return FAMILY
    @property
    def ref(self): return ExactRef(FAMILY,self.object_id,self.content_hash)
    def as_dict(self):
        return {
            "schema_id":self.schema_id,"schema_version":self.schema_version,
            "object_id":self.object_id,"content_hash":self.content_hash,
            "vector_subject_ref":self.vector_subject_ref.as_dict(),
            "authority_dimension_contract_ref":self.authority_dimension_contract_ref.as_dict(),
            "vector_rule_authority_ref":self.vector_rule_authority_ref.as_dict(),
            "governed_component_ids":list(self.governed_component_ids),
            "component_bindings":[b.as_dict() for b in self.component_bindings],
            "producer_replay_locator_or_reference_root":canonicalize(self.producer_replay_locator_or_reference_root),
            "declared_component_count":self.declared_component_count,"bound_component_count":self.bound_component_count,
            "missing_component_ids":list(self.missing_component_ids),"ambiguous_component_ids":list(self.ambiguous_component_ids),
            "unresolved_component_ids":list(self.unresolved_component_ids),"governed_empty_component_ids":list(self.governed_empty_component_ids),
            "denied_component_ids":list(self.denied_component_ids),"noncomparable_component_ids":list(self.noncomparable_component_ids),
            "complete_coverage":self.complete_coverage,"all_governed_components_nonempty":self.all_governed_components_nonempty,
            "unanimous_authoritative_value":self.unanimous_authoritative_value,
            "distinct_authoritative_value_digests":list(self.distinct_authoritative_value_digests),
            "coverage_proof_hash":self.coverage_proof_hash,"nonempty_proof_hash":self.nonempty_proof_hash,
            "unanimity_proof_hash":self.unanimity_proof_hash,"projection_disposition":self.projection_disposition,
            "scalar_value_digest":self.scalar_value_digest,
            "negative_or_limit_refs":[r.as_dict() for r in self.negative_or_limit_refs],
        }

def authoritative_value_digest(value:Any)->str:
    return semantic_hash({"producer_owned_authoritative_value":canonicalize(value)})

def _bsort(b:ComponentAuthorityBinding):
    return (b.ordinal_or_null is None,b.ordinal_or_null or 0,b.component_id,b.multiplicity_index,b.producer_family,b.component_ref.key)

def build_component_authority_vector_receipt(*,vector_subject_ref,authority_dimension_contract_ref,
        vector_rule_authority_ref,governed_component_ids:Sequence[str],
        component_bindings:Sequence[ComponentAuthorityBinding|Mapping[str,Any]],
        producer_replay_locator_or_reference_root)->ComponentAuthorityVectorReceipt:
    subject=exact_ref(vector_subject_ref); dim=exact_ref(authority_dimension_contract_ref)
    rule=authority_ref(vector_rule_authority_ref); root=_root(producer_replay_locator_or_reference_root)
    if isinstance(governed_component_ids,(str,bytes)) or not isinstance(governed_component_ids,Sequence): raise Pre553IntegrityError("governed ids must be explicit sequence")
    governed=tuple(_text(x,"governed_component_id") for x in governed_component_ids)
    if not governed or len(set(governed))!=len(governed): raise Pre553IntegrityError("governed component set must be nonempty and unique")
    if isinstance(component_bindings,(str,bytes)) or not isinstance(component_bindings,Sequence): raise Pre553IntegrityError("bindings must be sequence")
    bindings=tuple(sorted((b if isinstance(b,ComponentAuthorityBinding) else ComponentAuthorityBinding.from_dict(b) for b in component_bindings),key=_bsort))
    extras=sorted({b.component_id for b in bindings}-set(governed))
    if extras: raise Pre553IntegrityError(f"binding outside governed set: {extras}")
    by={cid:[] for cid in governed}
    for b in bindings: by[b.component_id].append(b)
    missing=tuple(cid for cid in governed if not by[cid])
    ambiguous=tuple(cid for cid in governed if len(by[cid])>1)
    unresolved=tuple(cid for cid in governed if any(b.authority_state=="UNRESOLVED" for b in by[cid]))
    empty=tuple(cid for cid in governed if any(b.authority_state=="GOVERNED_EMPTY" for b in by[cid]))
    denied=tuple(cid for cid in governed if any(b.authority_state=="DENIED" for b in by[cid]))
    noncomp=tuple(cid for cid in governed if any(b.authority_state=="NONCOMPARABLE" for b in by[cid]))
    complete=not(missing or ambiguous or unresolved) and all(len(by[cid])==1 for cid in governed)
    nonempty=bool(complete and not(empty or denied or noncomp) and all(by[cid][0].authority_state=="VALUE" for cid in governed))
    digests=tuple(sorted({by[cid][0].authoritative_value_digest for cid in governed if len(by[cid])==1 and by[cid][0].authority_state=="VALUE"}))
    unanimous=bool(nonempty and len(digests)==1)
    if not complete: disp,scalar="VECTOR_INCOMPLETE_COVERAGE",None
    elif denied or noncomp: disp,scalar="VECTOR_DENIED_OR_NONCOMPARABLE_COMPONENT",None
    elif empty: disp,scalar="VECTOR_GOVERNED_EMPTY_COMPONENT",None
    elif unanimous: disp,scalar="SCALARIZED_COMPLETE_UNANIMOUS_NONEMPTY",digests[0]
    else: disp,scalar="VECTOR_HETEROGENEOUS_COMPLETE",None
    negative=tuple(sorted({r for b in bindings for r in b.negative_or_limit_refs},key=lambda r:r.key))
    coverage={"governed_component_ids":list(governed),"bound":[{"id":b.component_id,"ref":b.component_ref.as_dict(),"producer":b.producer_family,"role":b.role,"ordinal":b.ordinal_or_null,"multiplicity":b.multiplicity_index,"state":b.authority_state} for b in bindings],"missing":list(missing),"ambiguous":list(ambiguous),"unresolved":list(unresolved),"complete":complete}
    nonempty_material={"complete":complete,"empty":list(empty),"denied":list(denied),"noncomparable":list(noncomp),"all_nonempty":nonempty}
    unanimity_material={"all_nonempty":nonempty,"digests":list(digests),"unanimous":unanimous}
    ch,nh,uh=semantic_hash(coverage),semantic_hash(nonempty_material),semantic_hash(unanimity_material)
    schema,version=FAMILY.split("@",1)
    material={"schema_id":schema,"schema_version":version,"vector_subject_ref":subject.as_dict(),"authority_dimension_contract_ref":dim.as_dict(),
              "vector_rule_authority_ref":rule.as_dict(),"governed_component_ids":list(governed),"component_bindings":[b.as_dict() for b in bindings],
              "producer_replay_locator_or_reference_root":canonicalize(root),"declared_component_count":len(governed),"bound_component_count":len(bindings),
              "missing_component_ids":list(missing),"ambiguous_component_ids":list(ambiguous),"unresolved_component_ids":list(unresolved),
              "governed_empty_component_ids":list(empty),"denied_component_ids":list(denied),"noncomparable_component_ids":list(noncomp),
              "complete_coverage":complete,"all_governed_components_nonempty":nonempty,"unanimous_authoritative_value":unanimous,
              "distinct_authoritative_value_digests":list(digests),"coverage_proof_hash":ch,"nonempty_proof_hash":nh,"unanimity_proof_hash":uh,
              "projection_disposition":disp,"scalar_value_digest":scalar,"negative_or_limit_refs":[r.as_dict() for r in negative]}
    digest=semantic_hash(material)
    return ComponentAuthorityVectorReceipt(subject,dim,rule,governed,bindings,root,schema,version,f"{URN}:{digest}",digest,
        len(governed),len(bindings),missing,ambiguous,unresolved,empty,denied,noncomp,complete,nonempty,unanimous,digests,ch,nh,uh,disp,scalar,negative)

def reload_component_authority_vector_receipt(value:Mapping[str,Any])->ComponentAuthorityVectorReceipt:
    r=build_component_authority_vector_receipt(
        vector_subject_ref=value["vector_subject_ref"],authority_dimension_contract_ref=value["authority_dimension_contract_ref"],
        vector_rule_authority_ref=value["vector_rule_authority_ref"],governed_component_ids=value["governed_component_ids"],
        component_bindings=value["component_bindings"],producer_replay_locator_or_reference_root=value["producer_replay_locator_or_reference_root"])
    expected=r.as_dict()
    for k,v in expected.items():
        if canonicalize(value.get(k))!=canonicalize(v): raise Pre553IntegrityError(f"serialized receipt mismatch: {k}")
    return r

__all__=["FAMILY","RULE_CONTRACT","STATES","ComponentAuthorityBinding","ComponentAuthorityVectorReceipt",
         "authoritative_value_digest","build_component_authority_vector_receipt","reload_component_authority_vector_receipt"]
