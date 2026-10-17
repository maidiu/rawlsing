from __future__ import annotations
import argparse, csv, hashlib, json, os, re, subprocess, sys
from pathlib import Path
from typing import Any

PREMAIN = Path(__file__).resolve().parents[2]
GOV = PREMAIN / "GOVERNANCE_PROTOCOLS_R1"
CENTRAL = PREMAIN / "CENTRAL_PROJECT_STATE_R1"
CANON = PREMAIN / "CANONICAL_GOVERNANCE_R1"
CANONICAL_REF = "integration/pre-main-reconciliation-r1"
PACKET_VERSION = "RAWLSING_GOVERNANCE_PACKET_R2"
ADOPTIVE_EFFECTS={"PROJECT_ADOPTION","CAMPAIGN_ACCEPTANCE","HQ_BANKING","GLOBAL_ADOPTION","PROJECT_CLOSURE_AT_GRAIN"}
MODE_EFFECTS={"GROUNDED_PROJECT_DECISION":ADOPTIVE_EFFECTS|{"FORENSIC_RETURN"},"GROUNDED_BOUNDED_EXECUTION":{"BOUNDED_EXECUTION_RETURN"},"FORENSIC_READ_ONLY":{"FORENSIC_RETURN"},"HOSTILE_INDEPENDENT_AUDIT":{"FORENSIC_RETURN"},"DELIBERATELY_UNGROUNDED_EXPLORATION":{"EXPLORATORY_RETURN"}}
EFFECT_AUTHORITY={"PROJECT_ADOPTION":{"HQ_BANKED_AUTHORITY","GLOBAL_SOVEREIGN_CONTROL"},"CAMPAIGN_ACCEPTANCE":{"DELEGATED_ACCEPTED_AUTHORITY","HQ_BANKED_AUTHORITY","GLOBAL_SOVEREIGN_CONTROL"},"HQ_BANKING":{"HQ_BANKED_AUTHORITY","GLOBAL_SOVEREIGN_CONTROL"},"GLOBAL_ADOPTION":{"GLOBAL_SOVEREIGN_CONTROL"},"PROJECT_CLOSURE_AT_GRAIN":{"PROJECT_CURRENT_AUTHORITY","HQ_BANKED_AUTHORITY","GLOBAL_SOVEREIGN_CONTROL"}}
DISPOSITIONS={"OPEN","PARTIALLY_CLOSED","BLOCKED_ON_DEPENDENCY","SUSPENDED_ON_DEPENDENCY","SPAWNED_SUCCESSOR_RETURN_REQUIRED","INTERRUPTED_STRANDED","RETURN_REQUIRED","UNKNOWN_REQUIRES_SYNTHESIS","SUPERSEDED_AT_GRAIN_WITH_SURVIVING_OBLIGATION","ABANDONED_BY_EXPLICIT_DECISION","CLOSED"}; TERMINAL_DISPOSITIONS={"CLOSED","ABANDONED_BY_EXPLICIT_DECISION"}; CURRENT_NONTERMINAL=DISPOSITIONS-TERMINAL_DISPOSITIONS
CLOSURE_FORBIDDEN_REINTEGRATION={"LOCAL_COMPLETE_UNRECONCILED","CAMPAIGN_ACCEPTED_UNBANKED","HQ_BANKED_NOT_CANONICALLY_INHERITED","SPAWNED_SUCCESSOR_RETURN_REQUIRED","BLOCKED_ON_DEPENDENCY","INTERRUPTED_STRANDED","UNKNOWN_REQUIRES_SYNTHESIS","EXPLORATORY_UNRECONCILED","ACTIVE_GROUNDED"}
BOUNDED_PROHIBITIONS={"NO_NEW_PROJECT_DECISIONS","NO_AUTHORITY_REINTERPRETATION","NO_OPEN_OBLIGATION_CLOSURE","NO_SUBSTITUTION","NO_FROZEN_ADJUDICATION_REINTERPRETATION"}
AUTHORITY_EFFECT_CLASSES={"PRESERVE_CURRENT_STATUS","CURRENT_SERVING_RUNTIME","SERVING_RUNTIME","CURRENT_RUNTIME","BINDING_CURRENT_ARCHITECTURE","PROJECT_CURRENT_AUTHORITY","CURRENT_SEMANTIC_AUTHORITY","ADMITTED_AUTHORITY","UNIVERSAL_LAW","CURRENT_ONTOLOGY","CURRENT_DENOMINATORS","CURRENT_ROUTING_AUTHORITY","ACCEPTED_RESULT","HQ_BANKED_AUTHORITY","NEGATIVE_TRUTH","FALSE","CLOSED"}
IMMUTABLE_REF_RE=re.compile(r"^(?P<sha>[0-9a-f]{40})(?::(?P<path>[^:\n]+))?$")
if os.environ.get("RAWLSING_SCHEMA_ENGINE")=="internal_subset": jsonschema=None; SCHEMA_ENGINE="internal_subset"
else:
 try: import jsonschema; SCHEMA_ENGINE="jsonschema"
 except Exception: jsonschema=None; SCHEMA_ENGINE="internal_subset"
