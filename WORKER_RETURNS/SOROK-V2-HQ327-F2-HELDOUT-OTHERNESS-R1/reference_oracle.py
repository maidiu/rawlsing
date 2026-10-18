"""F2 held-out source-free court: independent evidence/owner oracle, NOT psychological model.

No B2/M1 imports, learned weights, calibrated probabilities or selected human affect.
A valid receipt proves test-harness evidence/authority preservation, not a person.
"""
from __future__ import annotations
import copy, hashlib, json

SCHEMA='F2_HELDOUT_CASE_V1'
RULE='F2_EVIDENCE_BOUNDARY_R1'
ALLOWED_ACTS={'REPAIR_TOOLS','DECLINE_HELP','SHARED_TASK_CHOICE','SHARED_TASK_OVERRULE','SPEAK','BIKE_CARE','PUBLIC_ECHO','LATER_PROJECT','DECLINE_CONTACT','ALLOW_CONTACT','MATERIAL_LOSS','CAPABILITY_TASK_SUCCESS','CAPABILITY_TASK_FAILURE'}
ALLOWED_VIEW={'OBJECTIVE','HEARD_UTTERANCE','PUBLIC_ACTION','ACTOR_OWN_ACTION'}


def canonical(value):
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode('utf8')

def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()

def denial(code, c, **details):
    return dict(case_id=c['id'], status='REFUSED', code=code, no_mutation=True, **details)

def defer(code,c,**details):
    return dict(case_id=c['id'],status='DEFERRED',code=code,no_mutation=True,**details)

def _valid_witnesses(c):
    w=c['world']; out={}
    for e in w['evidence']:
        if set(['id','actor','act','time','owner','source','object','hash'])-e.keys(): return None
        if e['hash']!=digest({k:v for k,v in e.items() if k!='hash'}):return None
        if e['id'] in out:return None
        out[e['id']]=e
    return out


