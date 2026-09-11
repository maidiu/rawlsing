from __future__ import annotations

from dataclasses import replace

import pytest

from rawlsing_next.sdtf_r4_d1_hosting_replay import (
    D1Context,
    D1Evaluation,
    D1FactPointer,
    D1HostingAdapter,
    D1HostingIntegrityError,
    D1RuleApplicationRef,
)
from rawlsing_next.sdtf_r4_mechanism_rule_authority_binding import RuleCurrentness
from rawlsing_next import sdtf_r4_witness_currentness as w
from rawlsing_next.sdtf_r4_world_response_redrive import (
    R4WorldResponseStateError,
    WorldResponseSourceKind,
    bind_admitted_external_world_response_source,
)
from rawlsing_next.tests.test_sdtf_r4_mechanism_rule_authority_binding import (
    _binding,
    _ref,
)
from rawlsing_next.tests.test_sdtf_r4_witness_currentness import (
    NativeAdapter,
    NativeWitness,
    path_b_good,
    request,
)
from rawlsing_next.tests.test_sdtf_r4_world_response_redrive import _world_response


def _fact(tag: str, *, state: str = "sv1") -> D1FactPointer:
    return D1FactPointer(
        fact_ref=_ref("R2_FRESH_COURT_FACT", tag),
        context=D1Context("court-world", "court-state", state, "t1"),
    )


def _application(tag: str):
    binding = _binding(tag=tag)
    identity = binding.rule_identity
    app = D1RuleApplicationRef(
        rule_application_id=f"COURT-APP-{tag}",
        rule_id=identity.rule_id,
        rule_version=identity.rule_version,
        rule_hash=identity.rule_content_hash,
    )
    return app, binding


def test_prior_r1_r2_bypass_is_closed_before_supported_current_can_exist():
    app, _ = _application("bypass")
    repo = D1HostingAdapter()
    determinant = _fact("bypass-det")
    output = _fact("bypass-output")

    with pytest.raises(D1HostingIntegrityError, match="current-rule admission is required"):
        repo.host_direct_derivation(
            app,
            determinant_facts=(determinant,),
            output_fact=output,
        )

    assert repo.current_output_refs() == ()
    assert repo.hosted_mechanism_rule_refs() == ()
    assert repo.hosted_rule_authority_binding_refs() == ()


def test_r1_identity_and_current_admission_are_conserved_through_revision_and_replay():
    def run():
        app, binding = _application("identity")
        repo = D1HostingAdapter()
        determinant = _fact("identity-det")
        output = _fact("identity-output")
        revision = repo.host_direct_derivation(
            app,
            determinant_facts=(determinant,),
            output_fact=output,
            rule_admission=binding,
        )

        def evaluator(application, before):
            return D1Evaluation(True, before.determinant_facts, before.output_fact)

        receipt = repo.redrive(
            (determinant.fact_ref,),
            evaluator,
            rule_admission_resolver=lambda application, before: binding,
        )
        receipt.verify()
        return app, binding, revision, receipt, repo

    first = run()
    second = run()
    app, binding, revision, receipt, repo = first

    assert app.mechanism_rule_ref == binding.rule_identity.ref
    assert revision.application.mechanism_rule_ref == binding.rule_identity.ref
    assert revision.rule_authority_binding_ref == binding.ref
    assert revision.current_rule_admission_ref == binding.ref
    assert receipt.steps[0].current_rule_admission_ref == binding.ref
    assert receipt.steps[0].rule_authority_binding_ref == binding.ref
    assert binding.rule_identity.ref in repo.hosted_mechanism_rule_refs()
    assert binding.ref in repo.hosted_rule_authority_binding_refs()
    assert receipt.exact_ref == second[3].exact_ref
    assert receipt.content_hash == second[3].content_hash


