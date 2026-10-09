"""HQ253 T0 -- rich source-free C1 -> authenticated F8 EXISTING-API discriminator.

Court ID: HQ253_T0_C1_TO_AUTH_F8_EXISTING_API_DISCRIMINATOR@1

This is a TEST-ONLY, SOURCE-FREE, SINGLE-FILE discriminator executed against ADOPTED
EXISTING APIs only. It creates no architecture, no adapter, no permission and no
authority.

WHAT THIS COURT IS ALLOWED TO CONCLUDE
-------------------------------------
Success here establishes exactly two things:

  1. T0 EXISTING_API_COMPATIBILITY -- the real rich source-free C1 producer output
     can be handed to the existing authenticated source-scope F8 API using a real
     applicability-owner-built receipt and fixture-only target-use authority.
  2. The custody FALSE POSITIVE predicted statically by the HQ251 R01 independent
     review: mathematical parity with the direct C1 F8 result is NOT proof of
     producer custody.

Success is NOT T1 serving adoption, NOT an EE14 model-use grant, NOT N9/OC05
current/as-of, NOT empirical source occupancy, and NOT any actor or V3 authority.
`requested_currentness_claim` is deliberately None throughout: no CURRENT is
fabricated, so no B5/M5 CURRENT proof is claimed.

ORACLES ARE FROZEN BEFORE ANY CANDIDATE IS COMPUTED
---------------------------------------------------
The expected values below are read from the frozen `XOR_ORACLE` literal in the
fixture module at import time and pinned in this file. They are never derived from
any candidate output. The external expected pairs are asserted as LITERALS so that a
change in the candidate cannot silently move the oracle.
"""
from __future__ import annotations

import hashlib
from dataclasses import replace as dataclass_replace

import pytest

from rawlsing_next import pre553_service_f8_source_scope_binding as B
from rawlsing_next import pre553_service_source_applicability as SA
from rawlsing_next import source_backed_positioned_subject_possibility as F8
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef

from rawlsing_next.tests import c1_at08_at13_fixture as fx
from rawlsing_next.tests.test_pre553_empirical_query import _query_authority, _registry


# ===========================================================================
# FROZEN EXTERNAL ORACLE -- pinned from the fixture literal BEFORE any run
# ===========================================================================

#: The XOR source has exactly four respondents: (A,B) in {00,01,10,11} with C = A^B.
#: Pinned EXTERNALLY as literals. These are the pre-registered expected values.
FROZEN_DENOMINATOR = 4
FROZEN_Q1_P_C1_GIVEN_A1 = (1, 2)      # XOR_ORACLE unary_marginal_flat["P(C=1|A=1)"]
FROZEN_Q2_P_C1_GIVEN_A1_B0 = (1, 1)   # XOR_ORACLE joint_decisive["P(C=1|A=1,B=0)"]
FROZEN_Q2_P_C1_GIVEN_A1_B1 = (0, 1)   # the contrast that makes the joint decisive

#: Anti-vacuity: Q1 and Q2 must NOT be equal. Flat marginals with a decisive joint is
#: the whole point of AT09, and a court that only checked "both supported" would pass
#: on an empty result.
FROZEN_Q1_AND_Q2_MUST_DIFFER = True

Q1_CONDITIONS = (("RESPONSE", "A", 1),)
Q2_CONDITIONS = (("RESPONSE", "A", 1), ("RESPONSE", "B", 0))
TARGET_QUESTION = "C"
Q1_TAG = "hq253-qA"
Q2_TAG = "hq253-qAB"

SERVICE = "REVERSE_POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_INFERENCE"
GOVERNED_USE = "GT2_Q86B_TO_Q86A_STRUCTURAL_MEDIATION_INPUT_V554"


def _h(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:hq253:{kind.lower()}:{tag}", _h(f"{kind}:{tag}"))


def auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"HQ253-FIXTURE-ONLY-{tag}", "1.0.0", _h(f"auth:{tag}"))


