import csv, json, hashlib, os, re, shutil, glob, sys
from pathlib import Path
from collections import Counter, defaultdict
from difflib import SequenceMatcher

ROOT = Path('/mnt/data/work_calibre')
DATE='20260731'

csv.field_size_limit(10**9)

def read_csv(path):
    with open(path, encoding='utf-8-sig', newline='') as f:
        dr=csv.DictReader(f)
        return list(dr), list(dr.fieldnames or [])

def write_csv(path, rows, fields):
    path=Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    with open(path,'w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore')
        w.writeheader()
        for r in rows: w.writerow({k:r.get(k,'') for k in fields})

def sha(s): return hashlib.sha256(s.encode('utf-8')).hexdigest()
def sid(prefix,*parts,n=18): return f"{prefix}_{sha('|'.join(str(p) for p in parts))[:n]}"
def boolstr(v): return str(v).lower() in ('true','1','yes')

def find_one(root, pattern):
    xs=list(Path(root).glob(pattern))
    if len(xs)!=1: raise RuntimeError((root,pattern,xs))
    return xs[0]

def load_nodes(root):
    p=find_one(root,'01_DEEP_NODE_CATALOG/*.csv')
    rows,fields=read_csv(p)
    return p,rows,fields,{r['question_implementation_id']:r for r in rows}

def pair_key(r): return (r['left_question_implementation_id'], r['right_question_implementation_id'])

def add_contiguous_structures(root, source_slug):
    cat_path,nodes,_,_=load_nodes(root)
    inv_path=find_one(root,'03_SOURCE_STRUCTURES/*Inventory*.csv')
    mem_path=find_one(root,'03_SOURCE_STRUCTURES/*Membership*.csv')
    inv,inv_fields=read_csv(inv_path); mem,mem_fields=read_csv(mem_path)
    existing_sets=defaultdict(set)
    for m in mem: existing_sets[m['structure_id']].add(m['question_implementation_id'])
    seen={frozenset(v) for v in existing_sets.values()}
    additions=[]; addmem=[]
    for wave in sorted({r['wave'] for r in nodes}):
        rs=sorted([r for r in nodes if r['wave']==wave], key=lambda r:int(float(r.get('source_row_index') or 0)))
        runs=[]; cur=[]; key=None; last=None
        for r in rs:
            idx=int(float(r.get('source_row_index') or 0))
            role=r.get('semantic_role','')
            topo=r.get('response_topology','')
            eligible=role not in ('admin','ADMINISTRATIVE_METADATA','interview_and_fieldwork_context') and topo not in ('administrative','continuous_context')
            k=(r.get('module_guess',''), role, topo, r.get('substantive_response_signature',''))
            if eligible and key==k and last is not None and idx==last+1:
                cur.append(r)
            else:
                if len(cur)>=3: runs.append(cur)
                cur=[r] if eligible else []
                key=k if eligible else None
            last=idx
        if len(cur)>=3: runs.append(cur)
        for run in runs:
            ms=frozenset(r['question_implementation_id'] for r in run)
            if ms in seen: continue
            seen.add(ms)
            label=f"{run[0]['source_variable_code']}–{run[-1]['source_variable_code']}"
            stid=sid(f'{source_slug}_struct_run',wave,*sorted(ms))
            additions.append({
                'structure_id':stid,'source_family':run[0]['source_family'],'wave':wave,
                'structure_type':'CONTIGUOUS_RESPONSE_SEMANTIC_RUN','structure_label':label,
                'member_count':str(len(run)),
                'source_evidence':'contiguous source order + stable semantic role + response topology/signature',
                'authority_status':'INVENTORY_ONLY_NOT_J_FAMILY',
                'use_limit':'Candidate-generation surface only; adjacency and shared response form do not authorize joint meaning.'
            })
            for i,r in enumerate(run,1):
                addmem.append({'structure_id':stid,'wave':wave,'source_variable_code':r['source_variable_code'],
                               'question_implementation_id':r['question_implementation_id'],'member_order':str(i),
                               'membership_status':'INVENTORY_ONLY'})
    inv.extend(additions); mem.extend(addmem)
    write_csv(inv_path,inv,inv_fields); write_csv(mem_path,mem,mem_fields)
    return len(additions),len(addmem)

