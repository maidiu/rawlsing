"""HQ266 G01 -- G1 owner-only C1 -> REAL G2 -> authenticated F8 selected ingress court.

SOURCE-FREE. TEST_ONLY_UNISSUED model/use refs. NOT AN EE14 GRANT. NOT A TRUST ROOT.
NOT DEPLOYED SECURITY. G1_INTERNAL_OWNER_PATH_CANDIDATE_ONLY.

The whole point of this court is that the external client is a DATA-ONLY caller. Every
hostile below is attempted against the public `serve` surface, not against private state.

WHAT THIS COURT PROVES (HQ263 R01 F1-F6 corrections)
-----------------------------------------------------
F1  The ingress runs the REAL applicability owner, the REAL accepted G2 binder and the
    REAL bound-F8 evaluator. The owner-local `_applicability_scope` hash stand-in and the
    raw-F8 bypass are gone.
F2  q1 and q2 are two GENUINELY DIFFERENT C1 producer queries over ONE four-respondent
    XOR source: q1 has denominator 2 (1/2, 1/2), q2 has denominator 1 (0/1, 1/1), with
    distinct producer identities and distinct denominator members.
F3  Full C1 identity/evidence/authority/provenance is authenticated DEEPLY against
    non-mutable owner-held material, and refusal happens BEFORE any F8 invocation.
F4  Native C1 typed states are read for what they are; an intrinsic C1 negative is never
    reported as a missing G0b, and NO_ADMITTED_SOURCE is a distinct applicability reason.
F5  The public surface accepts only exact builtin types, and owner material is deeply
    immutable after construction.
F6  The hostiles actually exercise the ingress: forged material is refused at the real
    boundary, the real binder's refusals surface through the ingress, and a caller cannot
    reconstruct a selected receipt from the observable F8 number.

HQ268 G01 CORRECTIONS (D1 / D2 / R2), added on top of F1-F6
-----------------------------------------------------------
D1  The owner-held EXPECTED C1 identity must be complete, exact and typed before it is
    trusted. An empty or single-key cell expectation, a missing provenance key, a missing
    composed-identity key, an extraneous key or a wrong builtin type is refused at owner
    construction AND again immediately before the comparison -- always at zero F8 and with
    no applicability, binder or evaluate call. The field-by-field comparison iterates the
    closed required key set, so no required field can be skipped.
D2  `g2_receipt_hash` is the accepted owner's own
    `CandidateClassApplicabilityReceipt.replay_identity()`, exactly -- never a locally
    re-derived six-field subset -- and `origin_receipt_hash` transitively includes it.
R2  The live `_source` and `_cells` containers are read-only, and the BOUNDED RESIDUAL
    (the nested objects inside `_source` stay the owner's shared objects) is named in the
    test below rather than claimed away.

The positive control is the EXACT HQ253 T01 construction from historical witness commit
e609be4f68c51182c5acb3a99c671949f1b71d34 (test blob 17300a405d78820cd663618918e64bb0323f532e):
`_query_authority("c1-at09-xor")` + `_registry(source, qauth)` + `fx.xor_fixture()` +
`fx.direct_condition_composition(...)`. `_query_snapshot()` is NEVER used.
"""
from __future__ import annotations

import dataclasses
import hashlib

import pytest

from rawlsing_next import pre553_service_f8_source_scope_binding as B
from rawlsing_next import pre553_service_source_applicability as SA
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.pre553_ee14_c1_owner_authenticated_ingress import (
    ALLOWED_CELLS,
    CONTRACT,
    FORBIDDEN_AUTHORITY_IDS,
    PINNED_AUTHORITY_CONTENT_HASH,
    PINNED_AUTHORITY_ID,
    ApplicabilityMaterial,
    CellPlan,
    OwnerOnlySelectedIngress,
    SelectedIngressAuthenticationError,
    SelectedIngressC1StateError,
    SelectedIngressError,
    SelectedIngressG2Error,
    SelectedIngressPermissionError,
    SelectedRequest,
    IDENTITY_KEY_TYPES,
    REQUIRED_IDENTITY_KEYS,
    _key,
)
from rawlsing_next import pre553_ee14_c1_owner_authenticated_ingress as INGRESS_MODULE
from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_pre553_empirical_query import _query_authority, _registry

MARKER = "TEST_ONLY_UNISSUED__NOT_AN_EE14_GRANT__G1_INTERNAL_OWNER_PATH_CANDIDATE_ONLY"

SERVICE = "REVERSE_POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_INFERENCE"

# Exact HQ253 T01 conditions and tags -- never re-derived.
Q1_CONDITIONS = (("RESPONSE", "A", 1),)
Q2_CONDITIONS = (("RESPONSE", "A", 1), ("RESPONSE", "B", 0))
Q1_TAG, Q2_TAG = "hq253-qA", "hq253-qAB"
Q1_STRATUM, Q2_STRATUM = ("c0",), ("c0", "c1")

# Frozen external XOR oracle -- the original four-respondent figures.
FROZEN_Q1_DENOMINATOR = 2
FROZEN_Q1_C0, FROZEN_Q1_C1 = 1, 1        # 1/2, 1/2
FROZEN_Q2_DENOMINATOR = 1
FROZEN_Q2_C0, FROZEN_Q2_C1 = 0, 1        # 0/1, 1/1
FROZEN_RESPONDENTS = 4


def _h(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:hq266:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"HQ266-FIXTURE-ONLY-{tag}", "1.0.0", _h(f"auth:{tag}"))


CANDIDATE_CLASS = ref("TARGET_QUESTION_CLASS", "hq266-class-1")
TARGET_USE_REF = ref("TARGET_USE", "hq266-fixture-target-use")
PERMISSION_REF = ref("TARGET_USE_PERMISSION", "hq266-fixture-perm-only")
POPULATION_REF = ref("POPULATION_SCOPE", "hq266-fixture-pop")
GEOGRAPHY_REF = ref("GEOGRAPHY_SCOPE", "hq266-fixture-geo")
INTERVAL_REF = ref("TIME_INTERVAL", "hq266-fixture-2018")
OTHER_PERMISSION_REF = ref("TARGET_USE_PERMISSION", "hq266-other-perm")
OTHER_RELEASE = ref("C11LogicalRelease", "hq266-other-release")
OTHER_UNIVERSE = ref("EmpiricalUniverse@1.0.0", "hq266-other-universe")
OTHER_BASIS = ref("TARGET_QUESTION", "hq266-negative-basis")


# ============================================================ FIXTURES


@pytest.fixture(scope="module")
def source():
    """The ONE shared original four-respondent XOR source, built exactly once."""
    return fx.xor_fixture()


@pytest.fixture(scope="module")
def qauth():
    """The EXACT HQ253 grammar query authority. Never _query_snapshot()."""
    return _query_authority("c1-at09-xor")


@pytest.fixture(scope="module")
def registry(source, qauth):
    return _registry(source, qauth)


def _compose(**kwargs):
    """Owner-built C1 compose over the exact HQ253 construction.

    Returns the (composition, consumer_query) pair the ingress requires. The ingress
    supplies source/qauth/registry itself, so a caller cannot steer the source or the
    query authority.
    """
    composition, consumer_query, _witness, _pq, _predicate = (
        fx.direct_condition_composition(**kwargs))
    return composition, consumer_query


def _plans(source):
    return {
        "q1": CellPlan(cell="q1", conditions=Q1_CONDITIONS, target_question="C",
                       tag=Q1_TAG, stratum_ids=Q1_STRATUM,
                       model_rule=fx.make_model_rule(source["universe"].ref, Q1_TAG)),
        "q2": CellPlan(cell="q2", conditions=Q2_CONDITIONS, target_question="C",
                       tag=Q2_TAG, stratum_ids=Q2_STRATUM,
                       model_rule=fx.make_model_rule(source["universe"].ref, Q2_TAG)),
    }


