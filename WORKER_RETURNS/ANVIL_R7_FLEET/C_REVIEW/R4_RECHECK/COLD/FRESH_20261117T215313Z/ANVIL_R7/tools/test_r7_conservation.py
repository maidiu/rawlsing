#!/usr/bin/env python3
"""R7 field-level and executable no-drop checks against R5 and mainMAC-R6.

This does NOT prove authentic historical meanings or independent current consumer parity.
"""
import csv,hashlib,io,json,pathlib,tempfile,unittest,sys
from test_r6 import r6_fixture
from anvil import outputs,check_dir,validate
from impact import calculate
ROOT=pathlib.Path(__file__).resolve().parents[1]
R5=ROOT/'R5_BASELINE';M=ROOT/'MAINMAC_R6_REFERENCE/ANVIL_R6'

class Conservation(unittest.TestCase):
    def test_r5_all_manifest_entries_present_and_byte_identical(self):
        m=json.loads((R5/'MANIFEST.json').read_text());self.assertEqual(44,len(m['payloads']))
        self.assertEqual(45,len([p for p in R5.rglob('*') if p.is_file()]))
        for name,meta in m['payloads'].items():
            orig=R5/name;active=ROOT/name
            self.assertTrue(orig.is_file(),name);self.assertTrue(active.is_file(),name)
            self.assertEqual(meta['sha256'],hashlib.sha256(orig.read_bytes()).hexdigest(),name)
    def test_mainmac_reference_all_payloads_byte_identical(self):
        m=json.loads((M/'MANIFEST.json').read_text());self.assertEqual(33,len(m['files']))
        for name,meta in m['files'].items():
            p=M/name;self.assertTrue(p.is_file(),name)
            h=meta['sha256'] if isinstance(meta,dict) else meta
            self.assertEqual(h,hashlib.sha256(p.read_bytes()).hexdigest(),name)
    def test_mainmac_r7_reference_is_exact_unchanged_evidence(self):
        root=ROOT/'MAINMAC_R7_REFERENCE'
        meta=json.loads((root/'MANIFEST.json').read_text())
        self.assertEqual(108,len(meta['files']))
        for rel,detail in meta['files'].items():
            path=root/rel
            self.assertTrue(path.is_file(),rel)
            self.assertEqual(detail['sha256'],hashlib.sha256(path.read_bytes()).hexdigest(),rel)
            self.assertEqual(detail['bytes'],path.stat().st_size,rel)
    def test_all_r5_six_semantic_projections_still_work(self):
        s=r6_fixture();self.assertEqual([],validate(s))
        fs=outputs(s);self.assertEqual({'DESIGN_DECISION.md','COVERAGE_TO_DECISION.tsv','DOWNSTREAM_BUILD_HANDOFF.jsonl',
            'EVIDENCE_AND_FALSIFIER_INDEX.jsonl','GLOBAL_ARCHITECTURE.json','BOUNDARY_TRACE.json'},set(fs))
        cov=list(csv.DictReader(io.StringIO(fs['COVERAGE_TO_DECISION.tsv'].decode()),delimiter='\t'))
        self.assertEqual(118,len(cov))
        fields={'necessity','status','decision_ids','source_anchor','source_semantics','consumer_or_hold',
                'negative_meaning','architecture_effect','evidence_ids','why'}
        self.assertTrue(fields<=set(cov[0]))
        for r in cov:
            for k in ('source_semantics','consumer_or_hold','negative_meaning','architecture_effect','evidence_ids'):
                self.assertTrue(r[k].strip(),(r['id'],k))
        boundary=json.loads(fs['BOUNDARY_TRACE.json']);self.assertIn('integrated_epistemic_case',boundary)
        self.assertIn('provenance',boundary)
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td);(p/'SPINE.json').write_text(json.dumps(s))
            for name,b in fs.items():(p/name).write_bytes(b)
            self.assertEqual([],check_dir(p))
            (p/'COVERAGE_TO_DECISION.tsv').unlink()
            self.assertTrue(any('PROJECTION_MISSING_OR_CHANGED:COVERAGE_TO_DECISION.tsv' in x for x in check_dir(p)))
    def test_transitive_change_impact_is_still_executable(self):
        s=r6_fixture();res=calculate(s,['C11'],[])
        self.assertEqual('GRAPH_BASED_ADVISORY_NOT_SEMANTIC_CERTIFICATE',res['status'])
        self.assertIn('C11',res['nodes']);self.assertTrue(res['handoffs'])
    def test_preserve_original_r5_six_executable_test_commands(self):
        for script in ('test_r5.py','test_stage.py','test_compare.py','test_anvil.py','test_r4.py','preflight_launches.py'):
            self.assertTrue((ROOT/'tools'/script).is_file(),script)
            self.assertTrue((R5/'tools'/script).is_file(),script)
    def test_r7_not_promoting_historical_nonadopted_proposals(self):
        s=r6_fixture();self.assertEqual([],validate(s))
        self.assertEqual(26,len(s['coverage']['PYAT_PC']))
        self.assertEqual(14,len(s['coverage']['P4R']))
        self.assertEqual(29,len(s['coverage']['K1_CAP']))
        self.assertTrue(all(not x.get('adopted',False) for x in s['coverage']['PYAT_PC'].values()))
        self.assertTrue(all(not x.get('closed',False) for x in s['coverage']['P4R'].values()))

if __name__=='__main__':unittest.main(verbosity=2)
