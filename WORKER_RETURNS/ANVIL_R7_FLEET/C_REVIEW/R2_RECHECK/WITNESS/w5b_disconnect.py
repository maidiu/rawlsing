#!/usr/bin/env python3
"""R2 recheck W5b witness: disconnect F5 from the graph and add duplicate-typed
filler edges so node/edge counts remain 43/58. The terminal ID remains present and
the C terminal_audit still claims exact hold; the gate passes."""
import copy, json, pathlib, shutil, sys, tempfile

R2 = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R2_RECHECK')
TS=(R2/'LOGS/STAMP').read_text().strip(); PKG=R2/f'COLD/FRESH_{TS}/ANVIL_R7'; TOOLS=PKG/'tools'
sys.path.insert(0,str(TOOLS))
from r7_integrated import check, digest, sha  # noqa: E402
REPO='/Users/matthewsmith/s2b-work/rawlsing'; ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=R2/'WITNESS/W5_DISCONNECT'; OUT.mkdir(parents=True,exist_ok=True)
tmp=pathlib.Path(tempfile.mkdtemp(prefix='w5b_',dir=str(OUT))); ev=tmp/'EVIDENCE'; shutil.copytree(PKG/'EVIDENCE',ev); source=ev/'SOURCE_118'
frame=json.loads((ev/'FRAME.json').read_text()); decision=json.loads((ev/'DECISION.json').read_text()); c=json.loads((ev/'C.json').read_text())
g=decision['whole_machine_graph']
# Remove F5 edges and add two type-valid filler edges copied from an existing I03->F4 edge.
removed=[e for e in g['edges'] if e['from']=='F5' or e['to']=='F5']
g['edges']=[e for e in g['edges'] if not (e['from']=='F5' or e['to']=='F5')]
template=next(e for e in g['edges'] if e['from']=='I03' and e['to']=='F4')
for i in (1,2):
    e=copy.deepcopy(template); e['id']='E_FILL_%d'%i; g['edges'].append(e)
# Leave F5 node and C terminal_audit untouched: counts still 43/58.
(ev/'DECISION.json').write_text(json.dumps(decision,sort_keys=True,indent=2)+'\n')
c['integrated_decision']={'path':'DECISION.json','sha256':sha((ev/'DECISION.json').read_bytes())}; c['integrated_decision_sha256']=digest(decision)
(ev/'C.json').write_text(json.dumps(c,sort_keys=True,indent=2)+'\n')
de=check('DECISION',decision,ev,source,REPO,ZIP); cc=check('C_INTEGRATED',c,ev,source,REPO,ZIP)
f5_edges=[e for e in g['edges'] if e['from']=='F5' or e['to']=='F5']
report={'schema':'C_REVIEW_R2_W5_DISCONNECT','nodes':len(g['nodes']),'edges':len(g['edges']),
 'removed_F5_edges':len(removed),'remaining_F5_edges':len(f5_edges),'filler_edge_ids':['E_FILL_1','E_FILL_2'],
 'C_terminal_audit_F5':c['terminal_audit']['terminal_holds']['F5'],
 'DECISION':de,'C_INTEGRATED':cc,
 'verdict':'DISCONNECT_CONFIRMED_IF_BOTH_PASS' if de['status'].startswith('PASS') and cc['status'].startswith('PASS') else 'DISCONNECT_REFUSED'}
(OUT/'w5b_result.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
