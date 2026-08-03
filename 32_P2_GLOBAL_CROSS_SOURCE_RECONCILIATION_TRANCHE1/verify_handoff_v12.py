#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, hashlib, io, json, sys, zipfile
from pathlib import Path
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
    ap=argparse.ArgumentParser(description='Read-only v12 cumulative handoff verifier')
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
            if p.stat().st_size==0: raise ValueError('empty')
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
    expected_next='P2_GLOBAL_REWORDED_TRANSLATION_TARGET_RELATION_AXIS_AND_STRUCTURE_ADJUDICATION'
    ck('restart_controls_current',cur.get('handoff_version')=='v12' and scope.get('current_pass')==cur.get('current_pass') and scope.get('next_pass')==expected_next and val.get('p2_global_reconciliation_tranche1',{}).get('next_pass')==expected_next and len(cur.get('source_local_deep_passes_closed',[]))==9,'')
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
    ck('tranche_validation_current',secval.get('status')=='PASS' and secval.get('counts',{}).get('exact_accepted')==256 and secval.get('counts',{}).get('structure_memberships')==15990 and secval.get('next_pass')==expected_next,'')

    result={'status':'PASS' if not failures else 'FAIL','root':str(root),'checks_passed':sum(x['status']=='PASS' for x in checks),'checks_total':len(checks),'file_count':file_count,'recursive_archive_instances':archive_instances,'unique_archive_payloads':len(seen),'failures':failures,'checks':checks}
    out=json.dumps(result,indent=2,ensure_ascii=False)
    if a.json_out: Path(a.json_out).write_text(out+'\n',encoding='utf-8')
    print(out)
    raise SystemExit(0 if not failures else 1)
if __name__=='__main__': main()
