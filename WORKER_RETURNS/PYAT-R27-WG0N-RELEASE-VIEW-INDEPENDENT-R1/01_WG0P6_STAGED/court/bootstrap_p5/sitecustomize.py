"""WG0M versioned import/identity transport. Enabled only via explicit PYTHONPATH.
Original reviewer tests/helpers and all author/native source bytes stay unchanged.
"""
import hashlib,importlib,importlib.util,json,pathlib,sys
R=pathlib.Path(__file__).resolve().parents[1]
P5C=R/'runtime_phase_b/p5_return/review/runtime_phase_b/candidate'
SHA='9fa1098dfbcdb011d3624eb2dbc8a7cd9578fa34'
def verify_cut():
 cut=json.loads((R/'observations/WG0P5_candidate_read_cut.json').read_text())
 if cut['candidate_sha']!=SHA or not cut['return_only']:raise RuntimeError('UNVERIFIED_WG0P5_CUT')
 for row in cut['files']:
  path=R/row['staged_path'];data=path.read_bytes()
  if hashlib.sha256(data).hexdigest()!=row['sha256']:raise RuntimeError('CHANGED_WG0P5_SOURCE:'+str(path))
 return cut
verify_cut()
sys.path[:0]=[str(P5C/'repro'),str(P5C/'pinned'),str(R/'repro')]
spec=importlib.util.spec_from_file_location('wg0p4_workload',P5C/'repro/wg0p4_workload.py')
w=importlib.util.module_from_spec(spec);sys.modules[spec.name]=w;spec.loader.exec_module(w)
import phase_b_support_v1 as support
support.C=P5C
# This replaces only the old candidate path/hash transport, not an assertion.
def physical_modules():
 verify_cut();mods={}
 pins=json.loads((P5C/'source_selector.json').read_text())['files']
 for name in ('pre553_c11_repository','pre553_c11_ingest','pre553_empirical_query','pre553_batch_runner','pre553_empirical_objects','pre553_c11_integrity'):
  m=importlib.import_module('rawlsing_next.'+name);p=pathlib.Path(m.__file__).resolve()
  if not p.is_relative_to(P5C/'pinned/rawlsing_next'):raise RuntimeError('WRONG_PHYSICAL_OWNER:'+str(p))
  data=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
  row=next(x for x in pins if x['source_path']=='rawlsing_next/'+name+'.py')
  if blob!=row['git_blob_sha1']:raise RuntimeError('WRONG_NATIVE_BLOB:'+name)
  # Also bind the accepted source back to the original court's pinned owner bytes.
  original=R/'runtime_phase_b/candidate/pinned/rawlsing_next'/(name+'.py')
  if data!=original.read_bytes():raise RuntimeError('NATIVE_OWNER_CHANGED:'+name)
  mods[name]={'file':str(p),'sha256':hashlib.sha256(data).hexdigest(),'git_blob_sha1':blob}
 return mods
support.verified_modules=physical_modules
import phase_b_adapter_v1 as adapter
adapter.Adapter.candidate_sha=SHA
# Evidence trace transport: actual names/files, accepting the nested exact source root.
def profile_calls(calls):
 def trace(frame,event,arg):
  if event=='call' and str(P5C) in frame.f_code.co_filename and frame.f_code.co_name in ('__init__','enumerate','build_executable_plan','make_executor','run_plan','run','execute_empirical_query','consumer_effects','execute_positive_conditional','build_positive_conditional_frontier'):
   calls.append({'name':frame.f_code.co_name,'file':frame.f_code.co_filename,'line':frame.f_code.co_firstlineno})
 return trace
support.profile_calls=profile_calls
# The adapter imported the old profile symbol when loaded; map its tracing only.
adapter.profile_calls=profile_calls
