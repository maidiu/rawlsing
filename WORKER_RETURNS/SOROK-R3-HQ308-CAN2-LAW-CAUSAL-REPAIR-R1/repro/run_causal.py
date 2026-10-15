"""Execute byte-identical RCP3 instrumentation, report actual fixed controls."""
from pathlib import Path
import sys,json,re
RET=Path(__file__).resolve().parents[1];sys.path.insert(0,str(RET/'runtime_root/court_repaired/repro'))
from causal_probe import observe
tag=sys.argv[1] if len(sys.argv)>1 else ''
if tag and not re.fullmatch('[A-Za-z0-9_-]+',tag):raise SystemExit('Use an alphanumeric fresh tag')
out=RET/'evidence'/('causal_'+tag if tag else 'causal');out.mkdir(exist_ok=False)
runs={}
for mode in ('baseline','published_control','actual_absent_effect','physical_absent_effect','corrupt_stored_effect','forged_issuer','unadmitted','fake_event_hash'):
 runs[mode]=observe(mode)
 (out/(mode+'.json')).write_text(json.dumps(runs[mode],indent=2)+'\n')
again=observe()
a=runs['baseline']['result'];assert a['full_replay_digest']==again['result']['full_replay_digest']
assert a['later_event_response']['effect_kind']=='DEFLECT'
for mode in ('published_control','actual_absent_effect','physical_absent_effect'):
 r=runs[mode]['result'];assert r['terminal']=='CHAIN_COMPLETE' and r['later_event_response']['effect_kind']=='AMPLIFY' and r['later_event_response']['prior_effect_read'] is False
for mode in ('forged_issuer','unadmitted','fake_event_hash'):
 assert runs[mode]['result']['terminal']=='FIRST_EVENT_REFUSED' and runs[mode]['ledger_entries'][0]==[]
assert runs['corrupt_stored_effect']['result']['terminal']=='LATER_EVENT_REFUSED'
summary=dict(exact_replay=True,digest=a['full_replay_digest'],baseline=a['later_event_response'],controls={n:runs[n]['result'].get('later_event_response') for n in ('published_control','actual_absent_effect','physical_absent_effect')},refusals={n:runs[n]['result']['code'] for n in ('corrupt_stored_effect','forged_issuer','unadmitted','fake_event_hash')},actual_candidate_state=a['state_hash'],owner_hold=a['production_owner_hold'],public_hold=a['public_standing_hold'],sourcefree_only=True)
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
