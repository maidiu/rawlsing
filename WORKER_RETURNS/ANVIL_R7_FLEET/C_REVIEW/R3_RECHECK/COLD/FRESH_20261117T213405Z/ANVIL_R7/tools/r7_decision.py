#!/usr/bin/env python3
"""R7 receipt-bound, hard-veto-first comparator and decision-DAG guard.

This program authenticates *contents against hash-pinned files*, not who ran them,
their scientific authority or whether the observed performance is genuine.
All outputs are author/structural scope until independently authenticated.
"""
from __future__ import annotations
import argparse,hashlib,json,math,pathlib,re,sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
POL=json.loads((ROOT/'24_R7_MACHINE_POLICY.json').read_text())
H64=re.compile(r'^[0-9a-f]{64}$'); H40=re.compile(r'^[0-9a-f]{40}$')
METRICS=POL['metric_units']; CEILING=POL['process_tree_rss_ceiling_bytes']
FLOOR={(case,metric) for case,ms in POL['metric_floor_by_case'].items() for metric in ms}

def floor_for(scope):
    base=set(FLOOR)
    for case,ms in POL['scope_additional_metric_floor'].get(scope,{}).items():
        base.update((case,metric) for metric in ms)
    return base

def check_priority_rule(rule,cells,frozen,errors,evidence_root):
    if rule is None:return
    if not isinstance(rule,dict):errors.append('R7_PRIORITY_RULE_NOT_OBJECT');return
    ids={c['id'] for c in cells if isinstance(c,dict) and isinstance(c.get('id'),str)}
    order=rule.get('order');reg=rule.get('max_acceptable_regression_ratio')
    if rule.get('frozen_before_results') is not True or rule.get('independent_C_adjudication_pending') is not True:
        errors.append('R7_PRIORITY_NOT_FROZEN_OR_FALSE_INDEPENDENT_AUTHORITY')
    if not isinstance(order,list) or len(order)!=len(ids) or set(order)!=ids:
        errors.append('R7_PRIORITY_NOT_COMPLETE_AND_DISTINCT')
    if not isinstance(reg,dict) or set(reg)!=ids or any(
            type(v) not in (float,int) or not math.isfinite(v) or not 1<=v<=100 for v in reg.values()):
        errors.append('R7_PRIORITY_REGRESSION_LIMITS_INVALID')
    for name in ('owner_decision_source','B_pre_result_challenge','first_consumer_cost_basis'):
        if not isinstance(rule.get(name),str) or len(rule[name].strip())<30:
            errors.append('R7_PRIORITY_UNSUBSTANTIATED_'+name)
    if not ishash(rule.get('owner_source_sha256')):
        errors.append('R7_PRIORITY_OWNER_DECISION_NOT_PINNED')
    owner_ptr=rule.get('owner_priority_receipt')
    if not isinstance(owner_ptr,dict):errors.append('R7_PRIORITY_OWNER_SOURCE_RECEIPT_MISSING')
    elif evidence_root is not None:
        receipt=_read_json(evidence_root,owner_ptr.get('path'),owner_ptr.get('sha256'),errors,'R7_PRIORITY_OWNER_RECEIPT')
        if receipt is not None:
            fields={'schema':'ANVIL_R7_OWNER_PRIORITY_RECEIPT','source_cut':frozen.get('source_cut'),
                    'scope':frozen.get('scope'),'order':order,
                    'max_acceptable_regression_ratio':reg,
                    'owner_decision_source':rule.get('owner_decision_source'),
                    'B_pre_result_challenge':rule.get('B_pre_result_challenge'),
                    'first_consumer_cost_basis':rule.get('first_consumer_cost_basis'),
                    'owner_source_sha256':rule.get('owner_source_sha256'),
                    'frozen_before_results':True,
                    'authority_grade':'OWNER_ASSERTED_PENDING_EXTERNAL_AUTHENTICATION'}
            for field,v in fields.items():
                if receipt.get(field)!=v:
                    errors.append('R7_PRIORITY_RECEIPT_CONTENT_DRIFT:'+field)
    if rule.get('results_already_seen') is not False:
        errors.append('R7_PRIORITY_POSTRESULT_INTRODUCTION_PROHIBITED')
    if rule.get('source_cut')!=frozen.get('source_cut') or rule.get('scope')!=frozen.get('scope'):
        errors.append('R7_PRIORITY_NOT_BOUND_TO_FROZEN_SCOPE_AND_SOURCE')


