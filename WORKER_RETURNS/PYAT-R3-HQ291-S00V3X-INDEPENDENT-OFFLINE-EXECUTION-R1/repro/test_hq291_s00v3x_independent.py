"""New reviewer hostiles, frozen before execution and before author-test inspection."""
import copy,hashlib,json,os,subprocess,sys
from pathlib import Path
from dataclasses import replace
from fractions import Fraction
import pytest
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I
S=I.seam
OUT=Path(__file__).resolve().parent
ARTIFACT='a5d1146a5bc0182a0232b1f59dda9ea78a35b4c42096c2fc938fc0cd8ebd7606'
SELECTOR='cfce198d628298bbc5b4fa46d820f3d2354181c17cb13db3dd29f18d48763cfa'

def rehash(b,**kw):
 b=replace(b,content_hash='',**kw);return replace(b,content_hash=S._content_hash(b.as_dict()))
def compute(b):
 c=S.ContractOnlySeamConsumer(b);r=c.compute_scenario('S00V3X',[S.P04_STEPS[0]] if b.world_scope.get('target') is None else ['P_Q86A_given_Q86B_1']);return r,c.get_receipt()
def deny(monkeypatch):
 def f(*a,**kw):raise AssertionError('producer executed on saved serve')
 for mod,names in [(I.selected,['select_world','run_selected_world_progressive_chain']),(I.progressive,['build_synthetic_world','run_progressive_chain']),(S,['build_sociological_bundle','build_source_free_native_joint_bundle','select_world','build_synthetic_world','run_progressive_chain'])]:
  for name in names:monkeypatch.setattr(mod,name,f)

def test_independent_p04_commitments_derive_from_preexisting_durable_bytes():
 raw=subprocess.check_output(['git','show','473b7997d1b446c54a2d8688f94053b6c8670881:WORKER_RETURNS/PYAT-R3-HQ288-I01R-CROSSOWNER-PRODUCT-INDEPENDENT-R1/repro/product/artifacts/'+ARTIFACT+'.json'])
 assert hashlib.sha256(raw).hexdigest()==ARTIFACT
 b=I.bundle_from_payload(json.loads(raw));law=replace(b,content_hash='').as_dict();law.pop('bundle_id')
 assert S._content_hash(law)=='a621c7d80ad801f82da84c0f89346032d91aed26f45d125a2df6291329265576'==S._P04_OFFLINE_LAW_SHA256
 assert I.selected.contract_content_hash(b.selected_world_contract)=='f323c7206f97d58b47fdd8f391b9614680fd699cc24e90f61c3fcde91eb6758c'==S._P04_OFFLINE_ROOT_SHA256

@pytest.mark.parametrize('native',[False,True])
def test_coherent_stale_roots_with_every_local_geometry_check_green(native,monkeypatch):
 b=S.build_source_free_native_joint_bundle({(0,0):3,(0,1):1,(1,0):1,(1,1):3}) if native else S.build_sociological_bundle()
 step='P_Q86A_given_Q86B_1' if native else S.P04_STEPS[0];d=4 if native else 32;yes=2 if native else 17
 channels=[]
 for ch in b.channels:
  if ch.value['step_id']==step:
   v=dict(ch.value);n=yes if v['cell']=='1' else d-yes;f=Fraction(n,d);v.update(raw_numerator_support=n,raw_probability_exact_fraction={'$exact_fraction':[f.numerator,f.denominator]});ch=replace(ch,value=v)
  channels.append(ch)
 steps=copy.deepcopy(list(b.steps))
 for st in steps:
  if st['step_id']==step:
   for cell,n in [('0',d-yes),('1',yes)]:
    st['cells'][cell]['numerator']=n
    if 'fraction' in st['cells'][cell]:
     f=Fraction(n,d);st['cells'][cell]['fraction']={'$exact_fraction':[f.numerator,f.denominator]}
 b=rehash(b,channels=tuple(channels),steps=tuple(steps));c=S.ContractOnlySeamConsumer(b)
 assert c._validate_complete_domain() is None and c._validate_fraction_closure() is None and c._validate_step_geometry() is None
 deny(monkeypatch);r,receipt=compute(b)
 assert r['reason']=='PRODUCER_VALUE_IDENTITY_MISMATCH' and receipt.values_read==[]

def test_after_actual_restore_saved_bytes_are_the_only_numerical_inputs(tmp_path,monkeypatch):
 p,_=I.build_product(tmp_path);expected=I.serve(p);restored=I.restore_product(tmp_path);payload=I.load_artifact(tmp_path,p.subject_ref)
 assert restored.calls==[]
 observed=[];native=S.ContractOnlySeamConsumer
 def spy(bundle):observed.append(bundle.as_dict());return native(bundle)
 deny(monkeypatch);monkeypatch.setattr(S,'ContractOnlySeamConsumer',spy)
 assert I.serve(restored)==expected and observed==[payload['bundle']]
 I.artifact_path(tmp_path,p.subject_ref).unlink()
 with pytest.raises(I.I01Error,match='UNAVAILABLE'):I.serve(restored)

@pytest.mark.parametrize('field',['release_ref','selection_key_ref','selected_receipt'])
def test_forged_saved_release_and_selector_are_refused(tmp_path,field):
 p,_=I.build_product(tmp_path);path=tmp_path/'product_index.json';data=json.loads(path.read_text())
 if field=='selected_receipt':data[field]['selected_release_ref']=p.subject_ref.as_dict()
 else:data[field]=p.subject_ref.as_dict()
 I.save_json(path,data)
 try:
  q=I.restore_product(tmp_path);I.serve(q)
 except Exception as e:
  assert isinstance(e,ValueError) or type(e).__name__ in {'StopIteration','KeyError'},type(e).__name__
 else:pytest.fail('forged index accepted')

@pytest.mark.parametrize('attack',['selector','p04_code'])
def test_frozen_court_rejects_selector_or_code_substitution(tmp_path,attack):
 selector=tmp_path/'selector.json';raw=(OUT/'SOURCE_SELECTOR.json').read_bytes();selector.write_bytes(raw)
 env={**os.environ,'PYAT_S00V3R_SELECTOR':str(selector),'PYAT_S00V3R_SELECTOR_SHA256':SELECTOR}
 if attack=='selector':
  data=json.loads(raw);data['candidate_commit']='0'*40;selector.write_text(json.dumps(data))
 else:
  import shutil
  root=tmp_path/'substituted';shutil.copytree(OUT/'composite/rawlsing_next',root/'rawlsing_next')
  path=root/'rawlsing_next/pre553_selected_world_progressive_contract.py';path.write_bytes(path.read_bytes()+b'\n# forged P04\n')
  env['PYAT_S00V3R_COMPOSITE_ROOT']=str(root)
 proc=subprocess.run([sys.executable,'-m','pytest',str(OUT/'test_hq290_s00v3r_offline_custody_method.py'),'-q','-k','O14','-p','no:cacheprovider'],env=env,cwd=tmp_path,capture_output=True,text=True)
 assert proc.returncode!=0
 assert ('SELECTOR_ATTESTATION_MISMATCH' if attack=='selector' else 'pre553_selected_world_progressive_contract.py') in proc.stdout
 (tmp_path/'attack_stdout.txt').write_text(proc.stdout+proc.stderr)
