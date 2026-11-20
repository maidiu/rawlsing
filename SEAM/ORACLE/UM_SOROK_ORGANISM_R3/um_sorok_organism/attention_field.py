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
            'grade':GRADE,
        }
    }
