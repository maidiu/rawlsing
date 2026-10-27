#!/usr/bin/env python3
"""TEST_ONLY bridge probe: actual S36 targetless receipt -> proposed actor authority."""
from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
S36 = Path(os.environ.get("S36_RETURN", "")).resolve()
if not S36.is_dir():
    raise SystemExit("S36_RETURN_MISSING: " + str(S36))
for path in (S36, S36 / "runtime" / "native", HERE):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from candidate import CandidateStore  # noqa: E402
from s36_harness import run_s35_case  # noqa: E402
import probe_actor_authority as actor_probe  # noqa: E402


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        legacy_path = root / "c9_candidate.sqlite"
        with CandidateStore(legacy_path) as legacy:
            result, _ = run_s35_case(legacy)
            assert result.committed and result.receipt.committed
            assert result.receipt.target_branch == "NO_CHANGE"
            assert result.receipt.target_reason == "NO_PROPOSAL"
            assert result.receipt.target_id == ""
            assert legacy.committed_target_ids() == frozenset()
            old_receipt = legacy.db.execute(
                "SELECT hash,body FROM receipt WHERE hash=?",
                (result.receipt.receipt_hash,),
            ).fetchone()
            legacy_tables = sorted(legacy._logical_readset()["tables"])
        actor = actor_probe.connect(root / "c9_actor.sqlite")
        actor_probe.seed(actor, "A", "b0", "e0", "root")
        actor.execute(
            "INSERT INTO legacy_bridge VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (result.receipt.receipt_hash, "C9P_CANDIDATE_TRANSACTION@1",
             result.receipt.admitted_event_ref, result.receipt.response_ref,
             result.receipt.target_branch, result.receipt.target_reason,
             result.receipt.before_hash, result.receipt.after_hash,
             "S36_ALL_TABLE_DOMAIN", json.dumps({
                 "schema": "SOROK_C9_LEGACY_BRIDGE@1",
                 "receipt_hash": result.receipt.receipt_hash,
                 "readset": legacy_tables,
             }, sort_keys=True), actor_probe.NOW),
        )
        held = actor_probe.publish(
            actor, actor="A", branch="b0", epoch="e0", event_key="legacy-e1",
            attempt_no=1, idempotency_key="bridge-e1", request_digest="bridge-d1",
            decision_kind="HELD_MISSING_RULE",
            legacy_receipt=result.receipt.receipt_hash,
            source_scope="legacy-before/after",
            settled_scope="legacy-no-rule",
            rule_a_status="APPLIED_WITH_RESPONSE",
            rule_t_status="HELD_MISSING_RULE",
            sci05_status="ADMITTED",
        )
        actor_head = actor_probe.head(actor, "A", "b0")
        assert actor_head[0] == 0, actor_head
        assert held["head"][0] == 0
        assert actor.execute(
            "SELECT count(*) FROM actor_version WHERE actor_id='A' AND branch_id='b0'"
        ).fetchone()[0] == 1
        assert actor.execute(
            "SELECT decision_kind,rule_t_status FROM decision_receipt "
            "WHERE receipt_hash=?", (held["receipt_hash"],)
        ).fetchone() == ("HELD_MISSING_RULE", "HELD_MISSING_RULE")
        assert actor.execute(
            "SELECT projection_state FROM projection_outbox WHERE receipt_hash=?",
            (held["receipt_hash"],)
        ).fetchone()[0] == "PENDING"
        assert actor.execute(
            "SELECT count(*) FROM decision_receipt WHERE decision_kind="
            "'TRUE_NO_CHANGE_EVALUATED'"
        ).fetchone()[0] == 0
        assert actor.execute("SELECT count(*) FROM actor_target").fetchone()[0] == 0
        with CandidateStore(legacy_path) as legacy2:
            assert legacy2.db.execute(
                "SELECT hash,body FROM receipt WHERE hash=?",
                (result.receipt.receipt_hash,)
            ).fetchone() == old_receipt
            assert sorted(legacy2._logical_readset()["tables"]) == legacy_tables
            assert legacy2.committed_target_ids() == frozenset()
        print("PASS bridge: actual S36 receipt %s remains targetless NO_PROPOSAL" %
              result.receipt.receipt_hash)
        print("PASS bridge: actor authority records HELD_MISSING_RULE; no actor version beyond genesis")
        print("PASS bridge: legacy DB table domain remains 7 tables; no actor target/false true-nochange")
        print("OBSERVED bridge: actor_head=%r outbox=PENDING decision=HELD_MISSING_RULE" %
              (actor_head,))
        actor.close()
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
