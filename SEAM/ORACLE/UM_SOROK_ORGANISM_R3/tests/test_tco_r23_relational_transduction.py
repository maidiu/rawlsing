"""SEAM/30 THREE_AGENT_MULCH R23: acquired relations can be causally operative.

Not approval of objective harm, unconscious mind-reading, a real church model,
or a scientifically unique human response. All forms and witnesses are
explicitly sourcefree fictional fixtures; owner-qualified historical admission
and independent world settlement remain independent.
"""
from dataclasses import asdict
import unittest

from um_sorok_organism.types import (
    AccessibleEncounter, Constitution, Attempt, adult, blank_world, copy,
)
from um_sorok_organism.constitution import compose, materialize, actor_access
from um_sorok_organism.world import add_cue, resolve
from um_sorok_organism.development import admit, InvalidDevelopment
from um_sorok_organism.semantics import (
    CallbackLLMProvider, ValidatingSemanticService,
)
from um_sorok_organism.relational_metabolism import (
    validate_motif, InvalidRelationalMotif,
)


def form(fid, operation, *, tendency=None):
    return {
        'id':fid,'actor':'mother','kind':'RELATIONAL_INVESTMENT',
        'origin':['sourcefree_fictional_prior:mother'],
        'grade':'SOURCEFREE_RESEARCH_PROVISIONAL',
        'cues':['corrective_ritual'],'enables':[operation],
        'scope':{},'lifecycle':'ACTIVE','strength':.7,
        'body_min':.1,'access':'tacit',
        'tendencies':[tendency] if tendency else [],
    }


def motif():
    return {
        'id':'historically_learned_care_authority',
        'source_forms':['care','authority'],
        'cue_terms':['corrective_ritual'],
        'locations':['home'],
        'witnessed_source_actor_ref':'pastor',
        'origin':['sourcefree_fictional_prior:care_and_authority'],
        'status':'ACTIVE',
        'effects':[{
            'kind':'RELATION_MEDIATION',
            'source':'care','target':'authority',
            'relation':'SUBORDINATES',
            'mediated_action':'IMPOSE','polarity':'APPROACH',
        }],
    }


def read_model(*, inhibited=None, withhold=False, motif_override=None):
    forms={
        'care':form('care','CARE'),
        'authority':form('authority','IMPOSE',tendency={
            'action':'IMPOSE','polarity':'WITHHOLD',
            'cue_terms':['corrective_ritual'],
        } if withhold else None),
    }
    links=[]
    if inhibited:
        forms['guard']=form('guard','WAIT')
        links=[{
            'source':'guard','target':inhibited,'relation':'INHIBITS',
            'contexts':['home'],'origin':['sourcefree_prohibition'],
        }]
    c=Constitution(
        actor='mother',clock=7,
        body=adult('mother','Mother')['body'],
        forms=forms,links=links,projects=[],
        activity_links=[],composition_methods=[],
        memories=[],traces=[],other_models={},self_model={},
        relations=[],unknowns=[],
        relational_motifs=[copy(motif_override if motif_override is not None
                                 else motif())],
    )
    return c


def encounter(*, speaker='pastor', kind='speech', place='home',
              tags=('corrective_ritual',)):
    return AccessibleEncounter(
        'mother',7,place,[{
            'id':'objective:rebuke:7',
            'clock':7,'kind':kind,'tags':list(tags),
            'source_actor':speaker,'location':place,
            'modality':'auditory',
        }],[],['objective:rebuke:7'])


def mediated(s):
    return [c for c in s.currents
            if c['kind']=='RELATIONALLY_MEDIATED_ACTION_CURRENT'
            and c.get('mediation_mode')==
            'HISTORICALLY_ACQUIRED_RELATION_TRANSDUCTION']


def lived():
    return {'actor':'mother','ref':'lived:mother:new_contrast',
            'participated':True,
            'perceived_cues':[{'id':'objective:neighbor_contrast',
                                'source_actor':'neighbor'}],
            'status':'OBSERVED','own_action':None}


