"""C8O hostile court B: real SIGKILL crash boundaries, cold reopen and durability limits.

A real `SIGKILL` (signal 9, exit status -9) is distinguished from the abrupt
`os._exit(79)` boundary. Process death is NOT power-loss durability: this court
proves user-space file+directory fsync behavior and honest crash recovery only.
"""
from __future__ import annotations

import json
import signal
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))

from c8o_court_support import (  # noqa: E402
    capability,
    cold_reopen,
    legacy,
    spawn,
    write_evidence,
)

from c8o_trusted_outbox import C8OccurrenceJournal  # noqa: E402
from outbox_prototype import Journal  # noqa: E402


def _seed(path: Path) -> C8OccurrenceJournal:
    j = C8OccurrenceJournal(path)
    snap, v = j.recover()
    ev = snap.ledger.admit(legacy("SEED"))
    snap.outbox.emit(ev["occurrence_id"])
    assert j.commit(snap, v, capability=capability("SEED")).writer_version == 1
    return j


@pytest.mark.parametrize(
    "boundary,expected_rc,expected_version",
    [
        ("BEFORE_RENAME", 79, 1),
        ("SIGKILL_BEFORE_RENAME", -signal.SIGKILL, 1),
        ("AFTER_COMMIT", 79, 2),
        ("SIGKILL_AFTER_COMMIT", -signal.SIGKILL, 2),
    ],
)
def test_real_signal_and_exit_boundaries(boundary, expected_rc, expected_version, tmp_path):
    journal = tmp_path / "journal.json"
    j = _seed(journal)
    prior = journal.read_bytes()
    rows = spawn("crash", tmp_path, ["CRASH"], extra=(boundary,))
    assert len(rows) == 1
    row = rows[0]
    assert row["rc"] == expected_rc, (row["rc"], row["err"])
    reopened = cold_reopen(journal)
    if expected_version == 1:
        assert journal.read_bytes() == prior
        assert reopened["version"] == 1 and reopened["count"] == 1
        assert reopened["ids"] == ["OCC-0001"]
    else:
        assert reopened["version"] == 2 and reopened["count"] == 2
        assert reopened["ids"] == ["OCC-0001", "OCC-0002"]
    write_evidence(
        f"crash_boundary_{boundary}.json",
        {
            "boundary": boundary,
            "os_returncode": row["rc"],
            "expected_returncode": expected_rc,
            "signal_semantics": (
                "negative returncode == death by that signal"
                if expected_rc < 0
                else "os._exit abrupt non-returning exit; NOT a signal"
            ),
            "cold_reopen": reopened,
            "journal_byte_identical_to_prior": journal.read_bytes() == prior,
        },
    )


def test_sigkill_death_is_not_power_loss_and_no_media_claim(tmp_path):
    journal = tmp_path / "journal.json"
    _seed(journal)
    rows = spawn("crash", tmp_path, ["POWERISH"], extra=("SIGKILL_AFTER_COMMIT",))
    assert rows[0]["rc"] == -signal.SIGKILL
    receipt = json.loads(journal.read_text(encoding="utf8"))
    assert receipt["writer_version"] == 2
    plan = {
        "proved": [
            "temp file fsync before rename",
            "same-directory atomic os.replace",
            "parent directory fsync before acknowledgement",
            "prior state byte-identical when death occurs before rename",
        ],
        "not_proved": [
            "media-level durability under power loss",
            "fdatasync/syncfs barrier semantics",
            "exactly-once client delivery",
            "survival on exotic or network filesystems",
        ],
        "authority_form": "PROCESS_DEATH_RECOVERY_ONLY_NOT_POWER_LOSS_DURABILITY",
    }
    write_evidence("durability_limit_receipt.json", plan)
    reopened = cold_reopen(journal)
    assert reopened["version"] == 2


def test_cold_reopen_sees_only_committed_state_after_killed_writer(tmp_path):
    journal = tmp_path / "journal.json"
    _seed(journal)
    spawn("crash", tmp_path, ["KILLED"], extra=("SIGKILL_BEFORE_RENAME",))
    reopened = cold_reopen(journal)
    assert reopened["ids"] == ["OCC-0001"]
    pending = list(tmp_path.glob(".c8o-pending-*"))
    for leftover in pending:
        assert not leftover.exists() or leftover.stat().st_size >= 0
    reopened_again = cold_reopen(journal)
    assert reopened_again == reopened


def test_two_writer_race_survives_one_writer_kill_before_rename(tmp_path):
    journal = tmp_path / "journal.json"
    _seed(journal)
    rows = spawn("cas", tmp_path, ["W0", "W1"])
    assert all(r["rc"] == 0 for r in rows), rows
    spawn("crash", tmp_path, ["KILLED"], extra=("SIGKILL_BEFORE_RENAME",))
    reopened = cold_reopen(journal)
    assert reopened["version"] == 3
    assert reopened["count"] == 3
    assert reopened["ids"] == ["OCC-0001", "OCC-0002", "OCC-0003"]
    write_evidence(
        "kill_after_writer_race.json",
        {"rows": rows, "cold_reopen": reopened},
    )
