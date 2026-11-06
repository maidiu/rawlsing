"""Independent E1 recheck: actual positive, control, cold reopen and refusal.

Run from the repository root (or exact-subject scratch root):

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      WORKER_RETURNS/SOROK-P3-E1-INDEPENDENT-INPUT-REVIEW-R1/reproductions/e1_positive_control_cold_refusal.py

This uses the exact E1 probe fixture and B1Owner adapter, not a generic canary.
It prints the actual B1 mediator persistence, the identical later-event control,
the cold-reopen equality, and a pre-effect refusal count.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

REPO = next(
    path for path in Path(__file__).resolve().parents if (path / "WORKER_RETURNS").is_dir()
)
PROBE = REPO / "WORKER_RETURNS/SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe"
ENGINE = REPO / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
for path in (str(ENGINE), str(PROBE)):
    if path not in sys.path:
        sys.path.insert(0, path)
os.chdir(REPO)

from dataclasses import replace  # noqa: E402

from b1_owner_adapter import B1Owner  # noqa: E402
from developmental_recursion.contracts import EventProposal, RecursionRefusal  # noqa: E402
from developmental_recursion.engine import BatchEngine  # noqa: E402
from test_b1_owner_adapter import make_owner, make_proposals, scenario  # noqa: E402


def main() -> int:
    tmp = Path(tempfile.mkdtemp(prefix="sorok-e1-recheck-"))
    positive, positive_engine, positive_result, positive_props, positive_journal = scenario(
        tmp, "positive"
    )
    try:
        print("== positive ==")
        print("statuses", [row["status"] for row in positive_result["records"]])
        print("event_hashes", [row["objective"]["event"]["hash"] for row in positive_result["records"]])
        print(
            "record state hashes",
            [
                (row["event_id"], row["before"]["state_hash"], row["after"]["state_hash"])
                for row in positive_result["records"]
            ],
        )
        mediator = positive_result["records"][0]["consequences"]["middle_state_ids"]
        mediator_records = positive_result["records"][0]["consequences"]["middle_state_record_hashes"]
        print("mediator_ids", mediator)
        print("mediator_record_hashes", mediator_records)
        print(
            "event3",
            positive_result["records"][2]["consequences"]["practical_activity"],
            positive_result["records"][2]["consequences"]["recruited"],
        )
        print("event1_accessible", positive_result["records"][0]["accessible"])
        before_reopen = positive.snapshot()
        positive.close()
        positive_engine.close()
        cold = B1Owner(tmp / "positive.sqlite", root="root-positive", branch="main")
        try:
            cold_engine = BatchEngine(cold, positive_journal)
            try:
                history = cold_engine.history("batch-positive")
                print("cold snapshot equal", cold.snapshot() == before_reopen)
                print("cold history equal", history["records"] == positive_result["records"])
                print("cold mediator_count", len(cold.state()["middle"]))
                print("cold response_count", len(cold.state()["responses"]))
            finally:
                cold_engine.close()
        finally:
            cold.close()
    finally:
        try:
            positive.close()
        except Exception:
            pass
        try:
            positive_engine.close()
        except Exception:
            pass

    control, control_engine, control_result, control_props, _control_journal = scenario(
        tmp, "control", journal_only=True
    )
    try:
        print("== control ==")
        print("proposals_equal", positive_props == control_props)
        print("statuses", [row["status"] for row in control_result["records"]])
        print("event_hashes", [row["objective"]["event"]["hash"] for row in control_result["records"]])
        print(
            "event3",
            control_result["records"][2]["consequences"]["practical_activity"],
            control_result["records"][2]["consequences"]["recruited"],
        )
        print("mediator_count", len(control.state()["middle"]))
        print(
            "same_event3_hash",
            positive_result["records"][2]["objective"]["event"]["hash"]
            == control_result["records"][2]["objective"]["event"]["hash"],
        )
    finally:
        control.close()
        control_engine.close()

    print("== refusal ==")
    owner = make_owner(tmp, "refusal")
    engine = BatchEngine(owner, tmp / "refusal.journal.sqlite")
    proposals = make_proposals(owner.source_ref)
    before = owner.snapshot()
    try:
        bad = replace(proposals[0], source_refs=("B1_FIXTURE:wrong",))
        try:
            engine.run_batch("bad", [bad, proposals[1], proposals[2]])
            print("UNEXPECTED refusal success")
        except RecursionRefusal as exc:
            print("refusal", str(exc))
        print("state_same", owner.snapshot() == before)
        print("occurrences", owner.db.execute("SELECT COUNT(*) FROM occurrence").fetchone()[0])
        print("operations", owner.db.execute("SELECT COUNT(*) FROM b1_operations").fetchone()[0])
        print("batches", engine._connect().execute("SELECT COUNT(*) FROM batches").fetchone()[0])
    finally:
        engine.close()
        owner.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
