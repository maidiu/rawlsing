"""Conserve A42's independent 151/101, AT and all35 expectations without adoption."""
from pathlib import Path
import hashlib,json

R=Path(__file__).resolve().parents[1]


def main():
    s=json.loads((R/"inputs/A42_EXPECTED_SCOPE.json").read_text())
    waves=json.loads((R/"original35_wave_execution_manifest.json").read_text())
    frontier=json.loads((R/"evidence/original35_frontier_summary.json").read_text())
    if {w["atlas_id"] for w in waves}!={w["source_id"] for w in s["waves"]}:raise ValueError("A42_ALL35_NO_DROP")
    if (s["register_151_count"],s["ledger_101_count"],len(s["cells"]))!=(151,101,1890):raise ValueError("A42_EXPECTATION_CHANGED")
    owners={
        "S":"Competent original source/instrument/response/routing/design/scientific issuers; named per-source packets",
        "P":"Existing physical decoder, source-backed C11, source-equivalence and repository owners; B43 permitted native executor",
        "Q":"Existing I03/I05/Batch, V550/J and scientific U/E_pre owners; U43/B43 at admitted scope",
        "L":"Existing M1/M2/B5/I4 lifecycle and authority owners; E41/B43 exact source fact ingress",
        "F":"F43 plus original FF/independent-source transport method issuers",
        "T":"Existing temporal owners and F43; competent comparable-wave/estimand issuer",
        "W":"Existing W41/N9, E41/N10E and P41/N10W owners; J42 remains separate",
        "G":"Competent project/inheritance/proof HQ; source rights remain with original issuers",
        "A":"Existing A42/N11 assessor and independent N12 authority; no worker retirement rights",
    }
    unmatched=[]
    for row in s["register_151_rows"]:
        if row["id"] in s["crosswalk_151_101"]["unmatched_register_rows"]:
            unmatched.append(dict(original_register_row=row,owner=owners[row["group"]],
                exact_next_action="Bind exact existing owner/authority/product/consumer evidence satisfying: "+row["exit_proof"],
                status="UNRESOLVED_EXACT_CROSSWALK__NOT_NEW_METHOD_OR_GRANTED_OPERATION",competent_retirement_ref=None))
    if len(unmatched)!=81:raise ValueError("UNMATCHED_REGISTER_NO_DROP")
    at=sorted({g for r in s["register_151_rows"] for g in r["gates"] if g.startswith("AT")})
    (R/"A42_151_101_and_81_owner_demands.json").write_text(json.dumps(dict(
        a42_commit="843175b0587b54db3df1f461ad9f7f1314894372",register_151=s["register_151_rows"],
        ledger_101=s["ledger_101_rows"],original_crosswalk=s["crosswalk_151_101"],
        AT_obligations=at,unmatched81=unmatched,worker_retirements=0),sort_keys=True,indent=2)+"\n")
    payload=dict(schema="U43_B43_A42_HANDOFF@1",grade="AUTHOR_SOURCEFREE_NATIVE_AND_RESEARCH_ACCOUNTING__ORIGINAL_SCIENCE_UNISSUED",
        measured_original=0,original_eligible_count=None,permitted_original_manifests=[],
        full_scientific_workload_completed=False,frontier=frontier,
        source_decision_packets="original35_issuer_decision_packets.json",
        source_specific_demands=175,unmatched_register_demands=81,
        native_entrypoint="rawlsing_next.pre553_issued_workload.execute_issued_workload",
        actual_native_types=["GovernedC11Projection","RuntimeObjectCatalog","I03ExecutionRequest","DiscoveryAuthority","BatchManifest","UnitExecutionReceipt"],
        source_factory_binding="NativeWorkload.source_factory_ref; called only after authenticated current source/host/purpose and scientific record admission",
        issuer_resolver="External competent custody CurrentDecisionResolver.resolve_current; no signer or issuance by U43",
        immutable_identity="Complete projection/catalog/descriptor/request/discovery/U/E_pre envelope hashed; independent resolver holds issued hash and exact expected job multiset",
        restore="Existing WG0P4 authenticated owner/fact/receipt checkpoint path; new ingress rejects bare caller prior_receipts",
        E41_input="Native QueryExecutionResult, ExactBoundedDiscoveryResult and complete source/target/condition/risk/weight refs; existing E41 v1.1 provider/composition additionally needs its separately admitted binding witness and model rule",
        W41_F43_input="Source-native structural facts, country/carrier and separately admitted F5/F6/F7 method scopes; empirical facts alone do not authorize transport or time comparison",
        P41_J42_input="E41-composed exact source-scope possibility evidence under P41 purposes; route probabilities/selection weights remain null absent separate grants; J42 untouched",
        A42_input="Same frozen 35/1890/151/101/AT denominator; only qualified original measured receipts may occupy source-science cells",
        N11_measured_delta=0,sourcefree_positive_file="evidence/native_sourcefree_execution.json",
        acceptance_cells_are_operations=False,independent_acceptance="PENDING_COMPETENT_REVIEW",source_or_actor_rights_issued=False)
    (R/"B43_A42_HANDOFF.json").write_text(json.dumps(payload,sort_keys=True,indent=2)+"\n")
    print(json.dumps(dict(waves=35,cells=1890,register=151,ledger=101,unmatched=len(unmatched),AT=len(at),original_scientific_workload="INCOMPLETE_PERMISSION_AND_NATIVE_INPUTS_REQUIRED")))


if __name__=="__main__":main()
