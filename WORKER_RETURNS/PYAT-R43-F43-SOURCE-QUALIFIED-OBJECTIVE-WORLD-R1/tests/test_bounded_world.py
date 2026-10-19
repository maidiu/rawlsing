from copy import deepcopy
from fractions import Fraction as Q
import json
from pathlib import Path
import pytest
import bootstrap_f43 as boot
import bounded_methods as m
import objective_world as w

ORACLE = json.loads((boot.ROOT / '01_METHOD_ORACLE.json').read_text())


def native(case):
    key = next(k for k in w.f6.OW.WORLD_BUILDERS if k.split('_')[0] == case)
    t, sources, policy = w.f6.OW.WORLD_BUILDERS[key]()
    bundle = w.f6.F6M.synthesize(t, sources, policy)
    return bundle, w.f6.request(key)


@pytest.mark.parametrize('case', ['W1', 'W2', 'W3', 'W7'])
def test_native_f6_conditional_bounds(case):
    bundle, req = native(case)
    candidate = bundle['candidate']
    out = m.partial_conditional(candidate['covered_subprobability'], candidate['uncovered_target_mass'],
                                candidate['construct_topology'], req['conditions'], req['outcome'])
    oracle = ORACLE['conditional_formal'][case]
    assert out['bounds']['formal']['lower'] == oracle['lower']
    assert out['bounds']['formal']['upper'] == oracle['upper']
    assert out['uncovered_target_mass'] == oracle['unknown']
    assert out['route_probability'] is None
    if case != 'W1':
        assert out['supported_point'] is None


def test_w2_native_unknown_mass_drives_new_consumer_bounds():
    import f43_product as product
    out = product.f6_view('W2')
    assert out['state'] == 'PARTIAL_CONDITIONAL_IDENTIFICATION', out
    assert out['bounded_conditional']['bounds']['formal']['lower'] == '2/5'
    assert out['bounded_conditional']['bounds']['formal']['upper'] == '4/5'
    assert out['native_evidence']['evidence']['uncovered_target_mass'] == '1/4'
    assert out['original_N9_admitted'] is False


def test_bounded_conditional_sharpness_and_interior_allocations():
    # Independent constructive oracle: distribute unknown mass over C,Y cells.
    a, b, u = Q(1, 4), Q(3, 8), Q(1, 4)
    lo, hi = Q(2, 5), Q(4, 5)
    values = []
    for conditional_ticks in range(11):
        mass_c = u * conditional_ticks / 10
        for event_ticks in range(11):
            mass_event = mass_c * event_ticks / 10
            values.append((a + mass_event)/(b + mass_c))
    assert min(values) == lo and max(values) == hi
    assert lo <= Q(2, 3) <= hi  # naive covered-only value is only a scenario
    assert m.missing_sensitivity(str(a), str(b), str(u), missing_condition_share='1',
                                 missing_event_given_condition='1/2')['value'] == '3/5'


def test_native_source_and_bias_envelopes_widen_conditional_uncertainty():
    import f43_product as product
    out = product.f6_view('W2')
    oracle = ORACLE['W2_conditional_envelope']
    for name, expected in [('source_disagreement_conditional_envelope', oracle['source_disagreement']),
                           ('bias_sensitivity_conditional_envelope', oracle['bias_sensitivity'])]:
        actual = out[name]['bounds']['formal']
        assert (actual['lower'], actual['upper']) == (expected['lower'], expected['upper'])
        assert out[name]['point'] is None
    assert Q(out['bias_sensitivity_conditional_envelope']['bounds']['formal']['lower']) < Q('2/5')
    assert Q(out['bias_sensitivity_conditional_envelope']['bounds']['formal']['upper']) > Q('4/5')


def test_infeasible_cell_envelope_rejected():
    from cell_envelope_bounds import conditional_envelope
    rows = [dict(categories=['C', 'yes'], lower='3/4', upper='1'),
            dict(categories=['C', 'no'], lower='3/4', upper='1')]
    with pytest.raises(m.MethodError, match='INFEASIBLE_CELL_ENVELOPE'):
        conditional_envelope(rows, ['condition', 'outcome'], {'condition': 'C'}, 'outcome')


@pytest.mark.parametrize('fault', ['lost_unknown', 'negative', 'duplicate', 'self', 'outside'])
def test_invalid_partial_inputs_never_become_point(fault):
    bundle, req = native('W2'); c = deepcopy(bundle['candidate'])
    if fault == 'lost_unknown': c['uncovered_target_mass'] = '0'
    if fault == 'negative': c['covered_subprobability'][0]['probability'] = '-1'
    if fault == 'duplicate': c['covered_subprobability'].append(c['covered_subprobability'][0])
    if fault == 'self': req['conditions'] = {req['outcome']: 'formal'}
    if fault == 'outside': req['conditions'] = {'material_security': 'outside'}
    with pytest.raises(m.MethodError):
        m.partial_conditional(c['covered_subprobability'], c['uncovered_target_mass'],
                              c['construct_topology'], req['conditions'], req['outcome'])


def test_marginal_bounds_call_actual_f6_native_primitive():
    import f43_product as product
    view = product.marginal_view()
    assert view['native_primitive']['lower'] == '1/10'
    assert view['native_primitive']['upper'] == '1/2'
    assert view['candidate']['conditional'] == {'lower': '1/5', 'upper': '1'}
    assert view['native_primitive']['scenario_is_measured'] is False


