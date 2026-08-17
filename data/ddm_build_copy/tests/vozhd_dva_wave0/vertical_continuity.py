from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Mapping

STAGES = ("v553", "v554", "v555", "v556", "v557", "v558")
FIXTURE_CONTRACT_VERSION = "vozhd_dva_wave0_vertical_fixture_v1"
SLICE_IDS = {
    "VS1": "temporal_persistence_drift_rupture",
    "VS2": "contradictory_inter_strata_pressure",
    "VS3": "mediation_buffering_amplification",
    "VS4": "pressureflow_attractor_prerequisites",
    "VS5": "uncertainty_absence_noncomparability_forbidden_inference",
}
PRODUCER_OBLIGATIONS = {
    "v553": "Preserve typed temporal observations, pressure identity, uncertainty, absence/noncomparability, and provenance without producing personhood.",
    "v554": "Translate V553 structure into bounded seed affordances without collapsing pressure, contradiction, epistemic, temporal, or authority identities.",
    "v555": "Expose mediation routes plus typed buffering/amplification conditions while retaining the pressure/provenance identities they mediate; no biography or psyche facts.",
    "v556": "Expose pressure-flow routes and attractor prerequisites derived through mediation while retaining competing routes, condition effects, uncertainty, and provenance; no finished personality type.",
    "v557": "Carry the audited semantic graph required by rendering without converting structural evidence into voice, dialogue, autobiography, psyche, or persona facts.",
    "v558": "Expose a runtime-input gate preserving the lawful V553-V557 semantic graph and blockers/epistemic states for a future V3 consumer, while remaining non-persona and non-rendering.",
}
CURRENT_PRODUCTION_COVERAGE = {
    "VS1": {"status": "CURRENT_GAP", "first_gap": "v554->v555", "reason": "V553 has typed temporal keys/deltas/gaps/rupture candidates, but V555 does not preserve those temporal relation/key identities through V558.", "future_producer_obligation": PRODUCER_OBLIGATIONS["v555"]},
    "VS2": {"status": "CURRENT_GAP", "first_gap": "v554->v555", "reason": "V554 can carry contradiction IDs, but V555 reduces downstream mediation to seed IDs and unresolved slots, so competing pressure identities are not guaranteed through V558.", "future_producer_obligation": PRODUCER_OBLIGATIONS["v555"]},
    "VS3": {"status": "CURRENT_GAP", "first_gap": "v555", "reason": "Current V555 has mediation topology but no typed buffering/amplification condition/effect contract for V556.", "future_producer_obligation": PRODUCER_OBLIGATIONS["v555"]},
    "VS4": {"status": "CURRENT_GAP", "first_gap": "v556->v557", "reason": "Current V556 has generic candidate route axes/attractor requirements, not stable route identity tied to mediated pressures through V557/V558.", "future_producer_obligation": PRODUCER_OBLIGATIONS["v556"]},
    "VS5": {"status": "CURRENT_GAP", "first_gap": "v554->v558", "reason": "Absence/prohibition are explicit upstream and runtime leakage is blocked downstream, but uncertainty/noncomparability/provenance are not guaranteed as one semantic chain through V558.", "future_producer_obligation": PRODUCER_OBLIGATIONS["v558"]},
}
FORBIDDEN_DIRECT_OUTPUT_KEYS = frozenset({
    "biography", "autobiography", "persona", "persona_fact", "psyche", "psyche_fact",
    "dialogue", "voice", "memory", "parent_story", "household_story",
    "enneagram_type", "finished_personality_type",
})
ID_FIELDS = (
    "relation_id", "observation_id", "pressure_id", "condition_id", "mediation_route_id",
    "flow_route_id", "prerequisite_id", "uncertainty_id", "absence_id",
    "noncomparability_id", "authority_id",
)

class SemanticContinuityError(AssertionError):
    pass

class ForbiddenInferenceError(SemanticContinuityError):
    pass

def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)