def test_noncurrent_admission_closes_prior_consequence_without_evaluator_or_opposite_fact():
    app, current = _application("noncurrent")
    candidate = _binding(
        tag="noncurrent",
        currentness=RuleCurrentness.CANDIDATE_NOT_CURRENT,
        current_selection_refs=(),
    )
    determinant = _fact("noncurrent-det")
    output = _fact("noncurrent-output")
    repo = D1HostingAdapter()
    repo.host_direct_derivation(
        app,
        determinant_facts=(determinant,),
        output_fact=output,
        rule_admission=current,
    )
    calls = []

    def evaluator(application, before):
        calls.append(application)
        raise AssertionError("noncurrent admission must fail before evaluator invocation")

    receipt = repo.redrive(
        (determinant.fact_ref,),
        evaluator,
        rule_admission_resolver=lambda application, before: candidate,
    )

    assert calls == []
    assert receipt.steps[0].disposition == "CLOSED_RULE_NOT_CURRENT_OR_UNADMITTED"
    assert repo.current_revision(app).status == "CLOSED_UNSUPPORTED"
    assert repo.current_revision(app).output_fact is None
    assert output.fact_ref not in repo.current_output_refs()
    assert len(repo.history(app)) == 2


def test_cross_seam_currentness_axes_do_not_collapse_and_bare_active_is_not_k4_exclusive():
    k1_active = w.adjudicate_assertion_r1(
        request(descriptor=w.ACTIVE_UMBRELLA_DESCRIPTOR),
        NativeWitness(),
        NativeAdapter(),
    )
    assert k1_active.proof_adjudication is w.ProofAdjudication.PROVEN
    assert k1_active.assertion_kind is w.AssertionKind.K1_CONSTITUTIVE_POSITIONAL
    assert k1_active.operative_descriptor == "ACTIVE"
    assert k1_active.k4_path is None

    k4_good = replace(
        NativeWitness(),
        path=w.K4ProofPath.PATH_B_CONTINUING_STATE,
        path_b=path_b_good(),
    )
    proved = w.adjudicate_assertion_r1(
        request(w.AssertionKind.K4_ACTIVE_DURATIVE),
        k4_good,
        NativeAdapter(),
    )
    assert proved.proof_adjudication is w.ProofAdjudication.PROVEN

    stale_event_only = replace(
        k4_good,
        path_b=replace(
            path_b_good(),
            owner_declares_continuing_state=w.TriState.NO,
            support_interval_overlaps_asserted_or_query_interval=w.TriState.NO,
            complete_termination_supersession_invalidation_coverage_through_query=w.TriState.UNKNOWN,
        ),
    )
    unknown = w.adjudicate_assertion_r1(
        request(w.AssertionKind.K4_ACTIVE_DURATIVE),
        stale_event_only,
        NativeAdapter(),
    )
    assert unknown.proof_adjudication is w.ProofAdjudication.UNKNOWN_NOT_PROVEN


def test_private_v3_and_oee_sources_cannot_author_objective_world_response():
    for kind in (
        WorldResponseSourceKind.PRIVATE_V3_STATE,
        WorldResponseSourceKind.GENERIC_WORLD_SIMULATION,
        WorldResponseSourceKind.INTERPRETATION_EXPECTATION_STRIVING,
        WorldResponseSourceKind.OEE_ENCOUNTER_DERIVATION,
    ):
        candidate = _world_response(source_kind=kind)
        with pytest.raises(R4WorldResponseStateError):
            bind_admitted_external_world_response_source(
                candidate,
                expected_scope_ref=candidate.scope_ref,
                expected_world_context_ref=candidate.world_context_ref,
            )


def test_same_context_self_ancestry_is_rejected_without_fixed_point_authority():
    app, binding = _application("cycle")
    determinant = _fact("cycle-shared")
    repo = D1HostingAdapter()
    with pytest.raises(D1HostingIntegrityError):
        repo.host_direct_derivation(
            app,
            determinant_facts=(determinant,),
            output_fact=determinant,
            rule_admission=binding,
        )
    assert repo.current_output_refs() == ()
