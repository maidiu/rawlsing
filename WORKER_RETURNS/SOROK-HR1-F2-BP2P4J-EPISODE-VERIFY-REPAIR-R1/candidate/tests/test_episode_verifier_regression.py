"""Focused BP2P4J C12 episode preimage regression.

A valid ``say`` writes ``episode_id`` after hashing the episode body. The
independent verifier must exclude that derived field from the preimage while
still rejecting tampered bodies, hashes and derived ids.
"""
from __future__ import annotations

import json
import sqlite3

from bp2p4.c12_verify import chain_digest, verify_branch_chain
from bp2p4.product import JoinedProduct


def test_valid_say_episode_is_green_and_preserves_the_post_hash_id(intact, tmp_path):
    product = JoinedProduct(tmp_path / "product", artifacts=intact)
    try:
        spoken = product.say("a real episode before verification")
        row = product.store.db.execute(
            "SELECT seq, body, hash FROM episode WHERE branch_id='root' ORDER BY seq"
        ).fetchone()
        body = json.loads(row[1])
        report = verify_branch_chain(product.store, "root")
        assert report["ok"] is True, {
            "report": report, "seq": row[0], "stored_hash": row[2],
            "episode_id": body.get("episode_id"), "body": body}
        assert report["counts"]["episode"] == 1
        assert report["errors"] == []
        assert body["episode_id"] == "TEST_ONLY_BP4_EP_" + body["hash"]
        assert body["hash"] == row[2]
        assert body["body"]["event_id"] == spoken["event_id"]
    finally:
        product.close()


def test_tampered_episode_body_stays_red(intact, tmp_path):
    product = JoinedProduct(tmp_path / "tampered_body", artifacts=intact)
    try:
        product.say("tamper target")
        db_path = str(product.store.path)
    finally:
        product.close()
    with sqlite3.connect(db_path) as db:
        db.execute("DROP TRIGGER IF EXISTS episode_no_update")
        seq, body = db.execute(
            "SELECT seq, body FROM episode WHERE branch_id='root' ORDER BY seq"
        ).fetchone()
        parsed = json.loads(body)
        parsed["body"]["event_id"] = "0" * 64
        db.execute("UPDATE episode SET body=? WHERE branch_id='root' AND seq=?",
                   (json.dumps(parsed, sort_keys=True, separators=(",", ":")), seq))
        db.commit()
    from bp4.store import C12Store
    store = C12Store(db_path)
    try:
        report = verify_branch_chain(store, "root")
        assert report["ok"] is False
        assert report["errors"] == ["episode:0:body_hash_mismatch"]
        assert report["counts"]["episode"] == 1
    finally:
        store.close()


def test_tampered_episode_id_is_refused_without_waiving_preimage(intact, tmp_path):
    product = JoinedProduct(tmp_path / "tampered_id", artifacts=intact)
    try:
        product.say("tamper id target")
        db_path = str(product.store.path)
    finally:
        product.close()
    with sqlite3.connect(db_path) as db:
        db.execute("DROP TRIGGER IF EXISTS episode_no_update")
        seq, body = db.execute(
            "SELECT seq, body FROM episode WHERE branch_id='root' ORDER BY seq"
        ).fetchone()
        parsed = json.loads(body)
        parsed["episode_id"] = "TEST_ONLY_BP4_EP_" + "0" * 64
        db.execute("UPDATE episode SET body=? WHERE branch_id='root' AND seq=?",
                   (json.dumps(parsed, sort_keys=True, separators=(",", ":")), seq))
        db.commit()
    from bp4.store import C12Store
    store = C12Store(db_path)
    try:
        report = verify_branch_chain(store, "root")
        assert report["ok"] is False
        assert report["errors"] == ["episode:0:episode_id_mismatch"]
    finally:
        store.close()


def test_tampered_world_event_body_stays_red(intact, tmp_path):
    product = JoinedProduct(tmp_path / "tampered_world", artifacts=intact)
    try:
        product.say("world event target")
        product.wait(30)
        db_path = str(product.store.path)
    finally:
        product.close()
    with sqlite3.connect(db_path) as db:
        db.execute("DROP TRIGGER IF EXISTS world_event_no_update")
        seq, body = db.execute(
            "SELECT seq, body FROM world_event WHERE branch_id='root' ORDER BY seq"
        ).fetchone()
        parsed = json.loads(body)
        parsed["summary"] = "tampered world event"
        db.execute("UPDATE world_event SET body=? WHERE branch_id='root' AND seq=?",
                   (json.dumps(parsed, sort_keys=True, separators=(",", ":")), seq))
        db.commit()
    from bp4.store import C12Store
    store = C12Store(db_path)
    try:
        report = verify_branch_chain(store, "root")
        assert report["ok"] is False
        assert "world_event:0:body_hash_mismatch" in report["errors"]
    finally:
        store.close()


def test_cold_reopen_keeps_the_episode_chain_green(intact, tmp_path):
    product = JoinedProduct(tmp_path / "cold", artifacts=intact)
    try:
        product.say("cold reopen episode")
        before = chain_digest(product.store, "root")
        row = product.store.db.execute(
            "SELECT body, hash FROM episode WHERE branch_id='root' ORDER BY seq"
        ).fetchone()
        expected = json.loads(row[0])
        db_path = str(product.store.path)
    finally:
        product.close()
    from bp4.store import C12Store
    store = C12Store(db_path)
    try:
        report = verify_branch_chain(store, "root")
        assert report["ok"] is True, report
        assert report["counts"]["episode"] == 1
        reopened = store.episodes("root")[0]
        assert reopened["hash"] == row[1] == expected["hash"]
        assert reopened["episode_id"] == expected["episode_id"]
        assert chain_digest(store, "root") == before
    finally:
        store.close()
