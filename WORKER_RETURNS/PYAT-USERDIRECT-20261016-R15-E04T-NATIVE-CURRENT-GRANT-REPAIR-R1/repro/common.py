from pathlib import Path
from copy import deepcopy
from collections import Counter
import json,hashlib
from product.service import GenericSelectedWorldService
from product.empirical import GenericProgressiveProvider,build_source
from product.world import SelectedSnapshot
from product.nonparent import consume
from product.scenario import evaluate
from rawlsing_next.pre553_empirical_objects import semantic_hash
R=Path(__file__).resolve().parents[1];RT=R/'runtime_root';C=RT/'candidate';S=C/'runtime_root/source'
O=json.loads((R/'E04I_ORIGINAL_FROZEN_ORACLE.json').read_text())
# Literal original E04I event strata, preserved in its separately committed repro.
STRATA={'111':(6,2),'110':(4,4),'101':(5,3),'100':(3,5),'011':(4,2),'010':(2,4),'001':(3,3),'000':(2,6)}
def independent_rows():return [dict(zip('ABC',map(int,key)),Y=y) for key,(yes,no) in STRATA.items() for y,n in ((1,yes),(0,no)) for _ in range(n)]
def direct(data,target,conditions):
 rows=[r for r in data if all(r[q]==v for q,v in conditions)];return {'denominator':len(rows),'cells':dict(Counter(str(r[target]) for r in rows))}
def geometry(step):return {'denominator':step['denominator'],'cells':{c['cell']:c['raw_numerator_support'] for c in step['cells']}}
PROPOSALS=[{'scenario_id':'independent-institution','route':'institutional'},{'scenario_id':'independent-civil','route':'civil'}]
def full(**options):
 s=GenericSelectedWorldService(**options);snap=s.select();a=consume(s,snap);b=evaluate(s,snap,PROPOSALS);return s,snap,a,b
def dump(name,value):(R/'observations'/name).write_text(json.dumps(value,indent=2,default=str)+'\n')
