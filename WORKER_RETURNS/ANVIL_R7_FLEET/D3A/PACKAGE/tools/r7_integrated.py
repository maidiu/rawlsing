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
from r7_source_inventory import verify_inventory, row_hash_map, Anchors as SourceAnchors

SCHEMA='ANVIL_R7_INTEGRATED'
HEX40=re.compile(r'^[a-f0-9]{40}$')
HEX64=re.compile(r'^[a-f0-9]{64}$')
DOMAINS=('SOURCE_SEMANTICS','C11_PERSISTENCE','CURRENT_I03_I05',
         'HISTORICAL_DDM_FUNCTIONS','F1_F4_ANALYTICS','FIELD_FORGE',
         'SEAM_WORLD_ACTOR','AUTHORITY_AND_RECOVERY','RESOURCE_ECONOMICS')
BINDS={'PRESENT_HARD','FUTURE_NONPRECLUSION','EXTERNAL_OWNER_HELD'}
DISPOS={'PRESENT_PRESERVED','FUTURE_NONPRECLUDED','EXACT_OWNER_HOLD','BLOCKING_LOSS'}
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

def check_history(obj,errors,evidence_root=None,source_root=None,require_origin=True,anchors=None):
    """S1 conservation origin.  A bare R5/R6 SPINE is NOT accepted as origin.

    Two lawful origins exist:
      * ANVIL_SOURCE_QUALIFIED_INVENTORY — every row byte-located in supplied source;
      * ANVIL_R7_INHERITED_CONSERVATION — legacy transfer, admissible only when it
        points at a verified source-qualified inventory (`origin_inventory`).
    This removes the false dependency on an already-finished R5 P2 SPINE while
    still refusing a synthetic SPINE that merely imitates the original.
    """
    if not isinstance(obj,dict):
        errors.append('HISTORY:NOT_OBJECT');return
    schema=obj.get('schema')
    if schema=='ANVIL_SOURCE_QUALIFIED_INVENTORY':
        verify_inventory(obj,source_root or '',errors,'HISTORY',anchors=anchors)
        return
    if schema in ('ANVIL_SPINE_R5','ANVIL_SPINE_R6'):
        errors.append('HISTORY:NOT_SOURCE_QUALIFIED_INVENTORY');return
    if schema!='ANVIL_R7_INHERITED_CONSERVATION':
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
    if not require_origin:return
    inv=load(evidence_root,obj.get('origin_inventory'),errors,'HISTORY:ORIGIN_INVENTORY') if evidence_root else None
    if inv is None:
        errors.append('HISTORY:LEGACY_TRANSFER_WITHOUT_SOURCE_QUALIFIED_ORIGIN')
    else:
        verify_inventory(inv,source_root or '',errors,'HISTORY:ORIGIN',anchors=anchors)
        imap={r.get('id'):r for r in inv.get('rows',[]) if isinstance(r,dict)}
        for group,ids in REQUIRED.items():
            for rid in ids:
                a=coverage.get(group,{}).get(rid,{});b=imap.get(rid,{})
                for key in ('source_semantics','negative_meaning','consumer_or_hold'):
                    if isinstance(a,dict) and isinstance(b,dict) and a.get(key)!=b.get(key):
                        errors.append('HISTORY:TRANSFER_NOT_VERBATIM_TO_SOURCE:'+rid+':'+key)

def check_frame(frame,evidence_root,source_root,anchors=None):
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
    history=load(evidence_root,frame.get('historical_conservation'),e,'FRAME:HISTORY')
    if history is not None:
        check_history(history,e,evidence_root,source_root,anchors=anchors)
        spine=frame.get('historical_source_spine')
        if spine is not None:
            original=load(evidence_root,spine,e,'FRAME:SOURCE_SPINE')
            if original is not None:
                if original.get('schema') not in ('ANVIL_SPINE_R5','ANVIL_SPINE_R6'):
                    e.append('FRAME:SOURCE_SPINE_NOT_EXISTING_R5_R6')
                if history.get('schema')=='ANVIL_R7_INHERITED_CONSERVATION':
                    if original.get('coverage')!=history.get('coverage'):
                        e.append('FRAME:HISTORICAL_TRANSFER_NOT_BYTE_EQUIVALENT_TO_SOURCE_COVERAGE')
                # A SPINE may accompany the frame as a historical pointer only.  It is
                # never the origin of S1: every row must still resolve to real bytes.
                if not isinstance(original.get('coverage'),dict) or sum(len(v) for v in original['coverage'].values() if isinstance(v,dict))!=sum(map(len,REQUIRED.values())):
                    e.append('FRAME:SOURCE_SPINE_NOT_THE_118_UNIVERSE')
    if frame.get('duel_required') is not False:e.append('FRAME:UNNECESSARY_DUEL_REQUIRED')
    return {'status':'RED' if e else 'PASS_LOCAL_COMMON_REQUIREMENTS_NOT_OWNER_AUTHENTICATED','errors':sorted(set(e)),
            'requirements':len(rows),'domains':len(have&set(DOMAINS))}

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