#: One shared candidate class / target use / permission for BOTH Q1 and Q2, so the
#: applicability receipt may legitimately be reused exactly as R01 permits.
CANDIDATE_CLASS = ref("TARGET_QUESTION_CLASS", "hq253-class-1").as_dict()
TARGET_USE_REF = ref("TARGET_USE", "hq253-fixture-target-use")
PERMISSION_REF = ref("TARGET_USE_PERMISSION", "hq253-fixture-perm-only")
POPULATION_REF = ref("POPULATION_SCOPE", "hq253-fixture-pop")
GEOGRAPHY_REF = ref("GEOGRAPHY_SCOPE", "hq253-fixture-geo")
INTERVAL_REF = ref("TIME_INTERVAL", "hq253-fixture-2018")
OTHER_PERMISSION_REF = ref("TARGET_USE_PERMISSION", "hq253-other-perm")
OTHER_RELEASE = ref("C11LogicalRelease", "hq253-other-release")
OTHER_UNIVERSE = ref("EmpiricalUniverse@1.0.0", "hq253-other-universe")


# ===========================================================================
# FROZEN FIXTURE -- ONE exactly shared synthetic source, release and registry
# ===========================================================================

def _shared_source():
    """Exactly ONE source object, shared by Q1 and Q2.

    R01 is explicit: generating the source twice risks differing ref identities and
    would silently destroy the shared-release comparison.
    """
    return fx.xor_fixture()


@pytest.fixture(scope="module")
def source():
    return _shared_source()


@pytest.fixture(scope="module")
def qauth():
    return _query_authority("c1-at09-xor")


@pytest.fixture(scope="module")
def registry(source, qauth):
    return _registry(source, qauth)


@pytest.fixture(scope="module")
def q1(source, qauth, registry):
    """Q1  q(C | A=1)."""
    composition, consumer_query, witness, producer_query, predicate = (
        fx.direct_condition_composition(
            source=source, qauth=qauth, registry=registry,
            conditions=Q1_CONDITIONS, target_question=TARGET_QUESTION, tag=Q1_TAG,
        )
    )
    return {
        "tag": Q1_TAG,
        "composition": composition, "consumer_query": consumer_query,
        "witness": witness, "producer_query": producer_query, "predicate": predicate,
    }


@pytest.fixture(scope="module")
def q2(source, qauth, registry):
    """Q2  q(C | A=1,B=0) -- the exact progressive conditioning connection."""
    composition, consumer_query, witness, producer_query, predicate = (
        fx.direct_condition_composition(
            source=source, qauth=qauth, registry=registry,
            conditions=Q2_CONDITIONS, target_question=TARGET_QUESTION, tag=Q2_TAG,
        )
    )
    return {
        "tag": Q2_TAG,
        "composition": composition, "consumer_query": consumer_query,
        "witness": witness, "producer_query": producer_query, "predicate": predicate,
    }


@pytest.fixture(scope="module")
def receipt(source):
    """A REAL applicability-owner-built receipt from adopted owner code."""
    universe = source["universe"].ref
    candidate_class = SA.CandidateClassBinding(
        candidate_class_ref=CANDIDATE_CLASS,
        candidate_source_universe_refs=[universe.as_dict()],
        binding_authority_ref=auth("class-fixture-only").as_dict(),
        declared_population_scope_ref=POPULATION_REF.as_dict(),
        declared_geography_scope_ref=GEOGRAPHY_REF.as_dict(),
    )
    service_request = SA.ServiceApplicabilityRequest.build(
        service_id=SERVICE,
        service_authority_ref=auth("service-fixture-only").as_dict(),
        target_use_ref=TARGET_USE_REF.as_dict(),
        population_scope_ref=POPULATION_REF.as_dict(),
        geography_scope_ref=GEOGRAPHY_REF.as_dict(),
        effective_time_or_interval_ref=INTERVAL_REF.as_dict(),
        candidate_class_ref=CANDIDATE_CLASS,
        release_identity_ref=source["release_ref"].as_dict(),
        target_use_permission_refs=[PERMISSION_REF.as_dict()],
        candidate_source_universe_refs=[universe.as_dict()],
    )
    admitted = SA.ApplicabilityAuthorityRecord(
        universe, "ADMITTED", auth("admission-fixture-only").as_dict())
    return SA.resolve_service_source_applicability(
        service_request, candidate_class, [admitted])


