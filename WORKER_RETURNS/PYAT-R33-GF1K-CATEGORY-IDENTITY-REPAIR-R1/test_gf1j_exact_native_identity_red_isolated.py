"""Two independently executed strict RED hostiles on exact GF1H code.
Uses non-authoritative small fixture adapter. Original producer acceptance is still HOLD.
"""
import pytest
from generic_native_pair_relation import build,semantic_hash,PREFIX
from gf1_pair_support_consumer import compute_pair_support_signature as consume

def corrupt_role(kind):
    r=build(cells=(1,0,0,1),eligible=2)
    rows=[dict(v) for v in r.conditional_count_profile]
    if kind=='conditioner':
        rows[0]['condition_state']=0
    else:
        cells=[dict(x) for x in rows[0]['target_counts']]
        cells[0]['target_state']=0
        rows[0]['target_counts']=tuple(cells)
    r.conditional_count_profile=tuple(rows)
    h=semantic_hash(r.semantic_projection());r.content_hash=h;r.object_id=PREFIX+h
    return r

@pytest.mark.parametrize('kind',['conditioner','target'])
def test_no_native_category_coercion_into_false_exact(kind):
    r=corrupt_role(kind)
    got=consume(r)
    assert got['decision_state']=='CONSUMER_RELATION_INTEGRITY_REJECTED',got
    assert got['separation_class'] is None,got
    assert got['downstream_value_produced'] is False,got
