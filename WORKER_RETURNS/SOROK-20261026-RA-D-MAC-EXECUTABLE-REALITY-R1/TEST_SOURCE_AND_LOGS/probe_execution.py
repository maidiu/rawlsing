"""RA-D sourcefree execution probe for S39/S44/S48/S51/S52.

No provider call, no accepted-source edit, no raw data. Every output is from
the exact S52-cut archive, G18, JOIN-E and language-mediation source identities
recorded in import_manifest.json / SOURCE_INDEX.json.
"""
from __future__ import annotations
import hashlib, json, sys, tempfile
from pathlib import Path
from typing import Any

RETURN = Path(__file__).resolve().parent
ARCHIVE = RETURN / "isolated_archive_s52c821"
S52_DIR = ARCHIVE / "WORKER_RETURNS" / "SOROK-20261025-S52-PAID-ACTIVITY-REPERTOIRE-R1"
S48_DIR = ARCHIVE / "WORKER_RETURNS" / "SOROK-20261025-S48-ONE-CALL-CONTINUING-TURN-R1"
S39_DIR = ARCHIVE / "WORKER_RETURNS" / "SOROK-20261024-S39-GENERATED-RESPONSE-R1"
for path in (S52_DIR, S48_DIR, S39_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))
from s52.bootstrap import install  # noqa: E402
install()
from s45.fixtures import root_bundle  # noqa: E402
from s37.harness import case_for, source_for  # noqa: E402
from s52.session import S52Session  # noqa: E402
from s48.session import S48Session  # noqa: E402
from s48.sources import candidate_specs  # noqa: E402
from lab_sgi1.history import replay_history  # noqa: E402

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def actor_state(session) -> dict:
    return dict((session.world().actor_state or {}).get("B") or {})

def event_table(events: list[dict]) -> list[dict]:
    return [
        {"effective_index": e.get("effective_index"), "kind": e.get("kind"),
         "event_id": e.get("event_id"), "owner_id": e.get("owner_id"),
         "parents": list(e.get("causal_parent_event_ids") or [])}
        for e in events
    ]

def start_s52():
    state = Path(tempfile.mkdtemp(prefix="ra-d-s52-"))
    case = case_for(True)
    return S52Session.start(
        state, bundle=root_bundle("01" * 32), case=case,
        source=source_for(case), language_context={"milieu_id": "workshop"},
    )

s52 = start_s52()
try:
    life = s52.product.seed.life
    b_events = list(life.b_events or [])
    replay = replay_history(b_events)
    striving = next(e for e in b_events if e.get("kind") == "STRIVING")
    witness = next(w for w in replay["value_witnesses"] if w["event_id"] == striving["event_id"])
    route_usage = [
        {"event_id": e["event_id"], "route": (e.get("payload") or {}).get("route"),
         "effect": replay["effects"][e["event_id"]]}
        for e in b_events
        if e.get("kind") == "ROUTE_AVAILABILITY"
        and (replay["effects"].get(e["event_id"]) or {}).get("goal") == striving["payload"]["striving"]
    ]
    root = s52.read_root()
    current_b = actor_state(s52)

    obj = s52.recover_object()
    hyp = s52.declare_hypothesis(obj)
    offer = s52.issue_offer()
    access = s52._offer_access(offer)
    relevance = s52.evaluate(obj, hyp, offer, access)
    generation = s52.consume_generation(obj, hyp, offer, access, relevance)
    candidate = generation["candidate"]
    receipt = generation.get("generation_receipt") or {}
    before_action = actor_state(s52)
    denied = s52.perform_paid_participation(candidate, generation=generation, counterpart_performed=False)
    performed = s52.perform_paid_participation(candidate, generation=generation, counterpart_performed=True)
    after_action = actor_state(s52)

    def last_generation_receipt(session):
        turns = [row for row in session._episodes("S49_B_ACTOR_TURN")
                 if (row.get("body") or {}).get("generation")]
        return ((turns[-1].get("body") or {}).get("generation") or {}).get("generation") or {}

    def options_of(session):
        return [o.get("option_id") for o in last_generation_receipt(session).get("options", [])]

    s52.produce_b_turn(controlled=True, source_records_override=[])
    no_source_options = options_of(s52)
    s52.produce_b_turn(controlled=True, source_records_override=[candidate["source"]])
    source_only_options = options_of(s52)
    s52.produce_b_turn(controlled=True, source_records_override=[candidate["source"]],
                       repertoire=candidate["repertoire"])
    source_plus_repertoire_options = options_of(s52)

    # Later-event material consumer: repeat lawful controlled tasks until no free hours.
    sequence = []
    for i in range(10):
        run = s52.run_experiment()
        cand = run["candidate"]
        free = actor_state(s52).get("free_hours")
        sequence.append({"iteration": i + 1, "free_hours": free,
                         "relation": run["relevance"].get("relation"),
                         "candidate_status": cand.get("status"),
                         "reason": cand.get("reason")})
        if cand.get("status") in {"CONDITIONAL_ON_INDEPENDENT_PARTICIPATION", "FEASIBLE"}:
            s52.perform_paid_participation(cand, generation=run["generation"],
                                           counterpart_performed=True)
    final = s52.run_experiment()
    final_candidate = final["candidate"]
    final_receipt = final["generation"].get("generation_receipt") or {}
    verify = s52.verify()
