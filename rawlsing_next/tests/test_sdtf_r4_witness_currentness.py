from __future__ import annotations

from dataclasses import dataclass, replace

import pytest

from rawlsing_next import sdtf_r4_witness_currentness as w


OWNER = "TEST_OWNER_CONTRACT@1.0.0"
WTYPE = "TEST_NATIVE_WITNESS_TYPE@1.0.0"


@dataclass(frozen=True)
class NativeWitness:
    ref: str = "urn:test:witness:1"
    lifecycle: w.WitnessLifecycle = w.WitnessLifecycle.CURRENT
    authority_checks: tuple[w.CurrentnessCheckR1, ...] = (
        w.CurrentnessCheckR1("source_authority", "source@1", "source@1", w.CheckState.CURRENT),
        w.CurrentnessCheckR1("type_authority", "type@1", "type@1", w.CheckState.CURRENT),
    )
    dependencies: tuple[w.CurrentnessCheckR1, ...] = ()
    positive: w.TriState = w.TriState.YES
    negative: w.TriState = w.TriState.NO
    path: w.K4ProofPath | None = None
    path_a: w.K4PathAEvidenceR1 | None = None
    path_b: w.K4PathBEvidenceR1 | None = None


class NativeAdapter:
    owner_contract_ref = OWNER
    witness_type_ref = WTYPE

    def currentness_evidence(self, native_witness: NativeWitness, request: w.AssertionRequestR1):
        return w.WitnessCurrentnessEvidenceR1(
            self.owner_contract_ref,
            self.witness_type_ref,
            native_witness.ref,
            native_witness.lifecycle,
            native_witness.authority_checks,
            native_witness.dependencies,
        )

    def positive_proof(self, native_witness: NativeWitness, request: w.AssertionRequestR1):
        return native_witness.positive

    def explicit_negative_proof(self, native_witness: NativeWitness, request: w.AssertionRequestR1):
        return native_witness.negative

    def k4_path(self, native_witness: NativeWitness, request: w.AssertionRequestR1):
        return native_witness.path

    def k4_path_a_evidence(self, native_witness: NativeWitness, request: w.AssertionRequestR1):
        return native_witness.path_a

    def k4_path_b_evidence(self, native_witness: NativeWitness, request: w.AssertionRequestR1):
        return native_witness.path_b


def request(kind=w.AssertionKind.K1_CONSTITUTIVE_POSITIONAL, *, polarity=w.Polarity.POSITIVE,
            currentness=w.FactCurrentness.CURRENT, modality=w.Modality.ACTUAL,
            descriptor=None):
    return w.AssertionRequestR1(kind, polarity, currentness, modality, OWNER, WTYPE,
                                query_context={"opaque": "owner-defined"},
                                operative_descriptor=descriptor)


def path_a_good():
    return w.K4PathAEvidenceR1(w.TriState.YES, w.TriState.YES, w.TriState.YES)


def path_b_good():
    return w.K4PathBEvidenceR1(
        w.TriState.YES,
        w.TriState.YES,
        w.TriState.YES,
        w.TriState.YES,
        w.TriState.NO,
    )


def test_01_current_k1_positive_proof_is_proven_and_active_remains_umbrella_descriptor():
    result = w.adjudicate_assertion_r1(
        request(descriptor=w.ACTIVE_UMBRELLA_DESCRIPTOR), NativeWitness(), NativeAdapter()
    )
    assert result.proof_adjudication is w.ProofAdjudication.PROVEN
    assert result.assertion_kind is w.AssertionKind.K1_CONSTITUTIVE_POSITIONAL
    assert result.operative_descriptor == "ACTIVE"
    assert result.k4_path is None


def test_02_replaced_type_authority_stales_proof_before_use():
    witness = replace(
        NativeWitness(),
        authority_checks=(
            w.CurrentnessCheckR1("source_authority", "source@1", "source@1", w.CheckState.CURRENT),
            w.CurrentnessCheckR1("type_authority", "type@1", "type@2", w.CheckState.REPLACED),
        ),
    )
    result = w.adjudicate_assertion_r1(request(), witness, NativeAdapter())
    assert result.proof_adjudication is w.ProofAdjudication.UNKNOWN_NOT_PROVEN
    assert result.witness_currentness is w.WitnessCurrentness.STALE_REQUIRES_REPLAY
    assert result.first_failing_role == "type_authority"


