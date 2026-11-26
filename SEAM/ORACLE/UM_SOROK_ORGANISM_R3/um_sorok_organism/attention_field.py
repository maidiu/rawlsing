"""SORACLE R11 / Astra 1,5,16,20: attention is a scarce situated mediation.

The world owns material signals; actor_access owns *receivable* signals; this
read-only projection identifies some candidates for focal practical appraisal.
It neither claims an actor consciously attended the selected cues nor deletes
pre-attentive sensitivity. In particular, analyst cue tags are not infant words.

One historical experience may yield multiple accessible signs; exhausted
attention must not turn an unprocessed sign into absent psychology. Preserve
weak and contradictory cues without counting repeated descriptions as votes.
SOURCEFREE; no native CAN/ADP authority, no scientific learning law.
"""
from collections import Counter
from dataclasses import replace
from .types import copy, GRADE


def _bounded_unit(body, name, default):
    value = body.get(name, default)
    if type(value) not in (int,float) or not 0 <= value <= 1:
        raise ValueError('ATTENTION_INVALID_BODY_'+name.upper())
    return value


def _feature(cue, language):
    # The actor may discriminate a modality before possessing the observer's
    # cultural categories. The model's private lexical labels cannot silently
    # become the preverbal person's own sensorium.
    modality = cue.get('modality','unknown')
    if language < .25:
        return ('sensory:'+modality,) if modality in (
            'auditory','visual','tactile','olfactory','present') else ()
    terms = cue.get('tags', [])
    if not isinstance(terms, list):
        terms = []
    return tuple(sorted(set(t.casefold() for t in terms
                  if type(t) is str and t.strip())))[:24]


