#!/usr/bin/env python3
"""Integrated positive/mutation/restore suite for the repaired instrument.

Local structural and exact-byte checks only.  These tests do not create native
source science, an independent C, actor rights, architecture adoption or H1.
"""
import copy, json, pathlib, shutil, tempfile, unittest
from r7_integrated import check, digest, sha
from r7_inventory import check_inventory
import r7_build

PKG=pathlib.Path(__file__).resolve().parents[1]
RETURN=PKG.parents[1]
EVIDENCE=RETURN/'EVIDENCE'; SOURCE=EVIDENCE/'SOURCE_118'
REPO='/Users/matthewsmith/s2b-work/rawlsing'
ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'

def load(p): return json.loads(p.read_text())
class Strict(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.ev=pathlib.Path(self.tmp.name)/'evidence'
        shutil.copytree(EVIDENCE,self.ev)
        self.frame=load(self.ev/'FRAME.json'); self.decision=load(self.ev/'DECISION.json'); self.c=load(self.ev/'C.json')
        self.base={n:(self.ev/n).read_bytes() for n in ('FRAME.json','DECISION.json','C.json','SOURCE_IDENTITY_INVENTORY.json','RELEASE_REGISTER.json')}
    def tearDown(self): self.tmp.cleanup()
    def put(self,name,obj):
        b=(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode(); (self.ev/name).write_bytes(b)
        return {'path':name,'sha256':sha(b)}
    def resync(self):
        # refresh inventory/release pointers, then frame pointer + digest in decision
        inv=load(self.ev/'SOURCE_IDENTITY_INVENTORY.json'); self.frame['source_inventory']=self.put('SOURCE_IDENTITY_INVENTORY.json',inv)
        rel=load(self.ev/'RELEASE_REGISTER.json'); self.frame['release_register']=self.put('RELEASE_REGISTER.json',rel)
        self.put('FRAME.json',self.frame); self.decision['common_frame']={'path':'FRAME.json','sha256':sha((self.ev/'FRAME.json').read_bytes())}
        self.decision['frame_sha256']=digest(self.frame)
        self.put('DECISION.json',self.decision); self.c['integrated_decision']={'path':'DECISION.json','sha256':sha((self.ev/'DECISION.json').read_bytes())}
        self.c['integrated_decision_sha256']=digest(self.decision); self.put('C.json',self.c)
    def result(self,stage,packet):
        return check(stage,packet,self.ev,SOURCE,REPO,ZIP)
    def assertPass(self):
        for st,p in (('FRAME',self.frame),('DECISION',self.decision),('C_INTEGRATED',self.c)):
            r=self.result(st,p); self.assertTrue(r['status'].startswith('PASS'),(st,r))
    def test_positive_and_restore(self):
        self.assertPass()
        arts,err=r7_build.build(self.decision,self.ev,SOURCE,REPO,ZIP); self.assertIsNotNone(arts,err)
        out=pathlib.Path(self.tmp.name)/'built'; r7_build.write(arts,out); self.assertEqual(r7_build.verify(arts,out),[])
    def test_synthetic_spine_cannot_replace_inventory(self):
        bad=copy.deepcopy(self.frame); bad.pop('source_inventory'); bad['historical_source_spine']=self.put('fake.json',{'schema':'ANVIL_SPINE_R6','coverage':{}})
        r=self.result('FRAME',bad); self.assertIn('FRAME:NO_SOURCE_IDENTITY_INVENTORY',r['errors'])
    def test_k3_row_mutation_red(self):
        inv=load(self.ev/'SOURCE_IDENTITY_INVENTORY.json')
        for e in inv['entries']:
            if e['id']=='K1-CAP-01': e['source_excerpt']=e['source_excerpt'].replace('\t','X',1)
        self.put('SOURCE_IDENTITY_INVENTORY.json',inv); self.resync()
        r=self.result('FRAME',self.frame); self.assertTrue(any('ROW_BYTES_CHANGED' in x or 'ROW_NOT_IN_SOURCE' in x or 'EXCERPT_NOT_IN_SOURCE' in x for x in r['errors']),r)
    def test_requirement_deleted_red(self):
        bad=copy.deepcopy(self.frame); bad['requirements']=[r for r in bad['requirements'] if r['id']!='REQ-MULTIWAY-JOINT']
        r=self.result('FRAME',bad); self.assertIn('FRAME:REQUIREMENT_ROSTER_DRIFT',r['errors'])
    def test_revoked_release_red(self):
        rel=load(self.ev/'RELEASE_REGISTER.json'); rel['revoked']=[{'sha256':'526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332'}]
        self.put('RELEASE_REGISTER.json',rel); self.resync()
        r=self.result('FRAME',self.frame); self.assertTrue(any('REVOKED' in x or 'RELEASE' in x for x in r['errors']),r)
    def test_actor_firewall_red(self):
        bad=copy.deepcopy(self.decision); bad['actor_world_boundary']['survey_implies_actor_knowledge']=True
        r=self.result('DECISION',bad); self.assertIn('DECISION:ACTOR_WORLD_FIREWALL_BREACH:survey_implies_actor_knowledge',r['errors'])
    def test_fabricated_h1_red(self):
        bad=copy.deepcopy(self.decision); bad['h1_received_by_local_check']=True
        r=self.result('DECISION',bad); self.assertIn('DECISION:LOCAL_H1_CLAIM',r['errors'])
    def test_missing_identity_disposition_red(self):
        bad=copy.deepcopy(self.decision); bad['identity_dispositions']=[x for x in bad['identity_dispositions'] if x['identity_id']!='F5']
        r=self.result('DECISION',bad); self.assertIn('DECISION:INCOMPLETE_118_IDENTITY_RECONCILIATION',r['errors'])
    def test_prospective_adoption_red(self):
        bad=copy.deepcopy(self.decision)
        for x in bad['identity_dispositions']:
            if x['identity_id']=='PYAT-PC-R9-01': x['adopted_by_this_decision']=True
        r=self.result('DECISION',bad); self.assertIn('DECISION:PROSPECTIVE_ADOPTION:PYAT-PC-R9-01',r['errors'])
    def test_boundary_negative_missing_red(self):
        bad=copy.deepcopy(self.c); bad['boundary_court']['T4'].pop('negative',None)
        r=self.result('C_INTEGRATED',bad); self.assertIn('C:BOUNDARY_MISSING_NEGATIVE:T4',r['errors'])
    def test_builder_command_missing_red(self):
        bad=copy.deepcopy(self.c); bad['builder_cards'][0]={'id':'present','domain':'CURRENT_FIRST_CONSUMER','grade':'EXECUTED_FIRST_READER_PROOF',
            'test_command':'does_not_exist_runner.py --x',
            'receipt':{'argv':['does_not_exist_runner.py'],'raw_log':self.put('raw.log',{'x':1}),'host':'local','time':'2026-11-17T00:00:00Z','runner_head':'a'*40,'stdout_sha256':'b'*64,'test_command':'does_not_exist_runner.py --x'}}
        r=self.result('C_INTEGRATED',bad); self.assertTrue(any('NONEXISTENT_TEST_COMMAND' in x or 'C:BUILDER' in x for x in r['errors']),r)
    def test_zip_member_forgery_red(self):
        bad=copy.deepcopy(self.frame)
        bad['requirements'][0]['evidence']=dict(bad['requirements'][0]['evidence'],zip_member='ANVIL_R7/00_R7_READ_FIRST.md')
        r=self.result('FRAME',bad); self.assertTrue(any('ZIP_MEMBER_BYTES_OR_QUOTE_DISAGREE' in x for x in r['errors']),r)
    def test_restore_after_mutations(self):
        self.frame=load(self.ev/'FRAME.json'); self.decision=load(self.ev/'DECISION.json'); self.c=load(self.ev/'C.json')
        self.assertPass()
if __name__=='__main__': unittest.main(verbosity=2)