def test_native_ff_values_reach_context_consumer():
    import f43_product as product
    out = product.retained_view()
    assert out['GT2']['state'] == 'RETAINED_CONTEXT_VALUES_READ', out
    cells = [c for row in out['GT2']['relation']['conditional_count_profile'] for c in row['target_counts']]
    assert sum(c['joint_support_count'] for c in cells) == 19210
    assert sum(c['joint_support_count'] == 0 for c in cells) == 23
    assert len(cells) == 36
    assert out['J04']['fact_ref']['content_hash'] == 'c823a816ce6f71431c99b1a466c7313f3766e5d1e7832fc36b6a31f15835dd02'
    assert out['original_consumer_admitted'] is False


def test_native_temporal_population_gate_changes_f43_view():
    import f43_product as product
    out = product.temporal_view()
    assert out['native']['cases']['population_change']['state'] == 'NONCOMPARABLE_POPULATION_OR_ESTIMAND'
    assert out['strict']['population_change']['state'] == 'NONCOMPARABLE_POPULATION_OR_ESTIMAND'
    assert out['observed_delta'] is None


def test_t35_rule_drives_unchanged_original_e04():
    import f43_product as product
    out = product.original_client_view()
    early = out['HISTORICAL']['native_consumer']['material']['structural_routes']
    late = out['TEST_CURRENT']['native_consumer']['material']['structural_routes']
    assert early['training']['state'] == 'ELIGIBLE'
    assert late['training']['state'] == 'BLOCKED_BY_MODELED_RULE'
    assert early['civil']['state'] == late['civil']['state'] == 'ELIGIBLE'
    assert out['HISTORICAL']['learned_binding'] == out['TEST_CURRENT']['learned_binding']


@pytest.mark.parametrize('field', m.IDENTITY)
def test_missing_equal_temporal_identity_is_unknown(field):
    pair = w.periods.comparable_pair()
    for p in pair: p.pop(field)
    assert w.ee1.population_estimand_gate(pair)['state'] == 'POPULATION_OK'
    assert m.strict_temporal_gate(pair, w.periods.ASOF, w.ee1)['state'] == 'UNKNOWN_TEMPORAL_IDENTITY'


def test_missing_equal_population_identity_is_unknown():
    pair = w.periods.comparable_pair()
    for p in pair: p.pop('target_population')
    assert w.ee1.population_estimand_gate(pair)['state'] == 'POPULATION_OK'
    assert m.strict_temporal_gate(pair, w.periods.ASOF, w.ee1)['state'] == 'UNKNOWN_TEMPORAL_IDENTITY'


def test_rev1_label_cannot_bypass_future_publication():
    pair = w.periods.comparable_pair()
    for p in pair: p['rule_publication'] = '2027-01-01'
    assert w.ee1.clock_gate(pair[0], w.periods.ASOF)['state'] == 'CLOCK_OK'
    assert m.strict_temporal_gate(pair, w.periods.ASOF, w.ee1)['state'] == 'FUTURE_RULE_AT_HISTORICAL_AS_OF'


@pytest.mark.parametrize('change,expected', [
    ('missing_publication', 'UNKNOWN_PUBLICATION_TIME'),
    ('bad_date', 'UNKNOWN_PUBLICATION_TIME'),
    ('observation_mismatch', 'OBSERVATION_ANCHOR_MISMATCH'),
    ('future_evidence', 'FUTURE_EVIDENCE_AT_HISTORICAL_AS_OF'),
])
def test_temporal_clock_negative_controls(change, expected):
    pair = w.periods.comparable_pair()
    if change == 'missing_publication': pair[0].pop('evidence_publication')
    if change == 'bad_date': pair[0]['evidence_publication'] = '2020-99-99'
    if change == 'observation_mismatch': pair[0]['observation_year'] = 2019
    if change == 'future_evidence': pair[1]['evidence_publication'] = '2027-01-01'
    assert m.strict_temporal_gate(pair, w.periods.ASOF, w.ee1)['state'] == expected


def test_independent_design_change_and_unknown_covariance():
    kw = dict(before='2/5', after='11/20', variance_before='1/400', variance_after='1/400')
    out = m.design_change(**kw, independent=True)
    assert out['delta'] == '3/20'
    assert out['variance_of_difference'] == '1/200'
    unknown = m.design_change(**kw)
    assert unknown['standard_error'] is None
    assert unknown['standard_error_range'] == [0.0, 0.1]
    with pytest.raises(m.MethodError, match='INFEASIBLE_COVARIANCE'):
        m.design_change(**kw, covariance='1/100')
    assert m.design_change('2/5', '11/20', None, None)['standard_error'] is None


def test_scope_cannot_drop_wave_cell_or_pair():
    import f43_product as product
    scope = json.loads((boot.ROOT / '00_EXPECTED_WORLD_FREEZE.json').read_text())
    assert len(scope['waves']) == 35 and len(scope['cells']) == 105 and len(scope['pairs']) == 595
    with pytest.raises(ValueError, match='PROSPECTIVE_SCOPE_OMISSION'):
        product.validate_scope(scope, scope['waves'][:-1], scope['pairs'])
    actual = product.estate(scope)
    actual['cells'].pop()
    with pytest.raises(ValueError, match='EXPECTED_F5_F7_CELL_OMISSION_OR_DUPLICATION'):
        product.validate_estate(scope, actual)
    actual = product.estate(scope)
    actual['pairs'].pop()
    with pytest.raises(ValueError, match='PROSPECTIVE_SCOPE_OMISSION'):
        product.validate_estate(scope, actual)
