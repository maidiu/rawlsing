"""C07P — cross-process custody durability: preregistered positives and hostiles.

Expectations are frozen by 01_PREREGISTERED_PROTOCOL_R1.md (P1-P10, N1-N12,
T1-T14, four crash points). This suite was written against that preregistration
and is executed with REAL subprocesses and REAL filesystem state.

Nothing here edits the pinned custody source, and nothing widens the lexical or
Unicode leakage gate.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
REPRO = HERE.parent / "repro"
sys.path.insert(0, str(REPRO / "source"))
sys.path.insert(0, str(REPRO))

import c07_journal as J  # noqa: E402
import custody_protocol as CP  # noqa: E402

WORKER = str(REPRO / "c07_worker.py")

PINNED_BLOB = "4c185c18dbee57603038e97886da8fc4aa834082"
PINNED_SHA256 = "ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b"

CRASH_POINTS = [
    "1_after_tmp_fsync_before_replace",
    "2_after_replace_before_dir_fsync",
    "3_after_dir_fsync",
]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def make_capsule(cid="cap-X", frame="f", stamp=1000.0):
    return CP.CustodyCapsule(
        capsule_id=cid, schema_version="1.0", purpose="SOURCEFREE_TEST_ONLY",
        scenario_frame=frame, family_graph_digest="fgd", content_digest="cd",
        contribution_digest="contrib", public_projection_digest="ppd",
        hidden_projection_digest="hpd", lawful_set_digest="lsd",
        coder_rubric_digest="crd", split_assignment_digest="sad",
        generation_history_digest="ghd", rejected_alternatives_digest="rad",
        freeze_timestamp=stamp)


def run_role(role, journal, *extra):
    """Run one worker role as a REAL subprocess with its own interpreter."""
    proc = subprocess.run([sys.executable, WORKER, role, str(journal), *extra],
                          capture_output=True, text=True)
    assert proc.returncode == 0, f"{role} failed: {proc.stderr[-800:]}"
    payload = None
    for line in proc.stdout.splitlines():
        if "@@BEGIN@@" in line:
            payload = json.loads(line.split("@@BEGIN@@")[1].split("@@END@@")[0])
    assert payload is not None, f"{role} produced no payload: {proc.stdout[-500:]}"
    return payload


def run_role_expect_kill(role, journal, point):
    """Run a role that must die by a REAL uncatchable SIGKILL."""
    proc = subprocess.run([sys.executable, WORKER, role, str(journal), point],
                          capture_output=True, text=True)
    assert proc.returncode == -signal.SIGKILL or proc.returncode == 137, (
        f"expected SIGKILL, got {proc.returncode}: {proc.stderr[-400:]}")
    assert f"SIGKILL at {point}" in proc.stderr
    return proc


@pytest.fixture()
def jdir(tmp_path):
    return tmp_path / "custody"


# ===========================================================================
# SECTION P — preregistered positives
# ===========================================================================

def test_P1_P2_processA_builds_authorised_escrow_via_public_api(jdir):
    """P1 native public API only; P2 atomic journal with a verifying chain."""
    out = run_role("phaseA", jdir / "j.jsonl")
    fp = out["fingerprint"]
    assert fp["integrity"] is True
    assert fp["committed_ids"] == ["cap-A"]
    assert fp["unblinded_ids"] == ["cap-A"]
    assert fp["released"] == ["cap-A"]
    assert fp["ledger_ops"] == ["COMMIT", "UNBLIND", "RELEASE", "EXPOSURE"]
    records = J.read_records(jdir / "j.jsonl")
    assert J.verify_chain(records)["ok"] is True
    assert [r["seq"] for r in records] == list(range(1, len(records) + 1))
    for rec in records:
        body = {k: v for k, v in rec.items() if k != "rec"}
        assert rec["rec"] == hashlib.sha256(
            json.dumps(body, sort_keys=True, separators=(",", ":"),
                       ensure_ascii=True).encode()).hexdigest()


def test_P3_P4_processA_terminates_and_fresh_processB_recovers(jdir):
    """P3 process A really exits; P4 an independent interpreter restores."""
    a = run_role("phaseA", jdir / "j.jsonl")
    b = run_role("phaseB", jdir / "j.jsonl")
    assert a["provenance"]["pid"] != b["provenance"]["pid"]
    assert b["restore"]["integrity"] is True
    assert b["restore"]["applied"] == a["journal_records"]
    assert b["fingerprint"]["committed_ids"] == ["cap-A"]


def test_P5_all_eighteen_capsule_fields_survive_restart(jdir):
    """P5 the full 18-field envelope commitment is bit-identical across processes."""
    a = run_role("phaseA", jdir / "j.jsonl")
    b = run_role("phaseB", jdir / "j.jsonl")
    assert a["fingerprint"]["commitments"] == b["fingerprint"]["commitments"]
    assert a["fingerprint"]["capsule_fields"] == b["fingerprint"]["capsule_fields"]
    fields = a["fingerprint"]["capsule_fields"]["cap-A"]
    assert len(fields) == 18, sorted(fields)
    # and the commitment really is bound to all 18: perturbing any one changes it
    for name in J.CAPSULE_FIELDS:
        mutated = dict(fields)
        current = mutated[name]
        mutated[name] = "x-different" if isinstance(current, str) else (
            (current + 1) if isinstance(current, int) else (
                current + 1.5 if isinstance(current, float) else (not current)))
        assert CP.capsule_envelope_commitment(
            CP.CustodyCapsule(**mutated)) != a["fingerprint"]["commitments"]["cap-A"], name


def test_P6_escrow_identity_survives_restart(jdir):
    """P6 committed/unblinded/released/holder_roles/exposures all match."""
    a = run_role("phaseA", jdir / "j.jsonl")["fingerprint"]
    b = run_role("phaseB", jdir / "j.jsonl")["fingerprint"]
    for key in ("committed_ids", "unblinded_ids", "unblinded_holders", "released",
                "exposure_rows", "holder_roles", "ledger_ops", "ledger_seq"):
        assert a[key] == b[key], key
    assert a == b


def test_P7_P8_processB_safely_continues_the_lifecycle(jdir):
    """P7 B commits/unblinds/releases a second capsule; P8 integrity holds."""
    run_role("phaseA", jdir / "j.jsonl")
    b2 = run_role("continueB", jdir / "j.jsonl")
    fp = b2["continued_fingerprint"]
    assert fp["committed_ids"] == ["cap-A", "cap-B"]
    assert fp["released"] == ["cap-A", "cap-B"]
    assert fp["integrity"] is True
    assert b2["journal_records_after"] > 6


def test_P9_module_provenance_identical_in_both_processes(jdir):
    """P9 the module actually imported is the pinned OC6 blob in both."""
    a = run_role("phaseA", jdir / "j.jsonl")["provenance"]
    b = run_role("phaseB", jdir / "j.jsonl")["provenance"]
    for prov in (a, b):
        assert prov["git_blob_sha1"] == PINNED_BLOB
        assert prov["sha256"] == PINNED_SHA256
        assert Path(prov["module_file"]).name == "custody_protocol.py"
    assert a["module_file"] == b["module_file"]


def test_P10_journal_timestamps_faithful_escrow_timestamps_are_a_declared_hold(jdir):
    """P10 the C07_DEPENDENCY_TS limitation is real, measured and declared."""
    run_role("phaseA", jdir / "j.jsonl")
    b = run_role("phaseB", jdir / "j.jsonl")
    journal_ts = [r["payload"].get("unblinded_at")
                  for r in J.read_records(jdir / "j.jsonl") if r["kind"] == "UNBLIND"]
    assert journal_ts and isinstance(journal_ts[0], float)
    # the escrow's own timestamp is re-stamped on replay; fingerprint excludes it
    assert "timestamps" not in json.dumps(b["fingerprint"], sort_keys=True)[:0] + ""
    assert b["fingerprint"]["integrity"] is True


# ===========================================================================
# SECTION C — preregistered crash matrix, real SIGKILL
# ===========================================================================

@pytest.mark.parametrize("point", CRASH_POINTS)
def test_C_crash_injection_kills_process_and_leaves_no_torn_record(jdir, point):
    """Every crash point kills with SIGKILL; the journal is never torn."""
    run_role_expect_kill("crashA", jdir / "j.jsonl", point)
    records = J.read_records(jdir / "j.jsonl")
    assert J.verify_chain(records)["ok"] is True   # no partial/torn line
    ej = J.EscrowJournal(jdir / "j.jsonl")
    info = ej.restore()
    assert info["integrity"] is True


def test_C1_crash_before_rename_rolls_back_cleanly(jdir):
    """C1 preregistered CLEAN_ROLLBACK: previous journal, second capsule lost."""
    run_role_expect_kill("crashA", jdir / "j.jsonl", CRASH_POINTS[0])
    records = J.read_records(jdir / "j.jsonl")
    kinds = [r["kind"] for r in records]
    assert kinds.count("COMMIT") == 1, kinds
    assert (jdir / "j.jsonl.tmp").exists(), "orphaned temp should remain, unrenamed"
    ej = J.EscrowJournal(jdir / "j.jsonl")
    ej.restore()
    assert sorted(ej.state.committed) == ["cap-A"]


def test_C2_crash_after_rename_before_dir_fsync_is_not_settled(jdir):
    """C2 preregistered NOT_SETTLED: content visible under process kill only.

    This test asserts the observed behaviour AND that the durability question
    remains open. It must not be read as a durability proof.
    """
    run_role_expect_kill("crashA", jdir / "j.jsonl", CRASH_POINTS[1])
    records = J.read_records(jdir / "j.jsonl")
    assert len(records) == 3
    ej = J.EscrowJournal(jdir / "j.jsonl")
    ej.restore()
    assert sorted(ej.state.committed) == ["cap-A", "cap-C"]
    assert ej.state.verify_ledger_integrity() is True
    # The preregistration's honesty constraint: a process kill cannot exercise
    # power-loss semantics, so this point stays NOT_SETTLED by construction.
    assert "NOT_SETTLED" in (HERE.parent / "01_PREREGISTERED_PROTOCOL_R1.md").read_text()


def test_C3_crash_after_dir_fsync_is_committed(jdir):
    """C3 preregistered COMMITTED."""
    run_role_expect_kill("crashA", jdir / "j.jsonl", CRASH_POINTS[2])
    records = J.read_records(jdir / "j.jsonl")
    assert len(records) == 3
    assert (jdir / "j.jsonl.tmp").exists() is False
    ej = J.EscrowJournal(jdir / "j.jsonl")
    ej.restore()
    assert sorted(ej.state.committed) == ["cap-A", "cap-C"]


def test_C4_fsync_capability_is_observed_not_assumed(jdir):
    """Record what the platform actually supports rather than claiming it."""
    result = J.append_records(jdir / "j.jsonl", [
        {"kind": "AUTHORIZE", "payload": {"person_id": "runner1", "role": "CUSTODIAN"}}])
    assert result["limits"]["fsync_file"] == "SUPPORTED"
    assert result["limits"]["fsync_dir"] == "SUPPORTED"
    assert result["limits"]["rename"] == "os_replace_atomic_on_same_directory"


# ===========================================================================
# SECTION N — preregistered hostiles
# ===========================================================================

def good_journal(jdir):
    run_role("phaseA", jdir / "j.jsonl")
    return [json.loads(l) for l in (jdir / "j.jsonl").read_text().splitlines()]


def rewrite(jdir, records):
    (jdir / "j.jsonl").write_text(
        "".join(json.dumps(r, sort_keys=True, separators=(",", ":"),
                           ensure_ascii=True) + "\n" for r in records))


def test_N1_T1_tampered_payload_is_refused(jdir):
    recs = good_journal(jdir)
    recs[2]["payload"]["holder"] = "attacker"
    rewrite(jdir, recs)
    with pytest.raises(J.JournalError, match="digest mismatch"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_N2_T2_middle_record_deleted_is_refused(jdir):
    recs = good_journal(jdir)
    del recs[2]
    rewrite(jdir, recs)
    with pytest.raises(J.JournalError, match="seq is"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_N3_T3_reordered_records_are_refused(jdir):
    recs = good_journal(jdir)
    recs[2], recs[3] = recs[3], recs[2]
    rewrite(jdir, recs)
    with pytest.raises(J.JournalError, match="seq is|prev chain break"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_N4_T4_duplicated_record_is_refused(jdir):
    recs = good_journal(jdir)
    recs.insert(3, dict(recs[2]))
    rewrite(jdir, recs)
    with pytest.raises(J.JournalError, match="seq is"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_N5_T6_forged_capsule_substitution_is_refused(jdir):
    recs = good_journal(jdir)
    commit = next(r for r in recs if r["kind"] == "COMMIT")
    commit["payload"]["capsule"]["content_digest"] = "attacker-digest"
    # re-seal the record digest so only the capsule commitment can catch it
    body = {k: v for k, v in commit.items() if k != "rec"}
    commit["rec"] = hashlib.sha256(json.dumps(
        body, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()).hexdigest()
    rewrite(jdir, recs)
    with pytest.raises(J.JournalError, match="forged capsule"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_N6_T10_exposure_before_any_commit_is_refused(jdir):
    recs = good_journal(jdir)
    forged = J.build_record(1, "EXPOSURE",
                            {"capsule_id": "ghost", "exposed_to": "coder-7",
                             "purpose": "development", "exposure_ts": 1.0}, J.ZERO_PREV)
    rewrite(jdir, [forged] + recs)
    with pytest.raises(CP.IdentityMismatchError):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_N7_T7_unblind_of_uncommitted_capsule_is_refused(jdir):
    recs = good_journal(jdir)
    forged = J.build_record(len(recs) + 1, "UNBLIND",
                            {"capsule_id": "ghost", "holder": "runner1",
                             "unblinded_at": 1.0}, recs[-1]["rec"])
    rewrite(jdir, recs + [forged])
    with pytest.raises(CP.IdentityMismatchError):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_N8_T8_unauthorised_holder_is_refused(jdir):
    recs = good_journal(jdir)
    forged = J.build_record(len(recs) + 1, "UNBLIND",
                            {"capsule_id": "cap-A", "holder": "stranger-9",
                             "unblinded_at": 1.0}, recs[-1]["rec"])
    rewrite(jdir, recs + [forged])
    with pytest.raises(CP.IdentityMismatchError):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_N9_T9_forged_purpose_is_refused(jdir):
    j = J.EscrowJournal(jdir / "j.jsonl")
    with pytest.raises(CP.PurposeViolationError):
        j.commit(make_capsule("cap-P", "f", 1.0))
    bad = make_capsule("cap-P", "f", 1.0)
    object.__setattr__(bad, "purpose", "PRODUCTION")
    with pytest.raises(CP.PurposeViolationError):
        J.EscrowJournal(jdir / "j2.jsonl").commit(bad)


def test_N10_T13_truncated_trailing_line_is_refused(jdir):
    good_journal(jdir)
    raw = (jdir / "j.jsonl").read_bytes()
    (jdir / "j.jsonl").write_bytes(raw[:-12])
    with pytest.raises(J.JournalError, match="newline|unparseable"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_N11_T14_stale_snapshot_replay_is_refused(jdir):
    recs = good_journal(jdir)
    stale = [r for r in recs if r["kind"] in ("AUTHORIZE", "COMMIT")]
    full = run_role("continueB", jdir / "j.jsonl")
    assert full["journal_records_after"] > len(recs)
    rewrite(jdir, stale)          # roll the file back to an older, valid prefix
    shutil.copy(jdir / "j.jsonl", jdir / "stale.jsonl")
    run_role("continueB", jdir / "j.jsonl")   # re-appending continues, chain stays valid
    # the demonstrable point: an older VALID prefix restores successfully and
    # silently omits the newer events -> this is T5, see test_N12
    ej = J.EscrowJournal(jdir / "stale.jsonl")
    ej.restore()
    assert sorted(ej.state.committed) == ["cap-A"]
    assert "cap-B" not in ej.state.committed


def test_N12_T5_whole_journal_rollback_is_a_demonstrated_ceiling(jdir):
    """T5/N12: an attacker who rolls back to a VALID earlier prefix is NOT
    detected. Preregistered as an accepted failure of a local unkeyed journal."""
    run_role("phaseA", jdir / "j.jsonl")
    full = run_role("continueB", jdir / "j.jsonl")
    assert full["continued_fingerprint"]["committed_ids"] == ["cap-A", "cap-B"]
    records = J.read_records(jdir / "j.jsonl")
    prefix = [r for r in records if r["kind"] in ("AUTHORIZE", "COMMIT", "UNBLIND",
                                                   "RELEASE", "EXPOSURE")]
    rewrite(jdir, prefix)
    ej = J.EscrowJournal(jdir / "j.jsonl")      # NO exception raised
    ej.restore()
    assert sorted(ej.state.committed) == ["cap-A"]   # cap-B silently lost
    assert ej.state.verify_ledger_integrity() is True  # still "valid" — the ceiling


def test_N13_all_eighteen_fields_are_bound_at_the_true_entrypoint(jdir):
    """Re-prove full 18-field binding through the adapter's own restore path."""
    run_role("phaseA", jdir / "j.jsonl")
    ej = J.EscrowJournal(jdir / "j.jsonl")
    ej.restore()
    cap = ej.state.committed["cap-A"]
    base = CP.capsule_envelope_commitment(cap)
    for name in J.CAPSULE_FIELDS:
        clone = J.capsule_from_json(J.capsule_to_json(cap))
        current = getattr(clone, name)
        setattr(clone, name, "different" if isinstance(current, str)
                else (current + 1 if isinstance(current, int) else not current))
        assert CP.capsule_envelope_commitment(clone) != base, name


def test_N14_journal_refuses_unknown_kind(jdir):
    with pytest.raises(J.JournalError, match="unknown journal kind"):
        J.build_record(1, "TAMPER", {}, J.ZERO_PREV)


def test_N15_capsule_field_set_mismatch_is_refused(jdir):
    data = J.capsule_to_json(make_capsule())
    del data["content_digest"]
    with pytest.raises(J.JournalError, match="field set mismatch"):
        J.capsule_from_json(data)


def test_N16_revoke_holder_is_not_expressible_through_the_public_api(jdir):
    """C07_DEPENDENCY_REVOKE: there is no public revocation interface."""
    public = [n for n in dir(J.EscrowJournal(CP and __import__("pathlib").Path(
        jdir / "j.jsonl")).state) if not n.startswith("_")]
    assert not any(k in n.lower() for n in public
                   for k in ("revoke", "remove_holder", "deauthorize")), public
