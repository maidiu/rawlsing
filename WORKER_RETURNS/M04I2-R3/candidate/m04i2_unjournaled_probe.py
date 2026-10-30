#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path

def journaled_apply(c, accessibility: str, operation: str, target: str | None = None) -> dict:
    from cell import owner
    args = c.epi_args(accessibility)
    args.update(stance_operation=operation, target_record_ref=target)
    result = owner.adp017_apply_epistemic_effect(**args)
    assert result["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION", result
    c.journal.commit(
        "ADP017_COMMIT",
        {
            "before": result["transition"]["pre_state_hash"],
            "after": c.ctx.state_hash,
            "result": result,
        },
        c.e1.effective_causal_time,
        [c.e1.event_id],
    )
    return result


def run_forged(runtime: Path) -> dict:
    sys.path.insert(0, str(runtime))
    from cell import Cell, Refusal, digest
    c = Cell()
    c.prepare("CERTAIN", "BELIEF")
    packet = c.checkpoint()
    state = packet["ctx"]["state"]
    transition = deepcopy(state["epistemic_transitions"][0])
    effect = deepcopy(transition["effect"])
    forged_pre = digest(["M04I2_UNJOURNALED_FORGED_PRESTATE"])
    effect["effect_id"] = digest([
        "EPISTEMIC_EFFECT",
        {k: v for k, v in effect.items() if k != "effect_id"},
        forged_pre,
        transition["target_record_ref"],
    ])
    transition["effect"] = deepcopy(effect)
    transition["pre_state_hash"] = forged_pre
    state["stances"] = {effect["effect_id"]: deepcopy(effect)}
    transition["post_stance_set_hash"] = digest(state["stances"])
    transition["transition_id"] = digest({
        k: v for k, v in transition.items()
        if k not in ("transition_id", "post_state_set_hash")
    })
    snapshot = state["state_sets"][c.claim_id]
    snapshot["active_stance_records"] = [deepcopy(effect)]
    snapshot["last_transition_ref"] = transition["transition_id"]
    snapshot["current_state_hash"] = digest({
        k: v for k, v in snapshot.items() if k != "current_state_hash"
    })
    state["permissions"][c.claim_id]["epistemic_state_hash"] = snapshot["current_state_hash"]
    transition["post_state_set_hash"] = snapshot["current_state_hash"]
    state["epistemic_transitions"].append(transition)
    try:
        c.restore(packet)
    except Refusal as exc:
        return {"variant":"forged","restore":"REFUSED","code":exc.code,"exit":0}
    checkpoint = c.checkpoint()
    try:
        read = c.read_owner(c.ctx.state_hash, "1998-11-20T09:00:00Z")
        result = {"read":"ACCEPTED","streams":read["streams"],
                  "disposition":read["claim_selection_provenance"]["disposition"],
                  "rollback_unchanged":False}
        code = 2
    except Refusal as exc:
        result = {"read":"REFUSED","code":exc.code,
                  "rollback_unchanged":c.checkpoint()==checkpoint}
        code = 0
    return {
        "variant":"forged",
        "before_direct": {"state_transitions":1,"journaled_adp017":1,
                          "active_stances":1,
                          "accessibility":state["state_sets"][c.claim_id]["current_claim_accessibility"]},
        "after_direct": {"state_transitions":len(c.ctx.epistemic_transitions),
                         "journaled_adp017":len(c.journal.read_effects("ADP017_COMMIT")),
                         "active_stances":len(c.ctx.stances)},
        "result":result,
        "exit":code,
    }


def run(runtime: Path) -> dict:
    sys.path.insert(0, str(runtime))
    from cell import Cell, Refusal, owner
    c = Cell()
    c.prepare("CERTAIN", "BELIEF")
    initial_effect = next(iter(c.ctx.stances))
    journaled_apply(c, "CLAIM_INACCESSIBLE", "SUPERSEDE_EXACT_RECORD", initial_effect)
    revoked_effect = next(iter(c.ctx.stances))
    before_direct = {
        "state_transitions": len(c.ctx.epistemic_transitions),
        "journaled_adp017": len(c.journal.read_effects("ADP017_COMMIT")),
        "active_stances": len(c.ctx.stances),
        "accessibility": c.ctx.state_sets[c.claim_id]["current_claim_accessibility"],
    }
    args = c.epi_args("CLAIM_ACCESSIBLE")
    args.update(
        stance_operation="SUPERSEDE_EXACT_RECORD",
        target_record_ref=revoked_effect,
        pre_state_hash=c.ctx.state_hash,
    )
    direct = owner.adp017_apply_epistemic_effect(**args)
    after_direct = {
        "decision_state": direct.get("decision_state"),
        "state_transitions": len(c.ctx.epistemic_transitions),
        "journaled_adp017": len(c.journal.read_effects("ADP017_COMMIT")),
        "active_stances": len(c.ctx.stances),
        "accessibility": c.ctx.state_sets[c.claim_id]["current_claim_accessibility"],
    }
    checkpoint = c.checkpoint()
    try:
        read = c.read_owner(c.ctx.state_hash, "1998-11-20T09:00:00Z")
        result = {
            "read": "ACCEPTED",
            "streams": read["streams"],
            "disposition": read["claim_selection_provenance"]["disposition"],
            "rollback_unchanged": False,
        }
        code = 2
    except Refusal as exc:
        result = {
            "read": "REFUSED",
            "code": exc.code,
            "rollback_unchanged": c.checkpoint() == checkpoint,
        }
        code = 0
    return {
        "variant":"direct",
        "runtime": str(runtime),
        "before_direct": before_direct,
        "after_direct": after_direct,
        "result": result,
        "exit": code,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--runtime", type=Path, required=True)
    parser.add_argument("--variant", choices=("direct","forged"), default="direct")
    args = parser.parse_args()
    output = run_forged(args.runtime.resolve()) if args.variant == "forged" else run(args.runtime.resolve())
    print(json.dumps(output, indent=2))
    return output["exit"]


if __name__ == "__main__":
    raise SystemExit(main())
