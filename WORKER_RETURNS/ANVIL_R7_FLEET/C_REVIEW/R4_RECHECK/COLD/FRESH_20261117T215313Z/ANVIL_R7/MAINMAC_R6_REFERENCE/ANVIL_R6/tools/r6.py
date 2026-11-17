#!/usr/bin/env python3
"""ANVIL R6 documentary architecture-selection controls.

Exact structural/typed guards only. Nothing herein authenticates GitHub receipts,
scientific correctness, independent identity, real native use, or protected CAS.
Runtime: Python 3 standard library only.
"""
from __future__ import annotations
import argparse, copy, csv, hashlib, io, json, math, pathlib, re, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
POL=json.loads((ROOT/'contracts/policy.json').read_text())
SRC=json.loads((ROOT/'contracts/source_registry.json').read_text())
H64=re.compile(r'^[0-9a-f]{64}$'); H40=re.compile(r'^[0-9a-f]{40}$')
BADWORDS=('to be specified','tbd','todo','unknown current','future engineer','placeholder','insert here','not decided','someone')

def canonical(obj):return json.dumps(obj,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)
def digest(obj):return hashlib.sha256(canonical(obj).encode()).hexdigest()
def filehash(path):return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
def load(path):return json.loads(pathlib.Path(path).read_text())
def fail(code,detail=''):return f'{code}'+(':'+str(detail) if detail!='' else '')
def nonempty(x):return isinstance(x,str) and bool(x.strip())
def realtext(x):return nonempty(x) and len(x.strip())>=8 and not any(p in x.lower() for p in BADWORDS)
def valid_sh(x):return isinstance(x,str) and bool(H40.fullmatch(x))
def valid_evidence(eid, evidence, grade=None, verified=False):
    if not eid or eid not in evidence:return False
    x=evidence[eid]
    if not isinstance(x,dict) or x.get('grade') not in POL['evidence_grades']:return False
    if grade and x['grade'] not in grade:return False
    if verified and not (x.get('independent_checked') is True and x.get('raw_receipt_ref') and valid_sh(x.get('code_head'))):return False
    return realtext(x.get('description','')) and nonempty(x.get('source_ref'))

def validate_source_claim(c):
    errs=[]; axes=POL['source_claim_facets']
    for k,choices in axes.items():
        if c.get(k) not in choices:errs.append('CLAIM_BAD_'+k)
    if c.get('claim_kind') not in POL['source_claim_types']:errs.append('CLAIM_BAD_KIND')
    for k in ('release','instrument','country','wave','question','source_ref','evidence_ref','source_unit','target_unit'):
        if not nonempty(c.get(k)):errs.append('CLAIM_MISSING_'+k)
    kind=c.get('claim_kind')
    if kind=='RESPONDENT_ORIGINAL_VALUE':
        if c.get('asked')!='YES' or c.get('released')!='YES' or c.get('observation')!='VALUE' or c.get('eligibility')!='ELIGIBLE':errs.append('UNOBSERVED_TO_SUBSTANTIVE_SOURCE_VALUE')
        if c.get('source_status')!='DOCUMENTED_RESPONDENT_RESPONSE':errs.append('NON_SOURCE_TO_ORIGINAL_VALUE')
        if not nonempty(c.get('record_value_ref')):errs.append('SOURCE_VALUE_WITHOUT_SELECTED_RESPONDENT_RECORD')
        if c.get('source_unit')!=c.get('target_unit') or c.get('unit')!=c.get('target_unit'):errs.append('SOURCE_TARGET_UNIT_COLLAPSE')
        if c.get('attribution')!=c.get('target_attribution'):errs.append('INTERVIEWER_OR_ADMIN_TO_SELF')
        if not nonempty(c.get('original_code_ref')):errs.append('SOURCE_VALUE_WITHOUT_ORIGINAL_CODE')
    if kind=='INSTRUMENT_METADATA':
        if c.get('target_is_respondent_claim') is True:errs.append('METADATA_FALSE_RESPONDENT_CLAIM')
        if c.get('source_status')=='MODEL_OR_FICTION':errs.append('FABRICATED_INSTRUMENT_DESIGN')
    if kind in {'QUALIFIED_DESCRIPTIVE','EXTERNAL_STRUCTURAL'}:
        if not nonempty(c.get('qualification_authority_ref')):errs.append('UNQUALIFIED_SCIENCE_CLAIM')
    if kind=='EXTERNAL_STRUCTURAL' and c.get('source_status')=='MODEL_OR_FICTION':errs.append('MODEL_AS_STRUCTURAL_SOURCE')
    if kind=='INTERPRETIVE_HYPOTHESIS' and c.get('stated_as_design_intent') is True and not nonempty(c.get('design_intent_primary_evidence')):errs.append('INTERPRETATION_AS_DESIGN_INTENT')
    if c.get('claim_wave_comparable'):
        if c.get('translation')!='COMPARABLE_ISSUED' or not nonempty(c.get('equivalence_authority_ref')):errs.append('UNLICENSED_WAVE_SEMANTIC_EQUIVALENCE')
    if c.get('claim_no_effect_from_absence') and (c.get('observation')!='VALUE' or c.get('asked')!='YES'):errs.append('MISSING_TO_NO_EFFECT')
    if c.get('source_status')=='MODEL_OR_FICTION' and kind in {'RESPONDENT_ORIGINAL_VALUE','INSTRUMENT_METADATA','EXTERNAL_STRUCTURAL'}:errs.append('MODEL_OR_FICTION_PROMOTED')
    if c.get('target_is_respondent_claim') and kind=='INSTRUMENT_METADATA':errs.append('INSTRUMENT_METADATA_RESPONDENT_MERGE')
    return sorted(set(errs))

