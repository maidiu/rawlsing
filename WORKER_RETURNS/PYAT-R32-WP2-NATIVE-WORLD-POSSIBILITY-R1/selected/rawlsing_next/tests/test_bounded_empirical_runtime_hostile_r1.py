from decimal import Decimal
import hashlib

import pytest

import rawlsing_next.bounded_empirical_runtime as ber


def h(tag: str) -> str:
    return hashlib.sha256(tag.encode()).hexdigest()


def ref(kind: str, tag: str) -> ber.ExactRef:
    return ber.ExactRef(kind, f"urn:hostile:{kind.lower()}:{tag}", h(f"{kind}:{tag}"))


def channel(
    name="wvs7",
    coeff="0.4",
    ceiling=ber.ClaimCeiling.POPULATION_STATISTIC,
    required=False,
    fallback=None,
):
    return ber.EvidenceChannelPolicy(
        name, Decimal(coeff), ceiling, required, fallback
    )


def policy(*channels, allow_empty=False):
    return ber.DriverPolicy(
        "powerDistance",
        tuple(channels),
        allow_typed_no_numeric_driver=allow_empty,
        policy_version="HOSTILE_R1",
    )


def pop(channel_id="wvs7", value="0.61"):
    return ber.EvidenceContribution(
        "powerDistance",
        channel_id,
        ber.EvidenceTier.POPULATION_CERTIFIED,
        ber.ClaimCeiling.POPULATION_STATISTIC,
        Decimal(value),
        ref("SOURCE", channel_id),
        ref("POPULATION_AUTHORITY", channel_id),
        True,
        True,
    )


def model_prior(value="0.5"):
    return ber.FallbackRule(
        ber.FallbackKind.VERSIONED_MODEL_PRIOR,
        "prior-r1",
        Decimal(value),
        Decimal("0.25"),
        model_prior_version="RAWLSING_MODEL_PRIOR_R1",
    )


def test_h01_missing_numeric_zero_cannot_enter_as_unavailable():
    with pytest.raises(ber.MissingAsZeroError):
        ber.EvidenceContribution(
            "powerDistance", "wvs7", ber.EvidenceTier.UNAVAILABLE,
            ber.ClaimCeiling.POPULATION_STATISTIC, Decimal("0"), None
        )


def test_h02_missing_nonzero_numeric_cannot_enter_as_unavailable():
    with pytest.raises(ber.MissingAsZeroError):
        ber.assert_no_legacy_missing_zero("0.2", evidence_available=False)


def test_h03_legacy_zero_default_is_explicitly_rejected():
    with pytest.raises(ber.MissingAsZeroError):
        ber.assert_no_legacy_missing_zero(0, evidence_available=False)


def test_h04_source_local_cannot_satisfy_population_claim():
    weak = ber.EvidenceContribution(
        "powerDistance", "wvs7", ber.EvidenceTier.SOURCE_LOCAL_CERTIFIED,
        ber.ClaimCeiling.POPULATION_STATISTIC, Decimal("0.6"), ref("SOURCE", "weak")
    )
    with pytest.raises(ber.PopulationClaimAuthorityError):
        ber.resolve_driver_runtime(policy(channel()), [weak])


def test_h05_partial_cannot_satisfy_source_local_statistic():
    partial = ber.EvidenceContribution(
        "powerDistance", "ab", ber.EvidenceTier.PARTIAL_AUTHORITY,
        ber.ClaimCeiling.SOURCE_LOCAL_STATISTIC, Decimal("0.4"), ref("SOURCE", "partial")
    )
    with pytest.raises(ber.PopulationClaimAuthorityError):
        ber.resolve_driver_runtime(
            policy(channel("ab", ceiling=ber.ClaimCeiling.SOURCE_LOCAL_STATISTIC)),
            [partial],
        )


def test_h06_weaker_tier_cannot_smuggle_population_authority_ref():
    with pytest.raises(ber.PopulationClaimAuthorityError):
        ber.EvidenceContribution(
            "powerDistance", "wvs7", ber.EvidenceTier.SOURCE_LOCAL_CERTIFIED,
            ber.ClaimCeiling.SOURCE_LOCAL_STATISTIC, Decimal("0.6"), ref("SOURCE", "weak"),
            ref("POPULATION_AUTHORITY", "forged")
        )


