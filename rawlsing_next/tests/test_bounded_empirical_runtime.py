from decimal import Decimal
import hashlib

import pytest

from rawlsing_next.bounded_empirical_runtime import (
    ClaimCeiling,
    ContributionClass,
    DriverPolicy,
    DriverRuntimeState,
    EvidenceChannelPolicy,
    EvidenceContribution,
    EvidenceTier,
    ExactRef,
    FallbackKind,
    FallbackRule,
    ImplicitRenormalizationError,
    MissingAsZeroError,
    PopulationClaimAuthorityError,
    RelationAuthorityRequired,
    assert_no_legacy_missing_zero,
    resolve_driver_runtime,
)


def h(tag):
    return hashlib.sha256(tag.encode()).hexdigest()


def ref(kind, tag):
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", h(f"{kind}:{tag}"))


def pop(driver="collectivism", channel="wvs7"):
    return EvidenceContribution(
        driver,
        channel,
        EvidenceTier.POPULATION_CERTIFIED,
        ClaimCeiling.POPULATION_STATISTIC,
        Decimal("0.63"),
        ref("SOURCE", f"{driver}-{channel}"),
        ref("POP_AUTH", f"{driver}-{channel}"),
        True,
        True,
    )


def policy(*channels, driver="collectivism", allow_empty=False):
    return DriverPolicy(
        driver,
        tuple(channels),
        allow_typed_no_numeric_driver=allow_empty,
    )


def ch(
    channel_id="wvs7",
    *,
    coeff="0.4",
    ceiling=ClaimCeiling.POPULATION_STATISTIC,
    required=False,
    fallback=None,
):
    return EvidenceChannelPolicy(
        channel_id,
        Decimal(coeff),
        ceiling,
        required,
        fallback,
    )


def model_prior(value="0.5", *, widening="0.3"):
    return FallbackRule(
        FallbackKind.VERSIONED_MODEL_PRIOR,
        "GLOBAL_DRIVER_PRIOR",
        Decimal(value),
        Decimal(widening),
        model_prior_version="MODEL_PRIOR_R1",
    )


def test_01_population_certified_wvs_is_accepted_without_reallocation():
    out = resolve_driver_runtime(policy(ch()), [pop()])
    assert (
        out.state
        is DriverRuntimeState.ADMISSIBLE_WITH_NUMERIC_CONTRIBUTIONS
    )
    assert out.coverage_receipt.empirical_contributing_channel_count == 1
    assert out.coverage_receipt.coefficient_reallocated is False
    assert out.effective_contributions[0].coefficient == Decimal("0.4")


def test_02_missing_wvs_can_use_explicit_versioned_nonempirical_model_prior():
    out = resolve_driver_runtime(policy(ch(fallback=model_prior())), [])
    assert out.runtime_admissible
    contribution = out.effective_contributions[0]
    assert contribution.contribution_class is ContributionClass.MODEL_PRIOR
    assert contribution.evidence_tier is None
    assert contribution.model_prior_version == "MODEL_PRIOR_R1"
    assert out.coverage_receipt.empirical_contributing_channel_count == 0
    assert out.coverage_receipt.model_prior_channel_count == 1


def test_03_entire_family_absent_can_be_omitted_when_driver_allows_typed_absence():
    p = policy(
        ch(
            fallback=FallbackRule(
                FallbackKind.OMIT_CONTRIBUTION,
                "omit-wvs",
            )
        ),
        allow_empty=True,
    )
    out = resolve_driver_runtime(p, [])
    assert (
        out.state
        is DriverRuntimeState.ADMISSIBLE_TYPED_NO_NUMERIC_CONTRIBUTION
    )
    assert not out.effective_contributions


