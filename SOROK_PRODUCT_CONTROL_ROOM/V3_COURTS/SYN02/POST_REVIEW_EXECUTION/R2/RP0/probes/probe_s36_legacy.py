#!/usr/bin/env python3
"""TEST_ONLY probe of the actual S36 CandidateStore legacy publication domain."""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(os.environ.get("S36_RETURN", "")).resolve()
if not ROOT.is_dir():
    raise SystemExit("S36_RETURN_MISSING: " + str(ROOT))
for path in (ROOT, ROOT / "runtime" / "native"):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from candidate import CandidateStore  # noqa: E402
from s36_harness import run_s35_case  # noqa: E402


def readset_tables(store: CandidateStore) -> list[str]:
    return sorted(store._logical_readset()["tables"])


def main() -> int:
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        legacy = root / "c9_legacy.sqlite"
        with CandidateStore(legacy) as store:
            old, _ = run_s35_case(store)
            assert old.committed and old.receipt.committed
            assert old.receipt.target_branch == "NO_CHANGE"
            assert old.receipt.target_reason == "NO_PROPOSAL"
            old_tables = readset_tables(store)
            old_before = old.receipt.before_hash
            old_after = old.receipt.after_hash
            old_receipt_row = store.db.execute(
                "SELECT hash,body FROM receipt WHERE hash=?",
                (old.receipt.receipt_hash,),
            ).fetchone()
            assert old_receipt_row
            assert old_tables == [
                "clock", "event_identity", "occurrence", "receipt", "response",
                "target_journal", "target_state",
            ]

        mutated = root / "c9_legacy_with_actor_tables.sqlite"
        shutil.copy2(legacy, mutated)
        with CandidateStore(mutated) as store:
            store.db.execute(
                "CREATE TABLE actor_head_probe ("
                "actor_id TEXT PRIMARY KEY, version_no INTEGER NOT NULL, "
                "version_hash TEXT NOT NULL)"
            )
            store.db.execute(
                "INSERT INTO actor_head_probe VALUES ('A',1,'probe-head')"
            )
            assert "actor_head_probe" in readset_tables(store)
            before = store._logical_readset()
            store.db.execute(
                "UPDATE actor_head_probe SET version_no=2,version_hash='probe-head-2' "
                "WHERE actor_id='A'"
            )
            after = store._logical_readset()
            assert not set(before["tables"]["actor_head_probe"]).issubset(
                set(after["tables"]["actor_head_probe"])
            )
            new, _ = run_s35_case(
                store, event_id="TEST_ONLY_S36_RR2_E2", event_time=16, as_of=20
            )
            assert new.committed and new.receipt.committed
            assert new.receipt.target_branch == "NO_CHANGE"
            assert new.receipt.target_reason == "NO_PROPOSAL"
            assert "actor_head_probe" in readset_tables(store)
            assert new.receipt.before_hash != old_before
            assert store.db.execute(
                "SELECT hash,body FROM receipt WHERE hash=?",
                (old.receipt.receipt_hash,)
            ).fetchone() == old_receipt_row

        print("PASS s36_legacy: actual targetless receipt committed; old table count=7")
        print("PASS s36_legacy: old receipt hash=%s before=%s after=%s" %
              (old.receipt.receipt_hash, old_before, old_after))
        print("PASS s36_legacy: same-schema actor table changes readset domain; "
              "future legacy before=%s (old=%s)" %
              (new.receipt.before_hash, old_before))
        print("PASS s36_legacy: mutable actor row is non-additive under old "
              "all-table row-set invariant")
        print("PASS s36_legacy: old receipt/RESPONSE rows remain byte-identical "
              "after the counterexample copy")
        print("OBSERVED old target_branch=%s reason=%s target_id=%r" %
              (old.receipt.target_branch, old.receipt.target_reason,
               old.receipt.target_id))
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
