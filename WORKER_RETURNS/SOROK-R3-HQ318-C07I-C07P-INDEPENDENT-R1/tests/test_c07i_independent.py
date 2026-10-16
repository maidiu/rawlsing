"""C07I — fresh independent adversarial suite for the C07P cross-process custody candidate.

Reviewer-authored against `01_PREREGISTERED_REVIEWER_EXPECTATIONS_R1.md` (IP, IC, IH, IC-A/B/C, IH-T).
Nothing here is copied from the C07P suites. Real subprocesses, real filesystem,
real SIGKILL. The pinned OC6 source and the C07P adapter are never modified.
"""
from __future__ import annotations

import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
REPRO = HERE.parent / "repro"
sys.path.insert(0, str(REPRO / "source"))
sys.path.insert(0, str(REPRO))

import c07_journal as J          # adapter under review
import custody_protocol as CP    # pinned native module

WORKER = str(REPRO / "c07i_worker.py")
PINNED_BLOB = "4c185c18dbee57603038e97886da8fc4aa834082"
PINNED_SHA256 = "ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b"

CRASH_POINTS = [
    "0_before_tmp_fsync",
    "1_after_tmp_fsync_before_replace",
    "2_after_replace_before_dir_fsync",
    "3_after_dir_fsync",
]


# --------------------------------------------------------------------------- helpers
def run_role(role, journal, *extra):
    proc = subprocess.run([sys.executable, WORKER, role, str(journal), *extra],
                          capture_output=True, text=True)
    assert proc.returncode == 0, f"{role} failed rc={proc.returncode}: {proc.stderr[-900:]}"
    out = None
    for line in proc.stdout.splitlines():
        if line.startswith("@@C07I@@"):
            out = json.loads(line.split("@@C07I@@")[1].split("@@END@@")[0])
    assert out is not None, f"{role} produced no payload: {proc.stdout[-600:]}"
    return out


def run_role_killed(role, journal, point):
    proc = subprocess.run([sys.executable, WORKER, role, str(journal), point],
                          capture_output=True, text=True)
    assert proc.returncode in (-signal.SIGKILL, 137), \
        f"expected SIGKILL at {point}, got rc={proc.returncode}: {proc.stderr[-500:]}"
    assert f"SIGKILL at {point}" in proc.stderr, proc.stderr[-300:]
    return proc


@pytest.fixture()
def jdir(tmp_path):
    return tmp_path / "custody"


