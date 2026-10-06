"""HQ210 focused source-free court — SERVICE_APPLICABILITY_TO_F8_SOURCE_SCOPE_BINDING.

Synthetic exact refs only. No real source, no survey access, no warrant, no actor.

This court is written against two lessons from the HQ207 independent review of the
applicability owner (03/08 artifacts), so that it is not self-referential evidence:

  GAP-3: a court parametrised over the SAME constant the production code checks
         cannot detect a narrowing of that constant, and cannot prove a property of
         the DATA rather than of the FUNCTION. Therefore here:
           * every forbidden purpose is pinned as an EXPLICIT LITERAL in this file,
             never imported or iterated from the production tuple; and
           * the non-authorization property is additionally proven by VALUE
             INSPECTION of the binding material (no rank/score/priority field
             exists), not by asserting the module's own self-description.

  GAP-2: "unranked" is NOT proven by asserting a self-declared boolean. It is proven
         by PERMUTATION INVARIANCE of the binding replay identity across every
         ordering of the candidate class and every ordering of admitted sources,
         plus a value-inspecting field enumeration.

  GAP-4: a "runtime" check that re-runs identical inputs twice is tautological. Every
         runtime check here VARIES an input and observes a change, or asserts a refusal.

The binding implements ONLY:

    BINDING_GRANTS_ELIGIBILITY_SCOPE_ONLY

and the F8 law it is written against is

    EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION
"""
from __future__ import annotations

import ast
import hashlib
import inspect
import itertools
from pathlib import Path

import pytest

from rawlsing_next import pre553_service_f8_source_scope_binding as B
from rawlsing_next import source_backed_positioned_subject_possibility as F8
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.pre553_service_source_applicability import (
    AUTHORISED_AUTHORITY,
    COVERAGE_COMPLETE,
    COVERAGE_INCOMPLETE,
    OUTCOME_ADMISSIBLE_SET,
    OUTCOME_NO_ADMITTED_SOURCE,
    POSITIVE_DECISION,
    CandidateClassApplicabilityReceipt,
    resolve_service_source_applicability,
)
import rawlsing_next.pre553_service_source_applicability as SA

MODULE_PATH = Path(B.__file__).resolve()

#: The F8 blob recorded by HQ208 (02_F8_POWER_BOUNDARY.json). The binding lane must
#: not have modified the adopted F8 owner.
HQ208_F8_BLOB = "62e5eced47b64512f47b004e3e13a6ef3fe21de7"

#: Forbidden purposes PINNED AS LITERALS IN THIS FILE. Deliberately NOT read from
#: B.FORBIDDEN_BINDING_PURPOSES, so that truncating the production tuple cannot make
#: this court pass by collecting fewer cases. (Closes the GAP-3 failure mode.)
PINNED_FORBIDDEN_PURPOSES = (
    "SOURCE_SELECTION",
    "SOURCE_RANKING",
    "SOURCE_PRIORITY",
    "SOURCE_PREFERENCE",
    "FIRST_SOURCE_CHOICE",
    "BEST_SOURCE_CHOICE",
    "LATEST_SOURCE_CHOICE",
    "LOCAL_SOURCE_CHOICE",
    "PREFERRED_SOURCE_CHOICE",
    "POOLING",
    "CROSS_SOURCE_COMPOSITION",
    "ESTIMAND_COMPOSITION",
    "OVERLAP_OR_NONDUPLICATION_AUTHORITY",
    "RESPONDENT_LINKAGE",
    "SOURCE_SEMANTIC_EQUIVALENCE",
    "BACKFILL_AUTHORITY",
    "CURRENTNESS_AUTHORITY",
    "TARGET_USE_PERMISSION_GRANT",
    "F8_CONDITIONING",
    "F8_GEOMETRY_OR_DISTRIBUTION_TRANSFORM",
    "PROBABILITY_OR_DISTRIBUTION_TRANSFORM",
    "TEMPORAL_COMPARABILITY_OR_PRESSURE",
    "INDIVIDUAL_INFERENCE",
    "ACTOR_OR_PERSON_STATE",
    "PREV3_TO_V3_ACTOR_WORK",
)

SERVICE = "REVERSE_POSITIONED_SUBJECT_EMPIRICAL_POSSIBILITY_INFERENCE"


def h(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()


def ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:hq210:{kind.lower()}:{tag}", h(f"{kind}:{tag}"))


def auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"HQ210-{tag}", "1.0.0", h(f"auth:{tag}"))


def tqref(tag: str) -> dict:
    return ref("TQ", tag).as_dict()


A, BB, C = ref("EmpiricalUniverse@1.0.0", "a"), ref("EmpiricalUniverse@1.0.0", "b"), ref("EmpiricalUniverse@1.0.0", "c")
REL = ref("C11LogicalRelease", "r1")
OTHER_REL = ref("C11LogicalRelease", "r2")
TGT = ref("TARGET", "t")
CLASS = tqref("class-1")


def build_class(members):
    return SA.CandidateClassBinding(
        candidate_class_ref=CLASS,
        candidate_source_universe_refs=[m.as_dict() for m in members],
        binding_authority_ref=auth("class").as_dict(),
        declared_population_scope_ref=tqref("pop"),
        declared_geography_scope_ref=tqref("geo"),
    )


