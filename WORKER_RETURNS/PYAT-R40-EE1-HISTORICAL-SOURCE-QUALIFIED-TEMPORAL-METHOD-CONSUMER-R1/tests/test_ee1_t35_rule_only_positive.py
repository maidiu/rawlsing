"""C0 custody + C1 T35 rule-only institutional change (accepted consumer)."""
from __future__ import annotations

import subprocess
from pathlib import Path

import ee1_fixtures as F
from ee1_historical_consumer import accepted_epoch_facts, build_comparison_product
from ee1_paths import REPO, STAGED_WORLD
from ee1_temporal_owner import delta_observation_rows, probe_or_authorized_delta

UPSTREAM = "WORKER_RETURNS/PYAT-R35-T35-TEMPORAL-WORLD-POSITIVE-R1/runtime"
COMMIT = "8bfb145f7da8a2d5e6c0913919721ad4085b5d85"

STAGED_MAP = {
    "bootstrap.py": f"{UPSTREAM}/bootstrap.py",
    "two_epoch_world.py": f"{UPSTREAM}/two_epoch_world.py",
    "n8e_sourcefree_comparator.py": f"{UPSTREAM}/n8e_sourcefree_comparator.py",
    "selected/e05_n9_selected_world_adapter.py": f"{UPSTREAM}/selected/e05_n9_selected_world_adapter.py",
    "selected/product/world.py": f"{UPSTREAM}/selected/product/world.py",
    "selected/product/service.py": f"{UPSTREAM}/selected/product/service.py",
    "selected/product/empirical.py": f"{UPSTREAM}/selected/product/empirical.py",
    "selected/product/nonparent.py": f"{UPSTREAM}/selected/product/nonparent.py",
    "selected/product/scenario.py": f"{UPSTREAM}/selected/product/scenario.py",
    "selected/native_extra/pre553_hq297_n9c_two_field_reader.py": f"{UPSTREAM}/selected/native_extra/pre553_hq297_n9c_two_field_reader.py",
    "selected/native_extra/pre553_n9_n10w_progressive_candidate.py": f"{UPSTREAM}/selected/native_extra/pre553_n9_n10w_progressive_candidate.py",
    "selected/fixtures/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json": f"{UPSTREAM}/selected/fixtures/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json",
}

EXPECTED_STEPS = [
    {"denominator": 32, "cells": {"0": 14, "1": 18}},
    {"denominator": 16, "cells": {"0": 6, "1": 10}},
    {"denominator": 8, "cells": {"0": 2, "1": 6}},
]


def test_staged_world_files_match_upstream_commit_bytes():
    for staged_rel, upstream in STAGED_MAP.items():
        staged = (STAGED_WORLD / staged_rel).read_bytes()
        upstream_bytes = subprocess.run(
            ["git", "-C", str(REPO), "cat-file", "blob", f"{COMMIT}:{upstream}"],
            capture_output=True, check=True).stdout
        assert staged == upstream_bytes, staged_rel


def test_epoch_receipts_match_accepted_identity():
    facts, _ = accepted_epoch_facts()
    assert facts["E1"]["receipt_hash"] == \
        "4b592251eae91865c45dd11ee1ae61ca8f7c26841c687f5868ae314190459ae2"
    assert facts["E2"]["receipt_hash"] == \
        "d29f2aab2c27967f54083981ac19d25b84f315abe36dc94b18d833a02c595951"
    assert facts["E1"]["snapshot_hash"] == \
        "7e746c12ed2bd2081c6bfad43b6808a1fff185834bc9b10760e70b5a072e17d7"
    assert facts["E2"]["snapshot_hash"] == \
        "07aefe67ae7483204eee94b72d4ee98e4c96b40b7c96156d02e7542b21c408f0"


def test_rule_only_change_is_institutional_and_empirical_unchanged():
    facts, _ = accepted_epoch_facts()
    e1, e2 = facts["E1"], facts["E2"]
    assert (e1["fee"], e1["exit_cost"], e1["fee_publication"], e1["fee_revision"]) == \
        (2, 2, "2026-03-01", 1)
    assert (e2["fee"], e2["exit_cost"], e2["fee_publication"], e2["fee_revision"]) == \
        (6, 8, "2027-06-01", 2)
    assert e1["routes"] == {
        "training": "ELIGIBLE", "civil": "ELIGIBLE",
        "exit_constraint": "WITHIN_MODELED_BUDGET"}
    assert e2["routes"] == {
        "training": "BLOCKED_BY_MODELED_RULE", "civil": "ELIGIBLE",
        "exit_constraint": "RESOURCE_CONSTRAINED"}
    assert e1["empirical_steps"] == e2["empirical_steps"] == EXPECTED_STEPS
    assert e1["state"] == e2["state"] == "SELECTED_WORLD_VALUES_SERVED"


def test_consumer_product_reports_institutional_only_change():
    probe = probe_or_authorized_delta(
        delta_observation_rows(F.comparable_pair(), authorized=False))
    product, _ = build_comparison_product(
        {"state": "COMPARABLE_PROBE_ONLY", "delta": probe})
    institutional = product["institutional"]
    assert institutional["rule_only_change"] is True
    assert institutional["training_route_changed"] is True
    assert product["empirical_channel"]["steps_identical"] is True
    assert product["empirical_channel"]["delta_block"]["delta_value_kind"] == \
        "probe_delta"
    assert product["empirical_channel"]["historical_measured_delta"] is None
    assert product["authority"]["actor_executions"] == 0
    assert product["authority"]["model_calls"] == 0
    assert product["authority"]["source_read"] is False
