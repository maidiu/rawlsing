"""P2 recursion -> modern continuing organism, provisional sourcefree owner port.

The inherited RecursionCycle/BatchEngine still own call custody, order and
interruption holds. ConstitutiveRuntime still owns every actual world/actor
transition. A checkpoint proposes conditional actor-local policies, never
world outcomes or pre-issued future references. No remote call inside a step.
"""
from collections import Counter
import fcntl
import json
from math import isfinite
from pathlib import Path
import sqlite3
import sys
from time import perf_counter_ns

P2 = Path(__file__).resolve().parents[3] / "WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
if str(P2) not in sys.path:
    sys.path.insert(0, str(P2))
from developmental_recursion.contracts import (
    StateIdentity, RealizedEvent, RecursionRefusal, canonical, detached, digest)
from developmental_recursion.engine import BatchEngine
from developmental_recursion.model_cycle import RecursionCycle
from um_sorok_organism.semantics import HeuristicSemanticProvider, ValidatingSemanticService
from um_sorok_organism.historical_parent_bridge import (
    FAMILY_SOURCE, situated_family_pathways, family_encounter_evidence)
from um_sorok_organism.plural_care_paths import choose_one_grounded_plural_acquisition
from um_sorok_organism.relational_metabolism import RELATIONS, POLARITIES

GRADE = "PROVISIONAL_SOURCEFREE_MODERN_GENERATION_PORT_NOT_NATIVE_OR_MODEL_ADEQUACY"
MAX_TEXT = 512
MAX_POLICY_ITEMS = 24
# Existing native fields, not a new psychological schema.
ANALYTIC_DOMAINS = (
    "forms","links","projects","activity_links","composition_methods","relational_motifs",
    "possible_ends","functional_bindings","historical_orientations","self_model",
    "expectations","memories","co_regulation_orientations","joint_practices",
    "care_practical_commitments","cultural_reference_practices","vocal_coordination_practices",
    "material_investments","power_exercises","lived_genesis_episodes","evidence_paths",
    "activity_history","participation_history","notice_exposures","object_encounters",
    "practice_exposures","undergone_care_periods","experienced_care_events",
    "performed_feeding_events","institutional_expectations","material_dependency_encounters",
    "labor_dependency_encounters","care_contribution_episodes","cultural_demonstrations",
    "vocal_turn_experiences","traces","other_models","history_refs")
MAX_ANALYTIC_READS = 12
MAX_ANALYTIC_BYTES = 256*1024
MAX_DOMAIN_PAGE=32
RECENT_ACCESSIBLE_MEMORY=16

def exact_domain_rows(value):
    """Derived handles, not a second store or a claim of conscious access."""
    if isinstance(value,dict):
        return [("key:"+k,v) for k,v in sorted(value.items())]
    require(isinstance(value,list),"GEN_ROW_DOMAIN_NOT_COLLECTION")
    return [("id:"+v["id"] if isinstance(v,dict) and text(v.get("id"),512)
             else "digest:"+digest(v),v) for v in value]

def latest_native_event(runtime):
    # Joined owner provides a public bounded tail read. Preserve compatibility
    # with R63 without requiring or modifying its private storage methods.
    fn=getattr(runtime.ledger,"latest_event",None)
    return fn() if callable(fn) else runtime.ledger.events()[-1]

def require(ok, code):
    if not ok:
        raise RecursionRefusal(code)

def text(value, limit=MAX_TEXT):
    return isinstance(value,str) and bool(value.strip()) and len(value)<=limit

def exact_keys(value, required, optional=()):
    return isinstance(value,dict) and set(required)<=set(value)<=set(required)|set(optional)

def subset(row, match):
    return isinstance(row,dict) and all(k in row and (subset(row[k],v) if isinstance(v,dict) else row[k]==v) for k,v in match.items())

def policy_check(policy):
    require(exact_keys(policy,(),("actions","formation","expression","private_rehearsal")),"GEN_POLICY_SHAPE")
    if "private_rehearsal" in policy:
        r=policy["private_rehearsal"]
        require(exact_keys(r,("affect","meaning"),("memory_event_ref","memory_ref","affect_ref")) and
                r["affect"] in ("REQUIRED","NONE") and text(r["meaning"]) and
                all(text(r[k]) for k in ("memory_event_ref","memory_ref","affect_ref") if k in r) and
                ("affect_ref" not in r or r["affect"]=="REQUIRED"),"GEN_PRIVATE_REHEARSAL_POLICY")
    actions=policy.get("actions",[])
    require(isinstance(actions,list) and len(actions)<=MAX_POLICY_ITEMS,"GEN_ACTION_POLICY_SIZE")
    for rule in actions:
        require(exact_keys(rule,("action",),("option_match","project_id","speech_intent","rank_by","pool","project_course_actions","current_match","exclude_affect")) and
                text(rule["action"],80),"GEN_ACTION_RULE")
        if "option_match" in rule:
            require(isinstance(rule["option_match"],dict) and bool(rule["option_match"]) and
                    set(rule["option_match"])<= {"project_id","world_request","binding_status",
                                               "grounds_status","operation","source_material_object_ref","genesis_family","productive_witness_attention","cross_object_attention_analytic_only","possible_end_ref","private_rehearsal_ref"},
                    "GEN_ACTION_MATCH")
        if "current_match" in rule:
            m=rule["current_match"]
            require(isinstance(m,dict) and bool(m) and set(m)<={"action","kind","ref"} and
                    all(text(v,120) for v in m.values()),"GEN_CURRENT_MATCH")
        if "exclude_affect" in rule:
            m=rule["exclude_affect"]
            require("option_match" in rule and rule.get("pool","practical_options")=="practical_options" and
                    exact_keys(m,("course_orientation",),("basis",)) and
                    m["course_orientation"] in ("APPROACH","WITHHOLD") and
                    ("basis" not in m or (exact_keys(m["basis"],("formation_source",)) and
                        text(m["basis"]["formation_source"],100))),"GEN_AFFECT_EXCLUSION")
        if "project_course_actions" in rule:
            require(rule["action"]=="SELECT_HIGHEST_CURRENT_PROJECT_COURSE" and
                    isinstance(rule["project_course_actions"],list) and 1<=len(rule["project_course_actions"])<=12
                    and all(text(v,80) for v in rule["project_course_actions"]) and
                    set(rule)=={"action","project_course_actions"},"GEN_PROJECT_COURSE_RANK")
        if "pool" in rule:
            require(rule["pool"] in ("practical_options","addressed_lexical_options","possible_end_trials") and
                    "option_match" in rule,"GEN_ACTION_POOL")
            if rule["pool"]=="addressed_lexical_options":
                require(rule["action"]=="SPEAK" and text(rule.get("speech_intent"),500),"GEN_LEXICAL_ADDRESS_INTENT")
            if rule["pool"]=="possible_end_trials":
                require("speech_intent" not in rule and "project_id" not in rule,"GEN_TRIAL_POLICY")
        if "rank_by" in rule:
            require(rule["rank_by"]=="LATEST_PERSONALLY_SENSED_REGULATION" and
                    rule["action"]=="SIGNAL" and
                    rule.get("option_match",{}).get("grounds_status")=="HISTORICALLY_ACQUIRED_CO_REGULATION",
                    "GEN_REGULATION_RANK_SCOPE")
        if "project_id" in rule:
            require(rule["project_id"] is None or text(rule["project_id"]),"GEN_PROJECT_REF")
        if "speech_intent" in rule:
            require(rule["action"]=="SPEAK" and text(rule["speech_intent"],500),"GEN_SPEECH_INTENT")
    if "expression" in policy:
        require(exact_keys(policy["expression"],(),("speech","surface")) and
                all(text(v,500) for v in policy["expression"].values()),"GEN_EXPRESSION_POLICY")
    formation=policy.get("formation",{"base":"LOCAL","rules":[]})
    require(exact_keys(formation,("base","rules")) and formation["base"] in ("LOCAL","NONE") and
            isinstance(formation["rules"],list) and len(formation["rules"])<=MAX_POLICY_ITEMS,
            "GEN_FORMATION_POLICY")
    for rule in formation["rules"]:
        if exact_keys(rule,("private_construct","augment"),("match",)):
            kind=rule["private_construct"];v=rule["augment"];m=rule.get("match",{})
            require(isinstance(m,dict) and set(m)<={"private_affect_ref","possible_end_ref","possible_object"} and
                    all(text(x) for x in m.values()),"GEN_PRIVATE_CONSTRUCT_MATCH")
            require(kind in ("NOTICE_END","TAKE_UP_END"),"GEN_PRIVATE_CONSTRUCT_KIND")
            require(exact_keys(v,("possible_object","means") if kind=="NOTICE_END" else ("means",)) and
                    ("possible_object" not in v or text(v["possible_object"])) and
                    isinstance(v["means"],list) and 1<=len(v["means"])<=3 and
                    all(x in ("REST","ORIENT","EAT") for x in v["means"]) and
                    len(set(v["means"]))==len(v["means"]),"GEN_PRIVATE_CONSTRUCT_MEANING")
        elif exact_keys(rule,("candidate",),("when",)):
            c=rule["candidate"]
            require(isinstance(c,dict) and c.get("kind") in
                    ("MEMORY","ACQUIRE_HISTORICAL_ORIENTATION"),"GEN_DIRECT_KIND")
            if c["kind"]=="MEMORY":
                require(exact_keys(c,("kind","content","cue_terms")) and text(c["content"]) and
                        isinstance(c["cue_terms"],list) and 1<=len(c["cue_terms"])<=12 and
                        all(text(v,80) for v in c["cue_terms"]),"GEN_DIRECT_MEMORY")
            else:
                require(exact_keys(c,("kind","operation","orientation_mode")) and
                        text(c["operation"],80) and c["orientation_mode"] in ("APPROACH","WITHHOLD"),
                        "GEN_DIRECT_ORIENTATION")
            require(isinstance(rule.get("when",{}),dict) and
                    set(rule.get("when",{}))<= {"own_action","status","participated"},
                    "GEN_DIRECT_CONDITION")
        else:
            require(exact_keys(rule,("offer",),("match","augment","resolver","construct")) and
                    isinstance(rule["offer"],str) and
                    rule["offer"].startswith(("historically_possible_","historically_proposed_")) and
                    isinstance(rule.get("match",{}),dict) and isinstance(rule.get("augment",{}),dict),
                    "GEN_NOMINATION_RULE")
            if "resolver" in rule:
                require(rule["offer"]=="historically_possible_plural_care" and
                        rule["resolver"]=="EXISTING_PLURAL_CARE_SOURCE_RESOLUTION" and
                        not rule.get("augment"),"GEN_RESOLVER_SCOPE")
            if "construct" in rule:
                require(rule["construct"] in (*TYPED_FORMATION_OFFERS,"LEXICAL_PROJECT_REVALUATION","CROSS_OBJECT_POSSIBLE_END","INCIDENTAL_END_TAKEUP")
                        and not rule.get("resolver"),"GEN_TYPED_CONSTRUCTION")
                require(rule["offer"] in TYPED_FORMATION_OFFERS.get(rule["construct"],()) or rule["offer"]=={"LEXICAL_PROJECT_REVALUATION":"historically_possible_lexical_project_revaluations",
                    "CROSS_OBJECT_POSSIBLE_END":"historically_possible_cross_object_significance",
                    "INCIDENTAL_END_TAKEUP":"historically_possible_incidental_takeup"}.get(rule["construct"]),
                    "GEN_TYPED_CONSTRUCTION_OFFER")
            # Only semantic fields, never an invented source ref or owner basis.
            allowed={"interpretive_hypothesis","personal_significance","personal_sense",
                     "affect_name","course_orientation","priority","anticipated_availability",
                     "revision","new_relation","new_polarity"}
            if rule.get("construct") in TYPED_FORMATION_OFFERS:
                rich_meaning_check(rule["construct"],rule.get("augment",{}))
            elif rule.get("construct")=="LEXICAL_PROJECT_REVALUATION":
                v=rule.get("augment",{});require(exact_keys(v,("priority","personal_significance")) and
                    type(v["priority"]) in (int,float) and isfinite(v["priority"]) and v["priority"]>=0 and
                    text(v["personal_significance"]),"GEN_LEXICAL_MEANING")
            elif rule.get("construct")=="CROSS_OBJECT_POSSIBLE_END":
                v=rule.get("augment",{});require(exact_keys(v,("possible_object","possible_means","cue_terms")) and
                    text(v["possible_object"]) and v["possible_means"]==["INSPECT"] and
                    isinstance(v["cue_terms"],list) and 1<=len(v["cue_terms"])<=12 and
                    all(text(k,80) for k in v["cue_terms"]),"GEN_CROSS_OBJECT_MEANING")
            elif rule.get("construct")=="INCIDENTAL_END_TAKEUP":
                require(rule.get("augment")=={"means":["INSPECT"]},"GEN_TAKEUP_MEANS")
            else:require(set(rule.get("augment",{}))<=allowed,"GEN_NOMINATION_AUGMENT")

