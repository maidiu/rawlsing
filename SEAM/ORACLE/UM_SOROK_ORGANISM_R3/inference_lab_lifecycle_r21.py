"""R21: event-bound economic accounting of the existing R34 full course.

A descriptive allocation of actual semantic work, NOT a causal estimate of
acquisition savings, or a classification of psychological necessity.
The stage list is the exact R34 owner course, not a new developmental script.
"""
from collections import Counter
from um_sorok_organism.types import digest
from um_sorok_organism.inference_lab import verify_workload, compare_frozen, size
from um_sorok_organism.inference_lab_admission import verify_admissions
from inference_lab_cli import fixture_arms

# Each occurrence is pinned to the original R34 run_course source ordering.
STAGES=(
    ("first_object","father","MAKE_OBJECT"),
    ("reference","father","SPEAK"),
    ("cultural_acquisition","nadia","INSPECT"),
    ("independent_new_object","father","MAKE_OBJECT"),
    ("new_possible_end","nadia","INSPECT"),
    ("material_trial","nadia","INSPECT"),
    ("material_takeup","nadia","INSPECT"),
    ("material_exercise_1","nadia","INSPECT"),
    ("material_exercise_2","nadia","INSPECT"),
    ("material_exercise_3","nadia","INSPECT"),
    ("joint_vocal_source","nadia","SING"),
    ("vocal_genesis","nadia","SING"),
    ("vocal_trial","nadia","SING"),
    ("vocal_takeup","nadia","SING"),
    ("reciprocal_refunction","nadia","SING"),
    ("later_maternal_exercise","mother","ORIENT"),
)
# Diagnostic cases derived from the owner course, subject to owner review.
PILOT=(
    ("cultural_acquisition","nadia","historically_possible_cultural_references"),
    ("new_possible_end","nadia","historically_possible_cross_object_significance"),
    ("material_takeup","nadia","historically_possible_incidental_takeup"),
    ("material_exercise_3","nadia",None),
    ("vocal_takeup","nadia","historically_possible_productive_vocal_takeups"),
    ("reciprocal_refunction","mother","historically_possible_productive_witness_reorganizations"),
    ("later_maternal_exercise","mother",None),
)


def account_course(doc,state,witness):
    p=verify_workload(doc)
    if p["fixture"]!="R34_ACQUIRED_LIFE_F" or p["owner_state_sha256"]!=digest(state):
        raise ValueError("R21_SOURCE_STATE_MISMATCH")
    w=verify_admissions(doc,witness)
    events=[e for e in state["events"] if e["envelope"]["kind"]=="ACTOR_LIFE_TRANSITION"]
    if len(events)!=len(STAGES):raise ValueError("R21_OWNER_COURSE_DRIFT")
    rows=p["rows"];initial=[];groups=[];pending=[]
    for row in rows:
        if row["task"]=="adult_constructor":
            if groups or pending:raise ValueError("R21_LATE_CONSTRUCTOR")
            initial.append(row);continue
        pending.append(row)
        if row["task"]=="expression":
            groups.append(pending);pending=[]
    if pending or len(groups)!=len(events):raise ValueError("R21_CALL_EVENT_COVERAGE")
    comparison=compare_frozen(doc,fixture_arms(doc),sequence_ids=list(range(len(rows))))
    metrics={}
    for item in comparison["observations"]:
        if item["outcome"]!="PROPOSAL_RETURNED" or not item["equals_recorded_proposal"]:
            raise ValueError("R21_EXACT_COMPARISON_FAILED")
        metrics[(item["seq"],item["arm"])]=item["metric"]["request_bytes"]
    def totals(rs):
        return {"calls":len(rs),"by_task":dict(Counter(r["task"] for r in rs)),
                "raw_packet_bytes":sum(size(r["packet"]) for r in rs),
                "F_wire_bytes":sum(metrics[r["seq"],"F"] for r in rs),
                "E_wire_bytes":sum(metrics[r["seq"],"E"] for r in rs),
                "development_candidate_count":sum(len(r["proposal"]["candidates"])
                    for r in rs if r["task"]=="development"),
                "provider_tokens":None}
    output=[];pilot=[];used=set()
    for (name,actor,operation),event,rs in zip(STAGES,events,groups):
        payload=event["envelope"]["payload"]
        if (payload["attempt"]["actor"],payload["attempt"]["action"])!=(actor,operation):
            raise ValueError("R21_OWNER_OPERATION_DRIFT")
        if rs[-1]["packet"]["actor_id"]!=actor:raise ValueError("R21_EXPRESSION_ACTOR_MISMATCH")
        dev=[r for r in rs if r["task"]=="development"]
        if not dev:raise ValueError("R21_EVENT_WITHOUT_DEVELOPMENT")
        for r in dev:
            v=w[r["seq"]];aid=r["packet"]["actor"]["id"]
            if (v["committed_event_id"]!=event["id"] or v["event_ref"]!=payload["objective_ref"]
                    or v["effects"]!=payload["developmental_effects"][aid]
                    or aid not in payload["private_actor_experience_receipts"]
                    or v["experience_digest"]!=digest(payload["private_actor_experience_receipts"][aid])):
                raise ValueError("R21_EVENT_WITNESS_MISMATCH")
            used.add(r["seq"])
        output.append({"stage":name,"event_id":event["id"],"principal":actor,
            "operation":operation,"clock":dev[0]["packet"]["clock"],
            "sequence_ids":[r["seq"] for r in rs],**totals(rs)})
        for stage,aid,family in PILOT:
            if stage!=name:continue
            candidates=[r for r in dev if r["packet"]["actor"]["id"]==aid
                        and (family is None or r["packet"].get(family))]
            if len(candidates)!=1:raise ValueError("R21_PILOT_CASE_DRIFT:"+name)
            r=candidates[0]
            pilot.append({"stage":name,"actor":aid,"family":family,"seq":r["seq"],
                          "packet_digest":r["packet_digest"],"event_id":event["id"]})
    if used!=set(w) or len(pilot)!=len(PILOT):raise ValueError("R21_WITNESS_OR_PILOT_COVERAGE")
    return {"schema":"R21_R34_ACTUAL_EVENT_BOUND_ECONOMY_V1",
            "source_head":p["source_head"],"workload_sha256":doc["sha256"],
            "owner_state_sha256":p["owner_state_sha256"],"initialization":totals(initial),
            "stages":output,"total":totals(rows),"pilot_cases":pilot,
            "scope":"HERMETIC_DESCRIPTIVE_NOT_CAUSAL_OR_LIVE","network_calls":0}
