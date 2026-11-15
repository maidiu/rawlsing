from __future__ import annotations

import ast
import copy
import json
from pathlib import Path

import pytest

from rawlsing_next import ee_p2x_darwin_court_driver as driver


REPO = Path(__file__).resolve().parents[2]
CURRENT = REPO / "WORKER_RETURNS/FIABC-T2/01_SIX_CELL_EXECUTION_MANIFEST.json"
BACKEND = REPO / "rawlsing_next/ee_p2x_darwin_stage_backend.py"

BAD_TO_GOOD = {
    "72f8e8a2b6b2330332030e3978077c11e38ec8db": "72f8f3c03ed065e86fea4e76bb17f8e06c2bf540",
    "92e68693d72cbfcdd1c6d16e7f247ca3f60c8c55": "92e364b31eaf27be1bca2081eff65f6ffb779c3d",
    "62cea85788eb160796642ba09d9f0d41f987a3d43": "62ce608829c3d9c2fb7c999aefe40188637edf80",
    "cef346fca029fa920db16e83db908d466018f39e": "cef326ebbc40468428378f7fdbe76e4756179f39",
    "ffb07a9d0bafbf685d27aa1161ce830bcfc810fc": "ffb063b93c86e215604eecb29a9545c7efdff399",
}


def _doc():
    return json.loads(CURRENT.read_text(encoding="utf-8"))


def _validate_mutation(doc):
    ident = driver.MapIdentity(
        driver.CURRENT_EXECUTION_MANIFEST_SCHEMA,
        "0" * 64,
        "0" * 40,
    )
    return driver.validate_current_execution_manifest(doc, ident)


def test_absent_root_current_law_reenters_exact_measured_lits_a_s01():
    machine = driver.load_current_execution_manifest(CURRENT)
    law = machine.document["lits_a_absent_root_current_law"]
    assert law == driver.LITS_A_ABSENT_ROOT_CURRENT_LAW
    assert law["historical_root_current_host_state"] == "ABSENT"
    assert law["preserved_s01_physical_work_credit"] == "ZERO__NOT_AVAILABLE"
    assert law["prebuild_required"] is False
    assert law["separate_r35_prebuild_allowed"] is False
    assert machine.first_unfinished == "LITS_I/A/S01_CANDIDATE_PREPARATION_BUILD"
    s01 = machine.get(machine.first_unfinished)
    assert s01.disposition == "READY__RUN_LOCALLY"
    assert s01.evidence_or_stop_law_ref is None
    assert s01.empirical_source_access_required is True
    assert s01.physical_host_measurement_required is True


def test_historical_continuation_remains_immutable_history_only():
    doc = _doc()
    history = doc["historical_continuation"]
    assert history["role"] == "IMMUTABLE_HISTORY_ONLY__NOT_CURRENT_CAPABILITY_LAW"
    assert history["mutate_in_place"] is False
    assert history["sha256"] == "ffe7d40e5f2051f839a3a646fd434fbee3b93371e7571d959805ca7ca74e0422"
    assert history["git_blob_sha1"] == "e06e95dd370a4fd44235932088308c3372522ed4"


def test_preserved_root_law_cannot_be_reintroduced_to_suppress_current_s01():
    doc = _doc()
    row = next(x for x in doc["cells"] if x["source"] == "LITS_I" and x["candidate"] == "A")
    row["stages"]["S01_CANDIDATE_PREPARATION_BUILD"] = [
        "DONE__PRESERVE", "LITS_A_FIRST_BUILD", False, False, "S02_C11_REACHABILITY"
    ]
    with pytest.raises(driver.ContinuationMapError):
        _validate_mutation(doc)


def test_old_no_repeat_prohibition_is_hostile_under_absent_root_law():
    doc = _doc()
    doc["hard_prohibitions"].append("NO_REPEAT_COMPLETED_LITS_A_FIRST_BUILD")
    with pytest.raises(driver.ContinuationMapError):
        _validate_mutation(doc)


def test_first_unfinished_cannot_skip_current_lits_a_s01():
    doc = _doc()
    doc["entry_guard"]["first_unfinished_court_stage"] = "LITS_I/A/S02_C11_REACHABILITY"
    with pytest.raises(driver.ContinuationMapError):
        _validate_mutation(doc)


def test_absent_root_holding_cannot_be_relabeled_present():
    doc = _doc()
    doc["lits_a_absent_root_current_law"]["historical_root_current_host_state"] = "PRESENT"
    with pytest.raises(driver.ContinuationMapError):
        _validate_mutation(doc)


def test_all_five_malformed_r35_runtime_git_pins_are_removed():
    text = BACKEND.read_text(encoding="utf-8")
    for bad, good in BAD_TO_GOOD.items():
        assert bad not in text
        assert good in text


def test_lits_a_runtime_uses_one_candidate_owned_s01_build_and_no_historical_root_env():
    text = BACKEND.read_text(encoding="utf-8")
    assert "def _lits_a_build_current_s01" in text
    assert 'ctx.roots.durable/"lits_a_r5"' in text
    assert "LiTS-A current measured S01 requires absent candidate-owned target" in text
    assert "BUILD_LITS_A_R5_FROM_CANONICAL_PHYSICAL_INCIDENCE" in text
    assert "VERIFY_CANONICAL_LITS_I_RAW_SHA_FOR_CURRENT_S01_BUILD" in text
    assert "PENDING__MUST_USE_SAME_S01_STATE__NO_SECOND_BUILD" in text
    assert '"physical_equivalence_claimed":False' in text
    assert '"semantic_parity_claimed":False' in text
    assert "preserved LiTS-A R5 runtime path unbound" not in text
    assert '["LITS_I_A_FIRST_BUILD"] if cell=="LITS_I/A"' not in text


def test_current_manifest_forbids_duplicate_prebuild_and_historical_numeric_credit():
    doc = _doc()
    prohibitions = set(doc["hard_prohibitions"])
    assert "NO_DUPLICATE_LITS_A_S01_PREBUILD_OR_R35_REBUILD" in prohibitions
    assert "NO_HISTORICAL_LITS_A_S01_NUMERIC_CREDIT_WHEN_ROOT_ABSENT" in prohibitions
    assert "NO_REPEAT_COMPLETED_LITS_A_FIRST_BUILD" not in prohibitions


def test_repaired_live_backend_is_python_syntax_valid():
    ast.parse(BACKEND.read_text(encoding="utf-8"))
