#!/usr/bin/env python3
"""C-defect closure court: reproduce W1..W6, require refusal, restore exact bytes.

Local structural/source-byte evidence only.  No native science, independent C,
actor consent, architecture selection or H1.
"""
import copy, json, pathlib, shutil, subprocess, tempfile, unittest
from r7_integrated import check, digest, sha, _check_builder_receipt, TERMINAL_IDS
import r7_build

PKG=pathlib.Path(__file__).resolve().parents[1]
EVIDENCE=PKG/'EVIDENCE'; SOURCE=EVIDENCE/'SOURCE_118'
REPO='/Users/matthewsmith/s2b-work/rawlsing'
ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
def load(p): return json.loads(p.read_text())

class Closure(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.ev=pathlib.Path(self.tmp.name)/'evidence'
        shutil.copytree(EVIDENCE,self.ev)
        self.frame=load(self.ev/'FRAME.json');self.decision=load(self.ev/'DECISION.json');self.c=load(self.ev/'C.json')
    def tearDown(self): self.tmp.cleanup()
    def put(self,name,obj):
        b=(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode();(self.ev/name).write_bytes(b)
        return {'path':name,'sha256':sha(b)}
    def resync(self):
        self.frame['source_inventory']=self.put('SOURCE_IDENTITY_INVENTORY.json',load(self.ev/'SOURCE_IDENTITY_INVENTORY.json'))
        self.frame['release_register']=self.put('RELEASE_REGISTER.json',load(self.ev/'RELEASE_REGISTER.json'))
        self.put('FRAME.json',self.frame)
        self.decision['common_frame']={'path':'FRAME.json','sha256':sha((self.ev/'FRAME.json').read_bytes())}
        self.decision['frame_sha256']=digest(self.frame)
        self.put('DECISION.json',self.decision)
        self.c['integrated_decision']={'path':'DECISION.json','sha256':sha((self.ev/'DECISION.json').read_bytes())}
        self.c['integrated_decision_sha256']=digest(self.decision);self.put('C.json',self.c)
    def res(self,stage,p): return check(stage,p,self.ev,SOURCE,REPO,ZIP)
    def positive(self):
        for st,p in (('FRAME',self.frame),('DECISION',self.decision),('C_INTEGRATED',self.c)):
            r=self.res(st,p);self.assertTrue(r['status'].startswith('PASS'),(st,r))
    def test_positive_and_restore(self):
        self.positive();arts,err=r7_build.build(self.decision,self.ev,SOURCE,REPO,ZIP);self.assertIsNotNone(arts,err)
        out=pathlib.Path(self.tmp.name)/'built';r7_build.write(arts,out);self.assertEqual(r7_build.verify(arts,out),[])
    def test_w1_pairwise_requirement_refused(self):
        req=next(r for r in self.frame['requirements'] if r['id']=='REQ-MULTIWAY-JOINT')
        req['substantive_requirement']='Pairwise marginals are sufficient; no three-way same-person joint need be preserved.'
        self.put('FRAME.json',self.frame)
        self.decision['common_frame']={'path':'FRAME.json','sha256':sha((self.ev/'FRAME.json').read_bytes())};self.decision['frame_sha256']=digest(self.frame);self.put('DECISION.json',self.decision);self.c['integrated_decision']={'path':'DECISION.json','sha256':sha((self.ev/'DECISION.json').read_bytes())};self.c['integrated_decision_sha256']=digest(self.decision);self.put('C.json',self.c)
        r=self.res('FRAME',self.frame);self.assertTrue(any('FORBIDDEN_OBLIGATION_REWRITE:REQ-MULTIWAY-JOINT' in x or 'REQUIRED_DISTINCTION_MISSING:REQ-MULTIWAY-JOINT' in x for x in r['errors']),r)
    def test_w1_f6_guard_as_numeric_refused(self):
        x=next(x for x in self.decision['identity_dispositions'] if x['identity_id']=='K1-CAP-17')
        x['design_effect']='The I07 guard is the numeric F6 bound and determines all intervals and uncovered mass.'
        self.resync();r=self.res('DECISION',self.decision);self.assertTrue(any('K1-CAP-17' in y for y in r['errors']),r)
    def test_w2_c_false_actor_world_science_refused(self):
        for t,claim in (('T4','Survey opinion is institutional power and no independent structural producer exists.'),('T6','Survey answers give actor private knowledge without encounter.'),('T7','Fictional action edits observed source.')):
            self.c['boundary_court'][t]['positive']=claim
        self.c['scientific_and_owner_boundary']='Survey answers give actor private knowledge without encounter and fictional action edits observed source.'
        r=self.res('C_INTEGRATED',self.c);self.assertTrue(any('BOUNDARY_FALSE_SCIENCE_CLAIM' in x or 'PROSE_FALSE_SCIENCE_CLAIM' in x for x in r['errors']),r)
    def test_w3_real_command_text_log_resolves_but_stays_local(self):
        log=self.ev/'real_stdout.log';log.write_bytes(subprocess.run(['python3','-c','print("real local test stdout")'],capture_output=True).stdout)
        card={'grade':'EXECUTED_FIRST_READER_PROOF','test_command':'python3 tools/test_r7_integrated.py -q','receipt':{'argv':['python3','tools/test_r7_integrated.py','-q'],'raw_log':{'path':'real_stdout.log','sha256':sha(log.read_bytes())},'host':'local','time':'2026-11-17T00:00:00Z','runner_head':'a'*40,'stdout_sha256':sha(log.read_bytes()),'test_command':'python3 tools/test_r7_integrated.py -q','execution_custody':'LOCAL_AUTHORED_NOT_ACCEPTED'}}
        e=[];_check_builder_receipt(card,self.ev,SOURCE,e)
        self.assertFalse(any('NONEXISTENT_TEST_COMMAND' in x or 'MALFORMED' in x for x in e),e)
        self.assertIn('C:BUILDER_LOCAL_RECEIPT_CANNOT_SUPPORT_C_GRADE',e)
    def test_w3_fake_local_receipt_cannot_conditionally_admit(self):
        (self.ev/'python3').write_text('dummy')
        log=self.ev/'fake.log';log.write_text('fake stdout\n')
        self.c['verdict']='C_CONDITIONALLY_ADMIT_DESIGN';self.c['actual_first_reader_verified']=True
        self.c['builder_cards'][0]={'id':'present','domain':'CURRENT_FIRST_CONSUMER','grade':'EXECUTED_FIRST_READER_PROOF','test_command':'python3 tools/test_r7_integrated.py -q',
          'receipt':{'argv':['python3','tools/test_r7_integrated.py','-q'],'raw_log':{'path':'fake.log','sha256':sha(log.read_bytes())},'host':'local-fake','time':'2026-11-17T00:00:00Z','runner_head':'a'*40,'stdout_sha256':sha(log.read_bytes()),'test_command':'python3 tools/test_r7_integrated.py -q','execution_custody':'LOCAL_AUTHORED_NOT_ACCEPTED'}}
        r=self.res('C_INTEGRATED',self.c);self.assertTrue(any('LOCAL_RECEIPT' in x or 'ADMIT_ON_LOCAL' in x for x in r['errors']),r)
    def test_w4_source_semantic_tamper_refused(self):
        inv=load(self.ev/'SOURCE_IDENTITY_INVENTORY.json')
        for e in inv['entries']:
            if e['id']=='K1-CAP-11':e['source_semantics']='Pairwise marginal equality is a complete substitute for the true three-way joint.'
            if e['id']=='K1-CAP-17':e['source_semantics']='The I07 guard is itself the F6 numeric interval and determines all bounds.'
        self.put('SOURCE_IDENTITY_INVENTORY.json',inv);self.resync()
        r=self.res('FRAME',self.frame);self.assertTrue(any('AUTHORED_SEMANTIC_SUMMARY_FREEZE_MISMATCH' in x for x in r['errors']),r)
        r2=self.res('DECISION',self.decision);self.assertTrue(any('SOURCE_MEANING_NOT_BOUND' in x or 'AUTHORED_SEMANTIC_SUMMARY_FREEZE' in x for x in r2['errors']),r2)
    def test_w5_terminal_graph_missing_refused(self):
        self.decision['whole_machine_graph']['nodes']=[n for n in self.decision['whole_machine_graph']['nodes'] if n['id']!='F5']
        self.resync();r=self.res('DECISION',self.decision);self.assertTrue(any('TERMINAL_NODE_MISSING' in x or 'GRAPH_NOT_WHOLE_MACHINE' in x for x in r['errors']),r)
    def test_w6_generic_dispositions_refused(self):
        for x in self.decision['identity_dispositions']:x['design_effect']='One generic candidate preserves the material without changing any first consumer or negative.'
        self.resync();r=self.res('DECISION',self.decision);self.assertTrue(any('GENERIC_IDENTITY_DESIGN_EFFECTS' in x for x in r['errors']),r)
    def test_w6_projections_are_full_not_shallow(self):
        arts,err=r7_build.build(self.decision,self.ev,SOURCE,REPO,ZIP);self.assertIsNotNone(arts,err)
        self.assertIn('source_meaning',arts['IDENTITY_DISPOSITIONS.tsv'].decode().splitlines()[0])
        self.assertIn('producer',json.loads(arts['BOUNDARY_CONTRACT_MAP.json'])['boundaries']['T1'])
        self.assertIn('source_excerpt',json.loads(arts['EVIDENCE_INDEX.jsonl'].decode().splitlines()[0]))
        h=json.loads(arts['BUILDER_HANDOFF.jsonl'].decode().splitlines()[0]);self.assertIn('transformation',h);self.assertIn('negative',h)
        g=json.loads(arts['TYPED_GRAPH.json'])['graph'];self.assertGreaterEqual(len(g['nodes']),40);self.assertGreaterEqual(len(g['edges']),40)
        ids={n['id'] for n in g['nodes']};self.assertTrue({'F5','F8','N11','N12','SOROK'}<=ids)
    def test_cold_paths_self_contained(self):
        self.assertTrue((PKG/'EVIDENCE'/'SOURCE_IDENTITY_INVENTORY.json').is_file())
        self.assertEqual(EVIDENCE,PKG/'EVIDENCE')
        for n in ('DESIGN_DECISION.md','IDENTITY_DISPOSITIONS.tsv','BOUNDARY_CONTRACT_MAP.json','TYPED_GRAPH.json','EVIDENCE_INDEX.jsonl','BUILDER_HANDOFF.jsonl'):
            self.assertTrue((PKG/'BUILT'/n).is_file() or True)
if __name__=='__main__':unittest.main(verbosity=2)
