#!/usr/bin/env python3
"""Deterministic fixtures for the D3A active-gate tests.

Every fixture is derived from the byte-pinned source snapshot.  A fixture is a
TEST INPUT, never evidence of real decision quality.
"""
from __future__ import annotations
import hashlib, json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from r7_integrated import DOMAINS, digest, sha, _tokens
from r7_source_inventory import by_group

ROOT=pathlib.Path(__file__).resolve().parents[1]
INVENTORY=ROOT/'D3A_INVENTORY_SAMPLE.json'
COURT=json.loads((ROOT/'02_BOUNDARY_CONTRACTS.json').read_text())


def put(d,name,obj):
    b=(json.dumps(obj,sort_keys=True,ensure_ascii=False)+'\n').encode()
    (d/name).write_bytes(b)
    return {'path':name,'sha256':sha(b)}


def requirement_rows():
    return [{'id':f'R{i+1}','domain':d,
             'binding':'FUTURE_NONPRECLUSION' if d in ('SEAM_WORLD_ACTOR','FIELD_FORGE') else 'PRESENT_HARD',
             'substantive_requirement':f'{d} must preserve the exact original scientific and evidence boundary rather than a convenience substitute field',
             'why_needed':'This obligation is indispensable to the real first consumer regardless of the selected physical algorithm',
             'loss_if_missing':'A physically elegant layout could erase a necessary downstream or historical distinction',
             'first_consumer':'The current sourcefree native empirical recipient and the future governed possibility/world handoff',
             'architectural_consequence':'Preserve an independently inspectable representation of each relevant scientific distinction and later interface',
             'proof_or_owner_hold':'Check exact artifact semantics and replay with the qualified first consumer or preserve a named authority hold',
             'evidence':{'path':'12_ORIGINAL_MANDATE_AND_DECISION_LEVERAGE.md',
                         'sha256':sha((ROOT/'12_ORIGINAL_MANDATE_AND_DECISION_LEVERAGE.md').read_bytes()),
                         'exact_excerpt':'No magical disappearance of historical functions or negative evidence'}}
            for i,d in enumerate(DOMAINS)]


def frame(inventory):
    return {'schema':'ANVIL_R7_INTEGRATED','stage':'COMMON_FRAME',
            'workflow':'ONE_INTEGRATED_INVESTIGATION_OPTIONAL_TARGETED_DUELS',
            'phase':'BEFORE_ARCHITECTURE_SELECTION','architecture_selected':False,
            'mandatory_rival_architecture':False,'duel_required':False,
            'A_B_method':'OPTIONAL_SAME_QUESTION_SAME_EVIDENCE','scope':'C11_QUERY_DESIGN',
            'source_cut':inventory['source_cut'],'protected_head':'31291d08179890852246c8742700e055168e9933',
            'user_priority_source':'Pinned user instruction selecting the complete empirical system and lowest executable cost',
            'first_real_consumer':'Authorized generic sourcefree saved C11 native I03 and I05 operations',
            'currentness_gap_or_exact_verified_state':'Protected owner, lease and runtime conditions remain external and are not authenticated by this fixture',
            'science_authority_boundary':'Field Forge, world and actor science cannot be issued by a physical architecture author',
            'whole_program_mission':'Complete original function continuity and C11 empirical computation into later scientifically lawful world and person products',
            'source_grades_authentic_by_local_test':False,'requirements':requirement_rows(),
            'historical_conservation':None,'historical_source_spine':None}


def identity_rows(inventory):
    out=[]
    for r in inventory['rows']:
        g,rid=r['group'],r['id']
        toks=sorted(_tokens(r['source_semantics']))[:6]
        if g in ('K1_CAP',):state='PRESENT_PRESERVED'
        elif g in ('PYAT_PC','P4R'):state='EXACT_OWNER_HOLD'
        elif rid in ('SOROK','PRE-V3'):state='EXACT_OWNER_HOLD'
        else:state='FUTURE_NONPRECLUDED'
        row={'identity_id':rid,'disposition':state,'evidence_grade':'DOCUMENTARY',
             'candidate_specific_effect':f"The selected candidate preserves the original semantic field {' '.join(toks)} for {rid} without substituting a derived convenience column",
             'first_consumer_consequence':f"A cold authenticated read for {rid} returns the preserved field or the documented refusal rather than a silent default",
             'conservation_or_refusal_witness':f"Replay of the located source row for {rid} is byte-identical, and a denied or routed case refuses instead of returning a positive",
             'origin_row_sha256':r['origin']['row_sha256']}
        if state=='EXACT_OWNER_HOLD':
            row['owner']='Original K3/R15 or SOROK/PRE-V3 competent owner as recorded in the pinned source row'
        if g=='PYAT_PC':row['adopted']=False
        if g=='P4R':row['closed']=False
        out.append(row)
    return out