def canonical(o):return json.dumps(o,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False)
def digest(o):return hashlib.sha256(canonical(o).encode()).hexdigest()
def sha(b):return hashlib.sha256(b).hexdigest()
def isnum(x):return type(x) in (int,float) and math.isfinite(x) and x>=0
def ishash(x,pattern=H64):return isinstance(x,str) and bool(pattern.fullmatch(x))
def load_bytes(root,relative,expected,errors,code):
    if not isinstance(relative,str) or not relative.strip() or pathlib.PurePath(relative).is_absolute() or not ishash(expected):
        errors.append(code+'_LOCATOR');return None
    r=pathlib.Path(root).resolve();p=(r/relative).resolve()
    if not p.is_relative_to(r) or not p.is_file() or p.is_symlink():errors.append(code+'_MISSING_OR_ESCAPED');return None
    b=p.read_bytes()
    if sha(b)!=expected:errors.append(code+'_SHA256_MISMATCH');return None
    return b

def _read_json(root,rel,h,errors,code):
    b=load_bytes(root,rel,h,errors,code)
    if b is None:return None
    try:return json.loads(b)
    except (ValueError,UnicodeDecodeError):errors.append(code+'_NOT_JSON');return None

def _scope(cell,side,unit):
    return dict(candidate=side,cell_id=cell['id'],workload_case_id=cell['workload_case_id'],metric=cell['metric'],
                unit=unit,source_cut=cell.get('source_cut'),source_grade=cell.get('source_grade'),
                fixture_id=cell.get('fixture_id'),runner_id=cell.get('runner_id'))

