"""Independent instrumentation of the unmodified candidate's actual chain."""
from pathlib import Path
import sys,json,copy
from unittest.mock import patch
RET=Path(__file__).resolve().parents[1]
SOURCE=RET/'runtime_root/source'
CAN=SOURCE/'WORKER_RETURNS/SOROK-R3-HQ300-CAN008-FIRST-POSITIVE-SOURCEFREE-R1'
sys.path[:0]=[str(CAN),str(SOURCE)]
from candidate import positive_chain as pc


def observe(mode='baseline',**kwargs):
    calls=[];ledgers=[]
    original=pc.ChainEventLedger
    class ObservedLedger(original):
        def __init__(self):
            super().__init__();ledgers.append(self)
        def read_effects(self,kind=None):
            if mode=='corrupt_stored_effect' and kind=='CAN008_CURRENT_RESPONSE_EFFECT':
                self.entries[0]['payload']['effect_kind']='AMPLIFY'
            actual=super().read_effects(kind)
            returned=[] if mode=='actual_absent_effect' and kind=='CAN008_CURRENT_RESPONSE_EFFECT' else actual
            calls.append(dict(function='ChainEventLedger.read_effects',kind=kind,stored=copy.deepcopy(actual),returned=copy.deepcopy(returned)))
            return returned
    def wrapping(name):
        f=getattr(pc,name)
        def wrapped(*args,**kw):
            def mat(x):
                if isinstance(x,dict):return {k:mat(v) for k,v in x.items()}
                if isinstance(x,(tuple,list)):return [mat(v) for v in x]
                if hasattr(x,'__dict__'):return mat(vars(x))
                return x
            result=f(*args,**kw)
            calls.append(dict(function=name,args=mat(args),kwargs=mat(kw),returned=copy.deepcopy(result)))
            return result
        return wrapped
    event_class=pc.AdmittedEvent
    def event_factory(**kw):
        if kw['event_id'].startswith('EV1'):
            if mode=='forged_issuer':kw['issuer_authority_id']='REVIEWER_FORGED'
            elif mode=='unadmitted':kw['admission_state']='REJECTED'
            elif mode=='fake_event_hash':kw['event_hash']=''
        return event_class(**kw)
    with patch.object(pc,'ChainEventLedger',ObservedLedger),patch.object(pc,'AdmittedEvent',event_factory),patch.object(pc,'coupline_evaluate',wrapping('coupline_evaluate')),patch.object(pc,'response_rule_apply',wrapping('response_rule_apply')),patch.object(pc,'adp016_form_causal_trace',wrapping('adp016_form_causal_trace')),patch.object(pc,'adp017_apply_epistemic_effect',wrapping('adp017_apply_epistemic_effect')):
        if mode=='published_control':result=pc.run_control_without_prior_effect(**kwargs)
        else:result=pc.run_positive_chain(later_event_requires_prior_effect=mode!='actual_absent_effect',**kwargs)
    return dict(mode=mode,result=result,calls=calls,ledger_entries=[copy.deepcopy(l.entries) for l in ledgers])


def main():
    out=RET/'repro/causal';out.mkdir(exist_ok=True)
    runs={name:observe(name) for name in ('baseline','published_control','actual_absent_effect','corrupt_stored_effect','forged_issuer','unadmitted','fake_event_hash')}
    replay=observe('baseline')
    assert replay['result']['full_replay_digest']==runs['baseline']['result']['full_replay_digest']
    for name,run in runs.items():(out/(name+'.json')).write_text(json.dumps(run,indent=2)+'\n')
    summary=dict(baseline=runs['baseline']['result']['later_event_response'],published_control=runs['published_control']['result']['later_event_response'],actual_absent=runs['actual_absent_effect']['result']['later_event_response'],replay_digest=runs['baseline']['result']['full_replay_digest'],exact_replay=True,published_control_actually_removes_effect=False)
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))
if __name__=='__main__':main()
