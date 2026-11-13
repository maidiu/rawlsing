"""Executed hostile and cold-reopen controls for the final C03/C04 candidate.

These extend the committed A/B suites to the remaining first-consumer surfaces:
embedded admission-receipt exactness, event clock forgery, duplicate receipts
and episodes, historical hearing under later co-presence, changed C03 material
obligations, and genuine cold reopen after a refused mutation and restoration.

Real J1/P6/D03 stores and the existing C12 writers are used; no private model.
"""
from __future__ import annotations

from pathlib import Path
import json
import sys

import pytest

J1 = Path(__file__).resolve().parents[1] / "SOROK-E01-J1-995-R1"
if str(J1) not in sys.path:
    sys.path.insert(0, str(J1))

from test_j1_three_head_join import (  # noqa: E402
    PARENT_ID, HIDDEN, TEXT, open_j1_case, _close,
)
from p3_fixture_support import reopen_owner  # noqa: E402
from developmental_recursion.contracts import RecursionRefusal  # noqa: E402
from developmental_recursion.parent_speech import (  # noqa: E402
    PARENT_UTTERANCE_KIND, read_child_experience, read_child_uptake,
    read_parent_utterance,
)
from developmental_recursion.parent_decision import (  # noqa: E402
    read_parent_material_prospectives,
)
from developmental_recursion.parent_activity import read_parent_history  # noqa: E402
from run_p6 import child_speech_experience  # noqa: E402
import j1_join  # noqa: E402


def _episode_tamper(store, event_id, mutate):
    real = store.episodes

    def episodes(branch_id):
        rows = real(branch_id)
        result = []
        for row in rows:
            if (row.get("kind") == PARENT_UTTERANCE_KIND
                    and (row.get("body") or {}).get("event_id") == event_id):
                row = mutate(dict(row))
            result.append(row)
        return result

    store.episodes = episodes
    return real


def _perception_tamper(store, target_actor_id, mutate):
    real = store.perceptions

    def perceptions(branch_id, actor_id):
        rows = real(branch_id, actor_id)
        if actor_id == target_actor_id:
            return mutate(rows)
        return rows

    store.perceptions = perceptions
    return real


@pytest.mark.parametrize("field,value", [
    ("text", "I agree to everything."),
    ("event_kind", "MOVE"),
    ("event_authored_by", "IMPERSONATED_PARENT"),
    ("decision_action", "DECLINE"),
    ("hidden_reason_hash", "2" * 64),
    ("public_utterance", False),
])
def test_embedded_admission_receipt_fields_are_exactly_bound(
    tmp_path, field, value
):
    opened = open_j1_case(tmp_path / ("receipt-" + field))
    try:
        session = opened["session"]
        eid = opened["receipt"]["event_id"]
        store = session.product.store

        def forge(row):
            body = dict(row["body"])
            body["receipt"] = {**body["receipt"], field: value}
            row["body"] = body
            return row

        original = _episode_tamper(store, eid, forge)
        with pytest.raises(
            RecursionRefusal, match="CHILD_UPTAKE_UTTERANCE_MISMATCH"
        ):
            read_child_uptake(session, opened["focal"], eid)
        with pytest.raises(RecursionRefusal):
            child_speech_experience(session, event_id=eid)
        with pytest.raises(
            RecursionRefusal, match="PARENT_UTTERANCE_RECEIPT_SEVERED"
        ):
            read_parent_utterance(
                session, PARENT_ID, "j1-speech", as_actor=PARENT_ID)
        store.episodes = original
        assert read_child_uptake(
            session, opened["focal"], eid)["status"] == "PERCEIVED"
        assert child_speech_experience(
            session, event_id=eid)["status"] == "PERCEIVED"
        assert read_parent_utterance(
            session, PARENT_ID, "j1-speech", as_actor=PARENT_ID
        )["status"] == "READ"
    finally:
        _close(opened)


