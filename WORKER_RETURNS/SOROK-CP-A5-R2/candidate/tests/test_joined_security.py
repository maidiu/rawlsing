"""Security, forgery and honest-residual tests for the joined product.

These tests separate what the candidate actually closes from what remains a
typed residual. A shape-valid envelope, a self-performed E2 or a forged world
receipt must be refused; raw database access that drops the C12 append-only
trigger is reported as a residual, not claimed as closed.
"""
from __future__ import annotations

import json
import sqlite3
import types
from pathlib import Path

import pytest

from bp2p4 import reunion, seed as seed_mod
from bp2p4.assertion import joined_downstream_a0_a2_assertion
from bp2p4.envelope import EnvelopeRefusal, verify_producer_envelope
from bp2p4.product import JoinedProduct
from bp2p4.reunion import ReunionRefusal

LITERAL_TARGET = "950a4c7903cbe832c72d234a0095946720910c23c8235a28c3118afd8fc1b9f8"
LITERAL_RECORD = "8d784d48096f4d32d0df3d7c659a23b501681877a948580e0c0150ac60efcd3e"
LITERAL_CONSUMED = "4907a662d2494d9f7949d1f809195264e001f90d39021feb73e5a75cc31c656d"
OLD_BP4_TARGET = "08a8d89a2fca443c668288880a3c889cf3c06c40f12771a10050993ff16a62a6"


def test_shape_valid_envelope_claiming_the_literal_target_is_refused(intact, tmp_path):
    seed = seed_mod.build_seed(intact)
    forged = json.loads(json.dumps(seed.envelope))
    forged["c9_target_refs"] = [LITERAL_TARGET, LITERAL_RECORD]
    forged["consumed_state_hash"] = LITERAL_CONSUMED
    from bp4.bp2_compat import validate_envelope

    # BP4's contract is shape-only and accepts this.
    assert validate_envelope(forged)["ok"] is True
    # The independent re-derivation refuses it because no physical artifact backs it.
    with pytest.raises(EnvelopeRefusal) as error:
        verify_producer_envelope(forged, intact,
                                 world_hash=seed.world.snapshot()["hash"],
                                 clock_bridge=seed.clock.as_dict())
    assert error.value.code == "SHAPE_VALID_ENVELOPE_NOT_BACKED_BY_ARTIFACTS"
    assert "c9_target_refs" in str(error.value) or "consumed_state_hash" in str(error.value)


def test_native_smuggling_in_a_shape_valid_envelope_is_refused(intact):
    seed = seed_mod.build_seed(intact)
    forged = json.loads(json.dumps(seed.envelope))
    forged["native_grants"]["actor"] = True
    forged["authority_grades"]["actor"] = "NATIVE_OWNER_CLAIM"
    from bp4.bp2_compat import validate_envelope

    assert validate_envelope(forged)["ok"] is True
    with pytest.raises(EnvelopeRefusal):
        verify_producer_envelope(forged, intact,
                                 world_hash=seed.world.snapshot()["hash"],
                                 clock_bridge=seed.clock.as_dict())


def test_self_actuator_e2_is_refused(intact):
    receipt = dict(intact.e2_receipt)
    receipt["actuator_ref"] = intact.life.a_source.actor_id
    receipt.pop("hash", None)
    from candidate import seal

    with pytest.raises(ReunionRefusal) as error:
        seed_mod.build_seed(intact, e2=seal(receipt))
    assert error.value.code == "BP2_E2_SELF_PERFORMED"


def test_self_occurrence_e2_is_refused(intact):
    receipt = dict(intact.e2_receipt)
    receipt["occurrence_ref"] = intact.life.a_source.actor_id
    receipt.pop("hash", None)
    from candidate import seal

    with pytest.raises(ReunionRefusal) as error:
        seed_mod.build_seed(intact, e2=seal(receipt))
    assert error.value.code == "BP2_E2_OCCURRENCE_NOT_INDEPENDENT"


def test_forged_world_owner_receipt_is_refused(intact, tmp_path):
    from bp1.canon import digest
    from bp4.c10 import C10Refusal, _verify_world

    product = JoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        product.wait(30)
        state = product._runtime_state("root")
        tampered = {"world": json.loads(json.dumps(state["world"])),
                    "actors": state["actors"]}
        target = next(event for event in tampered["world"]["events"]
                      if event["kind"] == "OFFSCREEN_REPAIR")
        target["owner_receipt"]["owner_ref"] = "SELF"
        target["hash"] = digest({key: value for key, value in target.items()
                                 if key != "hash"})
        tampered["world"]["hash"] = digest(
            {key: value for key, value in tampered["world"].items() if key != "hash"})
        with pytest.raises(C10Refusal) as error:
            _verify_world(tampered)
        assert error.value.code == "WORLD_OWNER_RECEIPT_INVALID"
        assert _verify_world(state).clock == 40
    finally:
        product.close()


def test_c12_append_only_and_future_child_guards(intact, tmp_path):
    from bp4.store import StoreRefusal

    product = JoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        product.say("a real episode so delete triggers actually fire")
        with pytest.raises(Exception):
            product.store.db.execute(
                "UPDATE checkpoint SET clock=1 WHERE branch_id='root'")
        with pytest.raises(Exception):
            product.store.db.execute(
                "DELETE FROM episode WHERE branch_id='root'")
        with pytest.raises(StoreRefusal) as error:
            product.store.append_episode("root", actor_id="A", kind="DO",
                                         clock=1, body={})
        assert error.value.code == "RETROACTIVE_EPISODE"
        with pytest.raises(ValueError):
            product.store.append_episode("root", actor_id="A", kind="DO", clock=11,
                                         body={"future_child_outcome": "forged"})
    finally:
        product.close()


