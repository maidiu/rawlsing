"""B3AS-I2 reviewer-owned process worker. No candidate or frozen-test edits."""
from pathlib import Path
import os, sys, json, sqlite3

def snapshot(path):
 db = sqlite3.connect(path)
 schema = db.execute("SELECT type,name,tbl_name,sql FROM sqlite_master ORDER BY type,name").fetchall()
 tables = {n: db.execute('SELECT * FROM "' + n.replace('"', '""') + '" ORDER BY 1').fetchall()
           for typ, n, tbl, sql in schema if typ == 'table'}
 meta = {name: db.execute('PRAGMA ' + name).fetchone()[0] for name in ('schema_version', 'user_version', 'application_id')}
 integrity = db.execute('PRAGMA integrity_check').fetchone()[0]
 db.close()
 return dict(pid=os.getpid(), integrity=integrity, schema=schema, tables=tables, metadata=meta)

if __name__ == '__main__':
 mode, path = sys.argv[1:3]
 if mode == 'inspect':
  print(json.dumps(snapshot(path))); sys.exit(0)
 sys.path.insert(0, os.environ['I2_CANDIDATE_ROOT'])
 from integration import Integration
 from fixture_authority import FixtureAuthority
 from developmental_loop import permission_for
 from custody import prepare, admit, participant_from_records
 from sources import b2
 if mode == 'ddl':
  conn = sqlite3.connect(path, timeout=0)
  try:
   conn.executescript(sys.argv[3])
   print(json.dumps(dict(pid=os.getpid(), ddl='COMMITTED'))); sys.exit(0)
  except Exception as exc:
   print(json.dumps(dict(pid=os.getpid(), ddl='REFUSED', error=type(exc).__name__ + ': ' + str(exc)))); sys.exit(0)
  finally:
   conn.close()
 frame = json.loads(Path(sys.argv[3]).read_text())
 if mode == 'admit':
  bridge = b2.Bridge(path)
  bundle, _ = prepare(bridge.store.state(), frame['event'],
                      participant=participant_from_records(frame['evidence'], frame['event']['time']))
  result = admit(bridge, bundle); bridge.close()
  print(json.dumps(dict(pid=os.getpid(), result=result))); sys.exit(0)
 if mode == 'ddl_and_admit':
  conn = sqlite3.connect(path, timeout=0)
  try:
   conn.executescript(sys.argv[4]); ddl = 'COMMITTED'
  except Exception as exc:
   ddl = 'REFUSED ' + type(exc).__name__
  finally:
   conn.close()
  bridge = b2.Bridge(path)
  bundle, _ = prepare(bridge.store.state(), frame['event'],
                      participant=participant_from_records(frame['evidence'], frame['event']['time']))
  result = admit(bridge, bundle); bridge.close()
  print(json.dumps(dict(pid=os.getpid(), ddl=ddl, result=result))); sys.exit(0)
 from developmental_loop import permission_for
 authority = FixtureAuthority(); authority.register_observed(frame)
 integ = Integration(path, authority); stage = sys.argv[4]
 def wait(at):
  if at == stage:
   print(json.dumps(dict(pid=os.getpid(), stage=at)), flush=True); sys.stdin.readline()
 integ.fault = wait
 perm = permission_for([], frame)
 result = integ.run(frame, owner_permission=perm, registered_permissions=(perm,))
 if stage == 'after_successful_return':
  print(json.dumps(dict(pid=os.getpid(), stage=stage, result=result)), flush=True); sys.stdin.readline()
 integ.close()
