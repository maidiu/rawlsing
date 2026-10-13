import hashlib,json,pathlib,subprocess,sys
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I
OUT=pathlib.Path(__file__).resolve().parent;root=OUT/'product';root.mkdir(exist_ok=True)
p,report=I.build_product(root);before=I.serve(p)
assert p.subject_ref.content_hash=='a5d1146a5bc0182a0232b1f59dda9ea78a35b4c42096c2fc938fc0cd8ebd7606'
assert p.release.ref.content_hash=='582317a6731c43d84959f7d0e74604f30bba4d49f3fe114f1afb07f63108d22a'
I.save_json(root/'execution_summary.json',report);I.save_json(root/'served_before.json',before)
code="""import json,sys
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I
counts={}
for mod,name in [(I.selected,'select_world'),(I.progressive,'build_synthetic_world')]:
 native=getattr(mod,name)
 def spy(*a,_native=native,_name=name,**kw):counts[_name]=counts.get(_name,0)+1;return _native(*a,**kw)
 setattr(mod,name,spy)
p,report=I.build_product(sys.argv[1]);assert p.calls==[] and report['executed']==[]
def deny(*a,**kw):raise AssertionError('PRODUCER_ON_POST_RESTORE_SERVE')
for mod,names in [(I.selected,['select_world','run_selected_world_progressive_chain']),(I.progressive,['build_synthetic_world','run_progressive_chain']),(I.seam,['build_sociological_bundle','build_source_free_native_joint_bundle','build_synthetic_world','run_progressive_chain','select_world'])]:
 for name in names:setattr(mod,name,deny)
if sys.argv[2]=='historical':
 try:I.serve(p)
 except I.I01Error as e:assert 'NO_CURRENT' in str(e)
 else:raise AssertionError('current resurrected')
 result=I.serve(p,historical=True)
else:result=I.serve(p)
print(json.dumps(dict(result=result,durable_callbacks=p.calls,executed=report['executed'],restore_setup_calls=counts),sort_keys=True))
"""
records=[]
for mode in ['current','historical']:
 if mode=='historical':I.save_json(root/'invalidation_receipt.json',I.invalidate(p))
 cmd=[sys.executable,'-c',code,str(root),mode];proc=subprocess.run(cmd,capture_output=True,text=True);(OUT/('product_'+mode+'.log')).write_text(proc.stdout+proc.stderr);assert proc.returncode==0,proc.stderr
 observed=json.loads(proc.stdout);assert observed['result']['numeric_result']==before['numeric_result'] and observed['result']['consumer_receipt']==before['consumer_receipt']
 I.save_json(root/('fresh_'+mode+'.json'),observed);records.append(dict(argv=cmd,cwd=str(pathlib.Path.cwd()),exit=proc.returncode))
(OUT/'product_commands.json').write_text(json.dumps(records,indent=2)+'\n');print(json.dumps(dict(artifact=p.subject_ref.as_dict(),release=p.release.ref.as_dict(),fresh_process_durable_callbacks=0,restore_setup_calls=observed['restore_setup_calls']),indent=2))