# R44: typed wrappers for existing native offer grammars. The offered basis
# is copied at dispatch, never supplied by the remote policy. Semantic choices
# remain conditional and may be withheld; the native development owner admits.
TYPED_FORMATION_OFFERS = {
    "DELAYED_APPRAISAL": ("historically_possible_delayed_appraisals",),
    "ACTIVITY_AFFECT": ("historically_possible_activity_affects",
                        "historically_possible_self_expression_affects"),
    "ORDINARY_AFFECT_MEMORY": ("historically_possible_activity_affects",),
    "RECURRENT_ROUTINE": ("historically_possible_recurrent_routines",),
    "ROUTINE_REVISION": ("historically_possible_routine_revisions",),
    "EXPRESSIVE_PRACTICE": ("historically_possible_expressive_practices",),
    "RECURRENT_WORK_ORIENTATION": ("historically_possible_recurrent_livelihood_orientation",),
    "LIVED_CROSS_CONTEXT_REVALUATION": ("historically_possible_lived_cross_context_revaluations",),
    "WITNESSED_OTHER_RELATION": ("historically_possible_witnessed_third_party_relations",),
}

def rich_meaning_check(kind,v):
    if kind=="DELAYED_APPRAISAL":
        require(exact_keys(v,("appraisal",)) and text(v["appraisal"],100),"GEN_APPRAISAL")
    elif kind=="ACTIVITY_AFFECT":
        require(exact_keys(v,("affect_name","personal_sense","course_orientation")) and
                text(v["affect_name"],120) and text(v["personal_sense"]) and
                v["course_orientation"] in ("APPROACH","WITHHOLD"),"GEN_ACTIVITY_AFFECT")
    elif kind=="ORDINARY_AFFECT_MEMORY":
        require(exact_keys(v,("content","cue_terms")) and text(v["content"])
                and isinstance(v["cue_terms"],list) and 1<=len(v["cue_terms"])<=12
                and all(text(k,80) for k in v["cue_terms"]),"GEN_ORDINARY_AFFECT_MEMORY_MEANING")
    elif kind=="RECURRENT_ROUTINE":
        require(exact_keys(v,("window_days","hours_per_active_day","provisional_exposure_fraction"),
                             ("food_units_per_active_day",))
                and type(v["window_days"]) is int and 1<=v["window_days"]<=90
                and type(v["hours_per_active_day"]) in (int,float)
                and isfinite(v["hours_per_active_day"]) and 0<v["hours_per_active_day"]<=4
                and type(v["provisional_exposure_fraction"]) in (int,float)
                and isfinite(v["provisional_exposure_fraction"]) and 0<v["provisional_exposure_fraction"]<=1
                and ("food_units_per_active_day" not in v or (type(v["food_units_per_active_day"]) in (int,float)
                     and isfinite(v["food_units_per_active_day"]) and 0<v["food_units_per_active_day"]<=1
                     and round(v["food_units_per_active_day"],5)==v["food_units_per_active_day"])),
                "GEN_RECURRENT_ROUTINE_MEANING")
    elif kind=="ROUTINE_REVISION":
        require(exact_keys(v,("mode","interpretive_hypothesis"),("dose",))
                and v["mode"] in ("PAUSE","RESUME","RETIRE","RESIZE")
                and text(v["interpretive_hypothesis"])
                and ("dose" in v)==(v["mode"]=="RESIZE"),"GEN_ROUTINE_REVISION_MEANING")
        if "dose" in v:
            d=v["dose"]
            require(exact_keys(d,("hours_per_active_day","provisional_exposure_fraction"),
                               ("food_units_per_active_day",))
                    and all(type(x) in (int,float) and isfinite(x) and x>0 for x in d.values()),
                    "GEN_ROUTINE_REVISION_DOSE")
    elif kind=="EXPRESSIVE_PRACTICE":
        require(exact_keys(v,("cadence",)) and text(v["cadence"],40),"GEN_EXPRESSIVE_PRACTICE")
    elif kind=="RECURRENT_WORK_ORIENTATION":
        require(exact_keys(v,("orientation_mode",)) and
                v["orientation_mode"] in ("APPROACH","WITHHOLD"),"GEN_RECURRENT_ORIENTATION")
    elif kind=="LIVED_CROSS_CONTEXT_REVALUATION":
        require(exact_keys(v,("new_relation","new_polarity"),("interpretive_hypothesis",)) and
                text(v["new_relation"],80) and v["new_relation"] in RELATIONS and
                text(v["new_polarity"],80) and v["new_polarity"] in POLARITIES and
                ("interpretive_hypothesis" not in v or text(v["interpretive_hypothesis"])),
                "GEN_CROSS_CONTEXT_MEANING")
    elif kind=="WITNESSED_OTHER_RELATION":
        require(exact_keys(v,("hypothesis",)) and text(v["hypothesis"]),"GEN_OTHER_RELATION_HYPOTHESIS")

