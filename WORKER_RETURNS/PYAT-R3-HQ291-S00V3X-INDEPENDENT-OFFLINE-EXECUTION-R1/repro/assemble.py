import subprocess,pathlib,hashlib,json
ROOT=pathlib.Path(__file__).resolve().parents[3]; OUT=pathlib.Path(__file__).resolve().parent; C=OUT/'composite'
I='473b7997d1b446c54a2d8688f94053b6c8670881'; V='aba2f6a60d21b8daeeaf9eb3cfadef2620ac13f4'; R='d4967c2f00b60d496a9c8a78714cf47fb0035953'; V2='5e6e802f5f13e559a5b5c781ab6fa4ceb3cc97da'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def show(commit,path):return git('show',commit+':'+path)
manifest=[]
def copy(commit,path,target=None):
 raw=show(commit,path);dest=C/(target or path);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
 manifest.append(dict(path=str(dest.relative_to(C)),origin_commit=commit,origin_path=path,git_blob=git('rev-parse',commit+':'+path).decode().strip(),sha256=hashlib.sha256(raw).hexdigest()))
paths=git('ls-tree','-r','--name-only',I).decode().splitlines()
# Exact accepted I01R Python source tree, no later branch modules.
for p in paths:
 if p.startswith('rawlsing_next/') and p.endswith('.py') and '/tests/' not in p:copy(I,p)
 if p.startswith('WORKER_RETURNS/PYAT-R3-HQ287-I01-SOURCEFREE-INTEGRATED-WORLD-LIFECYCLE-R1/repro/') and (p.endswith('.py') or '/product/' in p):copy(I,p)
copy(V,'rawlsing_next/r3_s02_seam_witness.py')
for p in ['rawlsing_next/tests/test_hq288_i01r_independent_product.py','rawlsing_next/tests/test_pre553_selected_world_progressive_contract.py','rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py','rawlsing_next/tests/test_r3_s02_seam_witness.py','rawlsing_next/tests/test_hq286_s00e_s00cr_overlay.py']:copy(I,p)
copy(R,'rawlsing_next/tests/test_hq290_s00v3r_offline_custody_method.py')
copy(R,'WORKER_RETURNS/PYAT-R3-HQ290-S00V3R-OFFLINE-CUSTODY-METHOD-R1/01_FROZEN_OFFLINE_ORACLES.json')
copy(V2,'rawlsing_next/tests/test_hq289_s00v2_count_derived_acceptance.py')
F='WORKER_RETURNS/PYAT-R3-HQ289-S00V2-SOURCEFREE-PRODUCER-BINDING-R1/repro/'
for p in git('ls-tree','-r','--name-only',V2,F+'frozen',F+'historical_runtime').decode().splitlines():copy(V2,p)
# Original frozen court retained as immutable evidence as well as runnable composite.
for p in ['rawlsing_next/tests/test_hq290_s00v3r_offline_custody_method.py','WORKER_RETURNS/PYAT-R3-HQ290-S00V3R-OFFLINE-CUSTODY-METHOD-R1/01_FROZEN_OFFLINE_ORACLES.json']:
 (OUT/pathlib.Path(p).name).write_bytes(show(R,p))
(OUT/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
required=['rawlsing_next/r3_s02_seam_witness.py','rawlsing_next/pre553_i01_sourcefree_world_lifecycle_candidate.py','rawlsing_next/pre553_selected_world_progressive_contract.py','rawlsing_next/pre553_n9_n10w_progressive_candidate.py']
selector=dict(schema='PYAT_HQ290_S00V3R_TEST_SELECTOR@1',candidate_commit=V,reviewed_root_kind='ISOLATED_COMPOSITE_I01R_PLUS_SEAM',source_sha256={p:hashlib.sha256((C/p).read_bytes()).hexdigest() for p in required})
(OUT/'SOURCE_SELECTOR.json').write_text(json.dumps(selector,indent=2)+'\n')
print(json.dumps(selector,indent=2));print('selector_sha256',hashlib.sha256((OUT/'SOURCE_SELECTOR.json').read_bytes()).hexdigest());print('modules',len(manifest))
