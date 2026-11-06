"""Focused positive reproduction: valid explicit context in a later proposal.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-CONTEXT-RECHECK-R1/reproductions/repro_later_valid_context.py

A three-event ACTUAL/ordinary batch uses workshop on event 1, explicit family
on event 2 and workshop on event 3.  The native S43 records must carry the
per-event context, not just the session default.
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
    root = Path(tempfile.mkdtemp(prefix="sorok-context-later-positive-"))
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
        engine = BatchEngine(owner, root / "journal.sqlite")

        def proposal(index: int, context=None, interval=None) -> EventProposal:
            return EventProposal(
                f"valid-later-{index}",
                before.clock + 6 * index,
                "ADMIT_EVENT",
                (owner.source_ref,),
                owner.participants,
                {} if context is None else {"language_context": context},
                interval,
            )

        proposals = [
            proposal(1, None, {"mode": "ACTUAL", "span": 4}),
            proposal(2, {"milieu_id": "family"}),
            proposal(3, None),
        ]
        batch = engine.run_batch("valid-later", proposals)
        print("statuses", [record["status"] for record in batch["records"]])
        for record in batch["records"]:
            event = record["objective"]["event"]
            event_ref = event.get("e1_event_id")
            s43 = owner.fanin.session.read_s43_event(event_ref) if event_ref else {}
            print(
                record["event_id"],
                "performed",
                event.get("performed"),
                "s43.context",
                (s43.get("s43") or {}).get("context"),
                "language.status",
                (s43.get("language") or {}).get("status"),
                "event_hash",
                event.get("e1_event_hash"),
            )
        print("verify", engine.verify(), "clock", owner.snapshot().clock)
        return 0
    finally:
        owner.close()


if __name__ == "__main__":
    raise SystemExit(main())
