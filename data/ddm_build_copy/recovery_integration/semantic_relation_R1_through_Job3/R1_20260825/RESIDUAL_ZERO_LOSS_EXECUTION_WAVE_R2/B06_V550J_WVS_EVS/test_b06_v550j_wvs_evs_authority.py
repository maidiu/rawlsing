import copy, hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent

def load():
    return json.loads((HERE/"B06_SERIALIZATION_MANIFEST.json").read_text())

def verify_hash(m):
    x=dict(m); supplied=x.pop("manifest_content_hash")
    got=hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
    assert got==supplied

def test_exact_source_serializations():
    m=load(); verify_hash(m)
    assert m["production_completeness_claim"]=="NO_PRODUCTION_COMPLETENESS_CLAIM"
    d={x["source_family"]:x for x in m["sources"]}
    assert d["WVS"]["git_blob"]=="e4f303fc2e4967d6a48e8e457c27adf213d85d7a"
    assert d["WVS"]["admitted_members"]==["V22","V24"]
    assert d["EVS"]["git_blob"]=="12b9bed71f203464cf48b6d52cb32af6a3358428"
    assert d["EVS"]["admitted_members"]==["v471","v472","v514","v517"]

def test_denominator_remains_non_authority():
    m=load(); d=m["global_recovery_denominator"]
    assert (d["source_structures"],d["memberships"])==(2499,15990)
    assert d["per_source_raw_row_carrier_on_start"]=="NOT_MATERIALIZED"
    assert "NOT_EXECUTABLE_AUTHORITY" in d["authority_effect"]
    assert all(x["remaining_raw_candidate_count"] is None for x in m["sources"])

def test_routing_and_member_applicability_remain_blocked():
    m=load()
    assert all(x["live_routing_member_applicability"]=="BLOCKED__B02_B05_NOT_CONSUMED" for x in m["sources"])
    assert "NO_IMPLICIT_ROUTING_OR_MEMBER_APPLICABILITY" in m["negative_ceiling"]

def test_mutation_cannot_claim_completeness():
    m=load()
    bad=copy.deepcopy(m); bad["production_completeness_claim"]="PRODUCTION_COMPLETE"
    assert bad["production_completeness_claim"]!="NO_PRODUCTION_COMPLETENESS_CLAIM"
    try: verify_hash(bad)
    except AssertionError: pass
    else: raise AssertionError("mutated completeness retained sealed identity")
