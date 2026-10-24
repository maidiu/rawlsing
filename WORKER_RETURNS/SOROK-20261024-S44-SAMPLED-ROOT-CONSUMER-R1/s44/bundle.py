"""Explicit immutable TEST_ONLY source/model bundle for S44 root sampling."""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from .errors import S44Refusal
from .rng import canonical_json, sha256_hex

SCHEMA = "S44_SOURCE_MODEL_BUNDLE@1"
GRADE = "TEST_ONLY_S44_SYNTHETIC_SOURCE_MODEL_NOT_EMPIRICAL"
ROOT_SEED_SOURCE = "EXPLICIT_CALLER_SEED"
A_ID = "TEST_ONLY_BP1_R26V_ACTOR_A"
B_ID = "TEST_ONLY_BP1_R26V_ACTOR_B"
FORBIDDEN_KEYS = frozenset({
    "desired_action", "chosen_action", "response_witness", "biography",
    "finished_life", "personality", "psyche", "future_child",
    "variant", "genesis", "a_repair_long",
})


def _cand(candidate_id: str, value: int, weight: int = 1,
          source_ref: str = "") -> dict:
    return {
        "candidate_id": candidate_id,
        "value": int(value),
        "weight_units": int(weight),
        "source_ref": source_ref or ("TEST_ONLY_S44_CANDIDATE_" + candidate_id.upper()),
    }


def _rule(rule_id: str, stream: str, scope_kind: str, scope_id: str,
          candidates: list[dict], *, registry_hash: str,
          rule_version: str = "1") -> dict:
    return {
        "rule_id": rule_id,
        "rule_version": rule_version,
        "registry_hash": registry_hash,
        "stream": stream,
        "scope_kind": scope_kind,
        "scope_id": scope_id,
        "operation": "WEIGHTED_CANDIDATE_INTEGER",
        "candidate_owner_authority": "TEST_ONLY_S44_ROOT_MODEL",
        "candidates": candidates,
    }