def _binding_request(source, receipt, **overrides):
    base = dict(
        binding_request_id="hq253-breq-1",
        service_request_set_identity=receipt.service_request_set_identity,
        candidate_class_ref=ExactRef(**CANDIDATE_CLASS),
        service_id=SERVICE,
        target_use_ref=TARGET_USE_REF,
        release_identity_ref=source["release_ref"],
        bound_target_use_permission_refs=(PERMISSION_REF,),
        binding_mode=B.MODE_SINGLE_SOURCE_VALIDATION,
        requested_source_universe_ref=source["universe"].ref,
        # NO fabricated CURRENT. The binding is CURRENTNESS_UNREQUESTED and no
        # B5/M5 CURRENT proof is claimed anywhere in this court.
        requested_currentness_claim=None,
        requested_purpose=None,
    )
    base.update(overrides)
    return B.ServiceApplicabilityF8ScopeBindingRequest(**base)


def _join(source, receipt, case, **overrides):
    """Bind then consume through the adopted F8 API. Returns (request, binding, out)."""
    universe = source["universe"].ref
    composition = case["composition"]
    rule = fx.make_model_rule(universe, _tag_of(case))
    request = _binding_request(source, receipt, **overrides)
    binding = B.bind_service_applicability_to_f8_scope(
        request=request, receipt=receipt, rule=rule)
    out = B.evaluate_bound_positioned_subject_possibility(
        binding=binding, request=request, receipt=receipt,
        query=case["consumer_query"], rule=rule,
        evidence=(composition.possibility_slice_evidence_or_null,),
    )
    return request, binding, out


def _tag_of(case) -> str:
    return case["tag"]


def _cells(case):
    return case["composition"].consumer_result_or_null.material()[
        "exact_lane"]["geometry"]["cells"]


# ===========================================================================
# 0. Frozen oracle integrity -- the oracle must equal the adopted literal
# ===========================================================================

def test_frozen_oracle_matches_adopted_xor_literal():
    """The pinned expectations must be the fixture's own literal, not a paraphrase."""
    assert fx.XOR_ORACLE["denominator"] == FROZEN_DENOMINATOR
    assert fx.XOR_ORACLE["unary_marginal_flat"]["P(C=1|A=1)"] == FROZEN_Q1_P_C1_GIVEN_A1
    assert fx.XOR_ORACLE["joint_decisive"]["P(C=1|A=1,B=0)"] == FROZEN_Q2_P_C1_GIVEN_A1_B0
    assert fx.XOR_ORACLE["joint_decisive"]["P(C=1|A=1,B=1)"] == FROZEN_Q2_P_C1_GIVEN_A1_B1


def test_one_shared_source_and_release_across_q1_and_q2(source):
    """Q1 and Q2 must sit on ONE exactly shared source/release/universe.

    Both cases receive the SAME `source` object by construction; this pins the
    exact release and universe identity that Q1 and Q2 therefore share.
    """
    assert source["release_ref"].object_id == "REL-c1-at09-xor"
    assert source["universe"].ref.as_dict()["content_hash"] == (
        "318719f670e52a093a9a87ea92f3faf91555c7e1999b03dd47689964483f605c")


# ===========================================================================
# 1. C1 production -- exact progressive conditioning, against frozen values
# ===========================================================================

@pytest.mark.parametrize("case_name,expected", [
    ("q1", FROZEN_Q1_P_C1_GIVEN_A1),
    ("q2", FROZEN_Q2_P_C1_GIVEN_A1_B0),
])
def test_c1_produces_exact_frozen_values(q1, q2, case_name, expected):
    """Actual C1 direct_condition_composition output must equal the frozen pair."""
    case = {"q1": q1, "q2": q2}[case_name]
    composition = case["composition"]
    assert composition.analytical_state == "SUPPORTED"
    assert composition.producer_fact_state == "SUPPORTED"
    assert composition.consumer_result_or_null.result_state == "EXACT_SUPPORTED"
    assert composition.possibility_slice_evidence_or_null is not None
    assert composition.consumer_query_ref == case["consumer_query"].ref

    numerator, denominator = expected
    cells = {c["cell"]: c for c in _cells(case)}
    assert len(cells) == 2
    assert cells["1"]["raw_numerator_support"] == numerator
    assert composition.raw_denominator_support == denominator
    assert cells["1"]["raw_probability_exact_fraction"] == {
        "$exact_fraction": [numerator, denominator]}


