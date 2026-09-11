from __future__ import annotations

import pytest

from rawlsing_next.sdtf_r4_d1_hosting_replay import (
    CONTRACT_ID,
    CURRENT_RULE_ADMISSION_CONSERVATION_CONTRACT_ID,
    D1Context,
    D1Evaluation,
    D1FactPointer,
    D1HostingAdapter,
    D1HostingIntegrityError,
    D1RuleApplicationRef,
)
from rawlsing_next.sdtf_r4_mechanism_rule_authority_binding import (
    R4MechanismRuleAuthorityBindingError,
    RuleCurrentness,
)
from rawlsing_next.tests.test_sdtf_r4_mechanism_rule_authority_binding import (
    _binding,
    _h,
    _ref,
)


def _fact(tag: str, state_version: str = "sv1") -> D1FactPointer:
    return D1FactPointer(
        fact_ref=_ref("R2_SEAM_FACT", tag),
        context=D1Context("world-seam", "state-seam", state_version, "t1"),
    )


def _app(tag: str) -> tuple[D1RuleApplicationRef, object]:
    binding = _binding(tag=tag)
    identity = binding.rule_identity
    return (
        D1RuleApplicationRef(
            rule_application_id=f"APP-{tag}",
            rule_id=identity.rule_id,
            rule_version=identity.rule_version,
            rule_hash=identity.rule_content_hash,
        ),
        binding,
    )


def test_contract_bump_and_exact_r1_rule_identity_are_explicit() -> None:
    app, binding = _app("identity")
    assert CONTRACT_ID == "SDTF_R4_D1_HOSTING_REPLAY_R1@2.0.0"
    assert CURRENT_RULE_ADMISSION_CONSERVATION_CONTRACT_ID == (
        "SDTF_R4_R2_CURRENT_RULE_ADMISSION_CONSERVATION_R1@1.0.0"
    )
    assert app.mechanism_rule_ref == binding.rule_identity.ref
    assert app.mechanism_rule_ref.kind == "SDTF_R4_MECHANISM_RULE"
    assert app.mechanism_rule_ref.kind != "MECHANISM_RULE_RECORD"


def test_hostile_raw_rule_application_without_r1_admission_is_rejected() -> None:
    app, _ = _app("unadmitted")
    repo = D1HostingAdapter()
    determinant = _fact("unadmitted-det")
    output = _fact("unadmitted-output")

    with pytest.raises(
        D1HostingIntegrityError,
        match="exact R1 MechanismRuleAuthorityBinding current-rule admission is required",
    ):
        repo.host_direct_derivation(
            app,
            determinant_facts=(determinant,),
            output_fact=output,
        )

    assert repo.current_output_refs() == ()
    assert repo.hosted_mechanism_rule_refs() == ()
    assert repo.hosted_rule_authority_binding_refs() == ()


def test_exact_current_r1_admission_allows_hosting_and_conserves_binding_identity() -> None:
    app, binding = _app("admitted")
    repo = D1HostingAdapter()
    determinant = _fact("admitted-det")
    output = _fact("admitted-output")

    revision = repo.host_direct_derivation(
        app,
        determinant_facts=(determinant,),
        output_fact=output,
        rule_admission=binding,
    )

    assert revision.status == "SUPPORTED_CURRENT"
    assert revision.application.mechanism_rule_ref == binding.rule_identity.ref
    assert revision.rule_authority_binding_ref == binding.ref
    assert revision.current_rule_admission_ref == binding.ref
    assert binding.rule_identity.ref in repo.hosted_mechanism_rule_refs()
    assert binding.ref in repo.hosted_rule_authority_binding_refs()
    projection = revision.semantic_projection()
    assert projection["mechanism_rule_ref"] == binding.rule_identity.ref.as_dict()
    assert projection["rule_authority_binding_ref"] == binding.ref.as_dict()
    assert projection["current_rule_admission_ref"] == binding.ref.as_dict()


def test_candidate_and_historical_r1_bindings_fail_closed_at_hosting() -> None:
    app, _ = _app("noncurrent")
    candidate = _binding(
        tag="noncurrent",
        currentness=RuleCurrentness.CANDIDATE_NOT_CURRENT,
        current_selection_refs=(),
    )
    historical = _binding(
        tag="noncurrent",
        currentness=RuleCurrentness.HISTORICAL_NONCURRENT,
    )
    determinant = _fact("noncurrent-det")
    output = _fact("noncurrent-output")

    for binding in (candidate, historical):
        repo = D1HostingAdapter()
        with pytest.raises(D1HostingIntegrityError, match="current-rule admission failed closed"):
            repo.host_direct_derivation(
                app,
                determinant_facts=(determinant,),
                output_fact=output,
                rule_admission=binding,
            )
        assert repo.current_output_refs() == ()


