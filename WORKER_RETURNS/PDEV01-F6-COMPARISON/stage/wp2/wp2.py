"""Bounded owner transport. All science and modeled rules execute inherited code.

No original source processing, new world ontology, numeric scaling, model grant,
canonical installation or actor execution is performed by this port.
"""
from pathlib import Path
import sys,json,copy,hashlib,importlib.util,collections
R=Path(__file__).resolve().parents[1];S=R/'selected'
sys.path[:0]=list(map(str,[S,S/'rawlsing_next/tests',S/'rawlsing_next']))
import e05_n9_selected_world_adapter as E
from product.service import GenericSelectedWorldService
from product.nonparent import consume
from product.scenario import evaluate
from rawlsing_next.pre553_hq297_n9c_two_field_reader import TestOnlyRegistry,GSS,NCA
from rawlsing_next.pre553_empirical_objects import canonicalize,semantic_hash
from rawlsing_next.pre553_empirical_possibility_provider import provide_empirical_possibility_slice
from rawlsing_next.tests import n10e_empirical_slice_fixture as AT07
FIX=S/'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json'
HOLD=dict(code='NAMED_N10W_RULE_HOLD',owner='N10W structural-route possibility/model-use owner; competent HQ decision required',receiver='NONPARENT_OPTIONS generic read-only world input port',missing='Exact permitted joint structural-route model and consumer-use binding for selected M4/M5 world plus C1/N10E evidence; F6M test-only sidecar has no installed N9 binding',expected_property='A substantive permitted structural rule changes a structured opportunity result while exact empirical denominator, minority cells, clocks and source permissions remain conserved; any probability requires an independently justified model',positive_test='Use two exact issued rule refs with same empirical evidence, same-rule relabel control, selective revocation and effective/publication/request/actor-clock separation; native named receiver must dereference refs and refuse unissued model use',rollback='Keep all installed service/model flags false; retain exact upstream receipts and replay; no canonical writes')
PROPOSALS=[dict(scenario_id='WP2_INDEPENDENT_TRAINING',route='institutional'),dict(scenario_id='WP2_INDEPENDENT_CIVIL',route='civil')]
def rows():return json.loads(FIX.read_text())['fields']
def make(**kw):
 registry=kw.pop('registry',None)
 return E.N9SelectedWorldAdapter(service=GenericSelectedWorldService(**kw),registry=TestOnlyRegistry(rows() if registry is None else registry))
def execute(a=None,q=None,*,original_clients=True):
 a=make(structural_revision=True) if a is None else a;q=E.standard_request(label='CURRENT_TEST_CLOCK') if q is None else q
 s=a.build_snapshot(q);accept=a.accept(q,s)
 clients=[consume(a.service,s)['material'],evaluate(a.service,s,PROPOSALS)['material']] if original_clients else []
 receipt=a.serve(q,accept,s,consumers=clients)
 return a,q,s,accept,receipt

def direct_at07(direction,variant=None):
 c=AT07.build_provider_case(direction,variant=variant)
 p=provide_empirical_possibility_slice(repository=c['source']['repo'],empirical_query=c['empirical_query'],predicate=c['predicate'],authority_registry=c['registry'],release_refs=c['release_refs'],consumer_query=c['consumer_query'],model_rule=c['model_rule'],condition_binding_witness=c['condition_binding_witness'])
 evidence=p.generated_evidence_or_null;comp=p.composition_result;consumer=p.consumer_result_or_null
 return dict(provider_state=p.provider_state,producer_fact_state=comp.producer_fact_state,producer_fact_ref=comp.producer_fact_ref.as_dict(),evidence_ref=None if evidence is None else evidence.evidence_ref.as_dict(),geometry=None if evidence is None else canonicalize(evidence.geometry),raw_denominator=comp.raw_denominator_support,consumer_state=None if consumer is None else consumer.result_state,consumer_evidence_ref=None if consumer is None else consumer.exact_evidence_ref.as_dict(),identity_is_actual_composition_object=evidence is comp.possibility_slice_evidence_or_null,source_universe_ref=c['consumer_query'].source_universe_ref.as_dict(),release_ref=c['consumer_query'].release_ref.as_dict(),measure_scope='SYNTHETIC_TEST_ONLY; RAW_UNWEIGHTED; uncertainty is owner state, no invented sampling interval',uncertainty=None if evidence is None else evidence.uncertainty_state)

