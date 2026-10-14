"""Prospective TEST_ONLY oracle and RED→GREEN court; old owner bytes unchanged."""
from collections import Counter
from dataclasses import replace
import hashlib,json,os
from pathlib import Path
import pytest
from rawlsing_next.tests import test_postastra_pv_v2k_independent as PV
K,C,P,G=PV.K,PV.C,PV.P,PV.G
STAGE=os.environ.get('V2R_STAGE','green')
if STAGE=='green':
    from rawlsing_next import pre553_hq297_v2r_role_query_binding_candidate as R
RET=Path(os.environ['V2R_RETURN'])


def fixture(root,held_bj=False):
    data=[PV.inputs(ns) for ns in PV.ORACLE['scopes']]
    original=tuple(w for d in data for w in d['records'])
    if held_bj:
        extras=tuple(replace(w,legacy=replace(w.legacy,state='HELD',hold_reason='TEST_ONLY_OPERATION_OWNER_NOT_ISSUED',query_ref=None,predicate_ref=None,discovery_authority_ref=None),
            original_operation_scope_ref=PV._ref('TEST_ONLY_HELD_OPERATION',w.legacy.slot)) for w in original[:3] if w.legacy.slot in ('B','DISCOVERY'))
        original=(*original,*extras)
    rows=[]
    for w in original:
        slot=w.legacy.slot
        profile=PV.ORACLE['expected_consumer_counts'].get(slot)
        if slot=='DISCOVERY':profile={'0':{'denominator':0,'targets':{'0':0,'1':0}},'1':{'denominator':1,'targets':{'0':0,'1':1}}}
        rows.append(dict(record=w.record(),binding=dict(native_order=[r.as_dict() for r in w.original.native_item_refs],
            risk_ref=data[0]['fx']['risk'].as_dict(),raw_denominator=1 if slot=='DISCOVERY' else 2,
            profile=profile if w.legacy.is_runnable else None)))
    payload=dict(schema='HQ297_V2R_INDEPENDENT_TEST_ONLY_REGISTER@1.0.0',origin='PROSPECTIVE_INDEPENDENT_TEST_ONLY',
        competence='TEST_ONLY_NOT_SOURCE_QUALIFIED',records=rows)
    # Freeze COMPLETE original and independently written raw denominator/profile before production.
    (root/'prospective_register.json').write_text(json.dumps(payload,indent=2))
    expected=K.FrozenOriginalExpected.from_records(original,input_origin=K.ORIGIN)
    prepared=[PV.prepare(root/str(i),d,d['records']) for i,d in enumerate(data)]
    plans=tuple(x[0] for x in prepared);calls=[x[1] for x in prepared]
    register=R.FrozenSourceNativeRegister.from_payload(payload) if STAGE=='green' else payload
    return original,expected,plans,calls,register


def changed_case(records,expected,plans,kind):
    old=records[0]
    if kind=='role':new=replace(old,legacy=replace(old.legacy,semantic_roles=('TARGET','CONDITIONER')))
    elif kind=='form':new=replace(old,original=replace(old.original,form='FOREIGN'),legacy=replace(old.legacy,form='FOREIGN'))
    elif kind=='unit':new=replace(old,original=replace(old.original,respondent_unit='HOUSEHOLD'))
    elif kind=='held':return tuple(w for w in records if w.legacy.is_runnable),plans
    elif kind=='subset':
        kw=dict(plans[0].p01_kwargs);s=kw['session'];doc=json.loads(kw['expected'].payload_json);doc['declarations']=[K.legacy_preimage(old.legacy)]
        kw['expected']=P.FrozenExpected.from_documentary_payload(doc)
        u=next(u for u in s.manifest.units if u.job_ref==old.legacy.query_ref)
        kw['session']=G.open_session(manifest=PV.BatchManifest((u,)),repository=s.repository,root=s.store.root.parent/'subset',source_sha256=s.source_sha256,executors=s.executors)
        return (old,),(K.OwnerScopePlan((old.key,),kw),)
    changed=tuple(new if w is old else w for w in records)
    pp=list(PV.remap(plans,old,new));kw=dict(pp[0].p01_kwargs);doc=json.loads(kw['expected'].payload_json)
    doc['declarations']=[K.legacy_preimage(new.legacy) if r['slot']=='PAIR' else r for r in doc['declarations']]
    kw['expected']=P.FrozenExpected.from_documentary_payload(doc);pp[0]=replace(pp[0],p01_kwargs=kw)
    return changed,tuple(pp)


