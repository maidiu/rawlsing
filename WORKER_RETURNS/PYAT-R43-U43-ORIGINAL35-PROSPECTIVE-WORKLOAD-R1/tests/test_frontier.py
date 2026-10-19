from copy import deepcopy
import pytest
import build_frontier as b


@pytest.fixture(scope="module")
def product():
    return b.build()


def test_independent_full_research_identity_union_and_wave_denominator(product):
    items,waves,packets,inactive=product
    assert len(items)==18285 and len(waves)==35 and len(inactive)==259
    assert b.verify_no_drop(items)["missing"]==0
    assert sum(w["research_identity_count"] for w in waves)==18285
    assert sum(len(p["demands"]) for p in packets)==175
    assert all(w["eligible_E_pre_count"] is None and not w["permitted_native_execution_manifests"] for w in waves)


@pytest.mark.parametrize("attack",["drop","replace","role","form","country","permission"])
def test_full_identity_no_drop_is_payload_and_multiset_not_cardinality(product,attack):
    original=product[0];items=deepcopy(original)
    if attack=="drop":items.pop()
    elif attack=="replace":items[-1]=deepcopy(items[0])
    else:items[0][{"role":"inherited_role","form":"retained_response_form","country":"country_scope_as_recorded","permission":"status"}[attack]]="FORGED"
    with pytest.raises(ValueError,match="EXACT_NO_DROP_ASSERTION"):
        b.verify_no_drop(items,original)


def test_no_research_union_self_issuance_or_country_pooling(product):
    items,waves,packets,inactive=product
    assert all(i["eligible_operation_ids"] is None for i in items)
    assert all(i["source_native_occurrence_and_form"] is None for i in items)
    assert all(w["current_source_access_permission"] is None for w in waves)
    assert all(p["competent_issuer_identity"] is None for p in packets)
    assert {i["status"] for i in items}=={"NOT_YET_ISSUED"}
