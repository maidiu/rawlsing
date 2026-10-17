"""WG0Q Phase-A authority-body / temporal / cold-replay court.

FROZEN before any WG0P7 candidate is read.  The original WG0O 14 controls are
preserved byte-identically and are executed separately by their own court.  This
file exercises the new finite matrix over real AuthoritySnapshot, FixtureOwner
and ColdCheckpoint interfaces.

Negatives require a typed refusal, no served supported original fact, and zero
new I03 calls.  A late untyped KeyError after I03 is a RED, not a pass.  Honest
owner bodies must still serve exactly 42 supported cells and four I03 calls.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import pathlib
import sys

import pytest

R = pathlib.Path(__file__).resolve().parents[1]
RET = R.parent.parent
O = json.loads((RET / "01_FROZEN_AUTHORITY_BODY_AND_EPOCH_ORACLE.json").read_text())

NEW = O["new_controls"]
NEG = [c for c in NEW if c["kind"] == "NEGATIVE_TYPED_REFUSAL"]
POS = [c for c in NEW if c["kind"] != "NEGATIVE_TYPED_REFUSAL"]
FAMILIES = set(NEG[0]["expected"]["allowed_exception_families"])
TOKENS = set(NEG[0]["expected"]["allowed_typed_tokens"])


def _court():
    sys.path.insert(0, str(R / "repro"))
    return importlib.import_module("authority_body_adapter_v1").AuthorityBodyCourt()


@pytest.fixture(scope="module")
def court():
    return _court()


def test_phase_a_oracle_self_consistency():
    assert O["frozen_before_any_wg0p7_inspection"] is True
    assert O["original_control_count"] == 14
    assert O["original_negative_count"] == 11
    assert O["original_positive_count"] == 3
    assert len(O["original_wg0o_controls"]) == 14
    assert O["new_control_count"] == len(NEW) == 34
    assert O["new_negative_count"] == len(NEG) == 29
    assert O["new_positive_count"] == len(POS) == 5
    assert O["original_wg0o_oracle_sha256"] == hashlib.sha256(
        (R / "01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json").read_bytes()).hexdigest()


def test_original_wg0o_oracle_is_preserved_byte_for_byte():
    inherited = json.loads((R / "01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json").read_text())
    assert inherited["controls"] == O["original_wg0o_controls"]
    assert len(inherited["controls"]) == 14
    assert inherited["preserved_inherited_status"]["WG0N_five_unconstructible_controls"] == \
        O["five_wg0n_unconstructible_controls_preserved"]
    assert inherited["preserved_inherited_status"]["WG0N_two_historical_characterisation_failures"] == \
        O["two_historical_characterisation_failures_preserved"]


@pytest.mark.parametrize("control", NEG, ids=lambda c: c["group"] + "/" + c["case"])
def test_negative_authority_body_is_typed_refused_before_I03(court, control):
    e = court.execute_case(control["group"], control["case"])
    exp = control["expected"]
    assert e["attempted"] is True
    assert e["raw_path"], "raw receipt must be persisted"
    assert e["physical_modules"], "native owner modules must be physically verified"
    assert e["served_supported_original_fact"] is exp["expected_served_supported_original_fact"], (
        control["case"] + " served a supported original fact")
    assert e["new_I03_calls"] == exp["expected_new_I03_calls"], (
        f"{control['case']}: expected zero I03 calls before refusal, got "
        f"{e['new_I03_calls']} after {e['exception_type']}: {e['exception_reason']}")
    typed = e["exception_type"] in FAMILIES or e["typed_refusal"] in TOKENS
    assert typed, (
        f"{control['case']}: untyped/absent refusal "
        f"({e['exception_type']}: {e['exception_reason']}) is a RED")


@pytest.mark.parametrize("control", POS, ids=lambda c: c["group"] + "/" + c["case"])
def test_honest_owner_body_still_serves(court, control):
    e = court.execute_case(control["group"], control["case"])
    exp = control["expected"]
    assert e["attempted"] is True
    assert e["exception_type"] is exp["expected_exception_type"], (
        f"{control['case']}: honest path refused: {e['exception_reason']}")
    if control["kind"] == "POSITIVE_COLD_RESTORE":
        assert e.get("restored") is True
        assert e["new_I03_calls"] == exp["expected_new_I03_calls"]
        assert e["supported_fact_cells_served"] == 0
        return
    assert e["supported_fact_cells_served"] == exp["expected_supported_fact_cells_served"]
    assert e["effects_sha256"] == exp["expected_effects_sha256"]
    if "expected_new_I03_calls" in exp:
        assert e["new_I03_calls"] == exp["expected_new_I03_calls"]
    if control["kind"] == "POSITIVE_REPLAY":
        assert e["second_run_equal_consumer"] is True
        assert e["second_run_equal_receipts"] is True
