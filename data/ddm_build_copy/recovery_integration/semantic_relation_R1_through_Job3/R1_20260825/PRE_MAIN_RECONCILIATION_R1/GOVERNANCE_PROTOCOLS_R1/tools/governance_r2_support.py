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
MODE_EFFECTS={
 "GROUNDED_PROJECT_DECISION": ADOPTIVE_EFFECTS|{"FORENSIC_RETURN"},
 "GROUNDED_BOUNDED_EXECUTION":{"BOUNDED_EXECUTION_RETURN"},
 "FORENSIC_READ_ONLY":{"FORENSIC_RETURN"},
 "HOSTILE_INDEPENDENT_AUDIT":{"FORENSIC_RETURN"},
 "DELIBERATELY_UNGROUNDED_EXPLORATION":{"EXPLORATORY_RETURN"},
}
EFFECT_AUTHORITY={
 "PROJECT_ADOPTION":{"HQ_BANKED_AUTHORITY","GLOBAL_SOVEREIGN_CONTROL"},
 "CAMPAIGN_ACCEPTANCE":{"DELEGATED_ACCEPTED_AUTHORITY","HQ_BANKED_AUTHORITY","GLOBAL_SOVEREIGN_CONTROL"},
 "HQ_BANKING":{"HQ_BANKED_AUTHORITY","GLOBAL_SOVEREIGN_CONTROL"},
 "GLOBAL_ADOPTION":{"GLOBAL_SOVEREIGN_CONTROL"},
 "PROJECT_CLOSURE_AT_GRAIN":{"PROJECT_CURRENT_AUTHORITY","HQ_BANKED_AUTHORITY","GLOBAL_SOVEREIGN_CONTROL"},
}
DISPOSITIONS={"OPEN","PARTIALLY_CLOSED","BLOCKED_ON_DEPENDENCY","SUSPENDED_ON_DEPENDENCY","SPAWNED_SUCCESSOR_RETURN_REQUIRED","INTERRUPTED_STRANDED","RETURN_REQUIRED","UNKNOWN_REQUIRES_SYNTHESIS","SUPERSEDED_AT_GRAIN_WITH_SURVIVING_OBLIGATION","ABANDONED_BY_EXPLICIT_DECISION","CLOSED"}
CLOSURE_FORBIDDEN_REINTEGRATION={"LOCAL_COMPLETE_UNRECONCILED","CAMPAIGN_ACCEPTED_UNBANKED","HQ_BANKED_NOT_CANONICALLY_INHERITED","SPAWNED_SUCCESSOR_RETURN_REQUIRED","BLOCKED_ON_DEPENDENCY","INTERRUPTED_STRANDED","UNKNOWN_REQUIRES_SYNTHESIS","EXPLORATORY_UNRECONCILED","ACTIVE_GROUNDED"}
BOUNDED_PROHIBITIONS={"NO_NEW_PROJECT_DECISIONS","NO_AUTHORITY_REINTERPRETATION","NO_OPEN_OBLIGATION_CLOSURE","NO_SUBSTITUTION","NO_FROZEN_ADJUDICATION_REINTERPRETATION"}
CURRENT_NONTERMINAL={"OPEN","PARTIALLY_CLOSED","BLOCKED_ON_DEPENDENCY","SUSPENDED_ON_DEPENDENCY","SPAWNED_SUCCESSOR_RETURN_REQUIRED","INTERRUPTED_STRANDED","RETURN_REQUIRED","UNKNOWN_REQUIRES_SYNTHESIS","SUPERSEDED_AT_GRAIN_WITH_SURVIVING_OBLIGATION"}

if os.environ.get("RAWLSING_SCHEMA_ENGINE") == "internal_subset":
 jsonschema=None
 SCHEMA_ENGINE="internal_subset"
else:
 try:
  import jsonschema  # type: ignore
  SCHEMA_ENGINE="jsonschema"
 except Exception:
  jsonschema=None
  SCHEMA_ENGINE="internal_subset"

