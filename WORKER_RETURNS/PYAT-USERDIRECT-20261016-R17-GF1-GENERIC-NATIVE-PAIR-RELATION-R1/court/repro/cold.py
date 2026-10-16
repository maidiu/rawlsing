from pathlib import Path
import sys,os,json,subprocess,hashlib,shutil
from collections import Counter
R=Path(__file__).resolve().parents[1];RT=R/'runtime_root';root=RT/'pv3_final_cold';root.mkdir(exist_ok=False)
def call(mode,path=root,tag=None):
 tag=tag or 'cold_'+mode;p=subprocess.run([sys.executable,str(R/'repro/cold_child.py'),str(path),mode,tag],capture_output=True,text=True)
 (R/f'observations/{tag}.stdout').write_text(p.stdout+p.stderr);return {'mode':mode,'path':str(path),'pid_record':str(R/f'observations/{tag}.audit.json'),'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
first=call('first');assert first['exit']==0,first
before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'ledger').rglob('*') if p.is_file()}
replay=call('replay');assert replay['exit']==0,replay
after={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'ledger').rglob('*') if p.is_file()}
read=call('current_read',tag='cold_forged_current_grant');assert read['exit']==0
missing=call('missing_source',tag='cold_missing_source')
edition=call('changed_edition',tag='cold_changed_edition')
tamper=root.parent/'pv3_final_cold_receipt_tamper';shutil.copytree(root,tamper)
journal=next((tamper/'ledger').rglob('b01e_side_effects.jsonl'));lines=journal.read_text().splitlines();row=json.loads(lines[0]);row['PV2I_TAMPERED_RECEIPT_PAYLOAD']={'n':999};lines[0]=json.dumps(row,sort_keys=True);journal.write_text('\n'.join(lines)+'\n');tampered=call('replay',tamper,'cold_tampered_receipt')
a=json.loads((R/'observations/cold_first.audit.json').read_text());b=json.loads((R/'observations/cold_replay.audit.json').read_text())
f=json.loads((root/'observations/first.json').read_text());r=json.loads((root/'observations/replay.json').read_text())
out={'first':first,'replay':replay,'actual_owner_calls_first':dict(Counter(c['function'] for c in a['calls'])),'actual_owner_calls_replay':dict(Counter(c['function'] for c in b['calls'])),'distinct_pids':a['pid']!=b['pid'],'same_ledger_bytes':before==after,'ledger_before':before,'ledger_after':after,'links_exact':f['links']==r['links'],'held_exact':f['nonrunnable']==r['nonrunnable'],'register_exact':f['pv2_register']==r['pv2_register'],'no_new_durable_units':all(x['run']['executed']==[] for x in r['owner_reports']),'original_expected_persisted_before_first_owner':all(c['expected_file_exists'] for c in a['calls']),'fresh_forged_current_grant':json.loads((R/'observations/cold_forged_current_grant.json').read_text()),'missing_source':missing,'changed_edition':edition,'tampered_receipt':tampered}
(R/'observations/cold_court.json').write_text(json.dumps(out,indent=2)+'\n');print('TRUE_PROCESSES',out['distinct_pids'],'EXACT_JOURNAL',out['same_ledger_bytes'],'NEW_DURABLE_ZERO',out['no_new_durable_units']);print('ACTUAL_OWNER_REPLAY',out['actual_owner_calls_replay']);print('ATTACK_EXITS',missing['exit'],edition['exit'],tampered['exit'])
