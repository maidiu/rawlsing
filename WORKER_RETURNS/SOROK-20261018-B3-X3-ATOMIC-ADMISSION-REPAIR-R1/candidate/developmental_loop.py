"""Actually execute a small deterministic synthetic developmental world.

Each nonfocal actor consults only its own earlier actions/project. Test policies
are authored, uncalibrated, and have no autonomous-human or original-source grade.
"""
from copy import deepcopy
from pathlib import Path
import json,sys
from integration import Integration,digest,seal
from fixture_authority import FixtureAuthority
import target_owner

class OtherActor:
 def __init__(self,actor,project,activity):
  self.actor=actor;self.project=project;self.history=[dict(time=1,activity=activity)]
 def act(self,now):
  # No focal child's state, desired outcome, label, class or affect is available.
  if self.actor=='caregiver' and now==4:
   action=('SPEAK','We can check the lock after the inventory.')
  elif self.actor=='peer' and now==5:
   action=('SPEAK','Outsiders did it.')
  elif self.actor=='later_other' and now==9:
   action=('DECLINE_CONTACT',None) if any(x['activity']=='rehearsal_due' for x in self.history) else ('ALLOW_CONTACT',None)
  else:return None
  self.history.append(dict(time=now,activity=action[0]))
  return dict(actor=self.actor,project=self.project,action=action[0],words=action[1],time=now,source_history=deepcopy(self.history[:-1]))

class World:
 def __init__(self,other_due=True):
  self.now=0;self.records=[];self.speech=[];self.exposures=[];self.actor_actions=[]
  self.people=[OtherActor('caregiver','workshop','inventory_due'),OtherActor('peer','club','club_debate'),OtherActor('later_other','music','rehearsal_due' if other_due else 'free_rehearsal')]
  self.event=None
 def observe(self,id,actor,act,time,**fields):
  x=seal(dict(id=id,actor=actor,owner=actor,act=act,time=time,source='OBSERVED_TASK' if act.startswith('CAPABILITY_TASK') else 'WORLD',object='bike-child',**fields))
  self.records.append(x);return x
 def tick(self,now):
  assert now>self.now;self.now=now
  if now==1:
   self.observe('cap','child','CAPABILITY_TASK_SUCCESS',1)
   self.observe('choice','child','SHARED_TASK_CHOICE',1)
   self.observe('tools','caregiver','REPAIR_TOOLS',1)
   self.observe('other_project','later_other','LATER_PROJECT',1)
  if now in (2,7):self.observe('check:'+str(now),'child','PRACTICE_COMPLETED',now,observer='caregiver',result='LOCK_CHECK_CONFIRMED')
  if now==3:
   content=dict(fact='stolen',object='bike-child',place='garage',known_culprit=None)
   self.event=dict(id='loss:t3',time=3,owner='TEST_WORLD_REGISTRY',admitted=True,content=content,content_hash=digest(content))
   self.observe('loss_observed','child','MATERIAL_LOSS',3,observer='caregiver')
  for person in self.people:
   a=person.act(now)
   if not a:continue
   self.actor_actions.append(a)
   x=self.observe('action:'+person.actor+':'+str(now),person.actor,a['action'],now,independent_project=person.project,history_parent=digest(a['source_history']))
   if a['words']:
    self.exposures.append(dict(id='heard:words:'+person.actor,speech_id='words:'+person.actor,listener='child',time=now,observer='child',speech_witness=x['id'],source_hash=x['hash'],issuer='B3_TEST_ONLY_EXPOSURE_REGISTRY'))
    self.speech.append(dict(id='words:'+person.actor,speaker=person.actor,claim=a['words'],epistemic='ATTRIBUTED_CLAIM',witness=x['id'],heard_by=['child'],event_ref='loss:t3'))
  if now==9:
   a=self.actor_actions[-1]
   content=dict(fact='shared_tool_offer',object='bike-child',place='garage',known_culprit=None,counterpart='later_other',action='REFUSE' if a['action']=='DECLINE_CONTACT' else 'ALLOW')
   self.event=dict(id='encounter:t9',time=9,owner='TEST_WORLD_REGISTRY',admitted=True,content=content,content_hash=digest(content))
 def frame(self):
  f=dict(case_id='SYNTHETIC_DEVELOPMENTAL_LOOP',actor=dict(id='child',epistemic={'beliefs':[],'affect':[]},practice=[]),
   event=deepcopy(self.event),actors=['child','caregiver','peer','later_other'],evidence=deepcopy(self.records),utterances=deepcopy(self.speech),exposures=deepcopy(self.exposures),ledger=[],
   readset=[x['id'] for x in self.records if x['actor']=='child']+[s['witness'] for s in self.speech if 'child' in s['heard_by']],
   capability=dict(name='C07',scope='garage',declared='PRESENT',witnesses=[dict(actor='child',capability='C07',scope='garage',source='cap',time=1,end=None,outcome='PRESENT')]),
   as_of=self.now,proposals={},lineage=[])
  if self.now==9:f['origin_event_id']='loss:t3'
  return f

def permission_for(middle,frame):
 p=dict(actor='child',before=digest(middle),rule_hash=target_owner.RULE_HASH,time=frame['as_of'],parents=[x['hash'] for x in frame['evidence'] if x['act']=='PRACTICE_COMPLETED'])
 return digest(dict(actor='child',before=digest(middle),proposal=digest(p),rule=target_owner.RULE_HASH))

def execute(path,grant=True,other_due=True):
 authority=FixtureAuthority();e=Integration(path,authority);world=World(other_due);episodes=[]
 for time in range(1,10):
  world.tick(time)
  if time not in (3,4,5,6,7,9):continue
  frame=world.frame();authority.register_observed(frame)
  permission=permission_for(e.middle(),frame) if grant and time==7 else None
  receipt=e.run(frame,owner_permission=permission,registered_permissions=(permission,) if permission else ())
  assert receipt['status']=='ELIGIBLE_NONCAUSAL',receipt
  episodes.append(dict(frame=frame,owner_permission=permission,receipt=receipt,actor_actions=deepcopy(world.actor_actions)))
  # Cold connection on the same actual SQLite file, not in-memory persistence.
  e.close();e=Integration(path,authority)
 result=dict(grade=episodes[-1]['receipt']['grade'],episodes=episodes,final_snapshot=e.snapshot(),final_middle=e.middle(),grant=grant,other_due=other_due)
 result['snapshot_hash']=digest(result['final_snapshot']);e.close();return result

def replay(bundle,path):
 authority=FixtureAuthority();e=Integration(path,authority);receipts=[]
 for ep in bundle['episodes']:
  f=ep['frame'];authority.register_observed(f);permission=ep['owner_permission']
  receipts.append(e.run(f,owner_permission=permission,registered_permissions=(permission,) if permission else ()))
 actual=dict(receipts=receipts,snapshot_hash=digest(e.snapshot()),final_middle=e.middle());e.close();return actual

if __name__=='__main__':
 if sys.argv[1]=='replay':
  print(json.dumps(replay(json.loads(Path(sys.argv[2]).read_text()),Path(sys.argv[3])),sort_keys=True))
 else:
  out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True)
  for label,grant in [('positive',True),('permission_absent',False)]:
   path=out/(label+'.sqlite')
   if path.exists():path.unlink()
   bundle=execute(path,grant);(out/(label+'.json')).write_text(json.dumps(bundle,indent=2)+'\n')
   print(label,bundle['snapshot_hash'],bundle['episodes'][-1]['receipt']['CAN008_response']['practical_actions'])
