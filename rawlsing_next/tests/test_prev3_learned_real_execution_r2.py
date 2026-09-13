from rawlsing_next import prev3_learned_real_execution_r2 as g02


def qresult(den, counts):
    return {"raw_denominator_support":den,"complete_cell_counts":{str(k):v for k,v in counts.items()}}


def test_frontier_is_exact_50_candidates_77_roles():
    c=g02.compile_frontier()
    assert len(c["frontier"])==50
    assert sum(len(x["query_roles"]) for x in c["frontier"])==77
    assert len({x["execution_candidate_hash"] for x in c["frontier"]})==50


def test_lane_membership_counts_are_frozen():
    c=g02.compile_frontier()["frontier"]
    for lane,exp in g02.LANE_EXPECTATIONS.items():
        members=[x for x in c if x["lane"]==lane]
        assert len(members)==exp["candidate_count"]
        assert sum(len(x["query_roles"]) for x in members)==exp["query_role_count"]


def test_f02_selector_roots_are_exact_and_complete():
    for q in ("q310","q311"):
        assert sum(g02.EXPECTED_F02_SCAN[q]["counts"].values())==g02.SOURCE_ROWS
        assert set(g02.EXPECTED_F02_SCAN[q]["selector_roots"])=={"1","2","3","MISSING"}


def test_p2_has_exact_2x3x3_membership_no_more_no_less():
    p2=[x for x in g02.compile_frontier()["frontier"] if x["lane"]=="P2"]
    params={(x["parameters"]["q301_2"],x["parameters"]["q310"],x["parameters"]["q311"]) for x in p2}
    assert params=={(a,b,c) for a in (1,5) for b in (1,2,3) for c in (1,2,3)}
    assert all(len(x["query_roles"])==2 for x in p2)


def test_p3_is_exact_eight_role_q310_reversal_grid():
    p3=[x for x in g02.compile_frontier()["frontier"] if x["lane"]=="P3"][0]
    roles={x["role"] for x in p3["query_roles"]}
    assert roles=={"POOLED_POS","POOLED_NEG","STRATUM:Q310V1:POS","STRATUM:Q310V1:NEG","STRATUM:Q310V2:POS","STRATUM:Q310V2:NEG","STRATUM:Q310V3:POS","STRATUM:Q310V3:NEG"}
    assert p3["validation"]=={"kind":"CONDITIONAL_REVERSAL","target_cell":{"$exact_decimal":"5"}}


def test_target_cell_support_validator():
    c={"validation":{"kind":"TARGET_CELL_SUPPORTED","target_cell":{"$exact_decimal":"3"}}}
    state,detail=g02._validate(c,{"BASE":qresult(10,{1:1,2:0,3:2,4:0,5:0})})
    assert state=="EVALUATED_SUPPORTED" and detail["target_support"]==2
    state,_=g02._validate(c,{"BASE":qresult(10,{1:1,2:0,3:0,4:0,5:0})})
    assert state=="EVALUATED_VALID_EMPTY"


def test_distribution_difference_is_exact_fraction_cross_multiplication():
    c={"validation":{"kind":"DISTRIBUTION_DIFFERS_FROM_BASELINE"}}
    state,_=g02._validate(c,{"CONDITION":qresult(10,{1:5,2:5,3:0,4:0,5:0}),"BASELINE":qresult(20,{1:10,2:10,3:0,4:0,5:0})})
    assert state=="EVALUATED_VALID_EMPTY"
    state,_=g02._validate(c,{"CONDITION":qresult(10,{1:6,2:4,3:0,4:0,5:0}),"BASELINE":qresult(20,{1:10,2:10,3:0,4:0,5:0})})
    assert state=="EVALUATED_SUPPORTED"


def test_joint_dependence_exact_validator():
    c={"validation":{"kind":"JOINT_NOT_PRODUCT_OF_MARGINALS"}}
    roles={"JOINT":qresult(100,{f"{a},{b}":(40 if (a,b)==(1,1) else 0) for a in range(1,6) for b in range(1,6)}),"MARGINAL_0":qresult(100,{1:50,2:0,3:0,4:0,5:0}),"MARGINAL_1":qresult(100,{1:50,2:0,3:0,4:0,5:0})}
    state,detail=g02._validate(c,roles)
    assert state=="EVALUATED_SUPPORTED"
    assert detail["first_exact_dependence_witness"]["cell"]==[1,1]


def test_conditional_reversal_requires_opposite_common_nonzero_stratum_sign():
    c={"validation":{"kind":"CONDITIONAL_REVERSAL","target_cell":{"$exact_decimal":"5"}}}
    roles={"POOLED_POS":qresult(10,{5:8}),"POOLED_NEG":qresult(10,{5:2})}
    for s in (1,2,3):
        roles[f"STRATUM:Q310V{s}:POS"]=qresult(10,{5:7}); roles[f"STRATUM:Q310V{s}:NEG"]=qresult(10,{5:3})
    state,detail=g02._validate(c,roles)
    assert state=="EVALUATED_VALID_EMPTY" and detail["pooled_sign"]==1 and detail["stratum_signs"]==[1,1,1]
    for s in (1,2,3):
        roles[f"STRATUM:Q310V{s}:POS"]=qresult(10,{5:2}); roles[f"STRATUM:Q310V{s}:NEG"]=qresult(10,{5:8})
    state,detail=g02._validate(c,roles)
    assert state=="EVALUATED_SUPPORTED" and detail["stratum_signs"]==[-1,-1,-1]


def test_negative_ceiling_and_no_selection_surface():
    inv=g02.compile_frontier()["preexecution_frontier_seal"]["invariants"]
    assert inv["pruning_contract"]=={"kind":"NONE_EXACT_EVALUATE_ALL"}
    assert inv["rng_policy"]=="NONE" and inv["score_or_top_k"]=="FORBIDDEN"
    assert inv["post_data_frontier_mutation"]=="FORBIDDEN"
    assert "NO_PERSON_STATE" in g02.NEGATIVE_CEILING and "NO_V3" in g02.NEGATIVE_CEILING


def test_frontier_compilation_is_deterministic():
    a=g02.compile_frontier(); b=g02.compile_frontier()
    assert a==b
    assert a["preexecution_frontier_seal_hash"]==b["preexecution_frontier_seal_hash"]