def test_03_revoked_witness_fails_closed_and_never_becomes_negative_by_revocation_alone():
    witness = replace(NativeWitness(), lifecycle=w.WitnessLifecycle.REVOKED, negative=w.TriState.NO)
    positive = w.adjudicate_assertion_r1(request(), witness, NativeAdapter())
    negative = w.adjudicate_assertion_r1(
        request(polarity=w.Polarity.NEGATIVE), witness, NativeAdapter()
    )
    assert positive.proof_adjudication is w.ProofAdjudication.UNKNOWN_NOT_PROVEN
    assert negative.proof_adjudication is w.ProofAdjudication.UNKNOWN_NOT_PROVEN
    assert positive.witness_currentness is w.WitnessCurrentness.REVOKED
    assert negative.witness_currentness is w.WitnessCurrentness.REVOKED


def test_04_unknown_authority_currentness_is_unknown_not_proven():
    witness = replace(
        NativeWitness(),
        authority_checks=(
            w.CurrentnessCheckR1("source_authority", "source@1", None, w.CheckState.UNKNOWN_NOT_PROVEN),
        ),
    )
    result = w.adjudicate_assertion_r1(request(), witness, NativeAdapter())
    assert result.proof_adjudication is w.ProofAdjudication.UNKNOWN_NOT_PROVEN
    assert result.witness_currentness is w.WitnessCurrentness.UNKNOWN_NOT_PROVEN
    assert result.first_failing_role == "source_authority"


def test_05_k4_path_a_current_then_invalidating_replay_dependency_stales_proof_visible_witness():
    base = replace(
        NativeWitness(), path=w.K4ProofPath.PATH_A_DIRECT_INTERVAL, path_a=path_a_good()
    )
    current = w.adjudicate_assertion_r1(
        request(w.AssertionKind.K4_ACTIVE_DURATIVE), base, NativeAdapter()
    )
    assert current.proof_adjudication is w.ProofAdjudication.PROVEN
    assert current.k4_path is w.K4ProofPath.PATH_A_DIRECT_INTERVAL

    stale = replace(
        base,
        dependencies=(
            w.CurrentnessCheckR1(
                "adopted_replay_input:contact_authority",
                "contact@1",
                "contact@2",
                w.CheckState.REPLACED,
            ),
        ),
    )
    result = w.adjudicate_assertion_r1(
        request(w.AssertionKind.K4_ACTIVE_DURATIVE), stale, NativeAdapter()
    )
    assert result.proof_adjudication is w.ProofAdjudication.UNKNOWN_NOT_PROVEN
    assert result.witness_currentness is w.WitnessCurrentness.STALE_REQUIRES_REPLAY
    assert result.first_failing_role == "adopted_replay_input:contact_authority"


def test_06_k4_path_b_survives_unrelated_replay_churn_but_not_owner_source_revision():
    # Unrelated replay churn is intentionally absent from invalidating dependency checks;
    # the owner adapter declares what is actually invalidating for this witness type.
    continuing = replace(
        NativeWitness(), path=w.K4ProofPath.PATH_B_CONTINUING_STATE, path_b=path_b_good()
    )
    result = w.adjudicate_assertion_r1(
        request(w.AssertionKind.K4_ACTIVE_DURATIVE), continuing, NativeAdapter()
    )
    assert result.proof_adjudication is w.ProofAdjudication.PROVEN
    assert result.k4_path is w.K4ProofPath.PATH_B_CONTINUING_STATE

    owner_revised = replace(
        continuing,
        authority_checks=(
            w.CurrentnessCheckR1("source_authority", "source@1", "source@2", w.CheckState.REPLACED),
            w.CurrentnessCheckR1("type_authority", "type@1", "type@1", w.CheckState.CURRENT),
        ),
    )
    invalid = w.adjudicate_assertion_r1(
        request(w.AssertionKind.K4_ACTIVE_DURATIVE), owner_revised, NativeAdapter()
    )
    assert invalid.proof_adjudication is w.ProofAdjudication.UNKNOWN_NOT_PROVEN
    assert invalid.witness_currentness is w.WitnessCurrentness.STALE_REQUIRES_REPLAY
    assert invalid.first_failing_role == "source_authority"