def _expected_identity(source, qauth, registry):
    """Non-mutable owner-held expected C1 identity, computed once from the honest path."""
    identity = {}
    for cell, plan in _plans(source).items():
        composition, _cq = _compose(
            source=source, qauth=qauth, registry=registry,
            conditions=plan.conditions, target_question=plan.target_question, tag=plan.tag)
        evidence = composition.possibility_slice_evidence_or_null
        identity[cell] = {
            "composed_result_identity_hash": composition.composed_result_identity_hash,
            "producer_predicate_key": _key(composition.producer_predicate_ref),
            "producer_query_key": _key(composition.producer_query_ref),
            "producer_fact_key": _key(composition.producer_fact_ref),
            "condition_binding_witness_key": _key(
                composition.condition_binding_witness_ref_or_hash),
            "consumer_query_key": _key(composition.consumer_query_ref),
            "risk_set_key": _key(composition.risk_set_ref),
            "denominator_member_keys": tuple(
                _key(r) for r in composition.denominator_member_refs),
            "raw_denominator_support": composition.raw_denominator_support,
            "evidence_ref_key": _key(evidence.evidence_ref),
            "source_universe_key": _key(evidence.source_universe_ref),
            "release_key": _key(evidence.release_ref),
            "evidence_state": evidence.evidence_state,
            "retained_conditioner_ids": tuple(evidence.retained_conditioner_ids),
            "evidence_authority_keys": tuple(_key(a) for a in evidence.authority_refs),
            "evidence_provenance_keys": tuple(_key(p) for p in evidence.provenance_refs),
            "target_question_key": _key(evidence.target_ref),
            "source_universe_key_owner": source["universe"].ref.object_id,
            "release_key_owner": source["release_ref"].object_id,
        }
    return identity


def _applicability(admission_decision="ADMITTED", basis_refs=()):
    """REAL test-only unissued applicability material for the ACCEPTED owner."""
    return ApplicabilityMaterial(
        service_id=SERVICE,
        service_authority_ref=auth("service-fixture-only"),
        target_use_ref=TARGET_USE_REF,
        population_scope_ref=POPULATION_REF,
        geography_scope_ref=GEOGRAPHY_REF,
        effective_time_or_interval_ref=INTERVAL_REF,
        candidate_class_ref=CANDIDATE_CLASS,
        target_use_permission_refs=(PERMISSION_REF,),
        binding_authority_ref=auth("class-fixture-only"),
        admission_authority_ref=auth("admission-fixture-only"),
        binding_request_id="hq266-breq-1",
        admission_decision=admission_decision,
        admission_basis_refs=tuple(basis_refs),
    )


def build_ingress(source, qauth, registry, *, c1_compose=_compose,
                  applicability=None, owner_identity=None, plans=None):
    return OwnerOnlySelectedIngress(
        source=source,
        qauth=qauth,
        registry=registry,
        cells=plans if plans is not None else _plans(source),
        applicability=applicability if applicability is not None else _applicability(),
        owner_identity=(owner_identity if owner_identity is not None
                        else _expected_identity(source, qauth, registry)),
        c1_compose=c1_compose,
    )


@pytest.fixture(scope="module")
def ingress(source, qauth, registry):
    return build_ingress(source, qauth, registry)


@pytest.fixture()
def f8_calls(monkeypatch):
    """Count real bound-F8 invocations so 'ZERO F8 on refusal' is proven, not asserted."""
    counter = {"n": 0}
    original = B.evaluate_bound_positioned_subject_possibility

    def counting(*args, **kwargs):
        counter["n"] += 1
        return original(*args, **kwargs)

    monkeypatch.setattr(B, "evaluate_bound_positioned_subject_possibility", counting)
    return counter


@pytest.fixture()
def chain_calls(monkeypatch):
    """Count invocations of each accepted owner in the real C1 -> G2 -> F8 chain."""
    counts = {"compose": 0, "applicability": 0, "binder": 0, "evaluate": 0}
    original_compose = fx.direct_condition_composition
    original_resolve = SA.resolve_service_source_applicability
    original_bind = B.bind_service_applicability_to_f8_scope
    original_eval = B.evaluate_bound_positioned_subject_possibility

    def compose(*a, **k):
        counts["compose"] += 1
        return original_compose(*a, **k)

    def resolve(*a, **k):
        counts["applicability"] += 1
        return original_resolve(*a, **k)

    def bind(*a, **k):
        counts["binder"] += 1
        return original_bind(*a, **k)

    def evaluate(*a, **k):
        counts["evaluate"] += 1
        return original_eval(*a, **k)

    monkeypatch.setattr(fx, "direct_condition_composition", compose)
    monkeypatch.setattr(SA, "resolve_service_source_applicability", resolve)
    monkeypatch.setattr(B, "bind_service_applicability_to_f8_scope", bind)
    monkeypatch.setattr(B, "evaluate_bound_positioned_subject_possibility", evaluate)
    return counts


# ============================================================ 0. POSITIVE CONTROL
# The EXACT HQ253 T01 construction, asserted before anything else.


def test_positive_control_uses_the_exact_hq253_query_authority(qauth):
    """The pinned grammar authority, not _query_snapshot()."""
    fields = qauth.semantic_fields
    assert fields["authority_kind"] == "PREDICATE_GRAMMAR"
    assert fields["authority_id"] == PINNED_AUTHORITY_ID == "I03-AUTH-c1-at09-xor"
    assert fields["authority_content_hash"] == PINNED_AUTHORITY_CONTENT_HASH
    assert tuple(fields["governed_operations"]) == ("I03-OP-c1-at09-xor",)
    assert tuple(sorted(fields["governed_object_families"])) == tuple(sorted(
        ("EmpiricalFact@1.0.0", "EmpiricalPredicate@1.0.0", "EmpiricalQuerySpec@1.0.0")))


def test_positive_control_rejects_the_query_snapshot_substitute():
    """The commission's hard-forbidden substitution is refused structurally."""
    from rawlsing_next.tests.test_pre553_analytical_composition import _query_snapshot
    snapshot = _query_snapshot()
    assert snapshot.semantic_fields["authority_id"] in FORBIDDEN_AUTHORITY_IDS
    with pytest.raises(SelectedIngressError) as exc:
        OwnerOnlySelectedIngress(
            source=None, qauth=snapshot, registry=None, cells=_plans_stub(),
            applicability=_applicability(), owner_identity={}, c1_compose=_compose)
    assert "substitute" in str(exc.value) or "snapshot" in str(exc.value)


def _plans_stub():
    return {c: CellPlan(cell=c, conditions=Q1_CONDITIONS, target_question="C",
                        tag=Q1_TAG, stratum_ids=Q1_STRATUM, model_rule=None)
            for c in ALLOWED_CELLS}


def test_positive_control_source_release_and_universe(source):
    assert source["release_ref"].object_id == "REL-c1-at09-xor"
    assert source["universe"].ref.content_hash == (
        "318719f670e52a093a9a87ea92f3faf91555c7e1999b03dd47689964483f605c")


def test_positive_control_q1_and_q2_exact_xor_figures(source, qauth, registry):
    """THE ORIGINAL XOR FIGURES, produced by the exact HQ253 construction."""
    for cell, conditions, expected_denom, expected_c0, expected_c1 in (
        ("q1", Q1_CONDITIONS, FROZEN_Q1_DENOMINATOR, FROZEN_Q1_C0, FROZEN_Q1_C1),
        ("q2", Q2_CONDITIONS, FROZEN_Q2_DENOMINATOR, FROZEN_Q2_C0, FROZEN_Q2_C1),
    ):
        plan = _plans(source)[cell]
        composition, consumer_query = _compose(
            source=source, qauth=qauth, registry=registry,
            conditions=plan.conditions, target_question="C", tag=plan.tag)
        assert composition.analytical_state == "SUPPORTED"
        assert composition.producer_fact_state == "SUPPORTED"
        assert composition.possibility_slice_evidence_or_null is not None
        assert composition.consumer_result_or_null is not None
        assert composition.raw_denominator_support == expected_denom
        cells = {c["cell"]: c for c in consumer_query and composition.consumer_result_or_null
                 .material()["exact_lane"]["geometry"]["cells"]}
        assert cells["0"]["raw_numerator_support"] == expected_c0
        assert cells["1"]["raw_numerator_support"] == expected_c1


# ============================================================ 1. POSITIVE INGRESS


@pytest.mark.parametrize("cell", ALLOWED_CELLS)
def test_positive_owner_originated_ingress(ingress, cell):
    """Positive: the owner executes C1 and the receipt binds the full C1 identity."""
    ids = Q1_STRATUM if cell == "q1" else Q2_STRATUM
    r = ingress.serve(SelectedRequest(cell=cell, stratum_ids=ids))
    assert r.contract == CONTRACT
    assert r.cell == cell
    assert len(r.c1_identity_hash) == 64
    assert r.c1_evidence_ref_key
    assert r.c1_evidence_authority_keys, "C1-originated evidence must carry authority custody"
    assert r.c1_evidence_provenance_keys, "C1-originated evidence must carry provenance"
    assert len(r.f8_result_hash) == 64
    assert len(r.origin_receipt_hash) == 64
    assert r.authorizing is False


