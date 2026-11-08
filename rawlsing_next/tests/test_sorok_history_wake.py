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


def test_p4_wake_completes_through_a_mock_http_endpoint(tmp_path, monkeypatch):
    from http.server import BaseHTTPRequestHandler, HTTPServer
    import os
    from queue import Queue
    from subprocess import run
    from threading import Thread
    from time import monotonic, sleep

    monkeypatch.syspath_prepend(str(P4))
    from run_p4 import foreground_lock, open_owner
    from rawlsing_next.sorok_history.owner import HistoricalWorld

    packets = Queue()

    class MockEndpoint(BaseHTTPRequestHandler):
        def do_POST(self):
            request = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            prompt = request["messages"][0]["content"]
            packet = json.loads(prompt.split("Packet:\n", 1)[1])
            packets.put(packet)
            candidate = {
                "request_id": packet["request_id"],
                "facts": [{
                    "target_id": packet["target_ids"][0], "predicate": "texture",
                    "value": "matte", "effective_time": packet["time"],
                    "dependency_group": "physical", "asserted_H_class": "H0",
                }],
                "occurrences": [], "links": [],
                "dependencies": [{
                    "group_id": "physical", "parent_refs": packet["event_refs"],
                    "parent_groups": [], "asserted_H_class": "H0",
                }],
            }
            payload = json.dumps({
                "model": "test-endpoint",
                "choices": [{"message": {"content": json.dumps(candidate)}}],
            }).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, *args):
            pass

    env = {key: value for key, value in os.environ.items()
           if not key.startswith("SOROK_HISTORY_")}
    cli = [sys.executable, str(P4 / "run_p4.py"), "--state", str(tmp_path)]
    with HTTPServer(("127.0.0.1", 0), MockEndpoint) as server:
        request_thread = Thread(target=server.handle_request)
        server.timeout = 60
        request_thread.start()
        try:
            opened = run(
                cli + ["new"], capture_output=True, text=True, check=True, timeout=90,
                env={**env, "SOROK_HISTORY_MODEL": "test-endpoint",
                     "SOROK_HISTORY_MODEL_ENDPOINT": f"http://127.0.0.1:{server.server_port}"},
            )
            assert "matte" not in opened.stdout
            packet = packets.get(timeout=45)
        finally:
            request_thread.join()

    with foreground_lock(tmp_path):
        owner = open_owner(tmp_path / "actual-p2")
    try:
        history = HistoricalWorld(owner.base_owner.fanin.session)
        deadline = monotonic() + 15
        while True:
            job = history.job(packet["request_id"])
            if job["status"] not in {"RUNNING", "CANDIDATE_READY"} or monotonic() >= deadline:
                break
            sleep(0.1)
        assert job["status"] == "INDEX_READY", job
        assert job["provider_receipt"]["model"] == "test-endpoint"
    finally:
        owner.close()

    inspected = run(
        cli + ["inspect-particular", packet["target_ids"][0]],
        capture_output=True, text=True, check=True, timeout=45, env=env,
    )
    [fact] = json.loads(inspected.stdout)["observation"]["physical"]
    assert fact["value"] == "matte"
    assert fact["fact_id"] == job["admission"]["accepted"][0]["fact_ids"][0]
