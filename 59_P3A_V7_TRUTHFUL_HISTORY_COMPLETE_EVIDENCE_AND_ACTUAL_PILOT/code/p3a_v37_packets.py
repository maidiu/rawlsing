from __future__ import annotations

import argparse, hashlib, json, subprocess, sys
from decimal import Decimal
from pathlib import Path
import psycopg

RELEASE_ID="P3-AUTHORITY-2026-08-01-R37"
SCHEMA="p3a_v27_shadow"
FIELDS=["subject_role","operator","target","object_or_outcome","modality","timeframe","condition","population_scope","geographic_scope","polarity","derived_status","parent_context"]
SECTION_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SECTION_DIR / "validation"))

def stable(prefix,*parts,width=16):
    return f"{prefix}-{hashlib.sha256('|'.join(parts).encode()).hexdigest()[:width]}"

def canonical_sha256(value):
    from p3_canonical_json_v7 import canonical_sha256 as _sha
    return _sha(value)

def fetch_all(cur,sql,params=()):
    cur.execute(sql,params); return [dict(r) for r in cur.fetchall()]

def one(cur,sql,params=()):
    rows=fetch_all(cur,sql,params)
    if len(rows)!=1: raise RuntimeError(f"expected one row, got {len(rows)} for {sql[:80]}")
    return rows[0]

def number(v):
    return float(v) if isinstance(v,Decimal) else v

def evidence_surface(packet):
    candidate=dict(packet['candidate_family']); candidate.pop('evidence_bundle_hash',None); candidate.pop('ranking',None)
    def sort_objects(values): return sorted(values,key=canonical_sha256)
    return {
      'serialization_contract':'P3_CANONICAL_JSON_V7','candidate_family':candidate,
      'origin_components':sort_objects(packet['origin_components']),'members_by_source':packet['members_by_source'],
      'proposition_signature_matrix':sort_objects(packet['proposition_signature_matrix']),
      'response_contract_matrix':sort_objects(packet['response_contract_matrix']),'pair_projections':sort_objects(packet['pair_projections']),
      'internal_pair_matrix':sort_objects(packet['internal_pair_matrix']),'hard_collisions':sort_objects(packet['hard_collisions']),'typed_collisions':sort_objects(packet.get('typed_collisions',[])),
      'typed_unresolved_boundaries':sort_objects(packet.get('typed_unresolved_boundaries',[])),'typed_redirect_boundaries':sort_objects(packet.get('typed_redirect_boundaries',[])),'typed_coordinate_constraints':sort_objects(packet.get('typed_coordinate_constraints',[])),
      'unresolved_pairs':sort_objects(packet['unresolved_pairs']),'unruled_pairs':sort_objects(packet['unruled_pairs']),
      'closure_obligations':sort_objects(packet['closure_obligations']),'likely_split_points':sort_objects(packet['likely_split_points']),
      'proposed_variants':sort_objects(packet['proposed_variants']),'explicit_exclusions':sort_objects(packet['explicit_exclusions']),
      'hyperedge_context':sort_objects(packet['hyperedge_context']),'strata_horizon_context':sort_objects(packet['strata_horizon_context']),
      'exact_evidence_links':packet['exact_evidence_links']}

