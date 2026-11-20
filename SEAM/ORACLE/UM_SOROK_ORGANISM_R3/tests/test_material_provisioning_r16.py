"""R16 material household reproduction and independent live-feeding court.

Sourcefree research fixtures are NOT observed family histories or a human
developmental law. REMONT independently executes exact source normal/-O.
"""
import tempfile
import unittest
from pathlib import Path

from um_sorok_organism.types import newborn, adult, blank_world
from um_sorok_organism.ordinary_life import passage
from um_sorok_organism.historical_social_reproduction import (
    qualify_period_allocation)
from um_sorok_organism.routine_sources import (
    register_sourcefree_period_envelope)
from um_sorok_organism.runtime import ConstitutiveRuntime


PARENT={'source_ref':'r16_sourcefree_research_parent',
        'answers':{'explicit_fictional_condition':'fixture_answer_not_original_survey'},
        'source_grade':'UNQUALIFIED_FICTIONAL_TEST_FIXTURE',
        'fictional_seed':{'projects':[]}}


def family(include_sibling=False):
    world=blank_world()
    actors={'mother':adult('mother','Mother'),
            'father':adult('father','Father'),
            'nadia':newborn('nadia','Nadia')}
    if include_sibling:
        actors['sibling']=newborn('sibling','Sibling')
    for aid,actor in actors.items():
        world['positions'][aid]='home'
        actor['location']='home'
        if actor['role']=='adult':
            actor['projects']=[{'id':'care:'+aid,'status':'active',
                                'means':['CARE','FEED'],
                                'object':'continuing situated care'}]
    return world,actors


def process(world,actors,giver,recipient,days=10,units=1,
            origin='SHARED_SITE_FOOD',hours=2,desc='fixture'):
    source=register_sourcefree_period_envelope(world,actors,{
        'kind':'QUALIFIED_MATERIAL_FEEDING','actor':giver,
        'location':'home','start_clock':world['clock'],
        'end_clock':world['clock']+days,
        'max_hours_per_active_day':hours,
        'description':desc+giver+recipient})
    return {'kind':'QUALIFIED_MATERIAL_FEEDING',
        'actor':giver,'recipient':recipient,'location':'home',
        'source_ref':source['id'],'supply_origin':origin,
        'food_units_per_active_day':units,
        'hours_per_active_day':hours,
        'provisional_exposure_fraction':1.0}


class R16MaterialPeriod(unittest.TestCase):
    def test_one_qualified_household_history_consumes_food_and_changes_body(self):
        w,a=family()
        before=a['nadia']['body']['nutrition']
        p=process(w,a,'mother','nadia',days=20,units=.5)
        period=passage(w,a,20,[p])
        self.assertEqual(w['sites']['home']['food'],2)
        self.assertGreater(a['nadia']['body']['nutrition'],before)
        records=w['material_provisioning_periods']
        self.assertEqual(len(records),1)
        self.assertEqual(records[0]['consumed_food_units'],10)
        self.assertEqual(records[0]['uncovered_food_units'],0)
        self.assertEqual(len(period['material_feeding_period_refs']),1)
        self.assertFalse(a['nadia']['memories'])
        self.assertFalse(a['nadia']['co_regulation_orientations'])

    def test_competing_recipients_material_ration_not_registration_order(self):
        def scenario(reversed_order):
            w,a=family(include_sibling=True)
            ps=[
                process(w,a,'mother','nadia',days=10,units=1,
                        desc='first'),
                process(w,a,'father','sibling',days=10,units=1,
                        desc='second')]
            passage(w,a,10,list(reversed(ps)) if reversed_order else ps)
            records={x['recipient']:x for x in w['material_provisioning_periods']}
            return w,a,records
        wa,aa,ra=scenario(False)
        wb,ab,rb=scenario(True)
        self.assertEqual(wa['sites']['home']['food'],0)
        self.assertEqual(wb['sites']['home']['food'],0)
        for recipient in ('nadia','sibling'):
            self.assertEqual(ra[recipient]['consumed_food_units'],6)
            self.assertEqual(rb[recipient]['consumed_food_units'],6)
            self.assertEqual(ra[recipient]['uncovered_food_units'],4)
            self.assertEqual(aa[recipient]['body']['nutrition'],
                             ab[recipient]['body']['nutrition'])
        self.assertEqual(sum(x['consumed_food_units'] for x in ra.values()),12)

    def test_actor_owned_food_and_shared_food_are_not_same_claim(self):
        w,a=family()
        w['holdings']={'mother':{'food':2.0}}
        p=process(w,a,'mother','nadia',days=3,units=1,
                  origin='GIVER_HELD_FOOD')
        passage(w,a,3,[p])
        row=w['material_provisioning_periods'][0]
        self.assertEqual(row['consumed_food_units'],2)
        self.assertEqual(row['uncovered_food_units'],1)
        self.assertEqual(w['holdings']['mother']['food'],0)
        self.assertEqual(w['sites']['home']['food'],12)
        self.assertEqual(row['material_status'],'PARTIALLY_PROVISIONED')

    def test_empty_household_records_material_unmet_not_caregiver_rejection(self):
        w,a=family()
        w['sites']['home']['food']=0
        p=process(w,a,'mother','nadia',days=5,units=1)
        before=a['nadia']['body']['nutrition']
        passage(w,a,5,[p])
        row=w['material_provisioning_periods'][0]
        self.assertEqual(row['consumed_food_units'],0)
        self.assertEqual(row['uncovered_food_units'],5)
        self.assertEqual(row['material_status'],'UNPROVISIONED_NO_AVAILABLE_FOOD')
        self.assertLess(a['nadia']['body']['nutrition'],before)
        self.assertTrue(row['failure_is_not_evidence_of_caregiver_unwillingness'])

    def test_unsourced_source_ref_and_overbooked_feeding_deny_phantom_history(self):
        w,a=family(include_sibling=True)
        p=process(w,a,'mother','nadia',days=2,units=1,hours=12)
        q=process(w,a,'mother','sibling',days=2,units=1,hours=12)
        self.assertEqual(w['clock'],0)
        before=w['sites']['home']['food']
        with self.assertRaisesRegex(ValueError,'HISTORICAL_TIME_OVERBOOKED_ACTOR'):
            passage(w,a,2,[p,q])
        self.assertEqual(w['sites']['home']['food'],before)
        self.assertEqual(w.get('material_provisioning_periods',[]),[])
        p={**p,'source_ref':'fake_authority'}
        with self.assertRaisesRegex(ValueError,'UNREGISTERED_SOURCE_ENVELOPE'):
            qualify_period_allocation(w,a,[p],0,2)


