"""HQ324 P1 source-free LLM alternative seam. No owner side effects.

A validated proposal is NOT an admitted V3 occurrence or a CAN008/CAN011 effect.
This is a test-only implementation; it cannot confer ADP019/ADP020 authority.
"""
from __future__ import annotations
import copy
import hashlib
import json
import re
from datetime import datetime
from typing import Any

SCHEMA = 'P1_LLM_ALTERNATIVES_PROPOSAL_V1'
CONTEXT_SCHEMA = 'P1_SYNTHETIC_CONTEXT_V1'
POLICY_SCHEMA = 'P1_TEST_ONLY_AUTHORED_SELECTION_POLICY_V1'
MODEL_EPISTEMIC = 'LLM_PROPOSAL'
RNG_GRADE = 'ADP020_COMPATIBILITY_MOCK_TEST_ONLY'
PROB_GRADE = 'PROVISIONAL_NOT_CALIBRATED'
RULE_REF = 'P1_CANDIDATE_ELIGIBILITY_TEST_ONLY@1.0.0'
RULE_HASH = hashlib.sha256(RULE_REF.encode()).hexdigest()
_HEX = re.compile(r'^[0-9a-f]{64}$')
_ID = re.compile(r'^[A-Za-z][A-Za-z0-9_.:-]{0,100}$')
_ALLOWED_KINDS = {'OBSERVABLE_UTTERANCE', 'MATERIAL_ACTION_PROPOSAL', 'NONOCCURRENCE'}
_RESERVED = {'admitted_event_id','admission_grade','event_id','world_state','state_delta','actor_delta',
             'CAN008_update','CAN011_update','memory_delta','belief_delta','history_delta',
             'cursor_after','causal_cursor','effect_result','actual_culprit','psychological_truth',
             'probability','weight','weight_units','score','selected','selection'}
_PACKET = {'schema','epistemic_class','proposal_id','proposal_hash','world_ref','context_hash',
           'as_of','model','candidates'}
_CAND = {'candidate_id','family','parent_event_ref','time','place_ref','participants',
         'action_refs','readset','prerequisites','interpretations','courses','possible_effects',
         'prospective_participants',
         'visibility','uncertainty'}
_MODEL = {'provider_label','model_version','prompt_version','prompt_sha256','sampling_record'}
_ACTION = {'actor_ref','opportunity_ref','act_kind'}
_INTERP = {'speaker_actor_ref','utterance','claim','claim_kind','claim_world_fact_ref',
           'accessible_source_refs'}
_COURSE = {'course_id','actor_ref','action_ref','description'}
_EFFECT = {'target_actor_ref','description','owner_required','effect_kind','epistemic_class'}
_PREREQ = {'kind','ref'}
_PROSPECTIVE = {'proposed_ref','role_ref','independent_history_ref','owner_proposal_ref','epistemic_class'}
_KNOWN_REQ = {'WORLD_FACT_TRUE','WORLD_FACT_FALSE','ACTOR_ACCESS','HISTORY_PRESENT',
              'MATERIAL_AFFORDANCE','ABSENT_FACT'}


def canonical(obj: Any) -> bytes:
    """P1-only canonical JSON: JSON I-JSON-shaped scalars; no floats permitted in IDs/weights."""
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                      allow_nan=False).encode('utf-8')


def digest(obj: Any) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def _type_error(code: str, detail: str = '') -> dict:
    return {'decision':'REJECT','code':code,'detail':detail}


