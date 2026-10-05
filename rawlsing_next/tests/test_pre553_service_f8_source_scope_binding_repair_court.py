"""HQ213 bounded-repair hostile court — SERVICE_APPLICABILITY_TO_F8_SOURCE_SCOPE_BINDING.

Source-free. Synthetic exact refs only. No real source, no survey access, no warrant,
no actor/person, no live C4, no C7.

This court exists ONLY to witness the five repairs commissioned by HQ213 against the
HQ211 hostile review of the binder. It is deliberately written to be UNABLE to pass
while the reviewed defects are present:

  Repair 1 (review F1, blocking) — SINGLE_SOURCE_VALIDATION was inert. The binding
    carried no requested source at all, so a binding made for source A evaluated
    source B and returned EXACT_SUPPORTED. Court witness:
    `test_single_source_binding_for_a_REFUSES_evaluation_on_admitted_b` is the exact
    case the review reported as succeeding.
  Repair 2 (review F2, blocking) — "the two positive powers, and only two" was false as
    an API statement: FIVE public callables return. Counted from the exact exported
    surface, not from prose, and not from a noisy dir().
  Repair 3 (review F3) — the `bound_to_requested_release: False` branch was dead and
    fail-open. It is now removed and fail-closed, and the owner invariant it actually
    relied upon is pinned.
  Repair 4 (review F4) — claim/evidence mismatches: docstring counts, the AST scan that
    was narrower than its claim, and an ungoverned caller-defined currentness
    vocabulary.
  Repair 5 (review F5/G-3) — write-terrain guards skipped silently, so an all-green run
    could hide a guard that never ran.

Non-self-reference discipline (carried from the HQ207 review's GAP-2/GAP-3 lessons):
every expectation that a defect could be hidden by is PINNED AS A LITERAL IN THIS FILE
and never read from the production module. In particular the expected public callable
names are literals here, so DELETING a callable from the module's surface fails this
court rather than silently reducing the count.
"""
from __future__ import annotations

import ast
import hashlib
import inspect
import subprocess
from pathlib import Path

import pytest

from rawlsing_next import pre553_service_f8_source_scope_binding as B
from rawlsing_next import source_backed_positioned_subject_possibility as F8
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
import rawlsing_next.pre553_service_source_applicability as SA

MODULE_PATH = Path(B.__file__).resolve()

#: The three adopted owners HQ213 requires to stay byte-identical.
PINNED_ADOPTED_OWNER_BLOBS = {
    "rawlsing_next/pre553_service_source_applicability.py": "3e40caca29e8c96ee1f412f919cfc7dba63f96c4",
    "rawlsing_next/source_backed_positioned_subject_possibility.py":
        "62e5eced47b64512f47b004e3e13a6ef3fe21de7",
    "rawlsing_next/objective_consumer_bounded_evidence.py": "f30fca20e7b56e00348e82765d95f974b4b6a195",
}

#: Repair 2. The exact public CALLABLES, pinned as literals in this court.
#: Two source-touching powers, a constructor, a delegating evaluator, a replay
#: verifier, and a coverage guard. Five of these RETURN a value.
PINNED_TWO_SOURCE_TOUCHING_POWERS = ("assert_query_source_admitted",
                                    "expose_unranked_admitted_source_set")
PINNED_NON_POWER_RETURNING_CALLABLES = ("bind_service_applicability_to_f8_scope",
                                        "evaluate_bound_positioned_subject_possibility",
                                        "verify_service_f8_scope_binding_replay")
