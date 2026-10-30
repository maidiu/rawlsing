"""M04R terminal journal-coverage adversarial tests.

Run against the reconstructed M01/M02/M03 runtime:
    M04R_RUNTIME=<runtime>/m02/runtime/m01/repro \
    PYTHONPATH=$M04R_RUNTIME python3 -m pytest test_m04r_journal_coverage.py -q
"""
from __future__ import annotations

import sys
from copy import deepcopy
from pathlib import Path

import pytest

RUNTIME = Path(__import__("os").environ.get("M04R_RUNTIME", "")).resolve()
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from cell import Cell, Refusal, digest, owner  # noqa: E402

CUT = "1998-11-20T09:00:00Z"


def _journaled_apply(c: Cell, accessibility: str, operation: str, target: str | None = None):
    args = c.epi_args(accessibility)
    args.update(stance_operation=operation, target_record_ref=target)
    result = owner.adp017_apply_epistemic_effect(**args)
    assert result["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION", result
    c.journal.commit(
        "ADP017_COMMIT",
        {"before": result["transition"]["pre_state_hash"], "after": c.ctx.state_hash,
         "result": result},
        c.e1.effective_causal_time,
        [c.e1.event_id],
    )
    return result


def _refusal_code(exc: BaseException) -> str:
    return getattr(exc, "code", str(exc))


def test_direct_unjournaled_terminal_is_refused():
    c = Cell()
    c.prepare("CERTAIN", "BELIEF")
    initial = next(iter(c.ctx.stances))
    _journaled_apply(c, "CLAIM_INACCESSIBLE", "SUPERSEDE_EXACT_RECORD", initial)
    revoked = next(iter(c.ctx.stances))
    args = c.epi_args("CLAIM_ACCESSIBLE")
    args.update(stance_operation="SUPERSEDE_EXACT_RECORD",
                target_record_ref=revoked, pre_state_hash=c.ctx.state_hash)
    direct = owner.adp017_apply_epistemic_effect(**args)
    assert direct["decision_state"] == "APPLIED_EPISTEMIC_TRANSITION"
    assert len(c.ctx.epistemic_transitions) == 3
    assert len(c.journal.read_effects("ADP017_COMMIT")) == 2
    checkpoint = c.checkpoint()
    with pytest.raises(Refusal) as exc:
        c.read_owner(c.ctx.state_hash, CUT)
    assert _refusal_code(exc.value) == "CLAIM_TRANSITION_UNJOURNALED"
    assert c.checkpoint() == checkpoint


def test_orphan_terminal_journal_entry_is_refused():
    c = Cell()
    c.prepare("CERTAIN", "BELIEF")
    orphan = digest(["M04R_ORPHAN_TERMINAL"])
    c.journal.commit(
        "ADP017_COMMIT",
        {"before": c.ctx.state_hash, "after": c.ctx.state_hash,
         "result": {"transition": {"transition_id": orphan,
                                   "post_state_set_hash": c.ctx.state_hash}}},
        c.e1.effective_causal_time,
        [c.e1.event_id],
    )
    with pytest.raises(Refusal) as exc:
        c.read_owner(c.ctx.state_hash, CUT)
    assert _refusal_code(exc.value) == "CLAIM_TRANSITION_ANCESTRY_MISSING"


def test_duplicate_journal_coverage_is_refused():
    c = Cell()
    c.prepare("CERTAIN", "BELIEF")
    entry = c.journal.read_effects("ADP017_COMMIT")[0]
    c.journal.commit("ADP017_COMMIT", entry["payload"],
                     entry["effective_causal_time"], entry["causal_parent_refs"])
    with pytest.raises(Refusal) as exc:
        c.read_owner(c.ctx.state_hash, CUT)
    assert _refusal_code(exc.value) == "CLAIM_TRANSITION_JOURNAL_DUPLICATE"


def test_unjournaled_forged_prestate_is_refused():
    c = Cell()
    c.prepare("CERTAIN", "BELIEF")
    packet = c.checkpoint()
    state = packet["ctx"]["state"]
    transition = deepcopy(state["epistemic_transitions"][0])
    effect = deepcopy(transition["effect"])
    forged_pre = digest(["M04R_UNJOURNALED_FORGED_PRESTATE"])
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
    codes = {"CLAIM_TRANSITION_UNJOURNALED", "CLAIM_TRANSITION_PRESTATE_ANCESTRY"}
    try:
        c.restore(packet)
    except Refusal as exc:
        assert _refusal_code(exc) in codes
    else:
        checkpoint = c.checkpoint()
        with pytest.raises(Refusal) as exc:
            c.read_owner(c.ctx.state_hash, CUT)
        assert _refusal_code(exc.value) in codes
        assert c.checkpoint() == checkpoint
