"""SOROK B3AS-I2 independently authored hostile controls. Frozen before first execution.

External raw SQL is a privileged schema-writer adversary, distinct from an unauthenticated
B2 request. SIGKILL is process-death evidence only. Nothing here authorizes law or adoption.
"""
from pathlib import Path
from copy import deepcopy
import os, sys, json, sqlite3, subprocess, select, signal
import pytest

ROOT = Path(__file__).resolve().parent
CAND = Path(os.environ['I2_CANDIDATE_ROOT'])
sys.path.insert(0, str(CAND))
from integration import Integration, Refusal
from fixture_authority import FixtureAuthority
from developmental_loop import World, permission_for

OUT = Path(os.environ['I2_EVIDENCE'])
OUT.mkdir(parents=True, exist_ok=True)
WORKER = ROOT / 'independent_worker.py'

def frame():
 w = World()
 for t in range(1, 8):
  w.tick(t)
 return w.frame()

def cold(path):
 p = subprocess.run([sys.executable, str(WORKER), 'inspect', str(path)],
                    capture_output=True, text=True, check=True,
                    env=dict(os.environ, I2_CANDIDATE_ROOT=str(CAND)))
 r = json.loads(p.stdout)
 assert r['pid'] != os.getpid() and r['integrity'] == 'ok'
 return r

def rows_equal(a, b):
 return a['tables'] == b['tables']

def existing_rows_unchanged(before, after):
 for table, rows in before['tables'].items():
  assert after['tables'][table] == rows, 'existing rows mutated in ' + table
 for table, rows in after['tables'].items():
  if table not in before['tables']:
   assert rows == [], 'external new table ' + table + ' must stay empty'

def schema_equal(a, b):
 return a['schema'] == b['schema'] and a['metadata'] == b['metadata']

def no_candidate_rows(state):
 return not state['tables']['b3_source'] and not state['tables']['b3_transition']

def subset_rows(before, after):
 for table, rows in before['tables'].items():
  assert set(map(tuple, rows)) <= set(map(tuple, after['tables'][table])), table

def save(name, **kw):
 (OUT / (name + '.json')).write_text(json.dumps(kw, indent=2, default=str) + '\n')

def external(cmd, path, frame_obj=None, sql=None, timeout=30):
 args = [sys.executable, str(WORKER), cmd, str(path)]
 if frame_obj is not None:
  fp = path.parent / (cmd + '_frame.json')
  fp.write_text(json.dumps(frame_obj))
  args.append(str(fp))
 if sql is not None:
  args.append(sql)
 p = subprocess.run(args, capture_output=True, text=True, check=True,
                    env=dict(os.environ, I2_CANDIDATE_ROOT=str(CAND)), timeout=timeout)
 out = json.loads(p.stdout)
 assert out['pid'] != os.getpid()
 return out

def setup(tmp_path, seeded=False):
 f = frame(); a = FixtureAuthority(); a.register_observed(f)
 path = tmp_path / 'public.sqlite'; e = Integration(path, a)
 if seeded:
  other = deepcopy(f)
  other['event']['id'] = 'I2HC-independent-before-request'
  from custody import prepare, admit, participant_from_records
  bundle, _ = prepare(e.bridge.store.state(), other['event'],
                      participant=participant_from_records(other['evidence'], other['event']['time']))
  assert isinstance(admit(e.bridge, bundle)['event_admission'], dict)
 return f, a, e, path


# HC1 -- index created in the late window, independent OS process
@pytest.mark.parametrize('seeded', [False, True])
def test_hc_index_in_late_window(tmp_path, seeded):
 f, a, e, path = setup(tmp_path, seeded)
 before = cold(path); fired = []
 def fault(stage):
  if stage == 'after_target_effect_before_commit':
   out = external('ddl', path, sql='CREATE INDEX i2hc_late_index ON b3_source(body)')
   fired.append(out)
 e.fault = fault
 r = e.run(f); after = cold(path); e.close()
 save('hc1_index_' + str(seeded), before=before, result=r, after=after, fired=fired)
 assert fired and fired[0]['ddl'] == 'COMMITTED'
 assert not schema_equal(before, after)
 assert r['status'] == 'REFUSED', 'late schema-only change escaped the publication readset'
 assert r['code'] in ('PUBLICATION_READSET_CHANGED', 'PUBLICATION_SCHEMA_CHANGED')
 assert r['no_mutation'] is False
 assert rows_equal(before, after)
 assert any(n == 'i2hc_late_index' for t, n, tb, s in after['schema'])
 assert no_candidate_rows(after)
 subset_rows(before, after)


