"""The joined BP2 -> BP4 source-free product positive.

Every test here runs the real BP4 A0-A3 surface over artifacts produced by BP2's
real ``JoinedProducer``. Nothing is a shape-correct dict authored by this worker:
the expected identities come from the physical BP2 artifacts through
``JoinedProduct.seed``/``verify_join``.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from bp2p4 import reunion, seed as seed_mod
from bp2p4.assertion import ASSERTION_NAME, joined_downstream_a0_a2_assertion
from bp2p4.product import JoinedProduct, JoinedProductRefusal

RETURN = Path(__file__).resolve().parents[1]
OLD_BP4_TARGET = "08a8d89a2fca443c668288880a3c889cf3c06c40f12771a10050993ff16a62a6"


def _env() -> dict:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def test_joined_a0_a2_assertion_passes(intact, tmp_path):
    receipt = joined_downstream_a0_a2_assertion(tmp_path / "product", intact)
    assert receipt["status"] == "PASS"
    assert receipt["assertion"] == ASSERTION_NAME
    assert receipt["target_id"] == intact.target_id
    assert receipt["consumed_state_hash"] == intact.consumed_state_hash
    assert receipt["c8_state_digest"] == intact.c8_state_digest
    assert receipt["target_id"] != OLD_BP4_TARGET
    assert receipt["e2_admitted"] is True
    assert receipt["practice"]["established"] is True
    assert receipt["a0"]["claims"] == ["ARRIVAL"]
    assert receipt["a2"]["other_completed_units"] == 4
    assert "OFFSCREEN_REPAIR" in receipt["a2"]["reentry_claim_kinds"]
    assert receipt["a2"]["m6_hidden_before_attend"]["state"] == "NONRENDERABLE"
    assert receipt["native"] is False


def test_product_exposes_the_real_bp2_source(intact, tmp_path):
    product = JoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        source = product.verify_join()
        custody = source["custody"]
        assert custody["target_id"] == intact.target_id
        assert custody["target_record_hash"] == intact.target_record_hash
        assert custody["consumed_state_hash"] == intact.consumed_state_hash
        assert custody["c8_occurrence_id"] == "OCC-0001"
        assert custody["c8_state_digest"] == intact.c8_state_digest
        assert custody["e1_event_hash"] == intact.e1_event_hash
        assert custody["rule_a_content_hash"] == intact.rule_a_hash
        assert custody["rule_t_content_hash"] == intact.rule_t_hash
        assert custody["response_hash"] == intact.response_hash
        assert custody["grant_hash"] == intact.grant_hash
        assert custody["e2_receipt_hash"] == intact.e2_receipt_hash
        assert custody["adp019_admission_receipt"] == "ADP019_ADMISSION_RECEIPT_ABSENT"
        assert custody["native_grants"] == {
            "actor": False, "rule": False, "c8_trust": False, "e2": False,
            "world": False, "c11": False, "c12": False, "adp019": False}
        observed = product.observe()
        assert observed["c9"]["target_id"] == intact.target_id
        assert observed["c9"]["target_id"] != OLD_BP4_TARGET
        assert observed["c9"]["state_hash"] == intact.consumed_state_hash
        assert observed["c8"]["state_digest"] == intact.c8_state_digest
    finally:
        product.close()


def test_practice_is_materialized_from_the_committed_target_and_e2(intact, tmp_path):
    product = JoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        a0 = product.observe()
        projects = a0["self"]["state"]["projects"]
        assert len(projects) == 1
        practice = projects[0]
        assert practice["practice_label"] == "coordinated_material_inspection"
        assert practice["source_target_ref"] == intact.target_record_hash
        assert practice["performed_act"] == "inspect_with_tool"
        assert practice["e2_receipt_hash"] == intact.e2_receipt_hash
        assert practice["actor_id"] == intact.life.a_source.actor_id
        assert a0["self"]["state"]["tools_remaining"] == 1
        world = product._world("root")
        assert world.resources["workshop"]["tool_available"] is True
    finally:
        product.close()


def test_without_performed_e2_the_practice_and_world_effect_change(intact, tmp_path):
    """No-effect alternative: the committed target remains, E2 is not performed."""
    seed = seed_mod.build_seed(intact, e2=None)
    assert seed.practice.established is False
    assert seed.c9_e2_admitted is False
    assert seed.world.resources["workshop"]["tool_available"] is False
    product = JoinedProduct(tmp_path / "product", artifacts=intact, e2=None)
    try:
        a0 = product.observe()
        assert a0["status"] == "OK"
        assert a0["c9"]["e2_admitted"] is False
        assert a0["self"]["state"]["projects"] == []
        assert a0["self"]["state"]["tools_remaining"] == 0
        waited = product.wait(30)
        assert waited["clock"] == 40
        event = product.store.world_event("root", waited["offscreen_events"][-1])
        assert event["kind"] == "OFFSCREEN_NO_CHANGE"
        assert product.other()["public"]["completed_units"] == 3
    finally:
        product.close()


def test_fork_shared_root_and_lawful_divergence(intact, tmp_path):
    product = JoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        product.say("branch point")
        fork = product.fork("branch_leave")
        assert fork["shared_root"]["equal"] is True
        product.use("branch_leave")
        assert product.leave_tool()["admitted"] is True
        product.wait(30)
        leave_completed = product.other()["public"]["completed_units"]
        assert leave_completed == 4
        product.use("root")
        assert product.take_tool()["admitted"] is True
        product.wait(30)
        take_completed = product.other()["public"]["completed_units"]
        assert take_completed == 3
        assert product.store.shared_root_equal("branch_leave", "root")["equal"] is True
        leave_events = {e["event_id"] for e in product.store.world_events("branch_leave")}
        root_events = {e["event_id"] for e in product.store.world_events("root")}
        assert leave_events != root_events
    finally:
        product.close()


def test_cold_reentry_in_a_new_process_keeps_the_bp2_target(intact, tmp_path):
    root = tmp_path / "state"
    first = subprocess.run(
        [sys.executable, str(RETURN / "run_joined.py"), "--root", str(root),
         "wait", "30"],
        capture_output=True, text=True, cwd=tmp_path, env=_env())
    assert first.returncode == 0, first.stderr
    binding = json.loads((root / "bp2_join.json").read_text())["artifacts"]
    second = subprocess.run(
        [sys.executable, str(RETURN / "run_joined.py"), "--root", str(root),
         "observe"],
        capture_output=True, text=True, cwd=tmp_path, env=_env())
    assert second.returncode == 0, second.stderr
    observed = json.loads(second.stdout)
    assert observed["status"] == "OK"
    assert observed["clock"] == 40
    assert observed["c9"]["target_id"] == binding["target_id"]
    assert observed["c9"]["state_hash"] == binding["consumed_state_hash"]
    assert observed["c8"]["state_digest"] == binding["c8_state_digest"]
    assert observed["self"]["state"]["projects"][0]["source_target_ref"] == (
        binding["target_record_hash"])
    assert [claim["kind"] for claim in observed["claims"]] == ["ARRIVAL"]


def test_literal_bp2_origin_target_is_actually_consumed(origin_literal, tmp_path):
    assert origin_literal.mode == "ORIGIN_LITERAL"
    assert origin_literal.target_id == (
        "950a4c7903cbe832c72d234a0095946720910c23c8235a28c3118afd8fc1b9f8")
    assert origin_literal.consumed_state_hash == (
        "4907a662d2494d9f7949d1f809195264e001f90d39021feb73e5a75cc31c656d")
    assert origin_literal.c8_state_digest == (
        "058d006c1ce79d2783b02a3bb4e2f92d0672aec9b406b5f3312453f9c5608b4b")
    receipt = joined_downstream_a0_a2_assertion(tmp_path / "literal", origin_literal)
    assert receipt["status"] == "PASS"
    assert receipt["target_id"] == origin_literal.target_id
    assert receipt["consumed_state_hash"] == origin_literal.consumed_state_hash
    assert receipt["a2"]["other_completed_units"] == 4


def test_clock_domains_are_separate_and_never_numerically_ordered(intact, tmp_path):
    product = JoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        source = product.joined_source()
        clock = source["clock"]
        assert clock["bp2_domain"] == "BP2_TEST_ONLY_LOGICAL_CLOCK"
        assert clock["bp4_domain"] == "BP4_TEST_ONLY_WORLD_CLOCK"
        assert clock["bp2_event_time"] == 202
        assert clock["bp2_e2_action_time"] == 217
        assert clock["bp4_world_origin_clock"] == 10
        assert clock["numeric_ordering_used"] is False
        assert clock["relation"] == "DECLARED_PROCESS_ORDER_NOT_NUMERIC_COMPARISON"
        assert clock["process_order"][:3] == [
            "BP2_C8_COMMIT", "BP2_C9_TARGET_COMMIT", "BP2_E2_ADMISSION"]
    finally:
        product.close()


def test_time_coordinate_hold_without_a_join_binding(intact, tmp_path):
    from bp4.store import C12Store

    root = tmp_path / "unbound"
    store = C12Store(root / "c12.sqlite")
    store.create_root("root", clock=10, actor_ids=["A", "B"],
                      state={"world": {}, "actors": {}})
    store.close()
    with pytest.raises(JoinedProductRefusal) as error:
        JoinedProduct(root, artifacts=intact)
    assert error.value.code == "TIME_COORDINATE_HOLD"


def test_envelope_is_recomputed_from_artifacts(intact):
    seed = seed_mod.build_seed(intact)
    status = seed.envelope_validation
    assert status["ok"] is True
    assert status["recomputed_from_artifacts"] is True
    assert status["target_digest_equal_consumed"] is True
    assert seed.envelope["schema"] == (
        "BP2_JOINED_EVENT_HISTORY_TARGET_E2_ENVELOPE@1")
    assert seed.envelope["producer"]["name"] == "BP2_JOINED_PRODUCER"
    assert seed.envelope["native_grants"] == {
        "actor": False, "rule": False, "c8_trust": False, "world": False,
        "c11": False, "c12": False, "adp019": False, "e2": False}
    assert seed.envelope["consumed_state_hash"] == intact.consumed_state_hash
    assert seed.envelope["c8_occurrence_refs"] == ["OCC-0001"]