PINNED_GUARD_ONLY_CALLABLES = ("assert_complete_coverage_from_binding",)
#: Module-level public callables that are NOT the two binding methods.
#: The exported refusal error TYPE. A type, not a returning callable.
PINNED_EXPORTED_EXCEPTION_TYPE = "ServiceF8ScopeBindingError"
PINNED_MODULE_LEVEL_CALLABLES = frozenset(
    tuple(PINNED_NON_POWER_RETURNING_CALLABLES) + tuple(PINNED_GUARD_ONLY_CALLABLES)
    + (PINNED_EXPORTED_EXCEPTION_TYPE,)
)
#: All public CALLABLES (the exception type is tracked separately).
PINNED_ALL_PUBLIC_CALLABLES = frozenset(
    tuple(PINNED_TWO_SOURCE_TOUCHING_POWERS) + tuple(PINNED_NON_POWER_RETURNING_CALLABLES)
    + tuple(PINNED_GUARD_ONLY_CALLABLES)
)
#: The two powers are METHODS on the binding class, not module-level functions.
PINNED_BINDING_METHODS = frozenset(PINNED_TWO_SOURCE_TOUCHING_POWERS)
#: The count the old receipts under-stated by two.
PINNED_RETURNING_CALLABLE_COUNT = 5

#: Repair 4. The currentness vocabulary is closed and derived from the ADOPTED
#: currentness contract's own states, never from a caller-defined string.
PINNED_ACCEPTED_CURRENTNESS_RESULTS = frozenset({"CURRENT"})
PINNED_REFUSED_ADOPTED_NONCURRENCY_STATES = frozenset(
    {"STALE", "REFRESH_REQUIRED", "INVALID"})
PINNED_LEGACY_NEGATIVE_TOKENS = frozenset({"CONFLICTING", "UNKNOWN", "MISSING", "UNRESOLVED"})

# ---------------------------------------------------------------------------
# synthetic refs / helpers
# ---------------------------------------------------------------------------


def h(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()


def ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:hq213:{kind.lower()}:{tag}", h(f"{kind}:{tag}"))


def auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"HQ213-{tag}", "1.0.0", h(f"auth:{tag}"))


def tqref(tag: str) -> dict:
    return ref("TQ", tag).as_dict()


A, BB, C = (ref("EmpiricalUniverse@1.0.0", t) for t in ("a", "b", "c"))
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
        service_id="HQ213-SVC",
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
    return SA.ApplicabilityAuthorityRecord(
        src, decision, basis_refs=[ref("TQ", f"neg-{src.object_id[-1]}")])


def resolve(members, records, release=REL):
    return SA.resolve_service_source_applicability(
        build_request(members, release), build_class(members), records)


def binding_request(mode=B.MODE_EXHAUSTIVE_UNRANKED_SET, *, single=None, identity="identity-1",
                    release=REL, claim=None):
    return B.ServiceApplicabilityF8ScopeBindingRequest(
        binding_request_id="hq213-breq-1",
        service_request_set_identity=identity,
        candidate_class_ref=ExactRef(**CLASS),
        service_id="HQ213-SVC",
        target_use_ref=ref("TQ", "target-use"),
        release_identity_ref=release,
        bound_target_use_permission_refs=(ref("TQ", "perm-bound"),),
        binding_mode=mode,
        requested_source_universe_ref=single,
        requested_currentness_claim=claim,
    )


def f8_rule(sources):
    return F8.PositionedSubjectPossibilityModelRule(
        model_authority_ref=auth("model"),
        walkback_authority_ref=auth("walkback"),
        source_universe_refs=tuple(sources),
        walkback_steps=(),
        positive_proxy_authority_refs=(),
    )


def f8_query(universe, release=REL, ids=("country", "education")):
    return F8.PositionedSubjectPossibilityQuery(
        query_id="hq213-q1", subject_ref=ref("GENERATED_SUBJECT", "s"), target_ref=TGT,
        source_universe_ref=universe, release_ref=release,
        conditioner_bindings=tuple(cbind(i, universe) for i in ids),
        requested_projection={"kind": "JOINT_DISTRIBUTION"},
    )


def cbind(bid, universe):
    return F8.ConditionerBinding(bid, ref("GENERATED_SUBJECT_FACT", bid),
                                 ref("EMPIRICAL_COORDINATE", bid), auth(f"cmp-{bid}"),
                                 universe, REL, "2026-R1")


