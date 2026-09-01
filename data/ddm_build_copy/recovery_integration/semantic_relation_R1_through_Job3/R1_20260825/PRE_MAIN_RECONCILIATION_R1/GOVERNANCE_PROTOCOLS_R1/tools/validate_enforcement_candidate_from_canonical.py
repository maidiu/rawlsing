#!/usr/bin/env python3
"""Validate a governance-enforcement candidate from the LIVE CANONICAL predecessor copy.

This script is intentionally a meta-governance gate. A modified candidate copy is not authoritative.
"""
from governance_r2_support import *

SELF_REL="data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/GOVERNANCE_PROTOCOLS_R1/tools/validate_enforcement_candidate_from_canonical.py"
MANIFEST_REL="data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/GOVERNANCE_PROTOCOLS_R1/GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv"

def git_lines(*args):
 ok,out=run_git(*args); return ok,[x for x in out.splitlines() if x]

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("candidate_sha"); ap.add_argument("audit_evidence_ref"); a=ap.parse_args()
 ok,live,src=live_canonical(); checks={"LIVE_CANONICAL_REF_RESOLVED":ok}; details={"live_sha":live,"source":src}
 if not ok:
  print(json.dumps({"checks":checks,"EXTERNAL_INTEGRATION_ELIGIBLE":False,"details":details},sort_keys=True)); return 1
 ok1,canon_blob=run_git("rev-parse",f"{live}:{SELF_REL}"); ok2,current_blob=run_git("hash-object",str(Path(__file__).resolve()))
 checks["EXECUTING_COPY_IS_CANONICAL_PREDECESSOR"]=bool(ok1 and ok2 and canon_blob==current_blob)
 cok,_=run_git("cat-file","-e",f"{a.candidate_sha}^{{commit}}"); checks["CANDIDATE_COMMIT_EXISTS"]=cok
 anc,_=run_git("merge-base","--is-ancestor",live,a.candidate_sha); checks["CANDIDATE_DESCENDS_FROM_LIVE_CANONICAL"]=anc
 mok,mtext=run_git("show",f"{live}:{MANIFEST_REL}"); protected=set()
 if mok:
  rows=list(csv.DictReader(mtext.splitlines(),delimiter="\t")); protected={r.get("path","") for r in rows if r.get("path")}
 checks["CANONICAL_PROTECTED_MANIFEST_LOADED"]=bool(protected)
 dok,diff=git_lines("diff","--name-only",live,a.candidate_sha); changed=set(diff); pchanged=sorted(changed&protected); checks["PROTECTED_CHANGE_DETECTED"]=bool(dok and pchanged); details["protected_changed_paths"]=pchanged
 audit=immutable_json(a.audit_evidence_ref); checks["AUDIT_EVIDENCE_IMMUTABLE_JSON"]=bool(audit)
 audit_sha=a.audit_evidence_ref.split(":",1)[0] if ":" in a.audit_evidence_ref else ""; aok,_=run_git("merge-base","--is-ancestor",a.candidate_sha,audit_sha) if audit_sha else (False,""); checks["AUDIT_DESCENDS_FROM_CANDIDATE"]=aok
 ruling=str((audit or {}).get("overall_ruling",(audit or {}).get("ruling",""))); token=str((audit or {}).get("terminal_token","")); candidate_claim=str((audit or {}).get("candidate",(audit or {}).get("candidate_sha","")))
 checks["AUDIT_RULING_PASS"]=bool(ruling.startswith("PASS") or "_PASS" in ruling or "READY" in ruling)
 checks["AUDIT_BINDS_EXACT_CANDIDATE"]=bool(candidate_claim==a.candidate_sha or a.candidate_sha in token)
 eligible=all(checks.values()); print(json.dumps({"checks":checks,"EXTERNAL_INTEGRATION_ELIGIBLE":eligible,"details":details},sort_keys=True)); return 0 if eligible else 1

if __name__=="__main__": sys.exit(main())
