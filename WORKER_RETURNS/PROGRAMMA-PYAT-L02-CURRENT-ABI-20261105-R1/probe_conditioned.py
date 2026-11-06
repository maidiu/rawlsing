"""Named four-item forward/reverse qualification over unchanged current R01/R03."""
from pathlib import Path
from dataclasses import replace
from tempfile import TemporaryDirectory
from itertools import permutations
import json
from collections import Counter
from rawlsing_next.tests.test_universal_source_projection import write_rows,package
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceRule,materialize_native_preimages
from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.tests.test_universal_grammar import _inventory,_occurrence,_policy,_frontier
from rawlsing_next.universal_grammar.types import DirectionGrant
from rawlsing_next.pre553_universal_workload import compile_governed_frontier,execute_governed_frontier
NAMES=('income_band','access_code','route_choice','eligibility_group')
# Same respondents, asymmetric group sizes: 12 exposed, 4 unexposed.
ROWS=[]
for group,repeats in [(1,3),(0,1)]:
 for a in (0,1):
  for b in (0,1):
   for repeat in range(repeats):
    ROWS.append(dict(zip(NAMES,(float(a),float(b),float(a^b),float(group))),exposure_clock=0.0))

def run(consumer_hook=None):
 outputs=[]
 with TemporaryDirectory() as directory:
  path=Path(__file__).with_name('sourcefree-four-item.sav')
  if not path.exists():write_rows(path,ROWS)
  pkg=package(path,len(ROWS),tuple(NativeSourceRule('impl.'+n,n) for n in NAMES),coordinate='exposure_clock')
  bundle=materialize_native_preimages(package=pkg,incidence=decode_sav(path))
  for direction in ('FORWARD','REVERSE'):
   targets=NAMES[:3] if direction=='FORWARD' else NAMES[3:]
   conditioners=NAMES[3:] if direction=='FORWARD' else NAMES[:3]
   occurrences=tuple(_occurrence(n,target_role='OUTCOME' if n in targets else None,conditioner_role='EXPOSURE' if n in conditioners else None) for n in NAMES)
   inventory=replace(_inventory(occurrences,complete=True),source_sha256=bundle.source_sha256)
   policy=_policy(j=len(targets),k=len(conditioners),d=1)
   grants=list(policy.direction_grants)
   for arity in range(1,len(targets)+1):
    for depth in range(len(conditioners)+1):
     for claim in ('DIST','CONDITIONAL','JOINT','CO_TRAVEL','INTERACTION','FORK'):
      grants.append(DirectionGrant(('OUTCOME',)*arity,('EXPOSURE',)*depth,claim,f'L02-{direction}-{arity}-{depth}-{claim}'))
   # Avoid duplicate grants already present in the inherited fixture policy.
   unique={ (g.target_roles,g.conditioner_roles,g.claim_class):g for g in grants }
   policy=replace(policy,direction_grants=tuple(unique.values()))
   frontier=_frontier(inventory,policy)
   compilation=compile_governed_frontier(bundle=bundle,inventory=inventory,policy=policy,frontier=frontier,as_of='2026-10-23',host='local-r03',purpose='TEST_ONLY_SOURCEFREE')
   result=execute_governed_frontier(compilation=compilation,source_factory=lambda _:bundle.physical_stream)
   assert result.operation_anti_join['no_drop_ok']
   # Freeze actual native objects so later consumer binding uses these exact facts.
   if consumer_hook is not None:
    consumer_hook(direction,bundle,compilation,result)
   ledger=result.ledger()
   selected={op.op_id:op for op in frontier.operations if tuple(k.item_id for k in op.targets)==targets and len(op.conditions)==len(conditioners) and op.measure_kind=='SAMPLE' and op.claim_class==('JOINT' if direction=='FORWARD' else 'CONDITIONAL')}
   rows=[r for r in result.operation_ledger if r['operation_id'] in selected]
   outputs.append(dict(direction=direction,selected_operation_rows=rows,ledger=ledger))
 return outputs
if __name__=='__main__':
 output=run()
 Path(__file__).with_suffix('.json').write_text(json.dumps(output,sort_keys=True,default=str,indent=2)+'\n')
 print(json.dumps([{ 'direction':o['direction'],'selected':len(o['selected_operation_rows']),'states':sorted({r['lowering_status'] for r in o['selected_operation_rows']})} for o in output]))
