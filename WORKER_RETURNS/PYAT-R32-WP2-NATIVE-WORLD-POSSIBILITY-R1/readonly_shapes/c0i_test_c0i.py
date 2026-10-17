"""Independent C0I prospective court; frozen before first collection/execution."""
from pathlib import Path
from copy import deepcopy
from dataclasses import replace
import importlib.util,json,os,sys
import pytest
R=Path(__file__).resolve().parents[1];RT=R/'staging/runtime';sys.path.insert(0,str(RT))
from product.service import GenericSelectedWorldService
from product import nonparent,scenario
from product.empirical import GenericProgressiveProvider,build_source
from product.world import SelectedSnapshot
from rawlsing_next.pre553_empirical_objects import semantic_hash
from rawlsing_next.pre553_empirical_authority import AuthorityRegistry,Pre553AuthorityError
OBS=[]
@pytest.fixture(autouse=True)
def observed(request):
    OBS.clear();yield
    out=R/'evidence/hostile/observations';out.mkdir(parents=True,exist_ok=True)
    (out/(request.node.name+'.json')).write_text(json.dumps(dict(case=request.node.nodeid,observations=OBS),indent=2,default=str)+'\n')
def note(**kw):OBS.append(deepcopy(kw))
def seed(**kw):
    svc=GenericSelectedWorldService(**kw);ss=svc.select(valid_at='2027-09-01',published_asof='2027-09-01');return svc,ss
def consume(s,ss,who):return nonparent.consume(s,ss,budget_tokens=5) if who=='nonparent' else scenario.evaluate(s,ss,[dict(scenario_id='MS',route='institutional'),dict(scenario_id='CIV',route='civil')])
def projection(rec):return rec['material']['empirical']
def cells(step):return {x['cell']:x['raw_numerator_support'] for x in step['cells']}
def port_module(relocate=True):
    # Native imports are already from this fresh runtime. Do not read /tmp sources.
    name='c0p_port_under_review';spec=importlib.util.spec_from_file_location(name,R/'staging/c0p/repro/c0p_two_contract_port.py');m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m)
    if relocate:m.RUNTIME=RT # documented path-only harness adaptation; no source edit
    return m

@pytest.mark.parametrize('who',['nonparent','mother'])
def test_named_clients_read_exact_native_support_and_preserve_no_parent(who):
    s,ss=seed();rec=consume(s,ss,who);e=projection(rec);note(snapshot=ss.material,receipt=rec,provider_trace=s.provider.trace,structural_trace=s.catalog.trace)
    assert e['state']=='PRODUCTIVE_TEST_ONLY' and [x['denominator'] for x in e['steps']]==[32,16,8]
    assert [cells(x) for x in e['steps']]==[{'1':18,'0':14},{'1':10,'0':6},{'1':6,'0':2}]
    assert all(x['uncertainty'] and x['evidence_ref'] and x['condition_witness_ref'] and x['provenance_refs'] for x in e['steps'])
    assert rec['material']['snapshot_ref']==ss.snapshot_hash and semantic_hash(rec['material'])==rec['receipt_hash']
    assert not rec['material']['operative_N9'] and not rec['material']['operative_N10W'] and not rec['material']['new_issuer']
    if who=='mother':
        assert all(x['feasibility']=='FEASIBLE_MODELED_PREMISE' and x['selection_weight'] is None for x in rec['material']['scenarios'])
        assert not any(rec['material'][x] for x in ['person_generation','actual_conception','relationships_generated'])
    else:assert rec['material']['route_probability'] is None

@pytest.mark.parametrize('valid,pub,expected',[('2027-09-01','2026-06-01',True),('2026-06-01','2027-09-01',True),('2027-09-01','2027-09-01',False)])
def test_both_asof_clocks_control_revision_independently(valid,pub,expected):
    s=GenericSelectedWorldService(structural_revision=True);ss=s.select(mode='AS_OF',valid_at=valid,published_asof=pub);v=s.structural(ss,'training_access','C0I');note(snapshot=ss.material,value=v)
    assert v['value'] is expected and ss.material['valid_at']==valid and ss.material['published_asof']==pub
    assert v['payload']['publication']<=pub and v['payload']['effective_from']<=valid<v['payload']['effective_to']

