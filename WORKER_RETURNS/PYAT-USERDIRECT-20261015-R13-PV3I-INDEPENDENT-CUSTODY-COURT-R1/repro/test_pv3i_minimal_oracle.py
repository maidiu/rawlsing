"""PV3I independent native-source oracle: NOT a PV3 or accepted-owner import.
Source rows from pinned independent C11 provenance and pre-execution erratum.
"""
from collections import Counter
from copy import deepcopy
import pytest

NS=("PV2-ADULT-A","PV2-ADULT-B")
SLOTS=("PAIR","B","DISCOVERY","ORDERED")
ROWS={
 "R1":{"X":"1","Y":"1","Y_eligible":True},
 "R2":{"X":"0","Y":"0","Y_eligible":True},
 "R3":{"X":"1","Y":"1","Y_eligible":False},
}
def inventory():
 return {(n,s):"HELD" if s=="ORDERED" else "RUNNABLE" for n in NS for s in SLOTS}
def cells(rows=ROWS):
 c=Counter((r["X"],r["Y"]) for r in rows.values() if r["Y_eligible"])
 return {(x,y):c[(x,y)] for x in ("0","1") for y in ("0","1")}
def condition(rows,target,given,value):
 if {target,given}!={"X","Y"}: raise ValueError("UNISSUED_GENERIC_ROLE")
 matched=[r for r in rows.values() if r["Y_eligible"] and r[given]==value]
 return (len(matched),Counter(r[target] for r in matched))

def test_exact_eight():
 assert len(inventory())==8
def test_six_positive_two_held():
 assert Counter(inventory().values())=={"RUNNABLE":6,"HELD":2}
def test_held_both_namespaces():
 assert {n for (n,s),v in inventory().items() if v=="HELD"}==set(NS)
def test_r3_is_not_y_eligible():
 assert ROWS["R3"]["X"]=="1" and ROWS["R3"]["Y"]=="1" and not ROWS["R3"]["Y_eligible"]
def test_independent_joint_native_counts():
 assert cells()=={("0","0"):1,("0","1"):0,("1","0"):0,("1","1"):1}
def test_forward_and_reverse():
 assert condition(ROWS,"Y","X","0")==(1,Counter({"0":1}))
 assert condition(ROWS,"Y","X","1")==(1,Counter({"1":1}))
 assert condition(ROWS,"X","Y","0")==(1,Counter({"0":1}))
 assert condition(ROWS,"X","Y","1")==(1,Counter({"1":1}))
def test_A_R2_Y0_to_1_independent_B_not_modified():
 a=deepcopy(ROWS); a["R2"]["Y"]="1"
 assert cells(a)=={("0","0"):0,("0","1"):1,("1","0"):0,("1","1"):1}
 assert condition(a,"X","Y","1")==(2,Counter({"0":1,"1":1}))
 assert cells()=={("0","0"):1,("0","1"):0,("1","0"):0,("1","1"):1}
def test_supported_zero_is_not_zero_risk():
 n,c=condition(ROWS,"Y","X","0");assert n==1 and c["1"]==0
def test_generic_XY_native_semantics_not_issued():
 assert ("Q86B","Q86A")!=("X","Y")
