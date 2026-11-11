"""Independent reproduction: invalid native grounding mutates interval state.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-INDEPENDENT-REVIEW-R1/reproductions/repro_invalid_grounding.py

The first proposal carries an explicit ACTUAL interval and a ``history_refs``
entry that does not exist.  ``P2Owner.validate_proposal`` accepts it because it
never inspects the refs.  The interval is produced first; native ``admit_event``
then refuses the missing ref.  The engine has already reserved the operation,
so the interval result is not in engine history and the batch cannot be
retried without an ambiguous-operation hold.
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
    root = Path(tempfile.mkdtemp(prefix="sorok-review-invalid-grounding-"))
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
                "bad-grounding-1",
                before.clock + 6,
                "ADMIT_EVENT",
                (owner.source_ref,),
                owner.participants,
                {"history_refs": ["does-not-exist"]},
                {"mode": "ACTUAL", "span": 4},
            ),
            EventProposal(
                "bad-grounding-2",
                before.clock + 12,
                "ADMIT_EVENT",
                (owner.source_ref,),
                owner.participants,
                {},
                None,
            ),
            EventProposal(
                "bad-grounding-3",
                before.clock + 18,
                "ADMIT_EVENT",
                (owner.source_ref,),
                owner.participants,
                {},
                None,
            ),
        ]
        try:
            engine.run_batch("bad-grounding", proposals)
            print("UNEXPECTED: batch succeeded")
        except Exception as exc:  # noqa: BLE001 - reproduction prints the refusal
            print("batch exception:", type(exc).__name__, str(exc)[:300])
        after = owner.snapshot()
        print("before clock/state", before.clock, before.state_hash[:16])
        print("after  clock/state", after.clock, after.state_hash[:16])
        print("state changed:", before != after)
        print("history records:", len(engine.history("bad-grounding")["records"]))
        print("verify:", engine.verify())
        import sqlite3

        connection = sqlite3.connect(journal)
        try:
            rows = connection.execute(
                "select event_index,status,result_json,last_error "
                "from events order by event_index"
            ).fetchall()
        finally:
            connection.close()
        print("journal rows:", rows)
        try:
            engine.run_batch("bad-grounding", proposals)
            print("UNEXPECTED: retry succeeded")
        except Exception as exc:  # noqa: BLE001 - reproduction prints the refusal
            print("retry exception:", type(exc).__name__, str(exc)[:300])
        print("state after retry:", owner.snapshot().clock, owner.snapshot().state_hash[:16])
        return 0
    finally:
        owner.close()


if __name__ == "__main__":
    raise SystemExit(main())
