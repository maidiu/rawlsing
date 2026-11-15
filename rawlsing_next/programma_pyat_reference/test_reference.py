"""Hostile sourcefree requirements: challenge identity, evidence and illegal proof promotion."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from . import reference as ref


class ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=ref.build()

    def test_all_primary_and_atomic_grains_retained(self):
        for lane,n in ref.EXPECTED.items():self.assertEqual(self.s['coverage'][lane]['rows'],n)
        self.assertEqual(sum(self.s['coverage'][x]['atomic_findings'] for x in 'ABCDEFG'),213)
        self.assertEqual(len(self.s['input_lock']),39)
        self.assertLess(self.s['coverage']['a_distinct_component_ids'],656)
        self.assertEqual(len([e for e in self.s['entities'] if e.startswith('PYAT:SOURCE:')]),35)

    def test_raw_rows_exactly_equal_pinned_git(self):
        r=self.s['records']['ROW:A:PLAN_CROSSWALK:XW0051'];e=r['evidence']
        raw=json.loads(ref.git('show',e['cut']+':'+e['path']).splitlines()[e['line']-1])
        self.assertEqual(raw,r['raw'])
        self.assertEqual(e['blob'],ref.git('rev-parse',e['cut']+':'+e['path']))

    def test_same_label_m2_does_not_merge(self):
        q=ref.query(self.s,'focus','M2')
        self.assertEqual(q['status'],'AMBIGUOUS_ID')
        self.assertGreaterEqual(len(q['candidates']),2)
        self.assertNotEqual(ref.identity('WHOLE101:S01'),ref.identity('ESTATE_AXIS:S01'))
        self.assertNotEqual(ref.identity('WHOLE151:S001'),ref.identity('S01','C'))
        self.assertNotEqual(ref.identity('N9'),ref.identity('SOROK:N9'))

    def test_many_to_many_membership_is_not_alias(self):
        rid='ROW:A:PLAN_CROSSWALK:XW0051'
        edges=[e for e in self.s['edges'].values() if e['record']==rid]
        memberships=[e for e in edges if e['type']=='CROSS_MEMBERSHIP_NOT_IDENTITY']
        self.assertGreater(len(memberships),1)
        self.assertNotEqual(ref.resolve(self.s,'WHOLE151:G001'),ref.resolve(self.s,'WHOLE101:G01'))

    def test_conditional_edges_not_universal(self):
        all_edges=ref.select_edges(self.s,[ref.identity('N8S')])
        required=ref.select_edges(self.s,[ref.identity('N8S')],unconditional=True)
        self.assertTrue(any(e['from']==ref.identity('N8E') and e['type']=='CONDITIONAL_PREREQUISITE' for e in all_edges))
        self.assertFalse(any(e['from']==ref.identity('N8E') and e['to']==ref.identity('N8S') for e in required))
        self.assertEqual(sum(e['type']=='UNCONDITIONAL_PREREQUISITE' for e in self.s['edges'].values()),7)
        self.assertEqual(sum(e['type']=='CONDITIONAL_PREREQUISITE' for e in self.s['edges'].values()),26)

    def test_actual_source_not_consumer_or_fixture(self):
        source=ref.query(self.s,'source','SRC01')
        r=next(r for r in source['records'] if r['table']=='SOURCE35_COVERAGE')
        self.assertEqual(r['raw']['science_issued_eligible_operations'],'NOT_EVIDENCED')
        b=ref.query(self.s,'code','N10E')
        self.assertIn('test',json.dumps(b).lower())
        self.assertEqual(b['boundary']['source_native_empirical_pilot'],'HOLD')

    def test_older_stronger_variant_and_current_weaker_both_visible(self):
        q=ref.query(self.s,'alternatives','F6')
        r=next(r for r in q['records'] if r['original_id']=='HR-F6')
        self.assertIn('partial',json.dumps(r).lower())
        self.assertIn('S03',json.dumps(r))
        self.assertIn('absent',json.dumps(r).lower())
        self.assertEqual(q['boundary']['adoption'],'RETURNED_UNADOPTED')

    def test_stale_handoff_not_live_process(self):
        q=ref.query(self.s,'work-now')
        r=next(r for r in q['records'] if r['original_id']=='HQ_SEALED_R157')
        self.assertEqual(r['currentness'],'STALE_POINTER_PRESERVED')
        self.assertIn('UNKNOWN',r['raw']['local_running_proof_or_unknown'])
        self.assertIn('UNKNOWN',q['process_state'])

    def test_self_review_cannot_promote(self):
        with self.assertRaisesRegex(ValueError,'SELF_REVIEW'):
            ref.permit_promotion(author='a',reviewer='a',appointed=True,source_scope='SOURCEFREE',target_scope='REVIEWED')

    def test_synthetic_cannot_promote_native(self):
        with self.assertRaisesRegex(ValueError,'SYNTHETIC_NATIVE'):
            ref.permit_promotion(author='a',reviewer='b',appointed=True,source_scope='SYNTHETIC',target_scope='NATIVE')
        with self.assertRaisesRegex(ValueError,'NONISSUING'):
            ref.permit_promotion(author='a',reviewer='b',appointed=True,source_scope='NATIVE',target_scope='NATIVE')

    def test_tampered_input_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'input_lock.json').write_text(json.dumps(self.s['input_lock']))
            for x in self.s['input_lock']:
                p=root/x['local'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ref.ROOT/x['local']).read_bytes())
            p=root/self.s['input_lock'][0]['local'];p.write_bytes(p.read_bytes()+b'forged')
            with self.assertRaisesRegex(ValueError,'TAMPER'):ref.validate_inputs(root,False)

    def test_duplicate_manifest_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);locks=copy.deepcopy(self.s['input_lock']);locks[1]=locks[0]
            (root/'input_lock.json').write_text(json.dumps(locks))
            with self.assertRaisesRegex(ValueError,'DUPLICATE'):ref.validate_inputs(root,False)

    def test_exact_blob_mismatch_not_accepted(self):
        p=next(p for p in self.s['source_pins'].values() if p['status']=='VERIFIED')
        wrong={k:p[k] for k in ['cut','path','expected_blob','role']};wrong['expected_blob']='0'*40
        self.assertEqual(ref.check_pin(wrong)['status'],'BLOB_MISMATCH')

    def test_snapshot_tamper_and_ref_mismatch_rejected(self):
        forged=copy.deepcopy(self.s);forged['boundary']['source_native_empirical_pilot']='PASS'
        with self.assertRaisesRegex(ValueError,'TAMPER'):ref.verify(forged)
        # Even rehashing a fabricated edge cannot manufacture a source-grounded reference.
        forged=copy.deepcopy(self.s);next(iter(forged['edges'].values()))['to']='NONEXISTENT'
        forged.pop('snapshot_hash');forged['snapshot_hash']=ref.digest(forged)
        with self.assertRaisesRegex(ValueError,'REPLAY_MISMATCH'):ref.verify(forged)

    def test_absence_unknown_negative_are_first_class(self):
        q=ref.query(self.s,'gaps','N11')
        self.assertTrue(q['records'])
        self.assertIn('NOT',json.dumps(q))
        self.assertEqual(ref.query(self.s,'focus','DOES_NOT_EXIST')['status'],'UNKNOWN_ID')
        for r in q['records']:self.assertIn('science_state',r['maturity'])

    def test_negative_restore_only_exact_dependents_independent_red_survives(self):
        before=ref.regrade(self.s)
        r=self.s['records']['ROW:B:CURRENT_REALIZATION:F1.I03.QUERY']
        pin=next(p for p in r['support_pins'] if self.s['source_pins'][p]['role']=='implementation')
        after=ref.regrade(self.s,[pin])
        changed={k for k in before if before[k]!=after[k]}
        pointer=self.s['source_pins'][pin]
        same={p for p,x in self.s['source_pins'].items() if (x['cut'],x['path'])==(pointer['cut'],pointer['path'])}
        expected={k for k,r in self.s['records'].items() if same & set(r['support_pins'])}
        self.assertIn('ROW:C:SEAMS:W1C-S13',expected)
        self.assertTrue(changed);self.assertEqual(changed,expected)
        red='ROW:G:HISTORICAL_REALIZATIONS:HR-N9C'
        self.assertNotIn(red,changed);self.assertIn('RED',json.dumps(self.s['records'][red]))
        self.assertEqual(ref.regrade(self.s),before)

    def test_all_cli_query_surfaces_real_objects(self):
        for cmd,token in [('focus','N11'),('reverse','N10W'),('code','N2'),('seams','F6'),('gaps','WG0'),('alternatives','F7'),('source','SRC35')]:
            q=ref.query(self.s,cmd,token);self.assertEqual(q['status'],'OK');self.assertTrue(q['records'])
        self.assertTrue(ref.query(self.s,'whole')['coverage'])

    def test_inverse_uses_same_edge_identity(self):
        a=ref.select_edges(self.s,[ref.identity('N9')],direction='forward')
        b=ref.select_edges(self.s,[ref.identity('N10W')],direction='reverse')
        self.assertTrue({e['id'] for e in a}&{e['id'] for e in b})

    def test_code_view_has_exact_pins_and_static_call_scope(self):
        q=ref.query(self.s,'code','N2')
        self.assertTrue(any(e['type']=='AUTHOR_REPORTED_STATIC_CALL_NOT_RUNTIME' for e in q['edges']))
        self.assertTrue(any(p['status']=='VERIFIED' for p in q['source_pins'].values()))
        self.assertIn('read_cut_comparison',q)

    def test_cut_requires_exact_commit_and_version_diff_is_explicit(self):
        with self.assertRaisesRegex(ValueError,'40HEX'):ref.build('main')
        q=ref.changes(self.s,self.s)
        self.assertFalse(q['records']['changed']);self.assertFalse(q['read_cut_comparison']['changed'])
        self.assertTrue(any(p['state']=='ABSENT_AT_SELECTED_CUT' for p in self.s['read_cut_comparison'].values()))

if __name__=='__main__':unittest.main(verbosity=2)