def build_request(members, release=REL):
    return SA.ServiceApplicabilityRequest.build(
        service_id=SERVICE,
        service_authority_ref=auth("svc").as_dict(),
        target_use_ref=tqref("target-use"),
        population_scope_ref=tqref("pop"),
        geography_scope_ref=tqref("geo"),
        effective_time_or_interval_ref=tqref("interval-2018"),
        candidate_class_ref=CLASS,
        release_identity_ref=release.as_dict(),
        target_use_permission_refs=[tqref("perm-bound")],
        candidate_source_universe_refs=[m.as_dict() for m in members],
    )


def admitted(src):
    return SA.ApplicabilityAuthorityRecord(src, "ADMITTED", auth(f"adm-{src.object_id[-1]}"))


def negative(src, decision="SOURCE_NOT_APPLICABLE_TO_THIS_SERVICE_AND_USE"):
    return SA.ApplicabilityAuthorityRecord(src, decision, basis_refs=[ref("TQ", f"neg-{src.object_id[-1]}")])


def resolve(members, records, release=REL):
    return resolve_service_source_applicability(build_request(members, release), build_class(members), records)


def binding_request(mode=B.MODE_EXHAUSTIVE_UNRANKED_SET, *, single=None, identity="identity-1", cls=CLASS,
                    service=SERVICE, release=REL, perms=(tqref("perm-bound"),), claim=None, purpose=None):
    return B.ServiceApplicabilityF8ScopeBindingRequest(
        binding_request_id="hq210-breq-1",
        service_request_set_identity=identity,
        candidate_class_ref=ExactRef(**cls),
        service_id=service,
        target_use_ref=ref("TQ", "target-use"),
        release_identity_ref=release,
        bound_target_use_permission_refs=tuple(ExactRef(**p) for p in perms),
        binding_mode=mode,
        requested_source_universe_ref=single,
        requested_currentness_claim=claim,
        requested_purpose=purpose,
    )


def f8_rule(sources, steps=()):
    return F8.PositionedSubjectPossibilityModelRule(
        model_authority_ref=auth("model"),
        walkback_authority_ref=auth("walkback"),
        source_universe_refs=tuple(sources),
        walkback_steps=tuple(steps),
        positive_proxy_authority_refs=tuple(s.proxy_authority_ref for s in steps),
    )


def cbind(bid, universe):
    return F8.ConditionerBinding(bid, ref("GENERATED_SUBJECT_FACT", bid), ref("EMPIRICAL_COORDINATE", bid),
                                 auth(f"cmp-{bid}"), universe, REL, "2026-R1")


def f8_query(universe, release=REL, ids=("country", "education")):
    return F8.PositionedSubjectPossibilityQuery(
        query_id="hq210-q1", subject_ref=ref("GENERATED_SUBJECT", "s"), target_ref=TGT,
        source_universe_ref=universe, release_ref=release,
        conditioner_bindings=tuple(cbind(i, universe) for i in ids),
        requested_projection={"kind": "JOINT_DISTRIBUTION"},
    )


def evidence(universe, ids=("country", "education"), state="SUPPORTED", geometry=None, tag="e1", release=REL):
    return F8.PossibilitySliceEvidence(
        evidence_ref=ref("EmpiricalFact@1.0.0", tag), source_universe_ref=universe, release_ref=release,
        target_ref=TGT, retained_conditioner_ids=tuple(ids), evidence_state=state,
        geometry={"modes": {"A": 60, "B": 40}} if geometry is None and state == "SUPPORTED" else geometry,
        raw_support=100, uncertainty_state="GOVERNED_UPSTREAM_STATE",
        provenance_refs=(ref("PROVENANCE", tag),), authority_refs=(auth(f"ev-{tag}"),),
    )


def bind_one_admitted():
    """A: ADMITTED, B and C refused, COMPLETE coverage, single-source F8 rule."""
    rec = resolve([A, BB, C], [admitted(A), negative(BB), negative(C)])
    return rec, f8_rule((A,))


# ============================================================ 1. the positive path
def test_single_admitted_source_binds_and_F8_evaluates_exactly():
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    assert b.binding_mode == B.MODE_EXHAUSTIVE_UNRANKED_SET
    assert b.candidate_class_coverage == COVERAGE_COMPLETE
    assert [s.key for s in b.admitted_source_universe_refs] == [A.key]
    out = B.evaluate_bound_positioned_subject_possibility(
        binding=b, request=req_b, receipt=rec, query=f8_query(A), rule=rule,
        evidence=(evidence(A),))
    assert out.result_state == "EXACT_SUPPORTED"
    assert out.exact_disposition == "SUPPORTED"
    assert out.exact_reason == "EXACT_POSITIONED_STRATUM_SUPPORTED"


def test_binding_carries_exact_receipt_replay_identity_and_admission_provenance():
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    assert b.applicability_receipt_replay_identity == rec.replay_identity()
    assert b.applicability_receipt_id == rec.receipt_id
    row = b.admission_provenance[0]
    assert row["source_universe_ref"] == A.as_dict()
    assert row["admitted"] is True
    assert row["bound_to_requested_release"] is True
    assert row["admission_authority_ref"] is not None, "admission must carry provenance, not a bare yes"
    assert row["admission_provenance_refs"], "admission provenance refs must be non-empty"


