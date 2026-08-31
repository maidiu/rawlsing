#!/usr/bin/env python3
"""Deterministic, fail-closed W55B governance-packet checker (non-serving tooling)."""
import argparse,csv,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
STATE=ROOT/'CENTRAL_PROJECT_STATE_R1'
def ids(name,key):
 with (STATE/name).open() as f:return {r[key] for r in csv.DictReader(f,delimiter='\t')}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('packet');p=json.load(open(ap.parse_args().packet))
 states=ids('PROJECT_STATE.tsv','state_id'); obligations=ids('OPEN_OBLIGATIONS.tsv','obligation_id')
 g=p.get('grounding_receipt',{}); w=p.get('work_return',{}); canonical=p.get('canonical_project_head','564feddf4228759aed970f42061aeae4e6b96478')
 checks={
 'GROUNDING_PASS': bool(g) and g.get('grounding_complete_for_declared_scope')=='PASS',
 'CANONICAL_PROJECT_HEAD_MATCH': g.get('canonical_project_head')==canonical and g.get('central_state_head_match')=='PASS',
 'GROUND_VERSION_MATCH':g.get('ground_version')=='RAWLSING_GROUND_R1',
 'KNOWN_STATE_IDS':set(g.get('relevant_state_ids',[])).issubset(states),
 'KNOWN_OBLIGATION_IDS':set(g.get('relevant_obligation_ids',[])).issubset(obligations),
 'AUTHORITY_CEILING_DECLARED':bool(g.get('authority_ceiling')),
 'RETURN_DESTINATION_DECLARED':bool(g.get('required_return_destination')),
 'TOUCHED_OBLIGATIONS_DISPOSITIONED':all(x.get('obligation_id') in obligations and x.get('disposition') for x in w.get('touched_obligation_dispositions',[])),
 'NEW_OBLIGATIONS_REGISTERED':all(x in obligations for x in w.get('new_obligations',[])),
 'SUCCESSOR_RETURN_PATH_DECLARED':not w.get('spawned_successors') or bool(w.get('return_to_ids')),
 'REINTEGRATION_STATUS_VALID':w.get('reintegration_status') not in ('PROJECT_CLOSED',''),
 'ANTI_RESURRECTION_ACKNOWLEDGED':bool(g.get('anti_resurrection_constraints')),
 }
 if g.get('agent_mode')=='DELIBERATELY_UNGROUNDED_EXPLORATION': checks['GROUNDING_PASS']=False
 out={'checks':checks,'overall':'PASS' if all(checks.values()) else 'FAIL'};print(json.dumps(out,sort_keys=True));return 0 if out['overall']=='PASS' else 1
if __name__=='__main__':sys.exit(main())
