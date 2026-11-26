"""R8 historically acquired self-regulation, not a sovereign will module.

An actual actor may acquire a *practice* for organizing later initiative. The
practice is an ordinary actor-owned form with tendencies read by the inherited
psychodynamic engine; bodily/world constraints and other currents still govern.
This candidate is fictional sourcefree psychological construction, not native
CAN/ADP theory or proof of introspective accuracy.
"""
import hashlib
import json
import math

GRADE = 'SOURCEFREE_RESEARCH_PROVISIONAL'


def _ref(name, value):
    raw = json.dumps(value, sort_keys=True, ensure_ascii=False,
                     allow_nan=False, separators=(',', ':'))
    return name + '_' + hashlib.sha256(raw.encode('utf8')).hexdigest()[:16]


def acquire_reflective_regulation(actor, experience, event_ref, proposal,
                                  allowed_actions):
    """Build a learned form after an actor's real enacted, experienced activity.

    Must depend on an actual earlier actor-owned practice or undertaking. A
    language threshold gates ONLY a reflective self-description, not agency,
    desire, primitive goal-directedness, anticipation, or nonverbal inhibition.
    Future action still requires bodily eligibility and the world's actual
    permissions; opposition is not resolved by creating this practice.
    """
    if experience.get('actor') != actor.get('id') or not event_ref:
        raise ValueError('REFLECTIVE_ACTOR_IDENTITY_MISMATCH')
    body = actor.get('body', {})
    language, regulation = body.get('language'), body.get('regulation')
    if (isinstance(language, bool) or not isinstance(language,(int,float)) or
            not math.isfinite(language) or language < .35 or
            isinstance(regulation, bool) or not isinstance(regulation,(int,float)) or
            not math.isfinite(regulation) or regulation < .20):
        raise ValueError('REFLECTIVE_CAPACITY_NOT_YET_AVAILABLE')
    enactment = experience.get('felt_enactment') or {}
    if (not experience.get('participated') or
            experience.get('status') not in ('PERFORMED','PARTIAL') or
            not experience.get('own_action') or
            enactment.get('attempted_operation') != experience['own_action']):
        raise ValueError('REFLECTIVE_NO_ENACTED_ACTOR_ACTIVITY')
    target = proposal.get('future_operation')
    if type(target) is not str or target not in allowed_actions:
        raise ValueError('REFLECTIVE_NEW_UNLICENSED_OPERATION')
    tendency = proposal.get('recruitment_polarity')
    if tendency not in ('APPROACH','WITHHOLD'):
        raise ValueError('REFLECTIVE_UNSUPPORTED_RECRUITMENT')
    # An analyst cannot fabricate a personal source merely by citing a future
    # project. It must already be owned by this particular actor.
    source = proposal.get('historical_source_ref')
    known = set(actor.get('forms', {})) | {
        p.get('id') for p in actor.get('projects', []) if isinstance(p,dict)}
    if type(source) is not str or source not in known:
        raise ValueError('REFLECTIVE_UNOWNED_HISTORICAL_SOURCE')
    seen = {c['id']: c for c in experience.get('perceived_cues', [])
            if isinstance(c,dict) and isinstance(c.get('id'), str)}
    sign_id = proposal.get('perceived_cue_ref')
    if sign_id not in seen:
        raise ValueError('REFLECTIVE_UNEXPERIENCED_SIGN')
    tags = seen[sign_id].get('tags', [])
    if (not isinstance(tags,list) or not tags or len(tags)>16 or
            any(type(t) is not str or not t.strip() for t in tags)):
        raise ValueError('REFLECTIVE_INVALID_CONTEXT_CUES')
    location = actor.get('location')
    if type(location) is not str or not location:
        raise ValueError('REFLECTIVE_NO_ACTUAL_LOCATION')
    # This is not a direct action entitlement, nor an introspectively certain
    # motive. It is a recruitable, fallible self-organizing operation.
    ident = _ref('regulation',{'actor':actor['id'],'event':event_ref,
                              'source':source,'operation':target,'polarity':tendency})
    if ident in actor.get('forms', {}):
        raise ValueError('REFLECTIVE_DUPLICATE_FORM')
    form = {'id': ident, 'actor':actor['id'], 'kind':'PRACTICE',
            'content':'self-organizing practice with respect to '+target.lower(),
            'cues':sorted(set(t.strip().casefold() for t in tags)),
            'enables':[], 'tendencies':[{'action':target,'polarity':tendency,
                                       'cue_terms':sorted(set(t.strip().casefold() for t in tags))}],
            'scope':{'locations':[location]},
            'strength':.4, 'body_min':0, 'access':'ACQUIRED_REFLECTIVE_PRACTICE',
            'lifecycle':'ACTIVE','origin':[event_ref],
            'historical_source_ref':source,
            'actor_enactment_ref':experience['ref'],
            'actor_received_cue_ref':sign_id,
            'conscious_intention':'PROVISIONAL_PRACTICE_NOT_FULL_CAUSAL_EXPLANATION',
            'does_not_override_other_currents':True,
            'does_not_grant_world_feasibility':True,
            'source_grade':GRADE}
    # Development owner commits atomically on detached actor; this helper
    # makes its only actor-local change to that staged copy.
    actor.setdefault('forms', {})[ident] = form
    return {'kind':'ACQUIRE_REFLECTIVE_REGULATION','form':ident,
            'historical_source_ref':source, 'polarity':tendency,
            'future_operation':target,'not_sovereign_agency':True,'grade':GRADE}

