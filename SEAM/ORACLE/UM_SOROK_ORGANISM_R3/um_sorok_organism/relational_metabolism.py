"""Provisional R4/R5 actor-owned historical relational metabolism.

Derived read over already admitted forms and relations. Not an independent
psychic store, social-power issuer, clinical interpretation, or public tip.
"""
from .types import copy, GRADE, stable_id
from .organism import ACTIONS

RELATIONS=frozenset(('RECRUITS','SUPPORTS','INHIBITS','COMPETES','CONTRADICTS',
 'DERIVED_FROM','REINFORCES','LICENSES','JUSTIFIES','SUBORDINATES','SUPPRESSES',
 'COMPENSATES_FOR','RATIONALIZES','INTERPRETS_THROUGH','CONFLICTS_WITH',
 'QUARANTINES_FROM','ACTIVATES','INSTRUMENTALIZES','MUTUALLY_REINFORCES',
 'MUTUALLY_CONSTRAINS','REVALUES'))
EFFECTS=frozenset(('ACTION_CURRENT','RELATION_MEDIATION','RECRUIT_FORM'))
class InvalidRelationalMotif(ValueError): pass

def link_ref(link):
    return link.get('id') or stable_id('psychic_relation',{
        'source':link['source'],'target':link['target'],
        'relation':link['relation'],'origin':link.get('origin',[])})

def validate_motif(motif,forms):
    if type(motif) is not dict: raise InvalidRelationalMotif('INVALID_MOTIF')
    sources=motif.get('source_forms')
    if (type(sources) is not list or not 2<=len(sources)<=4 or
        any(type(s) is not str or s not in forms for s in sources) or
        len(set(sources))!=len(sources)):
        raise InvalidRelationalMotif('MOTIF_REQUIRES_TWO_TO_FOUR_ACQUIRED_FORMS')
    if any(not forms[s].get('origin') for s in sources):
        raise InvalidRelationalMotif('MOTIF_REQUIRES_ACTUAL_FORM_ANCESTRY')
    cue=motif.get('cue_terms',[]); loc=motif.get('locations',[])
    if (type(cue) is not list or type(loc) is not list or len(cue)>20 or
        len(loc)>12 or any(type(v) is not str or not v for v in cue+loc)):
        raise InvalidRelationalMotif('INVALID_MOTIF_CONTEXT')
    effects=motif.get('effects',[])
    if type(effects) is not list or not 1<=len(effects)<=8:
        raise InvalidRelationalMotif('MOTIF_REQUIRES_BOUNDED_EFFECTS')
    for e in effects:
        if type(e) is not dict or e.get('kind') not in EFFECTS:
            raise InvalidRelationalMotif('INVALID_MOTIF_EFFECT')
        if e['kind']=='ACTION_CURRENT':
            if e.get('action') not in ACTIONS or e.get('polarity') not in ('APPROACH','WITHHOLD'):
                raise InvalidRelationalMotif('MOTIF_ACTION_NOT_QUALIFIED')
        elif e['kind']=='RELATION_MEDIATION':
            if (e.get('source') not in sources or e.get('target') not in sources or
                    e['source']==e['target'] or e.get('relation') not in RELATIONS):
                raise InvalidRelationalMotif('MOTIF_RELATION_NOT_QUALIFIED')
        else:
            target=e.get('target_form')
            if (type(target) is not str or target not in forms or
                    target in sources or not forms[target].get('origin')):
                raise InvalidRelationalMotif('MOTIF_RECRUITMENT_TARGET_UNQUALIFIED')
    if motif.get('status','ACTIVE') not in ('ACTIVE','DORMANT'):
        raise InvalidRelationalMotif('INVALID_MOTIF_STATUS')
    return True

def _context(m,access,tags):
    if m.get('contexts') and access.location not in m['contexts']:return False
    if m.get('locations') and access.location not in m['locations']:return False
    if m.get('cue_terms') and not (set(s.lower() for s in m['cue_terms'])&tags):return False
    return True

