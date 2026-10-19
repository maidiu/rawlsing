"""F43 native consumers and conservative method improvements at declared grades.

No raw reader and no authority constructor. E04 is invoked unchanged. Retained
CONTEXT cannot be placed into its unsupported N9/structural-purpose slots.
"""
from copy import deepcopy
from fractions import Fraction as Q
import hashlib
import json
from pathlib import Path
import sys

import bootstrap_f43 as boot
import bounded_methods as methods
from cell_envelope_bounds import conditional_envelope
import objective_world as w

ROOT = boot.ROOT
SCHEMA = 'F43_OBJECTIVE_WORLD_RETURN@1'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                     allow_nan=False).encode()).hexdigest()


def retained_view():
    return dict(GT2=w.context_read_or_refusal(), J04=w.position_context(),
                world_use='SOURCE_INDEXED_RETAINED_CONTEXT_ONLY',
                original_consumer_admitted=False,
                limitation='CONTEXT is not structural-route permission or operative CURRENT')


def f6_view(case):
    evidence = w.f6_evidence(case)
    out = dict(native_evidence=evidence, bounded_conditional=None,
               sensitivity=[], original_N9_admitted=False,
               grade='SOURCEFREE_METHOD_CANDIDATE', route_probability=None)
    # A bounded alternative is useful only for a valid partial/complete native
    # target. Native refusals (overlap, self-conditioning, unknown category)
    # must remain refusals rather than becoming an attractive interval.
    if evidence['state'] not in ('SUPPORTED_SYNTHESIS', 'PARTIAL_IDENTIFICATION'):
        out['state'] = evidence['state']
        return out
    key = next(k for k in w.f6.OW.WORLD_BUILDERS if k.split('_')[0] == case)
    target, sources, policy = w.f6.OW.WORLD_BUILDERS[key]()
    bundle = w.f6.F6M.synthesize(target, sources, policy)
    if bundle['content_hash'] != evidence['product_ref']:
        raise ValueError('NATIVE_F6_BUNDLE_CHANGED_BETWEEN_READS')
    c = bundle['candidate']; request = w.f6.request(key)
    bound = methods.partial_conditional(c['covered_subprobability'], c['uncovered_target_mass'],
                                        c['construct_topology'], request['conditions'], request['outcome'])
    out.update(state=bound['state'], bounded_conditional=bound,
               native_bundle_ref=bundle['content_hash'], native_request=request,
               limitations=['Conditional identification set conditions on transported source tables and fixed target shares',
                            'Sampling uncertainty, mapping and transport bias are separate; no conditional CI is available',
                            'Hypothetical allocation points are not identified population probabilities'])
    out['source_disagreement_conditional_envelope'] = conditional_envelope(
        evidence['evidence']['bounds'], c['construct_topology'], request['conditions'], request['outcome'])
    out['bias_sensitivity_conditional_envelope'] = conditional_envelope(
        evidence['evidence']['bias_sensitivity_bounds'], c['construct_topology'], request['conditions'], request['outcome'])
    if bound.get('bounds') and Q(c['uncovered_target_mass']) > 0:
        for label, limits in bound['bounds'].items():
            for r in ('0', '1/2', '1'):
                for theta in ('0', '1/2', '1'):
                    scenario = methods.missing_sensitivity(limits['covered_event_mass'],
                               bound['covered_condition_mass'], c['uncovered_target_mass'],
                               missing_condition_share=r, missing_event_given_condition=theta)
                    scenario['outcome_category'] = label
                    out['sensitivity'].append(scenario)
    return out


def marginal_view():
    # Directly calls the actual native primitive, resolving R39I's recorded
    # missing staging path. These exact margins are frozen method inputs only.
    native = w.f6.F6M.complementary_binary_bounds('3/5', '1/2')
    candidate = methods.marginal_joint_bounds('3/5', '1/2')
    return dict(native_primitive=native, candidate=candidate,
                native_producer_blob='2df811d76db258d98d89ffb43c830cb221ff9a7d',
                source_population_match=None, real_use_authorized=False,
                limitation='No qualified original35 same-target margins were supplied; these are method inputs')


