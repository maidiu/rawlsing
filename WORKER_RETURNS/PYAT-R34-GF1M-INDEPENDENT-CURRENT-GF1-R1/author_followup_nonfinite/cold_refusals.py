"""Author follow-up cold proof; no changes to the frozen independent court."""
import importlib.util,os,json,hashlib
from pathlib import Path
s=importlib.util.spec_from_file_location('gf1m_frozen',os.environ['GF1M_ORIGINAL_PHASE_A']);f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
rows=[]
for role in ('condition','target'):
 for label,number in [('positive_inf',float('inf')),('negative_inf',float('-inf')),('nan',float('nan'))]:
  for position in (0,1):
   domain=[1.0,1.0];domain[position]=number;got=f.p.h.CONS(f.build(role,tuple(domain)))
   assert got['decision_state']=='CONSUMER_RELATION_INTEGRITY_REJECTED'
   assert got['separation_class'] is None and got['downstream_value_produced'] is False
   assert not {'support_vectors','joint_support_total','result_hash','separation_signature'}&got.keys()
   assert got['production_owner_commit'] is False
   json.dumps(got,allow_nan=False)
   rows.append(dict(role=role,nonfinite=label,position=position,result=got))
file=Path(f.p.h.RT/'gf1_pair_support_consumer.py').resolve()
print(json.dumps(dict(pid=os.getpid(),consumer_file=str(file),consumer_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),reattested=f.p.h.GB.REATTESTED,cases=rows),sort_keys=True,allow_nan=False))
