#!/usr/bin/env python3
"""Static source-ID no-drop + exact shared text parity validator, not a semantic/court/native judgment."""
import json, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
MANIFEST=ROOT/"CROSS_HQ_CONTROL_ROOM/PROGRAMMA/SHARED_RULE_SOURCE_MANIFEST_R1.json"
RULE=re.compile(r"<!-- HQ_RULE_START id=(HQ-C1-[0-9]{3}) src=([0-9a-f]{40}) -->\n(.*?)\n<!-- HQ_RULE_END id=\1 -->",re.S)
def read(path):
    s=(ROOT/path).read_text(encoding="utf8")
    x={}
    for id,sha,body in RULE.findall(s):
        if id in x: raise ValueError(f"{path}: duplicate {id}")
        x[id]=(sha,body)
    return x,s
def main():
    m=json.loads(MANIFEST.read_text(encoding="utf8"))
    traces={x["id"]:x for x in m["all_rule_traces"]}
    assert len(traces)==28
    got={k:read(v) for k,v in m["front_doors"].items()}
    for domain,(rules,text) in got.items():
        expected=set(m["shared_ids"]+m["local_ids"][domain])
        assert set(rules)==expected,(domain,"missing",sorted(expected-set(rules)),"extra",sorted(set(rules)-expected))
        for id,(sha,body) in rules.items():
            t=traces[id]
            assert sha==t["source_sha"],(domain,id,"source sha")
            for key in ("owner","trigger","action","falsifier"):
                assert t[key] in body,(domain,id,key)
        for s in ("PENDING_GUIDE_INTEGRATION","FINDINGS","INTERPRETATION","HQ ACTION","SOURCE"):
            assert s in text,(domain,s)
    for id in m["shared_ids"]:
        v=[got[k][0][id] for k in ("PRE_MAIN","PYAT","SOROK")]
        assert v[0]==v[1]==v[2],(id,"shared version/text drift")
    assert len(m["shared_ids"])==18
    p=got["PYAT"][1]
    for term in ("1,890","ALL_OF","ANY_OF","MODE_UNSELECTED","N11","N12","HQD115","COMPARE_ONLY"):
        assert term in p,("PYAT",term)
    s=got["SOROK"][1]
    for term in ("Rule T","NO_CHANGE","ALL_OF","ANY_OF","MODE_UNSELECTED","Gate4","Gate5","38 versioned seam","NOT_ISSUED"):
        assert term in s,("SOROK",term)
    print("PASS 28/28 ledger; shared 18 exact copies/source-pinned; domain local + protected negative markers")
if __name__=="__main__":
    try: main()
    except Exception as e:print("FAIL",repr(e),file=sys.stderr);sys.exit(1)