class R16LiveMaterialAction(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.rt=ConstitutiveRuntime(str(
            Path(self.tmp.name)/'r16.sqlite3'))
        self.addCleanup(self.rt.close)
        self.rt.initialize([('mother','Mother',PARENT),
                            ('father','Father',PARENT)])

    def test_care_does_not_create_food_or_nutrition(self):
        before=self.rt.snapshot('nadia')['body']['nutrition']
        effect=self.rt.step('mother',requested_action='CARE',target='nadia')
        self.assertEqual(effect['status'],'PERFORMED')
        self.assertLessEqual(
            self.rt.snapshot('nadia')['body']['nutrition'],before)
        self.assertEqual(len(self.rt.ledger.world('w1')[1][
            'material_feeding_events']),0)

    def test_real_feed_consumes_stock_and_writes_distinct_lived_histories(self):
        before=self.rt.snapshot('nadia')['body']['nutrition']
        output=self.rt.step('mother',requested_action='FEED',target='nadia')
        self.assertEqual(output['status'],'PERFORMED')
        mother=self.rt.snapshot('mother')
        child=self.rt.snapshot('nadia')
        world=self.rt.ledger.world('w1')[1]
        self.assertEqual(world['sites']['home']['food'],11)
        self.assertGreater(child['body']['nutrition'],before)
        self.assertEqual(len(world['material_feeding_events']),1)
        self.assertEqual(len(mother['performed_feeding_events']),1)
        self.assertEqual(len(child['experienced_care_events']),1)
        self.assertEqual(child['experienced_care_events'][0][
            'source_care_event_type'],'RECEIVED_UNSOLICITED_CARE')
        self.assertFalse(child['self_model'])
        self.assertTrue(self.rt.verify()['valid'])

    def test_prior_material_feeding_can_inform_independent_answer_to_signal(self):
        self.rt.step('mother',requested_action='FEED',target='nadia')
        self.rt.step('nadia',requested_action='ORIENT')
        self.assertEqual(len(self.rt.snapshot('nadia')[
            'co_regulation_orientations']),1)
        # Reproduction becomes materially scarce through continuing time.
        # The child has a separately formed history, not a scripted act.
        self.rt.background(600)
        planned=self.rt.plan('nadia')
        self.assertEqual(planned.action,'SIGNAL')
        self.assertEqual(planned.target,'mother')
        food_before=self.rt.ledger.world('w1')[1]['sites']['home']['food']
        performed=self.rt.step('nadia')
        self.assertEqual(performed['attempt'],'SIGNAL')
        self.assertEqual(performed['coactor'],'FEED')
        self.assertEqual(
            self.rt.ledger.world('w1')[1]['sites']['home']['food'],
            food_before-1)
        self.assertTrue(self.rt.verify()['valid'])

    def test_no_stock_blocks_feed_without_fabricated_benefit(self):
        # A child has lived material deprivation; the caregiver can still
        # genuinely attempt care. Insufficient material means no feeding.
        w=self.rt.ledger.world('w1')[1]
        w['sites']['home']['food']=0
        # The sole test-only world mutation must occur via ledger commit;
        # direct fetched dicts are copies and do not alter persistent world.
        version,original=self.rt.ledger.world('w1')
        original['sites']['home']['food']=0
        self.rt.ledger.commit('w1',version,original,{}, {},
                              'SOURCEFREE_TEST_STOCK_DEPLETION',None,
                              {'external_material_fixture':True})
        before=self.rt.snapshot('nadia')['body']['nutrition']
        result=self.rt.step('mother',requested_action='FEED',target='nadia')
        self.assertEqual(result['status'],'BLOCKED')
        self.assertLessEqual(
            self.rt.snapshot('nadia')['body']['nutrition'],before)
        self.assertEqual(len(self.rt.ledger.world('w1')[1][
            'material_feeding_events']),0)


if __name__=='__main__':
    unittest.main()
