"""I1 guarded joined consumer: material history, fork, cold process, severance."""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
from pathlib import Path

import pytest

from bp2p4.assertion import ASSERTION_NAME, joined_downstream_a0_a2_assertion
from bp2p4.i1_product import GuardedJoinedProduct
from bp2p4.severance import run_all_severances, severance_receipt
from bp4.store import StoreRefusal

RETURN = Path(__file__).resolve().parents[1]
EXPECTED_RED = {
    "BP2_C8_PROOF": "BP2_C8_PROOF_INVALID",
    "BP2_ACTOR_HISTORY": "BP1_ACTOR_SOURCE_NOT_MATCHING_BP2_C8",
    "BP2_RULE_A": "BP2_RULE_A_RESPONSE_ABSENT",
    "BP2_RULE_T": "BP2_RULE_T_AUTHORIZATION_ABSENT",
    "BP2_TARGET_HASH": "BP2_C9_CONSUMED_HASH_MISMATCH",
    "BP2_E2": "BP2_E2_SELF_PERFORMED",
    "BP4_C10_M6_ACCESS": "A0_CLAIM_SET",
    "BP2_OTHER_HISTORY_ALIASED": "BP1_OTHER_SNAPSHOT_NOT_MATCHING_BP2_C8",
    "BP2_E2_NOT_PERFORMED": "A0_E2_ADMITTED",
    "BP2_PRACTICE_NOT_MATERIALIZED": "A0_PRACTICE_NOT_ESTABLISHED",
}


def _env() -> dict:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def test_guarded_product_verifies_episode_fork_and_cold_branch(intact, tmp_path):
    root = tmp_path / "product"
    product = GuardedJoinedProduct(root, artifacts=intact)
    try:
        assert product.verify_c12()["ok"] is True
        product.say("root history")
        fork = product.fork("alt")
        assert fork["shared_root"]["equal"] is True
        product.use("alt")
        product.say("alt history")
        assert product.verify_c12()["ok"] is True
    finally:
        product.close()
    reopened = GuardedJoinedProduct.reopen(root, branch_id="alt")
    try:
        report = reopened.verify_c12()
        assert report["ok"] is True, report
        rows = reopened.store.db.execute(
            "SELECT branch_id, body FROM episode ORDER BY branch_id, seq").fetchall()
        origins = {json.loads(body)["branch_id"] for _, body in rows}
        assert origins == {"root", "alt"}
    finally:
        reopened.close()


def test_guarded_consumer_uses_the_named_assertion_and_all_severances(
        intact, tmp_path):
    receipt = joined_downstream_a0_a2_assertion(
        tmp_path / "guarded", intact, product_cls=GuardedJoinedProduct)
    assert receipt["status"] == "PASS"
    assert receipt["assertion"] == ASSERTION_NAME
    product = GuardedJoinedProduct.reopen(tmp_path / "guarded")
    try:
        assert product.verify_c12()["ok"] is True
    finally:
        product.close()
    trials = run_all_severances(
        tmp_path / "severance", intact, product_cls=GuardedJoinedProduct)
    summary = severance_receipt(trials)
    assert summary["all_primary_proved"] is True
    assert summary["all_supplementary_proved"] is True
    by_edge = {trial.edge: trial for trial in trials}
    assert set(by_edge) == set(EXPECTED_RED)
    for edge, code in EXPECTED_RED.items():
        assert by_edge[edge].baseline["red"] is False
        assert by_edge[edge].red["red"] is True
        assert code in by_edge[edge].red["message"]
        assert by_edge[edge].restored["red"] is False


def test_b_offscreen_market_work_adds_cash_but_stays_material_exhausted(
        intact, tmp_path):
    root = tmp_path / "product"
    product = GuardedJoinedProduct(root, artifacts=intact)
    try:
        before = product.owner_material_readout("B")
        product.wait(30)
        after = product.owner_material_readout("B")
        assert after["state"]["position"] == "market"
        assert after["state"]["completed_units"] == (
            before["state"]["completed_units"] + 1)
        assert after["state"]["cash"] == before["state"]["cash"] + 2
        assert after["state"]["material_remaining"] == 0
        assert after["state"]["free_hours"] == before["state"]["free_hours"]
        event = after["latest_work_event"]
        assert event["kind"] == "OFFSCREEN_REPAIR"
        assert event["body"]["cash_delta"] == 2
        assert event["body"]["material_delta"] == -1
        assert event["body"]["source_owned"] is True
        public = product.other()["public"]
        assert public["completed_units"] == 4
        assert public["position"] == "market"
        assert public["public_work_events"] == [event["event_id"]]
        assert "cash" in product.other()["private_fields_hidden"]
        assert product.verify_c12()["ok"] is True
    finally:
        product.close()
    reopened = GuardedJoinedProduct.reopen(root)
    try:
        assert reopened.verify_c12()["ok"] is True
        assert reopened.owner_material_readout("B") == after
    finally:
        reopened.close()


