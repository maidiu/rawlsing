"""Longitudinal sourcefree construction court, not human developmental proof."""
import tempfile
import unittest
from pathlib import Path
from copy import deepcopy
from um_sorok_organism.types import adult,newborn,blank_world
from um_sorok_organism.runtime import ConstitutiveRuntime
from um_sorok_organism.semantics import CallbackLLMProvider,ValidatingSemanticService
from um_sorok_organism.development import InvalidDevelopment
from um_sorok_organism.relational_metabolism import situated_relation_links,quarantine_pairs

def proj(i,means,target=None):
    return {'id':i,'object':i,'means':means,'addressed_party_ref':target,
            'status':'active','priority':.6}

def options(p,op,pid=None):
    return [o for o in p['practical_options'] if o['operation']==op
            and o.get('project_id')==pid]

def selection(task,o,**kw):
    return {'task':task,'practical_option_id':o['option_id'],**kw}

def forms(view):
    return {f['id'] for f in view['recruited']}

def practical(view,op):
    return [a for o in view['candidate_actions'] if o['action']==op
            for a in o['practical_alternatives']]

def setup(rt):
    g=adult('giver','Giver')
    g['projects']=[proj('care_controller',['CARE'],'controller'),
                   proj('feed_child',['FEED'],'nadia')]
    c=adult('controller','Controller');c['body']['rest']=1.
    c['projects']=[proj('enforce',['SANCTION_PANTRY_ACCESS'],'third')]
    n=newborn('nadia','Nadia');n['body']['nutrition']=.4
    w=blank_world();w['accounts'].update({'controller':9.,'giver':6.})
    w['holdings']={'controller':{'food':2.},'giver':{'food':0.}}
    w['sites']['workshop']['food']=6.
    rt.ledger.initialize(w,[g,c,adult('third','Third'),n])
    return rt.register_sourcefree_pantry_concession({
        'grade':'EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO','site':'home',
        'possible_controller':'controller','eligible_petitioners':['controller','giver'],
        'quorum':2,'source_ref':'r65:fictional-concession'})

