"""Small material counterexamples with captured actual values, not only assertions."""
from common import *
import copy
from collections import Counter
p=plan();r,rs,e=execute(p);out={}
# Documentary counts versus exact operation records; candidate input preserved untouched.
ledger=json.loads((R/'runtime_root/candidate/01_FULL_OPPORTUNITY_AND_DISPOSITION_LEDGER.json').read_text())
out['ledger']={'declared':ledger['counts'],'actual':dict(Counter(x['disposition'] for x in ledger['operations'])),'record_count':len(ledger['operations']),'used_by_runtime':False}
ops=builder().enumerate()
for status in ('HELD','INADMISSIBLE'):
 removed=next(o for o in ops if o.disposition.value==status);pp=plan(ops=[o for o in ops if o.op_id!=removed.op_id]);rr,rrs,ee=execute(pp)
 out['drop_'+status]={'removed':removed.op_id,'frontier_count':len(pp.frontier_receipts),'summary':asdict(rr.summary()),'consumer_ops':sorted(ee)}
items=w.independent_oracle_items();items[0]=replace(items[0],options=('changed','meaning'));pp=plan(items);_,rrs,ee=execute(pp)
out['option_mutation']={'unit_before':p.units_by_op['OP-WG0P-ORD-01-MARGINAL'].unit_ref.as_dict(),'unit_after':pp.units_by_op['OP-WG0P-ORD-01-MARGINAL'].unit_ref.as_dict(),'values_before':values(e)['OP-WG0P-ORD-01-MARGINAL'],'values_after':values(ee)['OP-WG0P-ORD-01-MARGINAL']}
p.source_issuer_grant['grant']='WITHDRAWN';old=w.consumer_effects(p,rs)
out['late_revocation']={'declared_current_grant':p.source_issuer_grant,'old_receipt_hashes':[x.receipt_hash for x in rs],'consumer_still_returns':sorted(old)}
p.fact_registry[rs[0].result_refs[0].key]['denominator']=999
out['consumer_tamper']={'result_ref':rs[0].result_refs[0].as_dict(),'old_receipt_hash':rs[0].receipt_hash,'returned_denominator':w.consumer_effects(p,rs)[rs[0].unit_ref.object_id] if False else [v['denominator'] for vals in w.consumer_effects(p,rs).values() for v in vals]}
pp=plan();pp.op_specs['OP-WG0P-ORD-01-MARGINAL'].release_tag='REL-A-W2';pp.op_specs['OP-WG0P-ORD-01-MARGINAL'].risk_name='R_ORD2';pp.op_specs['OP-WG0P-ORD-01-MARGINAL'].member_ids=('R11','R12','R13','R14');rr,rrs,ee=execute(pp)
out['wrong_release']={'unit_claims':[x.as_dict() for x in pp.units_by_op['OP-WG0P-ORD-01-MARGINAL'].release_refs],'executor_uses':pp.releases['REL-A-W2'].release_ref.as_dict(),'actual':values(ee)['OP-WG0P-ORD-01-MARGINAL'],'states':[x.state for x in rrs]}
orig=copy.deepcopy(w.COHORTS['REL-A-W1'])
for mode in ('row_change','missing_event','foreign_risk_member','mr_sets'):
 c=copy.deepcopy(orig)
 if mode=='row_change':c['rows'][0]['responses']['Q-ORD-A']='3'
 if mode=='missing_event':del c['rows'][0]['responses']['Q-ORD-A']
 if mode=='foreign_risk_member':c['risk_sets']['R_ORD']['Q-ORD-A'].add('FOREIGN')
 if mode=='mr_sets':c['native_option_sets']['H1']=('none',)
 w.COHORTS['REL-A-W1']=c
 try:
  pp=plan();rr,rrs,ee=execute(pp)
  rel=pp.repository.resolve_release_exact(pp.releases['REL-A-W1'].release_ref)
  out[mode]={'values':values(ee),'release':rel.release_ref.as_dict(),'source_artifact':rel.source_artifact_ref.as_dict(),'states':[x.state for x in rrs]}
 except Exception as ex:out[mode]={'error':type(ex).__name__,'detail':str(ex)}
 finally:w.COHORTS['REL-A-W1']=orig
# Replacing an edition on the mutable old plan: historical read has no new-edition resolver.
out['edition_replacement']={'old_receipts_remain_readable':bool(w.consumer_effects(p,rs)),'old_source_ref':p.releases['REL-A-W1'].release_ref.as_dict(),'replacement_ref':out['row_change']['release'],'limit':'New release constructed in fresh repository; old consumer has no source-edition/currentness interface. No canonical replacement performed.'}
dump('experiments.json',out);print('MATERIAL_EXPERIMENTS',len(out))
