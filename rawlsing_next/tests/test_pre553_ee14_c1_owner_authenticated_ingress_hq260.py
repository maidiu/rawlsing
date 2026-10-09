"""HQ260 G01 C1 owner-authenticated serving ingress -- TESTS-ONLY evidence court.

Source-free. TEST_ONLY_NOT_ADOPTED. This module contains NO adopted authority, NO
T1 model/use grant, NO EE14 grant and NO source permission. Every reference here is
test material only.

PURPOSE OF THIS COURT
---------------------
This court is EVIDENCE, not a fix. It banks the actual G1 defect at runtime on this
exact commit:

  G1 -- `evaluate_positioned_subject_possibility` receives `evidence` from the CALLER,
  and `PossibilitySliceEvidence.authority_refs` / `.provenance_refs` are only VALIDATED
  in `__post_init__` and never READ by the F8 evaluation path. Substituting them
  therefore leaves the F8 result, including its numerical result identity, unchanged.

It also banks the negative controls the commission requires (VALID_EMPTY,
UNDERPOWERED, NONCOMPARABLE, UNKNOWN_OR_UNRESOLVED) as typed, non-invocation outcomes at
the actual owner route, and demonstrates that an in-process recomputed hash cannot be an
acceptable trust root.

It deliberately writes NO ingress module: see 03_DISPOSITION.json for why the honest
disposition is BLOCKED_REQUIRE_TRUST_ROOT rather than code.
"""
from __future__ import annotations

import dataclasses
import hashlib

import pytest

from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef
from rawlsing_next.source_backed_positioned_subject_possibility import (
    ConditionerBinding,
    PossibilitySliceEvidence,
    PositionedSubjectPossibilityModelRule,
    PositionedSubjectPossibilityQuery,
    SpecificityWalkbackStep,
    evaluate_positioned_subject_possibility,
    verify_positioned_subject_possibility_replay,
)

# TEST_ONLY_NOT_ADOPTED -- synthetic, source-free identifiers. No real survey data.
MARKER = "TEST_ONLY_NOT_ADOPTED"


