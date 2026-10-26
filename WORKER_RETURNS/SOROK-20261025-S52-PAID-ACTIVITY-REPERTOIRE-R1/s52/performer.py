"""Smallest current-state performer port for the bounded paid-activity contract.

This is not a G18 action receipt, not unilateral wages, and not an independent
counterpart. The normal path remains conditional until another participant's
actual contribution exists. Controlled tests may explicitly pass the
counterpart flag to exercise the arithmetic and denial paths.
"""
from __future__ import annotations
from copy import deepcopy
from typing import Any, Mapping

from .bootstrap import install
install()

from bp4.world import make_event  # noqa: E402
from candidate import digest, seal  # noqa: E402
from s51.session import S51Refusal  # noqa: E402

GRADE="TEST_ONLY_S52_PAID_ACTIVITY_PORT_NOT_NATIVE"
ACTION_KIND="S52_PAID_ACTIVITY_RESULT"


def _refuse(reason, *, candidate=None, before=None):
 return {"schema":"S52_PAID_ACTIVITY_RESULT@1","grade":GRADE,"native":False,
  "performed":False,"status":"DENIED","reason":reason,
  "candidate_hash":(candidate or {}).get("candidate_hash",""),
  "before":before,"after":before,"event_id":"","event_hash":"","controlled_counterpart":False}


def perform_paid_participation(session,candidate:Mapping[str,Any],*,
                               generation:Mapping[str,Any]|None=None,
                               counterpart_performed:bool=False)->dict:
 if not isinstance(candidate,Mapping) or not candidate.get("candidate_hash"):
  return _refuse("S52_CANDIDATE_INVALID")
 rows=[row for row in session._episodes("S52_PAID_CANDIDATE")
  if (row.get("body") or {}).get("candidate_hash")==candidate.get("candidate_hash")]
 if not rows:
  return _refuse("S52_CANDIDATE_NOT_CANONICAL",candidate=candidate)
 candidate=dict(rows[-1].get("body") or {})
 if not generation:
  return _refuse("S52_GENERATION_REQUIRED",candidate=candidate)
 receipt=(generation.get("generation") or generation or {})
 repertoire=receipt.get("repertoire") or {}
 if repertoire.get("candidate_hash")!=candidate.get("candidate_hash") or (
  repertoire.get("option") or {}
 ).get("option_id")!="PAID_PARTICIPATION":
  return _refuse("S52_GENERATION_CANDIDATE_MISMATCH",candidate=candidate)
 existing=[row for row in session._episodes(ACTION_KIND)
  if (row.get("body") or {}).get("candidate_hash")==candidate["candidate_hash"]
  and (row.get("body") or {}).get("performed") is True]
 if existing:
  return _refuse("S52_DUPLICATE_PARTICIPATION",candidate=candidate)
 world=session.world(); actor=world.actor_state.get("B") or {}
 before=deepcopy(actor)
 offer=candidate.get("offer") or {}; p=offer.get("offer") or {}
 if not counterpart_performed:
  return {**_refuse("S52_INDEPENDENT_COUNTERPART_NOT_OBSERVED",candidate=candidate,before=before),
   "status":"CONDITIONAL_ON_INDEPENDENT_PARTICIPATION"}
 if candidate.get("status") not in {"CONDITIONAL_ON_INDEPENDENT_PARTICIPATION","FEASIBLE"}:
  return _refuse("S52_CANDIDATE_NOT_FEASIBLE",candidate=candidate,before=before)
 if world.positions.get("B")!="workshop" or p.get("place")!="INST_WORKSHOP_A":
  return _refuse("S52_ACTOR_PLACE_UNAVAILABLE",candidate=candidate,before=before)
 if p.get("permission")!="RESEARCH_JOINT_WITNESS_ONLY":
  return _refuse("S52_JOINT_PERMISSION_MISMATCH",candidate=candidate,before=before)
 if p.get("permit") is not True:
  return _refuse("S52_OFFER_PERMIT_FALSE",candidate=candidate,before=before)
 for key in ("payment_per_actor","task_hours","material_units"):
  if not isinstance(p.get(key),int):
   return _refuse("S52_OFFER_PARAMETER_UNKNOWN",candidate=candidate,before=before)
 free=before.get("free_hours"); material=before.get("material_remaining")
 completed=before.get("completed_units")
 if not isinstance(free,int) or not isinstance(material,int) or not isinstance(completed,int):
  return _refuse("S52_CURRENT_ACTOR_STATE_UNKNOWN",candidate=candidate,before=before)
 if free<int(p["task_hours"]):
  return _refuse("S52_INSUFFICIENT_FREE_HOURS",candidate=candidate,before=before)
 if material<int(p["material_units"]):
  return _refuse("S52_INSUFFICIENT_MATERIAL",candidate=candidate,before=before)
 after=deepcopy(before)
 after["cash"]=int(before.get("cash",0))+int(p["payment_per_actor"])
 after["free_hours"]=free-int(p["task_hours"])
 after["completed_units"]=completed+int(p["material_units"])
 event=make_event(clock=world.clock,kind="REPAIR",actor_id="B",
  location=world.positions["B"],
  summary="The finishing worker performs the controlled paid task.",
  body={"schema":"S52_CONTROLLED_PAID_ACTIVITY_EVENT@1",
   "candidate_hash":candidate["candidate_hash"],
   "material_event_id":offer.get("offer_event_id",""),
   "controlled_counterpart":True,
   "performed":True},
  sequence=len(world.events))
 world.add_event(event)
 session._append_event(event,perceive=("A","B","U"))
 world.actor_state["B"]=after
 session.product._checkpoint(session.branch_id,world.clock,world)
 body={"schema":"S52_PAID_ACTIVITY_RESULT@1","grade":GRADE,"native":False,
  "performed":True,"status":"PERFORMED","reason":"OK",
  "candidate_hash":candidate["candidate_hash"],
  "generation_hash":generation.get("generation_hash","") or (generation.get("generation_body") or {}).get("hash",""),
  "offer_event_id":offer.get("offer_event_id",""),
  "world_event_id":event["event_id"],"event_hash":event["hash"],
  "before":before,"after":after,"controlled_counterpart":True,
  "counterpart_status":"EXPLICIT_CONTROLLED_TEST_ONLY",
  "payment_earned":int(p["payment_per_actor"]),
  "material_source":deepcopy(offer.get("offer") or {}),
  "source_grade":GRADE,"source_ref":candidate.get("source_ref",""),
  "source_hash":candidate.get("source_hash","")}
 res=session._append(ACTION_KIND,body)
 return {**body,"episode_id":res["episode_id"]}