def test_material_stock_cannot_be_spent_twice(intact, tmp_path):
    product = GuardedJoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        assert product.observe()["self"]["state"]["material_remaining"] == 2
        first = product.repair()
        assert first["status"] == "OK"
        assert first["actor_state"]["material_remaining"] == 1
        second = product.repair()
        assert second["status"] == "OK"
        assert second["actor_state"]["material_remaining"] == 0
        third = product.repair()
        assert third["status"] == "DENY"
        assert third["code"] == "MATERIAL_EXHAUSTED"
        state = product.observe()["self"]["state"]
        assert state["material_remaining"] == 0
        assert state["completed_units"] == 6
        assert state["cash"] == 59
        assert state["free_hours"] == 10
        assert product.verify_c12()["ok"] is True
    finally:
        product.close()


def test_market_work_is_not_known_before_presence(intact, tmp_path):
    product = GuardedJoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        product.wait(30)
        before = [claim["kind"] for claim in product.observe()["claims"]]
        assert before == ["ARRIVAL"]
        workshop_attend = product.attend()
        assert workshop_attend["new_knowledge"] == []
        assert "OFFSCREEN_REPAIR" not in [
            claim["kind"] for claim in product.observe()["claims"]]
        assert product.travel("market")["admitted"] is True
        market_attend = product.attend()
        assert market_attend["new_knowledge"]
        claims = product.observe()["claims"]
        assert "OFFSCREEN_REPAIR" in [claim["kind"] for claim in claims]
        assert product.verify_c12()["ok"] is True
    finally:
        product.close()


def test_fork_child_cannot_rewrite_parent_material_history(intact, tmp_path):
    product = GuardedJoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        product.wait(30)
        parent_before = product.owner_material_readout("B")
        parent_chain = product.verify_c12()
        fork = product.fork("alt")
        assert fork["shared_root"]["equal"] is True
        product.use("alt")
        assert product.repair()["status"] == "OK"
        product.say("child-only history")
        child_state = product.owner_material_readout("A")
        assert child_state["state"]["completed_units"] == 5
        product.use("root")
        assert product.owner_material_readout("B") == parent_before
        assert product.verify_c12()["ok"] is True
        assert product.verify_c12("alt")["ok"] is True
        assert product.verify_c12()["counts"] == parent_chain["counts"]
        assert product.store.shared_root_equal("root", "alt")["equal"] is True
    finally:
        product.close()


def test_guarded_reader_refuses_unsupported_writer_schema(intact, tmp_path):
    root = tmp_path / "product"
    product = GuardedJoinedProduct(root, artifacts=intact)
    try:
        product.say("schema seed")
    finally:
        product.close()
    with sqlite3.connect(root / "c12.sqlite") as database:
        database.execute(
            "UPDATE meta SET value='BP4_C12_STORE@2' WHERE key='schema'")
        database.commit()
    reopened = GuardedJoinedProduct.reopen(root)
    try:
        report = reopened.verify_c12()
        assert report["ok"] is False
        assert report["schema_ok"] is False
        assert any("schema_version_unsupported" in error
                   for error in report["errors"])
        with pytest.raises(StoreRefusal) as error:
            reopened.fork("unsupported")
        assert error.value.code == "SCHEMA_UNSUPPORTED"
    finally:
        reopened.close()


def test_cold_process_reopens_guarded_material_and_public_history(
        intact, tmp_path):
    root = tmp_path / "state"
    first = subprocess.run(
        [sys.executable, str(RETURN / "run_guarded.py"), "--root", str(root),
         "wait", "30"],
        capture_output=True, text=True, cwd=tmp_path, env=_env())
    assert first.returncode == 0, first.stderr
    second = subprocess.run(
        [sys.executable, str(RETURN / "run_guarded.py"), "--root", str(root),
         "verify"],
        capture_output=True, text=True, cwd=tmp_path, env=_env())
    assert second.returncode == 0, second.stderr
    verified = json.loads(second.stdout)
    assert verified["c12"]["ok"] is True
    assert verified["c12"]["authenticity"]["code"] == "OWNER_ANCHOR_REQUIRED"
    third = subprocess.run(
        [sys.executable, str(RETURN / "run_guarded.py"), "--root", str(root),
         "owner-material"],
        capture_output=True, text=True, cwd=tmp_path, env=_env())
    assert third.returncode == 0, third.stderr
    material = json.loads(third.stdout)
    assert material["visibility"] == "OWNER_TEST_ONLY"
    assert material["state"]["cash"] == 56
    assert material["state"]["material_remaining"] == 0
    assert material["state"]["completed_units"] == 4
    fourth = subprocess.run(
        [sys.executable, str(RETURN / "run_guarded.py"), "--root", str(root),
         "other"],
        capture_output=True, text=True, cwd=tmp_path, env=_env())
    assert fourth.returncode == 0, fourth.stderr
    public = json.loads(fourth.stdout)["public"]
    assert public["completed_units"] == 4
    assert public["position"] == "market"
