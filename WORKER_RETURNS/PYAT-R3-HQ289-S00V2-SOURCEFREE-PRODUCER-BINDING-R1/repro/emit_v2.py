"""Retain actual generated source-free laws, outputs and value-used receipts."""
from dataclasses import replace
import json,pathlib,sys
from rawlsing_next import r3_s02_seam_witness as S
OUT=pathlib.Path(__file__).resolve().parent
joint={(0,0):3,(0,1):1,(1,0):1,(1,1):3}
records={}
for label,b,steps in [('p04',S.build_sociological_bundle(),list(S.P04_STEPS)),('native_base',S.build_source_free_native_joint_bundle(joint),['P_Q86A_given_Q86B_1']),('native_new',S.build_source_free_native_joint_bundle({**joint,(1,0):2,(1,1):2}),['P_Q86A_given_Q86B_1']),('native_unrelated_new',S.build_source_free_native_joint_bundle({**joint,(0,0):5,(0,1):7}),['P_Q86A_given_Q86B_1']),('zero',S.build_source_free_native_joint_bundle({**joint,(1,0):0,(1,1):0}),['P_Q86A_given_Q86B_1'])]:
 c=S.ContractOnlySeamConsumer(b);r=c.compute_scenario('v2_'+label,steps)
 contract=b.selected_world_contract
 records[label]={'bundle':b.as_dict(),'selected_contract':dict(contract_id=contract.contract_id,world_tag=contract.world_tag,source_universe_ref=contract.source_universe_ref.as_dict(),release_ref=contract.release_ref.as_dict(),risk_set_ref=contract.risk_set_ref.as_dict(),selection_metadata=dict(contract.selection_metadata),real_current=contract.real_current),'result':r,'receipt':c.get_receipt().as_dict()}
records['acceptance_version']=S.SOURCE_FREE_VALUE_ACCEPTANCE_VERSION
(OUT/'v2_product.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps({'version':S.SOURCE_FREE_VALUE_ACCEPTANCE_VERSION,'base':records['native_base']['result']['exact_probabilities'],'new':records['native_new']['result']['exact_probabilities'],'old_release':records['native_base']['selected_contract']['release_ref'],'new_release':records['native_new']['selected_contract']['release_ref'],'zero':records['zero']['result']},sort_keys=True))
