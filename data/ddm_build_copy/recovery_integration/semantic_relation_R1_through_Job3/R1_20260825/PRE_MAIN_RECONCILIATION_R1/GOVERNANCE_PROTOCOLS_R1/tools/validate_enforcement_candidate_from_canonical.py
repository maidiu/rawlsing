#!/usr/bin/env python3
"""Validate a governance-enforcement candidate from the LIVE CANONICAL predecessor copy.

A modified candidate copy is not authoritative. Hostile audit evidence must be
pre-authorized from a branch rooted directly at the live canonical predecessor.
"""
from governance_r2_support import *

SELF_REL="data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/GOVERNANCE_PROTOCOLS_R1/tools/validate_enforcement_candidate_from_canonical.py"
MANIFEST_REL="data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/GOVERNANCE_PROTOCOLS_R1/GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv"
AUTH_PREFIX="data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/PRE_MAIN_RECONCILIATION_R1/AUDIT_AUTHORIZATIONS/"

def git_lines(*args):
 ok,out=run_git(*args); return ok,[x for x in out.splitlines() if x]

def split_ref(v):
 if not isinstance(v,str) or ":" not in v:return "",""
 return v.split(":",1)

def branch_tip(name):
 lo,ls=run_git("rev-parse","--verify",f"refs/heads/{name}")
 ro,rs=run_git("rev-parse","--verify",f"refs/remotes/origin/{name}")
 if lo and ro and ls!=rs:return False,"","DIVERGED"
 if lo:return True,ls,"LOCAL"+("+REMOTE_MATCH" if ro else "")
 if ro:return True,rs,"REMOTE_ONLY"
 return False,"","UNRESOLVED"

def direct_child_of(commit,parent):
 ok,out=run_git("rev-list","--parents","-n","1",commit)
 parts=out.split() if ok else []
 return len(parts)==2 and parts[0]==commit and parts[1]==parent

