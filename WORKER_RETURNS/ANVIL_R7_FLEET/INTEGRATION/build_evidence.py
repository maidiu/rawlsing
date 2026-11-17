#!/usr/bin/env python3
"""Rebuild the authored local packet from the preserved source inventory and the
frozen D2A/D2B source-specific material.  This is a TEST INPUT, not architecture,
not native science, not independent C and not H1."""
import csv, json, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parent
PKG=ROOT/'REPAIRED_PACKAGE'/'ANVIL_R7'
EV=ROOT/'EVIDENCE'; SRC=EV/'SOURCE_118'
D2A=pathlib.Path('/Users/matthewsmith/Desktop/ANVIL_RABOCHII_EXECUTION_20261117/D2A/D2A_ANVIL_RETURN_R2')
sys.path.insert(0,str(PKG/'tools'))
from r7_inventory import build_inventory
from r7_integrated import digest, sha, REQUIREMENT_ROSTER, REQUIREMENT_DOMAIN, REQUIREMENT_SEMANTICS, TERMINAL_IDS
from r7_contract import REQUIREMENT_MACHINE, IDENTITY_MACHINE, BOUNDARY_MACHINE
def nh(obj,fields): return sha(json.dumps({k:obj.get(k,'') for k in fields},sort_keys=True,ensure_ascii=False).encode())

def put(name,obj):
    b=(json.dumps(obj,sort_keys=True,ensure_ascii=False,indent=2)+'\n').encode();(EV/name).write_bytes(b)
    return {'path':name,'sha256':sha(b)}
def ex_around(path,needle,width=90):
    t=path.read_text();i=t.index(needle);return t[i:i+width]
def anchor(ref,sf):
    if sf.get('kind')=='GIT':ref.update(commit=sf['commit'],git_path=sf['git_path'],git_blob=sf['git_blob'])
    else:ref.update(zip_sha256=sf['zip_sha256'],zip_member=sf['zip_member'])
    return ref

# Rebuild the exact source-authenticated inventory, then add the source-reported
# negative and exact-row fields separately from authored interpretation.
inv=build_inventory(SRC,SRC/'PIN_MANIFEST.json',PKG)
cross={x['source_id']:x for x in csv.DictReader((D2A/'118_TO_REQUIREMENT_OBLIGATION_CROSSWALK.tsv').open(),delimiter='\t')}
for e in inv['entries']:
    x=cross[e['id']]
    e['source_reported_negative_or_correction']=x.get('source_reported_negative_or_correction','')
    e['original_row_excerpt']=e.get('source_excerpt','')
    e['authored_source_meaning']=x.get('source_meaning','')
    e['authored_essential_negative']=x.get('essential_negative','')
    e['semantic_interpretation_grade']='AUTHORED_SOURCE_BOUNDED_PENDING_C'
    e['source_meaning_sha256']=sha((e.get('source_semantics') or '').encode())
inv_ptr=put('SOURCE_IDENTITY_INVENTORY.json',inv)
bc=json.loads((SRC/'02_BOUNDARY_CONTRACTS.json').read_text());bc_ptr=put('BOUNDARY_CONTRACTS.json',bc)
release=put('RELEASE_REGISTER.json',{'schema':'ANVIL_R7_SOURCE_RELEASE_REGISTER','current':[{'sha256':'526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332','status':'CURRENT_ORIGINAL_SUPPLIED_ZIP'}],'revoked':[],'note':'Original supplied ZIP is current for source authentication; no source right granted.'})
sfmap={sf['path']:sf for sf in inv['source_files']}
ref={'path':'22_R6_VALUE_AND_FUNCTION_CONSERVATION.md','sha256':sha((SRC/'22_R6_VALUE_AND_FUNCTION_CONSERVATION.md').read_bytes()),'exact_excerpt':'Historical pre-FORGE 29/26/14, 118 mixed identity and five-test law','zip_sha256':'526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332','zip_member':'ANVIL_R7/22_R6_VALUE_AND_FUNCTION_CONSERVATION.md'}