def test_positive_receipt_binds_full_c1_lineage_not_just_f8(ingress):
    r = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    # the receipt carries C1 identity AND the C1 evidence preimage AND the F8 hash, so a
    # caller who keeps only the F8 number cannot reconstruct a selected receipt
    assert r.c1_identity_hash != r.f8_result_hash
    assert r.origin_receipt_hash not in (r.c1_identity_hash, r.f8_result_hash)


def test_positive_is_deterministic_for_the_same_request(ingress):
    a = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    b = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert a.origin_receipt_hash == b.origin_receipt_hash
    assert a.f8_result_hash == b.f8_result_hash


# ============================================================ F1 -- REAL G2 CHAIN


def test_f1_positive_uses_every_accepted_owner_in_the_real_chain(
        ingress, source, chain_calls):
    """The chain really runs: C1 -> applicability -> accepted binder -> bound F8."""
    ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert chain_calls["compose"] >= 1
    assert chain_calls["applicability"] >= 1
    assert chain_calls["binder"] >= 1
    assert chain_calls["evaluate"] >= 1


def test_counter_control_bound_f8_actually_runs_on_the_positive_path(ingress, f8_calls):
    """NON-VACUITY: every later 'ZERO F8 on refusal' assertion is only meaningful if the
    same counter increments on a path that is supposed to reach F8."""
    assert f8_calls["n"] == 0
    ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert f8_calls["n"] == 1, "the positive path must reach the real bound-F8 evaluator"


def test_f1_receipt_carries_a_real_g2_receipt_and_binding_not_a_scope_hash(ingress):
    """F1's core: real G2 identities are bound instead of a locally hashed scope."""
    r = ingress.serve(SelectedRequest(cell="q2", stratum_ids=Q2_STRATUM))
    assert not hasattr(r, "applicability_scope_hash")
    assert r.g2_receipt_outcome == SA.OUTCOME_ADMISSIBLE_SET
    assert r.g2_service_request_set_identity
    assert len(r.g2_receipt_hash) == 64
    assert r.g2_binding_request_id == "hq266-breq-1"
    assert len(r.g2_binding_hash) == 64
    assert r.g2_permission_keys == (PERMISSION_REF.object_id,)
    assert r.g2_query_authority_id == PINNED_AUTHORITY_ID
    assert r.g2_replay_protocol_key


def test_f1_no_locally_hashed_scope_stand_in_remains():
    """The literal `_applicability_scope` stand-in is gone from the ingress source."""
    import pathlib
    import rawlsing_next.pre553_ee14_c1_owner_authenticated_ingress as M
    source_text = pathlib.Path(M.__file__).read_text(encoding="utf-8")
    assert "self._applicability_scope" not in source_text
    assert "_applicability_scope" not in source_text


def test_f1_ingress_is_wired_to_the_real_binder_and_has_no_bypass(
        ingress, monkeypatch, f8_calls):
    """Make the real binder raise: the ingress must surface that exact G2 refusal.

    This is the F1 probe. Before the repair the ingress never called the binder at all,
    so no binder refusal could ever surface. If it bypasses the binder it will silently
    fall through to raw F8 instead, which this test forbids.
    """
    def refusing(*args, **kwargs):
        raise B.ServiceF8ScopeBindingError(
            "BINDING_RELEASE_GRAIN_MISMATCH", "refused at the accepted binder")

    monkeypatch.setattr(B, "bind_service_applicability_to_f8_scope", refusing)
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert "BINDING_RELEASE_GRAIN_MISMATCH" in str(exc.value)
    assert f8_calls["n"] == 0, "F8 must not run when the real binder refuses"


def test_f1_real_binder_refuses_permission_identity_mismatch():
    """The accepted binder's own permission refusal still exists (proved directly)."""
    source = fx.xor_fixture()
    composition, _cq = _compose(
        source=source, qauth=_query_authority("c1-at09-xor"),
        registry=_registry(source, _query_authority("c1-at09-xor")),
        conditions=Q2_CONDITIONS, target_question="C", tag=Q2_TAG)
    receipt = _real_receipt(source)
    rule = fx.make_model_rule(source["universe"].ref, Q2_TAG)
    request = dataclasses.replace(
        _g2_request(source, receipt),
        bound_target_use_permission_refs=(OTHER_PERMISSION_REF,))
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        B.bind_service_applicability_to_f8_scope(request=request, receipt=receipt, rule=rule)
    assert "BINDING_PERMISSION_IDENTITY_MISMATCH" in str(exc.value)


def test_f1_real_binder_refuses_substituted_release(source):
    receipt = _real_receipt(source)
    rule = fx.make_model_rule(source["universe"].ref, Q2_TAG)
    request = dataclasses.replace(_g2_request(source, receipt),
                                  release_identity_ref=OTHER_RELEASE)
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        B.bind_service_applicability_to_f8_scope(request=request, receipt=receipt, rule=rule)
    assert "BINDING_RELEASE_GRAIN_MISMATCH" in str(exc.value)


def test_f1_real_binder_refuses_foreign_source_universe(source):
    receipt = _real_receipt(source)
    rule = fx.make_model_rule(source["universe"].ref, Q2_TAG)
    request = dataclasses.replace(_g2_request(source, receipt),
                                  requested_source_universe_ref=OTHER_UNIVERSE)
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        B.bind_service_applicability_to_f8_scope(request=request, receipt=receipt, rule=rule)
    assert "REQUESTED_SOURCE_NOT_ADMITTED" in str(exc.value)


def test_f1_bound_f8_equals_direct_c1_for_both_cells(ingress, source, qauth, registry):
    for cell, stratum in (("q1", Q1_STRATUM), ("q2", Q2_STRATUM)):
        r = ingress.serve(SelectedRequest(cell=cell, stratum_ids=stratum))
        plan = _plans(source)[cell]
        composition, _cq = _compose(
            source=source, qauth=qauth, registry=registry,
            conditions=plan.conditions, target_question="C", tag=plan.tag)
        direct = composition.consumer_result_or_null
        assert r.f8_result_hash == direct.result_hash
        assert r.f8_result_state == "EXACT_SUPPORTED"
        assert r.f8_matches_direct_c1 is True


def test_f1_no_currentness_is_claimed(ingress):
    r = ingress.serve(SelectedRequest(cell="q2", stratum_ids=Q2_STRATUM))
    assert "CURRENT" not in repr(dataclasses.asdict(r))
    assert r.authorizing is False


def test_receipt_is_not_a_grant_and_grants_no_permission(ingress):
    r = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert r.authorizing is False
    assert not hasattr(r, "grant_ref")
    assert not hasattr(r, "ee14_grant")
    assert not hasattr(r, "currentness")


# ============================================================ F2 -- GENUINE q1/q2


def test_f2_receipts_carry_the_exact_xor_denominators(ingress):
    r1 = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    r2 = ingress.serve(SelectedRequest(cell="q2", stratum_ids=Q2_STRATUM))
    assert r1.c1_raw_denominator_support == FROZEN_Q1_DENOMINATOR == 2
    assert r2.c1_raw_denominator_support == FROZEN_Q2_DENOMINATOR == 1
    assert len(r1.c1_denominator_member_keys) == 2
    assert len(r2.c1_denominator_member_keys) == 1


def test_f2_q1_and_q2_have_distinct_producer_identity(ingress):
    r1 = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    r2 = ingress.serve(SelectedRequest(cell="q2", stratum_ids=Q2_STRATUM))
    assert r1.c1_identity_hash != r2.c1_identity_hash
    assert r1.c1_producer_predicate_key != r2.c1_producer_predicate_key
    assert r1.c1_producer_query_key != r2.c1_producer_query_key
    assert r1.c1_producer_fact_key != r2.c1_producer_fact_key
    assert r1.c1_evidence_ref_key != r2.c1_evidence_ref_key
    assert r1.c1_denominator_member_keys != r2.c1_denominator_member_keys


