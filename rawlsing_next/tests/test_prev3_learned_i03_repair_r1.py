from rawlsing_next import prev3_learned_i03_repair_r1 as i02
from rawlsing_next import prev3_learned_real_execution_r2 as g02


def test_exact_source_and_authority_identities_are_frozen():
    assert i02.SOURCE_SHA256 == "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
    assert i02.D02_FRONTIER_GIT_BLOB == "5399a3f64642c8d9f8a0644db0adc15d38642971"
    assert i02.F02_FRONTIER_READOPTION_HASH == "07c6175b1d3828f8dc8763c51f3eb44a3cba6812bb128d4f0b84ffc5096cb851"
    assert i02.CANONICAL_I03_BLOB == "e2d91984541df7c692a1b2f32370500838a2a000"
    assert i02.AS2B_ACCEPTED_COMMIT == "923f2c00b6145182a5e2be5038f579845951da19"


def test_frozen_frontier_is_still_exact_50_candidates_77_roles():
    f=i02.frontier()
    assert len(f)==50
    assert sum(len(c["roles"]) for c in f)==77
    assert {c["lane"] for c in f}=={"P0","P1","P2","P3","P4"}


def test_i02_lane_membership_matches_frozen_d02_g02_counts():
    f=i02.frontier()
    expected={"P0":(5,5),"P1":(1,3),"P2":(18,36),"P3":(1,8),"P4":(25,25)}
    for lane,(nc,nr) in expected.items():
        members=[c for c in f if c["lane"]==lane]
        assert len(members)==nc
        assert sum(len(c["roles"]) for c in members)==nr
    g=g02.compile_frontier()
    assert g["preexecution_frontier_seal_hash"]==i02.G02_PREEXECUTION_SEAL


def test_i02_p2_membership_is_exact_same_2x3x3_cartesian_grid():
    ids={c["id"] for c in i02.frontier() if c["lane"]=="P2"}
    assert ids=={f"P2:{a}:{b}:{c}" for a in (1,5) for b in (1,2,3) for c in (1,2,3)}


def test_i02_p4_membership_is_exact_same_5x5_grid():
    ids={c["id"] for c in i02.frontier() if c["lane"]=="P4"}
    assert ids=={f"P4:{a}:{b}" for a in range(1,6) for b in range(1,6)}


def test_source_specific_special_codes_are_not_reinterpreted():
    assert i02.q301_state(6)==("SOURCE_SPECIFIC_SPECIAL",6)
    assert i02.q301_state(7)==("SOURCE_SPECIFIC_SPECIAL",7)
    assert i02.q301_state(None)==("SYSTEM_MISSING",None)
    for x in range(1,6):
        assert i02.q301_state(x)==("SUBSTANTIVE_RESPONSE",x)


def test_canonical_i03_partial_target_resolution_is_unresolved():
    records=[
        {"q301_2":1,"q301_7":1,"q310":1,"q311":1},
        {"q301_2":6,"q301_7":1,"q310":1,"q311":1},
        {"q301_2":7,"q301_7":1,"q310":1,"q311":1},
        {"q301_2":None,"q301_7":1,"q310":1,"q311":1},
    ]
    r=i02.query(records,"q301_2",["A000"])
    assert r["state"]=="UNRESOLVED"
    assert (r["denominator"],r["resolved"],r["unresolved"])==(4,1,3)
    assert r["unresolved_states"]=={"SOURCE_SPECIFIC_SPECIAL:6":1,"SOURCE_SPECIFIC_SPECIAL:7":1,"SYSTEM_MISSING":1}


def test_joint_resolution_requires_both_q301_components_resolved():
    records=[
        {"q301_2":1,"q301_7":5,"q310":1,"q311":1},
        {"q301_2":1,"q301_7":6,"q310":1,"q311":1},
        {"q301_2":7,"q301_7":5,"q310":1,"q311":1},
    ]
    r=i02.query(records,"joint",["A000"])
    assert r["state"]=="UNRESOLVED"
    assert (r["denominator"],r["resolved"],r["unresolved"])==(3,1,2)
    assert r["cells"]["1,5"]==1


def test_full_target_resolution_is_supported_without_recode():
    records=[
        {"q301_2":1,"q301_7":2,"q310":1,"q311":1},
        {"q301_2":5,"q301_7":4,"q310":1,"q311":1},
    ]
    r=i02.query(records,"q301_7",["A000"])
    assert r["state"]=="SUPPORTED"
    assert (r["denominator"],r["resolved"],r["unresolved"])==(2,2,0)


def test_negative_ceiling_preserved_and_no_result_selection_surface_added():
    assert "NO_STRUCTURAL_ADMISSION" in i02.NEGATIVE_CEILING
    assert "NO_CAUSAL_PROMOTION" in i02.NEGATIVE_CEILING
    assert "NO_POPULATION_GENERALIZATION" in i02.NEGATIVE_CEILING
    assert "NO_PERSON_STATE" in i02.NEGATIVE_CEILING
    assert "NO_V3" in i02.NEGATIVE_CEILING
