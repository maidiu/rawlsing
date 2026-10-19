"""Reviewer-owned process worker. No candidate edits, no author scratch state."""
from pathlib import Path
import os,sys,json,sqlite3

def snapshot(path):
 db=sqlite3.connect(path)
 schema=db.execute("SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name").fetchall()
 tables={n:db.execute('SELECT * FROM "'+n.replace('"','""')+'" ORDER BY 1').fetchall() for typ,n,tbl,sql in schema if typ=='table'}
 integrity=db.execute('PRAGMA integrity_check').fetchone()[0];db.close()
 return dict(pid=os.getpid(),integrity=integrity,schema=schema,tables=tables)

if __name__=='__main__':
 mode,path=sys.argv[1:3]
 if mode=='inspect':print(json.dumps(snapshot(path)));sys.exit()
 sys.path.insert(0,os.environ['REVIEW_B3_ROOT'])
 from integration import Integration
 from fixture_authority import FixtureAuthority
 from custody import prepare,admit,participant_from_records
 from sources import b2
 f=json.loads(Path(sys.argv[3]).read_text())
 if mode=='admit':
  bridge=b2.Bridge(path)
  bundle,_=prepare(bridge.store.state(),f['event'],participant=participant_from_records(f['evidence'],f['event']['time']))
  result=admit(bridge,bundle);bridge.close();print(json.dumps(dict(pid=os.getpid(),result=result)));sys.exit()
 from developmental_loop import permission_for
 a=FixtureAuthority();a.register_observed(f);e=Integration(path,a);stage=sys.argv[4]
 def wait(at):
  if at==stage:
   print(json.dumps(dict(pid=os.getpid(),stage=at)),flush=True);sys.stdin.readline()
 e.fault=wait;p=permission_for([],f)
 result=e.run(f,owner_permission=p,registered_permissions=(p,))
 if stage=='after_successful_return':
  print(json.dumps(dict(pid=os.getpid(),stage=stage,result=result)),flush=True);sys.stdin.readline()
 e.close()