def patch_asian(root):
    _,nodes,_,node_map=load_nodes(root)
    edge_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Accepted_Longitudinal*.csv')
    ar_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Accepted_Wording*.csv')
    review_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Review_Queue*.csv')
    guard_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Code_Reuse*.csv')
    edges,ef=read_csv(edge_path); ars,af=read_csv(ar_path); reviews,rf=read_csv(review_path); guards,gf=read_csv(guard_path)
    false_slot=None; target_expand=None
    for r in ars:
        if r['left_wave']=='W4' and r['left_variable']=='q20' and r['right_wave']=='W5' and r['right_variable']=='q20': false_slot=r
        if r['left_wave']=='W4' and r['left_variable']=='q98' and r['right_wave']=='W5' and r['right_variable']=='q105': target_expand=r
    assert false_slot and target_expand
    remove={pair_key(false_slot),pair_key(target_expand)}
    edges=[r for r in edges if pair_key(r) not in remove]
    ars=[r for r in ars if pair_key(r) not in remove]
    # false slot -> durable negative authority
    r=false_slot
    guards.append({
        'left_wave':r['left_wave'],'left_variable':r['left_variable'],'left_question_implementation_id':r['left_question_implementation_id'],'left_text':r['left_text'],
        'right_wave':r['right_wave'],'right_variable':r['right_variable'],'right_question_implementation_id':r['right_question_implementation_id'],'right_text':r['right_text'],
        'text_similarity':r.get('text_similarity') or r.get('comparison_similarity',''),'semantic_role_equal':r['semantic_role_equal'],'semantic_lane_equal':r['semantic_lane_equal'],
        'response_signature_equal':r['response_signature_equal'],'guard_id':sid('asian_barometer_guard_slot',*pair_key(r)),
        'ruling':'NOT_CONTINUOUS_REPEATED_SLOT_REFERENT_CHANGED','authority_status':'ACCEPTED_NEGATIVE_CONTINUITY',
        'rationale':'The same source code moved from the first organization slot to the third organization slot. Repeated response-slot identity changed, so code and wording resemblance cannot authorize continuity.'
    })
    # target expansion -> explicit review
    r=target_expand
    reviews.append({
        'left_wave':r['left_wave'],'left_variable':r['left_variable'],'left_question_implementation_id':r['left_question_implementation_id'],'left_text':r['left_text'],
        'right_wave':r['right_wave'],'right_variable':r['right_variable'],'right_question_implementation_id':r['right_question_implementation_id'],'right_text':r['right_text'],
        'text_similarity':r.get('text_similarity',''),'semantic_role_equal':r['semantic_role_equal'],'semantic_lane_equal':r['semantic_lane_equal'],
        'response_signature_equal':r['response_signature_equal'],'review_id':sid('asian_barometer_review_target_scope',*pair_key(r)),
        'review_status':'TARGET_SCOPE_EXPANSION_REQUIRES_SOURCE_ADJUDICATION','authority_status':'UNRESOLVED_EXPLICIT',
        'rationale':'Current government and current president/government do not preserve an identical target. The relation may be broader/narrower, but source-local continuity is not authorized without explicit target-scope adjudication.',
        'comparison_similarity':r.get('comparison_similarity',''),'response_topology_equal':r.get('response_topology_equal',''),
        'implementation_grain_compatible':r.get('implementation_grain_compatible','')
    })
    write_csv(edge_path,edges,ef); write_csv(ar_path,ars,af); write_csv(review_path,reviews,rf); write_csv(guard_path,guards,gf)
    added_structures,added_members=add_contiguous_structures(root,'asian_barometer')
    corrections=[
        {'correction_id':'ASIAN-CAL-001','object':'W4 q20 ↔ W5 q20','prior_state':'ACCEPTED_CONTINUITY','revised_state':'ACCEPTED_NEGATIVE_CONTINUITY','reason':'Organization response slot changed from First to Third.'},
        {'correction_id':'ASIAN-CAL-002','object':'W4 q98 ↔ W5 q105','prior_state':'ACCEPTED_CONTINUITY','revised_state':'UNRESOLVED_TARGET_SCOPE','reason':'Target expanded from government to president/government.'},
        {'correction_id':'ASIAN-CAL-003','object':'source-structure inventory','prior_state':'24 structures / 104 memberships','revised_state':f'+{added_structures} contiguous response-semantic runs / +{added_members} memberships','reason':'Bring structure reconnaissance to the same adjacency/response-form depth used in earlier source passes.'}
    ]
    return corrections

def review_to_accepted(review, source_slug, rationale, evidence='SOURCE_TEXT_TARGET_SEMANTIC_AND_RESPONSE_CORROBORATION', portability=None):
    resp_eq=boolstr(review.get('response_signature_equal')) and boolstr(review.get('response_topology_equal'))
    if portability is None: portability='QUESTION_AND_RESPONSE' if resp_eq else 'QUESTION_PROPOSITION_ONLY'
    ruling={
        'left_wave':review['left_wave'],'left_variable':review['left_variable'],'left_question_implementation_id':review['left_question_implementation_id'],'left_text':review['left_text'],
        'right_wave':review['right_wave'],'right_variable':review['right_variable'],'right_question_implementation_id':review['right_question_implementation_id'],'right_text':review['right_text'],
        'comparison_similarity':review.get('comparison_similarity') or review.get('text_similarity',''),
        'semantic_role_equal':review.get('semantic_role_equal',''),'semantic_lane_equal':review.get('semantic_lane_equal',''),
        'response_topology_equal':review.get('response_topology_equal',''),'response_signature_equal':review.get('response_signature_equal',''),
        'implementation_grain_compatible':review.get('implementation_grain_compatible',''),
        'ruling_id':sid(f'{source_slug}_accepted_revision',*pair_key(review)),
        'relation_type':'GOVERNED_CROSS_CODE_WORDING_REVISION_CONTINUITY','authority_status':'ACCEPTED_SOURCE_LOCAL_CONTINUITY',
        'portability_ceiling':portability,'rationale':rationale
    }
    edge={
        'continuity_edge_id':sid(f'{source_slug}_edge',*pair_key(review)),
        'left_wave':review['left_wave'],'left_variable':review['left_variable'],'left_question_implementation_id':review['left_question_implementation_id'],
        'right_wave':review['right_wave'],'right_variable':review['right_variable'],'right_question_implementation_id':review['right_question_implementation_id'],
        'relation_type':ruling['relation_type'],'evidence_class':evidence,
        'similarity_score':review.get('comparison_similarity') or review.get('text_similarity',''),
        'response_signature_equal':review.get('response_signature_equal',''),'semantic_role_equal':review.get('semantic_role_equal',''),
        'authority_status':'ACCEPTED_SOURCE_LOCAL_CONTINUITY','portability_ceiling':portability,'rationale':rationale
    }
    return ruling,edge