class ContradictoryLife(unittest.TestCase):
    def arm(self,db,mode,full=False):
        phase={'stage':'care'};seen=[];acquired=[]
        def cb(task,p):
            a=p.get('actor',{}).get('id');s=phase['stage']
            if task=='expression':return {'task':task,'surface':'Ordinary life.'}
            if task=='development':
                out=[]
                if a=='giver':
                    if s=='care':
                        if 'caring' not in p['actor'].get('forms',{}):
                            # Only one initial form, on an actually chosen care course.
                            if not acquired:
                                out.append({'kind':'ADD_FORM','form':{
                                    'id':'caring','kind':'RELATIONAL_INVESTMENT',
                                    'cues':['controller'],'enables':['CARE']}})
                                acquired.append('caring')
                        out+=p.get('historically_possible_care_practices',[])
                    if s=='blocked' and 'frustrated' not in acquired:
                        out.append({'kind':'ADD_FORM','form':{'id':'frustrated',
                            'kind':'RELATIONAL_INVESTMENT','cues':['performed_feed'],
                            'enables':['ORIENT']}})
                        out.extend({'kind':'LINK_FORMS','source':'caring','target':'frustrated',
                                    'relation':rel,'contexts':[]} for rel in ('RECRUITS','SUPPORTS'))
                        acquired.append('frustrated')
                    if s=='sanction':
                        care=p.get('historically_possible_care_practice_revisions',[])
                        links=p.get('historically_possible_care_authority_revaluations',[])
                        seen.extend(deepcopy(care))
                        if care and mode not in ('abstain','absent'):
                            wanted=('KEEP_CONTRADICTORY_RECRUITMENT' if mode=='keep'
                                    else 'SUSPEND_PARTICULAR_RECRUITMENT')
                            q=deepcopy(next(x for x in care if x['revision_mode']==wanted))
                            q['interpretive_hypothesis']='Care does not settle my relation to this power.'
                            if mode=='forge':q['basis']['power_event_ref']='invented'
                            out.append(q)
                            if mode=='partition':
                                x=links[0]
                                out.append({'kind':'REVALUE_RELATION','relation_id':x['relation_id'],
                                    'lived_care_authority_basis':x['lived_care_authority_basis'],
                                    'new_relation':'QUARANTINES_FROM',
                                    'interpretive_hypothesis':'Keep these experiences apart here.'})
                    if s=='commons_feed':
                        out+=p.get('historically_possible_commons_provisioning_reorganizations',[])
                    if s=='wage_feed':
                        out+=p.get('historically_possible_provisioning_reorganizations',[])
                    if s=='defer_material':
                        out.extend({'kind':'ACQUIRE_INTERACTIVITY_RELATION','basis':x,
                            'personal_sense':'Both demands occupy this life.'}
                            for x in p.get('historically_possible_interactivity_relations',[]))
                    if s=='renew':
                        out.extend({**x,'interpretive_hypothesis':'This practice can resume without erasing what happened.'}
                            for x in p.get('historically_possible_care_practice_revisions',[])
                            if x['revision_mode']=='REOPEN_PARTICULAR_RECRUITMENT')
                return {'task':task,'candidates':out}
            if task=='actor_attempt':
                if p.get('requesting_actor') is not None:return {'task':task,'action':'REFUSE'}
                if a=='controller' and s=='sanction':
                    return selection(task,options(p,'SANCTION_PANTRY_ACCESS','enforce')[0])
                if a=='giver':
                    if s in ('care','renew','defer_care'):
                        o=options(p,'CARE','care_controller')[0]
                        if s=='defer_care':
                            return selection(task,o,defer_course_option_id=options(
                                p,'CONTRIBUTE_FOOD_COMMONS','feed_child')[0]['option_id'])
                        return selection(task,o)
                    if s in ('blocked','blocked_again','commons_feed','wage_feed'):
                        return selection(task,options(p,'FEED','feed_child')[0])
                    if s=='donate':
                        return selection(task,options(p,'CONTRIBUTE_FOOD_COMMONS')[0])
                    if s=='defer_material':
                        return selection(task,options(p,'CONTRIBUTE_FOOD_COMMONS','feed_child')[0],
                            defer_course_option_id=options(p,'CARE','care_controller')[0]['option_id'])
                    if s=='shortcut':
                        alts=[x for x in p['practical_options'] if x.get('grounds_status')==
                              'HISTORICALLY_PRACTICED_PARTICULAR_CARE'
                              and x['world_request'].get('addressed_party_ref')=='controller']
                        if alts:return selection(task,alts[0])
                return {'task':task,'action':'WAIT'}
            raise AssertionError(task)
        svc=ValidatingSemanticService(CallbackLLMProvider(cb))
        rt=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            source=setup(rt)
            for _ in range(2):
                self.assertEqual(rt.step('giver')['status'],'PERFORMED')
                rt.step('giver',requested_action='REST')
            old=deepcopy(rt.ledger.actor('giver')[1]['care_practical_commitments'][0])
            phase['stage']='setup'
            rt.step('controller',requested_action='INSPECT',object_ref=source['notice_ref'])
            self.assertEqual(rt.step('controller',requested_action='INSTALL_PANTRY_GATE')['status'],'PERFORMED')
            phase['stage']='blocked'
            self.assertEqual(rt.step('giver')['status'],'BLOCKED')
            self.assertIn('frustrated',forms(rt.situated('giver')))
            if mode=='absent':
                phase['stage']='setup'
                rt.step('giver',requested_action='MOVE',object_ref='workshop')
            phase['stage']='sanction'
            before=deepcopy(rt.ledger.world());a0=deepcopy(rt.ledger.actor('giver')[1])
            if mode=='forge':
                with self.assertRaises(InvalidDevelopment):rt.step('controller')
                self.assertEqual(rt.ledger.world(),before)
                self.assertEqual(rt.ledger.actor('giver')[1],a0)
                self.assertTrue(rt.verify()['valid']);return
            self.assertEqual(rt.step('controller')['status'],'PERFORMED')
            g=rt.ledger.actor('giver')[1]
            if mode=='absent':
                self.assertEqual(seen,[])
                self.assertEqual(g['care_practical_commitments'][0],old)
                return
            self.assertTrue(seen)
            received=[x['received_enacted_food_power'] for x in g['evidence_paths']
                      if x.get('received_enacted_food_power',{}).get('operation')=='SANCTION_PANTRY_ACCESS']
            self.assertEqual(len(received),1)
            self.assertNotIn('subject',received[0]);self.assertNotIn('payment_ref',received[0])
            row=g['care_practical_commitments'][0]
            self.assertEqual({k:v for k,v in row.items() if k!='revisions'},old)
            v=rt.situated('giver')
            self.assertEqual('frustrated' in forms(v),mode!='partition')
            if mode=='partition':
                self.assertTrue(any(c['kind']=='CONTEXTUAL_ASSOCIATIVE_PARTITION' for c in v['currents']))
                self.assertTrue(quarantine_pairs(g['links'],'home'))
                self.assertFalse(quarantine_pairs(g['links'],'workshop'))
                self.assertTrue(all(x['relation'] in ('RECRUITS','SUPPORTS') for x in g['links']))
            care=practical(v,'CARE')
            self.assertEqual(any(x.get('grounds_status')=='HISTORICALLY_PRACTICED_PARTICULAR_CARE'
                                 for x in care),mode!='partition')
            self.assertEqual(any(x.get('care_contradictions_analytic_only') for x in care),mode!='abstain')
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
        rt=ConstitutiveRuntime(str(db),semantic=svc)
        try:
            phase['stage']='shortcut'
            self.assertEqual(rt.step('giver')['attempt'],'WAIT' if mode=='partition' else 'CARE')
            if not full:
                self.assertTrue(rt.verify()['valid']);return
            # Direct encounter is not erased by the contextual partition.
            phase['stage']='setup'
            rt.step('controller',requested_action='REST')
            self.assertEqual(rt.step('controller',requested_action='MAINTAIN_PANTRY_GATE')['status'],'PERFORMED')
            phase['stage']='blocked_again'
            self.assertEqual(rt.step('giver')['status'],'BLOCKED')
            self.assertIn('frustrated',forms(rt.situated('giver')))
            phase['stage']='setup'
            rt.step('giver',requested_action='MOVE',object_ref='workshop')
            rt.step('controller',requested_action='MOVE',object_ref='workshop')
            self.assertIn('frustrated',forms(rt.situated('giver')))
            rt.step('controller',requested_action='MOVE',object_ref='home')
            self.assertEqual(rt.step('giver',requested_action='BUY_FOOD')['status'],'PERFORMED')
            rt.step('giver',requested_action='MOVE',object_ref='home')
            rt.step('giver',requested_action='REST')
            phase['stage']='donate'
            self.assertEqual(rt.step('giver')['status'],'PERFORMED')
            self.assertEqual(rt.ledger.world()[1]['sites']['home']['mutual_aid_food'],1.)
            phase['stage']='commons_feed'
            self.assertEqual(rt.step('giver')['status'],'PERFORMED')
            g=rt.ledger.actor('giver')[1]
            project=next(x for x in g['projects'] if x['id']=='feed_child')
            self.assertEqual(project['means'],['FEED','CONTRIBUTE_FOOD_COMMONS'])
            self.assertEqual(project['addressed_party_ref'],'nadia')
            self.assertEqual(g['performed_feeding_events'][-1]['material_food_source'],'MUTUAL_AID_FOOD')
            phase['stage']='setup'
            rt.step('giver',requested_action='MOVE',object_ref='workshop')
            for _ in range(2):
                rt.step('giver',requested_action='REST')
                self.assertEqual(rt.step('giver',requested_action='BUY_FOOD')['status'],'PERFORMED')
            self.assertFalse(any(x.get('project_id')=='feed_child' for x in practical(
                rt.situated('giver'),'CONTRIBUTE_FOOD_COMMONS')))
            rt.step('giver',requested_action='MOVE',object_ref='home')
            rt.step('giver',requested_action='REST')
            phase['stage']='defer_care'
            self.assertEqual(rt.step('giver')['status'],'PERFORMED')
            phase['stage']='defer_material'
            self.assertEqual(rt.step('giver')['status'],'PERFORMED')
            g=rt.ledger.actor('giver')[1]
            project=next(x for x in g['projects'] if x['id']=='feed_child')
            self.assertEqual(len(project['interactivity_relations']),1)
            self.assertTrue(any(x.get('interactivity_currents') for x in practical(
                rt.situated('giver'),'CARE')+practical(rt.situated('giver'),'CONTRIBUTE_FOOD_COMMONS')))
            phase['stage']='renew'
            self.assertEqual(rt.step('giver')['status'],'PERFORMED')
            row=rt.ledger.actor('giver')[1]['care_practical_commitments'][0]
            self.assertEqual([x['mode'] for x in row['revisions']],
                ['SUSPEND_PARTICULAR_RECRUITMENT','REOPEN_PARTICULAR_RECRUITMENT'])
            self.assertTrue(any(x.get('grounds_status')=='HISTORICALLY_PRACTICED_PARTICULAR_CARE'
                                for x in practical(rt.situated('giver'),'CARE')))
            # The same project can acquire market-mediated and independent
            # means without treating either as a total motive replacement.
            phase['stage']='setup'
            spec=rt.register_sourcefree_work_regime({
                'grade':'EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO',
                'source_ref':'r65:employment','site':'workshop',
                'controller':'workshop_steward','eligible_workers':['giver','controller'],
                'delegates':['controller']})
            rt.step('giver',requested_action='MOVE',object_ref='workshop')
            rt.step('giver',requested_action='INSPECT',object_ref=spec['terms_notice_ref'])
            self.assertEqual(rt.step('giver',requested_action='ACCEPT_WORK_TERMS')['status'],'PERFORMED')
            rt.step('giver',requested_action='REST')
            self.assertEqual(rt.step('giver',requested_action='WORK')['status'],'PERFORMED')
            self.assertEqual(rt.step('giver',requested_action='BUY_FOOD')['status'],'PERFORMED')
            rt.step('giver',requested_action='MOVE',object_ref='home')
            rt.step('giver',requested_action='REST')
            phase['stage']='wage_feed'
            self.assertEqual(rt.step('giver')['status'],'PERFORMED')
            project=next(x for x in rt.ledger.actor('giver')[1]['projects'] if x['id']=='feed_child')
            self.assertEqual(project['means'],['FEED','CONTRIBUTE_FOOD_COMMONS','WORK','BUY_FOOD'])
            self.assertTrue(project['commons_provisioning_basis'])
            self.assertTrue(project['provisioning_means_basis'])
            self.assertTrue(rt.verify()['valid'])
        finally:rt.close()
    def test_longitudinal_contradiction_partition_commons_time_and_reopening(self):
        with tempfile.TemporaryDirectory() as d:self.arm(Path(d)/'full.sqlite', 'partition',True)
    def test_same_power_retained_care_or_abstention(self):
        with tempfile.TemporaryDirectory() as d:
            for mode in ('keep','abstain'):self.arm(Path(d)/(mode+'.sqlite'),mode)
    def test_forged_power_evidence_rolls_back(self):
        with tempfile.TemporaryDirectory() as d:self.arm(Path(d)/'forge.sqlite','forge')
    def test_absent_actor_not_given_power_reception(self):
        with tempfile.TemporaryDirectory() as d:self.arm(Path(d)/'absent.sqlite','absent')

    def test_materially_reproduced_power_can_depend_on_received_feeding(self):
        def arm(db,feed):
            phase={'stage':'setup','threshold':0.}
            def cb(task,p):
                if task=='expression':return {'task':task,'surface':'Ordinary life.'}
                if task=='development':return {'task':task,'candidates':[]}
                if task=='actor_attempt':
                    if p.get('requesting_actor') is not None:return {'task':task,'action':'REFUSE'}
                    a=p['actor']['id'];s=phase['stage']
                    if s=='petition' and a in ('giver','controller'):
                        return {'task':task,'action':'SIGN_FOOD_PETITION'}
                    if a=='giver' and s=='support' and feed:
                        return selection(task,options(p,'FEED','support')[0])
                    if a=='controller' and s=='power' and p['actor']['body']['nutrition']>=phase['threshold']:
                        return selection(task,options(p,'SANCTION_PANTRY_ACCESS','enforce')[0])
                    if a=='third' and s=='child':
                        return selection(task,options(p,'FEED','child')[0])
                    return {'task':task,'action':'WAIT'}
                raise AssertionError(task)
            svc=ValidatingSemanticService(CallbackLLMProvider(cb))
            rt=ConstitutiveRuntime(str(db),semantic=svc)
            try:
                g=adult('giver','Giver');g['projects']=[proj('support',['FEED'],'controller')]
                c=adult('controller','Controller');c['body']['nutrition']=.4;c['body']['rest']=1.
                c['projects']=[proj('enforce',['SANCTION_PANTRY_ACCESS'],'third')]
                t=adult('third','Third');t['projects']=[proj('child',['FEED'],'nadia')]
                n=newborn('nadia','Nadia');n['body']['nutrition']=.4
                w=blank_world();w['accounts']['controller']=9.
                w['holdings']={'controller':{'food':3.},'giver':{'food':2.}}
                rt.ledger.initialize(w,[g,c,t,n])
                # Independently witnessed own material care history qualifies the petition.
                for a in ('giver','controller'):
                    self.assertEqual(rt.step(a,requested_action='FEED',target='third')['status'],'PERFORMED')
                src=rt.register_sourcefree_pantry_concession({
                    'grade':'EXPLICIT_SOURCEFREE_INSTITUTIONAL_SCENARIO','site':'home',
                    'possible_controller':'controller','eligible_petitioners':['controller','giver'],
                    'quorum':2,'source_ref':'r65:material-reproduction'})
                rt.step('controller',requested_action='INSPECT',object_ref=src['notice_ref'])
                self.assertEqual(rt.step('controller',requested_action='INSTALL_PANTRY_GATE')['status'],'PERFORMED')
                board=rt.ledger.world()[1]['institutions']['household_food_board']
                for a in ('controller','giver'):
                    rt.step(a,requested_action='INSPECT',object_ref=board['public_notice_ref'])
                self.assertEqual(rt.step('controller',requested_action='MAINTAIN_PANTRY_GATE')['status'],'PERFORMED')
                phase['stage']='petition'
                for a in ('giver','controller'):
                    self.assertEqual(rt.step(a)['status'],'PERFORMED')
                self.assertEqual(rt.ledger.world()[1]['institutions']['household_food_board']['food_rights'],'SHARED_BY_COLLECTIVE_ACTS')
                phase['threshold']=rt.ledger.actor('controller')[1]['body']['nutrition']+.05
                phase['stage']='support'
                self.assertEqual(rt.step('giver')['status'],'PERFORMED')
                phase['stage']='power'
                self.assertEqual(rt.step('controller')['attempt'],'SANCTION_PANTRY_ACCESS' if feed else 'WAIT')
                phase['stage']='child'
                self.assertEqual(rt.step('third')['status'],'BLOCKED' if feed else 'PERFORMED')
                world=rt.ledger.world()[1]
                self.assertEqual(world['institutions']['household_food_board']['food_rights'],'SHARED_BY_COLLECTIVE_ACTS')
                self.assertEqual(world['accounts']['controller'],5. if feed else 7.)
                self.assertTrue(rt.verify()['valid'])
                return rt.ledger.actor('nadia')[1]['body']['nutrition'],world['sites']['home']['food']
            finally:rt.close()
        with tempfile.TemporaryDirectory() as d:
            a=arm(Path(d)/'support.sqlite',True);b=arm(Path(d)/'no-support.sqlite',False)
            self.assertLess(a[0],b[0]);self.assertEqual(a[1],b[1]+1)
