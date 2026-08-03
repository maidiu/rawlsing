#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, io, json, os, re, sys, zipfile
from pathlib import Path
sys.dont_write_bytecode = True
from collections import Counter, defaultdict
from docx import Document
try:
    import yaml
except Exception:
    yaml=None
csv.field_size_limit(sys.maxsize)

def sha(p: Path) -> str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def rows(p: Path):
    with p.open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))

def one(root: Path, pattern: str) -> Path:
    xs=list(root.glob(pattern))
    if len(xs)!=1: raise RuntimeError(f'{root}: {pattern}: {xs}')
    return xs[0]

def jlist(s):
    return json.loads(s) if s else []

def main():
    ap=argparse.ArgumentParser(description='Read-only v17 cumulative handoff verifier')
    ap.add_argument('root',nargs='?',default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument('--json-out')
    a=ap.parse_args(); root=Path(a.root).resolve()
    failures=[]; checks=[]
    def ck(name,ok,detail=''):
        checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})
        if not ok: failures.append({'check':name,'detail':detail})

    # Top-level manifests: exact hashes and full coverage, excluding the two manifest files themselves.
    idx=root/'PACKAGE_INDEX.csv'; sums=root/'SHA256SUMS.csv'
    for m in [idx,sums]:
        rs=rows(m); bad=[]
        for r in rs:
            p=root/r['relative_path']
            if not p.exists() or sha(p)!=r['sha256']: bad.append(r['relative_path'])
            if 'bytes' in r and p.exists() and int(r['bytes'])!=p.stat().st_size: bad.append(r['relative_path']+':size')
        actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p not in (idx,sums)}
        listed={r['relative_path'] for r in rs}
        ck(m.name+':hashes',not bad,json.dumps(bad))
        ck(m.name+':coverage',actual==listed,json.dumps({'actual':len(actual),'listed':len(listed),'only_actual':sorted(actual-listed),'only_listed':sorted(listed-actual)}))

    # Type-aware readability of every delivered file.
    file_count=0; readability_failures=[]
    for p in sorted(x for x in root.rglob('*') if x.is_file()):
        file_count+=1; ext=p.suffix.lower()
        try:
            if p.stat().st_size==0 and ext!='.py': raise ValueError('empty')
            if ext=='.csv':
                with p.open(encoding='utf-8-sig',newline='') as f:
                    r=csv.reader(f); hdr=next(r)
                    for n,row in enumerate(r,2):
                        if len(row)!=len(hdr): raise ValueError(f'row {n} has {len(row)} vs {len(hdr)} columns')
            elif ext=='.json': json.load(p.open(encoding='utf-8'))
            elif ext in ('.yaml','.yml'):
                if yaml is None: raise RuntimeError('PyYAML missing')
                yaml.safe_load(p.read_text(encoding='utf-8'))
            elif ext=='.py': compile(p.read_text(encoding='utf-8'),str(p),'exec')
            elif ext=='.docx': Document(p)
            elif ext=='.zip':
                with zipfile.ZipFile(p) as z:
                    if z.testzip() is not None: raise ValueError('bad zip member')
            else: p.open('rb').read(1)
        except Exception as e: readability_failures.append({'path':p.relative_to(root).as_posix(),'error':repr(e)})
    ck('all_files_type_readable',not readability_failures,json.dumps({'files':file_count,'failures':readability_failures}))

    # Recursive ZIP integrity, including archives nested inside archives.
    seen=set(); archive_instances=0; zip_failures=[]
    def walk(label,data):
        nonlocal archive_instances
        archive_instances+=1; seen.add(hashlib.sha256(data).hexdigest())
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            bad=z.testzip()
            if bad: zip_failures.append({'archive':label,'bad_member':bad})
            for i in z.infolist():
                if not i.is_dir() and i.filename.lower().endswith('.zip'): walk(label+'!/'+i.filename,z.read(i))
    for p in sorted(root.rglob('*.zip')):
        try: walk(p.relative_to(root).as_posix(),p.read_bytes())
        except Exception as e: zip_failures.append({'archive':p.relative_to(root).as_posix(),'error':repr(e)})
    ck('recursive_zip_integrity',not zip_failures,json.dumps({'instances':archive_instances,'unique_payloads':len(seen),'failures':zip_failures}))

    # Governing all-nine source-local state and exact Phase 0 identity reconciliation.
    phase=json.load((root/'08_P2_PHASE0'/'Rawlsing_P2_Phase0_Governed_Question_Node_Catalog_v1.json').open())
    by=defaultdict(set)
    for r in phase['question_implementations']: by[r['source_family']].add(r['question_implementation_id'])
    roots={
      'GSS':root/'09_P2_GSS_PASS1','WVS':root/'10_P2_WVS_PASS1','EVS':root/'12_P2_EVS_PASS1',
      'Arab Barometer':root/'15_P2_ARAB_BAROMETER_PASS1','Afrobarometer':root/'19_P2_AFROBAROMETER_PASS1',
      'Asian Barometer':root/'24_P2_ASIAN_BAROMETER_PASS1'/'PACKAGE_CONTENTS',
      'Latinobarómetro':root/'25_P2_LATINOBAROMETRO_PASS1'/'PACKAGE_CONTENTS',
      'South Asia':root/'26_P2_SOUTH_ASIA_PASS1'/'PACKAGE_CONTENTS',
      'LiTS':root/'27_P2_LITS_PASS1'/'PACKAGE_CONTENTS'}
    closure={r['source_family']:r for r in rows(root/'28_P2_ALL_NINE_SOURCE_LOCAL_CLOSURE'/'Rawlsing_P2_All_Nine_Source_Local_Closure_Summary_v2.csv')}
    union=set(); totals=Counter()
    for s,sr in roots.items():
        nodes=rows(one(sr,'**/*Deep_Question_Node_Catalog*.csv')); ids={r['question_implementation_id'] for r in nodes}; union|=ids
        gaps_files=list(sr.glob('**/*Response_Authority_Gaps*.csv'))
        if gaps_files: gaps=rows(gaps_files[0])
        else: gaps=[r for r in nodes if 'gap' in r.get('response_binding_status','').lower() or r.get('response_binding_status') in ('unbound','blocked')]
        edges=rows(one(sr,'**/*Accepted_Longitudinal_Continuity_Edges*.csv'))
        inv=rows(one(sr,'**/*Source_Structure_Inventory*.csv'))
        c=closure[s]
        ck(s+':phase0_identity',ids==by[s],json.dumps({'deep':len(ids),'phase0':len(by[s])}))
        ck(s+':counts',len(nodes)==int(c['nodes']) and len(gaps)==int(c['response_gaps']) and len(edges)==int(c['accepted_continuity_edges']) and len(inv)==int(c['source_structures']),json.dumps({'nodes':len(nodes),'gaps':len(gaps),'edges':len(edges),'structures':len(inv)}))
        bad_edges=[r for r in edges if r['left_question_implementation_id'] not in ids or r['right_question_implementation_id'] not in ids or r['left_question_implementation_id']==r['right_question_implementation_id']]
        ck(s+':edge_referential_integrity',not bad_edges,str(len(bad_edges)))
        totals['nodes']+=len(nodes); totals['gaps']+=len(gaps); totals['bound']+=len(nodes)-len(gaps); totals['edges']+=len(edges); totals['structures']+=len(inv)
    phaseall=set().union(*by.values())
    ck('all_nine_union_exact_phase0',union==phaseall,json.dumps({'union':len(union),'phase0':len(phaseall),'missing':len(phaseall-union),'extra':len(union-phaseall)}))
    ck('global_totals',dict(totals)=={'nodes':18276,'gaps':1968,'bound':16308,'edges':4759,'structures':2499},json.dumps(totals))

    # Restart controls and authority boundary.
    cur=json.load((root/'00_START_HERE'/'CURRENT_STATE.json').open())
    scope=json.load((root/'00_START_HERE'/'SCOPE_LOCK.json').open())
    val=json.load((root/'VALIDATION.json').open())
    expected_v14_next='P2_GLOBAL_SEMANTIC_NEIGHBORHOOD_FULL_ADJUDICATION_AND_STRATA_DOCTRINE_RUNTIME_REPAIR'
    expected_next='P2_GLOBAL_NEXT_FIXED_3000_PAIR_TRANCHE_FROM_8847_REMAINING_AND_LIVE_COMPONENT_STRATA_BRIDGE_INSTALLATION'
    ck('restart_controls_current',cur.get('handoff_version')=='v17' and scope.get('current_pass')==cur.get('current_pass') and scope.get('next_pass')==expected_next and val.get('next_pass')==expected_next and len(cur.get('source_local_deep_passes_closed',[]))==9,'')
    ck('authority_boundary_locked',cur.get('global_p2_closed') is False and cur.get('substantive_family_authority_authored') is False and cur.get('respondents_processed') is False and cur.get('live_pipeline_modified') is False and scope.get('p2_family_authoring_permitted') is False and scope.get('p2_respondent_execution_permitted') is False,'')
    ck('cumulative_output_protocol_present',(root/'00_START_HERE'/'OUTPUT_AND_HANDOFF_PROTOCOL.md').exists(),'')

    # Tranche 1 governed foundation.
    sec=root/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'
    nodes=rows(sec/'Rawlsing_P2_All_Nine_Unified_Node_Evidence_Registry_v1.csv')
    node_ids={r['question_implementation_id'] for r in nodes}
    ck('tranche_nodes_exact',len(nodes)==18276 and len(node_ids)==18276 and node_ids==phaseall,json.dumps({'rows':len(nodes),'unique':len(node_ids),'phase0':len(phaseall)}))
    join_counts=Counter(r['semantic_reference_join_status'] for r in nodes)
    ck('semantic_reference_join_partition',join_counts==Counter({'EXACT_SOURCE_WAVE_VARIABLE':18052,'UNIQUE_CASEFOLD_FALLBACK_DIAGNOSTIC':197,'NO_SEMANTIC_REFERENCE_MATCH':27}),json.dumps(join_counts))

    lineages=rows(sec/'Rawlsing_P2_All_Nine_Source_Local_Lineage_Registry_v1.csv')
    lineage_ids={r['lineage_id'] for r in lineages}; members=[]; bad_lineages=[]
    for r in lineages:
        ids=jlist(r['member_question_implementation_ids_json']); members.extend(ids)
        if len(ids)!=int(r['member_count']) or any(i not in node_ids for i in ids): bad_lineages.append(r['lineage_id'])
    ck('source_local_lineage_partition',len(lineages)==13526 and len(lineage_ids)==13526 and len(members)==18276 and len(set(members))==18276 and set(members)==node_ids and not bad_lineages,json.dumps({'lineages':len(lineages),'members':len(members),'bad':bad_lineages[:10]}))
    ck('multi_implementation_lineages',sum(int(r['member_count'])>1 for r in lineages)==2042,'')

    groups=rows(sec/'Rawlsing_P2_Exact_Proposition_Group_Adjudication_v1.csv')
    ck('exact_proposition_groups_governed',len(groups)==146 and len({r['exact_proposition_group_id'] for r in groups})==146 and all(r['authority_status'] for r in groups),'')

    exact=rows(sec/'Rawlsing_P2_Exact_Foundation_Pair_Rulings_v1.csv')
    auth=Counter(r['authority_status'] for r in exact)
    accepted=sum(v for k,v in auth.items() if k.startswith('ACCEPTED_'))
    rejected=sum(v for k,v in auth.items() if k.startswith('REJECTED_'))
    unresolved=sum(v for k,v in auth.items() if k.startswith('UNRESOLVED_'))
    bad_endpoints=[r['cross_source_candidate_id'] for r in exact if r['left_lineage_id'] not in lineage_ids or r['right_lineage_id'] not in lineage_ids or r['left_source_family']==r['right_source_family']]
    ck('exact_foundation_pair_partition',len(exact)==751 and len({r['cross_source_candidate_id'] for r in exact})==751 and (accepted,rejected,unresolved)==(256,74,421) and not bad_endpoints,json.dumps({'rows':len(exact),'accepted':accepted,'rejected':rejected,'unresolved':unresolved,'bad_endpoints':bad_endpoints[:10]}))
    accepted_rows=[r for r in exact if r['authority_status'].startswith('ACCEPTED_')]
    bad_ceiling=[r['cross_source_candidate_id'] for r in accepted_rows if not r['portability_ceiling'] or r['portability_ceiling']=='NONE']
    bad_two_sided=[r['cross_source_candidate_id'] for r in accepted_rows if not r['two_sided_evidence_status'].startswith('COMPLETE')]
    ck('accepted_exact_bounded_and_two_sided',not bad_ceiling and not bad_two_sided,json.dumps({'bad_ceiling':bad_ceiling,'bad_two_sided':bad_two_sided}))
    # Structural leak guard: no accepted row may be one of the explicit generic shells/weights/IDs/target-only rule classes.
    prohibited_accept_classes={'GENERIC_RESPONSE_OR_PROMPT_SHELL','GENERIC_IDENTIFIER_OR_WEIGHT','TARGET_LABEL_WITHOUT_RELATION_AXIS','GENERIC_METADATA_LABEL'}
    bad_generic=[r['cross_source_candidate_id'] for r in accepted_rows if r['adjudication_rule_class'] in prohibited_accept_classes]
    ck('accepted_exact_no_generic_shell_or_bare_target_leak',not bad_generic,json.dumps(bad_generic))

    neighborhoods=rows(sec/'Rawlsing_P2_Semantic_Neighborhood_Registry_v1.csv')
    cand_sum=sum(int(r['candidate_pair_count']) for r in neighborhoods)
    ck('semantic_neighborhood_registry',len(neighborhoods)==200 and len({r['semantic_neighborhood_id'] for r in neighborhoods})==200 and cand_sum==136329 and all(int(r['source_count'])>=2 for r in neighborhoods),json.dumps({'rows':len(neighborhoods),'candidate_sum':cand_sum}))
    queue=rows(sec/'Rawlsing_P2_Semantic_Neighborhood_Pair_Queue_v1.csv')
    bad_queue=[r['semantic_pair_candidate_id'] for r in queue if r['left_lineage_id'] not in lineage_ids or r['right_lineage_id'] not in lineage_ids or r['left_source_family']==r['right_source_family'] or int(r['cell_priority_rank'])>25 or r['authority_status']!='PROVISIONAL_DISCOVERY_PAIR_NOT_ADJUDICATED']
    ck('semantic_priority_queue_bounded_non_authoritative',len(queue)==18831 and len({r['semantic_pair_candidate_id'] for r in queue})==18831 and not bad_queue,json.dumps({'rows':len(queue),'bad':bad_queue[:10]}))

    structures=rows(sec/'Rawlsing_P2_Normalized_Source_Structure_Registry_v1.csv')
    memberships=rows(sec/'Rawlsing_P2_Normalized_Source_Structure_Memberships_v1.csv')
    sids={r['source_structure_id'] for r in structures}; memby=Counter(r['source_structure_id'] for r in memberships)
    bad_members=[r for r in memberships if r['source_structure_id'] not in sids or r['question_implementation_id'] not in node_ids or r['lineage_id'] not in lineage_ids]
    bad_counts=[r['source_structure_id'] for r in structures if int(r['declared_member_count'])!=memby[r['source_structure_id']] or int(r['recovered_member_count'])!=memby[r['source_structure_id']] or r['membership_recovery_status']!='COMPLETE']
    ck('structure_inventory_and_memberships_exact',len(structures)==2499 and len(sids)==2499 and len(memberships)==15990 and not bad_members and not bad_counts,json.dumps({'structures':len(structures),'memberships':len(memberships),'bad_members':len(bad_members),'bad_counts':bad_counts[:10]}))
    analogies=rows(sec/'Rawlsing_P2_Provisional_Structure_Analogy_Queue_v1.csv')
    bad_analogies=[r['structure_analogy_candidate_id'] for r in analogies if r['left_source_structure_id'] not in sids or r['right_source_structure_id'] not in sids or r['left_source_family']==r['right_source_family'] or not r['authority_status'].startswith('PROVISIONAL_')]
    ck('provisional_structure_analogy_queue',len(analogies)==19 and len({r['structure_analogy_candidate_id'] for r in analogies})==19 and not bad_analogies,json.dumps(bad_analogies))

    matrix=rows(sec/'Rawlsing_P2_Source_Pair_Coverage_Matrix_v1.csv')
    source_pairs={(r['left_source_family'],r['right_source_family']) for r in matrix}
    ck('all_36_source_pairs_covered',len(matrix)==36 and len(source_pairs)==36 and all(r['coverage_status']=='PRESENT' for r in matrix),'')

    anomalies=rows(sec/'Rawlsing_P2_Semantic_Reference_Anomaly_Queue_v1.csv')
    anomaly_counts=Counter(r['anomaly_type'] for r in anomalies)
    ck('semantic_reference_anomalies_preserved',len(anomalies)==30 and anomaly_counts==Counter({'NO_SEMANTIC_REFERENCE_MATCH':27,'INHERITED_SEMANTIC_CONTENT_CONTRADICTS_EXACT_ITEM':3}) and all(r['authority_status'] in {'OPEN_REFERENCE_ANOMALY_NO_INHERITED_MAPPING_AUTHORITY','OPEN_REFERENCE_ANOMALY_INHERITED_MAPPING_QUARANTINED'} for r in anomalies),json.dumps(anomaly_counts))

    gap=rows(sec/'Rawlsing_P2_Nine_Strata_Field_Lineage_Gap_Ledger_v1.csv')
    norm=json.load((sec/'Rawlsing_P2_Nine_Strata_Field_Lineage_Normalized_Summary_v1.json').open())
    raw=json.load((sec/'SOURCE_nine_strata_field_lineage_ledger.json').open())
    gap_status=Counter(r['lineage_status'] for r in gap)
    raw_count=len(raw.get('field_families',[])); raw_declared=raw.get('summary',{}).get('field_families_traced')
    raw_summary_status_sum=sum(raw.get('summary',{}).get(k,0) for k in ('preserved_authoritative','present_upstream_dropped_at_v552j','present_but_empty','missing_generated_artifact'))
    ck('nine_strata_gap_lineage_disclosed',len(gap)==33 and gap_status==Counter({'present_upstream_dropped_at_v552j':16,'preserved_authoritative':8,'present_but_empty':8,'missing_generated_artifact':1}) and norm.get('normalized_field_family_rows')==33 and norm.get('raw_summary_declared_field_families_traced')==30 and norm.get('raw_summary_status_count_sum')==28 and norm.get('raw_summary_consistent_with_rows') is False and raw_count==33 and raw_declared==30 and raw_summary_status_sum==28,json.dumps({'rows':len(gap),'statuses':gap_status,'raw_rows':raw_count,'raw_declared':raw_declared,'raw_status_sum':raw_summary_status_sum}))

    secval=json.load((sec/'VALIDATION.json').open())
    ck('tranche_validation_current',secval.get('status')=='PASS' and secval.get('counts',{}).get('exact_accepted')==256 and secval.get('counts',{}).get('structure_memberships')==15990 and secval.get('next_pass')=='P2_GLOBAL_REWORDED_TRANSLATION_TARGET_RELATION_AXIS_AND_STRUCTURE_ADJUDICATION','')


    # Tranche 2 governed adjudication.
    sec2=root/'33_P2_GLOBAL_REWORDED_RELATION_AXIS_STRUCTURE_ADJUDICATION_TRANCHE2'
    exact2=rows(sec2/'Rawlsing_P2_Exact_Foundation_Pair_Rulings_v2.csv')
    exact1_by={r['cross_source_candidate_id']:r for r in exact}
    exact2_by={r['cross_source_candidate_id']:r for r in exact2}
    auth2=Counter(r['authority_status'] for r in exact2)
    acc2=sum(v for k,v in auth2.items() if k.startswith('ACCEPTED_'))
    rej2=sum(v for k,v in auth2.items() if k.startswith('REJECTED_'))
    unr2=sum(v for k,v in auth2.items() if k.startswith('UNRESOLVED_'))
    ck('tranche2_exact_v2_partition',len(exact2)==751 and set(exact2_by)==set(exact1_by) and (acc2,rej2,unr2)==(270,78,403),json.dumps({'rows':len(exact2),'accepted':acc2,'rejected':rej2,'unresolved':unr2}))
    axis=rows(sec2/'Rawlsing_P2_Exact_Target_Relation_Axis_Rulings_v1.csv')
    axis_ids={r['cross_source_candidate_id'] for r in axis}
    changed={cid for cid in exact1_by if any(exact1_by[cid].get(k)!=exact2_by[cid].get(k) for k in ('adjudication_rule_class','relation_type','authority_status','portability_ceiling','adjudication_confidence','rationale'))}
    axis_status=Counter('accepted' if r['authority_status'].startswith('ACCEPTED_') else 'rejected' if r['authority_status'].startswith('REJECTED_') else 'other' for r in axis)
    bad_axis=[r['cross_source_candidate_id'] for r in axis if r['left_lineage_id'] not in lineage_ids or r['right_lineage_id'] not in lineage_ids or r['two_sided_evidence_status']!='COMPLETE_DEEP_REVIEWED_SOURCE_RECORDS_BOTH_SIDES']
    ck('exact_target_axis_18_complete',len(axis)==18 and len(axis_ids)==18 and changed==axis_ids and axis_status==Counter({'accepted':14,'rejected':4}) and not bad_axis,json.dumps({'changed':len(changed),'statuses':axis_status,'bad':bad_axis}))

    sem=rows(sec2/'Rawlsing_P2_Reworded_Translation_High_Precision_Pair_Rulings_v1.csv')
    sem_ids={r['semantic_pair_candidate_id'] for r in sem}
    sem_status=Counter(r['authority_status'] for r in sem)
    sem_positive=sum(v for k,v in sem_status.items() if k.startswith('ACCEPTED_'))
    sem_rejected=sum(v for k,v in sem_status.items() if k.startswith('REJECTED_'))
    sem_unresolved=sum(v for k,v in sem_status.items() if k.startswith('UNRESOLVED_'))
    exact_pairs={tuple(sorted((r['left_lineage_id'],r['right_lineage_id']))) for r in exact}
    bad_sem=[]
    for r in sem:
        pair=tuple(sorted((r['left_lineage_id'],r['right_lineage_id'])))
        if r['left_lineage_id'] not in lineage_ids or r['right_lineage_id'] not in lineage_ids or r['left_source_family']==r['right_source_family'] or pair in exact_pairs:
            bad_sem.append(r['semantic_pair_candidate_id'])
        if r['authority_status'].startswith('ACCEPTED_') and (not r['portability_ceiling'] or r['portability_ceiling']=='NONE'):
            bad_sem.append(r['semantic_pair_candidate_id']+':ceiling')
    ck('reworded_high_precision_121_governed',len(sem)==121 and len(sem_ids)==121 and (sem_positive,sem_rejected,sem_unresolved)==(97,18,6) and not bad_sem,json.dumps({'positive':sem_positive,'rejected':sem_rejected,'unresolved':sem_unresolved,'bad':bad_sem[:20]}))
    ck('inherited_semantic_conflicts_flagged',sum(r['inherited_semantic_coordinate_conflict_detected']=='true' for r in sem)==12,'')

    queue2=rows(sec2/'Rawlsing_P2_Semantic_Priority_Queue_Status_v2.csv')
    remaining=rows(sec2/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_v2.csv')
    q2_by={r['semantic_pair_candidate_id']:r for r in queue2}
    adjud={r['semantic_pair_candidate_id'] for r in queue2 if r['tranche2_review_status']=='ADJUDICATED'}
    pending={r['semantic_pair_candidate_id'] for r in queue2 if r['tranche2_review_status']=='PENDING'}
    bad_q=[cid for cid in adjud if cid not in sem_ids or q2_by[cid]['tranche2_ruling_id']=='' or q2_by[cid]['tranche2_authority_status']=='PROVISIONAL_DISCOVERY_PAIR_NOT_ADJUDICATED']
    ck('semantic_queue_v2_exact_partition',len(queue2)==18831 and len(q2_by)==18831 and adjud==sem_ids and len(pending)==18710 and {r['semantic_pair_candidate_id'] for r in remaining}==pending and not bad_q,json.dumps({'adjudicated':len(adjud),'pending':len(pending),'bad':bad_q[:10]}))

    sr=rows(sec2/'Rawlsing_P2_Structure_Analogy_Rulings_v1.csv')
    sm=rows(sec2/'Rawlsing_P2_Structure_Member_Correspondence_Rulings_v1.csv')
    sr_by={r['structure_analogy_candidate_id']:r for r in sr}
    old_struct_ids={r['structure_analogy_candidate_id'] for r in analogies}
    sr_status=Counter(r['authority_status'] for r in sr)
    sm_by=defaultdict(list)
    for r in sm: sm_by[r['structure_analogy_candidate_id']].append(r)
    bad_sr=[]
    for cid,r in sr_by.items():
        xs=sm_by[cid]
        matched=sum(bool(x['left_question_implementation_id']) and bool(x['right_question_implementation_id']) for x in xs)
        left_only=sum(bool(x['left_question_implementation_id']) and not x['right_question_implementation_id'] for x in xs)
        right_only=sum(bool(x['right_question_implementation_id']) and not x['left_question_implementation_id'] for x in xs)
        if (matched,left_only,right_only)!=(int(r['matched_member_count']),int(r['left_unmatched_count']),int(r['right_unmatched_count'])): bad_sr.append(cid+':counts')
        for x in xs:
            for qid in (x['left_question_implementation_id'],x['right_question_implementation_id']):
                if qid and qid not in node_ids: bad_sr.append(cid+':endpoint')
    ck('structure_19_member_level_adjudicated',len(sr)==19 and set(sr_by)==old_struct_ids and sr_status==Counter({'ACCEPTED_FULL_MEMBER_LEVEL_STRUCTURE_ANALOGY':13,'ACCEPTED_PARTIAL_MEMBER_LEVEL_STRUCTURE_ANALOGY':5,'REJECTED_SHARED_LABEL_WITHOUT_MEMBER_EQUIVALENCE':1}) and len(sm)==119 and not bad_sr,json.dumps({'statuses':sr_status,'members':len(sm),'bad':bad_sr[:20]}))

    resolutions=rows(sec2/'Rawlsing_P2_Semantic_Reference_Anomaly_Resolution_v1.csv')
    overlay=rows(sec2/'Rawlsing_P2_Semantic_Reference_Correction_Overlay_v1.csv')
    old_anom_ids={r['anomaly_id'] for r in anomalies}; res_ids={r['anomaly_id'] for r in resolutions}
    bad_res=[r['anomaly_id'] for r in resolutions if not r['corrected_semantic_content_id'] or r['question_implementation_id'] not in node_ids or (r['inherited_semantic_content_id'] and r['inherited_semantic_content_id']==r['corrected_semantic_content_id'])]
    ck('semantic_reference_30_overlay_resolved',len(resolutions)==30 and len(overlay)==30 and res_ids==old_anom_ids and sum(r['authority_status']=='RESOLVED_SOURCE_LOCAL_COORDINATE_PARENT_UNRESOLVED' for r in resolutions)==1 and not bad_res,json.dumps(bad_res))
    bridge2=rows(sec2/'Rawlsing_P2_Semantic_Driver_Strata_Bridge_v2.csv')
    b2={r['lineage_id']:r for r in bridge2}; node_lineage={r['question_implementation_id']:r['lineage_id'] for r in nodes}
    bad_bridge=[]
    for r in resolutions:
        lid=node_lineage[r['question_implementation_id']]
        b=b2.get(lid)
        if not b or r['corrected_semantic_content_id'] not in jlist(b['semantic_content_ids_json']) or not jlist(b['semantic_reference_correction_statuses_json']): bad_bridge.append(r['anomaly_id'])
        if r['inherited_semantic_content_id'] and r['inherited_semantic_content_id'] not in jlist(b['quarantined_inherited_semantic_ids_json']): bad_bridge.append(r['anomaly_id']+':quarantine')
    ck('semantic_bridge_v2_overlay_applied',len(bridge2)==13526 and set(b2)==lineage_ids and not bad_bridge,json.dumps(bad_bridge))

    contract=json.load((sec2/'Rawlsing_V552_to_V552J_Strata_Horizon_Sidecar_Contract_v1.json').open())
    testret=json.load((sec2/'SIDECAR_SYNTHETIC_TEST_RETURN.json').open())
    adapter=sec2/'v552j_strata_horizon_sidecar_adapter.py'; testscript=sec2/'test_v552j_strata_horizon_sidecar_adapter.py'
    sidecar_run=''; sidecar_ok=False
    try:
        import subprocess
        cp=subprocess.run([sys.executable,str(testscript)],cwd=sec2,capture_output=True,text=True,timeout=30,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        sidecar_run=(cp.stdout+cp.stderr).strip(); sidecar_ok=cp.returncode==0 and 'PASS' in cp.stdout
    except Exception as e: sidecar_run=repr(e)
    required={'stratum_id','stratum_label','strata_relevance','strata_path','conditional_strata_weights','horizon_affordance','horizon_type','horizon_scope','horizon_openness','horizon_reach','horizon_valence','horizon_sustaining_power'}
    ck('strata_horizon_sidecar_contract_tested_not_installed',contract.get('status')=='AUTHORED_AND_SYNTHETICALLY_TESTED_NOT_INSTALLED_OR_RUNTIME_EXECUTED' and set(contract.get('authoritative_passthrough_fields',[]))==required and contract.get('runtime_installation_status')=='NOT_INSTALLED' and testret.get('status')=='PASS' and sidecar_ok,json.dumps({'run':sidecar_run}))

    sec2val=json.load((sec2/'VALIDATION.json').open())
    ck('tranche2_validation_current',sec2val.get('status')=='PASS' and sec2val.get('counts',{}).get('exact_accepted')==270 and sec2val.get('counts',{}).get('semantic_pair_rulings')==121 and sec2val.get('counts',{}).get('structure_rulings')==19 and sec2val.get('next_pass')==expected_v14_next,'')
    ck('tranche2_task_return_and_sources_preserved',(sec2/'TASK_RETURN.md').exists() and (sec2/'SOURCE_high_precision_121_candidate_listing.txt').exists() and (sec2/'SOURCE_exact_target_18_context.csv').exists() and (sec2/'SOURCE_structure_analogy_members_context.csv').exists(),'')


    # V14 adversarial acceptance audit and corrections.
    sec3=root/'34_P2_TRANCHE2_ACCEPTANCE_AUDIT_AND_CORRECTION'
    findings=rows(sec3/'Rawlsing_P2_Tranche2_Acceptance_Audit_Findings_v1.csv')
    ck('v14_findings_governed',len(findings)==10 and all(r['resolution_status'] in ('CORRECTED','ACCEPTED') for r in findings) and sum(r['severity']=='CRITICAL' for r in findings)==1,json.dumps(Counter(r['resolution_status'] for r in findings)))
    ev=rows(sec3/'Rawlsing_P2_Tranche2_Ruling_Evidence_Provenance_Ledger_v1.csv')
    ev_ids={r['evidence_record_id'] for r in ev}
    bad_ev=[]
    for r in ev:
        for col in ('deep_node_catalog_path','source_native_row_authority_path'):
            if r[col] and not (root/r[col]).exists(): bad_ev.append(r['evidence_record_id']+':'+col)
        if r['lineage_id'] not in lineage_ids: bad_ev.append(r['evidence_record_id']+':lineage')
        if r['evidence_sufficiency']=='COMPLETE_FOR_RECORDED_PORTABILITY_CEILING' and not jlist(r['evidence_basis_json']): bad_ev.append(r['evidence_record_id']+':basis')
    ck('v14_evidence_ledger_complete',len(ev)==278 and len(ev_ids)==278 and not bad_ev and Counter(r['side'] for r in ev)==Counter({'LEFT':139,'RIGHT':139}),json.dumps({'bad':bad_ev[:20]}))
    exv2=rows(sec3/'Rawlsing_P2_Exact_Target_Relation_Axis_Rulings_v2.csv'); rwv2=rows(sec3/'Rawlsing_P2_Reworded_Translation_High_Precision_Pair_Rulings_v2.csv')
    bad_links=[]
    for r in exv2+rwv2:
        if r['left_evidence_record_id'] not in ev_ids or r['right_evidence_record_id'] not in ev_ids: bad_links.append(r.get('target_relation_axis_ruling_id') or r.get('reworded_pair_ruling_id'))
    ck('v14_v2_rulings_evidence_linked',len(exv2)==18 and len(rwv2)==121 and not bad_links and all(r['two_sided_evidence_status'] in ('COMPLETE_EXPLICIT_PROVENANCE_LEDGER_BOTH_SIDES','EXACT_ITEMS_PRESENT_PARENT_OR_POLARITY_UNRESOLVED') for r in exv2+rwv2),json.dumps(bad_links))
    reg=rows(sec3/'Rawlsing_P2_Tranche2_Candidate_ID_Decision_Registry_v2.csv')
    ck('v14_candidate_id_decision_registry',len(reg)==139 and len({r['candidate_id'] for r in reg})==139 and set(r['decision_key_policy'] for r in reg)=={'CANDIDATE_ID_PRIMARY_SEQUENCE_DISPLAY_ONLY'},'')
    accept=rows(sec3/'Rawlsing_P2_Tranche2_Substantive_Acceptance_Audit_v1.csv')
    ck('v14_substantive_acceptance_no_reversals',len(accept)==188 and all(r['substantive_disposition_changed']=='false' for r in accept) and Counter(r['audit_surface'] for r in accept)==Counter({'REWORDED_TRANSLATION_HIGH_PRECISION':121,'SEMANTIC_REFERENCE_ANOMALY':30,'STRUCTURE_ANALOGY':19,'EXACT_TARGET_RELATION_AXIS':18}),json.dumps(Counter(r['audit_surface'] for r in accept)))
    contract2=json.load((sec3/'Rawlsing_V552_to_V552J_Strata_Horizon_Sidecar_Contract_v2.json').open())
    pytestret=json.load((sec3/'SIDECAR_V2_PYTEST_RETURN.json').open())
    try:
        cp2=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_v552j_strata_horizon_sidecar_adapter_v2.py'],cwd=sec3,capture_output=True,text=True,timeout=60,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        pytest_ok=cp2.returncode==0 and 'passed' in cp2.stdout
        pytest_detail=re.sub(r' in [0-9.]+s(?=\n|$)','',(cp2.stdout+cp2.stderr).strip())
    except Exception as e: pytest_ok=False;pytest_detail=repr(e)
    ck('v14_sidecar_v2_real_pytest',contract2.get('status')=='AUTHORED_AND_PYTESTED_NOT_INSTALLED_OR_RUNTIME_EXECUTED' and contract2.get('version')=='2.1.0' and contract2.get('runtime_installation_status')=='NOT_INSTALLED' and pytestret.get('status')=='PASS' and pytestret.get('test_count')==17 and pytest_ok,json.dumps({'run':pytest_detail}))
    # Explicitly adversarial behavior, independent of pytest result text.
    try:
        sys.path.insert(0,str(sec3)); from v552j_strata_horizon_sidecar_adapter_v2 import enrich as enrich2, FIELDS as FIELDS2
        import pandas as pd
        def mk(rows):
            out=[]
            for z in rows:
                q={f:'' for f in FIELDS2};q.update(z);out.append(q)
            return pd.DataFrame(out)
        blank_failed=False
        try: enrich2(pd.DataFrame([{'question_implementation_id':''}]),mk([{'question_implementation_id':'','stratum_id':'bad'}]))
        except ValueError: blank_failed=True
        o=enrich2(pd.DataFrame([{'question_implementation_id':'q1'},{'question_implementation_id':'q2'}]),mk([{'question_implementation_id':'q1','stratum_id':'s1'}]))
        statuses=list(o['strata_horizon_sidecar_status'])
        pre=enrich2(pd.DataFrame([{'question_implementation_id':'q1','stratum_id':'already'}]),mk([{'question_implementation_id':'q1'}]))
        trimmed=enrich2(pd.DataFrame([{'question_implementation_id':' q1 '}]),mk([{'question_implementation_id':'q1','stratum_id':'s1'}]))
        normalized_dup_failed=False
        try: enrich2(pd.DataFrame([{'question_implementation_id':'q1'}]),mk([{'question_implementation_id':'q1'},{'question_implementation_id':' q1 '}]))
        except ValueError: normalized_dup_failed=True
        structured=enrich2(pd.DataFrame([{'question_implementation_id':'q1','conditional_strata_weights':[{'b':2,'a':1}]}]),mk([{'question_implementation_id':'q1','conditional_strata_weights':'[{"a":1,"b":2}]'}]))
        adversarial_ok=(blank_failed and statuses==['V552_AUTHORITATIVE_PASS_THROUGH_MATCHED','NO_V552_SIDECAR_MATCH']
                        and pre.loc[0,'strata_horizon_sidecar_status']=='V552_SIDECAR_MATCHED_NO_AUTHORITATIVE_VALUES'
                        and trimmed.loc[0,'stratum_id']=='s1' and normalized_dup_failed
                        and structured.loc[0,'conditional_strata_weights']==[{'b':2,'a':1}])
    except Exception as e: adversarial_ok=False;pytest_detail+=' | adversarial '+repr(e)
    ck('v14_sidecar_blank_key_and_status_partition',adversarial_ok,pytest_detail)
    rebuildret=json.load((sec3/'REBUILD_V2_RETURN.json').open())
    ck('v14_candidate_keyed_rebuild_pass',rebuildret.get('status')=='PASS' and (sec3/'rebuild_tranche2_authority_surfaces_v2.py').exists(),'')
    sec3val=json.load((sec3/'VALIDATION.json').open())
    ck('v14_section_validation_current',sec3val.get('status')=='PASS' and sec3val.get('substantive_disposition_reversals')==0 and sec3val.get('counts',{}).get('evidence_records')==278 and sec3val.get('next_pass')==expected_v14_next,'')
    ck('v14_master_and_report_present',(root/'00_START_HERE'/'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v14_20260731.docx').exists() and (sec3/'Rawlsing_P2_Tranche2_Acceptance_Audit_and_Correction_Report_v1_20260731.docx').exists(),'')


    # V15 embedded acceptance standard, component-aware runtime bridge, and trust tranche 3.
    standard = root/'00_START_HERE'/'ACCEPTANCE_STANDARD_NO_REVIEW_LOOP.md'
    ck('v15_acceptance_standard_embedded', standard.exists() and 'A second review is not the default next step' in standard.read_text(encoding='utf-8') and cur.get('acceptance_standard_embedded') is True and cur.get('automatic_second_review_required') is False, '')

    sec35 = root/'35_V552J_COMPONENT_AWARE_STRATA_HORIZON_RUNTIME_BRIDGE'
    qsh_files = sorted((sec35/'generated_question_semantic_hierarchy').glob('*_question_semantic_hierarchy.csv'))
    qsh_rows = sum(len(rows(p)) for p in qsh_files)
    qsh_ret = json.load((sec35/'generated_question_semantic_hierarchy'/'QSH_REGENERATION_RETURN.json').open())
    qsh_rep = json.load((sec35/'QSH_REPRODUCIBILITY_RETURN.json').open())
    bridge_rep = json.load((sec35/'RUNTIME_BRIDGE_REPRODUCIBILITY_RETURN.json').open())
    runtime_ret = json.load((sec35/'RUNTIME_INTEGRATION_RETURN_V3_1.json').open())
    ck('v15_qsh_17_scopes_111_rows', len(qsh_files)==17 and qsh_rows==111 and qsh_ret.get('scope_files')==17 and qsh_ret.get('total_question_semantic_hierarchy_rows')==111, json.dumps({'files':len(qsh_files),'rows':qsh_rows}))
    ck('v15_qsh_deterministic_rebuild', qsh_rep.get('status')=='PASS' and qsh_rep.get('hashes_exact') is True and qsh_rep.get('tracked_files')==17, '')
    ck('v15_component_bridge_deterministic_rebuild', bridge_rep.get('status')=='PASS' and bridge_rep.get('hashes_exact') is True, '')
    bridge_rows=rows(sec35/'Rawlsing_V552J_Component_Strata_Horizon_Bridge_GSS_2010_v3_1.csv')
    packet_rows=rows(sec35/'Rawlsing_V552J_Packet_Strata_Horizon_Summary_GSS_2010_v3_1.csv')
    enriched_rows=rows(sec35/'Rawlsing_V551J_Certified_Packet_Index_GSS_2010_With_Strata_Horizon_v3_1.csv')
    ck('v15_real_component_bridge_cardinality', len(bridge_rows)==109 and len(packet_rows)==19 and len(enriched_rows)==19 and all(r['qsh_match_status'].startswith('MATCHED_') for r in bridge_rows), json.dumps({'components':len(bridge_rows),'packets':len(packet_rows)}))
    ck('v15_real_component_bridge_status_partition', runtime_ret.get('bridge_version')=='v3.1' and runtime_ret.get('matched_component_rows')==109 and runtime_ret.get('unmatched_component_rows')==0 and runtime_ret.get('packet_status_counts')=={'COMPLETE_HOMOGENEOUS_COMPONENT_AUTHORITY':19}, json.dumps(runtime_ret))
    try:
        cp35=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_ddm_v552j_component_strata_horizon_bridge.py'],cwd=sec35,capture_output=True,text=True,timeout=90,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        bridge_pytest_ok=cp35.returncode==0 and '18 passed' in cp35.stdout
        bridge_pytest_detail=(cp35.stdout+cp35.stderr).strip()
    except Exception as e:
        bridge_pytest_ok=False; bridge_pytest_detail=repr(e)
    ck('v15_component_bridge_18_real_tests',bridge_pytest_ok,bridge_pytest_detail)
    ck('v15_component_bridge_live_installation_boundary',runtime_ret.get('installation_status')=='COMPONENT_BRIDGE_VALIDATED_AGAINST_RECOVERED_RUNTIME_SNAPSHOT_NOT_WRITTEN_TO_USER_LIVE_REPOSITORY','')

    sec36 = root/'36_P2_GLOBAL_TRUST_SEMANTIC_NEIGHBORHOOD_ADJUDICATION_TRANCHE3'
    trust_class=rows(sec36/'Rawlsing_P2_Trust_Lineage_Axis_Target_Classification_v2.csv')
    trust_rulings=rows(sec36/'Rawlsing_P2_Trust_Neighborhood_Pair_Rulings_v2.csv')
    trust_ev=rows(sec36/'Rawlsing_P2_Trust_Neighborhood_Two_Sided_Evidence_Ledger_v2.csv')
    trust_remaining=rows(sec36/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Trust_Tranche_v3.csv')
    trust_ret=json.load((sec36/'TRUST_ADJUDICATION_RETURN_V2.json').open())
    trust_rep=json.load((sec36/'TRUST_REPRODUCIBILITY_RETURN.json').open())
    ruling_ids={r['trust_pair_ruling_id'] for r in trust_rulings}
    ev_count=Counter(r['trust_pair_ruling_id'] for r in trust_ev)
    ev_sides=defaultdict(set)
    for r in trust_ev: ev_sides[r['trust_pair_ruling_id']].add(r['side'])
    ck('v15_trust_queue_partition_exact',len(trust_rulings)==3863 and len(trust_remaining)==14847 and len(trust_rulings)+len(trust_remaining)==18710 and len({r['semantic_pair_candidate_id'] for r in trust_rulings})==3863 and not ({r['semantic_pair_candidate_id'] for r in trust_rulings}&{r['semantic_pair_candidate_id'] for r in trust_remaining}),json.dumps({'rulings':len(trust_rulings),'remaining':len(trust_remaining)}))
    ck('v15_trust_lineage_classification_exact',len(trust_class)==562 and len({r['lineage_id'] for r in trust_class})==562 and Counter(r['authority_status'] for r in trust_class)==Counter({'P2_NONTRUST_EXCLUSION_CLASSIFIED':412,'P2_TRUST_LINEAGE_AXIS_TARGET_CLASSIFIED':148,'P2_TRUST_LINEAGE_CLASSIFICATION_UNRESOLVED':2}),json.dumps(Counter(r['authority_status'] for r in trust_class)))
    ck('v15_trust_two_sided_evidence_exact',len(trust_ev)==7726 and set(ev_count)==ruling_ids and all(v==2 for v in ev_count.values()) and all(v=={'LEFT','RIGHT'} for v in ev_sides.values()),'')
    bad_prop=[r['trust_pair_ruling_id'] for r in trust_rulings if r['authority_status']=='ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION' and (r['left_relation_axis']!=r['right_relation_axis'] or r['left_target_entity']!=r['right_target_entity'] or r['relation_type']!='REWORDED_PROPOSITION_EQUIVALENCE')]
    ck('v15_trust_proposition_axis_target_gate',not bad_prop,json.dumps(bad_prop[:20]))
    unresolved_lineages={r['lineage_id'] for r in trust_class if r['authority_status']=='P2_TRUST_LINEAGE_CLASSIFICATION_UNRESOLVED'}
    bad_hetero=[r['trust_pair_ruling_id'] for r in trust_rulings if ({r['left_lineage_id'],r['right_lineage_id']} & unresolved_lineages) and r['authority_status']!='UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_RELATION_AXIS_OR_TARGET_EVIDENCE']
    ck('v15_heterogeneous_lineages_fail_closed',not bad_hetero,json.dumps(bad_hetero[:20]))
    expected_status_counts=Counter({'ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY':76,'ACCEPTED_NONTRUST_RELATION_REDIRECTED_FROM_CONTAMINATED_TRUST_NEIGHBORHOOD':7,'ACCEPTED_TRUST_CONSTRUCT_COORDINATE_WITH_DERIVED_INDEX':30,'ACCEPTED_TRUST_CONSTRUCT_OR_TARGET_COORDINATE_ONLY':1,'ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION':329,'REDIRECTED_OUT_OF_TRUST_NEIGHBORHOOD_OTHER_DOMAIN_NOT_ADJUDICATED':1413,'REJECTED_CONTAMINATED_TRUST_NEIGHBORHOOD_NONTRUST_MISMATCH':65,'REJECTED_FALSE_EQUIVALENCE_TARGET_OR_TRUST_AXIS_MISMATCH':330,'REJECTED_TRUST_VERSUS_NONTRUST_OPERATOR_MISMATCH':1531,'UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_RELATION_AXIS_OR_TARGET_EVIDENCE':81})
    ck('v15_trust_authority_partition_exact',Counter(r['authority_status'] for r in trust_rulings)==expected_status_counts,json.dumps(Counter(r['authority_status'] for r in trust_rulings)))
    typo_lineage=next((r for r in trust_class if r['lineage_id']=='p2lineage_f47e6b84e36bddf926693820'),None)
    typo_pair=next((r for r in trust_rulings if r['semantic_pair_candidate_id']=='p2sempair_512304291ed8221bfe859cd9'),None)
    ck('v15_pollice_typo_target_recovered',typo_lineage is not None and typo_lineage['governed_target_entity']=='police_assistance_service' and typo_pair is not None and typo_pair['authority_status']=='ACCEPTED_NONTRUST_RELATION_REDIRECTED_FROM_CONTAMINATED_TRUST_NEIGHBORHOOD','')
    ck('v15_trust_deterministic_rebuild',trust_rep.get('status')=='PASS' and trust_rep.get('hashes_exact') is True and trust_rep.get('tracked_files')==5,'')
    try:
        cp36=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_trust_adjudication_v2.py'],cwd=sec36,capture_output=True,text=True,timeout=90,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        trust_pytest_ok=cp36.returncode==0 and '16 passed' in cp36.stdout
        trust_pytest_detail=(cp36.stdout+cp36.stderr).strip()
    except Exception as e:
        trust_pytest_ok=False; trust_pytest_detail=repr(e)
    ck('v15_trust_16_adversarial_tests',trust_pytest_ok,trust_pytest_detail)
    ck('v15_v16_history_and_v17_resume_current',cur.get('semantic_priority_pairs_remaining')==8847 and scope.get('trust_tranche3',{}).get('pairs_remaining')==14847 and scope.get('fixed_tranche_protocol',{}).get('tranche4_end')==11847 and scope.get('fixed_tranche_protocol',{}).get('tranche5_end')==8847 and scope.get('next_pass')==expected_next and val.get('next_pass')==expected_next,'')
    ck('v15_master_and_reports_present',(root/'00_START_HERE'/'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v15_20260731.docx').exists() and (sec35/'Rawlsing_V552J_Component_Strata_Horizon_Runtime_Bridge_v3_1_Report_20260731.docx').exists() and (sec36/'Rawlsing_P2_Global_Trust_Neighborhood_Tranche3_Report_20260731.docx').exists(),'')
    debris=[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir() and p.name in ('__pycache__','.pytest_cache')]
    debris += [p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.suffix in ('.pyc','.pyo')]
    ck('v15_no_generated_test_or_bytecode_debris',not debris,json.dumps(debris))



    # V16 exact fixed-3000 democracy/electoral tranche 4.
    sec37=root/'37_P2_GLOBAL_DEMOCRACY_ELECTORAL_FIXED_3000_TRANCHE4'
    fixed_candidates=rows(sec37/'Rawlsing_P2_Fixed_3000_Tranche_Candidate_Surface_v1.csv')
    fixed_class=rows(sec37/'Rawlsing_P2_Democracy_Electoral_Lineage_Classification_v1.csv')
    fixed_rulings=rows(sec37/'Rawlsing_P2_Democracy_Electoral_3000_Pair_Rulings_v1.csv')
    fixed_ev=rows(sec37/'Rawlsing_P2_Democracy_Electoral_3000_Two_Sided_Evidence_Ledger_v1.csv')
    fixed_remaining=rows(sec37/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Fixed_3000_Tranche_v4.csv')
    fixed_ret=json.load((sec37/'FIXED_3000_TRANCHE_RETURN.json').open())
    fixed_rep=json.load((sec37/'FIXED_3000_REPRODUCIBILITY_RETURN.json').open())
    trust_pending_ids={r['semantic_pair_candidate_id'] for r in trust_remaining}
    selected_ids={r['semantic_pair_candidate_id'] for r in fixed_candidates}
    remaining_ids={r['semantic_pair_candidate_id'] for r in fixed_remaining}
    ruling_candidate_ids={r['semantic_pair_candidate_id'] for r in fixed_rulings}
    ck('v16_fixed_work_unit_exactly_3000',len(fixed_candidates)==3000 and len(fixed_rulings)==3000 and fixed_ret.get('fixed_work_unit_pairs')==3000 and cur.get('fixed_semantic_pair_work_unit')==3000,json.dumps({'candidates':len(fixed_candidates),'rulings':len(fixed_rulings)}))
    ck('v16_queue_partition_14847_to_11847',len(fixed_remaining)==11847 and selected_ids.isdisjoint(remaining_ids) and selected_ids|remaining_ids==trust_pending_ids and ruling_candidate_ids==selected_ids,json.dumps({'selected':len(selected_ids),'remaining':len(remaining_ids),'incoming':len(trust_pending_ids)}))
    expected_sel=Counter({'DEMO_EXTENT':843,'CIVIC_VOTE_MATTERS':810,'CIVIC_VOTE':783,'REJECT_STRONGMAN':333,'REJECT_MILITARY':204,'REJECT_ONEPARTY':27})
    ck('v16_deterministic_selection_contract',Counter(r['semantic_content_id'] for r in fixed_candidates)==expected_sel,json.dumps(Counter(r['semantic_content_id'] for r in fixed_candidates)))
    fixed_class_ids={r['classification_id'] for r in fixed_class}; fixed_lineages={r['lineage_id'] for r in fixed_class}; fixed_ruling_ids={r['pair_ruling_id'] for r in fixed_rulings}
    ev_count=Counter(r['pair_ruling_id'] for r in fixed_ev); ev_sides=defaultdict(set)
    for r in fixed_ev: ev_sides[r['pair_ruling_id']].add(r['side'])
    ck('v16_lineage_and_id_integrity',len(fixed_class)==488 and len(fixed_class_ids)==488 and len(fixed_lineages)==488 and len(fixed_ruling_ids)==3000 and len({r['evidence_record_id'] for r in fixed_ev})==6000,'')
    ck('v16_two_sided_evidence_6000',len(fixed_ev)==6000 and set(ev_count)==fixed_ruling_ids and all(v==2 for v in ev_count.values()) and all(v=={'LEFT','RIGHT'} for v in ev_sides.values()) and all(r['classification_id'] in fixed_class_ids and r['lineage_id'] in fixed_lineages for r in fixed_ev),'')
    expected_fixed_status=Counter({'ACCEPTED_DOMAIN_COORDINATE_ONLY_RELATION_OR_TARGET_SCOPE_DIFFERS':201,'ACCEPTED_SAME_CONSTRUCT_TARGET_DIFFERENT_OPERATOR_COORDINATE_ONLY':19,'ACCEPTED_TYPED_DEMOCRACY_ELECTORAL_PROPOSITION_RELATION':13,'REDIRECTED_OUT_OF_DEMOCRACY_ELECTORAL_DOMAIN_SHARED_OTHER_AXIS_NOT_ADJUDICATED':92,'REJECTED_CONTAMINATED_NEIGHBORHOOD_OTHER_DOMAIN_MISMATCH':1305,'REJECTED_DEMOCRACY_ELECTORAL_VERSUS_OTHER_DOMAIN_MISMATCH':1163,'REJECTED_DIFFERENT_GOVERNED_RELATION_AXES':28,'REJECTED_FALSE_EQUIVALENCE_DEMOCRACY_ELECTORAL_RELATION_OR_TARGET_MISMATCH':171,'UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_SOURCE_LOCAL_EVIDENCE':8})
    ck('v16_authority_partition_exact',Counter(r['authority_status'] for r in fixed_rulings)==expected_fixed_status,json.dumps(Counter(r['authority_status'] for r in fixed_rulings)))
    accepted_fixed=[r for r in fixed_rulings if r['authority_status']=='ACCEPTED_TYPED_DEMOCRACY_ELECTORAL_PROPOSITION_RELATION']
    class_by={r['lineage_id']:r for r in fixed_class}
    bad_fixed_accept=[r['pair_ruling_id'] for r in accepted_fixed if not (r['left_relation_axis']==r['right_relation_axis'] and r['left_target_or_scope']==r['right_target_or_scope'] and r['left_operator']==r['right_operator'] and class_by[r['left_lineage_id']]['classification_confidence']=='HIGH' and class_by[r['right_lineage_id']]['classification_confidence']=='HIGH')]
    ck('v16_proposition_equivalence_axis_target_operator_gate',len(accepted_fixed)==13 and not bad_fixed_accept,json.dumps(bad_fixed_accept))
    ck('v16_reproducibility_hash_exact',fixed_rep.get('status')=='PASS' and fixed_rep.get('hashes_exact') is True and fixed_rep.get('tracked_files')==6,'')
    try:
        env37={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','RAWLSING_V15_ROOT':str(root),'RAWLSING_V16_OUT':str(sec37),'RAWLSING_V16_BUILDER':str(sec37/'build_democracy_electoral_tranche_v1.py')}
        cp37=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_fixed_3000_democracy_electoral_tranche_v1.py'],cwd=sec37,capture_output=True,text=True,timeout=120,env=env37)
        fixed_pytest_ok=cp37.returncode==0 and '20 passed' in cp37.stdout
        fixed_pytest_detail=(cp37.stdout+cp37.stderr).strip()
    except Exception as e:
        fixed_pytest_ok=False; fixed_pytest_detail=repr(e)
    ck('v16_fixed_tranche_20_adversarial_tests',fixed_pytest_ok,fixed_pytest_detail)
    ck('v16_history_fixed_protocol_and_v17_resume_embedded',(root/'00_START_HERE'/'FIXED_3000_TRANCHE_PROTOCOL.md').exists() and cur.get('fixed_tranche_protocol_embedded') is True and cur.get('semantic_priority_pairs_adjudicated_cumulative')==9984 and cur.get('semantic_priority_pairs_remaining')==8847 and val.get('fixed_tranche_protocol',{}).get('pairs_remaining')==8847,'')
    ck('v16_master_and_report_present',(root/'00_START_HERE'/'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v16_20260731.docx').exists() and (sec37/'Rawlsing_P2_Global_Democracy_Electoral_Fixed_3000_Tranche4_Report_20260731.docx').exists(),'')
    debris=[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir() and p.name in ('__pycache__','.pytest_cache')]
    debris += [p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.suffix in ('.pyc','.pyo')]
    ck('v16_no_generated_test_or_bytecode_debris',not debris,json.dumps(debris))



    # V17 exact fixed-3000 media/civic tranche 5.
    sec38=root/'38_P2_GLOBAL_MEDIA_CIVIC_FIXED_3000_TRANCHE5'
    mc_candidates=rows(sec38/'Rawlsing_P2_Media_Civic_Fixed_3000_Tranche_Candidate_Surface_v1.csv')
    mc_class=rows(sec38/'Rawlsing_P2_Media_Civic_Lineage_Classification_v1.csv')
    mc_rulings=rows(sec38/'Rawlsing_P2_Media_Civic_3000_Pair_Rulings_v1.csv')
    mc_ev=rows(sec38/'Rawlsing_P2_Media_Civic_3000_Two_Sided_Evidence_Ledger_v1.csv')
    mc_remaining=rows(sec38/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Media_Civic_Fixed_3000_Tranche_v5.csv')
    mc_ret=json.load((sec38/'FIXED_3000_MEDIA_CIVIC_TRANCHE_RETURN.json').open())
    mc_rep=json.load((sec38/'FIXED_3000_MEDIA_CIVIC_REPRODUCIBILITY_RETURN.json').open())
    mc_review=json.load((sec38/'FIXED_3000_MEDIA_CIVIC_ACCEPTANCE_REVIEW_RETURN.json').open())
    fixed4_pending_ids={r['semantic_pair_candidate_id'] for r in fixed_remaining}
    mc_selected_ids={r['semantic_pair_candidate_id'] for r in mc_candidates}
    mc_remaining_ids={r['semantic_pair_candidate_id'] for r in mc_remaining}
    mc_ruling_candidate_ids={r['semantic_pair_candidate_id'] for r in mc_rulings}
    ck('v17_fixed_work_unit_exactly_3000',len(mc_candidates)==3000 and len(mc_rulings)==3000 and mc_ret.get('fixed_work_unit_pairs')==3000 and cur.get('fixed_semantic_pair_work_unit')==3000,json.dumps({'candidates':len(mc_candidates),'rulings':len(mc_rulings)}))
    ck('v17_queue_partition_11847_to_8847',len(mc_remaining)==8847 and mc_selected_ids.isdisjoint(mc_remaining_ids) and mc_selected_ids|mc_remaining_ids==fixed4_pending_ids and mc_ruling_candidate_ids==mc_selected_ids,json.dumps({'selected':len(mc_selected_ids),'remaining':len(mc_remaining_ids),'incoming':len(fixed4_pending_ids)}))
    expected_mc_sel=Counter({'MEDIA_NEWS_SOURCE':893,'MEDIA_INTERNET':601,'CIVIC_DISCUSS_POLITICS':554,'CIVIC_INTEREST_POLITICS':527,'CIVIC_DEMONSTRATION':425})
    ck('v17_deterministic_selection_contract',Counter(r['semantic_content_id'] for r in mc_candidates)==expected_mc_sel,json.dumps(Counter(r['semantic_content_id'] for r in mc_candidates)))
    mc_class_ids={r['classification_id'] for r in mc_class}; mc_lineages={r['lineage_id'] for r in mc_class}; mc_ruling_ids={r['pair_ruling_id'] for r in mc_rulings}
    mc_ev_count=Counter(r['pair_ruling_id'] for r in mc_ev); mc_ev_sides=defaultdict(set)
    for r in mc_ev: mc_ev_sides[r['pair_ruling_id']].add(r['side'])
    ck('v17_lineage_and_id_integrity',len(mc_class)==379 and len(mc_class_ids)==379 and len(mc_lineages)==379 and len(mc_ruling_ids)==3000 and len({r['evidence_record_id'] for r in mc_ev})==6000,'')
    ck('v17_two_sided_evidence_6000',len(mc_ev)==6000 and set(mc_ev_count)==mc_ruling_ids and all(v==2 for v in mc_ev_count.values()) and all(v=={'LEFT','RIGHT'} for v in mc_ev_sides.values()) and all(r['classification_id'] in mc_class_ids and r['lineage_id'] in mc_lineages for r in mc_ev),'')
    expected_mc_status=Counter({'ACCEPTED_DOMAIN_COORDINATE_ONLY_RELATION_OR_TARGET_SCOPE_DIFFERS':287,'ACCEPTED_SAME_CONSTRUCT_TARGET_DIFFERENT_OPERATOR_OR_INCOMPLETE_EVIDENCE_COORDINATE_ONLY':25,'ACCEPTED_TYPED_MEDIA_CIVIC_PROPOSITION_RELATION':72,'REDIRECTED_OUT_OF_MEDIA_CIVIC_DOMAIN_SHARED_OTHER_AXIS_NOT_ADJUDICATED':27,'REJECTED_CONTAMINATED_NEIGHBORHOOD_OTHER_DOMAIN_MISMATCH':404,'REJECTED_FALSE_EQUIVALENCE_MEDIA_CIVIC_RELATION_OR_TARGET_MISMATCH':1017,'REJECTED_MEDIA_CIVIC_VERSUS_OTHER_DOMAIN_MISMATCH':1133,'UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_SOURCE_LOCAL_EVIDENCE':35})
    ck('v17_authority_partition_exact',Counter(r['authority_status'] for r in mc_rulings)==expected_mc_status,json.dumps(Counter(r['authority_status'] for r in mc_rulings)))
    mc_class_by={r['lineage_id']:r for r in mc_class}
    mc_accepted=[r for r in mc_rulings if r['authority_status']=='ACCEPTED_TYPED_MEDIA_CIVIC_PROPOSITION_RELATION']
    bad_mc_accept=[r['pair_ruling_id'] for r in mc_accepted if not (r['left_relation_axis']==r['right_relation_axis'] and r['left_target_or_scope']==r['right_target_or_scope'] and r['left_operator']==r['right_operator'] and mc_class_by[r['left_lineage_id']]['classification_confidence']=='HIGH' and mc_class_by[r['right_lineage_id']]['classification_confidence']=='HIGH')]
    ck('v17_proposition_equivalence_axis_target_operator_gate',len(mc_accepted)==72 and not bad_mc_accept,json.dumps(bad_mc_accept))
    medium_mc={r['lineage_id'] for r in mc_class if r['classification_confidence']=='MEDIUM'}
    accepted_mc_lineages={r['left_lineage_id'] for r in mc_accepted}|{r['right_lineage_id'] for r in mc_accepted}
    ck('v17_medium_confidence_never_exports_proposition_authority',not (medium_mc & accepted_mc_lineages),json.dumps(sorted(medium_mc & accepted_mc_lineages)))
    unresolved_mc={r['lineage_id'] for r in mc_class if r['authority_status']=='P2_MEDIA_CIVIC_LINEAGE_UNRESOLVED'}
    unresolved_mc_rulings=[r for r in mc_rulings if r['relation_type']=='UNRESOLVED']
    ck('v17_unresolved_surface_bounded_to_two_lineages',unresolved_mc=={'p2lineage_a153e49c62457bf801d60b1b','p2lineage_78193a6f13f138c9728f81d8'} and len(unresolved_mc_rulings)==35 and all(r['left_lineage_id'] in unresolved_mc or r['right_lineage_id'] in unresolved_mc for r in unresolved_mc_rulings),json.dumps({'lineages':sorted(unresolved_mc),'pairs':len(unresolved_mc_rulings)}))
    ck('v17_reproducibility_hash_exact',mc_rep.get('status')=='PASS' and mc_rep.get('hashes_exact') is True and mc_rep.get('tracked_files')==6,'')
    ck('v17_acceptance_review_complete',mc_review.get('status')=='PASS' and mc_review.get('accepted_proposition_pairs_reviewed')==72 and mc_review.get('unresolved_pairs_reviewed')==35 and mc_review.get('exact_text_exception_is_material_axis_difference') is True,'')
    try:
        env38={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','RAWLSING_V16_ROOT':str(root),'RAWLSING_V17_OUT':str(sec38),'RAWLSING_V17_BUILDER':str(sec38/'build_media_civic_tranche_v1.py'),'RAWLSING_FIXED_3000_SELECTION':str(sec38/'fixed_tranche5_3000_candidates.csv')}
        cp38=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_fixed_3000_media_civic_tranche_v1.py'],cwd=sec38,capture_output=True,text=True,timeout=120,env=env38)
        mc_pytest_ok=cp38.returncode==0 and '25 passed' in cp38.stdout
        mc_pytest_detail=(cp38.stdout+cp38.stderr).strip()
    except Exception as e:
        mc_pytest_ok=False; mc_pytest_detail=repr(e)
    ck('v17_media_civic_25_adversarial_tests',mc_pytest_ok,mc_pytest_detail)
    ck('v17_current_controls_and_cumulative_counts',cur.get('handoff_version')=='v17' and cur.get('semantic_priority_pairs_adjudicated_cumulative')==9984 and cur.get('semantic_priority_pairs_remaining')==8847 and scope.get('fixed_tranche_protocol',{}).get('tranche5_start')==11847 and scope.get('fixed_tranche_protocol',{}).get('tranche5_end')==8847 and val.get('fixed_tranche_protocol',{}).get('pairs_remaining')==8847,'')
    ck('v17_master_and_report_present',(root/'00_START_HERE'/'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v17_20260731.docx').exists() and (sec38/'Rawlsing_P2_Global_Media_Civic_Fixed_3000_Tranche5_Report_20260731.docx').exists(),'')
    debris=[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir() and p.name in ('__pycache__','.pytest_cache')]
    debris += [p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.suffix in ('.pyc','.pyo')]
    ck('v17_no_generated_test_or_bytecode_debris',not debris,json.dumps(debris))

    result={'status':'PASS' if not failures else 'FAIL','root':str(root),'checks_passed':sum(x['status']=='PASS' for x in checks),'checks_total':len(checks),'file_count':file_count,'recursive_archive_instances':archive_instances,'unique_archive_payloads':len(seen),'failures':failures,'checks':checks}
    out=json.dumps(result,indent=2,ensure_ascii=False)
    if a.json_out: Path(a.json_out).write_text(out+'\n',encoding='utf-8')
    print(out)
    raise SystemExit(0 if not failures else 1)
if __name__=='__main__': main()