def tsv(path:Path):
 with path.open(encoding="utf-8",newline="") as f:return list(csv.DictReader(f,delimiter="\t"))
def split(v):return [x for x in (v or "").split(";") if x]
def uniq(xs):return len(xs)==len(set(xs))
def run_git(*args):
 try:
  p=subprocess.run(["git","-C",str(PREMAIN),*args],text=True,capture_output=True,timeout=10);return p.returncode==0,p.stdout.strip()
 except Exception:return False,""
def repo_root():
 ok,out=run_git("rev-parse","--show-toplevel");return Path(out) if ok and out else PREMAIN
def live_canonical():
 lo,ls=run_git("rev-parse","--verify",f"refs/heads/{CANONICAL_REF}");ro,rs=run_git("rev-parse","--verify",f"refs/remotes/origin/{CANONICAL_REF}")
 if lo and ro and ls!=rs:return False,"","FAIL_CANONICAL_REF_DIVERGENCE"
 if lo:return True,ls,"LOCAL"+("+REMOTE_MATCH" if ro else "")
 if ro:return True,rs,"REMOTE_ONLY"
 return False,"","FAIL_CANONICAL_REF_UNRESOLVED"
def ground_version():
 try:text=(PREMAIN/"00_RAWLSING_GROUND.md").read_text(encoding="utf-8")
 except Exception:return False,""
 ms=re.findall(r"\*\*Ground version:\*\*\s*`([^`]+)`",text);return len(ms)==1,ms[0] if len(ms)==1 else ""
def immutable_ref(v:str):
 m=IMMUTABLE_REF_RE.fullmatch(v or "")
 if not m:return False
 target=f"{m.group('sha')}:{m.group('path')}" if m.group("path") else m.group("sha");ok,_=run_git("cat-file","-e",target);return ok
def immutable_json(v:str):
 if not immutable_ref(v) or ":" not in v:return None
 ok,out=run_git("show",v)
 if not ok:return None
 try:return json.loads(out)
 except Exception:return None
def immutable_bytes(v:str):
 if not immutable_ref(v) or ":" not in v:return None
 ok,out=run_git("show",v);return out.encode("utf-8") if ok else None
def sha256_bytes(b:bytes):return hashlib.sha256(b).hexdigest()
def exact_id_mentions(values,known):
 found=set();pat=re.compile(r"\b(?:OBL\d{3}|N\d{3}|S\d{3})\b")
 for value in values:
  for tok in pat.findall(str(value)):
   if tok in known:found.add(tok)
 return found
