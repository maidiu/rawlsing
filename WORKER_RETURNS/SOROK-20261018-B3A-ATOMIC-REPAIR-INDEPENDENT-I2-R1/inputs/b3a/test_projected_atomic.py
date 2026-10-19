"""S3's explicit failure immediately after admit_projection's own B2 commit."""
import pytest
from test_atomic import setup,snap,seed,cold,save,replay_no_ghost,Integration,Refusal
from developmental_loop import permission_for
@pytest.mark.parametrize('independent',[False,True])
def test_after_first_projected_source_admission(tmp_path,monkeypatch,independent):
 f,a,e,path=setup(tmp_path,independent);before=snap(e);original=Integration.admit_projection;observed=[]
 def fail(self,*args,**kwargs):
  r=original(self,*args,**kwargs);observed.append(dict(snapshot=snap(self),receipt=r))
  raise Refusal('INJECTED_AFTER_FIRST_PROJECTED_SOURCE_ADMISSION')
 monkeypatch.setattr(Integration,'admit_projection',fail);p=permission_for([],f)
 r=e.run(f,owner_permission=p,registered_permissions=(p,));assert r['status']=='REFUSED' and r['no_mutation'] and not r['owner_effect_committed']
 assert len(observed)==1 and len(observed[0]['snapshot']['occurrence'])>len(before['occurrence']) and snap(e)==before
 e.close();c=cold(path);assert c['snapshot']==before
 monkeypatch.setattr(Integration,'admit_projection',original)
 e=Integration(path,a);later=replay_no_ghost(e,a);e.close()
 save('after_first_projection_'+str(independent),before=before,tentative=observed,result=r,cold=c,later=later)