# Specific requirements; each contains the frozen required distinction and a
# falsifiable positive/negative probe.  No one-sentence generic row.
REQ_TEXT={
'REQ-SOURCE-SEMANTICS':('Native question, option, code, form, translation, routing, eligibility and missing status survive before normalization; source stratum cannot imply respondent sect or ancestry.','A changed native option or routing rule changes the cold typed event; a denied field refuses.','A sample stratum is substituted for a respondent-level sect variable and must refuse.'),
'REQ-C11-PERSISTENCE':('C11 body and locator parity, exact member projection, CURRENT release and cold restore are explicit; a body hash alone is not source truth.','A cold reopen of the exact release returns the same typed member; a changed body refuses.','A wrong member with a matching body hash is refused by locator/CURRENT comparison.'),
'REQ-CURRENT-I03-I05':('Current I03 and I05 first-reader paths are named; sourcefree execution is not source-native execution.','A sourcefree I03/I05 positive is labeled sourcefree and does not grant native proof.','A sourcefree result is relabeled source-native and must refuse.'),
'REQ-HISTORICAL-DDM':('V549 branch conditioning, V550 weighted/unweighted semantics, V550J prepared same-person substrate and F26 reuse possibility survive; old Postgres carrier and old bugs do not.','A true same-person joint and prepared-substrate replay change the typed output.','A pairwise product or stale prepared cache is accepted as V550J equivalence and must refuse.'),
'REQ-F1-F4':('F1-F4 preserve same-person k>=3 joint membership, branch/risk sets, weighted/unweighted denominators and both conditional directions.','Two equal-marginal cohorts with different three-way joint produce different F4 output.','A pairwise-marginal substitute for k>=3 is accepted as F4 and must refuse.'),
'REQ-FIELD-FORGE':('FF01 descriptive association is separate from FF02 structural/material ownership; neither is a survey-opinion relabel.','Holding survey answers fixed while changing an independently authenticated structural right changes only the qualified FF02/world object.','Survey opinion frequency is called institutional power and must refuse.'),
'REQ-SEAM-WORLD-ACTOR':('A differentiated Other, actual encounter, actor access and SOROK-owned later action are separate; no offscreen learning or automatic adoption.','Changing only the D2 other distribution may change a potential Other candidate but not the focal actor history.','A survey answer gives the actor private knowledge without encounter and must refuse.'),
'REQ-AUTHORITY-RECOVERY':('I02 source relation, trust root, invalidation, revocation of a revoked release and cold restore are independent of producer self-consistency.','A consistent wrong projection fails an independent source comparison; revoked release refuses.','Producer and verifier sharing the same wrong hash are accepted as source truth and must refuse.'),
'REQ-RESOURCE-ECONOMICS':('Real dense 100k width, process-tree 6 GiB, distinct 1/10/100 operations, scratch/disk/output cost remain NOT_RUN until lawful execution.','A lawful dense run measures phase cost and process-tree RSS on a representative fixture.','A synthetic green benchmark or 3.245 events/respondent run is called representative and must refuse.'),
'REQ-MULTIWAY-JOINT':('The true three-way same-person joint must be preserved; pairwise marginals are not a lawful replacement for k>=3 respondent structure.','Even/odd parity witnesses with identical marginals produce different P(111).','Pairwise marginals are sufficient and no three-way joint need be preserved; this must refuse.'),
'REQ-DENOMINATOR-MISSING-ROUTING':('Forward and reverse conditionals use distinct eligible denominators; missing, not-asked, refused, inapplicable and routing-unknown are typed and not zero.','A forward/reverse pair reports different eligible bases and a NOT_ASKED case refuses a false zero.','One denominator is reused for both directions and must refuse.'),
'REQ-PHYSICAL-WORKLOAD-1-10-100':('Dense 600-1,300-slot 100k, process-tree 6 GiB and distinct 1/10/100 cold operations are required evidence, not a sourcefree small example.','A representative wide cold run measures distinct phases and process-tree RSS.','A 3.245-events/respondent sourcefree example is representative and must refuse.'),
'REQ-SOURCE-I02-REVOCATION':('Independent source comparison, revocation of a revoked release and cold refusal of prepared facts are required; a shared wrong hash is not proof.','Exact authorized source restores; a revoked member refuses even after preparation.','Producer/verifier share a wrong hash and are accepted as proof; this must refuse.'),
'REQ-FF01-FF02-WORLD-ACTOR-FIREWALL':('Survey, actor and fictional-world claims are firewalled: survey opinion cannot be institutional power, actor private knowledge or a fictional edit of observed source.','Holding observed answers fixed, an independently admitted world/event may change a qualified possibility.','Survey opinion is institutional power or survey answers give actor knowledge without encounter; this must refuse.'),
'REQ-TERMINAL-F5-F8-N11-N12':('F5 learned product, F8 positioned world, N11 acceptance and N12 wake remain explicit typed readers or exact holds; T1-T7 are boundary interrogations, not a serial runtime.','Each terminal has a producer/authority/time/first reader or exact owner hold.','A terminal is silently dropped or T1-T7 is made a serial pipeline; this must refuse.'),
'REQ-HISTORICAL-NOADOPTION-CONSERVATION':('All 118 identities remain distinct; 26 PYAT-PC NOT_ADOPTED and 14 P4R HELD are not promoted; the separate 52/24/21 estate is not added as new requirements.','A missing identity, false adoption or false proof closure refuses.','All 26 are adopted or all 14 closed and must refuse.'),
}
reqs=[]
for rid in REQUIREMENT_ROSTER:
    d=REQUIREMENT_DOMAIN[rid]; sub,pos,neg=REQ_TEXT[rid]; spec=REQUIREMENT_SEMANTICS[rid]
    reqs.append({'id':rid,'domain':d,'binding':'FUTURE_NONPRECLUSION' if d in ('SEAM_WORLD_ACTOR','FIELD_FORGE') else 'PRESENT_HARD',
      'typed_obligation':spec['typed_obligation'],'machine_assertion':REQUIREMENT_MACHINE[rid],'substantive_requirement':sub,'positive_probe':pos,'negative_probe':neg,
      'why_needed':'This source-court distinction is choice-changing; losing it would let a coherent fixture certify a false preservation.',
      'loss_if_missing':'The named positive/negative distinction would disappear while IDs, headings and hashes remain valid.',
      'first_consumer':'Named typed graph reader or exact competent owner hold; no universal truth service is implied.',
      'architectural_consequence':'Carry the typed distinction and a refusal/restore test; do not replace the source semantics with a convenience label.',
      'proof_or_owner_hold':'Execute the named probe at its honest grade or preserve the exact external C/source-owner hold.',
      'authority_owner':'Competent source/science/engineering owner where the binding is EXTERNAL_OWNER_HELD','evidence':ref})
