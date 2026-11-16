"""Recovered Popen -> process.json -> wait -> completion.json supervisor.

Only changed bindings: explicit run/cwd, atomic receipts, parent launch handshake.
"""
import datetime
import json
import subprocess
import sys
from pathlib import Path
from completion_events import save


def main():
    run = Path(sys.argv[1]).resolve()
    job = json.loads((run / "job.json").read_text())
    binding = json.loads((run / "binding.json").read_text())
    identity = {k: job[k] for k in ("job_id", "session", "grant_id")}
    with (run / "stdout.jsonl").open("w") as out, (run / "stderr.log").open("w") as err:
        try:
            process = subprocess.Popen(job["argv"], cwd=binding["worktree"], stdout=out, stderr=err)
        except Exception as error:
            save(run / "launch-error.json", {**identity, "state": "LAUNCH_FAILED", "error": type(error).__name__})
            raise
        started = {**identity, "pid": process.pid, "started_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        save(run / "process.json", started)
        print(json.dumps(started), flush=True)  # one blocking parent handshake, no polling
        code = process.wait()
        save(run / "completion.json", {**started, "exit_code": code,
             "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
             "scope": binding["grant"]["scope"], "recipient_thread": binding["recipient_thread"]})


if __name__ == "__main__":
    main()
