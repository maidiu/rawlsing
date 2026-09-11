import hashlib
from dataclasses import fields

import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.sdtf_r4_mechanism_rule_authority_binding import (
    AuthorityCeilingBinding,
    AuthorityDisposition,
    AuthorityRole,
    MechanismClass,
    MechanismRuleAuthorityBinding,
    MechanismRuleIdentity,
    R4MechanismRuleAuthorityBindingError,
    RuleCurrentness,
    RuleNotCurrentError,
    RuleTraceBinding,
    RuleValueMode,
    require_current_rule_admission,
)


def _h(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:test:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def _aref(tag: str, version: str = "1.0.0") -> AuthorityRef:
    return AuthorityRef(f"AUTH-{tag}", version, _h(f"AUTH:{tag}:{version}"))


def _authority_binding(
    role: AuthorityRole,
    *,
    bound: bool = True,
    tag: str | None = None,
) -> AuthorityCeilingBinding:
    tag = tag or role.value.lower()
    if bound:
        return AuthorityCeilingBinding(
            role=role,
            disposition=AuthorityDisposition.BOUND,
            scope_or_na_ref=_ref("AUTHORITY_SCOPE", tag),
            authority_ref=_aref(tag),
            current_selection_evidence_refs=(
                _ref("AUTHORITY_CURRENT_SELECTION", tag),
            ),
        )
    return AuthorityCeilingBinding(
        role=role,
        disposition=AuthorityDisposition.NOT_APPLICABLE,
        scope_or_na_ref=_ref("AUTHORITY_NOT_APPLICABLE", tag),
        authority_ref=None,
        current_selection_evidence_refs=(),
    )


def _trace(tag: str = "base") -> RuleTraceBinding:
    return RuleTraceBinding(
        source_refs=(_ref("SOURCE", f"{tag}-s1"),),
        claim_refs=(_ref("CLAIM", f"{tag}-c1"),),
        evidence_status_ref=_ref("EVIDENCE_STATUS", tag),
        normalized_mechanism_ref=_ref("NORMALIZED_MECHANISM", tag),
        permitted_rule_shape_ref=_ref("PERMITTED_RULE_SHAPE", tag),
        required_objective_inputs_bindings_ref=_ref("REQUIRED_BINDINGS", tag),
        qualification_realization_proof_contract_ref=_ref("PROOF_CONTRACT", tag),
        temporal_currentness_contract_ref=_ref("TEMPORAL_CURRENTNESS", tag),
        portability_ceiling_ref=_ref("PORTABILITY_CEILING", tag),
        currentness_ceiling_ref=_ref("CURRENTNESS_CEILING", tag),
        historical_institutional_validity_ref=_ref("HISTORICAL_VALIDITY", tag),
        negative_ceiling_ref=_ref("NEGATIVE_CEILING", tag),
        v3_stop_boundary_ref=_ref("V3_STOP_BOUNDARY", tag),
    )


def _binding(
    *,
    tag: str = "base",
    mechanism_classes=(
        MechanismClass.P1_MATERIAL_ACCESS_DEPENDENCY,
        MechanismClass.P5_COUNTERPART_CHANNEL_RELATION,
    ),
    value_mode=RuleValueMode.NONNUMERIC,
    currentness=RuleCurrentness.CURRENT_ACCEPTED,
    calibration=None,
    rule_owner=None,
    causal_use=None,
    measurement=None,
    estimand=None,
    identification=None,
    current_selection_refs=None,
    noncurrent_refs=None,
    trace=None,
) -> MechanismRuleAuthorityBinding:
    if calibration is None:
        calibration = _authority_binding(
            AuthorityRole.CALIBRATION,
            bound=value_mode == RuleValueMode.NUMERIC,
            tag=f"{tag}-calibration",
        )
    if current_selection_refs is None:
        if currentness == RuleCurrentness.CURRENT_ACCEPTED:
            current_selection_refs = (_ref("RULE_CURRENT_SELECTION", tag),)
        elif currentness == RuleCurrentness.HISTORICAL_NONCURRENT:
            current_selection_refs = (_ref("RULE_CURRENT_SELECTION", tag),)
        else:
            current_selection_refs = ()
    if noncurrent_refs is None:
        noncurrent_refs = (
            (_ref("RULE_NONCURRENT_DISPOSITION", tag),)
            if currentness == RuleCurrentness.HISTORICAL_NONCURRENT
            else ()
        )
    return MechanismRuleAuthorityBinding(
        rule_identity=MechanismRuleIdentity(
            f"RULE-{tag}",
            "1.0.0",
            _h(f"rule-content:{tag}"),
        ),
        mechanism_classes=tuple(mechanism_classes),
        constitution_current_selection_ref=_ref(
            "R4_CONSTITUTION_CURRENT_SELECTION", "hq-adoption"
        ),
        trace=trace or _trace(tag),
        rule_owner=rule_owner
        or _authority_binding(AuthorityRole.RULE_OWNER, tag=f"{tag}-owner"),
        measurement_authority=measurement
        or _authority_binding(
            AuthorityRole.MEASUREMENT, bound=False, tag=f"{tag}-measurement"
        ),
        estimand_authority=estimand
        or _authority_binding(
            AuthorityRole.ESTIMAND, bound=False, tag=f"{tag}-estimand"
        ),
        identification_authority=identification
        or _authority_binding(
            AuthorityRole.IDENTIFICATION, bound=False, tag=f"{tag}-identification"
        ),
        causal_use_authority=causal_use
        or _authority_binding(AuthorityRole.CAUSAL_USE, tag=f"{tag}-causal"),
        calibration_authority=calibration,
        value_mode=value_mode,
        rule_currentness=currentness,
        rule_current_selection_evidence_refs=tuple(current_selection_refs),
        rule_noncurrent_disposition_refs=tuple(noncurrent_refs),
    )


def test_current_nonnumeric_rule_binding_has_exact_g1_g6_trace_and_no_values():
    binding = _binding()
    assert require_current_rule_admission(binding) is binding
    assert binding.rule_identity.rule_version == "1.0.0"
    assert binding.calibration_authority.disposition is AuthorityDisposition.NOT_APPLICABLE
    assert binding.causal_use_authority.disposition is AuthorityDisposition.BOUND
    assert binding.trace.source_refs
    assert binding.trace.claim_refs
    assert binding.trace.evidence_status_ref
    assert binding.trace.normalized_mechanism_ref
    material = binding.as_material()
    assert material["authority_law"]["constitution_current_does_not_imply_rule_current"] is True
    assert material["authority_law"]["source_citation_does_not_imply_causal_use"] is True
    assert "coefficient" not in material
    assert "probability" not in material
    assert "threshold" not in material
    assert "actor_ref" not in material


def test_constitution_currentness_does_not_promote_candidate_rule_currentness():
    candidate = _binding(
        tag="candidate",
        currentness=RuleCurrentness.CANDIDATE_NOT_CURRENT,
        current_selection_refs=(),
    )
    assert candidate.constitution_current_selection_ref
    with pytest.raises(RuleNotCurrentError, match="constitution currentness"):
        require_current_rule_admission(candidate)


def test_current_rule_requires_its_own_explicit_current_selection_evidence():
    with pytest.raises(
        R4MechanismRuleAuthorityBindingError,
        match="CURRENT_ACCEPTED rule requires explicit rule current-selection evidence",
    ):
        _binding(tag="no-selection", current_selection_refs=())


def test_historical_rule_requires_prior_current_and_noncurrent_disposition_proof():
    historical = _binding(
        tag="history",
        currentness=RuleCurrentness.HISTORICAL_NONCURRENT,
    )
    assert historical.rule_current_selection_evidence_refs
    assert historical.rule_noncurrent_disposition_refs
    with pytest.raises(RuleNotCurrentError):
        require_current_rule_admission(historical)
    with pytest.raises(R4MechanismRuleAuthorityBindingError):
        _binding(
            tag="history-missing-close",
            currentness=RuleCurrentness.HISTORICAL_NONCURRENT,
            noncurrent_refs=(),
        )


def test_rule_version_is_exact_and_rejects_mutable_or_range_selectors():
    for version in ("LATEST", "SEMVER:1", "^1.0.0", ">=1.0.0", "1.*"):
        with pytest.raises(R4MechanismRuleAuthorityBindingError):
            MechanismRuleIdentity("R", version, _h(version))


def test_rule_content_identity_requires_lowercase_sha256():
    with pytest.raises(
        R4MechanismRuleAuthorityBindingError,
        match="lowercase sha256",
    ):
        MechanismRuleIdentity("R", "1.0.0", "not-a-sha")


def test_only_exact_p1_p5_classes_are_accepted_and_p6_is_rejected():
    with pytest.raises(
        R4MechanismRuleAuthorityBindingError,
        match="exact P1-P5",
    ):
        _binding(tag="p6", mechanism_classes=("P6 invented",))


def test_mechanism_composition_is_canonical_but_duplicate_classes_fail():
    forward = _binding(
        tag="composition",
        mechanism_classes=(
            MechanismClass.P1_MATERIAL_ACCESS_DEPENDENCY,
            MechanismClass.P5_COUNTERPART_CHANNEL_RELATION,
        ),
    )
    reverse = _binding(
        tag="composition",
        mechanism_classes=(
            MechanismClass.P5_COUNTERPART_CHANNEL_RELATION,
            MechanismClass.P1_MATERIAL_ACCESS_DEPENDENCY,
        ),
    )
    assert forward.mechanism_class_composition_ref == reverse.mechanism_class_composition_ref
    assert forward.binding_hash == reverse.binding_hash

    with pytest.raises(
        R4MechanismRuleAuthorityBindingError,
        match="duplicates",
    ):
        _binding(
            tag="dup",
            mechanism_classes=(
                MechanismClass.P1_MATERIAL_ACCESS_DEPENDENCY,
                MechanismClass.P1_MATERIAL_ACCESS_DEPENDENCY,
            ),
        )


def test_source_claim_evidence_and_normalized_mechanism_trace_cannot_be_omitted():
    with pytest.raises(R4MechanismRuleAuthorityBindingError, match="source_refs"):
        RuleTraceBinding(
            source_refs=(),
            claim_refs=(_ref("CLAIM", "c"),),
            evidence_status_ref=_ref("EVIDENCE_STATUS", "x"),
            normalized_mechanism_ref=_ref("NORMALIZED_MECHANISM", "x"),
            permitted_rule_shape_ref=_ref("PERMITTED_RULE_SHAPE", "x"),
            required_objective_inputs_bindings_ref=_ref("REQUIRED_BINDINGS", "x"),
            qualification_realization_proof_contract_ref=_ref("PROOF_CONTRACT", "x"),
            temporal_currentness_contract_ref=_ref("TEMPORAL_CURRENTNESS", "x"),
            portability_ceiling_ref=_ref("PORTABILITY_CEILING", "x"),
            currentness_ceiling_ref=_ref("CURRENTNESS_CEILING", "x"),
            historical_institutional_validity_ref=_ref("HISTORICAL_VALIDITY", "x"),
            negative_ceiling_ref=_ref("NEGATIVE_CEILING", "x"),
            v3_stop_boundary_ref=_ref("V3_STOP_BOUNDARY", "x"),
        )


def test_rule_owner_is_mandatory_bound_exact_authority():
    owner_na = _authority_binding(AuthorityRole.RULE_OWNER, bound=False, tag="owner-na")
    with pytest.raises(
        R4MechanismRuleAuthorityBindingError,
        match="rule owner authority is mandatory",
    ):
        _binding(tag="owner-na", rule_owner=owner_na)


def test_causal_use_is_mandatory_and_not_inferred_from_source_citation():
    causal_na = _authority_binding(AuthorityRole.CAUSAL_USE, bound=False, tag="causal-na")
    with pytest.raises(
        R4MechanismRuleAuthorityBindingError,
        match="causal-use authority is mandatory",
    ):
        _binding(tag="causal-na", causal_use=causal_na)


def test_bound_authority_requires_exact_current_selection_and_rejects_latest():
    with pytest.raises(
        R4MechanismRuleAuthorityBindingError,
        match="current-selection evidence",
    ):
        AuthorityCeilingBinding(
            role=AuthorityRole.CAUSAL_USE,
            disposition=AuthorityDisposition.BOUND,
            scope_or_na_ref=_ref("AUTHORITY_SCOPE", "causal"),
            authority_ref=_aref("causal"),
            current_selection_evidence_refs=(),
        )

    latest = AuthorityRef("AUTH-latest", "LATEST", _h("latest"))
    with pytest.raises(R4MechanismRuleAuthorityBindingError):
        AuthorityCeilingBinding(
            role=AuthorityRole.CAUSAL_USE,
            disposition=AuthorityDisposition.BOUND,
            scope_or_na_ref=_ref("AUTHORITY_SCOPE", "causal-latest"),
            authority_ref=latest,
            current_selection_evidence_refs=(
                _ref("AUTHORITY_CURRENT_SELECTION", "causal-latest"),
            ),
        )


def test_numeric_rule_requires_bound_calibration_authority():
    calibration_na = _authority_binding(
        AuthorityRole.CALIBRATION, bound=False, tag="calibration-na"
    )
    with pytest.raises(
        R4MechanismRuleAuthorityBindingError,
        match="numeric rule shape requires exact current calibration authority",
    ):
        _binding(
            tag="numeric-no-calibration",
            value_mode=RuleValueMode.NUMERIC,
            calibration=calibration_na,
        )

    numeric = _binding(tag="numeric", value_mode=RuleValueMode.NUMERIC)
    assert numeric.calibration_authority.disposition is AuthorityDisposition.BOUND


def test_nonnumeric_rule_requires_explicit_calibration_not_applicable():
    calibration_bound = _authority_binding(
        AuthorityRole.CALIBRATION, bound=True, tag="unneeded-calibration"
    )
    with pytest.raises(
        R4MechanismRuleAuthorityBindingError,
        match="nonnumeric rule shape requires explicit calibration NOT_APPLICABLE",
    ):
        _binding(
            tag="nonnumeric-with-calibration",
            value_mode=RuleValueMode.NONNUMERIC,
            calibration=calibration_bound,
        )


def test_measurement_estimand_identification_are_explicit_bound_or_na_not_silent():
    binding = _binding()
    assert binding.measurement_authority.disposition is AuthorityDisposition.NOT_APPLICABLE
    assert binding.estimand_authority.disposition is AuthorityDisposition.NOT_APPLICABLE
    assert binding.identification_authority.disposition is AuthorityDisposition.NOT_APPLICABLE
    for item in (
        binding.measurement_authority,
        binding.estimand_authority,
        binding.identification_authority,
    ):
        assert item.scope_or_na_ref
        assert item.authority_ref is None

    with pytest.raises(R4MechanismRuleAuthorityBindingError):
        AuthorityCeilingBinding(
            role=AuthorityRole.MEASUREMENT,
            disposition=AuthorityDisposition.NOT_APPLICABLE,
            scope_or_na_ref=None,
        )


def test_binding_identity_changes_when_evidence_ceiling_changes():
    first = _binding(tag="identity")
    changed_trace = _trace("identity")
    changed_trace = RuleTraceBinding(
        source_refs=changed_trace.source_refs,
        claim_refs=changed_trace.claim_refs,
        evidence_status_ref=_ref("EVIDENCE_STATUS", "changed"),
        normalized_mechanism_ref=changed_trace.normalized_mechanism_ref,
        permitted_rule_shape_ref=changed_trace.permitted_rule_shape_ref,
        required_objective_inputs_bindings_ref=changed_trace.required_objective_inputs_bindings_ref,
        qualification_realization_proof_contract_ref=changed_trace.qualification_realization_proof_contract_ref,
        temporal_currentness_contract_ref=changed_trace.temporal_currentness_contract_ref,
        portability_ceiling_ref=changed_trace.portability_ceiling_ref,
        currentness_ceiling_ref=changed_trace.currentness_ceiling_ref,
        historical_institutional_validity_ref=changed_trace.historical_institutional_validity_ref,
        negative_ceiling_ref=changed_trace.negative_ceiling_ref,
        v3_stop_boundary_ref=changed_trace.v3_stop_boundary_ref,
    )
    second = _binding(tag="identity", trace=changed_trace)
    assert first.binding_hash != second.binding_hash
    assert first.ref != second.ref


def test_schema_has_no_actor_fact_or_numeric_policy_value_surface():
    names = {item.name for item in fields(MechanismRuleAuthorityBinding)}
    assert "actor_ref" not in names
    assert "actor_fact" not in names
    assert "coefficient" not in names
    assert "probability" not in names
    assert "threshold" not in names
    assert "calibration_value" not in names
