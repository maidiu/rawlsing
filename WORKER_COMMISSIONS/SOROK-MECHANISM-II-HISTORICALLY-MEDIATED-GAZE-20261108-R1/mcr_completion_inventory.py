#!/usr/bin/env python3
"""MCR-C source-native no-drop enumerator for the whole original MII mission.

Two independent checks: derive exactly 10 E stages + 44 00E cases from
immutable original #792 Git source and compare with amended MCR contract IDs.
No executed code, user-psychology science, or reviewer authority claimed.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

ORIGINAL="094937d3187ed3c2e215fe2c1f7c1c84f50d9006"
PATH="WORKER_COMMISSIONS/SOROK-MECHANISM-II-HISTORICALLY-MEDIATED-GAZE-20261108-R1/00_COPY_PASTE_LAUNCH.md"
BEGIN="MCR_COMPLETION_CONTRACT_BEGIN"
END="MCR_COMPLETION_CONTRACT_END"

def source():
    x=subprocess.run(["git","show",ORIGINAL+":"+PATH],capture_output=True,text=True,check=True)
    return x.stdout

def original_ids(text):
    stages=["MII-E%02d"%int(i) for i in re.findall(r"(?m)^\*\*E([0-9]{1,2})\.",text)]
    cases=["MII-"+i for i in re.findall(r"(?m)^\*\*([OPGMNT][0-9]{2}):\*\*",text)]
    assert stages == ["MII-E%02d"%i for i in range(1,11)], ("E_STAGES_CHANGED",stages)
    expected_cases=([f"MII-{x}{i:02d}" for x,n in [("O",6),("P",9),("G",8),("M",6),("N",10),("T",5)] for i in range(1,n+1)])
    assert cases == expected_cases, ("ORIGINAL_44_CHANGED",cases)
    return stages+cases

def contract_records(text):
    assert text.count(BEGIN)==1 and text.count(END)==1, "MCR_CONTRACT_MARKERS_MISSING"
    block=text.split(BEGIN,1)[1].split(END,1)[0]
    scope=None
    ids=[]
    for line in block.splitlines():
        if line.startswith("MCR_SCOPE: "):
            assert scope is None, "DUPLICATE_SCOPE"
            scope=json.loads(line.split(": ",1)[1])
        if line.startswith("MCR_OBLIGATION: "):
            ids.append(json.loads(line.split(": ",1)[1])["id"])
    return scope,ids

def check():
    src=source()
    got=Path(PATH).read_text(encoding="utf-8")
    expected=original_ids(src)
    scope,ids=contract_records(got)
    assert scope and scope["expected_count"]==54, "SCOPE_NOT_54"
    assert len(ids)==54 and len(set(ids))==54, "OBLIGATION_DUPLICATE_OR_DROP"
    assert set(ids)==set(expected), ("MCR_NO_DROP_SET_MISMATCH",sorted(set(expected)-set(ids)),sorted(set(ids)-set(expected)))
    anchor="## APPENDIX: COMPLETE SOURCE-BANKED 00E ARCHITECTURE"
    actual=got[got.index(anchor):got.rfind("\n"+"\x60"*3)]
    assert actual==src[src.index(anchor):], "HISTORIC_00E_CONTENT_MUTATED"
    print(json.dumps({"result":"PASS","expected":54,"actual":len(ids),"historical_00e_exact":True,"source":ORIGINAL},sort_keys=True))

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("operation",choices=("enumerate","verify"))
    args=parser.parse_args()
    if args.operation=="enumerate":
        print("\n".join(original_ids(source())))
    else:
        check()

if __name__=="__main__":
    main()
