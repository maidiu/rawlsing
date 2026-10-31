"""Bridge the sourcefree targetless C10 ledger to the same I1 guarded person.

`TargetlessGuardedJoinedProduct` is the unchanged I1 `GuardedJoinedProduct`
with one durable targetless-C10 receipt file under the same product root. It
does not create a second actor store or a C9 proposal/E2/practice/utterance.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from bp2p4.i1_product import GuardedJoinedProduct
from targetless_c10_consumer import TargetlessC10Ledger

TARGETLESS_FILE = "targetless_c10.json"
READ_SCHEMA = "SOROK_I1_TARGETLESS_C10_READ@1"


class TargetlessGuardedJoinedProduct(GuardedJoinedProduct):
    """Same I1 person/C12 store, plus a durable targetless-C10 receipt."""

    def targetless_history(self) -> list[TargetlessC10Ledger]:
        path = self.root / TARGETLESS_FILE
        if not path.exists():
            return []
        rows = json.loads(path.read_text(encoding="utf-8"))
        return [TargetlessC10Ledger.from_dict(row) for row in rows]

    def consume_targetless(self, ledger: TargetlessC10Ledger) -> dict[str, Any]:
        if not isinstance(ledger, TargetlessC10Ledger):
            raise TypeError("exact TargetlessC10Ledger required")
        history = self.targetless_history()
        history.append(ledger)
        (self.root / TARGETLESS_FILE).write_text(
            json.dumps([row.to_dict() for row in history], indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        return self.targetless_read()

    def targetless_read(self) -> dict[str, Any]:
        history = self.targetless_history()
        public = self.other()["public"]
        return {
            "schema": READ_SCHEMA,
            "same_person_product": "GuardedJoinedProduct",
            "branch_id": self.branch_id,
            "targetless_states": [row.state for row in history],
            "targetless_hashes": [row.receipt["receipt_hash"] for row in history],
            "can_read_B_behavior": any(
                row.action.observed and row.action.performed for row in history
            ),
            "tool_access": 1 if any(row.action.a_tool_access for row in history) else 0,
            "no_c9_target": all(row.c9_target is None for row in history),
            "no_performed_e2": all(not row.performed_e2 for row in history),
            "no_learned_practice": all(not row.learned_practice for row in history),
            "no_utterance": all(row.utterance is None for row in history),
            "a_public": public,
            "c12_ok": self.verify_c12()["ok"],
        }


__all__ = ["TargetlessGuardedJoinedProduct", "TARGETLESS_FILE"]
