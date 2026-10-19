from collections import Counter
from dataclasses import replace
from pathlib import Path
import copy,hashlib,json
import pytest
import scientific_crosswalk as cross
import experiment as exp
import reused_wg0r_fixture as inherited
from reconcile_execution import reconcile
from rawlsing_next.pre553_route_b_production import I03ExecutionRequest
R=Path(__file__).resolve().parent
EXPECTED_SHA='12f6d4880ce343ec9676863858d8bfcf2e801d1845bca72e71a0fc5e9d2dfb61'

@pytest.fixture(scope='module')
def research():return cross.build()
@pytest.fixture(scope='module')
def expected():
    p=R/'evidence/EXPERIMENT_EXPECTED.json'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==EXPECTED_SHA
    return json.loads(p.read_text())
@pytest.fixture(scope='module')
def receipts():return json.loads((R/'evidence/native_experiment.json').read_text())

def test_full_identity_multiset_and_all35(research):
    d=research; c=d['counts']
    assert [c[k] for k in ['p2','qra_active','common','p2_only','qra_only_blocked','net_delta','research_union','excluded_inactive']]==[18276,18259,18250,26,9,17,18285,259]
    assert len({r['record_id'] for r in d['union']})==18285
    assert len(d['waves'])==35 and len({x['atlas_id'] for x in d['waves']})==35
    assert Counter(x['join'] for x in d['union'])=={'COMMON_EXACT_HASH':18250,'P2_ONLY':26,'QRA_ONLY_BLOCKED':9}
    assert sum(x['P2_ONLY']-x['QRA_ONLY_BLOCKED'] for x in d['waves'])==17

def test_party_is_substantive_with_original_structure_witness(research):
    x=next(r for r in research['rows'] if r['variable']=='party')
    assert x['inherited_role']=='substantive_nominal_choice'
    assert x['classification']=='SUBSTANTIVE_MEASUREMENT_CANDIDATE'
    labels={e['owner'] for e in x['evidence']};assert {'P2_IMPLEMENTATION_AUTHORITY','register_A','register_B'}<=labels
    roles=research['counts']['p2_only_roles']; assert roles['admin']+roles['administrative_metadata']==6
    assert sum(roles.values())-6==20

def test_all_nine_blocked_rows_preserved_without_synthetic_identity(research):
    rows=[r for r in research['rows'] if r['side']=='QRA_BLOCKED']
    assert len(rows)==9 and all(r['p2_exact_identity_sha256'] is None for r in rows)
    assert all(r['current_operation_status']=='SOURCE_OR_OPERATION_HELD' for r in rows)

def test_accepted_duplicate_q47st_assertions_are_not_last_row_deduplicated():
    rows=cross.load('sources/owner_row_projections.json')['v525b_semantic']['selected_records']
    rows=[x for x in rows if x['exact_case_key']==['Latinobarómetro','2024','Q47ST']]
    assert len(rows)==2 and len({r['row_sha256'] for r in rows})==2
    assert any('printed press' in r['row']['display_text'] for r in rows)
    assert any('social media' in r['row']['display_text'] for r in rows)

def test_v525b_and_later_driver_difference_is_retained():
    owners=cross.load('sources/owner_row_projections.json')
    def driver(label,var):return [x['row']['final_driver_id'] for x in owners[label]['selected_records'] if x['exact_case_key']==['Latinobarómetro','1995',var]]
    assert driver('v525b_drivers','P43')==['genderEquality']
    assert driver('d62_driver_provenance_only','P43')==['imperialAlignment']
    assert driver('v525b_drivers','P47')==['temporalOrientation']
    assert driver('d62_driver_provenance_only','P47')==['imperialAlignment']

def test_exact_physical_names_are_candidate_bindings_not_replacements(research):
    rows={r['variable']:r for r in research['rows'] if r['side']=='P2_ONLY'}
    for q,p in cross.PHYSICAL_CANDIDATES.items():
        r=rows[q];assert r['physical_alias_candidate']==p
        assert any(e['owner']=='register_B' and e['exact_case_key'][2]==p for e in r['evidence'])
        assert r['variable']==q and r['current_operation_status']=='SOURCE_OR_OPERATION_HELD'

def test_p46_and_entity_subitems_keep_multiplicity(research):
    rows=[r for r in research['rows'] if r['side']=='P2_ONLY']
    assert len([r for r in rows if r['variable'].startswith('p46')])==8
    assert {r['variable'] for r in rows if r['variable'].startswith('p47')}=={'p47a','p47b','p47c'}
    assert all('UNBOUND' in r['respondent_carrier'] and r['source_version']['actual_source_edition_hash']=='UNBOUND' for r in rows)

def test_research_is_not_original_permission_or_full_frontier(research):
    assert research['original35_current_operation_permission']=='UNCHANGED_HOLD__NO_ISSUANCE'
    assert all(r['current_operation_status']=='SOURCE_OR_OPERATION_HELD' for r in research['rows'])
    assert all(r['operation_binding'].startswith('HELD') for r in research['union'])