for r in reqs: r['narrative_sha256']=nh(r,('substantive_requirement','why_needed','loss_if_missing','first_consumer','architectural_consequence','proof_or_owner_hold','positive_probe','negative_probe'))
frame={'schema':'ANVIL_R7_INTEGRATED','stage':'COMMON_FRAME','workflow':'ONE_INTEGRATED_INVESTIGATION_OPTIONAL_TARGETED_DUELS','phase':'BEFORE_ARCHITECTURE_SELECTION','architecture_selected':False,'mandatory_rival_architecture':False,'duel_required':False,'A_B_method':'OPTIONAL_SAME_QUESTION_SAME_EVIDENCE','scope':'C11_QUERY_DESIGN','source_cut':'7fc00289dd801d2d0a8ce159986c7595fc27a4d9','protected_head':'31291d08179890852246c8742700e055168e9933','user_priority_source':'Pinned user instruction: complete empirical system, exact source custody, lowest lawful executable cost','first_real_consumer':'Authorized generic sourcefree saved C11 native I03 and I05 operations','currentness_gap_or_exact_verified_state':'Protected PRE-MAIN rechecked at 31291d08179890852246c8742700e055168e9933; live owner rights and native execution remain external','science_authority_boundary':'Field Forge, world and actor science cannot be issued by a physical architecture author','whole_program_mission':'Complete original function continuity and C11 empirical computation into later scientifically lawful world and person products','source_grades_authentic_by_local_test':False,'requirements':reqs,'source_inventory':inv_ptr,'release_register':release,'boundary_contract':bc_ptr,'boundary_contracts':[{'id':b['id'],'producer':b['producers'],'receiver':b['receivers'],'must_preserve':b['must_preserve'],'expected_first_effect':b['first_effect'],'veto':b['veto'],'time_class':b['time_class'],'owner':b['owners']} for b in bc['boundaries']]}
frame_ptr=put('FRAME.json',frame)

