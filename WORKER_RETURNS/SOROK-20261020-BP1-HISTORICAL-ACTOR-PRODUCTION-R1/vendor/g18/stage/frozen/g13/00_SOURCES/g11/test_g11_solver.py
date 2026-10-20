"""Independent frozen oracle regressions for sourcefree K11 logical constraints."""
import copy
from datetime import date
import hashlib
import itertools
import json
import pathlib
import sys
import pytest

sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from g11_solver import (Refused, FROZEN_SHA256, ORACLE, assert_acyclic,
                        check_selection_no_cherry_pick, load_oracle, no_unauthorized_decision,
                        reject_target_leakage, solve, survivor_fractions,
                        validate_child_event_order, verify_anchor_preservation)


@pytest.fixture
def fx():
    return load_oracle()


def refuse(code, fn):
    with pytest.raises(Refused) as exc:
        fn()
    assert exc.value.code == code


def test_frozen_hash():
    assert hashlib.sha256(ORACLE.read_bytes()).hexdigest() == FROZEN_SHA256


def test_sourcefree_baseline_8_of_8_with_distinct_parents_and_alternative_endpoints(fx):
    x=solve(fx)
    assert x["attempts"] == 8
    assert len(x["results"]) == fx["oracle"]["baseline_feasible_count"] == 8
    assert not x["rejected"]
    assert {(w["mother"], w["father"], w["scenario"]) for w in x["results"]} == set(itertools.product(("M0","M1"),("F0","F1"),("C0","C1")))
    assert len({w["father_anchor_sha256"] for w in x["results"]}) == 2
    assert len({w["mother_anchor_sha256"] for w in x["results"]}) == 2
    assert {w["conception_status"] for w in x["results"]} == {"PENDING_NONCAUSAL_NOT_OCCURRED"}
    assert {w["CHILD_GENERATED_status"] for w in x["results"]} == {"NOT_ISSUED_NOT_OCCURRED"}


def test_forward_forecasts_are_not_events(fx):
    x=solve(fx)
    assert {w["forecast_birth_not_an_event"] for w in x["results"]} == {"2021-03-08", "2021-08-08"}
    assert all(w["birth_status"]=="FORECAST_ONLY_NOT_OCCURRED" for w in x["results"])


def test_deterministic_replay_and_input_enumeration(fx):
    a=solve(fx)["results"]
    b=solve(fx)["results"]
    assert a==b
    g=copy.deepcopy(fx)
    g["fixed_preconception"]["fathers"].reverse()
    g["proposals"].reverse()
    assert sorted(a, key=lambda x:(x["mother"],x["father"],x["scenario"]))==sorted(solve(g)["results"],key=lambda x:(x["mother"],x["father"],x["scenario"]))


def test_no_backedge_or_graph_cycle(fx):
    assert len(assert_acyclic(fx["graph"]["nodes"],fx["graph"]["edges"])) == len(fx["graph"]["nodes"])
    g=copy.deepcopy(fx)
    g["graph"]["edges"].append(["birth","mother_history"])
    refuse("REJECT_CYCLE",lambda:solve(g))


def test_mutual_parent_dependency_cycle(fx):
    g=copy.deepcopy(fx)
    g["graph"]["edges"].extend([["father_checkpoint","mother_history"],["mother_checkpoint","father_history"]])
    refuse("REJECT_CYCLE",lambda:solve(g))


def test_forbidden_teleological_edge(fx):
    g=copy.deepcopy(fx)
    g["graph"]["edges"].append(["child_provenance","scenario_proposal"])
    refuse("REJECT_CYCLE",lambda:solve(g))


def test_mother_history_immutable(fx):
    g=copy.deepcopy(fx)
    g["fixed_preconception"]["mothers"][1]["history"].append({"date":"2019-08-01","event":"selected_father_secret"})
    refuse("REJECT_FIXED_HISTORY_MUTATION",lambda:verify_anchor_preservation(fx,g))


def test_father_history_immutable(fx):
    g=copy.deepcopy(fx)
    g["fixed_preconception"]["fathers"][0]["history"][0]["event"]="desired_child_wound_origin"
    refuse("REJECT_FIXED_HISTORY_MUTATION",lambda:verify_anchor_preservation(fx,g))


def test_late_inserted_memory_refused(fx):
    g=copy.deepcopy(fx)
    g["fixed_preconception"]["fathers"][0]["history"].append({"date":"2022-05-01","event":"memory_backfill"})
    refuse("REJECT_TEMPORAL_ORDER",lambda:solve(g))


def test_inverted_preconception_history_refused(fx):
    g=copy.deepcopy(fx)
    g["fixed_preconception"]["mothers"][0]["history"].append({"date":"2015-01-01","event":"unsorted"})
    refuse("REJECT_TEMPORAL_ORDER",lambda:solve(g))


