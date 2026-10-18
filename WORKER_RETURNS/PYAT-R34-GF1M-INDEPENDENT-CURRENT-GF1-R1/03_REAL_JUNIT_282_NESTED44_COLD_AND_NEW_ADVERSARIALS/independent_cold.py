"""Independent cold source/projection evidence and exhaustive 82-case replay.
Expected labels use explicit diagonal/antidiagonal supports, not candidate labels.
"""
import os,sys,json,hashlib,importlib.util,itertools
from pathlib import Path
spec=importlib.util.spec_from_file_location('gf1m_helper',os.environ['GF1M_HISTORICAL_HELPER']);p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
h=p.h
results={}
for cell in itertools.product(range(3),repeat=4):
 a,b,c,d=cell; risk=sum(cell)
 expected=('UNDETERMINED_NO_ELIGIBLE_RISK' if risk==0 or a+b==0 or c+d==0 else 'EXACT_PAIR_SEPARATION' if (a*d>0 and b==c==0) or (b*c>0 and a==d==0) else 'NO_PAIR_SEPARATION')
 r=h._rebuild(counts=dict(zip(('00','01','10','11'),cell)),eligible=risk,zero_state='OBSERVED_ZERO_IN_SUPPORTED_RISK_SET');out=h.CONS(r)
 assert out['separation_class']==expected
 assert out['joint_support_total']==risk and out['production_owner_commit'] is False
 results[''.join(map(str,cell))]=out
r=h._rebuild(counts={},eligible=2,zero_state='OBSERVED_ZERO_IN_SUPPORTED_RISK_SET');out=h.CONS(r)
assert out['separation_class']=='UNDETERMINED_ZERO_SUPPORT_RISK';results['0000_eligible2']=out
assert len(results)==82
native=[]
for profile in ('BASELINE','R2_Y1','R1_Y0'):
 for row in h.ORACLE['genuine_native_relations'][profile]:
  r=h.gen_for(profile,row['work_key']);out=h.CONS(r)
  assert r.content_hash==row['relation_content_hash'] and r.object_id==row['relation_object_id']
  assert out['separation_class']==row['consumer']['separation_class']
  assert out['read_relation_content_hash']==r.content_hash
  assert out['production_owner_commit'] is False
  native.append(dict(profile=profile,work_key=row['work_key'],object_id=r.object_id,content_hash=r.content_hash,conditioner=r.conditioner_source_native_variable,target=r.target_source_native_variable,result=out))
for role in ('condition','target'):
 f=p.fields();cd=(float('inf'),1.0) if role=='condition' else f['conditioner_domain'];td=(float('inf'),1.0) if role=='target' else f['target_domain'];f['conditioner_domain']=cd;f['target_domain']=td
 f['conditional_count_profile']=tuple(dict(condition_state=c,source_native_conditioner=f['conditioner_source_native_variable'],condition_denominator_support=1,target_counts=tuple(dict(target_state=t,source_native_target=f['target_source_native_variable'],joint_support_count=int(ci==ti),joint_cell_state='OBSERVED_POSITIVE' if ci==ti else 'OBSERVED_ZERO_IN_SUPPORTED_RISK_SET') for ti,t in enumerate(td))) for ci,c in enumerate(cd))
 rel=p.make(f);got=h.CONS(rel)
 try:json.dumps(got,allow_nan=False);strict_error=None
 except (ValueError,TypeError) as e:strict_error=type(e).__name__+': '+str(e)
 assert strict_error is not None and got['decision_state']=='PAIR_SUPPORT_SIGNATURE_COMPUTED'
 # Keep witness text outside strict cold payload because nonfinite objects are
 # precisely what this court proves unsuitable for strict JSON exchange.
 results['witness_'+role]=dict(relation_projection=h.G.canonical_json(rel.semantic_projection()),relation_hash=rel.content_hash,result_repr=repr(got),decision=got['decision_state'],result_hash=got['result_hash'],strict_error=strict_error)
h.GB.reattest()
imports=[]
root=h.COURT.resolve()
for name,module in sorted(sys.modules.items()):
 file=getattr(module,'__file__',None)
 if file and Path(file).resolve().is_relative_to(root):
  path=Path(file).resolve();b=path.read_bytes();imports.append(dict(module=name,file=str(path),relative=str(path.relative_to(root)),sha256=hashlib.sha256(b).hexdigest(),git_blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
assert any(x['module']=='gf1_pair_support_consumer' for x in imports)
print(json.dumps(dict(pid=os.getpid(),python=sys.version,executable=sys.executable,native_reattested=h.GB.REATTESTED,native_relations=native,results=results,imports=imports),sort_keys=True,allow_nan=False))
