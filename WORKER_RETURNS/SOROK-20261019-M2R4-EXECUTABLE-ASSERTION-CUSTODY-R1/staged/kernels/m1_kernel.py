"""M1 source-free interpretation-lineage candidate. Nothing here is an accepted owner."""
from __future__ import annotations
from dataclasses import dataclass, asdict, replace
from hashlib import sha256
import json

GRADE = "TEST_ONLY_INTERPRETATION_LINEAGE_CANDIDATE"
RULE = "M1_CANDIDATE_LINEAGE_RULE@0.1.0"
RULE_HASH = sha256(RULE.encode()).hexdigest()
MODES = ("REATTRIBUTE", "NARROW", "GENERALIZE", "REINFORCE", "CONTRADICT", "DIFFERENTIATE", "NO_CHANGE")
STANCES = ("ACCEPT", "REJECT", "SUSPEND")

class Refusal(ValueError):
    pass

def canonical(o):
    return json.dumps(o, sort_keys=True, ensure_ascii=True, separators=(',', ':'), allow_nan=False)

def digest(o):
    return sha256(canonical(o).encode()).hexdigest()

def require(ok, reason):
    if not ok: raise Refusal(reason)

@dataclass(frozen=True)
class History:
    id: str
    actor: str
    time: int
    activity: str
    witnessed: bool
    accessible: bool

@dataclass(frozen=True)
class Actor:
    id: str
    history: tuple[History, ...]
    access: tuple[str, ...]
    private_project: str
    age: int = 12
    background: str = "unspecified"

@dataclass(frozen=True)
class Event:
    id: str
    kind: str
    time: int
    observer: str
    participants: tuple[str, ...]
    material: tuple[str, ...]
    issuer: str = "TEST_ONLY_INDEPENDENT_WORLD_FIXTURE"
    action_owner: str | None = None
    action: str | None = None

@dataclass(frozen=True)
class Speech:
    id: str
    event: str
    speaker: str
    time: int
    words: str
    claim_ref: str  # asserted interpretation, NOT objective fact

@dataclass(frozen=True)
class Scene:
    actors: tuple[Actor, ...]
    events: tuple[Event, ...]
    speech: tuple[Speech, ...]

@dataclass(frozen=True)
class Candidate:
    id: str
    actor: str
    event: str
    source: str | None
    mode: str
    stance: str
    parent: str | None
    rule_hash: str = RULE_HASH

@dataclass(frozen=True)
class Interpretation:
    actor: str
    event: str
    version: int
    previous_hash: str | None
    candidate_hash: str
    source: str | None
    mode: str
    belief_stance: str
    affect_ref: str | None
    public_action_ref: str | None
    retained_procedure_refs: tuple[str, ...]
    actor_memory_access: str  # only 'NOT_GRANTED' here; ADP016/017 is external
    rule_hash: str
    provenance_refs: tuple[str, ...]
    hash: str

@dataclass(frozen=True)
class State:
    actor: str
    lineage: tuple[Interpretation, ...] = ()
    procedure_refs: tuple[str, ...] = ()
    def hash(self): return digest(asdict(self))


def validate(scene: Scene):
    ids = [a.id for a in scene.actors]
    require(len(ids) == len(set(ids)), "ACTOR_ID_COLLISION")
    evs = {e.id:e for e in scene.events}
    require(len(evs) == len(scene.events), "EVENT_ID_COLLISION")
    require(len({s.id for s in scene.speech}) == len(scene.speech), "SPEECH_ID_COLLISION")
    for a in scene.actors:
        require(a.private_project != "", "ACTOR_PROJECT_MISSING")
        for h in a.history:
            require(h.actor == a.id and h.time >= 0, "FOREIGN_ACTOR_HISTORY")
    for e in scene.events:
        require(e.issuer == "TEST_ONLY_INDEPENDENT_WORLD_FIXTURE", "UNOWNED_EVENT")
        require(e.observer in ids and all(x in ids for x in e.participants), "EVENT_ACTOR_UNBOUND")
        require(e.kind in ("LOSS", "ENCOUNTER", "ACTION"), "UNKNOWN_EVENT")
        require(not any(x.startswith("culprit:") or x.startswith("ideology:") for x in e.material), "MORAL_FACT_IN_EVENT")
        if e.action_owner:
            require(e.action_owner in e.participants and e.kind in ("ACTION", "ENCOUNTER"), "ACTION_OWNER_UNBOUND")
            actor = next(a for a in scene.actors if a.id == e.action_owner)
            require(any(h.activity == actor.private_project and h.witnessed and h.time < e.time for h in actor.history), "INDEPENDENT_ACTION_HISTORY_REQUIRED")
    for s in scene.speech:
        require(s.event in evs and s.speaker in ids and s.time >= evs[s.event].time, "SPEECH_PARENT_INVALID")
        require(s.claim_ref and not s.claim_ref.startswith("objective:"), "ATTRIBUTION_LAUNDERED")
    return evs


