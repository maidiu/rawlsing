from um_sorok_organism.types import adult
from um_sorok_organism.activity import record_activity_afterlife
a=adult('ann','Ann')
a['projects']=[{'id':'care','object':'kin care','means':['CARE'],'status':'active','motive':'CARE'}]
try:
    r=record_activity_afterlife(a,'SING','PERFORMED','SANG',['project:care'],'event_x',purpose_selection={
        'status':'ACTOR_POLICY_SELECTED_PROJECT_COURSE','project_id':'care','project_ids':['care']})
    print('RETURNED',r)
except Exception as e:
    print('REFUSED',type(e).__name__,str(e))
print('activity_history',a.get('activity_history',[]))
print('operational_history',a['projects'][0].get('operational_history',[]))