def temporal_view():
    native = w.temporal_methods()
    strict = {}
    makers = dict(comparable_probe=w.periods.comparable_pair,
                  mixed_family=w.periods.mixed_family, mixed_country=w.periods.mixed_country,
                  population_change=w.periods.population_change, estimand_change=w.periods.estimand_change,
                  future_rule=w.periods.future_rule, future_evidence=w.periods.future_evidence,
                  duplicate_year=w.periods.duplicate_year)
    for name, maker in makers.items():
        strict[name] = methods.strict_temporal_gate(maker(), w.periods.ASOF, w.ee1)
    pair = w.periods.comparable_pair()
    for p in pair:
        for field in methods.IDENTITY: p.pop(field)
    strict['missing_equal_identity'] = methods.strict_temporal_gate(pair, w.periods.ASOF, w.ee1)
    pair = w.periods.comparable_pair()
    for p in pair: p['rule_publication'] = '2027-01-01'
    strict['future_rev1_label'] = methods.strict_temporal_gate(pair, w.periods.ASOF, w.ee1)
    args = dict(before='2/5', after='11/20', variance_before='1/400', variance_after='1/400')
    return dict(native=native, strict=strict, observed_pairs=[], observed_delta=None,
                grade='SOURCEFREE_V553_EE1_PLUS_F43_PRE_GUARD',
                design_method_comparison=dict(independent=methods.design_change(**args, independent=True),
                    unknown_covariance=methods.design_change(**args),
                    unknown_design=methods.design_change('2/5', '11/20', None, None)),
                limitation='No original measured wave-pair admission; T35 policy revisions are synthetic rules')


def original_client_view():
    world = w.ObjectiveWorld()
    return {mode: world.read(mode) for mode in ('HISTORICAL', 'AS_OF', 'TEST_CURRENT')}


def corrected_a_comparison():
    import f6c_method_c as conservative
    out = {}
    for case in ('W1', 'W2', 'W3', 'W7'):
        key = next(k for k in w.f6.OW.WORLD_BUILDERS if k.split('_')[0] == case)
        rows = {}
        for name in ('A', 'B'):
            bundle = w.f6.build(name, key)
            result = w.consume_f6m_evidence(bundle, w.f6.request(key))
            rows[name] = dict(implementation=bundle.get('implementation_version'),
                bundle_ref=bundle['content_hash'], state=result['evidence_state'],
                unknown=result['uncovered_target_mass'], point=result['supported_point'])
        target, sources, policy = w.f6.OW.WORLD_BUILDERS[key]()
        no_pool = conservative.nopooling_bounds(target, sources, policy)
        rows['C_NO_TRANSPORT'] = dict(method=no_pool['method'], state=no_pool['joint_status'],
                unknown=no_pool['total_unknown_mass'],
                target_marginal_bounds=no_pool['target_marginal_bounds_employment_position'],
                native_loader_result=no_pool['unidentified_cross_channel'],
                note='Inherited C staging loader remains unchanged; F43 separately calls exact native primitive')
        out[case] = rows
    return dict(comparison=out, selected='B_F6M_PLUS_F43_PARTIAL_CONDITIONAL_CANDIDATE',
                reason='Corrected A loses planned shares in W2/W7; B preserves them. F43 bounds add conditional information without dropping unknown mass.',
                calibrated_probability='NO_QUALIFIED_TARGET_OR_CALIBRATION_OWNER',
                partial_pooling='REQUIRES_MEASUREMENT_INVARIANCE_TARGET_AND_MODEL_VALIDATION',
                real_use_authorized=False)


def validate_scope(frozen, actual_waves, actual_pairs):
    if ([(r['id'], r['name']) for r in frozen['waves']] != [(r['id'], r['name']) for r in actual_waves]
            or [(p['left'], p['right']) for p in frozen['pairs']] != [(p['left'], p['right']) for p in actual_pairs]
            or len(frozen['cells']) != 105):
        raise ValueError('PROSPECTIVE_SCOPE_OMISSION')


