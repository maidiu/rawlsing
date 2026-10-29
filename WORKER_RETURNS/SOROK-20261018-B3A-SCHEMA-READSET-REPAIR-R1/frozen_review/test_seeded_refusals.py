"""Same new refusal assertions against original/repaired imports in separate processes."""
from copy import deepcopy
from test_reviewer_hostiles import setup,cold,stable,save
import pytest

@pytest.mark.parametrize('attack',['missing_origin','future_event'])
@pytest.mark.parametrize('seeded',[False,True])
def test_bad_request_has_no_cold_partial_rows(tmp_path,attack,seeded):
 f,a,e,path=setup(tmp_path,seeded);bad=deepcopy(f)
 if attack=='missing_origin':bad['origin_event_id']='I2-not-issued'
 else:bad['event']['time']=99
 a.register_observed(bad);before=cold(path)
 try:
  try:r=e.run(bad)
  except Exception as exc:r=dict(exception=type(exc).__name__,code=str(exc))
 finally:e.close()
 after=cold(path);save('seeded_'+attack+'_'+str(seeded),before=before,result=r,after=after)
 assert stable(after)==stable(before),'refusal left durable rows, or erased independently admitted fact'
 assert r['status']=='REFUSED' and r['no_mutation']