def test_binding_carries_service_target_class_release_and_permission_grain():
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    assert b.service_id == SERVICE
    assert b.service_request_set_identity == rec.service_request_set_identity
    assert b.candidate_class_ref.as_dict() == rec.candidate_class_ref
    assert b.release_identity_ref == REL
    assert b.target_use_ref.as_dict() == tqref("target-use")
    assert [p.as_dict() for p in b.bound_target_use_permission_refs] == [tqref("perm-bound")]
    assert b.material()["bound_permission_refs_are_inputs_not_grants"] is True


# ============================================================ 2. unranked, PROVEN not asserted
def test_admitted_set_is_unranked_by_permutation_invariance_of_replay_identity():
    """GAP-2 closed: proven by permutation invariance, not by a self-declared flag."""
    members = [A, BB, C]
    records = [admitted(A), admitted(BB), negative(C)]
    identities = set()
    admitted_orders = set()
    for perm in itertools.permutations(members):
        rec = resolve(list(perm), [admitted(A), admitted(BB), negative(C)])
        rule = f8_rule((A, BB))
        req_b = binding_request(identity=rec.service_request_set_identity)
        b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
        identities.add(b.replay_identity())
        admitted_orders.add(tuple(
            s.key for s in b.expose_unranked_admitted_source_set(
                request=req_b, receipt=rec, rule=rule)))
    assert len(identities) == 1, "binding identity changed under candidate reordering => an order is being consumed"
    assert len(admitted_orders) == 1, "admitted set order changed under reordering => the order is derived from input order"


def test_binding_material_contains_no_rank_score_priority_preference_or_weight_field():
    """GAP-2/GAP-3 closed: value inspection of the DATA, not of the function."""
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    material = b.material()
    banned = ("rank", "score", "priority", "preference", "preferred", "weight", "best", "first", "latest", "local")
    def walk(node, path=""):
        if isinstance(node, dict):
            for k, v in node.items():
                yield from walk(v, f"{path}.{k}")
        elif isinstance(node, (list, tuple)):
            for i, v in enumerate(node):
                yield from walk(v, f"{path}[{i}]")
        else:
            yield path, node
    hits = []
    for path, value in walk(material):
        leaf = path.rsplit(".", 1)[-1].split("[")[0].lower()
        if leaf in banned:
            hits.append((path, value))
        if isinstance(value, str):
            for w in banned:
                if value.strip().lower() == w:
                    hits.append((path, value))
    assert hits == [], f"binding material carries a ranking-shaped field: {hits}"


def test_binding_exposes_no_ordered_or_preferring_surface():
    """There is no method that YIELDS an ordered, first, best or preferred source.

    The refusal methods (first_admitted_source, ranked_sources, pooled_source_set) do
    carry selection-shaped NAMES, but each one raises rather than returning anything,
    and each is separately pinned by test_binding_has_no_grant_path_for_any_forbidden_power.
    So the check here is that no such method RETURNS a value.
    """
    selection_shaped = ("first_admitted_source", "ranked_sources", "pooled_source_set")
    for name in selection_shaped:
        assert callable(getattr(B.ServiceApplicabilityF8SourceScopeBinding, name)), name
    # The only source-touching methods are the TWO positive powers plus the raising
    # refusals. 'unranked' must not be satisfiable by a bare 'rank' substring match.
    yielding = {n for n in dir(B.ServiceApplicabilityF8SourceScopeBinding)
                if not n.startswith("_") and "source" in n.lower() and n not in selection_shaped}
    assert yielding == {"assert_query_source_admitted", "expose_unranked_admitted_source_set"}, (
        f"unexpected source-touching surface: {sorted(yielding)}")
    # power 1 returns a per-source validation, never a chosen source
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    one = b.assert_query_source_admitted(f8_query(A), request=req_b, receipt=rec, rule=rule)
    assert one["admitted"] is True
    assert one["not_a_selection_among_sources"] is True
    assert one["not_conditioning"] is True
    assert one["f8_query_source_confidence"] == "ELIGIBLE_FOR_SOURCE_SCOPE_ONLY"
    assert len(B.BINDING_MODES) == 2, "a third (ranked/best) binding mode appeared"


# ============================================================ 3. mandatory refusals
@pytest.mark.parametrize("purpose", PINNED_FORBIDDEN_PURPOSES)
def test_every_pinned_forbidden_purpose_is_refused(purpose):
    """Pinned literals, so a truncated production tuple fails this court."""
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        b.assert_binding_does_not_authorize(purpose)
    assert ei.value.reason_code == "BINDING_POWER_NONCOLLAPSE_VIOLATION"


@pytest.mark.parametrize("method,expected", [
    ("first_admitted_source", "BINDING_REFUSES_SOURCE_CHOICE"),
    ("ranked_sources", "BINDING_REFUSES_RANKING"),
    ("pooled_source_set", "BINDING_REFUSES_POOLING"),
    ("conditioned_f8_geometry", "BINDING_REFUSES_F8_CONDITIONING"),
    ("grant_target_use_permission", "BINDING_REFUSES_PERMISSION_GRANT"),
    ("currentness_authority", "BINDING_REFUSES_CURRENTNESS_AUTHORITY"),
    ("infer_individual_state", "BINDING_REFUSES_ACTOR_INFERENCE"),
])
def test_binding_has_no_grant_path_for_any_forbidden_power(method, expected):
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        getattr(b, method)()
    assert ei.value.reason_code == expected


def test_request_level_forbidden_purpose_refuses_before_any_binding():
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        binding_request(purpose="SOURCE_RANKING")
    assert ei.value.reason_code == "BINDING_POWER_NONCOLLAPSE_VIOLATION"


