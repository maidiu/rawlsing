"""Independent paired contrasts; reuse newly executed blinded receipts."""
import json,os
from pathlib import Path
from copy import deepcopy
ROOT=Path(__file__).resolve().parent;OUT=ROOT/'evidence/f2_blinded'
actual={f'F2-{i:03}':json.loads((OUT/f'F2-{i:03}.json').read_text()) for i in (1,2,3,5,7,8)}
def contrasts(receipts):
    def observable(r):return [r.get(k) for k in ('status','code','history_material_hash','admissible_routes','accessible_readset','owner_effect_committed')]
    return dict(label_invariance=observable(receipts['F2-001'])==observable(receipts['F2-002']),
        material_history=receipts['F2-001'].get('history_material_hash')!=receipts['F2-003'].get('history_material_hash'),
        practical_offer=receipts['F2-001'].get('admissible_routes')!=receipts['F2-005'].get('admissible_routes'),
        actual_hearing=receipts['F2-007'].get('accessible_readset')!=receipts['F2-008'].get('accessible_readset'))
constant={k:deepcopy(actual['F2-001']) for k in actual}
cosmetic=deepcopy(constant)
for k,r in cosmetic.items():r['history_material_hash']='LABEL_'+('renamed' if k=='F2-002' else 'same')
result=dict(actual=contrasts(actual),constant=contrasts(constant),cosmetic_label_only=contrasts(cosmetic),oracle_called=False)
assert all(result['actual'].values())
assert not all(result['constant'].values()) and not all(result['cosmetic_label_only'].values())
(ROOT/'evidence/independent_mutation_controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
