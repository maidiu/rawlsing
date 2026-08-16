#!/usr/bin/env python3
"""Registry-driven association lane classifier.

Loads association_lane_registry.yaml at startup and provides
scoped lane/publishability/authority classification.
Rules are filtered by source, wave, and country_code at load time.
Precedence: exact > prefix > regex.

``classify()`` remains available for non-executable probing. Executable
consumers must use ``classify_required()`` so missing governed association
authority cannot fall through to a hard-coded classifier.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

from data.ddm_build_copy.ddm_survey_identity import (
    canonical_country_code,
    canonical_family_key,
    require_survey_identity,
    wave_ordinal,
)
from data.ddm_build_copy.ddm_v550j_registry_contract import RegistryAuthorityError

DEFAULT_REGISTRY_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "ddm_registries" / "association_lane_registry.yaml"
)


@dataclass(frozen=True)
class RegistryRule:
    rule_id: str
    source: str
    wave_start: int | None
    wave_end: int | None
    country_code: str
    match_type: str
    var_code: str | None
    var_code_pattern: str | None
    association_lane: str
    association_lane_publishability: str
    authority_source: str
    authority_status: str
    notes: str | None = None


@dataclass(frozen=True)
class RegistryResult:
    rule_id: str
    lane: str
    publishability: str
    match_type: str
    authority_source: str
    authority_status: str


class AssociationLaneRegistry:
    """Runtime registry classifier.

    Loads association_lane_registry.yaml once, then provides
    classify() for individual var_codes within a source/wave/country scope.
    Thread-safe for read-only classify() calls after load().
    """

    def __init__(self, path: str | Path | None = None) -> None:
        self._path = Path(path) if path else DEFAULT_REGISTRY_PATH
        self._all_rules: list[RegistryRule] = []
        self._loaded = False

    @property
    def path(self) -> Path:
        return self._path

    def load(self) -> None:
        if not self._path.exists():
            raise RegistryAuthorityError(
                "association_lane_registry_missing",
                f"Association lane registry not found: {self._path}",
                authority_name="V550J association lane registry",
                path=self._path,
            )
        with open(self._path, "r") as f:
            data = yaml.safe_load(f)
        if not isinstance(data, dict):
            raise RegistryAuthorityError(
                "association_lane_registry_invalid",
                f"Association lane registry must be a mapping: {self._path}",
                authority_name="V550J association lane registry",
                path=self._path,
            )
        raw_rules = data.get("rules", [])
        if not isinstance(raw_rules, list):
            raise RegistryAuthorityError(
                "association_lane_registry_invalid",
                f"Association lane registry rules must be a list: {self._path}",
                authority_name="V550J association lane registry",
                path=self._path,
            )
        self._all_rules = []
        for index, rule in enumerate(raw_rules):
            if not isinstance(rule, dict):
                raise RegistryAuthorityError(
                    "association_lane_registry_rule_invalid",
                    f"Association lane registry rule {index} is not a mapping",
                    authority_name="V550J association lane registry",
                    path=self._path,
                )
            rule_id = str(rule.get("rule_id", "")).strip()
            lane = str(rule.get("association_lane", "")).strip()
            publishability = str(rule.get("association_lane_publishability", "")).strip()
            if not rule_id or not lane or not publishability:
                raise RegistryAuthorityError(
                    "association_lane_registry_rule_incomplete",
                    (
                        f"Association lane registry rule {index} is missing rule_id, "
                        "association_lane, or association_lane_publishability"
                    ),
                    authority_name="V550J association lane registry",
                    path=self._path,
                )
            self._all_rules.append(
                RegistryRule(
                    rule_id=rule_id,
                    source=str(rule.get("source", "")),
                    wave_start=_maybe_int(rule.get("wave_start")),
                    wave_end=_maybe_int(rule.get("wave_end")),
                    country_code=str(rule.get("country_code", "")).upper(),
                    match_type=str(rule.get("match_type", "exact")),
                    var_code=rule.get("var_code"),
                    var_code_pattern=rule.get("var_code_pattern"),
                    association_lane=lane,
                    association_lane_publishability=publishability,
                    authority_source=str(rule.get("authority_source", "registry")),
                    authority_status=str(rule.get("authority_status", "manual_registry_rule")),
                    notes=rule.get("notes"),
                )
            )
        self._loaded = True

    def rules_for_scope(self, source: str, wave: str | int, country_code: str) -> list[RegistryRule]:
        if not self._loaded:
            self.load()
        identity = require_survey_identity(
            source,
            wave,
            country_code,
            require_country=True,
        )
        ordinal = wave_ordinal(identity.source_key, identity.canonical_wave)
        if ordinal is None:
            return []
        return [
            r
            for r in self._all_rules
            if _rule_applies(r, identity.source_key, ordinal, identity.country_code)
        ]

    def classify(
        self, var_code: str, source: str, wave: str | int, country_code: str
    ) -> RegistryResult | None:
        """Return RegistryResult for var_code, or None if no registry rule matches.

        Precedence: exact > prefix > regex. Falls out on first match within a type.
        """
        code = str(var_code).strip().upper()
        if not code:
            return None
        rules = self.rules_for_scope(source, wave, country_code)
        if not rules:
            return None

        # Pass 1: exact matches (highest precedence)
        for r in rules:
            if r.match_type == "exact" and r.var_code:
                if r.var_code.upper() == code:
                    return _result_from_rule(r, "exact")

        # Pass 2: prefix matches
        for r in rules:
            if r.match_type == "prefix" and r.var_code_pattern:
                if code.startswith(r.var_code_pattern.upper()):
                    return _result_from_rule(r, "prefix")

        # Pass 3: regex matches
        for r in rules:
            if r.match_type == "regex" and r.var_code_pattern:
                try:
                    if re.match(r.var_code_pattern, code):
                        return _result_from_rule(r, "regex")
                except re.error:
                    continue

        return None

    def classify_required(
        self, var_code: str, source: str, wave: str | int, country_code: str
    ) -> RegistryResult:
        """Return governed classification or fail closed when authority is absent."""
        result = self.classify(var_code, source, wave, country_code)
        if result is None:
            raise RegistryAuthorityError(
                "association_lane_authority_missing",
                (
                    "No governed association-lane rule matches "
                    f"var_code={str(var_code).strip()} source={source} wave={wave} "
                    f"country_code={country_code}"
                ),
                authority_name="V550J association lane registry",
                path=self._path,
            )
        return result


def _rule_applies(rule: RegistryRule, source_key: str, wave_int: int, country: str) -> bool:
    rule_source = canonical_family_key(rule.source)
    if rule.source != "*" and rule_source != source_key:
        return False
    rule_country = canonical_country_code(rule.country_code)
    if rule.country_code != "*" and rule_country != country:
        return False
    if rule.wave_start is not None and wave_int < rule.wave_start:
        return False
    if rule.wave_end is not None and wave_int > rule.wave_end:
        return False
    return True


def _result_from_rule(rule: RegistryRule, match_type: str) -> RegistryResult:
    return RegistryResult(
        rule_id=rule.rule_id,
        lane=rule.association_lane,
        publishability=rule.association_lane_publishability,
        match_type=match_type,
        authority_source=rule.authority_source,
        authority_status=rule.authority_status,
    )


def _maybe_int(v: Any) -> int | None:
    if v is None:
        return None
    try:
        return int(str(v).strip())
    except (ValueError, TypeError):
        return None
