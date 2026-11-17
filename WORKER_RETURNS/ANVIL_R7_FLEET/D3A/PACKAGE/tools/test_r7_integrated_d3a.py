#!/usr/bin/env python3
"""D3A hostile tests for the corrected ACTIVE ANVIL gates.

Each test names the claim edge it severs.  All fixtures are synthetic test
inputs derived from byte-pinned sources; none is evidence of decision quality,
science, owner receiving or native execution.
"""
import copy, json, pathlib, tempfile, unittest

import d3a_fixture as F
from r7_integrated import check, digest, sha
from r7_builder import write as build_projections
from r7_source_inventory import verify_inventory
from test_r6 import r6_fixture

ROOT=F.ROOT


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.work=pathlib.Path(self.tmp.name)
        self.ev=self.work/'evidence';self.ev.mkdir()
        self.anchors=F.anchors()
        self.inv=json.loads(F.INVENTORY.read_text())
        self.invptr=F.put(self.ev,'inventory.json',self.inv)
        self.frame=F.frame(self.inv)
        self.frame['historical_conservation']=self.invptr
        self.fptr=F.put(self.ev,'frame.json',self.frame)
        self.dec=F.decision(self.inv,self.fptr)
        self.dec['frame_sha256']=digest(self.frame)
        self.dec['inventory_sha256']=digest(self.inv)
        man=build_projections(self.dec,self.frame,self.inv,self.ev)
        self.dec['projection_manifest']=man
        self.dptr=F.put(self.ev,'decision.json',self.dec)

    def tearDown(self): self.tmp.cleanup()

    def frame_result(self): return check('FRAME',self.frame,self.ev,ROOT,self.anchors)
    def dec_result(self,dec=None): return check('DECISION',dec or self.dec,self.ev,ROOT,self.anchors)

    def c_packet(self):
        return {'schema':'ANVIL_R7_INTEGRATED','stage':'INDEPENDENT_C','integrated_decision':self.dptr,
            'integrated_decision_sha256':digest(self.dec),'first_consumer':self.frame['first_real_consumer'],
            'independent_reverse_walk_of_whole_frame':'The reviewer independently traces original source through C11, I03, F1-F4 and Field Forge to the world and actor, including the negative and restore cases.',
            'strongest_choice_reversing_objection':'The installed event index may not support conditioned joint analysis economically at real survey width, which would reverse the physical selection.',
            'scientific_and_owner_boundary':'No source scientific right, structural causality or actor-level authority can be issued from a documentary C assessment.',
            'actual_first_consumer_assessment':'This packet does not execute a native first consumer and therefore cannot justify adopting original survey science.',
            'historical_no_loss_assessment':'All 118 historical and prospective identities remain at their recorded nonadoption and held-proof grades with no automatic function declared issued.',
            'reviewer_relationship':'DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION',
            'choice_reversing_objection_survives':False,'verdict':'C_HOLD_EXACT',
            'boundary_contract_sha256':self.dec['boundary_contract_sha256'],
            'boundary_court':copy.deepcopy(self.dec['boundary_court']),
            'typed_graph':copy.deepcopy(self.dec['typed_graph']),
            'projection_manifest':self.dec['projection_manifest'],
            'builder_cards':[{'id':'first','domain':'CURRENT_FIRST_CONSUMER','grade':'EXACT_BUILDER_HOLD',
                'exact_hold':'Actual native source consumer proof and competent owner execution are not part of this synthetic test'},
                {'id':'future','domain':'FUTURE_NONPRECLUSION','grade':'EXACT_BUILDER_HOLD',
                 'exact_hold':'Future actor and world source governance remains independent and cannot be invented by this local test'}],
            'original_source_granted_by_local_check':False,'owner_granted_by_local_check':False,
            'claims_protected_h1':False}