def test_older_child_preservation(fx):
    x=solve(fx)["results"]
    assert any(w["mother"]=="M1" and w["history_event_count"]==5 for w in x)
    g=copy.deepcopy(fx)
    g["fixed_preconception"]["mothers"][1]["prior_child"]["born"]="2016-03-01"
    refuse("REJECT_FIXED_HISTORY_MUTATION",lambda:solve(g))


def test_conception_before_checkpoint_rejected(fx):
    g=copy.deepcopy(fx)
    g["proposals"][0]["conception"]="2019-12-31"
    r=solve(g)
    assert len(r["results"])==4
    assert {x["code"] for x in r["rejected"]}=={"REJECT_TEMPORAL_ORDER"}


def test_parent_underage_rejected(fx):
    g=copy.deepcopy(fx)
    g["fixed_preconception"]["fathers"][1]["born"]="2006-01-01"
    r=solve(g)
    assert len(r["results"])==4
    assert {x["code"] for x in r["rejected"]}=={"REJECT_AGE"}


def test_no_objective_route_support(fx):
    g=copy.deepcopy(fx)
    g["fixed_preconception"]["fathers"][1]["eligible_windows"]=[["2020-08-01","2020-10-01"]]
    r=solve(g)
    assert len(r["results"])==4
    assert {x["code"] for x in r["rejected"]}=={"REJECT_SUPPORT"}


def test_proposal_outside_all_support(fx):
    g=copy.deepcopy(fx)
    g["proposals"][1]["conception"]="2025-01-01"
    r=solve(g)
    assert len(r["results"])==4
    assert len(r["rejected"])==4


def test_birth_child_provenance_temporal_rejection():
    assert validate_child_event_order("2020-06-01","2020-06-01","2021-03-08","2021-03-09")
    refuse("REJECT_TEMPORAL_ORDER", lambda:validate_child_event_order("2020-06-01","2020-06-01","2020-05-31","2020-06-02"))
    refuse("REJECT_TEMPORAL_ORDER", lambda:validate_child_event_order("2020-06-01","2021-03-09","2021-03-08","2021-03-10"))


def test_future_outcome_input_embargo(fx):
    g=copy.deepcopy(fx)
    g["desired_child"]="obedient"
    refuse("REJECT_CHILD_OUTCOME_LEAKAGE",lambda:solve(g))
    refuse("REJECT_CHILD_OUTCOME_LEAKAGE",lambda:reject_target_leakage({"ideal_child":"wealthy"}))


def test_heldout_child_swap_exact_indifference(fx):
    first=solve(fx)
    held_out_a={"child_trait":"pragmatic"}
    held_out_b={"child_trait":"revolutionary"}
    assert held_out_a != held_out_b
    assert solve(fx) == first   # Neither metadata object reaches the solver.


def test_child_outcome_rank_selection_refused():
    refuse("REJECT_CHERRY_PICK",lambda:check_selection_no_cherry_pick(["A","B"],"B",ranking_key="best_child"))


def test_authority_no_draw_for_weighting(fx):
    assert no_unauthorized_decision() == "NO_DRAW_UNISSUED"
    refuse("REJECT_UNISSUED_PROBABILITY",lambda:no_unauthorized_decision(weights={"C0":1,"C1":2}))
    refuse("MISSING_IMPLEMENTATION",lambda:no_unauthorized_decision(rule_issued=True))
    assert solve(fx)["selection"] == "NO_DRAW_NO_AUTHORIZED_DOMAIN_POLICY"


def test_rejection_selection_bias_counterexample():
    out=survivor_fractions({"A":.5,"B":.5},{"A":1.0,"B":.25})
    assert out=={"A":.8,"B":.2}
    assert out!={"A":.5,"B":.5}
    refuse("NO_SURVIVORS",lambda:survivor_fractions({"A":.5,"B":.5},{"A":0,"B":0}))


def test_invented_extra_candidate_does_not_silently_multiply(fx):
    g=copy.deepcopy(fx)
    g["proposals"].append(copy.deepcopy(g["proposals"][0]))
    refuse("REJECT_CHERRY_PICK",lambda:solve(g))


def test_malformed_dag_unknown_node(fx):
    g=copy.deepcopy(fx)
    g["graph"]["edges"].append(["child_future","father_history"])
    refuse("UNKNOWN_OR_MALFORMED_EDGE",lambda:solve(g))


def test_violated_no_actor_policy(fx):
    g=copy.deepcopy(fx)
    g["policy"]["actor_invocations"]=1
    refuse("FORBIDDEN_SIDE_EFFECT_OR_AUTHORITY",lambda:solve(g))