# Transform the frozen D2A 43-node/58-edge source->terminal graph into the active
# typed schema.  All 16 terminal identities are explicit nodes; held terminals
# carry exact holds rather than invented readers.
gd=json.loads((D2A/'SOURCE_TO_TERMINAL_BOUNDARY_GRAPH.json').read_text())
idmap={'F5':'F5_LEARNED','F8':'F8_POSITIONED','N11':'N11_ACCEPTANCE','N12':'N12_WAKE','PRE-V3':'PREV3','SEAM':'SEAM_HANDOFF','SOROK':'SOROK_CONTINUITY'}
rev={v:k for k,v in idmap.items()}
TERMINAL_NODE_IDS={idmap.get(t,t) for t in TERMINAL_IDS}
HELD={'F5_LEARNED','F8_POSITIONED','N11_ACCEPTANCE','N12_WAKE','SEAM_HANDOFF','SOROK_CONTINUITY'}
def node_time(nid):
    if nid in ('ACTOR_ACCESS','ACQUIRED','ACT','NEXT_STATE','E001','SOROK_CONTINUITY','N12_WAKE'):return 'FICTIONAL'
    if nid in ('FF01','MATERIAL_SOURCE','FF02','N9','N10E','N10W','OTHER_CANDIDATE','OTHER_INSTANTIATED','ENCOUNTER','PREV3','SEAM_HANDOFF'):return 'MODELED'
    if nid.startswith('K1') or nid.startswith('P4R'):return 'HISTORICAL_AS_OF'
    return 'OBSERVED'
nodes=[];out_types={};in_types={}
for n in gd['nodes']:
    nid=n['id'];out_types.setdefault(nid,[]);in_types.setdefault(nid,[])
for e in gd['edges']:
    out_types.setdefault(e['from'],[]).append(e['data_type']);in_types.setdefault(e['to'],[]).append(e['data_type'])
for n in gd['nodes']:
    nid=n['id'];held=nid in HELD
    nodes.append({'id':nid,'producer':f"{n.get('kind','typed node')} producer/owner",'producer_authority':n.get('owner','COMPETENT_OWNER_HELD'),
      'input_types':sorted(set(in_types.get(nid,[]))) or ['typed_input'],'output_types':sorted(set(out_types.get(nid,[]))) or ['typed_output'],
      'time_mode':node_time(nid),'first_consumer':'EXACT_HOLD' if held else 'NAMED_TYPED_CONSUMER_OR_OWNER_HOLD',
      'exact_hold':('Exact owner/science hold for '+rev.get(nid,nid)+': no current actual first reader is asserted') if held else '',
      'decision_id':'D1','alternative_id':'A1','kind':n.get('kind',''),'owner':n.get('owner',''),'evidence_grade':n.get('evidence_grade','')})
def boundary(e):
    for r in e.get('source_identity_refs',[]):
        if r in ('T1','T2','T3','T4','T5','T6','T7'):return r
    f,t=e['from'],e['to']
    if t=='S01_PROJECT':return 'T1'
    if t in ('C11_ESTATE','C11_ROOT','I02_PROOF'):return 'T2'
    if t in ('COLD_READ','QUERY_ISSUER','I03','I05','BATCH','F1','F2','F3','F4','DIAGNOSTICS','F6','F7'):return 'T3'
    if t in ('FF01','MATERIAL_SOURCE','FF02','PREV3'):return 'T4'
    if t in ('N10E','N9','N10W','OTHER_CANDIDATE'):return 'T5'
    if t in ('OTHER_INSTANTIATED','ENCOUNTER','ACTOR_ACCESS','ACQUIRED','ACT'):return 'T6'
    return 'T7'
edges=[]
for e in gd['edges']:
    tm='FICTIONAL' if e['from'] in ('ACTOR_ACCESS','ACQUIRED','ACT','OTHER_INSTANTIATED','ENCOUNTER','SOROK_CONTINUITY') or e['to'] in ('NEXT_STATE','WORLD_EFFECT','E001','SOROK_CONTINUITY') else ('HISTORICAL_AS_OF' if e.get('time_basis') in ('SURVEY_WAVE','INSTRUMENT_VERSION') else ('MODELED' if e['from'] in ('FF01','MATERIAL_SOURCE','FF02','N9','N10E','N10W') else 'MIXED_TYPED'))
    edges.append({'id':e['id'],'from':e['from'],'to':e['to'],'data_type':e['data_type'],'authority_grade':e.get('grade','PROPOSED_EDGE_NOT_EXECUTED'),
      'temporal_mode':tm,'negative_or_refusal':e.get('negative_or_severance','refuses missing authority or source'),
      'invalidation_rule':e.get('severance_instrument') or e.get('restoration') or 'source/owner invalidation refuses',
      'boundary':boundary(e),'edge_kind':e.get('edge_kind',''),'scope':e.get('scope',''),'positive_claim_to_test':e.get('positive_claim_to_test',''),
      'restoration':e.get('restoration',''),'claim_grade':e.get('claim_grade',''),'first_consumer_status':e.get('first_consumer_status',''),
      'source_identity_refs':e.get('source_identity_refs',[])})