def default_bundle(*, root_seed: str) -> dict:
    registry_hash = sha256_hex({
        "schema": "S44_TEST_MODEL_RULE_REGISTRY@1",
        "version": "1",
        "rule_ids": [
            "S44_A_MATERIAL", "S44_B_MATERIAL", "S44_A_CASH", "S44_B_CASH",
            "S44_A_HOURS", "S44_B_HOURS", "S44_A_BIRTH", "S44_B_BIRTH",
            "S44_JOINT_TIME", "S44_JOINT_PAYMENT", "S44_JOINT_HOURS",
            "S44_JOINT_UNITS", "S44_A_OPTIONAL_DECLINE", "S44_B_EXTRA_REFUSAL",
        ],
        "grade": GRADE,
    })
    rules = {
        "a_material": _rule(
            "S44_A_MATERIAL", "v3.causal.s44.initial.a_material", "ACTOR", A_ID,
            [_cand("a_material_2", 2, 1), _cand("a_material_3", 3, 2),
             _cand("a_material_4", 4, 2), _cand("a_material_5", 5, 1)],
            registry_hash=registry_hash),
        "b_material": _rule(
            "S44_B_MATERIAL", "v3.causal.s44.initial.b_material", "ACTOR", B_ID,
            [_cand("b_material_2", 2, 1), _cand("b_material_3", 3, 2),
             _cand("b_material_4", 4, 2), _cand("b_material_5", 5, 1)],
            registry_hash=registry_hash),
        "a_cash": _rule(
            "S44_A_CASH", "v3.causal.s44.initial.a_cash", "ACTOR", A_ID,
            [_cand("a_cash_18", 18, 1), _cand("a_cash_24", 24, 2),
             _cand("a_cash_30", 30, 2), _cand("a_cash_36", 36, 1)],
            registry_hash=registry_hash),
        "b_cash": _rule(
            "S44_B_CASH", "v3.causal.s44.initial.b_cash", "ACTOR", B_ID,
            [_cand("b_cash_16", 16, 1), _cand("b_cash_22", 22, 2),
             _cand("b_cash_28", 28, 2), _cand("b_cash_34", 34, 1)],
            registry_hash=registry_hash),
        "a_hours": _rule(
            "S44_A_HOURS", "v3.causal.s44.initial.a_hours", "ACTOR", A_ID,
            [_cand("a_hours_20", 20, 1), _cand("a_hours_24", 24, 2),
             _cand("a_hours_28", 28, 2), _cand("a_hours_32", 32, 1)],
            registry_hash=registry_hash),
        "b_hours": _rule(
            "S44_B_HOURS", "v3.causal.s44.initial.b_hours", "ACTOR", B_ID,
            [_cand("b_hours_18", 18, 1), _cand("b_hours_22", 22, 2),
             _cand("b_hours_26", 26, 2), _cand("b_hours_30", 30, 1)],
            registry_hash=registry_hash),
        "a_birth": _rule(
            "S44_A_BIRTH", "v3.causal.s44.initial.a_birth", "ACTOR", A_ID,
            [_cand("a_birth_11", 11, 1), _cand("a_birth_13", 13, 2),
             _cand("a_birth_15", 15, 2), _cand("a_birth_17", 17, 1)],
            registry_hash=registry_hash),
        "b_birth": _rule(
            "S44_B_BIRTH", "v3.causal.s44.initial.b_birth", "ACTOR", B_ID,
            [_cand("b_birth_10", 10, 1), _cand("b_birth_12", 12, 2),
             _cand("b_birth_14", 14, 2), _cand("b_birth_16", 16, 1)],
            registry_hash=registry_hash),
        "joint_time": _rule(
            "S44_JOINT_TIME", "v3.causal.s44.joint.time", "RUN", "S44_ROOT",
            [_cand("joint_time_210", 210, 1), _cand("joint_time_220", 220, 2),
             _cand("joint_time_230", 230, 2), _cand("joint_time_238", 238, 1)],
            registry_hash=registry_hash),
        "joint_payment": _rule(
            "S44_JOINT_PAYMENT", "v3.causal.s44.joint.payment", "RUN", "S44_ROOT",
            [_cand("payment_1", 1, 1), _cand("payment_2", 2, 2),
             _cand("payment_3", 3, 2), _cand("payment_4", 4, 1)],
            registry_hash=registry_hash),
        "joint_hours": _rule(
            "S44_JOINT_HOURS", "v3.causal.s44.joint.hours", "RUN", "S44_ROOT",
            [_cand("task_hours_1", 1, 2), _cand("task_hours_2", 2, 2),
             _cand("task_hours_3", 3, 1)],
            registry_hash=registry_hash),
        "joint_units": _rule(
            "S44_JOINT_UNITS", "v3.causal.s44.joint.units", "RUN", "S44_ROOT",
            [_cand("joint_units_1", 1, 3), _cand("joint_units_2", 2, 1)],
            registry_hash=registry_hash),
    }
    rules["a_optional_decline"] = {
        "rule_id": "S44_A_OPTIONAL_DECLINE",
        "rule_version": "1",
        "registry_hash": registry_hash,
        "stream": "v3.causal.s44.optional.a_decline",
        "scope_kind": "ACTOR",
        "scope_id": A_ID,
        "operation": "BERNOULLI_RATIONAL",
        "condition_on": "a_material",
        "condition_threshold": 3,
        "numerator_if_true": 1,
        "denominator_if_true": 4,
        "numerator_if_false": 3,
        "denominator_if_false": 4,
    }
    rules["b_extra_refusal"] = {
        "rule_id": "S44_B_EXTRA_REFUSAL",
        "rule_version": "1",
        "registry_hash": registry_hash,
        "stream": "v3.causal.s44.optional.b_refusal",
        "scope_kind": "ACTOR",
        "scope_id": B_ID,
        "operation": "BERNOULLI_RATIONAL",
        "condition_on": "a_material",
        "condition_threshold": 3,
        "numerator_if_true": 1,
        "denominator_if_true": 3,
        "numerator_if_false": 2,
        "denominator_if_false": 3,
    }
    body = {
        "schema": SCHEMA,
        "grade": GRADE,
        "native": False,
        "psychology_claim": False,
        "bundle_id": "TEST_ONLY_S44_ROOT_BUNDLE",
        "root_seed": root_seed,
        "root_seed_source": ROOT_SEED_SOURCE,
        "seed_scheme": "V3_CAUSAL_HMAC_SHA256_COUNTER_V1@1.0.0",
        "model_parameters": {
            "grade": "TEST_ONLY_EXPLICIT_SYNTHETIC_PARAMETERS",
            "empirical_claim": False,
            "production_default": False,
            "note": "Explicit invented weights and conditional fractions; not empirical coefficients.",
        },
        "rules": rules,
        "language_evidence": [{
            "evidence_id": "TEST_ONLY_S44_ROOT_FAMILY_REQUEST",
            "intent": "REQUEST_TOOL",
            "text": "¿Puedo usar la herramienta?",
            "concept_id": "concept:request-tool",
            "milieu_id": "family",
            "sense_id": "sense:family-request",
            "relation_label": "CONTESTED",
            "atoms": ["TOOL_REQUEST_WORKSHOP"],
            "language_tag": "es-MX",
            "speaker_actor": "B",
            "counterexample_event_ids": [],
        }, {
            "evidence_id": "TEST_ONLY_S44_ROOT_WORKSHOP_REQUEST",
            "intent": "REQUEST_TOOL",
            "text": "¿Puedo usar la herramienta?",
            "concept_id": "concept:request-tool",
            "milieu_id": "workshop",
            "sense_id": "sense:workshop-request",
            "relation_label": "AFFIRMED",
            "atoms": ["TOOL_REQUEST_WORKSHOP"],
            "language_tag": "es-MX",
            "speaker_actor": "B",
            "counterexample_event_ids": [],
        }],
        "source_bindings": {
            "root_model": "TEST_ONLY_S44_SOURCE_MODEL",
            "s43_base": "3edd631fb6c31751dfd2143ba2faa9fc31561e54",
            "join_e": "7bf2da302996491ddf34b9a039fea47ac982d135",
        },
    }
    return normalize_bundle(body)