STOP=set('the and for with from that this must shall into their there which where when only also each such than then they them these those have has been being will would could should about under over more most less least same different other another not non no yes can may need needs needed used using case cases given provide provided require required requirement specific exactly identity identities source sources evidence'.split())

def _tokens(text):
    return {t for t in re.findall(r'[a-z0-9_]{5,}',(text or '').lower()) if t not in STOP}

def check_identity_crosswalk(decision,frame,history,identity_map,errors):
    """S3 must reconcile the WHOLE 118 identity universe, not nine mission domains.

    A complete 53-row subset with one distinct historical functional decision
    missing is a hard RED, not a scoped PASS.
    """
    rows=decision.get('identity_dispositions')
    inv_sha=identity_map.get('__inventory_sha__')
    if decision.get('inventory_sha256')!=inv_sha:
        errors.append('DECISION:INVENTORY_NOT_PINNED')
    if not isinstance(rows,list):
        errors.append('DECISION:NO_IDENTITY_DISPOSITIONS');return 0
    want={
        'K1_CAP':set(REQUIRED['K1_CAP']),'PYAT_PC':set(REQUIRED['PYAT_PC']),'P4R':set(REQUIRED['P4R']),
        'SEAM_B':set(REQUIRED['SEAM_B']),'SEAM_S':set(REQUIRED['SEAM_S']),'ANVIL_L':set(REQUIRED['ANVIL_L']),
        'BOUNDARY':set(REQUIRED['BOUNDARY']),'TERMINAL':set(REQUIRED['TERMINAL'])}
    got=set();dupes=set()
    for x in rows:
        if not isinstance(x,dict):errors.append('DECISION:BAD_IDENTITY_ROW');continue
        rid=x.get('identity_id')
        if rid in got:dupes.add(rid)
        got.add(rid)
        group=next((g for g,ids in want.items() if rid in ids),None)
        if group is None:errors.append('DECISION:UNKNOWN_IDENTITY:'+str(rid));continue
        state=x.get('disposition')
        if state not in DISPOS:errors.append('DECISION:BAD_IDENTITY_DISPOSITION:'+str(rid))
        for k in ('candidate_specific_effect','first_consumer_consequence','conservation_or_refusal_witness'):
            if not good(x.get(k),45):errors.append('DECISION:VACUOUS_IDENTITY_DISPOSITION:'+str(rid)+':'+k)
        oh=x.get('origin_row_sha256')
        if not isinstance(oh,str) or not HEX64.fullmatch(oh) or identity_map.get(rid)!=oh:
            errors.append('DECISION:IDENTITY_ORIGIN_NOT_VERIFIED:'+str(rid))
        inv=history.get('rows') if isinstance(history.get('rows'),list) else []
        sem=next((r.get('source_semantics','') for r in inv if isinstance(r,dict) and r.get('id')==rid),'')
        overlap=_tokens(x.get('candidate_specific_effect'))&_tokens(sem)
        if len(overlap)<2:
            errors.append('DECISION:IDENTITY_EFFECT_NOT_GROUNDED_IN_ORIGIN:'+str(rid))
        if group=='PYAT_PC':
            if x.get('adopted') is not False:errors.append('DECISION:UNAUTHORIZED_PROPOSAL_ADOPTION:'+str(rid))
            if state=='PRESENT_PRESERVED':errors.append('DECISION:UNAUTHORIZED_PROPOSAL_ADOPTION:'+str(rid))
        if group=='P4R':
            if x.get('closed') is not False:errors.append('DECISION:FALSE_PROOF_CLOSURE:'+str(rid))
            if state=='PRESENT_PRESERVED':errors.append('DECISION:FALSE_PROOF_CLOSURE:'+str(rid))
        if state=='EXACT_OWNER_HOLD' and not good(x.get('owner'),8):
            errors.append('DECISION:IDENTITY_HOLD_WITHOUT_OWNER:'+str(rid))
    if dupes:errors.append('DECISION:DUPLICATE_IDENTITY_DISPOSITION:'+','.join(sorted(dupes)[:4]))
    for g,ids in want.items():
        miss=sorted(ids-got)
        if miss:errors.append('DECISION:IDENTITY_UNIVERSE_INCOMPLETE:'+g+':'+','.join(miss[:4]))
    extra=sorted(got-set().union(*want.values()))
    if extra:errors.append('DECISION:IDENTITY_UNIVERSE_HAS_EXTRA:'+','.join(extra[:4]))
    return len(rows)