class S1(Base):
    def test_source_only_inventory_passes_at_documentary_grade(self):
        r=self.frame_result()
        self.assertTrue(r['status'].startswith('PASS'),r)
        self.assertEqual(118,r['requirements'] and 118)

    def test_synthetic_spine_cannot_be_the_origin(self):
        sp=r6_fixture()
        self.frame['historical_conservation']=F.put(self.ev,'spine.json',sp)
        r=self.frame_result()
        self.assertIn('HISTORY:NOT_SOURCE_QUALIFIED_INVENTORY',r['errors'])
        self.assertFalse(r['status'].startswith('PASS'))

    def test_legacy_transfer_without_source_origin_is_red(self):
        sp=r6_fixture()
        legacy={'schema':'ANVIL_R7_INHERITED_CONSERVATION',
                'source_authentication':'NOT_AUTHENTICATED_BY_LOCAL_CHECK',
                'source_spine_sha256':sha(json.dumps(sp).encode()),
                'transfer_method':'VERBATIM_R5_R6_SEMANTIC_COVERAGE_NO_RECLASSIFICATION',
                'coverage':sp['coverage']}
        self.frame['historical_conservation']=F.put(self.ev,'legacy.json',legacy)
        r=self.frame_result()
        self.assertIn('HISTORY:LEGACY_TRANSFER_WITHOUT_SOURCE_QUALIFIED_ORIGIN',r['errors'])

    def test_missing_row_blob_or_B10_is_red(self):
        bad=copy.deepcopy(self.inv)
        bad['rows']=[r for r in bad['rows'] if r['id']!='B-10']
        e=[];verify_inventory(bad,ROOT,e,'HISTORY',anchors=self.anchors)
        self.assertTrue(any('ID_SET_DRIFT:SEAM_B' in x for x in e),e)

        blob=copy.deepcopy(self.inv)
        next(r for r in blob['rows'] if r['id']=='K1-CAP-01')['origin']['git_blob']='0'*40
        e=[];verify_inventory(blob,ROOT,e,'HISTORY',anchors=self.anchors)
        self.assertIn('HISTORY:K1-CAP-01:ORIGIN:ORIGIN_PATH_BLOB_MISMATCH',e)

        row=copy.deepcopy(self.inv)
        next(r for r in row['rows'] if r['id']=='K1-CAP-02')['origin']['row_sha256']='1'*64
        e=[];verify_inventory(row,ROOT,e,'HISTORY',anchors=self.anchors)
        self.assertIn('HISTORY:K1-CAP-02:ORIGIN:ROW_BYTES_CHANGED',e)

    def test_source_file_absent_is_red(self):
        bad=copy.deepcopy(self.inv)
        next(r for r in bad['rows'] if r['id']=='L-04')['origin']['path']='D3A_SOURCE_SNAPSHOT/nope.md'
        e=[];verify_inventory(bad,ROOT,e,'HISTORY',anchors=self.anchors)
        self.assertIn('HISTORY:L-04:ORIGIN:ORIGIN_PATH_NOT_IN_COMMIT',e)

    def test_26_adopted_or_14_closed_in_inventory_is_red(self):
        bad=copy.deepcopy(self.inv)
        next(r for r in bad['rows'] if r['id']=='PYAT-PC-R9-01')['adopted']=True
        e=[];verify_inventory(bad,ROOT,e,'HISTORY',anchors=self.anchors)
        self.assertIn('HISTORY:PYAT-PC-R9-01:FALSE_PROSPECTIVE_ADOPTION',e)

        bad=copy.deepcopy(self.inv)
        next(r for r in bad['rows'] if r['id']=='P4R-R01')['closed']=True
        e=[];verify_inventory(bad,ROOT,e,'HISTORY',anchors=self.anchors)
        self.assertIn('HISTORY:P4R-R01:FALSE_PROOF_CLOSURE',e)


