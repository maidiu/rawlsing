"""X01 sourcefree read-only probe of original V3 baseline/child-model/shards.

No source edits, no provider calls, no survey data. The YAML bridge uses the
system Ruby Psych parser only because PyYAML is absent in the qualified Python.
"""
from __future__ import annotations
import json, subprocess, sys, types
from copy import deepcopy
from pathlib import Path

SOURCE = Path(__import__('os').environ['RAWLSING_STAGING_ROOT'])
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

_RUBY = "require 'yaml'; require 'json'; print JSON.generate(YAML.safe_load(STDIN.read, [], [], true))"
def _safe_load(value):
    if hasattr(value, 'read'):
        value = value.read()
    if not isinstance(value, str):
        raise TypeError('yaml.safe_load expects text')
    p = subprocess.run(['ruby', '-e', _RUBY], input=value, capture_output=True, text=True)
    if p.returncode != 0:
        raise ValueError('YAML_PARSE_FAILED: ' + p.stderr.strip()[:300])
    return json.loads(p.stdout)
_m = sys.modules.get('yaml') or types.ModuleType('yaml')
_m.safe_load = _safe_load
sys.modules['yaml'] = _m

from v3.core.state import BackboneState, StrivingObject
from v3.engine.expectation_baseline import (
    derive_child_expectation_baseline, load_need_axis_rules,
)
from v3.io.parent_baseline_from_behavior import infer_parent_baseline_and_regime
from v3.io.identity_to_backbone import child_model_from_parent_baseline_and_regime
from v3.engine.expectation_events import apply_gift_disruption_shards_from_events
from v3.engine.effects.delta_templates import (
    apply_deltas_to_state, delta_from_event, merge_deltas,
)
from v3.engine.striving_objects import update_striving_step

def parent(father=None, mother=None):
    d = {}
    if father is not None or mother is not None:
        d['parent_behavior'] = {}
        if father is not None:
            d['parent_behavior']['father'] = father
        if mother is not None:
            d['parent_behavior']['mother'] = mother
    return d

def baseline_case(name, parent_identity, environment=None):
    baseline, regime = infer_parent_baseline_and_regime(parent_identity)
    rules = load_need_axis_rules()
    derived = derive_child_expectation_baseline(
        parent_baseline=baseline, transmission_regime=regime,
        environment=environment, rules=rules)
    cm = child_model_from_parent_baseline_and_regime(baseline, regime, age=0)
    return {
        'case': name,
        'parent_identity': parent_identity,
        'inferred_parent_baseline': baseline,
        'transmission_regime': regime,
        'derived_child_baseline': derived,
        'child_model': cm,
        'rules_loaded': bool(rules),
    }

out = {}
out['cases'] = {}
out['cases']['missing_parent'] = baseline_case('missing_parent', {})
out['cases']['loving_low_material'] = baseline_case(
    'loving_low_material',
    parent(father={'parental_warmth': 85, 'parental_authority': 45, 'parental_material_support': 20},
           mother={'parental_warmth': 85, 'parental_authority': 45, 'parental_material_support': 20}))
out['cases']['cold_high_material'] = baseline_case(
    'cold_high_material',
    parent(father={'parental_warmth': 30, 'parental_authority': 80, 'parental_material_support': 80},
           mother={'parental_warmth': 30, 'parental_authority': 80, 'parental_material_support': 80}))
out['cases']['loving_low_material_environment'] = baseline_case(
    'loving_low_material_environment',
    parent(father={'parental_warmth': 85, 'parental_authority': 45, 'parental_material_support': 20},
           mother={'parental_warmth': 85, 'parental_authority': 45, 'parental_material_support': 20}),
    environment={'economic_precarity': 90, 'external_threat': 90,
                 'institutional_reliability': 10, 'collective_solidarity': 0})

# Environment-only contrast: same parent baseline, with/without environment.
neutral_parent = {'attachment': 'hopeful', 'safety': 'hopeful', 'belonging': 'hopeful',
                  'status': 'hopeful', 'competence': 'hopeful', 'autonomy': 'hopeful',
                  'meaning': 'hopeful', 'justice': 'hopeful', 'beauty_play': 'hopeful',
                  'eros_intimacy': 'hopeful'}
neutral_regime = {'warmth': 50, 'coercion': 50, 'openness': 50, 'anxiety': 50,
                  'shame': 50, 'modeling_consistency': 55}
rules = load_need_axis_rules()
out['environment_ignored'] = {
    'without_env': derive_child_expectation_baseline(
        parent_baseline=neutral_parent, transmission_regime=neutral_regime,
        environment=None, rules=rules),
    'with_high_precarity': derive_child_expectation_baseline(
        parent_baseline=neutral_parent, transmission_regime=neutral_regime,
        environment={'economic_precarity': 90, 'external_threat': 90,
                     'institutional_reliability': 10, 'collective_solidarity': 0},
        rules=rules),
}