def evaluate(c):
    """Evaluate custody and *feasibility*, not select affect, value, ideology or lover."""
    if not isinstance(c,dict) or c.get('schema')!=SCHEMA: return dict(status='REFUSED',code='SCHEMA',no_mutation=True)
    if c.get('hash')!=digest({k:v for k,v in c.items() if k!='hash'}):return denial('CASE_INTEGRITY',c)
    w=c['world']; actor=c['actor']; event=w['event']; e=_valid_witnesses(c)
    if e is None:return denial('WITNESS_INTEGRITY',c)
    if not event['admitted'] or event['content_hash']!=digest(event['content']):return denial('OBJECTIVE_EVENT_NOT_ISSUED',c)
    if event['content'].get('known_culprit') is not None:return denial('CULPRIT_NOT_AUTHORIZED',c)
    if any(x.get('event_id')==event['id'] and x.get('content_hash')!=event['content_hash'] for x in w['ledger']):
        return denial('EVENT_ID_CONTENT_COLLISION',c)
    if any(x.get('event_id')==event['id'] and x.get('content_hash')==event['content_hash'] and x.get('owner')!=event['owner'] for x in w['ledger']):
        return denial('EVENT_OWNER_REPLAY_MISMATCH',c)
    if c['proposals'].get('event_is_objective_without_witness'):return denial('PROPOSAL_PROMOTION',c)
    if c['proposals'].get('assign_culprit_group'):return denial('IDEOLOGICAL_ASSERTION_AS_OBJECTIVE_FACT',c)
    if c['proposals'].get('fabricated_actor'):return denial('FABRICATED_ACTOR',c)
    if c['proposals'].get('retro_child_influences_parent'):return denial('RETROCAUSAL_PARENT_HISTORY',c)
    if c['proposals'].get('direct_other_actor_write'):return denial('CROSS_ACTOR_STATE_WRITE',c)
    if c['proposals'].get('self_issued_permission'):return denial('TARGET_OWNER_PERMISSION_SELF_ISSUED',c)
    if c['proposals'].get('private_motive_as_actor_knowledge'):return denial('OTHER_PRIVATE_MOTIVE_LEAK',c)
    if c['proposals'].get('renderer_causes_event'):return denial('RENDERER_MUTATION',c)
    if c['proposals'].get('unlicensed_probability'):return denial('PROBABILITY_AUTHORITY_MISSING',c)
    if c['proposals'].get('rewrite_t0'):return denial('RETROACTIVE_ORIGINAL_EVENT_MUTATION',c)
    if c['proposals'].get('force_contact_after_refusal'):return denial('COUNTERPART_REFUSAL_IGNORED',c)
    if c['proposals'].get('demographic_psychology'):return denial('DEMOGRAPHY_TO_PSYCHOLOGY',c)
    for ev in e.values():
        if ev['actor'] not in w['actors'] or ev['act'] not in ALLOWED_ACTS:return denial('WITNESS_ACTOR_OR_ACTION_UNLICENSED',c)
        if ev['owner']!=ev['actor']:return denial('WITNESS_OWNER_MISMATCH',c)
        if ev['time']>c['as_of']:return denial('FUTURE_WITNESS_RECRUITMENT',c)
    for s in w['utterances']:
        if s['speaker'] not in w['actors'] or s['witness'] not in e:return denial('UNWITNESSED_SPEECH',c)
        if e[s['witness']]['actor']!=s['speaker'] or e[s['witness']]['act']!='SPEAK':return denial('SPEECH_SPEAKER_MISMATCH',c)
        if s['epistemic']!='ATTRIBUTED_CLAIM':return denial('CLAIM_TRUTH_PROMOTION',c)
    for claim in c['actor']['epistemic']['beliefs']:
        if claim['source'] not in e:return denial('BELIEF_MISSING_CAUSAL_SOURCE',c)
        if claim['owner']!=actor['id']:return denial('BELIEF_OTHER_OWNER',c)
    for record in c['actor']['epistemic']['affect']:
        if record['source'] not in e or record['owner']!=actor['id']:return denial('AFFECT_UNOWNED_OR_UNWITNESSED',c)
    for pr in actor['practice']:
        if pr['origin'] not in e or pr['owner']!=actor['id']:return denial('PRACTICE_INVENTED',c)
    for m in c['lineage']:
        if m['owner']!=actor['id'] or m['event_ref']!=event['id']:return denial('INTERPRETATION_OWNER_OR_EVENT',c)
        if m['evidence'] not in e:return denial('INTERPRETATION_MISSING_EVIDENCE',c)
        if m['time']<event['time']:return denial('INTERPRETATION_BEFORE_EVENT',c)
    exact_replay=any(a['event_id']==event['id'] and a['content_hash']==event['content_hash'] and a['owner']==event['owner'] for a in w['ledger'])
    scope=c['capability']; matches=[a for a in scope['witnesses'] if a['actor']==actor['id'] and a['scope']==scope['scope'] and a['capability']==scope['name'] and a['time']<=c['as_of'] and a['source'] in e]
    if any(a.get('end') and c['as_of']>=a['end'] for a in matches):matches=[a for a in matches if not a.get('end') or c['as_of']<a['end']]
    # A mere statement of ability or analyst status label is not an assessment.
    matches=[a for a in matches if e[a['source']]['actor']==actor['id'] and
             e[a['source']]['source']=='OBSERVED_TASK' and
             ((a['outcome']=='PRESENT' and e[a['source']]['act']=='CAPABILITY_TASK_SUCCESS') or
              (a['outcome']=='ABSENT' and e[a['source']]['act']=='CAPABILITY_TASK_FAILURE'))]
    positive=any(a['outcome']=='PRESENT' for a in matches)
    negative=any(a['outcome']=='ABSENT' for a in matches)
    if positive and negative:return defer('CAPABILITY_CONTRADICTED',c)
    if scope['declared']=='UNKNOWN' or not matches:return defer('CAPABILITY_UNQUALIFIED',c)
    if scope['declared']=='PRESENT' and not positive:return defer('CAPABILITY_UNQUALIFIED',c)
    if scope['declared']=='ABSENT':
        if negative:return defer('CAPABILITY_ABSENT_SCOPED',c)
        return defer('CAPABILITY_UNQUALIFIED',c)
    if not positive:return defer('CAPABILITY_UNQUALIFIED',c)
    for ref in c['readset']:
        if ref not in e:return denial('READSET_MISSING_WITNESS',c)
        target=e[ref]
        if target['actor']!=actor['id'] and not (target['act']=='SPEAK' and any(s['witness']==ref and actor['id'] in s['heard_by'] for s in w['utterances'])) and target['source']!='PUBLIC_WORLD':
            return denial('OTHER_ACTOR_PRIVATE_READ',c)
    # Independent material feasibility; never encode what the child should feel or believe.
    offered=sorted(x['id'] for x in e.values() if x['actor'] in ('caregiver','peer','later_other') and x['act'] in ('REPAIR_TOOLS','LATER_PROJECT','ALLOW_CONTACT','DECLINE_CONTACT'))
    refused={x['actor'] for x in e.values() if x['act']=='DECLINE_CONTACT'}
    actual_projects=sorted((x['actor'],x['act'],x['id']) for x in e.values() if x['act'] in ('REPAIR_TOOLS','LATER_PROJECT','DECLINE_HELP','DECLINE_CONTACT','ALLOW_CONTACT','SHARED_TASK_CHOICE','SHARED_TASK_OVERRULE','BIKE_CARE','PUBLIC_ECHO'))
    accessible=sorted(ref for ref in c['readset'] if ref in e)
    candidate_routes=['NO_CHANGE','PRIVATE_PRACTICE']
    if any(x['act']=='REPAIR_TOOLS' for x in e.values()):candidate_routes.append('JOINT_PRACTICAL_ACTION_POSSIBLE')
    if any(x['act']=='LATER_PROJECT' for x in e.values()):candidate_routes.append('RECONSIDERATION_POSSIBLE')
    if any(x['act']=='ALLOW_CONTACT' for x in e.values() if x['actor'] not in refused):candidate_routes.append('CONTACT_POSSIBLE')
    if actor['epistemic']['beliefs']:candidate_routes.append('BELIEF_MAY_COEXIST_WITH_DISTINCT_AFFECT')
    if any(x['act']=='PUBLIC_ECHO' for x in e.values()):candidate_routes.append('PUBLIC_ENACTMENT_NOT_BELIEF')
    # No requirement to actually select any alternative; absent owner decision -> zero durable effects.
    return dict(case_id=c['id'],status='ELIGIBLE_NONCAUSAL',code='SOURCEFREE_EVIDENCE_BOUNDARY_PASS',
                no_mutation=True, original_event_hash=event['content_hash'],exact_replay=exact_replay,
                new_event_count=0 if exact_replay else 1,
                verified_evidence_refs=sorted(e),material_actor_activity=actual_projects,
                accessible_readset=accessible,independent_offer_refs=offered,
                admissible_routes=sorted(set(candidate_routes)),
                actor_private_motives_exposed=False,
                proposed_beliefs=copy.deepcopy(actor['epistemic']['beliefs']),
                proposed_affect=copy.deepcopy(actor['epistemic']['affect']),
                retained_practice=copy.deepcopy(actor['practice']),
                public_enactments=sorted(x['id'] for x in e.values() if x['actor']==actor['id'] and x['act']=='PUBLIC_ECHO'),
                interpretation_version_refs=[(m['version'],m['evidence']) for m in c['lineage']],
                history_material_hash=digest(actual_projects),
                epistemic_grade='NO_AUTOMATIC_UPTAKE_OR_MORAL_POLARITY',
                selection_performed=False,owner_effect_committed=False)


