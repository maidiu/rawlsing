"""HQ298 SM — TEST-ONLY source-free owner-effect stub.

###############################################################################
## LABELLED TEST-ONLY — NOT AN ADOPTED OWNER — NOT A V3 OPERATION            ##
##                                                                           ##
## This file is a LABORATORY TEST-ONLY executable stub produced under the     ##
## HQ298 SM commission's explicit fallback clause: "If owner rule is absent,  ##
## record precise missing source/module/authority; produce minimal            ##
## executable stub only as LABELLED TEST-ONLY, not adopted owner."            ##
##                                                                           ##
## It is NOT:                                                                ##
##   - an implementation of accepted CAN-008 / CAN-008 R2 runtime            ##
##   - an ADP-016 / ADP-017 owner transition producer                        ##
##   - a registered concrete R2 coupling rule                                ##
##   - an adopted V3 operation, actor run, or admitted occurrence issuer      ##
##                                                                           ##
## What IS reused from accepted, blob-verified project authority:            ##
##   - CAN-008 R2 occurrence gate law (b80dd6925066510ecbbfec7b427bf9f688475663) ##
##   - CAN-008 R2 effect vocabulary and noncollapse laws (same blob)         ##
##   - ADP-016 trace/access noncollapse semantics (0b7bbe29... / c6619a28...)   ##
##   - ADP-017 knowledge/access noncollapse semantics (6b4162df... / eece4f3f...)##
##   - SM predeclared LAB_R_K3 / LAB_R_K5 expected arm shapes                 ##
##     (7777a06dbd3a8f9dcf2b7ca3241e853dc485e505) — PROPOSED, never accepted  ##
##                                                                           ##
## What is TEST-ONLY fabricated (the missing producer, modelled not minted):  ##
##   - the concrete rule bodies LAB_R_K3 / LAB_R_K5                          ##
##   - the coupling evaluator and the target-owner effect transition         ##
##   - the ADP016 trace-commit / ADP017 epistemic transition executables     ##
###############################################################################
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Literal, Optional

STUB_GRAIN = "TEST_ONLY_STUB__NOT_ADOPTED_OWNER__NOT_V3_OPERATION"
STUB_RULE_STATUS = "TEST_ONLY_PROPOSED_NOT_ADOPTED"

# Reused from CAN-008 R2 adopted blob b80dd6925066510ecbbfec7b427bf9f688475663
CAN008_R2_EFFECT_VOCABULARY = ("BUFFER", "AMPLIFY", "DEFLECT", "REROUTE", "TRANSFORM", "BLOCK")
CAN008_R2_ADOPTED_BLOB = "b80dd6925066510ecbbfec7b427bf9f688475663"

IssuerRole = Literal["OFFICIAL", "PEER", "WORLD_SCHEDULE_OFFICE", "UNKNOWN"]
HistoryAxis = Literal["UNSAFE", "TRUSTED"]


class OccurrenceGateViolation(ValueError):
    """CAN-008 R2 occurrence gate: no committed causal response without an exact
    generated/admitted precipitating occurrence."""


class AccessLeakBlocked(ValueError):
    """ADP-017 / CAN-008 R2 hidden-cause firewall: UNAVAILABLE feature content
    cannot become a first-person claim."""


class AuthorityMismatch(ValueError):
    """Wrong source issuer / wrong occurrence identity / forced ratification."""


@dataclass(frozen=True)
class AdmittedEvent:
    """Minimal event-custody shape. Admission is DECLARED here; the real ADP-019
    admission producer is NOT present in this lab (see return 02)."""
    event_id: str
    kind: str
    issuer: str
    issuer_role: IssuerRole
    effective_time: str
    public_features: tuple[str, ...]
    admitted: bool
    admission_authority: str = "ADP019_EXTERNALLY_ADMITTED_OCCURRENCE"
    analyst_only_hidden_origin: Optional[str] = None  # never actor-readable
    content_state: str = "PUBLIC"


@dataclass(frozen=True)
class OwnerPrestate:
    """Read-only conditioning state bound to exact owner authority labels."""
    can010_striving: str
    can011_practice: str
    adp016_trace_id: Optional[str]
    adp016_trace_content_state: str  # AVAILABLE | UNAVAILABLE
    adp016_trace_usable_in_causal_role: bool
    adp017_first_person_permission: str  # DENY_HIDDEN_ORIGIN_CLAIM | ALLOWED
    history_axis: HistoryAxis
    prior_can008_response_count: int


@dataclass(frozen=True)
class CouplingRule:
    """TEST-ONLY concrete rule body. Rule ID mirrors SM's PROPOSED labels."""
    rule_id: str
    rule_version: str
    issuer_authority: str
    expected_event_issuer_role: IssuerRole
    expected_event_id: str
    effect_kind: str
    target_owner: str
    rule_status: str = STUB_RULE_STATUS

    def __post_init__(self):
        if self.effect_kind not in CAN008_R2_EFFECT_VOCABULARY:
            raise ValueError(f"effect_kind must be in R2 vocabulary: {self.effect_kind}")


