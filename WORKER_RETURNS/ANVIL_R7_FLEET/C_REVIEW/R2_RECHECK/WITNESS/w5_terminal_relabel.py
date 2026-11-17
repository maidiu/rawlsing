#!/usr/bin/env python3
"""R2 recheck W5 witness: a terminal graph can be relabeled from an exact owner
hold to a generic 'NAMED_TYPED_CONSUMER_OR_OWNER_HOLD' while the C terminal_audit
still claims an exact hold. Counts, edges and all 16 names remain unchanged."""
import json, pathlib, shutil, sys, tempfile

R2 = pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/C_REVIEW/WORKER_RETURNS/ANVIL_R7_FLEET/C_REVIEW/R2_RECHECK')
TS=(R2/'LOGS/STAMP').read_text().strip(); PKG=R2/f'COLD/FRESH_{TS}/ANVIL_R7'; TOOLS=PKG/'tools'
sys.path.insert(0,str(TOOLS))
from r7_integrated import check, digest, sha  # noqa: E402
REPO='/Users/matthewsmith/s2b-work/rawlsing'; ZIP='/Users/matthewsmith/Desktop/ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip'
OUT=R2/'WITNESS/W5_TERMINAL_RELABEL'; OUT.mkdir(parents=True,exist_ok=True)
tmp=pathlib.Path(tempfile.mkdtemp(prefix='w5_',dir=str(OUT))); ev=tmp/'EVIDENCE'; shutil.copytree(PKG/'EVIDENCE',ev); source=ev/'SOURCE_118'
frame=json.loads((ev/'FRAME.json').read_text()); decision=json.loads((ev/'DECISION.json').read_text()); c=json.loads((ev/'C.json').read_text())
for n in decision['whole_machine_graph']['nodes']:
    if n['id']=='F5':
        n['first_consumer']='NAMED_TYPED_CONSUMER_OR_OWNER_HOLD'
        n['exact_hold']=''
        # Leave producer/authority/time/edges intact; only the hold/consumer status changes.
# Re-pin DECISION and C pointers; terminal_audit deliberately left claiming F5 exact hold.
(ev/'DECISION.json').write_text(json.dumps(decision,sort_keys=True,indent=2)+'\n')
c['integrated_decision']={'path':'DECISION.json','sha256':sha((ev/'DECISION.json').read_bytes())}
c['integrated_decision_sha256']=digest(decision)
(ev/'C.json').write_text(json.dumps(c,sort_keys=True,indent=2)+'\n')
de=check('DECISION',decision,ev,source,REPO,ZIP); cc=check('C_INTEGRATED',c,ev,source,REPO,ZIP)
report={'schema':'C_REVIEW_R2_W5_TERMINAL_RELABEL','graph_nodes':len(decision['whole_machine_graph']['nodes']),
 'graph_edges':len(decision['whole_machine_graph']['edges']),
 'F5_graph':next(n for n in decision['whole_machine_graph']['nodes'] if n['id']=='F5'),
 'C_terminal_audit_F5':c['terminal_audit']['terminal_holds']['F5'],
 'DECISION':de,'C_INTEGRATED':cc,
 'verdict':'RELABEL_CONFIRMED_IF_BOTH_PASS' if de['status'].startswith('PASS') and cc['status'].startswith('PASS') else 'RELABEL_REFUSED'}
(OUT/'w5_result.json').write_text(json.dumps(report,indent=2)+'\n'); print(json.dumps(report,indent=2))
