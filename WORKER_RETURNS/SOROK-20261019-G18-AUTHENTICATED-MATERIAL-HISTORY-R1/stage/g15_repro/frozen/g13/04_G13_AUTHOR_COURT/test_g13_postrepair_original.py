"""Post-repair original K11 court: preserved content invariants + re-frozen hashes.

FROZEN BEFORE EXECUTION.

`test_original_sgi1.py` (byte-unchanged, inherited from G12) is retained and its
4 residual failures are disclosed: its frozen fingerprints bind `candidate_set_hash`,
and repairing selector integrity (defect family 6) necessarily rebases that value.
This module re-asserts everything that IS preserved -- the 24 case identities, the
98 predicate names, and all 98 predicate verdicts -- and compares against the
REPAIRED fingerprint manifest, which is published alongside it.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
COURT = ROOT.parent / "03_POSTREPAIR_COURT"
sys.dont_write_bytecode = True
sys.path.insert(0, str(COURT))

from replay_sgi1 import execute  # noqa: E402
from lab_sgi1.core import h_obj  # noqa: E402

RESULT, SUMMARY = execute()
REPAIRED_FINGERPRINTS = json.loads(
    (ROOT / "repaired_fingerprints.json").read_text())["fingerprints"]
ORIGINAL_PREDICATE_NAMES = json.loads(
    (ROOT / "original_predicate_names.json").read_text())


@pytest.mark.parametrize("case", RESULT["cases"], ids=lambda c: c["case_id"])
def test_postrepair_case_identity_and_predicates_unchanged(case):
    cid = case["case_id"]
    assert case["n_assertions"] == len(case["assertion_results"])
    assert all(case["assertion_results"].values()), case["assertion_results"]
    assert sorted(case["assertion_results"]) == ORIGINAL_PREDICATE_NAMES[cid]


def test_postrepair_denominators_complete_and_offline():
    assert RESULT["n_cases"] == 24
    assert RESULT["n_assertions"] == 98
    assert RESULT["n_assertions_pass"] == 98
    assert RESULT["cases_failed"] == []
    assert SUMMARY["network_attempts"] == []
    assert SUMMARY["new_provider_calls"] == 0


def _actual_fingerprint(case):
    """Recompute the case fingerprint exactly as the original court did."""
    obs = case["observed_state"]
    sel = (obs.get("selection") or obs.get("selection_a")
           or obs.get("selection_discordant") or obs.get("selection_base"))
    dad = obs.get("dad_event_hash") or obs.get("dad_hash_a")
    return h_obj(dict(assertions=case["assertion_results"],
                      grade=case["terminal_grade"], selection=sel, dad=dad))


def test_postrepair_fingerprints_match_repaired_manifest():
    mismatched = [c["case_id"] for c in RESULT["cases"]
                  if _actual_fingerprint(c) != REPAIRED_FINGERPRINTS[c["case_id"]]["fingerprint"]]
    assert not mismatched, mismatched


def test_postrepair_exactly_four_fingerprints_were_rebased():
    """The disclosed consequence set is closed and enumerated, not drifting."""
    rebased = sorted(c for c, v in SUMMARY["comparison"].items() if not v["equal"])
    expected = sorted(json.loads(
        (ROOT / "rebased_fingerprints.json").read_text())["cases"])
    assert rebased == expected


def test_postrepair_no_case_has_a_false_predicate():
    false_predicates = {
        c["case_id"]: [k for k, v in c["assertion_results"].items() if not v]
        for c in RESULT["cases"]
        if not all(c["assertion_results"].values())
    }
    assert false_predicates == {}