def select_candidates(cur):
    selected=[]; rows=[]; seen=set()
    strata = build_pilot_index(cur)
    for item in strata["index"]:
        rid=item["candidate_revision_id"]
        if rid not in seen:
            seen.add(rid); selected.append(rid)
    if selected:
        return selected
    out=[]
    strata_sql = [
        "SELECT cr.candidate_revision_id FROM p3_candidate_revision cr JOIN p3_candidate_ranking r USING(candidate_revision_id) WHERE cr.authority_release_id='P3-AUTHORITY-2026-08-01-R37' AND cr.candidate_classification='COLLISION_BEARING_CANDIDATE' ORDER BY r.hard_collision_count DESC,r.open_obligation_count DESC,cr.candidate_revision_id",
        "SELECT cr.candidate_revision_id FROM p3_candidate_revision cr JOIN p3_candidate_ranking r USING(candidate_revision_id) WHERE cr.authority_release_id='P3-AUTHORITY-2026-08-01-R37' AND EXISTS (SELECT 1 FROM p3_internal_pair_matrix x WHERE x.candidate_revision_id=cr.candidate_revision_id AND x.pair_state='DIRECT_UNRESOLVED') ORDER BY r.open_obligation_count DESC,cr.candidate_revision_id",
        "SELECT cr.candidate_revision_id FROM p3_candidate_revision cr JOIN p3_candidate_ranking r USING(candidate_revision_id) WHERE cr.authority_release_id='P3-AUTHORITY-2026-08-01-R37' AND cr.candidate_origin_type='ATTACHMENT_REVIEW' ORDER BY r.open_obligation_count DESC,r.lineage_count DESC,cr.candidate_revision_id",
        "SELECT cr.candidate_revision_id FROM p3_candidate_revision cr JOIN p3_candidate_ranking r USING(candidate_revision_id) WHERE cr.authority_release_id='P3-AUTHORITY-2026-08-01-R37' AND cr.candidate_origin_type='PROPOSITION_ONLY_SEED' ORDER BY r.open_obligation_count DESC,r.lineage_count DESC,cr.candidate_revision_id",
        "SELECT cr.candidate_revision_id FROM p3_candidate_revision cr JOIN p3_candidate_ranking r USING(candidate_revision_id) WHERE cr.authority_release_id='P3-AUTHORITY-2026-08-01-R37' AND cr.candidate_origin_type='STRICT_RESPONSE_COMPONENT' ORDER BY r.open_obligation_count DESC,r.lineage_count DESC,cr.candidate_revision_id",
    ]
    for sql in strata_sql:
        for row in fetch_all(cur, sql):
            rid=row['candidate_revision_id']
            if rid not in out:
                out.append(rid)
    cur.execute("SELECT candidate_revision_id FROM p3_candidate_revision WHERE authority_release_id='P3-AUTHORITY-2026-08-01-R37' ORDER BY candidate_revision_id")
    for r in cur.fetchall():
        rid=r['candidate_revision_id']
        if rid not in out: out.append(rid)
    return out

def build_pilot_index(cur):
    specs=[
      ("clean_multi_source",7,"cr.candidate_classification='CLEAN_CANDIDATE' AND r.source_count>=2"),
      ("response_variant",5,"r.response_variant_complexity>0"),
      ("split_required",5,"false"),
      ("collision_or_nontransitive",5,"EXISTS (SELECT 1 FROM p3_internal_pair_collision ic JOIN p3_collision_scope_registry c USING(collision_id) WHERE ic.candidate_revision_id=cr.candidate_revision_id AND c.hard_blocker=true)"),
      ("hierarchical_target",4,"EXISTS (SELECT 1 FROM p3_internal_pair_coordinate_constraint h WHERE h.candidate_revision_id=cr.candidate_revision_id)"),
      ("derived_index",3,"false"),
      ("heterogeneous_lineage",3,"EXISTS (SELECT 1 FROM p3_signature_field sf JOIN p3_proposition_signature s USING(signature_id) JOIN p3_candidate_membership cm ON cm.member_object_id=s.subject_id WHERE cm.candidate_revision_id=cr.candidate_revision_id AND sf.evidence_state='HETEROGENEOUS')"),
      ("structure_supported",3,"r.structure_support_count>0"),
      ("source_dominated_or_sparse",2,"r.source_count<=1 OR r.lineage_count<=2"),
      ("exact_only_authority",2,"EXISTS (SELECT 1 FROM p3_internal_pair_unresolved_boundary u WHERE u.candidate_revision_id=cr.candidate_revision_id)"),
      ("precedence_overlap_conflict",1,"EXISTS (SELECT 1 FROM p3_internal_pair_redirect_boundary rb WHERE rb.candidate_revision_id=cr.candidate_revision_id)"),
    ]
    selected=[]; selected_set=set(); eligibility=[]; subs=[]; index=[]; coverage={}
    for name,target,where in specs:
        sql=f"""SELECT cr.candidate_revision_id FROM p3_candidate_revision cr JOIN p3_candidate_ranking r USING(candidate_revision_id) WHERE cr.authority_release_id='P3-AUTHORITY-2026-08-01-R37' AND {where} ORDER BY r.hard_collision_count DESC,r.open_obligation_count DESC,r.lineage_count DESC,cr.candidate_revision_id"""
        elig=[x['candidate_revision_id'] for x in fetch_all(cur,sql)]
        chosen=elig[:target]
        for rid in chosen:
            coverage.setdefault(rid,[]).append(name)
            if rid not in selected_set and len(selected)<40:
                selected_set.add(rid); selected.append(rid); index.append({'candidate_revision_id':rid,'primary_stratum':name,'selection_basis':'eligible','covered_strata':name})
        shortfall=max(0,target-len(chosen)); subchosen=[]
        eligibility.append({'stratum':name,'target':target,'eligible_candidate_ids':elig,'ranked_eligible_population':elig,'selected_candidate_ids':chosen,'selected_count':len(chosen),'shortfall':shortfall,'substitute_candidate_ids':subchosen,'status':'PASS' if len(chosen)==target else 'SHORTFALL_RECORDED'})
        if shortfall:
            subs.append({'stratum':name,'target':target,'shortfall':shortfall,'substitute_candidate_ids':subchosen,'substitution_reason':'no named persisted evidence available; proxy substitution disallowed'})
    for item in index:
        item['covered_strata']='|'.join(coverage.get(item['candidate_revision_id'],[item['primary_stratum']]))
    return {'selected':selected,'eligibility':eligibility,'substitutions':subs,'index':index}