def event_custody_check(event: AdmittedEvent, rule: CouplingRule) -> dict:
    """Occurrence gate + issuer + occurrence identity, per R2 sections 6 and 16."""
    if not event.admitted:
        raise OccurrenceGateViolation(
            f"BLOCK_UNADMITTED_EVENT:{event.event_id}: no committed causal response "
            "without an exact generated/admitted precipitating occurrence")
    if event.kind in ("V2_RENDER_CANDIDATE", "DRAFT_RESPONSE", "REJECTED_RENDER",
                      "UNEMITTED_CANDIDATE", "STATIC_STATE_RECORD"):
        raise OccurrenceGateViolation(
            f"BLOCK_NON_OCCURRENCE_KIND:{event.kind}: DRAFT_RESPONSE/REJECTED_RENDER/"
            "UNEMITTED_CANDIDATE -> NO_SELF_FEEDBACK; static state may condition "
            "but may not be relabeled as an occurrence")
    if event.event_id != rule.expected_event_id:
        raise AuthorityMismatch(
            f"BLOCK_WRONG_OCCURRENCE:{event.event_id}!={rule.expected_event_id}")
    if event.issuer_role != rule.expected_event_issuer_role:
        raise AuthorityMismatch(
            f"BLOCK_WRONG_SOURCE_ISSUER:{event.issuer_role}!={rule.expected_event_issuer_role}")
    return {"occurrence_gate": "ADMITTED_OCCURRENCE_CONFIRMED",
            "event_id": event.event_id, "issuer_role": event.issuer_role}


