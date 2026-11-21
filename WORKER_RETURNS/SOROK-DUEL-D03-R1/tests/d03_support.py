"""Actual C04 speech/child-uptake support for D02 counterstrike and D03."""
from __future__ import annotations

import sys
from pathlib import Path

D03_ROOT = Path(__file__).resolve().parents[1]
WORKER_RETURNS = D03_ROOT.parent
P3_ROOT = WORKER_RETURNS / "SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1"
ENGINE_ROOT = WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
B02_ROOT = WORKER_RETURNS / "SOROK-DUEL-B02-R1"
P6_ROOT = WORKER_RETURNS / "SOROK-P6-ONE-LIVING-HOUSE-R1"
PROJECTION_ROOT = WORKER_RETURNS / "SOROK-S45-S47-PROJECTION-20261105-R1"
for _path in (P3_ROOT, P3_ROOT / "tests", ENGINE_ROOT, B02_ROOT,
              P6_ROOT, PROJECTION_ROOT):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

import house  # noqa: E402
from developmental_recursion.parent_activity import (  # noqa: E402
    establish_parent_material,
    historical_period_module,
    parent_material_fixture,
)
from developmental_recursion.parent_decision import (  # noqa: E402
    admit_parent_decision,
    parent_request_fixture,
)
from developmental_recursion.parent_speech import (  # noqa: E402
    perform_parent_utterance,
    read_child_uptake,
)
from developmental_recursion.supporting_actor import (  # noqa: E402
    register_supporting_actor,
)
from p3_fixture_support import build_case  # noqa: E402

PARENT_ID = "TEST_ONLY_D03_PARENT"
PARENT_ALIAS = "P"
HIDDEN = "d03-private-motive-not-for-nadia"
BASE = {
    "employment_status": "employed",
    "wage_units_per_hour": 5,
    "debt_units": 4,
    "care_hours_due": 2,
    "cash_units": 100,
    "free_hours": 8,
    "currency_unit": "sourcefree_currency_unit",
    "source_ref": "sourcefree:parent:antecedent:baseline",
}


def open_speech_case(
    path: Path,
    *,
    outcome: str = "recognized_plan",
    child_present: bool = True,
    debt_units: int = 4,
    text: str = "Not this time.",
    hidden: str = HIDDEN,
    operation_id: str = "d03-speech",
):
    """Build one fresh actual P2/P3 root with an actual C04 parent speech.

    The returned owner is the actual P3Owner; the caller owns/closes it. The
    speech is written by the C04 writer, not a hand-built utterance dictionary.
    """
    import shutil
    if path.exists():
        shutil.rmtree(path)
    case = build_case(path, history_outcomes=(outcome,))
    session = case.base_owner.fanin.session
    focal = session.read_root()["actor_ids"][0]
    case.owner.realize(
        "d03-formation", case.proposals[0], case.owner.snapshot())
    house.establish(session)
    house.establish_dwelling(session)
    historical_period_module().establish_period_plan(session)
    register_supporting_actor(
        session, alias=PARENT_ALIAS, actor_id=PARENT_ID, role="parent",
        private_state={"motive": hidden},
    )
    values = {**BASE, "debt_units": debt_units}
    establish_parent_material(
        session, PARENT_ID,
        fixture=parent_material_fixture(actor_id=PARENT_ID, **values),
    )
    b04 = __import__(
        "developmental_recursion.parent_decision",
        fromlist=["_b04_module"],
    )._b04_module()
    b04.establish_market_inventory(session)
    request = parent_request_fixture(kind="junior", owner_actor_id=PARENT_ID)
    admit_parent_decision(
        session, PARENT_ID, operation_id="d03-decision",
        request=request, as_actor=PARENT_ID,
    )
    if not child_present:
        child_alias = next(
            alias for alias, row in session.world().actor_state.items()
            if row.get("actor_id") == focal)
        world = session.world()
        world.positions[child_alias] = "market"
        session.product._checkpoint(session.branch_id, world.clock, world)
    receipt = perform_parent_utterance(
        session, PARENT_ID, decision_id="d03-decision",
        text=text, hidden_reason={"reason": hidden},
        operation_id=operation_id,
    )
    uptake = read_child_uptake(session, focal, receipt["event_id"])
    return {
        "case": case,
        "session": session,
        "focal": focal,
        "receipt": receipt,
        "uptake": uptake,
        "plan": case.plans[1],
    }
