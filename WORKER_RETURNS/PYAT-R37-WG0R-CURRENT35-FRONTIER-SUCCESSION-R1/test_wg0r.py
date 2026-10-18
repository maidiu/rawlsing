from dataclasses import replace
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import pytest
import repro_fixture as r
import account_current35 as accounting
from rawlsing_next.pre553_source_backed_c11_facade import SourceBackedC11FacadeError


@pytest.fixture(scope='module')
def output(): return r.run()


def test_enumeration_batch_native_parity_and_consumer(output):
    assert output['batch_summary']['completed_units']==3
    assert output['batch_summary']['full_coverage']
    assert output['resumed_new_executions']==0
    assert output['consumer_positive']['semantic_fields']['adjudication_outcome']=='RULE_SATISFIED'
    assert output['consumer_unknown']['semantic_fields']['adjudication_outcome']=='UNRESOLVED'
    facts={f['semantic_fields']['measure_kind']:f for f in output['i03_facts']}
    assert facts['RAW']['semantic_fields']['raw_denominator_support']==2
    assert facts['GOVERNED_WEIGHTED']['semantic_fields']['weighted_denominator_support_if_authorized']=={'$exact_fraction':[3,1]}
    assert all('sources/native/' in x['path'] for x in output['imports'].values())


def test_weight_absence_preserved_not_unit_default():
    result=r.run(missing_weight=True)
    weighted=next(f for f in result['i03_facts'] if f['semantic_fields']['measure_kind']=='GOVERNED_WEIGHTED')
    assert weighted['typed_state']=='UNAVAILABLE'
    assert weighted['semantic_fields']['weighted_denominator_support_if_authorized'] is None


@pytest.mark.parametrize('mutation',['duplicate','swap','omission'])
def test_pre_result_operation_antijoin(mutation):
    fx=r._fixture();frozen=r.binding(fx);requests=list(r.enumerate_requests(fx['catalog']))
    if mutation=='duplicate':requests.append(requests[0])
    if mutation=='omission':requests.pop()
    if mutation=='swap':requests[0]=replace(requests[0],predicate_ref=fx['x1'].ref)
    with pytest.raises(r.FrontierRefusal,match='FRONTIER_ANTI_JOIN'):
        r.reconcile(fx,requests,fx['catalog'].discovery_authorities,frozen)


@pytest.mark.parametrize('mutation',['route','subject','weight','source-version'])
def test_pre_result_authority_binding_substitution(mutation):
    fx=r._fixture();frozen=r.binding(fx);p=fx['projection']
    with pytest.raises((r.FrontierRefusal,SourceBackedC11FacadeError)):
        if mutation=='route':p=replace(p,routing=tuple(reversed(p.routing[:-1])))
        elif mutation=='subject':
            subjects=(replace(p.respondents[0],respondent_key='SUBSTITUTED'),*p.respondents[1:])
            p=replace(p,respondents=subjects)
        elif mutation=='weight':
            p=replace(p,weight_slots=(replace(p.weight_slots[0],weight_basis_id='SUBSTITUTED'),))
        else:p=replace(p,expected_source_sha256='1'*64)
        fx['projection']=p
        r.reconcile(fx,r.enumerate_requests(fx['catalog']),fx['catalog'].discovery_authorities,frozen)


def test_all35_expected_registry_antijoin_and_no_drop():
    rows,waves,_=accounting.load()
    assert len(rows)==len({x['question_implementation_id'] for x in rows})==18276
    assert len(waves)==35
    assert ('EVS','1999') in waves
    assert ('Asian Barometer','W6') not in waves
    assert {x['wave_uid'] for x in rows}=={w['wave_uid'] for w in waves.values()}


def test_no_drop_omission_duplicate_and_swap_falsifiers():
    rows,waves,_=accounting.load()
    expected={x['question_implementation_id']:x for x in rows}
    # Independent expected-work map rejects a same-count duplicated/swapped ID.
    for changed in [rows[:-1],rows[:-1]+[rows[0]],rows[:-1]+[{**rows[-1],'wave_uid':rows[0]['wave_uid']}]]:
        assert len(changed)!=len(expected) or len({x['question_implementation_id'] for x in changed})!=len(expected) or any(expected[x['question_implementation_id']]!=x for x in changed)


def test_native_source_custody():
    manifest=json.loads((r.ROOT/'evidence/source_manifest.json').read_text())
    for row in manifest:
        data=(r.ROOT/row['local_path']).read_bytes()
        assert hashlib.sha256(data).hexdigest()==row['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['blob_sha1']


def test_retained_disposition_pack_rejected_without_rewriting_authority():
    with pytest.raises(ValueError,match='DISPOSITION_PAYLOAD_MISMATCH'):
        accounting.decode_dispositions()
    rows,_,_=accounting.load()
    assert all(r['governed_use'] is None and r['hard_fail'] is None for r in rows)
    assert accounting.pack_receipt()['observed_bytes']==18387


def test_frozen_plan_custody():
    p=r.ROOT/'evidence/PRE_RESULT_COURT.json'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==(r.ROOT/'evidence/PRE_RESULT_COURT.sha256').read_text().split()[0]


def test_fresh_process_replay(output):
    proc=subprocess.run([sys.executable,'-B',str(r.ROOT/'repro_fixture.py')],
                        text=True,capture_output=True,check=True,cwd=r.ROOT)
    replay=json.loads(proc.stdout)['positive']
    assert replay==output
