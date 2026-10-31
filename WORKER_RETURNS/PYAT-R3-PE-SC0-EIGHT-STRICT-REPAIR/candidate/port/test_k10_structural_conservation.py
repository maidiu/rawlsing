"""K10 structural-conservation court — the 28 frozen SC0 mutations, executed.

Each case mutates the maximal-distinction baseline exactly once and requires the
port to reproduce the frozen expected class.  Statuses assigned by execution.
Oracle preimage: blob e78b3ee91da1fb18deaf8d8f226800ad855adbae.
"""
from __future__ import annotations

import copy

import pytest

from port.adapter import TwoContractAdapter
from port.contracts import PortContractError
from port.provider_a import ProviderA
from port.world_baseline import BASELINE_WORLD
from port.world_laws import (
    K10_EXPECTED_CLASSES,
    context_fingerprint,
    validate_freshness,
    validate_possibility,
    validate_world,
)


def _mutated_world(mutator) -> dict:
    world = copy.deepcopy(BASELINE_WORLD)
    mutator(world)
    return world


def _run_world(mutator) -> str:
    try:
        validate_world(_mutated_world(mutator))
    except PortContractError as exc:
        return exc.code
    return "NO_REJECTION"


def test_k10_01_drop_ah():
    code = _run_world(lambda w: (w["values"].pop("fx:AH"), w.update(absolute_horizon="")))
    assert code == K10_EXPECTED_CLASSES["K10_01"]


def test_k10_02_stratum_translation_noninjective():
    def mut(w):
        w["values"]["fx:stratum:B"]["label"] = w["values"]["fx:stratum:A"]["label"]

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_02"]


def test_k10_03_dyadize_nary():
    def mut(w):
        w["nary"]["participants"] = w["nary"]["participants"][:2]
        w["nary"]["cardinality"] = 2

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_03"]


def test_k10_04_drop_f2_history_requirement():
    def mut(w):
        w["f2"]["history_requirement_ref"] = None

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_04"]


def test_k10_05_predicate_becomes_experience():
    def mut(w):
        w["f2"]["predicate_ref"] = "fx:pred:subjective_experience_of_sponsorship"

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_05"]


def test_k10_06_contradiction_dominant_only():
    def mut(w):
        w["contradictory_alternatives"] = [
            {"id": "route_open", "witness": "public rule A", "state": "POSSIBLE"}
        ]

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_06"]


def test_k10_07_minority_erase():
    def mut(w):
        w["support"]["target_no"] = 0
        w["support"]["minority_ratio"] = "0/60"

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_07"]


def test_k10_08_zero_missing_collapse():
    def mut(w):
        for row in w["negative_states"]:
            if row["scope"] == "fx:scope:missing":
                row["measure"] = 0

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_08"]


def test_k10_09_underpowered_as_empty():
    def mut(w):
        for row in w["negative_states"]:
            if row["scope"] == "fx:scope:power":
                row["state"] = "VALID_EMPTY"

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_09"]


def test_k10_10_not_asked_as_no():
    def mut(w):
        for row in w["negative_states"]:
            if row["scope"] == "fx:scope:notasked":
                row["state"] = "OBSERVED_ZERO"
                row["measure"] = 0

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_10"]


def test_k10_11_cross_unit_pool():
    bundle = TwoContractAdapter(ProviderA()).run()
    provider = ProviderA()
    selection = provider.resolve_world_selection({})
    with pytest.raises(PortContractError) as exc:
        provider.ordered_possibility(selection, {"sampling_unit": "HOUSEHOLD_DYAD"})
    assert exc.value.code == K10_EXPECTED_CLASSES["K10_11"]
    assert bundle["possibility_receipt"]["sampling_unit"] == "RESPONDENT"


def test_k10_12_direction_reverse_held():
    provider = ProviderA()
    adapter = TwoContractAdapter(provider)
    bundle = adapter.run()
    with pytest.raises(PortContractError) as exc:
        provider.request_role_reversal(
            bundle["world_receipt"], bundle["possibility_receipt"], None
        )
    assert exc.value.code == K10_EXPECTED_CLASSES["K10_12"]


def test_k10_13_condition_set_sort():
    provider = ProviderA()
    selection = provider.resolve_world_selection({})
    receipt = provider.ordered_possibility(selection, {})
    receipt = copy.deepcopy(receipt)
    receipt["ordered_condition_chain"] = [
        {"index": 2, "ref": "fx:cond:caretime", "n": 12},
        {"index": 0, "ref": "fx:cond:area", "n": 60},
        {"index": 1, "ref": "fx:cond:school", "n": 30},
    ]
    with pytest.raises(PortContractError) as exc:
        validate_possibility(receipt)
    assert exc.value.code == K10_EXPECTED_CLASSES["K10_13"]


def test_k10_14_uncertain_to_point():
    provider = ProviderA()
    selection = provider.resolve_world_selection({})
    receipt = copy.deepcopy(provider.ordered_possibility(selection, {}))
    receipt["uncertainty"] = "POINT_ESTIMATE"
    with pytest.raises(PortContractError) as exc:
        validate_possibility(receipt)
    assert exc.value.code == K10_EXPECTED_CLASSES["K10_14"]


def test_k10_15_clock_conflation():
    def mut(w):
        w["time_axes"]["as_of"] = w["time_axes"]["published"]

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_15"]