def test_f2_q1_and_q2_share_exactly_one_source_and_release(ingress):
    r1 = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    r2 = ingress.serve(SelectedRequest(cell="q2", stratum_ids=Q2_STRATUM))
    assert r1.source_universe_key == r2.source_universe_key
    assert r1.release_key == r2.release_key == "REL-c1-at09-xor"


def test_f2_q1_and_q2_results_are_not_a_marginal_product(ingress, source, qauth, registry):
    """AT09's anti-vacuity: flat marginals vs a decisive joint, on real counts."""
    r1 = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    r2 = ingress.serve(SelectedRequest(cell="q2", stratum_ids=Q2_STRATUM))
    cells1 = _direct_cells(source, qauth, registry, Q1_CONDITIONS, Q1_TAG)
    cells2 = _direct_cells(source, qauth, registry, Q2_CONDITIONS, Q2_TAG)
    assert (cells1["0"], cells1["1"]) == (FROZEN_Q1_C0, FROZEN_Q1_C1)
    assert (cells2["0"], cells2["1"]) == (FROZEN_Q2_C0, FROZEN_Q2_C1)
    assert cells1 != cells2
    # q2 is an intersection of one respondent, never a product of q1's marginals
    assert r2.c1_raw_denominator_support == 1
    assert r1.c1_raw_denominator_support == 2
    assert FROZEN_RESPONDENTS == 4


def test_f2_cell_label_flip_is_refused_no_substitution(ingress):
    """Serving q1's cell with q2's grain (or the reverse) is refused."""
    with pytest.raises(SelectedIngressError):
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q2_STRATUM))
    with pytest.raises(SelectedIngressError):
        ingress.serve(SelectedRequest(cell="q2", stratum_ids=Q1_STRATUM))


def test_hostile_stratum_mismatch_refused_without_substitution(ingress):
    with pytest.raises(SelectedIngressError) as e:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=("not", "the", "grain")))
    assert "grain" in str(e.value) or "substitution" in str(e.value)


# ============================================================ F3 -- DEEP AUTHENTICATION


def _hostile_compose(real, *, mutate=None, replace_identity=False):
    """Wrap the honest compose and inject an alteration BEFORE the ingress sees it.

    Simulates in-flight mutation between the C1 return and the F8 call.
    """
    def compose(**kwargs):
        composition, consumer_query = real(**kwargs)
        if mutate is not None:
            evidence = mutate(composition.possibility_slice_evidence_or_null)
            composition = dataclasses.replace(
                composition, possibility_slice_evidence_or_null=evidence)
        if replace_identity:
            composition = dataclasses.replace(
                composition, composed_result_identity_hash="f" * 64)
        return composition, consumer_query
    return compose


def test_f3_provenance_substitution_refused_before_f8(
        source, qauth, registry, f8_calls):
    def mutate(evidence):
        return dataclasses.replace(
            evidence, provenance_refs=(ref("UNRELATED_PROVENANCE", "forged"),))

    ingress = build_ingress(source, qauth, registry, c1_compose=_hostile_compose(
        _compose, mutate=mutate))
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert f8_calls["n"] == 0, "refusal must happen BEFORE any F8 invocation"
    assert exc.value.f8_invoked is False
    assert "evidence_provenance_keys" in exc.value.mismatched_fields


def test_f3_authority_substitution_refused_before_f8(source, qauth, registry, f8_calls):
    def mutate(evidence):
        return dataclasses.replace(
            evidence, authority_refs=(auth("forged-evidence-authority"),))

    ingress = build_ingress(source, qauth, registry, c1_compose=_hostile_compose(
        _compose, mutate=mutate))
    with pytest.raises(SelectedIngressAuthenticationError):
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert f8_calls["n"] == 0


def test_f3_evidence_ref_substitution_refused_before_f8(source, qauth, registry, f8_calls):
    def mutate(evidence):
        return dataclasses.replace(
            evidence, evidence_ref=ref("C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1", "other"))

    ingress = build_ingress(source, qauth, registry, c1_compose=_hostile_compose(
        _compose, mutate=mutate))
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert f8_calls["n"] == 0
    assert "evidence_ref_key" in exc.value.mismatched_fields


def test_f3_forged_composed_identity_refused_before_f8(source, qauth, registry, f8_calls):
    ingress = build_ingress(
        source, qauth, registry,
        c1_compose=_hostile_compose(_compose, replace_identity=True))
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert f8_calls["n"] == 0
    assert "composed_result_identity_hash" in exc.value.mismatched_fields


def test_f3_denominator_substitution_refused_before_f8(source, qauth, registry, f8_calls):
    """Swapping q2's denominator onto q1's cell is caught by structured comparison."""

    def compose(**kwargs):
        composition, consumer_query = _compose(**kwargs)
        if kwargs.get("tag") == Q1_TAG:
            composition = dataclasses.replace(composition, raw_denominator_support=1)
        return composition, consumer_query

    ingress = build_ingress(source, qauth, registry, c1_compose=compose)
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert f8_calls["n"] == 0
    assert "raw_denominator_support" in exc.value.mismatched_fields


def test_f3_authentication_is_structural_not_a_hash_length_regex(
        source, qauth, registry):
    """The check compares named fields, so a wrong-but-correctly-sized value is caught."""
    ingress = build_ingress(source, qauth, registry)
    expected = ingress.owner_scope_material()["owner_identity"]["q1"]
    # every field is compared by name; a 64-hex impostor in any of them would fail
    assert "composed_result_identity_hash" in expected
    assert expected["raw_denominator_support"] == FROZEN_Q1_DENOMINATOR
    assert expected["retained_conditioner_ids"] == Q1_STRATUM


def test_f3_owner_identity_is_deeply_frozen_after_construction(source, qauth, registry):
    ingress = build_ingress(source, qauth, registry)
    material = ingress.owner_scope_material()
    with pytest.raises(TypeError):
        material["owner_identity"]["q1"]["composed_result_identity_hash"] = "f" * 64
    with pytest.raises(TypeError):
        material["owner_identity"]["q1"]["denominator_member_keys"] = ("injected",)


def test_c3_provenance_substitution_keeps_the_f8_number_yet_the_ingress_refuses_it(
        source, qauth, registry, f8_calls):
    """The custody gap F8 cannot close, and the ingress step that does.

    HQ253 proved that substituting only `provenance_refs` leaves the F8 result hash
    UNCHANGED, so F8 parity alone is NOT proof of producer custody. This test shows both
    halves at once: the accepted chain reproduces that identical-hash false positive, and
    the ingress's authentication refuses it BEFORE F8, so parity can no longer be reached
    by a substituted producer.
    """
    from dataclasses import replace as dc_replace

    plan = _plans(source)["q2"]
    composition, consumer_query = _compose(
        source=source, qauth=qauth, registry=registry,
        conditions=plan.conditions, target_question="C", tag=plan.tag)
    genuine = composition.possibility_slice_evidence_or_null
    forged = dc_replace(
        genuine, provenance_refs=(ref("UNRELATED_PROVENANCE", "hq266-custody"),))

    # --- half 1: through the ACCEPTED chain, provenance substitution keeps the hash ---
    receipt = _real_receipt(source)
    rule = fx.make_model_rule(source["universe"].ref, Q2_TAG)
    g2_request = _g2_request(source, receipt)
    binding = B.bind_service_applicability_to_f8_scope(
        request=g2_request, receipt=receipt, rule=rule)
    baseline = B.evaluate_bound_positioned_subject_possibility(
        binding=binding, request=g2_request, receipt=receipt,
        query=consumer_query, rule=rule, evidence=(genuine,))
    mutated = B.evaluate_bound_positioned_subject_possibility(
        binding=binding, request=g2_request, receipt=receipt,
        query=consumer_query, rule=rule, evidence=(forged,))
    assert baseline.result_hash == mutated.result_hash, (
        "the known custody false positive must still reproduce, or this control is vacuous")
    assert mutated.result_state == "EXACT_SUPPORTED"

    # --- half 2: the ingress refuses the same substitution BEFORE any F8 call ---
    # reset: half 1 deliberately called the accepted F8 evaluator directly, and the
    # number that matters here is only what the INGRESS causes to run.
    f8_calls["n"] = 0

    def compose(**kwargs):
        c, cq = _compose(**kwargs)
        return dc_replace(c, possibility_slice_evidence_or_null=forged), cq

    ingress = build_ingress(source, qauth, registry, c1_compose=compose)
    with pytest.raises(SelectedIngressAuthenticationError):
        ingress.serve(SelectedRequest(cell="q2", stratum_ids=Q2_STRATUM))
    assert f8_calls["n"] == 0


