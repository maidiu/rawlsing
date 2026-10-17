"""Explicit WG0J common API to final candidate; original tests stay unchanged."""
from pathlib import Path
from dataclasses import replace,asdict
import json,hashlib,sys
from phase_b_support_v1 import w,R as REVIEWER,C,plan,builder,execute,stripped
R=REVIEWER/'observations/phase_b/inherited_v1'
(R/'observations').mkdir(parents=True,exist_ok=True)
O=json.loads((C/'pinned/predecessors/j/01_FROZEN_ORACLE_AND_PINNED_OWNERS.json').read_text())
def values(e):return stripped(e)
def dump(name,obj):(R/'observations'/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