def _fixture_semantics() -> dict[str, Any]:
    return {
        "temporal_relations": [
            {"relation_id": "rel.persistence.local-solidarity", "trajectory_kind": "PERSISTENT",
             "observations": [
                 {"observation_id": "obs.persist.w1", "wave_id": "W1", "year": 2000, "value": 0.60},
                 {"observation_id": "obs.persist.w2", "wave_id": "W2", "year": 2005, "value": 0.62},
                 {"observation_id": "obs.persist.w3", "wave_id": "W3", "year": 2010, "value": 0.61}],
             "authority_ids": ["authority.temporal.reference"]},
            {"relation_id": "rel.drift.institutional-distance", "trajectory_kind": "DRIFT",
             "observations": [
                 {"observation_id": "obs.drift.w1", "wave_id": "W1", "year": 2000, "value": 0.20},
                 {"observation_id": "obs.drift.w2", "wave_id": "W2", "year": 2005, "value": 0.34},
                 {"observation_id": "obs.drift.w3", "wave_id": "W3", "year": 2010, "value": 0.49}],
             "authority_ids": ["authority.temporal.reference"]},
            {"relation_id": "rel.rupture.collective-trust", "trajectory_kind": "RUPTURE_CANDIDATE",
             "observations": [
                 {"observation_id": "obs.rupture.w1", "wave_id": "W1", "year": 2000, "value": 0.41},
                 {"observation_id": "obs.rupture.w2", "wave_id": "W2", "year": 2005, "value": 0.38},
                 {"observation_id": "obs.rupture.w3", "wave_id": "W3", "year": 2010, "value": -0.36}],
             "rupture_claim": {"status": "CANDIDATE_ONLY", "external_event_claim_made": False, "interpretation_permission": "STRUCTURAL_SIGNAL_ONLY"},
             "authority_ids": ["authority.temporal.reference"]},
        ],
        "structural_pressures": [
            {"pressure_id": "pressure.local-solidarity", "conflict_set_id": "conflict.household-orientation", "target_axis_id": "axis.household-orientation", "direction": 1, "magnitude": 0.72, "authority_ids": ["authority.structural.reference"]},
            {"pressure_id": "pressure.institutional-discipline", "conflict_set_id": "conflict.household-orientation", "target_axis_id": "axis.household-orientation", "direction": -1, "magnitude": 0.66, "authority_ids": ["authority.structural.reference"]},
        ],
        "mediation_routes": [{
            "mediation_route_id": "mediation.household-route",
            "source_pressure_ids": ["pressure.local-solidarity", "pressure.institutional-discipline"],
            "route_status": "CONDITIONAL_POTENTIAL",
            "conditions": [
                {"condition_id": "condition.buffer.peer-solidarity", "effect_kind": "BUFFER", "effect_on_pressure_id": "pressure.institutional-discipline", "effect_magnitude": 0.30},
                {"condition_id": "condition.amplify.workplace-surveillance", "effect_kind": "AMPLIFY", "effect_on_pressure_id": "pressure.institutional-discipline", "effect_magnitude": 0.25},
            ],
            "authority_ids": ["authority.mediation.reference"],
        }],
        "pressureflow_routes": [
            {"flow_route_id": "flow.household.deflection", "source_mediation_route_id": "mediation.household-route", "source_pressure_ids": ["pressure.local-solidarity", "pressure.institutional-discipline"], "route_kind": "DEFLECTION_CANDIDATE", "requires_condition_ids": ["condition.buffer.peer-solidarity"], "authority_ids": ["authority.flow.reference"]},
            {"flow_route_id": "flow.household.reinforcement", "source_mediation_route_id": "mediation.household-route", "source_pressure_ids": ["pressure.local-solidarity", "pressure.institutional-discipline"], "route_kind": "REINFORCEMENT_CANDIDATE", "requires_condition_ids": ["condition.amplify.workplace-surveillance"], "authority_ids": ["authority.flow.reference"]},
        ],
        "attractor_prerequisites": [
            {"prerequisite_id": "attractor.prereq.repeated-conflict", "source_flow_route_ids": ["flow.household.deflection", "flow.household.reinforcement"], "status": "PREREQUISITE_ONLY", "finished_type_assignment_allowed": False},
            {"prerequisite_id": "attractor.prereq.feedback-history", "source_flow_route_ids": ["flow.household.deflection", "flow.household.reinforcement"], "status": "PREREQUISITE_ONLY", "finished_type_assignment_allowed": False},
        ],
        "epistemic_boundaries": {
            "uncertainty": [{"uncertainty_id": "uncertainty.pressure-estimate", "state": "UNCERTAIN", "confidence": 0.58, "reason": "bounded uncertainty", "authority_ids": ["authority.epistemic.reference"]}],
            "absence": [{"absence_id": "absence.household-biography", "state": "ABSENT", "numeric_value": None, "must_not_coerce_to_zero": True, "reason": "no biography exists in V553-V558 jurisdiction"}],
            "noncomparability": [{"noncomparability_id": "noncomparability.w1-w3.locality", "state": "NONCOMPARABLE", "numeric_value": None, "must_not_coerce_to_neutral": True, "reason": "locality basis differs without harmonization authority"}],
        },
        "provenance": [
            {"authority_id": "authority.temporal.reference", "epistemic_class": "REFERENCE_TEMPORAL_AUTHORITY"},
            {"authority_id": "authority.structural.reference", "epistemic_class": "REFERENCE_STRUCTURAL_AUTHORITY"},
            {"authority_id": "authority.mediation.reference", "epistemic_class": "REFERENCE_MEDIATION_OBLIGATION"},
            {"authority_id": "authority.flow.reference", "epistemic_class": "REFERENCE_FLOW_OBLIGATION"},
            {"authority_id": "authority.epistemic.reference", "epistemic_class": "REFERENCE_EPISTEMIC_BOUNDARY"},
        ],
    }

