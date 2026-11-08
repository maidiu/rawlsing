"""Finite OS-event bridge for existing R157 terminal receipts; no timed polling.

Uses the installed controller's ordinary `codex queue` delivery primitive.
It neither registers jobs with that controller nor makes acceptance decisions.
One reserved dispatch per terminal process; ambiguous queue outcomes never retry.
"""
from pathlib import Path
import hashlib
import json
import os
import select
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
THREAD = "01a15c1e-5446-7ef3-80bb-9ff5c2cb27da"
CODEX = "/Applications/ChatGPT.app/Contents/Resources/codex-cli/CodexCLI.app/Contents/MacOS/codex"


def save(path, value):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(value, indent=2) + "\n")
    temporary.replace(path)


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "completion_event_targets.json"
    jobs = json.loads(target.read_text())
    receipt_dir = ROOT / ".completion-events"
    if len(sys.argv) > 1:
        receipt_dir = receipt_dir / target.stem
    receipt_dir.mkdir(parents=True, exist_ok=True)
    # One observer for this finite target set; stale-lock deletion is never automatic.
    lock = receipt_dir / "observer.lock"
    fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    os.write(fd, str(os.getpid()).encode())
    os.close(fd)
    queue = select.kqueue()
    handles = {}

    def watch(path):
        if str(path) in handles:
            return
        handle = os.open(path, os.O_RDONLY)
        handles[str(path)] = handle
        queue.control([select.kevent(
            handle, filter=select.KQ_FILTER_VNODE,
            flags=select.KQ_EV_ADD | select.KQ_EV_CLEAR,
            fflags=select.KQ_NOTE_WRITE | select.KQ_NOTE_EXTEND | select.KQ_NOTE_RENAME,
        )], 0, 0)

    def dispatch(job, completion, key):
        reservation = receipt_dir / (key + ".json")
        if reservation.exists():
            return
        record = {
            "task": job["task"], "session": job["session"],
            "thread": THREAD, "completion_path": job["completion_path"],
            "completion": completion, "state": "DISPATCH_RESERVED_NO_RETRY",
            "reserved_at": time.time(), "model_override": None,
        }
        save(reservation, record)
        message = (
            "R157 existing-job terminal notification; perform the existing scoped intake.\n"
            f"task={job['task']} session={job['session']}\n"
            f"completion_path={job['completion_path']}\n"
            f"pid={completion['pid']} exit_code={completion['exit_code']}\n"
            "Read actual return/commit/evidence before deciding. This is custody only, "
            "not acceptance or new authority. Preserve sealed plan and source/workload "
            "boundary; advance necessary ready work without duplicating effects. "
            "Heartbeat stays paused; no model/effort/provider change."
        )
        try:
            result = subprocess.run(
                [CODEX, "queue", "--thread", THREAD, "--message", message],
                capture_output=True, text=True, timeout=20, shell=False,
            )
            record.update({
                "state": "QUEUE_RETURNED" if result.returncode == 0 else "AMBIGUOUS_HOLD",
                "exit_code": result.returncode,
                "stdout": result.stdout[:8000],
                "stderr_sha256": hashlib.sha256(result.stderr.encode()).hexdigest(),
                "queue_ack_is_not_observed_hq_turn": True,
            })
        except Exception as error:
            record.update({"state": "AMBIGUOUS_HOLD", "error": type(error).__name__})
        save(reservation, record)

    try:
        for job in jobs:
            watch(Path(job["completion_path"]).parent)
        save(receipt_dir / "ready.json", {
            "pid": os.getpid(), "thread": THREAD, "targets": len(jobs),
            "mode": "KQUEUE_OS_FILE_EVENTS_NO_PERIODIC_POLLING", "interval": None,
        })
        remaining = list(jobs)
        while remaining:
            pending = []
            for job in remaining:
                path = Path(job["completion_path"])
                if not path.exists():
                    pending.append(job)
                    continue
                try:
                    completion = json.loads(path.read_text())
                    if completion["pid"] != job["pid"]:
                        raise ValueError("terminal receipt PID mismatch")
                    int(completion["exit_code"])
                except (json.JSONDecodeError, KeyError):
                    # Creation may precede final write: await that file's WRITE event.
                    watch(path)
                    pending.append(job)
                    continue
                key = hashlib.sha256((str(path) + str(job["pid"])).encode()).hexdigest()
                dispatch(job, completion, key)
            remaining = pending
            if remaining:
                queue.control(None, 1, None)  # OS blocks until a relevant vnode event.
        save(receipt_dir / "finished.json", {"pid": os.getpid(), "all_targets_terminal": True})
    finally:
        for handle in handles.values():
            os.close(handle)
        queue.close()
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
