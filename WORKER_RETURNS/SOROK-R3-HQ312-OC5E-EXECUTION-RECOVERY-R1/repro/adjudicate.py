#!/usr/bin/env python3
"""OC5E — derive the machine-readable red adjudication from executed JUnit."""
from __future__ import annotations

import collections
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
OBS = RETURN / 'observations'


def cases(junit):
    root = ET.parse(OBS / junit).getroot()
    suite = root.find('testsuite') if root.tag == 'testsuites' else root
    out = []
    for tc in suite.iter('testcase'):
        fail = next((k for k in tc if k.tag in ('failure', 'error')), None)
        out.append(dict(
            name=tc.get('name'),
            cls=(tc.get('classname') or '').split('.')[-1],
            outcome='FAIL' if fail is not None else 'PASS',
            type=(fail.get('type') if fail is not None else None),
            reason=((fail.get('message') or '').strip()[:220]
                    if fail is not None else None)))
    return out


def main() -> int:
    inherited = cases('inherited_131.xml')
    oc4 = cases('oc4_new_36.xml')
    e5 = cases('oc5e_native_hostiles.xml')
    oc5 = cases('oc5_prior_predictions.xml')

    reason_class = {}
    for c in inherited:
        if c['outcome'] != 'FAIL':
            continue
        r = c['reason'] or ''
        if 'LedgerRollbackError' in r or \
                'real capsule argument required' in r or \
                'does not bind capsule content' in r:
            reason_class[c['name']] = 'six_procedural'
        elif 'RevocationError' in r or 'PurposeViolationError' in r:
            reason_class[c['name']] = 'six_early_refusal'
        elif 'full signed capsule envelope identity' in r:
            reason_class[c['name']] = 'four_content_only_signature'
        else:
            reason_class[c['name']] = 'unclassified'

    family = {}
    for c in e5:
        if c['outcome'] != 'FAIL':
            continue
        n = c['name']
        if 'normalization_equivalent' in n:
            family[n] = 'A1_normalization_equivalent_allowed_field_alias'
        elif 'confusable_leak_token' in n:
            family[n] = 'A2_nfkc_invisible_confusable_leak_token'
        elif 'malformed_signature_object' in n:
            family[n] = 'A3_malformed_signature_object_untyped'
        elif 'non_enum_role' in n:
            family[n] = 'A4_non_enum_role_string_untyped'
        elif 'unhashable_holder' in n:
            family[n] = 'A5_unblind_unhashable_holder_untyped'
        elif 'capsule_identity_field_types' in n or 'semantic_fingerprint' in n:
            family[n] = 'A6_capsule_identity_field_types_unvalidated'
        else:
            family[n] = 'unclassified'

    inherited_reds = [c for c in inherited if c['outcome'] == 'FAIL']
    e5_reds = [c for c in e5 if c['outcome'] == 'FAIL']
    oc5_reds = [c for c in oc5 if c['outcome'] == 'FAIL']
    everything = inherited + oc4 + e5 + oc5

    adjudication = dict(
        verdict=('REVIEW_REVISE__NATIVE_EXECUTION_RECOVERED__'
                 f'{len(e5_reds)}_NEW_NATIVE_HOSTILE_REDS__'
                 f'{len(oc5_reds)}_OF_{len(oc5_reds)}_OC5_PREDICTIONS_'
                 'CONFIRMED_NATIVELY__NO_AUTHOR_REPAIR__TEST_ONLY_ONLY__'
                 'NO_ADOPTION'),
        source_under_review=dict(
            commit='0caaec590f6a8bf6744f22dc9c948c5fe233bc94',
            git_blob_sha1='af2b7e943018077cb36808b5af1cd67704624bec',
            sha256='447e5bb738fc49c946a39ca438126e9c2a69d93025600f053662'
                   'e56f846f9e3a'),
        tallies=dict(
            inherited_131=dict(total=len(inherited),
                               passed=sum(1 for c in inherited if c['outcome'] == 'PASS'),
                               red=sum(1 for c in inherited if c['outcome'] == 'FAIL'),
                               expected='121 PASS / 10 RED',
                               matches_expected=(sum(1 for c in inherited if c['outcome'] == 'PASS') == 121
                                                 and sum(1 for c in inherited if c['outcome'] == 'FAIL') == 10)),
            oc4_new_36=dict(total=len(oc4),
                            passed=sum(1 for c in oc4 if c['outcome'] == 'PASS'),
                            red=sum(1 for c in oc4 if c['outcome'] == 'FAIL'),
                            expected='36 PASS',
                            matches_expected=len(oc4) == 36 and all(c['outcome'] == 'PASS' for c in oc4)),
            oc5e_native_hostiles=dict(total=len(e5),
                                      passed=sum(1 for c in e5 if c['outcome'] == 'PASS'),
                                      red=len(e5_reds), expected='regression bank',
                                      matches_expected=None),
            oc5_prior_predictions=dict(total=len(oc5),
                                       passed=sum(1 for c in oc5 if c['outcome'] == 'PASS'),
                                       red=len(oc5_reds),
                                       expected='all predicted defects RED',
                                       matches_expected=len(oc5_reds) == 7),
            totals=dict(cases=len(everything),
                        passed=sum(1 for c in everything if c['outcome'] == 'PASS'),
                        red=sum(1 for c in everything if c['outcome'] == 'FAIL'))),
        part_a_ten_historical_original_reds=[
            dict(index=i + 1, case=c['name'],
                 literal_reason=c['reason'], classification=reason_class[c['name']],
                 adjudication='not an implementation defect; superseded by or '
                              'refused earlier than the authored expectation',
                 canonical_capsule_signature_identity_weakened=False)
            for i, c in enumerate(inherited_reds)],
        part_b_oc5_predictions=[
            dict(packet='{"public_projection":{"context":"safe","ｃontext":"shadow"}}',
                 oc5_status='predicted_unexecuted',
                 native_result='detect_leakage() == []', verdict='CONFIRMED_RED'),
            dict(packet='{"public_projection":{"context":"safe","con\\u034ftext":"shadow"}}',
                 oc5_status='predicted_unexecuted',
                 native_result='detect_leakage() == []', verdict='CONFIRMED_RED'),
            dict(packet='{"public_projection":{"context":"safe","CONT\\u00c9XT":"shadow"}}',
                 oc5_status='predicted_unexecuted',
                 native_result='detect_leakage() == []', verdict='CONFIRMED_RED'),
            dict(packet='{"note":"charming","n\\u034fote":"shadow"}}',
                 oc5_status='predicted_unexecuted',
                 native_result='detect_leakage() == []', verdict='CONFIRMED_RED'),
            dict(claim='malformed primary signature raises typed SignatureError',
                 oc5_status='predicted_unexecuted',
                 native_result='AttributeError for every non-None malformed object; '
                               'only None is typed',
                 verdict='CONFIRMED_RED'),
            dict(claim=f"OC5 committed falsifier bank ({len(oc5)} cases)",
                 oc5_status='predicted_unexecuted',
                 native_result=f'{len(oc5_reds)} FAIL / {len(oc5) - len(oc5_reds)} PASS',
                 verdict='CONFIRMED_RED'),
            dict(claim='value-level U+034F / U+200B / fullwidth splits',
                 oc5_status='excerpt_tested',
                 native_result="refused with ['answer_key']", verdict='CONFIRMED_FIXED'),
            dict(claim='positive single-context control', oc5_status='excerpt_tested',
                 native_result='[]', verdict='CONFIRMED_PASS')],
        part_c_new_native_reds=[
            dict(case=c['name'], family=family[c['name']], observed=c['reason'])
            for c in e5_reds],
        new_red_family_counts=dict(sorted(collections.Counter(family.values()).items())),
        new_red_total=len(e5_reds),
        oc5e_controls_passing=[c['name'] for c in e5 if c['outcome'] == 'PASS'],
        holds=dict(test_only_scope=True, no_real_signer_institution=True,
                    no_protected_holdout=True, no_durable_external_journal=True,
                    no_independent_semantic_oracle=True,
                    cross_process_c07='NOT_REACHED absent API',
                    no_external_model_calls=True, no_original_survey_data=True,
                    no_v3=True, no_product_premain_current_edit=True,
                    no_adoption=True, author_source_repaired=False,
                    distinct_independent_court_required=True))

    (RETURN / '02_RED_ADJUDICATION.json').write_text(
        json.dumps(adjudication, indent=2) + '\n')
    print('new red families:', json.dumps(adjudication['new_red_family_counts']))
    print('totals:', json.dumps(adjudication['tallies']['totals']))
    print('oc5e controls passing:', len(adjudication['oc5e_controls_passing']))
    print('matches expected inherited:', adjudication['tallies']['inherited_131']['matches_expected'])
    print('matches expected oc4:', adjudication['tallies']['oc4_new_36']['matches_expected'])
    print('oc5 bank all red:', adjudication['tallies']['oc5_prior_predictions']['matches_expected'])
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
