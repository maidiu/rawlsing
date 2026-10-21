import copy
from n1_eligibility import GRADE, seal_record, screen, compile_test_only_bp2_resources

A='TEST_ONLY_A'; B='TEST_ONLY_B'

def entry(k,n,t,who=A,owner=None,operation='coordinated_material_inspection',occurred=True):
    return seal_record(dict(kind=k,ref='TEST_ONLY_'+n,time=t,subject=who,
        owner=owner or 'TEST_ONLY_OWNER_'+n,grade=GRADE,
        operation=operation,occurred=occurred))

def fixture():
    return dict(case_id='TEST_ONLY_N1_CASE',actor_id=A,other_actor_id=B,
        operation='coordinated_material_inspection',as_of=50,records=[
         entry('ADP010_OPPORTUNITY','opp',1),entry('ACTOR_ENACTED','first',2),
         entry('ACTOR_ENACTED','second',4),entry('ADP010_ENCOUNTER','enc',6),
         entry('OTHER_OFFER','offer',7,B), entry('ADP019_E1','e1',9)])

def test_positive_only_owner_review_not_native():
    q=screen(fixture()); assert q['status']=='OWNER_REVIEW_CANDIDATE'; assert q['native_rule_issued'] is False; assert q['target_write_permitted'] is False

def test_e1_severance_to_request_evidence():
    x=fixture(); x['records']=[r for r in x['records'] if r['kind']!='ADP019_E1']; assert screen(x)['status']=='REQUEST_EVIDENCE'

def test_contact_without_encounter_not_e1():
    x=fixture(); x['records']=[r for r in x['records'] if r['kind']!='ADP010_ENCOUNTER']; assert screen(x)['status']=='REQUEST_EVIDENCE'

def test_no_enacted_is_no_change():
    x=fixture(); x['records']=[r for r in x['records'] if r['kind']!='ACTOR_ENACTED']; assert screen(x)['status']=='NO_CHANGE'

def test_no_other_is_no_change():
    x=fixture(); x['records']=[r for r in x['records'] if r['kind']!='OTHER_OFFER']; assert screen(x)['status']=='NO_CHANGE'

def test_single_act_not_universal_trait():
    x=fixture(); x['records']=[r for r in x['records'] if r['ref']!='TEST_ONLY_second']; assert screen(x)['status']=='REQUEST_EVIDENCE'

def test_same_source_owner_not_independent_method():
    x=fixture(); q=x['records'][2];q['owner']=x['records'][1]['owner'];x['records'][2]=seal_record({k:v for k,v in q.items() if k!='hash'}); assert screen(x)['status']=='REQUEST_EVIDENCE'

def test_contradictory_behavior_preserved():
    x=fixture();x['records'].append(entry('CONTRARY_ACTION','contrary',8)); assert screen(x)['status']=='COMPETING'

def test_self_narration_not_enacted():
    x=fixture();x['records']=[r for r in x['records'] if r['kind']!='ACTOR_ENACTED']; x['records'].append(entry('ACTOR_SELF_REPORT','speech',3));assert screen(x)['status']=='NO_CHANGE'

def test_role_prior_not_enacted():
    x=fixture();x['records']=[r for r in x['records'] if r['kind']!='ACTOR_ENACTED'];x['records'].append(entry('ROLE_PRIOR','role',3));assert screen(x)['status']=='NO_CHANGE'

def test_same_actor_as_other_denied():
    x=fixture();x['other_actor_id']=A;assert screen(x)['status']=='DENY'

def test_forged_hash_denied():
    x=fixture();x['records'][1]['operation']='forced_outcome';assert screen(x)['status']=='DENY'

def test_repeated_source_ref_denied():
    x=fixture(); x['records'].append(copy.deepcopy(x['records'][1]));assert screen(x)['status']=='DENY'

def test_foreign_source_owner_denied():
    x=fixture();x['records'][1]['owner']='BAD'; x['records'][1]=seal_record({k:v for k,v in x['records'][1].items() if k!='hash'});assert screen(x)['status']=='DENY'

def test_future_past_denied():
    x=fixture();x['records'][1]['time']=100; x['records'][1]=seal_record({k:v for k,v in x['records'][1].items() if k!='hash'});assert screen(x)['status']=='DENY'

def test_e1_before_encounter_denied():
    x=fixture();x['records'][-1]['time']=5;x['records'][-1]=seal_record({k:v for k,v in x['records'][-1].items() if k!='hash'});assert screen(x)['status']=='DENY'

def test_e1_not_occurred_unknown():
    x=fixture();x['records'][-1]['occurred']=False;x['records'][-1]=seal_record({k:v for k,v in x['records'][-1].items() if k!='hash'});assert screen(x)['status']=='REQUEST_EVIDENCE'

def test_no_resources_compiled_when_ineligible():
    x=fixture();x['records']=[];q=compile_test_only_bp2_resources(x,None,now=10); assert q['rule_a'] is None; assert q['grant'] is None

def test_qualified_requires_actual_bp2_ports():
    try:compile_test_only_bp2_resources(fixture(),None,now=10)
    except ValueError as e:assert str(e)=='ACTUAL_BP2_PORTS_REQUIRED'
    else:assert False

def test_order_and_fingerprint_stable():
    x=fixture(); a=screen(x);x['records'].reverse();b=screen(x);assert a==b

def test_unknown_self_knowledge_not_inferred():
    assert screen(fixture())['rivals']['actor_self_knowledge']=='UNKNOWN_WITHOUT_ADP017'
