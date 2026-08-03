#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path
import psycopg

def rows(p:Path):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f))
def sha(p:Path):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);ap.add_argument('--dsn',required=True);a=ap.parse_args()
    root=a.root; sec=root/'82_P3A_V40_CLEAN_RECONSTRUCTION_BASELINE'; s62=root/'62_P3A_V7_CANDIDATE_EVIDENCE_STAGING_AND_ATOMIC_PROMOTION'; ctl=root/'91_RECONSTRUCTION_CONTROL/manifests'
    inherited={r['candidate_revision_id']:r for r in rows(ctl/'inherited_P3A_V40_ALL_CANDIDATE_HASH_RECONCILIATION.csv')}
    inherited_snap={r['candidate_revision_id']:r for r in rows(ctl/'inherited_P3A_V40_ALL_CANDIDATE_SNAPSHOT_RECONCILIATION.csv')}
    with psycopg.connect(a.dsn,row_factory=psycopg.rows.dict_row) as c:
        q=c.cursor()
        counts={}
        for name,sql in {
          'lineage_objects':"select count(*) n from p3_object_registry where object_type='IMPORTED_SOURCE_LOCAL_LINEAGE'",
          'implementation_objects':"select count(*) n from p3_object_registry where object_type='IMPORTED_IMPLEMENTATION'",
          'imported_memberships':"select count(*) n from p3_imported_lineage_membership",
          'pair_facts':"select count(*) n from p3_pair_fact_bundle",
          'pair_endpoint_resolutions':"select count(*) n from p3_pair_endpoint_resolution",
          'candidate_components':"select count(*) n from p3_candidate_component",
          'candidate_revisions_r40':"select count(*) n from p3_candidate_revision where authority_release_id='P3-AUTHORITY-2026-08-01-R40'",
          'candidate_snapshots_r40':"select count(*) n from p3_candidate_evidence_snapshot where authority_release_id='P3-AUTHORITY-2026-08-01-R40'",
          'closure_obligations':"select count(*) n from p3_closure_obligation",
        }.items():q.execute(sql);counts[name]=q.fetchone()['n']
        q.execute("select r.candidate_revision_id,r.candidate_family_id,r.evidence_bundle_hash,s.evidence_bundle_hash snapshot_hash from p3_candidate_revision r join p3_candidate_evidence_snapshot s using(candidate_revision_id) where r.authority_release_id='P3-AUTHORITY-2026-08-01-R40' order by 1")
        current=list(q.fetchall())
    recon=[]
    for r in current:
        old=inherited.get(r['candidate_revision_id']); olds=inherited_snap.get(r['candidate_revision_id'])
        ok=bool(old and olds and old['evidence_bundle_hash']==r['evidence_bundle_hash']==r['snapshot_hash']==olds['revision_hash']==olds['snapshot_hash'])
        recon.append({'candidate_revision_id':r['candidate_revision_id'],'candidate_family_id':r['candidate_family_id'],'inherited_hash':old['evidence_bundle_hash'] if old else '', 'rebuilt_revision_hash':r['evidence_bundle_hash'],'rebuilt_snapshot_hash':r['snapshot_hash'],'status':'PASS' if ok else 'FAIL'})
    fields=list(recon[0]);
    with (sec/'outputs/P3A_V40_RECONSTRUCTION_HASH_RECONCILIATION.csv').open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(recon)
    qm=rows(s62/'P3A_V40_QUERY_MATRIX.csv'); applicable=[r for r in qm if r['status']=='FAIL' and r['query_or_gate'] not in {'q01b_postpromotion_pointer','q15b_no_unadjudicated_at_p3_close'}]
    fixture=json.loads((s62/'P3A_V40_FIXTURE_RETURN.json').read_text())
    packet=json.loads((s62/'outputs/p3a_v40_packet_build_return.json').read_text())
    verifier=json.loads((s62/'outputs/verify_handoff_v40_return.json').read_text())
    expected={'lineage_objects':13526,'implementation_objects':18276,'imported_memberships':18276,'pair_facts':19175,'pair_endpoint_resolutions':38350,'candidate_components':119,'candidate_revisions_r40':141,'candidate_snapshots_r40':141,'closure_obligations':345}
    failures=[]
    for k,v in expected.items():
        if counts.get(k)!=v:failures.append(f'{k}:{counts.get(k)}!={v}')
    if len(recon)!=141 or any(r['status']!='PASS' for r in recon):failures.append('candidate_hash_reconciliation')
    if applicable:failures.append('applicable_query_failures:'+','.join(r['query_or_gate'] for r in applicable))
    if fixture.get('status')!='PASS':failures.append('fixture')
    if packet.get('status')!='PASS':failures.append('packet')
    if verifier.get('status')!='PASS':failures.append('verifier')
    out={'status':'PASS' if not failures else 'FAIL','release_id':'P3-AUTHORITY-2026-08-01-R40','counts':counts,'expected_counts':expected,'candidate_hash_matches':sum(r['status']=='PASS' for r in recon),'candidate_hash_total':len(recon),'query_matrix_pass':sum(r['status']=='PASS' for r in qm),'query_matrix_fail':[r['query_or_gate'] for r in qm if r['status']=='FAIL'],'applicable_query_failures':[r['query_or_gate'] for r in applicable],'packet_status':packet.get('status'),'fixture_status':fixture.get('status'),'inherited_verifier_status':verifier.get('status'),'failures':failures,'inputs':{'inherited_hash_manifest_sha256':sha(ctl/'inherited_P3A_V40_ALL_CANDIDATE_HASH_RECONCILIATION.csv'),'ddl_sha256':sha(s62/'sql/p3_postgresql_compatible_ddl_v7_v40.sql')}}
    (sec/'outputs/P3A_V40_RECONSTRUCTION_VERIFIER_RETURN.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2));return 0 if not failures else 1
if __name__=='__main__':raise SystemExit(main())