@pytest.mark.parametrize('kind',['role','form','unit','held','subset'])
def test_precommitted_red_to_green(tmp_path,kind):
    records,expected,plans,calls,register=fixture(tmp_path)
    changed,selected=changed_case(records,expected,plans,kind)
    frozen=K.FrozenOriginalExpected.from_records(changed,input_origin=K.ORIGIN)
    if STAGE=='red':
        report=K.run_sourcefree(expected=frozen,selected_scopes=selected)
        (RET/'repro'/('RED_'+kind+'.json')).write_text(json.dumps(dict(candidate_ok=report['ok'],calls=[len(c) for c in calls],report=report),indent=2))
        assert not report['ok'], 'PV_RED_FALSE_POSITIVE_'+kind
    else:
        with pytest.raises(R.RoleBindingError):R.run_sourcefree(expected=frozen,selected_scopes=selected,register=register)
        assert calls==[[],[]]


def test_valid_six_consumers_and_held(tmp_path):
    records,expected,plans,calls,register=fixture(tmp_path)
    report=K.run_sourcefree(expected=expected,selected_scopes=plans) if STAGE=='red' else R.run_sourcefree(expected=expected,selected_scopes=plans,register=register)
    assert report['ok'] and len(report['links'])==6 and len(report['nonrunnable'])==2 and [len(c) for c in calls]==[3,3]
    if STAGE=='green':
        assert report['schema']==R.SCHEMA and report['original_qualification']=='CANNOT_QUALIFY_ORIGINAL'
        prior={l['original_expected_work_key']:PV.ExactRef(**l['consumer_ref']) for l in report['links']}
        replay=R.run_sourcefree(expected=expected,selected_scopes=plans,register=register,prior_consumer_refs=prior)
        assert replay['links']==report['links'] and [len(c) for c in calls]==[3,3]
        (RET/'repro/GREEN_positive.json').write_text(json.dumps(report,indent=2))
        (RET/'repro/frozen_prospective_register.json').write_bytes((tmp_path/'prospective_register.json').read_bytes())


