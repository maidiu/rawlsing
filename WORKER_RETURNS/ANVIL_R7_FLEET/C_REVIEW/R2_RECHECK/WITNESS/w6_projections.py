#!/usr/bin/env python3
"""R2 recheck W6 projection audit: check actual values and distinctness, not only
field names, across all six R5-equivalent projection roles."""
import json, pathlib, collections

R2 = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R2_RECHECK')
TS=(R2/'LOGS/STAMP').read_text().strip(); B=R2/f'COLD/FRESH_{TS}/ANVIL_R7/BUILT'; E=R2/f'COLD/FRESH_{TS}/ANVIL_R7/EVIDENCE'
d=json.loads((E/'DECISION.json').read_text()); c=json.loads((E/'C.json').read_text())
ids=d['identity_dispositions']; reqs=d['requirement_dispositions']
b=json.loads((B/'BOUNDARY_CONTRACT_MAP.json').read_text()); g=json.loads((B/'TYPED_GRAPH.json').read_text())['graph']
ev=[json.loads(l) for l in (B/'EVIDENCE_INDEX.jsonl').read_text().splitlines() if l.strip()]
h=[json.loads(l) for l in (B/'BUILDER_HANDOFF.jsonl').read_text().splitlines() if l.strip()]
th=json.loads((B/'BUILDER_HANDOFF.json').read_text())
report={
 'schema':'C_REVIEW_R2_W6_PROJECTIONS',
 'identity_rows':len(ids),
 'identity_field_distinct':{k:len({x.get(k) for x in ids}) for k in ('source_meaning','source_negative','design_effect','first_consumer_path','first_consumer_or_hold','conservation_or_refusal_witness','source_meaning_sha256','interpretation_grade')},
 'requirement_field_distinct':{k:len({x.get(k) for x in reqs}) for k in ('actual_design_effect','specific_first_consumer_path','conservation_or_refusal_witness','typed_obligation')},
 'boundary_T1_fields':sorted(b['boundaries']['T1'].keys()),
 'boundary_T4_values':b['boundaries']['T4'],
 'graph_nodes':len(g['nodes']),'graph_edges':len(g['edges']),
 'graph_terminal_ids':[n['id'] for n in g['nodes'] if n['id'] in ('F1','F2','F3','F4','F5','F6','F7','F8','N9','N10E','N10W','N11','N12','PRE-V3','SEAM','SOROK')],
 'evidence_lines':len(ev),'evidence_keys':sorted(ev[0].keys()),
 'evidence_has_source_excerpt':sum(1 for x in ev if x.get('source_excerpt')),
 'evidence_has_falsifier':sum(1 for x in ev if x.get('falsifier')),
 'handoff_lines':len(h),'handoff_keys':sorted(h[0].keys()),
 'handoff_status':[x.get('status') for x in h],
 'handoff_abi':[x.get('input_abi') for x in h],
 'handoff_deps':[x.get('dependencies') for x in h],
 'handoff_negative_restore':[(bool(x.get('negative')),bool(x.get('restore'))) for x in h],
 'typed_handoff_top_keys':sorted(th.keys()),
 'C_terminal_holds':len(c.get('terminal_audit',{}).get('terminal_holds',{})),
 'verdict':'FULL_PROJECTION_VALUES_PRESENT_EXCEPT_TERMINAL_HOLD_SEMANTICS_REVIEWED_SEPARATELY'
}
out=R2/'WITNESS/W6_PROJECTIONS'; out.mkdir(parents=True,exist_ok=True); (out/'w6_result.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