rename={'F5_LEARNED':'F5','F8_POSITIONED':'F8','N11_ACCEPTANCE':'N11','N12_WAKE':'N12','PREV3':'PRE-V3','SEAM_HANDOFF':'SEAM','SOROK_CONTINUITY':'SOROK'}
for n in nodes:n['id']=rename.get(n['id'],n['id'])
for e in edges:
    e['from']=rename.get(e['from'],e['from']);e['to']=rename.get(e['to'],e['to'])
# terminal fates and required incident edges are explicit, not count padding
incident={}
for e in edges:
    incident.setdefault(e['from'],[]).append(e['id']);incident.setdefault(e['to'],[]).append(e['id'])
outgoing={}
for e in edges: outgoing.setdefault(e['from'],[]).append(e['to'])
for n in nodes:
    if n['id'] in TERMINAL_IDS:
        n['terminal_fate']='EXACT_HOLD'
        n['exact_hold']='Exact owner/science hold for '+n['id']+': no current actual first reader is asserted; source-required dependencies are explicit'
        n['competent_owner']=n.get('owner','COMPETENT_OWNER_HELD')
        n['negative_or_refusal']='missing/unauthorized/absent source-required dependency refuses'
        n['restore']='exact owner/source and release restore the prior qualified state'
        n['required_edges']=sorted(set(incident.get(n['id'],[])))
        n['first_consumer']='EXACT_HOLD'
    elif n.get('first_consumer')=='NAMED_TYPED_CONSUMER_OR_OWNER_HOLD':
        nxt=(outgoing.get(n['id']) or [None])[0]
        if nxt:n['first_consumer']=nxt
        else:
            n['first_consumer']='EXACT_HOLD';n['exact_hold']='Exact hold for '+n['id']+': no current actual consumer asserted'
graph={'nodes':nodes,'edges':edges,'terminal_node_map':{t:t for t in TERMINAL_IDS},'schema':'ANVIL_WHOLE_MACHINE_TYPED_GRAPH_R2'}

