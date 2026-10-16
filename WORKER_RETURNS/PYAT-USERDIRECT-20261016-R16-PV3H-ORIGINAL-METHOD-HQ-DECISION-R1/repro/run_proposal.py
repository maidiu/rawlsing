"""New bounded native values-read experiment; no completed acceptance court rerun."""
from physical import *
from method_receipt import build,verify
from generic_proposal import build_proposal
ROOT=R/'runtime/generic_experiment';assert not ROOT.exists(),'EXISTING_EXPERIMENT_REFUSED';ROOT.mkdir()
E=R/'evidence/generic';E.mkdir(parents=True,exist_ok=True)
base=None
for name in ['BASELINE','R2_Y1','R1_Y0']:
 root=ROOT/name
 with Trace() as trace:
  owner,api,fx,installed=prepare(root/'ledger',name,policy=root/'policy.json',provision=True)
  report=api.run_sourcefree_with_register(**args(fx));current=api.read_current_consumer_material(fx['register'],report);actual=receipts(fx)
  data=trace.data();proposal=build_proposal(api,fx['register'],report,data);receipt=build(owner,report,current,actual);verify(receipt)
  output=dict(installed=installed,report=report,current=current,actual_receipts=actual,method_receipt=receipt,proposal=proposal,trace=data,source_cells=[dict(namespace=x['universe'].respondent_namespace,cells=[dict(row=c.row_ordinal,item=c.variable_name,value=c.raw_value) for c in x['fx']['stream'].cell_iter_factory()]) for x in fx['inputs']])
 write(E/(name+'.json'),output)
 if name=='BASELINE':
  base=output
  # Fresh source use resolves actual persisted withdrawal, preserving history.
  beforeB=build_proposal(api,fx['register'],report,data,namespace='PV2-ADULT-B');historical=deepcopy(proposal)
  FixtureOwnerControl(policy_path=root/'policy.json').withdraw('PV2-ADULT-A','PV3H_CURRENT_SOURCE_WITHDRAWAL')
  A=build_proposal(api,fx['register'],report,data,namespace='PV2-ADULT-A');B=build_proposal(api,fx['register'],report,data,namespace='PV2-ADULT-B');owner.client().verify_history(report)
  write(E/'current_history.json',dict(A_after=A,B_before=beforeB,B_after=B,historical_proposal_unchanged=proposal==historical,original_history_verified=True,generic_current=api.read_current_consumer_material(fx['register'],report,semantics='GENERIC_NATIVE')))
 else:
  # Retain original PV3A compatibility input for its exact focused assertions.
  old={x['original_expected_work_key']:x for x in base['report']['links'] if x['original_identity']['original']['respondent_namespace']=='PV2-ADULT-B'}
  assert all(x==old[x['original_expected_work_key']] for x in report['links'] if x['original_identity']['original']['respondent_namespace']=='PV2-ADULT-B')
  write(R/'evidence'/('intervention_'+name+'.json'),output)
 print(name,'six native specialized consumers and six separate proposal input reads',flush=True)
# Additional actual I03/Field Forge empty-risk and native missing response control.
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.field_forge_conditional_support import produce_exact_conditional_support_profile
with Trace() as edges:
 owner,api,fx,installed=prepare(ROOT/'edges/ledger',policy=ROOT/'edges/policy.json',provision=True)
 d=fx['inputs'][0];stub=dict(universe=d['universe'],respondents={r.respondent_key:r for r in d['projection'].respondents},qrefs=d['fx']['qrefs'],risk_refs={'R':d['fx']['risk']},source_auth=d['projection'].authority_snapshots[0]);qa=d['fx']['qauth'];da=d['fx']['dauth']
 pred=F._branch_predicate(stub,qa,members=(),tag='pv3h-empty');query=F._query(stub,qa,pred,('X','Y'),measure='RAW',tag='pv3h-empty');session=fx['plans'][0].p01_kwargs['session']
 fact=execute_empirical_query(repository=session.repository,query=query,predicate=pred,authority_registry=AuthorityRegistry((*d['projection'].authority_snapshots,qa,da)),release_refs=session.identity.release_refs).facts[0]
 consumer=produce_exact_conditional_support_profile(joint_fact=fact,joint_query=query,conditioner_ref=d['fx']['qrefs']['X'],target_ref=d['fx']['qrefs']['Y'],producer_permission_ceiling=('SOURCE_FREE_DEV',))
 import rawlsing_next.tests.test_pre553_empirical_query as Q
 source=Q._build_source('pv3h-missing',[dict(id='R1',responses={'X':1,'Y':1}),dict(id='R2',responses={'X':0})]);qauth=Q._query_authority('pv3h-missing');p=Q._branch_predicate(source,qauth);q=Q._query(source,qauth,p,('X','Y'),tag='pv3h-missing');missing=Q._run(source,qauth,p,q).facts[0]
write(E/'edge_cases.json',dict(empty_risk=dict(fact=fact.semantic_projection(),consumer=consumer.as_dict()),missing=missing.semantic_projection(),trace=edges.data()))
