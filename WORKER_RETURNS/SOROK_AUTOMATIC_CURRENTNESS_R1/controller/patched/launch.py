"""Finite local launcher using recovered supervisor and OS-event receipt bridge.

Operator-authored binding/grant files are local authority, not signed science grants.
No credential inspection, providers, model choices, services or recurring timers.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from completion_events import save


def command_digest(argv):
    return hashlib.sha256(json.dumps(argv, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()


def launch(binding_path, job_path):
    binding = json.loads(binding_path.read_text())
    job = json.loads(job_path.read_text())
    assert binding["schema"] == "LOCAL_COMPLETION_BINDING_V1"
    assert re.fullmatch(r"[0-9a-f-]{36}", binding["recipient_thread"])
    assert re.fullmatch(r"[A-Za-z0-9._-]+", job["job_id"])
    worktree = Path(binding["worktree"])
    state_root = Path(binding["state_root"])
    assert worktree.is_absolute() and worktree.is_dir()
    assert state_root.is_absolute() and state_root.is_dir()
    assert job["session"] == binding["session"] and job["grant_id"] == binding["grant"]["id"]
    assert job["job_id"] in binding["grant"]["job_ids"]
    expiry = datetime.datetime.fromisoformat(binding["grant"]["expires_utc"])
    assert expiry > datetime.datetime.now(datetime.timezone.utc), "GRANT_EXPIRED"
    assert isinstance(job["argv"], list) and job["argv"] and all(isinstance(v, str) for v in job["argv"])
    assert Path(job["argv"][0]).is_absolute(), "EXECUTABLE_MUST_BE_ABSOLUTE"
    assert command_digest(job["argv"]) == binding["grant"]["argv_sha256"], "COMMAND_NOT_GRANTED"
    assert Path(binding["codex_binary"]).is_absolute()
    run = state_root / job["job_id"]
    run.mkdir(mode=0o700)  # exclusive reservation; never restart an existing job
    save(run / "job.json", job)
    save(run / "binding.json", binding)
    root = Path(__file__).resolve().parent
    with (run / "supervisor.log").open("w") as err:
        supervisor = subprocess.Popen([sys.executable, str(root / "supervisor.py"), str(run)],
            stdout=subprocess.PIPE, stderr=err, text=True, start_new_session=True)
    line = supervisor.stdout.readline()  # waits for exact child PID, no timed loop
    supervisor.stdout.close()
    if not line:
        raise RuntimeError("LAUNCH_HELD: inspect supervisor.log and launch-error.json; no retry")
    process = json.loads(line)
    targets = [{"task": job["job_id"], "session": job["session"], "pid": process["pid"],
                "completion_path": str(run / "completion.json")}]
    save(run / "targets.json", targets)
    env = dict(os.environ, COMPLETION_THREAD=binding["recipient_thread"],
               COMPLETION_CODEX=binding["codex_binary"], COMPLETION_RECEIPT_DIR=str(run / "events"),
               COMPLETION_NOTIFY="1" if binding["notify"] else "0")
    # Additive SOROK-only hook: bindings without this field are unchanged.
    sorok_currentness = binding.get("sorok_currentness")
    if isinstance(sorok_currentness, dict):
        env["COMPLETION_SOROK_CURRENTNESS"] = json.dumps(
            sorok_currentness, sort_keys=True)
    with (run / "observer.log").open("w") as log:
        observer = subprocess.Popen([sys.executable, str(root / "completion_events.py"), str(run / "targets.json")],
            env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    receipt = {"job_id": job["job_id"], "child_pid": process["pid"], "supervisor_pid": supervisor.pid,
               "observer_pid": observer.pid, "run_dir": str(run), "launch_is_not_completion": True}
    save(run / "launch.json", receipt)
    return receipt


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--binding", required=True, type=Path)
    parser.add_argument("--job", required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(launch(args.binding.resolve(), args.job.resolve()), indent=2))
