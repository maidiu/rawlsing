#!/usr/bin/env python3
"""Offline schema/custody consistency only. Cannot verify Mac UI names, accounts, or authority."""
import json, pathlib, re, sys, copy
P=pathlib.Path(__file__).resolve().parent
SHA=re.compile(r"^[a-f0-9]{40}$")
DEV={"oldMac","mainMac","BROWSER","OTHER_VERIFIED","UNKNOWN"}
HAR={"Codex","OpenCode","DeepSeek-Harness","Browser","OTHER_VERIFIED","UNKNOWN"}
STATUS={"SEALED_NOT_LAUNCHED","ACTIVE_VERIFIED","RETURNED","HOLD"}
REQUIRED=("registry_id","revision","commission_id","branch","status","device","device_evidence","harness","agent_name","agent_id","agent_role","model_id",
"reasoning_effort_requested","reasoning_effort_verified","session_name","session_locator_type",
"return_sha","return_directory","confirmed_by","machine_claim","locator_status")
def check(obj):
 errors=[]; rows=obj.get("records",[])
 if obj.get("schema")!="CROSS_HQ_SESSION_LOCATOR_REGISTRY@1" or not isinstance(rows,list):return ["INVALID_SCHEMA"]
 seen=set(); latest={}
 for i,r in enumerate(rows):
  pre=f"row{i}:"
  for k in REQUIRED:
   if k not in r:errors.append(pre+"MISSING_"+k)
  if r.get("device") not in DEV:errors.append(pre+"DEVICE")
  if r.get("harness") not in HAR:errors.append(pre+"HARNESS")
  if r.get("status") not in STATUS:errors.append(pre+"STATUS")
  if not isinstance(r.get("agent_name"),str) or not r["agent_name"].strip():errors.append(pre+"AGENT_NAME")
  if not isinstance(r.get("agent_role"),str) or not r["agent_role"].strip():errors.append(pre+"AGENT_ROLE")
  if not isinstance(r.get("revision"),int) or r["revision"]<1:errors.append(pre+"REVISION")
  if r.get("return_sha") is not None and not SHA.fullmatch(str(r["return_sha"])):errors.append(pre+"RETURN_SHA")
  name=r.get("session_name"); proposed=r.get("suggested_session_name")
  if name is not None and (not isinstance(name,str) or not name.strip()):errors.append(pre+"EMPTY_TITLE")
  if name is not None and name==proposed and r.get("confirmed_by")=="UNVERIFIED":errors.append(pre+"UNVERIFIED_PROPOSED_TITLE_AS_OBSERVED")
  if r.get("device") in {"oldMac","mainMac"} and r.get("device_evidence") in {"LOCAL_MAC_REPORTED_WHICH_MACHINE_UNVERIFIED","UNVERIFIED"}:errors.append(pre+"MAC_GUESSED")
  if r.get("harness")=="DeepSeek-Harness" and str(r.get("model_id","")).startswith("opencode-go/"):errors.append(pre+"MODEL_CONFUSED_WITH_HARNESS")
  if not r.get("registry_id") or not r.get("commission_id") or not r.get("branch"):errors.append(pre+"NO_IDENTIFIERS")
  k=(r.get("commission_id"),r.get("revision"))
  if k in seen:errors.append(pre+"DUPLICATE_REVISION")
  seen.add(k)
  prev=latest.get(r.get("commission_id"),0)
  if isinstance(r.get("revision"),int):
   if r["revision"]!=prev+1:errors.append(pre+"NON_APPEND_REVISION")
   latest[r.get("commission_id")]=r["revision"]
 return errors
def main():
 obj=json.loads((P/"SESSION_LOCATORS.json").read_text())
 issues=check(obj)
 if issues:
  print("FAIL",issues);return 1
 print("PASS",len(obj["records"]),"locators, no host/session identity or authority attested")
 if "--selftest" in sys.argv:
  trials=[
   ("MAC_GUESSED",lambda x:x["records"][1].update(device="oldMac")),
   ("MODEL_CONFUSED_WITH_HARNESS",lambda x:x["records"][1].update(harness="DeepSeek-Harness")),
   ("DUPLICATE_REVISION",lambda x:x["records"].append(copy.deepcopy(x["records"][0]))),
   ("RETURN_SHA",lambda x:x["records"][0].update(return_sha="fake")),
   ("UNVERIFIED_PROPOSED_TITLE_AS_OBSERVED",lambda x:x["records"][0].update(session_name="same",suggested_session_name="same",confirmed_by="UNVERIFIED")),
   ("AGENT_NAME",lambda x:x["records"][0].update(agent_name=""))
  ]
  for required,mutator in trials:
   other=copy.deepcopy(obj);mutator(other);found=check(other)
   assert any(required in z for z in found),(required,found)
  print("PASS 6 adversarial locator integrity witnesses")
 return 0
if __name__=="__main__":raise SystemExit(main())