# Private activity extends the acquired self-organization owner. A WAIT is
# only the public carrier of elapsed time, never evidence of thinking.
from .types import stable_id, copy

_PRIVATE_MEANS=('REST','ORIENT','EAT')

def _capacity(body):
    return all(type(body.get(k)) in (int,float) and math.isfinite(body[k])
               and body[k]>=v for k,v in (('language',.35),('regulation',.20),('rest',.12)))

def offer_private_rehearsals(actor,clock,location,available_operations,*,body=None):
    """Actor-local, finite recollective opportunities; no matching external cue required.

    Historical memory is fallible acquired content, not a replay of a world
    archive. An affect acquired in the same lived event may be its object.
    Nondeclarative traces do not become explicit remembered propositions.
    """
    if not _capacity(actor['body'] if body is None else body):return []
    if 'WAIT' not in available_operations:return []
    means=[m for m in _PRIVATE_MEANS if m in available_operations]
    if not means:return []
    aid=actor['id'];out=[]
    paths={x.get('event'):x for x in actor.get('evidence_paths',[])[-256:]}
    episodes={x.get('event_ref'):x for x in actor.get('lived_genesis_episodes',[])[-256:]
              if x.get('actor')==aid}
    affects=[a for e in actor.get('expectations',[])[-128:]
             if e.get('actor')==aid for a in e.get('affective_organizations',[])[-16:]
             if a.get('actor')==aid and a.get('expectation_ref')==e.get('id')]
    for m in reversed(actor.get('memories',[])[-32:]):
        origins=m.get('origin',[])
        if (m.get('status')!='ACTOR_ACCESSIBLE' or len(origins)!=1
                or type(m.get('content')) is not str or not m['content'].strip()
                or type(m.get('id')) is not str):continue
        path=paths.get(origins[0]);episode=episodes.get(origins[0])
        if (not path or not episode or path.get('experience_ref')!=m.get('experience')
                or episode.get('experience_ref')!=m.get('experience')
                or episode.get('clock',clock)>clock
                or episode.get('location')!=location):continue
        cues=sorted(set(path.get('received_cue_refs',[]))&set(episode.get('received_sign_refs',[])))
        if not cues:continue
        linked=[a for a in affects if a.get('origin_event_ref')==origins[0]]
        # Keep the memory-only course distinct from affect-directed rehearsal.
        for aff in [*linked,None]:
            ar=aff['id'] if aff else None
            if any(x.get('affect_ref')==ar for x in m.get('private_rehearsals',[])):continue
            basis={'actor':aid,'as_of_clock':clock,'location':location,
                   'memory_ref':m['id'],'memory_event_ref':origins[0],
                   'memory_experience_ref':m['experience'],'historical_received_cue_refs':cues,
                   'affect_ref':ar,'possible_means':means}
            if m.get('undertaking_attention'):
                receipt=m['undertaking_attention']
                if (path.get('undertaking_attention')!=receipt
                        or receipt.get('cue_ref') not in cues):continue
                basis['undertaking_attention']=copy(receipt)
            if m.get('correspondence_attention'):
                receipt=m['correspondence_attention']
                if (path.get('correspondence_attention')!=receipt
                        or receipt.get('received_cue_ref') not in cues):continue
                basis['correspondence_attention']=copy(receipt)
            out.append({**basis,'rehearsal_id':stable_id('private_rehearsal_option',basis),
                        'remembered_content_hypothesis':m['content'][:400],
                        'affective_object':copy(aff) if aff else None,
                        'not_current_perception_or_accurate_memory_proof':True,
                        'carrier_operation':'WAIT','grade':GRADE})
            if len(out)>=12:return out
    return out


