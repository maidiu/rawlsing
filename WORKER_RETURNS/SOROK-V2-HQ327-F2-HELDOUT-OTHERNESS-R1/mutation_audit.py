"""Run independently distinguishable deliberate bad adapters against frozen F2."""
import copy,json
from pathlib import Path
from reference_oracle import evaluate,validate_native_receipt,scientific_projection
from test_heldout import CASES,mutant_constant,mutant_label_only,native_from_oracle


def mutate_false_event_identity(c):
    r=copy.deepcopy(evaluate(c))
    if c['id']=='F2-027':
        r.update(status='ELIGIBLE_NONCAUSAL',code='SOURCEFREE_EVIDENCE_BOUNDARY_PASS',no_mutation=True,new_event_count=1)
    return r

def mutate_fact_promotion(c):
    r=copy.deepcopy(evaluate(c))
    if r['status']=='ELIGIBLE_NONCAUSAL':r['asserted_culprit_group']='peer_blame'
    return r

def mutate_self_authorized_owner(c):
    r=copy.deepcopy(evaluate(c))
    if r['status']=='ELIGIBLE_NONCAUSAL':
        r['owner_effect_committed']=True;r.pop('independent_owner_receipt',None)
    return r


def check():
    mutants={
       'CONSTANT_RESPONDER':mutant_constant,
       'COSMETIC_LABEL_RESPONDER':mutant_label_only,
       'EVENT_ID_COLLISION_BYPASS':mutate_false_event_identity,
       'IDEOLOGICAL_CLAIM_AS_CULPRIT':mutate_fact_promotion,
       'SELF_GRANTED_DURABLE_EFFECT':mutate_self_authorized_owner,
    }
    rows=[]
    for name,mutant in mutants.items():
        reds=[];greens=[]
        for id,c in CASES.items():
            try:
                errors=validate_native_receipt(c,mutant(c))
            except Exception as ex:errors=['MUTANT_EXCEPTION_'+type(ex).__name__]
            (reds if errors else greens).append(id)
        rows.append(dict(mutant=name,killed=bool(reds),red_count=len(reds),pass_count=len(greens),sample_reds=reds[:8],
                         note='F2 oracle rejection, not independent human-model science'))
    metamorphic_bad=mutant_label_only(CASES['F2-001'])['selected_affect'] != mutant_label_only(CASES['F2-002'])['selected_affect']
    reference_invariant=scientific_projection(evaluate(CASES['F2-001']))==scientific_projection(evaluate(CASES['F2-002']))
    nochange_pass=[id for id in ('F2-015','F2-016','F2-041') if not validate_native_receipt(CASES[id],native_from_oracle(id))]
    result=dict(schema='F2_MUTATION_SENSITIVITY_V1',mutants=rows,mutants_killed=sum(r['killed'] for r in rows),total_mutants=len(rows),
        cosmetic_label_scientific_invariance=reference_invariant,cosmetic_mutant_changes_affect=metamorphic_bad,
        lawful_no_change_cases_green=nochange_pass,grade='INDEPENDENT_SOURCEFREE_REFERENCE_ONLY',future_b3='NOT_RUN')
    assert result['mutants_killed']==result['total_mutants'],result
    assert reference_invariant and metamorphic_bad
    assert len(nochange_pass)==3
    return result

if __name__=='__main__':
    r=check();Path('mutation_receipt.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,sort_keys=True))
