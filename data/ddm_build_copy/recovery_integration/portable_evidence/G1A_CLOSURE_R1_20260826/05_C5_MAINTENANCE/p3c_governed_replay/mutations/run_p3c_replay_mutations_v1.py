#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,json
from pathlib import Path
from typing import Callable
import psycopg


def run_mutation(dsn:str,name:str,mutate:Callable[[psycopg.Connection],None],assert_sql:str,expected_fragment:str)->dict:
    conn=psycopg.connect(dsn,autocommit=False)
    try:
        conn.execute("SET session_replication_role=replica")
        mutate(conn)
        conn.execute("SET session_replication_role=origin")
        try:
            conn.execute(assert_sql)
        except Exception as e:
            message=str(e)
            ok=expected_fragment.lower() in message.lower()
            conn.rollback()
            return {
                'mutation':name,
                'status':'PASS' if ok else 'FAIL',
                'expected_failure_fragment':expected_fragment,
                'observed_error':message,
                'failure_was_rejected':ok,
            }
        else:
            conn.rollback()
            return {
                'mutation':name,'status':'FAIL','expected_failure_fragment':expected_fragment,
                'observed_error':'NO ERROR: invalid state was accepted','failure_was_rejected':False,
            }
    finally:
        conn.close()


def main()->int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--dsn',required=True)
    ap.add_argument('--section',type=Path,required=True)
    args=ap.parse_args()
    tests=[]
    tests.append(run_mutation(
        args.dsn,'missing_collision_disposition',
        lambda c:c.execute("DELETE FROM p3_adjudication_collision_disposition WHERE adjudication_id='P3ADJ-000038'"),
        "SELECT p3_assert_replay_evidence_closure('P3ADJ-000038')",
        'lacks 1 collision dispositions'))
    tests.append(run_mutation(
        args.dsn,'missing_stronger_boundary_resolution',
        lambda c:c.execute("DELETE FROM p3_adjudication_stronger_boundary_resolution WHERE adjudication_id='P3ADJ-000047' AND ctid IN (SELECT ctid FROM p3_adjudication_stronger_boundary_resolution WHERE adjudication_id='P3ADJ-000047' LIMIT 1)"),
        "SELECT p3_assert_replay_evidence_closure('P3ADJ-000047')",
        'lacks 1 stronger-boundary resolutions'))
    tests.append(run_mutation(
        args.dsn,'missing_pair_obligation_resolution',
        lambda c:c.execute("DELETE FROM p3_adjudication_pair_resolution WHERE adjudication_id='P3ADJ-000001' AND ctid IN (SELECT ctid FROM p3_adjudication_pair_resolution WHERE adjudication_id='P3ADJ-000001' LIMIT 1)"),
        "SELECT p3_assert_replay_evidence_closure('P3ADJ-000001')",
        'leaves 1 baseline pair obligations unresolved'))
    def break_union(c:psycopg.Connection)->None:
        c.execute("""DELETE FROM p3_canonical_family_membership
                     WHERE family_revision_id=(SELECT family_revision_id FROM p3_canonical_family_revision WHERE created_by_adjudication_id='P3ADJ-000009')
                       AND ctid IN (SELECT ctid FROM p3_canonical_family_membership
                                   WHERE family_revision_id=(SELECT family_revision_id FROM p3_canonical_family_revision WHERE created_by_adjudication_id='P3ADJ-000009') LIMIT 1)""")
    tests.append(run_mutation(
        args.dsn,'broken_predecessor_union',break_union,
        "SELECT p3_assert_canonical_promotion_closure('P3ADJ-000009')",
        'canonical revision is not predecessor union disjoint accepts'))
    tests.append(run_mutation(
        args.dsn,'incomplete_split_partition',
        lambda c:c.execute("DELETE FROM p3_adjudication_split_result_member WHERE adjudication_id='P3ADJ-000111' AND ctid IN (SELECT ctid FROM p3_adjudication_split_result_member WHERE adjudication_id='P3ADJ-000111' LIMIT 1)"),
        "SELECT p3_assert_split_result_partition('P3ADJ-000111')",
        'split successor partition invalid'))
    out={
        'status':'PASS' if all(t['status']=='PASS' for t in tests) else 'FAIL',
        'mutation_count':len(tests),
        'passed':sum(t['status']=='PASS' for t in tests),
        'failed':sum(t['status']=='FAIL' for t in tests),
        'database_state_persisted':False,
        'method':'Each mutation ran in a separate transaction with trigger suppression limited to mutation construction; the governed assertion was then invoked explicitly and the transaction rolled back.',
        'mutations':tests,
    }
    outdir=args.section/'mutations';outdir.mkdir(parents=True,exist_ok=True)
    (outdir/'P3C_REPLAY_MUTATION_RETURN.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    with (outdir/'P3C_REPLAY_MUTATION_MATRIX.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['mutation','status','failure_was_rejected','expected_failure_fragment','observed_error'])
        w.writeheader();w.writerows(tests)
    print(json.dumps({k:v for k,v in out.items() if k!='mutations'},indent=2,sort_keys=True))
    return 0 if out['status']=='PASS' else 1

if __name__=='__main__':raise SystemExit(main())