@pytest.mark.parametrize('valid,pub',[('2026-02-01','2026-02-01'),('2029-01-01','2029-01-01')])
@pytest.mark.parametrize('who',['nonparent','mother'])
def test_unavailable_clocks_cannot_become_positive_routes(valid,pub,who):
    s=GenericSelectedWorldService();ss=s.select(mode='AS_OF',valid_at=valid,published_asof=pub);out=consume(s,ss,who);note(snapshot=ss.material,receipt=out)
    m=out['material'];assert 'PARTIAL' in m['state']
    if who=='nonparent':assert m['structural_routes']['training']['state']=='UNAVAILABLE_AUTHORITY_OR_CLOCK'
    else:assert m['scenarios'][0]['feasibility']=='UNKNOWN_PREMISE'

@pytest.mark.parametrize('who',['nonparent','mother'])
def test_revoked_training_read_removes_only_its_dependent_routes(who):
    s,ss=seed();base=consume(s,ss,who);s.catalog.revoke('training_access');out=consume(s,ss,who);note(before=base,after=out)
    assert projection(base)==projection(out) and 'PARTIAL' in out['material']['state']
    if who=='nonparent':
        assert out['material']['structural_routes']['training']['state']=='UNAVAILABLE_AUTHORITY_OR_CLOCK'
        assert out['material']['structural_routes']['civil']==base['material']['structural_routes']['civil']
    else:
        assert out['material']['scenarios'][0]['feasibility']=='UNKNOWN_PREMISE'
        assert out['material']['scenarios'][1]==base['material']['scenarios'][1]

@pytest.mark.parametrize('who',['nonparent','mother'])
def test_empirical_revocation_is_not_zero_or_renormalization(who):
    s,ss=seed();base=consume(s,ss,who);s.catalog.revoke('empirical');out=consume(s,ss,who);note(before=base,after=out)
    assert projection(out)['state']=='REVOKED' and projection(out)['steps']==[]
    if who=='nonparent':assert out['material']['structural_routes']==base['material']['structural_routes']
    else:assert [x['feasibility'] for x in out['material']['scenarios']]==['FEASIBLE_MODELED_PREMISE']*2

@pytest.mark.parametrize('warm',[False,True])
@pytest.mark.parametrize('who',['nonparent','mother'])
def test_native_query_grant_loss_cannot_serve_fresh_cells(warm,who):
    s,ss=seed()
    if warm:consume(s,ss,who)
    w=s.provider.world;w['registry']=AuthorityRegistry([v for k,v in w['registry']._by_key.items() if k!=w['qauth'].authority_ref.key]);before=len(s.receipts)
    try:out=consume(s,ss,who)
    except Pre553AuthorityError as exc:note(refusal=str(exc),warm=warm);assert len(s.receipts)==before
    else:
        note(receipt=out,warm=warm);e=projection(out);assert e['state']!='PRODUCTIVE_TEST_ONLY' and all(not t['cells'] and not t.get('evidence_ref') for t in e['steps'])


def test_native_forward_and_separately_granted_reverse_have_distinct_denominators():
    s,ss=seed();forward=s.possibilities(ss,target='Y',conditions=(('A',1),),consumer='C0I')['steps'][0]
    reverse=s.possibilities(ss,target='A',conditions=(('Y',1),),consumer='C0I')['steps'][0]
    note(forward=forward,reverse=reverse)
    assert (forward['target'],forward['denominator'],cells(forward))==('Y',32,{'1':18,'0':14})
    assert (reverse['target'],reverse['denominator'],cells(reverse))==('A',29,{'1':18,'0':11})
    assert forward['producer_query_ref']!=reverse['producer_query_ref']

