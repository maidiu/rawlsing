"""Limit observation: registry-valid but event-intent-incompatible context.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-CONTEXT-RECHECK-R1/reproductions/repro_public_known_context_limit.py

The P2 fixture attempt is REQUEST_TOOL.  ``public`` is a real S43 registry
milieu, but the registry has no REQUEST_TOOL/public unit.  The exact-subject
preflight checks registry membership only, so this known context passes
preflight and the native S43 returns an explicit no-speech refusal.  This is
outside the specified Mapping/milieu-membership repair; it is recorded as a
limit, not as the malformed-string field failure.
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


def main() -> int:
    root = Path(tempfile.mkdtemp(prefix="sorok-context-public-"))
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
        proposal = EventProposal(
            "context-public",
            before.clock + 6,
            "ADMIT_EVENT",
            (owner.source_ref,),
            owner.participants,
            {"language_context": {"milieu_id": "public"}},
            {"mode": "ACTUAL", "span": 4},
        )
        result = owner.realize("op-public", proposal, before)
        event_ref = result.objective["event"]["e1_event_id"]
        read = owner.fanin.session.read_s43_event(event_ref)
        print("event status", result.status)
        print("performed", result.objective["event"].get("performed"))
        print("accessible status", result.accessible.get("status"))
        print("s43.context", (read.get("s43") or {}).get("context"))
        print("s43_refusal", read.get("s43_refusal"))
        print("language", read.get("language"))
        print("clock", result.after.clock)
        print("intervals", len(owner.fanin.session.read_interval_states()))
        return 0
    finally:
        owner.close()


if __name__ == "__main__":
    raise SystemExit(main())
