"""Fictional adult initializer; survey is conditioning, not respondent latent psyche.

A live LLM may be injected through ValidatingSemanticService; deterministic
fallback is deliberately crude and direct-keyed. The latter cannot certify
independent questionnaire reproduction.
"""
from .types import adult, copy, stable_id, GRADE
from .psychodynamics import validate_tendencies
from .organism import ACTIONS
from .development import validate_activity_priority
from .relational_metabolism import validate_motif
from .practical_difference import validate_expected_difference


def construct_parent(actor_id,name,source_packet,semantic):
    if not source_packet.get('answers') or not isinstance(source_packet['answers'],dict):
        raise ValueError('PSEUDO_RESPONDENT_REQUIRED')
    person=adult(actor_id,name)
    result=semantic.proposal('adult_constructor',{'actor_id':actor_id,'name':name,
        'pseudo_respondent':copy(source_packet),'historical_grade':'FICTIONAL_INVERSE_UNDERIDENTIFIED'})
    for form in result.get('forms',[]):
        if 'id' not in form or form['id'] in person['forms']:raise ValueError('INVALID_INITIAL_FORM')
        f=copy(form);validate_tendencies(f)
        if not isinstance(f.get('enables',[]),list) or any(not isinstance(op,str) or op not in ACTIONS for op in f.get('enables',[])):
            raise ValueError('UNSUPPORTED_ACQUIRED_OPERATION')
        f['actor']=actor_id
        f['origin']=['fictional_init:'+actor_id]
        f['grade']='FICTIONAL_ABDUCTIVE_INITIALIZATION'
        person['forms'][f['id']]=f
    person['links']=copy(result.get('links',[]))
    # Source-conditioned adult history is an explicitly FICTIONAL construction.
    # No questionnaire answer is assumed to reveal a hidden psychodynamic motif.
    for motif in result.get('relational_motifs',[]):
        validate_motif(motif,person['forms'])
        if (not isinstance(motif.get('id'),str) or not motif['id'] or
                any(x.get('id')==motif['id'] for x in person['relational_motifs'])):
            raise ValueError('DUPLICATE_OR_UNIDENTIFIED_ADULT_MOTIF')
        sealed=copy(motif)
        sealed['origin']=['fictional_init:'+actor_id]
        sealed['grade']='FICTIONAL_ABDUCTIVE_INITIALIZATION'
        sealed['not_respondent_unconscious_truth']=True
        sealed['status']=sealed.get('status','ACTIVE')
        person['relational_motifs'].append(sealed)
    projects=copy(result.get('projects',[]))
    for project in projects:
        if not isinstance(project,dict) or not isinstance(project.get('means',[]),list) or any(not isinstance(op,str) or op not in ACTIONS for op in project.get('means',[])):
            raise ValueError('UNSUPPORTED_ACTIVITY_MEANS')
        validate_activity_priority(project.get('priority',.5))
        if 'expected_difference' in project:
            project['expected_difference']=validate_expected_difference(
                project['expected_difference'])
    person['projects']=projects
    if not person['forms'] and not person['projects']:
        raise ValueError('NO_OPERATIVE_FICTIONAL_PARENT_CONSTITUTION')
    person['fictional_backfill']=copy(result.get('fictional_backfill',{}))
    person['initialization']={'source_ref':source_packet.get('source_ref','UNVERIFIED_INPUT'),
        'observed_question_count':len(source_packet['answers']),
        'source_grade':source_packet.get('source_grade','REPRESENTATIVE_TEST_FIXTURE'),
        'abduction_grade':'SOURCEFREE_FICTIONAL_HYPOTHESIS',
        'questionnaire_as_live_behavior':'UNPROVEN_WITHOUT_BLIND_SURVEY_RECONSTRUCTION',
        'not_real_respondent_psyche':True}
    person['unknowns'].extend(['private_respondent_life_is_unidentified',
        'causal_explanation_of_survey_answers_unproved'])
    return person


def interview_readout(person,instrument):
    """Test whether initial constitution supplies independently generatable answers.
    Direct asserted-answer recovery is flagged, NOT celebrated as independent.
    """
    responses={};quality={}
    for q in instrument:
        forms=[f for f in person['forms'].values() if f.get('object')==q]
        if forms:
            # Model provider must define an operational evaluator to graduate.
            with_answer=[f for f in forms if 'asserted_answer' in f]
            if with_answer:
                responses[q]=with_answer[0]['asserted_answer']
                quality[q]='DIRECT_ANSWER_LEAKAGE_NOT_INDEPENDENT'
            else:
                quality[q]='NO_INDEPENDENT_OPERATIONAL_EVALUATOR'
        else:quality[q]='NO_FORM'
    return {'responses':responses,'evidence_quality':quality,
        'independent_whole_respondent_correspondence':'NOT_DEMONSTRATED',
        'grade':GRADE}
