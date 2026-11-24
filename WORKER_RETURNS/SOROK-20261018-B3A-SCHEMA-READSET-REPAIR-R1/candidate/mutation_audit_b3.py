"""Falsify deliberately bad adapters using contrasts in actual B3 execution receipts."""
from copy import deepcopy
import json
from materialize import ROOT,dump
from integration import digest

def check(results):
 errors=[]
 def proj(r):return {k:r[k] for k in ('original_event_hash','material_actor_activity','admissible_routes','history_material_hash','accessible_readset') }|{'practical_actions':r['CAN008_response']['practical_actions']}
 if proj(results['F2-001'])!=proj(results['F2-002']):errors.append('COSMETIC_LABEL_CAUSALITY')
 if results['F2-001']['history_material_hash']==results['F2-003']['history_material_hash']:errors.append('CONSTANT_MATERIAL_HISTORY')
 if ('JOINT_PRACTICAL_ACTION_POSSIBLE' in results['F2-001']['admissible_routes'])==('JOINT_PRACTICAL_ACTION_POSSIBLE' in results['F2-005']['admissible_routes']):errors.append('CONSTANT_MATERIAL_OFFER')
 if results['F2-007']['accessible_readset']==results['F2-008']['accessible_readset']:errors.append('CONSTANT_SPEECH_ACCESS')
 return errors

def main():
 ids=['F2-001','F2-002','F2-003','F2-005','F2-007','F2-008']
 actual={i:json.loads((ROOT/'evidence/f2'/f'{i}.json').read_text()) for i in ids}
 assert check(actual)==[]
 constant={i:deepcopy(actual['F2-001']) for i in ids}
 cosmetic=deepcopy(actual);cosmetic['F2-002']['CAN008_response']['practical_actions']=['LABEL_IMPOSED_CHECK']
 outcomes={name:dict(killed=bool(check(rows)),failed_contrasts=check(rows)) for name,rows in [('constant',constant),('cosmetic_label_only',cosmetic)]}
 assert all(row['killed'] for row in outcomes.values())
 dump(ROOT/'evidence/b3_mutation_receipt.json',dict(actual_adapter_contrasts='PASS',mutants=outcomes,reference_oracle_used=False,actual_receipt_hashes={i:digest(r) for i,r in actual.items()}))
 print(json.dumps(outcomes,sort_keys=True))
if __name__=='__main__':main()