def rich_candidate(kind,q,v):
    if kind=="DELAYED_APPRAISAL":
        return {"kind":"APPRAISE_EXPECTED_DIFFERENCE","expectation_ref":q["expectation_ref"],
                "perceived_cue_ref":q["source_perceived_cue_ref"],**v}
    if kind=="ACTIVITY_AFFECT":
        return {"kind":"ACQUIRE_ACTIVITY_AFFECT","basis":q,**v}
    if kind=="RECURRENT_ROUTINE":
        require(("food_units_per_active_day" in v)==(q["basis"]["operation"]=="FEED")
                and v["window_days"]<=q["maximum_window_days"]
                and v["hours_per_active_day"]<=q["maximum_hours_per_active_day"],
                "GEN_RECURRENCE_UNOFFERED_DOSE")
        return {"kind":"ACQUIRE_RECURRENT_ROUTINE","basis":q["basis"],**v}
    if kind=="ROUTINE_REVISION":
        require(v["mode"] in q["allowed_modes"],"GEN_ROUTINE_REVISION_UNOFFERED_MODE")
        if "dose" in v:
            ceiling={k:x for k,x in q["original_ceiling"].items() if k!="state"}
            require(set(v["dose"])==set(ceiling) and all(x<=ceiling[k] for k,x in v["dose"].items()),
                    "GEN_ROUTINE_REVISION_UNOFFERED_DOSE")
        return {"kind":"REVISE_RECURRENT_ROUTINE","basis":q["basis"],**v}
    if kind=="EXPRESSIVE_PRACTICE":
        return {"kind":"ACQUIRE_EXPRESSIVE_PRACTICE","basis":q["basis"],**v}
    if kind=="RECURRENT_WORK_ORIENTATION":
        return {"kind":"ACQUIRE_HISTORICAL_ORIENTATION","operation":"WORK",
                "perceived_cue_ref":q["current_received_work_sign_ref"],
                "recurrent_work_practice":{k:q[k] for k in (
                    "prior_exercised_work_refs","current_received_work_sign_ref","current_world_event_ref")},**v}
    if kind=="LIVED_CROSS_CONTEXT_REVALUATION":
        choices=q["semantic_choice_required"]
        require(v["new_relation"] in choices["new_relation"] and
                v["new_polarity"] in choices["new_polarity"],"GEN_CROSS_CONTEXT_UNOFFERED_MEANING")
        return {"kind":"REORGANIZE_RELATIONAL_MOTIF","motif_id":q["motif_id"],
                "lived_cross_context_basis":q["lived_cross_context_basis"],**v}
    if kind=="WITNESSED_OTHER_RELATION":
        return {"kind":"CHANGE_OTHER_MODEL","other_ref":q["source_actor_ref"],
                "about_relation_with_ref":q["target_actor_ref"],
                "witnessed_cue_ref":q["witnessed_cue_ref"],**v}
    raise RecursionRefusal("GEN_UNKNOWN_RICH_CONSTRUCTION")

class ConditionalPolicy:
    """Compile checkpoint-supplied hypotheses against fresh owner offers.

    Existing local heuristic supplies unplanned/failed-to-bind paths. No
    actor policy can select a second person's action on its behalf. Rules
    see only that actor's actual packet, never another's private packet.
    """
    grade=GRADE
    def __init__(self, policies, rehearsal=None, family_choice=None):
        self.policies=detached(policies)
        self.rehearsal=detached(rehearsal)
        self.family_choice=detached(family_choice)
        self.local=HeuristicSemanticProvider()
        self.counts=Counter()
        self.routes=Counter()
        self.packet_bytes=0
    def propose(self,task,packet):
        self.counts[task]+=1
        self.packet_bytes+=len(canonical(packet).encode("utf-8"))
        actor=packet.get("actor",{}).get("id") or packet.get("actor_id")
        policy=self.policies.get(actor,{})
        retro=self.rehearsal if self.rehearsal and self.rehearsal["actor"]==actor else None
        if task=="family_pathway_selection":
            require(self.family_choice is not None,"GEN_UNPLANNED_FAMILY_SELECTION")
            chosen=self.family_choice["pathway_id"]
            eligible={x["id"] for x in packet["eligible_pathways"]}
            self.routes["checkpoint_family_selection"]+=1
            return {"task":task,"pathway_id":chosen if chosen in eligible else None}
        if task=="actor_attempt":
            if retro and packet.get("requesting_actor") is None:
                rows=[o for o in packet.get("private_rehearsal_options",[])
                      if o.get("memory_event_ref")==retro["objective_ref"] and o.get("affect_ref") is None]
                if len(rows)==1:
                    self.routes["retrospective_rehearsal_selected"]+=1
                    return {"task":task,"action":"WAIT","private_rehearsal_id":rows[0]["rehearsal_id"],
                            "private_rehearsal_content":retro["meaning"]}
                self.routes["retrospective_rehearsal_not_currently_eligible"]+=1
            r=policy.get("private_rehearsal")
            if r and packet.get("requesting_actor") is None:
                rows=[q for q in packet.get("private_rehearsal_options",[])
                      if (q.get("affect_ref") is not None)==(r["affect"]=="REQUIRED")
                      and all(q.get(k)==r[k] for k in ("memory_event_ref","memory_ref","affect_ref") if k in r)]
                if len(rows)==1:
                    self.routes["private_rehearsal_selected"]+=1
                    return {"task":task,"action":"WAIT","private_rehearsal_id":rows[0]["rehearsal_id"],
                            "private_rehearsal_content":r["meaning"]}
                self.routes["private_rehearsal_absent_or_ambiguous"]+=1
            for rule in policy.get("actions",[]):
                action=rule["action"]
                if "current_match" in rule and not any(subset(c,rule["current_match"]) for c in packet.get("situated",{}).get("currents",[])):
                    self.routes["checkpoint_current_guard_unmet"]+=1
                    continue
                if action=="SELECT_HIGHEST_CURRENT_PROJECT_COURSE":
                    courses=[(c["priority"],o["action"],c["project_id"])
                             for o in packet.get("options",[]) if o["action"] in rule["project_course_actions"]
                             for c in o.get("project_courses",[])
                             if type(c.get("priority")) in (int,float) and c.get("project_id")]
                    best=[x for x in courses if x[0]==max(v[0] for v in courses)] if courses else []
                    if len(best)==1:
                        self.routes["checkpoint_current_project_rank"]+=1
                        return {"task":task,"action":best[0][1],"project_id":best[0][2]}
                    self.routes["checkpoint_project_rank_tie_or_absent"]+=1
                    continue
                if not any(o.get("action")==action for o in packet.get("options",[])):
                    continue
                if "option_match" in rule:
                    pool=rule.get("pool","practical_options")
                    rows=[o for o in packet.get(pool,[])
                          if o.get("operation")==action and subset(o,rule["option_match"])]
                    if "exclude_affect" in rule:
                        rows=[o for o in rows if not any(subset(a,rule["exclude_affect"])
                            for a in o.get("course_affective_organizations",[]))]
                    if rule.get("rank_by")=="LATEST_PERSONALLY_SENSED_REGULATION":
                        # A declared conditional selection, not a universal
                        # psychological preference law. Actual personal relief
                        # is the only eligible rank; ties leave it unresolved.
                        ranked=[]
                        for o in rows:
                            clocks=[x["event_clock"] for x in o.get("personally_sensed_support_history",[])
                                    if x.get("bodily_regulation_sensed") is True and
                                    type(x.get("event_clock")) is int]
                            if clocks:ranked.append((max(clocks),o))
                        rows=([o for clock,o in ranked if clock==max(v for v,_ in ranked)]
                              if ranked else [])
                    if len(rows)!=1:
                        self.routes["option_not_unique_or_absent"]+=1
                        continue
                    out=({"task":task,"possible_end_trial_id":rows[0]["trial_id"]}
                         if pool=="possible_end_trials" else {"task":task,"practical_option_id":rows[0]["option_id"]})
                else:
                    out={"task":task,"action":action}
                    if "project_id" in rule:
                        pid=rule["project_id"]
                        if pid is not None and not any(
                            any(c.get("project_id")==pid for c in o.get("project_courses",[]))
                            for o in packet.get("options",[]) if o.get("action")==action):
                            self.routes["project_not_currently_offered"]+=1
                            continue
                        if pid is not None:out["project_id"]=pid
                if "speech_intent" in rule and packet.get("requesting_actor") is None:
                    out["speech_intent"]=rule["speech_intent"]
                self.routes["checkpoint_actor_selection"]+=1
                return out
        if task=="development":
            form=policy.get("formation",{"base":"LOCAL","rules":[]})
            candidates=(self.local.propose(task,packet)["candidates"] if form["base"]=="LOCAL" else [])
            if retro:
                rows=[c for c in packet.get("historically_possible_retrospective_orientation_revisions",[])
                      if c.get("retrospective_repair_revaluation_basis",{}).get("earlier_event_ref")
                         ==retro["objective_ref"]]
                if len(rows)==1:
                    c=detached(rows[0]);c["interpretive_hypothesis"]=retro["meaning"]
                    candidates.append(c)
                    self.routes["retrospective_revision_nominated"]+=1
                elif packet.get("actual_private_rehearsal_analyst_only"):
                    self.routes["retrospective_no_qualified_revision"]+=1
            for rule in form["rules"]:
                if "private_construct" in rule:
                    kind=rule["private_construct"];v=rule["augment"];m=rule.get("match",{})
                    experience=packet.get("experience",{});sel=experience.get("own_practical_selection") or {}
                    rec=packet.get("actual_private_rehearsal_analyst_only")
                    if kind=="NOTICE_END":
                        if (rec and rec.get("actor")==actor and set(v["means"])<=set(rec.get("possible_means",[]))
                                and subset({"private_affect_ref":rec.get("affect_ref")},m)):
                            candidates.append({"kind":"NOTICE_PRIVATE_POSSIBLE_END","rehearsal_ref":rec["id"],
                                "possible_object":v["possible_object"],"possible_means":v["means"]})
                            self.routes["private_end_nominated"]+=1
                    else:
                        # Derive only from retained actual ends and a later own
                        # performed course. Native admission rechecks all grounds.
                        rows=[e for e in packet.get("actor_possible_ends",[])
                              if e.get("genesis_family")=="ACTUAL_PRIVATE_REHEARSAL"
                              and e.get("status")=="POSSIBLE_NOT_ACQUIRED_MOTIVE"
                              and subset({**e,"possible_end_ref":e.get("id")},m)
                              and e.get("private_location")==experience.get("location")
                              and type(e.get("origin_clock")) is int and e["origin_clock"]<experience.get("clock",-1)
                              and set(v["means"])<=set(e.get("possible_means",[]))
                              and (e.get("private_ordinary_affect_memory") is None
                                   or v["means"]==[experience.get("own_action")])
                              and any(t.get("actor_experienced_status")=="PERFORMED"
                                  and t.get("private_rehearsal_ref")==e.get("private_rehearsal_ref")
                                  and t.get("operation")==experience.get("own_action")
                                  and t.get("event_ref")!=packet.get("evidence_path",{}).get("event")
                                  for t in e.get("trial_history",[]))]
                        if (len(rows)==1 and experience.get("status")=="PERFORMED"
                                and experience.get("perceived_cues") and sel.get("status")=="ACTOR_POLICY_PRACTICAL_ATTEMPT"
                                and sel.get("selected_project_refs")==[] and sel.get("possible_end_trial") is None):
                            candidates.append({"kind":"TAKE_UP_POSSIBLE_END","possible_end_ref":rows[0]["id"],
                                               "means":v["means"]})
                            self.routes["private_end_takeup_nominated"]+=1
                elif "candidate" in rule:
                    if subset(packet.get("experience",{}),rule.get("when",{})):
                        candidates.append(detached(rule["candidate"]))
                        self.routes["checkpoint_direct_candidate"]+=1
                else:
                    rows=[c for c in packet.get(rule["offer"],[]) if subset(c,rule.get("match",{}))]
                    if rule.get("resolver")=="EXISTING_PLURAL_CARE_SOURCE_RESOLUTION":
                        proposals=choose_one_grounded_plural_acquisition(rows)
                        candidates.extend(proposals)
                        self.routes["existing_plural_care_resolution"]+=len(proposals)
                        continue
                    if len(rows)!=1:
                        self.routes["nomination_not_unique_or_absent"]+=1
                        continue
                    q=detached(rows[0]);extra=rule.get("augment",{})
                    construct=rule.get("construct")
                    if construct=="ORDINARY_AFFECT_MEMORY":
                        # Never let a generic memory borrow a coincident affect.
                        # Only the exact fresh owner offer AND an earlier same
                        # dispatch affect nomination can supply this memory.
                        # Native development still checks actual admission,
                        # expressive capacity, source, actor and chronology.
                        prior=[c for c in candidates if c.get("kind")=="ACQUIRE_ACTIVITY_AFFECT"
                               and c.get("basis")==q]
                        if q.get("formation_source")!="OWN_ORDINARY_PROJECT_EXERCISE" or len(prior)!=1:
                            self.routes["ordinary_affect_memory_unqualified"]+=1
                            continue
                        c={"kind":"MEMORY","ordinary_affect_memory_basis":q,**detached(extra)}
                    elif construct in TYPED_FORMATION_OFFERS:
                        c=rich_candidate(construct,q,detached(extra))
                    elif construct=="LEXICAL_PROJECT_REVALUATION":
                        c={"kind":"REORGANIZE_PROJECT","project_id":q["project_id"],
                           "lexical_revaluation_basis":q["lexical_revaluation_basis"],**detached(extra)}
                    elif construct=="CROSS_OBJECT_POSSIBLE_END":
                        c={"kind":"NOTICE_POSSIBLE_END","perceived_cue_ref":q["source_cue_ref"],
                           "origin_material_object_ref":q["world_material_object_ref"],
                           "incidental_object_end_basis":q["incidental_object_end_basis"],**detached(extra)}
                    elif construct=="INCIDENTAL_END_TAKEUP":
                        c={"kind":"TAKE_UP_POSSIBLE_END","possible_end_ref":q["possible_end_ref"],
                           "later_perceived_cue_ref":q["later_perceived_cue_ref"],
                           "incidental_takeup_basis":q,**detached(extra)}
                    else:c=q
                    if construct:
                        candidates.append(c);self.routes["typed_"+construct.lower()]+=1;continue
                    if set(extra)&set(c):
                        self.routes["nomination_augmentation_conflict"]+=1
                        continue
                    c.update(detached(extra));candidates.append(c)
                    self.routes["checkpoint_exact_offer_nomination"]+=1
            # De-duplicate identical local/model proposals without reordering.
            unique=[];seen=set()
            for c in candidates:
                key=canonical(c)
                if key not in seen:unique.append(c);seen.add(key)
            self.routes["development_"+form["base"].lower()]+=1
            return {"task":task,"candidates":unique}
        if task=="expression":
            expr=policy.get("expression",{})
            if packet.get("expression_phase")=="LEXICAL_REALIZATION_BEFORE_EXPERIENCE":
                if "speech" in expr:
                    self.routes["checkpoint_lexical"]+=1
                    return {"task":task,"speech":expr["speech"]}
                # No fake spoken words: let the owner reject the unavailable
                # local lexical response, not invent a narrative occurrence.
            elif "surface" in expr:
                self.routes["checkpoint_surface"]+=1
                return {"task":task,"surface":expr["surface"]}
        self.routes["existing_local_"+task]+=1
        return self.local.propose(task,packet)

