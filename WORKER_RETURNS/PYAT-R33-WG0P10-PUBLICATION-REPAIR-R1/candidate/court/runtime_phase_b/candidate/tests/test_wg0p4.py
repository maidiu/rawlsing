"""WG0P4 implementer hostiles. Prospective oracles are separately committed.

These additional cases are author regression evidence, never a WG0L verdict.
"""
import copy,json
from dataclasses import replace,asdict,FrozenInstanceError
import pytest
from common_v1 import *
from rawlsing_next.pre553_empirical_objects import EmpiricalFact

OP='OP-WG0P-ORD-01-MARGINAL'
@pytest.fixture(scope='module')
def original():
    p=plan();r,rs,e=execute(p);return p,r,rs,e

@pytest.mark.parametrize('status',['PRODUCED','HELD','INADMISSIBLE'])
@pytest.mark.parametrize('field,value',[('op_id','OP-FOREIGN'),('target','FOREIGN'),('conditioners',('FOREIGN',)),('item_ids',('FOREIGN',)),('op_class','FOREIGN'),('disposition_reason','FORGED')])
def test_equal_count_original_operation_substitutions(status,field,value):
    ops=builder().enumerate();old=next(o for o in ops if o.disposition.value==status)
    altered=[replace(o,**{field:value}) if o is old else o for o in ops]
    assert len(altered)==25
    with pytest.raises(w.FrontierError):w.validate_frontier(altered)
    with pytest.raises(w.FrontierError):w.validate_frontier_receipts(tuple(w.receipt_row(o) for o in altered),altered)

@pytest.mark.parametrize('field,value',[('options',('rotated','domain')),('missing_codes',()),('wave','W99'),('unit','household'),('source_id','FOREIGN'),('form_id','Q-OTHER'),('response_kind','MULTIPLE_RESPONSE'),('version','v2'),('grant','UNKNOWN'),('grant',None),('route_evidence','FOREIGN')])
def test_native_tuple_must_match_qualified_source_and_query(field,value):
    items=w.independent_oracle_items();items[0]=replace(items[0],**{field:value})
    with pytest.raises((w.IdentityError,w.FrontierError,TypeError)):
        execute(plan(items=items))

@pytest.mark.parametrize('part',['job_ref','release_refs','semantic_input_refs'])
def test_callback_checks_all_exact_unit_fields(original,part):
    p=original[0];u=p.units_by_op[OP]
    value=w._ref('EmpiricalQuerySpec@1.0.0','UNKNOWN') if part=='job_ref' else (p.releases['REL-A-W2'].release_ref,) if part=='release_refs' else ()
    with pytest.raises((w.IdentityError,KeyError)):w.make_executor(p)(replace(u,**{part:value}))

def test_external_oracle_root_is_not_recomputed_from_candidate(original):
    p=original[0]
    assert p.science_root==w.frontier_root('original25')
    assert p.expected_frontier_counts=={'PRODUCED':3,'HELD':16,'INADMISSIBLE':6}
    altered=copy.deepcopy(list(p.frontier_receipts));altered[0]['disposition_reason']='FORGED'
    with pytest.raises(w.FrontierError):w.consumer_effects(replace(p,frontier_receipts=tuple(altered)),original[2])

@pytest.mark.parametrize('seam',['store','read','snapshot','restore'])
def test_fact_aliases_do_not_modify_archived_bytes(seam):
    c=w.FactCustody();d={'cells':[{'n':2}],'denominator':6};c.store('ref',d)
    if seam=='store':d['cells'][0]['n']=999
    elif seam=='read':c.read('ref')['cells'][0]['n']=999
    elif seam=='snapshot':c.snapshot()['facts']['ref']['cells'][0]['n']=999
    else:
        snap=c.snapshot();other=w.FactCustody();other.restore(snap);snap['facts']['ref']['cells'][0]['n']=999;c=other
    assert c.read('ref')=={'cells':[{'n':2}],'denominator':6}

def test_collision_and_bad_restore_are_atomic():
    c=w.FactCustody();c.store('ref',{'n':2});before=c.snapshot()
    with pytest.raises(w.IdentityError):c.store('ref',{'n':999})
    bad=copy.deepcopy(before);bad['facts']['ref']['n']=999
    with pytest.raises(w.IdentityError):c.restore(bad)
    assert c.snapshot()==before