def two_admitted_receipt():
    """A and B are BOTH positively admitted under ONE release; the F8 rule spans both.

    This is the review's exact reproduction setup. Under the defect, a
    SINGLE_SOURCE_VALIDATION binding for A evaluated B and returned EXACT_SUPPORTED.
    """
    rec = resolve([A, BB, C], [admitted(A), admitted(BB), negative(C)])
    return rec, f8_rule((A, BB))


def bind_single_for(rec, rule, src, *, with_request=False):
    req = binding_request(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=src,
                          identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    return (b, req) if with_request else b


def bind_exhaustive(rec, rule, *, with_request=False):
    req = binding_request(identity=rec.service_request_set_identity)
    b = B.bind_service_applicability_to_f8_scope(request=req, receipt=rec, rule=rule)
    return (b, req) if with_request else b


def authz(req, rec, rule):
    """The authoritative triple every eligibility-revealing call now requires.

    Named ``authz`` because this court already has an ``auth(tag)`` AuthorityRef helper.
    """
    return {"request": req, "receipt": rec, "rule": rule}


# ===========================================================================
# Repair 1 — the single-source refinement must be semantically BINDING
# ===========================================================================


def test_single_source_binding_for_a_REFUSES_evaluation_on_admitted_b():
    """THE review defect, verbatim. Under the defect this returned EXACT_SUPPORTED.

    Review evidence, now reversed:
        single_mode_requested_source:   a
        single_mode_admitted_set:       [b, a]
        single_mode_evaluation_on_B:    ALLOWED state=EXACT_SUPPORTED   <-- the defect
    """
    rec, rule = two_admitted_receipt()
    b, req = bind_single_for(rec, rule, A, with_request=True)

    # B is genuinely admitted, so nothing about the fixture is refusing by accident.
    assert BB in set(b.admitted_source_universe_refs), "B must be admitted for this witness"
    assert A in set(b.admitted_source_universe_refs), "A must be admitted for this witness"

    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        b.assert_query_source_admitted(f8_query(BB), **authz(req, rec, rule))
    assert ei.value.reason_code == "F8_QUERY_SOURCE_NOT_THE_REQUESTED_SOURCE", (
        f"expected the single-source refinement to refuse B, got {ei.value.reason_code!r}")


def test_single_source_binding_evaluates_the_requested_source_exactly():
    """Positive control: the refinement still admits the source it was made for."""
    rec, rule = two_admitted_receipt()
    b, req = bind_single_for(rec, rule, A, with_request=True)
    got = b.assert_query_source_admitted(f8_query(A), **authz(req, rec, rule))
    assert got["admitted"] is True
    assert got["source_universe_ref"] == A.as_dict()


def test_the_two_modes_are_no_longer_equivalent_on_a_different_admitted_source():
    """Repair 1 is real: the modes must now DIFFER, where the review showed
    `same_result_hash (single vs exhaustive): True`."""
    rec, rule = two_admitted_receipt()
    single, sreq = bind_single_for(rec, rule, A, with_request=True)
    exhaustive, ereq = bind_exhaustive(rec, rule, with_request=True)

    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        single.assert_query_source_admitted(f8_query(BB), **authz(sreq, rec, rule))
    assert ei.value.reason_code == "F8_QUERY_SOURCE_NOT_THE_REQUESTED_SOURCE"

    # the exhaustive binding over the same receipt and rule still validates B, so the
    # refusal above is attributable to the mode, not to the fixture.
    assert exhaustive.assert_query_source_admitted(
        f8_query(BB), **authz(ereq, rec, rule))["admitted"] is True


def test_the_binding_carries_the_requested_source_it_is_enforcing():
    """The root cause was that the binding DISCARDED the requested source."""
    rec, rule = two_admitted_receipt()
    b = bind_single_for(rec, rule, A)
    assert b.requested_source_universe_ref is not None
    assert b.requested_source_universe_ref.key == A.key
    assert b.material()["requested_source_universe_ref"] == A.as_dict(), (
        "the enforced refinement must be part of the binding material and its replay identity")


def test_the_refinement_participates_in_the_replay_identity():
    """A single-source binding for A must not replay-verify as a binding for B.

    This is the enforcement half of Repair 1: the refinement is in the binding
    MATERIAL, so it is in the replay identity, so the replay verifier cannot silently
    re-derive a binding that enforces a different source.
    """
    rec, rule = two_admitted_receipt()
    b = bind_single_for(rec, rule, A)

    # the same request and receipt re-derive the identical binding
    verified = B.verify_service_f8_scope_binding_replay(
        b,
        request=binding_request(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=A,
                                identity=rec.service_request_set_identity),
        receipt=rec, rule=rule)
    assert verified.replay_identity() == b.replay_identity()

    # a request naming B re-derives a DIFFERENT binding, and cannot verify as A
    b_for_b = bind_single_for(rec, rule, BB)
    assert b_for_b.replay_identity() != b.replay_identity(), (
        "single-source bindings for different sources must not share a replay identity")

    with pytest.raises(B.ServiceF8ScopeBindingError):
        B.verify_service_f8_scope_binding_replay(
            b,
            request=binding_request(mode=B.MODE_SINGLE_SOURCE_VALIDATION, single=BB,
                                    identity=rec.service_request_set_identity),
            receipt=rec, rule=rule)


def test_single_source_requested_source_must_be_inside_the_bound_F8_rule_scope():
    """Review F1, second half: a single-source binding could name a source the bound
    F8 rule does not even span."""
    # A and B admitted, but the bound rule spans ONLY B. Requesting A must refuse.
    rec = resolve([A, BB, C], [admitted(A), admitted(BB), negative(C)])
    rule_b_only = f8_rule((BB,))
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        bind_single_for(rec, rule_b_only, A)
    assert ei.value.reason_code == "REQUESTED_SOURCE_NOT_IN_F8_RULE_SOURCE_SCOPE", (
        f"got {ei.value.reason_code!r}")


def test_single_source_may_narrow_to_a_subset_the_exhaustive_mode_would_refuse():
    """Narrowing is lawful: single-source over a rule spanning only A succeeds even
    when the exhaustive mode would demand the rule span every admitted source."""
    rec = resolve([A, BB, C], [admitted(A), admitted(BB), negative(C)])
    rule_a = f8_rule((A,))
    b = bind_single_for(rec, rule_a, A)
    assert b.binding_mode == B.MODE_SINGLE_SOURCE_VALIDATION

    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        bind_exhaustive(rec, rule_a)
    assert ei.value.reason_code == "F8_RULE_SOURCE_SET_NOT_EXHAUSTIVE"


def test_single_source_still_refuses_a_requested_source_that_is_not_admitted():
    rec, rule = two_admitted_receipt()
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        bind_single_for(rec, rule, C)
    assert ei.value.reason_code == "REQUESTED_SOURCE_NOT_ADMITTED"


def test_exhaustive_mode_is_unaffected_by_the_single_source_repair():
    """The repair must not narrow the exhaustive mode."""
    rec, rule = two_admitted_receipt()
    b, req = bind_exhaustive(rec, rule, with_request=True)
    for u in (A, BB):
        assert b.assert_query_source_admitted(
            f8_query(u), **authz(req, rec, rule))["admitted"] is True
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        b.assert_query_source_admitted(f8_query(C), **authz(req, rec, rule))
    assert ei.value.reason_code == "F8_QUERY_SOURCE_NOT_ADMITTED"


# ===========================================================================
# Repair 2 — truthful power accounting
# ===========================================================================


def _exported_module_callables() -> set[str]:
    """Exact exported MODULE-level callable surface, from __all__, not a noisy dir().

    The two source-touching powers are METHODS on the binding class, so they are
    enumerated separately by _exported_binding_methods().
    """
    data_names = {"ServiceApplicabilityF8ScopeBindingRequest",
                  "ServiceApplicabilityF8SourceScopeBinding"}
    out: set[str] = set()
    for name in B.__all__:
        if name in data_names:
            continue
        obj = getattr(B, name)
        if inspect.isfunction(obj) or inspect.isclass(obj):
            out.add(name)
    return out


def _exported_binding_methods() -> set[str]:
    """The two powers, as exported methods on the binding class."""
    cls = B.ServiceApplicabilityF8SourceScopeBinding
    return {n for n in PINNED_BINDING_METHODS
            if callable(getattr(cls, n, None)) and not n.startswith("_")}


def test_public_callable_surface_is_exactly_the_pinned_set():
    """Deletion or addition of a public callable FAILS here, because the expectation is
    pinned as a literal rather than derived from the module."""
    assert _exported_module_callables() == set(PINNED_MODULE_LEVEL_CALLABLES), (
        "the exported module-level callable surface changed; Repair 2 requires the declared "
        f"surface to be counted truthfully. Now: {sorted(_exported_module_callables())}")
    assert _exported_binding_methods() == set(PINNED_BINDING_METHODS), (
        f"the exported binding-method powers changed. Now: {sorted(_exported_binding_methods())}")


def test_the_returning_callable_count_is_five_not_two():
    """The review's F2 core: the old receipts claimed two; five public callables return."""
    returning = set(PINNED_TWO_SOURCE_TOUCHING_POWERS) | set(
        PINNED_NON_POWER_RETURNING_CALLABLES)
    assert len(returning) == PINNED_RETURNING_CALLABLE_COUNT, (
        "five public callables return; the old receipts claimed two")
    assert returning == set(PINNED_ALL_PUBLIC_CALLABLES) - set(PINNED_GUARD_ONLY_CALLABLES)
    # and the old claim of "exactly two" is true ONLY of powers over sources.
    assert len(PINNED_TWO_SOURCE_TOUCHING_POWERS) == 2


def test_the_module_production_constants_agree_with_the_pinned_surface():
    """The production module's own enumeration must match the pinned literals."""
    assert tuple(B.TWO_SOURCE_TOUCHING_POWERS) == PINNED_TWO_SOURCE_TOUCHING_POWERS
    assert tuple(B.NON_POWER_RETURNING_CALLABLES) == PINNED_NON_POWER_RETURNING_CALLABLES
    assert tuple(B.GUARD_ONLY_CALLABLES) == PINNED_GUARD_ONLY_CALLABLES
    assert len(B.TWO_SOURCE_TOUCHING_POWERS) + len(B.NON_POWER_RETURNING_CALLABLES) \
        + len(B.GUARD_ONLY_CALLABLES) == len(PINNED_ALL_PUBLIC_CALLABLES) == 6, (
        "six public callables: two powers, three returning non-powers, one guard")


def test_the_coverage_guard_returns_nothing_and_only_raises():
    """The one callable that is NOT a returning power."""
    rec, rule = two_admitted_receipt()
    b, _req = bind_exhaustive(rec, rule, with_request=True)
    assert B.assert_complete_coverage_from_binding(b) is None


def test_delegating_evaluator_is_declared_a_non_power_with_a_reason():
    """Repair 2 requires the non-power claim to be PRECISE, not merely asserted."""
    reason = B.DELEGATING_EVALUATOR_IS_NOT_A_POWER_BECAUSE
    assert "UNCHANGED" in reason
    for banned in ("selection", "ranking", "transformation", "pooling", "currentness",
                   "permission", "actor"):
        assert banned in reason.lower(), f"the declared reason must address {banned}"
    assert "no third power" in B.NO_THIRD_POWER_OVER_SOURCES.lower()


def test_module_docstring_no_longer_claims_exactly_two_and_says_three_refusals():
    """Repair 4 / F4.1 and F4.2: the docstring counts must match reality."""
    doc = (B.__doc__ or "")
    assert "There is no third." not in doc, "the docstring still makes the F4.2 claim"
    assert "no THIRD POWER OVER SOURCES" in doc
    assert "the three that are attempted-against refuse loudly" not in doc, (
        "the docstring still understates the refusal surface as three")
    assert "SEVEN" in doc


# ===========================================================================
# Repair 3 — the off-release positive branch is removed and fail-closed
# ===========================================================================


def test_adopted_owner_stamps_every_decision_with_the_request_release():
    """Repair 3 requires pinning THE OWNER INVARIANT the safety actually rests on."""
    rec, rule = two_admitted_receipt()
    releases = {d.release_identity_ref.get("object_id") for d in rec.decisions}
    assert releases == {REL.object_id}, (
        "the adopted owner must stamp every decision with the request release; this is the "
        f"invariant that made the off-release branch dead. Saw: {sorted(releases)}")
    assert len({d.release_identity_ref.get("object_id") for d in rec.decisions}) == 1


def test_an_off_release_positive_decision_is_REFUSED_not_admitted():
    """The fail-closed witness. Under the defect this produced a provenance row with
    `bound_to_requested_release: False` and STILL ADMITTED the source."""
    rec, rule = two_admitted_receipt()
    forged = _forge_receipt_with_one_off_release_decision(rec)
    assert forged is not None, "the forge helper must be able to build this fixture"
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=forged.service_request_set_identity),
            receipt=forged, rule=rule)
    assert ei.value.reason_code == "BINDING_OFF_RELEASE_POSITIVE_DECISION", (
        f"an off-release positive decision must fail closed, got {ei.value.reason_code!r}")


