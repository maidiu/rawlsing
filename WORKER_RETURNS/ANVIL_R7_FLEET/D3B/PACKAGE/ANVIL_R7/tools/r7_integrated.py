#!/usr/bin/env python3
"""Active ANVIL R7 integral investigation and decision gates.

A/B *duel* is OPTIONAL, and then only for a named question with shared evidence.
The obsolete full-architecture A/B comparator remains a read-only historical
specialist, not the active selection authority. All positives are LOCAL and do
not authenticate source rights, independent reviews, runner results, or HQ.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, sys
from anvil import REQUIRED
from r7_inventory import check_inventory

SCHEMA='ANVIL_R7_INTEGRATED'
HEX40=re.compile(r'^[a-f0-9]{40}$')
HEX64=re.compile(r'^[a-f0-9]{64}$')
DOMAINS=('SOURCE_SEMANTICS','C11_PERSISTENCE','CURRENT_I03_I05',
         'HISTORICAL_DDM_FUNCTIONS','F1_F4_ANALYTICS','FIELD_FORGE',
         'SEAM_WORLD_ACTOR','AUTHORITY_AND_RECOVERY','RESOURCE_ECONOMICS')
BINDS={'PRESENT_HARD','FUTURE_NONPRECLUSION','EXTERNAL_OWNER_HELD'}
DISPOS={'PRESENT_PRESERVED','FUTURE_NONPRECLUDED','EXACT_OWNER_HOLD','BLOCKING_LOSS','REFUSED_AUTHORITY'}
IDENTITY_STATES={'PRESENT_PRESERVED','FUTURE_NONPRECLUDED','EXACT_OWNER_HOLD','BLOCKING_LOSS','REFUSED_AUTHORITY','RETAINED_HISTORICAL_NONADOPTED'}
GRAPH_TIME={'OBSERVED','HISTORICAL_AS_OF','MODELED','FICTIONAL','MIXED_TYPED'}
BOUND_IDS=('T1','T2','T3','T4','T5','T6','T7')
GRADES={'CODE_STATIC','DOCUMENTARY','EXECUTED_SOURCEFREE','EXECUTED_NATIVE','UNVERIFIED_HELD'}
INVALID=('todo','tbd','placeholder','to be determined','see above','n/a','not applicable')

def good(x,n=24):
    return isinstance(x,str) and len(x.strip())>=n and not any(x.strip().lower()==s for s in INVALID)

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def sha(x):return hashlib.sha256(x).hexdigest()

def load(root,ptr,errors,code):
    if not isinstance(ptr,dict):errors.append(code+':NO_POINTER');return None
    rel=ptr.get('path');expected=ptr.get('sha256')
    if not isinstance(rel,str) or not rel or rel.startswith('/') or '\\' in rel or '..' in pathlib.PurePosixPath(rel).parts or not isinstance(expected,str) or not HEX64.fullmatch(expected):
        errors.append(code+':INVALID_LOCATOR');return None
    base=pathlib.Path(root).resolve() if root else None
    if base is None:errors.append(code+':NO_ROOT');return None
    path=(base/rel).resolve()
    if not path.is_relative_to(base) or not path.is_file() or path.is_symlink():errors.append(code+':UNSAFE_OR_ABSENT');return None
    data=path.read_bytes()
    if sha(data)!=expected:errors.append(code+':BYTES_CHANGED');return None
    try:return json.loads(data)
    except (UnicodeDecodeError,ValueError):errors.append(code+':MALFORMED_JSON');return None

def source_ref(item,root,errors,code):
    """Content pin and exact quote, NOT epistemic or owner authentication."""
    if not isinstance(item,dict):errors.append(code+':NO_SOURCE');return
    rel=item.get('path');wanted=item.get('sha256');quote=item.get('exact_excerpt')
    if (not isinstance(rel,str) or not rel or rel.startswith('/') or '\\' in rel or '..' in pathlib.PurePosixPath(rel).parts
        or not isinstance(wanted,str) or not HEX64.fullmatch(wanted) or not good(quote,20)):
        errors.append(code+':INVALID_SOURCE_PIN');return
    if root is None:errors.append(code+':NO_SOURCE_ROOT');return
    base=pathlib.Path(root).resolve();p=(base/rel).resolve()
    if not p.is_relative_to(base) or not p.is_file() or p.is_symlink():errors.append(code+':SOURCE_NOT_FOUND');return
    body=p.read_bytes()
    if sha(body)!=wanted or quote.encode() not in body:errors.append(code+':SOURCE_HASH_OR_QUOTE_DISAGREES')

def check_history(obj,errors):
    if not isinstance(obj,dict) or obj.get('schema')!='ANVIL_R7_INHERITED_CONSERVATION':
        errors.append('HISTORY:WRONG_SCHEMA');return
    coverage=obj.get('coverage',{})
    if not isinstance(coverage,dict) or set(coverage)!=set(REQUIRED):
        errors.append('HISTORY:GROUPS_NOT_INHERITED');return
    count=0
    for group,ids in REQUIRED.items():
        rows=coverage.get(group,{})
        if not isinstance(rows,dict) or set(rows)!=set(ids):errors.append('HISTORY:ID_SET_DRIFT:'+group);continue
        for rid,entry in rows.items():
            count+=1
            if not isinstance(entry,dict):errors.append('HISTORY:NO_RECORD:'+rid);continue
            for key in ('source_anchor','source_semantics','consumer_or_hold','negative_meaning','architecture_effect','why'):
                if not good(entry.get(key),12):errors.append('HISTORY:SEMANTIC_OR_CONSUMER_LOSS:'+rid+':'+key)
            if not isinstance(entry.get('evidence_ids'),list) or not entry['evidence_ids']:
                errors.append('HISTORY:NO_EVIDENCE:'+rid)
            if group=='PYAT_PC' and (entry.get('adopted') is not False or entry.get('necessity')!='HISTORICAL_NOT_ADOPTED'):
                errors.append('HISTORY:FALSE_PROSPECTIVE_ADOPTION:'+rid)
            if group=='P4R' and (entry.get('closed') is not False or entry.get('necessity')!='HISTORICAL_PROOF_HELD'):
                errors.append('HISTORY:FALSE_PROOF_CLOSURE:'+rid)
    if count!=sum(map(len,REQUIRED.values())):errors.append('HISTORY:COUNT_DRIFT')
    if obj.get('source_authentication')!='NOT_AUTHENTICATED_BY_LOCAL_CHECK':errors.append('HISTORY:FALSE_SOURCE_AUTHENTICATION')

def check_graph(graph,errors,code='GRAPH'):
    """Typed whole-machine graph: producer, authority, time and consumer are explicit.

    This is a structural contract check, not proof that any edge executed.
    """
    if not isinstance(graph,dict):errors.append(code+':NOT_OBJECT');return
    nodes=graph.get('nodes');edges=graph.get('edges')
    if not isinstance(nodes,list) or not nodes:errors.append(code+':NO_NODES');nodes=[]
    if not isinstance(edges,list) or not edges:errors.append(code+':NO_EDGES');edges=[]
    nmap={};emap={}
    for n in nodes:
        if not isinstance(n,dict):errors.append(code+':BAD_NODE');continue
        rid=n.get('id')
        if not isinstance(rid,str) or not rid or rid in nmap:errors.append(code+':DUPLICATE_OR_MISSING_NODE')
        nmap[rid]=n
        for k in ('producer','producer_authority','input_types','output_types','time_mode','first_consumer','decision_id','alternative_id'):
            if k in ('input_types','output_types'):
                if not isinstance(n.get(k),list) or not n[k]:errors.append(code+':NODE_FIELD:'+str(rid)+':'+k)
            elif not good(n.get(k),2 if k in ('first_consumer','decision_id','alternative_id','time_mode') else 8):errors.append(code+':NODE_FIELD:'+str(rid)+':'+k)
        if n.get('time_mode') not in GRAPH_TIME:errors.append(code+':BAD_TIME_MODE:'+str(rid))
    for edge in edges:
        if not isinstance(edge,dict):errors.append(code+':BAD_EDGE');continue
        rid=edge.get('id')
        if not isinstance(rid,str) or not rid or rid in emap:errors.append(code+':DUPLICATE_OR_MISSING_EDGE')
        emap[rid]=edge
        for k in ('from','to','data_type','authority_grade','temporal_mode','negative_or_refusal','invalidation_rule','boundary'):
            if not good(edge.get(k),2 if k in ('from','to','boundary') else 6):errors.append(code+':EDGE_FIELD:'+str(rid)+':'+k)
        a=nmap.get(edge.get('from'));b=nmap.get(edge.get('to'))
        if not a or not b:errors.append(code+':ORPHAN_EDGE:'+str(rid));continue
        if edge.get('data_type') not in a.get('output_types',[]) or edge.get('data_type') not in b.get('input_types',[]):
            errors.append(code+':TYPE_MISMATCH:'+str(rid))
        if edge.get('boundary') not in BOUND_IDS:errors.append(code+':BAD_BOUNDARY:'+str(rid))
        if a.get('time_mode') in ('FICTIONAL','MODELED') and b.get('time_mode')=='OBSERVED':
            errors.append(code+':FICTIONAL_BACKFLOW:'+str(rid))
    for t in BOUND_IDS:
        if not any(e.get('boundary')==t for e in edges if isinstance(e,dict)):errors.append(code+':BOUNDARY_EDGE_MISSING:'+t)

def check_identity_dispositions(decision,inventory,source_root,errors,evidence_root=None):
    """Every one of the 118 identities must have a candidate-specific disposition.

    Presence of an ID is not preservation.  The origin must match the verified
    inventory row; 26 proposals cannot be adopted and 14 proofs cannot be closed.
    """
    if inventory is None:errors.append('DECISION:NO_VERIFIED_INVENTORY');return
    rows=decision.get('identity_dispositions')
    if not isinstance(rows,list):errors.append('DECISION:NO_IDENTITY_DISPOSITIONS');return
    inv={e['id']:e for e in inventory.get('entries',[]) if isinstance(e,dict)}
    dmap={}
    for x in rows:
        if not isinstance(x,dict):errors.append('DECISION:BAD_IDENTITY_DISPOSITION');continue
        rid=x.get('identity_id')
        if rid in dmap:errors.append('DECISION:DUPLICATE_IDENTITY_DISPOSITION:'+str(rid))
        dmap[rid]=x
    if set(dmap)!=set(inv) or len(rows)!=len(inv):errors.append('DECISION:INCOMPLETE_118_IDENTITY_RECONCILIATION')
    for rid,row in dmap.items():
        base=inv.get(rid)
        if base is None:errors.append('DECISION:UNKNOWN_IDENTITY:'+str(rid));continue
        state=row.get('disposition')
        if state not in IDENTITY_STATES:errors.append('DECISION:BAD_IDENTITY_DISPOSITION:'+str(rid))
        if state=='RETAINED_HISTORICAL_NONADOPTED' and base.get('group') not in ('PYAT_PC','P4R'):
            errors.append('DECISION:HISTORICAL_NONADOPTION_OVERUSED:'+str(rid))
        if base.get('group')=='PYAT_PC' and row.get('adopted_by_this_decision') is not False:errors.append('DECISION:PROSPECTIVE_ADOPTION:'+str(rid))
        if base.get('group')=='P4R' and row.get('closed_by_this_decision') is not False:errors.append('DECISION:FALSE_PROOF_CLOSURE:'+str(rid))
        if row.get('status_assertion') in ('ADOPTED','CLOSED') and base.get('group') in ('PYAT_PC','P4R'):
            errors.append('DECISION:SILENT_HISTORICAL_PROMOTION:'+str(rid))
        for k in ('design_effect','first_consumer_path','conservation_or_refusal_witness'):
            if not good(row.get(k),38):errors.append('DECISION:VACUOUS_IDENTITY_EFFECT:'+str(rid)+':'+k)
        if row.get('evidence_grade') not in GRADES:errors.append('DECISION:BAD_IDENTITY_EVIDENCE_GRADE:'+str(rid))
        source_ref(row.get('evidence'),source_root,errors,'DECISION:IDENTITY_EVIDENCE:'+str(rid))
        if row.get('origin_sha256')!=base.get('origin_sha256'):errors.append('DECISION:IDENTITY_ORIGIN_DRIFT:'+str(rid))
        if state in ('PRESENT_PRESERVED','FUTURE_NONPRECLUDED') and not row.get('evidence'):
            errors.append('DECISION:UNPROVED_IDENTITY_PRESERVATION:'+str(rid))

def check_frame(frame,evidence_root,source_root,repo=None):
    e=[]
    if not isinstance(frame,dict) or frame.get('schema')!=SCHEMA or frame.get('stage')!='COMMON_FRAME':
        return {'status':'RED','errors':['FRAME:BAD_SCHEMA']}
    if frame.get('workflow')!='ONE_INTEGRATED_INVESTIGATION_OPTIONAL_TARGETED_DUELS':e.append('FRAME:DIVIDED_ARCHITECT_WORKFLOW_FORBIDDEN')
    if frame.get('phase')!='BEFORE_ARCHITECTURE_SELECTION':e.append('FRAME:WRONG_CHRONOLOGY')
    if frame.get('architecture_selected') is not False:e.append('FRAME:ARCHITECTURE_PRESELECTED')
    if frame.get('mandatory_rival_architecture') is not False:e.append('FRAME:RIVAL_NOT_OPTIONAL')
    if frame.get('A_B_method')!='OPTIONAL_SAME_QUESTION_SAME_EVIDENCE':e.append('FRAME:DUEL_METHOD_DISTORTED')
    if frame.get('scope') not in ('C11_QUERY_DESIGN','F1_F4_CONSUMER_DESIGN','FF_FIRST_EFFECT_DESIGN'):e.append('FRAME:INVALID_SCOPE')
    for name in ('source_cut','protected_head'):
        if not isinstance(frame.get(name),str) or not HEX40.fullmatch(frame[name]):e.append('FRAME:UNPINNED_'+name)
    for name in ('user_priority_source','first_real_consumer','currentness_gap_or_exact_verified_state','science_authority_boundary','whole_program_mission'):
        if not good(frame.get(name),35):e.append('FRAME:UNDERDEFINED_'+name)
    if frame.get('source_grades_authentic_by_local_test') is not False:e.append('FRAME:FALSE_SOURCE_AUTHORITY')
    # S1 identity source: a source-authenticated inventory, never an R5/R6 SPINE.
    inventory=None
    if not isinstance(frame.get('source_inventory'),dict):
        e.append('FRAME:NO_SOURCE_IDENTITY_INVENTORY')
    else:
        inventory=load(evidence_root,frame.get('source_inventory'),e,'FRAME:SOURCE_INVENTORY')
        if inventory is not None:
            res=check_inventory(inventory,source_root,repo)
            if res['status']=='RED':e.extend('FRAME:INVENTORY:'+x for x in res['errors'])
    # A legacy R5/R6 transfer is optional historical evidence only.  It cannot
    # supply identity truth; a synthetic self-consistent spine is not a source.
    if frame.get('historical_source_spine') is not None or frame.get('historical_conservation') is not None:
        if not isinstance(frame.get('historical_conservation'),dict):
            e.append('FRAME:LEGACY_TRANSFER_WITHOUT_CONSERVATION')
        else:
            hist=load(evidence_root,frame.get('historical_conservation'),e,'FRAME:HISTORY')
            if hist is not None:check_history(hist,e)
        if inventory is None:e.append('FRAME:LEGACY_SPINE_CANNOT_SUBSTITUTE_FOR_SOURCE_INVENTORY')
    rows=frame.get('requirements')
    if not isinstance(rows,list):rows=[];e.append('FRAME:REQUIREMENTS_NOT_LIST')
    seen=set();have=set()
    for row in rows:
        if not isinstance(row,dict):e.append('FRAME:BAD_REQUIREMENT');continue
        key=row.get('id');domain=row.get('domain');have.add(domain)
        if not isinstance(key,str) or not key or key in seen:e.append('FRAME:DUPLICATE_OR_MISSING_ID')
        seen.add(key)
        if domain not in DOMAINS:e.append('FRAME:UNRECOGNIZED_DOMAIN:'+str(domain))
        if row.get('binding') not in BINDS:e.append('FRAME:BAD_BINDING:'+str(key))
        for k in ('substantive_requirement','why_needed','loss_if_missing','first_consumer','architectural_consequence','proof_or_owner_hold'):
            if not good(row.get(k),28):e.append('FRAME:VACUOUS_'+str(key)+':'+k)
        source_ref(row.get('evidence'),source_root,e,'FRAME:EVIDENCE:'+str(key))
        if row.get('binding')=='EXTERNAL_OWNER_HELD' and not good(row.get('authority_owner'),10):e.append('FRAME:OWNER_NOT_NAMED:'+str(key))
    for domain in DOMAINS:
        if domain not in have:e.append('FRAME:WHOLE_MISSION_DOMAIN_MISSING:'+domain)
    if frame.get('duel_required') is not False:e.append('FRAME:UNNECESSARY_DUEL_REQUIRED')
    return {'status':'RED' if e else 'PASS_LOCAL_COMMON_REQUIREMENTS_SOURCE_IDENTITY_NOT_NATIVE_AUTHENTICATED','errors':sorted(set(e)),
            'requirements':len(rows),'domains':len(have&set(DOMAINS)),
            'identity_inventory_total':len(inventory.get('entries',[])) if inventory else 0}

def check_duel(duel,frame_sha,errors):
    if not isinstance(duel,dict) or duel.get('schema')!='ANVIL_R7_TARGETED_DUEL':errors.append('DECISION:DUEL_BAD_SCHEMA');return
    if duel.get('shared_frame_sha256')!=frame_sha:errors.append('DECISION:DUEL_DIFFERENT_PREMISES')
    if not good(duel.get('single_decision_question'),40):errors.append('DECISION:DUEL_NOT_SINGLE_QUESTION')
    if not good(duel.get('why_independence_is_needed'),40):errors.append('DECISION:DUEL_NO_JUSTIFICATION')
    if not good(duel.get('shared_evidence_description'),40):errors.append('DECISION:DUEL_MISSING_SHARED_EVIDENCE')
    investigators=duel.get('investigators')
    if not isinstance(investigators,list) or len(investigators)!=2 or len({i.get('id') for i in investigators if isinstance(i,dict)})!=2:
        errors.append('DECISION:DUEL_NOT_TWO_DISTINCT_PEERS');return
    if any(i.get('shared_frame_sha256')!=frame_sha or i.get('evidence_access')!='SAME_FULL_EVIDENCE' or not good(i.get('analysis'),40) for i in investigators):
        errors.append('DECISION:DUEL_DIVIDED_EVIDENCE_OR_NO_ANALYSIS')
    if any(i.get('assignment') not in ('SAME_EXACT_QUESTION_INDEPENDENT_ANALYSIS',) for i in investigators):
        errors.append('DECISION:DUEL_SPLIT_ASSIGNMENTS_FORBIDDEN')
    if not good(duel.get('integrated_adjudication'),50):errors.append('DECISION:DUEL_NOT_INTEGRATED')
    if duel.get('independence_proven_by_local_check') is not False:errors.append('DECISION:DUEL_SELF_CERTIFIES_INDEPENDENCE')

def check_decision(decision,evidence_root,source_root,repo=None):
    e=[]
    if not isinstance(decision,dict) or decision.get('schema')!=SCHEMA or decision.get('stage')!='INTEGRATED_DECISION':
        return {'status':'RED','errors':['DECISION:BAD_SCHEMA']}
    frame=load(evidence_root,decision.get('common_frame'),e,'DECISION:FRAME')
    if frame is None:return {'status':'RED','errors':sorted(set(e))}
    fr=check_frame(frame,evidence_root,source_root,repo)
    if fr['status']=='RED':e.extend('DECISION:INVALID_FRAME:'+v for v in fr['errors'])
    frozen_sha=digest(frame)
    if decision.get('frame_sha256')!=frozen_sha:e.append('DECISION:FRAME_NOT_FROZEN')
    if decision.get('first_real_consumer')!=frame.get('first_real_consumer'):e.append('DECISION:FIRST_CONSUMER_DRIFT')
    if decision.get('decision_process')!='ONE_SYNTHESIS_NO_MANDATORY_RIVAL':e.append('DECISION:WRONG_PROCESS')
    if decision.get('basis') not in ('ANALYTICAL_SOURCE_GROUNDED','EXECUTED_EXISTING_CODE','BOUNDED_DISCRIMINATOR','TARGETED_DUEL'):
        e.append('DECISION:UNKNOWN_BASIS')
    if decision.get('grade') not in ('AUTHOR_PROPOSED_PENDING_C','CONDITIONAL_DIRECTION','EXACT_HOLD'):
        e.append('DECISION:FALSE_AUTHORITY_GRADE')
    for k in ('architecture_description','entire_source_to_actor_dataflow','algorithm_and_data_structures','resource_cost_reasoning',
              'historical_function_conservation','scientific_boundary_and_nonpreclusion','strongest_surviving_objection',
              'why_selected_over_feasible_alternatives','next_actual_engineering_operation'):
        if not good(decision.get(k),55):e.append('DECISION:UNDERARGUED_'+k)
    if not good(decision.get('single_selected_strategy'),10) and decision.get('grade')!='EXACT_HOLD':
        e.append('DECISION:NO_PROPOSED_STRATEGY')
    alternatives=decision.get('alternatives_considered')
    if not isinstance(alternatives,list) or not alternatives:e.append('DECISION:ALTERNATIVES_NOT_ANALYTICALLY_CONSIDERED')
    else:
        for j,a in enumerate(alternatives):
            if not isinstance(a,dict) or not good(a.get('technical_approach'),20) or not good(a.get('why_not_selected_or_held'),45) or a.get('state') not in ('RULED_OUT_BY_REASON','VIABLE_NOT_SELECTED','UNRESOLVED_HOLD'):
                e.append('DECISION:ALTERNATIVE_UNREASONED:'+str(j))
    reversers=decision.get('choice_reversers')
    if not isinstance(reversers,list):e.append('DECISION:NO_REVERSER_ACCOUNTING')
    elif decision.get('grade')=='AUTHOR_PROPOSED_PENDING_C' and any(isinstance(r,dict) and r.get('status')=='UNRESOLVED_CHOICE_CHANGING' for r in reversers):
        e.append('DECISION:CHOICE_CHANGING_UNCERTAINTY_HIDDEN')
    if decision.get('requires_full_A_B_comparison') is not False:e.append('DECISION:COMPETITION_REQUIRED')
    if decision.get('architecture_claims_independent_acceptance') is not False:e.append('DECISION:UNAUTHORIZED_ACCEPTANCE')
    # All 118 identities: candidate-specific, non-vacuous and source-origin-bound.
    inv=load(evidence_root,frame.get('source_inventory'),e,'DECISION:INVENTORY') if isinstance(frame.get('source_inventory'),dict) else None
    check_identity_dispositions(decision,inv,source_root,e)
    # Typed whole-machine graph: producer / authority / time / consumer.
    check_graph(decision.get('whole_machine_graph'),e,'DECISION:GRAPH')
    # No local H1 or protected receiving.
    if decision.get('h1_received_by_local_check') is not False:e.append('DECISION:LOCAL_H1_CLAIM')
    if decision.get('protected_received_by_local_check') is not False:e.append('DECISION:LOCAL_PROTECTED_RECEIVING')
    if decision.get('codex_53_used_as_118') is True:e.append('DECISION:PARTIAL_53_CROSSWALK_SUBSTITUTES_FOR_118')
    reqs=frame.get('requirements',[])
    covers=decision.get('requirement_dispositions',[])
    if not isinstance(covers,list):covers=[];e.append('DECISION:NO_REQUIREMENT_DISPOSITIONS')
    rids={r['id'] for r in reqs if isinstance(r,dict) and isinstance(r.get('id'),str)}
    dmap={x.get('requirement_id'):x for x in covers if isinstance(x,dict)}
    if set(dmap)!=rids or len(covers)!=len(rids):e.append('DECISION:INCOMPLETE_REQUIREMENT_RECONCILIATION')
    for row in reqs:
        if not isinstance(row,dict):continue
        rid=row.get('id');x=dmap.get(rid,{})
        state=x.get('disposition')
        if state not in DISPOS:e.append('DECISION:BAD_DISPOSITION:'+str(rid))
        if row.get('binding')=='PRESENT_HARD' and state not in ('PRESENT_PRESERVED','BLOCKING_LOSS'):
            e.append('DECISION:HARD_PRESENT_RELABELED_FUTURE:'+str(rid))
        if row.get('binding')=='EXTERNAL_OWNER_HELD' and state=='PRESENT_PRESERVED' and x.get('evidence_grade') not in ('EXECUTED_SOURCEFREE','EXECUTED_NATIVE'):
            e.append('DECISION:HELD_SCIENCE_PROMOTED:'+str(rid))
        for k in ('actual_design_effect','specific_first_consumer_path','conservation_or_refusal_witness'):
            if not good(x.get(k),38):e.append('DECISION:VACUOUS_DISPOSITION:'+str(rid)+':'+k)
        if x.get('evidence_grade') not in GRADES:e.append('DECISION:BAD_EVIDENCE_GRADE:'+str(rid))
        if state in ('PRESENT_PRESERVED','FUTURE_NONPRECLUDED'):
            source_ref(x.get('evidence'),source_root,e,'DECISION:UNPROVED_PRESERVATION:'+str(rid))
    if decision.get('grade')=='AUTHOR_PROPOSED_PENDING_C' and any(x.get('disposition')=='BLOCKING_LOSS' for x in covers if isinstance(x,dict)):
        e.append('DECISION:READY_WHILE_LOSING_REQUIRED_FUNCTION')
    if decision.get('grade')=='AUTHOR_PROPOSED_PENDING_C' and any(x.get('disposition')=='BLOCKING_LOSS' for x in decision.get('identity_dispositions',[]) if isinstance(x,dict)):
        e.append('DECISION:READY_WHILE_LOSING_IDENTITY')
    if decision.get('grade')=='AUTHOR_PROPOSED_PENDING_C' and any(x.get('disposition')=='EXACT_OWNER_HOLD' for x in covers if isinstance(x,dict)
              and any(r.get('id')==x.get('requirement_id') and r.get('binding')=='PRESENT_HARD' for r in reqs)):
        e.append('DECISION:READY_WITH_PRESENT_HARD_HOLD')
    if decision.get('basis')=='TARGETED_DUEL':
        duel=load(evidence_root,decision.get('targeted_duel'),e,'DECISION:OPTIONAL_DUEL')
        if duel is not None:check_duel(duel,frozen_sha,e)
    elif decision.get('targeted_duel') is not None:e.append('DECISION:DUEL_PRESENT_WITHOUT_GROUNDED_NEED')
    # A/B comparison is a specialist input, never a globally mandatory decision oracle.
    if decision.get('competing_implementations_mandatory') is not False:e.append('DECISION:MANDATORY_BACKEND_BAKEOFF')
    return {'status':'RED' if e else 'PASS_LOCAL_INTEGRATED_DECISION_PENDING_C','errors':sorted(set(e)),
            'covered':len(covers),'requirement_total':len(rids),
            'identity_dispositions':len(decision.get('identity_dispositions',[])) if isinstance(decision.get('identity_dispositions'),list) else 0}

def check_boundary_court(court,evidence_root,source_root,errors,admit):
    if not isinstance(court,dict) or set(court)!=set(BOUND_IDS):
        errors.append('C:INCOMPLETE_BOUNDARY_COURT');return
    for t in BOUND_IDS:
        x=court.get(t)
        if not isinstance(x,dict):errors.append('C:BAD_BOUNDARY_COURT:'+t);continue
        for k in ('positive','negative','restore'):
            if not good(x.get(k),30):errors.append('C:BOUNDARY_MISSING_'+k.upper()+':'+t)
        if x.get('grade') not in ('EXECUTED_AT_SCOPE','SOURCE_STATIC_CONSERVED','NOT_RUN'):
            errors.append('C:BOUNDARY_BAD_GRADE:'+t)
        if admit and x.get('grade')=='NOT_RUN':errors.append('C:ADMIT_WITH_UNRUN_BOUNDARY:'+t)
        if x.get('grade')!='NOT_RUN':
            source_ref(x.get('evidence'),source_root,errors,'C:BOUNDARY_EVIDENCE:'+t)
        else:
            if not good(x.get('exact_hold'),30):errors.append('C:BOUNDARY_NOT_RUN_WITHOUT_EXACT_HOLD:'+t)
        if not good(x.get('first_consumer_or_hold'),20):errors.append('C:BOUNDARY_NO_CONSUMER_OR_HOLD:'+t)

def check_C(packet,evidence_root,source_root,repo=None):
    e=[]
    if not isinstance(packet,dict) or packet.get('schema')!=SCHEMA or packet.get('stage')!='INDEPENDENT_C':
        return {'status':'RED','errors':['C:BAD_SCHEMA']}
    decision=load(evidence_root,packet.get('integrated_decision'),e,'C:DECISION')
    if decision is not None:
        verdict=check_decision(decision,evidence_root,source_root,repo)
        if verdict['status']=='RED':e.extend('C:DEFECTIVE_DECISION:'+x for x in verdict['errors'])
        if packet.get('integrated_decision_sha256')!=digest(decision):e.append('C:DECISION_NOT_PINNED')
        if packet.get('first_consumer')!=decision.get('first_real_consumer'):
            e.append('C:CONSUMER_CHANGED')
    for k in ('independent_reverse_walk_of_whole_frame','strongest_choice_reversing_objection',
              'scientific_and_owner_boundary','actual_first_consumer_assessment','historical_no_loss_assessment'):
        if not good(packet.get(k),60):e.append('C:INSUFFICIENT_'+k)
    admit=packet.get('verdict')=='C_CONDITIONALLY_ADMIT_DESIGN'
    check_boundary_court(packet.get('boundary_court'),evidence_root,source_root,e,admit)
    audit=packet.get('graph_audit')
    if not isinstance(audit,dict):e.append('C:NO_TYPED_GRAPH_AUDIT')
    else:
        if audit.get('producer_authority_time_consumer_checked') is not True:e.append('C:GRAPH_AUDIT_NOT_TYPED')
        holes=audit.get('holes')
        if not isinstance(holes,list):e.append('C:GRAPH_HOLES_NOT_LIST')
        elif holes:e.append('C:TYPED_GRAPH_HOLE')
        if set(audit.get('boundary_edges_checked',[]))!=set(BOUND_IDS):e.append('C:GRAPH_BOUNDARY_COVERAGE_MISSING')
    if not good(packet.get('builder_handoff_review'),60):e.append('C:NO_ACTUAL_BUILDER_HANDOFF_REVIEW')
    if admit and packet.get('actual_first_reader_verified') is not True:e.append('C:ADMIT_WITHOUT_ACTUAL_FIRST_READER')
    cards=packet.get('builder_cards')
    if not isinstance(cards,list) or len(cards)!=2 or {c.get('domain') for c in cards if isinstance(c,dict)}!={'CURRENT_FIRST_CONSUMER','FUTURE_NONPRECLUSION'}:
        e.append('C:REQUIRES_PRESENT_AND_FUTURE_BUILDER_CARDS')
    else:
        from r7_stage import check_builder
        for card in cards:e.extend('C:BUILDER:'+v for v in check_builder(card,source_root,evidence_root))
        present=next(c for c in cards if c['domain']=='CURRENT_FIRST_CONSUMER')
        if admit and present.get('grade')=='EXACT_BUILDER_HOLD':
            e.append('C:ADMIT_WITHOUT_CURRENT_BUILDER')
    if packet.get('reviewer_relationship')!='DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION':
        e.append('C:SELF_CERTIFIED_INDEPENDENCE')
    if packet.get('choice_reversing_objection_survives') is not False and admit:
        e.append('C:ACCEPTS_SURVIVING_REVERSER')
    if packet.get('verdict') not in ('C_CONDITIONALLY_ADMIT_DESIGN','C_HOLD_EXACT'):
        e.append('C:FALSE_C_GRADE')
    if packet.get('original_source_granted_by_local_check') is not False or packet.get('owner_granted_by_local_check') is not False:
        e.append('C:FALSE_AUTHORITY')
    if packet.get('local_h1_claim') is not False or packet.get('protected_received_locally') is not False:
        e.append('C:LOCAL_H1_OR_PROTECTED_CLAIM')
    if packet.get('h1_grade')=='ACCEPTED':e.append('C:LOCAL_H1_ACCEPTED')
    return {'status':'RED' if e else 'PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED','errors':sorted(set(e))}

def check(stage,packet,evidence_root,source_root=None,repo=None):
    if stage=='FRAME':return check_frame(packet,evidence_root,source_root,repo)
    if stage=='DECISION':return check_decision(packet,evidence_root,source_root,repo)
    if stage=='C_INTEGRATED':return check_C(packet,evidence_root,source_root,repo)
    return {'status':'RED','errors':['ACTIVE_STAGE_UNKNOWN']}

def main():
    ap=argparse.ArgumentParser(description='Active ANVIL integral workflow, NOT autonomous accreditation')
    ap.add_argument('stage',choices=['FRAME','DECISION','C_INTEGRATED'])
    ap.add_argument('packet');ap.add_argument('--evidence-root',required=True);ap.add_argument('--source-root',required=True)
    ap.add_argument('--repo',help='optional Git object store for commit/blob verification of the source inventory')
    arg=ap.parse_args()
    try:out=check(arg.stage,json.loads(pathlib.Path(arg.packet).read_text()),arg.evidence_root,arg.source_root,arg.repo)
    except (OSError,ValueError,TypeError,KeyError) as exc:out={'status':'RED','errors':['UNHANDLED_MALFORMED_PACKET:'+repr(exc)]}
    print(json.dumps(out,indent=2));return 2 if out['status']=='RED' else 0
if __name__=='__main__':sys.exit(main())