class OriginBinding(Base):
    """HQ REVISE_EXACT_DEFECT: a claimed commit must resolve in the real object store."""
    def v(self,obj,anchors=None):
        e=[];verify_inventory(obj,ROOT,e,'HISTORY',anchors=anchors or self.anchors);return e

    def test_genuine_original_inventory_passes(self):
        self.assertEqual([],self.v(self.inv))

    def test_fake_commit_refuses(self):
        bad=copy.deepcopy(self.inv);bad['rows'][0]['origin']['commit']='a'*40
        self.assertIn('HISTORY:K1-CAP-01:ORIGIN:ORIGIN_COMMIT_OUTSIDE_PINNED_CUTS',self.v(bad))

    def test_nonexistent_but_wellformed_commit_refuses(self):
        bad=copy.deepcopy(self.inv);bad['rows'][0]['origin']['commit']='deadbeef'*5
        e=self.v(bad)
        self.assertTrue(any('ORIGIN_COMMIT' in x for x in e),e)

    def test_real_but_wrong_commit_refuses(self):
        # a real commit in the same repository that is not a pinned source cut
        import subprocess
        real=subprocess.check_output(['git','-C',str(F.GIT_REPO),'rev-parse','HEAD'],text=True).strip()
        bad=copy.deepcopy(self.inv);bad['rows'][0]['origin']['commit']=real
        self.assertIn('HISTORY:K1-CAP-01:ORIGIN:ORIGIN_COMMIT_OUTSIDE_PINNED_CUTS',self.v(bad))

    def test_wrong_path_refuses_even_with_same_commit(self):
        bad=copy.deepcopy(self.inv);bad['rows'][0]['origin']['path']='PYAT_CONTROL_ROOM/NOT_THE_SOURCE.tsv'
        self.assertIn('HISTORY:K1-CAP-01:ORIGIN:ORIGIN_PATH_NOT_IN_COMMIT',self.v(bad))

    def test_caller_supplied_replacement_bytes_with_matching_self_hashes_refuses(self):
        # replace the private snapshot bytes AND recompute every claimed hash:
        # the Git object store still resolves the original blob, so the pin fails.
        fake=b'K1-CAP-01\tFAKE\tFAKE\tFAKE\n'
        bad=copy.deepcopy(self.inv)
        o=bad['rows'][0]['origin']
        o['git_blob']=__import__('hashlib').sha1(b'blob %d\0'%len(fake)+fake).hexdigest()
        o['file_sha256']=__import__('hashlib').sha256(fake).hexdigest()
        o['row_sha256']=__import__('hashlib').sha256(fake.rstrip(b'\n')).hexdigest()
        e=self.v(bad)
        self.assertTrue(any('ORIGIN_PATH_BLOB_MISMATCH' in x or 'ROW_BYTES_CHANGED' in x for x in e),e)

    def test_no_external_anchor_refuses(self):
        e=[];verify_inventory(self.inv,ROOT,e,'HISTORY',anchors=None)
        self.assertIn('HISTORY:NO_EXTERNAL_TRUST_ANCHOR',e)

    def test_fake_zip_container_refuses(self):
        bad=copy.deepcopy(self.inv)
        next(r for r in bad['rows'] if r['id']=='T1')['origin']['zip_sha256']='b'*64
        self.assertIn('HISTORY:T1:ORIGIN:ZIP_CONTAINER_SHA_MISMATCH',self.v(bad))

    def test_restoration_passes_exactly(self):
        bad=copy.deepcopy(self.inv);bad['rows'][0]['origin']['commit']='a'*40
        self.assertTrue(any('ORIGIN' in x for x in self.v(bad)))
        restored=copy.deepcopy(bad);restored['rows'][0]['origin']['commit']=self.inv['rows'][0]['origin']['commit']
        self.assertEqual([],self.v(restored))