def validate_graph(spine):
    errs=[]; nodes=spine.get('nodes',[]); edges=spine.get('edges',[])
    by={x.get('id'):x for x in nodes if isinstance(x,dict)}
    if len(by)!=len(nodes) or not nodes:errs.append('GRAPH_DUPLICATE_OR_EMPTY_NODE_IDS')
    if any(x.get('domain') not in POL['domains'] for x in nodes if isinstance(x,dict)):errs.append('GRAPH_BAD_DOMAIN')
    emap={}
    allowed={tuple(x) for x in POL['transitions']}
    for i,e in enumerate(edges):
        if not isinstance(e,dict):errs.append('GRAPH_NONOBJECT_EDGE');continue
        eid=e.get('id'); f=e.get('from');t=e.get('to')
        if eid in emap or not nonempty(eid):errs.append('GRAPH_DUPLICATE_EDGE_ID')
        emap[eid]=e
        if f not in by or t not in by:errs.append('GRAPH_MISSING_ENDPOINT');continue
        key=(by[f].get('domain'),by[t].get('domain'),e.get('transition'),e.get('authority'))
        if key not in allowed:errs.append('GRAPH_FORBIDDEN_TRANSITION:'+str(eid))
        for field in ('payload','negative','clock','owner','evidence_ref'):
            if not realtext(e.get(field)):errs.append('GRAPH_EDGE_MISSING_'+field+':'+str(eid))
        for extra in ('grade','shadow_authority','alternate_clock','evidence_grade'):
            if extra in e:errs.append('GRAPH_CONTRADICTORY_SECOND_VOCABULARY:'+extra)
    if not emap:errs.append('GRAPH_NO_EDGES')
    routes=spine.get('routes',{})
    for rid,(start,end) in POL['required_named_routes'].items():
        r=routes.get(rid)
        if not isinstance(r,dict):errs.append('ROUTE_MISSING:'+rid);continue
        path=r.get('edge_ids')
        if not isinstance(path,list) or not path:errs.append('ROUTE_EMPTY:'+rid);continue
        if any(eid not in emap for eid in path):errs.append('ROUTE_UNKNOWN_EDGE:'+rid);continue
        first=emap[path[0]];last=emap[path[-1]]
        if first.get('from') not in by or last.get('to') not in by:continue
        if by[first['from']].get('domain')!=start or by[last['to']].get('domain')!=end:errs.append('ROUTE_DOMAIN_SPOOF:'+rid)
        for j in range(1,len(path)):
            if emap[path[j-1]].get('to')!=emap[path[j]].get('from'):errs.append('ROUTE_DISCONNECTED:'+rid)
        for field in ('first_consumer','source_or_world_clock','preserved_information','legitimate_owner','negative_or_hold'):
            if not realtext(r.get(field)):errs.append('ROUTE_MISSING_'+field+':'+rid)
        if r.get('proof_grade') not in ('SOURCE_STATIC_NONPRECLUSION','EXECUTED_FIRST_EFFECT','OWNER_HELD_WITH_FEASIBLE_EXTENSION'):errs.append('ROUTE_BAD_PROOF_GRADE:'+rid)
        if r.get('proof_grade')=='OWNER_HELD_WITH_FEASIBLE_EXTENSION':
            if not realtext(r.get('extension_abi')):errs.append('ROUTE_HELD_WITHOUT_EXTENSIBLE_ABI:'+rid)
            if spine.get('claimed_future_executed') is True:errs.append('ROUTE_HELD_BUT_EXECUTED_CLAIM:'+rid)
        if r.get('proof_grade')=='EXECUTED_FIRST_EFFECT' and not nonempty(r.get('execution_evidence_id')):errs.append('ROUTE_EXECUTED_WITHOUT_EVIDENCE:'+rid)
    return sorted(set(errs))