# ============================================================ F4 -- TYPED C1 NEGATIVES


def _zero_support_compose(**kwargs):
    """A GENUINE native C1 negative on the SAME XOR source: no respondent satisfies the
    condition, so the producer returns its real ZERO_SUPPORT state and null evidence."""
    conditions = kwargs.get("conditions") or ()
    poisoned = tuple(c[:2] + (99,) for c in conditions)
    kwargs = dict(kwargs)
    kwargs["conditions"] = poisoned
    return _compose(**kwargs)


def test_f4_native_negative_yields_typed_c1_state_error_with_zero_f8(
        source, qauth, registry, f8_calls):
    ingress = build_ingress(source, qauth, registry, c1_compose=_zero_support_compose)
    with pytest.raises(SelectedIngressC1StateError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert f8_calls["n"] == 0, "ZERO F8 invocation on a native C1 negative"
    assert exc.value.f8_invoked is False
    assert exc.value.native_state == "ZERO_SUPPORT"
    assert exc.value.producer_fact_state == "ZERO_SUPPORT"


def test_f4_native_negative_is_not_attributed_to_a_missing_g0b(
        source, qauth, registry):
    """F4's core: an intrinsic C1 outcome is never relabelled 'no G0b'."""
    ingress = build_ingress(source, qauth, registry, c1_compose=_zero_support_compose)
    with pytest.raises(SelectedIngressC1StateError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    message = str(exc.value)
    assert "ZERO_SUPPORT" in message
    assert "intrinsic C1" in message or "intrinsic C1 outcome" in message
    assert "NOT a missing-EE14-G0b" in message
    # and it is NOT the permission error type
    assert not isinstance(exc.value, SelectedIngressPermissionError)
    assert exc.value.applicability_invoked is False


def test_f4_unknown_state_is_refused_rather_than_coerced(source, qauth, registry, f8_calls):
    def compose(**kwargs):
        composition, consumer_query = _compose(**kwargs)
        composition = dataclasses.replace(
            composition, analytical_state="NOT_A_REAL_STATE")
        return composition, consumer_query

    ingress = build_ingress(source, qauth, registry, c1_compose=compose)
    with pytest.raises(SelectedIngressC1StateError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert f8_calls["n"] == 0
    assert exc.value.native_state == "UNKNOWN_OR_UNRESOLVED"


def test_f4_no_admitted_source_is_a_distinct_applicability_reason(
        source, qauth, registry, f8_calls):
    """NO_ADMITTED_SOURCE is an applicability outcome, distinct from a C1 negative."""
    ingress = build_ingress(
        source, qauth, registry,
        applicability=_applicability(
            admission_decision="SOURCE_NOT_APPLICABLE_TO_THIS_SERVICE_AND_USE",
            basis_refs=(OTHER_BASIS,)))
    with pytest.raises(SelectedIngressG2Error) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert exc.value.reason_code == "NO_ADMITTED_SOURCE"
    assert f8_calls["n"] == 0
    assert not isinstance(exc.value, SelectedIngressC1StateError)
    assert "not a C1 native negative" in str(exc.value)


def test_f4_permission_error_is_a_separate_type_not_used_for_c1_negatives():
    """The permission error still exists as a distinct type and is never what a native
    C1 negative raises, so 'no G0b' can never be conflated with an intrinsic C1 outcome."""
    assert issubclass(SelectedIngressPermissionError, SelectedIngressError)
    assert not issubclass(SelectedIngressC1StateError, SelectedIngressPermissionError)
    assert not issubclass(SelectedIngressAuthenticationError, SelectedIngressPermissionError)
    assert not issubclass(SelectedIngressG2Error, SelectedIngressPermissionError)


#: The commission names these native states. ZERO_SUPPORT is the one genuinely
#: constructible on this XOR source (and maps to UNDERPOWERED in the accepted
#: pre553_analytical_state_and_route route table). The rest are verified here as
#: HANDLER-ACCURATE: the ingress reports whatever native state C1 actually returned,
#: rather than flattening every non-SUPPORTED outcome into one message.
@pytest.mark.parametrize("native_state", [
    "ZERO_SUPPORT", "VALID_EMPTY", "NONCOMPARABLE",
    "UNRESOLVED", "OBSERVED_ZERO", "LOW_SUPPORT", "INTEGRITY_FAILURE",
])
def test_f4_handler_reports_the_exact_native_state_it_received(
        native_state, source, qauth, registry, f8_calls):
    assert native_state in INGRESS_MODULE.NATIVE_C1_FACT_STATES

    def compose(**kwargs):
        composition, consumer_query = _compose(**kwargs)
        composition = dataclasses.replace(
            composition, analytical_state=native_state,
            producer_fact_state=native_state)
        return composition, consumer_query

    ingress = build_ingress(source, qauth, registry, c1_compose=compose)
    with pytest.raises(SelectedIngressC1StateError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))

    assert f8_calls["n"] == 0, "ZERO F8 invocation for every native negative"
    assert exc.value.native_state == native_state, (
        "the handler must report the exact state it received, not a generic message")
    assert exc.value.f8_invoked is False
    assert not isinstance(exc.value, SelectedIngressPermissionError)


def test_f4_underpowered_route_family_is_not_silently_accepted(source, qauth, registry):
    """UNDERPOWERED names a route family, not an empirical fact state; refuse it."""
    assert "UNDERPOWERED" not in INGRESS_MODULE.NATIVE_C1_FACT_STATES

    def compose(**kwargs):
        composition, consumer_query = _compose(**kwargs)
        composition = dataclasses.replace(
            composition, analytical_state="UNDERPOWERED",
            producer_fact_state="UNDERPOWERED")
        return composition, consumer_query

    ingress = build_ingress(source, qauth, registry, c1_compose=compose)
    with pytest.raises(SelectedIngressC1StateError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert exc.value.native_state == "UNKNOWN_OR_UNRESOLVED"


# ============================================================ F5 -- EXACT TYPES


def test_f5_subclass_of_selected_request_is_refused(ingress):
    class Extra(SelectedRequest):
        arbitrary = object()

    ids = Q1_STRATUM
    with pytest.raises(SelectedIngressError):
        ingress.serve(Extra(cell="q1", stratum_ids=ids))


def test_f5_subclass_of_str_is_refused_as_a_stratum_entry(ingress):
    class StrSub(str):
        pass

    with pytest.raises(SelectedIngressError):
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=(StrSub("c0"),)))


def test_f5_subclass_of_tuple_is_refused_as_stratum_ids(ingress):
    class TupleSub(tuple):
        pass

    with pytest.raises(SelectedIngressError):
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=TupleSub(("c0",))))


def test_f5_subclass_of_str_is_refused_as_a_cell(ingress):
    class CellSub(str):
        pass

    with pytest.raises(SelectedIngressError):
        ingress.serve(SelectedRequest(cell=CellSub("q1"), stratum_ids=Q1_STRATUM))


def test_hostile_client_cannot_supply_evidence_at_all(ingress):
    """There is no request field through which evidence can arrive."""
    bad = SelectedRequest(cell="q1", stratum_ids=("x",))
    with pytest.raises(dataclasses.FrozenInstanceError):
        bad.evidence = object()
    assert not hasattr(SelectedRequest, "evidence")
    assert not hasattr(SelectedRequest, "authority_refs")
    assert not hasattr(SelectedRequest, "c1_result")
    assert not hasattr(SelectedRequest, "hash")


def test_owner_scope_material_is_read_only(ingress):
    scope = ingress.owner_scope_material()
    with pytest.raises(TypeError):
        scope["injected"] = True


def test_f5_owner_scope_material_is_deeply_read_only(ingress):
    scope = ingress.owner_scope_material()
    nested = scope["owner_identity"]["q1"]
    with pytest.raises(TypeError):
        nested["injected"] = True
    with pytest.raises(TypeError):
        scope["applicability"]["target_use_permission_refs"] = ("injected",)
    with pytest.raises(TypeError):
        scope["cells"]["q1"]["stratum_ids"] = ("injected",)


def test_owner_setup_requires_every_permitted_cell(source, qauth, registry):
    with pytest.raises(SelectedIngressError):
        OwnerOnlySelectedIngress(
            source=source, qauth=qauth, registry=registry, cells={},
            applicability=_applicability(),
            owner_identity=_expected_identity(source, qauth, registry),
            c1_compose=_compose)


