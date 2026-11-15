"""Independent R2 closure probe for the exact repeated-promotion defect.

Product read-only. Fresh scratch P2 state. Verifies the corrected public writer
refuses a different new depth-2 operation before any append, with zero relation /
world / perception / checkpoint deltas, exact relation history and later-event
context, and an unchanged original-operation retry.
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
SCRATCH = REPO / ".local-logs/sorok-c05-focused-r2/scratch"
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from developmental_recursion.continuing_relations import (  # noqa: E402
    RELATION_CHANGE_KIND,
    promote_relation,
    read_actor_relative_context,
    read_relation_history,
    record_relation_change,
)
from developmental_recursion.contracts import (  # noqa: E402
    EventProposal,
    RecursionRefusal,
    canonical,
    digest,
)
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from developmental_recursion.supporting_actor import (  # noqa: E402
    register_supporting_actor,
)

P_ID = "TEST_ONLY_C05_R2_CLOSURE_PARENT"
O_ID = "TEST_ONLY_C05_R2_CLOSURE_NEIGHBOR"
RELATION = "closure-household"


def counts(session) -> dict:
    store = session.product.store
    episodes = store.episodes(session.branch_id)
    return {
        "episodes": len(episodes),
        "changes": len([
            row for row in episodes if row.get("kind") == RELATION_CHANGE_KIND
        ]),
        "world_events": len(store.world_events(session.branch_id)),
        "perceptions": len(store.perceptions(session.branch_id)),
        "checkpoints": len(store.checkpoints(session.branch_id)),
    }


def refusal_code(fn):
    try:
        fn()
    except RecursionRefusal as exc:
        return str(exc)
    return None


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    SCRATCH.mkdir(parents=True, exist_ok=True)
    state = Path(tempfile.mkdtemp(prefix="closure-", dir=SCRATCH)) / "p2"
    fanin = load_p2().start(state)
    report = {
        "schema": "SOROK_C05_R2_INDEPENDENT_CLOSURE@1",
        "candidate_sha": "5d771dd86767655534b23576075e5da2db4fba78",
        "report_commit": "1cf1a37113cb7a48137734648b523a0a6deccd92",
        "reviewer_session": "ses_e2186e745ffecK1Ilg4cw26pVu",
        "state_root": str(state),
    }
    checks = []

    def check(name, value):
        checks.append({"name": name, "pass": bool(value)})
        return bool(value)

    try:
        session = fanin.session
        focal = session.read_root()["actor_ids"][0]
        register_supporting_actor(
            session, alias="CP", actor_id=P_ID, role="parent",
            private_state={"motive": "closure-parent-private"})
        register_supporting_actor(
            session, alias="CO", actor_id=O_ID, role="neighbor",
            private_state={"motive": "closure-neighbor-private"})
        case = fanin.deps["case_for"](True)
        owner = P2Owner(
            fanin, case=case, source=fanin.deps["source_for"](case),
            participants=(focal, P_ID, O_ID))
        try:
            record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="ENTER",
                clock=session.world().clock,
                operation_id="closure:enter", exposed_actor_ids=[P_ID, O_ID],
                value="guest")
            before_event = owner.snapshot()
            proposal = EventProposal(
                "closure:event", before_event.clock + 6, "ADMIT_EVENT",
                (owner.source_ref,), (focal, P_ID, O_ID), {})
            result = owner.realize("closure:op:event", proposal, before_event)
            event_id = result.consequences[
                "supporting_participants"][0]["event_id"]
            event_clock = session.event(event_id)["clock"]
            first = promote_relation(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, depth=2, clock=session.world().clock,
                operation_id="closure:promote:1")
            history = read_relation_history(
                session, P_ID, as_of_clock=event_clock)
            context = read_actor_relative_context(session, P_ID, event_id)
            baseline_counts = counts(session)
            baseline_world = session.world().snapshot()
            baseline_events = session.events()
            baseline_perceptions = session.product.store.perceptions(
                session.branch_id)
            baseline_checkpoints = session.product.store.checkpoints(
                session.branch_id)
            baseline_episodes = session.product.store.episodes(
                session.branch_id)
            enter_row = next(
                row for row in baseline_episodes
                if row.get("kind") == RELATION_CHANGE_KIND
                and (row.get("body") or {}).get("change") == "ENTER")
            promotion_row = next(
                row for row in baseline_episodes
                if row.get("kind") == RELATION_CHANGE_KIND
                and (row.get("body") or {}).get("operation_id")
                == "closure:promote:1")
            enter_body = enter_row["body"]
            expected_history_hash = digest([{
                "episode_id": enter_row["episode_id"],
                "episode_hash": enter_row["hash"],
                "clock": enter_body["clock"],
                "change": enter_body["change"],
                "value": enter_body.get("value"),
                "operation_id": enter_body["operation_id"],
            }])
            check("first_promotion_recorded",
                  first["status"] == "RECORDED"
                  and first["representation_depth"] == 2)
            check("history_depth_two",
                  history["status"] == "QUALIFIED"
                  and history["relations"][0]["representation_depth"] == 2)
            check("context_qualified_perceived",
                  context["relation_scope"]["status"] == "QUALIFIED"
                  and context["event_access"]["status"] == "PERCEIVED")
            check("promotion_history_hash_is_state_entries_only",
                  promotion_row["body"]["history_hash"]
                  == expected_history_hash)
            retry = promote_relation(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, depth=2, clock=first["clock"],
                operation_id="closure:promote:1")
            check("original_operation_retry_unchanged",
                  retry["status"] == "UNCHANGED"
                  and retry["primary_episode_id"]
                  == first["primary_episode_id"]
                  and counts(session) == baseline_counts)
            second_refusal = refusal_code(lambda: promote_relation(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, depth=2, clock=session.world().clock,
                operation_id="closure:promote:2"))
            check("different_new_depth2_refused_before_append",
                  second_refusal == "RELATION_PROMOTION_NOT_DEEPER")
            check("zero_counts_delta", counts(session) == baseline_counts)
            check("world_events_perceptions_checkpoints_unchanged",
                  session.world().snapshot() == baseline_world
                  and session.events() == baseline_events
                  and session.product.store.perceptions(session.branch_id)
                  == baseline_perceptions
                  and session.product.store.checkpoints(session.branch_id)
                  == baseline_checkpoints)
            check("relation_episodes_unchanged",
                  session.product.store.episodes(session.branch_id)
                  == baseline_episodes)
            check("history_and_context_byte_exact",
                  read_relation_history(
                      session, P_ID, as_of_clock=event_clock) == history
                  and read_actor_relative_context(
                      session, P_ID, event_id) == context)
            check("c12_verify_ok",
                  session.product.store.verify(session.branch_id)["ok"])
            retry_again = promote_relation(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, depth=2, clock=first["clock"],
                operation_id="closure:promote:1")
            check("original_retry_after_refusal_unchanged",
                  retry_again["status"] == "UNCHANGED"
                  and retry_again["primary_episode_id"]
                  == first["primary_episode_id"]
                  and counts(session) == baseline_counts)
            report.update({
                "first_promotion": {
                    "status": first["status"],
                    "representation_depth": first["representation_depth"],
                    "primary_episode_id": first["primary_episode_id"],
                },
                "history": history,
                "context": context,
                "second_refusal": second_refusal,
                "baseline_counts": baseline_counts,
                "after_counts": counts(session),
                "checks": checks,
                "passed": all(row["pass"] for row in checks),
            })
        finally:
            owner.close()
    finally:
        fanin.close()
    path = EVIDENCE / "c05_closure_report.json"
    path.write_text(json.dumps(report, indent=2, sort_keys=True))
    print(json.dumps({
        "passed": report.get("passed"),
        "second_refusal": report.get("second_refusal"),
        "baseline_counts": report.get("baseline_counts"),
        "after_counts": report.get("after_counts"),
        "failed": [row["name"] for row in checks if not row["pass"]],
        "report": str(path),
    }, indent=2, sort_keys=True))
    return 0 if report.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