def payload_plan(plan):return {k:v for k,v in plan.items() if k!='freeze_digest'}
def planhash(plan):return digest(payload_plan(plan))
def plan_errors(plan, parent=None):
    e=[]
    if plan.get('schema')!='ANVIL_R6_PLAN_1':e.append('BAD_PLAN_SCHEMA')
    if plan.get('scope') not in POL['scope_enum']:e.append('BAD_SCOPE')
    if plan.get('policy_digest')!=filehash(ROOT/'contracts/policy.json'):e.append('PLAN_POLICY_PIN_MISMATCH')
    if plan.get('freeze_digest')!=planhash(plan):e.append('FREEZE_HASH_MISSING_OR_STALE')
    if plan.get('phase')!='BEFORE_FIRST_RESULT':e.append('PLAN_NOT_PRERESULT')
    if not isinstance(plan.get('version'),int) or plan['version']<1:e.append('BAD_PLAN_VERSION')
    if not valid_sh(plan.get('A0_head')) or not valid_sh(plan.get('B0_head')):e.append('PLAN_MISSING_FROZEN_A_B_HEAD')
    cells=plan.get('cells')
    if not isinstance(cells,list) or not cells:e.append('NO_MATERIAL_CELLS');cells=[]
    seen=set();dims=set();workloads=set()
    for c in cells:
        if not isinstance(c,dict):e.append('BAD_CELL');continue
        cid=c.get('id'); key=(c.get('workload'),c.get('dimension'),c.get('metric'))
        if cid in seen:e.append('DUPLICATE_CELL_ID')
        seen.add(cid)
        if c.get('workload') not in POL['workloads']:e.append('BAD_WORKLOAD')
        if c.get('metric') not in POL['physical_dimensions'].get(c.get('dimension'),[]):e.append('METRIC_DIMENSION_MISMATCH')
        if c.get('decision_id') is None:e.append('CELL_NO_DECISION_ID')
        for k in ('selection_reverser_A','selection_reverser_B','input_sha','runner_identity','negative_restore','first_consumer','source_grade'):
            if not realtext(c.get(k)):e.append('CELL_MISSING_'+k+':'+str(cid))
        dims.add((c.get('workload'),c.get('dimension'),c.get('metric')));workloads.add(c.get('workload'))
    exclusions=plan.get('exclusions',[])
    if not isinstance(exclusions,list):e.append('BAD_EXCLUSIONS');exclusions=[]
    exw=set()
    for x in exclusions:
        if not isinstance(x,dict):e.append('BAD_EXCLUSION');continue
        w=x.get('workload');exw.add(w)
        if w not in POL['workloads']:e.append('UNKNOWN_EXCLUDED_CASE')
        for k in ('specific_nonmateriality','first_consumer_consequence','B_objection_or_concurrence','owner','H0_source_ref'):
            if not realtext(x.get(k)):e.append('EXCLUSION_UNCHALLENGED_'+k+':'+str(w))
        if x.get('disposition') not in ('CHALLENGED_PENDING_C','B_CONCURS_PENDING_C'):e.append('EXCLUSION_SELF_ACCEPTANCE')
    if workloads|exw != set(POL['workloads']):e.append('UNACCOUNTED_WORKLOAD_SHAPES')
    if len(exw)!=len(exclusions):e.append('DUPLICATE_EXCLUSION')
    if workloads & exw:e.append('WORKLOAD_INCLUDED_AND_EXCLUDED')
    if parent is not None:
        if plan.get('version')!=parent.get('version',-1)+1:e.append('AMENDMENT_BAD_VERSION')
        if plan.get('parent_digest')!=parent.get('freeze_digest'):e.append('AMENDMENT_WRONG_PARENT')
        if plan.get('first_results_seen') is not False:e.append('POSTRESULT_AMENDMENT_NOT_LAWFUL_IN_PLACE')
        if not isinstance(plan.get('discovery'),dict):e.append('NO_B_DISCOVERY')
        else:
            d=plan['discovery']
            for k in ('B_frozen_objection_sha','source_finding_ref','new_discriminator','why_original_frame_incomplete','controller_pre_result_freeze_ref'):
                if not realtext(d.get(k)):e.append('UNSUPPORTED_FRAME_AMENDMENT_'+k)
            if d.get('origin')!='INDEPENDENT_B_PRE_RESULT':e.append('NOT_INDEPENDENT_B_DISCOVERY')
        oldids={c.get('id') for c in parent.get('cells',[])}
        if not oldids.issubset({c.get('id') for c in cells}):e.append('AMENDMENT_DROPPED_OLD_CELL')
    elif plan.get('version')!=1:e.append('AMENDMENT_PARENT_REQUIRED')
    return sorted(set(e))