@pytest.mark.parametrize('target,conditions',[('A',(('Y',1),('B',1))),('B',(('Y',1),)),('HOUSEHOLD',(('A',1),)),('DYAD',(('A',1),)),('Y',(('Y',1),)),('Y',(('A',True),)),('Y',(('A',1),('A',0)))])
def test_unsupported_reverse_roles_household_dyad_and_mixed_identity_refuse(target,conditions):
    s,ss=seed();before=len(s.receipts)
    with pytest.raises(ValueError) as ex:s.possibilities(ss,target=target,conditions=conditions,consumer='C0I')
    note(target=target,conditions=conditions,refusal=str(ex.value));assert len(s.receipts)==before


def test_reverse_without_existing_separate_permit_refuses_while_forward_survives():
    w=build_source();del w['query_permits']['A'];p=GenericProgressiveProvider(w)
    with pytest.raises(ValueError):p.step('A',(('Y',1),))
    out=p.step('Y',(('A',1),));note(forward=out,reverse='ROLE_REFUSED');assert out['denominator']==32 and cells(out)['1']==18


def test_condition_order_is_preserved_not_sorted_away():
    s,ss=seed();a=s.possibilities(ss,conditions=(('A',1),('B',1),('C',1)));b=s.possibilities(ss,conditions=(('C',1),('B',1),('A',1)));note(ABC=a,CBA=b)
    assert a['steps'][0]['conditioners']==[['A',1]] and b['steps'][0]['conditioners']==[['C',1]]
    assert a['steps'][-1]['denominator']==b['steps'][-1]['denominator']==8
    assert a['steps'][-1]['condition_witness_ref']!=b['steps'][-1]['condition_witness_ref']

@pytest.mark.parametrize('who',['nonparent','mother'])
def test_null_support_remains_typed_with_no_invented_weight(who):
    s,ss=seed(support_loss=True);out=consume(s,ss,who);note(receipt=out);e=projection(out);t=e['steps'][-1]
    assert t['denominator']==0 and not t['cells'] and t['geometry'] is None and not t.get('evidence_ref')
    assert e['state']!='PRODUCTIVE_TEST_ONLY'
    if who=='mother':assert all(x['selection_weight'] is None for x in out['material']['scenarios'])
    else:assert out['material']['route_probability'] is None

@pytest.mark.parametrize('field',['cells','conditioners','permission_root','evidence_ref','uncertainty'])
def test_rehashed_cached_provenance_cannot_override_native_owner(field):
    s,ss=seed();s.possibilities(ss);key=('Y',(('A',1),));p=s.provider;entry=deepcopy(p.cache[key])
    if field=='cells':entry['cells'][0]['raw_numerator_support']=999
    elif field=='conditioners':entry[field]=[['B',1]]
    elif field=='evidence_ref':entry[field]={'kind':'FOREIGN','id':'OTHER','content_hash':'0'*64}
    else:entry[field]='FORGED'
    entry['content_hash']=semantic_hash({k:v for k,v in entry.items() if k!='content_hash'});p.cache[key]=entry
    with pytest.raises(ValueError,match='CACHE_PROJECTION_MISMATCH'):s.possibilities(ss)
    note(forged=entry)

@pytest.mark.parametrize('attack',['foreign_source','row_hash','model_rule','rehashed_snapshot','unregistered_snapshot'])
def test_source_and_snapshot_identity_refuse_coherent_outer_hashes(attack):
    s,ss=seed();s.possibilities(ss)
    if attack=='foreign_source':s.provider.world['source']['release_ref']=build_source(changed=True)['source']['release_ref']
    elif attack=='row_hash':s.provider.world['rows_hash']='F'*64
    elif attack=='model_rule':s.provider.world['model_rule']=build_source(changed=True)['model_rule']
    else:
        material=deepcopy(ss.material);material['fields']['training_access']['value']=False
        ss=SelectedSnapshot(material,semantic_hash(material) if attack=='rehashed_snapshot' else '0'*64)
    with pytest.raises((ValueError,KeyError)) as ex:s.possibilities(ss)
    note(attack=attack,refusal=str(ex.value))

