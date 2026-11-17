#!/usr/bin/env python3
"""Synthetic test generator only. DO NOT use these receipts as native/independent evidence."""
import hashlib,json,pathlib,sys
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
import r7
HASH='a'*40

def put(root,path,datum):
    p=pathlib.Path(root)/path;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(datum,sort_keys=True,indent=2)+'\n')
    return {'path':path,'sha256':r7.filehash(p)}

def claim():
    return {'release':'sourcefree rel 1','instrument':'synthetic test only instrument','country':'fictional country','wave':'synthetic test wave',
            'question':'Q1 synthetic test question','source_ref':'synthetic qualified questionnaire source','evidence_ref':'synthetic sourcefree evidence',
            'source_unit':'PERSON','target_unit':'PERSON','asked':'YES','released':'YES','observation':'VALUE','eligibility':'ELIGIBLE',
            'unit':'PERSON','attribution':'SELF','target_attribution':'SELF','source_status':'DOCUMENTED_RESPONDENT_RESPONSE',
            'translation':'SAME_INSTRUMENT','original_code_ref':'selected original code in sourcefree fixture',
            'record_value_ref':'respondent source record exact ref fixture','claim_kind':'RESPONDENT_ORIGINAL_VALUE','target_is_respondent_claim':True}

def graph():
    names=['OBSERVED','DESCRIPTIVE_MODELED','EXTERNAL_OBSERVED','STRUCTURAL_QUALIFIED','FICTIONAL_WORLD','ACTOR_STATE','HISTORY_EVENT']
    nodes=[{'id':s,'domain':s} for s in names]
    arr=[('OBSERVED','DESCRIPTIVE_MODELED','DESCRIPTIVE_INFERENCE','SCIENCE_GRADED'),
         ('EXTERNAL_OBSERVED','STRUCTURAL_QUALIFIED','INDEPENDENT_STRUCTURAL_ISSUANCE','EXTERNAL_STRUCTURAL_ISSUER'),
         ('STRUCTURAL_QUALIFIED','FICTIONAL_WORLD','WORLD_OPPORTUNITY','WORLD_PARTICULARIZER'),
         ('FICTIONAL_WORLD','ACTOR_STATE','ACTOR_ACCESS_OR_LEARNING','ACTOR_OWNER'),
         ('ACTOR_STATE','HISTORY_EVENT','PERFORMED_ACT','ACTOR_OWNER'),
         ('FICTIONAL_WORLD','HISTORY_EVENT','EXOGENOUS_WORLD_EVENT','WORLD_OWNER')]
    edges=[]
    for i,(f,t,tr,au) in enumerate(arr):edges.append({'id':f'G{i}','from':f,'to':t,'transition':tr,'authority':au,
                  'payload':'synthetic typed source observation with explicit provenance','negative':'source deny returns typed hold and no invented value',
                  'clock':'observed historical clock separate fictional world clock','owner':'synthetic sourcefree authority test owner',
                  'evidence_ref':'sourcefree synthetic graph witness only'})
    lookup={'OBSERVED_TO_DESCRIPTIVE':['G0'],'EXTERNAL_TO_STRUCTURAL_WORLD':['G1','G2'],'WORLD_TO_ACTOR':['G3'],
            'ACTOR_TO_HISTORY':['G4'],'EXOGENOUS_TO_HISTORY':['G5']}
    routes={rid:{'edge_ids':ids,'first_consumer':'test fixture proposed receiver type matching domain',
        'first_consumer_node_id':edges[int(ids[-1][1:])]['to'], 'consumer_status':'PLANNED_OWNER_HELD',
        'source_or_world_clock':'source clock separate from derived fictional world clock',
        'preserved_information':'exact source code identity and respondent occurrence provenance',
        'legitimate_owner':'separate competent scientific actor source owner required',
        'negative_or_hold':'no actor or independent structural authority inferred from survey',
        'proof_grade':'OWNER_HELD_WITH_FEASIBLE_EXTENSION',
        'extension_abi':'future qualified first-consumer typed versioned ABI candidate'} for rid,ids in lookup.items()}
    return nodes,edges,routes