def test_f5_owner_setup_requires_the_pinned_query_authority(source, registry):
    from rawlsing_next.tests.test_pre553_analytical_composition import _query_snapshot
    with pytest.raises(SelectedIngressError):
        OwnerOnlySelectedIngress(
            source=source, qauth=_query_snapshot(), registry=registry,
            cells=_plans(source), applicability=_applicability(),
            owner_identity=_expected_identity(
                source, _query_authority("c1-at09-xor"), registry),
            c1_compose=_compose)


@pytest.mark.parametrize("bad", [
    None, 42, "q1", [], {}, object(), b"q1",
    type("Sneaky", (), {})(),
])
def test_hostile_non_request_shapes_refused(ingress, bad):
    with pytest.raises(SelectedIngressError):
        ingress.serve(bad)


def test_hostile_stratum_ids_must_be_plain_strings(ingress):
    for bad in ((), ["a"], ("a", 1), (object(),), (None,)):
        with pytest.raises(SelectedIngressError):
            ingress.serve(SelectedRequest(cell="q1", stratum_ids=bad))


def test_hostile_unknown_cell_refused(ingress):
    with pytest.raises(SelectedIngressError):
        ingress.serve(SelectedRequest(cell="q3", stratum_ids=Q1_STRATUM))


# ============================================================ F6 -- REAL HOSTILES


def test_f6_forged_receipt_is_not_reconstructable_from_the_f8_number(ingress):
    """A caller who keeps only the observable F8 number cannot rebuild the receipt."""
    r = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    forged = "0" * 64
    assert r.origin_receipt_hash != forged
    assert r.origin_receipt_hash != r.f8_result_hash
    assert r.origin_receipt_hash != r.g2_receipt_hash
    assert r.origin_receipt_hash != r.g2_binding_hash
    # and there is no request channel to submit a hash into
    assert not hasattr(SelectedRequest, "origin_receipt_hash")


def test_hostile_recomputed_caller_hash_is_unusable(ingress):
    r = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    recomputed = _h(r.f8_result_hash)
    assert recomputed != r.origin_receipt_hash


def test_f6_hostile_compose_cannot_reach_f8_with_forged_provenance(
        source, qauth, registry, f8_calls):
    """F6's 'self-consistent forged C1/G2 receipt' attempted at the actual ingress."""
    forged_identity = _expected_identity(source, qauth, registry)

    def compose(**kwargs):
        composition, consumer_query = _compose(**kwargs)
        evidence = dataclasses.replace(
            composition.possibility_slice_evidence_or_null,
            provenance_refs=(ref("UNRELATED_PROVENANCE", "self-consistent"),),
            authority_refs=(auth("self-consistent"),),
        )
        composition = dataclasses.replace(
            composition, possibility_slice_evidence_or_null=evidence)
        return composition, consumer_query

    ingress = build_ingress(source, qauth, registry, c1_compose=compose,
                            owner_identity=forged_identity)
    with pytest.raises(SelectedIngressAuthenticationError):
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert f8_calls["n"] == 0


def test_f6_real_binder_refusal_surfaces_instead_of_a_silent_fallback(
        ingress, monkeypatch, f8_calls):
    def refusing(*args, **kwargs):
        raise B.ServiceF8ScopeBindingError(
            "BINDING_PERMISSION_IDENTITY_MISMATCH", "refused at the accepted binder")

    monkeypatch.setattr(B, "bind_service_applicability_to_f8_scope", refusing)
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        ingress.serve(SelectedRequest(cell="q2", stratum_ids=Q2_STRATUM))
    assert "BINDING_PERMISSION_IDENTITY_MISMATCH" in str(exc.value)
    assert f8_calls["n"] == 0


def test_f6_cross_source_proxy_is_refused_at_the_real_boundary(source):
    """Cross-source / proxy substitution reaches the accepted binder and is refused."""
    receipt = _real_receipt(source)
    rule = fx.make_model_rule(source["universe"].ref, Q2_TAG)
    request = dataclasses.replace(_g2_request(source, receipt),
                                  requested_source_universe_ref=OTHER_UNIVERSE)
    with pytest.raises(B.ServiceF8ScopeBindingError):
        B.bind_service_applicability_to_f8_scope(request=request, receipt=receipt, rule=rule)


def test_f6_walkback_wrong_service_is_refused(source):
    receipt = _real_receipt(source)
    rule = fx.make_model_rule(source["universe"].ref, Q2_TAG)
    request = dataclasses.replace(_g2_request(source, receipt),
                                  service_id="SOME_OTHER_SERVICE")
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        B.bind_service_applicability_to_f8_scope(request=request, receipt=receipt, rule=rule)
    assert "BINDING_SERVICE_GRAIN_MISMATCH" in str(exc.value)


def test_f6_walkback_wrong_request_receipt_is_refused(source):
    receipt = _real_receipt(source)
    rule = fx.make_model_rule(source["universe"].ref, Q2_TAG)
    request = dataclasses.replace(_g2_request(source, receipt),
                                  service_request_set_identity="f" * 64)
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        B.bind_service_applicability_to_f8_scope(request=request, receipt=receipt, rule=rule)
    assert "BINDING_REQUEST_RECEIPT_GRAIN_MISMATCH" in str(exc.value)


def test_low_level_f8_direct_call_can_never_mint_a_selected_receipt(source, qauth, registry):
    """F8 has no notion of the selected receipt; a direct call yields only the number."""
    composition, consumer_query = _compose(
        source=source, qauth=qauth, registry=registry,
        conditions=Q2_CONDITIONS, target_question="C", tag=Q2_TAG)
    from rawlsing_next.source_backed_positioned_subject_possibility import (
        evaluate_positioned_subject_possibility)
    low = evaluate_positioned_subject_possibility(
        query=consumer_query,
        rule=fx.make_model_rule(source["universe"].ref, Q2_TAG),
        evidence=(composition.possibility_slice_evidence_or_null,))
    assert not hasattr(low, "origin_receipt_hash")
    assert not hasattr(low, "authorizing")
    for field in ("c1_identity_hash", "g2_receipt_hash", "g2_binding_hash"):
        assert not hasattr(low, field)


def test_f6_owner_material_carries_no_grant_or_currentness(ingress):
    material = ingress.owner_scope_material()
    dumped = repr(dataclasses.asdict(_applicability()))
    assert "grant" not in dumped.lower()
    assert "CURRENT" not in repr(material)
    assert MARKER


def test_strong_same_process_monkeypatch_adversary_is_labelled_unproved():
    """Explicitly UNPROVED under the data-only contract. Not claimed as covered."""
    assert "UNPROVED" in INGRESS_MODULE.__doc__
    assert "NOT DEPLOYED" in INGRESS_MODULE.__doc__.upper()


# ============================================================ HELPERS


def _real_receipt(source):
    universe = source["universe"].ref
    mat = _applicability()
    candidate_class = SA.CandidateClassBinding(
        candidate_class_ref=CANDIDATE_CLASS.as_dict(),
        candidate_source_universe_refs=[universe.as_dict()],
        binding_authority_ref=mat.binding_authority_ref.as_dict(),
        declared_population_scope_ref=POPULATION_REF.as_dict(),
        declared_geography_scope_ref=GEOGRAPHY_REF.as_dict(),
    )
    service_request = SA.ServiceApplicabilityRequest.build(
        service_id=SERVICE,
        service_authority_ref=mat.service_authority_ref.as_dict(),
        target_use_ref=TARGET_USE_REF.as_dict(),
        population_scope_ref=POPULATION_REF.as_dict(),
        geography_scope_ref=GEOGRAPHY_REF.as_dict(),
        effective_time_or_interval_ref=INTERVAL_REF.as_dict(),
        candidate_class_ref=CANDIDATE_CLASS.as_dict(),
        release_identity_ref=source["release_ref"].as_dict(),
        target_use_permission_refs=[PERMISSION_REF.as_dict()],
        candidate_source_universe_refs=[universe.as_dict()],
    )
    admitted = SA.ApplicabilityAuthorityRecord(
        universe, "ADMITTED", mat.admission_authority_ref.as_dict())
    return SA.resolve_service_source_applicability(
        service_request, candidate_class, [admitted])