def _validate_tree(obj: Any) -> None:
    """Fail closed on strange JSON/Python types or injected forbidden keys anywhere."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if not isinstance(k, str): raise ValueError('NON_STRING_KEY')
            if k in _RESERVED: raise ValueError('FORBIDDEN_OWNER_FIELD:'+k)
            _validate_tree(v)
    elif isinstance(obj, list):
        for v in obj: _validate_tree(v)
    elif isinstance(obj, (str, bool, int)) or obj is None:
        return
    else:
        raise ValueError('UNSUPPORTED_VALUE_TYPE')


def _exact(obj: Any, keys: set, path: str) -> None:
    if not isinstance(obj, dict) or set(obj) != keys:
        raise ValueError('SCHEMA_FIELDS:'+path)


def _valid_id(x: Any) -> bool:
    return isinstance(x, str) and bool(_ID.fullmatch(x))


def _strings(values, *, unique=True):
    return isinstance(values, list) and all(_valid_id(x) for x in values) and (
        not unique or len(values) == len(set(values)))


def _nonempty_string(x: Any) -> bool:
    return isinstance(x,str) and bool(x.strip()) and len(x) <= 4000


def _check_context(ctx: dict) -> None:
    # The external synthetic fixture is the sole read-only factual source in this court.
    _exact(ctx, {'schema','world_ref','as_of','places','facts','people','histories',
                 'actor_access','action_opportunities','material_affordances','allowed_role_refs','context_hash'}, 'context')
    if ctx['schema']!=CONTEXT_SCHEMA or not _valid_id(ctx['world_ref']): raise ValueError('CONTEXT_SCHEMA')
    if not _nonempty_string(ctx['as_of']) or not isinstance(ctx['facts'],dict): raise ValueError('CONTEXT_VALUES')
    if not all(isinstance(ctx[k],dict) for k in ('people','histories','actor_access','action_opportunities')):
        raise ValueError('CONTEXT_MAPS')
    if not _strings(ctx['places']) or not _strings(ctx['material_affordances']) or not _strings(ctx['allowed_role_refs']):raise ValueError('CONTEXT_ARRAYS')
    if digest({k:v for k,v in ctx.items() if k!='context_hash'})!=ctx['context_hash']:
        raise ValueError('CONTEXT_HASH_MISMATCH')
    for actor,person in ctx['people'].items():
        if not _valid_id(actor): raise ValueError('CONTEXT_ACTOR_ID')
        if not isinstance(person,dict) or set(person)!={'role','history_ref'}:raise ValueError('CONTEXT_PERSON')
        history = ctx['histories'].get(person['history_ref'])
        if history is None:raise ValueError('HISTORY_REFERENCE_MISSING')
        if not isinstance(history, dict) or history.get('owner') != actor:
            raise ValueError('CONTEXT_HISTORY_OWNER_MISMATCH')
    for actor,access in ctx['actor_access'].items():
        if actor not in ctx['people'] or not _strings(access):raise ValueError('CONTEXT_ACCESS')
    for key,op in ctx['action_opportunities'].items():
        if not _valid_id(key) or not isinstance(op,dict) or set(op)!={'actor_ref','act_kind','place_ref','time'}:
            raise ValueError('CONTEXT_ACTION_OPPORTUNITY')


def _check_packet(p: dict, ctx: dict) -> None:
    _validate_tree(p)
    _exact(p, _PACKET, 'packet')
    if p['schema']!=SCHEMA or p['epistemic_class']!=MODEL_EPISTEMIC:raise ValueError('PROPOSAL_EPISTEMIC_CLASS')
    if not _valid_id(p['proposal_id']):raise ValueError('PROPOSAL_ID')
    if p['world_ref']!=ctx['world_ref'] or p['as_of']!=ctx['as_of']:
        raise ValueError('WORLD_TIME_BINDING')
    if p['context_hash']!=ctx['context_hash']:raise ValueError('CONTEXT_HASH_MISMATCH')
    _exact(p['model'], _MODEL, 'model')
    m=p['model']
    if not all(_nonempty_string(m[k]) for k in ('provider_label','model_version','prompt_version')):
        raise ValueError('MODEL_PROVENANCE')
    if not isinstance(m['prompt_sha256'],str) or not _HEX.fullmatch(m['prompt_sha256']):
        raise ValueError('PROMPT_HASH_MISSING')
    if not isinstance(m['sampling_record'],dict) or not m['sampling_record']:
        raise ValueError('MODEL_SAMPLING_PROVENANCE')
    if not isinstance(p['proposal_hash'],str) or not _HEX.fullmatch(p['proposal_hash']):
        raise ValueError('PROPOSAL_HASH_MISSING')
    if p['proposal_hash'] != digest({k:v for k,v in p.items() if k!='proposal_hash'}):
        raise ValueError('PROPOSAL_HASH_MISMATCH')
    if not isinstance(p['candidates'],list):raise ValueError('CANDIDATE_LIST_REQUIRED')
    ids=[]
    for c in p['candidates']:
        _exact(c,_CAND,'candidate')
        if not _valid_id(c['candidate_id']):raise ValueError('CANDIDATE_ID')
        ids.append(c['candidate_id'])
    if len(set(ids))!=len(ids):raise ValueError('DUPLICATE_CANDIDATE_ID')


def _candidate(c: dict, ctx:dict, p:dict) -> dict:
    cid=c['candidate_id']; base={'candidate_id':cid,'candidate_replay_hash':digest(c)}
    def reject(code): return dict(base,decision='REJECT',code=code)
    def defer(code): return dict(base,decision='DEFER',code=code)
    if c['family'] not in _ALLOWED_KINDS:return reject('UNKNOWN_EVENT_FAMILY')
    if c['time']!=ctx['as_of']:return reject('RETROACTIVE_OR_FUTURE_UNWITNESSED_EVENT')
    if c['place_ref'] not in ctx['places']:return reject('UNKNOWN_PLACE')
    if not _strings(c['participants']) or len(c['participants'])==0:return reject('BAD_PARTICIPANTS')
    prospective=c['prospective_participants']
    if not isinstance(prospective,list):return reject('PROSPECTIVE_PARTICIPANTS_NOT_LIST')
    proposed_ids=[]
    for prospect in prospective:
        try:_exact(prospect,_PROSPECTIVE,'prospective_participant')
        except ValueError:return reject('BAD_PROSPECTIVE_PERSON_SCHEMA')
        if not all(_valid_id(prospect[k]) for k in ('proposed_ref','role_ref','independent_history_ref','owner_proposal_ref')):
            return reject('BAD_PROSPECTIVE_PERSON_REFS')
        if prospect['epistemic_class']!='NEW_ENTITY_CANDIDATE_ONLY':return reject('PROSPECTIVE_PERSON_LAUNDERED_AS_FACT')
        if prospect['role_ref'] not in ctx['allowed_role_refs']:return reject('UNKNOWN_PROSPECTIVE_ROLE')
        if prospect['proposed_ref'] in ctx['people']:return reject('PROSPECTIVE_COLLIDES_WITH_EXISTING_PERSON')
        proposed_ids.append(prospect['proposed_ref'])
    if len(proposed_ids)!=len(set(proposed_ids)):return reject('DUPLICATE_PROSPECTIVE_PERSON')
    if not set(c['participants']).issubset(set(ctx['people'])|set(proposed_ids)):
        return reject('FABRICATED_PARTICIPANT')
    if proposed_ids:
        # Recognition is not genealogy: new people require independently issued
        # identity, separate history and lawful agent permission.
        return defer('PROSPECTIVE_PERSON_AND_HISTORY_OWNER_REQUIRED')
    if not _strings(c['readset']) or not _strings(c['visibility']):return reject('BAD_READSET_OR_VISIBILITY')
    if not set(c['visibility']).issubset(c['participants']):return reject('UNKNOWN_OBSERVER')
    if not isinstance(c['uncertainty'],str) or not c['uncertainty'].strip():return reject('MISSING_UNCERTAINTY')
    if c['parent_event_ref'] not in ctx['facts']:
        return defer('PARENT_EVENT_NOT_ADMITTED')
    event=ctx['facts'][c['parent_event_ref']]
    if event.get('epistemic_class')!='ADMITTED_OBJECTIVE_EVENT' or event.get('occurred') is not True:
        return reject('PARENT_NOT_OBJECTIVE_OCCURRENCE')
    if not set(c['readset']).issubset(ctx['facts']):return defer('SOURCE_READSET_UNRESOLVED')
    if any(ctx['facts'][r].get('epistemic_class')!='ADMITTED_OBJECTIVE_EVENT' for r in c['readset']):
        return reject('CLAIM_AS_OBJECTIVE_WORLD_FACT')
    try:
        now=datetime.fromisoformat(ctx['as_of'].replace('Z','+00:00'))
        facts=[event]+[ctx['facts'][r] for r in c['readset']]
        if any(datetime.fromisoformat(item['time'].replace('Z','+00:00'))>now for item in facts):
            return reject('FUTURE_EVIDENCE_AS_PAST_FACT')
    except (KeyError,TypeError,ValueError):
        return reject('MALFORMED_FACT_TEMPORAL_RECEIPT')
    if any(c['parent_event_ref'] not in ctx['actor_access'].get(a,[]) for a in c['visibility']):
        return reject('ACTOR_VISIBILITY_UNSUPPORTED')
    if not isinstance(c['action_refs'],list) or not isinstance(c['courses'],list):return reject('BAD_ACTION_OR_COURSES')
    if c['family']=='NONOCCURRENCE':
        if c['action_refs'] or c['courses'] or c['interpretations'] or c['possible_effects']:
            return reject('NONOCCURRENCE_WITH_CAUSAL_PAYLOAD')
    elif not c['action_refs']:return reject('NO_INDEPENDENT_ACTION_OPPORTUNITY')
    seen={}
    for action in c['action_refs']:
        try:_exact(action,_ACTION,'action')
        except ValueError:return reject('BAD_ACTION_SCHEMA')
        a=action['actor_ref']; opportunity=action['opportunity_ref']
        if a not in c['participants'] or opportunity in seen:return reject('ACTION_ACTOR_OR_DUPLICATE')
        seen[opportunity]=a
        op=ctx['action_opportunities'].get(opportunity)
        if op is None:return defer('ACTION_OPPORTUNITY_UNRESOLVED')
        if op != {'actor_ref':a,'act_kind':action['act_kind'],
                  'place_ref':c['place_ref'],'time':c['time']}:
            return reject('ACTION_OPPORTUNITY_MISMATCH')
    if not isinstance(c['prerequisites'],list) or not isinstance(c['interpretations'],list):return reject('BAD_PREREQUISITES_OR_INTERPRETATIONS')
    for req in c['prerequisites']:
        try:_exact(req,_PREREQ,'prerequisite')
        except ValueError:return reject('BAD_PREREQUISITE_SCHEMA')
        kind,r=req['kind'],req['ref']
        if kind not in _KNOWN_REQ:return reject('UNREGISTERED_PREREQUISITE_RULE')
        if kind=='HISTORY_PRESENT':
            if not isinstance(r,str) or '|' not in r:return reject('BAD_HISTORY_BINDING')
            actor,history=r.split('|',1)
            if actor not in c['participants']:return reject('FOREIGN_PRIVATE_HISTORY')
            if history not in ctx['histories']:return defer('HISTORY_NOT_AVAILABLE')
            if ctx['histories'][history].get('owner') != actor:
                return reject('FOREIGN_ACTOR_HISTORY_OWNERSHIP')
            if ctx['people'][actor]['history_ref']!=history:return reject('HISTORY_BINDING_FALSE')
            continue
        if kind=='ACTOR_ACCESS':
            if not isinstance(r,str) or '|' not in r:return reject('BAD_ACCESS_REF')
            a,ref=r.split('|',1)
            if a not in c['participants']:return reject('FOREIGN_PRIVATE_ACCESS')
            if ref not in ctx['facts']:return defer('ACCESS_FACT_UNRESOLVED')
            if ref not in ctx['actor_access'].get(a,[]):return reject('ACTOR_KNOWLEDGE_LIMIT')
            continue
        if kind=='MATERIAL_AFFORDANCE':
            if r not in ctx['material_affordances']:return reject('MATERIAL_PREREQUISITE_FALSE')
            continue
        if kind=='ABSENT_FACT':
            if r in ctx['facts']:return reject('ABSENCE_PREREQUISITE_FALSE')
            continue
        if r not in ctx['facts']:return defer('FACT_PREREQUISITE_UNRESOLVED')
        actual=bool(ctx['facts'][r].get('occurred'))
        if kind in ('WORLD_FACT_TRUE','WORLD_FACT_FALSE') and (ctx['facts'][r].get('epistemic_class') != 'ADMITTED_OBJECTIVE_EVENT'
           or type(ctx['facts'][r].get('occurred')) is not bool):
            return reject('PREREQUISITE_NOT_OBJECTIVE_WORLD_FACT')
        if (kind=='WORLD_FACT_TRUE' and not actual) or (kind=='WORLD_FACT_FALSE' and actual):
            return reject('WORLD_PREREQUISITE_FALSE')
    if not isinstance(c['courses'],list):return reject('COURSES_NOT_LIST')
    courses=set()
    for course in c['courses']:
        try:_exact(course,_COURSE,'course')
        except ValueError:return reject('BAD_COURSE_SCHEMA')
        if course['course_id'] in courses:return reject('DUPLICATE_COURSE')
        courses.add(course['course_id'])
        if course['actor_ref'] not in c['participants'] or course['action_ref'] not in seen:
            return reject('UNAUTHORIZED_COURSE_ACTION')
        if seen[course['action_ref']] != course['actor_ref']:
            return reject('CROSS_ACTOR_COURSE_ACTION_FORBIDDEN')
        if not _nonempty_string(course['description']):return reject('EMPTY_COURSE')
    if not isinstance(c['interpretations'],list):return reject('INTERPRETATIONS_NOT_LIST')
    speaking_actors={act['actor_ref'] for act in c['action_refs'] if act['act_kind'].startswith('SPEAK_')}
    for interpretation in c['interpretations']:
        try:_exact(interpretation,_INTERP,'interpretation')
        except ValueError:return reject('BAD_INTERPRETATION_SCHEMA')
        who=interpretation['speaker_actor_ref']
        if who not in c['participants']:return reject('UNBOUND_INTERPRETATION_SOURCE')
        if who not in speaking_actors:return reject('UNAUTHORIZED_INTERPRETIVE_SPEECH')
        if not _nonempty_string(interpretation['utterance']) or not _nonempty_string(interpretation['claim']):
            return reject('EMPTY_INTERPRETIVE_UTTERANCE')
        if interpretation['claim_kind']!='ATTRIBUTED_UNVERIFIED_ASSERTION' or interpretation['claim_world_fact_ref'] is not None:
            return reject('CLAIM_LAUNDERED_INTO_OBJECTIVE_FACT')
        refs=interpretation['accessible_source_refs']
        if not _strings(refs) or not set(refs).issubset(ctx['actor_access'].get(who, [])):
            return reject('SPEAKER_PRIVATE_KNOWLEDGE_FORGED')
    if not isinstance(c['possible_effects'],list):return reject('EFFECTS_NOT_LIST')
    for effect in c['possible_effects']:
        try:_exact(effect,_EFFECT,'effect')
        except ValueError:return reject('BAD_EFFECT_SCHEMA')
        if effect['target_actor_ref'] not in c['participants']:
            return reject('FOREIGN_ACTOR_EFFECT')
        if effect['owner_required']!='CAN011_EXTERNAL_OWNER' or effect['epistemic_class']!='HYPOTHESIS_ONLY':
            return reject('DIRECT_PSYCHIC_MUTATION_FORBIDDEN')
        if effect['effect_kind'] not in ('MAY_REVISE_PRACTICE','MAY_RETAIN_CONTRADICTION','NO_CHANGE'):
            return reject('UNREGISTERED_DURABLE_EFFECT')
        if not _nonempty_string(effect['description']):return reject('EMPTY_EFFECT_HYPOTHESIS')
    return dict(base,decision='ADMIT',code='PROPOSAL_CANDIDATE_ONLY_NOT_CAUSAL')


def evaluate(packet: dict, context: dict, *, prior_proposals:dict|None=None) -> dict:
    """Immutable test-only evaluation. Never applies events or effects."""
    p=copy.deepcopy(packet); ctx=copy.deepcopy(context)
    try:
        _check_context(ctx);_check_packet(p,ctx)
        if prior_proposals is not None:
            if not isinstance(prior_proposals,dict):raise ValueError('BAD_PRIOR_PROPOSAL_REGISTRY')
            old=prior_proposals.get(p['proposal_id'])
            if old is not None and old!=p['proposal_hash']:
                raise ValueError('INVALID_PROPOSAL_ID_CONTENT_COLLISION')
    except (ValueError, TypeError, KeyError, OverflowError) as exc:
        return {'decision':'REJECT','code':'PACKET_INTEGRITY_OR_SCHEMA_FAILURE',
                'detail':str(exc),'candidates':[],'candidate_set_hash':None,
                'consumption':None,'event_admission':'NOT_PERFORMED'}
    decisions=sorted((_candidate(c,ctx,p) for c in p['candidates']),key=lambda x:x['candidate_id'].encode())
    admitted=[d for d in decisions if d['decision']=='ADMIT']
    entries=[{'candidate_id':d['candidate_id'],'candidate_replay_hash':d['candidate_replay_hash'],
              'candidate_authority_id':RULE_REF,'candidate_authority_version':'1.0.0',
              'eligibility_or_admission_receipt_hash':digest(d)} for d in admitted]
    set_hash=hashlib.sha256(b'P1_CANDIDATE_SET_V1\0'+canonical(entries)).hexdigest()
    status=('DEFER' if any(d['decision']=='DEFER' for d in decisions) else
            'VALID_EMPTY' if not admitted else 'ADMIT')
    result={'decision':status,'code':'P1_NONCAUSAL_ELIGIBILITY_COURT',
            'proposal_id':p['proposal_id'],'proposal_hash':p['proposal_hash'],
            'context_hash':ctx['context_hash'],'rule_ref':RULE_REF,'rule_hash':RULE_HASH,
            'candidates':decisions,'eligible_entries':entries,'candidate_set_hash':set_hash,
            'consumption':None,'event_admission':'NOT_PERFORMED'}
    # Detect accidental/downstream modification of the pure evaluation before
    # test selection; this is an unkeyed test-only receipt, not an owner grant.
    result['evaluation_hash']=digest(result)
    return result


def select_test_only(evaluation:dict, policy:dict, *,seed_hex:str, coordinate:int) -> dict:
    """Synthetic deterministic draw; never native ADP020 and never causal admission."""
    if not isinstance(evaluation,dict) or not isinstance(evaluation.get('decision'),str):
        return {'decision':'REJECT','reason':'EVALUATION_RECEIPT_INTEGRITY_FAILURE',
                'consumption':None}
    if evaluation['decision']!='ADMIT':
        return {'decision':evaluation['decision'],'selected_candidate_id':None,
                'draw_consumed':False,'reason':'NO_COMPLETE_LAWFUL_CANDIDATE_SET',
                'consumption':None}
    try:
        provided=evaluation['evaluation_hash']
        recomputed=digest({k:v for k,v in evaluation.items() if k!='evaluation_hash'})
        entries=evaluation['eligible_entries']
        admitted=evaluation['candidates']
        expected=[{'candidate_id':d['candidate_id'],'candidate_replay_hash':d['candidate_replay_hash'],
                   'candidate_authority_id':RULE_REF,'candidate_authority_version':'1.0.0',
                   'eligibility_or_admission_receipt_hash':digest(d)} for d in admitted if d['decision']=='ADMIT']
        expected.sort(key=lambda x:x['candidate_id'].encode('utf-8'))
        set_hash=hashlib.sha256(b'P1_CANDIDATE_SET_V1\0'+canonical(entries)).hexdigest()
        good=(isinstance(provided,str) and bool(_HEX.fullmatch(provided)) and
              provided==recomputed and entries==expected and bool(entries) and
              set_hash==evaluation['candidate_set_hash'] and
              evaluation['event_admission']=='NOT_PERFORMED' and
              evaluation['consumption'] is None and
              evaluation['rule_ref']==RULE_REF and evaluation['rule_hash']==RULE_HASH)
        if not good:raise ValueError('EVALUATION_NOT_COHERENT')
    except (ValueError,KeyError,TypeError,OverflowError):
        return {'decision':'REJECT','reason':'EVALUATION_RECEIPT_INTEGRITY_FAILURE',
                'consumption':None}
    ids=[x['candidate_id'] for x in entries]
    if not isinstance(policy,dict) or set(policy)!={'schema','policy_id','policy_version','parameter_source',
        'calibration_grade','candidate_set_hash','weight_units','policy_hash'}:
        return {'decision':'DEFER','reason':'SELECTION_POLICY_SCHEMA_MISSING','consumption':None}
    if (policy['schema']!=POLICY_SCHEMA or policy['calibration_grade']!=PROB_GRADE or
        policy['parameter_source']!='AUTHORED_DESIGN_HYPOTHESIS_TEST_ONLY' or
        not _valid_id(policy['policy_id']) or not _nonempty_string(policy['policy_version'])):
        return {'decision':'DEFER','reason':'NUMERIC_AUTHORITY_NOT_GRANTED','consumption':None}
    if policy['policy_hash']!=digest({k:v for k,v in policy.items() if k!='policy_hash'}):
        return {'decision':'REJECT','reason':'SELECTION_POLICY_HASH_MISMATCH','consumption':None}
    if policy['candidate_set_hash']!=evaluation['candidate_set_hash']:
        return {'decision':'REJECT','reason':'CANDIDATE_SET_DIVERGENCE','consumption':None}
    weights=policy['weight_units']
    if not isinstance(weights,dict) or set(weights)!=set(ids) or any(type(v)!=int or v<0 for v in weights.values()):
        return {'decision':'DEFER','reason':'UNLICENSED_OR_INCOMPLETE_WEIGHT_UNITS','consumption':None}
    total=sum(weights.values())
    if total > (1 << 256):
        return {'decision':'DEFER','reason':'TEST_ONLY_WEIGHT_DOMAIN_EXCEEDED','consumption':None}
    if not total:return {'decision':'VALID_EMPTY','reason':'ALL_ZERO_TEST_WEIGHTS_NO_DRAW','consumption':None,
                         'draw_consumed':False,'selected_candidate_id':None}
    if type(coordinate)!=int or coordinate<0 or not isinstance(seed_hex,str) or not _HEX.fullmatch(seed_hex):
        return {'decision':'DEFER','reason':'SEED_OR_COORDINATE_MISSING','consumption':None}
    positive=[x for x in ids if weights[x]>0]
    positive.sort(key=lambda s:s.encode('utf-8'))
    chosen=positive[0] if len(positive)==1 else None
    draw=None
    if len(positive)>1:
        # Rejection sampling over counter-derived 256-bit blocks prevents modulo bias.
        bound=(1<<256)//total*total
        for attempt in range(10000):
            entropy=hashlib.sha256(b'P1_TEST_ONLY_SELECTION_V1\0'+bytes.fromhex(seed_hex)+
                canonical({'coordinate':coordinate,'attempt':attempt,'policy_hash':policy['policy_hash'],
                           'candidate_set_hash':evaluation['candidate_set_hash']})).digest()
            value=int.from_bytes(entropy,'big')
            if value<bound:
                draw={'counter_attempt':attempt,'uniform_below':value%total,
                      'entropy_sha256':hashlib.sha256(entropy).hexdigest()}
                break
        if draw is None:return {'decision':'DEFER','reason':'RNG_REJECTION_BUDGET_EXCEEDED','consumption':None}
        ticket=draw['uniform_below']
        for cid in positive:
            if ticket < weights[cid]:chosen=cid;break
            ticket-=weights[cid]
    rng={'algorithm':RNG_GRADE,'static_stream':'p1.test.causal.alternative',
         'seed_source':'EXPLICIT_TEST_ONLY_SEED','seed_sha256':hashlib.sha256(bytes.fromhex(seed_hex)).hexdigest(),
         'coordinate':coordinate,'draw_consumed':draw is not None,'draw':draw,
         'probability_grade':PROB_GRADE,'parameter_source':policy['parameter_source'],
         'weight_units':{x:weights[x] for x in sorted(weights)},'total_weight_units':total,
         'policy_hash':policy['policy_hash'],'candidate_set_hash':evaluation['candidate_set_hash']}
    replay=digest({'candidate_set_hash':evaluation['candidate_set_hash'],'context_hash':evaluation['context_hash'],
                   'rule_ref':RULE_REF,'policy_hash':policy['policy_hash'],'rng':rng,'selection':chosen})
    return {'decision':'ADMIT','code':'TEST_ONLY_SELECTED_NONCAUSAL_ALTERNATIVE',
            'selected_candidate_id':chosen,'draw_consumed':draw is not None,
            'rng_receipt':rng,'replay_identity':replay,
            'consumption':{'contract':'BFirstCandidateDecision_PROVISIONAL_P1',
                'candidate_id':chosen,'event_admission':'NOT_PERFORMED',
                'actor_response_rule_ref':None,'recruited_source_refs':[],
                'competing_influence_refs':[],'response_effect_proposals':[],
                'target_CAN011_update_proposals':[],'probability_grade':PROB_GRADE,
                'model_proposal_provenance':evaluation['proposal_hash'],'negatives':[],
                'rng_receipt':rng,'no_world_or_actor_mutation':True}}


def replay_test_only(previous:dict, evaluation:dict, policy:dict, *,seed_hex:str,coordinate:int)->dict:
    current=select_test_only(evaluation,policy,seed_hex=seed_hex,coordinate=coordinate)
    if not isinstance(previous,dict) or previous != current:
        return {'decision':'REJECT','reason':'TEST_ONLY_REPLAY_DIVERGENCE'}
    return current