def coupling_evaluate(event: AdmittedEvent, prestate: OwnerPrestate,
                      rule: CouplingRule) -> dict:
    """TEST-ONLY coupling evaluation following CAN-008 R2 section shape:
    receivability -> uptake/appraisal -> situated recruitment -> response effect.
    Every noncollapse law of the adopted R2 blob is enforced on the way."""
    custody = event_custody_check(event, rule)

    # Receivability: event material the rule uses
    receivable = any(f in event.public_features for f in event.public_features)

    # Uptake/appraisal (projection, NOT durable belief)
    if rule.rule_id == "LAB_R_K3":
        uptake = "disruption_appraisal_under_routine_stability_striving"
    else:
        uptake = "recognition_appraisal_under_relationship_history"

    # Situated recruitment: recruitment != actor access
    recruited: list[str] = []
    if rule.rule_id == "LAB_R_K3" and prestate.adp016_trace_id and prestate.adp016_trace_usable_in_causal_role:
        recruited.append(f"ADP016:{prestate.adp016_trace_id}:CAUSAL_ROLE_ONLY")
    recruited.append(f"CAN011:{prestate.can011_practice}")
    recruited.append(f"CAN010:{prestate.can010_striving}")

    # Response effect (non-durable current consequence)
    if rule.rule_id == "LAB_R_K3":
        effect = "BUFFER" if any(r.startswith("ADP016:") for r in recruited) else "RESPONSE_EFFECTS_VALID_EMPTY"
    else:
        if event.issuer_role == "OFFICIAL" and prestate.history_axis == "UNSAFE":
            effect = "DEFLECT"
        elif event.issuer_role == "OFFICIAL":
            effect = "REROUTE"
        elif prestate.history_axis == "UNSAFE":
            effect = "DEFLECT"
        else:
            effect = "AMPLIFY"
    if effect not in CAN008_R2_EFFECT_VOCABULARY and effect != "RESPONSE_EFFECTS_VALID_EMPTY":
        raise ValueError("effect escaped R2 vocabulary")

    # Target-owner effect requests — NOT committed here (separate owner authority)
    target_owner_effect = {
        "target_owner": rule.target_owner,
        "commit_requires_separate_owner_authority": True,
        "committed_in_this_stub": False,
    }

    return {
        "grain": STUB_GRAIN,
        "rule_id": rule.rule_id,
        "rule_status": rule.rule_status,
        "custody": custody,
        "receivability": "RECEIVABLE" if receivable else "NOT_RECEIVABLE",
        "uptake_appraisal_projection": uptake,
        "situated_recruitment": recruited,
        "recruitment_is_not_actor_access": True,
        "response_effect_kind": effect,
        "response_durability": "NON_DURABLE_CURRENT_CONSEQUENCE",
        "target_owner_effect": target_owner_effect,
        "decision_status": "TEST_ONLY_PROTOTYPE_CAUSAL_EFFECT",
    }


def adp016_trace_commit_request(trace_id: str, basis_event_id: str,
                                content_state: str) -> dict:
    """TEST-ONLY ADP-016 durable trace-commit REQUEST. The accepted ADP-016 owner
    transition producer does not exist in staged code; this returns a request
    shape and refuses to claim a commit."""
    return {
        "request_kind": "ADP016_TRACE_COMMIT_REQUEST",
        "trace_id": trace_id,
        "basis_event_id": basis_event_id,
        "content_state": content_state,
        "committed": False,
        "refusal": "MISSING_IMPLEMENTATION:ADP016_OWNER_TRANSITION_PRODUCER",
        "law_reused": "ADP016: memory/causal traces only after generated/admitted basis; "
                      "inaccessible contents cannot be rehydrated",
    }


def adp017_first_person_claim_check(prestate: OwnerPrestate,
                                    claimed_origin: Optional[str],
                                    event: AdmittedEvent) -> dict:
    """ADP-017 knowledge/access gate. Objective truth != actor knowledge;
    UNAVAILABLE feature content cannot become a first-person claim."""
    if claimed_origin is not None:
        if prestate.adp017_first_person_permission == "DENY_HIDDEN_ORIGIN_CLAIM":
            raise AccessLeakBlocked(
                "BLOCK_UNAVAILABLE_CHILDHOOD_FEATURE_TO_FIRST_PERSON: "
                f"claim={claimed_origin}")
        if (event.analyst_only_hidden_origin is not None
                and claimed_origin == event.analyst_only_hidden_origin
                and prestate.adp016_trace_content_state == "UNAVAILABLE"):
            raise AccessLeakBlocked("BLOCK_HIDDEN_ORIGIN_FALSE_EXPLANATORY_ANSWER")
    return {
        "first_person_claim": None,
        "claim_permission": "DENY_FIRST_PERSON_CLAIM",
        "objective_truth_separate_from_knowledge": True,
        "trace_recruited_in_causal_role_only": True,
    }