# HC2 -- trigger / view / table / version metadata inside the documented schema contract
@pytest.mark.parametrize('obj', ['trigger', 'view', 'table', 'userversion'])
def test_hc_schema_object_families(tmp_path, obj):
 f, a, e, path = setup(tmp_path, False)
 before = cold(path); fired = []
 statements = {
  'trigger': 'CREATE TRIGGER i2hc_trg AFTER INSERT ON b3_source BEGIN UPDATE b3_audit SET body=body WHERE 0; END',
  'view': 'CREATE VIEW i2hc_view AS SELECT id FROM b3_source',
  'table': 'CREATE TABLE i2hc_tbl (id TEXT PRIMARY KEY)',
  'userversion': 'PRAGMA user_version=7',
 }
 def fault(stage):
  if stage == 'after_target_effect_before_commit':
   fired.append(external('ddl', path, sql=statements[obj]))
 e.fault = fault
 r = e.run(f); after = cold(path); e.close()
 save('hc2_' + obj, before=before, result=r, after=after, fired=fired)
 assert fired and fired[0]['ddl'] == 'COMMITTED'
 assert r['status'] == 'REFUSED'
 assert r['code'] in ('PUBLICATION_READSET_CHANGED', 'PUBLICATION_SCHEMA_CHANGED')
 assert r['no_mutation'] is False, obj + ' change must force no_mutation false'
 existing_rows_unchanged(before, after)
 assert not schema_equal(before, after)
 assert no_candidate_rows(after)


# HC3 -- external trigger immediately before a late domain refusal
def test_hc_late_refusal_with_trigger(tmp_path):
 f, a, e, path = setup(tmp_path, False)
 before = cold(path); fired = []
 def fault(stage):
  if stage == 'after_target_effect_before_commit':
   fired.append(external('ddl', path, sql='CREATE TRIGGER i2hc_refused AFTER INSERT ON b3_source BEGIN UPDATE b3_audit SET body=body WHERE 0; END'))
   raise Refusal('I2HC_LATE_REFUSAL_WITH_TRIGGER')
 e.fault = fault
 r = e.run(f); after = cold(path); e.close()
 save('hc3_refusal_trigger', before=before, result=r, after=after, fired=fired)
 assert fired and fired[0]['ddl'] == 'COMMITTED'
 assert r['status'] == 'REFUSED' and r['code'] == 'I2HC_LATE_REFUSAL_WITH_TRIGGER'
 existing_rows_unchanged(before, after)
 assert not schema_equal(before, after)
 assert r['no_mutation'] is False, 'external schema change before refusal must be reported'
 assert any(n == 'i2hc_refused' for t, n, tb, s in after['schema'])
 assert no_candidate_rows(after)


# HC4 -- concurrent independent B2 fact AND index; no deletion or rollback of foreign state
@pytest.mark.parametrize('seeded', [False, True])
def test_hc_concurrent_fact_and_index(tmp_path, seeded):
 f, a, e, path = setup(tmp_path, seeded)
 before = cold(path); fired = []
 def fault(stage):
  if stage != 'after_target_effect_before_commit':
   return
  other = deepcopy(f)
  other['event']['id'] = 'I2HC-concurrent-B2-objective'
  fired.append(external('ddl_and_admit', path, frame_obj=other,
                        sql='CREATE INDEX i2hc_fact_index ON b3_source(body)'))
 e.fault = fault
 r = e.run(f); after = cold(path); e.close()
 save('hc4_fact_index_' + str(seeded), before=before, result=r, after=after, fired=fired)
 assert fired and fired[0]['ddl'] == 'COMMITTED'
 assert isinstance(fired[0]['result']['event_admission'], dict)
 assert r['status'] == 'REFUSED'
 assert r['code'] in ('PUBLICATION_READSET_CHANGED', 'PUBLICATION_SCHEMA_CHANGED')
 assert r['no_mutation'] is False
 subset_rows(before, after)
 assert after['tables'] != before['tables'], 'independent B2 fact must survive'
 assert no_candidate_rows(after)
 assert any(n == 'i2hc_fact_index' for t, n, tb, s in after['schema'])


# HC5 -- real SIGKILL at scratch/public publication boundaries, cold schema+row inspection
@pytest.mark.parametrize('stage', ['after_target_effect_before_commit',
                                   'after_publication_before_commit',
                                   'after_successful_return'])
