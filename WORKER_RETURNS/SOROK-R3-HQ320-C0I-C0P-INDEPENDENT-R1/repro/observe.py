"""Independent positive named clients and AS_OF receipts; exact original calls."""
from stage import R
from pathlib import Path
import sys,json,hashlib
sys.path.insert(0,str(R/'staging/runtime'))
from product.service import GenericSelectedWorldService
from product import nonparent,scenario
from rawlsing_next.pre553_empirical_objects import semantic_hash
s=GenericSelectedWorldService();ss=s.select(mode='AS_OF',valid_at='2027-09-01',published_asof='2027-09-01')
a=nonparent.consume(s,ss,budget_tokens=5);b=scenario.evaluate(s,ss,[dict(scenario_id='S1',route='institutional'),dict(scenario_id='S2',route='civil')])
orig=json.loads((R/'staging/c0p/observations/two_contract_receipts.json').read_text())
assert a['receipt_hash']==orig['receipt_A_NONPARENT_APPRENTICESHIP']['owner_receipt_hash'] and b['receipt_hash']==orig['receipt_B_CONCEPTION_CONTEXT_PROPOSALS']['owner_receipt_hash']
assert ss.snapshot_hash==orig['snapshot_ref']
for rec in [a,b]:assert semantic_hash(rec['material'])==rec['receipt_hash']
c=GenericSelectedWorldService(structural_revision=True);clock=[]
for valid,pub in [('2027-09-01','2026-06-01'),('2026-06-01','2027-09-01'),('2027-09-01','2027-09-01')]:
 q=c.select(mode='AS_OF',valid_at=valid,published_asof=pub);clock.append(dict(snapshot=q.material,snapshot_hash=q.snapshot_hash,nonparent=nonparent.consume(c,q),mother=scenario.evaluate(c,q,[dict(scenario_id='S1',route='institutional'),dict(scenario_id='S2',route='civil')])))
result=dict(schema='C0I_FRESH_NAMED_NATIVE_CONSUMERS@1',sourcefree=True,snapshot=ss.material,snapshot_hash=ss.snapshot_hash,nonparent=a,mother=b,exact_original_receipt_hashes_reproduced=True,structural_native_trace=s.catalog.trace,empirical_native_trace=s.provider.trace,asof_clock_rectangle=clock,source_ceilings=dict(grade='SYNTHETIC_NOT_OBSERVED',original_respondents=False,person_generation=False,scenario_selection_model=None,operative_N9=False),owner_grain='These are two distinct downstream consumer receipts. N9 selection is ss; N10E/C1/F8 evidence is nested. Distinct client hashes alone do not prove two exposed transport contracts.')
out=R/'evidence/positive';out.mkdir(parents=True,exist_ok=True);(out/'native_named_receipts.json').write_text(json.dumps(result,indent=2,default=str)+'\n')
print('EXACT_NATIVE_POSITIVES',a['receipt_hash'],b['receipt_hash'],'same_snapshot',ss.snapshot_hash,'clock_rectangles',len(clock))
