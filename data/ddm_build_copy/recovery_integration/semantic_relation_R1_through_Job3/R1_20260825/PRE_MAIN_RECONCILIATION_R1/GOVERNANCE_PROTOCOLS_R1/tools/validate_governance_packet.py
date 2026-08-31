#!/usr/bin/env python3
"""Rawlsing Governance Packet R2 fail-closed validator."""
from governance_r2_support import *
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("packet"); a=ap.parse_args()
 try: p=json.loads(Path(a.packet).read_text(encoding="utf-8"))
 except Exception as ex:
  print(json.dumps({"PACKET_VALID":False,"ADOPTION_ELIGIBLE":False,"PROJECT_CLOSURE_ELIGIBLE":False,"error":f"packet-load:{ex}"},sort_keys=True)); return 1
 g=p.get("grounding_receipt",{}); w=p.get("work_return",{}); u=p.get("central_state_update",{})
 mode=g.get("agent_mode"); effect=p.get("requested_effect"); domain=p.get("decision_domain")
 C={}; D={"schema_engine":SCHEMA_ENGINE}
 for key,obj,file in [("SCHEMA_GROUNDING_RECEIPT",g,"GROUNDING_RECEIPT_SCHEMA.json"),("SCHEMA_WORK_RETURN",w,"WORK_RETURN_SCHEMA.json"),("SCHEMA_CENTRAL_STATE_UPDATE",u,"CENTRAL_STATE_UPDATE_SCHEMA.json"),("SCHEMA_PACKET_R2",p,"GOVERNANCE_PACKET_SCHEMA_R2.json")]:
  C[key],D[key+"_ERRORS"]=schema_check(obj,GOV/file)
 live_ok,live_sha,source=live_canonical(); C["LIVE_CANONICAL_REF_RESOLVED"]=live_ok; D["live_canonical_sha"]=live_sha; D["live_canonical_source"]=source
 C["CANONICAL_PROJECT_HEAD_MATCH"]=bool(live_ok and g.get("canonical_project_head")==live_sha and u.get("canonical_project_head")==live_sha and w.get("canonical_launch_head")==live_sha)
 gv_ok,gv=ground_version(); C["LIVE_GROUND_VERSION_RESOLVED"]=gv_ok; D["live_ground_version"]=gv
 C["GROUND_VERSION_MATCH"]=bool(gv_ok and g.get("ground_version")==gv and u.get("ground_version")==gv)
 try:
  state_rows=tsv(CENTRAL/"PROJECT_STATE.tsv"); states={r["state_id"] for r in state_rows}
  obl_rows=tsv(CENTRAL/"OPEN_OBLIGATIONS.tsv"); obligations={r["obligation_id"]:r for r in obl_rows}
  levels={r["level"] for r in tsv(CANON/"AUTHORITY_LEVELS.tsv")}
  ar={r["gate_id"] for r in tsv(CANON/"ANTI_RESURRECTION_INDEX.tsv")}
  scopes={r["decision_domain"]:r for r in tsv(GOV/"GROUNDING_SCOPE_REQUIREMENTS.tsv")}
  targets={r["target_id"]:r for r in tsv(GOV/"ANTI_RESURRECTION_ENFORCEMENT_MAP.tsv")}
  registry=True
 except Exception as ex:
  states=set(); obligations={}; levels=set(); ar=set(); scopes={}; targets={}; registry=False; D["registry_error"]=str(ex)
 C["AGENT_MODE_VALID"]=bool(mode in MODE_EFFECTS and w.get("agent_mode")==mode)
 C["REQUESTED_EFFECT_ALLOWED_FOR_MODE"]=bool(mode in MODE_EFFECTS and effect in MODE_EFFECTS[mode])
 ceiling=g.get("authority_ceiling")
 ceiling_ok=bool(registry and ceiling in levels and u.get("authority_ceiling")==ceiling)
 if mode=="GROUNDED_BOUNDED_EXECUTION": ceiling_ok &= ceiling=="WORKER_LOCAL_RESULT"
 if effect in EFFECT_AUTHORITY: ceiling_ok &= ceiling in EFFECT_AUTHORITY[effect]
 C["AUTHORITY_CEILING_VALID"]=bool(ceiling_ok)
 C["CROSS_FIELD_RECEIPT_ID_MATCH"]=bool(g.get("grounding_receipt_id") and u.get("grounding_receipt_id")==g.get("grounding_receipt_id"))
 touched_states=u.get("touched_state_ids",[]) if isinstance(u.get("touched_state_ids"),list) else []
 C["TOUCHED_STATE_IDS_VALID"]=bool(uniq(touched_states) and set(touched_states)<=states)
 relevant_states=g.get("relevant_state_ids",[]) if isinstance(g.get("relevant_state_ids"),list) else []
 relevant_obls=g.get("relevant_obligation_ids",[]) if isinstance(g.get("relevant_obligation_ids"),list) else []
 C["NONVACUOUS_RELEVANT_STATE"]=bool(set(relevant_states)<=states and uniq(relevant_states) and (mode!="GROUNDED_PROJECT_DECISION" or relevant_states))
 active={}
 for oid,r in obligations.items():
  if r.get("status") not in {"CLOSED","ABANDONED_BY_EXPLICIT_DECISION"}: active.setdefault(r.get("parent_state_id",""),set()).add(oid)
 exclusions=p.get("scope_exclusions",[]) if isinstance(p.get("scope_exclusions"),list) else []
 exids=[x.get("obligation_id") for x in exclusions if isinstance(x,dict)]
 exok=uniq([x for x in exids if x]) and all(isinstance(x,dict) and x.get("obligation_id") in obligations and bool(x.get("reason")) and x.get("preserved_open") is True for x in exclusions)
 active_rel=set().union(*(active.get(s,set()) for s in relevant_states)) if relevant_states else set()
 C["ACTIVE_OBLIGATIONS_ACCOUNTED"]=bool(exok and uniq(relevant_obls) and set(relevant_obls)<=set(obligations) and active_rel <= (set(relevant_obls)|set(exids)))
 scope=scopes.get(domain); reqs=set(split(scope.get("required_state_ids") if scope else "")); reqo=set(split(scope.get("required_obligation_ids") if scope else "")); reqb=split(scope.get("required_binding_surfaces") if scope else ""); reqm=split(scope.get("required_must_factor_surfaces") if scope else "")
 C["DOMAIN_REQUIRED_STATE_IDS"]=bool(scope and reqs<=set(relevant_states))
 C["DOMAIN_REQUIRED_OBLIGATION_IDS"]=bool(scope and reqo<=set(relevant_obls) and not(reqo&set(exids)))
 bset=set(g.get("binding_authority_surfaces_read",[])) if isinstance(g.get("binding_authority_surfaces_read"),list) else set(); mset=set(g.get("must_factor_surfaces_read",[])) if isinstance(g.get("must_factor_surfaces_read"),list) else set()
 C["DOMAIN_REQUIRED_SURFACES"]=bool(scope and set(reqb)<=bset and set(reqm)<=mset and all((PREMAIN/x).exists() for x in reqb+reqm))
 D["domain_required_states"]=sorted(reqs); D["domain_required_obligations"]=sorted(reqo); D["domain_required_surfaces"]=reqb+reqm
 bp=p.get("bounded_parent",{}) if isinstance(p.get("bounded_parent"),dict) else {}; parent_ok=mode!="GROUNDED_BOUNDED_EXECUTION"
 if mode=="GROUNDED_BOUNDED_EXECUTION":
  keys={"parent_receipt_path","parent_receipt_sha256","parent_grounding_receipt_id","governing_adjudication_ref","forbidden_reinterpretation"}
  if keys<=set(bp):
   try:
    pp=locate_path(str(bp["parent_receipt_path"])); parent=json.loads(pp.read_text(encoding="utf-8")); ps,_=schema_check(parent,GOV/"GROUNDING_RECEIPT_SCHEMA.json")
    parent_ok=all([pp.exists(),sha256(pp)==bp.get("parent_receipt_sha256"),ps,parent.get("grounding_receipt_id")==bp.get("parent_grounding_receipt_id"),parent.get("agent_mode")=="GROUNDED_PROJECT_DECISION",parent.get("canonical_project_head")==live_sha,parent.get("ground_version")==gv,parent.get("grounding_complete_for_declared_scope")=="PASS",resolve_ref(str(bp.get("governing_adjudication_ref",""))),BOUNDED_PROHIBITIONS<=set(bp.get("forbidden_reinterpretation",[])),set(relevant_states)<=set(parent.get("relevant_state_ids",[])),set(relevant_obls)<=set(parent.get("relevant_obligation_ids",[]))])
   except Exception: parent_ok=False
 else:
  parent_ok = bp=={}
 C["BOUNDED_PARENT_VALID"]=bool(parent_ok)
 bnon=True
 if mode=="GROUNDED_BOUNDED_EXECUTION":
  bnon=all([effect=="BOUNDED_EXECUTION_RETURN",ceiling=="WORKER_LOCAL_RESULT",g.get("may_decide")==[],BOUNDED_PROHIBITIONS<=set(g.get("may_not_decide",[])),p.get("authority_effects")==[],p.get("closure_claims")==[],w.get("authority_obtained")==[]])
 C["BOUNDED_EXECUTION_NONESCALATION"]=bool(bnon)
 wt=w.get("touched_obligation_dispositions",[]) if isinstance(w.get("touched_obligation_dispositions"),list) else []; ut=u.get("obligation_dispositions",[]) if isinstance(u.get("obligation_dispositions"),list) else []; touched=u.get("touched_obligation_ids",[]) if isinstance(u.get("touched_obligation_ids"),list) else []
 wids=[x.get("obligation_id") for x in wt if isinstance(x,dict)]; uids=[x.get("obligation_id") for x in ut if isinstance(x,dict)]; wstat={x.get("obligation_id"):x.get("disposition") for x in wt if isinstance(x,dict)}; ustat={x.get("obligation_id"):x.get("status") for x in ut if isinstance(x,dict)}
 mentioned=set()
 for field in ("accomplished","not_accomplished","remaining_open"):
  for s in w.get(field,[]) if isinstance(w.get(field),list) else []:
   mentioned |= {oid for oid in obligations if oid in str(s)}
 parents={obligations[oid].get("parent_state_id") for oid in touched if oid in obligations}
 exact=all([uniq(touched),uniq([x for x in wids if x]),uniq([x for x in uids if x]),set(touched)==set(wids)==set(uids),set(touched)<=set(obligations),all(wstat.get(oid)==ustat.get(oid) and wstat.get(oid) in DISPOSITIONS for oid in touched),mentioned<=set(touched),parents<=set(touched_states)])
 C["TOUCHED_OBLIGATIONS_EXACTLY_DISPOSITIONED"]=bool(exact)
 nw=w.get("new_obligations",[]) if isinstance(w.get("new_obligations"),list) else []; nu=u.get("new_obligations",[]) if isinstance(u.get("new_obligations"),list) else []
 C["NEW_OBLIGATIONS_REGISTERED"]=bool((not nw and not nu) or (uniq(nw) and uniq(nu) and set(nw)==set(nu) and set(nw)<=set(obligations)))
 succ=w.get("spawned_successors",[]) if isinstance(w.get("spawned_successors"),list) else []; paths=u.get("successor_return_paths",[]) if isinstance(u.get("successor_return_paths"),list) else []; spids=[x.get("successor_id") for x in paths if isinstance(x,dict)]; known=states|set(obligations)
 sok=all([uniq(succ),uniq([x for x in spids if x]),set(succ)==set(spids),all(isinstance(x,dict) and x.get("return_to") in known for x in paths)])
 if succ: sok &= set(x.get("return_to") for x in paths)<=set(w.get("return_to_ids",[]))
 C["SUCCESSOR_RETURN_PATHS_COMPLETE"]=bool(sok)
 C["REINTEGRATION_STATUS_VALID"]=bool(C["SCHEMA_WORK_RETURN"] and w.get("reintegration_status")==u.get("reintegration_status"))
 closed={oid for oid,s in wstat.items() if s=="CLOSED"}; claims=p.get("closure_claims",[]) if isinstance(p.get("closure_claims"),list) else []; claimids=[x.get("obligation_id") for x in claims if isinstance(x,dict)]; closure_claimed=bool(effect=="PROJECT_CLOSURE_AT_GRAIN" or w.get("local_status")=="PROJECT_CLOSED" or closed)
 closure=True
 if closure_claimed:
  closure=bool(mode=="GROUNDED_PROJECT_DECISION" and w.get("reintegration_status") not in CLOSURE_FORBIDDEN_REINTEGRATION and claims and uniq([x for x in claimids if x]) and set(claimids)==closed and closed)
  for cl in claims:
   oid=cl.get("obligation_id"); row=obligations.get(oid,{})
   closure &= bool(oid in obligations and cl.get("closure_authority")==row.get("competent_closure_authority") and cl.get("closure_condition_addressed") and resolve_ref(str(cl.get("supporting_evidence_ref",""))))
  closure &= not any(wstat.get(oid) in (DISPOSITIONS-{"CLOSED","ABANDONED_BY_EXPLICIT_DECISION"}) for oid in touched)
 else: closure = claims==[]
 if mode=="GROUNDED_BOUNDED_EXECUTION" and closed: closure=False
 C["PROJECT_CLOSURE_STRUCTURALLY_VALID"]=bool(closure)
 norm=True
 for oid in touched:
  cur=obligations.get(oid,{}).get("status"); prop=wstat.get(oid)
  if prop not in DISPOSITIONS: norm=False
  if mode=="GROUNDED_BOUNDED_EXECUTION" and cur in CURRENT_NONTERMINAL and prop=="CLOSED": norm=False
  if cur=="UNKNOWN_REQUIRES_SYNTHESIS" and prop=="CLOSED" and oid not in claimids: norm=False
 C["BLOCKED_UNKNOWN_NORMALIZATION_VALID"]=bool(norm)
 ack=g.get("anti_resurrection_constraints",[]) if isinstance(g.get("anti_resurrection_constraints"),list) else []
 gate=bool(uniq(ack) and set(ack)<=ar)
 if mode=="GROUNDED_PROJECT_DECISION": gate &= bool(ack)
 if effect=="GLOBAL_ADOPTION" or domain=="GLOBAL_ADOPTION": gate &= set(ack)==ar
 C["ANTI_RESURRECTION_GATE_IDS_VALID"]=bool(gate)
 ae=p.get("authority_effects",[]) if isinstance(p.get("authority_effects"),list) else []; aeok=True; encoded=set()
 for x in ae:
  target=x.get("target_id") if isinstance(x,dict) else None; row=targets.get(target or "")
  if not row: aeok=False; continue
  req=x.get("requested_effect"); encoded.add(f"{target}:{req}"); gates=set(x.get("applicable_gate_ids",[])) if isinstance(x.get("applicable_gate_ids"),list) else set(); required=set(split(row.get("gate_ids"))); forbidden=set(split(row.get("prohibited_promotion_classes")))
  aeok &= gates<=ar and required<=gates and req not in forbidden and resolve_ref(str(x.get("supporting_authority_ref","")))
 obtained=set(w.get("authority_obtained",[])) if isinstance(w.get("authority_obtained"),list) else set()
 if obtained: aeok &= obtained==encoded
 if mode=="GROUNDED_BOUNDED_EXECUTION": aeok &= not ae and not obtained
 C["AUTHORITY_EFFECTS_NONRESURRECTING"]=bool(aeok)
 rd=g.get("required_return_destination"); rids=w.get("return_to_ids",[]) if isinstance(w.get("return_to_ids"),list) else []
 C["RETURN_DESTINATION_VALID"]=bool(rd in known and u.get("return_destination")==rd and rids and set(rids)<=known and rd in rids)
 D["EXPLORATION_ALLOWED"]=bool(mode=="DELIBERATELY_UNGROUNDED_EXPLORATION" and effect=="EXPLORATORY_RETURN")
 D["DIRECT_UNGROUNDED_ADOPTION"]=False if mode=="DELIBERATELY_UNGROUNDED_EXPLORATION" else None
 domain_adopt=bool(scope and scope.get("adoption_eligible")=="YES" and domain!="CUSTOM")
 required=["SCHEMA_GROUNDING_RECEIPT","SCHEMA_WORK_RETURN","SCHEMA_CENTRAL_STATE_UPDATE","SCHEMA_PACKET_R2","LIVE_CANONICAL_REF_RESOLVED","CANONICAL_PROJECT_HEAD_MATCH","LIVE_GROUND_VERSION_RESOLVED","GROUND_VERSION_MATCH","AGENT_MODE_VALID","REQUESTED_EFFECT_ALLOWED_FOR_MODE","AUTHORITY_CEILING_VALID","CROSS_FIELD_RECEIPT_ID_MATCH","TOUCHED_STATE_IDS_VALID","NONVACUOUS_RELEVANT_STATE","ACTIVE_OBLIGATIONS_ACCOUNTED","DOMAIN_REQUIRED_STATE_IDS","DOMAIN_REQUIRED_OBLIGATION_IDS","DOMAIN_REQUIRED_SURFACES","BOUNDED_PARENT_VALID","BOUNDED_EXECUTION_NONESCALATION","TOUCHED_OBLIGATIONS_EXACTLY_DISPOSITIONED","NEW_OBLIGATIONS_REGISTERED","SUCCESSOR_RETURN_PATHS_COMPLETE","REINTEGRATION_STATUS_VALID","PROJECT_CLOSURE_STRUCTURALLY_VALID","BLOCKED_UNKNOWN_NORMALIZATION_VALID","ANTI_RESURRECTION_GATE_IDS_VALID","AUTHORITY_EFFECTS_NONRESURRECTING","RETURN_DESTINATION_VALID"]
 packet_valid=bool(registry and all(C.get(k,False) for k in required))
 adoption=bool(packet_valid and mode=="GROUNDED_PROJECT_DECISION" and effect in ADOPTIVE_EFFECTS and domain_adopt and w.get("reintegration_status") not in CLOSURE_FORBIDDEN_REINTEGRATION)
 closure_eligible=bool(packet_valid and adoption and effect=="PROJECT_CLOSURE_AT_GRAIN" and closure)
 if effect in ADOPTIVE_EFFECTS and not adoption: packet_valid=False; closure_eligible=False
 out={"checks":C,"detail":D,"PACKET_VALID":packet_valid,"ADOPTION_ELIGIBLE":adoption,"PROJECT_CLOSURE_ELIGIBLE":closure_eligible}
 print(json.dumps(out,sort_keys=True)); return 0 if packet_valid else 1

if __name__=="__main__": sys.exit(main())