def test_04_multiple_families_partial_absence_preserves_survivor_coefficients():
    p = policy(
        ch(
            "wvs7",
            coeff="0.4",
            fallback=model_prior("0.5"),
        ),
        ch(
            "evs",
            coeff="0.3",
            fallback=FallbackRule(
                FallbackKind.WIDEN_UNCERTAINTY,
                "evs-wide",
                uncertainty_widening=Decimal("0.2"),
            ),
        ),
        ch(
            "ab",
            coeff="0.3",
            ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
            fallback=FallbackRule(
                FallbackKind.OMIT_CONTRIBUTION,
                "ab-omit",
            ),
        ),
    )
    ab = EvidenceContribution(
        "collectivism",
        "ab",
        EvidenceTier.SOURCE_LOCAL_CERTIFIED,
        ClaimCeiling.SOURCE_LOCAL_STATISTIC,
        Decimal("0.4"),
        ref("SOURCE", "ab"),
    )
    out = resolve_driver_runtime(p, [ab])
    coefficients = {
        item.channel_id: item.coefficient
        for item in out.effective_contributions
    }
    assert coefficients == {
        "ab": Decimal("0.3"),
        "wvs7": Decimal("0.4"),
    }
    assert out.coverage_receipt.coefficient_reallocated is False


def test_05_source_local_cannot_masquerade_as_population_evidence():
    item = EvidenceContribution(
        "collectivism",
        "wvs7",
        EvidenceTier.SOURCE_LOCAL_CERTIFIED,
        ClaimCeiling.POPULATION_STATISTIC,
        Decimal("0.6"),
        ref("SOURCE", "wvs-local"),
    )
    with pytest.raises(PopulationClaimAuthorityError):
        resolve_driver_runtime(policy(ch()), [item])


def test_06_missing_channel_numeric_zero_is_rejected():
    with pytest.raises(MissingAsZeroError):
        EvidenceContribution(
            "collectivism",
            "wvs7",
            EvidenceTier.UNAVAILABLE,
            ClaimCeiling.POPULATION_STATISTIC,
            Decimal("0"),
            None,
        )
    with pytest.raises(MissingAsZeroError):
        assert_no_legacy_missing_zero(0, evidence_available=False)


def test_07_implicit_renormalization_is_rejected():
    with pytest.raises(ImplicitRenormalizationError):
        resolve_driver_runtime(
            policy(ch()),
            [pop()],
            requested_coefficient_reallocation={
                "wvs7": Decimal("1"),
            },
        )


def test_08_broader_or_alternate_source_requires_exact_relation_authority():
    with pytest.raises(RelationAuthorityRequired):
        FallbackRule(
            FallbackKind.AUTHORIZED_BROADER_PRIOR,
            "region-backfill",
            Decimal("0.5"),
        )


def test_09_authorized_broader_prior_with_relation_authority_is_accepted_and_bounded_source_local():
    relation = ref("RELATION_AUTHORITY", "country-to-region")
    fallback = FallbackRule(
        FallbackKind.AUTHORIZED_BROADER_PRIOR,
        "region-backfill",
        Decimal("0.5"),
        Decimal("0.15"),
        relation_authority_ref=relation,
    )
    out = resolve_driver_runtime(policy(ch(fallback=fallback)), [])
    contribution = out.effective_contributions[0]
    assert contribution.contribution_class is ContributionClass.EMPIRICAL
    assert (
        contribution.evidence_tier
        is EvidenceTier.SOURCE_LOCAL_CERTIFIED
    )
    assert (
        contribution.claim_ceiling
        is ClaimCeiling.SOURCE_LOCAL_STATISTIC
    )
    assert contribution.relation_authority_ref == relation


def test_10_weight_estimand_unavailable_does_not_widen_source_local_ceiling():
    p = policy(
        ch(
            "ab",
            ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
        )
    )
    item = EvidenceContribution(
        "collectivism",
        "ab",
        EvidenceTier.SOURCE_LOCAL_CERTIFIED,
        ClaimCeiling.SOURCE_LOCAL_STATISTIC,
        Decimal("0.45"),
        ref("SOURCE", "ab"),
        weight_authorized=False,
        estimand_authorized=False,
    )
    out = resolve_driver_runtime(p, [item])
    assert (
        out.effective_contributions[0].claim_ceiling
        is ClaimCeiling.SOURCE_LOCAL_STATISTIC
    )
    assert (
        out.effective_contributions[0].evidence_tier
        is EvidenceTier.SOURCE_LOCAL_CERTIFIED
    )


