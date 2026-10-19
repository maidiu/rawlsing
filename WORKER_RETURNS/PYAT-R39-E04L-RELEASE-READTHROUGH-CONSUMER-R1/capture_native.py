"""Record actual call edges and source imports; export only sourcefree fixture evidence."""
from pathlib import Path
import hashlib,json,sys,subprocess
import bootstrap
from fixture import prepare
from readthrough import execute
R=Path(__file__).resolve().parent;W=R.parents[1]
calls=[]
names={'execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','adjudicate_learned_empirical','constitute_release','register_product','publish_product','select_current','resolve_selection_exact','resolve_release_exact','compose_learned_world','consume','possibilities','resolve','step'}
def profile(frame,event,arg):
    if event=='call' and frame.f_code.co_name in names:
        p=Path(frame.f_code.co_filename).resolve()
        if p.is_relative_to(W):calls.append(dict(module=frame.f_globals.get('__name__'),function=frame.f_code.co_name,path=str(p.relative_to(W))))
sys.setprofile(profile)
p=prepare();service,receipt=execute(p)
sys.setprofile(None)
imports=[]
for name,module in sorted(sys.modules.items()):
    if name=='rawlsing_next' or name.startswith('rawlsing_next.') or name=='product' or name.startswith('product.'):
        location=getattr(module,'__file__',None)
        if location is None:continue
        path=Path(location).resolve();assert path.is_relative_to(W)
        data=path.read_bytes();relative=str(path.relative_to(W))
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if path.is_relative_to(R):
            row=next(x for x in json.loads((R/'source_manifest.json').read_text()) if R/x['local']==path)
            assert blob==row['blob_sha1'];commit=row['commit'];sourcepath=row['path']
        else:
            commit='2e6c189fd54b818556a44419b19691938ea76d5a';sourcepath=relative
            assert data==subprocess.check_output(['git','show',commit+':'+relative],cwd=W)
        imports.append(dict(module=name,module_file=relative,commit=commit,path=sourcepath,blob_sha1=blob,sha256=hashlib.sha256(data).hexdigest()))
bindings=[x['learned_release_binding'] for x in receipt['material']['values_read'] if x['channel']=='empirical']
result=dict(schema='E04L_ACTUAL_NATIVE_READTHROUGH_CAPTURE_R1',receipt=receipt,calls=calls,imports=imports,release_ref=p.composition.m2_artifacts.release.ref.as_dict(),subject_ref=p.composition.m1_disposition.ref.as_dict(),selection_ref=p.composition.b5_selection_receipt.ref.as_dict(),i4_receipt_ref=p.composition.receipt.ref.as_dict(),bindings=bindings,source_rows_hash=p.native_provider.world['rows_hash'],no_actor_or_model_calls=True)
output=R/'evidence/native_capture.json';output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(receipt_hash=receipt['receipt_hash'],release_ref=result['release_ref'],call_count=len(calls),import_count=len(imports)),sort_keys=True))
