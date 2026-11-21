"""DHIKRYMULCH F6 uncertain-source partial identification, actual I03 -> S04.

Every authorization here is a TEST_ONLY, explicitly issued synthetic snapshot.
No original survey's population interval is inferred from a RAW sample rate.
"""
import pytest

from rawlsing_next.pre553_empirical_authority import AuthorityRegistry
from rawlsing_next.pre553_empirical_objects import (
    AuthoritySnapshot, canonical_json, semantic_hash,
)
from rawlsing_next.pre553_s04_partially_identified_repertoire import (
    PartialIdentificationError,
)
from rawlsing_next.pre553_s04_uncertain_repertoire import (
    BRIDGE_KIND, BRIDGE_OPERATION, CONTRACT, INTERVAL_COVERAGE,
    INTERVAL_OPERATION, UncertainRepertoire, UncertainRepertoireError,
    identify_uncertain_unobserved_overlap,
    replay_uncertain_unobserved_overlap,
    ask_uncertain_repertoire_configuration,
)
from rawlsing_next.tests.test_pre553_empirical_query import _h, _ref
from rawlsing_next.tests.test_pre553_s04_partially_identified_repertoire import (
    _observed,
)


def _f(n, d=1):
    return {"numerator": n, "denominator": d}


def _auth(*, kind, operation, scope, name, decision="ALLOW"):
    material = canonical_json(scope)
    return AuthoritySnapshot(
        typed_state=decision, decision_state=decision,
        authority_snapshot_refs=(), dependency_refs=(),
        producer_replay_locator_or_reference_root=_ref(
            "REPLAY_ROOT", "issued-" + name
        ),
        authority_id="SYNTHETIC_UNCERTAINTY_" + name,
        authority_version="1.0.0",
        authority_content_hash=_h(name + material + decision),
        authority_kind=kind,
        governed_operations=(operation,),
        governed_object_families=("EmpiricalFact@1.0.0",),
        scope_envelope=scope,
        effective_time_or_interval="SYNTHETIC_1972",
        parent_authority_refs=(),
        negative_limit_refs=(),
        supersession_refs=(),
        interpretation_semantics_fingerprint=_h(
            "synthetic-explicit-design-issuer"
        ),
        replay_protocol_ref=_ref("REPLAY_PROTOCOL", name),
    )


POP = _ref("TARGET_POPULATION", "qualified-common-1972").as_dict()
DESIGN = _ref("DESIGN_METHOD", "synthetic-sampling-design").as_dict()
SELECT = _ref("SELECTION_COVERAGE_METHOD", "synthetic-selection-aware").as_dict()


def _method_scope(obs, low, high, alpha=_f(1,20), *, modifications=None):
    m = obs.material()
    scope = {
        "source_universe_refs": [m["universe_ref"]],
        "source_universe_ref": m["universe_ref"],
        "release_ref": m["release_ref"],
        "s04_observation_ref": obs.ref.as_dict(),
        "risk_set_ref": m["risk_set_ref"],
        "query_ref": m["query_ref"],
        "fact_ref": m["fact_ref"],
        "predicate_ref": m["predicate_ref"],
        "replay_ref": m["replay_ref"],
        "target_ref": m["target_refs"][0],
        "response_semantics_ref": m["response_semantics_ref"],
        "measure_basis_ref": m["measure_basis_ref"],
        "event_cell": "1",
        "coverage_kind": INTERVAL_COVERAGE,
        "target_population_ref": POP,
        "population_period": "SYNTHETIC_1972",
        "survey_design_method_ref": DESIGN,
        "selection_coverage_method_ref": SELECT,
        "parameter_lower": low, "parameter_upper": high,
        "error_probability_upper": alpha,
        "uses_observed_raw_as_population_prevalence": False,
    }
    if modifications:
        scope.update(modifications)
    return scope


