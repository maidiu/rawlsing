import hashlib
import json

from rawlsing_next.objective_consumer_bounded_evidence import (
    ClaimCeiling,
    EvidenceKind,
    EvidenceTier,
    ExactRef,
    OC01,
    OC02,
    OC03,
    OC04,
    OC05,
    PolicyInput,
    evaluate_oc01_pre553_source_local,
    evaluate_oc02_structural_admission,
    installation_manifest,
)
from rawlsing_next.tests.d07_bounded_loss_harness import run_harness


def _h(tag: str) -> str:
    return hashlib.sha256(tag.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:d07-repair:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _present(
    input_id: str,
    *,
    authority_tags: tuple[str, ...] = ("A",),
    required: bool = True,
    ceiling: ClaimCeiling = ClaimCeiling.SOURCE_LOCAL_STATISTIC,
    tier: EvidenceTier = EvidenceTier.SOURCE_LOCAL_CERTIFIED,
) -> PolicyInput:
    return PolicyInput(
        input_id=input_id,
        required=required,
        available=True,
        evidence_kind=EvidenceKind.EMPIRICAL,
        evidence_tier=tier,
        claim_ceiling=ceiling,
        producer_ref=_ref("PRODUCER", input_id),
        authority_refs=tuple(_ref("AUTHORITY", tag) for tag in authority_tags),
    )


def _missing(input_id: str, *, reason: str, required: bool = True) -> PolicyInput:
    return PolicyInput(
        input_id=input_id,
        required=required,
        available=False,
        evidence_kind=EvidenceKind.EMPIRICAL,
        evidence_tier=EvidenceTier.UNAVAILABLE,
        claim_ceiling=ClaimCeiling.SUPPORTED_COMPONENT_ONLY,
        omission_reason=reason,
    )


def test_d07_loss_deletion_harness_passes_all_current_consumer_cases():
    result = run_harness()
    assert result["status"] == "PASS"
    assert result["case_count"] == 12
    assert result["pass_count"] == 12
    assert result["fail_count"] == 0
    assert result["executed_policy_ids"] == [OC01, OC02]
    assert result["not_yet_applicable_policy_ids"] == [OC03, OC04, OC05]


def test_d07_installation_manifest_is_finite_and_exact():
    manifest = installation_manifest()
    assert [x["policy_id"] for x in manifest] == [OC01, OC02, OC03, OC04, OC05]
    assert [x["current_applicability"] for x in manifest] == [
        "APPLICABLE_CURRENT",
        "APPLICABLE_CURRENT",
        "NOT_YET_APPLICABLE",
        "NOT_YET_APPLICABLE",
        "NOT_YET_APPLICABLE",
    ]
    assert manifest[0]["consumer_seam"] == "rawlsing_next.pre553_empirical_query.execute_empirical_query"
    assert manifest[1]["consumer_seam"] == "rawlsing_next.pre553_structural_admission"
    assert all(x["consumer_seam"] is None for x in manifest[2:])


def test_d07_harness_result_is_deterministic():
    left = run_harness()
    right = run_harness()
    assert json.dumps(left, sort_keys=True, separators=(",", ":")) == json.dumps(
        right, sort_keys=True, separators=(",", ":")
    )


def test_d07_unavailable_omission_reason_is_receipt_and_hash_bearing():
    left = evaluate_oc01_pre553_source_local(
        operation_id="D07_REPAIR_OMISSION_REASON",
        inputs=(
            _present("survivor", required=False),
            _missing("required", reason="RISK_SET_UNAVAILABLE"),
        ),
        requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
    )
    right = evaluate_oc01_pre553_source_local(
        operation_id="D07_REPAIR_OMISSION_REASON",
        inputs=(
            _present("survivor", required=False),
            _missing("required", reason="SOURCE_SCOPE_UNAVAILABLE"),
        ),
        requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
    )
    assert left.receipt_hash != right.receipt_hash
    assert left.as_dict() != right.as_dict()
    assert left.as_dict()["unavailable_input_omission_reasons"] == [
        {"input_id": "required", "omission_reason": "RISK_SET_UNAVAILABLE"}
    ]
    assert right.as_dict()["unavailable_input_omission_reasons"] == [
        {"input_id": "required", "omission_reason": "SOURCE_SCOPE_UNAVAILABLE"}
    ]


def test_d07_selected_input_authority_refs_are_receipt_and_hash_bearing():
    left = evaluate_oc02_structural_admission(
        operation_id="D07_REPAIR_SELECTED_AUTHORITY",
        inputs=(
            _present(
                "relation",
                authority_tags=("AUTH-1",),
                ceiling=ClaimCeiling.STRUCTURAL_RELATION,
                tier=EvidenceTier.PARTIAL_AUTHORITY,
            ),
        ),
    )
    right = evaluate_oc02_structural_admission(
        operation_id="D07_REPAIR_SELECTED_AUTHORITY",
        inputs=(
            _present(
                "relation",
                authority_tags=("AUTH-2",),
                ceiling=ClaimCeiling.STRUCTURAL_RELATION,
                tier=EvidenceTier.PARTIAL_AUTHORITY,
            ),
        ),
    )
    assert left.receipt_hash != right.receipt_hash
    assert left.as_dict() != right.as_dict()
    assert left.as_dict()["selected_input_authority_refs"][0]["input_id"] == "relation"
    assert right.as_dict()["selected_input_authority_refs"][0]["input_id"] == "relation"
    assert left.as_dict()["selected_input_authority_refs"] != right.as_dict()["selected_input_authority_refs"]


def test_d07_replay_provenance_projection_is_canonical_and_association_bearing():
    left = evaluate_oc01_pre553_source_local(
        operation_id="D07_REPAIR_CANONICAL",
        inputs=(
            _present("a", authority_tags=("Z", "A")),
            _present("b", authority_tags=("B",)),
        ),
        requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
    )
    reordered = evaluate_oc01_pre553_source_local(
        operation_id="D07_REPAIR_CANONICAL",
        inputs=(
            _present("b", authority_tags=("B",)),
            _present("a", authority_tags=("A", "Z")),
        ),
        requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
    )
    assert left.receipt_hash == reordered.receipt_hash
    assert left.as_dict() == reordered.as_dict()

    swapped_authority_binding = evaluate_oc01_pre553_source_local(
        operation_id="D07_REPAIR_AUTHORITY_ASSOCIATION",
        inputs=(
            _present("a", authority_tags=("X",)),
            _present("b", authority_tags=("Y",)),
        ),
        requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
    )
    swapped_authority_binding_other = evaluate_oc01_pre553_source_local(
        operation_id="D07_REPAIR_AUTHORITY_ASSOCIATION",
        inputs=(
            _present("a", authority_tags=("Y",)),
            _present("b", authority_tags=("X",)),
        ),
        requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
    )
    assert swapped_authority_binding.receipt_hash != swapped_authority_binding_other.receipt_hash
    assert swapped_authority_binding.as_dict() != swapped_authority_binding_other.as_dict()

    swapped_omission_binding = evaluate_oc01_pre553_source_local(
        operation_id="D07_REPAIR_OMISSION_ASSOCIATION",
        inputs=(
            _present("survivor", required=False),
            _missing("a", reason="R1"),
            _missing("b", reason="R2", required=False),
        ),
        requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
    )
    swapped_omission_binding_other = evaluate_oc01_pre553_source_local(
        operation_id="D07_REPAIR_OMISSION_ASSOCIATION",
        inputs=(
            _present("survivor", required=False),
            _missing("a", reason="R2"),
            _missing("b", reason="R1", required=False),
        ),
        requested_claim_ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
    )
    assert swapped_omission_binding.receipt_hash != swapped_omission_binding_other.receipt_hash
    assert swapped_omission_binding.as_dict() != swapped_omission_binding_other.as_dict()