def check_decision(decision,evidence_root,source_root,anchors=None):
    e=[]
    if not isinstance(decision,dict) or decision.get('schema')!=SCHEMA or decision.get('stage')!='INTEGRATED_DECISION':
        return {'status':'RED','errors':['DECISION:BAD_SCHEMA']}
    frame=load(evidence_root,decision.get('common_frame'),e,'DECISION:FRAME')
    if frame is None:return {'status':'RED','errors':sorted(set(e))}
    fr=check_frame(frame,evidence_root,source_root,anchors)
    if fr['status']=='RED':e.extend('DECISION:INVALID_FRAME:'+v for v in fr['errors'])
    frozen_sha=digest(frame)
    if decision.get('frame_sha256')!=frozen_sha:e.append('DECISION:FRAME_NOT_FROZEN')
    hist=load(evidence_root,frame.get('historical_conservation'),e,'DECISION:HISTORY')
    idmap={'__inventory_sha__':digest(hist) if hist else None}
    if isinstance(hist,dict):
        if hist.get('schema')=='ANVIL_SOURCE_QUALIFIED_INVENTORY':
            idmap.update(row_hash_map(hist))
        else:
            for r in hist.get('coverage',{}).values():
                if isinstance(r,dict):
                    for rid,v in r.items():
                        if isinstance(v,dict) and isinstance(v.get('row_sha256'),str):idmap[rid]=v['row_sha256']
    check_identity_crosswalk(decision,frame,hist if isinstance(hist,dict) else {},idmap,e)
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
            'covered':len(covers),'requirement_total':len(rids)}

AUTHORITIES={'EXTERNAL_OBSERVED','OBSERVED','DESCRIPTIVE_MODELED','STRUCTURAL_QUALIFIED','FICTIONAL_WORLD','ACTOR_STATE','HISTORY_EVENT','RIGHTS_METADATA'}
FORBIDDEN_UPGRADES={('DESCRIPTIVE_MODELED','STRUCTURAL_QUALIFIED'),('DESCRIPTIVE_MODELED','OBSERVED'),
                    ('FICTIONAL_WORLD','OBSERVED'),('ACTOR_STATE','OBSERVED'),('FICTIONAL_WORLD','STRUCTURAL_QUALIFIED'),
                    ('ACTOR_STATE','STRUCTURAL_QUALIFIED'),('HISTORY_EVENT','OBSERVED')}
COURT_STATUS={'ACTUAL_PROVED_AT_SCOPE','SOURCE_STATIC_CONSERVED','EXACT_OWNER_HOLD'}
PROJECTIONS=('DESIGN_DECISION.md','COVERAGE_TO_DECISION.tsv','DOWNSTREAM_BUILD_HANDOFF.jsonl',
             'EVIDENCE_AND_FALSIFIER_INDEX.jsonl','GLOBAL_ARCHITECTURE.json','BOUNDARY_TRACE.json')