def _bridge_scope(a, b, left_ref, right_ref, *, modifications=None):
    x, y = a.material(), b.material()
    scope = {
        "source_universe_refs": [x["universe_ref"], y["universe_ref"]],
        "release_refs": [x["release_ref"], y["release_ref"]],
        "s04_knowledge_refs": [a.ref.as_dict(), b.ref.as_dict()],
        "risk_set_refs": [x["risk_set_ref"], y["risk_set_ref"]],
        "target_refs": [x["target_refs"][0], y["target_refs"][0]],
        "response_semantics_refs": [
            x["response_semantics_ref"], y["response_semantics_ref"],
        ],
        "measure_basis_refs": [
            x["measure_basis_ref"], y["measure_basis_ref"],
        ],
        "predicate_refs": [x["predicate_ref"], y["predicate_ref"]],
        "interval_authority_refs": [
            left_ref.as_dict(), right_ref.as_dict(),
        ],
        "target_population_ref": POP,
        "population_period": "SYNTHETIC_1972",
        "population_bridge_kind": BRIDGE_KIND,
        "sample_pooling_state": "NO_SOURCE_POOLING",
    }
    if modifications:
        scope.update(modifications)
    return scope


def _setup(
    *,
    a_n=10, b_n=10,
    left_mod=None, right_mod=None, bridge_mod=None,
    left_decision="ALLOW", right_decision="ALLOW", bridge_decision="ALLOW",
    l_interval=(_f(3,5), _f(4,5)),
    r_interval=(_f(1,2), _f(7,10)),
    alpha=_f(1,20), beta=_f(1,20),
):
    a = _observed("uncertain-a-" + str(a_n), 7, a_n)
    b = _observed("uncertain-b-" + str(b_n), 6, b_n)
    la = _auth(
        kind="UNCERTAINTY_METHOD", operation=INTERVAL_OPERATION,
        scope=_method_scope(a, *l_interval, alpha, modifications=left_mod),
        name="left-" + str(a_n), decision=left_decision,
    )
    ra = _auth(
        kind="UNCERTAINTY_METHOD", operation=INTERVAL_OPERATION,
        scope=_method_scope(b, *r_interval, beta, modifications=right_mod),
        name="right-" + str(b_n), decision=right_decision,
    )
    bridge = _auth(
        kind="SOURCE_UNIVERSE_RELATION", operation=BRIDGE_OPERATION,
        scope=_bridge_scope(
            a, b, la.authority_ref, ra.authority_ref,
            modifications=bridge_mod,
        ),
        name="bridge-" + str(a_n) + "-" + str(b_n),
        decision=bridge_decision,
    )
    reg = AuthorityRegistry((la, ra, bridge))
    return (a, b, reg, la.authority_ref, ra.authority_ref, bridge.authority_ref)


def _invoke(fixture):
    a, b, reg, l, r, bridge = fixture
    return identify_uncertain_unobserved_overlap(
        left=a, right=b,
        left_event_cell="1", right_event_cell="1",
        registry=reg,
        left_interval_authority=l,
        right_interval_authority=r,
        common_population_authority=bridge,
    )


def _replay(receipt, fixture):
    a, b, reg, l, r, bridge = fixture
    return replay_uncertain_unobserved_overlap(
        receipt=receipt, left=a, right=b,
        left_event_cell="1", right_event_cell="1",
        registry=reg,
        left_interval_authority=l,
        right_interval_authority=r,
        common_population_authority=bridge,
    )


def test_exact_source_unary_to_sharp_issued_population_feasible_polytope():
    fixture = _setup()
    receipt = _invoke(fixture)
    m = receipt.material()
    assert m["contract"] == CONTRACT
    assert m["state"] == "SHARP_PARTIAL_ID_UNDER_ISSUED_POPULATION_INTERVALS"
    assert m["bounds"] == {
        "A_AND_B": {"lower": _f(1,10), "upper": _f(7,10)},
        "A_ONLY": {"lower": _f(0), "upper": _f(1,2)},
        "B_ONLY": {"lower": _f(0), "upper": _f(2,5)},
        "NEITHER": {"lower": _f(0), "upper": _f(2,5)},
    }
    assert m["simultaneous_coverage_lower_bound"] == _f(9,10)
    assert m["marginal_left"]["source_local_raw_fraction"] == _f(7,10)
    assert m["marginal_right"]["source_local_raw_fraction"] == _f(3,5)
    assert m["selected_coupling"] is None
    assert m["population_joint_point_estimate"] is None
    assert m["no_new_i03_query"] is True
    low = m["witness_couplings"]["MIN_A_AND_B"]
    high = m["witness_couplings"]["MAX_A_AND_B"]
    assert low["cells"] == {
        "A_AND_B": _f(1,10), "A_ONLY": _f(1,2),
        "B_ONLY": _f(2,5), "NEITHER": _f(0),
    }
    assert high["cells"] == {
        "A_AND_B": _f(7,10), "A_ONLY": _f(1,10),
        "B_ONLY": _f(0), "NEITHER": _f(1,5),
    }
    assert _replay(receipt, fixture).ref == receipt.ref