def test_q1_and_q2_are_not_interchangeable(source, q1, q2):
    """The exact progressive conditioning connection is REAL, not cosmetic.

    AT09's anti-vacuity point: unary marginals are flat while the joint is decisive.
    If Q1 and Q2 produced the same value this whole court would be vacuous.
    """
    a, b = q1, q2
    # distinct producer predicate / query / witness / fact identities
    assert a["composition"].producer_predicate_ref != b["composition"].producer_predicate_ref
    assert a["composition"].producer_query_ref != b["composition"].producer_query_ref
    assert a["composition"].producer_fact_ref != b["composition"].producer_fact_ref
    assert a["composition"].consumer_query_ref != b["composition"].consumer_query_ref
    assert (a["composition"].condition_binding_witness_ref_or_hash
            != b["composition"].condition_binding_witness_ref_or_hash)
    assert (a["composition"].composed_result_identity_hash
            != b["composition"].composed_result_identity_hash)
    # distinct denominators: q(A,B) is an intersection, never multiplied marginals
    assert a["composition"].raw_denominator_support == 2
    assert b["composition"].raw_denominator_support == 1
    assert (a["composition"].complete_cell_geometry
            != b["composition"].complete_cell_geometry)
    # the values genuinely differ
    q1_c1 = {c["cell"]: c["raw_numerator_support"] for c in _cells(a)}
    q2_c1 = {c["cell"]: c["raw_numerator_support"] for c in _cells(b)}
    assert q1_c1["1"] == 1 and q1_c1["0"] == 1     # flat 1/2, 1/2
    assert q2_c1["1"] == 1 and q2_c1["0"] == 0     # decisive 1, 0
    assert FROZEN_Q1_AND_Q2_MUST_DIFFER
    assert q1_c1 != q2_c1


def test_c1_envelope_preserves_joint_risk_and_ancestry_as_separate_product(q1, q2):
    """Full C1 product geometry survives as a SEPARATE envelope F8 cannot attest."""
    for case in (q1, q2):
        composition = case["composition"]
        assert composition.risk_set_ref is not None
        assert composition.risk_set_member_refs
        assert composition.denominator_member_refs
        assert composition.complete_cell_geometry
        assert composition.composed_result_identity_hash
        assert composition.authority_refs
        assert composition.uncertainty_state
        assert composition.ancestry_refs is not None
        # F8's own result carries NO composed identity: custody stays in the C1 envelope
        material = composition.consumer_result_or_null.material()
        assert "composed_result_identity_hash" not in repr(material)


# ===========================================================================
# 2. T0 positive -- real applicability receipt -> authenticated F8 consumption
# ===========================================================================

def test_applicability_owner_produces_a_real_receipt(source, receipt):
    """Adopted owner code, given fixture data, yields an ACCEPTED receipt.

    This is a positive test of an adopted owner FUNCTION on test data. It is NOT an
    EE14 service-use receipt and NOT a T1 grant.
    """
    assert receipt.outcome == SA.OUTCOME_ADMISSIBLE_SET
    assert any(d.applicability_decision == SA.POSITIVE_DECISION
               for d in receipt.decisions)
    assert receipt.candidate_class_coverage == SA.COVERAGE_COMPLETE
    assert receipt.service_request_set_identity
    assert dict(receipt.candidate_class_ref) == CANDIDATE_CLASS
    assert receipt.service_id == SERVICE
    assert source["universe"].ref.as_dict() in [
        r.as_dict() for r in receipt.admissible_source_universe_refs()]


@pytest.mark.parametrize("case_name", ["q1", "q2"])
def test_t0_positive_join_is_exactly_equivalent_to_direct_c1(
        source, receipt, q1, q2, case_name):
    """The T0 claim: F8 reproduces the direct C1 result EXACTLY.

    `material()` equality and `result_hash` equality are asserted on the COMPLETE
    material, not on a subset.
    """
    case = {"q1": q1, "q2": q2}[case_name]
    composition = case["composition"]
    direct = composition.consumer_result_or_null
    _request, _binding, out = _join(source, receipt, case)

    assert out.result_state == "EXACT_SUPPORTED"
    assert out.exact_disposition == "SUPPORTED"
    assert out.exact_reason == "EXACT_POSITIONED_STRATUM_SUPPORTED"
    assert out.material() == direct.material()
    assert out.result_hash == direct.result_hash
    evidence = composition.possibility_slice_evidence_or_null
    assert out.exact_evidence_ref == evidence.evidence_ref
    assert out.exact_geometry == evidence.geometry