def situate_attention(constitution, access, *, ceiling=8, historical=None):
    if constitution.actor != access.actor:
        raise ValueError('ATTENTION_FOREIGN_ACTOR')
    if type(ceiling) is not int or ceiling < 2 or ceiling > 32:
        raise ValueError('ATTENTION_INVALID_CEILING')
    body = constitution.body
    language = _bounded_unit(body,'language',0)
    rest = _bounded_unit(body,'rest',.5)
    comfort = _bounded_unit(body,'comfort',.5)
    arousal = _bounded_unit(body,'arousal',.5)
    # A *policy* for scarce semantic focus; not a measured human span or
    # proof that the actor has ignored a receivable event.
    load = int(rest < .35) + int(comfort < .3) + int(arousal > .78)
    live_projects = [p for p in constitution.projects
                     if p.get('status','active')=='active']
    load += min(2, len(live_projects)//3)
    capacity = max(2, min(ceiling, ceiling-load))
    cues = [c for c in access.cues if type(c) is dict and
            type(c.get('id')) is str]
    if not cues:
        return {'focus_access':replace(access,cues=[]),
                'frame':{'actor':access.actor,'clock':access.world_clock,
                         'focally_eligible_cue_refs':[],
                         'accessible_but_not_focally_selected_refs':[],
                         'coverage':'NO_PRESENT_CUES',
                         'grade':GRADE,'not_a_conscious_attention_report':True}}
    # Distinguish historical *exercise* from source frequency of presentation.
    # A cue frequently encountered may be routinized, but absence in a sample
    # of received cues is not evidence it never mattered.
    exposure = Counter()
    for ep in constitution.evidence_paths[-256:]:
        for t in set(ep.get('received_cue_tags',[])):
            if type(t) is str:
                exposure[t.casefold()] += 1
    project_terms = set()
    for p in live_projects:
        project_terms.update(t.casefold() for t in p.get('cue_terms',[])
                             if type(t) is str)
    active_forms = [f for f in constitution.forms.values()
                    if f.get('lifecycle','ACTIVE')=='ACTIVE']
    form_terms = set(t.casefold() for f in active_forms
                     for t in f.get('cues',[]) if type(t) is str)
    historical_modalities={x.get('source_modality') for x in
        (historical or {}).get('currents',[]) if type(x.get('source_modality')) is str}
    evaluated = []
    for index,cue in enumerate(cues):
        tokens = _feature(cue,language)
        known = bool(set(tokens)&form_terms) if language >= .25 else False
        purposeful = bool(set(tokens)&project_terms) if language >= .25 else False
        rarity = min((exposure[t] for t in tokens),default=0)
        same_person = cue.get('source_actor') in {
            c.get('source_actor') for c in access.cues
            if c.get('kind')=='coactor_present'}
        # Rank is for resource allocation, not strength of a motive.
        rank = (3 if purposeful else 0) + (2 if known else 0) + (
            1 if same_person else 0) + (
            1 if cue.get('modality') in historical_modalities else 0)
        evaluated.append({'cue':cue,'index':index,'tokens':tokens,
                          'rank':rank,'rarity':rarity,
                          'preverbal_resolution':language < .25})
    # Preserve some rare exposure despite dominant familiar/practical topics.
    high = sorted(evaluated,key=lambda x:(-x['rank'],x['index']))
    rare = sorted(evaluated,key=lambda x:(x['rarity'],x['index']))
    reserve = max(1,capacity//4)
    chosen = []
    def add(entry):
        if entry['cue']['id'] not in {x['cue']['id'] for x in chosen}:
            chosen.append(entry)
    for v in rare[:reserve]: add(v)
    # One existing focal position may be occupied by an acquired, specifically
    # practiced orientation to a present Other. Keep the rarity reserve and
    # total capacity unchanged. This is a bounded policy, not proof of
    # compulsive attention or a universal conservation law.
    monitoring = []
    for row in getattr(constitution, 'historical_orientations', []):
        if (row.get('actor') != constitution.actor
                or row.get('acquisition') != 'LIVED_DIRECTED_MONITORING_PRACTICE'
                or row.get('location') != access.location
                or (row.get('revisions') and row['revisions'][-1]['mode'] == 'INHIBIT')):
            continue
        other = row.get('monitoring_basis', {}).get('counterpart_ref')
        for entry in high:
            if (entry['cue'].get('kind') == 'coactor_present'
                    and entry['cue'].get('source_actor') == other):
                monitoring.append((row['id'], entry))
    monitoring_refs = []
    if monitoring and len(chosen) < capacity:
        ref, entry = sorted(monitoring, key=lambda pair: pair[0])[0]
        add(entry)
        monitoring_refs.append(ref)
    for v in high:
        if len(chosen)>=capacity: break
        add(v)
    selected = {x['cue']['id'] for x in chosen}
    focal = [c for c in cues if c['id'] in selected]
    omitted = [c for c in cues if c['id'] not in selected]
    return {
        'focus_access': replace(access,cues=copy(focal)),
        'frame':{
            'actor':access.actor,'clock':access.world_clock,
            'focally_eligible_cue_refs':[c['id'] for c in focal],
            'accessible_but_not_focally_selected_refs':[c['id'] for c in omitted],
            'focal_capacity_provisional':capacity,
            'competing_project_count':len(live_projects),
            'somatic_load_components':load,
            'preverbal_tags_not_cognitive_categories':language < .25,
            'nonselected_cues_not_conclusively_unnoticed':True,
            'pre_attentive_recruitment_uses_full_access':True,
            'historical_sensory_bias_is_provisional':bool(historical_modalities),
            'requires_independent_actor_learning_for_durable_bias':True,
            'budget_policy_not_a_human_attention_law':True,
            **({'monitoring_orientation_refs': monitoring_refs,
                'monitoring_focus_is_not_actual_attention': True}
               if monitoring_refs else {}),
            'grade':GRADE,
        }
    }


# Explicitly undertaken focal reception is distinct from the read-only
# attention budget. The producer's authored act and the recipient's own
# experienced sign must remain two different historical events.
from .types import stable_id

def offer_undertaking_attention(actor, world, access, focal_refs):
    """Existing actor pledge and R24 visitor undertaking, one recipient law.

    Objective history validates provenance; only the already eligible
    outward sign supplies content. Neither its deadline outcome nor the
    Other's intentions enter the option. No new world write.
    """
    aid=actor['id'];clock=world['clock'];location=access.location
    if access.actor!=aid or access.world_clock!=clock:return []
    if actor['body'].get('language',0)<.35:return []
    out=[]
    for cue in access.cues:
        if cue.get('id') not in focal_refs:continue
        kind=cue.get('kind')
        if kind=='visitor_offer_undertaking':
            # This is the exact source contract of NEIGHBOR R24, not a
            # synthetic Other or new human contribution writer.
            ev=[e for e in world.get('neighbor_user_events',[])
                if e.get('event_ref')==cue.get('visitor_event_ref')
                and e.get('operation')=='PLEDGE_OFFER' and e.get('status')=='PERFORMED'
                and e.get('target_actor_ref')==aid and e.get('destination')==location
                and e.get('user')==cue.get('visitor_ref')
                and e.get('clock')==cue.get('clock')
                and e.get('human_offer_commitment_ref')==cue.get('commitment_ref')
                and any(x.get('actor')==aid and x.get('cue_ref')==cue['id']
                        and x.get('event_ref')==e['event_ref']
                        and x.get('basis')==kind for x in e.get('perceptual_candidates',[]))]
            if len(ev)!=1:continue
            e=ev[0];other=e['user'];source=e['event_ref'];commit=e['human_offer_commitment_ref']
            if not isinstance(commit,str) or not commit:continue
            if not any(o.get('id')==commit and o.get('kind')=='HUMAN_PROMISED_FOOD_OFFER'
                       and o.get('responsible_actor')==other and o.get('recipient')==aid
                       and o.get('source_user_event_ref')==source
                       for o in world.get('scheduled_obligations',[])):continue
            family='HUMAN_AUTHORED_NEIGHBOR'
        elif kind=='performed_pledge_care':
            ev=[e for e in world.get('public_history',[])
                if e.get('action')=='PLEDGE_CARE' and e.get('status')=='PERFORMED'
                and e.get('actor')==cue.get('source_actor')
                and e.get('target')==aid and e.get('clock')==cue.get('clock')
                and e.get('future_care_obligation_ref')]
            if len(ev)!=1:continue
            e=ev[0];other=e['actor'];commit=e['future_care_obligation_ref']
            if not any(o.get('id')==commit and o.get('kind')=='ACTOR_PROMISED_FUTURE_CARE'
                       and o.get('responsible_actor')==other and o.get('recipient')==aid
                       and o.get('origin_clock')==e['clock']
                       for o in world.get('scheduled_obligations',[])):continue
            source=commit
            family='INDEPENDENT_COMPUTATIONAL_ACTOR'
        else:continue
        if type(other) is not str or other==aid:continue
        if any(x.get('undertaking_attention',{}).get('commitment_ref')==commit
               for x in actor.get('evidence_paths',[])):continue
        # Never include status, fulfilment, internal deadline settlement, or
        # the objective proposition as if it were already actor knowledge.
        basis={'actor':aid,'as_of_clock':clock,'location':location,
               'cue_ref':cue['id'],'counterpart_ref':other,'source_kind':family,
               'source_event_ref':source,'commitment_ref':commit}
        out.append({**basis,'attention_id':stable_id('undertaking_attention',basis),
                    'operation':'ORIENT','outward_sign':copy(cue),
                    'not_understanding_consent_or_future_outcome':True,'grade':GRADE})
        if len(out)>=8:break
    return out


def received_undertaking_attention(actor, selection, experience):
    """Recompute the exact selected-sign receipt for atomic memory admission."""
    chosen=(selection or {}).get('undertaking_attention')
    if not isinstance(chosen,dict):return None
    if (selection.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or selection.get('actor')!=actor['id'] or chosen.get('actor')!=actor['id']
            or experience.get('actor')!=actor['id']
            or experience.get('own_action')!='ORIENT' or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True
            or experience.get('clock')!=chosen.get('as_of_clock',-2)+1
            or experience.get('location')!=chosen.get('location')
            or selection.get('selected_project_refs')!=[]
            or selection.get('possible_end_trial') is not None):return None
    cue=chosen.get('outward_sign')
    if not isinstance(cue,dict) or cue.get('id')!=chosen.get('cue_ref'):return None
    if sum(c==cue for c in experience.get('perceived_cues',[]))!=1:return None
    return {k:copy(chosen[k]) for k in ('attention_id','actor','cue_ref',
                'source_event_ref','commitment_ref','source_kind','counterpart_ref',
                'location','as_of_clock')}


def offer_correspondence_attention(actor,world,access):
    """Recipient-only opportunity to open delivered text on a qualified device.
    Only metadata crosses the selection boundary, never unread body text.
    Existing ORIENT selection/admission owns the consequential choice.
    """
    aid=actor['id']
    if access.actor!=aid or access.world_clock!=world['clock']:return []
    body=actor['body']
    if body.get('language',0)<.35 or body.get('sensor',0)<.05:return []
    geometry=world.get('neighbor_sensory_source',{})
    view=geometry.get('actor_conditions',{}).get(aid,{})
    if (geometry.get('grade')!='SOURCEFREE_TEST_ONLY' or view.get('visual') is not True
            or view.get('light')!='lit' or view.get('sightline')!='unobstructed'):
        return []
    out=[]
    routes=world.get('neighbor_correspondence_routes',{})
    for key,row in sorted(world.get('neighbor_correspondence',{}).items()):
        route=routes.get(row.get('route_ref'),{})
        if (key!=row.get('id') or row.get('recipient')!=aid
                or route.get('recipient')!=aid or route.get('sender')!=row.get('sender')
                or route.get('device_site')!=access.location
                or type(row.get('delivered_clock')) is not int
                or row['delivered_clock']>world['clock']
                or row.get('opened_clock') is not None):continue
        basis={'actor':aid,'message_ref':key,'route_ref':route['id'],
               'as_of_clock':world['clock'],'location':access.location,
               'sender_label':row['sender'],'delivered_clock':row['delivered_clock']}
        out.append({**basis,'attention_id':stable_id('correspondence_attention',basis),
                    'operation':'ORIENT','unopened_body_not_available':True})
        if len(out)>=8:break
    return out


def settle_correspondence_attention(world,actor,chosen,summary):
    """Called only after the actual selected ORIENT settles. No inferred reading."""
    from .world import add_cue
    aid=actor['id']
    row=world.get('neighbor_correspondence',{}).get(chosen['message_ref'])
    if (not row or row['recipient']!=aid or row['opened_clock'] is not None
            or row['route_ref']!=chosen['route_ref']
            or row['delivered_clock']!=chosen['delivered_clock']
            or world['clock']!=chosen['as_of_clock']+1
            or summary.get('actor')!=aid or summary.get('action')!='ORIENT'
            or summary.get('status')!='PERFORMED'
            or world['positions'].get(aid)!=chosen['location']):
        raise ValueError('CORRESPONDENCE_OPEN_NOT_QUALIFIED')
    row['opened_clock']=world['clock']
    cue=add_cue(world,'opened_correspondence',['correspondence','written_words'],
                location=chosen['location'],description=row['text'],
                modality='visual',private_to=aid,source_actor=aid)
    cue.update(message_ref=row['id'],route_ref=row['route_ref'],
               sender_label=row['sender'],comprehension='NOT_ESTABLISHED',
               truth_or_reply_not_inferred=True)
    return cue


def received_correspondence_attention(actor,selection,experience):
    chosen=(selection or {}).get('correspondence_attention')
    if not isinstance(chosen,dict):return None
    if (chosen.get('actor')!=actor['id'] or experience.get('actor')!=actor['id']
            or experience.get('own_action')!='ORIENT' or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True
            or experience.get('clock')!=chosen.get('as_of_clock',-2)+1
            or selection.get('selected_project_refs')!=[]
            or selection.get('possible_end_trial') is not None):return None
    matches=[c for c in experience.get('perceived_cues',[])
             if c.get('kind')=='opened_correspondence'
             and c.get('message_ref')==chosen.get('message_ref')
             and c.get('route_ref')==chosen.get('route_ref')]
    if len(matches)!=1:return None
    return {'attention_id':chosen['attention_id'],'message_ref':chosen['message_ref'],
            'route_ref':chosen['route_ref'],'received_cue_ref':matches[0]['id'],
            'actor':actor['id'],'opened_clock':experience['clock'],
            'comprehension_not_established':True}


def offer_focal_encounters(actor, access, focal_refs):
    """A bounded existing ORIENT operation can deliberately receive a present
    coactor sign. Only open this sourcefree family after personally received
    directed imposition; do not infer vigilance from co-presence alone.
    """
    if access.actor != actor['id'] or not any(
            p.get('directed_encounter', {}).get('operation') == 'IMPOSE'
            for p in actor.get('evidence_paths', [])):
        return []
    out = []
    for cue in access.cues:
        if (cue.get('id') not in focal_refs or cue.get('kind') != 'coactor_present'
                or type(cue.get('source_actor')) is not str
                or cue.get('source_actor') == actor['id']
                or cue.get('location') != access.location
                or cue.get('clock') != access.world_clock):
            continue
        basis = {'actor':actor['id'], 'as_of_clock':access.world_clock,
                 'location':access.location, 'cue_ref':cue['id'],
                 'counterpart_ref':cue['source_actor']}
        out.append({**basis, 'attention_id':stable_id('focal_encounter',basis),
                    'operation':'ORIENT', 'outward_sign':copy(cue),
                    'not_private_mind_or_actual_attention_yet':True})
    return out


def received_focal_encounter(actor, selection, experience):
    chosen=(selection or {}).get('focal_encounter')
    if not isinstance(chosen,dict):return None
    if (selection.get('status')!='ACTOR_POLICY_PRACTICAL_ATTEMPT'
            or selection.get('actor')!=actor['id'] or chosen.get('actor')!=actor['id']
            or experience.get('actor')!=actor['id']
            or experience.get('own_action')!='ORIENT'
            or experience.get('status')!='PERFORMED'
            or experience.get('participated') is not True
            or experience.get('clock')!=chosen.get('as_of_clock',-2)+1
            or experience.get('location')!=chosen.get('location')
            or selection.get('selected_project_refs')!=[]
            or selection.get('possible_end_trial') is not None):return None
    cue=chosen.get('outward_sign')
    if (not isinstance(cue,dict) or cue.get('id')!=chosen.get('cue_ref')
            or cue.get('kind')!='coactor_present'
            or cue.get('source_actor')!=chosen.get('counterpart_ref')
            or sum(c==cue for c in experience.get('perceived_cues',[]))!=1):
        return None
    basis={k:copy(chosen[k]) for k in ('actor','as_of_clock','location','cue_ref','counterpart_ref')}
    if chosen.get('attention_id')!=stable_id('focal_encounter',basis):return None
    return {**basis,'attention_id':chosen['attention_id'],
            'received_at_clock':experience['clock'],
            'not_inference_of_other_mind_or_monitoring_motive':True}


def personally_received_directed_act(experience):
    """A target's actual sensed person-directed act, not another's intention."""
    if experience.get('participated') is not True or experience.get('status')!='OBSERVED':
        return None
    if (experience.get('own_action')=='RECEIVED_CARE'
            and experience.get('felt_effect')=='SOMATIC_CARE_CANDIDATE'):
        operation='CARE'
    elif (experience.get('own_action') is None
            and experience.get('felt_effect')=='IMPOSED_EFFECT_UNINTERPRETED'):
        operation='IMPOSE'
    else:return None
    signs=[c for c in experience.get('perceived_cues',[])
           if c.get('kind')=='performed_'+operation.lower()
           and c.get('actor_accessible_target_ref')==experience['actor']
           and c.get('public_person_directed_act_not_private_intention') is True
           and type(c.get('source_actor')) is str and c['source_actor']!=experience['actor']
           and c.get('location')==experience.get('location')
           and c.get('clock')==experience.get('clock')]
    if len(signs)!=1:return None
    return {'actor':experience['actor'],'counterpart_ref':signs[0]['source_actor'],
            'cue_ref':signs[0]['id'],'operation':operation,
            'location':experience['location'],'clock':experience['clock'],
            'not_motive_safety_or_consent':True}


def possible_monitoring_changes(actor, experience, event_ref):
    """Existing historical-orientation owner consumes these qualified options.

    Imposition, two subsequent selected focal encounters, and later two
    actually received relieving care acts license distinct OPTIONAL changes.
    A coactor's favorable act need not heal anyone. No recollection is created.
    """
    if experience.get('actor')!=actor.get('id'):return []
    site=experience.get('location');clock=experience.get('clock')
    if site!=actor.get('location') or type(clock) is not int:return []
    paths=actor.get('evidence_paths',[])
    current=[p for p in paths if p.get('event')==event_ref
             and p.get('experience_ref')==experience.get('ref')]
    if len(current)!=1:return []
    now=current[0]
    focal=now.get('focal_encounter');directed=now.get('directed_encounter')
    if focal and focal!=received_focal_encounter(
            actor,experience.get('own_practical_selection'),experience):return []
    if directed and directed!=personally_received_directed_act(experience):return []
    latest=focal or directed
    if not latest:return []
    other=latest['counterpart_ref']
    def matching(path,key):
        row=path.get(key,{})
        return (row.get('actor')==actor['id'] and row.get('location')==site
                and row.get('counterpart_ref')==other
                and row.get('cue_ref') in path.get('received_cue_refs',[]))
    existing=[r for r in actor.get('historical_orientations',[])
              if r.get('actor')==actor['id'] and r.get('location')==site
              and r.get('acquisition')=='LIVED_DIRECTED_MONITORING_PRACTICE'
              and r.get('monitoring_basis',{}).get('counterpart_ref')==other]
    if len(existing)>1:return []
    row=existing[0] if existing else None
    active=bool(row and (not row['revisions'] or row['revisions'][-1]['mode']!='INHIBIT'))
    cutoff=(row['revisions'][-1]['clock'] if row and row['revisions']
            else row['origin_clock'] if row else -1)
    if type(cutoff) is not int:return []
    directed_paths=[p for p in paths if matching(p,'directed_encounter')
                    and type(p['directed_encounter'].get('clock')) is int
                    and cutoff<p['directed_encounter']['clock']<=clock]
    directed_paths.sort(key=lambda p:p['directed_encounter']['clock'])
    def path_ref(p,key):
        return {'event_ref':p['event'],'experience_ref':p['experience_ref'],
                'cue_ref':p[key]['cue_ref']}
    common={'actor':actor['id'],'location':site,'counterpart_ref':other,
            'not_diagnosis_or_necessary_adaptation':True}
    if focal and not active:
        adverse=[p for p in directed_paths if p['directed_encounter']['operation']=='IMPOSE']
        if not adverse:return []
        prior=adverse[-1];after=prior['directed_encounter']['clock']
        received=[p for p in paths if matching(p,'focal_encounter')
                  and type(p['focal_encounter'].get('received_at_clock')) is int
                  and after<p['focal_encounter']['received_at_clock']<=clock]
        received.sort(key=lambda p:p['focal_encounter']['received_at_clock'])
        if (len(received)<2 or received[-1]!=now
                or received[-2]['event']==event_ref
                or received[-2]['focal_encounter']['received_at_clock']>=clock):
            return []
        basis={**common,'imposition':path_ref(prior,'directed_encounter'),
               'selected_focal_courses':[path_ref(p,'focal_encounter') for p in received[-2:]]}
        if row:
            return [{'kind':'REVISE_HISTORICAL_ORIENTATION','orientation_ref':row['id'],
                     'revision_mode':'REINSTATE','perceived_cue_ref':focal['cue_ref'],
                     'monitoring_revision_basis':basis}]
        return [{'kind':'ACQUIRE_HISTORICAL_ORIENTATION','operation':'ORIENT',
                 'orientation_mode':'APPROACH','perceived_cue_ref':focal['cue_ref'],
                 'monitoring_basis':basis}]
    if directed and directed['operation']=='CARE' and active:
        if len(directed_paths)<2 or directed_paths[-1]!=now:return []
        pair=directed_paths[-2:]
        if (any(p['directed_encounter']['operation']!='CARE' for p in pair)
                or pair[0]['event']==event_ref
                or pair[0]['directed_encounter']['clock']>=clock):return []
        witnesses=actor.get('lived_genesis_episodes',[])
        for p in pair:
            lived=[w for w in witnesses if w.get('actor')==actor['id']
                   and w.get('event_ref')==p['event']
                   and w.get('experience_ref')==p['experience_ref']
                   and p['directed_encounter']['cue_ref'] in w.get('received_sign_refs',[])
                   and w.get('received_relief') and not w.get('personally_lived_adverse_course')]
            if len(lived)!=1:return []
        basis={**common,'orientation_ref':row['id'],
               'received_care_courses':[path_ref(p,'directed_encounter') for p in pair],
               'not_proof_safety_or_global_recovery':True}
        return [{'kind':'REVISE_HISTORICAL_ORIENTATION','orientation_ref':row['id'],
                 'revision_mode':'INHIBIT','perceived_cue_ref':directed['cue_ref'],
                 'monitoring_revision_basis':basis}]
    return []
