"""BP3 independent sourcefree writer/anchor/OUT9/C9 court.

The old accepted OUT9 writer is exercised only through its actual class method;
the candidate must refuse it after installing the executable gate.
"""
from __future__ import annotations

import json
import os
import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "vendor"))
import c8_exclusive_writer as X
import c8o_trusted_outbox as C8O
import outbox_prototype as OP
from c8_readonly_consumer import C8ReadOnlyConsumer
from c9_event_ingress import receive_event


def make_env(tmp_path, *, key_dir=None):
    journal_dir = tmp_path / "journal"
    journal_dir.mkdir()
    key_dir = key_dir or (tmp_path / "keys")
    key_dir.mkdir(parents=True, exist_ok=True)
    key = os.urandom(32)
    import base64
    key_path = key_dir / "writer_keys.json"
    key_path.write_text(json.dumps({"key_id": "BP3-TEST-KEY", "key_b64": base64.b64encode(key).decode()}))
    store = X.WriterKeyStore.load(key_path, "BP3-TEST-KEY")
    anchor = X.KeyedMonotonicAnchor(tmp_path / "anchor" / "rows.json",
                                    tmp_path / "anchor" / "watermark.json", store)
    journal = X.ExclusiveJournal(journal_dir / "journal.json", store=store, anchor=anchor)
    cap = X.KeyedCapability.issue(store, journal.journal_id, "writer-A", ttl_seconds=3600)
    return journal, store, anchor, cap


def candidate(label="C1"):
    return {"candidate_id": label, "payload": {"utterance": "hello"}}


def test_exclusive_append_reaches_actual_out9_consumer():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        event, err, receipt = journal.append_occurrence(candidate(), capability=cap)
        assert event is not None and err is None and receipt is not None
        assert receipt.proof["anchor_seq"] == 0
        journal.verify_journal()
        consumer = C8ReadOnlyConsumer(journal.path)
        view = consumer.load()
        assert view.count() == 1
        readset = consumer.readset()
        assert readset["state_digest"] == receipt.c8o["state_digest"]
        assert readset["writer_version"] == 1
        assert readset["occurrence_ids"] == [event["occurrence_id"]]


def test_old_journal_commit_route_closed_preserves_acknowledged_bytes():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        journal.append_occurrence(candidate(), capability=cap)
        before = journal.path.read_bytes()
        with pytest.raises(X.LegacyWriterRouteClosed):
            OP.Journal(journal.path).commit(OP.make_prototype())
        assert journal.path.read_bytes() == before
        assert C8ReadOnlyConsumer(journal.path).load().count() == 1


def test_forged_capability_refused():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        forged = X.KeyedCapability(**{**cap.__dict__, "signature": "0" * 64})
        with pytest.raises(X.CapabilityRefused):
            journal.commit(OP.make_prototype(), 0, capability=forged)


def test_unkeyed_receipt_forgery_refused_while_out9_would_accept():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        journal.append_occurrence(candidate(), capability=cap)
        raw = json.loads(journal.path.read_text())
        forged = C8O.forged_receipt(raw, writer_id="attacker")
        journal.path.write_text(forged)
        with pytest.raises(X.KeyedProofInvalid):
            journal.verify_journal()


def test_byte_valid_rollback_detected_by_external_anchor():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        journal.append_occurrence(candidate("C1"), capability=cap)
        snap_bytes = journal.path.read_bytes()
        snap_proof = journal._proof_path().read_bytes()
        journal.append_occurrence(candidate("C2"), capability=cap)
        journal.path.write_bytes(snap_bytes)
        journal._proof_path().write_bytes(snap_proof)
        with pytest.raises(X.AnchorRollbackDetected):
            journal.verify_journal()


def test_anchor_offline_refused():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        journal.append_occurrence(candidate(), capability=cap)
        anchor.watermark_path.unlink()
        with pytest.raises(X.AnchorUnavailable):
            journal.verify_journal()