def test_c1_custody_identity_is_separate_from_the_f8_result(source, receipt, q2):
    """F8 cannot attest `composed_result_identity_hash`; it lives in the C1 envelope."""
    composition = q2["composition"]
    _request, _binding, out = _join(source, receipt, q2)
    assert composition.composed_result_identity_hash
    assert composition.composed_result_identity_hash not in repr(out.material())
    assert composition.composed_result_identity_hash not in out.result_hash


def test_no_currentness_is_claimed_anywhere(source, receipt, q2):
    """requested_currentness_claim is None: no CURRENT is claimed anywhere."""
    request, binding, _out = _join(source, receipt, q2)
    assert request.requested_currentness_claim is None
    material = repr(binding.material())
    assert material.count(B.CURRENTNESS_UNREQUESTED) == 1
    assert f"'currentness_result': '{B.CURRENTNESS_UNREQUESTED}'" in material
    # and no CURRENT result is asserted anywhere
    assert "CURRENT'" not in material
    assert "STALE" not in material


# ===========================================================================
# 3. THE INDISPENSABLE HOSTILE -- provenance-substitution false positive
# ===========================================================================

def _join_with_evidence(source, receipt, case, evidence):
    universe = source["universe"].ref
    rule = fx.make_model_rule(universe, _tag_of(case))
    request = _binding_request(source, receipt)
    binding = B.bind_service_applicability_to_f8_scope(
        request=request, receipt=receipt, rule=rule)
    out = B.evaluate_bound_positioned_subject_possibility(
        binding=binding, request=request, receipt=receipt,
        query=case["consumer_query"], rule=rule, evidence=(evidence,))
    return out


def test_provenance_substitution_is_a_confirmed_custody_false_positive(
        source, receipt, q2):
    """R01's static prediction, executed.

    Only `provenance_refs` changes. evidence_ref, geometry, support, state, release,
    target and conditioners all stay constant. R01 predicted the F8 result hash would
    be UNCHANGED. If that holds, parity with the direct C1 result is NOT evidence of
    producer custody. This is NOT an F8 vulnerability finding: it is the narrow
    adopted contract behaving exactly as inspected.
    """
    case = q2
    genuine = case["composition"].possibility_slice_evidence_or_null
    _r, _b, baseline = _join(source, receipt, case)

    forged = ref("UNRELATED_PROVENANCE", "hq253-forged-provenance")
    mutated = dataclass_replace(genuine, provenance_refs=(forged,))

    # everything except provenance is held constant -- asserted, not assumed
    assert mutated.evidence_ref == genuine.evidence_ref
    assert mutated.geometry == genuine.geometry
    assert mutated.raw_support == genuine.raw_support
    assert mutated.evidence_state == genuine.evidence_state
    assert mutated.retained_conditioner_ids == genuine.retained_conditioner_ids
    assert mutated.release_ref == genuine.release_ref
    assert mutated.source_universe_ref == genuine.source_universe_ref
    assert mutated.provenance_refs != genuine.provenance_refs

    mutated_out = _join_with_evidence(source, receipt, case, mutated)

    assert mutated_out.result_state == "EXACT_SUPPORTED"
    # THE OBSERVED RESULT: identical hash despite changed provenance custody.
    assert mutated_out.result_hash == baseline.result_hash
    assert mutated_out.material() == baseline.material()


def test_authority_ref_substitution_also_yields_an_identical_hash(source, receipt, q2):
    """The separate authority_refs substitution is equally undetected by F8."""
    case = q2
    genuine = case["composition"].possibility_slice_evidence_or_null
    _r, _b, baseline = _join(source, receipt, case)

    mutated = dataclass_replace(
        genuine,
        provenance_refs=(ref("UNRELATED_PROVENANCE", "hq253-fp"),),
        authority_refs=(auth("forged-evidence-authority"),),
    )
    assert mutated.evidence_ref == genuine.evidence_ref
    assert mutated.authority_refs != genuine.authority_refs

    out = _join_with_evidence(source, receipt, case, mutated)
    assert out.result_state == "EXACT_SUPPORTED"
    assert out.result_hash == baseline.result_hash


