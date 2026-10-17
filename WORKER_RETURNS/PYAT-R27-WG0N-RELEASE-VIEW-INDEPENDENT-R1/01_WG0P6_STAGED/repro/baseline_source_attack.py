"""Literal precompile and copied-plan SOURCE_SNAPSHOT substitution on P5."""
import copy,json,sys
from pathlib import Path
from dataclasses import replace
from phase_b_support_v1 import w,plan,execute,profile_calls,OP
R=Path(__file__).resolve().parents[1]
rows=[]
for mode in ['precompile','copied_plan']:
 releases=w.build_all_releases();p=plan(releases=releases)
 original=releases['REL-A-W1'];foreign=releases['REL-A-W2'].source_artifact_ref
 before=w.digest(w._release_material(original))
 changed=replace(original,source_artifact_ref=foreign)
 after=w.digest(w._release_material(changed));calls=[];error=None;consumer={}
 try:
  if mode=='precompile':
   releases['REL-A-W1']=changed
   sys.setprofile(profile_calls(calls));bad=plan(releases=releases)
  else:
   mapping=dict(p.releases);mapping['REL-A-W1']=changed;bad=replace(p,releases=mapping)
   sys.setprofile(profile_calls(calls))
  _,rs,consumer=execute(bad)
 except Exception as exc:error=dict(type=type(exc).__name__,message=str(exc))
 finally:sys.setprofile(None)
 rows.append(dict(mode=mode,registered_material_digest_before=before,registered_material_digest_after=after,
                  material_digest_unchanged=before==after,actual_native_artifact=original.repo.resolve_release_exact(original.release_ref).source_artifact_ref.as_dict(),
                  original_view=original.source_artifact_ref.as_dict(),foreign_view=foreign.as_dict(),
                  exception=error,consumer=consumer,new_I03_calls=sum(c['name']=='execute_empirical_query' for c in calls)))
assert all(r['material_digest_unchanged'] and r['consumer'] and r['exception'] is None and r['new_I03_calls']>0 for r in rows)
(R/'observations/baseline_source_attack.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps([{k:v for k,v in r.items() if k!='consumer'} for r in rows],indent=2))
