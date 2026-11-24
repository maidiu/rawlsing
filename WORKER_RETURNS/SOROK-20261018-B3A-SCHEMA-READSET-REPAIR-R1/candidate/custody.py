"""Test-only adaptation of exact corrected B2 ingress; legacy psyche remains unused."""
from copy import deepcopy
from datetime import datetime,timedelta,timezone
from dataclasses import asdict
from sources import b2,m2

def prepare(initial,external,project='bike_security',participant=None,projection=None):
 # P1 possibilities are proposals, not evidence. All source words are empty here;
 # later speech is a different occurrence, never bundled into the loss.
 person=participant or b2.b1.participant(outcome='NO_OBSERVED_MATERIAL_OFFER')
 packet,context,policy=b2.input_pair(initial,other={'CARE-1':person})
 iso=(datetime(2026,10,17,10,tzinfo=timezone.utc)+timedelta(seconds=external['time'])).isoformat().replace('+00:00','Z')
 context['as_of']=iso
 for x in context['action_opportunities'].values():x['time']=iso
 for c in packet['candidates']:
  c['time']=iso;c['interpretations']=[]
 context=b2.rehash(context,'context_hash');packet.update(as_of=iso,context_hash=context['context_hash'])
 packet=b2.rehash(packet,'proposal_hash');ev=b2.p1.evaluate(packet,context)
 policy['candidate_set_hash']=ev['candidate_set_hash'];policy=b2.rehash(policy,'policy_hash')
 witness=b2.occurrence_witness(initial,packet,context,other={'CARE-1':person},observed=[])
 witness.update(event_id=external['id'],number=external['time']-1,time=iso,project=project,
  objective_occurrence=external['content']['fact'],interrupted=external['content']['fact']=='stolen',
  external_occurrence=deepcopy(external))
 loss=projection or m2.Event(external['id'],'LOSS',external['time'],'child',('child','caregiver','peer'),
  (m2.WorldFact('RESOURCE_STATUS',external['content']['object'],'MISSING',b2.b1.digest(external)),))
 if projection is None and external['content']['fact']!='stolen':
  loss=m2.Event(external['id'],'ENCOUNTER',external['time'],'child',('child','caregiver','peer','later_other'),('community_hall',),action_owner=external['content'].get('counterpart'),action=external['content'].get('action'))
 witness['m2_projection']=asdict(loss);witness['m2_projection_hash']=m2.objective_event_hash(loss)
 witness=b2.b1.sealed({k:v for k,v in witness.items() if k!='hash'})
 cap,reg=b2.capability_fixture(external['id'],iso[:10],status='CAPABILITY_UNKNOWN')
 return dict(packet=packet,context=context,policy=policy,witness=witness,capability=cap,registry=reg),loss

def admit(bridge,bundle):
 w=bundle['witness'];bridge.witnesses={w['hash']:w};bridge.capability_witnesses=bundle['registry']
 r=bridge.advance(bundle['packet'],bundle['context'],bundle['policy'],w,bundle['capability'],grant=False)
 # The native D1 UNKNOWN deliberately stops the legacy B1 response *after*
 # lawful admission. B3 then runs its own candidate CAN008-compatible response.
 assert not r['b1_invoked'],'LEGACY_LABEL_RESPONSE_MUST_NOT_EXECUTE'
 return r

def projected_loss(bridge,bundle):
 w=bundle['witness'];row=bridge.store.db.execute('SELECT binding,event_ref FROM b2_event_identity WHERE event_id=?',(w['event_id'],)).fetchone()
 assert row and m2.digest(__import__('json').loads(row[0])['witness'])==m2.digest(w),'UNQUALIFIED_OCCURRENCE_PROJECTION'
 p=deepcopy(w['m2_projection']);p['participants']=tuple(p['participants']);p['material']=tuple(m2.WorldFact(**x) if isinstance(x,dict) else x for x in p['material'])
 e=m2.Event(**p);assert m2.objective_event_hash(e)==w['m2_projection_hash']
 return e


def participant_from_records(records,now):
 observed=[x for x in records if x['actor']=='caregiver' and x['time']<=now and x['act'] in ('REPAIR_TOOLS','DECLINE_HELP')]
 history=tuple(b2.b1.HistoryEpisode(x['id'],'caretaker','workshop','own_work',x['time'],x['act'],
  'tools_available' if x['act']=='REPAIR_TOOLS' else x['act'],'EXPLICIT',(),
  'B3_SOURCEFREE_COMPATIBILITY_PROJECTION:'+x['hash']) for x in observed)
 return b2.b1.Participant('caretaker','own_work',history)