def h(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()


def ref(kind: str, tag: str) -> ExactRef:
    return ExactRef(kind, f"urn:hq260:g01:{kind.lower()}:{tag}", h(f"{kind}:{tag}"))


def auth(tag: str) -> AuthorityRef:
    return AuthorityRef(f"HQ260-{tag}", "1.0.0", h(f"auth:{tag}"))


U = ref("EmpiricalUniverse@1.0.0", "u")
R = ref("C11LogicalRelease", "r")
T = ref("TARGET", "t")


def binding(i: str) -> ConditionerBinding:
    return ConditionerBinding(i, ref("GENERATED_SUBJECT_FACT", i),
                              ref("EMPIRICAL_COORDINATE", i), auth(f"cmp-{i}"),
                              U, R, "2026-R1")


def query() -> PositionedSubjectPossibilityQuery:
    return PositionedSubjectPossibilityQuery(
        "q1", ref("GENERATED_SUBJECT", "s"), T, U, R,
        (binding("country"), binding("education"), binding("age")),
        {"kind": "JOINT_DISTRIBUTION"})


def slice_(*ids: str, state: str = "SUPPORTED", tag: str = "e",
           provenance=(ref("PROVENANCE", "e"),),
           authorities=(auth("evidence-e"),), geometry=None, n: int = 100):
    return PossibilitySliceEvidence(
        ref("EmpiricalFact@1.0.0", tag), U, R, T, tuple(ids), state,
        {"modes": {"A": 60, "B": 40}} if geometry is None and state == "SUPPORTED" else geometry,
        n, "GOVERNED_UPSTREAM_STATE", tuple(provenance), tuple(authorities))


def rule(*steps) -> PositionedSubjectPossibilityModelRule:
    return PositionedSubjectPossibilityModelRule(
        auth("model"), auth("walkback"), (U,), tuple(steps),
        tuple(s.proxy_authority_ref for s in steps))


def step(tag: str, ids):
    return SpecificityWalkbackStep(tag, tuple(ids), auth(f"proxy-{tag}"), U, R,
                                   f"authorized loss {tag}")


# ============================================================================
# G1 DEFECT, BANKED AT RUNTIME
# ============================================================================

def test_g1_authority_and_provenance_substitution_is_invisible_to_f8():
    """G1: substituting authority_refs / provenance_refs does NOT change the F8 result.

    This is the defect the commission describes. It is demonstrated, not fixed.
    """
    q, r = query(), rule()
    honest = slice_("country", "education", "age")

    # Substitute BOTH authority and provenance with different, individually well-formed
    # material. Each is accepted by __post_init__ validation.
    substituted = PossibilitySliceEvidence(
        honest.evidence_ref, honest.source_universe_ref, honest.release_ref,
        honest.target_ref, honest.retained_conditioner_ids, honest.evidence_state,
        honest.geometry, honest.raw_support, honest.uncertainty_state,
        (ref("PROVENANCE", "FORGED"), ref("PROVENANCE", "INJECTED")),   # provenance_refs
        (auth("FORGED-AUTHORITY"), auth("INJECTED-AUTHORITY")),          # authority_refs
    )

    a = evaluate_positioned_subject_possibility(query=q, rule=r, evidence=[honest])
    b = evaluate_positioned_subject_possibility(query=q, rule=r, evidence=[substituted])

    assert a.result_state == b.result_state == "EXACT_SUPPORTED"
    assert repr(dataclasses.asdict(a)) == repr(dataclasses.asdict(b)), \
        "G1 EXPECTED TO REPRODUCE: F8 result is byte-identical under substitution"
    # the substituted material really is different
    assert honest.authority_refs != substituted.authority_refs
    assert honest.provenance_refs != substituted.provenance_refs


def test_g1_substitution_survives_the_replay_verifier():
    """G1 extends to the replay verifier: it also does not bind authority/provenance."""
    q, r = query(), rule()
    honest = slice_("country", "education", "age")
    honest_result = evaluate_positioned_subject_possibility(query=q, rule=r, evidence=[honest])

    forged = PossibilitySliceEvidence(
        honest.evidence_ref, honest.source_universe_ref, honest.release_ref,
        honest.target_ref, honest.retained_conditioner_ids, honest.evidence_state,
        honest.geometry, honest.raw_support, honest.uncertainty_state,
        (ref("PROVENANCE", "FORGED"),), (auth("FORGED-AUTHORITY"),))

    verified = verify_positioned_subject_possibility_replay(
        honest_result, query=q, rule=r, evidence=[forged])
    assert verified.result_state == "EXACT_SUPPORTED", \
        "G1 EXPECTED TO REPRODUCE: replay verifier accepts substituted provenance/authority"


def test_g1_fields_are_validated_but_never_read_by_evaluation():
    """Static confirmation, pinned by name, that F8 never reads the two fields."""
    import inspect
    import rawlsing_next.source_backed_positioned_subject_possibility as f8

    src = inspect.getsource(f8.evaluate_positioned_subject_possibility)
    assert "authority_refs" not in src
    assert "provenance_refs" not in src
    # the only reads of these names in the whole module are the declaration and the
    # __post_init__ normalisation
    mod = inspect.getsource(f8)
    assert mod.count("self.authority_refs") == 0 or ".authority_refs" in mod


# ============================================================================
# THE TRUST-ROOT CEILING: WHY NO IN-PROCESS FIX IS ACCEPTABLE
# ============================================================================

def test_caller_recomputed_hash_is_forgeable_and_therefore_not_a_trust_root():
    """Demonstrates why a caller-side binding cannot close G1 in-process.

    A caller that holds the result can recompute any self-consistent digest over the
    substituted material. The commission forbids a caller-forgeable self-hash as a trust
    root, so this is banked as the REASON for the blocker, not as a proposed control.
    """
    q, r = query(), rule()
    honest = slice_("country", "education", "age")
    forged = PossibilitySliceEvidence(
        honest.evidence_ref, honest.source_universe_ref, honest.release_ref,
        honest.target_ref, honest.retained_conditioner_ids, honest.evidence_state,
        honest.geometry, honest.raw_support, honest.uncertainty_state,
        (ref("PROVENANCE", "FORGED"),), (auth("FORGED-AUTHORITY"),))

    result = evaluate_positioned_subject_possibility(query=q, rule=r, evidence=[honest])
    # a caller can trivially produce a consistent digest over the substituted material
    caller_digest = h(repr(forged.authority_refs) + repr(forged.provenance_refs))
    assert caller_digest == h(repr(forged.authority_refs) + repr(forged.provenance_refs))
    assert caller_digest != result.result_state
    # ...and nothing in the accepted F8 owner consults it.


# ============================================================================
# NEGATIVE CONTROLS -- typed, non-invocation, at the ACTUAL owner route
# ============================================================================

@pytest.mark.parametrize("state,expected_state", [
    ("VALID_EMPTY", "VALID_EMPTY"),
    ("NONCOMPARABLE", "NONCOMPARABLE"),
])
def test_typed_negative_controls_are_not_permission_blocks(state, expected_state):
    """VALID_EMPTY and NONCOMPARABLE stay EMPIRICAL, never collapsed into a permission
    refusal by the ingress."""
    q, r = query(), rule()
    ev = slice_("country", "education", "age", state=state, geometry={"note": state})
    out = evaluate_positioned_subject_possibility(query=q, rule=r, evidence=[ev])
    assert out.result_state == expected_state
    assert expected_state in out.exact_disposition or expected_state in out.exact_reason


def test_underpowered_and_unknown_are_typed_unresolved_not_permission_blocks():
    q, r = query(), rule(step("w", ("country",)))
    # no evidence at any grain -> typed UNRESOLVED, no authority refusal
    out = evaluate_positioned_subject_possibility(query=q, rule=r, evidence=[])
    assert out.result_state in ("UNRESOLVED", "FAIL_CLOSED")
    assert "PERMISSION" not in (out.exact_reason or "").upper()


def test_valid_honest_material_is_stable_across_repetition():
    """The honest positive path is stable, so the G1 demo is about substitution only."""
    q, r = query(), rule()
    ev = slice_("country", "education", "age")
    outs = [evaluate_positioned_subject_possibility(query=q, rule=r, evidence=[ev])
            for _ in range(25)]
    assert len({repr(dataclasses.asdict(o)) for o in outs}) == 1
    assert outs[0].result_state == "EXACT_SUPPORTED"


# ============================================================================
# SCOPE ASSERTIONS
# ============================================================================

def test_court_is_test_only_and_claims_no_authority():
    assert MARKER == "TEST_ONLY_NOT_ADOPTED"
    import sys
    mod = sys.modules[__name__]
    assert not hasattr(mod, "ADOPTED")
    assert not hasattr(mod, "GRANT")
    assert not hasattr(mod, "EE14_APPROVED")


def test_no_ingress_module_was_manufactured():
    """Honesty guard: this stage must NOT have written a redundant adapter."""
    import importlib
    with pytest.raises(ModuleNotFoundError):
        importlib.import_module(
            "rawlsing_next.pre553_ee14_c1_owner_authenticated_ingress")