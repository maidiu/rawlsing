"""S51 bounded retained-object relevance experiment over actual S49 root."""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from .bootstrap import install
install()

from bp4.world import make_event, owner_receipt, validate_owner_receipt  # noqa: E402
from candidate import digest  # noqa: E402
from candidate.actor_access_response import make_actor_local_access_witness  # noqa: E402
from s49.session import S49Session  # noqa: E402
from s49.actor import record_b_observation  # noqa: E402
from s39.sources import make_source  # noqa: E402
from lab_sgi1.history import replay_history  # noqa: E402
from lab_sgi1.joint import material_joint_opportunity, verify_material_source  # noqa: E402

S51="SOROK_S51_SITUATED_OBJECT_RELEVANCE@1"
HYPOTHESIS_KIND="S51_RETAINED_OBJECT_HYPOTHESIS"
HYPOTHESIS_LIFECYCLE_KIND="S51_RETAINED_OBJECT_HYPOTHESIS_LIFECYCLE"
OFFER_KIND="S51_WORLD_OFFER"
ACCESS_KIND="S51_ACTOR_ACCESS"
RELEVANCE_KIND="S51_OBJECT_RELEVANCE"
CONSUMER_KIND="S51_S49_CONSUMER_BINDING"
RULE_ID="S51_OBJECT_RELEVANCE_TO_S49@1"
GRADE="TEST_ONLY_S51_RETAINED_OBJECT_HYPOTHESIS_NOT_NATIVE"
ACTUAL_HOLD="S51_ACTUAL_CURRENT_PURPOSE_STILL_UNPROVED"
OFFER_ACTOR="G15_INDEPENDENT_MATERIAL_OBSERVER"


class S51Refusal(ValueError):
 def __init__(self,code,detail=""):
  super().__init__(code if not detail else f"{code}: {detail}")
  self.code=code