# Per-identity dispositions from D2A source-specific crosswalk.
disp=[]
for e in inv['entries']:
    x=cross[e['id']];g=e['group'];meaning=x.get('source_meaning') or e.get('source_semantics');neg=x.get('essential_negative') or e.get('negative_meaning');consumer=x.get('first_consumer_or_hold') or e.get('consumer_or_hold')
    if e['id']=='K1-CAP-11': meaning=meaning+' Three-way same-person joint must be preserved.'; neg=neg+' a product of lower-order marginals is not a lawful replacement.'
    if g=='K1_CAP':state='PRESENT_PRESERVED';sa='HISTORICAL_FUNCTION_RETAINED';tg='HISTORICAL_FUNCTION_PRESERVED'
    elif g=='PYAT_PC':state='RETAINED_HISTORICAL_NONADOPTED';sa='NOT_ADOPTED';tg='NOT_ADOPTED_PROPOSAL'
    elif g=='P4R':state='EXACT_OWNER_HOLD';sa='HELD';tg='HELD_PROOF_ROUTE'
    elif g=='SEAM_B':state='FUTURE_NONPRECLUDED';sa='INCLUDED_NOT_ADOPTED';tg='BOUNDARY_QUESTION'
    elif g=='SEAM_S':state='FUTURE_NONPRECLUDED';sa='INCLUDED_NOT_ADOPTED';tg='SOCIAL_FIELD_REQUIREMENT'
    elif g=='ANVIL_L':state='FUTURE_NONPRECLUDED';sa='INCLUDED_NOT_ADOPTED';tg='IRREVERSIBLE_LOSS_GUARD'
    elif g=='BOUNDARY':state='FUTURE_NONPRECLUDED';sa='INCLUDED_NOT_ADOPTED';tg='TYPED_BOUNDARY_INTERROGATION'
    elif e['id'] in ('F5','F8','N11','N12','SEAM','SOROK'):state='EXACT_OWNER_HOLD';sa='HELD';tg='TERMINAL_SCOPE_OR_HOLD'
    else:state='FUTURE_NONPRECLUDED';sa='INCLUDED_NOT_ADOPTED';tg='TERMINAL_SCOPE_OR_HOLD'
    ev={'path':e['source_file'],'sha256':sha((SRC/e['source_file']).read_bytes()),'exact_excerpt':e['source_excerpt']}
    if g=='BOUNDARY':ev['exact_excerpt']=ex_around(SRC/e['source_file'],'"id":"'+e['id']+'"')
    elif g=='TERMINAL':ev['exact_excerpt']=ex_around(SRC/e['source_file'],'"'+e['id']+'"')
    anchor(ev,sfmap[e['source_file']])
    disp.append({'identity_id':e['id'],'disposition':state,'status_assertion':sa,'evidence_grade':'DOCUMENTARY','typed_obligation':tg,'machine_assertion':IDENTITY_MACHINE.get(e['id'],{'operation':'IDENTITY_SCOPE','adopted':False,'closed':False}),
      'source_meaning':meaning,'source_negative':neg,'source_meaning_sha256':sha((e.get('source_semantics') or '').encode()),
      'interpretation_grade':'AUTHORED_SOURCE_BOUNDED_PENDING_C','original_row_excerpt':e.get('source_excerpt',''),
      'source_reported_negative_or_correction':x.get('source_reported_negative_or_correction',''),
      'first_consumer_or_hold':consumer,'decision_ids':[z.strip() for z in (x.get('candidate_S1_requirement_ids') or '').split(',') if z.strip()],
      'design_effect':f"Candidate carries '{meaning}' through the typed edge/reader '{consumer}' and refuses the stated negative without promoting a historical name",
      'first_consumer_path':consumer+' (source-bound first consumer or exact owner hold)','conservation_or_refusal_witness':f"Positive: source-bound {e['id']} effect at {consumer}; negative: {neg}; restore: exact owner/source bytes and hold",
      'origin_sha256':e['origin_sha256'],'adopted_by_this_decision':False,'closed_by_this_decision':False,'evidence':ev})
