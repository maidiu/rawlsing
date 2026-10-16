"""HQ297 G11: source-free, NO-ACTOR finite constraint feasibility oracle.

This is deliberately NOT ADP-015 implementation, an ADP-020 draw, an actor, a
real genealogical event, a probability estimate, or a V3 forward owner engine.
"""
from __future__ import annotations

import copy
import hashlib
import itertools
import json
from datetime import date, timedelta
from pathlib import Path

ORACLE = Path(__file__).with_name("01_FROZEN_INDEPENDENT_K11_EXPECTATIONS.json")
FROZEN_SHA256 = "091b81c1604f856fb33d4b2da38d1aedf9d0e35b41e0831cdfad84f12fe2f055"


class Refused(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def canonical(v):
    return json.dumps(v, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def digest(v):
    return hashlib.sha256(canonical(v).encode("utf-8")).hexdigest()


def load_oracle():
    data = ORACLE.read_bytes()
    if hashlib.sha256(data).hexdigest() != FROZEN_SHA256:
        raise Refused("FROZEN_ORACLE_CHANGED")
    return json.loads(data)


def when(d):
    return date.fromisoformat(d)


def assert_acyclic(nodes, edges):
    nodes = set(nodes)
    if any(len(e) != 2 or e[0] not in nodes or e[1] not in nodes for e in edges):
        raise Refused("UNKNOWN_OR_MALFORMED_EDGE")
    successors = {n: [] for n in nodes}
    indegree = {n: 0 for n in nodes}
    for source, dest in edges:
        successors[source].append(dest)
        indegree[dest] += 1
    queue = sorted(n for n in nodes if not indegree[n])
    seen = []
    while queue:
        n = queue.pop(0)
        seen.append(n)
        for dest in successors[n]:
            indegree[dest] -= 1
            if indegree[dest] == 0:
                queue.append(dest)
                queue.sort()
    if len(seen) != len(nodes):
        raise Refused("REJECT_CYCLE")
    return seen


def _allowed_fixture(fixture):
    if set(fixture) != {"schema", "grade", "freeze_sequence", "not_claimed", "clock", "graph", "fixed_preconception", "proposals", "oracle", "branching", "policy"}:
        raise Refused("REJECT_CHILD_OUTCOME_LEAKAGE")
    if fixture["policy"] != {"adopted_owner_changed": False, "actor_invocations": 0,
                              "llm_invocations": 0, "original_survey_rows": 0}:
        raise Refused("FORBIDDEN_SIDE_EFFECT_OR_AUTHORITY")


def _validate_history(actor, checkpoint):
    if not when(actor["born"]) < when(checkpoint):
        raise Refused("REJECT_AGE")
    last = when(actor["born"])
    for event in actor["history"]:
        current = when(event["date"])
        if current < last or current >= when(checkpoint):
            raise Refused("REJECT_TEMPORAL_ORDER")
        last = current
    if "prior_child" in actor and actor["prior_child"] is not None:
        old = actor["prior_child"]
        if not when(actor["born"]) < when(old["conceived"]) < when(old["born"]) < when(checkpoint):
            raise Refused("REJECT_TEMPORAL_ORDER")
        if (old["conceived"], "older_child_conception") not in {(x["date"], x["event"]) for x in actor["history"]}:
            raise Refused("REJECT_FIXED_HISTORY_MUTATION")
        if (old["born"], "older_child_birth") not in {(x["date"], x["event"]) for x in actor["history"]}:
            raise Refused("REJECT_FIXED_HISTORY_MUTATION")


def _within(day, windows):
    return any(when(lo) <= day <= when(hi) for lo, hi in windows)


def _validate_combo(m, f, proposal, checkpoint):
    conceived = when(proposal["conception"])
    if conceived <= when(checkpoint):
        raise Refused("REJECT_TEMPORAL_ORDER")
    if (conceived - when(m["born"])).days < 18 * 365 or (conceived - when(f["born"])).days < 18 * 365:
        raise Refused("REJECT_AGE")
    if not _within(conceived, m["eligible_windows"]) or not _within(conceived, f["eligible_windows"]):
        raise Refused("REJECT_SUPPORT")
    if proposal["birth_rule_days"] != 280:
        raise Refused("UNISSUED_GESTATION_RULE")
    forecast = conceived + timedelta(days=proposal["birth_rule_days"])
    if forecast <= conceived:
        raise Refused("REJECT_TEMPORAL_ORDER")
    return forecast


def _forward_witness(m, f, prop, checkpoint):
    """An event-order proof for fixed histories, not V3 actor forward replay."""
    forecast = _validate_combo(m, f, prop, checkpoint)
    events = sorted([(when(e["date"]), "M:" + e["event"]) for e in m["history"]] +
                    [(when(e["date"]), "F:" + e["event"]) for e in f["history"]])
    events += [(when(checkpoint), "FIXED_HISTORY_CHECKPOINT"),
               (when(prop["conception"]), "NONCAUSAL_ENDPOINT_FEASIBILITY_CHECK")]
    if events != sorted(events):
        raise Refused("REJECT_TEMPORAL_ORDER")
    return {
        "mother": m["id"], "father": f["id"], "scenario": prop["id"],
        "mother_anchor_sha256": digest(m), "father_anchor_sha256": digest(f),
        "ledger_hash": digest([(e[0].isoformat(), e[1]) for e in events]),
        "forecast_birth_not_an_event": forecast.isoformat(),
        "conception_status": "PENDING_NONCAUSAL_NOT_OCCURRED",
        "CHILD_GENERATED_status": "NOT_ISSUED_NOT_OCCURRED",
        "birth_status": "FORECAST_ONLY_NOT_OCCURRED",
        "history_event_count": len(m["history"]) + len(f["history"]),
    }


def solve(fixture):
    """Enumerate *all* fixed candidate combinations; no selection or re-draw."""
    _allowed_fixture(fixture)
    nodes = fixture["graph"]["nodes"]
    edges = fixture["graph"]["edges"]
    assert_acyclic(nodes, edges)
    for forbidden in fixture["graph"]["forbidden_edges"]:
        if forbidden in edges:
            raise Refused("REJECT_CAUSAL_ORDER_OR_CHILD_OUTCOME")
    original = digest(fixture)
    base = fixture["fixed_preconception"]
    checkpoint = base["checkpoint"]
    mothers = base["mothers"]
    fathers = base["fathers"]
    proposals = fixture["proposals"]
    if len({x["id"] for x in mothers}) != len(mothers) or len({x["id"] for x in fathers}) != len(fathers):
        raise Refused("DUPLICATE_HISTORY_ID")
    if len({x["id"] for x in proposals}) != len(proposals):
        raise Refused("REJECT_CHERRY_PICK")
    for a in mothers + fathers:
        _validate_history(a, checkpoint)
    results = []
    rejected = []
    for m, f, p in itertools.product(mothers, fathers, proposals):
        try:
            results.append(_forward_witness(m, f, p, checkpoint))
        except Refused as error:
            rejected.append({"mother": m["id"], "father": f["id"], "scenario": p["id"], "code": error.code})
    if digest(fixture) != original:
        raise Refused("REJECT_FIXED_HISTORY_MUTATION")
    return {"results": results, "rejected": rejected, "attempts": len(mothers)*len(fathers)*len(proposals),
            "fixture_hash": original, "selection": "NO_DRAW_NO_AUTHORIZED_DOMAIN_POLICY"}


def verify_anchor_preservation(original, attempted):
    if digest(original["fixed_preconception"]) != digest(attempted["fixed_preconception"]):
        raise Refused("REJECT_FIXED_HISTORY_MUTATION")
    return True


def validate_child_event_order(conception, child_generated, birth, child_provenance):
    # Construction fixture only; does not grant or simulate the actual events.
    if not when(conception) <= when(child_generated) <= when(birth) <= when(child_provenance):
        raise Refused("REJECT_TEMPORAL_ORDER")
    return True


def no_unauthorized_decision(weights=None, rule_issued=False):
    if weights is not None and not rule_issued:
        raise Refused("REJECT_UNISSUED_PROBABILITY")
    if not rule_issued:
        return "NO_DRAW_UNISSUED"
    raise Refused("MISSING_IMPLEMENTATION")  # Never implement/adopt ADP020 here.


def reject_target_leakage(candidate):
    banned = {"desired_child", "child_future", "child_trait", "ideal_child", "author_preferred_arc", "post_child_memory"}
    if any(key in candidate for key in banned):
        raise Refused("REJECT_CHILD_OUTCOME_LEAKAGE")
    return True


def check_selection_no_cherry_pick(candidate_set, selected_id, ranking_key=None):
    if ranking_key is not None:
        raise Refused("REJECT_CHERRY_PICK")
    if selected_id not in candidate_set:
        raise Refused("REJECT_SUPPORT")
    return "SELECTED_PENDING_HISTORY_VALIDATION"  # No draw is made.


def survivor_fractions(q, acceptance):
    """Math counterexample only: weights q_i * acceptance_i, NOT a calibrated posterior."""
    if set(q) != set(acceptance):
        raise Refused("MISSING_SELECTION_DENOMINATOR")
    weighted = {k: q[k]*acceptance[k] for k in q}
    z = sum(weighted.values())
    if z <= 0:
        raise Refused("NO_SURVIVORS")
    return {k: weighted[k]/z for k in q}


def main():
    fx = load_oracle()
    result = solve(fx)
    print(json.dumps({"grade":"SOURCEFREE_NO_ACTOR", "oracle_sha256":FROZEN_SHA256,
                      "witnesses":result["results"], "rejections":result["rejected"],
                      "attempts":result["attempts"],"selection":result["selection"]}, indent=2))


if __name__ == "__main__":
    main()