def comparison(plan, data, parent=None):
    errors=plan_errors(plan,parent)
    if data.get('schema')!='ANVIL_R6_MEASUREMENTS_1':errors.append('BAD_MEASUREMENT_SCHEMA')
    if data.get('freeze_digest')!=plan.get('freeze_digest'):errors.append('MEASUREMENT_FREEZE_MISMATCH')
    rows=data.get('results',[]); evidence=data.get('evidence',{})
    if not isinstance(rows,list):rows=[];errors.append('BAD_MEASUREMENT_ROWS')
    if not isinstance(evidence,dict):evidence={};errors.append('BAD_EVIDENCE_REGISTRY')
    by={r.get('cell_id'):r for r in rows if isinstance(r,dict)}
    if len(rows)!=len(by):errors.append('DUPLICATE_OR_INVALID_MEASUREMENT_ID')
    all_comparable=True; dominance={'A':0,'B':0,'OVERLAP':0}; decisive_unknown=[]; measured_ids=[]
    for c in plan.get('cells',[]):
        cid=c.get('id'); r=by.get(cid)
        if r is None:errors.append('MISSING_FROZEN_CELL_RESULT:'+str(cid));all_comparable=False;decisive_unknown.append(cid);continue
        if r.get('fixture_hash')!=c.get('input_sha') or r.get('runner_identity')!=c.get('runner_identity'):errors.append('UNMATCHED_FIXTURE_OR_RUNNER:'+str(cid))
        pairs=[]
        for side in ('A','B'):
            v=r.get(side,{})
            if not isinstance(v,dict):v={}
            status=v.get('status')
            if status not in ('MEASURED','MODELED','UNRUN_HELD'):errors.append('BAD_MEASUREMENT_STATUS:'+str(cid))
            if status!='MEASURED':all_comparable=False;decisive_unknown.append(cid)
            if status=='MEASURED':
                low=v.get('low');high=v.get('high')
                if not (type(low) in (float,int) and type(high) in (float,int) and math.isfinite(low) and math.isfinite(high) and 0<=low<=high):errors.append('BAD_INTERVAL:'+str(cid))
                if not valid_evidence(v.get('evidence_id'),evidence,{'S2_SOURCEFREE_EXECUTED','S2_NATIVE_EXECUTED'},verified=True):errors.append('UNAUTHENTICATED_MEASUREMENT_METADATA:'+str(cid)+':'+side)
            pairs.append(v)
        a,b=pairs
        if a.get('status')=='MEASURED' and b.get('status')=='MEASURED' and all(isinstance(v.get('low'),(int,float)) and isinstance(v.get('high'),(int,float)) for v in (a,b)):
            measured_ids.append(cid)
            if a['high']<b['low']:dominance['A']+=1
            elif b['high']<a['low']:dominance['B']+=1
            else:dominance['OVERLAP']+=1;decisive_unknown.append(cid)
    for x in by:
        if x not in {c.get('id') for c in plan.get('cells',[])}:errors.append('UNFROZEN_MEASUREMENT_SUBMITTED:'+str(x))
    # Each coverage class is separately challenged; a fully excluded shape can never give a design-wide winning comparison.
    mandatory=set(map(tuple,POL['minimal_design_wide_matrix']))
    actual={(c.get('workload'),c.get('dimension'),c.get('metric')) for c in plan.get('cells',[])}
    if not mandatory.issubset(actual):missing=mandatory-actual;errors.append('MANDATORY_DIMENSION_GAPS:'+','.join(sorted('/'.join(x) for x in missing)))
    if errors:return {'schema':'ANVIL_R6_COMPARISON_RESULT_1','status':'RED','errors':sorted(set(errors)),'dominance':dominance}
    if plan.get('exclusions'):status='SCOPE_EXCLUSIONS_REQUIRE_INDEPENDENT_C'
    elif not all_comparable:status='MISSING_MATCHED_DECISIVE_EVIDENCE'
    elif dominance['OVERLAP']:status='PARETO_OR_UNRESOLVED'
    elif dominance['A'] and dominance['B']:status='TRADEOFF_OWNER_DECISION'
    elif dominance['A']:status='A_ADVANTAGE_AT_COMPLETE_SCOPE'
    elif dominance['B']:status='B_ADVANTAGE_AT_COMPLETE_SCOPE'
    else:status='NO_DISCRIMINATING_ADVANTAGE'
    # This helper never selects a final architecture; C must verify raw receipts and scientific/economic scope.
    return {'schema':'ANVIL_R6_COMPARISON_RESULT_1','status':status,'errors':[], 'dominance':dominance,'evaluated_cell_ids':sorted(measured_ids),'unresolved_cell_ids':sorted(set(decisive_unknown)),'freeze_digest':plan['freeze_digest'],'comparison_input_digest':digest(data),'unverified_scope_notes':'No external receipt/host authentication is performed by this Python helper'}

def validate_handoff(h):
    e=[]
    if h.get('implementation_status') not in ('READY_FOR_IMPLEMENTER','OWNER_HELD','PROSPECTIVE_INTERFACE'):e.append('HANDOFF_BAD_STATUS')
    for k in ('id','owner','input_abi','output_abi','negative','currentness','rights_grade','first_effect','dependency','test_command','first_consumer'):
        if not realtext(h.get(k)):e.append('HANDOFF_MISSING_'+k)
    status=h.get('implementation_status')
    if status=='READY_FOR_IMPLEMENTER':
        for k in ('producer_symbol','consumer_symbol','source_cut','test_command'):
            if not realtext(h.get(k)):e.append('READY_BUT_PLACEHOLDER_'+k)
        if not valid_sh(h.get('source_cut')):e.append('READY_UNPINNED_CODE')
        if '::' not in h.get('producer_symbol','') or '::' not in h.get('consumer_symbol',''):e.append('READY_WITHOUT_RESOLVABLE_SYMBOL')
        if h.get('first_consumer_grade') not in ('EXACT_STATIC_IMPLEMENTATION_ABI','EXECUTED_FIRST_CONSUMER'):e.append('READY_WITHOUT_QUALIFIED_CONSUMER')
    else:
        if not realtext(h.get('held_reason')):e.append('HELD_WITHOUT_REASON')
    return sorted(set(e))