@pytest.mark.parametrize("field,value", [
    ("clock", None),
    ("summary", "Mother is now represented as agreeing."),
    ("location", "market"),
    ("sequence", None),
])
def test_stale_hash_event_clock_and_public_fields_refuse(
    tmp_path, monkeypatch, field, value
):
    opened = open_j1_case(tmp_path / ("event-" + field))
    try:
        session = opened["session"]
        eid = opened["receipt"]["event_id"]
        real = session.event

        def forged(ref):
            row = real(ref)
            if ref != eid or row is None:
                return row
            row = dict(row)
            if field == "clock":
                row["clock"] = row["clock"] + 1
            elif field == "sequence":
                row["sequence"] = row["sequence"] + 1
            else:
                row[field] = value
            return row

        monkeypatch.setattr(session, "event", forged)
        with pytest.raises(RecursionRefusal):
            read_child_uptake(session, opened["focal"], eid)
        with pytest.raises(RecursionRefusal):
            child_speech_experience(session, event_id=eid)
        with pytest.raises(RecursionRefusal):
            read_parent_utterance(
                session, PARENT_ID, "j1-speech", as_actor=PARENT_ID)
        monkeypatch.setattr(session, "event", real)
        assert read_child_uptake(
            session, opened["focal"], eid)["status"] == "PERCEIVED"
    finally:
        _close(opened)


@pytest.mark.parametrize("field,value", [
    ("root", "0" * 64),
    ("branch", "FORGED_BRANCH"),
    ("actor_id", "FORGED_PARENT"),
    ("alias", "X"),
    ("clock", 999999),
    ("child_actor_id", "FORGED_CHILD"),
    ("child_alias", "Z"),
])
def test_episode_custody_field_mismatch_refuses(tmp_path, field, value):
    opened = open_j1_case(tmp_path / ("episode-" + field))
    try:
        session = opened["session"]
        eid = opened["receipt"]["event_id"]
        store = session.product.store

        def forge(row):
            if field == "clock":
                row["clock"] = value
            else:
                row["body"] = {**row["body"], field: value}
            return row

        original = _episode_tamper(store, eid, forge)
        with pytest.raises(RecursionRefusal):
            read_child_uptake(session, opened["focal"], eid)
        with pytest.raises(RecursionRefusal):
            child_speech_experience(session, event_id=eid)
        store.episodes = original
        assert read_child_uptake(
            session, opened["focal"], eid)["status"] == "PERCEIVED"
    finally:
        _close(opened)


def test_duplicate_parent_receipt_and_duplicate_episode_refuse(tmp_path):
    opened = open_j1_case(tmp_path / "duplicates")
    try:
        session = opened["session"]
        eid = opened["receipt"]["event_id"]
        alias = opened["receipt"]["alias"]
        store = session.product.store

        original_perceptions = _perception_tamper(
            store, alias, lambda rows: rows + rows[-1:])
        with pytest.raises(
            RecursionRefusal, match="CHILD_UPTAKE_PARENT_RECEIPT_SEVERED"
        ):
            read_child_uptake(session, opened["focal"], eid)
        store.perceptions = original_perceptions

        real_episodes = store.episodes

        def duplicate(branch_id):
            rows = real_episodes(branch_id)
            hit = [row for row in rows
                   if (row.get("body") or {}).get("event_id") == eid]
            return rows + hit

        store.episodes = duplicate
        with pytest.raises(
            RecursionRefusal, match="CHILD_UPTAKE_UTTERANCE_NOT_FOUND"
        ):
            read_child_uptake(session, opened["focal"], eid)
        with pytest.raises(RecursionRefusal):
            read_child_experience(session, opened["focal"], event_id=eid)
        store.episodes = real_episodes
        assert read_child_uptake(
            session, opened["focal"], eid)["status"] == "PERCEIVED"
    finally:
        _close(opened)


def test_later_co_presence_cannot_invent_historically_unheard_speech(
    tmp_path,
):
    opened = open_j1_case(tmp_path / "late-presence", child_present=False)
    try:
        session = opened["session"]
        eid = opened["receipt"]["event_id"]
        assert opened["receipt"]["child_perception_channel"] == "NOT_PERCEIVED"
        child_alias = opened["receipt"]["child_alias"]
        parent_location = session.world().positions[opened["receipt"]["alias"]]
        world = session.world()
        world.positions[child_alias] = parent_location
        session.product._checkpoint(session.branch_id, world.clock, world)
        assert session.world().positions[child_alias] == parent_location
        assert read_child_uptake(
            session, opened["focal"], eid)["status"] == "NOT_PERCEIVED"
        p6 = child_speech_experience(session, event_id=eid)
        assert p6["status"] == "NOT_PERCEIVED"
        assert p6["event"] is None
        joined = j1_join.compose_j1(
            opened["case"].owner, session, child_id=opened["focal"],
            speech_event_id=eid, utterance_receipt=opened["receipt"],
            plan=opened["plan"])
        assert joined["status"] == "HELD_NOT_PERCEIVED"
        assert joined["child_experience"]["response_input"] is None
        assert HIDDEN not in json.dumps(joined)
    finally:
        _close(opened)


