"""WG0O preregistered authority-seam / issuer-residual court.

FROZEN BEFORE ANY CANDIDATE EXECUTION. Assertions express the declared law over
the REAL rel.authorities / rel.qauth surface and the REAL owner interfaces; they
are independent of the author implementation. A late untyped KeyError/TypeError
is a RED, not a refusal pass.

PHASE A freezes this file, repro/authority_seam_adapter_v1.py and
01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json.
PHASE B executes them against the independently staged WG0P6 candidate.
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
O = json.loads((R / "01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json").read_text())
WG0N = pathlib.Path(os.environ.get(
    "WG0O_WG0N_ROOT", R.parent / "PYAT-R27-WG0N-RELEASE-VIEW-INDEPENDENT-R1"))

PRESERVED_MARKERS = (
    "tests/test_hostile_source_view_court.py",
    "repro/hostile_source_view_adapter_v1.py",
    "01_PREREGISTERED_HOSTILE_SOURCE_VIEW_ORACLE.json",
    "02_PHASE_B_VERDICT.md",
)


def _load_court():
    sys.path.insert(0, str(R / "repro"))
    name = os.environ.get("WG0O_ADAPTER", "authority_seam_adapter_v1")
    return importlib.import_module(name).AuthoritySeamCourt()


@pytest.fixture(scope="module")
def court():
    return _load_court()


def test_phase_a_oracle_is_self_consistent():
    ctr = O["controls"]
    assert len(ctr) == O["control_count"] == 14
    assert sum(1 for c in ctr if c["kind"] == "NEGATIVE_REFUSAL") == O["negative_count"] == 11
    assert sum(1 for c in ctr if c["kind"] == "POSITIVE_SERVE") == O["positive_count"] == 3
    groups = {c["group"] for c in ctr}
    for required in ("authority_issuer_substitution", "signature_and_callback",
                     "revocation_and_alias", "positive_owner"):
        assert required in groups, required
    assert O["frozen_before_any_candidate_execution"] is True


def test_inherited_wg0n_status_preserved_not_regraded():
    """The five unconstructible controls and two characterisation failures stay NOT green."""
    for rel in PRESERVED_MARKERS:
        assert (WG0N / rel).is_file(), rel
    verdict = (WG0N / "02_PHASE_B_VERDICT.md").read_text()
    assert "5 of my own controls are untested" in verdict
    assert "2 inherited characterisation tests fail" in verdict
    preserved = O["preserved_inherited_status"]
    assert len(preserved["WG0N_five_unconstructible_controls"]) == 5
    assert len(preserved["WG0N_two_historical_characterisation_failures"]) == 2


NEG = [c for c in O["controls"] if c["kind"] == "NEGATIVE_REFUSAL"]
POS = [c for c in O["controls"] if c["kind"] == "POSITIVE_SERVE"]


@pytest.mark.parametrize("control", NEG, ids=lambda c: c["group"] + "/" + c["case"])
def test_forged_or_substituted_authority_does_not_serve_supported_fact(court, control):
    e = court.execute_case(control["group"], control["case"])
    assert e["attempted"] is True
    assert e["raw_path"], "execution must produce a persisted raw receipt"
    assert e["physical_modules"], "native owner modules must be physically imported/verified"
    # the law: no SUPPORTED original fact under a forged/substituted/stale issuer
    assert e["served_supported_original_fact"] is False, control["case"]
    ok_exc = e["exception_type"] in O["allowed_refusal_exceptions"]
    ok_tok = e["typed_refusal"] in O["allowed_typed_refusals"]
    assert ok_exc or ok_tok or e["served_positive"] is False, (
        f"{control['case']}: untyped/absent refusal ({e['exception_type']}: "
        f"{e['exception_reason']}) is a RED, not a pass")


@pytest.mark.parametrize("control", POS, ids=lambda c: c["group"] + "/" + c["case"])
def test_legitimate_owner_still_serves_supported_fact(court, control):
    e = court.execute_case(control["group"], control["case"])
    assert e["attempted"] is True
    assert e["exception_type"] is None, f"legitimate owner refused: {e['exception_reason']}"
    assert e["served_supported_original_fact"] is True, "the honest path must still serve"
    assert e["consumer"], "legitimate owner must produce consumer values"


def test_phase_a_artifacts_are_frozen_and_identified():
    digest = hashlib.sha256(
        (R / "01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json").read_bytes()).hexdigest()
    receipt = R / "observations/PHASE_A_FREEZE_RECEIPT.json"
    assert receipt.is_file(), "Phase A must be frozen and committed before Phase B execution"
    data = json.loads(receipt.read_text())
    assert data["oracle_sha256"] == digest
    assert data["frozen_before_any_candidate_execution"] is True