def make(root,scope='C11_QUERY_DESIGN'):
    root=pathlib.Path(root);root.mkdir(parents=True,exist_ok=True)
    cells=[];dim={m:d for d,vs in r7.POL['physical_dimensions'].items() for m in vs}
    for i,(w,d,m) in enumerate(sorted(r7.required_floor(scope))):
        cells.append({'id':f'M{i:02d}','workload':w,'dimension':d,'metric':m,'decision_id':'P-C11',
         'selection_reverser_A':'If A cannot meet this source-qualified metric B may win',
         'selection_reverser_B':'If B cannot meet this source-qualified metric A may win',
         'input_sha':r7.digest(['synthetic',w,d,m]),'runner_identity':'SYNTHETIC_UNTRUSTED_RUNNER_R7',
         'negative_restore':'SYNTHETIC source cut denied then exactly restored',
         'first_consumer':'exact sourcefree C11 I03 cold operation selected consumer',
         'source_grade':'S2_SOURCEFREE_EXECUTED'})
    plan={'schema':'ANVIL_R7_PLAN_1','scope':scope,'version':1,'parent_digest':None,'phase':'BEFORE_FIRST_RESULT',
          'policy_digest':r7.filehash(r7.ROOT/'contracts/policy.json'),'A0_head':HASH,'B0_head':'b'*40,
          'first_results_seen':False,'cells':cells,'exclusions':[]}
    plan['freeze_digest']=r7.planhash(plan)
    evidence={}; results=[]
    for c in cells:
        row={'cell_id':c['id'],'fixture_hash':c['input_sha'],'runner_identity':c['runner_identity']}
        for side,interval in [('A',(1.,1.1)),('B',(2.,2.1))]:
            evid='receipt_'+side+'_'+c['id']
            rec={'schema':'ANVIL_R7_MEASUREMENT_RECEIPT_1','candidate':side,'cell_id':c['id'],
                  'fixture_hash':c['input_sha'],'runner_identity':c['runner_identity'],'metric':c['metric'],
                  'grade':'S2_SOURCEFREE_EXECUTED','code_head':HASH,
                  'design_frozen_head':plan[side+'0_head'],
                  'unit':'BYTES' if c['metric'].endswith('_bytes') else 'SECONDS',
                  'mechanism_signature':'synthetic '+side+' design signature - no actual backend',
                  'low':interval[0],'high':interval[1],
                  'source_ref':'SYNTHETIC-FIXTURE-NO-REAL-SOURCE','methodology':'constructed numbers for negative validator tests ONLY',
                  'sample_count':3,'positive':'synthetic sample positive no real run','negative':'synthetic invalid-source denied as test data',
                  'restore':'synthetic clean source restored as fake test','measuring_host':'UNITTEST_HOST_NOT_REAL_ENGINE'}
            loc=put(root,f'receipts/{side}_{c["id"]}.json',rec)
            evidence[evid]={'grade':'S2_SOURCEFREE_EXECUTED','code_head':HASH,'raw_receipt_ref':loc['path'],
                         'raw_sha256':loc['sha256'],'source_ref':'SYNTHETIC-FIXTURE-NO-REAL-SOURCE',
                         'independent_checked':True,'description':'local mock-only no real host scientific evidence'}
            row[side]={'status':'MEASURED','low':interval[0],'high':interval[1],'evidence_id':evid}
        results.append(row)
    vet=[]
    for side in ('A','B'):
      for v in r7.POL['required_non_numeric_vetoes']:
        data={'schema':'ANVIL_R7_VETO_WITNESS_1','veto_id':v,'candidate':side,
              'scope':scope,'status':'PASS_AT_STATED_SCOPE',
              'source_ref':'SOURCEFREE_SYNTHETIC_ONLY_NO_REAL_AUTHORITY',
              'evidence_grade':'S2_SOURCEFREE_EXECUTED_SYNTHETIC_ONLY',
              'qualified_owner':'synthetic test runner not competent for real source',
              'negative':'synthetic denied tampered source state false',
              'restore':'synthetic restored source same exact fixture',
              'limitation':'UNTRUSTED SYNTHETIC NEVER PRODUCTION SCIENCE'}
        loc=put(root,f'veto/{side}_{v}.json',data);vet.append({'veto_id':v,'candidate':side,**loc})
    measurement={'schema':'ANVIL_R7_MEASUREMENTS_1','freeze_digest':plan['freeze_digest'],
         'policy_digest':r7.filehash(r7.ROOT/'contracts/policy.json'),'results':results,'evidence':evidence,'veto_receipts':vet}
    compared=r7.comparison(plan,measurement,evidence_root=root)
    nodes,edges,routes=graph();ev={'e0':{'grade':'S1_SOURCE_STATIC','code_head':HASH,
                     'raw_receipt_ref':'fixture static source only','source_ref':'synthetic presource',
                     'independent_checked':True,'description':'synthetic fake evidence no scientific authority'}}
    sem={}
    for w in ('W-R','W-J','W-X'):
        id='semantic_'+w;loc=put(root,f'semantic/{w}.json',{'schema':'ANVIL_R7_SEMANTIC_WITNESS_1','witness_id':w,
          'scope':scope,'status':'PASS_AT_STATED_SCOPE','scientific_ceiling':'SYNTHETIC_SOURCEFREE_ONLY'})
        ev[id]={'grade':'S2_SOURCEFREE_EXECUTED','code_head':HASH,'raw_receipt_ref':loc['path'],
          'raw_sha256':loc['sha256'],'source_ref':'synthetic selected source meaning',
          'independent_checked':True,'description':'synthetic semantic witness not real native execution'};sem[w]=id
    handoff={'id':'HANDOFF-P-C11','decision_id':'P-C11','first_consumer_node_id':'DESCRIPTIVE_MODELED','implementation_status':'READY_FOR_IMPLEMENTER',
        'owner':'qualified actual technical owner at live source HEAD',
        'input_abi':'source-free selected exact sealed C11 release','output_abi':'typed empirical I03 result with negative replay',
        'negative':'tampered or missing source returns typed error and no fact','currentness':'current release recertify each new session',
        'rights_grade':'synthetic no original source or science authority','first_effect':'changed cell changes selected cold first I03 fact',
        'dependency':'source-valid C11 persistence and valid native first query',
        'test_command':'python -m pytest tests/test_native_i03 -q',
        'first_consumer':'existing supported sourcefree I03 query first reader',
        'producer_symbol':'rawlsing_next/pre553_direct_estate_i03.py::DirectEstateI03Session',
        'consumer_symbol':'rawlsing_next/pre553_empirical_query.py::execute_empirical_query',
        'source_cut':HASH,'first_consumer_grade':'EXACT_STATIC_IMPLEMENTATION_ABI'}
    spine={'schema':'ANVIL_R7_SPINE_1','policy_digest':r7.filehash(r7.ROOT/'contracts/policy.json'),
       'source_registry_digest':r7.filehash(r7.ROOT/'contracts/source_registry.json'),
       'freeze_digest':plan['freeze_digest'],'comparison_digest':r7.digest(compared),'scope':scope,
       'author_proposed_grade':'DESIGN_READY_SCOPED','builder_cold_start':'PENDING_INDEPENDENT_C','P2_source_head':HASH,'selected_candidate':'A',
       'historical_inheritance':{'families':29,'K3_not_adopted_count':26,'P4R_held_count':14,
         'exact_ids':sum(r7.SRC['mandatory'].values(),[])},
       'claims':[claim()],'nodes':nodes,'edges':edges,'routes':routes,'evidence':ev,
       'physical_decisions':[{'id':'P-C11','selected':'A','cell_ids':[x['id'] for x in cells],
         'actual_first_consumer':'sourcefree direct C11 I03 selected cold first reader','first_consumer_node_id':'DESCRIPTIVE_MODELED','handoff_id':'HANDOFF-P-C11',
         'dependency_effect':'all tested physical layout and access decisions belong to this same selected test target',
         'shared_evidence_scope':'DIRECTLY_MEASURED','hard_veto_evidence_ids':['e0']}],
       'handoffs':[handoff],'semantic_witnesses':sem,
       'product_deltas':[{'grade':'NO_NEW_PRODUCT_ADVANCE','before_evidence':'e0','after_evidence':'e0',
         'changed_first_consumer_effect':'synthetic only no real product delta'}]}
    return plan,measurement,compared,spine

if __name__=='__main__':
    root=pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parents[1]/'fixtures'
    plan,measure,compare,spine=make(root)
    for name,d in [('SYNTHETIC_PLAN.json',plan),('SYNTHETIC_MEASUREMENTS.json',measure),
                   ('SYNTHETIC_COMPARISON.json',compare),('SYNTHETIC_SPINE.json',spine)]:
        (root/name).write_text(json.dumps(d,indent=2)+'\n')
    print(json.dumps({'scope':plan['scope'],'cells':len(plan['cells']),'comparison':compare['status'],
          'plan_errors':r7.plan_errors(plan),'spine_errors':r7.validate_spine(spine,plan,measure,compare,root)},indent=2))