@pytest.mark.parametrize('seeded', [False, True])
def test_hc_sigkill_cold_schema_rows(tmp_path, stage, seeded):
 f, a, e, path = setup(tmp_path, seeded)
 e.close(); before = cold(path)
 fp = tmp_path / 'frame.json'; fp.write_text(json.dumps(f))
 proc = subprocess.Popen([sys.executable, str(WORKER), 'kill', str(path), str(fp), stage],
                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True, env=dict(os.environ, I2_CANDIDATE_ROOT=str(CAND)))
 try:
  assert select.select([proc.stdout], [], [], 25)[0], 'worker never reached selected boundary'
  ready = json.loads(proc.stdout.readline())
  assert ready['pid'] == proc.pid and proc.poll() is None
  os.kill(proc.pid, signal.SIGKILL)
  out, err = proc.communicate(timeout=15)
  assert proc.returncode == -signal.SIGKILL
 finally:
  if proc.poll() is None:
   proc.kill(); proc.wait()
 after = cold(path)
 save('hc5_kill_' + stage + '_' + str(seeded), before=before, ready=ready,
      exit_code=proc.returncode, after=after)
 assert ready['pid'] != os.getpid()
 if stage == 'after_successful_return':
  assert after['tables']['b3_transition'] or after['tables']['b3_source']
  subset_rows(before, after)
 else:
  assert schema_equal(before, after), 'SIGKILL at ' + stage + ' left schema drift'
  assert rows_equal(before, after), 'SIGKILL at ' + stage + ' left row drift'
  assert no_candidate_rows(after)


# HC6 -- refused proposal then correct retry; no target/source ghosts
@pytest.mark.parametrize('seeded', [False, True])
def test_hc_refusal_then_retry_no_ghosts(tmp_path, seeded):
 f, a, e, path = setup(tmp_path, seeded)
 before = cold(path)
 bad = deepcopy(f); bad['origin_event_id'] = 'I2HC-never-admitted'
 a.register_observed(bad)
 r1 = e.run(bad); middle = cold(path)
 assert r1['status'] == 'REFUSED' and r1['no_mutation'] is True
 assert rows_equal(before, middle) and schema_equal(before, middle)
 assert no_candidate_rows(middle)
 perm = permission_for([], f)
 r2 = e.run(f, owner_permission=perm, registered_permissions=(perm,))
 final = cold(path); e.close()
 reopened = Integration(path, a)
 replay = reopened.run(f, owner_permission=perm, registered_permissions=(perm,))
 last = cold(path); reopened.close()
 save('hc6_retry_' + str(seeded), before=before, first=r1, middle=middle,
      second=r2, final=final, replay=replay, last=last)
 assert r2['status'] == 'ELIGIBLE_NONCAUSAL'
 assert replay['status'] == 'ELIGIBLE_NONCAUSAL' and replay['exact_replay']
 assert len(final['tables']['b3_source']) == len(last['tables']['b3_source']) == 1
 assert json.loads(final['tables']['b3_source'][0][1])['id'] == f['event']['id']
 final_transitions = [row[0] for row in final['tables']['b3_transition']]
 last_transitions = [row[0] for row in last['tables']['b3_transition']]
 assert len(final_transitions) == len(set(final_transitions)), 'duplicate transition ghosts after retry'
 assert set(last_transitions) == set(final_transitions), 'replay added transition ghosts'
 assert [row[0] for row in final['tables']['b3_source']] == [row[0] for row in last['tables']['b3_source']]
 assert no_candidate_rows(middle) and middle['tables']['b3_source'] == []
 subset_rows(before, final)