def test_changed_debt_and_care_history_change_material_possibilities(
    tmp_path,
):
    baseline = open_j1_case(tmp_path / "prospective-baseline")
    debt = open_j1_case(
        tmp_path / "prospective-debt", parent_overrides={"debt_units": 61})
    care = open_j1_case(
        tmp_path / "prospective-care", parent_overrides={"care_hours_due": 8})
    try:
        def options(opened):
            result = read_parent_material_prospectives(
                opened["session"], PARENT_ID, as_actor=PARENT_ID)
            assert result["chosen_candidate"] is None
            assert result["performed_event"] is None
            assert all(not row["chosen"] and not row["performed"]
                       for row in result["options"])
            return result, {row["candidate"]: row for row in result["options"]}

        base_result, base = options(baseline)
        debt_result, debt_options = options(debt)
        care_result, care_options = options(care)
        assert base["POSSIBLE_JUNIOR_PURCHASE"]["status"] == (
            "ELIGIBLE_NOT_SELECTED")
        assert debt_options["POSSIBLE_JUNIOR_PURCHASE"]["status"] == (
            "MATERIALLY_INELIGIBLE")
        assert "OBLIGATION_DEBT" in (
            debt_options["POSSIBLE_JUNIOR_PURCHASE"]["reasons"])
        assert care_options["POSSIBLE_JUNIOR_PURCHASE"]["status"] == (
            "MATERIALLY_INELIGIBLE")
        assert "OBLIGATION_CARE" in (
            care_options["POSSIBLE_JUNIOR_PURCHASE"]["reasons"])
        assert base["QUIET_NONPURCHASE"]["status"] == "ELIGIBLE_NOT_SELECTED"
        assert debt_options["QUIET_NONPURCHASE"]["status"] == (
            "ELIGIBLE_NOT_SELECTED")
        assert care_options["QUIET_NONPURCHASE"]["status"] == (
            "ELIGIBLE_NOT_SELECTED")
        assert (base_result["history_source"] != debt_result["history_source"]
                or base_result["source"] != debt_result["source"])
        assert (base_result["history_source"] != care_result["history_source"]
                or base_result["source"] != care_result["source"])
    finally:
        _close(baseline)
        _close(debt)
        _close(care)


def test_cold_reopen_after_refused_mutation_and_restore_conserves_c04(
    tmp_path,
):
    opened = open_j1_case(tmp_path / "cold-c04")
    state_root = Path(opened["path"])
    try:
        session = opened["session"]
        eid = opened["receipt"]["event_id"]
        event_hash = opened["receipt"]["event_hash"]
        episode_count = len([
            row for row in session.product.store.episodes(session.branch_id)
            if row.get("kind") == PARENT_UTTERANCE_KIND])
        history = read_parent_history(
            session, PARENT_ID, as_actor=PARENT_ID)
        purchase_count = history["purchase_episode_count"]
        assert purchase_count == 1
    finally:
        _close(opened)

    base2, owner2 = reopen_owner(opened["case"])
    try:
        session2 = base2.fanin.session
        assert read_child_uptake(
            session2, opened["focal"], eid)["status"] == "PERCEIVED"
        assert child_speech_experience(
            session2, event_id=eid)["status"] == "PERCEIVED"
        real_event = session2.event

        def forged(ref):
            row = real_event(ref)
            if ref != eid or row is None:
                return row
            row = dict(row)
            row["summary"] = "Forged after cold reopen."
            return row

        session2.event = forged
        with pytest.raises(RecursionRefusal):
            child_speech_experience(session2, event_id=eid)
        session2.event = real_event
        assert child_speech_experience(
            session2, event_id=eid)["status"] == "PERCEIVED"
        assert session2.event(eid)["hash"] == event_hash
    finally:
        owner2.close()

    base3, owner3 = reopen_owner(opened["case"])
    try:
        session3 = base3.fanin.session
        assert session3.event(eid)["hash"] == event_hash
        assert len([
            row for row in session3.product.store.episodes(session3.branch_id)
            if row.get("kind") == PARENT_UTTERANCE_KIND]) == episode_count
        assert read_parent_history(
            session3, PARENT_ID, as_actor=PARENT_ID
        )["purchase_episode_count"] == purchase_count
        assert read_child_uptake(
            session3, opened["focal"], eid)["status"] == "PERCEIVED"
        assert child_speech_experience(
            session3, event_id=eid)["status"] == "PERCEIVED"
    finally:
        owner3.close()
