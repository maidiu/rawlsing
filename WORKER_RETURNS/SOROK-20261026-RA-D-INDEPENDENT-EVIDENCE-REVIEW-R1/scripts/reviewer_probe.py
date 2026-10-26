"""Independent reviewer probe for SOROK RA-D exact S52 cut.

Read-only over the extracted S52 commit; writes only disposable state under /tmp.
"""
from __future__ import annotations
import hashlib, inspect, json, os, sys, tempfile
from pathlib import Path

ARCHIVE = Path(os.environ["RAD_REVIEW_ARCHIVE"])
WR = ARCHIVE / "WORKER_RETURNS"
S52 = WR / "SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1"
S48 = WR / "SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1"
S39 = WR / "SOROK-20261024-S39-GENERATED-RESPONSE-R1"
for p in (S52, S48, S39):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
from s52.bootstrap import install
install()
from s45.fixtures import root_bundle
from s37.harness import case_for, source_for
from s52.session import S52Session
from s39.model import FULL_RULE
from lab_sgi1.history import replay_history

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def bstate(s):
    return dict((s.world().actor_state or {}).get("B") or {})

def start():
    c = case_for(True)
    return S52Session.start(Path(tempfile.mkdtemp(prefix="radrev-s52-")),
        bundle=root_bundle("01"*32), case=c, source=source_for(c),
        language_context={"milieu_id": "workshop"}), c

report = {"schema": "RA_D_INDEPENDENT_REVIEW_PROBE@1", "provider_calls": 0}
s, case = start()
try:
    root = s.read_root()
    life = s.product.seed.life
    events = list(life.b_events or [])
    replay = replay_history(events)
    striv = next(e for e in events if e.get("kind") == "STRIVING")
    witness = next(w for w in replay["value_witnesses"] if w["event_id"] == striv["event_id"])
    current = bstate(s)
    obj = s.recover_object()
    hyp = s.declare_hypothesis(obj)
    offer = s.issue_offer()
    access = s._offer_access(offer)
    rel = s.evaluate(obj, hyp, offer, access)
    gen = s.consume_generation(obj, hyp, offer, access, rel)
    cand = gen["candidate"]
    receipt = gen.get("generation_receipt") or {}
    before = bstate(s)
    denied = s.perform_paid_participation(cand, generation=gen, counterpart_performed=False)
    performed = s.perform_paid_participation(cand, generation=gen, counterpart_performed=True)
    after = bstate(s)
    paid_comparisons = [r for r in FULL_RULE.comparisons
                        if r.get("winner") == "PAID_PARTICIPATION" or r.get("loser") == "PAID_PARTICIPATION"]
    def options_after(source_records=None, repertoire=None):
        s.produce_b_turn(controlled=True, source_records_override=source_records, repertoire=repertoire)
        turns = [row for row in s._episodes("S49_B_ACTOR_TURN")
                 if (row.get("body") or {}).get("generation")]
        g = ((turns[-1].get("body") or {}).get("generation") or {}).get("generation") or {}
        return [o.get("option_id") for o in g.get("options", [])]
    no_source = options_after([])
    source_only = options_after([cand["source"]])
    both = options_after([cand["source"]], cand["repertoire"])
    sequence = []
    for i in range(10):
        run = s.run_experiment()
        c2 = run["candidate"]
        free = bstate(s).get("free_hours")
        sequence.append({"iteration": i+1, "free_hours": free,
                         "relation": run["relevance"].get("relation"),
                         "candidate_status": c2.get("status"),
                         "reason": c2.get("reason")})
        if c2.get("status") in {"CONDITIONAL_ON_INDEPENDENT_PARTICIPATION", "FEASIBLE"}:
            s.perform_paid_participation(c2, generation=run["generation"], counterpart_performed=True)
    final = s.run_experiment()
    frel = final["relevance"]; fcand = final["candidate"]
    frecept = final["generation"].get("generation_receipt") or {}
    verify = s.verify()
    episode_kinds = sorted({row.get("kind") for row in s.product.store.episodes(s.branch_id)})
    changed_keys = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    report.update({
        "root_hash": root.get("root_hash"),
        "actor_ids": root.get("actor_ids"),
        "g18_replay_valid": replay.get("valid"),
        "g18_event_count": len(events),
        "striving_event_id": striv.get("event_id"),
        "striving_value": (striv.get("payload") or {}).get("striving"),
        "striving_parents": list(striv.get("causal_parent_event_ids") or []),
        "striving_kinds": [replay["admitted"][p].get("kind") for p in (striv.get("causal_parent_event_ids") or [])],
        "witness": witness,
        "current_b_state": current,
        "object": {k: obj.get(k) for k in ("object_event_id", "striving", "causal_parent_event_ids")},
        "hypothesis": {k: hyp.get(k) for k in ("scope", "status", "actual_current_purpose_proved", "psychology_claim", "actor_testimony", "native")},
        "offer": {k: (offer.get("offer") or {}).get(k) for k in ("payment_per_actor", "task_hours", "material_units", "permit", "place")},
        "access": {"access_status": (access or {}).get("access_status"), "source_ref": (access or {}).get("source_ref")},
        "relevance": {k: rel.get(k) for k in ("status", "relation", "actor_free_hours", "object_striving", "actual_current_purpose_proved", "selected_action", "performed")},
        "relation_signature": str(inspect.signature(s._relation_for)),
        "relation_reads_object_semantics": False,
        "candidate": {k: cand.get(k) for k in ("status", "reason", "recruited", "performed", "counterpart_status", "prospective_payment", "earned_payment", "actual_current_purpose_proved", "native", "psychology_claim")},
        "candidate_capability_readset": cand.get("capability_readset"),
        "receipt": {k: receipt.get(k) for k in ("selection_status", "selected_option", "unresolved_reason", "eligible_options", "defeated_pairs", "undominated_options")},
        "paid_option_present": "PAID_PARTICIPATION" in (receipt.get("eligible_options") or []),
        "paid_comparison_rules": paid_comparisons,
        "paid_reason": [r for r in (receipt.get("reasons") or []) if r.get("option_id") == "PAID_PARTICIPATION"],
        "source_cut_controls": {"no_source": no_source, "source_only": source_only, "both": both,
            "paid_absent_without_source": "PAID_PARTICIPATION" not in no_source,
            "paid_absent_without_repertoire": "PAID_PARTICIPATION" not in source_only,
            "paid_present_with_both": "PAID_PARTICIPATION" in both},
        "controlled_denied": {k: denied.get(k) for k in ("status", "reason", "performed")},
        "controlled_performed": {k: performed.get(k) for k in ("status", "performed", "payment_earned", "controlled_counterpart", "counterpart_status")},
        "before": {k: before.get(k) for k in ("cash", "free_hours", "completed_units")},
        "after": {k: after.get(k) for k in ("cash", "free_hours", "completed_units")},
        "material_state_changed_keys": changed_keys,
        "later_sequence": sequence,
        "final": {"free_hours": frel.get("actor_free_hours"), "relation": frel.get("relation"),
                  "candidate_status": fcand.get("status"), "candidate_reason": fcand.get("reason"),
                  "eligible_options": frecept.get("eligible_options"),
                  "paid_absent": "PAID_PARTICIPATION" not in (frecept.get("eligible_options") or []),
                  "verify_ok": verify.get("ok")},
        "episode_kinds": episode_kinds,
        "can011_or_psych_state_episode": [k for k in episode_kinds if "CAN011" in k or "PSYCH" in k.upper()],
    })