def test_native_payload_matches_actual_exact_empirical_fact(original):
    p,r,rs,e=original
    for receipt in rs:
        for f in receipt.result_refs:
            entry=p.fact_custody.read(f.key);native=w._validate_entry(f.key,entry,p)
            assert native.ref==f and native.condition_predicate_ref==entry['predicate_ref']
            assert entry['query_ref']==p.op_specs[entry['op_id']].query.ref.as_dict()
            assert entry['source_edition']==p.releases[p.op_specs[entry['op_id']].release_tag].source_edition
    assert r.summary().full_coverage and r.summary().populated_data_execution_claim is False

def test_self_rehashed_native_fact_and_receipt_do_not_become_issued_results(original):
    p,r,rs,e=original;s=p.op_specs[OP];entry=copy.deepcopy(e[OP][0]);proj=entry['native_fact']
    proj['semantic_fields']['raw_denominator_support']=999
    native=EmpiricalFact(**{k:v for k,v in proj.items() if k!='semantic_fields'},**proj['semantic_fields'])
    forged=w._plain(w._fact_entry(OP,s,native));w._validate_entry(native.ref.key,forged,p)
    # Local hashes are internally consistent, but no genuine issuer execution returned this fact.
    with pytest.raises(w.IdentityError,match='FACT_NOT_THE_NATIVE_ISSUED_RESULT'):p.fixture_owner.assert_fact_issued(native.ref.key,forged)
    old=next(r for r in rs if r.unit_ref==p.units_by_op[OP].unit_ref)
    new=replace(old,result_refs=(native.ref,));custody=w.FactCustody();custody.restore(p.fact_custody.snapshot());custody.store(native.ref.key,forged)
    altered=replace(p,fact_custody=custody)
    with pytest.raises(w.IdentityError,match='RECEIPT_NOT_ISSUED'):w.consumer_effects(altered,[new])

def test_fixture_owner_currentness_not_plan_self_issued_grant():
    p=plan();_,rs,e=execute(p);before=p.fact_custody.snapshot()
    p.fixture_owner.revoke('REL-A-W1');p.source_issuer_grant['grant']='GRANTED_FIXTURE'
    with pytest.raises(w.RevocationError):w.consumer_effects(p,rs)
    assert p.fact_custody.snapshot()==before

def test_unknown_fixture_owner_is_not_permission():
    releases=w.build_all_releases();d=dict(releases)
    with pytest.raises(w.IdentityError,match='FIXTURE_OWNER_REQUIRED'):plan(releases=d)

@pytest.fixture(scope='module')
def partial():
    p=plan();r,rs=w.run_plan(p,w.make_executor(p),max_units=1);assert len(rs)==1
    return p,w.create_checkpoint(p,rs)

@pytest.mark.parametrize('attack',['grant','fact','fact_hash','receipt_provenance','receipt_executor','receipt_result','receipt_attempt','source_edition','source_material','knowledge_clock','frontier_root','manifest','missing_payload','completed_unit'])
def test_cold_self_rehash_cannot_launder_any_bound_field(partial,attack):
    source,cp=partial;d=json.loads(cp.to_json())
    if attack=='grant':d['grant_state']='ISSUED_ORIGINAL_SOURCE_PERMISSION'
    elif attack=='fact':next(iter(d['fact_custody_snapshot']['facts'].values()))['denominator']=999
    elif attack=='fact_hash':
        k=next(iter(d['fact_custody_snapshot']['facts']));d['fact_custody_snapshot']['facts'][k]['denominator']=999;d['fact_custody_snapshot']['hashes'][k]=w.digest(d['fact_custody_snapshot']['facts'][k])
    elif attack=='receipt_provenance':d['prior_receipts'][0]['provenance_refs']=[]
    elif attack=='receipt_executor':d['prior_receipts'][0]['executor_ref']=w._ref('EXECUTOR','FORGED').as_dict()
    elif attack=='receipt_result':d['prior_receipts'][0]['result_refs']=[]
    elif attack=='receipt_attempt':d['prior_receipts'][0]['attempt_index']=2
    elif attack=='source_edition':d['source_editions']['REL-A-W1']='v999'
    elif attack=='source_material':d['source_material']='{}'
    elif attack=='knowledge_clock':d['owner_snapshot']['known_at']='1995-01-01'
    elif attack=='frontier_root':d['science_root']='0'*64
    elif attack=='manifest':d['manifest_hash']='0'*64
    elif attack=='missing_payload':d['fact_custody_snapshot']={'facts':{},'hashes':{}}
    else:d['completed_units']={}
    payload={k:v for k,v in d.items() if k not in ['signature','checkpoint_hash']};d['checkpoint_hash']=w.digest(payload)
    p=plan(releases=w.build_all_releases(fixture_owner=source.fixture_owner));before=p.fact_custody.snapshot()
    with pytest.raises((w.ColdRestartError,w.IdentityError)):
        loaded=w.ColdCheckpoint.from_json(json.dumps(d),fixture_owner=source.fixture_owner)
        w.restore_from_checkpoint(loaded,p)
    assert p.fact_custody.snapshot()==before and p.prior_receipts==()