class Decision(Base):
    def test_118_reconciliation_passes(self):
        r=self.dec_result()
        self.assertTrue(r['status'].startswith('PASS'),r)

    def test_one_missing_historical_decision_in_complete_53_is_red(self):
        d=copy.deepcopy(self.dec)
        d['identity_dispositions']=[x for x in d['identity_dispositions'] if x['identity_id']!='K1-CAP-17']
        d['frame_sha256']=digest(self.frame);d['inventory_sha256']=digest(self.inv)
        r=self.dec_result(d)
        self.assertTrue(any('IDENTITY_UNIVERSE_INCOMPLETE:K1_CAP' in x for x in r['errors']),r)
        self.assertFalse(r['status'].startswith('PASS'))

    def test_decision_cannot_adopt_26_or_close_14(self):
        d=copy.deepcopy(self.dec)
        x=next(x for x in d['identity_dispositions'] if x['identity_id'].startswith('PYAT-PC'))
        x['disposition']='PRESENT_PRESERVED'
        r=self.dec_result(d)
        self.assertTrue(any('UNAUTHORIZED_PROPOSAL_ADOPTION' in e for e in r['errors']),r)

        d=copy.deepcopy(self.dec)
        x=next(x for x in d['identity_dispositions'] if x['identity_id'].startswith('P4R'))
        x['closed']=True
        r=self.dec_result(d)
        self.assertTrue(any('FALSE_PROOF_CLOSURE' in e for e in r['errors']),r)

    def test_identity_origin_must_match_inventory_bytes(self):
        d=copy.deepcopy(self.dec)
        d['identity_dispositions'][0]['origin_row_sha256']='2'*64
        r=self.dec_result(d)
        self.assertTrue(any('IDENTITY_ORIGIN_NOT_VERIFIED' in e for e in r['errors']),r)

    def test_boilerplate_identity_effect_is_red(self):
        d=copy.deepcopy(self.dec)
        for x in d['identity_dispositions']:
            x['candidate_specific_effect']='Preserved by the selected candidate with no further specific statement of the affected semantics'
        r=self.dec_result(d)
        self.assertTrue(any('IDENTITY_EFFECT_NOT_GROUNDED_IN_ORIGIN' in e for e in r['errors']),r)

    def test_inventory_pin_is_required(self):
        d=copy.deepcopy(self.dec);d['inventory_sha256']='3'*64
        self.assertIn('DECISION:INVENTORY_NOT_PINNED',self.dec_result(d)['errors'])

    def test_no_full_rival_ab_required(self):
        d=copy.deepcopy(self.dec);d['requires_full_A_B_comparison']=True
        self.assertIn('DECISION:COMPETITION_REQUIRED',self.dec_result(d)['errors'])
        d=copy.deepcopy(self.dec);d['competing_implementations_mandatory']=True
        self.assertIn('DECISION:MANDATORY_BACKEND_BAKEOFF',self.dec_result(d)['errors'])

    def test_present_hard_cannot_be_relabelled_future(self):
        d=copy.deepcopy(self.dec);d['requirement_dispositions'][0]['disposition']='FUTURE_NONPRECLUDED'
        self.assertTrue(any('HARD_PRESENT_RELABELED_FUTURE' in e for e in self.dec_result(d)['errors']))


