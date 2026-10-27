"""S52 paid-activity candidate over the accepted S51/S49 person."""
from __future__ import annotations
import json
from copy import deepcopy
from typing import Any, Mapping

from .bootstrap import install
install()

from candidate import digest  # noqa: E402
from s39.sources import make_source  # noqa: E402
from s51.session import S51Session, S51Refusal  # noqa: E402
from r30a.first_session import SessionRefusal  # noqa: E402

S52="SOROK_S52_PAID_ACTIVITY_REPERTOIRE@1"
CANDIDATE_KIND="S52_PAID_CANDIDATE"
PAID_OPTION="PAID_PARTICIPATION"
PAID_ACTION="PARTICIPATE_IN_PAID_TASK"
PAID_PERFORMER="s52.paid_activity"
RULE_ID="S52_PAID_OBJECT_RELEVANCE_TO_OPTION@1"
GRADE="TEST_ONLY_S52_PAID_ACTIVITY_REPERTOIRE_NOT_NATIVE"
SOURCE_GRADE="TEST_ONLY_S52_PAID_ACTIVITY_PORT_NOT_NATIVE"


def candidate_digest(candidate: Mapping[str, Any]) -> str:
 body={key:value for key,value in candidate.items() if key not in {"candidate_hash","episode_id"}}
 if isinstance(body.get("repertoire"), Mapping):
  body["repertoire"]={key:value for key,value in body["repertoire"].items()
   if key!="candidate_hash"}
 return digest(body)


class S52ColdOpenRefusal(S51Refusal):
 """A cold S52 session whose own semantic/history verification failed."""


