#!/usr/bin/env python3
"""Verify a scoped operational projection, not a grant of source/scientific authority."""
import argparse
import copy
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROGRESS = ROOT / "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.json"
MARKDOWN = ROOT / "SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md"
START = "<!-- SOROK_OPERATIONAL_CURRENT_START -->"
END = "<!-- SOROK_OPERATIONAL_CURRENT_END -->"
EXPECTED = {f"{f}{i:02d}" for f,n in (("B",5),("C",5),("D",5),("E",4),("F",4),("G",4)) for i in range(1,n+1)}
COUNTS = {"G":6,"M":12,"T":9}
PROTECTED = {"P3","P4","P5","P6","MI","MII","MIII"}
HEX = re.compile(r"^[0-9a-f]{40}$")

def validate(s, git=True):
    errors=[]
    tasks=s.get("tasks",[])
    ids=[t.get("id") for t in tasks]
    if s.get("schema")!="SOROK_OPERATIONAL_CURRENTNESS_R1":
        errors.append("wrong schema")
    if len(ids)!=27 or set(ids)!=EXPECTED or len(set(ids))!=27:
        errors.append("27 original packet IDs incomplete or duplicate")
    if {k:sum(t.get("class")==k for t in tasks) for k in COUNTS}!=COUNTS:
        errors.append("G/M/T classification count drift")
    edges={}
    for t in tasks:
        name=t.get("id")
        deps=t.get("depends_on",[])
        if not isinstance(deps,list) or len(deps)!=len(set(deps)) or any(d not in EXPECTED for d in deps):
            errors.append(str(name)+": invalid original dependencies")
        edges[name]=deps
        if t.get("sourcefree_state") not in {"CANDIDATE","SCOPED_RECEIVED_UNMERGED","HELD_NOT_LAUNCHED","PARTIAL_CANDIDATE"}:
            errors.append(str(name)+": invalid engineering state")
        if t.get("full_original_claim")!="NOT_ESTABLISHED":
            errors.append(str(name)+": full original claim inflated")
        if t.get("sourcefree_state")=="SCOPED_RECEIVED_UNMERGED":
            if not t.get("review_pr") or not HEX.fullmatch(t.get("code_sha","")) or not HEX.fullmatch(t.get("review_sha","")):
                errors.append(str(name)+": unpinned scoped acceptance")
    active,visited=set(),set()
    def visit(k):
        if k in active:
            errors.append("dependency cycle at "+k);return
        if k in visited or k not in edges:return
        active.add(k)
        for d in edges[k]: visit(d)
        active.remove(k)
        visited.add(k)
    for k in edges:visit(k)
    foundations=s.get("protected_foundations",{})
    if set(foundations)!=PROTECTED:
        errors.append("protected 7-component denominator drift")
    for name in PROTECTED.intersection(foundations):
        r=foundations[name]
        sha=r.get("merge_sha","")
        if r.get("scope")!="SOURCEFREE_PROTECTED" or not HEX.fullmatch(sha):
            errors.append(name+": invalid protected-scope claim")
        elif git:
            done=subprocess.run(["git","merge-base","--is-ancestor",sha,"HEAD"],cwd=ROOT,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            if done.returncode!=0:errors.append(name+": protected merge not ancestor of HEAD")
    for k in ("B05","C05"):
        t=next((v for v in tasks if v.get("id")==k),{})
        if t.get("sourcefree_state")!="SCOPED_RECEIVED_UNMERGED":
            errors.append(k+": latest scoped G5 lost")
    if s.get("adoption") not in {"PENDING_INDEPENDENT_RECEIVING","ADOPTED_PROTECTED_CURRENTNESS"}:
        errors.append("adoption omitted")
    if s.get("unreconciled_external_events")!="UNKNOWN_REQUIRES_LIVE_INTAKE":
        errors.append("external event completeness falsely claimed")
    if s.get("execution",{}).get("locally_verified_live_workers") is not None:
        errors.append("GitHub snapshot cannot certify live process state")
    return errors

def render(s):
    parts=[START,
           "## SOROK operational currentness — generated from paired JSON",
           "**Cut:** "+s["as_of"]+" | **Adoption:** "+s["adoption"],
           "**Evidence grade:** sourcefree engineering where stated; never native, scientific, human or protected integration by implication.",
           "",
           "**Protected:** "+", ".join(name+" (#"+str(s["protected_foundations"][name]["pr"])+")" for name in ("P3","P4","P5","P6","MI","MII","MIII"))+".",
           "**Scoped received, unmerged:** "+", ".join(t["id"]+" (#"+str(t["review_pr"])+")" for t in s["tasks"] if t["sourcefree_state"]=="SCOPED_RECEIVED_UNMERGED")+".",
           "",
           "**Current blockers and next owner actions:**"]
    for x in s.get("work_frontier",[]):
        parts.append("- "+x["id"]+" | "+x["state"]+" | owner: "+x["owner"]+" | next: "+x["next_action"])
    parts += ["","**None of the 27 whole original CG-B–G claims is marked complete.**",
              "**External PR/review events and local runner processes:** must be authenticated at each HQ intake; older comments and stored leases are history, not live state.",
              END]
    return "\n".join(parts)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--self-test",action="store_true")
    ap.add_argument("--status",action="store_true")
    ap.add_argument("--no-git",action="store_true")
    args=ap.parse_args()
    s=json.loads(PROGRESS.read_text())["operational_currentness_r1"]
    errors=validate(s,git=not args.no_git)
    m=MARKDOWN.read_text()
    if m.count(START)!=1 or m.count(END)!=1:
        errors.append("MD projection markers absent/duplicated")
    elif m[m.index(START):m.index(END)+len(END)]!=render(s):
        errors.append("MD/JSON projection drift")
    if args.self_test:
        for mutation in ("B05","MI","DUPLICATE","FULL_CLAIM"):
            t=copy.deepcopy(s)
            if mutation=="B05": next(v for v in t["tasks"] if v["id"]=="B05")["sourcefree_state"]="CANDIDATE"
            if mutation=="MI": del t["protected_foundations"]["MI"]
            if mutation=="DUPLICATE": t["tasks"].append(copy.deepcopy(t["tasks"][0]))
            if mutation=="FULL_CLAIM":t["tasks"][0]["full_original_claim"]="ACCEPT"
            if not validate(t,git=False):errors.append("self-test missed "+mutation)
    if args.status:print(render(s))
    if errors:
        for e in errors: print("SOROK_CURRENTNESS_RED: "+e,file=sys.stderr)
        return 1
    print("SOROK_CURRENTNESS_PASS: 27 packets, 7 protected foundations, scoped grades conserved")
    return 0

if __name__=="__main__":sys.exit(main())