def domain_requirements(scope,g):
 if not scope:return False,{}
 reqs=set(split(scope.get("required_state_ids")));reqo=set(split(scope.get("required_obligation_ids")));reqb=split(scope.get("required_binding_surfaces"));reqm=split(scope.get("required_must_factor_surfaces"));bset=set(g.get("binding_authority_surfaces_read",[])) if isinstance(g.get("binding_authority_surfaces_read"),list) else set();mset=set(g.get("must_factor_surfaces_read",[])) if isinstance(g.get("must_factor_surfaces_read"),list) else set();rs=set(g.get("relevant_state_ids",[])) if isinstance(g.get("relevant_state_ids"),list) else set();ro=set(g.get("relevant_obligation_ids",[])) if isinstance(g.get("relevant_obligation_ids"),list) else set();paths_ok=all((PREMAIN/x).exists() for x in reqb+reqm)
 return bool(reqs<=rs and reqo<=ro and set(reqb)<=bset and set(reqm)<=mset and paths_ok),{"required_states":sorted(reqs),"required_obligations":sorted(reqo),"required_surfaces":reqb+reqm}
def active_accounting(g,exclusions,obligations):
 rs=g.get("relevant_state_ids",[]) if isinstance(g.get("relevant_state_ids"),list) else [];ro=g.get("relevant_obligation_ids",[]) if isinstance(g.get("relevant_obligation_ids"),list) else [];exids=[x.get("obligation_id") for x in exclusions if isinstance(x,dict)];exok=uniq([x for x in exids if x]) and all(isinstance(x,dict) and x.get("obligation_id") in obligations and bool(x.get("reason")) and x.get("preserved_open") is True for x in exclusions);active={}
 for oid,r in obligations.items():
  if r.get("status") not in TERMINAL_DISPOSITIONS:active.setdefault(r.get("parent_state_id",""),set()).add(oid)
 active_rel=set().union(*(active.get(s,set()) for s in rs)) if rs else set();return bool(exok and uniq(ro) and set(ro)<=set(obligations) and active_rel<=(set(ro)|set(exids))),set(exids)
def parent_packet_grounding_ok(parent,scopes,states,obligations,levels,ar,live_sha,gv):
 if not isinstance(parent,dict):return False
 g=parent.get("grounding_receipt",{});w=parent.get("work_return",{});u=parent.get("central_state_update",{});domain=parent.get("decision_domain");effect=parent.get("requested_effect");scope=scopes.get(domain)
 checks=[]
 for obj,file in [(parent,"GOVERNANCE_PACKET_SCHEMA_R2.json"),(g,"GROUNDING_RECEIPT_SCHEMA.json"),(w,"WORK_RETURN_SCHEMA.json"),(u,"CENTRAL_STATE_UPDATE_SCHEMA.json")]:checks.append(schema_check(obj,GOV/file)[0])
 checks += [g.get("agent_mode")=="GROUNDED_PROJECT_DECISION",w.get("agent_mode")=="GROUNDED_PROJECT_DECISION",g.get("canonical_project_head")==live_sha,w.get("canonical_launch_head")==live_sha,u.get("canonical_project_head")==live_sha,g.get("ground_version")==gv,u.get("ground_version")==gv,g.get("grounding_complete_for_declared_scope")=="PASS",u.get("grounding_receipt_id")==g.get("grounding_receipt_id"),bool(scope and scope.get("adoption_eligible")=="YES"),effect in ADOPTIVE_EFFECTS,effect in set(split(scope.get("allowed_requested_effects") if scope else "")),g.get("authority_ceiling") in levels,u.get("authority_ceiling")==g.get("authority_ceiling"),effect not in EFFECT_AUTHORITY or g.get("authority_ceiling") in EFFECT_AUTHORITY[effect],domain_requirements(scope,g)[0]]
 rs=g.get("relevant_state_ids",[]) if isinstance(g.get("relevant_state_ids"),list) else [];ro=g.get("relevant_obligation_ids",[]) if isinstance(g.get("relevant_obligation_ids"),list) else [];ts=u.get("touched_state_ids",[]) if isinstance(u.get("touched_state_ids"),list) else [];to=u.get("touched_obligation_ids",[]) if isinstance(u.get("touched_obligation_ids"),list) else [];allowed_s=set(split(scope.get("allowed_state_ids") if scope else ""));allowed_o=set(split(scope.get("allowed_obligation_ids") if scope else ""));checks += [bool(rs and uniq(rs) and set(rs)<=states),bool(uniq(ts) and set(ts)<=states),bool("*" in allowed_s or set(ts)<=allowed_s),bool("*" in allowed_o or set(to)<=allowed_o)]
 acct,exids=active_accounting(g,parent.get("scope_exclusions",[]) if isinstance(parent.get("scope_exclusions"),list) else [],obligations);checks.append(acct);checks.append(not(set(split(scope.get("required_obligation_ids") if scope else ""))&exids));ack=g.get("anti_resurrection_constraints",[]) if isinstance(g.get("anti_resurrection_constraints"),list) else [];checks.append(bool(uniq(ack) and set(ack)<=ar));known=states|set(obligations);checks.append(g.get("required_return_destination") in known and u.get("return_destination")==g.get("required_return_destination"));return all(checks)