def test_original_manifest_receipt_resume_and_legitimate_replay(partial):
    source,cp=partial;p=plan(releases=w.build_all_releases(fixture_owner=source.fixture_owner))
    native=w.receipt_from_json(cp.prior_receipts[0]);assert type(native).__name__=='UnitExecutionReceipt'
    result=w.resume_plan(p,w.ColdCheckpoint.from_json(cp.to_json(),fixture_owner=source.fixture_owner),w.make_executor(p))
    assert result['summary'].coverage_state=='FULL_MANIFEST_COVERAGE' and result['remaining_units']==2
    assert len(result['receipts'])==3 and native in result['receipts'] and all(x.manifest_hash==cp.manifest_hash for x in result['receipts'])
    assert set(result['consumer'])=={o['op_id'] for o in w.expected_rows('original25') if o['disposition']=='PRODUCED'}
    again=w.resume_plan(p,cp,w.make_executor(p));assert again['remaining_units']==0 and again['receipts']==result['receipts']

def test_cold_revoke_keeps_historical_bytes_but_denies_current_resume():
    p=plan();_,rs=w.run_plan(p,w.make_executor(p),max_units=1);cp=w.create_checkpoint(p,rs);snapshot=copy.deepcopy(cp.fact_custody_snapshot)
    p.fixture_owner.revoke('REL-A-W1')
    with pytest.raises(w.RevocationError):w.restore_from_checkpoint(cp,p)
    assert cp.fact_custody_snapshot==snapshot

def test_actual_subprocesses_restore_one_original_receipt_and_execute_only_two():
    a=json.loads((R/'observations/native_cold_crash.json').read_text());b=json.loads((R/'observations/native_cold_resume.json').read_text())
    assert a['pid']!=b['pid'] and a['exit']==23 and a['unit_count']==b['unit_count']==3 and a['manifest']==b['manifest']
    assert a['receipts'][0] in b['receipts'] and b['remaining_executed']==2 and b['summary']['coverage_state']=='FULL_MANIFEST_COVERAGE'
    assert sum(c['function']=='execute_empirical_query' for c in a['actual_calls'])==1
    assert sum(c['function']=='execute_empirical_query' for c in b['actual_calls'])==2

def test_conditional_uses_ordinary_chain_with_same_person_and_complete_second_frontier():
    p=plan(joint=True);r,rs,e=execute(p);op='OP-WG0P4-JOINT-RT-GIVEN-WG0P4-JOINT-ORD'
    assert len(p.frontier_receipts)==4 and sum(o['op_class']=='CONDITIONAL' and o['disposition']=='PRODUCED' for o in p.frontier_receipts)==1
    assert e[op][0]['denominator']==2 and {c['cell']:c['n'] for c in e[op][0]['cells']}=={'yes':1,'no':1}
    assert p.units_by_op[op].job_ref==p.op_specs[op].query.ref and len(rs)==3 and r.summary().full_coverage
    expected=[p.releases['REL-A-W1'].respondent_keys[x].as_dict() for x in ['R2','R3']]
    assert sorted(e[op][0]['native_fact']['semantic_fields']['denominator_member_refs'],key=lambda x:x['object_id'])==sorted(expected,key=lambda x:x['object_id'])
    missing=[o for o in builder(w.conditional_items(),True).enumerate() if o.op_id!=op]
    with pytest.raises(w.FrontierError):w.validate_frontier(missing)