def f6_products():
 f=R/'inherited/F6M';sys.path.insert(0,str(f/'inherited/F6C/02_TESTS'))
 import f6c_worlds as W
 name='rawlsing_next.pre553_heterogeneous_synthesis';spec=importlib.util.spec_from_file_location(name,f/'candidate/rawlsing_next/pre553_heterogeneous_synthesis.py');M=importlib.util.module_from_spec(spec);sys.modules[name]=M;spec.loader.exec_module(M)
 out={}
 for name,world in [('world_a',W.world_a()),('world_b',W.world_b())]:
  bundle=M.synthesize(*world);conditional=M.conditional(bundle,{'material_security':'secure'},'employment_position')
  out[name]=dict(input_target=world[0],input_sources=world[1],input_policy=world[2],native_bundle=bundle,native_conditional_consumer=conditional,comparison_naive_pooled_distribution=W.naive_pooled_mixture(world[1]),comparison_ceiling='COUNTEREXAMPLE_ONLY_NOT_ESTIMAND_OR_PRODUCT',ceiling='F6M_I2_METHOD_CANDIDATE__NO_INSTALL')
 cases=json.loads((f/'inherited/F6L/02_PHASE_A/01_WORLDS_AND_EXACT_EXPECTATIONS.json').read_text())['worlds'];index={x['case']:x for x in cases}
 for case in ['P1_ORIGINAL_UNCOVERED_WORLD','P8_DISTRIBUTED_SUPPORT_MIN_150_SOURCE_EXCLUDED']:
  w=index[case];bundle=M.synthesize(w['target'],w['sources'],w['policy'],admit=lambda *_:True)
  out[case]=dict(input_target=w['target'],input_sources=w['sources'],input_policy=w['policy'],native_bundle=bundle,native_conditional_consumer=M.conditional(bundle,{},bundle['candidate']['construct_topology'][-1]),ceiling='F6M_I2_METHOD_CANDIDATE__NO_INSTALL')
 return out

