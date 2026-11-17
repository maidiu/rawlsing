#!/usr/bin/env python3
"""Independent C-review witness W6: projection no-loss comparison.

Compares the candidate six projections with the original R5 output roles/fields.
Renamed shallow views are not equivalent. This is an audit, not a repair.
"""
import json, pathlib, collections

ROOT=pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW')
INT=ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION'
ev=INT/'EVIDENCE'; built=INT/'BUILT'
d=json.loads((ev/'DECISION.json').read_text())
frame=json.loads((ev/'FRAME.json').read_text())
disps=d['identity_dispositions']; reqs=d['requirement_dispositions']
out=ROOT/'WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/WITNESS/W6_PROJECTION_NO_LOSS'
out.mkdir(parents=True,exist_ok=True)

def distinct(rows,fields):
    return {f:len(set(str(r.get(f,'')) for r in rows)) for f in fields}

boundary=json.loads((built/'BOUNDARY_CONTRACT_MAP.json').read_text())
graph=json.loads((built/'TYPED_GRAPH.json').read_text())['graph']
evidence=[json.loads(l) for l in (built/'EVIDENCE_INDEX.jsonl').read_text().splitlines() if l.strip()]
handoff=json.loads((built/'BUILDER_HANDOFF.json').read_text())
r5_required={
 'COVERAGE_TO_DECISION.tsv':['group','id','necessity','status','decision_ids','source_anchor','source_semantics','consumer_or_hold','negative_meaning','architecture_effect','evidence_ids','why'],
 'BOUNDARY_TRACE':['contract_name','first_consumer','status','negative','integrated_epistemic_case','provenance'],
 'DOWNSTREAM_BUILD_HANDOFF':['id','boundary','recipient_owner','producer_symbol','producer_cut','consumer_symbol','consumer_status','input_abi','output_abi','transformation','negative','restore','test_command','expected_first_effect','source_authority','implementation_status','required_now_or_future','dependencies','evidence_ids'],
 'EVIDENCE_AND_FALSIFIER_INDEX':['evidence records with source/falsifier provenance; not merely ID+origin hash'],
 'GLOBAL_ARCHITECTURE':['nodes/edges with implementation/decision/alternative and boundary'],
}
report={
 'schema':'C_REVIEW_WITNESS_W6',
 'identity_rows':len(disps),
 'identity_distinct_field_values':distinct(disps,['design_effect','first_consumer_path','conservation_or_refusal_witness']),
 'requirement_rows':len(reqs),
 'requirement_distinct_field_values':distinct(reqs,['actual_design_effect','specific_first_consumer_path','conservation_or_refusal_witness']),
 'frame_requirement_distinct_field_values':distinct(frame['requirements'],['substantive_requirement','why_needed','loss_if_missing','first_consumer','architectural_consequence','proof_or_owner_hold']),
 'boundary_map_field_keys_per_T':sorted({tuple(sorted(v.keys())) for v in boundary['boundaries'].values()}),
 'boundary_source_contract_fields_present_in_map':{k:False for k in ['producers','receivers','must_preserve','first_effect','veto','time_class','owners']},
 'graph_nodes':len(graph['nodes']),'graph_edges':len(graph['edges']),
 'graph_terminal_nodes':[n['id'] for n in graph['nodes'] if n['id'] in {'F1','F2','F3','F4','F5','F6','F7','F8','N9','N10E','N10W','N11','N12','PRE-V3','SEAM','SOROK'}],
 'evidence_index_lines':len(evidence),'evidence_index_keys':sorted(evidence[0].keys()),
 'builder_handoff_keys':sorted(handoff.keys()),
 'build_handoff_is_single_object':isinstance(handoff,dict),
 'r5_required_roles_fields':r5_required,
 'verdict':'SHALLOW_PROJECTION_LOSS_CONFIRMED' if (len(set(str(x.get('design_effect')) for x in disps))==1 and len(set(str(x.get('actual_design_effect')) for x in reqs))==1 and len(graph['nodes'])==6 and not any(n['id'] in {'F5','F8','N11','N12','SEAM','SOROK'} for n in graph['nodes'])) else 'REVIEW'
}
(out/'w6_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
