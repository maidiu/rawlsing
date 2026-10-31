"""Five actual same-product source-edge severances with restoration."""
from __future__ import annotations

import shutil
import sqlite3

import pytest

from bp4.c10 import C10Refusal, receive, _verify_world
from bp4.perception import render_requested_event
from bp4.product import BP4Product


def test_severance_c9_target_removed(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        assert p.observe()["status"] == "OK"
        copy = tmp_path / "c9_missing.sqlite"
        shutil.copy(p.seed.c9_path, copy)
        with sqlite3.connect(copy) as db:
            db.execute("DELETE FROM target_state")
            db.commit()
        original = p.seed.c9_path
        p.seed.c9_path = copy
        try:
            held = p.observe()
            assert held["status"] == "HELD"
            assert held["code"] == "C9_TARGET_MISSING"
        finally:
            p.seed.c9_path = original
        assert p.observe()["status"] == "OK"
    finally:
        p.close()


def test_severance_bp1_actor_source(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        ok = receive(p.seed, p.store, "root", actor_id="A")
        assert ok.receipt["c9_target_id"] == p.seed.c9_target_id
        with pytest.raises(C10Refusal) as err:
            receive(p.seed, p.store, "root", actor_id="A", expected_a_hash="0" * 64)
        assert err.value.code == "BP1_ACTOR_SOURCE_NOT_AUTHENTICATED"
        assert receive(p.seed, p.store, "root", actor_id="A").receipt["c9_target_id"]
    finally:
        p.close()


def test_severance_bp3_receipt_substituted(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        assert receive(p.seed, p.store, "root", actor_id="A").c8_ingress["occurrence_ids"]
        def bad_verifier():
            raise RuntimeError("substituted proof")
        with pytest.raises(C10Refusal) as err:
            receive(p.seed, p.store, "root", actor_id="A", proof_verifier=bad_verifier)
        assert err.value.code == "BP3_PROOF_INVALID"
        assert receive(p.seed, p.store, "root", actor_id="A").c8_ingress["occurrence_ids"]
    finally:
        p.close()


def test_severance_actor_perception_boundary(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        p.wait(30)
        state = p._runtime_state("root")
        events = p.store.world_events("root")
        offscreen = next(e for e in events if e["kind"] == "OFFSCREEN_REPAIR")
        hidden = render_requested_event("A", 40, state, events, offscreen["event_id"])
        assert hidden["state"] == "NONRENDERABLE"
        assert hidden["code"] == "NO_ACTOR_PERCEPTION"
        p.travel("market")
        p.attend()
        state = p._runtime_state("root")
        visible = render_requested_event("A", 40, state, p.store.world_events("root"),
                                         offscreen["event_id"])
        assert visible["state"] == "READY"
    finally:
        p.close()


def test_severance_offscreen_self_attestation(tmp_path):
    p = BP4Product(tmp_path / "state")
    try:
        p.wait(30)
        state = p._runtime_state("root")
        assert _verify_world(state).clock == 40
        tampered = {
            "world": dict(state["world"]),
            "actors": state["actors"],
        }
        tampered["world"]["events"] = [dict(e) for e in state["world"]["events"]]
        target = next(e for e in tampered["world"]["events"]
                      if e["kind"] == "OFFSCREEN_REPAIR")
        target["owner_receipt"] = dict(target["owner_receipt"])
        target["owner_receipt"]["owner_ref"] = "SELF"
        from bp4.canon import digest
        target["hash"] = digest({k: v for k, v in target.items() if k != "hash"})
        tampered["world"]["hash"] = digest(
            {k: v for k, v in tampered["world"].items() if k != "hash"})
        with pytest.raises(C10Refusal) as err:
            _verify_world(tampered)
        assert err.value.code == "WORLD_OWNER_RECEIPT_INVALID"
        assert _verify_world(state).clock == 40
    finally:
        p.close()
