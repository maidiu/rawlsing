from __future__ import annotations
import hashlib, json, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent; BASE=HERE.parent; REPO=BASE.parents[1]
sys.path[:0]=[str(REPO),str(HERE)]
from rawlsing_next.tests import test_pre553_empirical_query as native
from rawlsing_next.pre553_empirical_objects import canonical_json, exact_ref
from wide_fixture import build_source, build_queries
rows=json.loads((BASE/'evidence'/'wide_baseline.json').read_text())['rows']
source,_=build_source(); qa,preds,queries=build_queries(source)
m=[]
for row,q in zip(rows,queries):
    pred=next(p for p in preds if exact_ref(q.condition_predicate_ref,'condition')==p.ref)
    fact=native._run(source,qa,pred,q).facts[0]
    for k,v in {
      'fact_ref':json.loads(canonical_json(fact.ref)),
      'typed_state':fact.typed_state,
      'raw_numerator_support':fact.raw_numerator_support,
      'raw_denominator_support':fact.raw_denominator_support,
      'replay_ref':json.loads(canonical_json(fact.replay_ref)),
      'fact_sha256':hashlib.sha256(canonical_json(fact).encode()).hexdigest(),
    }.items():
        if row[k]!=v: m.append({'index':row['index'],'field':k})
out={'schema':'PYAT_P0_PARITY@1','scope':'64 respondents / 30 questions / 20 operations vs in-memory native oracle','compared':len(rows),'mismatches':m,'exact':not m}
(BASE/'evidence'/'parity_wide_oracle.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