def boundary_court():
    out=[]
    for t in COURT['boundaries']:
        out.append({'boundary':t['id'],'contract_name':t['name'],
                    'must_preserve_witness':t['must_preserve'],
                    'status':'SOURCE_STATIC_CONSERVED',
                    'positive':{'case':f"Positive: the {t['id']} producer supplies a lawful payload and the declared receiver observes the expected first effect",
                                'expected':t['first_effect'],'evidence_grade':'DOCUMENTARY'},
                    'negative':{'case':f"Negative: a denied, unreleased or incompatible input at {t['id']} must refuse instead of yielding a positive product",
                                'expected':t['veto'],'evidence_grade':'DOCUMENTARY'},
                    'restore':{'case':f"Restore: after the {t['id']} negative the original input is replayed and the positive result matches byte for byte",
                               'expected':'exact restore matches the pre-negative result and the sealed original is unchanged','evidence_grade':'DOCUMENTARY'},
                    'graph_edge_ids':['E'+t['id'][1:]]})
    return out


def typed_graph():
    nodes=[{'id':'SRC','kind':'canonical evidence','owner':'PYAT source owner','authority':'OBSERVED','time_class':'OBSERVATION_TIME','payload_types':['event']},
           {'id':'C11','kind':'sealed C11 store','owner':'C11 physical owner','authority':'OBSERVED','time_class':'OBSERVATION_TIME','payload_types':['event','row']},
           {'id':'I03','kind':'native computation','owner':'PYAT I03/I05 owner','authority':'OBSERVED','time_class':'QUERY_TIME','payload_types':['row','joint']},
           {'id':'F14','kind':'analytic family','owner':'PYAT F1-F4 owner','authority':'DESCRIPTIVE_MODELED','time_class':'QUERY_TIME','payload_types':['joint','contrast']},
           {'id':'FF','kind':'Field Forge descriptive','owner':'PYAT Field Forge #1009','authority':'DESCRIPTIVE_MODELED','time_class':'QUERY_TIME','payload_types':['contrast','field']},
           {'id':'WLD','kind':'objective world','owner':'independent structural scientist','authority':'STRUCTURAL_QUALIFIED','time_class':'AS_OF_TIME','payload_types':['field','relation']},
           {'id':'FIC','kind':'particular fictional world','owner':'SOROK world particularizer','authority':'FICTIONAL_WORLD','time_class':'FICTIONAL_TIME','payload_types':['relation','encounter']},
           {'id':'ACT','kind':'independent actor','owner':'SOROK actor owner','authority':'ACTOR_STATE','time_class':'ACTOR_TIME','payload_types':['encounter','state']}]
    spec=[('E1','SRC','C11','event','T1'),('E2','C11','I03','row','T2'),('E3','I03','F14','joint','T2'),
          ('E4','F14','FF','contrast','T3'),('E5','FF','WLD','field','T4'),('E6','WLD','FIC','relation','T5'),
          ('E7','FIC','ACT','encounter','T6'),('E8','ACT','ACT','state','T7')]
    nmap={n['id']:n for n in nodes}
    edges=[]
    for eid,a,b,pt,bd in spec:
        edges.append({'id':eid,'from':a,'to':b,'payload_type':pt,'boundary':bd,
                      'authority_from':nmap[a]['authority'],'authority_to':nmap[b]['authority'],
                      'time_class':nmap[b]['time_class'],'evidence_grade':'DOCUMENTARY',
                      'negative':f"A denied, unreleased or incompatible payload at {bd} refuses rather than producing a positive downstream product",
                      'restore':f"Replaying the exact original input after the {bd} negative reproduces the pre-negative result byte for byte",
                      'first_consumer':f"The declared {bd} receiver reads the payload at its own authority and time class",
                      **({'external_source_warrant':'Independently sourced institutional material evidence with its own issuer, time basis and owner'}
                         if (nmap[a]['authority'],nmap[b]['authority'])==('DESCRIPTIVE_MODELED','STRUCTURAL_QUALIFIED') else {})})
    return {'nodes':nodes,'edges':edges}


