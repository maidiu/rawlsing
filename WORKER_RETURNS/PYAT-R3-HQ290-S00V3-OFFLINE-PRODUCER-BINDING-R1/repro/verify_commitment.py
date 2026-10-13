"""Admission-time verification against accepted Git evidence; never service."""
import hashlib,json,pathlib,subprocess
from rawlsing_next import r3_s02_seam_witness as S
ROOT=pathlib.Path.cwd();OUT=pathlib.Path(__file__).resolve().parent
SHA='473b7997d1b446c54a2d8688f94053b6c8670881'
PATH='WORKER_RETURNS/PYAT-R3-HQ287-I01-SOURCEFREE-INTEGRATED-WORLD-LIFECYCLE-R1/repro/product/artifacts/a5d1146a5bc0182a0232b1f59dda9ea78a35b4c42096c2fc938fc0cd8ebd7606.json'
raw=subprocess.check_output(['git','show',SHA+':'+PATH]);assert hashlib.sha256(raw).hexdigest()=='a5d1146a5bc0182a0232b1f59dda9ea78a35b4c42096c2fc938fc0cd8ebd7606'
(OUT/'pinned_accepted_artifact.json').write_bytes(raw)
payload=json.loads(raw);issued=S.build_sociological_bundle()
assert issued.as_dict()==payload['bundle']
material=dict(payload['bundle']);material.pop('bundle_id');material['content_hash']=''
assert S._content_hash(material)==S._P04_OFFLINE_LAW_SHA256
assert S.contract_content_hash(issued.selected_world_contract)==S._P04_OFFLINE_ROOT_SHA256
pins=[]
for path in ['rawlsing_next/pre553_selected_world_progressive_contract.py','rawlsing_next/pre553_n9_n10w_progressive_candidate.py']:
 expected=subprocess.check_output(['git','show','c98e888166a941a06ad694411911bc58f9c4639b:'+path]);assert (ROOT/path).read_bytes()==expected
 pins.append(dict(path=path,p04_commit='c98e888166a941a06ad694411911bc58f9c4639b',blob=subprocess.check_output(['git','hash-object',path],text=True).strip(),sha256=hashlib.sha256(expected).hexdigest()))
receipt=dict(version=S.P04_OFFLINE_LAW_VERSION,law_digest=S._P04_OFFLINE_LAW_SHA256,selected_root_digest=S._P04_OFFLINE_ROOT_SHA256,custody_commit=SHA,custody_path=PATH,custody_blob=subprocess.check_output(['git','rev-parse',SHA+':'+PATH],text=True).strip(),artifact_sha256=hashlib.sha256(raw).hexdigest(),admission_replay_exact=True,normalization=['content_hash empty','bundle_id omitted','only string unrelated_test_note omitted'],producer_pins=pins,external_authentication=False)
(OUT/'commitment_custody.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,sort_keys=True))
