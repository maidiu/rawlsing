#!/usr/bin/env python3
"""C2R three-frontdoor verifier: pinned documentary parity is NOT verified current authority."""
import argparse
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
MANIFEST = ROOT / "CROSS_HQ_CONTROL_ROOM/PROGRAMMA/SHARED_RULE_SOURCE_MANIFEST_R1.json"
RULE = re.compile(r"<!-- HQ_RULE_START id=(HQ-(?:C1|C2R)-[0-9]{3}) src=([0-9a-f]{40}) -->\n(.*?)\n<!-- HQ_RULE_END id=\1 -->", re.S)
COURTS = ("ENGINEERING", "SCIENTIFIC", "AUTHORITY")
FIELDS = ("ACCEPT_IF", "FAIL_OR_RED_IF", "HOLD_IF", "EVIDENCE", "OWNER_OF_DECISION")

class Invalid(Exception):
    pass

def require(ok, why):
    if not ok:
        raise Invalid(why)

def rules_and_text(path):
    content = (ROOT / path).read_text(encoding="utf8")
    entries = {}
    for rid, sha, body in RULE.findall(content):
        require(rid not in entries, "duplicate rule: " + rid)
        entries[rid] = (sha, body)
    return entries, content

def untagged_body(content, heading):
    key = heading + "\n"
    at = content.find(key)
    require(at >= 0, "missing untagged operating section: " + heading)
    tail = content[at+len(key):]
    end = re.search(r"^#{1,4} ", tail, re.M)
    return tail[:end.start() if end else None].rstrip()

def court_matrix(content):
    heads = list(re.finditer(r"(?m)^#{2,6} (ENGINEERING|SCIENTIFIC|AUTHORITY) COURT[ \t]*$", content))
    require(tuple(h.group(1) for h in heads) == COURTS,
            "three separate ordered court blocks ENGINEERING/SCIENTIFIC/AUTHORITY required")
    for i, head in enumerate(heads):
        body = content[head.end(): heads[i+1].start()] if i+1 < len(heads) else content[head.end():]
        if i+1 == len(heads):
            body = body.split("<!-- HQ_RULE_END", 1)[0]
        rows = {}
        for line in body.splitlines():
            match = re.match(r"^(ACCEPT_IF|FAIL_OR_RED_IF|HOLD_IF|EVIDENCE|OWNER_OF_DECISION):[ \t]*(.*)$", line.strip())
            if match:
                require(match.group(1) not in rows,
                        "duplicate field in " + head.group(1) + ": " + match.group(1))
                rows[match.group(1)] = match.group(2).strip()
        require(set(rows) == set(FIELDS),
                head.group(1) + " missing field(s) " + repr(sorted(set(FIELDS)-set(rows))))
        require(all(rows.values()), head.group(1)+" empty court criterion")

def check_static(manifest):
    traces = {entry["id"]:entry for entry in manifest["all_rule_traces"]}
    require(len(traces) == len(manifest["all_rule_traces"]), "duplicate manifest rule ID")
    doors = {domain: rules_and_text(path) for domain,path in manifest["front_doors"].items()}
    for domain,(found,content) in doors.items():
        expected = set(manifest["shared_ids"] + manifest["local_ids"][domain])
        require(set(found) == expected,
                domain+" missing/extra tagged rules missing="+repr(sorted(expected-set(found)))+
                " extra="+repr(sorted(set(found)-expected)))
        for rid,(sha,body) in found.items():
            trace=traces[rid]
            require(domain.replace("_","-") in trace["scope"], domain+" wrong scope "+rid)
            require(sha == trace["source_sha"], domain+" source revision mismatch "+rid)
            for field in ("owner","trigger","action","falsifier"):
                require(trace[field] in body, domain+" material law text lost "+rid+" "+field)
        for field in manifest["required_m5_fields"]:
            require(field in content, domain+" missing M5 currentness "+field)
        for field in ("epoch_id","runtime_marker","source_closure",
                      "RAWLSING_ENVIRONMENT_PASSPORT","PASSPORT",
                      "SEVEN-STEP EXECUTABLE DISPENSATION","next_affinity_tags","module.__file__"):
            require(field in content, domain+" missing actionable warm/passport rule "+field)
        for field in ("PENDING_GUIDE_INTEGRATION","FINDINGS","INTERPRETATION","HQ ACTION","SOURCE"):
            require(field in content, domain+" prior operating requirement lost "+field)
        court_matrix(found["HQ-C2R-030"][1])
    for rid in manifest["shared_ids"]:
        versions=[doors[name][0][rid] for name in ("PRE_MAIN","PYAT","SOROK")]
        require(versions[0]==versions[1]==versions[2], "shared law-copy drift "+rid)
    for section in manifest["required_untagged_sections"]:
        current=untagged_body(doors[section["domain"]][1],section["heading"])
        require(current==section["exact_body"],
                "substantive untagged operating procedure changed/deleted: "+
                section["domain"]+" "+section["heading"])
    pyat=doors["PYAT"][1]
    require("the already existing accepted" not in pyat, "Pyat G4 falsely accepted")
    for field in ("fc8ba54e2f7f2ec4a06baf7dbc3c24ca6ac53770",
                  "accepted_guide_head=NONE_VERIFIED","49 source-identified gaps",
                  "82 typed seams","RRIF_TERMINAL__PROGRAMMA_REMAINS_USER_STOPPED",
                  "COMPARE_ONLY","ALL_OF","ANY_OF","MODE_UNSELECTED","N11","N12"):
        require(field in pyat, "Pyat status/source requirement dropped "+field)
    sorok=doors["SOROK"][1]
    for field in ("revision 36","revision 35","38 versioned seams",
                  "NOT_ISSUED","NO_CHANGE","Gate4","Gate5"):
        require(field in sorok, "Sorok authority/negative requirement dropped "+field)

