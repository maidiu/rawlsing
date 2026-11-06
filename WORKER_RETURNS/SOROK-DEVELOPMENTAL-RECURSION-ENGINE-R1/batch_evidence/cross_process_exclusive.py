"""Cross-process exclusive-execution evidence for the batch engine.

Two operating-system processes share one journal and one durable owner.  The
first holds the engine lock while its owner is deliberately slow.  The second
must wait, then start from the first batch's actual final state.  Evidence only.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
PACKAGE_ROOT = HERE.parent
if str(PACKAGE_ROOT) not in sys.path:
    sys.path.insert(0, str(PACKAGE_ROOT))
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from developmental_recursion.engine import BatchEngine  # noqa: E402
from hard_crash_recovery import DurableOwner, make_proposals  # noqa: E402


def run_child() -> None:
    root = Path(os.environ["SOROK_STATE"])
    prefix = os.environ["SOROK_PREFIX"]
    start = int(os.environ["SOROK_START"])
    owner = DurableOwner(root)
    engine = BatchEngine(owner, root / "journal.sqlite")
    result = engine.run_batch("batch-" + prefix, make_proposals(prefix, start))
    print(
        json.dumps(
            {
                "prefix": prefix,
                "history_hash": result["history_hash"],
                "event_ids": [record["event_id"] for record in result["records"]],
            },
            sort_keys=True,
        )
    )


def wait_for_reservation(journal: Path, event_id: str, timeout: float = 10.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if journal.is_file():
            connection = sqlite3.connect(journal)
            try:
                row = connection.execute(
                    "SELECT status FROM events WHERE event_id=?", (event_id,)
                ).fetchone()
            finally:
                connection.close()
            if row == ("RESERVED",):
                return
        time.sleep(0.02)
    raise SystemExit("timed out waiting for reservation " + event_id)


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="sorok-engine-cross-process-") as directory:
        root = Path(directory)
        DurableOwner(root)  # create the shared owner state before either child
        journal = root / "journal.sqlite"
        first_env = dict(os.environ)
        first_env.update(
            {
                "SOROK_STATE": str(root),
                "SOROK_PREFIX": "a",
                "SOROK_START": "1",
                "SOROK_SLOW_EVENT": "a1",
            }
        )
        first = subprocess.Popen(
            [sys.executable, str(Path(__file__).resolve())],
            env=first_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        wait_for_reservation(journal, "a1")

        second_env = dict(os.environ)
        second_env.update(
            {
                "SOROK_STATE": str(root),
                "SOROK_PREFIX": "b",
                "SOROK_START": "4",
            }
        )
        second = subprocess.run(
            [sys.executable, str(Path(__file__).resolve())],
            env=second_env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        first_stdout, first_stderr = first.communicate(timeout=30)
        if first.returncode != 0:
            raise SystemExit(
                "first process failed: "
                + str(first.returncode)
                + "\n"
                + first_stderr
            )
        if second.returncode != 0:
            raise SystemExit(
                "second process failed: "
                + str(second.returncode)
                + "\n"
                + second.stderr
            )

        owner = DurableOwner(root)
        engine = BatchEngine(owner, journal)
        assert engine.verify() is True
        first_result = json.loads(first_stdout)
        second_result = json.loads(second.stdout)
        assert first_result["event_ids"] == ["a1", "a2", "a3"]
        assert second_result["event_ids"] == ["b1", "b2", "b3"]
        state = json.loads((root / "owner.json").read_text(encoding="utf-8"))
        assert state["order"] == ["a1", "a2", "a3", "b1", "b2", "b3"]
        assert len(state["order"]) == len(set(state["order"])) == 6
        print(
            json.dumps(
                {
                    "first": first_result,
                    "second": second_result,
                    "owner_order": state["order"],
                    "duplicate_effects": len(state["order"]) - len(set(state["order"])),
                    "final_clock": owner.snapshot().clock,
                    "verified": True,
                },
                indent=2,
                sort_keys=True,
            )
        )


if __name__ == "__main__":
    if os.environ.get("SOROK_STATE") and os.environ.get("SOROK_PREFIX"):
        run_child()
    else:
        main()
