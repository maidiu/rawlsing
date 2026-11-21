from um_sorok_organism.types import adult, stable_id
from um_sorok_organism.development import admit
from copy import deepcopy
a=adult('ann','Ann')
a['possible_ends']=[{
 'id':ref,'status':'POSSIBLE_NOT_ACQUIRED_MOTIVE','origin_event':'old_'+ref,
 'experience_ref':'lived_'+ref,'actor_perceived_cue_ref':'cue_'+ref,
 'possible_object':obj,'possible_means':['SING'],'cue_terms':['song']}
 for ref,obj in (('end_a','sing together'),('end_b','learn piano'))]
ticket={'actor':'ann','as_of_clock':9,'possible_end_ref':'end_a','operation':'SING',
 'origin_event':'old_end_a','origin_experience_ref':'lived_end_a','actor_project_ref':None}
ticket['trial_id']=stable_id('end_trial',{'actor':'ann','clock':9,'end':'end_a','operation':'SING'})
exp={'actor':'ann','ref':'today_lived','participated':True,'own_action':'SING',
 'status':'PERFORMED','felt_enactment':{'attempted_operation':'SING'},
 'perceived_cues':[{'id':'cue_today','tags':['song']}]}
before=deepcopy(a)
try:
 r=admit(a,exp,'today_event',[{'kind':'TAKE_UP_POSSIBLE_END','possible_end_ref':'end_b',
  'later_perceived_cue_ref':'cue_today','means':['SING']}],issued_trial=ticket)
 print('COMMITTED',r)
 print('projects',[(p['object'],p['motive']) for p in a['projects']])
 print('ends',[(e['id'],e['status']) for e in a['possible_ends']])
except Exception as e:
 print('REFUSED',type(e).__name__,str(e))
print('unchanged',a==before)