for x in disp: x['narrative_sha256']=nh(x,('source_meaning','source_negative','design_effect','first_consumer_path','conservation_or_refusal_witness','disposition','status_assertion','evidence_grade','first_consumer_or_hold'))
decision={'schema':'ANVIL_R7_INTEGRATED','stage':'INTEGRATED_DECISION','common_frame':frame_ptr,'frame_sha256':digest(frame),'decision_process':'ONE_SYNTHESIS_NO_MANDATORY_RIVAL','basis':'ANALYTICAL_SOURCE_GROUNDED','grade':'AUTHOR_PROPOSED_PENDING_C',
 'architecture_description':'A prepared integrated instrument candidate that preserves source identity, C11 authority, true same-person joints and typed downstream boundaries without selecting a production backend',
 'entire_source_to_actor_dataflow':'From authenticated source through sealed C11 and native empirical computation into separately owned field, world and actor readers; no empirical or fictional fact is promoted across a boundary without its owner',
 'algorithm_and_data_structures':'One verified identity ledger, 118 source-specific dispositions, a 43-node source-to-terminal typed graph and deterministic projections; no duplicate authority store',
 'resource_cost_reasoning':'Minimize repeated reconstruction and preserve the six-gibibyte aggregate ceiling; native 100k dense 1/10/100 economics remain NOT_RUN until lawful execution',
 'historical_function_conservation':'Conserve all 118 mixed identities with exact source excerpts, source-reported negatives and source-specific authored dispositions; 26 remain NOT_ADOPTED and 14 HELD',
 'scientific_boundary_and_nonpreclusion':'Observational survey relationships cannot become structural causes, fictional world facts or actor experiences without separate competent science and actual contact',
 'strongest_surviving_objection':'The current body-json layout may impose first-query cost that an authenticated selective reader cannot avoid without an alternative index',
 'why_selected_over_feasible_alternatives':'Uses accepted semantic and physical assets and introduces less compatibility and authority risk than a wholesale replacement',
 'next_actual_engineering_operation':'Publish and independently receive the prepared saved-session correction, then execute one sourcefree lawful first-reader path without claiming native or H1 authority',
 'single_selected_strategy':'Verified C11 with a prepared analytical execution layer (authored instrument fixture only)','first_real_consumer':'Authorized generic sourcefree saved C11 native I03 and I05 operations',
 'alternatives_considered':[{'technical_approach':'Wholesale independent SQL-backed physical replacement','state':'VIABLE_NOT_SELECTED','why_not_selected_or_held':'It would reopen canonical replay and source authentication without evidence that it resolves repeated-evaluation costs'}],
 'choice_reversers':[{'status':'RESOLVED_AT_ANALYTICAL_SCOPE','question':'Can qualified population preparation be reused without changing source truth?'}],
 'requires_full_A_B_comparison':False,'competing_implementations_mandatory':False,'architecture_claims_independent_acceptance':False,'targeted_duel':None,'whole_machine_graph':graph,
 'boundary_contract_map':{b['id']:{'name':b.get('name',''),'producer':b['producers'],'receiver':b['receivers'],'producers':b['producers'],'receivers':b['receivers'],'must_preserve':b['must_preserve'],'first_effect':b['first_effect'],'veto':b['veto'],'time_class':b['time_class'],'owner':b['owners'],'owners':b['owners'],'source':b.get('source','')} for b in bc['boundaries']},
 'builder_handoff':{'first_reader_abi':'ANVIL_R7_FIRST_READER_ABI@1','input':'verified frame + source inventory + 118 dispositions + 43-node graph','output':'six deterministic projections','negative':'refuse if any identity origin, source meaning binding, terminal node or boundary evidence mismatches','restore':'byte-identical rebuild','consumer':'distinct C then competent H1'},
 'builder_handoffs':[{'id':'CURRENT_FIRST_CONSUMER','producer_symbol':'tools/r7_integrated.py::check_decision','consumer_symbol':'tools/r7_build.py::_artifacts','input_abi':'ANVIL_R7_INTEGRATED frame+decision','output_abi':'ANVIL_R7_FIRST_READER_ABI@1','transformation':'verified packet -> six deterministic projections','negative':'any origin/semantic freeze/graph/boundary mismatch refuses','restore':'exact bytes regenerate identical projections','test_command':'python3 -m unittest test_r7_integrated -q','expected_effect':'local source-byte and topology pass only','authority':'PREPARED_NOT_C','status':'LOCAL_AUTHORED_NOT_EXTERNAL','dependencies':['SOURCE_IDENTITY_INVENTORY','BOUNDARY_CONTRACTS']},
                      {'id':'FUTURE_NONPRECLUSION','producer_symbol':'tools/r7_integrated.py::check_C','consumer_symbol':'future qualified C/H1 owner','input_abi':'C packet + exact terminal holds','output_abi':'C_HOLD_EXACT or C_CONDITIONALLY_ADMIT_DESIGN only with external custody','transformation':'typed boundary court -> owner review','negative':'missing terminal/boundary/external custody refuses','restore':'exact owner grant and evidence restore','test_command':'python3 test_integrated_strict.py','expected_effect':'no science/actor grant','authority':'OWNER_HELD','status':'NOT_RUN','dependencies':['TERMINAL_HOLDS','EXTERNAL_C']}],
 'h1_received_by_local_check':False,'protected_received_by_local_check':False,'actor_world_boundary':{'survey_implies_actor_knowledge':False,'fictional_mutates_source':False,'source_implies_material_power':False,'actor_private_state_from_source':False},
 'identity_dispositions':disp,'requirement_dispositions':[{'requirement_id':r['id'],'typed_obligation':r['typed_obligation'],'machine_assertion':r['machine_assertion'],'disposition':'FUTURE_NONPRECLUDED' if r['binding']=='FUTURE_NONPRECLUSION' else 'PRESENT_PRESERVED','evidence_grade':'DOCUMENTARY','actual_design_effect':r['substantive_requirement'],'specific_first_consumer_path':r['id']+' -> '+r['first_consumer'],'conservation_or_refusal_witness':r['positive_probe']+' / '+r['negative_probe'],'evidence':ref} for r in reqs]}