finally:
    s52.close()

# S48 source-owner hold / SCI05 probe, fake product runner only.
def start_s48():
    state = Path(tempfile.mkdtemp(prefix="ra-d-s48-"))
    case = case_for(True)
    return S48Session.start(state, bundle=root_bundle("01" * 32), case=case,
                            source=source_for(case),
                            language_context={"milieu_id": "workshop"})

def envelope(candidate="OTHER_REFUSES_TOOL", self_account=None):
    return {"schema": "S48_PRODUCT_ENVELOPE@1",
            "narrative": "The prior turn is retained.",
            "self_account": self_account,
            "self_account_present": bool(self_account),
            "prospective": ([{"candidate_id": candidate, "rationale": "fixture"}]
                            if candidate else [])}

def fake_runner(env, calls):
    def run(prompt, *, workdir, log_dir, timeout):
        calls.append(1)
        return {"status": "OK", "envelope": dict(env),
                "call_receipt": {"actual_provider_call": False,
                                 "provider_call_count": 1, "step_count": 1},
                "prompt_hash": "fixture"}
    return run

s48 = start_s48()
try:
    calls = []
    hold = s48.run_turn(product_runner=fake_runner(envelope(), calls))
    s48_candidate_specs = candidate_specs(s48)
finally:
    s48.close()
s48b = start_s48()
try:
    calls2 = []
    sci = s48b.run_turn(product_runner=fake_runner(envelope(self_account="a proposed self-account"), calls2))
finally:
    s48b.close()

# S39 direct controls using the accepted producer seam.
from s39.producer import GeneratedProducer
from s39.sources import context_records
producer = GeneratedProducer(Path(tempfile.mkdtemp(prefix="ra-d-s39-")) / "source",
                             case=case_for(True), source=source_for(case_for(True)))
producer.stage_m35()
try:
    def rec(**flags):
        return context_records(actor_id=producer.occurrence.actor_id,
                               branch_id="first_session", as_of=producer.as_of, **flags)
    s39_cases = {}
    for name, flags in {
        "baseline": dict(repair_urgent=True, avoid_debt=True, prior_b_share=True),
        "labels": dict(repair_urgent=True, avoid_debt=True, prior_b_share=True,
                       labels={"class": "X", "Enneagram": "Y"}),
        "prefer_independent": dict(avoid_debt=True, prefer_independent=True),
        "prior_b_refusal": dict(prior_b_refusal=True),
        "none": dict(),
        "cycle": dict(repair_urgent=True, avoid_debt=True, prior_b_share=True,
                      prefer_independent=True, prior_b_refusal=True),
    }.items():
        r = producer.generate(source_records=rec(**flags))
        s39_cases[name] = {
            "selection_status": r.get("selection_status"),
            "selected_option": r.get("selected_option"),
            "unresolved_reason": r.get("unresolved_reason"),
            "ignored_label_count": r.get("ignored_label_count"),
            "source_refs": r.get("source_refs"),
            "supporting": [x["predicate"] for x in r.get("supporting_reasons", [])],
            "contrary": [x["predicate"] for x in r.get("contrary_reasons", [])],
        }
finally:
    producer.close()