class ModernDevelopmentOwner:
    """Adapter to the existing modern runtime, not an independent state writer.

    The extra SQLite table is operation-id receipt custody, as in P2Owner.
    Pending/ambiguous operations are never blindly replayed. The native owner
    DB remains the only world/psyche writer. A failure after a compressed
    interval may have committed that interval; the operation is held.
    """
    grade=GRADE
    def __init__(self,runtime,actor,receipt_path,*,sourcefree_attested=False,period_catalog=None,
                 family_sources=(),qualified_interval_cuts=False,continuity_link=None,selective_memory_context=False):
        require(sourcefree_attested is True,"GEN_SOURCEFREE_ATTESTATION_REQUIRED")
        self.rt=runtime;self.actor=actor
        self.rt.ledger.actor(actor)
        genesis=self.rt.ledger.events(limit=1)
        require(len(genesis)==1 and genesis[0]["kind"]=="INITIALIZATION","GEN_NO_GENESIS")
        self.root=genesis[0]["chain_hash"];self.branch="modern:"+runtime.world_id
        self.source_ref="SOURCEFREE_MODERN_ROOT:"+self.root
        self.period_catalog=detached(period_catalog or {})
        self.qualified_interval_cuts=qualified_interval_cuts
        require(type(selective_memory_context) is bool,"GEN_MEMORY_PROFILE")
        self.selective_memory_context=selective_memory_context
        self.continuity_link=detached(continuity_link)
        if self.continuity_link:
            require(self.continuity_link["root"]==self.root,"GEN_CONTINUITY_ROOT")
            require(self.continuity_link["actor"]==actor,"GEN_CONTINUITY_ACTOR")
            validate_actual_live_link(runtime,self.continuity_link)
        self.family_sources=tuple(sorted(set(family_sources)))
        for sid in self.family_sources:
            row=self.rt.ledger.source(sid)
            require(row and row["category"]==FAMILY_SOURCE,"GEN_FAMILY_SOURCE_UNSEALED")
            require(all(x["prior_shared_effects"]=="RETAIN_EXISTING_ACTUAL_HISTORY"
                        for x in row["content"]["candidates"]),"GEN_FAMILY_REGENERATION_NOT_AUTHORIZED")
        self.path=Path(receipt_path)
        self.db=sqlite3.connect(self.path)
        self.db.execute("CREATE TABLE IF NOT EXISTS binding (id INTEGER PRIMARY KEY,value TEXT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS operations "
                        "(id TEXT PRIMARY KEY, proposal TEXT NOT NULL, before_state TEXT NOT NULL, result TEXT)")
        self.db.execute("CREATE TABLE IF NOT EXISTS checkpoint_attempts (id INTEGER PRIMARY KEY, receipt TEXT NOT NULL)")
        binding=canonical({"root":self.root,"branch":self.branch,"actor":actor,
                           "catalog":self.period_catalog,"family_sources":self.family_sources,"qualified_interval_cuts":self.qualified_interval_cuts,
                           "continuity_link":self.continuity_link,"grade":GRADE,
                           **({"selective_memory_context":True} if self.selective_memory_context else {})})
        row=self.db.execute("SELECT value FROM binding WHERE id=1").fetchone()
        if row is None:self.db.execute("INSERT INTO binding VALUES (1,?)",(binding,))
        else:require(row[0]==binding,"GEN_RECEIPT_BINDING")
        self.db.commit()

    def record_checkpoint_start(self,receipt):
        cur=self.db.execute("INSERT INTO checkpoint_attempts(receipt) VALUES (?)",(canonical(receipt),))
        self.db.commit()
        return cur.lastrowid

    def record_checkpoint_update(self,attempt_id,**fields):
        row=self.db.execute("SELECT receipt FROM checkpoint_attempts WHERE id=?",(attempt_id,)).fetchone()
        require(row is not None,"GEN_CHECKPOINT_RECEIPT_MISSING")
        rec=json.loads(row[0]);rec.update(detached(fields))
        self.db.execute("UPDATE checkpoint_attempts SET receipt=? WHERE id=?",(canonical(rec),attempt_id))
        self.db.commit()

    def checkpoint_receipts(self):
        return [{"id":i,**json.loads(r)} for i,r in self.db.execute(
            "SELECT id,receipt FROM checkpoint_attempts ORDER BY id")]

    def snapshot(self):
        # Native verification binds current actors, world and entire ancestry.
        verified=self.rt.verify()
        require(verified.get("valid") is True,"GEN_NATIVE_CHAIN_INVALID")
        _,w=self.rt.ledger.world(self.rt.world_id)
        return StateIdentity(self.root,self.actor,self.branch,w["clock"],verified["last_hash"])

    def resolve_analytic_reads(self,reads,*,now=None,people=None):
        require(isinstance(reads,list) and len(reads)<=MAX_ANALYTIC_READS,"GEN_ANALYTIC_READ_LIMIT")
        out=[];seen=set();people=self.rt.ledger.actors() if people is None else people;events=None
        now=now or self.snapshot()
        for read in reads:
            require(isinstance(read,dict) and read.get("actor") in people,"GEN_ANALYTIC_READ_ACTOR")
            aid=read["actor"];kind=read.get("kind")
            if kind in ("ACTOR_DOMAIN","ACTOR_DOMAIN_PAGE","ACTOR_ROW"):
                extra={"ACTOR_DOMAIN":(),"ACTOR_DOMAIN_PAGE":("offset","limit"),"ACTOR_ROW":("row_ref",)}[kind]
                require(exact_keys(read,("kind","actor","domain",*extra)) and read["domain"] in ANALYTIC_DOMAINS,
                        "GEN_ANALYTIC_READ_DOMAIN")
                require(read["domain"] in people[aid],"GEN_ANALYTIC_READ_DOMAIN_ABSENT")
                value=people[aid][read["domain"]]
                identity={"current_state":now.state_hash,"domain":read["domain"],
                          "domain_digest":digest(value)}
                if kind!="ACTOR_DOMAIN":
                    rows=exact_domain_rows(value)
                    if kind=="ACTOR_DOMAIN_PAGE":
                        offset,limit=read["offset"],read["limit"]
                        require(type(offset) is int and 0<=offset<=len(rows) and
                                type(limit) is int and 1<=limit<=MAX_DOMAIN_PAGE,"GEN_ROW_PAGE_BOUNDS")
                        counts=Counter(k for k,_ in rows)
                        value={"count":len(rows),"offset":offset,"limit":limit,
                               "next_offset":offset+limit if offset+limit<len(rows) else None,
                               "rows":[{"row_ref":k,"row_digest":digest(v),"bytes":len(canonical(v).encode("utf-8")),
                                       "unique":counts[k]==1} for k,v in rows[offset:offset+limit]]}
                    else:
                        require(text(read["row_ref"],1024),"GEN_ROW_REF")
                        matches=[v for k,v in rows if k==read["row_ref"]]
                        require(len(matches)==1,"GEN_ROW_ABSENT_OR_AMBIGUOUS")
                        identity["row_ref"]=read["row_ref"]
                        value=matches[0]
            elif kind=="ACTUAL_EXPERIENCE":
                require(exact_keys(read,("kind","actor","objective_ref")) and text(read["objective_ref"]),
                        "GEN_ANALYTIC_READ_SOURCE")
                if events is None:events=self.rt.ledger.events()
                matches=[e for e in events if e["envelope"].get("payload",{}).get("objective_ref")==read["objective_ref"]
                         and aid in e["envelope"].get("payload",{}).get("private_actor_experience_receipts",{})]
                require(len(matches)==1,"GEN_ANALYTIC_READ_UNRECEIVED_OR_AMBIGUOUS")
                e=matches[0];value=e["envelope"]["payload"]["private_actor_experience_receipts"][aid]
                identity={"native_receipt":e["id"],"chain_hash":e["chain_hash"]}
            else:raise RecursionRefusal("GEN_ANALYTIC_READ_KIND")
            key=canonical(read);require(key not in seen,"GEN_ANALYTIC_READ_DUPLICATE");seen.add(key)
            out.append({"request":detached(read),"source":identity,"value":detached(value),
                        "value_digest":digest(value),"analyst_only_not_actor_self_knowledge":True})
        require(len(canonical(out).encode("utf-8"))<=MAX_ANALYTIC_BYTES,
                "GEN_ANALYTIC_EXPANSION_BUDGET_HOLD")
        require(latest_native_event(self.rt)["chain_hash"]==now.state_hash,"GEN_READ_STATE_MOVED")
        return out

    def context(self,analytic_reads=None):
        """Analyst-only, actor-separated working set; not a first-person account.
        Prior actual experience comes separately from inherited RecursionCycle.
        """
        now=self.snapshot()
        result={};people=self.rt.ledger.actors()
        for aid,a in people.items():
            situated=self.rt.situated(aid)
            memories=[m for m in a.get("memories",[]) if m.get("status")=="ACTOR_ACCESSIBLE"]
            working=memories
            if self.selective_memory_context and len(memories)>RECENT_ACCESSIBLE_MEMORY:
                # Keep recent accessible memory and all whose exact identity
                # or origin appears in the current actual tip; other accessible
                # rows remain canonically conserved and explicitly retrievable.
                tip=canonical(situated)
                def relevant(m):
                    refs=[m.get("id"),*(m.get("origin",[]) if isinstance(m.get("origin"),list) else [])]
                    return any(isinstance(ref,str) and len(ref)>0 and canonical(ref) in tip for ref in refs)
                working=[m for i,m in enumerate(memories)
                         if i>=len(memories)-RECENT_ACCESSIBLE_MEMORY or relevant(m)]
            result[aid]={"role":a["role"],"age_days":a["age_days"],"body":a["body"],
                         "location":a["location"],"projects":a.get("projects",[]),
                         "accessible_memories":working,
                         **({"accessible_memory_projection":{"profile":"RECENT_AND_CURRENT_TIP_REFERENCED",
                              "full_accessible_count":len(memories),"included_count":len(working),
                              "full_accessible_digest":digest(memories),
                              "exact_dormant_access_via_domain_page_and_row":True,
                              "not_a_change_of_actor_accessibility":True}} if self.selective_memory_context else {}),
                         "analyst_only_historical_orientations":a.get("historical_orientations",[]),
                         "current_situated":situated,
                         "exact_analytic_domain_index":{k:{"count":len(a[k]) if isinstance(a[k],(dict,list)) else None,
                             "digest":digest(a[k]),"bytes":len(canonical(a[k]).encode("utf-8"))}
                             for k in ANALYTIC_DOMAINS if k in a},
                         "possible_ends":a.get("possible_ends",[]),
                         "recent_lived_source_refs":[{"objective_ref":x["event"],"experience_ref":x.get("experience_ref")}
                             for x in a.get("evidence_paths",[])[-12:] if x.get("event")]}
        # Genealogy source is an analyst-only conditional premise. Do not
        # expose counterpart private source packets to an actor policy.
        family={}
        for sid in self.family_sources:
            source=self.rt.ledger.source(sid)["content"]
            family[sid]={"mother":source["mother"],"paths":[
                {k:x[k] for k in ("id","source_ref","intersection_clock","intersection_site",
                                  "conception_clock","birth_clock","counterpart_id","child_id")}
                for x in source["candidates"]]}
        _,world=self.rt.ledger.world(self.rt.world_id)
        return detached({"grade":GRADE,"source_ref":self.source_ref,"clock":now.clock,
                         "conditional_family_sources_analyst_only":family,
                         "family_stage_analyst_only":world.get("family_genesis",{}).get("stage"),
                         "actor_contexts":result,"period_refs":sorted(self.period_catalog),
                         "qualified_routine_windows":{key:[{
                            "source_ref":p["source_ref"],
                            "kind":p["kind"],"actor":p["actor"],
                            "from_clock":world["routine_source_registry"][p["source_ref"]]["from_clock"],
                            "through_clock":world["routine_source_registry"][p["source_ref"]]["through_clock"]}
                            for p in rows] for key,rows in self.period_catalog.items()},
                         **({"prior_generation_and_live_ancestry":self.continuity_link}
                            if self.continuity_link else {}),
                         "selected_exact_analytic_reads":self.resolve_analytic_reads(analytic_reads or [],now=now,people=people),
                         "actor_contexts_are_separate_analyst_only_not_actor_self_report":True})

    def validate_proposal(self,p):
        require(p.operation in ("CONTINUE_ACTOR_LIFE","REALIZE_FAMILY_BIRTH"),"GEN_OPERATION")
        require(p.source_refs==(self.source_ref,),"GEN_SOURCE")
        roster=set(self.rt.ledger.actors())
        require(len(p.participants)==1 and p.participants[0] in roster,"GEN_PRINCIPAL")
        require(type(p.event_time) is int and p.event_time>self.snapshot().clock,"GEN_CLOCK")
        c=p.circumstances
        require(exact_keys(c,("policies",),("retrospective_event_id","rehearsal","period_ref","family","next_analytic_reads")),
                "GEN_CIRCUMSTANCES")
        require(isinstance(c["policies"],dict) and set(c["policies"])<=roster,"GEN_POLICY_ACTOR")
        for policy in c["policies"].values():policy_check(policy)
        if p.interval is not None:
            require(exact_keys(p.interval,("mode","span")) and p.interval["mode"]=="ACTUAL" and
                    type(p.interval["span"]) is int and 1<=p.interval["span"]<=3650,"GEN_INTERVAL")
        if "period_ref" in c:
            require(p.interval is not None and c["period_ref"] in self.period_catalog,"GEN_PERIOD_REF")
        if "next_analytic_reads" in c:
            self.resolve_analytic_reads(c["next_analytic_reads"])
        family=c.get("family")
        if family is not None:
            require(exact_keys(family,("kind","source_seal_id"),("pathway_id",)) and
                    family["source_seal_id"] in self.family_sources and
                    family["kind"] in ("INTERSECTION","CONCEPTION","BIRTH"),"GEN_FAMILY_AUTHORITY")
            src=self.rt.ledger.source(family["source_seal_id"])["content"]
            if family["kind"]=="INTERSECTION":
                require("pathway_id" in family and (family["pathway_id"] is None or
                        any(x["id"]==family["pathway_id"] for x in src["candidates"])),
                        "GEN_FAMILY_PATHWAY_UNISSUED")
                require(p.participants==(src["mother"],),"GEN_MATERNAL_SELECTION_PRINCIPAL")
            else:
                require("pathway_id" not in family,"GEN_FAMILY_FORGED_SELECTION")
            clock_field={"INTERSECTION":"intersection_clock","CONCEPTION":"conception_clock",
                         "BIRTH":"birth_clock"}[family["kind"]]
            require(any(x[clock_field]==p.event_time for x in src["candidates"]),
                    "GEN_FAMILY_SOURCE_CLOCK")
        if p.operation=="REALIZE_FAMILY_BIRTH":
            require(family and family["kind"]=="BIRTH" and p.interval is not None and
                    not c["policies"] and "rehearsal" not in c and
                    p.participants==(self.rt.ledger.source(family["source_seal_id"])["content"]["mother"],),
                    "GEN_BIRTH_SURFACE")
        else:
            require(not family or family["kind"]!="BIRTH","GEN_BIRTH_WRONG_OPERATION")
        if "rehearsal" in c:
            r=c["rehearsal"]
            require(exact_keys(r,("actor","objective_ref","meaning")) and
                    r["actor"]==p.participants[0] and text(r["meaning"]) and text(r["objective_ref"]),
                    "GEN_REHEARSAL_SCHEMA")
            # The reference must resolve an actual actor-local experience in
            # the native chain. The current private rehearsal owner rechecks
            # memory access and acquired means during realization.
            matches=[e for e in self.rt.ledger.events() if
                     e["envelope"].get("payload",{}).get("objective_ref")==r["objective_ref"] and
                     r["actor"] in e["envelope"].get("payload",{}).get("private_actor_experience_receipts",{})]
            require(len(matches)==1,"GEN_REHEARSAL_SOURCE_NOT_ACTUAL")
        require(("retrospective_event_id" in c)==("rehearsal" in c),"GEN_RETRO_BINDING")

    def family_transition(self, family):
        """Recheck native stage/clock/encounter; conditional nonoccurrence is real."""
        if family is None:return None
        sid=family["source_seal_id"];kind=family["kind"]
        source=self.rt.ledger.source(sid)["content"]
        _,world=self.rt.ledger.world(self.rt.world_id)
        current=world.get("family_genesis",{})
        if kind=="INTERSECTION":
            mother=self.rt.ledger.actor(source["mother"])[1]
            offers=situated_family_pathways(world,mother,source,self.rt.ledger.actors())
            if not offers:return {"kind":kind,"status":"NOT_REALIZED_NO_SITUATED_PATHWAY"}
            out=self.rt.select_family_intersection(sid)
            return {"kind":kind,"status":out.get("status","BOUND"),"native":out}
        if current.get("source_seal_id")!=sid:
            return {"kind":kind,"status":"NOT_REALIZED_NO_MATCHING_BOUND_PATH"}
        path=current["selected_pathway"]
        if kind=="CONCEPTION":
            if (current.get("stage")!="COUNTERPART_ADMITTED" or
                    world["clock"]!=path["conception_clock"] or
                    not all(world["positions"].get(a)==path["intersection_site"]
                            for a in (path["mother"],path["counterpart"])) or
                    not family_encounter_evidence(world,path)):
                return {"kind":kind,"status":"NOT_REALIZED_CONDITIONS_UNMET"}
            return {"kind":kind,"status":"CONDITIONAL_CONCEPTION_ADMITTED",
                    "native":self.rt.admit_family_conception()}
        if (current.get("stage")!="CONCEPTION_ADMITTED" or
                world["clock"]!=path["birth_clock"]):
            return {"kind":kind,"status":"NOT_REALIZED_CONDITIONS_UNMET"}
        return {"kind":kind,"status":"CHILD_BORN","native":self.rt.realize_family_birth()}

    def advance_interval(self,span,processes,*,birth_surface=False,principal=None):
        """Reuse the joined owner's source windows and discontinuity reader.

        No independent calendar or invented event. Passive boundaries are
        reached in actual native periods. A due actor turn or unplanned birth
        is held rather than silently erased by a speculative time budget.
        A planned birth is settled by the existing family operation.
        """
        if not self.qualified_interval_cuts:
            out=self.rt.background(span,processes=processes)
            return [out],[latest_native_event(self.rt)]
        from um_sorok_organism.continuity_clock import (
            qualify_mixed_history_schedule,mixed_history_interval,next_discontinuity,MAX_HORIZON)
        world=self.rt.ledger.world(self.rt.world_id)[1];target=world["clock"]+span
        require(not any(x.get("present") is True for x in world.get("neighbor_users",{}).values()),
                "GEN_PRESENT_VISITOR_REQUIRES_LIVE_OWNER")
        from um_sorok_organism.routine_sources import acquired_routine_processes, lived_work_permission_boundaries
        schedule=qualify_mixed_history_schedule(world,processes)
        explicit_refs={row["source_ref"] for _,_,row in schedule}
        receipts=[];events=[]
        while world["clock"]<target:
            clock=world["clock"]
            # Same actor-owned routine registry and cut semantics as the
            # existing mixed-history owner. Never carry a stale copied dose
            # from an earlier semantic checkpoint or omit independent claims.
            dynamic=qualify_mixed_history_schedule(world,[p for p in acquired_routine_processes(world)
                       if p["source_ref"] not in explicit_refs])
            end,active=mixed_history_interval(schedule+dynamic,clock,min(target,clock+MAX_HORIZON))
            for p in active:
                if p["kind"]=="QUALIFIED_WAGE_LABOR":
                    times=lived_work_permission_boundaries(world,p["actor"],p["location"],clock,end)
                    if times:end=min(end,times[0])
            boundary=next_discontinuity(world,self.rt.ledger.actors(),end-clock)
            if boundary:
                kind=boundary["kind"];at=boundary["at"]
                if kind=="CONDITIONAL_FAMILY_BIRTH":
                    require(birth_surface and at==target,"GEN_UNPLANNED_CONDITIONAL_BIRTH")
                if kind=="OBLIGATION_DUE":
                    require(at==target and not birth_surface and boundary["actor"]==principal,
                            "GEN_DUE_OCCASION_REQUIRES_EXPLICIT_SURFACE")
                end=at
            require(end>clock,"GEN_ZERO_INTERVAL")
            out=self.rt.background(end-clock,processes=active)
            evt=latest_native_event(self.rt)
            require(evt["id"]==out["receipt"] and evt["clock"]==end,"GEN_NATIVE_INTERVAL_RECEIPT")
            receipts.append(out);events.append(evt);world=self.rt.ledger.world(self.rt.world_id)[1]
        return receipts,events

    def realize(self,operation_id,p,expected):
        with self.path.with_suffix(self.path.suffix+".lock").open("a") as lock:
            fcntl.flock(lock,fcntl.LOCK_EX)
            ph=digest(p.document());before=canonical(expected.document())
            row=self.db.execute("SELECT proposal,before_state,result FROM operations WHERE id=?",
                                (operation_id,)).fetchone()
            if row:
                require(row[:2]==(ph,before),"GEN_OPERATION_REUSE")
                require(row[2] is not None,"GEN_AMBIGUOUS_PRIOR_OPERATION_HOLD")
                d=json.loads(row[2]);d["before"]=StateIdentity(**d["before"])
                d["after"]=StateIdentity(**d["after"]);d["readset"]=tuple(d["readset"])
                result=RealizedEvent(**d)
                require(self.snapshot()==result.after,"GEN_REPLAY_STATE_MOVED")
                return result
            require(self.snapshot()==expected,"GEN_STALE_OWNER")
            self.validate_proposal(p)
            span=p.interval["span"] if p.interval else 0
            require(p.event_time==expected.clock+span+(p.operation=="CONTINUE_ACTOR_LIFE"),
                    "GEN_EVENT_CLOCK_NOT_SEQUENTIAL")
            if self.qualified_interval_cuts:
                # The interval cutter is not the authority for a detail beat:
                # span=0 bypasses it, and a span+one detail beat could land on
                # a pending birth after the last compressed cut. Check the
                # entire proposed event against actual current owner state
                # BEFORE any native write or pending operation receipt.
                world=self.rt.ledger.world(self.rt.world_id)[1]
                require(not any(v.get("present") is True for v in world.get("neighbor_users",{}).values()),
                        "GEN_PRESENT_VISITOR_REQUIRES_LIVE_OWNER")
                current=world.get("family_genesis",{})
                if current.get("stage")=="CONCEPTION_ADMITTED":
                    birth=current["selected_pathway"]["birth_clock"]
                    if p.operation=="REALIZE_FAMILY_BIRTH":
                        require(p.event_time==birth and
                                p.circumstances["family"]["source_seal_id"]==current["source_seal_id"],
                                "GEN_UNPLANNED_CONDITIONAL_BIRTH")
                    else:
                        require(p.event_time<birth,"GEN_UNPLANNED_CONDITIONAL_BIRTH")
                if not span:
                    from um_sorok_organism.continuity_clock import next_discontinuity
                    boundary=next_discontinuity(world,self.rt.ledger.actors(),1)
                    if (boundary and boundary["kind"]=="OBLIGATION_DUE"
                            and boundary["at"]==world["clock"]):
                        require(boundary["actor"]==p.participants[0],
                                "GEN_DUE_OCCASION_REQUIRES_EXPLICIT_SURFACE")
            self.db.execute("INSERT INTO operations VALUES (?,?,?,NULL)",(operation_id,ph,before))
            self.db.commit()
            interval=None;interval_events=[]
            c=p.circumstances
            if span:
                intervals,interval_events=self.advance_interval(span,detached(self.period_catalog.get(c.get("period_ref"),[])),
                    birth_surface=p.operation=="REALIZE_FAMILY_BIRTH",principal=p.participants[0])
                interval=intervals[0] if len(intervals)==1 else {"segments":intervals}
                require(interval_events[-1]["clock"]==expected.clock+span,"GEN_INTERVAL_RECEIPT_CLOCK")
            policy=ConditionalPolicy(c["policies"],c.get("rehearsal"),c.get("family"))
            old=self.rt.semantic
            step_event=None;out=None;family_result=None
            try:
                self.rt.semantic=ValidatingSemanticService(policy)
                if p.operation=="CONTINUE_ACTOR_LIFE":
                    out=self.rt.step(p.participants[0]) # no injected action, target or coactor
                    step_event=latest_native_event(self.rt)
                    require(step_event["id"]==out["receipt"] and step_event["kind"]=="ACTOR_LIFE_TRANSITION",
                            "GEN_NATIVE_RECEIPT")
                family_result=self.family_transition(c.get("family"))
            finally:self.rt.semantic=old
            event=latest_native_event(self.rt)
            after=self.snapshot()
            require(after.clock==p.event_time,"GEN_NATIVE_CLOCK")
            payload=step_event["envelope"]["payload"] if step_event else {}
            accessible={"objective_ref":payload.get("objective_ref",event["id"]),
                        "by_actor":detached(payload.get("private_actor_experience_receipts",{})),
                        "receipt_grade":GRADE}
            # A birth or genealogy binding is not an invented lived receipt.
            # Preserve the actual step separately from a same-clock family op.
            readset=tuple(dict.fromkeys([self.source_ref,
                       *[e["chain_hash"] for e in interval_events],
                       *([step_event["chain_hash"]] if step_event else []),event["chain_hash"]]))
            result=RealizedEvent(operation_id,ph,expected,after,"REALIZED",
                {"native_receipt":event["id"],"step_receipt":step_event["id"] if step_event else None,
                 "actual":detached(payload.get("actual")),"interval":detached(interval),
                 "attempt":out["attempt"] if out else None,
                 "status":out["status"] if out else None,
                 "selection_grade":out["selection_grade"] if out else None,
                 "family":detached(family_result)},
                accessible,
                {"grade":GRADE,"developmental_effects":detached(payload.get("developmental_effects",{})),
                 "local_semantic_tasks":dict(policy.counts),"conditional_routes":dict(policy.routes),
                 "local_packet_bytes":policy.packet_bytes,
                 "remote_calls_during_event":0,"native_chain_hash":after.state_hash,
                 "next_analytic_reads":detached(c.get("next_analytic_reads",[]))},
                readset,event["id"])
            self.db.execute("UPDATE operations SET result=? WHERE id=?",
                            (canonical(result.document()),operation_id));self.db.commit()
            return result
    def close(self):self.db.close()

