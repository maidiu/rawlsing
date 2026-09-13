"""Finite W2-D07 loss/deletion harness for *current* objective consumers only."""
from __future__ import annotations

import hashlib
import json
from typing import Callable

from rawlsing_next.objective_consumer_bounded_evidence import (
    ClaimCeiling,
    DecisionState,
    EvidenceKind,
    EvidenceTier,
    ExactRef,
    MissingAsValueError,
    NonEmpiricalAuthorityRequired,
    NotYetApplicableConsumer,
    OC01,
    OC02,
    OC03,
    OC04,
    OC05,
    PolicyInput,
    RelationAuthorityRequired,
    RenormalizationForbidden,
    evaluate_current_consumer,
    evaluate_oc01_pre553_source_local,
    evaluate_oc02_structural_admission,
    installation_manifest,
)


def h(tag: str) -> str:
    return hashlib.sha256(tag.encode("utf-8")).hexdigest()


def ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:d07:{kind.lower()}:{tag}", h(f"{kind}:{tag}"))


def empirical(
    input_id: str,
    *,
    required: bool,
    tier: EvidenceTier = EvidenceTier.SOURCE_LOCAL_CERTIFIED,
    ceiling: ClaimCeiling = ClaimCeiling.SOURCE_LOCAL_STATISTIC,
    substitution: bool = False,
    relation: ExactRef | None = None,
) -> PolicyInput:
    return PolicyInput(
        input_id=input_id,
        required=required,
        available=True,
        evidence_kind=EvidenceKind.EMPIRICAL,
        evidence_tier=tier,
        claim_ceiling=ceiling,
        producer_ref=ref("PRODUCER", input_id),
        authority_refs=(ref("AUTHORITY", input_id),),
        substitution=substitution,
        relation_authority_ref=relation,
    )


def missing(input_id: str, *, required: bool, reason: str) -> PolicyInput:
    return PolicyInput(
        input_id=input_id,
        required=required,
        available=False,
        evidence_kind=EvidenceKind.EMPIRICAL,
        evidence_tier=EvidenceTier.UNAVAILABLE,
        claim_ceiling=ClaimCeiling.SUPPORTED_COMPONENT_ONLY,
        omission_reason=reason,
    )


def model_prior(input_id: str) -> PolicyInput:
    return PolicyInput(
        input_id=input_id,
        required=False,
        available=True,
        evidence_kind=EvidenceKind.NON_EMPIRICAL_MODEL,
        evidence_tier=EvidenceTier.PARTIAL_AUTHORITY,
        claim_ceiling=ClaimCeiling.SUPPORTED_COMPONENT_ONLY,
        producer_ref=ref("MODEL", input_id),
        authority_refs=(ref("MODEL_INPUT_AUTHORITY", input_id),),
        model_prior_version="D07_TEST_MODEL_PRIOR_R1",
        model_prior_authority_ref=ref("NON_EMPIRICAL_POLICY_AUTHORITY", input_id),
    )


def _case(case_id: str, policy_id: str, description: str, fn: Callable[[], dict]) -> dict:
    try:
        detail = fn()
        return {"case_id": case_id, "policy_id": policy_id, "description": description, "result": "PASS", **detail}
    except Exception as exc:  # pragma: no cover - only visible on harness failure
        return {
            "case_id": case_id,
            "policy_id": policy_id,
            "description": description,
            "result": "FAIL",
            "error_type": type(exc).__name__,
            "error": str(exc),
        }


