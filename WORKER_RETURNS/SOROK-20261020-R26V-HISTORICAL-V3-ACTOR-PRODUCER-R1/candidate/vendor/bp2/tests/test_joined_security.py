"""Security, crash and owner-boundary tests for the joined producer.

These are honest tests: they assert what the BP3 candidate actually closes in a
process that imports it, and they *also* demonstrate the typed residuals that
are NOT closed (old writer outside the gated import, leaked TEST_ONLY key, crash
after journal rename before the proof sidecar). A residual that is not closed is
reported as a residual, never as a security success.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

import bp2_joined
from bp2_joined.binding import build_world_occurrence
from bp2_joined.producer import JoinedProducer, prepare_journal_env

ROOT = Path(__file__).resolve().parents[1]


def _env() -> dict:
    env = dict(os.environ)
    env["PYTHONHASHSEED"] = "0"
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def _run(code: str, cwd) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True,
        cwd=str(cwd), env=_env())


def test_old_class_writer_route_is_closed_in_the_gated_process(tmp_path):
    import c8_exclusive_writer as writer
    import outbox_prototype as op

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        before = producer.env.journal_path.read_bytes()
        with pytest.raises(writer.LegacyWriterRouteClosed):
            op.Journal(producer.env.journal_path).commit(op.make_prototype())
        with pytest.raises(writer.LegacyWriterRouteClosed):
            op.Journal(producer.env.journal_path).admit_and_queue(
                {"candidate_id": "OLD", "payload": {"x": 1}})
        assert producer.env.journal_path.read_bytes() == before


def test_old_writer_still_callable_outside_the_gated_import_is_a_typed_residual(tmp_path):
    root = tmp_path / "root"
    legacy = tmp_path / "legacy.json"
    vendor = ROOT / "vendor" / "bp3" / "vendor"
    code = f"""
import sys
sys.path.insert(0, {str(vendor)!r})
import outbox_prototype as op
assert not getattr(op.Journal, "_bp3_exclusive_gate", False)
op.Journal({str(legacy)!r}).commit(op.make_prototype())
print("LEGACY_WRITER_AVAILABLE")
"""
    completed = _run(code, tmp_path)
    assert completed.returncode == 0, completed.stderr
    assert "LEGACY_WRITER_AVAILABLE" in completed.stdout
    from c8o_trusted_outbox import LegacyWriterBypassDetected, VersionStateUnreadable
    from c8_readonly_consumer import C8ReadOnlyConsumer

    with pytest.raises((LegacyWriterBypassDetected, VersionStateUnreadable)) as excinfo:
        C8ReadOnlyConsumer(legacy).load()
    assert excinfo.value.code == "LEGACY_WRITER_BYPASS_DETECTED"


def test_forged_capability_is_refused(tmp_path):
    import c8_exclusive_writer as writer

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        env = producer.env
        forged = writer.KeyedCapability(
            **{**env.capability.__dict__, "signature": "0" * 64})
        with pytest.raises(writer.CapabilityRefused):
            env.journal.commit(env.journal.recover()[0], 1, capability=forged)


def test_unkeyed_receipt_forgery_is_refused_by_the_keyed_proof(tmp_path):
    import c8_exclusive_writer as writer
    import c8o_trusted_outbox as c8o

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        env = producer.env
        raw = json.loads(env.journal_path.read_text())
        forged = c8o.forged_receipt(raw, writer_id="attacker")
        env.journal_path.write_text(forged)
        with pytest.raises(writer.KeyedProofInvalid):
            env.journal.verify_journal()


def test_withheld_anchor_and_invalid_anchor_are_refused(tmp_path):
    import c8_exclusive_writer as writer

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        env = producer.env
        env.anchor.watermark_path.unlink()
        with pytest.raises(writer.AnchorUnavailable):
            env.journal.verify_journal()


def test_tampered_anchor_watermark_mac_is_refused(tmp_path):
    import c8_exclusive_writer as writer

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        env = producer.env
        watermark = json.loads(env.anchor.watermark_path.read_text())
        watermark["version"] = watermark["version"] + 99
        env.anchor.watermark_path.write_text(
            json.dumps(watermark, sort_keys=True, separators=(",", ":")))
        with pytest.raises(writer.AnchorUnavailable):
            env.journal.verify_journal()


def test_byte_valid_rollback_with_old_proof_is_detected(tmp_path):
    import c8_exclusive_writer as writer

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        env = producer.env
        journal_bytes = env.journal_path.read_bytes()
        proof_bytes = env.journal._proof_path().read_bytes()
        anchor_rows = env.anchor.log_path.read_bytes()
        second = producer.occurrence.candidate
        second = {**second, "candidate_id": second["candidate_id"] + "-ROLLBACK"}
        env.journal.append_occurrence(second, capability=env.capability)
        env.journal_path.write_bytes(journal_bytes)
        env.journal._proof_path().write_bytes(proof_bytes)
        env.anchor.log_path.write_bytes(anchor_rows)
        with pytest.raises(writer.AnchorRollbackDetected):
            env.journal.verify_journal()


def test_stale_writer_version_is_refused(tmp_path):
    import c8o_trusted_outbox as c8o

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        env = producer.env
        with pytest.raises(c8o.StaleJournalConflict):
            env.journal.append_occurrence(
                {"candidate_id": "STALE", "payload": {"x": 1}},
                capability=env.capability, expected_version=0)


def test_crash_after_journal_rename_before_proof_sidecar_is_not_acknowledged(tmp_path):
    import c8_exclusive_writer as writer
    from c8_readonly_consumer import C8ReadOnlyConsumer
    from c9_event_ingress import C9IngressRefused, receive_event

    root = tmp_path / "crash"
    code = f"""