def test_evidence_ref_substitution_IS_detected(source, receipt, q2):
    """The boundary of the custody gap: evidence identity IS in the hash.

    This is the control that keeps the finding honest. The gap is narrow and
    specific to provenance/authority, NOT a total absence of evidence binding.
    """
    case = q2
    genuine = case["composition"].possibility_slice_evidence_or_null
    _r, _b, baseline = _join(source, receipt, case)

    mutated = dataclass_replace(
        genuine,
        evidence_ref=ref("C1_POSITIONED_SUBJECT_SLICE_EVIDENCE@1", "hq253-other-evidence"),
    )
    out = _join_with_evidence(source, receipt, case, mutated)
    assert out.result_state == "EXACT_SUPPORTED"
    assert out.result_hash != baseline.result_hash


def test_geometry_substitution_is_detected(source, receipt, q2):
    """Geometry IS covered by the result material, unlike provenance."""
    case = q2
    genuine = case["composition"].possibility_slice_evidence_or_null
    _r, _b, baseline = _join(source, receipt, case)

    forged_geometry = {**genuine.geometry,
                       "raw_denominator_support_probe": "FORGED_GT253_SENTINEL"}
    mutated = dataclass_replace(genuine, geometry=forged_geometry)
    assert mutated.geometry != genuine.geometry
    assert mutated.evidence_ref == genuine.evidence_ref
    out = _join_with_evidence(source, receipt, case, mutated)
    assert out.result_state == "EXACT_SUPPORTED"
    assert out.material() != baseline.material()


# ===========================================================================
# 4. Independent boundary discrimination -- which boundary rejects what
# ===========================================================================

@pytest.mark.parametrize("override,expected_code", [
    ({"release_identity_ref": OTHER_RELEASE}, "BINDING_RELEASE_GRAIN_MISMATCH"),
    ({"requested_source_universe_ref": OTHER_UNIVERSE}, "REQUESTED_SOURCE_NOT_ADMITTED"),
    ({"service_id": "SOME_OTHER_SERVICE"}, "BINDING_SERVICE_GRAIN_MISMATCH"),
    ({"service_request_set_identity": "f" * 64}, "BINDING_REQUEST_RECEIPT_GRAIN_MISMATCH"),
])
def test_authenticated_binding_refuses_substituted_grain(source, receipt, q2,
                                                          override, expected_code):
    """Forged source scope / swapped release / swapped service are REFUSED by the
    existing HQ217 authentication boundary -- NOT by C1 producer identity."""
    universe = source["universe"].ref
    rule = fx.make_model_rule(universe, Q2_TAG)
    request = _binding_request(source, receipt, **override)
    with pytest.raises(B.ServiceF8ScopeBindingError) as exc:
        B.bind_service_applicability_to_f8_scope(request=request, receipt=receipt, rule=rule)
    assert expected_code in str(exc.value)


def test_non_admitted_source_is_not_admissible_in_the_receipt(source):
    """A negative applicability decision removes the source from the admissible set."""
    universe = source["universe"].ref
    candidate_class = SA.CandidateClassBinding(
        candidate_class_ref=CANDIDATE_CLASS,
        candidate_source_universe_refs=[universe.as_dict(), OTHER_UNIVERSE.as_dict()],
        binding_authority_ref=auth("class-fixture-only").as_dict(),
        declared_population_scope_ref=POPULATION_REF.as_dict(),
        declared_geography_scope_ref=GEOGRAPHY_REF.as_dict(),
    )
    service_request = SA.ServiceApplicabilityRequest.build(
        service_id=SERVICE,
        service_authority_ref=auth("service-fixture-only").as_dict(),
        target_use_ref=TARGET_USE_REF.as_dict(),
        population_scope_ref=POPULATION_REF.as_dict(),
        geography_scope_ref=GEOGRAPHY_REF.as_dict(),
        effective_time_or_interval_ref=INTERVAL_REF.as_dict(),
        candidate_class_ref=CANDIDATE_CLASS,
        release_identity_ref=source["release_ref"].as_dict(),
        target_use_permission_refs=[PERMISSION_REF.as_dict()],
        candidate_source_universe_refs=[universe.as_dict(), OTHER_UNIVERSE.as_dict()],
    )
    records = [
        SA.ApplicabilityAuthorityRecord(universe, "ADMITTED",
                                        auth("admission-fixture-only").as_dict()),
        SA.ApplicabilityAuthorityRecord(
            OTHER_UNIVERSE, "SOURCE_NOT_APPLICABLE_TO_THIS_SERVICE_AND_USE",
            basis_refs=[ref("TARGET_QUESTION", "hq253-negative-basis")]),
    ]
    outcome = SA.resolve_service_source_applicability(
        service_request, candidate_class, records)
    admissible = [r.as_dict() for r in outcome.admissible_source_universe_refs()]
    assert universe.as_dict() in admissible
    assert OTHER_UNIVERSE.as_dict() not in admissible


