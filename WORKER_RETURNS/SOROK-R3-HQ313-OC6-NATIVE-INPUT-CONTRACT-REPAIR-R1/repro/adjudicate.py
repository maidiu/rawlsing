#!/usr/bin/env python3
"""OC6 — per-case before/after adjudication of the unchanged 349-case court."""
from __future__ import annotations

import json
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent
BEFORE = Path('/tmp/oc6-before/observations')
AFTER = RETURN / 'observations'

FAMILY = (
    ('normalization_equivalent', 'A1'),
    ('confusable_leak_token', 'A2'),
    ('malformed_signature_object', 'A3'),
    ('non_enum_role', 'A4'),
    ('unhashable_holder', 'A5'),
    ('capsule_identity_field_types', 'A6'),
    ('semantic_fingerprint', 'A6'),
)

COURTS = ['inherited_131', 'oc4_new_36', 'oc5e_native_hostiles',
          'oc5_prior_predictions']


def family_of(name):
    for needle, code in FAMILY:
        if needle in name:
            return code
    return None


def load(root, label):
    out = {}
    for court in COURTS:
        data = json.loads((root / f'case_matrix_{label}.json').read_text())
        for case in data['matrix'][court]:
            out[(court, case['name'])] = case
    return out


def main() -> int:
    before = load(BEFORE, 'before')
    after = load(AFTER, 'after')
    assert set(before) == set(after), 'the 349-case court changed identity'

    rows = []
    for key in sorted(before):
        court, name = key
        b, a = before[key], after[key]
        if b['outcome'] == a['outcome']:
            continue
        rows.append(dict(court=court, case=name,
                         before=b['outcome'], after=a['outcome'],
                         family=family_of(name),
                         before_reason=b['reason'], after_reason=a['reason']))

    still_red = [dict(court=c, case=n, family=family_of(n),
                       reason=after[(c, n)]['reason'],
                       type=after[(c, n)]['type'])
                 for (c, n) in sorted(after)
                 if after[(c, n)]['outcome'] == 'FAIL']

    fixed = [r for r in rows if r['before'] == 'FAIL' and r['after'] == 'PASS']
    flipped = [r for r in rows if r['before'] == 'PASS' and r['after'] == 'FAIL']

    # classify the nine expected by-design flips
    BY_DESIGN = {
        'test_alias_holes_are_observed_not_theorised': 'A1 hole witness: asserted the alias holes existed',
        'test_confusable_holes_are_observed_only_for_nfkc_invisible_scripts': 'A2 hole witness: asserted the confusable holes existed',
        'test_malformed_signature_holes_are_observed_as_attributeerror': 'A3 hole witness: asserted raw AttributeError',
        'test_non_enum_role_string_hole_is_observed_as_attributeerror': 'A4 hole witness: asserted raw AttributeError',
        'test_capsule_identity_field_type_hole_is_observed': 'A6 hole witness: asserted malformed capsules commit',
        'test_unblind_unhashable_holder_hole_is_observed_as_typeerror': 'A5 hole witness: asserted raw TypeError',
        'test_imported_module_is_the_pinned_oc4_blob': 'provenance pin for the UNREPAIRED blob, necessarily superseded by the repaired source',
    }

    def classify(row):
        base = row['case'].split('[')[0]
        return BY_DESIGN.get(row['case']) or BY_DESIGN.get(base) or 'UNCLASSIFIED'

    for row in flipped:
        row['classification'] = classify(row)
    assert all(r['classification'] != 'UNCLASSIFIED' for r in flipped), \
        [r['case'] for r in flipped if r['classification'] == 'UNCLASSIFIED']

    MALFORMED_A2 = {
        'test_confusable_leak_token_substitution_must_be_flagged[greek-o]':
            "OC5E input 'l\\u03bfwful_answers' folds to 'lowful_answers': U+03BF is a "
            "homoglyph for 'o' and was placed where 'a' belongs, so it does not "
            "spell the denied token 'lawful_answers' even under a perfect fold.",
        'test_confusable_leak_token_substitution_must_be_flagged[mixed-cyrillic]':
            "OC5E input '\\u0430ns\\u0435er\\u0455_key' folds to 'anseers_key': the "
            "'w' is absent and U+0435 (homoglyph for 'e') sits where 'w' belongs, "
            "so it does not spell the denied token 'answer_key'.",
    }
    for row in still_red:
        base = row['case'].split('[')[0]
        if row['case'] in MALFORMED_A2:
            row['adjudication'] = 'MALFORMED_OC5E_INPUT'
            row['detail'] = MALFORMED_A2[row['case']]
        elif base == 'test_imported_module_is_the_pinned_oc4_blob':
            row['adjudication'] = 'BY_DESIGN_PROVENANCE_PIN'
        elif base in BY_DESIGN:
            row['adjudication'] = 'BY_DESIGN_HOLE_WITNESS'
            row['detail'] = BY_DESIGN[base]
        else:
            row['adjudication'] = 'HISTORICAL_ORIGINAL_RED_UNCHANGED'

    payload = dict(
        claim=('SOURCEFREE_TEST_ONLY_INPUT_CONTRACT_REPAIR__349_COURT_UNCHANGED__'
               '54_OF_56_DEMONSTRATED_REDS_CLOSED__2_OC5E_INPUTS_MALFORMED__'
               'TEN_HISTORICAL_REDS_UNCHANGED__NO_ADOPTION'),
        before=dict(cases=len(before),
                    passed=sum(1 for v in before.values() if v['outcome'] == 'PASS'),
                    red=sum(1 for v in before.values() if v['outcome'] == 'FAIL')),
        after=dict(cases=len(after),
                   passed=sum(1 for v in after.values() if v['outcome'] == 'PASS'),
                   red=sum(1 for v in after.values() if v['outcome'] == 'FAIL')),
        oc6_new_author_controls=json.loads(
            (AFTER / 'case_matrix_after.json').read_text()
        )['courts'][-1] if len(json.loads(
            (AFTER / 'case_matrix_after.json').read_text())['courts']) > 4 else None,
        fixed=[dict(court=r['court'], case=r['case'], family=r['family'])
               for r in fixed],
        flipped_to_red=flipped,
        still_red=still_red,
        totals=dict(
            demonstrated_reds_closed=len([r for r in fixed
                                          if r['family']]),
            oc5_predicted_closed=len([r for r in fixed
                                      if r['court'] == 'oc5_prior_predictions']),
            oc5e_new_closed=len([r for r in fixed
                                 if r['court'] == 'oc5e_native_hostiles']),
            malformed_oc5e_inputs=len([r for r in still_red
                                       if r['adjudication'] ==
                                       'MALFORMED_OC5E_INPUT']),
            historical_original_reds=len([r for r in still_red
                                          if r['adjudication'] ==
                                          'HISTORICAL_ORIGINAL_RED_UNCHANGED']),
            by_design_flips=len(flipped)),
    )
    (RETURN / 'observations' / 'before_after_adjudication.json').write_text(
        json.dumps(payload, indent=2) + '\n')
    print('before:', json.dumps(payload['before']))
    print('after :', json.dumps(payload['after']))
    print('fixed:', len(fixed), ' flipped-to-RED:', len(flipped))
    print('totals:', json.dumps(payload['totals'], indent=1))
    print('still red adjudications:')
    for row in still_red:
        print(f"  {row['adjudication']:<34} {row['case'][:62]}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