@pytest.mark.parametrize(
    "path_b",
    [
        replace(path_b_good(), support_interval_overlaps_asserted_or_query_interval=w.TriState.NO),
        replace(
            path_b_good(),
            complete_termination_supersession_invalidation_coverage_through_query=w.TriState.NO,
        ),
        replace(path_b_good(), defeating_closing_fact=w.TriState.YES),
        replace(
            path_b_good(),
            complete_termination_supersession_invalidation_coverage_through_query=w.TriState.UNKNOWN,
        ),
    ],
)
def test_07_k4_path_b_requires_overlap_complete_closure_coverage_and_no_defeating_fact(path_b):
    witness = replace(
        NativeWitness(), path=w.K4ProofPath.PATH_B_CONTINUING_STATE, path_b=path_b
    )
    result = w.adjudicate_assertion_r1(
        request(w.AssertionKind.K4_ACTIVE_DURATIVE), witness, NativeAdapter()
    )
    assert result.proof_adjudication is w.ProofAdjudication.UNKNOWN_NOT_PROVEN
    assert result.k4_path is w.K4ProofPath.PATH_B_CONTINUING_STATE


def test_08_old_establishment_event_plus_silence_cannot_prove_k4_path_b():
    witness = replace(
        NativeWitness(),
        path=w.K4ProofPath.PATH_B_CONTINUING_STATE,
        path_b=replace(
            path_b_good(),
            owner_declares_continuing_state=w.TriState.NO,
            complete_termination_supersession_invalidation_coverage_through_query=w.TriState.UNKNOWN,
        ),
    )
    result = w.adjudicate_assertion_r1(
        request(w.AssertionKind.K4_ACTIVE_DURATIVE), witness, NativeAdapter()
    )
    assert result.proof_adjudication is w.ProofAdjudication.UNKNOWN_NOT_PROVEN


def test_09_negative_truth_requires_explicit_negative_proof_not_failed_positive_proof():
    no_positive = replace(NativeWitness(), positive=w.TriState.NO, negative=w.TriState.NO)
    result = w.adjudicate_assertion_r1(
        request(polarity=w.Polarity.NEGATIVE), no_positive, NativeAdapter()
    )
    assert result.proof_adjudication is w.ProofAdjudication.UNKNOWN_NOT_PROVEN
    assert result.reason == "explicit-negative-proof-absent"

    explicit_negative = replace(no_positive, negative=w.TriState.YES)
    proved = w.adjudicate_assertion_r1(
        request(polarity=w.Polarity.NEGATIVE), explicit_negative, NativeAdapter()
    )
    assert proved.proof_adjudication is w.ProofAdjudication.PROVEN


def test_10_axes_remain_orthogonal_for_projected_historical_request():
    req = request(
        w.AssertionKind.K2_QUALIFIED_POSSIBILITY,
        currentness=w.FactCurrentness.HISTORICAL_NONCURRENT,
        modality=w.Modality.PROJECTED_COUNTERFACTUAL,
    )
    result = w.adjudicate_assertion_r1(req, NativeWitness(), NativeAdapter())
    assert result.proof_adjudication is w.ProofAdjudication.PROVEN
    assert result.assertion_kind is w.AssertionKind.K2_QUALIFIED_POSSIBILITY
    assert result.currentness is w.FactCurrentness.HISTORICAL_NONCURRENT
    assert result.modality is w.Modality.PROJECTED_COUNTERFACTUAL


def test_11_adapter_owner_or_type_mismatch_fails_closed_without_semantic_inference():
    class WrongAdapter(NativeAdapter):
        witness_type_ref = "OTHER_NATIVE_WITNESS_TYPE@1.0.0"

    result = w.adjudicate_assertion_r1(request(), NativeWitness(), WrongAdapter())
    assert result.proof_adjudication is w.ProofAdjudication.UNKNOWN_NOT_PROVEN
    assert result.witness_currentness is w.WitnessCurrentness.STALE_REQUIRES_REPLAY
    assert result.first_failing_role == "witness_type"


def test_12_current_check_must_bind_expected_and_observed_exactly():
    evidence = w.WitnessCurrentnessEvidenceR1(
        OWNER,
        WTYPE,
        "urn:test:witness:1",
        w.WitnessLifecycle.CURRENT,
        (w.CurrentnessCheckR1("source_authority", "source@1", "source@2", w.CheckState.CURRENT),),
    )
    decision = w.evaluate_witness_currentness_r1(
        evidence, required_owner_contract_ref=OWNER, required_witness_type_ref=WTYPE
    )
    assert decision.currentness is w.WitnessCurrentness.UNKNOWN_NOT_PROVEN
    assert decision.first_failing_role == "source_authority"