def _g2_request(source, receipt):
    universe = source["universe"].ref
    return B.ServiceApplicabilityF8ScopeBindingRequest(
        binding_request_id="hq266-breq-1",
        service_request_set_identity=receipt.service_request_set_identity,
        candidate_class_ref=CANDIDATE_CLASS,
        service_id=SERVICE,
        target_use_ref=TARGET_USE_REF,
        release_identity_ref=source["release_ref"],
        bound_target_use_permission_refs=(PERMISSION_REF,),
        binding_mode=B.MODE_SINGLE_SOURCE_VALIDATION,
        requested_source_universe_ref=universe,
        requested_currentness_claim=None,
        requested_purpose=None,
    )


def _direct_cells(source, qauth, registry, conditions, tag):
    composition, _cq = _compose(
        source=source, qauth=qauth, registry=registry,
        conditions=conditions, target_question="C", tag=tag)
    cells = composition.consumer_result_or_null.material()[
        "exact_lane"]["geometry"]["cells"]
    return {c["cell"]: c["raw_numerator_support"] for c in cells}


# ============================================================ HQ268 G01 -- D1 / D2 / R2
#
# D1  The owner-held expected C1 identity is COMPLETE, exact and typed BEFORE it is
#     trusted. Incomplete, mistyped or extraneous owner material is refused at owner
#     construction AND again immediately before the field-by-field comparison, so
#     authentication can never be vacuous and an incomplete owner setup reaches no
#     applicability, G2 or F8 call at all. This is an internal owner-setup
#     completeness invariant -- NOT an independent cryptographic trust root (R1).
# D2  `g2_receipt_hash` is the accepted owner's own
#     `CandidateClassApplicabilityReceipt.replay_identity()`, not a locally re-derived
#     subset, and `origin_receipt_hash` transitively includes it.
# R2  The live `_source` and `_cells` containers are read-only. The bounded residual
#     (nested objects stay the owner's shared objects -- shallow container freezing
#     only) is named rather than papered over.


def _identity_source_text():
    import pathlib
    import rawlsing_next.pre553_ee14_c1_owner_authenticated_ingress as M
    return pathlib.Path(M.__file__).read_text(encoding="utf-8")


def _build_with_identity(source, qauth, registry, identity, **kw):
    return build_ingress(source, qauth, registry, owner_identity=identity, **kw)


# ------------------------------------------------------------------ D1


def test_d1_required_key_set_is_closed_exact_and_typed(source, qauth, registry):
    """The required set is one closed set of 19 keys, every one with an exact type."""
    assert isinstance(REQUIRED_IDENTITY_KEYS, frozenset)
    assert set(IDENTITY_KEY_TYPES) == set(REQUIRED_IDENTITY_KEYS)
    assert len(REQUIRED_IDENTITY_KEYS) == 19
    # every observed key the ingress itself produces is in the required set
    honest = _expected_identity(source, qauth, registry)
    for cell in ALLOWED_CELLS:
        assert set(honest[cell]) == set(REQUIRED_IDENTITY_KEYS)
    # the type map is exhaustive and exact-builtin
    assert all(isinstance(v, type) for v in IDENTITY_KEY_TYPES.values())
    assert "bool" not in {t.__name__ for t in IDENTITY_KEY_TYPES.values()}


def test_d1_empty_owner_identity_is_refused_before_any_chain_owner(
        source, qauth, registry, chain_calls):
    """HQ267 P1b: `owner_identity={"q1": {}, "q2": {}}` must not be trusted.

    Before the repair this configuration passed authentication and was issued a
    selected technical receipt. It is now refused at owner construction, so it never
    reaches compose, applicability, the binder or F8.
    """
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        _build_with_identity(source, qauth, registry, {"q1": {}, "q2": {}})
    assert "INCOMPLETE" in str(exc.value)
    assert set(exc.value.missing_keys) == set(REQUIRED_IDENTITY_KEYS)
    assert exc.value.f8_invoked is False
    assert chain_calls["compose"] == 0
    assert chain_calls["applicability"] == 0
    assert chain_calls["binder"] == 0
    assert chain_calls["evaluate"] == 0


def test_d1_single_key_owner_identity_is_refused(
        source, qauth, registry, chain_calls):
    """A cell expectation holding exactly one key leaves 18 fields unverified."""
    full = _expected_identity(source, qauth, registry)
    one = {"q1": {"raw_denominator_support": full["q1"]["raw_denominator_support"]},
           "q2": {}}
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        _build_with_identity(source, qauth, registry, one)
    assert len(exc.value.missing_keys) == 18
    assert "raw_denominator_support" not in exc.value.missing_keys
    assert "evidence_provenance_keys" in exc.value.missing_keys
    assert chain_calls["applicability"] == chain_calls["evaluate"] == 0


def test_d1_missing_evidence_provenance_key_is_refused(
        source, qauth, registry, chain_calls):
    """Exactly the custody field HQ267 proved could be skipped."""
    identity = _expected_identity(source, qauth, registry)
    for cell in ALLOWED_CELLS:
        del identity[cell]["evidence_provenance_keys"]
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        _build_with_identity(source, qauth, registry, identity)
    assert exc.value.missing_keys == ("evidence_provenance_keys",)
    assert "evidence_provenance_keys" in exc.value.mismatched_fields
    assert chain_calls["evaluate"] == 0


def test_d1_missing_composed_identity_key_is_refused(
        source, qauth, registry, chain_calls):
    """Exactly the C1 identity field HQ267 proved could be skipped."""
    identity = _expected_identity(source, qauth, registry)
    for cell in ALLOWED_CELLS:
        del identity[cell]["composed_result_identity_hash"]
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        _build_with_identity(source, qauth, registry, identity)
    assert exc.value.missing_keys == ("composed_result_identity_hash",)
    assert chain_calls["evaluate"] == 0


def test_d1_partially_populated_q2_identity_is_refused(
        source, qauth, registry, chain_calls):
    """q2 fully populated, q1 nearly so -- refused, and q2's completeness is no excuse."""
    identity = _expected_identity(source, qauth, registry)
    for key in ("evidence_provenance_keys", "evidence_authority_keys", "release_key"):
        del identity["q1"][key]
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        _build_with_identity(source, qauth, registry, identity)
    assert set(exc.value.missing_keys) == {
        "evidence_provenance_keys", "evidence_authority_keys", "release_key"}
    assert chain_calls["applicability"] == 0


def test_d1_extraneous_unknown_identity_key_is_refused(
        source, qauth, registry, chain_calls):
    """Only the exact necessary canonical keys are accepted."""
    identity = _expected_identity(source, qauth, registry)
    identity["q1"]["attacker_supplied_key"] = "whatever"
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        _build_with_identity(source, qauth, registry, identity)
    assert exc.value.mismatched_fields == ("attacker_supplied_key",)
    assert chain_calls["evaluate"] == 0


def test_d1_wrong_builtin_type_is_refused(source, qauth, registry, chain_calls):
    """An int field holding a str, and a str field holding an int, are both refused."""
    for field, bad in (("raw_denominator_support", "2"),
                       ("composed_result_identity_hash", 123),
                       ("evidence_provenance_keys", "not-a-tuple"),
                       ("evidence_state", True)):
        identity = _expected_identity(source, qauth, registry)
        for cell in ALLOWED_CELLS:
            identity[cell][field] = bad
        with pytest.raises(SelectedIngressAuthenticationError) as exc:
            _build_with_identity(source, qauth, registry, identity)
        assert exc.value.mismatched_fields == (field,), (field, exc.value.mismatched_fields)
    assert chain_calls["evaluate"] == 0


def test_d1_complete_identity_positive_control_runs_the_whole_chain(
        source, qauth, registry, chain_calls):
    """The exact counterexample's control: a COMPLETE expectation is accepted and the
    real C1 -> G2 -> bound-F8 chain runs exactly once each."""
    ingress = _build_with_identity(
        source, qauth, registry, _expected_identity(source, qauth, registry))
    r = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert r is not None
    # compose also runs while the honest expectation is built (twice, once per cell)
    # and the binder is invoked explicitly, from inside evaluate and from
    # assert_query_source_admitted -- so assert presence, not an exact call count.
    assert chain_calls["compose"] >= 1
    assert chain_calls["binder"] >= 1
    assert chain_calls["applicability"] == 1
    assert chain_calls["evaluate"] == 1


