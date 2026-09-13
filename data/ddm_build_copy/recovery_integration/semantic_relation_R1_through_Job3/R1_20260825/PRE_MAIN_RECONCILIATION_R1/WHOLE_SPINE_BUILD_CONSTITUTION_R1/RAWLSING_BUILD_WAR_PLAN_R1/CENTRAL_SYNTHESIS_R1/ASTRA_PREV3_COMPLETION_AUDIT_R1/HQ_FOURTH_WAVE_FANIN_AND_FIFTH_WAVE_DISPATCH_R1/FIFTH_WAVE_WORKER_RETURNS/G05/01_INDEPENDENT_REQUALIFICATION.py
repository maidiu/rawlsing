from __future__ import annotations
import hashlib, json
from rawlsing_next.objective_consumer_bounded_evidence import (
    ClaimCeiling, DecisionState, EvidenceKind, EvidenceTier, ExactRef,
    NonEmpiricalAuthorityRequired, NotYetApplicableConsumer, OC01, OC02, OC03, OC04, OC05,
    PolicyInput, RenormalizationForbidden, evaluate_current_consumer,
    evaluate_oc01_pre553_source_local, evaluate_oc02_structural_admission,
)

def h(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def ref(kind: str, tag: str, *, object_id: str | None = None) -> ExactRef:
    return ExactRef(kind, object_id or f"urn:g05:{kind.lower()}:{tag}", h(f"{kind}:{tag}"))

def present(input_id: str, *, required=True, ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
            tier=EvidenceTier.SOURCE_LOCAL_CERTIFIED, authority_refs=None):
    if authority_refs is None:
        authority_refs=(ref("AUTHORITY", input_id+":A"),)
    return PolicyInput(
        input_id=input_id, required=required, available=True, evidence_kind=EvidenceKind.EMPIRICAL,
        evidence_tier=tier, claim_ceiling=ceiling, producer_ref=ref("PRODUCER", input_id),
        authority_refs=tuple(authority_refs),
    )

def missing(input_id: str, reason: str, *, required=False):
    return PolicyInput(
        input_id=input_id, required=required, available=False, evidence_kind=EvidenceKind.EMPIRICAL,
        evidence_tier=EvidenceTier.UNAVAILABLE, claim_ceiling=ClaimCeiling.SUPPORTED_COMPONENT_ONLY,
        omission_reason=reason,
    )

def check(case_id: str, condition: bool, detail: dict):
    return {"case_id":case_id, "result":"PASS" if condition else "FAIL", **detail}

results=[]

# Q01: omission reason alone changes replay identity while decision semantics stay fixed.
a=evaluate_oc01_pre553_source_local(
    operation_id="G05-Q01", inputs=(present("survivor"), missing("lost","SCOPE_A")),
    requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC, partial_allowed=True)
b=evaluate_oc01_pre553_source_local(
    operation_id="G05-Q01", inputs=(present("survivor"), missing("lost","SCOPE_B")),
    requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC, partial_allowed=True)
results.append(check("G05-Q01", a.receipt_hash!=b.receipt_hash and a.as_dict()!=b.as_dict()
                     and a.state==b.state==DecisionState.PARTIAL_OBJECTIVE_RESULT
                     and a.positive_completion and b.positive_completion,
                     {"left_hash":a.receipt_hash,"right_hash":b.receipt_hash,"state":a.state.value}))

# Q02: exact authority content change with stable input/producer changes identity, not decision state.
shared_oid="urn:g05:authority:stable-object"
a1=ref("AUTHORITY","content-v1", object_id=shared_oid)
a2=ref("AUTHORITY","content-v2", object_id=shared_oid)
a=evaluate_oc02_structural_admission(operation_id="G05-Q02", inputs=(present("rel",ceiling=ClaimCeiling.STRUCTURAL_RELATION,tier=EvidenceTier.PARTIAL_AUTHORITY,authority_refs=(a1,)),))
b=evaluate_oc02_structural_admission(operation_id="G05-Q02", inputs=(present("rel",ceiling=ClaimCeiling.STRUCTURAL_RELATION,tier=EvidenceTier.PARTIAL_AUTHORITY,authority_refs=(a2,)),))
results.append(check("G05-Q02", a.receipt_hash!=b.receipt_hash and a.state==b.state==DecisionState.SUPPORTED_OBJECTIVE_RESULT,
                     {"left_hash":a.receipt_hash,"right_hash":b.receipt_hash,"state":a.state.value}))

# Q03: duplicate/order variance in authority refs canonicalizes to one receipt.
x=ref("AUTHORITY","X"); y=ref("AUTHORITY","Y")
a=evaluate_oc01_pre553_source_local(operation_id="G05-Q03",inputs=(present("a",authority_refs=(x,y,x)),),requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC)
b=evaluate_oc01_pre553_source_local(operation_id="G05-Q03",inputs=(present("a",authority_refs=(y,x)),),requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC)
results.append(check("G05-Q03", a.receipt_hash==b.receipt_hash and a.as_dict()==b.as_dict(), {"receipt_hash":a.receipt_hash}))

# Q04: input-order variance, including unavailable provenance, canonicalizes stably.
manifest1=(missing("z","Z_REASON"),present("a",required=False),missing("m","M_REASON",required=True))
manifest2=(missing("m","M_REASON",required=True),missing("z","Z_REASON"),present("a",required=False))
a=evaluate_oc01_pre553_source_local(operation_id="G05-Q04",inputs=manifest1,requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC)
b=evaluate_oc01_pre553_source_local(operation_id="G05-Q04",inputs=manifest2,requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC)
results.append(check("G05-Q04", a.receipt_hash==b.receipt_hash and a.as_dict()==b.as_dict(), {"receipt_hash":a.receipt_hash,"state":a.state.value}))

# Q05: swapping omission-reason associations with fixed missing IDs changes identity, while state/refusal stay fixed.
a=evaluate_oc01_pre553_source_local(operation_id="G05-Q05",inputs=(present("survivor",required=False),missing("m1","R1",required=True),missing("m2","R2",required=True)),requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC)
b=evaluate_oc01_pre553_source_local(operation_id="G05-Q05",inputs=(present("survivor",required=False),missing("m1","R2",required=True),missing("m2","R1",required=True)),requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC)
results.append(check("G05-Q05", a.receipt_hash!=b.receipt_hash and a.state==b.state==DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE and a.refusal_reasons==b.refusal_reasons,
                     {"left_hash":a.receipt_hash,"right_hash":b.receipt_hash,"state":a.state.value}))

# Q06: source-local evidence remains unable to satisfy a population claim.
r=evaluate_oc01_pre553_source_local(operation_id="G05-Q06",inputs=(present("local"),),requested_claim_ceiling=ClaimCeiling.POPULATION_STATISTIC)
results.append(check("G05-Q06", r.state is DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE and not r.positive_completion,
                     {"state":r.state.value,"positive_completion":r.positive_completion}))

# Q07: nonempirical prior still needs distinct authority and cannot manufacture empirical completion.
prior_guard=False
try:
    PolicyInput(input_id="prior",required=False,available=True,evidence_kind=EvidenceKind.NON_EMPIRICAL_MODEL,
        evidence_tier=EvidenceTier.PARTIAL_AUTHORITY,claim_ceiling=ClaimCeiling.SUPPORTED_COMPONENT_ONLY,
        producer_ref=ref("MODEL","prior"),authority_refs=(ref("MODEL_INPUT_AUTHORITY","prior"),),model_prior_version="G05-R1")
except NonEmpiricalAuthorityRequired:
    prior_guard=True
prior=PolicyInput(input_id="prior-ok",required=False,available=True,evidence_kind=EvidenceKind.NON_EMPIRICAL_MODEL,
    evidence_tier=EvidenceTier.PARTIAL_AUTHORITY,claim_ceiling=ClaimCeiling.SUPPORTED_COMPONENT_ONLY,
    producer_ref=ref("MODEL","prior-ok"),authority_refs=(ref("MODEL_INPUT_AUTHORITY","prior-ok"),),
    model_prior_version="G05-R1",model_prior_authority_ref=ref("NON_EMPIRICAL_POLICY_AUTHORITY","prior-ok"))
r=evaluate_oc01_pre553_source_local(operation_id="G05-Q07",inputs=(prior,missing("empirical","NO_SOURCE")),requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC)
results.append(check("G05-Q07", prior_guard and r.state is DecisionState.ALL_UNAVAILABLE__NOT_POSITIVE_COMPLETION and not r.positive_completion,
                     {"prior_guard":prior_guard,"state":r.state.value,"positive_completion":r.positive_completion}))

# Q08: renormalization remains forbidden.
renorm_guard=False
try:
    evaluate_oc01_pre553_source_local(operation_id="G05-Q08",inputs=(present("x"),),requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,renormalization_requested=True)
except RenormalizationForbidden:
    renorm_guard=True
results.append(check("G05-Q08",renorm_guard,{"renormalization_forbidden":renorm_guard}))

# Q09: repair does not promote future consumers.
residual=[]
for p in (OC03,OC04,OC05):
    try:
        evaluate_current_consumer(policy_id=p,operation_id="G05-Q09",inputs=(present("x"),),requested_claim_ceiling=ClaimCeiling.OBJECTIVE_FACT,partial_allowed=False)
    except NotYetApplicableConsumer:
        residual.append(p)
results.append(check("G05-Q09",residual==[OC03,OC04,OC05],{"not_yet_applicable":residual}))

out={"schema":"G05_BOUNDED_EVIDENCE_INDEPENDENT_REQUALIFICATION_R1","status":"PASS" if all(x["result"]=="PASS" for x in results) else "FAIL","case_count":len(results),"pass_count":sum(x["result"]=="PASS" for x in results),"fail_count":sum(x["result"]!="PASS" for x in results),"cases":results}
print(json.dumps(out,indent=2,sort_keys=True))
raise SystemExit(0 if out["status"]=="PASS" else 1)