def test_conditional_joint_grant_cannot_authorize_cross_wave_or_household():
    b=w.WorkloadBuilder();bad=w.joint_risk_authority();bad['members']=['H1','H2']
    with pytest.raises(w.IdentityError):b.add_joint_risk_authority(bad)
    for field,value in [('wave','W2'),('unit','household'),('source_id','FOREIGN')]:
        items=w.conditional_items();items[0]=replace(items[0],**{field:value})
        with pytest.raises(w.IdentityError):plan(items=items,joint=True)

def test_supported_zero_distinct_from_zero_risk_and_unknown(original):
    zero=next(x for x in original[3][OP][0]['cells'] if x['cell']=='9')
    assert zero['n']==0 and zero['state']=='OBSERVED_ZERO_IN_SUPPORTED_RISK_SET' and original[3][OP][0]['denominator']==6
    rel=original[0].releases['REL-A-W1'];pred=w._branch_predicate_for(rel,(),tag='empty',risk_name='R_ORD');q=w._query_for(rel,pred,(('Q-ORD-A',('0','1','2','3','9')),),risk='R_ORD',tag='empty')
    out=w.execute_empirical_query(repository=rel.repo,query=q,predicate=pred,authority_registry=w._registry_for(rel),release_refs=(rel.release_ref,))
    assert out.facts[0].typed_state=='ZERO_SUPPORT' and out.facts[0].raw_denominator_support==0
    with pytest.raises(KeyError):w.make_executor(original[0])(replace(original[0].units_by_op[OP],job_ref=w._ref('EmpiricalQuerySpec@1.0.0','UNKNOWN')))

@pytest.mark.parametrize('attack',['grant','missing_payload','receipt_provenance','source_leaf','revoked_owner','knowledge_clock'])
def test_new_process_rejects_cold_forgeries_before_any_native_execution(partial,attack):
    import os,pathlib,shutil,subprocess,sys
    source,cp=partial;folder=R/'runtime'/('attack-'+w.secrets.token_hex(8));folder.mkdir()
    ownerdir=folder/'owner';shutil.copytree(source.fixture_owner.directory,ownerdir)
    d=json.loads(cp.to_json())
    if attack=='grant':d['grant_state']='REAL_SOURCE_SIGNED_PERMISSION'
    if attack=='missing_payload':d['fact_custody_snapshot']={'facts':{},'hashes':{}}
    if attack=='receipt_provenance':d['prior_receipts'][0]['provenance_refs']=[]
    if attack=='knowledge_clock':d['owner_snapshot']['known_at']='1995-01-01'
    if attack=='revoked_owner':w.FixtureOwner(ownerdir).revoke('REL-A-W1')
    d['checkpoint_hash']=w.digest({k:v for k,v in d.items() if k not in ['signature','checkpoint_hash']})
    path=folder/'checkpoint.json';path.write_text(json.dumps(d))
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(R/'repro'))
    child=subprocess.run([sys.executable,str(R/'repro/cold_attack_worker.py'),str(ownerdir),str(path),attack],capture_output=True,text=True,env=env)
    assert child.returncode==0,child.stderr
    out=json.loads(child.stdout);assert out['accepted'] is False and out['actual_owner_calls']==[]
    dump('fresh_process_attack_'+attack+'.json',out)

def test_self_rehashed_plan_contract_is_not_independent_compiler_authority(original):
    p=original[0];contract=json.loads(p.contract);contract['bindings'][OP]['query']['typed_state']='FORGED'
    forged=replace(p,contract=w.canonical(contract))
    with pytest.raises(w.IdentityError,match='PLAN_NOT_REGISTERED_BY_QUALIFIED_COMPILER'):
        w.consumer_effects(forged,original[2])