def compare(data,frozen,evidence_root):
    errors=[]; policy_sha=sha((ROOT/'24_R7_MACHINE_POLICY.json').read_bytes())
    if not isinstance(data,dict) or not isinstance(frozen,dict):return {'status':'RED','winner':None,'errors':['R7_INPUT_NOT_OBJECT']}
    if data.get('schema')!='ANVIL_R7_COMPARATOR_INPUT' or frozen.get('schema')!='ANVIL_R7_FROZEN_PLAN':errors.append('R7_WRONG_SCHEMA')
    if evidence_root is None:errors.append('R7_EVIDENCE_ROOT_MANDATORY')
    if frozen.get('policy_sha256')!=policy_sha:errors.append('R7_POLICY_PIN_MISMATCH')
    if data.get('frozen_sha256')!=digest(frozen):errors.append('R7_MISSING_OR_STALE_FROZEN_PLAN_DIGEST')
    if data.get('candidate_ids')!=['A','B']:errors.append('R7_NOT_EXACT_A_B')
    scope=frozen.get('scope')
    if scope not in POL['scope_enum']:errors.append('R7_INVALID_OR_MISSING_DECISION_SCOPE')
    scope_floor=floor_for(scope) if scope in POL['scope_enum'] else FLOOR
    cheads=frozen.get('candidate_code_heads')
    if not isinstance(cheads,dict) or set(cheads)!={'A','B'} or any(not ishash(x,H40) for x in cheads.values()):
        errors.append('R7_UNPINNED_MATCHED_A_B_CODE_HEADS');cheads={}
    if frozen.get('phase')!='FROZEN_BEFORE_FIRST_RESULT' or not isinstance(frozen.get('version'),int) or frozen['version']<1:errors.append('R7_NOT_PRERESULT_VERSIONED_FREEZE')
    additional_units=frozen.get('new_metric_units',{})
    if not isinstance(additional_units,dict):errors.append('R7_BAD_NEW_METRIC_UNITS');additional_units={}
    for metric,unit in additional_units.items():
        if metric in METRICS or not isinstance(metric,str) or len(metric)<6 or unit not in ('s','bytes','count'):
            errors.append('R7_UNAUTHORIZED_NEW_METRIC_UNIT:'+str(metric))
    version=frozen.get('version')
    parent=None
    if type(version) is int and version>1:
        pointer=frozen.get('parent_plan_ref')
        if not isinstance(pointer,dict):errors.append('R7_NO_PARENT_PLAN_FOR_VERSIONED_AMENDMENT')
        elif evidence_root is not None:
            parent=_read_json(evidence_root,pointer.get('path'),pointer.get('sha256'),errors,'R7_PARENT_FROZEN_PLAN')
        if parent is not None:
            if parent.get('version')!=version-1 or parent.get('source_cut')!=frozen.get('source_cut') or parent.get('phase')!='FROZEN_BEFORE_FIRST_RESULT':
                errors.append('R7_AMENDMENT_PARENT_VERSION_OR_SOURCE_DRIFT')
            if frozen.get('first_results_seen') is not False or parent.get('first_results_seen') is not False:
                errors.append('R7_POST_RESULT_AMENDMENT_PROHIBITED')
            if not {digest(c) for c in parent.get('cells',[])}.issubset({digest(c) for c in frozen.get('cells',[])}):
                errors.append('R7_VERSIONED_AMENDMENT_DELETED_OR_REWROTE_FROZEN_CELL')
    elif additional_units:errors.append('R7_NOVEL_DISCRIMINATOR_WITHOUT_VERSIONED_PRERESULT_AMENDMENT')
    cells=frozen.get('cells',[])
    if not isinstance(cells,list):cells=[];errors.append('R7_CELLS_NOT_LIST')
    by={};keys=set()
    for c in cells:
        if not isinstance(c,dict) or not isinstance(c.get('id'),str):errors.append('R7_BAD_CELL');continue
        k=(c.get('workload_case_id'),c.get('metric'))
        if c['id'] in by or k in keys:errors.append('R7_DUPLICATE_CELL_OR_METRIC')
        by[c['id']]=c;keys.add(k)
        if k not in scope_floor:
            admitted=(type(version) is int and version>1 and c.get('metric') in additional_units and any(
                isinstance(z,dict) and z.get('new_metric')==c.get('metric') and z.get('workload_case_id')==c.get('workload_case_id')
                and z.get('status')=='MEASURED_IN_AMENDED_POLICY' for z in frozen.get('B_discriminators',[])))
            if not admitted:errors.append('R7_UNAUTHORIZED_EXTRA_METRIC_REQUIRES_B_CHALLENGE:'+str(k))
        for field in ('source_cut','source_grade','fixture_id','runner_id','first_consumer_id','negative_restore_oracle'):
            if not isinstance(c.get(field),str) or len(c[field].strip())<8:errors.append('R7_BAD_CELL_SCOPE:'+c['id']+':'+field)
        if not ishash(c.get('source_cut'),H40) or c.get('source_cut')!=frozen.get('source_cut'):
            errors.append('R7_BAD_OR_DRIFTING_SOURCE_CUT:'+c['id'])
        if not ishash(c.get('input_sha256')):errors.append('R7_UNPINNED_MATCHED_INPUT:'+c['id'])
        for f in ('source_width','respondent_count','event_count'):
            if type(c.get(f)) is not int or c[f]<0:errors.append('R7_UNPINNED_MATCHED_GEOMETRY:'+c['id']+':'+f)
    missing=scope_floor-keys
    check_priority_rule(frozen.get('priority_rule'),cells,frozen,errors,evidence_root)
    if missing:errors.append('R7_MISSING_MANDATORY_METRICS:'+repr(sorted(missing)))
    exclusions=frozen.get('exclusions',[])
    if not isinstance(exclusions,list):errors.append('R7_INVALID_EXCLUSIONS');exclusions=[]
    if exclusions:errors.append('R7_EXCLUSIONS_CANNOT_PROVE_COMPLETE_DOMINANCE')
    # A newly discovered B discriminator can change materiality. It cannot simply
    # be declared immaterial by the candidate that benefits from its omission.
    challenges=frozen.get('B_discriminators',[])
    if not isinstance(challenges,list):challenges=[];errors.append('R7_INVALID_B_CHALLENGES')
    for c in challenges:
        if not isinstance(c,dict):errors.append('R7_INVALID_B_CHALLENGE');continue
        if c.get('status') not in ('MEASURED_IN_AMENDED_POLICY','INDEPENDENTLY_DISPROVED_BEFORE_RESULTS'):

            errors.append('R7_UNRESOLVED_B_DISCOVERED_DISCRIMINATOR')
        for f in ('B_source_ref','independent_C_receipt_path','independent_C_receipt_sha256','pre_result_amendment_sha256'):
            if not c.get(f):errors.append('R7_B_CHALLENGE_MISSING:'+f)
        if evidence_root and c.get('independent_C_receipt_path'):
            review=_read_json(evidence_root,c['independent_C_receipt_path'],c.get('independent_C_receipt_sha256'),errors,'R7_B_CHALLENGE_C_RECEIPT')
            if review is not None and (review.get('schema')!='ANVIL_R7_C_DISCRIMINATOR_REVIEW' or review.get('new_metric')!=c.get('new_metric') or review.get('workload_case_id')!=c.get('workload_case_id') or review.get('pre_result') is not True or review.get('verdict')!='MATERIAL_COMPARATOR_ADDITIONAL_DIMENSION'):
                errors.append('R7_B_DISCRIMINATOR_REVIEW_WRONG_CONTENT')
        if type(version) is int and version>1 and isinstance(frozen.get('parent_plan_ref'),dict):
            if c.get('pre_result_amendment_sha256')!=frozen['parent_plan_ref'].get('sha256'):
                errors.append('R7_B_CHALLENGE_NOT_BOUND_TO_PARENT_BEFORE_RESULTS')
        if c.get('status')=='MEASURED_IN_AMENDED_POLICY' and (type(version) is not int or version<=1 or c.get('new_metric') not in additional_units):
            errors.append('R7_B_ADDED_METRIC_WITHOUT_AMENDED_VERSION')
    mlist=data.get('measurements',[])
    if not isinstance(mlist,list):mlist=[];errors.append('R7_MEASUREMENTS_NOT_LIST')
    bym={}; vals={}; proofkinds=set()
    for m in mlist:
        if not isinstance(m,dict):errors.append('R7_BAD_MEASUREMENT');continue
        cid=m.get('cell_id');c=by.get(cid)
        if cid in bym:errors.append('R7_DUPLICATE_MEASUREMENT:'+str(cid))
        bym[cid]=m
        if c is None:errors.append('R7_UNDECLARED_MEASUREMENT:'+str(cid));continue
        for side in ('A','B'):
            v=m.get(side)
            if not isinstance(v,dict) or v.get('status')!='MEASURED':errors.append('R7_UNMEASURED:'+str(cid)+':'+side);continue
            rec=_read_json(evidence_root,v.get('receipt_path'),v.get('receipt_sha256'),errors,'R7_MEASUREMENT_RECEIPT:'+str(cid)+':'+side) if evidence_root else None
            if rec is None:continue
            if rec.get('schema')!='ANVIL_R7_MEASUREMENT_RECEIPT':errors.append('R7_WRONG_RECEIPT_SCHEMA:'+cid+':'+side)
            for field,value in _scope(c,side,METRICS.get(c['metric'],additional_units.get(c['metric']))).items():
                if rec.get(field)!=value:errors.append('R7_RECEIPT_SCOPE_MISMATCH:'+cid+':'+side+':'+field)
            if rec.get('code_head')!=cheads.get(side) or rec.get('input_sha256')!=c.get('input_sha256'):
                errors.append('R7_RECEIPT_NOT_BOUND_TO_FROZEN_CODE_OR_SHARED_INPUT:'+cid+':'+side)
            if not ishash(rec.get('code_head'),H40) or not ishash(rec.get('input_sha256')):
                errors.append('R7_RECEIPT_UNPINNED_CODE_OR_INPUT:'+cid+':'+side)
            if any(rec.get(f)!=c.get(f) for f in ('source_width','respondent_count','event_count')):
                errors.append('R7_UNMATCHED_A_B_SOURCE_GEOMETRY:'+cid+':'+side)
            for f in ('clock_id','first_consumer_id','negative_restore_oracle','runner_command','source_width_label'):
                if not isinstance(rec.get(f),str) or len(rec[f].strip())<8:errors.append('R7_RECEIPT_MISSING:'+cid+':'+side+':'+f)
            if rec.get('first_consumer_id')!=c.get('first_consumer_id') or rec.get('negative_restore_oracle')!=c.get('negative_restore_oracle'):
                errors.append('R7_RECEIPT_CONSUMER_OR_NEGATIVE_DRIFT:'+cid+':'+side)
            if c.get('workload_case_id')=='W-D' and (type(rec.get('respondent_count')) is not int or rec['respondent_count']<100000 or type(rec.get('source_width')) is not int or rec['source_width']<600):
                errors.append('R7_DENSE_WIDTH_OR_100K_NOT_ACTUALLY_REPRESENTED:'+cid+':'+side)
            if c.get('workload_case_id')=='W-D' and (type(rec.get('event_count')) is not int or type(rec.get('respondent_count')) is not int or rec['event_count']<100*rec['respondent_count']):
                errors.append('R7_DENSE_NOT_ACTUALLY_HIGH_EVENT_DENSITY:'+cid+':'+side)
            if c.get('workload_case_id')=='W-S' and (type(rec.get('respondent_count')) is not int or rec['respondent_count']<100000 or type(rec.get('source_width')) is not int or rec['source_width']<600):
                errors.append('R7_SPARSE_WIDE_INSTRUMENT_OR_100K_MISSING:'+cid+':'+side)
            if c.get('workload_case_id')=='W-S' and (type(rec.get('event_count')) is not int or type(rec.get('respondent_count')) is not int or rec['event_count']>10*rec['respondent_count']):
                errors.append('R7_SPARSE_EVENT_GEOMETRY_NOT_SPARSE:'+cid+':'+side)
            if rec.get('execution_kind') not in ('SYNTHETIC_TEST','EXTERNAL_RUNNER_UNVERIFIED','EXTERNALLY_REVIEWED'):
                errors.append('R7_RECEIPT_UNKNOWN_EXECUTION_KIND:'+cid+':'+side)
            proofkinds.add(rec.get('execution_kind'))
            for f in ('respondent_count','source_width','event_count'):
                if type(rec.get(f)) is not int or rec[f]<0:errors.append('R7_RECEIPT_BAD_GEOMETRY:'+cid+':'+side+':'+f)
            fields=('low','value','high')
            nums=[rec.get(f) for f in fields]
            if not all(isnum(x) for x in nums) or not nums[0]<=nums[1]<=nums[2]:errors.append('R7_RECEIPT_INVALID_INTERVAL:'+cid+':'+side);continue
            if any(v.get(f)!=rec.get(f) for f in fields):errors.append('R7_MEASUREMENT_NOT_BOUND_TO_RECEIPT:'+cid+':'+side)
            vals[(cid,side)]=dict(zip(fields,nums))
    if set(by)!=set(bym):errors.append('R7_MISSING_DECLARED_MEASUREMENTS:'+repr(sorted(set(by)-set(bym))))
    # Veto receipts are candidate-specific and validated by exact content, not a
    # free-form PASS assertion or a shared source-static string.
    vlist=data.get('hard_veto_checks',[])
    if not isinstance(vlist,list):vlist=[];errors.append('R7_VETOES_NOT_LIST')
    vv={};vout={}
    for v in vlist:
        if not isinstance(v,dict):errors.append('R7_BAD_VETO');continue
        key=(v.get('candidate'),v.get('id'))
        if key in vv:errors.append('R7_DUPLICATE_VETO:'+str(key))
        vv[key]=v
        if key[0] not in ('A','B') or key[1] not in POL['required_non_numeric_vetoes']:errors.append('R7_UNKNOWN_VETO:'+str(key));continue
        rec=_read_json(evidence_root,v.get('receipt_path'),v.get('receipt_sha256'),errors,'R7_VETO_RECEIPT:'+str(key)) if evidence_root else None
        if rec is None:continue
        for f,x in [('schema','ANVIL_R7_VETO_RECEIPT'),('candidate',key[0]),('id',key[1]),('status',v.get('status'))]:
            if rec.get(f)!=x:errors.append('R7_VETO_RECEIPT_CONTENT_MISMATCH:'+str(key)+':'+f)
        if rec.get('source_cut')!=frozen.get('source_cut') or rec.get('code_head')!=cheads.get(key[0]) or not ishash(rec.get('code_head'),H40) or not isinstance(rec.get('first_consumer_id'),str) or len(rec['first_consumer_id'])<8:
            errors.append('R7_VETO_NO_SCOPE_OR_CONSUMER:'+str(key))
        if rec.get('status') not in ('PASS_AT_MEASURED_SCOPE','FAIL','HELD_WITH_OWNER'):errors.append('R7_BAD_VETO_STATUS:'+str(key))
        for f in ('negative_or_refusal','restoration','source_grade'):
            if not isinstance(rec.get(f),str) or len(rec[f])<8:errors.append('R7_VETO_MISSING:'+str(key)+':'+f)
        vout[key]=rec.get('status')
    required={(side,name) for side in ('A','B') for name in POL['required_non_numeric_vetoes']}
    if required!=set(vv):errors.append('R7_INCOMPLETE_CANDIDATE_SPECIFIC_VETOES:'+repr(sorted(required-set(vv))))
    if errors:return {'status':'RED','winner':None,'errors':sorted(set(errors)),'claim_grade':POL['author_only_grade']}
    relative={'A':[], 'B':[], 'uncertain':[]}
    for cid in sorted(by):
        a,b=vals[(cid,'A')],vals[(cid,'B')]
        if a['high']<b['low']:relative['A'].append(cid)
        elif b['high']<a['low']:relative['B'].append(cid)
        else:relative['uncertain'].append(cid)
    feasibility={}
    for side in ('A','B'):
        mem=[x for cid,c in by.items() if c['metric']=='process_tree_peak_rss_bytes' for x in [vals[(cid,side)]]]
        if not mem:feasibility[side]='HELD_NO_MEMORY_EVIDENCE'
        elif any(x['low']>CEILING for x in mem):feasibility[side]='FAIL_ABOVE_6GIB'
        elif any(x['high']>CEILING for x in mem):feasibility[side]='HELD_INTERVAL_CROSSES_6GIB'
        else:feasibility[side]='PASS_MEASURED_6GIB'
        if any(vout[(side,v)]=='FAIL' for v in POL['required_non_numeric_vetoes']):feasibility[side]='FAIL_SOURCE_OR_SEMANTIC_VETO'
        elif any(vout[(side,v)]!='PASS_AT_MEASURED_SCOPE' for v in POL['required_non_numeric_vetoes']) and not feasibility[side].startswith('FAIL'):
            feasibility[side]='HELD_SOURCE_OR_SEMANTIC_VETO'
    outcome={'status':'','winner':None,'claim_grade':POL['author_only_grade'],'runner_proof':'NOT_INDEPENDENTLY_AUTHENTICATED_BY_THIS_PROGRAM','relative_advantages':relative,'feasibility':feasibility,'measured_cells':len(by),'receipt_proof_kinds':sorted(proofkinds)}
    if all(feasibility[c].startswith('FAIL') for c in ('A','B')):outcome['status']='BOTH_INFEASIBLE';return outcome
    if any(feasibility[c].startswith('HELD') for c in ('A','B')):outcome['status']='FEASIBILITY_HELD';return outcome
    if any(feasibility[c].startswith('FAIL') for c in ('A','B')):
        fit=[c for c in ('A','B') if feasibility[c].startswith('PASS')]
        outcome.update(status='ONLY_'+fit[0]+'_FEASIBLE_AT_MEASURED_SCOPE',winner=fit[0] if fit else None)
        return outcome
    if relative['A'] and relative['B']:
        priority=frozen.get('priority_rule')
        if not priority:
            outcome['status']='MATERIAL_TRADEOFF_OWNER_PRIORITY_NOT_FROZEN';return outcome
        winner=next((('A' if cid in relative['A'] else 'B') for cid in priority['order']
                     if cid in relative['A'] or cid in relative['B']),None)
        if winner is None:
            outcome['status']='MATERIAL_TRADEOFF';return outcome
        loser='B' if winner=='A' else 'A'
        excessive=[];regressions={}
        for cid in priority['order']:
            if cid not in relative[loser]:continue
            chosen=vals[(cid,winner)];other=vals[(cid,loser)]
            # Conservative interval bound: worst winner divided by best loser.
            ratio=float('inf') if other['low']==0 else chosen['high']/other['low']
            regressions[cid]=ratio
            if ratio>priority['max_acceptable_regression_ratio'][cid]:excessive.append(cid)
        outcome['priority_rule_source_sha256']=priority['owner_source_sha256']
        outcome['priority_regressions']=regressions
        if excessive:
            outcome.update(status='TRADEOFF_EXCEEDS_FROZEN_REGRESSION_LIMITS',excessive_cells=sorted(excessive))
        else:
            outcome.update(status=winner+'_PRIORITY_WIN_PENDING_INDEPENDENT_C',winner=winner,
                           reviewer_grade='AUTHOR_PROVISIONAL_NOT_COMPETENT_OWNER_SELECTION')
        return outcome
    if relative['uncertain']:outcome['status']='UNRESOLVED_MATERIAL_INTERVAL';return outcome
    if relative['A'] and not relative['B']:outcome.update(status='A_DOMINATES_RECEIPT_BOUND_MATERIAL_SET',winner='A')
    elif relative['B'] and not relative['A']:outcome.update(status='B_DOMINATES_RECEIPT_BOUND_MATERIAL_SET',winner='B')
    else:outcome['status']='PARETO_NO_DECISIVE_ADVANTAGE'
    return outcome