if STAGE=='green':
    def test_complete_held_B_J_and_ordered_multiset(tmp_path):
        records,expected,plans,calls,register=fixture(tmp_path,held_bj=True)
        report=R.run_sourcefree(expected=expected,selected_scopes=plans,register=register)
        assert report['ok'] and len(report['links'])==6 and len(report['nonrunnable'])==4
        assert Counter(json.dumps(w.record(),sort_keys=True) for w in records if not w.legacy.is_runnable)==Counter(json.dumps(r,sort_keys=True) for r in report['nonrunnable'])
        (RET/'repro/GREEN_held_B_J.json').write_text(json.dumps(report,indent=2))

    @pytest.mark.parametrize('field',['original_U_ref','original_operation_scope_ref','independent_E_ref','independent_custody_ref'])
    def test_foreign_issuer_refs_never_replace_register(tmp_path,field):
        records,expected,plans,calls,register=fixture(tmp_path);old=records[0];new=replace(old,**{field:PV._ref('FOREIGN',field)})
        frozen=K.FrozenOriginalExpected.from_records(tuple(new if w is old else w for w in records),input_origin=K.ORIGIN)
        with pytest.raises(R.RoleBindingError,match='ORIGINAL_REGISTER_MULTISET_MISMATCH'):R.run_sourcefree(expected=frozen,selected_scopes=PV.remap(plans,old,new),register=register)
        assert calls==[[],[]]

    def test_no_register_no_original_qualification(tmp_path):
        _,expected,plans,calls,register=fixture(tmp_path)
        with pytest.raises(R.RoleBindingError,match='CANNOT_QUALIFY_ORIGINAL'):R.run_sourcefree(expected=expected,selected_scopes=plans,register=None)
        assert calls==[[],[]]

    def test_self_hash_cannot_issue_real_authority(tmp_path):
        _,expected,plans,calls,register=fixture(tmp_path)
        payload=json.loads(register.payload_json);payload['competence']='REAL_SOURCE_ISSUED'
        with pytest.raises(R.RoleBindingError,match='CANNOT_QUALIFY_ORIGINAL'):R.FrozenSourceNativeRegister.from_payload(payload)
        assert calls==[[],[]]

    @pytest.mark.parametrize('kind',['role','unit','form'])
    def test_coherently_refrozen_register_still_cannot_fake_query_roles(tmp_path,kind):
        records,expected,plans,calls,register=fixture(tmp_path)
        changed,selected=changed_case(records,expected,plans,kind)
        payload=json.loads(register.payload_json)
        for row in payload['records']:
            if row['record']['expected_work_key']==records[0].key:row['record']=changed[0].record()
        if kind=='role':
            refrozen=R.FrozenSourceNativeRegister.from_payload(payload)
            with pytest.raises(R.RoleBindingError,match='ROLE_QUERY_SEMANTIC_MISMATCH'):R.run_sourcefree(expected=K.FrozenOriginalExpected.from_records(changed,input_origin=K.ORIGIN),selected_scopes=selected,register=refrozen)
            assert calls==[[],[]]
        else:
            # A fully refrozen TEST_ONLY register can describe a different hypothetical
            # form/unit. It cannot become original-source competence, even if consistent.
            refrozen=R.FrozenSourceNativeRegister.from_payload(payload)
            report=R.run_sourcefree(expected=K.FrozenOriginalExpected.from_records(changed,input_origin=K.ORIGIN),selected_scopes=selected,register=refrozen)
            assert report['original_qualification']=='CANNOT_QUALIFY_ORIGINAL'

    @pytest.mark.parametrize('field',['risk_ref','native_order'])
    def test_false_query_binding_register_rejected(tmp_path,field):
        _,expected,plans,calls,register=fixture(tmp_path);raw=json.loads(register.payload_json)
        row=next(r for r in raw['records'] if r['record']['legacy']['slot']=='PAIR')
        row['binding'][field]=PV._ref('FOREIGN','risk').as_dict() if field=='risk_ref' else list(reversed(row['binding'][field]))
        forged=R.FrozenSourceNativeRegister.from_payload(raw)
        with pytest.raises(R.RoleBindingError):R.run_sourcefree(expected=expected,selected_scopes=plans,register=forged)
        assert calls==[[],[]]

    @pytest.mark.parametrize('field',['raw_denominator','profile'])
    def test_denominator_or_profile_witness_mismatch_is_not_green(tmp_path,field):
        _,expected,plans,calls,register=fixture(tmp_path);raw=json.loads(register.payload_json)
        row=next(r for r in raw['records'] if r['record']['legacy']['slot']=='PAIR')
        if field=='raw_denominator':row['binding'][field]=3
        else:row['binding'][field]['1']['denominator']=3
        forged=R.FrozenSourceNativeRegister.from_payload(raw)
        with pytest.raises(R.RoleBindingError,match='DENOMINATOR|CONSUMER_PROFILE'):R.run_sourcefree(expected=expected,selected_scopes=plans,register=forged)
        # Denominator verification occurs at actual saved-fact resolution, or at
        # consumer values-read; durable execution may already have committed.
        assert sum(len(c) for c in calls)>0

    def test_bad_register_digest_refuses(tmp_path):
        _,expected,plans,calls,register=fixture(tmp_path)
        with pytest.raises(R.RoleBindingError,match='REGISTER_DIGEST'):R.run_sourcefree(expected=expected,selected_scopes=plans,register=replace(register,payload_sha256='f'*64))
        assert calls==[[],[]]

    def test_lost_held_reason_or_consumer_refuses(tmp_path):
        records,expected,plans,calls,register=fixture(tmp_path);old=next(w for w in records if not w.legacy.is_runnable)
        new=replace(old,legacy=replace(old.legacy,hold_reason='CHANGED'))
        frozen=K.FrozenOriginalExpected.from_records(tuple(new if w is old else w for w in records),input_origin=K.ORIGIN)
        with pytest.raises(R.RoleBindingError,match='ORIGINAL_REGISTER_MULTISET'):R.run_sourcefree(expected=frozen,selected_scopes=plans,register=register)
        assert calls==[[],[]]


if STAGE=='green':
    @pytest.mark.parametrize('field',['empirical_universe_ref','routing_refs'])
    def test_refrozen_native_universe_routing_still_binds_c11(tmp_path,field):
        records,expected,plans,calls,register=fixture(tmp_path);old=records[0]
        v=PV._ref('FOREIGN','universe') if field=='empirical_universe_ref' else (PV._ref('FOREIGN','routing'),)
        new=replace(old,original=replace(old.original,**{field:v}))
        changed=tuple(new if w is old else w for w in records);raw=json.loads(register.payload_json)
        for row in raw['records']:
            if row['record']['expected_work_key']==old.key:row['record']=new.record()
        forged=R.FrozenSourceNativeRegister.from_payload(raw)
        with pytest.raises((R.RoleBindingError,K.IdentityError)):
            R.run_sourcefree(expected=K.FrozenOriginalExpected.from_records(changed,input_origin=K.ORIGIN),selected_scopes=PV.remap(plans,old,new),register=forged)
        assert calls==[[],[]]

    def test_sourcefree_gate_cannot_authorize_real_execution(tmp_path):
        _,expected,plans,calls,register=fixture(tmp_path);kw=dict(plans[0].p01_kwargs);kw['producer_permission_ceiling']=('REAL_EXECUTION',)
        with pytest.raises(K.IdentityError,match='SOURCEFREE_ONLY'):
            R.run_sourcefree(expected=expected,selected_scopes=(replace(plans[0],p01_kwargs=kw),plans[1]),register=register)
        assert calls==[[],[]]