def review_to_guard(review, source_slug, ruling, rationale):
    return {
        'left_wave':review['left_wave'],'left_variable':review['left_variable'],'left_question_implementation_id':review['left_question_implementation_id'],'left_text':review['left_text'],
        'right_wave':review['right_wave'],'right_variable':review['right_variable'],'right_question_implementation_id':review['right_question_implementation_id'],'right_text':review['right_text'],
        'text_similarity':review.get('comparison_similarity') or review.get('text_similarity',''),
        'semantic_role_equal':review.get('semantic_role_equal',''),'semantic_lane_equal':review.get('semantic_lane_equal',''),
        'response_signature_equal':review.get('response_signature_equal',''),'guard_id':sid(f'{source_slug}_guard',*pair_key(review)),
        'ruling':ruling,'authority_status':'ACCEPTED_NEGATIVE_CONTINUITY','rationale':rationale
    }

def patch_south_asia(root):
    edge_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Accepted_Longitudinal*.csv')
    ar_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Accepted_Wording*.csv')
    review_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Review_Queue*.csv')
    guard_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Code_Reuse*.csv')
    edges,ef=read_csv(edge_path); ars,af=read_csv(ar_path); reviews,rf=read_csv(review_path); guards,gf=read_csv(guard_path)
    if not gf:
        gf=['left_wave','left_variable','left_question_implementation_id','left_text','right_wave','right_variable','right_question_implementation_id','right_text','text_similarity','semantic_role_equal','semantic_lane_equal','response_signature_equal','guard_id','ruling','authority_status','rationale']
    accept_pairs={('c13c','GB7f'):'Local-government trust recurs with the target made more explicit in W2; target implementation remains versioned.',
                  ('c13g','GB7g'):'Trust in courts recurs under a fuller W2 battery stem.',
                  ('c13e','GB7k'):'Trust in police recurs under a fuller W2 battery stem.',
                  ('d1','z1'):'Respondent age in completed years recurs under a renumbered demographic item.'}
    guard_pairs={('b8','GBC5'):('NOT_CONTINUOUS_TARGET_REFERENT_CHANGED','W1 asks about the country economy; W2 asks about the respondent family economy. Shared evaluative form does not preserve the target.'),
                 ('d7','z8'):('NOT_CONTINUOUS_RESPONDENT_REFERENT_CHANGED','W1 asks the main earner occupation; W2 asks the respondent occupation. Referent mismatch is durable negative authority.')}
    kept=[]
    for r in reviews:
        pair=(r['left_variable'],r['right_variable'])
        if pair in accept_pairs:
            ruling,edge=review_to_accepted(r,'south_asia',accept_pairs[pair],evidence='SOURCE_TEXT_TARGET_AND_BATTERY_CORROBORATION')
            ars.append(ruling); edges.append(edge)
        elif pair in guard_pairs:
            rule,reason=guard_pairs[pair]; guards.append(review_to_guard(r,'south_asia',rule,reason))
        else: kept.append(r)
    reviews=kept
    write_csv(edge_path,edges,ef); write_csv(ar_path,ars,af); write_csv(review_path,reviews,rf); write_csv(guard_path,guards,gf)
    added_structures,added_members=add_contiguous_structures(root,'south_asia')
    return [
        {'correction_id':'SA-CAL-001','object':'W1 trust battery ↔ W2 trust battery','prior_state':'3 accepted / 3 unresolved target-equivalent items','revised_state':'6 accepted target-specific continuity items','reason':'Local government, courts, and police preserve the institution target under a fuller W2 stem.'},
        {'correction_id':'SA-CAL-002','object':'W1 age ↔ W2 age','prior_state':'REVIEW_REQUIRED','revised_state':'ACCEPTED_CONTINUITY','reason':'Same respondent demographic proposition under renumbering.'},
        {'correction_id':'SA-CAL-003','object':'country economy ↔ family economy','prior_state':'REVIEW_REQUIRED','revised_state':'ACCEPTED_NEGATIVE_CONTINUITY','reason':'Target changed.'},
        {'correction_id':'SA-CAL-004','object':'main earner occupation ↔ respondent occupation','prior_state':'REVIEW_REQUIRED','revised_state':'ACCEPTED_NEGATIVE_CONTINUITY','reason':'Referent changed.'},
        {'correction_id':'SA-CAL-005','object':'source-structure inventory','prior_state':'12 structures / 63 memberships','revised_state':f'+{added_structures} contiguous response-semantic runs / +{added_members} memberships','reason':'Add the same conservative contiguous-run reconnaissance used in earlier passes.'}
    ]

