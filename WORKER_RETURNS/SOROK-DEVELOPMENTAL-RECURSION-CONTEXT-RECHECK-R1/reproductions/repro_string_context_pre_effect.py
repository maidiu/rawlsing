"""Focused reproduction: malformed explicit language_context refuses pre-effect.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-CONTEXT-RECHECK-R1/reproductions/repro_string_context_pre_effect.py

The first proposal carries an ACTUAL interval and a string language_context.
The exact-subject preflight must refuse before the owner clock, interval state,
owner operation table, or engine journal changes.
"""
from __future__ import annotations

import os
import sqlite3
import sys
import tempfile
from pathlib import Path

REPO = next(
    path for path in Path(__file__).resolve().parents if (path / "WORKER_RETURNS").is_dir()
)
sys.path.insert(0, str(REPO / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
os.chdir(REPO)

from developmental_recursion.contracts import EventProposal, RecursionRefusal  # noqa: E402
from developmental_recursion.engine import BatchEngine  # noqa: E402
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-context-string-"))
    fanin = load_p2().start(root)
    case = fanin.deps["case_for"](True)
    owner = P2Owner(
        fanin,
        case=case,
        source=fanin.deps["source_for"](case),
        participants=tuple(fanin.session.read_root()["actor_ids"]),
    )
    try:
        before = owner.snapshot()
        journal = root / "journal.sqlite"
        engine = BatchEngine(owner, journal)
        first = EventProposal(
            "bad-string",
            before.clock + 6,
            "ADMIT_EVENT",
            (owner.source_ref,),
            owner.participants,
            {"language_context": "invalid-context"},
            {"mode": "ACTUAL", "span": 4},
        )
        later = [
            EventProposal(
                f"ok-{index}",
                before.clock + 6 * index,
                "ADMIT_EVENT",
                (owner.source_ref,),
                owner.participants,
                {},
                None,
            )
            for index in (2, 3)
        ]
        try:
            engine.run_batch("bad-string", [first, *later])
            print("UNEXPECTED: batch succeeded")
        except RecursionRefusal as exc:
            print("refused:", str(exc))
        after = owner.snapshot()
        connection = sqlite3.connect(journal)
        try:
            batches = connection.execute("select count(*) from batches").fetchone()[0]
            events = connection.execute("select count(*) from events").fetchone()[0]
        finally:
            connection.close()
        operations = owner.db.execute("select count(*) from operations").fetchone()[0]
        print("batches", batches, "events", events)
        print(
            "state_same",
            before == after,
            "clock",
            before.clock,
            after.clock,
            "intervals",
            len(fanin.session.read_interval_states()),
            "ops",
            operations,
        )
        try:
            engine.run_batch("bad-string", [first, *later])
            print("UNEXPECTED: retry succeeded")
        except RecursionRefusal as exc:
            print("same input retry refused:", str(exc))
        return 0
    finally:
        owner.close()


if __name__ == "__main__":
    raise SystemExit(main())
