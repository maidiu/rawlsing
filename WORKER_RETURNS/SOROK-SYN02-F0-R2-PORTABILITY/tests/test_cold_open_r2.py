"""R2 cold-open, fork/failure, cleanup and non-mutation adversaries."""
from __future__ import annotations

import json
import shutil
import tempfile
from copy import deepcopy
from pathlib import Path

import pytest

from s52.bootstrap import install

install()

from s51.session import S51Session  # noqa: E402
from s52.session import (  # noqa: E402
    CANDIDATE_KIND,
    S52ColdOpenRefusal,
    S52Session,
    candidate_digest,
)
from r30a.first_session import SessionRefusal  # noqa: E402
from s45.fixtures import root_bundle  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402


def _start(state):
    case = case_for(True)
    return S52Session.start(
        state,
        bundle=root_bundle("01" * 32),
        case=case,
        source=source_for(case),
        language_context={"milieu_id": "workshop"},
    )


def _forge(session):
    actual = session.run_experiment()
    forged = deepcopy(actual["candidate"])
    forged.pop("episode_id", None)
    forged["task_parameters"]["payment_per_actor"] = 999
    forged["candidate_hash"] = candidate_digest(forged)
    forged["repertoire"]["candidate_hash"] = forged["candidate_hash"]
    session._append(CANDIDATE_KIND, forged)


def test_base_s51_remains_ok_while_s52_refuses_cold_error():
    root = Path(tempfile.mkdtemp())
    session = _start(root)
    try:
        _forge(session)
    finally:
        session.close()
    base = S51Session.open(root)
    try:
        assert base.verify()["ok"] is True
        assert base.verify()["s51"]["errors"] == []
    finally:
        base.close()
    with pytest.raises(S52ColdOpenRefusal) as exc:
        S52Session.open(root)
    assert exc.value.code == "S52_COLD_OPEN_INVALID"
    assert "S52_CANDIDATE_SEMANTIC_INVALID" in str(exc.value)


def test_moved_cold_fork_is_refused_and_original_remains_clean():
    root = Path(tempfile.mkdtemp())
    session = _start(root)
    try:
        session.run_experiment()
    finally:
        session.close()
    fork = Path(tempfile.mkdtemp()) / "fork"
    shutil.copytree(root, fork)
    with pytest.raises(SessionRefusal) as exc:
        S52Session.open(fork)
    assert exc.value.code == "SESSION_ROOT_MOVED"
    reopened = S52Session.open(root)
    try:
        assert reopened.verify()["ok"] is True
    finally:
        reopened.close()


def test_unexpected_parent_refusal_is_not_masked(monkeypatch, tmp_path):
    def boom(cls, *args, **kwargs):
        raise SessionRefusal("PARENT_BUG")

    monkeypatch.setattr(S51Session, "open", classmethod(boom))
    with pytest.raises(SessionRefusal) as exc:
        S52Session.open(tmp_path)
    assert exc.value.code == "PARENT_BUG"


def test_false_verify_and_verify_exception_close_session(monkeypatch, tmp_path):
    closed = []

    class Fake:
        def __init__(self, mode):
            self.mode = mode

        def verify(self):
            if self.mode == "raise":
                raise RuntimeError("verify boom")
            return {"ok": False, "s52": {"errors": ["S52_ONLY"]}}

        def close(self):
            closed.append(self.mode)

    monkeypatch.setattr(
        S51Session, "open", classmethod(lambda cls, *args, **kwargs: Fake("false"))
    )
    with pytest.raises(S52ColdOpenRefusal) as exc:
        S52Session.open(tmp_path)
    assert exc.value.code == "S52_COLD_OPEN_INVALID"
    assert closed == ["false"]

    monkeypatch.setattr(
        S51Session, "open", classmethod(lambda cls, *args, **kwargs: Fake("raise"))
    )
    with pytest.raises(RuntimeError, match="verify boom"):
        S52Session.open(tmp_path)
    assert closed == ["false", "raise"]


def test_verify_is_non_mutating_and_not_native():
    session = _start(Path(tempfile.mkdtemp()))
    try:
        before = json.dumps(session.world().snapshot(), sort_keys=True)
        result = session.verify()
        after = json.dumps(session.world().snapshot(), sort_keys=True)
        assert result["ok"] is True
        assert result["s52"]["native"] is False
        assert before == after
    finally:
        session.close()
