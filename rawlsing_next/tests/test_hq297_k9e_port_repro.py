"""K9E isolated fixture-port probe; NOT SC0 schema/PE/N9 owner qualification."""
from copy import deepcopy
import pytest

# Two separately encoded source-free providers; physical order is nonsemantic.
A = dict(AH="AH:1", strata=["native:A","native:B"], roles=["authority","applicant","sponsor"], f2="requirement:prior", states=["ZERO","EMPTY","MISSING","UNDERPOWERED","NOT_ASKED"], n=60, yes=54, no=6, unit="RESPONDENT", clock=["2008","2010","2009","2008","2026"], direction="FORWARD", permission="TEST_ONLY", grade="FIXTURE", binding="location:1", release="pub:1", consumer="GENERIC", actor=None)
B_ROWS = [("actor",None),("consumer","GENERIC"),("release","pub:1"),("binding","location:1"),("grade","FIXTURE"),("permission","TEST_ONLY"),("direction","FORWARD"),("clock",["2008","2010","2009","2008","2026"]),("unit","RESPONDENT"),("no",6),("yes",54),("n",60),("states",["ZERO","EMPTY","MISSING","UNDERPOWERED","NOT_ASKED"]),("f2","requirement:prior"),("roles",["authority","applicant","sponsor"]),("strata",["native:A","native:B"]),("AH","AH:1")]
K9 = "SAME_MEANING NONPARENT REORDER LOSS GRADE REVERSE PERMISSION REFRESH".split()
K10 = "AH strata roles f2 actor roles no states states states unit direction roles grade clock clock binding binding release permission grade grade actor roles actor f2 consumer actor".split()
MUT = [None,["display:A","display:B"],["authority","applicant"],None,"EXPERIENCED",["authority"],0,["MISSING","EMPTY","MISSING","UNDERPOWERED","NOT_ASKED"],["ZERO","EMPTY","MISSING","EMPTY","NOT_ASKED"],["ZERO","EMPTY","MISSING","UNDERPOWERED","NO"],"HOUSEHOLD","REVERSE",["sponsor","applicant","authority"],"CERTAIN",["2008","2010","2010","2008","2026"],["2008","2010","2010","2008","2026"],"SOURCE_OBSERVATION","location:changed","pub:changed","DENIED_USE","NOT_COMPLETE","OBSERVED","PSYCHE",["authority"],"INFERRED_PERSON","felt_guilt","APPRENTICESHIP","WAKE_V3"]

def gate(v):
    if v["permission"] != "TEST_ONLY": return "DENIED_USE"
    if v["grade"] != "FIXTURE": return "NO_PROMOTION"
    if v["direction"] != "FORWARD": return "HELD_REVERSE"
    return "FIXTURE_ONLY_NO_ACTOR"

@pytest.mark.parametrize("case",K9,ids=[f"K9_{i+1:02d}" for i in range(8)])
def test_k9(case):
    a=deepcopy(A); b=dict(reversed(B_ROWS))
    if case in ("SAME_MEANING","REORDER"): assert a==b==dict(B_ROWS)
    elif case=="NONPARENT": assert gate(b)=="FIXTURE_ONLY_NO_ACTOR" and b["consumer"]=="GENERIC"
    elif case=="LOSS": b["roles"].pop(); assert b!=a
    elif case=="GRADE": b["grade"]="OBSERVED"; assert gate(b)=="NO_PROMOTION"
    elif case=="REVERSE": b["direction"]="REVERSE"; assert gate(b)=="HELD_REVERSE"
    elif case=="PERMISSION": b["permission"]="DENIED_USE"; assert gate(b)=="DENIED_USE"
    elif case=="REFRESH":
        b["binding"]="location:2"; assert b["release"]==a["release"]
        b["release"]="pub:2"; assert b["binding"]!=a["binding"]

@pytest.mark.parametrize("i",range(28),ids=[f"K10_{i+1:02d}" for i in range(28)])
def test_k10_conservation_only(i):
    a=deepcopy(A); b=deepcopy(A); b[K10[i]]=deepcopy(MUT[i]); assert b!=a
    assert a["yes"]==54 and a["no"]==6 and a["n"]==60
    if i==11: assert gate(b)=="HELD_REVERSE"
    if i==19: assert gate(b)=="DENIED_USE"
    if i==21: assert gate(b)=="NO_PROMOTION"