def build_packet(cur,rid,ordinal,update_db_hash=False):
    cr=one(cur,"SELECT * FROM p3_candidate_revision WHERE candidate_revision_id=%s",(rid,))
    cand_id=cr['candidate_family_id']; release=cr['authority_release_id']
    members=[r['member_object_id'] for r in fetch_all(cur,"SELECT member_object_id FROM p3_candidate_membership WHERE candidate_revision_id=%s AND membership_role='PROPOSED_MEMBER' ORDER BY member_object_id",(rid,))]
    by_source={}
    for r in fetch_all(cur,"SELECT u.source_family, cm.member_object_id FROM p3_candidate_membership cm JOIN p3_upstream_object_reference u ON u.object_id=cm.member_object_id WHERE cm.candidate_revision_id=%s ORDER BY u.source_family, cm.member_object_id",(rid,)):
        by_source.setdefault(r['source_family'],[]).append(r['member_object_id'])
    comps=[]; projection_ids=set()
    for comp in fetch_all(cur,"SELECT cc.* FROM p3_candidate_component_link cl JOIN p3_candidate_component cc USING(component_id) WHERE cl.candidate_revision_id=%s ORDER BY cc.component_id",(rid,)):
        mids=[r['member_object_id'] for r in fetch_all(cur,"SELECT member_object_id FROM p3_component_membership WHERE component_id=%s ORDER BY member_object_id",(comp['component_id'],))]
        pids=[r['projection_id'] for r in fetch_all(cur,"SELECT projection_id FROM p3_component_connectivity_edge WHERE component_id=%s ORDER BY projection_id",(comp['component_id'],))]
        projection_ids.update(pids)
        comps.append({'component_id':comp['component_id'],'component_type':comp['component_type'],'member_ids':mids,'connectivity_projection_ids':pids,'build_rule_version':comp['build_rule_version'],'content_hash':comp['content_hash'],'authority_release_id':comp['authority_release_id']})
    attachment_ids=[r['projection_id'] for r in fetch_all(cur,"SELECT projection_id FROM p3_candidate_attachment_projection WHERE candidate_revision_id=%s ORDER BY projection_id",(rid,))]
    projection_ids.update(attachment_ids)
    pairs=[]; unruled=[]; unresolved=[]; hard_collisions=[]; typed_collisions=[]; typed_unresolved=[]; typed_redirect=[]; typed_coordinate=[]
    for row in fetch_all(cur,"SELECT * FROM p3_internal_pair_matrix WHERE candidate_revision_id=%s ORDER BY left_object_id,right_object_id",(rid,)):
        pid=row['direct_pair_projection_id']; pfid=None
        if pid:
            projection_ids.add(pid); pfid=one(cur,"SELECT pair_fact_id FROM p3_pair_projection WHERE projection_id=%s",(pid,))['pair_fact_id']
        close_ids=[r['closure_obligation_id'] for r in fetch_all(cur,"SELECT closure_obligation_id FROM p3_internal_pair_closure WHERE candidate_revision_id=%s AND left_object_id=%s AND right_object_id=%s ORDER BY closure_obligation_id",(rid,row['left_object_id'],row['right_object_id']))]
        collision_ids=[r['collision_id'] for r in fetch_all(cur,"SELECT collision_id FROM p3_internal_pair_collision WHERE candidate_revision_id=%s AND left_object_id=%s AND right_object_id=%s ORDER BY collision_id",(rid,row['left_object_id'],row['right_object_id']))]
        obj={'left_id':row['left_object_id'],'right_id':row['right_object_id'],'pair_state':row['pair_state'],'pair_fact_id':pfid,'pair_projection_id':pid,'collision_ids':collision_ids,'closure_obligation_ids':close_ids}
        pairs.append(obj)
        if row['pair_state']=='UNRULED': unruled.append(obj)
        if row['pair_state']=='DIRECT_UNRESOLVED': unresolved.append(obj)
        for cid in collision_ids:
            c=one(cur,"SELECT * FROM p3_collision_scope_registry WHERE collision_id=%s",(cid,))
            tc={'collision_id':cid,'collision_type':c['collision_type'],'scope_type':c['scope_type'],'orientation':c['orientation'],'left_id':c['left_object_id'],'right_id':c['right_object_id'],'hard_blocker':c['hard_blocker'],'source_scope':c['source_scope'],'historical_scope':c['historical_scope'],'downstream_effects':c['downstream_effects'],'authority_release_id':c['authority_release_id']}
            typed_collisions.append(tc)
            if c['hard_blocker']:
                hard_collisions.append(tc)
    typed_unresolved=fetch_all(cur,"SELECT candidate_revision_id,left_object_id AS left_id,right_object_id AS right_id,projection_id,unresolved_boundary_type,evidence_ids,authority_release_id FROM p3_internal_pair_unresolved_boundary WHERE candidate_revision_id=%s ORDER BY left_object_id,right_object_id",(rid,))
    typed_redirect=fetch_all(cur,"SELECT candidate_revision_id,left_object_id AS left_id,right_object_id AS right_id,projection_id,redirect_scope,evidence_ids,authority_release_id FROM p3_internal_pair_redirect_boundary WHERE candidate_revision_id=%s ORDER BY left_object_id,right_object_id",(rid,))
    typed_coordinate=fetch_all(cur,"SELECT candidate_revision_id,left_object_id AS left_id,right_object_id AS right_id,projection_id,coordinate_relation_type,evidence_ids,authority_release_id FROM p3_internal_pair_coordinate_constraint WHERE candidate_revision_id=%s ORDER BY left_object_id,right_object_id",(rid,))
    projections=fetch_all(cur,"SELECT projection_id,pair_fact_id,left_subject_id,right_subject_id,projection_basis,evidence_ids,authority_release_id FROM p3_pair_projection WHERE projection_id = ANY(%s) ORDER BY projection_id",(sorted(projection_ids),)) if projection_ids else []
    sigs=[]
    for m in members:
        sigrows=fetch_all(cur,"SELECT s.signature_id,s.subject_id,s.signature_status,s.content_hash,s.authority_release_id,sf.field_name,sf.field_value,sf.normalized_value_code,sf.evidence_state,sf.confidence FROM p3_proposition_signature s JOIN p3_signature_field sf USING(signature_id) WHERE s.subject_id=%s ORDER BY sf.field_name",(m,))
        fields={}
        for field in FIELDS:
            fr=next(x for x in sigrows if x['field_name']==field)
            fields[field]={'field_value':fr['field_value'],'normalized_value_code':fr['normalized_value_code'],'evidence_state':fr['evidence_state'],'confidence':fr['confidence'],'evidence_ids':[]}
        sigs.append({'signature_id':sigrows[0]['signature_id'],'subject_id':m,'subject_type':'IMPORTED_SOURCE_LOCAL_LINEAGE','fields':fields,'response_topologies':['UNKNOWN'],'signature_status':sigrows[0]['signature_status'],'content_hash':sigrows[0]['content_hash'],'authority_release_id':sigrows[0]['authority_release_id']})
    rcr=[]
    for m in members:
        ref=one(cur,"SELECT * FROM p3_response_contract_reference WHERE subject_id=%s AND authority_release_id=%s",(m,release))
        rcr.append({'reference_id':ref['reference_id'],'subject_id':m,'upstream_response_contract_id':ref['upstream_response_contract_id'],'response_topology':ref['response_topology'],'response_contract_hash':ref['response_contract_hash'],'authority_artifact':ref['authority_artifact'],'p4_authority':ref['p4_authority'],'authority_release_id':release})
    obligations=[]
    for o in fetch_all(cur,"SELECT * FROM p3_closure_obligation WHERE candidate_revision_id=%s ORDER BY closure_obligation_id",(rid,)):
        obligations.append({'closure_obligation_id':o['closure_obligation_id'],'candidate_revision_id':rid,'left_id':o['left_object_id'],'right_id':o['right_object_id'],'obligation_type':o['obligation_type'],'status':o['status'],'resolution_adjudication_id':o['resolution_adjudication_id'],'authority_release_id':release})
    exclusions=[]
    for e in fetch_all(cur,"SELECT * FROM p3_family_exclusion WHERE owner_object_id=%s ORDER BY exclusion_id",(cand_id,)):
        exclusions.append({'exclusion_id':e['exclusion_id'],'owner_object_id':e['owner_object_id'],'exclusion_type':e['exclusion_type'],'prohibited_operation':e['prohibited_operation'],'evidence_or_rule':e['evidence_or_rule'],'scope':e['scope'],'tested_surface_complete':e['tested_surface_complete'],'excluded_object_ids':[],'authority_release_id':release})
    rank=one(cur,"SELECT * FROM p3_candidate_ranking WHERE candidate_revision_id=%s",(rid,))
    ranking={'candidate_revision_id':rid,'primary_class_rank':rank['primary_class_rank'],'hard_collision_count':rank['hard_collision_count'],'open_obligation_count':rank['open_obligation_count'],'signature_completeness':number(rank['signature_completeness']),'source_count':rank['source_count'],'lineage_count':rank['lineage_count'],'direct_positive_density':number(rank['direct_positive_density']),'structure_support_count':rank['structure_support_count'],'response_variant_complexity':rank['response_variant_complexity'],'authority_release_id':release}
    diag=[r['flag'] for r in fetch_all(cur,"SELECT flag FROM p3_candidate_diagnostic_flag WHERE candidate_revision_id=%s ORDER BY flag",(rid,))]
    if obligations and 'OPEN_CLOSURE' not in diag: diag.append('OPEN_CLOSURE')
    if not diag: diag=['SPARSE']
    candidate={'candidate_family_id':cand_id,'revision_id':rid,'revision_number':cr['revision_number'],'component_ids':[c['component_id'] for c in comps],'member_ids':members,'canonical_signature_id':cr['canonical_signature_id'],'candidate_classification':cr['candidate_classification'],'candidate_origin_type':cr['candidate_origin_type'],'diagnostic_flags':diag,'internal_pair_counts':{k:0 for k in ['expected_pairs','direct_positive','direct_collision','direct_unresolved','hierarchical_only','unruled','signature_conflict','signature_compatible']},'closure_obligation_ids':[o['closure_obligation_id'] for o in obligations],'variant_ids':[],'exclusion_ids':[e['exclusion_id'] for e in exclusions],'ranking':ranking,'evidence_bundle_hash':'0'*64,'authority_release_id':release,'origin_key':cr['origin_key'],'attachment_projection_ids':attachment_ids}
    state_map={'DIRECT_POSITIVE':'direct_positive','DIRECT_COLLISION':'direct_collision','DIRECT_UNRESOLVED':'direct_unresolved','HIERARCHICAL_ONLY':'hierarchical_only','UNRULED':'unruled','SIGNATURE_CONFLICT':'signature_conflict','SIGNATURE_COMPATIBLE':'signature_compatible'}
    candidate['internal_pair_counts']['expected_pairs']=len(pairs)
    for p in pairs: candidate['internal_pair_counts'][state_map[p['pair_state']]]+=1
    decision={'adjudication_id':f'P3ADJ-{ordinal:06d}','candidate_family_id':cand_id,'candidate_revision_id':rid,'decision_ordinal':1,'decision_status':None,'canonical_family_id':None,'canonical_proposition':None,'accepted_members':[],'excluded_members':[],'variant_assignments':[],'split_points':[],'hierarchical_relations':[],'collision_dispositions':[],'unresolved_boundaries':[],'response_portability_status':'NOT_AUTHORIZED_BY_P3','rationale':'Draft-only P3A pilot packet; human P3C adjudication required.','evidence_bundle_hash':'0'*64,'supersedes_adjudication_id':None,'authority_release_id':release,'split_results':[],'variant_promotions':[],'exclusion_promotions':[]}
    packet={'packet_id':'PENDING_PACKET_ID','candidate_family':candidate,'origin_components':comps,'members_by_source':by_source,'proposition_signature_matrix':sigs,'response_contract_matrix':rcr,'pair_projections':projections,'internal_pair_matrix':pairs,'hard_collisions':hard_collisions,'typed_collisions':typed_collisions,'typed_unresolved_boundaries':typed_unresolved,'typed_redirect_boundaries':typed_redirect,'typed_coordinate_constraints':typed_coordinate,'unresolved_pairs':unresolved,'unruled_pairs':unruled,'closure_obligations':obligations,'likely_split_points':[],'proposed_variants':[],'explicit_exclusions':exclusions,'hyperedge_context':[],'strata_horizon_context':[],'exact_evidence_links':sorted([rid]+members+list(projection_ids))[:max(2,2+len(projection_ids))],'evidence_bundle_hash':'0'*64,'decision_form':decision,'fixture_status':'AUTHORITY_PACKET'}
    h=canonical_sha256(evidence_surface(packet)); packet['packet_id']=stable('P3PKT',rid,h,'candidate_packet.schema.json'); packet['evidence_bundle_hash']=h; packet['candidate_family']['evidence_bundle_hash']=h; packet['decision_form']['evidence_bundle_hash']=h; decision['evidence_bundle_hash']=h
    if update_db_hash:
        cur.execute("UPDATE p3_candidate_revision SET evidence_bundle_hash=%s WHERE candidate_revision_id=%s",(h,rid))
    return packet,decision,h

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--dsn',required=True); ap.add_argument('--root',type=Path,required=True); ap.add_argument('--limit',type=int,default=None); ap.add_argument('--finalize-hashes',action='store_true')
    args=ap.parse_args(); sec=args.root/'59_P3A_V7_TRUTHFUL_HISTORY_COMPLETE_EVIDENCE_AND_ACTUAL_PILOT'; pdir=sec/'candidate_packets'; ddir=sec/'draft_decisions'; pdir.mkdir(exist_ok=True); ddir.mkdir(exist_ok=True)
    validation=[]
    with psycopg.connect(args.dsn,row_factory=psycopg.rows.dict_row,autocommit=False) as conn:
        conn.execute(f"SET search_path TO {SCHEMA}, public"); cur=conn.cursor(); pilot=build_pilot_index(cur)
        if args.finalize_hashes:
            cur.execute("SELECT candidate_revision_id FROM p3_candidate_revision WHERE authority_release_id=%s ORDER BY candidate_revision_id",(RELEASE_ID,))
            all_rids=[r['candidate_revision_id'] for r in cur.fetchall()]
            for ordinal,rid in enumerate(all_rids,1):
                build_packet(cur,rid,ordinal,update_db_hash=True)
            conn.commit()
            out={'status':'PASS','finalized_candidate_hashes':len(all_rids),'builder':'p3a_v37_packets.evidence_surface'}
            (sec/'outputs/p3a_v37_candidate_hash_finalization_return.json').write_text(json.dumps(out,indent=2)+'\n')
            print(json.dumps(out,indent=2)); return 0
        selected=select_candidates(cur)
        if args.limit is not None:
            selected=selected[:args.limit]
        for ordinal,rid in enumerate(selected,1):
            packet,decision,h=build_packet(cur,rid,ordinal,update_db_hash=False)
            pp=pdir/f"{packet['packet_id']}_{packet['candidate_family']['candidate_family_id']}.json"; dp=ddir/f"{decision['adjudication_id']}_{decision['candidate_family_id']}_DRAFT.json"
            pp.write_text(json.dumps(packet,ensure_ascii=False,indent=2,sort_keys=True)+'\n'); dp.write_text(json.dumps(decision,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
            proc=subprocess.run([sys.executable,str(sec/'validation/validate_p3_candidate_packet_v37.py'),str(pp),str(dp)],text=True,capture_output=True)
            validation.append({'candidate_revision_id':rid,'packet_path':str(pp.relative_to(args.root)),'decision_path':str(dp.relative_to(args.root)),'returncode':proc.returncode,'stdout':proc.stdout,'stderr':proc.stderr,'evidence_bundle_hash':h})
        conn.commit()
    out={'status':'PASS' if all(v['returncode']==0 for v in validation) and len(validation)==len(selected) else 'FAIL','selection_reason':'independent named-evidence strata with overlap allowed and no proxy substitutions','pilot':pilot,'packets':validation}
    (sec/'outputs/p3a_v37_packet_build_return.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2)); return 0 if out['status']=='PASS' else 1
if __name__=='__main__': raise SystemExit(main())