class ThreeAgentMulchR23(unittest.TestCase):
    def test_admitted_relation_itself_operates_not_merely_narrates(self):
        s=compose(read_model(),encounter())
        self.assertEqual(len(mediated(s)),1)
        self.assertEqual(mediated(s)[0]['action'],'IMPOSE')
        self.assertEqual(mediated(s)[0]['polarity'],'APPROACH')
        self.assertEqual(mediated(s)[0]['relation_transduced'],'SUBORDINATES')
        self.assertTrue(mediated(s)[0]['not_objective_justification_of_conduct'])
        a=next(o for o in s.candidate_actions if o['action']=='IMPOSE')
        self.assertEqual(
            a['psychodynamic_status'],
            'ACQUIRED_APPROACH_WITHOUT_RECORDED_COUNTERCURRENT')
        self.assertIn('motif:historically_learned_care_authority',
                      a['support_currents'])
        self.assertTrue(any(
            c['kind']=='ACQUIRED_PERSONAL_SENSE_MEDIATION'
            and c['operative_mediation'] for c in s.currents))
        self.assertIn('historically_learned_care_authority',s.readset)

    def test_same_words_by_different_other_do_not_identify_authority(self):
        s=compose(read_model(),encounter(speaker='neighbor'))
        self.assertEqual(mediated(s),[])
        self.assertNotIn('historically_learned_care_authority',s.readset)
        self.assertIn('IMPOSE',{o['action'] for o in s.candidate_actions})
        self.assertFalse(any(
            o.get('support_currents') for o in s.candidate_actions
            if o['action']=='IMPOSE'))

    def test_ambient_co_presence_is_not_a_witnessed_authority_event(self):
        s=compose(read_model(),encounter(kind='coactor_present'))
        self.assertEqual(mediated(s),[])
        self.assertFalse(any(
            c['kind']=='ACQUIRED_RELATIONAL_CONFIGURATION'
            for c in s.currents))

    def test_material_setting_and_ritual_genre_are_conditional(self):
        for e in (
            encounter(place='market'),
            encounter(tags=('unfamiliar_utterance',)),
        ):
            with self.subTest(place=e.location,tags=e.cues[0]['tags']):
                self.assertEqual(mediated(compose(read_model(),e)),[])

    def test_inhibited_care_remains_indirectly_causal_not_restored(self):
        s=compose(read_model(inhibited='care'),encounter())
        self.assertIn('care',s.inhibited)
        self.assertNotIn('care',{f['id'] for f in s.recruited})
        self.assertNotIn('CARE',{o['action'] for o in s.candidate_actions})
        self.assertEqual(len(mediated(s)),1)
        self.assertTrue(mediated(s)[0]['has_inhibited_source'])
        self.assertTrue(any(
            c['kind']=='ACQUIRED_PERSONAL_SENSE_MEDIATION'
            and c['has_inhibited_source'] for c in s.currents))

    def test_inhibited_target_is_not_resurrected_to_act(self):
        s=compose(read_model(inhibited='authority'),encounter())
        self.assertIn('authority',s.inhibited)
        self.assertEqual(mediated(s),[])
        self.assertNotIn('IMPOSE',{o['action'] for o in s.candidate_actions})
        self.assertTrue(any(
            c['kind']=='ACQUIRED_PERSONAL_SENSE_MEDIATION'
            and not c['operative_mediation'] and
            not c['target_directly_recruited'] for c in s.currents))

    def test_opposed_relational_and_direct_currents_remain_unresolved(self):
        s=compose(read_model(withhold=True),encounter())
        self.assertEqual(len(mediated(s)),1)
        o=next(o for o in s.candidate_actions if o['action']=='IMPOSE')
        self.assertEqual(o['psychodynamic_status'],'UNRESOLVED_CONTRADICTION')
        self.assertIn('authority',o['opposed_currents']['withhold'])
        self.assertIn('motif:historically_learned_care_authority',
                      o['opposed_currents']['approach'])
        self.assertTrue(any(x['action']=='IMPOSE' for x in s.antagonisms))

    def test_operative_target_must_be_previously_acquired_mean_not_magic(self):
        bad=motif()
        bad['effects'][0]['mediated_action']='FEED'
        with self.assertRaisesRegex(
                InvalidRelationalMotif,
                'MOTIF_MEDIATED_ACTION_NOT_ACQUIRED_BY_TARGET'):
            validate_motif(bad,read_model().forms)
        for changes in ({'polarity':'COMPULSORY'},
                        {'mediated_action':None},
                        {'polarity':None}):
            candidate=motif()
            candidate['effects'][0].update(changes)
            with self.subTest(changes=changes):
                with self.assertRaises(InvalidRelationalMotif):
                    validate_motif(candidate,read_model().forms)

    def test_bad_actor_witness_ref_cannot_create_unbounded_authority(self):
        for badref in ('',False,42,[],{}):
            candidate=motif()
            candidate['witnessed_source_actor_ref']=badref
            with self.subTest(ref=badref):
                with self.assertRaisesRegex(
                        InvalidRelationalMotif,
                        'INVALID_MOTIF_WITNESSED_SOURCE_ACTOR'):
                    validate_motif(candidate,read_model().forms)

    def test_relation_requalification_preserves_prior_historical_meaning(self):
        actor=adult('mother','Mother')
        actor['forms']=copy(read_model().forms)
        actor['relational_motifs']=[motif()]
        original=copy(actor)
        admitted=admit(actor,lived(),'objective:new_counterexample',[{
            'kind':'REORGANIZE_RELATIONAL_MOTIF',
            'motif_id':'historically_learned_care_authority',
            'witnessed_source_actor_ref':'neighbor',
        }])
        self.assertEqual(admitted[0]['status'],
                         'ADMITTED_SOURCEFREE_MOTIF_REORGANIZATION')
        changed=actor['relational_motifs'][0]
        self.assertEqual(changed['witnessed_source_actor_ref'],'neighbor')
        self.assertEqual(changed['motif_history'][-1]['previous']
                         ['witnessed_source_actor_ref'],'pastor')
        self.assertEqual(changed['origin'],original['relational_motifs'][0]['origin'])
        self.assertEqual(mediated(compose(
            read_model(motif_override=changed),encounter())),[])
        self.assertEqual(len(mediated(compose(
            read_model(motif_override=changed),
            encounter(speaker='neighbor')))),1)

    def test_invalid_requalification_rolls_back_entire_actor(self):
        actor=adult('mother','Mother')
        actor['forms']=copy(read_model().forms)
        actor['relational_motifs']=[motif()]
        before=copy(actor)
        with self.assertRaisesRegex(
                InvalidDevelopment,'INVALID_MOTIF_WITNESSED_SOURCE_ACTOR'):
            admit(actor,lived(),'objective:bad_reinterpretation',[{
                'kind':'REORGANIZE_RELATIONAL_MOTIF',
                'motif_id':'historically_learned_care_authority',
                'witnessed_source_actor_ref':'',
            }])
        self.assertEqual(actor,before)

    def test_real_world_sensory_gate_and_expiring_event_control_mediation(self):
        world=blank_world()
        world['positions'].update({'mother':'home','pastor':'home'})
        actor=adult('mother','Mother')
        actor['forms']=copy(read_model().forms)
        actor['relational_motifs']=[motif()]
        start=compose(materialize(actor,world),actor_access(actor,world))
        self.assertEqual(mediated(start),[])
        add_cue(world,'speech',['corrective_ritual'],
                location='home',modality='auditory',source_actor='pastor')
        live=compose(materialize(actor,world),actor_access(actor,world))
        self.assertEqual(len(mediated(live)),1)
        # The world can keep the pastor nearby; a *past* speech event does
        # not remain perceptible simply because its speaker is co-present.
        world['clock']+=1
        after=compose(materialize(actor,world),actor_access(actor,world))
        self.assertEqual(mediated(after),[])
        self.assertTrue(any(
            cue.get('kind')=='coactor_present' for cue in
            actor_access(actor,world).cues))
        self.assertEqual(actor['relational_motifs'][0]['origin'],
                         ['sourcefree_fictional_prior:care_and_authority'])

    def test_world_gate_refuses_other_person_private_sign_and_weak_sensor(self):
        world=blank_world()
        world['positions'].update({'mother':'home','pastor':'home'})
        actor=adult('mother','Mother')
        actor['forms']=copy(read_model().forms)
        actor['relational_motifs']=[motif()]
        add_cue(world,'speech',['corrective_ritual'],
                location='home',modality='auditory',
                source_actor='pastor',private_to='different_actor')
        self.assertEqual(mediated(
            compose(materialize(actor,world),actor_access(actor,world))),[])
        # Replace only the external sensory fixture: the same actor's
        # history does not override the body's concrete reception gate.
        world['cues']=[]
        add_cue(world,'speech',['corrective_ritual'],
                location='home',modality='auditory',
                source_actor='pastor',threshold=1.0)
        self.assertEqual(mediated(
            compose(materialize(actor,world),actor_access(actor,world))),[])

    def test_same_event_recruits_different_acquired_relational_histories(self):
        already=compose(read_model(),encounter())
        without=read_model()
        without.relational_motifs=[]
        other=compose(without,encounter())
        self.assertEqual(len(mediated(already)),1)
        self.assertEqual(mediated(other),[])
        self.assertEqual(without.relational_motifs,[])
        self.assertIn('IMPOSE',{x['action'] for x in other.candidate_actions})
        # A sourcefree current says nothing about the speaker's actual
        # moral authority, the target's injury, or the follower's endorsement.
        self.assertTrue(mediated(already)[0]
                        ['not_objective_justification_of_conduct'])

    def test_older_descriptive_mediation_keeps_no_implicit_action_current(self):
        older=motif()
        older['effects'][0].pop('mediated_action')
        older['effects'][0].pop('polarity')
        s=compose(read_model(motif_override=older),encounter())
        self.assertEqual(mediated(s),[])
        self.assertTrue(any(c['kind']=='ACQUIRED_PERSONAL_SENSE_MEDIATION'
                            for c in s.currents))
        self.assertFalse(any(c['kind']=='RELATIONALLY_MEDIATED_ACTION_CURRENT'
                             for c in s.currents))

    def test_new_witnessed_relation_requires_actual_actor_lived_source(self):
        actor=adult('mother','Mother')
        actor['forms']=copy(read_model().forms)
        original=copy(actor)
        proposal={'kind':'ACQUIRE_RELATIONAL_MOTIF','motif':motif()}
        with self.assertRaisesRegex(
                InvalidDevelopment,'MOTIF_WITNESSED_OTHER_NOT_RECEIVED'):
            admit(actor,lived(),'objective:unrelated_neighbor',[proposal])
        self.assertEqual(actor,original)
        perceived=copy(lived())
        perceived['perceived_cues']=[{
            'id':'objective:pastor_source','source_actor':'pastor'}]
        result=admit(actor,perceived,'objective:qualified_pastor',[proposal])
        self.assertEqual(result[0]['status'],
                         'ADMITTED_SOURCEFREE_RELATIONAL_FORMATION')
        self.assertEqual(actor['relational_motifs'][0]['experience_ref'],
                         perceived['ref'])
        self.assertEqual(actor['relational_motifs'][0]['origin'],
                         ['objective:qualified_pastor'])
        self.assertTrue(any(
            x['kind']=='RELATIONALLY_MEDIATED_ACTION_CURRENT'
            for x in compose(
                read_model(motif_override=actor['relational_motifs'][0]),
                encounter()).currents))

    def test_relation_cannot_retarget_to_unexperienced_other(self):
        actor=adult('mother','Mother')
        actor['forms']=copy(read_model().forms)
        actor['relational_motifs']=[motif()]
        before=copy(actor)
        unqualified=copy(lived())
        unqualified['perceived_cues']=[{'id':'objective:irrelevant'}]
        with self.assertRaisesRegex(
                InvalidDevelopment,'MOTIF_WITNESSED_OTHER_NOT_RECEIVED'):
            admit(actor,unqualified,'objective:invented_neighbor',[{
                'kind':'REORGANIZE_RELATIONAL_MOTIF',
                'motif_id':'historically_learned_care_authority',
                'witnessed_source_actor_ref':'neighbor',
            }])
        self.assertEqual(actor,before)

    def test_personal_moralization_never_overrides_independent_world_harm(self):
        world=blank_world()
        world['positions'].update({
            'mother':'home','pastor':'home','target':'home'})
        actor=adult('mother','Mother')
        target=adult('target','Target')
        actor['forms']=copy(read_model().forms)
        actor['relational_motifs']=[motif()]
        actors={'mother':actor,'target':target}
        add_cue(world,'speech',['corrective_ritual'],location='home',
                modality='auditory',source_actor='pastor')
        before=compose(materialize(actor,world),actor_access(actor,world))
        self.assertEqual(len(mediated(before)),1)
        # Research-selected IMPOSE is NOT silently attributed to the actor's
        # own motive just because it is eligible and morally recruited.
        outcome=resolve(world,actors,Attempt(
            actor='mother',action='IMPOSE',target='target'))
        self.assertEqual(outcome.status,'PERFORMED')
        self.assertEqual(outcome.objective_description,
                         'UNILATERAL_IMPOSITION_NOT_CONSENT')
        self.assertEqual(outcome.personal_effects['target']['action'],
                         'IMPOSED_ON')
        # An admired authority or actor-level ideological relation cannot
        # force physical presence or rename an absent target's suffering.
        absent=resolve(world,actors,Attempt(
            actor='mother',action='IMPOSE',target='not_present'))
        self.assertEqual(absent.status,'BLOCKED')
        self.assertEqual(absent.objective_description,'TARGET_NOT_PRESENT')

    def test_llm_semantic_proposal_becomes_operative_only_after_owner_admission(self):
        actor=adult('mother','Mother')
        actor['forms']=copy(read_model().forms)
        lived_pastor=copy(lived())
        lived_pastor['perceived_cues']=[{
            'id':'objective:pastor','source_actor':'pastor'}]
        calls=[]
        def candidate_model(task,packet):
            calls.append((task,copy(packet)))
            return {'task':task,'candidates':[
                {'kind':'ACQUIRE_RELATIONAL_MOTIF','motif':motif()}]}
        semantic=ValidatingSemanticService(
            CallbackLLMProvider(candidate_model))
        response=semantic.proposal('development',{
            'actor':{'id':'mother'},
            'experience':copy(lived_pastor)})
        self.assertEqual(len(calls),1)
        self.assertEqual(len(response['candidates']),1)
        self.assertEqual(actor.get('relational_motifs',[]),[])
        report=admit(actor,lived_pastor,'objective:pastor',response['candidates'])
        self.assertEqual(report[0]['status'],
                         'ADMITTED_SOURCEFREE_RELATIONAL_FORMATION')
        self.assertEqual(len(actor['relational_motifs']),1)
        c=read_model(motif_override=actor['relational_motifs'][0])
        self.assertEqual(len(mediated(compose(c,encounter()))),1)

    def test_semantic_proposal_is_not_an_unguarded_other_person_memory(self):
        actor=adult('mother','Mother')
        actor['forms']=copy(read_model().forms)
        old=copy(actor)
        semantic=ValidatingSemanticService(CallbackLLMProvider(
            lambda task,packet:{
                'task':task,'candidates':[
                    {'kind':'ACQUIRE_RELATIONAL_MOTIF','motif':motif()}]}))
        proposal=semantic.proposal('development',{'experience':lived()})
        self.assertEqual(actor,old)
        with self.assertRaisesRegex(
                InvalidDevelopment,'MOTIF_WITNESSED_OTHER_NOT_RECEIVED'):
            admit(actor,lived(),'objective:unwitnessed',
                  proposal['candidates'])
        self.assertEqual(actor,old)

    def test_read_cannot_write_other_psyche_or_world_permission(self):
        c=read_model()
        a=encounter()
        before_c=copy(asdict(c)); before_a=copy(asdict(a))
        s=compose(c,a)
        self.assertEqual(asdict(c),before_c)
        self.assertEqual(asdict(a),before_a)
        self.assertFalse(any(x['action']=='FEED' for x in s.candidate_actions))
        self.assertFalse(any(
            x.get('objective_consent') is True or x.get('institutional_right') is True
            for x in s.currents if isinstance(x,dict)))