def institutional_ratification_check(event: AdmittedEvent,
                                     world_owner_grant: bool,
                                     conferral_attempt: Optional[str]) -> dict:
    """K5 world/felt orthogonality: peer cannot confer institution status;
    official grant cannot compel felt belief; missing world-owner grant bars
    objective change."""
    institutional_permission = "PRESENT" if event.issuer_role == "OFFICIAL" else "ABSENT"
    if conferral_attempt == "PEER_CONFERS_OFFICIAL_STATUS" and event.issuer_role != "OFFICIAL":
        raise AuthorityMismatch("BLOCK_PEER_CANNOT_CONFER_INSTITUTIONAL_STATUS")
    world_effect = ("OFFICIAL_RECOGNITION"
                    if institutional_permission == "PRESENT" and world_owner_grant
                    else "NO_INSTITUTIONAL_CHANGE")
    return {
        "institutional_permission": institutional_permission,
        "world_effect": world_effect,
        "world_effect_is_committed": False,
        "official_grant_does_not_compel_felt_belief": True,
    }


def next_event_response(post_owner_state: dict, next_event: AdmittedEvent,
                        rule: CouplingRule) -> dict:
    """Subsequent typed response at t2 against post-t1 owner state. Never uses
    prior response prose as a synthetic occurrence."""
    if next_event.kind in ("V2_RENDER_CANDIDATE", "DRAFT_RESPONSE"):
        raise OccurrenceGateViolation("BLOCK_SELF_FEEDBACK_ON_PRIOR_PROSE")
    return {
        "event_id": next_event.event_id,
        "evaluated_against_post_owner_state": sorted(post_owner_state.keys()),
        "typed_effect_stream": post_owner_state.get("committed_effect_stream", "NONE"),
        "prior_prose_used_as_occurrence": False,
    }


# ---------------------------------------------------------------------------
# K3 / K5 arm fixtures (shapes frozen in 01_PREDECLARED_POSITIVE_CELL_AND_ARMS.json)
# ---------------------------------------------------------------------------

def k3_arms() -> dict[str, dict]:
    return {
        "K3_A_TRACE": {"trace_formed": True, "trace_use_rule": True,
                       "child_feature_state": "UNAVAILABLE"},
        "K3_B_NO_TRACE": {"trace_formed": False, "trace_use_rule": False,
                          "child_feature_state": "UNAVAILABLE"},
        "K3_C_UNAVAILABLE_NO_TRACE": {"trace_formed": False, "trace_use_rule": False,
                                      "child_feature_state": "UNAVAILABLE"},
    }


def run_k3_arm(arm: dict) -> dict:
    if arm["trace_formed"] and arm["trace_use_rule"]:
        return {"trace_recruitment": "ADP016_TRACE_T7",
                "effect": "BUFFER",
                "claim": "DENY_FIRST_PERSON_CLAIM"}
    return {"trace_recruitment": "NONE",
            "effect": "RESPONSE_EFFECTS_VALID_EMPTY",
            "claim": "DENY_FIRST_PERSON_CLAIM"}


def run_k5_arm(world_role: IssuerRole, history: HistoryAxis,
               world_owner_grant: bool) -> dict:
    event = AdmittedEvent(
        event_id="E_OFFICIAL_SAME_TEXT", kind="EXTERNAL_RUNTIME_EVENT",
        issuer="SAME_TEXT_ISSUER", issuer_role=world_role,
        effective_time="t1", public_features=("same_text",),
        admitted=True)
    institutional = "PRESENT" if world_role == "OFFICIAL" else "ABSENT"
    world_effect = ("OFFICIAL_RECOGNITION" if institutional == "PRESENT" and world_owner_grant
                    else "NO_INSTITUTIONAL_CHANGE")
    if world_role == "OFFICIAL" and history == "UNSAFE":
        felt = "DEFLECT"
    elif world_role == "OFFICIAL":
        felt = "REROUTE"
    elif history == "UNSAFE":
        felt = "DEFLECT"
    else:
        felt = "AMPLIFY"
    return {"institutional_permission": institutional,
            "world_effect": world_effect,
            "effect": felt}