@pytest.mark.parametrize('path', ['sources/p2_identity_projection.jsonl','sources/qra_identity_projection.jsonl','sources/p2_only_exact_rows.json','sources/qra_blocked_exact_rows.json'])
def test_mutated_source_projection_refused(path,tmp_path,monkeypatch):
    for p in [*cross.load('evidence/PREIMPLEMENTATION_FREEZE.json')['inputs'], 'evidence/PREIMPLEMENTATION_FREEZE.json']:
        d=tmp_path/p;d.parent.mkdir(parents=True,exist_ok=True);d.write_bytes((R/p).read_bytes())
    p=tmp_path/path;p.write_bytes(p.read_bytes()+b' ')
    monkeypatch.setattr(cross,'R',tmp_path)
    with pytest.raises(ValueError,match='FROZEN_INPUT_CHANGED'):cross.build()

@pytest.mark.parametrize('mode',['positive','missing_weight','valid_empty'])
def test_named_prefrozen_fixture_matches_input(mode,expected):
    fx=exp._fixture(**({'missing_weight':True} if mode=='missing_weight' else {'valid_empty':True} if mode=='valid_empty' else {}))
    exp.verify_fixture(fx,expected[mode]); exp.verify_jobs(expected[mode],inherited.enumerate_requests(fx['catalog']),fx['catalog'].discovery_authorities)

@pytest.mark.parametrize('mutation',['missing','duplicate','wrong_predicate','no_discovery'])
def test_preexecution_job_anti_join_refuses(mutation,expected):
    fx=exp._fixture();req=list(inherited.enumerate_requests(fx['catalog']));ds=fx['catalog'].discovery_authorities
    if mutation=='missing':req.pop()
    if mutation=='duplicate':req.append(req[0])
    if mutation=='wrong_predicate':req[0]=I03ExecutionRequest(req[0].query_ref,fx['x1'].ref)
    if mutation=='no_discovery':ds=()
    with pytest.raises(ValueError,match='MULTISET'):exp.verify_jobs(expected['positive'],req,ds)

@pytest.mark.parametrize('mutation',['source_version','respondent_mapping_swap','changed_weight'])
def test_full_source_binding_changes_refused(mutation,expected):
    fx=exp._fixture()
    if mutation=='source_version':fx['stream']=replace(fx['stream'],source_sha256='f'*64)
    elif mutation=='changed_weight':fx=exp._fixture(missing_weight=True)
    else:
        # Same row/slot counts, substituted exact respondent namespace.
        p=fx['projection']; b=p.row_bindings[0]
        other=p.row_bindings[1]
        fx['projection']=replace(p,row_bindings=(replace(b,respondent_ref=other.respondent_ref),replace(other,respondent_ref=b.respondent_ref),*p.row_bindings[2:]))
    with pytest.raises(ValueError,match='PREIMAGE'):exp.verify_fixture(fx,expected['positive'])

@pytest.mark.parametrize('mode',['positive','missing_weight'])
def test_actual_receipts_and_consumers(mode,expected,receipts):
    out=reconcile(expected[mode],receipts[mode])
    assert out['expected']==out['actual']==out['executed']==3
    assert out['consumer_positive']=='RULE_SATISFIED' and out['consumer_held']=='UNRESOLVED'
    assert receipts[mode]['resumed_new_executions']==0
    assert receipts[mode]['batch_summary']['pending_units']==0

def test_actual_missing_weight_stays_unavailable(receipts):
    fs=receipts['missing_weight']['i03_facts'];weighted=[f for f in fs if f['semantic_fields']['measure_kind']=='GOVERNED_WEIGHTED']
    assert weighted and all(f['typed_state']=='UNAVAILABLE' for f in weighted)
    assert any(f['typed_state']=='SUPPORTED' for f in fs)

def test_valid_empty_discovery_has_native_typed_receipt(receipts):
    ds=receipts['valid_empty']['i05_receipts']
    assert ds and all(d['typed_state']=='VALID_EMPTY' for d in ds)

@pytest.mark.parametrize('mutation',['missing_receipt','duplicate_receipt','deferred','drop_fact','wrong_result','consumer_drop','drop_manifest'])
def test_postexecution_missing_substituted_or_hidden_results_refused(mutation,expected,receipts):
    x=copy.deepcopy(receipts['positive'])
    if mutation=='missing_receipt':x['batch_receipts'].pop()
    if mutation=='duplicate_receipt':x['batch_receipts'].append(x['batch_receipts'][0])
    if mutation=='deferred':x['batch_receipts'][0]['state']='DEFERRED'
    if mutation=='drop_fact':x['i03_facts'].pop()
    if mutation=='wrong_result':x['batch_receipts'][0]['result_refs']=[]
    if mutation=='consumer_drop':x['consumer_positive']['semantic_fields']['discovery_result_receipt_refs']=[]
    if mutation=='drop_manifest':x['manifest']['units'].pop()
    with pytest.raises(ValueError):reconcile(expected['positive'],x)
