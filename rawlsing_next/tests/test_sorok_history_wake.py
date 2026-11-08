import fcntl
import json
from pathlib import Path
import sys

import pytest


P4 = (Path(__file__).resolve().parents[2] / "WORKER_RETURNS"
      / "SOROK-P4-FIRST-FULL-MPC-R1")


@pytest.mark.parametrize("configured", [False, True])
def test_p4_new_wakes_history_after_foreground_publication(
    tmp_path, monkeypatch, capsys, configured,
):
    monkeypatch.syspath_prepend(str(P4))
    from run_p4 import main

    for key in ("SOROK_HISTORY_MODEL_ENDPOINT", "SOROK_HISTORY_ENDPOINT",
                "SOROK_HISTORY_MODEL", "SOROK_HISTORY_MODEL_ID"):
        monkeypatch.delenv(key, raising=False)
    if configured:
        monkeypatch.setenv("SOROK_HISTORY_MODEL_ENDPOINT", "https://unused.invalid/v1")
        monkeypatch.setenv("SOROK_HISTORY_MODEL", "test-model")

    calls = []

    def new(state, ledger_file, history):
        ledger_file.write_text(json.dumps({"pending": None}))
        return {"status": "READY"}

    def launch(args, **kwargs):
        assert json.loads((tmp_path / "p4_receipts.json").read_text()) == {"pending": None}
        with (tmp_path / "p4.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        assert args == [sys.executable, str(P4 / "run_p4.py"),
                        "--state", str(tmp_path), "history-worker"]
        assert kwargs["start_new_session"]
        calls.append(args)

    monkeypatch.setattr("run_p4.new", new)
    monkeypatch.setattr("run_p4.subprocess.Popen", launch)
    monkeypatch.setattr(sys, "argv", ["run_p4.py", "--state", str(tmp_path), "new"])
    assert main() == 0
    assert json.loads(capsys.readouterr().out) == {"status": "READY"}
    assert len(calls) == int(configured)


def test_worker_releases_foreground_guard_during_inference():
    import asyncio
    from contextlib import contextmanager
    from types import SimpleNamespace

    from rawlsing_next.sorok_history.runtime import run_once

    locked = False

    @contextmanager
    def guard():
        nonlocal locked
        assert not locked
        locked = True
        try:
            yield
        finally:
            locked = False

    class History:
        def ready_candidate_id(self):
            assert locked

        def lease(self, *, seconds):
            assert locked
            return {"job": {"id": "job", "lease_token": "lease"}, "packet": {}}

        def record_candidate(self, job, token, candidate, receipt):
            assert locked
            return "CANDIDATE_READY"

        def commit_candidate(self, job):
            assert locked
            return {"status": "INDEX_READY"}

    class Provider:
        async def propose(self, packet):
            assert not locked
            await asyncio.sleep(0)
            assert not locked
            return SimpleNamespace(
                candidate={}, receipt=SimpleNamespace(as_dict=dict)
            )

    assert asyncio.run(run_once(History(), Provider(), guard=guard)) == {
        "status": "INDEX_READY"
    }
    assert not locked