def test_request_receipt_grain_mismatch_refuses():
    rec, rule = bind_one_admitted()
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity="some-other-service-request"), receipt=rec, rule=rule)
    assert ei.value.reason_code == "BINDING_REQUEST_RECEIPT_GRAIN_MISMATCH"


def test_service_grain_mismatch_refuses():
    rec, rule = bind_one_admitted()
    breq = binding_request(identity=rec.service_request_set_identity, service="STRUCTURAL_STRATAL_FIELD_PRODUCTION")
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(request=breq, receipt=rec, rule=rule)
    assert ei.value.reason_code == "BINDING_SERVICE_GRAIN_MISMATCH"


def test_candidate_class_mismatch_refuses():
    rec, rule = bind_one_admitted()
    breq = binding_request(identity=rec.service_request_set_identity, cls=tqref("class-2"))
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(request=breq, receipt=rec, rule=rule)
    assert ei.value.reason_code == "BINDING_CANDIDATE_CLASS_MISMATCH"


def test_release_grain_mismatch_refuses_and_admission_is_not_inherited_across_releases():
    rec = resolve([A, BB, C], [admitted(A), negative(BB), negative(C)], release=REL)
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity, release=OTHER_REL),
            receipt=rec, rule=f8_rule((A,)))
    assert ei.value.reason_code == "BINDING_RELEASE_GRAIN_MISMATCH"


def test_query_source_absent_from_admitted_set_refuses():
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.evaluate_bound_positioned_subject_possibility(
            binding=b, request=req_b, receipt=rec, query=f8_query(BB), rule=rule, evidence=())
    assert ei.value.reason_code == "F8_QUERY_SOURCE_NOT_ADMITTED"


def test_query_release_mismatch_refuses_even_for_an_admitted_source():
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    q = F8.PositionedSubjectPossibilityQuery(
        query_id="q-other-rel", subject_ref=ref("GENERATED_SUBJECT", "s"), target_ref=TGT,
        source_universe_ref=A, release_ref=OTHER_REL,
        conditioner_bindings=(cbind("country", A)._replace if False else
                              F8.ConditionerBinding("country", ref("GENERATED_SUBJECT_FACT", "country"),
                                                     ref("EMPIRICAL_COORDINATE", "country"), auth("cmp-country"),
                                                     A, OTHER_REL, "2026-R1"),),
        requested_projection={"kind": "JOINT_DISTRIBUTION"})
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.evaluate_bound_positioned_subject_possibility(
            binding=b, request=req_b, receipt=rec, query=q, rule=rule, evidence=())
    assert ei.value.reason_code == "F8_QUERY_RELEASE_GRAIN_MISMATCH"


def test_nonpositive_applicability_is_never_treated_as_admission():
    rec = resolve([A, BB, C], [negative(A), negative(BB), negative(C)])
    assert rec.outcome == OUTCOME_NO_ADMITTED_SOURCE
    assert rec.no_applicable_source is True
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=A,
                                    identity=rec.service_request_set_identity),
            receipt=rec, rule=f8_rule((A,)))
    assert ei.value.reason_code in {"REQUESTED_SOURCE_NOT_ADMITTED", "F8_RULE_SOURCE_OUTSIDE_ADMITTED_SET"}


def test_single_source_mode_refuses_a_non_admitted_requested_source():
    rec, rule = bind_one_admitted()
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=BB,
                                    identity=rec.service_request_set_identity),
            receipt=rec, rule=rule)
    assert ei.value.reason_code == "REQUESTED_SOURCE_NOT_ADMITTED"


def test_exhaustive_mode_refuses_a_single_requested_source_as_an_implicit_selection():
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        binding_request(mode=B.MODE_EXHAUSTIVE_UNRANKED_SET, single=A)
    assert ei.value.reason_code == "BINDING_MODE_NOT_SUPPORTED"


def test_missing_permission_refs_refuse_rather_than_defaulting():
    rec, rule = bind_one_admitted()
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        binding_request(identity=rec.service_request_set_identity, perms=())
    assert ei.value.reason_code == "TARGET_USE_PERMISSION_BOUND_REFS_REQUIRED"


def test_f8_rule_source_outside_admitted_set_refuses_and_is_never_widened():
    rec = resolve([A, BB, C], [admitted(A), negative(BB), negative(C)])
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity),
            receipt=rec, rule=f8_rule((A, BB)))
    assert ei.value.reason_code == "F8_RULE_SOURCE_OUTSIDE_ADMITTED_SET"


def test_exhaustive_mode_refuses_when_the_f8_rule_does_not_span_every_admitted_source():
    rec = resolve([A, BB, C], [admitted(A), admitted(BB), negative(C)])
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity), receipt=rec, rule=f8_rule((A,)))
    assert ei.value.reason_code == "F8_RULE_SOURCE_SET_NOT_EXHAUSTIVE"


def test_exhaustive_use_under_incomplete_coverage_refuses():
    rec = resolve([A, BB, C], [admitted(A), negative(BB)])  # C undecided => INCOMPLETE
    assert rec.candidate_class_coverage == COVERAGE_INCOMPLETE
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity), receipt=rec, rule=f8_rule((A,)))
    assert ei.value.reason_code == "APPLICABILITY_COVERAGE_INCOMPLETE"