def enforcement_integrity(live_sha:str):
 try:rows=tsv(GOV/"GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv")
 except Exception:return False,["manifest-unreadable"]
 mismatches=[];root=repo_root()
 for r in rows:
  rel=r.get("path","");p=root/rel
  if not rel or not p.exists():mismatches.append(rel or "<empty>");continue
  ok,canon=run_git("rev-parse",f"{live_sha}:{rel}")
  if not ok:mismatches.append(rel);continue
  ok,cur=run_git("hash-object",str(p))
  if not ok or cur!=canon:mismatches.append(rel)
 return not mismatches,mismatches
def _type(v,t):return {"object":isinstance(v,dict),"array":isinstance(v,list),"string":isinstance(v,str),"boolean":isinstance(v,bool),"integer":isinstance(v,int) and not isinstance(v,bool),"number":isinstance(v,(int,float)) and not isinstance(v,bool),"null":v is None}.get(t,False)
def subset_validate(inst:Any,s:dict,path="$"):
 e=[]
 if "type" in s:
  ts=s["type"] if isinstance(s["type"],list) else [s["type"]]
  if not any(_type(inst,t) for t in ts):return [f"{path}:type"]
 if "const" in s and inst!=s["const"]:e.append(f"{path}:const")
 if "enum" in s and inst not in s["enum"]:e.append(f"{path}:enum")
 if isinstance(inst,str):
  if len(inst)<s.get("minLength",0):e.append(f"{path}:minLength")
  if "pattern" in s and not re.search(s["pattern"],inst):e.append(f"{path}:pattern")
 if isinstance(inst,list):
  if len(inst)<s.get("minItems",0):e.append(f"{path}:minItems")
  if "items" in s:
   for i,x in enumerate(inst):e+=subset_validate(x,s["items"],f"{path}[{i}]")
 if isinstance(inst,dict):
  for k in s.get("required",[]):
   if k not in inst:e.append(f"{path}:missing:{k}")
  props=s.get("properties",{})
  if s.get("additionalProperties") is False:
   for k in inst:
    if k not in props:e.append(f"{path}:additional:{k}")
  for k,ss in props.items():
   if k in inst:e+=subset_validate(inst[k],ss,f"{path}.{k}")
 return e
def schema_check(inst,path):
 try:s=json.loads(path.read_text(encoding="utf-8"))
 except Exception as ex:return False,[f"schema-load:{ex}"]
 if jsonschema is not None:
  try:jsonschema.Draft202012Validator(s).validate(inst);return True,[]
  except Exception as ex:return False,[str(ex).splitlines()[0]]
 e=subset_validate(inst,s);return not e,e
