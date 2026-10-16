"""Two accepted prospective TEST_ONLY physical source profiles; B is invariant."""
from physical import *
from method_receipt import build,verify
base=json.loads((R/'runtime/handoff/first.json').read_text())['report'];root=R/'runtime/interventions';root.mkdir()
for name in ['R2_Y1','R1_Y0']:
 with Trace() as trace:
  owner,api,fx,installed=prepare(root/name/'ledger',name,policy=root/name/'policy.json',provision=True)
  report=api.run_sourcefree_with_register(**args(fx));current=api.read_current_consumer_material(fx['register'],report);actual=receipts(fx);receipt=build(owner,report,current,actual);verify(receipt)
 changes=[]
 for link in report['links']:
  ns=link['original_identity']['original']['respondent_namespace'];slot=link['original_identity']['operation']['slot'];old=next(x for x in base['links'] if x['original_identity']['original']['respondent_namespace']==ns and x['original_identity']['operation']['slot']==slot)
  if ns=='PV2-ADULT-B':assert link==old
  p=profile(link['consumer_material'])
  if ns=='PV2-ADULT-A' and name=='R2_Y1' and slot=='PAIR':assert p=={'0':{'denominator':1,'targets':{'0':0,'1':1}},'1':{'denominator':1,'targets':{'0':0,'1':1}}}
  if ns=='PV2-ADULT-A' and name=='R2_Y1' and slot=='B':assert p['1']==dict(denominator=2,targets={'0':1,'1':1})
  if ns=='PV2-ADULT-A' and name=='R1_Y0' and slot in ('PAIR','DISCOVERY'):assert p['1']==dict(denominator=1,targets={'0':1,'1':0})
  changes.append(dict(namespace=ns,slot=slot,old_consumer_ref=old['consumer_ref'],new_consumer_ref=link['consumer_ref'],old_fact=old['producer_result_ref'],new_fact=link['producer_result_ref'],old_query=old['consumer_material']['producer_query_ref'],new_query=link['consumer_material']['producer_query_ref'],profile=p,bitwise_unchanged=link==old))
 write(R/'evidence'/('intervention_'+name+'.json'),dict(installed=installed,report=report,current=current,method_receipt=receipt,exact_changes=changes,observed_distinct_product_refs=len({x['consumer_ref']['content_hash'] for x in report['links']}),new_durable_jobs=[len(x) for x in fx['calls']],actual_receipts=actual,trace=trace.data(),source_cells=[dict(namespace=x['universe'].respondent_namespace,cells=[dict(row=c.row_ordinal,item=c.variable_name,value=c.raw_value) for c in x['fx']['stream'].cell_iter_factory()]) for x in fx['inputs']]))
 print(name,'six original outputs; B bitwise stable')