def tsv(path:Path):
 with path.open(encoding="utf-8",newline="") as f: return list(csv.DictReader(f,delimiter="\t"))
def split(v): return [x for x in (v or "").split(";") if x]
def uniq(xs): return len(xs)==len(set(xs))
def run_git(*args):
 try:
  p=subprocess.run(["git","-C",str(PREMAIN),*args],text=True,capture_output=True,timeout=10)
  return p.returncode==0,p.stdout.strip()
 except Exception: return False,""
def repo_root():
 ok,out=run_git("rev-parse","--show-toplevel"); return Path(out) if ok and out else PREMAIN
def live_canonical():
 lo,ls=run_git("rev-parse","--verify",f"refs/heads/{CANONICAL_REF}")
 ro,rs=run_git("rev-parse","--verify",f"refs/remotes/origin/{CANONICAL_REF}")
 if lo and ro and ls!=rs: return False,"","FAIL_CANONICAL_REF_DIVERGENCE"
 if lo: return True,ls,"LOCAL"+("+REMOTE_MATCH" if ro else "")
 if ro: return True,rs,"REMOTE_ONLY"
 return False,"","FAIL_CANONICAL_REF_UNRESOLVED"
def ground_version():
 try: text=(PREMAIN/"00_RAWLSING_GROUND.md").read_text(encoding="utf-8")
 except Exception: return False,""
 m=re.search(r"\*\*Ground version:\*\*\s*`([^`]+)`",text); return bool(m),m.group(1) if m else ""
def resolve_ref(v:str):
 if not v: return False
 for p in [PREMAIN/v, repo_root()/v]:
  try:
   if p.exists(): return True
  except Exception: pass
 ok,_=run_git("cat-file","-e",v); return ok
def sha256(path:Path):
 h=hashlib.sha256()
 with path.open("rb") as f:
  for chunk in iter(lambda:f.read(65536),b""): h.update(chunk)
 return h.hexdigest()
def locate_path(v:str):
 for p in [PREMAIN/v,repo_root()/v]:
  if p.exists(): return p
 return PREMAIN/v

def _type(v,t):
 return {"object":isinstance(v,dict),"array":isinstance(v,list),"string":isinstance(v,str),"boolean":isinstance(v,bool),"integer":isinstance(v,int) and not isinstance(v,bool),"number":isinstance(v,(int,float)) and not isinstance(v,bool),"null":v is None}.get(t,False)
def subset_validate(inst:Any,s:dict,path="$"):
 e=[]
 if "type" in s:
  ts=s["type"] if isinstance(s["type"],list) else [s["type"]]
  if not any(_type(inst,t) for t in ts): return [f"{path}:type"]
 if "const" in s and inst!=s["const"]: e.append(f"{path}:const")
 if "enum" in s and inst not in s["enum"]: e.append(f"{path}:enum")
 if isinstance(inst,str):
  if len(inst)<s.get("minLength",0): e.append(f"{path}:minLength")
  if "pattern" in s and not re.search(s["pattern"],inst): e.append(f"{path}:pattern")
 if isinstance(inst,list):
  if len(inst)<s.get("minItems",0): e.append(f"{path}:minItems")
  if "items" in s:
   for i,x in enumerate(inst): e += subset_validate(x,s["items"],f"{path}[{i}]")
 if isinstance(inst,dict):
  for k in s.get("required",[]):
   if k not in inst: e.append(f"{path}:missing:{k}")
  props=s.get("properties",{})
  if s.get("additionalProperties") is False:
   for k in inst:
    if k not in props: e.append(f"{path}:additional:{k}")
  for k,ss in props.items():
   if k in inst: e += subset_validate(inst[k],ss,f"{path}.{k}")
 return e
def schema_check(inst,path):
 try: s=json.loads(path.read_text(encoding="utf-8"))
 except Exception as ex: return False,[f"schema-load:{ex}"]
 if jsonschema is not None:
  try: jsonschema.Draft202012Validator(s).validate(inst); return True,[]
  except Exception as ex: return False,[str(ex).splitlines()[0]]
 e=subset_validate(inst,s); return not e,e
