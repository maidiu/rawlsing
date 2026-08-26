#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,re
from collections import Counter,defaultdict
from pathlib import Path
from typing import Any
import psycopg

FINAL='P3-AUTHORITY-2026-08-02-R184'

def cjson(v:Any)->str:return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(v:Any)->str:return hashlib.sha256((v if isinstance(v,str) else cjson(v)).encode()).hexdigest()
def read_csv(p:Path):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--dsn',required=True);ap.add_argument('--section',type=Path,required=True);args=ap.parse_args()
    sec=args.section
    expected=defaultdict(set)
    for r in read_csv(sec/'inputs/P3C_EVIDENCE_FIRST_MEMBER_MAP.csv'):
        expected[r['final_canonical_family_id']].add(r['member_object_id'])
    checks=[]
    def ck(name:str,ok:bool,actual:Any=None,expected_value:Any=None,note:str=''):
        checks.append({'check':name,'status':'PASS' if ok else 'FAIL','actual':actual,'expected':expected_value,'note':note})
    with psycopg.connect(args.dsn) as conn:
        q=lambda sql,p=():conn.execute(sql,p).fetchone()[0]
        decisions=q('select count(*) from p3_adjudication_decision'); ck('decision_count',decisions==143,decisions,143)
        accepted=q("select count(*) from p3_adjudication_decision where decision_status in ('ACCEPTED_CANONICAL','ACCEPTED_WITH_VARIANTS')");ck('accepted_count',accepted==142,accepted,142)
        splits=q("select count(*) from p3_adjudication_decision where decision_status='SPLIT_REQUIRED'");ck('split_count',splits==1,splits,1)
        families=q('select count(*) from p3_canonical_family');ck('family_count',families==111,families,111)
        revisions=q('select count(*) from p3_canonical_family_revision');ck('family_revision_count',revisions==142,revisions,142)
        obligations=q('select count(*) from p3_closure_obligation');open_n=q("select count(*) from p3_closure_obligation where status='OPEN'");res_n=q("select count(*) from p3_adjudication_pair_resolution")
        ck('obligation_count',obligations==345,obligations,345);ck('no_open_obligations',open_n==0,open_n,0);ck('resolution_row_count',res_n==345,res_n,345)
        ck('collision_dispositions',q('select count(*) from p3_adjudication_collision_disposition')==2,q('select count(*) from p3_adjudication_collision_disposition'),2)
        ck('stronger_boundary_resolutions',q('select count(*) from p3_adjudication_stronger_boundary_resolution')==10,q('select count(*) from p3_adjudication_stronger_boundary_resolution'),10)
        ck('all_candidates_decided',q("select count(*) from p3_candidate_revision_current_stage where lifecycle_stage<>'DECIDED'")==0,q("select count(*) from p3_candidate_revision_current_stage where lifecycle_stage<>'DECIDED'"),0)
        ck('candidate_count_including_successors',q('select count(*) from p3_candidate_revision')==143,q('select count(*) from p3_candidate_revision'),143)
        ck('complete_signatures',q("select count(*) from p3_canonical_family_revision f join p3_proposition_signature s on s.signature_id=f.canonical_signature_id left join (select signature_id,count(*) n from p3_signature_field group by 1)x using(signature_id) where s.signature_status<>'COMPLETE' or coalesce(x.n,0)<>12")==0,q("select count(*) from p3_canonical_family_revision f join p3_proposition_signature s on s.signature_id=f.canonical_signature_id left join (select signature_id,count(*) n from p3_signature_field group by 1)x using(signature_id) where s.signature_status<>'COMPLETE' or coalesce(x.n,0)<>12"),0)
        ck('rule_exclusion_each_revision',q("select count(*) from p3_canonical_family_revision f where not exists(select 1 from p3_family_exclusion e where e.owner_object_id=f.canonical_family_id and e.exclusion_type='RULE_BASED' and e.authority_release_id=f.authority_release_id)")==0,q("select count(*) from p3_canonical_family_revision f where not exists(select 1 from p3_family_exclusion e where e.owner_object_id=f.canonical_family_id and e.exclusion_type='RULE_BASED' and e.authority_release_id=f.authority_release_id)"),0)
        ck('no_variant_value_portability',q("select count(*) from p3_family_variant_revision where value_portability_status<>'NOT_AUTHORIZED_BY_P3'")==0,q("select count(*) from p3_family_variant_revision where value_portability_status<>'NOT_AUTHORIZED_BY_P3'"),0)
        ck('runtime_pointer_final',q('select promoted_release_id from p3_runtime_promotion_pointer')==FINAL,q('select promoted_release_id from p3_runtime_promotion_pointer'),FINAL)
        ck('final_lineage_snapshot_count',q('select count(*) from p3_lineage_disposition where authority_release_id=%s',(FINAL,))==13526,q('select count(*) from p3_lineage_disposition where authority_release_id=%s',(FINAL,)),13526)
        dist=dict(conn.execute('select disposition_status,count(*) from p3_lineage_disposition where authority_release_id=%s group by 1',(FINAL,)).fetchall())
        ck('final_lineage_partition',dist=={'CANONICAL_MEMBER':397,'CONSTRAINT_ONLY_PRESERVED':2897,'SOURCE_LOCAL_SINGLETON_PRESERVED':10232},dist,{'CANONICAL_MEMBER':397,'CONSTRAINT_ONLY_PRESERVED':2897,'SOURCE_LOCAL_SINGLETON_PRESERVED':10232})
        # Latest canonical membership exactness.
        actual=defaultdict(set)
        for fam,m in conn.execute('''with latest as(select distinct on(canonical_family_id) canonical_family_id,family_revision_id from p3_canonical_family_revision order by canonical_family_id,revision_number desc) select canonical_family_id,member_object_id from latest join p3_canonical_family_membership using(family_revision_id)'''):
            actual[fam].add(m)
        ck('latest_family_map_exact',dict(actual)==dict(expected),sha({k:sorted(v) for k,v in sorted(actual.items())}),sha({k:sorted(v) for k,v in sorted(expected.items())}))
        overlaps=q('''with latest as(select distinct on(canonical_family_id) canonical_family_id,family_revision_id from p3_canonical_family_revision order by canonical_family_id,revision_number desc) select count(*) from(select m.member_object_id from latest l join p3_canonical_family_membership m using(family_revision_id) group by m.member_object_id having count(*)>1)x''')
        ck('no_latest_membership_overlap',overlaps==0,overlaps,0)
        duplicate_sets=q('''with latest as(select distinct on(canonical_family_id) canonical_family_id,family_revision_id from p3_canonical_family_revision order by canonical_family_id,revision_number desc), sets as(select canonical_family_id,array_agg(member_object_id order by member_object_id) s from latest join p3_canonical_family_membership using(family_revision_id) group by canonical_family_id) select count(*) from(select s from sets group by s having count(*)>1)x''')
        ck('no_duplicate_exact_family_sets',duplicate_sets==0,duplicate_sets,0)
        # Split and special candidate proofs.
        split_rows=conn.execute("select result_ordinal,successor_candidate_family_id,array_agg(member_object_id order by member_object_id) from p3_adjudication_split_result join p3_adjudication_split_result_member using(adjudication_id,result_ordinal) where adjudication_id=(select adjudication_id from p3_adjudication_decision where candidate_revision_id='P3CANDREV-000252-R0002') group by 1,2 order by 1").fetchall()
        ck('candidate252_exact_split',len(split_rows)==2 and split_rows[0][1]=='P3CAND-000424' and split_rows[1][1]=='P3CAND-000425' and sum(len(r[2]) for r in split_rows)==2,split_rows,'two disjoint singleton successors 424/425')
        c264=dict(conn.execute("select member_object_id,member_disposition from p3_adjudication_decision join p3_adjudication_member using(adjudication_id) where candidate_revision_id='P3CANDREV-000264-R0002'").fetchall())
        ck('candidate264_direct_constructed_boundary',Counter(c264.values())==Counter({'ALREADY_CANONICAL':3,'EXCLUDE':1}),Counter(c264.values()),Counter({'ALREADY_CANONICAL':3,'EXCLUDE':1}))
        c273=dict(conn.execute("select member_object_id,member_disposition from p3_adjudication_decision join p3_adjudication_member using(adjudication_id) where candidate_revision_id='P3CANDREV-000273-R0002'").fetchall())
        ck('candidate273_append_only_extension',Counter(c273.values())==Counter({'ALREADY_CANONICAL':2,'ACCEPT':1}),Counter(c273.values()),Counter({'ALREADY_CANONICAL':2,'ACCEPT':1}))
        ck('candidate273_is_business_management',q("select canonical_family_id from p3_adjudication_decision where candidate_revision_id='P3CANDREV-000273-R0002'")=='JFAM-000219',q("select canonical_family_id from p3_adjudication_decision where candidate_revision_id='P3CANDREV-000273-R0002'"),'JFAM-000219')
        # Release chain and event lifecycle.
        broken_chain=q("select count(*) from p3_authority_release r where r.release_id like 'P3-AUTHORITY-2026-08-02-R%%' and r.release_id<>'P3-AUTHORITY-2026-08-02-R41' and r.parent_release_id is null")
        ck('release_parent_chain_nonnull',broken_chain==0,broken_chain,0)
        bad_events=q("select count(*) from(select release_id,count(*) n,count(*) filter(where status='PROMOTED') promoted from p3_release_status_event where release_id like 'P3-AUTHORITY-2026-08-02-R%%' group by release_id having count(*)<>4 or count(*) filter(where status='PROMOTED')<>1)x")
        ck('decision_release_lifecycle_exact',bad_events==0,bad_events,0)
        ck('variant_promotions_present',q('select count(*) from p3_variant_promotion')>0,q('select count(*) from p3_variant_promotion'),'>0')
        ck('variant_promotion_one_to_one',q('select count(*) from(select canonical_variant_revision_id from p3_variant_promotion group by 1 having count(*)<>1)x')==0,q('select count(*) from(select canonical_variant_revision_id from p3_variant_promotion group by 1 having count(*)<>1)x'),0)
        ck('named_boundary_surface',q("select count(*) from p3_family_exclusion where exclusion_type='NAMED_MEMBER'")>=11,q("select count(*) from p3_family_exclusion where exclusion_type='NAMED_MEMBER'"),'>=11')
        # Release accounting and deterministic reconstruction controls.
        release_rows=list(conn.execute("""select release_id,parent_release_id,input_manifest_hash,validation_return_hash,created_at
                                         from p3_authority_release
                                         where release_id ~ '^P3-AUTHORITY-2026-08-02-R(4[1-9]|[5-9][0-9]|1[0-7][0-9]|18[0-4])$'"""))
        release_rows.sort(key=lambda r:int(r[0].rsplit('R',1)[1]))
        chain_ok=len(release_rows)==144 and release_rows[0][1]=='P3-AUTHORITY-2026-08-01-R40' and all(release_rows[i][1]==release_rows[i-1][0] for i in range(1,len(release_rows)))
        ck('release_parent_chain_exact',chain_ok,len(release_rows),144)
        placeholder=lambda h: len(set(str(h)))==1
        ck('no_release_hash_placeholders',all(not placeholder(r[2]) and not placeholder(r[3]) for r in release_rows),sum(placeholder(r[2]) or placeholder(r[3]) for r in release_rows),0)
        ck('validation_hash_unique_per_release',len({str(r[3]) for r in release_rows})==144,len({str(r[3]) for r in release_rows}),144)
        ck('contract_release_timestamp_deterministic',str(release_rows[0][4])=='2026-08-02 11:59:59+00:00',str(release_rows[0][4]),'2026-08-02 11:59:59+00:00')
        unledgered=q("""select count(*) from p3_object_registry o
                         where o.allocation_release_id ~ '^P3-AUTHORITY-2026-08-02-R(4[2-9]|[5-9][0-9]|1[0-7][0-9]|18[0-4])$'
                           and not exists(select 1 from p3_release_change_ledger l where l.release_id=o.allocation_release_id and l.object_id=o.object_id)""")
        replay_object_count=q("""select count(*) from p3_object_registry where allocation_release_id ~ '^P3-AUTHORITY-2026-08-02-R(4[2-9]|[5-9][0-9]|1[0-7][0-9]|18[0-4])$'""")
        replay_ledger_count=q("""select count(*) from p3_release_change_ledger where release_id ~ '^P3-AUTHORITY-2026-08-02-R(4[2-9]|[5-9][0-9]|1[0-7][0-9]|18[0-4])$'""")
        ck('all_replay_objects_change_ledgered',unledgered==0 and replay_object_count==replay_ledger_count,{'objects':replay_object_count,'ledger':replay_ledger_count,'missing':unledgered},{'missing':0,'objects_equal_ledger':True})
        ledger_hash_mismatch=q("""select count(*) from p3_object_registry o join p3_release_change_ledger l on l.release_id=o.allocation_release_id and l.object_id=o.object_id
                                  where o.allocation_release_id ~ '^P3-AUTHORITY-2026-08-02-R(4[2-9]|[5-9][0-9]|1[0-7][0-9]|18[0-4])$'
                                    and o.content_hash is not null and o.content_hash<>l.content_hash""")
        ck('ledger_matches_registry_content_hash_when_present',ledger_hash_mismatch==0,ledger_hash_mismatch,0)
        # Parse inherited/adjusted 56-query result.
        raw=(sec/'validation/P3C_POSTCLOSE_QUERY_MATRIX_v1_raw.txt').read_text().splitlines()
        results=[x.strip() for x in raw if x.strip() in ('PASS','FAIL')]
        ck('postclose_query_matrix_56_of_56',len(results)==56 and all(x=='PASS' for x in results),Counter(results),{'PASS':56})
    out={'status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL','check_count':len(checks),'passed':sum(x['status']=='PASS' for x in checks),'failed':sum(x['status']=='FAIL' for x in checks),'checks':checks}
    (sec/'validation/P3C_GOVERNED_REPLAY_VALIDATION_RETURN.json').write_text(json.dumps(out,indent=2,sort_keys=True,default=str)+'\n')
    with (sec/'validation/P3C_GOVERNED_REPLAY_CHECK_MATRIX.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['check','status','actual','expected','note']);w.writeheader();
        for x in checks:w.writerow({k:cjson(v) if isinstance(v,(dict,list,tuple,Counter)) else v for k,v in x.items()})
    print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2,sort_keys=True))
    return 0 if out['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