def _forge_receipt_with_one_off_release_decision(rec):
    """Rewrite one decision's release onto a different release, bypassing the owner.

    This is deliberately an owner BYPASS: it proves the binder no longer depends on the
    owner's single-release invariant for its own release-grain safety.
    """
    import dataclasses

    decisions = list(rec.decisions)
    mutated = False
    new_decisions = []
    for d in decisions:
        if not mutated and d.applicability_decision == SA.POSITIVE_DECISION:
            rel = dict(d.release_identity_ref)
            rel["object_id"] = OTHER_REL.object_id
            rel["content_digest"] = h(f"forged:{OTHER_REL.object_id}")
            d = dataclasses.replace(d, release_identity_ref=rel)
            mutated = True
        new_decisions.append(d)
    if not mutated:
        return None
    return dataclasses.replace(rec, decisions=tuple(new_decisions))


def test_no_bound_to_requested_release_false_branch_remains():
    """The dead branch is deleted, not merely unreachable."""
    src = MODULE_PATH.read_text()
    assert '"bound_to_requested_release": False' not in src, (
        "the dead off-release provenance branch must be removed")
    assert "bound_to_requested_release" in src, (
        "the truthful all-admitted-rows-are-bound field should remain")


def test_every_admitted_provenance_row_reports_the_requested_release():
    rec, rule = two_admitted_receipt()
    b = bind_exhaustive(rec, rule)
    assert b.admission_provenance, "expected provenance rows"
    for row in b.admission_provenance:
        assert row["bound_to_requested_release"] is True, (
            "every admitted row must be bound to the requested release, because an "
            "off-release positive decision now refuses instead of being admitted")
        assert row["release_identity_ref"]["object_id"] == REL.object_id