def git(*args):
    proc=subprocess.run(["git","-C",str(ROOT),*args],capture_output=True,text=True)
    if proc.returncode:
        raise Invalid("selected authoritative local source unavailable: "+proc.stderr.strip()[:200])
    return proc.stdout.strip()

def check_selected_current_law(manifest, selected_ref):
    if not selected_ref:
        return "REVALIDATION_REQUIRED: no independently qualified current PRE-MAIN ref selected"
    try:
        selected_sha=git("rev-parse","--verify",selected_ref+"^{commit}")
        require(re.fullmatch(r"[0-9a-f]{40}",selected_sha), "selected authority SHA invalid")
        for source in manifest["source_laws"]:
            orig=git("rev-parse",source["pinned_commit"]+":"+source["path"])
            if orig != source["pinned_blob_sha1"]:
                return "REVALIDATION_REQUIRED: original pinned Git blob mismatched "+source["path"]
            current=git("rev-parse",selected_sha+":"+source["path"])
            if current != source["pinned_blob_sha1"]:
                return "REVALIDATION_REQUIRED: governing law revised "+source["path"]
        return ("SELECTED_SOURCE_PARITY_PASS at "+selected_sha+
                "; independently verify source ref is actual current authoritative remote HEAD and owner-selected")
    except Invalid as error:
        return "REVALIDATION_REQUIRED: "+str(error)

def check_commission(path):
    content=pathlib.Path(path).read_text(encoding="utf8")
    court_matrix(content)
    for name in ("AGENT_TYPE","INTELLIGENCE_LEVEL","EXACT_BRANCH","EXACT_STARTUP_SHA",
                 "POST_RETURN_INDEPENDENT_REVIEW","epoch_id","PASSPORT"):
        require(name in content, "complete commission missing "+name)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pinned-only",action="store_true",
                        help="static pinned-document validation; no live authority claim")
    parser.add_argument("--authoritative-ref",
                        help="owner-selected local Git ref for verified current protected PRE-MAIN")
    parser.add_argument("--commission",help="optional complete single-agent prompt for 3x5 validation")
    args=parser.parse_args()
    manifest=json.loads(MANIFEST.read_text(encoding="utf8"))
    check_static(manifest)
    if args.commission:
        check_commission(args.commission)
    print("PINNED_SOURCE_ONLY PASS: obligations="+str(len(manifest["all_rule_traces"]))+
          " shared="+str(len(manifest["shared_ids"]))+
          " untagged="+str(len(manifest["required_untagged_sections"]))+
          " source_pins="+str(len(manifest["source_laws"]))+" courts=3x5")
    if args.pinned_only:
        print("LIVE_AUTHORITATIVE_HEAD NOT_VERIFIED: static-only validation")
        return 0
    state=check_selected_current_law(manifest,args.authoritative_ref)
    print(state)
    return 2 if state.startswith("REVALIDATION_REQUIRED") else 0

if __name__=="__main__":
    try:
        sys.exit(main())
    except (Invalid, ValueError, KeyError, OSError) as error:
        print("FAIL",str(error),file=sys.stderr)
        sys.exit(1)
