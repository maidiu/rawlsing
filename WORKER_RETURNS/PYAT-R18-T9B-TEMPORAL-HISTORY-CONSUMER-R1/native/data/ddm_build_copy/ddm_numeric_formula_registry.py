#!/usr/bin/env python3
"""Validation helpers for the numeric formula registry."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any
import re

import yaml


ROOT = Path(__file__).resolve().parents[2]
NUMERIC_FORMULA_REGISTRY_PATH = Path(__file__).resolve().parent / "manifests" / "numeric_formula_registry.yaml"
FORMULA_FUNCTIONS = {"weighted_mean", "clamp", "min", "max", "abs", "sign", "log"}
FORMULA_RESERVED_TOKENS = {
    "and",
    "or",
    "not",
    "in",
    "null",
    "none",
    "true",
    "false",
    "missing",
    "weighted",
    "unweighted_only",
    "blocked",
    "demote",
    "allow",
    "threshold",
    "below",
    "above",
    "least",
    "most",
    "at",
    "is",
    "n",
    "if",
}

TOP_LEVEL_REQUIRED_KEYS = {
    "registry_version",
    "doctrine",
    "status",
    "required_formula_fields",
    "score_families",
    "hard_gate_policy",
    "formulas",
}

BASE_REQUIRED_FORMULA_FIELDS = {
    "formula_id",
    "formula_version",
    "output_field",
    "score_family",
    "score_interpretation",
    "scale",
    "higher_is_better",
    "decision_role",
    "inputs",
    "input_scales",
    "denominator_policy",
    "null_policy",
    "thresholds",
    "allowed_artifacts",
}

COMPONENT_POLARITY_ALLOWED = {"positive", "negative", "neutral", "signed"}
INPUT_SCALE_ALLOWED = {"0-1", "0-100", "count", "ratio", "boolean", "categorical", "raw", "ratio_capped_0_1"}
NORMALIZED_INPUT_SCALES = {"0-1", "0-100", "ratio", "ratio_capped_0_1"}
RATIO_SCALE_FAMILY = {"0-1", "ratio", "ratio_capped_0_1"}
HUNDRED_SCALE_FAMILY = {"0-100"}
HARD_GATE_POLICY_REQUIRED_KEYS = {
    "hard_gates_override_scores",
    "blocked_rows_may_emit_scores_for_diagnostics",
    "blocked_rows_must_not_be_eligible_for_downstream_evidence",
    "category_only_evidence_must_fail_closed",
}
EXEMPT_INPUT_GROUP_KEYS = ("metadata_inputs", "provenance_inputs", "gate_inputs", "hard_gate_inputs")


def _clean_text(value: object) -> str:
    if value is None:
        return ""
    text = str(value).strip()
    if text.lower() in {"", "nan", "none", "<na>"}:
        return ""
    return text


def _is_nonempty_string(value: object) -> bool:
    return bool(_clean_text(value))


def _is_bool(value: object) -> bool:
    return isinstance(value, bool)


def _is_string_list(value: object) -> bool:
    return isinstance(value, list) and all(_is_nonempty_string(item) for item in value)


def _is_valid_input_scale(value: object) -> bool:
    return _clean_text(value) in INPUT_SCALE_ALLOWED


def _scale_family(scale: object) -> str:
    cleaned = _clean_text(scale)
    if cleaned in RATIO_SCALE_FAMILY:
        return "ratio"
    if cleaned in HUNDRED_SCALE_FAMILY:
        return "hundred"
    if cleaned in {"count", "boolean", "categorical", "raw"}:
        return cleaned
    return "unknown"


def _looks_like_formula_expression(value: object) -> bool:
    text = _clean_text(value)
    if not text:
        return False
    if any(token in text for token in ("weighted_mean(", "clamp(", "min(", "max(", "sign(")):
        return True
    if any(op in text for op in ("+", "-", "*", "/", "==", "!=", ">=", "<=", ">", "<")):
        return True
    return bool(text.count("(") and text.count(")") and any(ch.isdigit() for ch in text))


def _identifier_tokens(value: object) -> set[str]:
    text = _clean_text(value)
    if not text:
        return set()
    return {token for token in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text)}


def _declared_formula_fields(formula: dict[str, Any]) -> set[str]:
    declared: set[str] = set()
    for key in ("inputs", "metadata_inputs", "provenance_inputs", "gate_inputs", "hard_gate_inputs"):
        values = formula.get(key)
        if _is_string_list(values):
            declared.update(_clean_text(item) for item in values if _clean_text(item))
    return declared


def _extract_weighted_mean_arguments(expression: str) -> list[str]:
    marker = "weighted_mean("
    args: list[str] = []
    start = 0
    while True:
        idx = expression.find(marker, start)
        if idx == -1:
            break
        pos = idx + len(marker)
        depth = 1
        chunk: list[str] = []
        while pos < len(expression) and depth > 0:
            char = expression[pos]
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    break
            if depth > 0:
                chunk.append(char)
            pos += 1
        if chunk:
            args.append("".join(chunk))
        start = pos + 1
    return args


def _contains_visible_hundred_scale(expression: str) -> bool:
    text = _clean_text(expression)
    if not text:
        return False
    return bool(
        re.search(r"(?<!\d)100\s*\*", text)
        or re.search(r"\*\s*100(?!\d)", text)
    )


def _validate_formula_tokens(formula: dict[str, Any], issues: list[str]) -> None:
    formula_id = _clean_text(formula.get("formula_id")) or "<unknown>"
    declared = _declared_formula_fields(formula)
    scales = formula.get("input_scales")
    if not isinstance(scales, dict) or not scales:
        issues.append(f"{formula_id}: input_scales must be a non-empty mapping")
        scales = {}
    else:
        for field, scale in scales.items():
            if not _is_nonempty_string(field):
                issues.append(f"{formula_id}: input_scales contains a blank field name")
            if not _is_valid_input_scale(scale):
                issues.append(f"{formula_id}: input_scales for {field} must be one of {sorted(INPUT_SCALE_ALLOWED)}")
        for field in declared:
            if field not in scales:
                issues.append(f"{formula_id}: input_scales missing declared field {field}")
        for field in scales:
            if field not in declared:
                issues.append(f"{formula_id}: input_scales contains undeclared field {field}")
    allowed_functions = set(FORMULA_FUNCTIONS)
    expression = formula.get("formula_expression")
    if _is_nonempty_string(expression):
        tokens = _identifier_tokens(expression)
        undeclared = sorted(
            token
            for token in tokens
            if token not in declared and token not in allowed_functions and token.lower() not in FORMULA_RESERVED_TOKENS
        )
        if undeclared:
            issues.append(f"{formula_id}: formula_expression references undeclared tokens {undeclared}")

        if "weighted_mean(" in _clean_text(expression):
            expression_text = _clean_text(expression)
            visible_hundred_scale = _contains_visible_hundred_scale(expression_text)
            output_scale_family = _scale_family(formula.get("scale"))
            weighted_mean_seen = False
            for arg_block in _extract_weighted_mean_arguments(_clean_text(expression)):
                weighted_mean_seen = True
                arg_tokens = _identifier_tokens(arg_block)
                arg_families: set[str] = set()
                for token in arg_tokens:
                    if token in declared and token not in allowed_functions and token.lower() not in FORMULA_RESERVED_TOKENS:
                        scale = _clean_text(scales.get(token))
                        if scale not in NORMALIZED_INPUT_SCALES:
                            issues.append(
                                f"{formula_id}: weighted_mean argument {token} must use a normalized input scale, not {scale or 'missing'}"
                            )
                        family = _scale_family(scale)
                        if family in {"ratio", "hundred"}:
                            arg_families.add(family)
                if len(arg_families) > 1:
                    issues.append(
                        f"{formula_id}: weighted_mean arguments mix normalized scale families {sorted(arg_families)}; use one normalized family per weighted_mean"
                    )
                if output_scale_family == "hundred":
                    if arg_families and arg_families <= {"ratio"} and not visible_hundred_scale:
                        issues.append(
                            f"{formula_id}: output scale 0-100 with ratio-family weighted_mean arguments must visibly scale by 100"
                        )
                elif output_scale_family == "ratio":
                    if visible_hundred_scale:
                        issues.append(
                            f"{formula_id}: output scale ratio must not visibly scale ratio-family weighted_mean arguments by 100"
                        )

    hard_gate_rules = formula.get("hard_gate_rules")
    if _is_string_list(hard_gate_rules):
        gate_declarations = declared
        for rule in hard_gate_rules:
            condition = _clean_text(rule).split("->", 1)[0].strip()
            tokens = _identifier_tokens(condition)
            undeclared = sorted(
                token
                for token in tokens
                if token not in gate_declarations and token not in allowed_functions and token.lower() not in FORMULA_RESERVED_TOKENS
            )
            if undeclared:
                issues.append(f"{formula_id}: hard_gate_rules references undeclared tokens {undeclared}")


def _is_parseable_hard_gate_rule(rule: object) -> bool:
    text = _clean_text(rule)
    if not text or "->" not in text:
        return False
    lhs, rhs = [part.strip() for part in text.split("->", 1)]
    if not lhs or not rhs:
        return False
    comparison_tokens = ("==", "!=", ">=", "<=", ">", "<", " in ", " not in ")
    threshold_tokens = (
        "below threshold",
        "above threshold",
        "is null",
        "is not null",
        "missing",
        "at least",
        "at most",
    )
    return any(op in lhs for op in comparison_tokens) or any(token in lhs.lower() for token in threshold_tokens)


def load_numeric_formula_registry(path: Path | str | None = None) -> dict[str, Any]:
    registry_path = Path(path) if path is not None else NUMERIC_FORMULA_REGISTRY_PATH
    raw = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"numeric_formula_registry: expected mapping at top level in {registry_path}")
    return raw


def _validate_top_level_keys(registry: dict[str, Any], issues: list[str]) -> None:
    missing = sorted(TOP_LEVEL_REQUIRED_KEYS - set(registry))
    if missing:
        issues.append(f"numeric_formula_registry: missing top-level keys {missing}")


def _validate_required_formula_fields(registry: dict[str, Any], issues: list[str]) -> list[str]:
    raw = registry.get("required_formula_fields")
    if not isinstance(raw, list) or not all(_is_nonempty_string(item) for item in raw):
        issues.append("numeric_formula_registry: required_formula_fields must be a non-empty list of strings")
        return []

    required_fields = [_clean_text(item) for item in raw if _clean_text(item)]
    required_set = set(required_fields)
    missing = sorted(BASE_REQUIRED_FORMULA_FIELDS - required_set)
    if missing:
        issues.append(f"numeric_formula_registry: required_formula_fields missing baseline fields {missing}")

    computation_fields = {"formula_expression", "implementation_function"}
    missing_computation = sorted(computation_fields - required_set)
    if missing_computation:
        issues.append(f"numeric_formula_registry: required_formula_fields missing computation fields {missing_computation}")

    return required_fields


def _validate_score_families(registry: dict[str, Any], issues: list[str]) -> dict[str, bool]:
    raw = registry.get("score_families")
    if not isinstance(raw, dict) or not raw:
        issues.append("numeric_formula_registry: score_families must be a non-empty mapping")
        return {}

    families: dict[str, bool] = {}
    for family_name, family_payload in raw.items():
        family = _clean_text(family_name)
        if not family:
            issues.append("numeric_formula_registry: score_families contains a blank family name")
            continue
        if not isinstance(family_payload, dict):
            issues.append(f"numeric_formula_registry: score_family {family} must map to a dictionary")
            continue
        for key in ("comparable_only_within_family", "higher_is_better"):
            if key not in family_payload:
                issues.append(f"numeric_formula_registry: score_family {family} missing {key}")
            elif not _is_bool(family_payload.get(key)):
                issues.append(f"numeric_formula_registry: score_family {family} has non-boolean {key}")
        if _is_bool(family_payload.get("higher_is_better")):
            families[family] = bool(family_payload.get("higher_is_better"))
    return families


def _validate_hard_gate_policy(registry: dict[str, Any], issues: list[str]) -> None:
    raw = registry.get("hard_gate_policy")
    if not isinstance(raw, dict):
        issues.append("numeric_formula_registry: hard_gate_policy must be a mapping")
        return
    missing = sorted(HARD_GATE_POLICY_REQUIRED_KEYS - set(raw))
    if missing:
        issues.append(f"numeric_formula_registry: hard_gate_policy missing keys {missing}")
    for key in HARD_GATE_POLICY_REQUIRED_KEYS & set(raw):
        if not _is_bool(raw.get(key)):
            issues.append(f"numeric_formula_registry: hard_gate_policy {key} must be boolean")


def _validate_thresholds(formula: dict[str, Any], issues: list[str]) -> None:
    thresholds = formula.get("thresholds")
    if not isinstance(thresholds, dict) or not thresholds:
        issues.append(f"{formula.get('formula_id', '<unknown>')}: thresholds must be a non-empty mapping")
        return
    for key in ("low", "medium", "high"):
        if key not in thresholds:
            issues.append(f"{formula.get('formula_id', '<unknown>')}: thresholds missing {key}")
        elif not isinstance(thresholds.get(key), (int, float)):
            issues.append(f"{formula.get('formula_id', '<unknown>')}: thresholds {key} must be numeric")
    if all(isinstance(thresholds.get(key), (int, float)) for key in ("low", "medium", "high")):
        low = float(thresholds["low"])
        medium = float(thresholds["medium"])
        high = float(thresholds["high"])
        if not (low <= medium <= high):
            issues.append(f"{formula.get('formula_id', '<unknown>')}: thresholds must be ordered low <= medium <= high on the numeric axis")


def _validate_formula(formula: dict[str, Any], required_fields: list[str], score_families: dict[str, bool], issues: list[str]) -> None:
    formula_id = _clean_text(formula.get("formula_id")) or "<unknown>"

    missing = [field for field in required_fields if field not in formula and field not in {"formula_expression", "implementation_function"}]
    if missing:
        issues.append(f"{formula_id}: missing required fields {sorted(missing)}")

    if not _is_nonempty_string(formula.get("formula_id")):
        issues.append(f"{formula_id}: formula_id must be a non-empty string")
    if not _is_nonempty_string(formula.get("formula_version")):
        issues.append(f"{formula_id}: formula_version must be a non-empty string")
    if not _is_nonempty_string(formula.get("output_field")):
        issues.append(f"{formula_id}: output_field must be a non-empty string")

    score_family = _clean_text(formula.get("score_family"))
    if not score_family:
        issues.append(f"{formula_id}: score_family must be declared")
    elif score_family not in score_families:
        issues.append(f"{formula_id}: score_family {score_family} is not declared in score_families")

    if "higher_is_better" not in formula:
        issues.append(f"{formula_id}: higher_is_better must be declared")
    elif not _is_bool(formula.get("higher_is_better")):
        issues.append(f"{formula_id}: higher_is_better must be boolean")

    if not _is_nonempty_string(formula.get("decision_role")):
        issues.append(f"{formula_id}: decision_role must be declared")

    has_expression = _is_nonempty_string(formula.get("formula_expression"))
    has_implementation = _is_nonempty_string(formula.get("implementation_function"))
    if not has_expression:
        issues.append(f"{formula_id}: formula_expression must be present")
    elif not _looks_like_formula_expression(formula.get("formula_expression")):
        issues.append(f"{formula_id}: formula_expression must look executable, not descriptive prose")
    if not has_implementation:
        issues.append(f"{formula_id}: implementation_function must be present")

    inputs = formula.get("inputs")
    if not isinstance(inputs, list) or not all(_is_nonempty_string(item) for item in inputs):
        issues.append(f"{formula_id}: inputs must be a non-empty list of strings")
        input_names: list[str] = []
    else:
        input_names = [_clean_text(item) for item in inputs if _clean_text(item)]

    for group_key in EXEMPT_INPUT_GROUP_KEYS:
        if group_key in formula and not _is_string_list(formula.get(group_key)):
            issues.append(f"{formula_id}: {group_key} must be a list of non-empty strings when present")

    exempt_inputs: set[str] = set()
    for group_key in EXEMPT_INPUT_GROUP_KEYS:
        group_values = formula.get(group_key)
        if _is_string_list(group_values):
            exempt_inputs.update(_clean_text(item) for item in group_values if _clean_text(item))

    polarity = formula.get("component_polarity")
    if not isinstance(polarity, dict) or not polarity:
        issues.append(f"{formula_id}: component_polarity must be a non-empty mapping")
    else:
        for component in input_names:
            if component in exempt_inputs:
                continue
            if component not in polarity:
                issues.append(f"{formula_id}: component_polarity missing input component {component}")
        for component, component_polarity in polarity.items():
            if not _is_nonempty_string(component):
                issues.append(f"{formula_id}: component_polarity contains a blank component name")
            if _clean_text(component_polarity) not in COMPONENT_POLARITY_ALLOWED:
                issues.append(f"{formula_id}: component_polarity for {component} must be one of {sorted(COMPONENT_POLARITY_ALLOWED)}")

    hard_gate_rules = formula.get("hard_gate_rules")
    if hard_gate_rules is not None:
        if not _is_string_list(hard_gate_rules):
            issues.append(f"{formula_id}: hard_gate_rules must be a list of non-empty strings when present")
        elif any(not _is_parseable_hard_gate_rule(rule) for rule in hard_gate_rules):
            issues.append(f"{formula_id}: hard_gate_rules must be parseable rule strings of the form 'condition -> action'")

    allowed_artifacts = formula.get("allowed_artifacts")
    if not _is_string_list(allowed_artifacts):
        issues.append(f"{formula_id}: allowed_artifacts must be a non-empty list of strings")

    for source_key in ("allowed_source_artifacts", "forbidden_source_artifacts", "forbidden_source_artifacts_for_strict"):
        if source_key in formula and not _is_string_list(formula.get(source_key)):
            issues.append(f"{formula_id}: {source_key} must be a list of non-empty strings when present")

    if "allowed_source_artifacts" in formula and "forbidden_source_artifacts" in formula:
        allowed = {_clean_text(item) for item in formula.get("allowed_source_artifacts", []) if _clean_text(item)}
        forbidden = {_clean_text(item) for item in formula.get("forbidden_source_artifacts", []) if _clean_text(item)}
        overlap = sorted(allowed & forbidden)
        if overlap:
            issues.append(f"{formula_id}: forbidden_source_artifacts overlaps allowed_source_artifacts {overlap}")

    if "allowed_source_artifacts" in formula and "forbidden_source_artifacts_for_strict" in formula:
        allowed = {_clean_text(item) for item in formula.get("allowed_source_artifacts", []) if _clean_text(item)}
        forbidden = {_clean_text(item) for item in formula.get("forbidden_source_artifacts_for_strict", []) if _clean_text(item)}
        overlap = sorted(allowed & forbidden)
        if overlap:
            issues.append(f"{formula_id}: forbidden_source_artifacts_for_strict overlaps allowed_source_artifacts {overlap}")

    _validate_thresholds(formula, issues)

    if not _is_string_list(formula.get("monotonicity_expectations", [])):
        if "monotonicity_expectations" in formula:
            issues.append(f"{formula_id}: monotonicity_expectations must be a list of non-empty strings when present")

    _validate_formula_tokens(formula, issues)

    if score_family in score_families and _is_bool(formula.get("higher_is_better")):
        family_higher = score_families[score_family]
        if bool(formula.get("higher_is_better")) != family_higher:
            issues.append(
                f"{formula_id}: higher_is_better must match score_family {score_family} ({family_higher})"
            )


def validate_numeric_formula_registry(registry: dict[str, Any]) -> list[str]:
    issues: list[str] = []
    if not isinstance(registry, dict):
        return ["numeric_formula_registry: registry must be a mapping"]

    _validate_top_level_keys(registry, issues)
    required_fields = _validate_required_formula_fields(registry, issues)
    score_families = _validate_score_families(registry, issues)
    _validate_hard_gate_policy(registry, issues)

    raw_formulas = registry.get("formulas")
    if not isinstance(raw_formulas, list) or not raw_formulas:
        issues.append("numeric_formula_registry: formulas must be a non-empty list")
        return issues

    formula_ids: set[str] = set()
    output_field_artifacts: dict[str, list[tuple[str, set[str]]]] = {}
    for formula in raw_formulas:
        if not isinstance(formula, dict):
            issues.append("numeric_formula_registry: each formula entry must be a mapping")
            continue
        formula_id = _clean_text(formula.get("formula_id"))
        output_field = _clean_text(formula.get("output_field"))
        if formula_id:
            if formula_id in formula_ids:
                issues.append(f"numeric_formula_registry: duplicate formula_id {formula_id}")
            formula_ids.add(formula_id)
        if output_field:
            artifact_list = formula.get("allowed_artifacts")
            artifact_set = {_clean_text(item) for item in artifact_list or [] if _clean_text(item)}
            output_field_artifacts.setdefault(output_field, []).append((formula_id or "<unknown>", artifact_set))
        _validate_formula(formula, required_fields, score_families, issues)

    for output_field, entries in output_field_artifacts.items():
        if len(entries) < 2:
            continue
        for idx, (formula_a, artifacts_a) in enumerate(entries):
            for formula_b, artifacts_b in entries[idx + 1 :]:
                overlap = sorted(artifacts_a & artifacts_b)
                if overlap:
                    issues.append(
                        f"numeric_formula_registry: duplicate output_field {output_field} overlaps allowed_artifacts for {formula_a} and {formula_b} on {overlap}"
                    )
                    break

    return issues


def validate_numeric_formula_registry_file(path: Path | str | None = None) -> list[str]:
    return validate_numeric_formula_registry(load_numeric_formula_registry(path))


def copy_numeric_formula_registry(path: Path | str | None = None) -> dict[str, Any]:
    return deepcopy(load_numeric_formula_registry(path))
