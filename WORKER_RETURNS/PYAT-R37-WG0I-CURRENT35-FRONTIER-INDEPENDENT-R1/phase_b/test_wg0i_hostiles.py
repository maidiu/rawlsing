"""WG0I Phase B independent hostile court.

Independent assertions only: the frozen Phase A oracle, the pinned O35E matrix,
and a TEST_ONLY probe frontier.  No WG0R expectation is imported.
"""
from __future__ import annotations

import collections
import hashlib
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import wg0i_oracle as O  # noqa: E402


def test_frozen_oracle_artifact_hashes_are_integrity_bound():
    oracle_file = (O.R / "phase_a/01_PHASE_A_FROZEN_ORACLE.json").read_bytes()
    ledger_file = (O.R / "phase_a/02_ITEM_IDENTITY_LEDGER.jsonl").read_bytes()
    assert hashlib.sha256(ledger_file).hexdigest() == \
        O.ORACLE["item_census"]["identity_ledger"]["sha256"]
    assert len(O.LEDGER) == O.ORACLE["item_census"]["identity_ledger"]["rows"] == 18259
    core = json.loads(oracle_file)
    digest = core.pop("oracle_digest_sha256")
    assert hashlib.sha256(json.dumps(core, sort_keys=True, separators=(",", ":")).encode()).hexdigest() == digest


def test_35_sources_exact_and_no_drop():
    m = O.load_matrix()
    assert len(m["waves"]) == 35
    assert [w["atlas_id"] for w in m["waves"]] == ["SRC%02d" % i for i in range(1, 36)]
    assert sum(len(w["items"]) for w in m["waves"]) == 18259
    assert m["census"]["all_rows"] == 18518
    assert m["census"]["active_rows"] == 18259
    assert m["census"]["excluded_Asian_W6_rows"] == 259
    assert m["census"]["active_rows"] + m["census"]["excluded_Asian_W6_rows"] == m["census"]["all_rows"]


def test_status_census_exact():
    got = collections.Counter(it["qra_authority_status"] for it in O.matrix_items(O.load_matrix()))
    assert dict(got) == O.ORACLE["item_census"]["status_counts"]
    assert sum(got.values()) == 18259


def test_identity_ledger_is_complete_no_duplicate_substitution():
    m = O.load_matrix()
    ids = O.matrix_ids(m)
    assert len(ids) == len(O.matrix_items(m)) == 18259
    assert ids == O.expected_ledger_ids()


def test_all_operation_eligibilities_hold_and_permitted_zero():
    m = O.load_matrix()
    assert all(it["original_item_operation_eligibility"] == "HOLD_SOURCE_SCIENTIFIC_E_PRE_UNISSUED"
               for it in O.matrix_items(m))
    assert O.ORACLE["operation_census"]["permitted"] == 0
    assert O.ORACLE["operation_census"]["hold"] == 18259 * 7
    assert O.ORACLE["operation_census"]["potential_rows"] == 127813
    assert all(v["default"].startswith("HOLD_UNISSUED_ORIGINAL_SOURCE_ITEM_OP_BINDING")
               for v in O.ORACLE["operation_census"]["counts"].values())


def test_primary_disposition_partition_and_six_labels():
    p = O.ORACLE["primary_disposition"]
    assert p == {"SOURCE_INTRINSIC_NONAPPLICABLE": 13577, "AUTHORITY_HELD": 4630,
                 "EXECUTED_WITH_CONSUMER": 52, "PERMITTED": 0, "UNDECIDED": 0}
    assert sum(p.values()) == 18259
    assert O.ORACLE["six_label_census"]["PERMITTED"]["count"] == 0
    assert O.ORACLE["six_label_census"]["PRODUCER_PENDING"]["count"] == 18259
    assert O.ORACLE["six_label_census"]["EXECUTED_WITH_CONSUMER"]["count"] == 52


