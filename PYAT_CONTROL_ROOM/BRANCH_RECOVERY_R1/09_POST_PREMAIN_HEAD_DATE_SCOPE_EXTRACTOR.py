#!/usr/bin/env python3
"""Read-only post-regular-PREMAIN Git ref index. Commit-date proxy, not branch creation date.

Requires a sourcefree Git clone where all remote HEAD tip commit objects are available.
The workflow fetches tree:0 depth-one tips only; this script never reads survey bytes,
edits refs, executes user code, infers a source grant, or launches workers.
"""
from __future__ import annotations
import argparse
import collections
import datetime as dt
import json
from pathlib import Path
import re
import subprocess
import sys

UTC = dt.timezone.utc
RE_MAIN = re.compile(r"^(?:integration/pre-main-reconciliation-r1|main)$")
RE_PYAT = re.compile(r"pyat|pre553|prev3|fiabc|astra", re.I)
RE_SOROK = re.compile(r"sorok", re.I)
RE_CONTROL = re.compile(r"(^|/)(?:controller|hq|control-room)", re.I)
DATE_NAME = re.compile(r"20(?:2[5-9]|3[0-9])[-_]?([01][0-9])[-_]?([0-3][0-9])")

def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], text=True, stderr=subprocess.PIPE)

def commit_info(oid: str) -> dict:
    raw = git("cat-file", "-p", oid)
    head = raw.split("\n\n", 1)[0].splitlines()
    kind = ""
    parent = []
    times = []
    for line in head:
        if line.startswith("tree "):
            kind = line[5:]
        elif line.startswith("parent "):
            parent.append(line[7:])
        elif line.startswith("author ") or line.startswith("committer "):
            m = re.search(r" ([0-9]{9,12}) [+-][0-9]{4}$", line)
            if m:
                times.append((line.split(" ",1)[0], int(m.group(1))))
    timestamp = dict(times)
    return {"tree_oid": kind, "parents": parent, "author_utc":timestamp.get("author"),
      "committer_utc": timestamp.get("committer")}

def categorise(name: str) -> str:
    if RE_MAIN.match(name): return "CURRENT_MAIN_OR_PREMAIN"
    if RE_SOROK.search(name) and not RE_PYAT.search(name): return "SOROK_BOUNDARY"
    if RE_PYAT.search(name): return "PYAT_OR_SHARED"
    if RE_CONTROL.search(name): return "OTHER_HQ_OR_CONTROLLER_CANDIDATE"
    return "UNKNOWN_REQUIRES_CONTENT_TRIAGE"

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--cutoff", required=True, help="RFC3339 UTC, exact last integration candidate")
    a.add_argument("--cutoff-sha", required=True)
    a.add_argument("--output", required=True, type=Path)
    args=a.parse_args()
    threshold=int(dt.datetime.fromisoformat(args.cutoff.replace("Z","+00:00")).timestamp())
    refs=git("for-each-ref","--format=%(refname)\t%(objectname)","refs/remotes/origin/").splitlines()
    records=[]
    object_cache={}
    errors=[]
    for line in refs:
        if "\t" not in line: continue
        ref, oid=line.split("\t",1)
        if not ref.startswith("refs/remotes/origin/"): continue
        name=ref[len("refs/remotes/origin/"):]
        if name=="HEAD": continue
        if not re.fullmatch(r"[0-9a-f]{40}",oid):
            errors.append({"branch":name,"reason":"BAD_OID"}); continue
        try:
            if oid not in object_cache: object_cache[oid]=commit_info(oid)
            info=object_cache[oid]
        except (subprocess.CalledProcessError,ValueError) as exc:
            errors.append({"branch":name,"reason":"COMMIT_OBJECT_UNAVAILABLE", "error":str(exc)[:220]}); continue
        time=info["committer_utc"]
        grade="POST_CUTOFF_TIP_DATE" if time is not None and time >= threshold else "BEFORE_OR_UNKNOWN_TIP_DATE"
        records.append({"branch":name,"tip_sha":oid,"cohort_date_status":grade,"kind":categorise(name),
            "committer_time_utc":dt.datetime.fromtimestamp(time,UTC).isoformat() if time is not None else None,
            "author_time_utc":dt.datetime.fromtimestamp(info["author_utc"],UTC).isoformat() if info["author_utc"] is not None else None,
            "tree_sha":info["tree_oid"],"parent_shas":info["parents"]})
    if errors or len(records)<2500:
        print(json.dumps({"status":"INCOMPLETE__NO_COHORT_CLAIM","refs_read":len(records),"errors":errors[:10]}))
        return 2
    post=[x for x in records if x["cohort_date_status"]=="POST_CUTOFF_TIP_DATE"]
    post_nonmain=[x for x in post if x["kind"]!="CURRENT_MAIN_OR_PREMAIN"]
    post_pyat=[x for x in post_nonmain if x["kind"] in ("PYAT_OR_SHARED","OTHER_HQ_OR_CONTROLLER_CANDIDATE","UNKNOWN_REQUIRES_CONTENT_TRIAGE")]
    before=[x for x in records if x["cohort_date_status"]=="BEFORE_OR_UNKNOWN_TIP_DATE"]
    counts=dict(collections.Counter(x["kind"] for x in post))
    result={"schema":"PYAT_POST_INTEGRATION_HEAD_DATE_COHORT@1","status":"CANDIDATE_SET_NOT_CREATION_PROOF",
        "cutoff_sha":args.cutoff_sha,"cutoff_time_utc":args.cutoff,
        "source_method":"git fetch depth=1 filter=tree:0 ALL HEAD refs, git cat-file commit metadata; no branch creation time available",
        "epistemic_limits":["Branch tip date is not branch creation/push date","Old refs may advance late","New branch made from old SHA is not detected","Commit clock can be rewritten or backdated","Candidates require merge-base and actual touched-files census before indexed acceptance"],
        "ref_count":len(records),"distinct_tip_sha_count":len(object_cache),
        "post_cutoff_refs_all":len(post),"post_cutoff_nonmain_refs":len(post_nonmain),
        "post_cutoff_pyat_potential_including_unknown":len(post_pyat),
        "pre_cutoff_or_unknown_tip_refs":len(before),"post_cutoff_categories":counts,
        "post_cutoff_nonmain_heads":sorted(post_nonmain,key=lambda x:x["branch"]),
        "pre_cutoff_tip_names":[{"branch":x["branch"],"tip_sha":x["tip_sha"]} for x in before],
        "all_refs":sorted(records,key=lambda x:x["branch"]),"errors":errors}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    print("CUT_SHA",args.cutoff_sha,"CUT_TIME",args.cutoff)
    print("TOTAL_REFS",len(records),"UNIQUE_HEADS",len(object_cache))
    print("POST_CUTOFF_ALL",len(post),"POST_CUTOFF_NONMAIN",len(post_nonmain))
    print("POST_CUTOFF_PYAT_POTENTIAL_WITH_UNKNOWN",len(post_pyat))
    print("PRE_CUTOFF_OR_UNKNOWN",len(before))
    print("POST_CATEGORIES",json.dumps(counts,sort_keys=True))
    print("CAVEAT: TIP DATE NOT BRANCH CREATION DATE. NO RECOVERY/CONTENT-INDEX CLAIM.")
    return 0

if __name__=="__main__": sys.exit(main())
