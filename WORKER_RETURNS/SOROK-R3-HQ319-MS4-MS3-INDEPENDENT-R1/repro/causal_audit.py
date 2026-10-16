from stage import R,git
import json,sys
sys.path.insert(0,str(R/'staging/ms3/staging/ms2/staging/ms1/runtime'))
from candidate.candidate_registry_fixture import digest
rows=[]
for cid in ['C1','C2','C3','C4','C4b','C5','C6','C7','C8','C9','C10']:
    path='evidence/ms3/ms2_51/observations/cell_'+cid+'.json';d=json.loads((R/path).read_text())
    original=json.loads(git('show','34b96ea98de181ca5264f0eed3824cad2db7cfc0:WORKER_RETURNS/SOROK-R3-HQ317-MS2-MS1-SERIAL-INDEPENDENT-R1/evidence/new/observations/cell_'+cid+'.json'))
    response=d['response'];old=original['response'];owner=d['pre_read']['owner']['state']
    assert d['pre_read']['owner']==original['pre_read']['owner'] and d['pre_read']['owner']==d['after']['owner']
    assert (response['decision_state'],response.get('effect_kind'))==(old['decision_state'],old.get('effect_kind'))
    assert response['owner_state_hash_read']==digest(owner)
    rows.append(dict(cell=cid,content=d['content'],native_owner_pre_read_hash=digest(owner),same_original_MS2_owner=True,decision=response['decision_state'],effect=response.get('effect_kind'),permission=response.get('chosen_from_permission'),committed=response['committed'],observation=path))
by={x['cell']:x for x in rows}
assert (by['C2']['decision'],by['C2']['effect'])==(by['C4']['decision'],by['C4']['effect'])==('DEFER_MISSING_AUTHORITY',None)
h=json.loads((R/'evidence/ms3/ms2_51/observations/history_and_CAN3.json').read_text())
can3=h['comparator'];assert can3['stored']['state']==can3['omitted']['state']
assert can3['stored']['later_event_response']['effect_kind']=='DEFLECT' and can3['omitted']['later_event_response']['effect_kind']=='AMPLIFY'
(R/'08_CAUSAL_AND_SCIENTIFIC_LEDGER.json').write_text(json.dumps(dict(cells=rows,P3b='LITERAL_FAIL',F_B='FIRED',serial_mechanism_identification='HOLD',consumer_full_ctx=True,response_journal_commit=False,hypothetical_mediator='UNISSUED',native_content_to_belief_law='NOT_ISSUED',history_input='COUNT_CONTROL_DISTINCT_FROM_NATIVE_CAN3',native_CAN3=dict(equal_owner_state=True,stored='DEFLECT',omitted='AMPLIFY'),authority_quote_correction='Trace refs may condition a private update is a CAN2 candidate-code comment, not a quotation from accepted ADP017',e2_content_scope='ANY_NONEMPTY_STRING_FEATURES_WITHIN_NATIVE_ENVELOPE; no exact-E2-content selector'),indent=2)+'\n')
print('11 cell native-owner/decision invariants verified; P3b FAIL; native CAN3 contrast retained')
