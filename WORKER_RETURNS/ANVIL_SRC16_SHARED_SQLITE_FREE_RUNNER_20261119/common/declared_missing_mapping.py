#!/usr/bin/env python3
"""Build a private, source-neutral overlay for declared source-missing ranges.

The input is the already completed aggregate census.  This code never opens the
source, never emits raw tokens, and never promotes an observed storage value to
substantive merely because it exists.

Only `FORMAT_USER_MISSING_RANGE` cells are materialized, using the exact
declared range and the existing physical missing state.  They retain the raw
source token and are assigned the existing typed `MISSING` response state.
Observed storage tokens remain explicitly unresolved for a later decision.
"""
from __future__ import annotations

import argparse
import ast
import copy
import hashlib
import json
import os
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "ANVIL_SRC16_DECLARED_MISSING_OVERLAY@1"
BASE_CONFIG_FILE_SHA256 = "1106de3e086032f5ac0b26fee0b56a147722399c80ac2841b70f0b851dea93b7"
BASE_CONFIG_CANONICAL_SHA256 = "c26e8e71afbc629a9f19708cedb7b38cc2ba3cefb9ac53f11e0608044e64b534"
SOURCE_SHA256 = "e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204"
SOURCE_ID = "SRC16"
RANGE_STATE = "PhysicalMissingState.FORMAT_USER_MISSING_RANGE"
OBSERVED_STATE = "PhysicalMissingState.OBSERVED_STORAGE_VALUE"


