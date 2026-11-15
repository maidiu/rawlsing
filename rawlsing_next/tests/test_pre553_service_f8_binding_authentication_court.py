"""HQ217 hostile court -- H-D/F8 BINDING AUTHENTICATION.

Source-free. Synthetic exact refs only. No real source, no survey access, no warrant,
no actor/person, no live C4, no C7.

WHAT THIS COURT EXISTS FOR
--------------------------
HQ215 found that ``ServiceApplicabilityF8SourceScopeBinding`` is a PUBLIC, directly
constructible, ``dataclasses.replace``-able dataclass, and that the evaluator trusted its
attacker-controlled fields. A forged binding could therefore carry an admitted source that
service applicability had never admitted, and reach adopted F8 with
``state=EXACT_SUPPORTED``.

Every authority-consuming path now authenticates the binding by RE-DERIVING it from the
authoritative request, the authoritative applicability receipt and the exact bound F8
rule, and then uses the RE-DERIVED binding. This court attacks that.

Non-self-reference discipline: every expected name is PINNED AS A LITERAL in this file and
never read from the production module, so truncating the public surface makes this court
FAIL rather than silently pass with a smaller count.

HQD-216 (local grain): this court also REQUIRES that lawful competent input still reaches
the intended positive F8 evaluation. A repair that refused every path would fail here.
"""
from __future__ import annotations

import dataclasses
import hashlib
import inspect
from pathlib import Path

import pytest

from rawlsing_next import pre553_service_f8_source_scope_binding as B
from rawlsing_next import source_backed_positioned_subject_possibility as F8
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, semantic_hash
from rawlsing_next.pre553_service_source_applicability import (
    COVERAGE_COMPLETE,
    POSITIVE_DECISION,
    resolve_service_source_applicability,
)
import rawlsing_next.pre553_service_source_applicability as SA

MODULE_PATH = Path(B.__file__).resolve()

# ---------------------------------------------------------------------------
# PINNED census -- literals, never read from the module under test
# ---------------------------------------------------------------------------

#: Every class exported by __all__, INCLUDING the two dataclasses whose public
#: constructors are the forgery surface HQ217 exists to close.
PINNED_EXPORTED_CLASSES = (
    "ServiceF8ScopeBindingError",
    "ServiceApplicabilityF8ScopeBindingRequest",
    "ServiceApplicabilityF8SourceScopeBinding",
)

#: Every module-level function exported by __all__.
PINNED_EXPORTED_FUNCTIONS = (
    "bind_service_applicability_to_f8_scope",
    "evaluate_bound_positioned_subject_possibility",
    "verify_service_f8_scope_binding_replay",
    "assert_complete_coverage_from_binding",
)

#: EVERY public method on the binding class. The HQ213 census enumerated only the two
#: source-touching powers; the other twelve were filtered out by construction. This is
#: the honest census: two powers, one coverage/misc accessor set, and NINE loud refusals.
PINNED_BINDING_PUBLIC_METHODS = (
    "as_dict",
    "binding_statement",
    "assert_binding_does_not_authorize",
    "assert_query_source_admitted",
    "conditioned_f8_geometry",
    "currentness_authority",
    "expose_unranked_admitted_source_set",
    "first_admitted_source",
    "grant_target_use_permission",
    "infer_individual_state",
    "material",
    "pooled_source_set",
    "ranked_sources",
    "replay_identity",
)

#: The methods that reveal or assert eligibility. All of them require the authoritative
#: request + receipt + rule; none can be called with the binding's own fields alone.
PINNED_ELIGIBILITY_REVEALING_METHODS = (
    "assert_query_source_admitted",
    "expose_unranked_admitted_source_set",
)