class CheckpointProvider:
    """One provider call per inherited checkpoint; bind impressions to actuality.

    The provider is an explicit CallProvider, not a network default. The
    provider may emit one retrospective disposition per actually received
    event/actor. REHEARSE must bind a next prospective surface; it is a
    hypothesis to be tested through an actual owner-selected private activity.
    Interpret-only content is conserved, never called admitted psychology.
    """
    def __init__(self,provider,*,owner,max_request_bytes=1024*1024):
        require(hasattr(provider,"call"),"GEN_EXPLICIT_CALL_PROVIDER")
        self.provider=provider;self.owner=owner;self.max_request_bytes=max_request_bytes
        self.attempts=[];self.current_attempt_id=None
    def call(self,request):
        raw_bytes=len(canonical(request).encode("utf-8"))
        rec={"mode":request["mode"],"request_bytes":raw_bytes,"request_digest":digest(request),
             "outcome":"STARTED","provider_called":False,"cycle_disposition":"PENDING"}
        aid=self.owner.record_checkpoint_start(rec);self.current_attempt_id=aid
        self.attempts.append(rec);start=perf_counter_ns()
        usage=getattr(self.provider,"usage_snapshot",None)
        before=usage()["total"] if usage else None
        try:
            if raw_bytes>self.max_request_bytes:
                rec["outcome"]="PREFLIGHT_REJECTED"
                raise RecursionRefusal("GEN_CHECKPOINT_CONTEXT_LIMIT")
            rec["provider_called"]=True
            self.owner.record_checkpoint_update(aid,provider_called=True)
            raw=detached(self.provider.call(detached(request)))
            rec["response_bytes"]=len(canonical(raw).encode("utf-8"))
            rec["outcome"]="RESPONSE_REJECTED"
            response=self.bind(request,raw)
            rec["outcome"]="RETURNED"
            return response
        except BaseException as exc:
            if rec["outcome"]=="STARTED":rec["outcome"]="PROVIDER_FAILED_OR_AMBIGUOUS"
            rec["exception_type"]=type(exc).__name__
            raise
        finally:
            rec["elapsed_ns"]=perf_counter_ns()-start
            if usage:
                snap=usage();after=snap["receipts"]
                if snap["total"]==before+1 and after:
                    rec["transport_receipt"]={k:detached(v) for k,v in after[-1].items()
                        if k in ("task","transport","attempts","outcome","request_bytes","response_bytes",
                                 "instruction_bytes","packet_bytes","response_content_bytes","usage","elapsed_ns")}
            self.owner.record_checkpoint_update(aid,**rec)
    @staticmethod
    def bind(request,response):
        require(exact_keys(response,("retrospective","prospective")),"GEN_CHECKPOINT_RESPONSE")
        mode=request["mode"];previous=request["previous"]
        ret=response["retrospective"];pros=response["prospective"]
        plans={}
        if mode=="BOOTSTRAP":
            require(ret is None and previous is None,"GEN_BOOTSTRAP_HISTORY")
        else:
            require(exact_keys(ret,("batch_id","history_hash","event_ids","impressions")) and
                    ret["batch_id"]==previous["batch_id"] and ret["history_hash"]==previous["history_hash"],
                    "GEN_RETRO_SOURCE")
            events=previous["events"];ids=[e["event_id"] for e in events]
            require(ret["event_ids"]==ids and isinstance(ret["impressions"],list) and
                    len(ret["impressions"])==len(ids),"GEN_RETRO_ORDER")
            for item,prior in zip(ret["impressions"],events):
                require(exact_keys(item,("event_id","interpretations")) and
                        item["event_id"]==prior["event_id"] and isinstance(item["interpretations"],list),
                        "GEN_RETRO_EVENT")
                seen=set();access=prior["accessible"]
                for meaning in item["interpretations"]:
                    require(exact_keys(meaning,("actor","meaning","disposition")) and
                            meaning["actor"] in access["by_actor"] and meaning["actor"] not in seen and
                            text(meaning["meaning"]) and meaning["disposition"] in
                            ("INTERPRET_ONLY","REHEARSE","ABSTAIN"),"GEN_RETRO_ACTOR_ACCESS")
                    seen.add(meaning["actor"])
                    if meaning["disposition"]=="REHEARSE":
                        require(mode=="ORDINARY","GEN_TERMINAL_NO_ACTUAL_CARRIER")
                        key=(item["event_id"],meaning["actor"])
                        plans[key]={"actor":meaning["actor"],"objective_ref":access["objective_ref"],
                                    "meaning":meaning["meaning"]}
        if mode=="TERMINAL":
            require(pros is None and not plans,"GEN_TERMINAL_PROSPECTIVE")
            return response
        require(isinstance(pros,list) and 3<=len(pros)<=5,"GEN_PROSPECTIVE_COUNT")
        prior_clock=request["context"].get("clock")
        for ordinal,p in enumerate(pros):
            require(isinstance(p,dict) and isinstance(p.get("circumstances"),dict) and
                    isinstance(p.get("participants"),list) and len(p["participants"])==1,
                    "GEN_PROSPECTIVE_SURFACE")
            c=p["circumstances"]
            if "next_analytic_reads" in c:
                require(ordinal==len(pros)-1,"GEN_ANALYTIC_READS_ON_FINAL_SURFACE_ONLY")
            if prior_clock is not None:
                interval=p.get("interval")
                require(interval is None or (exact_keys(interval,("mode","span")) and
                    interval["mode"]=="ACTUAL" and type(interval["span"]) is int and
                    1<=interval["span"]<=3650),"GEN_INTERVAL")
                op=p.get("operation")
                require(op in ("CONTINUE_ACTOR_LIFE","REALIZE_FAMILY_BIRTH"),"GEN_OPERATION")
                expected=prior_clock+(interval["span"] if interval else 0)+(op=="CONTINUE_ACTOR_LIFE")
                require(type(p.get("event_time")) is int and p["event_time"]==expected and
                        expected>prior_clock,"GEN_EVENT_CLOCK_NOT_SEQUENTIAL")
                prior_clock=expected
            require("rehearsal" not in c,"GEN_PROVIDER_INVENTED_REHEARSAL_BASIS")
            if "retrospective_event_id" in c:
                key=(c["retrospective_event_id"],p["participants"][0])
                require(key in plans,"GEN_UNBOUND_RETROSPECTIVE_CARRIER")
                c["rehearsal"]=plans.pop(key)
        require(not plans,"GEN_RETROSPECTIVE_CARRIER_DROPPED")
        return response