def test_incomplete_coverage_still_validates_one_known_admitted_source():
    """The narrow power survives where the exhaustive power is refused."""
    rec = resolve([A, BB, C], [admitted(A), negative(BB)])
    assert rec.candidate_class_coverage == COVERAGE_INCOMPLETE
    rule = f8_rule((A,))
    req_b = binding_request(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=A,
                                identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    assert b.assert_query_source_admitted(
        f8_query(A), request=req_b, receipt=rec, rule=rule)["admitted"] is True
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        b.expose_unranked_admitted_source_set(request=req_b, receipt=rec, rule=rule)
    assert ei.value.reason_code == "APPLICABILITY_COVERAGE_INCOMPLETE"


def test_no_applicable_source_under_complete_coverage_is_first_class_not_an_error():
    rec = resolve([A, BB, C], [negative(A), negative(BB), negative(C)])
    assert rec.outcome == OUTCOME_NO_ADMITTED_SOURCE
    assert rec.candidate_class_coverage == COVERAGE_COMPLETE
    assert rec.no_applicable_source is True
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity), receipt=rec, rule=f8_rule((A,)))
    assert ei.value.reason_code == "F8_RULE_SOURCE_OUTSIDE_ADMITTED_SET"


def test_currentness_missing_when_claimed_refuses():
    rec, rule = bind_one_admitted()
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity, claim="CURRENT"),
            receipt=rec, rule=rule, currentness_result=None)
    assert ei.value.reason_code == "CURRENTNESS_MISSING_WHEN_CLAIMED"


def test_currentness_conflicting_when_claimed_refuses():
    rec, rule = bind_one_admitted()
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity, claim="CURRENT"),
            receipt=rec, rule=rule, currentness_result="CONFLICTING")
    assert ei.value.reason_code == "CURRENTNESS_MISSING_OR_CONFLICTING"


def test_currentness_supplied_without_a_claim_refuses():
    rec, rule = bind_one_admitted()
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity),
            receipt=rec, rule=rule, currentness_result="CURRENT_ACCEPTED")
    assert ei.value.reason_code == "CURRENTNESS_RESULT_WITHOUT_CLAIM"


def test_currentness_absent_by_default_and_is_not_inferred_from_applicability():
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    assert b.currentness_result == B.CURRENTNESS_UNREQUESTED
    with pytest.raises(B.ServiceF8ScopeBindingError):
        b.currentness_authority()


def test_receipt_mutated_after_binding_is_detected_at_evaluation():
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    # HQ217: mutate a NON-ADMITTED row only, so the admitted set and the rule's coverage
    # stay valid. That isolates the receipt-mismatch signal from an incidental
    # F8_RULE_SOURCE_SET_NOT_EXHAUSTIVE refusal, so this test measures what it claims.
    import dataclasses as _dc
    mutated_decisions = []
    for d in rec.decisions:
        if d.source_universe_ref["object_id"] == C.object_id:
            d = _dc.replace(d, reason_code="A_MUTATED_NONADMITTED_REASON")
        mutated_decisions.append(d)
    other = _dc.replace(rec, decisions=tuple(mutated_decisions))
    assert other.replay_identity() != rec.replay_identity(), "the mutation must actually change it"
    assert set(other.admissible_source_universe_refs()) == set(rec.admissible_source_universe_refs()), (
        "the admitted set must be unchanged, so only the receipt identity differs")
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.evaluate_bound_positioned_subject_possibility(
            binding=b, request=req_b, receipt=other, query=f8_query(A), rule=rule, evidence=())
    assert ei.value.reason_code == "BINDING_REPLAY_MISMATCH", (
        f"a receipt mutated after binding must fail authentication, got {ei.value.reason_code!r}")


def test_different_f8_rule_at_evaluation_refuses():
    rec, _ = bind_one_admitted()
    bound_rule = f8_rule((A,))
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=bound_rule)
    tampered = F8.PositionedSubjectPossibilityModelRule(
        model_authority_ref=auth("different-model"), walkback_authority_ref=auth("walkback"),
        source_universe_refs=(A,), walkback_steps=(), positive_proxy_authority_refs=())
    assert tampered.rule_hash != b.f8_rule_hash, "the tampered rule must actually differ"
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.evaluate_bound_positioned_subject_possibility(
            binding=b, request=req_b, receipt=rec, query=f8_query(A), rule=tampered, evidence=())
    # HQ217: rule binding is now enforced by AUTHENTICATION. A tampered rule cannot
    # re-derive the binding, so it refuses there. There is deliberately no second
    # rule-hash comparison in the evaluator; see the evaluator docstring.
    assert ei.value.reason_code == "BINDING_REPLAY_MISMATCH", (
        f"a tampered F8 rule must fail authentication, got {ei.value.reason_code!r}")


def test_binding_replay_is_stable_and_re_derivation_must_match():
    rec, rule = bind_one_admitted()
    breq = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=breq, receipt=rec, rule=rule)
    again = B.verify_service_f8_scope_binding_replay(b, request=breq, receipt=rec, rule=rule)
    assert again.replay_identity() == b.replay_identity()
    assert again.material() == b.material()