def test_estate_axis_census_1890_cells_no_hidden_cell():
    e = O.ORACLE["estate_axis_census"]
    assert e["sources"] == 35 and e["cells"] == 1890
    assert e["source_native_expected"] == 1050
    assert e["ee_expected"] == 560
    assert e["f_expected"] == 280
    assert all(x["cells"] == 54 for x in e["per_source"])
    assert sum(e["status_counts"].values()) == 1890


def test_task_ledger_101_and_critical_gate_not_proved():
    t = O.ORACLE["task_census"]
    assert t["tasks"] == 101
    assert t["state_counts"] == {"OPEN_EVIDENCE_BINDING__NOT_A_DEFECT_VERDICT": 101}
    assert t["critical_gate_status"] == "NOT_PROVED_AT_COMPLETE_CLOSED35_ORIGINAL_ITEM_OPERATION_GRAIN"
    assert t["task_identity_ledger_sha256"]


def test_queue_35_sources_175_null_current_refs():
    q = O.ORACLE["queue_census"]
    assert q["sources"] == 35
    assert q["all_current_refs_null"] is True
    assert sum(q["current_ref_nulls"].values()) == 175
    assert all(v == 35 for v in q["current_ref_nulls"].values())
    assert len(q["per_source"]) == 35


def test_accepted_positives_are_historical_not_current_all35():
    pos = O.ORACLE["accepted_positives"]
    lits = pos["lits_i_as2b"]
    assert (lits["respondents"], lits["respondent_events"], lits["coordinate_facts"]) == (
        29002, 58004, 145010)
    assert lits["weight_facts"] == 0
    assert (lits["i03_executed"], lits["i03_passed"], lits["i03_failed"]) == (8, 8, 0)
    assert pos["gss_frozen_accepted"] == 52
    assert pos["o35e_test_only_positive"]["original_source_run"] == \
        "NOT_EXECUTED__SOURCE_AND_ISSUER_HOLD"
    assert "NOT_CURRENT_ALL35" in lits["grain"]


def test_permitted_requires_exact_authority_rule():
    rule = O.ORACLE["classification_contract"]["PERMITTED"]
    assert "E_pre" in rule and "source-use permission" in rule and "operation requirement" in rule
    assert all(s["source_use_status"] == "HOLD_NO_VERIFIED_CURRENT_SIGNED_ORIGINAL_RIGHT"
               for s in O.ORACLE["source_census"]["sources"])
    assert all(s["permission_warrant_ref"] is None and s["competent_original_E_pre_ref"] is None
               for s in O.ORACLE["source_census"]["sources"])


@pytest.mark.parametrize("name", sorted(O.MATRIX_EXPECT))
def test_matrix_hostile_mutation_detected(name):
    got = O.run_matrix_mutation(name)
    assert got["detected"] is True, got
    assert any(x["code"] == O.MATRIX_EXPECT[name] for x in got["violations"]), got


def test_probe_frontier_baseline_clean():
    frontier = O.probe_frontier()
    assert len(frontier["rows"]) == 35
    assert O.validate_probe(frontier) == []
    assert all(r["frontier_state"] == "PRODUCER_PENDING" for r in frontier["rows"])
    assert all(set(r["operation_classes"].values()) == {"HOLD"} for r in frontier["rows"])
    assert all(r["weight"] is None for r in frontier["rows"])


@pytest.mark.parametrize("name", sorted(O.PROBE_EXPECT))
def test_probe_hostile_mutation_detected(name):
    got = O.run_probe_mutation(name)
    assert got["detected"] is True, got
    assert any(x["code"] == O.PROBE_EXPECT[name] for x in got["violations"]), got


def test_wg0r_output_status_recorded():
    st = O.wg0r_status()
    assert st["head"] and st["base"] == "68873526efe5a39a0849aa401666ac997870f156"
    if st["output_present"]:
        assert st["return_dirs"], st
    else:
        assert st["commits_beyond_base"] == 0
        assert st["head"] == st["base"]