class ModernGeneration:
    """Existing durable P2 cycle with a modern owner, not a new scheduler."""
    def __init__(self,owner,provider,journal_path,cycle_path):
        self.owner=owner;self.provider=CheckpointProvider(provider,owner=owner)
        self.engine=BatchEngine(owner,journal_path)
        self.cycle=RecursionCycle(self.engine,self.provider,cycle_path)
    def _run(self,method):
        self.provider.current_attempt_id=None
        try:
            reads=[]
            if method.__name__ in ("advance","finish"):
                store=self.cycle._load()
                if store.get("phase")=="PENDING_BATCH":
                    pending=store["pending"];history=self.engine.history(pending["batch_id"])
                    require(history==pending,"GEN_ANALYTIC_READ_HISTORY_CHANGED")
                    reads=history["records"][-1]["consequences"].get("next_analytic_reads",[])
            context=self.owner.context(reads)
            if self.owner.continuity_link and method.__name__!="bootstrap":
                link=context["prior_generation_and_live_ancestry"]
                context["prior_generation_and_live_ancestry"]={
                    "root":link["root"],"actor":link["actor"],"resumption_chain_hash":link["resumption_chain_hash"],
                    "exact_link_digest":digest(link),"event_count":len(link["events"]),
                    "grade":"CANONICAL_ACTUAL_ANCESTRY_LINK_NOT_ACTOR_RECOLLECTION",
                    "retained_full_actual_link_in_owner_receipt_binding":True}
            result=method(context)
        except BaseException:
            if self.provider.current_attempt_id is not None:
                self.owner.record_checkpoint_update(self.provider.current_attempt_id,cycle_disposition="HELD_OR_FAILED")
            raise
        if self.provider.current_attempt_id is not None:
            self.owner.record_checkpoint_update(self.provider.current_attempt_id,cycle_disposition="CYCLE_RETURNED")
        return result
    def bootstrap(self):
        link=self.owner.continuity_link
        if link:require(self.owner.snapshot().state_hash==link["resumption_chain_hash"],
                        "GEN_LIVE_LINK_STALE_RESUMPTION")
        return self._run(self.cycle.bootstrap)
    def advance(self):return self._run(self.cycle.advance)
    def finish(self):return self._run(self.cycle.finish)
    def terminal_handoff(self):
        """Only an actually completed P2 cycle can yield a mode boundary."""
        store=self.cycle._load()
        require(store["phase"]=="COMPLETE" and store["pending"] is None and
                store["model_call"] is None,"GEN_HANDOFF_REQUIRES_TERMINAL")
        require(self.engine.verify(),"GEN_HANDOFF_JOURNAL_INVALID")
        state=self.owner.snapshot().document()
        require(state==store["expected_owner_state"],"GEN_HANDOFF_STATE_MOVED")
        return {"state":state,"cycle_digest":digest(store),
                "retrospectives_digest":digest(store["retrospectives"]),
                "grade":"SOURCEFREE_TERMINAL_GENERATION_MODE_BOUNDARY"}

    def close(self):self.engine.close();self.owner.close()