#: PINNED ADOPTED OWNER BLOBS -- must stay byte-identical.
PINNED_ADOPTED_OWNER_BLOBS = {
    "rawlsing_next/pre553_service_source_applicability.py": "3e40caca29e8c96ee1f412f919cfc7dba63f96c4",
    "rawlsing_next/source_backed_positioned_subject_possibility.py": "62e5eced47b64512f47b004e3e13a6ef3fe21de7",
    "rawlsing_next/objective_consumer_bounded_evidence.py": "f30fca20e7b56e00348e82765d95f974b4b6a195",
}


# ---------------------------------------------------------------------------
# synthetic refs / fixtures
# ---------------------------------------------------------------------------

def h(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()


def ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:hq217:{kind.lower()}:{tag}", h(f"{kind}:{tag}"))


def authref(tag: str) -> AuthorityRef:
    return AuthorityRef(f"HQ217-{tag}", "1.0.0", h(f"auth:{tag}"))


def tqref(tag: str) -> dict:
    return ref("TQ", tag).as_dict()


A, BB, C = (ref("EmpiricalUniverse@1.0.0", t) for t in ("a", "b", "c"))
REL = ref("C11LogicalRelease", "r1")
TGT = ref("TARGET", "t")
CLASS = tqref("class-1")
SERVICE = "HQ217-SVC"


def breq(mode=B.MODE_EXHAUSTIVE_UNRANKED_SET, *, single=None, identity="identity-1", claim=None):
    return B.ServiceApplicabilityF8ScopeBindingRequest(
        binding_request_id="hq217-breq-1",
        service_request_set_identity=identity,
        candidate_class_ref=ExactRef(**CLASS),
        service_id=SERVICE,
        target_use_ref=ref("TQ", "target-use"),
        release_identity_ref=REL,
        bound_target_use_permission_refs=(ref("TQ", "perm-bound"),),
        binding_mode=mode,
        requested_source_universe_ref=single,
        requested_currentness_claim=claim,
    )


def f8_rule(sources):
    return F8.PositionedSubjectPossibilityModelRule(
        model_authority_ref=authref("model"), walkback_authority_ref=authref("walkback"),
        source_universe_refs=tuple(sources), walkback_steps=(), positive_proxy_authority_refs=(),
    )


def cbind(bid, universe):
    return F8.ConditionerBinding(bid, ref("GENERATED_SUBJECT_FACT", bid),
                                 ref("EMPIRICAL_COORDINATE", bid), authref(f"cmp-{bid}"),
                                 universe, REL, "2026-R1")


def f8_query(universe, ids=("country", "education")):
    return F8.PositionedSubjectPossibilityQuery(
        query_id="hq217-q1", subject_ref=ref("GENERATED_SUBJECT", "s"), target_ref=TGT,
        source_universe_ref=universe, release_ref=REL,
        conditioner_bindings=tuple(cbind(i, universe) for i in ids),
        requested_projection={"kind": "JOINT_DISTRIBUTION"},
    )


def slice_evidence(universe, ids=("country", "education"), tag="e1"):
    return F8.PossibilitySliceEvidence(
        evidence_ref=ref("EmpiricalFact@1.0.0", tag), source_universe_ref=universe,
        release_ref=REL, target_ref=TGT, retained_conditioner_ids=tuple(ids),
        evidence_state="SUPPORTED", geometry={"modes": {"A": 60, "B": 40}},
        raw_support=100, uncertainty_state="GOVERNED_UPSTREAM_STATE",
        provenance_refs=(ref("PROVENANCE", tag),), authority_refs=(authref(f"ev-{tag}"),),
    )


def authoritative_receipt(records):
    """A genuinely authoritative receipt, built by the ADOPTED owner, not by hand."""
    members = [A, BB, C]
    cls = SA.CandidateClassBinding(
        candidate_class_ref=CLASS,
        candidate_source_universe_refs=[m.as_dict() for m in members],
        binding_authority_ref=authref("class").as_dict(),
        declared_population_scope_ref=tqref("pop"),
        declared_geography_scope_ref=tqref("geo"),
    )
    req = SA.ServiceApplicabilityRequest.build(
        service_id=SERVICE, service_authority_ref=authref("svc").as_dict(),
        target_use_ref=tqref("target-use"), population_scope_ref=tqref("pop"),
        geography_scope_ref=tqref("geo"),
        effective_time_or_interval_ref=tqref("interval-2018"),
        candidate_class_ref=CLASS, release_identity_ref=REL.as_dict(),
        target_use_permission_refs=[tqref("perm-bound")],
        candidate_source_universe_refs=[m.as_dict() for m in members],
    )
    return resolve_service_source_applicability(req, cls, records)


def adm(src):
    return SA.ApplicabilityAuthorityRecord(src, "ADMITTED", authref(f"adm-{src.object_id[-1]}"))


def neg(src):
    return SA.ApplicabilityAuthorityRecord(
        src, "SOURCE_NOT_APPLICABLE_TO_THIS_SERVICE_AND_USE",
        basis_refs=[ref("TQ", f"neg-{src.object_id[-1]}")])


def receipt_only_a_admits():
    """B is NOT admitted. This is the fixture every forgery attack runs against."""
    return authoritative_receipt([adm(A), neg(BB), neg(C)])


def receipt_admits_a_and_b():
    return authoritative_receipt([adm(A), adm(BB), neg(C)])


def forge_binding(real_receipt, bound_rule, admitted_src, requested_src, *,
                  binding_ref=None, coverage=COVERAGE_COMPLETE):
    """DIRECT CONSTRUCTION of a binding admitting a source the receipt does not admit.

    Every field the pre-repair evaluator consulted is attacker-controlled here, and the
    receipt id and replay identity are copied verbatim from the genuine receipt.
    """
    return B.ServiceApplicabilityF8SourceScopeBinding(
        binding_ref=binding_ref or ref("TQ", "attacker-binding-ref"),
        binding_request_ref=ref("TQ", "attacker-request-ref"),
        applicability_receipt_id=real_receipt.receipt_id,
        applicability_receipt_replay_identity=real_receipt.replay_identity(),
        service_request_set_identity=real_receipt.service_request_set_identity,
        service_id=real_receipt.service_id,
        target_use_ref=ref("TQ", "target-use"),
        candidate_class_ref=ExactRef(**CLASS),
        candidate_class_coverage=coverage,
        release_identity_ref=REL,
        bound_target_use_permission_refs=(ref("TQ", "perm-bound"),),
        admitted_source_universe_refs=(admitted_src,),
        admission_provenance=({
            "source_universe_ref": admitted_src.as_dict(),
            "release_identity_ref": REL.as_dict(),
            "admitted": True,
            "bound_to_requested_release": True,
            "admission_authority_ref": authref("forged-authority").as_dict(),
            "admission_provenance_refs": [],
            "public_typed_state": "APPLICABLE_TO_THIS_SERVICE_AND_USE",
        },),
        non_admitted_source_states=(),
        f8_model_rule_refs=tuple(bound_rule.source_universe_refs),
        f8_rule_hash=bound_rule.rule_hash,
        f8_algorithm_id=bound_rule.algorithm_id,
        binding_mode=B.MODE_SINGLE_SOURCE_VALIDATION,
        requested_source_universe_ref=requested_src,
        currentness_result=B.CURRENTNESS_UNREQUESTED,
    )


# ===========================================================================
# HQD-216 -- LAWFUL POSITIVE PATHS. Mandatory: the repair must not refuse everything.
# ===========================================================================


def test_lawful_constructor_binding_reaches_the_intended_positive_F8_evaluation():
    """HQD-216: competent applicability must still carry into F8, exactly."""
    rec = receipt_only_a_admits()
    rule = f8_rule((A,))
    req = breq(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    assert b.binding_mode == B.MODE_EXHAUSTIVE_UNRANKED_SET
    assert b.candidate_class_coverage == COVERAGE_COMPLETE

    out = B.evaluate_bound_positioned_subject_possibility(
        binding=b, request=req, receipt=rec, query=f8_query(A), rule=rule,
        evidence=(slice_evidence(A),))
    assert out.result_state == "EXACT_SUPPORTED"
    assert out.exact_disposition == "SUPPORTED"
    assert out.source_universe_ref is A
    # F8 was not transformed by the binding
    assert out.model_rule_hash == rule.rule_hash
    assert out.exact_geometry == {"modes": {"A": 60, "B": 40}}


def test_lawful_single_source_mode_remains_usable():
    rec = receipt_admits_a_and_b()
    rule = f8_rule((A, BB))
    req = breq(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=A,
               identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    out = B.evaluate_bound_positioned_subject_possibility(
        binding=b, request=req, receipt=rec, query=f8_query(A), rule=rule,
        evidence=(slice_evidence(A),))
    assert out.result_state == "EXACT_SUPPORTED"
    assert out.source_universe_ref is A

    got = b.assert_query_source_admitted(
        f8_query(A), request=req, receipt=rec, rule=rule)
    assert got["admitted"] is True
    assert got["admission_re_derived_from_authoritative_receipt"] is True


def test_lawful_exhaustive_mode_remains_usable_and_exposes_its_set():
    rec = receipt_admits_a_and_b()
    rule = f8_rule((A, BB))
    req = breq(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    out = B.evaluate_bound_positioned_subject_possibility(
        binding=b, request=req, receipt=rec, query=f8_query(BB), rule=rule,
        evidence=(slice_evidence(BB),))
    assert out.result_state == "EXACT_SUPPORTED"
    assert out.source_universe_ref is BB

    exposed = b.expose_unranked_admitted_source_set(request=req, receipt=rec, rule=rule)
    assert {s.key for s in exposed} == {A.key, BB.key}


def test_authentication_does_not_transform_F8_geometry_or_identity():
    """The seam stays non-transformative on the authenticated path."""
    rec = receipt_admits_a_and_b()
    rule = f8_rule((A, BB))
    req = breq(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    ev = slice_evidence(A, tag="ev-a")
    before = dict(ev.geometry)
    out = B.evaluate_bound_positioned_subject_possibility(
        binding=b, request=req, receipt=rec, query=f8_query(A), rule=rule, evidence=(ev,))
    assert out.exact_geometry == before, "the binding must not alter pre-materialized geometry"
    assert out.model_rule_hash == rule.rule_hash, "the F8 rule must pass through unchanged"
    assert b.f8_algorithm_id == F8.MODEL_ALGORITHM_ID, (
        "the F8 algorithm identity must be the exact-conditional-lookup law")
    assert out.model_authority_ref == rule.model_authority_ref
    assert out.walkback_authority_ref == rule.walkback_authority_ref
    assert out.replay_determinants == (slice_evidence(A, tag="ev-a").evidence_ref,
                                        f8_query(A).ref), (
        "the binding must not substitute the query or the evidence")


# ===========================================================================
# ATTACK 1 -- direct constructor forgery
# ===========================================================================


def test_direct_constructor_forgery_cannot_reach_F8_with_a_genuine_receipt():
    rec = receipt_only_a_admits()
    assert BB not in set(rec.admissible_source_universe_refs()), "fixture: B must NOT be admitted"
    rule = f8_rule((BB,))
    forged = forge_binding(rec, rule, BB, BB)
    req = breq(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=BB,
               identity=rec.service_request_set_identity)
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.evaluate_bound_positioned_subject_possibility(
            binding=forged, request=req, receipt=rec, query=f8_query(BB), rule=rule,
            evidence=(slice_evidence(BB),))
    assert ei.value.reason_code == "REQUESTED_SOURCE_NOT_ADMITTED", (
        f"got {ei.value.reason_code!r}")


def test_direct_constructor_forgery_cannot_manufacture_an_admission_claim():
    """The forgery must not even produce an eligibility ASSERTION, not merely fail at F8."""
    rec = receipt_only_a_admits()
    rule = f8_rule((BB,))
    forged = forge_binding(rec, rule, BB, BB)
    req = breq(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=BB,
               identity=rec.service_request_set_identity)
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        forged.assert_query_source_admitted(
            f8_query(BB), request=req, receipt=rec, rule=rule)
    assert ei.value.reason_code == "REQUESTED_SOURCE_NOT_ADMITTED"


def test_direct_constructor_forgery_cannot_expose_a_forged_admitted_set():
    rec = receipt_admits_a_and_b()
    rule = f8_rule((A, BB))
    forged = forge_binding(rec, rule, BB, BB)
    req = breq(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=A,
               identity=rec.service_request_set_identity)
    with pytest.raises(B.ServiceF8ScopeBindingError):
        forged.expose_unranked_admitted_source_set(request=req, receipt=rec, rule=rule)


# ===========================================================================
# ATTACK 2 -- dataclasses.replace of a LAWFUL binding
# ===========================================================================


def test_dataclasses_replace_forgery_cannot_reach_F8_with_a_genuine_receipt():
    """A lawful binding, then every eligibility field swapped, must still refuse."""
    rec = receipt_only_a_admits()
    rule = f8_rule((BB,))
    req = breq(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=A,
               identity=rec.service_request_set_identity)
    lawful = B.bind_service_applicability_to_f8_scope(
        request=breq(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=A,
                     identity=rec.service_request_set_identity),
        receipt=rec, rule=f8_rule((A,)))

    forged_provenance = ({
        "source_universe_ref": BB.as_dict(),
        "release_identity_ref": REL.as_dict(),
        "admitted": True,
        "bound_to_requested_release": True,
        "admission_authority_ref": authref("forged-authority").as_dict(),
        "admission_provenance_refs": [],
        "public_typed_state": "APPLICABLE_TO_THIS_SERVICE_AND_USE",
    },)
    replaced = dataclasses.replace(
        lawful,
        admitted_source_universe_refs=(BB,),
        admission_provenance=forged_provenance,
        binding_mode=B.MODE_SINGLE_SOURCE_VALIDATION,
        requested_source_universe_ref=BB,
        f8_model_rule_refs=tuple(rule.source_universe_refs),
        f8_rule_hash=rule.rule_hash,
    )
    assert replaced.admitted_source_universe_refs == (BB,), "the forgery must really claim B"
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.evaluate_bound_positioned_subject_possibility(
            binding=replaced, request=req, receipt=rec, query=f8_query(BB), rule=rule,
            evidence=(slice_evidence(BB),))
    # The refusal happens during RE-DERIVATION, before the binding's own fields are ever
    # consulted: the request names B, the authoritative receipt does not admit B, and the
    # rule spans only A. Any of these codes is a refusal; the point is that none of the
    # forged fields is trusted.
    assert ei.value.reason_code in {
        "BINDING_REPLAY_MISMATCH",
        "BINDING_NOT_AUTHENTICATED_AGAINST_AUTHORITY",
        "REQUESTED_SOURCE_NOT_ADMITTED",
        "REQUESTED_SOURCE_NOT_IN_F8_RULE_SOURCE_SCOPE",
        "F8_RULE_SOURCE_OUTSIDE_ADMITTED_SET",
    }, f"unexpected refusal code {ei.value.reason_code!r}"


def test_replacing_only_binding_ref_or_coverage_also_refuses():
    """Altering binding_ref, coverage or the requested source alone must refuse."""
    rec = receipt_admits_a_and_b()
    rule = f8_rule((A, BB))
    req = breq(identity=rec.service_request_set_identity)
    lawful = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)

    for mutation in (
        {"binding_ref": ref("TQ", "attacker-ref")},
        {"candidate_class_coverage": "INCOMPLETE"},
        {"requested_source_universe_ref": BB},
        {"f8_rule_hash": h("attacker-rule")},
        {"applicability_receipt_replay_identity": h("attacker-replay")},
        {"admission_provenance": ()},
        {"service_id": "ATTACKER-SERVICE"},
    ):
        tampered = dataclasses.replace(lawful, **mutation)
        with pytest.raises(B.ServiceF8ScopeBindingError):
            B.evaluate_bound_positioned_subject_possibility(
                binding=tampered, request=req, receipt=rec, query=f8_query(A), rule=rule,
                evidence=(slice_evidence(A),))


# ===========================================================================
# ATTACK 3 -- copied / rehashed attacker-controlled replay identity
# ===========================================================================


def test_copied_rehashed_attacker_replay_identity_does_not_authenticate_eligibility():
    """A SELF-CONSISTENT, correctly-rehashed forgery still refuses.

    This is the commission's point that a self-hash is not authentication. The attacker
    computes a genuine ``binding_ref`` from a fabricated seed using the module's own
    ``semantic_hash``, so the binding is internally consistent -- and still must refuse,
    because only the ADOPTED receipt can say what is admitted.
    """
    rec = receipt_admits_a_and_b()
    rule = f8_rule((A, BB))
    req = breq(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=C,
               identity=rec.service_request_set_identity)

    attacker_seed = {
        "request": req.material(),
        "receipt_replay_identity": rec.replay_identity(),   # copied, correct
        "receipt_id": rec.receipt_id,                       # copied, correct
        "f8_rule_hash": rule.rule_hash,
        "admitted": [C.as_dict()],                          # FABRICATED eligibility
        "currentness_result": B.CURRENTNESS_UNREQUESTED,
    }
    forged_hash = semantic_hash(attacker_seed)
    self_consistent_ref = ExactRef(
        B.BINDING_FAMILY,
        f"urn:rawlsing:service-f8-scope-binding:sha256:{forged_hash}",
        forged_hash,
    )
    forged = forge_binding(rec, rule, C, C, binding_ref=self_consistent_ref)

    # the forgery really is self-consistent about its own admitted set
    assert forged.admitted_source_universe_refs == (C,)
    assert C not in set(rec.admissible_source_universe_refs()), "fixture: C must NOT be admitted"

    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.evaluate_bound_positioned_subject_possibility(
            binding=forged, request=req, receipt=rec, query=f8_query(C), rule=rule,
            evidence=(slice_evidence(C),))
    assert ei.value.reason_code == "REQUESTED_SOURCE_NOT_ADMITTED", (
        f"a self-consistent forgery must still refuse, got {ei.value.reason_code!r}")


def test_authenticating_against_a_different_receipt_refuses():
    rec = receipt_admits_a_and_b()
    other = receipt_only_a_admits()
    rule = f8_rule((A, BB))
    req = breq(identity=rec.service_request_set_identity)
    lawful = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    with pytest.raises(B.ServiceF8ScopeBindingError):
        B.evaluate_bound_positioned_subject_possibility(
            binding=lawful, request=req, receipt=other, query=f8_query(A), rule=rule,
            evidence=(slice_evidence(A),))


def test_authenticating_with_a_mismatched_request_refuses():
    rec = receipt_admits_a_and_b()
    rule = f8_rule((A, BB))
    req = breq(identity=rec.service_request_set_identity)
    lawful = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    wrong_req = breq(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=BB,
                     identity=rec.service_request_set_identity)
    with pytest.raises(B.ServiceF8ScopeBindingError):
        B.evaluate_bound_positioned_subject_possibility(
            binding=lawful, request=wrong_req, receipt=rec, query=f8_query(A), rule=rule,
            evidence=(slice_evidence(A),))


# ===========================================================================
# The authority inputs are MANDATORY, not optional
# ===========================================================================


def test_the_evaluator_cannot_be_called_without_the_authoritative_request():
    """``receipt`` used to be optional. Now the request is a required keyword."""
    params = inspect.signature(B.evaluate_bound_positioned_subject_possibility).parameters
    assert params["request"].default is inspect.Parameter.empty, (
        "the authoritative request must be REQUIRED, not optional")
    assert params["receipt"].default is inspect.Parameter.empty, (
        "the authoritative receipt must be REQUIRED, not optional")


@pytest.mark.parametrize("method", PINNED_ELIGIBILITY_REVEALING_METHODS)
def test_no_eligibility_revealing_method_can_be_called_without_authority(method):
    """The powers cannot be exercised on a binding's own fields alone."""
    rec = receipt_admits_a_and_b()
    rule = f8_rule((A, BB))
    req = breq(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    fn = getattr(b, method)
    with pytest.raises(TypeError):
        if method == "assert_query_source_admitted":
            fn(f8_query(A))
        else:
            fn()


def test_supplying_the_wrong_types_for_authority_is_refused_not_crashed():
    rec = receipt_admits_a_and_b()
    rule = f8_rule((A, BB))
    req = breq(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    for bad in ({"request": "not-a-request"}, {"receipt": "not-a-receipt"}):
        kwargs = {"request": req, "receipt": rec}
        kwargs.update(bad)
        with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
            B.evaluate_bound_positioned_subject_possibility(
                binding=b, query=f8_query(A), rule=rule, evidence=(slice_evidence(A),),
                **kwargs)
        assert ei.value.reason_code in {"BINDING_AUTHORITY_INPUTS_REQUIRED",
                                        "BINDING_INTEGRITY_FAILURE"}


# ===========================================================================
# The original HQ211/HQ213 defect must remain CLOSED
# ===========================================================================


def test_original_A_bound_B_query_refusal_remains_closed():
    """Repair 1 from HQ213 must not have been reopened by the authentication repair."""
    rec = receipt_admits_a_and_b()
    rule = f8_rule((A, BB))
    req = breq(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=A,
               identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    assert BB in set(b.admitted_source_universe_refs), "B is genuinely admitted here"

    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        b.assert_query_source_admitted(f8_query(BB), request=req, receipt=rec, rule=rule)
    assert ei.value.reason_code == "F8_QUERY_SOURCE_NOT_THE_REQUESTED_SOURCE"


def test_off_release_fail_closed_law_survives():
    """Repair 3 from HQ213 must still hold."""
    rec = receipt_admits_a_and_b()
    forged_off_release = dataclasses.replace(rec, decisions=tuple(
        dataclasses.replace(
            d, release_identity_ref={**d.release_identity_ref,
                                     "object_id": ref("C11LogicalRelease", "r2").object_id})
        if d.applicability_decision == POSITIVE_DECISION else d
        for d in rec.decisions))
    rule = f8_rule((A, BB))
    req = breq(identity=rec.service_request_set_identity)
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=req, receipt=forged_off_release, rule=rule)
    assert ei.value.reason_code == "BINDING_OFF_RELEASE_POSITIVE_DECISION"


def test_complete_incomplete_law_survives():
    """Repair-set law: set exposure requires COMPLETE coverage in every mode."""
    rec = authoritative_receipt([adm(A), neg(BB)])
    assert rec.candidate_class_coverage == "INCOMPLETE"
    rule = f8_rule((A,))
    req = breq(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=A,
               identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    # a single known-admitted source still validates
    assert b.assert_query_source_admitted(
        f8_query(A), request=req, receipt=rec, rule=rule)["admitted"] is True
    # but the set may never be exposed
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        b.expose_unranked_admitted_source_set(request=req, receipt=rec, rule=rule)
    assert ei.value.reason_code == "APPLICABILITY_COVERAGE_INCOMPLETE"


# ===========================================================================
# HONEST PUBLIC-SURFACE CENSUS -- nothing filtered out by construction
# ===========================================================================


def test_exact_exported_surface_is_counted_honestly_with_no_filtering():
    """Every __all__ name is classified. Nothing is excluded by name."""
    exported = set(B.__all__)
    classes = {n for n in exported if inspect.isclass(getattr(B, n))}
    functions = {n for n in exported if inspect.isfunction(getattr(B, n))}
    # everything else in __all__ must be a non-callable constant
    rest = exported - classes - functions
    for n in rest:
        assert not callable(getattr(B, n)), f"{n} is callable but was classified as a constant"

    assert classes == set(PINNED_EXPORTED_CLASSES), (
        "the exported CLASS set changed. The dataclass constructors are the forgery "
        f"surface and must be visible. Now: {sorted(classes)}")
    assert functions == set(PINNED_EXPORTED_FUNCTIONS), (
        f"the exported FUNCTION set changed. Now: {sorted(functions)}")
    # and the dataclasses really are directly constructible, which is why auth is needed
    assert dataclasses.is_dataclass(B.ServiceApplicabilityF8SourceScopeBinding)
    assert dataclasses.is_dataclass(B.ServiceApplicabilityF8ScopeBindingRequest)


def test_every_public_binding_method_is_enumerated_not_filtered():
    """The HQ213 census listed only the two powers. All public methods are listed here."""
    cls = B.ServiceApplicabilityF8SourceScopeBinding
    public = {n for n in dir(cls) if not n.startswith("_")}
    assert public == set(PINNED_BINDING_PUBLIC_METHODS), (
        "the binding's public method set changed. An unexpected public method must be "
        f"reviewed as a possible new power. Now: {sorted(public)}")


def test_the_census_counts_the_two_powers_without_hiding_the_loud_refusals():
    """Honest accounting: 2 eligibility powers, and 9 loud refusal methods."""
    cls = B.ServiceApplicabilityF8SourceScopeBinding
    refusals = {
        "first_admitted_source", "ranked_sources", "grant_target_use_permission",
        "pooled_source_set", "conditioned_f8_geometry", "currentness_authority",
        "infer_individual_state", "assert_binding_does_not_authorize",
    }
    assert refusals <= set(PINNED_BINDING_PUBLIC_METHODS)
    assert set(PINNED_ELIGIBILITY_REVEALING_METHODS) <= set(PINNED_BINDING_PUBLIC_METHODS)
    # each declared refusal really does refuse
    rec = receipt_admits_a_and_b()
    rule = f8_rule((A, BB))
    req = breq(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    for name in sorted(refusals):
        with pytest.raises(B.ServiceF8ScopeBindingError):
            if name == "assert_binding_does_not_authorize":
                # this one takes a purpose argument by design
                getattr(b, name)("SOURCE_SELECTION")
            else:
                getattr(b, name)()


def test_the_module_still_declares_no_third_power_over_sources():
    assert "no THIRD POWER OVER SOURCES" in B.NO_THIRD_POWER_OVER_SOURCES
    assert set(B.TWO_SOURCE_TOUCHING_POWERS) == set(PINNED_ELIGIBILITY_REVEALING_METHODS), (
        "the declared source-touching powers must be exactly the two eligibility methods")


def test_no_test_hooks_in_the_production_module():
    assert "pytest" not in MODULE_PATH.read_text()


# ===========================================================================
# Preservation
# ===========================================================================


def test_all_three_adopted_owners_are_byte_identical():
    import subprocess
    repo = Path(MODULE_PATH).resolve().parents[1]
    for rel, expected in PINNED_ADOPTED_OWNER_BLOBS.items():
        path = repo / rel
        assert path.exists(), (
            f"REQUIRED ADOPTED OWNER ABSENT: {rel} at {path}. The guard could not run, so "
            f"this qualification is NOT certified.")
        out = subprocess.run(["git", "-C", str(repo), "hash-object", str(path)],
                             capture_output=True, text=True, timeout=60)
        assert out.returncode == 0, f"REQUIRED GIT FACILITY UNAVAILABLE for {rel}"
        assert out.stdout.strip() == expected, f"{rel} was modified: {out.stdout.strip()}"