def validate_spine(spine,plan,measure,compare_result):
    e=[]
    if spine.get('schema')!='ANVIL_R6_SPINE_1':e.append('SPINE_BAD_SCHEMA')
    if spine.get('policy_digest')!=filehash(ROOT/'contracts/policy.json'):e.append('SPINE_POLICY_MISMATCH')
    if spine.get('source_registry_digest')!=filehash(ROOT/'contracts/source_registry.json'):e.append('SPINE_SOURCE_REGISTRY_MISMATCH')
    if spine.get('freeze_digest')!=plan.get('freeze_digest'):e.append('SPINE_FREEZE_MISMATCH')
    if spine.get('comparison_digest')!=digest(compare_result):e.append('SPINE_COMPARISON_DIGEST_MISMATCH')
    if spine.get('scope')!=plan.get('scope'):e.append('SPINE_SCOPE_MISMATCH')
    if spine.get('author_proposed_grade') not in POL['decision_grades']:e.append('SPINE_BAD_GRADE')
    if spine.get('builder_cold_start')!='PENDING_INDEPENDENT_C':e.append('AUTHOR_FABRICATED_FUTURE_BUILDER')
    if spine.get('selected_candidate') not in ('A','B','UNDECIDED'):e.append('SPINE_INVALID_WINNER')
    evidence=spine.get('evidence',{})
    if not isinstance(evidence,dict):evidence={};e.append('SPINE_NO_EVIDENCE_REGISTRY')
    if spine.get('historical_inheritance',{}).get('K3_not_adopted_count')!=26 or spine.get('historical_inheritance',{}).get('P4R_held_count')!=14 or spine.get('historical_inheritance',{}).get('families')!=29:e.append('K3_FUNCTION_CONSERVATION_MISMATCH')
    expected=sum(SRC['mandatory'].values(),[])
    if spine.get('historical_inheritance',{}).get('exact_ids')!=expected:e.append('118_IDENTITY_CONSERVATION_MISMATCH')
    for i,c in enumerate(spine.get('claims',[])):
        e.extend(f'claim[{i}]/{q}' for q in validate_source_claim(c))
    e.extend(validate_graph(spine))
    for i,h in enumerate(spine.get('handoffs',[])):
        e.extend(f'handoff[{i}]/{q}' for q in validate_handoff(h))
    material=set(x['id'] for x in plan.get('cells',[])); decision_ids=set();used_cells=set()
    for d in spine.get('physical_decisions',[]):
        if d.get('id') in decision_ids:e.append('PHYSICAL_DUPLICATE_DECISION')
        decision_ids.add(d.get('id'))
        if d.get('selected') not in ('A','B','HOLD'):e.append('PHYSICAL_BAD_SELECTION')
        refs=d.get('cell_ids',[])
        if not isinstance(refs,list) or not refs:e.append('PHYSICAL_WITHOUT_COMPARISON_REF:'+str(d.get('id')))
        for x in refs:
            if x not in material:e.append('PHYSICAL_UNFROZEN_EVIDENCE:'+str(d.get('id')))
            else:
                cell=next(c for c in plan['cells'] if c['id']==x)
                if cell.get('decision_id')!=d.get('id') and d.get('shared_evidence_scope')!='DERIVED_WITH_EXPLICIT_DEPENDENCY':e.append('PHYSICAL_BORROWED_UNRELATED_COMPARISON:'+str(d.get('id')))
                if cell.get('decision_id')!=d.get('id') and not nonempty(d.get('qualified_source_decision_id')):e.append('PHYSICAL_SHARED_EVIDENCE_WITHOUT_DEPENDENCY_ID:'+str(d.get('id')))
            used_cells.add(x)
        if d.get('selected') in ('A','B') and d.get('selected')!=spine.get('selected_candidate'):e.append('PHYSICAL_CONTRADICTS_GLOBAL_WINNER')
        if not realtext(d.get('actual_first_consumer')):e.append('PHYSICAL_NO_CONSUMER')
        if d.get('first_consumer_node_id') not in {n.get('id') for n in spine.get('nodes',[])}:e.append('PHYSICAL_CONSUMER_NOT_IN_GLOBAL_GRAPH')
        if not realtext(d.get('dependency_effect')):e.append('PHYSICAL_NO_DEPENDENCY_ANALYSIS')
        if d.get('shared_evidence_scope') not in ('DIRECTLY_MEASURED','DERIVED_WITH_EXPLICIT_DEPENDENCY','OWNER_HELD'):e.append('PHYSICAL_UNJUSTIFIED_SHARED_EVIDENCE')
        for eid in d.get('hard_veto_evidence_ids',[]):
            if not valid_evidence(eid,evidence):e.append('PHYSICAL_VETO_ORPHAN_EVIDENCE')
    if not spine.get('physical_decisions'):e.append('NO_PHYSICAL_DECISIONS')
    if not set(x.get('decision_id') for x in plan.get('cells',[])).issubset(decision_ids):e.append('FROZEN_DECISIONS_MISSING_FROM_SPINE')
    if len(used_cells)<len(material):e.append('FROZEN_CELLS_WITHOUT_A_DECISION')
    for i,p in enumerate(spine.get('product_deltas',[])):
        if not valid_evidence(p.get('before_evidence'),evidence):e.append('DELTA_UNPROVED_BEFORE:'+str(i))
        if not valid_evidence(p.get('after_evidence'),evidence):e.append('DELTA_UNPROVED_AFTER:'+str(i))
        if p.get('grade') not in POL['author_delta_grades']:e.append('DELTA_BAD_AUTHOR_GRADE')
        if p.get('grade')!='NO_NEW_PRODUCT_ADVANCE' and not realtext(p.get('changed_first_consumer_effect')):e.append('DELTA_NO_REAL_EFFECT')
    ready=spine.get('author_proposed_grade')=='DESIGN_READY_SCOPED'
    if ready:
        expected_status='A_ADVANTAGE_AT_COMPLETE_SCOPE' if spine.get('selected_candidate')=='A' else 'B_ADVANTAGE_AT_COMPLETE_SCOPE'
        if compare_result.get('status')!=expected_status:e.append('READY_NOT_SUPPORTED_BY_COMPLETE_COMPARISON')
        if not spine.get('semantic_witnesses',{}).get('W-R') or not spine.get('semantic_witnesses',{}).get('W-J') or not spine.get('semantic_witnesses',{}).get('W-X'):e.append('READY_WITHOUT_REQUIRED_SEMANTIC_WITNESSES')
        for wid,eid in spine.get('semantic_witnesses',{}).items():
            if not valid_evidence(eid,evidence,verified=True):e.append('READY_UNVERIFIED_SEMANTIC_WITNESS:'+wid)
        if not any(h.get('implementation_status')=='READY_FOR_IMPLEMENTER' for h in spine.get('handoffs',[])):e.append('READY_WITH_NO_REAL_FIRST_CONSUMER_HANDOFF')
        if any(d.get('selected')=='HOLD' for d in spine.get('physical_decisions',[])):e.append('READY_WITH_HELD_MATERIAL_DECISION')
    if spine.get('author_proposed_grade')=='CONDITIONAL_CANDIDATE' and not realtext(spine.get('exact_conditional_reverser')):e.append('CONDITIONAL_WITH_NO_REVERSER')
    if spine.get('author_proposed_grade')=='DECISION_BLOCKED_EXACT' and not realtext(spine.get('exact_decision_blocker')):e.append('BLOCKED_WITHOUT_EXACT_BLOCKER')
    if spine.get('author_proposed_grade')=='DESIGN_READY_SCOPED' and spine.get('selected_candidate')=='UNDECIDED':e.append('READY_NO_WINNER')
    return sorted(set(e))

