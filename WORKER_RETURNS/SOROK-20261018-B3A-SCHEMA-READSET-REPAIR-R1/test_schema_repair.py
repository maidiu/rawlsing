"""Repair-author regressions extending the unchanged two independent falsifiers."""
from pathlib import Path
import sys,os,sqlite3,json
import pytest
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'frozen_review'))
from test_reviewer_hostiles import setup,save,cold,stable
from integration import Integration,Refusal

@pytest.mark.parametrize('change',['index','view','trigger','schema_version','user_version','application_id','quoted_table','schema_aba'])
def test_schema_or_metadata_race_preserves_existing_facts_and_refuses(tmp_path,change):
 f,a,e,path=setup(tmp_path,True);before=cold(path);fired=[]
 def fault(stage):
  if stage!='after_target_effect_before_commit':return
  with sqlite3.connect(path) as db:
   if change=='index':db.execute('CREATE INDEX repair_external_index ON b3_source(body)')
   elif change=='view':db.execute('CREATE VIEW repair_external_view AS SELECT id FROM b3_source')
   elif change=='trigger':db.execute('CREATE TRIGGER repair_external_trigger AFTER INSERT ON b3_source BEGIN SELECT 1; END')
   elif change=='schema_version':db.execute('PRAGMA schema_version = 700')
   elif change=='user_version':db.execute('PRAGMA user_version = 701')
   elif change=='application_id':db.execute('PRAGMA application_id = 702')
   elif change=='quoted_table':db.execute('CREATE TABLE "external audit" (id TEXT PRIMARY KEY)')
   else:
    db.execute('CREATE INDEX repair_transient_index ON b3_source(body)');db.execute('DROP INDEX repair_transient_index')
  fired.append(stage)
 e.fault=fault;r=e.run(f);after=cold(path);metadata=e._database_snapshot();e.close();save('repair_race_'+change,before=before,result=r,after=after,metadata=metadata)
 assert fired and r['status']=='REFUSED' and r['code']=='PUBLICATION_READSET_CHANGED' and r['no_mutation'] is False
 for table,rows in before['tables'].items():assert after['tables'][table]==rows
 assert not after['tables']['b3_source'] and not after['tables']['b3_transition']

@pytest.mark.parametrize('change',['index','user_version'])
def test_external_metadata_after_domain_refusal_reports_mutation(tmp_path,change):
 f,a,e,path=setup(tmp_path,True);before=cold(path)
 def fault(stage):
  if stage=='after_target_effect_before_commit':
   with sqlite3.connect(path) as db:db.execute('CREATE INDEX refusal_index ON b3_source(body)' if change=='index' else 'PRAGMA user_version = 17')
   raise Refusal('REPAIR_LATE_REFUSAL')
 e.fault=fault;r=e.run(f);after=cold(path);e.close();save('repair_refusal_'+change,before=before,result=r,after=after)
 assert r['status']=='REFUSED' and not r['no_mutation'] and not r['owner_effect_committed']
 assert before['tables']==after['tables']


def test_private_schema_change_cannot_publish_rows(tmp_path,monkeypatch):
 f,a,e,path=setup(tmp_path,True);before=cold(path);original=Integration._run
 def changed(self,*args,**kwargs):
  result=original(self,*args,**kwargs);self.db.execute('CREATE INDEX private_schema_drift ON b3_source(body)');return result
 monkeypatch.setattr(Integration,'_run',changed);r=e.run(f);after=cold(path);e.close();save('repair_private_schema',before=before,result=r,after=after)
 assert r['status']=='REFUSED' and r['code']=='PUBLICATION_SCHEMA_CHANGED' and r['no_mutation'] and stable(after)==stable(before)


def test_rolled_back_external_ddl_does_not_falsely_refuse(tmp_path):
 f,a,e,path=setup(tmp_path);before=cold(path)
 def fault(stage):
  if stage=='after_target_effect_before_commit':
   db=sqlite3.connect(path);db.execute('BEGIN IMMEDIATE');db.execute('CREATE INDEX rolled_back_index ON b3_source(body)');db.rollback();db.close()
 e.fault=fault;r=e.run(f);after=cold(path);e.close();save('repair_ddl_rollback',before=before,result=r,after=after)
 assert r['status']=='ELIGIBLE_NONCAUSAL' and before['schema']==after['schema']


def test_snapshot_keeps_existing_transaction_uncommitted(tmp_path):
 f,a,e,path=setup(tmp_path);before=cold(path);assert not e.db.in_transaction
 e._database_snapshot();assert not e.db.in_transaction
 e.db.execute('BEGIN IMMEDIATE');e.db.execute('INSERT INTO b3_clock VALUES (991)');seen=e._database_snapshot()
 assert e.db.in_transaction and seen['tables']['b3_clock']==[(991,)]
 # A separate process still cannot see the uncommitted row.
 during=cold(path);assert during['tables']['b3_clock']==[]
 e.db.execute('ROLLBACK');e.close();after=cold(path);save('repair_snapshot_transaction',before=before,during=during,after=after)
 assert stable(after)==stable(before)