def test_11_zero_empirical_coverage_can_still_be_runtime_admissible_with_model_prior():
    p = policy(
        ch(
            "wvs7",
            coeff="0.5",
            fallback=model_prior("0.4"),
        ),
        ch(
            "evs",
            coeff="0.5",
            fallback=model_prior("0.6"),
        ),
    )
    out = resolve_driver_runtime(p, [])
    assert out.runtime_admissible
    assert out.coverage_receipt.empirical_contributing_channel_count == 0
    assert out.coverage_receipt.model_prior_channel_count == 2
    assert all(
        item.contribution_class is ContributionClass.MODEL_PRIOR
        for item in out.effective_contributions
    )


def test_12_nonfallbackable_required_channel_fails_exactly():
    out = resolve_driver_runtime(policy(ch(required=True)), [])
    assert (
        out.state
        is DriverRuntimeState.BLOCKED_TERMINAL_REQUIREMENT
    )
    assert (
        out.block_reason
        == "NON_FALLBACKABLE_REQUIRED_CHANNELS_MISSING:wvs7"
    )


def test_13_coverage_receipt_is_deterministic_under_input_order():
    p = policy(
        ch("wvs7", coeff="0.4"),
        ch(
            "ab",
            coeff="0.6",
            ceiling=ClaimCeiling.SOURCE_LOCAL_STATISTIC,
        ),
    )
    wvs = pop()
    ab = EvidenceContribution(
        "collectivism",
        "ab",
        EvidenceTier.SOURCE_LOCAL_CERTIFIED,
        ClaimCeiling.SOURCE_LOCAL_STATISTIC,
        Decimal("0.5"),
        ref("SOURCE", "ab"),
    )
    left = resolve_driver_runtime(p, [wvs, ab])
    right = resolve_driver_runtime(p, [ab, wvs])
    assert (
        left.coverage_receipt.receipt_hash
        == right.coverage_receipt.receipt_hash
    )
    assert left.as_dict() == right.as_dict()


def test_14_mutating_tier_fallback_or_relation_changes_receipt_identity():
    base = resolve_driver_runtime(
        policy(ch(fallback=model_prior("0.5"))),
        [],
    )
    changed_prior = resolve_driver_runtime(
        policy(ch(fallback=model_prior("0.6"))),
        [],
    )
    relation1 = ref("RELATION_AUTHORITY", "r1")
    relation2 = ref("RELATION_AUTHORITY", "r2")
    first = FallbackRule(
        FallbackKind.AUTHORIZED_BROADER_PRIOR,
        "region",
        Decimal("0.5"),
        relation_authority_ref=relation1,
    )
    second = FallbackRule(
        FallbackKind.AUTHORIZED_BROADER_PRIOR,
        "region",
        Decimal("0.5"),
        relation_authority_ref=relation2,
    )
    r1 = resolve_driver_runtime(policy(ch(fallback=first)), [])
    r2 = resolve_driver_runtime(policy(ch(fallback=second)), [])
    assert (
        base.coverage_receipt.receipt_hash
        != changed_prior.coverage_receipt.receipt_hash
    )
    assert (
        r1.coverage_receipt.receipt_hash
        != r2.coverage_receipt.receipt_hash
    )


def test_15_typed_no_numeric_envelope_cannot_be_coerced_to_legacy_zero():
    p = policy(
        ch(
            fallback=FallbackRule(
                FallbackKind.OMIT_CONTRIBUTION,
                "omit",
            )
        ),
        allow_empty=True,
    )
    out = resolve_driver_runtime(p, [])
    with pytest.raises(MissingAsZeroError):
        out.require_legacy_scalar()


def test_16_widen_uncertainty_without_numeric_fill_is_explicit_and_deterministic():
    fallback = FallbackRule(
        FallbackKind.WIDEN_UNCERTAINTY,
        "wide",
        uncertainty_widening=Decimal("0.25"),
    )
    out = resolve_driver_runtime(
        policy(
            ch(fallback=fallback),
            allow_empty=True,
        ),
        [],
    )
    assert out.runtime_admissible
    assert not out.effective_contributions
    assert out.total_uncertainty_widening == Decimal("0.25")
    assert (
        out.coverage_receipt.total_uncertainty_widening
        == Decimal("0.25")
    )
