"""Independent exact-source, status, source-fault and terrain audit; no repairs."""
from pathlib import Path
import hashlib,json,subprocess,xml.etree.ElementTree as ET,collections,sys
ROOT=Path(__file__).resolve().parent
REPO=ROOT.parents[1]
def load(p):return json.loads(p.read_text())
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def main():
    rows=load(ROOT/'source_custody.json')
    for row in rows:
        data=(ROOT/row['local']).read_bytes()
        assert blob(data)==row['blob'] and hashlib.sha256(data).hexdigest()==row['sha256']
        assert git('rev-parse',row['commit']+':'+row['path']).decode().strip()==row['blob']
    original=load(ROOT/'sources/g15/frozen/source_manifest.json')+load(ROOT/'sources/g15/frozen/shared_manifest.json')
    for row in original:
        p=ROOT/'sources/g15'/row['staged'];data=p.read_bytes()
        assert blob(data)==row['blob_sha1'] and sha(p)==row['sha256']
        assert blob(git('show',row['commit']+':'+row['path']))==row['blob_sha1']
    prior=load(ROOT/'sources/g14/custody/module_preimages_and_imports.json')
    for row in prior['original_manifest_preimages']:
        assert blob(git('show',row['commit']+':'+row['path']))==row['blob_sha1']
    imported=load(ROOT/'execution/reproduced_g15/baseline/g14_observations.json')['imports']
    for row in prior['modules']:
        match=next(x for x in imported if x['module_file'].endswith('/'+row['module']))
        assert match['git_blob_sha1']==row['target_blob_sha1']
    assert len(prior['modules'])==14 and len(prior['original_manifest_preimages'])==104
    # Exact pristine candidate restored after all faults; every local copied test unchanged.
    for p in (ROOT/'sources/g15/candidate').rglob('*'):
        if p.is_file():assert p.read_bytes()==(ROOT/'sandbox/candidate'/p.relative_to(ROOT/'sources/g15/candidate')).read_bytes()
    replica=ROOT/'runs/replica/WORKER_RETURNS/SOROK-20261019-G15-G14-SEVEN-FAMILY-GENEALOGY-CAUSAL-REPAIR-R1'
    test_rows=[]
    for epoch in ['baseline','candidate']:
        for p in (replica/'runs'/epoch/'reproduction').rglob('test*.py'):
            rel=p.relative_to(replica/'runs'/epoch/'reproduction');src=ROOT/'sources/g15/frozen/g13'/rel
            assert p.read_bytes()==src.read_bytes();test_rows.append(dict(epoch=epoch,path=str(rel),sha256=sha(p)))
        assert (replica/'runs'/epoch/'test_g14_science.py').read_bytes()==(ROOT/'sources/g14/test_g14_science.py').read_bytes()
    counts={}
    for epoch,expected in [('baseline',{'PASS':164,'RED':17}),('candidate',{'PASS':108,'RED':73})]:
        j=load(ROOT/'execution/reproduced_g15'/epoch/'case_matrix.json')
        c=dict(collections.Counter(x['status'] for x in j['court_181']));assert c==expected
        g=dict(collections.Counter(x['status'] for x in j['g14_67']));assert g==({'PASS':40,'RED':27} if epoch=='baseline' else {'PASS':67})
        counts[epoch]=dict(inherited181=c,g14_67=g)
    adjud=load(ROOT/'02_COMPATIBILITY_56.json');assert adjud['count']==56 and all(not c['waived'] for c in adjud['cases'])
    assert load(ROOT/'03_ORIGINAL_17_REDS.json')['all_remain_RED']
    independent=load(ROOT/'execution/independent/results.json');c=dict(collections.Counter(x['status'] for x in independent['cases']));assert c=={'PASS':14,'RED':10}
    assert all((x['failure_message'] or '').startswith(('assert ','AssertionError')) for x in independent['cases'] if x['status']=='RED')
    # JUnit and result matrix agree at exact case identity and assertion outcome.
    xml=list(ET.parse(ROOT/'execution/independent/final_court.xml').iter('testcase'));assert len(xml)==24
    assert sum(x.find('failure') is not None for x in xml)==10 and all(x.find('error') is None and x.find('skipped') is None for x in xml)
    faults=load(ROOT/'execution/independent/fault_receipts.json');assert len(faults)==9
    for row in faults:
        assert row['positive']['exit']==row['restored']['exit']==0 and row['fault']['exit']==1
        assert row['before_sha256']==row['restore_sha256']
        assert sha(REPO/row['claim']['fault']['path'])==row['restore_sha256']
        assert len(row['fault']['cases'])==1 and row['fault']['cases'][0]['name']==row['claim']['positive_node'].split('::')[-1]
    imports=load(ROOT/'execution/independent/final_court_observations.json');assert imports['network_attempts']==[]
    for row in imports['imports']:
        p=ROOT/row['path'];assert sha(p)==row['sha256'] and blob(p.read_bytes())==row['blob_sha1']
    author_faults=load(ROOT/'execution/reproduced_g15/faults/receipts.json');assert len(author_faults)==13
    for row in author_faults:assert row['positive']['exit']==0 and row['fault']['exit']==1 and row['fault']['assertion_failure'] and row['source_before_sha256']==row['restored_sha256']
    assert load(ROOT/'execution/reproduced_g15/prospective/results.json')[0]['counts']['PASS']==75
    preserve=load(ROOT/'execution/reproduced_g15/preservation/results.json')[0];assert preserve['counts']==dict(PASS=25,RED=0,ERROR=0,SKIP=0)
    historic=load(ROOT/'execution/reproduced_g15/preservation/full_replay_audit_historical.json');assert all(c['exact_contract_predicate_names'] and c['exact_assertion_results'] and c['exact_observed_state_excluding_timing'] for c in historic['cases'])
    assert historic['historical_provider_records']==7 and historic['historical_intervention_records']==3 and historic['historical_tokens']==12183
    assert all(p['exact_record_replayed'] for p in historic['proposals'])
    a=load(ROOT/'execution/reproduced_g15/joined_positive.json');b=load(ROOT/'execution/reproduced_g15/joined_cold_replay.json')
    assert a['result']['causal_replay_record']==b['result']['causal_replay_record'] and b['complete_causal_record_equal']
    assert load(ROOT/'execution/shared_witness.json')['status']=='MECHANICAL_WITNESS_PASS_NOT_SEMANTIC_ADOPTION'
    assert len(load(ROOT/'execution/shared_witness.json')['claims'])==9
    assert git('rev-parse','HEAD').decode().strip()=='8fdced60b7162407b08d20247405cc39b8410fa2' or git('merge-base','8fdced60b7162407b08d20247405cc39b8410fa2','HEAD').decode().strip()=='8fdced60b7162407b08d20247405cc39b8410fa2'
    changed=git('diff','--name-only','8fdced60b7162407b08d20247405cc39b8410fa2','--').decode().splitlines()
    assert all(p.startswith(str(ROOT.relative_to(REPO))+'/') for p in changed)
    receipt=dict(status='INDEPENDENT_CUSTODY_AND_EVIDENCE_VERIFIED_NOT_ADOPTION',top_level_pinned_blobs=len(rows),nested_frozen_source_and_law_blobs=len(original),baseline_exact_G13_modules=14,original_native_manifest_preimages=104,pristine_candidate_restored=True,frozen_tests_unchanged=test_rows,actual_independent_imports=imports['imports'],counts=counts,independent24=c,independent_witnesses=9,author_witnesses_reexecuted=13,original17_preserved=True,new56_adjudicated=True,unavailable_handler_groups=9,whole_causal_cold_record_equal=True,historical_original_SGI1='25 PASS; 24 observed states and98 flags preserved; full receipts timing-limited',source_authority='SOURCEFREE_AND_FROZEN_ONLY',new_provider_calls=0)
    (ROOT/'custody_validation.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k not in {'frozen_tests_unchanged','actual_independent_imports'}},sort_keys=True))
if __name__=='__main__':main()