def perform_private_rehearsal(actor,experience,event_ref,selection,before):
    """Retain an explicitly selected internal act in the existing memory owner.

    A world WAIT has actually consumed time. Its private accompaniment is a
    separate sourcefree semantic construction, not a public sign.
    """
    chosen=selection.get('private_rehearsal')
    if chosen is None:return None
    opt=chosen.get('option');content=chosen.get('imagined_content')
    if (type(opt) is not dict or type(content) is not str or not content.strip()
            or len(content)>512 or experience.get('actor')!=actor['id']
            or experience.get('own_practical_selection')!=selection
            or experience.get('own_action')!='WAIT' or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True
            or selection.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or selection.get('selected_project_refs')!=[]
            or selection.get('possible_end_trial') is not None
            or experience.get('clock')!=opt.get('as_of_clock',-2)+1
            or opt.get('location')!=experience.get('location')):
        raise ValueError('PRIVATE_REHEARSAL_NO_ACTUAL_SELECTED_INTERVAL')
    offers=offer_private_rehearsals(actor,opt['as_of_clock'],opt['location'],
                                    ['WAIT',*opt['possible_means']],body=before)
    if opt not in offers:raise ValueError('PRIVATE_REHEARSAL_STALE_OR_FOREIGN_SOURCE')
    m=next(x for x in actor['memories'] if x['id']==opt['memory_ref'])
    rec={'id':stable_id('private_rehearsal',{'actor':actor['id'],'event':event_ref,
                     'option':opt['rehearsal_id']}),'actor':actor['id'],
         'event_ref':event_ref,'experience_ref':experience['ref'],'clock':experience['clock'],
         'location':opt['location'],'memory_ref':m['id'],'memory_event_ref':opt['memory_event_ref'],
         'historical_received_cue_refs':copy(opt['historical_received_cue_refs']),
         'affect_ref':opt['affect_ref'],'imagined_content':content.strip(),
         'possible_means':copy(opt['possible_means']),
         'private_activity_not_new_world_event':True,
         'reconstructed_not_verified_recollection':True,
         'no_new_perception_skill_or_permission':True,'grade':GRADE}
    if opt.get('undertaking_attention'):
        rec['undertaking_attention']=copy(opt['undertaking_attention'])
    if opt.get('correspondence_attention'):
        rec['correspondence_attention']=copy(opt['correspondence_attention'])
    m.setdefault('private_rehearsals',[]).append(rec)
    return rec


def admit_private_possible_end(actor,experience,event_ref,proposal):
    """Private comparison can form a genuinely new object for a future trial."""
    allowed={'kind','rehearsal_ref','possible_object','possible_means'}
    if set(proposal)!=allowed:raise ValueError('PRIVATE_END_INVALID_FIELDS')
    matches=[r for m in actor.get('memories',[]) for r in m.get('private_rehearsals',[])
             if r.get('id')==proposal['rehearsal_ref'] and r.get('actor')==actor['id']
             and r.get('event_ref')==event_ref and r.get('experience_ref')==experience.get('ref')]
    if len(matches)!=1 or experience.get('actor')!=actor['id']:
        raise ValueError('PRIVATE_END_NO_ACTUAL_REHEARSAL')
    rec=matches[0];obj=proposal['possible_object'];means=proposal['possible_means']
    if (type(obj) is not str or not obj.strip() or len(obj)>512
            or type(means) is not list or not means or len(means)>len(_PRIVATE_MEANS)
            or any(type(m) is not str or m not in rec['possible_means'] for m in means)
            or len(set(means))!=len(means)):
        raise ValueError('PRIVATE_END_UNQUALIFIED_OBJECT_OR_MEANS')
    if any(e.get('private_rehearsal_ref')==rec['id'] for e in actor.get('possible_ends',[])):
        raise ValueError('PRIVATE_END_DUPLICATE_REHEARSAL')
    ident=stable_id('private_possible_end',{'actor':actor['id'],'rehearsal':rec['id'],'object':obj})
    end={'id':ident,'possible_object':obj.strip(),'possible_means':copy(means),
         'cue_terms':[],'status':'POSSIBLE_NOT_ACQUIRED_MOTIVE',
         'origin_event':event_ref,'experience_ref':experience['ref'],
         'origin_clock':rec['clock'],'eliciting_actor_action':None,
         'genesis_family':'ACTUAL_PRIVATE_REHEARSAL',
         'private_rehearsal_ref':rec['id'],'private_memory_ref':rec['memory_ref'],
         'private_affect_ref':rec['affect_ref'],'private_location':rec['location'],
         'historical_received_cue_refs':copy(rec['historical_received_cue_refs']),
         'actor_perceived_cue_ref':None,'not_a_new_received_world_sign':True,
         'meaning_hypothesis_not_empirical_learning_law':True,'grade':GRADE}
    if rec.get('undertaking_attention'):
        end['private_undertaking_attention']=copy(rec['undertaking_attention'])
    if rec.get('correspondence_attention'):
        end['private_correspondence_attention']=copy(rec['correspondence_attention'])
    actor.setdefault('possible_ends',[]).append(end)
    return {'kind':'NOTICE_PRIVATE_POSSIBLE_END','possible_end':ident,'grade':GRADE}


def private_end_ground(memories,end,aid,location,clock):
    if end.get('genesis_family')!='ACTUAL_PRIVATE_REHEARSAL':return None
    rows=[r for m in memories if m.get('id')==end.get('private_memory_ref')
          for r in m.get('private_rehearsals',[])
          if r.get('id')==end.get('private_rehearsal_ref') and r.get('actor')==aid
          and r.get('event_ref')==end.get('origin_event')
          and r.get('experience_ref')==end.get('experience_ref')
          and r.get('location')==location==end.get('private_location')
          and r.get('clock',clock)<=clock
          and r.get('affect_ref')==end.get('private_affect_ref')]
    return rows[0] if len(rows)==1 else None
