from __future__ import annotations
import hashlib, importlib.util, json, platform
from pathlib import Path
HERE=Path(__file__).resolve().parent
QIDS=['question_impl.phase0.03ea3430fb4f08a1f0da','question_impl.phase0.068ef710ac1c269b8adf']
PAIR='aefe3477977a0b443bdf173b5d3866a0cc8d256a5937fa4c7af1107efa98ce07'
WVS='2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d'; LITS='7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09'
ORDER=['WVS7::OP001','WVS7::OP002','WVS7::OP003','WVS7::OP004','WVS7::OP005','WVS7::OP006','WVS7::OP020','WVS7::OP021','WVS7::OP022','LiTS-I::OP001','LiTS-I::OP002','LiTS-I::OP003','LiTS-I::OP004','LiTS-I::OP005','LiTS-I::OP006','LiTS-I::OP020','LiTS-I::OP021','LiTS-I::OP022']
def cbytes(x): return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()
def sha_file(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1<<20),b''): h.update(b)
 return h.hexdigest()
p=json.loads((HERE/'01_R6A_R6B_SPLICE_PAYLOAD.json').read_text())
assert p['schema']=='RAWLSING_EE_R6A_FOUR_CELL_SPLICE_PAYLOAD@1.0.0'
assert [x['slot_id'] for x in p['slots']]==ORDER[2:6]
for x in p['slots']:
 assert x['frozen_qids']==QIDS and x['frozen_pair_newline_stream_sha256']==PAIR and x['source_sha256']==WVS
 y=dict(x); claimed=y.pop('profile_content_sha256'); assert hashlib.sha256(cbytes(y)).hexdigest()==claimed
r=json.loads((HERE/'02_18_CELL_READINESS_RECEIPT.json').read_text())
assert r['selection_floor']['ready_count']==18 and r['selection_floor']['pending_count']==0 and r['selection_floor']['ready_cells']==ORDER
assert r['candidate_operation_physical_cells']=={'ready':27,'total':27}
b=json.loads((HERE/'03_EXECUTION_SURFACE_BLOCKER.json').read_text())
assert sha_file('/mnt/data/ee_r7a/WVS Wave 7.sav')==WVS and sha_file('/mnt/data/ee_r7a/LITS-2006-data.dta')==LITS
assert importlib.util.find_spec('pyreadstat') is None and importlib.util.find_spec('pyarrow') is None
assert platform.python_version()=='3.13.5'
c=json.loads((HERE/'04_FINAL_COMPARISON_EVIDENCE.json').read_text())
assert c['status'].startswith('NOT_EXECUTED') and not c['performance_numbers_generated'] and not c['ranking_or_winner_emitted']
print(json.dumps({'status':'PASS','splice_slots':4,'ready_cells':18,'pending_cells':0,'source_hashes_verified':2,'runtime_blocker_verified':True,'candidate_processes_launched':0,'performance_numbers_generated':False,'ranking':False},sort_keys=True))
