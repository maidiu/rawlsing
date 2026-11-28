"""P2 recursion -> modern continuing organism, provisional sourcefree owner port.

The inherited RecursionCycle/BatchEngine still own call custody, order and
interruption holds. ConstitutiveRuntime still owns every actual world/actor
transition. A checkpoint proposes conditional actor-local policies, never
world outcomes or pre-issued future references. No remote call inside a step.
"""
from collections import Counter
import fcntl
import json
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

GRADE = "PROVISIONAL_SOURCEFREE_MODERN_GENERATION_PORT_NOT_NATIVE_OR_MODEL_ADEQUACY"
MAX_TEXT = 512
MAX_POLICY_ITEMS = 24

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
    require(exact_keys(policy,(),("actions","formation","expression")),"GEN_POLICY_SHAPE")
    actions=policy.get("actions",[])
    require(isinstance(actions,list) and len(actions)<=MAX_POLICY_ITEMS,"GEN_ACTION_POLICY_SIZE")
    for rule in actions:
        require(exact_keys(rule,("action",),("option_match","project_id","speech_intent")) and
                text(rule["action"],80),"GEN_ACTION_RULE")
        if "option_match" in rule:
            require(isinstance(rule["option_match"],dict) and bool(rule["option_match"]) and
                    set(rule["option_match"])<= {"project_id","world_request","binding_status",
                                               "grounds_status","operation"},
                    "GEN_ACTION_MATCH")
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
        if exact_keys(rule,("candidate",),("when",)):
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
            require(exact_keys(rule,("offer",),("match","augment")) and
                    isinstance(rule["offer"],str) and
                    rule["offer"].startswith(("historically_possible_","historically_proposed_")) and
                    isinstance(rule.get("match",{}),dict) and isinstance(rule.get("augment",{}),dict),
                    "GEN_NOMINATION_RULE")
            # Only semantic fields, never an invented source ref or owner basis.
            allowed={"interpretive_hypothesis","personal_significance","personal_sense",
                     "affect_name","course_orientation","priority","anticipated_availability",
                     "revision","new_relation","new_polarity"}
            require(set(rule.get("augment",{}))<=allowed,"GEN_NOMINATION_AUGMENT")

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
            for rule in policy.get("actions",[]):
                action=rule["action"]
                if not any(o.get("action")==action for o in packet.get("options",[])):
                    continue
                if "option_match" in rule:
                    rows=[o for o in packet.get("practical_options",[])
                          if o.get("operation")==action and subset(o,rule["option_match"])]
                    if len(rows)!=1:
                        self.routes["option_not_unique_or_absent"]+=1
                        continue
                    out={"task":task,"practical_option_id":rows[0]["option_id"]}
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
                if "candidate" in rule:
                    if subset(packet.get("experience",{}),rule.get("when",{})):
                        candidates.append(detached(rule["candidate"]))
                        self.routes["checkpoint_direct_candidate"]+=1
                else:
                    rows=[c for c in packet.get(rule["offer"],[]) if subset(c,rule.get("match",{}))]
                    if len(rows)!=1:
                        self.routes["nomination_not_unique_or_absent"]+=1
                        continue
                    c=detached(rows[0]);extra=rule.get("augment",{})
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
                 family_sources=()):
        require(sourcefree_attested is True,"GEN_SOURCEFREE_ATTESTATION_REQUIRED")
        self.rt=runtime;self.actor=actor
        self.rt.ledger.actor(actor)
        genesis=self.rt.ledger.events(limit=1)
        require(len(genesis)==1 and genesis[0]["kind"]=="INITIALIZATION","GEN_NO_GENESIS")
        self.root=genesis[0]["chain_hash"];self.branch="modern:"+runtime.world_id
        self.source_ref="SOURCEFREE_MODERN_ROOT:"+self.root
        self.period_catalog=detached(period_catalog or {})
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
        binding=canonical({"root":self.root,"branch":self.branch,"actor":actor,
                           "catalog":self.period_catalog,"family_sources":self.family_sources,"grade":GRADE})
        row=self.db.execute("SELECT value FROM binding WHERE id=1").fetchone()
        if row is None:self.db.execute("INSERT INTO binding VALUES (1,?)",(binding,))
        else:require(row[0]==binding,"GEN_RECEIPT_BINDING")
        self.db.commit()

    def snapshot(self):
        # Native verification binds current actors, world and entire ancestry.
        verified=self.rt.verify()
        require(verified.get("valid") is True,"GEN_NATIVE_CHAIN_INVALID")
        _,w=self.rt.ledger.world(self.rt.world_id)
        return StateIdentity(self.root,self.actor,self.branch,w["clock"],verified["last_hash"])

    def context(self):
        """Analyst-only, actor-separated working set; not a first-person account.
        Prior actual experience comes separately from inherited RecursionCycle.
        """
        now=self.snapshot()
        result={}
        for aid,a in self.rt.ledger.actors().items():
            situated=self.rt.situated(aid)
            result[aid]={"role":a["role"],"age_days":a["age_days"],"body":a["body"],
                         "location":a["location"],"projects":a.get("projects",[]),
                         "accessible_memories":[m for m in a.get("memories",[])
                                                if m.get("status")=="ACTOR_ACCESSIBLE"],
                         "analyst_only_historical_orientations":a.get("historical_orientations",[]),
                         "current_situated":situated}
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
                         "actor_contexts_are_separate_analyst_only_not_actor_self_report":True})

    def validate_proposal(self,p):
        require(p.operation in ("CONTINUE_ACTOR_LIFE","REALIZE_FAMILY_BIRTH"),"GEN_OPERATION")
        require(p.source_refs==(self.source_ref,),"GEN_SOURCE")
        roster=set(self.rt.ledger.actors())
        require(len(p.participants)==1 and p.participants[0] in roster,"GEN_PRINCIPAL")
        require(type(p.event_time) is int and p.event_time>self.snapshot().clock,"GEN_CLOCK")
        c=p.circumstances
        require(exact_keys(c,("policies",),("retrospective_event_id","rehearsal","period_ref","family")),
                "GEN_CIRCUMSTANCES")
        require(isinstance(c["policies"],dict) and set(c["policies"])<=roster,"GEN_POLICY_ACTOR")
        for policy in c["policies"].values():policy_check(policy)
        if p.interval is not None:
            require(exact_keys(p.interval,("mode","span")) and p.interval["mode"]=="ACTUAL" and
                    type(p.interval["span"]) is int and 1<=p.interval["span"]<=3650,"GEN_INTERVAL")
        if "period_ref" in c:
            require(p.interval is not None and c["period_ref"] in self.period_catalog,"GEN_PERIOD_REF")
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
            self.db.execute("INSERT INTO operations VALUES (?,?,?,NULL)",(operation_id,ph,before))
            self.db.commit()
            interval=None
            c=p.circumstances
            if span:
                interval=self.rt.background(span,processes=detached(self.period_catalog.get(c.get("period_ref"),[])))
            policy=ConditionalPolicy(c["policies"],c.get("rehearsal"),c.get("family"))
            old=self.rt.semantic
            step_event=None;out=None;family_result=None
            try:
                self.rt.semantic=ValidatingSemanticService(policy)
                if p.operation=="CONTINUE_ACTOR_LIFE":
                    out=self.rt.step(p.participants[0]) # no injected action, target or coactor
                    step_event=self.rt.ledger.events()[-1]
                    require(step_event["id"]==out["receipt"] and step_event["kind"]=="ACTOR_LIFE_TRANSITION",
                            "GEN_NATIVE_RECEIPT")
                family_result=self.family_transition(c.get("family"))
            finally:self.rt.semantic=old
            event=self.rt.ledger.events()[-1]
            after=self.snapshot()
            require(after.clock==p.event_time,"GEN_NATIVE_CLOCK")
            payload=step_event["envelope"]["payload"] if step_event else {}
            accessible={"objective_ref":payload.get("objective_ref",event["id"]),
                        "by_actor":detached(payload.get("private_actor_experience_receipts",{})),
                        "receipt_grade":GRADE}
            # A birth or genealogy binding is not an invented lived receipt.
            # Preserve the actual step separately from a same-clock family op.
            readset=tuple(dict.fromkeys([self.source_ref,
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
                 "remote_calls_during_event":0,"native_chain_hash":after.state_hash},
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
    def __init__(self,provider,*,max_request_bytes=1024*1024):
        require(hasattr(provider,"call"),"GEN_EXPLICIT_CALL_PROVIDER")
        self.provider=provider;self.max_request_bytes=max_request_bytes;self.attempts=[]
    def call(self,request):
        raw_bytes=len(canonical(request).encode("utf-8"))
        require(raw_bytes<=self.max_request_bytes,"GEN_CHECKPOINT_CONTEXT_LIMIT")
        rec={"mode":request["mode"],"request_bytes":raw_bytes,"outcome":"STARTED"}
        self.attempts.append(rec);start=perf_counter_ns()
        try:
            raw=detached(self.provider.call(detached(request)))
            rec["response_bytes"]=len(canonical(raw).encode("utf-8"))
            response=self.bind(request,raw)
            rec["outcome"]="RETURNED"
            return response
        finally:rec["elapsed_ns"]=perf_counter_ns()-start
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
        for p in pros:
            require(isinstance(p,dict) and isinstance(p.get("circumstances"),dict) and
                    isinstance(p.get("participants"),list) and len(p["participants"])==1,
                    "GEN_PROSPECTIVE_SURFACE")
            c=p["circumstances"]
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
        self.owner=owner;self.provider=CheckpointProvider(provider)
        self.engine=BatchEngine(owner,journal_path)
        self.cycle=RecursionCycle(self.engine,self.provider,cycle_path)
    def bootstrap(self):return self.cycle.bootstrap(self.owner.context())
    def advance(self):return self.cycle.advance(self.owner.context())
    def finish(self):return self.cycle.finish(self.owner.context())
    def close(self):self.engine.close();self.owner.close()