def validate_estate(frozen, result):
    validate_scope(frozen, result['waves'], result['pairs'])
    actual = [c['cell_id'] for c in result['cells']]
    if set(actual) != set(frozen['cells']) or len(actual) != len(set(actual)):
        raise ValueError('EXPECTED_F5_F7_CELL_OMISSION_OR_DUPLICATION')
    if any(r['original_measured_occupancy'] for r in result['waves']):
        raise ValueError('UNISSUED_ORIGINAL_OCCUPANCY')


def estate(frozen):
    waves = []
    for row in frozen['waves']:
        wave = deepcopy(row)
        wave.update(F5='RETAINED_AFRO_R5_CONTEXT_ONLY' if row['id'] == 'SRC02' else 'NEEDS_SOURCE_AND_FF_POSITION_RELATION_ISSUANCE',
                    F6='NEEDS_TARGET_POPULATION_ESTIMAND_TRANSPORT_AND_N9_USE',
                    F7='NEEDS_SOURCE_QUALIFIED_OBSERVED_PAIR_AND_DESIGN',
                    original_measured_occupancy=False, source_opened=False)
        waves.append(wave)
    pairs = [dict(p, actual_state='NOT_SOURCE_QUALIFIED_AT_THIS_EVIDENCE_CUT',
                  measured_delta=None, population_joint=None) for p in frozen['pairs']]
    validate_scope(frozen, waves, pairs)
    cells = [dict(cell_id=f"{r['id']}.{g}", source_id=r['id'], gate=g, state=r[g],
                  grade='HISTORICAL_RETAINED_EVIDENCE' if r['id'] == 'SRC02' and g == 'F5'
                        else 'DEVELOPMENT_BLOCKER_WITH_NARROW_OWNER')
             for r in waves for g in ('F5', 'F6', 'F7')]
    result = dict(waves=waves, pairs=pairs, cells=cells, all35_no_drop=True,
                original_measured_occupancy=0, observed_temporal_pairs=0,
                no_intrinsic_nonapplicability_claim=True)
    validate_estate(frozen, result)
    return result


def owner_decisions(frozen):
    out = []
    for row in frozen['waves']:
        out.append(dict(decision_id=f"F43-{row['id']}-SOURCE-FIELD-TIME", source_id=row['id'],
            source_name=row['name'], status='NEEDS_COMPETENT_ISSUER',
            authority_owner=f"{row['family']} source/semantic/design issuer; identity/delegation must be authenticated by HQ",
            operation_owner='U43 prospective item/operation owner; not F43',
            requested_material=dict(source=['exact edition and source digest', 'approved host, purpose, operation and export ceiling', 'issuer-signed prospective U/E_pre'],
                F5=['producer-owned source/target, positioned risk, area and time', 'structural relation and carrier/mediation meaning', 'FF admission and native N9 resolution-purpose grant'],
                F6=['matched target population, unit and estimand', 'native response mapping, design and weight refs', 'overlap/nonduplication', 'target-share/positivity basis', 'operation-specific I07 composition/transport and model/version/use'],
                F7=['observed fieldwork and publication dates', 'country/population/estimand and wording topology', 'qualified harmonization and design/variance/covariance', 'exact V553 source temporal identity', 'historical/as-of N9 purpose']),
            next_action='Issue exact permitted subset or typed reason per item/operation; supply derived nonperson-level products to F43 through B43',
            positive_test='Exact issued product resolves under permitted clock/purpose; unsupported version/host/transport is refused',
            rollback='Revoke only affected product/relation; preserve other admitted source-indexed views',
            cannot_substitute=['file ownership', 'worker commission', 'fixture REVIEWED labels', 'matching source-family name'] ))
    out.extend([
        dict(decision_id='F43-F6-METHOD', authority_owner='Independent F6 scientific/model/transport owner',
             status='AUTHOR_VALIDATED_CANDIDATE_PENDING_INDEPENDENT_ACCEPTANCE',
             next_action='Adjudicate fixed-target partial conditional allocation bounds separately from mapping/transport bias and sampling uncertainty; qualify each real target before N9 use'),
        dict(decision_id='F43-F7-METHOD', authority_owner='Independent temporal scientific/design owner',
             status='AUTHOR_VALIDATED_PRE_GUARD_PENDING_INDEPENDENT_ACCEPTANCE',
             next_action='Review missing-equal-identity and rev1 publication bypass controls; issue any design-compatible harmonization instead of assuming signature equality'),
        dict(decision_id='F43-ORIGINAL-CONSUMER-PURPOSE', authority_owner='Original E04/N9/N10W purpose issuer',
             status='NO_NEW_PURPOSE_ISSUANCE',
             next_action='Admit exact qualified F5/F6/F7 readset to original consumer contract; CONTEXT does not authorize structural routes'),
    ])
    return out


