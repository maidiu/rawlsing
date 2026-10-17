from pathlib import Path
from dataclasses import replace
import json,hashlib,copy
import pv2_original_scope_register as V
import pv2_sourcefree_fixture as F
from rawlsing_next import pre553_original_identity_v2k_successor_candidate as K
from rawlsing_next.pre553_empirical_objects import ExactRef
R=Path(__file__).resolve().parents[1];RT=R/'runtime_root';O=json.loads((R/'01_FROZEN_ORIGINAL_EXPECTED_SET.json').read_text())
def dump(name,obj): (R/'observations'/name).write_text(json.dumps(obj,indent=2,default=str)+'\n')
def ref(label):return ExactRef('PV2I_FOREIGN','urn:pv2i:'+label,hashlib.sha256(label.encode()).hexdigest())
def run(fx,expected=None,plans=None,register=None,**kw):
 return V.run_sourcefree_with_register(expected=expected or fx['expected'],selected_scopes=plans if plans is not None else fx['plans'],register=register or fx['register'],scope_metadata=tuple(fx['meta']),**kw)
def slot(fx,ns='PV2-ADULT-A',kind='PAIR'):return next(w for w in fx['records'] if w.original.respondent_namespace==ns and w.legacy.slot==kind)
def mutate_work(fx,old,new):
 records=tuple(new if w is old else w for w in fx['records']);expected=K.FrozenOriginalExpected.from_records(records,input_origin=K.ORIGIN)
 plans=tuple(replace(p,original_work_keys=tuple(new.key if k==old.key else k for k in p.original_work_keys)) for p in fx['plans'])
 return expected,plans

def profile(material):return {str(c['condition_state']):{'denominator':c['condition_denominator_support'],'targets':{str(t['target_state']):t['joint_support_count'] for t in c['target_counts']}} for c in material['conditional_count_profile']}

def make_numeric_fixture(root, row=2, new_value='1'):
 """Reviewer-defined R2 Y0->1 trial, independently frozen arithmetic; not an author test helper."""
 physical=F.physical_fixture
 def altered():
  fx=physical();old=fx['stream'];cells=tuple(replace(c,raw_value=new_value) if c.row_ordinal==row and c.variable_name=='Y' else c for c in old.cell_iter_factory())
  h=hashlib.sha256(json.dumps([(c.row_ordinal,c.variable_name,c.raw_value) for c in cells],sort_keys=True).encode()).hexdigest()
  fx['stream']=replace(old,source_sha256=h,cell_iter_factory=lambda:iter(cells))
  p=fx['projection'];fx['projection']=replace(p,expected_source_sha256=h,source_snapshot_retention_ref=replace(p.source_snapshot_retention_ref,content_hash=h))
  return fx
 F.physical_fixture=altered
 try:a=F.sourcefree_original_inputs('PV2-ADULT-A')
 finally:F.physical_fixture=physical
 b=F.sourcefree_original_inputs('PV2-ADULT-B');inputs=[a,b]
 original=V.author_sourcefree_original_scope_register()
 register=replace(original,source_native_inventory=tuple(replace(c,raw_value=new_value) if c.respondent_namespace=='PV2-ADULT-A' and c.respondent_key=='R'+str(row) and c.item_short_name=='Y' else c for c in original.source_native_inventory))
 groups=[F.freeze_original_before_production(x,register) for x in inputs];records=tuple(w for g in groups for w in g)
 prepared=[F.prepare_owner_scope(root/str(i),data,g,ns) for i,(data,g,ns) in enumerate(zip(inputs,groups,F.NAMESPACES))]
 return dict(register=register,records=records,expected=K.FrozenOriginalExpected.from_records(records,input_origin=K.ORIGIN),plans=tuple(x[0] for x in prepared),calls=[x[1] for x in prepared],meta=[{'respondent_namespace':m['respondent_namespace'],'respondent_refs':m['respondent_refs']} for _,_,m in prepared],inputs=inputs)