# ===========================================================================
# Repair 4 — claim/evidence precision
# ===========================================================================


def test_currentness_vocabulary_is_closed_to_the_adopted_states():
    """The old code accepted ANY caller string outside four negative tokens."""
    rec, rule = two_admitted_receipt()
    assert set(B.ACCEPTED_CURRENTNESS_RESULTS) == set(PINNED_ACCEPTED_CURRENTNESS_RESULTS)
    assert B.ACCEPTED_CURRENTNESS_RESULTS_ARE_ADOPTED is True


@pytest.mark.parametrize("result", sorted(PINNED_REFUSED_ADOPTED_NONCURRENCY_STATES))
def test_adopted_non_currency_states_are_refused_not_recorded_as_positive(result):
    rec, rule = two_admitted_receipt()
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity, claim=result),
            receipt=rec, rule=rule, currentness_result=result)
    assert ei.value.reason_code in ("CURRENTNESS_MISSING_OR_CONFLICTING",
                                    "CURRENTNESS_RESULT_OUTSIDE_ADOPTED_VOCABULARY")


@pytest.mark.parametrize("result", sorted(PINNED_LEGACY_NEGATIVE_TOKENS))
def test_legacy_negative_currentness_tokens_still_refuse(result):
    rec, rule = two_admitted_receipt()
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity, claim=result),
            receipt=rec, rule=rule, currentness_result=result)
    assert ei.value.reason_code == "CURRENTNESS_MISSING_OR_CONFLICTING"


