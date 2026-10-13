import hashlib,json,pathlib,subprocess
OUT=pathlib.Path(__file__).resolve().parent;C=OUT/'composite'
def git(*a):return subprocess.check_output(['git',*a])
checks=[]
def verify(commit,path,local):
 raw=git('show',commit+':'+path);actual=local.read_bytes();assert actual==raw
 checks.append(dict(commit=commit,path=path,local=str(local),git_blob=git('rev-parse',commit+':'+path).decode().strip(),sha256=hashlib.sha256(raw).hexdigest(),exact=True))
for p in ['rawlsing_next/pre553_selected_world_progressive_contract.py','rawlsing_next/pre553_n9_n10w_progressive_candidate.py','rawlsing_next/tests/test_pre553_selected_world_progressive_contract.py','rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py']:verify('c98e888166a941a06ad694411911bc58f9c4639b',p,C/p)
for p in ['rawlsing_next/pre553_i01_sourcefree_world_lifecycle_candidate.py','rawlsing_next/tests/test_hq288_i01r_independent_product.py']:verify('473b7997d1b446c54a2d8688f94053b6c8670881',p,C/p)
verify('aba2f6a60d21b8daeeaf9eb3cfadef2620ac13f4','rawlsing_next/r3_s02_seam_witness.py',C/'rawlsing_next/r3_s02_seam_witness.py')
rows=json.loads(git('show','5e6e802f5f13e559a5b5c781ab6fa4ceb3cc97da:WORKER_RETURNS/PYAT-R3-HQ289-S00V2-SOURCEFREE-PRODUCER-BINDING-R1/repro/frozen_custody.json'))
for r in rows:verify(r['commit'],r['path'],C/r['local'])
for p in ['rawlsing_next/tests/test_r3_s02_seam_witness.py','rawlsing_next/tests/test_hq286_s00e_s00cr_overlay.py']:verify('aba2f6a60d21b8daeeaf9eb3cfadef2620ac13f4',p,C/p)
for p in ['rawlsing_next/tests/test_hq290_s00v3r_offline_custody_method.py','WORKER_RETURNS/PYAT-R3-HQ290-S00V3R-OFFLINE-CUSTODY-METHOD-R1/01_FROZEN_OFFLINE_ORACLES.json']:verify('d4967c2f00b60d496a9c8a78714cf47fb0035953',p,C/p)
(OUT/'exact_custody_checks.json').write_text(json.dumps(checks,indent=2)+'\n');print('exact Git custody checks',len(checks))
