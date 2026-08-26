#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json
from pathlib import Path
from typing import Any
import psycopg
from psycopg.rows import dict_row


def cjson(v:Any)->str:return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,default=str)
def serial(v:Any)->Any:
    if isinstance(v,(dict,list,tuple)): return cjson(v)
    return v

def write_csv(path:Path,rows:list[dict[str,Any]])->dict[str,Any]:
    fields=list(rows[0]) if rows else []
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for row in rows:w.writerow({k:serial(v) for k,v in row.items()})
    data=path.read_bytes()
    return {'file':path.name,'rows':len(rows),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}

def fetch(conn:psycopg.Connection,sql:str)->list[dict[str,Any]]:
    return [dict(r) for r in conn.execute(sql)]

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument('--dsn',required=True);ap.add_argument('--section',type=Path,required=True);args=ap.parse_args()
    outdir=args.section/'authority';outdir.mkdir(parents=True,exist_ok=True)
    with psycopg.connect(args.dsn,row_factory=dict_row) as conn:
        datasets={
        'P3C_CANONICAL_FAMILY_AUTHORITY.csv':fetch(conn,"""
          WITH latest AS (
            SELECT DISTINCT ON (canonical_family_id) * FROM p3_canonical_family_revision
            ORDER BY canonical_family_id,revision_number DESC),
          mc AS (SELECT family_revision_id,count(*) member_count FROM p3_canonical_family_membership GROUP BY 1),
          src AS (SELECT m.family_revision_id,count(DISTINCT u.source_family) source_count,string_agg(DISTINCT u.source_family,' | ' ORDER BY u.source_family) source_families
                  FROM p3_canonical_family_membership m JOIN p3_upstream_object_reference u ON u.object_id=m.member_object_id GROUP BY 1),
          exc AS (SELECT owner_object_id,count(*) FILTER(WHERE exclusion_type='RULE_BASED') rule_exclusion_count,count(*) FILTER(WHERE exclusion_type='NAMED_MEMBER') named_exclusion_count FROM p3_family_exclusion WHERE authority_release_id ~ '^P3-AUTHORITY-2026-08-02-R' GROUP BY 1)
          SELECT l.canonical_family_id,l.family_revision_id AS latest_family_revision_id,l.revision_number,l.canonical_signature_id,
                 l.canonical_proposition,l.evidence_bundle_hash,l.created_by_adjudication_id,l.authority_release_id,
                 mc.member_count,src.source_count,src.source_families,a.response_portability_status,
                 coalesce(exc.rule_exclusion_count,0) rule_exclusion_count,coalesce(exc.named_exclusion_count,0) named_exclusion_count
          FROM latest l JOIN mc USING(family_revision_id) JOIN src USING(family_revision_id)
          JOIN p3_adjudication_decision a ON a.adjudication_id=l.created_by_adjudication_id
          LEFT JOIN exc ON exc.owner_object_id=l.canonical_family_id ORDER BY l.canonical_family_id"""),
        'P3C_CANONICAL_FAMILY_MEMBERSHIP.csv':fetch(conn,"""
          WITH latest AS (SELECT DISTINCT ON (canonical_family_id) canonical_family_id,family_revision_id,revision_number FROM p3_canonical_family_revision ORDER BY canonical_family_id,revision_number DESC)
          SELECT l.canonical_family_id,l.family_revision_id,l.revision_number,m.member_object_id,u.source_family,u.upstream_object_id,m.variant_revision_id
          FROM latest l JOIN p3_canonical_family_membership m USING(family_revision_id)
          LEFT JOIN p3_upstream_object_reference u ON u.object_id=m.member_object_id
          ORDER BY l.canonical_family_id,m.member_object_id"""),
        'P3C_CANONICAL_FAMILY_REVISION_HISTORY.csv':fetch(conn,"""
          SELECT r.family_revision_id,r.canonical_family_id,r.revision_number,r.canonical_signature_id,r.canonical_proposition,r.evidence_bundle_hash,
                 r.created_by_adjudication_id,r.authority_release_id,p.predecessor_family_revision_id,p.extension_rule,
                 count(m.member_object_id) member_count
          FROM p3_canonical_family_revision r JOIN p3_family_revision_predecessor p USING(family_revision_id)
          LEFT JOIN p3_canonical_family_membership m USING(family_revision_id)
          GROUP BY r.family_revision_id,r.canonical_family_id,r.revision_number,r.canonical_signature_id,r.canonical_proposition,r.evidence_bundle_hash,
                   r.created_by_adjudication_id,r.authority_release_id,p.predecessor_family_revision_id,p.extension_rule
          ORDER BY r.canonical_family_id,r.revision_number"""),
        'P3C_CANONICAL_SIGNATURE_FIELDS.csv':fetch(conn,"""
          SELECT r.canonical_family_id,r.family_revision_id,r.revision_number,s.signature_id,s.signature_status,
                 f.field_name,f.field_value,f.normalized_value_code,f.evidence_state,f.confidence,s.content_hash,s.authority_release_id
          FROM p3_canonical_family_revision r JOIN p3_proposition_signature s ON s.signature_id=r.canonical_signature_id
          JOIN p3_signature_field f USING(signature_id)
          ORDER BY r.canonical_family_id,r.revision_number,f.field_name"""),
        'P3C_CANONICAL_VARIANT_AUTHORITY.csv':fetch(conn,"""
          SELECT p.adjudication_id,d.candidate_revision_id,d.canonical_family_id,p.candidate_variant_revision_id,p.canonical_variant_revision_id,
                 v.variant_id,v.revision_number,v.variant_dimension,v.variant_value,v.value_portability_status,v.authority_release_id
          FROM p3_variant_promotion p JOIN p3_adjudication_decision d USING(adjudication_id)
          JOIN p3_family_variant_revision v ON v.variant_revision_id=p.canonical_variant_revision_id
          ORDER BY p.adjudication_id,p.candidate_variant_revision_id"""),
        'P3C_FAMILY_EXCLUSION_AUTHORITY.csv':fetch(conn,"""
          SELECT exclusion_id,owner_object_id,exclusion_type,prohibited_operation,evidence_or_rule,scope,tested_surface_complete,authority_release_id
          FROM p3_family_exclusion WHERE authority_release_id ~ '^P3-AUTHORITY-2026-08-02-R' ORDER BY owner_object_id,authority_release_id,exclusion_id"""),
        'P3C_PAIR_RESOLUTION_AUTHORITY.csv':fetch(conn,"""
          SELECT r.adjudication_id,d.candidate_revision_id,r.closure_obligation_id,o.left_object_id,o.right_object_id,o.obligation_type,
                 r.resolution_status,r.rationale,r.evidence_hash,r.authority_release_id
          FROM p3_adjudication_pair_resolution r JOIN p3_adjudication_decision d USING(adjudication_id)
          JOIN p3_closure_obligation o USING(closure_obligation_id)
          ORDER BY r.adjudication_id,r.closure_obligation_id"""),
        'P3C_COLLISION_DISPOSITION_AUTHORITY.csv':fetch(conn,"""
          SELECT d.adjudication_id,a.candidate_revision_id,d.collision_id,d.disposition,d.rationale,a.authority_release_id
          FROM p3_adjudication_collision_disposition d JOIN p3_adjudication_decision a USING(adjudication_id)
          ORDER BY d.adjudication_id,d.collision_id"""),
        'P3C_STRONGER_BOUNDARY_AUTHORITY.csv':fetch(conn,"""
          SELECT r.adjudication_id,d.candidate_revision_id,r.boundary_kind,r.boundary_key,r.left_object_id,r.right_object_id,
                 r.disposition,r.rationale,r.evidence_hash,r.authority_release_id
          FROM p3_adjudication_stronger_boundary_resolution r JOIN p3_adjudication_decision d USING(adjudication_id)
          ORDER BY r.adjudication_id,r.boundary_kind,r.boundary_key"""),
        'P3C_SPLIT_SUCCESSOR_AUTHORITY.csv':fetch(conn,"""
          SELECT s.adjudication_id,d.candidate_revision_id AS parent_candidate_revision_id,s.result_ordinal,s.successor_candidate_family_id,
                 cr.candidate_revision_id AS successor_candidate_revision_id,s.successor_origin_key,s.rationale,m.member_object_id,
                 x.evidence_hash AS singleton_authority_hash,x.authority_release_id
          FROM p3_adjudication_split_result s JOIN p3_adjudication_decision d USING(adjudication_id)
          JOIN p3_adjudication_split_result_member m USING(adjudication_id,result_ordinal)
          JOIN p3_candidate_revision cr ON cr.candidate_family_id=s.successor_candidate_family_id
          JOIN p3_singleton_split_authority x ON x.candidate_revision_id=cr.candidate_revision_id
          ORDER BY s.adjudication_id,s.result_ordinal,m.member_object_id"""),
        'P3C_ADJUDICATION_AUTHORITY.csv':fetch(conn,"""
          SELECT d.adjudication_id,d.candidate_revision_id,d.decision_ordinal,d.decision_status,d.canonical_family_id,d.canonical_proposition,
                 d.response_portability_status,d.rationale,d.evidence_bundle_hash,d.supersedes_adjudication_id,d.authority_release_id,d.created_at,
                 count(*) FILTER(WHERE m.member_disposition='ACCEPT') accepted_member_count,
                 count(*) FILTER(WHERE m.member_disposition='ALREADY_CANONICAL') already_canonical_member_count,
                 count(*) FILTER(WHERE m.member_disposition='EXCLUDE') excluded_member_count,
                 count(*) FILTER(WHERE m.member_disposition='SPLIT') split_member_count
          FROM p3_adjudication_decision d LEFT JOIN p3_adjudication_member m USING(adjudication_id)
          GROUP BY d.adjudication_id,d.candidate_revision_id,d.decision_ordinal,d.decision_status,d.canonical_family_id,d.canonical_proposition,
                   d.response_portability_status,d.rationale,d.evidence_bundle_hash,d.supersedes_adjudication_id,d.authority_release_id,d.created_at
          ORDER BY d.adjudication_id""")}
    files=[]
    for name,rows in datasets.items():files.append(write_csv(outdir/name,rows))
    counts={x['file']:x['rows'] for x in files}
    expected={
      'P3C_CANONICAL_FAMILY_AUTHORITY.csv':111,
      'P3C_CANONICAL_FAMILY_MEMBERSHIP.csv':397,
      'P3C_CANONICAL_FAMILY_REVISION_HISTORY.csv':142,
      'P3C_CANONICAL_SIGNATURE_FIELDS.csv':1704,
      'P3C_CANONICAL_VARIANT_AUTHORITY.csv':464,
      'P3C_FAMILY_EXCLUSION_AUTHORITY.csv':153,
      'P3C_PAIR_RESOLUTION_AUTHORITY.csv':345,
      'P3C_COLLISION_DISPOSITION_AUTHORITY.csv':2,
      'P3C_STRONGER_BOUNDARY_AUTHORITY.csv':10,
      'P3C_SPLIT_SUCCESSOR_AUTHORITY.csv':2,
      'P3C_ADJUDICATION_AUTHORITY.csv':143,
    }
    mismatches={k:{'actual':counts.get(k),'expected':v} for k,v in expected.items() if counts.get(k)!=v}
    manifest_hash=hashlib.sha256(cjson(sorted((x['file'],x['sha256'],x['rows']) for x in files)).encode()).hexdigest()
    result={'status':'PASS' if not mismatches else 'FAIL','authority_release_id':'P3-AUTHORITY-2026-08-02-R184','file_count':len(files),'counts':counts,'expected_counts':expected,'count_mismatches':mismatches,'authority_export_manifest_hash':manifest_hash,'files':files,'response_value_portability_authorized':False}
    (outdir/'P3C_AUTHORITY_EXPORT_RETURN.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('files','counts','expected_counts')},indent=2,sort_keys=True))
    return 0 if result['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