def check_decision_dag(ledger,comparison_result,frozen,r5_spine=None):
    """Check all material physical choices, reference integrity, metric effects and local cost evidence.

    Numerical coverage cannot by itself prove every causal dependency. Independent C
    still owes a substantive omitted-dependency challenge.
    """
    e=[]
    if ledger.get('schema')!='ANVIL_R7_PHYSICAL_DECISION_LEDGER':e.append('R7_BAD_DECISION_LEDGER_SCHEMA')
    if ledger.get('frozen_sha256')!=digest(frozen):e.append('R7_DECISION_NOT_BOUND_TO_FROZEN_PLAN')
    decisions=ledger.get('physical_decisions',[])
    if not isinstance(decisions,list) or not decisions:e.append('R7_NO_MATERIAL_DECISIONS');decisions=[]
    by={d.get('id'):d for d in decisions if isinstance(d,dict)}
    if len(by)!=len(decisions):e.append('R7_DUPLICATE_DECISION_ID')
    cby={x['id']:x for x in frozen.get('cells',[])}
    winner=comparison_result.get('winner')
    for d in decisions:
        if not isinstance(d,dict):e.append('R7_BAD_PHYSICAL_DECISION');continue
        did=d.get('id');cls=d.get('decision_class');deps=d.get('depends_on')
        if cls not in POL['decision_class_metric_requirements']:e.append('R7_UNKNOWN_MATERIAL_DECISION_CLASS:'+str(did));continue
        if not isinstance(deps,list) or any(dep not in by or dep==did for dep in deps) or len(deps)!=len(set(deps)):
            e.append('R7_NONEXISTENT_OR_DUPLICATE_DEPENDENCY:'+str(did))
        if d.get('selected_candidate')!=winner or winner not in ('A','B'):
            e.append('R7_PHYSICAL_CHOICE_WITHOUT_COMPARATOR_SUPPORT:'+str(did))
        if not isinstance(d.get('first_consumer_id'),str) or len(d['first_consumer_id'])<8:
            e.append('R7_NO_REAL_FIRST_CONSUMER_ID:'+str(did))
        if not isinstance(d.get('source_semantic_effect'),str) or len(d['source_semantic_effect'])<30 or not isinstance(d.get('negative_and_restore_effect'),str) or len(d['negative_and_restore_effect'])<30:
            e.append('R7_MISSING_SEMANTIC_OR_NEGATIVE_CONSEQUENCE:'+str(did))
        ids=d.get('material_cell_ids',[])
        if not isinstance(ids,list) or len(ids)!=len(set(ids)) or any(x not in cby for x in ids):e.append('R7_INVALID_LINKED_MATERIAL_CELL:'+str(did));ids=[]
        matched={cby[x]['metric'] for x in ids if x in cby}
        matched_cases={(cby[x]['workload_case_id'],cby[x]['metric']) for x in ids if x in cby}
        if not set(POL['decision_class_metric_requirements'][cls])<=matched:e.append('R7_DECISION_LACKS_REQUIRED_COST_DIMENSIONS:'+str(did))
        required_pairs={tuple(x) for x in POL['decision_class_case_metric_requirements'][cls]}
        for x in POL['decision_scope_extra_pairs'].get(frozen.get('scope'),{}).get(cls,[]):
            required_pairs.add(tuple(x))
        if not required_pairs<=matched_cases:e.append('R7_DECISION_LACKS_REQUIRED_MATERIAL_CASES:'+str(did))
        effects=d.get('material_effects',[])
        if not isinstance(effects,list) or {z.get('cell_id') for z in effects if isinstance(z,dict)}!=set(ids):
            e.append('R7_DECISION_EFFECTS_DO_NOT_CLOSE_ON_LINKED_CELLS:'+str(did))
        for z in effects if isinstance(effects,list) else []:
            if not isinstance(z,dict):continue
            cid=z.get('cell_id');c=cby.get(cid)
            if c is None:continue
            if z.get('metric')!=c['metric'] or z.get('workload_case_id')!=c['workload_case_id']:
                e.append('R7_MATERIAL_EFFECT_MISMATCH:'+str(did)+':'+str(cid))
            if not isinstance(z.get('causal_dependency'),str) or len(z['causal_dependency'])<35:
                e.append('R7_UNJUSTIFIED_EFFECT_OR_BORROWED_BENCHMARK:'+str(did)+':'+str(cid))
        if cls=='CANONICAL_SOURCE_LAYOUT' and 'SOURCE_SEMANTICS_AND_ROUTING' not in d.get('hard_veto_ids',[]):e.append('R7_LAYOUT_MISSING_SOURCE_SEMANTICS_VETO:'+str(did))
        if cls=='DOWNSTREAM_OUTPUT_ABI' and 'NONPRECLUSION_OF_INDEPENDENT_WORLD_AND_ACTOR' not in d.get('hard_veto_ids',[]):e.append('R7_OUTPUT_MISSING_WORLD_ACTOR_VETO:'+str(did))
    if r5_spine is not None:
        inherited={d.get('id') for d in r5_spine.get('decisions',[]) if isinstance(d,dict) and d.get('class')=='PHYSICAL'}
        claimed={d.get('inherited_R5_physical_decision_id') for d in decisions if isinstance(d,dict)}
        if not inherited.issubset(claimed):e.append('R7_R5_PHYSICAL_DECISIONS_NOT_ALL_INHERITED:'+repr(sorted(inherited-claimed)))
        if claimed-inherited:e.append('R7_INVENTED_R5_PHYSICAL_DEPENDENCY:'+repr(sorted(claimed-inherited)))
    visited=set();stack=set()
    def visit(x):
        if x in stack:e.append('R7_DECISION_DEPENDENCY_CYCLE');return
        if x in visited:return
        visited.add(x);stack.add(x)
        for child in by.get(x,{}).get('depends_on',[]):
            if child in by:visit(child)
        stack.remove(x)
    for x in by:visit(x)
    return sorted(set(e))

def main():
    p=argparse.ArgumentParser();sub=p.add_subparsers(dest='mode',required=True)
    c=sub.add_parser('compare');c.add_argument('measurements');c.add_argument('frozen');c.add_argument('--evidence-root',required=True)
    c=sub.add_parser('check-decisions');c.add_argument('ledger');c.add_argument('measurements');c.add_argument('frozen');c.add_argument('--evidence-root',required=True)
    a=p.parse_args()
    try:
        frozen=json.loads(pathlib.Path(a.frozen).read_text());data=json.loads(pathlib.Path(a.measurements).read_text())
        result=compare(data,frozen,a.evidence_root)
        if a.mode=='check-decisions':
            errs=check_decision_dag(json.loads(pathlib.Path(a.ledger).read_text()),result,frozen)
            result={'status':'RED' if errs else result['status'],'comparison':result,'decision_errors':errs}
    except (OSError,ValueError,TypeError,KeyError) as exc:result={'status':'RED','errors':['R7_BAD_INPUT:'+type(exc).__name__+':'+str(exc)]}
    print(json.dumps(result,indent=2));return 2 if result['status']=='RED' else 0
if __name__=='__main__':sys.exit(main())