def check_stage(stage, x):
    errors=[]
    if x.get('schema')!='ANVIL_R6_STAGE_1' or x.get('stage')!=stage:errors.append('STAGE_SCHEMA_OR_ID')
    if x.get('verdict') not in POL['stage_verdicts'][stage]:errors.append('STAGE_INVALID_VERDICT')
    if not realtext(x.get('source_cut')):errors.append('STAGE_NO_SOURCE_CUT')
    if not realtext(x.get('owner')):errors.append('STAGE_NO_OWNER')
    if stage in ('A0','B0') and not x.get('blind_to_other') is True:errors.append('NOT_BLIND_P0')
    if stage=='B0':
        for k in ('credible_rival','frame_challenge','downstream_consumer','material_discriminator'):
            if not realtext(x.get(k)):errors.append('B_MISSING_'+k)
    if stage in ('A1','B1'):
        if not valid_sh(x.get('opponent_frozen_head')):errors.append('P1_NO_FROZEN_OPPONENT')
    if stage=='P15':
        if not nonempty(x.get('plan_digest')) or not H64.fullmatch(x['plan_digest']):errors.append('P15_NO_FROZEN_PLAN')
        if x.get('verdict')=='P15_DECISIVE_SCOPED' and x.get('comparison_status') not in ('A_ADVANTAGE_AT_COMPLETE_SCOPE','B_ADVANTAGE_AT_COMPLETE_SCOPE'):errors.append('P15_FALSE_DECISIVE_VERDICT')
        if x.get('verdict')=='P15_DECISIVE_SCOPED' and not realtext(x.get('matched_runner_receipt_ref')):errors.append('P15_NO_RUNNER_RECEIPT')
    if stage=='P2':
        if x.get('builder_grade')!='PENDING_INDEPENDENT_C':errors.append('P2_CLAIMS_INDEPENDENT_FUTURE')
        if not H64.fullmatch(str(x.get('spine_sha256'))):errors.append('P2_MISSING_FROZEN_SPINE')
    if stage=='C':
        if x.get('builder_grade') not in POL['builder_grades']:errors.append('C_UNKNOWN_BUILDER_GRADE')
        if x.get('future_builder_grade') not in POL['builder_grades']:errors.append('C_UNKNOWN_FUTURE_BUILDER_GRADE')
        if not realtext(x.get('current_handoff_id')) or not realtext(x.get('future_handoff_id')) or x.get('current_handoff_id')==x.get('future_handoff_id'):errors.append('C_NOT_TWO_DISTINCT_BUILDER_CARDS')
        if not valid_sh(x.get('P2_frozen_head')):errors.append('C_UNPINNED_P2')
        if x.get('verdict')=='C_ACCEPT_SCOPED' and x.get('builder_grade')=='EXACT_BUILDER_HOLD':errors.append('C_ACCEPT_WITH_HELD_BUILDER')
        if x.get('verdict')=='C_ACCEPT_SCOPED' and (not x.get('raw_comparison_verified') or not x.get('semantic_paths_verified') or not x.get('first_consumer_scope_verified')):errors.append('C_ACCEPT_WITHOUT_SUBSTANCE')
        if x.get('verdict')=='C_ACCEPT_DOCUMENTARY_HOLD' and not realtext(x.get('exact_hold')):errors.append('C_HOLD_NOT_EXACT')
    if stage=='H1':
        c=x.get('C_receipt',{})
        if c.get('builder_grade') not in POL['builder_grades']:errors.append('H1_UNKNOWN_BUILDER_GRADE')
        if c.get('future_builder_grade') not in POL['builder_grades']:errors.append('H1_UNKNOWN_FUTURE_BUILDER_GRADE')
        if c.get('verdict') not in POL['stage_verdicts']['C']:errors.append('H1_UNKNOWN_C_VERDICT')
        if c.get('P2_head')!=x.get('P2_head'):errors.append('H1_C_RECEIPT_WRONG_P2')
        if not valid_sh(c.get('head')):errors.append('H1_UNPINNED_C_RECEIPT')
        if not valid_sh(x.get('P2_head')):errors.append('H1_UNPINNED_P2')
        if x.get('verdict') in ('H1_RECEIVED_SCOPED','H1_RECEIVED_CONDITIONAL'):
            if x.get('owner_authority')!='VERIFIED_COMPETENT_OWNER':errors.append('H1_NOT_COMPETENT_OWNER')
            if x.get('protected_received_YN')!='YES' or x.get('paired_progress_CAS')!='AUTHENTICATED_CAS_RECEIVED':errors.append('H1_NOT_ACTUALLY_RECEIVED')
            if not nonempty(x.get('CAS_commit_sha')) or not valid_sh(x['CAS_commit_sha']):errors.append('H1_NO_EXACT_CAS')
            if not nonempty(x.get('CAS_receipt_evidence')):errors.append('H1_NO_CAS_RECEIPT_EVIDENCE')
        if x.get('verdict')=='H1_RECEIVED_SCOPED':
            if c.get('verdict')!='C_ACCEPT_SCOPED' or c.get('builder_grade')=='EXACT_BUILDER_HOLD':errors.append('H1_BAD_C_FOR_READY')
            if x.get('architecture_decidable_YN')!='YES' or x.get('commission_complete_YN')!='YES':errors.append('H1_READY_TRUTH_TABLE_FAIL')
        if x.get('verdict')=='H1_RECEIVED_CONDITIONAL':
            if c.get('verdict')!='C_ACCEPT_DOCUMENTARY_HOLD':errors.append('H1_BAD_C_FOR_CONDITIONAL')
            if x.get('architecture_decidable_YN')!='NO' or not realtext(x.get('exact_hold')):errors.append('H1_CONDITIONAL_WITHOUT_HOLD')
            if x.get('product_advance_grade') not in POL['progress_grades'][:-1]:errors.append('H1_CONDITIONAL_WITHOUT_VERIFIED_DELTA')
            if not realtext(x.get('product_delta_evidence_ref')):errors.append('H1_DELTA_NO_EVIDENCE')
        if x.get('engineering_accepted_YN')=='YES' and c.get('builder_grade')!='EXECUTED_FIRST_READER_PROOF':errors.append('H1_ENGINEERING_WITHOUT_EXECUTED_FIRST_EFFECT')
        if x.get('verdict')=='HQ_CURRENTNESS_HOLD' and not realtext(x.get('exact_hold')):errors.append('VAGUE_CURRENTNESS_HOLD')
        for k in ('commission_complete_YN','architecture_decidable_YN','engineering_accepted_YN','scientific_granted_YN','source_rights_granted_YN','actor_granted_YN','protected_received_YN'):
            if x.get(k) not in ('YES','NO'):errors.append('H1_MISSING_BINARY_'+k)
    return sorted(set(errors))

