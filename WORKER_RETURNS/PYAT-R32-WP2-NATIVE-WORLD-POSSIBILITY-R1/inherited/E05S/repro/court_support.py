import pathlib,json,copy,hashlib
import e05_n9_selected_world_adapter as E
from product.service import GenericSelectedWorldService
from product.nonparent import consume
from product.scenario import evaluate
from rawlsing_next.pre553_hq297_n9c_two_field_reader import TestOnlyRegistry,GSS,NCA,read_historical_test_only
ROOT=pathlib.Path(__file__).resolve().parents[1];RT=ROOT/'runtime';O=ROOT/'observations';O.mkdir(exist_ok=True)
FIX=RT/'WORKER_RETURNS/PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1/02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json'
PROPOSALS=[dict(scenario_id='INDEPENDENT_TRAINING',route='institutional'),dict(scenario_id='INDEPENDENT_CIVIL',route='civil')]
def rows():return json.loads(FIX.read_text())['fields']
def adapter(data=None,**kw):return E.N9SelectedWorldAdapter(service=GenericSelectedWorldService(**dict(structural_revision=True,**kw)),registry=TestOnlyRegistry(rows() if data is None else data))
def clients(a,s):return [consume(a.service,s)['material'],evaluate(a.service,s,PROPOSALS)['material']]
def run(a=None,label='CURRENT_TEST_CLOCK',request=None):
 a=adapter() if a is None else a;q=request or E.standard_request(label=label);s=a.build_snapshot(q);acc=a.accept(q,s);cs=clients(a,s);r=a.serve(q,acc,s,consumers=cs);return a,q,s,acc,r
def save(name,data):
 (O/(name+'.json')).write_text(json.dumps(data,indent=2,default=str)+'\n')
def count(r):return [(next(c['raw_numerator_support'] for c in s['cells'] if c['cell']=='1'),s['denominator']) for s in r['empirical_steps']]
def native(r):return {v['role']:v for v in r['native_field_readset']['values_read']}
def fresh_read(reg,asof='2027-09-01'):
 refs=reg.refs_by_role();return read_historical_test_only(reg,selected_refs=refs,relation=dict(kind='TEST_ONLY_NONPOOLED_COPRESENCE',fixture_only=True,issued_EE13=False,population_join=False,ordered_refs=[refs[GSS],refs[NCA]]),as_of=asof,clock_mode='HISTORICAL_PUBLICATION_AWARE',partial_allowed=True)
def integrity(r):
 x=copy.deepcopy(r);payload=x.pop('receipt_payload_sha256');assert hashlib.sha256(E._canonical(x).encode()).hexdigest()==payload
 h=x.pop('receipt_hash');assert E.semantic_hash(E._float_free(x))==h
