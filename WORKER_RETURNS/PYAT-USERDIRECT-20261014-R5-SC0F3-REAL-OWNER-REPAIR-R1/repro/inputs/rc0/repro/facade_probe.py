import copy,json,os,pathlib
from port.adapter import TwoContractAdapter
from port.provider_a import ProviderA
bundle=TwoContractAdapter(ProviderA()).run();mutated=copy.deepcopy(bundle)
mutated['facade']['consumer_effects']={}
result=TwoContractAdapter.round_trip_two_contracts(mutated)
out=dict(probe='RC0_FACADE_SCOPE',original_consumer_count=len(bundle['facade']['consumer_effects']),facade_consumer_count_after_mutation=0,two_receipt_checker_result=result,classification='CHECKER_COVERS_TWO_RECEIPTS_ONLY; DO_NOT_PROMOTE_TO_FULL_CONSUMER_EFFECT_TRANSPORT_PROOF',reviewer_expectation_limit='No claim that a method named two_contracts authenticates arbitrary outer consumer effects; separate carrier acceptance needs an explicit effect round-trip check')
(pathlib.Path(os.environ['RC0_RETURN'])/'repro/facade_probe.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
