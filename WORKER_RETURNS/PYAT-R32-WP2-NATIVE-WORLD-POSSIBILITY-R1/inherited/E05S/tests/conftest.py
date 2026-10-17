import sys,json,hashlib,pathlib,collections,pytest
R=pathlib.Path(__file__).resolve().parents[1];RT=R/'runtime';O=R/'observations'
sys.path[:0]=list(map(str,[RT,RT/'rawlsing_next/tests',RT/'rawlsing_next',R/'repro']))
COUNTS=collections.Counter();CALLS=[]
def profile(frame,event,arg):
 if event!='call':return
 fn=frame.f_code.co_filename
 if str(RT) not in fn:return
 module=frame.f_globals.get('__name__','');name=frame.f_code.co_name
 COUNTS[(module,name,fn,frame.f_code.co_firstlineno)]+=1
 if len(CALLS)<300 and (module.startswith('product') or name in ['resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','execute_empirical_query','read_historical_test_only']):CALLS.append(dict(module=module,function=name,file=fn,line=frame.f_code.co_firstlineno))
@pytest.fixture(scope='session',autouse=True)
def capture():
 sys.setprofile(profile)
 yield
 sys.setprofile(None)
 manifest=json.loads((R/'source_manifest.json').read_text());by_local={str(RT/x['local']):x for x in manifest};mods=[]
 for name,m in sorted(sys.modules.items()):
  f=getattr(m,'__file__',None)
  if f and str(RT) in f:
   b=pathlib.Path(f).read_bytes();blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();src=by_local.get(f)
   assert src and src['git_blob']==blob,(name,f)
   mods.append(dict(module=name,file=f,git_blob=blob,sha256=hashlib.sha256(b).hexdigest(),source_commit=src['commit'],source_path=src['path']))
 out=dict(imported_modules=mods,actual_call_counts=[dict(module=k[0],function=k[1],file=k[2],line=k[3],count=v) for k,v in sorted(COUNTS.items())],ordered_call_sample=CALLS,method='sys.setprofile observes original function calls without wrappers, mocks or source edits')
 (R/'02_ACTUAL_M4_M5_N9C_E04_NATIVE_OWNER_TRACE.json').write_text(json.dumps(out,indent=2)+'\n')
