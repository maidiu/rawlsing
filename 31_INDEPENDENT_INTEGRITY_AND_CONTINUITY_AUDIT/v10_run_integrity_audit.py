from __future__ import annotations
import csv, json, hashlib, os, sys, zipfile, re
from pathlib import Path
from collections import defaultdict, Counter

csv.field_size_limit(sys.maxsize)
BASE=Path('/mnt/data/rawlsing_audit')
V10=BASE/'v10'/'Rawlsing_J_Family_Authority_Strategy_Handoff_v10_20260731'
P2=BASE/'p2v2'/'Rawlsing_P2_Remaining_Four_Calibre_Audit_and_Closure_v2_20260731'
PHASE0=V10/'08_P2_PHASE0'/'Rawlsing_P2_Phase0_Governed_Question_Node_Catalog_v1.json'
OUT=BASE/'independent_audit'
OUT.mkdir(exist_ok=True)

def sha256_file(p:Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def read_csv(p:Path):
    with p.open(encoding='utf-8-sig',newline='') as f:
        return list(csv.DictReader(f))

def one(root:Path,pat:str)->Path:
    xs=list(root.glob(pat))
    if len(xs)!=1: raise RuntimeError((root,pat,[str(x) for x in xs]))
    return xs[0]

def check_manifest(root:Path):
    res=[]
    idx=root/'PACKAGE_INDEX.csv'; sums=root/'SHA256SUMS.csv'
    for manifest,kind in [(idx,'index'),(sums,'sums')]:
        if not manifest.exists():
            res.append({'check':f'{kind}_present','status':'FAIL','detail':str(manifest)}); continue
        rows=read_csv(manifest)
        bad=[]; missing=[]; sizebad=[]
        for r in rows:
            p=root/r['relative_path']
            if not p.exists(): missing.append(r['relative_path']); continue
            got=sha256_file(p)
            if got!=r['sha256']: bad.append(r['relative_path'])
            if 'bytes' in r and str(p.stat().st_size)!=str(r['bytes']): sizebad.append(r['relative_path'])
        res.append({'check':f'{kind}_hashes','status':'PASS' if not(bad or missing or sizebad) else 'FAIL','detail':json.dumps({'rows':len(rows),'bad':bad,'missing':missing,'sizebad':sizebad})})
        actual={str(p.relative_to(root)).replace(os.sep,'/') for p in root.rglob('*') if p.is_file() and p not in (idx,sums)}
        listed={r['relative_path'] for r in rows}
        res.append({'check':f'{kind}_coverage','status':'PASS' if actual==listed else 'FAIL','detail':json.dumps({'actual':len(actual),'listed':len(listed),'only_actual':sorted(actual-listed),'only_listed':sorted(listed-actual)})})
    return res

phase=json.load(PHASE0.open())
phase_impl=phase['question_implementations']
phase_by_source=defaultdict(set)
for r in phase_impl: phase_by_source[r['source_family']].add(r['question_implementation_id'])
phase_all=set().union(*phase_by_source.values())

# Source roots in governing handoff.
roots={
 'GSS':V10/'09_P2_GSS_PASS1',
 'WVS':V10/'10_P2_WVS_PASS1',
 'EVS':V10/'12_P2_EVS_PASS1',
 'Arab Barometer':V10/'15_P2_ARAB_BAROMETER_PASS1',
 'Afrobarometer':V10/'19_P2_AFROBAROMETER_PASS1',
 'Asian Barometer':V10/'24_P2_ASIAN_BAROMETER_PASS1'/'PACKAGE_CONTENTS',
 'Latinobarómetro':V10/'25_P2_LATINOBAROMETRO_PASS1'/'PACKAGE_CONTENTS',
 'South Asia':V10/'26_P2_SOUTH_ASIA_PASS1'/'PACKAGE_CONTENTS',
 'LiTS':V10/'27_P2_LITS_PASS1'/'PACKAGE_CONTENTS',
}
closure={r['source_family']:r for r in read_csv(V10/'28_P2_ALL_NINE_SOURCE_LOCAL_CLOSURE'/'Rawlsing_P2_All_Nine_Source_Local_Closure_Summary_v2.csv')}

source_results={}
source_summary=[]
all_node_ids=set()
for source,root in roots.items():
    checks=[]
    # locate artifacts across v1/v2 layouts
    nodep=one(root,'**/*Deep_Question_Node_Catalog*.csv')
    nodes=read_csv(nodep); ids=[r['question_implementation_id'] for r in nodes]; idset=set(ids)
    all_node_ids |= idset
    gapsps=list(root.glob('**/*Response_Authority_Gaps*.csv'))
    gap_rows=read_csv(gapsps[0]) if gapsps else []
    status_gap_ids={r['question_implementation_id'] for r in nodes if 'gap' in r.get('response_binding_status','').lower() or r.get('response_binding_status') in ('unbound','blocked')}
    gapids={r['question_implementation_id'] for r in gap_rows} if gap_rows else status_gap_ids
    gaps=[{'question_implementation_id':x} for x in sorted(gapids)]
    if gap_rows:
        checks.append({'check':'gap_file_matches_node_status','status':'PASS' if gapids==status_gap_ids else 'FAIL','detail':json.dumps({'file':len(gapids),'status':len(status_gap_ids),'file_only':len(gapids-status_gap_ids),'status_only':len(status_gap_ids-gapids)})})
    edgep=one(root,'**/*Accepted_Longitudinal_Continuity_Edges*.csv')
    edges=read_csv(edgep)
    invp=one(root,'**/*Source_Structure_Inventory*.csv'); inv=read_csv(invp)
    memps=list(root.glob('**/*Source_Structure_Memberships*.csv')); mem=read_csv(memps[0]) if memps else []
    checks.append({'check':'node_id_unique','status':'PASS' if len(ids)==len(idset) and '' not in idset else 'FAIL','detail':f'{len(ids)} rows / {len(idset)} unique'})
    expected=phase_by_source[source]
    checks.append({'check':'phase0_exact_identity_set','status':'PASS' if idset==expected else 'FAIL','detail':json.dumps({'deep':len(idset),'phase0':len(expected),'deep_only':len(idset-expected),'phase0_only':len(expected-idset)})})
    checks.append({'check':'gap_ids_subset_nodes','status':'PASS' if gapids<=idset else 'FAIL','detail':f'{len(gapids)} gaps; orphan={len(gapids-idset)}'})
    c=closure[source]
    checks.append({'check':'closure_node_count','status':'PASS' if len(nodes)==int(c['nodes']) else 'FAIL','detail':f"actual={len(nodes)} closure={c['nodes']}"})
    checks.append({'check':'closure_gap_count','status':'PASS' if len(gaps)==int(c['response_gaps']) else 'FAIL','detail':f"actual={len(gaps)} closure={c['response_gaps']}"})
    checks.append({'check':'closure_bound_arithmetic','status':'PASS' if len(nodes)-len(gaps)==int(c['response_bound']) else 'FAIL','detail':f"nodes-gaps={len(nodes)-len(gaps)} closure={c['response_bound']}"})
    # edges
    eids=[r.get('continuity_edge_id','') for r in edges]
    orphan=[]; self_edges=[]; badstatus=[]
    epairs=set()
    for r in edges:
        l=r['left_question_implementation_id']; rr=r['right_question_implementation_id']; epairs.add((l,rr))
        if l not in idset or rr not in idset: orphan.append((l,rr))
        if l==rr: self_edges.append((l,rr))
        if 'ACCEPTED' not in r.get('authority_status',''): badstatus.append(r.get('authority_status',''))
    checks.append({'check':'edge_ids_unique','status':'PASS' if len(eids)==len(set(eids)) and '' not in set(eids) else 'FAIL','detail':f'{len(eids)} rows / {len(set(eids))} unique'})
    checks.append({'check':'edge_referential_integrity','status':'PASS' if not(orphan or self_edges or badstatus) else 'FAIL','detail':json.dumps({'orphan':len(orphan),'self':len(self_edges),'badstatus':Counter(badstatus)})})
    checks.append({'check':'closure_edge_count','status':'PASS' if len(edges)==int(c['accepted_continuity_edges']) else 'FAIL','detail':f"actual={len(edges)} closure={c['accepted_continuity_edges']}"})
    # structures
    sid_key='structure_id' if 'structure_id' in inv[0] else 'source_structure_id'
    sids=[r[sid_key] for r in inv]; sidset=set(sids)
    checks.append({'check':'structure_ids_unique','status':'PASS' if len(sids)==len(sidset) and '' not in sidset else 'FAIL','detail':f'{len(sids)} rows / {len(sidset)} unique'})
    checks.append({'check':'closure_structure_count','status':'PASS' if len(inv)==int(c['source_structures']) else 'FAIL','detail':f"actual={len(inv)} closure={c['source_structures']}"})
    if mem:
        mem_sid_key='structure_id' if 'structure_id' in mem[0] else 'source_structure_id'
        orphs=[r for r in mem if r[mem_sid_key] not in sidset]
        if 'question_implementation_id' in mem[0]:
            orphn=[r for r in mem if r['question_implementation_id'] not in idset]
        else:
            node_keys={(r.get('wave',''),r.get('source_variable_code','')) for r in nodes}
            orphn=[r for r in mem if (r.get('wave',''),r.get('source_variable_code','')) not in node_keys]
        counts=Counter(r[mem_sid_key] for r in mem)
        mismatch=[]
        for r in inv:
            if r.get('member_count') not in ('',None) and int(float(r['member_count']))!=counts[r[sid_key]]: mismatch.append((r[sid_key],r['member_count'],counts[r[sid_key]]))
        checks.append({'check':'structure_membership_integrity','status':'PASS' if not(orphs or orphn or mismatch) else 'FAIL','detail':json.dumps({'memberships':len(mem),'orphan_structures':len(orphs),'orphan_nodes':len(orphn),'member_count_mismatch':len(mismatch)})})
    # v2-specific surfaces
    acceptedp=list(root.glob('**/*Accepted_Wording_Revision_Rulings*.csv')); accepted=read_csv(acceptedp[0]) if acceptedp else []
    guardps=list(root.glob('**/*Code_Reuse*Guards*.csv'))+list(root.glob('**/*Anti_Continuity_Guards*.csv'))+list(root.glob('**/*Positional_Code_Anti_Continuity_Guards*.csv'))
    guards=[]
    seenp=set()
    for p in guardps:
        if p in seenp: continue
        seenp.add(p); guards.extend(read_csv(p))
    reviewps=list(root.glob('**/*Wording_Revision_Review_Queue*.csv'))+list(root.glob('**/*Cross_Code_Wording_Revision_Review*.csv'))
    reviews=[]
    for p in reviewps: reviews.extend(read_csv(p))
    def pairset(rows): return {(r.get('left_question_implementation_id',''),r.get('right_question_implementation_id','')) for r in rows if r.get('left_question_implementation_id')}
    aps=pairset(accepted); gps=pairset(guards); rps=pairset(reviews)
    checks.append({'check':'positive_negative_unresolved_pair_disjointness','status':'PASS' if not((epairs & gps) or (epairs & rps) or (gps & rps)) else 'FAIL','detail':json.dumps({'edge_guard_overlap':len(epairs&gps),'edge_review_overlap':len(epairs&rps),'guard_review_overlap':len(gps&rps)})})
    # current state metric crosscheck where easy
    stateps=list(root.glob('**/CURRENT_STATE.json')); state=json.load(stateps[0].open()) if stateps else {}
    flat=json.dumps(state,ensure_ascii=False)
    checks.append({'check':'pipeline_boundary_declared','status':'PASS' if re.search(r'"(?:j_family_authority_authored|family_authority_authored|substantive_family_authority_authored)"\s*:\s*(?:false|0)',flat) and re.search(r'"respondents_processed"\s*:\s*(?:false|0)',flat) and re.search(r'"(?:live_pipeline_modified|live_changes)"\s*:\s*(?:false|0)',flat) else 'FAIL','detail':'state flags inspected'})
    # validation all pass
    valres=list(root.glob('**/Validation_Results.csv'))
    if valres:
        vr=read_csv(valres[0]); bad=[r for r in vr if r.get('status')!='PASS']
        checks.append({'check':'validation_results_all_pass','status':'PASS' if not bad else 'FAIL','detail':f'{len(vr)-len(bad)}/{len(vr)} PASS'})
    valsum=list(root.glob('**/Validation_Summary.json'))
    if valsum:
        vs=json.load(valsum[0].open()); checks.append({'check':'validation_summary_pass','status':'PASS' if ('PASS' in str(vs.get('status','PASS')) and int(vs.get('tests_failed',0) or 0)==0 and not vs.get('failed_checks')) else 'FAIL','detail':json.dumps(vs,ensure_ascii=False)})
    # manifest for v2 packages
    if (root/'PACKAGE_INDEX.csv').exists(): checks += check_manifest(root)
    # wave coverage totals
    covp=list(root.glob('**/*Wave_Coverage*.csv'))
    if covp:
        cov=read_csv(covp[0])
        sums={k:sum(int(float(r.get(k,0) or 0)) for r in cov) for k in ['question_nodes','response_bound','response_gaps','source_structures'] if k in cov[0]}
        checks.append({'check':'wave_coverage_totals','status':'PASS' if sums.get('question_nodes',len(nodes))==len(nodes) and sums.get('response_gaps',len(gaps))==len(gaps) and sums.get('source_structures',len(inv))==len(inv) else 'FAIL','detail':json.dumps(sums)})
    # known correction assertions
    def vars_pair(rows,lw,lv,rw,rv):
        return [r for r in rows if r.get('left_wave')==lw and r.get('left_variable')==lv and r.get('right_wave')==rw and r.get('right_variable')==rv]
    if source=='Asian Barometer':
        checks.append({'check':'asian_false_slot_demoted','status':'PASS' if vars_pair(guards,'W4','q20','W5','q20') and not vars_pair(edges,'W4','q20','W5','q20') else 'FAIL','detail':'W4 q20 ↔ W5 q20'})
        checks.append({'check':'asian_target_expansion_unresolved','status':'PASS' if vars_pair(reviews,'W4','q98','W5','q105') and not vars_pair(edges,'W4','q98','W5','q105') else 'FAIL','detail':'W4 q98 ↔ W5 q105'})
    if source=='South Asia':
        acc=[('W1','c13c','W2','GB7f'),('W1','c13g','W2','GB7g'),('W1','c13e','W2','GB7k'),('W1','d1','W2','z1')]
        neg=[('W1','b8','W2','GBC5'),('W1','d7','W2','z8')]
        checks.append({'check':'south_asia_recovered_continuities','status':'PASS' if all(vars_pair(edges,*x) for x in acc) else 'FAIL','detail':str(acc)})
        checks.append({'check':'south_asia_false_matches_blocked','status':'PASS' if all(vars_pair(guards,*x) and not vars_pair(edges,*x) for x in neg) else 'FAIL','detail':str(neg)})
    if source=='LiTS':
        neg=[('III','q213','IV','q213'),('III','q401a','IV','q401a')]
        checks.append({'check':'lits_false_same_code_continuities_removed','status':'PASS' if all(vars_pair(guards,*x) and not vars_pair(edges,*x) for x in neg) else 'FAIL','detail':str(neg)})
        recp=list(root.glob('**/*Semantic_Role_Reconciliation_Rulings*.csv')); rec=read_csv(recp[0]) if recp else []
        checks.append({'check':'lits_semantic_role_reconciliations_present','status':'PASS' if len(rec)==6 else 'FAIL','detail':f'{len(rec)} rulings'})
    source_results[source]=checks
    source_summary.append({'source':source,'nodes':len(nodes),'bound':len(nodes)-len(gaps),'gaps':len(gaps),'edges':len(edges),'structures':len(inv),'memberships':len(mem),'accepted_wording':len(accepted),'guards':len(guards),'reviews':len(reviews),'checks_passed':sum(x['status']=='PASS' for x in checks),'checks_total':len(checks),'status':'PASS' if all(x['status']=='PASS' for x in checks) else 'FAIL'})

# Global checks
global_checks=[]
global_checks.append({'check':'all_nine_node_union_exact_phase0','status':'PASS' if all_node_ids==phase_all else 'FAIL','detail':json.dumps({'all_sources':len(all_node_ids),'phase0':len(phase_all),'source_only':len(all_node_ids-phase_all),'phase0_only':len(phase_all-all_node_ids)})})
for field in ['nodes','response_bound','response_gaps','accepted_continuity_edges','source_structures']:
    total=sum(int(r[field]) for r in closure.values())
    expected={'nodes':18276,'response_bound':16308,'response_gaps':1968,'accepted_continuity_edges':4759,'source_structures':2499}[field]
    global_checks.append({'check':f'all_nine_{field}_total','status':'PASS' if total==expected else 'FAIL','detail':f'{total} expected {expected}'})
# Final four package manifests / outer content
p2_checks=check_manifest(P2)
# nested zips integrity
for zp in sorted(P2.glob('03_SOURCE_PACKAGES/*.zip')):
    with zipfile.ZipFile(zp) as z:
        bad=z.testzip(); p2_checks.append({'check':f'zip_integrity:{zp.name}','status':'PASS' if bad is None else 'FAIL','detail':str(bad)})
# Copies between uploaded package and handoff section 30
vsec=V10/'30_P2_REMAINING_FOUR_CALIBRE_AUDIT'/'PACKAGE_CONTENTS'
for p in sorted(P2.rglob('*')):
    if p.is_file():
        rel=p.relative_to(P2); q=vsec/rel
        p2_checks.append({'check':f'handoff_section30_copy:{rel}','status':'PASS' if q.exists() and sha256_file(p)==sha256_file(q) else 'FAIL','detail':str(rel)})
# Handoff package manifest and all zips
handoff_checks=check_manifest(V10)
for zp in sorted(V10.rglob('*.zip')):
    try:
        with zipfile.ZipFile(zp) as z: bad=z.testzip()
        handoff_checks.append({'check':f'zip_integrity:{zp.relative_to(V10)}','status':'PASS' if bad is None else 'FAIL','detail':str(bad)})
    except Exception as e:
        handoff_checks.append({'check':f'zip_integrity:{zp.relative_to(V10)}','status':'FAIL','detail':repr(e)})
# semantic control consistency flags
cur=json.load((V10/'00_START_HERE/CURRENT_STATE.json').open())
text_files={p.name:p.read_text(encoding='utf-8',errors='replace') for p in [V10/'00_START_HERE'/'MASTER_HANDOFF.md',V10/'00_START_HERE'/'NEXT_CHAT_OPENING_INSTRUCTION.txt',V10/'00_START_HERE'/'EXACT_RESUME_POINT.md',V10/'00_START_HERE'/'README_FIRST.md']}
validation=json.load((V10/'VALIDATION.json').open())
scope=json.load((V10/'00_START_HERE'/'SCOPE_LOCK.json').open())
handoff_checks += [
 {'check':'current_state_all_nine_closed','status':'PASS' if len(cur.get('source_local_deep_passes_closed',[]))==9 and cur.get('next_pass')=='P2_GLOBAL_CROSS_SOURCE_RECONCILIATION' else 'FAIL','detail':json.dumps(cur,ensure_ascii=False)},
 {'check':'master_handoff_md_current','status':'PASS' if 'all nine' in text_files['MASTER_HANDOFF.md'].lower() and 'global cross-source reconciliation' in text_files['MASTER_HANDOFF.md'].lower() else 'FAIL','detail':text_files['MASTER_HANDOFF.md']},
 {'check':'next_chat_instruction_current_version','status':'PASS' if 'v10 master handoff' in text_files['NEXT_CHAT_OPENING_INSTRUCTION.txt'].lower() and 'v9' not in text_files['NEXT_CHAT_OPENING_INSTRUCTION.txt'].lower() else 'FAIL','detail':text_files['NEXT_CHAT_OPENING_INSTRUCTION.txt']},
 {'check':'top_level_validation_current','status':'PASS' if len(validation.get('source_local_deep_passes_closed',[]))==9 and validation.get('next_pass')=='P2_GLOBAL_CROSS_SOURCE_RECONCILIATION' else 'FAIL','detail':json.dumps(validation,ensure_ascii=False)},
 {'check':'scope_lock_current_pass_exact','status':'PASS' if scope.get('current_pass')==cur.get('current_pass') else 'FAIL','detail':f"scope={scope.get('current_pass')} state={cur.get('current_pass')}"},
]

# Seed refresh integrity
seed=read_csv(V10/'29_P2_ALL_NINE_CROSS_SOURCE_SEED_REFRESH'/'Rawlsing_P2_All_Nine_Source_Comparison_Proposition_Seed_Refresh_v1.csv')
psum=read_csv(V10/'29_P2_ALL_NINE_CROSS_SOURCE_SEED_REFRESH'/'Rawlsing_P2_All_Nine_Source_Pairwise_Seed_Summary_v1.csv')
seed_checks=[]
seedids=[r['candidate_id'] for r in seed]
seed_checks.append({'check':'seed_ids_unique','status':'PASS' if len(seedids)==len(set(seedids)) and '' not in set(seedids) else 'FAIL','detail':f'{len(seedids)} rows / {len(set(seedids))} unique'})
orph=[r for r in seed if r['left_question_implementation_id'] not in phase_all or r['right_question_implementation_id'] not in phase_all]
seed_checks.append({'check':'seed_endpoint_integrity','status':'PASS' if not orph else 'FAIL','detail':f'orphan rows={len(orph)}'})
counts=Counter((r['left_source'],r['right_source']) for r in seed)
bad=[]
for r in psum:
    if counts[(r['left_source'],r['right_source'])]!=int(r['seed_rows']): bad.append((r,counts[(r['left_source'],r['right_source'])]))
seed_checks.append({'check':'pairwise_seed_summary_reconciles','status':'PASS' if not bad else 'FAIL','detail':json.dumps(bad,ensure_ascii=False)})
seed_checks.append({'check':'all_36_source_pairs_present','status':'PASS' if len(psum)==36 else 'FAIL','detail':str(len(psum))})
seed_checks.append({'check':'seeds_non_authoritative','status':'PASS' if all(r['authority_status']=='PROVISIONAL_NON_AUTHORITY' for r in seed+psum) else 'FAIL','detail':'all rows inspected'})

result={'source_summary':source_summary,'source_checks':source_results,'global_checks':global_checks,'p2_package_checks':p2_checks,'handoff_checks':handoff_checks,'seed_checks':seed_checks}
(OUT/'independent_integrity_audit.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
# flat CSV
flat=[]
for area, checks in [('global',global_checks),('p2_package',p2_checks),('handoff',handoff_checks),('seed_refresh',seed_checks)]:
    for x in checks: flat.append({'area':area,**x})
for s,checks in source_results.items():
    for x in checks: flat.append({'area':s,**x})
with (OUT/'independent_integrity_audit.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['area','check','status','detail']); w.writeheader(); w.writerows(flat)
with (OUT/'source_summary.csv').open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(source_summary[0])); w.writeheader(); w.writerows(source_summary)
print(json.dumps({'source_summary':source_summary,'global':global_checks,'p2_failures':[x for x in p2_checks if x['status']!='PASS'],'handoff_failures':[x for x in handoff_checks if x['status']!='PASS'],'seed_failures':[x for x in seed_checks if x['status']!='PASS']},indent=2,ensure_ascii=False))