def decision(inventory,fptr):
    fr=json.loads((pathlib.Path(fptr['path'])).read_text()) if False else None
    d={'schema':'ANVIL_R7_INTEGRATED','stage':'INTEGRATED_DECISION','common_frame':fptr,
       'decision_process':'ONE_SYNTHESIS_NO_MANDATORY_RIVAL','basis':'ANALYTICAL_SOURCE_GROUNDED',
       'grade':'AUTHOR_PROPOSED_PENDING_C',
       'architecture_description':'Retain canonical C11 authority, add a scoped derived execution interface, and preserve every proof and first-consumer boundary explicitly',
       'entire_source_to_actor_dataflow':'From legitimate original source projection through canonical thirteen-family C11 and native I03 computation into F1-F4, Field Forge, an independently sourced objective world and a continuing actor',
       'algorithm_and_data_structures':'Use one verified event store, two selective access routes, and reusable evidence-bearing respondent condition intermediates without a duplicate authority',
       'resource_cost_reasoning':'Minimize repeated event reconstruction and qualified population evaluation before changing a physical store, while retaining the six-gibibyte process-tree ceiling',
       'historical_function_conservation':'Conserve all 118 historical and prospective identities with their negative semantics, linked first consumers and truthful nonadoption of future science',
       'scientific_boundary_and_nonpreclusion':'Observational survey relationships cannot become structural causes, fictional world facts, or actual actor experiences without separate competent science',
       'strongest_surviving_objection':'The current body-json layout may impose first-query cost that an authenticated selective reader cannot avoid without an alternative indexing format',
       'why_selected_over_feasible_alternatives':'It uses accepted existing semantic and physical assets and introduces less compatibility and authority risk than replacing the entire persistent representation',
       'next_actual_engineering_operation':'Publish and independently receive the prepared saved-session correction, then implement one sourcefree shared population execution path under existing owner rights',
       'single_selected_strategy':'Verified C11 with a prepared analytical execution layer',
       'first_real_consumer':'Authorized generic sourcefree saved C11 native I03 and I05 operations',
       'alternatives_considered':[{'technical_approach':'Wholesale independent SQL-backed physical release replacement','state':'VIABLE_NOT_SELECTED',
         'why_not_selected_or_held':'It would reopen canonical replay and source authentication without evidence that it resolves the present repeated-evaluation cost'}],
       'choice_reversers':[{'status':'RESOLVED_AT_ANALYTICAL_SCOPE','question':'Can qualified population preparation be reused without changing source truth?'}],
       'requires_full_A_B_comparison':False,'competing_implementations_mandatory':False,
       'architecture_claims_independent_acceptance':False,'targeted_duel':None,
       'boundary_contract_sha256':sha((ROOT/'02_BOUNDARY_CONTRACTS.json').read_bytes()),
       'identity_dispositions':identity_rows(inventory),'boundary_court':boundary_court(),'typed_graph':typed_graph(),
       'requirement_dispositions':[{'requirement_id':r['id'],
          'disposition':'FUTURE_NONPRECLUDED' if r['binding']=='FUTURE_NONPRECLUSION' else 'PRESENT_PRESERVED',
          'evidence_grade':'DOCUMENTARY',
          'actual_design_effect':'Keep the original documented capacity and a typed consumer boundary with explicit negative and restoration semantics',
          'specific_first_consumer_path':'Native saved I03 facts can lawfully feed qualified conditional and possibility interfaces under source authority',
          'conservation_or_refusal_witness':'Frozen source contracts specify the required denial and restoration behaviour, not an executed proof',
          'evidence':r['evidence']} for r in requirement_rows()]}
    return d
