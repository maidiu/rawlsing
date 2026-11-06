"""Independent privacy walker check for the exact-subject P2 accessible payloads.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-INDEPENDENT-REVIEW-R1/reproductions/repro_privacy.py

This checks the inherited P2 public-key privacy walker against the exact
subject's accessible payloads.  It does not cure finding R1: the payload is the
portal user's view, not the developing actor's perception receipts.
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
    root = Path(tempfile.mkdtemp(prefix="sorok-review-privacy-"))
    fanin = load_p2().start(root)
    case = fanin.deps["case_for"](True)
    owner = P2Owner(
        fanin,
        case=case,
        source=fanin.deps["source_for"](case),
        participants=tuple(fanin.session.read_root()["actor_ids"]),
    )
    from p2_continuation.continuation import privacy_hits

    try:
        before = owner.snapshot()
        proposals = [
            EventProposal(
                f"privacy-{index}",
                before.clock + 6 * (index + 1),
                "ADMIT_EVENT",
                (owner.source_ref,),
                owner.participants,
                {},
                {"mode": "ACTUAL", "span": 4} if index == 0 else None,
            )
            for index in range(3)
        ]
        batch = BatchEngine(owner, root / "journal.sqlite").run_batch("privacy", proposals)
        for record in batch["records"]:
            hits = privacy_hits(record["accessible"])
            print(record["event_id"], "privacy_hits=", hits)
            print("accessible_keys=", sorted(record["accessible"]))
        return 0
    finally:
        owner.close()


if __name__ == "__main__":
    raise SystemExit(main())