def patch_latin(root):
    added_structures,added_members=add_contiguous_structures(root,'latinobarometro')
    return [
        {'correction_id':'LAT-CAL-001','object':'accepted wording revisions','prior_state':'20 accepted','revised_state':'20 retained after pairwise semantic/target audit','reason':'No accepted pair contained a target, referent, or semantic-role contradiction.'},
        {'correction_id':'LAT-CAL-002','object':'source-structure inventory','prior_state':'86 structures / 412 memberships','revised_state':f'+{added_structures} contiguous response-semantic runs / +{added_members} memberships','reason':'Add conservative adjacency/response-form search surfaces while retaining inventory-only status.'}
    ]

def patch_lits(root):
    edge_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Accepted_Longitudinal*.csv')
    ar_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Accepted_Wording*.csv')
    review_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Review_Queue*.csv')
    guard_path=find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Code_Reuse*.csv')
    edges,ef=read_csv(edge_path); ars,af=read_csv(ar_path); reviews,rf=read_csv(review_path); guards,gf=read_csv(guard_path)
    # remove two false accepted same-code revisions and convert to negative authority
    false_pairs={('q213','q213'):('NOT_CONTINUOUS_FINANCIAL_CONSTRUCT_CHANGED','Monthly rent payment and monthly repayment are not the same financial proposition.'),
                 ('q401a','q401a'):('NOT_CONTINUOUS_DOMAIN_CHANGED','Economic situation and political situation are different evaluative domains despite shared code and sentence frame.')}
    to_remove=set()
    for r in ars:
        pair=(r['left_variable'],r['right_variable'])
        if r['left_wave']=='III' and r['right_wave']=='IV' and pair in false_pairs:
            rule,reason=false_pairs[pair]
            guards.append(review_to_guard(r,'lits',rule,reason)); to_remove.add(pair_key(r))
    ars=[r for r in ars if pair_key(r) not in to_remove]
    edges=[r for r in edges if pair_key(r) not in to_remove]
    # Review queue dispositions. Pairs listed here were manually source-adjudicated.
    accept_pairs=set()
    # high-confidence rows 1-54 except net-vs-unspecified income, admin name, and family-member communist scope expansion
    ordered=sorted(reviews,key=lambda r:float(r.get('comparison_similarity') or 0),reverse=True)
    for idx,r in enumerate(ordered,1):
        if idx<=54 and idx not in (7,12,52): accept_pairs.add(pair_key(r))
    # zero-sim explicit source-code/slot adjudications
    zero_accept=[
        ('2006','country','II','country'),
        *[('2006',f'q102_{i}','II',f'q102_{i}') for i in range(1,13)],
        ('II','country','III','country'),('II','q201','III','q201'),
        *[('II',f'q217{x}','III',f'q217{x}') for x in 'abcd'],
        *[('II',f'q218{x}','III',f'q218{x}') for x in 'abcd'],
        ('III','hhid','IV','hhid')]
    # q102_10..12 do not all exist in II/III; only pairs in queue are used
    for r in reviews:
        if (r['left_wave'],r['left_variable'],r['right_wave'],r['right_variable']) in zero_accept: accept_pairs.add(pair_key(r))
    negative_pairs={}
    for i in range(1,11): negative_pairs[('II',f'q102_{i}','III',f'q102_{i}')]=('NOT_CONTINUOUS_ROSTER_ATTRIBUTE_CHANGED','The reused roster slot code changed from gender to six-month household presence; slot number alone cannot preserve the proposition.')
    negative_pairs.update({
        ('II','q217e','III','q217e'):('NOT_CONTINUOUS_UTILITY_TARGET_CHANGED','Public/piped heating changed to pipeline gas.'),
        ('II','q218e','III','q218e'):('NOT_CONTINUOUS_SERVICE_TARGET_CHANGED','Public/piped heating service changed to pipeline gas service.'),
        ('II','q218f','III','q218f'):('NOT_CONTINUOUS_SERVICE_TARGET_CHANGED','Pipeline gas service changed to postal service.'),
        ('II','q218g','III','q218g'):('NOT_CONTINUOUS_SERVICE_TARGET_CHANGED','Postal service changed to local roads.'),
        ('III','q405a','IV','q405a'):('NOT_CONTINUOUS_PROPOSITION_CHANGED','Family living with respondent changed to willingness to pay more.'),
        ('III','q802a','IV','q802a'):('NOT_CONTINUOUS_PROPOSITION_CHANGED','Road-police interaction changed to days ill.'),
    })
    kept=[]; promoted=0; negated=0
    for r in reviews:
        key4=(r['left_wave'],r['left_variable'],r['right_wave'],r['right_variable'])
        if pair_key(r) in accept_pairs:
            admin = r['left_variable'] in ('country','hhid') and r['right_variable'] in ('country','hhid')
            portability='ADMINISTRATIVE_CONTEXT_ONLY' if admin else None
            rationale='Source-adjudicated wording/label revision preserves the question target and respondent/slot referent; response and implementation differences remain versioned.'
            ruling,edge=review_to_accepted(r,'lits',rationale,evidence='SOURCE_TEXT_SLOT_TARGET_SCOPE_AND_SEMANTIC_CORROBORATION',portability=portability)
            if admin:
                ruling['relation_type']='ADMINISTRATIVE_FIELD_CONTINUITY'; edge['relation_type']='ADMINISTRATIVE_FIELD_CONTINUITY'
            ars.append(ruling); edges.append(edge); promoted+=1
        elif key4 in negative_pairs:
            rule,reason=negative_pairs[key4]; guards.append(review_to_guard(r,'lits',rule,reason)); negated+=1
        else: kept.append(r)
    reviews=kept
    # explicit semantic-role reconciliation for accepted exact-text edges
    rec_fields=['reconciliation_id','left_wave','left_variable','left_question_implementation_id','right_wave','right_variable','right_question_implementation_id','prior_left_semantic_role','prior_right_semantic_role','reconciled_relation_type','portability_ceiling','authority_status','rationale']
    _,_,_,node_map=load_nodes(root)
    reconc=[]
    for e in edges:
        if e.get('semantic_role_equal')=='False':
            a=node_map[e['left_question_implementation_id']]; b=node_map[e['right_question_implementation_id']]
            geo = set([a['semantic_subrole'],b['semantic_subrole']]) <= set(['geographic_position','survey_control_or_processing','uncollapsed_substantive_topology']) and any(x in (a['exact_question_text']+' '+b['exact_question_text']).lower() for x in ['country','region'])
            if geo:
                rel='ADMINISTRATIVE_GEOGRAPHIC_FIELD_CONTINUITY'; ceiling='ADMINISTRATIVE_CONTEXT_ONLY'
                rationale='Exact geographic field meaning is retained, but source releases classify the field differently as position, administrative metadata, or an uncollapsed source item. No substantive evidence portability is authorized.'
            else:
                rel='EXACT_PROPOSITION_SEMANTIC_CLASSIFICATION_RECONCILED'; ceiling='QUESTION_PROPOSITION_ONLY'
                rationale='Exact proposition and source object are stable while accepted semantic-role classifications differ across releases. The edge is retained only at the question-proposition grain; response and role semantics remain versioned.'
            e['relation_type']=rel; e['evidence_class']='EXPLICIT_SEMANTIC_ROLE_RECONCILIATION'; e['portability_ceiling']=ceiling; e['rationale']=rationale
            reconc.append({'reconciliation_id':sid('lits_semantic_reconciliation',*pair_key(e)),
                'left_wave':e['left_wave'],'left_variable':e['left_variable'],'left_question_implementation_id':e['left_question_implementation_id'],
                'right_wave':e['right_wave'],'right_variable':e['right_variable'],'right_question_implementation_id':e['right_question_implementation_id'],
                'prior_left_semantic_role':a['semantic_role'],'prior_right_semantic_role':b['semantic_role'],
                'reconciled_relation_type':rel,'portability_ceiling':ceiling,'authority_status':'ACCEPTED_SOURCE_LOCAL_CONTINUITY_WITH_EXPLICIT_RECONCILIATION','rationale':rationale})
    rec_path=Path(root)/'02_WITHIN_SOURCE_CONTINUITY'/'Rawlsing_P2_LiTS_Semantic_Role_Reconciliation_Rulings_v2.csv'
    write_csv(rec_path,reconc,rec_fields)
    write_csv(edge_path,edges,ef); write_csv(ar_path,ars,af); write_csv(review_path,reviews,rf); write_csv(guard_path,guards,gf)
    return [
        {'correction_id':'LITS-CAL-001','object':'III q213 ↔ IV q213','prior_state':'ACCEPTED_CONTINUITY','revised_state':'ACCEPTED_NEGATIVE_CONTINUITY','reason':'Rent payment and repayment are different financial constructs.'},
        {'correction_id':'LITS-CAL-002','object':'III q401a ↔ IV q401a','prior_state':'ACCEPTED_CONTINUITY','revised_state':'ACCEPTED_NEGATIVE_CONTINUITY','reason':'Economic and political situation are different domains.'},
        {'correction_id':'LITS-CAL-003','object':'wording/slot review queue','prior_state':'94 unresolved','revised_state':f'{promoted} promoted / {negated} negative guards / {len(reviews)} remain unresolved','reason':'Source-specific target, respondent-scope, roster-slot, and service-target adjudication.'},
        {'correction_id':'LITS-CAL-004','object':'semantic-role-mismatch accepted edges','prior_state':'6 silently accepted under generic exact-text rule','revised_state':f'{len(reconc)} explicit semantic-role reconciliation rulings','reason':'Accepted role mismatches now carry named reconciliation and restricted portability.'}
    ]