def render(spine,output_dir):
    d=pathlib.Path(output_dir);d.mkdir(parents=True,exist_ok=True)
    title=f"ANVIL R6 — {spine['author_proposed_grade']} — {spine['scope']}"
    lines=[f'# {title}','',f"Author proposal: **{spine['selected_candidate']}**; independent review pending.",f"Frozen plan: `{spine['freeze_digest']}`; comparator: `{spine['comparison_digest']}`.",'' ,'## Physical decisions']
    for x in spine.get('physical_decisions',[]):lines.append(f"- **{x['id']}** → {x['selected']}; cells {', '.join(x.get('cell_ids',[]))}; first consumer: {x.get('actual_first_consumer','NONE')}; dependency: {x.get('dependency_effect','NONE')}")
    lines.extend(['','## Limitations',spine.get('exact_conditional_reverser') or spine.get('exact_decision_blocker') or 'No conditional/blocked reverer declared.','','This output is an **author proposal** until independent C and owner H1 receiving; no native, source, scientific, actor or protected promotion.'])
    files={'DESIGN_DECISION.md':'\n'.join(lines)+'\n','GLOBAL_ARCHITECTURE.json':json.dumps({'nodes':spine.get('nodes',[]),'edges':spine.get('edges',[]),'routes':spine.get('routes',{})},indent=2)+'\n'}
    handoffs=''.join(canonical(x)+'\n' for x in spine.get('handoffs',[]));files['DOWNSTREAM_BUILD_HANDOFF.jsonl']=handoffs
    hist=spine['historical_inheritance'];items=[]
    for group,ids in SRC['mandatory'].items():
        for identity in ids:items.append({'id':identity,'group':group,'source_registry_digest':spine['source_registry_digest'],'operative_disposition':'INHERITED_EXACT_ID__NO_NEW_BUILD_GRANT','note':'Actual architecture effect is explicit only when linked to a material physical or semantic decision'})
    files['REQUIREMENT_CONSERVATION.jsonl']=''.join(canonical(x)+'\n' for x in items)
    eio=io.StringIO();w=csv.writer(eio,delimiter='\t');w.writerow(('evidence_id','grade','source_ref','raw_receipt_ref','independent_checked','description'))
    for key,x in sorted(spine.get('evidence',{}).items()):w.writerow((key,x.get('grade',''),x.get('source_ref',''),x.get('raw_receipt_ref',''),x.get('independent_checked',False),x.get('description','')))
    files['EVIDENCE_AND_FALSIFIERS.tsv']=eio.getvalue()
    files['OPERATIONAL_HANDOFF.md']=f"# ANVIL R6 operational handoff\n\nScope: {spine['scope']}\nAuthor-only grade: {spine['author_proposed_grade']}\nSelected: {spine['selected_candidate']}\n\nNext: independent C receives exact frozen P2, tests raw economics, source meaning, high-risk builder card, strongest rival, and contested materiality; then competent H1 owner with actual CAS.\n\nNo worker launch or authority promotion is implied.\n"
    for name,s in files.items():(d/name).write_text(s)
    manifest={n:hashlib.sha256(s.encode()).hexdigest() for n,s in files.items()};(d/'RENDER_SHA256.json').write_text(json.dumps(manifest,indent=2)+'\n')
    return manifest