def test_key_store_inside_journal_directory_refused():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        jdir = td / "journal"
        jdir.mkdir()
        keydir = jdir / "keys"
        keydir.mkdir()
        import base64
        key = os.urandom(32)
        kp = keydir / "k.json"
        kp.write_text(json.dumps({"key_id": "K", "key_b64": base64.b64encode(key).decode()}))
        store = X.WriterKeyStore.load(kp, "K")
        anchor = X.KeyedMonotonicAnchor(td / "anchor" / "rows.json", td / "anchor" / "wm.json", store)
        with pytest.raises(X.KeyCustodyNotExternal):
            X.ExclusiveJournal(jdir / "journal.json", store=store, anchor=anchor)


def test_c9_ingress_reads_actual_c8_receipt_without_native_claim():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        event, _, receipt = journal.append_occurrence(candidate(), capability=cap)
        ingress = receive_event(journal.path, proof_verifier=journal.verify_journal)
        assert ingress["occurrence_ids"] == [event["occurrence_id"]]
        assert ingress["state_digest"] == receipt.c8o["state_digest"]
        assert ingress["adp019_admission_receipt"] == "ADP019_ADMISSION_RECEIPT_ABSENT"
        assert ingress["e2_performed"] is False
        assert ingress["native_actor_admitted"] is False
        assert ingress["route_probability"] is None
        assert ingress["selection_weight"] is None


def test_c9_ingress_refuses_wrong_expected_digest():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        journal.append_occurrence(candidate(), capability=cap)
        with pytest.raises(Exception):
            receive_event(journal.path, expected_state_digest="SEVERED", proof_verifier=journal.verify_journal)


def _spawn_workers(tmp_path, journal, store, anchor, count):
    import subprocess
    env = dict(os.environ, PYTHONPATH=str(ROOT) + os.pathsep + str(ROOT / "vendor"))
    procs = []
    for i in range(count):
        procs.append(subprocess.Popen(
            [sys.executable, str(ROOT / "bp3_worker.py"),
             str(journal.path), str(store.path), store.key_id,
             str(anchor.log_path), str(anchor.watermark_path),
             f"writer-{i}", f"PROC-{i}"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=env))
    out = []
    for proc in procs:
        stdout, stderr = proc.communicate(timeout=120)
        out.append((proc.returncode, stdout.strip(), stderr.strip()))
    return out


def test_two_three_five_real_process_writers_no_acknowledged_loss(tmp_path):
    import tempfile
    for count in (2, 3, 5):
        td = Path(tempfile.mkdtemp(dir=tmp_path))
        journal, store, anchor, cap = make_env(td)
        results = _spawn_workers(td, journal, store, anchor, count)
        assert all(rc == 0 for rc, _, _ in results), results
        consumer = C8ReadOnlyConsumer(journal.path)
        view = consumer.load()
        assert view.count() == count
        assert consumer.readset()["writer_version"] == count
        journal.verify_journal()


def test_cold_reopen_sees_only_committed_state(tmp_path):
    import subprocess, tempfile
    with tempfile.TemporaryDirectory(dir=tmp_path) as td:
        journal, store, anchor, cap = make_env(Path(td))
        journal.append_occurrence(candidate(), capability=cap)
        code = (
            "import sys,json;"
            f"sys.path.insert(0,{str(ROOT)!r});"
            f"sys.path.insert(0,{str(ROOT/'vendor')!r});"
            "from c8_readonly_consumer import C8ReadOnlyConsumer;"
            f"c=C8ReadOnlyConsumer({str(journal.path)!r});"
            "print(json.dumps(c.readset()))"
        )
        proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                              env=dict(os.environ, PYTHONPATH=str(ROOT) + os.pathsep + str(ROOT / "vendor")))
        assert proc.returncode == 0, proc.stderr
        readset = json.loads(proc.stdout.strip().splitlines()[-1])
        assert readset["writer_version"] == 1
        assert len(readset["occurrence_ids"]) == 1


def test_old_admit_and_queue_route_closed():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        with pytest.raises(X.LegacyWriterRouteClosed):
            OP.Journal(journal.path).admit_and_queue({"candidate_id": "LEGACY"})