def check_boundary_court(packet,source_root,errors):
    """T1-T7 must each carry positive, negative and restore (or a named exact hold)."""
    court=packet.get('boundary_court')
    if not isinstance(court,list):errors.append('C:NO_BOUNDARY_COURT');return
    frozen={x['id']:x for x in json.loads((pathlib.Path(source_root)/'02_BOUNDARY_CONTRACTS.json').read_bytes())['boundaries']}
    try:fsha=sha((pathlib.Path(source_root)/'02_BOUNDARY_CONTRACTS.json').read_bytes())
    except OSError:fsha=None
    if packet.get('boundary_contract_sha256')!=fsha:errors.append('C:BOUNDARY_CONTRACT_NOT_PINNED')
    ids=set()
    for row in court:
        if not isinstance(row,dict):errors.append('C:BAD_BOUNDARY_ROW');continue
        tid=row.get('boundary');ids.add(tid)
        base=frozen.get(tid)
        if base is None:errors.append('C:UNKNOWN_BOUNDARY:'+str(tid));continue
        if row.get('contract_name')!=base['name']:errors.append('C:BOUNDARY_REDEFINED:'+str(tid))
        if len(_tokens(row.get('must_preserve_witness'))&_tokens(base['must_preserve']))<3:
            errors.append('C:BOUNDARY_MUST_PRESERVE_NOT_WITNESSED:'+str(tid))
        status=row.get('status')
        if status not in COURT_STATUS:errors.append('C:BAD_BOUNDARY_STATUS:'+str(tid))
        if status=='EXACT_OWNER_HOLD':
            if not good(row.get('owner'),8):errors.append('C:BOUNDARY_HOLD_WITHOUT_OWNER:'+str(tid))
            if not good(row.get('exact_hold'),40):errors.append('C:BOUNDARY_HOLD_NOT_EXACT:'+str(tid))
            continue
        for k in ('positive','negative','restore'):
            t=row.get(k)
            if not isinstance(t,dict):errors.append('C:BOUNDARY_MISSING_'+k.upper()+':'+str(tid));continue
            if not good(t.get('case'),40):errors.append('C:BOUNDARY_'+k.upper()+'_CASE_VACUOUS:'+str(tid))
            if not good(t.get('expected'),20):errors.append('C:BOUNDARY_'+k.upper()+'_EXPECTATION_VACUOUS:'+str(tid))
            if t.get('evidence_grade') not in GRADES:errors.append('C:BOUNDARY_'+k.upper()+'_BAD_GRADE:'+str(tid))
        if not row.get('graph_edge_ids'):errors.append('C:BOUNDARY_NOT_GRAPHLY_CONNECTED:'+str(tid))
    if ids!=set(frozen):errors.append('C:BOUNDARY_UNIVERSE_INCOMPLETE:'+','.join(sorted(set(frozen)-ids)))


