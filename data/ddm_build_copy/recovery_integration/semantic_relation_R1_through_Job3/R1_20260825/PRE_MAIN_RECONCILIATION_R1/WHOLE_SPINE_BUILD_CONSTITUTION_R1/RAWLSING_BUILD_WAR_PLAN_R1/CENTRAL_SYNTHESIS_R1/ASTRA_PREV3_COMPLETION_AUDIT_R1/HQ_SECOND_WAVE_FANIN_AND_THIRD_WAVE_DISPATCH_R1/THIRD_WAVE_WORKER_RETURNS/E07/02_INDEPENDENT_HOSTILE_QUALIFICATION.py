from __future__ import annotations
import hashlib
from rawlsing_next.objective_consumer_bounded_evidence import (
    ClaimCeiling, DecisionState, EvidenceKind, EvidenceTier, ExactRef,
    NotYetApplicableConsumer, OC01, OC02, OC03, OC04, OC05, PolicyInput,
    RenormalizationForbidden, evaluate_current_consumer,
    evaluate_oc01_pre553_source_local, evaluate_oc02_structural_admission,
)

def h(s): return hashlib.sha256(s.encode()).hexdigest()
def ref(kind, tag): return ExactRef(kind, f"urn:e07:{kind.lower()}:{tag}", h(f"{kind}:{tag}"))
def present(input_id, *, required=True, ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC, tier=EvidenceTier.SOURCE_LOCAL_CERTIFIED, authority_tag="A"):
    return PolicyInput(input_id=input_id, required=required, available=True, evidence_kind=EvidenceKind.EMPIRICAL,
        evidence_tier=tier, claim_ceiling=ceiling, producer_ref=ref("PRODUCER", input_id), authority_refs=(ref("AUTHORITY", authority_tag),))
def missing(input_id, *, required, reason):
    return PolicyInput(input_id=input_id, required=required, available=False, evidence_kind=EvidenceKind.EMPIRICAL,
        evidence_tier=EvidenceTier.UNAVAILABLE, claim_ceiling=ClaimCeiling.SUPPORTED_COMPONENT_ONLY, omission_reason=reason)

def check(name, condition, detail):
    print(f"{name}: {'PASS' if condition else 'FAIL'}: {detail}")
    return bool(condition)

results=[]
# H01 source-local != population
r=evaluate_oc01_pre553_source_local(operation_id="E07-H01", inputs=(present("src"),), requested_claim_ceiling=ClaimCeiling.POPULATION_STATISTIC)
results.append(check("E07-H01", r.state is DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE and not r.positive_completion, r.state.value))

# H02 omission/refusal reason provenance must be replayable. Only reason changes.
a=evaluate_oc01_pre553_source_local(operation_id="E07-H02", inputs=(present("survivor", required=False), missing("required", required=True, reason="RISK_SET_UNAVAILABLE")), requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC)
b=evaluate_oc01_pre553_source_local(operation_id="E07-H02", inputs=(present("survivor", required=False), missing("required", required=True, reason="SOURCE_SCOPE_UNAVAILABLE")), requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC)
results.append(check("E07-H02", a.receipt_hash != b.receipt_hash and a.as_dict() != b.as_dict(), f"same_hash={a.receipt_hash == b.receipt_hash}; same_receipt={a.as_dict()==b.as_dict()}"))

# H03 selected exact authority dependencies must be provenance-bearing/replayable. Only authority ref changes.
a=evaluate_oc02_structural_admission(operation_id="E07-H03", inputs=(present("relation", ceiling=ClaimCeiling.STRUCTURAL_RELATION, tier=EvidenceTier.PARTIAL_AUTHORITY, authority_tag="AUTH-1"),))
b=evaluate_oc02_structural_admission(operation_id="E07-H03", inputs=(present("relation", ceiling=ClaimCeiling.STRUCTURAL_RELATION, tier=EvidenceTier.PARTIAL_AUTHORITY, authority_tag="AUTH-2"),))
results.append(check("E07-H03", a.receipt_hash != b.receipt_hash and a.as_dict() != b.as_dict(), f"same_hash={a.receipt_hash == b.receipt_hash}; same_receipt={a.as_dict()==b.as_dict()}"))

# H04 no-renormalization explicit request refuses
try:
    evaluate_oc01_pre553_source_local(operation_id="E07-H04", inputs=(present("src"),), requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC, renormalization_requested=True)
except RenormalizationForbidden:
    results.append(check("E07-H04", True, "RENORMALIZATION_FORBIDDEN"))
else:
    results.append(check("E07-H04", False, "renormalization accepted"))

# H05 all unavailable cannot positive-complete
r=evaluate_oc01_pre553_source_local(operation_id="E07-H05", inputs=(missing("a", required=True, reason="LOSS"), missing("b", required=False, reason="LOSS")), requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC)
results.append(check("E07-H05", r.state is DecisionState.ALL_UNAVAILABLE__NOT_POSITIVE_COMPLETION and not r.positive_completion, r.state.value))

# H06 unrelated lawful service remains selected while required local evidence loss refuses affected operation
r=evaluate_oc01_pre553_source_local(operation_id="E07-H06", inputs=(present("unrelated", required=False), missing("required", required=True, reason="LOSS")), requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC)
results.append(check("E07-H06", r.state is DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE and r.selected_input_ids == ("unrelated",), f"state={r.state.value}; selected={r.selected_input_ids}"))

# H07 future consumers stay explicit residuals
ok=True
for p in (OC03, OC04, OC05):
    try:
        evaluate_current_consumer(policy_id=p, operation_id="E07-H07", inputs=(present("fake"),), requested_claim_ceiling=ClaimCeiling.OBJECTIVE_FACT, partial_allowed=False)
    except NotYetApplicableConsumer:
        pass
    else:
        ok=False
results.append(check("E07-H07", ok, "OC03/OC04/OC05 NOT_YET_APPLICABLE" if ok else "future consumer executed"))

print(f"SUMMARY: pass={sum(results)} fail={len(results)-sum(results)} total={len(results)}")
raise SystemExit(0 if all(results) else 1)
