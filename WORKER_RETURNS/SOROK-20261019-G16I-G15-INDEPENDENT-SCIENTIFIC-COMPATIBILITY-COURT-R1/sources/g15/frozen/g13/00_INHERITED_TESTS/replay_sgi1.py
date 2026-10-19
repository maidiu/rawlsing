"""Execute original K11Run unchanged, using original frozen records, offline."""
from pathlib import Path
import sys, json, time, hashlib
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'sources/sgi1'
sys.dont_write_bytecode=True
sys.path.insert(0,str(SOURCE/'01_LAB_IMPLEMENTATION'))
network_attempts=[]
def offline(event,args):
    if event in {'socket.connect','socket.getaddrinfo','socket.__new__'}:
        network_attempts.append(event)
        raise RuntimeError('G12_NEW_NETWORK_OR_MODEL_CALL_FORBIDDEN')
sys.addaudithook(offline)
from lab_sgi1.k11_runner import K11Run
from lab_sgi1.core import h_obj

def execute():
    t=time.perf_counter()
    run=K11Run(str(SOURCE),model_enabled=False,reuse_records=True)
    assert run._load_persisted(), 'EXACT_FROZEN_RECORDS_MISSING_HOLD'
    # Recreate clean runner; its original acquire_records must load, not generate.
    run=K11Run(str(SOURCE),model_enabled=False,reuse_records=True)
    result=run.run_all()
    expected=json.loads((SOURCE/'05_MEASUREMENTS/suite_fingerprints.json').read_text())['fingerprints']
    comparisons={}
    for c in result['cases']:
        obs=c['observed_state']
        sel=obs.get('selection') or obs.get('selection_a') or obs.get('selection_discordant') or obs.get('selection_base')
        dad=obs.get('dad_event_hash') or obs.get('dad_hash_a')
        actual=h_obj(dict(assertions=c['assertion_results'],grade=c['terminal_grade'],selection=sel,dad=dad))
        comparisons[c['case_id']]={'actual':actual,'original':expected[c['case_id']]['fingerprint'],
                                  'equal':actual==expected[c['case_id']]['fingerprint']}
    imports=[]
    for name,module in sorted(sys.modules.items()):
        if name.startswith('lab_sgi1') and getattr(module,'__file__',None):
            p=Path(module.__file__);b=p.read_bytes()
            imports.append(dict(module=name,module_file=str(p.relative_to(ROOT)),
                                git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
    evidence=ROOT/'evidence';evidence.mkdir(exist_ok=True)
    (evidence/'sgi1_actual.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    summary=dict(n_cases=result['n_cases'],n_assertions=result['n_assertions'],
                 n_assertions_pass=result['n_assertions_pass'],cases_failed=result['cases_failed'],
                 comparison=comparisons,imports=imports,new_provider_calls=0,
                 network_attempts=network_attempts,wall_seconds=time.perf_counter()-t,
                 historical_usage_in_frozen_records_is_not_new_usage=True)
    (evidence/'sgi1_replay.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({k:v for k,v in summary.items() if k not in {'comparison','imports'}},indent=2))
    print('EXACT_FINGERPRINT_MATCHES',sum(x['equal'] for x in comparisons.values()))
    return result,summary

if __name__=='__main__': execute()