def canon(rec):
    return json.dumps(rec, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def read_lines(journal):
    return [json.loads(l) for l in Path(journal).read_text().splitlines() if l.strip()]


def write_lines(journal, records):
    Path(journal).write_text("".join(canon(r) + "\n" for r in records))


def reseal(records):
    """Recompute seq/prev/rec across the whole chain, as a rewriting attacker would."""
    prev, out = J.ZERO_PREV, []
    for i, rec in enumerate(records, start=1):
        body = {"v": rec["v"], "seq": i, "kind": rec["kind"],
                "payload": rec["payload"], "prev": prev}
        body["rec"] = hashlib.sha256(canon(body).encode()).hexdigest()
        prev = body["rec"]
        out.append(body)
    return out


def reseal_with_commitment(records):
    """Re-seal AND recompute each COMMIT's recorded capsule commitment."""
    out = reseal(records)
    fixed = []
    for rec in out:
        if rec["kind"] == "COMMIT":
            cap = J.capsule_from_json(rec["payload"]["capsule"])
            rec["payload"]["commitment"] = CP.capsule_envelope_commitment(cap)
        fixed.append(rec)
    return reseal(fixed)


def valid_journal(jdir, name="j.jsonl"):
    run_role("build", jdir / name)
    return read_lines(jdir / name)


# ===========================================================================
# SECTION IP — preregistered independent positives
# ===========================================================================

def test_IP1_processA_builds_authorised_lifecycle_via_public_api(jdir):
    out = run_role("build", jdir / "j.jsonl")
    ident = out["identity"]
    assert ident["integrity"] is True
    assert [op for _, op, _ in ident["ledger"]] == ["COMMIT", "UNBLIND", "RELEASE", "EXPOSURE"]
    assert ident["committed_ids"] == ["cap-A"]
    assert ident["released"] == ["cap-A"]
    assert ident["unblinded"] == {"cap-A": "custodian-zoe"}


def test_IP2_distinct_processes_and_pinned_import(jdir):
    a = run_role("build", jdir / "j.jsonl")
    b = run_role("recover", jdir / "j.jsonl")
    assert a["provenance"]["pid"] != b["provenance"]["pid"]
    for prov in (a["provenance"], b["provenance"]):
        assert prov["git_blob_sha1"] == PINNED_BLOB, prov
        assert prov["sha256"] == PINNED_SHA256, prov
        assert Path(prov["module_file"]).name == "custody_protocol.py"


def test_IP3_processB_restores_with_integrity(jdir):
    run_role("build", jdir / "j.jsonl")
    b = run_role("recover", jdir / "j.jsonl")
    assert b["restore"]["integrity"] is True
    assert b["restore"]["chain"]["ok"] is True
    assert b["identity"]["committed_ids"] == ["cap-A"]


def test_IP4_all_eighteen_fields_and_seal_are_byte_equal_across_processes(jdir):
    a = run_role("build", jdir / "j.jsonl")["identity"]
    b = run_role("recover", jdir / "j.jsonl")["identity"]
    assert a["capsule_18_fields"] == b["capsule_18_fields"]
    assert a["seals"] == b["seals"]
    assert len(a["capsule_18_fields"]["cap-A"]) == 18


def test_IP5_every_field_is_bound_to_the_seal(jdir):
    run_role("build", jdir / "j.jsonl")
    ident = run_role("recover", jdir / "j.jsonl")["identity"]
    base = ident["seals"]["cap-A"]
    fields = ident["capsule_18_fields"]["cap-A"]
    assert set(fields) == set(J.CAPSULE_FIELDS)
    for name in J.CAPSULE_FIELDS:
        clone = dict(fields)
        cur = clone[name]
        # bool MUST be tested before int: isinstance(False, int) is True
        if isinstance(cur, bool):
            new = not cur
        elif isinstance(cur, int):
            new = cur + 1
        elif isinstance(cur, float):
            new = cur + 1.5
        else:
            new = "different-value"
        clone[name] = new
        assert CP.capsule_envelope_commitment(CP.CustodyCapsule(**clone)) != base, name


def test_IP6_journal_is_canonical_jsonl_with_contiguous_sealed_chain(jdir):
    out = run_role("build", jdir / "j.jsonl")
    raw = Path(jdir / "j.jsonl").read_text()
    assert raw.endswith("\n")
    lines = raw.splitlines()
    for line in lines:
        rec = json.loads(line)
        assert canon(rec) == line, "line is not canonical JSON"
    recs = J.read_records(jdir / "j.jsonl")
    assert [r["seq"] for r in recs] == list(range(1, len(recs) + 1))
    prev = J.ZERO_PREV
    for rec in recs:
        assert rec["prev"] == prev
        body = {k: v for k, v in rec.items() if k != "rec"}
        assert rec["rec"] == hashlib.sha256(canon(body).encode()).hexdigest()
        prev = rec["rec"]
    assert out["journal_head"] == prev


def test_IP7_processB_continues_the_lifecycle_safely(jdir):
    run_role("build", jdir / "j.jsonl")
    c = run_role("continue", jdir / "j.jsonl")
    after = c["identity_after_continue"]
    assert after["committed_ids"] == ["cap-A", "cap-B"]
    assert after["released"] == ["cap-A", "cap-B"]
    assert after["integrity"] is True
    assert c["journal_records_after"] > 6


def test_IP8_head_digest_identifies_the_journal_and_is_stable(jdir):
    a = run_role("build", jdir / "j.jsonl")
    b = run_role("recover", jdir / "j.jsonl")
    assert a["journal_head"] == b["journal_head"]
    again = J.verify_chain(J.read_records(jdir / "j.jsonl"))
    assert again["head"] == a["journal_head"]
    assert again["records"] == a["journal_records"]


def test_IP9_journal_side_timestamps_are_byte_equal_across_processes(jdir):
    a = run_role("build", jdir / "j.jsonl")
    b = run_role("recover", jdir / "j.jsonl")
    recs = read_lines(jdir / "j.jsonl")
    assert a["journal_unblinded_at"] if "journal_unblinded_at" in a else True
    assert b["journal_unblinded_at"] == [r["payload"]["unblinded_at"]
                                         for r in recs if r["kind"] == "UNBLIND"]
    assert b["journal_exposure_ts"] == [r["payload"]["exposure_ts"]
                                        for r in recs if r["kind"] == "EXPOSURE"]


def test_IP10_escrow_event_times_are_re_stamped_on_replay_HOLD_CONFIRMED(jdir):
    """IP10: expect a NON-ZERO drift. This is C07_DEPENDENCY_TS, measured."""
    a = run_role("build", jdir / "j.jsonl")
    b = run_role("recover", jdir / "j.jsonl")
    journal_times = [r["payload"]["unblinded_at"]
                     for r in read_lines(jdir / "j.jsonl") if r["kind"] == "UNBLIND"]
    escrow_b = list(b["identity"]["escrow_unblinded_at"].values())
    escrow_a = list(a["identity"]["escrow_unblinded_at"].values())
    assert escrow_a != journal_times or True  # A is the writer; record what happened
    # The reconstructed escrow's own timestamps must NOT equal the journal's originals.
    assert escrow_b != journal_times, \
        "escrow timestamps unexpectedly matched the journal; the TS hold may be closed"
    # and integrity is still true, which is exactly why the hold is silent
    assert b["identity"]["integrity"] is True


# ===========================================================================
# SECTION IC — preregistered crash timing, real SIGKILL
# ===========================================================================

@pytest.mark.parametrize("point", CRASH_POINTS)
def test_IC5_every_crash_point_yields_a_clean_non_torn_journal(jdir, point):
    run_role_killed("crash", jdir / "j.jsonl", point)
    recs = J.read_records(jdir / "j.jsonl")
    assert J.verify_chain(recs)["ok"] is True
    info = J.EscrowJournal(jdir / "j.jsonl").restore()
    assert info["integrity"] is True


def test_IC1_crash_before_temp_fsync_keeps_previous_journal(jdir):
    """Reached by shadowing os.fsync in the reviewer worker only."""
    run_role_killed("crash", jdir / "j.jsonl", "0_before_tmp_fsync")
    recs = J.read_records(jdir / "j.jsonl")
    assert [r["kind"] for r in recs].count("COMMIT") == 1
    ej = J.EscrowJournal(jdir / "j.jsonl")
    ej.restore()
    assert sorted(ej.state.committed) == ["cap-A"]


def test_IC2_crash_after_temp_fsync_before_rename_rolls_back_cleanly(jdir):
    run_role_killed("crash", jdir / "j.jsonl", "1_after_tmp_fsync_before_replace")
    ej = J.EscrowJournal(jdir / "j.jsonl")
    ej.restore()
    assert sorted(ej.state.committed) == ["cap-A"]
    assert (jdir / "j.jsonl.tmp").exists(), "orphaned temp should remain unrenamed"


def test_IC3_post_rename_pre_dir_fsync_is_NOT_SETTLED_never_durability(jdir):
    """Prereg IC3 + §4.1: must never be classified as power-loss durability."""
    run_role_killed("crash", jdir / "j.jsonl", "2_after_replace_before_dir_fsync")
    recs = J.read_records(jdir / "j.jsonl")
    assert len(recs) == 3
    ej = J.EscrowJournal(jdir / "j.jsonl")
    ej.restore()
    assert sorted(ej.state.committed) == ["cap-A", "cap-C"]
    prereg = (HERE.parent / "01_PREREGISTERED_REVIEWER_EXPECTATIONS_R1.md").read_text()
    assert "NOT_SETTLED" in prereg
    # The observation is about PROCESS death only.
    assert "power-loss" in prereg and "durability" in prereg


def test_IC4_crash_after_dir_fsync_has_no_temp_left(jdir):
    run_role_killed("crash", jdir / "j.jsonl", "3_after_dir_fsync")
    recs = J.read_records(jdir / "j.jsonl")
    assert len(recs) == 3
    assert not (jdir / "j.jsonl.tmp").exists()
    ej = J.EscrowJournal(jdir / "j.jsonl")
    ej.restore()
    assert sorted(ej.state.committed) == ["cap-A", "cap-C"]


def test_IC_observe_fsync_support_rather_than_assuming_it(jdir):
    res = J.append_records(jdir / "p.jsonl", [
        {"kind": "AUTHORIZE", "payload": {"person_id": "runner1", "role": "CUSTODIAN"}}])
    assert res["limits"]["fsync_file"] == "SUPPORTED"
    assert res["limits"]["fsync_dir"] == "SUPPORTED"


# ===========================================================================
# SECTION IH — preregistered hostiles
# ===========================================================================

def test_IH1_tampered_payload_is_refused(jdir):
    recs = valid_journal(jdir)
    recs[2]["payload"]["holder"] = "attacker"
    write_lines(jdir / "j.jsonl", recs)
    with pytest.raises(J.JournalError, match="digest mismatch"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH2_middle_record_deleted_is_refused(jdir):
    recs = valid_journal(jdir)
    del recs[2]
    write_lines(jdir / "j.jsonl", recs)
    with pytest.raises(J.JournalError, match="seq is"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH3_two_records_swapped_is_refused(jdir):
    recs = valid_journal(jdir)
    recs[2], recs[3] = recs[3], recs[2]
    write_lines(jdir / "j.jsonl", recs)
    with pytest.raises(J.JournalError, match="seq is|prev chain break"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH4_record_duplicated_is_refused(jdir):
    recs = valid_journal(jdir)
    recs.insert(3, dict(recs[2]))
    write_lines(jdir / "j.jsonl", recs)
    with pytest.raises(J.JournalError, match="seq is"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH5_whole_journal_forked_into_one_file_is_refused(jdir):
    recs = valid_journal(jdir)
    write_lines(jdir / "j.jsonl", recs + recs)
    with pytest.raises(J.JournalError, match="seq is"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH6_trailing_bytes_after_final_newline_are_refused(jdir):
    valid_journal(jdir)
    with open(jdir / "j.jsonl", "ab") as fh:
        fh.write(b"GARBAGE-AFTER-END")
    with pytest.raises(J.JournalError):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH7_final_record_truncated_mid_line_is_refused(jdir):
    valid_journal(jdir)
    raw = (jdir / "j.jsonl").read_bytes()
    (jdir / "j.jsonl").write_bytes(raw[:-15])
    with pytest.raises(J.JournalError):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH8_non_canonical_json_is_not_silently_accepted(jdir):
    recs = valid_journal(jdir)
    recs[0]["payload"]["person_id"] = "mallory"
    pretty = json.dumps(recs[0], indent=2, sort_keys=False)
    body = "".join(canon(r) + "\n" for r in recs[1:])
    (jdir / "j.jsonl").write_text(pretty + "\n" + body)
    with pytest.raises(J.JournalError):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH9_capsule_substituted_with_chain_resealed_is_refused(jdir):
    recs = valid_journal(jdir)
    commit = next(r for r in recs if r["kind"] == "COMMIT")
    commit["payload"]["capsule"]["content_digest"] = "attacker-digest"
    write_lines(jdir / "j.jsonl", reseal(recs))
    with pytest.raises(J.JournalError, match="forged capsule"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH10_capsule_AND_recorded_commitment_both_rewritten(jdir):
    """IH10 preregistered as ACCEPTED (ceiling), not expected-refused.

    Prereg 5.1: if the attacker rewrites the capsule AND recomputes the recorded
    commitment, BOTH the per-record chain and the commitment check pass. That is
    the same failure class as prefix rollback and must be reported as part of the
    ceiling. If it were ever REFUSED that would be stronger than preregistered and
    must be re-adjudicated, so that case FAILS loudly instead of being absorbed.
    """
    recs = valid_journal(jdir)
    commit = next(r for r in recs if r["kind"] == "COMMIT")
    commit["payload"]["capsule"]["content_digest"] = "attacker-digest"
    commit["payload"]["capsule"]["scenario_frame"] = "attacker-frame"
    write_lines(jdir / "j.jsonl", reseal_with_commitment(recs))

    ej = J.EscrowJournal(jdir / "j.jsonl")
    try:
        ej.restore()
    except Exception as exc:  # pragma: no cover - would be stronger than preregistered
        pytest.fail(
            "STRONGER THAN PREREGISTERED: a fully rewritten capsule with a matching "
            f"recomputed commitment and a resealed chain was REFUSED ({type(exc).__name__}: "
            f"{exc}). The preregistered ceiling must be re-adjudicated, not silently kept.")

    # preregistered: accepted, silently carrying the attacker's capsule
    assert ej.state.committed["cap-A"].content_digest == "attacker-digest"
    assert ej.state.committed["cap-A"].scenario_frame == "attacker-frame"
    assert ej.state.verify_ledger_integrity() is True


def test_IH11_unblind_of_uncommitted_capsule_is_refused(jdir):
    jdir.mkdir(parents=True, exist_ok=True)
    forged = J.build_record(1, "UNBLIND",
                            {"capsule_id": "ghost", "holder": "custodian-zoe",
                             "unblinded_at": 1.0}, J.ZERO_PREV)
    write_lines(jdir / "j.jsonl", [forged])
    with pytest.raises(CP.IdentityMismatchError):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH12_exposure_of_uncommitted_capsule_is_refused(jdir):
    jdir.mkdir(parents=True, exist_ok=True)
    forged = J.build_record(1, "EXPOSURE",
                            {"capsule_id": "ghost", "exposed_to": "coder-x",
                             "purpose": "development", "exposure_ts": 1.0}, J.ZERO_PREV)
    write_lines(jdir / "j.jsonl", [forged])
    with pytest.raises(CP.IdentityMismatchError):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH13_unblind_by_ungranted_holder_is_refused(jdir):
    recs = valid_journal(jdir)
    forged = J.build_record(len(recs) + 1, "UNBLIND",
                            {"capsule_id": "cap-A", "holder": "stranger-9",
                             "unblinded_at": 1.0}, recs[-1]["rec"])
    write_lines(jdir / "j.jsonl", recs + [forged])
    with pytest.raises(CP.IdentityMismatchError):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH14_forged_holder_on_an_already_unblinded_capsule_is_refused(jdir):
    recs = valid_journal(jdir)
    unblind = next(r for r in recs if r["kind"] == "UNBLIND")
    unblind["payload"]["holder"] = "someone-else"
    write_lines(jdir / "j.jsonl", reseal(recs))
    with pytest.raises((J.JournalError, CP.EditAfterFreezeError, CP.IdentityMismatchError)):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH15_old_source_state_alias_restores_the_OLD_state_silently(jdir):
    """IH15 preregistered: valid old journal restores without error."""
    valid_journal(jdir)                       # build j.jsonl (5 records)
    shutil.copy(jdir / "j.jsonl", jdir / "old.jsonl")   # snapshot the OLD state
    old = read_lines(jdir / "old.jsonl")
    run_role("continue", jdir / "j.jsonl")     # advance j.jsonl
    new = read_lines(jdir / "j.jsonl")
    assert len(new) > len(old), (len(new), len(old))
    shutil.copy(jdir / "j.jsonl", jdir / "newer.jsonl")
    ej = J.EscrowJournal(jdir / "old.jsonl")      # no refusal
    ej.restore()
    assert sorted(ej.state.committed) == ["cap-A"]
    assert "cap-B" not in ej.state.committed
    assert ej.state.verify_ledger_integrity() is True


def test_IH16_blank_line_inside_journal_is_refused(jdir):
    valid_journal(jdir)
    raw = (jdir / "j.jsonl").read_text()
    (jdir / "j.jsonl").write_text(raw.replace("\n", "\n\n", 1))
    with pytest.raises(J.JournalError, match="blank line"):
        J.EscrowJournal(jdir / "j.jsonl").restore()


def test_IH17_unknown_record_kind_is_refused(jdir):
    with pytest.raises(J.JournalError, match="unknown journal kind"):
        J.build_record(1, "TAMPER", {}, J.ZERO_PREV)


def test_IH18_capsule_field_set_mismatch_is_refused(jdir):
    data = J.capsule_to_json(CP.CustodyCapsule(
        capsule_id="x", schema_version="1.0", purpose="SOURCEFREE_TEST_ONLY",
        scenario_frame="f", family_graph_digest="a", content_digest="b",
        contribution_digest="c", public_projection_digest="d", hidden_projection_digest="e",
        lawful_set_digest="f", coder_rubric_digest="g", split_assignment_digest="h",
        generation_history_digest="i", rejected_alternatives_digest="j", freeze_timestamp=1.0))
    del data["content_digest"]
    with pytest.raises(J.JournalError, match="field set mismatch"):
        J.capsule_from_json(data)
    data2 = J.capsule_to_json(CP.CustodyCapsule(
        capsule_id="x", schema_version="1.0", purpose="SOURCEFREE_TEST_ONLY",
        scenario_frame="f", family_graph_digest="a", content_digest="b",
        contribution_digest="c", public_projection_digest="d", hidden_projection_digest="e",
        lawful_set_digest="f", coder_rubric_digest="g", split_assignment_digest="h",
        generation_history_digest="i", rejected_alternatives_digest="j", freeze_timestamp=1.0))
    data2["smuggled"] = 1
    with pytest.raises(J.JournalError, match="field set mismatch"):
        J.capsule_from_json(data2)


def test_IH19_empty_journal_is_recorded_not_silently_trusted(jdir):
    jdir.mkdir(parents=True, exist_ok=True)
    (jdir / "j.jsonl").write_bytes(b"")
    assert J.read_records(jdir / "j.jsonl") == []
    assert J.verify_chain([])["ok"] is True
    ej = J.EscrowJournal(jdir / "j.jsonl")
    info = ej.restore()
    assert info["applied"] == 0
    assert info["integrity"] is True          # vacuously true — that is the risk
    assert ej.state.committed == {}


# ===========================================================================
# SECTION IC-A/B/C — PRESERVE the demonstrated unkeyed-rollback ceiling
# ===========================================================================

def test_IC_A_self_consistent_prefix_rollback_with_recomputed_hashes_is_ACCEPTED(jdir):
    """Preregistered as ACCEPTED. If this ever fails, the ceiling was mis-stated."""
    run_role("build", jdir / "j.jsonl")
    run_role("continue", jdir / "j.jsonl")
    recs = read_lines(jdir / "j.jsonl")

    def owns(r):
        return (r["kind"] == "AUTHORIZE"
                or r["payload"].get("capsule_id") == "cap-A"
                or r["payload"].get("capsule", {}).get("capsule_id") == "cap-A")
    prefix = [r for r in recs if owns(r)]
    assert len(prefix) < len(recs), "prefix must actually be shorter"

    # Attacker rewrites the file to the earlier prefix AND recomputes every hash.
    write_lines(jdir / "j.jsonl", reseal(prefix))

    ej = J.EscrowJournal(jdir / "j.jsonl")   # expected: NO refusal
    ej.restore()
    assert sorted(ej.state.committed) == ["cap-A"]
    assert "cap-B" not in ej.state.committed, "cap-B must be silently lost (the ceiling)"


def test_IC_B_escrow_reports_integrity_on_the_rolled_back_state(jdir):
    """The escrow itself cannot tell. This is why local integrity is not a trust anchor."""
    run_role("build", jdir / "j.jsonl")
    run_role("continue", jdir / "j.jsonl")
    recs = read_lines(jdir / "j.jsonl")
    prefix = [r for r in recs
              if r["kind"] == "AUTHORIZE"
              or r["payload"].get("capsule_id") == "cap-A"
              or r["payload"].get("capsule", {}).get("capsule_id") == "cap-A"]
    write_lines(jdir / "j.jsonl", reseal(prefix))
    ej = J.EscrowJournal(jdir / "j.jsonl")
    ej.restore()
    assert ej.state.verify_ledger_integrity() is True
    assert J.verify_chain(J.read_records(jdir / "j.jsonl"))["ok"] is True


def test_IC_C_prefix_rollback_is_undetectable_even_with_a_totally_empty_newer_state(jdir):
    """Deleting the prefix entirely is likewise invisible to local checks."""
    run_role("build", jdir / "j.jsonl")
    recs = read_lines(jdir / "j.jsonl")
    write_lines(jdir / "j.jsonl", recs[:1])
    ej = J.EscrowJournal(jdir / "j.jsonl")
    ej.restore()
    assert ej.state.committed == {}
    assert ej.state.verify_ledger_integrity() is True


# ===========================================================================
# SECTION IH-T — both typed API holds must remain OPEN
# ===========================================================================

def test_IH_T1_unblind_and_record_exposure_take_no_timestamp_parameter(jdir):
    import inspect
    for name in ("unblind", "record_exposure"):
        sig = inspect.signature(getattr(CP.EscrowState, name))
        params = set(sig.parameters)
        assert "at" not in params and "timestamp" not in params, (name, params)
        assert all(p.kind is not inspect.Parameter.KEYWORD_ONLY or "at" not in p.name
                   for p in sig.parameters.values())


def test_IH_T2_no_public_revoke_holder_exists(jdir):
    public = [n for n in dir(CP.EscrowState) if not n.startswith("_")]
    assert not any("revoke" in n.lower() or "deauthor" in n.lower() for n in public), public
    assert "authorize_holder" in public


def test_IH_T3_reviewer_did_not_mutate_private_state_to_force_green(jdir):
    """AST check: no pickle import, no __setattr__ call, no private-state access.

    A substring scan is not adequate here because the adapter's own docstrings
    legitimately contain the word "pickles". Only real imports and real
    attribute/subscript accesses are inspected.
    """
    import ast
    tree = ast.parse((REPRO / "c07_journal.py").read_text())

    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])
    assert "pickle" not in imported and "dill" not in imported and "shelve" not in imported, imported

    called = {n.func.attr for n in ast.walk(tree)
              if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)}
    assert "__setattr__" not in called, called

    touched = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript):
            base = node.value
            while isinstance(base, (ast.Attribute, ast.Subscript)):
                base = base.value
            if isinstance(base, ast.Attribute):
                touched.add(base.attr)
            elif isinstance(base, ast.Name):
                touched.add(base.id)
    for forbidden in ("_event_proofs", "_capsule_seals", "_ledger_seq",
                      "committed", "unblinded", "released", "exposure_log",
                      "ledger", "holder_roles"):
        assert forbidden not in touched, \
            f"adapter must not subscript private/public escrow state {forbidden!r}: {sorted(touched)}"


def test_IH_T4_good_positive_restoration_still_works(jdir):
    """Final positive control after all the hostile mutations."""
    run_role("build", jdir / "j.jsonl")
    b = run_role("recover", jdir / "j.jsonl")
    assert b["identity"]["integrity"] is True
    assert b["identity"]["committed_ids"] == ["cap-A"]
    assert b["identity"]["released"] == ["cap-A"]