def test_h07_population_tier_requires_population_authority_ref():
    with pytest.raises(ber.PopulationClaimAuthorityError):
        ber.EvidenceContribution(
            "powerDistance", "wvs7", ber.EvidenceTier.POPULATION_CERTIFIED,
            ber.ClaimCeiling.POPULATION_STATISTIC, Decimal("0.6"), ref("SOURCE", "pop"), None
        )


def test_h08_nearest_country_backfill_without_relation_authority_fails():
    with pytest.raises(ber.RelationAuthorityRequired):
        ber.FallbackRule(
            ber.FallbackKind.AUTHORIZED_BROADER_PRIOR,
            "nearest-country",
            Decimal("0.5"),
        )


def test_h09_alternate_source_without_relation_authority_fails():
    with pytest.raises(ber.RelationAuthorityRequired):
        ber.FallbackRule(
            ber.FallbackKind.AUTHORIZED_ALTERNATE_SOURCE,
            "alternate-family",
            Decimal("0.5"),
        )


def test_h10_model_prior_cannot_carry_relation_authority_as_empirical_camouflage():
    with pytest.raises(ber.BoundedEmpiricalRuntimeError):
        ber.FallbackRule(
            ber.FallbackKind.VERSIONED_MODEL_PRIOR,
            "model-prior",
            Decimal("0.5"),
            relation_authority_ref=ref("RELATION", "camouflage"),
            model_prior_version="P1",
        )


def test_h11_model_prior_must_be_versioned():
    with pytest.raises(ber.BoundedEmpiricalRuntimeError):
        ber.FallbackRule(
            ber.FallbackKind.VERSIONED_MODEL_PRIOR,
            "model-prior",
            Decimal("0.5"),
        )


def test_h12_missing_family_with_model_prior_is_runtime_admissible_but_zero_empirical_coverage():
    out = ber.resolve_driver_runtime(
        policy(channel(fallback=model_prior())), []
    )
    assert out.runtime_admissible
    assert out.coverage_receipt.empirical_contributing_channel_count == 0
    assert out.coverage_receipt.model_prior_channel_count == 1
    assert out.effective_contributions[0].contribution_class is ber.ContributionClass.MODEL_PRIOR
    assert out.effective_contributions[0].evidence_tier is None


def test_h13_surviving_channel_never_inherits_missing_channel_mass():
    p = policy(
        channel("wvs7", coeff="0.4", fallback=ber.FallbackRule(
            ber.FallbackKind.OMIT_CONTRIBUTION, "omit-wvs")),
        channel("evs", coeff="0.6"),
    )
    evs = pop("evs", "0.7")
    out = ber.resolve_driver_runtime(p, [evs])
    assert len(out.effective_contributions) == 1
    assert out.effective_contributions[0].channel_id == "evs"
    assert out.effective_contributions[0].coefficient == Decimal("0.6")
    assert out.coverage_receipt.empirical_coefficient_mass == Decimal("0.6")
    assert out.coverage_receipt.intended_coefficient_mass == Decimal("1")
    assert out.coverage_receipt.coefficient_reallocated is False


def test_h14_explicit_reallocation_request_is_rejected_even_if_mass_sums_to_original():
    with pytest.raises(ber.ImplicitRenormalizationError):
        ber.resolve_driver_runtime(
            policy(channel("wvs7", coeff="0.4"), channel("evs", coeff="0.6")),
            [pop("evs")],
            requested_coefficient_reallocation={"evs": Decimal("1")},
        )


def test_h15_unknown_channel_injection_is_rejected():
    with pytest.raises(ber.BoundedEmpiricalRuntimeError):
        ber.resolve_driver_runtime(policy(channel("wvs7")), [pop("evs")])


def test_h16_duplicate_channel_injection_is_rejected():
    p = policy(channel("wvs7"))
    with pytest.raises(ber.BoundedEmpiricalRuntimeError):
        ber.resolve_driver_runtime(p, [pop(), pop(value="0.62")])