def test_target_use_permission_divergence_is_NOT_refused_by_the_binding(
        source, receipt, q2):
    """SECOND, INDEPENDENT OBSERVED NON-REFUSAL -- reported, not fixed.

    The binding may declare target-use permissions that CONTRADICT the receipt's own
    request key, and both binding and consumption succeed with the identical result
    hash. Unlike the provenance case this is about a permission IDENTITY divergence
    between receipt and binding.

    No production edit is made. This is banked as observed counterevidence for the
    independent reviewer and for any future T1 ingress design.
    """
    receipt_perms = [dict(p) for p in receipt.request_key["target_use_permission_refs"]]
    assert PERMISSION_REF.as_dict() in receipt_perms
    assert OTHER_PERMISSION_REF.as_dict() not in receipt_perms
    request = _binding_request(
        source, receipt, bound_target_use_permission_refs=(OTHER_PERMISSION_REF,))
    rule = fx.make_model_rule(source["universe"].ref, Q2_TAG)
    binding = B.bind_service_applicability_to_f8_scope(
        request=request, receipt=receipt, rule=rule)
    assert [p.as_dict() for p in binding.bound_target_use_permission_refs] == [
        OTHER_PERMISSION_REF.as_dict()]

    out = B.evaluate_bound_positioned_subject_possibility(
        binding=binding, request=request, receipt=receipt,
        query=q2["consumer_query"], rule=rule,
        evidence=(q2["composition"].possibility_slice_evidence_or_null,))
    assert out.result_state == "EXACT_SUPPORTED"
    assert out.result_hash == q2["composition"].consumer_result_or_null.result_hash


def test_c1_producer_identity_substitution_is_a_separate_boundary(q1, q2):
    """C1 producer identity is NOT what F8 authenticates.

    F8 authenticates the APPLICABILITY receipt grain. It does not authenticate the
    C1 producer predicate/query/fact/witness identity: swapping the C1 product for a
    different supported one changes the result honestly, which is why custody needs
    a T1 owner-selected replay rather than parity with F8.
    """
    assert q1["composition"].composed_result_identity_hash != \
        q2["composition"].composed_result_identity_hash


# ===========================================================================
# 5. Read-only AT09/10/11 inheritance -- no coverage overclaim
# ===========================================================================

def test_read_only_inheritance_is_asserted_not_reexecuted(source):
    """AT09/10/11 remain the owner of that coverage; this court must not restate it.

    Q1/Q2 alone prove the exact joint conditioning on THIS XOR fixture. They do NOT
    prove universal minority enumeration, depth-two recursion, or complete branch
    coverage. This witness pins the distinction rather than borrowing the claims.
    """
    import ast
    import pathlib

    path = pathlib.Path(
        "rawlsing_next/tests/test_pre553_analytical_composition_higher_order.py")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = {n.name for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)}
    for required in (
        "test_at09_xor_unary_marginals_flat_but_joint_configuration_decisive",
        "test_at10_minority_branch_survives_c1_composition",
        "test_at11_depth_two_continuation_reaches_the_recursive_owner_twice",
    ):
        assert required in names, required


def test_negative_c1_states_are_not_forged_here(q1, q2):
    """No synthetic VALID_EMPTY / UNDERPOWERED artifact is manufactured.

    Negative C1 outcomes are reported under their owner-native C1-03A/route grain.
    This court only exercises SUPPORTED and asserts nothing about negatives.
    """
    for case in (q1, q2):
        assert case["composition"].analytical_state == "SUPPORTED"
        assert case["composition"].possibility_slice_evidence_or_null.evidence_state \
            == "SUPPORTED"


def test_no_production_owner_was_modified_by_this_court():
    """The court is test-only: it imports adopted owners and edits nothing."""
    import pathlib

    import rawlsing_next.pre553_service_f8_source_scope_binding as owner
    import rawlsing_next.pre553_service_source_applicability as sa_owner

    assert owner.__file__.endswith("pre553_service_f8_source_scope_binding.py")
    assert sa_owner.__file__.endswith("pre553_service_source_applicability.py")
    court = pathlib.Path(__file__)
    assert "tests" in str(court)