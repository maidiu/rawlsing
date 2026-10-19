"""J42 breadth: independent 84-view route oracle, published-boundary selection,
no-drop coverage and returned-bank dereference."""
from __future__ import annotations

import j42_build
import j42_join as J

FROZEN_FAMILIES = {"base", "two_epoch", "formal", "civil_sanction",
                   "civil_closed", "exit_only", "fee_only"}


def test_route_oracle_all_84(joined):
    assert len(joined["views"]) == 84
    mismatches = [view["key"] for view in joined["views"] if not view["match"]]
    assert mismatches == []
    for view in joined["views"]:
        family, mode, budget = view["key"].split("/")
        budget = int(budget.replace("budget", ""))
        assert view["actual"] == J.expected_routes(family, mode, budget)


def test_published_boundary_selection(fresh):
    _, w41 = fresh
    asof = w41["worlds"][J.view_key("fee_only", "AS_OF", 5)]
    late = w41["worlds"][J.view_key("fee_only", "TEST_CURRENT", 5)]
    assert asof["structural_values"]["training_fee"]["value"] == 2
    assert asof["native_consumer"]["routes"]["training"] == "ELIGIBLE"
    assert late["structural_values"]["training_fee"]["value"] == 6
    assert late["native_consumer"]["routes"]["training"] == "BLOCKED_BY_MODELED_RULE"
    assert w41["worlds"][J.view_key("base", "AS_OF", 5)]["native_consumer"][
        "routes"]["training"] == "ELIGIBLE"


def test_no_drop_all_84_families(joined):
    assert set(J.JOIN_FAMILIES) == FROZEN_FAMILIES
    expected = {J.view_key(f, m, b) for f in FROZEN_FAMILIES
                for m in J.JOIN_MODES for b in J.JOIN_BUDGETS}
    assert {view["key"] for view in joined["views"]} == expected
    assert len(joined["joined_receipts"]) == 84
    assert len(joined["p41_receipts"]) == 84
    assert all(len(receipt["n10e_steps"]) == 3 for receipt in joined["p41_receipts"])
    assert sum(len(receipt["n10e_steps"]) for receipt in joined["p41_receipts"]) == 252


def test_e41_returned_bank_dereferenced(fresh):
    e41, _ = fresh
    custody = e41["returned_bank_custody"]
    ledger = custody["f1f4_coverage_ledger.json"]
    assert ledger["executed"] == 31 and ledger["expected"] == 31
    assert ledger["no_drop_ok"] is True
    assert ledger["original_source_occupied_count"] == 0
    assert ledger["held_original_scope"]
    assert custody["computed_slice_evidence.json"]["slice_count"] == 18


def test_typed_holds_preserved(fresh):
    e41, w41 = fresh
    holds = j42_build.typed_holds(e41, w41)
    assert holds["e41_returned_bank"]["join_state"] == "SAME_SOURCE_JOIN_UNISSUED"
    assert holds["e41_returned_bank"]["slice_count"] == 18
    assert holds["retained_gt2_j04"]["join_state"] == "NO_AUTHORIZED_JOIN"
    assert holds["retained_gt2_j04"]["retained_context_state"]
    assert holds["f6_evidence"]["join_state"] == \
        "SEPARATE_READONLY_EVIDENCE_ONLY"
    assert set(holds["purposes"].values()) == {"HOLD"}
    assert holds["original35"]
    assert holds["actor"] == "NOT TOUCHED"
    assert holds["n11"] == "HAND-BACK ONLY"
    assert holds["n12"] == "NOT TOUCHED"


def test_w41_evidence_view_refuses_cross_source_join(fresh):
    _, w41 = fresh
    hold = w41["evidence_view_hold"]
    assert hold["matching_decision"]["state"] == "NO_AUTHORIZED_JOIN"
    assert hold["matching_decision"]["common_respondents"] is None
    assert hold["matching_decision"]["joint_probability"] is None
    assert hold["route_probability"] is None
    assert all(view["route_probability"] is None
               for view in w41["worlds"].values())
    assert all(view["operative_N9"] is False
               for view in w41["worlds"].values())