@pytest.mark.parametrize("a,b,expected", [
    (True, True, (_f(1,10), _f(7,10))),
    (True, False, (_f(0), _f(1,2))),
    (False, True, (_f(0), _f(2,5))),
    (False, False, (_f(0), _f(2,5))),
])
def test_qualified_consumer_returns_only_source_replayed_feasible_interval(a,b,expected):
    fixture = _setup()
    receipt = _invoke(fixture)
    src_a, src_b, reg, la, ra, bridge = fixture
    v = ask_uncertain_repertoire_configuration(
        relation=receipt, left=src_a, right=src_b,
        left_event_cell="1", right_event_cell="1",
        event_a=a, event_b=b, registry=reg,
        left_interval_authority=la, right_interval_authority=ra,
        common_population_authority=bridge,
    )
    assert v["state"] == "QUALIFIED_PARAMETER_COMPATIBILITY_INTERVAL"
    assert v["interval"] == {"lower":expected[0],"upper":expected[1]}
    assert v["selected_coupling"] is None
    assert v["person_or_respondent_created"] is False


def test_without_any_authority_local_raw_facts_survive_but_no_population_bounds():
    a, b, _, _, _, _ = _setup()
    receipt = identify_uncertain_unobserved_overlap(
        left=a, right=b, left_event_cell="1", right_event_cell="1"
    )
    m = receipt.material()
    assert m["state"] == "HELD_ISSUED_POPULATION_INTERVALS_OR_BRIDGE_MISSING"
    assert m["marginal_left"]["source_local_raw_fraction"] == _f(7,10)
    assert m["marginal_right"]["source_local_raw_fraction"] == _f(3,5)
    assert m["bounds"] is None
    assert m["simultaneous_coverage_lower_bound"] is None


@pytest.mark.parametrize("changes", [
    {"left_mod":{"uses_observed_raw_as_population_prevalence":True}},
    {"right_mod":{"coverage_kind":"IID_BOOTSTRAP_SENSITIVITY_ONLY"}},
    {"left_mod":{"s04_observation_ref":_ref("S04_FOREIGN","wrong").as_dict()}},
    {"right_mod":{"target_ref":_ref("FOREIGN_TARGET","swapped").as_dict()}},
    {"left_mod":{"parameter_lower":_f(9,10),"parameter_upper":_f(2,5)}},
    {"right_mod":{"parameter_lower":_f(-1,10)}},
    {"right_mod":{"population_period":"SYNTHETIC_1985"}},
    {"left_decision":"DENY"},
    {"bridge_decision":"DEFER"},
    {"bridge_mod":{"population_bridge_kind":"SAME_COUNTRY_YEAR_IS_ENOUGH"}},
    {"bridge_mod":{"target_population_ref":_ref("OTHER_POP","foreign").as_dict()}},
    {"bridge_mod":{"sample_pooling_state":"POOL_SAMPLES"}},
    {"bridge_mod":{"interval_authority_refs":[
        _ref("AUTH","stale").as_dict(),_ref("AUTH","other").as_dict()
    ]}},
    {"bridge_mod":{"response_semantics_refs":[
        _ref("SEM","wrong").as_dict(),_ref("SEM","also-wrong").as_dict()
    ]}},
])
def test_ambiguous_mismatched_or_negative_science_does_not_launder_population_claim(changes):
    fixture = _setup(**changes)
    m = _invoke(fixture).material()
    assert m["state"] == "HELD_ISSUED_POPULATION_INTERVALS_OR_BRIDGE_MISSING"
    assert m["bounds"] is None
    assert m["simultaneous_coverage_lower_bound"] is None
    assert m["marginal_left"]["source_local_raw_fraction"] == _f(7,10)


