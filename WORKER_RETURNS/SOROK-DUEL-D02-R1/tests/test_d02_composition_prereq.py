"""Composition prerequisite: D01 retention + B01 household + C01 actor access.

One fresh actual root at the frozen AUT0MERGED cut is used for all three
interfaces.  This is not a claim that three separate suites prove the join:
the test exercises the actual owners and readers together, then cold-reopens
the same root and uses the P3 later consumer.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

D02_ROOT = Path(__file__).resolve().parents[1]
WORKER_RETURNS = D02_ROOT.parent
D01_ROOT = WORKER_RETURNS / "SOROK-DUEL-D01-R1"
P3_ROOT = WORKER_RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
ENGINE_ROOT = WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
P6_ROOT = WORKER_RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
B02_ROOT = WORKER_RETURNS / "SOROK-DUEL-B02-R1"
for _path in (D01_ROOT, P3_ROOT, ENGINE_ROOT, P3_ROOT / "tests", P6_ROOT, B02_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import d01_reuse  # noqa: E402
import historical_period as b02  # noqa: E402
import house  # noqa: E402
from developmental_recursion.contracts import EventProposal  # noqa: E402
from developmental_recursion.p2_owner import P2Owner, load_p2  # noqa: E402
from developmental_recursion.supporting_actor import (  # noqa: E402
    read_actor_access,
    read_supporting_actor,
    register_supporting_actor,
)
from p3 import situated_context  # noqa: E402
from p3_fixture_support import (  # noqa: E402
    COUNTERPART,
    PROJECT,
    build_case,
)

PARENT_ID = "TEST_ONLY_D02_PARENT"
PARENT_ALIAS = "P"


def _open_base(case):
    fanin = load_p2().open(Path(case.state_root))
    try:
        actual = fanin.deps["case_for"](True)
        return P2Owner(
            fanin,
            case=actual,
            source=fanin.deps["source_for"](actual),
            participants=tuple(fanin.session.read_root()["actor_ids"]),
        )
    except BaseException:
        fanin.close()
        raise


def test_fresh_root_d01_retention_household_and_supporting_actor_coexist(
    tmp_path: Path,
) -> None:
    case = build_case(tmp_path / "composition")
    cold = None
    case_closed = False
    first = None
    household_before = None
    try:
        session = case.base_owner.fanin.session
        focal = session.read_root()["actor_ids"][0]
        house.establish(session)
        b02.establish_period_plan(session)
        household_before = house.read_household(session)
        registered = register_supporting_actor(
            session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
            private_state={"motive": "d02-composition-secret"},
        )
        assert registered["status"] == "REGISTERED"

        first = case.owner.realize(
            "d02-composition-formation", case.proposals[0],
            case.owner.snapshot(),
        )
        records = case.owner.store.query(
            project=PROJECT, counterpart=COUNTERPART,
            as_of=first.after.clock,
        )
        assert len(records) == 2
        record_hashes = [row["hash"] for row in records]

        shared = EventProposal(
            "d02-composition-parent-event", first.after.clock + 3,
            "ADMIT_EVENT", (case.base_owner.source_ref,),
            (focal, PARENT_ID), {},
        )
        parent_result = case.base_owner.realize(
            "d02-composition-parent-op", shared,
            case.base_owner.snapshot(),
        )
        assert parent_result.consequences["supporting_participation"] == "RECORDED"
        event_id = parent_result.consequences["supporting_participants"][0][
            "event_id"]
        assert read_actor_access(session, focal, event_id)["status"] == (
            "PERCEIVED")
        assert read_actor_access(session, PARENT_ID, event_id)["status"] == (
            "PERCEIVED")
        parent_before = read_supporting_actor(session, PARENT_ID)
        assert parent_before["role"] == "parent"
        assert parent_before["private_state"] == "NOT_READ"
        case.owner.close()
        case_closed = True

        base = _open_base(case)
        cold = d01_reuse.open_cold_owner(base, state_root=case.state_root)
        assert cold.store.head()["count"] == 2
        reread = d01_reuse.read_sourcefree_records(
            cold, project=PROJECT, counterpart=COUNTERPART,
            as_of=first.after.clock,
        )
        assert reread["hashes"] == record_hashes
        household_after = house.read_household(base.fanin.session)
        assert household_after["source"] == household_before["source"]
        assert household_after["place"] == household_before["place"]
        assert household_after["resources"] == household_before["resources"]
        parent_after = read_supporting_actor(base.fanin.session, PARENT_ID)
        assert parent_after["role"] == "parent"
        focal_access_after = read_actor_access(
            base.fanin.session, focal, event_id)
        assert focal_access_after["status"] == "PERCEIVED"
        selector = situated_context.build_situated_context(
            cold, event_id=event_id, plan=case.plans[3])
        assert selector["material"]["status"] == "AVAILABLE"
        assert selector["relations"][0]["actor_id"] == PARENT_ID
        assert "ATTEND_HOUSEHOLD_MATERIAL" in selector["admissible_options"]
        assert "ADDRESS_ELIGIBLE_OTHER" in selector["admissible_options"]
        acquired = selector["acquired_state"]
        assert acquired["scope"]["counterpart"] == "vertical:counterpart"
        assert acquired["scope"]["counterpart"] != PARENT_ID
        assert acquired["status"] == "CONTRADICTION"
        assert acquired["eligible_modes"] == ["joint_check", "private_check"]
        assert "d02-composition-secret" not in json.dumps(acquired)
        assert cold.store.head()["count"] == 2
        period = selector["period"]
        assert period["status"] == "QUALIFIED_CURRENT_PERIOD"
        assert period["logical_tick"] == cold.snapshot().clock
        assert period["period"]["period_id"] == "period:2026-h1"
        assert period["employment"]["term_id"] == (
            "employment:workshop-cooperative")
        assert period["holder_actor_slot"] == "A"
        assert selector["date_scope"]["calendar"] == "B02_CURRENT_LOGICAL_PERIOD"

        later = d01_reuse.later_consumer(
            cold, "d02-composition-later", case.proposals[1],
            require_record_hashes=record_hashes,
        )
        assert set(later["record_hashes"]) == set(record_hashes)
        assert cold.store.head()["count"] == 2
        assert later["response"]["native_rule"] == "MISSING_RULE"
    finally:
        if cold is not None:
            cold.close()
        elif not case_closed:
            case.owner.close()
