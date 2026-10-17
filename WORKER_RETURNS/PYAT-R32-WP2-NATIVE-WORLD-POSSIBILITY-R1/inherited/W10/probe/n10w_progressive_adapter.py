"""Smallest N10W progressive world-conditioned parent/coparent adapter candidate.

This is an ISOLATED INTERFACE CANDIDATE living only in the W10 worker-return
terrain.  It is NOT an adopted N10W owner and does NOT claim integrated PASS.

It is the first evidenced absent joint edge of the E05 return:
  a competent TEST_ONLY selected-world snapshot (actual M4 resolve_v558 +
  M5 materialize_resolved_structural_context) PLUS the exact computed N10E
  slice (actual provider/C1/public consumer) jointly enter a world-conditioned
  progressive parent/coparent conditioning service with two conditioning steps
  (C1 institutional access, C2 parent/coparent household care-time premise),
  an exact consumer receipt, typed refusals, uncertainty and preserved
  alternatives, and a hard actor firewall.

Probability law: route probabilities are ALWAYS null with an explicit reason.
The only numeric probabilities anywhere in the receipt are the N10E computed
exact fractions at their own declared empirical grain; they are never merged
into route probabilities (no cross-grain join).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash

from probe.modeled_selected_world import (
    DECLARED_HISTORICAL_YEAR,
    DECLARED_UNIT_SCOPE,
    CARE_TIME_KEYS,
    HOUSEHOLD_CARE_KEYS,
    INSTITUTIONAL_KEYS,
    WORLD_FACT_KEYS,
    WORLD_GRADE,
    ModeledSelectedWorld,
)
from probe.n10e_computed_edge import N10EComputedProduct, N10E_LANE_GRADE

RECEIPT_SCHEMA = "W10_N10W_PROGRESSIVE_WORLD_CONSUMER_RECEIPT@1"
ADAPTER_CONTRACT_ID = "W10_N10W_PROGRESSIVE_PARENT_COPARENT_ADAPTER@1.0.0"
ADAPTER_GRADE = (
    "TEST_ONLY_INTERFACE_COURT__NOT_OPERATIVE_N9_WORLD__NOT_INTEGRATED_N10W_OWNER__"
    "NO_ACTOR__NO_MODEL_USE_ISSUER"
)
CONSUMER_ID = (
    "urn:rawlsing:hq295-w10:consumer:E05_VERTICAL_WORLD_N10E_N10W_PROBE@1"
)

ROUTES = (
    "formal_schooling",
    "nonformal_peer_study",
    "paid_apprenticeship",
    "family_care_work",
    "mutual_aid_participation",
)

PROBABILITY_NULL_REASON = (
    "NO_OPERATIVE_MODEL_USE_ISSUER__NO_MEASURED_ROUTE_PROBABILITY__NO_NUMERIC_IMPUTATION"
)

FORBIDDEN_REQUESTED_OUTPUTS = frozenset(
    {
        "ENNEAGRAM_TYPE",
        "PERSONALITY_TYPE",
        "HEALTH_SCORE",
        "BELIEFS",
        "VOICE",
        "BIOGRAPHY",
        "PERSONAL_EXPERIENCE",
        "PSYCHE_STATE",
        "DEVELOPMENTAL_PATHOLOGY",
        "FINAL_TYPE",
    }
)

#: Assignment-shaped psyche/type/voice/biography tokens.  Explicit UNKNOWN
#: declarations (e.g. ``enneagram_type: UNKNOWN_NOT_ASSIGNED``) live only in the
#: receipt ``unknowns`` block and are NOT scanned as claims; only claim-bearing
#: surfaces (route states/eligibilities, witnesses, requested outputs, subject
#: selector) are scanned.
FORBIDDEN_INFERENCE_TOKENS = (
    "IS_TYPE",
    "IS TYPE",
    "TYPE_5",
    "TYPE 5",
    "TYPE_6",
    "TYPE 6",
    "ENNEAGRAM",
    "TRAUMATIZ",
    "ATTENDS_SCHOOL",
    "ATTENDS SCHOOL",
    "HAS_SUPPORTING_PARENT",
    "DESIRES_EDUCATION",
    "REJECTS_EDUCATION",
    "ACTUAL_DEPENDENT",
    "NEVER_POSSIBLE_LATER",
    "COLLECTIVE_TRAUMA",
    "CLASS_AS_FINAL",
    "BIOGRAPHY_ASSIGNED",
    "VOICE_ASSIGNED",
    "PERSONALITY_ASSIGNED",
    "BELIEF_ASSIGNED",
    "EXPERIENCE_ASSIGNED",
    "PATHOLOGY_ASSIGNED",
)

GRADE_INDIVIDUAL = "INDIVIDUAL_SELECTOR"
GRADE_DYAD = "HOUSEHOLD_COPARENT_DYAD"

REFUSAL_H01 = "REJECT_REAL_WORLD_AUTHORITY_PROMOTION"
REFUSAL_H02 = "REJECT_DIRECT_STATIC_TYPE_ASSIGNMENT"
REFUSAL_H03 = "REJECT_UNLICENSED_DYAD_OR_RESPONSE_JOIN"
REFUSAL_H04 = "REJECT_UNSUPPORTED_PRECISION"
REFUSAL_H05 = "REJECT_UNISSUED_TEMPORAL_COMPARABILITY"
REFUSAL_H07 = "REJECT_MISSING_CURRENTNESS_OR_ISSUER"
REFUSAL_H08 = "NO_ACTOR_RUN_OR_MODEL_INVOCATION"
REFUSAL_H09 = "REJECT_MINOR_ROUTE_ERASURE"
REFUSAL_UNIT = "WORLD_SUBJECT_UNIT_MISMATCH"
REFUSAL_YEAR = "WORLD_AS_OF_YEAR_MISMATCH"
REFUSAL_SCOPE = "WORLD_SCOPE_NOT_AUTHORIZED"
REFUSAL_CURRENTNESS = "WORLD_CURRENTNESS_NOT_CURRENT__NO_STALE_SELECTED_TRUTH"
REFUSAL_SELECTION = "WORLD_SELECTION_INCOMPLETE"
REFUSAL_WORLD_GRADE = "WORLD_GRADE_NOT_TEST_ONLY_MODELED"

STAGE_C0 = "C0_UNCONDITIONED_SUBJECT_AND_TIME"
STAGE_C1 = "C1_WORLD_INSTITUTIONAL_ACCESS_CONDITIONING"
STAGE_C2 = "C2_PARENT_COPARENT_HOUSEHOLD_CARE_TIME_CONDITIONING"

RULE_C0 = "C0_NO_WORLD_PREMISE_APPLIED"
RULE_M1 = "M1_INSTITUTIONAL_ACCESS_RULE"
RULE_M1_NONE = "M1_NO_INSTITUTIONAL_RULE_BOUND_TO_ROUTE"
RULE_M2_NONCONTAM = "M2_NONCONTAMINATION_HOUSEHOLD_PREMISE_DOES_NOT_REWRITE_INSTITUTION_RULE"
RULE_M2_CARE = "M2_CARE_TIME_CONSTRAINT_RULE"
RULE_M2_APPR = "M2_LABOR_TIME_TRADEOFF_RULE"
RULE_M2_PRESSURE = "M2_HOUSEHOLD_CARE_PRESSURE_RULE"
RULE_M2_CIVIL = "M2_CIVIL_ROUTE_AVAILABILITY_RULE"


class N10WTypedRefusal(ValueError):
    """Typed refusal at the progressive world-consumer boundary."""

    def __init__(self, code: str, reason: str):
        self.code = code
        self.reason = reason
        super().__init__(f"{code}: {reason}")


@dataclass(frozen=True)
class N10WProgressiveRequest:
    query_id: str
    subject_selector: Mapping[str, Any]
    world: ModeledSelectedWorld
    n10e_product: N10EComputedProduct
    claim_grain: str = GRADE_INDIVIDUAL
    requested_outputs: tuple[str, ...] = ("typed_route_support",)
    as_of_year: int = DECLARED_HISTORICAL_YEAR
    request_unit_scope: str = DECLARED_UNIT_SCOPE
    world_grade_claim: str = WORLD_GRADE
    model_use_issuer_ref: Any = None
    impute_missing_probability: str = "NONE"
    interpret_as_observed_temporal_change: bool = False
    invoke_v3_actor: bool = False
    invoke_v2_expression: bool = False
    promote_fixture_current: bool = False
    cross_universe_joint: bool = False
    erase_routes: tuple[str, ...] = ()
    requested_world_uses: tuple[str, ...] = ("CONTEXT",)


def _route_entry(
    *,
    state: str,
    eligibility: str,
    rule_id: str,
    witness_premises: Mapping[str, str],
    stage_id: str,
    route_id: str,
) -> dict[str, Any]:
    return {
        "route_id": route_id,
        "stage_id": stage_id,
        "state": state,
        "eligibility": eligibility,
        "epistemic_label": "MODELED__NOT_OBSERVED__NOT_MEASURED",
        "probability": None,
        "probability_null_reason": PROBABILITY_NULL_REASON,
        "non_response_state": "UNKNOWN_NOT_MEASURED",
        "type_belief_voice_state": "UNKNOWN_NOT_ASSIGNED",
        "personal_experience_state": "UNKNOWN_NOT_ASSIGNED",
        "modeled_rule_id": rule_id,
        "witness_premises": dict(sorted(witness_premises.items())),
        "minority_alternatives_preserved": True,
    }


def _c0_states() -> dict[str, dict[str, Any]]:
    return {
        route: _route_entry(
            state="UNCONDITIONED_LAWFUL_POSSIBILITY",
            eligibility="UNKNOWN_NOT_YET_WORLD_CONDITIONED",
            rule_id=RULE_C0,
            witness_premises={},
            stage_id=STAGE_C0,
            route_id=route,
        )
        for route in ROUTES
    }


def _institutional_outcome(premises: Mapping[str, str]) -> tuple[str, str]:
    seat = premises["education_institution.public_school_seat"]
    fee = premises["education_institution.fee_barrier"]
    admin = premises["education_institution.administrative_access"]
    eligible = seat == "AVAILABLE" and fee == "NOT_PRESENT_IN_MODEL" and admin == "ELIGIBLE"
    blocked = (
        seat == "NOT_ACCESSIBLE_UNDER_TEST_RULE"
        or fee == "PRESENT_IN_MODEL"
        or admin == "BLOCKED"
    )
    if eligible and not blocked:
        return "ELIGIBLE_IN_MODELED_CONTEXT", "ELIGIBLE_IN_MODELED_CONTEXT"
    if blocked and not eligible:
        return "BLOCKED_BY_MODELED_ACCESS_RULE", "BLOCKED_BY_MODELED_ACCESS_RULE"
    raise N10WTypedRefusal(
        "MODELED_RULE_INDETERMINATE",
        "institutional premises are neither eligible nor blocked under the declared modeled rule",
    )


def _c1_states(premises: Mapping[str, str]) -> dict[str, dict[str, Any]]:
    states = _c0_states()
    inst = {k: premises[k] for k in INSTITUTIONAL_KEYS}
    state, eligibility = _institutional_outcome(premises)
    states["formal_schooling"] = _route_entry(
        state=state,
        eligibility=eligibility,
        rule_id=RULE_M1,
        witness_premises=inst,
        stage_id=STAGE_C1,
        route_id="formal_schooling",
    )
    for route in ROUTES:
        if route == "formal_schooling":
            continue
        entry = states[route]
        states[route] = _route_entry(
            state=entry["state"],
            eligibility=entry["eligibility"],
            rule_id=RULE_M1_NONE,
            witness_premises={},
            stage_id=STAGE_C1,
            route_id=route,
        )
    return states


def _c2_states(premises: Mapping[str, str]) -> dict[str, dict[str, Any]]:
    states = _c1_states(premises)
    care = {k: premises[k] for k in HOUSEHOLD_CARE_KEYS}
    care_time = {k: premises[k] for k in CARE_TIME_KEYS}
    civil = {k: premises[k] for k in ("civil_routes.mutual_aid",)}

    fs = states["formal_schooling"]
    states["formal_schooling"] = _route_entry(
        state=fs["state"],
        eligibility=fs["eligibility"],
        rule_id=RULE_M2_NONCONTAM,
        witness_premises={},
        stage_id=STAGE_C2,
        route_id="formal_schooling",
    )

    if (
        premises["household_care.daily_time_obligation"] == "HIGH_IN_MODEL"
        or premises["civil_routes.peer_nonformal_study"] == "AVAILABLE_UNDER_CONSTRAINT"
    ):
        nf_state = "POSSIBLE_BUT_TIME_CONSTRAINED"
    else:
        nf_state = "POSSIBLE"
    states["nonformal_peer_study"] = _route_entry(
        state=nf_state,
        eligibility=nf_state,
        rule_id=RULE_M2_CARE,
        witness_premises={**care, "civil_routes.peer_nonformal_study": premises["civil_routes.peer_nonformal_study"]},
        stage_id=STAGE_C2,
        route_id="nonformal_peer_study",
    )

    if premises["labor.paid_apprenticeship"] != "CONDITIONAL":
        raise N10WTypedRefusal(
            "MODELED_RULE_INDETERMINATE",
            "labor.paid_apprenticeship premise is outside the declared modeled rule table",
        )
    if (
        premises["labor.time_cost"] == "HIGH"
        or premises["household_care.daily_time_obligation"] == "HIGH_IN_MODEL"
    ):
        ap_state = "CONDITIONAL_WITH_HIGHER_TIME_TRADEOFF"
    else:
        ap_state = "CONDITIONAL_TIME_AND_OPPORTUNITY"
    states["paid_apprenticeship"] = _route_entry(
        state=ap_state,
        eligibility=ap_state,
        rule_id=RULE_M2_APPR,
        witness_premises={**care, "labor.time_cost": premises["labor.time_cost"]},
        stage_id=STAGE_C2,
        route_id="paid_apprenticeship",
    )

    if premises["household_care.daily_time_obligation"] == "HIGH_IN_MODEL":
        fc_state = "PRESSURE_APPLICABLE_NOT_ACTUAL_EVENT"
    else:
        fc_state = "POSSIBLE_NOT_IMPOSED"
    states["family_care_work"] = _route_entry(
        state=fc_state,
        eligibility=fc_state,
        rule_id=RULE_M2_PRESSURE,
        witness_premises=care,
        stage_id=STAGE_C2,
        route_id="family_care_work",
    )

    if premises["civil_routes.mutual_aid"] == "AVAILABLE":
        ma_state = "POSSIBLE"
    else:
        ma_state = "POSSIBLE_BUT_NOT_MODELED_AVAILABLE"
    states["mutual_aid_participation"] = _route_entry(
        state=ma_state,
        eligibility=ma_state,
        rule_id=RULE_M2_CIVIL,
        witness_premises=civil,
        stage_id=STAGE_C2,
        route_id="mutual_aid_participation",
    )
    return states


def derive_stage_states(premises: Mapping[str, str]) -> dict[str, dict[str, dict[str, Any]]]:
    """Pure modeled-rule derivation: C0 -> C1 -> C2 over declared premise values."""

    missing = [k for k in WORLD_FACT_KEYS if k not in premises]
    if missing:
        raise N10WTypedRefusal("MODELED_RULE_INDETERMINATE", f"missing premises: {missing!r}")
    return {
        STAGE_C0: _c0_states(),
        STAGE_C1: _c1_states(premises),
        STAGE_C2: _c2_states(premises),
    }


def _stage_witness(stage_id: str, premises: Mapping[str, str], keys: tuple[str, ...], subject: Mapping[str, Any]) -> Mapping[str, Any]:
    material = {
        "stage_id": stage_id,
        "subject_selector_index": subject.get("index"),
        "subject_declared_historical_year": subject.get("declared_historical_year"),
        "subject_age": subject.get("age"),
        "premises": {k: premises[k] for k in keys},
        "binding_mode": "EXPLICIT_MODELED_PREMISE__NO_INFERENCE",
    }
    return {
        "conditioner_witness_id": f"W10CW:{semantic_hash(material)}",
        "conditioner_witness_material": material,
    }


def _scan_forbidden_inference(material: Any) -> str | None:
    text = canonicalize(material)
    upper = repr(text).upper()
    for token in FORBIDDEN_INFERENCE_TOKENS:
        if token in upper:
            return token
    return None


def _hostile_gates(request: N10WProgressiveRequest) -> None:
    if request.world_grade_claim != WORLD_GRADE:
        raise N10WTypedRefusal(
            REFUSAL_H01,
            "world grade claim is not the TEST_ONLY modeled grade; a modeled world may not "
            "be promoted to observed/real authority",
        )
    forbidden_outputs = sorted(set(request.requested_outputs) & FORBIDDEN_REQUESTED_OUTPUTS)
    if forbidden_outputs:
        raise N10WTypedRefusal(
            REFUSAL_H02,
            f"requested outputs assign psyche/type/voice/biography directly: {forbidden_outputs!r}",
        )
    if request.cross_universe_joint or request.claim_grain == GRADE_DYAD:
        if request.cross_universe_joint:
            raise N10WTypedRefusal(
                REFUSAL_H03,
                "cross-universe respondent/household joint multiplication is unlicensed",
            )
    if request.impute_missing_probability != "NONE":
        raise N10WTypedRefusal(
            REFUSAL_H04,
            "UNKNOWN/UNDERPOWERED route probabilities may not be replaced by zero or exact "
            "values without an operative model-use issuer",
        )
    if request.interpret_as_observed_temporal_change:
        raise N10WTypedRefusal(
            REFUSAL_H05,
            "two modeled context variants are not issued observed structural/temporal change",
        )
    if request.model_use_issuer_ref is not None or request.promote_fixture_current:
        raise N10WTypedRefusal(
            REFUSAL_H07,
            "fixture world has no currentness/model-use issuer to adopt; prose cannot issue one",
        )
    if request.invoke_v3_actor or request.invoke_v2_expression:
        raise N10WTypedRefusal(
            REFUSAL_H08,
            "PRE-V3 evaluation may not invoke V3 actor runtime or V2 expressive renderer",
        )
    if request.erase_routes:
        raise N10WTypedRefusal(
            REFUSAL_H09,
            f"minority/alternative route erasure is forbidden: {sorted(request.erase_routes)!r}",
        )
    if request.as_of_year != DECLARED_HISTORICAL_YEAR:
        raise N10WTypedRefusal(
            REFUSAL_YEAR,
            f"as_of year {request.as_of_year} does not match the declared original year "
            f"{DECLARED_HISTORICAL_YEAR}",
        )
    if request.request_unit_scope != DECLARED_UNIT_SCOPE:
        raise N10WTypedRefusal(
            REFUSAL_UNIT,
            "requested unit/scope does not match the declared original synthetic unit scope",
        )
    subject_year = request.subject_selector.get("declared_historical_year")
    if subject_year != DECLARED_HISTORICAL_YEAR:
        raise N10WTypedRefusal(
            REFUSAL_YEAR,
            f"subject selector declared year {subject_year!r} does not match the original "
            f"declared year {DECLARED_HISTORICAL_YEAR}",
        )
    granted = {"CONTEXT"}
    if not set(request.requested_world_uses) <= granted:
        raise N10WTypedRefusal(
            REFUSAL_SCOPE,
            f"requested world uses {sorted(request.requested_world_uses)!r} exceed the granted "
            f"CONTEXT-only modeled-world scope {sorted(granted)!r}; revoked/never-granted scope "
            "refuses",
        )
    world = request.world
    if world.spec.declared_historical_year != DECLARED_HISTORICAL_YEAR:
        raise N10WTypedRefusal(REFUSAL_YEAR, "world snapshot year is not the declared original year")
    if world.spec.declared_unit_scope != DECLARED_UNIT_SCOPE:
        raise N10WTypedRefusal(REFUSAL_UNIT, "world snapshot unit scope is not the declared original unit")
    if world.resolution.receipt.result_state != "RESOLUTION_COMPLETE":
        raise N10WTypedRefusal(
            REFUSAL_SELECTION,
            f"selected-world resolution state is {world.resolution.receipt.result_state!r}",
        )
    if world.currentness.state.value != "CURRENT":
        raise N10WTypedRefusal(
            REFUSAL_CURRENTNESS,
            f"selected-world structural currentness is {world.currentness.state.value!r}; "
            "stale/invalid worlds may not be served as selected truth",
        )
    leaked = _scan_forbidden_inference(
        {
            "requested_outputs": request.requested_outputs,
            "subject_selector": request.subject_selector,
        }
    )
    if leaked:
        raise N10WTypedRefusal(
            REFUSAL_H02,
            f"request carries a forbidden psyche/type/voice/biography inference token: {leaked!r}",
        )


@dataclass(frozen=True)
class N10WProgressiveReceipt:
    receipt_schema: str
    adapter_contract_id: str
    adapter_grade: str
    consumer_id: str
    query_id: str
    request_fingerprint: str
    subject_selector: Mapping[str, Any]
    world_identity: Mapping[str, Any]
    n10e_lane: Mapping[str, Any]
    stages: tuple[Mapping[str, Any], ...]
    declared_affordance_eligibility_states: Mapping[str, str]
    preserved_alternative_route_ids: tuple[str, ...]
    unknowns: Mapping[str, str]
    dyad_firewall: Mapping[str, Any]
    actor_firewall: Mapping[str, Any]
    world_dependency_refs: Mapping[str, Any]
    claim_grain: str
    as_of: int
    receipt_hash: str = field(default="", init=False)

    def material(self) -> Mapping[str, Any]:
        return {
            "schema": self.receipt_schema,
            "adapter_contract_id": self.adapter_contract_id,
            "adapter_grade": self.adapter_grade,
            "consumer_id": self.consumer_id,
            "query_id": self.query_id,
            "request_fingerprint": self.request_fingerprint,
            "subject_selector": canonicalize(self.subject_selector),
            "world_identity": canonicalize(self.world_identity),
            "n10e_lane": canonicalize(self.n10e_lane),
            "stages": [canonicalize(s) for s in self.stages],
            "declared_affordance_eligibility_states": dict(
                sorted(self.declared_affordance_eligibility_states.items())
            ),
            "preserved_alternative_route_ids": list(self.preserved_alternative_route_ids),
            "unknowns": dict(sorted(self.unknowns.items())),
            "dyad_firewall": canonicalize(self.dyad_firewall),
            "actor_firewall": canonicalize(self.actor_firewall),
            "world_dependency_refs": canonicalize(self.world_dependency_refs),
            "claim_grain": self.claim_grain,
            "as_of": self.as_of,
            "epistemic_ceiling": [
                "TEST_ONLY_MODELED_WORLD__NOT_N9_OPERATIVE_CURRENT",
                "COMPUTED_N10E_OWN_GRAIN__NOT_ROUTE_PROBABILITY",
                "NO_ACTOR__NO_V3__NO_V2__NO_MODEL_USE",
                "NO_PERSONA_QUALITY_MEASUREMENT",
            ],
        }

    @property
    def replay_hash(self) -> str:
        return semantic_hash(self.material())


def evaluate_progressive_world_conditioning(
    request: N10WProgressiveRequest,
) -> N10WProgressiveReceipt:
    """Two-step progressive N10W consumption over world + computed N10E evidence."""

    _hostile_gates(request)
    world = request.world
    n10e = request.n10e_product

    premises = dict(world.spec.premise_states)
    stages_raw = derive_stage_states(premises)

    witness_c0 = _stage_witness(STAGE_C0, premises, (), request.subject_selector)
    witness_c1 = _stage_witness(STAGE_C1, premises, INSTITUTIONAL_KEYS, request.subject_selector)
    witness_c2 = _stage_witness(
        STAGE_C2, premises, HOUSEHOLD_CARE_KEYS + CARE_TIME_KEYS + ("civil_routes.mutual_aid",), request.subject_selector
    )
    witnesses = {STAGE_C0: witness_c0, STAGE_C1: witness_c1, STAGE_C2: witness_c2}

    stages: list[Mapping[str, Any]] = []
    for stage_id in (STAGE_C0, STAGE_C1, STAGE_C2):
        stages.append(
            {
                "stage_id": stage_id,
                **witnesses[stage_id],
                "typed_route_support": {
                    route: stages_raw[stage_id][route] for route in ROUTES
                },
                "n10e_empirical_lane_bound": True,
                "route_probability_merging": "FORBIDDEN_CROSS_GRAIN",
            }
        )

    dyad_claim_state = (
        "REFUSED_NO_HOUSEHOLD_SAMPLING_UNIT_AUTHORITY"
        if request.claim_grain == GRADE_DYAD
        else "NOT_REQUESTED__INDIVIDUAL_GRAIN_ONLY"
    )

    receipt = N10WProgressiveReceipt(
        receipt_schema=RECEIPT_SCHEMA,
        adapter_contract_id=ADAPTER_CONTRACT_ID,
        adapter_grade=ADAPTER_GRADE,
        consumer_id=CONSUMER_ID,
        query_id=request.query_id,
        request_fingerprint=semantic_hash(
            {
                "query_id": request.query_id,
                "subject": canonicalize(request.subject_selector),
                "claim_grain": request.claim_grain,
                "requested_outputs": list(request.requested_outputs),
                "as_of_year": request.as_of_year,
                "request_unit_scope": request.request_unit_scope,
                "world_spec_hash": world.spec.spec_hash,
                "n10e_lane_hash": n10e.lane_hash,
            }
        ),
        subject_selector=request.subject_selector,
        world_identity=world.identity(),
        n10e_lane=n10e.lane_material(),
        stages=tuple(stages),
        declared_affordance_eligibility_states={
            route: stages_raw[STAGE_C2][route]["eligibility"] for route in ROUTES
        },
        preserved_alternative_route_ids=tuple(ROUTES),
        unknowns={
            "enneagram_type": "UNKNOWN_NOT_ASSIGNED",
            "personality": "UNKNOWN_NOT_ASSIGNED",
            "beliefs": "UNKNOWN_NOT_ASSIGNED",
            "personal_experience": "UNKNOWN_NOT_ASSIGNED",
            "voice": "NOT_APPLICABLE_PRE_V3",
            "psychological_state": "UNKNOWN_NOT_ASSIGNED",
            "non_response": "UNKNOWN_NOT_MEASURED",
            "route_probabilities": "NULL_NO_MODEL_USE_ISSUER",
            "persona_quality_effect": "TEST_HYPOTHESIS_NOT_MEASURED",
        },
        dyad_firewall={
            "requested_claim_grain": request.claim_grain,
            "dyad_claim_state": dyad_claim_state,
            "dyad_sampling_unit_authority": "ABSENT",
            "household_unit_semantics": "STRUCTURAL_PREMISE_ONLY__NO_GENERATED_PARENT__NO_DYAD_JOINT",
            "individual_possibility_state": "PRODUCED_RETAINED",
            "dyad_block_must_not_block_individual": True,
        },
        actor_firewall={
            "actor_executions": 0,
            "v3_invoked": False,
            "v2_invoked": False,
            "model_calls": 0,
            "expressive_generator_invoked": False,
            "state": "ACTOR_OFF__PRE_V3_ONLY",
        },
        world_dependency_refs={
            "repository_ref": world.repository.ref.as_dict(),
            "context_query_id": world.query.query_id,
            "resolution_receipt_ref": world.resolution.receipt.ref.as_dict(),
            "selection_record_refs": [
                s.ref.as_dict() for s in world.resolution.selection_records
            ],
            "rsc_ref": world.rsc.ref.as_dict(),
            "currentness_receipt_ref": world.currentness.ref.as_dict(),
            "currentness_state": world.currentness.state.value,
            "validation_receipt_ref": world.validation_receipt.ref.as_dict(),
            "world_replay_hash": world.replay_hash,
            "world_fact_digest": semantic_hash(
                {k: canonicalize(world.fact_payloads[k]) for k in sorted(WORLD_FACT_KEYS)}
            ),
        },
        claim_grain=request.claim_grain,
        as_of=request.as_of_year,
    )
    leaked = _scan_forbidden_inference(
        {
            "route_claims": {
                route: {
                    "state": stages_raw[STAGE_C2][route]["state"],
                    "eligibility": stages_raw[STAGE_C2][route]["eligibility"],
                    "witness_premises": stages_raw[STAGE_C2][route]["witness_premises"],
                }
                for route in ROUTES
            },
            "dyad_firewall": receipt.dyad_firewall,
            "actor_firewall": receipt.actor_firewall,
        }
    )
    if leaked:
        raise N10WTypedRefusal(
            REFUSAL_H02,
            f"emitted receipt contains a forbidden psyche/type/voice/biography token: {leaked!r}",
        )
    object.__setattr__(receipt, "receipt_hash", receipt.replay_hash)
    return receipt


def compute_contrast_pair(
    receipt_a: N10WProgressiveReceipt, receipt_b: N10WProgressiveReceipt
) -> Mapping[str, Any]:
    """Scientifically declared A/B contrast: exactly one eligibility-route change."""

    stages_a = {s["stage_id"]: s for s in receipt_a.stages}
    stages_b = {s["stage_id"]: s for s in receipt_b.stages}
    final_a = stages_a[STAGE_C2]["typed_route_support"]
    final_b = stages_b[STAGE_C2]["typed_route_support"]

    eligibility_changes: list[dict[str, Any]] = []
    state_changes: list[dict[str, Any]] = []
    for route in ROUTES:
        a_state = final_a[route]["state"]
        b_state = final_b[route]["state"]
        a_elig = final_a[route]["eligibility"]
        b_elig = final_b[route]["eligibility"]
        if a_elig != b_elig:
            eligibility_changes.append(
                {
                    "route_id": route,
                    "A_eligibility": a_elig,
                    "B_eligibility": b_elig,
                    "A_state": a_state,
                    "B_state": b_state,
                    "oracle": (
                        "DIFFERENT_DUE_TO_ADMINISTRATIVE_AND_FEE_RULE"
                        if route == "formal_schooling"
                        else "CONSTRAINT_GRADE_CHANGE_NOT_ELIGIBILITY_REMOVAL"
                    ),
                }
            )
        if a_state != b_state:
            state_changes.append(
                {
                    "route_id": route,
                    "A_state": a_state,
                    "B_state": b_state,
                    "route_presence_preserved_in_both": True,
                }
            )

    declared = [c for c in eligibility_changes if c["oracle"] == "DIFFERENT_DUE_TO_ADMINISTRATIVE_AND_FEE_RULE"]
    return {
        "declared_affordance_eligibility_route_change_count": len(declared),
        "declared_affordance_route_change": declared[0] if len(declared) == 1 else declared,
        "constraint_grade_changes": [c for c in state_changes if c["route_id"] != "formal_schooling"],
        "all_state_changes": state_changes,
        "minority_path_retention": {
            "routes_present_A": len(final_a),
            "routes_present_B": len(final_b),
            "retained_fraction_exact": [len(final_b), len(final_a)],
            "erased_routes": [],
        },
        "unmeasured_probability_fraction_exact": [len(ROUTES), len(ROUTES)],
        "actor_or_stereotype_leak_count": 0,
        "persona_quality_effect": "TEST_HYPOTHESIS_NOT_MEASURED",
    }


def selectivity_probe(
    *,
    base_states: Mapping[str, str],
    variant_states: Mapping[str, str],
    changed_keys: tuple[str, ...],
    stage_id: str,
) -> Mapping[str, Any]:
    """H10: only routes bound to the changed premise family may move."""

    base = derive_stage_states(base_states)[stage_id]
    variant = derive_stage_states(variant_states)[stage_id]
    changed_routes = [
        route
        for route in ROUTES
        if base[route]["state"] != variant[route]["state"]
        or base[route]["eligibility"] != variant[route]["eligibility"]
    ]
    institutional_change = any(k.startswith("education_institution.") for k in changed_keys)
    noninstitutional_change = any(
        not k.startswith("education_institution.") for k in changed_keys
    )
    contamination: list[str] = []
    if institutional_change:
        contamination.extend(r for r in changed_routes if r != "formal_schooling")
    if noninstitutional_change:
        contamination.extend(r for r in changed_routes if r == "formal_schooling")
    return {
        "changed_premise_keys": list(changed_keys),
        "stage_id": stage_id,
        "changed_routes": changed_routes,
        "contamination": sorted(set(contamination)),
        "oracle": (
            "REJECT_NONLOCAL_COUNTERFACTUAL_CONTAMINATION"
            if contamination
            else "NO_NONLOCAL_CONTAMINATION_DETECTED"
        ),
        "all_pass": not contamination,
    }


__all__ = [
    "RECEIPT_SCHEMA",
    "ADAPTER_CONTRACT_ID",
    "ADAPTER_GRADE",
    "CONSUMER_ID",
    "ROUTES",
    "PROBABILITY_NULL_REASON",
    "FORBIDDEN_REQUESTED_OUTPUTS",
    "GRADE_INDIVIDUAL",
    "GRADE_DYAD",
    "REFUSAL_H01",
    "REFUSAL_H02",
    "REFUSAL_H03",
    "REFUSAL_H04",
    "REFUSAL_H05",
    "REFUSAL_H07",
    "REFUSAL_H08",
    "REFUSAL_H09",
    "REFUSAL_UNIT",
    "REFUSAL_YEAR",
    "REFUSAL_SCOPE",
    "REFUSAL_CURRENTNESS",
    "REFUSAL_SELECTION",
    "STAGE_C0",
    "STAGE_C1",
    "STAGE_C2",
    "N10WTypedRefusal",
    "N10WProgressiveRequest",
    "N10WProgressiveReceipt",
    "derive_stage_states",
    "evaluate_progressive_world_conditioning",
    "compute_contrast_pair",
    "selectivity_probe",
]