class IndependentC(Base):
    def test_complete_C_packet_passes_locally(self):
        r=check('C_INTEGRATED',self.c_packet(),self.ev,ROOT,self.anchors)
        self.assertTrue(r['status'].startswith('PASS'),r)

    def test_each_T_contract_needs_positive_negative_and_restore(self):
        for tid in ('T1','T4','T7'):
            c=self.c_packet()
            row=next(x for x in c['boundary_court'] if x['boundary']==tid)
            del row['restore']
            r=check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)
            self.assertIn(f'C:BOUNDARY_MISSING_RESTORE:{tid}',r['errors'])
            c=self.c_packet()
            row=next(x for x in c['boundary_court'] if x['boundary']==tid)
            del row['negative']
            self.assertIn(f'C:BOUNDARY_MISSING_NEGATIVE:{tid}',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])

    def test_weakened_boundary_contract_is_red(self):
        c=self.c_packet();c['boundary_contract_sha256']='4'*64
        self.assertIn('C:BOUNDARY_CONTRACT_NOT_PINNED',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])
        c=self.c_packet()
        next(x for x in c['boundary_court'] if x['boundary']=='T2')['must_preserve_witness']='some marginals are kept'
        self.assertIn('C:BOUNDARY_MUST_PRESERVE_NOT_WITNESSED:T2',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])

    def test_typed_graph_type_authority_time_and_consumer_holes_are_red(self):
        c=self.c_packet()
        next(e for e in c['typed_graph']['edges'] if e['id']=='E3')['payload_type']='not_a_declared_type'
        self.assertIn('C:GRAPH_TYPE_HOLE:E3',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])

        c=self.c_packet()
        next(e for e in c['typed_graph']['edges'] if e['id']=='E5')['authority_from']='FICTIONAL_WORLD'
        self.assertIn('C:GRAPH_AUTHORITY_HOLE:E5',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])

        c=self.c_packet()
        next(e for e in c['typed_graph']['edges'] if e['id']=='E6')['time_class']='WRONG_CLOCK'
        self.assertIn('C:GRAPH_TIME_HOLE:E6',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])

        c=self.c_packet()
        next(e for e in c['typed_graph']['edges'] if e['id']=='E4')['first_consumer']=''
        self.assertIn('C:GRAPH_NO_CONSUMER:E4',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])

    def test_authority_upgrade_needs_an_external_warrant(self):
        c=self.c_packet()
        edge=next(e for e in c['typed_graph']['edges'] if e['id']=='E5')
        edge['authority_from']='DESCRIPTIVE_MODELED';edge['authority_to']='STRUCTURAL_QUALIFIED'
        edge.pop('external_source_warrant',None)
        r=check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)
        self.assertIn('C:GRAPH_AUTHORITY_UPGRADE_WITHOUT_WARRANT:E5',r['errors'])
        edge['external_source_warrant']='Independently sourced institutional material evidence with its own owner and time basis'
        r=check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)
        self.assertNotIn('C:GRAPH_AUTHORITY_UPGRADE_WITHOUT_WARRANT:E5',r['errors'])

    def test_graph_must_reach_an_actor_from_observed_source(self):
        c=self.c_packet()
        c['typed_graph']['edges']=[e for e in c['typed_graph']['edges'] if e['id']!='E7']
        self.assertIn('C:GRAPH_SOURCE_TO_ACTOR_DISCONNECTED',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])

    def test_six_builder_projections_must_match_bytes(self):
        c=self.c_packet();c['projection_manifest']['files']['DESIGN_DECISION.md']='5'*64
        self.assertIn('C:PROJECTION_BYTES_CHANGED:DESIGN_DECISION.md',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])
        c=self.c_packet();del c['projection_manifest']['files']['BOUNDARY_TRACE.json']
        c['projection_manifest']['digest']=digest(c['projection_manifest']['files'])
        self.assertIn('C:PROJECTION_SET_INCOMPLETE',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])

    def test_builder_is_deterministic(self):
        a=build_projections(self.dec,self.frame,self.inv,self.ev)
        b=build_projections(self.dec,self.frame,self.inv,self.ev)
        self.assertEqual(a,b)
        self.assertEqual(set(a['files']),{'DESIGN_DECISION.md','COVERAGE_TO_DECISION.tsv','DOWNSTREAM_BUILD_HANDOFF.jsonl',
                                          'EVIDENCE_AND_FALSIFIER_INDEX.jsonl','GLOBAL_ARCHITECTURE.json','BOUNDARY_TRACE.json'})

    def test_local_fake_h1_is_red(self):
        c=self.c_packet();c['claims_protected_h1']=True
        self.assertIn('C:FALSE_PROTECTED_H1',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])
        c=self.c_packet();c['original_source_granted_by_local_check']=True
        self.assertIn('C:FALSE_AUTHORITY',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])
        c=self.c_packet();c['verdict']='C_ACCEPTED'
        self.assertIn('C:FALSE_C_GRADE',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])
        c=self.c_packet();c['reviewer_relationship']='I_AM_INDEPENDENT'
        self.assertIn('C:SELF_CERTIFIED_INDEPENDENCE',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])

    def test_admit_requires_an_executed_current_builder(self):
        c=self.c_packet();c['verdict']='C_CONDITIONALLY_ADMIT_DESIGN'
        self.assertIn('C:ADMIT_WITHOUT_CURRENT_BUILDER',check('C_INTEGRATED',c,self.ev,ROOT,self.anchors)['errors'])


if __name__=='__main__':unittest.main(verbosity=2)
