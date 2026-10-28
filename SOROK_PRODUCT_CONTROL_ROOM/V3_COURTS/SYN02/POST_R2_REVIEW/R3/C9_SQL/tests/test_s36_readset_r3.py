"""C9-R3 test: separate actor DB leaves actual S36 seven-table readset unchanged."""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

import c9_actor_r3 as r3


def test_actual_s36_seven_table_domain_is_unchanged_by_actor_db(tmp_path):
    raw = os.environ.get("S36_RETURN", "")
    root = Path(raw).expanduser() if raw else Path()
    if not raw or not root.is_absolute() or not root.is_dir():
        pytest.skip("S36_RETURN_MISSING")
    for path in (root, root / "runtime" / "native"):
        if str(path) not in sys.path:
            sys.path.insert(0, str(path))
    from candidate import CandidateStore
    from s36_harness import run_s35_case

    legacy_path = tmp_path / "legacy.sqlite"
    with CandidateStore(legacy_path) as legacy:
        result, _ = run_s35_case(legacy)
        assert result.committed and result.receipt.committed
        old_receipt = legacy.db.execute(
            "SELECT hash,body FROM receipt WHERE hash=?",
            (result.receipt.receipt_hash,),
        ).fetchone()
        old_tables = sorted(legacy._logical_readset()["tables"])

    actor = r3.connect(tmp_path / "actor.sqlite")
    r3.seed(actor, "A", "b0", "e0", "c12-root")
    r3.publish(
        actor, actor="A", branch="b0", epoch="e0", event_key="legacy-event",
        attempt_no=1, idempotency_key="legacy-key", request_digest="legacy-digest",
        decision_kind="HELD_MISSING_RULE", legacy_receipt=result.receipt.receipt_hash,
        source_scope="source-legacy", settled_scope="settled-legacy",
        rule_t_status="HELD_MISSING_RULE", sci05_status="HELD",
    )
    actor.close()

    with CandidateStore(legacy_path) as legacy:
        assert sorted(legacy._logical_readset()["tables"]) == old_tables
        assert set(legacy._logical_readset()["tables"]) == {
            "clock", "event_identity", "occurrence", "receipt", "response",
            "target_journal", "target_state",
        }
        assert legacy.db.execute(
            "SELECT hash,body FROM receipt WHERE hash=?",
            (result.receipt.receipt_hash,),
        ).fetchone() == old_receipt
        assert legacy.committed_target_ids() == frozenset()