report = {
    "schema": "RA_D_CAUSAL_PROBE_RESULT@1",
    "grade": "TEST_ONLY_SOURCEFREE_S52_CUT_NOT_NATIVE",
    "provider_calls": 0,
    "root": {
        "root_hash": root.get("root_hash"),
        "root_id": root.get("root_id"),
        "actor_ids": root.get("actor_ids"),
        "source_hashes": root.get("source_hashes"),
        "g18_history_hashes": root.get("g18_history_hashes"),
        "snapshot_hashes": root.get("snapshot_hashes"),
        "b_events": event_table(b_events),
        "historical_replay_valid": replay.get("valid"),
        "historical_replay_errors": replay.get("errors"),
        "historical_state": replay.get("state"),
        "striving_event_id": striving.get("event_id"),
        "striving_value": (striving.get("payload") or {}).get("striving"),
        "striving_parents": list(striving.get("causal_parent_event_ids") or []),
        "striving_witness": witness,
        "route_usage": route_usage,
    },
    "current_b_state_before": current_b,
    "recovered_object": obj,
    "hypothesis": {k: hyp.get(k) for k in (
        "hypothesis_id", "object_event_id", "object_striving", "scope",
        "actual_current_purpose_proved", "native", "psychology_claim",
        "actor_testimony", "grade")},
    "offer": {
        "offer_event_id": offer.get("offer_event_id"),
        "world_event_id": offer.get("world_event_id"),
        "payment_per_actor": (offer.get("offer") or {}).get("payment_per_actor"),
        "task_hours": (offer.get("offer") or {}).get("task_hours"),
        "permit": (offer.get("offer") or {}).get("permit"),
        "place": (offer.get("offer") or {}).get("place"),
    },
    "access": {
        "access_status": (access or {}).get("access_status"),
        "source_ref": (access or {}).get("source_ref"),
        "actor_id": (access or {}).get("actor_id"),
    },
    "relevance": {k: relevance.get(k) for k in (
        "status", "relation", "actor_free_hours", "financial",
        "object_event_id", "object_striving", "actual_current_purpose_proved",
        "hypothesis_id", "native", "reasons", "selected_action", "performed")},
    "generation": {
        "selection_status": receipt.get("selection_status"),
        "selected_option": receipt.get("selected_option"),
        "unresolved_reason": receipt.get("unresolved_reason"),
        "eligible_options": receipt.get("eligible_options"),
        "defeated_pairs": receipt.get("defeated_pairs"),
        "undominated_options": receipt.get("undominated_options"),
        "options": receipt.get("options"),
        "paid_reasons": [x for x in receipt.get("reasons", [])
                         if x.get("option_id") == "PAID_PARTICIPATION"],
        "source_refs": receipt.get("source_refs"),
    },
    "candidate": {k: candidate.get(k) for k in (
        "candidate_hash", "status", "reason", "recruited",
        "counterpart_status", "prospective_payment", "earned_payment",
        "capability_readset", "performed", "native", "psychology_claim",
        "actual_current_purpose_proved")},
    "controlled_action": {
        "denied": {k: denied.get(k) for k in ("status", "performed", "reason")},
        "performed": {k: performed.get(k) for k in (
            "status", "performed", "reason", "payment_earned", "world_event_id")},
        "before": before_action,
        "after": after_action,
        "state_changed": {
            "cash": after_action.get("cash") != before_action.get("cash"),
            "free_hours": after_action.get("free_hours") != before_action.get("free_hours"),
            "completed_units": after_action.get("completed_units") != before_action.get("completed_units"),
        },
    },
    "source_cut": {
        "no_source_options": no_source_options,
        "source_only_options": source_only_options,
        "source_plus_repertoire_options": source_plus_repertoire_options,
        "paid_absent_without_source": "PAID_PARTICIPATION" not in no_source_options,
        "paid_absent_without_repertoire": "PAID_PARTICIPATION" not in source_only_options,
        "paid_present_with_both": "PAID_PARTICIPATION" in source_plus_repertoire_options,
    },
    "later_material_consumer": {
        "iterations": sequence,
        "final_free_hours": actor_state(s52) if False else final["relevance"].get("actor_free_hours"),
        "final_relation": final["relevance"].get("relation"),
        "final_candidate_status": final_candidate.get("status"),
        "final_candidate_reason": final_candidate.get("reason"),
        "final_eligible_options": final_receipt.get("eligible_options"),
        "paid_absent": "PAID_PARTICIPATION" not in (final_receipt.get("eligible_options") or []),
        "verify_ok": verify.get("ok"),
    },
    "s48": {
        "source_owner_hold": {k: hold.get(k) for k in (
            "status", "reason", "missing_function", "event_ref",
            "provider_call_count")},
        "candidate_specs": s48_candidate_specs,
        "nonempty_self_account": {k: sci.get(k) for k in (
            "status", "reason", "event_ref", "provider_call_count")},
    },
    "s39_controls": s39_cases,
    "batch_implementation": {
        "source_search": "no 3-5-event batch/sequential-realization/retrospective-half implementation in the S39-S52 source closure",
        "s48_prospective_bound": "S48 accepts at most one prospective candidate and allowed_prospective_candidates is empty",
    },
}
print(json.dumps(report, indent=2, sort_keys=True))