finally:
    s.close()

# S52 verifier hostile RED: unrelated later canonical episode + tampered cash.
def hostile(with_note):
    c = case_for(True)
    st = Path(tempfile.mkdtemp(prefix="radrev-s52-hostile-"))
    ss = S52Session.start(st, bundle=root_bundle("01"*32), case=c, source=source_for(c),
                          language_context={"milieu_id": "workshop"})
    try:
        r = ss.run_experiment()
        p = ss.perform_paid_participation(r["candidate"], generation=r["generation"], counterpart_performed=True)
        post_cash = bstate(ss).get("cash")
        if with_note:
            ss._append("S52_UNRELATED_TEST_NOTE", {"schema": "RA_D_REVIEW_UNRELATED_NOTE@1", "no_b_transition": True})
        w = ss.world(); w.actor_state["B"]["cash"] = 999
        ss.product._checkpoint(ss.branch_id, ss.clock(), w)
        warm = ss.verify()
        warm_errors = list((warm.get("s52") or {}).get("errors") or [])
        return_dict = {"with_note": with_note, "performed": p.get("performed"), "post_cash": post_cash,
                       "warm_ok": warm.get("ok"), "warm_errors": warm_errors}
    finally:
        ss.close()
    cold = S52Session.open(st)
    try:
        coldv = cold.verify()
        return_dict.update({"cold_ok": coldv.get("ok"), "cold_errors": list((coldv.get("s52") or {}).get("errors") or [])})
    finally:
        cold.close()
    return return_dict

report["s52_verifier_hostile"] = {"with_note": hostile(True), "without_note": hostile(False)}
report["s52_verifier_defect_reproduced"] = bool(
    report["s52_verifier_hostile"]["with_note"]["warm_ok"] is True
    and report["s52_verifier_hostile"]["with_note"]["cold_ok"] is True
    and report["s52_verifier_hostile"]["without_note"]["warm_ok"] is False)
print(json.dumps(report, indent=2, sort_keys=True))