@pytest.mark.parametrize("bogus", ["FRESH", "LOOKS_GOOD", "ASSUMED_FINE", "YES", "OK", "2026"])
def test_ungoverned_caller_defined_currentness_vocabulary_is_refused(bogus):
    """The F4 defect: any caller string outside four negatives was accepted."""
    rec, rule = two_admitted_receipt()
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity, claim=bogus),
            receipt=rec, rule=rule, currentness_result=bogus)
    assert ei.value.reason_code == "CURRENTNESS_RESULT_OUTSIDE_ADOPTED_VOCABULARY", (
        f"an ungoverned positive currentness vocabulary must refuse, got "
        f"{ei.value.reason_code!r} for {bogus!r}")


def test_the_single_adopted_currency_state_is_accepted_and_recorded():
    rec, rule = two_admitted_receipt()
    b = B.bind_service_applicability_to_f8_scope(
        request=binding_request(identity=rec.service_request_set_identity, claim="CURRENT"),
        receipt=rec, rule=rule, currentness_result="CURRENT")
    assert b.currentness_result == "CURRENT"


def test_currentness_is_still_never_inferred_and_still_not_an_authority():
    """Pinning a vocabulary must not turn this binder into a currentness authority."""
    rec, rule = two_admitted_receipt()
    b = bind_exhaustive(rec, rule)
    assert b.currentness_result == B.CURRENTNESS_UNREQUESTED
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        b.currentness_authority()
    assert ei.value.reason_code == "BINDING_REFUSES_CURRENTNESS_AUTHORITY"
    with pytest.raises(B.ServiceF8ScopeBindingError) as ei:
        B.bind_service_applicability_to_f8_scope(
            request=binding_request(identity=rec.service_request_set_identity),
            receipt=rec, rule=rule, currentness_result="CURRENT")
    assert ei.value.reason_code == "CURRENTNESS_RESULT_WITHOUT_CLAIM"


