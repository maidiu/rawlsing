#!/usr/bin/env python3
import pandas as pd
import pytest
from v552j_strata_horizon_sidecar_adapter_v2 import FIELDS, enrich, enrich_with_report, select_join_key

def sidecar(rows):
    out=[]
    for r in rows:
        z={f:'' for f in FIELDS}; z.update(r); out.append(z)
    return pd.DataFrame(out)

def test_basic_match_unmatched_and_statuses():
    p=pd.DataFrame([{'question_implementation_id':'q1','packet_id':'p1'},{'question_implementation_id':'q2','packet_id':'p2'}])
    o,rep=enrich_with_report(p,sidecar([{'question_implementation_id':'q1','stratum_id':'s1'}]))
    assert list(o.packet_id)==['p1','p2']
    assert o.loc[0,'stratum_id']=='s1'
    assert o.loc[0,'strata_horizon_sidecar_status']=='V552_AUTHORITATIVE_PASS_THROUGH_MATCHED'
    assert o.loc[1,'strata_horizon_sidecar_status']=='NO_V552_SIDECAR_MATCH'
    assert rep['matched_packet_rows']==1 and rep['unmatched_complete_packet_rows']==1

def test_blank_sidecar_key_fails():
    p=pd.DataFrame([{'question_implementation_id':'q1'}])
    with pytest.raises(ValueError,match='no safe supported join key'):
        enrich(p,sidecar([{'question_implementation_id':'','stratum_id':'bad'}]))

def test_blank_packet_keys_never_match():
    p=pd.DataFrame([{'question_implementation_id':'','packet_id':'a'},{'question_implementation_id':'q1','packet_id':'b'}])
    o=enrich(p,sidecar([{'question_implementation_id':'q1','stratum_id':'s1'}]))
    assert o.loc[0,'strata_horizon_sidecar_status']=='PACKET_JOIN_KEY_MISSING'
    assert pd.isna(o.loc[0,'stratum_id'])

def test_duplicate_sidecar_key_fails():
    p=pd.DataFrame([{'question_implementation_id':'q1'}]); s=sidecar([{'question_implementation_id':'q1'},{'question_implementation_id':'q1'}])
    with pytest.raises(ValueError,match='duplicate sidecar join keys'): enrich(p,s)

def test_missing_required_field_schema_fails():
    p=pd.DataFrame([{'question_implementation_id':'q1'}]); s=sidecar([{'question_implementation_id':'q1'}]).drop(columns=['horizon_type'])
    with pytest.raises(ValueError,match='missing required sidecar fields'): enrich(p,s)

def test_conflicting_nonempty_value_fails():
    p=pd.DataFrame([{'question_implementation_id':'q1','stratum_id':'left'}]); s=sidecar([{'question_implementation_id':'q1','stratum_id':'right'}])
    with pytest.raises(ValueError,match='conflicting non-empty values'): enrich(p,s)

def test_canonical_json_equality_is_not_conflict():
    p=pd.DataFrame([{'question_implementation_id':'q1','conditional_strata_weights':'{"a":1,"b":2}'}]); s=sidecar([{'question_implementation_id':'q1','conditional_strata_weights':'{"b": 2, "a": 1}'}])
    o=enrich(p,s); assert o.loc[0,'conditional_strata_weights']=='{"a":1,"b":2}'

def test_many_packet_rows_to_one_sidecar_row_is_allowed():
    p=pd.DataFrame([{'question_implementation_id':'q1','packet_id':'a'},{'question_implementation_id':'q1','packet_id':'b'}])
    o=enrich(p,sidecar([{'question_implementation_id':'q1','stratum_id':'s1'}])); assert list(o.stratum_id)==['s1','s1']

def test_packet_row_count_and_order_preserved():
    p=pd.DataFrame([{'question_implementation_id':'q2','packet_id':'2'},{'question_implementation_id':'','packet_id':'blank'},{'question_implementation_id':'q1','packet_id':'1'}])
    o=enrich(p,sidecar([{'question_implementation_id':'q1','stratum_id':'s1'},{'question_implementation_id':'q2','stratum_id':'s2'}]))
    assert len(o)==len(p) and list(o.packet_id)==['2','blank','1']

def test_composite_key_blank_sidecar_component_fails():
    p=pd.DataFrame([{'source':'GSS','wave':'1972','question_id':'q1'}])
    s=sidecar([{'source':'GSS','wave':'','question_id':'q1','stratum_id':'s1'}])
    with pytest.raises(ValueError,match='no safe supported join key'): enrich(p,s)

def test_composite_key_blank_packet_component_is_missing_not_match():
    p=pd.DataFrame([{'source':'GSS','wave':'','question_id':'q1'}])
    s=sidecar([{'source':'GSS','wave':'1972','question_id':'q1','stratum_id':'s1'}])
    # No packet row has a complete candidate key, so key selection fails rather than risk a blank join.
    with pytest.raises(ValueError,match='no safe supported join key'): enrich(p,s)

def test_key_preference_is_deterministic():
    p=pd.DataFrame([{'question_implementation_id':'q1','source':'GSS','wave':'1972','question_id':'x'}])
    s=sidecar([{'question_implementation_id':'q1','source':'GSS','wave':'1972','question_id':'x'}])
    assert select_join_key(p,s)==['question_implementation_id']

def test_matched_empty_sidecar_row_is_distinguished():
    p=pd.DataFrame([{'question_implementation_id':'q1'}]); o=enrich(p,sidecar([{'question_implementation_id':'q1'}]))
    assert o.loc[0,'strata_horizon_sidecar_status']=='V552_SIDECAR_MATCHED_NO_AUTHORITATIVE_VALUES'


def test_status_uses_sidecar_values_not_preexisting_packet_values():
    p = pd.DataFrame([{'question_implementation_id':'q1','stratum_id':'already-present'}])
    o = enrich(p, sidecar([{'question_implementation_id':'q1'}]))
    assert o.loc[0,'stratum_id'] == 'already-present'
    assert o.loc[0,'strata_horizon_sidecar_status'] == 'V552_SIDECAR_MATCHED_NO_AUTHORITATIVE_VALUES'


def test_python_list_structured_values_compare_canonically():
    p = pd.DataFrame([{'question_implementation_id':'q1','conditional_strata_weights':[{'b':2,'a':1}]}])
    s = sidecar([{'question_implementation_id':'q1','conditional_strata_weights':'[{"a":1,"b":2}]'}])
    o = enrich(p, s)
    assert o.loc[0,'conditional_strata_weights'] == [{'b':2,'a':1}]


def test_join_keys_are_trimmed_before_matching():
    p = pd.DataFrame([{'question_implementation_id':' q1 ','packet_id':'p1'}])
    o, rep = enrich_with_report(p, sidecar([{'question_implementation_id':'q1','stratum_id':'s1'}]))
    assert o.loc[0,'stratum_id'] == 's1'
    assert rep['key_normalization'] == 'TRIMMED_STRING_OR_CANONICAL_STRUCTURED_VALUE'


def test_duplicate_sidecar_keys_after_trimming_fail():
    p = pd.DataFrame([{'question_implementation_id':'q1'}])
    s = sidecar([{'question_implementation_id':'q1'}, {'question_implementation_id':' q1 '}])
    with pytest.raises(ValueError, match='duplicate sidecar join keys after canonical trimming'):
        enrich(p, s)
