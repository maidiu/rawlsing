from __future__ import annotations

import hashlib

import pytest

from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.sdtf_r4_d1_hosting_replay import (
    CONTRACT_ID,
    D1Context,
    D1Evaluation,
    D1FactPointer,
    D1HostingIntegrityError,
    D1HostingAdapter as ProductionD1HostingAdapter,
    D1RuleApplicationRef,
)
from rawlsing_next.tests.test_sdtf_r4_mechanism_rule_authority_binding import _binding


def _sha(label: str) -> str:
    return hashlib.sha256(label.encode("utf-8")).hexdigest()


def _ref(kind: str, object_id: str) -> ExactRef:
    return ExactRef(kind=kind, object_id=object_id, content_hash=_sha(f"{kind}:{object_id}"))


def _fact(object_id: str, *, state_version: str = "sv1", valid_time: str = "t1") -> D1FactPointer:
    return D1FactPointer(
        fact_ref=_ref("TEST_FACT", object_id),
        context=D1Context("world-1", "state-1", state_version, valid_time),
    )


def _app(app_id: str, version: str = "1.0.0") -> D1RuleApplicationRef:
    binding = _binding(tag=app_id)
    assert binding.rule_identity.rule_version == version
    return D1RuleApplicationRef(
        rule_application_id=app_id,
        rule_id=binding.rule_identity.rule_id,
        rule_version=binding.rule_identity.rule_version,
        rule_hash=binding.rule_identity.rule_content_hash,
    )


def _admission(application: D1RuleApplicationRef):
    return _binding(tag=application.rule_id.removeprefix("RULE-"))


class D1HostingAdapter(ProductionD1HostingAdapter):
    """Regression harness supplying exact deterministic R1 admissions to R2."""

    def host_direct_derivation(self, application, **kwargs):
        return super().host_direct_derivation(
            application,
            rule_admission=_admission(application),
            **kwargs,
        )

    def redrive(self, changed_determinant_refs, evaluator):
        return super().redrive(
            changed_determinant_refs,
            evaluator,
            rule_admission_resolver=lambda application, before: _admission(application),
        )


def _build_chain() -> tuple[
    D1HostingAdapter,
    D1FactPointer,
    D1FactPointer,
    D1FactPointer,
    D1FactPointer,
    D1RuleApplicationRef,
    D1RuleApplicationRef,
    D1RuleApplicationRef,
]:
    repo = D1HostingAdapter()
    determinant = _fact("det-A")
    out_a = _fact("out-A")
    out_b = _fact("out-B")
    unrelated_out = _fact("unrelated-out")
    app_a, app_b, app_u = _app("app-A"), _app("app-B"), _app("app-U")
    witness = _ref("EVIDENCE_WITNESS_RECORD", "witness-A")
    unrelated_det = _fact("det-U")

    repo.host_direct_derivation(
        app_a,
        determinant_facts=(determinant,),
        output_fact=out_a,
        evidence_witness_refs=(witness,),
    )
    repo.host_direct_derivation(app_b, determinant_facts=(out_a,), output_fact=out_b)
    repo.host_direct_derivation(app_u, determinant_facts=(unrelated_det,), output_fact=unrelated_out)
    return repo, determinant, out_a, out_b, unrelated_out, app_a, app_b, app_u


def test_direct_derivation_pins_exact_rule_application_version_and_reverse_edge() -> None:
    repo, determinant, out_a, _, _, app_a, _, _ = _build_chain()
    revision = repo.current_revision(app_a)

    assert CONTRACT_ID.endswith("@2.0.0")
    assert revision.application.rule_application_id == "app-A"
    assert revision.application.rule_version == "1.0.0"
    assert revision.output_fact == out_a
    assert revision.determinant_facts == (determinant,)
    assert repo.reverse_dependents(determinant.fact_ref) == (app_a,)
    assert revision.evidence_witness_refs[0].kind == "EVIDENCE_WITNESS_RECORD"
    assert app_a.mechanism_rule_ref in repo.hosted_mechanism_rule_refs()
    assert revision.rule_authority_binding_ref in repo.hosted_rule_authority_binding_refs()
    assert revision.current_rule_admission_ref == revision.rule_authority_binding_ref
    assert revision.evidence_witness_refs[0] in repo.hosted_evidence_witness_refs()
    assert app_a.exact_ref.kind == "RULE_APPLICATION_RECORD"


