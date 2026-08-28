from __future__ import annotations
import copy, json
import pytest
from data.ddm_build_copy import validate_v550j_b08_source_family_authority as v

def test_b08_serializations_fail_closed_and_validate_exact_independent_scope():
    receipt=v.validate_all()
    assert receipt["status"]=="PASS_BLOCKED_SERIALIZATION_FAILS_CLOSED"
    assert receipt["r14_evidence_rows"]==73
    assert receipt["production_executable_registries"]==0
    assert receipt["denominator_disposition_complete"] is False

def test_asian_w6_is_explicitly_excluded_and_never_eligible():
    a=v.load_registry(v.ASIAN)
    assert a["eligible_waves"]==["W1","W4","W5"]
    assert "W6" not in a["eligible_waves"]
    assert a["explicitly_excluded_waves"]==[{
        "wave":"W6",
        "disposition":"EXCLUDED_BY_GOVERNING_CLOSED_35_SCOPE_LAW",
        "source_scope_authority_blob":"83f99e22fe1275794e9ded3d7720f4a6d1bcf530",
    }]

def test_latin_exact_independent_wave_scope_is_preserved():
    l=v.load_registry(v.LATIN)
    assert l["eligible_waves"]==["1995","2011","2024"]
    assert l["source_specific_cautions"][0]["wave"]=="2024"

def test_aggregate_2499_15990_never_becomes_exact_row_authority():
    for path in (v.ASIAN,v.LATIN):
        d=v.load_registry(path)
        den=d["recovery_adjudication_denominator"]
        assert (den["global_source_structure_count"],den["global_membership_count"])==(2499,15990)
        assert den["exact_b08_source_family_row_partition_materialized_on_start_surface"] is False
        assert d["denominator_disposition_complete"] is False
        assert d["admitted_product_configurations"]==[]

def test_missing_routing_dependency_never_becomes_execution_authority():
    for path in (v.ASIAN,v.LATIN):
        d=v.load_registry(path)
        assert d["routing_dependency"]["b02_b05_consumed"] is False
        assert d["routing_dependency"]["product_execution_authorized"] is False
        assert d["production_executable_registry"] is False

def test_bounded_canaries_are_preserved_but_not_promoted():
    a=v.load_registry(v.ASIAN); l=v.load_registry(v.LATIN)
    assert a["bounded_existing_governed_canary"]["registry_blob"]=="68a85a4da8d702bdf39719f0b461f66cc3bd8909"
    assert l["bounded_existing_governed_canary"]["registry_blob"]=="74eac8d8814514a1acd20eb6c48cecf7ea62e01a"
    assert a["bounded_existing_governed_canary"]["disposition"].endswith("NOT_PROMOTED_TO_PRODUCT_SCOPE")
    assert l["bounded_existing_governed_canary"]["disposition"].endswith("NOT_PROMOTED_TO_PRODUCT_SCOPE")

def test_archive08_and_v3_architecture_promotion_are_absent():
    for path in (v.ASIAN,v.LATIN):
        d=v.load_registry(path)
        assert d["archive08_promotion"] is False
        assert d["v3_effect"] is False
        assert d["architecture_selection"] is False

def test_hostile_w6_widening_is_rejected_by_validator(tmp_path,monkeypatch):
    data=json.loads(v.ASIAN.read_text())
    data["eligible_waves"].append("W6")
    p=tmp_path/"asian.json"; p.write_text(json.dumps(data),encoding="utf-8")
    monkeypatch.setattr(v,"ASIAN",p)
    with pytest.raises(v.B08AuthoritySerializationError,match="Asian exact CLOSED_35 scope drift|W6"):
        v.validate_all()

def test_hostile_false_executability_is_rejected(tmp_path):
    data=json.loads(v.LATIN.read_text())
    data["production_executable_registry"]=True
    p=tmp_path/"latin.json"; p.write_text(json.dumps(data),encoding="utf-8")
    with pytest.raises(v.B08AuthoritySerializationError,match="may not become executable authority"):
        v.load_registry(p)
