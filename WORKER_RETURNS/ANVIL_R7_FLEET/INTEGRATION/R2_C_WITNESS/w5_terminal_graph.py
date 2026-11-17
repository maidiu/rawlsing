#!/usr/bin/env python3
"""Independent C-review witness W5: the actual typed graph payload.

The instrument names 16 terminal identities in the 118 inventory, but the
DECISION whole_machine_graph contains only six generic nodes and none of the
16 terminal IDs. The candidate gate and C graph audit still pass. This is a
terminal16-name-vs-producer-graph loss, not a missing label.
"""
import json, pathlib, sys

ROOT = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/INTEGRATION/WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION/R2_C_WITNESS_OUTPUT')
INT = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/INTEGRATION/WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION')
COLD = pathlib.Path('/var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/anvil-c-reviewr2-f47lroa6')
TOOLS = COLD/'ANVIL_R7/tools'
sys.path.insert(0, str(TOOLS))
from r7_integrated import check  # noqa: E402

REPO='/Users/matthewsmith/s2b-work/rawlsing'
ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
ev=INT/'EVIDENCE'; source=ev/'SOURCE_118'
frame=json.loads((ev/'FRAME.json').read_text())
decision=json.loads((ev/'DECISION.json').read_text())
c=json.loads((ev/'C.json').read_text())
inv=json.loads((ev/'SOURCE_IDENTITY_INVENTORY.json').read_text())
g=decision['whole_machine_graph']
nodes={n['id'] for n in g['nodes']}
terminal=[e['id'] for e in inv['entries'] if e['group']=='TERMINAL']
missing=[t for t in terminal if t not in nodes]
# Also show that only seven boundary edges exist and no terminal/FF/SEAM/SOROK node is named.
fr=check('FRAME',frame,ev,source,REPO,ZIP)
de=check('DECISION',decision,ev,source,REPO,ZIP)
cc=check('C_INTEGRATED',c,ev,source,REPO,ZIP)
report={
 'schema':'C_REVIEW_WITNESS_W5',
 'graph_nodes':sorted(nodes),'graph_edges':len(g['edges']),
 'terminal_ids_in_inventory':terminal,
 'terminal_ids_in_graph':[t for t in terminal if t in nodes],
 'terminal_ids_missing_from_graph':missing,
 'terminal_mentions_anywhere_in_graph':{t:json.dumps(g).count('"'+t+'"') for t in terminal},
 'FRAME':fr,'DECISION':de,'C_INTEGRATED':cc,
 'C_graph_audit':c.get('graph_audit'),
 'verdict':'WITNESS_CONFIRMED_IF_GATE_PASS_AND_MISSING_TERMINALS_NONEMPTY' if de['status'].startswith('PASS') and cc['status'].startswith('PASS') and missing else 'WITNESS_REFUTED'
}
out=pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/INTEGRATION/WORKER_RETURNS/ANVIL_R7_FLEET/INTEGRATION/R2_C_WITNESS_OUTPUT/W5_TERMINAL_GRAPH')
out.mkdir(parents=True,exist_ok=True)
(out/'w5_result.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