class S52Session(S51Session):
 @classmethod
 def open(cls,state_root,**kwargs):
  try:
   session=super().open(state_root,**kwargs)
  except SessionRefusal as exc:
   if getattr(exc,"code","")=="S37_VERIFY_FAILED":
    raise S52ColdOpenRefusal("S52_COLD_OPEN_INVALID",str(exc)) from exc
   raise
  try:
   verification=session.verify()
   if not verification.get("ok"):
    raise S52ColdOpenRefusal(
     "S52_COLD_OPEN_INVALID",
     json.dumps(verification,sort_keys=True),
    )
   return session
  except Exception:
   session.close()
   raise

 def _checkpoint_readset(self,checkpoint_hash):
  checkpoint=next((c for c in self.product.store.checkpoints(self.branch_id)
   if c.get("hash")==checkpoint_hash),None)
  if not checkpoint:
   raise S51Refusal("S52_CANDIDATE_READSET_MISSING")
  state=checkpoint.get("state") or {}
  actor=dict((((state.get("actors") or {}).get("B") or {}).get("state") or {}))
  world=state.get("world") or {}
  actor["actor_id"]=actor.get("actor_id") or (self.world().actor_state.get("B") or {}).get("actor_id")
  return {"actor":actor,"position":(world.get("positions") or {}).get("B"),
   "checkpoint_hash":checkpoint_hash,"clock":checkpoint.get("clock")}

 def _relevance_source(self,obj,hypothesis,offer,access,relevance):
  actor=(self.world().actor_state.get("B") or {}).get("actor_id")
  return make_source(
   source_ref="S51_SOURCE_"+str(obj["object_event_id"]).split(":")[-1][:16],
   source_class="HISTORICAL_EPISODE",actor_id=actor,branch_id=self.branch_id,
   as_of=self.clock(),predicate="S51_OBJECT_RELEVANCE",value=1,
   content={"object_event_id":obj["object_event_id"],
    "offer_event_id":offer["offer_event_id"],
    "world_offer_event_id":offer["world_event_id"],
    "relation":relevance["relation"],"hypothesis_id":hypothesis["hypothesis_id"],
    "relevance_hash":relevance["relevance_hash"],
    "access_ref":access.get("source_ref")})

 def resolve_candidate(self,candidate:Mapping[str,Any])->dict:
  if not isinstance(candidate,Mapping) or not candidate.get("candidate_hash"):
   raise S51Refusal("S52_CANONICAL_CANDIDATE_MISSING")
  rows=[row for row in self._episodes(CANDIDATE_KIND)
   if (row.get("body") or {}).get("candidate_hash")==candidate.get("candidate_hash")]
  if len(rows)!=1:
   raise S51Refusal("S52_CANONICAL_CANDIDATE_MISSING")
  stored=dict(rows[0].get("body") or {})
  if stored.get("candidate_hash")!=candidate_digest(stored):
   raise S51Refusal("S52_CANDIDATE_HASH_INVALID")
  relevance_rows=[row for row in self._episodes("S51_OBJECT_RELEVANCE")
   if ((row.get("body") or {}).get("result") or {}).get("relevance_hash")==stored.get("relevance_hash")]
  if len(relevance_rows)!=1:
   raise S51Refusal("S52_CANDIDATE_RELEVANCE_MISSING")
  rel_body=dict(relevance_rows[0].get("body") or {})
  relevance=self._canonical_relevance({"episode_id":relevance_rows[0]["episode_id"],
   "relevance_hash":(rel_body.get("result") or {}).get("relevance_hash")})
  obj=self._canonical_object(rel_body.get("object") or {})
  hyp=self._canonical_hypothesis(rel_body.get("hypothesis") or {},
   allow_consumed=True,allow_inactive=True)
  offer=self._canonical_offer(rel_body.get("offer") or {})
  access=self._canonical_access(rel_body.get("access"),offer) if rel_body.get("access") is not None else None
  checkpoint_hash=rel_body.get("evaluation_checkpoint_hash")
  readset=self._checkpoint_readset(checkpoint_hash)
  expected=self.compile_candidate(obj,hyp,offer,access,relevance,
   readset=readset,checkpoint_hash=checkpoint_hash)
  if expected.get("candidate_hash")!=stored.get("candidate_hash"):
   raise S51Refusal("S52_CANDIDATE_STALE_OR_FOREIGN")
  if stored.get("actor_id")!=expected.get("actor_id") or stored.get("root_hash")!=expected.get("root_hash") or stored.get("branch_id")!=expected.get("branch_id"):
   raise S51Refusal("S52_CANDIDATE_IDENTITY_MISMATCH")
  if stored.get("source_ref")!=expected.get("source_ref") or stored.get("source_hash")!=expected.get("source_hash"):
   raise S51Refusal("S52_CANDIDATE_SOURCE_MISMATCH")
  return expected

 def resolve_repertoire(self,repertoire:Mapping[str,Any])->dict:
  if not isinstance(repertoire,Mapping):
   raise S51Refusal("S52_CANONICAL_REPERTOIRE_REQUIRED")
  candidate=self.resolve_candidate({"candidate_hash":repertoire.get("candidate_hash")})
  canonical=candidate.get("repertoire")
  if not isinstance(canonical,Mapping):
   raise S51Refusal("S52_CANONICAL_REPERTOIRE_MISSING")
  return dict(canonical)

 def resolve_generation(self,generation:Mapping[str,Any],candidate:Mapping[str,Any])->dict:
  if not isinstance(generation,Mapping):
   raise S51Refusal("S52_CANONICAL_GENERATION_MISSING")
  target=generation.get("generation_hash")
  turns=[row for row in self._episodes("S49_B_ACTOR_TURN")
   if ((row.get("body") or {}).get("generation") or {}).get("hash")==target]
  if not turns:
   raise S51Refusal("S52_CANONICAL_GENERATION_MISSING")
  body=dict(turns[-1]["body"].get("generation") or {})
  receipt=body.get("generation") or {}
  rep=receipt.get("repertoire") or {}
  if (
   rep.get("candidate_hash")!=candidate.get("candidate_hash")
   or (rep.get("option") or {}).get("option_id")!=PAID_OPTION
  ):
   raise S51Refusal("S52_GENERATION_CANDIDATE_MISMATCH")
  return body

 def produce_b_turn(self,*,controlled=False,source_records_override=None,repertoire=None):
  if repertoire is not None:
   repertoire=self.resolve_repertoire(repertoire)
  return super().produce_b_turn(controlled=controlled,
   source_records_override=source_records_override,repertoire=repertoire)

 def compile_candidate(self,obj,hypothesis,offer,access,relevance,*,
                       readset=None,checkpoint_hash="")->dict:
  obj=self._canonical_object(obj)
  hypothesis=self._canonical_hypothesis(hypothesis,allow_consumed=True,allow_inactive=True)
  offer=self._canonical_offer(offer)
  access=self._canonical_access(access,offer)
  relevance=self._canonical_relevance(relevance)
  source=self._relevance_source(obj,hypothesis,offer,access,relevance)
  p=offer.get("offer") or {}
  if readset is not None:
   actor=dict(readset.get("actor") or {}); place=readset.get("position")
   checkpoint_hash=readset.get("checkpoint_hash",checkpoint_hash)
  else:
   world=self.world(); actor=world.actor_state.get("B") or {}
   place=world.positions.get("B")
   checkpoint_hash=checkpoint_hash or self.product.store.checkpoints(self.branch_id)[-1].get("hash","")
  free=actor.get("free_hours"); material=actor.get("material_remaining")
  completed=actor.get("completed_units")
  status=""; reason=""
  if p.get("permit") is not True:
   status="BLOCKED"; reason="S52_OFFER_PERMIT_FALSE"
  elif place!="workshop" or p.get("place")!="INST_WORKSHOP_A":
   status="BLOCKED"; reason="S52_ACTOR_OR_OFFER_PLACE_UNAVAILABLE"
  elif not isinstance(free,int) or not isinstance(material,int) or not isinstance(completed,int):
   status="UNKNOWN"; reason="S52_CURRENT_CAPABILITY_OR_TIME_UNKNOWN"
  elif free<int(p.get("task_hours",0)):
   status="BLOCKED"; reason="S52_INSUFFICIENT_FREE_HOURS"
  elif material<int(p.get("material_units",0)):
   status="BLOCKED"; reason="S52_INSUFFICIENT_MATERIAL"
  elif completed<1:
   status="UNKNOWN"; reason="S52_PAID_CAPABILITY_HISTORY_NOT_OBSERVED"
  elif relevance.get("status")!="RELEVANCE_WARRANTED" or relevance.get("relation")!="FACILITATES":
   status="NOT_RECRUITED"; reason="S52_NON_FACILITATING_OR_ABSENT_RELEVANCE"
  else:
   status="CONDITIONAL_ON_INDEPENDENT_PARTICIPATION"
   reason="S52_INDEPENDENT_COUNTERPART_NOT_OBSERVED"
  recruited=relevance.get("status")=="RELEVANCE_WARRANTED" and relevance.get("relation")=="FACILITATES" and status in {"CONDITIONAL_ON_INDEPENDENT_PARTICIPATION","FEASIBLE"}
  option={"option_id":PAID_OPTION,"s36_response_kind":"PAID_PARTICIPATION",
   "action":PAID_ACTION,"performer":PAID_PERFORMER}
  reason_row=None
  if recruited:
   reason_row={"option_id":PAID_OPTION,"relation":"CONDITIONAL_SUPPORTS",
    "predicate":"S52_PAID_OBJECT_RELEVANCE","source_ref":source["source_ref"],
    "source_hash":source["source_hash"],"source_class":source["source_class"],
    "content":{"object_event_id":obj["object_event_id"],
     "offer_event_id":offer["offer_event_id"],"world_offer_event_id":offer["world_event_id"],
     "relation":relevance["relation"],"relevance_hash":relevance["relevance_hash"],
     "candidate_status":status}}
  repertoire=None
  if relevance.get("relation")=="FACILITATES" and status not in {"NOT_RECRUITED"}:
   repertoire={"schema":"S52_PAID_REPERTOIRE@1","eligible":recruited,
    "option":dict(option),"reason":reason_row,"candidate_hash":""}
  candidate={
   "schema":S52,"stage":"PAID_ACTIVITY_CANDIDATE","candidate_version":"R1",
   "actor_id":actor.get("actor_id"),"root_hash":self.read_root()["root_hash"],
   "root_id":self.read_root()["root_id"],"branch_id":self.branch_id,
   "object_event_id":obj["object_event_id"],"hypothesis_id":hypothesis["hypothesis_id"],
   "hypothesis_episode_id":hypothesis.get("episode_id",""),
   "relevance_episode_id":relevance.get("episode_id",""),
   "offer_event_id":offer["offer_event_id"],"world_offer_event_id":offer["world_event_id"],
   "offer":offer,"access_ref":access.get("source_ref"),
   "access":access,"relevance_hash":relevance["relevance_hash"],
   "relation":relevance["relation"],"status":status,"reason":reason,
   "objective_feasibility":status,"recruited":recruited,
   "option":option,"counterpart_required":True,
   "counterpart_status":"INDEPENDENT_PARTICIPATION_NOT_OBSERVED",
   "participant_role":"ACTOR_B","counterpart_role":"ACTOR_A_INDEPENDENT",
   "task_parameters":{k:p.get(k) for k in ("payment_per_actor","task_hours",
    "material_units","permit","place","owner_id","effective_index")},
   "prospective_payment":p.get("payment_per_actor") if recruited else 0,
   "earned_payment":0,"performed":False,
   "capability_readset":{"completed_units":completed,"free_hours":free,
    "material_remaining":material,"skill":actor.get("skill"),
    "practices":list(actor.get("practices") or []),
    "material_position":actor.get("material_position"),"position":place,
    "grade":"CURRENT_ACTOR_STATE_ONLY_NOT_PAID_HISTORY"},
   "capability_checkpoint_hash":checkpoint_hash,
   "source_ref":source["source_ref"],"source_hash":source["source_hash"],
   "source_class":source["source_class"],"source":source,
   "rule_id":RULE_ID,"grade":GRADE,"source_grade":SOURCE_GRADE,
   "native":False,"psychology_claim":False,"actual_current_purpose_proved":False}
  if repertoire is not None:
   candidate["repertoire"]=repertoire
  candidate["candidate_hash"]=candidate_digest(candidate)
  if repertoire is not None:
   repertoire["candidate_hash"]=candidate["candidate_hash"]
  return candidate

 def consume_generation(self,obj,hypothesis,offer,access,relevance,*,repertoire=None):
  candidate=self.compile_candidate(obj,hypothesis,offer,access,relevance)
  ep=self._append(CANDIDATE_KIND,candidate)
  candidate["episode_id"]=ep["episode_id"]
  rep=candidate.get("repertoire")
  result=super().consume_generation(obj,hypothesis,offer,access,relevance,repertoire=rep)
  turns=[row for row in self._episodes("S49_B_ACTOR_TURN")
   if (row.get("body") or {}).get("generation")]
  if turns:
   result["generation_body"]=dict(turns[-1]["body"]["generation"])
   result["generation_receipt"]=dict(turns[-1]["body"]["generation"].get("generation") or {})
  result["candidate"]=candidate
  result["repertoire"]=rep
  return result

 def run_experiment(self,**kwargs):
  result=super().run_experiment(**kwargs)
  generation=result.get("generation") or {}
  if generation.get("candidate") is not None:
   result["candidate"]=generation["candidate"]
  return result

 def perform_paid_participation(self,candidate,*,generation=None,
                                counterpart_performed=False):
  from .performer import perform_paid_participation
  return perform_paid_participation(self,candidate,generation=generation,
   counterpart_performed=counterpart_performed)

 def verify(self):
  r=super().verify()
  base_ok=bool(r.get("ok"))
  errors=list(r.get("s51",{}).get("errors",[]))
  candidates=[dict(row.get("body") or {}) for row in self._episodes(CANDIDATE_KIND)]
  by_hash={row.get("candidate_hash"):row for row in candidates}
  b_actor=(self.world().actor_state.get("B") or {}).get("actor_id")
  for body in candidates:
   if body.get("candidate_hash")!=candidate_digest(body):
    errors.append("S52_CANDIDATE_HASH_INVALID")
   if body.get("source_ref") and body.get("source",{}).get("source_ref")!=body.get("source_ref"):
    errors.append("S52_CANDIDATE_SOURCE_MISMATCH")
   if (
    body.get("actor_id")!=b_actor
    or body.get("root_hash")!=self.read_root().get("root_hash")
    or body.get("branch_id")!=self.branch_id
   ):
    errors.append("S52_CANDIDATE_IDENTITY_INVALID")
   try:
    expected=self.resolve_candidate({"candidate_hash":body.get("candidate_hash")})
   except S51Refusal as exc:
    errors.append("S52_CANDIDATE_SEMANTIC_INVALID:"+exc.code)
   else:
    if expected.get("candidate_hash")!=body.get("candidate_hash"):
     errors.append("S52_CANDIDATE_SEMANTIC_MISMATCH")
  action_hashes=[]; last_performed=None; last_action_episode_id=""
  for row in self._episodes("S52_PAID_ACTIVITY_RESULT"):
   body=dict(row.get("body") or {})
   if body.get("performed") is not True: continue
   action_hashes.append(body.get("candidate_hash")); last_performed=body
   last_action_episode_id=row.get("episode_id","")
   candidate=by_hash.get(body.get("candidate_hash"))
   if candidate is None:
    errors.append("S52_ACTION_CANDIDATE_MISSING"); continue
   params=candidate.get("task_parameters") or {}
   before=body.get("before") or {}; after=body.get("after") or {}
   if (
    after.get("cash") != int(before.get("cash",0))+int(params.get("payment_per_actor",0))
    or after.get("free_hours") != int(before.get("free_hours",0))-int(params.get("task_hours",0))
    or after.get("completed_units") != int(before.get("completed_units",0))+int(params.get("material_units",0))
   ):
    errors.append("S52_ACTION_EFFECT_MISMATCH")
   if not self.event(body.get("world_event_id","")):
    errors.append("S52_ACTION_WORLD_EVENT_MISSING")
  if any(action_hashes.count(value)>1 for value in action_hashes):
   errors.append("S52_DUPLICATE_PERFORMED_ACTION")
  if last_performed is not None:
   all_episodes=self.product.store.episodes(self.branch_id)
   last_index=max((i for i,row in enumerate(all_episodes)
    if row.get("episode_id")==last_action_episode_id),default=-1)
   # If a later canonical episode exists, a lawful transition may have moved
   # the current state; do not freeze B to the last paid postcondition. The
   # action's own effect and event are still validated above.
   if last_index==len(all_episodes)-1:
    current=self.world().actor_state.get("B") or {}
    after=last_performed.get("after") or {}
    for key in ("cash","free_hours","completed_units"):
     if current.get(key)!=after.get(key):
      errors.append("S52_CURRENT_STATE_DIVERGES:"+key)
  r["s52"]={"candidate_count":len(candidates),
   "performed_action_count":len(action_hashes),"errors":errors,"native":False}
  r["ok"]=base_ok and not errors
  return r