# HC7 -- no_mutation semantics across success, repeat, valid-empty, denial and refusals
def test_hc_no_mutation_semantics(tmp_path):
 report = {}
 def scenario(name):
  d = tmp_path / name; d.mkdir(); return d
 d = scenario('s1')
 f, a, e, path = setup(d, False)
 perm = permission_for([], f)
 fresh = e.run(f, owner_permission=perm, registered_permissions=(perm,))
 after_fresh = cold(path)
 repeat = e.run(f, owner_permission=perm, registered_permissions=(perm,))
 after_repeat = cold(path); e.close()
 report['fresh'] = fresh; report['repeat'] = repeat
 d = scenario('s2')
 f2, a2, e2, path2 = setup(d, False)
 p2 = permission_for([], f2)
 e2.run(f2, owner_permission=p2, registered_permissions=(p2,))
 after_target = cold(path2)
 replay = e2.run(f2)
 after_replay = cold(path2); e2.close()
 replay_delta = {t: [row for row in after_replay['tables'][t] if row not in after_target['tables'].get(t, [])]
                 for t in after_replay['tables']}
 replay_delta = {t: rows for t, rows in replay_delta.items() if rows}
 report['replay_after_target'] = replay; report['replay_delta'] = replay_delta
 d = scenario('s3')
 f3, a3, e3, path3 = setup(d, False)
 empty = e3.run(f3); after_empty = cold(path3); e3.close()
 report['empty'] = empty
 d = scenario('s4')
 f4, a4, e4, path4 = setup(d, False)
 denied = e4.run(f4, owner_permission='I2HC-bogus-token', registered_permissions=())
 after_denied = cold(path4); e4.close()
 report['denied'] = denied
 d = scenario('s5')
 f5, a5, e5, path5 = setup(d, False)
 b5 = cold(path5)
 clean_ref = deepcopy(f5); clean_ref['origin_event_id'] = 'I2HC-nope'
 a5.register_observed(clean_ref)
 clean_refusal = e5.run(clean_ref); after_clean = cold(path5); e5.close()
 report['clean_refusal'] = clean_refusal
 d = scenario('s6')
 f6, a6, e6, path6 = setup(d, False)
 def schemafault(stage):
  if stage == 'after_target_effect_before_commit':
   external('ddl', path6, sql='CREATE TABLE i2hc_semantic_marker (id TEXT)')
 e6.fault = schemafault
 schema_refusal = e6.run(f6); after_schema = cold(path6); e6.close()
 report['schema_refusal'] = schema_refusal
 d = scenario('s7')
 f7, a7, e7, path7 = setup(d, False)
 def rowfault(stage):
  if stage == 'after_target_effect_before_commit':
   other = deepcopy(f7); other['event']['id'] = 'I2HC-semantic-external-row'
   external('admit', path7, frame_obj=other)
 e7.fault = rowfault
 row_refusal = e7.run(f7); after_row = cold(path7); e7.close()
 report['row_refusal'] = row_refusal
 save('hc7_semantics', **report,
      states=dict(after_fresh=after_fresh, after_repeat=after_repeat,
                  after_target=after_target, after_replay=after_replay,
                  after_empty=after_empty, after_denied=after_denied,
                  after_clean=after_clean, after_schema=after_schema, after_row=after_row))
 assert fresh['status'] == 'ELIGIBLE_NONCAUSAL' and fresh['owner_effect_committed'] is True
 assert fresh['no_mutation'] is False, 'a request that published rows must not claim no mutation'
 assert repeat['status'] == 'ELIGIBLE_NONCAUSAL' and repeat['exact_replay']
 assert rows_equal(after_fresh, after_repeat), 'identical repeat call must not change state'
 assert replay['status'] == 'ELIGIBLE_NONCAUSAL' and replay['exact_replay']
 assert set(replay_delta) <= {'b3_response'}, 'post-target repeat may only append its own response record'
 assert empty['status'] == 'ELIGIBLE_NONCAUSAL' and empty['owner_effect_committed'] is False
 assert empty['CAN011_transition']['status'] == 'VALID_EMPTY'
 assert empty['no_mutation'] is False, 'valid-empty target still admits the objective event'
 assert denied['status'] == 'ELIGIBLE_NONCAUSAL' and denied['owner_effect_committed'] is False
 assert denied['CAN011_transition']['status'] == 'DENIED'
 assert 'independent_owner_receipt' not in denied
 assert clean_refusal['status'] == 'REFUSED' and clean_refusal['no_mutation'] is True
 assert rows_equal(b5, after_clean)
 assert schema_refusal['status'] == 'REFUSED' and schema_refusal['no_mutation'] is False
 assert row_refusal['status'] == 'REFUSED' and row_refusal['no_mutation'] is False


# HC8 -- no external DDL can commit inside the public BEGIN IMMEDIATE window
def test_hc_no_ddl_inside_immediate(tmp_path):
 f, a, e, path = setup(tmp_path, False)
 before = cold(path); fired = []
 def fault(stage):
  if stage == 'after_publication_before_commit':
   fired.append(external('ddl', path, sql='CREATE TABLE i2hc_inside_window (id TEXT)'))
 e.fault = fault
 r = e.run(f); after = cold(path); e.close()
 save('hc8_inside_immediate', before=before, result=r, after=after, fired=fired)
 assert r['status'] == 'ELIGIBLE_NONCAUSAL'
 assert fired and fired[0]['ddl'] == 'REFUSED', 'external writer bypassed BEGIN IMMEDIATE'
 assert not any(n == 'i2hc_inside_window' for t, n, tb, s in after['schema'])
 assert after['metadata']['user_version'] == before['metadata']['user_version']
 assert after['tables']['b3_source'], 'successful publication expected'
