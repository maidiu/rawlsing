"""S51 bounded retained-object relevance experiment over actual S49 root."""
from __future__ import annotations
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

from .bootstrap import install
install()

from candidate import digest, seal  # noqa: E402
from candidate.actor_access_response import make_actor_local_access_witness  # noqa: E402
from s49.session import S49Session  # noqa: E402
from s49.actor import record_b_observation, generate_b  # noqa: E402
from s39.sources import make_source  # noqa: E402
from lab_sgi1.history import replay_history  # noqa: E402
from lab_sgi1.joint import material_joint_opportunity  # noqa: E402

S51="SOROK_S51_SITUATED_OBJECT_RELEVANCE@1"
HYPOTHESIS_KIND="S51_RETAINED_OBJECT_HYPOTHESIS"
OFFER_KIND="S51_WORLD_OFFER"
ACCESS_KIND="S51_ACTOR_ACCESS"
RELEVANCE_KIND="S51_OBJECT_RELEVANCE"
RULE_ID="S51_OBJECT_RELEVANCE_TO_S49@1"
GRADE="TEST_ONLY_S51_RETAINED_OBJECT_HYPOTHESIS_NOT_NATIVE"
ACTUAL_HOLD="S51_ACTUAL_CURRENT_PURPOSE_STILL_UNPROVED"