def main():
    p=argparse.ArgumentParser(description=__doc__);sub=p.add_subparsers(dest='cmd',required=True)
    for cmd in ('check-claim','check-graph','check-handoff','check-stage','check-plan','compare','check-spine','render','check-render','amend'):
        a=sub.add_parser(cmd)
        if cmd in ('check-claim','check-graph','check-handoff','check-plan'):a.add_argument('path')
        elif cmd=='check-stage':a.add_argument('stage',choices=POL['stage_verdicts']);a.add_argument('path')
        elif cmd=='compare':a.add_argument('plan');a.add_argument('measure')
        elif cmd=='check-spine':a.add_argument('spine');a.add_argument('plan');a.add_argument('measure')
        elif cmd=='render':a.add_argument('spine');a.add_argument('output_dir')
        elif cmd=='check-render':a.add_argument('output_dir')
        elif cmd=='amend':a.add_argument('old_plan');a.add_argument('new_plan')
    a=p.parse_args();errs=[];out=None
    try:
        if a.cmd=='check-claim':errs=validate_source_claim(load(a.path))
        elif a.cmd=='check-graph':errs=validate_graph(load(a.path))
        elif a.cmd=='check-handoff':errs=validate_handoff(load(a.path))
        elif a.cmd=='check-stage':errs=check_stage(a.stage,load(a.path))
        elif a.cmd=='check-plan':errs=plan_errors(load(a.path))
        elif a.cmd=='compare':out=comparison(load(a.plan),load(a.measure));errs=out.get('errors',[])
        elif a.cmd=='check-spine':
            plan,measure=load(a.plan),load(a.measure);res=comparison(plan,measure);errs=res.get('errors',[])+validate_spine(load(a.spine),plan,measure,res)
        elif a.cmd=='render':out=render(load(a.spine),a.output_dir)
        elif a.cmd=='check-render':
            d=pathlib.Path(a.output_dir);m=load(d/'RENDER_SHA256.json')
            for fn,sha in m.items():
                if not (d/fn).is_file() or filehash(d/fn)!=sha:errs.append('RENDER_PROJECTION_TAMPER:'+fn)
        elif a.cmd=='amend':errs=plan_errors(load(a.new_plan),load(a.old_plan))
    except (ValueError,TypeError,KeyError,FileNotFoundError) as z:errs=['MALFORMED_INPUT:'+type(z).__name__+':'+str(z)]
    if out is None:out={}
    print(json.dumps({'status':'RED' if errs else 'PASS_STRUCTURAL_ONLY_NOT_AUTHENTICATED','errors':errs,'result':out},indent=2))
    return 2 if errs else 0
if __name__=='__main__':sys.exit(main())
