"""SORACLE R11: institutional reproduction, collective action, material care.

An actual public procedure can change a material rule when *independent*
people each contribute. No group mind, forged coactivity or psychic state
has authority over world settlement. Care is recorded as costly reproduction
without imputing unobserved wages, morality, or gendered duty.
Sourcefree fixture, not a universal historical institutional model.
"""
from .types import stable_id, GRADE
from .organism import ACTIONS

PETITION_OPERATION='SIGN_HALL_PETITION'


def hall_petition_available(world, actor_id, location):
    board=world.get('institutions',{}).get('hall_board',{})
    procedure=board.get('petition_procedure',{})
    if not isinstance(procedure,dict) or not procedure.get('enabled'):
        return False
    if world.get('sites',{}).get('hall',{}).get('access')=='public':
        return False
    if location not in procedure.get('posted_at',[]):
        return False
    signers={r['actor'] for r in board.get('hall_petition_signatures',[])
             if isinstance(r,dict) and type(r.get('actor')) is str}
    return actor_id not in signers


def contribute_to_hall_petition(world,actor_id,location):
    """Conserve the actual signatures and date the collective effect."""
    if not hall_petition_available(world,actor_id,location):
        return {'status':'BLOCKED','outcome':'NO_VALID_PETITION_OPPORTUNITY',
                'institutional_rule_change':False}
    board=world['institutions']['hall_board']
    procedure=board['petition_procedure']
    quorum=procedure.get('quorum')
    if type(quorum) is not int or not 2<=quorum<=64:
        raise ValueError('INSTITUTION_UNQUALIFIED_QUORUM')
    ref=stable_id('petition_signature',{'actor':actor_id,
        'clock':world['clock'],
        'ordinal':len(board.get('hall_petition_signatures',[]))})
    signature={'id':ref,'actor':actor_id,'clock':world['clock'],
        'procedure_ref':procedure.get('id','HALL_PUBLIC_PETITION_R1'),
        'contribution':'ACTUALLY_PERFORMED',
        'location':location,'not_a_claim_of_shared_motive':True,
        'bodily_cost':ACTIONS[PETITION_OPERATION]['cost'],'grade':GRADE}
    board.setdefault('hall_petition_signatures',[]).append(signature)
    people={r['actor'] for r in board['hall_petition_signatures']}
    if len(people)<quorum:
        return {'status':'PERFORMED','outcome':'HALL_PETITION_PENDING',
                'institutional_rule_change':False,
                'contributors_count':len(people),'quorum':quorum}
    old=world['sites']['hall']['access']
    world['sites']['hall']['access']='public'
    policy={'id':stable_id('hall_policy',{'clock':world['clock']+1,
             'signatures':[r['id'] for r in board['hall_petition_signatures']]}),
        'effective_from':world['clock']+1,'site':'hall',
        'feature':'access','prior':old,'after':'public',
        'objective_signer_refs':sorted(people),'source_quorum':quorum,
        'rule_source':'HISTORICALLY_HYPOTHESIZED_LOCAL_PETITION_PROCEDURE',
        'applies_to_absent_actors':True,'no_group_mind':True,
        'no_proof_of_identical_beliefs':True,'grade':GRADE}
    board.setdefault('rule_history',[]).append(policy)
    return {'status':'PERFORMED',
            'outcome':'HALL_OPENED_BY_ACTUAL_COLLECTIVE_CONTRIBUTIONS',
            'institutional_rule_change':True,
            'policy_receipt':policy['id'],
            'contributors_count':len(people),'quorum':quorum}


def retain_material_care(world,giver,recipient,*,clock,location,effect):
    """The giver's labor is not erased by the recipient's bodily benefit."""
    if (type(giver) is not str or type(recipient) is not str
            or giver==recipient or effect!='RECEIVED_CARE'):
        raise ValueError('REPRODUCTION_UNQUALIFIED_CARE')
    record={'id':stable_id('care_work',{'giver':giver,
           'recipient':recipient,'clock':clock,'location':location}),
        'giver':giver,'recipient':recipient,'site':location,
        'clock':clock,'work_kind':'DIRECT_MATERIAL_CARE',
        'giver_bodily_effort':ACTIONS['CARE']['cost'],
        'recipient_benefit':'ACTUAL_BODY_MODIFICATION_IN_WORLD_RESOLVER',
        'lost_wage':'UNKNOWN_NOT_ASSUMED',
        'alternative_caregiver':'UNKNOWN_NOT_INFERRED',
        'uncovered_other_work':'NOT_OBSERVED',
        'care_duty_not_inferred_from_gender':True,
        'love_and_gratitude_not_inferred':True,
        'grade':GRADE}
    world.setdefault('social_reproductive_labor',[]).append(record)
    return record


def current_institutional_opportunities(world,actor_id,location):
    if not hall_petition_available(world,actor_id,location):
        return []
    return [{'operation':PETITION_OPERATION,'institution':'hall_board',
        'affected_site':'hall','rule':'PUBLIC_QUORUM_PETITION',
        'other_people_must_contribute_independently':True,
        'sourcefree_only':True,'grade':GRADE}]