class CrossContextMetabolismR32(unittest.TestCase):
    """Actual R28 history -> R23 motif revaluation -> cold operative future.

    The sourcefree callback is a controlled choice, not human psychology or
    live LLM performance. It may choose no change from identical grounds.
    """
    @staticmethod
    def _run_history(db, decision):
        from um_sorok_organism.runtime import ConstitutiveRuntime
        from um_sorok_organism.semantics import HeuristicSemanticProvider
        parent={'source_ref':'R32_FICTIONAL_PARENT',
                'source_grade':'SOURCEFREE_TEST_FIXTURE_NOT_EMPIRICAL',
                'answers':{'r32':'not_a_survey_observation'},
                'fictional_seed':{'projects':[]}}
        offers=[]
        chosen=[]
        def callback(task,packet):
            if task=='adult_constructor':
                return HeuristicSemanticProvider().propose(task,packet)
            if task=='expression':
                # The expression owner receives no private revision basis.
                if 'historically_possible_lived_cross_context_revaluations' in packet:
                    raise AssertionError('PRIVATE_DEVELOPMENT_PACKET_LEAK')
                return {'task':task,'surface':'The household continues.'}
            if task=='actor_attempt':
                options={x['action'] for x in packet.get('options',[])}
                return {'task':task,'action':'REST' if 'REST' in options else 'WAIT'}
            if task!='development':
                raise AssertionError(task)
            if packet['actor']['id']!='mother':
                return {'task':task,'candidates':[]}
            e=packet['experience']
            if e.get('own_action')=='WAIT' and 'r32_care' not in packet['actor_forms']:
                forms=[]
                for ident,operation in (('r32_care','CARE'),('r32_duty','REST')):
                    forms.append({'kind':'ADD_FORM','form':{
                        'id':ident,'kind':'PRACTICE','cues':['rest'],
                        'enables':[operation],'always_recruitable':True,
                        'scope':{'locations':['workshop']}}})
                forms.append({'kind':'ACQUIRE_RELATIONAL_MOTIF','motif':{
                    'source_forms':['r32_care','r32_duty'],
                    'locations':['workshop'],'effects':[{
                        'kind':'RELATION_MEDIATION','source':'r32_care',
                        'target':'r32_duty','relation':'SUBORDINATES',
                        'mediated_action':'REST','polarity':'WITHHOLD'}]}})
                return {'task':task,'candidates':forms}
            if e.get('location')=='home':
                return {'task':task,'candidates':packet.get(
                    'historically_possible_lived_directional_orientation',[])}
            grounds=packet.get('historically_possible_lived_cross_context_revaluations',[])
            offers.extend(copy(grounds))
            if grounds and not chosen and decision=='revalue':
                g=grounds[0]
                candidate={'kind':g['kind'],'motif_id':g['motif_id'],
                    'lived_cross_context_basis':copy(g['lived_cross_context_basis']),
                    'new_relation':'SUPPORTS','new_polarity':'APPROACH',
                    'interpretive_hypothesis':'Rest may sustain care rather than betray duty.'}
                chosen.append(copy(candidate))
                return {'task':task,'candidates':[candidate]}
            return {'task':task,'candidates':[]}
        service=ValidatingSemanticService(CallbackLLMProvider(callback))
        rt=ConstitutiveRuntime(db,semantic=service)
        try:
            rt.initialize([('mother','Mother',parent),('father','Father',parent)])
            rt.step('mother',requested_action='WAIT')
            rt.step('mother',requested_action='REST')
            rt.step('mother',requested_action='REST')
            history=rt.snapshot('mother')
            orientations=[r for r in history['historical_orientations']
                          if r.get('acquisition')=='REPEATED_LIVED_BODY_COURSE'
                          and r['operation']=='REST']
            if len(orientations)!=1:
                raise AssertionError(('HOME_ORIENTATION_MISSING',orientations))
            old=copy(history['relational_motifs'][0])
            rt.step('mother',requested_action='MOVE',object_ref='workshop')
            pre=rt.situated('mother')
            if any(o['action']=='REST' for o in pre['candidate_actions']):
                raise AssertionError('OLD_MOTIF_FAILED_TO_INHIBIT_REST')
            if offers:
                raise AssertionError('MOVE_IS_NOT_SHARED_REST_COURSE')
            result=rt.step('mother',requested_action='REST')
            if result['status']!='PERFORMED' or not offers:
                raise AssertionError(('NO_CROSS_CONTEXT_OCCASION',result,offers))
            if not rt.verify()['valid']:
                raise AssertionError('BROKEN_HISTORY')
            state=rt.snapshot('mother')
            settled=rt.situated('mother')
            return service,orientations[0],old,state,settled,offers,chosen
        finally:
            rt.close()

    def test_lived_cross_context_revaluation_changes_actual_future_after_cold_reopen(self):
        import tempfile
        from pathlib import Path
        from um_sorok_organism.runtime import ConstitutiveRuntime
        with tempfile.TemporaryDirectory() as d:
            outcomes={}
            for decision in ('revalue','abstain'):
                db=str(Path(d)/(decision+'.sqlite3'))
                service,source,old,state,situated,offers,chosen=self._run_history(
                    db,decision)
                self.assertEqual(len(offers),1)
                basis=offers[0]['lived_cross_context_basis']
                self.assertEqual(basis['historical_orientation_ref'],source['id'])
                self.assertEqual((basis['earlier_location'],basis['later_location']),
                                 ('home','workshop'))
                self.assertEqual(basis['shared_enacted_operation'],'REST')
                self.assertEqual(state['historical_orientations'],[source])
                changed=state['relational_motifs'][0]
                self.assertEqual(changed['id'],old['id'])
                self.assertEqual(changed['origin'],old['origin'])
                self.assertEqual(changed['source_forms'],old['source_forms'])
                self.assertEqual(changed['locations'],old['locations'])
                if decision=='revalue':
                    self.assertEqual(len(chosen),1)
                    self.assertEqual(changed['effects'][0]['relation'],'SUPPORTS')
                    self.assertEqual(changed['effects'][0]['polarity'],'APPROACH')
                    self.assertEqual(changed['motif_history'][0]['previous']['effects'],
                                     old['effects'])
                    currents=[c for c in situated['currents'] if
                              c.get('lived_cross_context_revaluation')]
                    self.assertEqual(len(currents),1)
                    self.assertEqual(currents[0]['polarity'],'APPROACH')
                    self.assertEqual(currents[0]['lived_cross_context_revaluation'][
                        'historical_orientation_ref'],source['id'])
                else:
                    self.assertEqual(changed,old)
                    self.assertEqual(chosen,[])
                # The source's original relational field is absent; its
                # influence is mediated by the changed motif, not copied.
                self.assertFalse(any(c.get('ref')==source['id']
                    for c in situated['currents']))
                cold=ConstitutiveRuntime(db,semantic=service)
                try:
                    self.assertEqual(cold.snapshot('mother')['relational_motifs'][0],changed)
                    actual=cold.step('mother')
                    self.assertTrue(cold.verify()['valid'])
                    outcomes[decision]=actual['attempt']
                finally:
                    cold.close()
            self.assertEqual(outcomes,{'revalue':'REST','abstain':'WAIT'})

    def test_cross_context_source_recomputed_and_arbitrary_effect_rewrite_refused(self):
        import tempfile
        from pathlib import Path
        from um_sorok_organism.runtime import ConstitutiveRuntime
        from um_sorok_organism.relational_metabolism import (
            possible_lived_cross_context_revaluations)
        with tempfile.TemporaryDirectory() as d:
            db=str(Path(d)/'negative.sqlite3')
            _,_,_,_,_,offers,_=self._run_history(db,'abstain')
            rt=ConstitutiveRuntime(db)
            try:
                actor=rt.ledger.actor('mother')[1]
                basis=offers[0]['lived_cross_context_basis']
                # Reconstruct only the already recorded final lived witness
                # for this isolated typed-owner falsifier.
                w=next(x for x in actor['lived_genesis_episodes']
                       if x['id']==basis['later_episode_ref'])
                experience={'actor':'mother','clock':w['clock'],
                    'ref':w['experience_ref'],'location':w['location'],
                    'own_action':'REST','participated':True,
                    'felt_enactment':{'attempted_operation':'REST'},
                    'perceived_cues':[{'id':basis['later_received_sign_ref'],
                                       'kind':'performed_rest',
                                       'source_actor':'mother','tags':['rest']}]}
                event=w['event_ref']
                valid=possible_lived_cross_context_revaluations(actor,experience,event)
                self.assertEqual(len(valid),1)
                original=copy(actor)
                candidate={'kind':'REORGANIZE_RELATIONAL_MOTIF',
                    'motif_id':valid[0]['motif_id'],
                    'lived_cross_context_basis':copy(valid[0]['lived_cross_context_basis']),
                    'new_relation':'SUPPORTS','new_polarity':'APPROACH'}
                for field,value in (('earlier_event_refs',['forged','later']),
                                    ('historical_orientation_ref','foreign'),
                                    ('later_location','home'),
                                    ('effect_index',17)):
                    bad=copy(candidate);bad['lived_cross_context_basis'][field]=value
                    with self.assertRaises(InvalidDevelopment):
                        admit(actor,experience,event,[bad])
                    self.assertEqual(actor,original)
                bad=copy(candidate);bad['locations']=['home','workshop']
                with self.assertRaises(InvalidDevelopment):
                    admit(actor,experience,event,[bad])
                self.assertEqual(actor,original)
                missing=copy(actor);missing['historical_orientations']=[]
                self.assertEqual(possible_lived_cross_context_revaluations(
                    missing,experience,event),[])
                no_sign=copy(experience);no_sign['perceived_cues']=[]
                self.assertEqual(possible_lived_cross_context_revaluations(
                    actor,no_sign,event),[])
                admit(actor,experience,event,[candidate])
                # A consumed occasion cannot revalue the same motif twice.
                with self.assertRaises(InvalidDevelopment):
                    admit(actor,experience,event,[candidate])
            finally:
                rt.close()


if __name__=='__main__':
    unittest.main()