for x in decision['requirement_dispositions']: x['narrative_sha256']=nh(x,('actual_design_effect','specific_first_consumer_path','conservation_or_refusal_witness','disposition'))
dec_ptr=put('DECISION.json',decision)
c={'schema':'ANVIL_R7_INTEGRATED','stage':'INDEPENDENT_C','integrated_decision':dec_ptr,'integrated_decision_sha256':digest(decision),'first_consumer':frame['first_real_consumer'],
 'independent_reverse_walk_of_whole_frame':'The reviewer separately traces source through C11, I03, FF, world and actor evidence including negative cases and exact terminal holds',
 'strongest_choice_reversing_objection':'The installed event index may not support conditioned joint analysis economically at survey width','scientific_and_owner_boundary':'No source scientific rights or actor-level structural causality can be issued from a documentary assessment',
 'actual_first_consumer_assessment':'This authored fixture does not run a real native first consumer and cannot justify adoption of original survey science','historical_no_loss_assessment':'The complete historical inventory remains frozen with no recovered function automatically declared issued',
 'reviewer_relationship':'DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION','choice_reversing_objection_survives':False,'verdict':'C_HOLD_EXACT',
 'boundary_court':{},'graph_audit':{'producer_authority_time_consumer_checked':True,'holes':[],'boundary_edges_checked':['T1','T2','T3','T4','T5','T6','T7'],'terminal_ids_present':list(TERMINAL_IDS),'terminal_graph_checked':True},
 'terminal_audit':{'terminal_ids_present':list(TERMINAL_IDS),'terminal_fates':{n['id']:{'fate':n.get('terminal_fate'),'exact_hold':n.get('exact_hold',''),'owner':n.get('competent_owner','')} for n in graph['nodes'] if n['id'] in TERMINAL_IDS}},
 'builder_handoff_review':'The handoff identifies exact first-reader ABI, six projections, refusal/restore behavior, named external C/H1 consumer and honest local-only status','actual_first_reader_verified':False,'local_h1_claim':False,'protected_received_locally':False,'h1_grade':'NOT_RECEIVED',
 'builder_cards':[{'id':'present','domain':'CURRENT_FIRST_CONSUMER','grade':'EXACT_BUILDER_HOLD','exact_hold':'Actual native source consumer proof and competent owner execution are not part of this authored local fixture'},{'id':'future','domain':'FUTURE_NONPRECLUSION','grade':'EXACT_BUILDER_HOLD','exact_hold':'Future actor/world source governance remains independent and cannot be invented by this local fixture'}],
 'original_source_granted_by_local_check':False,'owner_granted_by_local_check':False}
for b in bc['boundaries']:
    t=b['id'];c['boundary_court'][t]={'machine_assertion':BOUNDARY_MACHINE[t],'positive':b['first_effect'],'negative':b['veto'],'restore':'Exact authorized source/owner bytes and permission restore the prior positive boundary effect','grade':'SOURCE_STATIC_CONSERVED','claim_grade':'SOURCE_STATIC_CONSERVED','actual_first_reader_verified':False,'authority_owner':b['owners'],'forbidden_promotions':[],'first_consumer_or_hold':b['receivers'],'evidence':{'path':'02_BOUNDARY_CONTRACTS.json','sha256':sha((SRC/'02_BOUNDARY_CONTRACTS.json').read_bytes()),'exact_excerpt':ex_around(SRC/'02_BOUNDARY_CONTRACTS.json','"id":"'+t+'"'),'zip_sha256':'526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332','zip_member':'ANVIL_R7/02_BOUNDARY_CONTRACTS.json'}}
for t,x in c['boundary_court'].items(): x['narrative_sha256']=nh(x,('positive','negative','restore','first_consumer_or_hold','authority_owner','claim_grade','grade','actual_first_reader_verified'))
c['narrative_sha256']=nh(c,('independent_reverse_walk_of_whole_frame','strongest_choice_reversing_objection','scientific_and_owner_boundary','actual_first_consumer_assessment','historical_no_loss_assessment','builder_handoff_review'))
put('C.json',c)
print(json.dumps({'status':'AUTHORED_FIXTURE_R2_BUILT','frame':frame_ptr,'decision':dec_ptr,'graph_nodes':len(nodes),'graph_edges':len(edges),'terminal_ids':len(TERMINAL_IDS)},indent=2))