# Missing baseline default vs explicit forbidden baseline.
out['child_model_defaults'] = {
    'missing_parent_baseline': child_model_from_parent_baseline_and_regime(None, None, age=0),
    'forbidden_attachment_safety': child_model_from_parent_baseline_and_regime(
        {'attachment': 'forbidden', 'safety': 'hopeless'},
        {'openness': 70, 'coercion': 30}, age=0),
}

# Gift/disruption: same event label, opposite declared expectation_type; baseline ignored.
def shard_case(expectation_type, baseline_axis='attachment'):
    s = BackboneState(year=2024, age=8)
    s.expectation_baseline = {baseline_axis: 'hopeful'}
    s.striving_objects.append(StrivingObject(
        id='so_attachment', label='Parent closeness', need_axis='attachment',
        started_age=3, investment=70, identity_load=65, active=True))
    ev = {'kind': 'relationship', 'id': 'ev_parent_late',
          'label': 'Parent works late but calls to say she loves me',
          'expectation_type': expectation_type,
          'striving_object_id': 'so_attachment'}
    apply_gift_disruption_shards_from_events(s, [ev])
    return {
        'expectation_type': expectation_type,
        'gift_shards': [g.__dict__ for g in s.gift_shards],
        'disruption_shards': [d.__dict__ for d in s.disruption_shards],
        'baseline_after': dict(s.expectation_baseline),
        'striving_after': [x.__dict__ for x in s.striving_objects],
    }
out['shard_cases'] = {
    'fulfillment': shard_case('fulfillment'),
    'violation': shard_case('violation'),
}

# Baseline is not revised by an expectation event.
s = BackboneState(year=2024, age=8)
s.expectation_baseline = {'attachment': 'forbidden', 'status': 'hopeless'}
s.striving_objects.append(StrivingObject(
    id='so_attachment', label='Parent closeness', need_axis='attachment',
    started_age=3, investment=70, identity_load=65, active=True))
ev = {'kind': 'relationship', 'label': 'Parent works late but calls to say she loves me',
      'expectation_type': 'fulfillment', 'striving_object_id': 'so_attachment'}
before = deepcopy(s.expectation_baseline)
apply_deltas_to_state(s, {'capacity_deltas': {}, 'domain_deltas': {}, 'alienation_delta': 0,
                          'coherence_delta': 0, 'practice_deltas': {}},
                      {}, selected_events=[ev])
out['baseline_after_event'] = {'before': before, 'after': dict(s.expectation_baseline)}

# update_striving_step setdefaults missing axes to hopeful; it does not change existing values.
s2 = BackboneState(year=2024, age=14)
s2.expectation_baseline = {'attachment': 'forbidden'}
update_striving_step(s2, None, {})
out['baseline_after_striving_step'] = dict(s2.expectation_baseline)

# Expectation-event delta and alienation-vector mutation check.
s3 = BackboneState(year=2024, age=8)
d = delta_from_event({'kind': 'expectation_event', 'intensity': 'major',
                      'expectation_type': 'violation',
                      'magnets': {}, 'implicated': {}}, {})
before_av = {k: getattr(s3.alienation_vector, k) for k in
             ('distant_others', 'near_others', 'self', 'moral_totality')}
before_scalar = s3.alienation
apply_deltas_to_state(s3, merge_deltas([d]), {}, selected_events=[])
after_av = {k: getattr(s3.alienation_vector, k) for k in
            ('distant_others', 'near_others', 'self', 'moral_totality')}
out['alienation_delta_check'] = {
    'delta': d.get('alienation_delta'),
    'before_scalar': before_scalar,
    'after_scalar': s3.alienation,
    'before_vector': before_av,
    'after_vector': after_av,
    'dynamic_attrs': {k: getattr(s3.alienation_vector, k, None) for k in
                      ('structural', 'affective', 'institutional')},
}

# Need-axis YAML per-axis rules are not applied: compare actual rules with empty rules
# on a regime that activates only per-axis economic_precarity conditions.
out['axis_rules_application'] = {
    'actual_rules': derive_child_expectation_baseline(
        parent_baseline=neutral_parent,
        transmission_regime={'warmth': 50, 'coercion': 50, 'openness': 50,
                             'anxiety': 50, 'shame': 50, 'modeling_consistency': 55},
        environment={'economic_precarity': 90, 'external_threat': 90},
        rules=rules),
    'empty_rules': derive_child_expectation_baseline(
        parent_baseline=neutral_parent,
        transmission_regime={'warmth': 50, 'coercion': 50, 'openness': 50,
                             'anxiety': 50, 'shame': 50, 'modeling_consistency': 55},
        environment={'economic_precarity': 90, 'external_threat': 90},
        rules={}),
}

print(json.dumps(out, indent=2, sort_keys=True, default=str))
