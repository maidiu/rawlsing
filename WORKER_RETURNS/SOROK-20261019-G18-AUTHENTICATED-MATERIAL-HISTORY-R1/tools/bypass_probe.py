#!/usr/bin/env python3
"""Probe the three G17I bypasses against one candidate tree.

Usage: python3 tools/bypass_probe.py <candidate_dir> <c9_dir>
Prints a JSON receipt. Used only for before/after evidence; issues no authority.
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

candidate_dir = Path(sys.argv[1]).resolve()
c9_dir = Path(sys.argv[2]).resolve()
sys.path.insert(0, str(candidate_dir))
sys.path.insert(0, str(c9_dir))

from lab_sgi1.core import h_obj  # noqa: E402
from lab_sgi1.history import PersonHistoryBuilder  # noqa: E402
from lab_sgi1.mother import build_mother_checkpoint  # noqa: E402
from lab_sgi1.continuation import continue_person  # noqa: E402
from lab_sgi1.joint import material_joint_opportunity, observe_joint_actions  # noqa: E402
from lab_sgi1.research import inputs, run  # noqa: E402
import c9_handoff_consumer as C9  # noqa: E402


def relation_packet():
    anchor = build_mother_checkpoint("FIX_M0", "M0").anchor_dict()
    events = PersonHistoryBuilder("R", "S").build()
    witness = observe_joint_actions(anchor, events, material_joint_opportunity())
    return anchor, events, witness


def forged_cash_probe():
    anchor, events, witness = relation_packet()
    material = deepcopy(witness["material"])
    material["payment_per_actor"] = 100000
    material["event_id"] = h_obj({k: v for k, v in material.items()
                                  if k != "event_id"})
    action = deepcopy(witness["actions"][1])
    action["material_event_ref"] = material["event_id"]
    action["causal_parent_event_ids"] = [
        x for x in action["causal_parent_event_ids"]
        if x != witness["material"]["event_id"]] + [material["event_id"]]
    after = deepcopy(action["before"])
    after["cash"] += 100000
    after["free_hours"] -= 1
    after["completed_units"] += 1
    action["after"] = after
    action["event_id"] = h_obj({k: v for k, v in action.items()
                                if k != "event_id"})
    out = continue_person(events, participation=action, material_event=material)
    return dict(
        status="REFUSED" if out is None else "ACCEPTED",
        continuation_cash=None if out is None else out["payload"]["after"]["cash"],
        returned_continuation=out is not None,
    )


def nested_future_child_probe():
    data = inputs()
    data["joint_material_opportunity"]["metadata"] = {
        "future_child_personality": "NESTED_ALIAS"}
    data["joint_material_opportunity"]["event_id"] = h_obj(
        {k: v for k, v in data["joint_material_opportunity"].items()
         if k != "event_id"})
    out = run(data)
    return dict(status=out["terminal"]["status"],
                committed=out["terminal"]["status"] == "COMMITTED")


def c9_fabricated_cash_probe():
    anchor, events, witness = relation_packet()
    material = deepcopy(witness["material"])
    material["payment_per_actor"] = 100000
    material["event_id"] = h_obj({k: v for k, v in material.items()
                                  if k != "event_id"})
    action = deepcopy(witness["actions"][0])
    action["material_event_ref"] = material["event_id"]
    action["causal_parent_event_ids"] = [
        x for x in action["causal_parent_event_ids"]
        if x != witness["material"]["event_id"]] + [material["event_id"]]
    after = deepcopy(action["before"])
    after["cash"] += 100000
    after["free_hours"] -= 1
    after["completed_units"] += 1
    action["after"] = after
    action["event_id"] = h_obj({k: v for k, v in action.items()
                                if k != "event_id"})
    try:
        handoff = C9.build_handoff(action, material)
        receipt = C9.receive_handoff(handoff, material)
        return dict(status=receipt["status"], received_cash=receipt["after"]["cash"],
                    accepted=True)
    except C9.C9Refusal as exc:
        return dict(status="REFUSED", refusal=str(exc), accepted=False)


def main():
    print(json.dumps(dict(
        candidate_dir=str(candidate_dir),
        c9_dir=str(c9_dir),
        forged_material_cash=forged_cash_probe(),
        nested_future_child=nested_future_child_probe(),
        c9_fabricated_cash=c9_fabricated_cash_probe(),
    ), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
