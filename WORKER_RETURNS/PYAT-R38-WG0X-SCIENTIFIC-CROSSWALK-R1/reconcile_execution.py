"""Expected versus actual native receipts; does not trust echoed request lists."""
from collections import Counter
from pathlib import Path
import json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'native'))
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_carrier_execution import materialize_public_object


def reconcile(expected,receipt):
    wanted=Counter(tuple(x) for x in expected['expected_jobs'])
    units=receipt['manifest']['units'];receipts=receipt['batch_receipts']
    actual=[];unit_keys=[]
    facts=[materialize_public_object(x) for x in receipt['i03_facts']]
    discoveries=[materialize_public_object(x) for x in receipt['i05_receipts']]
    by_unit={exact_ref(x['unit_ref'],'unit').key:x for x in receipts}
    if len(by_unit)!=len(receipts):raise ValueError('DUPLICATE_EXECUTION_RECEIPT')
    for entry in units:
        u=entry['semantic_projection'];uk=exact_ref(entry['unit_ref'],'unit').key
        unit_keys.append(uk)
        jr=exact_ref(u['job_ref'],'job');pred=exact_ref(u['semantic_input_refs'][0],'predicate') if u['job_kind']=='QUERY' else None
        actual.append((u['job_kind'],jr.key,pred.key if pred else ''))
        r=by_unit.get(uk)
        if not r or r['state']!='COMPLETED' or not r['execution_performed']:raise ValueError('UNVISITED_OR_HELD_EXPECTED_UNIT')
        results={exact_ref(x,'result').key for x in r['result_refs']}
        products=facts if u['job_kind']=='QUERY' else discoveries
        linked=[f for f in products if jr.key in {d.key for d in f.dependency_refs} and (not pred or pred.key in {d.key for d in f.dependency_refs})]
        if not linked or {f.ref.key for f in linked}!=results:raise ValueError('RESULT_CUSTODY_OR_QUERY_PREDICATE_MISMATCH')
    if Counter(actual)!=wanted:raise ValueError('EXPECTED_ACTUAL_JOB_MULTISET_MISMATCH')
    if Counter(unit_keys)!=Counter(by_unit.keys()):raise ValueError('EXECUTION_RECEIPT_SET_MISMATCH')
    if receipt['consumer_positive']['semantic_fields']['discovery_result_receipt_refs']!=receipt['consumer_unknown']['semantic_fields']['discovery_result_receipt_refs']:raise ValueError('CONSUMER_DISAGREES_ON_SELECTED_DISCOVERY')
    for name in ['consumer_positive','consumer_unknown']:
        used={exact_ref(x,'selected_discovery').key for x in receipt[name]['semantic_fields']['discovery_result_receipt_refs']}
        if used!={d.ref.key for d in discoveries}:raise ValueError('CONSUMER_DISCOVERY_CUSTODY_MISMATCH')
    return dict(expected=sum(wanted.values()),actual=len(actual),executed=len(receipts),missing=[],unexpected=[],consumer_positive=receipt['consumer_positive']['semantic_fields']['adjudication_outcome'],consumer_held=receipt['consumer_unknown']['semantic_fields']['adjudication_outcome'],scope='TEST_ONLY_NAMED_FIXTURE__NOT_ORIGINAL35')

if __name__=='__main__':
    r=Path(__file__).resolve().parent;e=json.loads((r/'evidence/EXPERIMENT_EXPECTED.json').read_text());d=json.loads((r/'evidence/native_experiment.json').read_text())
    result={k:reconcile(e[k],d[k]) for k in ['positive','missing_weight']}
    (r/'evidence/expected_vs_actual_receipts.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True))