def test_the_widened_attribute_scan_pins_the_full_inventory_and_no_conditioner():
    """Repair 4: the scan must cover the FULL attribute set, not a chosen subset."""
    tree = ast.parse(MODULE_PATH.read_text())
    read = {n.attr for n in ast.walk(tree) if isinstance(n, ast.Attribute)}
    forbidden = {
        "conditioner_bindings", "retained_conditioner_ids", "effective_time_or_interval",
        "geometry", "exact_geometry", "uncertainty_state", "raw_support", "walkback_steps",
        "positive_proxy_authority_refs", "slice_possibility", "possibility_geometry",
        "conditional_lookup_table", "projection", "point_masses", "density", "estimand",
        "distribution", "bandwidth", "variance", "posterior", "likelihood",
    }
    assert not (read & forbidden), (
        f"the binding reads conditioner/geometry/estimation attributes: "
        f"{sorted(read & forbidden)}")
    # The identity attributes the binder legitimately reads are present, so this court
    # is scanning the real inventory rather than an empty set.
    assert {"rule_hash", "model_rule_id", "algorithm_id", "source_universe_refs"} <= read


# ===========================================================================
# Repair 5 — write-terrain guards must fail, never skip
# ===========================================================================


def test_all_three_adopted_owners_are_byte_identical():
    """Fails loudly if an owner is absent or git is unavailable. Never skips."""
    repo = Path(MODULE_PATH).resolve().parents[1]
    for rel, expected in PINNED_ADOPTED_OWNER_BLOBS.items():
        path = repo / rel
        assert path.exists(), (
            f"REQUIRED ADOPTED OWNER ABSENT: {rel} at {path}. The byte-identity guard could "
            f"not run, so this qualification is NOT certified.")
        try:
            out = subprocess.run(["git", "-C", str(repo), "hash-object", str(path)],
                                 capture_output=True, text=True, timeout=60)
        except Exception as exc:
            pytest.fail(f"REQUIRED GIT FACILITY UNAVAILABLE: {exc!r}; the guard for {rel} "
                        f"could not run.")
        assert out.returncode == 0, (
            f"REQUIRED GIT FACILITY UNAVAILABLE: git hash-object exited {out.returncode} for {rel}")
        assert out.stdout.strip() == expected, f"{rel} was modified: {out.stdout.strip()}"