def _forbidden(value: Any) -> str | None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str) and key.lower() in FORBIDDEN_KEYS:
                return key
            found = _forbidden(item)
            if found:
                return found
    elif isinstance(value, (list, tuple)):
        for item in value:
            found = _forbidden(item)
            if found:
                return found
    return None


def normalize_bundle(bundle: Mapping[str, Any]) -> dict:
    if not isinstance(bundle, Mapping):
        raise S44Refusal("S44_BUNDLE_NOT_OBJECT")
    body = deepcopy(dict(bundle))
    if body.get("schema") != SCHEMA:
        raise S44Refusal("S44_BUNDLE_SCHEMA_MISMATCH")
    if body.get("native") is not False or body.get("psychology_claim") is not False:
        raise S44Refusal("S44_BUNDLE_NATIVE_OR_PSYCHOLOGY_CLAIM")
    if body.get("root_seed_source") != ROOT_SEED_SOURCE:
        raise S44Refusal("S44_ROOT_SEED_SOURCE_INVALID")
    bad = _forbidden(body)
    if bad:
        raise S44Refusal("S44_BUNDLE_FORBIDDEN_INPUT", bad)
    rules = body.get("rules")
    if not isinstance(rules, Mapping) or not rules:
        raise S44Refusal("S44_RULE_SET_MISSING")
    normalized_rules = {}
    for name, rule in rules.items():
        if not isinstance(rule, Mapping):
            raise S44Refusal("S44_RULE_INVALID", name)
        r = deepcopy(dict(rule))
        for key in ("rule_id", "rule_version", "stream", "scope_kind",
                    "scope_id", "operation", "registry_hash"):
            if not isinstance(r.get(key), str) or not r.get(key):
                raise S44Refusal("S44_RULE_FIELD_MISSING", f"{name}:{key}")
        if r["operation"] == "WEIGHTED_CANDIDATE_INTEGER":
            r["candidates"] = sorted(
                [deepcopy(dict(row)) for row in r.get("candidates") or []],
                key=lambda row: (str(row.get("candidate_id", "")),
                                 canonical_json(row)),
            )
            if not r["candidates"]:
                raise S44Refusal("S44_CANDIDATE_SET_EMPTY", name)
        normalized_rules[name] = r
    body["rules"] = normalized_rules
    body.pop("bundle_hash", None)
    body["bundle_hash"] = sha256_hex(body)
    return body


def effective_probability(bundle: Mapping[str, Any], rule_name: str,
                          predecessor: int) -> tuple[int, int]:
    rule = bundle["rules"][rule_name]
    threshold = int(rule["condition_threshold"])
    if predecessor >= threshold:
        return int(rule["numerator_if_true"]), int(rule["denominator_if_true"])
    return int(rule["numerator_if_false"]), int(rule["denominator_if_false"])


__all__ = [
    "SCHEMA", "GRADE", "ROOT_SEED_SOURCE", "A_ID", "B_ID",
    "default_bundle", "normalize_bundle", "effective_probability",
]
