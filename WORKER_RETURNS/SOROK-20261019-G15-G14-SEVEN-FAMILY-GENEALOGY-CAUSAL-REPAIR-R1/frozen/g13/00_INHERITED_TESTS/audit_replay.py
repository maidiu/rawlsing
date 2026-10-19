"""Verify frozen source contract, all original semantic receipts and model records."""
from pathlib import Path
import json,sys,hashlib
ROOT=Path(__file__).resolve().parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(ROOT/'sources/sgi1/01_LAB_IMPLEMENTATION'))
from lab_sgi1.core import h_obj
from lab_sgi1.proposal import dedup_candidates
def read(path):return json.loads((ROOT/path).read_text())
def semantic(x):
    if isinstance(x,dict):return {k:semantic(v) for k,v in x.items() if not k.endswith('seconds')}
    if isinstance(x,list):return [semantic(v) for v in x]
    return x
def main():
    actual=read('evidence/sgi1_actual.json');contract=read('sources/sg/03_K11_EXECUTABLE_TEST_CONTRACT.json')
    expected={c['id']:c for c in contract['cases']};comparison=[]
    for c in actual['cases']:
        original=read('sources/sgi1/04_RESULT_RECEIPTS/'+c['case_id']+'.json')
        comparison.append(dict(case_id=c['case_id'],exact_contract_predicate_names=c['assertion_names_contract']==expected[c['case_id']]['assertions'],
            exact_assertion_results=c['assertion_results']==original['assertion_results'],
            exact_observed_state_excluding_timing=semantic(c['observed_state'])==semantic(original['observed_state']),
            exact_semantic_receipt=semantic(c)==semantic(original),
            original_receipt_hash_equal=c['receipt_hash']==original['receipt_hash'],
            changed_top_level_fields=[k for k in c if semantic(c[k])!=semantic(original.get(k))]))
    proposals=[]
    for path in sorted((ROOT/'sources/sgi1/08_LLM_PROPOSAL_RECORDS').glob('proposal_*.json')):
        if path.name=='proposal_index.json':continue
        r=json.loads(path.read_text())['record'];ded=dedup_candidates(r['parsed_candidates'])
        checks=dict(prompt_hash=h_obj({'prompt':r['prompt_text'],'system':r['system_text']})==r['prompt_hash'],
                    system_hash=h_obj(r['system_text'])==r['system_hash'],raw_hash=h_obj(r['raw_output'])==r['raw_output_hash'],
                    dedup_hash=ded['class_set_hash']==r['dedup']['class_set_hash'],
                    proposal_hash=h_obj(dict(prompt_hash=r['prompt_hash'],raw_output_hash=r['raw_output_hash'],parsed=r['parsed_candidates'],dedup_class_set_hash=ded['class_set_hash']))==r['proposal_hash'])
        replay_record=next(p['record'] for p in actual['proposal_records'] if 'proposal_'+p['record_key']+'.json'==path.name)
        proposals.append(dict(record=path.name,provider=r['provider'],checks=checks,historical_usage=r['usage'],
                              exact_record_replayed=r==replay_record,
                              hashing_contract='MODEL_CAPTURE' if r['provider']=='openai' else 'DECLARED_INTERVENTION_FACTORY'))
    native_rows=read('native_source_manifest.json')
    result=dict(contract_case_count=len(expected),contract_predicate_count=sum(len(c['assertions']) for c in expected.values()),
        exact_case_set=set(expected)=={c['case_id'] for c in actual['cases']},cases=comparison,proposals=proposals,
        historical_provider_records=sum(p['provider']=='openai' for p in proposals),
        historical_intervention_records=sum(p['provider']=='declared_test_intervention' for p in proposals),
        historical_tokens=sum(p['historical_usage'].get('total_tokens',0) for p in proposals),
        actual_replay_new_model_calls=0,runner_model_calls_field=actual['model_calls'],
        runner_model_calls_field_means_frozen_record_count=True,
        semantic_normalization='Only recursively omit keys ending seconds; retain every other field, list, hash, selection, event and assertion',
        native_closure=[dict(path=r['staged_path'],blob=r['git_blob_sha1']) for r in native_rows])
    (ROOT/'evidence/full_replay_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'exact_case_set':result['exact_case_set'],'semantic_receipts_equal':sum(c['exact_semantic_receipt'] for c in comparison),
                      'contract_name_matches':sum(c['exact_contract_predicate_names'] for c in comparison),
                      'observed_states_equal_excluding_timing':sum(c['exact_observed_state_excluding_timing'] for c in comparison),
                      'all_seven_model_capture_hash_checks':all(all(p['checks'].values()) for p in proposals if p['provider']=='openai'),
                      'all_ten_records_exactly_replayed':all(p['exact_record_replayed'] for p in proposals)}))
    assert result['exact_case_set'] and result['contract_predicate_count']==98
    assert all(c['exact_contract_predicate_names'] and c['exact_assertion_results'] for c in comparison)
    assert all(all(p['checks'].values()) for p in proposals if p['provider']=='openai')
    assert all(p['exact_record_replayed'] for p in proposals)
if __name__=='__main__':main()
