import sqlite3
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import c9_actor_r3 as c9


def add_world(a, name):
    a.add_world_receipt(
        world_receipt_hash=name,
        world_event_id="event-" + name,
        c8_branch_id="c8-branch",
        c8_root_hash="c8-root",
        c8_head_hash="c8-head",
        effective_us=10,
    )
    return name


def held_request(a, world, *, key="k1", event="e1", **overrides):
    values = {
        "event_key": event,
        "idempotency_key": key,
        "decision_kind": "HELD_MISSING_RULE",
        "source_cut_hash": a.source_cut_hash,
        "source_scope_hash": "source-scope",
        "settled_scope_hash": "settled-scope",
        "world_receipt_hash": world,
    }
    values.update(overrides)
    return c9.PublishRequest(**values)


def final_request(a, world, rule_hash, *, key="final", event="final-event", **overrides):
    values = {
        "event_key": event,
        "idempotency_key": key,
        "decision_kind": "COMMITTED_CHANGE",
        "source_cut_hash": a.source_cut_hash,
        "source_scope_hash": "source-scope",
        "settled_scope_hash": "settled-scope",
        "world_receipt_hash": world,
        "rule_t_hash": rule_hash,
        "rule_t_status": "COMMITTED_CHANGE",
        "evaluation_basis": "ISSUED_RULE_T_EVALUATED",
        "evaluated_readset_hash": "readset-" + rule_hash,
        "semantic_payload": {"value": rule_hash},
    }
    values.update(overrides)
    return c9.PublishRequest(**values)


def counts(a, event_key):
    return (
        a.conn.execute(
            "SELECT count(*) FROM decision_receipt WHERE event_key=?", (event_key,)
        ).fetchone()[0],
        a.conn.execute(
            "SELECT count(*) FROM actor_version WHERE version_no>0"
        ).fetchone()[0],
        a.conn.execute(
            "SELECT count(*) FROM event_attempt WHERE event_key=?", (event_key,)
        ).fetchone()[0],
    )


def test_c0_s36_seven_table_readset_is_unchanged(tmp_path, monkeypatch):
    s36_root = Path(
        "/private/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/"
        "syn02-s36-r2-wt/WORKER_RETURNS/"
        "SOROK-20261024-S36-ACTOR-ACCESS-RESPONSE-R1"
    )
    if not (s36_root / "candidate" / "transaction.py").exists():
        pytest.skip("S36 source unavailable")
    monkeypatch.syspath_prepend(str(s36_root))
    monkeypatch.syspath_prepend(str(s36_root / "runtime" / "native"))
    from candidate.canon import digest
    from candidate.transaction import CandidateStore
    from s36_harness import run_s35_case

    s36 = CandidateStore(tmp_path / "s36.db")
    legacy, _ = run_s35_case(s36)
    assert legacy.committed and legacy.receipt.committed
    assert legacy.receipt.receipt_hash == (
        "1cec8633d861959c7d4b744c6770f9720110e977f021f460a1608e1aebbf4ee9"
    )
    assert legacy.receipt.before_hash == (
        "9c5137f214d299bdb627c72ac8ff1880be98822d56082ec8ecce3eea0ba3fe62"
    )
    assert legacy.receipt.after_hash == (
        "07d38064535ec54c9d96a570775dc70b4a4d285453ccdcbe739ecb8ba3df01b6"
    )
    before = digest(s36._logical_readset())
    assert before == (
        "b3cc7c9e4a55ccce935f0cdbea9fbd8db003c59467748f805df317d51310214d"
    )
    tables = sorted(s36._logical_readset()["tables"])
    assert tables == [
        "clock",
        "event_identity",
        "occurrence",
        "receipt",
        "response",
        "target_journal",
        "target_state",
    ]

    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    marker = add_world(a, "w-c0")
    a.add_rule(
        rule_hash="T-C0",
        rule_kind="T",
        issuer_ref="sourcefree-test",
        source_cut_hash=a.source_cut_hash,
    )
    a.publish(final_request(a, marker, "T-C0"))

    after = digest(s36._logical_readset())
    assert after == before
    s36.close()