class MappingRefusal(RuntimeError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _declaration(value: Any) -> Mapping[str, Any]:
    if isinstance(value, str):
        try:
            value = ast.literal_eval(value)
        except (ValueError, SyntaxError) as exc:
            raise MappingRefusal("MISSING_DECLARATION_NOT_PARSEABLE") from exc
    if not isinstance(value, Mapping) or value.get("kind") != "range":
        raise MappingRefusal("UNSUPPORTED_MISSING_DECLARATION")
    if not {"lo", "hi"} <= set(value):
        raise MappingRefusal("MISSING_RANGE_BOUNDS_ABSENT")
    return {str(k): value[k] for k in sorted(value)}


def _numeric_token(token: str) -> float:
    try:
        value = float(Decimal(str(token)))
    except (InvalidOperation, ValueError) as exc:
        raise MappingRefusal("SOURCE_RANGE_TOKEN_NOT_NUMERIC") from exc
    if value != value or value in (float("inf"), float("-inf")):
        raise MappingRefusal("SOURCE_RANGE_TOKEN_NOT_FINITE")
    return value


def _base_slots(config: Mapping[str, Any]) -> dict[tuple[int, str], Mapping[str, Any]]:
    result = {}
    for section in config.get("response_slots", ()):
        slot = section["slot"]
        result[(int(slot["ordinal"]), str(slot["name"]))] = section
    return result


def build_overlay(
    census: Mapping[str, Any],
    config: Mapping[str, Any],
    *,
    config_file_sha256: str,
    config_canonical_sha256: str,
    census_sha256: str,
) -> tuple[dict[str, Any], dict[str, int]]:
    if census.get("source_id") != SOURCE_ID:
        raise MappingRefusal("CENSUS_SOURCE_ID_MISMATCH")
    if census.get("source_sha256") != SOURCE_SHA256:
        raise MappingRefusal("CENSUS_SOURCE_SHA_MISMATCH")
    if census.get("source_config_file_sha256") != config_file_sha256:
        raise MappingRefusal("CENSUS_CONFIG_FILE_MISMATCH")
    if census.get("source_config_canonical_sha256") != config_canonical_sha256:
        raise MappingRefusal("CENSUS_CONFIG_CANONICAL_MISMATCH")
    if config_file_sha256 != BASE_CONFIG_FILE_SHA256:
        raise MappingRefusal("BASE_CONFIG_FILE_NOT_PINNED")
    if config_canonical_sha256 != BASE_CONFIG_CANONICAL_SHA256:
        raise MappingRefusal("BASE_CONFIG_CANONICAL_NOT_PINNED")

    base = _base_slots(config)
    rules: dict[tuple[int, str], list[dict[str, Any]]] = {}
    range_cells = 0
    observed_cells = 0
    ignored_cells = 0
    range_tokens = 0
    for slot_report in census["census"]["unresolved_slots"]:
        if slot_report.get("family") != "response":
            ignored_cells += int(slot_report.get("unresolved_count", 0))
            continue
        key = (int(slot_report["ordinal"]), str(slot_report["name"]))
        section = base.get(key)
        if section is None:
            raise MappingRefusal("CENSUS_SLOT_NOT_IN_PINNED_CONFIG")
        occurrences = section.get("values", [{}])[0].get("occurrences")
        if not occurrences:
            raise MappingRefusal("SLOT_OCCURRENCE_TEMPLATE_ABSENT")
        for token in slot_report.get("tokens", ()):
            state = str(token.get("missing_state"))
            count = int(token.get("count", 0))
            if state == RANGE_STATE:
                declaration = _declaration(token.get("source_missing_declaration"))
                raw_value = _numeric_token(str(token.get("token")))
                rule = {
                    "raw_value": raw_value,
                    "missing_state": "FORMAT_USER_MISSING_RANGE",
                    "source_missing_declaration": declaration,
                    "response_state": "MISSING",
                    "occurrences": copy.deepcopy(occurrences),
                    "canonical_value": None,
                    "transform_authority_ref": None,
                    "extra_authority_refs": [],
                }
                rules.setdefault(key, []).append(rule)
                range_cells += count
                range_tokens += 1
            elif state == OBSERVED_STATE:
                # Deliberately no rule: observed tokens are not made substantive.
                observed_cells += count
            else:
                ignored_cells += count

    overlay = {
        "schema": SCHEMA,
        "source_id": SOURCE_ID,
        "source_sha256": SOURCE_SHA256,
        "base_config_file_sha256": config_file_sha256,
        "base_config_canonical_sha256": config_canonical_sha256,
        "census_file_sha256": census_sha256,
        "authority_expansion": False,
        "source_reopened": False,
        "respondent_records_emitted": False,
        "private_data": True,
        "rules": [
            {
                "slot": {"ordinal": key[0], "name": key[1]},
                "values": values,
            }
            for key, values in sorted(rules.items())
        ],
        "totals": {
            "declared_missing_range_cells": range_cells,
            "declared_missing_range_rules": range_tokens,
            "observed_storage_cells_left_unresolved": observed_cells,
            "other_cells_left_untouched": ignored_cells,
        },
    }
    summary = {
        "declared_missing_range_cells": range_cells,
        "declared_missing_range_rules": range_tokens,
        "observed_storage_cells_left_unresolved": observed_cells,
        "other_cells_left_untouched": ignored_cells,
        "slots_with_rules": len(rules),
    }
    return overlay, summary


def replay(overlay: Mapping[str, Any], census: Mapping[str, Any]) -> dict[str, Any]:
    by_slot = {
        (int(section["slot"]["ordinal"]), str(section["slot"]["name"])): section
        for section in overlay.get("rules", ())
    }
    covered = 0
    remaining = 0
    for slot_report in census["census"]["unresolved_slots"]:
        key = (int(slot_report["ordinal"]), str(slot_report["name"]))
        section = by_slot.get(key)
        if section is None:
            remaining += int(slot_report.get("unresolved_count", 0))
            continue
        # Count each exact range token as covered by its exact rule key.
        rule_keys = set()
        for value in section.get("values", ()):
            from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key
            from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
            rule_keys.add(physical_value_binding_key(
                value["raw_value"],
                PhysicalMissingState(value["missing_state"]),
                value.get("source_missing_declaration"),
            ))
        for token in slot_report.get("tokens", ()):
            count = int(token.get("count", 0))
            if str(token.get("missing_state")) == RANGE_STATE:
                raw_value = _numeric_token(str(token.get("token")))
                from rawlsing_next.pre553_source_backed_c11_facade import physical_value_binding_key
                from rawlsing_next.pre553_physical_decoder import PhysicalMissingState
                key_value = physical_value_binding_key(
                    raw_value,
                    PhysicalMissingState.FORMAT_USER_MISSING_RANGE,
                    _declaration(token.get("source_missing_declaration")),
                )
                if key_value in rule_keys:
                    covered += count
                else:
                    remaining += count
            else:
                remaining += count
    return {
        "covered_declared_missing_range_cells": covered,
        "remaining_unresolved_cells": remaining,
        "expected_missing_range_cells": 40592,
        "expected_observed_cells": 18105,
        "coverage_replay_passed": covered == 40592 and remaining == 18105,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--census", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--summary", type=Path, required=True)
    args = parser.parse_args()
    try:
        census_path = args.census.absolute()
        config_path = args.config.absolute()
        census = json.loads(census_path.read_text())
        config = json.loads(config_path.read_text())
        overlay, summary = build_overlay(
            census,
            config,
            config_file_sha256=_sha(config_path),
            config_canonical_sha256=BASE_CONFIG_CANONICAL_SHA256,
            census_sha256=_sha(census_path),
        )
        replay_result = replay(overlay, census)
        if not replay_result["coverage_replay_passed"]:
            raise MappingRefusal("COVERAGE_REPLAY_FAILED")
        args.out = args.out.absolute()
        args.out.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        args.out.write_text(json.dumps(overlay, indent=2, sort_keys=True) + "\n")
        os.chmod(args.out, 0o600)
        safe = {
            "schema": "ANVIL_SRC16_DECLARED_MISSING_OVERLAY_SUMMARY@1",
            "overlay_sha256": _sha(args.out),
            "overlay_bytes": args.out.stat().st_size,
            "base_config_file_sha256": BASE_CONFIG_FILE_SHA256,
            "base_config_canonical_sha256": BASE_CONFIG_CANONICAL_SHA256,
            "census_sha256": _sha(census_path),
            **summary,
            **replay_result,
            "observed_value_decision_class": "PhysicalMissingState.OBSERVED_STORAGE_VALUE",
            "observed_value_count": replay_result["expected_observed_cells"],
            "source_reopened": False,
            "raw_tokens_published": False,
            "authority_expansion": False,
        }
        args.summary = args.summary.absolute()
        args.summary.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(safe, indent=2, sort_keys=True) + "\n")
        os.chmod(args.summary, 0o600)
        print(json.dumps(safe, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "status": "OVERLAY_REFUSED",
            "code": getattr(exc, "code", type(exc).__name__),
            "raw_tokens_published": False,
        }, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