def test_crash_before_rename_preserves_prior_ack(tmp_path):
    import subprocess, tempfile
    with tempfile.TemporaryDirectory(dir=tmp_path) as td:
        journal, store, anchor, cap = make_env(Path(td))
        journal.append_occurrence(candidate("PRIOR"), capability=cap)
        prior = journal.path.read_bytes()
        env = dict(os.environ, PYTHONPATH=str(ROOT) + os.pathsep + str(ROOT / "vendor"))
        proc = subprocess.run([sys.executable, str(ROOT / "bp3_crash_worker.py"),
                               str(journal.path), str(store.path), store.key_id,
                               str(anchor.log_path), str(anchor.watermark_path),
                               "crash", "CRASH-BEFORE", "BEFORE_RENAME"],
                              capture_output=True, text=True, env=env)
        assert proc.returncode != 0
        assert journal.path.read_bytes() == prior
        assert C8ReadOnlyConsumer(journal.path).load().count() == 1


def test_crash_after_commit_has_no_acknowledged_proof(tmp_path):
    import subprocess, tempfile
    with tempfile.TemporaryDirectory(dir=tmp_path) as td:
        journal, store, anchor, cap = make_env(Path(td))
        journal.append_occurrence(candidate("PRIOR"), capability=cap)
        proof_before = journal._proof_path().read_bytes()
        env = dict(os.environ, PYTHONPATH=str(ROOT) + os.pathsep + str(ROOT / "vendor"))
        proc = subprocess.run([sys.executable, str(ROOT / "bp3_crash_worker.py"),
                               str(journal.path), str(store.path), store.key_id,
                               str(anchor.log_path), str(anchor.watermark_path),
                               "crash", "CRASH-AFTER", "AFTER_COMMIT"],
                              capture_output=True, text=True, env=env)
        assert proc.returncode != 0
        assert C8ReadOnlyConsumer(journal.path).load().count() == 2
        assert journal._proof_path().read_bytes() == proof_before
        with pytest.raises(X.KeyedProofInvalid):
            journal.verify_journal()


def test_key_leak_means_external_key_custody_boundary():
    import tempfile, base64
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        # An attacker with the writer key can mint a capability; the proof then
        # verifies. This is intentionally a custody-boundary test, not a claim
        # that a leaked key is detected.
        attacker_store = X.WriterKeyStore(store.path, store.key_id, store.key)
        attacker_cap = X.KeyedCapability.issue(attacker_store, journal.journal_id, "attacker")
        event, err, receipt = journal.append_occurrence(candidate("LEAK"), capability=attacker_cap)
        assert event is not None and receipt is not None
        assert receipt.proof["writer_id"] == "attacker"


def test_anchor_rotated_key_refuses_old_watermark():
    import tempfile, os, base64
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        journal.append_occurrence(candidate(), capability=cap)
        other_key = os.urandom(32)
        other_path = Path(td) / "keys2" / "other.json"
        other_path.parent.mkdir()
        other_path.write_text(json.dumps({"key_id": "OTHER", "key_b64": base64.b64encode(other_key).decode()}))
        other = X.WriterKeyStore.load(other_path, "OTHER")
        rotated = X.KeyedMonotonicAnchor(anchor.log_path, anchor.watermark_path, other)
        with pytest.raises(X.AnchorUnavailable):
            rotated.check(1, journal.verify_journal()["proof"]["receipt_id"])


def test_raw_filesystem_erasure_is_out_of_api_scope_and_typed():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        journal.append_occurrence(candidate(), capability=cap)
        assert C8ReadOnlyConsumer(journal.path).load().count() == 1
        # This is NOT the legacy class method; it is an OS-privileged raw write.
        # The candidate does not claim to prevent it. D1 must install OS/file
        # permissions and an external writer process discipline.
        journal.path.write_text("{}", encoding="utf8")
        with pytest.raises(Exception):
            C8ReadOnlyConsumer(journal.path).load()


def test_lawful_duplicate_is_no_change_not_a_second_append():
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        journal, store, anchor, cap = make_env(Path(td))
        first, err, receipt = journal.append_occurrence(candidate("DUP"), capability=cap)
        assert first is not None and err is None
        before = journal.path.read_bytes()
        second, reason, receipt2 = journal.append_occurrence(candidate("DUP"), capability=cap)
        assert second is None
        assert receipt2 is None
        assert journal.path.read_bytes() == before
        assert C8ReadOnlyConsumer(journal.path).load().count() == 1