def build_reference_fixture() -> dict[str, Any]:
    """Reference mediation/flow semantics are future producer obligations, not claims about current V555/V556."""
    return {
        "fixture_contract_version": FIXTURE_CONTRACT_VERSION,
        "fixture_id": "vozhd-dva-wave0.vertical.r0-05.v1",
        "grain": "one synthetic source-country, three ordered waves, stable semantic IDs",
        "source_identity": {"source": "REFERENCE_SURVEY", "country_code": "ZZ", "waves": ["W1", "W2", "W3"]},
        "semantic_payload": _fixture_semantics(),
        "adversarial_cases": [{
            "case_id": "forbidden.direct-persona-from-structure",
            "source_layers": ["v553", "v554", "v555", "v556"],
            "requested_output": {"enneagram_type": "8", "biography": "invented childhood narrative"},
            "expected_disposition": "FAIL_CLOSED",
            "reason": "structural/temporal evidence cannot directly become finished psyche or biography",
        }],
    }

def build_reference_chain(fixture: Mapping[str, Any] | None = None) -> dict[str, dict[str, Any]]:
    fixture = copy.deepcopy(dict(fixture or build_reference_fixture()))
    chain, previous = {}, "reference_upstream"
    for stage in STAGES:
        chain[stage] = {
            "fixture_contract_version": FIXTURE_CONTRACT_VERSION,
            "fixture_id": fixture["fixture_id"], "stage": stage,
            "packet_kind": "REFERENCE_CONTRACT_FIXTURE_NOT_PRODUCTION_OUTPUT",
            "artifact_shape_status": "PASS", "production_semantic_readiness_claim": False,
            "future_producer_obligation": PRODUCER_OBLIGATIONS[stage],
            "reference_source_stage": previous,
            "semantic_payload": copy.deepcopy(fixture["semantic_payload"]),
            "generated_outputs": {},
        }
        previous = stage
    return chain

