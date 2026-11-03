"""R4 D2R deliberately strict acceptance oracles: real RED expected against pinned code.
These are NOT xfails; run separately to preserve failing stdout/JUnit."""
from copy import deepcopy
from pathlib import Path
import json
import pytest
from d2p.external_fields import GSS,NCA,produce_two_fields,field_content_ref,FieldProducerError
from d2p.n9c_reader import TestOnlyRegistry,TestOnlyReadError,read_historical_test_only


def rows():return deepcopy(json.loads((Path(__file__).resolve().parents[1]/'n9c_fields.json').read_text())['fields'])


def read_produced_refs(fields,reg):
    selected={x:fields[x]['field_ref'] for x in (GSS,NCA)}
    relation={'kind':'TEST_ONLY_NONPOOLED_COPRESENCE','fixture_only':True,'issued_EE13':False,
              'ordered_refs':[selected[GSS],selected[NCA]],'population_join':False}
    return read_historical_test_only(reg,selected_refs=selected,relation=relation,
             as_of='2022-07-08',clock_mode='HISTORICAL_PUBLICATION_AWARE')


def test_RED01_exact_D2P_field_refs_must_dereference_in_downstream_registry():
    x=rows(); fields=produce_two_fields(x);reg=TestOnlyRegistry(x)
    # Real result: BOTH UNKNOWN_EXACT_FIELD_REF; test demands successful values-read.
    got=read_produced_refs(fields,reg)
    assert got['state']=='TWO_VALUES_READ_TEST_ONLY'
    assert got['values_read'][0]['values']['numerator']==2388192


def test_RED02_downstream_dependency_readset_must_bind_original_producer_refs():
    x=rows();fields=produce_two_fields(x);reg=TestOnlyRegistry(x)
    selected=reg.refs_by_role()
    relation={'kind':'TEST_ONLY_NONPOOLED_COPRESENCE','fixture_only':True,'issued_EE13':False,
              'ordered_refs':[selected[GSS],selected[NCA]],'population_join':False}
    got=read_historical_test_only(reg,selected_refs=selected,relation=relation,
                                 as_of='2022-07-08',clock_mode='HISTORICAL_PUBLICATION_AWARE')
    assert got['dependency_readset']==[fields[GSS]['field_ref'],fields[NCA]['field_ref']]


def test_RED03_exported_field_content_ref_must_refuse_stale_tampered_payload():
    x=rows();p=produce_two_fields(x)[GSS];old=p['field_ref']
    p['values']['numerator'] += 1
    # Real field_content_ref is merely `return field['field_ref']`.
    with pytest.raises(FieldProducerError):
        field_content_ref(p)
    assert p['field_ref']==old


def test_RED04_reader_must_refuse_forged_issuer_signature():
    x=rows();x[0]['issuer_signature']='FAKE_REAL_ISSUER'
    # D2P rejects this, but N9C source registry currently ignores issuer_signature.
    with pytest.raises(TestOnlyReadError):
        TestOnlyRegistry(x)


def test_RED05_reader_must_refuse_fake_native_electricity_subtype_label():
    x=rows();parts=x[0]['values']['electricity_subtypes']
    parts['hydro_turbine']=parts.pop('wind')
    # Same sum and five keys but false native measure label.
    with pytest.raises(TestOnlyReadError):
        TestOnlyRegistry(x)


def test_RED06_d2p_field_producer_must_check_native_source_unit_before_producing():
    x=rows();x[1]['native_unit']='PERSON_WITH_MOBILE_DATA'
    # D2P producer check covers authority/clocks only; N9C independent reader refuses.
    with pytest.raises(FieldProducerError):
        produce_two_fields(x)


def test_RED07_downstream_reader_must_refuse_fake_source_publisher_identity():
    x=rows();x[0]['publisher']='Invented Census Foundation'
    with pytest.raises(TestOnlyReadError):
        TestOnlyRegistry(x)