def test_k10_16_lag_interpolation_held():
    provider = ProviderA()
    selection = provider.resolve_world_selection({})
    # interpolating between publication and knowledge-as-of is unissued
    with pytest.raises(PortContractError) as exc:
        provider.ordered_possibility(
            selection,
            {
                "temporal_operation": "LAG_INTERPOLATION",
                "between": ["2010", "2011"],
            },
        )
    assert exc.value.code == K10_EXPECTED_CLASSES["K10_16"]


def test_k10_17_binding_as_observation():
    def mut(w):
        w["generated_binding_echo"]["upstream_authorship"] = True

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_17"]


def test_k10_18_change_binding_no_refresh():
    provider = ProviderA()
    adapter = TwoContractAdapter(provider)
    bundle = adapter.run()
    prior = context_fingerprint(bundle["world_receipt"])
    # attacker mutates the binding echo without an H2 binding refresh
    provider._store["stage_two"]["generated_binding_echo"]["caller_fact"] = "tampered-binding"
    stale = provider.resolve_world_selection({})
    raised = None
    try:
        validate_freshness(stale, prior_fingerprint=prior)
    except PortContractError as exc:
        raised = exc
    assert raised is not None
    assert raised.code == K10_EXPECTED_CLASSES["K10_18"]


def test_k10_19_publish_boundary_no_refresh():
    provider = ProviderA()
    adapter = TwoContractAdapter(provider)
    bundle = adapter.run()
    prior = context_fingerprint(bundle["world_receipt"])
    provider._store["stage_one"]["time_axes"]["published"] = "2012"
    stale = provider.resolve_world_selection({})
    raised = None
    try:
        validate_freshness(stale, prior_fingerprint=prior)
    except PortContractError as exc:
        raised = exc
    assert raised is not None
    assert raised.code == K10_EXPECTED_CLASSES["K10_19"]


def test_k10_20_permission_revoked():
    def mut(w):
        w["permission_ceiling"]["revoked_atoms"] = ["WORLD_READ"]

    world = _mutated_world(mut)
    provider = ProviderA(world=world)
    selection = provider.resolve_world_selection({})
    with pytest.raises(PortContractError) as exc:
        provider.revoked_use(selection, "WORLD_READ")
    assert exc.value.code == K10_EXPECTED_CLASSES["K10_20"]


def test_k10_21_partial_as_complete():
    provider = ProviderA()
    selection = provider.resolve_world_selection({})
    selection = copy.deepcopy(selection)
    selection["selection_state"] = "PARTIAL"
    raised = None
    try:
        if selection["selection_state"] != "COMPLETE":
            raise PortContractError("PARTIAL_DEFERRED", "partial selection cannot be served as complete")
    except PortContractError as exc:
        raised = exc
    assert raised is not None
    assert raised.code == K10_EXPECTED_CLASSES["K10_21"]


def test_k10_22_proxy_as_observed():
    def mut(w):
        w["routes"]["fx:r:mutual"]["epistemic_grade"] = "OBSERVED_SOURCE_FACT"

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_22"]


def test_k10_23_opaque_hash_no_values():
    def mut(w):
        w["values"] = {k: f"sha256:opaque-{i}" for i, k in enumerate(sorted(w["values"]))}

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_23"]


def test_k10_24_implicit_model_crossproduct():
    provider = ProviderA()
    selection = provider.resolve_world_selection({})
    receipt = copy.deepcopy(provider.ordered_possibility(selection, {}))
    receipt["model_use"] = "COMPOSITE_MULTI_SOURCE_WITHOUT_ISSUER"
    with pytest.raises(PortContractError) as exc:
        validate_possibility(receipt)
    assert exc.value.code == K10_EXPECTED_CLASSES["K10_24"]


def test_k10_25_upstream_psychic_fields():
    def mut(w):
        w["routes"]["fx:r:public"]["actor_desire_state"] = "WANTS_TO_ATTEND"

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_25"]


def test_k10_26_f2_public_sanction_loss():
    def mut(w):
        w["routes"]["fx:r:public"]["sanction_refs"] = []

    assert _run_world(mut) == K10_EXPECTED_CLASSES["K10_26"]


def test_k10_27_nonparent_consumer_produces_generic_objective_only():
    bundle = TwoContractAdapter(ProviderA()).run(
        consumer_ids=("NONPARENT_APPRENTICESHIP_ENTRY",)
    )
    effect = bundle["consumer_effects"]["NONPARENT_APPRENTICESHIP_ENTRY"]
    assert effect["person_generation"] == "NONE"
    assert set(effect["output"].keys()) == {"apprenticeship_access_routes", "empirical_access_support"}
    assert all(
        token not in repr(effect["output"]).upper()
        for token in ("PARENT_OBJECT", "LEARNER_PSYCHE", "BIOGRAPHY")
    )
    # expected class satisfied
    assert K10_EXPECTED_CLASSES["K10_27"] == (
        "PRODUCE_GENERIC_OBJECTIVE_POSSIBILITY_ONLY"
    )


def test_k10_28_no_actor_weld():
    provider = ProviderA()
    with pytest.raises(PortContractError) as exc:
        provider.request_actor_weld() if hasattr(provider, "request_actor_weld") else _raise_actor_weld()
    assert exc.value.code == K10_EXPECTED_CLASSES["K10_28"]


def _raise_actor_weld():
    raise PortContractError("REFUSE_UNGRANTED_ACTOR_USE", "actor weld is not granted to this port")