def test_c1_exact_replay_returns_original_receipt_without_extra_version(tmp_path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    marker = add_world(a, "w-c1")
    request = held_request(a, marker)
    first = a.publish(request)
    before = counts(a, "e1")
    second = a.publish(request)
    assert second["replayed"] is True
    assert second["receipt_hash"] == first["receipt_hash"]
    assert second["receipt_json"] == first["receipt_json"]
    assert second["attempt_id"] == first["attempt_id"]
    assert counts(a, "e1") == before
    assert a.verify()["ok"] is True

    a.add_rule(
        rule_hash="T-REPLAY",
        rule_kind="T",
        issuer_ref="sourcefree-test",
        source_cut_hash=a.source_cut_hash,
    )
    final = final_request(a, marker, "T-REPLAY")
    published = a.publish(final)
    final_counts = counts(a, "final-event")
    rule_count = a.conn.execute("SELECT count(*) FROM rule_issuance").fetchone()[0]
    replayed = a.publish(final)
    assert replayed["replayed"] is True
    assert replayed["receipt_hash"] == published["receipt_hash"]
    assert counts(a, "final-event") == final_counts
    assert a.conn.execute("SELECT count(*) FROM rule_issuance").fetchone()[0] == rule_count


def test_c2_idempotency_conflict_is_typed_and_non_mutating(tmp_path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    marker = add_world(a, "w-c2")
    first = a.publish(held_request(a, marker))
    before = a.head_signature()
    conflicting = held_request(a, marker, settled_scope_hash="different")
    with pytest.raises(c9.IdempotencyConflict):
        a.publish(conflicting)
    assert a.head_signature() == before
    assert a.conn.execute("SELECT count(*) FROM decision_receipt").fetchone()[0] == 1

    b = c9.ActorAuthority(tmp_path / "actor.db", actor_id="B")
    with pytest.raises(c9.Refusal) as error:
        b.publish(held_request(b, marker))
    assert error.value.code == "IDEMPOTENCY_KEY_SCOPE_MISMATCH"
    assert first["attempt_no"] == 1


def test_c3_cas_and_fault_rollback_leave_no_ghost_state(tmp_path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    marker = add_world(a, "w-c3")
    old_head = a.head_signature()
    first = a.publish(held_request(a, marker), expected_head=old_head)
    with pytest.raises(c9.Refusal) as error:
        a.publish(
            held_request(a, marker, key="k2", event="e2"),
            expected_head=old_head,
        )
    assert error.value.code == "CAS_CONFLICT"
    with pytest.raises(c9.Refusal) as error:
        a.publish(
            held_request(a, marker, key="partial", event="partial"),
            expected_head={"branch_epoch": a.branch_epoch},
        )
    assert error.value.code == "CAS_CONFLICT"

    before = counts(a, "e3")
    head_before = a.head_signature()
    with pytest.raises(c9.Refusal) as error:
        a.publish(
            held_request(a, marker, key="k3", event="e3"),
            fault="before_commit",
        )
    assert error.value.code == "C3_INJECTED_FAILURE"
    assert counts(a, "e3") == before
    assert a.head_signature() == head_before
    assert a.conn.execute(
        "SELECT count(*) FROM projection_outbox WHERE commit_seq>?", (first["seq"],)
    ).fetchone()[0] == 0

    with pytest.raises(c9.Refusal) as error:
        c9.ActorAuthority(
            tmp_path / "actor.db",
            actor_id="A",
            branch_epoch="wrong-epoch",
        )
    assert error.value.code == "BRANCH_EPOCH_MISMATCH"


def test_c4_c9_commit_precedes_clean_mirror_and_ack(tmp_path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    marker = add_world(a, "w-c4")
    a.add_rule(
        rule_hash="T-C4",
        rule_kind="T",
        issuer_ref="sourcefree-test",
        source_cut_hash=a.source_cut_hash,
    )
    result = a.publish(final_request(a, marker, "T-C4"))
    outbox = a.conn.execute(
        "SELECT projection_state FROM projection_outbox WHERE receipt_hash=?",
        (result["receipt_hash"],),
    ).fetchone()
    assert outbox[0] == "PENDING"

    mirror = c9.MirrorStore(tmp_path / "mirror.db")
    mirror.add_root_branch(
        c12_branch_id=a.c12_branch_id,
        actor_id=a.actor_id,
        actor_branch_epoch=a.branch_epoch,
        c12_root_hash="c12-root-hash",
        c12_created_clock=1,
    )
    assert mirror.status(a, result["receipt_hash"])["state"] == "SYNC_HELD"
    mirror.project(
        a,
        result["receipt_hash"],
        c12_root_hash="c12-root-hash",
        c12_last_clock=2,
    )
    assert mirror.status(a, result["receipt_hash"])["code"] == "PROJECTED"
    mirror.ack(a, result["receipt_hash"])
    assert mirror.status(a, result["receipt_hash"])["state"] == "CLEAN"

    mirror.hold_watermark(a.c12_branch_id, "SYNC_HELD")
    assert mirror.status(a, result["receipt_hash"])["state"] == "SYNC_HELD"
    with pytest.raises(c9.Refusal):
        mirror.project(
            a,
            result["receipt_hash"],
            c12_root_hash="c12-root-hash",
            c12_last_clock=2,
        )
    mirror.hold_watermark(a.c12_branch_id, "CLEAN")
    assert mirror.status(a, result["receipt_hash"])["state"] == "CLEAN"
    assert mirror.verify()["ok"] is True
    assert a.conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"
    assert mirror.conn.execute("PRAGMA integrity_check").fetchone()[0] == "ok"


def test_c5_mirror_projection_and_ack_are_idempotent(tmp_path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    marker = add_world(a, "w-c5")
    a.add_rule(
        rule_hash="T-C5",
        rule_kind="T",
        issuer_ref="sourcefree-test",
        source_cut_hash=a.source_cut_hash,
    )
    result = a.publish(final_request(a, marker, "T-C5"))
    mirror = c9.MirrorStore(tmp_path / "mirror.db")
    mirror.add_root_branch(
        c12_branch_id=a.c12_branch_id,
        actor_id=a.actor_id,
        actor_branch_epoch=a.branch_epoch,
        c12_root_hash="c12-root-hash",
        c12_created_clock=1,
    )
    with pytest.raises(c9.Refusal):
        mirror.ack(a, result["receipt_hash"])

    first = mirror.project(
        a,
        result["receipt_hash"],
        c12_root_hash="c12-root-hash",
        c12_last_clock=2,
    )
    second = mirror.project(
        a,
        result["receipt_hash"],
        c12_root_hash="c12-root-hash",
        c12_last_clock=2,
    )
    assert first["projection_hash"] == second["projection_hash"]
    assert second["replayed"] is True
    assert mirror.conn.execute("SELECT count(*) FROM mirror_receipt").fetchone()[0] == 1
    assert a.conn.execute(
        "SELECT attempt_count FROM projection_outbox WHERE receipt_hash=?",
        (result["receipt_hash"],),
    ).fetchone()[0] == 1

    first_ack = mirror.ack(a, result["receipt_hash"])
    second_ack = mirror.ack(a, result["receipt_hash"])
    assert first_ack["replayed"] is False
    assert second_ack["replayed"] is True
    assert mirror.conn.execute("SELECT count(*) FROM mirror_receipt").fetchone()[0] == 1
    assert mirror.status(a, result["receipt_hash"])["state"] == "CLEAN"


def test_c6_actual_c12_perception_suffix_stays_held(tmp_path):
    j = Path(
        "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/"
        "SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j"
    )
    needed = [
        j / "r26e" / "c12_integrity.py",
        j / "candidate" / "vendor" / "bp4" / "bp4" / "store.py",
    ]
    if not all(path.exists() for path in needed):
        pytest.skip("C12 source unavailable")
    sys.path.insert(0, str(j))
    sys.path.insert(0, str(j / "candidate" / "vendor" / "bp4"))
    sys.path.insert(0, str(j / "candidate" / "vendor" / "bp4" / "vendor" / "bp1"))
    from bp4.canon import seal
    from bp4.store import C12Store, GRADE
    from r26e.c12_integrity import QualifiedC12Store

    path = tmp_path / "c12.db"
    store = QualifiedC12Store(path)
    store.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
    event = seal(
        {
            "schema": "BP4_C12_WORLD_EVENT@1",
            "branch_id": "root",
            "event_id": "ev1",
            "clock": 10,
            "body": {},
            "grade": GRADE,
            "native": False,
        }
    )
    store.append_world_event("root", event)
    store.record_perception("root", actor_id="A", event_id="ev1", clock=11, channel="test")
    assert store.verify("root")["ok"] is True
    assert store.last_clock("root") == 10
    store.close()

    guard = c9.c12_fork_guard(path, "root")
    assert guard["state"] == "FORK_HELD"
    assert guard["code"] == "C12_PERCEPTION_ONLY_SUFFIX"
    assert guard["nonperception_last_clock"] == 10
    assert guard["perception_last_clock"] == 11
    assert c9.c12_fork_guard(
        path, "root", expected_base_root_hash="wrong-root"
    )["code"] == "C12_BASE_ROOT_MISMATCH"

    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    marker = add_world(a, "w-c6")
    held = a.publish(held_request(a, marker))
    fork = a.fork_branch(
        branch_id="fork",
        branch_epoch="fork-epoch",
        source_cut_hash="fork-source-cut",
        source_root_hash="fork-source-root",
        source_grant_hash="fork-grant",
        c12_branch_id="c12-fork",
        c12_root_hash="c12-fork-root",
        c12_perception_hash=guard["base_perception_hash"],
        c12_watermark=guard["fork_cut"],
    )
    assert fork["parent_branch_id"] == a.branch_id
    child = c9.ActorAuthority(
        tmp_path / "actor.db",
        actor_id="A",
        branch_id="fork",
        branch_epoch="fork-epoch",
    )
    assert child.read_semantic()["semantic_hash"] == a.read_semantic()["semantic_hash"]
    assert child.verify()["ok"] is True

    mirror = c9.MirrorStore(tmp_path / "mirror.db")
    mirror.add_fork_branch(
        c12_branch_id="c12-fork",
        actor_id="A",
        actor_branch_epoch="fork-epoch",
        c12_parent_branch_id="/c12-root",
        c12_root_hash="c12-fork-root",
        c12_fork_clock=guard["fork_cut"],
        c12_created_clock=guard["fork_cut"],
        c9_start_seq=held["seq"],
        c9_start_receipt_hash=held["receipt_hash"],
        base_c12_root_hash="c12-root-hash",
        base_c12_perception_hash=guard["base_perception_hash"],
        base_c12_perception_count=guard["base_perception_count"],
        mirror_state="FORK_HELD",
    )
    assert mirror.verify()["ok"] is True


def test_c6_missing_c12_source_fails_closed(tmp_path):
    missing = c9.c12_fork_guard(tmp_path / "missing.db", "root")
    assert missing["state"] == "FORK_HELD"
    assert missing["code"] == "C12_READ_FAILED"


def test_c6_same_count_perception_substitution_is_held(tmp_path):
    j = Path(
        "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/"
        "SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j"
    )
    if not (j / "candidate" / "vendor" / "bp4" / "bp4" / "store.py").exists():
        pytest.skip("C12 source unavailable")
    sys.path.insert(0, str(j / "candidate" / "vendor" / "bp4"))
    sys.path.insert(0, str(j / "candidate" / "vendor" / "bp4" / "vendor" / "bp1"))
    sys.path.insert(0, str(j))
    from bp4.canon import seal
    from bp4.store import C12Store, GRADE
    from r26e.c12_integrity import QualifiedC12Store

    path = tmp_path / "substitution.db"
    store = QualifiedC12Store(path)
    store.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
    first = seal(
        {
            "schema": "BP4_C12_WORLD_EVENT@1",
            "branch_id": "root",
            "event_id": "ev1",
            "clock": 10,
            "body": {},
            "grade": GRADE,
            "native": False,
        }
    )
    second = seal(
        {
            "schema": "BP4_C12_WORLD_EVENT@1",
            "branch_id": "root",
            "event_id": "ev2",
            "clock": 10,
            "body": {},
            "grade": GRADE,
            "native": False,
        }
    )
    store.append_world_event("root", first)
    store.append_world_event("root", second)
    store.record_perception("root", actor_id="A", event_id="ev1", clock=10, channel="test")
    store.record_perception("root", actor_id="A", event_id="ev2", clock=11, channel="test")
    parent = c9.c12_fork_guard(path, "root")
    assert parent["state"] == "FORK_HELD"
    assert store.verify("root")["ok"] is True

    store.fork("root", "child")
    third = seal(
        {
            "schema": "BP4_C12_WORLD_EVENT@1",
            "branch_id": "child",
            "event_id": "ev3",
            "clock": 10,
            "body": {},
            "grade": GRADE,
            "native": False,
        }
    )
    store.append_world_event("child", third)
    store.record_perception("child", actor_id="A", event_id="ev3", clock=10, channel="test")
    assert store.verify("child")["ok"] is True
    assert len(store.perceptions("root")) == len(store.perceptions("child"))
    child = c9.c12_fork_guard(
        path,
        "child",
        expected_base_perception_hash=parent["base_perception_hash"],
    )
    assert child["state"] == "FORK_HELD"
    assert child["code"] == "C12_BASE_PERCEPTION_IDENTITY_MISMATCH"
    store.close()


def test_c7_status_orthogonality_requalification_and_raw_guards(tmp_path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    marker = add_world(a, "w-c7")
    with pytest.raises(c9.Refusal) as error:
        a.publish(
            held_request(
                a,
                marker,
                rule_t_status="COMMITTED_CHANGE",
            )
        )
    assert error.value.code == "STATUS_AXIS_CONFLICT"

    with pytest.raises(c9.Refusal) as error:
        a.publish(
            held_request(
                a,
                marker,
                decision_kind="TRUE_NO_CHANGE_EVALUATED",
                proposal_state="NO_PROPOSAL",
                rule_t_status="TRUE_NO_CHANGE_EVALUATED",
                evaluation_basis="ISSUED_RULE_T_EVALUATED",
                evaluated_readset_hash="readset-missing-rule",
            )
        )
    assert error.value.code == "RULE_T_HASH_REQUIRED"

    a.add_rule(
        rule_hash="T-PROP",
        rule_kind="T",
        issuer_ref="sourcefree-test",
        source_cut_hash=a.source_cut_hash,
    )
    with pytest.raises(c9.Refusal) as error:
        a.publish(
            held_request(
                a,
                marker,
                key="no-proposal",
                decision_kind="TRUE_NO_CHANGE_EVALUATED",
                proposal_state="NO_PROPOSAL",
                rule_t_status="TRUE_NO_CHANGE_EVALUATED",
                rule_t_hash="T-PROP",
                evaluation_basis="ISSUED_RULE_T_EVALUATED",
                evaluated_readset_hash="readset-no-proposal",
            )
        )
    assert error.value.code == "FINAL_CANNOT_INFER_NO_CHANGE"

    seen = a.publish(
        held_request(
            a,
            marker,
            actor_presence="NOT_PRESENT",
            world_occurrence="OCCURRED",
        )
    )
    receipt = a.conn.execute(
        "SELECT * FROM decision_receipt WHERE receipt_hash=?", (seen["receipt_hash"],)
    ).fetchone()
    assert receipt["decision_kind"] == "HELD_MISSING_RULE"
    assert receipt["world_occurrence"] == "OCCURRED"
    assert receipt["actor_presence"] == "NOT_PRESENT"

    a.add_rule(
        rule_hash="T-C7",
        rule_kind="T",
        issuer_ref="sourcefree-test",
        source_cut_hash=a.source_cut_hash,
    )
    a.add_requalification_grant(
        grant_hash="g-c7",
        prior_attempt_id=seen["attempt_id"],
        issuance_kind="RULE_T",
        issuance_ref="T-C7",
        source_cut_hash=a.source_cut_hash,
    )
    final = a.publish(
        final_request(
            a,
            marker,
            "T-C7",
            event="e1",
            key="requal-final",
            prior_attempt_id=seen["attempt_id"],
            supersession_grant_hash="g-c7",
            rule_t_status="COMMITTED_CHANGE",
        )
    )
    old = a.conn.execute(
        "SELECT attempt_state FROM event_attempt WHERE attempt_id=?",
        (seen["attempt_id"],),
    ).fetchone()
    assert old["attempt_state"] == "HELD"
    assert final["final"] is True
    assert final["receipt"]["prior_receipt_hash"] == seen["receipt_hash"]
    assert a.verify()["ok"] is True

    with pytest.raises(c9.Refusal) as error:
        a.publish(
            final_request(a, marker, "T-C7", event="e1", key="after-final"),
        )
    assert error.value.code == "EVENT_ALREADY_FINALIZED"

    with pytest.raises(sqlite3.IntegrityError):
        a.conn.execute(
            "UPDATE actor_version SET semantic_hash='x' WHERE version_no=0"
        )
    with pytest.raises(sqlite3.IntegrityError):
        a.conn.execute("DELETE FROM decision_receipt")
    pending = a.conn.execute(
        "SELECT receipt_hash FROM projection_outbox WHERE projection_state='PENDING'"
    ).fetchone()
    assert pending is not None
    with pytest.raises(sqlite3.IntegrityError):
        a.conn.execute(
            "UPDATE projection_outbox SET projection_state='ACKED',"
            "projected_c12_hash='x',acked_admin_us=1 WHERE receipt_hash=?",
            (pending["receipt_hash"],),
        )


def test_c7_requalification_requires_fresh_grant_and_source_changes_use_fork(tmp_path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    marker = add_world(a, "w-grant")
    held = a.publish(held_request(a, marker))
    with pytest.raises(c9.Refusal) as error:
        a.publish(
            held_request(
                a,
                marker,
                key="missing-grant",
                prior_attempt_id=held["attempt_id"],
                supersession_grant_hash="missing",
                attempt_no=2,
            )
        )
    assert error.value.code == "REQUALIFICATION_GRANT_MISSING"

    a.add_rule(
        rule_hash="T-HELD",
        rule_kind="T",
        issuer_ref="sourcefree-test",
        source_cut_hash=a.source_cut_hash,
        issued_state="HELD",
    )
    with pytest.raises(c9.Refusal) as error:
        a.add_requalification_grant(
            grant_hash="bad-grant",
            prior_attempt_id=held["attempt_id"],
            issuance_kind="RULE_T",
            issuance_ref="T-HELD",
            source_cut_hash=a.source_cut_hash,
        )
    assert error.value.code == "GRANT_ISSUANCE_NOT_ISSUED"

    a.add_rule(
        rule_hash="T-GRANT",
        rule_kind="T",
        issuer_ref="sourcefree-test",
        source_cut_hash=a.source_cut_hash,
    )
    a.add_requalification_grant(
        grant_hash="g-source",
        prior_attempt_id=held["attempt_id"],
        issuance_kind="SOURCE",
        issuance_ref="source-issuance",
        source_cut_hash="new-source-cut",
    )
    with pytest.raises(c9.Refusal) as error:
        a.publish(
            held_request(
                a,
                marker,
                key="source-change",
                source_cut_hash="new-source-cut",
                source_root_hash="new-source-root",
                prior_attempt_id=held["attempt_id"],
                supersession_grant_hash="g-source",
                attempt_no=2,
            )
        )
    assert error.value.code == "SOURCE_CHANGED_REQUIRES_FORK"
    assert a.conn.execute("SELECT count(*) FROM decision_receipt").fetchone()[0] == 1


def test_c7_raw_mirror_watermark_requires_exact_receipt(tmp_path):
    mirror = c9.MirrorStore(tmp_path / "mirror.db")
    mirror.add_root_branch(
        c12_branch_id="c12-raw",
        actor_id="A",
        actor_branch_epoch="e0",
        c12_root_hash="root",
        c12_created_clock=1,
    )
    with pytest.raises(sqlite3.IntegrityError):
        mirror.conn.execute(
            "UPDATE mirror_watermark SET last_seq=1,last_receipt_hash='x',"
            "last_projection_hash='y' WHERE c12_branch_id='c12-raw'"
        )
    with pytest.raises(sqlite3.IntegrityError):
        mirror.conn.execute("DELETE FROM mirror_branch")

    mirror.add_fork_branch(
        c12_branch_id="c12-fork-ready",
        actor_id="A",
        actor_branch_epoch="e0-fork",
        c12_parent_branch_id="c12-raw",
        c12_root_hash="fork-root",
        c12_fork_clock=1,
        c12_created_clock=1,
        c9_start_seq=0,
        c9_start_receipt_hash=None,
        base_c12_root_hash="root",
        base_c12_perception_hash="perception",
        base_c12_perception_count=0,
        mirror_state="FORK_READY",
    )
    mirror.hold_watermark("c12-fork-ready", "SYNC_HELD")
    assert mirror.verify()["ok"] is False


def test_c7_final_requires_issued_rule_issuance(tmp_path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    marker = add_world(a, "w-rule")
    a.add_rule(
        rule_hash="T-UNISSUED",
        rule_kind="T",
        issuer_ref="sourcefree-test",
        source_cut_hash=a.source_cut_hash,
        issued_state="HELD",
    )
    with pytest.raises(c9.Refusal) as error:
        a.publish(final_request(a, marker, "T-UNISSUED"))
    assert error.value.code == "ISSUED_RULE_T_REQUIRED"
    assert a.conn.execute("SELECT count(*) FROM decision_receipt").fetchone()[0] == 0


def test_c7_two_actors_same_target_and_normal_fork_ready(tmp_path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    b = c9.ActorAuthority(tmp_path / "actor.db", actor_id="B")
    add_world(a, "w-a")
    add_world(b, "w-b")
    a.publish(
        held_request(
            a,
            "w-a",
            key="a-target",
            event="a-event",
            target_id="legacy-target",
            target_hash="a-target-hash",
        )
    )
    b.publish(
        held_request(
            b,
            "w-b",
            key="b-target",
            event="b-event",
            target_id="legacy-target",
            target_hash="b-target-hash",
        )
    )
    rows = a.conn.execute(
        "SELECT actor_id,target_id FROM actor_target WHERE target_id='legacy-target' "
        "ORDER BY actor_id"
    ).fetchall()
    assert [(row["actor_id"], row["target_id"]) for row in rows] == [
        ("A", "legacy-target"),
        ("B", "legacy-target"),
    ]

    j = Path(
        "/Users/matthewsmith/Desktop/Rawlsing/rawlsing-join-e/WORKER_RETURNS/"
        "SOROK-20261022-SAME-PERSON-JOIN-R1/vendor/j"
    )
    if not (j / "candidate" / "vendor" / "bp4" / "bp4" / "store.py").exists():
        pytest.skip("C12 source unavailable")
    sys.path.insert(0, str(j / "candidate" / "vendor" / "bp4"))
    from bp4.store import C12Store

    path = tmp_path / "normal-c12.db"
    store = C12Store(path)
    store.create_root("root", clock=10, actor_ids=["A"], state={"world": 1})
    event = store.append_world_event(
        "root",
        {
            "schema": "BP4_C12_WORLD_EVENT@1",
            "branch_id": "root",
            "event_id": "ev-normal",
            "clock": 10,
            "body": {},
            "hash": "",
            "grade": "TEST_ONLY",
            "native": False,
        },
    )
    store.record_perception(
        "root", actor_id="A", event_id=event["event_id"], clock=10, channel="test"
    )
    store.close()
    guard = c9.c12_fork_guard(path, "root")
    assert guard["code"] == "C12_BASE_PERCEPTION_IDENTITY_UNPROVEN"
    ready = c9.c12_fork_guard(
        path,
        "root",
        expected_base_perception_hash=guard["base_perception_hash"],
    )
    assert ready["state"] == "FORK_READY"
    assert ready["fork_cut"] == 10


def test_c7_true_no_change_requires_issued_evaluation(tmp_path):
    a = c9.ActorAuthority(tmp_path / "actor.db", actor_id="A")
    marker = add_world(a, "w-true")
    a.add_rule(
        rule_hash="T-TRUE",
        rule_kind="T",
        issuer_ref="sourcefree-test",
        source_cut_hash=a.source_cut_hash,
    )
    result = a.publish(
        c9.PublishRequest(
            event_key="true-event",
            idempotency_key="true-key",
            decision_kind="TRUE_NO_CHANGE_EVALUATED",
            source_cut_hash=a.source_cut_hash,
            source_scope_hash="source-scope",
            settled_scope_hash="settled-scope",
            world_receipt_hash=marker,
            rule_t_hash="T-TRUE",
            rule_t_status="TRUE_NO_CHANGE_EVALUATED",
            evaluation_basis="ISSUED_RULE_T_EVALUATED",
            evaluated_readset_hash="readset-true",
        )
    )
    assert result["final"] is True
    version = a.conn.execute(
        "SELECT version_kind,canonical_state_json FROM actor_version "
        "WHERE version_no=1"
    ).fetchone()
    assert version["version_kind"] == "ADMINISTRATIVE_NOCHANGE"
    assert version["canonical_state_json"] == "{}"
    assert a.verify()["ok"] is True
