#!/usr/bin/env python3
"""Runnable frozen-payload witness for semantic/width truth closure gaps."""
from __future__ import annotations
import gzip,json
from pathlib import Path
B=Path('/Users/matthewsmith/Desktop/ANVIL_ENGINEERING_EXECUTION_20261117/MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_SCALE_QUALIFICATION_20261118')
SC=B/'SEMANTIC_CLOSURE'; W=B/'WIDTH128'
t=json.loads((SC/'EXPECTED_TRUTH.json').read_text()); r=json.loads((SC/'RESULT.json').read_text())
semantic={}
for label,v in t['operations'].items():
 semantic[label]={'truth_full_expected_sets':all(k in v for k in ('expected_denominator_members','expected_risk_members')),'truth_keys':sorted(v.keys()),'result_row_has_identity_lists':all(k in next(x for x in r['operations'] if x['label']==label) for k in ('risk_set_member_refs','denominator_member_refs'))}
width_r=json.loads((W/'RESULT.json').read_text()); width_p=json.loads(gzip.decompress((W/'f4.payload.json.gz').read_bytes()))
act={c['cell']:c for c in width_p['semantic_fields']['target_topology']['complete_cell_semantic_projection']}; exp={c['cell']:c for c in width_r['expected']['cells']}
width={'actual_cells':sorted(act),'expected_cells':sorted(exp),'actual_zero_cell':act.get('1'),'expected_zero_cell':exp.get('1'),'checks_cells_declared':width_r['checks']['cells'],'all_expected_declared':width_r['all_expected_match'],'raw_stdout_all_expected':json.loads((W/'query.json').read_text())['stdout'].split('"all_expected": ')[-1].split(',')[0].strip()}
out={'semantic_closure':{'operations':semantic,'derive_expected_requires_result_identity_lists':True,'defect':'EXPECTED_TRUTH has no expected full member sets; RESULT rows have counts/hashes only, while derive_expected.py line 45 indexes row[risk_set_member_refs]/denominator_member_refs; full identity-set proof is absent and the derivation is not runnable against the frozen RESULT.','raw_stdout_all_expected':json.loads((SC/'SUPERVISION.json').read_text())['stdout'].split('"all_expected": ')[-1].split(',')[0].strip(),'result_all_expected':r['all_expected_match']},'width128':width,'defect_present':True}
print(json.dumps(out,indent=2,sort_keys=True));raise SystemExit(1)
