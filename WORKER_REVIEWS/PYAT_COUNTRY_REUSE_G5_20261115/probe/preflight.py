"""Capture one pre-timing native process/CPU contention snapshot."""
from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
REPO = BASE.parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from court_instrumentation import preflight_snapshot


def main() -> int:
    snapshot = preflight_snapshot(repo=REPO)
    out = BASE / "evidence" / "preflight.json"
    out.write_text(json.dumps(snapshot, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({
        "utc": snapshot["utc"],
        "git_head": snapshot["git_head"],
        "git_branch": snapshot["git_branch"],
        "python": snapshot["python"].splitlines()[0],
        "cpu_count": snapshot["cpu_count"],
        "load_average_1_5_15": snapshot["load_average_1_5_15"],
        "packages": snapshot["packages"],
        "other_rawlsing_process_count": snapshot["other_rawlsing_process_count"],
        "estate_disk": snapshot["estate_disk"],
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