def test_d1_fails_closed_inside_authenticate_before_applicability_and_f8(
        source, qauth, registry, chain_calls, f8_calls):
    """Belt and braces: even a POST-construction replacement of the live expectation
    is caught inside `_authenticate`, before applicability and at zero F8."""
    ingress = _build_with_identity(
        source, qauth, registry, _expected_identity(source, qauth, registry))
    ingress._owner_identity = {"q1": {}, "q2": {}}
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert "INCOMPLETE" in str(exc.value)
    assert set(exc.value.missing_keys) == set(REQUIRED_IDENTITY_KEYS)
    assert exc.value.f8_invoked is False
    # compose must already have run (twice building the honest expectation, once for
    # this serve) so the material being authenticated exists...
    assert chain_calls["compose"] >= 1
    # ...but nothing downstream of the completeness gate may run
    assert chain_calls["applicability"] == 0
    assert chain_calls["binder"] == 0
    assert chain_calls["evaluate"] == 0
    assert f8_calls["n"] == 0


def test_d1_authenticate_has_no_membership_hole(source, qauth, registry):
    """The conditional-membership guard is gone; completeness is re-checked first and
    every required field is compared, with the observed builder pinned to the same
    closed set so neither side can drift."""
    import inspect
    text = inspect.getsource(OwnerOnlySelectedIngress._authenticate)
    assert "if k in expected" not in text
    assert "_require_complete_identity(expected, req.cell)" in text
    assert "for k in REQUIRED_IDENTITY_KEYS" in text
    assert "REQUIRED_IDENTITY_KEYS - set(observed)" in text
    # and the construction-time gate is wired too
    assert "_require_complete_identity(owner_identity[cell], cell)" in _identity_source_text()


def test_d1_authenticate_refuses_a_mismatched_complete_expectation(
        source, qauth, registry, f8_calls):
    """Completeness is not sufficient on its own -- a complete but DIFFERENT
    expectation is still caught, before any F8."""
    identity = _expected_identity(source, qauth, registry)
    identity["q1"]["release_key_owner"] = "REL-forged"
    ingress = _build_with_identity(source, qauth, registry, identity)
    with pytest.raises(SelectedIngressAuthenticationError) as exc:
        ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert exc.value.mismatched_fields == ("release_key_owner",)
    assert exc.value.missing_keys == ()
    assert exc.value.f8_invoked is False
    assert f8_calls["n"] == 0


# ------------------------------------------------------------------ D2


def test_d2_g2_receipt_hash_equals_the_accepted_owner_replay_identity(
        source, ingress):
    """Parity: the technical field IS the accepted owner's primitive, exactly."""
    r = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    accepted = _real_receipt(source)
    assert r.g2_receipt_hash == accepted.replay_identity()
    assert r.g2_receipt_hash == SA.semantic_hash(accepted._material())
    assert len(r.g2_receipt_hash) == 64


def test_d2_replay_identity_discriminates_receipt_id_and_request_key(source):
    """Isolated record-construction discrimination (never operative G0b authority).

    receipt_id and request_key were absent from the pre-D2 six-field subset, so two
    receipts differing only in those produced an IDENTICAL g2_receipt_hash. They must
    now discriminate.
    """
    base = _real_receipt(source)
    base_hash = base.replay_identity()
    for field, other in (("receipt_id", "0" * 64),
                         ("request_key", dict(base.request_key, extra="x")),
                         ("service_id", "SOME_OTHER_SERVICE")):
        changed = dataclasses.replace(base, **{field: other})
        assert changed.replay_identity() != base_hash, field
        assert changed._material()[field] != base._material()[field], field


def test_d2_replay_identity_discriminates_no_applicable_source_and_binding(source):
    """Isolated record-construction discrimination for the remaining omitted fields."""
    base = _real_receipt(source)
    base_hash = base.replay_identity()

    # coverage is COMPLETE here, so no_applicable_source may lawfully flip -- and
    # flipping it must move the replay identity.
    assert base.no_applicable_source is False
    flipped = dataclasses.replace(base, no_applicable_source=True)
    assert flipped.replay_identity() != base_hash

    binding = dict(base.candidate_class_binding)
    binding["declared_population_scope_ref"] = dict(
        binding["declared_population_scope_ref"], object_id="urn:hq268:other-pop")
    rebound = dataclasses.replace(base, candidate_class_binding=binding)
    assert rebound.replay_identity() != base_hash


def test_d2_authorised_authority_is_carried_by_the_replay_identity(source):
    """authorised_authority cannot be varied (the accepted owner validates the exact
    ratified label), so prove it is present in -- and discriminates -- the material."""
    base = _real_receipt(source)
    assert base.authorised_authority == SA.AUTHORISED_AUTHORITY
    assert "authorised_authority" in base._material()
    material = dict(base._material())
    material["authorised_authority"] = "SOME_OTHER_RATIFIED_LABEL"
    assert SA.semantic_hash(material) != base.replay_identity()


def test_d2_origin_receipt_hash_binds_the_g2_replay_identity():
    """origin_receipt_hash must transitively include the G2 replay identity, and must
    also carry canonical_replay_only_order -- the ONE receipt field the accepted
    owner's own _material() omits, so it cannot be bound via replay_identity alone."""
    text = _identity_source_text()
    assert "g2_receipt_hash = receipt.replay_identity()" in text
    assert '"g2_receipt_hash": g2_receipt_hash' in text
    assert '"g2_canonical_replay_only_order"' in text


def test_d2_no_local_six_field_subset_hash_remains():
    """The hand-rolled six-field dict is gone from the ingress source."""
    text = _identity_source_text()
    assert '"coverage": receipt.candidate_class_coverage' not in text
    assert "g2_receipt_hash = semantic_hash({" not in text
    # nothing else in this module re-derives a receipt hash locally
    assert text.count("receipt.replay_identity()") == 1


def test_d2_receipt_identity_varies_with_the_applicability_construction(
        source, qauth, registry):
    """End to end: two ingresses whose applicability material differs produce
    different origin receipt hashes, so the origin layer is sensitive to the G2
    receipt it carries."""
    a = build_ingress(source, qauth, registry)
    b = build_ingress(
        source, qauth, registry,
        applicability=dataclasses.replace(
            _applicability(), binding_request_id="hq268-breq-B"))
    req = SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM)
    ra, rb = a.serve(req), b.serve(req)
    assert ra.g2_receipt_hash == rb.g2_receipt_hash  # same receipt material
    assert ra.origin_receipt_hash != rb.origin_receipt_hash  # origin carries the binding
    assert ra.g2_binding_request_id != rb.g2_binding_request_id


# ------------------------------------------------------------------ R2


def test_r2_live_source_and_cells_containers_are_read_only(
        source, qauth, registry):
    """The live trusted containers are read-only mappings, not plain dicts."""
    ingress = build_ingress(source, qauth, registry)
    assert not isinstance(ingress._source, dict)
    assert not isinstance(ingress._cells, dict)
    # MappingProxyType exposes no mutating methods at all, and item assignment /
    # deletion is refused outright.
    with pytest.raises(TypeError):
        ingress._source["release_ref"] = "x"
    with pytest.raises(TypeError):
        ingress._cells["q1"] = None
    with pytest.raises(TypeError):
        del ingress._source["universe"]
    with pytest.raises(TypeError):
        del ingress._cells["q1"]
    # bounded residual, named rather than papered over: the freeze is SHALLOW. The
    # nested objects are still the owner's own shared objects, because converting
    # them would change the semantic refs the accepted C1/G2 owners consume.
    assert ingress._source["universe"] is source["universe"]
    assert ingress._source["release_ref"] is source["release_ref"]
    # and the owner-held expectation remains deeply frozen, as before
    with pytest.raises(TypeError):
        ingress._owner_identity["q1"]["release_key"] = "x"


def test_r2_external_source_dict_mutation_does_not_reach_the_ingress(
        source, qauth, registry):
    """A caller cannot mutate the ingress's view by mutating the dict it passed in."""
    detached = dict(source)
    ingress = build_ingress(source=detached, qauth=qauth, registry=registry)
    honest_release = ingress._source["release_ref"].object_id
    detached["release_ref"] = ExactRef(
        kind=source["release_ref"].kind, object_id="REL-hq268-forged",
        content_hash="0" * 64)
    r = ingress.serve(SelectedRequest(cell="q1", stratum_ids=Q1_STRATUM))
    assert r.release_key == honest_release == source["release_ref"].object_id
    assert r.release_key != "REL-hq268-forged"