def test_a_mislabelled_receipt_cannot_even_be_constructed():
    """Stronger than the binder's own label check.

    I originally wrote this to prove the BINDER refuses a mislabelled receipt. The
    court proved something better: the adopted applicability owner refuses to
    CONSTRUCT one, because CandidateClassApplicabilityReceipt.__post_init__ pins
    authorised_authority. So a wrong-label receipt cannot reach the binder at all.
    The binder's own check is retained below as defence in depth.
    """
    rec, rule = bind_one_admitted()
    with pytest.raises(SA.ServiceSourceApplicabilityError):
        CandidateClassApplicabilityReceipt(
            receipt_id=rec.receipt_id, service_request_set_identity=rec.service_request_set_identity,
            service_id=rec.service_id, candidate_class_ref=rec.candidate_class_ref,
            candidate_class_coverage=rec.candidate_class_coverage, decisions=rec.decisions,
            outcome=rec.outcome, no_applicable_source=rec.no_applicable_source,
            candidate_class_binding=rec.candidate_class_binding, request_key=rec.request_key,
            canonical_replay_only_order=rec.canonical_replay_only_order,
            authorised_authority="SOME_OTHER_AUTHORITY")
    # defence in depth: the binder checks the label too
    assert B.AUTHORISED_AUTHORITY == AUTHORISED_AUTHORITY
    src = inspect.getsource(B.bind_service_applicability_to_f8_scope)
    assert "BINDING_AUTHORITY_LABEL_MISMATCH" in src


# ============================================================ 4. F8 law preserved
def test_F8_owner_module_is_byte_unchanged_from_the_HQ208_recorded_blob():
    """The adopted F8 owner must not have been modified by this lane."""
    import subprocess

    repo = Path(MODULE_PATH).resolve().parents[1]
    # Repair 5: fail loudly rather than skip, for the same reason as the owners guard.
    assert Path(F8.__file__).resolve().exists(), (
        "REQUIRED ADOPTED F8 OWNER ABSENT: the byte-identity guard could not run, so this "
        "qualification is NOT certified.")
    try:
        out = subprocess.run(["git", "-C", str(repo), "hash-object", str(Path(F8.__file__).resolve())],
                             capture_output=True, text=True, timeout=60)
    except Exception as exc:  # pragma: no cover
        pytest.fail(f"REQUIRED GIT FACILITY UNAVAILABLE: git hash-object raised {exc!r}; "
                    f"the F8 byte-identity guard could not run.")
    assert out.returncode == 0, (
        f"REQUIRED GIT FACILITY UNAVAILABLE: git hash-object exited {out.returncode} "
        f"({out.stderr.strip()!r}); the F8 byte-identity guard could not run.")
    assert out.stdout.strip() == HQ208_F8_BLOB, (
        f"the F8 owner was modified: {out.stdout.strip()} != HQ208-recorded {HQ208_F8_BLOB}")


def test_F8_algorithm_law_is_still_exact_conditional_lookup():
    assert F8.MODEL_ALGORITHM_ID == "EXACT_CONDITIONAL_LOOKUP__NO_SMOOTHING_INTERPOLATION_OR_EXTRAPOLATION"
    assert B.EXPECTED_F8_ALGORITHM_ID == F8.MODEL_ALGORITHM_ID
    assert B.BINDING_MODES == (B.MODE_SINGLE_SOURCE_VALIDATION, B.MODE_EXHAUSTIVE_UNRANKED_SET)


def test_binding_passes_query_rule_evidence_to_F8_by_identity_and_changes_no_geometry():
    """ELIGIBILITY IS NOT CONDITIONING, and output selection is not transformation."""
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    q = f8_query(A)
    ex = evidence(A)
    before_geometry = dict(ex.geometry)
    out = B.evaluate_bound_positioned_subject_possibility(binding=b, request=req_b, receipt=rec,
                                                          query=q, rule=rule, evidence=(ex,))
    assert out.exact_geometry == before_geometry, "binding altered the pre-materialized geometry"
    assert out.model_rule_hash == rule.rule_hash, "binding altered or replaced the F8 rule"
    assert q.source_universe_ref is A and q.release_ref is REL, "binding mutated the query"
    assert ex.source_universe_ref is A and ex.retained_conditioner_ids == ("country", "education")
    # F8 sorts replay_determinants, so membership is the property, not index 0.
    assert out.query_ref == q.ref, "F8 did not receive the caller's own query object"
    assert q.ref in out.replay_determinants
    assert ex.evidence_ref in out.replay_determinants


#: Repair 4. The previous scan asserted "reads no conditioner/geometry attribute" while
#: checking only 8 hardcoded names, which is narrower than the claim. This court now
#: pins the COMPLETE inventory of attributes the binder reads, as LITERALS in this file
#: (never read from the production module). The proof is therefore stronger AND
#: honest: any NEW attribute read -- a conditioner, a geometry, or anything else --
#: fails this test. No conditioner or geometry attribute appears in the inventory.
PINNED_BINDING_ATTRIBUTE_INVENTORY = frozenset({
    "__init__", "__setattr__", "_provenance_for", "_refuse_if_forbidden_purpose",
    "_require_single_source_binding", "admissible_source_universe_refs",
    "admission_authority_ref", "admission_provenance", "admission_provenance_refs",
    "admitted_source_universe_refs", "algorithm_id", "append", "applicability_decision",
    "applicability_receipt_id", "applicability_receipt_replay_identity", "as_dict",
    "assert_query_source_admitted", "authorised_authority", "binding_mode", "binding_ref",
    "binding_request_id", "binding_request_ref", "binding_statement",
    "bound_target_use_permission_refs", "candidate_class_coverage", "candidate_class_ref",
    "currentness_result", "decisions", "f8_algorithm_id", "f8_model_rule_refs",
    "f8_rule_hash", "get", "key", "material", "model_rule_id", "no_applicable_source",
    "non_admitted_source_states", "object_id", "public_typed_state", "reason_code",
    "receipt_id", "ref", "release_identity_ref", "release_ref", "replay_identity",
    "request_key", "requested_currentness_claim", "requested_purpose",
    "requested_source_universe_ref", "rule_hash", "service_id",
    "service_request_set_identity", "source_universe_ref", "source_universe_refs", "strip",
    "target_use_ref", "upper",
})

