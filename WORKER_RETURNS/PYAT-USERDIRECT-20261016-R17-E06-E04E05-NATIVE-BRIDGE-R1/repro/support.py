from bootstrap import ROOT,RT
import json
from copy import deepcopy
from bridge import NativeBridge
import e05_n9_selected_world_adapter as E
from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot,canonicalize
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_hq297_n9c_two_field_reader import TestOnlyRegistry,GSS,NCA

def rows():return json.loads((RT/'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json').read_text())['fields']
def request(label='CURRENT_TEST_CLOCK',**kw):return E.standard_request(label=label,**kw).binding()
def bridge(**kw):return NativeBridge(rows(),enabled=True,**kw)
def grants(w):return (*w['source']['authorities'],w['qauth'])
def hydrate(d):return AuthoritySnapshot(typed_state=d['typed_state'],authority_snapshot_refs=d['authority_snapshot_refs'],dependency_refs=d['dependency_refs'],producer_replay_locator_or_reference_root=d['producer_replay_locator_or_reference_root'],**d['semantic_fields'])
def clone(a,**changes):
 d=a.as_dict();d['semantic_fields'].update(changes);d['typed_state']=d['semantic_fields']['decision_state'];return hydrate(d)
def support(receipt):return [(next(c['raw_numerator_support'] for c in s['cells'] if c['cell']=='1'),s['denominator']) for s in receipt['empirical_steps']]