def test_determinant_scoped_close_redrives_only_dependents_and_preserves_unrelated_history() -> None:
    repo, determinant, out_a, out_b, unrelated_out, app_a, app_b, app_u = _build_chain()
    initial_unrelated = repo.current_revision(app_u).exact_ref
    calls: list[str] = []

    def evaluator(application, before):
        calls.append(application.rule_application_id)
        if application == app_a:
            return D1Evaluation(
                supported=False,
                determinant_facts=before.determinant_facts,
                output_fact=None,
                evidence_witness_refs=before.evidence_witness_refs,
            )
        if application == app_b:
            return D1Evaluation(
                supported=False,
                determinant_facts=before.determinant_facts,
                output_fact=None,
            )
        raise AssertionError("unrelated application must not be redriven")

    receipt = repo.redrive((determinant.fact_ref,), evaluator)

    assert calls == ["app-A", "app-B"]
    assert [step.disposition for step in receipt.steps] == [
        "CLOSED_UNSUPPORTED",
        "CLOSED_UNSUPPORTED",
    ]
    assert repo.current_revision(app_a).output_fact is None
    assert repo.current_revision(app_b).output_fact is None
    assert repo.current_revision(app_u).exact_ref == initial_unrelated
    assert unrelated_out.fact_ref in repo.current_output_refs()
    assert out_a.fact_ref not in repo.current_output_refs()
    assert out_b.fact_ref not in repo.current_output_refs()
    assert len(repo.history(app_a)) == 2
    assert repo.history(app_a)[0].output_fact == out_a
    assert len(repo.history(app_u)) == 1
    assert all(step.application_ref != app_u.exact_ref for step in receipt.steps)
    receipt.verify()


def test_unsupported_evaluation_cannot_synthesize_opposite_fact() -> None:
    with pytest.raises(D1HostingIntegrityError, match="opposite fact"):
        D1Evaluation(
            supported=False,
            determinant_facts=(_fact("det"),),
            output_fact=_fact("invented-opposite"),
        )


def test_unchanged_upstream_output_does_not_redrive_dependent() -> None:
    repo, determinant, _, _, unrelated_out, app_a, _, app_u = _build_chain()
    calls: list[str] = []

    def evaluator(application, before):
        calls.append(application.rule_application_id)
        assert application == app_a
        return D1Evaluation(
            supported=True,
            determinant_facts=before.determinant_facts,
            output_fact=before.output_fact,
            evidence_witness_refs=before.evidence_witness_refs,
        )

    receipt = repo.redrive((determinant.fact_ref,), evaluator)
    assert calls == ["app-A"]
    assert len(receipt.steps) == 1
    assert receipt.steps[0].disposition == "UNCHANGED"
    assert repo.current_revision(app_u).output_fact == unrelated_out


