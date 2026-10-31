from __future__ import annotations

from pathlib import Path

import pytest

from targetless_i1_bridge import TargetlessGuardedJoinedProduct
from targetless_c10_consumer import BAction, MaterialLedger, TargetlessC10Ledger


def market_material() -> MaterialLedger:
    return MaterialLedger.consume(
        stock_before=0, replenish=1, consume=1, hours_before=12,
        hours_after=11, tick=40, replenishment_ref="TESTONLY_I1_PRIOR_STOCK",
    )


def ledger(action: str, *, observed: bool = True) -> TargetlessC10Ledger:
    performed = action in {"SHARE", "REFUSE"}
    if action == "SHARE":
        kind = "TEST_ONLY_INTERVENTION"
        performer = "B" if performed else None
        tool = True
    elif action == "REFUSE":
        kind = "TEST_ONLY_INTERVENTION"
        performer = "B"
        tool = False
    elif action == "SILENCE":
        kind = "NON_EVENT_CONDITION"
        performer = None
        tool = False
    else:
        raise ValueError(action)
    record = {
        "action": action, "kind": kind, "performer": performer,
        "A_event_access": observed and performed, "A_tool_access": tool,
        "frozen_parent_hash": "TESTONLY_F1C_FROZEN",
        "receipt_hash": f"TESTONLY_{action}_{observed}",
    }
    b_action = BAction(
        action=action, performer=performer, kind=kind, observed=observed,
        a_event_access=observed and performed, a_tool_access=tool,
        b_hours_before=12, b_hours_after=11 if action == "SHARE" else 12,
        b_history_digest="TESTONLY_B_HISTORY",
        shared_history_digest="TESTONLY_SHARED_HISTORY",
        material=market_material(), performed=performed, evaluated=False,
        evaluation_receipt=None, source_record=record,
    )
    return TargetlessC10Ledger.build(b_action, tick_before=241, tick_after=251)


def test_targetless_refuse_is_consumed_by_same_i1_person(intact, tmp_path):
    product = TargetlessGuardedJoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        product.wait(30)
        before = product.other()["public"]
        read = product.consume_targetless(ledger("REFUSE"))
        after = product.other()["public"]
        assert read["same_person_product"] == "GuardedJoinedProduct"
        assert read["targetless_states"] == ["TARGETLESS_REFUSE"]
        assert read["can_read_B_behavior"] is True
        assert read["tool_access"] == 0
        assert read["no_c9_target"] is True
        assert read["no_performed_e2"] is True
        assert read["no_learned_practice"] is True
        assert read["no_utterance"] is True
        assert read["c12_ok"] is True
        assert after == before
        material = product.owner_material_readout("B")
        assert material["state"]["material_remaining"] == 0
        assert material["latest_work_event"]["body"]["material_delta"] == -1
        ledger_row = product.targetless_history()[0]
        assert ledger_row.action.material.replenished == 1
        assert ledger_row.action.material.consumed == 1
        assert ledger_row.action.material.stock_after == 0
        assert ledger_row.action.material.receipt["clamped"] is False
    finally:
        product.close()


def test_silence_is_distinct_and_not_a_refuse(intact, tmp_path):
    product = TargetlessGuardedJoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        read = product.consume_targetless(ledger("SILENCE"))
        assert read["targetless_states"] == ["TARGETLESS_SILENCE"]
        assert read["can_read_B_behavior"] is False
        assert read["tool_access"] == 0
    finally:
        product.close()


def test_observed_and_unobserved_share_differ_for_same_i1_person(intact, tmp_path):
    observed = TargetlessGuardedJoinedProduct(tmp_path / "observed", artifacts=intact)
    unobserved = TargetlessGuardedJoinedProduct(tmp_path / "unobserved", artifacts=intact)
    try:
        ro = observed.consume_targetless(ledger("SHARE", observed=True))
        ru = unobserved.consume_targetless(ledger("SHARE", observed=False))
        assert ro["can_read_B_behavior"] is True
        assert ru["can_read_B_behavior"] is False
        assert ro["tool_access"] == 1
        assert ru["tool_access"] == 1
        assert ro["targetless_states"] == ["SHARE_OBSERVED"]
        assert ru["targetless_states"] == ["SHARE_UNOBSERVED"]
    finally:
        observed.close()
        unobserved.close()


def test_cold_reopen_reads_same_targetless_history(intact, tmp_path):
    root = tmp_path / "product"
    product = TargetlessGuardedJoinedProduct(root, artifacts=intact)
    try:
        first = product.consume_targetless(ledger("REFUSE"))
        hashes = first["targetless_hashes"]
    finally:
        product.close()
    reopened = TargetlessGuardedJoinedProduct.reopen(root)
    try:
        second = reopened.targetless_read()
        assert second["targetless_hashes"] == hashes
        assert second["targetless_states"] == ["TARGETLESS_REFUSE"]
        assert second["c12_ok"] is True
    finally:
        reopened.close()


def test_targetless_does_not_fabricate_c9_or_e2(intact, tmp_path):
    product = TargetlessGuardedJoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        read = product.consume_targetless(ledger("REFUSE"))
        assert read["no_c9_target"] is True
        assert read["no_performed_e2"] is True
        assert read["targetless_states"] == ["TARGETLESS_REFUSE"]
        assert read["a_public"]["completed_units"] == product.other()["public"]["completed_units"]
    finally:
        product.close()