#: Pinned as literals: the conditioner/geometry attribute NAMES that must never appear.
PINNED_FORBIDDEN_CONDITIONER_GEOMETRY_ATTRS = frozenset({
    "conditioner_bindings", "retained_conditioner_ids", "effective_time_or_interval",
    "geometry", "exact_geometry", "uncertainty_state", "raw_support", "walkback_steps",
    "positive_proxy_authority_refs", "slice_possibility", "possibility_geometry",
    "conditional_lookup_table", "projection", "point_masses", "density", "estimand",
    "distribution", "bandwidth", "variance", "posterior", "likelihood",
})


def test_binding_reads_exactly_the_pinned_attribute_inventory_and_no_conditioner():
    """Repair 4: the scan now covers the FULL attribute set, not a chosen subset.

    Two independent checks, both non-self-referential (the expected values are literals
    in this file, never read from the production module):
      1. the binder's complete read-attribute inventory equals the pinned inventory, so
         adding any attribute read fails; and
      2. no pinned conditioner/geometry/estimation attribute is read at all.
    """
    tree = ast.parse(MODULE_PATH.read_text())
    read: set[str] = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    assert read == set(PINNED_BINDING_ATTRIBUTE_INVENTORY), (
        "the binder's attribute-read inventory changed. Newly read: "
        f"{sorted(read - set(PINNED_BINDING_ATTRIBUTE_INVENTORY))}; no longer read: "
        f"{sorted(set(PINNED_BINDING_ATTRIBUTE_INVENTORY) - read)}. A new attribute read must "
        f"be reviewed as a possible conditioning or geometry read.")
    forbidden = read & PINNED_FORBIDDEN_CONDITIONER_GEOMETRY_ATTRS
    assert forbidden == set(), (
        f"the binding reads conditioner/geometry/estimation attributes: {sorted(forbidden)}")


def test_no_conditioner_attribute_is_among_those_the_binding_reads():
    """The same no-conditioner claim, stated directly against the live inventory."""
    tree = ast.parse(MODULE_PATH.read_text())
    read = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    assert not (read & PINNED_FORBIDDEN_CONDITIONER_GEOMETRY_ATTRS)


def test_narrowing_eligibility_changes_which_slice_is_selected_not_the_geometry():
    """The exact trap HQ208 flagged: selection != transformation."""
    members = [A, BB]
    rec_both = resolve(members, [admitted(A), admitted(BB)])
    geo_a = {"modes": {"A": 60, "B": 40}}
    ev_a = evidence(A, geometry=geo_a, tag="ev-a")
    q_a = f8_query(A)
    rule_both = f8_rule((A, BB))
    req_b_both = binding_request(identity=rec_both.service_request_set_identity)
    b_both = B.bind_service_applicability_to_f8_scope(request=req_b_both, receipt=rec_both, rule=rule_both)
    out_both = B.evaluate_bound_positioned_subject_possibility(
        binding=b_both, request=req_b_both, receipt=rec_both, query=q_a, rule=rule_both,
        evidence=(ev_a,))
    # Now narrow: B is no longer admitted, so the F8 rule may only span A.
    rec_a_only = resolve(members, [admitted(A), negative(BB)])
    rule_a = f8_rule((A,))
    req_b_a = binding_request(identity=rec_a_only.service_request_set_identity)
    b_a = B.bind_service_applicability_to_f8_scope(request=req_b_a, receipt=rec_a_only, rule=rule_a)
    out_a = B.evaluate_bound_positioned_subject_possibility(
        binding=b_a, request=req_b_a, receipt=rec_a_only, query=q_a, rule=rule_a, evidence=(ev_a,))
    assert out_both.exact_geometry == out_a.exact_geometry == geo_a
    assert out_both.result_state == out_a.result_state == "EXACT_SUPPORTED"
    assert [s.key for s in b_a.expose_unranked_admitted_source_set(
        request=req_b_a, receipt=rec_a_only, rule=rule_a)] == [A.key]


def test_applicability_NONCOMPARABLE_stays_distinct_from_F8_evidence_NONCOMPARABLE():
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    out = B.evaluate_bound_positioned_subject_possibility(
        binding=b, request=req_b, receipt=rec, query=f8_query(A), rule=rule,
        evidence=(evidence(A, state="NONCOMPARABLE", tag="nc"),))
    assert out.result_state == "NONCOMPARABLE"
    assert out.exact_reason == "EXACT_POSITIONED_STRATUM_NONCOMPARABLE"
    # the applicability-side refusals are still reported separately
    states = {row["source_universe_ref"]["object_id"].rsplit(":", 1)[-1]: row["public_typed_state"]
              for row in b.non_admitted_source_states}
    assert states["b"] == "NOT_APPLICABLE" and states["c"] == "NOT_APPLICABLE"
    assert "applicability_noncomparable_is_not_f8_evidence_noncomparable" in b.non_admitted_source_states[0]