class S51Session(S49Session):
 def _append(self,kind,body):
  ep=self.product._append_episode(self.branch_id,"B",kind,self.clock(),dict(body))
  self.product._checkpoint(self.branch_id,self.clock(),self.world())
  return ep

 def recover_object(self)->dict:
  life=self.product.seed.life
  events=list(getattr(life,"b_events",[]) or [])
  if not events: raise ValueError("S51_B_HISTORY_MISSING")
  replay=replay_history(events)
  if not replay.get("valid"): raise ValueError("S51_B_HISTORY_INVALID:"+str(replay.get("errors")))
  rows=[e for e in events if e.get("kind")=="STRIVING" and e.get("event_id") in replay.get("admitted",{})]
  if len(rows)!=1: raise ValueError("S51_B_STRIVING_NOT_UNIQUE")
  event=rows[0]
  if (event.get("payload") or {}).get("striving")!="fund_finishing_equipment": raise ValueError("S51_OBJECT_NOT_EXPECTED")
  parents=list(event.get("causal_parent_event_ids") or [])
  if len(parents)!=2: raise ValueError("S51_OBJECT_PARENT_COUNT")
  parent_rows=[replay["admitted"].get(x) for x in parents]
  if any(x is None for x in parent_rows): raise ValueError("S51_OBJECT_PARENT_MISSING")
  work=next((x for x in parent_rows if x.get("kind")=="WORK_POSITION"),None)
  project=next((x for x in parent_rows if x.get("kind")=="PROJECT"),None)
  if not work or not project: raise ValueError("S51_OBJECT_PARENT_TYPES")
  witness=next((w for w in replay["value_witnesses"] if w["event_id"]==event["event_id"]),None)
  if not witness: raise ValueError("S51_OBJECT_WITNESS_MISSING")
  routes=[e for e in events if e.get("kind")=="ROUTE_AVAILABILITY" and e.get("event_id") in replay.get("admitted",{})]
  used=[e for e in routes if (replay["effects"].get(e["event_id"]) or {}).get("goal")==event["payload"]["striving"]]
  if not used: raise ValueError("S51_OBJECT_ROUTE_USAGE_MISSING")
  return {"schema":"S51_RECOVERED_OBJECT@1","actor_id":event.get("actors",[None])[0],
   "object_event_id":event["event_id"],"object_hash":event["event_id"],"striving":event["payload"]["striving"],
   "effective_index":event.get("effective_index"),"owner_id":event.get("owner_id"),
   "causal_parent_event_ids":parents,"work_parent_event_id":work["event_id"],"project_parent_event_id":project["event_id"],
   "replay_witness":witness,"route_usage":[{ "event_id":e["event_id"],"route":(e.get("payload") or {}).get("route"),"effect":replay["effects"][e["event_id"]]} for e in used],
   "source_grade":"SOURCEFREE_RESEARCH_INPUT","native":False,"native_purpose_proof":False}

 def declare_hypothesis(self,obj:Mapping[str,Any])->dict:
  seq=len([r for r in self.product.store.episodes(self.branch_id) if r.get("kind")==HYPOTHESIS_KIND])
  body={"schema":S51,"stage":"RETAINED_OBJECT_HYPOTHESIS","hypothesis_id":"S51_HYPOTHESIS_"+str(obj["object_event_id"]).split(":")[-1][:12]+"_"+str(seq),
   "hypothesis_version":"R1","rule_id":RULE_ID,"actor_id":obj["actor_id"],"root_hash":self.read_root()["root_hash"],
   "root_id":self.read_root()["root_id"],"branch_id":self.branch_id,"object_event_id":obj["object_event_id"],
   "object_hash":obj["object_event_id"],"object_striving":obj["striving"],"scope":"ONE_SUBSEQUENT_RECEIVED_EVENT",
   "expires_after_events":1,"status":"ACTIVE","native":False,"psychology_claim":False,"actor_testimony":False,
   "actual_current_purpose_proved":False,"grade":GRADE}
  ep=self._append(HYPOTHESIS_KIND,body);return {**body,"episode_id":ep["episode_id"]}

 def _active_hypothesis(self)->dict|None:
  rows=[r for r in self.product.store.episodes(self.branch_id) if r.get("kind")==HYPOTHESIS_KIND and (r.get("body") or {}).get("status")=="ACTIVE"]
  if not rows:return None
  b=dict(rows[-1]["body"]); b["episode_id"]=rows[-1].get("episode_id"); return b

 def issue_offer(self,*,permit=True,payment=2,hours=1)->dict:
  offered=len([r for r in self.product.store.episodes(self.branch_id) if r.get("kind")==OFFER_KIND])
  offer=material_joint_opportunity(effective_index=self.clock()+offered,permit=permit,units=1,payment_per_actor=payment,task_hours=hours)
  body={"schema":S51,"stage":"WORLD_OFFER","offer":offer,"offer_event_id":offer["event_id"],"owner_id":offer["owner_id"],"native":False,"performance_performed":False,"actor_willingness_claim":False}
  ep=self._append(OFFER_KIND,body);return {**body,"episode_id":ep["episode_id"]}

 def _actor_access(self,event_ref:str,offer:Mapping[str,Any])->dict:
  actor=(self.world().actor_state.get("B") or {}).get("actor_id")
  if not actor: raise ValueError("S51_B_ACTOR_MISSING")
  current=self.read_events()[-1]
  record_b_observation(self,current)
  a=make_actor_local_access_witness(actor_id=actor,event_ref=event_ref,access_time=self.clock(),source_ref="S51_ACCESS_"+str(offer["event_id"]).split(":")[-1][:16],access_status="ACCESSIBLE",scene="workshop",content={"received_offer_event_id":offer["event_id"]})
  ep=self._append(ACCESS_KIND,{"schema":S51,"access":a,"actor_id":actor,"event_ref":event_ref,"native":False});return {**a,"episode_id":ep["episode_id"]}

 def evaluate(self,obj,hypothesis,offer,access,*,hypothesis_active=True)->dict:
  p=offer.get("offer") or {}; actors=(self.world().actor_state.get("B") or {}); actor_id=actors.get("actor_id")
  relation="UNKNOWN"; reasons=[]
  if not hypothesis_active: relation="HYPOTHESIS_ABSENT"; return {"schema":S51,"status":"OBJECT_RELEVANCE_HOLD","relation":relation,"object_event_id":obj["object_event_id"],"offer_event_id":offer["offer_event_id"],"actor_id":actor_id,"hypothesis_active":False,"reasons":[],"native":False,"selected_action":None,"performed":False}
  if not access or access.get("access_status")!="ACCESSIBLE": relation="NOT_RECEIVED"; status="NOT_RECEIVED"
  elif p.get("permit") is not True: relation="OBSTRUCTS"; status="RELEVANCE_WARRANTED"
  elif int(p.get("payment_per_actor",0))<=0 or int(p.get("task_hours",0))>int(actors.get("free_hours",0)): relation="OBSTRUCTS"; status="RELEVANCE_WARRANTED"
  elif int(p.get("payment_per_actor",0))>0 and int(p.get("task_hours",0))<=int(actors.get("free_hours",0)): relation="FACILITATES"; status="RELEVANCE_WARRANTED"
  else: relation="NEUTRAL"; status="RELEVANCE_WARRANTED"
  result={"schema":S51,"status":status,"relation":relation,"actor_id":actor_id,"object_event_id":obj["object_event_id"],"object_striving":obj["striving"],"offer_event_id":offer["offer_event_id"],"access_ref":(access or {}).get("source_ref", ""),"hypothesis_id":hypothesis.get("hypothesis_id"),"hypothesis_active":True,"hypothesis_scope":hypothesis.get("scope"),"financial":{k:p.get(k) for k in ("payment_per_actor","task_hours","permit")},"actor_free_hours":actors.get("free_hours"),"native":False,"selected_action":None,"performed":False,"actual_current_purpose_proved":False,"reasons":reasons}
  result["relevance_hash"]=digest({**result,"episode_id":""})
  body={"schema":S51,"stage":"OBJECT_RELEVANCE","result":result,"object":obj,"offer":offer,"access":access,"hypothesis":hypothesis,"rule_id":RULE_ID,"native":False}
  ep=self._append(RELEVANCE_KIND,body);result["episode_id"]=ep["episode_id"];return result

 def consume_generation(self,obj,hypothesis,offer,access,relevance)->dict:
  actor=(self.world().actor_state.get("B") or {}).get("actor_id")
  source=make_source(source_ref="S51_SOURCE_"+str(obj["object_event_id"]).split(":")[-1][:16],source_class="HISTORICAL_EPISODE",actor_id=actor,branch_id=self.branch_id,as_of=self.clock(),predicate="S51_OBJECT_RELEVANCE",value=1,content={"object_event_id":obj["object_event_id"],"offer_event_id":offer["offer_event_id"],"relation":relevance["relation"],"hypothesis_id":hypothesis["hypothesis_id"]})
  reasons=[{"option_id":"","relation":"OBJECT_RELEVANCE_"+relevance["relation"],"predicate":"S51_OBJECT_RELEVANCE","source_ref":source["source_ref"],"source_hash":source["source_hash"],"source_class":source["source_class"],"object_event_id":obj["object_event_id"],"offer_event_id":offer["offer_event_id"],"relevance_hash":relevance["relevance_hash"]}]
  gen=generate_b(self,source_records=[source],supplemental_reasons=reasons)
  body={"schema":S51,"stage":"S49_GENERATION_CONSUMPTION","source":source,"generation":gen,"relevance":relevance,"native":False}
  ep=self._append("S51_S49_CONSUMER",body)
  return {"schema":S51,"episode_id":ep["episode_id"],"generation_hash":gen.get("hash"),"source_ref":source["source_ref"],"reasons":gen.get("generation",{}).get("reasons",[]),"selection_status":gen.get("generation",{}).get("selection_status"),"selected_option":gen.get("generation",{}).get("selected_option",""),"target_proposals":[],"native":False}

 def run_experiment(self,*,permit=True,payment=2,hours=1,declare=True,receive=True)->dict:
  obj=self.recover_object()
  hyp=self.declare_hypothesis(obj) if declare else None
  offer=self.issue_offer(permit=permit,payment=payment,hours=hours)
  event=self.read_events()[-1]
  access=self._actor_access(event["e1_event_id"],offer["offer"]) if receive else None
  rel=self.evaluate(obj,hyp or {},offer,access,hypothesis_active=bool(hyp))
  gen=self.consume_generation(obj,hyp or {},offer,access,rel) if rel["status"]=="RELEVANCE_WARRANTED" else None
  return {"schema":S51,"object":obj,"hypothesis":hyp,"offer":{"event_id":offer["offer_event_id"],"payment":offer["offer"].get("payment_per_actor"),"hours":offer["offer"].get("task_hours"),"permit":offer["offer"].get("permit")},"access":access,"relevance":rel,"generation":gen,"actual_root_current_purpose_proved":False,"native":False}

 def verify(self):
  r=super().verify(); r["s51"]={"object_recovered":True,"actual_root_current_purpose_proved":False}; return r

__all__=["S51","S51Session","ACTUAL_HOLD","GRADE","RULE_ID"]
