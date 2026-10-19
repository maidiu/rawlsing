"""Frozen native producer-to-original-consumer edges; no asserted sidecar joins."""
from copy import deepcopy
import json
import pytest
import objective_world as w
from readthrough import ReadThroughError


def routes(view):return view['native_consumer']['material']['structural_routes']
def balances(view):return [s['source_balance_count'] for s in view['native_consumer']['material']['source_balance_reads']]

def test_ff_context_reaches_readonly_consumer():
    out=w.context_read_or_refusal()
    assert out['state']=='RETAINED_CONTEXT_VALUES_READ',out
    rows=out['relation']['conditional_count_profile']
    cells=[c for r in rows for c in r['target_counts']]
    assert len(cells)==36
    assert sum(c['joint_support_count'] for c in cells)==19210
    assert sum(c['joint_support_count']==0 for c in cells)==23
    dk=next(r for r in rows if r['condition_state']=={'typed_response_state':'DK'})
    assert next(c['joint_support_count'] for c in dk['target_counts'] if c['target_state']=={'typed_response_state':'DK'})==334
    assert out['published_B1'] is None
    assert out['resolved_producer_ref']['kind']=='F1'


def test_f6_native_partial_drives_world_evidence_view():
    out=w.ObjectiveWorld().evidence_view('W2')
    e=out['multifield_evidence']
    assert e['state']=='PARTIAL_IDENTIFICATION'
    assert e['evidence']['uncovered_target_mass']=='1/4'
    assert e['evidence']['supported_point'] is None
    assert e['display_class']=='BOUNDS_AND_UNKNOWN'
    assert out['matching_decision']['state']=='NO_AUTHORIZED_JOIN'
    assert routes(out['original_client'])['civil']['state']=='ELIGIBLE'


def test_temporal_revision_drives_original_consumer():
    world=w.ObjectiveWorld();early=world.read('HISTORICAL');late=world.read()
    assert early['structural_values']['training_fee']['value']==2
    assert late['structural_values']['training_fee']['value']==6
    assert routes(early)['training']['state']=='ELIGIBLE'
    assert routes(late)['training']['state']=='BLOCKED_BY_MODELED_RULE'
    assert balances(early)==balances(late)
    assert routes(early)['civil']==routes(late)['civil']


def test_selected_release_drives_original_consumer():
    world=w.ObjectiveWorld();world.native.stage_release('alternate')
    try:
        before=world.read();world.native.select_release('alternate');after=world.read()
        state='VALUES_READ'
    except ValueError as exc:
        state=str(exc);before=None;after=None
    assert state=='VALUES_READ',state
    assert balances(before)!=balances(after)
    assert before['structural_values']==after['structural_values']
    assert before['learned_binding']['release_ref']!=after['learned_binding']['release_ref']


def test_m4_resolution_drives_original_consumer():
    try:
        out=w.ObjectiveWorld().read();state=out['native_consumer']['material']['state']
    except ValueError as exc:state=str(exc)
    assert state=='OPTIONS_AND_SOURCE_SUPPORT_PRODUCED',state


def test_native_temporal_population_gate_drives_view():
    r=w.temporal_methods()
    assert r['cases']['comparable_probe']['state']=='COMPARABLE_PROBE_ONLY'
    assert r['cases']['population_change']['state']=='NONCOMPARABLE_POPULATION_OR_ESTIMAND'
    assert r['cases']['future_rule']['state']=='FUTURE_RULE_AT_HISTORICAL_AS_OF'
    assert r['measured_delta'] is None


def test_j04_position_is_exact_owner_bound():
    r=w.position_context()
    assert r['fact_ref']['content_hash']=='c823a816ce6f71431c99b1a466c7313f3766e5d1e7832fc36b6a31f15835dd02'
    assert r['state']=='EXACT_J04_RECONSTRUCTION_CONTEXT_READ'
    assert r['present_day_persistence'] is False


@pytest.mark.parametrize('family,key,value,route,expected',[
 ('formal','training_access',False,'training','BLOCKED_BY_MODELED_RULE'),
 ('civil_sanction','civil_sanction',True,'civil','BLOCKED_BY_MODELED_RULE'),
 ('civil_closed','civil_open',False,'civil','BLOCKED_BY_MODELED_RULE'),
 ('exit_only','exit_cost',8,'exit_constraint','RESOURCE_CONSTRAINED'),
 ('fee_only','training_fee',6,'training','BLOCKED_BY_MODELED_RULE'),
])
def test_independent_rule_families_reach_original_client(family,key,value,route,expected):
    world=w.ObjectiveWorld(family);early=world.read('HISTORICAL');late=world.read()
    assert late['structural_values'][key]['value']==value
    assert routes(late)[route]['state']==expected
    assert balances(early)==balances(late)
    for k in set(w.t35.E.STRUCTURAL_KEYS)-{key}:
        assert early['structural_values'][k]==late['structural_values'][k]


