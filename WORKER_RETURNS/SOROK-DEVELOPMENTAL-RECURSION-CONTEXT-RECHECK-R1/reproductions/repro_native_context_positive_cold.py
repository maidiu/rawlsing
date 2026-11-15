"""Focused positive/cold reproduction: native default and explicit contexts.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-CONTEXT-RECHECK-R1/reproductions/repro_native_context_positive_cold.py

Checks omitted, explicit-null, workshop and family contexts on the actual P2
owner, then reopens the exact root and reads the native S43 record.  The S43
record must carry the explicit milieu, not merely the session default.
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
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402


def run(label: str, context, include_key: bool) -> None:
    root = Path(tempfile.mkdtemp(prefix="sorok-context-cold-" + label + "-"))
    fanin = load_p2().start(root)
    case = fanin.deps["case_for"](True)
    pack = {
        "case": case,
        "source": fanin.deps["source_for"](case),
        "participants": tuple(fanin.session.read_root()["actor_ids"]),
    }
    owner = P2Owner(fanin, **pack)
    circumstances = {} if not include_key else {"language_context": context}
    try:
        before = owner.snapshot()
        proposal = EventProposal(
            "context-cold-" + label,
            before.clock + 6,
            "ADMIT_EVENT",
            (owner.source_ref,),
            owner.participants,
            circumstances,
            {"mode": "ACTUAL", "span": 4},
        )
        result = owner.realize("op-" + label, proposal, before)
        event_ref = result.objective["event"]["e1_event_id"]
        s43 = owner.fanin.session.read_s43_event(event_ref)
        print("===", label, "include_key", include_key, "context", context)
        print(
            " performed",
            result.objective["event"].get("performed"),
            "s43.context",
            (s43.get("s43") or {}).get("context"),
            "language.status",
            (s43.get("language") or {}).get("status"),
            "native_text",
            (s43.get("language") or {}).get("native_text"),
        )
        print(
            " event_hash",
            result.objective["event"]["e1_event_hash"],
            "plan_hash",
            (s43.get("language") or {}).get("plan_hash"),
        )
        owner.close()
        cold = P2Owner(load_p2().open(root), **pack)
        try:
            cold_s43 = cold.fanin.session.read_s43_event(event_ref)
            print(
                " cold s43.context",
                (cold_s43.get("s43") or {}).get("context"),
                "language.status",
                (cold_s43.get("language") or {}).get("status"),
                "performed",
                cold_s43.get("performed"),
            )
            print(
                " cold snapshot clock",
                cold.snapshot().clock,
                "s43_context",
                cold.fanin.session.s43_context(),
            )
        finally:
            cold.close()
    finally:
        try:
            owner.close()
        except Exception:
            pass


def main() -> int:
    run("default-omitted", None, False)
    run("default-null", None, True)
    run("workshop", {"milieu_id": "workshop"}, True)
    run("family", {"milieu_id": "family"}, True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
