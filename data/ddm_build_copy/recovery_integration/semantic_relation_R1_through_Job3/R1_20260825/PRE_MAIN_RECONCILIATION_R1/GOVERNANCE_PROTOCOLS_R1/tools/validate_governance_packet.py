#!/usr/bin/env python3
"""Rawlsing Governance Packet R2.1 fail-closed validator."""
from governance_r2_support import *

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("packet"); a=ap.parse_args()
 try: p=json.loads(Path(a.packet).read_text(encoding="utf-8"))
 except Exception as ex:
  print(json.dumps({"PACKET_VALID":False,"ADOPTION_ELIGIBLE":False,"PROJECT_CLOSURE_ELIGIBLE":False,"error":f"packet-load:{ex}"},sort_keys=True)); return 1
 g=p.get("grounding_receipt",{}); w=p.get("work_return",{}); u=p.get("central_state_update",{})
 mode=g.get("agent_mode"); effect=p.get("requested_effect"); domain=p.get("decision_domain"); C={}; D={"schema_engine":SCHEMA_ENGINE}
 for key,obj,file in [("SCHEMA_GROUNDING_RECEIPT",g,"GROUNDING_RECEIPT_SCHEMA.json"),("SCHEMA_WORK_RETURN",w,"WORK_RETURN_SCHEMA.json"),("SCHEMA_CENTRAL_STATE_UPDATE",u,"CENTRAL_STATE_UPDATE_SCHEMA.json"),("SCHEMA_PACKET_R2",p,"GOVERNANCE_PACKET_SCHEMA_R2.json")]:
  C[key],D[key+"_ERRORS"]=schema_check(obj,GOV/file)
 live_ok,live_sha,source=live_canonical(); C["LIVE_CANONICAL_REF_RESOLVED"]=live_ok; D["live_canonical_sha"]=live_sha; D["live_canonical_source"]=source
 C["CANONICAL_PROJECT_HEAD_MATCH"]=bool(live_ok and g.get("canonical_project_head")==live_sha and u.get("canonical_project_head")==live_sha and w.get("canonical_launch_head")==live_sha)
 gv_ok,gv=ground_version(); C["LIVE_GROUND_VERSION_RESOLVED"]=gv_ok; D["live_ground_version"]=gv; C["GROUND_VERSION_MATCH"]=bool(gv_ok and g.get("ground_version")==gv and u.get("ground_version")==gv)
 try:
  state_rows=tsv(CENTRAL/"PROJECT_STATE.tsv"); states={r["state_id"] for r in state_rows}
  obl_rows=tsv(CENTRAL/"OPEN_OBLIGATIONS.tsv"); obligations={r["obligation_id"]:r for r in obl_rows}
  levels={r["level"] for r in tsv(CANON/"AUTHORITY_LEVELS.tsv")}; ar={r["gate_id"] for r in tsv(CANON/"ANTI_RESURRECTION_INDEX.tsv")}
  scopes={r["decision_domain"]:r for r in tsv(GOV/"GROUNDING_SCOPE_REQUIREMENTS.tsv")}; targets={r["target_id"]:r for r in tsv(GOV/"ANTI_RESURRECTION_ENFORCEMENT_MAP.tsv")}; registry=True
 except Exception as ex:
  states=set(); obligations={}; levels=set(); ar=set(); scopes={}; targets={}; registry=False; D["registry_error"]=str(ex)
 C["AGENT_MODE_VALID"]=bool(mode in MODE_EFFECTS and w.get("agent_mode")==mode)
 C["REQUESTED_EFFECT_ALLOWED_FOR_MODE"]=bool(mode in MODE_EFFECTS and effect in MODE_EFFECTS[mode])
 ceiling=g.get("authority_ceiling"); ceiling_ok=bool(registry and ceiling in levels and u.get("authority_ceiling")==ceiling)
 if mode=="GROUNDED_BOUNDED_EXECUTION": ceiling_ok &= ceiling=="WORKER_LOCAL_RESULT"
 if effect in EFFECT_AUTHORITY: ceiling_ok &= ceiling in EFFECT_AUTHORITY[effect]
 C["AUTHORITY_CEILING_VALID"]=bool(ceiling_ok)
 C["CROSS_FIELD_RECEIPT_ID_MATCH"]=bool(g.get("grounding_receipt_id") and u.get("grounding_receipt_id")==g.get("grounding_receipt_id"))
 scope=scopes.get(domain); allowed_effects=set(split(scope.get("allowed_requested_effects") if scope else ""))
 C["DECISION_DOMAIN_REGISTERED"]=bool(scope); C["DECISION_DOMAIN_EFFECT_BOUND"]=bool(scope and effect in allowed_effects)
 relevant_states=g.get("relevant_state_ids",[]) if isinstance(g.get("relevant_state_ids"),list) else []; relevant_obls=g.get("relevant_obligation_ids",[]) if isinstance(g.get("relevant_obligation_ids"),list) else []
 C["NONVACUOUS_RELEVANT_STATE"]=bool(set(relevant_states)<=states and uniq(relevant_states) and relevant_states)
 req_ok,req_detail=domain_requirements(scope,g); D["domain_requirements"]=req_detail; C["DOMAIN_REQUIRED_GROUNDING"]=bool(req_ok)
 touched_states=u.get("touched_state_ids",[]) if isinstance(u.get("touched_state_ids"),list) else []; touched=u.get("touched_obligation_ids",[]) if isinstance(u.get("touched_obligation_ids"),list) else []
 C["TOUCHED_STATE_IDS_VALID"]=bool(uniq(touched_states) and set(touched_states)<=states)
 allowed_states=set(split(scope.get("allowed_state_ids") if scope else "")); allowed_obls=set(split(scope.get("allowed_obligation_ids") if scope else ""))
 C["DECISION_DOMAIN_SUBJECT_BOUND"]=bool(scope and ("*" in allowed_states or set(touched_states)<=allowed_states) and ("*" in allowed_obls or set(touched)<=allowed_obls))
 acct,exids=active_accounting(g,p.get("scope_exclusions",[]) if isinstance(p.get("scope_exclusions"),list) else [],obligations)
 C["ACTIVE_OBLIGATIONS_ACCOUNTED"]=acct; reqo=set(req_detail.get("required_obligations",[])); C["DOMAIN_REQUIRED_OBLIGATIONS_NOT_EXCLUDED"]=bool(not(reqo&exids))
 bp=p.get("bounded_parent",{}) if isinstance(p.get("bounded_parent"),dict) else {}; parent_ok=mode!="GROUNDED_BOUNDED_EXECUTION"; parent_reason=""
 if mode=="GROUNDED_BOUNDED_EXECUTION":
  keys={"parent_packet_ref","parent_packet_sha256","parent_grounding_receipt_id","governing_adjudication_ref","forbidden_reinterpretation"}
  if keys<=set(bp):
   try:
    raw=immutable_bytes(str(bp["parent_packet_ref"])); parent=immutable_json(str(bp["parent_packet_ref"])); pg=(parent or {}).get("grounding_receipt",{})
    parent_ok=all([raw is not None,raw is not None and sha256_bytes(raw)==bp.get("parent_packet_sha256"),(parent or {}).get("decision_domain")==domain,parent_packet_grounding_ok(parent,scopes,states,obligations,levels,ar,live_sha,gv),pg.get("grounding_receipt_id")==bp.get("parent_grounding_receipt_id"),immutable_ref(str(bp.get("governing_adjudication_ref",""))),BOUNDED_PROHIBITIONS<=set(bp.get("forbidden_reinterpretation",[])),set(relevant_states)<=set(pg.get("relevant_state_ids",[])),set(relevant_obls)<=set(pg.get("relevant_obligation_ids",[]))])
   except Exception as ex: parent_ok=False; parent_reason=str(ex)
 else: parent_ok=bp=={}
 C["BOUNDED_PARENT_VALID"]=bool(parent_ok); D["bounded_parent_error"]=parent_reason
 bnon=True
 if mode=="GROUNDED_BOUNDED_EXECUTION": bnon=all([effect=="BOUNDED_EXECUTION_RETURN",ceiling=="WORKER_LOCAL_RESULT",g.get("may_decide")==[],BOUNDED_PROHIBITIONS<=set(g.get("may_not_decide",[])),p.get("authority_effects")==[],p.get("closure_claims")==[],w.get("authority_obtained")==[]])
 C["BOUNDED_EXECUTION_NONESCALATION"]=bool(bnon)
 wt=w.get("touched_obligation_dispositions",[]) if isinstance(w.get("touched_obligation_dispositions"),list) else []; ut=u.get("obligation_dispositions",[]) if isinstance(u.get("obligation_dispositions"),list) else []
 wids=[x.get("obligation_id") for x in wt if isinstance(x,dict)]; uids=[x.get("obligation_id") for x in ut if isinstance(x,dict)]
 wstat={x.get("obligation_id"):x.get("disposition") for x in wt if isinstance(x,dict)}; ustat={x.get("obligation_id"):x.get("status") for x in ut if isinstance(x,dict)}
 mentioned=exact_id_mentions(sum([w.get(f,[]) if isinstance(w.get(f),list) else [] for f in ("accomplished","not_accomplished","remaining_open")],[]),set(obligations)); parents={obligations[oid].get("parent_state_id") for oid in touched if oid in obligations}
 C["TOUCHED_OBLIGATIONS_EXACTLY_DISPOSITIONED"]=bool(uniq(touched) and uniq([x for x in wids if x]) and uniq([x for x in uids if x]) and set(touched)==set(wids)==set(uids) and set(touched)<=set(obligations) and all(wstat.get(oid)==ustat.get(oid) and wstat.get(oid) in DISPOSITIONS for oid in touched) and mentioned<=set(touched) and parents<=set(touched_states))
 nw=w.get("new_obligations",[]) if isinstance(w.get("new_obligations"),list) else []; nu=u.get("new_obligations",[]) if isinstance(u.get("new_obligations"),list) else []
 C["NEW_OBLIGATIONS_REGISTERED"]=bool((not nw and not nu) or (uniq(nw) and uniq(nu) and set(nw)==set(nu) and set(nw)<=set(obligations)))
 succ=w.get("spawned_successors",[]) if isinstance(w.get("spawned_successors"),list) else []; paths=u.get("successor_return_paths",[]) if isinstance(u.get("successor_return_paths"),list) else []; spids=[x.get("successor_id") for x in paths if isinstance(x,dict)]; known=states|set(obligations)
 sok=bool(uniq(succ) and uniq([x for x in spids if x]) and set(succ)==set(spids) and all(isinstance(x,dict) and x.get("return_to") in known and x.get("parent_obligation_id") in obligations for x in paths))
 if succ:
  parent_ids={x.get("parent_obligation_id") for x in paths}; sok &= set(x.get("return_to") for x in paths)<=set(w.get("return_to_ids",[])); sok &= parent_ids<=set(touched); sok &= all(wstat.get(oid)=="SPAWNED_SUCCESSOR_RETURN_REQUIRED" for oid in parent_ids); sok &= w.get("reintegration_status")=="SPAWNED_SUCCESSOR_RETURN_REQUIRED"
 C["SUCCESSOR_RETURN_PATHS_COMPLETE"]=bool(sok)
 C["REINTEGRATION_STATUS_VALID"]=bool(C["SCHEMA_WORK_RETURN"] and w.get("reintegration_status")==u.get("reintegration_status"))
 terminal={oid for oid,s in wstat.items() if s in TERMINAL_DISPOSITIONS}; claims=p.get("closure_claims",[]) if isinstance(p.get("closure_claims"),list) else []; claimids=[x.get("obligation_id") for x in claims if isinstance(x,dict)]; terminal_ok=True
 if terminal:
  terminal_ok=bool(mode=="GROUNDED_PROJECT_DECISION" and w.get("reintegration_status") not in CLOSURE_FORBIDDEN_REINTEGRATION and uniq([x for x in claimids if x]) and set(claimids)==terminal)
  for cl in claims:
   oid=cl.get("obligation_id"); row=obligations.get(oid,{}); ep=immutable_json(str(cl.get("supporting_evidence_ref",""))); eps,_=schema_check(ep,GOV/"CLOSURE_EVIDENCE_SCHEMA_R1.json") if ep else (False,[])
   terminal_ok &= all([oid in obligations,cl.get("terminal_status")==wstat.get(oid),cl.get("closure_authority")==row.get("competent_closure_authority"),g.get("agent_role")==row.get("competent_closure_authority"),cl.get("closure_condition_addressed")==row.get("closure_condition"),eps,ep and ep.get("obligation_id")==oid,ep and ep.get("terminal_status")==wstat.get(oid),ep and ep.get("closure_condition")==row.get("closure_condition"),ep and ep.get("closure_authority")==row.get("competent_closure_authority"),ep and ep.get("authorizing_grounding_receipt_id")==g.get("grounding_receipt_id"),ep and all(immutable_ref(str(x)) for x in ep.get("evidence_refs",[]))])
 else: terminal_ok=claims==[]
 if succ: terminal_ok &= not ({x.get("parent_obligation_id") for x in paths}&terminal)
 C["TERMINAL_DISPOSITION_EVIDENCE_BOUND"]=bool(terminal_ok)
 closure_claimed=bool(effect=="PROJECT_CLOSURE_AT_GRAIN" or w.get("local_status")=="PROJECT_CLOSED"); closure=True
 if closure_claimed: closure=bool(terminal_ok and terminal and set(touched)==terminal and w.get("reintegration_status") not in CLOSURE_FORBIDDEN_REINTEGRATION and not succ)
 C["PROJECT_CLOSURE_STRUCTURALLY_VALID"]=bool(closure)
 norm=True
 for oid in touched:
  prop=wstat.get(oid)
  if prop not in DISPOSITIONS: norm=False
  if mode=="GROUNDED_BOUNDED_EXECUTION" and prop in TERMINAL_DISPOSITIONS: norm=False
 C["BLOCKED_UNKNOWN_NORMALIZATION_VALID"]=bool(norm)
 ack=g.get("anti_resurrection_constraints",[]) if isinstance(g.get("anti_resurrection_constraints"),list) else []; gate=bool(uniq(ack) and set(ack)<=ar)
 if mode=="GROUNDED_PROJECT_DECISION": gate &= bool(ack)
 if effect=="GLOBAL_ADOPTION" or domain=="GLOBAL_ADOPTION": gate &= set(ack)==ar
 C["ANTI_RESURRECTION_GATE_IDS_VALID"]=bool(gate)
 ae=p.get("authority_effects",[]) if isinstance(p.get("authority_effects"),list) else []; aeok=True; encoded=set()
 for x in ae:
  if not isinstance(x,dict): aeok=False; continue
  target=x.get("target_id"); row=targets.get(target or "")
  if not row: aeok=False; continue
  req=x.get("requested_effect"); encoded.add(f"{target}:{req}"); gates=set(x.get("applicable_gate_ids",[])) if isinstance(x.get("applicable_gate_ids"),list) else set(); required=set(split(row.get("gate_ids"))); forbidden=set(split(row.get("prohibited_promotion_classes"))); allowed=set(split(row.get("allowed_promotion_classes")))
  aeok &= all([req in AUTHORITY_EFFECT_CLASSES,req in allowed,req not in forbidden,gates<=ar,required<=gates,immutable_ref(str(x.get("supporting_authority_ref","")))])
 obtained=set(w.get("authority_obtained",[])) if isinstance(w.get("authority_obtained"),list) else set()
 if obtained or ae: aeok &= obtained==encoded
 if mode=="GROUNDED_BOUNDED_EXECUTION": aeok &= not ae and not obtained
 C["AUTHORITY_EFFECTS_NONRESURRECTING"]=bool(aeok)
 rd=g.get("required_return_destination"); rids=w.get("return_to_ids",[]) if isinstance(w.get("return_to_ids"),list) else []
 C["RETURN_DESTINATION_VALID"]=bool(rd in known and u.get("return_destination")==rd and rids and set(rids)<=known and rd in rids)
 integrity_ok,integrity_mismatches=enforcement_integrity(live_sha) if live_ok else (False,["no-live-head"]); C["GOVERNANCE_SELF_INTEGRITY"]=bool(integrity_ok); D["governance_self_integrity_mismatches"]=integrity_mismatches
 D["EXPLORATION_ALLOWED"]=bool(mode=="DELIBERATELY_UNGROUNDED_EXPLORATION" and effect=="EXPLORATORY_RETURN"); D["DIRECT_UNGROUNDED_ADOPTION"]=False if mode=="DELIBERATELY_UNGROUNDED_EXPLORATION" else None
 required=["SCHEMA_GROUNDING_RECEIPT","SCHEMA_WORK_RETURN","SCHEMA_CENTRAL_STATE_UPDATE","SCHEMA_PACKET_R2","LIVE_CANONICAL_REF_RESOLVED","CANONICAL_PROJECT_HEAD_MATCH","LIVE_GROUND_VERSION_RESOLVED","GROUND_VERSION_MATCH","AGENT_MODE_VALID","REQUESTED_EFFECT_ALLOWED_FOR_MODE","AUTHORITY_CEILING_VALID","CROSS_FIELD_RECEIPT_ID_MATCH","DECISION_DOMAIN_REGISTERED","DECISION_DOMAIN_EFFECT_BOUND","NONVACUOUS_RELEVANT_STATE","DOMAIN_REQUIRED_GROUNDING","TOUCHED_STATE_IDS_VALID","DECISION_DOMAIN_SUBJECT_BOUND","ACTIVE_OBLIGATIONS_ACCOUNTED","DOMAIN_REQUIRED_OBLIGATIONS_NOT_EXCLUDED","BOUNDED_PARENT_VALID","BOUNDED_EXECUTION_NONESCALATION","TOUCHED_OBLIGATIONS_EXACTLY_DISPOSITIONED","NEW_OBLIGATIONS_REGISTERED","SUCCESSOR_RETURN_PATHS_COMPLETE","REINTEGRATION_STATUS_VALID","TERMINAL_DISPOSITION_EVIDENCE_BOUND","PROJECT_CLOSURE_STRUCTURALLY_VALID","BLOCKED_UNKNOWN_NORMALIZATION_VALID","ANTI_RESURRECTION_GATE_IDS_VALID","AUTHORITY_EFFECTS_NONRESURRECTING","RETURN_DESTINATION_VALID"]
 packet_valid=bool(registry and all(C.get(k,False) for k in required)); domain_adopt=bool(scope and scope.get("adoption_eligible")=="YES"); adoptive_requested=effect in ADOPTIVE_EFFECTS
 adoption_eligible=bool(packet_valid and adoptive_requested and mode=="GROUNDED_PROJECT_DECISION" and domain_adopt and C["GOVERNANCE_SELF_INTEGRITY"]); closure_eligible=bool(adoption_eligible and effect=="PROJECT_CLOSURE_AT_GRAIN" and C["PROJECT_CLOSURE_STRUCTURALLY_VALID"])
 out={"checks":C,"details":D,"PACKET_VALID":packet_valid,"ADOPTION_ELIGIBLE":adoption_eligible,"PROJECT_CLOSURE_ELIGIBLE":closure_eligible}; print(json.dumps(out,sort_keys=True))
 return 0 if (adoption_eligible if adoptive_requested else packet_valid) else 1

if __name__=="__main__": sys.exit(main())