def product():
    frozen = json.loads((ROOT / '00_EXPECTED_WORLD_FREEZE.json').read_text())
    return dict(schema=SCHEMA, expected_scope_sha256=hashlib.sha256((ROOT / '00_EXPECTED_WORLD_FREEZE.json').read_bytes()).hexdigest(),
                estate=estate(frozen), retained=retained_view(),
                F6={f'W{i}': f6_view(f'W{i}') for i in range(1, 9)},
                marginal_bounds=marginal_view(), temporal=temporal_view(),
                method_comparison=corrected_a_comparison(), original_client=original_client_view(),
                original_purpose_refusals=w.purpose_refusals(), owner_decisions=owner_decisions(frozen),
                full_original_F5_F7_N9_complete=False, source_reads=0,
                authority_grade='NO_NEW_SOURCE_FF_MODEL_TRANSPORT_PURPOSE_OR_ACTOR_RIGHTS',
                scientific_grade='AUTHOR_VALIDATED_CANDIDATE_NOT_INDEPENDENT_SCIENTIFIC_ACCEPTANCE')


def capture():
    p = product()
    if set(p['F6']) != {f'W{i}' for i in range(1, 9)}:
        raise ValueError('F6_OUTPUT_OMISSION')
    if p['retained']['GT2']['state'] != 'RETAINED_CONTEXT_VALUES_READ':
        raise ValueError('RETAINED_FF_POSITIVE_MISSING')
    if p['retained']['J04']['state'] != 'EXACT_J04_RECONSTRUCTION_CONTEXT_READ':
        raise ValueError('RETAINED_POSITION_POSITIVE_MISSING')
    if p['temporal']['observed_delta'] is not None or p['temporal']['observed_pairs']:
        raise ValueError('UNISSUED_OBSERVED_HISTORY')
    raw = (json.dumps(p, sort_keys=True, indent=2, allow_nan=False) + '\n').encode()
    (ROOT / 'world_products.json').write_bytes(raw)
    pins = {p['local']: p for p in json.loads((boot.W41 / 'owner_pins.json').read_text())}
    imports = []
    for name, module in sorted(sys.modules.items()):
        path = getattr(module, '__file__', None)
        if not path:
            continue
        path = Path(path).resolve()
        if path.suffix != '.py' or not path.is_relative_to(ROOT):
            continue
        data = path.read_bytes(); relative = path.relative_to(ROOT).as_posix()
        pin = pins.get(path.relative_to(boot.W41).as_posix()) if path.is_relative_to(boot.W41) else None
        imports.append(dict(module=name, module_file=relative, sha256=hashlib.sha256(data).hexdigest(),
                       git_blob=hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest(),
                       inherited_owner_pin=pin))
    (ROOT / 'evidence/imports.json').write_text(json.dumps(imports, sort_keys=True, indent=2) + '\n')
    print(json.dumps(dict(product_sha256=hashlib.sha256(raw).hexdigest(), waves=35,
                          cells=105, pairs=595, retained_context_paths=2,
                          original_measured_occupancy=0, observed_temporal_pairs=0)))


if __name__ == '__main__':
    capture()