def test_forged_actor_perception_is_caught_by_the_same_assertion(intact, tmp_path):
    """No ghost knowledge: a perception A never had becomes an A0 claim."""
    from bp4.world import make_event, WorldState

    root = tmp_path / "leak"
    product = JoinedProduct(root, artifacts=intact)
    try:
        world = WorldState.restore(product.store.latest_state("root")["world"])
        event = make_event(
            clock=10, kind="SPEECH", actor_id="B", location="market",
            summary="B speaks where A has never been.", body={"text": "forged"},
            sequence=len(world.events))
        world.add_event(event)
        product.store.append_world_event("root", event)
        product.store.record_perception("root", actor_id="A",
                                        event_id=event["event_id"], clock=10,
                                        channel="forged")
        product.store.checkpoint("root", 10, {"world": world.snapshot(),
                                              "actors": product.store.latest_state(
                                                  "root")["actors"]})
    finally:
        product.close()
    with pytest.raises(AssertionError) as error:
        joined_downstream_a0_a2_assertion(root, intact)
    assert "A0_CLAIM_SET" in str(error.value)


def test_bp4_own_c10_refuses_a_tampered_target_preimage(tmp_path):
    from bp4.c10 import C10Refusal, _read_c9

    fresh = reunion.build_fresh(tmp_path / "bp2")
    with sqlite3.connect(fresh.c9_path) as db:
        row = db.execute("SELECT body FROM target_state WHERE id=?",
                         (fresh.target_id,)).fetchone()
        body = json.loads(row[0])
        body["record_preimage"]["governed_payload"]["practice_label"] = "TAMPERED"
        db.execute("UPDATE target_state SET body=? WHERE id=?",
                   (json.dumps(body, sort_keys=True, separators=(",", ":")),
                    fresh.target_id))
        db.commit()
    seed = types.SimpleNamespace(c9_path=fresh.c9_path,
                                 c9_target_id=fresh.target_id,
                                 c9_state_hash=fresh.consumed_state_hash)
    with pytest.raises(C10Refusal) as error:
        _read_c9(seed)
    # A rewritten preimage is no longer a sealed record; BP4's own read refuses
    # before any digest comparison can be reached.
    assert error.value.code in {"C9_TARGET_PREIMAGE_UNSEALED",
                                "C9_TARGET_PREIMAGE_DIGEST_MISMATCH"}


def test_raw_database_access_can_drop_the_append_only_trigger_is_a_residual(
        intact, tmp_path):
    """Honest residual: append-only is an in-process guard, not an OS boundary."""
    from bp2p4.c12_verify import chain_digest, verify_branch_chain

    root = tmp_path / "residual"
    product = JoinedProduct(root, artifacts=intact)
    try:
        product.say("a real utterance")
        db_path = product.store.path
        before_digest = chain_digest(product.store, "root")
        before_counts = verify_branch_chain(product.store, "root")["counts"]
    finally:
        product.close()
    with sqlite3.connect(db_path) as db:
        db.execute("DROP TRIGGER IF EXISTS episode_no_delete")
        deleted = db.execute("DELETE FROM episode WHERE branch_id='root'").rowcount
        db.commit()
    from bp4.store import C12Store

    store = C12Store(db_path)
    try:
        assert deleted >= 1
        after = verify_branch_chain(store, "root")
        # Remaining rows are intact; the deletion itself is only visible against
        # the out-of-band chain digest recorded before the attack.
        assert after["ok"] is True
        assert after["counts"]["episode"] == 0 < before_counts["episode"]
        assert chain_digest(store, "root") != before_digest
        assert store.episodes("root") == []
    finally:
        store.close()


def test_upstream_bp4_store_verify_is_self_referential(intact, tmp_path):
    from bp2p4.c12_verify import upstream_verify_defect

    product = JoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        report = upstream_verify_defect(product.store, "root")
        assert report["upstream_verify"]["ok"] is False
        assert report["independent_verify"]["ok"] is True
        assert report["agrees"] is False
        assert "including the body's own hash" in report["upstream_defect"]
    finally:
        product.close()


def test_old_bp1_only_target_is_not_the_joined_consumer(intact, tmp_path):
    from bp4.product import BP4Product

    standalone = BP4Product(tmp_path / "bp4_only")
    try:
        assert standalone.seed.c9_target_id == OLD_BP4_TARGET
    finally:
        standalone.close()
    product = JoinedProduct(tmp_path / "joined", artifacts=intact)
    try:
        observed = product.observe()
        assert observed["c9"]["target_id"] == intact.target_id
        assert observed["c9"]["target_id"] != OLD_BP4_TARGET
    finally:
        product.close()


def test_joined_reconciliation_matches_bp2_committed_evidence(intact):
    reconciliation = reunion.reconciliation(intact.receipt["persisted"], intact)
    exact = [row for row in reconciliation["rows"] if row["class"] == "EXACT"]
    assert len(exact) >= 19
    assert reconciliation["recomputed_count"] >= 10
    for row in reconciliation["rows"]:
        if row["class"] == "EXACT":
            assert row["actual"] == row["expected"]
        assert row["class"] != "MISMATCH"