def artifact_shape_report(chain: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    errors = []
    for stage in STAGES:
        packet = chain.get(stage)
        if not isinstance(packet, Mapping):
            errors.append(f"missing stage packet: {stage}"); continue
        for key in ("fixture_contract_version", "fixture_id", "stage", "packet_kind", "artifact_shape_status"):
            if key not in packet: errors.append(f"{stage} missing envelope field {key}")
        if packet.get("stage") != stage: errors.append(f"{stage} stage identity mismatch")
        if packet.get("artifact_shape_status") != "PASS": errors.append(f"{stage} artifact shape not PASS")
    return {"ready": not errors, "errors": errors, "level": "artifact_shape"}

def semantic_fingerprint(payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(_canonical_json(payload).encode()).hexdigest()

def _ids_for_key(value: Any, key: str) -> list[str]:
    found = []
    if isinstance(value, Mapping):
        if isinstance(value.get(key), str): found.append(value[key])
        for child in value.values(): found.extend(_ids_for_key(child, key))
    elif isinstance(value, list):
        for child in value: found.extend(_ids_for_key(child, key))
    return found

def _forbidden_keys(value: Any) -> set[str]:
    hits = set()
    if isinstance(value, Mapping):
        for key, child in value.items():
            if str(key).strip().lower() in FORBIDDEN_DIRECT_OUTPUT_KEYS: hits.add(str(key).strip().lower())
            hits.update(_forbidden_keys(child))
    elif isinstance(value, list):
        for child in value: hits.update(_forbidden_keys(child))
    return hits

def assert_stage_jurisdiction(packet: Mapping[str, Any]) -> None:
    hits = _forbidden_keys(packet.get("generated_outputs", {}))
    if hits: raise ForbiddenInferenceError(f"{packet.get('stage', 'unknown')}: forbidden direct personhood output keys: {sorted(hits)}")

def reject_direct_persona_inference(case: Mapping[str, Any]) -> None:
    hits = _forbidden_keys(case.get("requested_output", {}))
    if hits: raise ForbiddenInferenceError(f"fail closed: V553-V558 cannot satisfy direct structural/temporal -> persona inference; forbidden keys={sorted(hits)}")

def _assert_fixture_distinctions(payload: Mapping[str, Any], stage: str) -> None:
    kinds = {r.get("trajectory_kind") for r in payload.get("temporal_relations", [])}
    if kinds != {"PERSISTENT", "DRIFT", "RUPTURE_CANDIDATE"}:
        raise SemanticContinuityError(f"{stage}: temporal distinctions lost")
    conflict = [r for r in payload.get("structural_pressures", []) if r.get("conflict_set_id") == "conflict.household-orientation"]
    if len(conflict) != 2 or {r.get("direction") for r in conflict} != {-1, 1}:
        raise SemanticContinuityError(f"{stage}: contradictory pressures were collapsed or neutralized")
    conditions = [c for r in payload.get("mediation_routes", []) for c in r.get("conditions", [])]
    effects = {c.get("effect_kind") for c in conditions}
    if effects != {"BUFFER", "AMPLIFY"}:
        raise SemanticContinuityError(f"{stage}: mediation buffer/amplify distinction lost: {effects}")
    if {r.get("route_kind") for r in payload.get("pressureflow_routes", [])} != {"DEFLECTION_CANDIDATE", "REINFORCEMENT_CANDIDATE"}:
        raise SemanticContinuityError(f"{stage}: pressure-flow route distinction lost")
    prereqs = payload.get("attractor_prerequisites", [])
    if len(prereqs) < 2 or any(r.get("finished_type_assignment_allowed") is not False for r in prereqs):
        raise SemanticContinuityError(f"{stage}: attractor prerequisites lost or illegally promoted")
    epistemic = payload.get("epistemic_boundaries", {})
    if not epistemic.get("uncertainty") or epistemic["uncertainty"][0].get("state") != "UNCERTAIN":
        raise SemanticContinuityError(f"{stage}: explicit uncertainty lost")
    if not epistemic.get("absence") or epistemic["absence"][0].get("state") != "ABSENT" or epistemic["absence"][0].get("numeric_value") is not None:
        raise SemanticContinuityError(f"{stage}: absence was lost or coerced into a numeric value")
    if not epistemic.get("noncomparability") or epistemic["noncomparability"][0].get("state") != "NONCOMPARABLE" or epistemic["noncomparability"][0].get("numeric_value") is not None:
        raise SemanticContinuityError(f"{stage}: noncomparability was lost or coerced into neutral/zero")
    expected = {"authority.temporal.reference", "authority.structural.reference", "authority.mediation.reference", "authority.flow.reference", "authority.epistemic.reference"}
    missing = expected - set(_ids_for_key(payload, "authority_id"))
    if missing: raise SemanticContinuityError(f"{stage}: provenance/authority identity lost: {sorted(missing)}")

def semantic_continuity_report(chain: Mapping[str, Mapping[str, Any]], fixture: Mapping[str, Any] | None = None) -> dict[str, Any]:
    baseline = dict(fixture or build_reference_fixture())["semantic_payload"]
    fingerprint, errors = semantic_fingerprint(baseline), []
    for stage in STAGES:
        packet = chain.get(stage)
        if not isinstance(packet, Mapping): errors.append(f"missing stage packet: {stage}"); continue
        if not packet.get("future_producer_obligation"): errors.append(f"{stage}: missing future producer obligation")
        payload = packet.get("semantic_payload")
        if not isinstance(payload, Mapping): errors.append(f"{stage}: semantic payload missing"); continue
        try: _assert_fixture_distinctions(payload, stage)
        except SemanticContinuityError as exc: errors.append(str(exc))
        actual = semantic_fingerprint(payload)
        if actual != fingerprint: errors.append(f"{stage}: semantic fingerprint mismatch; information changed/dropped ({fingerprint[:12]} != {actual[:12]})")
        try: assert_stage_jurisdiction(packet)
        except ForbiddenInferenceError as exc: errors.append(str(exc))
    return {"ready": not errors, "errors": errors, "level": "semantic_chain", "reference_contract_only": True, "production_semantic_readiness_claim": False}

def assert_semantic_continuity(chain: Mapping[str, Mapping[str, Any]], fixture: Mapping[str, Any] | None = None) -> None:
    report = semantic_continuity_report(chain, fixture)
    if not report["ready"]: raise SemanticContinuityError("; ".join(report["errors"]))

TEST_CAPABILITY_MAP = {
    "fixture_determinism": {"producer": "reference upstream", "consumer": "all tests"},
    "VS1": {"producer": "V553-V558", "consumer": "future V3", "protects": SLICE_IDS["VS1"]},
    "VS2": {"producer": "V553-V555", "consumer": "V556/V3", "protects": SLICE_IDS["VS2"]},
    "VS3": {"producer": "V555", "consumer": "V556/V3", "protects": SLICE_IDS["VS3"]},
    "VS4": {"producer": "V556", "consumer": "V557/V558/V3", "protects": SLICE_IDS["VS4"]},
    "VS5": {"producer": "V553-V558", "consumer": "future V3", "protects": SLICE_IDS["VS5"]},
    "semantic_loss": {"producer": "V555/V556", "consumer": "CI/V3"},
    "forbidden_inference": {"producer": "V553-V558", "consumer": "runtime/V3"},
}