def eligible(scene: Scene, state: State, event_id: str):
    evs = validate(scene)
    require(event_id in evs and state.actor in [a.id for a in scene.actors], "UNKNOWN_EVENT_OR_ACTOR")
    e = evs[event_id]
    require(state.actor in e.participants and e.id in actor(scene,state.actor).access, "EVENT_NOT_ACTOR_ACCESSIBLE")
    # Candidate generation does not infer child beliefs from speakers, event label or demographics.
    own = actor(scene,state.actor)
    for ref in state.procedure_refs:
        require(any(h.id == ref and h.actor == own.id and h.witnessed and h.time < e.time for h in own.history), "PROCEDURAL_ORIGIN_UNBOUND")
    for index, record in enumerate(state.lineage):
        content=asdict(record); content.pop("hash")
        require(digest(content)==record.hash and record.actor==state.actor and record.version==index+1, "LINEAGE_INTEGRITY_FAILURE")
        require(record.previous_hash==(state.lineage[index-1].hash if index else None), "LINEAGE_PARENT_INVALID")
    if state.lineage:
        prior=evs.get(state.lineage[-1].event)
        require(prior is not None and prior.time < e.time, "HISTORICAL_TIME_ORDER")
    parent = state.lineage[-1].hash if state.lineage else None
    out = [Candidate(digest([state.actor,e.id,parent,"NONE"])[:20],state.actor,e.id,None,"NO_CHANGE","SUSPEND",parent)]
    if e.kind == "LOSS":
        # Condition eligibility on the child's *witnessed* earlier relation history,
        # without deriving a uniquely true story, affect or behavior from its label.
        for h in own.history:
            if h.time < e.time and h.witnessed and h.id.startswith("prior_"):
                token=digest(asdict(h))
                out.append(Candidate(digest([state.actor,e.id,parent,"PRIOR",token])[:20],state.actor,e.id,"history:"+token,"PROCEDURAL_RECRUITMENT","SUSPEND",parent))
        for s in scene.speech:
            if s.event == e.id and s.id in actor(scene,state.actor).access:
                for stance in STANCES:
                    out.append(Candidate(digest([state.actor,e.id,s.id,stance,parent])[:20],state.actor,e.id,s.id,"RECONSIDER",stance,parent))
    if e.kind in ("ENCOUNTER", "ACTION") and state.lineage:
        for mode in MODES:
            if mode == "NO_CHANGE": continue
            out.append(Candidate(digest([state.actor,e.id,mode,parent])[:20],state.actor,e.id,None,mode,"SUSPEND",parent))
    return tuple(out)


def actor(scene, actor_id):
    return next(a for a in scene.actors if a.id == actor_id)


def propose(scene, state, event_id, candidate_id, *, affect_ref=None, public_action_ref=None, model_packet=None):
    require(model_packet is None or (isinstance(model_packet,dict) and set(model_packet)=={"candidate_id","model_provenance"} and model_packet["candidate_id"]==candidate_id), "LLM_CAUSAL_AUTHORITY_FORBIDDEN")
    possible = eligible(scene,state,event_id)
    selected = next((c for c in possible if c.id == candidate_id),None)
    require(selected is not None, "CANDIDATE_NOT_ELIGIBLE")
    own = actor(scene,state.actor)
    if affect_ref is not None:
        require(any(h.id == affect_ref and h.actor == own.id and h.witnessed for h in own.history), "AFFECT_EVIDENCE_MISSING")
    if public_action_ref is not None:
        require(any(h.id == public_action_ref and h.actor == own.id and h.witnessed for h in own.history), "PUBLIC_ACTION_NOT_OWNED")
    return {"grade":GRADE,"actor":own.id,"event":event_id,"candidate":asdict(selected),"candidate_hash":digest(asdict(selected)),"affect_ref":affect_ref,"public_action_ref":public_action_ref,"state_before_hash":state.hash(),"possible_owner_effect":"CAN011_OR_ADP016_017_UNISSUED","no_actor_or_world_mutation":True}


