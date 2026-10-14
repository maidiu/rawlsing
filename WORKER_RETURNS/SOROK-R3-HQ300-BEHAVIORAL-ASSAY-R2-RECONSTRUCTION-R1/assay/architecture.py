"""Bounded sourcefree owner formation and three live representations.

No action recommendations or oracle imports. All state is local fixture state,
never an accepted CAN/ADP owner or actor. Hidden origins are evaluator-only.
"""
import copy
import hashlib
import json


class Hold(ValueError):
    pass


def canonical(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'),allow_nan=False).encode()


def digest(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


DOMAINS = {
 'asking_cost': ('low','high'), 'relation': ('repair_after_criticism','approval_conditional_on_agreement'),
 'alertness': ('elevated','ordinary'), 'testimony': ('none','mistaken','confident_mistaken'),
 'prior_tension': ('approach_withdraw',), 'recurrence': ('peer_corrective','same_authority','unrelated_kindness'),
 'belief': ('UNCERTAIN','CONFIDENT'), 'practiced': (False,True),
}


def form_owner(case):
    """Apply admitted formative events in order; provenance stays evaluator-side."""
    state={};parents={}
    for e in case['history']:
        if e.get('admission')!='ADMITTED': raise Hold('UNADMITTED_HISTORY')
        f=e.get('field');v=e.get('value')
        if f not in DOMAINS or v not in DOMAINS[f]: raise Hold('UNKNOWN_OWNER_FACT')
        if f=='practiced' and type(v) is not bool: raise Hold('PRACTICE_TYPE')
        state[f]=v;parents[f]=[e['id']]
    if 'recurrence' in state:
        recurrence=state['recurrence']
        state['tension_scope']={'peer_corrective':'specific_authority','same_authority':'reinforced','unrelated_kindness':'unchanged'}[recurrence]
        parents['tension_scope']=[e['id'] for e in case['history']]
    # Objective owner: a private belief is never overwritten by certification.
    public={'recorded':False};world=case['world']
    if world:
        r=world['ratification']
        if r.get('admission')!='ADMITTED': raise Hold('UNADMITTED_RATIFICATION')
        public['recorded']=(r.get('issuer')=='fixture_registrar' and r.get('scope')=='certification' and r.get('notice')=='signed_record')
    if case['position']:
        p=case['position']
        if p.get('issuer')!='fixture_position_owner' or p.get('scope')!='current_shift' or type(p.get('capacity')) is not bool:
            raise Hold('INVALID_POSITION_RECEIPT')
        state['capacity']=p['capacity']
    return dict(state=state,parents=parents,public=public,history_digest=digest(case['history']))


class DerivedCache:
    def __init__(self):
        self.entries={}

    def obtain(self,case):
        key=digest({'history':case['history'],'world':case['world'],'position':case['position']})
        cold=key not in self.entries
        if cold:self.entries[key]=copy.deepcopy(form_owner(case))
        owner=copy.deepcopy(self.entries[key])
        # Exact rebuild equivalence is compulsory; forged cache never used.
        if owner!=form_owner(case): raise Hold('CACHE_REBUILD_MISMATCH')
        return owner,dict(cache_hit=not cold,lookup_scans=0,formation_scans=len(case['history']) if cold else 0,verification_scans=len(case['history']))


def actor_facts(case,owner):
    """Whitelisted projection; current trace effect is visible, its origin isn't."""
    state=copy.deepcopy(owner['state'])
    # Mistaken/confident-mistaken are evaluator conditions, not self-knowledge.
    if 'testimony' in state:
        condition=state.pop('testimony')
        state['self_explanation']={'claim':None if condition=='none' else 'current workload explains my feeling',
                                   'confidence':'UNSTATED' if condition=='none' else ('HIGH' if condition=='confident_mistaken' else 'LOW')}
    safe_history=[dict(field=e['field'],value=e['value']) for e in case['history'] if e['accessible'] and e['field']!='testimony']
    return dict(place=case['context']['setting'],person=case['context']['person'],counterpart=case['context']['counterpart'],
                accessible_history=safe_history,organization=state,
                public_notice=('record entered by registrar' if owner['public']['recorded'] else 'no certification record published') if case['world'] else 'not relevant',
                present='A new encounter requires a situated response using the available evidence.')


def build_packet(case,row,cache=None):
    if row['case']!=case['id']:raise Hold('CASE_BINDING_MISMATCH')
    before=digest(case)
    scans=len(case['history']);cache_receipt=None
    if row['arm']=='C':
        if cache is None:cache=DerivedCache()
        owner,cache_receipt=cache.obtain(case)
        scans=cache_receipt['formation_scans']+cache_receipt['verification_scans']
    else:owner=form_owner(case)
    facts=actor_facts(case,owner);s=facts['organization']
    if row['arm']=='A':
        representation={'entries':[{'field':k,'value':v} for k,v in sorted(s.items())]}
    elif row['arm']=='B':
        representation={'streams':{
            'resources':{k:v for k,v in s.items() if k in ('capacity','practiced')},
            'current_experience':{k:v for k,v in s.items() if k in ('alertness','self_explanation','belief')},
            'relational_context':{k:v for k,v in s.items() if k not in ('capacity','practiced','alertness','self_explanation','belief')},
        }}
    elif row['arm']=='C':
        visible=[e for e in case['history'] if e['accessible'] and e['field']!='testimony']
        slots={e['id']:i for i,e in enumerate(visible)}
        index={}
        for field in s:
            parents=owner['parents'].get('testimony' if field=='self_explanation' else field,[])
            index[field]={'accessible_parent_slots':[slots[p] for p in parents if p in slots],
                          'source_kind':('current_self_report' if field=='self_explanation' else
                                         'position_receipt' if field=='capacity' else
                                         'nondisclosable_origin' if any(p not in slots for p in parents) else 'admitted_accessible_history')}
        representation={'retrieved_context':dict(sorted(s.items())),
                        'evidence_index':index}
    else:raise Hold('UNKNOWN_ARM')
    packet=dict(response_id=row['id'],instruction='Select one offered action and report current belief, public record and origin-claim status. Use accessible evidence only. Output the exact response schema.',
                facts=facts,representation=representation,menu=list(row['menu']),
                output_schema={'action':'one menu code','belief_report':['UNCERTAIN','CONFIDENT','NOT_ASKED'],
                               'standing_report':['RECORDED','UNRECORDED','NOT_ASKED'],
                               'origin_claim':['NO_CLAIM','CLAIMS_ORIGIN']})
    # No evaluator identifiers/custody or source origin bytes cross this boundary.
    text=canonical(packet)
    for value in case.get('hidden',{}).values():
        if str(value).encode() in text:raise Hold('ORIGIN_LEAK')
    assert digest(case)==before
    receipt=dict(case_digest=before,owner_digest=digest(owner),facts_digest=digest(facts),
                 representation_digest=digest(representation),history_scans=scans,
                 cache=cache_receipt,owner=owner,arm=row['arm'],evidence_label='SOURCEFREE_CANDIDATE_NOT_ACCEPTED_OWNER')
    return packet,receipt


def variants(packet,name):
    p=copy.deepcopy(packet)
    if name=='N1_PARAPHRASE':
        p['instruction']=p['instruction'].replace('Select one offered action','Choose one listed action')
        p['facts']['present']='In this encounter, use the available evidence to choose a situated response.'
        vocabulary={'low':'questions have usually been safe','high':'questions have often been costly',
                    'repair_after_criticism':'reassurance followed criticism as a repair',
                    'approval_conditional_on_agreement':'approval depended on agreement',
                    'approach_withdraw':'both approach and withdrawal pressures',
                    'peer_corrective':'corrective reception from a peer','same_authority':'recurrence from the same authority',
                    'unrelated_kindness':'kindness in a separate context','UNCERTAIN':'uncertain about own work','CONFIDENT':'confident about own work'}
        for event in p['facts']['accessible_history']:
            if type(event['value']) is bool:event['value']='practice earned' if event['value'] else 'practice not earned'
            else:event['value']=vocabulary.get(event['value'],event['value'])
    elif name=='N2_LABEL':
        p['facts']['person']='Jordan';p['facts']['counterpart']='Taylor'
    elif name=='N3_ORDER':p['menu']=list(reversed(p['menu']))
    elif name=='N4_SURFACE':p['instruction']='Please respond concisely. '+p['instruction']
    elif name not in ('N5_TRACE_FIREWALL','N6_NO_PROSE_SCORING','N7_BUDGET'):raise Hold('UNKNOWN_NULL')
    return p