def test_missing_rule_current_selection_is_rejected_by_r1_before_r2_can_consume_it() -> None:
    with pytest.raises(
        R4MechanismRuleAuthorityBindingError,
        match="CURRENT_ACCEPTED rule requires explicit rule current-selection evidence",
    ):
        _binding(tag="missing-selection", current_selection_refs=())


def test_current_binding_for_different_rule_identity_is_rejected() -> None:
    app, _ = _app("target")
    wrong = _binding(tag="other-rule")
    repo = D1HostingAdapter()

    with pytest.raises(D1HostingIntegrityError, match="does not exactly match"):
        repo.host_direct_derivation(
            app,
            determinant_facts=(_fact("mismatch-det"),),
            output_fact=_fact("mismatch-output"),
            rule_admission=wrong,
        )
    assert repo.current_output_refs() == ()


def test_redrive_without_current_admission_closes_prior_current_output_without_evaluator() -> None:
    app, binding = _app("redrive-missing")
    repo = D1HostingAdapter()
    determinant = _fact("redrive-missing-det")
    output = _fact("redrive-missing-output")
    first = repo.host_direct_derivation(
        app,
        determinant_facts=(determinant,),
        output_fact=output,
        rule_admission=binding,
    )
    calls = []

    def evaluator(application, before):
        calls.append(application)
        raise AssertionError("unadmitted rule must not be evaluated")

    receipt = repo.redrive((determinant.fact_ref,), evaluator)

    assert calls == []
    assert len(receipt.steps) == 1
    step = receipt.steps[0]
    assert step.disposition == "CLOSED_RULE_NOT_CURRENT_OR_UNADMITTED"
    assert step.current_rule_admission_ref is None
    assert output.fact_ref not in repo.current_output_refs()
    current = repo.current_revision(app)
    assert current.status == "CLOSED_UNSUPPORTED"
    assert current.output_fact is None
    assert current.current_rule_admission_ref is None
    assert len(repo.history(app)) == 2
    assert repo.history(app)[0].exact_ref == first.exact_ref
    assert repo.history(app)[0].output_fact == output
    receipt.verify()


def test_redrive_with_candidate_binding_closes_output_and_conserves_attempted_binding_provenance() -> None:
    app, current = _app("redrive-candidate")
    candidate = _binding(
        tag="redrive-candidate",
        currentness=RuleCurrentness.CANDIDATE_NOT_CURRENT,
        current_selection_refs=(),
    )
    repo = D1HostingAdapter()
    determinant = _fact("redrive-candidate-det")
    output = _fact("redrive-candidate-output")
    repo.host_direct_derivation(
        app,
        determinant_facts=(determinant,),
        output_fact=output,
        rule_admission=current,
    )
    calls = []

    def evaluator(application, before):
        calls.append(application)
        return D1Evaluation(True, before.determinant_facts, before.output_fact)

    receipt = repo.redrive(
        (determinant.fact_ref,),
        evaluator,
        rule_admission_resolver=lambda application, before: candidate,
    )

    assert calls == []
    assert receipt.steps[0].disposition == "CLOSED_RULE_NOT_CURRENT_OR_UNADMITTED"
    assert receipt.steps[0].rule_authority_binding_ref == candidate.ref
    assert receipt.steps[0].current_rule_admission_ref is None
    assert repo.current_revision(app).rule_authority_binding_ref == candidate.ref
    assert repo.current_revision(app).current_rule_admission_ref is None
    assert output.fact_ref not in repo.current_output_refs()


def test_redrive_with_exact_current_admission_can_preserve_current_output_and_replay_identity() -> None:
    def run():
        app, binding = _app("redrive-current")
        repo = D1HostingAdapter()
        determinant = _fact("redrive-current-det")
        output = _fact("redrive-current-output")
        repo.host_direct_derivation(
            app,
            determinant_facts=(determinant,),
            output_fact=output,
            rule_admission=binding,
        )

        def evaluator(application, before):
            return D1Evaluation(
                supported=True,
                determinant_facts=before.determinant_facts,
                output_fact=before.output_fact,
                evidence_witness_refs=before.evidence_witness_refs,
            )

        receipt = repo.redrive(
            (determinant.fact_ref,),
            evaluator,
            rule_admission_resolver=lambda application, before: binding,
        )
        return repo, app, binding, output, receipt

    first_repo, first_app, first_binding, first_output, first_receipt = run()
    second_repo, second_app, second_binding, second_output, second_receipt = run()

    assert first_receipt.steps[0].disposition == "UNCHANGED"
    assert first_receipt.steps[0].current_rule_admission_ref == first_binding.ref
    assert first_output.fact_ref in first_repo.current_output_refs()
    assert first_repo.current_revision(first_app).current_rule_admission_ref == first_binding.ref
    assert first_receipt.content_hash == second_receipt.content_hash
    assert first_receipt.exact_ref == second_receipt.exact_ref
    assert first_binding.ref == second_binding.ref
    assert first_app.exact_ref == second_app.exact_ref
    assert first_output.fact_ref == second_output.fact_ref