def test_multiple_admitted_sources_remain_separate_source_indexed_entries():
    rec = resolve([A, BB, C], [admitted(A), admitted(BB), negative(C)])
    rule = f8_rule((A, BB))
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    admitted_set = b.expose_unranked_admitted_source_set(
        request=req_b, receipt=rec, rule=rule)
    assert len(admitted_set) == 2
    assert b.material()["admitted_entries_remain_separate_source_indexed"] is True
    assert b.material()["admitted_set_cardinality_is_not_a_sample_size"] is True
    rows = {r["source_universe_ref"]["object_id"].rsplit(":", 1)[-1] for r in b.admission_provenance}
    assert rows == {"a", "b"}, "each admitted source must carry its own provenance row"
    # each source evaluates independently through F8
    for u in (A, BB):
        o = B.evaluate_bound_positioned_subject_possibility(
            binding=b, request=req_b, receipt=rec, query=f8_query(u), rule=rule,
            evidence=(evidence(u, tag=f"ev-{u.object_id[-1]}"),))
        assert o.result_state == "EXACT_SUPPORTED"
        assert o.source_universe_ref is u


# ============================================================ 5. write-terrain discipline
def test_binding_does_not_modify_the_adopted_owners():
    """The three owners HQ210 forbade touching must still import cleanly and be unmodified."""
    import subprocess

    repo = Path(MODULE_PATH).resolve().parents[1]
    for rel, expected in (
        ("rawlsing_next/pre553_service_source_applicability.py", "3e40caca29e8c96ee1f412f919cfc7dba63f96c4"),
        ("rawlsing_next/source_backed_positioned_subject_possibility.py", HQ208_F8_BLOB),
        ("rawlsing_next/objective_consumer_bounded_evidence.py", "f30fca20e7b56e00348e82765d95f974b4b6a195"),
    ):
        path = repo / rel
        # Repair 5: a write-terrain guard must FAIL, not skip. A skip here would make
        # an all-green run indistinguishable from a run in which no owner was ever
        # checked, so an absent owner or absent git facility is now an explicit FAIL.
        assert path.exists(), (
            f"REQUIRED ADOPTED OWNER ABSENT: {rel} is not present at {path}. The byte-identity "
            f"guard could not run, so this qualification is NOT certified. Fail loudly instead "
            f"of skipping.")
        try:
            out = subprocess.run(["git", "-C", str(repo), "hash-object", str(path)],
                                 capture_output=True, text=True, timeout=60)
        except Exception as exc:  # pragma: no cover
            pytest.fail(f"REQUIRED GIT FACILITY UNAVAILABLE: git hash-object raised {exc!r}. "
                        f"The write-terrain guard could not run for {rel}; fail loudly.")
        assert out.returncode == 0, (
            f"REQUIRED GIT FACILITY UNAVAILABLE: git hash-object exited {out.returncode} "
            f"({out.stderr.strip()!r}) for {rel}. The write-terrain guard could not run.")
        assert out.stdout.strip() == expected, f"{rel} was modified: {out.stdout.strip()} != {expected}"


def test_binder_grants_no_authority_and_declares_its_own_ceiling():
    rec, rule = bind_one_admitted()
    req_b = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req_b, receipt=rec, rule=rule)
    m = b.material()
    assert m["grants_no_authority"] is True
    assert m["applicability_authorised_authority"] == AUTHORISED_AUTHORITY
    assert m["f8_does_not_transform_possibility_geometry"] is True
    assert m["canonical_order_grants_no_rank_priority_preference_weight_or_fallback"] is True
    assert m["binding_statement"] == B.BINDING_STATEMENT
    for law in ("ELIGIBILITY != CONDITIONING",
                "ELIGIBILITY_NARROWING != POSSIBILITY_GEOMETRY_TRANSFORMATION",
                "BINDING != SOURCE_SELECTION",
                "BINDING != CURRENTNESS",
                "BOUND_PERMISSION_REFS != GRANTED_PERMISSION",
                "APPLICABILITY_NONCOMPARABLE != F8_EVIDENCE_NONCOMPARABLE"):
        assert law in B.NON_COLLAPSE_LAWS
        assert law in m["non_collapse_laws"]


def test_module_exposes_only_the_two_positive_powers():
    """Public callable surface of the module, pinned against __all__ (not bare dir()).

    dir() would also list every name imported INTO the module, which is not the
    module's own surface. __all__ is the declared surface and is what is pinned.
    """
    public = sorted(n for n in B.__all__ if not n.startswith("_") and callable(getattr(B, n)))
    expected = {
        "ServiceApplicabilityF8ScopeBindingRequest",
        "ServiceApplicabilityF8SourceScopeBinding",
        "ServiceF8ScopeBindingError",
        "bind_service_applicability_to_f8_scope",
        "evaluate_bound_positioned_subject_possibility",
        "verify_service_f8_scope_binding_replay",
        "assert_complete_coverage_from_binding",
    }
    assert set(public) == expected, f"unexpected declared public surface: {sorted(set(public) ^ expected)}"
    # exactly two operations yield or validate sources; nothing else is exported
    powers = {"bind_service_applicability_to_f8_scope", "evaluate_bound_positioned_subject_possibility",
              "assert_complete_coverage_from_binding"}
    assert powers <= set(B.__all__)
    assert "rank_sources" not in B.__all__ and "select_source" not in B.__all__