import sys
sys.path.insert(0, {str(ROOT)!r})
import bp2_joined
bp2_joined.install()
from bp1.composer import build_two_actor_life
from bp2_joined.binding import build_world_occurrence
from bp2_joined.producer import prepare_journal_env
root = {str(root)!r}
env = prepare_journal_env(root)
life = build_two_actor_life()
occurrence = build_world_occurrence(life)
p, version = env.journal.recover()
event = p.ledger.admit(occurrence.candidate)
env.journal.commit(p, version, capability=env.capability,
                   crash_boundary="AFTER_COMMIT")
"""
    completed = _run(code, tmp_path)
    assert completed.returncode == 79, (completed.returncode, completed.stderr)
    env = prepare_journal_env(root)
    raw = json.loads(env.journal_path.read_text())
    assert raw["state_digest"]
    with pytest.raises(writer.KeyedProofInvalid) as excinfo:
        env.journal.verify_journal()
    assert "PROOF_SIDECAR_MISSING" in str(excinfo.value)
    # A raw OUT9 read of the unacknowledged state DOES succeed: this is exactly
    # why the proof-gated joined consumer must refuse it.
    view = C8ReadOnlyConsumer(env.journal_path).load()
    assert view.count() == 1
    with pytest.raises(C9IngressRefused) as excinfo:
        receive_event(env.journal_path, proof_verifier=None)
    assert excinfo.value.code == "PROOF_VERIFIER_REQUIRED"
    with pytest.raises(writer.KeyedProofInvalid):
        receive_event(env.journal_path, proof_verifier=env.journal.verify_journal)


def test_leaked_test_key_can_forge_a_valid_capability_is_a_typed_residual(tmp_path):
    import c8_exclusive_writer as writer

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        env = producer.env
        attacker_store = writer.WriterKeyStore.load(
            env.key_path, env.key_store.key_id)
        attacker_capability = writer.KeyedCapability.issue(
            attacker_store, env.journal.journal_id, "attacker-writer")
        candidate = {"candidate_id": "ATTACKER", "payload": {"utterance": "x"}}
        event, refusal, receipt = env.journal.append_occurrence(
            candidate, capability=attacker_capability)
        # Honest result: the TEST_ONLY key is the whole boundary, so possession
        # of the key file mints a valid capability. This is D2, not a success.
        assert event is not None and receipt is not None
        assert receipt.c8o["writer_id"] == "attacker-writer"
        assert receipt.c8o["capability_trust_grade"] == (
            "CAPABILITY_FORMAT_ONLY_NOT_AUTHENTICATION")


def test_withheld_expected_digest_is_refused_by_out9_ingress(tmp_path):
    from c9_event_ingress import C9IngressRefused, receive_event

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        with pytest.raises(C9IngressRefused) as excinfo:
            receive_event(
                producer.env.journal_path,
                expected_state_digest="SEVERED",
                proof_verifier=producer.env.journal.verify_journal,
            )
        assert excinfo.value.code == "C8_STATE_DIGEST_MISMATCH"


def test_key_store_inside_the_journal_directory_is_refused(tmp_path):
    import c8_exclusive_writer as writer

    journal_dir = tmp_path / "journal"
    key_dir = journal_dir / "keys"
    key_dir.mkdir(parents=True)
    import base64

    key_path = key_dir / "k.json"
    key_path.write_text(json.dumps(
        {"key_id": "K", "key_b64": base64.b64encode(os.urandom(32)).decode()}))
    store = writer.WriterKeyStore.load(key_path, "K")
    anchor = writer.KeyedMonotonicAnchor(
        tmp_path / "anchor" / "rows.json", tmp_path / "anchor" / "wm.json", store)
    with pytest.raises(writer.KeyCustodyNotExternal):
        writer.ExclusiveJournal(journal_dir / "journal.json",
                                store=store, anchor=anchor)


def test_consistently_resealed_forged_durable_record_reddens_the_same_assertion(tmp_path):
    """A forged row that re-seals its own preimage still fails the same assertion.

    C9R's later read accepts a self-consistent row; the joined consumer assertion
    detects that the durable record is no longer the exact committed record.
    """
    import json as _json

    from candidate.canon import digest, seal

    from bp2_joined.producer import joined_consumer_assertion

    with JoinedProducer(tmp_path / "root") as producer:
        outcome = producer.run()
        assert outcome.ok is True
        joined_consumer_assertion(outcome)
        decision = producer.pipeline.decision
        row = producer.c9.db.execute(
            "SELECT body FROM target_state WHERE id=?", (decision.target_id,)
        ).fetchone()
        body = _json.loads(row[0])
        preimage = {k: v for k, v in body["record_preimage"].items() if k != "hash"}
        preimage["governed_payload"] = {"practice_label": "FORGED_LABEL"}
        new_preimage = seal(preimage)
        body["record_preimage"] = new_preimage
        body["record_hash"] = new_preimage["hash"]
        producer.c9.db.execute(
            "UPDATE target_state SET body=? WHERE id=?",
            (_json.dumps(body, sort_keys=True, separators=(",", ":")),
             decision.target_id))
        producer.c9.db.commit()
        e2 = producer.stage_e2()
        assert getattr(e2, "admitted", False) is True
        forged = producer.outcome_after_e2(e2)
        assert forged.ok is True
        with pytest.raises(AssertionError) as excinfo:
            joined_consumer_assertion(forged)
        assert "later read saw a different record" in str(excinfo.value)
        assert digest(_json.loads(_json.dumps(body))) != decision.record_hash