class S51Session(S49Session):
 def _append(self,kind,body):
  ep=self.product._append_episode(self.branch_id,"B",kind,self.clock(),dict(body))
  self.product._checkpoint(self.branch_id,self.clock(),self.world())
  return ep

 def _append_event(self,event,*,perceive=()):
  result=super()._append_event(event,perceive=perceive)
  if "B" in perceive:
   self._note_b_received_event(event)
  return result

 def _perceive_if_present(self,event,*actors):
  super()._perceive_if_present(event,*actors)
  if "B" in actors:
   self._note_b_received_event(event)

 def _note_b_received_event(self,event):
  active=self._active_hypothesis()
  if not active: return
  baseline=active.get("b_perception_baseline")
  if not isinstance(baseline,int): return
  perceptions=self.product.store.perceptions(self.branch_id,"B")
  indexes=[i for i,row in enumerate(perceptions) if row.get("event_id")==event.get("event_id")]
  if not indexes or indexes[0]!=baseline: return
  stored=self.event(event.get("event_id","")) or event
  body=stored.get("body") or {}
  common={"schema":S51,"hypothesis_id":active["hypothesis_id"],
   "hypothesis_episode_id":active["episode_id"],
   "received_event_id":stored.get("event_id",""),"received_event_hash":stored.get("hash",""),
   "received_event_clock":stored.get("clock"),"native":False}
  if body.get("schema")=="S51_PUBLISHED_OFFER_EVENT@1":
   common.update({"status":"BOUND","reason":"NEXT_RECEIVED_EVENT_IS_OFFER",
    "bound_event_id":stored.get("event_id","")})
  else:
   common.update({"status":"EXPIRED","reason":"NEXT_RECEIVED_EVENT_NOT_OFFER"})
  self._append(HYPOTHESIS_LIFECYCLE_KIND,common)

 def _expire_hypothesis(self,hypothesis,*,reason,event_id=""):
  self._append(HYPOTHESIS_LIFECYCLE_KIND,{"schema":S51,
   "hypothesis_id":hypothesis["hypothesis_id"],
   "hypothesis_episode_id":hypothesis["episode_id"],
   "status":"EXPIRED","reason":reason,"received_event_id":event_id,"native":False})

 def _episodes(self,kind):
  return [row for row in self.product.store.episodes(self.branch_id) if row.get("kind")==kind]

 def _episode(self,kind,episode_id):
  for row in self._episodes(kind):
   if row.get("episode_id")==episode_id:
    return row
  raise S51Refusal("S51_CANONICAL_EPISODE_MISSING",str(episode_id))

 def _latest_body(self,kind,hypothesis_id):
  rows=[row for row in self._episodes(kind) if (row.get("body") or {}).get("hypothesis_id")==hypothesis_id]
  return dict(rows[-1].get("body") or {}) if rows else None

 def _hypothesis_status(self,hypothesis_id):
  life=self._latest_body(HYPOTHESIS_LIFECYCLE_KIND,hypothesis_id)
  return str((life or {}).get("status") or "ACTIVE")

 def _active_hypothesis(self):
  rows=self._episodes(HYPOTHESIS_KIND)
  for row in reversed(rows):
   body=dict(row.get("body") or {})
   if self._hypothesis_status(body.get("hypothesis_id",""))=="ACTIVE":
    body["episode_id"]=row["episode_id"]
    return body
  return None

 def recover_object(self)->dict:
  life=self.product.seed.life
  events=list(getattr(life,"b_events",[]) or [])
  if not events: raise S51Refusal("S51_B_HISTORY_MISSING")
  replay=replay_history(events)
  if not replay.get("valid"): raise S51Refusal("S51_B_HISTORY_INVALID:"+str(replay.get("errors")))
  rows=[e for e in events if e.get("kind")=="STRIVING" and e.get("event_id") in replay.get("admitted",{})]
  if len(rows)!=1: raise S51Refusal("S51_B_STRIVING_NOT_UNIQUE")
  event=rows[0]
  if (event.get("payload") or {}).get("striving")!="fund_finishing_equipment": raise S51Refusal("S51_OBJECT_NOT_EXPECTED")
  parents=list(event.get("causal_parent_event_ids") or [])
  if len(parents)!=2: raise S51Refusal("S51_OBJECT_PARENT_COUNT")
  parent_rows=[replay["admitted"].get(x) for x in parents]
  if any(x is None for x in parent_rows): raise S51Refusal("S51_OBJECT_PARENT_MISSING")
  work=next((x for x in parent_rows if x.get("kind")=="WORK_POSITION"),None)
  project=next((x for x in parent_rows if x.get("kind")=="PROJECT"),None)
  if not work or not project: raise S51Refusal("S51_OBJECT_PARENT_TYPES")
  witness=next((w for w in replay["value_witnesses"] if w["event_id"]==event["event_id"]),None)
  if not witness: raise S51Refusal("S51_OBJECT_WITNESS_MISSING")
  routes=[e for e in events if e.get("kind")=="ROUTE_AVAILABILITY" and e.get("event_id") in replay.get("admitted",{})]
  used=[e for e in routes if (replay["effects"].get(e["event_id"]) or {}).get("goal")==event["payload"]["striving"]]
  if not used: raise S51Refusal("S51_OBJECT_ROUTE_USAGE_MISSING")
  return {"schema":"S51_RECOVERED_OBJECT@1","actor_id":event.get("actors",[None])[0],
   "object_event_id":event["event_id"],"object_hash":event["event_id"],"striving":event["payload"]["striving"],
   "effective_index":event.get("effective_index"),"owner_id":event.get("owner_id"),
   "causal_parent_event_ids":parents,"work_parent_event_id":work["event_id"],"project_parent_event_id":project["event_id"],
   "replay_witness":witness,"route_usage":[{"event_id":e["event_id"],"route":(e.get("payload") or {}).get("route"),"effect":replay["effects"][e["event_id"]]} for e in used],
   "source_grade":"SOURCEFREE_RESEARCH_INPUT","native":False,"native_purpose_proof":False}

 def _canonical_object(self,obj:Mapping[str,Any])->dict:
  actual=self.recover_object()
  if not isinstance(obj,Mapping):
   raise S51Refusal("S51_OBJECT_INPUT_INVALID")
  for key in ("object_event_id","object_hash","actor_id","striving"):
   if obj.get(key)!=actual.get(key):
    raise S51Refusal("S51_FOREIGN_RETAINED_OBJECT",str(key))
  return actual

 def declare_hypothesis(self,obj:Mapping[str,Any])->dict:
  try:
   obj=self._canonical_object(obj)
  except S51Refusal as exc:
   return {"schema":S51,"status":"S51_FOREIGN_INPUT_REFUSED","reason":exc.code,
    "object_event_id":(obj or {}).get("object_event_id"),"native":False}
  for active in self._episodes(HYPOTHESIS_KIND):
   body=dict(active.get("body") or {})
   if self._hypothesis_status(body.get("hypothesis_id","")) in {"ACTIVE","BOUND"}:
    self._append(HYPOTHESIS_LIFECYCLE_KIND,{"schema":S51,"hypothesis_id":body.get("hypothesis_id"),
     "hypothesis_episode_id":active["episode_id"],"status":"EXPIRED","reason":"NEW_CANONICAL_DECLARATION","native":False})
  seq=len(self._episodes(HYPOTHESIS_KIND))
  baseline=len(self.product.store.perceptions(self.branch_id,"B"))
  h={"schema":S51,"stage":"RETAINED_OBJECT_HYPOTHESIS","hypothesis_id":"S51_HYPOTHESIS_"+str(obj["object_event_id"]).split(":")[-1][:12]+"_"+str(seq),
   "hypothesis_version":"R1","rule_id":RULE_ID,"actor_id":obj["actor_id"],"root_hash":self.read_root()["root_hash"],
   "root_id":self.read_root()["root_id"],"branch_id":self.branch_id,"object_event_id":obj["object_event_id"],
   "object_hash":obj["object_hash"],"object_striving":obj["striving"],"scope":"ONE_SUBSEQUENT_RECEIVED_EVENT",
   "expires_after_events":1,"b_perception_baseline":baseline,"status":"DECLARED_IMMUTABLE","native":False,"psychology_claim":False,"actor_testimony":False,
   "actual_current_purpose_proved":False,"grade":GRADE}
  ep=self._append(HYPOTHESIS_KIND,h);return {**h,"episode_id":ep["episode_id"]}

 def _canonical_hypothesis(self,hypothesis:Mapping[str,Any],*,allow_consumed=False,allow_inactive=False)->dict:
  if not isinstance(hypothesis,Mapping) or not hypothesis.get("episode_id"):
   raise S51Refusal("S51_FOREIGN_HYPOTHESIS")
  row=self._episode(HYPOTHESIS_KIND,hypothesis["episode_id"])
  body=dict(row.get("body") or {})
  actual=self.recover_object()
  if (
   body.get("object_event_id")!=actual["object_event_id"]
   or body.get("object_hash")!=actual["object_hash"]
   or body.get("actor_id")!=actual["actor_id"]
   or body.get("rule_id")!=RULE_ID
   or body.get("root_hash")!=self.read_root()["root_hash"]
   or body.get("branch_id")!=self.branch_id
  ):
   raise S51Refusal("S51_FOREIGN_HYPOTHESIS_PARENT")
  status=self._hypothesis_status(body.get("hypothesis_id",""))
  if status=="WITHDRAWN" and not allow_inactive:
   raise S51Refusal("S51_HYPOTHESIS_WITHDRAWN",str(body.get("hypothesis_id")))
  if status=="EXPIRED" and not allow_inactive:
   raise S51Refusal("S51_HYPOTHESIS_EXPIRED",str(body.get("hypothesis_id")))
  if status=="CONSUMED" and not allow_consumed:
   raise S51Refusal("S51_HYPOTHESIS_CONSUMED",str(body.get("hypothesis_id")))
  if status=="BOUND":
   life=self._latest_body(HYPOTHESIS_LIFECYCLE_KIND,body.get("hypothesis_id","")) or {}
   body["bound_event_id"]=life.get("bound_event_id","")
   body["bound_event_clock"]=life.get("received_event_clock")
  if status not in {"ACTIVE","BOUND","CONSUMED"} and not (
   allow_inactive and status in {"EXPIRED","WITHDRAWN"}
  ):
   raise S51Refusal("S51_HYPOTHESIS_NOT_ACTIVE",str(body.get("hypothesis_id")))
  body["episode_id"]=row["episode_id"]
  return body

 def withdraw_hypothesis(self,hypothesis:Mapping[str,Any])->dict:
  canonical=self._canonical_hypothesis(hypothesis)
  self._append(HYPOTHESIS_LIFECYCLE_KIND,{"schema":S51,"hypothesis_id":canonical["hypothesis_id"],
   "hypothesis_episode_id":canonical["episode_id"],"status":"WITHDRAWN","reason":"EXPLICIT_WITHDRAWAL","native":False})
  return {"schema":S51,"hypothesis_id":canonical["hypothesis_id"],"status":"WITHDRAWN","native":False}

 def _consume_hypothesis(self,hypothesis,relevance_hash,event_id=""):
  self._append(HYPOTHESIS_LIFECYCLE_KIND,{"schema":S51,"hypothesis_id":hypothesis["hypothesis_id"],
   "hypothesis_episode_id":hypothesis["episode_id"],"status":"CONSUMED","reason":"ONE_SUBSEQUENT_RECEIVED_EVENT",
   "consumed_by_relevance_hash":relevance_hash,"received_event_id":event_id,"native":False})

 def _actor_access(self,event_ref:str,offer:Mapping[str,Any])->dict:
  # Compatibility entry point: an access is only synthesized from the
  # published offer event and B's recorded perception of that exact event.
  source_id=(offer or {}).get("event_id")
  rows=[row for row in self._episodes(OFFER_KIND) if (row.get("body") or {}).get("offer_event_id")==source_id]
  if not rows:
   raise S51Refusal("S51_ACCESS_REQUIRES_PUBLISHED_OFFER",str(event_ref))
  canonical=dict(rows[-1]["body"]); canonical["episode_id"]=rows[-1]["episode_id"]
  access=self._offer_access(canonical)
  if access is None:
   raise S51Refusal("S51_ACCESS_NOT_WITNESSED")
  return access

 def issue_offer(self,*,permit=True,payment=2,hours=1,receive=True)->dict:
  seq=len(self._episodes(OFFER_KIND))
  material=material_joint_opportunity(effective_index=self.clock()+seq,permit=permit,units=1,payment_per_actor=payment,task_hours=hours)
  accepted,reason,_=verify_material_source(material)
  if not accepted: raise S51Refusal("S51_OFFER_SOURCE_INVALID",str(reason))
  world=self.world(); location="workshop"; clock=world.clock
  receipt=owner_receipt(act="REPAIR",actor_id=OFFER_ACTOR,clock=clock,location=location)
  event=make_event(clock=clock,kind="REPAIR",actor_id=OFFER_ACTOR,location=location,
   summary="The independent material observer publishes a bounded paid task offer.",
   body={"schema":"S51_PUBLISHED_OFFER_EVENT@1","offer_event_id":material["event_id"],
     "material_source":material,"offer":{k:material[k] for k in ("owner_id","place","payment_per_actor","task_hours","permit","material_units","effective_index")},
     "source_grade":material["source_receipt"].get("source_grade")},
   receipt=receipt,sequence=len(world.events))
  world.add_event(event)
  self.product._checkpoint(self.branch_id,self.clock(),world)
  self._append_event(event,perceive=("B",) if receive else ())
  body={"schema":S51,"stage":"WORLD_OFFER","offer":material,"offer_event_id":material["event_id"],
   "world_event_id":event["event_id"],"world_event_hash":event["hash"],"owner_id":material["owner_id"],
   "world_owner_receipt":receipt,"native":False,"performance_performed":False,"actor_willingness_claim":False}
  ep=self._append(OFFER_KIND,body);return {**body,"episode_id":ep["episode_id"]}

 def _canonical_offer(self,offer:Mapping[str,Any])->dict:
  if not isinstance(offer,Mapping) or not offer.get("episode_id"):
   raise S51Refusal("S51_FOREIGN_OFFER")
  row=self._episode(OFFER_KIND,offer["episode_id"])
  body=dict(row.get("body") or {})
  material=body.get("offer") or {}
  accepted,reason,_=verify_material_source(material)
  if not accepted: raise S51Refusal("S51_OFFER_SOURCE_INVALID",str(reason))
  event=self.event(body.get("world_event_id",""))
  if not event or event.get("hash")!=body.get("world_event_hash"):
   raise S51Refusal("S51_OFFER_EVENT_MISSING")
  expected=event.get("body") or {}
  if expected.get("material_source")!=material or expected.get("offer_event_id")!=material.get("event_id"):
   raise S51Refusal("S51_OFFER_EVENT_SUBSTITUTED")
  if event.get("actor_id")!=OFFER_ACTOR or event.get("location")!="workshop":
   raise S51Refusal("S51_OFFER_WORLD_OWNER_MISMATCH")
  try:
   validate_owner_receipt(event.get("owner_receipt"),actor_id=OFFER_ACTOR,act=event.get("kind"),clock=event.get("clock"))
  except Exception as exc:
   raise S51Refusal("S51_OFFER_WORLD_RECEIPT_INVALID",str(exc))
  if event.get("clock")>self.clock(): raise S51Refusal("S51_OFFER_CLOCK_FUTURE")
  body["episode_id"]=row["episode_id"]
  return body

 def _offer_access(self,offer)->dict|None:
  rows=[row for row in self.product.store.perceptions(self.branch_id,"B") if row.get("event_id")==offer.get("world_event_id")]
  if not rows: return None
  row=rows[-1]; actor=(self.world().actor_state.get("B") or {}).get("actor_id")
  if not actor: raise S51Refusal("S51_B_ACTOR_MISSING")
  access=make_actor_local_access_witness(actor_id=actor,event_ref=offer["world_event_id"],access_time=int(row.get("clock",self.clock())),
   source_ref="S51_ACCESS_"+str(offer["world_event_id"]).split("_")[-1][:16],access_status="ACCESSIBLE",
   scene=str(row.get("channel", "workshop")),content={"received_offer_event_id":offer["world_event_id"],
   "material_event_id":offer["offer_event_id"],"received_world_event_id":offer["world_event_id"],"received_world_event_hash":offer["world_event_hash"],
   "perception_clock":row.get("clock"),"perception_channel":row.get("channel"),"observer":"B"})
  ep=self._append(ACCESS_KIND,{"schema":S51,"access":access,"actor_id":actor,"event_ref":offer["world_event_id"],
   "offer_event_id":offer["offer_event_id"],"native":False})
  return {**access,"episode_id":ep["episode_id"],"offer_episode_id":offer["episode_id"]}

 def _canonical_access(self,access:Mapping[str,Any]|None,offer:Mapping[str,Any])->dict:
  if access is None: raise S51Refusal("S51_ACCESS_MISSING")
  if not isinstance(access,Mapping) or not access.get("episode_id"):
   raise S51Refusal("S51_FOREIGN_ACCESS")
  row=self._episode(ACCESS_KIND,access["episode_id"])
  body=dict(row.get("body") or {})
  witness=body.get("access") or {}
  if body.get("event_ref")!=offer.get("world_event_id") or body.get("offer_event_id")!=offer.get("offer_event_id"):
   raise S51Refusal("S51_ACCESS_OFFER_MISMATCH")
  actor=(self.world().actor_state.get("B") or {}).get("actor_id")
  content=witness.get("content") or {}
  if (
   witness.get("access_status")!="ACCESSIBLE"
   or witness.get("event_ref")!=offer.get("world_event_id")
   or witness.get("actor_id")!=actor
   or content.get("received_offer_event_id")!=offer.get("world_event_id")
   or content.get("received_world_event_hash")!=offer.get("world_event_hash")
  ):
   raise S51Refusal("S51_ACCESS_NOT_WITNESSED")
  rows=[r for r in self.product.store.perceptions(self.branch_id,"B") if r.get("event_id")==offer.get("world_event_id")]
  if not rows: raise S51Refusal("S51_ACCESS_PERCEPTION_MISSING")
  perception=rows[-1]
  if int(content.get("perception_clock",-1))!=int(perception.get("clock",-2)):
   raise S51Refusal("S51_ACCESS_CLOCK_MISMATCH")
  witness["episode_id"]=row["episode_id"];return witness

 def evaluate(self,obj,hypothesis,offer,access,*,hypothesis_active=True)->dict:
  try:
   return self._evaluate_canonical(obj,hypothesis,offer,access)
  except S51Refusal as exc:
   relation={
    "S51_HYPOTHESIS_WITHDRAWN":"HYPOTHESIS_WITHDRAWN",
    "S51_HYPOTHESIS_EXPIRED":"HYPOTHESIS_EXPIRED",
    "S51_HYPOTHESIS_CONSUMED":"HYPOTHESIS_CONSUMED",
    "S51_HYPOTHESIS_NOT_ACTIVE":"HYPOTHESIS_INACTIVE",
   }.get(exc.code,"FOREIGN_INPUT")
   return {"schema":S51,"status":"OBJECT_RELEVANCE_HOLD","relation":relation,
    "reason":exc.code,"object_event_id":(obj or {}).get("object_event_id"),
    "offer_event_id":(offer or {}).get("offer_event_id"),
    "actor_id":(self.world().actor_state.get("B") or {}).get("actor_id"),
    "hypothesis_active":False,"reasons":[],"native":False,"selected_action":None,"performed":False}

 def _evaluate_canonical(self,obj,hypothesis,offer,access)->dict:
  if not hypothesis:
   return {"schema":S51,"status":"OBJECT_RELEVANCE_HOLD","relation":"HYPOTHESIS_ABSENT",
    "object_event_id":(obj or {}).get("object_event_id"),"offer_event_id":(offer or {}).get("offer_event_id"),
    "actor_id":(self.world().actor_state.get("B") or {}).get("actor_id"),"hypothesis_active":False,
    "reasons":[],"native":False,"selected_action":None,"performed":False}
  obj=self._canonical_object(obj); hypothesis=self._canonical_hypothesis(hypothesis)
  offer=self._canonical_offer(offer)
  access=self._canonical_access(access,offer) if access is not None else None
  if hypothesis.get("bound_event_id") and hypothesis["bound_event_id"]!=offer["world_event_id"]:
   self._expire_hypothesis(hypothesis,reason="BOUND_EVENT_WAS_NOT_OFFER",event_id=offer["world_event_id"])
   return {"schema":S51,"status":"OBJECT_RELEVANCE_HOLD","relation":"HYPOTHESIS_EXPIRED",
    "reason":"S51_HYPOTHESIS_BOUND_EVENT_MISMATCH","object_event_id":obj["object_event_id"],
    "offer_event_id":offer["offer_event_id"],"actor_id":(self.world().actor_state.get("B") or {}).get("actor_id"),
    "hypothesis_active":False,"reasons":[],"native":False,"selected_action":None,"performed":False}
  actors=(self.world().actor_state.get("B") or {}); actor_id=actors.get("actor_id")
  actor_free_hours=actors.get("free_hours")
  checkpoint=self.product.store.checkpoints(self.branch_id)[-1]
  relation,status=self._relation_for(offer,access,actor_free_hours)
  p=offer.get("offer") or {}
  result={"schema":S51,"status":status,"relation":relation,"actor_id":actor_id,"object_event_id":obj["object_event_id"],
   "object_striving":obj["striving"],"offer_event_id":offer["offer_event_id"],"world_offer_event_id":offer["world_event_id"],
   "access_ref":(access or {}).get("source_ref",""),"hypothesis_id":hypothesis.get("hypothesis_id"),
   "hypothesis_active":True,"hypothesis_scope":hypothesis.get("scope"),
   "financial":{k:p.get(k) for k in ("payment_per_actor","task_hours","permit")},
   "actor_free_hours":actor_free_hours,"native":False,"selected_action":None,"performed":False,
   "actual_current_purpose_proved":False,"reasons":[]}
  result["relevance_hash"]=digest({**result,"episode_id":""})
  body={"schema":S51,"stage":"OBJECT_RELEVANCE","result":dict(result),"object":obj,"offer":offer,"access":access,
   "hypothesis":hypothesis,"evaluation_clock":self.clock(),"evaluation_checkpoint_hash":checkpoint.get("hash",""),
   "rule_id":RULE_ID,"native":False}
  ep=self._append(RELEVANCE_KIND,body);result["episode_id"]=ep["episode_id"]
  if status=="RELEVANCE_WARRANTED":
   self._consume_hypothesis(hypothesis,result["relevance_hash"],event_id=offer["world_event_id"])
  return result

 def _relation_for(self,offer,access,actor_free_hours):
  p=offer.get("offer") or {}
  if access is None or access.get("access_status")!="ACCESSIBLE":
   return "NOT_RECEIVED","NOT_RECEIVED"
  if p.get("permit") is not True:
   return "OBSTRUCTS","RELEVANCE_WARRANTED"
  if not isinstance(actor_free_hours,int):
   return "UNKNOWN","RELEVANCE_WARRANTED"
  if p.get("payment_per_actor") is None or p.get("task_hours") is None:
   return "UNKNOWN","RELEVANCE_WARRANTED"
  if int(p.get("payment_per_actor",0))<=0:
   return "OBSTRUCTS","RELEVANCE_WARRANTED"
  if int(p.get("task_hours",0))>int(actor_free_hours):
   return "OBSTRUCTS","RELEVANCE_WARRANTED"
  return "FACILITATES","RELEVANCE_WARRANTED"

 def _canonical_relevance(self,relevance:Mapping[str,Any])->dict:
  if not isinstance(relevance,Mapping) or not relevance.get("episode_id"):
   raise S51Refusal("S51_FOREIGN_RELEVANCE")
  row=self._episode(RELEVANCE_KIND,relevance["episode_id"])
  body=dict(row.get("body") or {}); result=dict(body.get("result") or {})
  if result.get("relevance_hash")!=relevance.get("relevance_hash") or body.get("rule_id")!=RULE_ID:
   raise S51Refusal("S51_RELEVANCE_SUBSTITUTED")
  obj=self._canonical_object(body.get("object") or {})
  hypothesis=self._canonical_hypothesis(body.get("hypothesis") or {},allow_consumed=True,allow_inactive=True)
  offer=self._canonical_offer(body.get("offer") or {})
  access=self._canonical_access(body.get("access"),offer) if body.get("access") is not None else None
  checkpoint_hash=body.get("evaluation_checkpoint_hash")
  checkpoint=next((c for c in self.product.store.checkpoints(self.branch_id) if c.get("hash")==checkpoint_hash),None)
  if not checkpoint:
   raise S51Refusal("S51_RELEVANCE_READSET_MISSING")
  if checkpoint.get("clock")!=body.get("evaluation_clock"):
   raise S51Refusal("S51_RELEVANCE_READSET_CLOCK_MISMATCH")
  state=checkpoint.get("state") or {}
  actor_state=(((state.get("actors") or {}).get("B") or {}).get("state") or {})
  actor_free_hours=actor_state.get("free_hours")
  actor_id=actor_state.get("actor_id")
  relation,status=self._relation_for(offer,access,actor_free_hours)
  p=offer.get("offer") or {}
  expected={
   "schema":S51,"status":status,"relation":relation,"actor_id":actor_id,
   "object_event_id":obj["object_event_id"],"object_striving":obj["striving"],
   "offer_event_id":offer["offer_event_id"],"world_offer_event_id":offer["world_event_id"],
   "access_ref":(access or {}).get("source_ref",""),"hypothesis_id":hypothesis["hypothesis_id"],
   "hypothesis_active":True,"hypothesis_scope":hypothesis.get("scope"),
   "financial":{k:p.get(k) for k in ("payment_per_actor","task_hours","permit")},
   "actor_free_hours":actor_free_hours,"native":False,"selected_action":None,"performed":False,
   "actual_current_purpose_proved":False,"reasons":[],
  }
  for key,value in expected.items():
   if result.get(key)!=value:
    raise S51Refusal("S51_RELEVANCE_SEMANTIC_MISMATCH",str(key))
  expected_hash=digest({**expected,"episode_id":""})
  if result.get("relevance_hash")!=expected_hash:
   raise S51Refusal("S51_RELEVANCE_HASH_INVALID")
  if status=="RELEVANCE_WARRANTED":
   life=self._latest_body(HYPOTHESIS_LIFECYCLE_KIND,hypothesis["hypothesis_id"]) or {}
   if (
    life.get("status")!="CONSUMED"
    or life.get("consumed_by_relevance_hash")!=result.get("relevance_hash")
    or life.get("received_event_id")!=offer["world_event_id"]
   ):
    raise S51Refusal("S51_RELEVANCE_LIFECYCLE_MISMATCH")
  result["episode_id"]=row["episode_id"];return result

 def consume_generation(self,obj,hypothesis,offer,access,relevance,*,repertoire=None)->dict:
  try:
   return self._consume_generation_canonical(obj,hypothesis,offer,access,relevance,repertoire=repertoire)
  except S51Refusal as exc:
   return {"schema":S51,"selection_status":"S51_INPUT_REFUSED","reason":exc.code,
    "source_ref":"","reasons":[],"selected_option":"","native":False}

 def _consume_generation_canonical(self,obj,hypothesis,offer,access,relevance,*,repertoire=None)->dict:
  obj=self._canonical_object(obj); hypothesis=self._canonical_hypothesis(hypothesis,allow_consumed=True)
  offer=self._canonical_offer(offer); access=self._canonical_access(access,offer)
  relevance=self._canonical_relevance(relevance)
  life=self._latest_body(HYPOTHESIS_LIFECYCLE_KIND,hypothesis["hypothesis_id"]) or {}
  if life.get("status")!="CONSUMED" or life.get("consumed_by_relevance_hash")!=relevance.get("relevance_hash"):
   raise S51Refusal("S51_HYPOTHESIS_RELEVANCE_LINK_MISMATCH")
  actor=(self.world().actor_state.get("B") or {}).get("actor_id")
  source=make_source(source_ref="S51_SOURCE_"+str(obj["object_event_id"]).split(":")[-1][:16],
   source_class="HISTORICAL_EPISODE",actor_id=actor,branch_id=self.branch_id,as_of=self.clock(),
   predicate="S51_OBJECT_RELEVANCE",value=1,
   content={"object_event_id":obj["object_event_id"],"offer_event_id":offer["offer_event_id"],
    "world_offer_event_id":offer["world_event_id"],"relation":relevance["relation"],
    "hypothesis_id":hypothesis["hypothesis_id"],"relevance_hash":relevance["relevance_hash"],
    "access_ref":access.get("source_ref")})
  # The canonical S49 turn is the consumer. No generic reason channel is used.
  record_b_observation(self)
  s49=self.produce_b_turn(controlled=True,source_records_override=[source],repertoire=repertoire)
  turn=[row for row in self._episodes("S49_B_ACTOR_TURN") if (row.get("body") or {}).get("generation",{}).get("hash")]
  gen=dict((turn[-1].get("body") or {}).get("generation") or {}) if turn else {}
  body={"schema":S51,"stage":"S49_GENERATION_CONSUMPTION","source":source,"s49_result":s49,
   "s49_generation_hash":gen.get("hash",""),"relevance":relevance,"native":False}
  ep=self._append(CONSUMER_KIND,body)
  selection=dict(gen.get("generation") or {})
  return {"schema":S51,"episode_id":ep["episode_id"],"generation_hash":gen.get("hash"),
   "source_ref":source["source_ref"],"source":source,"source_refs":gen.get("source_refs",[]),
   "qualified_sources":selection.get("qualified_sources",[]),
   "reasons":selection.get("reasons",[]),"selection_status":selection.get("selection_status"),
   "selected_option":selection.get("selected_option",""),"s49_status":s49.get("status"),
   "s49_episode_id":s49.get("generation_episode_ref",""),
   "missing_option_relation":"NO_EXISTING_S49_OPTION_EXPRESSES_PAID_FINISHING_EQUIPMENT_OFFER",
   "target_proposals":[],"native":False}

 def run_experiment(self,*,permit=True,payment=2,hours=1,declare=True,receive=True)->dict:
  obj=self.recover_object()
  hyp=self.declare_hypothesis(obj) if declare else None
  offer=self.issue_offer(permit=permit,payment=payment,hours=hours,receive=receive)
  access=self._offer_access(offer) if receive else None
  rel=self.evaluate(obj,hyp or {},offer,access,hypothesis_active=bool(hyp))
  gen=self.consume_generation(obj,hyp,offer,access,rel) if rel["status"]=="RELEVANCE_WARRANTED" else None
  return {"schema":S51,"object":obj,"hypothesis":hyp,
   "offer":{"event_id":offer["world_event_id"],"material_event_id":offer["offer_event_id"],
    "world_event_id":offer["world_event_id"],
    "payment":offer["offer"].get("payment_per_actor"),"hours":offer["offer"].get("task_hours"),
    "permit":offer["offer"].get("permit")},"access":access,"relevance":rel,"generation":gen,
   "actual_root_current_purpose_proved":False,"native":False}

 def verify(self):
  r=super().verify(); errors=[]; ok=True
  try:
   obj=self.recover_object()
   active=0; consumed_hashes=set()
   b_perceptions=self.product.store.perceptions(self.branch_id,"B")
   for row in self._episodes(HYPOTHESIS_KIND):
    body=dict(row.get("body") or {})
    if (
     body.get("object_event_id")!=obj["object_event_id"]
     or body.get("object_hash")!=obj["object_hash"]
     or body.get("actor_id")!=obj["actor_id"]
     or body.get("rule_id")!=RULE_ID
     or body.get("root_hash")!=self.read_root()["root_hash"]
     or body.get("branch_id")!=self.branch_id
    ):
     errors.append("S51_HYPOTHESIS_PARENT_INVALID")
    status=self._hypothesis_status(body.get("hypothesis_id",""))
    life=self._latest_body(HYPOTHESIS_LIFECYCLE_KIND,body.get("hypothesis_id","")) or {}
    if status not in {"ACTIVE","BOUND","CONSUMED","EXPIRED","WITHDRAWN"}:
     errors.append("S51_HYPOTHESIS_LIFECYCLE_INVALID:"+str(status))
    if status in {"ACTIVE","BOUND"}: active+=1
    if status=="CONSUMED":
     consumed_hashes.add(life.get("consumed_by_relevance_hash",""))
    if life and life.get("hypothesis_episode_id")!=row["episode_id"]:
     errors.append("S51_HYPOTHESIS_LIFECYCLE_PARENT_INVALID")
    baseline=body.get("b_perception_baseline")
    if not isinstance(baseline,int) or baseline<0 or baseline>len(b_perceptions):
     errors.append("S51_HYPOTHESIS_PERCEPTION_BASELINE_INVALID")
    elif len(b_perceptions)>baseline:
     next_event=b_perceptions[baseline].get("event_id")
     if status=="ACTIVE":
      errors.append("S51_HYPOTHESIS_UNBOUND_RECEIVED_EVENT")
     elif status=="BOUND" and life.get("bound_event_id")!=next_event:
      errors.append("S51_HYPOTHESIS_BOUND_EVENT_MISMATCH")
     elif status=="CONSUMED" and life.get("received_event_id")!=next_event:
      errors.append("S51_HYPOTHESIS_CONSUMED_EVENT_MISMATCH")
     elif status=="EXPIRED" and life.get("reason")=="NEXT_RECEIVED_EVENT_NOT_OFFER" and life.get("received_event_id")!=next_event:
      errors.append("S51_HYPOTHESIS_EXPIRED_EVENT_MISMATCH")
   if active>1: errors.append("S51_MULTIPLE_ACTIVE_HYPOTHESES")
   relevance_hashes={
    (row.get("body") or {}).get("result",{}).get("relevance_hash")
    for row in self._episodes(RELEVANCE_KIND)
    if (row.get("body") or {}).get("stage")=="OBJECT_RELEVANCE"
   }
   for value in consumed_hashes:
    if value not in relevance_hashes: errors.append("S51_HYPOTHESIS_CONSUMPTION_UNLINKED")
   for row in self._episodes(OFFER_KIND):
    body=dict(row.get("body") or {})
    accepted,reason,_=verify_material_source(body.get("offer") or {})
    if not accepted: errors.append("S51_OFFER_SOURCE_INVALID:"+str(reason))
    event=self.event(body.get("world_event_id",""))
    if not event or event.get("hash")!=body.get("world_event_hash"):
     errors.append("S51_OFFER_EVENT_INVALID")
    else:
     if event.get("event_id") not in {x.get("event_id") for x in self.world().events}:
      errors.append("S51_OFFER_WORLD_JOURNAL_MISSING")
     if event.get("actor_id")!=OFFER_ACTOR or event.get("location")!="workshop":
      errors.append("S51_OFFER_WORLD_OWNER_INVALID")
     try:
      validate_owner_receipt(event.get("owner_receipt"),actor_id=OFFER_ACTOR,act=event.get("kind"),clock=event.get("clock"))
     except Exception:
      errors.append("S51_OFFER_WORLD_RECEIPT_INVALID")
   for row in self._episodes(ACCESS_KIND):
    body=dict(row.get("body") or {}); witness=body.get("access") or {}
    rows=[p for p in self.product.store.perceptions(self.branch_id,"B") if p.get("event_id")==body.get("event_ref")]
    content=witness.get("content") or {}
    if (
     witness.get("access_status")!="ACCESSIBLE"
     or not rows
     or witness.get("event_ref")!=body.get("event_ref")
     or content.get("received_offer_event_id")!=body.get("event_ref")
     or content.get("material_event_id")!=body.get("offer_event_id")
    ):
     errors.append("S51_ACCESS_NOT_WITNESSED")
   for row in self._episodes(RELEVANCE_KIND):
    body=dict(row.get("body") or {}); result=body.get("result") or {}
    if body.get("stage")!="OBJECT_RELEVANCE" or body.get("rule_id")!=RULE_ID:
     errors.append("S51_RELEVANCE_EPISODE_INVALID")
     continue
    try:
     self._canonical_relevance({"episode_id":row["episode_id"],"relevance_hash":result.get("relevance_hash")})
    except S51Refusal as exc:
     errors.append("S51_RELEVANCE_INVALID:"+exc.code)
   for row in self._episodes(CONSUMER_KIND):
    body=dict(row.get("body") or {}); source=body.get("source") or {}
    turns=[x for x in self._episodes("S49_B_ACTOR_TURN")
     if (x.get("body") or {}).get("generation",{}).get("hash")==body.get("s49_generation_hash")]
    if not turns or source.get("source_ref") not in (
     turns[-1].get("body",{}).get("generation",{}).get("source_refs",[])
    ):
     errors.append("S51_S49_CONSUMER_DEPENDENCY_INVALID")
  except Exception as exc:
   errors.append("S51_VERIFY_EXCEPTION:"+str(exc))
  if errors: ok=False
  r["ok"]=bool(r.get("ok")) and ok
  r["s51"]={"object_recovered":not any(x.startswith("S51_VERIFY_EXCEPTION") for x in errors),
   "actual_root_current_purpose_proved":False,"errors":errors,"native":False}
  return r


__all__=["S51","S51Session","S51Refusal","ACTUAL_HOLD","GRADE","RULE_ID"]
