"""R4 D2R independent executable core: exact D2P producer vs N9C consumer refs.
Prereqs: byte-verified D2P external_fields.py and n9c_reader.py + n9c_fields.json.
No source issuance, real OC05 or actor use.
"""
from copy import deepcopy
from pathlib import Path
import json
from d2p.external_fields import GSS, NCA, produce_two_fields
from d2p.n9c_reader import TestOnlyRegistry, read_historical_test_only, TestOnlyReadError

rows = deepcopy(json.loads((Path(__file__).resolve().parents[1]/'n9c_fields.json').read_text())['fields'])
fields = produce_two_fields(rows)
registry = TestOnlyRegistry(rows)
reader_refs = registry.refs_by_role()
producer_refs = {role: fields[role]['field_ref'] for role in (GSS,NCA)}
relation = {'kind':'TEST_ONLY_NONPOOLED_COPRESENCE','fixture_only':True,
            'issued_EE13':False,'ordered_refs':[reader_refs[GSS],reader_refs[NCA]],
            'population_join':False}
receipt = read_historical_test_only(registry,selected_refs=reader_refs,
    relation=relation,as_of='2022-07-08',clock_mode='HISTORICAL_PUBLICATION_AWARE')
errors={}
for role in (GSS,NCA):
    try: registry.dereference(producer_refs[role])
    except TestOnlyReadError as error: errors[role]=error.code
assert receipt['state']=='TWO_VALUES_READ_TEST_ONLY'
assert receipt['dependency_readset']==[reader_refs[GSS],reader_refs[NCA]]
assert set(producer_refs.values()).isdisjoint(reader_refs.values())
assert errors=={GSS:'UNKNOWN_EXACT_FIELD_REF',NCA:'UNKNOWN_EXACT_FIELD_REF'}
print(json.dumps({'disposition':'RED_EXACT_PRODUCER_FIELD_REF_NOT_DOWNSTREAM_DEREFERENCED',
    'producer_refs':producer_refs,'downstream_refs':reader_refs,
    'downstream_readset':receipt['dependency_readset'],
    'direct_producer_dereference_errors':errors,'numbers_read_from_parallel_rows':{
        row['role']:row['values'] for row in receipt['values_read']},
    'issued_N5N6':False,'issued_EE13':False,'operative_OC05':False},indent=2,sort_keys=True))
