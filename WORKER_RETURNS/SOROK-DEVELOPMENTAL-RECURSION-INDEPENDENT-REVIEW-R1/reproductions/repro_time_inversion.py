"""Independent reproduction: out-of-order event times are accepted pre-effect.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-INDEPENDENT-REVIEW-R1/reproductions/repro_time_inversion.py

All three proposal times are greater than the starting clock, so per-proposal
validation accepts them.  The engine does not enforce nondecreasing batch
event_time.  Event 1 realizes at clock 240; event 2 then fails the native
future-clock check at 230 and the batch is permanently stuck with event 1
already recorded.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

REPO = next(
    path for path in Path(__file__).resolve().parents if (path / "WORKER_RETURNS").is_dir()
)
sys.path.insert(0, str(REPO / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"))
os.chdir(REPO)

from developmental_recursion.contracts import EventProposal  # noqa: E402
from developmental_recursion.engine import BatchEngine  # noqa: E402
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-review-time-inversion-"))
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
        proposals = [
            EventProposal(
                "t1",
                before.clock + 18,
                "ADMIT_EVENT",
                (owner.source_ref,),
                owner.participants,
                {},
                None,
            ),
            EventProposal(
                "t2",
                before.clock + 6,
                "ADMIT_EVENT",
                (owner.source_ref,),
                owner.participants,
                {},
                None,
            ),
            EventProposal(
                "t3",
                before.clock + 24,
                "ADMIT_EVENT",
                (owner.source_ref,),
                owner.participants,
                {},
                None,
            ),
        ]
        try:
            engine.run_batch("time-inversion", proposals)
            print("UNEXPECTED: batch succeeded")
        except Exception as exc:  # noqa: BLE001 - reproduction prints the refusal
            print("exception:", type(exc).__name__, str(exc)[:200])
        print(
            "before",
            before.clock,
            "after",
            owner.snapshot().clock,
            "changed",
            before != owner.snapshot(),
        )
        print(
            "records",
            [record["event_id"] for record in engine.history("time-inversion")["records"]],
        )
        import sqlite3

        connection = sqlite3.connect(journal)
        try:
            rows = connection.execute(
                "select event_index,status,result_json is not null,last_error "
                "from events order by event_index"
            ).fetchall()
        finally:
            connection.close()
        print("rows", rows)
        try:
            engine.run_batch("time-inversion", proposals)
            print("UNEXPECTED: retry succeeded")
        except Exception as exc:  # noqa: BLE001 - reproduction prints the refusal
            print("retry:", type(exc).__name__, str(exc)[:200])
        return 0
    finally:
        owner.close()


if __name__ == "__main__":
    raise SystemExit(main())