def fixture_grant(proposal, scope_actor):
    """Only an explicit external *fixture* permit; no native CAN011 or memory authority."""
    require(proposal["actor"] == scope_actor and proposal["grade"] == GRADE, "GRANT_ACTOR_SCOPE_INVALID")
    return {"issuer":"M1_TEST_FIXTURE_AUTHORIZER_ONLY","scope_actor":scope_actor,"proposal_hash":digest(proposal),"rule_hash":RULE_HASH}


def append_test_only(scene, state, proposal, grant):
    """Append a research interpretation record, not a canonical psychological effect."""
    require(grant == fixture_grant(proposal,state.actor), "OWNER_PERMISSION_NOT_GRANTED")
    require(proposal["state_before_hash"] == state.hash(), "STALE_LINEAGE_STATE")
    c=proposal["candidate"]
    require(proposal["candidate_hash"] == digest(c) and c["rule_hash"] == RULE_HASH, "CANDIDATE_HASH_OR_RULE")
    new=propose(scene,state,c["event"],c["id"],affect_ref=proposal["affect_ref"],public_action_ref=proposal["public_action_ref"])
    require(new==proposal, "PROPOSAL_RECOMPUTATION_FAILED")
    previous=state.lineage[-1].hash if state.lineage else None
    require(c["parent"]==previous, "LINEAGE_PARENT_MISMATCH")
    fields={"actor":state.actor,"event":c["event"],"version":len(state.lineage)+1,"previous_hash":previous,
        "candidate_hash":proposal["candidate_hash"],"source":c["source"],"mode":c["mode"],"belief_stance":c["stance"],
        "affect_ref":proposal["affect_ref"],"public_action_ref":proposal["public_action_ref"],
        "retained_procedure_refs":state.procedure_refs,"actor_memory_access":"NOT_GRANTED","rule_hash":RULE_HASH,
        "provenance_refs":(proposal["event"],proposal["candidate_hash"],grant["proposal_hash"])}
    record=Interpretation(**fields,hash=digest(fields))
    return replace(state,lineage=state.lineage+(record,))


def seed_scene(*, child_history="cooperative", parent_history="care_work", peer_speech=True, child_access_peer=True, other_action="REFUSE", age=12, background="any"):
    """Synthetic witnessed histories. Changing demographics alone cannot change possibilities."""
    child=Actor("child",(
        History("prior_recognition","child",1,child_history,True,False),
        History("old_watchful_habit","child",2,"guard_property",True,False),
        History("first_distress","child",4,"bodily_grief",True,True),
        History("public_lock_check","child",5,"lock_inspection",True,True)),
        ("loss","parent_said")+(("peer_said",) if child_access_peer else ())+("later",),"repair_bicycle",age,background)
    caregiver=Actor("caregiver",(History("care_work_history","caregiver",1,parent_history,True,False),), ("loss",),"care_work",42,background)
    peer=Actor("peer",(History("peer_debate","peer",1,"school_club",True,False),),("loss",),"school_club",13,background)
    other=Actor("other_P",(History("other_project","other_P",3,"own_music_project",True,False),),("later",),"own_music_project",19,background)
    loss=Event("loss","LOSS",3,"child",("child","caregiver","peer"),("bike","garage","loss_of_transport"))
    later=Event("later","ENCOUNTER",9,"child",("child","other_P"),("community_hall",),action_owner="other_P",action=other_action)
    speech=[Speech("parent_said","loss","caregiver",4,"Someone could be in need.","parent_need_account")]
    if peer_speech:speech.append(Speech("peer_said","loss","peer",5,"It must be that group.","peer_group_blame"))
    return Scene((child,caregiver,peer,other),(loss,later),tuple(speech))