def _native_link_rows(tail):
    return [{"native_ref":e["id"],"chain_hash":e["chain_hash"],"clock":e["clock"],
             "kind":e["kind"],"actor":e["actor_id"],
             "actor_accessible":e["envelope"].get("payload",{}).get("private_actor_experience_receipts",{})}
            for e in tail]

def validate_actual_live_link(runtime,link):
    require(runtime.verify()["valid"],"GEN_LIVE_LINK_NATIVE_CHAIN")
    events=runtime.ledger.events()
    require(events[0]["chain_hash"]==link["root"],"GEN_LIVE_LINK_ROOT")
    state=link["prior_terminal"]["state"]
    require(state["root"]==link["root"] and state["actor"]==link["actor"],"GEN_LIVE_LINK_PRIOR_IDENTITY")
    a=[i for i,e in enumerate(events) if e["chain_hash"]==state["state_hash"]]
    b=[i for i,e in enumerate(events) if e["chain_hash"]==link["resumption_chain_hash"]]
    require(len(a)==len(b)==1 and a[0]<b[0],"GEN_LIVE_LINK_ANCESTRY")
    require(link["events"]==_native_link_rows(events[a[0]+1:b[0]+1]),"GEN_LIVE_LINK_FABRICATED_RECEIPT")
    return True

