from bootstrap import ROOT,RT
import json
from bridge import NativeBridge
import e05_n9_selected_world_adapter as E
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
rows=json.loads((RT/'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json').read_text())['fields']
b=NativeBridge(rows,enabled=True);p=b.prepare(E.standard_request(label='CURRENT_TEST_CLOCK').binding());a=b.read(p);w=b.provider.world
print(a['state'],[(s['denominator'],[c['raw_numerator_support'] for c in s['cells']]) for s in a['selected_world_receipt']['empirical_steps']])
w['registry']=AuthorityRegistry(w['source']['authorities']);d=b.read(p);print(d['state'],d['selected_world_receipt']['empirical_state'],len(d['actual_warm_client_denials']))
w['registry']=AuthorityRegistry((*w['source']['authorities'],w['qauth']));c=b.read(p);print('RESTORED',c['state'])
(ROOT/'observations').mkdir(exist_ok=True);(ROOT/'observations/early_positive_withdraw_restore.json').write_text(json.dumps(dict(positive=a,withdrawn=d,restored=c),indent=2)+'\n')