def product():
 counts=collections.Counter();compositions=[];n10e=[]
 def trace(frame,event,arg):
  mod=frame.f_globals.get('__name__','');name=frame.f_code.co_name
  if event=='call' and (mod.startswith('rawlsing_next') or mod.startswith('product') or mod=='e05_n9_selected_world_adapter'):
   counts[(mod,name,frame.f_code.co_filename)]+=1
  if event=='return' and arg is not None and name=='compose_positioned_subject_possibility' and mod=='rawlsing_next.pre553_analytical_composition':
   e=arg.possibility_slice_evidence_or_null
   compositions.append(dict(producer_fact_ref=arg.producer_fact_ref.as_dict(),state=arg.producer_fact_state,denominator=arg.raw_denominator_support,evidence_ref=None if e is None else e.evidence_ref.as_dict(),geometry=None if e is None else canonicalize(e.geometry),composition_hash=arg.composed_result_identity_hash))
  if event=='return' and arg is not None and name=='provide_empirical_possibility_slice' and mod=='rawlsing_next.pre553_empirical_possibility_provider':
   e=arg.generated_evidence_or_null;n10e.append(dict(state=arg.provider_state,evidence_ref=None if e is None else e.evidence_ref.as_dict(),same_composition_evidence_object=e is arg.composition_result.possibility_slice_evidence_or_null))
 sys.setprofile(trace)
 try:
  cases={};a,q,s,acc,base=execute();cases['current_rule_revision']=base
  cases['historical_rule']=execute(q=E.standard_request(label='HISTORICAL_AS_OF'))[-1]
  relabel=copy.copy(q) # only the external display label changes; the request stays exact
  cases['same_rule_relabel_control']=execute(q=relabel)[-1]
  cases['label_only_control']=dict(before_display_label='WP2 current access rule',after_display_label='Renamed access rule',before_receipt_hash=base['receipt_hash'],after_receipt_hash=cases['same_rule_relabel_control']['receipt_hash'],model_request_unchanged=q.binding()==relabel.binding())
  cases['changed_empirical_law']=execute(make(empirical_changed=True,structural_revision=True))[-1]
  cases['zero_support']=execute(make(support_loss=True,structural_revision=True))[-1]
  # Native independently authorized reverse target, never inversion.
  reverse=E.N9SelectedWorldRequest(**{**q.__dict__,'empirical_target':'A','empirical_conditions':(('Y',1),)})
  cases['reverse_native_role']=execute(q=reverse,original_clients=False)[-1]
  opposite=E.N9SelectedWorldRequest(**{**q.__dict__,'empirical_conditions':(('A',0),('B',1),('C',1))})
  cases['opposite_condition']=execute(q=opposite,original_clients=False)[-1]
  # Same service after selective structural and empirical invalidation.
  for scope in ['training_access','empirical']:
   aa,qq,ss,ac,before=execute();invalidation=aa.invalidate(scope)
   clients=[consume(aa.service,ss)['material'],evaluate(aa.service,ss,PROPOSALS)['material']]
   after=aa.serve(qq,ac,ss,consumers=clients)
   cases['revoked_'+scope]=dict(before=before,invalidation=invalidation,after=after)
  for role in [GSS,NCA]:
   aa,qq,ss,ac,before=execute();rr=rows();next(x for x in rr if x['role']==role)['status']='REVOKED_TEST_ONLY';aa.registry=TestOnlyRegistry(rr)
   after=aa.serve(qq,ac,ss,consumers=[consume(aa.service,ss)['material'],evaluate(aa.service,ss,PROPOSALS)['material']])
   cases['source_family_revoked_'+role]=dict(before=before,after=after)
  # Native validity/publication selection: same valid date before revision publication.
  early=E.N9SelectedWorldRequest(**{**q.__dict__,'clock':E.SelectedWorldClock('AS_OF','2027-05-01','2027-05-01')})
  cases['effective_but_unpublished_revision']=execute(q=early)[-1]
  at07={d:direct_at07(d) for d in ['forward','reverse']};at07['changed_forward']=direct_at07('forward',AT07.CHANGED_SOURCE_VARIANT)
  f6=f6_products()
 finally:sys.setprofile(None)
 # Native consumer outputs carried unchanged. This envelope adds no model.
 generic=dict(contract='WP2_GENERIC_WORLD_INPUT_UNINSTALLED@1',state='UNINSTALLED_TEST_ONLY_PORT',world_receipt_hash=base['receipt_hash'],nonparent_consumer=base['consumers'][0],f6_sidecars={k:dict(bundle_hash=v['native_bundle']['content_hash'],conditional=v['native_conditional_consumer']) for k,v in f6.items()},join_state='NO_AUTHORIZED_COMMON_WORLD_OR_RESPONDENT_JOIN',actor_knowledge_time='NOT_REQUESTED_NO_ACTOR_OWNER',actor_executions=0,model_calls=0,hold=HOLD)
 return dict(terminal='OWNER_CHAIN_PARTIAL_WITH_EXACT_HOLD',hold=HOLD,installation=False,cases=cases,at07_native_2x2=at07,f6_sourcefree=f6,generic_read_only_input=generic,actual_C1_returns=compositions,actual_N10E_returns=n10e,call_counts=[dict(module=k[0],function=k[1],file=k[2],count=v) for k,v in sorted(counts.items())],edge_statuses=[dict(edge='C11/I03→C1/N10E→F8',status='NATIVE_SOURCEFREE_OWNER_VALUE_CONSUMED'),dict(edge='M4/M5→E05R selected-world→NONPARENT_OPTIONS and finite proposal client',status='NATIVE_SOURCEFREE_OWNER_VALUE_CONSUMED; MODELED_TEST_ONLY_CONTEXT'),dict(edge='independent source A/B→F6M→native conditional',status='NATIVE_SOURCEFREE_OWNER_VALUE_CONSUMED; F6M_I2_METHOD_CANDIDATE__NO_INSTALL'),dict(edge='F6M→installed selected-world binding',status='UNINSTALLED_TEST_ONLY_PORT; no common joint or issuer'),dict(edge='N9→competent N10W structural-route model/use',status='NAMED_N10W_RULE_HOLD')])

def import_manifest():
 indexed={}
 for name in ['staged_manifest.json','selected_manifest.json','supplement_manifest.json']:
  for row in json.loads((R/'discovery'/name).read_text()):indexed[str((R/row['path']).resolve())]=row
 imports=[]
 for name,module in sorted(sys.modules.items()):
  file=getattr(module,'__file__',None)
  if not file:continue
  path=Path(file).resolve()
  if not path.is_relative_to(R) or path.suffix!='.py':continue
  b=path.read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();row=indexed.get(str(path))
  if row:assert blob==row['blob'],(file,blob,row['blob'])
  imports.append(dict(module=name,file=str(path),git_blob=blob,sha256=hashlib.sha256(b).hexdigest(),source=None if row is None else dict(commit=row['commit'],path=row['source']),kind='WP2_TRANSPORT' if row is None else 'EXACT_INHERITED_NATIVE'))
 return dict(sealed_startup='5940793fbf87373dccd99dbc95973785a2b85aee',imports=imports)
if __name__=='__main__':
 p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);result=product();p.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n');p.with_suffix('.imports.json').write_text(json.dumps(import_manifest(),indent=2)+'\n');print(result['terminal'],len(result['actual_C1_returns']),'native C1 returns')