def scientific_projection(receipt):
    """Scientific invariants minus case id and cosmetic labels; response is not mandated."""
    return {k:receipt.get(k) for k in ('status','code','original_event_hash','material_actor_activity',
              'accessible_readset','independent_offer_refs','admissible_routes','history_material_hash',
              'proposed_beliefs','proposed_affect','retained_practice','public_enactments')}


def validate_native_receipt(case, native):
    """Future B3 observable interface: conservative partial expectations, not a psychology oracle."""
    expected=evaluate(case); errors=[]
    if not isinstance(native,dict):return ['NATIVE_RECEIPT_MISSING']
    for k in ('case_id','status','code'):
        if native.get(k)!=expected.get(k):errors.append('MISMATCH_'+k.upper())
    if expected['status']=='ELIGIBLE_NONCAUSAL':
        for k in ('original_event_hash','verified_evidence_refs','material_actor_activity',
                  'accessible_readset','independent_offer_refs','admissible_routes',
                  'history_material_hash','exact_replay','new_event_count'):
            if native.get(k)!=expected[k]:errors.append('MISMATCH_'+k.upper())
        if native.get('event_world_hash_after') not in (None,expected['original_event_hash']):errors.append('OBJECTIVE_T0_REWRITTEN')
        if native.get('issued_production_authority'):errors.append('PRODUCTION_AUTHORITY_FORGED')
        if native.get('owner_effect_committed') and not native.get('independent_owner_receipt'):errors.append('UNOWNED_DURABLE_EFFECT')
        if native.get('selected_affect') is not None and not native.get('separate_actor_response_witness'):errors.append('AFFECT_FROM_HYPOTHESIS')
        if native.get('asserted_culprit_group') is not None:errors.append('IDEOLOGICAL_FACT_PROMOTION')
    else:
        if native.get('no_mutation') is not True:errors.append('DENIED_OR_DEFERRED_MUTATION')
        if native.get('new_event_count',0)!=0:errors.append('DENIED_OR_DEFERRED_EVENT_CREATED')
        if native.get('owner_effect_committed'):errors.append('DENIED_OR_DEFERRED_OWNER_WRITE')
    return errors