def link_actual_live_interval(runtime,handoff,prior_cycle_path,*,max_events=128):
    """Bind later generation to the same actual ledger after an explicit live mode.

    No human action is selected by the generation model. No prior-cycle
    event is rewritten. The native ledger is the durable ancestry; the
    caller retains the completed cycle/journal and separate live receipts.
    """
    store=json.loads(Path(prior_cycle_path).read_text())
    state=handoff["state"]
    require(handoff["cycle_digest"]==digest(store) and store["phase"]=="COMPLETE" and
            store["expected_owner_state"]==state and store["pending"] is None and
            store["model_call"] is None,"GEN_LIVE_LINK_PRIOR_CYCLE")
    require(runtime.verify()["valid"],"GEN_LIVE_LINK_NATIVE_CHAIN")
    events=runtime.ledger.events()
    require(events[0]["chain_hash"]==state["root"],"GEN_LIVE_LINK_ROOT")
    anchors=[i for i,e in enumerate(events) if e["chain_hash"]==state["state_hash"]]
    require(len(anchors)==1,"GEN_LIVE_LINK_MISSING_ANCESTOR")
    tail=events[anchors[0]+1:]
    require(0<len(tail)<=max_events,"GEN_LIVE_LINK_BOUNDED_ACTUAL_HISTORY")
    world=runtime.ledger.world(runtime.world_id)[1]
    require(not any(x.get("present") is True for x in world.get("neighbor_users",{}).values()),
            "GEN_LIVE_LINK_PRESENT_VISITOR")
    return detached({"root":state["root"],"actor":state["actor"],
        "prior_terminal":handoff,"resumption_chain_hash":events[-1]["chain_hash"],
        "events":_native_link_rows(tail),
        "grade":"ACTUAL_LEDGER_LINK_NOT_ACTOR_RECOLLECTION_OR_HUMAN_AUTHORITY"})