def test_separate_survey_sample_sizes_can_legitimately_differ():
    # Unlike F6's exact finite census path, qualifying parameter intervals
    # may come from samples with unequal n, but only if the source authority
    # issues same-population design-correct estimates for each.
    fixture = _setup(a_n=10,b_n=13)
    m = _invoke(fixture).material()
    assert m["state"] == "SHARP_PARTIAL_ID_UNDER_ISSUED_POPULATION_INTERVALS"
    assert m["marginal_left"]["eligible_raw_n"] == 10
    assert m["marginal_right"]["eligible_raw_n"] == 13
    assert m["bounds"]["A_AND_B"] == {
        "lower":_f(1,10), "upper":_f(7,10),
    }


def test_coverage_is_union_bound_not_independent_product():
    fixture = _setup(alpha=_f(1,20), beta=_f(1,10))
    m = _invoke(fixture).material()
    assert m["simultaneous_coverage_lower_bound"] == _f(17,20)
    assert "BOOLE_UNION_BOUND" in m["coverage_rule"]


def test_source_interval_can_differ_from_sample_raw_rate_without_reinterpreting_raw():
    # A source-authorized population interval is NOT recomputed by this
    # consumer from the source's unweighted sample prevalence.
    fixture = _setup(
        l_interval=(_f(1,5),_f(3,10)),
        r_interval=(_f(4,5),_f(9,10)),
    )
    m = _invoke(fixture).material()
    assert m["state"] == "SHARP_PARTIAL_ID_UNDER_ISSUED_POPULATION_INTERVALS"
    assert m["bounds"]["A_AND_B"] == {
        "lower":_f(0), "upper":_f(3,10),
    }
    assert m["marginal_left"]["source_local_raw_fraction"] == _f(7,10)


def test_same_source_marginal_is_not_an_unobserved_joint():
    a, _, _, _, _, _ = _setup()
    with pytest.raises(UncertainRepertoireError, match="SAME_SOURCE_USE_RESPONDENT_LEVEL_I03"):
        identify_uncertain_unobserved_overlap(
            left=a,right=a,left_event_cell="1",right_event_cell="1"
        )


def test_unsupported_native_event_cell_cannot_be_selected():
    a,b,_,_,_,_ = _setup()
    with pytest.raises(PartialIdentificationError, match="POSITIVE_CELL_NOT_IN_SOURCE_DOMAIN"):
        identify_uncertain_unobserved_overlap(
            left=a,right=b,left_event_cell="undocumented",right_event_cell="1"
        )


def test_self_rehashed_forged_claim_cannot_pass_cold_external_authority_replay():
    fixture = _setup()
    truth = _invoke(fixture)
    counterfeit = truth.material()
    counterfeit["bounds"]["A_AND_B"]["lower"] = _f(0)
    rehashed = UncertainRepertoire(
        canonical_json(counterfeit), semantic_hash(counterfeit)
    )
    with pytest.raises(UncertainRepertoireError, match="SOURCE_REPLAY_FAILED"):
        _replay(rehashed,fixture)
    src_a,src_b,reg,la,ra,bridge=fixture
    with pytest.raises(UncertainRepertoireError, match="SOURCE_REPLAY_FAILED"):
        ask_uncertain_repertoire_configuration(
            relation=rehashed,
            left=src_a,right=src_b,
            left_event_cell="1",right_event_cell="1",
            event_a=True,event_b=True,
            registry=reg,left_interval_authority=la,
            right_interval_authority=ra,common_population_authority=bridge,
        )


def test_held_consumer_remains_held_not_an_impossible_character():
    fixture=_setup()
    a,b,_,_,_,_=fixture
    held=identify_uncertain_unobserved_overlap(
        left=a,right=b,left_event_cell="1",right_event_cell="1"
    )
    v=ask_uncertain_repertoire_configuration(
        relation=held,left=a,right=b,left_event_cell="1",right_event_cell="1",
        event_a=True,event_b=True,
    )
    assert v["state"]=="HELD_NOT_AN_IMPOSSIBLE_PERSON_CLAIM"
    assert v["interval"] is None
    assert v["person_or_respondent_created"] is False


def test_synthetic_exact_point_interval_reuses_existing_F6_constraint_mathematics():
    # New code *extends* F6; when issued intervals collapse to the same exact
    # marginals, the resulting Fréchet bounds agree with inherited finite F6.
    fixture = _setup(
        l_interval=(_f(7,10),_f(7,10)),
        r_interval=(_f(3,5),_f(3,5)),
    )
    m = _invoke(fixture).material()
    assert m["bounds"]["A_AND_B"] == {
        "lower":_f(3,10),"upper":_f(3,5)
    }