def test_h17_all_empirical_absent_and_explicit_typed_omit_can_remain_admissible_without_scalar():
    p = policy(
        channel(fallback=ber.FallbackRule(
            ber.FallbackKind.OMIT_CONTRIBUTION, "omit")),
        allow_empty=True,
    )
    out = ber.resolve_driver_runtime(p, [])
    assert out.state is ber.DriverRuntimeState.ADMISSIBLE_TYPED_NO_NUMERIC_CONTRIBUTION
    assert not out.has_numeric_contribution
    with pytest.raises(ber.MissingAsZeroError):
        out.require_legacy_scalar()


def test_h18_nonfallbackable_required_channel_fails_at_exact_channel():
    out = ber.resolve_driver_runtime(policy(channel(required=True)), [])
    assert out.state is ber.DriverRuntimeState.BLOCKED_TERMINAL_REQUIREMENT
    assert out.block_reason == "NON_FALLBACKABLE_REQUIRED_CHANNELS_MISSING:wvs7"


def test_h19_receipt_identity_changes_on_relation_authority_mutation():
    def run(tag):
        fallback = ber.FallbackRule(
            ber.FallbackKind.AUTHORIZED_BROADER_PRIOR,
            "regional",
            Decimal("0.5"),
            relation_authority_ref=ref("RELATION", tag),
        )
        return ber.resolve_driver_runtime(policy(channel(fallback=fallback)), [])
    assert run("a").coverage_receipt.receipt_hash != run("b").coverage_receipt.receipt_hash


def test_h20_receipt_is_replay_deterministic_across_input_order():
    p = policy(channel("wvs7", coeff="0.4"), channel("evs", coeff="0.6"))
    left = ber.resolve_driver_runtime(p, [pop("wvs7", "0.55"), pop("evs", "0.65")])
    right = ber.resolve_driver_runtime(p, [pop("evs", "0.65"), pop("wvs7", "0.55")])
    assert left.as_dict() == right.as_dict()
    assert left.coverage_receipt.receipt_hash == right.coverage_receipt.receipt_hash


def test_h21_widen_uncertainty_does_not_create_numeric_evidence():
    p = policy(
        channel(fallback=ber.FallbackRule(
            ber.FallbackKind.WIDEN_UNCERTAINTY,
            "wide",
            uncertainty_widening=Decimal("0.5"),
        )),
        allow_empty=True,
    )
    out = ber.resolve_driver_runtime(p, [])
    assert out.runtime_admissible
    assert not out.effective_contributions
    assert out.total_uncertainty_widening == Decimal("0.5")
    assert out.coverage_receipt.empirical_contributing_channel_count == 0


def test_h22_runtime_contract_has_no_v3_or_pff_import_dependency():
    import inspect
    src = inspect.getsource(ber)
    forbidden = (
        "v3_adp010",
        "v3_psepf",
        "psychic_field",
        "render_bounded_expression",
        "m6_actor_safe_expression",
    )
    assert all(token not in src for token in forbidden)


def test_h23_mutating_evidence_tier_changes_receipt_or_fails_lawfully():
    p = policy(channel("wvs7", ceiling=ber.ClaimCeiling.SOURCE_LOCAL_STATISTIC))
    pop_item = ber.EvidenceContribution(
        "powerDistance", "wvs7", ber.EvidenceTier.POPULATION_CERTIFIED,
        ber.ClaimCeiling.SOURCE_LOCAL_STATISTIC, Decimal("0.5"), ref("SOURCE", "pop2"),
        ref("POPULATION_AUTHORITY", "pop2")
    )
    local_item = ber.EvidenceContribution(
        "powerDistance", "wvs7", ber.EvidenceTier.SOURCE_LOCAL_CERTIFIED,
        ber.ClaimCeiling.SOURCE_LOCAL_STATISTIC, Decimal("0.5"), ref("SOURCE", "local2")
    )
    a = ber.resolve_driver_runtime(p, [pop_item])
    b = ber.resolve_driver_runtime(p, [local_item])
    assert a.coverage_receipt.receipt_hash != b.coverage_receipt.receipt_hash


def test_h24_policy_mutation_changes_receipt_identity():
    a = ber.resolve_driver_runtime(policy(channel(coeff="0.4")), [pop()])
    b = ber.resolve_driver_runtime(policy(channel(coeff="0.5")), [pop()])
    assert a.coverage_receipt.policy_hash != b.coverage_receipt.policy_hash
    assert a.coverage_receipt.receipt_hash != b.coverage_receipt.receipt_hash