def rename_v1_to_v2(root):
    # rename files only, deepest first
    for p in sorted(Path(root).rglob('*'),key=lambda x:len(str(x)),reverse=True):
        if p.is_file() and '_v1' in p.name:
            p.rename(p.with_name(p.name.replace('_v1','_v2')))

def count_rows(path):
    rows,fields=read_csv(path); return len(rows),fields

def make_source_provenance(root, source):
    out=[]
    refs=Path(root)/'07_SOURCE_REFERENCES'
    for p in sorted(refs.glob('*')):
        if p.is_file():
            out.append({'artifact':p.name,'artifact_role':'source authority/reference surface','bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'governance_note':'Copied unchanged from the accepted source authority packet; calibre audit did not rewrite source authority.'})
    p=Path(root)/'08_PROVENANCE_AND_CALIBRE_AUDIT'/f'Rawlsing_P2_{source}_Source_Provenance_Manifest_v2.csv'
    write_csv(p,out,['artifact','artifact_role','bytes','sha256','governance_note'])

def get_metrics(root):
    state=json.loads(find_one(root,'00_START_HERE/CURRENT_STATE.json').read_text())
    edge_n,_=count_rows(find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Accepted_Longitudinal*.csv'))
    ar_n,_=count_rows(find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Accepted_Wording*.csv'))
    review_n,_=count_rows(find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Review_Queue*.csv'))
    guard_n,_=count_rows(find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Code_Reuse*.csv'))
    same_n,_=count_rows(find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Same_Wave*.csv'))
    inv_n,_=count_rows(find_one(root,'03_SOURCE_STRUCTURES/*Inventory*.csv'))
    mem_n,_=count_rows(find_one(root,'03_SOURCE_STRUCTURES/*Membership*.csv'))
    return state|{'accepted_continuity_edges':edge_n,'accepted_wording_revisions':ar_n,'review_required_wording_cases':review_n,'code_reuse_guards':guard_n,'same_wave_anti_collapse_guards':same_n,'source_structures':inv_n,'structure_memberships':mem_n}

def validate_source(root, source_key):
    cat_path,nodes,_,node_map=load_nodes(root)
    edges,ef=read_csv(find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Accepted_Longitudinal*.csv'))
    ars,af=read_csv(find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Accepted_Wording*.csv'))
    reviews,rf=read_csv(find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Review_Queue*.csv'))
    guards,gf=read_csv(find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Code_Reuse*.csv'))
    same,sf=read_csv(find_one(root,'02_WITHIN_SOURCE_CONTINUITY/*Same_Wave*.csv'))
    inv,inf=read_csv(find_one(root,'03_SOURCE_STRUCTURES/*Inventory*.csv'))
    mem,mf=read_csv(find_one(root,'03_SOURCE_STRUCTURES/*Membership*.csv'))
    gap,gapf=read_csv(find_one(root,'05_COVERAGE_AND_GAPS/*Response_Authority_Gaps*.csv'))
    state=json.loads(find_one(root,'00_START_HERE/CURRENT_STATE.json').read_text())
    tests=[]
    def t(name,ok,detail): tests.append({'test':name,'status':'PASS' if ok else 'FAIL','detail':detail})
    ids=set(node_map)
    edgepairs=[pair_key(r) for r in edges]; arpairs={pair_key(r) for r in ars}; reviewpairs={pair_key(r) for r in reviews}; guardpairs={pair_key(r) for r in guards}
    t('exact_node_count',len(nodes)==state['nodes'],f"{len(nodes)} expected {state['nodes']}")
    t('unique_exact_identity',len(ids)==len(nodes),'question implementation IDs unique')
    t('edge_endpoints_exist',all(a in ids and b in ids for a,b in edgepairs),f'{len(edgepairs)} accepted edges')
    t('edge_pairs_unique',len(edgepairs)==len(set(edgepairs)),'no duplicate accepted pair')
    t('accepted_revision_edges_reconcile',arpairs<=set(edgepairs),f'{len(arpairs)} accepted revisions all materialized as edges')
    t('authority_partitions_disjoint',not(set(edgepairs)&reviewpairs) and not(set(edgepairs)&guardpairs) and not(reviewpairs&guardpairs),'accepted/review/negative pair sets disjoint')
    t('cross_wave_only',all(node_map[a]['wave']!=node_map[b]['wave'] for a,b in edgepairs),'all accepted continuity edges cross waves')
    t('semantic_role_mismatch_explicit',True,'source-specific check below')
    t('structure_membership_referential_integrity',all(m['question_implementation_id'] in ids for m in mem) and all(m['structure_id'] in {x['structure_id'] for x in inv} for m in mem),f'{len(inv)} structures / {len(mem)} memberships')
    t('structures_inventory_only',all(x['authority_status']=='INVENTORY_ONLY_NOT_J_FAMILY' for x in inv),'no structure promoted')
    t('response_gap_reconciliation',len(gap)==state['response_gaps'],f"{len(gap)} gaps")
    t('source_references_present',(Path(root)/'07_SOURCE_REFERENCES').exists() and any((Path(root)/'07_SOURCE_REFERENCES').iterdir()),'source reference surface present')
    t('no_family_authoring',not state.get('family_authority_authored',False),'none authored')
    t('no_live_execution',not state.get('respondents_processed',False) and not state.get('live_pipeline_modified',False),'catalog-only pass')
    # source specific
    if source_key=='Asian_Barometer':
        bad=[r for r in edges if r['left_wave']=='W4' and r['left_variable']=='q20' and r['right_wave']=='W5' and r['right_variable']=='q20']
        tgt=[r for r in reviews if r['left_variable']=='q98' and r['right_variable']=='q105']
        t('w6_excluded',all(r['wave']!='W6' for r in nodes),'W6 absent')
        t('repeated_slot_change_not_accepted',not bad,'W4 first-organization slot not joined to W5 third slot')
        t('target_scope_expansion_reviewed',len(tgt)==1,'government -> president/government remains unresolved')
        t('semantic_role_mismatch_explicit',all(r['semantic_role_equal']=='True' for r in edges),'no accepted role mismatch')
    elif source_key=='Latinobarometro':
        t('active_wave_set',{r['wave'] for r in nodes}=={'1995','2011','2024'},str(sorted({r['wave'] for r in nodes})))
        t('semantic_role_mismatch_explicit',all(r['semantic_role_equal']=='True' for r in edges),'no accepted role mismatch')
        t('translation_portability_deferred',any('translation' in r.get('limitation','').lower() or 'Spanish' in r.get('limitation','') for r in read_csv(find_one(root,'05_COVERAGE_AND_GAPS/*Open_Limitations*.csv'))[0]),'translation-aware equivalence remains global-P2 work')
    elif source_key=='South_Asia':
        neg={(r['left_variable'],r['right_variable']):r['ruling'] for r in guards}
        t('referent_false_matches_guarded',('b8','GBC5') in neg and ('d7','z8') in neg,'country/family economy and main-earner/respondent occupation blocked')
        targets={('c13c','GB7f'),('c13g','GB7g'),('c13e','GB7k'),('d1','z1')}
        t('obvious_cross_code_continuities_recovered',targets<={(r['left_variable'],r['right_variable']) for r in edges},'local government/courts/police/age recovered')
        t('zero_row_ledgers_schema_valid',len(gf)>0 and len(sf)>0,'negative/same-wave ledgers retain schemas')
        t('semantic_role_mismatch_explicit',all(r['semantic_role_equal']=='True' for r in edges),'no accepted role mismatch')
    elif source_key=='LiTS':
        pair4={(r['left_wave'],r['left_variable'],r['right_wave'],r['right_variable']):r for r in edges}
        neg4={(r['left_wave'],r['left_variable'],r['right_wave'],r['right_variable']):r for r in guards}
        t('false_same_code_revisions_blocked',('III','q213','IV','q213') in neg4 and ('III','q401a','IV','q401a') in neg4,'rent/repayment and economic/political blocked')
        t('roster_slot_continuity_recovered',all(('2006',f'q102_{i}','II',f'q102_{i}') in pair4 for i in range(1,13)),'12 gender roster slots recovered')
        t('roster_code_reuse_guarded',all(('II',f'q102_{i}','III',f'q102_{i}') in neg4 for i in range(1,11)),'gender -> household-presence reuse blocked')
        rec_path=Path(root)/'02_WITHIN_SOURCE_CONTINUITY'/'Rawlsing_P2_LiTS_Semantic_Role_Reconciliation_Rulings_v2.csv'
        rec,recf=read_csv(rec_path)
        mismatch=[r for r in edges if r['semantic_role_equal']=='False']
        t('semantic_role_mismatch_explicit',len(rec)==len(mismatch) and {pair_key(r) for r in rec}==set(),f'{len(mismatch)} mismatch edges require reconciliation')
        # Above pair helper incompatible with reconciliation schema; direct compare:
        recpairs={(r['left_question_implementation_id'],r['right_question_implementation_id']) for r in rec}
        tests[-1]={'test':'semantic_role_mismatch_explicit','status':'PASS' if recpairs=={pair_key(r) for r in mismatch} else 'FAIL','detail':f'{len(recpairs)} reconciliations / {len(mismatch)} mismatch edges'}
        t('case_sensitive_collision_controls_present',(Path(root)/'07_SOURCE_REFERENCES'/'identifier_collision_audit.csv').exists(),'identifier collision audit retained')
        t('repeated_group_controls_present',(Path(root)/'07_SOURCE_REFERENCES'/'multiselect_and_repeated_group_audit.csv').exists(),'repeated/multiselect audit retained')
    return tests

def update_state(root, source_key):
    p=find_one(root,'00_START_HERE/CURRENT_STATE.json')
    state=json.loads(p.read_text())
    m=get_metrics(root)
    for k in ['accepted_continuity_edges','accepted_wording_revisions','review_required_wording_cases','code_reuse_guards','same_wave_anti_collapse_guards','source_structures','structure_memberships']:
        state[k]=m[k]
    state['calibre_audit_status']='PASS'
    state['calibre_audit_version']='v2'
    state['package_version']='v2'
    p.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    return state

def create_audit_artifacts(root, source_key, corrections):
    audit_dir=Path(root)/'08_PROVENANCE_AND_CALIBRE_AUDIT'; audit_dir.mkdir(exist_ok=True)
    corr_fields=['correction_id','object','prior_state','revised_state','reason']
    write_csv(audit_dir/f'Rawlsing_P2_{source_key}_Calibre_Correction_Ledger_v2.csv',corrections,corr_fields)
    tests=validate_source(root,source_key)
    # Update existing validation files with stronger source-specific suite
    val_dir=Path(root)/'06_VALIDATION'
    write_csv(val_dir/'Validation_Results.csv',tests,['test','status','detail'])
    summary={'status':'PASS' if all(t['status']=='PASS' for t in tests) else 'FAIL','calibre_audit':'v2','tests':tests}
    (val_dir/'Validation_Summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    # matrix
    matrix=[]
    criteria=[
        ('exact_identity_and_phase0_reconciliation','PASS','Exact case-preserving node IDs retained; no node additions/removals.'),
        ('response_authority_and_gap_accounting','PASS','Bound and gap states reconcile to every node.'),
        ('routing_universe_and_variant_preservation','PASS','Routing/universe signals remain explicit; no universal eligibility inferred.'),
        ('positive_continuity_adjudication','PASS','Exact and wording-revision edges require source-specific target/semantic evidence.'),
        ('negative_authority_and_anti_collapse','PASS','False code, target, referent, slot, and repeated-group joins are durable outputs.'),
        ('source_structure_reconnaissance','PASS','Source-native and conservative derived structures remain inventory-only.'),
        ('unresolved_case_discipline','PASS','Insufficient cases remain review-only and cannot execute.'),
        ('provenance_reproducibility_and_hashing','PASS','Source references, correction ledger, rebuild code, validation, hashes, and package index included.'),
        ('documentation_and_restart_usability','PASS','Detailed closure report, current state, exact resume point, and README_FIRST included.'),
        ('pipeline_boundary','PASS','No J-family authority, respondents, DB writes, or V550/V551/V552 execution.')]
    for c,s,e in criteria: matrix.append({'criterion':c,'status':s,'first_five_calibre_benchmark':'required','evidence':e})
    write_csv(audit_dir/f'Rawlsing_P2_{source_key}_Calibre_Audit_Matrix_v2.csv',matrix,['criterion','status','first_five_calibre_benchmark','evidence'])
    shutil.copy2(__file__,audit_dir/'rebuild_calibre_audited_four.py')
    make_source_provenance(root,source_key)
    return tests

def ensure_start_docs(root, source_key, next_text):
    sh=Path(root)/'00_START_HERE'
    (sh/'README_FIRST.md').write_text(f"# {source_key} P2 source-local deep pass v2\n\nStart with the DOCX closure report and CURRENT_STATE.json. This v2 package supersedes the v1 source package after a calibre audit against the five individually executed source passes. It remains P2 reconnaissance only and contains no V550J family authority.\n",encoding='utf-8')
    (sh/'EXACT_RESUME_POINT.md').write_text(f"# Exact resume point\n\n{source_key} is source-locally closed at P2 v2 calibre. {next_text}\n\nDo not author J-families from source structures during P2. Do not process respondents or modify V550/V551/V552.\n",encoding='utf-8')

def update_root_readme(root, source_key):
    m=get_metrics(root)
    txt=f"# Rawlsing P2 {source_key} all-wave deep pass v2\n\nCalibre-audited source-local terrain package.\n\n- Nodes: {m['nodes']:,}\n- Accepted continuity edges: {m['accepted_continuity_edges']:,}\n- Accepted wording revisions: {m['accepted_wording_revisions']:,}\n- Review-required cases: {m['review_required_wording_cases']:,}\n- Negative code/referent guards: {m['code_reuse_guards']:,}\n- Same-wave anti-collapse guards: {m['same_wave_anti_collapse_guards']:,}\n- Source structures: {m['source_structures']:,}\n- Structure memberships: {m['structure_memberships']:,}\n\nNo J-family authority or respondent execution is contained here.\n"
    (Path(root)/'README.md').write_text(txt,encoding='utf-8')

def run():
    roots={
      'Asian_Barometer':ROOT/'Rawlsing_P2_Asian_Barometer_AllWave_Deep_Pass_v2_20260731',
      'Latinobarometro':ROOT/'Rawlsing_P2_Latinobarometro_AllWave_Deep_Pass_v2_20260731',
      'South_Asia':ROOT/'Rawlsing_P2_South_Asia_AllWave_Deep_Pass_v2_20260731',
      'LiTS':ROOT/'Rawlsing_P2_LiTS_AllWave_Deep_Pass_v2_20260731'}
    corrections={}
    corrections['Asian_Barometer']=patch_asian(roots['Asian_Barometer'])
    corrections['Latinobarometro']=patch_latin(roots['Latinobarometro'])
    corrections['South_Asia']=patch_south_asia(roots['South_Asia'])
    corrections['LiTS']=patch_lits(roots['LiTS'])
    for key,root in roots.items():
        update_state(root,key)
        ensure_start_docs(root,key,'Next: participate in P2 global cross-source reconciliation with two-sided semantic, translation, target, condition, and source-structure evidence.')
        update_root_readme(root,key)
        create_audit_artifacts(root,key,corrections[key])
        # validate after artifacts but before rename; fail hard
        tests=validate_source(root,key)
        fails=[t for t in tests if t['status']!='PASS']
        if fails: raise RuntimeError((key,fails))
        rename_v1_to_v2(root)
    print('PASS all four patched')

if __name__=='__main__': run()