@pytest.mark.parametrize('case,expected,unknown',[
 ('W1','SUPPORTED_SYNTHESIS','0'),('W2','PARTIAL_IDENTIFICATION','1/4'),
 ('W3','PARTIAL_IDENTIFICATION','1/5'),('W4','SELF_CONDITIONING',None),
 ('W5','INCOMPLETE_NATIVE_JOINT_DOMAIN',None),('W6','INCOMPATIBLE_RESPONDENT',None),
 ('W7','PARTIAL_IDENTIFICATION','1/2'),('W8','CATEGORY_OUTSIDE_SUPPORT',None)])
def test_all_native_f6_cases_are_read_or_typed(case,expected,unknown):
    r=w.f6_evidence(case)
    assert r['state']==expected
    assert r['route_probability'] is None
    assert r['world_joint'] is None
    if unknown is not None:assert r['evidence']['uncovered_target_mass']==unknown
    if case=='W1':assert r['evidence']['supported_point']=={'formal':'5/8','informal':'3/8'}
    if case in ('W2','W3','W7'):assert r['evidence']['supported_point'] is None


def test_native_fields_preserve_households_subscriptions_and_independent_currentness():
    r=w.independent_fields();by={x['role']:x for x in r['values_read']}
    assert r['state']=='TWO_VALUES_READ_TEST_ONLY'
    assert by['GSS_RURAL_LIGHTING']['values']['denominator']==3288063
    assert by['NCA_NATIONAL_MOBILE_DATA']['values']['active_subscriptions']==23414527
    assert by['GSS_RURAL_LIGHTING']['native_unit']=='RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING'
    assert by['NCA_NATIONAL_MOBILE_DATA']['native_unit']=='ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS'
    historical=w.independent_fields(as_of='2022-03-01')
    assert [x['role'] for x in historical['values_read']]==['GSS_RURAL_LIGHTING']
    revoked=w.independent_fields(revoked='GSS_RURAL_LIGHTING')
    assert [x['role'] for x in revoked['values_read']]==['NCA_NATIONAL_MOBILE_DATA']


def test_source_family_collision_refuses_native_reader():
    rows=deepcopy(w.boot.bootstrap.fixture_rows());rows[1]['family']=rows[0]['family']
    with pytest.raises(w.n9c.TestOnlyReadError,match='NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'):
        w.independent_fields(rows=rows)


def test_purpose_checks_not_rewritten():
    r=w.purpose_refusals()
    assert set(r)=={'CONCEPTION_SCENARIO_PROPOSALS','N9_SELECTED_WORLD'}
    assert {v['reason'] for v in r.values()}=={'TEST_ONLY_CONSUMER_PERMISSION_UNAVAILABLE'}


def test_temporal_future_leakage_archival_and_selective_revocation():
    world=w.ObjectiveWorld();early=world.read('AS_OF');current=world.read()
    assert early['structural_values']['training_fee']['value']==2
    assert current['structural_values']['training_fee']['value']==6
    archived=world.historical_receipt(current['content_hash'])
    assert archived['fresh_use_authorized'] is False
    world.revoke('civil_sanction');after=world.read()
    assert routes(after)['civil']['state']=='UNAVAILABLE_AUTHORITY_OR_CLOCK'
    assert routes(after)['training']==routes(current)['training']
    assert balances(after)==balances(current)
    assert archived['receipt']==current


def test_missing_weight_and_real_use_never_promoted():
    r=w.f6_evidence('W2',request_overrides={'use':'REAL_USE'})
    assert r['state']=='PROHIBITED_MODEL_USE'
    assert r['evidence']['supported_point'] is None
    assert r['evidence']['real_use_authorized'] is False
    target,sources,policy=w.f6.OW.W1_full_coverage_disjoint()
    sources[0]['weight_ref']=None
    with pytest.raises(w.f6.F6M.SynthesisError,match='missing identity/semantic material'):
        w.f6.F6M.synthesize(target,sources,policy)


def test_temporal_scientific_replay_excludes_only_execution_timestamp():
    first=w.temporal_methods();second=w.temporal_methods()
    assert first==second
    assert first['cases']['comparable_probe']['report']['created_at']=='EXECUTION_TIMESTAMP_NOT_SCIENTIFIC_IDENTITY'
    assert first['cases']['future_rule']['state']=='FUTURE_RULE_AT_HISTORICAL_AS_OF'
