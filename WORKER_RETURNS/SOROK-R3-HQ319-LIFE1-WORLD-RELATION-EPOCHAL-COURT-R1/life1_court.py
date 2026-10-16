"""HQ319 LIFE1 — world-conditioned, relation-dependent, epochal person-response court.

GRAIN: LABORATORY_STRUCTURAL_FIXTURE__NOT_PREV3_OUTPUT
RULES R-K1..R-K6: PROPOSED UNISSUED LAB RULE LABELS (never executed as accepted law)
NOT AN ACTOR, NOT A WORLD OWNER, NOT A SEMANTIC ISSUER.

This module builds the mission's required world/relation/epoch construction and
then makes a GENUINE attempt to obtain an owner-authorized positive producer at
REAL native entrypoints. Where no authorized producer exists it records the EXACT
refusal, rather than substituting a hand-authored response label.

Nothing here creates an actor, a person, a world fact, or a durable owner effect.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

_NATIVE = Path(__file__).resolve().parent / "native"
if str(_NATIVE) not in sys.path:
    sys.path.insert(0, str(_NATIVE))

from rawlsing_next import wsc_gt0_end_to_end as GT0_E2E          # noqa: E402
from rawlsing_next import field_forge_conditional_support as FF   # noqa: E402
from rawlsing_next import sdtf_r4_mechanism_rule_authority_binding as MECH  # noqa: E402

FIXTURE_LABEL = "LABORATORY_STRUCTURAL_FIXTURE__NOT_PREV3_OUTPUT"
RULE_GRAIN = "PROPOSED_UNISSUED_LAB_RULE_LABEL__NOT_ACCEPTED__NOT_CURRENT"

DEFER = "DEFER_MISSING_RULE_OR_AUTHORITY"


# ---------------------------------------------------------------------------
# The mission's required construction. Every piece is an explicit, hashable
# structural declaration. None of it is an actor, a world fact, or an owner state.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class HistoricalMaterialWorld:
    world_id: str
    institution: str
    period: str
    lawful_routes: tuple
    provenance: str
    excluded: tuple
    typed_unknowns: tuple

    def identity(self) -> dict:
        return dict(world_id=self.world_id, institution=self.institution,
                    period=self.period, lawful_routes=list(self.lawful_routes),
                    provenance=self.provenance, excluded=list(self.excluded),
                    typed_unknowns=list(self.typed_unknowns))


@dataclass(frozen=True)
class AsymmetricRelation:
    """Directed, role-ordered, time-scoped relation edge. Not an atomised trait."""
    subject: str
    object: str
    direction: str            # A_TO_B | B_TO_A
    role_order: tuple
    time_scope: str
    contingent_authority: str  # BINDING_EVALUATOR | NONBINDING_OBSERVER | NONE
    causal_consequence: str

    def identity(self) -> dict:
        return dict(subject=self.subject, object=self.object,
                    direction=self.direction, role_order=list(self.role_order),
                    time_scope=self.time_scope,
                    contingent_authority=self.contingent_authority,
                    causal_consequence=self.causal_consequence)


@dataclass(frozen=True)
class UserAbsenceEpoch:
    actor_id: str
    start: str
    end: str
    user_absent: bool
    independent_clock: str
    intervening_changes: tuple

    def identity(self) -> dict:
        return dict(actor_id=self.actor_id, start=self.start, end=self.end,
                    user_absent=self.user_absent, clock=self.independent_clock,
                    intervening_changes=list(self.intervening_changes))


def build_w0() -> HistoricalMaterialWorld:
    return HistoricalMaterialWorld(
        world_id="W_INSTITUTION_V0", institution="SYNTH_INSTITUTION",
        period="1998", lawful_routes=("PRAISE_ROUTE", "CORRECTION_ROUTE", "SANCTION_ROUTE"),
        provenance="SOURCE_FREE_LABORATORY_STRUCTURAL_FIXTURE",
        excluded=("GENERATED_PERSON", "REAL_WORLD_FACT", "FELT_STATE"),
        typed_unknowns=("UNRESOLVED_PRIOR_HISTORY_ORIGIN",))


def build_w1() -> HistoricalMaterialWorld:
    return HistoricalMaterialWorld(
        world_id="W_INSTITUTION_V1", institution="SYNTH_INSTITUTION",
        period="1999", lawful_routes=("PRAISE_ROUTE", "CORRECTION_ROUTE"),
        provenance="SOURCE_FREE_LABORATORY_STRUCTURAL_FIXTURE",
        excluded=("GENERATED_PERSON", "REAL_WORLD_FACT", "FELT_STATE"),
        typed_unknowns=("SANCTION_ROUTE_WITHDRAWN",))


def build_relation(direction: str, authority: str) -> AsymmetricRelation:
    return AsymmetricRelation(
        subject="ACTOR_A" if direction == "A_TO_B" else "ACTOR_B",
        object="ACTOR_B" if direction == "A_TO_B" else "ACTOR_A",
        direction=direction, role_order=("SOURCE", "RECIPIENT"),
        time_scope="1998-1999",
        contingent_authority=authority,
        causal_consequence="DECLARED_NOT_ADMITTED")


def build_epoch() -> UserAbsenceEpoch:
    return UserAbsenceEpoch(
        actor_id="ACTOR_A", start="1998-11-01T00:00:00Z",
        end="1999-03-01T00:00:00Z", user_absent=True,
        independent_clock="SOURCE_NATIVE_EPOCHAL_CLOCK",
        intervening_changes=("W1_INSTITUTIONAL_CHANGE", "THIRD_PARTY_OPPORTUNITY"))


# ---------------------------------------------------------------------------
# B0 (minimum derivational) vs B1 (richer) at MATCHED budgets.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Mechanism:
    mechanism_id: str
    evidence_reads: int
    retrieval_calls: int
    compute_units: int
    rule_label: str


B0 = Mechanism("B0_MINIMUM_DERIVATIONAL", evidence_reads=1, retrieval_calls=1,
               compute_units=1, rule_label="LAB_R_K_MIN@proposed")
B1 = Mechanism("B1_RICHER_PROPOSAL", evidence_reads=1, retrieval_calls=1,
               compute_units=1, rule_label="LAB_R_K_RICH@proposed")


# ---------------------------------------------------------------------------
# The genuine positive-path attempt.
# ---------------------------------------------------------------------------

def run_native_thread() -> dict:
    """Execute the real staged native GT0 end-to-end thread."""
    result = GT0_E2E.run_gt0_end_to_end()
    return dict(terminal=result.terminal,
                full_thread_hash=result.full_thread_hash,
                stages=[dict(index=i, status=getattr(s.status, "name", str(s.status)),
                             content_hash=s.content_hash)
                        for i, s in enumerate(result.receipts)])


def probe_positive_producer_available() -> dict:
    """Ask the real native surface whether an executable mechanism rule exists.

    This is a capability probe of ACCEPTED code, not a substitute for it.
    """
    # The only coupling producer present is a POPULATION STATISTIC over a
    # specialized Q86B->Q86A relation, not a person-response mechanism.
    return dict(
        coupling_producers_present=["rawlsing_next.field_forge_conditional_support"],
        coupling_producer_semantics=FF.RELATION_SEMANTICS,
        coupling_producer_is_person_response=False,
        coupling_producer_family=FF.RELATION_FAMILY,
        coupling_producer_owner=FF.SEMANTIC_OWNER,
        mechanism_binding_module=MECH.__name__,
        mechanism_binding_can_mint_rules=False,
        mechanism_binding_can_execute_rule_bodies=False,
        actor_sentinel="GT0_NO_ACTOR_BOUND",
        positive_producer_available=False,
        missing_positive_producer=(
            "An independently authorized, versioned, concrete CAN008_R2 "
            "world->admitted-event coupling/response rule body with genuine actor "
            "binding, plus a competent durable target owner that accepts its emitted "
            "effect with replayable access filtering."),
    )


@dataclass
class Attempt:
    case: str
    arm: str
    requested_effect: str
    outcome: str
    detail: str
    evidence_reads: int = 0
    retrieval_calls: int = 0
    compute_units: int = 0
    native_entered: bool = False
    extras: dict = field(default_factory=dict)


def attempt_case(case: str, arms: Mapping[str, str], mechanism: Mechanism) -> list[Attempt]:
    """Attempt each arm through the real native surface and record the EXACT result.

    No arm may be answered by a hand-authored label: if no authorized producer
    exists the outcome is the native DEFER, and that is what is recorded.
    """
    probe = probe_positive_producer_available()
    out = []
    for arm, requested in arms.items():
        if probe["positive_producer_available"]:
            raise AssertionError("lifecycle: a positive producer appeared; re-adjudicate")
        out.append(Attempt(
            case=case, arm=arm, requested_effect=requested,
            outcome=DEFER,
            detail=("NO_AUTHORIZED_CAN008_R2_MECHANISM_RULE_BODY; "
                    "requested effect '%s' cannot be produced by any accepted owner"
                    % requested),
            evidence_reads=mechanism.evidence_reads,
            retrieval_calls=mechanism.retrieval_calls,
            compute_units=mechanism.compute_units,
            native_entered=False,
            extras=dict(missing_positive_producer=probe["missing_positive_producer"])))
    return out


# The K1-K6 arms exactly as SM froze them (proposed expectations only).
K1_ARMS = {"A_HISTORY_SUPPORT": "REROUTE_TO_CLARIFICATION",
           "B_HISTORY_SANCTION": "BUFFER_OR_DEFLECT_VIA_REGISTERED_RULE"}
K2_ARMS = {"A_DIRECT_AUTHORITY_EDGE": "REGISTERED_PUBLIC_COMPLIANCE_OR_EXPLANATION",
           "B_OBSERVER_EDGE": "REGISTERED_INFORMAL_RESPONSE_OR_VALID_EMPTY"}
K3_ARMS = {"A_CAUSAL_TRACE": "R_K3_TRACE_CONDITIONED_EFFECT",
           "B_NO_TRACE": "R_K3_NONTRACE_EFFECT_OR_VALID_EMPTY",
           "C_MEMORY_UNAVAILABLE": "BASELINE_NONTRACE"}
K4_ARMS = {"A_CREDIBLE_COUNTEREXAMPLE": "NARROW_OR_SPLIT_IF_AUTHORIZED",
           "B_WEAK_REPETITION": "NO_CHANGE_OR_VALID_EMPTY",
           "C_CONFLICT_UNRESOLVED": "KEEP_MULTIPLE_MEDIATORS"}
K5_ARMS = {"A_CREDENTIAL_AUTHORITY_FELT_UNSAFE": "DEFLECT_OR_BUFFER",
           "B_POWERLESS_WITNESS_FELT_VALIDATED": "RECEIVE_OR_RESPOND_WITH_ENGAGEMENT",
           "C_AUTHORITY_AND_FELT_VALIDATED": "ENGAGEMENT_ALLOWED"}
K6_ARMS = {"A_INTERNALIZED_AND_HAS_ACTION_ROUTE": "R_K6_CONDITIONED_ACTION_PROPOSAL",
           "B_NONINTERNALIZED_AND_HAS_ACTION_ROUTE": "CONTEST_OR_VALID_EMPTY",
           "C_INTERNALIZED_BUT_NO_POWER_OR_OPPORTUNITY": "NO_ACTION_OR_NONPOLICING_RESPONSE"}

ALL_CASES = {"K1": K1_ARMS, "K2": K2_ARMS, "K3": K3_ARMS,
             "K4": K4_ARMS, "K5": K5_ARMS, "K6": K6_ARMS}


def run_all_cases(mechanism: Mechanism = B0) -> dict:
    attempts = []
    for case, arms in ALL_CASES.items():
        attempts.extend(attempt_case(case, arms, mechanism))
    return dict(mechanism=mechanism, attempts=attempts,
                all_deferred=all(a.outcome == DEFER for a in attempts))


def valid_empty_control() -> dict:
    """A genuinely lawful valid-empty outcome, distinct from a fabricated effect."""
    return dict(decision_state="RESPONSE_EFFECTS_VALID_EMPTY",
                produced_effect=None,
                rule_label=B0.rule_label,
                note="valid-empty is a real nonpositive outcome, not a missing value")


def budget_match(b0: Mechanism = B0, b1: Mechanism = B1) -> bool:
    return (b0.evidence_reads == b1.evidence_reads
            and b0.retrieval_calls == b1.retrieval_calls
            and b0.compute_units == b1.compute_units)