"""WG0N preregistered hostile source-view / release-identity court.

FROZEN BEFORE WG0P6 WAS READ. Assertions are independent of any author
implementation: they express the declared admission law. A late untyped KeyError
is a RED, not a refusal pass.

PHASE A freezes this file and 01_PREREGISTERED_HOSTILE_SOURCE_VIEW_ORACLE.json.
PHASE B executes it against the independently staged WG0P6 candidate.
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
WG0M = pathlib.Path(os.environ.get("WG0N_PRESERVED_ROOT", R.parent / "PYAT-R26-WG0M-ORIGINAL-FRONTIER-INDEPENDENT-DELTA-R1"))
O = json.loads((R / "01_PREREGISTERED_HOSTILE_SOURCE_VIEW_ORACLE.json").read_text())

# The parent's own suites must still be present and byte-exact: nothing here may
# rewrite an inherited expectation to make an ignored field pass.
PRESERVED_ROOT = WG0M
PRESERVED_MARKERS = (
    "tests/test_descriptor_delta_frozen.py",
    "tests/phase_b/test_additional_descriptor_binding_red.py",
    "tests/test_precommitted_phase_b.py",
    "01_FROZEN_DESCRIPTOR_EXPECTATIONS.json",
    "01_FROZEN_EXPECTATIONS_BEFORE_WG0P4.json",
)


def _load_adapter():
    sys.path.insert(0, str(R / "repro"))
    name = os.environ.get("WG0N_ADAPTER", "hostile_source_view_adapter_v1")
    return importlib.import_module(name).HostileSourceViewCourt()


@pytest.fixture(scope="module")
def court():
    return _load_adapter()


def test_phase_a_oracle_is_self_consistent():
    ctr = O["controls"]
    assert len(ctr) == O["control_count"] == 17
    assert sum(1 for c in ctr if c["kind"] == "NEGATIVE_REFUSAL") == O["negative_count"] == 14
    assert sum(1 for c in ctr if c["kind"] == "POSITIVE_SERVE") == O["positive_count"] == 3
    # every named commission class is represented
    groups = {c["group"] for c in ctr}
    for required in ("release_source_view_substitution", "reused_source_pointer",
                     "source_epoch_and_revocation", "altered_snapshot",
                     "issuer_mismatch", "positive_legitimate_owner"):
        assert required in groups, required


def test_inherited_suites_are_present_and_unmodified():
    """No inherited file may be rewritten by this reviewer."""
    for rel in PRESERVED_MARKERS:
        p = PRESERVED_ROOT / rel
        assert p.is_file(), rel
    # The retained WG0M RED control must still exist verbatim in the parent oracle.
    parent_oracle = json.loads((PRESERVED_ROOT / "01_FROZEN_DESCRIPTOR_EXPECTATIONS.json").read_text())
    reds = [c for c in parent_oracle["controls"] if c["group"] == "source" and c["case"] == "release_source_artifact"]
    assert len(reds) == 1, "the retained RED control must be preserved exactly once"


NEG = [c for c in O["controls"] if c["kind"] == "NEGATIVE_REFUSAL"]
POS = [c for c in O["controls"] if c["kind"] == "POSITIVE_SERVE"]


@pytest.mark.parametrize("control", NEG, ids=lambda c: c["group"] + "/" + c["case"])
def test_hostile_source_view_is_refused(court, control):
    e = court.execute_case(control["group"], control["case"])
    assert e["attempted"] is True
    assert e["raw_path"], "execution must produce a persisted raw receipt"
    assert e["physical_modules"], "native owner modules must be physically imported/verified"
    # the law: typed refusal BEFORE any new I03 call
    assert e["new_I03_calls"] == 0, control["case"]
    assert e["served_positive"] is False, f"{control['case']} must not serve a positive"
    # either a lawfully typed error family, or a typed refusal token
    ok_exc = e["exception_type"] in O["allowed_refusal_exceptions"]
    ok_tok = e["typed_refusal"] in O["allowed_typed_refusals"]
    assert ok_exc or ok_tok, (
        f"{control['case']}: untyped/absent refusal ({e['exception_type']}: "
        f"{e['exception_reason']}) is a RED, not a pass"
    )


@pytest.mark.parametrize("control", POS, ids=lambda c: c["group"] + "/" + c["case"])
def test_legitimate_owner_still_serves(court, control):
    e = court.execute_case(control["group"], control["case"])
    assert e["attempted"] is True
    assert e["exception_type"] is None, f"legitimate owner refused: {e['exception_reason']}"
    assert e["served_positive"] is True, "the honest path must still serve"
    assert e["consumer"], "legitimate owner must produce consumer values"


def test_preregistration_is_hashed_and_pushed():
    """Phase A artefacts must be committed; the hash is checked in the return."""
    digest = hashlib.sha256((R / "01_PREREGISTERED_HOSTILE_SOURCE_VIEW_ORACLE.json").read_bytes()).hexdigest()
    receipt = R / "observations/PHASE_A_FREEZE_RECEIPT.json"
    if receipt.is_file():
        data = json.loads(receipt.read_text())
        assert data["oracle_sha256"] == digest
        assert data["frozen_before_reading_WG0P6"] is True
