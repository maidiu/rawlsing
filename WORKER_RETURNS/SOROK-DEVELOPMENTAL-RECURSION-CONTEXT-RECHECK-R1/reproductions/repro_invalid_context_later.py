"""Focused reproduction: invalid later-proposal context refuses before first interval.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-CONTEXT-RECHECK-R1/reproductions/repro_invalid_context_later.py

The first proposal is a valid ACTUAL-interval proposal; the third proposal
carries each malformed/absent/unknown language_context.  Batch-level validation
must refuse before the first event, interval, owner operation or journal claim.
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


def proposal(owner: P2Owner, index: int, context=None, interval=None) -> EventProposal:
    return EventProposal(
        f"context-later-{index}",
        owner.snapshot().clock + 6 * index,
        "ADMIT_EVENT",
        (owner.source_ref,),
        owner.participants,
        {} if context is None else {"language_context": context},
        interval,
    )


def main() -> int:
    cases = [
        ("string", "invalid-context"),
        ("list", []),
        ("empty-dict", {}),
        ("milieu-list", {"milieu_id": []}),
        ("milieu-empty", {"milieu_id": ""}),
        ("unknown", {"milieu_id": "MISSING_NATIVE_CONTEXT"}),
    ]
    for label, bad in cases:
        root = Path(tempfile.mkdtemp(prefix="sorok-context-later-" + label + "-"))
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
                proposal(owner, 1, interval={"mode": "ACTUAL", "span": 4}),
                proposal(owner, 2),
                proposal(owner, 3, context=bad),
            ]
            try:
                engine.run_batch("later-" + label, proposals)
                print(label, "UNEXPECTED success")
            except RecursionRefusal as exc:
                print(label, "refused:", str(exc))
            after = owner.snapshot()
            connection = sqlite3.connect(journal)
            try:
                batches = connection.execute("select count(*) from batches").fetchone()[0]
                events = connection.execute("select count(*) from events").fetchone()[0]
            finally:
                connection.close()
            operations = owner.db.execute("select count(*) from operations").fetchone()[0]
            print(
                "  state_same",
                before == after,
                "clock",
                before.clock,
                after.clock,
                "intervals",
                len(fanin.session.read_interval_states()),
                "ops",
                operations,
                "batches",
                batches,
                "events",
                events,
            )
        finally:
            owner.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