@pytest.mark.parametrize('field,value',[('father','PERSON'),('partner_actor','PERSON'),('household',{}),('dyad',{}),('weight',0.25),('psychological_memory',[])])
def test_mother_input_refuses_unissued_people_joints_psyche_weights(field,value):
    s,ss=seed();before=(len(s.value_reads),len(s.receipts));proposal=dict(scenario_id='MOTHER',route='institutional',**{field:value})
    with pytest.raises(ValueError):scenario.evaluate(s,ss,[proposal])
    note(proposal=proposal,before=before,after=(len(s.value_reads),len(s.receipts)));assert (len(s.value_reads),len(s.receipts))==before


def test_changed_empirical_version_changes_source_not_unrelated_structural_truth():
    a,sa=seed();b,sb=seed(empirical_changed=True);aa=nonparent.consume(a,sa);bb=nonparent.consume(b,sb);note(base=aa,changed=bb)
    assert aa['material']['structural_routes']==bb['material']['structural_routes']
    x=projection(aa)['steps'][-1];y=projection(bb)['steps'][-1]
    assert (cells(x)['1'],cells(y)['1'])==(6,7) and x['denominator']==y['denominator']==8
    assert x['release_ref']!=y['release_ref'] and x['source_universe_ref']!=y['source_universe_ref']


def test_port_runtime_binding_uses_actual_imported_native_module_tree():
    p=port_module(relocate=False)
    note(declared_runtime=str(p.RUNTIME),actual_runtime='staging/runtime',nonparent_module_file=str(Path(nonparent.__file__).relative_to(R)))
    assert p.RUNTIME.resolve()==Path(nonparent.__file__).resolve().parent.parent,'Hardcoded /tmp path is not the fresh imported native runtime'


def test_port_relocation_preserves_exact_original_consumers_and_values():
    p=port_module();port=p.TwoContractPort();ss=port.select(valid_at='2027-09-01',published_asof='2027-09-01');a=port.consume_nonparent(ss);b=port.consume_conception_proposals(ss,[dict(scenario_id='M',route='institutional')]);note(nonparent=a.as_dict(),mother=b.as_dict(),dispatched=port.dispatched)
    assert a.owner_receipt_hash==semantic_hash(a.owner_payload) and b.owner_receipt_hash==semantic_hash(b.owner_payload)
    assert a.owner_receipt_hash!=b.owner_receipt_hash and a.bound_snapshot_ref==b.bound_snapshot_ref==ss.snapshot_hash
    for rec,mod in [(a,nonparent),(b,scenario)]:
        raw=Path(mod.__file__).read_bytes();assert rec.lineage['producer_blob']==__import__('hashlib').sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()


def test_facade_exposes_two_distinct_owner_contract_receipts_not_two_N9_clients():
    p=port_module();port=p.TwoContractPort();ss=port.select(valid_at='2027-09-01',published_asof='2027-09-01');a=port.consume_nonparent(ss);b=port.consume_conception_proposals(ss,[dict(scenario_id='M',route='institutional')]);note(A=a.as_dict(),B=b.as_dict())
    assert {a.contract,b.contract}=={port.CONTRACT_N9,port.CONTRACT_N10},'Two consumer hashes do not demonstrate two separately exposed owner contracts'


def test_facade_receipt_roundtrips_frozen_SC0_envelope_not_only_a_consumer_hash():
    p=port_module();port=p.TwoContractPort();ss=port.select(valid_at='2027-09-01',published_asof='2027-09-01');out=port.consume_nonparent(ss).as_dict()
    schema=json.loads((R/'staging/oracles/sc0/01_envelope.json').read_text());requirements=schema['$defs']['WorldReceipt']['required'];missing=sorted(set(requirements)-set(out));note(receipt=out,missing_fields=missing,expected_contract='GENERIC_WORLD_SELECTION@1.0.0')
    assert not missing and out['contract']=='GENERIC_WORLD_SELECTION@1.0.0','Claimed literal SC0 envelope is not provided'
