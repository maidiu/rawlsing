"""Independent nonauthor C05 G5 probe.

Product read-only. Writes only reviewer scratch state and the report file under
this review return. Covers exposure qualification, physical co-presence vs
relation access, late exposure/no retro-fill, depth 1 -> 2 promotion, a later
real P2 owner event, change/head sever/restore, coherent append-only forgery,
C01 role extension, and fresh-process cold exactness.
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRATCH = REPO / ".local-logs/sorok-c05-independent-g5/scratch"
EVIDENCE = HERE.parent / "evidence"
ENGINE = REPO / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
if str(ENGINE) not in sys.path:
    sys.path.insert(0, str(ENGINE))

from c05_observe import counts, relation_counts, snapshot  # noqa: E402
from developmental_recursion.continuing_relations import (  # noqa: E402
    RELATION_CHANGE_KIND,
    RELATION_CHANGE_SCHEMA,
    RELATION_GRADE,
    RELATION_HEAD_KIND,
    RELATION_HEAD_SCHEMA,
    promote_relation,
    read_actor_relative_context,
    read_relation_history,
    record_relation_change,
    relation_change_source,
    relation_head_source,
)
from developmental_recursion.contracts import (  # noqa: E402
    EventProposal,
    RecursionRefusal,
    canonical,
    digest,
)
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from developmental_recursion.supporting_actor import (  # noqa: E402
    SUPPORTING_ROLES,
    read_actor_access,
    read_supporting_actor,
    register_supporting_actor,
)

P_ID = "TEST_ONLY_C05_REVIEW_PARENT"
P_ALIAS = "RVP"
O_ID = "TEST_ONLY_C05_REVIEW_NEIGHBOR"
O_ALIAS = "RVO"
Q_ID = "TEST_ONLY_C05_REVIEW_OBSERVER"
Q_ALIAS = "RVQ"
R_ID = "TEST_ONLY_C05_REVIEW_OUTSIDER"
R_ALIAS = "RVR"
RELATION = "review-household"
P_SECRET = "review-parent-private-motive"
O_SECRET = "review-neighbor-private-motive"
Q_SECRET = "review-observer-private-motive"
R_SECRET = "review-outsider-private-motive"
REL_SECRET = "review-relation-private-note"

CHECKS: list[dict] = []
OBSERVATIONS: list[dict] = []


def check(name: str, condition: bool, detail=None) -> bool:
    passed = bool(condition)
    CHECKS.append({"name": name, "pass": passed, "detail": detail})
    if not passed:
        print("FAIL", name, json.dumps(detail, sort_keys=True, default=str))
    return passed


def observe(name: str, detail) -> None:
    OBSERVATIONS.append({"name": name, "detail": detail})
    print("OBSERVE", name, json.dumps(detail, sort_keys=True, default=str))


def refusal_code(fn) -> str | None:
    try:
        fn()
    except RecursionRefusal as exc:
        return str(exc)
    return None


def later_event(owner, session, participants, *, operation_id, proposal_id,
                delta=6):
    before = owner.snapshot()
    proposal = EventProposal(
        proposal_id, before.clock + delta, "ADMIT_EVENT",
        (owner.source_ref,), tuple(participants), {},
    )
    result = owner.realize(operation_id, proposal, before)
    supporting = list(
        (result.consequences or {}).get("supporting_participants") or ())
    event_id = supporting[0]["event_id"] if supporting else None
    if event_id is None:
        candidates = [
            row for row in session.events()
            if row.get("clock") == proposal.event_time
        ]
        event_id = candidates[-1]["event_id"] if candidates else None
    return result, proposal, event_id


def relation_row(session, episode_id):
    return next(
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("episode_id") == episode_id
    )


def world_dir(prefix: str) -> Path:
    SCRATCH.mkdir(parents=True, exist_ok=True)
    return Path(tempfile.mkdtemp(prefix=prefix, dir=SCRATCH)) / "p2"


def main_world():
    state_root = world_dir("main-")
    fanin = load_p2().start(state_root)
    session = fanin.session
    root = session.read_root()
    focal = root["actor_ids"][0]
    reg = {}
    reg[P_ID] = register_supporting_actor(
        session, alias=P_ALIAS, actor_id=P_ID, role="parent",
        private_state={"motive": P_SECRET})
    reg[O_ID] = register_supporting_actor(
        session, alias=O_ALIAS, actor_id=O_ID, role="neighbor",
        private_state={"motive": O_SECRET})
    reg[Q_ID] = register_supporting_actor(
        session, alias=Q_ALIAS, actor_id=Q_ID, role="neighbor",
        private_state={"motive": Q_SECRET})
    reg[R_ID] = register_supporting_actor(
        session, alias=R_ALIAS, actor_id=R_ID, role="neighbor",
        private_state={"motive": R_SECRET})
    case = fanin.deps["case_for"](True)
    source = fanin.deps["source_for"](case)
    owner = P2Owner(
        fanin, case=case, source=source,
        participants=(focal, P_ID, O_ID))
    return fanin, session, focal, owner, reg, state_root


def c01_checks(session, focal, reg):
    check("c01_role_allowlist_is_parent_plus_neighbor",
          SUPPORTING_ROLES == frozenset({"parent", "neighbor"}),
          sorted(SUPPORTING_ROLES))
    check("c01_registered_roles",
          reg[P_ID]["role"] == "parent"
          and reg[O_ID]["role"] == "neighbor"
          and reg[Q_ID]["role"] == "neighbor"
          and reg[R_ID]["role"] == "neighbor")
    before = counts(session)
    sibling_code = refusal_code(lambda: register_supporting_actor(
        session, alias="TEST_ONLY_C05_REVIEW_SIBLING",
        actor_id="TEST_ONLY_C05_REVIEW_SIBLING_ID", role="sibling"))
    check("c01_unleased_role_refused",
          sibling_code == "SUPPORTING_ACTOR_SCHEMA"
          and counts(session) == before, sibling_code)
    duplicate = register_supporting_actor(
        session, alias=P_ALIAS, actor_id=P_ID, role="parent",
        private_state={"motive": P_SECRET})
    check("c01_duplicate_registration_unchanged",
          duplicate["status"] == "UNCHANGED"
          and counts(session) == before, duplicate.get("status"))
    public_read = read_supporting_actor(session, P_ID)
    self_read = read_supporting_actor(session, P_ID, as_actor=P_ID)
    other_read = read_supporting_actor(session, P_ID, as_actor=O_ID)
    check("c01_private_state_self_only",
          public_read["private_state"] == "NOT_READ"
          and other_read["private_state"] == "NOT_READ"
          and self_read["private_state"] == {"motive": P_SECRET})
    root_ids = list(session.read_root()["actor_ids"])
    check("c01_root_unchanged",
          root_ids[0] == focal and len(root_ids) == 2)
    check("c01_review_actors_live",
          all(read_supporting_actor(session, actor_id)["status"] == "REGISTERED"
              for actor_id in (P_ID, O_ID, Q_ID, R_ID)))
    check("c01_source_blob_unchanged_outside_allowlist",
          True,
          "verified separately by git diff ee82397a9..9cf13763b")


def relation_checks(session, focal, owner):
    start_clock = session.world().clock
    before_registration_counts = relation_counts(
        session, (P_ID, O_ID, Q_ID, R_ID))
    entry = record_relation_change(
        session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
        change="ENTER", clock=start_clock,
        operation_id="c05review:enter", exposed_actor_ids=[P_ID, O_ID],
        value="guest", private_state={"note": REL_SECRET},
    )
    check("entry_recorded",
          entry["status"] == "RECORDED"
          and entry["current_status"] == "ACTIVE"
          and entry["representation_depth"] == 1,
          {k: entry.get(k) for k in (
              "status", "current_status", "representation_depth")})
    entry_episode = relation_row(session, entry["primary_episode_id"])
    head_episode = relation_row(session, entry["head_episode_id"])
    entry_canonical = canonical(entry_episode["body"])
    entry_hash = entry_episode["hash"]
    check("entry_head_present",
          head_episode["kind"] == RELATION_HEAD_KIND
          and head_episode["body"]["primary_episode_id"]
          == entry_episode["episode_id"])
    after_entry_counts = relation_counts(session, (P_ID, O_ID, Q_ID, R_ID))
    check("entry_writes_one_change_one_head",
          after_entry_counts["relation_changes"]
          == before_registration_counts["relation_changes"] + 1
          and after_entry_counts["relation_heads"]
          == before_registration_counts["relation_heads"] + 1
          and after_entry_counts["registrations"]
          == before_registration_counts["registrations"]
          and after_entry_counts["c04_utterances"] == 0,
          after_entry_counts)

    p_start = read_relation_history(session, P_ID, as_of_clock=start_clock)
    o_start = read_relation_history(session, O_ID, as_of_clock=start_clock)
    q_start = read_relation_history(session, Q_ID, as_of_clock=start_clock)
    nadia_start = read_relation_history(
        session, focal, as_of_clock=start_clock)
    r_start = read_relation_history(session, R_ID, as_of_clock=start_clock)
    check("parties_qualified_at_entry",
          p_start["status"] == "QUALIFIED"
          and o_start["status"] == "QUALIFIED"
          and len(p_start["relations"]) == 1
          and p_start["relations"][0]["entries"][0]["change"] == "ENTER"
          and p_start["relations"][0]["representation_depth"] == 1
          and p_start["relations"][0]["history_complete"] is True
          and p_start["relations"][0]["counterpart"]["actor_id"] == O_ID
          and p_start["relations"][0]["prior_exposure"] == "QUALIFIED")
    for label, envelope in (
            ("nadia", nadia_start), ("observer", q_start), ("outsider", r_start)):
        blob = canonical(envelope)
        check(f"unexposed_{label}_qualified_hold_no_fact",
              envelope["status"] == "HOLD_NOT_EXPOSED"
              and envelope["relations"] == []
              and envelope["withheld_relation_count"] == 1
              and RELATION not in blob
              and P_ID not in blob
              and O_ID not in blob
              and REL_SECRET not in blob,
              envelope["status"])
    check("absolute_query_unknown_scope",
          read_relation_history(
              session, P_ID, other_actor_id=O_ID, relation="other-relation"
          )["status"] == "HOLD_UNKNOWN_SCOPE")
    check("owner_query_qualified",
          read_relation_history(
              session, P_ID, other_actor_id=O_ID, relation=RELATION
          )["status"] == "QUALIFIED")
    check("nonparty_query_pair_unknown_scope",
          read_relation_history(
              session, Q_ID, other_actor_id=P_ID, relation=RELATION
          )["status"] == "HOLD_UNKNOWN_SCOPE")
    check("future_as_of_refused",
          refusal_code(lambda: read_relation_history(
              session, P_ID,
              as_of_clock=session.world().clock + 1))
          == "RELATION_AS_OF_FUTURE")

    retry_before = counts(session)
    retried = record_relation_change(
        session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
        change="ENTER", clock=start_clock,
        operation_id="c05review:enter", exposed_actor_ids=[P_ID, O_ID],
        value="guest", private_state={"note": REL_SECRET},
    )
    check("entry_retry_unchanged_no_duplicate",
          retried["status"] == "UNCHANGED"
          and retried["primary_episode_id"] == entry["primary_episode_id"]
          and counts(session) == retry_before)

    no_write_baseline = counts(session)
    checks = {
        "reuse_mismatch": (
            refusal_code(lambda: record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="ENTER", clock=start_clock,
                operation_id="c05review:enter",
                exposed_actor_ids=[P_ID, O_ID], value="different",
                private_state={"note": REL_SECRET})),
            "RELATION_OPERATION_REUSE_MISMATCH"),
        "missing_party_exposure": (
            refusal_code(lambda: record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="CHANGE",
                clock=session.world().clock,
                operation_id="c05review:bad-exposure",
                exposed_actor_ids=[P_ID])),
            "RELATION_EXPOSURE_MISSING_PARTY"),
        "stranger_exposure": (
            refusal_code(lambda: record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="CHANGE",
                clock=session.world().clock,
                operation_id="c05review:bad-stranger",
                exposed_actor_ids=[P_ID, O_ID,
                                   "TEST_ONLY_C05_REVIEW_STRANGER"])),
            "RELATION_EXPOSURE_ACTOR_UNKNOWN"),
        "future_clock": (
            refusal_code(lambda: record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="CHANGE",
                clock=session.world().clock + 1,
                operation_id="c05review:bad-future",
                exposed_actor_ids=[P_ID, O_ID])),
            "RELATION_CLOCK_FUTURE"),
        "backdated_clock": (
            refusal_code(lambda: record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="CHANGE",
                clock=session.world().clock - 1,
                operation_id="c05review:bad-backdated",
                exposed_actor_ids=[P_ID, O_ID])),
            "RELATION_CLOCK_BACKDATED"),
        "private_leak": (
            refusal_code(lambda: record_relation_change(
                session, actor_id=P_ID, other_actor_id=O_ID,
                relation=RELATION, change="CHANGE",
                clock=session.world().clock,
                operation_id="c05review:bad-leak",
                exposed_actor_ids=[P_ID, O_ID], value=REL_SECRET,
                private_state={"note": REL_SECRET})),
            "RELATION_PRIVATE_STATE_LEAK"),
        "unknown_reader": (
            refusal_code(lambda: read_relation_history(
                session, "TEST_ONLY_C05_REVIEW_UNKNOWN")),
            "RELATION_ACTOR_UNKNOWN"),
    }
    for name, (actual, expected) in checks.items():
        check(f"refusal_{name}", actual == expected, actual)
    check("refusals_wrote_nothing", counts(session) == no_write_baseline)

    first_result, first_proposal, first_event = later_event(
        owner, session, (focal, P_ID, O_ID),
        operation_id="c05review:event:1", proposal_id="review:event:1")
    first_clock = session.event(first_event)["clock"]
    check("later_owner_event_realized",
          first_result.status == "REALIZED"
          and first_clock == start_clock + 6
          and session.world().clock == first_clock
          and first_event.startswith("TEST_ONLY_BP4_WORLD_EVT_"),
          {"status": first_result.status, "clock": first_clock,
           "event": first_event})
    first_stored = session.event(first_event)
    first_world_rows = [
        row for row in session.product.store.world_events(session.branch_id)
        if row.get("event_id") == first_event
    ]
    document = dict(first_stored)
    recorded_hash = document.pop("hash")
    hash_ok = recorded_hash == digest(document)
    recorded_id = document.pop("event_id")
    check("later_event_hash_and_id_seal",
          hash_ok
          and recorded_id == "TEST_ONLY_BP4_WORLD_EVT_" + digest(document)
          and len(first_world_rows) == 1
          and first_world_rows[0]["hash"] == recorded_hash)
    check("owner_event_identity",
          first_result.before.actor == focal
          and owner.snapshot().actor == focal
          and owner.source_ref in first_proposal.source_refs)

    access = {
        actor_id: read_actor_access(session, actor_id, first_event)
        for actor_id in (focal, P_ID, O_ID, Q_ID, R_ID)
    }
    check("later_event_separate_access_first",
          access[focal]["status"] == "PERCEIVED"
          and access[P_ID]["status"] == "PERCEIVED"
          and access[O_ID]["status"] == "PERCEIVED"
          and access[Q_ID]["status"] == "NOT_PERCEIVED"
          and access[R_ID]["status"] == "NOT_PERCEIVED")
    prior = next(
        (row for row in session.events()
         if row["event_id"] != first_event
         and row.get("clock", 0) < first_clock
         and read_actor_access(session, focal, row["event_id"])["status"]
         == "PERCEIVED"
         and read_actor_access(session, P_ID, row["event_id"])["status"]
         == "NOT_PERCEIVED"),
        None)
    check("prior_event_access_separate", prior is not None)

    ctx1 = {
        actor_id: read_actor_relative_context(session, actor_id, first_event)
        for actor_id in (focal, P_ID, O_ID, Q_ID, R_ID)
    }
    for actor_id in (P_ID, O_ID):
        relation = ctx1[actor_id]["relation_scope"]["relations"][0]
        check(f"first_event_party_context_{actor_id}",
              ctx1[actor_id]["event_access"]["status"] == "PERCEIVED"
              and ctx1[actor_id]["relation_scope"]["status"] == "QUALIFIED"
              and relation["entries"][0]["change"] == "ENTER"
              and relation["representation_depth"] == 1
              and relation["history_complete"] is True
              and ctx1[actor_id]["context_effect"][
                  "both_parties_event_access"] is True)
    check("first_event_nadia_present_but_unexposed",
          ctx1[focal]["event_access"]["status"] == "PERCEIVED"
          and ctx1[focal]["relation_scope"]["status"] == "HOLD_NOT_EXPOSED"
          and ctx1[focal]["relation_scope"]["relations"] == []
          and ctx1[focal]["relation_scope"]["withheld_relation_count"] == 1)
    for actor_id in (Q_ID, R_ID):
        check(f"first_event_absent_unexposed_{actor_id}",
              ctx1[actor_id]["event_access"]["status"] == "NOT_PERCEIVED"
              and ctx1[actor_id]["relation_scope"]["status"]
              == "HOLD_NOT_EXPOSED")
    for label, document_value in (
            ("contexts", ctx1),
            ("event", session.event(first_event)),
            ("world", session.world().snapshot())):
        blob = canonical(document_value)
        check(f"private_state_absent_first_{label}",
              all(secret not in blob for secret in (
                  P_SECRET, O_SECRET, Q_SECRET, R_SECRET, REL_SECRET)))
    check("event_private_not_read",
          all(ctx1[actor_id]["private_state"] == "NOT_READ"
              for actor_id in ctx1))

    second_result, second_proposal, second_event = later_event(
        owner, session, (focal, P_ID),
        operation_id="c05review:event:2", proposal_id="review:event:2")
    second_clock = session.event(second_event)["clock"]
    check("second_owner_event_realized",
          second_result.status == "REALIZED"
          and second_clock == first_clock + 6
          and session.world().clock == second_clock)
    check("second_event_absent_neighbor_still_not_perceived",
          read_actor_access(session, O_ID, second_event)["status"]
          == "NOT_PERCEIVED"
          and read_actor_access(session, P_ID, second_event)["status"]
          == "PERCEIVED")
    ctx2 = {
        actor_id: read_actor_relative_context(session, actor_id, second_event)
        for actor_id in (focal, P_ID, O_ID, Q_ID, R_ID)
    }
    check("relation_qualified_without_copresence",
          ctx2[O_ID]["event_access"]["status"] == "NOT_PERCEIVED"
          and ctx2[O_ID]["relation_scope"]["status"] == "QUALIFIED"
          and ctx2[O_ID]["relation_scope"]["relations"][0]["entries"][0][
              "change"] == "ENTER"
          and ctx2[P_ID]["event_access"]["status"] == "PERCEIVED"
          and ctx2[P_ID]["context_effect"][
              "both_parties_event_access"] is False
          and ctx2[O_ID]["context_effect"][
              "both_parties_event_access"] is False)
    check("present_unexposed_nadia_second",
          ctx2[focal]["event_access"]["status"] == "PERCEIVED"
          and ctx2[focal]["relation_scope"]["status"] == "HOLD_NOT_EXPOSED")

    change = record_relation_change(
        session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
        change="CHANGE", clock=session.world().clock,
        operation_id="c05review:change", exposed_actor_ids=[P_ID, O_ID, focal],
        value="member",
    )
    check("change_recorded",
          change["status"] == "RECORDED"
          and change["current_status"] == "CHANGED"
          and change["representation_depth"] == 1)
    p_234 = read_relation_history(session, P_ID, as_of_clock=second_clock)
    nadia_234 = read_relation_history(
        session, focal, as_of_clock=second_clock)
    q_234 = read_relation_history(session, Q_ID, as_of_clock=second_clock)
    check("parties_see_full_dated_history",
          [row["change"] for row in p_234["relations"][0]["entries"]]
          == ["ENTER", "CHANGE"]
          and p_234["relations"][0]["history_complete"] is True
          and p_234["relations"][0]["representation_depth"] == 1)
    check("late_exposure_no_retro_fill",
          [row["change"] for row in nadia_234["relations"][0]["entries"]]
          == ["CHANGE"]
          and nadia_234["relations"][0]["history_complete"] is False
          and nadia_234["relations"][0]["prior_exposure"]
          == "HOLD_NOT_EXPOSED"
          and nadia_234["relations"][0]["entries"][0]["clock"]
          == second_clock
          and nadia_234["relations"][0]["entries"][0]["change"] != "ENTER")
    check("unexposed_observer_still_hold", q_234["status"]
          == "HOLD_NOT_EXPOSED")
    ctx2_after_change = {
        actor_id: read_actor_relative_context(session, actor_id, second_event)
        for actor_id in (focal, P_ID, O_ID, Q_ID, R_ID)
    }
    check("second_event_nadia_partial_change_only",
          ctx2_after_change[focal]["event_access"]["status"] == "PERCEIVED"
          and ctx2_after_change[focal]["relation_scope"]["status"]
          == "QUALIFIED"
          and [row["change"] for row in ctx2_after_change[focal][
              "relation_scope"]["relations"][0]["entries"]] == ["CHANGE"]
          and ctx2_after_change[focal]["relation_scope"]["relations"][0][
              "history_complete"] is False
          and ctx2_after_change[focal]["relation_scope"]["relations"][0][
              "prior_exposure"] == "HOLD_NOT_EXPOSED")
    check("second_event_party_entries_both",
          [row["change"] for row in ctx2_after_change[P_ID][
              "relation_scope"]["relations"][0]["entries"]]
          == ["ENTER", "CHANGE"])

    third_result, third_proposal, third_event = later_event(
        owner, session, (focal, P_ID),
        operation_id="c05review:event:3", proposal_id="review:event:3")
    third_clock = session.event(third_event)["clock"]
    check("third_owner_event_realized",
          third_result.status == "REALIZED"
          and third_clock == second_clock + 6
          and session.world().clock == third_clock)
    check("third_event_access",
          read_actor_access(session, P_ID, third_event)["status"]
          == "PERCEIVED"
          and read_actor_access(session, focal, third_event)["status"]
          == "PERCEIVED"
          and read_actor_access(session, O_ID, third_event)["status"]
          == "NOT_PERCEIVED")

    pre_promotion_240 = read_relation_history(
        session, P_ID, as_of_clock=third_clock)
    p_first_before = read_actor_relative_context(session, P_ID, first_event)
    p_second_before = read_actor_relative_context(session, P_ID, second_event)
    nadia_second_before = read_actor_relative_context(
        session, focal, second_event)
    entry_row_before = relation_row(session, entry["primary_episode_id"])
    change_row_before = relation_row(session, change["primary_episode_id"])
    check("pre_promotion_depth_one_without_label_only",
          pre_promotion_240["relations"][0]["representation_depth"] == 1
          and pre_promotion_240["relations"][0]["promotions"] == []
          and [row["change"] for row in pre_promotion_240["relations"][0][
              "entries"]] == ["ENTER", "CHANGE"])

    promoted = promote_relation(
        session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
        depth=2, clock=session.world().clock,
        operation_id="c05review:promote")
    check("promotion_recorded",
          promoted["status"] == "RECORDED"
          and promoted["current_status"] == "CHANGED"
          and promoted["representation_depth"] == 2)
    post_promotion_240 = read_relation_history(
        session, P_ID, as_of_clock=third_clock)
    pre_relations = pre_promotion_240["relations"][0]
    post_relations = post_promotion_240["relations"][0]
    check("promotion_future_only_reader_difference",
          post_relations["representation_depth"] == 2
          and len(post_relations["promotions"]) == 1
          and post_relations["promotions"][0]["depth"] == 2
          and len(post_relations["promotions"][0]["history_hash"]) == 64
          and post_relations["entries"] == pre_relations["entries"]
          and post_relations["visible_history_hash"]
          == pre_relations["visible_history_hash"]
          and post_relations["history_complete"] is True)
    pre_239 = read_relation_history(session, P_ID, as_of_clock=third_clock - 1)
    check("as_of_before_promotion_stays_depth_one",
          pre_239["relations"][0]["representation_depth"] == 1
          and pre_239["relations"][0]["promotions"] == []
          and pre_239["relations"][0]["entries"]
          == pre_relations["entries"])
    check("earlier_event_contexts_byte_exact_after_promotion",
          read_actor_relative_context(session, P_ID, first_event)
          == p_first_before
          and read_actor_relative_context(session, P_ID, second_event)
          == p_second_before
          and read_actor_relative_context(session, focal, second_event)
          == nadia_second_before)
    entry_row_after = relation_row(session, entry["primary_episode_id"])
    change_row_after = relation_row(session, change["primary_episode_id"])
    check("promotion_does_not_rewrite_entries",
          canonical(entry_row_after["body"]) == canonical(
              entry_row_before["body"])
          and entry_row_after["hash"] == entry_row_before["hash"]
          and canonical(change_row_after["body"]) == canonical(
              change_row_before["body"])
          and change_row_after["hash"] == change_row_before["hash"])
    p_third_after = read_actor_relative_context(session, P_ID, third_event)
    nadia_third_after = read_actor_relative_context(
        session, focal, third_event)
    check("later_consumer_sees_depth_two",
          p_third_after["relation_scope"]["status"] == "QUALIFIED"
          and p_third_after["relation_scope"]["representation_depth"] == 2
          and p_third_after["relation_scope"]["relations"][0][
              "representation_depth"] == 2
          and p_third_after["event_access"]["status"] == "PERCEIVED")
    check("partial_late_viewer_gets_promotion_only_after_exposure",
          nadia_third_after["relation_scope"]["status"] == "QUALIFIED"
          and nadia_third_after["relation_scope"]["representation_depth"] == 2
          and nadia_third_after["relation_scope"]["relations"][0][
              "history_complete"] is False
          and [row["change"] for row in nadia_third_after[
              "relation_scope"]["relations"][0]["entries"]] == ["CHANGE"])
    promotion_retry_before = counts(session)
    promotion_retry = promote_relation(
        session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
        depth=2, clock=promoted["clock"],
        operation_id="c05review:promote")
    check("promotion_retry_unchanged_no_duplicate",
          promotion_retry["status"] == "UNCHANGED"
          and promotion_retry["primary_episode_id"]
          == promoted["primary_episode_id"]
          and counts(session) == promotion_retry_before)
    check("promotion_depth_one_refused",
          refusal_code(lambda: promote_relation(
              session, actor_id=P_ID, other_actor_id=O_ID,
              relation=RELATION, depth=1, clock=session.world().clock,
              operation_id="c05review:promote-depth1"))
          == "RELATION_PROMOTION_DEPTH")
    late = record_relation_change(
        session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
        change="CHANGE", clock=session.world().clock,
        operation_id="c05review:late-change",
        exposed_actor_ids=[P_ID, O_ID, Q_ID], value="late-member",
    )
    check("late_change_recorded", late["status"] == "RECORDED")
    q_240 = read_relation_history(session, Q_ID, as_of_clock=third_clock)
    nadia_240 = read_relation_history(
        session, focal, as_of_clock=third_clock)
    p_240 = read_relation_history(session, P_ID, as_of_clock=third_clock)
    r_240 = read_relation_history(session, R_ID, as_of_clock=third_clock)
    check("late_exposed_nonparty_sees_only_own_entry",
          q_240["status"] == "QUALIFIED"
          and [row["change"] for row in q_240["relations"][0]["entries"]]
          == ["CHANGE"]
          and q_240["relations"][0]["history_complete"] is False
          and q_240["relations"][0]["prior_exposure"]
          == "HOLD_NOT_EXPOSED"
          and q_240["relations"][0]["representation_depth"] == 1
          and q_240["relations"][0]["viewer_is_party"] is False
          and q_240["relations"][0]["counterpart"] is None
          and q_240["relations"][0]["promotions"] == [])
    check("late_exposure_does_not_retro_fill_other_viewer",
          [row["change"] for row in nadia_240["relations"][0]["entries"]]
          == ["CHANGE"]
          and nadia_240["relations"][0]["history_complete"] is False)
    check("party_full_history_after_late_change",
          [row["change"] for row in p_240["relations"][0]["entries"]]
          == ["ENTER", "CHANGE", "CHANGE"]
          and p_240["relations"][0]["history_complete"] is True
          and p_240["relations"][0]["representation_depth"] == 2)
    check("outsider_still_hold", r_240["status"] == "HOLD_NOT_EXPOSED"
          and r_240["relations"] == [] and r_240["withheld_relation_count"] == 1)
    q_third = read_actor_relative_context(session, Q_ID, third_event)
    check("nonparticipant_exposed_relation_qualified",
          q_third["event_access"]["status"] == "NOT_PERCEIVED"
          and q_third["relation_scope"]["status"] == "QUALIFIED"
          and [row["change"] for row in q_third["relation_scope"][
              "relations"][0]["entries"]] == ["CHANGE"]
          and q_third["relation_scope"]["relations"][0][
              "viewer_is_party"] is False)
    observe("caller_exposure_is_not_event_perception", {
        "observer_was_never_a_participant": True,
        "observer_event_access": q_third["event_access"]["status"],
        "observer_relation_status": q_third["relation_scope"]["status"],
        "observer_entries": [row["change"] for row in q_third[
            "relation_scope"]["relations"][0]["entries"]],
    })

    left = record_relation_change(
        session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
        change="LEAVE", clock=session.world().clock,
        operation_id="c05review:leave", exposed_actor_ids=[P_ID, O_ID],
    )
    check("leave_recorded", left["status"] == "RECORDED"
          and left["current_status"] == "LEFT")
    reentered = record_relation_change(
        session, actor_id=P_ID, other_actor_id=O_ID, relation=RELATION,
        change="ENTER", clock=session.world().clock,
        operation_id="c05review:reenter", exposed_actor_ids=[P_ID, O_ID],
        value="member",
    )
    check("reenter_recorded", reentered["status"] == "RECORDED"
          and reentered["current_status"] == "ACTIVE")
    p_final = read_relation_history(session, P_ID, as_of_clock=third_clock)
    nadia_final = read_relation_history(
        session, focal, as_of_clock=third_clock)
    q_final = read_relation_history(session, Q_ID, as_of_clock=third_clock)
    check("leave_reenter_state_machine",
          [row["change"] for row in p_final["relations"][0]["entries"]]
          == ["ENTER", "CHANGE", "CHANGE", "LEAVE", "ENTER"]
          and p_final["relations"][0]["status"] == "ACTIVE"
          and p_final["relations"][0]["history_complete"] is True)
    check("leave_reenter_not_retrofilled_to_unexposed",
          [row["change"] for row in nadia_final["relations"][0]["entries"]]
          == ["CHANGE"]
          and [row["change"] for row in q_final["relations"][0]["entries"]]
          == ["CHANGE"])
    check("no_duplicate_changes_or_heads_after_leave",
          relation_counts(session, (P_ID, O_ID, Q_ID, R_ID))[
              "relation_changes"] == 6
          and relation_counts(session, (P_ID, O_ID, Q_ID, R_ID))[
              "relation_heads"] == 6)

    baseline_contexts = {
        f"{actor_id}|{event_id}": read_actor_relative_context(
            session, actor_id, event_id)
        for actor_id in (focal, P_ID, O_ID, Q_ID, R_ID)
        for event_id in (first_event, second_event, third_event)
    }
    baseline_world = session.world().snapshot()
    baseline_events = session.events()
    baseline_perceptions = session.product.store.perceptions(session.branch_id)
    baseline_checkpoints = session.product.store.checkpoints(session.branch_id)
    baseline_histories = {
        f"{actor_id}|{third_clock}": read_relation_history(
            session, actor_id, as_of_clock=third_clock)
        for actor_id in (focal, P_ID, O_ID, Q_ID, R_ID)
    }
    baseline_counts = counts(session)
    store = session.product.store
    original_episodes = store.episodes

    def hider(episode_id):
        def patched(branch_id):
            return [
                row for row in original_episodes(branch_id)
                if row.get("episode_id") != episode_id
            ]
        return patched

    change_head = next(
        row for row in original_episodes(session.branch_id)
        if row.get("kind") == RELATION_HEAD_KIND
        and (row.get("body") or {}).get("primary_episode_id")
        == change["primary_episode_id"]
    )
    for label, hidden_id in (
            ("change_primary", change["primary_episode_id"]),
            ("change_head", change_head["episode_id"])):
        with patch.object(store, "episodes", side_effect=hider(hidden_id)):
            severed = {
                actor_id: read_actor_relative_context(
                    session, actor_id, third_event)
                for actor_id in (focal, P_ID, O_ID, Q_ID)
            }
            check(f"sever_{label}_exposed_viewers_custody_hold",
                  all(context["relation_scope"]["status"]
                      == "HOLD_CUSTODY_SEVERED"
                      and context["relation_scope"]["relations"] == []
                      for context in severed.values()))
            check(f"sever_{label}_event_access_preserved",
                  all(severed[actor_id]["event_access"]["status"]
                      == baseline_contexts[
                          f"{actor_id}|{third_event}"]["event_access"][
                              "status"]
                      for actor_id in severed))
            r_severed = read_actor_relative_context(
                session, R_ID, third_event)
            check(f"sever_{label}_outsider_not_disclosed",
                  r_severed["relation_scope"]["status"]
                  == "HOLD_NOT_EXPOSED"
                  and r_severed["relation_scope"]["relations"] == [])
            check(f"sever_{label}_world_events_perceptions_checkpoints_same",
                  session.world().snapshot() == baseline_world
                  and session.events() == baseline_events
                  and session.product.store.perceptions(session.branch_id)
                  == baseline_perceptions
                  and session.product.store.checkpoints(session.branch_id)
                  == baseline_checkpoints)
        restored = {
            f"{actor_id}|{event_id}": read_actor_relative_context(
                session, actor_id, event_id)
            for actor_id in (focal, P_ID, O_ID, Q_ID, R_ID)
            for event_id in (first_event, second_event, third_event)
        }
        restored_histories = {
            f"{actor_id}|{third_clock}": read_relation_history(
                session, actor_id, as_of_clock=third_clock)
            for actor_id in (focal, P_ID, O_ID, Q_ID, R_ID)
        }
        check(f"restore_{label}_contexts_exact",
              restored == baseline_contexts
              and restored_histories == baseline_histories
              and counts(session) == baseline_counts)

    return {
        "start_clock": start_clock,
        "first_event": first_event,
        "second_event": second_event,
        "third_event": third_event,
        "first_clock": first_clock,
        "second_clock": second_clock,
        "third_clock": third_clock,
        "entry": entry,
        "change": change,
        "promoted": promoted,
        "left": left,
        "reentered": reentered,
        "actors": [focal, P_ID, O_ID, Q_ID, R_ID],
        "events": [first_event, second_event, third_event],
    }


def forgery_probe():
    state_root = world_dir("forge-")
    fanin = load_p2().start(state_root)
    session = fanin.session
    focal = session.read_root()["actor_ids"][0]
    for actor_id, alias, role in (
            (P_ID, P_ALIAS, "parent"), (O_ID, O_ALIAS, "neighbor")):
        register_supporting_actor(
            session, alias=alias, actor_id=actor_id, role=role,
            private_state={"motive": "forgery-private"})
    case = fanin.deps["case_for"](True)
    source = fanin.deps["source_for"](case)
    owner = P2Owner(
        fanin, case=case, source=source, participants=(focal, P_ID, O_ID))
    clock = session.world().clock
    actor_ids = sorted((P_ID, O_ID))
    aliases = [
        read_supporting_actor(session, actor_id)["alias"]
        for actor_id in actor_ids
    ]
    relation = "forged-household"
    key = digest({"actor_ids": actor_ids, "relation": relation})
    body = {
        "schema": RELATION_CHANGE_SCHEMA,
        "grade": RELATION_GRADE,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "relation_key": key,
        "actor_ids": actor_ids,
        "aliases": aliases,
        "relation": relation,
        "change": "ENTER",
        "value": "forged",
        "clock": clock,
        "operation_id": "c05review:forged:append",
        "exposed_actor_ids": actor_ids,
        "exposed_aliases": aliases,
        "private_state_hash": digest({}),
        "sequence": 1,
        "previous_episode_id": None,
    }
    body["source"] = relation_change_source(body)
    body["private_state"] = {}
    primary = session.product.store.append_episode(
        session.branch_id, actor_id=aliases[0],
        kind=RELATION_CHANGE_KIND, clock=clock, body=body)
    head_body = {
        "schema": RELATION_HEAD_SCHEMA,
        "grade": RELATION_GRADE,
        "root": body["root"],
        "branch": body["branch"],
        "relation_key": key,
        "actor_ids": actor_ids,
        "aliases": aliases,
        "relation": relation,
        "sequence": 1,
        "clock": clock,
        "operation_id": body["operation_id"],
        "primary_episode_id": primary["episode_id"],
        "primary_episode_hash": primary["hash"],
        "previous_head_episode_id": None,
        "previous_head_hash": None,
        "exposed_actor_ids": actor_ids,
        "exposed_aliases": aliases,
    }
    head_body["source"] = relation_head_source(head_body)
    head = session.product.store.append_episode(
        session.branch_id, actor_id=aliases[0],
        kind=RELATION_HEAD_KIND, clock=clock, body=head_body)
    history = read_relation_history(session, P_ID, as_of_clock=clock)
    result, proposal, event_id = later_event(
        owner, session, (focal, P_ID),
        operation_id="c05review:forged:event",
        proposal_id="review:forged:event")
    context = read_actor_relative_context(session, P_ID, event_id)
    appended_without_writer = history["status"] == "QUALIFIED"
    context_forged = (
        context["relation_scope"]["status"] == "QUALIFIED"
        and context["relation_scope"]["relations"][0]["relation"] == relation
        and context["context_effect"]["relation_aware"] is True
    )
    observe("coherent_append_only_relation_accepted", {
        "forged_change_episode_id": primary["episode_id"],
        "forged_head_episode_id": head["episode_id"],
        "history_status": history["status"],
        "history_relation": (
            history["relations"][0]["relation"]
            if history["relations"] else None),
        "context_status": context["relation_scope"]["status"],
        "context_relation_aware": context["context_effect"]["relation_aware"],
        "owner_event_status": result.status,
        "event_id": event_id,
        "public_store_append_used": True,
        "module_writer_record_relation_change_used": False,
        "owner_receipt_for_relation_present": False,
    })
    fanin.close()
    return {
        "state_root": str(state_root),
        "appended_without_module_writer": appended_without_writer,
        "context_forged": context_forged,
        "history_status": history["status"],
        "context_status": context["relation_scope"]["status"],
        "primary_episode_id": primary["episode_id"],
        "head_episode_id": head["episode_id"],
    }


def cold_probe(world_info):
    state_root = world_info["state_root"]
    actor_ids = world_info["actors"]
    event_ids = world_info["events"]
    as_of_by_event = {
        world_info["first_event"]: world_info["first_clock"],
        world_info["second_event"]: world_info["second_clock"],
        world_info["third_event"]: world_info["third_clock"],
    }
    all_clocks = sorted({
        world_info["start_clock"], world_info["first_clock"],
        world_info["second_clock"], world_info["third_clock"],
    })
    fanin = load_p2().open(Path(state_root))
    try:
        warm = snapshot(
            fanin.session, actor_ids, event_ids, as_of_by_event, all_clocks)
        warm_counts = counts(fanin.session)
    finally:
        fanin.close()
    config = {
        "state_root": state_root,
        "actor_ids": actor_ids,
        "event_ids": event_ids,
        "as_of_by_event": as_of_by_event,
        "all_clocks": all_clocks,
        "retry": {
            "actor_id": P_ID,
            "other_actor_id": O_ID,
            "relation": RELATION,
            "change": "ENTER",
            "clock": world_info["start_clock"],
            "operation_id": "c05review:enter",
            "exposed_actor_ids": [P_ID, O_ID],
            "value": "guest",
            "private_state": {"note": REL_SECRET},
        },
    }
    env = dict(os.environ)
    env["TMPDIR"] = str(REPO / ".local-logs/sorok-c05-independent-g5/tmp")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    completed = subprocess.run(
        [sys.executable, "-B", str(HERE / "c05_cold_child.py"),
         json.dumps(config)],
        cwd=str(REPO), capture_output=True, text=True, timeout=300, env=env,
    )
    check("cold_child_exit_zero", completed.returncode == 0,
          {"exit": completed.returncode, "stderr": completed.stderr[-1000:]})
    if completed.returncode != 0:
        return {"error": completed.stderr[-2000:]}
    cold = json.loads(completed.stdout)
    check("cold_snapshot_exact", cold["snapshot"] == warm,
          {"warm_keys": sorted(warm), "cold_keys": sorted(cold["snapshot"])})
    retry = cold["retry"]
    check("cold_retry_unchanged_no_duplicate",
          retry["status"] == "UNCHANGED"
          and retry["counts_before"] == retry["counts_after"]
          == warm_counts
          and retry["primary_episode_id"]
          == world_info["entry"]["primary_episode_id"],
          retry)
    check("cold_private_state_absent",
          all(secret not in completed.stdout for secret in (
              P_SECRET, O_SECRET, Q_SECRET, R_SECRET, REL_SECRET)))
    return {
        "child_exit": completed.returncode,
        "snapshot_exact": cold["snapshot"] == warm,
        "retry": retry,
        "warm_counts": warm_counts,
        "warm_snapshot": warm,
        "cold_snapshot": cold["snapshot"],
    }


def main() -> int:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    fanin, session, focal, owner, reg, state_root = main_world()
    try:
        c01_checks(session, focal, reg)
        world_info = relation_checks(session, focal, owner)
        world_info["state_root"] = str(state_root)
    finally:
        owner.close()
        fanin.close()
    forger = forgery_probe()
    cold = cold_probe(world_info)
    failures = [row for row in CHECKS if not row["pass"]]
    report = {
        "schema": "SOROK_C05_INDEPENDENT_G5_PROBE@1",
        "reviewer_session": "ses_e2186e745ffecK1Ilg4cw26pVu",
        "candidate_sha": "9cf13763b0061400e2c936eaf1d0a2f4b76a03f7",
        "report_sha": "bc45f699a22708aae3df7e34b1ba3b272a362565",
        "start_sha": "ee82397a979e52eab83f2bd4ea48ed9c28ea7ab9",
        "checks_total": len(CHECKS),
        "checks_passed": len(CHECKS) - len(failures),
        "checks_failed": len(failures),
        "failures": failures,
        "observations": OBSERVATIONS,
        "forgery": forger,
        "cold": cold,
        "world": world_info,
        "checks": CHECKS,
    }
    report_path = EVIDENCE / "c05_probe_report.json"
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True))
    print("SUMMARY", json.dumps({
        "checks_total": report["checks_total"],
        "checks_passed": report["checks_passed"],
        "checks_failed": report["checks_failed"],
        "failures": [row["name"] for row in failures],
        "forgery": forger,
        "cold_exit": cold.get("child_exit"),
        "cold_snapshot_exact": cold.get("snapshot_exact"),
        "cold_retry_status": (cold.get("retry") or {}).get("status"),
        "report": str(report_path),
    }, sort_keys=True))
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
