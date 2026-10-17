"""Independent pre-WP1 scientific reference implementation; NOT WP1 or source authority."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

FROZEN=Path(__file__).with_name("01_PHASE_A_FROZEN_ORACLE.json")
class ScienceRefusal(ValueError):
    def __init__(self,code): self.code=code;super().__init__(code)
def load(): return json.loads(FROZEN.read_text())
def fraction(n,d):
    if d==0:raise ScienceRefusal("UNSUPPORTED_NO_DENOMINATOR")
    return Fraction(n,d)
def directional(table,condition,outcome):
    if condition not in ("X1","X0","Y1","Y0") or outcome not in ("X1","X0","Y1","Y0") or condition[0]==outcome[0]:
        raise ScienceRefusal("INVALID_CONDITIONAL")
    rows={("X1","Y1"):table["X1_Y1"],("X1","Y0"):table["X1_Y0"],("X0","Y1"):table["X0_Y1"],("X0","Y0"):table["X0_Y0"]}
    if any(type(v)is not int or v<0 for v in rows.values()):raise ScienceRefusal("BAD_CELL")
    n=sum(v for pair,v in rows.items() if condition in pair and outcome in pair)
    d=sum(v for pair,v in rows.items() if condition in pair)
    return fraction(n,d)
def support(positive,negative,missing=0,suppressed=False):
    if suppressed:return ("SUPPRESSED",None)
    if any(type(v)is not int or v<0 for v in (positive,negative,missing)):raise ScienceRefusal("BAD_SUPPORT_COUNTS")
    t=positive+negative+missing
    if t==0:return ("UNSUPPORTED",None)
    if missing:return ("PARTIAL_IDENTIFICATION",(fraction(positive,t),fraction(positive+missing,t)))
    if positive==0:return ("OBSERVED_ZERO",Fraction(0,1))
    return ("COMPLETE",fraction(positive,t))
def separated_source(a,b,kind):
    if a["source_family"]==b["source_family"] and a["release"]==b["release"]:raise ScienceRefusal("DUPLICATE_UNIVERSE")
    if kind!="NONPOOLED_CONTEXTUAL_COPRESENCE_ONLY":raise ScienceRefusal("CROSS_SURVEY_POOLING")
    return {"kind":kind,"source_ids":(a["source_family"],b["source_family"]),
            "respondent_matching":False,"combined_denominator":None,"joint_distribution":None}
def actions(w,location="DISTRICT_WEST",policy_present=True):
    if not policy_present:raise ScienceRefusal("NO_QUALIFIED_WORLD_RULE")
    if w["eligible_location"]!=location:return ("remain_home",)
    if w["route_operational"] and w["capacity"]>0:return ("remain_home","reach_clinic")
    return ("remain_home",)
def compare_worlds(a,b):
    aa,bb=actions(a),actions(b)
    return {"substantive_effect":aa!=bb,"A":aa,"B":bb,
            "changed_action_set":tuple(sorted(set(aa).symmetric_difference(bb)))}
def publication_asof(*,as_of,observed,release,world_time,epoch,required_epoch):
    if epoch!=required_epoch:raise ScienceRefusal("STALE_EPOCH")
    if as_of<release:raise ScienceRefusal("SOURCE_NOT_YET_PUBLISHED")
    if world_time>as_of:raise ScienceRefusal("FUTURE_SELECTED_WORLD")
    if observed>world_time:raise ScienceRefusal("FUTURE_OBSERVATION")
    return True
def authority_gate(source,*,caller_admit=False,model_requested=False,person_requested=False):
    if caller_admit:raise ScienceRefusal("CALLER_ADMIT_FORGERY")
    if source.get("issuer")!="SOURCEFREE_UNISSUED":raise ScienceRefusal("ISSUER_FORGERY")
    if source.get("origin")!="INDEPENDENT_SYNTHETIC_TEST_ONLY":raise ScienceRefusal("SOURCE_IDENTITY_FORGERY")
    if model_requested or person_requested:raise ScienceRefusal("ACTOR_OR_MODEL_PROMOTION")
    return "TEST_ONLY_NOT_ISSUED"
def hash_obj(v):return sha256(json.dumps(v,sort_keys=True,separators=(",",":")).encode()).hexdigest()
