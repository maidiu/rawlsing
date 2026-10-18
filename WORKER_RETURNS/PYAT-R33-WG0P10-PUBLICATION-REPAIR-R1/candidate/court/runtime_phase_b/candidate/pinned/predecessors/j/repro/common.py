from pathlib import Path
from dataclasses import replace,asdict
import json,hashlib,sys
import wg0p2_workload as w
R=Path(__file__).resolve().parents[1]
O=json.loads((R/'01_FROZEN_ORACLE_AND_PINNED_OWNERS.json').read_text())
def builder(items=None):
 b=w.WorkloadBuilder()
 for i in (w.independent_oracle_items() if items is None else items): assert b.add_item(i)=='OK'
 return b
def plan(items=None,ops=None,releases=None):
 items=w.independent_oracle_items() if items is None else items
 b=builder(items); freeze=b.freeze()
 return w.build_executable_plan(b.enumerate() if ops is None else ops,w.build_all_releases() if releases is None else releases,freeze_hash=freeze,items_by_id={i.item_id:i for i in items})
def execute(p):
 runner,rs=w.run_plan(p,w.make_executor(p));return runner,rs,w.consumer_effects(p,rs)
def values(e):
 return {k:[{'denominator':x['denominator'],'typed_state':x['typed_state'],'cells':x['cells']} for x in v] for k,v in e.items()}
def dump(name,obj): (R/'observations'/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
