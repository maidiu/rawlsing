"""Separate TEST_ONLY CAN011 destination court. No canonical registry grant."""
from pathlib import Path
import hashlib
from sources import m2
RULE='B3_WITNESSED_REPEATED_SECURITY_PRACTICE@1'
RULE_HASH=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
class Denied(ValueError):pass

def validate(before,event,records,proposal,permission,registered):
 # Independently rederive source predicates; never trust CAN008's eligibility flag.
 if permission not in registered:raise Denied('CAN011_OWNER_PERMISSION_DENIED')
 if permission!=m2.digest({'actor':'child','before':m2.digest(before),'proposal':m2.digest(proposal),'rule':RULE_HASH}):raise Denied('STALE_OR_UNBOUND_TARGET_PERMISSION')
 if proposal.get('before')!=m2.digest(before):raise Denied('CAN011_STALE_STATE')
 if proposal.get('rule_hash')!=RULE_HASH or proposal.get('actor')!='child':raise Denied('CAN011_RULE_OR_ACTOR')
 if any(x.get('kind')=='V3MS_PRACTICE' and x.get('targets')==[event['content']['object']] for x in before):raise Denied('CAN011_CREATE_ALREADY_EXISTS')
 parents=[]
 for x in records:
  if (x.get('actor')=='child' and x.get('act')=='PRACTICE_COMPLETED' and x.get('object')==event['content']['object']
      and x.get('owner')=='child' and x['time']<=proposal['time'] and x.get('observer') in ('caregiver','peer','later_other')
      and x['hash']==m2.digest({k:v for k,v in x.items() if k!='hash'}) and x.get('result')=='LOCK_CHECK_CONFIRMED'):
   parents.append(x)
 if len({x['id'] for x in parents})<2:raise Denied('CAN011_ENACTED_REPEATED_PRACTICE_MISSING')
 if not any(x['time']>event['time'] for x in parents):raise Denied('CAN011_NEW_PRACTICE_AFTER_EVENT_MISSING')
 if sorted(proposal.get('parents',[]))!=sorted(x['hash'] for x in parents):raise Denied('CAN011_PARENT_BINDING')
 record=dict(registry_id='B3_TEST_ONLY_CAN011_REGISTRY',registry_version='1',registry_snapshot_hash=m2.digest({'kind':'V3MS_PRACTICE','rule':RULE_HASH}),before_target_hash=m2.digest(before),actor='child',kind='V3MS_PRACTICE',rule=RULE,rule_hash=RULE_HASH,
  targets=[event['content']['object']],payload={'procedure':'CHECK_LOCK','scope':'garage'},
  effective_from=proposal['time'],lifecycle='ACTIVE',causal_parents=[event['content_hash']]+sorted(proposal['parents']),
  actor_memory_access='NOT_GRANTED',grade='TEST_ONLY_RESEARCH_RULE_UNCALIBRATED')
 return dict(record,hash=m2.digest(record))
