"""Independent reproduction: exact-subject accessible projection is the portal view.

Run from the repository root:

    PYTHONDONTWRITEBYTECODE=1 python3 -B \
      WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-INDEPENDENT-REVIEW-R1/reproductions/repro_actor_access.py

The exact subject (418639192) sends ``P2Owner.realize(...).accessible`` to the
retrospective provider.  That payload is ``P2ProductFanin.public_opportunity``,
whose ``view`` is ``S45Projection.project_view`` filtered by
``session.user_perceived_ids()`` for ``USER_ACTOR``.  It is the portal user's
view, not the developing actor's perception receipts.  The payload has no
developing-actor binding or perception receipts.  The later lead head
99e79810f replaces this with ``P2Owner.actor_experience``; that repair is not
part of the exact subject.
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
    root = Path(tempfile.mkdtemp(prefix="sorok-review-actor-access-"))
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
        proposals = [
            EventProposal(
                f"actor-access-{index}",
                before.clock + 6 * (index + 1),
                "ADMIT_EVENT",
                (owner.source_ref,),
                owner.participants,
                {},
                {"mode": "ACTUAL", "span": 4} if index == 0 else None,
            )
            for index in range(3)
        ]
        batch = BatchEngine(owner, root / "journal.sqlite").run_batch("actor-access", proposals)
        first = batch["records"][0]
        accessible = first["accessible"]
        print("root actor_ids:", owner.participants)
        print("user_actor:", fanin.session.meta.get("user_actor"))
        print("accessible keys:", sorted(accessible))
        print("accessible has actor_ref/status:", "actor_ref" in accessible, "status" in accessible)
        view = accessible.get("view") or {}
        visible = view.get("visible_events") or []
        print("view.visible_event_ids:", [row.get("event_id") for row in visible])
        print("view.perceived_by_user values:", [row.get("perceived_by_user") for row in visible])
        event = first["objective"].get("event") or {}
        action_id = event.get("action_event_id")
        action = fanin.session.event(action_id) if action_id else None
        alias = action.get("actor_id") if action else None
        print("action_event_id:", action_id)
        print("action alias:", alias)
        if alias:
            receipts = fanin.session.product.store.perceptions(
                fanin.session.branch_id, actor_id=alias
            )
            print(
                "developing-actor perception event_ids:",
                [row.get("event_id") for row in receipts],
            )
        user_receipts = fanin.session.product.store.perceptions(
            fanin.session.branch_id, actor_id=fanin.session.meta.get("user_actor")
        )
        print("portal-user perception event_ids:", [row.get("event_id") for row in user_receipts])
        # The exact subject's payload is the portal view and has no actor receipt
        # binding.  The later head adds status/actor_ref/perception receipts.
        assert view.get("schema") == "SOROK_WP19_ENCOUNTER_VIEW@1"
        assert "actor_ref" not in accessible
        assert "perceptions" not in accessible
        print("exact subject uses portal view: CONFIRMED")
        return 0
    finally:
        owner.close()


if __name__ == "__main__":
    raise SystemExit(main())
