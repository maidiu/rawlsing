"""Canonical V552 v2.1.4 contract hashing helpers."""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import dataclass
from typing import Any, Mapping, Sequence

import pandas as pd

def v552_canonical_value(value: Any) -> Any:
    if value is None:
        return ""
    try:
        if hasattr(value, "item"):
            value = value.item()
    except Exception:
        pass
    try:
        if value != value:
            return ""
    except Exception:
        pass
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        if isinstance(value, float) and not math.isfinite(value):
            return ""
        number = float(value)
        if number.is_integer():
            return str(int(number))
        return format(number, ".12g")
    text = str(value).strip()
    if text.lower() in {"nan", "none", "null"}:
        return ""
    if text.casefold() in {"true", "false"}:
        return text.casefold()
    try:
        number = float(text)
        if math.isfinite(number):
            if number.is_integer():
                return str(int(number))
            return format(number, ".12g")
    except Exception:
        pass
    return text


def v552_canonical_json(payload: Mapping[str, Any]) -> str:
    def norm(value: Any) -> Any:
        if isinstance(value, Mapping):
            return {str(k): norm(v) for k, v in sorted(value.items(), key=lambda item: str(item[0]))}
        if isinstance(value, (list, tuple)):
            return [norm(v) for v in value]
        return v552_canonical_value(value)

    return json.dumps(norm(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def v552_hash_payload(namespace: str, payload: Mapping[str, Any]) -> str:
    return hashlib.sha256(v552_canonical_json({"namespace": namespace, **dict(payload)}).encode("utf-8")).hexdigest()


def v552_stable_hash(payload: Any) -> str:
    if isinstance(payload, Mapping):
        serialized = v552_canonical_json(payload)
    else:
        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _prefixed_id(prefix: str, payload: Mapping[str, Any], length: int = 20) -> str:
    return f"{prefix}{v552_stable_hash(payload)[:length]}"


def v552_component_identity_payload(component: Mapping[str, Any]) -> dict[str, str]:
    fields = [
        "source_atom_id",
        "empirical_object_id",
        "response_value_normalized",
        "response_scale_signature",
        "semantic_identity_signature",
        "structural_identity_signature",
    ]
    return {field: str(v552_canonical_value(component.get(field))) for field in fields}


def recompute_v552_pressure_component_id(component: Mapping[str, Any]) -> str:
    return _prefixed_id("v552pc__", v552_component_identity_payload(component), 24)


def v552_observation_identity_payload(atom_or_observation: Mapping[str, Any]) -> dict[str, str]:
    fields = [
        "source",
        "source_family",
        "canonical_wave",
        "country_code",
        "analysis_scope",
        "empirical_object_type",
        "empirical_distribution_id",
        "question_id",
        "var_code",
        "position_field",
        "position_value",
        "semantic_identity_signature",
        "structural_identity_signature",
        "response_scale_signature",
    ]
    return {field: str(v552_canonical_value(atom_or_observation.get(field))) for field in fields}


def recompute_v552_pressure_observation_id(atom_or_observation: Mapping[str, Any]) -> str:
    return _prefixed_id("v552po__", v552_observation_identity_payload(atom_or_observation), 20)


def v552_response_surface_payload(components: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    rows = []
    for component in components:
        rows.append({
            "response_value_normalized": v552_canonical_value(component.get("response_value_normalized")),
            "normalized_response_label": v552_canonical_value(component.get("normalized_response_label")),
            "response_family": v552_canonical_value(component.get("response_family")),
            "response_direction": v552_canonical_value(component.get("response_direction")),
            "response_direction_sign": v552_canonical_value(component.get("response_direction_sign")),
            "canonical_signed_component": v552_canonical_value(component.get("canonical_signed_component")),
            "scale_encoding_class": v552_canonical_value(component.get("scale_encoding_class")),
            "source_intensity_representation_class": v552_canonical_value(component.get("source_intensity_representation_class")),
            "source_intensity_representation_status": v552_canonical_value(component.get("source_intensity_representation_status")),
            "scale_transform_id": v552_canonical_value(component.get("scale_transform_id")),
        })
    return {
        "contract": "V552_COMPONENT_RESPONSE_SURFACE_V1",
        "components": sorted(rows, key=lambda item: v552_canonical_json(item)),
    }


def recompute_v552_response_surface_signature(components: Sequence[Mapping[str, Any]]) -> str:
    return v552_stable_hash(v552_response_surface_payload(components))


def recompute_v552_dominant_orientation(
    positive_share: float | None,
    negative_share: float | None,
    neutral_share: float | None,
) -> tuple[str, float | None]:
    shares = {
        "neutral": _num(neutral_share) or 0.0,
        "positive": _num(positive_share) or 0.0,
        "negative": _num(negative_share) or 0.0,
    }
    order = {"neutral": 0, "positive": 1, "negative": 2}
    label, share = max(shares.items(), key=lambda item: (item[1], -order[item[0]]))
    return label, share


@dataclass(frozen=True)
class V552ObservationState:
    pressure_score_status: str
    observed_pressure_zero: bool
    pressure_magnitude: float | None
    pressure_orientation: str
    component_permission_status: str
    pressure_observation_status: str
    pressure_observation_ineligibility_reason: str
    v552j_pressure_linkage_eligible: bool
    v552j_structural_context_eligible: bool
    v553_probe_candidate_after_v552j: bool


def recompute_v552_observation_state(
    *,
    pressure_score: float | None,
    components: pd.DataFrame,
    response_surface_status: str,
    root_issue_tokens: Sequence[str],
) -> V552ObservationState:
    score = _num(pressure_score)
    root_issues = tuple(str(token) for token in root_issue_tokens if str(token))
    component_ok = True
    if not components.empty and "component_pressure_eligible" in components:
        component_ok = components["component_pressure_eligible"].map(lambda value: str(v552_canonical_value(value)).casefold() in {"true", "1", "yes"}).all()
    surface_ok = response_surface_status in {
        "COMPLETE_SELECTED_RESPONSE_CATEGORY_COVERAGE",
        "PARTIAL_SELECTED_RESPONSE_CATEGORY_COVERAGE",
        "UNKNOWN_RESPONSE_CATEGORY_COVERAGE",
    }
    if score is None:
        score_status = "NOT_COMPUTABLE"
        observed_zero = False
        magnitude = None
        orientation = "unknown"
    elif abs(score) <= 1e-12:
        score = 0.0
        score_status = "OBSERVED_ZERO"
        observed_zero = True
        magnitude = 0.0
        orientation = "axis_balanced_or_neutral"
    elif score > 0:
        score_status = "OBSERVED_NONZERO"
        observed_zero = False
        magnitude = abs(score)
        orientation = "axis_amplifying"
    else:
        score_status = "OBSERVED_NONZERO"
        observed_zero = False
        magnitude = abs(score)
        orientation = "axis_suppressing"
    lawful = score is not None and component_ok and surface_ok and not root_issues
    component_status = "ALL_COMPONENTS_ELIGIBLE" if component_ok else "SOME_COMPONENTS_INELIGIBLE"
    obs_status = "OBSERVED_PRESSURE" if lawful else "NOT_COMPUTABLE_OR_BLOCKED"
    reason = "" if lawful else "|".join(root_issues) or ("" if score is not None else "pressure_not_computable")
    return V552ObservationState(
        pressure_score_status=score_status,
        observed_pressure_zero=observed_zero,
        pressure_magnitude=magnitude,
        pressure_orientation=orientation,
        component_permission_status=component_status,
        pressure_observation_status=obs_status,
        pressure_observation_ineligibility_reason=reason,
        v552j_pressure_linkage_eligible=lawful,
        v552j_structural_context_eligible=True,
        v553_probe_candidate_after_v552j=lawful,
    )


V552_COMPONENT_MEASUREMENT_FIELDS = [
    "v552_pressure_component_id",
    "source_atom_id",
    "source_atom_contract_hash",
    "source_measurement_contract_hash",
    "empirical_object_id",
    "empirical_distribution_id",
    "question_id",
    "var_code",
    "response_value_normalized",
    "normalized_response_label",
    "response_family",
    "response_direction",
    "response_direction_sign",
    "response_intensity",
    "source_intensity_zero",
    "scale_min",
    "scale_max",
    "scale_direction",
    "source_scale_direction_token",
    "directionality_policy",
    "response_topology",
    "response_scale_signature",
    "source_intensity_representation_class",
    "source_intensity_representation_status",
    "source_intensity_exact_fit_candidates_json",
    "normalized_intensity_min",
    "normalized_intensity_max",
    "scale_encoding_class",
    "scale_transform_id",
    "normalized_source_coordinate",
    "normalized_construct_magnitude",
    "canonical_signed_component",
    "canonical_signed_component_zero",
    "direction_scale_consistency_status",
    "distribution_weight_basis",
    "distribution_weight_raw",
    "distribution_weight_normalized",
    "n_unweighted",
    "n_respondents",
    "n_weighted",
    "pct_unweighted",
    "pct_weighted",
    "population_share",
    "weight_status",
    "component_pressure_eligible",
    "component_pressure_status",
    "component_pressure_ineligibility_reason",
    "semantic_identity_signature",
    "structural_identity_signature",
]


def v552_v2_1_4_component_measurement_payload(component: Mapping[str, Any]) -> dict[str, Any]:
    return {field: v552_canonical_value(component.get(field)) for field in V552_COMPONENT_MEASUREMENT_FIELDS}


def recompute_v552_v2_1_4_component_measurement_hash(component: Mapping[str, Any]) -> str:
    return v552_hash_payload(
        "v552_component_measurement_v2_1_4",
        v552_v2_1_4_component_measurement_payload(component),
    )


def v552_v2_1_4_pressure_measurement_payload(
    observation: Mapping[str, Any],
    ordered_components: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    components = sorted(
        [
            {
                "v552_pressure_component_id": c.get("v552_pressure_component_id"),
                "component_measurement_hash": c.get("component_measurement_hash"),
                "source_atom_id": c.get("source_atom_id"),
                "source_atom_contract_hash": c.get("source_atom_contract_hash"),
                "source_measurement_contract_hash": c.get("source_measurement_contract_hash"),
                "response_value_normalized": c.get("response_value_normalized"),
                "response_direction": c.get("response_direction"),
                "response_direction_sign": c.get("response_direction_sign"),
                "response_intensity": c.get("response_intensity"),
                "canonical_signed_component": c.get("canonical_signed_component"),
                "distribution_weight_basis": c.get("distribution_weight_basis"),
                "distribution_weight_raw": c.get("distribution_weight_raw"),
                "distribution_weight_normalized": c.get("distribution_weight_normalized"),
            }
            for c in ordered_components
        ],
        key=lambda item: v552_canonical_json(item),
    )
    fields = [
        "v552_pressure_observation_id",
        "pressure_observation_identity_hash",
        "empirical_distribution_id",
        "source",
        "source_family",
        "wave",
        "canonical_wave",
        "country_code",
        "question_id",
        "var_code",
        "semantic_identity_signature",
        "structural_identity_signature",
        "response_scale_signature",
        "source_intensity_representation_class",
        "source_intensity_representation_status",
        "source_intensity_exact_fit_candidates_json",
        "normalized_intensity_min",
        "normalized_intensity_max",
        "source_scale_direction_token",
        "component_response_surface_signature",
        "response_surface_component_count",
        "response_surface_respondent_coverage",
        "response_surface_completeness_status",
        "response_surface_completeness_basis",
        "distribution_weight_basis",
        "distribution_mass_raw",
        "distribution_mass_used",
        "substantive_response_coverage",
        "respondent_denominator_unweighted",
        "weighted_response_mass",
        "pressure_formula_id",
        "pressure_formula_version",
        "pressure_scale_id",
        "pressure_scale_min",
        "pressure_scale_max",
        "pressure_score",
        "pressure_magnitude",
        "pressure_orientation",
        "pressure_score_status",
        "observed_pressure_zero",
        "pressure_measure_class",
        "positive_component_share",
        "negative_component_share",
        "neutral_component_share",
        "directional_entropy",
        "polarization_index",
        "dominant_orientation",
        "dominant_orientation_share",
        "component_signed_intensity_min",
        "component_signed_intensity_max",
        "component_signed_intensity_std",
        "component_permission_status",
        "pressure_observation_status",
        "pressure_observation_ineligibility_reason",
        "v552j_pressure_linkage_eligible",
        "v552j_structural_context_eligible",
        "v553_probe_candidate_after_v552j",
        "allowed_for_v553_temporal_field",
        "known_absences_json",
        "forbidden_inference_json",
        "schema_version",
        "compiler_version",
    ]
    payload = {field: observation.get(field) for field in fields}
    payload["components"] = components
    payload["component_ids"] = [c["v552_pressure_component_id"] for c in components]
    payload["component_measurement_hashes"] = [c["component_measurement_hash"] for c in components]
    return payload


def recompute_v552_v2_1_4_pressure_measurement_hash(
    observation: Mapping[str, Any],
    ordered_components: Sequence[Mapping[str, Any]],
) -> str:
    return v552_hash_payload(
        "v552_pressure_measurement_v2_1_4",
        v552_v2_1_4_pressure_measurement_payload(observation, ordered_components),
    )


@dataclass(frozen=True)
class V552DistributionContractRecomputation:
    empirical_distribution_id: str
    representation_class: str
    representation_status: str
    distribution_weight_basis: str
    distribution_weight_raw_by_atom: dict[str, float]
    distribution_weight_normalized_by_atom: dict[str, float]
    distribution_mass_raw: float | None
    distribution_mass_used: float | None
    substantive_response_coverage: float | None
    respondent_denominator_unweighted: float | None
    weighted_response_mass: float | None
    response_surface_component_count: int
    response_surface_respondent_coverage: float | None
    response_surface_completeness_status: str
    response_surface_completeness_basis: str
    pressure_score: float | None
    pressure_score_status: str
    pressure_measure_class: str
    positive_component_share: float | None
    negative_component_share: float | None
    neutral_component_share: float | None
    directional_entropy: float | None
    polarization_index: float | None
    dominant_orientation: str
    dominant_orientation_share: float | None
    component_signed_intensity_min: float | None
    component_signed_intensity_max: float | None
    component_signed_intensity_std: float | None
    root_issue_tokens: tuple[str, ...]


def _num(value: Any) -> float | None:
    try:
        if value is None:
            return None
        out = float(value)
        if not math.isfinite(out):
            return None
        return out
    except Exception:
        return None


def _direction_sign(value: Any) -> int | None:
    token = str(value or "").strip().casefold()
    if token in {"positive", "support", "agree", "approve", "favor", "favour", "yes"}:
        return 1
    if token in {"negative", "oppose", "disagree", "disapprove", "against", "no"}:
        return -1
    if token in {"neutral", "neither", "balanced"}:
        return 0
    return None


def _signed_for(row: Mapping[str, Any], representation: str) -> tuple[float | None, str]:
    sign = _direction_sign(row.get("response_direction"))
    if sign is None:
        return None, "unknown_response_direction"
    intensity = _num(row.get("response_intensity"))
    if intensity is None or intensity < -1e-12 or intensity > 1.0 + 1e-12:
        return None, "normalized_intensity_out_of_bounds"
    if abs(intensity) <= 1e-12:
        intensity = 0.0
    if abs(intensity - 1.0) <= 1e-12:
        intensity = 1.0
    signed = 2.0 * intensity - 1.0 if representation == "NORMALIZED_AXIS_COORDINATE_0_1" else float(sign) * intensity
    if sign > 0 and signed <= 1e-12:
        return None, "unresolved_intensity_representation"
    if sign < 0 and signed >= -1e-12:
        return None, "unresolved_intensity_representation"
    if sign == 0 and abs(signed) > 1e-12:
        return None, "unresolved_intensity_representation"
    return (0.0 if abs(signed) <= 1e-12 else signed), ""


def _representation(atom_group: pd.DataFrame) -> tuple[str, str, tuple[str, ...], tuple[str, ...]]:
    exact: list[str] = []
    roots: list[str] = []
    for candidate in ["NORMALIZED_AXIS_COORDINATE_0_1", "NORMALIZED_UNSIGNED_MAGNITUDE_0_1"]:
        ok = True
        for row in atom_group.to_dict("records"):
            _, issue = _signed_for(row, candidate)
            if issue:
                ok = False
                if issue not in roots:
                    roots.append(issue)
                break
        if ok:
            exact.append(candidate)
    if len(exact) == 1:
        return exact[0], "EXACT_UNIQUE_DISTRIBUTION_RESOLUTION", tuple(exact), tuple()
    if len(exact) > 1:
        return "UNRESOLVED", "BLOCKED_AMBIGUOUS_INTENSITY_REPRESENTATION", tuple(exact), ("ambiguous_intensity_representation",)
    if "unknown_response_direction" in roots:
        return "UNRESOLVED", "BLOCKED_UNKNOWN_RESPONSE_DIRECTION", tuple(), ("unknown_response_direction",)
    if "normalized_intensity_out_of_bounds" in roots:
        return "UNRESOLVED", "BLOCKED_INVALID_NORMALIZED_INTENSITY", tuple(), ("normalized_intensity_out_of_bounds",)
    return "UNRESOLVED", "BLOCKED_UNRESOLVED_INTENSITY_REPRESENTATION", tuple(), ("unresolved_intensity_representation",)


def recompute_v552_distribution_contract(
    input_atom_group: pd.DataFrame,
    component_group: pd.DataFrame,
) -> V552DistributionContractRecomputation:
    dist = str(input_atom_group["empirical_distribution_id"].iloc[0] if not input_atom_group.empty else component_group.get("empirical_distribution_id", pd.Series([""])).iloc[0])
    rep_class, rep_status, _, root_issues = _representation(input_atom_group)
    atom_by_id = {str(row.get("atom_id")): row for row in input_atom_group.to_dict("records")}
    raw_by_atom: dict[str, float] = {}
    norm_by_atom: dict[str, float] = {}
    basis = "none"
    if not root_issues:
        for candidate in ["pct_weighted", "pct_unweighted", "population_share", "n_unweighted"]:
            values: dict[str, float] = {}
            ok = True
            for atom_id, atom in atom_by_id.items():
                value = _num(atom.get(candidate))
                if value is None or value < -1e-12:
                    ok = False
                    break
                values[atom_id] = value
            if ok and sum(values.values()) > 0:
                if candidate == "pct_weighted":
                    statuses = [str(a.get("weight_status", "")).casefold() for a in atom_by_id.values()]
                    if any(any(tok in s for tok in ["missing", "unavailable", "invalid", "unweighted_only", "not_weighted"]) for s in statuses):
                        continue
                basis = "normalized_n_unweighted" if candidate == "n_unweighted" else candidate
                raw_by_atom = values
                total = sum(values.values())
                norm_by_atom = {k: v / total for k, v in values.items()}
                break
    mass_raw = sum(raw_by_atom.values()) if raw_by_atom else None
    pressure = None
    pressure_status = "NOT_COMPUTABLE"
    signed_values: dict[str, float] = {}
    if not root_issues and norm_by_atom:
        total = 0.0
        for atom_id, atom in atom_by_id.items():
            signed, issue = _signed_for(atom, rep_class)
            if issue:
                root_issues = (issue,)
                break
            assert signed is not None
            signed_values[atom_id] = signed
            total += norm_by_atom[atom_id] * signed
        if not root_issues:
            pressure = 0.0 if abs(total) <= 1e-12 else total
            pressure_status = "OBSERVED_ZERO" if pressure == 0.0 else "OBSERVED_NONZERO"
    denom_values = sorted({_num(row.get("n_respondents")) for row in atom_by_id.values()} - {None})
    denom = denom_values[0] if len([v for v in denom_values if v and v > 0]) == 1 else None
    sum_n = sum((_num(row.get("n_unweighted")) or 0.0) for row in atom_by_id.values())
    coverage = (sum_n / denom) if denom else None
    if denom and sum_n == denom:
        surface_status = "COMPLETE_SELECTED_RESPONSE_CATEGORY_COVERAGE"
    elif denom and sum_n < denom:
        surface_status = "PARTIAL_SELECTED_RESPONSE_CATEGORY_COVERAGE"
    elif denom and sum_n > denom:
        surface_status = "BLOCKED_RESPONSE_CATEGORY_COUNT_EXCEEDS_DENOMINATOR"
    else:
        surface_status = "UNKNOWN_RESPONSE_CATEGORY_COVERAGE"
    measure_class = "single_question_scale_aware_directional_distribution_not_computable"
    if pressure is not None:
        if surface_status == "COMPLETE_SELECTED_RESPONSE_CATEGORY_COVERAGE":
            measure_class = "single_question_scale_aware_directional_distribution_pressure"
        elif surface_status == "PARTIAL_SELECTED_RESPONSE_CATEGORY_COVERAGE":
            measure_class = "single_question_scale_aware_conditional_selected_response_surface_pressure"
        elif surface_status == "UNKNOWN_RESPONSE_CATEGORY_COVERAGE":
            measure_class = "single_question_scale_aware_observed_response_surface_pressure_unknown_denominator"
    if pressure is not None:
        pos = sum(norm_by_atom[k] for k, v in signed_values.items() if v > 1e-12)
        neg = sum(norm_by_atom[k] for k, v in signed_values.items() if v < -1e-12)
        neu = sum(norm_by_atom[k] for k, v in signed_values.items() if abs(v) <= 1e-12)
        opposed = pos + neg
        if opposed > 0:
            p = pos / opposed
            n = neg / opposed
            polarization = 2 * min(p, n)
            entropy = -sum(v * math.log(v, 2) for v in [p, n] if v > 0)
        else:
            polarization = entropy = 0.0
        dominant = max([("positive", pos), ("negative", neg), ("neutral", neu)], key=lambda x: (x[1], x[0]))[0]
        dominant_share = max(pos, neg, neu)
        values = list(signed_values.values())
        mean = pressure
        std = math.sqrt(sum(norm_by_atom[k] * ((signed_values[k] - mean) ** 2) for k in signed_values))
    else:
        pos = neg = neu = polarization = entropy = dominant_share = std = None
        dominant = ""
        values = []
    weighted_values = [_num(row.get("n_weighted")) for row in atom_by_id.values()]
    weighted_present = [value for value in weighted_values if value is not None]
    weighted_response_mass = sum(weighted_present) if weighted_present else None
    return V552DistributionContractRecomputation(
        empirical_distribution_id=dist,
        representation_class=rep_class,
        representation_status=rep_status,
        distribution_weight_basis=basis,
        distribution_weight_raw_by_atom=raw_by_atom,
        distribution_weight_normalized_by_atom=norm_by_atom,
        distribution_mass_raw=mass_raw,
        distribution_mass_used=1.0 if pressure is not None else None,
        substantive_response_coverage=mass_raw if basis in {"pct_weighted", "pct_unweighted", "population_share"} else None,
        respondent_denominator_unweighted=denom,
        weighted_response_mass=weighted_response_mass,
        response_surface_component_count=len(input_atom_group),
        response_surface_respondent_coverage=coverage,
        response_surface_completeness_status=surface_status,
        response_surface_completeness_basis="unweighted_component_count_over_unique_respondent_denominator",
        pressure_score=pressure,
        pressure_score_status=pressure_status,
        pressure_measure_class=measure_class,
        positive_component_share=pos,
        negative_component_share=neg,
        neutral_component_share=neu,
        directional_entropy=entropy,
        polarization_index=polarization,
        dominant_orientation=dominant,
        dominant_orientation_share=dominant_share,
        component_signed_intensity_min=min(values) if values else None,
        component_signed_intensity_max=max(values) if values else None,
        component_signed_intensity_std=std,
        root_issue_tokens=tuple(root_issues),
    )
