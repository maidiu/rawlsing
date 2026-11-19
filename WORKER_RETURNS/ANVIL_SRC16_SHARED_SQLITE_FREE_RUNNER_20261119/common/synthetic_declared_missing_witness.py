#!/usr/bin/env python3
"""Synthetic positive/refusal witnesses for declared-missing overlay mapping."""
from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from declared_missing_mapping import (  # noqa: E402
    BASE_CONFIG_CANONICAL_SHA256,
    BASE_CONFIG_FILE_SHA256,
    SOURCE_SHA256,
    build_overlay,
)

CAND = Path(os.environ["ANVIL_CANDIDATE_TREE"])
CFG = Path(os.environ.get(
    "ANVIL_SRC16_CONFIG",
    CAND / "rawlsing_next/source_configuration/data/SRC16/SRC16.source.config.json",
)).absolute()


def main() -> int:
    config = json.loads(CFG.read_text())
    census = {
        "source_id": "SRC16",
        "source_sha256": SOURCE_SHA256,
        "source_config_file_sha256": BASE_CONFIG_FILE_SHA256,
        "source_config_canonical_sha256": BASE_CONFIG_CANONICAL_SHA256,
        "census": {
            "unresolved_slots": [{
                "family": "response",
                "ordinal": 11,
                "name": "age",
                "unresolved_count": 4,
                "tokens": [
                    {"token": "-99", "missing_state": "PhysicalMissingState.FORMAT_USER_MISSING_RANGE",
                     "source_missing_declaration": "{'kind': 'range', 'lo': -100.0, 'hi': -10.0}", "count": 2},
                    {"token": "-97", "missing_state": "PhysicalMissingState.FORMAT_USER_MISSING_RANGE",
                     "source_missing_declaration": "{'kind': 'range', 'lo': -100.0, 'hi': -10.0}", "count": 1},
                    {"token": "18", "missing_state": "PhysicalMissingState.OBSERVED_STORAGE_VALUE",
                     "source_missing_declaration": "None", "count": 1},
                ],
            }],
        },
    }
    overlay, summary = build_overlay(
        census, config,
        config_file_sha256=BASE_CONFIG_FILE_SHA256,
        config_canonical_sha256=BASE_CONFIG_CANONICAL_SHA256,
        census_sha256=hashlib.sha256(b"synthetic-census").hexdigest(),
    )
    rules = overlay["rules"][0]["values"] if overlay["rules"] else []
    checks = {
        "declared_range_token_positive_yes": (
            len(rules) == 2
            and all(v["response_state"] == "MISSING" for v in rules)
            and all(v["missing_state"] == "FORMAT_USER_MISSING_RANGE" for v in rules)
        ),
        "observed_token_refused_as_substantive_yes": (
            summary["observed_storage_cells_left_unresolved"] == 1
            and not any(v["raw_value"] == 18.0 for v in rules)
        ),
        "observed_not_dropped_yes": summary["observed_storage_cells_left_unresolved"] == 1,
        "range_cell_count_yes": summary["declared_missing_range_cells"] == 3,
        "no_authority_expansion_yes": overlay["authority_expansion"] is False,
        "private_overlay_only_yes": overlay["private_data"] is True,
        "provenance_pinned_yes": (
            overlay["base_config_file_sha256"] == BASE_CONFIG_FILE_SHA256
            and overlay["census_file_sha256"] == hashlib.sha256(b"synthetic-census").hexdigest()
        ),
    }
    status = "SYNTHETIC_DECLARED_MISSING_WITNESS_PASS" if all(checks.values()) else "SYNTHETIC_DECLARED_MISSING_WITNESS_FAILED"
    print(json.dumps({
        "status": status,
        "checks": checks,
        "rule_count": len(rules),
        "declared_missing_cells": summary["declared_missing_range_cells"],
        "observed_cells_left_unresolved": summary["observed_storage_cells_left_unresolved"],
        "raw_tokens_published": False,
        "source_read_performed": False,
    }, sort_keys=True))
    return 0 if all(checks.values()) else 2


if __name__ == "__main__":
    raise SystemExit(main())
