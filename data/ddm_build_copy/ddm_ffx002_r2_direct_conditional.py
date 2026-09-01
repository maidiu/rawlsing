#!/usr/bin/env python3
"""FFX002-R2 Core-C respondent-level direct conditional redistribution producer.

This is deliberately distinct from ddm_v551_conditional.  V551 conditional
determinicity is a derived-determinicity bridge index; this module estimates a
bounded respondent-level P(D|C), or an explicitly declared strict-subset
backoff, over one frozen common semantic input.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from statistics import NormalDist
from typing import Any, Mapping, Sequence

ARM_ID = "C"
VIEW_FAMILY = "DIRECT_CONDITIONAL_REDISTRIBUTION"
PRODUCER_VERSION = "FFX002_R2_CORE_C_DIRECT_CONDITIONAL_REDISTRIBUTION_R1"
OUTPUT_SCHEMA_VERSION = "FFX002_R2_DIRECT_CONDITIONAL_OUTPUT_R1"
LOSS_RECEIPT_SCHEMA_VERSION = "FFX002_R2_VIEW_LOSS_RECEIPT_R1"
REPLAY_RECEIPT_SCHEMA_VERSION = "FFX002_R2_REPLAY_RECEIPT_R1"
NUMERIC_REPLAY_CONTRACT_VERSION = "FFX002_R2_DIRECT_CONDITIONAL_NUMERIC_R1"
FLOAT_DIGITS = 12

COMMON_MANIFEST_REQUIRED_FIELDS = (
    "manifest_schema_version",
    "current_execution_sha",
    "observation_substrate_ref",
    "respondent_entity_binding_ref",
    "exposure_risk_set_ref",
    "source_scope_ref",
    "source_native_measurement_refs",
    "qimpl_measurement_binding_refs",
    "response_state_semantics_ref",
    "special_state_semantics_ref",
    "ttar_execution_sequence",
    "post_transform_state_manifest",
    "claim_scope_ref",
    "estimand_ref",
    "weight_design_refs",
    "analytic_role_authority_refs",
    "ancestry_disjointness_receipt",
    "unresolved_noncomparable_manifest",
    "source_native_ancestry_ref",
    "loss_profile",
    "holdout_generation_inputs_hash",
    "canonicalization_spec",
    "manifest_hash",
)


class DirectConditionalContractError(ValueError):
    def __init__(self, code: str, detail: str):
        super().__init__(f"{code}: {detail}")
        self.code = code
        self.detail = detail


def _fail(code: str, detail: str) -> None:
    raise DirectConditionalContractError(code, detail)


def _canonical(value: Any) -> str:
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        _fail("DIRECT_CONDITIONAL_NONCANONICAL_VALUE", str(exc))


def _hash(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _pointer(path: tuple[str, ...]) -> str:
    if not path:
        return ""
    return "/" + "/".join(p.replace("~", "~0").replace("/", "~1") for p in path)


def _canon_manifest(value: Any, set_paths: frozenset[str], path: tuple[str, ...] = ()) -> Any:
    if isinstance(value, Mapping):
        return {
            str(k): _canon_manifest(v, set_paths, path + (str(k),))
            for k, v in value.items()
        }
    if isinstance(value, (list, tuple)):
        out = [
            _canon_manifest(v, set_paths, path + (str(i),))
            for i, v in enumerate(value)
        ]
        if _pointer(path) in set_paths:
            out.sort(key=_canonical)
        return out
    return value


def recompute_common_manifest_hash(common_manifest: Mapping[str, Any]) -> str:
    if not isinstance(common_manifest, Mapping):
        _fail("COMMON_INPUT_MISSING_HARD_FIELD", "common_manifest must be an object")
    missing = [f for f in COMMON_MANIFEST_REQUIRED_FIELDS if f not in common_manifest]
    if missing:
        _fail("COMMON_INPUT_MISSING_HARD_FIELD", "missing fields: " + ",".join(missing))
    if not isinstance(common_manifest.get("manifest_hash"), str) or not common_manifest["manifest_hash"]:
        _fail("COMMON_INPUT_MISSING_HARD_FIELD", "manifest_hash must be a nonempty string")

    set_paths: frozenset[str] = frozenset()
    spec = common_manifest.get("canonicalization_spec")
    if isinstance(spec, Mapping):
        alg = str(spec.get("hash_algorithm", "sha256")).lower().replace("-", "")
        if alg != "sha256":
            _fail("COMMON_INPUT_UNSUPPORTED_HASH_ALGORITHM", f"unsupported hash algorithm {alg!r}")
        raw_paths = spec.get("set_valued_paths", ())
        if raw_paths is None:
            raw_paths = ()
        if isinstance(raw_paths, (str, bytes)) or not isinstance(raw_paths, Sequence):
            _fail("COMMON_INPUT_INVALID_CANONICALIZATION_SPEC", "set_valued_paths must be an array")
        parsed = []
        for item in raw_paths:
            if not isinstance(item, str) or (item and not item.startswith("/")):
                _fail("COMMON_INPUT_INVALID_CANONICALIZATION_SPEC", "invalid JSON pointer")
            parsed.append(item)
        set_paths = frozenset(parsed)

    payload = {k: v for k, v in common_manifest.items() if k != "manifest_hash"}
    return _hash(_canon_manifest(payload, set_paths))


def attest_common_manifest(common_manifest: Mapping[str, Any]) -> dict[str, Any]:
    recomputed = recompute_common_manifest_hash(common_manifest)
    received = common_manifest["manifest_hash"]
    if received != recomputed:
        _fail(
            "EXPERIMENT_INVALID__POSTFORK_SEMANTIC_DIVERGENCE",
            f"received manifest hash {received} != recomputed {recomputed}",
        )
    return {
        "arm_id": ARM_ID,
        "view_family": VIEW_FAMILY,
        "received_manifest_hash": received,
        "recomputed_manifest_hash": recomputed,
        "attestation_status": "ATTESTED_EQUAL",
    }


def _mapping(value: Any, code: str, name: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        _fail(code, f"{name} must be an object")
    return value


def _sequence(value: Any, code: str, name: str) -> Sequence[Any]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        _fail(code, f"{name} must be an array")
    return value


def _id(value: Any, code: str, name: str) -> str:
    if not isinstance(value, str) or not value:
        _fail(code, f"{name} must be a nonempty string")
    return value


def _same(a: Any, b: Any) -> bool:
    return _canonical(a) == _canonical(b)


def _round(value: float | None) -> float | None:
    if value is None:
        return None
    return round(float(value), FLOAT_DIGITS)


def _states(
    common_manifest: Mapping[str, Any],
    frozen_state_registry: Mapping[str, Any],
) -> dict[str, tuple[str, ...]]:
    registry = _mapping(
        frozen_state_registry,
        "DIRECT_CONDITIONAL_STATE_REGISTRY_INVALID",
        "frozen_state_registry",
    )
    if not _same(
        registry.get("post_transform_state_manifest_ref"),
        common_manifest["post_transform_state_manifest"],
    ):
        _fail(
            "DIRECT_CONDITIONAL_STATE_REGISTRY_DIVERGENCE",
            "registry is not bound to the frozen post_transform_state_manifest",
        )
    raw = _mapping(
        registry.get("states_by_measurement"),
        "DIRECT_CONDITIONAL_STATE_REGISTRY_INVALID",
        "states_by_measurement",
    )
    out: dict[str, tuple[str, ...]] = {}
    for measurement_id, values in raw.items():
        mid = _id(measurement_id, "DIRECT_CONDITIONAL_STATE_REGISTRY_INVALID", "measurement_id")
        seq = _sequence(values, "DIRECT_CONDITIONAL_STATE_REGISTRY_INVALID", mid)
        seen: set[str] = set()
        state_ids: list[str] = []
        for value in seq:
            sid = _id(value, "DIRECT_CONDITIONAL_STATE_REGISTRY_INVALID", f"{mid} state")
            if sid in seen:
                _fail("DIRECT_CONDITIONAL_STATE_REGISTRY_INVALID", f"duplicate state {sid!r} for {mid!r}")
            seen.add(sid)
            state_ids.append(sid)
        if not state_ids:
            _fail("DIRECT_CONDITIONAL_STATE_REGISTRY_INVALID", f"{mid!r} has no frozen states")
        out[mid] = tuple(state_ids)
    if not out:
        _fail("DIRECT_CONDITIONAL_STATE_REGISTRY_INVALID", "states_by_measurement is empty")
    return out


def _condition_states(
    condition: Mapping[str, Any],
    state_registry: Mapping[str, tuple[str, ...]],
) -> tuple[str, tuple[tuple[str, str], ...]]:
    condition_id = _id(
        condition.get("condition_id"),
        "DIRECT_CONDITIONAL_CONDITION_IDENTITY_INVALID",
        "condition_id",
    )
    raw_states = _sequence(
        condition.get("states"),
        "DIRECT_CONDITIONAL_CONDITION_IDENTITY_INVALID",
        "condition.states",
    )
    if not raw_states:
        _fail("DIRECT_CONDITIONAL_CONDITION_IDENTITY_INVALID", "condition.states cannot be empty")
    seen: set[str] = set()
    out: list[tuple[str, str]] = []
    for item in raw_states:
        row = _mapping(item, "DIRECT_CONDITIONAL_CONDITION_IDENTITY_INVALID", "condition state")
        mid = _id(row.get("measurement_id"), "DIRECT_CONDITIONAL_CONDITION_IDENTITY_INVALID", "measurement_id")
        sid = _id(row.get("state_id"), "DIRECT_CONDITIONAL_CONDITION_IDENTITY_INVALID", "state_id")
        if mid in seen:
            _fail("DIRECT_CONDITIONAL_CONDITION_IDENTITY_INVALID", f"duplicate condition measurement {mid!r}")
        if mid not in state_registry or sid not in state_registry[mid]:
            _fail("DIRECT_CONDITIONAL_UNKNOWN_FROZEN_STATE", f"unknown condition state {mid}={sid}")
        seen.add(mid)
        out.append((mid, sid))
    return condition_id, tuple(out)


def _outcome(
    outcome: Mapping[str, Any],
    state_registry: Mapping[str, tuple[str, ...]],
) -> tuple[str, str, tuple[str, ...]]:
    outcome_id = _id(outcome.get("outcome_id"), "DIRECT_CONDITIONAL_OUTCOME_IDENTITY_INVALID", "outcome_id")
    mid = _id(outcome.get("measurement_id"), "DIRECT_CONDITIONAL_OUTCOME_IDENTITY_INVALID", "outcome.measurement_id")
    if mid not in state_registry:
        _fail("DIRECT_CONDITIONAL_UNKNOWN_FROZEN_STATE", f"unknown outcome measurement {mid!r}")
    declared = tuple(
        _id(v, "DIRECT_CONDITIONAL_OUTCOME_IDENTITY_INVALID", "destination_state_id")
        for v in _sequence(
            outcome.get("destination_state_ids"),
            "DIRECT_CONDITIONAL_OUTCOME_IDENTITY_INVALID",
            "destination_state_ids",
        )
    )
    frozen = state_registry[mid]
    if declared != frozen:
        _fail(
            "DIRECT_CONDITIONAL_OUTCOME_STATE_POOLING_FORBIDDEN",
            "destination_state_ids must equal the complete frozen outcome state list in frozen order",
        )
    return outcome_id, mid, frozen


def _risk_set(
    common_manifest: Mapping[str, Any],
    risk_set: Mapping[str, Any],
) -> tuple[str, ...]:
    risk = _mapping(risk_set, "DIRECT_CONDITIONAL_RISK_SET_INVALID", "risk_set")
    if not _same(risk.get("risk_set_ref"), common_manifest["exposure_risk_set_ref"]):
        _fail("EXPERIMENT_INVALID__RESPONDENT_OR_EXPOSURE_AUTHORITY", "risk_set_ref diverges from common manifest")
    raw_ids = _sequence(risk.get("respondent_ids"), "DIRECT_CONDITIONAL_RISK_SET_INVALID", "respondent_ids")
    ids = [_id(v, "DIRECT_CONDITIONAL_RISK_SET_INVALID", "respondent_id") for v in raw_ids]
    if not ids:
        _fail("DIRECT_CONDITIONAL_RISK_SET_INVALID", "risk set cannot be empty")
    if len(ids) != len(set(ids)):
        _fail("DIRECT_CONDITIONAL_RISK_SET_INVALID", "risk set contains duplicate respondent ids")
    return tuple(sorted(ids))


def _index_rows(
    respondent_measurements: Sequence[Mapping[str, Any]],
    risk_ids: tuple[str, ...],
    required_measurements: tuple[str, ...],
    state_registry: Mapping[str, tuple[str, ...]],
) -> dict[tuple[str, str], str]:
    rows = _sequence(
        respondent_measurements,
        "DIRECT_CONDITIONAL_RESPONDENT_ROWS_INVALID",
        "respondent_measurements",
    )
    risk = set(risk_ids)
    required = set(required_measurements)
    index: dict[tuple[str, str], str] = {}
    for raw in rows:
        row = _mapping(raw, "DIRECT_CONDITIONAL_RESPONDENT_ROWS_INVALID", "respondent row")
        rid = _id(row.get("respondent_id"), "DIRECT_CONDITIONAL_RESPONDENT_ROWS_INVALID", "respondent_id")
        mid = _id(row.get("measurement_id"), "DIRECT_CONDITIONAL_RESPONDENT_ROWS_INVALID", "measurement_id")
        sid = _id(row.get("state_id"), "DIRECT_CONDITIONAL_RESPONDENT_ROWS_INVALID", "state_id")
        exposed = row.get("exposed")
        if rid not in risk or mid not in required:
            continue
        if type(exposed) is not bool:
            _fail("DIRECT_CONDITIONAL_COEXPOSURE_UNPROVED", f"exposure for {rid}/{mid} must be explicit boolean")
        if not exposed:
            _fail(
                "EXPERIMENT_INVALID__RESPONDENT_OR_EXPOSURE_AUTHORITY",
                f"{rid}/{mid} is not positively coexposed",
            )
        if mid not in state_registry or sid not in state_registry[mid]:
            _fail("DIRECT_CONDITIONAL_UNKNOWN_FROZEN_STATE", f"unknown observed state {mid}={sid}")
        key = (rid, mid)
        if key in index:
            _fail("DIRECT_CONDITIONAL_RESPONDENT_ROWS_INVALID", f"duplicate row for {rid}/{mid}")
        index[key] = sid

    for rid in risk_ids:
        for mid in required_measurements:
            if (rid, mid) not in index:
                _fail(
                    "DIRECT_CONDITIONAL_COEXPOSURE_UNPROVED",
                    f"missing positively exposed row for risk-set respondent {rid}/{mid}; missingness is not exposure authority",
                )
    return index


def _weights(
    common_manifest: Mapping[str, Any],
    estimand_design: Mapping[str, Any],
    risk_ids: tuple[str, ...],
) -> tuple[dict[str, float], str, str, float]:
    design = _mapping(estimand_design, "DIRECT_CONDITIONAL_ESTIMAND_DESIGN_INVALID", "estimand_design")
    if not _same(design.get("estimand_ref"), common_manifest["estimand_ref"]):
        _fail("EXPERIMENT_INVALID__ESTIMAND_DIVERGENCE", "estimand_ref diverges from common manifest")
    if not _same(design.get("weight_design_refs"), common_manifest["weight_design_refs"]):
        _fail("EXPERIMENT_INVALID__ESTIMAND_DIVERGENCE", "weight_design_refs diverge from common manifest")

    uncertainty = _mapping(
        design.get("uncertainty"),
        "DIRECT_CONDITIONAL_UNCERTAINTY_CONTRACT_INVALID",
        "uncertainty",
    )
    method = str(uncertainty.get("method", "KISH_WILSON_SCORE_R1"))
    if method != "KISH_WILSON_SCORE_R1":
        _fail("DIRECT_CONDITIONAL_UNCERTAINTY_CONTRACT_INVALID", f"unsupported uncertainty method {method!r}")
    try:
        confidence = float(uncertainty.get("confidence_level", 0.95))
    except (TypeError, ValueError):
        _fail("DIRECT_CONDITIONAL_UNCERTAINTY_CONTRACT_INVALID", "confidence_level must be numeric")
    if not 0.0 < confidence < 1.0:
        _fail("DIRECT_CONDITIONAL_UNCERTAINTY_CONTRACT_INVALID", "confidence_level must be between 0 and 1")

    raw = design.get("weight_by_respondent")
    refs = common_manifest["weight_design_refs"]
    explicit_none = refs is None or refs == [] or refs == "NONE" or refs == {"status": "NONE"}
    if raw in (None, {}):
        if not explicit_none:
            _fail("DIRECT_CONDITIONAL_WEIGHT_DESIGN_UNCONSUMED", "governed weight design exists but no respondent weights supplied")
        return {rid: 1.0 for rid in risk_ids}, "UNIT_WEIGHT__EXPLICIT_GOVERNED_NONE", method, confidence
    if explicit_none:
        _fail("EXPERIMENT_INVALID__ESTIMAND_DIVERGENCE", "weights supplied while common manifest declares no weight design")
    raw_map = _mapping(raw, "DIRECT_CONDITIONAL_WEIGHT_DESIGN_INVALID", "weight_by_respondent")
    out: dict[str, float] = {}
    for rid in risk_ids:
        if rid not in raw_map:
            _fail("DIRECT_CONDITIONAL_WEIGHT_DESIGN_INVALID", f"missing governed weight for {rid}")
        try:
            value = float(raw_map[rid])
        except (TypeError, ValueError):
            _fail("DIRECT_CONDITIONAL_WEIGHT_DESIGN_INVALID", f"non-numeric weight for {rid}")
        if not math.isfinite(value) or value < 0:
            _fail("DIRECT_CONDITIONAL_WEIGHT_DESIGN_INVALID", f"invalid weight for {rid}")
        out[rid] = value
    extras = set(raw_map) - set(risk_ids)
    if extras:
        _fail("DIRECT_CONDITIONAL_WEIGHT_DESIGN_INVALID", "weights include respondents outside exact risk set")
    return out, "GOVERNED_RESPONDENT_WEIGHTS_CONSUMED", method, confidence


def _support_policy(
    support_policy: Mapping[str, Any],
    exact_states: tuple[tuple[str, str], ...],
    state_registry: Mapping[str, tuple[str, ...]],
) -> tuple[int, float | None, tuple[dict[str, Any], ...]]:
    policy = _mapping(support_policy, "DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "support_policy")
    raw_min = policy.get("minimum_unweighted_support")
    if isinstance(raw_min, bool):
        _fail("DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "minimum_unweighted_support must be an integer")
    try:
        minimum_n = int(raw_min)
    except (TypeError, ValueError):
        _fail("DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "minimum_unweighted_support must be an integer")
    if minimum_n < 1 or minimum_n != raw_min:
        _fail("DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "minimum_unweighted_support must be an integer >= 1")

    raw_eff = policy.get("minimum_effective_sample_size")
    if raw_eff is None:
        minimum_eff = None
    else:
        try:
            minimum_eff = float(raw_eff)
        except (TypeError, ValueError):
            _fail("DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "minimum_effective_sample_size must be numeric")
        if not math.isfinite(minimum_eff) or minimum_eff <= 0:
            _fail("DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "minimum_effective_sample_size must be positive")

    exact_map = dict(exact_states)
    prior = exact_states
    steps: list[dict[str, Any]] = []
    raw_steps = policy.get("backoff_steps", ())
    if raw_steps is None:
        raw_steps = ()
    for raw in _sequence(raw_steps, "DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "backoff_steps"):
        step = _mapping(raw, "DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "backoff step")
        backoff_id = _id(step.get("backoff_id"), "DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "backoff_id")
        raw_states = _sequence(step.get("states"), "DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "backoff states")
        parsed: list[tuple[str, str]] = []
        seen: set[str] = set()
        for item in raw_states:
            entry = _mapping(item, "DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "backoff state")
            mid = _id(entry.get("measurement_id"), "DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "measurement_id")
            sid = _id(entry.get("state_id"), "DIRECT_CONDITIONAL_SUPPORT_POLICY_INVALID", "state_id")
            if mid in seen or mid not in exact_map or exact_map[mid] != sid:
                _fail(
                    "DIRECT_CONDITIONAL_BACKOFF_SEMANTIC_CHANGE_FORBIDDEN",
                    "backoff may only remove exact condition predicates; replacement/rebin/re-role is forbidden",
                )
            if mid not in state_registry or sid not in state_registry[mid]:
                _fail("DIRECT_CONDITIONAL_UNKNOWN_FROZEN_STATE", f"unknown backoff state {mid}={sid}")
            seen.add(mid)
            parsed.append((mid, sid))
        parsed_tuple = tuple(parsed)
        if not parsed_tuple and not bool(policy.get("allow_unconditional_backoff", False)):
            _fail("DIRECT_CONDITIONAL_BACKOFF_SEMANTIC_CHANGE_FORBIDDEN", "unconditional backoff not explicitly allowed")
        if not set(parsed_tuple) < set(prior):
            _fail(
                "DIRECT_CONDITIONAL_BACKOFF_SEMANTIC_CHANGE_FORBIDDEN",
                "each backoff step must be a strict nested subset of the previous condition",
            )
        exact_order = tuple(pair for pair in exact_states if pair in set(parsed_tuple))
        if parsed_tuple != exact_order:
            _fail("DIRECT_CONDITIONAL_BACKOFF_SEMANTIC_CHANGE_FORBIDDEN", "backoff predicate order must preserve exact condition order")
        relaxed = tuple(pair for pair in exact_states if pair not in set(parsed_tuple))
        steps.append({"backoff_id": backoff_id, "states": parsed_tuple, "relaxed_exact_states": relaxed})
        prior = parsed_tuple
    return minimum_n, minimum_eff, tuple(steps)


def _matching(
    risk_ids: tuple[str, ...],
    index: Mapping[tuple[str, str], str],
    condition_states: tuple[tuple[str, str], ...],
) -> tuple[str, ...]:
    return tuple(
        rid for rid in risk_ids
        if all(index[(rid, mid)] == sid for mid, sid in condition_states)
    )


def _effective(weights: Sequence[float]) -> float:
    total = math.fsum(weights)
    squares = math.fsum(w * w for w in weights)
    return 0.0 if squares <= 0 else total * total / squares


def _support_attempt(
    attempt_id: str,
    states: tuple[tuple[str, str], ...],
    exact_states: tuple[tuple[str, str], ...],
    matching_ids: tuple[str, ...],
    weights: Mapping[str, float],
    minimum_n: int,
    minimum_eff: float | None,
) -> dict[str, Any]:
    used_weights = [weights[rid] for rid in matching_ids]
    n_eff = _effective(used_weights)
    sufficient = len(matching_ids) >= minimum_n and (
        minimum_eff is None or n_eff >= minimum_eff
    )
    return {
        "attempt_id": attempt_id,
        "condition_states": [{"measurement_id": m, "state_id": s} for m, s in states],
        "relaxed_exact_states": [
            {"measurement_id": m, "state_id": s}
            for m, s in exact_states if (m, s) not in set(states)
        ],
        "unweighted_support": len(matching_ids),
        "weighted_support": _round(math.fsum(used_weights)),
        "effective_sample_size": _round(n_eff),
        "support_status": "SUFFICIENT_SUPPORT" if sufficient else "INSUFFICIENT_SUPPORT",
    }


def _wilson(p: float, n_eff: float, confidence: float) -> tuple[float | None, float | None, float | None]:
    if n_eff <= 0:
        return None, None, None
    z = NormalDist().inv_cdf(0.5 + confidence / 2.0)
    denominator = 1.0 + z * z / n_eff
    center = (p + z * z / (2.0 * n_eff)) / denominator
    margin = z * math.sqrt((p * (1.0 - p) / n_eff) + z * z / (4.0 * n_eff * n_eff)) / denominator
    se = math.sqrt(max(p * (1.0 - p) / n_eff, 0.0))
    return se, max(0.0, center - margin), min(1.0, center + margin)


def _distribution(
    matching_ids: tuple[str, ...],
    index: Mapping[tuple[str, str], str],
    outcome_mid: str,
    destination_states: tuple[str, ...],
    weights: Mapping[str, float],
    confidence: float,
    estimate: bool,
) -> list[dict[str, Any]]:
    counts = {sid: 0 for sid in destination_states}
    masses = {sid: [] for sid in destination_states}
    all_weights: list[float] = []
    for rid in matching_ids:
        sid = index[(rid, outcome_mid)]
        counts[sid] += 1
        masses[sid].append(weights[rid])
        all_weights.append(weights[rid])
    total_weight = math.fsum(all_weights)
    n_eff = _effective(all_weights)
    out = []
    for sid in destination_states:
        mass = math.fsum(masses[sid])
        if estimate and total_weight > 0:
            p = mass / total_weight
            se, lo, hi = _wilson(p, n_eff, confidence)
            probability = _round(p)
        else:
            probability = se = lo = hi = None
        out.append(
            {
                "destination_state_id": sid,
                "unweighted_count": counts[sid],
                "weighted_mass": _round(mass),
                "probability": probability,
                "standard_error_kish": _round(se),
                "ci_lower": _round(lo),
                "ci_upper": _round(hi),
                "estimate_status": "ESTIMATED" if probability is not None else "WITHHELD",
            }
        )
    return out


def _loss_receipt(
    common_manifest_hash: str,
    used_backoff: bool,
    relaxed_states: tuple[tuple[str, str], ...],
    status: str,
) -> dict[str, Any]:
    losses = [
        {
            "loss_code": "ROW_LEVEL_CONFIGURATION_NOT_EXPOSED",
            "invariant_id": "I04",
            "status": "DECLARED_VIEW_LIMIT",
            "detail": "Core C exposes bounded conditional redistribution, not an exact configuration carrier.",
        },
        {
            "loss_code": "HIGHER_ORDER_DISPOSITION_CONFIGURATION_NOT_REPRESENTED",
            "invariant_id": "I06",
            "status": "DOES_NOT_REPRESENT",
            "detail": "Core C does not claim higher-order disposition J/configuration preservation.",
        },
    ]
    if used_backoff:
        losses.append(
            {
                "loss_code": "CONDITION_SPECIFICITY_RELAXED",
                "invariant_id": "I07",
                "status": "EXPLICIT_BACKOFF_LOSS",
                "detail": [{"measurement_id": m, "state_id": s} for m, s in relaxed_states],
            }
        )
    if status.startswith("ABSTAINED"):
        losses.append(
            {
                "loss_code": "ESTIMATE_WITHHELD_INSUFFICIENT_SUPPORT",
                "invariant_id": "I15",
                "status": "HONEST_ABSTENTION",
                "detail": "No probability estimate emitted below declared support.",
            }
        )
    receipt = {
        "receipt_type": "TYPED_LOSS_RECEIPT",
        "schema_version": LOSS_RECEIPT_SCHEMA_VERSION,
        "arm_id": ARM_ID,
        "view_family": VIEW_FAMILY,
        "common_manifest_hash": common_manifest_hash,
        "invariant_status": {
            "I01_empirical_unit_identity": "PRESERVED_BY_EXACT_RISK_SET_RESPONDENT_ID",
            "I02_risk_set_integrity": "PRESERVED_BY_EXACT_MANIFEST_BOUND_RISK_SET",
            "I03_source_native_measurement_identity": "PRESERVED_AS_FROZEN_MEASUREMENT_IDS",
            "I05_minority_branch_preservation": "PRESERVED_IN_FULL_DESTINATION_STATE_OUTPUT",
            "I07_conditional_redistribution": "PRESERVED_BY_CONSTRUCTION",
            "I13_contradiction_nonmodal_alternatives": "PRESERVED_IN_NONMODAL_DESTINATION_MASS",
            "I15_uncertainty_support": "PRESERVED_WITH_SUPPORT_AND_UNCERTAINTY_OR_ABSTENTION",
            "I16_estimand_fidelity": "PRESERVED_BY_MANIFEST_BOUND_ESTIMAND_WEIGHT_DESIGN",
            "I18_semantic_manifest_identity": "PRESERVED_BY_HASH_ATTESTATION",
        },
        "losses": losses,
    }
    receipt["receipt_hash"] = _hash(receipt)
    return receipt


def _normalized_rows(
    respondent_measurements: Sequence[Mapping[str, Any]],
    risk_ids: tuple[str, ...],
    required_measurements: tuple[str, ...],
) -> list[dict[str, Any]]:
    risk = set(risk_ids)
    required = set(required_measurements)
    rows = []
    for raw in respondent_measurements:
        if not isinstance(raw, Mapping):
            continue
        if raw.get("respondent_id") in risk and raw.get("measurement_id") in required:
            rows.append(
                {
                    "respondent_id": raw.get("respondent_id"),
                    "measurement_id": raw.get("measurement_id"),
                    "state_id": raw.get("state_id"),
                    "exposed": raw.get("exposed"),
                }
            )
    rows.sort(key=lambda r: (r["respondent_id"], r["measurement_id"], r["state_id"]))
    return rows


def produce_direct_conditional_redistribution(
    *,
    common_manifest: Mapping[str, Any],
    frozen_state_registry: Mapping[str, Any],
    risk_set: Mapping[str, Any],
    respondent_measurements: Sequence[Mapping[str, Any]],
    condition: Mapping[str, Any],
    outcome: Mapping[str, Any],
    support_policy: Mapping[str, Any],
    estimand_design: Mapping[str, Any],
    analytic_role_binding_ref: Any,
) -> dict[str, Any]:
    common_manifest = _mapping(common_manifest, "COMMON_INPUT_MISSING_HARD_FIELD", "common_manifest")
    attestation = attest_common_manifest(common_manifest)
    if not _same(analytic_role_binding_ref, common_manifest["analytic_role_authority_refs"]):
        _fail("DIRECT_CONDITIONAL_ANALYTIC_ROLE_DIVERGENCE", "analytic role binding diverges from common manifest")

    registry = _states(common_manifest, frozen_state_registry)
    condition = _mapping(condition, "DIRECT_CONDITIONAL_CONDITION_IDENTITY_INVALID", "condition")
    condition_id, exact_states = _condition_states(condition, registry)
    outcome = _mapping(outcome, "DIRECT_CONDITIONAL_OUTCOME_IDENTITY_INVALID", "outcome")
    outcome_id, outcome_mid, destination_states = _outcome(outcome, registry)
    condition_mids = tuple(mid for mid, _ in exact_states)
    if outcome_mid in condition_mids:
        _fail("DIRECT_CONDITIONAL_CONDITION_OUTCOME_COLLISION", "outcome measurement cannot also be a condition measurement")

    risk_ids = _risk_set(common_manifest, risk_set)
    required_measurements = condition_mids + (outcome_mid,)
    index = _index_rows(respondent_measurements, risk_ids, required_measurements, registry)
    weights, weight_mode, uncertainty_method, confidence = _weights(
        common_manifest, estimand_design, risk_ids
    )
    minimum_n, minimum_eff, backoff_steps = _support_policy(
        support_policy, exact_states, registry
    )

    exact_matching = _matching(risk_ids, index, exact_states)
    attempts = [
        _support_attempt(
            "EXACT",
            exact_states,
            exact_states,
            exact_matching,
            weights,
            minimum_n,
            minimum_eff,
        )
    ]
    selected_id: str | None = None
    selected_states: tuple[tuple[str, str], ...] | None = None
    selected_matching: tuple[str, ...] | None = None
    relaxed: tuple[tuple[str, str], ...] = ()

    if attempts[0]["support_status"] == "SUFFICIENT_SUPPORT":
        selected_id, selected_states, selected_matching = "EXACT", exact_states, exact_matching
    else:
        for step in backoff_steps:
            matching = _matching(risk_ids, index, step["states"])
            attempt = _support_attempt(
                step["backoff_id"],
                step["states"],
                exact_states,
                matching,
                weights,
                minimum_n,
                minimum_eff,
            )
            attempts.append(attempt)
            if attempt["support_status"] == "SUFFICIENT_SUPPORT":
                selected_id = step["backoff_id"]
                selected_states = step["states"]
                selected_matching = matching
                relaxed = step["relaxed_exact_states"]
                break

    if selected_matching is None:
        status = "ABSTAINED__INSUFFICIENT_SUPPORT"
        basis = "EXACT_CONDITION_SUPPORT_ONLY__NO_ESTIMATE"
        selected_condition = None
        distribution = _distribution(
            exact_matching,
            index,
            outcome_mid,
            destination_states,
            weights,
            confidence,
            False,
        )
    else:
        used_backoff = selected_id != "EXACT"
        status = "ESTIMATED__BACKOFF_USED" if used_backoff else "ESTIMATED__EXACT_CONDITION"
        basis = "BACKOFF_CONDITION" if used_backoff else "EXACT_CONDITION"
        selected_condition = {
            "selection_id": selected_id,
            "states": [{"measurement_id": m, "state_id": s} for m, s in selected_states or ()],
            "relaxed_exact_states": [{"measurement_id": m, "state_id": s} for m, s in relaxed],
        }
        distribution = _distribution(
            selected_matching,
            index,
            outcome_mid,
            destination_states,
            weights,
            confidence,
            True,
        )

    condition_identity = {
        "condition_id": condition_id,
        "states": [{"measurement_id": m, "state_id": s} for m, s in exact_states],
    }
    condition_identity["identity_hash"] = _hash(condition_identity)
    outcome_identity = {
        "outcome_id": outcome_id,
        "measurement_id": outcome_mid,
        "destination_state_ids": list(destination_states),
    }
    outcome_identity["identity_hash"] = _hash(outcome_identity)
    used_backoff = selected_id is not None and selected_id != "EXACT"

    loss_receipt = _loss_receipt(
        common_manifest["manifest_hash"], used_backoff, relaxed, status
    )
    core = {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "producer_version": PRODUCER_VERSION,
        "arm_id": ARM_ID,
        "view_family": VIEW_FAMILY,
        "semantic_non_equivalence_notice": (
            "NOT_V551_CONDITIONAL_DETERMINICITY__RESPONDENT_LEVEL_DIRECT_REDISTRIBUTION_ONLY"
        ),
        "status": status,
        "common_manifest_attestation": attestation,
        "condition_identity": condition_identity,
        "outcome_identity": outcome_identity,
        "risk_set": {
            "risk_set_ref": risk_set["risk_set_ref"],
            "n_respondents": len(risk_ids),
            "risk_set_hash": _hash({"respondent_ids": list(risk_ids)}),
            "coexposure_status": "POSITIVE_COEXPOSURE_PROVED_FOR_ALL_RISK_SET_RESPONDENTS",
            "required_measurement_ids": list(required_measurements),
        },
        "estimand_design": {
            "estimand_ref": estimand_design["estimand_ref"],
            "weight_design_refs": estimand_design["weight_design_refs"],
            "weight_mode": weight_mode,
            "uncertainty_method": uncertainty_method,
            "confidence_level": _round(confidence),
            "uncertainty_scope": (
                "KISH_EFFECTIVE_SAMPLE_SIZE_WILSON_APPROXIMATION__"
                "NOT_SILENT_COMPLEX_SURVEY_VARIANCE"
            ),
        },
        "support_policy": {
            "minimum_unweighted_support": minimum_n,
            "minimum_effective_sample_size": _round(minimum_eff),
            "backoff_policy": "STRICT_SUBSET_PREDICATE_REMOVAL_ONLY",
            "attempts": attempts,
            "selected_condition": selected_condition,
            "abstention_status": (
                "ABSTAINED_INSUFFICIENT_SUPPORT"
                if status.startswith("ABSTAINED")
                else "NOT_ABSTAINED"
            ),
        },
        "distribution_basis": basis,
        "destination_distribution": distribution,
        "loss_receipt": loss_receipt,
    }

    input_hashes = {
        "common_manifest_hash": common_manifest["manifest_hash"],
        "frozen_state_registry_hash": _hash(frozen_state_registry),
        "risk_set_hash": _hash({"risk_set_ref": risk_set["risk_set_ref"], "respondent_ids": list(risk_ids)}),
        "respondent_measurements_hash": _hash(_normalized_rows(respondent_measurements, risk_ids, required_measurements)),
        "condition_contract_hash": _hash(condition),
        "outcome_contract_hash": _hash(outcome),
        "support_policy_hash": _hash(support_policy),
        "estimand_design_hash": _hash(estimand_design),
        "analytic_role_binding_hash": _hash(analytic_role_binding_ref),
    }
    output_hash = _hash(core)
    replay = {
        "receipt_type": "TYPED_REPLAY_RECEIPT",
        "schema_version": REPLAY_RECEIPT_SCHEMA_VERSION,
        "producer_version": PRODUCER_VERSION,
        "numeric_replay_contract_version": NUMERIC_REPLAY_CONTRACT_VERSION,
        "arm_id": ARM_ID,
        "view_family": VIEW_FAMILY,
        "common_manifest_hash": common_manifest["manifest_hash"],
        "input_hashes": input_hashes,
        "determinism_contract": {
            "respondent_order": "LEXICOGRAPHIC_RESPONDENT_ID",
            "row_hash_order": "RESPONDENT_MEASUREMENT_STATE_EXPOSURE_SORTED",
            "destination_order": "FROZEN_OUTCOME_STATE_ORDER",
            "summation": "PYTHON_MATH_FSUM_R1",
            "float_output_round_digits": FLOAT_DIGITS,
            "uncertainty": uncertainty_method,
            "hash": "SHA256_CANONICAL_JSON",
        },
        "output_hash": output_hash,
    }
    replay["receipt_hash"] = _hash(replay)
    result = dict(core)
    result["output_hash"] = output_hash
    result["replay_receipt"] = replay
    return result


def compile_direct_conditional_bundle(bundle: Mapping[str, Any]) -> dict[str, Any]:
    bundle = _mapping(bundle, "DIRECT_CONDITIONAL_INPUT_BUNDLE_INVALID", "input bundle")
    return produce_direct_conditional_redistribution(
        common_manifest=bundle.get("common_manifest"),
        frozen_state_registry=bundle.get("frozen_state_registry"),
        risk_set=bundle.get("risk_set"),
        respondent_measurements=bundle.get("respondent_measurements"),
        condition=bundle.get("condition"),
        outcome=bundle.get("outcome"),
        support_policy=bundle.get("support_policy"),
        estimand_design=bundle.get("estimand_design"),
        analytic_role_binding_ref=bundle.get("analytic_role_binding_ref"),
    )


def _error_envelope(exc: DirectConditionalContractError) -> dict[str, Any]:
    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "producer_version": PRODUCER_VERSION,
        "arm_id": ARM_ID,
        "view_family": VIEW_FAMILY,
        "status": "FAILED_CLOSED",
        "error": {"code": exc.code, "detail": exc.detail},
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compile one FFX002-R2 Core-C respondent-level direct conditional redistribution bundle."
    )
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args(argv)

    with open(args.input_json, "r", encoding="utf-8") as handle:
        bundle = json.load(handle)
    code = 0
    try:
        result = compile_direct_conditional_bundle(bundle)
    except DirectConditionalContractError as exc:
        result = _error_envelope(exc)
        code = 2
    with open(args.output_json, "w", encoding="utf-8") as handle:
        json.dump(
            result,
            handle,
            ensure_ascii=False,
            sort_keys=True,
            indent=2 if args.pretty else None,
            separators=None if args.pretty else (",", ":"),
            allow_nan=False,
        )
        handle.write("\n")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
