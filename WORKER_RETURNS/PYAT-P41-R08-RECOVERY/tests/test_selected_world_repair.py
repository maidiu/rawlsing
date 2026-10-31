from dataclasses import replace
import json

import pytest

from selected_world_repair import (
    build_source_owned_joint,
    cold_restore,
    read_selected_world,
    rebind_source_owned_joint,
    stale_mutation_with_old_contract,
)


def test_source_owned_value_change_rebinds_contract_and_changes_output():
    before_world = build_source_owned_joint({(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3})
    before = read_selected_world(before_world, "P_Q86A_given_Q86B_1")
    after_world = rebind_source_owned_joint(before_world, {(0, 0): 3, (0, 1): 1, (1, 0): 2, (1, 1): 2})
    after = read_selected_world(after_world, "P_Q86A_given_Q86B_1")
    assert before["status"] == after["status"] == "COMPUTED"
    assert before["exact_probabilities"]["1"] == {"$exact_fraction": [3, 4]}
    assert after["exact_probabilities"]["1"] == {"$exact_fraction": [1, 2]}
    assert before["raw_denominator_support"] == after["raw_denominator_support"] == 4
    assert before["source_value_dependency"]["contract_hash"] != after["source_value_dependency"]["contract_hash"]
    assert before["source_value_dependency"]["used_input_refs"] != after["source_value_dependency"]["used_input_refs"]


def test_old_contract_with_changed_numeric_values_is_refused():
    world = build_source_owned_joint({(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3})
    stale = stale_mutation_with_old_contract(world, {(0, 0): 3, (0, 1): 1, (1, 0): 2, (1, 1): 2})
    result = read_selected_world(stale, "P_Q86A_given_Q86B_1")
    assert result["status"] == "REFUSED"
    assert result["reason"] == "SOURCE_VALUE_CONTRACT_MISMATCH"


def test_zero_support_is_distinct_from_missing_channel():
    zero_world = build_source_owned_joint({(0, 0): 2, (0, 1): 3, (1, 0): 0, (1, 1): 0})
    zero = read_selected_world(zero_world, "P_Q86A_given_Q86B_1")
    missing = read_selected_world(zero_world, "P_MISSING")
    assert (zero["status"], zero["reason"]) == ("ZERO_SUPPORT", "ZERO_DENOMINATOR_ABSTENTION")
    assert (missing["status"], missing["reason"]) == ("NO_SUPPORT", "NO_MATCHING_CHANNEL")


def test_cold_restore_preserves_exact_read_and_rejects_tamper():
    world = build_source_owned_joint({(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3})
    baseline = read_selected_world(world, "P_Q86A_given_Q86B_1")
    restored = cold_restore(world, json.dumps(world.as_dict()))
    assert read_selected_world(restored, "P_Q86A_given_Q86B_1") == baseline
    payload = world.as_dict()
    payload["channels"][2]["raw_numerator_support"] = 2
    with pytest.raises(ValueError, match="RESTORED_CONTENT_HASH_MISMATCH"):
        cold_restore(world, payload)


def test_live_channel_tamper_is_refused_and_restore_is_green():
    world = build_source_owned_joint({(0, 0): 3, (0, 1): 1, (1, 0): 1, (1, 1): 3})
    tampered = stale_mutation_with_old_contract(world, {(0, 0): 3, (0, 1): 1, (1, 0): 2, (1, 1): 2})
    assert read_selected_world(tampered, "P_Q86A_given_Q86B_1")["reason"] == "SOURCE_VALUE_CONTRACT_MISMATCH"
    assert read_selected_world(world, "P_Q86A_given_Q86B_1")["status"] == "COMPUTED"
