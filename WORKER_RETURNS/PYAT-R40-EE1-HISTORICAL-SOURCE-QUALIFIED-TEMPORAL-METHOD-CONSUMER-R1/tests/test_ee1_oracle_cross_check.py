"""C6 independent comparison oracle: wrong-source and wrong-clock crossovers
are caught independently of the machinery under test."""
from __future__ import annotations

import ast
from pathlib import Path

import ee1_fixtures as F
import ee1_oracle
from ee1_temporal_owner import compare_periods

SCENARIOS = [
    ("S1", F.comparable_pair(), "COMPARABLE"),
    ("S2", F.mixed_family(), "NONCOMPARABLE_SOURCE_FAMILY"),
    ("S3", F.mixed_country(), "NONCOMPARABLE_COUNTRY"),
    ("S4", F.population_change(), "NONCOMPARABLE_POPULATION_OR_ESTIMAND"),
    ("S5", F.future_rule(), "FUTURE_RULE_AT_HISTORICAL_AS_OF"),
    ("S6", F.annual_gap(), "UNKNOWN_GAP"),
]


def test_oracle_and_bridge_agree_on_frozen_scenarios(tmp_path):
    for label, periods, expected in SCENARIOS:
        oracle_state = ee1_oracle.oracle_verdict(periods, F.ASOF)
        assert oracle_state == expected, label
        verdict = compare_periods(periods, F.ASOF, tmp_path / label)
        assert verdict["state"] in ee1_oracle.BRIDGE_FAMILY[expected], \
            (label, verdict["state"])


def test_oracle_module_is_import_independent():
    source = Path(ee1_oracle.__file__).read_text()
    tree = ast.parse(source)
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
    forbidden = [name for name in imported
                 if name.startswith(("data", "rawlsing_next", "ee1_"))]
    assert forbidden == []