def test_no_write_terrain_guard_in_the_binder_court_skips():
    """Repair 5: a silent skip lets an all-green run hide a guard that never ran."""
    court = (MODULE_PATH.parents[0] / "tests"
             / "test_pre553_service_f8_source_scope_binding_court.py")
    assert court.exists(), f"the binding court must be present at {court}"
    tree = ast.parse(court.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr == "skip":
            args = [a.value for a in node.args if isinstance(a, ast.Constant)]
            raise AssertionError(
                f"the binding court calls pytest.skip({args}) at line {node.lineno}. A "
                f"write-terrain guard must fail loudly rather than skip.")


def test_the_repaired_module_itself_never_uses_pytest_skip():
    """The production binder has no test hooks at all."""
    assert "pytest" not in MODULE_PATH.read_text()


# ===========================================================================
# Preserved: the seam is still non-selecting and non-transformative
# ===========================================================================


#: Pinned as literals: any rank-like leaf in emitted binding material is a selection power.
PINNED_RANK_LIKE_TOKENS = (
    "rank", "score", "priority", "preference", "weight", "best", "first", "latest",
    "local", "top", "preferred", "ordering_value", "sort_key",
)


def _walk_values(obj, out):
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.add(str(k).lower())
            _walk_values(v, out)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            _walk_values(v, out)


def test_the_repair_added_no_rank_leaf_to_the_emitted_binding_material():
    """The substantive claim that IS exact, proven by VALUE INSPECTION (not by prose).

    Repair 2 must correct the COUNT without ever admitting a selection power, so the
    emitted material is searched recursively for any rank-like leaf.
    """
    rec, rule = two_admitted_receipt()
    b, _req = bind_single_for(rec, rule, A, with_request=True)
    keys: set[str] = set()
    _walk_values(b.material(), keys)
    # Negative disclaimer keys legitimately CONTAIN rank words while asserting their
    # ABSENCE. They are pinned here as disclaimers so the scan targets real rank leaves.
    disclaimers = {k for k in keys if any(
        neg in k for neg in ("no_rank", "grants_no", "not_a_selection", "no_ranking",
                             "no_priority", "no_preference", "no_weight", "no_source_order",
                             "unranked", "not_transform", "not_conditioning"))}
    substantive = keys - disclaimers
    found = sorted(t for t in PINNED_RANK_LIKE_TOKENS
                   if any(t in k for k in substantive))
    assert found == [], f"binding material carries rank-like leaves: {found}"
    # the unranked set must be exactly the admitted sources, with no ordering value
    exposed = b.expose_unranked_admitted_source_set(**authz(_req, rec, rule))
    assert set(exposed) == set(b.admitted_source_universe_refs)


def test_expose_unranked_set_still_refuses_under_incomplete_coverage():
    """The sustained INCOMPLETE hardening must survive the repair."""
    rec = resolve([A, BB], [admitted(A), negative(BB), ])
    from rawlsing_next.pre553_service_source_applicability import COVERAGE_INCOMPLETE
    rec = dataclasses_replace_coverage_incomplete(rec)
    rule = f8_rule((A,))
    b, req = bind_single_for(rec, rule, A, with_request=True)
    assert b.candidate_class_coverage == COVERAGE_INCOMPLETE
    with pytest.raises(B.ServiceF8ScopeBindingError):
        b.expose_unranked_admitted_source_set(**authz(req, rec, rule))


def dataclasses_replace_coverage_incomplete(rec):
    import dataclasses
    return dataclasses.replace(rec, candidate_class_coverage="INCOMPLETE")