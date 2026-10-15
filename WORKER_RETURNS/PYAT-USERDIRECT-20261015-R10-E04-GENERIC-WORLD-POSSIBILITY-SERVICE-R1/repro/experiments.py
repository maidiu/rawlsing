"""Actual producer -> selected snapshot -> native probabilities -> two consumers.

Author experiment at predeclared synthetic grain; not independent adoption.
"""
from pathlib import Path
import sys,json,copy
RET=Path(__file__).resolve().parents[1];sys.path[:0]=[str(RET),str(RET/'runtime_root/source')]
from product.service import GenericSelectedWorldService
from product.nonparent import consume
from product.scenario import evaluate
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.objective_consumer_bounded_evidence import installation_manifest,OC05
TARGETS={'provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context','ingest_c11_source_release','execute_empirical_query'}
observed=[];active={}
def profiler(frame,event,result):
    if frame.f_code.co_name not in TARGETS or not frame.f_globals.get('__name__','').startswith('rawlsing_next.'):return
    if event=='call':
        row=dict(id=len(observed),function=frame.f_code.co_name,module=frame.f_globals['__name__'],file=str(Path(frame.f_code.co_filename).resolve().relative_to(RET)),event='ACTUAL_CALL',input_evidence_refs=[])
        for e in frame.f_locals.get('evidence',()):row['input_evidence_refs'].append(e.evidence_ref.as_dict())
        observed.append(row);active[id(frame)]=row
    if event=='return' and id(frame) in active:
        row=active.pop(id(frame));row['return_type']=type(result).__name__
        for key in ('raw_denominator_support','provider_state','analytical_state','result_state'):
            if hasattr(result,key):row[key]=getattr(result,key)
        if getattr(result,'exact_evidence_ref',None) is not None:row['consumed_evidence_ref']=result.exact_evidence_ref.as_dict()

def pair(**options):
    s=GenericSelectedWorldService(**options);snap=s.select()
    worker=consume(s,snap);scenario=evaluate(s,snap,[dict(scenario_id='INSTITUTIONAL_PROPOSAL',route='institutional'),dict(scenario_id='CIVIL_PROPOSAL',route='civil')])
    return s,snap,dict(nonparent=worker,conception_proposals=scenario)

def main():
    out=RET/'outputs';out.mkdir(exist_ok=True);sys.setprofile(profiler)
    base,snap,a=pair();emp,es,b=pair(empirical_changed=True);struct,ss,c=pair(structural_revision=True);null,ns,d=pair();irrelevant,irs,e=pair(extra_field=999)
    reverse=base.possibilities(snap,target='A',conditions=[('Y',1)],consumer='GENERIC_REVERSE')
    loss=GenericSelectedWorldService(support_loss=True);loss_product=loss.possibilities(loss.select())
    marginal=GenericSelectedWorldService(same_marginals=True);same_marginal_reverse=marginal.possibilities(marginal.select(),target='A',conditions=[('Y',1)])
    civil=base.structural_product(snap);history=copy.deepcopy(a['nonparent'])
    invalidation=base.invalidate('training_access');after_revoke=consume(base,base.select())
    rev_emp=base.invalidate('empirical');emp_after_revoke=consume(base,snap)
    archived=base.historical_receipt(history['receipt_hash'])
    clocks={mode:struct.select(mode=mode,valid_at=valid,published_asof=pub,**({'test_now':valid} if mode=='TEST_CURRENT' else {})).material for mode,valid,pub in [('HISTORICAL','2026-09-01','2027-09-01'),('AS_OF','2027-02-01','2027-03-01'),('TEST_CURRENT','2027-09-01','2027-09-01')]}
    sys.setprofile(None)
    worker=lambda r:r['nonparent']['material'];scenarios=lambda r:r['conception_proposals']['material']['scenarios']
    assert worker(a)['structural_routes']==worker(b)['structural_routes']
    assert worker(a)['empirical']==worker(c)['empirical']
    assert worker(a)['structural_routes']['training']['state']!=worker(c)['structural_routes']['training']['state']
    assert worker(a)['structural_routes']['civil']==worker(c)['structural_routes']['civil']
    assert a==d
    assert worker(a)['empirical']==worker(e)['empirical'] and scenarios(a)==scenarios(e)
    assert [x['source_balance_count'] for x in worker(a)['source_balance_reads']]==[4,4,4]
    assert [x['source_balance_count'] for x in worker(b)['source_balance_reads']]==[6,6,6]
    assert reverse['steps'][0]['denominator']==29 and same_marginal_reverse['steps'][0]['denominator']==29
    assert loss_product['steps'][-1]['state']=='ZERO_SUPPORT' and loss_product['steps'][-1]['denominator']==0
    assert archived['material']==history['material'] and archived['fresh_use_authorized'] is False
    assert civil['receipt_hash'] in invalidation['unaffected'] and civil['receipt_hash'] in rev_emp['unaffected']
    packet=dict(schema='E04_EXECUTED_INDEPENDENT_INTERVENTION_PACKET@1',grade='AUTHOR_SOURCEFREE_INTERFACE_PROOF_NOT_ADOPTION',baseline=a,empirical_source_cell_intervention=b,structural_access_exit_intervention=c,null_control=d,irrelevant_field_control=e,legal_reverse=reverse,same_marginal_different_conditional=same_marginal_reverse,measured_support_loss=loss_product,structural_permission_invalidation=invalidation,after_structural_revoke=after_revoke,empirical_permission_invalidation=rev_emp,after_empirical_revoke=emp_after_revoke,historical_receipt_retained=archived,publication_clock_selections=clocks,native_owner_trace=observed,adapter_traces=dict(empirical=base.provider.trace,selected_world=base.catalog.trace),values_read=base.value_reads)
    (RET/'03_TWO_GENERIC_CONSUMERS_AND_INDEPENDENT_INTERVENTIONS.json').write_text(json.dumps(packet,indent=2)+'\n')
    (RET/'01_COHERENT_WORLD_SNAPSHOT_AND_CLOCKS.json').write_text(json.dumps(dict(snapshot_ref=snap.snapshot_hash,material=snap.material,native_clock_correction='00A_NATIVE_CLOCK_CORRECTION.json',clock_selections=clocks,grade='TEST_ONLY; no operative N9/CURRENT or issuer'),indent=2)+'\n')
    policy=next(p for p in installation_manifest() if p['policy_id']==OC05)
    summary=dict(empirical_denominators=[x['denominator'] for x in worker(a)['empirical']['steps']],baseline_balances=[x['source_balance_count'] for x in worker(a)['source_balance_reads']],changed_balances=[x['source_balance_count'] for x in worker(b)['source_balance_reads']],reverse_denominator=reverse['steps'][0]['denominator'],support_loss_denominators=[x['denominator'] for x in loss_product['steps']],same_marginal_reverse_denominator=same_marginal_reverse['steps'][0]['denominator'],actual_native_calls=len(observed),native_functions=sorted({r['function'] for r in observed}),OC05_actual_installation=policy,packet_sha256=__import__('hashlib').sha256((RET/'03_TWO_GENERIC_CONSUMERS_AND_INDEPENDENT_INTERVENTIONS.json').read_bytes()).hexdigest(),null_replay_identical=True,source_original_reads=0,model_calls=0,actor_calls=0)
    (out/'experiment_summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
