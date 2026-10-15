"""Measure original producer function calls; no monkeypatch or fake estimator."""
import pathlib,sys,json,os,collections
from port.adapter import TwoContractAdapter
from port.provider_a import ProviderA
from port.provider_b import ProviderB
from rawlsing_next import pre553_analytical_composition as C
from rawlsing_next import pre553_empirical_possibility_provider as N
from rawlsing_next import pre553_postastra_pe_generic_world_possibility as P
from rawlsing_next.tests.test_postastra_pe_fixture import law_a_cases
RET=pathlib.Path(os.environ['RC0_RETURN']);files={pathlib.Path(m.__file__).resolve():name for name,m in [('C1',C),('N10E',N),('PE',P)]};calls=collections.Counter()
def trace(frame,event,arg):
 if event=='call':
  p=pathlib.Path(frame.f_code.co_filename).resolve()
  if p in files:calls[(files[p],frame.f_code.co_name)]+=1
sys.setprofile(trace)
bundle=TwoContractAdapter(ProviderA()).run();bundle_b=TwoContractAdapter(ProviderB()).run();sys.setprofile(None);port_calls=[dict(module=k[0],function=k[1],calls=v) for k,v in calls.items()]
assert port_calls==[]
case=law_a_cases()['multi_binding_parent_context'];calls.clear();sys.setprofile(trace)
result=P.serve_generic_world_situated_possibility(repository=case['repository'],empirical_query=case['empirical_query'],predicate=case['predicate'],authority_registry=case['registry'],release_refs=case['release_refs'],request=case['request'],model_rule=case['model_rule'],condition_binding_witness=case['witness'])
sys.setprofile(None);assert result.result_state=='EXACT_SUPPORTED' and calls[('C1','compose_positioned_subject_possibility')]>0
control=[dict(module=k[0],function=k[1],calls=v) for k,v in calls.items()]
out=dict(port_producer_calls=port_calls,PE_positive_control_calls=control,PE_state=result.result_state,port_consumer_count=len(bundle['consumer_effects']),port_providers_traced=['ProviderA','ProviderB'],conclusion='PORT_USES_STATIC_TEST_ONLY_EMPIRICAL_HINT; LEGACY_PE_C1_RUN_IS_SEPARATE_POSITIVE; NO_PORT_TO_PINNED_EMPIRICAL_PRODUCER_LINK_PROVED')
(RET/'repro/connection_probe.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