def derive_relational_metabolism(constitution,access,active_forms,inhibited):
    forms=constitution.forms;active=set(active_forms);blocked=set(inhibited)&set(forms)
    situated=active|blocked
    tags={str(v).lower() for cue in access.cues for v in cue.get('tags',[])+[cue.get('kind','')]}
    currents=[];actions=[];recruits=[];readset=set()
    for link in constitution.links:
        if (link.get('source') not in situated or link.get('target') not in situated or
             link.get('relation') not in RELATIONS or not _context(link,access,tags)):
            continue
        ref=link_ref(link);readset.add(ref)
        currents.append({'kind':'OPERATIVE_RELATION' if link['source'] in active and link['target'] in active else 'INDIRECT_INHIBITED_RELATION',
           'relation_ref':ref,'relation':link['relation'],'source_form_ref':link['source'],
           'target_form_ref':link['target'],'source_directly_recruited':link['source'] in active,
           'target_directly_recruited':link['target'] in active,'grade':GRADE})
    for motif in getattr(constitution,'relational_motifs',[]):
        validate_motif(motif,forms)
        if motif.get('status','ACTIVE')!='ACTIVE' or not _context(motif,access,tags):continue
        sources=set(motif['source_forms'])
        if not sources<=situated or not sources&active:continue
        ref=motif['id'];readset.add(ref)
        currents.append({'kind':'ACQUIRED_RELATIONAL_CONFIGURATION','motif_ref':ref,
           'source_form_refs':sorted(sources),'inhibited_source_refs':sorted(sources&blocked),
           'origin':copy(motif.get('origin',[])),'not_a_self_known_reason':True,'grade':GRADE})
        for e in motif['effects']:
            if e['kind']=='ACTION_CURRENT':
                actions.append({'action':e['action'],'polarity':e['polarity'],
                  'motif_ref':ref,'source_form_refs':sorted(sources),
                  'has_inhibited_source':bool(sources&blocked)})
            elif e['kind']=='RECRUIT_FORM':
                recruits.append({'target_form':e['target_form'],'motif_ref':ref,
                  'source_form_refs':sorted(sources),
                  'had_inhibited_source':bool(sources&blocked),'grade':GRADE})
            else:
                currents.append({'kind':'ACQUIRED_PERSONAL_SENSE_MEDIATION',
                  'motif_ref':ref,'source_form_ref':e['source'],
                  'target_form_ref':e['target'],'relation':e['relation'],
                  'no_automatic_motive_fulfillment':True,'grade':GRADE})
    return {'currents':currents,'action_currents':actions,
            'recruitment_candidates':recruits,'readset':sorted(readset),'grade':GRADE,
            'not_a_clinical_unconscious_etiology':True}

def admit_motif(actor,candidate,event_ref,experience,index):
    motif=copy(candidate.get('motif',{}));validate_motif(motif,actor['forms'])
    if not experience.get('participated') and not experience.get('perceived_cues'):
        raise InvalidRelationalMotif('MOTIF_HAS_NO_ACTOR_EXPERIENCE')
    if len(actor.get('relational_motifs',[]))>=256:
        raise InvalidRelationalMotif('MOTIF_STORAGE_BUDGET')
    motif['id']=stable_id('relational_motif',{'actor':actor['id'],'event':event_ref,
        'index':index,'sources':sorted(motif['source_forms']),'effects':motif['effects']})
    if any(m.get('id')==motif['id'] for m in actor.get('relational_motifs',[])):
        raise InvalidRelationalMotif('DUPLICATE_RELATIONAL_MOTIF')
    motif['origin']=[event_ref];motif['experience_ref']=experience['ref']
    motif['grade']=GRADE;motif['status']='ACTIVE'
    motif['not_a_validated_unconscious_explanation']=True
    motif.setdefault('cue_terms',[]);motif.setdefault('locations',[])
    return motif
