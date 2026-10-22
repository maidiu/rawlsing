"""Post-repair branch-lineage and parent-integrity attacks for 75a134e."""
import json
from pathlib import Path

import pytest

from joined.refusal import RefusalSession
from joined.session import JoinedSession
from r30a.first_session import SessionRefusal
from support import read_meta, start, write_meta


def _branch_rows(session, branch):
    return session.product.store.episodes(branch)


def test_refusal_fork_receipt_and_parent_integrity(tmp_path):
    state = tmp_path / "fork"
    session = RefusalSession.start(state)
    try:
        parent_episodes = _branch_rows(session, "first_session")
        parent_counts = session.product.store.verify("first_session")["counts"]
        forked = session.fork_alt("alt")
        branch = session.product.store.branch("alt")
        receipt = session.meta["branch_lineage"]["fork_receipt"]
        assert forked["status"] == "OK"
        assert session.branch_id == "alt"
        assert session.meta["branch_id"] == "alt"
        assert receipt["parent_branch"] == "first_session"
        assert receipt["new_branch"] == "alt"
        assert receipt["fork_clock"] == branch["fork_clock"]
        assert receipt["root_hash"] == branch["root_hash"]
        assert _branch_rows(session, "first_session") == parent_episodes
        assert session.product.store.verify("first_session")["counts"] == parent_counts
        session.say("Back at the bench.")
        assert _branch_rows(session, "first_session") == parent_episodes
        assert session.verify()["ok"] is True
    finally:
        session.close()

    cold = RefusalSession.open(state)
    try:
        assert cold.branch_id == "alt"
        assert cold.verify()["ok"] is True
        assert _branch_rows(cold, "first_session") == parent_episodes
        assert cold.product.store.verify("first_session")["counts"] == parent_counts
    finally:
        cold.close()


def test_refusal_fork_parent_not_corrupted_positive(tmp_path):
    state = tmp_path / "fork_parent"
    session = RefusalSession.start(state)
    parent_episodes = _branch_rows(session, "first_session")
    parent_counts = session.product.store.verify("first_session")["counts"]
    try:
        session.fork_alt("alt")
        assert _branch_rows(session, "first_session") == parent_episodes
        assert session.product.store.verify("first_session")["counts"] == parent_counts
        session.say("Back at the bench.")
        assert _branch_rows(session, "first_session") == parent_episodes
        assert session.product.store.verify("first_session")["counts"] == parent_counts
        assert session.verify()["ok"] is True
    finally:
        session.close()
    cold = RefusalSession.open(state)
    try:
        assert cold.branch_id == "alt"
        assert cold.verify()["ok"] is True
        assert _branch_rows(cold, "first_session") == parent_episodes
        assert cold.product.store.verify("first_session")["counts"] == parent_counts
    finally:
        cold.close()


def test_refusal_parent_metadata_switch_refused(tmp_path):
    state = tmp_path / "parent_switch"
    session = RefusalSession.start(state)
    session.fork_alt("alt")
    session.close()
    meta = read_meta(state)
    meta["branch_id"] = "first_session"
    write_meta(state, meta)
    try:
        opened = RefusalSession.open(state)
    except SessionRefusal as exc:
        assert exc.code in {"UNAUTHORIZED_BRANCH", "BRANCH_LINEAGE_MISMATCH"}
        return
    try:
        pytest.fail(json.dumps({
            "case": "refusal_parent_metadata_switch",
            "opened": True,
            "branch_id": opened.branch_id,
            "branch_lineage": opened.meta.get("branch_lineage"),
            "verify": opened.verify().get("ok"),
        }, sort_keys=True))
    finally:
        opened.close()


def test_joined_parent_metadata_switch_refused(tmp_path):
    state = tmp_path / "joined_parent_switch"
    session = start(state, perform="omit")
    session.fork_alt("alt")
    session.close()
    meta = read_meta(state)
    meta["branch_id"] = "first_session"
    write_meta(state, meta)
    try:
        opened = JoinedSession.open(state)
    except SessionRefusal as exc:
        assert exc.code in {"UNAUTHORIZED_BRANCH", "BRANCH_LINEAGE_MISMATCH"}
        return
    try:
        pytest.fail(json.dumps({
            "case": "joined_parent_metadata_switch",
            "opened": True,
            "branch_id": opened.branch_id,
            "branch_lineage": opened.meta.get("branch_lineage"),
            "verify": opened.verify().get("ok"),
        }, sort_keys=True))
    finally:
        opened.close()
