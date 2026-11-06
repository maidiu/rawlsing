"""Initial exact-current 3-target joint probe; sourcefree only."""
from pathlib import Path
from dataclasses import replace
from tempfile import TemporaryDirectory
import json
from rawlsing_next.tests.test_universal_source_projection import write_rows,package
from rawlsing_next.pre553_source_native_preimage_adapter import NativeSourceRule,materialize_native_preimages
from rawlsing_next.pre553_physical_decoder import decode_sav
from rawlsing_next.tests.test_universal_grammar import _inventory,_occurrence,_policy,_frontier
from rawlsing_next.universal_grammar.types import DirectionGrant
from rawlsing_next.pre553_universal_workload import compile_governed_frontier,execute_governed_frontier
names=('income_band','access_code','route_choice')
rows=[{names[0]:float(i%2),names[1]:float((i//2)%2),names[2]:float((i%2)^((i//2)%2)),'exposure_clock':0.0} for i in range(12)]
with TemporaryDirectory() as directory:
 path=Path(directory)/'respondent-linked.sav';write_rows(path,rows)
 pkg=package(path,len(rows),tuple(NativeSourceRule('impl.'+name,name) for name in names),coordinate='exposure_clock')
 bundle=materialize_native_preimages(package=pkg,incidence=decode_sav(path))
 inventory=replace(_inventory(tuple(_occurrence(n,conditioner_role=None) for n in names),complete=True),source_sha256=bundle.source_sha256)
 policy=_policy(j=3,k=0,d=1)
 policy=replace(policy,direction_grants=policy.direction_grants+(DirectionGrant(('OUTCOME',)*3,(),'JOINT','L02-JOINT3'),DirectionGrant(('OUTCOME',)*3,(),'CO_TRAVEL','L02-COTRAVEL3')))
 frontier=_frontier(inventory,policy)
 compilation=compile_governed_frontier(bundle=bundle,inventory=inventory,policy=policy,frontier=frontier,as_of='2026-10-23',host='local-r03',purpose='TEST_ONLY_SOURCEFREE')
 result=execute_governed_frontier(compilation=compilation,source_factory=lambda _:bundle.physical_stream)
 ids={op.op_id for op in frontier.operations if len(op.targets)==3 and op.claim_class=='JOINT'}
 selected=[row for row in result.operation_ledger if row['operation_id'] in ids]
 out={'sourcefree':True,'names':names,'rows':rows,'three_target_operations':selected,'anti_join':result.operation_anti_join,'ledger':result.ledger()}
 Path(__file__).with_name('probe_kway.json').write_text(json.dumps(out,sort_keys=True,default=str,indent=2)+'\n')
 print(json.dumps({'three_target_operations':len(selected),'states':sorted({r['lowering_status'] for r in selected}),'no_drop':result.operation_anti_join['no_drop_ok']}))