def run_harness() -> dict:
    cases: list[dict] = []

    def l01():
        receipt = evaluate_oc01_pre553_source_local(
            operation_id="L01_SOURCE_LOCAL_SURVIVES_POPULATION_AUTHORITY_LOSS",
            inputs=(empirical("wvs_source_local", required=True),),
            requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
        )
        assert receipt.state is DecisionState.SUPPORTED_OBJECTIVE_RESULT
        assert receipt.positive_completion
        return {"state": receipt.state.value, "receipt_hash": receipt.receipt_hash}
    cases.append(_case("D07-L01", OC01, "source-local lawful service survives population-authority absence at source-local ceiling", l01))

    def l02():
        receipt = evaluate_oc01_pre553_source_local(
            operation_id="L02_SOURCE_LOCAL_CANNOT_SATISFY_POPULATION_CLAIM",
            inputs=(empirical("wvs_source_local", required=True),),
            requested_claim_ceiling=ClaimCeiling.POPULATION_STATISTIC,
        )
        assert receipt.state is DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE
        assert not receipt.positive_completion
        assert any(x.startswith("CLAIM_CEILING_NOT_AUTHORIZED") for x in receipt.refusal_reasons)
        return {"state": receipt.state.value, "receipt_hash": receipt.receipt_hash}
    cases.append(_case("D07-L02", OC01, "source-local evidence does not become population evidence", l02))

    def l03():
        survivor = empirical("independent_family", required=False)
        receipt = evaluate_oc01_pre553_source_local(
            operation_id="L03_REQUIRED_DETERMINANT_LOSS_LOCALIZES_FAILURE",
            inputs=(missing("required_risk_set", required=True, reason="RISK_SET_UNAVAILABLE"), survivor),
            requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
            partial_allowed=True,
        )
        assert receipt.state is DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE
        assert "independent_family" in receipt.selected_input_ids
        assert survivor.producer_ref in receipt.selected_producer_refs
        return {"state": receipt.state.value, "selected_input_ids": list(receipt.selected_input_ids), "receipt_hash": receipt.receipt_hash}
    cases.append(_case("D07-L03", OC01, "required determinant loss refuses affected operation while unrelated lawful family remains replayable", l03))

    def l04():
        try:
            empirical("alternate_source", required=True, substitution=True)
        except RelationAuthorityRequired:
            return {"state": "RELATION_AUTHORITY_REQUIRED"}
        raise AssertionError("alternate source without relation authority was accepted")
    cases.append(_case("D07-L04", OC01, "alternate/backfill without exact relation authority refuses", l04))

    def l05():
        receipt = evaluate_oc01_pre553_source_local(
            operation_id="L05_ALL_UNAVAILABLE_NOT_POSITIVE",
            inputs=(missing("source", required=True, reason="SOURCE_SCOPE_UNAVAILABLE"), missing("risk", required=True, reason="RISK_SET_UNAVAILABLE")),
            requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
        )
        assert receipt.state is DecisionState.ALL_UNAVAILABLE__NOT_POSITIVE_COMPLETION
        assert not receipt.positive_completion
        return {"state": receipt.state.value, "receipt_hash": receipt.receipt_hash}
    cases.append(_case("D07-L05", OC01, "all-unavailable never becomes successful zero/empty completion", l05))

    def l06():
        candidate = empirical("discovery_candidate", required=False, tier=EvidenceTier.PARTIAL_AUTHORITY, ceiling=ClaimCeiling.SUPPORTED_COMPONENT_ONLY)
        receipt = evaluate_oc02_structural_admission(
            operation_id="L06_VALIDATION_OR_ADMISSION_MISSING",
            inputs=(candidate, missing("structural_admission_authority", required=True, reason="MISSING_STRUCTURAL_ADMISSION_AUTHORITY")),
        )
        assert receipt.state is DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE
        assert not receipt.positive_completion
        assert "structural_admission_authority" in receipt.missing_required_input_ids
        return {"state": receipt.state.value, "receipt_hash": receipt.receipt_hash}
    cases.append(_case("D07-L06", OC02, "discovery support survives as lineage but cannot promote without structural-admission authority", l06))

    def l07():
        same_source = empirical("same_source_validated_relation", required=False, tier=EvidenceTier.PARTIAL_AUTHORITY, ceiling=ClaimCeiling.SUPPORTED_COMPONENT_ONLY)
        receipt = evaluate_oc02_structural_admission(
            operation_id="L07_COMPARABILITY_LOSS",
            inputs=(same_source, missing("cross_source_comparability", required=True, reason="COMPARABILITY_AUTHORITY_UNAVAILABLE")),
        )
        assert receipt.state is DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE
        assert receipt.coefficient_reallocated is False
        return {"state": receipt.state.value, "receipt_hash": receipt.receipt_hash}
    cases.append(_case("D07-L07", OC02, "cross-source comparability loss blocks promotion without renormalizing surviving support", l07))

    def l08():
        receipt = evaluate_oc02_structural_admission(
            operation_id="L08_POSITIVE_STRUCTURAL_ADMISSION_BOUND",
            inputs=(empirical("admitted_relation", required=True, tier=EvidenceTier.PARTIAL_AUTHORITY, ceiling=ClaimCeiling.STRUCTURAL_RELATION),),
        )
        assert receipt.state is DecisionState.SUPPORTED_OBJECTIVE_RESULT
        assert receipt.positive_completion
        return {"state": receipt.state.value, "receipt_hash": receipt.receipt_hash}
    cases.append(_case("D07-L08", OC02, "current structural-admission seam can produce a positive receipt only at its exact structural ceiling", l08))

    def l09():
        try:
            PolicyInput(
                input_id="unauthorized_prior",
                required=False,
                available=True,
                evidence_kind=EvidenceKind.NON_EMPIRICAL_MODEL,
                evidence_tier=EvidenceTier.PARTIAL_AUTHORITY,
                claim_ceiling=ClaimCeiling.SUPPORTED_COMPONENT_ONLY,
                producer_ref=ref("MODEL", "unauthorized_prior"),
                authority_refs=(ref("MODEL_INPUT_AUTHORITY", "unauthorized_prior"),),
                model_prior_version="R1",
            )
        except NonEmpiricalAuthorityRequired:
            pass
        else:
            raise AssertionError("model prior without distinct non-empirical authority was accepted")
        receipt = evaluate_oc01_pre553_source_local(
            operation_id="L09_AUTHORIZED_MODEL_PRIOR_NOT_EMPIRICAL_COMPLETION",
            inputs=(model_prior("authorized_prior"), missing("empirical_source", required=False, reason="SOURCE_UNAVAILABLE")),
            requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
        )
        assert receipt.state is DecisionState.ALL_UNAVAILABLE__NOT_POSITIVE_COMPLETION
        assert not receipt.positive_completion
        return {"state": receipt.state.value, "non_empirical_input_ids": list(receipt.non_empirical_input_ids), "receipt_hash": receipt.receipt_hash}
    cases.append(_case("D07-L09", OC01, "model prior is separately authorized/non-empirical and cannot create empirical positive completion", l09))

    def l10():
        try:
            evaluate_oc01_pre553_source_local(
                operation_id="L10_RENORMALIZATION_FORBIDDEN",
                inputs=(empirical("survivor", required=True),),
                requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
                renormalization_requested=True,
            )
        except RenormalizationForbidden:
            return {"state": "RENORMALIZATION_FORBIDDEN"}
        raise AssertionError("renormalization was accepted")
    cases.append(_case("D07-L10", OC01, "coefficient/confidence/semantic-scope renormalization refuses", l10))

    def l11():
        residuals = []
        for policy in (OC03, OC04, OC05):
            try:
                evaluate_current_consumer(
                    policy_id=policy,
                    operation_id="MUST_NOT_SIMULATE",
                    inputs=(empirical("fake", required=True),),
                    requested_claim_ceiling=ClaimCeiling.OBJECTIVE_FACT,
                    partial_allowed=False,
                )
            except NotYetApplicableConsumer:
                residuals.append(policy)
            else:
                raise AssertionError(f"future consumer {policy} was simulated")
        assert residuals == [OC03, OC04, OC05]
        return {"state": "NOT_YET_APPLICABLE_ENFORCED", "policies": residuals}
    cases.append(_case("D07-L11", "OC03/OC04/OC05", "future consumers are explicit typed residuals, not synthetic whole-system coverage", l11))

    def l12():
        receipt = evaluate_oc01_pre553_source_local(
            operation_id="L12_OPTIONAL_LOCAL_LOSS_SURVIVES",
            inputs=(empirical("family_a", required=True), missing("family_b", required=False, reason="LOCAL_FAMILY_LOSS")),
            requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
            partial_allowed=True,
        )
        assert receipt.state is DecisionState.PARTIAL_OBJECTIVE_RESULT
        assert receipt.positive_completion
        assert receipt.selected_input_ids == ("family_a",)
        assert receipt.omitted_optional_input_ids == ("family_b",)
        return {"state": receipt.state.value, "selected_input_ids": list(receipt.selected_input_ids), "omitted_optional_input_ids": list(receipt.omitted_optional_input_ids), "receipt_hash": receipt.receipt_hash}
    cases.append(_case("D07-L12", OC01, "optional local loss preserves unrelated lawful objective service without scope transfer", l12))

    failed = [x for x in cases if x["result"] != "PASS"]
    return {
        "schema": "W2_D07_BOUNDED_LOSS_DELETION_RESULTS_R1",
        "status": "PASS" if not failed else "FAIL",
        "executed_policy_ids": [OC01, OC02],
        "not_yet_applicable_policy_ids": [OC03, OC04, OC05],
        "case_count": len(cases),
        "pass_count": len(cases) - len(failed),
        "fail_count": len(failed),
        "installation_manifest": list(installation_manifest()),
        "cases": cases,
    }


if __name__ == "__main__":
    print(json.dumps(run_harness(), indent=2, sort_keys=True))
