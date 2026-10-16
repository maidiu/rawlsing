from pathlib import Path
import json
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.pre553_batch_runner import UnitExecutionReceipt
R=Path(__file__).resolve().parents[1];root=R/'runtime_root/pv3_final_cold';rows=[]
for file in sorted((root/'ledger').rglob('b01e_checkpoint.json')):
 cp=json.loads(file.read_text())
 for record in cp['records']:
  p=dict(record['receipt_projection'])
  for k in ('unit_ref','executor_ref'):
   if p[k] is not None:p[k]=ExactRef(**p[k])
  for k in ('result_refs','provenance_refs'):p[k]=tuple(ExactRef(**x) for x in p[k])
  receipt=UnitExecutionReceipt(**p);assert receipt.receipt_hash==record['receipt_hash'];assert receipt.state=='COMPLETED';assert receipt.manifest_hash==cp['identity']['manifest_hash']
  rows.append({'checkpoint':str(file.relative_to(root)),'manifest':cp['identity']['manifest_ref'],'original_class':type(receipt).__module__+'.'+type(receipt).__name__,'receipt_hash':receipt.receipt_hash,'receipt_ref':receipt.receipt_ref.as_dict(),'preimage':receipt.projection()})
assert len(rows)==6
(R/'observations/verified_original_owner_receipt_preimages.json').write_text(json.dumps(rows,indent=2)+'\n');print('SIX_ORIGINAL_ACCEPTED_UNIT_RECEIPT_PREIMAGES_AND_HASHES_VERIFIED')
