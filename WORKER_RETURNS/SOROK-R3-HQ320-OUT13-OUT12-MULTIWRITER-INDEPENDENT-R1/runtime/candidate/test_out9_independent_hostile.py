"""HQ314 OUT9 — fresh independent hostile court (not author OUT8/OUT6/OUT7).

Expectations frozen in ../01_INDEPENDENT_FROZEN_EXPECTATIONS.json before this
file was executed. Cases N01-N25 are deliberately complementary to OUT7 I01-I14:
- N01/N02/N09/N23 = legitimate-positive multiviewer + revoked-history survival
- N03-N06 = aggregate/client ACK-count congruence
- N07/N08 = active placeholder vs revoked tombstone
- N10-N13 = detached restore atomicity
- N14-N17 = cold journal recovery + real os._exit crash boundaries (byte-level)
- N18 = remaining-authorized retry
- N19 = terminal ACK immutability across cold
- N20-N22 = revoked emission, ghost opportunity, failed-only client receipt
- N24/N25 = duplicate admission identity, cold-forged revoked tombstone

Source-free custody court only: no human perception, no real client ACK, no
ADP019 authority, no multiwriter proof, no adoption.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from outbox_prototype import (  # noqa: E402
    DeliveryState, Journal, _hash, durable_attempt_id, durable_delivery_id,
    make_prototype,
)


def strict(label="OUT9", **overrides):
    d = dict(
        candidate_id=label, payload={"utterance": "hello-out9"},
        source_refs=["SOURCEFREE_PUBLISHED_ONLY"],
        causal_time="1998-10-03T16:00:00Z",
        artifact_id="ART-1", artifact_digest="DIGEST-1",
        issuer_ref="ISSUER-1", authority_ref="RULE-1", release_ref="R-1",
        participant_refs=["ACTOR-A"], parent_refs=[], envelope_mode="STRICT",
    )
    d.update(overrides)
    return d


def mk(label, grade_decider=True):
    """Admit a STRICT-envelope source-free event under a local adjudicator."""
    p = make_prototype()
    p.ledger.admission_decider = (lambda _: True) if grade_decider else (lambda _: False)
    ev = p.ledger.admit(strict(label))
    assert ev is not None, "strict admission must succeed under local adjudicator"
    return p, ev["occurrence_id"]


def dkey(eid, viewer):
    return durable_delivery_id(eid, viewer)


def chain_ack(p, eid, viewer):
    assert p.outbox.authorize_viewer(eid, viewer)
    assert p.outbox.emit_to(eid, viewer)["state"] == DeliveryState.ADMITTED_UNDELIVERED.value
    assert p.outbox.deliver_to(eid, viewer)["state"] == DeliveryState.DELIVERED_UNACKED.value
    assert p.outbox.ack_to(eid, viewer)["state"] == DeliveryState.ACKNOWLEDGED.value
    assert p.projection.offer(viewer, eid)
    assert p.outbox.deliver(eid) == DeliveryState.DELIVERED_UNACKED
    assert p.outbox.ack(eid) == DeliveryState.ACKNOWLEDGED


def restore_probe(p, bad):
    before = p.snapshot()
    with pytest.raises(ValueError):
        p.restore(bad)
    assert p.snapshot() == before


# ---------------------------------------------------------------------------
# legitimate positives (must validate)
# ---------------------------------------------------------------------------

def test_N01_legitimate_revoked_historical_ack_survives():
    p, eid = mk("N01")
    chain_ack(p, eid, "V")
    assert p.outbox.revoke_viewer(eid, "V")
    p.validate_state()
    assert p.outbox.deliveries[eid]["state"] == DeliveryState.ACKNOWLEDGED.value


def test_N02_multiviewer_congruence_with_one_revoked():
    p, eid = mk("N02")
    chain_ack(p, eid, "A")
    assert p.outbox.authorize_viewer(eid, "B")
    p.outbox.emit_to(eid, "B")
    p.outbox.deliver_to(eid, "B")
    p.outbox.ack_to(eid, "B")
    p.projection.offer("B", eid)
    assert p.outbox.authorize_viewer(eid, "C")
    p.outbox.emit_to(eid, "C")
    p.outbox.deliver_to(eid, "C")
    p.outbox.ack_to(eid, "C")
    p.projection.offer("C", eid)
    assert p.outbox.revoke_viewer(eid, "C")
    p.validate_state()
    assert p.outbox.viewers[eid] == {"A", "B"}
    assert p.outbox.revoked_viewers[eid] == {"C"}


def test_N07_active_not_sent_placeholder_valid():
    p, eid = mk("N07")
    assert p.outbox.authorize_viewer(eid, "V")
    e = p.outbox.emit_to(eid, "V")
    assert e["state"] == DeliveryState.ADMITTED_UNDELIVERED.value
    # return the ACTIVE viewer's receipt to a legitimate never-sent placeholder
    d = p.outbox.client_deliveries[dkey(eid, "V")]
    d.update({"state": DeliveryState.NOT_SENT.value, "attempts": 0,
              "last_attempt_id": None})
    p.outbox.deliveries[eid].update({"state": DeliveryState.NOT_SENT.value,
                                     "attempts": 0, "ack_count": 0})
    p.validate_state()


def test_N09_revoked_legitimate_unacked_survives():
    p, eid = mk("N09")
    assert p.outbox.authorize_viewer(eid, "V")
    p.outbox.emit_to(eid, "V")
    p.outbox.deliver_to(eid, "V")
    assert p.outbox.revoke_viewer(eid, "V")
    d = p.outbox.client_deliveries[dkey(eid, "V")]
    assert d["attempts"] == 1 and d["state"] == DeliveryState.DELIVERED_UNACKED.value
    p.validate_state()


def test_N14_cold_valid_record_recomputed_digest_recovers(tmp_path):
    p, eid = mk("N14")
    chain_ack(p, eid, "V")
    jp = tmp_path / "j14.json"
    Journal(jp).commit(p)
    rec = json.loads(jp.read_text())
    rec["state_digest"] = _hash(rec["state"])  # unkeyed recompute, valid bytes
    jp.write_text(json.dumps(rec))
    q = Journal(jp).recover()
    q.validate_state()
    assert q.outbox.deliveries[eid]["state"] == DeliveryState.ACKNOWLEDGED.value


def test_N16_cold_crash_before_rename_keeps_prior_bytes(tmp_path):
    p, eid = mk("N16")
    chain_ack(p, eid, "V")
    jp = tmp_path / "j16.json"
    Journal(jp).commit(p)
    before = jp.read_bytes()
    code = (
        "import sys\n"
        "sys.path.insert(0, %r)\n"
        "from outbox_prototype import Journal\n"
        "j = Journal(sys.argv[1])\n"
        "p = j.recover()\n"
        "e = 'OCC-0001'\n"
        "assert p.outbox.deliver_to(e, 'V')\n"
        "j.commit(p, crash_boundary='BEFORE_RENAME')\n"
        "raise AssertionError('did not crash')\n" % str(HERE)
    )
    r = subprocess.run([sys.executable, "-c", code, str(jp)],
                       capture_output=True, text=True, timeout=20, cwd=str(HERE))
    assert r.returncode == 79, (r.returncode, r.stdout, r.stderr)
    assert jp.read_bytes() == before  # prior record byte-identical; no partial record
    q = Journal(jp).recover()
    q.validate_state()
    assert q.outbox.deliveries[eid]["state"] == DeliveryState.ACKNOWLEDGED.value


def test_N17_cold_crash_after_commit_recovers_new_state(tmp_path):
    p, eid = mk("N17")
    chain_ack(p, eid, "V")
    jp = tmp_path / "j17.json"
    Journal(jp).commit(p)
    code = (
        "import sys\n"
        "sys.path.insert(0, %r)\n"
        "from outbox_prototype import Journal\n"
        "j = Journal(sys.argv[1])\n"
        "p = j.recover()\n"
        "e = 'OCC-0001'\n"
        "assert p.outbox.authorize_viewer(e, 'W')\n"
        "p.outbox.emit_to(e, 'W')\n"
        "j.commit(p, crash_boundary='AFTER_COMMIT')\n"
        "raise AssertionError('did not crash')\n" % str(HERE)
    )
    r = subprocess.run([sys.executable, "-c", code, str(jp)],
                       capture_output=True, text=True, timeout=20, cwd=str(HERE))
    assert r.returncode == 79, (r.returncode, r.stdout, r.stderr)
    q = Journal(jp).recover()
    q.validate_state()
    assert "W" in q.outbox.viewers[eid]  # newest committed state durable and valid


def test_N18_multiviewer_remaining_authorized_retry():
    p, eid = mk("N18")
    for v in ("A", "B", "C"):
        assert p.outbox.authorize_viewer(eid, v)
    for v in ("A", "B", "C"):
        p.outbox.emit_to(eid, v)
    p.outbox.fail(eid)
    assert p.outbox.retry(eid) == DeliveryState.ADMITTED_UNDELIVERED
    assert p.outbox.revoke_viewer(eid, "C")
    p.outbox.deliver_to(eid, "A")
    p.outbox.ack_to(eid, "A")
    p.projection.offer("A", eid)
    p.validate_state()
    assert p.outbox.deliver(eid) == DeliveryState.DELIVERED_UNACKED
    assert p.outbox.ack(eid) == DeliveryState.ACKNOWLEDGED


def test_N19_ack_terminal_immutability_across_cold(tmp_path):
    p, eid = mk("N19")
    chain_ack(p, eid, "V")
    jp = tmp_path / "j19.json"
    Journal(jp).commit(p)
    p.outbox.fail_to(eid, "V")  # late failure callback cannot reopen terminal ACK
    acked = p.outbox.client_deliveries[dkey(eid, "V")]
    assert acked["state"] == DeliveryState.ACKNOWLEDGED.value and acked["ack_count"] == 1
    Journal(jp).commit(p)
    q = Journal(jp).recover()
    q.validate_state()
    assert q.outbox.deliveries[eid]["state"] == DeliveryState.ACKNOWLEDGED.value


def test_N23_full_valid_chain_cold_reload_positive(tmp_path):
    p, eid = mk("N23")
    chain_ack(p, eid, "A")
    assert p.outbox.authorize_viewer(eid, "B")
    p.outbox.emit_to(eid, "B")
    p.outbox.deliver_to(eid, "B")
    p.outbox.ack_to(eid, "B")
    p.projection.offer("B", eid)
    jp = tmp_path / "j23.json"
    Journal(jp).commit(p)
    q = Journal(jp).recover()
    q.validate_state()
    assert q.outbox.deliveries[eid]["state"] == DeliveryState.ACKNOWLEDGED.value


def test_N24_duplicate_admission_identity():
    p = make_prototype()
    p.ledger.admission_decider = lambda _: True
    first = p.ledger.admit(strict("DUP"))
    second = p.ledger.admit(strict("DUP"))
    assert first is not None and second is not None
    assert p.ledger.count() == 1
    assert first["occurrence_id"] == second["occurrence_id"]


# ---------------------------------------------------------------------------
# hostile typed rejections
# ---------------------------------------------------------------------------

def test_N03_client_zero_attempt_masquerading_as_acked():
    p, eid = mk("N03")
    chain_ack(p, eid, "V")
    d = p.outbox.client_deliveries[dkey(eid, "V")]
    d.update({"attempts": 0, "state": DeliveryState.ACKNOWLEDGED.value,
              "ack_count": 1, "last_attempt_id": None})
    with pytest.raises(ValueError, match="INCONSISTENT_DELIVERY_STATE"):
        p.validate_state()


def test_N04_client_too_many_acks():
    p, eid = mk("N04")
    chain_ack(p, eid, "V")
    p.outbox.client_deliveries[dkey(eid, "V")]["ack_count"] = 2
    with pytest.raises(ValueError, match="BAD_DELIVERY_IDENTITY"):
        p.validate_state()


def test_N05_aggregate_too_many_acks():
    p, eid = mk("N05")
    chain_ack(p, eid, "V")
    p.outbox.deliveries[eid]["ack_count"] = 2
    with pytest.raises(ValueError, match="BAD_AGGREGATE_DELIVERY_COUNTS"):
        p.validate_state()


def test_N06_aggregate_acknowledged_with_zero_attempts():
    p, eid = mk("N06")
    chain_ack(p, eid, "V")
    p.outbox.deliveries[eid]["attempts"] = 0
    with pytest.raises(ValueError, match="BAD_AGGREGATE_DELIVERY_COUNTS"):
        p.validate_state()


def test_N08_revoked_zero_attempt_tombstone_forged():
    p, eid = mk("N08")
    chain_ack(p, eid, "V")
    assert p.outbox.revoke_viewer(eid, "V")
    d = p.outbox.client_deliveries[dkey(eid, "V")]
    d.update({"attempts": 0, "state": DeliveryState.NOT_SENT.value,
              "ack_count": 0, "last_attempt_id": None})
    with pytest.raises(ValueError, match="FORGED_ZERO_ATTEMPT_CLIENT_HISTORY"):
        p.validate_state()


def test_N10_detached_restore_ghost_viewer():
    p, eid = mk("N10")
    chain_ack(p, eid, "V")
    bad = p.snapshot()
    bad["viewers"]["GHOST_OCCURRENCE"] = ["V"]
    restore_probe(p, bad)


def test_N11_detached_restore_revoked_active_intersection():
    p, eid = mk("N11")
    assert p.outbox.authorize_viewer(eid, "V")
    bad = p.snapshot()
    bad["revoked_viewers"] = {eid: ["V"]}
    restore_probe(p, bad)


def test_N12_detached_restore_forged_last_attempt_id():
    p, eid = mk("N12")
    assert p.outbox.authorize_viewer(eid, "V")
    p.outbox.emit_to(eid, "V")
    bad = p.snapshot()
    for d in bad["client_deliveries"].values():
        d["last_attempt_id"] = "ATT_FORGED_9f9f"
    restore_probe(p, bad)


def test_N13_detached_restore_bad_world_state():
    p, eid = mk("N13")
    chain_ack(p, eid, "V")
    bad = p.snapshot()
    bad["world"] = ["not", "a", "dict"]
    restore_probe(p, bad)


def test_N15_cold_tampered_payload_recompute_refused(tmp_path):
    p, eid = mk("N15")
    chain_ack(p, eid, "V")
    jp = tmp_path / "j15.json"
    Journal(jp).commit(p)
    rec = json.loads(jp.read_text())
    rec["state"]["outbox"][eid].update({"state": DeliveryState.ACKNOWLEDGED.value,
                                        "ack_count": 1, "attempts": 0})
    rec["state_digest"] = _hash(rec["state"])
    jp.write_text(json.dumps(rec))
    with pytest.raises(ValueError):
        Journal(jp).recover()


def test_N20_emit_to_revoked_viewer_refused():
    p, eid = mk("N20")
    assert p.outbox.authorize_viewer(eid, "V")
    p.outbox.emit_to(eid, "V")
    assert p.outbox.revoke_viewer(eid, "V")
    assert p.outbox.emit_to(eid, "V") is None
    assert p.outbox.client_deliveries[dkey(eid, "V")]["attempts"] == 1
    p.validate_state()


def test_N21_ghost_opportunity_refused():
    p, eid = mk("N21")
    chain_ack(p, eid, "V")
    bad = p.snapshot()
    bad["opportunity"]["GHOST_USER"] = [eid]
    restore_probe(p, bad)


def test_N22_aggregate_ack_with_only_failed_client_receipt():
    p, eid = mk("N22")
    assert p.outbox.authorize_viewer(eid, "V")
    p.outbox.emit_to(eid, "V")
    p.outbox.fail(eid)
    p.outbox.deliveries[eid].update({"state": DeliveryState.ACKNOWLEDGED.value,
                                     "ack_count": 1, "attempts": 1})
    with pytest.raises(ValueError, match="FORGED_AGGREGATE_ACK_WITHOUT_CLIENT_RECEIPT"):
        p.validate_state()


def test_N25_cold_forged_revoked_tombstone_payload(tmp_path):
    p, eid = mk("N25")
    chain_ack(p, eid, "V")
    assert p.outbox.revoke_viewer(eid, "V")
    jp = tmp_path / "j25.json"
    Journal(jp).commit(p)
    rec = json.loads(jp.read_text())
    k = dkey(eid, "V")
    rec["state"]["client_deliveries"][k].update({"attempts": 0, "state": "NOT_SENT",
                                                 "ack_count": 0,
                                                 "last_attempt_id": None})
    rec["state_digest"] = _hash(rec["state"])
    jp.write_text(json.dumps(rec))
    with pytest.raises(ValueError, match="FORGED_ZERO_ATTEMPT_CLIENT_HISTORY"):
        Journal(jp).recover()