def main():
 ap=argparse.ArgumentParser(); ap.add_argument("candidate_sha"); ap.add_argument("audit_evidence_ref"); ap.add_argument("audit_authorization_ref"); a=ap.parse_args()
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
 dok,diff=git_lines("diff","--name-only",live,a.candidate_sha); changed=set(diff); pchanged=sorted(changed&protected)
 checks["PROTECTED_CHANGE_DETECTED"]=bool(dok and pchanged); details["protected_changed_paths"]=pchanged

 auth=immutable_json(a.audit_authorization_ref); checks["AUDIT_AUTHORIZATION_IMMUTABLE_JSON"]=bool(auth)
 auth_schema_ok,_=schema_check(auth,GOV/"HOSTILE_AUDIT_AUTHORIZATION_SCHEMA_R1.json") if auth else (False,[]); checks["AUDIT_AUTHORIZATION_SCHEMA_VALID"]=auth_schema_ok
 auth_sha,auth_path=split_ref(a.audit_authorization_ref); checks["AUTHORIZATION_PATH_IS_EXTERNAL_AUDIT_PREFIX"]=bool(auth_path.startswith(AUTH_PREFIX))
 checks["AUTHORIZATION_DIRECT_CHILD_OF_LIVE_CANONICAL"]=bool(auth_sha and direct_child_of(auth_sha,live))
 cand_to_auth,_=run_git("merge-base","--is-ancestor",a.candidate_sha,auth_sha) if auth_sha else (False,""); checks["AUTHORIZATION_OUTSIDE_CANDIDATE_LINEAGE"]=bool(auth_sha and not cand_to_auth)
 arok,ardiff=git_lines("diff","--name-only",live,auth_sha) if auth_sha else (False,[]); auth_changed=set(ardiff)
 checks["AUTHORIZATION_COMMIT_JURISDICTION_PURE"]=bool(arok and auth_changed and all(x.startswith(AUTH_PREFIX) for x in auth_changed) and not(auth_changed&protected)); details["authorization_changed_paths"]=sorted(auth_changed)
 checks["AUTHORIZATION_BINDS_CANONICAL_HEAD"]=bool(auth and auth.get("canonical_head")==live)
 checks["AUTHORIZATION_BINDS_EXACT_CANDIDATE"]=bool(auth and auth.get("candidate_sha")==a.candidate_sha)

 audit=immutable_json(a.audit_evidence_ref); checks["AUDIT_EVIDENCE_IMMUTABLE_JSON"]=bool(audit)
 audit_schema_ok,_=schema_check(audit,GOV/"HOSTILE_AUDIT_RESULT_SCHEMA_R1.json") if audit else (False,[]); checks["AUDIT_RESULT_SCHEMA_VALID"]=audit_schema_ok
 audit_sha,audit_path=split_ref(a.audit_evidence_ref); terminal=str((audit or {}).get("terminal_sha","")); branch=str((audit or {}).get("audit_branch","")); expected_branch=str((auth or {}).get("expected_audit_branch","")); prefix=str((auth or {}).get("audit_write_prefix",""))
 checks["AUDIT_EVIDENCE_COMMIT_IS_DECLARED_TERMINAL"]=bool(audit_sha and audit_sha==terminal)
 checks["AUDIT_RESULT_PATH_WITHIN_AUTHORIZED_PREFIX"]=bool(prefix and audit_path.startswith(prefix))
 bok,btip,bsource=branch_tip(expected_branch) if expected_branch else (False,"",""); details["audit_branch_source"]=bsource
 checks["AUTHORIZED_AUDIT_BRANCH_RESOLVES"]=bok
 checks["AUDIT_BRANCH_TIP_IS_DECLARED_TERMINAL"]=bool(bok and btip==terminal)
 checks["AUDIT_RESULT_BRANCH_MATCHES_AUTHORIZATION"]=bool(audit and branch==expected_branch)
 aok,_=run_git("merge-base","--is-ancestor",a.candidate_sha,terminal) if terminal else (False,""); checks["AUDIT_DESCENDS_FROM_CANDIDATE"]=aok
 adok,adiff=git_lines("diff","--name-only",a.candidate_sha,terminal) if terminal else (False,[]); audit_changed=set(adiff)
 checks["AUDIT_COMMIT_JURISDICTION_PURE"]=bool(adok and audit_changed and prefix and all(x.startswith(prefix) for x in audit_changed) and not(audit_changed&protected)); details["audit_changed_paths"]=sorted(audit_changed)
 checks["AUDIT_BINDS_EXACT_AUTHORIZATION_REF"]=bool(audit and audit.get("authorization_ref")==a.audit_authorization_ref)
 checks["AUDIT_CHALLENGE_MATCH"]=bool(audit and auth and audit.get("challenge_nonce")==auth.get("challenge_nonce"))
 checks["AUDIT_BINDS_EXACT_CANDIDATE"]=bool(audit and audit.get("candidate_sha")==a.candidate_sha)
 checks["AUDIT_MODE_HOSTILE_INDEPENDENT"]=bool(audit and audit.get("audit_mode")=="HOSTILE_INDEPENDENT_AUDIT")
 ruling=str((audit or {}).get("overall_ruling","")); token=str((audit or {}).get("terminal_token","")); allowed=set((auth or {}).get("allowed_pass_rulings",[])); token_prefixes=list((auth or {}).get("allowed_terminal_token_prefixes",[]))
 checks["AUDIT_RULING_EXACTLY_AUTHORIZED_PASS"]=bool(ruling and ruling in allowed)
 checks["AUDIT_TERMINAL_TOKEN_PREFIX_AUTHORIZED"]=bool(token and any(token.startswith(x) for x in token_prefixes))

 eligible=all(checks.values())
 print(json.dumps({"checks":checks,"EXTERNAL_INTEGRATION_ELIGIBLE":eligible,"details":details},sort_keys=True))
 return 0 if eligible else 1

if __name__=="__main__": sys.exit(main())