def test_replacement_output_redrives_only_exact_reverse_dependents() -> None:
    repo, determinant, out_a, out_b, unrelated_out, app_a, app_b, app_u = _build_chain()
    replacement = _fact("out-A-v2")
    replacement_b = _fact("out-B-v2")
    calls: list[str] = []

    def evaluator(application, before):
        calls.append(application.rule_application_id)
        if application == app_a:
            return D1Evaluation(
                supported=True,
                determinant_facts=before.determinant_facts,
                output_fact=replacement,
                evidence_witness_refs=before.evidence_witness_refs,
            )
        if application == app_b:
            assert before.output_fact == out_b
            return D1Evaluation(
                supported=True,
                determinant_facts=(replacement,),
                output_fact=replacement_b,
            )
        raise AssertionError("unrelated application must not be redriven")

    receipt = repo.redrive((determinant.fact_ref,), evaluator)
    assert calls == ["app-A", "app-B"]
    assert [step.disposition for step in receipt.steps] == ["REPLACED_OUTPUT", "REPLACED_OUTPUT"]
    assert replacement.fact_ref in repo.current_output_refs()
    assert replacement_b.fact_ref in repo.current_output_refs()
    assert out_a.fact_ref not in repo.current_output_refs()
    assert out_b.fact_ref not in repo.current_output_refs()
    assert unrelated_out.fact_ref in repo.current_output_refs()
    assert repo.current_revision(app_u).output_fact == unrelated_out
    assert repo.reverse_dependents(replacement.fact_ref) == (app_b,)
    assert repo.reverse_dependents(out_a.fact_ref) == ()
    assert repo.reverse_dependents(out_a.fact_ref, historical=True) == (app_b,)


def test_same_context_rule_application_self_ancestry_is_rejected() -> None:
    repo = D1HostingAdapter()
    determinant = _fact("base")
    first_output = _fact("first-output")
    app = _app("recursive-app")
    repo.host_direct_derivation(app, determinant_facts=(determinant,), output_fact=first_output)

    def evaluator(application, before):
        assert application == app
        return D1Evaluation(
            supported=True,
            determinant_facts=(first_output,),
            output_fact=_fact("second-output"),
        )

    with pytest.raises(D1HostingIntegrityError, match="rule-application self-ancestry"):
        repo.redrive((determinant.fact_ref,), evaluator)


def test_same_application_prior_context_can_be_used_for_next_state_version() -> None:
    repo = D1HostingAdapter()
    determinant = _fact("base")
    first_output = _fact("first-output", state_version="sv1")
    app = _app("stateful-app")
    repo.host_direct_derivation(app, determinant_facts=(determinant,), output_fact=first_output)

    next_output = _fact("second-output", state_version="sv2")

    def evaluator(application, before):
        return D1Evaluation(
            supported=True,
            determinant_facts=(first_output,),
            output_fact=next_output,
        )

    receipt = repo.redrive((determinant.fact_ref,), evaluator)
    assert receipt.steps[0].disposition == "REPLACED_OUTPUT"
    assert repo.current_revision(app).output_fact == next_output


def test_replay_receipt_is_deterministic_for_same_exact_graph_independent_of_trigger_order() -> None:
    def run(reverse: bool):
        repo = D1HostingAdapter()
        d1, d2 = _fact("d1"), _fact("d2")
        out = _fact("out")
        app = _app("app")
        repo.host_direct_derivation(app, determinant_facts=(d1, d2), output_fact=out)

        def evaluator(application, before):
            return D1Evaluation(
                supported=False,
                determinant_facts=before.determinant_facts,
                output_fact=None,
            )

        triggers = (d2.fact_ref, d1.fact_ref) if reverse else (d1.fact_ref, d2.fact_ref)
        return repo.redrive(triggers, evaluator)

    first = run(False)
    second = run(True)
    assert first.content_hash == second.content_hash
    assert first.exact_ref == second.exact_ref
    assert first.semantic_projection() == second.semantic_projection()
    first.verify()
    second.verify()


def test_receipt_captures_exact_affected_graph_and_not_unrelated_edges() -> None:
    repo, determinant, _, _, _, app_a, app_b, app_u = _build_chain()

    def evaluator(application, before):
        return D1Evaluation(
            supported=False,
            determinant_facts=before.determinant_facts,
            output_fact=None,
            evidence_witness_refs=before.evidence_witness_refs,
        )

    receipt = repo.redrive((determinant.fact_ref,), evaluator)
    application_keys = {edge[1] for edge in receipt.exact_affected_edges}
    assert app_a.exact_ref.key in application_keys
    assert app_b.exact_ref.key in application_keys
    assert app_u.exact_ref.key not in application_keys
