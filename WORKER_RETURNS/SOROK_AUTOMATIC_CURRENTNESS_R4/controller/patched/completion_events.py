"""Finite OS-event bridge for existing R157 terminal receipts; no timed polling.

Uses the installed controller's ordinary `codex queue` delivery primitive.
It neither registers jobs with that controller nor makes acceptance decisions.
One reserved dispatch per terminal process; ambiguous queue outcomes never retry.
"""
from pathlib import Path
import hashlib
import fcntl
import json
import os
import select
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
THREAD = os.environ.get("COMPLETION_THREAD")
CODEX = os.environ.get("COMPLETION_CODEX")


def save(path, value):
    temporary = path.with_suffix(".tmp")
    with temporary.open("w") as output:
        output.write(json.dumps(value, indent=2) + "\n")
        output.flush()
        os.fsync(output.fileno())
    temporary.replace(path)
    directory_fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


def sorok_currentness_hook(job):
    """Additive SOROK-only intake hook; absent env means no behavior change."""
    raw = os.environ.get("COMPLETION_SOROK_CURRENTNESS")
    if not raw:
        return None
    try:
        config = json.loads(raw)
    except (ValueError, TypeError):
        return {"state": "SOROK_CURRENTNESS_CONFIG_INVALID"}
    script = config.get("runtime_script")
    config_path = config.get("config_path")
    python = config.get("python", sys.executable)
    if not script or not config_path:
        return {"state": "SOROK_CURRENTNESS_CONFIG_INCOMPLETE"}
    command = [python, script, "--config", config_path, "intake-completion",
               "--run-dir", str(Path(job["completion_path"]).parent)]
    try:
        result = subprocess.run(command, capture_output=True, text=True,
                                timeout=120, shell=False)
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        return {
            "state": ("SOROK_CURRENTNESS_INTAKE_OK" if result.returncode == 0
                      else "SOROK_CURRENTNESS_INTAKE_FAILED"),
            "exit_code": result.returncode,
            "stdout_sha256": hashlib.sha256(stdout.encode()).hexdigest(),
            "stderr_sha256": hashlib.sha256(stderr.encode()).hexdigest(),
            "stderr_tail": stderr[-2000:],
            "hook_is_not_acceptance": True,
        }
    except Exception as error:
        return {"state": "SOROK_CURRENTNESS_HOOK_ERROR",
                "error": type(error).__name__, "hook_is_not_acceptance": True}


def main():
    assert THREAD and CODEX, "EXPLICIT_THREAD_AND_CODEX_BINDINGS_REQUIRED"
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "completion_event_targets.json"
    jobs = json.loads(target.read_text())
    receipt_dir = Path(os.environ["COMPLETION_RECEIPT_DIR"])
    receipt_dir.mkdir(parents=True, exist_ok=True)
    # The OS releases this lock on exit, including a terminated observer.
    # Keep the inode so concurrent restarts always contend on the same lock.
    lock = receipt_dir / "observer.lock"
    lock_fd = os.open(lock, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        os.close(lock_fd)
        raise RuntimeError("OBSERVER_ALREADY_RUNNING")
    os.ftruncate(lock_fd, 0)
    os.write(lock_fd, str(os.getpid()).encode())
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
        hook = sorok_currentness_hook(job)
        if hook is not None:
            record["sorok_currentness"] = hook
        save(reservation, record)
        qualification = any(label in job["task"] for label in
                            ("notification-qualification", "opencode-roundtrip"))
        continuation = (
            "For infrastructure qualification only, acknowledge receipt; do not launch work."
            if qualification else
            "Continue the existing authorized construction mission: inspect the actual "
            "return, recover retryable failures, integrate and publish evidence, and commission "
            "the next independent authorized work. Maintain 3-5 useful noncolliding lanes when "
            "dependencies permit. This receipt grants no new scientific, source or protected-merge authority."
        )
        message = (
            "Local supervised-job terminal notification; custody only, not acceptance.\n"
            f"task={job['task']} session={job['session']}\n"
            f"completion_path={job['completion_path']}\n"
            f"pid={completion['pid']} exit_code={completion['exit_code']}\n"
            "Read the exact durable terminal receipt and actual return before deciding. "
            + ("" if not record.get("sorok_currentness")
               or record["sorok_currentness"].get("state") == "SOROK_CURRENTNESS_INTAKE_OK"
               else "\nSOROK currentness intake is not OK: "
                    + str(record["sorok_currentness"].get("state"))
                    + " - reconcile before acting.")
            + continuation
        )
        if os.environ.get("COMPLETION_NOTIFY") != "1":
            record["state"] = "NOTIFICATION_DISABLED"
            save(reservation, record)
            return
        try:
            result = subprocess.run(
                [CODEX, "queue", "--thread", THREAD, "--message", message],
                capture_output=True, text=True, timeout=20, shell=False,
            )
            import re
            match = re.fullmatch(r"Queued message ([0-9a-f-]{36}) for thread " + re.escape(THREAD) + r"\.", result.stdout.strip())
            record.update({
                "queued_message_id": match.group(1) if match and result.returncode == 0 else None,
                "state": "QUEUE_RETURNED" if result.returncode == 0 and match else "AMBIGUOUS_HOLD",
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
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)


if __name__ == "__main__":
    main()
