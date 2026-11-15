"""Minimal independent witness: repeated depth-2 promotion commits, then severs.

Product read-only. One fresh scratch P2 state. The public writer is called twice
with distinct operation IDs at depth 2. The second call raises custody refusal
after committing a change+head whose PROMOTE depth is not greater than the
already verified depth. The relation scope is then permanently severed through
the public API.
"""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
EVIDENCE = HERE.parent / "evidence"
ENGINE = REPO / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
SCRATCH = REPO / ".local-logs/sorok-c05-independent-g5/scratch"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from developmental_recursion.continuing_relations import (  # noqa: E402
    RELATION_CHANGE_KIND,
    RELATION_HEAD_KIND,
    promote_relation,
    read_relation_history,
    record_relation_change,
)
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.p2_owner import load_p2  # noqa: E402
from developmental_recursion.supporting_actor import (  # noqa: E402
    register_supporting_actor,
)

P_ID = "TEST_ONLY_C05_DEFECT_PARENT"
O_ID = "TEST_ONLY_C05_DEFECT_NEIGHBOR"
REL = "defect-household"


def count_kind(session, kind: str) -> int:
    return len([
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("kind") == kind
    ])


def snapshot(session) -> dict:
    store = session.product.store
    return {
        "relation_status": read_relation_history(session, P_ID)["status"],
        "episodes": len(store.episodes(session.branch_id)),
        "changes": count_kind(session, RELATION_CHANGE_KIND),
        "heads": count_kind(session, RELATION_HEAD_KIND),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
        "c12_verify_ok": store.verify(session.branch_id)["ok"],
        "promotions": [
            {
                "operation_id": (row.get("body") or {}).get("operation_id"),
                "sequence": (row.get("body") or {}).get("sequence"),
                "promoted_depth": (row.get("body") or {}).get("promoted_depth"),
                "previous_episode_id": (
                    row.get("body") or {}).get("previous_episode_id"),
            }
            for row in store.episodes(session.branch_id)
            if row.get("kind") == RELATION_CHANGE_KIND
            and (row.get("body") or {}).get("change") == "PROMOTE"
        ],
    }


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    state = Path(tempfile.mkdtemp(prefix="defect-", dir=SCRATCH)) / "p2"
    fanin = load_p2().start(state)
    report = {
        "schema": "SOROK_C05_REPEAT_PROMOTION_DEFECT@1",
        "reviewer_session": "ses_e2186e745ffecK1Ilg4cw26pVu",
        "candidate_sha": "9cf13763b0061400e2c936eaf1d0a2f4b76a03f7",
        "state_root": str(state),
    }
    try:
        session = fanin.session
        register_supporting_actor(
            session, alias="DP", actor_id=P_ID, role="parent",
            private_state={"motive": "defect-private"})
        register_supporting_actor(
            session, alias="DO", actor_id=O_ID, role="neighbor",
            private_state={"motive": "defect-private"})
        record_relation_change(
            session, actor_id=P_ID, other_actor_id=O_ID, relation=REL,
            change="ENTER", clock=session.world().clock,
            operation_id="defect:enter", exposed_actor_ids=[P_ID, O_ID],
            value="guest")
        first = promote_relation(
            session, actor_id=P_ID, other_actor_id=O_ID, relation=REL,
            depth=2, clock=session.world().clock,
            operation_id="defect:promote:1")
        before = snapshot(session)
        second_result = None
        second_refusal = None
        try:
            second_result = promote_relation(
                session, actor_id=P_ID, other_actor_id=O_ID, relation=REL,
                depth=2, clock=session.world().clock,
                operation_id="defect:promote:2")
        except RecursionRefusal as exc:
            second_refusal = str(exc)
        after = snapshot(session)
        retry_first = None
        try:
            retry_first = promote_relation(
                session, actor_id=P_ID, other_actor_id=O_ID, relation=REL,
                depth=2, clock=first["clock"],
                operation_id="defect:promote:1")
        except RecursionRefusal as exc:
            retry_first = {"refusal": str(exc)}
        report.update({
            "first_promotion": {
                "status": first["status"],
                "representation_depth": first["representation_depth"],
                "primary_episode_id": first["primary_episode_id"],
            },
            "before_second": before,
            "second_call_returned": second_result,
            "second_call_refusal": second_refusal,
            "after_second": after,
            "retry_first_after_second": (
                retry_first if isinstance(retry_first, dict)
                else {
                    "status": retry_first.get("status"),
                    "primary_episode_id": retry_first.get(
                        "primary_episode_id"),
                }
            ),
            "wrote_episode_on_refusal": (
                after["episodes"] == before["episodes"] + 2
                and after["changes"] == before["changes"] + 1
                and after["heads"] == before["heads"] + 1
                and after["world_events"] == before["world_events"]
                and after["perceptions"] == before["perceptions"]
                and after["checkpoints"] == before["checkpoints"]
            ),
            "scope_severed_after_write": (
                before["relation_status"] == "QUALIFIED"
                and after["relation_status"] == "HOLD_CUSTODY_SEVERED"
            ),
            "c12_verify_unchanged": (
                before["c12_verify_ok"] and after["c12_verify_ok"]),
            "defect": (
                "promote_relation's pre-write depth check uses only "
                "RELATION_STATE_CHANGES, so a prior PROMOTE is invisible; a "
                "second depth-2 PROMOTE is appended, then _verify_scope "
                "rejects promoted_depth <= current depth and the committed "
                "episode severs the scope."
            ),
        })
    finally:
        fanin.close()
    path = EVIDENCE / "c05_defect_report.json"
    path.write_text(json.dumps(report, indent=2, sort_keys=True))
    print(json.dumps({
        "defect": report.get("defect"),
        "second_call_refusal": report.get("second_call_refusal"),
        "wrote_episode_on_refusal": report.get("wrote_episode_on_refusal"),
        "scope_severed_after_write": report.get("scope_severed_after_write"),
        "c12_verify_unchanged": report.get("c12_verify_unchanged"),
        "report": str(path),
    }, indent=2, sort_keys=True))
    ok = (
        report.get("second_call_refusal") == "RELATION_CUSTODY_SEVERED"
        and report.get("wrote_episode_on_refusal") is True
        and report.get("scope_severed_after_write") is True
    )
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
