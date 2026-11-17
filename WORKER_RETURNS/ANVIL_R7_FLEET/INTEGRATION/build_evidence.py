#!/usr/bin/env python3
"""Build the authored local acceptance fixture for the repaired instrument.

This is a TEST INPUT, not a real architecture decision, not source science,
not an independent C packet and not protected H1.  It exercises the exact
positive path of the corrected gate and builder.
"""
import json, pathlib, sys, hashlib
ROOT=pathlib.Path(__file__).resolve().parent
PKG=ROOT/'REPAIRED_PACKAGE'/'ANVIL_R7'
EV=ROOT/'EVIDENCE'; SRC=EV/'SOURCE_118'
sys.path.insert(0,str(PKG/'tools'))
from r7_inventory import build_inventory
from r7_integrated import digest, sha, DOMAINS, REQUIREMENT_ROSTER, REQUIREMENT_DOMAIN

def put(name,obj):
    b=(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode()
    (EV/name).write_bytes(b)
    return {'path':name,'sha256':sha(b)}

inv=build_inventory(SRC,SRC/'PIN_MANIFEST.json',PKG)
inv_ptr=put('SOURCE_IDENTITY_INVENTORY.json',inv)
bc=json.loads((SRC/'02_BOUNDARY_CONTRACTS.json').read_text())
bc_ptr=put('BOUNDARY_CONTRACTS.json',bc)
release=put('RELEASE_REGISTER.json',{'schema':'ANVIL_R7_SOURCE_RELEASE_REGISTER',
   'current':[{'sha256':'526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332','status':'CURRENT_ORIGINAL_SUPPLIED_ZIP'}],
   'revoked':[],
   'note':'Original supplied ZIP is current for source authentication. Individual Git source cuts are pinned separately; no source right is granted.'})
sfmap={sf['path']:sf for sf in inv['source_files']}
def ex_around(path,needle,width=80):
    t=path.read_text(); i=t.index(needle); return t[i:i+width]

def anchor(ref,sf):
    if sf.get('kind')=='GIT':ref.update(commit=sf['commit'],git_path=sf['git_path'],git_blob=sf['git_blob'])
    else:ref.update(zip_sha256=sf['zip_sha256'],zip_member=sf['zip_member'])
    return ref
ref={'path':'22_R6_VALUE_AND_FUNCTION_CONSERVATION.md','sha256':sha((SRC/'22_R6_VALUE_AND_FUNCTION_CONSERVATION.md').read_bytes()),'exact_excerpt':'Historical pre-FORGE 29/26/14, 118 mixed identity and five-test law','zip_sha256':'526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332','zip_member':'ANVIL_R7/22_R6_VALUE_AND_FUNCTION_CONSERVATION.md'}
reqs=[]
for rid in REQUIREMENT_ROSTER:
    d=REQUIREMENT_DOMAIN[rid]
    reqs.append({'id':rid,'domain':d,'binding':'FUTURE_NONPRECLUSION' if d in ('SEAM_WORLD_ACTOR','FIELD_FORGE') else 'PRESENT_HARD',
      'substantive_requirement':f'{rid}: preserve the exact {d} source meaning, negative, authority and first-consumer boundary with no invented science',
      'why_needed':'This obligation is indispensable to the real first consumer and to honest no-loss accounting regardless of the selected physical algorithm',
      'loss_if_missing':'Without it a physically convenient source layout could erase a native distinction, denominator, negative, owner hold or downstream boundary',
      'first_consumer':'Current sourcefree saved C11 native I03/I05 computation or the named future owner where science authority is not issued',
      'architectural_consequence':'Carry an independently inspectable typed representation of the distinction and refuse silent collapse or promotion',
      'proof_or_owner_hold':'Check exact source bytes and the selected positive/refusal/restore witness, or preserve an exact named owner hold',
      'authority_owner':'Competent source/science/engineering owner where the binding is EXTERNAL_OWNER_HELD',
      'evidence':ref})
frame={'schema':'ANVIL_R7_INTEGRATED','stage':'COMMON_FRAME',
  'workflow':'ONE_INTEGRATED_INVESTIGATION_OPTIONAL_TARGETED_DUELS','phase':'BEFORE_ARCHITECTURE_SELECTION',
  'architecture_selected':False,'mandatory_rival_architecture':False,'duel_required':False,
  'A_B_method':'OPTIONAL_SAME_QUESTION_SAME_EVIDENCE','scope':'C11_QUERY_DESIGN',
  'source_cut':'7fc00289dd801d2d0a8ce159986c7595fc27a4d9','protected_head':'31291d08179890852246c8742700e055168e9933',
  'user_priority_source':'Pinned user instruction: complete empirical system, exact source custody, lowest lawful executable cost',
  'first_real_consumer':'Authorized generic sourcefree saved C11 native I03 and I05 operations',
  'currentness_gap_or_exact_verified_state':'Protected PRE-MAIN rechecked at 31291d08179890852246c8742700e055168e9933; live owner rights and native execution remain external',
  'science_authority_boundary':'Field Forge, world and actor science cannot be issued by a physical architecture author',
  'whole_program_mission':'Complete original function continuity and C11 empirical computation into later scientifically lawful world and person products',
  'source_grades_authentic_by_local_test':False,'requirements':reqs,'source_inventory':inv_ptr,
  'release_register':release,'boundary_contract':bc_ptr,
  'boundary_contracts':[{'id':b['id'],'producer':b['producers'],'receiver':b['receivers'],'must_preserve':b['must_preserve'],
      'expected_first_effect':b['first_effect'],'veto':b['veto'],'time_class':b['time_class'],'owner':b['owners']} for b in bc['boundaries']]}
frame_ptr=put('FRAME.json',frame)
nodes=[
 {'id':'N_SRC','producer':'Original source decoder and release custodian','producer_authority':'PYAT S01 source owner','input_types':['external_source'],'output_types':['raw_source'],'time_mode':'OBSERVED','first_consumer':'N_C11','decision_id':'D1','alternative_id':'A1'},
 {'id':'N_C11','producer':'Sealed thirteen-family C11 writer','producer_authority':'S2-C/S1-E physical owner','input_types':['raw_source'],'output_types':['canonical_event'],'time_mode':'OBSERVED','first_consumer':'N_CALC','decision_id':'D1','alternative_id':'A1'},
 {'id':'N_CALC','producer':'Native I03/I05/F1-F4 computation','producer_authority':'PYAT empirical computation owner','input_types':['canonical_event'],'output_types':['empirical_configuration'],'time_mode':'OBSERVED','first_consumer':'N_FIELD','decision_id':'D1','alternative_id':'A1'},
 {'id':'N_FIELD','producer':'FF01 descriptive field reader','producer_authority':'PYAT Field Forge #1009 owner','input_types':['empirical_configuration'],'output_types':['field_configuration'],'time_mode':'MODELED','first_consumer':'N_WORLD','decision_id':'D1','alternative_id':'A1'},
 {'id':'N_WORLD','producer':'N9/N10W selected world','producer_authority':'PYAT N9/N10W science owner (HELD)','input_types':['field_configuration','performed_event'],'output_types':['world_possibility','world_possible_event'],'time_mode':'FICTIONAL','first_consumer':'N_ACTOR','decision_id':'D1','alternative_id':'A1'},
 {'id':'N_ACTOR','producer':'SOROK continuing actor','producer_authority':'SOROK actor/consent owner (HELD)','input_types':['world_possibility','world_possible_event'],'output_types':['actor_state','performed_event'],'time_mode':'FICTIONAL','first_consumer':'N_WORLD','decision_id':'D1','alternative_id':'A1'}]
edges=[
 {'id':'E1','from':'N_SRC','to':'N_C11','data_type':'raw_source','authority_grade':'DOCUMENTARY','temporal_mode':'OBSERVED','negative_or_refusal':'wrong edition or denied source refuses','invalidation_rule':'source hash or release revocation','boundary':'T1'},
 {'id':'E2','from':'N_C11','to':'N_CALC','data_type':'canonical_event','authority_grade':'DOCUMENTARY','temporal_mode':'OBSERVED','negative_or_refusal':'false same-person join or wrong denominator refuses','invalidation_rule':'C11 member or CURRENT revocation','boundary':'T2'},
 {'id':'E3','from':'N_CALC','to':'N_FIELD','data_type':'empirical_configuration','authority_grade':'DOCUMENTARY','temporal_mode':'OBSERVED','negative_or_refusal':'marginal-only substitute refuses','invalidation_rule':'source or estimand incompatibility','boundary':'T3'},
 {'id':'E4','from':'N_FIELD','to':'N_WORLD','data_type':'field_configuration','authority_grade':'DOCUMENTARY','temporal_mode':'MIXED_TYPED','negative_or_refusal':'survey opinion treated as institutional power refuses','invalidation_rule':'structural source revocation','boundary':'T4'},
 {'id':'E5','from':'N_WORLD','to':'N_ACTOR','data_type':'world_possibility','authority_grade':'DOCUMENTARY','temporal_mode':'FICTIONAL','negative_or_refusal':'respondent-to-character identity collapse refuses','invalidation_rule':'world branch invalidation','boundary':'T5'},
 {'id':'E6','from':'N_WORLD','to':'N_ACTOR','data_type':'world_possible_event','authority_grade':'DOCUMENTARY','temporal_mode':'FICTIONAL','negative_or_refusal':'no actor access yields no knowledge','invalidation_rule':'actor/world permission revocation','boundary':'T6'},
 {'id':'E7','from':'N_ACTOR','to':'N_WORLD','data_type':'performed_event','authority_grade':'DOCUMENTARY','temporal_mode':'FICTIONAL','negative_or_refusal':'fictional act cannot edit observed C11','invalidation_rule':'branch replay or committed past invalidation','boundary':'T7'}]
graph={'nodes':nodes,'edges':edges}
disp=[]
for e in inv['entries']:
    g=e['group']
    if g=='K1_CAP': st='PRESENT_PRESERVED';sa='HISTORICAL_FUNCTION_RETAINED'
    elif g in ('PYAT_PC','P4R'): st='RETAINED_HISTORICAL_NONADOPTED';sa='NOT_ADOPTED' if g=='PYAT_PC' else 'HELD'
    else: st='FUTURE_NONPRECLUDED';sa='INCLUDED_NOT_ADOPTED'
    ev={'path':e['source_file'],'sha256':sha((SRC/e['source_file']).read_bytes()),'exact_excerpt':e['source_excerpt']}
    if g=='BOUNDARY':
        ev['exact_excerpt']=ex_around(SRC/e['source_file'],'"id":"'+e['id']+'"')
    elif g=='TERMINAL':
        ev['exact_excerpt']=ex_around(SRC/e['source_file'],'"'+e['id']+'"')
    anchor(ev,sfmap[e['source_file']])
    disp.append({'identity_id':e['id'],'disposition':st,'status_assertion':sa,'evidence_grade':'DOCUMENTARY',
      'design_effect':'Candidate preserves the exact identity meaning, negative, owner boundary and no-adoption status without promoting it to issued science',
      'first_consumer_path':'Traced from the source identity to the typed whole-machine node and first consumer or explicit competent owner hold',
      'conservation_or_refusal_witness':'The identity origin hash, exact source excerpt and negative/refusal semantics are retained and rechecked by the gate',
      'origin_sha256':e['origin_sha256'],'adopted_by_this_decision':False,'closed_by_this_decision':False,'evidence':ev})
decision={'schema':'ANVIL_R7_INTEGRATED','stage':'INTEGRATED_DECISION','common_frame':frame_ptr,'frame_sha256':digest(frame),
  'decision_process':'ONE_SYNTHESIS_NO_MANDATORY_RIVAL','basis':'ANALYTICAL_SOURCE_GROUNDED','grade':'AUTHOR_PROPOSED_PENDING_C',
  'architecture_description':'A prepared integrated instrument candidate that preserves source identity, C11 authority and typed downstream boundaries without selecting a production backend',
  'entire_source_to_actor_dataflow':'From authenticated source through sealed C11 and native empirical computation into separately owned field, world and actor readers; no empirical or fictional fact is promoted across a boundary without its owner',
  'algorithm_and_data_structures':'One verified identity ledger, one candidate disposition table, one typed producer/authority/time/consumer graph and deterministic projections; no duplicate authority store',
  'resource_cost_reasoning':'Minimize repeated reconstruction and preserve the six-gibibyte aggregate ceiling; native 100k dense 1/10/100 economics remain NOT_RUN until lawful execution',
  'historical_function_conservation':'Conserve all 118 mixed identities with exact source excerpts, negatives, first consumers and truthful nonadoption of prospective or held science',
  'scientific_boundary_and_nonpreclusion':'Observational survey relationships cannot become structural causes, fictional world facts or actor experiences without separate competent science and actual contact',
  'strongest_surviving_objection':'The current body-json layout may impose first-query cost that an authenticated selective reader cannot avoid without an alternative index',
  'why_selected_over_feasible_alternatives':'Uses accepted semantic and physical assets and introduces less compatibility and authority risk than a wholesale replacement',
  'next_actual_engineering_operation':'Publish and independently receive the prepared saved-session correction, then execute one sourcefree lawful first-reader path without claiming native or H1 authority',
  'single_selected_strategy':'Verified C11 with a prepared analytical execution layer (authored instrument fixture only)',
  'first_real_consumer':'Authorized generic sourcefree saved C11 native I03 and I05 operations',
  'alternatives_considered':[{'technical_approach':'Wholesale independent SQL-backed physical replacement','state':'VIABLE_NOT_SELECTED','why_not_selected_or_held':'It would reopen canonical replay and source authentication without evidence that it resolves repeated-evaluation costs'}],
  'choice_reversers':[{'status':'RESOLVED_AT_ANALYTICAL_SCOPE','question':'Can qualified population preparation be reused without changing source truth?'}],
  'requires_full_A_B_comparison':False,'competing_implementations_mandatory':False,'architecture_claims_independent_acceptance':False,
  'targeted_duel':None,'whole_machine_graph':graph,
  'boundary_contract_map':{t:{'name':n} for t,n in zip(('T1','T2','T3','T4','T5','T6','T7'),('source to canonical','canonical to computation','computation to field','field to world','world to encounter','encounter to actor','performed to next situation'))},
  'builder_handoff':{'first_reader_abi':'ANVIL_R7_FIRST_READER_ABI@1','input':'verified frame + source inventory','output':'six deterministic projections','negative':'refuse if any identity origin or boundary evidence mismatches','restore':'byte-identical rebuild','consumer':'distinct C then competent H1'},
  'h1_received_by_local_check':False,'protected_received_by_local_check':False,
  'actor_world_boundary':{'survey_implies_actor_knowledge':False,'fictional_mutates_source':False,'source_implies_material_power':False,'actor_private_state_from_source':False},
  'identity_dispositions':disp,
  'requirement_dispositions':[{'requirement_id':r['id'],'disposition':'FUTURE_NONPRECLUDED' if r['binding']=='FUTURE_NONPRECLUSION' else 'PRESENT_PRESERVED',
      'evidence_grade':'DOCUMENTARY','actual_design_effect':'Keep the documented capacity and typed consumer boundary with explicit negative and restoration semantics',
      'specific_first_consumer_path':'Native saved I03 facts can feed qualified conditional and possibility interfaces under source authority',
      'conservation_or_refusal_witness':'The frozen source contracts specify denial and restoration behavior, not an actual native execution','evidence':ref} for r in reqs]}
dec_ptr=put('DECISION.json',decision)
c={'schema':'ANVIL_R7_INTEGRATED','stage':'INDEPENDENT_C','integrated_decision':dec_ptr,'integrated_decision_sha256':digest(decision),
  'first_consumer':frame['first_real_consumer'],
  'independent_reverse_walk_of_whole_frame':'The reviewer separately traces source through C11, I03, FF and world/actor evidence including negative cases and exact owner holds',
  'strongest_choice_reversing_objection':'The installed event index may not support conditioned joint analysis economically at survey width',
  'scientific_and_owner_boundary':'No source scientific rights or actor-level structural causality can be issued from a documentary assessment',
  'actual_first_consumer_assessment':'This authored fixture does not run a real native first consumer and cannot justify adoption of original survey science',
  'historical_no_loss_assessment':'The complete historical inventory remains frozen with no recovered function automatically declared issued',
  'reviewer_relationship':'DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION','choice_reversing_objection_survives':False,'verdict':'C_HOLD_EXACT',
  'boundary_court':{t:{'positive':'A valid source-consistent input produces the specified typed output at the boundary',
      'negative':'A mutated, revoked or absent input is refused at the actual boundary consumer without cached positive',
      'restore':'Exact authorized bytes and permission restore the prior positive output','grade':'SOURCE_STATIC_CONSERVED',
      'first_consumer_or_hold':'Boundary consumer named in the typed graph; owner-held where future science is not issued',
      'evidence':{'path':'02_BOUNDARY_CONTRACTS.json','sha256':sha((SRC/'02_BOUNDARY_CONTRACTS.json').read_bytes()),'exact_excerpt':ex_around(SRC/'02_BOUNDARY_CONTRACTS.json','"id":"'+t+'"'),
                  'zip_sha256':'526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332','zip_member':'ANVIL_R7/02_BOUNDARY_CONTRACTS.json'}} for t in ('T1','T2','T3','T4','T5','T6','T7')},
  'graph_audit':{'producer_authority_time_consumer_checked':True,'holes':[],'boundary_edges_checked':['T1','T2','T3','T4','T5','T6','T7']},
  'builder_handoff_review':'The handoff identifies an exact first-reader ABI, six projections, refusal and restore behavior and a named external C/H1 consumer',
  'actual_first_reader_verified':False,'local_h1_claim':False,'protected_received_locally':False,'h1_grade':'NOT_RECEIVED',
  'builder_cards':[{'id':'present','domain':'CURRENT_FIRST_CONSUMER','grade':'EXACT_BUILDER_HOLD','exact_hold':'Actual native source consumer proof and competent owner execution are not part of this authored local fixture'},
                   {'id':'future','domain':'FUTURE_NONPRECLUSION','grade':'EXACT_BUILDER_HOLD','exact_hold':'Future actor/world source governance remains independent and cannot be invented by this local fixture'}],
  'original_source_granted_by_local_check':False,'owner_granted_by_local_check':False}
c_ptr=put('C.json',c)
print(json.dumps({'status':'AUTHORED_FIXTURE_BUILT','frame':frame_ptr,'decision':dec_ptr,'c':c_ptr,'inventory_total':inv['total']},indent=2))