def check_typed_graph(packet,errors):
    """One typed source->world->actor graph with no authority or time hole."""
    g=packet.get('typed_graph')
    if not isinstance(g,dict):errors.append('C:NO_TYPED_GRAPH');return
    nodes=g.get('nodes');edges=g.get('edges')
    if not isinstance(nodes,list) or not nodes:errors.append('C:GRAPH_NO_NODES');return
    if not isinstance(edges,list) or not edges:errors.append('C:GRAPH_NO_EDGES');return
    nmap={}
    for n in nodes:
        if not isinstance(n,dict):errors.append('C:GRAPH_BAD_NODE');continue
        nid=n.get('id')
        if nid in nmap:errors.append('C:GRAPH_DUPLICATE_NODE:'+str(nid))
        nmap[nid]=n
        for k in ('kind','owner','time_class'):
            if not good(n.get(k),6):errors.append('C:GRAPH_NODE_HOLE:'+str(nid)+':'+k)
        if n.get('authority') not in AUTHORITIES:errors.append('C:GRAPH_NODE_BAD_AUTHORITY:'+str(nid))
        if not isinstance(n.get('payload_types'),list) or not n['payload_types']:
            errors.append('C:GRAPH_NODE_NO_PAYLOAD:'+str(nid))
    emap={}
    covered=set()
    for x in edges:
        if not isinstance(x,dict):errors.append('C:GRAPH_BAD_EDGE');continue
        eid=x.get('id')
        if eid in emap:errors.append('C:GRAPH_DUPLICATE_EDGE:'+str(eid))
        emap[eid]=x
        a=nmap.get(x.get('from'));b=nmap.get(x.get('to'))
        if a is None or b is None:errors.append('C:GRAPH_ORPHAN_EDGE:'+str(eid));continue
        bd=x.get('boundary');covered.add(bd)
        if bd not in REQUIRED['BOUNDARY']:errors.append('C:GRAPH_BAD_BOUNDARY:'+str(eid))
        pt=x.get('payload_type')
        if pt not in a.get('payload_types',[]) or pt not in b.get('payload_types',[]):
            errors.append('C:GRAPH_TYPE_HOLE:'+str(eid))
        af,at=a.get('authority'),b.get('authority')
        if x.get('authority_from')!=af or x.get('authority_to')!=at:
            errors.append('C:GRAPH_AUTHORITY_HOLE:'+str(eid))
        if (af,at) in FORBIDDEN_UPGRADES and not good(x.get('external_source_warrant'),40):
            errors.append('C:GRAPH_AUTHORITY_UPGRADE_WITHOUT_WARRANT:'+str(eid))
        if not good(x.get('time_class'),6) or x.get('time_class')!=b.get('time_class'):
            errors.append('C:GRAPH_TIME_HOLE:'+str(eid))
        if not good(x.get('negative'),30):errors.append('C:GRAPH_NO_NEGATIVE:'+str(eid))
        if not good(x.get('restore'),30):errors.append('C:GRAPH_NO_RESTORE:'+str(eid))
        if not good(x.get('first_consumer'),10):errors.append('C:GRAPH_NO_CONSUMER:'+str(eid))
        if x.get('evidence_grade') not in GRADES:errors.append('C:GRAPH_BAD_EVIDENCE_GRADE:'+str(eid))
    for tid in REQUIRED['BOUNDARY']:
        if tid not in covered:errors.append('C:GRAPH_BOUNDARY_UNROUTED:'+tid)
    adj={}
    for x in edges:
        if isinstance(x,dict):adj.setdefault(x.get('from'),set()).add(x.get('to'))
    start=[n for n,v in nmap.items() if v.get('authority')=='OBSERVED']
    goal={n for n,v in nmap.items() if v.get('authority')=='ACTOR_STATE'}
    if not start:errors.append('C:GRAPH_NO_OBSERVED_SOURCE_NODE')
    if not goal:errors.append('C:GRAPH_NO_ACTOR_TERMINAL_NODE')
    seen=set(start);stack=list(start)
    while stack:
        cur=stack.pop()
        for nxt in adj.get(cur,()):
            if nxt not in seen:seen.add(nxt);stack.append(nxt)
    if goal and not (seen&goal):errors.append('C:GRAPH_SOURCE_TO_ACTOR_DISCONNECTED')


def check_projections(packet,evidence_root,errors):
    """The six deterministic first-reader projections must exist and match bytes."""
    man=packet.get('projection_manifest')
    if not isinstance(man,dict):errors.append('C:NO_BUILDER_PROJECTIONS');return
    if set(man.get('files',{}))!=set(PROJECTIONS):errors.append('C:PROJECTION_SET_INCOMPLETE')
    if man.get('digest')!=digest(man.get('files',{})):errors.append('C:PROJECTION_MANIFEST_NOT_SELF_CONSISTENT')
    root=pathlib.Path(evidence_root).resolve()
    for name,want in (man.get('files') or {}).items():
        p=(root/name).resolve()
        if not p.is_relative_to(root) or not p.is_file():errors.append('C:PROJECTION_MISSING:'+name);continue
        if sha(p.read_bytes())!=want:errors.append('C:PROJECTION_BYTES_CHANGED:'+name)


