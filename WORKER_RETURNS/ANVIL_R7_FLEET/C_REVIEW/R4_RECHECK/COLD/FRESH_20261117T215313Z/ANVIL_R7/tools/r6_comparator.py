#!/usr/bin/env python3
"""R6 decision-grade structural comparator. Retains R5's numerical comparator as a historical API.

No local JSON field, SHA-looking string or successful arithmetic authenticates measurement,
source meaning, legal rights, an independent reviewer, or owner authority.
"""
import hashlib, json, math, pathlib
from compare_candidates import METRICS

ROOT=pathlib.Path(__file__).resolve().parents[1]
POLICY=json.loads((ROOT/'20_R6_MATERIAL_DECISION_CONSTITUTION.json').read_text())
FLOOR={k:set(v) for k,v in POLICY['metric_floor_by_case'].items()}
VETOES=set(POLICY['required_non_numeric_vetoes'])

def digest(data):
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False,separators=(',',':')).encode()).hexdigest()

def r6_full_comparison(data,frozen,evidence_root=None):
    """Return winner only for matched complete material coverage, no uncertified exclusions.

    B-added discriminators can extend the frozen contract only via a documented source-graded
    amendment frozen BEFORE its measurements. Material source/routing rights may be held;
    in that case report conditional rather than inventing a full-scope winner.
    """
    errors=[]
    if not isinstance(data,dict) or not isinstance(frozen,dict):
        return {'status':'RED','winner':None,'errors':['R6_BAD_COMPARISON_OBJECT']}
    if data.get('schema')!='ANVIL_R6_COMPARATOR_INPUT' or frozen.get('schema')!='ANVIL_R6_FROZEN_MATERIAL_CELLS':errors.append('R6_SCHEMA_MISMATCH')
    provided=data.get('frozen_sha256')
    if not isinstance(provided,str) or len(provided)!=64:errors.append('R6_MISSING_FROZEN_DIGEST')
    elif provided!=digest(frozen):errors.append('R6_FROZEN_DIGEST_MISMATCH')
    if frozen.get('material_floor_sha256')!=hashlib.sha256((ROOT/'20_R6_MATERIAL_DECISION_CONSTITUTION.json').read_bytes()).hexdigest():errors.append('R6_MATERIAL_POLICY_MISMATCH')
    cells=frozen.get('cells',[])
    if not isinstance(cells,list):cells=[];errors.append('R6_BAD_CELLS')
    seen={};cellids=set()
    for c in cells:
        if not isinstance(c,dict):errors.append('R6_BAD_CELL_OBJECT');continue
        ident=c.get('id');key=(c.get('workload_case_id'),c.get('metric'))
        if not isinstance(ident,str) or ident in cellids:errors.append('R6_DUPLICATE_CELL_ID')
        cellids.add(ident);seen.setdefault(key,[]).append(c)
        if key[0] not in FLOOR or key[1] not in METRICS:errors.append('R6_UNKNOWN_WORKLOAD_METRIC')
    exclusions=frozen.get('exclusions',[])
    if not isinstance(exclusions,list):exclusions=[];errors.append('R6_BAD_EXCLUSIONS')
    excluded=set()
    for ex in exclusions:
        if not isinstance(ex,dict):errors.append('R6_BAD_EXCLUSION');continue
        k=(ex.get('workload_case_id'),ex.get('metric'))
        if k not in {(ca,m) for ca,ms in FLOOR.items() for m in ms} or k in excluded or k in seen:errors.append('R6_BAD_EXCLUSION_SCOPE')
        excluded.add(k)
        if ex.get('B_challenge_status') not in {'INDEPENDENT_B_NONREVERSING_WITH_EVIDENCE','B_CHALLENGES_EXCLUSION'}:errors.append('R6_EXCLUSION_LACKS_B_CHALLENGE')
        if ex.get('B_challenge_status')=='B_CHALLENGES_EXCLUSION':errors.append('R6_CONTESTED_EXCLUSION')
        for f in ('reason_not_material','bounded_reversal_argument','first_consumer_impact','B_evidence_ref','C_adjudication_required','scope_effect'):
            if not isinstance(ex.get(f),str) or len(ex[f].strip())<25:errors.append('R6_EXCLUSION_UNPROVED_'+f)
    needed={(ca,m) for ca,ms in FLOOR.items() for m in ms}
    missing=sorted(needed-set(seen)-excluded)
    if missing:errors.append('R6_MATERIAL_DIMENSION_GAPS:'+','.join(f'{c}/{m}' for c,m in missing))
    extra=set(seen)-needed
    # Newly discovered material dimensions are allowed, but must be pre-result independently challenged.
    if extra:
        for key in extra:
            for c in seen[key]:
                if c.get('discovery_status')!='B_DISCOVERED_FROZEN_BEFORE_MEASUREMENT' or not isinstance(c.get('B_challenge_evidence'),str) or len(c['B_challenge_evidence'])<25:
                    errors.append('R6_UNQUALIFIED_NEW_DISCRIMINATOR:'+str(key))
    discovered=frozen.get('discovered_discriminators',[])
    if not isinstance(discovered,list):errors.append('R6_BAD_NEW_DISCRIMINATOR_REGISTER');discovered=[]
    for x in discovered:
        if not isinstance(x,dict):errors.append('R6_BAD_DISCOVERY');continue
        for k in ('id','source_or_consumer_reason','architecture_reversal_if_true','B_independent_challenge_receipt','premeasurement_freeze_receipt','smallest_probe_or_exact_hold'):
            if not isinstance(x.get(k),str) or len(x[k])<20:errors.append('R6_DISCOVERY_MISSING_'+k)
        if x.get('disposition') not in {'MATCHED_MEASURED','EXACT_HOLD','PROVED_IMMATERIAL_WITH_COURT'}:errors.append('R6_DISCOVERY_NOT_ADJUDICATED')
    checks=data.get('hard_veto_checks',[])
    if not isinstance(checks,list):checks=[]
    ids=[c.get('id') for c in checks if isinstance(c,dict)]
    if set(ids)!=VETOES or len(ids)!=len(VETOES):errors.append('R6_HARD_VETO_COVERAGE_INCOMPLETE')
    for c in checks:
        if not isinstance(c,dict):errors.append('R6_BAD_VETO_OBJECT');continue
        if c.get('status') not in {'PASS_AT_CLAIMED_SCOPE','HELD_WITH_EXACT_OWNER','FAIL'}:errors.append('R6_VETO_UNQUALIFIED')
        if not isinstance(c.get('evidence_ref'),str) or len(c['evidence_ref'])<20:errors.append('R6_VETO_MISSING_EVIDENCE')
        if c.get('status')=='PASS_AT_CLAIMED_SCOPE':
            f=c.get('receipt_path');h=c.get('receipt_sha256')
            if not isinstance(f,str) or not isinstance(h,str) or len(h)!=64:errors.append('R6_VETO_NO_RECEIPT_BYTES:'+str(c.get('id')))
            elif evidence_root is not None:
                root=pathlib.Path(evidence_root).resolve();path=(root/f).resolve()
                if not path.is_relative_to(root) or not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=h:errors.append('R6_VETO_RECEIPT_HASH_MISMATCH:'+str(c.get('id')))
    if data.get('candidate_ids')!=['A','B']:errors.append('R6_MISSING_EXACT_CANDIDATE_MAP')
    if errors:return {'status':'RED','winner':None,'errors':sorted(set(errors)),'missing_dimensions':missing}
    # R5's public numerical API remains available and unchanged for previously qualified
    # historical comparisons; R6 checks a stronger metric floor and separate veto court.
    obs=data.get('measurements',[])
    omap={x.get('cell_id'):x for x in obs if isinstance(x,dict)}
    unmeasured=[];A=[];B=[];overlap=[];invalid=[]
    for c in cells:
        cid=c.get('id'); o=omap.get(cid)
        if not o:unmeasured.append(cid);continue
        for scope in ('source_cut','source_grade','fixture_id','runner_id'):
            if o.get(scope)!=c.get(scope):invalid.append('R6_SCOPE_DRIFT:'+cid+':'+scope)
        for side in ('A','B'):
            v=o.get(side)
            if not isinstance(v,dict) or v.get('status')!='MEASURED':unmeasured.append(cid+':'+side);continue
            vals=[v.get(z) for z in ('low','value','high')]
            if any(type(t) not in (float,int) or not math.isfinite(t) or t<0 for t in vals) or not vals[0]<=vals[1]<=vals[2]:invalid.append('R6_INVALID_INTERVAL:'+cid+':'+side)
            receipt=v.get('receipt_path');sha=v.get('receipt_sha256')
            if not isinstance(receipt,str) or not isinstance(sha,str) or len(sha)!=64:invalid.append('R6_NO_RUNNER_RECEIPT:'+cid+':'+side)
            elif evidence_root is not None:
                root=pathlib.Path(evidence_root).resolve();p=(root/receipt).resolve()
                if not p.is_relative_to(root) or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:invalid.append('R6_RECEIPT_BYTES_MISMATCH:'+cid+':'+side)
        if cid in unmeasured or any(cid+':'+side in unmeasured for side in ('A','B')):continue
        if all(type(o[side].get(t)) in (float,int) for side in ('A','B') for t in ('low','high')):
            if o['A']['high']<o['B']['low']:A.append(cid)
            elif o['B']['high']<o['A']['low']:B.append(cid)
            else:overlap.append(cid)
    if set(omap)!=set(cellids) or len(obs)!=len(omap):invalid.append('R6_UNDECLARED_OR_DUPLICATE_MEASUREMENTS')
    hard=data.get('hard_vetoes')
    if not isinstance(hard,dict) or set(hard)!={'A','B'} or any(not isinstance(hard[x],list) for x in ('A','B')):invalid.append('R6_BAD_HARD_VETO_MAP')
    if invalid:return {'status':'RED','winner':None,'errors':sorted(set(invalid))}
    if any(c.get('status')!='PASS_AT_CLAIMED_SCOPE' for c in checks):return {'status':'HARD_VETO_UNPROVED','winner':None,'held_or_failed':[c['id'] for c in checks if c['status']!='PASS_AT_CLAIMED_SCOPE']}
    if hard['A'] or hard['B']:return {'status':'HARD_VETO_CANDIDATE_REJECTED','winner':None,'failed_vetoes':hard}
    if unmeasured:return {'status':'MISSING_DECISIVE_EVIDENCE','winner':None,'unmeasured_cells':sorted(set(unmeasured))}
    if any(x.get('disposition')=='EXACT_HOLD' for x in discovered):return {'status':'NEW_DISCRIMINATOR_UNRESOLVED','winner':None}
    if exclusions:return {'status':'EXCLUSIONS_REQUIRE_C_INDEPENDENT_COURT','winner':None,'measured_A_advantages':A,'measured_B_advantages':B,'excluded':len(exclusions)}
    if evidence_root is None:return {'status':'UNAUTHENTICATED_MEASUREMENT_RECEIPTS','winner':None,'A_advantages':A,'B_advantages':B,'uncertain_cells':overlap}
    if A and B:return {'status':'TRADEOFF','winner':None,'A_advantages':A,'B_advantages':B}
    if overlap:return {'status':'PARETO_NONDECISIVE','winner':None,'uncertain_cells':overlap,'A_advantages':A,'B_advantages':B}
    if A and not B:return {'status':'A_DOMINATES_FULL_MATERIAL_DIMENSIONS','winner':'A','A_advantages':A,'B_advantages':[]}
    if B and not A:return {'status':'B_DOMINATES_FULL_MATERIAL_DIMENSIONS','winner':'B','A_advantages':[],'B_advantages':B}
    return {'status':'PARETO_NONDECISIVE','winner':None,'uncertain_cells':[], 'A_advantages':A, 'B_advantages':B}

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser(description='Structural R6 matched comparison; actual runner and science independently verify')
    parser.add_argument('input');parser.add_argument('--frozen',required=True);parser.add_argument('--evidence-root')
    args=parser.parse_args()
    result=r6_full_comparison(json.loads(pathlib.Path(args.input).read_text()),json.loads(pathlib.Path(args.frozen).read_text()),args.evidence_root)
    print(json.dumps(result,indent=2));raise SystemExit(2 if result['status']=='RED' else 0)
