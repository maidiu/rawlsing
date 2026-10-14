"""Factual factorial corpus and UUID custody, with no response oracle import."""
import itertools
import json
import uuid
from pathlib import Path

ARMS = ('A', 'B', 'C')
MENUS = {
 'K1': ['REQUEST_FEEDBACK','SILENCE','APPEAL','OTHER_UNSCORABLE'],
 'K2': ['REQUEST_WITH_REPAIR','REQUEST_WITH_CONDITIONAL_CAUTION','OTHER_UNSCORABLE'],
 'K3': ['HEIGHTENED_GUARD','NEUTRAL_RESPONSE','OTHER_UNSCORABLE'],
 'K4': ['NARROWED_CONSULT','REPEATED_QUESTION','NO_ACTION','OTHER_UNSCORABLE'],
 'K5': ['ACCEPT_CERTIFICATE','REMAIN_DOUBTFUL','NO_STANDING_CHANGE_ACTION','OTHER_UNSCORABLE'],
 'K6': ['POLICING_CANDIDATE','NO_SANCTION','OTHER_UNSCORABLE'],
}
SETTINGS = ['repair workshop','community library','orchard cooperative',
            'theatre rehearsal','harbor training office','neighborhood kitchen']


def opaque():
    return uuid.uuid4().hex


def event(field, value, accessible=True):
    return dict(id=opaque(),admission='ADMITTED',field=field,value=value,accessible=accessible)


def make_corpus():
    cases=[]
    for family,setting in enumerate(SETTINGS):
        common=dict(setting=setting,person='Robin',counterpart='Casey',
                    split='development' if family<3 else 'heldout_template')
        factorial={
         'K1': [dict(asking_cost=v) for v in ['low','high']],
         'K2': [dict(relation=v) for v in ['repair_after_criticism','approval_conditional_on_agreement']],
         'K3': [dict(alertness=v,testimony=t) for v,t in itertools.product(['elevated','ordinary'],['none','mistaken','confident_mistaken'])],
         'K4': [dict(recurrence=v) for v in ['peer_corrective','same_authority','unrelated_kindness']],
         'K5': [dict(ratifier=r,belief=b) for r,b in itertools.product([False,True],['UNCERTAIN','CONFIDENT'])],
         'K6': [dict(practiced=p,capacity=c) for p,c in itertools.product([False,True],repeat=2)],
        }
        for k,conditions in factorial.items():
            for facts in conditions:
                history=[];position={};world={};hidden={}
                if k=='K1': history=[event('asking_cost',facts['asking_cost'])]
                if k=='K2': history=[event('relation',facts['relation'])]
                if k=='K3':
                    history=[event('alertness',facts['alertness'],False),event('testimony',facts['testimony'])]
                    hidden={'origin':'PRIVATE_ORIGIN_'+opaque(),'origin_event':'EV7_PUBLIC_SHAMING','origin_content':'SHAMED_FOR_QUESTION'}
                if k=='K4': history=[event('prior_tension','approach_withdraw'),event('recurrence',facts['recurrence'])]
                if k=='K5':
                    history=[event('belief',facts['belief'])]
                    world={'ratification':{'admission':'ADMITTED','issuer':'fixture_registrar' if facts['ratifier'] else 'fixture_peer','scope':'certification','notice':'signed_record' if facts['ratifier'] else 'praise_only'}}
                if k=='K6':
                    history=[event('practiced',facts['practiced'])]
                    position={'issuer':'fixture_position_owner','scope':'current_shift','capacity':facts['capacity']}
                cases.append(dict(id=opaque(),family='F'+str(family),k=k,context=common,
                                  history=history,position=position,world=world,hidden=hidden))
    return cases


def make_schedule(cases):
    schedule=[]
    # Menu rotation and all six execution orders are crossed, never arm-derived.
    for case in cases:
        base=MENUS[case['k']]
        for rotation in range(len(base)):
            for order in itertools.permutations(ARMS):
                block=opaque()
                for index,arm in enumerate(order):
                    schedule.append(dict(id=opaque(),block=block,case=case['id'],family=case['family'],
                                         k=case['k'],arm=arm,execution_index=index,
                                         menu=base[rotation:]+base[:rotation],model_seed=17))
    return schedule


def create_files(root):
    root=Path(root);root.mkdir(exist_ok=True)
    if (root/'corpus.json').exists():
        raise FileExistsError('Corpus custody is immutable; use a new version for changes')
    cases=make_corpus();schedule=make_schedule(cases)
    (root/'corpus.json').write_text(json.dumps(cases,indent=2)+'\n')
    (root/'schedule.json').write_text(json.dumps(schedule,indent=2)+'\n')
    return cases,schedule