def check_C(packet,evidence_root,source_root,anchors=None):
    e=[]
    if not isinstance(packet,dict) or packet.get('schema')!=SCHEMA or packet.get('stage')!='INDEPENDENT_C':
        return {'status':'RED','errors':['C:BAD_SCHEMA']}
    decision=load(evidence_root,packet.get('integrated_decision'),e,'C:DECISION')
    if decision is not None:
        verdict=check_decision(decision,evidence_root,source_root,anchors)
        if verdict['status']=='RED':e.extend('C:DEFECTIVE_DECISION:'+x for x in verdict['errors'])
        if packet.get('integrated_decision_sha256')!=digest(decision):e.append('C:DECISION_NOT_PINNED')
        if packet.get('first_consumer')!=decision.get('first_real_consumer'):
            e.append('C:CONSUMER_CHANGED')
    for k in ('independent_reverse_walk_of_whole_frame','strongest_choice_reversing_objection',
              'scientific_and_owner_boundary','actual_first_consumer_assessment','historical_no_loss_assessment'):
        if not good(packet.get(k),60):e.append('C:INSUFFICIENT_'+k)
    cards=packet.get('builder_cards')
    if not isinstance(cards,list) or len(cards)!=2 or {c.get('domain') for c in cards if isinstance(c,dict)}!={'CURRENT_FIRST_CONSUMER','FUTURE_NONPRECLUSION'}:
        e.append('C:REQUIRES_PRESENT_AND_FUTURE_BUILDER_CARDS')
    else:
        from r7_stage import check_builder
        for card in cards:e.extend('C:BUILDER:'+v for v in check_builder(card,source_root,evidence_root))
        present=next(c for c in cards if c['domain']=='CURRENT_FIRST_CONSUMER')
        if packet.get('verdict')=='C_CONDITIONALLY_ADMIT_DESIGN' and present.get('grade')=='EXACT_BUILDER_HOLD':
            e.append('C:ADMIT_WITHOUT_CURRENT_BUILDER')
    if packet.get('reviewer_relationship')!='DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION':
        e.append('C:SELF_CERTIFIED_INDEPENDENCE')
    if packet.get('choice_reversing_objection_survives') is not False and packet.get('verdict')=='C_CONDITIONALLY_ADMIT_DESIGN':
        e.append('C:ACCEPTS_SURVIVING_REVERSER')
    if packet.get('verdict') not in ('C_CONDITIONALLY_ADMIT_DESIGN','C_HOLD_EXACT'):
        e.append('C:FALSE_C_GRADE')
    if packet.get('original_source_granted_by_local_check') is not False or packet.get('owner_granted_by_local_check') is not False:
        e.append('C:FALSE_AUTHORITY')
    check_boundary_court(packet,source_root,e)
    check_typed_graph(packet,e)
    check_projections(packet,evidence_root,e)
    if packet.get('claims_protected_h1') is not False:e.append('C:FALSE_PROTECTED_H1')
    return {'status':'RED' if e else 'PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED','errors':sorted(set(e))}

def check(stage,packet,evidence_root,source_root=None,anchors=None):
    if stage=='FRAME':return check_frame(packet,evidence_root,source_root,anchors)
    if stage=='DECISION':return check_decision(packet,evidence_root,source_root,anchors)
    if stage=='C_INTEGRATED':return check_C(packet,evidence_root,source_root,anchors)
    return {'status':'RED','errors':['ACTIVE_STAGE_UNKNOWN']}

def main():
    ap=argparse.ArgumentParser(description='Active ANVIL integral workflow, NOT autonomous accreditation')
    ap.add_argument('stage',choices=['FRAME','DECISION','C_INTEGRATED'])
    ap.add_argument('packet');ap.add_argument('--evidence-root',required=True);ap.add_argument('--source-root',required=True)
    ap.add_argument('--git-repo');ap.add_argument('--zip');ap.add_argument('--zip-sha256');ap.add_argument('--commits')
    arg=ap.parse_args()
    from r7_source_inventory import Anchors
    anchors=Anchors(git_repo=arg.git_repo,zip_path=arg.zip,zip_sha256=arg.zip_sha256,
                    commits=json.loads(arg.commits) if arg.commits else None) if (arg.git_repo or arg.zip) else None
    try:out=check(arg.stage,json.loads(pathlib.Path(arg.packet).read_text()),arg.evidence_root,arg.source_root,anchors)
    except (OSError,ValueError,TypeError,KeyError) as exc:out={'status':'RED','errors':['UNHANDLED_MALFORMED_PACKET:'+repr(exc)]}
    print(json.dumps(out,indent=2));return 2 if out['status']=='RED' else 0
if __name__=='__main__':sys.exit(main())
